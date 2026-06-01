"""F-UPLOADER-ATTACHMENT-MISSING — PRE-gate.

Per Blueprint §12.9.5 + §4 v2.7 amendment. Every `AttachmentRef.file_path`
must resolve to a file on disk. A missing file blocks Uploader assembly.

No direct file I/O — file existence is checked via an injected
`FileExistsCallable` per the §4 v2.2 _protocols.py pattern. Bypass: M13.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Protocol, runtime_checkable


F_UPLOADER_ATTACHMENT_MISSING: str = "F-UPLOADER-ATTACHMENT-MISSING"


@runtime_checkable
class _AttachmentRef(Protocol):
    file_path: str


@runtime_checkable
class FileExistsCallable(Protocol):
    """Returns True iff `file_path` resolves to a regular file on disk."""

    def __call__(self, file_path: str) -> bool: ...


@dataclass(frozen=True, kw_only=True)
class AttachmentMissingResult:
    """Result of F-UPLOADER-ATTACHMENT-MISSING check."""

    success: bool
    failure_code: Optional[str]
    missing: tuple[str, ...]
    detail: str


def check_uploader_attachment_missing(
    *,
    attachments: Iterable[_AttachmentRef],
    file_exists: FileExistsCallable,
) -> AttachmentMissingResult:
    """PRE-gate: every attachment file resolves on disk."""
    missing: list[str] = []
    for att in attachments:
        try:
            present = file_exists(att.file_path)
        except Exception as exc:
            # Fail-closed on reader exception
            return AttachmentMissingResult(
                success=False,
                failure_code=F_UPLOADER_ATTACHMENT_MISSING,
                missing=(att.file_path,),
                detail=f"file_exists reader raised on {att.file_path!r}: {exc!r}",
            )
        if not present:
            missing.append(att.file_path)
    if missing:
        return AttachmentMissingResult(
            success=False,
            failure_code=F_UPLOADER_ATTACHMENT_MISSING,
            missing=tuple(missing),
            detail=f"{len(missing)} attachment file(s) missing on disk: {missing}",
        )
    return AttachmentMissingResult(
        success=True,
        failure_code=None,
        missing=(),
        detail="all attachment files resolve on disk",
    )
