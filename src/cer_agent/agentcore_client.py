"""Clients for article 7's AgentCore window (D55): the agent on Runtime, and the MCP tools through Gateway.

- `run_agent`: one report to the agent's Runtime (InvokeAgentRuntime), a new session per report, as production
  would. Returns what `agent.run` returns, plus the client's own wall time, so the eval can separate the agent's
  time (measured inside the microVM) from what hosting adds (session start, network, the Runtime's proxy).
- `gateway_tools`: the MCP client against the Gateway URL, each request signed with SigV4 for
  `bedrock-agentcore` from the caller's AWS credentials (the Gateway's inbound auth is AWS_IAM: no Cognito, no
  tokens to hand out). Lists the tools and calls them, as Claude Code did over stdio in article 5.

Env: AGENT_RUNTIME_ARN, GATEWAY_URL (terraform output agentcore_agent_runtime_arn / agentcore_gateway_url).
"""

from __future__ import annotations

import datetime as dt
import json
import time
import uuid

REGION = "ca-central-1"


def _client(region: str = REGION):
    import boto3
    from botocore.config import Config

    # The agent runs a minute at most; the default 60 s read timeout would cut a slow review short.
    return boto3.client("bedrock-agentcore", region_name=region, config=Config(read_timeout=300))


def run_agent(runtime_arn: str, report: str, received: dt.date | None, client=None) -> dict:
    from cer_agent.evals import facts_from_json

    body = {"report": report, **({"received": received.isoformat()} if received else {})}
    t0 = time.perf_counter()
    r = (client or _client()).invoke_agent_runtime(
        agentRuntimeArn=runtime_arn,
        runtimeSessionId=f"cer-{uuid.uuid4()}",  # 33+ characters; new each time = a fresh microVM
        qualifier="DEFAULT",
        contentType="application/json",
        accept="application/json",
        payload=json.dumps(body).encode(),
    )
    out = json.loads(r["response"].read())
    wall = time.perf_counter() - t0
    if "error" in out:
        raise RuntimeError(f"Runtime: {out['error']}")
    return {**out, "facts": facts_from_json(out["facts"]), "agent_latency_s": out["latency_s"], "latency_s": wall,
            "hosting_overhead_s": wall - out["latency_s"]}  # fmt: skip


def sigv4_auth(service: str = "bedrock-agentcore", region: str = REGION):
    """An httpx2 auth that signs each request with the caller's credentials (botocore's SigV4). The body is read
    first: SigV4 signs its hash."""
    import boto3
    import httpx2
    from botocore.auth import SigV4Auth
    from botocore.awsrequest import AWSRequest

    creds = boto3.Session().get_credentials()

    class SigV4(httpx2.Auth):
        requires_request_body = True

        def auth_flow(self, request):
            aws = AWSRequest(method=request.method, url=str(request.url), data=request.content,
                             headers={k: v for k, v in request.headers.items() if k.lower() in SIGNED})  # fmt: skip
            SigV4Auth(creds.get_frozen_credentials(), service, region).add_auth(aws)
            request.headers.update(dict(aws.headers))
            yield request

    return SigV4()


SIGNED = {"host", "content-type", "accept", "mcp-session-id", "mcp-protocol-version"}


async def gateway_tools(url: str, calls: list[tuple[str, dict]]) -> dict:
    """List the Gateway's tools and make `calls` through it. Gateway names a target's tools `<target>___<tool>`."""
    import httpx2
    from mcp import ClientSession
    from mcp.client.streamable_http import streamable_http_client

    out: dict = {"calls": []}
    async with (
        httpx2.AsyncClient(auth=sigv4_auth(), timeout=120) as http,
        streamable_http_client(url, http_client=http) as streams,
        ClientSession(streams[0], streams[1]) as s,
    ):
        t0 = time.perf_counter()
        await s.initialize()
        tools = await s.list_tools()
        out["tools"] = [t.name for t in tools.tools]
        out["list_s"] = round(time.perf_counter() - t0, 2)
        for name, args in calls:
            full = next((t for t in out["tools"] if t == name or t.endswith(f"___{name}")), name)
            t0 = time.perf_counter()
            res = await s.call_tool(full, args)
            text = "".join(getattr(c, "text", "") for c in res.content)
            out["calls"].append({"tool": full, "s": round(time.perf_counter() - t0, 2), "error": res.is_error,
                                 "text": text[:400]})  # fmt: skip
    return out


def main(argv=None) -> int:
    """Gateway demo: list the tools and look up a rule ($0, no model call); with --triage, also read a report."""
    import argparse
    import os

    import anyio

    ap = argparse.ArgumentParser(description="Call the CER tools through AgentCore Gateway (SigV4).")
    ap.add_argument("--url", default=os.environ.get("GATEWAY_URL"))
    ap.add_argument("--triage", help="also triage this report file (a Nova Lite call, ~0.05 cents)")
    args = ap.parse_args(argv)
    if not args.url:
        ap.error("set GATEWAY_URL (terraform output agentcore_gateway_url) or pass --url")
    calls = [("rule_text", {"rule_id": "T24"})]
    if args.triage:
        with open(args.triage, encoding="utf-8") as fh:
            calls.append(("triage_report", {"report": fh.read()}))
    print(json.dumps(anyio.run(gateway_tools, args.url, calls), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
