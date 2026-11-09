"""Our own code as an MCP client (article 5): the strict check and the reviewing agent, run through the MCP server
(cer_agent.mcp_server) instead of in-process, so the evals can show the same answers come back through the protocol
and measure what it adds.

- `triage`: the strict check through the server's triage_report tool.
- `run_agent`: the reviewing agent. The reading, the case's state, every tool call and the final packet go through
  the server; only the agent's own model (Strands, Nova Lite) runs here. The agent's model sees the same four tools,
  with the same descriptions, as the in-process agent (cer_agent.agent).

Both return the same shape as their in-process versions, plus `mcp_overhead_s`: the client's wall time for the tool
calls less the time the server spent working on them.
"""

from __future__ import annotations

import datetime as dt
import functools
import json
import os
import pathlib
import sys
import time

from cer_agent.extract import RETRY_TEMPERATURES, to_facts

SRC = pathlib.Path(__file__).resolve().parents[1]


class MCPToolError(RuntimeError):
    pass


def connect(review: bool = True):
    """Start the server as a child process (stdio) and connect to it. The caller closes it (client.stop or `with`).
    Returns the client and the seconds the server took to start."""
    from mcp import StdioServerParameters
    from mcp.client.stdio import stdio_client
    from strands.tools.mcp import MCPClient

    env = {**os.environ, "PYTHONPATH": os.pathsep.join(filter(None, [str(SRC), os.environ.get("PYTHONPATH")]))}
    args = ["-m", "cer_agent.mcp_server", *(["--review"] if review else [])]
    client = MCPClient(lambda: stdio_client(StdioServerParameters(command=sys.executable, args=args, env=env)))
    t0 = time.perf_counter()
    client.start()
    return client, time.perf_counter() - t0


@functools.cache
def shared(review: bool = True):
    """One server for a whole eval run (cases run one at a time). Its start-up time is kept on the client."""
    client, startup = connect(review)
    client.startup_s = startup
    return client


def call(client, name: str, args: dict, timer: list | None = None):
    """Call one tool; returns its structured result (or text), raises MCPToolError with the server's message.
    `timer` collects each call's wall seconds."""
    t0 = time.perf_counter()
    r = client.call_tool_sync(f"{name}-{time.perf_counter_ns()}", name, args)
    if timer is not None:
        timer.append(time.perf_counter() - t0)
    if r.get("isError") or r["status"] == "error":
        raise MCPToolError(" ".join(c.get("text", "") for c in r["content"]))
    return r.get("structuredContent") or r["content"][0]["text"]


def _date(received: dt.date | None) -> str | None:
    return received.isoformat() if received else None


def triage(client, report: str, received: dt.date | None = None) -> dict:
    """`workflow.run_strict` through the server."""
    timer: list[float] = []
    r = call(client, "triage_report", {"report": report, "received": _date(received)}, timer)
    pk = r["packet"]
    return {"packet": pk, "facts": to_facts(pk["extracted"], received), "latency_s": timer[0],
            "server_s": r["latency_s"], "mcp_overhead_s": timer[0] - r["latency_s"], "calls": r["model_calls"],
            "input_tokens": r["input_tokens"], "output_tokens": r["output_tokens"], "retries": 0}  # fmt: skip


def run_agent(client, model_id: str, report: str, received: dt.date | None = None,
              region: str = "ca-central-1", in_process_order: bool = False) -> dict:  # fmt: skip
    """`agent.run` through the server: read_report, then open_case and the agent's review over the server's
    patch_facts / confirm_missing / rule_text / finish, then case_result. Retries warmer on a malformed model reply,
    from the same reading, as agent.run does."""
    from strands import Agent
    from strands.models import BedrockModel

    from cer_agent.agent import MAX_TURNS, SYSTEM, _session
    from cer_agent.mcp_server import AGENT_TOOLS

    t0, timer, rec = time.perf_counter(), [], _date(received)
    x = call(client, "read_report", {"report": report, "received": rec}, timer)
    server_s = x["latency_s"]
    tin, tout, last = x["input_tokens"], x["output_tokens"], None
    tools = [t for t in client.list_tools_sync() if t.tool_name in AGENT_TOOLS]  # the server's order
    if in_process_order:  # the order cer_agent.agent gives them (patch_facts first), to test what order changes
        tools.sort(key=lambda t: AGENT_TOOLS.index(t.tool_name))
    tool_calls_before = len(timer)
    for temp in (0, *RETRY_TEMPERATURES):
        case = call(client, "open_case", {"report": report, "reading": x["reading"], "received": rec}, timer)
        prompt = (
            f"<report>\n{case['report']}\n</report>\n\n<recorded_facts>\n{json.dumps(case['facts'])}\n"
            f"</recorded_facts>\n\n<rules_result>\n{json.dumps(case['rules_result'])}\n</rules_result>"
        )
        model = BedrockModel(model_id=model_id, boto_session=_session(region), temperature=temp, max_tokens=1000,
                             streaming=False)  # fmt: skip
        agent = Agent(model=model, tools=tools, system_prompt=SYSTEM, callback_handler=None)
        try:
            result = agent(prompt, limits={"turns": MAX_TURNS})
        except Exception as e:  # noqa: BLE001 - a model error ends this attempt; usage so far still counts
            last = e
            usage = agent.event_loop_metrics.accumulated_usage
            tin, tout = tin + usage.get("inputTokens", 0), tout + usage.get("outputTokens", 0)
            continue
        usage = result.metrics.accumulated_usage
        tin, tout = tin + usage.get("inputTokens", 0), tout + usage.get("outputTokens", 0)
        tool_s = [m.total_time for name, m in result.metrics.tool_metrics.items() if name in AGENT_TOOLS]
        trace = {"stop_reason": str(result.stop_reason), "turns": result.metrics.cycle_count,
                 "transport": "mcp", "agent_tool_s": sum(tool_s)}  # fmt: skip
        break
    else:  # every review attempt failed: the workflow's own packet stands
        call(client, "open_case", {"report": report, "reading": x["reading"], "received": rec}, timer)
        trace = {"error": f"{type(last).__name__}: {last}"[:200], "transport": "mcp"}
    done = call(client, "case_result", {"trace": trace}, timer)
    # open_case, case_result and the agent's tool calls are pure code on the server (milliseconds of work), so their
    # round trips count as overhead in full; read_report's counts less the server's own time.
    setup_s = sum(timer[tool_calls_before:])
    return {"packet": done["packet"], "facts": to_facts(done["reading"], received), "input_tokens": tin,
            "output_tokens": tout, "latency_s": time.perf_counter() - t0, "retries": x["retries"],
            "mcp_overhead_s": timer[0] - server_s + setup_s + trace.get("agent_tool_s", 0.0)}  # fmt: skip
