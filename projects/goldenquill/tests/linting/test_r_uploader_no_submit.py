"""Tests for R-UPLOADER-NO-SUBMIT (pipeline.linting.ast_lint).

Per Blueprint §12.9.3 + §4 v2.7 amendment. Verifies the allow-list-based
AST-lint rule fires on aliased / alternative HTTP-client / dynamic-import
bypass attempts and stays silent on legitimate Uploader / adapter code.

The rule's target glob is:
  - pipeline/orchestrator/seats/uploader.py
  - pipeline/orchestrator/seats/uploader_adapters/*.py

Fixtures live under ``tests/linting/fixtures/uploader_no_submit/``. The
test relocates each fixture to a tmpdir mimicking the target glob layout
so the rule's path filter applies, then asserts violations / no-violations.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from pipeline.linting.ast_lint import (
    DEFAULT_RULES,
    UPLOADER_ALLOW_LIST,
    UPLOADER_NO_SUBMIT,
    lint_tree,
)


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE_DIR = (
    REPO_ROOT / "tests" / "linting" / "fixtures" / "uploader_no_submit"
)


# ---------------------------------------------------------------------------
# Surface contract
# ---------------------------------------------------------------------------


def test_rule_is_registered_in_default_rules() -> None:
    assert UPLOADER_NO_SUBMIT in DEFAULT_RULES


def test_rule_name_and_reason_tag() -> None:
    assert UPLOADER_NO_SUBMIT.name == "R_UPLOADER_NO_SUBMIT"
    assert UPLOADER_NO_SUBMIT.reason_tag == "uploader_call_outside_allow_list"


def test_allow_list_is_frozen_set_of_strings() -> None:
    assert isinstance(UPLOADER_ALLOW_LIST, frozenset)
    assert all(isinstance(t, str) for t in UPLOADER_ALLOW_LIST)
    # Sanity: a few load-bearing entries.
    assert "module:hashlib" in UPLOADER_ALLOW_LIST
    assert "attr:hashlib.sha3_512" in UPLOADER_ALLOW_LIST
    assert "module:subprocess" in UPLOADER_ALLOW_LIST  # LibreOffice path
    assert "attr:subprocess.run" in UPLOADER_ALLOW_LIST
    assert "module:datetime" in UPLOADER_ALLOW_LIST
    assert "module:dataclasses" in UPLOADER_ALLOW_LIST


# ---------------------------------------------------------------------------
# Live-tree regression — Uploader + adapters must stay clean
# ---------------------------------------------------------------------------


def test_live_uploader_tree_has_zero_violations() -> None:
    vs = lint_tree(
        REPO_ROOT / "pipeline" / "orchestrator" / "seats",
        [UPLOADER_NO_SUBMIT],
    )
    assert vs == [], f"Uploader tree drifted: {[str(v) for v in vs]}"


# ---------------------------------------------------------------------------
# Fixture lift helper — relocate fixture into the target glob layout
# ---------------------------------------------------------------------------


def _stage_fixture(
    tmp_path: Path,
    fixture_name: str,
    *,
    target_subdir: str = "uploader_adapters",
) -> Path:
    """Copy fixture into tmpdir under the rule's target glob layout.

    Returns the tmpdir root (the path to pass to lint_tree).
    """
    seats_dir = tmp_path / "pipeline" / "orchestrator" / "seats"
    if target_subdir:
        target_dir = seats_dir / target_subdir
    else:
        target_dir = seats_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    src = FIXTURE_DIR / fixture_name
    dst = target_dir / fixture_name
    shutil.copyfile(src, dst)
    return tmp_path


# ---------------------------------------------------------------------------
# Clean fixture — must produce zero violations
# ---------------------------------------------------------------------------


def test_clean_uploader_fixture_passes(tmp_path: Path) -> None:
    root = _stage_fixture(tmp_path, "clean_uploader.py")
    vs = lint_tree(root, [UPLOADER_NO_SUBMIT])
    assert vs == [], f"clean fixture should be allow-listed: {vs}"


# ---------------------------------------------------------------------------
# Dirty fixtures — each must produce at least one R-UPLOADER-NO-SUBMIT
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fixture_name",
    [
        "dirty_httpx_post.py",
        "dirty_requests_request.py",
        "dirty_aiohttp.py",
        "dirty_urllib3.py",
        "dirty_raw_socket.py",
        "dirty_subprocess_curl.py",
        "dirty_aliased_post.py",
    ],
)
def test_dirty_fixture_fires_rule(tmp_path: Path, fixture_name: str) -> None:
    root = _stage_fixture(tmp_path, fixture_name)
    vs = lint_tree(root, [UPLOADER_NO_SUBMIT])
    assert vs, f"{fixture_name}: expected R-UPLOADER-NO-SUBMIT violation, got none"
    assert all(v.rule_name == "R_UPLOADER_NO_SUBMIT" for v in vs)
    assert all(
        v.reason_tag == "uploader_call_outside_allow_list" for v in vs
    )


# ---------------------------------------------------------------------------
# Aliased-import bypass — proves the allow-list approach beats the regex
# ---------------------------------------------------------------------------


def test_aliased_post_collapses_to_httpx_post_token(tmp_path: Path) -> None:
    """``from httpx import post as p; p(...)`` collapses via _AliasResolver
    to a token starting with ``attr:httpx.post`` — not on the allow-list.
    """
    root = _stage_fixture(tmp_path, "dirty_aliased_post.py")
    vs = lint_tree(root, [UPLOADER_NO_SUBMIT])
    assert vs, "aliased httpx.post via `from httpx import post as p` must fire"
    # The violation message names the resolved token.
    msgs = " ".join(v.message for v in vs)
    assert "httpx.post" in msgs, msgs


# ---------------------------------------------------------------------------
# uploader.py path coverage — fixture also runs when staged to seats/
# ---------------------------------------------------------------------------


def test_dirty_fixture_at_uploader_py_path_fires_rule(tmp_path: Path) -> None:
    """Same dirty fixture, staged at the seats/ root as uploader.py."""
    seats_dir = tmp_path / "pipeline" / "orchestrator" / "seats"
    seats_dir.mkdir(parents=True, exist_ok=True)
    src = FIXTURE_DIR / "dirty_httpx_post.py"
    dst = seats_dir / "uploader.py"
    shutil.copyfile(src, dst)
    vs = lint_tree(tmp_path, [UPLOADER_NO_SUBMIT])
    assert vs, "rule must fire when dirty code lives at seats/uploader.py"
