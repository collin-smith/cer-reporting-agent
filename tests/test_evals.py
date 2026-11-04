"""Tier-1 harness checks at $0: the labels agree with the rules, and the scorers catch the costly errors."""

import copy

from cer_agent.evals import (
    check_targets_by_pass,
    facts_from_json,
    load_cases,
    load_config,
    render_md,
    run_case,
    score_case,
    spread,
    summarize,
    wilson,
)


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


def _three_passes_one_flip():
    """Three oracle passes over dev; in pass 2 one T3 case is answered "not reportable" (a flip)."""
    cases = load_cases(load_config(), ["dev"])
    base = [run_case(c, "oracle") for c in cases]
    rows = [{**copy.deepcopy(r), "rep": rep} for rep in (1, 2, 3) for r in base]
    case = next(c for c in cases if c["expected"]["deadline"] == "T3")
    flip = next(r for r in rows if r["id"] == case["id"] and r["rep"] == 2)
    wrong = {"status": "not reportable", "deadline": None, "route": "clear-cut", "incident_types": [], "missing": []}
    flip["packet"] = wrong
    flip["score"] = score_case(case, wrong, facts_from_json(case["facts"]))
    return cases, rows, case["id"]


def test_spread_reports_each_pass_and_the_flipped_case():
    cases, rows, flipped = _three_passes_one_flip()
    sp = spread(rows)
    assert sp["passes"] == 3
    st = sp["metrics"]["status"]
    assert st["per_pass"][0] == st["per_pass"][2] == st["max"] == 1.0
    assert st["min"] == st["per_pass"][1] == (len(cases) - 1) / len(cases)
    assert sp["metrics"]["missed_reports"]["per_pass"] == [0, 1, 0]
    assert [u["id"] for u in sp["unstable"]] == [flipped] and sp["unstable"][0]["right"] == 2


def test_a_target_missed_in_one_pass_is_not_met():
    _, rows, _ = _three_passes_one_flip()
    t = {x["target"]: x for x in check_targets_by_pass(rows, load_config()["targets"])}
    assert not t["missed_reports"]["met"] and t["missed_reports"]["passes_met"] == 2
    assert t["missing_recall"]["met"] and t["missing_recall"]["passes_met"] == 3


def test_a_single_pass_has_no_spread_and_renders_as_before():
    rows = [run_case(c, "oracle") for c in load_cases(load_config(), ["dev"])]
    assert spread(rows) is None
    md = render_md(
        "x",
        {"arm": "oracle", "splits": ["dev"]},
        summarize(rows),
        {},
        check_targets_by_pass(rows, load_config()["targets"]),
        rows,
    )
    assert "Spread" not in md and "Passes met" not in md


def test_the_report_shows_the_spread_and_the_unstable_case():
    _, rows, flipped = _three_passes_one_flip()
    sp = spread(rows)
    md = render_md(
        "x",
        {"arm": "oracle", "splits": ["dev"]},
        summarize(rows),
        {},
        check_targets_by_pass(rows, load_config()["targets"]),
        rows,
        sp,
    )
    assert "## Spread across passes" in md and f"| {flipped} |" in md and "× 3 passes" in md


def test_demo_samples_match_the_answer_key_and_skip_held_out():
    import importlib.util
    import json
    import pathlib

    path = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "make_samples.py"
    spec = importlib.util.spec_from_file_location("make_samples", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    built = mod.build()
    assert 15 <= len(built) <= 25 and all(s["split"] != "heldout" for s in built)
    assert json.loads(mod.OUT.read_text(encoding="utf-8")) == built  # regenerate with scripts/make_samples.py
