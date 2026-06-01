"""R-CLASS-POSTURE-FIELD-COVERAGE — AST-lint rule. [v7.0.10 §1.4 enforcement]

Architecture v7.0.10 LOCKED 2026-05-11 (row 215) §1.4 amends Classification
Review step 3 + step 4 to add deployment-posture selection alongside per-field
classification. The signed register at v7.0.10 attests to BOTH per-field
classifications AND the operator-selected ``selected_posture`` field (one of
``frontier_eligible`` / ``split_context_hybrid`` / ``local_only_sovereign``).
The F-CLASS-REGISTER-* gates (rows 1-4 of the F-CLASS-* family per v7.0.7
§5.1 — F_CLASS_REGISTER_MISSING / _UNSIGNED / _SIGNATURE_INVALID /
_HASH_MISMATCH) carry sub-tag extensions to verify the posture-signature
trail (`.posture_unsigned` / `.posture_invalid` / `.posture_hash_mismatch`).

This AST-lint rule enforces that the F-CLASS-REGISTER-* gate module references
the ``selected_posture`` field — confirming the predicate signature has been
extended to inspect the posture coverage. The check is a presence check on
the gate-module source: the module file at ``pipeline/logician/gates/f_class_register.py``
must contain at least one reference to the string ``selected_posture``.

Authority:
  - architecture v7.0.10 §1.4 (Classification Review UX surface flip)
  - section_04_v2_x_amendment.md §4.3.7 (Posture-signature sub-tag extensions)
  - section_00_5_v7_0_10_amendment.md §B (sub-tag extension recording)

Scope:
  - ``pipeline/logician/gates/f_class_register.py``

Mechanics:
  - This is a "presence" check at the module level rather than a per-call
    static analysis. The rule fires once per module load if no reference to
    ``selected_posture`` is found in any string, docstring, attribute access,
    or symbol reference. The rule is intentionally lenient about WHERE the
    reference appears — what matters is that the gate predicate's signature
    and implementation know about the field.
  - The rule does NOT fire on test modules; tests can independently verify
    that the gate predicate correctly inspects the posture field via named
    drift-test bindings (per §4 v2.x amendment §4.3.7).
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation


_TARGET_GLOB = "pipeline/logician/gates/f_class_register.py"


def _references_selected_posture(tree: ast.AST) -> bool:
    """Walk the AST and return True iff any node references `selected_posture`.

    Accepts the reference in:
      - String constants (e.g., dict-key lookups, log messages).
      - Attribute access on objects (e.g., ``register.selected_posture``).
      - Name references (defensive — unlikely but possible).
      - Keyword argument names in function calls.
      - Function parameter names in def / lambda signatures.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if "selected_posture" in node.value:
                return True
        elif isinstance(node, ast.Attribute):
            if node.attr == "selected_posture":
                return True
        elif isinstance(node, ast.Name):
            if node.id == "selected_posture":
                return True
        elif isinstance(node, ast.keyword):
            if node.arg == "selected_posture":
                return True
        elif isinstance(node, ast.arg):
            if node.arg == "selected_posture":
                return True
    return False


def _check_class_posture_field_coverage(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    if _references_selected_posture(tree):
        return
    # Module-level violation — emit a single Violation at line 1 because the
    # absence is module-scope, not site-scope.
    yield Violation(
        rule_name="R-CLASS-POSTURE-FIELD-COVERAGE",
        reason_tag="class_register_gate_missing_posture_field_reference",
        file=path,
        line=1,
        col=0,
        message=(
            "F-CLASS-REGISTER-* gate module does not reference the "
            "`selected_posture` field. Architecture v7.0.10 LOCKED 2026-05-11 "
            "(row 215) §1.4 + section_04_v2_x_amendment.md §4.3.7 require "
            "F-CLASS-REGISTER-UNSIGNED / -SIGNATURE-INVALID / -HASH-MISMATCH "
            "to extend their predicate signature to inspect the operator-"
            "signed deployment posture. Add the sub-tag extensions "
            "(`.posture_unsigned`, `.posture_invalid`, `.posture_hash_mismatch`) "
            "and the corresponding named drift-test bindings to "
            "`tests/logician/gates/test_f_class_register.py`."
        ),
    )


CLASS_POSTURE_FIELD_COVERAGE: Rule = Rule(
    name="R-CLASS-POSTURE-FIELD-COVERAGE",
    reason_tag="class_posture_field_coverage",
    target_glob=_TARGET_GLOB,
    check=_check_class_posture_field_coverage,
    description=(
        "Enforce that the F-CLASS-REGISTER-* gate module references the "
        "`selected_posture` field added at architecture v7.0.10 §1.4. "
        "Layer 1 of the sub-tag-extension realization for "
        "`.posture_unsigned` / `.posture_invalid` / `.posture_hash_mismatch`."
    ),
)


__all__ = ["CLASS_POSTURE_FIELD_COVERAGE"]
