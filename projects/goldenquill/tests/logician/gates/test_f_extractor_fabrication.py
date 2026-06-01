"""Unit tests for F-EXTRACTOR-FABRICATION (PRE-pre-queue, Law 5, P0).

Per architecture v7.0.4 §5.2 + WS-E §11 LOCK row 185 substrate dispatch.
"""

from __future__ import annotations

import pytest

from pipeline.logician.gates.f_extractor_fabrication import (
    F_EXTRACTOR_FABRICATION,
    MODE_AWARD_INGEST,
    MODE_BULK_INGEST,
    MODE_INCREMENTAL_INGEST,
    PERMITTED_MODES,
    PERMITTED_SUBSTRATES,
    SUBSTRATE_DOCX,
    SUBSTRATE_MARKDOWN,
    SUBSTRATE_PDF,
    CandidateFact,
    check_extractor_fabrication,
)


def test_failure_code_constant() -> None:
    assert F_EXTRACTOR_FABRICATION == "F-EXTRACTOR-FABRICATION"


def test_permitted_modes_constant() -> None:
    assert PERMITTED_MODES == frozenset({
        "BULK_INGEST",
        "INCREMENTAL_INGEST",
        "AWARD_INGEST",
    })


def test_permitted_substrates_constant() -> None:
    assert PERMITTED_SUBSTRATES == frozenset({"PDF", "DOCX", "MARKDOWN"})


def test_invalid_mode_rejected_at_construction() -> None:
    with pytest.raises(ValueError, match="not in"):
        CandidateFact(
            candidate_quote="x",
            source_doc_id="doc",
            mode="WRONG",
            substrate=SUBSTRATE_PDF,
            source_page=1,
        )


def test_invalid_substrate_rejected_at_construction() -> None:
    with pytest.raises(ValueError, match="not in"):
        CandidateFact(
            candidate_quote="x",
            source_doc_id="doc",
            mode=MODE_BULK_INGEST,
            substrate="HTML",
            source_page=1,
        )


# --------------------------------------------------------------------------
# PDF substrate
# --------------------------------------------------------------------------

def test_pdf_verbatim_match_passes() -> None:
    candidate = CandidateFact(
        candidate_quote="The program enrolled 197 graduates in FY25.",
        source_doc_id="annual_report.pdf",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_PDF,
        source_page=12,
    )
    pages = {12: "...background...\n\nThe program enrolled 197 graduates in FY25.\n\n..."}
    r = check_extractor_fabrication(
        candidate=candidate, source_pages=pages
    )
    assert r.success is True
    assert r.matched_at_locator == "page=12"


def test_pdf_unicode_nfc_normalization_passes() -> None:
    # Decomposed cafe (combining acute) vs precomposed in source.
    candidate = CandidateFact(
        candidate_quote="The café served 50 meals daily.",  # cafe + combining acute
        source_doc_id="audit.pdf",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_PDF,
        source_page=3,
    )
    pages = {3: "Other text. The café served 50 meals daily. More text."}  # precomposed é
    r = check_extractor_fabrication(candidate=candidate, source_pages=pages)
    assert r.success is True


def test_pdf_whitespace_collapse_passes() -> None:
    candidate = CandidateFact(
        candidate_quote="enrolled    197    graduates",
        source_doc_id="report.pdf",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_PDF,
        source_page=1,
    )
    pages = {1: "We\tenrolled\n197\tgraduates last year."}
    r = check_extractor_fabrication(candidate=candidate, source_pages=pages)
    assert r.success is True


def test_pdf_ocr_substitution_rejected() -> None:
    # Source has digit "0", quote has letter "O" — not bridged.
    candidate = CandidateFact(
        candidate_quote="EIN 12-3456789O",
        source_doc_id="audit.pdf",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_PDF,
        source_page=1,
    )
    pages = {1: "EIN 12-34567890 is the legal entity identifier."}
    r = check_extractor_fabrication(candidate=candidate, source_pages=pages)
    assert r.success is False
    assert r.failure_code == F_EXTRACTOR_FABRICATION


def test_pdf_page_off_by_one_rejected_in_bulk_ingest() -> None:
    candidate = CandidateFact(
        candidate_quote="197 graduates",
        source_doc_id="report.pdf",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_PDF,
        source_page=12,
    )
    pages = {11: "197 graduates wrong page", 12: "different content here"}
    r = check_extractor_fabrication(candidate=candidate, source_pages=pages)
    assert r.success is False
    assert r.failure_code == F_EXTRACTOR_FABRICATION


def test_pdf_page_off_by_one_rejected_in_incremental_ingest() -> None:
    candidate = CandidateFact(
        candidate_quote="197 graduates",
        source_doc_id="report.pdf",
        mode=MODE_INCREMENTAL_INGEST,
        substrate=SUBSTRATE_PDF,
        source_page=5,
    )
    pages = {4: "197 graduates", 5: "no match here", 6: "197 graduates"}
    r = check_extractor_fabrication(candidate=candidate, source_pages=pages)
    assert r.success is False


def test_pdf_award_ingest_off_by_one_with_flag_passes() -> None:
    candidate = CandidateFact(
        candidate_quote="197 graduates",
        source_doc_id="proposal.pdf",
        mode=MODE_AWARD_INGEST,
        substrate=SUBSTRATE_PDF,
        source_page=12,
        operator_award_page_offset_flag=True,
    )
    pages = {11: "197 graduates moved here on reflow", 12: "different now"}
    r = check_extractor_fabrication(candidate=candidate, source_pages=pages)
    assert r.success is True
    assert "page=11" in r.matched_at_locator


def test_pdf_award_ingest_off_by_one_without_flag_rejected() -> None:
    candidate = CandidateFact(
        candidate_quote="197 graduates",
        source_doc_id="proposal.pdf",
        mode=MODE_AWARD_INGEST,
        substrate=SUBSTRATE_PDF,
        source_page=12,
        operator_award_page_offset_flag=False,
    )
    pages = {11: "197 graduates", 12: "different content"}
    r = check_extractor_fabrication(candidate=candidate, source_pages=pages)
    assert r.success is False


def test_pdf_missing_source_pages_arg_fails() -> None:
    candidate = CandidateFact(
        candidate_quote="x",
        source_doc_id="d",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_PDF,
        source_page=1,
    )
    r = check_extractor_fabrication(candidate=candidate, source_pages=None)
    assert r.success is False
    assert "PDF substrate requires source_pages" in r.detail


def test_pdf_missing_page_locator_fails() -> None:
    candidate = CandidateFact(
        candidate_quote="x",
        source_doc_id="d",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_PDF,
        source_page=None,
    )
    r = check_extractor_fabrication(candidate=candidate, source_pages={1: "x"})
    assert r.success is False
    assert "source_page" in r.detail


# --------------------------------------------------------------------------
# DOCX substrate
# --------------------------------------------------------------------------

def test_docx_verbatim_match_passes() -> None:
    candidate = CandidateFact(
        candidate_quote="The board adopted the policy.",
        source_doc_id="bylaws.docx",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_DOCX,
        source_paragraph_index=4,
    )
    paragraphs = ["intro", "p1", "p2", "p3", "On 2026-01-15: The board adopted the policy. Effective immediately."]
    r = check_extractor_fabrication(
        candidate=candidate, source_paragraphs=paragraphs
    )
    assert r.success is True
    assert r.matched_at_locator == "paragraph=4"


def test_docx_paragraph_out_of_range_fails() -> None:
    candidate = CandidateFact(
        candidate_quote="x",
        source_doc_id="d.docx",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_DOCX,
        source_paragraph_index=99,
    )
    r = check_extractor_fabrication(
        candidate=candidate, source_paragraphs=["only", "two"]
    )
    assert r.success is False
    assert "out of range" in r.detail


def test_docx_quote_in_wrong_paragraph_fails() -> None:
    candidate = CandidateFact(
        candidate_quote="board adopted",
        source_doc_id="bylaws.docx",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_DOCX,
        source_paragraph_index=0,
    )
    paragraphs = ["unrelated content", "the board adopted the policy"]
    r = check_extractor_fabrication(
        candidate=candidate, source_paragraphs=paragraphs
    )
    assert r.success is False


def test_docx_missing_index_fails() -> None:
    candidate = CandidateFact(
        candidate_quote="x",
        source_doc_id="d.docx",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_DOCX,
        source_paragraph_index=None,
    )
    r = check_extractor_fabrication(
        candidate=candidate, source_paragraphs=["x"]
    )
    assert r.success is False


# --------------------------------------------------------------------------
# Markdown substrate
# --------------------------------------------------------------------------

def test_markdown_verbatim_match_passes() -> None:
    candidate = CandidateFact(
        candidate_quote="| Net revenue | $42,000 |",
        source_doc_id="financials.md",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_MARKDOWN,
        source_line=7,
    )
    lines = [
        "# Heading",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        "| Total acres | 12 |",
        "| Gross sales | $50,000 |",
        "| Net revenue | $42,000 |",
        "",
    ]
    r = check_extractor_fabrication(candidate=candidate, source_lines=lines)
    assert r.success is True
    assert r.matched_at_locator == "line=7"


def test_markdown_line_out_of_range_fails() -> None:
    candidate = CandidateFact(
        candidate_quote="x",
        source_doc_id="d.md",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_MARKDOWN,
        source_line=999,
    )
    r = check_extractor_fabrication(
        candidate=candidate, source_lines=["one", "two"]
    )
    assert r.success is False
    assert "out of range" in r.detail


def test_markdown_one_indexed_locator() -> None:
    # Verify 1-based indexing — line=1 should map to lines[0].
    candidate = CandidateFact(
        candidate_quote="first line content",
        source_doc_id="d.md",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_MARKDOWN,
        source_line=1,
    )
    r = check_extractor_fabrication(
        candidate=candidate, source_lines=["first line content", "second"]
    )
    assert r.success is True


# --------------------------------------------------------------------------
# Cross-substrate ellipsis universal rejection
# --------------------------------------------------------------------------

def test_ellipsis_ascii_rejected_universally() -> None:
    candidate = CandidateFact(
        candidate_quote="The program enrolled... 197 graduates",
        source_doc_id="d.pdf",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_PDF,
        source_page=1,
    )
    r = check_extractor_fabrication(
        candidate=candidate,
        source_pages={1: "The program enrolled and produced 197 graduates"},
    )
    assert r.success is False
    assert "ellipsis" in r.detail


def test_ellipsis_unicode_rejected_universally() -> None:
    candidate = CandidateFact(
        candidate_quote="The program… 197 graduates",
        source_doc_id="d.docx",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_DOCX,
        source_paragraph_index=0,
    )
    r = check_extractor_fabrication(
        candidate=candidate,
        source_paragraphs=["The program enrolled 197 graduates"],
    )
    assert r.success is False
    assert "ellipsis" in r.detail


def test_empty_quote_after_normalization_fails() -> None:
    candidate = CandidateFact(
        candidate_quote="    \t\n   ",
        source_doc_id="d.pdf",
        mode=MODE_BULK_INGEST,
        substrate=SUBSTRATE_PDF,
        source_page=1,
    )
    r = check_extractor_fabrication(
        candidate=candidate, source_pages={1: "anything"}
    )
    assert r.success is False
    assert "empty after normalization" in r.detail
