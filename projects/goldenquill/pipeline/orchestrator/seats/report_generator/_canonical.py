"""Canonical-JSON + content-hash helpers for §14 Report Generator.

Per §14.5.1 + §14 v1 LOCK 2026-05-10 Cycle 2 RT-C2-08 closure:

* Canonical-JSON encoding: ``sort_keys=True``, ``separators=(",", ":")``,
  ``ensure_ascii=False``, UTF-8 bytes. Mirrors
  ``pipeline.logician.claim_evidence._canonical_json_bytes`` for byte
  parity with the submission-flow claim-evidence assembler.
* Content-hash: SHA-3-512 lowercase-hex digest over canonical-JSON bytes.
  Mirrors v7.0.4-M1 §2 KFR canonical-signing pattern.
* Caption / narrative text normalization (RT-C2-08): strip leading /
  trailing whitespace, collapse internal whitespace runs to single space,
  normalize line endings to LF, UTF-8 NFC.

This module is the canonical byte-stream substrate every downstream
signing / re-read / drift-check operation MUST go through. Any drift
between the canonical bytes computed at author time and the canonical
bytes computed at finalize re-read time fail-closes the
``F-REPORT-COMMITMENT-UNTRACED.source_content_drift`` sub-tag.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from typing import Final

_SHA3_512_HEX_LEN: Final[int] = 128


def canonical_json_bytes(obj: object) -> bytes:
    """Deterministic JSON bytes — sort_keys + tight separators + utf-8.

    Mirrors ``pipeline.logician.claim_evidence._canonical_json_bytes`` so the
    submission-flow and report-flow byte streams compose at the same
    canonicalization boundary.
    """
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def compute_sha3_512_hex(data: bytes) -> str:
    """Lowercase-hex SHA-3-512 digest of ``data``."""
    return hashlib.sha3_512(data).hexdigest()


def is_well_formed_sha3_512_hex(value: object) -> bool:
    """True iff ``value`` is a 128-char lowercase-hex string."""
    if not isinstance(value, str):
        return False
    if len(value) != _SHA3_512_HEX_LEN:
        return False
    return all(c in "0123456789abcdef" for c in value)


def normalize_text_for_hash(text: str) -> str:
    """Per RT-C2-08 closure — canonical normalization for caption / claim text.

    Pipeline: NFC normalize → strip leading/trailing whitespace → collapse
    internal whitespace runs to single space → normalize line endings to LF.

    ``str`` in, ``str`` out. Bytes-level hashing is the caller's
    responsibility (encode UTF-8 then SHA-3-512).
    """
    if not isinstance(text, str):
        raise TypeError(f"normalize_text_for_hash expected str, got {type(text).__name__}")
    nfc = unicodedata.normalize("NFC", text)
    nfc = nfc.replace("\r\n", "\n").replace("\r", "\n")
    # Strip then collapse whitespace runs.
    tokens = nfc.split()
    return " ".join(tokens)


def normalized_text_hash(text: str) -> str:
    """Lowercase-hex SHA-3-512 of ``normalize_text_for_hash(text).encode('utf-8')``."""
    return compute_sha3_512_hex(normalize_text_for_hash(text).encode("utf-8"))


__all__ = [
    "canonical_json_bytes",
    "compute_sha3_512_hex",
    "is_well_formed_sha3_512_hex",
    "normalize_text_for_hash",
    "normalized_text_hash",
]
