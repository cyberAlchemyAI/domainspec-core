"""``photos`` sub-kind — binary media metadata records. [§2.11.3, §2.13]

Schema, canonical-bytes encode/decode, and intent constant for photo
metadata. The binary blob is callable-managed at v7.2 (a v7.3 spin can
promote ``(metadata, blob)`` to a compound transaction if atomicity becomes
a felt need); the on-disk record file is the metadata wrapper that points
at the blob via ``blob_relative_path``.

Severity YELLOW. Photos may carry geolocation EXIF and faces — both are
admin-risk surfaces the operator must classify.

Blueprint authority:
    - section_02_v7_2_amendment.md §2.11.3 (schema)
    - section_02_v7_2_amendment.md §2.13 (POST_GATE_ALLOWLIST row)
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final, Optional

from pipeline.vault.sub_kinds._canonical import (
    from_canonical_json_bytes,
    to_canonical_json_bytes,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_v7_2_amendment.md": {
        "version": "v7.2-DRAFT",
        "sections_implemented": [
            "§2.11.3 PhotoRecord schema",
            "§2.13 operational-photos-write allowlist row",
        ],
    },
}

INTENT: Final[str] = "operational-photos-write"
SUB_KIND: Final[str] = "photos"
VAULT_SUBTREE: Final[str] = "operational/photos/"
ADMIN_RISK_SEVERITY: Final[str] = "YELLOW"

_HASH_RE: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{128}$")
_MIME_RE: Final[re.Pattern[str]] = re.compile(r"^image/[a-z0-9.+-]+$")


@dataclass(frozen=True, kw_only=True)
class PhotoRecord:
    """Photo metadata. Blob lives at ``operational/photos/blobs/<blob_relative_path>``."""

    record_id: str
    blob_relative_path: str
    content_hash: str
    mime_type: str
    captured_at: str
    caption: str
    geo_lat: Optional[float]
    geo_lon: Optional[float]

    def __post_init__(self) -> None:
        if not isinstance(self.record_id, str) or not self.record_id:
            raise ValueError("record_id must be a non-empty string")
        if not isinstance(self.blob_relative_path, str) or not self.blob_relative_path:
            raise ValueError("blob_relative_path must be a non-empty string")
        if not isinstance(self.content_hash, str) or not _HASH_RE.match(self.content_hash):
            raise ValueError(
                "content_hash must be 128 lowercase hex chars (SHA-3-512)"
            )
        if not isinstance(self.mime_type, str) or not _MIME_RE.match(self.mime_type):
            raise ValueError("mime_type must match ^image/[a-z0-9.+-]+$")
        if not isinstance(self.captured_at, str) or not self.captured_at.endswith("Z"):
            raise ValueError("captured_at must be a UTC ISO-8601 string ending in 'Z'")
        if not isinstance(self.caption, str):
            raise ValueError("caption must be a string (may be empty)")
        # geo: both-None or both-set
        lat_set = self.geo_lat is not None
        lon_set = self.geo_lon is not None
        if lat_set != lon_set:
            raise ValueError("(geo_lat, geo_lon) must be both-None or both-set")
        if lat_set:
            if not isinstance(self.geo_lat, (int, float)) or isinstance(
                self.geo_lat, bool
            ):
                raise ValueError("geo_lat must be a number when set")
            if not isinstance(self.geo_lon, (int, float)) or isinstance(
                self.geo_lon, bool
            ):
                raise ValueError("geo_lon must be a number when set")
            if not -90.0 <= float(self.geo_lat) <= 90.0:
                raise ValueError("geo_lat must be between -90 and 90")
            if not -180.0 <= float(self.geo_lon) <= 180.0:
                raise ValueError("geo_lon must be between -180 and 180")


def to_canonical_bytes(record: PhotoRecord) -> bytes:
    if not isinstance(record, PhotoRecord):
        raise TypeError(
            f"record must be PhotoRecord, got {type(record).__name__}"
        )
    return to_canonical_json_bytes(record)


def from_canonical_bytes(payload: bytes) -> PhotoRecord:
    parsed = from_canonical_json_bytes(payload)
    raw_lat = parsed.get("geo_lat")
    raw_lon = parsed.get("geo_lon")
    return PhotoRecord(
        record_id=str(parsed["record_id"]),
        blob_relative_path=str(parsed["blob_relative_path"]),
        content_hash=str(parsed["content_hash"]),
        mime_type=str(parsed["mime_type"]),
        captured_at=str(parsed["captured_at"]),
        caption=str(parsed["caption"]),
        geo_lat=float(raw_lat) if raw_lat is not None else None,
        geo_lon=float(raw_lon) if raw_lon is not None else None,
    )


def record_id_for(record: PhotoRecord) -> str:
    return record.record_id


__all__ = [
    "ADMIN_RISK_SEVERITY",
    "BLUEPRINT_DEPS",
    "INTENT",
    "PhotoRecord",
    "SUB_KIND",
    "VAULT_SUBTREE",
    "from_canonical_bytes",
    "record_id_for",
    "to_canonical_bytes",
]
