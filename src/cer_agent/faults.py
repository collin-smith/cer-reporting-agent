"""Article 6 (D52): what happens when the model fails, measured without calling it.

A botocore `before-send` hook answers every Converse call on the machine: either with an injected error, so
botocore's own retry rules, backoff and retry quota run exactly as they would against Bedrock, or with the reading
a real run saved for that exact text, so the decision downstream is a real one. No request leaves the machine ($0).
Retry sleeps go on a virtual clock (recorded, not slept), so a run that "waits" minutes takes seconds.

Usage (from code/, with src on PYTHONPATH):
  python -m cer_agent.faults run [--source RUN_DIR] [--split test] [--scenario NAME ...] [--retries 10 3]  # $0
  python -m cer_agent.faults summary RUN_DIR                                                # $0

What it measures, per scenario: who answered (Nova Lite, the fallback, or nobody, so a person), whether the
decision still matches the answer key, how many attempts each model took, and how long the retries waited (the
longest chain of the three parallel readings: what the Lambda would wait). The fallback replays Nova's saved
reading, so its accuracy here is Nova's: this measures the switch, not the fallback model.
"""

from __future__ import annotations

import argparse
import collections
import contextlib
import datetime as dt
import functools
import json
import pathlib
import threading

from botocore import endpoint as _endpoint
from botocore.awsrequest import AWSResponse
from botocore.config import Config

from cer_agent.extract import TOOL, normalise
from cer_agent.workflow import REGION, error_code, layouts, run_strict

CODE = pathlib.Path(__file__).resolve().parents[2]
CASES = CODE / "evals/cases/cases.jsonl"
RUNS = CODE / "evals/runs"
SOURCE = RUNS / "20261108-105630-workflow-nova-strict-test"  # strict Nova Lite, test split, every layout saved
LAMBDA_TIMEOUT_S = 120  # infra/approval.tf

STATUS = {"ThrottlingException": 429, "ServiceUnavailableException": 503, "InternalServerException": 500,
          "ModelNotReadyException": 429, "ModelTimeoutException": 408, "ModelErrorException": 424,
          "AccessDeniedException": 403, "ValidationException": 400}  # fmt: skip

# Each scenario: (primary error, how many attempts per reading fail (None = all), fallback error, fallback on?).
SCENARIOS = {
    "clean": (None, 0, None, True),
    "throttled-briefly": ("ThrottlingException", 2, None, True),
    "throttled": ("ThrottlingException", None, None, True),
    "malformed-tool-call": ("ModelErrorException", None, None, True),
    "model-timeout": ("ModelTimeoutException", None, None, True),
    "model-not-ready": ("ModelNotReadyException", None, None, True),
    "outage": ("ServiceUnavailableException", None, None, True),
    "outage-no-fallback": ("ServiceUnavailableException", None, None, False),
    "outage-fallback-not-enabled": ("ServiceUnavailableException", None, "AccessDeniedException", True),
}


class _Body:
    def __init__(self, data: bytes):
        self.data = data

    def stream(self, **kw):
        yield self.data


def _response(status: int, body: dict, headers: dict | None = None) -> AWSResponse:
    from botocore.awsrequest import HeadersDict

    h = HeadersDict({"content-type": "application/json", **(headers or {})})
    return AWSResponse("https://bedrock-runtime.local", status, h, _Body(json.dumps(body).encode()))


class VirtualClock:
    """Stands in for time in botocore's retry path: the backoff sleep between attempts (endpoint.py) and adaptive
    mode's client-side rate limiter (retries/bucket.py), which otherwise waits for real. Sleeps are kept per reading
    (the layout text the thread last sent, primary and fallback together: one chain); the limiter's clock reads real
    time plus the longest chain so far, as the readings run in parallel."""

    def __init__(self):
        self.waits = collections.defaultdict(float)
        self.lock = threading.Lock()
        self.current = threading.local()

    def sleep(self, seconds: float):
        with self.lock:
            self.waits[getattr(self.current, "text", None)] += seconds

    def current_time(self) -> float:
        import time

        return time.time() + max(self.waits.values(), default=0.0)

    def __getattr__(self, name):  # everything else in `time` as usual
        import time

        return getattr(time, name)


def _acquire(self, amount, block):
    """TokenBucket._acquire with the wait on the virtual clock instead of a condition variable."""
    self._refill()
    while amount > self._current_capacity:
        self._clock.sleep(self._sleep_amount(amount))
        self._refill()
    self._current_capacity -= amount
    return True


@contextlib.contextmanager
def virtual_time():
    """Retry sleeps and rate-limiter waits recorded, not slept. Clients must be created inside the block."""
    from botocore.retries import adaptive, bucket

    clock = VirtualClock()
    saved = (_endpoint.time, adaptive.bucket.Clock, bucket.TokenBucket._acquire)
    _endpoint.time, adaptive.bucket.Clock, bucket.TokenBucket._acquire = clock, lambda: clock, _acquire
    try:
        yield clock
    finally:
        _endpoint.time, adaptive.bucket.Clock, bucket.TokenBucket._acquire = saved


class FakeBedrock:
    """Answers Converse locally: an injected error, or the saved reading for that text."""

    def __init__(self, replay: dict[str, dict], plan, clock: VirtualClock | None = None):
        self.replay, self.plan, self.clock = replay, plan, clock
        self.attempts = collections.Counter()  # (model, layout text) -> attempts so far; a report's texts are unique
        self.lock = threading.Lock()

    def attach(self, client, name: str):
        client.meta.events.register_first("before-send.bedrock-runtime.Converse", functools.partial(self._send, name))
        return client

    def _send(self, name, request, **kw):
        body = json.loads(request.body)
        text = body["messages"][0]["content"][0]["text"].removeprefix("<report>\n").removesuffix("\n</report>")
        key = (name, text)
        if self.clock:
            self.clock.current.text = text  # the next sleep on this thread belongs to this reading
        with self.lock:
            n = self.attempts[key]
            self.attempts[key] += 1
        if err := self.plan(name, n):
            return _response(STATUS[err], {"message": f"injected {err}"}, {"x-amzn-ErrorType": f"{err}:"})
        raw = self.replay[text]
        return _response(200, {
            "output": {"message": {"role": "assistant", "content": [
                {"toolUse": {"toolUseId": "t1", "name": TOOL["name"], "input": raw}}]}},
            "stopReason": "tool_use", "usage": {"inputTokens": 1500, "outputTokens": 150, "totalTokens": 1650},
            "metrics": {"latencyMs": 0}})  # fmt: skip


def plan_for(scenario: str):
    err, fails, fb_err, _ = SCENARIOS[scenario]

    def plan(name: str, attempt: int) -> str | None:
        if name == "fallback":
            return fb_err
        return err if err and (fails is None or attempt < fails) else None

    return plan


def client(fake: FakeBedrock, name: str, max_attempts: int = 10):
    """A client as `workflow.make_client` builds it (adaptive retries), answered by `fake`."""
    import boto3

    c = boto3.client("bedrock-runtime", region_name=REGION, aws_access_key_id="x", aws_secret_access_key="x",
                     config=Config(retries={"max_attempts": max_attempts, "mode": "adaptive"}))  # fmt: skip
    return fake.attach(c, name)


def load(source: pathlib.Path, split: str | None):
    cases = {c["id"]: c for c in map(json.loads, CASES.read_text(encoding="utf-8").splitlines())}
    rows = [json.loads(line) for line in (source / "results.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r.get("rep", 1) == 1 and (split is None or r["split"] == split)]
    replay = {}
    for r in rows:
        texts = layouts(cases[r["id"]]["report"])
        for name, text in texts.items():
            replay[normalise(text)] = r["packet"]["layouts"][name]["extracted"]
    return cases, rows, replay


def run(source: pathlib.Path, split: str | None, scenarios: list[str], retries: list[int]) -> pathlib.Path:
    cases, rows, replay = load(source, split)
    out = RUNS / f"{dt.datetime.now():%Y%m%d-%H%M%S}-faults"
    out.mkdir(parents=True)
    with virtual_time() as clock, (out / "results.jsonl").open("w", encoding="utf-8") as fh:
        for max_attempts in retries:
            for scenario in scenarios:
                for r in rows:
                    case = cases[r["id"]]
                    fake = FakeBedrock(replay, plan_for(scenario), clock)
                    fb = (client(fake, "fallback", max_attempts), "fallback-model") if SCENARIOS[scenario][3] else None
                    clock.waits.clear()
                    row = {"scenario": scenario, "retries": max_attempts, "id": r["id"], "kind": r["kind"],
                           "expected": case["expected"]["status"]}  # fmt: skip
                    try:
                        x = run_strict(client(fake, "primary", max_attempts), "primary-model", case["report"],
                                       dt.date.fromisoformat(case["discovered_at"][:10]), fb)  # fmt: skip
                        row |= {"answered_by": "fallback" if x["fallback"]["readings"] else "primary",
                                "fallback_readings": x["fallback"]["readings"], "status": x["packet"]["status"],
                                "deadline": x["packet"]["deadline"]}  # fmt: skip
                    except Exception as e:
                        row |= {"answered_by": "person", "error": error_code(e), "status": None}
                    att = collections.Counter()
                    for (name, _), n in fake.attempts.items():
                        att[name] += n
                    row |= {"status_ok": row["status"] == row["expected"], "attempts": dict(att),
                            "retry_wait_s": round(max(clock.waits.values(), default=0.0), 2)}  # fmt: skip
                    fh.write(json.dumps(row) + "\n")
                    fh.flush()
    meta = {"source": source.name, "split": split, "scenarios": scenarios, "retries": retries}
    (out / "run.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    summarise(out)
    return out


def summarise(out: pathlib.Path) -> dict:
    rows = [json.loads(line) for line in (out / "results.jsonl").open(encoding="utf-8")]
    s = {}
    for retries, scenario in dict.fromkeys((r["retries"], r["scenario"]) for r in rows):
        rs = [r for r in rows if (r["retries"], r["scenario"]) == (retries, scenario)]
        waits = sorted(r["retry_wait_s"] for r in rs)
        reportable = [r for r in rs if r["expected"] in ("reportable", "precautionary")]
        s[f"retries={retries} {scenario}"] = {
            "reports": len(rs),
            "answered_by": dict(collections.Counter(r["answered_by"] for r in rs)),
            "status_ok": sum(r["status_ok"] for r in rs),
            "missed_reportable": sum(r["status"] == "not reportable" for r in reportable),
            "errors_to_person": dict(collections.Counter(r["error"] for r in rs if r.get("error"))),
            "attempts_per_report": {
                m: round(sum(r["attempts"].get(m, 0) for r in rs) / len(rs), 1) for m in ("primary", "fallback")
            },  # fmt: skip
            "retry_wait_s": {"p50": waits[len(waits) // 2], "max": waits[-1]},
            "over_lambda_timeout": sum(w > LAMBDA_TIMEOUT_S for w in waits),
        }
    (out / "summary.json").write_text(json.dumps(s, indent=2), encoding="utf-8")
    print(json.dumps(s, indent=2))
    return s


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Fault injection for the reader's retries and fallback ($0).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--source", type=pathlib.Path, default=SOURCE)
    r.add_argument("--split", default="test")
    r.add_argument("--scenario", nargs="+", choices=list(SCENARIOS), default=list(SCENARIOS))
    r.add_argument("--retries", nargs="+", type=int, default=[10, 3], help="botocore max_attempts (retries)")
    sm = sub.add_parser("summary")
    sm.add_argument("run_dir", type=pathlib.Path)
    args = ap.parse_args(argv)
    if args.cmd == "summary":
        summarise(args.run_dir)
    else:
        print(run(args.source, args.split, args.scenario, args.retries))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
