"""The supervisor's structure without a model: who gets which tools, and the limits that stop a runaway case."""

import datetime as dt

from cer_agent import agent, supervisor

REPORT = "Gas blowing at the Aspen Ridge station at 01:40. About 0.085 kg/s from a valve packing. Not sure if sour."
RAW = {"discovered_time": "01:40", "death": "no", "injury": "none", "env_effect": "none", "release": "yes",
       "substance": "not_stated", "volume": None, "rate": 0.085, "rate_unit": "kg/s", "rate_basis": "estimated",
       "through_pipe_body_or_weld": "no", "lands": [], "h2s_detected": "unknown"}  # fmt: skip


def team():
    return supervisor.Team(agent.Case(REPORT, dt.date(2026, 11, 6), RAW), model_factory=None)


def test_the_supervisor_gets_specialists_and_finish_but_no_fact_tools():
    names = {t.tool_name for t in team().supervisor_tools()}
    assert names == {"ask_completeness", "ask_policy", "finish"}  # it can't patch facts itself


def test_a_specialist_is_asked_at_most_twice_per_case():
    t = team()
    t.calls = [{"specialist": "completeness"}] * supervisor.CALLS_PER_SPECIALIST
    out = t._specialist("completeness", supervisor.COMPLETENESS, [], "check again")
    assert "already been asked" in out and len(t.calls) == supervisor.CALLS_PER_SPECIALIST


def test_no_specialist_call_once_the_token_budget_is_used():
    t = team()
    t.usage["inputTokens"] = supervisor.TOKEN_BUDGET
    assert "budget" in t._specialist("policy", supervisor.POLICY, [], "which fact?") and not t.calls


def test_the_supervisor_arm_is_wired_into_the_harness():
    from cer_agent.evals import ARMS

    assert ARMS["supervisor-nova"] == "nova-lite"


def test_the_handoff_drops_thinking_text_and_keeps_the_answer():
    assert supervisor.handoff("<thinking>long notes</thinking> Changed lands.") == "Changed lands."
    assert supervisor.handoff("<thinking>never closed") == "(no answer)"
    assert len(supervisor.handoff("x" * 900)) == 600
