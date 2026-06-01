"""F-VERDICT-CITATION-MISSING (F-AMDT-03) — POST-gate on Judge verdict ingest.

Judge verdicts carry per-dimension scores. Each scored dimension must cite
evidence from the draft under review. Without this gate, Judge scores could
float free of draft content — arbitrary numbers with fabricated or absent
evidence would pass silently. The gate mechanically enforces that every
scored dimension has an ``evidence`` string whose whitespace-delimited
tokens ALL appear verbatim (case-sensitive substring) in the draft text.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(parent LOCK); v2.2 delta row for F-AMDT-03 (Wave 1, no external deps).

Semantics (spec card v1, 2026-04-20):
  * Gate ordering: runs AFTER F-VERDICT-BLOCKING-MISSING on the same
    verdict; the caller (gate_runner) is responsible for sequencing.
  * Draft access via injected ``DraftReaderCallable`` (E-017 pattern) —
    the gate never opens a file directly (AST-lint R3).
  * Reader exception → fail-closed with ``reader_raised`` detail.
  * Structural errors (no ``dimensions`` key, non-list dimensions, non-dict
    entry) → fail-closed with a structural reason tag.
  * Per-dimension evidence missing / non-string / empty / non-resolving →
    fail-closed with ``F-AMDT-03`` and populated ``failed_dimensions``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Failure-code constant (blueprint §6 v2.2 delta)
# ---------------------------------------------------------------------------


F_AMDT_03: str = "F-AMDT-03"


_DETAIL_VERDICT_NOT_DICT: str = "verdict_not_dict"
_DETAIL_DIMENSIONS_ABSENT: str = "dimensions_key_absent"
_DETAIL_DIMENSIONS_NOT_LIST: str = "dimensions_not_list"
_DETAIL_READER_RAISED: str = "draft_reader_raised"
_DETAIL_TOKENS_UNRESOLVED: str = "evidence_tokens_unresolved"

_DIM_REASON_NOT_DICT: str = "dimension_entry_not_dict"
_DIM_REASON_EVIDENCE_ABSENT: str = "evidence_key_absent"
_DIM_REASON_EVIDENCE_NOT_STRING: str = "evidence_not_string"
_DIM_REASON_EVIDENCE_EMPTY: str = "evidence_empty"
_DIM_REASON_EVIDENCE_WHITESPACE_ONLY: str = "evidence_whitespace_only"
_DIM_REASON_TOKENS_UNRESOLVED: str = "evidence_tokens_unresolved"


# ---------------------------------------------------------------------------
# Injected Protocol (E-017 pattern)
# ---------------------------------------------------------------------------


@runtime_checkable
class DraftReaderCallable(Protocol):
    """Returns the full text of the draft at ``draft_path``.

    Callers inject a concrete reader that performs the actual file I/O.
    The gate never calls ``open()`` — AST-lint R3 LOGICIAN_OPEN_BAN.
    """

    def __call__(self, draft_path: str) -> str: ...


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class DimensionCitationFailure:
    dimension_index: int
    dimension_name: Optional[str]
    reason_tag: str
    missing_tokens: tuple[str, ...]


@dataclass(frozen=True, kw_only=True)
class CitationMissingDetail:
    reason_tag: str
    failed_dimensions: tuple[DimensionCitationFailure, ...]
    reader_error: Optional[str]


@dataclass(frozen=True, kw_only=True)
class CitationMissingResult:
    success: bool
    failure_code: Optional[str]
    detail: Optional[CitationMissingDetail]


# ---------------------------------------------------------------------------
# Gate predicate
# ---------------------------------------------------------------------------


def _structural_fail(
    *, reason_tag: str, reader_error: Optional[str] = None
) -> CitationMissingResult:
    return CitationMissingResult(
        success=False,
        failure_code=F_AMDT_03,
        detail=CitationMissingDetail(
            reason_tag=reason_tag,
            failed_dimensions=(),
            reader_error=reader_error,
        ),
    )


def _check_single_dimension(
    *, index: int, entry: object, draft_text: str
) -> Optional[DimensionCitationFailure]:
    if not isinstance(entry, dict):
        return DimensionCitationFailure(
            dimension_index=index,
            dimension_name=None,
            reason_tag=_DIM_REASON_NOT_DICT,
            missing_tokens=(),
        )

    dim_name_raw = entry.get("name")
    dim_name: Optional[str] = dim_name_raw if isinstance(dim_name_raw, str) else None

    if "evidence" not in entry:
        return DimensionCitationFailure(
            dimension_index=index,
            dimension_name=dim_name,
            reason_tag=_DIM_REASON_EVIDENCE_ABSENT,
            missing_tokens=(),
        )

    evidence = entry["evidence"]
    if not isinstance(evidence, str):
        return DimensionCitationFailure(
            dimension_index=index,
            dimension_name=dim_name,
            reason_tag=_DIM_REASON_EVIDENCE_NOT_STRING,
            missing_tokens=(),
        )

    if evidence == "":
        return DimensionCitationFailure(
            dimension_index=index,
            dimension_name=dim_name,
            reason_tag=_DIM_REASON_EVIDENCE_EMPTY,
            missing_tokens=(),
        )

    tokens = evidence.split()
    if not tokens:
        return DimensionCitationFailure(
            dimension_index=index,
            dimension_name=dim_name,
            reason_tag=_DIM_REASON_EVIDENCE_WHITESPACE_ONLY,
            missing_tokens=(),
        )

    missing = tuple(tok for tok in tokens if tok not in draft_text)
    if missing:
        return DimensionCitationFailure(
            dimension_index=index,
            dimension_name=dim_name,
            reason_tag=_DIM_REASON_TOKENS_UNRESOLVED,
            missing_tokens=missing,
        )
    return None


def check_verdict_citations(
    *,
    verdict_json: object,
    draft_path: str,
    draft_reader: DraftReaderCallable,
) -> CitationMissingResult:
    """POST-gate F-VERDICT-CITATION-MISSING (F-AMDT-03).

    Args:
      verdict_json: Judge's parsed verdict. Must be a ``dict`` containing a
        ``"dimensions"`` key whose value is a list of per-dimension entries,
        each a dict containing an ``"evidence"`` string.
      draft_path: path to the draft under review. Passed verbatim to the
        injected reader; the gate does not inspect or normalise it.
      draft_reader: injected callable that returns the full draft text.

    Returns:
      ``CitationMissingResult`` — PASS iff every dimension's evidence
      tokens resolve against the draft via case-sensitive substring match.
    """
    if not isinstance(verdict_json, dict):
        return _structural_fail(reason_tag=_DETAIL_VERDICT_NOT_DICT)

    if "dimensions" not in verdict_json:
        return _structural_fail(reason_tag=_DETAIL_DIMENSIONS_ABSENT)

    dimensions = verdict_json["dimensions"]
    if not isinstance(dimensions, list):
        return _structural_fail(reason_tag=_DETAIL_DIMENSIONS_NOT_LIST)

    try:
        draft_text = draft_reader(draft_path)
    except Exception as exc:  # fail-closed per spec
        return _structural_fail(
            reason_tag=_DETAIL_READER_RAISED,
            reader_error=f"{type(exc).__name__}: {exc}"[:500],
        )

    if not isinstance(draft_text, str):
        return _structural_fail(
            reason_tag=_DETAIL_READER_RAISED,
            reader_error=f"draft_reader returned {type(draft_text).__name__}, expected str",
        )

    failures: list[DimensionCitationFailure] = []
    for i, entry in enumerate(dimensions):
        f = _check_single_dimension(index=i, entry=entry, draft_text=draft_text)
        if f is not None:
            failures.append(f)

    if failures:
        return CitationMissingResult(
            success=False,
            failure_code=F_AMDT_03,
            detail=CitationMissingDetail(
                reason_tag=_DETAIL_TOKENS_UNRESOLVED,
                failed_dimensions=tuple(failures),
                reader_error=None,
            ),
        )

    return CitationMissingResult(success=True, failure_code=None, detail=None)
