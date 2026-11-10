"""The CER reporting tools as an MCP server (article 5): the same code as the workflow and the agent, behind a
standard protocol, so any MCP client (Claude Code, Claude Desktop, our Strands agent) can use it.

Two scopes:
- public (default), for an outside client such as Claude Code:
  triage_report  the strict check (D33): reads the report in each layout (Nova Lite), the rules engine decides
  decide         the rules engine on facts you give it; no model call, $0
  rule_text      the rules spec's text for one rule ID; $0
  draft_notice   a draft Preliminary Incident Report for a person to approve (Nova Lite; the system never files)
- review (--review), for the reviewing agent: also read_report, open_case, patch_facts, confirm_missing, finish and
  case_result. One case at a time per server process; open_case starts a fresh one.

The server never sets a decision a model chose: every packet is the rules engine's, and patch_facts keeps the
stricter-only gate (D38). Model calls use the tagged Nova Lite profile in NOVA_LITE_ARN and the caller's AWS
credentials. Hosted only for article 7's AgentCore window (`--http`, D55), behind AgentCore Gateway.

Usage (from code/, src on PYTHONPATH):
    NOVA_LITE_ARN=... python3 -m cer_agent.mcp_server [--review]      # stdio; a client starts it
    NOVA_LITE_ARN=... python3 -m cer_agent.mcp_server --http          # hosted: AgentCore Runtime (article 7, D55)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from typing import Any

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

from cer_agent.agent import FIELDS, Case, check, example
from cer_agent.extract import extract, to_facts
from cer_agent.workflow import make_client, packet, run_strict

# USD per 1M tokens (input, output), Nova Lite, ca-central-1 (config.toml [models.nova-lite]).
PRICE_IN, PRICE_OUT = 0.064, 0.256  # Price List 2026-11-10 (D53)
INSTRUCTIONS = """Tools for triaging pipeline field reports against the Canada Energy Regulator's incident-reporting
rules. A rules engine makes every decision; the model only reads the report. Nothing is filed: a person approves
and submits. Start with triage_report on the report's text; use decide to test facts, rule_text to look up a cited
rule, and draft_notice for a draft notice to approve."""

READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=False)
CALLS_MODEL = ToolAnnotations(readOnlyHint=True, openWorldHint=True)  # no side effects, but a paid model call
CASE_STATE = ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=False)


class _State:
    client = None
    case: Case | None = None
    workflow_status: str | None = None


def _bedrock():
    if not (arn := os.environ.get("NOVA_LITE_ARN")):
        raise ToolError("The server needs NOVA_LITE_ARN (the tagged Nova Lite profile; terraform output "
                         "nova_lite_profile_arn) to read a report.")  # fmt: skip
    _State.client = _State.client or make_client()
    return _State.client, arn


def _date(received: str | None) -> dt.date | None:
    if not received:
        return None
    try:
        return dt.date.fromisoformat(received)
    except ValueError:
        raise ToolError(f"received must be a date as YYYY-MM-DD, e.g. 2026-07-11; got {received!r}.") from None


def _json(obj) -> dict:
    """A packet as plain JSON (dates as ISO text), so every client gets the same thing."""
    return json.loads(json.dumps(obj, default=str))


def _cost(tin: int, tout: int) -> float:
    return round((tin * PRICE_IN + tout * PRICE_OUT) / 1e6, 8)


def _reading(facts: dict) -> dict:
    """Facts in the record_facts schema, checked field by field; an error names the field and shows a valid value."""
    unknown = sorted(set(facts) - set(FIELDS))
    if unknown:
        raise ToolError(f"Unknown fact(s) {', '.join(unknown)}. Facts: {', '.join(FIELDS)}.")
    for k, v in facts.items():
        if err := check(FIELDS[k], v, k):
            raise ToolError(f"{err}. Example: {json.dumps({k: example(FIELDS[k])})}.")
    return facts


def triage_report(report: str, received: str | None = None) -> dict[str, Any]:
    """Decide whether a pipeline field report must be reported to the regulator, by when, and whether a person must
    judge it. report: the field report's text as sent (email, text message or call notes). received: the date it
    arrived, YYYY-MM-DD, for reports that give a time but no date. Reads the report three ways (as written, without
    blank lines, hard-wrapped) and keeps the strictest answer; the rules engine decides. Returns the decision packet:
    status, deadline, due_at, route, incident_types, missing facts, cited rule IDs and the facts read. About
    $0.0006 per report (three Nova Lite calls)."""
    client, arn = _bedrock()
    x = run_strict(client, arn, report, _date(received))
    return {"packet": _json(x["packet"]), "latency_s": round(x["latency_s"], 3), "model_calls": x["calls"],
            "input_tokens": x["input_tokens"], "output_tokens": x["output_tokens"],
            "cost_usd": _cost(x["input_tokens"], x["output_tokens"])}  # fmt: skip


def decide(facts: dict[str, Any], received: str | None = None) -> dict[str, Any]:
    """Run the rules engine on facts you supply, with no model call ($0): to check a decision, or to see what
    changes if one fact were different. facts: fields of the reading (the "extracted" object in a triage_report
    packet), e.g. {"release": "yes", "substance": "crude oil - sweet", "volume": 2, "volume_unit": "m3"}; a field left
    out counts as not stated. received: YYYY-MM-DD, as for triage_report. Returns the decision packet."""
    raw = _reading(facts)
    return _json(packet(to_facts(raw, _date(received)), {"raw": raw}))


def rule_text(rule_id: str) -> str:
    """The rules spec's text for one rule ID (e.g. T3-LVP, INC-d, PREC, U2-NEAR)."""
    return Case.rule_text(rule_id)


def draft_notice(report: str, packet: dict[str, Any], operator: str | None = None) -> dict[str, Any]:
    """Draft the notice a person approves and submits: a Preliminary Incident Report for a reportable or
    precautionary case, or a file note for one that isn't reportable. report: the same text given to
    triage_report; packet: the packet it returned (unchanged); operator: the company name for the notice.
    The decision parts are written from the packet by code; Nova Lite writes only the narrative fields. Returns
    the draft text and flags for the reviewer (numbers not in the report, rule talk, personal data)."""
    from cer_agent import drafter

    needed = {"status", "deadline", "due_at", "route", "incident_types", "missing", "citations"}
    if lacking := sorted(needed - set(packet)):
        raise ToolError(f"packet is missing {', '.join(lacking)}: pass the packet triage_report returned.")
    if packet["status"] == "not reportable":
        d = drafter.draft(None, "", report, packet, operator)
    else:
        client, arn = _bedrock()
        d = drafter.draft(client, arn, report, packet, operator)
    return {"text": d["text"], "flags": d["flags"], "cost_usd": _cost(d["input_tokens"], d["output_tokens"])}


# --- review scope: the reviewing agent's case session ---
def read_report(report: str, received: str | None = None) -> dict[str, Any]:
    """The workflow's single reading of a report (one Nova Lite call): the facts in the record_facts schema, to
    pass to open_case."""
    client, arn = _bedrock()
    t0 = time.perf_counter()
    x = extract(client, arn, report, _date(received))
    return {"reading": x["raw"], "input_tokens": x["input_tokens"], "output_tokens": x["output_tokens"],
            "retries": x.get("retries", 0), "latency_s": round(time.perf_counter() - t0, 3)}  # fmt: skip


def open_case(report: str, reading: dict[str, Any], received: str | None = None) -> dict[str, Any]:
    """Start reviewing one report from a reading (read_report's), replacing any open case. Returns the report as
    the tools see it, the recorded facts and the rules engine's result."""
    _State.case = Case(report, _date(received), reading)
    _State.workflow_status = _State.case.packet["status"]
    return {"report": _State.case.report, "facts": _State.case.facts_shown(),
            "rules_result": json.loads(_State.case.summary())}  # fmt: skip


def _case() -> Case:
    if _State.case is None:
        raise ToolError("No case is open: call open_case first.")
    return _State.case


def patch_facts(field: str, value: str, quote: str) -> str:
    return _case().patch_facts(field, value, quote)


def confirm_missing(fact: str, found: bool) -> str:
    return _case().confirm_missing(fact, found)


def finish(escalate: bool, reason: str) -> str:
    return _case().finish(escalate, reason)


def case_result(trace: dict[str, Any] | None = None) -> dict[str, Any]:
    """The open case's packet from the reviewed facts, with the review's trace (patches, confirmations, held
    suggestions), and the reviewed reading. trace: the client's notes on the run, kept with it."""
    c = _case()
    return {"packet": _json(c.result(_State.workflow_status, trace or {})), "reading": c.raw}


for _f in (patch_facts, confirm_missing, finish):  # the agent sees the in-process tools' words
    _f.__doc__ = getattr(Case, _f.__name__).__doc__

PUBLIC = [(triage_report, CALLS_MODEL), (decide, READ_ONLY), (rule_text, READ_ONLY), (draft_notice, CALLS_MODEL)]
REVIEW = [(read_report, CALLS_MODEL), (open_case, CASE_STATE), (patch_facts, CASE_STATE),
          (confirm_missing, CASE_STATE), (finish, CASE_STATE), (case_result, READ_ONLY)]  # fmt: skip
AGENT_TOOLS = ("patch_facts", "confirm_missing", "rule_text", "finish")  # what the reviewing agent's model sees


def build(review: bool = False) -> MCPServer:
    """The server. A deliberate error is a ToolError, whose message reaches the client: the SDK keeps any other
    exception's text on the server and sends only "Error executing tool ...", which a model can't act on."""
    server = MCPServer("cer-reporting", instructions=INSTRUCTIONS)
    for fn, ann in PUBLIC + (REVIEW if review else []):
        # A text tool stays plain text (no {"result": ...} wrapper), so the agent reads what it reads in-process.
        server.tool(annotations=ann, structured_output=fn.__annotations__["return"] != "str")(fn)
    return server


def serve_http(server: MCPServer, port: int = 8000) -> None:
    """Hosted on AgentCore Runtime (article 7, D55): the Runtime's MCP contract is stateless streamable HTTP on
    0.0.0.0:8000/mcp, with GET /ping for health. The Runtime proxies every request, so the Host header is its own;
    DNS-rebinding protection is for a server on a person's machine, not one behind a SigV4-checked endpoint."""
    from mcp.server.transport_security import TransportSecuritySettings
    from starlette.responses import JSONResponse

    @server.custom_route("/ping", methods=["GET"])
    async def ping(_request):
        return JSONResponse({"status": "Healthy", "time_of_last_update": int(time.time())})

    server.run("streamable-http", host="0.0.0.0", port=port, stateless_http=True,
               transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False))  # fmt: skip


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Serve the CER reporting tools over MCP (stdio, or HTTP when hosted).")
    ap.add_argument("--review", action="store_true", help="also serve the reviewing agent's case tools")
    ap.add_argument("--http", action="store_true", help="stateless streamable HTTP on :8000 (AgentCore Runtime)")
    args = ap.parse_args(argv)
    if args.http and args.review:  # the case tools keep one case in process memory: not for a stateless server
        ap.error("--review needs one process per client (stdio); a hosted server is stateless, public scope only")
    if args.http:
        serve_http(build())
    else:
        build(args.review).run("stdio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
