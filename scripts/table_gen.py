"""Render a table as an SVG + PNG image for Medium articles (Medium mangles HTML tables).

Same visual style as the MLOps and RAG series: dark navy header (#232F3E) with white bold text, alternating
white / #F5F5F5 rows, #CCCCCC grid lines, navy outer border. Column widths are sized from the content.

The PNG step needs cairosvg; run through uv, e.g.:
    UV_CACHE_DIR=$TMPDIR/uvcache uv run --no-project --with cairosvg python -I code/scripts/article_html.py \
        output/companion-draft.md --table-images
Without cairosvg the SVG is still written and a note is printed.
"""
import html
import pathlib
import textwrap

FONT_SIZE = 13.5
LINE_HEIGHT = 18
CELL_PAD_X = 14
CELL_PAD_Y = 23.5
HEADER_HEIGHT = 38
HEADER_FILL = "#232F3E"
HEADER_TEXT = "#FFFFFF"
ROW_FILL_A = "#FFFFFF"
ROW_FILL_B = "#F5F5F5"
GRID = "#CCCCCC"
TEXT_COLOR = "#222222"
CHAR_WIDTH = 8.0  # average glyph width at FONT_SIZE in DejaVu Sans (what cairosvg falls back to)
TABLE_WIDTH = 820
MIN_COL = 90


def _wrap(text, width_px):
    chars_per_line = max(8, int((width_px - 2 * CELL_PAD_X) / CHAR_WIDTH))
    return textwrap.wrap(text, chars_per_line) or [""]


def auto_widths(headers, rows, total=TABLE_WIDTH):
    """Give each column its natural width, shrinking the widest columns first if the table is too wide."""
    natural = [max(len(str(c)) for c in [h] + [r[i] for r in rows if i < len(r)]) * CHAR_WIDTH + 2 * CELL_PAD_X
               for i, h in enumerate(headers)]
    # Header text doesn't wrap, so a column never shrinks below its (bold) header.
    floor = [max(MIN_COL, len(h) * CHAR_WIDTH * 1.1 + 2 * CELL_PAD_X) for h in headers]
    widths = [max(f, w) for f, w in zip(floor, natural)]
    while sum(widths) > total:
        shrinkable = [i for i, w in enumerate(widths) if w > floor[i]]
        if not shrinkable:
            break
        i = max(shrinkable, key=lambda k: widths[k])
        widths[i] = max(floor[i], widths[i] - (sum(widths) - total))
    return [int(w) for w in widths]


def render_table(out_stem, headers, rows, col_widths=None, font_family="Helvetica, Arial, sans-serif"):
    """Write `<out_stem>.svg` (and `.png` if cairosvg is available). Returns the .png path if written, else .svg."""
    out_stem = pathlib.Path(out_stem)
    col_widths = col_widths or auto_widths(headers, rows)
    width = sum(col_widths)
    col_x = [sum(col_widths[:i]) for i in range(len(col_widths))]

    wrapped = [[_wrap(str(cell), col_widths[i]) for i, cell in enumerate(row)] for row in rows]
    heights = [max(2 * CELL_PAD_Y - LINE_HEIGHT, max(len(c) for c in wr) * LINE_HEIGHT
                   + 2 * (CELL_PAD_Y - LINE_HEIGHT)) for wr in wrapped]
    height = HEADER_HEIGHT + sum(heights)

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" font-family="{font_family}">',
           f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
           f'<rect x="0" y="0" width="{width}" height="{HEADER_HEIGHT}" fill="{HEADER_FILL}"/>']
    header_y = HEADER_HEIGHT / 2 + FONT_SIZE / 2.6
    for x, h in zip(col_x, headers):
        svg.append(f'<text x="{x + CELL_PAD_X}" y="{header_y:.1f}" font-size="{FONT_SIZE}" font-weight="700" '
                   f'fill="{HEADER_TEXT}">{html.escape(h)}</text>')
    y = HEADER_HEIGHT
    for i, (wr, rh) in enumerate(zip(wrapped, heights)):
        svg.append(f'<rect x="0" y="{y}" width="{width}" height="{rh}" '
                   f'fill="{ROW_FILL_A if i % 2 == 0 else ROW_FILL_B}"/>')
        for x, lines in zip(col_x, wr):
            for li, line in enumerate(lines):
                ty = y + (CELL_PAD_Y - LINE_HEIGHT) + LINE_HEIGHT * (li + 1) - (LINE_HEIGHT - FONT_SIZE)
                svg.append(f'<text x="{x + CELL_PAD_X}" y="{ty:.1f}" font-size="{FONT_SIZE}" '
                           f'fill="{TEXT_COLOR}">{html.escape(line)}</text>')
        y += rh
        svg.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="{GRID}" stroke-width="1"/>')
    for x in col_x[1:]:
        svg.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="{GRID}" stroke-width="1"/>')
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="none" stroke="{HEADER_FILL}" '
               f'stroke-width="1.5"/>')
    svg.append("</svg>")

    out_stem.parent.mkdir(parents=True, exist_ok=True)
    svg_path = out_stem.with_suffix(".svg")
    svg_path.write_text("\n".join(svg), encoding="utf-8")
    try:
        import cairosvg
    except ImportError:
        print(f"wrote {svg_path} (cairosvg not installed; PNG skipped)")
        return svg_path
    png_path = out_stem.with_suffix(".png")
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), scale=2)
    return png_path
