"""§12 Uploader — AST-lint anti-autosubmit reference test.

The R-UPLOADER-NO-SUBMIT rule is implemented in
``pipeline/linting/ast_lint.py`` (see TASK 2 of the §4 v2.7 pre-fix
dispatch). Rule logic, fixtures, and aliased-import bypass coverage live
under ``tests/linting/test_r_uploader_no_submit.py``.

This module's role is narrowed to a thin reference test:
  1. The rule is registered in ``DEFAULT_RULES``.
  2. The rule's target glob covers the live Uploader / adapter tree.
  3. The live Uploader / adapter tree is currently clean under the rule.

We do not duplicate the rule's logic here. Bypass-class fixtures live with
the rule definition.
"""

from __future__ import annotations

from pathlib import Path

from pipeline.linting.ast_lint import (
    DEFAULT_RULES,
    UPLOADER_NO_SUBMIT,
    _glob_matches_path,
    lint_tree,
)


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SEATS_DIR = REPO_ROOT / "pipeline" / "orchestrator" / "seats"


def test_rule_is_registered() -> None:
    """R-UPLOADER-NO-SUBMIT must appear in DEFAULT_RULES (CI hook)."""
    assert UPLOADER_NO_SUBMIT in DEFAULT_RULES


def test_rule_target_covers_uploader_py() -> None:
    """The rule must target pipeline/orchestrator/seats/uploader.py."""
    # The rule uses a multi-glob check function; verify glob coverage by
    # asserting the rule fires at lint time on the live uploader.py path.
    assert _glob_matches_path(
        UPLOADER_NO_SUBMIT.target_glob,
        SEATS_DIR / "uploader.py",
    )


def test_rule_target_covers_adapters_dir() -> None:
    """The rule must target pipeline/orchestrator/seats/uploader_adapters/."""
    sample_adapter = SEATS_DIR / "uploader_adapters" / "grants_gov.py"
    assert _glob_matches_path(UPLOADER_NO_SUBMIT.target_glob, sample_adapter)


def test_live_uploader_and_adapters_pass_rule() -> None:
    """The live uploader.py + every adapter file must be clean under the rule."""
    vs = lint_tree(SEATS_DIR, [UPLOADER_NO_SUBMIT])
    assert vs == [], (
        "F-UPLOADER-AUTOSUBMIT-ATTEMPTED defense layer 1 violation: "
        f"{[str(v) for v in vs]}"
    )
