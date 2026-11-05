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
import re
import sys
import textwrap
import time
from concurrent.futures import ThreadPoolExecutor

from cer_agent.extract import extract, normalise, to_facts
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


# --- The strictest-of-layouts check (D33) ---
# The same words in another layout: rewrites the normaliser can't undo. Nova's answer moves with layout on about 3-7%
# of inputs (findings log 2026-11-04), so the check reads the report in each layout and treats disagreement as doubt.
LAYOUTS = {
    "noblank": lambda t: re.sub(r"\n\s*\n", "\n", t),  # pasted from a chat or SMS app: blank lines gone
    "wrap72": lambda t: "\n".join(textwrap.fill(ln, 72, break_long_words=False, break_on_hyphens=False) if ln.strip()
                                  else ln for ln in t.split("\n")),  # plain-text email client: hard-wrapped at 72
}  # fmt: skip
DEADLINE_ORDER = {"T3": 0, "T24": 1}


def layouts(report: str) -> dict[str, str]:
    """The report as written, then each layout variant that the normaliser doesn't make identical to one already
    kept (a one-paragraph text message has no blank lines to remove)."""
    out, seen = {"as_written": report}, {normalise(report)}
    for name, fn in LAYOUTS.items():
        text = fn(report)
        if normalise(text) not in seen:
            seen.add(normalise(text))
            out[name] = text
    return out


def _union(lists) -> list:
    return list(dict.fromkeys(x for xs in lists for x in xs))


def combine(packets: dict[str, dict]) -> dict:
    """One decision from the layouts' decisions, taking the stricter side wherever they differ (rules spec "when in
    doubt, notify"):
    - status: the shared status if all agree; if they differ, "precautionary" (citing PREC), since whether it must
      be reported is in doubt;
    - deadline: the earliest any layout set (due_at likewise); none only if the status is "not reportable";
    - route: "judgment" if any layout says so or the layouts disagree (route trigger LAYOUT), so a person sees it;
    - incident types, deadline rules, missing facts, citations: the union.
    The first packet (as written) supplies the extracted facts shown to the reviewer; every layout's extraction and
    answer is kept under `layouts` for the audit trail."""
    ps = list(packets.values())
    statuses = {p["status"] for p in ps}
    answers = {(p["status"], p["deadline"]) for p in ps}
    status = ps[0]["status"] if len(statuses) == 1 else "precautionary"
    deadlines = [p["deadline"] for p in ps if p["deadline"]]
    deadline = min(deadlines, key=DEADLINE_ORDER.get) if deadlines and status != "not reportable" else None
    dues = [p["due_at"] for p in ps if p["due_at"] and p["deadline"] == deadline]
    disagree = len(answers) > 1
    out = {**ps[0], "status": status, "deadline": deadline, "due_at": min(dues) if dues else None,
           "incident_types": _union(p["incident_types"] for p in ps) if status != "not reportable" else [],
           "deadline_rules": _union(p["deadline_rules"] for p in ps if p["deadline"] == deadline),
           "missing": _union(p["missing"] for p in ps),
           "citations": _union([p["citations"] for p in ps] + ([["PREC"]] if len(statuses) > 1 else [])),
           "route": "judgment" if disagree or any(p["route"] == "judgment" for p in ps) else "clear-cut",
           "route_triggers": _union([p["route_triggers"] for p in ps] + ([["LAYOUT"]] if disagree else [])),
           "outcomes_considered": sum(p["outcomes_considered"] for p in ps),
           "layouts": {k: {"status": p["status"], "deadline": p["deadline"], "route": p["route"],
                           "extracted": p.get("extracted")} for k, p in packets.items()}}  # fmt: skip
    if any("suspicious_instructions" in p for p in ps):
        out["suspicious_instructions"] = any(p.get("suspicious_instructions") for p in ps)
    return out


def recombine(layout_raw: dict[str, dict], received: dt.date | None = None) -> dict:
    """Rebuild a strict packet from saved raw extractions (re-scoring, $0)."""
    return combine({k: packet(to_facts(raw, received), {"raw": raw}) for k, raw in layout_raw.items()})


def run_strict(client, model_id: str, report: str, received: dt.date | None = None) -> dict:
    """The strictest-of-layouts workflow: one extraction per layout, in parallel, then `combine`. Latency is wall
    time, so about one call's; tokens and cost are the sum."""
    texts = layouts(report)
    t0 = time.perf_counter()
    with ThreadPoolExecutor(len(texts)) as pool:
        xs = dict(zip(texts, pool.map(lambda t: extract(client, model_id, t, received), texts.values()), strict=True))
    latency = time.perf_counter() - t0
    pk = combine({k: packet(x["facts"], x) for k, x in xs.items()})
    return {
        "packet": pk,
        "facts": xs["as_written"]["facts"],
        "latency_s": latency,
        "calls": len(xs),
        **{k: sum(x.get(k, 0) for x in xs.values()) for k in ("input_tokens", "output_tokens", "retries")},
    }


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
