"""``narrative_entries`` sub-kind — free-form journal records. [§2.11.4, §2.13]

Schema, canonical-bytes encode/decode, and intent constant for free-form
narrative entries (operator field notes, sub-awardee narrative responses).

Severity YELLOW. Free-form text may surface PII; the operator's
classification register (per architecture v7.0.7 LOCKED) governs routing
decisions for downstream agents that touch these records.

Blueprint authority:
    - section_02_v7_2_amendment.md §2.11.4 (schema)
    - section_02_v7_2_amendment.md §2.13 (POST_GATE_ALLOWLIST row)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from pipeline.vault.sub_kinds._canonical import (
    _coerce_str_tuple,
    from_canonical_json_bytes,
    to_canonical_json_bytes,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_v7_2_amendment.md": {
        "version": "v7.2-DRAFT",
        "sections_implemented": [
            "§2.11.4 NarrativeEntry schema",
            "§2.13 operational-narrative-write allowlist row",
        ],
    },
}

INTENT: Final[str] = "operational-narrative-write"
SUB_KIND: Final[str] = "narrative_entries"
VAULT_SUBTREE: Final[str] = "operational/narratives/"
ADMIN_RISK_SEVERITY: Final[str] = "YELLOW"


@dataclass(frozen=True, kw_only=True)
class NarrativeEntry:
    """One free-form narrative entry."""

    record_id: str
    authored_at: str
    author: str
    body: str
    tags: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.record_id, str) or not self.record_id:
            raise ValueError("record_id must be a non-empty string")
        if not isinstance(self.authored_at, str) or not self.authored_at.endswith("Z"):
            raise ValueError("authored_at must be a UTC ISO-8601 string ending in 'Z'")
        if not isinstance(self.author, str) or not self.author:
            raise ValueError("author must be a non-empty string")
        if not isinstance(self.body, str) or not self.body:
            raise ValueError("body must be a non-empty string")
        if not isinstance(self.tags, tuple):
            raise ValueError("tags must be a tuple of strings")
        for i, t in enumerate(self.tags):
            if not isinstance(t, str):
                raise ValueError(f"tags[{i}] must be str")


def to_canonical_bytes(record: NarrativeEntry) -> bytes:
    if not isinstance(record, NarrativeEntry):
        raise TypeError(
            f"record must be NarrativeEntry, got {type(record).__name__}"
        )
    return to_canonical_json_bytes(record)


def from_canonical_bytes(payload: bytes) -> NarrativeEntry:
    parsed = from_canonical_json_bytes(payload)
    return NarrativeEntry(
        record_id=str(parsed["record_id"]),
        authored_at=str(parsed["authored_at"]),
        author=str(parsed["author"]),
        body=str(parsed["body"]),
        tags=_coerce_str_tuple(parsed.get("tags", []), field="tags"),
    )


def record_id_for(record: NarrativeEntry) -> str:
    return record.record_id


__all__ = [
    "ADMIN_RISK_SEVERITY",
    "BLUEPRINT_DEPS",
    "INTENT",
    "NarrativeEntry",
    "SUB_KIND",
    "VAULT_SUBTREE",
    "from_canonical_bytes",
    "record_id_for",
    "to_canonical_bytes",
]
