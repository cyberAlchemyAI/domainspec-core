"""F-KFR-TAG-MODIFIED — KFR PRE-write gate (M1 §4 / §4.2 / §4.4).

CF-RT-04 closure.  Removing a ``required_for_funder`` tag silently
disables the §3.2 NEEDED hard-block.  The gate ships a tamper event
analog of §4.4 tolerance-widening: any modification of the tracked
metadata fields requires an admin-risk-ledger entry with
operator signature.

Tracked fields (per §4.2):

* ``required_for_category``
* ``required_for_funder``
* ``key_credentials`` (presence + key set)

Disk-state SHA3-512 hash comparison per §4.2.1.  The hash covers a
canonicalized tag-payload tuple so semantically equal tag sets hash
identically across loaders.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional, Sequence

from pipeline.logician.canonicalization.kfr_canonical import canonical_dump


F_KFR_TAG_MODIFIED: Final[str] = "F-KFR-TAG-MODIFIED"

LEDGER_KIND_TAG_MODIFIED: Final[str] = "kfr_tag_modified"

# Canonical tracked fields per §4.2.
TRACKED_TAG_FIELDS: Final[tuple[str, ...]] = (
    "required_for_category",
    "required_for_funder",
)


@dataclass(frozen=True, kw_only=True)
class TagModifiedResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    fact_id: Optional[str] = None
    tag_set_hash_before: Optional[str] = None
    tag_set_hash_after: Optional[str] = None


def compute_tag_set_hash(fact: Mapping[str, Any]) -> bytes:
    """SHA3-512 over canonical tag-set payload per §4.2.1.

    Members of each tag list are sorted (string-NFC + lex order) so
    semantically equal tag sets hash identically.
    """
    if not isinstance(fact, Mapping):
        raise TypeError(
            f"compute_tag_set_hash expects mapping, got {type(fact).__name__}"
        )
    payload = {
        "fact_id": str(fact.get("id") or fact.get("fact_id") or ""),
        "required_for_category": sorted(
            str(t) for t in (fact.get("required_for_category") or [])
        ),
        "required_for_funder": sorted(
            str(t) for t in (fact.get("required_for_funder") or [])
        ),
        "key_credentials_present": fact.get("key_credentials") is not None,
        "key_credentials_keys": sorted(
            str(k) for k in (fact.get("key_credentials") or {}).keys()
        ),
    }
    canonical = canonical_dump(payload)
    return hashlib.sha3_512(canonical).digest()


def _has_signed_tag_ledger_entry(
    ledger_entries: Sequence[Mapping[str, Any]],
    *,
    fact_id: str,
    hash_before: str,
    hash_after: str,
) -> bool:
    for row in ledger_entries:
        if not isinstance(row, Mapping):
            continue
        if row.get("ledger_kind") != LEDGER_KIND_TAG_MODIFIED:
            continue
        if row.get("fact_id") != fact_id:
            continue
        if row.get("tag_set_hash_before") != hash_before:
            continue
        if row.get("tag_set_hash_after") != hash_after:
            continue
        signed = row.get("signed_at_utc")
        operator_key = row.get("operator_key_id")
        rationale = row.get("rationale")
        if not isinstance(signed, str) or not signed.strip():
            continue
        if not isinstance(operator_key, str) or not operator_key.strip():
            continue
        if not isinstance(rationale, str) or not rationale.strip():
            continue
        return True
    return False


def check_kfr_tag_modified(
    *,
    fact_id: str,
    fact_before: Mapping[str, Any],
    fact_after: Mapping[str, Any],
    ledger_entries: Sequence[Mapping[str, Any]],
) -> TagModifiedResult:
    """PRE-write gate: any tag-mutation requires signed ledger row.

    Parameters
    ----------
    fact_before
        On-disk fact tag set BEFORE the proposed write.
    fact_after
        Proposed fact tag set AFTER the write.
    ledger_entries
        Admin-risk ledger rows the caller has already loaded.
    """
    hash_before = compute_tag_set_hash(fact_before)
    hash_after = compute_tag_set_hash(fact_after)
    hash_before_hex = hash_before.hex()
    hash_after_hex = hash_after.hex()

    if hash_before == hash_after:
        return TagModifiedResult(
            success=True,
            failure_code=None,
            detail=(
                f"tag_set_hash unchanged for fact_id={fact_id!r} "
                f"(no tracked tag mutation)"
            ),
            fact_id=fact_id,
            tag_set_hash_before=hash_before_hex,
            tag_set_hash_after=hash_after_hex,
        )

    if _has_signed_tag_ledger_entry(
        ledger_entries,
        fact_id=fact_id,
        hash_before=hash_before_hex,
        hash_after=hash_after_hex,
    ):
        return TagModifiedResult(
            success=True,
            failure_code=None,
            detail=(
                f"tag_set_hash changed for fact_id={fact_id!r}; signed "
                f"admin-risk-ledger row of kind "
                f"{LEDGER_KIND_TAG_MODIFIED!r} present"
            ),
            fact_id=fact_id,
            tag_set_hash_before=hash_before_hex,
            tag_set_hash_after=hash_after_hex,
        )

    return TagModifiedResult(
        success=False,
        failure_code=F_KFR_TAG_MODIFIED,
        detail=(
            f"fact_id={fact_id!r} tracked-tag mutation detected "
            f"(tag_set_hash {hash_before_hex[:16]}…→{hash_after_hex[:16]}…) "
            f"with no signed admin-risk-ledger row of kind "
            f"{LEDGER_KIND_TAG_MODIFIED!r}"
        ),
        fact_id=fact_id,
        tag_set_hash_before=hash_before_hex,
        tag_set_hash_after=hash_after_hex,
    )


__all__ = [
    "F_KFR_TAG_MODIFIED",
    "LEDGER_KIND_TAG_MODIFIED",
    "TRACKED_TAG_FIELDS",
    "TagModifiedResult",
    "check_kfr_tag_modified",
    "compute_tag_set_hash",
]
