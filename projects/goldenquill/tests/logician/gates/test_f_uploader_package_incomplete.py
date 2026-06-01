"""Unit tests for F-UPLOADER-PACKAGE-INCOMPLETE (POST-17).

Per Blueprint §12.9.1 + §4 v2.7 amendment.
"""

from __future__ import annotations

from dataclasses import dataclass

from pipeline.logician.gates.f_uploader_package_incomplete import (
    F_UPLOADER_PACKAGE_INCOMPLETE,
    check_uploader_package_incomplete,
)


@dataclass(frozen=True)
class _Section:
    section_name: str


@dataclass(frozen=True)
class _Rfa:
    section_structure: tuple
    required_attachments: tuple


class _Manifest:
    def __init__(self, sections_present: set[str]) -> None:
        self._sections = sections_present

    def has_section(self, section_name: str) -> bool:
        return section_name in self._sections


class _AttManifest:
    def __init__(self, attachments_present: set[str]) -> None:
        self._atts = attachments_present

    def has_attachment(self, attachment_name: str) -> bool:
        return attachment_name in self._atts


def test_failure_code_constant() -> None:
    assert F_UPLOADER_PACKAGE_INCOMPLETE == "F-UPLOADER-PACKAGE-INCOMPLETE"


def test_complete_package_passes() -> None:
    rfa = _Rfa(
        section_structure=(_Section("narrative"), _Section("budget")),
        required_attachments=("sf424.pdf", "audit.pdf"),
    )
    r = check_uploader_package_incomplete(
        rfa=rfa,
        manifest=_Manifest({"narrative", "budget"}),
        attachment_manifest=_AttManifest({"sf424.pdf", "audit.pdf"}),
    )
    assert r.success is True
    assert r.failure_code is None
    assert r.missing_sections == ()
    assert r.missing_attachments == ()


def test_missing_section_fails() -> None:
    rfa = _Rfa(
        section_structure=(_Section("narrative"), _Section("budget")),
        required_attachments=(),
    )
    r = check_uploader_package_incomplete(
        rfa=rfa,
        manifest=_Manifest({"narrative"}),
        attachment_manifest=_AttManifest(set()),
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_PACKAGE_INCOMPLETE
    assert r.missing_sections == ("budget",)


def test_missing_attachment_fails() -> None:
    rfa = _Rfa(
        section_structure=(),
        required_attachments=("sf424.pdf",),
    )
    r = check_uploader_package_incomplete(
        rfa=rfa,
        manifest=_Manifest(set()),
        attachment_manifest=_AttManifest(set()),
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_PACKAGE_INCOMPLETE
    assert r.missing_attachments == ("sf424.pdf",)


def test_missing_both_fails_with_aggregated_detail() -> None:
    rfa = _Rfa(
        section_structure=(_Section("narrative"),),
        required_attachments=("sf424.pdf",),
    )
    r = check_uploader_package_incomplete(
        rfa=rfa,
        manifest=_Manifest(set()),
        attachment_manifest=_AttManifest(set()),
    )
    assert r.success is False
    assert "narrative" in r.detail
    assert "sf424.pdf" in r.detail


def test_empty_rfa_passes_vacuously() -> None:
    rfa = _Rfa(section_structure=(), required_attachments=())
    r = check_uploader_package_incomplete(
        rfa=rfa,
        manifest=_Manifest(set()),
        attachment_manifest=_AttManifest(set()),
    )
    assert r.success is True
