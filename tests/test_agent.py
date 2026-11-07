"""The single agent's tools, without a model: rules lookup, one-fact patches checked against the report, and the
missing-fact check."""

import datetime as dt

import pytest

from cer_agent import agent

REPORT = """Gas blowing at the Aspen Ridge station at 01:40. About 0.085 kg/s from a valve packing. Stayed inside
the fence. Not sure if it was sour."""
RAW = {"discovered_time": "01:40", "death": "no", "injury": "none", "env_effect": "none", "release": "yes",
       "substance": "not_stated", "volume": None, "rate": 0.085, "rate_unit": "kg/s", "rate_basis": "estimated",
       "through_pipe_body_or_weld": "no", "lands": [], "h2s_detected": "unknown"}  # fmt: skip


def tools(case):
    return {t.tool_name: t for t in case.tools()}


@pytest.mark.skipif(not agent.RULES_SPEC.exists(), reason="input/cer/rules-spec.md is outside code/ (not in the repo)")
def test_rule_passage_finds_headings_and_table_rows():
    assert agent.rule_passage("PREC").startswith("### PREC")
    assert "1.5 m3" in agent.rule_passage("T3-LVP") and "Interpretation of `T3-LVP`" in agent.rule_passage("T3-LVP")
    assert agent.rule_passage("T3-NOPE") == "No rule T3-NOPE in the rules spec."


def test_patch_changes_one_fact_with_a_quote_and_keeps_the_rest():
    case = agent.Case(REPORT, dt.date(2026, 11, 6), RAW)
    assert "lands" in case.packet["missing"]
    out = tools(case)["patch_facts"](field="lands", value='["company_property"]', quote="Stayed inside the fence")
    assert out.startswith("Changed lands") and case.raw["lands"] == ["company_property"]
    assert case.raw["rate"] == 0.085 and case.raw["rate_basis"] == "estimated"  # untouched
    assert "lands" not in case.packet["missing"]


def test_patch_without_the_reports_words_or_with_a_bad_value_changes_nothing():
    case = agent.Case(REPORT, None, RAW)
    patch = tools(case)["patch_facts"]
    assert patch(field="rate_basis", value="measured", quote="metered at 0.085 kg/s").startswith("Not changed")
    assert "must be one of" in patch(field="rate_basis", value="exact", quote="About 0.085 kg/s")
    assert "No field" in patch(field="colour", value="red", quote="Gas blowing")
    assert "rate must be a number. Example: 1.5" in patch(field="rate", value="0.05 to 0.1", quote="About 0.085 kg/s")
    assert case.raw == RAW


def test_confirm_missing_only_takes_facts_the_rules_list_as_missing():
    case = agent.Case(REPORT, None, RAW)
    confirm = tools(case)["confirm_missing"]
    assert "isn't missing" in confirm(fact="death", found=False)
    assert "stays a question" in confirm(fact="lands", found=False)
    assert "patch_facts on lands" in confirm(fact="lands", found=True)


SOUR = """Gas blowing at the Aspen Ridge station at 01:40. About 0.085 kg/s from a valve packing. Stayed inside
the fence. Crew reported no H2S on the monitors. No one hurt."""


def test_a_patch_that_would_loosen_the_result_is_held_for_a_person():
    raw = {**RAW, "lands": ["company_property"], "h2s_detected": "unknown"}
    case = agent.Case(SOUR, dt.date(2026, 11, 6), raw)
    before = (case.packet["status"], case.packet["deadline"], case.packet["route"])
    out = tools(case)["patch_facts"](field="release", value="no", quote="No one hurt")  # real words, wrong meaning
    assert out.startswith("Held for the approver") and case.raw == raw
    assert (case.packet["status"], case.packet["deadline"], case.packet["route"]) == before
    assert case.held[0]["field"] == "release" and case.held[0]["would"]
    assert case.patches[-1]["accepted"] is False and case.patches[-1]["held"]


def test_loosening_compares_notify_deadline_due_and_route():
    base = {"status": "reportable", "deadline": "T3", "due_at": "2026-11-06T04:40", "route": "judgment"}
    assert agent.loosening(base, base) == []
    assert agent.loosening(base, {**base, "status": "precautionary"}) == []  # both notify
    assert agent.loosening(base, {**base, "status": "not reportable", "deadline": None, "due_at": None})
    assert agent.loosening(base, {**base, "deadline": "T24"}) == ["deadline T3 -> T24"]
    assert agent.loosening(base, {**base, "due_at": "2026-11-06T05:40"})
    assert agent.loosening(base, {**base, "route": "clear-cut"}) == ["route judgment -> clear-cut"]
    assert agent.loosening({**base, "deadline": "T24"}, base) == []  # stricter is fine


def test_values_are_checked_all_the_way_down_and_errors_show_a_correct_example():
    v, err = agent._value("lands_alternatives", '[":["]')
    assert v is None and "must be a list" in err and '[["company_property"], ["off_right_of_way"]]' in err
    v, err = agent._value("volume_alternatives", '["(estimated 1.2 to 2.0 m3)"]')
    assert v is None and "must be a number" in err and "[1.2, 2.0]" in err
    assert agent._value("lands", '["park"]')[1].startswith("lands[0] must be one of")


def test_common_harmless_forms_are_accepted():
    assert agent._value("volume_alternatives", "(1.2, 2.0)") == ([1.2, 2.0], None)
    assert agent._value("lands_alternatives", "[[&quot;company_property&quot;],[&quot;right_of_way&quot;]]") == (
        [["company_property"], ["right_of_way"]],
        None,
    )
    assert agent._value("lands", "company_property") == (["company_property"], None)
    assert agent._value("volume", "null") == (None, None)


def test_a_patch_to_the_value_already_recorded_changes_nothing_and_says_so():
    case = agent.Case(REPORT, None, {**RAW, "lands": ["company_property"]})
    out = tools(case)["patch_facts"](field="lands", value='["company_property"]', quote="inside the fence")
    assert out.startswith('lands is already ["company_property"]; nothing to change')  # before the quote check
    assert case.patches[-1]["noop"] and not case.patches[-1]["accepted"]


def test_rule_text_answers_instead_of_crashing_when_the_spec_is_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(agent, "RULES_SPEC", tmp_path / "missing.md")
    assert agent.rule_passage("PREC") == "The rules spec isn't available here, so there's no text for PREC."
