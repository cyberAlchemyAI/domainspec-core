"""Tests for R-CLASS-POSTURE-FIELD-COVERAGE (pipeline.linting.r_class_posture_field_coverage).

Per architecture v7.0.10 LOCKED 2026-05-11 §1.4 + section_04_v2_x_amendment.md
§4.3.7 — the F-CLASS-REGISTER-* gate module must reference the
``selected_posture`` field added at v7.0.10 (Classification Review UX surface
flip; sub-tag extensions `.posture_unsigned` / `.posture_invalid` /
`.posture_hash_mismatch`).

The rule is a "presence" check on the gate-module source: the module file at
``pipeline/logician/gates/f_class_register.py`` must contain at least one
reference to the string ``selected_posture`` (in a string constant, attribute
access, name reference, keyword argument, or function parameter).
"""

from __future__ import annotations

from pathlib import Path

from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree
from pipeline.linting.r_class_posture_field_coverage import (
    CLASS_POSTURE_FIELD_COVERAGE,
)


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Surface contract
# ---------------------------------------------------------------------------


def test_rule_is_registered_in_default_rules() -> None:
    assert CLASS_POSTURE_FIELD_COVERAGE in DEFAULT_RULES


def test_rule_name_and_reason_tag() -> None:
    assert CLASS_POSTURE_FIELD_COVERAGE.name == "R-CLASS-POSTURE-FIELD-COVERAGE"
    assert (
        CLASS_POSTURE_FIELD_COVERAGE.reason_tag == "class_posture_field_coverage"
    )


def test_rule_targets_f_class_register_module() -> None:
    assert (
        "f_class_register.py" in CLASS_POSTURE_FIELD_COVERAGE.target_glob
    )


# ---------------------------------------------------------------------------
# Live-tree regression — the actual gate module must satisfy the coverage check
# ---------------------------------------------------------------------------


def test_live_f_class_register_module_satisfies_coverage() -> None:
    vs = lint_tree(
        REPO_ROOT / "pipeline" / "logician" / "gates",
        [CLASS_POSTURE_FIELD_COVERAGE],
    )
    assert vs == [], (
        f"F-CLASS-REGISTER-* gate module is missing selected_posture "
        f"references — v7.0.10 §1.4 + section_04_v2_x_amendment.md §4.3.7 "
        f"require the sub-tag extensions: {[str(v) for v in vs]}"
    )


# ---------------------------------------------------------------------------
# Synthetic fixtures
# ---------------------------------------------------------------------------


def _stage_gate_module(tmp_path: Path, *, source: str) -> Path:
    target = tmp_path / "pipeline" / "logician" / "gates" / "f_class_register.py"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding="utf-8")
    return tmp_path


def test_module_missing_posture_reference_fires(tmp_path: Path) -> None:
    """A gate module with no `selected_posture` reference fires the rule."""
    src = (
        '"""Stale gate module — does not yet know about v7.0.10."""\n'
        "from typing import Optional\n"
        "def check_class_register_unsigned() -> Optional[str]:\n"
        '    return "F-CLASS-REGISTER-UNSIGNED"\n'
    )
    root = _stage_gate_module(tmp_path, source=src)
    vs = lint_tree(root, [CLASS_POSTURE_FIELD_COVERAGE])
    assert vs, "expected violation on module with no posture reference"
    assert vs[0].rule_name == "R-CLASS-POSTURE-FIELD-COVERAGE"


def test_module_with_string_reference_passes(tmp_path: Path) -> None:
    """A gate module referencing `selected_posture` in a string passes."""
    src = (
        '"""Gate module — knows about v7.0.10."""\n'
        '_POSTURE_KEY = "selected_posture"\n'
        "def check_class_register_unsigned():\n"
        "    return _POSTURE_KEY\n"
    )
    root = _stage_gate_module(tmp_path, source=src)
    vs = lint_tree(root, [CLASS_POSTURE_FIELD_COVERAGE])
    assert vs == [], f"unexpected violation on compliant fixture: {vs}"


def test_module_with_attribute_reference_passes(tmp_path: Path) -> None:
    """A gate module referencing `selected_posture` as an attribute passes."""
    src = (
        '"""Gate module — knows about v7.0.10."""\n'
        "class Register:\n"
        "    selected_posture: str = ''\n"
        "def check(reg: Register) -> str:\n"
        "    return reg.selected_posture\n"
    )
    root = _stage_gate_module(tmp_path, source=src)
    vs = lint_tree(root, [CLASS_POSTURE_FIELD_COVERAGE])
    assert vs == [], f"unexpected violation on attribute-reference fixture: {vs}"


def test_module_with_keyword_argument_passes(tmp_path: Path) -> None:
    """A gate module passing `selected_posture=` as a kwarg passes."""
    src = (
        '"""Gate module — calls helper with posture kwarg."""\n'
        "def helper(*, selected_posture=None):\n"
        "    return selected_posture\n"
        "def check():\n"
        '    return helper(selected_posture="frontier_eligible")\n'
    )
    root = _stage_gate_module(tmp_path, source=src)
    vs = lint_tree(root, [CLASS_POSTURE_FIELD_COVERAGE])
    assert vs == [], f"unexpected violation on kwarg fixture: {vs}"


def test_violation_message_mentions_v7_0_10_and_subtags(tmp_path: Path) -> None:
    """The violation message references v7.0.10 + the sub-tag extensions."""
    src = "X = 1\n"
    root = _stage_gate_module(tmp_path, source=src)
    vs = lint_tree(root, [CLASS_POSTURE_FIELD_COVERAGE])
    assert vs
    assert "v7.0.10" in vs[0].message
    assert "posture_unsigned" in vs[0].message
    assert "posture_invalid" in vs[0].message
    assert "posture_hash_mismatch" in vs[0].message
