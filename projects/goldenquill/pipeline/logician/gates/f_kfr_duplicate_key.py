"""F-KFR-DUPLICATE-KEY — KFR PRE-write gate (M1 §7.2).

CF-RT-05 closure leg 1 — composite-key uniqueness on
``(who, what, when_period)`` across the active KFR.  Historical
duplicates beyond the active set are admitted (audit trail), but
gate evaluation uses the **most-recent ``when_as_of``** as the
active entry.

Composite key derivation per §7.2.1:
``sha3_512(canonical(who) + "\\0" + canonical(what) + "\\0" +
canonical(when_period))[:24]``.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional, Sequence

from pipeline.logician.canonicalization.kfr_canonical import canonical_dump


F_KFR_DUPLICATE_KEY: Final[str] = "F-KFR-DUPLICATE-KEY"

_NULL_BYTE: Final[bytes] = b"\x00"

# Composite-key length per §7.2.1 — first 24 bytes of SHA3-512.
COMPOSITE_KEY_BYTE_LEN: Final[int] = 24


@dataclass(frozen=True, kw_only=True)
class DuplicateKeyResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    fact_id: Optional[str] = None
    composite_key_hex: Optional[str] = None


def compute_composite_key(fact: Mapping[str, Any]) -> bytes:
    """Composite-key bytes per §7.2.1.

    The three component slots are canonicalized independently then
    concatenated under a NUL separator so two distinct triples cannot
    coincidentally collapse to the same payload.
    """
    parts = (
        canonical_dump(fact.get("who")),
        canonical_dump(fact.get("what")),
        canonical_dump(fact.get("when_period")),
    )
    payload = _NULL_BYTE.join(parts)
    return hashlib.sha3_512(payload).digest()[:COMPOSITE_KEY_BYTE_LEN]


def check_kfr_duplicate_key(
    *,
    fact_id: str,
    candidate_fact: Mapping[str, Any],
    active_facts: Sequence[Mapping[str, Any]],
) -> DuplicateKeyResult:
    """PRE-write gate: refuse a duplicate composite key in the active KFR.

    Parameters
    ----------
    candidate_fact
        The fact being written.
    active_facts
        Facts currently in the active KFR (excluding entries past
        expiry).  The candidate's composite key is compared against
        each.  A self-match (same ``fact_id``) is admitted — re-saving
        the same entry is allowed; only a different ``fact_id`` with
        the same composite key triggers the gate.
    """
    candidate_key = compute_composite_key(candidate_fact)
    candidate_key_hex = candidate_key.hex()
    for existing in active_facts:
        existing_id = existing.get("id") or existing.get("fact_id")
        if existing_id == fact_id:
            continue
        existing_key = compute_composite_key(existing)
        if existing_key == candidate_key:
            return DuplicateKeyResult(
                success=False,
                failure_code=F_KFR_DUPLICATE_KEY,
                detail=(
                    f"composite_key {candidate_key_hex[:16]}… for fact_id="
                    f"{fact_id!r} collides with existing active fact_id="
                    f"{existing_id!r}; (who, what, when_period) tuple "
                    "must be unique in active KFR per §7.2.1"
                ),
                fact_id=fact_id,
                composite_key_hex=candidate_key_hex,
            )
    return DuplicateKeyResult(
        success=True,
        failure_code=None,
        detail=(
            f"composite_key {candidate_key_hex[:16]}… for fact_id="
            f"{fact_id!r} unique across {len(active_facts)} active fact(s)"
        ),
        fact_id=fact_id,
        composite_key_hex=candidate_key_hex,
    )


__all__ = [
    "COMPOSITE_KEY_BYTE_LEN",
    "F_KFR_DUPLICATE_KEY",
    "DuplicateKeyResult",
    "check_kfr_duplicate_key",
    "compute_composite_key",
]
