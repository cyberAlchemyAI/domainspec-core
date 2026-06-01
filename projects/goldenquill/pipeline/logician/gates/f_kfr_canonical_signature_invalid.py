"""F-KFR-CANONICAL-SIGNATURE-INVALID — KFR PRE-load gate (M1 §2.4).

Supersedes ``F-KFR-SIGNATURE-INVALID`` (v7.0.4 §1.1) — the signature
surface is now the entry's **canonical-JSON bytes** (per
:func:`pipeline.logician.canonicalization.kfr_canonical.canonicalize`),
not the raw YAML bytes.

When ``legacy_accept_mode == "enabled"`` (per §2.6 migration cycle),
the gate falls back to raw-YAML signature verification via
:func:`pipeline.logician.canonicalization.legacy_migration.verify_kfr_signature_with_migration`.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Optional

from pipeline.logician.canonicalization.kfr_canonical import (
    CanonicalizationError,
    canonicalize,
)
from pipeline.logician.canonicalization.legacy_migration import (
    LEGACY_ACCEPT_DISABLED,
    verify_kfr_signature_with_migration,
)
from pipeline.logician.gates._protocols import SignatureVerifyCallable


F_KFR_CANONICAL_SIGNATURE_INVALID: Final[str] = (
    "F-KFR-CANONICAL-SIGNATURE-INVALID"
)


@dataclass(frozen=True, kw_only=True)
class CanonicalSignatureResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    fact_id: Optional[str] = None
    used_legacy_path: bool = False


def check_kfr_canonical_signature_invalid(
    *,
    fact_id: str,
    entry_mapping: dict,
    raw_yaml_bytes: bytes,
    signature: bytes,
    public_key: bytes,
    signature_verify: SignatureVerifyCallable,
    legacy_accept_mode: str = LEGACY_ACCEPT_DISABLED,
) -> CanonicalSignatureResult:
    """PRE-load gate: verify canonical-JSON Ed25519 signature on KFR entry.

    Parameters
    ----------
    entry_mapping
        The parsed KFR entry mapping (dict).  The gate canonicalizes
        EXCEPT for the signature field itself; the canonicalization
        helper does no exclusion — callers MUST pass the entry with
        the signature stripped to the surface they signed against.
    raw_yaml_bytes
        Bytes of the entry's raw YAML representation (used only when
        ``legacy_accept_mode == "enabled"`` per §2.6).
    signature_verify
        Injected Ed25519 verifier.
    legacy_accept_mode
        When ``"enabled"``, dual-verification fires per §2.6.1.
    """
    try:
        canonical_bytes = canonicalize(entry_mapping)
    except CanonicalizationError as exc:
        return CanonicalSignatureResult(
            success=False,
            failure_code=F_KFR_CANONICAL_SIGNATURE_INVALID,
            detail=(
                f"canonicalization refused: {exc}; cannot verify "
                "signature against canonical-JSON bytes"
            ),
            fact_id=fact_id,
        )

    result = verify_kfr_signature_with_migration(
        canonical_bytes=canonical_bytes,
        raw_yaml_bytes=raw_yaml_bytes,
        signature=signature,
        public_key=public_key,
        legacy_accept_mode=legacy_accept_mode,
        canonical_verify=signature_verify,
    )

    if result.success:
        return CanonicalSignatureResult(
            success=True,
            failure_code=None,
            detail=(
                f"KFR entry {fact_id!r} canonical-JSON signature verified"
                + (" (legacy raw-YAML fallback path)" if result.used_legacy_path else "")
            ),
            fact_id=fact_id,
            used_legacy_path=result.used_legacy_path,
        )

    return CanonicalSignatureResult(
        success=False,
        failure_code=F_KFR_CANONICAL_SIGNATURE_INVALID,
        detail=(
            f"KFR entry {fact_id!r} signature verification failed — "
            f"{result.detail}"
        ),
        fact_id=fact_id,
        used_legacy_path=result.used_legacy_path,
    )


__all__ = [
    "F_KFR_CANONICAL_SIGNATURE_INVALID",
    "CanonicalSignatureResult",
    "check_kfr_canonical_signature_invalid",
]
