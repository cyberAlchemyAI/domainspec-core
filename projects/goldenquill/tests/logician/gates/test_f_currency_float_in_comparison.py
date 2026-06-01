"""F-CURRENCY-FLOAT-IN-COMPARISON gate tests (M1 §6.4)."""

from __future__ import annotations

from decimal import Decimal

from pipeline.logician.gates.f_currency_float_in_comparison import (
    F_CURRENCY_FLOAT_IN_COMPARISON,
    check_currency_float_in_comparison,
)


def test_failure_code_constant() -> None:
    assert F_CURRENCY_FLOAT_IN_COMPARISON == "F-CURRENCY-FLOAT-IN-COMPARISON"


def test_decimal_within_tolerance_passes() -> None:
    r = check_currency_float_in_comparison(
        draft=Decimal("999500"),
        kfr=Decimal("1000000"),
    )
    assert r.success is True
    assert r.within_tolerance is True


def test_float_draft_fails() -> None:
    r = check_currency_float_in_comparison(
        draft=999500.0,  # type: ignore[arg-type]
        kfr=Decimal("1000000"),
    )
    assert r.success is False
    assert r.failure_code == F_CURRENCY_FLOAT_IN_COMPARISON


def test_float_kfr_fails() -> None:
    r = check_currency_float_in_comparison(
        draft=Decimal("999500"),
        kfr=1000000.0,  # type: ignore[arg-type]
    )
    assert r.success is False
    assert r.failure_code == F_CURRENCY_FLOAT_IN_COMPARISON


def test_outside_tolerance_passes_gate_but_within_false() -> None:
    """Gate is for *float* refusal — outside-tolerance returns success=True
    with within_tolerance=False (the float gate doesn't conflate the two)."""
    r = check_currency_float_in_comparison(
        draft=Decimal("500000"),
        kfr=Decimal("1000000"),
    )
    assert r.success is True
    assert r.within_tolerance is False
