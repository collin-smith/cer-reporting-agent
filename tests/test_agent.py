"""The single agent's tools, without a model: rules lookup, record_facts running the rules, the missing-fact check."""

import datetime as dt
import json

from cer_agent import agent

REPORT = """Found crude in the ditch past the station fence at 01:40. Maybe 1.8 m3. Not sure if it reached the creek."""
RAW = {"discovered_time": "01:40", "death": "no", "injury": "none", "env_effect": "unknown", "release": "yes",
       "substance": "crude oil - sweet", "volume": 1.8, "volume_unit": "m3", "volume_basis": "estimated",
       "volume_state": "liquid", "rate": None, "lands": ["off_right_of_way"], "h2s_detected": "no"}  # fmt: skip


def tools(case):
    return {getattr(t, "tool_name", None) or t.__name__: t for t in case.tools()}


def test_rule_passage_finds_headings_and_table_rows():
    assert agent.rule_passage("PREC").startswith("### PREC")
    assert "1.5 m3" in agent.rule_passage("T3-LVP") and "Interpretation of `T3-LVP`" in agent.rule_passage("T3-LVP")
    assert agent.rule_passage("T3-NOPE") == "No rule T3-NOPE in the rules spec."


def test_record_facts_runs_the_rules_and_shows_missing_facts_and_open_points():
    case = agent.Case(REPORT, dt.date(2026, 11, 6))
    rec = tools(case)["record_facts"]
    out = rec._tool_func({"toolUseId": "t1", "input": RAW})
    summary = json.loads(out["content"][0]["text"])
    assert summary["status"] == "precautionary" and summary["deadline"] == "T3"
    assert "env_effect" in summary["missing_facts"] and summary["open_points"]
    assert case.packet["route"] == "judgment" and case.records == 1


def test_confirm_missing_checks_the_quote_against_the_report():
    case = agent.Case(REPORT, None)
    confirm = tools(case)["confirm_missing"]
    assert "Call record_facts again" in confirm(fact="lands", found=True, quote="past the station fence")
    assert "isn't in the report" in confirm(fact="lands", found=True, quote="inside the fence")
    assert "stays a question" in confirm(fact="env_effect", found=False)
    assert [c["quote_in_report"] for c in case.confirmations] == [True, False, False]
