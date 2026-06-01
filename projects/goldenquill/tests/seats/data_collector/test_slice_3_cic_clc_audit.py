"""Tests for the 4-layer CIC × CLC orthogonality audit (Slice 3).

Per §13.16.1 RT-20 closure + §13.16.6.2 RT-C2-08 CI requirement. The
audit is consolidated under the lint rule
``R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY``; this test file proves the
audit runs across the live tree at commit time and that each of the four
detection layers is exercised by the lint rule.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from pipeline.linting.ast_lint import lint_tree
from pipeline.linting.r_datacollector_slice_3 import (
    CIC_TOKEN_REGEX,
    R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _dc_path(tmp_path: Path, name: str) -> Path:
    return (
        tmp_path
        / "pipeline"
        / "orchestrator"
        / "seats"
        / "data_collector"
        / name
    )


def _write(path: Path, source: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(source).lstrip("\n"), encoding="utf-8")
    return path


def test_cic_clc_audit_clean_at_lock():
    """Layer-1+2+3+4 audit MUST pass against the live tree (§13.16.1
    RT-20 + §13.16.6.2 RT-C2-08).
    """
    target = REPO_ROOT / "pipeline" / "orchestrator" / "seats" / "data_collector"
    violations = lint_tree(target, [R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY])
    assert violations == [], (
        "CIC × CLC four-layer audit fired on the live Data Collector tree:\n"
        + "\n".join(
            f"{v.file}:{v.line}:{v.col}: {v.rule_name} [{v.reason_tag}] {v.message}"
            for v in violations
        )
    )


@pytest.mark.parametrize(
    "cic_token",
    [
        "FOOD_SYSTEMS",
        "EDUCATOR",
        "PUBLIC_AGENCY",
        "ARTS_CULTURE",
        "COOPERATIVE",
        "ECOSYSTEM_INTERMEDIARY",
        "CIC_FOOD_SYSTEMS",
        "INTERNAL_FOOD_SYSTEMS",
    ],
)
def test_cic_token_regex_matches_each_archetype(cic_token: str):
    """Layer 1 — the lexical regex matches each canonical CIC token."""
    assert CIC_TOKEN_REGEX.fullmatch(cic_token), (
        f"CIC token regex does not match {cic_token!r}"
    )


def test_cic_token_regex_does_not_match_unrelated_uppercase(cic_token: str = "PAYLOAD"):
    """Layer 1 — the regex is narrow; non-CIC uppercase identifiers don't
    match."""
    assert not CIC_TOKEN_REGEX.fullmatch(cic_token), (
        f"CIC token regex incorrectly matches unrelated identifier {cic_token!r}"
    )


def test_layer_1_lexical_scan_fires_on_code_reference(tmp_path: Path):
    """Layer 1 — bare identifier reference (Name) fires."""
    src = """
    FOOD_SYSTEMS = "x"
    """
    _write(_dc_path(tmp_path, "layer1.py"), src)
    target = tmp_path / "pipeline" / "orchestrator" / "seats" / "data_collector"
    violations = lint_tree(target, [R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY])
    assert len(violations) >= 1


def test_layer_2_pydantic_field_default_scan_fires(tmp_path: Path):
    """Layer 2 — Pydantic field default matching a CIC enum member fires
    via Name resolution."""
    src = """
    from dataclasses import dataclass

    EDUCATOR = "educator"

    @dataclass
    class Config:
        archetype: str = EDUCATOR
    """
    _write(_dc_path(tmp_path, "layer2.py"), src)
    target = tmp_path / "pipeline" / "orchestrator" / "seats" / "data_collector"
    violations = lint_tree(target, [R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY])
    assert len(violations) >= 1


def test_layer_3_value_set_scan_fires_on_string_literal(tmp_path: Path):
    """Layer 3 — string literal in outbound template register fires."""
    src = """
    TEMPLATE_REGISTER = {
        "foo_template": {"archetype": "PUBLIC_AGENCY"},
    }
    """
    _write(_dc_path(tmp_path, "layer3.py"), src)
    target = tmp_path / "pipeline" / "orchestrator" / "seats" / "data_collector"
    violations = lint_tree(target, [R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY])
    assert len(violations) >= 1


def test_layer_4_kp_schema_anchor_admitted(tmp_path: Path):
    """Layer 4 — the rule delegates the KP schema audit per the v7.0.8
    F-CIC-CLC-COUPLING-VIOLATION predicate. The lint rule fires for any
    CIC token in source, which is the structural anchor that the
    schema-audit CI job runs. The test exercises the four-layer rule
    overall rather than the schema-audit external runner."""
    # A schema-like module with CIC token in field default → fires.
    src = """
    from typing import Literal
    from dataclasses import dataclass, field

    @dataclass
    class FunderTagSchema:
        archetype: Literal["FOOD_SYSTEMS", "EDUCATOR"] = "FOOD_SYSTEMS"
    """
    _write(_dc_path(tmp_path, "schema.py"), src)
    target = tmp_path / "pipeline" / "orchestrator" / "seats" / "data_collector"
    violations = lint_tree(target, [R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY])
    # Multiple fires (Literal[...] arguments + default value).
    assert len(violations) >= 2


def test_comments_do_not_fire_layer_1(tmp_path: Path):
    """The Python `#` comment-strip works — a comment-only CIC reference
    does not fire."""
    src = """
    # FOOD_SYSTEMS is one of six customer identity categories.
    # PUBLIC_AGENCY, EDUCATOR, ARTS_CULTURE, COOPERATIVE, ECOSYSTEM_INTERMEDIARY round out the six.
    def f():
        return "channel"
    """
    _write(_dc_path(tmp_path, "comments_only.py"), src)
    target = tmp_path / "pipeline" / "orchestrator" / "seats" / "data_collector"
    violations = lint_tree(target, [R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY])
    assert violations == []


def test_audit_runs_as_default_rule():
    """RT-C2-08 — the audit is registered in DEFAULT_RULES so every CI
    lint invocation includes it (not only at LOCK ceremony)."""
    from pipeline.linting.ast_lint import DEFAULT_RULES
    names = {r.name for r in DEFAULT_RULES}
    assert "R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY" in names
