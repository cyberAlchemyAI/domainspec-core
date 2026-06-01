"""Tests for F-CURRENCY-CONTEXT-MISMATCH gate wrapper (Cycle 1 RT-04 + RT-05 + DC-01 + E-03 closure).

Wrapper-layer tests covering success path + every failure-leg shape +
dataclass field population.
"""

from __future__ import annotations

import decimal

import pytest

from pipeline.logician.currency.decimal_arithmetic import (
    F_CURRENCY_CONTEXT_MISMATCH,
    KFR_DECIMAL_CONTEXT,
)
from pipeline.logician.gates.f_currency_context_mismatch import (
    CurrencyContextMismatchResult,
    check_currency_context_mismatch,
)


class TestSuccessPath:
    def test_singleton_kfr_context_passes(self) -> None:
        result = check_currency_context_mismatch(context=KFR_DECIMAL_CONTEXT)
        assert result.success is True
        assert result.failure_code is None
        assert "singleton" in result.detail


class TestFailureLegs:
    def test_non_decimal_context_fails(self) -> None:
        result = check_currency_context_mismatch(context="not-a-context")
        assert result.success is False
        assert result.failure_code == F_CURRENCY_CONTEXT_MISMATCH
        assert "decimal.Context" in result.detail

    def test_none_context_is_caught_at_mismatch_layer(self) -> None:
        # MISMATCH catches non-Context types; OMITTED catches None.
        # When None reaches MISMATCH, the isinstance check fails too.
        result = check_currency_context_mismatch(context=None)
        assert result.success is False
        assert result.failure_code == F_CURRENCY_CONTEXT_MISMATCH

    def test_structurally_equivalent_but_distinct_context_fails(self) -> None:
        # A different decimal.Context object with the same prec/rounding
        # still fails — identity check, not structural.
        twin = decimal.Context(
            prec=KFR_DECIMAL_CONTEXT.prec,
            rounding=KFR_DECIMAL_CONTEXT.rounding,
            traps=dict(KFR_DECIMAL_CONTEXT.traps),
        )
        assert twin is not KFR_DECIMAL_CONTEXT
        result = check_currency_context_mismatch(context=twin)
        assert result.success is False
        assert result.failure_code == F_CURRENCY_CONTEXT_MISMATCH
        assert "identity" in result.detail.lower() or "is KFR" in result.detail

    def test_int_context_fails_with_typename_in_detail(self) -> None:
        result = check_currency_context_mismatch(context=42)
        assert result.success is False
        assert result.failure_code == F_CURRENCY_CONTEXT_MISMATCH
        assert "int" in result.detail


class TestResultDataclassImmutability:
    def test_result_is_frozen(self) -> None:
        result = check_currency_context_mismatch(context=KFR_DECIMAL_CONTEXT)
        with pytest.raises((AttributeError, Exception)):
            result.success = False  # type: ignore[misc]
