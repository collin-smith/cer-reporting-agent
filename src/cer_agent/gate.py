"""The eval gate (article 2): fails the build when a code change makes saved results worse. Costs nothing: no model
calls. Runs in CI on every push.

Three checks:
1. The rules engine on the answer key's own facts (the oracle arm) gets every case right, on every split.
2. Frozen runs, re-scored with the current code from their saved model output, meet the eval targets where they
   should (the strictest-of-layouts check, on dev and on test rebuilt from saved layout readings).
3. No frozen run scores worse than the committed baseline (`evals/gate-baseline.json`): fewer correct statuses or
   routes, or more missed reports, late deadlines or unneeded notices, fails.

A model can drift and this gate won't see it: it re-checks what the code does with saved readings, not new
readings. Live runs (3 passes, priced first) cover the model; the gate covers the code between them.

Usage (from code/):
    python -m cer_agent.gate                     # check; exit 1 on any failure
    python -m cer_agent.gate --update-baseline   # after an intended change; commit the new baseline with it
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys

from cer_agent.evals import (
    CODE,
    _rep,
    check_targets_by_pass,
    load_cases,
    load_config,
    load_rows,
    rescore_row,
    run_case,
    score_case,
)

BASELINE = CODE / "evals" / "gate-baseline.json"
# Counts where higher is better, and where lower is better.
UP = ("status", "route")
DOWN = ("missed", "late", "over_notify")


def counts(rows: list[dict]) -> dict:
    s = [r["score"] for r in rows]
    return {"n": len(rows), "status": sum(x["status"] for x in s), "route": sum(x["route"] for x in s),
            "missed": sum(x["missed_report"] for x in s), "late": sum(x["late_deadline"] for x in s),
            "over_notify": sum(x["over_notify"] for x in s)}  # fmt: skip


def strict_replay(rows: list[dict], cases: dict) -> list[dict]:
    """The strictest-of-layouts check rebuilt from a single-reading run that also read each report in the layout
    variants (D33's $0 replay): per case and pass, combine the layouts' readings the way `run_strict` does."""
    from cer_agent.extract import to_facts
    from cer_agent.workflow import LAYOUTS, recombine

    groups: dict[tuple, dict] = {}
    for r in rows:
        base, _, layout = r["id"].partition("~")
        groups.setdefault((base, _rep(r)), {})[layout or "as_written"] = r
    out = []
    for (base, _), g in groups.items():
        order = ["as_written", *[k for k in LAYOUTS if k in g]]
        case, first = cases[base], g["as_written"]
        received = dt.date.fromisoformat(case["discovered_at"][:10])
        pk = recombine({k: g[k]["packet"]["extracted"] for k in order}, received)
        got = to_facts(first["packet"]["extracted"], received)
        out.append({**first, "packet": pk, "score": score_case(case, pk, got),
                    "latency_s": max(g[k]["latency_s"] for k in order)})  # fmt: skip
    return out


def evaluate(cfg: dict) -> dict:
    """Every gated result's counts, plus whether the oracle and the targeted runs pass."""
    cases = {c["id"]: c for c in load_cases(cfg, ["dev", "test", "heldout"])}
    oracle = [{**run_case(c, "oracle"), "rep": 1} for c in cases.values()]
    o = counts(oracle)
    results = {"oracle": {"counts": o, "ok": o["status"] == o["route"] == o["n"] and not o["missed"] + o["late"]}}
    runs_dir = CODE / cfg["run"]["runs_dir"]
    for g in cfg["gate"]["runs"]:
        saved = load_rows(runs_dir / g["run"] / "results.jsonl")
        if not saved:
            raise SystemExit(f"Gate run {g['run']} has no saved results.")
        rows = [rescore_row(r, cases) for r in saved]
        if g.get("mode") == "strict-replay":
            rows = strict_replay(rows, cases)
        else:
            rows = [r for r in rows if "~" not in r["id"]]  # the reports as written
        res = {"counts": counts(rows), "targets_ok": None}
        if g.get("targets"):
            missed = [t for t in check_targets_by_pass(rows, cfg["targets"]) if not t["met"]]
            res["targets_ok"] = not missed
            res["targets_missed"] = [f"{t['target']} {t['value']:.3g}" for t in missed]
        results[g["name"]] = res
    return results


def compare(baseline: dict, current: dict) -> list[str]:
    """What got worse than the baseline (empty if nothing did)."""
    worse = []
    for name, b in baseline.items():
        c = current.get(name, {}).get("counts")
        if c is None:
            worse.append(f"{name}: no longer gated")
            continue
        if c["n"] != b["n"]:
            worse.append(f"{name}: {c['n']} results, baseline {b['n']}")
        worse += [f"{name}: {k} {c[k]} < baseline {b[k]}" for k in UP if c[k] < b[k]]
        worse += [f"{name}: {k} {c[k]} > baseline {b[k]}" for k in DOWN if c[k] > b[k]]
    return worse


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="The $0 eval gate: oracle, targets and baseline on frozen runs.")
    ap.add_argument("--update-baseline", action="store_true", help="write the current counts as the new baseline")
    args = ap.parse_args(argv)
    cfg = load_config()
    current = evaluate(cfg)
    failures = []
    for name, r in current.items():
        c = r["counts"]
        line = (f"{name:28} n={c['n']:4}  status {c['status']:4}  route {c['route']:4}  missed {c['missed']}  "
                f"late {c['late']}  over-notify {c['over_notify']}")  # fmt: skip
        if name == "oracle" and not r["ok"]:
            failures.append("oracle: the rules engine got a case wrong on the answer key's own facts")
        if r.get("targets_ok") is False:
            failures.append(f"{name}: targets missed: {', '.join(r['targets_missed'])}")
        print(line + ("  targets met" if r.get("targets_ok") else ""))
    if args.update_baseline:
        BASELINE.write_text(json.dumps({k: v["counts"] for k, v in current.items()}, indent=2) + "\n")
        print(f"Baseline written to {BASELINE.relative_to(CODE)}; commit it with the change that moved it.")
    elif BASELINE.exists():
        failures += compare(json.loads(BASELINE.read_text()), current)
    else:
        failures.append(f"no baseline at {BASELINE.relative_to(CODE)}; run with --update-baseline")
    for f in failures:
        print(f"::error::{f}" if "GITHUB_ACTIONS" in os.environ else f"FAIL {f}")
    print("Gate passed." if not failures else f"Gate failed: {len(failures)} problem(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
