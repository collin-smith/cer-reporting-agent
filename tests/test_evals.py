"""Tier-1 harness checks at $0: the labels agree with the rules, and the scorers catch the costly errors."""

from cer_agent.evals import facts_from_json, load_cases, load_config, run_case, score_case, summarize, wilson


def test_oracle_arm_matches_every_label():
    cases = load_cases(load_config(), ["dev", "test", "heldout"])
    rows = [run_case(c, "oracle") for c in cases]
    s = summarize(rows)
    assert s["cases"] == len(cases) > 0
    assert s["status"]["rate"] == s["deadline_correct"]["rate"] == s["route"]["rate"] == 1.0
    assert s["extraction_accuracy"]["rate"] == 1.0 and s["missed_reports"]["k"] == 0


def test_a_missed_report_and_a_late_deadline_are_scored():
    case = next(c for c in load_cases(load_config(), ["dev", "test", "heldout"]) if c["expected"]["deadline"] == "T3")
    wrong = {"status": "not reportable", "deadline": None, "route": "clear-cut", "incident_types": [], "missing": []}
    sc = score_case(case, wrong, facts_from_json(case["facts"]))
    assert sc["missed_report"] and sc["late_deadline"] and not sc["status"]


def test_wilson_interval():
    lo, hi = wilson(30, 30)
    assert hi == 1.0 and 0.88 < lo < 0.89
