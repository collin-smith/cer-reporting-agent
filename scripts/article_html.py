"""Render an article draft (Markdown) as a single readable HTML page.

Usage: python3 -I code/scripts/article_html.py output/companion-draft.md [--table-images]
Writes the .html next to the .md. Handles the subset the drafts use: headings, paragraphs, lists (one nesting
level), tables, images, fenced code, block quotes, rules, bold/italic/code/links. No dependencies.

--table-images renders each table as a PNG (table_gen.py, needs cairosvg) into output/assets/<draft>-table-NN.png
and puts the image in the page instead, the way it will appear on Medium.
"""

import html
import pathlib
import re
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # -I drops the script dir
import table_gen  # noqa: E402

ASSETS = pathlib.Path(__file__).resolve().parents[2] / "output" / "assets"
TABLE_IMAGES = {"on": False, "stem": "", "n": 0}

CSS = """
body { margin: 0; background: #fff; color: #242424; }
main { max-width: 680px; margin: 0 auto; padding: 48px 24px 96px;
       font: 20px/1.6 Georgia, Cambria, "Times New Roman", serif; }
h1 { font: 700 40px/1.2 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; margin: 0 0 16px; }
h2 { font: 700 26px/1.3 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; margin: 48px 0 8px; }
h3 { font: 700 21px/1.3 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; margin: 32px 0 8px; }
p, ul, ol { margin: 0 0 20px; }
li { margin: 4px 0; }
li > ul { margin: 4px 0 0; }
hr { border: 0; text-align: center; margin: 40px 0; }
hr::before { content: "· · ·"; letter-spacing: 12px; color: #6b6b6b; }
table { border-collapse: collapse; width: 100%; margin: 0 0 24px;
        font: 15px/1.4 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
th, td { border-bottom: 1px solid #e6e6e6; padding: 8px 10px; text-align: left; vertical-align: top; }
th { border-bottom: 2px solid #242424; }
td.n, th.n { text-align: right; font-variant-numeric: tabular-nums; }
code { font: 16px Menlo, Consolas, monospace; background: #f2f2f2; padding: 1px 4px; border-radius: 3px; }
pre { background: #f2f2f2; padding: 16px; overflow-x: auto; border-radius: 4px; }
pre code { padding: 0; background: none; }
blockquote { margin: 0 0 20px; padding-left: 20px; border-left: 3px solid #242424; font-style: italic; }
a { color: inherit; }
figure { margin: 0 0 24px; }
figure img { max-width: 100%; height: auto; }
.note { font-size: 15px; color: #6b6b6b; font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
"""


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?![\*\w])", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"(?<![\"'>])(https?://[^\s<)]+[^\s<).,])", r'<a href="\1">\1</a>', text)
    return text


def is_number(cell):
    return bool(re.fullmatch(r"[<>≤≥~]?\s*[\d,.]+\s*%?(\s*\(.*\))?|–", cell.strip()))


def plain(text):
    return re.sub(r"\*\*(.+?)\*\*|\*(.+?)\*|`([^`]+)`", lambda m: next(g for g in m.groups() if g), text)


def render_table(lines):
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    head, body = rows[0], rows[2:]
    if TABLE_IMAGES["on"]:
        TABLE_IMAGES["n"] += 1
        stem = ASSETS / f"{TABLE_IMAGES['stem']}-table-{TABLE_IMAGES['n']:02d}"
        img = table_gen.render_table(stem, [plain(c) for c in head], [[plain(c) for c in r] for r in body])
        alt = html.escape(plain(head[0]))
        size = ""
        if img.suffix == ".png":  # PNG is rendered at 2x; show it at its design width
            size = f' width="{struct.unpack(">I", img.read_bytes()[16:20])[0] // 2}"'
        return [f'<figure><img src="assets/{img.name}" alt="Table: {alt}"{size}></figure>']
    numeric = [all(is_number(r[i]) for r in body if i < len(r)) for i in range(len(head))]

    def cls(i):
        return ' class="n"' if numeric[i] else ""

    out = [
        "<table>",
        "<thead><tr>" + "".join(f"<th{cls(i)}>{inline(c)}</th>" for i, c in enumerate(head)) + "</tr></thead>",
        "<tbody>",
    ]
    out += ["<tr>" + "".join(f"<td{cls(i)}>{inline(c)}</td>" for i, c in enumerate(r)) + "</tr>" for r in body]
    return out + ["</tbody>", "</table>"]


def render_list(lines):
    ordered = bool(re.match(r"\d+\.", lines[0].strip()))
    tag = "ol" if ordered else "ul"
    out = [f"<{tag}>"]
    item = None
    items = []
    for ln in lines:
        top = re.match(r"(?:[-*]|\d+\.)\s+(.*)", ln)
        child = re.match(r"\s{2,}(?:[-*]|\d+\.)\s+(.*)", ln)
        if child:
            item["children"].append(child.group(1))
        elif top and not ln.startswith(" "):
            item = {"text": top.group(1), "children": []}
            items.append(item)
        else:
            if item["children"]:
                item["children"][-1] += " " + ln.strip()
            else:
                item["text"] += " " + ln.strip()
    for it in items:
        kids = "".join(f"<li>{inline(k)}</li>" for k in it["children"])
        out.append(f"<li>{inline(it['text'])}" + (f"<ul>{kids}</ul>" if kids else "") + "</li>")
    return out + [f"</{tag}>"]


def convert(md):
    lines = md.splitlines()
    out, i, title = [], 0, None
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
        elif ln.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(lines[i + 1 : j])) + "</code></pre>")
            i = j + 1
        elif m := re.match(r"(#{1,3})\s+(.*)", ln):
            level = len(m.group(1))
            title = title or (m.group(2) if level == 1 else None)
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
        elif m := re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", ln.strip()):
            out.append(f'<figure><img src="{html.escape(m.group(2))}" alt="{html.escape(m.group(1))}"></figure>')
            i += 1
        elif re.fullmatch(r"-{3,}", ln.strip()):
            out.append("<hr>")
            i += 1
        elif ln.lstrip().startswith("|"):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            out += render_table(lines[i:j])
            i = j
        elif re.match(r"(?:[-*]|\d+\.)\s+", ln):
            j = i + 1
            while (
                j < len(lines)
                and lines[j].strip()
                and (lines[j].startswith(" ") or re.match(r"(?:[-*]|\d+\.)\s+", lines[j]))
            ):
                j += 1
            out += render_list(lines[i:j])
            i = j
        elif ln.startswith(">"):
            j = i
            while j < len(lines) and lines[j].startswith(">"):
                j += 1
            out.append("<blockquote>" + inline(" ".join(q.lstrip("> ") for q in lines[i:j])) + "</blockquote>")
            i = j
        else:
            j = i
            while (
                j < len(lines) and lines[j].strip() and not re.match(r"(#{1,3}\s|\||```|>|(?:[-*]|\d+\.)\s)", lines[j])
            ):
                j += 1
            text = inline(" ".join(p.strip() for p in lines[i:j]))
            cls = ' class="note"' if text.startswith("<em>") and text.endswith("</em>") else ""
            out.append(f"<p{cls}>{text}</p>")
            i = j
    return title or "Draft", "\n".join(out)


def main():
    src = pathlib.Path(sys.argv[1])
    TABLE_IMAGES.update(on="--table-images" in sys.argv[2:], stem=src.stem)
    title, body = convert(src.read_text(encoding="utf-8"))
    page = (
        f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(re.sub(r'[*`]', '', title))}</title>\n<style>{CSS}</style>\n</head>\n"
        f"<body>\n<main>\n{body}\n</main>\n</body>\n</html>\n"
    )
    dst = src.with_suffix(".html")
    dst.write_text(page, encoding="utf-8")
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
