"""Unit tests for F-FUNDER-CORPUS-INTEGRITY (PRE/POST-load, Law 5, P0).

Per architecture v7.0.5 §5.7.
"""

from __future__ import annotations

import hashlib

from pipeline.logician.gates.f_funder_corpus_integrity import (
    F_FUNDER_CORPUS_INTEGRITY,
    check_funder_corpus_integrity,
)


def _sha3_512_hex(b: bytes) -> str:
    return hashlib.sha3_512(b).hexdigest()


def test_failure_code_constant() -> None:
    assert F_FUNDER_CORPUS_INTEGRITY == "F-FUNDER-CORPUS-INTEGRITY"


def test_matching_hash_passes() -> None:
    doc = b"USDA VAPG FY26 Request for Applications\n\n..."
    recorded = _sha3_512_hex(doc)
    r = check_funder_corpus_integrity(
        doc_bytes=doc,
        recorded_hash=recorded,
    )
    assert r.success is True
    assert r.computed_hash_prefix16 == recorded[:16]
    assert r.recorded_hash_prefix16 == recorded[:16]


def test_mismatched_hash_fails() -> None:
    doc = b"USDA VAPG FY26 Request for Applications\n\n..."
    tampered_recorded = _sha3_512_hex(b"different bytes")
    r = check_funder_corpus_integrity(
        doc_bytes=doc,
        recorded_hash=tampered_recorded,
    )
    assert r.success is False
    assert r.failure_code == F_FUNDER_CORPUS_INTEGRITY
    assert "tamper or corruption" in r.detail


def test_empty_recorded_hash_fails_closed() -> None:
    r = check_funder_corpus_integrity(
        doc_bytes=b"any bytes",
        recorded_hash="",
    )
    assert r.success is False
    assert r.failure_code == F_FUNDER_CORPUS_INTEGRITY
    assert "register row malformed" in r.detail


def test_case_insensitive_hash_match() -> None:
    doc = b"some bytes"
    recorded_upper = _sha3_512_hex(doc).upper()
    r = check_funder_corpus_integrity(
        doc_bytes=doc,
        recorded_hash=recorded_upper,
    )
    assert r.success is True


def test_recorded_hash_with_whitespace_normalizes() -> None:
    doc = b"data"
    recorded = f"  {_sha3_512_hex(doc)}  \n"
    r = check_funder_corpus_integrity(
        doc_bytes=doc,
        recorded_hash=recorded,
    )
    assert r.success is True


def test_injected_hash_callable_used() -> None:
    # Verify that an injected hash_bytes callable is invoked rather than
    # the default
    captured: list[bytes] = []

    def fake_hasher(b: bytes) -> str:
        captured.append(b)
        return "deadbeef" * 16  # 128 hex chars

    r = check_funder_corpus_integrity(
        doc_bytes=b"sample",
        recorded_hash="deadbeef" * 16,
        hash_bytes=fake_hasher,
    )
    assert r.success is True
    assert captured == [b"sample"]


def test_empty_bytes_with_correct_empty_hash_passes() -> None:
    empty = b""
    recorded = _sha3_512_hex(empty)
    r = check_funder_corpus_integrity(
        doc_bytes=empty,
        recorded_hash=recorded,
    )
    assert r.success is True


def test_one_byte_change_detected() -> None:
    doc_a = b"PROPOSAL: $500,000 award request"
    doc_b = b"PROPOSAL: $500,001 award request"  # one digit changed
    recorded = _sha3_512_hex(doc_a)
    r = check_funder_corpus_integrity(
        doc_bytes=doc_b,
        recorded_hash=recorded,
    )
    assert r.success is False
    assert r.failure_code == F_FUNDER_CORPUS_INTEGRITY
