"""Tests for R-NO-POLITICAL-AXIS-LITERAL.

Per §4 v2.x apolitical_dialect §4.X.2 + §0.5 v28 row 551. LOCKED
2026-05-16T14:00:00Z; lock_history rows 236/249. Layer 1 (commit-hook
static check) paired with the runtime gate
F-DIALECT-POLITICAL-AXIS-LEAK at
:mod:`pipeline.logician.gates.f_dialect_political_axis_leak`.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree
from pipeline.linting.r_no_political_axis_literal import (
    NO_POLITICAL_AXIS_LITERAL_CARDS,
    NO_POLITICAL_AXIS_LITERAL_LOGICIAN,
    NO_POLITICAL_AXIS_LITERAL_TYPES,
)


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Surface contract
# ---------------------------------------------------------------------------


def test_rules_registered_in_default_rules() -> None:
    assert NO_POLITICAL_AXIS_LITERAL_CARDS in DEFAULT_RULES
    assert NO_POLITICAL_AXIS_LITERAL_TYPES in DEFAULT_RULES
    assert NO_POLITICAL_AXIS_LITERAL_LOGICIAN in DEFAULT_RULES


def test_rule_names_match_amendment_text() -> None:
    """§4 v2.x apolitical_dialect §4.X.2 names the rule
    R-NO-POLITICAL-AXIS-LITERAL — all three target-glob instances must
    share this name."""
    assert NO_POLITICAL_AXIS_LITERAL_CARDS.name == "R-NO-POLITICAL-AXIS-LITERAL"
    assert NO_POLITICAL_AXIS_LITERAL_TYPES.name == "R-NO-POLITICAL-AXIS-LITERAL"
    assert NO_POLITICAL_AXIS_LITERAL_LOGICIAN.name == "R-NO-POLITICAL-AXIS-LITERAL"


def test_rule_targets_disjoint_subtrees() -> None:
    """Each rule instance targets a different pipeline subtree."""
    assert "cards" in NO_POLITICAL_AXIS_LITERAL_CARDS.target_glob
    assert "types" in NO_POLITICAL_AXIS_LITERAL_TYPES.target_glob
    assert "logician/gates" in NO_POLITICAL_AXIS_LITERAL_LOGICIAN.target_glob


# ---------------------------------------------------------------------------
# Live-tree regression — current cards/types/logician trees stay clean
# ---------------------------------------------------------------------------


def test_live_cards_tree_has_zero_violations() -> None:
    """The cards subtree must be clean of political-axis vocabulary."""
    cards_dir = REPO_ROOT / "pipeline" / "cards"
    if not cards_dir.is_dir():
        pytest.skip("pipeline/cards/ tree absent at test time")
    vs = lint_tree(cards_dir, [NO_POLITICAL_AXIS_LITERAL_CARDS])
    assert vs == [], (
        f"pipeline/cards/ subtree carries retired political-axis vocabulary: "
        f"{[str(v) for v in vs]}. "
        "Architecture v7.0.12 LOCKED 2026-05-16 retires the four-axis enum; "
        "rename to CLC slugs per pipeline/types/identity_capital.py."
    )


def test_live_types_tree_has_zero_violations() -> None:
    types_dir = REPO_ROOT / "pipeline" / "types"
    if not types_dir.is_dir():
        pytest.skip("pipeline/types/ tree absent at test time")
    vs = lint_tree(types_dir, [NO_POLITICAL_AXIS_LITERAL_TYPES])
    assert vs == [], (
        f"pipeline/types/ subtree carries retired political-axis vocabulary: "
        f"{[str(v) for v in vs]}."
    )


def test_live_logician_gates_tree_clean_modulo_exemptions() -> None:
    """The Logician gates subtree must be clean except for the named
    exemptions (detector modules + migration-pending gates per Option-B
    split)."""
    gates_dir = REPO_ROOT / "pipeline" / "logician" / "gates"
    if not gates_dir.is_dir():
        pytest.skip("pipeline/logician/gates/ tree absent at test time")
    vs = lint_tree(gates_dir, [NO_POLITICAL_AXIS_LITERAL_LOGICIAN])
    # Exemptions are enforced inside the check function; any surviving
    # violation is a real regression.
    assert vs == [], (
        f"pipeline/logician/gates/ subtree carries unexempted political-"
        f"axis vocabulary: {[str(v) for v in vs]}."
    )


# ---------------------------------------------------------------------------
# Synthetic fixtures — stage modules under tmp_path mimicking each glob
# ---------------------------------------------------------------------------


def _stage_module(tmp_path: Path, *, subpath: str, source: str) -> Path:
    target = tmp_path / subpath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding="utf-8")
    return tmp_path


# ---------------------------------------------------------------------------
# Field-name literal detection (Layer 1)
# ---------------------------------------------------------------------------


def test_funder_political_axis_string_literal_fires_in_cards(tmp_path: Path) -> None:
    src = (
        '"""greenfield cards module."""\n'
        '\n'
        'BAD_FIELD: str = "funder_political_axis"\n'
    )
    root = _stage_module(
        tmp_path, subpath="pipeline/cards/CIC/loader.py", source=src
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_CARDS])
    assert vs, "expected violation on funder_political_axis literal"
    assert vs[0].rule_name == "R-NO-POLITICAL-AXIS-LITERAL"
    assert "field_name_in_literal" in vs[0].reason_tag


def test_progressive_register_string_literal_fires(tmp_path: Path) -> None:
    src = 'FIELD = "progressive_register"\n'
    root = _stage_module(
        tmp_path, subpath="pipeline/types/some_new_module.py", source=src
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_TYPES])
    assert vs, "expected violation on progressive_register literal"


def test_political_axis_substring_in_literal_fires(tmp_path: Path) -> None:
    """FI-2 substring detector catches creative wrappers."""
    src = 'KEY = "custom_political_axis_v3"\n'
    root = _stage_module(
        tmp_path, subpath="pipeline/cards/CIC/loader.py", source=src
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_CARDS])
    assert vs


def test_innocent_literal_passes(tmp_path: Path) -> None:
    src = 'KEY = "operating_capacity"\n'
    root = _stage_module(
        tmp_path, subpath="pipeline/cards/CIC/loader.py", source=src
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_CARDS])
    assert vs == []


# ---------------------------------------------------------------------------
# Identifier detection (Layer 1)
# ---------------------------------------------------------------------------


def test_function_arg_with_political_axis_name_fires(tmp_path: Path) -> None:
    src = (
        "def configure(funder_political_axis: str) -> None:\n"
        "    pass\n"
    )
    root = _stage_module(
        tmp_path, subpath="pipeline/cards/CIC/loader.py", source=src
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_CARDS])
    assert vs
    assert any("field_name_in_identifier" in v.reason_tag for v in vs)


def test_annotated_assign_with_political_axis_target_fires(tmp_path: Path) -> None:
    src = "progressive_register: dict = {}\n"
    root = _stage_module(
        tmp_path, subpath="pipeline/cards/CIC/loader.py", source=src
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_CARDS])
    assert vs


# ---------------------------------------------------------------------------
# Layer 2: Literal[...] annotations
# ---------------------------------------------------------------------------


def test_literal_with_two_retired_values_fires(tmp_path: Path) -> None:
    src = (
        "from typing import Literal\n"
        "\n"
        "Dialect = Literal['conservative', 'centrist', 'progressive', 'soul_fire']\n"
    )
    root = _stage_module(
        tmp_path, subpath="pipeline/cards/CIC/dialect_model.py", source=src
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_CARDS])
    assert vs
    assert any(
        "pydantic_literal" in v.reason_tag for v in vs
    )


def test_literal_with_one_retired_value_does_not_fire(tmp_path: Path) -> None:
    """Layer 2 requires 2-or-more; single-value Literal alone doesn't trip."""
    src = (
        "from typing import Literal\n"
        "\n"
        "X = Literal['progressive']\n"
    )
    root = _stage_module(
        tmp_path, subpath="pipeline/cards/CIC/dialect_model.py", source=src
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_CARDS])
    # Note: the bare string literal 'progressive' is NOT a field-name
    # token (no progressive_register or political_axis substring), so
    # Layer 1 string-literal check doesn't fire either.
    assert vs == []


def test_literal_with_innocuous_values_passes(tmp_path: Path) -> None:
    src = (
        "from typing import Literal\n"
        "\n"
        "CLC = Literal['public_purpose_works', 'catalytic_change', 'operating_capacity']\n"
    )
    root = _stage_module(
        tmp_path, subpath="pipeline/cards/CIC/model.py", source=src
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_CARDS])
    assert vs == []


def test_literal_with_typing_dot_literal_fires(tmp_path: Path) -> None:
    """Resolves both ``Literal[...]`` and ``typing.Literal[...]``."""
    src = (
        "import typing\n"
        "X = typing.Literal['conservative', 'progressive']\n"
    )
    root = _stage_module(
        tmp_path, subpath="pipeline/cards/CIC/model.py", source=src
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_CARDS])
    assert vs


# ---------------------------------------------------------------------------
# Exemptions
# ---------------------------------------------------------------------------


def test_detector_gate_module_exempt(tmp_path: Path) -> None:
    """The f_dialect_political_axis_leak.py detector legitimately holds the
    retired vocabulary; its exemption is named in the rule module."""
    src = (
        'RETIRED = ("conservative", "centrist", "progressive", "soul_fire")\n'
        'FIELD = "funder_political_axis"\n'
    )
    root = _stage_module(
        tmp_path,
        subpath="pipeline/logician/gates/f_dialect_political_axis_leak.py",
        source=src,
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_LOGICIAN])
    assert vs == [], "detector gate should be exempt"


def test_migration_pending_gate_exempt(tmp_path: Path) -> None:
    """f_logician_spine_drift.py is on the migration-pending exemption
    list; the operator removes the exemption after the cards-ceremony
    re-keys the file."""
    src = (
        'VALID = ("conservative", "centrist", "progressive", "soul_fire")\n'
    )
    root = _stage_module(
        tmp_path,
        subpath="pipeline/logician/gates/f_logician_spine_drift.py",
        source=src,
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_LOGICIAN])
    assert vs == []


def test_random_logician_gate_not_exempt(tmp_path: Path) -> None:
    """A newly-authored gate that's NOT on the exemption list trips the
    rule."""
    src = 'FIELD = "funder_political_axis"\n'
    root = _stage_module(
        tmp_path,
        subpath="pipeline/logician/gates/f_some_new_gate.py",
        source=src,
    )
    vs = lint_tree(root, [NO_POLITICAL_AXIS_LITERAL_LOGICIAN])
    assert vs


# ---------------------------------------------------------------------------
# Glob scope — out-of-scope files NOT touched
# ---------------------------------------------------------------------------


def test_seats_subtree_out_of_scope_at_lock(tmp_path: Path) -> None:
    """Per Option-B split, the seats subtree is migration-pending; the
    rule's target_glob does NOT cover it at v7.0.12 LOCK."""
    src = 'FIELD = "funder_political_axis"\n'
    root = _stage_module(
        tmp_path, subpath="pipeline/seats/scribe/dialect.py", source=src
    )
    # Run with all three rule instances — none should match this path.
    vs = lint_tree(
        root,
        [
            NO_POLITICAL_AXIS_LITERAL_CARDS,
            NO_POLITICAL_AXIS_LITERAL_TYPES,
            NO_POLITICAL_AXIS_LITERAL_LOGICIAN,
        ],
    )
    assert vs == [], (
        "seats/ is out of scope at v7.0.12 LOCK (Option-B split — "
        "cards-ceremony pending). Adding seats/ requires a follow-on "
        "amendment row + rule target_glob extension."
    )
