"""The reviewing agent on AgentCore Runtime (article 7, D55): the same `agent.run` as every eval, behind the
Runtime's HTTP contract. That contract is two endpoints on 0.0.0.0:8080:

  POST /invocations  the request body, as sent to InvokeAgentRuntime; here {"report": ..., "received": "YYYY-MM-DD"}
  GET  /ping         {"status": "Healthy"}; the Runtime polls it while the session lives

Starlette and uvicorn already come with the MCP SDK, so no AgentCore SDK is needed (it pins an older pydantic than
the MCP SDK's). The packet is the rules engine's, as everywhere: the model reads and reviews, the code decides.

The Runtime runs one session per microVM. A session ID the client reuses lands on the same microVM; a new one starts
a fresh microVM, so the eval sends a new ID per report (every report independent, as in production), and the
lifecycle's idle timeout (60 s, infra/agentcore.tf) ends each session soon after its reply.

Usage: the zip from scripts/build_agentcore.py has two entry files at its root, one per Runtime: `agent_main.py`
(this module's main) and `tools_main.py` (the MCP server, `--http`). Locally, from code/ with src on PYTHONPATH:
    NOVA_LITE_ARN=... python3 -m cer_agent.runtime        # then POST a report to localhost:8080/invocations
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

STARTED = time.time()  # module load = the microVM's cold start, as far as this process can see it
_STATE = {"invocations": 0}


def triage(body: dict) -> dict:
    """One report through the reviewing agent. Returns what an eval records, plus the session's own view of time."""
    from cer_agent.agent import run
    from cer_agent.cases import facts_json

    report = body.get("report")
    if not isinstance(report, str) or not report.strip():
        raise ValueError('body needs "report": the field report as text')
    received = dt.date.fromisoformat(body["received"]) if body.get("received") else None
    arn = os.environ["NOVA_LITE_ARN"]
    _STATE["invocations"] += 1
    x = run(arn, report, received, os.environ.get("AWS_REGION", "ca-central-1"))
    session = {"invocation": _STATE["invocations"], "process_age_s": round(time.time() - STARTED, 2)}
    return {**{k: v for k, v in x.items() if k != "facts"}, "facts": facts_json(x["facts"]), "session": session}


async def invocations(request: Request) -> JSONResponse:
    import anyio

    try:
        body = await request.json()
    except json.JSONDecodeError:
        return JSONResponse({"error": "body must be JSON"}, status_code=400)
    try:
        out = await anyio.to_thread.run_sync(triage, body)  # the agent is synchronous; keep /ping answering
    except (ValueError, KeyError) as e:
        return JSONResponse({"error": f"{type(e).__name__}: {e}"}, status_code=400)
    return JSONResponse(json.loads(json.dumps(out, default=str)))


async def ping(_request: Request) -> JSONResponse:
    return JSONResponse({"status": "Healthy", "time_of_last_update": int(time.time())})


app = Starlette(routes=[Route("/invocations", invocations, methods=["POST"]), Route("/ping", ping, methods=["GET"])])


def main() -> int:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), log_level="info")
    return 0


if __name__ == "__main__":
    sys.exit(main())
