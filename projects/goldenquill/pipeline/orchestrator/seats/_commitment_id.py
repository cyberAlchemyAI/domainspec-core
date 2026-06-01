"""commitment_id safe-identifier sanitization — shared producer/consumer module.

Per §11 v1.1 amendment LOCKED 2026-05-11 (parent_lock_row=185) — relocates
the canonical declaration of the commitment_id safe-identifier contract
from the §14 Report Generator consumer module to a producer-side / shared
sibling module. Both §11 Intake (producer at AWARD_INGEST extraction) and
§14 Report Generator (consumer at filesystem operations + claim_evidence
trace) import from this single canonical home.

The previous canonical home at
``pipeline/orchestrator/seats/report_generator/_commitment_id.py`` is
retained as a backward-compatibility re-export shim so existing §14
LOCK imports (per row 200/201) continue to resolve without modification.

Per §14 v1 LOCK 2026-05-10 Cycle 2 RT-C2-02 closure (verbatim text
preserved here to keep the closure traceable from the canonical home):

> ``commitment_id`` MUST validate against safe-identifier regex
> ``^[A-Z0-9_-]+$`` (uppercase alphanumeric + underscore + hyphen; max
> 64 chars) BEFORE any filesystem operation OR proposal_commitments.yaml
> row admission via §11 v1 PROMOTED-status filter. New sub-tag
> ``F-REPORT-COMMITMENT-MISSED.commitment_id_invalid_format``
> fail-closes at PRE-pre-track-dispatch.

Pure-regex + length predicate. No filesystem access. Callers (the §11
Intake AWARD_INGEST extractor at row admission, §14 Logician gates,
composer modules, waiver-file path constructors) MUST route every
operator-provided OR auto-generated ``commitment_id`` through
``sanitize_commitment_id`` before any subsequent use; rejection raises
``CommitmentIdInvalid`` with the violated rule recorded in the
exception payload.

The regex deliberately rejects lowercase letters, whitespace, path
separators, dots, quotes, and any non-ASCII character — these are the
path-traversal + filesystem-escape vectors RT-C2-02 surfaces. The
``re.ASCII`` flag is set so ``\\d`` cannot match Unicode digit lookalikes
on Python's default unicode-aware ``re`` engine; ``[0-9]`` is already
literal-ASCII so this is defense-in-depth against future predicate
edits.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

# Canonical safe-identifier pattern per RT-C2-02 closure.
SAFE_COMMITMENT_ID_REGEX: Final[str] = r"^[A-Z0-9_-]+$"
SAFE_COMMITMENT_ID_PATTERN: Final[re.Pattern[str]] = re.compile(
    SAFE_COMMITMENT_ID_REGEX, flags=re.ASCII
)

# Length bound per RT-C2-02 closure.
COMMITMENT_ID_MAX_LEN: Final[int] = 64


@dataclass(frozen=True, kw_only=True)
class CommitmentIdInvalid(ValueError):
    """Raised when an operator-supplied commitment_id fails the safe-id contract.

    Carries the offending value (truncated to the max-len bound to keep
    error payloads bounded) and the violated rule name so downstream
    failure-code routers can map to the right sub-tag.
    """

    value: str
    rule: str

    def __post_init__(self) -> None:
        super(ValueError, self).__init__(
            f"commitment_id={self.value!r} violates {self.rule}"
        )


def is_safe_commitment_id(raw: object) -> bool:
    """True iff ``raw`` is a str matching the safe-id regex within the length bound."""
    if not isinstance(raw, str):
        return False
    if not raw:
        return False
    if len(raw) > COMMITMENT_ID_MAX_LEN:
        return False
    return SAFE_COMMITMENT_ID_PATTERN.fullmatch(raw) is not None


def sanitize_commitment_id(raw: object) -> str:
    """Returns ``raw`` unchanged when safe; raises ``CommitmentIdInvalid`` otherwise.

    Three distinct rules surface through the ``rule`` field of the raised
    exception so downstream sub-tag dispatch can route to the right
    failure-code (a single ``not_safe`` rule would lose this signal):

    * ``commitment_id_must_be_str``
    * ``commitment_id_empty_or_too_long``
    * ``commitment_id_regex_mismatch``
    """
    if not isinstance(raw, str):
        raise CommitmentIdInvalid(
            value=repr(raw)[:COMMITMENT_ID_MAX_LEN],
            rule="commitment_id_must_be_str",
        )
    if not raw or len(raw) > COMMITMENT_ID_MAX_LEN:
        raise CommitmentIdInvalid(
            value=raw[:COMMITMENT_ID_MAX_LEN],
            rule="commitment_id_empty_or_too_long",
        )
    if SAFE_COMMITMENT_ID_PATTERN.fullmatch(raw) is None:
        raise CommitmentIdInvalid(
            value=raw[:COMMITMENT_ID_MAX_LEN],
            rule="commitment_id_regex_mismatch",
        )
    return raw


__all__ = [
    "COMMITMENT_ID_MAX_LEN",
    "CommitmentIdInvalid",
    "SAFE_COMMITMENT_ID_PATTERN",
    "SAFE_COMMITMENT_ID_REGEX",
    "is_safe_commitment_id",
    "sanitize_commitment_id",
]
