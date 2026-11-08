"""Article 3, figures 2 and 4, from the saved eval runs ($0, no model calls).

Figure 2: cost against harmful errors. Each design as a dot: cost per 1,000 reports (x) against missed plus late
reports (y), test and held-out as two panels on the same axes. The strict check with the reader fix (D44) is on test
only: the held-out set was spent on the comparison (D43), so there's no held-out dot for it.

Figure 4: what the reviewing agents changed. For each agent run, its status against the workflow's own reading of the
same report inside that run (the paired comparison): same answer, fixed an error, or made one. Plus the 88 escalations
re-scored in D42.

SVG, then PNG at 2x through cairosvg, as the other article figures. Colours: the dataviz reference palette, fixed order,
validated (scripts/validate_palette.js); every dot and bar is labelled directly, since three hues are under 3:1.

Usage (from the project root):
    code/.venv/bin/python -I code/scripts/chart_article3.py output/assets
Writes output/assets/article-3-figure-02.png and article-3-figure-04.png (and their SVGs).
"""

import html
import json
import pathlib
import sys

CODE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "src"))
from cer_agent.gate import counts, strict_replay  # noqa: E402

RUNS = CODE / "evals" / "runs"
CASES = CODE / "evals" / "cases" / "cases.jsonl"
D44_CASES = {f"CL-{n}" for n in range(167, 176)}

SURFACE, TEXT, TEXT_2, GRID, AXIS = "#ffffff", "#0b0b0b", "#52514e", "#e6e5e1", "#b9b8b3"
FONT = "DejaVu Sans, Arial, sans-serif"
# Categorical slots 1-5, fixed order (one per design, the same in both figures).
DESIGNS = {
    "workflow": ("Workflow, single reading", "#2a78d6"),
    "strict": ("Strict check", "#eb6834"),
    "agent": ("Single agent", "#1baf7a"),
    "supervisor": ("Supervisor + specialists", "#eda100"),
    "strict_fix": ("Strict check + reader fix", "#e87ba4"),
}
TEST = {
    "workflow": "20261104-163507-workflow-nova-test",
    "agent": "20261107-092254-agent-nova-test",
    "supervisor": "20261107-155940-supervisor-nova-test",
    "strict_fix": "20261108-105630-workflow-nova-strict-test",
}
HELDOUT = {
    "workflow": "20261108-081029-workflow-nova-heldout",
    "strict": "20261108-081321-workflow-nova-strict-heldout",
    "agent": "20261108-081634-agent-nova-heldout",
    "supervisor": "20261108-083527-supervisor-nova-heldout",
}


def rows(run: str) -> list[dict]:
    return [json.loads(line) for line in (RUNS / run / "results.jsonl").read_text(encoding="utf-8").splitlines()]


def point(rs: list[dict]) -> tuple[float, int, int]:
    """Cost per 1,000 reports, harmful errors (missed + late), and the number of runs."""
    c = counts(rs)
    return 1000 * sum(r["cost_usd"] for r in rs) / len(rs), c["missed"] + c["late"], c["n"]


def test_points() -> dict:
    cases = {json.loads(line)["id"]: json.loads(line) for line in CASES.read_text(encoding="utf-8").splitlines()}
    wf = rows(TEST["workflow"])
    single = [r for r in wf if "~" not in r["id"]]  # the run also read each report in the layout variants
    strict = strict_replay(wf, cases)
    for r in strict:  # the replay rebuilds the strict check; its cost is the three readings it combines
        r["cost_usd"] = sum(x["cost_usd"] for x in wf if x["id"].partition("~")[0] == r["id"] and x["rep"] == r["rep"])
    out = {"workflow": point(single), "strict": point(strict)}
    for k in ("agent", "supervisor"):
        out[k] = point(rows(TEST[k]))
    out["strict_fix"] = point([r for r in rows(TEST["strict_fix"]) if r["id"] not in D44_CASES])  # the same 80 cases
    return out


def heldout_points() -> dict:
    return {k: point(rows(run)) for k, run in HELDOUT.items()}


def text(x, y, s, size=13, fill=TEXT, anchor="start", weight="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}">{html.escape(s)}</text>')  # fmt: skip


def save(parts: list[str], w: int, h: int, stem: pathlib.Path) -> None:
    svg = stem.with_suffix(".svg")
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="{FONT}">', f'<rect width="{w}" height="{h}" fill="{SURFACE}"/>']  # fmt: skip
    svg.parent.mkdir(parents=True, exist_ok=True)
    svg.write_text("\n".join([*head, *parts, "</svg>"]), encoding="utf-8")
    import cairosvg

    cairosvg.svg2png(url=str(svg), write_to=str(stem.with_suffix(".png")), scale=2)
    print("wrote", stem.with_suffix(".png"))


# Label offsets (dx, dy, anchor) per design and panel, so labels don't collide at this data's positions.
LABELS = {
    ("test", "workflow"): (14, 5, "start"), ("test", "agent"): (14, 5, "start"),
    ("test", "strict"): (0, -22, "middle"), ("test", "supervisor"): (0, -22, "middle"),
    ("heldout", "workflow"): (0, 28, "middle"), ("heldout", "strict"): (0, -18, "middle"),
    ("heldout", "agent"): (0, -18, "middle"), ("heldout", "supervisor"): (-14, 5, "end"),
}  # fmt: skip


def figure2(out: pathlib.Path) -> None:
    panels = [("test", "Test: 80 reports, 3 passes (240 runs)", test_points()),
              ("heldout", "Held-out: 56 reports, 3 passes (168 runs)", heldout_points())]  # fmt: skip
    for key, _, pts in panels:
        print(key, {k: (round(c, 2), e, n) for k, (c, e, n) in pts.items()})
    W, H, PW, PH, TOP, LEFT, GAP = 1200, 600, 500, 330, 120, 80, 80
    XMAX, YMAX = 1.6, 6
    parts = [text(24, 34, "Cost against harmful errors", size=19, weight="bold"),
             text(24, 58, "Each dot is one design. Harmful errors are reports missed (the regulator never told) plus "
                  "reports late, counted over every run.", size=12.5, fill=TEXT_2),
             text(24, 78, "On test, three designs reach zero, and the agents cost 1.5–2.6× the strict check to get "
                  "there. On held-out, every design misses the same report (CL-064).", size=12.5,
                  fill=TEXT_2)]  # fmt: skip
    for i, (key, title, pts) in enumerate(panels):
        x0 = LEFT + i * (PW + GAP)
        sx = lambda c, x0=x0: x0 + PW * c / XMAX  # noqa: E731
        sy = lambda e: TOP + PH - PH * e / YMAX  # noqa: E731
        parts.append(text(x0, TOP - 14, title, size=14, weight="bold"))
        for e in range(0, YMAX + 1):
            parts.append(f'<line x1="{x0}" y1="{sy(e):.1f}" x2="{x0 + PW}" y2="{sy(e):.1f}" stroke="{GRID}"/>')
            parts.append(text(x0 - 10, sy(e) + 4.5, str(e), size=12, fill=TEXT_2, anchor="end"))
        for c in (0, 0.4, 0.8, 1.2, 1.6):
            parts.append(text(sx(c), TOP + PH + 20, f"${c:.2f}", size=12, fill=TEXT_2, anchor="middle"))
        parts.append(f'<line x1="{x0}" y1="{TOP + PH}" x2="{x0 + PW}" y2="{TOP + PH}" stroke="{AXIS}"/>')
        parts.append(text(x0 + PW / 2, TOP + PH + 44, "cost per 1,000 reports (US$)", size=12, fill=TEXT_2,
                          anchor="middle"))  # fmt: skip
        if i == 0:
            parts.append(f'<text transform="translate({x0 - 44},{TOP + PH / 2}) rotate(-90)" font-size="12" '
                         f'fill="{TEXT_2}" text-anchor="middle">missed + late reports</text>')  # fmt: skip
        for k, (cost, harm, _) in pts.items():
            name, colour = DESIGNS[k]
            cx, cy = sx(cost), sy(harm)
            if k == "strict_fix":  # same place as the strict check on test: a ring around its dot
                parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="13" fill="none" stroke="{colour}" '
                             f'stroke-width="3"/>')  # fmt: skip
                continue
            parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{colour}" stroke="{SURFACE}" '
                         f'stroke-width="2"/>')  # fmt: skip
            dx, dy, anchor = LABELS[(key, k)]
            label = f"{name}: {harm}"
            if key == "test" and k == "strict":
                label = "Strict check, with or without the fix (ring): 0"
            parts.append(text(cx + dx, cy + dy, label, size=12, anchor=anchor))
    x0 = LEFT + PW + GAP
    parts.append(text(x0, TOP + PH + 70, "No ring here: the held-out set was already used for the comparison. On 3 "
                      "fresh held-out", size=11.5, fill=TEXT_2))  # fmt: skip
    parts.append(text(x0, TOP + PH + 86, "reports, the strict check with the reader fix was right 9 of 9 times.",
                      size=11.5, fill=TEXT_2))  # fmt: skip
    # legend, one row: identity never by colour alone
    lx = 24
    for k, (name, colour) in DESIGNS.items():
        ring = k == "strict_fix"
        fill = f'fill="none" stroke="{colour}" stroke-width="2.5"' if ring else f'fill="{colour}"'
        parts.append(f'<circle cx="{lx + 6}" cy="{H - 24}" r="6" {fill}/>')
        parts.append(text(lx + 18, H - 19.5, name, size=12))
        lx += 30 + 7.2 * len(name)
    save(parts, W, H, out / "article-3-figure-02")


def paired(run: str) -> dict:
    c = {"same": 0, "fixed": 0, "broke": 0, "changed": 0}
    for r in rows(run):
        before, after, truth = r["packet"]["agent"]["workflow_status"], r["packet"]["status"], r["expected"]["status"]
        if before == after:
            c["same"] += 1
        elif after == truth:
            c["fixed"] += 1
        elif before == truth:
            c["broke"] += 1
        else:
            c["changed"] += 1
    return c


def figure4(out: pathlib.Path) -> None:
    bars = [(k, split, paired(run)) for split, runs in (("test", TEST), ("held-out", HELDOUT))
            for k, run in runs.items() if k in ("agent", "supervisor")]  # fmt: skip
    for k, split, c in bars:
        print(k, split, c)
    esc = [("Repeated the rules' own routing", 66, "#b9b8b3"), ("Needless (clear-cut cases)", 21, "#7b7a75"),
           ("A real catch", 1, "#2a78d6")]  # D42; neutrals for the noise, one hue for the catch  # fmt: skip
    W, H, LEFT, BAR_H, ROW = 1200, 440, 300, 22, 40
    TOP, BW = 120, 620
    parts = [text(24, 34, "What the reviewing agents changed", size=19, weight="bold"),
             text(24, 58, "Each agent run against the workflow's own reading of the same report, inside that run. "
                  "A changed answer is either a fix or a new error.", size=12.5, fill=TEXT_2)]  # fmt: skip
    parts.append(text(24, TOP - 16, "Status answers, per run", size=14, weight="bold"))
    for i, (k, split, c) in enumerate(bars):
        y = TOP + i * ROW
        n = sum(c.values())
        name, colour = DESIGNS[k]
        parts.append(text(LEFT - 12, y + BAR_H / 2 + 4.5, f"{name}, {split} ({n})", fill=TEXT_2, anchor="end"))
        x = LEFT
        for part, fill in (("same", "#d9d8d3"), ("fixed", colour), ("broke", "#e34948"), ("changed", "#7b7a75")):
            w = BW * c[part] / n
            if c[part]:
                parts.append(f'<rect x="{x:.1f}" y="{y}" width="{max(w, 3):.1f}" height="{BAR_H}" rx="3" '
                             f'fill="{fill}" stroke="{SURFACE}" stroke-width="2"/>')  # fmt: skip
            x += w
        changed = c["fixed"] + c["broke"] + c["changed"]
        note = ", ".join(f"{c[p]} {w}" for p, w in (("fixed", "fixed"), ("broke", "made worse")) if c[p])
        parts.append(text(LEFT + BW + 12, y + BAR_H / 2 + 4.5, f"{c['same']} same" + (f", {note}" if note else ""),
                          size=12, weight="bold" if changed else "normal"))  # fmt: skip
    y0 = TOP + len(bars) * ROW + 56
    parts.append(text(24, y0 - 16, "Escalations the agents asked for (88, test and dev, re-scored in D42)", size=14,
                      weight="bold"))  # fmt: skip
    x = LEFT
    for _label, n, fill in esc:
        w = BW * n / 88
        parts.append(f'<rect x="{x:.1f}" y="{y0}" width="{max(w, 3):.1f}" height="{BAR_H}" rx="3" fill="{fill}" '
                     f'stroke="{SURFACE}" stroke-width="2"/>')  # fmt: skip
        x += w
    parts.append(text(LEFT - 12, y0 + BAR_H / 2 + 4.5, "Escalations (88)", fill=TEXT_2, anchor="end"))
    lx = LEFT
    for label, n, fill in esc:
        parts.append(f'<rect x="{lx}" y="{y0 + 40}" width="12" height="12" rx="2" fill="{fill}"/>')
        s = f"{label}: {n} ({100 * n / 88:.0f}%)"
        parts.append(text(lx + 18, y0 + 50.5, s, size=12))
        lx += 40 + 7.0 * len(s)
    parts.append(text(24, H - 28, "Grey: same answer as the workflow · colour: a fix · red: a new error. Routing "
                      "stayed with the rules engine; escalations became a note to the approver (D42).", size=12,
                      fill=TEXT_2))  # fmt: skip
    save(parts, W, H, out / "article-3-figure-04")


if __name__ == "__main__":
    o = pathlib.Path(sys.argv[1])
    figure2(o)
    figure4(o)
