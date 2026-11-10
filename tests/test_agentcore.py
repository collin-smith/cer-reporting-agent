"""Article 7's AgentCore window (D55), offline: the Runtime entrypoint's contract, the client, the hosted MCP mode,
the zip builder and the SigV4 signer. No AWS calls."""

import datetime as dt
import io
import json
import zipfile

import pytest
from starlette.testclient import TestClient

from cer_agent import agentcore_client, mcp_server, runtime
from cer_agent.cases import facts_json
from cer_agent.rules import Facts
from cer_agent.workflow import packet

FACTS = Facts(discovered_at=dt.datetime(2026, 11, 10, 2, 0), release=True, substance="crude oil", volume_m3=2.0)


def fake_run(arn, report, received, region):
    return {"packet": packet(FACTS), "facts": FACTS, "input_tokens": 9000, "output_tokens": 500,
            "cache_read_tokens": 2228, "cache_write_tokens": 0, "latency_s": 4.2, "retries": 0}  # fmt: skip


def test_runtime_contract_ping_and_bad_bodies(monkeypatch):
    c = TestClient(runtime.app)
    assert c.get("/ping").json()["status"] == "Healthy"
    assert c.post("/invocations", content=b"not json").status_code == 400
    r = c.post("/invocations", json={"received": "2026-11-10"})
    assert r.status_code == 400 and "report" in r.json()["error"]


def test_runtime_returns_what_an_eval_records(monkeypatch):
    import cer_agent.agent

    monkeypatch.setenv("NOVA_LITE_ARN", "arn:test")
    monkeypatch.setattr(cer_agent.agent, "run", fake_run)
    r = TestClient(runtime.app).post("/invocations", json={"report": "Oil on the ground.", "received": "2026-11-10"})
    out = r.json()
    assert r.status_code == 200
    assert out["facts"] == json.loads(json.dumps(facts_json(FACTS)))
    assert out["packet"]["status"] == packet(FACTS)["status"]
    assert out["session"]["invocation"] >= 1 and out["cache_read_tokens"] == 2228


class FakeAgentCore:
    def __init__(self, body):
        self.body, self.sent = body, None

    def invoke_agent_runtime(self, **kw):
        self.sent = kw
        return {"response": io.BytesIO(json.dumps(self.body).encode())}


def test_client_rebuilds_facts_and_splits_hosting_time():
    body = {**fake_run(None, None, None, None), "facts": facts_json(FACTS), "latency_s": 0.0}
    fake = FakeAgentCore(body)
    x = agentcore_client.run_agent("arn:rt", "report text", dt.date(2026, 11, 10), client=fake)
    assert x["facts"] == FACTS
    assert len(fake.sent["runtimeSessionId"]) >= 33 and fake.sent["qualifier"] == "DEFAULT"
    assert json.loads(fake.sent["payload"]) == {"report": "report text", "received": "2026-11-10"}
    assert x["agent_latency_s"] == 0.0 and x["hosting_overhead_s"] == pytest.approx(x["latency_s"])


def test_client_raises_the_runtimes_error():
    with pytest.raises(RuntimeError, match="body needs"):
        agentcore_client.run_agent("arn:rt", "x", None, client=FakeAgentCore({"error": "ValueError: body needs"}))


def test_hosted_server_is_public_scope_only():
    with pytest.raises(SystemExit):
        mcp_server.main(["--http", "--review"])


def test_sigv4_signs_for_agentcore(monkeypatch):
    import httpx2

    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "AKIDEXAMPLE")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "secret")
    monkeypatch.delenv("AWS_SESSION_TOKEN", raising=False)
    monkeypatch.delenv("AWS_PROFILE", raising=False)
    req = httpx2.Request("POST", "https://gw.example/mcp", content=b"{}", headers={"content-type": "application/json"})
    signed = next(agentcore_client.sigv4_auth().auth_flow(req))
    auth = signed.headers["authorization"]
    assert "Credential=AKIDEXAMPLE/" in auth and "/ca-central-1/bedrock-agentcore/aws4_request" in auth


def test_zip_layout_entry_points_and_permissions(tmp_path, monkeypatch):
    import build_agentcore as b

    (tmp_path / "deps/pkg").mkdir(parents=True)
    (tmp_path / "deps/pkg/__init__.py").write_text("")
    (tmp_path / "deps/pkg/__pycache__").mkdir()
    (tmp_path / "deps/pkg/__pycache__/x.pyc").write_bytes(b"")
    monkeypatch.setattr(b, "DEPS", tmp_path / "deps")
    monkeypatch.setattr(b, "BUILD", tmp_path)
    monkeypatch.setattr(b, "OUT", tmp_path / "agentcore.zip")
    assert b.main(["--no-download"]) == 0
    with zipfile.ZipFile(tmp_path / "agentcore.zip") as zf:
        names = set(zf.namelist())
        modes = {i.external_attr >> 16 for i in zf.infolist()}
        for entry in ("agent_main.py", "tools_main.py"):
            compile(zf.read(entry), entry, "exec")
    # agent.py finds the rules spec two levels up from itself, so the repo layout is kept
    want = {"agent_main.py", "tools_main.py", "src/cer_agent/agent.py", "docs/rules-spec.md", "pkg/__init__.py"}
    assert want <= names
    assert not any("__pycache__" in n for n in names)
    assert modes == {0o100644}
