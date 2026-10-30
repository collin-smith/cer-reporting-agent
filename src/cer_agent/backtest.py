"""Back-test the rules engine on the CER's own incident records (rules-spec §7, D12). $0, no AI.

Usage (from the project root):  python3 -I -m cer_agent.backtest   (with code/src on PYTHONPATH)
Writes output/backtest-report.md and output/backtest-disagreements.csv (incident numbers only; no company names).

What it can and can't test. Every CER record is a reported incident, so the engine should call each one reportable.
Some comparisons are independent checks of the rules; some are near-circular because the record's own incident
type is the only evidence the engine gets. The report labels which is which:
- independent: release classification (substance class and volume decide INC-d / INC-e / neither), the Significant
  flag (SIG-*), the 3-hour triggers, and reporting lag against the deadline for incidents since 2025-03-12;
- near-circular: injury, environment, fire and beyond-design types (the record's type is the evidence).
"""

from __future__ import annotations

import collections
import csv
import datetime as dt
import json
import pathlib

from cer_agent.rules import (
    COMPANY_PROPERTY,
    GAS,
    HVP,
    LVP,
    NON_HC,
    OFF_RIGHT_OF_WAY,
    RIGHT_OF_WAY,
    SOUR,
    Facts,
    decide,
    substance_class,
)

PROJECT = pathlib.Path(__file__).resolve().parents[3]
CER = PROJECT / "input" / "cer"
OUT = PROJECT / "output"
GUIDELINES_IN_FORCE = dt.date(2025, 3, 12)
EXCLUDED_FACILITY_TYPES = {"Processing"}  # rules-spec Q-1: plants follow the PPR, not the OPR


def yes(v: str) -> bool:
    return v.strip().lower() == "yes"


def num(v: str) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def parse_day(v: str, fmt: str) -> dt.date | None:
    try:
        return dt.datetime.strptime(v.strip()[:10], fmt).date()
    except ValueError:
        return None


def record_to_facts(r: dict) -> Facts:
    """What a field report about this incident would have told us, as far as the record shows it."""
    types = {t.strip() for t in r["Incident Types"].split(",")}
    substance = r["Substance"].strip()
    cls = substance_class(substance) if substance != "Not Applicable" else None
    lands = set()
    if yes(r["Affects Company Property"]):
        lands.add(COMPANY_PROPERTY)
    if yes(r["Affects Pipeline right-of-way"]):
        lands.add(RIGHT_OF_WAY)
    if yes(r["Affects off Pipeline right-of-way"]) or yes(r["Off Company Property"]):
        lands.add(OFF_RIGHT_OF_WAY)
    disc = parse_day(r["Discovered Date and Time"], "%Y/%m/%d")
    return Facts(
        discovered_at=dt.datetime.combine(disc, dt.time()) if disc else None,
        death="Fatality" in types,
        serious_injury=any("Serious Injury" in t for t in types),
        env_effect="significant" if "Adverse Environmental Effects" in types else "none",
        fire_or_explosion=bool(types & {"Fire", "Explosion"}),
        release="Release of Substance" in types,
        substance=substance if cls else None,
        volume_m3=num(r["Approximate Volume Released (m3)"]),
        # VOL-UNIT: CER volumes for HVP products are treated as liquid (rules-spec §7).
        volume_state="liquid" if cls == HVP else "gas" if cls in (GAS, SOUR) else None,
        # The record establishes that a gas release qualified; the rate isn't in the data (near-circular).
        gas_release_qualifies=True if cls in (GAS, SOUR, HVP) else None,
        through_pipe_body_or_weld={"yes": True, "no": False}.get(r["Pipe body release"].strip().lower()),
        lands=lands or None,
        rupture=yes(r["Rupture"]),
        toxic_plume=(num(r["Number of people evacuated"]) or 0) > 0,  # proxy: no plume column
        other_beyond_design="recorded" if "Operation Beyond Design Limits" in types else None,
    )


def significant_by_rule(r: dict, f: Facts) -> bool | None:
    """SIG-* (rules-spec §7). None where the record can't show the deciding fact."""
    cls = substance_class(f.substance) if f.substance else None
    year = int(r["Year"])
    vol = f.volume_m3 or 0
    if f.death or f.serious_injury:
        return True  # SIG-HARM
    if f.release and cls == SOUR:
        return True  # SIG-SOUR
    if f.release and cls == GAS and vol > 30_000:
        return True  # SIG-GAS30K
    if f.release and cls == LVP and vol > 1.5 and f.lands and f.lands - {COMPANY_PROPERTY}:
        return True  # SIG-LVP
    if f.release and cls in (GAS, LVP) and f.volume_m3 is None:
        return None  # the volume decides SIG-GAS30K / SIG-LVP, and the record has none
    if f.rupture and cls != NON_HC:
        return True  # SIG-RUPTURE
    if f.env_effect == "significant" and year <= 2024:
        return True  # SIG-ENV (applied before 2025 only)
    if f.fire_or_explosion:
        return None  # "fire or explosion that causes a pipeline or facility to be inoperative": no column
    return False


def release_expectation(f: Facts) -> str:
    cls = substance_class(f.substance) if f.substance else None
    if cls == LVP:
        return "INC-d" if (f.volume_m3 is None or f.volume_m3 > 1.5) else "OUT-LVP15"
    if cls in (GAS, SOUR, HVP):
        return "INC-e"
    if cls == NON_HC:
        return "NON-HC"
    return "no substance recorded" if cls is None else "JUDGE"


def run(path: pathlib.Path) -> dict:
    with path.open(encoding="cp1252", newline="") as fh:
        rows = list(csv.DictReader(fh))
    kept = [r for r in rows if r["Pipeline or Facility Type"].strip() not in EXCLUDED_FACILITY_TYPES]
    res = collections.Counter()
    release_cases = collections.Counter()
    sig = collections.Counter()
    sig_disagree = collections.Counter()
    timeliness = collections.Counter()
    disagreements = []
    t3_rules = collections.Counter()
    for r in kept:
        f = record_to_facts(r)
        d = decide(f)
        res[d.status] += 1
        res[f"route {d.route}"] += 1
        res[f"deadline {d.deadline}"] += 1
        if d.deadline == "T3":
            # A precautionary 3 h comes from the worst case, not a trigger in the record: count it once, as PREC.
            t3_rules.update(["PREC"] if "PREC" in d.deadline_rules else d.deadline_rules)
        if d.status == "not reportable":
            disagreements.append((r["Incident Number"], "engine: not reportable", ";".join(d.citations)))
        if f.release:
            exp = release_expectation(f)
            release_cases[exp] += 1
            if exp in ("OUT-LVP15", "NON-HC", "JUDGE", "no substance recorded"):
                disagreements.append((r["Incident Number"], f"release recorded; rules say {exp}", r["Substance"]))
        rule_sig = significant_by_rule(r, f)
        cer_sig = yes(r["Significant"])
        if rule_sig is None:
            sig["untestable"] += 1
        else:
            sig["agree" if rule_sig == cer_sig else "disagree"] += 1
            if rule_sig != cer_sig:
                reason = f"rules {'Significant' if rule_sig else 'not Significant'}; CER {'yes' if cer_sig else 'no'}"
                sig_disagree[reason] += 1
                disagreements.append((r["Incident Number"], f"Significant: {reason}", r["Incident Types"]))
        disc = f.discovered_at.date() if f.discovered_at else None
        rep = parse_day(r["Reported Date"], "%m/%d/%Y")
        if disc and rep and disc >= GUIDELINES_IN_FORCE and d.deadline:
            lag = (rep - disc).days
            timeliness[(d.deadline, "same or next day" if lag <= 1 else f"{lag} days")] += 1
            if lag > 1:
                disagreements.append((r["Incident Number"], f"{d.deadline} case reported after {lag} days", ""))
    return {
        "rows": len(rows),
        "kept": len(kept),
        "excluded": len(rows) - len(kept),
        "results": res,
        "release_cases": release_cases,
        "significant": sig,
        "significant_disagreements": sig_disagree,
        "timeliness": timeliness,
        "t3_rules": t3_rules,
        "disagreements": disagreements,
    }


def pct(n: int, d: int) -> str:
    return f"{100 * n / d:.1f}%" if d else "–"


def report(r: dict, snapshot: str) -> str:
    res, rel, sig, tl = r["results"], r["release_cases"], r["significant"], r["timeliness"]
    reportable = res["reportable"] + res["precautionary"]
    tested = sig["agree"] + sig["disagree"]
    lines = [
        "# Rules back-test",
        f"*Generated by `cer_agent.backtest` on {dt.date.today()} from `{snapshot}`. Incident numbers only.*",
        "",
        f"Records: {r['rows']}; processing plants excluded (rules-spec Q-1): {r['excluded']}; tested: {r['kept']}.",
        "",
        "## 1. Every record is a reported incident: does the engine agree?",
        f"- Reportable: **{reportable} of {r['kept']} ({pct(reportable, r['kept'])})**, of which "
        f"{res['precautionary']} precautionary (a deciding fact missing from the record).",
        f"- Not reportable under the rules: {res['not reportable']} (listed in the disagreements file).",
        f"- Deadline class: 3 h {res['deadline T3']}, 24 h {res['deadline T24']}. Rules behind the 3 h cases (a case "
        "can meet several): " + ", ".join(f"{k} {v}" for k, v in r["t3_rules"].most_common()) + ". PREC means a "
        "deciding fact (usually the volume) is missing from the record, so the worst case applies.",
        f"- Route: clear-cut {res['route clear-cut']}, judgment {res['route judgment']}.",
        "",
        "## 2. Releases: substance and volume against the release rules (independent)",
        "| What the rules say about the recorded release | Records |",
        "|---|---|",
        *[f"| {k} | {v} |" for k, v in rel.most_common()],
        "",
        "## 3. Significant flag against SIG-* (independent)",
        f"- Testable: {tested}; agree **{sig['agree']} ({pct(sig['agree'], tested)})**; disagree {sig['disagree']}; "
        f"untestable: {sig['untestable']} (fire or explosion with no 'inoperative' column, or a release with no "
        "volume).",
        *[f"  - {k}: {v}" for k, v in r["significant_disagreements"].most_common()],
        "",
        f"## 4. Reporting lag for incidents discovered since {GUIDELINES_IN_FORCE} (current guidelines)",
        "Proxy: the record has a report date but no time, so 'same or next day' is the best available check.",
        "| Deadline | Reported | Records |",
        "|---|---|---|",
        *[f"| {k[0]} | {k[1]} | {v} |" for k, v in sorted(tl.items(), key=lambda kv: (kv[0][0], -kv[1]))],
        "",
        "## 5. Near-circular checks",
        "Injury, environment, fire and beyond-design types come from the record's own incident type, and gas releases",
        "are taken as qualifying because the rate isn't recorded. Agreement there confirms the mapping, not the rules.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    manifest = json.loads((CER / "manifest.json").read_text(encoding="utf-8"))
    snapshot = manifest["current"]
    r = run(CER / snapshot)
    OUT.mkdir(exist_ok=True)
    (OUT / "backtest-report.md").write_text(report(r, snapshot), encoding="utf-8")
    with (OUT / "backtest-disagreements.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["incident_number", "finding", "detail"])
        w.writerows(sorted(r["disagreements"]))
    print(f"wrote output/backtest-report.md and output/backtest-disagreements.csv ({len(r['disagreements'])} rows)")


if __name__ == "__main__":
    main()
