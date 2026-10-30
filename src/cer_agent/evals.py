"""Eval harness, tier 1: deterministic scoring of decision, deadline, route, missing facts and extraction (D3).

Config in evals/config.toml (test set, splits, arm, prices, targets). Each run writes to evals/runs/<run-id>/:
results.jsonl (one line per case, saved after every case so a crash loses nothing), summary.json and summary.md.

Arms:
- workflow-nova: the fixed workflow, Nova Lite through the tagged profile (costs money; printed before it starts);
- oracle: the case's own facts go straight to the rules. $0. Checks the harness and that labels match the rules.

Usage (from code/, src on PYTHONPATH):
    python3 -m cer_agent.evals [--arm oracle] [--splits dev test] [--only ID ...] [--resume RUN_ID]
    python3 -m cer_agent.evals --rescore RUN_ID   # $0: re-map and re-score saved model output with the current code
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import math
import os
import pathlib
import statistics
import sys
import tomllib

from cer_agent.rules import Facts, decide

CODE = pathlib.Path(__file__).resolve().parents[2]
CONFIG = CODE / "evals" / "config.toml"
REPORTABLE = {"reportable", "precautionary"}

# Fields scored for extraction. Fields a judgment point covers are scored as that point instead.
FIELDS = [
    "discovered_at",
    "death",
    "serious_injury",
    "env_effect",
    "fire_or_explosion",
    "fire_linked_to_pipeline",
    "release",
    "substance",
    "volume_m3",
    "volume_estimated",
    "rate_kg_s",
    "rate_estimated",
    "through_pipe_body_or_weld",
    "planned_venting",
    "lands",
    "rupture",
    "toxic_plume",
    "pressure_kpa",
    "limit_kpa",
    "other_beyond_design",
]


def facts_from_json(d: dict) -> Facts:
    """Inverse of cases.facts_json."""
    d = dict(d)
    d["discovered_at"] = dt.datetime.fromisoformat(d["discovered_at"]) if d.get("discovered_at") else None
    d["lands"] = set(d["lands"]) if d.get("lands") is not None else None
    for k in ("open_points", "conflicts"):
        d[k] = {n: [set(v) if isinstance(v, list) else v for v in vals] for n, vals in d.get(k, {}).items()}
    return Facts(**d)


def text_supported(case: dict) -> bool:
    """False when the label rests on a fact the report can't carry (the CER record's own gas-release finding)."""
    f = facts_from_json(case["facts"])
    if f.gas_release_qualifies is None:
        return True
    d = decide(dataclasses.replace(f, gas_release_qualifies=None))
    return (d.status, d.deadline) == (case["expected"]["status"], case["expected"]["deadline"])


# --- Scoring one case ---


def _same(field: str, want, got) -> bool:
    if field == "discovered_at":
        return want is not None and got is not None and want.replace(second=0) == got.replace(second=0)
    if field in ("volume_m3", "rate_kg_s", "pressure_kpa", "limit_kpa"):
        if want is None or got is None:
            return want is None and got is None
        return math.isclose(want, got, rel_tol=0.01, abs_tol=1e-9)
    if field == "substance":
        return (want or "").casefold() == (got or "").casefold()
    if field == "other_beyond_design":
        return bool(want) == bool(got)
    return want == got


def _points(f: Facts) -> dict:
    """Judgment points as comparable values: name -> sorted plausible values."""
    pts = {**f.open_points, **f.conflicts}
    return {k: sorted(repr(sorted(v) if isinstance(v, set) else v) for v in vals) for k, vals in pts.items()}


def score_extraction(want: Facts, got: Facts) -> dict:
    """Per-field match; fields that only matter for a release are skipped when the case has none."""
    out, covered = {}, set(want.open_points) | set(want.conflicts)
    for field in FIELDS:
        if field in covered or (field == "volume_estimated" and (want.volume_m3 is None or "volume_m3" in covered)):
            continue
        if field == "rate_estimated" and (want.rate_kg_s is None or "rate_kg_s" in covered):
            continue
        if field in ("substance", "volume_m3", "volume_estimated", "rate_kg_s", "through_pipe_body_or_weld",
                     "planned_venting", "lands") and not want.release:  # fmt: skip
            continue
        if field == "fire_linked_to_pipeline" and not want.fire_or_explosion:
            continue
        out[field] = _same(field, getattr(want, field), getattr(got, field))
    wp, gp = _points(want), _points(got)
    for name in set(wp) | set(gp):
        out[f"point:{name}"] = wp.get(name) == gp.get(name)
    return out


def score_case(case: dict, packet: dict, got: Facts) -> dict:
    exp = case["expected"]
    want_rep, got_rep = exp["status"] in REPORTABLE, packet["status"] in REPORTABLE
    exp_missing, got_missing = set(exp["missing"]), set(packet["missing"])
    fields = score_extraction(facts_from_json(case["facts"]), got)
    return {
        "status": packet["status"] == exp["status"],
        "missed_report": want_rep and not got_rep,
        "late_deadline": exp["deadline"] == "T3" and packet["deadline"] != "T3",
        "over_notify": (not want_rep) and got_rep,
        "deadline": packet["deadline"] == exp["deadline"],
        "route": packet["route"] == exp["route"],
        "incident_types": sorted(packet["incident_types"]) == sorted(exp["incident_types"]),
        "missing_hit": len(exp_missing & got_missing),
        "missing_expected": len(exp_missing),
        "missing_extra": sorted(got_missing - exp_missing),
        "fields": fields,
        "injection_flagged": bool(packet.get("suspicious_instructions")) if case.get("injection") else None,
    }


# --- Summaries ---


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson interval for k of n."""
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centre - half), min(1.0, centre + half))


def _rate(k: int, n: int) -> dict:
    lo, hi = wilson(k, n)
    return {"k": k, "n": n, "rate": k / n if n else math.nan, "ci95": [lo, hi]}


def summarize(rows: list[dict]) -> dict:
    s = [r["score"] for r in rows]
    nrep = [r for r in rows if r["expected"]["status"] in REPORTABLE]
    nnot = [r for r in rows if r["expected"]["status"] not in REPORTABLE]
    t3 = [r for r in rows if r["expected"]["deadline"] == "T3"]
    field_hits = [v for x in s for v in x["fields"].values()]
    per_field: dict[str, list[bool]] = {}
    for x in s:
        for k, v in x["fields"].items():
            per_field.setdefault(k, []).append(v)
    inj = [x["injection_flagged"] for x in s if x["injection_flagged"] is not None]
    lat = sorted(r["latency_s"] for r in rows)
    return {
        "cases": len(rows),
        "status": _rate(sum(x["status"] for x in s), len(s)),
        "missed_reports": _rate(sum(r["score"]["missed_report"] for r in nrep), len(nrep)),
        "late_deadlines": _rate(sum(r["score"]["late_deadline"] for r in t3), len(t3)),
        "deadline_correct": _rate(sum(x["deadline"] for x in s), len(s)),
        "over_notify": _rate(sum(r["score"]["over_notify"] for r in nnot), len(nnot)),
        "route": _rate(sum(x["route"] for x in s), len(s)),
        "incident_types": _rate(sum(x["incident_types"] for x in s), len(s)),
        "missing_recall": _rate(sum(x["missing_hit"] for x in s), sum(x["missing_expected"] for x in s)),
        "extraction_accuracy": _rate(sum(field_hits), len(field_hits)),
        "per_field": {k: _rate(sum(v), len(v)) for k, v in sorted(per_field.items())},
        "injection_flagged": _rate(sum(inj), len(inj)),
        "cost_usd": sum(r["cost_usd"] for r in rows),
        "cost_per_case_usd": statistics.fmean(r["cost_usd"] for r in rows) if rows else 0.0,
        "latency_p50_s": statistics.median(lat) if lat else 0.0,
        "latency_p95_s": lat[min(len(lat) - 1, math.ceil(0.95 * len(lat)) - 1)] if lat else 0.0,
    }


def breakdown(rows: list[dict], key) -> dict:
    groups: dict[str, list[dict]] = {}
    for r in rows:
        groups.setdefault(str(key(r)), []).append(r)
    return {g: {"cases": len(rs), "status": _rate(sum(r["score"]["status"] for r in rs), len(rs)),
                "deadline": _rate(sum(r["score"]["deadline"] for r in rs), len(rs))}
            for g, rs in sorted(groups.items())}  # fmt: skip


BREAKDOWNS = {
    "kind": lambda r: r["kind"],
    "writer": lambda r: r["writer"],
    "split": lambda r: r["split"],
    "label_source": lambda r: r["label_source"],
    "text_supported": lambda r: r["text_supported"],
}


def check_targets(summary: dict, targets: dict) -> list[dict]:
    out = []
    for name, t in targets.items():
        m = summary.get(name)
        value = m["k"] if name in ("missed_reports", "late_deadlines") else (m["rate"] if isinstance(m, dict) else m)
        ok = value <= t["max"] if "max" in t else value >= t["min"]
        out.append({"target": name, "value": value, "limit": t, "met": ok, "proposed": t.get("proposed", False)})
    return out


def _pct(m: dict) -> str:
    if not m["n"]:
        return "n/a"
    lo, hi = m["ci95"]
    return f"{m['k']}/{m['n']} = {m['rate']:.1%} (95% CI {lo:.0%}–{hi:.0%})"


def render_md(run_id: str, cfg: dict, summary: dict, parts: dict, targets: list[dict], rows: list[dict]) -> str:
    lines = [f"# Eval run {run_id}", "", f"Arm `{cfg['arm']}`, splits {cfg['splits']}, {summary['cases']} cases. "
             f"Cost ${summary['cost_usd']:.4f} (${summary['cost_per_case_usd']:.5f}/case); latency p50 "
             f"{summary['latency_p50_s']:.1f} s, p95 {summary['latency_p95_s']:.1f} s.", "", "## Targets", "",
             "| Target | Value | Limit | Met |", "|---|---|---|---|"]  # fmt: skip
    for t in targets:
        lim = f"≤ {t['limit']['max']}" if "max" in t["limit"] else f"≥ {t['limit']['min']}"
        v = t["value"] if isinstance(t["value"], int) else f"{t['value']:.3f}"
        lines.append(f"| {t['target']}{' [proposed]' if t['proposed'] else ''} | {v} | {lim} | "
                     f"{'yes' if t['met'] else '**no**'} |")  # fmt: skip
    lines += ["", "## Metrics", ""]
    for k in ("status", "missed_reports", "late_deadlines", "deadline_correct", "over_notify", "route",
              "incident_types", "missing_recall", "extraction_accuracy", "injection_flagged"):  # fmt: skip
        lines.append(f"- **{k}**: {_pct(summary[k])}")
    lines += ["", "## Extraction by field", "", "| Field | Correct |", "|---|---|"]
    lines += [f"| {k} | {_pct(m)} |" for k, m in summary["per_field"].items()]
    for name, groups in parts.items():
        lines += ["", f"## By {name}", "", "| Group | Cases | Status | Deadline |", "|---|---|---|---|"]
        lines += [f"| {g} | {v['cases']} | {_pct(v['status'])} | {_pct(v['deadline'])} |" for g, v in groups.items()]
    wrong = [r for r in rows if not (r["score"]["status"] and r["score"]["deadline"] and r["score"]["route"])]
    lines += ["", "## Cases with a wrong status, deadline or route", "",
              "| Case | Kind | Expected | Got | Wrong fields |", "|---|---|---|---|---|"]  # fmt: skip
    for r in wrong:
        e, p = r["expected"], r["packet"]
        bad = ", ".join(k for k, v in r["score"]["fields"].items() if not v)
        lines.append(f"| {r['id']} | {r['kind']} | {e['status']} {e['deadline']} {e['route']} | "
                     f"{p['status']} {p['deadline']} {p['route']} | {bad} |")  # fmt: skip
    return "\n".join(lines) + "\n"


# --- Running ---


def load_config(path: pathlib.Path = CONFIG) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def load_cases(cfg: dict, splits: list[str], only: list[str] | None = None) -> list[dict]:
    lines = (CODE / cfg["run"]["cases"]).read_text(encoding="utf-8").splitlines()
    cases = [json.loads(line) for line in lines]
    return [c for c in cases if (c["id"] in only if only else c["split"] in splits)]


def run_case(case: dict, arm: str, client=None, model: dict | None = None) -> dict:
    from cer_agent.workflow import packet

    if arm == "oracle":
        got = facts_from_json(case["facts"])
        pk, tin, tout, lat = packet(got), 0, 0, 0.0
    else:
        from cer_agent.extract import extract

        received = dt.date.fromisoformat(case["discovered_at"][:10])
        x = extract(client, os.environ[model["env"]], case["report"], received)
        got, pk = x["facts"], packet(x["facts"], x)
        tin, tout, lat = x["input_tokens"], x["output_tokens"], x["latency_s"]
    cost = (tin * model["price_in"] + tout * model["price_out"]) / 1e6 if model else 0.0
    keep = ("id", "kind", "variant", "writer", "split", "label_source", "expected")
    return {**{k: case[k] for k in keep}, "text_supported": text_supported(case), "packet": pk,
            "score": score_case(case, pk, got), "input_tokens": tin, "output_tokens": tout, "cost_usd": cost,
            "latency_s": lat}  # fmt: skip


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run the tier-1 evals.")
    ap.add_argument("--arm", choices=["workflow-nova", "oracle"])
    ap.add_argument("--splits", nargs="*")
    ap.add_argument("--only", nargs="*", help="case IDs (overrides --splits)")
    ap.add_argument("--resume", help="run ID to continue; finished cases are skipped")
    ap.add_argument("--rescore", help="run ID to re-score from its saved model output (no model calls)")
    ap.add_argument("--yes", action="store_true", help="skip the cost confirmation")
    args = ap.parse_args(argv)
    cfg = load_config()
    if args.rescore:
        return rescore(cfg, args.rescore)
    run_cfg = {**cfg["run"], **{k: v for k, v in {"arm": args.arm, "splits": args.splits}.items() if v}}
    cases = load_cases(cfg, run_cfg["splits"], args.only)
    model = cfg["models"]["nova-lite"] if run_cfg["arm"] == "workflow-nova" else None
    client = None
    if model:
        if not os.environ.get(model["env"]):
            print(f"Set {model['env']} (terraform output nova_lite_profile_arn).")
            return 2
        est = len(cases) * (2500 * model["price_in"] + 400 * model["price_out"]) / 1e6
        print(f"{len(cases)} cases on Nova Lite; estimated cost ${est:.3f} (about 2,500 in / 400 out tokens a case).")
        if not args.yes and input("Run? [y/N] ").strip().lower() != "y":
            return 1
        from cer_agent.workflow import make_client

        client = make_client(model["region"])
    run_id = args.resume or f"{dt.datetime.now():%Y%m%d-%H%M%S}-{run_cfg['arm']}-{'-'.join(run_cfg['splits'])}"
    out = CODE / run_cfg["runs_dir"] / run_id
    out.mkdir(parents=True, exist_ok=True)
    results = out / "results.jsonl"
    rows = [json.loads(line) for line in results.read_text().splitlines()] if results.exists() else []
    done = {r["id"] for r in rows}
    with results.open("a", encoding="utf-8") as fh:
        for case in cases:
            if case["id"] in done:
                continue
            r = run_case(case, run_cfg["arm"], client, model)
            fh.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
            fh.flush()  # after every case, so an interruption loses nothing
            rows.append(r)
            ok = "ok" if r["score"]["status"] and r["score"]["deadline"] else "WRONG"
            print(f"{case['id']} {ok:5} {r['packet']['status']} {r['packet']['deadline']} "
                  f"{r['latency_s']:.1f}s ${r['cost_usd']:.5f}", flush=True)  # fmt: skip
    write_summary(cfg, {**run_cfg, "extractor": _extractor_version()}, run_id, out, rows)
    return 0


def _extractor_version() -> str:
    from cer_agent.extract import VERSION

    return VERSION


def rescore(cfg: dict, run_id: str) -> int:
    """Re-map each saved tool input and re-score it, e.g. after a scorer fix. Costs nothing."""
    from cer_agent.extract import to_facts
    from cer_agent.workflow import packet

    out = CODE / cfg["run"]["runs_dir"] / run_id
    cases = {c["id"]: c for c in load_cases(cfg, ["dev", "test", "heldout"])}
    old = [json.loads(line) for line in (out / "results.jsonl").read_text(encoding="utf-8").splitlines()]
    run_cfg = json.loads((out / "summary.json").read_text(encoding="utf-8"))["run"]
    rows = []
    for r in old:
        case, raw = cases[r["id"]], r["packet"].get("extracted")
        if raw is None:  # oracle arm
            rows.append(run_case(case, "oracle"))
            continue
        got = to_facts(raw, dt.date.fromisoformat(case["discovered_at"][:10]))
        pk = packet(got, {"raw": raw})
        rows.append({**r, "text_supported": text_supported(case), "packet": pk, "score": score_case(case, pk, got)})
    (out / "results.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False, default=str) + "\n" for r in rows), encoding="utf-8"
    )
    write_summary(cfg, {**run_cfg, "rescored_with": _extractor_version()}, run_id, out, rows)
    return 0


def write_summary(cfg: dict, run_cfg: dict, run_id: str, out: pathlib.Path, rows: list[dict]) -> None:
    summary = summarize(rows)
    parts = {name: breakdown(rows, key) for name, key in BREAKDOWNS.items()}
    targets = check_targets(summary, cfg["targets"])
    (out / "summary.json").write_text(json.dumps({"run": run_cfg, "summary": summary, "by": parts,
                                                  "targets": targets}, indent=2), encoding="utf-8")  # fmt: skip
    (out / "summary.md").write_text(render_md(run_id, run_cfg, summary, parts, targets, rows), encoding="utf-8")
    print(f"{out}/summary.md: status {_pct(summary['status'])}; missed {summary['missed_reports']['k']}; "
          f"extraction {_pct(summary['extraction_accuracy'])}; cost ${summary['cost_usd']:.4f}")  # fmt: skip


if __name__ == "__main__":
    sys.exit(main())
