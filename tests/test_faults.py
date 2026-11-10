import datetime as dt

import pytest
from botocore.exceptions import ClientError

from cer_agent import faults, workflow


def _err(code):
    return ClientError({"Error": {"Code": code, "Message": "x"}}, "Converse")


def test_read_falls_back_only_on_model_failures(monkeypatch):
    calls = []

    def fake_extract(client, model, text, received):
        calls.append(model)
        if model == "nova":
            raise client
        return {"facts": None, "raw": {}, "input_tokens": 1, "output_tokens": 1}

    monkeypatch.setattr(workflow, "extract", fake_extract)
    x = workflow.read(_err("ServiceUnavailableException"), "nova", "t", None, ("fb-client", "haiku"))
    assert (x["model"], x["primary_error"], calls) == ("fallback", "ServiceUnavailableException", ["nova", "haiku"])
    with pytest.raises(ClientError):  # ours to fix: straight to a person
        workflow.read(_err("ValidationException"), "nova", "t", None, ("fb-client", "haiku"))
    with pytest.raises(ClientError):  # no fallback configured
        workflow.read(_err("ThrottlingException"), "nova", "t", None, None)


def _strict(scenario, max_attempts=10):
    """One report through run_strict with the fake Bedrock: real botocore retries, virtual sleep."""
    report = "Gas release at the compressor station, about 2 m3, discovered 2026-07-11 at 09:00."
    raw = {"release": "yes", "substance": "natural_gas", "volume": 2}
    replay = {workflow.normalise(t): raw for t in workflow.layouts(report).values()}
    with faults.virtual_time() as clock:
        fake = faults.FakeBedrock(replay, faults.plan_for(scenario), clock)
        fb = (faults.client(fake, "fallback", max_attempts), "fb") if faults.SCENARIOS[scenario][3] else None
        x = workflow.run_strict(faults.client(fake, "primary", max_attempts), "p", report, dt.date(2026, 7, 11), fb)
    return x, fake, clock


def test_brief_throttling_is_retried_by_botocore():
    x, fake, clock = _strict("throttled-briefly")
    assert x["fallback"]["readings"] == 0
    assert all(n == 3 for (m, _), n in fake.attempts.items() if m == "primary")  # 2 throttles + success
    assert max(clock.waits.values()) > 0


def test_malformed_tool_call_is_not_retried_by_botocore_and_falls_back():
    x, fake, _ = _strict("malformed-tool-call")
    assert x["fallback"] == {**x["fallback"], "readings": x["calls"], "errors": ["ModelErrorException"]}
    # the reader's own temperature steps: 1 + 2 attempts, no botocore retries
    assert all(n == 3 for (m, _), n in fake.attempts.items() if m == "primary")


def test_fallback_not_enabled_goes_to_a_person():
    with pytest.raises(ClientError) as e:
        _strict("outage-fallback-not-enabled")
    assert workflow.error_code(e.value) == "AccessDeniedException"


def test_ten_retries_outlast_the_lambda_three_fit():
    """botocore's max_attempts counts retries: 10 means 11 calls, and the backoff plus adaptive mode's rate limiter
    outlast the Lambda's 120 s before the fallback is tried. 3 retries leave room for it."""
    x, fake, clock = _strict("throttled", 10)
    assert all(n == 11 for (m, _), n in fake.attempts.items() if m == "primary")
    x, fake, clock = _strict("throttled", 3)
    assert x["fallback"]["readings"] == x["calls"] and x["fallback"]["errors"] == ["ThrottlingException"]
    assert all(n == 4 for (m, _), n in fake.attempts.items() if m == "primary")
    assert max(clock.waits.values()) < faults.LAMBDA_TIMEOUT_S / 4
