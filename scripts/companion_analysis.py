"""Companion-piece analysis of the CER pipeline incident data.

Usage: python3 -I code/scripts/companion_analysis.py
Reads input/cer/pipeline-incidents-comprehensive-data.csv (cp1252),
writes output/companion-findings.md (tables only; no company names).
"""

import collections
import csv
import datetime as dt
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # -I drops the script dir
import chart_gen  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
CSV = PROJECT / "input" / "cer" / "pipeline-incidents-comprehensive-data.csv"
OUT = PROJECT / "output" / "companion-findings.md"
ASSETS = PROJECT / "output" / "assets"
SOURCE = (
    "Source: Canada Energy Regulator, Pipeline Incident Data (snapshot 2026-10-28). Open Government Licence – Canada."
)

LATE_DAYS = 30
BATCH_DAYS = 14
PERIODS = [(2008, 2012), (2013, 2017), (2018, 2022), (2023, 2026)]


def load():
    with open(CSV, encoding="cp1252", newline="") as f:
        return list(csv.DictReader(f))


def day(value, fmt):
    try:
        return dt.datetime.strptime(value.strip()[:10], fmt).date()
    except ValueError:
        return None


def num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def split(value):
    return [p.strip() for p in value.split(",") if p.strip()]


def yes(value):
    return value.strip().lower() == "yes"


def pct(n, d):
    return f"{100 * n / d:.0f}%" if d else "–"


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def counts(rows, key, top=10, explode=False):
    c = collections.Counter()
    for r in rows:
        for v in split(r[key]) if explode else [r[key].strip()]:
            c[v or "(blank)"] += 1
    return c.most_common(top)


def enrich(rows):
    for r in rows:
        r["_disc"] = day(r["Discovered Date and Time"], "%Y/%m/%d")
        r["_occ"] = day(r["Occurrence Date and Time"], "%Y/%m/%d")
        r["_rep"] = day(r["Reported Date"], "%m/%d/%Y")
        r["_lag"] = (r["_rep"] - r["_disc"]).days if r["_rep"] and r["_disc"] else None
        r["_hidden"] = (r["_disc"] - r["_occ"]).days if r["_disc"] and r["_occ"] else None
        r["_types"] = split(r["Incident Types"])
        r["_year"] = int(r["Year"]) if r["Year"].strip().isdigit() else None
        r["_sig"] = yes(r["Significant"])


def section_overview(rows):
    years = [r["_year"] for r in rows if r["_year"]]
    last = max(r["_rep"] for r in rows if r["_rep"])
    out = [
        "## 1. Overview",
        f"- Incidents: **{len(rows)}**, reported {min(years)}–{max(years)} (latest report date {last}; "
        f"{max(years)} is a partial year).",
        "- Status: " + ", ".join(f"{k} {v}" for k, v in counts(rows, "Status")),
        "",
        table(
            ["Incident type (an incident can have several)", "Incidents", "Share"],
            [(k, v, pct(v, len(rows))) for k, v in counts(rows, "Incident Types", explode=True)],
        ),
        "",
        table(["Pipeline or facility type", "Incidents"], counts(rows, "Pipeline or Facility Type")),
    ]
    return out


def section_lag(rows):
    lagged = [r for r in rows if r["_lag"] is not None and r["_lag"] >= 0]
    late = [r for r in lagged if r["_lag"] > LATE_DAYS]
    lags = [r["_lag"] for r in lagged]
    out = [
        "## 2. Time from discovery to report",
        "Calendar days from the discovered date to the reported date. The deadlines that applied before March 2025 "
        "aren't confirmed yet (rules-spec Q-5), so this measures lag, not lateness against a rule.",
        "",
        f"- Incidents with both dates: {len(lagged)}. Median lag {statistics.median(lags):.0f} day; "
        f"same day {pct(sum(1 for x in lags if x == 0), len(lags))}, "
        f"same or next day {pct(sum(1 for x in lags if x <= 1), len(lags))}, "
        f"over {LATE_DAYS} days **{len(late)}**.",
        "",
    ]
    rows_by_period = []
    for a, b in PERIODS:
        p = [r["_lag"] for r in lagged if r["_year"] and a <= r["_year"] <= b]
        p30 = sum(1 for x in p if x > LATE_DAYS)
        rows_by_period.append(
            (f"{a}–{b}", len(p), f"{statistics.median(p):.0f}", pct(sum(1 for x in p if x <= 1), len(p)), p30)
        )
    out += [
        table(["Period", "Incidents", "Median lag (days)", "Same/next day", f"> {LATE_DAYS} days"], rows_by_period),
        "",
    ]

    def compare(key, explode=False, top=8):
        allc = dict(counts(lagged, key, top=100, explode=explode))
        return [
            (k, v, pct(v, len(late)), pct(allc.get(k, 0), len(lagged)))
            for k, v in counts(late, key, top=top, explode=explode)
        ]

    out += [f"**The {len(late)} reports over {LATE_DAYS} days, compared with all incidents:**", ""]
    out += [
        table(
            ["Incident type", f"> {LATE_DAYS} d", "Share of late", "Share of all"],
            compare("Incident Types", explode=True),
        ),
        "",
    ]
    out += [
        table(
            ["How discovered", f"> {LATE_DAYS} d", "Share of late", "Share of all"],
            compare("How the incident was discovered"),
        ),
        "",
    ]
    out += [
        table(
            ["What happened (category)", f"> {LATE_DAYS} d", "Share of late", "Share of all"],
            compare("What happened category", explode=True),
        ),
        "",
    ]
    late_lags = sorted(r["_lag"] for r in late)
    out += [
        f"- Lag among the late reports: median {statistics.median(late_lags):.0f} days, "
        f"longest {late_lags[-1]} days; {sum(1 for x in late_lags if x > 365)} over a year.",
        "- Late reports by period: "
        + ", ".join(f"{a}–{b} {sum(1 for r in late if a <= r['_year'] <= b)}" for a, b in PERIODS),
        "",
    ]

    def in_batch(r):
        return any(
            o is not r and o["Company"] == r["Company"] and abs((o["_rep"] - r["_rep"]).days) <= BATCH_DAYS
            for o in late
        )

    batched = [r for r in late if in_batch(r)]
    single = sorted(r["_lag"] for r in late if not in_batch(r))
    geo = [r for r in late if "Geotechnical" in r["Detailed what happened"]]
    out += [
        f"**Batches:** {len(batched)} of the {len(late)} late reports were filed in batches (the same operator "
        f"filing other late reports within {BATCH_DAYS} days), including "
        f"{sum(1 for r in batched if r['_lag'] > 365)} of the {sum(1 for r in late if r['_lag'] > 365)} "
        f"that took over a year. Late reports filed on their own: median lag {statistics.median(single):.0f} days.",
        f"- {len(geo)} of the late reports have a geotechnical cause (wash-out, erosion, scouring, landslide); "
        f"{sum(1 for r in geo if 'Operation Beyond Design Limits' in r['_types'])} of them are recorded as "
        f"operation beyond design limits, the type that covers unintended pipe exposures.",
        f"- Late reports come from {len(set(r['Company'] for r in late))} of the "
        f"{len(set(r['Company'] for r in rows))} company names in the file (names overstate operators).",
        "",
    ]

    hidden = [r["_hidden"] for r in rows if r["_hidden"] is not None and r["_hidden"] >= 0]
    out += [
        f"**Occurrence to discovery:** {pct(sum(1 for x in hidden if x == 0), len(hidden))} discovered the day "
        f"they occurred; {sum(1 for x in hidden if x > LATE_DAYS)} went more than {LATE_DAYS} days undetected.",
        "",
    ]
    return out


def section_significant(rows):
    sig = [r for r in rows if r["_sig"]]
    non = [r for r in rows if not r["_sig"]]
    out = [
        "## 3. What Significant incidents have in common",
        f"{len(sig)} of {len(rows)} incidents ({pct(len(sig), len(rows))}) are marked Significant.",
        "",
    ]

    def share(group, test):
        return pct(sum(1 for r in group if test(r)), len(group))

    feats = [
        ("Release of substance", lambda r: "Release of Substance" in r["_types"]),
        ("Fire", lambda r: "Fire" in r["_types"]),
        ("Explosion", lambda r: "Explosion" in r["_types"]),
        ("Serious injury or fatality", lambda r: any("Injury" in t or t == "Fatality" for t in r["_types"])),
        ("Adverse environmental effects", lambda r: "Adverse Environmental Effects" in r["_types"]),
        ("Operation beyond design limits", lambda r: "Operation Beyond Design Limits" in r["_types"]),
        ("Rupture", lambda r: yes(r["Rupture"])),
        ("Off company property", lambda r: yes(r["Off Company Property"])),
        ("Emergency declared (any level)", lambda r: r["Emergency Level"].strip().startswith("Level")),
        ("People evacuated", lambda r: (num(r["Number of people evacuated"]) or 0) > 0),
        ("Liquid release type", lambda r: r["Release Type"].strip() == "Liquid"),
        ("Gas release type", lambda r: r["Release Type"].strip() == "Gas"),
    ]
    out += [
        table(
            ["Feature", "Significant", "Not significant"], [(name, share(sig, f), share(non, f)) for name, f in feats]
        ),
        "",
    ]
    by_period = []
    for a, b in PERIODS:
        p = [r for r in rows if r["_year"] and a <= r["_year"] <= b]
        by_period.append((f"{a}–{b}", len(p), sum(1 for r in p if r["_sig"]), share(p, lambda r: r["_sig"])))
    out += [table(["Period", "Incidents", "Significant", "Share"], by_period), ""]
    out += [table(["What happened (Significant)", "Count"], counts(sig, "What happened category", 8, True)), ""]
    return out


def section_causes(rows):
    out = ["## 4. Recurring causes", "Category fields can list several causes; each is counted.", ""]
    out += [
        table(
            ["What happened", "Incidents", "Share"],
            [(k, v, pct(v, len(rows))) for k, v in counts(rows, "What happened category", 10, True)],
        ),
        "",
    ]
    out += [
        table(
            ["Why it happened", "Incidents", "Share"],
            [(k, v, pct(v, len(rows))) for k, v in counts(rows, "Why it happened category", 10, True)],
        ),
        "",
    ]
    cats = [k for k, _ in counts(rows, "What happened category", 6, True)]
    trend = []
    for a, b in PERIODS:
        p = [r for r in rows if r["_year"] and a <= r["_year"] <= b]
        trend.append(
            [f"{a}–{b}"] + [pct(sum(1 for r in p if c in split(r["What happened category"])), len(p)) for c in cats]
        )
    out += ["**Share of incidents by period:**", "", table(["Period"] + cats, trend), ""]
    out += [
        table(["Activity at the time", "Incidents"], counts(rows, "Activity being performed at time of incident")),
        "",
    ]
    out += [
        table(["Most common detailed causes (what happened)", "Incidents"], counts(rows, "Detailed what happened", 8)),
        "",
    ]
    return out


def section_significant_rule(rows):
    """Check the Significant flag against the CER glossary definition and the Guidelines' 3-hour list."""
    lvp = {
        "Crude Oil - Sweet",
        "Crude Oil - Sour",
        "Crude Oil - Synthetic",
        "Condensate",
        "Gasoline",
        "Diesel Fuel",
        "Jet Fuel",
        "Lube Oil",
        "Waste Oil",
        "Hydraulic Fluid",
    }
    non_hc = {"Water", "Contaminated Water", "Produced Water", "Pulp slurry", "Drilling Fluid"}

    def vol(r):
        return num(r["Approximate Volume Released (m3)"]) or 0

    def line(name, group):
        return (name, len(group), sum(1 for r in group if r["_sig"]))

    env = [r for r in rows if "Adverse Environmental Effects" in r["_types"]]
    ruptures = [r for r in rows if yes(r["Rupture"])]
    groups = [
        line(
            "Death or serious injury", [r for r in rows if any("Injury" in t or t == "Fatality" for t in r["_types"])]
        ),
        line(
            "Sour gas or H2S release",
            [r for r in rows if r["Substance"].strip() in ("Natural Gas - Sour", "Hydrogen Sulphide")],
        ),
        line(
            "Sweet gas release over 30,000 m³",
            [r for r in rows if r["Substance"].strip() == "Natural Gas - Sweet" and vol(r) > 30000],
        ),
        line(
            "LVP release over 1.5 m³ off company property",
            [
                r
                for r in rows
                if r["Substance"].strip() in lvp
                and vol(r) > 1.5
                and (yes(r["Off Company Property"]) or yes(r["Affects off Pipeline right-of-way"]))
            ],
        ),
        line("Rupture, hydrocarbon line", [r for r in ruptures if r["Substance"].strip() not in non_hc]),
        line("Rupture, water or slurry line", [r for r in ruptures if r["Substance"].strip() in non_hc]),
        line("Adverse environmental effects, 2008–2024", [r for r in env if r["_year"] <= 2024]),
        line("Adverse environmental effects, 2025–2026", [r for r in env if r["_year"] >= 2025]),
    ]
    by_period = []
    for a, b in PERIODS:
        p = [r for r in rows if r["_year"] and a <= r["_year"] <= b]
        sig = [r for r in p if r["_sig"]]
        by_period.append((f"{a}–{b}", len(sig), sum(1 for r in sig if "Adverse Environmental Effects" in r["_types"])))
    return [
        "## 3a. The Significant flag against its definition",
        'CER glossary (Interactive Pipeline Map, modified 2022-08-05): "A significant incident is an acute event '
        "that results in: death; a serious injury (as defined in the OPR); a fire or explosion that causes a "
        "pipeline or facility to be inoperative; a LVP hydrocarbon release in excess of 1.5 m³ that leaves company "
        'property or the right-of-way; a rupture; or a toxic plume (as defined in CSA Z662)."',
        "",
        table(["Group", "Incidents", "Marked Significant"], groups),
        "",
        table(["Period", "Significant", "Of which adverse environmental effects"], by_period),
        "",
    ]


def section_quality(rows):
    releases = [r for r in rows if "Release of Substance" in r["_types"]]
    ruptures = [r for r in rows if yes(r["Rupture"])]
    hc_ruptures = [
        r
        for r in ruptures
        if r["Substance"].strip()
        not in ("Water", "Contaminated Water", "Produced Water", "Pulp slurry", "Drilling Fluid")
    ]
    closed = [r for r in rows if r["Status"].strip() == "Closed"]
    injury = [r for r in rows if any("Injury" in t for t in r["_types"])]
    fatal = [r for r in rows if "Fatality" in r["_types"]]
    ngl = [r for r in rows if r["Substance"].strip() == "Natural Gas Liquids"]
    two_cols = [
        r
        for r in rows
        if set(split(r["Incident Types"])) != set(split(r["Incident type"])) and r["Incident type"].strip()
    ]
    flags = [
        (
            "Releases with no volume",
            sum(1 for r in releases if num(r["Approximate Volume Released (m3)"]) is None),
            len(releases),
        ),
        (
            "Ruptures on hydrocarbon lines not marked Significant (water/slurry-line ruptures never are; see 3a)",
            sum(1 for r in hc_ruptures if not r["_sig"]),
            len(hc_ruptures),
        ),
        (
            "Closed incidents with cause still 'To be determined'",
            sum(1 for r in closed if "To be determined" in r["Why it happened category"]),
            len(closed),
        ),
        (
            "Serious-injury incidents with blank or zero injured count",
            sum(1 for r in injury if not num(r["Number of individuals injured"])),
            len(injury),
        ),
        (
            "Fatality incidents with blank or zero fatality count",
            sum(1 for r in fatal if not num(r["Number of fatalities"])),
            len(fatal),
        ),
        (
            "Natural gas liquids filed under release type 'Gas' (methodology lists NGL as Liquid)",
            sum(1 for r in ngl if r["Release Type"].strip() == "Gas"),
            len(ngl),
        ),
        (
            "Reported before discovered (negative lag)",
            sum(1 for r in rows if r["_lag"] is not None and r["_lag"] < 0),
            len(rows),
        ),
        (
            "Discovered before it occurred",
            sum(1 for r in rows if r["_hidden"] is not None and r["_hidden"] < 0),
            len(rows),
        ),
        (
            "Pipeline or facility type blank",
            sum(1 for r in rows if not r["Pipeline or Facility Type"].strip()),
            len(rows),
        ),
        ("How discovered blank", sum(1 for r in rows if not r["How the incident was discovered"].strip()), len(rows)),
        (
            "'Incident Types' and 'Incident type' columns disagree (where both filled)",
            len(two_cols),
            sum(1 for r in rows if r["Incident type"].strip()),
        ),
    ]
    out = [
        "## 5. Data-quality flags",
        "Questions about the data, not findings against any company. Each is a count over the relevant rows.",
        "",
        table(["Flag", "Rows flagged", "Out of", "Share"], [(n, k, d, pct(k, d)) for n, k, d in flags]),
        "",
        "- The file is cp1252-encoded (accented place names garble if read as UTF-8).",
        "- Discovered and occurrence times carry a time-zone word: "
        + ", ".join(
            f"{k} {v}"
            for k, v in collections.Counter(
                r["Discovered Date and Time"].split()[-1] for r in rows if r["Discovered Date and Time"].strip()
            ).most_common()
        ),
        "- Reported Date has no time, so a 3-hour deadline can't be checked from this file.",
        "",
    ]
    return out


def make_charts(rows):
    lagged = [r for r in rows if r["_lag"] is not None and r["_lag"] >= 0]
    labels, shares = [], []
    for a, b in PERIODS:
        p = [r["_lag"] for r in lagged if r["_year"] and a <= r["_year"] <= b]
        labels.append(f"{a}–{b}")
        shares.append(100 * sum(1 for x in p if x <= 1) / len(p))
    chart_gen.column_chart(
        ASSETS / "companion-chart-01-next-day",
        "Most incidents are reported by the next day",
        "Share of incidents reported the same day or the day after discovery, by period",
        labels,
        shares,
        SOURCE,
    )

    late = [r for r in lagged if r["_lag"] > LATE_DAYS]

    def in_batch(r):
        return any(
            o is not r and o["Company"] == r["Company"] and abs((o["_rep"] - r["_rep"]).days) <= BATCH_DAYS
            for o in late
        )

    split = {True: [0, 0], False: [0, 0]}
    for r in late:
        split[in_batch(r)][0 if r["_lag"] > 365 else 1] += 1
    chart_gen.stacked_bars(
        ASSETS / "companion-chart-02-batches",
        "Most of the longest delays were filed in batches",
        f"The {len(late)} incidents reported more than {LATE_DAYS} days after discovery, by how they were filed",
        [("Filed in a batch", split[True]), ("Filed alone", split[False])],
        ["More than a year", f"{LATE_DAYS + 1} days to a year"],
        SOURCE,
    )


def main():
    rows = load()
    enrich(rows)
    parts = [
        "# Companion piece: findings from the CER incident data",
        f"*Generated by `code/scripts/companion_analysis.py` on {dt.date.today()} from "
        f"`{CSV.name}` (snapshot 2026-10-28). Categories only, no company names.*",
        "",
    ]
    for section in (
        section_overview,
        section_lag,
        section_significant,
        section_significant_rule,
        section_causes,
        section_quality,
    ):
        parts += section(rows)
    make_charts(rows)
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
