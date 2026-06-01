"""Unit tests for F-UPLOADER-AUTOSUBMIT-ATTEMPTED (PRE-29). NO M13 BYPASS.

Per Blueprint §12.9.3 + §4 v2.7 amendment.
"""

from __future__ import annotations

from dataclasses import dataclass

from pipeline.logician.gates.f_uploader_autosubmit_attempted import (
    F_UPLOADER_AUTOSUBMIT_ATTEMPTED,
    check_uploader_autosubmit_attempted,
)


@dataclass(frozen=True)
class _Output:
    submitted: bool


def test_failure_code_constant() -> None:
    assert F_UPLOADER_AUTOSUBMIT_ATTEMPTED == "F-UPLOADER-AUTOSUBMIT-ATTEMPTED"


def test_submitted_false_passes() -> None:
    r = check_uploader_autosubmit_attempted(output=_Output(submitted=False))
    assert r.success is True
    assert r.failure_code is None
    assert r.layer is None


def test_submitted_true_fails_runtime_layer() -> None:
    r = check_uploader_autosubmit_attempted(output=_Output(submitted=True))
    assert r.success is False
    assert r.failure_code == F_UPLOADER_AUTOSUBMIT_ATTEMPTED
    assert r.layer == "runtime_submitted_flag"


def test_cedar_intent_with_forbidden_key_fails() -> None:
    r = check_uploader_autosubmit_attempted(
        output=_Output(submitted=False),
        cedar_intent_reader=lambda: {"submission_api_call", "audit_log"},
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_AUTOSUBMIT_ATTEMPTED
    assert r.layer == "cedar_intent"


def test_cedar_intent_clean_passes() -> None:
    r = check_uploader_autosubmit_attempted(
        output=_Output(submitted=False),
        cedar_intent_reader=lambda: {"audit_log", "manifest_write"},
    )
    assert r.success is True


def test_cedar_intent_reader_raises_fails_closed() -> None:
    def _bad() -> set[str]:
        raise RuntimeError("intent reader broke")

    r = check_uploader_autosubmit_attempted(
        output=_Output(submitted=False),
        cedar_intent_reader=_bad,
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_AUTOSUBMIT_ATTEMPTED
    assert r.layer == "cedar_intent"


def test_runtime_layer_takes_precedence_over_cedar() -> None:
    """Layer 3 fires first; reader never invoked when submitted=True."""
    invoked: list[bool] = []

    def _reader() -> set[str]:
        invoked.append(True)
        return set()

    r = check_uploader_autosubmit_attempted(
        output=_Output(submitted=True),
        cedar_intent_reader=_reader,
    )
    assert r.success is False
    assert r.layer == "runtime_submitted_flag"
    assert invoked == []
