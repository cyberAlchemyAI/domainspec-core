"""F-DERIVATION-RUNTIME-ARITHMETIC-ERROR — derivation POST-eval gate (M1 §8.1).

DC-CF-01 closure.  Maps Decimal traps raised during derivation
evaluation into a structured failure code with sub-tag:

* :class:`decimal.DivisionByZero` → ``.divide_by_zero``
* :class:`decimal.Overflow` → ``.overflow``
* :class:`decimal.InvalidOperation` → ``.invalid_operation``

Severity: LOW (HARD-BLOCK the claim; logged at MEDIUM if recurring).
"""

from __future__ import annotations

import decimal
from dataclasses import dataclass
from typing import Final, Optional


F_DERIVATION_RUNTIME_ARITHMETIC_ERROR: Final[str] = (
    "F-DERIVATION-RUNTIME-ARITHMETIC-ERROR"
)

SUB_TAG_DIVIDE_BY_ZERO: Final[str] = "divide_by_zero"
SUB_TAG_OVERFLOW: Final[str] = "overflow"
SUB_TAG_INVALID_OPERATION: Final[str] = "invalid_operation"
SUB_TAG_OTHER: Final[str] = "other"

_SUB_TAG_BY_TRAP: Final[dict[type[Exception], str]] = {
    decimal.DivisionByZero: SUB_TAG_DIVIDE_BY_ZERO,
    decimal.Overflow: SUB_TAG_OVERFLOW,
    decimal.InvalidOperation: SUB_TAG_INVALID_OPERATION,
}


@dataclass(frozen=True, kw_only=True)
class DerivationArithmeticErrorResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    derivation_id: Optional[str] = None
    sub_tag: Optional[str] = None


def classify_arithmetic_error(exc: BaseException) -> str:
    """Map a Decimal trap exception to the canonical sub-tag."""
    for trap, sub_tag in _SUB_TAG_BY_TRAP.items():
        if isinstance(exc, trap):
            return sub_tag
    return SUB_TAG_OTHER


def check_derivation_runtime_arithmetic_error(
    *,
    derivation_id: str,
    arithmetic_error: Optional[BaseException],
) -> DerivationArithmeticErrorResult:
    """POST-eval gate: capture Decimal trap raised during derivation eval.

    Parameters
    ----------
    arithmetic_error
        The exception caught by the derivation evaluator (or None on
        success).  When None, the gate passes; when present, the gate
        fails with the appropriate sub-tag.
    """
    if arithmetic_error is None:
        return DerivationArithmeticErrorResult(
            success=True,
            failure_code=None,
            detail=(
                f"derivation_id={derivation_id!r} evaluated without "
                "Decimal traps"
            ),
            derivation_id=derivation_id,
        )
    sub_tag = classify_arithmetic_error(arithmetic_error)
    full_code = f"{F_DERIVATION_RUNTIME_ARITHMETIC_ERROR}.{sub_tag}"
    return DerivationArithmeticErrorResult(
        success=False,
        failure_code=full_code,
        detail=(
            f"derivation_id={derivation_id!r} raised "
            f"{type(arithmetic_error).__name__}: {arithmetic_error}"
        ),
        derivation_id=derivation_id,
        sub_tag=sub_tag,
    )


__all__ = [
    "F_DERIVATION_RUNTIME_ARITHMETIC_ERROR",
    "SUB_TAG_DIVIDE_BY_ZERO",
    "SUB_TAG_INVALID_OPERATION",
    "SUB_TAG_OTHER",
    "SUB_TAG_OVERFLOW",
    "DerivationArithmeticErrorResult",
    "check_derivation_runtime_arithmetic_error",
    "classify_arithmetic_error",
]
