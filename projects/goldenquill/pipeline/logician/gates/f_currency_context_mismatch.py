"""F-CURRENCY-CONTEXT-MISMATCH — currency PRE-runtime gate (M1 §6.2.1).

RT-07 closure leg 2.  Helper call MUST pass the singleton
:data:`KFR_DECIMAL_CONTEXT`; passing any other context (even one
that happens to share prec/rounding/traps) fails-closed.
"""

from __future__ import annotations

import decimal
from dataclasses import dataclass
from typing import Any, Final, Optional

from pipeline.logician.currency.decimal_arithmetic import (
    F_CURRENCY_CONTEXT_MISMATCH,
    KFR_DECIMAL_CONTEXT,
)


@dataclass(frozen=True, kw_only=True)
class CurrencyContextMismatchResult:
    success: bool
    failure_code: Optional[str]
    detail: str


def check_currency_context_mismatch(
    *,
    context: Any,
) -> CurrencyContextMismatchResult:
    """PRE-runtime gate: identity-check on the passed Decimal context."""
    if not isinstance(context, decimal.Context):
        return CurrencyContextMismatchResult(
            success=False,
            failure_code=F_CURRENCY_CONTEXT_MISMATCH,
            detail=(
                f"context must be decimal.Context, got "
                f"{type(context).__name__}"
            ),
        )
    if context is not KFR_DECIMAL_CONTEXT:
        return CurrencyContextMismatchResult(
            success=False,
            failure_code=F_CURRENCY_CONTEXT_MISMATCH,
            detail=(
                "currency helper invoked with non-KFR_DECIMAL_CONTEXT "
                "instance — RT-07 closure leg 2 requires identity "
                "match (`context is KFR_DECIMAL_CONTEXT`), not just "
                "structurally-equivalent context"
            ),
        )
    return CurrencyContextMismatchResult(
        success=True,
        failure_code=None,
        detail="currency helper invoked with the singleton KFR_DECIMAL_CONTEXT",
    )


__all__ = [
    "F_CURRENCY_CONTEXT_MISMATCH",
    "CurrencyContextMismatchResult",
    "check_currency_context_mismatch",
]
