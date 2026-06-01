"""Unit tests for F-UPLOADER-ATTACHMENT-TAMPERED (PRE-35).

Per Blueprint §12.9.5 + §4 v2.7 amendment.
"""

from __future__ import annotations

from dataclasses import dataclass

from pipeline.logician.gates.f_uploader_attachment_tampered import (
    F_UPLOADER_ATTACHMENT_TAMPERED,
    check_uploader_attachment_tampered,
)


@dataclass(frozen=True)
class _Att:
    file_path: str
    content_sha3_512: str


def test_failure_code_constant() -> None:
    assert F_UPLOADER_ATTACHMENT_TAMPERED == "F-UPLOADER-ATTACHMENT-TAMPERED"


def test_all_hashes_match_passes() -> None:
    atts = [
        _Att(file_path="a.pdf", content_sha3_512="aaa"),
        _Att(file_path="b.pdf", content_sha3_512="bbb"),
    ]
    r = check_uploader_attachment_tampered(
        attachments=atts,
        assembly_time_hashes={"a.pdf": "aaa", "b.pdf": "bbb"},
    )
    assert r.success is True
    assert r.failure_code is None
    assert r.tampered == ()


def test_one_hash_mismatch_fails() -> None:
    atts = [
        _Att(file_path="a.pdf", content_sha3_512="aaa"),
        _Att(file_path="b.pdf", content_sha3_512="bbb"),
    ]
    r = check_uploader_attachment_tampered(
        attachments=atts,
        assembly_time_hashes={"a.pdf": "aaa", "b.pdf": "ZZZ"},
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_ATTACHMENT_TAMPERED
    assert r.tampered == ("b.pdf",)


def test_missing_hash_treated_as_tampered() -> None:
    atts = [_Att(file_path="a.pdf", content_sha3_512="aaa")]
    r = check_uploader_attachment_tampered(
        attachments=atts,
        assembly_time_hashes={},
    )
    assert r.success is False
    assert r.tampered == ("a.pdf",)


def test_empty_attachments_passes() -> None:
    r = check_uploader_attachment_tampered(
        attachments=[],
        assembly_time_hashes={},
    )
    assert r.success is True
