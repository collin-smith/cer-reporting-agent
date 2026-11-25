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


def _pairs():
    import json

    return [json.loads(ln) for ln in j.PAIRS.read_text(encoding="utf-8").splitlines()]


def test_pairs_file_is_current():
    import importlib.util

    spec = importlib.util.spec_from_file_location("make_judge_pairs", j.CODE / "scripts" / "make_judge_pairs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.build() == _pairs()


def test_pairs_only_the_judge_can_tell_them_apart():
    """Same draft both sides; the key quote is in both reports and every code check passes on both."""
    items = _pairs()
    for pair in {it["pair"] for it in items}:
        today, past = (next(it for it in items if it["pair"] == pair and it["side"] == s) for s in ("today", "past"))
        assert today["draft"] == past["draft"] and today["report"] != past["report"]
        assert sorted(today["report"].split()) == sorted(past["report"].split())  # same words, moved
        for it in (today, past):
            assert j.in_report(it["key"], it["report"])
            assert failed(j.code_checks(it["packet"], it["draft"], it["report"])) == set()


def test_key_outcome_keeps_not_found_apart_from_wrong_incident():
    item = {"key": "After power-up, one valve stayed open.", "key_field": "PIR-6"}

    def judged(words, ok, same, field="PIR-6"):
        return {"statements": [{"field": field, "statement": "x", "report_words": words, "quote_ok": ok,
                                "same_fact": same}]}  # fmt: skip

    assert j.key_outcome(item, judged("one valve stayed open", True, True)) == "accepted"
    assert j.key_outcome(item, judged("one valve stayed open", True, False)) == "quoted, judged unsupported"
    assert j.key_outcome(item, judged("one valve stayed open", False, True)) == "quote not found in report"
    assert j.key_outcome(item, judged(None, False, False)) == "judge found no support"
    assert j.key_outcome(item, judged("one valve stayed open", True, True, "PIR-8")) == "key statement not listed"


def test_saved_pair_verdicts_frozen_prompt():
    """$0: the saved Nova Lite verdicts on the pairs (frozen prompt, 3 passes, 2026-11-23). The judge told 5 of 6
    apart; on P4 it took the 2024 fire's damage as today's on every pass. A change to the quote check or the
    combine rules that moves this shows up here."""
    import json

    items = _pairs()
    rows = map(json.loads, (j.VERDICTS / "nova-lite-c1edd9b9.jsonl").read_text(encoding="utf-8").splitlines())
    by_hash = {(r["draft_hash"], r["pass"]): r for r in rows}
    got = {(it["cal_id"], p): by_hash[(j.draft_hash(it), p)] for it in items for p in (1, 2, 3)}
    assert j.told_apart(items, got, 3) == ["P1", "P2", "P3", "P5", "P6"]
    p4 = next(it for it in items if it["cal_id"] == "P4-past")
    assert [j.key_outcome(p4, got[("P4-past", p)]) for p in (1, 2, 3)] == ["accepted"] * 3


def test_attribution_variant_is_the_frozen_prompt_plus_one_field():
    """D76: same system prompt, same tool except an `incident` field recorded before same_fact; the frozen VERSION
    is untouched, and the variant runs on the pairs only."""
    import json

    assert json.loads(j.FROZEN.read_text())["version"] == j.VERSION
    base = j.TOOL["inputSchema"]["json"]["properties"]["statements"]["items"]
    attr = j.TOOL_ATTR["inputSchema"]["json"]["properties"]["statements"]["items"]
    assert list(attr["properties"]) == ["field", "statement", "report_words", "incident", "same_fact"]
    assert {k: v for k, v in attr["properties"].items() if k != "incident"} == base["properties"]
    assert attr["properties"]["incident"]["enum"] == list(j.INCIDENTS)
    rest = lambda t: {k: v for k, v in t["inputSchema"]["json"]["properties"].items() if k != "statements"}  # noqa: E731
    assert rest(j.TOOL_ATTR) == rest(j.TOOL) and j.VERSION_ATTR != j.VERSION
    assert j.main(["--set", "measure", "--attribution"]) == 2

    s = Stub([answer()])
    j.judge(s, "arn", REPORT, GOOD, attribution=True)
    call = s.calls[0]
    assert call["toolConfig"]["tools"][0]["toolSpec"] is j.TOOL_ATTR and call["system"][0]["text"] == j.SYSTEM


def test_earlier_incident_rule_fails_only_when_asked():
    code = {c: {"verdict": "pass", "reason": ""} for c in j.CRITERIA}
    st = {"field": "PIR-6", "statement": "x", "report_words": "y", "quote_ok": True, "same_fact": True,
          "incident": "an earlier incident"}  # fmt: skip
    judged = {"statements": [st], "criteria": {"faithful": {"verdict": "pass", "reason": ""},
                                               "clean": {"verdict": "pass", "reason": ""}}}  # fmt: skip
    assert j.combine(code, judged)["verdict"] == "pass"
    assert j.combine(code, judged, earlier_fails=True)["verdict"] == "fail"
    assert j.key_incident({"key_field": "PIR-6"}, judged) == "an earlier incident"


def test_saved_pair_verdicts_attribution_variant():
    """$0: the saved Nova Lite verdicts with the incident field (D76, 3 passes, 2026-11-25, $0.0093). On P4 the judge
    still accepted the 2024 fire's damage as the same fact on every pass, but labelled it an earlier incident: the
    miss is legible. "Earlier" appears only on past-side (wrong) drafts, so a code rule on it adds no false fail."""
    import json

    items = _pairs()
    rows = map(json.loads, (j.VERDICTS / f"nova-lite-{j.VERSION_ATTR}.jsonl").read_text(encoding="utf-8").splitlines())
    by_hash = {(r["draft_hash"], r["pass"]): r for r in rows}
    got = {(it["cal_id"], p): by_hash[(j.draft_hash(it), p)] for it in items for p in (1, 2, 3)}
    assert j.told_apart(items, got, 3) == ["P1", "P2", "P3", "P5", "P6"]
    p4 = next(it for it in items if it["cal_id"] == "P4-past")
    assert [j.key_outcome(p4, got[("P4-past", p)]) for p in (1, 2, 3)] == ["accepted"] * 3
    assert [j.key_incident(p4, got[("P4-past", p)]) for p in (1, 2, 3)] == ["an earlier incident"] * 3
    earlier = {cid for (cid, _), v in got.items() for s in v["statements"] if s.get("incident") == j.INCIDENTS[1]}
    assert earlier == {"P3-past", "P4-past"}
    for it in items:
        code, sent = j.code_checks(it["packet"], it["draft"], it["report"]), j.sent_fields(it["draft"])
        for p in (1, 2, 3):
            v = got[(it["cal_id"], p)]
            if it["side"] == "today":
                assert j.combine(code, v, sent, True)["verdict"] == j.combine(code, v, sent)["verdict"]
            else:
                assert j.combine(code, v, sent, True)["verdict"] == "fail"
