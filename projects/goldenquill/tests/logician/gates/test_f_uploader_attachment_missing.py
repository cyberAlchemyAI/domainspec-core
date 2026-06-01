"""Unit tests for F-UPLOADER-ATTACHMENT-MISSING (PRE-34).

Per Blueprint §12.9.5 + §4 v2.7 amendment.
"""

from __future__ import annotations

from dataclasses import dataclass

from pipeline.logician.gates.f_uploader_attachment_missing import (
    F_UPLOADER_ATTACHMENT_MISSING,
    check_uploader_attachment_missing,
)


@dataclass(frozen=True)
class _Att:
    file_path: str


def _exists(present: set[str]):
    def _r(file_path: str) -> bool:
        return file_path in present
    return _r


def test_failure_code_constant() -> None:
    assert F_UPLOADER_ATTACHMENT_MISSING == "F-UPLOADER-ATTACHMENT-MISSING"


def test_all_files_present_passes() -> None:
    r = check_uploader_attachment_missing(
        attachments=[_Att("a.pdf"), _Att("b.pdf")],
        file_exists=_exists({"a.pdf", "b.pdf"}),
    )
    assert r.success is True
    assert r.failure_code is None
    assert r.missing == ()


def test_one_file_missing_fails() -> None:
    r = check_uploader_attachment_missing(
        attachments=[_Att("a.pdf"), _Att("b.pdf")],
        file_exists=_exists({"a.pdf"}),
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_ATTACHMENT_MISSING
    assert r.missing == ("b.pdf",)


def test_all_files_missing_fails() -> None:
    r = check_uploader_attachment_missing(
        attachments=[_Att("a.pdf"), _Att("b.pdf")],
        file_exists=_exists(set()),
    )
    assert r.success is False
    assert r.missing == ("a.pdf", "b.pdf")


def test_reader_exception_fails_closed() -> None:
    def _bad(file_path: str) -> bool:
        raise OSError("disk fault")

    r = check_uploader_attachment_missing(
        attachments=[_Att("a.pdf")],
        file_exists=_bad,
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_ATTACHMENT_MISSING


def test_empty_attachments_passes() -> None:
    r = check_uploader_attachment_missing(
        attachments=[],
        file_exists=_exists(set()),
    )
    assert r.success is True
