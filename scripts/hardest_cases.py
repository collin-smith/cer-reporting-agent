"""The 30 hardest cases for article 7's model comparison (D19, D54), from the saved runs ($0, no model calls).

D19 planned "the 30 hardest judgment cases", but 46 of the 57 judgment cases are right in every run since
2026-11-07, while some clear-cut and not-reportable cases fail every time (CL-064, NO-081). So: every case kind,
ranked by how often the Nova Lite arms (workflow, strict, agent, supervisor, MCP, cache) got them wrong in runs from
2026-11-07 on (after the fixes that earlier runs would count against), stability variants left out.

    hardness = (status wrong + deadline wrong + 0.5 x incident types wrong + 2 x missed-or-late) / rows

Selection bias: these cases were picked because Nova got them wrong, so any model re-run on them will look better
than Nova's history (regression to the mean). Compare against Nova Lite re-run on the same cases, the same day.

Usage (from code/):  .venv/bin/python -I scripts/hardest_cases.py   ->  evals/cases/hardest30.json
"""

import collections
import json
import pathlib

CODE = pathlib.Path(__file__).resolve().parents[1]
RUNS = CODE / "evals" / "runs"
OUT = CODE / "evals" / "cases" / "hardest30.json"
SINCE = "20261107"
N = 30


def main() -> None:
    cases = {c["id"]: c for c in map(json.loads, (CODE / "evals/cases/cases.jsonl").open())}
    tally: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for results in sorted(RUNS.glob("*/results.jsonl")):
        if results.parent.name[:8] < SINCE:
            continue
        for line in results.open():
            r = json.loads(line)
            if "perturb" in r or "score" not in r or r["id"] not in cases:
                continue
            s, t = r["score"], tally[r["id"]]
            t["rows"] += 1
            t["status"] += not s["status"]
            t["deadline"] += not s.get("deadline", True)
            t["types"] += not s.get("incident_types", True)
            t["missed_or_late"] += bool(s["missed_report"] or s["late_deadline"])

    def hardness(i: str) -> float:
        t = tally[i]
        return (t["status"] + t["deadline"] + 0.5 * t["types"] + 2 * t["missed_or_late"]) / t["rows"]

    ranked = sorted((i for i in tally if hardness(i) > 0), key=lambda i: (-hardness(i), i))[:N]
    rows = [{"id": i, "kind": cases[i]["kind"], "split": cases[i]["split"], "hardness": round(hardness(i), 3),
             **{k: tally[i][k] for k in ("rows", "status", "deadline", "types", "missed_or_late")}}
            for i in ranked]  # fmt: skip
    OUT.write_text(json.dumps({"rule": __doc__.split("\n\n")[1:3], "since": SINCE, "cases": rows}, indent=1) + "\n")
    print(f"{len(rows)} cases -> {OUT.relative_to(CODE)}; by kind {dict(collections.Counter(r['kind'] for r in rows))}"
          f"; cut at hardness {rows[-1]['hardness']}")  # fmt: skip


if __name__ == "__main__":
    main()
