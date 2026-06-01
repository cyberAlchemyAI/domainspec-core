"""Tests for ``pipeline.orchestrator.seats.report_generator._canonical``.

Per §14 v1 Slice 1 Code phase — canonical-JSON byte stability,
SHA-3-512 helpers, and RT-C2-08 text-normalization closure.
"""
from __future__ import annotations

import json

import pytest

from pipeline.orchestrator.seats.report_generator._canonical import (
    canonical_json_bytes,
    compute_sha3_512_hex,
    is_well_formed_sha3_512_hex,
    normalize_text_for_hash,
    normalized_text_hash,
)


class TestCanonicalJsonBytes:
    def test_sort_keys_deterministic(self):
        a = canonical_json_bytes({"b": 1, "a": 2})
        b = canonical_json_bytes({"a": 2, "b": 1})
        assert a == b

    def test_tight_separators_no_whitespace(self):
        assert canonical_json_bytes({"a": 1, "b": [1, 2]}) == b'{"a":1,"b":[1,2]}'

    def test_utf8_unicode_preserved(self):
        out = canonical_json_bytes({"k": "héllo é"})
        # ensure_ascii=False — characters serialize as UTF-8
        assert "é".encode("utf-8") in out

    def test_round_trip_canonical(self):
        obj = {"a": [1, 2, 3], "b": {"c": "x"}}
        bytes_ = canonical_json_bytes(obj)
        reparsed = json.loads(bytes_)
        assert canonical_json_bytes(reparsed) == bytes_


class TestSha3512Hex:
    def test_known_empty(self):
        digest = compute_sha3_512_hex(b"")
        # SHA3-512("") well-known constant
        assert digest == (
            "a69f73cca23a9ac5c8b567dc185a756e97c98216"
            "4fe25859e0d1dcc1475c80a615b2123af1f5f94c"
            "11e3e9402c3ac558f500199d95b6d3e301758586"
            "281dcd26"
        )

    def test_lowercase_hex(self):
        digest = compute_sha3_512_hex(b"hello")
        assert digest == digest.lower()
        assert all(c in "0123456789abcdef" for c in digest)

    def test_length_128(self):
        assert len(compute_sha3_512_hex(b"x")) == 128


class TestIsWellFormedSha3512Hex:
    def test_well_formed_passes(self):
        assert is_well_formed_sha3_512_hex("a" * 128)

    def test_wrong_length_fails(self):
        assert not is_well_formed_sha3_512_hex("a" * 127)

    def test_non_hex_fails(self):
        assert not is_well_formed_sha3_512_hex("z" * 128)

    def test_uppercase_fails(self):
        assert not is_well_formed_sha3_512_hex("A" * 128)

    def test_non_str_fails(self):
        assert not is_well_formed_sha3_512_hex(b"a" * 128)
        assert not is_well_formed_sha3_512_hex(None)


class TestNormalizeTextForHash:
    def test_strip_leading_trailing(self):
        assert normalize_text_for_hash("  hello world  ") == "hello world"

    def test_collapse_internal_whitespace(self):
        assert normalize_text_for_hash("a   b\tc\nd") == "a b c d"

    def test_normalize_line_endings(self):
        assert normalize_text_for_hash("a\r\nb\rc") == "a b c"

    def test_nfc_normalize(self):
        # 'é' as NFC single codepoint vs decomposed e + combining acute
        composed = "café"
        decomposed = "café"
        assert normalize_text_for_hash(composed) == normalize_text_for_hash(decomposed)

    def test_non_str_raises(self):
        with pytest.raises(TypeError):
            normalize_text_for_hash(b"bytes")

    def test_idempotent(self):
        out = normalize_text_for_hash("hello world")
        assert normalize_text_for_hash(out) == out


class TestNormalizedTextHash:
    def test_byte_stable_across_normalization(self):
        a = normalized_text_hash("  hello\nworld  ")
        b = normalized_text_hash("hello world")
        assert a == b

    def test_distinct_content_distinct_hash(self):
        assert normalized_text_hash("hello") != normalized_text_hash("goodbye")
