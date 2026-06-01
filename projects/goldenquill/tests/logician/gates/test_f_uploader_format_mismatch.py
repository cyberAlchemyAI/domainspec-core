"""Unit tests for F-UPLOADER-FORMAT-MISMATCH (POST-18).

Per Blueprint §12.9.2 + §4 v2.7 amendment.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pipeline.logician.gates.f_uploader_format_mismatch import (
    F_UPLOADER_FORMAT_MISMATCH,
    check_uploader_format_mismatch,
)


@dataclass(frozen=True)
class _Entry:
    file_name: str
    format: str
    page_count: Optional[int]
    file_size_bytes: int
    portal_section: Optional[str]


@dataclass(frozen=True)
class _Manifest:
    entries: tuple


class _Adapter:
    def __init__(
        self,
        *,
        formats: dict[Optional[str], Optional[str]] | None = None,
        pages: dict[Optional[str], Optional[int]] | None = None,
        sizes: dict[Optional[str], Optional[int]] | None = None,
    ) -> None:
        self._formats = formats or {}
        self._pages = pages or {}
        self._sizes = sizes or {}

    def required_format(self, portal_section: Optional[str]) -> Optional[str]:
        return self._formats.get(portal_section)

    def page_limit(self, portal_section: Optional[str]) -> Optional[int]:
        return self._pages.get(portal_section)

    def file_size_limit(self, portal_section: Optional[str]) -> Optional[int]:
        return self._sizes.get(portal_section)


def test_failure_code_constant() -> None:
    assert F_UPLOADER_FORMAT_MISMATCH == "F-UPLOADER-FORMAT-MISMATCH"


def test_all_constraints_satisfied_passes() -> None:
    manifest = _Manifest(
        entries=(
            _Entry(
                file_name="narrative.pdf",
                format="pdf",
                page_count=10,
                file_size_bytes=1_000_000,
                portal_section="narrative",
            ),
        )
    )
    adapter = _Adapter(
        formats={"narrative": "pdf"},
        pages={"narrative": 15},
        sizes={"narrative": 5_000_000},
    )
    r = check_uploader_format_mismatch(adapter=adapter, manifest=manifest)
    assert r.success is True
    assert r.failure_code is None
    assert r.mismatches == ()


def test_wrong_format_fails() -> None:
    manifest = _Manifest(
        entries=(
            _Entry(
                file_name="narrative.docx",
                format="docx",
                page_count=10,
                file_size_bytes=1_000,
                portal_section="narrative",
            ),
        )
    )
    adapter = _Adapter(formats={"narrative": "pdf"})
    r = check_uploader_format_mismatch(adapter=adapter, manifest=manifest)
    assert r.success is False
    assert r.failure_code == F_UPLOADER_FORMAT_MISMATCH
    assert any("narrative.docx" in m for m in r.mismatches)


def test_page_limit_exceeded_fails() -> None:
    manifest = _Manifest(
        entries=(
            _Entry(
                file_name="long.pdf",
                format="pdf",
                page_count=20,
                file_size_bytes=1,
                portal_section="narrative",
            ),
        )
    )
    adapter = _Adapter(formats={"narrative": "pdf"}, pages={"narrative": 15})
    r = check_uploader_format_mismatch(adapter=adapter, manifest=manifest)
    assert r.success is False
    assert any("20 pages" in m for m in r.mismatches)


def test_file_size_exceeded_fails() -> None:
    manifest = _Manifest(
        entries=(
            _Entry(
                file_name="big.pdf",
                format="pdf",
                page_count=1,
                file_size_bytes=10_000_000,
                portal_section="narrative",
            ),
        )
    )
    adapter = _Adapter(
        formats={"narrative": "pdf"}, sizes={"narrative": 5_000_000}
    )
    r = check_uploader_format_mismatch(adapter=adapter, manifest=manifest)
    assert r.success is False
    assert any("10000000 bytes" in m for m in r.mismatches)


def test_no_constraints_set_passes() -> None:
    """When adapter sets no limits for the section, anything passes."""
    manifest = _Manifest(
        entries=(
            _Entry(
                file_name="a.pdf",
                format="pdf",
                page_count=999,
                file_size_bytes=999_999_999,
                portal_section="anything",
            ),
        )
    )
    adapter = _Adapter()
    r = check_uploader_format_mismatch(adapter=adapter, manifest=manifest)
    assert r.success is True


def test_multiple_mismatches_aggregated() -> None:
    manifest = _Manifest(
        entries=(
            _Entry(
                file_name="a.docx",
                format="docx",
                page_count=20,
                file_size_bytes=10_000,
                portal_section="narrative",
            ),
        )
    )
    adapter = _Adapter(
        formats={"narrative": "pdf"},
        pages={"narrative": 15},
        sizes={"narrative": 1_000},
    )
    r = check_uploader_format_mismatch(adapter=adapter, manifest=manifest)
    assert r.success is False
    # All three mismatch types fired
    assert len(r.mismatches) == 3
