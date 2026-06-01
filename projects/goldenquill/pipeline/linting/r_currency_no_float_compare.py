"""R-CURRENCY-NO-FLOAT-COMPARE — AST-lint rule (architecture v7.0.4-M1 §6.2.3).

Layer 2 defense in the three-layer currency-float ban.  Forbids
``float`` literals adjacent to currency-typed Decimal arithmetic in
``pipeline/logician/currency/**`` and ``pipeline/logician/gates/f_currency_*``.

Targets:

* ``ast.Compare`` whose operands include any ``float`` literal.
* ``ast.BinOp`` whose operands include any ``float`` literal AND the
  containing module path matches the currency glob.
* ``Decimal(...)`` calls whose first argument is an ``ast.Constant``
  of type ``float``.

Pure-Python; runs as part of :data:`pipeline.linting.ast_lint.DEFAULT_RULES`.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation


_CURRENCY_TARGET_GLOB = "pipeline/logician/currency/**/*.py"
_CURRENCY_GATE_GLOB = "pipeline/logician/gates/f_currency_*.py"


def _check_currency_no_float_compare(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            yield Violation(
                rule_name="R-CURRENCY-NO-FLOAT-COMPARE",
                reason_tag="float_literal_in_currency_module",
                file=path,
                line=node.lineno,
                col=node.col_offset,
                message=(
                    f"float literal {node.value!r} present in currency "
                    "module — currency arithmetic must use Decimal "
                    "(F-CURRENCY-FLOAT-IN-COMPARISON guard)"
                ),
            )
        if isinstance(node, ast.Call):
            if (
                isinstance(node.func, ast.Name)
                and node.func.id == "Decimal"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, float)
            ):
                first = node.args[0]
                yield Violation(
                    rule_name="R-CURRENCY-NO-FLOAT-COMPARE",
                    reason_tag="decimal_constructed_from_float",
                    file=path,
                    line=first.lineno,
                    col=first.col_offset,
                    message=(
                        f"Decimal({first.value!r}) — Decimal must be "
                        "constructed from int / str, never float"
                    ),
                )


CURRENCY_NO_FLOAT_COMPARE: Rule = Rule(
    name="R-CURRENCY-NO-FLOAT-COMPARE",
    reason_tag="currency_no_float_compare",
    target_glob=_CURRENCY_TARGET_GLOB,
    check=_check_currency_no_float_compare,
    description=(
        "Forbid float literals in pipeline/logician/currency/** and "
        "Decimal(...) constructors taking float arguments."
    ),
)

# Companion rule with the same predicate but pointed at the currency
# gate modules so violations in either tree surface.
CURRENCY_GATE_NO_FLOAT_COMPARE: Rule = Rule(
    name="R-CURRENCY-NO-FLOAT-COMPARE",
    reason_tag="currency_gate_no_float_compare",
    target_glob=_CURRENCY_GATE_GLOB,
    check=_check_currency_no_float_compare,
    description=(
        "Forbid float literals / Decimal(float-literal) calls in "
        "pipeline/logician/gates/f_currency_*.py."
    ),
)


__all__ = [
    "CURRENCY_GATE_NO_FLOAT_COMPARE",
    "CURRENCY_NO_FLOAT_COMPARE",
]
