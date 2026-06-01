"""Currency context-gate trio tests (M1 §6.2.1).

* F-CURRENCY-CONTEXT-OMITTED
* F-CURRENCY-CONTEXT-MISMATCH
* F-CURRENCY-DECIMAL-CONTEXT-DRIFT
"""

from __future__ import annotations

import decimal

import pytest

from pipeline.logician.currency import KFR_DECIMAL_CONTEXT
from pipeline.logician.gates.f_currency_context_mismatch import (
    F_CURRENCY_CONTEXT_MISMATCH,
    check_currency_context_mismatch,
)
from pipeline.logician.gates.f_currency_context_omitted import (
    F_CURRENCY_CONTEXT_OMITTED,
    check_currency_context_omitted,
)
from pipeline.logician.gates.f_currency_decimal_context_drift import (
    F_CURRENCY_DECIMAL_CONTEXT_DRIFT,
    check_currency_decimal_context_drift,
)


def test_omitted_failure_code_constant() -> None:
    assert F_CURRENCY_CONTEXT_OMITTED == "F-CURRENCY-CONTEXT-OMITTED"


def test_mismatch_failure_code_constant() -> None:
    assert F_CURRENCY_CONTEXT_MISMATCH == "F-CURRENCY-CONTEXT-MISMATCH"


def test_drift_failure_code_constant() -> None:
    assert F_CURRENCY_DECIMAL_CONTEXT_DRIFT == "F-CURRENCY-DECIMAL-CONTEXT-DRIFT"


def test_context_omitted_fails() -> None:
    r = check_currency_context_omitted(context=None)
    assert r.success is False
    assert r.failure_code == F_CURRENCY_CONTEXT_OMITTED


def test_context_present_passes() -> None:
    r = check_currency_context_omitted(context=KFR_DECIMAL_CONTEXT)
    assert r.success is True


def test_context_identity_match_passes() -> None:
    r = check_currency_context_mismatch(context=KFR_DECIMAL_CONTEXT)
    assert r.success is True


def test_context_identity_mismatch_fails() -> None:
    other = decimal.Context(prec=28, rounding=decimal.ROUND_HALF_EVEN)
    r = check_currency_context_mismatch(context=other)
    assert r.success is False
    assert r.failure_code == F_CURRENCY_CONTEXT_MISMATCH


def test_context_non_context_fails() -> None:
    r = check_currency_context_mismatch(context="not a context")
    assert r.success is False
    assert r.failure_code == F_CURRENCY_CONTEXT_MISMATCH


def test_context_drift_passes_under_default() -> None:
    r = check_currency_decimal_context_drift()
    assert r.success is True


def test_context_drift_fires_under_drift() -> None:
    saved = decimal.getcontext()
    decimal.setcontext(decimal.Context(prec=10))
    try:
        r = check_currency_decimal_context_drift()
        assert r.success is False
        assert r.failure_code == F_CURRENCY_DECIMAL_CONTEXT_DRIFT
    finally:
        decimal.setcontext(saved)
