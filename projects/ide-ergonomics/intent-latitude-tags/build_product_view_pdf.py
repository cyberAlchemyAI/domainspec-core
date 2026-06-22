#!/usr/bin/env python3
"""Build the Intent-Latitude Tags product-view PDF (+ markdown source).

Companion to projects/ide-ergonomics/IDE-ERGONOMICS-PRODUCT-VIEW.pdf, same
toolchain (fpdf2, Creator "Codex / fpdf2"). One block model renders both
outputs so the .md source and .pdf export stay in sync.
"""
from fpdf import FPDF
from fpdf.fonts import FontFace

NAVY = (33, 55, 90)
GRAY = (90, 90, 90)
LIGHT = (244, 246, 249)

# ---- content as one block model -------------------------------------------
# block kinds: h1, sub, h2, p, quote, code, bullets, table
BLOCKS = [
    ("h1", "Product View: Intent-Latitude Tags"),
    ("sub", "Companion to the IDE Ergonomics Product View  |  input-side ergonomic "
            "primitive for the conversation surface  |  status: research-backed, "
            "L0 proof-of-concept planned  |  2026-06-19"),

    ("h2", "One-Sentence Product"),
    ("p", "Intent-Latitude Tags let a user mark how much freedom the agent has over a "
          "span of their own message - reproduce it exactly, achieve this outcome "
          "however, or never cross this line - and a post-hoc validator checks the "
          "agent's output against those marks. It is the input-side companion to the "
          "IDE Ergonomics routing cards: those route what the agent produced; this "
          "constrains how the agent reads what you meant."),

    ("h2", "The Problem: Intent Drift"),
    ("p", "You write a prompt. The agent reads one span too literally - it obeys an "
          "aside as an instruction, or reproduces context you meant as flexible. It "
          "reads another span too freely - it paraphrases away a legal disclaimer "
          "that had to stay exact, or chases the literal words instead of the outcome "
          "you wanted. You knew what you meant; the surface gave you no governed way "
          "to say it. This is the conversation-input analog of route ambiguity, and "
          "it is named in the literature (\"Intent Misalignment\"; \"specification "
          "gaming\")."),

    ("h2", "What The Product Is"),
    ("p", "A one-tap latitude annotation over a selected span, plus a validator that "
          "turns the mark into a check."),
    ("table", [
        ["Tag", "Means", "The validator does", "Strength"],
        ["[literal]", "Reproduce / preserve exactly",
         "Diff-checks the span appears verbatim in output", "STRONG (no model)"],
        ["[goal]", "Outcome to achieve, wording free",
         "Excludes from verbatim checks; routes to a rubric/oracle", "WEAK (flag-grade)"],
        ["[constraint]", "A line not to cross",
         "Checks output does not violate it", "MEDIUM"],
    ], (18, 33, 34, 15)),
    ("p", "The load-bearing rule: the tag's force lives in the validator, never in the "
          "agent \"understanding\" a magic marker. An ungrounded tag is just a prose "
          "header re-skinned - which is why naive bracket tags add nothing."),

    ("h2", "What People Gain"),
    ("table", [
        ["Gain", "Before", "With Intent-Latitude Tags"],
        ["Less misread intent", "The agent guesses how literally to take each span.",
         "The user marks latitude once; the check enforces it."],
        ["Exact strings stay exact", "A disclaimer or ID gets quietly paraphrased.",
         "[literal] spans are diff-checked verbatim; drift is caught."],
        ["Honest uncertainty", "\"It probably followed the prompt.\"",
         "Unenforceable spans are reported, never silently passed."],
        ["No false confidence", "Structure is assumed to fix interpretation.",
         "Strong vs flag-grade is labelled on every check."],
    ], (22, 39, 39)),

    ("h2", "How It Works"),
    ("code", "selected message span\n"
             "  -> latitude annotation ( [literal] / [goal] / [constraint] )\n"
             "  -> agent produces output\n"
             "  -> post-hoc validator checks each tagged span\n"
             "  -> draft verdict: PASS / FAIL / FLAG / unenforced\n"
             "  -> nothing canonical or runtime is promoted"),

    ("h2", "Why The Naive Version Fails (and what we cite)"),
    ("p", "A precedent sweep killed the obvious version. Bare brackets whose meaning "
          "the agent reads off the word inside collapse to existing delimiter and "
          "content-tag practice: \"[literal] keep the disclaimer\" does nothing that "
          "\"Verbatim - do not change: keep the disclaimer\" does not. Only the "
          "grounded form - latitude enforced by a validator - earns its keep. Cite "
          "the idea honestly: it is an \"inline IFID for prompts\" (Searle & "
          "Vanderveken, 1985), and it must be distinguished by name from the "
          "same-named Gmeiner et al. CHI 2025 \"Intent Tagging\" (a different, "
          "canvas-based system)."),

    ("h2", "MVP Shape: the L0 proof"),
    ("p", "The first proof is not an IDE extension and not all three tags. It is the "
          "cheapest falsifier: a pure parser plus the [literal] verbatim check, run "
          "over a fixture set, with no model required. Four small units "
          "(SWU-ILT-001..004) end at one decision."),
    ("table", [
        ["Unit", "Builds", "Done when"],
        ["SWU-ILT-001", "Tag parser with author-time errors",
         "parses valid input; rejects unbalanced / overlap / unknown"],
        ["SWU-ILT-002", "[literal] verbatim check + normalize",
         "paraphrase -> FAIL; intact -> PASS"],
        ["SWU-ILT-003", "Fixture set + runner (the kill condition)",
         "green on cases; >=1 real-model output captured"],
        ["SWU-ILT-004", "L0 decision note",
         "states continue or kill, with the evidence"],
    ], (20, 39, 41)),

    ("h2", "How We Will Test It (the kill condition)"),
    ("p", "The L0 proof answers one question:"),
    ("quote", "Does grounded [literal] enforcement catch a paraphrased verbatim span "
              "that a prose header would miss - AND does that check ever fire on "
              "output a real model actually produces?"),
    ("bullets", [
        "If yes: the grounded form is real; promote to L1 ([goal] exclusion) and the "
        "judge question (L2).",
        "If the check never fires in practice: the tag layer is ceremony - kill it. "
        "A clean kill is a successful, cheap result.",
    ]),

    ("h2", "Boundaries and Open Debt"),
    ("bullets", [
        "Research and planning only; no validator/runtime change without an approved "
        "task-session.",
        "Judge-grounding for [goal]/[constraint] is deferred (the central open "
        "question) - kept flag-grade until fixture-validated.",
        "Lane A alternative still owed: a clarification loop that asks before acting, "
        "which overlaps this project's bounded conversation-transition card MVP. "
        "Compare before promotion.",
        "Full artifacts: see intent-latitude-tags/ (SEED, FINDINGS, SPEC, "
        "development/).",
    ]),
]

# ---- PDF renderer ----------------------------------------------------------
_SUBS = {"—": "-", "–": "-", "’": "'", "‘": "'",
         "“": '"', "”": '"', "→": "->", "≥": ">=",
         "…": "...", "•": "-", " ": " "}


def s(t):
    for k, v in _SUBS.items():
        t = t.replace(k, v)
    return t.encode("latin-1", "replace").decode("latin-1")


class PDF(FPDF):
    def footer(self):
        self.set_y(-13)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 8, f"Intent-Latitude Tags  -  IDE Ergonomics      {self.page_no()}",
                  align="C")


pdf = PDF(format="A4")
pdf.set_title("Intent-Latitude Tags Product View")
pdf.set_creator("Codex / fpdf2")
pdf.set_author("ide-ergonomics")
pdf.set_auto_page_break(True, margin=18)
pdf.set_margins(20, 18, 20)
pdf.add_page()

head = FontFace(emphasis="BOLD", color=255, fill_color=NAVY)

for blk in BLOCKS:
    kind = blk[0]
    if kind == "h1":
        pdf.set_font("Helvetica", "B", 21)
        pdf.set_text_color(*NAVY)
        pdf.multi_cell(0, 9, s(blk[1]), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
    elif kind == "sub":
        pdf.set_font("Helvetica", "I", 9.5)
        pdf.set_text_color(*GRAY)
        pdf.multi_cell(0, 5, s(blk[1]), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
    elif kind == "h2":
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(*NAVY)
        pdf.multi_cell(0, 7, s(blk[1]), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(*NAVY)
        pdf.set_line_width(0.4)
        y = pdf.get_y() + 0.5
        pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
        pdf.ln(2.5)
    elif kind == "p":
        pdf.set_font("Helvetica", "", 10.5)
        pdf.set_text_color(20, 20, 20)
        pdf.multi_cell(0, 5.4, s(blk[1]), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1.5)
    elif kind == "quote":
        pdf.ln(0.5)
        pdf.set_font("Helvetica", "I", 10.5)
        pdf.set_text_color(*NAVY)
        pdf.set_fill_color(*LIGHT)
        pdf.set_x(pdf.l_margin + 3)
        pdf.multi_cell(pdf.epw - 3, 5.6, s(blk[1]), new_x="LMARGIN", new_y="NEXT",
                       fill=True, border="L")
        pdf.ln(1.5)
    elif kind == "code":
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(30, 30, 30)
        pdf.set_fill_color(*LIGHT)
        pdf.multi_cell(0, 4.8, s(blk[1]), new_x="LMARGIN", new_y="NEXT", fill=True,
                       border=0)
        pdf.ln(1.5)
    elif kind == "bullets":
        pdf.set_font("Helvetica", "", 10.5)
        pdf.set_text_color(20, 20, 20)
        for item in blk[1]:
            pdf.set_x(pdf.l_margin)
            pdf.cell(5, 5.4, "-")
            pdf.multi_cell(pdf.epw - 5, 5.4, s(item), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1.5)
    elif kind == "table":
        rows, weights = blk[1], blk[2]
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(20, 20, 20)
        with pdf.table(col_widths=weights, headings_style=head,
                       text_align="LEFT", line_height=5.2,
                       borders_layout="SINGLE_TOP_LINE", width=pdf.epw) as table:
            for r in rows:
                row = table.row()
                for cell in r:
                    row.cell(s(cell))
        pdf.ln(2.5)

out = "INTENT-LATITUDE-TAGS-PRODUCT-VIEW.pdf"
pdf.output(out)
print("wrote", out, "pages:", pdf.page_no())

# ---- markdown source (same blocks, keep unicode) ---------------------------
md = []
for blk in BLOCKS:
    k = blk[0]
    if k == "h1":
        md.append(f"# {blk[1]}\n")
    elif k == "sub":
        md.append(f"_{blk[1]}_\n")
    elif k == "h2":
        md.append(f"\n## {blk[1]}\n")
    elif k == "p":
        md.append(f"{blk[1]}\n")
    elif k == "quote":
        md.append(f"> {blk[1]}\n")
    elif k == "code":
        md.append("```text\n" + blk[1] + "\n```\n")
    elif k == "bullets":
        md.append("\n".join(f"- {i}" for i in blk[1]) + "\n")
    elif k == "table":
        rows = blk[1]
        md.append("| " + " | ".join(rows[0]) + " |")
        md.append("| " + " | ".join("---" for _ in rows[0]) + " |")
        for r in rows[1:]:
            md.append("| " + " | ".join(r) + " |")
        md.append("")
with open("INTENT-LATITUDE-TAGS-PRODUCT-VIEW.md", "w") as f:
    f.write("\n".join(md) + "\n")
print("wrote INTENT-LATITUDE-TAGS-PRODUCT-VIEW.md")
