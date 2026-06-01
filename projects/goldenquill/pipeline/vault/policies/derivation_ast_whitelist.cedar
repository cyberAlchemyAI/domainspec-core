// pipeline/vault/policies/derivation_ast_whitelist.cedar
// SKELETON — paired with pipeline/logician/derivation/ast_whitelist.py.
//
// Architecture authority:
//   - architecture v7.0.4-M1 §3 (CF-RT-02 closure)
//   - blueprint section_04_v2_x_amendment.md §6 row M1-7
//
// Denies surface as:
//   F-DERIVATION-AST-FORBIDDEN-NODE.<sub_tag>
//
// Sub-tags include: bool_constant, float_constant, constant_type,
//   forbidden_identifier, forbidden_attribute, non_kfr_facts_subscript,
//   ast_index_wrapper, ast_slice, subscript_slice_not_constant,
//   subscript_slice_not_string, subscript_key_dunder,
//   subscript_key_empty, binop_operator, unaryop_operator.

// Rule 1 — derivation_formula_whitelisted
// Permits derivation override write or POST-eval read when the AST
// has been validated through the explicit-allow-list visitor and
// every node passed.
permit (
  principal,
  action == VaultAction::"derivation-formula-validate",
  resource
)
when {
  resource has ast_whitelisted &&
  resource.ast_whitelisted == true &&
  resource has formula_chain_depth &&
  resource.formula_chain_depth == 1
};

// Rule 2 — derivation_decimal_context_active
// Permits derivation evaluation when the runtime is operating under
// KFR_DECIMAL_CONTEXT (drift guard from §6.2.1).
permit (
  principal,
  action == VaultAction::"derivation-evaluate",
  resource
)
when {
  resource has decimal_context_active &&
  resource.decimal_context_active == true &&
  resource has ast_whitelisted &&
  resource.ast_whitelisted == true
};
