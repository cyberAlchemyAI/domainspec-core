// pipeline/vault/policies/currency_decimal.cedar
// SKELETON — paired with pipeline/logician/currency/decimal_arithmetic.py.
//
// Architecture authority:
//   - architecture v7.0.4-M1 §6 (DC-CF-02 closure — Decimal mandate)
//   - architecture v7.0.4-M1 §8.2 (CF-RT-06 unit-conversion)
//   - blueprint section_04_v2_x_amendment.md §6 row M1-12 .. M1-16
//
// Denies surface as:
//   F-CURRENCY-FLOAT-IN-COMPARISON
//   F-CURRENCY-CONTEXT-OMITTED
//   F-CURRENCY-CONTEXT-MISMATCH
//   F-CURRENCY-DECIMAL-CONTEXT-DRIFT
//   F-CURRENCY-UNIT-MISMATCH

// Rule 1 — currency_helper_invocation_disciplined
// Permits a currency helper call ONLY when KFR_DECIMAL_CONTEXT is
// passed explicitly (identity match) AND no float reaches the helper.
permit (
  principal,
  action == VaultAction::"currency-helper-invoke",
  resource
)
when {
  resource has context_explicit &&
  resource.context_explicit == true &&
  resource has context_identity_match &&
  resource.context_identity_match == true &&
  resource has float_input_present &&
  resource.float_input_present == false
};

// Rule 2 — currency_runtime_context_intact
// Permits a currency tolerance comparison ONLY when
// decimal.getcontext() matches KFR_DECIMAL_CONTEXT semantics
// (prec=28, ROUND_HALF_EVEN, traps include InvalidOperation/
// DivisionByZero/Overflow).
permit (
  principal,
  action == VaultAction::"currency-tolerance-compare",
  resource
)
when {
  resource has runtime_context_matches &&
  resource.runtime_context_matches == true &&
  resource has prec_matches &&
  resource.prec_matches == true &&
  resource has rounding_matches &&
  resource.rounding_matches == true
};

// Rule 3 — currency_unit_convertible
// Permits a tolerance comparison across two unit strings ONLY when
// both canonicalize to the same canonical unit (per the conversion
// table in §6.2.1 / §8.2).
permit (
  principal,
  action == VaultAction::"currency-tolerance-compare",
  resource
)
when {
  resource has draft_canonical_unit &&
  resource has kfr_canonical_unit &&
  resource.draft_canonical_unit == resource.kfr_canonical_unit
};
