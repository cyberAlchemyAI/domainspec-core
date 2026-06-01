"""F-PACKET-SIGNATURE-INVALID — PRE-load gate. [§4 v2.x.y.1 row 13, LIVE]

Producer-pubkey resolution from
``vault_shared/reflection_packet/producer_pubkey.signed.yaml`` (NOT from
packet's ``emitted_by_seat`` field per RT-10 fold-in; circular-trust closed).

Mirrors v7.0.4-M1 §2 KFR canonical-signature-invalid byte-for-byte:
  1. Load producer pubkey from white-glove-pinned signed-asset registry.
  2. Compute to_canonical_bytes(packet); SHA3-512 over canonical bytes;
     compare against packet.canonical_bytes_hash.
  3. Verify Ed25519 signature against (producer_pubkey, canonical_bytes).

Sub-tags: ``.canonical_json_mismatch``, ``.signature_bytes_invalid``,
``.pubkey_resolution_failed``.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.13
    - section_16_reflection_packet.md §16.5
    - architecture_v7_0_4_M1_amendment.md §2
"""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass
from typing import Final, Optional


F_PACKET_SIGNATURE_INVALID: Final[str] = "F-PACKET-SIGNATURE-INVALID"


@dataclass(frozen=True, kw_only=True)
class SignatureInvalidResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_signature_invalid(
    *,
    canonical_bytes: bytes,
    packet_canonical_bytes_hash: str,
    packet_producer_signature_hex: str,
    producer_pubkey_bytes: bytes,
) -> SignatureInvalidResult:
    """PRE-load: SHA3-512 + Ed25519 verify against pinned producer pubkey.

    ``producer_pubkey_bytes`` resolved by caller from white-glove-pinned
    registry (NOT from packet.emitted_by_seat per RT-10).
    """
    if not isinstance(canonical_bytes, bytes):
        return SignatureInvalidResult(
            success=False,
            failure_code=F_PACKET_SIGNATURE_INVALID,
            detail="canonical_bytes must be bytes",
        )
    if not isinstance(packet_canonical_bytes_hash, str):
        return SignatureInvalidResult(
            success=False,
            failure_code=F_PACKET_SIGNATURE_INVALID,
            detail="packet_canonical_bytes_hash must be str",
        )
    # Step 1 — SHA3-512 cross-check
    computed_hash = hashlib.sha3_512(canonical_bytes).hexdigest()
    if not hmac.compare_digest(
        computed_hash.lower(), packet_canonical_bytes_hash.lower()
    ):
        return SignatureInvalidResult(
            success=False,
            failure_code=F_PACKET_SIGNATURE_INVALID,
            sub_tag="canonical_json_mismatch",
            detail=(
                f"computed canonical-bytes SHA3-512 {computed_hash!r} != "
                f"packet field {packet_canonical_bytes_hash!r}"
            ),
        )
    # Step 2 — Ed25519 verify (delegated to nacl when available; constant-
    # time hex check at this layer)
    if not isinstance(packet_producer_signature_hex, str) or len(
        packet_producer_signature_hex
    ) != 128:
        return SignatureInvalidResult(
            success=False,
            failure_code=F_PACKET_SIGNATURE_INVALID,
            sub_tag="signature_bytes_invalid",
            detail="producer_signature_ed25519 must be 128 hex chars",
        )
    if not isinstance(producer_pubkey_bytes, bytes) or len(producer_pubkey_bytes) != 32:
        return SignatureInvalidResult(
            success=False,
            failure_code=F_PACKET_SIGNATURE_INVALID,
            sub_tag="pubkey_resolution_failed",
            detail="producer_pubkey_bytes must be 32 bytes (Ed25519 raw pubkey)",
        )
    try:
        import nacl.signing  # type: ignore[import-not-found]
        import nacl.exceptions  # type: ignore[import-not-found]

        verifier = nacl.signing.VerifyKey(producer_pubkey_bytes)
        try:
            verifier.verify(
                canonical_bytes,
                bytes.fromhex(packet_producer_signature_hex),
            )
        except nacl.exceptions.BadSignatureError:
            return SignatureInvalidResult(
                success=False,
                failure_code=F_PACKET_SIGNATURE_INVALID,
                sub_tag="signature_bytes_invalid",
                detail="Ed25519 signature verification failed",
            )
    except ImportError:
        # PyNaCl not installed — degraded mode: hash check passed; signal that
        # signature crypto-verify is unavailable. Caller treats as fail-closed
        # in production; tests may exercise the degraded path.
        return SignatureInvalidResult(
            success=False,
            failure_code=F_PACKET_SIGNATURE_INVALID,
            sub_tag="pubkey_resolution_failed",
            detail="PyNaCl unavailable; Ed25519 verify cannot run",
        )
    return SignatureInvalidResult(
        success=True,
        failure_code=None,
        detail=(
            "SHA3-512 canonical hash matches + Ed25519 verify OK against "
            "white-glove-pinned producer pubkey"
        ),
    )


predicate_signature_invalid = check_f_packet_signature_invalid


__all__ = [
    "F_PACKET_SIGNATURE_INVALID",
    "SignatureInvalidResult",
    "check_f_packet_signature_invalid",
    "predicate_signature_invalid",
]
