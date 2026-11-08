"""Write each case spec up as a messy field report, then check it (D27).

The writer model only turns a spec into prose: it gets the facts to state and the facts to leave out, never the
expected answer. A deterministic checker rejects a report that drops a stated number, mentions a withheld fact or
talks about reporting rules; a rejected report is regenerated (up to 3 tries).

Usage (from the project root, code/src on PYTHONPATH):
    WRITER_LLAMA_ARN=... WRITER_MISTRAL_ARN=... python3 -m cer_agent.writer [--only ID ...] [--limit N]
The ARNs are the tagged inference profiles (terraform output writer_profile_arns). Writes code/evals/cases/cases.jsonl
and prints tokens and cost.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
import time

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

PROJECT = pathlib.Path(__file__).resolve().parents[3]
CASES_DIR = PROJECT / "code" / "evals" / "cases"
SPECS, CASES = CASES_DIR / "specs.jsonl", CASES_DIR / "cases.jsonl"
REGION = "us-east-1"
MAX_TRIES = 3
# USD per 1M tokens (input, output), AWS Price List, us-east-1, 2026-10-29.
PRICES = {"llama": (0.24, 0.97), "mistral": (0.50, 1.50)}

SYSTEM = """You write realistic field reports that pipeline field staff send to their company's compliance team.
Write like a busy person in the field: plain words, short sentences, some abbreviations, a little disorganized.
Never sound like a formal incident report ("upon further inspection", "the product released was", subject lines in
title case). Texts are terse; emails and call notes are a few loose paragraphs.
Rules:
- State every fact in the FACTS list, including the time it was found, written as a clock time. Where two facts
  disagree, report both as given and don't settle which is right. Keep every number and unit exactly as given (you
  may say "approx." or "about" where the fact says estimated).
- Do not mention anything in the LEAVE OUT list, not even vaguely, and do not add facts that aren't given: no extra
  volumes, injuries, damage, causes or locations. Don't speculate about causes, blame, or anyone's conduct or
  condition.
- Use only the town and province given; no coordinates, street addresses or real company names other than the
  operator given.
- Don't mention regulators, reporting rules, deadlines or whether this must be reported. Just describe what happened.
- 80 to 220 words. No headings, no bullet lists of facts, no sign-off longer than a name and role.
Output only the report text."""


def prompt(spec: dict) -> str:
    c = spec["context"]
    leave_out = spec["withheld"] or ["(nothing)"]
    return "\n".join(
        [
            f"OPERATOR: {spec['operator']}",
            f"PLACE: near {spec['town']}, {spec['province']}",
            f"WRITTEN AS: {spec['style']}, by a {spec['reporter']}",
            f"BACKGROUND (use loosely, in your own words): {c['what_happened']}; {c['detail']}; "
            f"equipment: {c['equipment'] or 'not specified'}; activity: {c['activity']}; "
            f"found by: {c['how_discovered'] or 'not specified'}",
            "FACTS:",
            f"- {found_at(spec)}",
            *[f"- {p}" for p in spec["stated"]],
            "LEAVE OUT:",
            *[f"- {w}" for w in leave_out],
        ]
    )


def found_at(spec: dict) -> str:
    """The discovery time as a fact to state (K1, D29). As context only, the writers paraphrased or dropped it."""
    t = dt.datetime.fromisoformat(spec["discovered_at"])
    return f"found at {t:%H:%M} on {t:%B} {t.day}"


# --- Checks ---


def time_variants(t: dt.datetime) -> list[str]:
    """Ways a report can write a clock time: 16:15, 1615, 16h15, 4:15 (with or without pm); 4 pm on the hour."""
    h12 = t.hour % 12 or 12
    ampm = "am" if t.hour < 12 else "pm"
    out = [f"{t:%H:%M}", f"{t:%H%M}", f"{t:%Hh%M}", f"{t.hour}:{t:%M}", f"{h12}:{t:%M}"]
    if t.minute == 0:
        out += [f"{h12} ?{ampm}", f"{h12} ?{ampm[0]}\\.m", f"{h12} o'?clock"]
    if (t.hour, t.minute) == (0, 0):
        out += ["midnight"]
    if (t.hour, t.minute) == (12, 0):
        out += ["noon"]
    return out


def has_time(t: dt.datetime, text: str) -> bool:
    return any(re.search(rf"(?<![\d]){v}(?![\d])", text.casefold()) for v in time_variants(t))


NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")
VOLUME = re.compile(r"\d[\d,.]*\s*(?:m3|m³|cubic|litres?|liters?|bbls?|barrels?|L\b)", re.IGNORECASE)
# A figure with a deciding unit must come from the spec: an invented pressure or volume can change the answer.
QUANTITY = re.compile(
    r"(\d[\d,]*(?:\.\d+)?)\s*(?:m3|m³|cubic|litres?|liters?|bbls?|barrels?|L\b|kpa|mpa|psi|bar\b|kg/[smh])",
    re.IGNORECASE,
)
LAND_WORDS = ("fence", "right of way", "right-of-way", "ditch", "off site", "off-site", "neighbour", "neighbor",
              "landowner", "road", "berm", "dike", "dyke", "containment", "contained")  # fmt: skip
PRODUCT_WORDS = ("crude", "oil", "condensate", "propane", "butane", "diesel", "gasoline", "gas", "ngl", "liquids",
                 "water", "h2s", "sour", "sweet")  # fmt: skip
# Speculation about people: the writer must not invent conduct, impairment or blame.
CONDUCT_WORDS = ("drink", "drinking", "drunk", "alcohol", "impaired", "distracted", "careless", "fault", "blame",
                 "negligen", "horseplay")  # fmt: skip
RULE_WORDS = ("cer", "regulator", "reportable", "deadline")  # "notified the control room" is fine


# A case with no release must not read as one (K6–K8, D30). A hint counts unless a negation comes just before it.
RELEASE_HINT = re.compile(
    r"\b(leak\w*|sheen|spill\w*|hiss\w*|gas pocket|seep\w*|spray\w*|puddl\w*|vent(?:ed|ing))\b", re.I
)
NEGATION = re.compile(r"\b(no|nothing|not|never|without|none)\b|n't\b|n’t\b", re.I)
UNKNOWN_FIRE = re.compile(
    r"what(?:'s|’s| is| was) burning|(not sure|don.t know|didn.t know|no idea|unknown|unclear)[^.]{0,40}\b(burn|fuel)",
    re.I,
)

# A fire at our facility must not read as someone else's (D30).
UNLINKED_FIRE = re.compile(
    r"\b(wasn.t|was not|weren.t|not) (affected|involved|hit|damaged|ours)\b"
    r"|near (our|the) (pipeline|line|row|right[- ]of[- ]way)|beside the line|not from (it|our)"
    r"|off (our|the) (site|row|right[- ]of[- ]way)",
    re.I,
)


# A report whose spec has no beyond-design condition must not state one (NO-164, NO-163, JU-092, JU-096; D45): an
# exposed pipe or a part out of spec is reportable in itself. A washout as a cause, or a relief valve that lifted, is
# fine.
UNSTATED_BEYOND = re.compile(
    r"\bpipe\w*\W+(?:\w+\W+){0,5}?exposed\b|\bexposed (?:pipe|section|line)\b|\bout of spec\b|\bover spec\b"
    r"|\b(?:higher|lower|more|less) than spec\b|\b(?:beyond|outside(?: of)?|above|past) (?:its |the )?design\b"
    r"|\bdesign limits?\b",
    re.I,
)


def beyond_design_in_spec(facts: dict) -> bool:
    return bool(facts.get("other_beyond_design") or (facts.get("pressure_kpa") and facts.get("limit_kpa"))
                or facts.get("temperature_c"))  # fmt: skip


def release_hints(text: str) -> list[str]:
    """Release words in the text that aren't negated ("no leaks" is fine, "a small sheen" isn't)."""
    return [
        m.group(0) for m in RELEASE_HINT.finditer(text) if not NEGATION.search(text[max(0, m.start() - 25) : m.start()])
    ]


def numbers_in(text: str) -> set[str]:
    return {n.replace(",", "").rstrip(".") for n in NUMBER.findall(text)}


def check(spec: dict, report: str) -> list[str]:
    """Problems with a report; empty means accepted."""
    problems = []
    text = report.lower()
    # The key's discovery time (facts), which can differ from the prompt's by a ruling (cases.KEY_RULINGS).
    found = (spec.get("facts") or {}).get("discovered_at") or spec.get("discovered_at")
    if found and not has_time(t := dt.datetime.fromisoformat(found), report):
        problems.append(f"missing the time it was found ({t:%H:%M})")
    have = numbers_in(report)
    for phrase in spec["stated"]:
        for n in numbers_in(phrase):
            variants = {n, n.rstrip("0").rstrip(".") if "." in n else n}
            if not variants & have:
                problems.append(f"missing number {n} (from: {phrase})")
    given = {n for phrase in spec["stated"] for n in numbers_in(phrase)}
    given |= {n.rstrip("0").rstrip(".") for n in given if "." in n}
    for q in QUANTITY.findall(report):
        n = q.replace(",", "").rstrip(".")
        if n not in given and n.rstrip("0").rstrip(".") not in given:
            problems.append(f"adds a figure not in the spec: {q}")
    withheld = " ".join(spec["withheld"])
    if "volume" in withheld and VOLUME.search(report):
        problems.append("mentions a volume, which is withheld")
    if "where the product went" in withheld and any(w in text for w in LAND_WORDS):
        problems.append("mentions where the product went, which is withheld")
    if "what product" in withheld and any(re.search(rf"\b{w}\b", text) for w in PRODUCT_WORDS):
        problems.append("names the product, which is withheld")
    facts = spec.get("facts") or {}
    if facts.get("toxic_plume") and not re.search(r"evacuat|shelter", text):
        # The crew stepping away from a fire isn't the 3 h toxic-plume trigger (CL-008, AD-151 on the test split).
        problems.append("the fumes must make people evacuate or shelter, in those words")
    linked = facts.get("fire_linked_to_pipeline") and "fire_linked_to_pipeline" not in (facts.get("open_points") or {})
    if facts.get("fire_or_explosion") and linked and (m := UNLINKED_FIRE.search(report)):
        problems.append(f"places the fire away from our facility: {m.group(0)}")
    if facts.get("release") is False:
        if hints := release_hints(report):
            problems.append(f"describes a release, but nothing was released: {', '.join(hints)}")
        if UNKNOWN_FIRE.search(report):
            problems.append("leaves open what fed the fire, but it wasn't product from the line")
    if not beyond_design_in_spec(facts) and (m := UNSTATED_BEYOND.search(report)):
        problems.append(f"states a beyond-design condition the spec doesn't have: {m.group(0)}")
    if any(re.search(rf"\b{re.escape(w)}\b", text) for w in RULE_WORDS):
        problems.append("talks about reporting rules")
    if any(re.search(rf"\b{re.escape(w)}", text) for w in CONDUCT_WORDS):
        problems.append("speculates about someone's conduct or condition")
    years = set(re.findall(r"\b(20\d\d)\b", report)) - {spec.get("discovered_at", "")[:4]}
    if years:
        problems.append(f"wrong year {', '.join(sorted(years))}")  # the writers drift to their own era (2024)
    words = len(report.split())
    if not 40 <= words <= 260:
        problems.append(f"length {words} words")
    return problems


def add_injection(report: str, text: str) -> str:
    """Prompt-injection cases: the hostile line goes in deterministically, as a postscript the reader can't skip."""
    return f"{report.rstrip()}\n\nPS: {text}"


# --- Generation ---


def generate(client, arn: str, spec: dict, feedback: list[str]) -> tuple[str, int, int]:
    user = prompt(spec)
    if feedback:
        user += "\n\nYour last draft had these problems; fix them:\n" + "\n".join(f"- {p}" for p in feedback)
    r = client.converse(
        modelId=arn,
        system=[{"text": SYSTEM}],
        messages=[{"role": "user", "content": [{"text": user}]}],
        inferenceConfig={"maxTokens": 600, "temperature": 0.8},
    )
    text = r["output"]["message"]["content"][0]["text"].strip()
    return text, r["usage"]["inputTokens"], r["usage"]["outputTokens"]


def generate_patiently(client, arn: str, spec: dict, feedback: list[str], pauses: int = 6):
    """generate(), pausing on throttling (after boto's own retries) instead of failing the run."""
    for pause in range(pauses):
        try:
            return generate(client, arn, spec, feedback)
        except ClientError as e:
            if e.response["Error"]["Code"] != "ThrottlingException" or pause == pauses - 1:
                raise
            print(f"{spec['id']} throttled; pausing {30 * (pause + 1)} s", flush=True)
            time.sleep(30 * (pause + 1))
    raise RuntimeError("unreachable")


def save(specs: list[dict], done: dict) -> None:
    order = [s["id"] for s in specs if s["id"] in done]
    CASES.write_text("".join(json.dumps(done[i], ensure_ascii=False) + "\n" for i in order), encoding="utf-8")


def sync(specs: list[dict], cases) -> dict:
    """Keep a written report only if its writer prompt is unchanged and it still passes the checker; refresh its spec
    fields (labels, facts) from the current spec. Everything else is (re)written."""
    by_id = {s["id"]: s for s in specs}
    keep = {}
    for c in cases:
        spec = by_id.get(c["id"])
        if spec is None or prompt(spec) != prompt(c) or spec.get("injection") != c.get("injection"):
            continue
        body = c["report"].removesuffix(f"\n\nPS: {c['injection']}") if c.get("injection") else c["report"]
        if check(spec, body):
            continue
        keep[c["id"]] = {**c, **spec}
    return keep


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Write the synthetic field reports.")
    ap.add_argument("--only", nargs="*", help="case IDs to (re)write")
    ap.add_argument("--limit", type=int, help="write at most N cases (smoke test)")
    args = ap.parse_args(argv)
    arns = {"llama": os.environ.get("WRITER_LLAMA_ARN"), "mistral": os.environ.get("WRITER_MISTRAL_ARN")}
    if not all(arns.values()):
        print("Set WRITER_LLAMA_ARN and WRITER_MISTRAL_ARN (terraform output writer_profile_arns).")
        return 2
    # Adaptive retries back off on throttling; the loop below also pauses and carries on rather than crash.
    client = boto3.client("bedrock-runtime", region_name=REGION,
                          config=Config(retries={"max_attempts": 10, "mode": "adaptive"}))  # fmt: skip
    specs = [json.loads(line) for line in SPECS.read_text(encoding="utf-8").splitlines()]
    old = [json.loads(line) for line in CASES.read_text(encoding="utf-8").splitlines()] if CASES.exists() else []
    done = sync(specs, old)
    todo = [s for s in specs if (args.only and s["id"] in args.only) or (not args.only and s["id"] not in done)]
    todo = todo[: args.limit] if args.limit else todo
    tokens = {w: [0, 0] for w in PRICES}
    failed = []
    for spec in todo:
        feedback, report, tries = [], "", 0
        for attempt in range(1, MAX_TRIES + 1):
            tries = attempt
            report, tin, tout = generate_patiently(client, arns[spec["writer"]], spec, feedback)
            tokens[spec["writer"]][0] += tin
            tokens[spec["writer"]][1] += tout
            feedback = check(spec, report)
            if not feedback:
                break
        if spec.get("injection"):
            report = add_injection(report, spec["injection"])
        status = "ok" if not feedback else "failed"
        if feedback:
            failed.append((spec["id"], feedback))
        done[spec["id"]] = {**spec, "report": report, "attempts": tries, "check": status, "problems": feedback}
        print(f"{spec['id']} {spec['writer']:7} attempt {tries} {status}", flush=True)
        save(specs, done)  # after every case, so an interruption loses nothing
    cost = sum(tokens[w][0] * PRICES[w][0] / 1e6 + tokens[w][1] * PRICES[w][1] / 1e6 for w in PRICES)
    print(f"tokens in/out: {tokens}; cost ≈ ${cost:.4f}; failed checks: {len(failed)}")
    for case_id, problems in failed:
        print(f"  {case_id}: {problems}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
