"""R-REPORT-DECIMAL-MANDATE — AST-lint rule (§14 v1 LOCK Cycle-2 RT-C2-01).

Per §14 v1 LOCKED 2026-05-10 §14.9.4 + Cycle 2 RT-C2-01 closure + v7.0.4-M1
Decimal mandate + WS-J Slice 3 handoff (2026-05-11).

Scope (per RT-C2-01 closure — EXTENDED beyond gate modules):

* ``pipeline/logician/gates/f_report_*.py`` — gate predicate bodies
* ``pipeline/orchestrator/seats/report_generator/**/*.py`` — composer
  bodies, claim_evidence_map signer, schemas
* ``pipeline/orchestrator/tracks/report_mode.py`` — track-mode entry
  point

Forbids the following ``float`` defects:

(a) ``float(...)`` constructor call inside any function body — explicit
    float coercion of substrate values.
(b) Float-literal arithmetic — ``ast.BinOp`` whose operand is an
    ``ast.Constant`` with a ``float`` value.
(c) ``==`` / ``!=`` / ``<`` / ``<=`` / ``>`` / ``>=`` ``ast.Compare``
    whose immediate operand is a ``float`` literal.
(d) ``Decimal(float_literal)`` constructor — common gotcha; Decimal must
    be built from int / str.

Float literals inside test fixtures are allowed; the rule scopes by glob
so ``tests/`` is never matched. Comment-only float references (e.g.,
``# tolerance defaults to 0.0 — sentinel``) are unaffected because
comments are not in the AST.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation


_REPORT_GATES_GLOB = "pipeline/logician/gates/f_report_*.py"
_REPORT_GENERATOR_GLOB = "pipeline/orchestrator/seats/report_generator/**/*.py"
_REPORT_MODE_GLOB = "pipeline/orchestrator/tracks/report_mode.py"


def _is_float_constant(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Constant)
        and isinstance(node.value, float)
        and not isinstance(node.value, bool)
    )


def _check_report_decimal_mandate(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        # (a) float(...) coercion.
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "float":
                yield Violation(
                    rule_name="R-REPORT-DECIMAL-MANDATE",
                    reason_tag="float_coercion",
                    file=path,
                    line=node.lineno,
                    col=node.col_offset,
                    message=(
                        "`float(...)` call in §14 substrate — Decimal "
                        "mandate per v7.0.4-M1 / R-REPORT-DECIMAL-MANDATE"
                    ),
                )
            # (d) Decimal(float_literal)
            if (
                isinstance(func, ast.Name)
                and func.id == "Decimal"
                and node.args
                and _is_float_constant(node.args[0])
            ):
                first = node.args[0]
                yield Violation(
                    rule_name="R-REPORT-DECIMAL-MANDATE",
                    reason_tag="decimal_constructed_from_float",
                    file=path,
                    line=first.lineno,
                    col=first.col_offset,
                    message=(
                        f"`Decimal({first.value!r})` — Decimal must be "
                        "constructed from int / str, never float "
                        "(R-REPORT-DECIMAL-MANDATE)"
                    ),
                )
        # (b) Float-literal arithmetic.
        if isinstance(node, ast.BinOp):
            if _is_float_constant(node.left) or _is_float_constant(node.right):
                offender = node.left if _is_float_constant(node.left) else node.right
                yield Violation(
                    rule_name="R-REPORT-DECIMAL-MANDATE",
                    reason_tag="float_arithmetic",
                    file=path,
                    line=offender.lineno,
                    col=offender.col_offset,
                    message=(
                        f"float literal {getattr(offender, 'value', '?')!r} "
                        "in arithmetic expression — Decimal mandate per "
                        "v7.0.4-M1 / R-REPORT-DECIMAL-MANDATE"
                    ),
                )
        # (c) Float-literal comparison.
        if isinstance(node, ast.Compare):
            for operand in [node.left] + list(node.comparators):
                if _is_float_constant(operand):
                    yield Violation(
                        rule_name="R-REPORT-DECIMAL-MANDATE",
                        reason_tag="float_comparison",
                        file=path,
                        line=operand.lineno,
                        col=operand.col_offset,
                        message=(
                            f"float literal {operand.value!r} in comparison "
                            "expression — Decimal mandate per v7.0.4-M1 / "
                            "R-REPORT-DECIMAL-MANDATE"
                        ),
                    )


def _check_multi_glob(tree: ast.AST, path: Path) -> Iterator[Violation]:
    """Multi-glob wrapper covering all three scope branches per RT-C2-01."""
    from pipeline.linting.ast_lint import _glob_matches_path

    if not any(
        _glob_matches_path(g, path)
        for g in (_REPORT_GATES_GLOB, _REPORT_GENERATOR_GLOB, _REPORT_MODE_GLOB)
    ):
        return
    yield from _check_report_decimal_mandate(tree, path)


REPORT_DECIMAL_MANDATE: Rule = Rule(
    name="R-REPORT-DECIMAL-MANDATE",
    reason_tag="report_decimal_mandate",
    target_glob="pipeline/**/*.py",
    check=_check_multi_glob,
    description=(
        "Forbid float() coercion, float-literal arithmetic, float-literal "
        "comparison, and Decimal(float_literal) in §14 Report Generator "
        "substrate per v7.0.4-M1 Decimal mandate + Cycle 2 RT-C2-01 closure "
        "(scope: gates + composers + report_mode)."
    ),
)


__all__ = ["REPORT_DECIMAL_MANDATE"]
