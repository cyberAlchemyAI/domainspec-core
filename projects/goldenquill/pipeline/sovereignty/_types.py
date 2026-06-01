"""Section 1 frozen-dataclass type definitions.

Module-level types for the Sovereignty Envelope.

Blueprint references:
  - HashPair           [§2.1]
  - HashDigest         [§2.1 extension — A12.3 crypto-agility scaffold]
  - OperatorSignature  [addendum A12.3 forward-reference ahead of §1 v6.1 backfill]

BLUEPRINT_DEPS intentionally populated before first LOCK so the drift
detector has a baseline. Hashes are 16-char SHA3-512 prefixes; full
hashes recorded at code LOCK time.
"""

from __future__ import annotations

from dataclasses import dataclass

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": ["§2.1 HashPair"],
        "hash_at_lock": None,  # populated at first LOCK
        "hash_source_version": "v6",
    },
    "v7_round_handoff_addendum_A7_A8_A9_2026-04-19.md": {
        "sections_implemented": ["§A12.3 OperatorSignature"],
        "hash_at_lock": None,
        "hash_source_version": "signed-off-2026-04-19",
    },
}


@dataclass(frozen=True, kw_only=True)
class HashPair:
    """Dual-hash envelope carrier. [§2.1]

    url_hash: SHA-3-512 of the URL string (UTF-8, no BOM). No nonce — identical
              URLs across sessions produce the same hash, enabling
              "same URL, different content" detection.

    content_hash: SHA-3-512 of (content_bytes || nonce). Nonce is generated
                  once at ingest per §5.1 BT1 and carried for the life of
                  the envelope. Identical content in two independent
                  ingests still produces distinct content_hashes.

    algorithm: algorithm identifier. v0.1 = "SHA3-512". A12 crypto-agility
               commitment means downstream dispatches on this field rather
               than hardcoding the algorithm.

    nonce_hex: 32 random bytes (64 hex chars) from secrets.token_bytes.
    """
    url_hash: str
    content_hash: str
    algorithm: str
    nonce_hex: str


@dataclass(frozen=True, kw_only=True)
class HashDigest:
    """A single hash value with algorithm tag and optional nonce.

    A12.3 crypto-agility scaffold — extends §2.1 HashPair's pattern to the
    single-hash case (where only content needs hashing, not a URL + content
    pair). Used by every primitive that produces a hash destined to cross
    a section boundary, so downstream dispatches on algorithm rather than
    assuming SHA-3-512.

    algorithm values at v0.1: "sha3-512", "sha3-512-nonce" (i.e., BT1 form).
    v0.2 additions will include "blake3" and any post-quantum variants per A12.

    nonce_hex is present when algorithm includes a per-hash nonce (e.g.,
    "sha3-512-nonce"); absent (empty string) otherwise.
    """
    algorithm: str
    digest_hex: str
    nonce_hex: str = ""


@dataclass(frozen=True, kw_only=True)
class OperatorSignature:
    """Operator-signed artifact carrier.

    A12.3 crypto-agility commitment. v0.1 populates `algorithm = "ed25519"`.
    v0.2 introduces `"hybrid-ed25519-ml-dsa-65"` (dual sign; either verifies).
    v0.3+ migrates to pure `"ml-dsa-65"` after fleet-wide key rotation.

    Downstream verifiers look up the verify routine by algorithm; they do NOT
    pattern-match on a hardcoded string. This type and its dispatch pattern
    are the forcing function behind A12.7 (every v0.1 interface touching
    signatures carries crypto-agility scaffolding).

    algorithm values at v0.1: "ed25519"
    algorithm values at v0.2: "ed25519", "hybrid-ed25519-ml-dsa-65"
    algorithm values at v0.3+: "ml-dsa-65", "hybrid-ed25519-ml-dsa-65"

    signature_bytes: the actual signature, opaque to downstream.
    signer_key_id: stable identifier for the operator key; keystore-scoped.
    signed_at_iso8601: UTC timestamp, `Z` suffix.
    """
    algorithm: str
    signature_bytes: bytes
    signer_key_id: str
    signed_at_iso8601: str
