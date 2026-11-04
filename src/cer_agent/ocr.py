"""OCR for the rendered documents (D24): Textract plain text detection, cached by the render's SHA-256.

    rendered document -> Textract DetectDocumentText -> lines of text -> the same extraction as a typed report

Only DetectDocumentText: no forms, queries or Bedrock Data Automation, so OCR is the only step that differs from the
text arm. A cached result is reused until its render's bytes change; then that one document is re-run. Eval runs
use the cache committed under evals/renders/ocr/ (the deployed pipeline caches in S3 the same way, keyed by hash).

Usage (from code/, src on PYTHONPATH):
    python3 -m cer_agent.ocr            # OCR every render in the manifest that isn't cached (asks first, states cost)
    python3 -m cer_agent.ocr --check    # list renders missing from the cache, no AWS calls
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import statistics
import sys
import time

CODE = pathlib.Path(__file__).resolve().parents[2]
RENDERS = CODE / "evals" / "renders"
CACHE = RENDERS / "ocr"
REGION = "ca-central-1"
PRICE_PER_PAGE = 0.0015  # DetectDocumentText, first 1M pages a month; check the Textract pricing page before quoting


def manifest() -> dict:
    return json.loads((RENDERS / "manifest.json").read_text(encoding="utf-8"))


def cache_path(sha256: str) -> pathlib.Path:
    return CACHE / f"{sha256[:16]}.json"


def cached(entry: dict) -> dict | None:
    p = cache_path(entry["sha256"])
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def detect_text(client, data: bytes) -> dict:
    """One synchronous DetectDocumentText call (single-page PDF, JPEG or PNG). Lines in Textract's reading order."""
    t0 = time.perf_counter()
    r = client.detect_document_text(Document={"Bytes": data})
    latency = time.perf_counter() - t0
    lines = [b for b in r["Blocks"] if b["BlockType"] == "LINE"]
    return {"text": "\n".join(b["Text"] for b in lines), "pages": r["DocumentMetadata"]["Pages"],
            "lines": len(lines), "mean_confidence": round(statistics.fmean(b["Confidence"] for b in lines), 2)
            if lines else None, "latency_s": round(latency, 3)}  # fmt: skip


def unwrap(text: str, full: float = 0.8) -> str:
    """Rejoin printed lines into paragraphs: a line that ran to near the page width (at least `full` of the longest
    line) was wrapped, so it joins the next; a shorter line ends its paragraph (headings, greetings, signatures).

    Textract returns one line per printed line. Word for word that is the report, but Nova Lite reads hard-wrapped
    text differently (2026-11-04: same words, status 93% as typed vs 83-87% as OCR lines), so the OCR step hands the
    model paragraphs separated by blank lines, as a typed report has."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ""
    width = max(len(ln) for ln in lines)
    out, buf = [], ""
    for ln in lines:
        buf = f"{buf} {ln}" if buf else ln
        if len(ln) < full * width:
            out.append(buf)
            buf = ""
    if buf:
        out.append(buf)
    return "\n\n".join(out)  # paragraphs end in a blank line, as in a typed report


def ocr_text(case_id: str, fmt: str) -> dict:
    """The cached OCR result for one case and format; raises if the render isn't cached or has changed."""
    entry = next(e for e in manifest()["renders"] if e["id"] == case_id and e["format"] == fmt)
    hit = cached(entry)
    if hit is None:
        raise LookupError(f"{entry['file']} has no OCR result for its current bytes; run python3 -m cer_agent.ocr")
    return hit


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="OCR the rendered documents with Textract (cached).")
    ap.add_argument("--check", action="store_true", help="list uncached renders and exit; no AWS calls")
    ap.add_argument("--yes", action="store_true", help="skip the cost confirmation")
    args = ap.parse_args(argv)
    todo = []
    for e in manifest()["renders"]:
        path = RENDERS / e["file"]
        if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() != e["sha256"]:
            print(f"{e['file']}: bytes differ from the manifest; re-run scripts/render_docs.py")
            return 2
        if cached(e) is None:
            todo.append(e)
    print(f"{len(todo)} of {len(manifest()['renders'])} renders not cached; "
          f"estimated Textract cost ${len(todo) * PRICE_PER_PAGE:.3f} (1 page each).")  # fmt: skip
    if args.check or not todo:
        return 0
    if not args.yes and input("Run? [y/N] ").strip().lower() != "y":
        return 1
    import boto3

    client = boto3.client("textract", region_name=REGION)
    CACHE.mkdir(parents=True, exist_ok=True)
    for e in todo:
        r = detect_text(client, (RENDERS / e["file"]).read_bytes())
        out = {"file": e["file"], "sha256": e["sha256"], "api": "DetectDocumentText", "region": REGION,
               "at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"), **r}  # fmt: skip
        cache_path(e["sha256"]).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{e['file']:22} {r['lines']:3} lines, confidence {r['mean_confidence']}, {r['latency_s']:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
