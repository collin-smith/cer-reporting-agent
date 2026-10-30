"""Static SVG + PNG charts for Medium articles (Medium takes images, so there's no hover layer).

Colours are the dataviz skill's default categorical slots, validated on a light surface (blue, then orange; adjacent
CVD ΔE 24.7, normal-vision ΔE 33.6, both ≥ 3:1 contrast). Text uses ink colours, never series colours. The PNG step
needs cairosvg (see table_gen.py); without it only the SVG is written.
"""

import html
import pathlib

FONT = "Helvetica, Arial, sans-serif"
SURFACE = "#ffffff"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
SERIES = ["#2a78d6", "#eb6834"]
ON_SERIES = ["#ffffff", INK]  # in-bar label ink: 4.4:1 on blue, 6.2:1 on orange
IN_BAR_SIZE = 19  # bold ≥ 18.7px is large text, so the 3:1 contrast floor applies
WIDTH = 680


def _text(x, y, s, size=14, fill=INK, weight=400, anchor="start"):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}">{html.escape(s)}</text>'
    )


def _bar(x, y, w, h, fill, round_end):
    """A bar with a 4px rounded data-end; round_end is 'top' or 'right'. The baseline end stays square."""
    r = min(4, w / 2, h / 2)
    if round_end == "top":
        d = f"M{x},{y + h} V{y + r} Q{x},{y} {x + r},{y} H{x + w - r} Q{x + w},{y} {x + w},{y + r} V{y + h} Z"
    else:
        d = (
            f"M{x},{y} H{x + w - r} Q{x + w},{y} {x + w},{y + r} V{y + h - r} Q{x + w},{y + h} {x + w - r},{y + h} "
            f"H{x} Z"
        )
    return f'<path d="{d}" fill="{fill}"/>'


def _header(title, subtitle):
    return [_text(0, 24, title, 19, INK, 700), _text(0, 48, subtitle, 14, INK_2)]


def _write(out_stem, width, height, body):
    out_stem = pathlib.Path(out_stem)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT}">\n'
        f'<rect width="{width}" height="{height}" fill="{SURFACE}"/>\n' + "\n".join(body) + "\n</svg>\n"
    )
    out_stem.parent.mkdir(parents=True, exist_ok=True)
    svg_path = out_stem.with_suffix(".svg")
    svg_path.write_text(svg, encoding="utf-8")
    try:
        import cairosvg
    except ImportError:
        print(f"wrote {svg_path} (cairosvg not installed; PNG skipped)")
        return svg_path
    png_path = out_stem.with_suffix(".png")
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), scale=2)
    return png_path


def column_chart(out_stem, title, subtitle, labels, values, source, y_max=100, unit="%"):
    """One series of vertical bars, each value labelled above its bar (few bars, so every value is shown)."""
    top, plot_h, left, bottom = 84, 220, 44, 60
    height = top + plot_h + bottom
    plot_w = WIDTH - left
    slot = plot_w / len(values)
    bar_w = min(72, slot * 0.5)
    body = _header(title, subtitle)
    for tick in range(0, y_max + 1, 25):
        y = top + plot_h - plot_h * tick / y_max
        body.append(f'<line x1="{left}" y1="{y:.1f}" x2="{WIDTH}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        body.append(_text(left - 8, y + 4, f"{tick}{unit}", 12, INK_2, anchor="end"))
    for i, (lab, v) in enumerate(zip(labels, values, strict=True)):
        cx = left + slot * (i + 0.5)
        h = plot_h * v / y_max
        body.append(_bar(cx - bar_w / 2, top + plot_h - h, bar_w, h, SERIES[0], "top"))
        body.append(_text(cx, top + plot_h - h - 8, f"{v:.0f}{unit}", 14, INK, 700, "middle"))
        body.append(_text(cx, top + plot_h + 20, lab, 13, INK_2, anchor="middle"))
    body.append(
        f'<line x1="{left}" y1="{top + plot_h}" x2="{WIDTH}" y2="{top + plot_h}" stroke="{INK_2}" stroke-width="1"/>'
    )
    body.append(_text(0, height - 10, source, 11, INK_2))
    return _write(out_stem, WIDTH, height, body)


def stacked_bars(out_stem, title, subtitle, rows, segments, source):
    """Horizontal bars split into two segments. rows: [(label, [seg1, seg2])]; segments: two legend names."""
    top, bar_h, gap, label_w = 108, 40, 22, 150
    height = top + len(rows) * (bar_h + gap) + 34
    total_max = max(sum(v) for _, v in rows)
    scale = (WIDTH - label_w - 48) / total_max
    body = _header(title, subtitle)
    lx = 0
    for name, colour in zip(segments, SERIES, strict=False):  # legend: swatch + name, in ink
        body.append(f'<rect x="{lx}" y="70" width="12" height="12" rx="2" fill="{colour}"/>')
        body.append(_text(lx + 18, 81, name, 13, INK))
        lx += 18 + len(name) * 7.4 + 24
    for r, (label, vals) in enumerate(rows):
        y = top + r * (bar_h + gap)
        body.append(_text(label_w - 12, y + bar_h / 2 + 5, label, 14, INK, 400, "end"))
        x = label_w
        for s, v in enumerate(vals):
            w = v * scale
            last = s == len(vals) - 1
            seg_w = w - (0 if last else 2)  # 2px surface gap between segments
            body.append(
                _bar(x, y, seg_w, bar_h, SERIES[s], "right")
                if last
                else f'<rect x="{x:.1f}" y="{y}" width="{seg_w:.1f}" height="{bar_h}" fill="{SERIES[s]}"/>'
            )
            if v:
                body.append(_text(x + seg_w / 2, y + bar_h / 2 + 7, str(v), IN_BAR_SIZE, ON_SERIES[s], 700, "middle"))
            x += w
        body.append(_text(x + 8, y + bar_h / 2 + 5, f"{sum(vals)}", 14, INK_2, 400))
    body.append(_text(0, height - 10, source, 11, INK_2))
    return _write(out_stem, WIDTH, height, body)
