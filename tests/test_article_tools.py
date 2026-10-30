"""The article tooling: Markdown to HTML conversion and table-image column widths."""

import article_html
import table_gen


def test_table_becomes_html_table_with_numeric_columns_right_aligned():
    _, body = article_html.convert("| Type | Incidents |\n|---|---|\n| Fire | 472 |\n| Explosion | 33 |\n")
    assert "<table>" in body
    assert '<td class="n">472</td>' in body
    assert "<td>Fire</td>" in body


def test_nested_list_and_inline_marks():
    md = "- **Bold** item with `code`\n  - child *item*\n- second\n"
    _, body = article_html.convert(md)
    assert "<strong>Bold</strong>" in body
    assert "<code>code</code>" in body
    assert "<ul><li>child <em>item</em></li></ul>" in body
    assert body.count("<li>") == 3


def test_image_line_becomes_figure_and_title_comes_from_h1():
    title, body = article_html.convert("# The title\n\n![A chart](assets/x.png)\n")
    assert title == "The title"
    assert '<img src="assets/x.png" alt="A chart">' in body


def test_auto_widths_fit_the_page_and_never_cut_below_a_header():
    headers = ["Flag", "Rows", "Out of"]
    rows = [["A very long description of a data-quality flag that would overflow one line", "252", "846 (30%)"]]
    widths = table_gen.auto_widths(headers, rows)
    assert sum(widths) <= table_gen.TABLE_WIDTH
    for w, h in zip(widths, headers, strict=True):
        assert w >= len(h) * table_gen.CHAR_WIDTH
