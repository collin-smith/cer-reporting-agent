"""Does each report actually carry its answer key? $0, no model calls.

The harness scores extraction against each case's spec facts, assuming the writer model put every stated fact into
the text and left every withheld one out. Nothing checked that (findings log 2026-11-02). This script looks for each
stated fact, the discovery time and each withheld fact in the report text with keyword and number matching, and
lists what it can't find. It only flags: a flag is a candidate for review, not a verdict.

Run from code/:  python3 -I scripts/check_key_text.py [--out ../output/key-text-check.md]
"""

# ruff: noqa: E501  (the pattern table reads best one rule per line)
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re

CODE = pathlib.Path(__file__).resolve().parents[1]
SPECS = CODE / "evals" / "cases" / "specs.jsonl"
CASES = CODE / "evals" / "cases" / "cases.jsonl"

# Substance -> words a report would use for it.
SUBSTANCE_WORDS = {
    "natural gas - sweet": r"\bgas\b",
    "natural gas - sour": r"\bsour\b|h2s|h₂s",
    "crude oil - sweet": r"crude|\boil\b",
    "crude oil - synthetic": r"synthetic|syn ?crude|\bsco\b",
    "lube oil": r"lube|lubricat",
    "drilling fluid": r"drilling (fluid|mud)|\bmud\b|bentonite",
    "carbon dioxide": r"co2|co₂|carbon dioxide",
    "diesel fuel": r"diesel",
    "gasoline": r"gasoline|\bgas\b|petrol",
    "amine": r"amine",
    "glycol": r"glycol",
    "sulphur dioxide": r"so2|so₂|sulph?ur dioxide|sulfur dioxide",
}

# Stated-fact template -> pattern(s) that must all appear (case-insensitive).
TEMPLATES = [
    (
        r"everything stayed inside the station fence|spill stayed inside the station fence",
        [r"fence|inside the (station|site|facility)|on[- ]site|within the station"],
    ),
    (r"the leak is through the pipe body / a weld", [r"pipe body|weld|body of the pipe|pipe wall"]),
    (r"^there was a fire", [r"fire|flame|burn|ignit"]),
    (r"product reached the pipeline right of way", [r"right[- ]of[- ]way|\brow\b"]),
    (r"broken leg \(femur\)", [r"femur|leg"]),
    (r"broke a collarbone", [r"collarbone|clavicle"]),
    (r"broke a finger", [r"finger"]),
    (
        r"evacuate or shelter",
        [r"evacuat|shelter|cleared the (immediate )?area|pulled back|moved (everyone|people) (back|away)"],
    ),
    (r"operated outside its design limits", [r"design|\bmop\b|max(imum)?[- ]allowable|rated|beyond|outside"]),
    (
        r"off the right of way onto neighbouring land",
        [r"neighbo|farm|field|landowner|adjacent|off the (right|row)|crop|pasture"],
    ),
    (
        r"visible harm to a creek/wetland",
        [r"creek|wetland|stream|river|water", r"dead|kill|damage|harm|sheen|vegetation"],
    ),
    (r"landowner who phoned it in says there is oil in the road ditch", [r"landowner|farmer|resident", r"ditch"]),
    (
        r"nobody has confirmed which is right|not resolved yet|nobody has confirmed yet",
        [
            r"confirm|not (yet )?(sure|clear|known|resolved|fixed)|unclear|unknown|check|verify|walked|waiting|no resolution|don.t know"
        ],
    ),
    (r"no meter reading yet", [r"meter|metered|measure"]),
    (r"H2S monitor", [r"h2s|h₂s|hydrogen sulph?fide|monitor|detector", r"alarm|went off|beep|trip"]),
    (
        r"drilling mud ran across the right of way to the edge",
        [r"wetland|creek|water", r"silt fence|fence|confirm|sure|check"],
    ),
    (r"line ruptured", [r"ruptur|burst|blew|broke open|failed"]),
    (r"vented on purpose", [r"vent", r"plan|maintenance|on purpose|intentional|scheduled"]),
    (r"grass fire at the station fence line", [r"fire", r"fence"]),
    (r"small sheen on gravel", [r"sheen", r"gravel"]),
    (r"not at our facility", [r"fire"]),
]

NUM = r"(?<![\d.])0*{}(?:\.0+)?(?![\d])"


def _num_present(x: float, text: str) -> bool:
    s = f"{x:g}"
    variants = {s, s.replace(".", ","), f"{x:,.0f}" if x >= 1000 else s, f"{x / 1000:g}k" if x >= 1000 else s}
    if s.startswith("0."):
        variants.add(s[1:])  # ".5"
    return any(re.search(NUM.format(re.escape(v)), text) for v in variants)


def _time_variants(t: dt.datetime) -> list[str]:
    h12 = t.hour % 12 or 12
    ampm = "am" if t.hour < 12 else "pm"
    out = [f"{t:%H:%M}", f"{t:%H%M}", f"{t:%Hh%M}", f"{t.hour}:{t:%M}", f"{h12}:{t:%M}"]  # "4:30" for 16:30 counts
    if t.minute == 0:
        out += [f"{h12} ?{ampm}", f"{h12} ?{ampm[0]}\\.m", f"{h12} o'?clock"]
    if (t.hour, t.minute) == (0, 0):
        out += ["midnight"]
    if (t.hour, t.minute) == (12, 0):
        out += ["noon"]
    return out


def check(spec: dict, report: str) -> list[str]:
    text = report.casefold()
    flags = []
    f = spec["facts"]
    # Discovery time: the clock starts there, so it must be in the text unless deliberately vague.
    if f.get("discovered_at"):
        t = dt.datetime.fromisoformat(f["discovered_at"])
        if not any(re.search(rf"(?<![\d]){v}(?![\d])", text) for v in _time_variants(t)):
            flags.append(f"time: {t:%H:%M} not found")
    for s in spec["stated"]:
        low = s.casefold()
        if low.startswith("the product released is "):
            sub = low.removeprefix("the product released is ")
            pat = SUBSTANCE_WORDS.get(sub)
            if pat and not re.search(pat, text):
                flags.append(f"stated: substance '{sub}' not found")
            continue
        nums = [] if "h2s" in low else [float(n) for n in re.findall(r"\d+(?:\.\d+)?", s.replace(",", ""))]
        missing = [n for n in nums if not _num_present(n, text)]
        if missing:
            flags.append(f"stated: number(s) {', '.join(f'{n:g}' for n in missing)} not found ({s})")
        if ("metered at" in low or "measured at" in low) and not re.search(
            r"meter|measur|gaug|scada|read|record|calculat|totali", text
        ):
            flags.append(f"stated: no sign the figure is measured ({s})")
        if "estimated at about" in low and not re.search(
            r"about|approx|around|roughly|estimat|guess|~|maybe|or so|ish\b|look(s|ed) like", text
        ):
            flags.append(f"stated: no sign the figure is an estimate ({s})")
        for tpl, pats in TEMPLATES:
            if re.search(tpl, s, re.I):
                for p in pats:
                    if not re.search(p, text):
                        flags.append(f"stated: no match for /{p}/ ({s})")
                break
    for w in spec["withheld"]:
        if w == "what product was released":
            sub = (f.get("substance") or "").casefold()
            pat = SUBSTANCE_WORDS.get(sub)
            if pat and re.search(pat, text):
                flags.append(f"withheld: product appears in text (/{pat}/ for '{sub}')")
        elif w == "volume released" and f.get("volume_m3"):
            if _num_present(float(f["volume_m3"]), text):
                flags.append(f"withheld: volume {f['volume_m3']:g} appears in text")
        elif w == "where the product went":
            if re.search(r"fence|right[- ]of[- ]way|\brow\b|neighbo|ditch|off[- ]site|on[- ]site", text):
                flags.append("withheld: a location word appears in text (check it doesn't settle where it went)")
    return flags


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(CODE.parent / "output" / "key-text-check.md"))
    args = ap.parse_args(argv)
    specs = {d["id"]: d for d in map(json.loads, SPECS.read_text(encoding="utf-8").splitlines())}
    cases = {d["id"]: d for d in map(json.loads, CASES.read_text(encoding="utf-8").splitlines())}
    rows = [(cid, specs[cid], check(specs[cid], cases[cid]["report"])) for cid in sorted(cases)]
    flagged = [r for r in rows if r[2]]
    lines = [
        "# Answer key vs. report text",
        "",
        f"Generated {dt.date.today()} by `code/scripts/check_key_text.py` ($0). {len(rows)} cases, "
        f"{len(flagged)} with at least one flag, {sum(len(r[2]) for r in rows)} flags. A flag means the keyword and "
        "number matching couldn't find a stated fact (or found a withheld one); it's a candidate, not a verdict.",
        "",
        "| Case | Split | Variant | Flags |",
        "|---|---|---|---|",
    ]
    for cid, spec, fl in flagged:
        lines.append(f"| {cid} | {spec['split']} | {spec['variant']} | {'<br>'.join(fl)} |")
    pathlib.Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(flagged)}/{len(rows)} cases flagged, {sum(len(r[2]) for r in rows)} flags -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
