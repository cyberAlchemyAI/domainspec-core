"""tests.demo.conftest — Demo Driver MVP fixture library.

Provides pytest fixtures for the Demo Driver MVP end-to-end test harness
(:mod:`tests.demo.test_demo_driver`). Built on top of the existing §5 R13
integration harness at :mod:`tests.loop.conftest_section_5` — the demo
driver is composition over LOCKed §5 primitives, not new test infrastructure.

Spec card: ``pipeline/engineering/spec_cards/demo_driver_mvp_end_to_end.md``.

Fixtures
--------

``demo_rfa_path`` / ``demo_project_context_path`` / ``demo_rubric_path`` /
``demo_pipeline_output_schema_path``
    Path objects for the four canonical fixture files. Tests read these
    deterministically; bytes are committed to the repo as snapshots
    (deliberate trade-off: live RFA / live PROJECT_CONTEXT would couple
    the demo run to mutable upstream state and break reproducibility).

``demo_rfa_bytes`` / ``demo_project_context_bytes`` / ``demo_rubric_bytes``
    UTF-8-decoded bytes content; SHA-256 digests are derived per-run and
    threaded into ``run_pipeline``'s ``rfa_hash`` + ``project_context_hash``
    kwargs.

``demo_submission_harness``
    A :class:`tests.loop.conftest_section_5.SubmissionHarness` constructed
    via :func:`build_submission_harness` — happy-path defaults
    (PRE-gate PASS, POST-gate PASS, all seats land first cascade level).
    Tests that require failure-mode injection construct their own harness
    via the same builder with overrides.

``demo_pipeline_output_schema``
    Loaded JSONSchema (Python dict) for validating
    :class:`pipeline.loop.run_pipeline.PipelineRunResult` shapes.

Reference module — not a fixture file:
    ``tests.loop.conftest_section_5`` carries the actual builder
    (:func:`build_submission_harness`) + Launcher / Clock / Vault fakes.
    This conftest re-exports nothing; tests import builders directly
    from the loop conftest module.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

# Public imports — the demo conftest re-exports nothing; this is for the
# benefit of test files importing the demo conftest module directly.
from tests.loop.conftest_section_5 import (
    SubmissionHarness,
    build_submission_harness,
)

# ---------------------------------------------------------------------------
# Repo-root path resolution
# ---------------------------------------------------------------------------
#
# tests/demo/conftest.py → tests/demo → tests → repo root
# Three .parent hops; resolved at import time, not per-fixture, to avoid
# repeated stat() syscalls.

_THIS_FILE: Path = Path(__file__).resolve()
_DEMO_DIR: Path = _THIS_FILE.parent
_TESTS_DIR: Path = _DEMO_DIR.parent
_REPO_ROOT: Path = _TESTS_DIR.parent


# ---------------------------------------------------------------------------
# Canonical fixture paths
# ---------------------------------------------------------------------------


@pytest.fixture
def demo_rfa_path() -> Path:
    """Path to the demo RFA snapshot (USDA VAPG FY26)."""

    return _DEMO_DIR / "demo_rfa" / "vapg_fy26_synopsis.json"


@pytest.fixture
def demo_project_context_path() -> Path:
    """Path to the demo PROJECT_CONTEXT snapshot (FIT Farms LLC)."""

    return _DEMO_DIR / "demo_project_context" / "PROJECT_CONTEXT.md"


@pytest.fixture
def demo_rubric_path() -> Path:
    """Path to the canonical VAPG FY26 rubric (live, not snapshotted).

    Pinned to ``pipeline/rubrics/vapg_fy26.json`` — the rubric is
    committee-LOCKed engineering content, so the live file IS the
    deterministic fixture. Snapshotting would create a divergence
    surface; reading live ties the demo run to the LOCKed rubric.
    """

    return _REPO_ROOT / "pipeline" / "rubrics" / "vapg_fy26.json"


@pytest.fixture
def demo_pipeline_output_schema_path() -> Path:
    """Path to the demo pipeline-output JSONSchema."""

    return _DEMO_DIR / "expected" / "pipeline_output_schema.json"


# ---------------------------------------------------------------------------
# Bytes content fixtures (deterministic — no clock / no environment)
# ---------------------------------------------------------------------------


@pytest.fixture
def demo_rfa_bytes(demo_rfa_path: Path) -> bytes:
    """RFA snapshot bytes."""

    return demo_rfa_path.read_bytes()


@pytest.fixture
def demo_project_context_bytes(demo_project_context_path: Path) -> bytes:
    """PROJECT_CONTEXT snapshot bytes."""

    return demo_project_context_path.read_bytes()


@pytest.fixture
def demo_rubric_bytes(demo_rubric_path: Path) -> bytes:
    """VAPG FY26 rubric bytes (live engineering content)."""

    return demo_rubric_path.read_bytes()


# ---------------------------------------------------------------------------
# Hash fixtures — threaded into run_pipeline kwargs
# ---------------------------------------------------------------------------


@pytest.fixture
def demo_rfa_hash(demo_rfa_bytes: bytes) -> str:
    """SHA-256 hex digest of the RFA snapshot — feeds run_pipeline.rfa_hash."""

    return hashlib.sha256(demo_rfa_bytes).hexdigest()


@pytest.fixture
def demo_project_context_hash(demo_project_context_bytes: bytes) -> str:
    """SHA-256 hex digest of the PROJECT_CONTEXT snapshot."""

    return hashlib.sha256(demo_project_context_bytes).hexdigest()


# ---------------------------------------------------------------------------
# Schema fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def demo_pipeline_output_schema(
    demo_pipeline_output_schema_path: Path,
) -> dict[str, object]:
    """Loaded JSONSchema dict for PipelineRunResult validation."""

    return json.loads(demo_pipeline_output_schema_path.read_text("utf-8"))


# ---------------------------------------------------------------------------
# Rubric fixture — JSON-decoded
# ---------------------------------------------------------------------------


@pytest.fixture
def demo_rubric(demo_rubric_bytes: bytes) -> dict[str, object]:
    """VAPG FY26 rubric, JSON-decoded."""

    return json.loads(demo_rubric_bytes.decode("utf-8"))


# ---------------------------------------------------------------------------
# Submission harness fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def demo_submission_harness() -> SubmissionHarness:
    """Happy-path SubmissionHarness — PRE-gate PASS, POST-gate PASS, all
    seats land their first cascade level on the first call.

    Tests that need failure-mode injection should construct their own
    harness via :func:`build_submission_harness` with overrides for
    ``pre_gate_result`` / ``post_gate_result`` / launcher per-seat queue.
    """

    return build_submission_harness(run_id="demo-mvp-happy")
