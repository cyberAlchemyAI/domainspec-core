#!/usr/bin/env python3
"""Build the IDE Ergonomics presentation PDF from the markdown slide source."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap

from fpdf import FPDF


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "IDE-ERGONOMICS-PRESENTATION.md"
OUTPUT = ROOT / "IDE-ERGONOMICS-PRESENTATION.pdf"

NAVY = (30, 48, 82)
TEAL = (19, 121, 112)
AMBER = (205, 139, 45)
PLUM = (103, 72, 129)
INK = (28, 32, 38)
MUTED = (92, 99, 112)
LIGHT = (244, 247, 249)
LINE = (214, 220, 228)

ACCENTS = [TEAL, AMBER, PLUM, NAVY]


@dataclass
class Slide:
    title: str
    subtitle: str
    body: list[tuple[str, object]]


def clean(text: str) -> str:
    subs = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2192": "->",
        "\u00a0": " ",
    }
    for src, dst in subs.items():
        text = text.replace(src, dst)
    return text.encode("latin-1", "replace").decode("latin-1")


def parse_markdown(path: Path) -> list[Slide]:
    chunks: list[list[str]] = [[]]
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip() == "---":
            chunks.append([])
        else:
            chunks[-1].append(raw.rstrip())

    slides: list[Slide] = []
    for chunk in chunks:
        lines = [line for line in chunk if line.strip() or line == ""]
        if not any(line.strip() for line in lines):
            continue

        title = ""
        subtitle = ""
        body_lines: list[str] = []
        for line in lines:
            if line.startswith("# ") and not title:
                title = line[2:].strip()
            elif line.startswith("## ") and not subtitle:
                subtitle = line[3:].strip()
            else:
                body_lines.append(line)

        body: list[tuple[str, object]] = []
        i = 0
        while i < len(body_lines):
            line = body_lines[i]
            if not line.strip():
                i += 1
                continue
            if line.startswith("```"):
                code: list[str] = []
                i += 1
                while i < len(body_lines) and not body_lines[i].startswith("```"):
                    code.append(body_lines[i])
                    i += 1
                body.append(("code", "\n".join(code)))
                i += 1
                continue
            if line.startswith("- "):
                bullets: list[str] = []
                while i < len(body_lines) and body_lines[i].startswith("- "):
                    bullets.append(body_lines[i][2:].strip())
                    i += 1
                body.append(("bullets", bullets))
                continue
            if line.startswith("> "):
                quote: list[str] = []
                while i < len(body_lines) and body_lines[i].startswith("> "):
                    quote.append(body_lines[i][2:].strip())
                    i += 1
                body.append(("quote", " ".join(quote)))
                continue

            para: list[str] = []
            while (
                i < len(body_lines)
                and body_lines[i].strip()
                and not body_lines[i].startswith(("- ", "```", "> "))
            ):
                para.append(body_lines[i].strip())
                i += 1
            body.append(("p", " ".join(para)))

        slides.append(Slide(title=title, subtitle=subtitle, body=body))
    return slides


class DeckPDF(FPDF):
    def footer(self) -> None:
        if self.page_no() <= 1:
            return
        self.set_y(-11)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 6, f"IDE Ergonomics presentation  |  {self.page_no()}", align="C")


def text_lines(pdf: FPDF, width: float, text: str, font_size: float) -> list[str]:
    # fpdf2 can wrap, but this keeps code-block sizing predictable.
    avg_mm = max(font_size * 0.34, 2.5)
    chars = max(int(width / avg_mm), 28)
    out: list[str] = []
    for part in text.splitlines() or [""]:
        out.extend(wrap(part, chars) or [""])
    return out


def draw_header(pdf: DeckPDF, slide: Slide, idx: int) -> float:
    accent = ACCENTS[(idx - 1) % len(ACCENTS)]
    pdf.set_fill_color(*accent)
    pdf.rect(0, 0, pdf.w, 6, style="F")
    pdf.set_draw_color(*LINE)
    pdf.line(18, 41, pdf.w - 18, 41)

    pdf.set_xy(18, 15)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(pdf.w - 36, 10, clean(slide.title), new_x="LMARGIN", new_y="NEXT")

    if slide.subtitle:
        pdf.set_x(18)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(pdf.w - 36, 5.6, clean(slide.subtitle), new_x="LMARGIN", new_y="NEXT")

    return max(pdf.get_y() + 7, 49)


def render_cover(pdf: DeckPDF, slide: Slide) -> None:
    pdf.add_page()
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, pdf.w, pdf.h, style="F")
    pdf.set_fill_color(*TEAL)
    pdf.rect(0, 0, 18, pdf.h, style="F")
    pdf.set_fill_color(*AMBER)
    pdf.rect(pdf.w - 18, 0, 18, pdf.h, style="F")

    pdf.set_xy(32, 48)
    pdf.set_font("Helvetica", "B", 34)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(pdf.w - 64, 14, clean(slide.title), new_x="LMARGIN", new_y="NEXT")

    pdf.set_x(32)
    pdf.set_font("Helvetica", "", 17)
    pdf.set_text_color(223, 231, 240)
    pdf.multi_cell(pdf.w - 64, 8, clean(slide.subtitle), new_x="LMARGIN", new_y="NEXT")

    y = pdf.get_y() + 10
    pdf.set_xy(32, y)
    pdf.set_font("Helvetica", "", 11.5)
    for kind, payload in slide.body:
        if kind == "p":
            pdf.multi_cell(pdf.w - 64, 6.4, clean(str(payload)), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1.5)

    pdf.set_xy(32, pdf.h - 33)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 7, "Project overview | generated from IDE-ERGONOMICS-PRESENTATION.md")


def render_slide(pdf: DeckPDF, slide: Slide, idx: int) -> None:
    pdf.add_page()
    y = draw_header(pdf, slide, idx)
    left = 22
    width = pdf.w - 44
    pdf.set_y(y)

    for kind, payload in slide.body:
        if kind == "p":
            pdf.set_x(left)
            pdf.set_font("Helvetica", "", 12)
            pdf.set_text_color(*INK)
            pdf.multi_cell(width, 6.2, clean(str(payload)), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif kind == "bullets":
            pdf.set_font("Helvetica", "", 11.4)
            pdf.set_text_color(*INK)
            for item in payload:  # type: ignore[assignment]
                pdf.set_x(left)
                pdf.set_font("Helvetica", "B", 11.4)
                pdf.set_text_color(*TEAL)
                pdf.cell(6, 6.1, "-")
                pdf.set_font("Helvetica", "", 11.4)
                pdf.set_text_color(*INK)
                pdf.multi_cell(width - 7, 6.1, clean(str(item)), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif kind == "code":
            code = clean(str(payload))
            lines = text_lines(pdf, width - 14, code, 9.4)
            box_h = min(max(10 + len(lines) * 4.8, 24), 108)
            pdf.set_x(left)
            pdf.set_fill_color(*LIGHT)
            pdf.set_draw_color(*LINE)
            pdf.rect(left, pdf.get_y(), width, box_h, style="DF")
            pdf.set_xy(left + 7, pdf.get_y() + 6)
            pdf.set_font("Courier", "", 9.4)
            pdf.set_text_color(42, 47, 56)
            pdf.multi_cell(width - 14, 4.8, code, new_x="LMARGIN", new_y="NEXT")
            pdf.set_y(pdf.get_y() + 4)
        elif kind == "quote":
            pdf.set_x(left)
            pdf.set_fill_color(249, 244, 235)
            pdf.set_draw_color(*AMBER)
            start_y = pdf.get_y()
            pdf.set_font("Helvetica", "I", 12)
            pdf.set_text_color(*INK)
            pdf.multi_cell(width, 6.3, clean(str(payload)), new_x="LMARGIN", new_y="NEXT", fill=True)
            pdf.line(left, start_y, left, pdf.get_y())
            pdf.ln(2)


def main() -> None:
    slides = parse_markdown(SOURCE)
    if not slides:
        raise SystemExit("no slides parsed")

    pdf = DeckPDF(orientation="L", format="A4")
    pdf.set_title("IDE Ergonomics Presentation")
    pdf.set_creator("Codex / fpdf2")
    pdf.set_author("ide-ergonomics")
    pdf.set_auto_page_break(False)
    pdf.set_margins(18, 14, 18)

    render_cover(pdf, slides[0])
    for idx, slide in enumerate(slides[1:], start=2):
        render_slide(pdf, slide, idx)

    pdf.output(str(OUTPUT))
    print(f"wrote {OUTPUT.relative_to(ROOT)} pages: {len(slides)}")


if __name__ == "__main__":
    main()
