"""F-UPLOADER-ATTACHMENT-TAMPERED — PRE-gate.

Per Blueprint §12.9.5 + §4 v2.7 amendment. Attachment files must hash-match
their upload-time SHA3-512. A mismatch indicates the file was modified
between operator upload and Uploader assembly — hard-block.

No file I/O — assembly-time hashes are computed by the caller (§2 Vault
read primitive) and passed in as a `(file_path, sha3_512)` mapping. Bypass:
M13.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Optional, Protocol, runtime_checkable


F_UPLOADER_ATTACHMENT_TAMPERED: str = "F-UPLOADER-ATTACHMENT-TAMPERED"


@runtime_checkable
class _AttachmentRef(Protocol):
    file_path: str
    content_sha3_512: str


@dataclass(frozen=True, kw_only=True)
class AttachmentTamperedResult:
    """Result of F-UPLOADER-ATTACHMENT-TAMPERED check."""

    success: bool
    failure_code: Optional[str]
    tampered: tuple[str, ...]  # file paths whose hashes mismatched
    detail: str


def check_uploader_attachment_tampered(
    *,
    attachments: Iterable[_AttachmentRef],
    assembly_time_hashes: Mapping[str, str],
) -> AttachmentTamperedResult:
    """PRE-gate: every attachment's assembly-time hash matches upload-time."""
    tampered: list[str] = []
    for att in attachments:
        live = assembly_time_hashes.get(att.file_path)
        if live is None:
            # Missing hash entry is treated as tamper signal (the caller is
            # responsible for invoking F-UPLOADER-ATTACHMENT-MISSING first;
            # if that gate passed, the file exists and a hash should exist).
            tampered.append(att.file_path)
            continue
        if live != att.content_sha3_512:
            tampered.append(att.file_path)
    if tampered:
        return AttachmentTamperedResult(
            success=False,
            failure_code=F_UPLOADER_ATTACHMENT_TAMPERED,
            tampered=tuple(tampered),
            detail=(
                f"{len(tampered)} attachment(s) have hash mismatch vs upload-"
                f"time: {tampered}"
            ),
        )
    return AttachmentTamperedResult(
        success=True,
        failure_code=None,
        tampered=(),
        detail="all attachments hash-match upload-time",
    )
