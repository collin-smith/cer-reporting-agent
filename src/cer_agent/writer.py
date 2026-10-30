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
- State every fact in the FACTS list. Where two facts disagree, report both as given and don't settle which is
  right. Keep every number and unit exactly as given (you may say "approx." or
  "about" where the fact says estimated).
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
            f"DISCOVERED: {spec['discovered_at'].replace('T', ' ')}",
            f"WRITTEN AS: {spec['style']}, by a {spec['reporter']}",
            f"BACKGROUND (use loosely, in your own words): {c['what_happened']}; {c['detail']}; "
            f"equipment: {c['equipment'] or 'not specified'}; activity: {c['activity']}; "
            f"found by: {c['how_discovered'] or 'not specified'}",
            "FACTS:",
            *[f"- {p}" for p in spec["stated"]],
            "LEAVE OUT:",
            *[f"- {w}" for w in leave_out],
        ]
    )


# --- Checks ---

NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")
VOLUME = re.compile(r"\d[\d,.]*\s*(?:m3|m³|cubic|litres?|liters?|bbls?|barrels?|L\b)", re.IGNORECASE)
LAND_WORDS = ("fence", "right of way", "right-of-way", "ditch", "off site", "off-site", "neighbour", "neighbor",
              "landowner", "road")  # fmt: skip
PRODUCT_WORDS = ("crude", "oil", "condensate", "propane", "butane", "diesel", "gasoline", "gas", "ngl", "liquids",
                 "water", "h2s", "sour", "sweet")  # fmt: skip
# Speculation about people: the writer must not invent conduct, impairment or blame.
CONDUCT_WORDS = ("drink", "drinking", "drunk", "alcohol", "impaired", "distracted", "careless", "fault", "blame",
                 "negligen", "horseplay")  # fmt: skip
RULE_WORDS = ("cer", "regulator", "reportable", "deadline")  # "notified the control room" is fine


def numbers_in(text: str) -> set[str]:
    return {n.replace(",", "").rstrip(".") for n in NUMBER.findall(text)}


def check(spec: dict, report: str) -> list[str]:
    """Problems with a report; empty means accepted."""
    problems = []
    text = report.lower()
    have = numbers_in(report)
    for phrase in spec["stated"]:
        for n in numbers_in(phrase):
            variants = {n, n.rstrip("0").rstrip(".") if "." in n else n}
            if not variants & have:
                problems.append(f"missing number {n} (from: {phrase})")
    withheld = " ".join(spec["withheld"])
    if "volume" in withheld and VOLUME.search(report):
        problems.append("mentions a volume, which is withheld")
    if "where the product went" in withheld and any(w in text for w in LAND_WORDS):
        problems.append("mentions where the product went, which is withheld")
    if "what product" in withheld and any(re.search(rf"\b{w}\b", text) for w in PRODUCT_WORDS):
        problems.append("names the product, which is withheld")
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
    done = {}
    if CASES.exists():
        done = {c["id"]: c for c in map(json.loads, CASES.read_text(encoding="utf-8").splitlines())}
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
