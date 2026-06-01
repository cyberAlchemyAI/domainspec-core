"""F-PACKET-OPERATOR-SIGNATURE-INVALID — PRE-load gate. [§4 v2.x.y.1 row 15, LIVE]

Operator-pubkey resolution from v7.0.7 §6.1 classification-register operator
signature mechanism (already pinned at white-glove). Same verify procedure
as F-PACKET-SIGNATURE-INVALID, applied to packet.operator_signature_ed25519
when non-None.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.15
    - architecture_v7_0_7_amendment.md §6.1
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional


F_PACKET_OPERATOR_SIGNATURE_INVALID: Final[str] = "F-PACKET-OPERATOR-SIGNATURE-INVALID"


@dataclass(frozen=True, kw_only=True)
class OperatorSignatureInvalidResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_operator_signature_invalid(
    *,
    canonical_bytes: bytes,
    packet_operator_signature_hex: str | None,
    operator_pubkey_bytes: bytes,
) -> OperatorSignatureInvalidResult:
    """PRE-load: Ed25519 verify operator signature against pinned operator pubkey.

    When packet_operator_signature_hex is None, returns PASS (no signature
    to verify — F-PACKET-OPERATOR-SIGNATURE-MISSING is the missing-sig path).
    """
    if packet_operator_signature_hex is None:
        return OperatorSignatureInvalidResult(
            success=True,
            failure_code=None,
            detail="operator signature absent — nothing to verify",
        )
    if not isinstance(packet_operator_signature_hex, str) or len(
        packet_operator_signature_hex
    ) != 128:
        return OperatorSignatureInvalidResult(
            success=False,
            failure_code=F_PACKET_OPERATOR_SIGNATURE_INVALID,
            sub_tag="signature_bytes_invalid",
            detail="operator_signature_ed25519 must be 128 hex chars",
        )
    if (
        not isinstance(operator_pubkey_bytes, bytes)
        or len(operator_pubkey_bytes) != 32
    ):
        return OperatorSignatureInvalidResult(
            success=False,
            failure_code=F_PACKET_OPERATOR_SIGNATURE_INVALID,
            sub_tag="pubkey_resolution_failed",
            detail="operator_pubkey_bytes must be 32 bytes (Ed25519 raw pubkey)",
        )
    try:
        import nacl.signing  # type: ignore[import-not-found]
        import nacl.exceptions  # type: ignore[import-not-found]

        verifier = nacl.signing.VerifyKey(operator_pubkey_bytes)
        try:
            verifier.verify(
                canonical_bytes,
                bytes.fromhex(packet_operator_signature_hex),
            )
        except nacl.exceptions.BadSignatureError:
            return OperatorSignatureInvalidResult(
                success=False,
                failure_code=F_PACKET_OPERATOR_SIGNATURE_INVALID,
                sub_tag="signature_bytes_invalid",
                detail="Ed25519 operator-signature verification failed",
            )
    except ImportError:
        return OperatorSignatureInvalidResult(
            success=False,
            failure_code=F_PACKET_OPERATOR_SIGNATURE_INVALID,
            sub_tag="pubkey_resolution_failed",
            detail="PyNaCl unavailable; Ed25519 verify cannot run",
        )
    return OperatorSignatureInvalidResult(
        success=True,
        failure_code=None,
        detail="operator Ed25519 signature verifies against pinned pubkey",
    )


predicate_operator_signature_invalid = check_f_packet_operator_signature_invalid


__all__ = [
    "F_PACKET_OPERATOR_SIGNATURE_INVALID",
    "OperatorSignatureInvalidResult",
    "check_f_packet_operator_signature_invalid",
    "predicate_operator_signature_invalid",
]
