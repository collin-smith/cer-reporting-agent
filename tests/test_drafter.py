"""The notice drafter: rendering from the packet, the $0 checks, and the model call with a stub client."""

from cer_agent.drafter import NARRATIVE, NOT_STATED, check, draft, render

REPORT = """Found a leak at the Elm Creek station at 09:30. About 8 m3 of crude in the road ditch past the fence.
Shut in the line, vac truck on the way. Call me at 403-555-0199. - J. Doe, operator"""


def pk(status="reportable", deadline="T3", rules=("T3-LVP",), types=("INC-d",), missing=(), route="clear-cut",
       triggers=(), cites=None, suspicious=False):  # fmt: skip
    return {"status": status, "deadline": deadline, "deadline_rules": list(rules), "incident_types": list(types),
            "due_at": "2026-09-17T12:30:00" if deadline else None, "missing": list(missing), "route": route,
            "route_triggers": list(triggers), "citations": cites or [*types, *rules, "DIR-84"],
            "suspicious_instructions": suspicious}  # fmt: skip


FIELDS = {k: None for k in NARRATIVE} | {
    "how_discovered": "Found by the station operator.",
    "specific_details": "About 8 m3 of crude oil.",
    "affected_lands": "Road ditch past the station fence.",
}


def test_render_takes_status_deadline_and_reasons_from_the_packet():
    text = render(pk(), FIELDS, "Prairie Midstream Ltd.")
    assert "Verbal and written notice within 3 hours" in text and "2026-09-17 12:30" in text
    assert "**PIR-4 Discovered:** 2026-09-17 09:30" in text
    assert "**PIR-3 Precautionary:** No." in text and "DIR-84" in text and "T3-LVP: 3-hour notice" in text
    assert "INC-d" in text and "Prairie Midstream Ltd." in text
    assert f"**PIR-10 Facility:** {NOT_STATED}" in text and "Also not in the report:" in text


def test_precautionary_says_so_and_mentions_relief():
    text = render(pk(status="precautionary", rules=("T3-LVP", "PREC"), missing=["lands"]), FIELDS)
    assert "**PIR-3 Precautionary:** Yes" in text and "RELIEF" in text
    assert "Where did the product go" in text
    assert "stricter reading" not in text  # that line is for a reportable case whose deadline PREC set


def test_reportable_at_the_stricter_reading_says_so():
    text = render(pk(rules=("T3-LVP", "PREC")), FIELDS)
    assert "taken at the stricter reading" in text and "**PIR-3 Precautionary:** No." in text


def test_judgment_and_suspicious_reports_are_flagged_to_the_reviewer():
    text = render(pk(route="judgment", triggers=["LAYOUT", "U2-NEAR"], suspicious=True), FIELDS)
    assert "Reviewer decision needed" in text and "layout" in text and "within 25%" in text
    assert text.startswith("> **Warning:**")


def test_not_reportable_is_a_file_note():
    text = render(pk(status="not reportable", deadline=None, rules=(), types=(), cites=["OUT-LVP15"]), None)
    assert text.startswith("# File note") and "OUT-LVP15" in text and "PIR-" not in text


def test_check_flags_invented_numbers_rule_talk_and_personal_data():
    ok = {"specific_details": "About 8.0 m3 of crude found at 9:30.", "actions": "Line shut in; vac truck called.",
          "narrative": "The crew put out the small grass fire."}  # fmt: skip
    assert check(ok, REPORT) == []
    bad = {"specific_details": "About 12 m3 of crude.", "narrative": "This is reportable within 3 hours.",
           "actions": "Contact 403-555-0199.", "facility": "Cited under T3-LVP."}  # fmt: skip
    flags = check(bad, REPORT)
    assert any("number not in report (12)" in f for f in flags)
    assert any(f.startswith("narrative: rule or deadline") for f in flags)
    assert any(f == "actions: phone" for f in flags) and any(f.startswith("facility: rule") for f in flags)


class Stub:
    def __init__(self, fields, fail_first=False):
        self.fields, self.fail_first, self.calls = fields, fail_first, []

    def converse(self, **kw):
        self.calls.append(kw)
        if self.fail_first and len(self.calls) == 1:
            e = Exception("invalid sequence as part of ToolUse")
            e.response = {"Error": {"Code": "ModelErrorException"}}
            raise e
        return {"output": {"message": {"content": [{"toolUse": {"input": self.fields}}]}},
                "usage": {"inputTokens": 900, "outputTokens": 200}}  # fmt: skip


def test_draft_calls_the_model_with_the_report_only_and_retries_hotter():
    stub = Stub(FIELDS, fail_first=True)
    d = draft(stub, "arn", REPORT, pk(), "Prairie Midstream Ltd.")
    assert len(stub.calls) == 2 and stub.calls[1]["inferenceConfig"]["temperature"] > 0
    sent = stub.calls[0]["messages"][0]["content"][0]["text"]
    assert "Elm Creek" in sent and "T3" not in sent and "reportable" not in sent  # the model never sees the decision
    assert d["flags"] == [] and d["retries"] == 1 and "About 8 m3" in d["text"]


def test_not_reportable_makes_no_model_call():
    stub = Stub(FIELDS)
    d = draft(stub, "arn", REPORT, pk(status="not reportable", deadline=None, rules=(), types=(), cites=["OUT-VENT"]))
    assert stub.calls == [] and d["fields"] is None and d["input_tokens"] == 0


def test_null_in_words_is_not_stated_and_gps_is_always_asked_for():
    text = render(pk(), FIELDS | {"actions": "null", "facility": " None. "})
    assert f"**PIR-9 Actions:** {NOT_STATED}" in text and f"**PIR-10 Facility:** {NOT_STATED}" in text
    assert "GPS coordinates to 8 decimals (PIR-11)" in text
