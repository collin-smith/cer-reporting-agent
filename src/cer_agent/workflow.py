"""The fixed workflow (article 2's baseline): one model call reads the report, plain code decides.

    report -> extract (Nova Lite, forced tool call) -> Facts -> rules.decide -> decision packet

No agent, no retrieval, no second model call. Deployed, these steps become Lambda states in Step Functions (D7); run
locally, they call Bedrock directly through the tagged inference profile.

Usage (from code/, src on PYTHONPATH):
    NOVA_LITE_ARN=... python3 -m cer_agent.workflow path/to/report.txt [--received 2026-07-11]
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import pathlib
import sys

from cer_agent.extract import extract
from cer_agent.rules import decide

REGION = "ca-central-1"


def make_client(region: str = REGION):
    import boto3
    from botocore.config import Config

    return boto3.client("bedrock-runtime", region_name=region,
                        config=Config(retries={"max_attempts": 10, "mode": "adaptive"}))  # fmt: skip


def packet(facts, extraction: dict | None = None) -> dict:
    """The decision packet a reviewer sees: decision, cited rules, missing facts, and the facts it was based on."""
    d = decide(facts)
    out = dataclasses.asdict(d)
    out["due_at"] = d.due_at.isoformat() if d.due_at else None
    if extraction:
        out["suspicious_instructions"] = bool(extraction["raw"].get("suspicious_instructions"))
        out["extracted"] = extraction["raw"]
    return out


def run(client, model_id: str, report: str, received: dt.date | None = None) -> dict:
    x = extract(client, model_id, report, received)
    return {"packet": packet(x["facts"], x), "facts": x["facts"], **{k: x[k] for k in
            ("input_tokens", "output_tokens", "latency_s")}}  # fmt: skip


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run the fixed workflow on one field report.")
    ap.add_argument("report", type=pathlib.Path)
    ap.add_argument("--received", type=dt.date.fromisoformat, help="date the report arrived (YYYY-MM-DD)")
    args = ap.parse_args(argv)
    arn = os.environ.get("NOVA_LITE_ARN")
    if not arn:
        print("Set NOVA_LITE_ARN (terraform output nova_lite_profile_arn).")
        return 2
    r = run(make_client(), arn, args.report.read_text(encoding="utf-8"), args.received)
    print(json.dumps(r["packet"], indent=2, default=str))
    print(f"tokens in/out {r['input_tokens']}/{r['output_tokens']}, {r['latency_s']:.1f} s", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
