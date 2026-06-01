"""F-DERIVATION-RUNTIME-ARITHMETIC-ERROR tests (M1 §8.1)."""

from __future__ import annotations

import decimal

from pipeline.logician.gates.f_derivation_runtime_arithmetic_error import (
    F_DERIVATION_RUNTIME_ARITHMETIC_ERROR,
    SUB_TAG_DIVIDE_BY_ZERO,
    SUB_TAG_INVALID_OPERATION,
    SUB_TAG_OTHER,
    SUB_TAG_OVERFLOW,
    check_derivation_runtime_arithmetic_error,
    classify_arithmetic_error,
)


def test_failure_code_constant() -> None:
    assert (
        F_DERIVATION_RUNTIME_ARITHMETIC_ERROR
        == "F-DERIVATION-RUNTIME-ARITHMETIC-ERROR"
    )


def test_no_error_passes() -> None:
    r = check_derivation_runtime_arithmetic_error(
        derivation_id="D1",
        arithmetic_error=None,
    )
    assert r.success is True


def test_division_by_zero_classified() -> None:
    err = decimal.DivisionByZero("divide")
    r = check_derivation_runtime_arithmetic_error(
        derivation_id="D1",
        arithmetic_error=err,
    )
    assert r.success is False
    assert r.failure_code == (
        f"{F_DERIVATION_RUNTIME_ARITHMETIC_ERROR}.{SUB_TAG_DIVIDE_BY_ZERO}"
    )


def test_overflow_classified() -> None:
    err = decimal.Overflow("overflow")
    r = check_derivation_runtime_arithmetic_error(
        derivation_id="D1",
        arithmetic_error=err,
    )
    assert r.failure_code == (
        f"{F_DERIVATION_RUNTIME_ARITHMETIC_ERROR}.{SUB_TAG_OVERFLOW}"
    )


def test_invalid_operation_classified() -> None:
    err = decimal.InvalidOperation("op")
    r = check_derivation_runtime_arithmetic_error(
        derivation_id="D1",
        arithmetic_error=err,
    )
    assert r.failure_code == (
        f"{F_DERIVATION_RUNTIME_ARITHMETIC_ERROR}.{SUB_TAG_INVALID_OPERATION}"
    )


def test_other_exception_classified() -> None:
    r = check_derivation_runtime_arithmetic_error(
        derivation_id="D1",
        arithmetic_error=ValueError("unexpected"),
    )
    assert r.failure_code == (
        f"{F_DERIVATION_RUNTIME_ARITHMETIC_ERROR}.{SUB_TAG_OTHER}"
    )


def test_classify_arithmetic_error_helper() -> None:
    assert classify_arithmetic_error(decimal.DivisionByZero()) == SUB_TAG_DIVIDE_BY_ZERO
    assert classify_arithmetic_error(decimal.Overflow()) == SUB_TAG_OVERFLOW
    assert classify_arithmetic_error(decimal.InvalidOperation()) == SUB_TAG_INVALID_OPERATION
    assert classify_arithmetic_error(RuntimeError()) == SUB_TAG_OTHER
