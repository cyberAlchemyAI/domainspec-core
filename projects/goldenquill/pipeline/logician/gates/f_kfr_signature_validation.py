"""F-KFR-SIGNATURE-INVALID + F-KFR-AUDIT-CHAIN-BROKEN — KFR PRE-load gates.

Per architecture v7.0.4 §1.1 (RT-07 closure).

Both sub-codes are PRE-gates that fire at session start (before SP0)
AND at draft-time read (analog POST-gate when Scribe pulls a fact).
They share the same Protocol injection surface (operator-keyring
active-key catalog from Section 1 M9 + ``SignatureVerifyCallable``)
and the same KFR-entry input shape, so they are housed together per
the v2.2 F-AMDT-08/09/10/11 sub-code-collapse precedent.

* ``F-KFR-SIGNATURE-INVALID`` — KFR entry's
  ``validation.confirmed_by`` Ed25519 signature fails verification
  against the operator-keyring active-key catalog.

* ``F-KFR-AUDIT-CHAIN-BROKEN`` — KFR entry's ``audit_chain`` has
  missing or out-of-order operator signatures:
  - initial-population row missing,
  - SP0-review entries with non-monotonic timestamps, OR
  - signatures from retired keys without operator-confirmed
    rotation marker.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional, Sequence

from pipeline.logician.gates._protocols import SignatureVerifyCallable


F_KFR_SIGNATURE_INVALID: Final[str] = "F-KFR-SIGNATURE-INVALID"
F_KFR_AUDIT_CHAIN_BROKEN: Final[str] = "F-KFR-AUDIT-CHAIN-BROKEN"

# Canonical audit_chain row kinds per §1.1 schema.
AUDIT_CHAIN_KIND_INITIAL: Final[str] = "operator_signature_at_initial_population"
AUDIT_CHAIN_KIND_SP0_REVIEW: Final[str] = "operator_signature_at_sp0_review"
AUDIT_CHAIN_PERMITTED_KINDS: Final[frozenset[str]] = frozenset({
    AUDIT_CHAIN_KIND_INITIAL,
    AUDIT_CHAIN_KIND_SP0_REVIEW,
})

# Canonical key-rotation marker kind — operator-confirmed acknowledgment
# that a retired key's prior signatures remain authoritative for entries
# pre-dating the rotation.
KEY_ROTATION_MARKER_KIND: Final[str] = "operator_key_rotation_marker"


@dataclass(frozen=True, kw_only=True)
class KeyringEntry:
    """One operator-keyring active-key catalog row.

    Mirrors the Section 1 M9 per-org BYOK key-scoping discipline. The
    gate consumes already-parsed entries; key-catalog persistence lives
    elsewhere.
    """

    key_id: str
    public_key: bytes
    is_active: bool
    retired_at_utc: Optional[str] = None  # ISO-8601 string when retired


@dataclass(frozen=True, kw_only=True)
class KfrSignatureValidationResult:
    """Result of combined signature + audit-chain validation."""

    success: bool
    failure_code: Optional[str]
    detail: str
    fact_id: Optional[str] = None


def _find_key(
    keyring: Sequence[KeyringEntry],
    key_id: str,
) -> Optional[KeyringEntry]:
    for entry in keyring:
        if entry.key_id == key_id:
            return entry
    return None


def _has_rotation_marker(
    audit_chain: Sequence[Mapping[str, Any]],
    retired_key_id: str,
) -> bool:
    for row in audit_chain:
        if not isinstance(row, Mapping):
            continue
        if row.get("kind") != KEY_ROTATION_MARKER_KIND:
            continue
        if row.get("retired_key_id") == retired_key_id:
            return True
    return False


def check_kfr_signature_invalid(
    *,
    fact_id: str,
    confirmed_by_key_id: str,
    confirmation_message_bytes: bytes,
    confirmation_signature: bytes,
    keyring: Sequence[KeyringEntry],
    signature_verify: SignatureVerifyCallable,
) -> KfrSignatureValidationResult:
    """PRE-load gate: validate KFR entry's confirmed_by signature.

    Verifies that the Ed25519 signature on the KFR entry's
    ``validation`` block resolves against an active key in the
    operator-keyring catalog.
    """
    if not confirmed_by_key_id.strip():
        return KfrSignatureValidationResult(
            success=False,
            failure_code=F_KFR_SIGNATURE_INVALID,
            detail="confirmed_by_key_id empty — KFR entry validation block malformed",
            fact_id=fact_id,
        )

    key_entry = _find_key(keyring, confirmed_by_key_id)
    if key_entry is None:
        return KfrSignatureValidationResult(
            success=False,
            failure_code=F_KFR_SIGNATURE_INVALID,
            detail=(
                f"confirmed_by_key_id={confirmed_by_key_id!r} not present in "
                f"operator-keyring active-key catalog"
            ),
            fact_id=fact_id,
        )
    if not key_entry.is_active:
        return KfrSignatureValidationResult(
            success=False,
            failure_code=F_KFR_SIGNATURE_INVALID,
            detail=(
                f"confirmed_by_key_id={confirmed_by_key_id!r} is retired "
                "(no active-key match for KFR confirmation signature)"
            ),
            fact_id=fact_id,
        )

    try:
        verified = signature_verify(
            confirmation_message_bytes,
            confirmation_signature,
            key_entry.public_key,
        )
    except Exception as exc:  # noqa: BLE001 — fail-closed
        return KfrSignatureValidationResult(
            success=False,
            failure_code=F_KFR_SIGNATURE_INVALID,
            detail=(
                f"signature_verify raised {type(exc).__name__}: {exc}"
            ),
            fact_id=fact_id,
        )
    if verified is not True:
        return KfrSignatureValidationResult(
            success=False,
            failure_code=F_KFR_SIGNATURE_INVALID,
            detail=(
                f"Ed25519 verification failed for KFR entry {fact_id!r} "
                f"under key {confirmed_by_key_id!r}"
            ),
            fact_id=fact_id,
        )

    return KfrSignatureValidationResult(
        success=True,
        failure_code=None,
        detail=(
            f"KFR entry {fact_id!r} confirmation signature verified under "
            f"active key {confirmed_by_key_id!r}"
        ),
        fact_id=fact_id,
    )


def check_kfr_audit_chain_broken(
    *,
    fact_id: str,
    audit_chain: Sequence[Mapping[str, Any]],
    keyring: Sequence[KeyringEntry],
) -> KfrSignatureValidationResult:
    """PRE-load gate: validate KFR audit_chain integrity.

    Enforces three invariants per §1.1:
    1. Initial-population row exists.
    2. SP0-review timestamps are monotonically non-decreasing.
    3. Any retired-key signature requires a matching
       ``operator_key_rotation_marker`` row.
    """
    if not audit_chain:
        return KfrSignatureValidationResult(
            success=False,
            failure_code=F_KFR_AUDIT_CHAIN_BROKEN,
            detail=(
                f"KFR entry {fact_id!r} audit_chain empty — initial-"
                "population row missing"
            ),
            fact_id=fact_id,
        )

    has_initial = False
    sp0_timestamps: list[str] = []
    for row in audit_chain:
        if not isinstance(row, Mapping):
            return KfrSignatureValidationResult(
                success=False,
                failure_code=F_KFR_AUDIT_CHAIN_BROKEN,
                detail=(
                    f"KFR entry {fact_id!r} audit_chain has non-mapping row "
                    f"of type {type(row).__name__}"
                ),
                fact_id=fact_id,
            )
        kind = row.get("kind")
        if kind == AUDIT_CHAIN_KIND_INITIAL:
            has_initial = True
        elif kind == AUDIT_CHAIN_KIND_SP0_REVIEW:
            ts = row.get("signed_at_utc")
            if not isinstance(ts, str) or not ts.strip():
                return KfrSignatureValidationResult(
                    success=False,
                    failure_code=F_KFR_AUDIT_CHAIN_BROKEN,
                    detail=(
                        f"KFR entry {fact_id!r} SP0-review row lacks "
                        "non-empty signed_at_utc"
                    ),
                    fact_id=fact_id,
                )
            sp0_timestamps.append(ts.strip())
        elif kind == KEY_ROTATION_MARKER_KIND:
            # Rotation markers permitted as bookkeeping rows; do not
            # contribute to monotonicity check.
            continue
        else:
            return KfrSignatureValidationResult(
                success=False,
                failure_code=F_KFR_AUDIT_CHAIN_BROKEN,
                detail=(
                    f"KFR entry {fact_id!r} audit_chain row has unrecognized "
                    f"kind {kind!r}"
                ),
                fact_id=fact_id,
            )

        # Per-row signing-key currency check: any signing key referenced
        # in an audit_chain row must either be active OR carry a matching
        # rotation marker elsewhere in the chain.
        signing_key_id = row.get("signing_key_id")
        if isinstance(signing_key_id, str) and signing_key_id.strip():
            key_entry = _find_key(keyring, signing_key_id.strip())
            if key_entry is None:
                return KfrSignatureValidationResult(
                    success=False,
                    failure_code=F_KFR_AUDIT_CHAIN_BROKEN,
                    detail=(
                        f"KFR entry {fact_id!r} audit_chain references "
                        f"unknown signing_key_id={signing_key_id!r}"
                    ),
                    fact_id=fact_id,
                )
            if not key_entry.is_active:
                if not _has_rotation_marker(
                    audit_chain, signing_key_id.strip()
                ):
                    return KfrSignatureValidationResult(
                        success=False,
                        failure_code=F_KFR_AUDIT_CHAIN_BROKEN,
                        detail=(
                            f"KFR entry {fact_id!r} audit_chain row "
                            f"signed by retired key {signing_key_id!r} "
                            "without operator-confirmed rotation marker"
                        ),
                        fact_id=fact_id,
                    )

    if not has_initial:
        return KfrSignatureValidationResult(
            success=False,
            failure_code=F_KFR_AUDIT_CHAIN_BROKEN,
            detail=(
                f"KFR entry {fact_id!r} audit_chain missing required "
                f"{AUDIT_CHAIN_KIND_INITIAL!r} row"
            ),
            fact_id=fact_id,
        )

    # Monotonic timestamp check on SP0-review rows.
    for prev, nxt in zip(sp0_timestamps, sp0_timestamps[1:]):
        if nxt < prev:
            return KfrSignatureValidationResult(
                success=False,
                failure_code=F_KFR_AUDIT_CHAIN_BROKEN,
                detail=(
                    f"KFR entry {fact_id!r} SP0-review timestamps non-"
                    f"monotonic: {prev!r} followed by {nxt!r}"
                ),
                fact_id=fact_id,
            )

    return KfrSignatureValidationResult(
        success=True,
        failure_code=None,
        detail=(
            f"KFR entry {fact_id!r} audit_chain integrity verified "
            f"({len(audit_chain)} rows)"
        ),
        fact_id=fact_id,
    )


__all__ = [
    "AUDIT_CHAIN_KIND_INITIAL",
    "AUDIT_CHAIN_KIND_SP0_REVIEW",
    "AUDIT_CHAIN_PERMITTED_KINDS",
    "F_KFR_AUDIT_CHAIN_BROKEN",
    "F_KFR_SIGNATURE_INVALID",
    "KEY_ROTATION_MARKER_KIND",
    "KeyringEntry",
    "KfrSignatureValidationResult",
    "check_kfr_audit_chain_broken",
    "check_kfr_signature_invalid",
]
