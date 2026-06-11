#!/usr/bin/env python3
"""Render a Markdown file to a styled PDF (DejaVu unicode, tables, page numbers).

Usage: render_pdf.py <input.md> <output.pdf> "<Doc Title>" "<Subtitle>"
"""
import sys, re
import markdown
from fpdf import FPDF

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

def main():
    src, out = sys.argv[1], sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else ""
    subtitle = sys.argv[4] if len(sys.argv) > 4 else ""

    with open(src, encoding="utf-8") as fh:
        md_text = fh.read()

    html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    # fpdf2 html renderer: give tables a border + full width so columns lay out.
    html = html.replace("<table>", '<table border="1" width="100%">')

    # fpdf2 cannot render nested inline tags inside <td>/<th>; strip them (keep text).
    def _strip_cell(m):
        inner = re.sub(r"</?(strong|b|em|i|code)>", "", m.group(2))
        return m.group(1) + inner + m.group(3)

    html = re.sub(r"(<t[dh][^>]*>)(.*?)(</t[dh]>)", _strip_cell, html, flags=re.DOTALL)

    class PDF(FPDF):
        def header(self):
            if self.page_no() == 1:
                return
            self.set_font("DejaVu", "", 7)
            self.set_text_color(120)
            self.cell(0, 6, title, align="L")
            self.ln(8)
            self.set_text_color(0)

        def footer(self):
            self.set_y(-12)
            self.set_font("DejaVu", "", 7)
            self.set_text_color(120)
            self.cell(0, 6, f"{title}  —  page {self.page_no()}", align="C")
            self.set_text_color(0)

    pdf = PDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(16, 16, 16)
    # Unicode font (only regular + bold variants exist; map I/BI as fallback).
    pdf.add_font("DejaVu", "", f"{FONT_DIR}/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
    pdf.add_font("DejaVu", "I", f"{FONT_DIR}/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "BI", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
    pdf.add_font("DejaVuMono", "", f"{FONT_DIR}/DejaVuSansMono.ttf")
    pdf.add_font("DejaVuMono", "B", f"{FONT_DIR}/DejaVuSansMono-Bold.ttf")
    pdf.add_font("DejaVuMono", "I", f"{FONT_DIR}/DejaVuSansMono-Oblique.ttf")
    pdf.add_font("DejaVuMono", "BI", f"{FONT_DIR}/DejaVuSansMono-BoldOblique.ttf")
    pdf.set_font("DejaVu", "", 9.5)
    pdf.add_page()

    # Title block on page 1.
    if title:
        pdf.set_font("DejaVu", "B", 18)
        pdf.multi_cell(0, 9, title)
        pdf.ln(1)
    if subtitle:
        pdf.set_font("DejaVu", "", 10.5)
        pdf.set_text_color(90)
        pdf.multi_cell(0, 6, subtitle)
        pdf.set_text_color(0)
        pdf.ln(2)
    pdf.set_draw_color(180)
    pdf.line(16, pdf.get_y(), 194, pdf.get_y())
    pdf.ln(4)

    pdf.set_font("DejaVu", "", 9.5)
    # Small mono size for <pre>/<code> so wide ASCII diagrams fit the page width.
    tag_styles = None
    try:
        from fpdf.fonts import TextStyle
        tag_styles = {
            "pre": TextStyle(family="DejaVuMono", size_pt=6.5),
            "code": TextStyle(family="DejaVuMono", size_pt=6.5),
        }
    except Exception:
        tag_styles = None

    try:
        pdf.write_html(html, pre_code_font="DejaVuMono", tag_styles=tag_styles)
    except TypeError:
        try:
            pdf.write_html(html, pre_code_font="DejaVuMono")
        except TypeError:
            pdf.write_html(html)
    pdf.output(out)
    print(f"WROTE {out}  ({pdf.page_no()} pages)")

if __name__ == "__main__":
    main()
