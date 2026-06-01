"""F-AWARD-INGEST-ATTN-UNVERIFIED — AWARD_INGEST PRE gate (M1 §7.1).

CF-RT-03 closure.  The ``--attest-unsigned-award-doc`` operator flag
bypasses signature verification when the funder doesn't sign.  The
flag was previously single-bit; M1 requires:

1. A non-empty ``--rationale`` argument from the operator.
2. A matching admin-risk-ledger row of kind
   ``award_ingest_attestation`` with operator signature.

Either missing → fail-closed.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional, Sequence


F_AWARD_INGEST_ATTN_UNVERIFIED: Final[str] = "F-AWARD-INGEST-ATTN-UNVERIFIED"

LEDGER_KIND_AWARD_INGEST_ATTESTATION: Final[str] = (
    "award_ingest_attestation"
)


@dataclass(frozen=True, kw_only=True)
class AwardAttestationResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    grant_id: Optional[str] = None


def _has_signed_attestation_ledger_entry(
    ledger_entries: Sequence[Mapping[str, Any]],
    *,
    grant_id: str,
    award_doc_path: str,
    rationale: str,
) -> bool:
    for row in ledger_entries:
        if not isinstance(row, Mapping):
            continue
        if row.get("ledger_kind") != LEDGER_KIND_AWARD_INGEST_ATTESTATION:
            continue
        if row.get("grant_id") != grant_id:
            continue
        if row.get("award_doc_path") != award_doc_path:
            continue
        ledger_rationale = row.get("attestation_rationale")
        if not isinstance(ledger_rationale, str) or not ledger_rationale.strip():
            continue
        if ledger_rationale != rationale:
            continue
        signed = row.get("signed_at_utc")
        operator_key = row.get("operator_key_id")
        if not isinstance(signed, str) or not signed.strip():
            continue
        if not isinstance(operator_key, str) or not operator_key.strip():
            continue
        return True
    return False


def check_award_ingest_attn_unverified(
    *,
    grant_id: str,
    award_doc_path: str,
    attest_unsigned_award_doc: bool,
    rationale: Optional[str],
    ledger_entries: Sequence[Mapping[str, Any]],
) -> AwardAttestationResult:
    """PRE-AWARD_INGEST gate: attestation requires rationale + signed ledger."""
    if not attest_unsigned_award_doc:
        return AwardAttestationResult(
            success=True,
            failure_code=None,
            detail=(
                f"AWARD_INGEST grant_id={grant_id!r} did not invoke "
                "attestation flag (signature verification stays "
                "authoritative)"
            ),
            grant_id=grant_id,
        )
    if rationale is None or not isinstance(rationale, str) or not rationale.strip():
        return AwardAttestationResult(
            success=False,
            failure_code=F_AWARD_INGEST_ATTN_UNVERIFIED,
            detail=(
                f"AWARD_INGEST grant_id={grant_id!r} invoked "
                "--attest-unsigned-award-doc without --rationale "
                "(non-empty operator-supplied free text required per M1 §7.1)"
            ),
            grant_id=grant_id,
        )
    if not _has_signed_attestation_ledger_entry(
        ledger_entries,
        grant_id=grant_id,
        award_doc_path=award_doc_path,
        rationale=rationale,
    ):
        return AwardAttestationResult(
            success=False,
            failure_code=F_AWARD_INGEST_ATTN_UNVERIFIED,
            detail=(
                f"AWARD_INGEST grant_id={grant_id!r} attestation flag "
                f"invoked with rationale, but no matching admin-risk-"
                f"ledger row of kind "
                f"{LEDGER_KIND_AWARD_INGEST_ATTESTATION!r} with operator "
                "signature found"
            ),
            grant_id=grant_id,
        )
    return AwardAttestationResult(
        success=True,
        failure_code=None,
        detail=(
            f"AWARD_INGEST grant_id={grant_id!r} attestation rationale "
            "present and signed admin-risk-ledger row located"
        ),
        grant_id=grant_id,
    )


__all__ = [
    "F_AWARD_INGEST_ATTN_UNVERIFIED",
    "LEDGER_KIND_AWARD_INGEST_ATTESTATION",
    "AwardAttestationResult",
    "check_award_ingest_attn_unverified",
]
