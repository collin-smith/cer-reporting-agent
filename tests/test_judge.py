"""Grading drafts: the $0 code checks, the judge call with a stub client, the quote check, and scoring."""

from cer_agent import drafter
from cer_agent import judge as j

REPORT = """Found gas blowing at the Aspen Ridge station 09:43. Meter shows 300 m3 released. Stayed inside fence.
J. Lee, patrol contractor, 403-555-0199"""
PACKET = {"status": "reportable", "incident_types": ["INC-e"], "deadline": "T3", "deadline_rules": ["T3-SOUR", "PREC"],
          "due_at": "2026-08-30T12:43:00", "missing": ["lands"], "route": "clear-cut", "route_triggers": [],
          "citations": ["INC-e", "PREC", "T3-SOUR", "DIR-84"]}  # fmt: skip
FIELDS = {k: None for k in drafter.NARRATIVE} | {
    "how_discovered": "Found by the patrol contractor.",
    "specific_details": "Meter shows 300 m3 released.",
    "affected_lands": "Inside the fence.",
}
GOOD = drafter.render(PACKET, FIELDS, "Aspen Ridge Pipelines Inc.")


def failed(checks):
    return {c for c, v in checks.items() if v["verdict"] == "fail"}


def test_code_checks_pass_a_correct_draft():
    assert failed(j.code_checks(PACKET, GOOD, REPORT)) == set()


def test_code_checks_catch_each_structural_fault():
    cases = {
        "consistent": GOOD.replace("Verbal and written notice within 3 hours", "Written notice within 24 hours"),
        "complete": GOOD.replace("- Where did the product go", "- Where else"),
        "cited": GOOD.replace("- DIR-84:", "- DIR-99:"),
        "precautionary": GOOD.replace("The deadline was taken at the stricter reading", "The deadline is"),
    }
    for crit, text in cases.items():
        assert crit in failed(j.code_checks(PACKET, text, REPORT)), crit
    narrative_faults = {
        "consistent": GOOD.replace("Found by the patrol contractor.", "Found. The notice is due within 24 hours."),
        "faithful": GOOD.replace("300 m3", "3000 m3"),
        "clean": GOOD.replace("Found by the patrol contractor.", "Call 403-555-0199."),
    }
    for crit, text in narrative_faults.items():
        assert crit in failed(j.code_checks(PACKET, text, REPORT)), crit


def test_quote_check_rejects_words_not_in_the_report():
    assert j.in_report("Meter shows 300 m3 released", REPORT)
    assert j.in_report("gas blowing ... inside fence", REPORT)
    assert not j.in_report("landowner call", REPORT)


class Stub:
    def __init__(self, outputs):
        self.outputs, self.calls = list(outputs), []

    def converse(self, **kw):
        self.calls.append(kw)
        out = self.outputs.pop(0)
        return {"output": {"message": {"content": [{"toolUse": {"input": out}}]}},
                "usage": {"inputTokens": 100, "outputTokens": 20}}  # fmt: skip


def answer(report_words="Meter shows 300 m3 released", same=True, faithful="pass"):
    return {"statements": [{"field": "PIR-6", "statement": "300 m3 released", "report_words": report_words,
                            "same_fact": same}],
            "faithful_reason": "x", "faithful_verdict": faithful,
            "clean_evidence": "none found", "clean_verdict": "pass"}  # fmt: skip


def test_prompt_sends_only_the_report_and_narrative_fields():
    p = j.prompt(REPORT, GOOD)
    assert "PIR-6: Meter shows 300 m3 released." in p and "<report>" in p
    assert "Deadline" not in p and "Reasons" not in p


def test_judge_retries_an_incomplete_call_and_quote_check_overrides_a_pass():
    stub = Stub([{"faithful_verdict": "pass"}, answer(report_words="landowner call")])
    r = j.judge(stub, "arn", REPORT, GOOD)
    assert r["retries"] == 1 and stub.calls[1]["inferenceConfig"]["temperature"] > 0
    assert r["statements"][0]["quote_ok"] is False
    code = j.code_checks(PACKET, GOOD, REPORT)
    assert j.combine(code, r)["criteria"]["faithful"]["verdict"] == "fail"
    ok = j.judge(Stub([answer()]), "arn", REPORT, GOOD)
    assert j.combine(code, ok)["verdict"] == "pass"


def test_score_counts_false_pass_false_fail_hits_and_flips():
    items = [{"cal_id": "A", "criteria": ["faithful"]}, {"cal_id": "B", "criteria": []}]
    labels = {"A": "fail", "B": "pass"}

    def v(fail):
        return {"verdict": "fail" if fail else "pass",
                "criteria": {c: {"verdict": "fail" if c in fail else "pass"} for c in j.CRITERIA}}  # fmt: skip

    got = {("A", 1): v(["faithful"]), ("A", 2): v([]), ("B", 1): v([]), ("B", 2): v(["clean"])}
    s = j.score(items, labels, got, 2)
    assert s["false_pass_rate"] == 0.5 and s["false_fail_rate"] == 0.5 and s["criterion_hit_rate"] == 0.5
    assert s["flipped"] == ["A", "B"] and s["stability"] == 0.0


def test_kappa():
    assert j.kappa([(True, True), (False, False)]) == 1.0
    assert j.kappa([(False, False)]) is None


def test_missing_faithful_verdict_falls_back_to_the_judges_own_marks():
    a = answer(same=False)
    del a["faithful_reason"], a["faithful_verdict"]
    r = j.judge(Stub([a]), "arn", REPORT, GOOD)
    assert r["criteria"]["faithful"]["verdict"] == "fail" and r["retries"] == 0
