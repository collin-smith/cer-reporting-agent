"""The single agent's tools, without a model: rules lookup, one-fact patches checked against the report, and the
missing-fact check."""

import datetime as dt

from cer_agent import agent

REPORT = """Gas blowing at the Aspen Ridge station at 01:40. About 0.085 kg/s from a valve packing. Stayed inside
the fence. Not sure if it was sour."""
RAW = {"discovered_time": "01:40", "death": "no", "injury": "none", "env_effect": "none", "release": "yes",
       "substance": "not_stated", "volume": None, "rate": 0.085, "rate_unit": "kg/s", "rate_basis": "estimated",
       "through_pipe_body_or_weld": "no", "lands": [], "h2s_detected": "unknown"}  # fmt: skip


def tools(case):
    return {t.tool_name: t for t in case.tools()}


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
    assert "takes one number" in patch(field="rate", value="0.05 to 0.1", quote="About 0.085 kg/s")
    assert case.raw == RAW


def test_confirm_missing_only_takes_facts_the_rules_list_as_missing():
    case = agent.Case(REPORT, None, RAW)
    confirm = tools(case)["confirm_missing"]
    assert "isn't missing" in confirm(fact="death", found=False)
    assert "stays a question" in confirm(fact="lands", found=False)
    assert "patch_facts on lands" in confirm(fact="lands", found=True)
