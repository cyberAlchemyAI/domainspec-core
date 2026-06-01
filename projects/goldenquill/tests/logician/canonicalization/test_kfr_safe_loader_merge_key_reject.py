"""KFR SafeLoader rejection tests (architecture v7.0.4-M1 §2.2.2)."""

from __future__ import annotations

import pytest

from pipeline.logician.canonicalization import (
    KfrConstructError,
    load_kfr_safe_bytes,
)


def test_clean_kfr_loads() -> None:
    parsed = load_kfr_safe_bytes(
        b"fact_id: F1\nunit: usd\nvalue: 100\n"
    )
    assert parsed["fact_id"] == "F1"
    assert parsed["unit"] == "usd"
    assert parsed["value"] == 100


def test_anchor_alias_pair_refused() -> None:
    """``a: &foo bar\\nb: *foo\\n`` — anchor declaration rejection."""
    bad = b"a: &foo bar\nb: *foo\n"
    with pytest.raises(KfrConstructError) as exc:
        load_kfr_safe_bytes(bad)
    # The pre-scan event-stream pass surfaces the anchor declaration
    # as the first refusal.
    assert exc.value.offending_construct in {"anchor", "alias"}


def test_alias_without_anchor_refused() -> None:
    """Alias-only event refused even when no anchor decl precedes it."""
    bad = b"key: *missing\n"
    with pytest.raises(KfrConstructError):
        load_kfr_safe_bytes(bad)


def test_explicit_merge_key_with_alias_refused() -> None:
    """RT-01 verbatim path: ``<<: *anchor`` merge-key rejection."""
    bad = (
        b"defaults: &d\n"
        b"  key: 1\n"
        b"target:\n"
        b"  <<: *d\n"
        b"  other: 2\n"
    )
    with pytest.raises(KfrConstructError) as exc:
        load_kfr_safe_bytes(bad)
    # Either the anchor decl or the merge-key surfaces — both are
    # forbidden.
    assert exc.value.offending_construct in {
        "anchor",
        "alias",
        "merge_key",
        "forbidden_tag",
    }


def test_merge_key_inline_mapping_refused() -> None:
    """Merge-key with inline mapping (no anchor) — RT-01 leg 2."""
    bad = b"target:\n  <<: {x: 1, y: 2}\n  z: 3\n"
    with pytest.raises(KfrConstructError) as exc:
        load_kfr_safe_bytes(bad)
    assert exc.value.offending_construct in {"merge_key", "forbidden_tag"}


def test_python_custom_tag_refused() -> None:
    bad = b"value: !!python/object/apply:os.system ['ls']\n"
    with pytest.raises(KfrConstructError) as exc:
        load_kfr_safe_bytes(bad)
    assert exc.value.offending_construct in {"custom_tag", "forbidden_tag"}


def test_set_tag_refused() -> None:
    bad = b"items: !!set\n  ? a\n  ? b\n"
    with pytest.raises(KfrConstructError) as exc:
        load_kfr_safe_bytes(bad)
    assert exc.value.offending_construct in {"custom_tag", "forbidden_tag"}


def test_omap_tag_refused() -> None:
    bad = b"order: !!omap\n  - a: 1\n  - b: 2\n"
    with pytest.raises(KfrConstructError) as exc:
        load_kfr_safe_bytes(bad)
    assert exc.value.offending_construct in {"custom_tag", "forbidden_tag"}


def test_invalid_utf8_refused() -> None:
    with pytest.raises(KfrConstructError) as exc:
        load_kfr_safe_bytes(b"\xff\xfe\x00x")
    assert exc.value.offending_construct == "invalid_encoding"


def test_non_bytes_input_refused() -> None:
    with pytest.raises(KfrConstructError):
        load_kfr_safe_bytes("not bytes")  # type: ignore[arg-type]


def test_clean_yaml_with_int_string_lists_loads() -> None:
    text = (
        b"fact_id: F1\n"
        b"required_for_funder: [USDA-VAPG, USDA-RD]\n"
        b"required_for_category: []\n"
        b"value: 12345\n"
    )
    parsed = load_kfr_safe_bytes(text)
    assert parsed["required_for_funder"] == ["USDA-VAPG", "USDA-RD"]
    assert parsed["required_for_category"] == []


def test_timestamp_tag_refused() -> None:
    """YAML 1.2 timestamp tag is in our forbidden set per §2.2.2 strict-tag list."""
    bad = b"created_at: !!timestamp 2026-05-10T00:00:00Z\n"
    with pytest.raises(KfrConstructError) as exc:
        load_kfr_safe_bytes(bad)
    assert exc.value.offending_construct in {"custom_tag", "forbidden_tag"}
