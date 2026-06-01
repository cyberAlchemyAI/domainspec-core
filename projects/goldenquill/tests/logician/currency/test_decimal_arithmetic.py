"""Decimal arithmetic tests (architecture v7.0.4-M1 §6)."""

from __future__ import annotations

import decimal
from decimal import Decimal

import pytest

from pipeline.logician.currency import (
    F_CURRENCY_CONTEXT_MISMATCH,
    F_CURRENCY_CONTEXT_OMITTED,
    F_CURRENCY_DECIMAL_CONTEXT_DRIFT,
    F_CURRENCY_FLOAT_IN_COMPARISON,
    KFR_DECIMAL_CONTEXT,
    UNIT_CONVERSION_TABLE,
    CurrencyContextError,
    CurrencyFloatError,
    UnitConversionError,
    assert_kfr_context_active,
    convert_to_canonical_unit,
    to_currency,
    tolerance_check_currency,
)


# ---- Context discipline ----------------------------------------------------


def test_kfr_context_singleton_prec_28() -> None:
    assert KFR_DECIMAL_CONTEXT.prec == 28


def test_kfr_context_singleton_round_half_even() -> None:
    assert KFR_DECIMAL_CONTEXT.rounding == decimal.ROUND_HALF_EVEN


def test_kfr_context_traps_required_set() -> None:
    traps = KFR_DECIMAL_CONTEXT.traps
    assert traps[decimal.DivisionByZero] is True
    assert traps[decimal.Overflow] is True
    assert traps[decimal.InvalidOperation] is True


def test_assert_kfr_context_active_default_python_context_passes() -> None:
    # Python's default context already has the three traps.
    assert_kfr_context_active()


def test_to_currency_requires_explicit_context() -> None:
    with pytest.raises(CurrencyContextError) as exc:
        to_currency(100)  # context=None
    assert exc.value.failure_code == F_CURRENCY_CONTEXT_OMITTED


def test_to_currency_requires_singleton_identity() -> None:
    other_context = decimal.Context(prec=28, rounding=decimal.ROUND_HALF_EVEN)
    with pytest.raises(CurrencyContextError) as exc:
        to_currency(100, context=other_context)
    assert exc.value.failure_code == F_CURRENCY_CONTEXT_MISMATCH


# ---- Float refusal (DC-CF-02 + RT-10) -------------------------------------


def test_to_currency_refuses_float() -> None:
    with pytest.raises(CurrencyFloatError):
        to_currency(123.45, context=KFR_DECIMAL_CONTEXT)


def test_tolerance_check_refuses_float_draft() -> None:
    with pytest.raises(CurrencyFloatError):
        tolerance_check_currency(
            123.45,  # type: ignore[arg-type]
            Decimal("100"),
            context=KFR_DECIMAL_CONTEXT,
        )


def test_tolerance_check_refuses_float_kfr() -> None:
    with pytest.raises(CurrencyFloatError):
        tolerance_check_currency(
            Decimal("100"),
            99.5,  # type: ignore[arg-type]
            context=KFR_DECIMAL_CONTEXT,
        )


def test_tolerance_check_refuses_float_tolerance_pct() -> None:
    with pytest.raises(CurrencyFloatError):
        tolerance_check_currency(
            Decimal("100"),
            Decimal("99"),
            tolerance_pct=0.005,  # type: ignore[arg-type]
            context=KFR_DECIMAL_CONTEXT,
        )


def test_tolerance_check_refuses_float_floor() -> None:
    with pytest.raises(CurrencyFloatError):
        tolerance_check_currency(
            Decimal("100"),
            Decimal("99"),
            tolerance_floor=2500.0,  # type: ignore[arg-type]
            context=KFR_DECIMAL_CONTEXT,
        )


# ---- Tolerance behavior ---------------------------------------------------


def test_within_tolerance_pct_passes() -> None:
    # 0.5% of 1_000_000 = 5_000; 999_500 within 0.5% → True.
    assert (
        tolerance_check_currency(
            Decimal("999500"),
            Decimal("1000000"),
            context=KFR_DECIMAL_CONTEXT,
        )
        is True
    )


def test_outside_tolerance_pct_fails() -> None:
    assert (
        tolerance_check_currency(
            Decimal("990000"),
            Decimal("1000000"),
            context=KFR_DECIMAL_CONTEXT,
        )
        is False
    )


def test_floor_dominates_for_small_values() -> None:
    """At small values, $2500 floor dominates over 0.5% pct."""
    # 0.5% of $100 = $0.50; floor = $2500; |draft-kfr|=200 < 2500 → True
    assert (
        tolerance_check_currency(
            Decimal("300"),
            Decimal("100"),
            context=KFR_DECIMAL_CONTEXT,
        )
        is True
    )


def test_exact_tolerance_boundary_passes() -> None:
    """|delta| == max(pct*kfr, floor) → ``<=`` includes boundary."""
    # delta = 5_000; threshold = max(5_000, 2_500) = 5_000.
    assert (
        tolerance_check_currency(
            Decimal("995000"),
            Decimal("1000000"),
            context=KFR_DECIMAL_CONTEXT,
        )
        is True
    )


def test_decimal_string_pin_no_drift() -> None:
    """Currency arithmetic uses Decimal — no IEEE-754 drift at boundary."""
    # The classic float drift case: 0.1 + 0.2 != 0.3 in IEEE-754.
    # In Decimal: exact.
    a = Decimal("0.1") + Decimal("0.2")
    b = Decimal("0.3")
    assert a == b


# ---- Conversion ------------------------------------------------------------


def test_to_currency_int_input() -> None:
    out = to_currency(12345, context=KFR_DECIMAL_CONTEXT)
    assert out == Decimal("12345.00")


def test_to_currency_str_input() -> None:
    out = to_currency("12345.6", context=KFR_DECIMAL_CONTEXT)
    assert out == Decimal("12345.60")


def test_to_currency_decimal_input() -> None:
    out = to_currency(Decimal("12345.678"), context=KFR_DECIMAL_CONTEXT)
    assert out == Decimal("12345.68")  # quantized to .01 with banker's


def test_unit_conversion_table_includes_canonicals() -> None:
    assert "usd" in UNIT_CONVERSION_TABLE
    assert "count" in UNIT_CONVERSION_TABLE
    assert "acres" in UNIT_CONVERSION_TABLE
    assert "percentage" in UNIT_CONVERSION_TABLE


def test_thousands_usd_to_usd() -> None:
    converted, canonical = convert_to_canonical_unit(
        Decimal("12.5"), "thousands_usd", context=KFR_DECIMAL_CONTEXT
    )
    assert canonical == "usd"
    assert converted == Decimal("12500")


def test_millions_usd_to_usd() -> None:
    converted, canonical = convert_to_canonical_unit(
        Decimal("1.5"), "millions_usd", context=KFR_DECIMAL_CONTEXT
    )
    assert canonical == "usd"
    assert converted == Decimal("1500000")


def test_unknown_unit_refused() -> None:
    with pytest.raises(UnitConversionError):
        convert_to_canonical_unit(
            Decimal("100"), "bitcoins", context=KFR_DECIMAL_CONTEXT
        )


def test_canonicalize_unit_lowercase_strip() -> None:
    converted, canonical = convert_to_canonical_unit(
        Decimal("1"), "  USD  ", context=KFR_DECIMAL_CONTEXT
    )
    assert canonical == "usd"


# ---- Context drift sentinel -----------------------------------------------


def test_context_drift_detected_on_prec_change() -> None:
    saved = decimal.getcontext()
    drifted = decimal.Context(
        prec=10,
        rounding=decimal.ROUND_HALF_EVEN,
        traps=[
            decimal.DivisionByZero,
            decimal.Overflow,
            decimal.InvalidOperation,
        ],
    )
    decimal.setcontext(drifted)
    try:
        with pytest.raises(CurrencyContextError) as exc:
            tolerance_check_currency(
                Decimal("100"),
                Decimal("99"),
                context=KFR_DECIMAL_CONTEXT,
            )
        assert exc.value.failure_code == F_CURRENCY_DECIMAL_CONTEXT_DRIFT
    finally:
        decimal.setcontext(saved)


def test_context_drift_detected_on_missing_trap() -> None:
    saved = decimal.getcontext()
    drifted = decimal.Context(
        prec=28,
        rounding=decimal.ROUND_HALF_EVEN,
        traps=[],  # no traps — fail-closed
    )
    decimal.setcontext(drifted)
    try:
        with pytest.raises(CurrencyContextError) as exc:
            tolerance_check_currency(
                Decimal("100"),
                Decimal("99"),
                context=KFR_DECIMAL_CONTEXT,
            )
        assert exc.value.failure_code == F_CURRENCY_DECIMAL_CONTEXT_DRIFT
    finally:
        decimal.setcontext(saved)
