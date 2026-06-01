"""pipeline.seats.scribe.smart — §7.6 SMART outcome primitive + numeric-verbatim helpers.

Blueprint §7 Scribe v1.1.1 §7.6 LOCKED 2026-04-21. Pure-deterministic
shape + validator + string-extraction helpers. Zero I/O, zero LLM, zero
external-package imports.

R2 ships the evidence-producing helpers (``extract_numeric_tokens``,
``check_numeric_verbatim``) that R3 Logician POST-gate
``F-SCRIBE-PARAPHRASED-NUMERIC`` + ``F-SCRIBE-SMART-INVENTED-METRIC`` will
consume. R2 DOES NOT fire the failure code — it produces the deltas that
R3 turns into failures.

§7.6 closed-set contract:
- SmartObjective carries 5 SMART dimensions (objective / outcome /
  measurement / timeline / achievability) + `relevance_pointer`.
- `validate_smart_objective` returns a tuple of violation codes — empty
  tuple is the VALID state.
- `extract_numeric_tokens` canonicalizes money, percent, decimal, integer.
- `check_numeric_verbatim` returns tokens in claim missing from evidence.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final


# ---------------------------------------------------------------------------
# Shape — SmartObjective
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class SmartObjective:
    """§7.6 SMART dimensions + RFA-criterion relevance pointer.

    ``relevance_pointer`` may be empty at construction (drafter has not yet
    assigned an evaluation-criterion mapping); R3 POST-gate
    ``F-SCRIBE-EVALUATION-CRITERION-MISSING`` catches the full-draft
    exhaustiveness violation.

    The five SMART text fields MUST be non-empty non-whitespace strings.
    """

    objective_text: str
    outcome_text: str
    measurement_text: str
    timeline_text: str
    achievability_evidence: str
    relevance_pointer: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "objective_text",
            "outcome_text",
            "measurement_text",
            "timeline_text",
            "achievability_evidence",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"SmartObjective.{name} must be a non-empty string; "
                    f"got {value!r}."
                )


# ---------------------------------------------------------------------------
# Validator — returns violation-code tuple (empty tuple = VALID)
# ---------------------------------------------------------------------------


# Violation-code closed set. R3 maps each to a Logician POST-gate code.
VIOLATION_MISSING_OBJECTIVE: Final[str] = "smart.missing_objective"
VIOLATION_MISSING_OUTCOME: Final[str] = "smart.missing_outcome"
VIOLATION_MISSING_MEASUREMENT: Final[str] = "smart.missing_measurement"
VIOLATION_MISSING_TIMELINE: Final[str] = "smart.missing_timeline"
VIOLATION_MISSING_ACHIEVABILITY: Final[str] = "smart.missing_achievability"
VIOLATION_NO_RELEVANCE_POINTER: Final[str] = "smart.no_relevance_pointer"


def validate_smart_objective(obj: SmartObjective) -> tuple[str, ...]:
    """Return tuple of violation codes; empty tuple means valid.

    Construction already enforces the 5 SMART text fields non-empty, so
    those violation codes surface only if the caller reads a
    ``SmartObjective`` whose shape was bypassed via ``object.__setattr__``
    (OUT-OF-MODEL) and fed back in. Relevance-pointer absence is a
    draft-quality warning, not a construction error — returned here so R3
    can decide POST-gate severity.
    """
    violations: list[str] = []
    if not obj.objective_text.strip():
        violations.append(VIOLATION_MISSING_OBJECTIVE)
    if not obj.outcome_text.strip():
        violations.append(VIOLATION_MISSING_OUTCOME)
    if not obj.measurement_text.strip():
        violations.append(VIOLATION_MISSING_MEASUREMENT)
    if not obj.timeline_text.strip():
        violations.append(VIOLATION_MISSING_TIMELINE)
    if not obj.achievability_evidence.strip():
        violations.append(VIOLATION_MISSING_ACHIEVABILITY)
    if len(obj.relevance_pointer) == 0:
        violations.append(VIOLATION_NO_RELEVANCE_POINTER)
    return tuple(violations)


# ---------------------------------------------------------------------------
# Numeric-verbatim helpers (§7.6 invariant)
# ---------------------------------------------------------------------------


# Matches in priority order: money, percent, decimal, integer. Each match
# returns a canonicalized form:
#   $1,200 / $1200     → "1200"
#   $12.50             → "12.50"
#   75%                → "75"
#   75.5%              → "75.5"
#   12.50              → "12.50"
#   12,000             → "12000"
#   12                 → "12"
_MONEY_RE: Final[re.Pattern[str]] = re.compile(
    r"\$\s*([0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)(\.[0-9]+)?"
)
_PERCENT_RE: Final[re.Pattern[str]] = re.compile(
    r"([0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)(\.[0-9]+)?\s*%"
)
_DECIMAL_RE: Final[re.Pattern[str]] = re.compile(
    r"(?<![0-9.])([0-9]+\.[0-9]+)(?![0-9.])"
)
_INTEGER_WITH_COMMAS_RE: Final[re.Pattern[str]] = re.compile(
    r"(?<![0-9.])([0-9]{1,3}(?:,[0-9]{3})+)(?!\.[0-9])(?![0-9])"
)
_INTEGER_RE: Final[re.Pattern[str]] = re.compile(
    r"(?<![0-9.,])([0-9]+)(?![0-9.,])"
)


def _canonical_number(raw: str) -> str:
    """Strip commas, whitespace, leading $, trailing %; keep decimal."""
    s = raw.strip().lstrip("$").rstrip("%").strip()
    s = s.replace(",", "")
    return s


def extract_numeric_tokens(text: str) -> tuple[str, ...]:
    """Return canonical-form numeric tokens in document-order.

    §7.6 numeric-verbatim basis. Canonical forms:
    - Money: ``$1,200.00`` → ``"1200.00"``
    - Percent: ``75%`` → ``"75"``, ``75.5%`` → ``"75.5"``
    - Decimal: ``12.5`` → ``"12.5"``
    - Integer: ``12,000`` → ``"12000"``, ``12`` → ``"12"``

    Multiple occurrences of the same token are preserved (duplicates kept
    in order). Empty / non-numeric input returns ``()``.
    """
    if not isinstance(text, str) or not text:
        return ()

    # Walk the text left-to-right with a priority pattern. We annotate
    # spans to avoid double-matching (e.g., the "12" inside "$12.50" must
    # only produce "12.50" once).
    claimed: list[tuple[int, int, str]] = []  # (start, end, canonical)

    def _claim(match: re.Match[str], canonical: str) -> None:
        start, end = match.span()
        # Skip if overlaps an already-claimed span.
        for s, e, _ in claimed:
            if not (end <= s or start >= e):
                return
        claimed.append((start, end, canonical))

    for m in _MONEY_RE.finditer(text):
        frac = m.group(2) or ""
        _claim(m, _canonical_number(m.group(1)) + frac)
    for m in _PERCENT_RE.finditer(text):
        frac = m.group(2) or ""
        _claim(m, _canonical_number(m.group(1)) + frac)
    for m in _DECIMAL_RE.finditer(text):
        _claim(m, m.group(1))
    for m in _INTEGER_WITH_COMMAS_RE.finditer(text):
        _claim(m, _canonical_number(m.group(1)))
    for m in _INTEGER_RE.finditer(text):
        _claim(m, m.group(1))

    claimed.sort(key=lambda t: t[0])
    return tuple(c for _, _, c in claimed)


def check_numeric_verbatim(
    claim_text: str,
    evidence_text: str,
) -> tuple[str, ...]:
    """Return tokens in ``claim_text`` that are NOT present in
    ``evidence_text`` (after canonicalization).

    Empty tuple = every numeric in the claim appears byte-identical in the
    evidence. §7.6 numeric-verbatim invariant basis.
    """
    claim_tokens = extract_numeric_tokens(claim_text)
    evidence_tokens = set(extract_numeric_tokens(evidence_text))
    return tuple(t for t in claim_tokens if t not in evidence_tokens)


__all__ = [
    "SmartObjective",
    "validate_smart_objective",
    "extract_numeric_tokens",
    "check_numeric_verbatim",
    "VIOLATION_MISSING_OBJECTIVE",
    "VIOLATION_MISSING_OUTCOME",
    "VIOLATION_MISSING_MEASUREMENT",
    "VIOLATION_MISSING_TIMELINE",
    "VIOLATION_MISSING_ACHIEVABILITY",
    "VIOLATION_NO_RELEVANCE_POINTER",
]
