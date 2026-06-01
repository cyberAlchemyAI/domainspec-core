"""F-UPLOADER-FORMAT-MISMATCH — POST-gate.

Per Blueprint §12.9.2 + §4 v2.7 amendment. Fires after Uploader format
conversion, before the package is surfaced to the operator.

Trigger
-------
For each entry in the staged manifest, the entry must satisfy:
  * file format equals portal-required format (when adapter specifies one),
  * page count is at or below portal page limit (when set),
  * file size is at or below portal file-size limit (when set).

Fail-closed. Hard-block. No file I/O — operates on already-staged manifest
entries with `format`, `page_count`, `file_size_bytes` already populated by
Uploader assembly. Bypass: M13.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Protocol, runtime_checkable


F_UPLOADER_FORMAT_MISMATCH: str = "F-UPLOADER-FORMAT-MISMATCH"


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class FormatMismatchResult:
    """Result of F-UPLOADER-FORMAT-MISMATCH check."""

    success: bool
    failure_code: Optional[str]
    mismatches: tuple[str, ...]
    detail: str


# ---------------------------------------------------------------------------
# Injected protocols
# ---------------------------------------------------------------------------


@runtime_checkable
class _ManifestEntry(Protocol):
    file_name: str
    format: str
    page_count: Optional[int]
    file_size_bytes: int
    portal_section: Optional[str]


@runtime_checkable
class _PortalAdapter(Protocol):
    def required_format(self, portal_section: Optional[str]) -> Optional[str]: ...
    def page_limit(self, portal_section: Optional[str]) -> Optional[int]: ...
    def file_size_limit(self, portal_section: Optional[str]) -> Optional[int]: ...


@runtime_checkable
class _ManifestSource(Protocol):
    entries: Iterable[_ManifestEntry]


# ---------------------------------------------------------------------------
# Gate predicate
# ---------------------------------------------------------------------------


def check_uploader_format_mismatch(
    *,
    adapter: _PortalAdapter,
    manifest: _ManifestSource,
) -> FormatMismatchResult:
    """POST-gate: every staged manifest entry satisfies portal constraints."""
    mismatches: list[str] = []
    for entry in manifest.entries:
        expected = adapter.required_format(entry.portal_section)
        if expected is not None and entry.format != expected:
            mismatches.append(
                f"{entry.file_name}: expected format {expected!r}, got {entry.format!r}"
            )
        page_limit = adapter.page_limit(entry.portal_section)
        if (
            page_limit is not None
            and entry.page_count is not None
            and entry.page_count > page_limit
        ):
            mismatches.append(
                f"{entry.file_name}: {entry.page_count} pages > limit {page_limit}"
            )
        size_limit = adapter.file_size_limit(entry.portal_section)
        if size_limit is not None and entry.file_size_bytes > size_limit:
            mismatches.append(
                f"{entry.file_name}: {entry.file_size_bytes} bytes > limit {size_limit}"
            )
    if mismatches:
        return FormatMismatchResult(
            success=False,
            failure_code=F_UPLOADER_FORMAT_MISMATCH,
            mismatches=tuple(mismatches),
            detail="; ".join(mismatches),
        )
    return FormatMismatchResult(
        success=True,
        failure_code=None,
        mismatches=(),
        detail="all staged entries satisfy portal format / page / size constraints",
    )
