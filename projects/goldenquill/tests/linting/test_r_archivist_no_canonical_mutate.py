"""Tests for R-ARCHIVIST-NO-CANONICAL-MUTATE — §4 v2.x.1 corrective.

Spec card: ``pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md`` (LOCKED
2026-05-10 — Cycle-1 closures applied) and the predecessor disposition packet
``pipeline/planning/section_04_v2_x_1_tilth_rt_07_backlog_2026-05-10.md`` §3.

Closes Tilth-RT-07 PARTIAL via AST-lint enumeration extension: the
R-ARCHIVIST-NO-CANONICAL-MUTATE rule fires ``.low_level_rename_*`` sub-tags on
six low-level rename primitives (os.replace / os.rename / os.renames /
shutil.move / shutil.copy family / os.link / os.symlink) under
``pipeline/orchestrator/seats/archivist/**``.

This test file is the §4 v2.x.1 acceptance-criterion surface; it implements
the disposition packet §3.2 acceptance test stub against the real ast_lint
API (the stub used helpers that don't exist on disk —
``ast_lint_archivist_seat_source`` / ``make_module_with`` — so the
test adapts to ``lint_tree`` + ``_write`` per the test_ast_lint.py pattern).

Cycle-1 fold-ins applied 2026-05-10:
- RT-09: ``os.renames`` added to parametrized acceptance + table-coverage
  closures.
- RT-14: ``test_forbidden_primitives_table_is_immutable`` asserts the
  ``MappingProxyType``-wrapped export refuses mutation.
- RT-15: ``test_rule_fires_in_dead_code`` asserts AST-lint is structural
  (not flow-sensitive) — ``if False:`` forbidden calls still fire.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree
from pipeline.linting.r_archivist_no_canonical_mutate import (
    ARCHIVIST_NO_CANONICAL_MUTATE,
    FORBIDDEN_PRIMITIVES,
)


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Fixture helpers (mirrors tests/linting/test_ast_lint.py conventions)
# ---------------------------------------------------------------------------


def _write(path: Path, source: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(source).lstrip("\n"), encoding="utf-8")
    return path


def _archivist_module_with(body: str) -> str:
    """Synthesize a minimal Archivist seat source string with the given body."""
    return dedent(
        f"""
        # Synthetic Archivist seat source for AST-lint test.
        import os
        import shutil

        def archivist_curation_step(src: str, dst: str) -> None:
            {body}
        """
    ).lstrip("\n")


def _seat_path(tmp_path: Path) -> Path:
    """Return the tmp_path Archivist-seat source-file location."""
    return tmp_path / "pipeline" / "orchestrator" / "seats" / "archivist" / "synthetic.py"


# ---------------------------------------------------------------------------
# §4 v2.x.1 acceptance test (Tilth-RT-07 PARTIAL closure)
# ---------------------------------------------------------------------------


# (primitive source, expected sub-tag w/ leading dot) — verbatim from §3.2.
_PARAMETRIZED_PRIMITIVES = [
    pytest.param(
        "os.replace(src, '/vault_shared/funder_intelligence/register.yaml')",
        ".low_level_rename_replace",
        id="os.replace",
    ),
    pytest.param(
        "os.rename(src, 'orgs/clientA/vault/kfr/register.yaml')",
        ".low_level_rename_rename",
        id="os.rename",
    ),
    pytest.param(
        "os.renames(src, 'orgs/clientA/vault/kfr/register.yaml')",
        ".low_level_rename_renames",
        id="os.renames",
    ),
    pytest.param(
        "shutil.move(src, 'orgs/clientA/vault/kfr/register.yaml')",
        ".low_level_rename_shutil_move",
        id="shutil.move",
    ),
    pytest.param(
        "shutil.copy(src, 'orgs/clientA/vault/kfr/register.yaml')",
        ".low_level_rename_shutil_copy",
        id="shutil.copy",
    ),
    pytest.param(
        "os.link(src, dst)",
        ".low_level_rename_os_link",
        id="os.link",
    ),
]


@pytest.mark.parametrize("primitive, expected_sub_tag", _PARAMETRIZED_PRIMITIVES)
def test_r_archivist_no_canonical_mutate_enumerates_low_level_rename_primitives(
    tmp_path, primitive: str, expected_sub_tag: str
) -> None:
    """Tilth-RT-07 PARTIAL closure: verify R-ARCHIVIST-NO-CANONICAL-MUTATE
    fires ``.low_level_rename_*`` sub-tags on each enumerated primitive
    and emits failure code ``F-ARCHIVIST-AUTO-APPLY-ATTEMPTED`` in the
    diagnostic message body.
    """
    seat_path = _seat_path(tmp_path)
    _write(seat_path, _archivist_module_with(primitive))
    violations = lint_tree(
        tmp_path / "pipeline" / "orchestrator" / "seats" / "archivist",
        [ARCHIVIST_NO_CANONICAL_MUTATE],
    )
    assert len(violations) == 1, (
        f"Expected exactly one violation for {primitive!r}; got {violations!r}"
    )
    v = violations[0]
    assert v.rule_name == "R-ARCHIVIST-NO-CANONICAL-MUTATE"
    assert expected_sub_tag in v.reason_tag, (
        f"sub-tag {expected_sub_tag!r} not present in reason_tag "
        f"{v.reason_tag!r} for primitive {primitive!r}"
    )
    assert "F-ARCHIVIST-AUTO-APPLY-ATTEMPTED" in v.message, (
        "failure code attribution F-ARCHIVIST-AUTO-APPLY-ATTEMPTED "
        f"missing from diagnostic message body: {v.message!r}"
    )


# ---------------------------------------------------------------------------
# shutil.copy family fan-out — copy / copy2 / copyfile / copytree all map to
# the same sub-tag per disposition packet §3.1.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "primitive",
    [
        "shutil.copy(src, dst)",
        "shutil.copy2(src, dst)",
        "shutil.copyfile(src, dst)",
        "shutil.copytree(src, dst)",
    ],
)
def test_shutil_copy_family_all_map_to_shutil_copy_sub_tag(
    tmp_path, primitive: str
) -> None:
    """All four shutil.copy-family primitives collapse to a single sub-tag."""
    seat_path = _seat_path(tmp_path)
    _write(seat_path, _archivist_module_with(primitive))
    violations = lint_tree(
        tmp_path / "pipeline" / "orchestrator" / "seats" / "archivist",
        [ARCHIVIST_NO_CANONICAL_MUTATE],
    )
    assert len(violations) == 1
    assert ".low_level_rename_shutil_copy" in violations[0].reason_tag


# ---------------------------------------------------------------------------
# os.link / os.symlink — both map to the same sub-tag per disposition packet
# §3.1.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("primitive", ["os.link(src, dst)", "os.symlink(src, dst)"])
def test_os_link_family_all_map_to_os_link_sub_tag(
    tmp_path, primitive: str
) -> None:
    seat_path = _seat_path(tmp_path)
    _write(seat_path, _archivist_module_with(primitive))
    violations = lint_tree(
        tmp_path / "pipeline" / "orchestrator" / "seats" / "archivist",
        [ARCHIVIST_NO_CANONICAL_MUTATE],
    )
    assert len(violations) == 1
    assert ".low_level_rename_os_link" in violations[0].reason_tag


# ---------------------------------------------------------------------------
# Import-alias resolution: `import os as o; o.replace(...)` still fires.
# ---------------------------------------------------------------------------


def test_rule_resolves_module_import_aliases(tmp_path) -> None:
    """Aliased imports (``import os as o``) resolve to the canonical module."""
    seat_path = _seat_path(tmp_path)
    seat_path.parent.mkdir(parents=True, exist_ok=True)
    seat_path.write_text(
        dedent(
            """
            import os as o

            def f(src: str, dst: str) -> None:
                o.replace(src, dst)
            """
        ).lstrip("\n"),
        encoding="utf-8",
    )
    violations = lint_tree(
        tmp_path / "pipeline" / "orchestrator" / "seats" / "archivist",
        [ARCHIVIST_NO_CANONICAL_MUTATE],
    )
    assert len(violations) == 1
    assert ".low_level_rename_replace" in violations[0].reason_tag


def test_rule_resolves_from_import_aliases(tmp_path) -> None:
    """``from os import replace`` resolves to ``os.replace`` and fires."""
    seat_path = _seat_path(tmp_path)
    seat_path.parent.mkdir(parents=True, exist_ok=True)
    seat_path.write_text(
        dedent(
            """
            from os import replace

            def f(src: str, dst: str) -> None:
                replace(src, dst)
            """
        ).lstrip("\n"),
        encoding="utf-8",
    )
    violations = lint_tree(
        tmp_path / "pipeline" / "orchestrator" / "seats" / "archivist",
        [ARCHIVIST_NO_CANONICAL_MUTATE],
    )
    assert len(violations) == 1
    assert ".low_level_rename_replace" in violations[0].reason_tag


def test_rule_resolves_from_import_with_asname(tmp_path) -> None:
    """``from shutil import move as m`` rebind tracked through to ``shutil.move``."""
    seat_path = _seat_path(tmp_path)
    seat_path.parent.mkdir(parents=True, exist_ok=True)
    seat_path.write_text(
        dedent(
            """
            from shutil import move as m

            def f(src: str, dst: str) -> None:
                m(src, dst)
            """
        ).lstrip("\n"),
        encoding="utf-8",
    )
    violations = lint_tree(
        tmp_path / "pipeline" / "orchestrator" / "seats" / "archivist",
        [ARCHIVIST_NO_CANONICAL_MUTATE],
    )
    assert len(violations) == 1
    assert ".low_level_rename_shutil_move" in violations[0].reason_tag


# ---------------------------------------------------------------------------
# Scope discipline — the rule only applies under the Archivist seat package.
# Other modules using these primitives must NOT fire (out-of-scope by glob).
# ---------------------------------------------------------------------------


def test_rule_does_not_fire_outside_archivist_seat(tmp_path) -> None:
    """A module outside pipeline/orchestrator/seats/archivist/** is unaffected."""
    other_path = (
        tmp_path / "pipeline" / "orchestrator" / "seats" / "intake" / "synthetic.py"
    )
    other_path.parent.mkdir(parents=True, exist_ok=True)
    other_path.write_text(
        _archivist_module_with("os.replace(src, dst)"),
        encoding="utf-8",
    )
    violations = lint_tree(
        tmp_path / "pipeline",
        [ARCHIVIST_NO_CANONICAL_MUTATE],
    )
    assert violations == []


# ---------------------------------------------------------------------------
# Clean-module assertion — Archivist seat code with no forbidden primitives
# raises zero violations.
# ---------------------------------------------------------------------------


def test_clean_archivist_module_passes(tmp_path) -> None:
    """A module that doesn't use any forbidden primitive passes clean."""
    seat_path = _seat_path(tmp_path)
    _write(
        seat_path,
        """
        from pathlib import Path

        def emit_digest(payload: bytes, dest: str) -> None:
            Path(dest).write_bytes(payload)
        """,
    )
    violations = lint_tree(
        tmp_path / "pipeline" / "orchestrator" / "seats" / "archivist",
        [ARCHIVIST_NO_CANONICAL_MUTATE],
    )
    assert violations == []


# ---------------------------------------------------------------------------
# Multi-primitive emission — a single module with multiple forbidden calls
# emits one violation per call.
# ---------------------------------------------------------------------------


def test_multiple_primitive_calls_emit_one_violation_each(tmp_path) -> None:
    """A module with six distinct forbidden primitive calls emits six violations.

    Cycle-1 RT-09 fold-in: ``os.renames`` joins the six-primitive sweep so
    the test covers the full sub-tag closure.
    """
    seat_path = _seat_path(tmp_path)
    seat_path.parent.mkdir(parents=True, exist_ok=True)
    seat_path.write_text(
        dedent(
            """
            import os
            import shutil

            def f(src: str, dst: str) -> None:
                os.replace(src, dst)
                os.rename(src, dst)
                os.renames(src, dst)
                shutil.move(src, dst)
                shutil.copy(src, dst)
                os.link(src, dst)
            """
        ).lstrip("\n"),
        encoding="utf-8",
    )
    violations = lint_tree(
        tmp_path / "pipeline" / "orchestrator" / "seats" / "archivist",
        [ARCHIVIST_NO_CANONICAL_MUTATE],
    )
    assert len(violations) == 6
    sub_tags_seen = {v.reason_tag for v in violations}
    assert sub_tags_seen == {
        "archivist_auto_apply_attempted.low_level_rename_replace",
        "archivist_auto_apply_attempted.low_level_rename_rename",
        "archivist_auto_apply_attempted.low_level_rename_renames",
        "archivist_auto_apply_attempted.low_level_rename_shutil_move",
        "archivist_auto_apply_attempted.low_level_rename_shutil_copy",
        "archivist_auto_apply_attempted.low_level_rename_os_link",
    }


# ---------------------------------------------------------------------------
# Forbidden-primitive table coverage — every entry in FORBIDDEN_PRIMITIVES
# must be reachable from one of the five §3.1 sub-tags.
# ---------------------------------------------------------------------------


def test_forbidden_primitives_table_covers_six_sub_tags() -> None:
    """The forbidden-primitive table folds ten call shapes into six sub-tags.

    Cycle-1 RT-09 fold-in: ``low_level_rename_renames`` extends the original
    five-sub-tag closure with ``os.renames`` as its own sub-tag.
    """
    sub_tags = set(FORBIDDEN_PRIMITIVES.values())
    assert sub_tags == {
        "low_level_rename_replace",
        "low_level_rename_rename",
        "low_level_rename_renames",
        "low_level_rename_shutil_move",
        "low_level_rename_shutil_copy",
        "low_level_rename_os_link",
    }


def test_forbidden_primitives_table_includes_all_ten_call_shapes() -> None:
    """Ten concrete call shapes are enumerated across the six sub-tags.

    Cycle-1 RT-09 fold-in: ``("os", "renames")`` joins the original
    nine-call-shape closure as the tenth concrete shape.
    """
    expected_call_shapes = {
        ("os", "replace"),
        ("os", "rename"),
        ("os", "renames"),
        ("shutil", "move"),
        ("shutil", "copy"),
        ("shutil", "copy2"),
        ("shutil", "copyfile"),
        ("shutil", "copytree"),
        ("os", "link"),
        ("os", "symlink"),
    }
    assert set(FORBIDDEN_PRIMITIVES.keys()) == expected_call_shapes


# ---------------------------------------------------------------------------
# Cycle-1 RT-14 fold-in — immutable forbidden-primitive table.  The exported
# public view is wrapped in ``types.MappingProxyType`` so a downstream
# consumer cannot mutate the table at runtime to silence the rule.
# ---------------------------------------------------------------------------


def test_forbidden_primitives_table_is_immutable() -> None:
    """The exported ``FORBIDDEN_PRIMITIVES`` view rejects mutation.

    Cycle-1 RT-14 fold-in: a contributor (or attacker) cannot silence the
    rule by reassigning entries in the public table — ``MappingProxyType``
    raises ``TypeError`` on any ``__setitem__`` / ``__delitem__`` / ``pop``.
    """
    with pytest.raises(TypeError):
        FORBIDDEN_PRIMITIVES[("os", "fdopen")] = "low_level_rename_bypass"  # type: ignore[index]
    with pytest.raises((TypeError, AttributeError)):
        FORBIDDEN_PRIMITIVES.clear()  # type: ignore[attr-defined]
    with pytest.raises((TypeError, AttributeError)):
        del FORBIDDEN_PRIMITIVES[("os", "replace")]  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Cycle-1 RT-15 fold-in — AST-lint is structural, not flow-sensitive.  Dead
# code (``if False:`` blocks) still triggers the rule because AST-lint walks
# the entire syntax tree regardless of reachability.  Confirms expected
# behavior so future contributors don't mistake the rule for a flow-sensitive
# analyzer.
# ---------------------------------------------------------------------------


def test_rule_fires_in_dead_code(tmp_path) -> None:
    """``if False:`` forbidden calls still fire — AST-lint is structural."""
    seat_path = _seat_path(tmp_path)
    _write(
        seat_path,
        """
        import os

        def f(src: str, dst: str) -> None:
            if False:
                os.replace(src, dst)
        """,
    )
    violations = lint_tree(
        tmp_path / "pipeline" / "orchestrator" / "seats" / "archivist",
        [ARCHIVIST_NO_CANONICAL_MUTATE],
    )
    assert len(violations) == 1
    assert ".low_level_rename_replace" in violations[0].reason_tag


# ---------------------------------------------------------------------------
# Live-tree regression guard — on-disk Archivist seat must pass DEFAULT_RULES
# with the new rule active (no regression of v0.2 SPEC LOCK skeleton state).
# ---------------------------------------------------------------------------


def test_live_archivist_seat_tree_passes_default_rules() -> None:
    """The shipping Archivist seat module passes the full DEFAULT_RULES set."""
    seat_dir = REPO_ROOT / "pipeline" / "orchestrator" / "seats" / "archivist"
    if not seat_dir.is_dir():
        pytest.skip("Archivist seat dir not yet present")
    violations = lint_tree(seat_dir, DEFAULT_RULES)
    assert violations == [], (
        f"Archivist seat tree drifted vs. DEFAULT_RULES: {violations}"
    )
