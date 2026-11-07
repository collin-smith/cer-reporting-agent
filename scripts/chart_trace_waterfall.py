"""Article 2, figure 4: one case's trace as a waterfall, before and after the shared AWS client (D40).

Reads two pipeline trace files, takes the same case from each, and draws its top-level stages as bars on one shared
time axis (two panels). The untraced gap before the agent's first model call gets its own row. SVG, then PNG at 2x
through cairosvg (as the article table images are made).

Usage (from the project root):
    code/.venv/bin/python -I code/scripts/chart_trace_waterfall.py \
        code/evals/traces/20261107-140110-pipeline-dev code/evals/traces/20261107-140524-pipeline-dev CL-046 \
        output/assets/article-2-draft-figure-04
"""

import html
import json
import math
import pathlib
import sys

# Reference palette (dataviz skill): one categorical hue for model work, a neutral for untraced time.
SURFACE, TEXT, TEXT_2, GRID = "#ffffff", "#0b0b0b", "#52514e", "#e6e5e1"
MODEL, UNTRACED = "#2a78d6", "#b9b8b3"
FONT = "DejaVu Sans, Arial, sans-serif"

ROWS = [("extract", "Read the report"), ("gap", "Untraced"), ("review", "Agent review"), ("draft", "Draft the notice"),
        ("judge (model)", "Judge (model)")]  # fmt: skip
W, LEFT, RIGHT = 1200, 190, 40
ROW_H, BAR_H, PANEL_GAP = 34, 18, 46


def stages(trace_dir: pathlib.Path, case_id: str) -> tuple[dict, float]:
    spans = [json.loads(line) for line in (trace_dir / "traces.jsonl").read_text(encoding="utf-8").splitlines()]
    case = next(s for s in spans if s["name"] == "case" and s["attributes"].get("cer.id") == case_id)
    t0, kids = case["start_ms"], [s for s in spans if s["parent_id"] == case["span_id"]]
    out = {}
    for s in kids:
        key = "review" if s["name"].startswith("invoke_agent") else s["name"]
        if key in ("extract", "review", "draft", "judge (model)"):
            out[key] = ((s["start_ms"] - t0) / 1000, s["duration_ms"] / 1000)
    gap_start = out["extract"][0] + out["extract"][1]
    out["gap"] = (gap_start, out["review"][0] - gap_start)
    return out, case["duration_ms"] / 1000


def text(x, y, s, size=13, fill=TEXT, anchor="start", weight="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}">{html.escape(s)}</text>')  # fmt: skip


def panel(y0: float, title: str, st: dict, xmax: float, scale) -> list[str]:
    out = [text(LEFT, y0, title, size=15, weight="bold")]
    top = y0 + 16
    for i, (key, label) in enumerate(ROWS):
        cy = top + i * ROW_H + ROW_H / 2
        out.append(text(LEFT - 12, cy + 4.5, label, fill=TEXT_2, anchor="end"))
        start, dur = st[key]
        x0, x1 = scale(start), scale(start + dur)
        fill = UNTRACED if key == "gap" else MODEL
        w = max(x1 - x0, 2.0)
        out.append(f'<rect x="{x0:.1f}" y="{cy - BAR_H / 2:.1f}" width="{w:.1f}" height="{BAR_H}" rx="3" '
                   f'fill="{fill}"/>')  # fmt: skip
        note = f"{dur:.1f} s" if dur >= 0.05 else "under 0.1 s"
        if key == "gap" and dur >= 1:
            note += ": creating a new AWS client"
        out.append(text(x0 + w + 8, cy + 4.5, note, fill=TEXT))
    return out


def main(before_dir: str, after_dir: str, case_id: str, out_stem: str) -> None:
    before, t_before = stages(pathlib.Path(before_dir), case_id)
    after, t_after = stages(pathlib.Path(after_dir), case_id)
    xmax = math.ceil(max(t_before, t_after) / 2) * 2
    scale = lambda t: LEFT + (W - LEFT - RIGHT - 170) * t / xmax  # noqa: E731 (170 px kept for labels)
    panel_h = 16 + len(ROWS) * ROW_H
    y1 = 70
    y2 = y1 + panel_h + PANEL_GAP
    axis_y = y2 + panel_h + 8
    h = axis_y + 58
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" '
             f'font-family="{FONT}">', f'<rect width="{W}" height="{h}" fill="{SURFACE}"/>',
             text(24, 32, f"One case ({case_id}), traced stage by stage", size=18, weight="bold"),
             text(24, 54, "Bars are spans on one time axis from the start of the case. The rules engine and the "
                  "code checks take under 0.01 s each and are left out.", size=12.5, fill=TEXT_2)]  # fmt: skip
    for t in range(0, xmax + 1, 2):  # recessive vertical grid, shared by both panels
        x = scale(t)
        parts.append(f'<line x1="{x:.1f}" y1="{y1 + 10}" x2="{x:.1f}" y2="{axis_y}" stroke="{GRID}" stroke-width="1"/>')
        parts.append(text(x, axis_y + 18, f"{t} s", size=12, fill=TEXT_2, anchor="middle"))
    parts.append(text(scale(xmax / 2), axis_y + 42, "seconds from the start of the case", size=12, fill=TEXT_2,
                      anchor="middle"))  # fmt: skip
    parts += panel(y1 + 6, f"Before: a new AWS client for every case ({t_before:.1f} s)", before, xmax, scale)
    parts += panel(y2 + 6, f"After: one shared client per region ({t_after:.1f} s)", after, xmax, scale)
    parts.append("</svg>")
    svg = pathlib.Path(out_stem + ".svg")
    svg.parent.mkdir(parents=True, exist_ok=True)
    svg.write_text("\n".join(parts), encoding="utf-8")
    import cairosvg

    cairosvg.svg2png(url=str(svg), write_to=out_stem + ".png", scale=2)
    print("wrote", out_stem + ".png")


if __name__ == "__main__":
    main(*sys.argv[1:5])
