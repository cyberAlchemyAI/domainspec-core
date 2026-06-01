"""F-DERIVATION-AST-FORBIDDEN-NODE gate tests (M1 §3)."""

from __future__ import annotations

from pipeline.logician.gates.f_derivation_ast_forbidden_node import (
    F_DERIVATION_AST_FORBIDDEN_NODE,
    check_derivation_ast_forbidden_node,
)


def test_failure_code_constant() -> None:
    assert F_DERIVATION_AST_FORBIDDEN_NODE == "F-DERIVATION-AST-FORBIDDEN-NODE"


def test_clean_formula_passes() -> None:
    r = check_derivation_ast_forbidden_node(
        formula='kfr_facts["a"].value + kfr_facts["b"].value'
    )
    assert r.success is True
    assert r.parsed is not None
    assert r.parsed.fact_id_refs == ("a", "b")


def test_call_node_fails() -> None:
    r = check_derivation_ast_forbidden_node(
        formula='__import__("os").system("rm")'
    )
    assert r.success is False
    assert r.failure_code == F_DERIVATION_AST_FORBIDDEN_NODE


def test_dunder_subscript_fails() -> None:
    r = check_derivation_ast_forbidden_node(
        formula='kfr_facts["__class__"].value'
    )
    assert r.success is False
    assert r.failure_code == F_DERIVATION_AST_FORBIDDEN_NODE


def test_float_literal_fails() -> None:
    r = check_derivation_ast_forbidden_node(
        formula='kfr_facts["a"].value * 0.5'
    )
    assert r.success is False
    assert r.failure_code == F_DERIVATION_AST_FORBIDDEN_NODE


def test_parse_error_fails() -> None:
    r = check_derivation_ast_forbidden_node(formula="1 +")
    assert r.success is False
    assert r.failure_code == F_DERIVATION_AST_FORBIDDEN_NODE
    assert r.offending_node_type == "parse_error"
