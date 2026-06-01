"""Canonical-JSON serializer for KFR entries.

Architecture v7.0.4-M1 §2.2.1 (CF-RT-01 closure — sign canonical bytes,
not raw YAML bytes). Pipeline order is fixed and deterministic:

1. NFC-normalize every string value (mapping keys, scalar values, list
   elements).
2. Pin numeric representation:

   * ``int`` → ``"123"``.
   * ``Decimal`` → exact textual form (e.g., ``"123.450000"``); never
     scientific.
   * ``bool`` → ``"true"``/``"false"`` (Python's ``True/False`` shape).
   * ``float`` is FORBIDDEN → :class:`CanonicalizationError` raised so
     the caller can fail-closed via ``F-CURRENCY-FLOAT-IN-COMPARISON``.
   * Forbidden numeric forms (``Infinity``, ``-Infinity``, ``NaN``,
     hex/octal/binary literals reaching us as int objects with weird
     repr — all impossible since we use the int's own decimal form,
     so this is enforced at the loader rather than here) → caller's
     responsibility.
   * ``-0`` (Decimal/int) canonicalizes to ``0``.
3. Mapping keys sorted lexicographically (codepoint order, post-NFC).
4. Whitespace minimal — one space after ``:`` and ``,`` per RFC 8259-ish
   convention.  No indent, no trailing newline.
5. Boolean literal ``true`` / ``false`` only.
6. Null literal ``null`` only.
7. Array order preserved.
8. No comments / aliases / anchors / merge-keys (loader strips those at
   construction time per §2.2.2).

Determinism contract: ``canonicalize(load(file_bytes))`` returns the
same bytes byte-for-byte across PyYAML, ruamel.yaml, and hand-written
YAML loaders.  The differential test fixture under
``tests/logician/canonicalization/test_kfr_canonical_differential.py``
asserts byte-equality.
"""

from __future__ import annotations

import math
import unicodedata
from decimal import Decimal
from typing import Any, Final


CANONICALIZATION_SCHEMA_VERSION: Final[str] = "kfr_canonical.v1"


class CanonicalizationError(ValueError):
    """Raised when an entry contains a value the canonicalizer refuses.

    The caller (KFR PRE-gate) translates this into the appropriate
    fail-closed failure code: ``F-KFR-YAML-CONSTRUCT-FORBIDDEN`` for
    forbidden numeric / string shapes, or ``F-CURRENCY-FLOAT-IN-COMPARISON``
    when a ``float`` reaches the canonicalizer through any path.
    """


def _nfc(text: str) -> str:
    """NFC-normalize Step 1 per §2.2.1.

    Closes the cross-loader divergence path where PyYAML emits raw
    UTF-8 bytes while ruamel.yaml may emit ``é``-style escapes for the
    same logical codepoint.
    """
    return unicodedata.normalize("NFC", text)


def _encode_string(text: str) -> str:
    normalized = _nfc(text)
    out = ['"']
    for ch in normalized:
        cp = ord(ch)
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\b":
            out.append("\\b")
        elif ch == "\f":
            out.append("\\f")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif cp < 0x20:
            out.append(f"\\u{cp:04x}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _encode_int(value: int) -> str:
    # Bools subclass int — handled separately by caller.
    if value == 0:
        return "0"
    return f"{value:d}"


def _encode_decimal(value: Decimal) -> str:
    if not value.is_finite():
        raise CanonicalizationError(
            f"Decimal value {value!r} is non-finite (Infinity/NaN); "
            "canonicalization refuses fail-closed"
        )
    if value == 0:
        # Canonicalize -0 to 0 per §2.2.1 negative-zero clause.
        return "0"
    # Strip exponent: convert to fixed-precision text via __format__("f")
    # which renders the Decimal's own coefficient/exponent without
    # falling back to float.  Decimal("1E+3") → "1000".
    sign, digits, exponent = value.as_tuple()
    if exponent >= 0:
        text = "-" if sign else ""
        text += "".join(str(d) for d in digits) + "0" * exponent
        return text
    int_part_len = len(digits) + exponent
    sign_prefix = "-" if sign else ""
    if int_part_len <= 0:
        frac = "0" * (-int_part_len) + "".join(str(d) for d in digits)
        return f"{sign_prefix}0.{frac}"
    int_part = "".join(str(d) for d in digits[:int_part_len])
    frac_part = "".join(str(d) for d in digits[int_part_len:])
    if frac_part:
        return f"{sign_prefix}{int_part}.{frac_part}"
    return f"{sign_prefix}{int_part}"


def _encode_bool(value: bool) -> str:
    return "true" if value else "false"


def _encode_value(value: Any) -> str:
    # Order matters — bool subclasses int, so check bool first.
    if value is None:
        return "null"
    if isinstance(value, bool):
        return _encode_bool(value)
    if isinstance(value, float):
        # CF-RT-01 closure leg + DC-CF-02 closure: float never enters
        # canonical bytes.
        raise CanonicalizationError(
            f"float value {value!r} forbidden in canonicalization "
            "(use Decimal for currency / numeric facts); "
            "F-CURRENCY-FLOAT-IN-COMPARISON applies"
        )
    if isinstance(value, int):
        return _encode_int(value)
    if isinstance(value, Decimal):
        return _encode_decimal(value)
    if isinstance(value, str):
        return _encode_string(value)
    if isinstance(value, (list, tuple)):
        items = [_encode_value(v) for v in value]
        return "[" + ", ".join(items) + "]"
    if isinstance(value, dict):
        return _encode_mapping(value)
    raise CanonicalizationError(
        f"value of type {type(value).__name__} is not canonicalizable "
        f"(value={value!r}); only int/Decimal/str/bool/None/list/dict "
        "are admitted"
    )


def _encode_mapping(mapping: dict) -> str:
    sorted_items = []
    for raw_key, raw_value in mapping.items():
        if not isinstance(raw_key, str):
            raise CanonicalizationError(
                f"mapping key {raw_key!r} of type "
                f"{type(raw_key).__name__} is not a string — "
                "canonicalization requires string keys"
            )
        normalized_key = _nfc(raw_key)
        encoded_value = _encode_value(raw_value)
        sorted_items.append((normalized_key, encoded_value))
    sorted_items.sort(key=lambda kv: kv[0])
    parts = [
        _encode_string(key) + ": " + value for key, value in sorted_items
    ]
    return "{" + ", ".join(parts) + "}"


def canonical_dump(value: Any) -> bytes:
    """Encode any canonicalizable Python value to canonical-JSON bytes.

    The top-level value may be any admitted shape (mapping, list,
    scalar).  The KFR signature surface uses ``canonicalize(entry)``
    (mapping form); ``canonical_dump`` is the lower-level helper for
    benchmarks / allowlists that sign sub-mappings.
    """
    text = _encode_value(value)
    return text.encode("utf-8")


def canonicalize(entry: dict) -> bytes:
    """Canonical-JSON bytes for a KFR entry mapping (§2.2.1 entry surface).

    The entry MUST be a mapping at the top level — the KFR schema
    requires a ``fact_id`` key; refusal is fail-closed at
    :class:`CanonicalizationError` for the caller to translate into a
    Logician failure code.
    """
    if not isinstance(entry, dict):
        raise CanonicalizationError(
            f"canonicalize expects mapping at top level, got "
            f"{type(entry).__name__}"
        )
    return canonical_dump(entry)


# Re-exported guard for callers that want to assert a Decimal value is
# representable before canonicalization.
def assert_finite_decimal(value: Decimal) -> None:
    if not isinstance(value, Decimal):
        raise CanonicalizationError(
            f"assert_finite_decimal expects Decimal, got "
            f"{type(value).__name__}"
        )
    if not value.is_finite():
        raise CanonicalizationError(
            f"Decimal {value!r} is non-finite (Infinity/NaN)"
        )
    # `math.isnan` is incidentally protective if a numeric type that
    # isn't quite Decimal slipped through (defensive).
    try:
        if math.isnan(float(value)) or math.isinf(float(value)):
            raise CanonicalizationError(
                f"Decimal {value!r} non-finite under float coercion"
            )
    except (OverflowError, ValueError):
        # Decimal too large for float — fine, still canonicalizable.
        return


__all__ = [
    "CANONICALIZATION_SCHEMA_VERSION",
    "CanonicalizationError",
    "assert_finite_decimal",
    "canonical_dump",
    "canonicalize",
]
