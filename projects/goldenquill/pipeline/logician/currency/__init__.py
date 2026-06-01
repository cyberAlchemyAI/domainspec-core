"""KFR currency Decimal mandate (architecture v7.0.4-M1 §6)."""

from pipeline.logician.currency.decimal_arithmetic import (
    F_CURRENCY_CONTEXT_MISMATCH,
    F_CURRENCY_CONTEXT_OMITTED,
    F_CURRENCY_DECIMAL_CONTEXT_DRIFT,
    F_CURRENCY_FLOAT_IN_COMPARISON,
    F_CURRENCY_UNIT_MISMATCH,
    KFR_DECIMAL_CONTEXT,
    UNIT_CONVERSION_TABLE,
    CurrencyContextError,
    CurrencyFloatError,
    CurrencyUnitMismatchError,
    UnitConversionError,
    assert_kfr_context_active,
    canonicalize_unit,
    convert_to_canonical_unit,
    to_currency,
    tolerance_check_currency,
)

__all__ = [
    "F_CURRENCY_CONTEXT_MISMATCH",
    "F_CURRENCY_CONTEXT_OMITTED",
    "F_CURRENCY_DECIMAL_CONTEXT_DRIFT",
    "F_CURRENCY_FLOAT_IN_COMPARISON",
    "F_CURRENCY_UNIT_MISMATCH",
    "KFR_DECIMAL_CONTEXT",
    "UNIT_CONVERSION_TABLE",
    "CurrencyContextError",
    "CurrencyFloatError",
    "CurrencyUnitMismatchError",
    "UnitConversionError",
    "assert_kfr_context_active",
    "canonicalize_unit",
    "convert_to_canonical_unit",
    "to_currency",
    "tolerance_check_currency",
]
