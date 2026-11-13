"""Article 1, figure 2, from the saved test run with layout variants ($0, no model calls).

Same words, different layout: how often the answer changed when a test report was read again with its blank lines
removed (`noblank`) or its lines wrapped at 72 characters (`wrap72`), against the same report in the same pass. By
case kind, with Wilson 95% intervals, using the harness's own `stability()`, so the numbers are the findings log's
(D32: 28 of 426, 6.6%).

One hue (one series, rows labelled directly, no legend), the dataviz reference palette's slot 1, as in articles 3-7.
SVG, then PNG at 2x through cairosvg.

Usage (from the project root):
    code/.venv/bin/python -I code/scripts/chart_article1.py output/assets
Writes output/assets/article-1-figure-02.png (and .svg).
"""

import html
import json
import pathlib
import sys

CODE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "src"))  # -I drops the script dir and the package path
from cer_agent.evals import stability  # noqa: E402

RUN = CODE / "evals" / "runs" / "20261104-163507-workflow-nova-test" / "results.jsonl"
KINDS = [  # (kind in the case file, label)
    ("not-reportable", "Not reportable"),
    ("judgment", "Judgment"),
    ("adversarial", "Adversarial"),
    ("clear-cut", "Clear-cut"),
]
SURFACE, TEXT, TEXT_2, GRID, AXIS, BAR = "#ffffff", "#0b0b0b", "#52514e", "#e6e5e1", "#b9b8b3", "#2a78d6"
FONT = "DejaVu Sans, Arial, sans-serif"


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


def data() -> tuple[dict, list[tuple[str, dict, int]]]:
    rows = [json.loads(line) for line in RUN.read_text(encoding="utf-8").splitlines()]
    overall = stability(rows)["overall"]
    by_kind = []
    for kind, label in KINDS:
        s = stability([r for r in rows if r["kind"] == kind])
        by_kind.append((label, s["overall"], len(s["flipped_cases"])))
    return overall, by_kind


def figure2(out: pathlib.Path) -> None:
    overall, by_kind = data()
    print("all", overall["flips"], "missed", overall["missed_reports"], "late", overall["late_deadlines"])
    for label, o, n_cases in by_kind:
        print(label, o["flips"], n_cases, "cases")
    W, H, LEFT, TOP, PW, ROW, BAR_H, XMAX = 1000, 430, 220, 130, 640, 56, 22, 0.30
    sx = lambda v: LEFT + PW * v / XMAX  # noqa: E731
    bottom = TOP + len(by_kind) * ROW - 18
    f = overall["flips"]
    parts = [text(24, 34, f"Same words, different layout: the answer changed {f['rate']:.1%} of the time", size=19,
                  weight="bold"),
             text(24, 58, f"Test split, 80 reports x 3 passes, each read again with its blank lines removed and with "
                  f"its lines wrapped ({f['n']} pairs).", size=12.5, fill=TEXT_2),
             text(24, 78, "Bars: share whose status, deadline or route changed. Whiskers: 95% intervals, which overlap "
                  "at this sample size.", size=12.5, fill=TEXT_2)]  # fmt: skip
    for t in (0, 0.1, 0.2, 0.3):
        parts.append(f'<line x1="{sx(t):.1f}" y1="{TOP - 12}" x2="{sx(t):.1f}" y2="{bottom}" stroke="{GRID}"/>')
        parts.append(text(sx(t), bottom + 18, f"{t:.0%}", size=11.5, fill=TEXT_2, anchor="middle"))
    parts.append(f'<line x1="{LEFT}" y1="{TOP - 12}" x2="{LEFT}" y2="{bottom}" stroke="{AXIS}"/>')
    # The overall rate as a reference line, labelled where it can't collide with a bar label.
    xo = sx(f["rate"])
    parts.append(f'<line x1="{xo:.1f}" y1="{TOP - 20}" x2="{xo:.1f}" y2="{bottom}" stroke="{TEXT_2}" '
                 f'stroke-width="1.5" stroke-dasharray="4 3"/>')  # fmt: skip
    parts.append(text(xo + 6, TOP - 22, f"all reports {f['rate']:.1%}", size=11.5, fill=TEXT_2))
    for i, (label, o, n_cases) in enumerate(by_kind):
        y = TOP + i * ROW
        fl = o["flips"]
        parts.append(text(LEFT - 14, y + 10, label, size=13, anchor="end", weight="bold"))
        sub = f"{fl['k']} of {fl['n']} reads; {n_cases} report{'s' if n_cases != 1 else ''}"
        parts.append(text(LEFT - 14, y + 27, sub, size=11.5, fill=TEXT_2, anchor="end"))
        w = sx(fl["rate"]) - LEFT
        parts.append(f'<path d="M{LEFT},{y} h{w - 4:.1f} a4,4 0 0 1 4,4 v{BAR_H - 8} a4,4 0 0 1 -4,4 '
                     f'h{-(w - 4):.1f} z" fill="{BAR}"/>')  # fmt: skip
        lo, hi = (sx(v) for v in fl["ci95"])
        mid = y + BAR_H / 2
        parts.append(f'<line x1="{lo:.1f}" y1="{mid}" x2="{hi:.1f}" y2="{mid}" stroke="{TEXT}" stroke-width="2"/>')
        for xx in (lo, hi):
            parts.append(f'<line x1="{xx:.1f}" y1="{mid - 6}" x2="{xx:.1f}" y2="{mid + 6}" stroke="{TEXT}" '
                         f'stroke-width="2"/>')  # fmt: skip
        parts.append(text(hi + 8, mid + 4.5, f"{fl['rate']:.1%}", size=12.5, weight="bold"))
    parts.append(text(24, H - 46, f"Among the re-laid-out reads: {overall['missed_reports']} missed reports and "
                      f"{overall['late_deadlines']} late deadlines. Reading every report in three layouts and "
                      "keeping the strictest", size=12, fill=TEXT_2))  # fmt: skip
    parts.append(text(24, H - 28, "answer gave 0 and 0 on the same test runs, for about 2.7 times the cost of one "
                      "read.", size=12, fill=TEXT_2))  # fmt: skip
    save(parts, W, H, out / "article-1-figure-02")


if __name__ == "__main__":
    figure2(pathlib.Path(sys.argv[1]))
