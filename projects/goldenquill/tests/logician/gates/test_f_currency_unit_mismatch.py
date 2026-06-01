"""F-CURRENCY-UNIT-MISMATCH gate tests (M1 §8.2)."""

from __future__ import annotations

from decimal import Decimal

from pipeline.logician.gates.f_currency_unit_mismatch import (
    F_CURRENCY_UNIT_MISMATCH,
    check_currency_unit_mismatch,
)


def test_failure_code_constant() -> None:
    assert F_CURRENCY_UNIT_MISMATCH == "F-CURRENCY-UNIT-MISMATCH"


def test_matching_units_pass() -> None:
    r = check_currency_unit_mismatch(
        draft_value=Decimal("100"),
        draft_unit="usd",
        kfr_value=Decimal("100"),
        kfr_unit="usd",
    )
    assert r.success is True
    assert r.canonical_unit == "usd"


def test_thousands_usd_to_usd_canonicalizes() -> None:
    """CF-RT-06 closure verbatim — 12.5 thousands_usd should equal 12500 usd."""
    r = check_currency_unit_mismatch(
        draft_value=Decimal("12.5"),
        draft_unit="thousands_usd",
        kfr_value=Decimal("12500"),
        kfr_unit="usd",
    )
    assert r.success is True
    draft_canon, kfr_canon = r.canonical_pair  # type: ignore[misc]
    assert draft_canon == kfr_canon


def test_unknown_unit_fails() -> None:
    r = check_currency_unit_mismatch(
        draft_value=Decimal("100"),
        draft_unit="bitcoins",
        kfr_value=Decimal("100"),
        kfr_unit="usd",
    )
    assert r.success is False
    assert r.failure_code == F_CURRENCY_UNIT_MISMATCH


def test_acres_to_hectares_passes() -> None:
    r = check_currency_unit_mismatch(
        draft_value=Decimal("100"),
        draft_unit="hectares",
        kfr_value=Decimal("100"),
        kfr_unit="acres",
    )
    assert r.success is True


def test_disjoint_canonical_unit_classes_fail() -> None:
    """USD ↔ acres are distinct canonical classes."""
    r = check_currency_unit_mismatch(
        draft_value=Decimal("100"),
        draft_unit="usd",
        kfr_value=Decimal("100"),
        kfr_unit="acres",
    )
    assert r.success is False
    assert r.failure_code == F_CURRENCY_UNIT_MISMATCH
