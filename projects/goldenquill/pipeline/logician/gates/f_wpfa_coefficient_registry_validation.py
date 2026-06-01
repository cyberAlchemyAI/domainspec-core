"""F-WPFA-COEFFICIENT-REGISTRY-* — consolidated PRE-load gates. [§5.1.WPFA.{1,2,3}]

Three failure codes consolidated into one module per §4 v2.x.z OQ-4
default (matches §4 v2.x F-AMDT-08/09/10/11 + F-CLASS-* sub-code-collapse
precedent):

  - F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED — PRE-load, P0
  - F-WPFA-COEFFICIENT-SIGNATURE-INVALID — PRE-load, P0
  - F-WPFA-COEFFICIENT-ROLLBACK-INVALID — PRE-load, HIGH

The Coefficient Registry trust mechanism mirrors v7.0.7 §6.1 router-template
signing byte-for-byte. PRE-load gate verifies signature against white-glove-
pinned SN-LLC pubkey BEFORE loading; failure fail-closes deployment on prior
pinned version.

Bypass:
  - F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED: M13 audited (HIGH severity ledger).
  - F-WPFA-COEFFICIENT-SIGNATURE-INVALID: M13 audited.
  - F-WPFA-COEFFICIENT-ROLLBACK-INVALID: M13 audited.

Blueprint authority:
    - section_04_v2_x_z_wpfa_amendment.md §5.1.WPFA.{1,2,3}
    - section_02_v7_4_coefficient_registry_amendment.md §2.14.4 (trust mechanism)
    - architecture_v7_0_7_amendment.md §6.1 (load-bearing precedent)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final, Optional

from pipeline.logician.gates._protocols import SignatureVerifyCallable


F_WPFA_COEFFICIENT_REGISTRY_UNSIGNED: Final[str] = (
    "F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED"
)
F_WPFA_COEFFICIENT_SIGNATURE_INVALID: Final[str] = (
    "F-WPFA-COEFFICIENT-SIGNATURE-INVALID"
)
F_WPFA_COEFFICIENT_ROLLBACK_INVALID: Final[str] = (
    "F-WPFA-COEFFICIENT-ROLLBACK-INVALID"
)

_SUB_TAGS_SIGNATURE_INVALID: Final[frozenset[str]] = frozenset(
    {"pubkey_mismatch", "signature_bytes_invalid", "canonical_json_mismatch"}
)


@dataclass(frozen=True, kw_only=True)
class CoefficientRegistryValidationResult:
    """Outcome of any of the three PRE-load checks."""

    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_wpfa_coefficient_registry_unsigned(
    *,
    signature_hex: Optional[str],
) -> CoefficientRegistryValidationResult:
    """PRE-load: registry signature must be present and well-formed."""
    if signature_hex is None or not isinstance(signature_hex, str) or not signature_hex.strip():
        return CoefficientRegistryValidationResult(
            success=False,
            failure_code=F_WPFA_COEFFICIENT_REGISTRY_UNSIGNED,
            detail="registry missing or empty sn_llc_signature_ed25519",
        )
    if len(signature_hex) != 128 or not all(
        c in "0123456789abcdef" for c in signature_hex.lower()
    ):
        return CoefficientRegistryValidationResult(
            success=False,
            failure_code=F_WPFA_COEFFICIENT_SIGNATURE_INVALID,
            sub_tag="signature_bytes_invalid",
            detail=(
                f"signature_hex wrong length/charset (expected 128-char "
                f"lowercase hex, got {len(signature_hex)} chars)"
            ),
        )
    return CoefficientRegistryValidationResult(
        success=True,
        failure_code=None,
        detail="signature present and well-formed",
    )


def check_f_wpfa_coefficient_signature_invalid(
    *,
    canonical_signing_payload: bytes,
    signature_hex: str,
    pinned_pubkey_hex: str,
    signature_verify: SignatureVerifyCallable,
) -> CoefficientRegistryValidationResult:
    """PRE-load: signature must verify against pinned SN-LLC pubkey."""
    if (
        not isinstance(canonical_signing_payload, (bytes, bytearray))
        or not bytes(canonical_signing_payload)
    ):
        return CoefficientRegistryValidationResult(
            success=False,
            failure_code=F_WPFA_COEFFICIENT_SIGNATURE_INVALID,
            sub_tag="canonical_json_mismatch",
            detail="canonical_signing_payload empty or non-bytes",
        )
    if (
        not isinstance(pinned_pubkey_hex, str)
        or len(pinned_pubkey_hex) != 64
        or not all(c in "0123456789abcdef" for c in pinned_pubkey_hex.lower())
    ):
        return CoefficientRegistryValidationResult(
            success=False,
            failure_code=F_WPFA_COEFFICIENT_SIGNATURE_INVALID,
            sub_tag="pubkey_mismatch",
            detail=(
                "pinned_pubkey_hex must be 64-char lowercase hex Ed25519 pubkey"
            ),
        )
    try:
        sig_bytes = bytes.fromhex(signature_hex)
        pubkey_bytes = bytes.fromhex(pinned_pubkey_hex)
    except ValueError as exc:
        return CoefficientRegistryValidationResult(
            success=False,
            failure_code=F_WPFA_COEFFICIENT_SIGNATURE_INVALID,
            sub_tag="signature_bytes_invalid",
            detail=f"hex decode failed: {exc}",
        )
    try:
        verified = signature_verify(
            bytes(canonical_signing_payload), sig_bytes, pubkey_bytes
        )
    except Exception as exc:  # fail-closed on verifier exception
        return CoefficientRegistryValidationResult(
            success=False,
            failure_code=F_WPFA_COEFFICIENT_SIGNATURE_INVALID,
            sub_tag="canonical_json_mismatch",
            detail=f"signature_verify raised {type(exc).__name__}: {exc}",
        )
    if verified is not True:  # strict identity, not truthiness
        return CoefficientRegistryValidationResult(
            success=False,
            failure_code=F_WPFA_COEFFICIENT_SIGNATURE_INVALID,
            sub_tag="canonical_json_mismatch",
            detail=(
                "signature did not verify against pinned SN-LLC pubkey — "
                "deployment stays on previous pinned version"
            ),
        )
    return CoefficientRegistryValidationResult(
        success=True,
        failure_code=None,
        detail="signature verified",
    )


def check_f_wpfa_coefficient_rollback_invalid(
    *,
    rollback_target_sha3: str,
    history_dir: Path,
) -> CoefficientRegistryValidationResult:
    """PRE-load: rollback target SHA3 must resolve to a registry under history/."""
    if (
        not isinstance(rollback_target_sha3, str)
        or len(rollback_target_sha3) != 128
        or not all(
            c in "0123456789abcdef" for c in rollback_target_sha3.lower()
        )
    ):
        return CoefficientRegistryValidationResult(
            success=False,
            failure_code=F_WPFA_COEFFICIENT_ROLLBACK_INVALID,
            detail=(
                f"rollback_target_sha3 must be 128-char lowercase hex, got "
                f"{len(rollback_target_sha3) if isinstance(rollback_target_sha3, str) else type(rollback_target_sha3).__name__}"
            ),
        )
    if not isinstance(history_dir, Path):
        return CoefficientRegistryValidationResult(
            success=False,
            failure_code=F_WPFA_COEFFICIENT_ROLLBACK_INVALID,
            detail="history_dir must be a pathlib.Path",
        )
    expected = history_dir / f"{rollback_target_sha3}.yaml"
    if not expected.is_file():
        return CoefficientRegistryValidationResult(
            success=False,
            failure_code=F_WPFA_COEFFICIENT_ROLLBACK_INVALID,
            detail=(
                f"rollback target {expected!s} does not exist under history/"
            ),
        )
    return CoefficientRegistryValidationResult(
        success=True,
        failure_code=None,
        detail=f"rollback target {expected!s} resolved",
    )


__all__ = [
    "F_WPFA_COEFFICIENT_REGISTRY_UNSIGNED",
    "F_WPFA_COEFFICIENT_SIGNATURE_INVALID",
    "F_WPFA_COEFFICIENT_ROLLBACK_INVALID",
    "CoefficientRegistryValidationResult",
    "check_f_wpfa_coefficient_registry_unsigned",
    "check_f_wpfa_coefficient_signature_invalid",
    "check_f_wpfa_coefficient_rollback_invalid",
]
