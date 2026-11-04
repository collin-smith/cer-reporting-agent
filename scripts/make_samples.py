"""Build the demo's sample cases from the test set (brief §5.6, D8). $0, no model calls.

About 20 cases, each with its report and expected answer, for the public replays and the ✓/✗ badges. Chosen by hand
to cover every kind of case and every operator policy; taken only from the dev and test splits, never held-out, so
publishing results on them doesn't spend the held-out set. Generated from cases.jsonl, so a sample can't drift from
its answer key.

Run from code/:  uv run python -I scripts/make_samples.py
Writes code/evals/cases/samples.json.
"""

from __future__ import annotations

import json
import pathlib

CODE = pathlib.Path(__file__).resolve().parents[1]
CASES = CODE / "evals" / "cases" / "cases.jsonl"
OUT = CODE / "evals" / "cases" / "samples.json"

# Case ID -> (short title, what the case shows). Order is the order the demo lists them.
SAMPLES = {
    "CL-022": ("Worker seriously hurt", "A serious injury on the list sets the 3-hour clock (INC-a, T3-INJURY)."),
    "CL-032": ("Dead fish in a wetland", "Visible harm to a wetland is a significant effect: reportable, 24 hours."),
    "CL-008": ("Fire, people sheltering", "A fire at the facility with people sheltering from smoke: 3 hours."),
    "CL-010": ("Run outside design limits", "Operating outside design limits is reportable on its own (INC-f), 24 h."),
    "CL-018": (
        "Spill, volume unknown",
        "A missing volume can't be assumed small: precautionary, and the follow-up asks.",
    ),
    "CL-030": ("Leak, product not named", "Without the product, the worst plausible case sets the deadline."),
    "CL-007": (
        "Spill, location unknown",
        "Where the product went decides 3 h vs 24 h; missing, so 3 h and a question.",
    ),
    "NO-076": ("Small lube-oil spill", "A metered liquid release under 1.5 m³ is not reportable (OUT-LVP15)."),
    "NO-077": ("Gas weep", "A gas leak under 0.1 kg/s, not through the pipe body, is not reportable."),
    "NO-090": ("Planned venting", "Venting through a working relief valve during maintenance is excluded."),
    "NO-164": ("Broken finger", "A finger fracture alone is not a serious injury (operator policy P3)."),
    "NO-079": (
        "Small sheen, cleaned up",
        "About 0.1 m³ of lube oil with no harm to water or wildlife: not reportable.",
    ),
    "JU-094": ("Mud at a wetland's edge", "Nobody has confirmed any got in: precautionary, judgment (policy P1)."),
    "JU-100": ("Broken collarbone", "A fracture not on the CER's list: precautionary 3 h until a filer advises (P3)."),
    "JU-110": ("Estimate near 1.5 m³", "An estimated 1.6 m³ can fall either side of the line: judgment (P6)."),
    "JU-116": (
        "Gas estimate near 30,000 m³",
        "Reportable either way; only 3 h vs 24 h is open, so not precautionary (X1).",
    ),
    "JU-128": (
        "Inside the fence or in the ditch?",
        "Two accounts disagree on location: reportable, the stricter 3 h (G7).",
    ),
    "JU-139": ("Two volume estimates", "One says under 1.5 m³, one over: whether it's reportable is open (G8)."),
    "JU-143": ("Sweet gas, but an H2S alarm", "An alarm on a sweet line: reportable, 3 h until H2S is ruled out (G9)."),
    "AD-149": ("A fake rule in the report", "The report cites a rule that doesn't exist; the answer ignores it."),
    "AD-157": ("Personal data in the report", "A phone number and SIN in the text; the answer ignores them."),
}

EXPECTED_KEYS = ("status", "deadline", "incident_types", "deadline_rules", "route", "route_triggers", "missing",
                 "citations")  # fmt: skip


def build() -> list[dict]:
    cases = {c["id"]: c for c in map(json.loads, CASES.read_text(encoding="utf-8").splitlines())}
    out = []
    for cid, (title, shows) in SAMPLES.items():
        c = cases[cid]
        if c["split"] == "heldout":
            raise SystemExit(f"{cid} is held out; samples come from dev and test only")
        out.append(
            {
                "id": cid,
                "title": title,
                "shows": shows,
                "kind": c["kind"],
                "variant": c["variant"],
                "split": c["split"],
                "operator": c["operator"],
                "place": f"{c['town']}, {c['province']}",
                "report": c["report"],
                "expected": {k: c["expected"][k] for k in EXPECTED_KEYS},
                "label_source": c["label_source"],
                "rationale": c["rationale"],
            }
        )
    return out


def main() -> int:
    samples = build()
    OUT.write_text(json.dumps(samples, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(samples)} samples to {OUT.relative_to(CODE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
