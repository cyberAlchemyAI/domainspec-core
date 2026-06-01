"""Tests for F-CURRENCY-CONTEXT-OMITTED gate wrapper (Cycle 1 RT-04 + RT-05 + DC-01 + E-03 closure).

Wrapper-layer tests covering success path + every failure-leg shape +
dataclass field population. Helper-layer tests live in
`tests/logician/currency/test_decimal_arithmetic.py`.
"""

from __future__ import annotations

import pytest

from pipeline.logician.currency.decimal_arithmetic import (
    F_CURRENCY_CONTEXT_OMITTED,
    KFR_DECIMAL_CONTEXT,
)
from pipeline.logician.gates.f_currency_context_omitted import (
    CurrencyContextOmittedResult,
    check_currency_context_omitted,
)


class TestSuccessPath:
    def test_non_none_context_passes(self) -> None:
        result = check_currency_context_omitted(context=KFR_DECIMAL_CONTEXT)
        assert result.success is True
        assert result.failure_code is None
        assert "non-None context" in result.detail

    def test_arbitrary_non_none_context_passes_at_omitted_layer(self) -> None:
        # The omitted gate only catches None; identity-mismatch is the
        # MISMATCH gate's surface (RT-07 closure leg 2).
        result = check_currency_context_omitted(context=object())
        assert result.success is True
        assert result.failure_code is None


class TestFailurePathDataclassFields:
    def test_none_context_fails_with_dataclass_fields_populated(self) -> None:
        result = check_currency_context_omitted(context=None)
        assert result.success is False
        assert result.failure_code == F_CURRENCY_CONTEXT_OMITTED
        assert isinstance(result.detail, str)
        assert result.detail  # non-empty
        assert "context=None" in result.detail or "None" in result.detail

    def test_failure_detail_references_caller_responsibility(self) -> None:
        result = check_currency_context_omitted(context=None)
        assert "KFR_DECIMAL_CONTEXT" in result.detail


class TestResultDataclassImmutability:
    def test_result_is_frozen(self) -> None:
        result = check_currency_context_omitted(context=KFR_DECIMAL_CONTEXT)
        with pytest.raises((AttributeError, Exception)):  # FrozenInstanceError
            result.success = False  # type: ignore[misc]

    def test_failure_code_constant_matches_module_export(self) -> None:
        from pipeline.logician.gates import f_currency_context_omitted as mod
        assert mod.F_CURRENCY_CONTEXT_OMITTED == F_CURRENCY_CONTEXT_OMITTED
        assert F_CURRENCY_CONTEXT_OMITTED.startswith("F-CURRENCY-CONTEXT-OMITTED")
