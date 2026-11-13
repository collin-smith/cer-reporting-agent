"""The strictest-of-layouts check (D33): layout variants and how decisions combine. $0, no model calls."""

from cer_agent.workflow import combine, layouts


def pk(status, deadline, route="clear-cut", types=(), missing=(), cites=(), triggers=()):
    return {"status": status, "deadline": deadline, "due_at": None, "route": route, "incident_types": list(types),
            "deadline_rules": [deadline] if deadline else [], "missing": list(missing), "citations": list(cites),
            "route_triggers": list(triggers), "outcomes_considered": 1, "extracted": {"s": status}}  # fmt: skip


def test_layouts_drop_variants_the_normaliser_makes_identical():
    one_line = "Small sheen at the meter skid, cleaned up."
    assert list(layouts(one_line)) == ["as_written"]
    long = "First paragraph, " + "with plenty of words to wrap " * 4 + "here.\n\nSecond."
    out = layouts(long)
    assert list(out) == ["as_written", "noblank", "wrap72"] and out["noblank"].count("\n\n") == 0


def test_agreement_keeps_the_answer():
    out = combine({"as_written": pk("reportable", "T24", types=["INC-c"]), "wrap72": pk("reportable", "T24")})
    assert (out["status"], out["deadline"], out["route"]) == ("reportable", "T24", "clear-cut")
    assert "PREC" not in out["citations"] and "LAYOUT" not in out["route_triggers"]
    assert out["layouts"]["wrap72"]["status"] == "reportable"


def test_disagreement_on_reportability_is_precautionary_earliest_deadline_and_judgment():
    out = combine({"as_written": pk("not reportable", None, missing=["volume"]),
                   "noblank": pk("reportable", "T24", types=["INC-c"], cites=["INC-c"]),
                   "wrap72": pk("reportable", "T3", types=["INC-c"])})  # fmt: skip
    assert (out["status"], out["deadline"], out["route"]) == ("precautionary", "T3", "judgment")
    assert out["deadline_rules"] == ["T3"] and out["incident_types"] == ["INC-c"]
    assert "PREC" in out["citations"] and "LAYOUT" in out["route_triggers"] and out["missing"] == ["volume"]
    assert out["extracted"] == {"s": "not reportable"}  # the reviewer sees the report as written


def test_a_deadline_disagreement_alone_is_not_precautionary_but_goes_to_a_person():
    out = combine({"as_written": pk("reportable", "T24"), "wrap72": pk("reportable", "T3")})
    assert (out["status"], out["deadline"], out["route"]) == ("reportable", "T3", "judgment")
    assert "PREC" not in out["citations"]


def test_all_not_reportable_stays_not_reportable():
    out = combine({"as_written": pk("not reportable", None), "noblank": pk("not reportable", None)})
    assert (out["status"], out["deadline"], out["incident_types"]) == ("not reportable", None, [])


def test_strict_readings_nest_under_the_callers_span(monkeypatch):
    import io
    import json

    from cer_agent import tracing, workflow

    def fake_read(client, model_id, text, received, fallback):
        with tracing.span("extract", layout=text):
            return {"facts": {}, "model": "primary", "input_tokens": 1, "output_tokens": 1}

    monkeypatch.setattr(workflow, "read", fake_read)
    monkeypatch.setattr(workflow, "layouts", lambda report: {"as_written": "A", "b": "B", "c": "C"})
    monkeypatch.setattr(workflow, "packet", lambda facts, x: {})
    monkeypatch.setattr(workflow, "combine", lambda pks: {"status": "reportable"})
    monkeypatch.setattr(tracing, "_provider", None)
    out = io.StringIO()
    provider = tracing.setup(None, stream=out)
    with tracing.span("gate.triage"):
        r = workflow.run_strict(None, "m", "report")
    provider.shutdown()
    monkeypatch.setattr(tracing, "_provider", None)
    spans = [json.loads(line) for line in out.getvalue().splitlines()]
    (root,) = [s for s in spans if s["name"] == "gate.triage"]
    reads = [s for s in spans if s["name"] == "extract"]
    assert len(reads) == 3 and all(s["parent_id"] == root["span_id"] for s in reads)
    assert r["input_tokens"] == 3
