"""Entailment + paraphrase-flag checks for §14 Report Generator.

Per §14 v1 LOCK 2026-05-10:

* **Cycle 1 RT-1a closure** — per-claim source MUST contain the claim's
  load-bearing keywords / values verbatim where rendered. For
  ``claim_kind: numeric``: source ``source_value`` MUST match claim
  ``claim_value`` EXACTLY in Decimal (per v7.0.4-M1). For
  ``claim_kind: narrative``: heuristic N-gram entailment check —
  claim's content-bearing tokens MUST appear in source text within a
  50-token window.
* **Cycle 2 RT-C2-10 closure** — strict-verbatim path is the primary
  enforcement; the N-gram heuristic is the advisory fallback that
  surfaces operator-decision-required cases. For ``claim_kind:
  narrative``, EITHER (a) the exact claim sentence (after normalization)
  appears verbatim in at least one source ``text`` field, OR (b) the
  operator attached an ``editor_approved_paraphrase: true`` flag to the
  claim_evidence_map entry. The N-gram heuristic continues to surface
  advisory cases.

This module is deterministic-Python. NO LLM call. Logician is
zero-token by §4 v2.2 contract.

The N-gram heuristic uses a simple content-token extraction (lowercase
words minus a small stop-word set) and a sliding-window match. It is
deliberately conservative: more false-positives than false-negatives on
the entailment side, because the verbatim-or-paraphrase-flag mechanism
is the structural enforcement and the N-gram heuristic is the soft
diagnostic.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from decimal import Decimal
from typing import Final, Optional

# Stop-word set for content-token extraction. Deliberately small — we
# want to retain most signal in the claim text. Tuned against
# §14.6.1 (narrative) and §14.6.5 (beneficiary_section) authoring
# patterns; expand at v1.x if at-scale false-positive rate exceeds
# operator tolerance.
_STOP_WORDS: Final[frozenset[str]] = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has",
    "have", "he", "her", "his", "in", "is", "it", "its", "of", "on", "or",
    "she", "than", "that", "the", "their", "them", "they", "this", "to",
    "was", "we", "were", "will", "with", "would",
})

_TOKEN_RE: Final[re.Pattern[str]] = re.compile(r"[a-z0-9]+", re.ASCII)


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class NumericEntailmentResult:
    """Outcome of ``check_numeric_entailment``."""

    success: bool
    detail: str


@dataclass(frozen=True, kw_only=True)
class NarrativeEntailmentResult:
    """Outcome of ``check_narrative_entailment``.

    ``path`` records which branch satisfied the check:

    * ``"verbatim"`` — claim sentence appeared verbatim (normalized) in a source.
    * ``"editor_approved_paraphrase"`` — operator flagged the claim as a
      paraphrase via the ``editor_approved_paraphrase`` per-claim flag.
    * ``"ngram_advisory_only"`` — neither path satisfied; N-gram heuristic
      is the advisory diagnostic.
    """

    success: bool
    path: str
    matched_source_idx: Optional[int]
    ngram_overlap_ratio: float
    detail: str


# ---------------------------------------------------------------------------
# Numeric entailment (RT-1a closure)
# ---------------------------------------------------------------------------


def check_numeric_entailment(
    *,
    claim_value: Decimal,
    source_value: Decimal,
) -> NumericEntailmentResult:
    """Strict Decimal equality per RT-1a closure + v7.0.4-M1 Decimal mandate.

    Both inputs MUST be ``decimal.Decimal``. The defense-in-depth assert
    here mirrors §14.9.4 closure's first-executable-statement Decimal
    assertion in the gate predicate body.

    Raises ``TypeError`` if either argument is not a Decimal — float
    arithmetic in the entailment path is a defect (caught by
    R-REPORT-DECIMAL-MANDATE AST-lint at the gate layer; this Python
    assertion is the runtime defense).
    """
    if not isinstance(claim_value, Decimal):
        raise TypeError(
            f"claim_value must be decimal.Decimal, got {type(claim_value).__name__} "
            f"— float comparison in numeric-entailment path is a defect"
        )
    if not isinstance(source_value, Decimal):
        raise TypeError(
            f"source_value must be decimal.Decimal, got {type(source_value).__name__} "
            f"— float comparison in numeric-entailment path is a defect"
        )
    # Decimal equality: numerically equal AND representational match
    # (Decimal("1.0") == Decimal("1.00") is True; that's intentional for
    # entailment — funder may write 1 and KFR may carry 1.00 and both
    # represent the same actual value).
    if claim_value == source_value:
        return NumericEntailmentResult(
            success=True,
            detail=f"exact-Decimal-match: {claim_value} == {source_value}",
        )
    return NumericEntailmentResult(
        success=False,
        detail=f"Decimal-mismatch: claim={claim_value} source={source_value}",
    )


# ---------------------------------------------------------------------------
# Narrative entailment (RT-1a + RT-C2-10 closure)
# ---------------------------------------------------------------------------


def _normalize_sentence_for_verbatim_match(text: str) -> str:
    """Per RT-C2-10 closure — whitespace + punctuation normalization for
    verbatim claim-sentence match against source ``text`` field.

    Pipeline: NFC → lowercase → strip → collapse whitespace runs → strip
    trailing punctuation. Returns the normalized string.
    """
    nfc = unicodedata.normalize("NFC", text)
    lowered = nfc.lower().strip()
    lowered = " ".join(lowered.split())
    # Strip trailing sentence-terminal punctuation (single pass — claim
    # text may end "...workshops." or "...workshops" identically).
    while lowered and lowered[-1] in ".!?;:":
        lowered = lowered[:-1].rstrip()
    return lowered


def _content_tokens(text: str) -> list[str]:
    """Extract content tokens (lowercase alpha-numeric, minus stop-words)."""
    nfc = unicodedata.normalize("NFC", text).lower()
    raw = _TOKEN_RE.findall(nfc)
    return [tok for tok in raw if tok not in _STOP_WORDS]


def _ngram_window_overlap(
    *,
    claim_tokens: list[str],
    source_tokens: list[str],
    window_tokens: int,
) -> float:
    """Best-window overlap ratio of claim_tokens against any window of
    ``window_tokens`` consecutive tokens in source_tokens.

    Returns the maximum (matched-claim-tokens / total-claim-tokens) ratio
    over all candidate windows. ``0.0`` if claim_tokens is empty or no
    overlap found.
    """
    if not claim_tokens:
        return 0.0
    if not source_tokens:
        return 0.0
    claim_set = set(claim_tokens)
    best = 0
    span = max(window_tokens, len(claim_tokens))
    last_start = max(0, len(source_tokens) - span)
    # Slide window across source_tokens; track best overlap.
    if last_start == 0 and len(source_tokens) <= span:
        window_matches = len(claim_set & set(source_tokens))
        return window_matches / len(claim_tokens)
    for start in range(last_start + 1):
        window = source_tokens[start:start + span]
        overlap = len(claim_set & set(window))
        if overlap > best:
            best = overlap
            if best == len(claim_tokens):
                break
    return best / len(claim_tokens)


def check_narrative_entailment(
    *,
    claim_text: str,
    source_texts: tuple[str, ...],
    editor_approved_paraphrase: bool = False,
    window_tokens: int = 50,
    advisory_overlap_threshold: float = 0.6,
) -> NarrativeEntailmentResult:
    """Narrative entailment per RT-1a + RT-C2-10 closure.

    Path A (verbatim, primary): claim sentence (after normalization)
    appears as a substring of at least one normalized source text. PASS.

    Path B (editor_approved_paraphrase, primary): operator flagged the
    claim as a paraphrase via the per-claim flag. PASS.

    Path C (N-gram advisory): for surfacing operator-decision-required
    cases. Returns PASS only if no other source matches AND ``editor_
    approved_paraphrase=False`` AND N-gram overlap exceeds
    ``advisory_overlap_threshold`` against at least one source. The
    advisory PASS is operator-actionable signal — the gate caller
    typically routes this to a "review" surface rather than to
    ``F-REPORT-COMMITMENT-UNTRACED.narrative_paraphrase_unflagged``.

    No source matches AND no operator paraphrase flag AND N-gram below
    threshold → FAIL with path ``"ngram_advisory_only"``.
    """
    if editor_approved_paraphrase:
        return NarrativeEntailmentResult(
            success=True,
            path="editor_approved_paraphrase",
            matched_source_idx=None,
            ngram_overlap_ratio=1.0,
            detail="operator-flagged paraphrase; verbatim check skipped",
        )

    norm_claim = _normalize_sentence_for_verbatim_match(claim_text)
    if not norm_claim:
        return NarrativeEntailmentResult(
            success=False,
            path="ngram_advisory_only",
            matched_source_idx=None,
            ngram_overlap_ratio=0.0,
            detail="empty claim sentence after normalization",
        )

    # Path A — verbatim substring match.
    for idx, source in enumerate(source_texts):
        norm_source = _normalize_sentence_for_verbatim_match(source)
        if norm_source and norm_claim in norm_source:
            return NarrativeEntailmentResult(
                success=True,
                path="verbatim",
                matched_source_idx=idx,
                ngram_overlap_ratio=1.0,
                detail=f"verbatim match in source[{idx}]",
            )

    # Path C — N-gram heuristic (advisory only, may still fail).
    claim_tokens = _content_tokens(claim_text)
    best_ratio = 0.0
    best_idx: Optional[int] = None
    for idx, source in enumerate(source_texts):
        source_tokens = _content_tokens(source)
        ratio = _ngram_window_overlap(
            claim_tokens=claim_tokens,
            source_tokens=source_tokens,
            window_tokens=window_tokens,
        )
        if ratio > best_ratio:
            best_ratio = ratio
            best_idx = idx

    if best_ratio >= advisory_overlap_threshold:
        return NarrativeEntailmentResult(
            success=True,
            path="ngram_advisory_only",
            matched_source_idx=best_idx,
            ngram_overlap_ratio=best_ratio,
            detail=(
                f"N-gram advisory PASS at overlap={best_ratio:.3f} >= "
                f"threshold={advisory_overlap_threshold:.3f} "
                f"(operator review surface)"
            ),
        )
    return NarrativeEntailmentResult(
        success=False,
        path="ngram_advisory_only",
        matched_source_idx=best_idx,
        ngram_overlap_ratio=best_ratio,
        detail=(
            f"no verbatim match; no paraphrase flag; N-gram overlap "
            f"{best_ratio:.3f} < threshold {advisory_overlap_threshold:.3f}"
        ),
    )


__all__ = [
    "NarrativeEntailmentResult",
    "NumericEntailmentResult",
    "check_narrative_entailment",
    "check_numeric_entailment",
]
