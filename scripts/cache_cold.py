"""Article 7 (D53): prompt caching when reports arrive one at a time, more than 5 minutes apart.

Nova Lite's cache lives 5 minutes, so a lone report at 2 a.m. finds nothing cached from the last one. This sends
dev reports one at a time with caching on (CER_PROMPT_CACHE=1), alternating the strict check and the reviewing
agent, and waits GAP seconds (default 360, past the TTL) between them. What it measures is what each case reads back
from its own earlier calls: none for the strict check's parallel readings, the later turns for the agent.

Each row is the harness's own `run_case` (same scoring, same cost: cache writes at the full input price), written
to evals/runs/<run-id>-cache-cold/results.jsonl as it goes. Takes about (N - 1) x GAP seconds.

Usage (from code/, NOVA_LITE_ARN set):
    .venv/bin/python -I scripts/cache_cold.py [--n 10] [--gap 360]
"""

import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import time

CODE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "src"))
os.environ["CER_PROMPT_CACHE"] = "1"

from cer_agent import evals  # noqa: E402
from cer_agent.workflow import make_client  # noqa: E402

ARMS = ("workflow-nova-strict-cache", "agent-nova-cache")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--gap", type=int, default=360, help="seconds between reports (Nova's TTL is 300)")
    args = ap.parse_args()
    if not os.environ.get("NOVA_LITE_ARN"):
        print("Set NOVA_LITE_ARN (the agentic-ai-nova-lite application inference profile).")
        return 2
    cfg = evals.load_config()
    model = cfg["models"]["nova-lite"]
    cases = sorted(evals.load_cases(cfg, ["dev"]), key=lambda c: c["id"])[: args.n]
    out = CODE / "evals" / "runs" / f"{dt.datetime.now():%Y%m%d-%H%M%S}-cache-cold"
    out.mkdir(parents=True)
    client = make_client(model.get("region", "ca-central-1"))
    with (out / "results.jsonl").open("w") as f:
        for i, case in enumerate(cases):
            if i:
                time.sleep(args.gap)
            arm = ARMS[i % 2]
            row = {"arm": arm, "sent_at": dt.datetime.now().isoformat(timespec="seconds"),
                   **evals.run_case(case, arm, client, model)}  # fmt: skip
            f.write(json.dumps(row, default=str) + "\n")
            f.flush()
            print(f"{i + 1}/{len(cases)} {case['id']} {arm}: right={row['score']['status']} in={row['input_tokens']} "
                  f"read={row['cache_read_tokens']} write={row['cache_write_tokens']} ${row['cost_usd']:.6f}",
                  flush=True)  # fmt: skip
    print(f"Saved {out.relative_to(CODE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
