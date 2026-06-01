"""Tests for F-CURRENCY-DECIMAL-CONTEXT-DRIFT gate wrapper (Cycle 1 RT-04 + RT-05 + DC-01 + E-03 closure).

Wrapper-layer tests covering success path + every failure-leg shape +
dataclass field population. Helper-layer tests for
`assert_kfr_context_active` live in
`tests/logician/currency/test_decimal_arithmetic.py`.
"""

from __future__ import annotations

import decimal
from contextlib import contextmanager

import pytest

from pipeline.logician.currency.decimal_arithmetic import (
    F_CURRENCY_DECIMAL_CONTEXT_DRIFT,
    KFR_DECIMAL_CONTEXT,
)
from pipeline.logician.gates.f_currency_decimal_context_drift import (
    CurrencyContextDriftResult,
    check_currency_decimal_context_drift,
)


@contextmanager
def kfr_context_temporarily_active():
    """Set decimal.getcontext() to KFR semantics for the duration."""
    saved = decimal.getcontext()
    try:
        snapshot = decimal.Context(
            prec=KFR_DECIMAL_CONTEXT.prec,
            rounding=KFR_DECIMAL_CONTEXT.rounding,
            traps=dict(KFR_DECIMAL_CONTEXT.traps),
        )
        decimal.setcontext(snapshot)
        yield
    finally:
        decimal.setcontext(saved)


class TestSuccessPath:
    def test_when_kfr_semantics_active_passes(self) -> None:
        with kfr_context_temporarily_active():
            result = check_currency_decimal_context_drift()
        assert result.success is True
        assert result.failure_code is None
        assert "matches" in result.detail.lower()


class TestFailurePath:
    def test_low_precision_drift_fails(self) -> None:
        saved = decimal.getcontext()
        try:
            decimal.setcontext(decimal.Context(prec=4, rounding=decimal.ROUND_DOWN))
            result = check_currency_decimal_context_drift()
        finally:
            decimal.setcontext(saved)
        assert result.success is False
        assert result.failure_code == F_CURRENCY_DECIMAL_CONTEXT_DRIFT

    def test_failure_detail_is_non_empty(self) -> None:
        saved = decimal.getcontext()
        try:
            decimal.setcontext(decimal.Context(prec=2))
            result = check_currency_decimal_context_drift()
        finally:
            decimal.setcontext(saved)
        assert result.success is False
        assert isinstance(result.detail, str) and result.detail


class TestResultDataclassImmutability:
    def test_result_is_frozen(self) -> None:
        with kfr_context_temporarily_active():
            result = check_currency_decimal_context_drift()
        with pytest.raises((AttributeError, Exception)):
            result.success = False  # type: ignore[misc]

    def test_failure_code_constant_export_aligns(self) -> None:
        assert F_CURRENCY_DECIMAL_CONTEXT_DRIFT.startswith(
            "F-CURRENCY-DECIMAL-CONTEXT-DRIFT"
        )
