"""AST whitelist tests for derivation formulas (architecture v7.0.4-M1 §3)."""

from __future__ import annotations

import pytest

from pipeline.logician.derivation import (
    AstWhitelistError,
    DerivationParseError,
    validate_derivation_formula,
)


# ---- Accepting forms -------------------------------------------------------


def test_simple_subscript_accepted() -> None:
    parsed = validate_derivation_formula('kfr_facts["a"].value')
    assert parsed.fact_id_refs == ("a",)


def test_two_factor_addition_accepted() -> None:
    parsed = validate_derivation_formula(
        'kfr_facts["a"].value + kfr_facts["b"].value'
    )
    assert parsed.fact_id_refs == ("a", "b")


def test_division_with_int_literal_accepted() -> None:
    parsed = validate_derivation_formula(
        'kfr_facts["enrolled"].value / kfr_facts["total"].value'
    )
    assert parsed.fact_id_refs == ("enrolled", "total")


def test_unary_minus_accepted() -> None:
    parsed = validate_derivation_formula('-kfr_facts["a"].value')
    assert parsed.fact_id_refs == ("a",)


def test_decimal_string_constant_accepted() -> None:
    """ast.Constant of str is admitted (Decimal-string literal)."""
    parsed = validate_derivation_formula('kfr_facts["a"].value * "100"')
    assert parsed.fact_id_refs == ("a",)


def test_int_constant_accepted() -> None:
    parsed = validate_derivation_formula('kfr_facts["a"].value + 5')
    assert parsed.fact_id_refs == ("a",)


def test_dedup_fact_ids_in_complex_formula() -> None:
    parsed = validate_derivation_formula(
        'kfr_facts["a"].value + kfr_facts["a"].value * kfr_facts["b"].value'
    )
    assert parsed.fact_id_refs == ("a", "b")


# ---- Rejecting forms (per §3.2 forbidden-list + RT closures) ---------------


def test_call_node_refused() -> None:
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula('__import__("os").system("rm -rf /")')


def test_dunder_name_refused() -> None:
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula('kfr_facts["a"].__class__')


def test_dunder_subscript_string_refused() -> None:
    """RT-04 closure — string contents must not contain '__'."""
    with pytest.raises(AstWhitelistError) as exc:
        validate_derivation_formula('kfr_facts["__class__"].value')
    assert "subscript_key_dunder" in (
        exc.value.offending_detail or ""
    ) or exc.value.offending_node_type == "Constant"


def test_other_attribute_name_refused() -> None:
    """Only ``.value`` admitted; ``.tolerance_pct`` etc. refused."""
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula('kfr_facts["a"].tolerance_pct')


def test_other_name_id_refused() -> None:
    """Only ``kfr_facts`` admitted as Name id."""
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula('cache["a"].value')


def test_float_constant_refused() -> None:
    """RT-10 closure — float literals refused."""
    with pytest.raises(AstWhitelistError) as exc:
        validate_derivation_formula('kfr_facts["a"].value * 0.5')
    assert exc.value.offending_node_type == "Constant"


def test_bool_constant_refused() -> None:
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula('kfr_facts["a"].value * True')


def test_compare_refused() -> None:
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula('kfr_facts["a"].value > 100')


def test_boolop_refused() -> None:
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula(
            'kfr_facts["a"].value and kfr_facts["b"].value'
        )


def test_lambda_refused() -> None:
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula('lambda x: x')


def test_list_literal_refused() -> None:
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula('[kfr_facts["a"].value]')


def test_nested_subscript_refused() -> None:
    """Subscript value must be ast.Name(id='kfr_facts'), no nesting."""
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula(
            'kfr_facts[kfr_facts["a"].value].value'
        )


def test_slice_subscript_refused() -> None:
    """ast.Slice (e.g., ``[1:2]``) refused."""
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula('kfr_facts["a":"b"].value')


def test_modulo_operator_refused() -> None:
    """``%`` not in allowed binop set."""
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula(
            'kfr_facts["a"].value % kfr_facts["b"].value'
        )


def test_floordiv_operator_refused() -> None:
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula(
            'kfr_facts["a"].value // kfr_facts["b"].value'
        )


def test_power_operator_refused() -> None:
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula(
            'kfr_facts["a"].value ** 2'
        )


def test_invalid_syntax_refused() -> None:
    with pytest.raises(DerivationParseError):
        validate_derivation_formula("1 +")


def test_non_string_input_refused() -> None:
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula(123)  # type: ignore[arg-type]


def test_subscript_int_key_refused() -> None:
    """Subscript slice must be str-typed Constant, not int."""
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula('kfr_facts[0].value')


def test_empty_subscript_key_refused() -> None:
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula('kfr_facts[""].value')


def test_subscript_with_leading_underscore_refused() -> None:
    """Identifier discipline — refusing ``_`` patterns at the fact_id level
    is RT-04 leg 2 (substring pattern).  ``_a`` does not contain '__' but
    the visitor's identifier discipline still rejects via dunder substring
    check on string contents only — leading single underscore in a fact_id
    is admitted as long as it doesn't contain '__'.
    """
    parsed = validate_derivation_formula('kfr_facts["_a"].value')
    assert parsed.fact_id_refs == ("_a",)


def test_subscript_with_trailing_double_underscore_refused() -> None:
    with pytest.raises(AstWhitelistError):
        validate_derivation_formula('kfr_facts["foo__"].value')
