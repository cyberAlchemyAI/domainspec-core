"""F-UPLOADER-PACKAGE-INCOMPLETE — POST-gate.

Per Blueprint §12.9.1 + §4 v2.7 amendment. Fires after Uploader assembly,
before the staged package is surfaced to the operator.

Trigger
-------
Any RFA-required section has no corresponding document in the staged
``submission_manifest.yaml``, OR any RFA-required mandatory attachment has
no corresponding entry in the ``attachment_manifest.yaml``.

Fail-closed. Hard-block. Predicate is deterministic; zero LLM tokens; no
file I/O (operates over already-parsed manifest objects). Bypass: M13.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Protocol, runtime_checkable


F_UPLOADER_PACKAGE_INCOMPLETE: str = "F-UPLOADER-PACKAGE-INCOMPLETE"


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PackageIncompleteResult:
    """Result of F-UPLOADER-PACKAGE-INCOMPLETE check."""

    success: bool
    failure_code: Optional[str]
    missing_sections: tuple[str, ...]
    missing_attachments: tuple[str, ...]
    detail: str


# ---------------------------------------------------------------------------
# Injected protocols (duck-typed shapes per §12 contracts)
# ---------------------------------------------------------------------------


@runtime_checkable
class _SectionStructureItem(Protocol):
    section_name: str


@runtime_checkable
class _RfaRecord(Protocol):
    section_structure: Iterable[_SectionStructureItem]
    required_attachments: Iterable[str]


@runtime_checkable
class _SubmissionManifest(Protocol):
    def has_section(self, section_name: str) -> bool: ...


@runtime_checkable
class _AttachmentManifest(Protocol):
    def has_attachment(self, attachment_name: str) -> bool: ...


# ---------------------------------------------------------------------------
# Gate predicate
# ---------------------------------------------------------------------------


def check_uploader_package_incomplete(
    *,
    rfa: _RfaRecord,
    manifest: _SubmissionManifest,
    attachment_manifest: _AttachmentManifest,
) -> PackageIncompleteResult:
    """POST-gate: every RFA-required section + mandatory attachment present."""
    missing_sections = tuple(
        s.section_name
        for s in rfa.section_structure
        if not manifest.has_section(s.section_name)
    )
    missing_attachments = tuple(
        a
        for a in rfa.required_attachments
        if not attachment_manifest.has_attachment(a)
    )
    if missing_sections or missing_attachments:
        return PackageIncompleteResult(
            success=False,
            failure_code=F_UPLOADER_PACKAGE_INCOMPLETE,
            missing_sections=missing_sections,
            missing_attachments=missing_attachments,
            detail=(
                f"Missing sections: {list(missing_sections)}; "
                f"Missing attachments: {list(missing_attachments)}"
            ),
        )
    return PackageIncompleteResult(
        success=True,
        failure_code=None,
        missing_sections=(),
        missing_attachments=(),
        detail="all RFA-required sections and attachments present",
    )
