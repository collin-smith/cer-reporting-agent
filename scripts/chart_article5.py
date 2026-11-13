"""Article 5, figure 2, from the saved D47 dev runs ($0, no model calls).

Same answers, different behaviour: the reviewing agent in-process, through MCP with the in-process tool order, and
through MCP with the server's order. Three small multiples on their own axes (never one axis for two measures):
no-op patches a case (a value the agent re-sent that was already recorded), turns a case, and cost per 1,000
reports. Bars are the mean over all runs; ticks are each pass's mean, so the spread between passes shows. The
in-process-order MCP run is one pass (33 runs), so it has no spread.

One hue (one series per panel, rows labelled directly, no legend), the dataviz reference palette's slot 1, as in
article 3. SVG, then PNG at 2x through cairosvg.

Usage (from the project root):
    code/.venv/bin/python -I code/scripts/chart_article5.py output/assets
Writes output/assets/article-5-figure-02.png (and .svg).
"""

import html
import json
import pathlib
import statistics as st
import sys

CODE = pathlib.Path(__file__).resolve().parents[1]
RUNS = CODE / "evals" / "runs"
# The harness recorded cost_usd at Nova Lite $0.06 / $0.24 per 1M tokens (evals/config.toml); the AWS Price List
# for ca-central-1, as billed, is $0.064 / $0.256: both exactly 16/15 of the recorded rates (D53, D59).
LIST = 16 / 15
ARMS = [  # (label, sub-label, run)
    ("In-process", "Strands tools, articles 2–3", "20261108-203420-agent-nova-dev"),
    ("MCP, in-process order", "1 pass", "20261108-212028-agent-nova-mcp-inorder-dev"),
    ("MCP, server order", "kept for MCP (D48)", "20261108-204403-agent-nova-mcp-dev"),
]
SURFACE, TEXT, TEXT_2, GRID, AXIS, BAR = "#ffffff", "#0b0b0b", "#52514e", "#e6e5e1", "#b9b8b3", "#2a78d6"
FONT = "DejaVu Sans, Arial, sans-serif"


def rows(run: str) -> list[dict]:
    return [json.loads(line) for line in (RUNS / run / "results.jsonl").read_text(encoding="utf-8").splitlines()]


def measures(rs: list[dict]) -> dict:
    """Each measure: (mean over all runs, [mean per pass]), plus status right / missed counts."""
    per = {
        "noop": lambda r: sum(1 for p in r["packet"]["agent"]["patches"] if p.get("noop")),
        "turns": lambda r: r["packet"]["agent"]["turns"],
        "cost": lambda r: 1000 * LIST * r["cost_usd"],
    }
    reps = sorted({r["rep"] for r in rs})
    out = {k: (st.mean(f(r) for r in rs), [st.mean(f(r) for r in rs if r["rep"] == p) for p in reps])
           for k, f in per.items()}  # fmt: skip
    out["right"] = (sum(r["score"]["status"] for r in rs), len(rs))
    out["missed"] = sum(r["score"]["missed_report"] for r in rs)
    return out


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


def figure2(out: pathlib.Path) -> None:
    data = [(label, sub, measures(rows(run))) for label, sub, run in ARMS]
    for label, _, m in data:
        print(label, {k: (round(v[0], 3), [round(x, 2) for x in v[1]]) if isinstance(v, tuple) and
                      isinstance(v[1], list) else v for k, v in m.items()})  # fmt: skip
    panels = [("noop", "No-op patches a case", 1.25, (0, 0.5, 1.0), "{:.2f}", "{:.1f}"),
              ("turns", "Turns a case", 5, (0, 1, 2, 3, 4, 5), "{:.2f}", "{:.0f}"),
              ("cost", "Cost per 1,000 reports (US$)", 1.0, (0, 0.5, 1.0), "${:.2f}", "${:.2f}")]  # fmt: skip
    W, H, LEFT, TOP, PW, GAP, ROW, BAR_H = 1200, 420, 230, 150, 270, 40, 62, 22
    parts = [text(24, 34, "Same answers, different behaviour", size=19, weight="bold"),
             text(24, 58, "The reviewing agent on dev, 3 passes of 33 reports. Identical tool descriptions; what "
                  "changed through MCP was the order of the tool list.", size=12.5, fill=TEXT_2),
             text(24, 78, "Status right 91 of 99 and 3 missed, in-process and through MCP alike. Bars: mean over all "
                  "runs. Ticks: each pass's mean.", size=12.5, fill=TEXT_2)]  # fmt: skip
    for i, (label, sub, _m) in enumerate(data):
        y = TOP + i * ROW
        parts.append(text(LEFT - 14, y + 10, label, size=13, anchor="end", weight="bold"))
        parts.append(text(LEFT - 14, y + 27, sub, size=11.5, fill=TEXT_2, anchor="end"))
    for j, (key, title, xmax, ticks, fmt, tfmt) in enumerate(panels):
        x0 = LEFT + j * (PW + GAP)
        sx = lambda v, x0=x0, xmax=xmax: x0 + (PW - 50) * v / xmax  # noqa: E731
        parts.append(text(x0, TOP - 26, title, size=14, weight="bold"))
        bottom = TOP + len(data) * ROW - 18
        for t in ticks:
            parts.append(f'<line x1="{sx(t):.1f}" y1="{TOP - 12}" x2="{sx(t):.1f}" y2="{bottom}" stroke="{GRID}"/>')
            parts.append(text(sx(t), bottom + 18, tfmt.format(t), size=11.5, fill=TEXT_2, anchor="middle"))
        parts.append(f'<line x1="{x0}" y1="{TOP - 12}" x2="{x0}" y2="{bottom}" stroke="{AXIS}"/>')
        for i, (_, _, m) in enumerate(data):
            y = TOP + i * ROW
            mean, passes = m[key]
            w = sx(mean) - x0
            parts.append(f'<path d="M{x0},{y} h{w - 4:.1f} a4,4 0 0 1 4,4 v{BAR_H - 8} a4,4 0 0 1 -4,4 h{-(w - 4):.1f} '
                         f'z" fill="{BAR}"/>')  # fmt: skip
            if len(passes) > 1:
                for p in passes:
                    parts.append(f'<line x1="{sx(p):.1f}" y1="{y - 5}" x2="{sx(p):.1f}" y2="{y + BAR_H + 5}" '
                                 f'stroke="{TEXT}" stroke-width="2"/>')  # fmt: skip
            right = max([mean, *passes])
            parts.append(text(sx(right) + 8, y + BAR_H / 2 + 4.5, fmt.format(mean), size=12.5, weight="bold"))
    parts.append(text(24, H - 46, "A no-op patch re-sends a value the case already holds; the tool answers "
                      "\"nothing to change\". Restoring the in-process order through MCP brought it back to 0.61,",
                      size=12, fill=TEXT_2))  # fmt: skip
    parts.append(text(24, H - 28, "inside the in-process range (0.45–1.18 by pass), so the order explains most of the "
                      "gap. One pass: a direction, not a precise split.", size=12, fill=TEXT_2))  # fmt: skip
    save(parts, W, H, out / "article-5-figure-02")


if __name__ == "__main__":
    figure2(pathlib.Path(sys.argv[1]))
