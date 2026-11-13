import pytest

from cer_agent import approval


def test_marks_follow_d25_from_discovery():
    assert approval.marks("T3", 0, 1) == [60, 150, 180]
    assert approval.marks("T3", 70, 1) == [1, 80, 110]  # past the backup mark already: escalate at once
    assert approval.marks("T24", 0, 60) == [480 * 60, 1200 * 60, 1440 * 60]
    assert approval.marks(None, 0, 1) == [480, 1200, 1440]  # not reportable still waits for a person


@pytest.fixture
def recorded(monkeypatch):
    log = []
    monkeypatch.setattr(approval, "_table", lambda: None)
    monkeypatch.setattr(approval, "_append", lambda t, cid, ev, **sets: log.append((ev["event"], sets)))
    monkeypatch.setattr(approval, "notify", lambda t, cid, who, msg: log.append(("paged", who)))
    return log


def test_escalate_pages_each_level_then_goes_overdue(recorded, monkeypatch):
    monkeypatch.setattr(approval.time, "time", lambda: 1000.0)
    state = {"case_id": "X", "deadline": "T3", "level": 0, "start": 1000, "marks": [60, 150, 180]}
    s1 = approval.escalate({"case": state})
    assert (s1["level"], s1["wait_s"], s1["overdue"]) == (1, 150, False)
    s2 = approval.escalate({"case": s1})
    assert (s2["level"], s2["wait_s"]) == (2, 180)
    s3 = approval.escalate({"case": s2})
    assert s3["overdue"] is True
    assert recorded == [("paged", "backup"), ("paged", "primary+backup"), ("overdue", {"status": "OVERDUE"}),
                        ("paged", "primary+backup")]  # fmt: skip


def test_park_marks_escalated_from_level_two(recorded):
    approval.park({"case": {"case_id": "X", "level": 2, "wait_s": 30}, "token": "tok"})
    assert recorded[0][1]["status"] == "ESCALATED"


def test_reject_needs_a_reason(recorded):
    with pytest.raises(ValueError):
        approval.close({"case": {"case_id": "X", "level": 0}, "decision": {"decision": "reject", "by": "C"}})
    with pytest.raises(SystemExit):
        approval.decide("X", "reject", "C")


class FakeBedrock:
    def __init__(self, response):
        self.response = response

    def apply_guardrail(self, **kw):
        return self.response


def test_guardrail_flags_keep_medium_and_up_and_topics():
    r = {"action": "GUARDRAIL_INTERVENED", "assessments": [{
        "contentPolicy": {"filters": [{"type": "PROMPT_ATTACK", "confidence": "MEDIUM"},
                                      {"type": "VIOLENCE", "confidence": "LOW"}]},
        "topicPolicy": {"topics": [{"name": "reporting-exemption"}]}}], "usage": {"topicPolicyUnits": 1}}  # fmt: skip
    flags, usage = approval.guardrail_flags(FakeBedrock(r), "g", "text")
    assert flags == ["prompt attack (medium confidence)", "denied topic: reporting-exemption"]
    assert approval._guard_cost(usage) == pytest.approx(0.00015)


def test_mask_draft_uses_masked_text_only_when_intervened():
    hit = {"action": "GUARDRAIL_INTERVENED", "outputs": [{"text": "Call {PHONE}"}],
           "assessments": [{"sensitiveInformationPolicy": {"piiEntities": [{"type": "PHONE"}]}}]}  # fmt: skip
    assert approval.mask_draft(FakeBedrock(hit), "g", "Call 403-555-0187")[:2] == ("Call {PHONE}", ["PHONE"])
    miss = {"action": "NONE", "outputs": [], "assessments": []}
    assert approval.mask_draft(FakeBedrock(miss), "g", "No PII")[0] == "No PII"


def test_override_must_match_the_draft():
    prec = "# Draft Preliminary Incident Report\n**PIR-3 Precautionary:** Yes. In doubt.\n"
    assert "edit PIR-3" in approval.override_mismatch("reportable", prec)
    assert approval.override_mismatch("precautionary", prec) is None
    assert approval.override_mismatch("reportable", prec.replace("Yes. In doubt.", "No.")) is None
    assert "file note" in approval.override_mismatch("not reportable", prec)
    assert approval.override_mismatch("not reportable", "# File note: not reportable to the CER\n") is None


def test_triage_failure_goes_to_a_person(monkeypatch):
    calls = []

    class Table:
        def update_item(self, **kw):
            calls.append(kw)

    monkeypatch.setattr(approval, "_table", lambda: Table())
    monkeypatch.setattr(approval, "notify", lambda t, cid, who, msg: calls.append(("paged", who, msg)))
    monkeypatch.setenv("TIME_SCALE", "1")
    err = {"Error": "ModelErrorException", "Cause": '{"errorMessage": "Model produced invalid sequence"}'}
    state = approval.triage_failed({"case_id": "X", "report": "Fire at the station.", "elapsed_min": 0,
                                    "error": err})  # fmt: skip
    values = calls[0]["ExpressionAttributeValues"]
    assert values[":d"] == "0000"  # top of the queue
    assert "Fire at the station." in values[":n"] and values[":f"] == ["triage failed: ModelErrorException"]
    assert calls[1][:2] == ("paged", "primary")
    assert (state["deadline"], state["marks"]) == ("T3", [60, 150, 180])


def test_draft_falls_back_then_renders_from_the_rules(monkeypatch):
    from botocore.exceptions import ClientError

    from cer_agent import drafter

    down = ClientError({"Error": {"Code": "ServiceUnavailableException", "Message": "x"}}, "Converse")

    def fake_draft(client, model, report, pk, operator):
        if client == "down":
            raise down
        return {"text": f"drafted by {model}", "input_tokens": 10, "output_tokens": 5}

    monkeypatch.setattr(drafter, "draft", fake_draft)
    pk = {"status": "reportable", "deadline": "T24"}
    monkeypatch.setattr(drafter, "render", lambda pk, fields, op: f"rules draft {fields}")
    d = approval.draft_with_fallback(("down", "nova"), ("up", "haiku"), "report", pk, None)
    assert (d["model"], d["text"], d["errors"]) == ("fallback", "drafted by haiku", ["ServiceUnavailableException"])
    d = approval.draft_with_fallback(("down", "nova"), ("down", "haiku"), "Fire at the station.", pk, None)
    assert d["model"] == "rules only" and "rules draft {}" in d["text"] and d["text"].endswith("Fire at the station.")
    assert "blank because no model wrote them" in d["text"]
    d = approval.draft_with_fallback(("down", "nova"), (None, None), "r", pk, None)  # no fallback configured
    assert d["errors"] == ["ServiceUnavailableException"] and d["model"] == "rules only"


def test_emit_writes_nothing_outside_the_observability_window(monkeypatch, capsys):
    monkeypatch.setattr(approval, "_observing", None)
    monkeypatch.delenv("OBSERVABILITY", raising=False)
    approval.emit({"Overdue": 1}, case_id="CL-001")
    assert capsys.readouterr().out == ""
    monkeypatch.setattr(approval, "_observing", None)


def test_emit_writes_one_emf_line_in_the_window(monkeypatch, capsys):
    import json

    from cer_agent import tracing

    monkeypatch.setattr(approval, "_observing", None)
    monkeypatch.setenv("OBSERVABILITY", "on")
    monkeypatch.setattr(tracing, "setup", lambda path, stream=None: None)
    approval.emit({"Fallbacks": 2}, case_id="CL-010", cost_usd=0.001)
    line = json.loads(capsys.readouterr().out)
    (directive,) = line["_aws"]["CloudWatchMetrics"]
    assert directive["Namespace"] == "CER/Gate" and directive["Dimensions"] == [[]]
    assert directive["Metrics"] == [{"Name": "Fallbacks", "Unit": "Count"}]
    assert line["Fallbacks"] == 2 and line["case_id"] == "CL-010"
    monkeypatch.setattr(approval, "_observing", None)


def test_overdue_emits_its_metric(recorded, monkeypatch):
    sent = []
    monkeypatch.setattr(approval, "emit", lambda metrics, **props: sent.append((metrics, props)))
    state = {"case_id": "CL-007", "deadline": "T3", "level": 2, "start": 0, "marks": [], "wait_s": 1}
    assert approval.escalate({"case": state})["overdue"] is True
    assert sent == [({"Overdue": 1}, {"case_id": "CL-007", "deadline": "T3"})]


def test_handler_wraps_each_step_in_a_root_span(monkeypatch):
    import io
    import json

    from cer_agent import tracing

    monkeypatch.setattr(tracing, "_provider", None)
    out = io.StringIO()
    provider = tracing.setup(None, stream=out)
    monkeypatch.setattr(approval, "_observing", True)
    monkeypatch.setenv("_X_AMZN_TRACE_ID", "Root=1-abc-def;Parent=123;Sampled=1")
    monkeypatch.setattr(approval, "park", lambda event: None)
    approval.handler({"step": "park", "case": {"case_id": "NO-090"}, "token": "t"})
    provider.shutdown()
    monkeypatch.setattr(tracing, "_provider", None)
    monkeypatch.setattr(approval, "_observing", None)
    (s,) = map(json.loads, out.getvalue().splitlines())
    assert s["name"] == "gate.park" and s["attributes"]["cer.case_id"] == "NO-090"
    assert s["attributes"]["cer.xray_trace_id"] == "1-abc-def"
