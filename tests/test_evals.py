"""Tier-1 harness checks at $0: the labels agree with the rules, and the scorers catch the costly errors."""

import copy
import json

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


def test_ocr_cases_are_current_cached_and_never_held_out():
    """Every render in the manifest has an OCR result, and no report changed since it was rendered (D24)."""
    from cer_agent.evals import case_id, ocr_cases

    cases = ocr_cases(load_config())
    assert len(cases) == 90 and {c["render"] for c in cases} == {"form", "scan", "photo"}
    assert all(c["split"] in ("dev", "test") and c["report"].strip() for c in cases)
    assert case_id(cases[0]["id"]) == cases[0]["id"].split("@")[0] and "@" in cases[0]["id"]
    row = run_case(cases[0], "oracle")
    assert row["render"] == cases[0]["render"] and row["score"]["status"]


def test_lost_words_ignores_extra_text_and_typographic_quotes():
    import importlib.util
    import pathlib

    path = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "ocr_report.py"
    spec = importlib.util.spec_from_file_location("ocr_report", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    report = "It’s about 1.6 m³ — we didn’t see a sheen."
    assert mod.lost(report, "OPERATOR Acme\nIt's about 1.6 m³ - we\ndidn't see a sheen.\nSUPERVISOR REVIEW") == 0
    assert 0 < mod.lost(report, "It's about 1.8 m³ - we didn't see a sheen.") < 0.2


def test_normalise_folds_typography_and_keeps_structure():
    from cer_agent.extract import normalise

    raw = "Hi,\r\n\r\n\r\nIt’s  about 1.6 m³ — we didn’t see “oil”.  \n\nJesse\nField Op"
    assert normalise(raw) == "Hi,\n\nIt's about 1.6 m³ - we didn't see \"oil\".\n\nJesse\nField Op"
    assert normalise(normalise(raw)) == normalise(raw)


def test_ocr_paragraphs_match_the_typed_layout():
    from cer_agent.extract import normalise
    from cer_agent.ocr import unwrap

    typed = "Found a leak at the station this morning, about 300 m³ out, and it looks like it went\n\nCrew on it."
    ocr = "Found a leak at the station this morning, about 300 m³ out, and it\nlooks like it went\nCrew on it."
    assert normalise(unwrap(ocr)) == normalise(typed)  # the wrapped line is rejoined


def test_variants_identical_after_normalising_are_left_out():
    from cer_agent.evals import perturbed_cases

    one_para = {"id": "X-1", "report": "A single short line, no blank lines."}
    two_para = {"id": "X-2", "report": "First paragraph.\n\nSecond paragraph."}
    out, same = perturbed_cases([one_para, two_para], ["noblank", "wrap72"])
    assert [c["id"] for c in out] == ["X-1", "X-2", "X-2~noblank"] and same == 3
    assert out[2]["report"] == "First paragraph.\nSecond paragraph." and out[2]["perturb"] == "noblank"


def test_stability_counts_a_flip_against_the_same_pass_only():
    from cer_agent.evals import case_id, stability

    case = next(c for c in load_cases(load_config(), ["dev"]) if c["expected"]["status"] == "reportable")
    good = run_case(case, "oracle")
    bad = copy.deepcopy(good)
    bad["packet"] = {**bad["packet"], "status": "not reportable", "deadline": None}
    bad["score"] = score_case(case, bad["packet"], facts_from_json(case["facts"]))
    rows = [{**good, "rep": 1}, {**good, "rep": 2},
            {**good, "id": f"{case['id']}~wrap72", "perturb": "wrap72", "rep": 1},
            {**bad, "id": f"{case['id']}~wrap72", "perturb": "wrap72", "rep": 2}]  # fmt: skip
    st = stability(rows)
    assert st["overall"]["flips"]["k"] == 1 and st["overall"]["flips"]["n"] == 2
    assert st["overall"]["right_to_wrong"] == 1 and st["overall"]["missed_reports"] == 1
    assert st["flipped_cases"] == [case["id"]] and case_id(f"{case['id']}~wrap72") == case["id"]
    assert stability([{**good, "rep": 1}]) is None


def test_load_rows_keeps_the_first_row_per_case_and_pass(tmp_path):
    from cer_agent.evals import load_rows

    f = tmp_path / "results.jsonl"
    rows = [
        {"id": "A", "rep": 1, "n": 1},
        {"id": "A", "rep": 2, "n": 2},
        {"id": "A", "rep": 1, "n": 3},
        {"id": "B", "n": 4},
    ]
    f.write_text("".join(json.dumps(r) + "\n" for r in rows))
    assert [r["n"] for r in load_rows(f)] == [1, 2, 4]
    assert load_rows(tmp_path / "missing.jsonl") == []


def test_a_second_writer_on_the_same_run_is_refused(tmp_path):
    import pytest

    from cer_agent.evals import run_lock

    with run_lock(tmp_path), pytest.raises(SystemExit, match="locked by another process"), run_lock(tmp_path):
        pass
    assert not (tmp_path / ".lock").exists()
    with run_lock(tmp_path):  # free again once the first writer ends
        pass
