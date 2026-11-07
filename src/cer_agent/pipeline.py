"""One case end to end, traced (article 2): the agent arm (extract, review, decide), then the drafter, then the judge,
each a span under one root "case" span. Writes traces.jsonl, the drafts and verdicts, and a per-stage summary.

This is the production path in miniature; the eval harness scores decisions, this shows where each case's time and
tokens go. Models: Nova Lite for every stage (the judge's frozen prompt v5 was measured on it, D36).

Usage (from code/, src on PYTHONPATH):
    NOVA_LITE_ARN=... python -m cer_agent.pipeline --split dev --n 5 [--only CL-007 ...] [--yes]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys

from cer_agent import agent, drafter, judge, tracing
from cer_agent.evals import CODE, load_cases, load_config
from cer_agent.workflow import make_client

# USD per case, measured on 2026-11-07: the agent arm about $0.00085, a draft about $0.0002, a judge call about
# $0.0004 (D36-D38). Used only to quote a run before it starts.
EST_PER_CASE = 0.00085 + 0.0002 + 0.0004


def run_case(case: dict, client, model_id: str, region: str) -> dict:
    received = dt.date.fromisoformat(case["discovered_at"][:10])
    with tracing.span("case", id=case["id"], split=case["split"], expected=case["expected"]["status"]) as root:
        a = agent.run(model_id, case["report"], received, region, client=client)
        pk = a["packet"]
        d = drafter.draft(client, model_id, case["report"], pk)
        checks = judge.code_checks(pk, d["text"], case["report"])
        verdict = judge.judge(client, model_id, case["report"], d["text"]) if d["fields"] else None
        for k in ("status", "deadline", "route"):
            root.set_attribute(f"cer.{k}", pk[k] or "none")
        root.set_attribute("cer.correct", pk["status"] == case["expected"]["status"])
    return {"id": case["id"], "packet": {k: pk[k] for k in ("status", "deadline", "route", "route_triggers")},
            "held": pk["agent"].get("held", []), "draft": d["text"], "flags": d["flags"], "code_checks": checks,
            "judge": verdict and verdict["criteria"]}  # fmt: skip


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run cases end to end with per-stage tracing.")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--n", type=int, default=5, help="first N cases of the split (ignored with --only)")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--yes", action="store_true", help="skip the cost confirmation")
    args = ap.parse_args(argv)
    arn = os.environ.get("NOVA_LITE_ARN")
    if not arn:
        print("Set NOVA_LITE_ARN (the tagged Nova Lite profile ARN).")
        return 2
    cfg = load_config()
    model = cfg["models"]["nova-lite"]
    cases = load_cases(cfg, [args.split], args.only)
    cases = cases if args.only else cases[: args.n]
    print(f"{len(cases)} cases end to end (agent, draft, judge) on Nova Lite; about ${EST_PER_CASE * len(cases):.3f}.")
    if not args.yes and input("Run? [y/N] ").strip().lower() != "y":
        return 1
    out = CODE / "evals" / "traces" / f"{dt.datetime.now():%Y%m%d-%H%M%S}-pipeline-{args.split}"
    provider = tracing.setup(out / "traces.jsonl")
    client = make_client(model["region"])
    results = []
    for case in cases:
        r = run_case(case, client, arn, model["region"])
        results.append(r)
        print(f"{case['id']}: {r['packet']['status']} {r['packet']['deadline']} {r['packet']['route']}", flush=True)
    provider.shutdown()
    (out / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    spans = [json.loads(line) for line in (out / "traces.jsonl").read_text(encoding="utf-8").splitlines()]
    table = tracing.render(tracing.summary(spans, model["price_in"], model["price_out"]))
    (out / "summary.md").write_text(f"# Traced pipeline run {out.name}\n\n{table}\n", encoding="utf-8")
    print(table)
    print(f"Wrote {out.relative_to(CODE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
