"""Tests for pipeline.sovereignty.crypto_primitives.

Coverage targets (per engineering_process_v0.1.md §11 spec card):
  - §5.1 BT1: sha3_512_with_nonce + verify_sha3_512_with_nonce round-trip
  - §5.1 BT1: nonce entropy / non-repetition across independent calls
  - §4.6 M7: hmac_sha3_512 deterministic output + stdlib-vector parity
  - Timing-side-channel safety: constant_time_equal uses hmac.compare_digest
  - Secure zero: zero_bytes handles bytearray + writable memoryview; rejects immutable
  - Type-safety at every public surface: TypeError on wrong types
  - HashDigest / HashPair invariants: algorithm tags correct
"""

from __future__ import annotations

import hashlib
import secrets

import pytest

from pipeline.sovereignty import (
    HashDigest,
    HashPair,
    constant_time_equal,
    hmac_sha3_512,
    sha3_512_hex,
    sha3_512_with_nonce,
    verify_sha3_512_with_nonce,
    zero_bytes,
)
from pipeline.sovereignty.crypto_primitives import (
    _derive_hashpair_from_url_and_content,
)


# -------- sha3_512_hex --------

class TestSha3512Hex:
    def test_known_vector_empty_input(self) -> None:
        # NIST FIPS 202 known vector: SHA3-512("") =
        # a69f73cca23a9ac5c8b567dc185a756e97c982164fe25859e0d1dcc1475c80a6
        # 15b2123af1f5f94c11e3e9402c3ac558f500199d95b6d3e301758586281dcd26
        result = sha3_512_hex(b"")
        assert isinstance(result, HashDigest)
        assert result.algorithm == "sha3-512"
        assert result.nonce_hex == ""
        assert result.digest_hex == (
            "a69f73cca23a9ac5c8b567dc185a756e97c982164fe25859e0d1dcc1475c80a6"
            "15b2123af1f5f94c11e3e9402c3ac558f500199d95b6d3e301758586281dcd26"
        )

    def test_matches_hashlib_directly(self) -> None:
        data = b"grant narrative bytes under test"
        result = sha3_512_hex(data)
        assert result.digest_hex == hashlib.sha3_512(data).hexdigest()

    def test_digest_is_128_hex_chars(self) -> None:
        for content in [b"", b"a", b"x" * 10_000]:
            result = sha3_512_hex(content)
            assert len(result.digest_hex) == 128
            assert all(c in "0123456789abcdef" for c in result.digest_hex)

    def test_rejects_str(self) -> None:
        with pytest.raises(TypeError, match="requires bytes"):
            sha3_512_hex("not bytes")  # type: ignore[arg-type]

    def test_rejects_none(self) -> None:
        with pytest.raises(TypeError):
            sha3_512_hex(None)  # type: ignore[arg-type]

    def test_determinism(self) -> None:
        # Same input → same output, always.
        payload = b"deterministic"
        r1 = sha3_512_hex(payload)
        r2 = sha3_512_hex(payload)
        assert r1 == r2


# -------- sha3_512_with_nonce (BT1) --------

class TestSha3512WithNonce:
    def test_returns_hashdigest_with_correct_algorithm(self) -> None:
        result = sha3_512_with_nonce(b"some content")
        assert isinstance(result, HashDigest)
        assert result.algorithm == "sha3-512-nonce"

    def test_digest_is_128_hex_chars(self) -> None:
        result = sha3_512_with_nonce(b"content")
        assert len(result.digest_hex) == 128
        assert all(c in "0123456789abcdef" for c in result.digest_hex)

    def test_nonce_is_64_hex_chars(self) -> None:
        result = sha3_512_with_nonce(b"content")
        # 32 random bytes = 64 hex chars per §5.1
        assert len(result.nonce_hex) == 64
        assert all(c in "0123456789abcdef" for c in result.nonce_hex)

    def test_same_content_produces_different_digests(self) -> None:
        # BT1 invariant: identical content in independent ingest events
        # produces distinct content_hash values (nonce provides entropy).
        content = b"identical content"
        digests = {sha3_512_with_nonce(content).digest_hex for _ in range(50)}
        assert len(digests) == 50, (
            "Nonce collision in 50 draws — entropy is broken or nonce reuse"
        )

    def test_nonce_entropy_across_independent_calls(self) -> None:
        # Draw 50 nonces; they MUST all be distinct (50 × 256-bit CSPRNG
        # draws colliding has probability well below 2^-200).
        nonces = {sha3_512_with_nonce(b"x").nonce_hex for _ in range(50)}
        assert len(nonces) == 50

    def test_rejects_str(self) -> None:
        with pytest.raises(TypeError, match="requires bytes"):
            sha3_512_with_nonce("not bytes")  # type: ignore[arg-type]

    def test_accepts_empty_bytes(self) -> None:
        # Zero-length content is allowed; BT1 still produces a valid hash+nonce.
        result = sha3_512_with_nonce(b"")
        assert len(result.digest_hex) == 128
        assert len(result.nonce_hex) == 64


# -------- verify_sha3_512_with_nonce --------

class TestVerifySha3512WithNonce:
    def test_round_trip_verifies(self) -> None:
        content = b"the payload"
        digest = sha3_512_with_nonce(content)
        assert verify_sha3_512_with_nonce(content, expected=digest) is True

    def test_wrong_content_fails(self) -> None:
        original = sha3_512_with_nonce(b"original")
        assert verify_sha3_512_with_nonce(b"tampered", expected=original) is False

    def test_tampered_digest_fails(self) -> None:
        content = b"the payload"
        original = sha3_512_with_nonce(content)
        tampered = HashDigest(
            algorithm=original.algorithm,
            digest_hex="0" * 128,  # definitely not the right hash
            nonce_hex=original.nonce_hex,
        )
        assert verify_sha3_512_with_nonce(content, expected=tampered) is False

    def test_rejects_non_bt1_algorithm(self) -> None:
        # A digest produced by sha3_512_hex (no-nonce variant) must NOT be
        # accepted by the BT1 verify function.
        plain = sha3_512_hex(b"hi")
        with pytest.raises(ValueError, match="algorithm must be"):
            verify_sha3_512_with_nonce(b"hi", expected=plain)

    def test_rejects_wrong_nonce_hex_length(self) -> None:
        bad = HashDigest(
            algorithm="sha3-512-nonce",
            digest_hex="a" * 128,
            nonce_hex="deadbeef",  # too short
        )
        with pytest.raises(ValueError, match="nonce_hex must be"):
            verify_sha3_512_with_nonce(b"content", expected=bad)

    def test_rejects_non_hex_nonce(self) -> None:
        bad = HashDigest(
            algorithm="sha3-512-nonce",
            digest_hex="a" * 128,
            nonce_hex="z" * 64,  # not hex
        )
        with pytest.raises(ValueError, match="nonce_hex is not valid hex"):
            verify_sha3_512_with_nonce(b"content", expected=bad)

    def test_rejects_wrong_digest_hex_length(self) -> None:
        # RT-v1-L-01 closure — digest_hex shape must be validated.
        bad = HashDigest(
            algorithm="sha3-512-nonce",
            digest_hex="a" * 64,  # half length
            nonce_hex="a" * 64,
        )
        with pytest.raises(ValueError, match="digest_hex must be"):
            verify_sha3_512_with_nonce(b"content", expected=bad)

    def test_rejects_non_hex_digest(self) -> None:
        # RT-v1-L-01 closure — digest_hex must actually be hex.
        bad = HashDigest(
            algorithm="sha3-512-nonce",
            digest_hex="z" * 128,  # correct length, not hex
            nonce_hex="a" * 64,
        )
        with pytest.raises(ValueError, match="digest_hex is not valid hex"):
            verify_sha3_512_with_nonce(b"content", expected=bad)

    def test_rejects_wrong_content_type(self) -> None:
        d = sha3_512_with_nonce(b"hi")
        with pytest.raises(TypeError, match="content must be bytes"):
            verify_sha3_512_with_nonce("not bytes", expected=d)  # type: ignore[arg-type]

    def test_rejects_wrong_expected_type(self) -> None:
        with pytest.raises(TypeError, match="expected must be HashDigest"):
            verify_sha3_512_with_nonce(b"hi", expected="not a HashDigest")  # type: ignore[arg-type]


# -------- hmac_sha3_512 --------

class TestHmacSha3512:
    def test_deterministic(self) -> None:
        key = b"0" * 32
        data = b"m7 message"
        a = hmac_sha3_512(key, data)
        b = hmac_sha3_512(key, data)
        assert a == b

    def test_output_is_64_bytes(self) -> None:
        result = hmac_sha3_512(b"k" * 32, b"data")
        assert len(result) == 64

    def test_different_keys_produce_different_macs(self) -> None:
        data = b"same data"
        m1 = hmac_sha3_512(b"k1" * 16, data)
        m2 = hmac_sha3_512(b"k2" * 16, data)
        assert m1 != m2

    def test_different_data_produces_different_macs(self) -> None:
        key = b"k" * 32
        m1 = hmac_sha3_512(key, b"msg1")
        m2 = hmac_sha3_512(key, b"msg2")
        assert m1 != m2

    def test_rejects_empty_key_by_default(self) -> None:
        # Default min_key_bytes=32; empty key fails the length check.
        with pytest.raises(ValueError, match=">= 32 bytes"):
            hmac_sha3_512(b"", b"data")

    def test_rejects_short_key_by_default_rt_v1_m_01(self) -> None:
        # RT-v1-M-01 closure (GPT-OSS round-2 finding): primitive now
        # enforces 32-byte minimum by default. Short keys fail loudly.
        with pytest.raises(ValueError, match=">= 32 bytes"):
            hmac_sha3_512(b"k", b"data")
        with pytest.raises(ValueError, match=">= 32 bytes"):
            hmac_sha3_512(b"x" * 31, b"data")

    def test_accepts_minimum_32_byte_key(self) -> None:
        # Exactly 32 bytes is accepted.
        result = hmac_sha3_512(b"k" * 32, b"data")
        assert len(result) == 64

    def test_accepts_long_key(self) -> None:
        # Keys longer than the minimum are accepted.
        result = hmac_sha3_512(b"x" * 1024, b"data")
        assert len(result) == 64

    def test_min_key_bytes_override_allows_shorter(self) -> None:
        # Callers with a legitimate short-key use case can override. The
        # override is explicit and reviewable; the default path stays safe.
        result = hmac_sha3_512(b"k", b"data", min_key_bytes=1)
        assert len(result) == 64

    def test_min_key_bytes_override_stricter(self) -> None:
        # Stricter override also works — caller can demand 64-byte keys.
        with pytest.raises(ValueError, match=">= 64 bytes"):
            hmac_sha3_512(b"k" * 32, b"data", min_key_bytes=64)
        result = hmac_sha3_512(b"k" * 64, b"data", min_key_bytes=64)
        assert len(result) == 64

    def test_min_key_bytes_must_be_positive_int(self) -> None:
        with pytest.raises(ValueError, match="must be >= 1"):
            hmac_sha3_512(b"k" * 32, b"data", min_key_bytes=0)
        with pytest.raises(ValueError, match="must be >= 1"):
            hmac_sha3_512(b"k" * 32, b"data", min_key_bytes=-5)

    def test_min_key_bytes_rejects_non_int(self) -> None:
        with pytest.raises(TypeError, match="min_key_bytes must be int"):
            hmac_sha3_512(b"k" * 32, b"data", min_key_bytes="32")  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="min_key_bytes must be int"):
            hmac_sha3_512(b"k" * 32, b"data", min_key_bytes=True)  # bool is an int subclass; explicitly rejected

    def test_rejects_str_key(self) -> None:
        with pytest.raises(TypeError, match="key must be bytes"):
            hmac_sha3_512("keystr", b"data")  # type: ignore[arg-type]

    def test_rejects_str_data(self) -> None:
        with pytest.raises(TypeError, match="data must be bytes"):
            hmac_sha3_512(b"key", "datastr")  # type: ignore[arg-type]


# -------- constant_time_equal --------

class TestConstantTimeEqual:
    def test_equal_bytes_return_true(self) -> None:
        assert constant_time_equal(b"abc", b"abc") is True

    def test_unequal_bytes_return_false(self) -> None:
        assert constant_time_equal(b"abc", b"abd") is False

    def test_different_lengths_return_false(self) -> None:
        assert constant_time_equal(b"abc", b"abcd") is False

    def test_empty_bytes_are_equal(self) -> None:
        assert constant_time_equal(b"", b"") is True

    def test_rejects_str_a(self) -> None:
        with pytest.raises(TypeError):
            constant_time_equal("abc", b"abc")  # type: ignore[arg-type]

    def test_rejects_str_b(self) -> None:
        with pytest.raises(TypeError):
            constant_time_equal(b"abc", "abc")  # type: ignore[arg-type]


# -------- zero_bytes --------

class TestZeroBytes:
    def test_zeros_bytearray(self) -> None:
        buf = bytearray(b"\xffsecret key material")
        zero_bytes(buf)
        assert all(b == 0 for b in buf)

    def test_zeros_writable_memoryview(self) -> None:
        buf = bytearray(b"sensitive")
        view = memoryview(buf)
        zero_bytes(view)
        assert all(b == 0 for b in buf)

    def test_rejects_immutable_bytes(self) -> None:
        with pytest.raises(TypeError, match="immutable"):
            zero_bytes(b"cannot be zeroed")  # type: ignore[arg-type]

    def test_rejects_str(self) -> None:
        with pytest.raises(TypeError, match="immutable"):
            zero_bytes("also not allowed")  # type: ignore[arg-type]

    def test_rejects_readonly_memoryview(self) -> None:
        # memoryview(bytes(...)) is read-only
        view = memoryview(b"immutable source")
        with pytest.raises(TypeError, match="read-only"):
            zero_bytes(view)

    def test_rejects_random_other_types(self) -> None:
        with pytest.raises(TypeError):
            zero_bytes([1, 2, 3])  # type: ignore[arg-type]


# -------- _derive_hashpair_from_url_and_content (internal helper) --------

class TestDeriveHashPair:
    def test_produces_hashpair_with_correct_fields(self) -> None:
        pair = _derive_hashpair_from_url_and_content(
            "https://grants.gov/view-opportunity/VAPG",
            b"<pdf bytes>",
        )
        assert isinstance(pair, HashPair)
        # Algorithm lowercase per Round-A retry Gemini finding (cross-module
        # consistency with HashDigest identifiers). Blueprint §2.1 prose
        # uses uppercase "SHA3-512"; D-09 drift logged for v6.1 backfill.
        assert pair.algorithm == "sha3-512"
        assert len(pair.url_hash) == 128
        assert len(pair.content_hash) == 128
        assert len(pair.nonce_hex) == 64

    def test_url_hash_is_nonced_free(self) -> None:
        # Same URL → same url_hash across independent calls.
        p1 = _derive_hashpair_from_url_and_content("https://example.com", b"A")
        p2 = _derive_hashpair_from_url_and_content("https://example.com", b"B")
        assert p1.url_hash == p2.url_hash

    def test_content_hashes_differ_across_calls(self) -> None:
        # Same content bytes in two ingests → distinct content_hashes
        # because nonces are independent. This is the BT1 invariant.
        p1 = _derive_hashpair_from_url_and_content("https://x.test", b"same")
        p2 = _derive_hashpair_from_url_and_content("https://x.test", b"same")
        assert p1.content_hash != p2.content_hash
        assert p1.nonce_hex != p2.nonce_hex

    def test_rejects_str_content(self) -> None:
        with pytest.raises(TypeError):
            _derive_hashpair_from_url_and_content(
                "https://x.test",
                "not bytes",  # type: ignore[arg-type]
            )

    def test_rejects_bytes_url(self) -> None:
        with pytest.raises(TypeError):
            _derive_hashpair_from_url_and_content(
                b"https://x.test",  # type: ignore[arg-type]
                b"content",
            )


# -------- BT1 cross-primitive round-trip --------

class TestBT1RoundTrip:
    """The end-to-end BT1 contract: hash at ingest, re-verify pre-draft."""

    def test_ingest_reverify_happy_path(self) -> None:
        content = secrets.token_bytes(4096)
        digest_at_ingest = sha3_512_with_nonce(content)
        # ... time passes ...
        # re-verify reproduces the hash with the retained nonce
        assert verify_sha3_512_with_nonce(content, expected=digest_at_ingest) is True

    def test_ingest_reverify_tampered_fails(self) -> None:
        content = secrets.token_bytes(4096)
        digest_at_ingest = sha3_512_with_nonce(content)
        tampered = content[:-1] + bytes([content[-1] ^ 0x01])
        assert verify_sha3_512_with_nonce(tampered, expected=digest_at_ingest) is False
