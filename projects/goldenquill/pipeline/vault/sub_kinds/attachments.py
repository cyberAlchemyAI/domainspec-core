"""``attachments`` sub-kind — file attachments for Uploader. [§2.11.7, §2.13]

Schema, canonical-bytes encode/decode, and intent constant for grant-cycle
attachments (PDFs, supporting docs, signed letters, photos packaged with
proposals).

Per WS-F coordination (dispatch plan §WS-H internal notes, recommendation
(a)): the schema lands at v7.2 with a concrete substrate; Uploader
consumption follows in §12 v1.1. The ``attached_to_grant_id`` field is the
foreign key Uploader will key into.

Severity YELLOW.

Blueprint authority:
    - section_02_v7_2_amendment.md §2.11.7 (schema)
    - section_02_v7_2_amendment.md §2.13 (POST_GATE_ALLOWLIST row)
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

from pipeline.vault.sub_kinds._canonical import (
    from_canonical_json_bytes,
    to_canonical_json_bytes,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_v7_2_amendment.md": {
        "version": "v7.2-DRAFT",
        "sections_implemented": [
            "§2.11.7 AttachmentRecord schema",
            "§2.13 operational-attachment-write allowlist row",
        ],
    },
}

INTENT: Final[str] = "operational-attachment-write"
SUB_KIND: Final[str] = "attachments"
VAULT_SUBTREE: Final[str] = "operational/attachments/"
ADMIN_RISK_SEVERITY: Final[str] = "YELLOW"

_HASH_RE: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{128}$")


@dataclass(frozen=True, kw_only=True)
class AttachmentRecord:
    """One attachment metadata record. Blob lives at
    ``operational/attachments/blobs/<blob_relative_path>`` (callable-managed)."""

    record_id: str
    filename: str
    mime_type: str
    content_hash: str
    size_bytes: int
    attached_to_grant_id: str
    proposal_section_anchor: str
    blob_relative_path: str

    def __post_init__(self) -> None:
        if not isinstance(self.record_id, str) or not self.record_id:
            raise ValueError("record_id must be a non-empty string")
        if not isinstance(self.filename, str) or not self.filename:
            raise ValueError("filename must be a non-empty string")
        if not isinstance(self.mime_type, str) or not self.mime_type:
            raise ValueError("mime_type must be a non-empty string")
        if not isinstance(self.content_hash, str) or not _HASH_RE.match(self.content_hash):
            raise ValueError(
                "content_hash must be 128 lowercase hex chars (SHA-3-512)"
            )
        if not isinstance(self.size_bytes, int) or isinstance(self.size_bytes, bool):
            raise ValueError("size_bytes must be int")
        if self.size_bytes < 0:
            raise ValueError("size_bytes must be >= 0")
        if not isinstance(self.attached_to_grant_id, str) or not self.attached_to_grant_id:
            raise ValueError("attached_to_grant_id must be a non-empty string")
        if not isinstance(self.proposal_section_anchor, str):
            raise ValueError("proposal_section_anchor must be a string")
        if not isinstance(self.blob_relative_path, str) or not self.blob_relative_path:
            raise ValueError("blob_relative_path must be a non-empty string")


def to_canonical_bytes(record: AttachmentRecord) -> bytes:
    if not isinstance(record, AttachmentRecord):
        raise TypeError(
            f"record must be AttachmentRecord, got {type(record).__name__}"
        )
    return to_canonical_json_bytes(record)


def from_canonical_bytes(payload: bytes) -> AttachmentRecord:
    parsed = from_canonical_json_bytes(payload)
    return AttachmentRecord(
        record_id=str(parsed["record_id"]),
        filename=str(parsed["filename"]),
        mime_type=str(parsed["mime_type"]),
        content_hash=str(parsed["content_hash"]),
        size_bytes=int(parsed["size_bytes"]),
        attached_to_grant_id=str(parsed["attached_to_grant_id"]),
        proposal_section_anchor=str(parsed["proposal_section_anchor"]),
        blob_relative_path=str(parsed["blob_relative_path"]),
    )


def record_id_for(record: AttachmentRecord) -> str:
    return record.record_id


__all__ = [
    "ADMIN_RISK_SEVERITY",
    "AttachmentRecord",
    "BLUEPRINT_DEPS",
    "INTENT",
    "SUB_KIND",
    "VAULT_SUBTREE",
    "from_canonical_bytes",
    "record_id_for",
    "to_canonical_bytes",
]
