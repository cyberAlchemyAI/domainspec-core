"""Tests for R-V0-10-NO-SLOT-TOKEN-EMISSION (pipeline.linting.r_v0_10_no_slot_token_emission).

Per architecture v7.0.10 LOCKED 2026-05-11 §2.2 + §5.2 — defense-in-depth
Layer 1 against accidental slot-token emission. The opaque-slot-token
mechanism (v7.0.7 "Sanitized" posture) is deprecated entirely at v7.0.10;
no legitimate code path emits `[SLOT_*]` tokens into cloud-routed prompts
under any of the three remaining postures (Frontier-Eligible /
Split-Context Hybrid / Local-Only-Sovereign).

The rule fires on any `[SLOT_*]` substring inside a string literal in
orchestrator + seats modules. Defense-in-depth scanner modules (e.g., the
Data Collector's outbound-boundary regex in
`pipeline/orchestrator/seats/data_collector/field_validator.py`) are
explicitly exempted as detection-side uses.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree
from pipeline.linting.r_v0_10_no_slot_token_emission import (
    V0_10_NO_SLOT_TOKEN_EMISSION,
    V0_10_NO_SLOT_TOKEN_EMISSION_SEATS,
)


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Surface contract
# ---------------------------------------------------------------------------


def test_rule_is_registered_in_default_rules() -> None:
    assert V0_10_NO_SLOT_TOKEN_EMISSION in DEFAULT_RULES
    assert V0_10_NO_SLOT_TOKEN_EMISSION_SEATS in DEFAULT_RULES


def test_rule_name_and_reason_tag() -> None:
    assert V0_10_NO_SLOT_TOKEN_EMISSION.name == "R-V0-10-NO-SLOT-TOKEN-EMISSION"
    assert V0_10_NO_SLOT_TOKEN_EMISSION.reason_tag == "v0_10_no_slot_token_emission"
    assert (
        V0_10_NO_SLOT_TOKEN_EMISSION_SEATS.name
        == "R-V0-10-NO-SLOT-TOKEN-EMISSION"
    )


def test_rule_targets_orchestrator_and_seats_separately() -> None:
    assert "orchestrator" in V0_10_NO_SLOT_TOKEN_EMISSION.target_glob
    assert "seats" in V0_10_NO_SLOT_TOKEN_EMISSION_SEATS.target_glob


# ---------------------------------------------------------------------------
# Live-tree regression — current orchestrator + seats trees must stay clean
# ---------------------------------------------------------------------------


def test_live_orchestrator_tree_has_zero_violations() -> None:
    vs = lint_tree(
        REPO_ROOT / "pipeline" / "orchestrator",
        [V0_10_NO_SLOT_TOKEN_EMISSION, V0_10_NO_SLOT_TOKEN_EMISSION_SEATS],
    )
    assert vs == [], (
        f"Orchestrator tree contains slot-token literal(s): "
        f"{[str(v) for v in vs]}. v7.0.10 deprecated the opaque-slot-token "
        f"mechanism — see pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md"
    )


def test_live_seats_tree_has_zero_violations() -> None:
    seats_dir = REPO_ROOT / "pipeline" / "seats"
    if not seats_dir.is_dir():
        pytest.skip("pipeline/seats/ tree absent at test time")
    vs = lint_tree(
        seats_dir,
        [V0_10_NO_SLOT_TOKEN_EMISSION, V0_10_NO_SLOT_TOKEN_EMISSION_SEATS],
    )
    assert vs == [], (
        f"Seats tree contains slot-token literal(s): "
        f"{[str(v) for v in vs]}."
    )


# ---------------------------------------------------------------------------
# Synthetic fixtures — staged into a tmpdir mimicking the rule's path globs
# ---------------------------------------------------------------------------


def _stage_module(tmp_path: Path, *, subpath: str, source: str) -> Path:
    """Write a synthetic .py source under tmp_path/<subpath>."""
    target = tmp_path / subpath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding="utf-8")
    return tmp_path


def test_dirty_numeric_slot_fires(tmp_path: Path) -> None:
    """A literal `[SLOT_001]` in an orchestrator module fires the rule."""
    src = (
        '"""Module docstring."""\n'
        "def emit():\n"
        '    return "Annual revenue is [SLOT_001] per audited statement"\n'
    )
    root = _stage_module(
        tmp_path,
        subpath="pipeline/orchestrator/seats/scribe/cloud_prompt.py",
        source=src,
    )
    # Path is under pipeline/orchestrator/ so the orchestrator-scoped rule matches.
    vs = lint_tree(root, [V0_10_NO_SLOT_TOKEN_EMISSION])
    assert vs, "expected violation on numeric slot token"
    assert vs[0].rule_name == "R-V0-10-NO-SLOT-TOKEN-EMISSION"


def test_dirty_semantic_slot_fires(tmp_path: Path) -> None:
    """A semantic slot name like `[SLOT_ANNUAL_REVENUE]` fires the rule."""
    src = (
        "def emit():\n"
        '    return f"Org: [SLOT_ANNUAL_REVENUE] / EIN [SLOT_EIN]"\n'
    )
    root = _stage_module(
        tmp_path,
        subpath="pipeline/orchestrator/router.py",
        source=src,
    )
    vs = lint_tree(root, [V0_10_NO_SLOT_TOKEN_EMISSION])
    assert vs, "expected violation on semantic slot token"
    # Each f-string literal segment + value substitution may produce
    # multiple Constant nodes; the rule fires on at least one.
    assert any(v.rule_name == "R-V0-10-NO-SLOT-TOKEN-EMISSION" for v in vs)


def test_dirty_empty_slot_fires(tmp_path: Path) -> None:
    """An empty slot `[SLOT_]` still matches the broadened v7.0.10 regex."""
    src = (
        "def emit():\n"
        '    return "draft: [SLOT_]"\n'
    )
    root = _stage_module(
        tmp_path,
        subpath="pipeline/seats/scribe/draft.py",
        source=src,
    )
    vs = lint_tree(root, [V0_10_NO_SLOT_TOKEN_EMISSION_SEATS])
    assert vs, "expected violation on empty slot token"


def test_clean_orchestrator_module_passes(tmp_path: Path) -> None:
    """A module with no slot-token literal produces no violation."""
    src = (
        "from typing import Optional\n"
        "def render(value: Optional[str]) -> str:\n"
        "    return value or 'unset'\n"
    )
    root = _stage_module(
        tmp_path,
        subpath="pipeline/orchestrator/router.py",
        source=src,
    )
    vs = lint_tree(root, [V0_10_NO_SLOT_TOKEN_EMISSION])
    assert vs == [], f"unexpected violation on clean fixture: {vs}"


def test_field_validator_path_is_exempt(tmp_path: Path) -> None:
    """The data_collector field_validator is exempt as a defense-in-depth scanner."""
    src = (
        "import re\n"
        "def scan_outbound(body: bytes):\n"
        '    pattern = re.compile(rb"\\[SLOT_([A-Z0-9_]+)\\]")\n'
        "    return list(pattern.finditer(body))\n"
    )
    root = _stage_module(
        tmp_path,
        subpath="pipeline/orchestrator/seats/data_collector/field_validator.py",
        source=src,
    )
    vs = lint_tree(root, [V0_10_NO_SLOT_TOKEN_EMISSION_SEATS])
    assert vs == [], f"field_validator should be exempt: {vs}"


def test_violation_message_mentions_v7_0_10(tmp_path: Path) -> None:
    """The violation message references the v7.0.10 LOCK for operator clarity."""
    src = 'X = "[SLOT_007]"\n'
    root = _stage_module(
        tmp_path,
        subpath="pipeline/orchestrator/seats/scribe/cloud_prompt.py",
        source=src,
    )
    vs = lint_tree(root, [V0_10_NO_SLOT_TOKEN_EMISSION])
    assert vs
    assert "v7.0.10" in vs[0].message
    assert "deprecated" in vs[0].message.lower() or "deprecates" in vs[0].message
