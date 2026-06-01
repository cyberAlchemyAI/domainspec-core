"""§12 Uploader cross-gate composition — PRE-34 must run before PRE-35.

MEDIUM-1 (§4 v2.7 pre-fix dispatch): F-UPLOADER-ATTACHMENT-MISSING
(PRE-34) tests file existence; F-UPLOADER-ATTACHMENT-TAMPERED (PRE-35)
tests assembly-time hash equality. PRE-35 is logically dependent on
PRE-34 — a missing file cannot be hashed. The §4 v2.7 amendment §4.5
ordering rationale states: "PRE-34 (file existence) before PRE-35 (file
integrity) — a missing file cannot be hashed."

This test exercises the dependency: when PRE-35 fires alone (without
PRE-34 having passed first against a real file), the gate runner must
emit a warning and the test must fail.

Because the gate runner module is not yet on disk in this slice (Cowork
session is still pre-fixing §12), this test asserts the *contract* the
runner must honor: a synthetic runner that chains PRE-34 → PRE-35
short-circuits when PRE-34 fails, and emits a warning when PRE-35 is
invoked without PRE-34 first.
"""

from __future__ import annotations

import warnings
from datetime import datetime, timezone
from typing import Mapping

import pytest

from pipeline.logician.gates.f_uploader_attachment_missing import (
    F_UPLOADER_ATTACHMENT_MISSING,
    check_uploader_attachment_missing,
)
from pipeline.logician.gates.f_uploader_attachment_tampered import (
    F_UPLOADER_ATTACHMENT_TAMPERED,
    check_uploader_attachment_tampered,
)
from pipeline.orchestrator.seats.uploader import AttachmentRef


def _att(path: str, content_hash: str = "0" * 128) -> AttachmentRef:
    return AttachmentRef(
        file_path=path,
        original_file_name=path.split("/")[-1],
        content_sha3_512=content_hash,
        uploaded_at_utc=datetime.now(timezone.utc),
        uploaded_by="josh",
        rfa_attachment_match=None,
    )


def _runner_in_sequence(
    *,
    attachments: tuple,
    files_on_disk: set[str],
    assembly_hashes: Mapping[str, str],
) -> tuple:
    """Synthetic gate runner — invokes PRE-34 then PRE-35 in correct order."""
    pre_34 = check_uploader_attachment_missing(
        attachments=attachments,
        file_exists=lambda p: p in files_on_disk,
    )
    if not pre_34.success:
        # Short-circuit: PRE-35 doesn't run on missing files.
        return (pre_34, None)
    pre_35 = check_uploader_attachment_tampered(
        attachments=attachments,
        assembly_time_hashes=assembly_hashes,
    )
    return (pre_34, pre_35)


def _runner_pre_35_alone(
    *,
    attachments: tuple,
    assembly_hashes: Mapping[str, str],
) -> object:
    """Synthetic runner that fires PRE-35 without first running PRE-34.

    Per the §4 v2.7 §4.5 ordering rationale, this is incorrect ordering;
    the runner must emit a warning to flag the missing dependency.
    """
    warnings.warn(
        "PRE-35 (F-UPLOADER-ATTACHMENT-TAMPERED) invoked without PRE-34 "
        "(F-UPLOADER-ATTACHMENT-MISSING) having passed first — sequence "
        "position violation per §4 v2.7 §4.5",
        RuntimeWarning,
        stacklevel=2,
    )
    return check_uploader_attachment_tampered(
        attachments=attachments,
        assembly_time_hashes=assembly_hashes,
    )


def test_pre34_passes_then_pre35_passes_when_files_exist_and_hash_matches() -> None:
    att = _att("/tmp/real.pdf", content_hash="abc")
    pre_34, pre_35 = _runner_in_sequence(
        attachments=(att,),
        files_on_disk={"/tmp/real.pdf"},
        assembly_hashes={"/tmp/real.pdf": "abc"},
    )
    assert pre_34.success is True
    assert pre_35 is not None
    assert pre_35.success is True


def test_pre34_blocks_pre35_when_file_missing() -> None:
    att = _att("/tmp/missing.pdf", content_hash="abc")
    pre_34, pre_35 = _runner_in_sequence(
        attachments=(att,),
        files_on_disk=set(),
        assembly_hashes={},
    )
    assert pre_34.success is False
    assert pre_34.failure_code == F_UPLOADER_ATTACHMENT_MISSING
    # Short-circuit: PRE-35 must not have run.
    assert pre_35 is None


def test_pre35_alone_emits_warning() -> None:
    """Calling PRE-35 without PRE-34 first must emit a RuntimeWarning."""
    att = _att("/tmp/anywhere.pdf", content_hash="abc")
    with pytest.warns(RuntimeWarning, match="PRE-34"):
        result = _runner_pre_35_alone(
            attachments=(att,),
            assembly_hashes={},  # empty → tampered (treated as tamper signal)
        )
    # Without PRE-34 first, PRE-35 will tamper-signal because the empty
    # assembly_hashes mapping has no entry for the file. This is the
    # sequence-position violation: the operator gets a tamper alarm for a
    # file that doesn't exist on disk.
    assert result.failure_code == F_UPLOADER_ATTACHMENT_TAMPERED


def test_pre34_pre35_codes_are_distinct() -> None:
    """Sanity: the two codes are distinct (distinct failure surfaces)."""
    assert F_UPLOADER_ATTACHMENT_MISSING != F_UPLOADER_ATTACHMENT_TAMPERED
