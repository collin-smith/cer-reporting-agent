"""Article 7, figures 1 and 2 ($0, no model calls).

1. Bigger or thinking harder: status right (of the 30 hardest reports) against cost per report, one dot per arm, a
   log cost axis, and Wilson 95% intervals as vertical bars, so the overlap the text describes is visible. One series,
   one hue, each dot labelled directly (no legend).
2. Where the cost of a report goes: cost per 1,000 held-out reports by design at list prices, split into input and
   output tokens (two series: legend plus in-bar labels where they fit). Input dominates, which is why caching the
   prompt prefix pays.

Numbers are the article's tables: figure 1 from the D19 runs of 2026-11-10 (D54), costs at the billed Haiku 4.5 price;
figure 2 from `cost_article7.py` (held-out, 168 report-runs, Nova Lite $0.064 / $0.256 per million tokens).
Colours: the dataviz reference palette's validated slots 1 and 2 (chart_gen.SERIES). SVG, then PNG at 2x.

Usage (from the project root):
    code/.venv/bin/python -I code/scripts/chart_article7.py output/assets
Writes output/assets/article-7-figure-0{1,2}.png (and .svg).
"""

import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # -I drops the script dir
from chart_gen import GRID, INK, INK_2, ON_SERIES, SERIES, WIDTH, _bar, _header, _text, _write  # noqa: E402

N = 30
ARMS = [  # (label, status right of 30, cost a report in cents, label anchor, dx, dy): the two Haiku dots sit 1 apart
    ("Nova Lite", 19, 0.11, "start", 12, -6),
    ("Haiku 4.5", 23, 1.52, "end", -12, 34),
    ("Haiku 4.5 + thinking", 24, 2.16, "end", -12, -64),
]
DESIGNS = [  # (label, input tokens a report, output tokens a report), held-out
    ("Workflow (one reading)", 2829, 126),
    ("Strict check (shipped)", 7592, 335),
    ("One reviewing agent", 14266, 788),
    ("Supervisor + specialists", 19396, 1360),
]
PRICE_IN, PRICE_OUT = 0.064, 0.256  # Nova Lite, USD per 1M tokens, ca-central-1 list


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (centre - half) * n, (centre + half) * n


def figure1(out: pathlib.Path) -> pathlib.Path:
    top, plot_h, left, right, bottom = 84, 300, 56, 40, 84
    height = top + plot_h + bottom
    plot_w = WIDTH - left - right
    lo_c, hi_c = 0.05, 5.0  # cents, log axis
    lo_y, hi_y = 10, 30

    def x(c: float) -> float:
        return left + plot_w * (math.log10(c) - math.log10(lo_c)) / (math.log10(hi_c) - math.log10(lo_c))

    def y(v: float) -> float:
        return top + plot_h - plot_h * (v - lo_y) / (hi_y - lo_y)

    sub = "The 30 hardest reports, status right against cost. Bars: 95% intervals, which overlap."
    body = _header("A bigger model got 4 more right, at 14 times the cost", sub)
    for t in range(lo_y, hi_y + 1, 5):
        body.append(f'<line x1="{left}" y1="{y(t):.1f}" x2="{WIDTH - right}" y2="{y(t):.1f}" stroke="{GRID}"/>')
        body.append(_text(left - 8, y(t) + 4, str(t), 12, INK_2, anchor="end"))
    for c, lab in ((0.1, "0.1¢"), (0.3, "0.3¢"), (1, "1¢"), (3, "3¢")):
        body.append(f'<line x1="{x(c):.1f}" y1="{top}" x2="{x(c):.1f}" y2="{top + plot_h}" stroke="{GRID}"/>')
        body.append(_text(x(c), top + plot_h + 20, lab, 12, INK_2, anchor="middle"))
    body.append(_text(left + plot_w / 2, top + plot_h + 44, "Cost a report (log scale)", 13, INK_2, anchor="middle"))
    body.append(_text(0, top - 12, "Status right, of 30", 13, INK_2))
    for label, k, c, anchor, dx, dy in ARMS:
        lo, hi = wilson(k, N)
        cx, cy = x(c), y(k)
        body.append(f'<line x1="{cx:.1f}" y1="{y(min(hi, hi_y)):.1f}" x2="{cx:.1f}" y2="{y(lo):.1f}" '
                    f'stroke="{SERIES[0]}" stroke-width="2"/>')  # fmt: skip
        for v in (lo, min(hi, hi_y)):
            body.append(f'<line x1="{cx - 6:.1f}" y1="{y(v):.1f}" x2="{cx + 6:.1f}" y2="{y(v):.1f}" '
                        f'stroke="{SERIES[0]}" stroke-width="2"/>')  # fmt: skip
        body.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6" fill="{SERIES[0]}" stroke="#ffffff" stroke-width="2"/>')
        body.append(_text(cx + dx, cy + dy, label, 14, INK, 700, anchor))
        body.append(_text(cx + dx, cy + dy + 18, f"{k}/30 · {c:.2f}¢", 13, INK_2, 400, anchor))
    body.append(_text(0, height - 24, "Source: one pass per arm, same day; same agent, tools and rules (D54).", 11,
                      INK_2))  # fmt: skip
    body.append(_text(0, height - 9, "Haiku 4.5 at the billed $1.10 / $5.50 per million tokens.", 11, INK_2))
    return _write(out / "article-7-figure-01", WIDTH, height, body)


def figure2(out: pathlib.Path) -> pathlib.Path:
    top, bar_h, gap, label_w = 108, 40, 22, 190
    rows = [(lab, [tin * PRICE_IN / 1000, tout * PRICE_OUT / 1000]) for lab, tin, tout in DESIGNS]  # $ per 1,000
    height = top + len(rows) * (bar_h + gap) + 34
    scale = (WIDTH - label_w - 64) / max(sum(v) for _, v in rows)
    body = _header("Input tokens are most of the cost",
                   "Cost per 1,000 held-out reports by design, Nova Lite at list prices")  # fmt: skip
    lx = 0
    for name, colour in zip(("Input tokens", "Output tokens"), SERIES, strict=True):
        body.append(f'<rect x="{lx}" y="70" width="12" height="12" rx="2" fill="{colour}"/>')
        body.append(_text(lx + 18, 81, name, 13, INK))
        lx += 18 + len(name) * 7.4 + 24
    for r, (label, vals) in enumerate(rows):
        yy = top + r * (bar_h + gap)
        body.append(_text(label_w - 12, yy + bar_h / 2 + 5, label, 14, INK, 400, "end"))
        xx = label_w
        for s, v in enumerate(vals):
            w = v * scale
            last = s == len(vals) - 1
            seg_w = w - (0 if last else 2)  # 2px surface gap between segments
            rect = f'<rect x="{xx:.1f}" y="{yy}" width="{seg_w:.1f}" height="{bar_h}" fill="{SERIES[s]}"/>'
            body.append(_bar(xx, yy, seg_w, bar_h, SERIES[s], "right") if last else rect)
            if seg_w > 64:  # label only segments wide enough to hold it
                body.append(_text(xx + seg_w / 2, yy + bar_h / 2 + 6, f"${v:.2f}", 16, ON_SERIES[s], 700, "middle"))
            xx += w
        body.append(_text(xx + 8, yy + bar_h / 2 + 5, f"${sum(vals):.2f}", 14, INK, 700))
    body.append(_text(0, height - 10, "Source: held-out set, 168 report-runs per design; $0.064 / $0.256 per million "
                      "tokens (ca-central-1).", 11, INK_2))  # fmt: skip
    return _write(out / "article-7-figure-02", WIDTH, height, body)


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "output/assets")
    print(figure1(out))
    print(figure2(out))
