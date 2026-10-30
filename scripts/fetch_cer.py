"""Fetch the CER pipeline-incident data as a dated, checked snapshot (brief §4, D14, D22).

Usage (from the project root):
    python3 -I code/scripts/fetch_cer.py              # download, check, save a snapshot, print what changed
    python3 -I code/scripts/fetch_cer.py --promote    # ...and make it the current file the other scripts read
    python3 -I code/scripts/fetch_cer.py --offline F  # use a local CSV instead of downloading

What it does:
1. Downloads the incident CSV (and the data dictionary, kept when it changes).
2. Detects the encoding (the file is cp1252, not UTF-8) and parses it.
3. Fails loudly, saving nothing, if a column this project reads is missing or the header differs from the previous
   snapshot. Pass --accept-schema after reviewing a header change.
4. Saves input/cer/pipeline-incidents-YYYY-MM-DD.csv and records its SHA-256, row count, encoding and columns in
   input/cer/manifest.json.
5. Prints the diff against the previous snapshot: new and removed incidents, and which fields changed.
6. Writes input/cer/operator-map.csv, mapping each company name to one operator for analysis. Names are grouped
   automatically (legal suffixes and "as general partner…" clauses removed); merges only a person can decide go in
   input/cer/operator-overrides.json.

The data, the manifest and the operator map live in input/cer/, outside the public repo. Nothing here names a company.
"""

import argparse
import collections
import csv
import datetime as dt
import hashlib
import io
import json
import pathlib
import re
import shutil
import sys
import urllib.request

PROJECT = pathlib.Path(__file__).resolve().parents[2]
CER = PROJECT / "input" / "cer"
CURRENT = CER / "pipeline-incidents-comprehensive-data.csv"
MANIFEST = CER / "manifest.json"
OPERATOR_MAP = CER / "operator-map.csv"
OVERRIDES = CER / "operator-overrides.json"
DICTIONARY_DIR = CER / "data-dictionary"

CSV_URL = "https://www.cer-rec.gc.ca/open/incident/pipeline-incidents-comprehensive-data.csv"
DICTIONARY_URL = "https://www.cer-rec.gc.ca/open/incident/pipeline-incidents-data-dictionary.csv"
KEY = "Incident Number"

# Columns the rules back-test, the companion analysis and the test-set builder read. A rename here breaks them.
REQUIRED = [
    "Incident Number", "Incident Types", "Reported Date", "Nearest Populated Centre", "Province", "Company",
    "Status", "Latitude", "Longitude", "Approximate Volume Released (m3)", "Substance", "Release Type",
    "Significant", "Year", "Occurrence Date and Time", "Discovered Date and Time", "Detailed what happened",
    "What happened category", "Detailed why it happened", "Why it happened category",
    "Activity being performed at time of incident", "How the incident was discovered", "Pipeline or Facility Type",
    "Rupture", "Incident type", "Off Company Property", "Affects Company Property", "Affects Pipeline right-of-way",
    "Affects off Pipeline right-of-way", "Emergency Level", "Number of people evacuated", "Number of fatalities",
    "Number of individuals injured",
]  # fmt: skip

LEGAL_SUFFIX = r"\b(ltd|limited|inc|incorporated|corp|corporation|company|co|lp|l p|gp|partnership|ulc|llc|the)\b"
# Everything after one of these is the legal arrangement, not the operator's name.
CLAUSES = r"\s*,?\s+(as general partner|as agent|carrying on business as|on behalf of)\b.*$"


# --- Pure functions (tested in tests/test_fetch_cer.py) ---


def detect_encoding(data: bytes) -> str:
    """UTF-8 if the bytes decode cleanly (with or without a BOM), otherwise cp1252."""
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return "cp1252"
    return "utf-8-sig" if data.startswith(b"\xef\xbb\xbf") else "utf-8"


def parse(data: bytes, encoding: str) -> tuple[list[str], list[dict]]:
    reader = csv.DictReader(io.StringIO(data.decode(encoding), newline=""))
    rows = list(reader)
    return list(reader.fieldnames or []), rows


def norm(column: str) -> str:
    return re.sub(r"\s+", " ", column).strip().casefold()


def check_schema(header: list[str], previous: list[str] | None, required=REQUIRED) -> list[str]:
    """Errors that should stop the fetch: required columns missing, or columns added/removed since last time."""
    errors = [f"required column missing: {c!r}" for c in required if c not in header]
    if previous is not None:
        errors += [f"column removed or renamed since last snapshot: {c!r}" for c in previous if c not in header]
        errors += [f"new column since last snapshot: {c!r}" for c in header if c not in previous]
    return errors


def dictionary_gaps(header: list[str], dictionary_names: list[str]) -> tuple[list[str], list[str]]:
    """Columns missing from the data dictionary, and dictionary entries with no column (whitespace/case ignored)."""
    h, d = {norm(c) for c in header}, {norm(c) for c in dictionary_names}
    return sorted(h - d), sorted(d - h)


def diff(previous: list[dict], current: list[dict], key: str = KEY) -> dict:
    before = {r[key]: r for r in previous}
    after = {r[key]: r for r in current}
    changed_fields = collections.Counter()
    changed = []
    for k in before.keys() & after.keys():
        fields = [f for f in after[k] if f in before[k] and before[k][f] != after[k][f]]
        if fields:
            changed.append(k)
            changed_fields.update(fields)
    return {
        "new": sorted(after.keys() - before.keys()),
        "removed": sorted(before.keys() - after.keys()),
        "changed": sorted(changed),
        "changed_fields": changed_fields,
    }


def operator_key(name: str) -> str:
    """A grouping key: case, punctuation, legal suffixes and partnership clauses removed."""
    k = re.sub(CLAUSES, "", name, flags=re.IGNORECASE)
    k = k.casefold().replace("&", " and ")
    k = re.sub(r"[^\w\s]", " ", k)
    k = re.sub(LEGAL_SUFFIX, " ", k)
    return re.sub(r"\s+", " ", k).strip()


def build_operator_map(counts: dict[str, int], overrides: dict[str, str]) -> dict[str, tuple[str, str]]:
    """Map each company name to (operator, how). The operator is the group's most frequent name; an override maps a
    group key to another group's key."""
    groups = collections.defaultdict(list)
    for name in counts:
        groups[operator_key(name)].append(name)
    label = {k: max(names, key=lambda n: (counts[n], n)) for k, names in groups.items()}
    result = {}
    for k, names in groups.items():
        target = overrides.get(k, k)
        how = "override" if target != k else ("grouped" if len(names) > 1 else "as-is")
        operator = label.get(target, target)
        for n in names:
            result[n] = (operator, how)
    return result


# --- I/O ---


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "cer-reporting-agent (research; github.com)"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"snapshots": [], "dictionary": None, "current": None}


def bootstrap(manifest: dict) -> None:
    """First run: register the CSV downloaded by hand on 2026-10-28 as the baseline snapshot."""
    if manifest["snapshots"] or not CURRENT.exists():
        return
    data = CURRENT.read_bytes()
    enc = detect_encoding(data)
    header, rows = parse(data, enc)
    file = CER / "pipeline-incidents-2026-10-28.csv"
    shutil.copyfile(CURRENT, file)
    entry = snapshot_entry(file, data, enc, header, rows, CSV_URL, "2026-10-28T00:00:00Z (manual download)")
    manifest["snapshots"].append(entry)
    manifest["current"] = file.name
    print(f"bootstrap: registered {CURRENT.name} as baseline snapshot {file.name} ({len(rows)} rows)")


def snapshot_entry(file, data, enc, header, rows, url, fetched_at) -> dict:
    return {
        "file": file.name,
        "sha256": sha256(data),
        "rows": len(rows),
        "encoding": enc,
        "columns": header,
        "source": url,
        "fetched_at": fetched_at,
    }


def write_operator_map(rows: list[dict]) -> None:
    counts = collections.Counter(r["Company"] for r in rows)
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))["map"] if OVERRIDES.exists() else {}
    known = set()
    if OPERATOR_MAP.exists():
        with OPERATOR_MAP.open(encoding="utf-8", newline="") as f:
            known = {r["company_name"] for r in csv.DictReader(f)}
    mapping = build_operator_map(counts, overrides)
    with OPERATOR_MAP.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["company_name", "operator", "how", "incidents"])
        for name in sorted(mapping, key=lambda n: (mapping[n][0], n)):
            w.writerow([name, *mapping[name], counts[name]])
    operators = len({op for op, _ in mapping.values()})
    print(f"operator map: {len(mapping)} company names -> {operators} operators ({OPERATOR_MAP.name})")
    new_names = sorted(set(mapping) - known) if known else []
    if new_names:
        print(f"  {len(new_names)} company name(s) not seen before: review {OPERATOR_MAP.name}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--promote", action="store_true", help="make this snapshot the current file")
    ap.add_argument("--offline", type=pathlib.Path, help="read this CSV instead of downloading")
    ap.add_argument("--accept-schema", action="store_true", help="save even if the header changed")
    args = ap.parse_args(argv)

    manifest = load_manifest()
    bootstrap(manifest)
    previous = manifest["snapshots"][-1] if manifest["snapshots"] else None

    data = args.offline.read_bytes() if args.offline else download(CSV_URL)
    digest = sha256(data)
    enc = detect_encoding(data)
    header, rows = parse(data, enc)
    print(f"fetched {len(rows)} rows, {len(header)} columns, encoding {enc}, sha256 {digest[:12]}…")

    errors = check_schema(header, previous["columns"] if previous else None)
    if errors and not args.accept_schema:
        print("SCHEMA CHECK FAILED (nothing saved):", *errors, sep="\n  ")
        print("Review the change, update REQUIRED in this script if needed, then re-run with --accept-schema.")
        return 1
    for e in errors:
        print(f"  accepted: {e}")

    if previous and previous["sha256"] == digest:
        print(f"unchanged since {previous['file']}: nothing new to save")
        file = CER / previous["file"]
    else:
        file = CER / f"pipeline-incidents-{dt.date.today().isoformat()}.csv"
        file.write_bytes(data)
        fetched_at = dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        manifest["snapshots"].append(snapshot_entry(file, data, enc, header, rows, CSV_URL, fetched_at))
        print(f"saved {file.name}")
        if previous:
            with (CER / previous["file"]).open(encoding=previous["encoding"], newline="") as f:
                d = diff(list(csv.DictReader(f)), rows)
            print(f"vs {previous['file']}: {len(d['new'])} new, {len(d['removed'])} removed, "
                  f"{len(d['changed'])} changed")  # fmt: skip
            for field, n in d["changed_fields"].most_common(10):
                print(f"  {n:5}  {field}")

    dict_data = None if args.offline else download(DICTIONARY_URL)
    if dict_data is not None:
        known = manifest["dictionary"]
        if not known or known["sha256"] != sha256(dict_data):
            # Reuse an identical copy already on disk rather than saving a duplicate.
            same = [p for p in sorted(DICTIONARY_DIR.glob("*.csv")) if sha256(p.read_bytes()) == sha256(dict_data)]
            path = same[0] if same else DICTIONARY_DIR / f"pipeline-incidents-data-dictionary-{dt.date.today()}.csv"
            if not same:
                path.write_bytes(dict_data)
            manifest["dictionary"] = {"file": str(path.relative_to(CER)), "sha256": sha256(dict_data)}
            print(f"data dictionary {'changed' if known else 'recorded'}: {path.name}")
        names = [r[0] for r in csv.reader(io.StringIO(dict_data.decode(detect_encoding(dict_data)))) if r][1:]
        csv_only, dict_only = dictionary_gaps(header, names)
        print(f"dictionary vs columns: {len(csv_only)} columns not in the dictionary, {len(dict_only)} entries with "
              f"no column (older names; report only)")  # fmt: skip

    write_operator_map(rows)

    if args.promote:
        shutil.copyfile(file, CURRENT)
        manifest["current"] = file.name
        print(f"promoted {file.name} -> {CURRENT.name}; re-run companion_analysis.py to refresh the figures")
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
