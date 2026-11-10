"""Article 7, cost per case from the saved runs ($0, no model calls).

Three things, all from evals/runs/*/results.jsonl:

1. Cost per case at the AWS Price List rates for Nova Lite in ca-central-1 (2026-11-10), next to the cost the harness
   recorded at the config's older rates ($0.06 / $0.24).
2. What prompt caching could save, as an estimate to price the live run, in two arrival patterns:
   - warm: reports arrive within Nova's 5-minute cache TTL of each other (an eval batch, a busy day), so every
     call's fixed prefix (tool schema + system prompt) is read from the cache;
   - cold: one report at 2 a.m., nothing cached. Only calls made one after another inside the case can hit:
     the agent's later turns. The strict check's three readings run in parallel, and a request sent before an
     identical one has started its response writes its own entry instead of reading one (Bedrock user guide).
   Nova Lite takes cache points in `system` and `messages` only (not `tools`), needs a 1K-token prefix, and caches
   at most 20K tokens. Prefix sizes below are estimates from the prompt lengths and the 2026-11-07 traces; the
   live run measures cacheReadInputTokens instead.
3. A Nova-only cascade, replayed: the strict check for cases it routes clear-cut, the reviewing agent only for the
   cases it routes to judgment. Same held-out cases and passes, so each case's two results can be combined.

Usage (from code/):
    .venv/bin/python -I scripts/cost_article7.py
"""

import collections
import json
import pathlib
import statistics as st

CODE = pathlib.Path(__file__).resolve().parents[1]
RUNS = CODE / "evals" / "runs"

# USD per 1M tokens, AWS Price List, AmazonBedrock, regionCode ca-central-1, 2026-11-10 (CAN1-NovaLite-*).
PRICE_IN, PRICE_OUT, PRICE_CACHE_READ, PRICE_CACHE_WRITE = 0.064, 0.256, 0.016, 0.0
CONFIG_IN, CONFIG_OUT = 0.06, 0.24  # evals/config.toml, what the harness recorded

# Estimated fixed prefix per call, tokens (tools + system). Extraction: 1,702 + 7,030 characters, and its input
# varies only 2,788-2,855 tokens across reports. Agent turn: system + 4 tool schemas; the first turn's smallest input
# is 1,269 tokens including the case. Both are above Nova's 1K minimum; the drafter's (~850) is not.
EXTRACT_PREFIX, AGENT_PREFIX = 2_600, 1_150

HELDOUT = {
    "workflow": "20261108-081029-workflow-nova-heldout",
    "strict": "20261108-081321-workflow-nova-strict-heldout",
    "agent": "20261108-081634-agent-nova-heldout",
    "supervisor": "20261108-083527-supervisor-nova-heldout",
}
SHIPPED = ("strict, test (after the D44 fix)", "20261108-105630-workflow-nova-strict-test")


def load(run: str) -> list[dict]:
    return [json.loads(line) for line in (RUNS / run / "results.jsonl").open()]


def cost(tin: float, tout: float, cached: float = 0.0) -> float:
    return ((tin - cached) * PRICE_IN + cached * PRICE_CACHE_READ + tout * PRICE_OUT) / 1e6


def calls(arm: str, r: dict) -> tuple[int, int]:
    """(extraction calls, agent turns) for one case."""
    turns = (r["packet"].get("agent") or {}).get("turns") or 0
    return (3 if arm == "strict" else 1), turns


def cached_tokens(arm: str, r: dict, warm: bool) -> float:
    ext, turns = calls(arm, r)
    if warm:
        return ext * EXTRACT_PREFIX + turns * AGENT_PREFIX
    return max(turns - 1, 0) * AGENT_PREFIX  # cold: only the agent's later turns


def scored(r: dict) -> dict:
    s = r["score"]
    return {"right": s["status"], "missed": s["missed_report"], "late": s["late_deadline"]}


def table(rows: list[list], head: list[str]) -> str:
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def per_1000(x: float) -> str:
    return f"${x * 1000:.2f}"


def saving(x: float | None, base: float) -> str:
    if x is None:
        return "–"
    cut = 1 - x / base
    return per_1000(x) + (f" (−{cut:.0%})" if cut >= 0.005 else " (none)")


def main() -> None:
    runs = {arm: load(run) for arm, run in HELDOUT.items()}

    # 1 + 2: cost per case, recorded vs. Price List, and caching estimates.
    rows = []
    for arm, R in runs.items():
        tin = st.mean(r["input_tokens"] for r in R)
        tout = st.mean(r["output_tokens"] for r in R)
        recorded = st.mean(r["cost_usd"] for r in R)
        listed = cost(tin, tout)
        if arm == "supervisor":  # several agents with their own prompts: not estimated
            warm = cold = None
        else:
            warm = st.mean(cost(r["input_tokens"], r["output_tokens"], cached_tokens(arm, r, True)) for r in R)
            cold = st.mean(cost(r["input_tokens"], r["output_tokens"], cached_tokens(arm, r, False)) for r in R)
        rows.append([
            arm, f"{tin:,.0f}", f"{tout:,.0f}", per_1000(recorded), per_1000(listed),
            saving(warm, listed), saving(cold, listed),
        ])
    print("## Cost per 1,000 reports, held-out (168 case-runs per arm)\n")
    print(table(rows, ["arm", "input tok/case", "output tok/case", "recorded (config rates)",
                       "Price List (ca-central-1)", "cached, warm (est.)", "cached, cold 2 a.m. (est.)"]))

    label, run = SHIPPED
    R = load(run)
    tin, tout = st.mean(r["input_tokens"] for r in R), st.mean(r["output_tokens"] for r in R)
    print(f"\nShipped design, {label}: {per_1000(cost(tin, tout))} per 1,000 reports at Price List rates "
          f"({len(R)} case-runs, recorded {per_1000(st.mean(r['cost_usd'] for r in R))}).")

    # 3: the Nova-only cascade, replayed per (case, pass).
    def key(r: dict) -> tuple:
        return r["id"], r["rep"]

    strict = {key(r): r for r in runs["strict"]}
    agent = {key(r): r for r in runs["agent"]}
    reading = {key(r): r for r in runs["workflow"]}  # one extraction: what the agent's own reading cost
    both = sorted(strict.keys() & agent.keys() & reading.keys())
    tally = collections.Counter()
    spend = 0.0
    for k in both:
        s = strict[k]
        r = agent[k] if s["packet"].get("route") == "judgment" else s
        tally["agent" if r is agent[k] else "strict"] += 1
        sc = scored(r)
        tally["right"] += sc["right"]
        tally["missed"] += sc["missed"]
        tally["late"] += sc["late"]
        # The strict check runs first, always; the agent then reuses its reading, so its own extraction is not paid.
        spend += s["cost_usd"] + (agent[k]["cost_usd"] - reading[k]["cost_usd"] if r is agent[k] else 0)
    rows = []
    for arm in ("strict", "agent"):
        R = [x for x in runs[arm] if key(x) in both]
        rows.append([arm, f"{sum(scored(x)['right'] for x in R)}/{len(R)}", sum(scored(x)["missed"] for x in R),
                     sum(scored(x)["late"] for x in R), per_1000(st.mean(x["cost_usd"] for x in R))])
    rows.append([f"cascade (agent on {tally['agent']}/{len(both)})", f"{tally['right']}/{len(both)}",
                 tally["missed"], tally["late"], per_1000(spend / len(both))])
    print("\n## Nova-only cascade, replayed on held-out (recorded rates)\n")
    print(table(rows, ["arm", "status right", "missed", "late", "cost / 1,000"]))


if __name__ == "__main__":
    main()
