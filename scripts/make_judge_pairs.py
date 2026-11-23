"""Paired judge fixtures: a quote that is in the report but describes a different incident (reader suggestion on
article 2, 2026-11-23).

Each pair starts from a judge-set draft labelled correct. The two reports carry the same sentences; only which
incident one key sentence describes is swapped:
- "today": the key sentence describes today's incident, a past incident gets the other sentence. The draft is right.
- "past": the key sentence describes a past incident, today's gets the other sentence. The same draft is now wrong.
The draft and the quote the judge would give are identical in both, and `in_report` finds the quote in both, so
only the judge's reading of which incident the words belong to can tell them apart. Labels are the builder's.

Usage (from code/): python3 -I scripts/make_judge_pairs.py   ->  evals/judge/pairs.jsonl
"""

from __future__ import annotations

import json
import pathlib

CODE = pathlib.Path(__file__).resolve().parents[1]
JUDGE_DIR = CODE / "evals" / "judge"

# base: a judge-set draft labelled pass. key: the shared words the draft's PIR-6 statement rests on (every base
# draft states the key fact in PIR-6, its "Specific details" field).
# today/past: the report text, with {key} and {other} filled in; the two differ only in where each sentence goes.
PAIRS = [
    {
        "pair": "P1", "base": "CAL-19", "key": "After power-up, one valve stayed open.",
        "other": "After power-up, the controller lost comms and the station tripped.",
        "report": "Got a gas release at Coulee Creek station near 100 Mile House. Found it at 0830 today.\n\n"
                  "Maintenance crew was swapping a compressor control panel. {today} Sweet gas vented through the "
                  "relief line. Station meter logged 159,600 m³ released, exact number.\n\n"
                  "Same panel failed last month. {past} Tech said comms card was flaky.\n\n"
                  "Shut in the station, isolated the panel. New card on order, should be here tomorrow.",
    },
    {
        "pair": "P2", "base": "CAL-07",
        "key": "Valve was tagged \"closed\" but the handle was about 1/4 turn off seat.",
        "other": "Valve handle was wide open and the tag was missing.",
        "report": "Subject: gas release at Compressor Station 4\n\n"
                  "Just rolled up to Station 4 around 1530 for the quarterly valve grease job. At 1538 I caught a "
                  "sweet gas smell near the suction scrubber skid. Walked the lines, found the 3-inch vent on the "
                  "scrubber discharge was open. {today} No flowmeter on the vent so no number on volume.\n\n"
                  "Same vent was found open on this skid last October. {past}\n\n"
                  "Compressor was running the whole time, no trip. Secured the valve and called it in. Site's "
                  "stable now.\n\n- L. Chen, Field Op",
    },
    {
        "pair": "P3", "base": "CAL-29", "key": "Landed wrong, ended up with a broken femur.",
        "other": "Landed wrong, ended up with a sprained wrist.",
        "report": "Hey,\n\nGot a call from site near Wonowon at around 16:00 today—contractor crew hit a snag. One "
                  "of the guys, name not given yet, took a bad fall off a Cat. {today} They had him on a backboard "
                  "and airlifted to hospital right away. No product release, line's still tight, just the "
                  "injury.\n\nSame crew had a guy fall off a Cat last spring too. {past}\n\n"
                  "Not sure what they were doing exactly—supervisor just said \"construction work\". Will follow up "
                  "if more comes in.\n\n—Raj, Control Room",
    },
    {
        "pair": "P4", "base": "CAL-34",
        "key": "Heat discoloration on the separator shell and some wiring harness melted off the scrubber control "
               "panel.",
        "other": "Only scorch marks on the drip trays.",
        "report": "Got a call from the night shift at Sundre station—fire on east compressor pad around 21:00 May "
                  "26. Crew saw flames, pulled the E-stop, called 911. Local FD showed up, knocked it down quick. "
                  "Looked like the inlet scrubber skid caught. {today} No product hit the fire, everything stayed "
                  "inside pipe. Still running a temp line through the unit to keep downstream pressure up; will "
                  "need to swap the scrubber ASAP.\n\nSame pad had a small fire in 2024 too. {past}\n\n"
                  "—J. Delgado, Area Supervisor",
    },
    {
        "pair": "P5", "base": "CAL-60", "key": "Estimated volume released is about 36,000 m³.",
        "other": "No volume estimate yet.",
        "report": "Got a call from the landowner near Temagami, Ontario, on 2026-07-09 around 18:12. They reported "
                  "a gas release at Northline Gas Transmission Ltd.'s compression station. Patrol team headed there "
                  "to check it out.\n\nUpon arrival, we confirmed a leak. The product released is sweet natural "
                  "gas. {today} The leak appears to be coming from the pipe body or a weld. Everything is contained "
                  "within the station fence.\n\nThis station leaked back in 2022 too. {past}\n\n"
                  "Still investigating the source and cause.\n\nSamantha Lee, Pipeline Patrol Contractor",
    },
    {
        "pair": "P6", "base": "CAL-03",
        "key": "Looks like it's coming through the pipe body or maybe a weld.",
        "other": "Looks like it's coming from a flange on the meter run.",
        "report": "Got a gas leak at Rosetown station, found it at 0940 this morning. Sweet gas, approx. 24,000 m³ "
                  "escaped. {today} Haven't pinpointed it yet.\n\nWe had a leak here in 2023 too. {past}\n\n"
                  "Contained inside the station fence. Shut down the line, venting to flare. Contractor crew's here "
                  "now, starting repairs. Will update when we know more.\n\nDave\nArea Supervisor, Aspen Ridge",
    },
]  # fmt: skip


def build() -> list[dict]:
    base = {d["cal_id"]: d for d in map(json.loads, (JUDGE_DIR / "calibration.jsonl").read_text().splitlines())}
    out = []
    for p in PAIRS:
        b = base[p["base"]]
        for side, (today, past), expected in (("today", (p["key"], p["other"]), "pass"),
                                              ("past", (p["other"], p["key"]), "fail")):  # fmt: skip
            out.append({
                "cal_id": f"{p['pair']}-{side}", "pair": p["pair"], "side": side, "base": p["base"],
                "case_id": b["case_id"], "set": "pairs", "expected": expected,
                "criteria": ["faithful"] if expected == "fail" else [],
                "source": "paired fixture: same draft, key sentence moved between incidents",
                "key": p["key"], "key_field": "PIR-6", "report": p["report"].format(today=today, past=past),
                "packet": b["packet"], "draft": b["draft"],
            })  # fmt: skip
    return out


if __name__ == "__main__":
    rows = build()
    (JUDGE_DIR / "pairs.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"wrote {len(rows)} reports ({len(PAIRS)} pairs) -> evals/judge/pairs.jsonl")
