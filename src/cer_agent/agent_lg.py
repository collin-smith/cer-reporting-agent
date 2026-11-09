"""The single agent built a second time, in LangGraph (article 4, D1): the same prompt, the same four tools and the
same Nova Lite model as cer_agent.agent (Strands), so only the framework differs.

What is shared: the workflow's first reading (extract.extract), the Case class (its tools' logic, their descriptions
and the stricter-only gate), the system prompt, the turn limit, and the packet the case ends with. What LangGraph
changes is the loop: in Strands the loop is inside Agent(); here it is a graph we write.

    START -> model -> (tool calls?) -> tools -> (finished? turn limit?) -> model ... -> END

Two choices the graph makes explicit that Strands keeps inside its loop:
- After `finish`, the graph ends. Strands sends the tool's "Done. Stop now." back to the model for one more turn.
- The turn limit is an edge condition on a counter in the graph's state, not an argument to the call.

The case's facts stay in the Case object, as in Strands, so both builds run the same gate code. LangGraph could carry
them in the graph's state instead, with a checkpointer to pause and resume a case; that isn't needed here
(D1: Step Functions owns the outer flow and the approval wait).

Tracing: Strands emits OpenTelemetry spans for the agent, each model call and each tool call on its own. LangGraph's
built-in tracing goes to LangSmith (a hosted service). To keep traces local and in OpenTelemetry, this module opens
the same spans itself (cer_agent.tracing, under Strands' span names), so one trace summary reads both builds.

Usage (from code/, src on PYTHONPATH; needs the `langgraph` extra):
    NOVA_LITE_ARN=... python3 -m cer_agent.agent_lg path/to/report.txt [--received YYYY-MM-DD]
"""

import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import time
from typing import Annotated, TypedDict

from cer_agent import tracing
from cer_agent.agent import MAX_TURNS, SYSTEM, Case, _session
from cer_agent.extract import RETRY_TEMPERATURES, extract, to_facts
from cer_agent.workflow import make_client

BASE_MODEL = "amazon.nova-lite-v1:0"  # what the tagged inference profile points at; LangChain needs it for an ARN


def tools(case: Case) -> list:
    """The four tools as LangChain tools, in the in-process order, with the descriptions Strands shows."""
    from langchain_core.tools import StructuredTool

    def patch_facts(field: str, value: str, quote: str) -> str:
        with tracing.span("execute_tool patch_facts"):
            return case.patch_facts(field, value, quote)

    def confirm_missing(fact: str, found: bool) -> str:
        with tracing.span("execute_tool confirm_missing"):
            return case.confirm_missing(fact, found)

    def rule_text(rule_id: str) -> str:
        with tracing.span("execute_tool rule_text"):
            return case.rule_text(rule_id)

    def finish(escalate: bool, reason: str) -> str:
        with tracing.span("execute_tool finish"):
            return case.finish(escalate, reason)

    return [StructuredTool.from_function(f, description=getattr(Case, f.__name__).__doc__)
            for f in (patch_facts, confirm_missing, rule_text, finish)]  # fmt: skip


def graph(case: Case, llm):
    """The review loop as a graph: a model node, a tool node, and the two edges that decide what runs next."""
    from langchain_core.messages import SystemMessage
    from langgraph.graph import END, START, StateGraph
    from langgraph.graph.message import add_messages
    from langgraph.prebuilt import ToolNode

    class State(TypedDict):
        messages: Annotated[list, add_messages]
        turns: int

    case_tools = tools(case)
    bound = llm.bind_tools(case_tools)

    def model(state: State) -> dict:
        with tracing.span("chat") as s:
            reply = bound.invoke([SystemMessage(SYSTEM), *state["messages"]])
            if u := reply.usage_metadata:
                tracing.usage(s, u["input_tokens"], u["output_tokens"])
        return {"messages": [reply], "turns": state["turns"] + 1}

    def after_model(state: State) -> str:
        return "tools" if state["messages"][-1].tool_calls else END

    def after_tools(state: State) -> str:
        if case.finished or state["turns"] >= MAX_TURNS:
            return END
        return "model"

    g = StateGraph(State)
    g.add_node("model", model)
    g.add_node("tools", ToolNode(case_tools))
    g.add_edge(START, "model")
    g.add_conditional_edges("model", after_model, ["tools", END])
    g.add_conditional_edges("tools", after_tools, ["model", END])
    return g.compile()


def _usage(messages: list) -> tuple[int, int]:
    used = [m.usage_metadata for m in messages if getattr(m, "usage_metadata", None)]
    return sum(u["input_tokens"] for u in used), sum(u["output_tokens"] for u in used)


def run(model_id: str, report: str, received: dt.date | None = None, region: str = "ca-central-1",
        client=None) -> dict:  # fmt: skip
    """As cer_agent.agent.run, with the review loop in LangGraph: the workflow's reading first, then the review. A
    model error ends that attempt and the next runs warmer; if every attempt fails, the workflow's packet stands."""
    from langchain_aws import ChatBedrockConverse
    from langchain_core.messages import HumanMessage

    t0 = time.perf_counter()
    x = extract(client or make_client(region), model_id, report, received)
    tin, tout, last = x["input_tokens"], x["output_tokens"], None
    bedrock = _session(region).client("bedrock-runtime")
    for temp in (0, *RETRY_TEMPERATURES):
        case = Case(report, received, x["raw"])
        prompt = (
            f"<report>\n{case.report}\n</report>\n\n<recorded_facts>\n{json.dumps(case.facts_shown())}\n"
            f"</recorded_facts>\n\n<rules_result>\n{case.summary()}\n</rules_result>"
        )
        llm = ChatBedrockConverse(model=model_id, base_model_id=BASE_MODEL, provider="amazon", client=bedrock,
                                  temperature=temp, max_tokens=1000)  # fmt: skip
        state = {"messages": [HumanMessage(prompt)], "turns": 0}
        try:
            with tracing.span("invoke_agent review"):
                for step in graph(case, llm).stream(state, stream_mode="values"):
                    state = step  # the last state, so usage so far still counts if a later step fails
        except Exception as e:  # noqa: BLE001 - a model error ends this attempt
            last = e
            i, o = _usage(state["messages"])
            tin, tout = tin + i, tout + o
            continue
        i, o = _usage(state["messages"])
        tin, tout = tin + i, tout + o
        stop = "finish" if case.finished else "limit_turns" if state["turns"] >= MAX_TURNS else "end_turn"
        trace = {"stop_reason": stop, "turns": state["turns"], "framework": "langgraph"}
        break
    else:  # every review attempt failed: the workflow's own packet stands
        case, trace = Case(report, received, x["raw"]), {"error": f"{type(last).__name__}: {last}"[:200]}
    pk = case.result(Case(report, received, x["raw"]).packet["status"], trace)
    return {"packet": pk, "facts": to_facts(case.raw, received), "input_tokens": tin, "output_tokens": tout,
            "latency_s": time.perf_counter() - t0, "retries": x.get("retries", 0)}  # fmt: skip


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run the single agent, built in LangGraph, on one field report.")
    ap.add_argument("report", type=pathlib.Path)
    ap.add_argument("--received", type=dt.date.fromisoformat)
    args = ap.parse_args(argv)
    arn = os.environ.get("NOVA_LITE_ARN")
    if not arn:
        print("Set NOVA_LITE_ARN (terraform output nova_lite_profile_arn).")
        return 2
    r = run(arn, args.report.read_text(encoding="utf-8"), args.received)
    print(json.dumps(r["packet"], indent=2, default=str))
    print(f"tokens in/out {r['input_tokens']}/{r['output_tokens']}, {r['latency_s']:.1f} s", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
