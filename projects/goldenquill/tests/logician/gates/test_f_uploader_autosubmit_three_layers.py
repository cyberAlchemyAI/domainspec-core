"""§12 Uploader F-UPLOADER-AUTOSUBMIT-ATTEMPTED — three-layer composition.

MEDIUM-3 (§4 v2.7 pre-fix dispatch): one auto-submit stimulus must trip
three independent fail signals:

  Layer 1 — AST-lint rule R-UPLOADER-NO-SUBMIT
  Layer 2 — Cedar policy ``uploader_no_submit.cedar``
  Layer 3 — Runtime gate ``UploaderOutput.__post_init__`` raise

This test asserts all three fire on the same stimulus. Layers 1 and 3 are
exercised against real code paths; Layer 2 is exercised via the
``cedar_intent_reader`` Protocol surface on
``check_uploader_autosubmit_attempted`` since the Cedar policy file
itself is out of v0.1 scope (architecture v7.0.6 — Logician Cedar policy
authoring is its own LOCK round).
"""

from __future__ import annotations

import shutil
import textwrap
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pytest

from pipeline.linting.ast_lint import UPLOADER_NO_SUBMIT, lint_tree
from pipeline.logician.gates.f_uploader_autosubmit_attempted import (
    F_UPLOADER_AUTOSUBMIT_ATTEMPTED,
    check_uploader_autosubmit_attempted,
)
from pipeline.orchestrator.seats.uploader import (
    ReadinessChecklist,
    SubmissionManifest,
    UploaderOutput,
)


@dataclass(frozen=True)
class _Output:
    submitted: bool


def test_layer_1_ast_lint_fires_on_autosubmit_attempt(tmp_path: Path) -> None:
    """Static analysis rejects an auto-submit code path."""
    seats_dir = tmp_path / "pipeline" / "orchestrator" / "seats"
    seats_dir.mkdir(parents=True, exist_ok=True)
    src = (
        Path(__file__).resolve().parent.parent.parent
        / "linting"
        / "fixtures"
        / "uploader_no_submit"
        / "dirty_httpx_post.py"
    )
    shutil.copyfile(src, seats_dir / "uploader.py")
    vs = lint_tree(tmp_path, [UPLOADER_NO_SUBMIT])
    assert vs, "Layer 1 (AST-lint) failed to fire on httpx.post"


def test_layer_2_cedar_intent_reader_fires_on_submission_intent() -> None:
    """The cedar_intent_reader surrogate fires on a forbidden intent key."""
    r = check_uploader_autosubmit_attempted(
        output=_Output(submitted=False),
        cedar_intent_reader=lambda: {"submission_api_call"},
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_AUTOSUBMIT_ATTEMPTED
    assert r.layer == "cedar_intent"


def test_layer_3_runtime_post_init_raises_on_submitted_true() -> None:
    """UploaderOutput.__post_init__ raises when submitted=True."""
    manifest = SubmissionManifest(
        entries=(),
        assembled_at_utc=datetime.now(timezone.utc),
        adapter_id="copy_paste",
        run_id="r1",
    )
    checklist = ReadinessChecklist(
        overall_status="ready",
        items=(),
        fail_count=0,
        warn_count=0,
        pass_count=0,
        checked_at_utc=datetime.now(timezone.utc),
    )
    with pytest.raises(RuntimeError) as exc_info:
        UploaderOutput(
            run_id="r1",
            manifest=manifest,
            readiness_checklist=checklist,
            output_dir="/tmp",
            submitted=True,
        )
    assert F_UPLOADER_AUTOSUBMIT_ATTEMPTED in str(exc_info.value)


def test_three_layers_compose_on_one_stimulus(tmp_path: Path) -> None:
    """One auto-submit stimulus → three independent fail signals."""
    # Layer 1
    seats_dir = tmp_path / "pipeline" / "orchestrator" / "seats"
    seats_dir.mkdir(parents=True, exist_ok=True)
    (seats_dir / "uploader.py").write_text(
        textwrap.dedent(
            """
            import httpx

            def submit(url, payload):
                httpx.post(url, content=payload)
            """
        ).lstrip()
    )
    layer_1_violations = lint_tree(tmp_path, [UPLOADER_NO_SUBMIT])
    assert layer_1_violations, "Layer 1 must fire"

    # Layer 2
    layer_2 = check_uploader_autosubmit_attempted(
        output=_Output(submitted=False),
        cedar_intent_reader=lambda: {"submission_api_call"},
    )
    assert layer_2.failure_code == F_UPLOADER_AUTOSUBMIT_ATTEMPTED

    # Layer 3
    manifest = SubmissionManifest(
        entries=(),
        assembled_at_utc=datetime.now(timezone.utc),
        adapter_id="copy_paste",
        run_id="r1",
    )
    checklist = ReadinessChecklist(
        overall_status="ready",
        items=(),
        fail_count=0,
        warn_count=0,
        pass_count=0,
        checked_at_utc=datetime.now(timezone.utc),
    )
    with pytest.raises(RuntimeError) as exc_info:
        UploaderOutput(
            run_id="r1",
            manifest=manifest,
            readiness_checklist=checklist,
            output_dir="/tmp",
            submitted=True,
        )
    assert F_UPLOADER_AUTOSUBMIT_ATTEMPTED in str(exc_info.value)
