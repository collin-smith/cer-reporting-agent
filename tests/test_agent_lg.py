"""The LangGraph build of the single agent (article 4), with a scripted model: the same tools and descriptions as
Strands, the stricter-only gate still in force, the graph ends at `finish`, and the turn limit stops it. No model calls
($0). Skipped without the `langgraph` extra."""

import datetime as dt

import pytest

pytest.importorskip("langgraph")

from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel  # noqa: E402
from langchain_core.messages import AIMessage, HumanMessage  # noqa: E402

from cer_agent import agent_lg  # noqa: E402
from cer_agent.agent import MAX_TURNS, Case  # noqa: E402

READING = {"release": "yes", "substance": "crude oil - sweet", "volume": 2, "volume_unit": "m3",
           "volume_basis": "estimated", "lands": ["company_property"]}  # fmt: skip
REPORT = "Line strike at the yard. About 2 m3 of crude on our lease, maybe more like 20 m3 per the operator."


class Scripted(FakeMessagesListChatModel):
    """Replies from a list, one per model call; tools are accepted and ignored (the replies already call them)."""

    def bind_tools(self, tools, **kwargs):
        return self


def call(name, args, i=0):
    return AIMessage("", tool_calls=[{"name": name, "args": args, "id": f"{name}-{i}", "type": "tool_call"}])


def run(replies):
    case = Case(REPORT, dt.date(2026, 7, 11), READING)
    llm = Scripted(responses=replies)
    state = agent_lg.graph(case, llm).invoke({"messages": [HumanMessage("review")], "turns": 0})
    return case, state


def test_same_tools_and_descriptions_as_strands():
    lg = agent_lg.tools(Case(REPORT, None, READING))
    strands = Case.tools(Case(REPORT, None, READING))
    assert [t.name for t in lg] == [t.tool_name for t in strands]
    for t in lg:
        assert t.description == getattr(Case, t.name).__doc__


def test_ends_at_finish_and_keeps_the_gate():
    case, state = run([
        call("patch_facts", {"field": "volume", "value": "20", "quote": "maybe more like 20 m3"}, 1),
        call("patch_facts", {"field": "release", "value": "no", "quote": "Line strike at the yard"}, 2),
        call("finish", {"escalate": False, "reason": "done"}, 3),
        AIMessage("never reached"),
    ])  # fmt: skip
    assert state["turns"] == 3  # no fourth model call after finish
    assert case.raw["volume"] == 20 and case.raw["release"] == "yes"  # stricter in, looser held
    assert case.held and case.finished == {"escalate": False, "reason": "done"}


def test_a_plain_reply_ends_the_case():
    case, state = run([AIMessage("Nothing to correct.")])
    assert state["turns"] == 1 and case.finished is None


def test_turn_limit_stops_the_loop():
    replies = [call("rule_text", {"rule_id": "PREC"}, i) for i in range(MAX_TURNS + 3)]
    case, state = run(replies)
    assert state["turns"] == MAX_TURNS and case.finished is None


def test_strands_stop_at_finish_keeps_the_name_and_description():
    tools = Case(REPORT, None, READING).tools(stop_at_finish=True)
    assert [t.tool_name for t in tools] == ["patch_facts", "confirm_missing", "rule_text", "finish"]
    spec = tools[-1].tool_spec
    assert spec["description"] == Case.finish.__doc__
    assert set(spec["inputSchema"]["json"]["properties"]) == {"escalate", "reason"}  # no tool_context
