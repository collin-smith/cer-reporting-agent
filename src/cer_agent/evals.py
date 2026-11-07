"""Eval harness, tier 1: deterministic scoring of decision, deadline, route, missing facts and extraction (D3).

Config in evals/config.toml (test set, splits, arm, prices, targets). Each run writes to evals/runs/<run-id>/:
results.jsonl (one line per case and pass, saved after every case so a crash loses nothing), summary.json and
summary.md.

Repeats: a live arm runs every case `repeats` times (config; --repeats overrides), one full pass after another,
because the model isn't repeatable even at temperature 0. The metrics pool every pass; the spread section gives each
pass's value, and the unstable-cases table lists cases whose answer changed between passes. A target counts as met
only if every pass meets it. The oracle arm is deterministic and always runs once.

Stability: a live arm on typed reports also runs each case as the variants in config `perturb` (same words, other
layout; see workflow.LAYOUTS) in every pass. Their rows (ID `<case>~<variant>`) are kept out of the headline
metrics; the "Stability under formatting" section reports how often the answer flips against the same case in the
same pass.

Arms:
- workflow-nova, workflow-haiku45: the fixed workflow, Nova Lite or Claude Haiku 4.5 through its tagged profile (costs
  money; printed before it starts);
- workflow-nova-ocr: the same workflow on Textract's text of the rendered documents (D24): about 30 dev/test cases,
  each as a form PDF, a scan and a photo, row ID `<case>@<format>`; workflow-nova-ocr-para rejoins the printed
  lines into paragraphs first (ocr.unwrap). Needs the OCR cache (python3 -m cer_agent.ocr);
  compared with workflow-nova on the same cases by scripts/ocr_report.py;
- agent-nova: the single agent (D12, cer_agent.agent): a Strands agent records the facts, checks missing facts
  against the report and can escalate; the rules engine computes the packet from its last reading;
- workflow-nova-strict: the strictest-of-layouts check (D33): each report read as written and in each layout variant,
  decisions combined on the stricter side (workflow.combine); about 3 calls a case, in parallel;
- oracle: the case's own facts go straight to the rules. $0. Checks the harness and that labels match the rules.

Usage (from code/, src on PYTHONPATH):
    python3 -m cer_agent.evals [--arm oracle] [--splits dev test] [--only ID ...] [--repeats N] [--resume RUN_ID]
    python3 -m cer_agent.evals --rescore RUN_ID   # $0: re-map and re-score saved model output with the current code
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as dt
import hashlib
import json
import math
import os
import pathlib
import re
import statistics
import sys
import tomllib

from cer_agent.rules import Facts, decide, substance_class

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
    """Judgment points as comparable values: name -> sorted plausible values.

    A substance point is compared by rule class (SUB-CLASS): "sweet gas or hydrogen sulphide" and "sweet gas or sour
    gas" pose the same question to the rules. The single substance field is still scored by name, since the notice
    names the product."""
    pts = {**f.open_points, **f.conflicts}
    if "substance" in pts:
        pts["substance"] = sorted({substance_class(s) or "" for s in pts["substance"]})
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
    "render": lambda r: r.get("render", "text"),
}


def check_targets(summary: dict, targets: dict) -> list[dict]:
    out = []
    for name, t in targets.items():
        m = summary.get(name)
        value = m["k"] if name in ("missed_reports", "late_deadlines") else (m["rate"] if isinstance(m, dict) else m)
        ok = value <= t["max"] if "max" in t else value >= t["min"]
        out.append({"target": name, "value": value, "limit": t, "met": ok, "proposed": t.get("proposed", False)})
    return out


# --- Repeated passes ---

COUNTS = ("missed_reports", "late_deadlines")  # targets on a count of errors, not a rate
SPREAD = ("status", "deadline_correct", "route", "missed_reports", "late_deadlines", "over_notify",
          "missing_recall", "extraction_accuracy")  # fmt: skip


def _rep(r: dict) -> int:
    return r.get("rep", 1)  # runs from before repeats were added have one pass


def load_rows(results: pathlib.Path) -> list[dict]:
    """A run's saved results, keeping the first row for each case and pass. Two processes once wrote to the same
    run (a run suspended by sleep came back while its resume was going, 2026-11-07); later rows are duplicates."""
    if not results.exists():
        return []
    rows, seen = [], set()
    for line in results.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if (key := (r["id"], _rep(r))) not in seen:
            seen.add(key)
            rows.append(r)
    return rows


@contextlib.contextmanager
def run_lock(out: pathlib.Path):
    """One writer per run. A run that seems dead may only be suspended (WSL stops when Windows sleeps) and come back
    later; a second process resuming it would then call the model twice for the same cases. The lock refuses that.
    After a real crash, delete the .lock file by hand."""
    lock = out / ".lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise SystemExit(f"{out.name} is locked by another process ({lock.read_text().strip()}). If that process is "
                         f"really gone, delete {lock} and resume.") from None  # fmt: skip
    os.write(fd, f"pid {os.getpid()} since {dt.datetime.now():%Y-%m-%d %H:%M:%S}".encode())
    os.close(fd)
    try:
        yield
    finally:
        lock.unlink(missing_ok=True)


def by_pass(rows: list[dict]) -> dict[int, list[dict]]:
    out: dict[int, list[dict]] = {}
    for r in rows:
        out.setdefault(_rep(r), []).append(r)
    return dict(sorted(out.items()))


def _answer(r: dict) -> tuple:
    p = r["packet"]
    return (p["status"], p["deadline"], p["route"])


def spread(rows: list[dict]) -> dict | None:
    """Each pass's headline metrics, and the cases whose answer changed between passes. None for a single pass."""
    passes = by_pass(rows)
    if len(passes) < 2:
        return None
    per = [summarize(rs) for rs in passes.values()]
    metrics = {}
    for m in SPREAD:
        vals = [s[m]["k"] if m in COUNTS else s[m]["rate"] for s in per]
        real = [v for v in vals if not (isinstance(v, float) and math.isnan(v))]
        metrics[m] = {"per_pass": vals, "min": min(real, default=math.nan), "max": max(real, default=math.nan)}
    by_id: dict[str, list[dict]] = {}
    for r in rows:
        by_id.setdefault(r["id"], []).append(r)
    unstable = []
    for cid, rs in sorted(by_id.items()):
        if len({_answer(r) for r in rs}) > 1:
            rs = sorted(rs, key=_rep)
            right = sum(r["score"]["status"] and r["score"]["deadline"] and r["score"]["route"] for r in rs)
            unstable.append({"id": cid, "kind": rs[0]["kind"], "answers": [" ".join(map(str, _answer(r))) for r in rs],
                             "right": right, "passes": len(rs)})  # fmt: skip
    return {"passes": len(passes), "metrics": metrics, "unstable": unstable}


def check_targets_by_pass(rows: list[dict], targets: dict) -> list[dict]:
    """Targets on the pooled metrics, met only if every pass meets them on its own."""
    pooled = check_targets(summarize(rows), targets)
    per = [check_targets(summarize(rs), targets) for rs in by_pass(rows).values()]
    for i, t in enumerate(pooled):
        t["passes_met"] = sum(p[i]["met"] for p in per)
        t["passes"] = len(per)
        t["met"] = t["passes_met"] == len(per)
    return pooled


def _pct(m: dict) -> str:
    if not m["n"]:
        return "n/a"
    lo, hi = m["ci95"]
    return f"{m['k']}/{m['n']} = {m['rate']:.1%} (95% CI {lo:.0%}–{hi:.0%})"


def _num(v) -> str:
    return "n/a" if isinstance(v, float) and math.isnan(v) else (str(v) if isinstance(v, int) else f"{v:.3f}")


def render_stability(st: dict | None, cfg: dict, cost_all: float) -> str:
    if not st:
        return ""
    lines = [
        "",
        "## Stability under formatting",
        "",
        f"Each report also run as {', '.join(f'`{v}`' for v in cfg.get('perturb', []))} (same words, different "
        f"layout); a flip is a different status, deadline or route from the same case in the same pass. "
        f"{cfg.get('perturb_identical', 0)} variants identical after normalising were not run. Cost including "
        f"variants ${cost_all:.4f}.",
        "",
        "| Variant | Flips | Right → wrong | Wrong → right | Missed | Late | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, v in [("all", st["overall"]), *st["by_variant"].items()]:
        lines.append(
            f"| {name} | {_pct(v['flips'])} | {v['right_to_wrong']} | {v['wrong_to_right']} | "
            f"{v['missed_reports']} | {v['late_deadlines']} | {_pct(v['status'])} |"
        )
    lines += ["", f"Cases that flipped at least once: {', '.join(st['flipped_cases']) or 'none'}."]
    return "\n".join(lines) + "\n"


def render_md(run_id: str, cfg: dict, summary: dict, parts: dict, targets: list[dict], rows: list[dict],
              sp: dict | None = None) -> str:  # fmt: skip
    n_pass = sp["passes"] if sp else 1
    n_ids = len({r["id"] for r in rows})
    size = f"{n_ids} cases × {n_pass} passes = {summary['cases']} results" if sp else f"{summary['cases']} cases"
    lines = [f"# Eval run {run_id}", "", f"Arm `{cfg['arm']}`, splits {cfg['splits']}, {size}. "
             f"Cost ${summary['cost_usd']:.4f} (${summary['cost_per_case_usd']:.5f}/case); latency p50 "
             f"{summary['latency_p50_s']:.1f} s, p95 {summary['latency_p95_s']:.1f} s.", ""]  # fmt: skip
    if sp:
        lines += ["Metrics pool every pass. A target is met only if every pass meets it; counts (missed reports, "
                  "late deadlines) are totals across passes.", ""]  # fmt: skip
    lines += ["## Targets", "", "| Target | Value | Limit | Met |" + (" Passes met |" if sp else ""),
              "|---|---|---|---|" + ("---|" if sp else "")]  # fmt: skip
    for t in targets:
        lim = f"≤ {t['limit']['max']}" if "max" in t["limit"] else f"≥ {t['limit']['min']}"
        lines.append(f"| {t['target']}{' [proposed]' if t['proposed'] else ''} | {_num(t['value'])} | {lim} | "
                     f"{'yes' if t['met'] else '**no**'} |"
                     + (f" {t['passes_met']}/{t['passes']} |" if sp else ""))  # fmt: skip
    if sp:
        lines += ["", "## Spread across passes", "",
                  "| Metric | " + " | ".join(f"Pass {i}" for i in range(1, n_pass + 1)) + " | Min | Max |",
                  "|---|" + "---|" * (n_pass + 2)]  # fmt: skip
        for m, v in sp["metrics"].items():
            cells = " | ".join(_num(x) for x in v["per_pass"])
            lines.append(f"| {m} | {cells} | {_num(v['min'])} | {_num(v['max'])} |")
        lines += ["", f"## Unstable cases ({len(sp['unstable'])}): the answer changed between passes", ""]
        if sp["unstable"]:
            lines += ["| Case | Kind | Answer per pass (status, deadline, route) | Right |", "|---|---|---|---|"]
            lines += [f"| {u['id']} | {u['kind']} | {' / '.join(u['answers'])} | {u['right']}/{u['passes']} |"
                      for u in sp["unstable"]]  # fmt: skip
        else:
            lines.append("None.")
    lines += ["", "## Metrics", ""]
    for k in ("status", "missed_reports", "late_deadlines", "deadline_correct", "over_notify", "route",
              "incident_types", "missing_recall", "extraction_accuracy", "injection_flagged"):  # fmt: skip
        lines.append(f"- **{k}**: {_pct(summary[k])}")
    lines += ["", "## Extraction by field", "", "| Field | Correct |", "|---|---|"]
    lines += [f"| {k} | {_pct(m)} |" for k, m in summary["per_field"].items()]
    for name, groups in parts.items():
        lines += ["", f"## By {name}", "", "| Group | Cases | Status | Deadline |", "|---|---|---|---|"]
        lines += [f"| {g} | {v['cases']} | {_pct(v['status'])} | {_pct(v['deadline'])} |" for g, v in groups.items()]
    wrong: dict[str, list[dict]] = {}
    for r in rows:
        if not (r["score"]["status"] and r["score"]["deadline"] and r["score"]["route"]):
            wrong.setdefault(r["id"], []).append(r)
    lines += ["", "## Cases with a wrong status, deadline or route", "",
              "| Case | Kind | Expected | Got | Wrong fields |" + (" Passes wrong |" if sp else ""),
              "|---|---|---|---|---|" + ("---|" if sp else "")]  # fmt: skip
    for cid, rs in wrong.items():
        r = rs[0]  # the first wrong pass
        e, p = r["expected"], r["packet"]
        bad = ", ".join(k for k, v in r["score"]["fields"].items() if not v)
        lines.append(f"| {cid} | {r['kind']} | {e['status']} {e['deadline']} {e['route']} | "
                     f"{p['status']} {p['deadline']} {p['route']} | {bad} |"
                     + (f" {len(rs)}/{n_pass} |" if sp else ""))  # fmt: skip
    return "\n".join(lines) + "\n"


# --- Running ---


def load_config(path: pathlib.Path = CONFIG) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def load_cases(cfg: dict, splits: list[str], only: list[str] | None = None) -> list[dict]:
    lines = (CODE / cfg["run"]["cases"]).read_text(encoding="utf-8").splitlines()
    cases = [json.loads(line) for line in lines]
    return [c for c in cases if (c["id"] in only if only else c["split"] in splits)]


def case_id(row_id: str) -> str:
    """The answer-key ID of a result row: an OCR row is `<case>@<format>`, a stability row `<case>~<variant>`."""
    return re.split(r"[@~]", row_id)[0]


# --- Stability under formatting (findings log 2026-11-04) ---
# Meaning-preserving rewrites of a report that the input normaliser can't undo. Each live pass runs every case as
# written and as each variant; a flip is a variant whose (status, deadline, route) differs from the same case's answer
# in the same pass. Variant rows never enter the headline metrics.
def _perturb() -> dict:
    from cer_agent.workflow import LAYOUTS  # the same variants the strict arm reads (D33)

    return LAYOUTS


def perturbed_cases(cases: list[dict], variants: list[str]) -> tuple[list[dict], int]:
    """Each case followed by its variants. A variant the normaliser makes identical to the original is left out (it
    can't flip: the model sees the same bytes); the count of those is returned."""
    from cer_agent.extract import normalise

    out, same = [], 0
    for c in cases:
        out.append(c)
        for v in variants:
            text = _perturb()[v](c["report"])
            if normalise(text) == normalise(c["report"]):
                same += 1
                continue
            out.append({**c, "id": f"{c['id']}~{v}", "perturb": v, "report": text})
    return out, same


def stability(rows: list[dict]) -> dict | None:
    """Flip rate per variant and overall, against the same case's answer in the same pass. None without variants."""
    base = {(r["id"], _rep(r)): r for r in rows if not r.get("perturb")}
    per: dict[str, list[tuple[dict, dict]]] = {}
    for r in rows:
        b = base.get((case_id(r["id"]), _rep(r))) if r.get("perturb") else None
        if b:
            per.setdefault(r["perturb"], []).append((b, r))
    if not per:
        return None

    def stats(pairs: list[tuple[dict, dict]]) -> dict:
        flips = [(b, r) for b, r in pairs if _answer(b) != _answer(r)]
        right = lambda x: x["score"]["status"] and x["score"]["deadline"] and x["score"]["route"]  # noqa: E731
        return {"flips": _rate(len(flips), len(pairs)),
                "right_to_wrong": sum(right(b) and not right(r) for b, r in flips),
                "wrong_to_right": sum(not right(b) and right(r) for b, r in flips),
                "missed_reports": sum(r["score"]["missed_report"] for _, r in pairs),
                "late_deadlines": sum(r["score"]["late_deadline"] for _, r in pairs),
                "status": _rate(sum(r["score"]["status"] for _, r in pairs), len(pairs))}  # fmt: skip

    flipped = sorted({case_id(r["id"]) for pairs in per.values() for b, r in pairs if _answer(b) != _answer(r)})
    return {"overall": stats([p for pairs in per.values() for p in pairs]),
            "by_variant": {v: stats(pairs) for v, pairs in sorted(per.items())}, "flipped_cases": flipped}  # fmt: skip


def ocr_cases(cfg: dict, only: list[str] | None = None, paragraphs: bool = False) -> list[dict]:
    """One case per rendered document, its report replaced by the cached OCR text. Fails if a report changed since
    it was rendered, or a render has no OCR result, rather than scoring stale text. `paragraphs` rejoins the
    printed lines first (ocr.unwrap)."""
    from cer_agent.ocr import manifest, ocr_text, unwrap

    by_id = {c["id"]: c for c in load_cases(cfg, ["dev", "test", "heldout"])}
    out = []
    for e in manifest()["renders"]:
        if only and e["id"] not in only:
            continue
        case = by_id[e["id"]]
        if hashlib.sha256(case["report"].encode()).hexdigest() != e["report_sha256"]:
            raise ValueError(f"{e['id']}: report changed since it was rendered; re-run scripts/render_docs.py")
        out.append({**case, "id": f"{e['id']}@{e['format']}", "render": e["format"],
                    "report": (unwrap if paragraphs else str)(ocr_text(e["id"], e["format"])["text"])})  # fmt: skip
    return out


def run_case(case: dict, arm: str, client=None, model: dict | None = None) -> dict:
    from cer_agent.workflow import packet

    retries = 0
    if arm == "oracle":
        got = facts_from_json(case["facts"])
        pk, tin, tout, lat = packet(got), 0, 0, 0.0
    elif arm.startswith("agent-"):
        from cer_agent.agent import run as run_agent

        received = dt.date.fromisoformat(case["discovered_at"][:10])
        x = run_agent(os.environ[model["env"]], case["report"], received, model.get("region", "ca-central-1"))
        got, pk = x["facts"], x["packet"]
        tin, tout, lat, retries = x["input_tokens"], x["output_tokens"], x["latency_s"], x["retries"]
    elif arm.endswith("-strict"):
        from cer_agent.workflow import run_strict

        received = dt.date.fromisoformat(case["discovered_at"][:10])
        x = run_strict(client, os.environ[model["env"]], case["report"], received)
        got, pk = x["facts"], x["packet"]
        tin, tout, lat = x["input_tokens"], x["output_tokens"], x["latency_s"]
    else:
        from cer_agent.extract import extract

        received = dt.date.fromisoformat(case["discovered_at"][:10])
        x = extract(client, os.environ[model["env"]], case["report"], received)
        got, pk = x["facts"], packet(x["facts"], x)
        tin, tout, lat = x["input_tokens"], x["output_tokens"], x["latency_s"]
        retries = x.get("retries", 0)
    cost = (tin * model["price_in"] + tout * model["price_out"]) / 1e6 if model else 0.0
    keep = ("id", "kind", "variant", "writer", "split", "label_source", "expected")
    return {**{k: case[k] for k in keep}, **({"perturb": case["perturb"]} if "perturb" in case else {}),
            "render": case.get("render", "text"), "text_supported": text_supported(case),
            "packet": pk,
            "score": score_case(case, pk, got), "input_tokens": tin, "output_tokens": tout, "cost_usd": cost,
            "latency_s": lat, "retries": retries}  # fmt: skip


# Live arm -> model key in config.toml [models.*]. Same fixed workflow; only the extractor model changes.
ARMS = {
    "workflow-nova": "nova-lite",
    "workflow-haiku45": "haiku-45",
    "workflow-nova-ocr": "nova-lite",
    "workflow-nova-ocr-para": "nova-lite",
    "workflow-nova-strict": "nova-lite",
    "agent-nova": "nova-lite",  # the single agent (D12): Strands, facts only; the rules engine decides
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run the tier-1 evals.")
    ap.add_argument("--arm", choices=[*ARMS, "oracle"])
    ap.add_argument("--splits", nargs="*")
    ap.add_argument("--only", nargs="*", help="case IDs (overrides --splits)")
    ap.add_argument("--repeats", type=int, help="passes over the cases (live arm; default from config)")
    ap.add_argument("--resume", help="run ID to continue; finished cases are skipped")
    ap.add_argument("--rescore", help="run ID to re-score from its saved model output (no model calls)")
    ap.add_argument("--no-perturb", action="store_true", help="skip the stability variants (config run.perturb)")
    ap.add_argument("--yes", action="store_true", help="skip the cost confirmation")
    args = ap.parse_args(argv)
    cfg = load_config()
    if args.rescore:
        return rescore(cfg, args.rescore)
    run_cfg = {**cfg["run"], **{k: v for k, v in {"arm": args.arm, "splits": args.splits}.items() if v}}
    if "-ocr" in run_cfg["arm"]:
        cases = ocr_cases(cfg, args.only, paragraphs=run_cfg["arm"].endswith("-para"))
        run_cfg["splits"] = sorted({c["split"] for c in cases})
    else:
        cases = load_cases(cfg, run_cfg["splits"], args.only)
    model_key = ARMS.get(run_cfg["arm"])
    model = cfg["models"][model_key] if model_key else None
    repeats = run_cfg["repeats"] = (args.repeats or run_cfg.get("repeats", 1)) if model else 1
    # No stability variants on the OCR arms (their input is fixed) or the strict arm (it already reads every layout).
    skip = args.no_perturb or not model or "-ocr" in run_cfg["arm"] or run_cfg["arm"].endswith("-strict")
    variants = [] if skip else run_cfg.get("perturb", [])
    run_cfg["perturb"] = variants
    if variants:
        n_base = len(cases)
        cases, run_cfg["perturb_identical"] = perturbed_cases(cases, variants)
        print(f"Stability variants {variants}: {len(cases) - n_base} extra inputs; "
              f"{run_cfg['perturb_identical']} left out (identical after normalising).")  # fmt: skip
    client = None
    if model:
        if not os.environ.get(model["env"]):
            print(f"Set {model['env']} (the model's tagged profile ARN; terraform output).")
            return 2
        est = (
            (3 if run_cfg["arm"].endswith("-strict") else 1)
            * repeats
            * len(cases)
            * (2500 * model["price_in"] + 400 * model["price_out"])
            / 1e6
        )
        print(f"{len(cases)} cases × {repeats} passes on {model_key}; estimated cost ${est:.3f} "
              f"(about 2,500 in / 400 out tokens a case).")  # fmt: skip
        if not args.yes and input("Run? [y/N] ").strip().lower() != "y":
            return 1
        from cer_agent.workflow import make_client

        client = make_client(model["region"])
    run_id = args.resume or f"{dt.datetime.now():%Y%m%d-%H%M%S}-{run_cfg['arm']}-{'-'.join(run_cfg['splits'])}"
    out = CODE / run_cfg["runs_dir"] / run_id
    out.mkdir(parents=True, exist_ok=True)
    results = out / "results.jsonl"
    with run_lock(out), results.open("a", encoding="utf-8") as fh:
        rows = load_rows(results)
        done = {(r["id"], _rep(r)) for r in rows}
        for rep in range(1, repeats + 1):  # one full pass after another, so an interruption leaves whole passes
            for case in cases:
                if (case["id"], rep) in done:
                    continue
                r = {**run_case(case, run_cfg["arm"], client, model), "rep": rep}
                fh.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
                fh.flush()  # after every case, so an interruption loses nothing
                rows.append(r)
                ok = "ok" if r["score"]["status"] and r["score"]["deadline"] else "WRONG"
                print(f"pass {rep} {case['id']} {ok:5} {r['packet']['status']} {r['packet']['deadline']} "
                      f"{r['latency_s']:.1f}s ${r['cost_usd']:.5f}", flush=True)  # fmt: skip
    write_summary(cfg, {**run_cfg, "extractor": _extractor_version()}, run_id, out, rows)
    return 0


def _extractor_version() -> str:
    from cer_agent.extract import VERSION

    return VERSION


def rescore_row(r: dict, cases: dict) -> dict:
    """One saved row re-mapped and re-scored with the current code, from its saved model output. No model calls."""
    from cer_agent.extract import to_facts
    from cer_agent.workflow import packet

    case, raw = cases[case_id(r["id"])], r["packet"].get("extracted")
    if raw is None:  # oracle arm
        return {**run_case(case, "oracle"), "rep": _rep(r)}
    received = dt.date.fromisoformat(case["discovered_at"][:10])
    got = to_facts(raw, received)
    if "layouts" in r["packet"]:  # strict arm: rebuild every layout's decision and combine again
        from cer_agent.workflow import recombine

        pk = recombine({k: v["extracted"] for k, v in r["packet"]["layouts"].items()}, received)
    else:
        pk = packet(got, {"raw": raw})
        if agent := r["packet"].get("agent"):  # agent arm: keep its trace, and a held suggestion still routes
            pk["agent"] = agent  # to a person (D38)
            if agent.get("held"):
                pk["route"], pk["route_triggers"] = "judgment", [*pk["route_triggers"], "AGENT-HOLD"]
    return {**r, "text_supported": text_supported(case), "packet": pk, "score": score_case(case, pk, got)}


def rescore(cfg: dict, run_id: str) -> int:
    """Re-map each saved tool input and re-score it, e.g. after a scorer fix. Costs nothing."""
    out = CODE / cfg["run"]["runs_dir"] / run_id
    cases = {c["id"]: c for c in load_cases(cfg, ["dev", "test", "heldout"])}
    run_cfg = json.loads((out / "summary.json").read_text(encoding="utf-8"))["run"]
    rows = [rescore_row(r, cases) for r in load_rows(out / "results.jsonl")]
    (out / "results.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False, default=str) + "\n" for r in rows), encoding="utf-8"
    )
    write_summary(cfg, {**run_cfg, "rescored_with": _extractor_version()}, run_id, out, rows)
    return 0


def write_summary(cfg: dict, run_cfg: dict, run_id: str, out: pathlib.Path, rows: list[dict]) -> None:
    st = stability(rows)
    cost_all = sum(r["cost_usd"] for r in rows)
    rows = [r for r in rows if not r.get("perturb")]  # headline metrics: reports as written only
    summary = summarize(rows)
    summary["cost_with_stability_usd"] = cost_all
    parts = {name: breakdown(rows, key) for name, key in BREAKDOWNS.items()}
    targets = check_targets_by_pass(rows, cfg["targets"])
    sp = spread(rows)
    (out / "summary.json").write_text(json.dumps({"run": run_cfg, "summary": summary, "spread": sp, "by": parts,
                                                  "targets": targets, "stability": st}, indent=2),
                                      encoding="utf-8")  # fmt: skip
    md = render_md(run_id, run_cfg, summary, parts, targets, rows, sp) + render_stability(st, run_cfg, cost_all)
    (out / "summary.md").write_text(md, encoding="utf-8")
    extra = ""
    if sp:
        st = sp["metrics"]["status"]
        extra = f"; status range {st['min']:.1%}–{st['max']:.1%} over {sp['passes']} passes, " \
                f"{len(sp['unstable'])} unstable"  # fmt: skip
    print(f"{out}/summary.md: status {_pct(summary['status'])}; missed {summary['missed_reports']['k']}; "
          f"extraction {_pct(summary['extraction_accuracy'])}; cost ${summary['cost_usd']:.4f}{extra}")  # fmt: skip


if __name__ == "__main__":
    sys.exit(main())
