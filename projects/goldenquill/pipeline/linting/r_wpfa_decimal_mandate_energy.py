"""R-WPFA-DECIMAL-MANDATE-ENERGY — AST-lint rule. [§17.3.5, §5.1.WPFA.AST_LINT]

Extends the A12 Decimal mandate (architecture v7.0.4-M1 §6) to energy
quantities. Forbids ``float`` annotations on field names matching the
regex ``(_minor_units|_micro|_saved)$`` within WPFA modules.

Targets:
  - ``pipeline/orchestrator/seats/wpfa/**/*.py``
  - ``pipeline/vault/sub_kinds/cycle_receipts.py``
  - ``pipeline/vault/sub_kinds/coefficient_registry.py``
  - ``pipeline/logician/gates/f_wpfa_*.py``
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation


_TARGET_GLOB = "pipeline/orchestrator/seats/wpfa/**/*.py"
_FIELD_NAME_RE: re.Pattern[str] = re.compile(r"(_minor_units|_micro|_saved)$")


def _is_float_annotation(annot: ast.AST) -> bool:
    if isinstance(annot, ast.Name) and annot.id == "float":
        return True
    if isinstance(annot, ast.Subscript):
        # e.g., `tuple[float, ...]`, `Optional[float]`
        return any(
            _is_float_annotation(child) for child in ast.iter_child_nodes(annot)
        )
    if isinstance(annot, ast.BinOp):
        # e.g., `float | None`
        return _is_float_annotation(annot.left) or _is_float_annotation(annot.right)
    if isinstance(annot, ast.Tuple):
        return any(_is_float_annotation(elt) for elt in annot.elts)
    if isinstance(annot, ast.Index):  # Py<3.9 compat (defensive)
        return _is_float_annotation(annot.value)  # type: ignore[attr-defined]
    return False


def _check_wpfa_decimal_mandate_energy(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            field_name = node.target.id
            if _FIELD_NAME_RE.search(field_name) and _is_float_annotation(
                node.annotation
            ):
                yield Violation(
                    rule_name="R-WPFA-DECIMAL-MANDATE-ENERGY",
                    reason_tag="float_annotation_on_int_unit_field",
                    file=path,
                    line=node.lineno,
                    col=node.col_offset,
                    message=(
                        f"field {field_name!r} matches pattern "
                        f"(_minor_units|_micro|_saved)$ but is annotated as "
                        "float; A12 Decimal mandate (extended to energy per "
                        "§17.3.5) requires int. R-WPFA-DECIMAL-MANDATE-ENERGY."
                    ),
                )
        # Also catch arg annotations in function signatures
        if isinstance(node, ast.arg) and node.annotation is not None:
            arg_name = node.arg
            if _FIELD_NAME_RE.search(arg_name) and _is_float_annotation(
                node.annotation
            ):
                yield Violation(
                    rule_name="R-WPFA-DECIMAL-MANDATE-ENERGY",
                    reason_tag="float_annotation_on_int_unit_param",
                    file=path,
                    line=node.lineno,
                    col=node.col_offset,
                    message=(
                        f"parameter {arg_name!r} matches pattern "
                        f"(_minor_units|_micro|_saved)$ but is annotated as "
                        "float; A12 Decimal mandate requires int."
                    ),
                )


WPFA_DECIMAL_MANDATE_ENERGY: Rule = Rule(
    name="R-WPFA-DECIMAL-MANDATE-ENERGY",
    reason_tag="wpfa_decimal_mandate_energy",
    target_glob=_TARGET_GLOB,
    check=_check_wpfa_decimal_mandate_energy,
    description=(
        "Extends A12 Decimal mandate to energy fields: forbid float "
        "annotations on names matching (_minor_units|_micro|_saved)$."
    ),
)


# Second target glob — coefficient_registry + cycle_receipts + WPFA gates
_TARGET_GLOB_VAULT = "pipeline/vault/sub_kinds/*.py"
WPFA_DECIMAL_MANDATE_ENERGY_VAULT: Rule = Rule(
    name="R-WPFA-DECIMAL-MANDATE-ENERGY",
    reason_tag="wpfa_decimal_mandate_energy",
    target_glob=_TARGET_GLOB_VAULT,
    check=_check_wpfa_decimal_mandate_energy,
    description=(
        "WPFA Decimal mandate (vault sub_kinds scope) — mirrors the WPFA "
        "seat scope."
    ),
)

_TARGET_GLOB_GATES = "pipeline/logician/gates/f_wpfa_*.py"
WPFA_DECIMAL_MANDATE_ENERGY_GATES: Rule = Rule(
    name="R-WPFA-DECIMAL-MANDATE-ENERGY",
    reason_tag="wpfa_decimal_mandate_energy",
    target_glob=_TARGET_GLOB_GATES,
    check=_check_wpfa_decimal_mandate_energy,
    description=(
        "WPFA Decimal mandate (Logician gate scope) — mirrors the WPFA "
        "seat scope."
    ),
)


__all__ = [
    "WPFA_DECIMAL_MANDATE_ENERGY",
    "WPFA_DECIMAL_MANDATE_ENERGY_VAULT",
    "WPFA_DECIMAL_MANDATE_ENERGY_GATES",
]
