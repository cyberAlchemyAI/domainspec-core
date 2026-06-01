"""F-CURRENCY-CONTEXT-OMITTED — currency PRE-runtime gate (M1 §6.2.1).

RT-07 closure leg 1.  Every currency helper REQUIRES the caller to
pass ``context=KFR_DECIMAL_CONTEXT`` explicitly; omission is
fail-closed.

Wrapper-style gate: callers that already invoke the helper directly
get the failure raised; this gate exists so the gate-runner has a
named code to dispatch on when the helper raises.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Optional

from pipeline.logician.currency.decimal_arithmetic import (
    CurrencyContextError,
    F_CURRENCY_CONTEXT_OMITTED,
)


@dataclass(frozen=True, kw_only=True)
class CurrencyContextOmittedResult:
    success: bool
    failure_code: Optional[str]
    detail: str


def check_currency_context_omitted(
    *,
    context: Any,
) -> CurrencyContextOmittedResult:
    """PRE-runtime gate: refuse helper calls with ``context=None``.

    The gate is a thin pre-flight check the gate-runner can fire on
    any helper invocation BEFORE the helper itself; surfaced
    separately from the runtime raise so audit trails distinguish
    "operator forgot to pass context" from other context drift.
    """
    if context is None:
        return CurrencyContextOmittedResult(
            success=False,
            failure_code=F_CURRENCY_CONTEXT_OMITTED,
            detail=(
                "currency helper invoked with context=None — caller must "
                "pass KFR_DECIMAL_CONTEXT explicitly (RT-07 closure leg 1)"
            ),
        )
    return CurrencyContextOmittedResult(
        success=True,
        failure_code=None,
        detail="currency helper invoked with non-None context",
    )


__all__ = [
    "F_CURRENCY_CONTEXT_OMITTED",
    "CurrencyContextError",
    "CurrencyContextOmittedResult",
    "check_currency_context_omitted",
]
