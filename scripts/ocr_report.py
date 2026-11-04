"""Compare the OCR arm with the text arm on the same rendered cases (D24). $0, reads saved runs only.

For each format (text, form, scan, photo): status, deadline, missed and late, extraction accuracy, and the fields
that got worse; plus OCR quality per format (share of the report's words lost or changed, Textract confidence).
The text rows come from text runs that used the same extractor version, restricted to the rendered cases.

Run from code/:  python3 -I scripts/ocr_report.py OCR_RUN_ID [TEXT_RUN_ID ...]
Writes evals/runs/<OCR_RUN_ID>/ocr-comparison.md.
"""

from __future__ import annotations

import collections
import json
import pathlib
import re
import statistics
import sys

CODE = pathlib.Path(__file__).resolve().parents[1]
RUNS = CODE / "evals" / "runs"
RENDERS = CODE / "evals" / "renders"
CASES = CODE / "evals" / "cases" / "cases.jsonl"
TEXT_RUNS = ["20261103-174404-workflow-nova-test", "20261103-173717-workflow-nova-dev"]
FORMATS = ("text", "form", "scan", "photo")


TYPO = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "—": "-", "–": "-"})


def words(s: str) -> list[str]:
    """Lower-case words; curly quotes and dashes folded first, since Textract returns straight ones."""
    s = s.translate(TYPO)
    return re.findall(r"[a-z0-9]+(?:[.:'][a-z0-9]+)*", s.lower())


def lost(ref: str, hyp: str) -> float:
    """Share of the report's words missing or changed in the OCR text: 1 - LCS / len(ref), on words, case and line
    breaks ignored. Extra text (the form's labels) costs nothing, so the formats compare fairly."""
    r, h = words(ref), words(hyp)
    prev = [0] * (len(h) + 1)
    for rw in r:
        cur = [0]
        for j, hw in enumerate(h, 1):
            cur.append(prev[j - 1] + 1 if rw == hw else max(prev[j], cur[j - 1]))
        prev = cur
    return 1 - prev[-1] / max(1, len(r))


def load(run: str) -> tuple[dict, list[dict]]:
    d = RUNS / run
    rows = [json.loads(line) for line in (d / "results.jsonl").read_text(encoding="utf-8").splitlines()]
    return json.loads((d / "summary.json").read_text(encoding="utf-8"))["run"], rows


def metrics(rows: list[dict]) -> dict:
    s = [r["score"] for r in rows]
    fields = collections.defaultdict(list)
    for x in s:
        for k, v in x["fields"].items():
            fields[k].append(v)
    hits = [v for vs in fields.values() for v in vs]
    return {"n": len(rows), "status": sum(x["status"] for x in s) / len(s), "deadline": sum(x["deadline"] for x in s)
            / len(s), "missed": sum(x["missed_report"] for x in s), "late": sum(x["late_deadline"] for x in s),
            "extraction": sum(hits) / len(hits), "fields": {k: sum(v) / len(v) for k, v in fields.items()}}  # fmt: skip


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    ocr_run, text_runs = argv[0], argv[1:] or TEXT_RUNS
    ocr_cfg, ocr_rows = load(ocr_run)
    ids = {r["id"].split("@")[0] for r in ocr_rows}
    by_fmt: dict[str, list[dict]] = collections.defaultdict(list)
    for r in ocr_rows:
        by_fmt[r["render"]].append(r)
    versions = {ocr_cfg.get("extractor")}
    for t in text_runs:
        cfg, rows = load(t)
        versions.add(cfg.get("extractor"))
        by_fmt["text"] += [r for r in rows if r["id"] in ids]
    m = {f: metrics(by_fmt[f]) for f in FORMATS if by_fmt[f]}

    reports = {c["id"]: c["report"] for c in map(json.loads, CASES.read_text(encoding="utf-8").splitlines())}
    manifest = json.loads((RENDERS / "manifest.json").read_text(encoding="utf-8"))
    q: dict[str, list[tuple[float, float]]] = collections.defaultdict(list)
    worst = []
    for e in manifest["renders"]:
        p = RENDERS / "ocr" / f"{e['sha256'][:16]}.json"
        if not p.exists():
            continue
        o = json.loads(p.read_text(encoding="utf-8"))
        w = lost(reports[e["id"]], o["text"])
        q[e["format"]].append((w, o["mean_confidence"] or 0.0))
        worst.append((w, e["file"]))

    lines = [f"# OCR vs. text: {ocr_run}", "",
             f"{len(ids)} cases from dev and test, each rendered as a form PDF, a scan and a photo (D24); text rows "
             f"from {', '.join(text_runs)} on the same cases. Extractor versions: "
             f"{', '.join(sorted(map(str, versions)))}"
             + (" (**differ: not comparable**)" if len(versions) > 1 else "") + ". Every pass pooled.", "",
             "| Format | Results | Status | Deadline | Missed | Late | Extraction | Report words lost | Confidence |",
             "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for f, v in m.items():
        ocr = q.get(f)
        werc = f"{statistics.fmean(w for w, _ in ocr):.1%}" if ocr else "n/a"
        conf = f"{statistics.fmean(c for _, c in ocr):.1f}" if ocr else "n/a"
        lines.append(f"| {f} | {v['n']} | {v['status']:.1%} | {v['deadline']:.1%} | {v['missed']} | {v['late']} | "
                     f"{v['extraction']:.1%} | {werc} | {conf} |")  # fmt: skip
    if "text" in m:
        lines += ["", "## Fields that moved by 3 points or more against text", "",
                  "| Field | Text | " + " | ".join(f for f in FORMATS[1:] if f in m) + " |",
                  "|---|---|" + "---|" * sum(f in m for f in FORMATS[1:])]  # fmt: skip
        for k, base in sorted(m["text"]["fields"].items()):
            vals = [m[f]["fields"].get(k) for f in FORMATS[1:] if f in m]
            if any(v is not None and abs(v - base) >= 0.03 for v in vals):
                lines.append(f"| {k} | {base:.1%} | " + " | ".join("n/a" if v is None else f"{v:.1%}" for v in vals)
                             + " |")  # fmt: skip
    lines += ["", "## Most report words lost", "", "| Render | Words lost |", "|---|---|"]
    lines += [f"| {name} | {w:.1%} |" for w, name in sorted(worst, reverse=True)[:8]]
    wrong = [r for r in ocr_rows if not (r["score"]["status"] and r["score"]["deadline"])]
    lines += ["", f"## OCR results with a wrong status or deadline ({len(wrong)})", "",
              "| Row | Pass | Expected | Got | Wrong fields |", "|---|---|---|---|---|"]  # fmt: skip
    for r in sorted(wrong, key=lambda r: (r["id"], r.get("rep", 1))):
        e, p = r["expected"], r["packet"]
        bad = ", ".join(k for k, v in r["score"]["fields"].items() if not v)
        lines.append(f"| {r['id']} | {r.get('rep', 1)} | {e['status']} {e['deadline']} | {p['status']} "
                     f"{p['deadline']} | {bad} |")  # fmt: skip
    out = RUNS / ocr_run / "ocr-comparison.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:12]))
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
