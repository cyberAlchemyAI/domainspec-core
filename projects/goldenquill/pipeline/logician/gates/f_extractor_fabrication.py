"""F-EXTRACTOR-FABRICATION — PRE-pre-queue gate (Law 5 fabrication, P0).

Per architecture v7.0.4 §5.2 + WS-E §11 LOCK row 185 substrate dispatch.

Intake's deterministic post-processor validates a candidate fact's
``source_quote`` against the indicated ``source_doc`` slice (page /
paragraph / line, depending on substrate) BEFORE the candidate enters
``orgs/<slug>/vault/kfr/pending_facts.yaml`` for operator review.

Substrate dispatch (mode-immutable from input dataclass)
--------------------------------------------------------
* ``PDF``      — quote must literally appear at the indicated page;
                 page-off-by-one is REJECTED in BULK_INGEST and
                 INCREMENTAL_INGEST and only allowed in AWARD_INGEST
                 with ``operator_award_page_offset_flag=True`` (proposal
                 documents may reflow when re-rendered post-submit).
* ``DOCX``     — quote must literally appear at the indicated paragraph
                 index within the source document.
* ``MARKDOWN`` — quote must literally appear at the indicated single
                 line (line indices are 1-based per WS-E §11).

Allowable normalization (PASS — applied symmetrically to quote + source)
------------------------------------------------------------------------
* Unicode NFC normalization on both sides.
* Whitespace runs ``[\\t\\n\\r\\f\\v ]+`` collapse to a single ASCII
  space; leading/trailing whitespace stripped.

REJECTED (treated as fabrication, fail-closed)
----------------------------------------------
* OCR-substitution mapping (``0`` ↔ ``O``, ``1`` ↔ ``l``, ``5`` ↔ ``S``,
  etc.) — ambiguous OCR bytes must be re-OCR'd by operator before
  Intake processes them. Detected by checking for an exact-after-
  normalization match; OCR-substituted variants do not normalize
  identically and therefore fail the verbatim test.
* Page-off-by-one in BULK_INGEST / INCREMENTAL_INGEST.
* Substring-of-claim with ellipsis (``...``) — quote must literally
  span start-to-end of the asserted source bytes. The gate flags any
  candidate quote containing an ellipsis token as fabrication.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Final, Mapping, Optional, Sequence


F_EXTRACTOR_FABRICATION: Final[str] = "F-EXTRACTOR-FABRICATION"

# Mode constants — mode-immutable per dispatch directive.
MODE_BULK_INGEST: Final[str] = "BULK_INGEST"
MODE_INCREMENTAL_INGEST: Final[str] = "INCREMENTAL_INGEST"
MODE_AWARD_INGEST: Final[str] = "AWARD_INGEST"
PERMITTED_MODES: Final[frozenset[str]] = frozenset({
    MODE_BULK_INGEST,
    MODE_INCREMENTAL_INGEST,
    MODE_AWARD_INGEST,
})

# Substrate constants — substrate-immutable per WS-E §11 LOCK row 185.
SUBSTRATE_PDF: Final[str] = "PDF"
SUBSTRATE_DOCX: Final[str] = "DOCX"
SUBSTRATE_MARKDOWN: Final[str] = "MARKDOWN"
PERMITTED_SUBSTRATES: Final[frozenset[str]] = frozenset({
    SUBSTRATE_PDF,
    SUBSTRATE_DOCX,
    SUBSTRATE_MARKDOWN,
})

# Whitespace collapse pattern per RFC 3066 / W3C XML Information Set.
_WHITESPACE_RE: Final[re.Pattern[str]] = re.compile(r"[\t\n\r\f\v ]+")

# Ellipsis tokens — Unicode "…" (U+2026) and ASCII "..." both rejected.
_ELLIPSIS_TOKENS: Final[tuple[str, ...]] = ("…", "...")


@dataclass(frozen=True, kw_only=True)
class CandidateFact:
    """Input dataclass — mode and substrate immutable post-construction.

    The dispatch keys (``mode``, ``substrate``) are required; downstream
    routing depends on them and the gate fail-closes if either is absent
    or outside the permitted enum.
    """

    candidate_quote: str
    source_doc_id: str
    mode: str
    substrate: str
    # Substrate-specific locator. Exactly one of these must be supplied
    # per the substrate enum:
    #   PDF      → source_page (1-based)
    #   DOCX     → source_paragraph_index (0-based)
    #   MARKDOWN → source_line (1-based)
    source_page: Optional[int] = None
    source_paragraph_index: Optional[int] = None
    source_line: Optional[int] = None
    # AWARD_INGEST + PDF only: operator-flagged ±1 page tolerance.
    operator_award_page_offset_flag: bool = False

    def __post_init__(self) -> None:
        if self.mode not in PERMITTED_MODES:
            raise ValueError(
                f"CandidateFact.mode={self.mode!r} not in "
                f"{sorted(PERMITTED_MODES)!r}"
            )
        if self.substrate not in PERMITTED_SUBSTRATES:
            raise ValueError(
                f"CandidateFact.substrate={self.substrate!r} not in "
                f"{sorted(PERMITTED_SUBSTRATES)!r}"
            )


@dataclass(frozen=True, kw_only=True)
class ExtractorFabricationResult:
    """Result of F-EXTRACTOR-FABRICATION check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    matched_at_locator: Optional[str] = None


def _normalize(text: str) -> str:
    """Symmetric normalization: Unicode NFC + whitespace collapse + strip."""
    nfc = unicodedata.normalize("NFC", text)
    collapsed = _WHITESPACE_RE.sub(" ", nfc)
    return collapsed.strip()


def _contains_ellipsis(quote: str) -> bool:
    return any(token in quote for token in _ELLIPSIS_TOKENS)


def _check_pdf(
    candidate: CandidateFact,
    source_pages: Mapping[int, str],
) -> ExtractorFabricationResult:
    """PDF: unique-page-match per WS-E §11.9.1.A.

    BULK_INGEST + INCREMENTAL_INGEST: quote must appear at exactly the
    indicated ``source_page``; off-by-one is fabrication.

    AWARD_INGEST + ``operator_award_page_offset_flag=True``: ±1 page
    tolerance allowed (page p, p-1, p+1 all admissible).
    """
    page = candidate.source_page
    if page is None:
        return ExtractorFabricationResult(
            success=False,
            failure_code=F_EXTRACTOR_FABRICATION,
            detail="PDF substrate requires source_page locator (got None)",
        )

    normalized_quote = _normalize(candidate.candidate_quote)
    if not normalized_quote:
        return ExtractorFabricationResult(
            success=False,
            failure_code=F_EXTRACTOR_FABRICATION,
            detail="candidate_quote empty after normalization",
        )

    # Determine candidate page set per mode + substrate.
    if (
        candidate.mode == MODE_AWARD_INGEST
        and candidate.operator_award_page_offset_flag
    ):
        candidate_pages: tuple[int, ...] = (page - 1, page, page + 1)
    else:
        candidate_pages = (page,)

    for p in candidate_pages:
        page_text = source_pages.get(p)
        if page_text is None:
            continue
        if normalized_quote in _normalize(page_text):
            return ExtractorFabricationResult(
                success=True,
                failure_code=None,
                detail=(
                    f"quote verbatim-matches source_doc {candidate.source_doc_id!r} "
                    f"at page {p}"
                ),
                matched_at_locator=f"page={p}",
            )

    return ExtractorFabricationResult(
        success=False,
        failure_code=F_EXTRACTOR_FABRICATION,
        detail=(
            f"quote does not verbatim-match source_doc {candidate.source_doc_id!r} "
            f"at page {page}"
            + (
                " (±1 tolerance applied)"
                if (
                    candidate.mode == MODE_AWARD_INGEST
                    and candidate.operator_award_page_offset_flag
                )
                else ""
            )
        ),
    )


def _check_docx(
    candidate: CandidateFact,
    source_paragraphs: Sequence[str],
) -> ExtractorFabricationResult:
    """DOCX: paragraph-index per WS-E §11.9.1.B.

    Quote must verbatim-match within the indicated paragraph (no
    cross-paragraph spanning, no ±1 tolerance — DOCX paragraph indices
    are stable).
    """
    idx = candidate.source_paragraph_index
    if idx is None:
        return ExtractorFabricationResult(
            success=False,
            failure_code=F_EXTRACTOR_FABRICATION,
            detail="DOCX substrate requires source_paragraph_index locator (got None)",
        )
    if idx < 0 or idx >= len(source_paragraphs):
        return ExtractorFabricationResult(
            success=False,
            failure_code=F_EXTRACTOR_FABRICATION,
            detail=(
                f"source_paragraph_index={idx} out of range "
                f"[0, {len(source_paragraphs)}) for source_doc "
                f"{candidate.source_doc_id!r}"
            ),
        )

    normalized_quote = _normalize(candidate.candidate_quote)
    if not normalized_quote:
        return ExtractorFabricationResult(
            success=False,
            failure_code=F_EXTRACTOR_FABRICATION,
            detail="candidate_quote empty after normalization",
        )
    paragraph_text = _normalize(source_paragraphs[idx])
    if normalized_quote in paragraph_text:
        return ExtractorFabricationResult(
            success=True,
            failure_code=None,
            detail=(
                f"quote verbatim-matches source_doc {candidate.source_doc_id!r} "
                f"at paragraph {idx}"
            ),
            matched_at_locator=f"paragraph={idx}",
        )
    return ExtractorFabricationResult(
        success=False,
        failure_code=F_EXTRACTOR_FABRICATION,
        detail=(
            f"quote does not verbatim-match source_doc {candidate.source_doc_id!r} "
            f"at paragraph {idx}"
        ),
    )


def _check_markdown(
    candidate: CandidateFact,
    source_lines: Sequence[str],
) -> ExtractorFabricationResult:
    """Markdown: single-line per WS-E §11.9.1.C.

    Markdown line indices are 1-based per WS-E spec; quote must
    verbatim-match within the indicated single line (no cross-line
    spanning).
    """
    line = candidate.source_line
    if line is None:
        return ExtractorFabricationResult(
            success=False,
            failure_code=F_EXTRACTOR_FABRICATION,
            detail="MARKDOWN substrate requires source_line locator (got None)",
        )
    zero_idx = line - 1
    if zero_idx < 0 or zero_idx >= len(source_lines):
        return ExtractorFabricationResult(
            success=False,
            failure_code=F_EXTRACTOR_FABRICATION,
            detail=(
                f"source_line={line} (1-based) out of range "
                f"[1, {len(source_lines) + 1}) for source_doc "
                f"{candidate.source_doc_id!r}"
            ),
        )

    normalized_quote = _normalize(candidate.candidate_quote)
    if not normalized_quote:
        return ExtractorFabricationResult(
            success=False,
            failure_code=F_EXTRACTOR_FABRICATION,
            detail="candidate_quote empty after normalization",
        )
    line_text = _normalize(source_lines[zero_idx])
    if normalized_quote in line_text:
        return ExtractorFabricationResult(
            success=True,
            failure_code=None,
            detail=(
                f"quote verbatim-matches source_doc {candidate.source_doc_id!r} "
                f"at line {line}"
            ),
            matched_at_locator=f"line={line}",
        )
    return ExtractorFabricationResult(
        success=False,
        failure_code=F_EXTRACTOR_FABRICATION,
        detail=(
            f"quote does not verbatim-match source_doc {candidate.source_doc_id!r} "
            f"at line {line}"
        ),
    )


def check_extractor_fabrication(
    *,
    candidate: CandidateFact,
    source_pages: Optional[Mapping[int, str]] = None,
    source_paragraphs: Optional[Sequence[str]] = None,
    source_lines: Optional[Sequence[str]] = None,
) -> ExtractorFabricationResult:
    """PRE-pre-queue gate: substrate-dispatched verbatim-match check.

    Ellipsis-substring is rejected universally before substrate dispatch.
    The caller supplies only the substrate-relevant source slice; other
    arguments may be None.

    Parameters
    ----------
    candidate
        :class:`CandidateFact` with mode + substrate dispatch keys.
    source_pages
        PDF substrate: mapping ``{page_number: page_text}``. 1-based.
    source_paragraphs
        DOCX substrate: ordered sequence of paragraph texts. 0-based.
    source_lines
        MARKDOWN substrate: ordered sequence of line texts. The
        ``source_line`` locator is 1-based per WS-E §11.9.1.C.

    Returns
    -------
    ExtractorFabricationResult. Passes iff the candidate quote
    verbatim-matches the indicated source slice under the symmetric
    normalization rules. Fails on missing locator, out-of-range index,
    ellipsis-bearing quote, or any miss.
    """
    # Ellipsis universally rejected before substrate dispatch — quote
    # must literally span start-to-end of asserted source bytes per
    # §5.2 REJECTED clause.
    if _contains_ellipsis(candidate.candidate_quote):
        return ExtractorFabricationResult(
            success=False,
            failure_code=F_EXTRACTOR_FABRICATION,
            detail=(
                "candidate_quote contains ellipsis token — quote must "
                "literally span source bytes start-to-end (no substring "
                "elision permitted under §5.2 REJECTED clause)"
            ),
        )

    if candidate.substrate == SUBSTRATE_PDF:
        if source_pages is None:
            return ExtractorFabricationResult(
                success=False,
                failure_code=F_EXTRACTOR_FABRICATION,
                detail="PDF substrate requires source_pages mapping (got None)",
            )
        return _check_pdf(candidate, source_pages)
    if candidate.substrate == SUBSTRATE_DOCX:
        if source_paragraphs is None:
            return ExtractorFabricationResult(
                success=False,
                failure_code=F_EXTRACTOR_FABRICATION,
                detail="DOCX substrate requires source_paragraphs sequence (got None)",
            )
        return _check_docx(candidate, source_paragraphs)
    if candidate.substrate == SUBSTRATE_MARKDOWN:
        if source_lines is None:
            return ExtractorFabricationResult(
                success=False,
                failure_code=F_EXTRACTOR_FABRICATION,
                detail="MARKDOWN substrate requires source_lines sequence (got None)",
            )
        return _check_markdown(candidate, source_lines)

    # Unreachable under PERMITTED_SUBSTRATES enum guard — defensive.
    return ExtractorFabricationResult(
        success=False,
        failure_code=F_EXTRACTOR_FABRICATION,
        detail=f"unsupported substrate {candidate.substrate!r}",
    )


__all__ = [
    "F_EXTRACTOR_FABRICATION",
    "MODE_AWARD_INGEST",
    "MODE_BULK_INGEST",
    "MODE_INCREMENTAL_INGEST",
    "PERMITTED_MODES",
    "PERMITTED_SUBSTRATES",
    "SUBSTRATE_DOCX",
    "SUBSTRATE_MARKDOWN",
    "SUBSTRATE_PDF",
    "CandidateFact",
    "ExtractorFabricationResult",
    "check_extractor_fabrication",
]
