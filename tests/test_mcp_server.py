"""The MCP server (article 5): its tool scopes, the agent's tool words, errors a client can read, the case session
and its stricter-only gate, and one round trip over stdio. No model calls ($0)."""

import asyncio
import datetime as dt
import json

import pytest
from mcp.server.mcpserver.exceptions import ToolError

from cer_agent import mcp_client, mcp_server
from cer_agent.agent import Case
from cer_agent.extract import to_facts
from cer_agent.workflow import packet

READING = {"release": "yes", "substance": "crude oil - sweet", "volume": 2, "volume_unit": "m3",
           "volume_basis": "estimated", "lands": ["company_property"]}  # fmt: skip


def call(server, name, args):
    async def go():
        return await server.call_tool(name, args)

    r = asyncio.run(go())
    return r.structured_content if r.structured_content is not None else r.content[0].text


def names(server):
    return [t.name for t in asyncio.run(server.list_tools())]


def test_public_scope_hides_the_review_tools():
    assert names(mcp_server.build()) == ["triage_report", "decide", "rule_text", "draft_notice"]
    review = names(mcp_server.build(review=True))
    assert set(mcp_server.AGENT_TOOLS) <= set(review) and "open_case" in review


def test_agent_tool_order_is_pinned_per_path():
    """D48: the order the agent's model sees changed its redundant calls (D47: 0.88 no-op patches a case in-process,
    0.16 through MCP), with the same answers, so the CI gate wouldn't notice. Each path keeps the order it was
    measured with; change one only with a re-measure."""
    served = [n for n in names(mcp_server.build(review=True)) if n in mcp_server.AGENT_TOOLS]
    assert served == ["rule_text", "patch_facts", "confirm_missing", "finish"]  # MCP: the server's order
    in_process = [t.tool_name for t in Case.tools(Case.__new__(Case))]
    assert in_process == ["patch_facts", "confirm_missing", "rule_text", "finish"]  # articles 2-3
    assert list(mcp_server.AGENT_TOOLS) == in_process  # what the -inorder arm sorts by


def test_agent_tools_have_the_in_process_descriptions():
    tools = {t.name: t for t in asyncio.run(mcp_server.build(review=True).list_tools())}
    for name in mcp_server.AGENT_TOOLS:
        assert tools[name].description == getattr(Case, name).__doc__
        assert tools[name].output_schema is None  # plain text, as in-process


def test_decide_is_the_rules_engine():
    got = call(mcp_server.build(), "decide", {"facts": READING, "received": "2026-07-11"})
    want = json.loads(json.dumps(packet(to_facts(READING, dt.date(2026, 7, 11)), {"raw": READING}), default=str))
    assert got == want


def test_errors_reach_the_client_with_a_valid_example():
    server = mcp_server.build(review=True)
    with pytest.raises(ToolError, match=r"substance must be one of.*Example: \{\"substance\""):
        call(server, "decide", {"facts": {"substance": "oil"}})
    with pytest.raises(ToolError, match="Unknown fact"):
        call(server, "decide", {"facts": {"colour": "red"}})
    with pytest.raises(ToolError, match="YYYY-MM-DD"):
        call(server, "decide", {"facts": {}, "received": "July 11"})
    with pytest.raises(ToolError, match="No case is open"):
        mcp_server._State.case = None
        call(server, "patch_facts", {"field": "volume", "value": "3", "quote": "x"})


def test_case_session_keeps_the_stricter_only_gate():
    server = mcp_server.build(review=True)
    report = "Line strike at the yard. About 2 m3 of crude on our lease, maybe more like 20 m3 per the operator."
    opened = call(server, "open_case", {"report": report, "reading": READING})
    assert opened["rules_result"]["status"] == "reportable"
    stricter = call(server, "patch_facts", {"field": "volume", "value": "20", "quote": "maybe more like 20 m3"})
    assert stricter.startswith("Changed volume")
    looser = call(server, "patch_facts", {"field": "release", "value": "no", "quote": "Line strike at the yard"})
    assert looser.startswith("Held for the approver")
    call(server, "finish", {"escalate": False, "reason": "done"})
    done = call(server, "case_result", {"trace": {"transport": "test"}})
    assert done["reading"]["volume"] == 20 and done["reading"]["release"] == "yes"
    assert done["packet"]["route"] == "judgment" and "AGENT-HOLD" in done["packet"]["route_triggers"]
    assert done["packet"]["agent"]["workflow_status"] == "reportable"
    assert done["packet"]["agent"]["transport"] == "test"


def test_triage_report_returns_the_strict_packet(monkeypatch):
    fake = {"packet": {"status": "reportable", "due_at": dt.datetime(2026, 7, 11, 12)}, "facts": None,
            "latency_s": 1.2, "calls": 3, "input_tokens": 3000, "output_tokens": 600, "retries": 0}  # fmt: skip
    monkeypatch.setattr(mcp_server, "_bedrock", lambda: (None, "arn"))
    monkeypatch.setattr(mcp_server, "run_strict", lambda *a: fake)
    got = call(mcp_server.build(), "triage_report", {"report": "text"})
    assert got["packet"]["due_at"] == "2026-07-11 12:00:00" and got["model_calls"] == 3
    assert got["cost_usd"] == pytest.approx((3000 * 0.064 + 600 * 0.256) / 1e6)


def test_triage_report_without_a_profile_says_what_to_set(monkeypatch):
    monkeypatch.delenv("NOVA_LITE_ARN", raising=False)
    with pytest.raises(ToolError, match="NOVA_LITE_ARN"):
        call(mcp_server.build(), "triage_report", {"report": "text"})


def test_over_stdio_with_the_strands_client():
    client, startup = mcp_client.connect(review=False)
    try:
        assert startup > 0
        got = mcp_client.call(client, "decide", {"facts": READING})
        assert got["status"] == "reportable"
        assert mcp_client.call(client, "rule_text", {"rule_id": "PREC"}).startswith("### PREC")
        with pytest.raises(mcp_client.MCPToolError, match="Unknown fact"):
            mcp_client.call(client, "decide", {"facts": {"colour": "red"}})
    finally:
        client.stop(None, None, None)
