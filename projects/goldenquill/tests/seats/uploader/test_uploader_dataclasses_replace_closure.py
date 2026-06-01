"""§12 Uploader — verify ``dataclasses.replace`` cannot bypass the gate.

The classic frozen-dataclass mutation bypass is to call
``dataclasses.replace(out, submitted=True)``: the resulting instance is a
fresh frozen object that satisfies the type system without re-running
the original assignment. Our defense is that ``replace`` constructs a
new instance, which re-invokes ``__post_init__``, which raises.

This test asserts the gate fires on every replacement that flips
``submitted`` to True.

Per Blueprint §12.9.3 + §4 v2.7 amendment.
"""

from __future__ import annotations

import dataclasses
from datetime import datetime, timezone

import pytest

from pipeline.orchestrator.seats.uploader import (
    ReadinessChecklist,
    SubmissionManifest,
    UploaderOutput,
)


def _make_output() -> UploaderOutput:
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
    return UploaderOutput(
        run_id="r1",
        manifest=manifest,
        readiness_checklist=checklist,
        output_dir="/tmp",
    )


def test_default_construction_passes() -> None:
    out = _make_output()
    assert out.submitted is False


def test_dataclasses_replace_with_submitted_true_raises() -> None:
    out = _make_output()
    with pytest.raises(RuntimeError) as exc_info:
        dataclasses.replace(out, submitted=True)
    assert "F-UPLOADER-AUTOSUBMIT-ATTEMPTED" in str(exc_info.value)


def test_dataclasses_replace_with_submitted_false_passes() -> None:
    out = _make_output()
    # Replace into the same value — should still PASS.
    new = dataclasses.replace(out, submitted=False)
    assert new.submitted is False


def test_dataclasses_replace_with_other_field_passes() -> None:
    out = _make_output()
    new = dataclasses.replace(out, output_dir="/tmp/elsewhere")
    assert new.submitted is False
    assert new.output_dir == "/tmp/elsewhere"


def test_direct_construction_with_submitted_true_raises() -> None:
    """Direct constructor call with submitted=True must also raise."""
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
    assert "F-UPLOADER-AUTOSUBMIT-ATTEMPTED" in str(exc_info.value)
