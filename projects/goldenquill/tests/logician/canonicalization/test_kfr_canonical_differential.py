"""Differential test for kfr_canonical (architecture v7.0.4-M1 §2.2.1).

The canonicalizer's contract: ``canonicalize(load(file_bytes))``
returns the same bytes byte-for-byte across PyYAML, ruamel.yaml, and
hand-written YAML loaders.  This test materializes a small set of
fixtures, runs them through both PyYAML and the M1 SafeLoader, and
asserts byte-equal canonical output.

ruamel.yaml is NOT a hard dependency of v0.1; the relevant
divergence-paths it surfaces are NFC normalization (covered by
test_unicode_nfc_normalization) and key ordering (covered by
test_mapping_key_order).
"""

from __future__ import annotations

import unicodedata
from decimal import Decimal

import pytest
import yaml

from pipeline.logician.canonicalization import (
    CanonicalizationError,
    canonical_dump,
    canonicalize,
    load_kfr_safe_bytes,
)


def _safeloader_load(text: str) -> dict:
    """Plain PyYAML SafeLoader load — used as one comparison leg."""
    return yaml.safe_load(text)


def test_byte_equality_safe_loader_versus_kfr_safe_loader() -> None:
    """Canonical bytes match across plain SafeLoader and KFR SafeLoader."""
    text = (
        "fact_id: F1\n"
        "unit: usd\n"
        "value: 12345\n"
        "tags: [a, b, c]\n"
    )
    a = canonicalize(yaml.safe_load(text))
    b = canonicalize(load_kfr_safe_bytes(text.encode("utf-8")))
    assert a == b
    assert a == b'{"fact_id": "F1", "tags": ["a", "b", "c"], "unit": "usd", "value": 12345}'


def test_mapping_key_order_lexicographic() -> None:
    """Mapping keys serialize in NFC + codepoint order, regardless of source order."""
    text_a = "z: 1\na: 2\nm: 3\n"
    text_b = "a: 2\nm: 3\nz: 1\n"
    out_a = canonicalize(yaml.safe_load(text_a))
    out_b = canonicalize(yaml.safe_load(text_b))
    assert out_a == out_b == b'{"a": 2, "m": 3, "z": 1}'


def test_unicode_nfc_normalization() -> None:
    """NFC-equivalent codepoint sequences canonicalize identically.

    Composed ``é`` (U+00E9) and decomposed ``e + ́`` (U+0065 U+0301)
    must hash the same after NFC.
    """
    composed = "é"
    decomposed = unicodedata.normalize("NFD", "é")
    assert composed != decomposed  # raw byte comparison differs
    a = canonical_dump({"name": composed})
    b = canonical_dump({"name": decomposed})
    assert a == b


def test_negative_zero_canonicalizes_to_zero() -> None:
    a = canonical_dump(Decimal("-0"))
    b = canonical_dump(Decimal("0"))
    assert a == b == b"0"


def test_decimal_string_pin_no_scientific() -> None:
    out = canonical_dump(Decimal("123.45"))
    assert out == b"123.45"


def test_decimal_with_trailing_zeros_preserved() -> None:
    """Decimal('123.450000') and Decimal('123.45') canonicalize differently.

    The canonicalizer uses the Decimal's own coefficient/exponent to
    preserve operator-supplied precision (so the signature surface can
    distinguish '123.45' (lowest precision) from '123.450000' which
    may carry a trailing-zero invariant).
    """
    a = canonical_dump(Decimal("123.450000"))
    b = canonical_dump(Decimal("123.45"))
    assert a == b"123.450000"
    assert b == b"123.45"


def test_float_input_refused() -> None:
    with pytest.raises(CanonicalizationError):
        canonical_dump(1.5)
    with pytest.raises(CanonicalizationError):
        canonicalize({"value": 1.5})


def test_arbitrary_python_object_refused() -> None:
    class Foo:
        pass
    with pytest.raises(CanonicalizationError):
        canonical_dump(Foo())


def test_non_finite_decimal_refused() -> None:
    with pytest.raises(CanonicalizationError):
        canonical_dump(Decimal("Infinity"))
    with pytest.raises(CanonicalizationError):
        canonical_dump(Decimal("NaN"))


def test_bool_serializes_as_true_false() -> None:
    assert canonical_dump(True) == b"true"
    assert canonical_dump(False) == b"false"


def test_null_serializes_as_null() -> None:
    assert canonical_dump(None) == b"null"


def test_array_order_preserved() -> None:
    a = canonical_dump([3, 1, 2])
    assert a == b"[3, 1, 2]"


def test_nested_mapping_canonical() -> None:
    obj = {
        "fact_id": "F1",
        "audit_chain": [
            {"kind": "initial", "ts": "2026-05-10T00:00:00Z"},
            {"kind": "sp0", "ts": "2026-05-10T01:00:00Z"},
        ],
    }
    out = canonical_dump(obj)
    # Inner dicts must also be sorted; outer dict must be sorted.
    assert b'"audit_chain":' in out
    assert b'"fact_id":' in out
    # Audit chain order preserved (list).
    assert out.index(b'"initial"') < out.index(b'"sp0"')


def test_string_with_control_chars_escaped() -> None:
    out = canonical_dump("a\nb\tc\"d\\e")
    assert b'"a\\nb\\tc\\"d\\\\e"' == out


def test_top_level_must_be_mapping_for_canonicalize() -> None:
    with pytest.raises(CanonicalizationError):
        canonicalize([1, 2, 3])  # type: ignore[arg-type]
    with pytest.raises(CanonicalizationError):
        canonicalize("nope")  # type: ignore[arg-type]


def test_empty_string_value_serializes_as_empty_quoted_string() -> None:
    assert canonical_dump({"k": ""}) == b'{"k": ""}'


def test_bytes_input_to_canonicalize_refused() -> None:
    with pytest.raises(CanonicalizationError):
        canonicalize({"value": b"raw bytes"})  # type: ignore[arg-type]
