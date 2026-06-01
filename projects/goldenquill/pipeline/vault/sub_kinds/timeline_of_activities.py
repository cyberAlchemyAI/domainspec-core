"""``timeline_of_activities`` sub-kind — event records. [§2.11.5, §2.13]

Schema, canonical-bytes encode/decode, and intent constant for time-bounded
activity records (workshops, site visits, deliverables, milestones).

Severity YELLOW. Participants are stored as opaque ids — the schema rejects
raw names so a downstream Cedar gate (e.g. for Report Generator export) can
treat the field as already-de-identified.

Blueprint authority:
    - section_02_v7_2_amendment.md §2.11.5 (schema)
    - section_02_v7_2_amendment.md §2.13 (POST_GATE_ALLOWLIST row)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from pipeline.vault.sub_kinds._canonical import (
    _coerce_str_tuple,
    from_canonical_json_bytes,
    to_canonical_json_bytes,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_v7_2_amendment.md": {
        "version": "v7.2-DRAFT",
        "sections_implemented": [
            "§2.11.5 TimelineActivity schema",
            "§2.13 operational-timeline-write allowlist row",
        ],
    },
}

INTENT: Final[str] = "operational-timeline-write"
SUB_KIND: Final[str] = "timeline_of_activities"
VAULT_SUBTREE: Final[str] = "operational/timeline/"
ADMIN_RISK_SEVERITY: Final[str] = "YELLOW"


@dataclass(frozen=True, kw_only=True)
class TimelineActivity:
    """One activity event."""

    record_id: str
    started_at: str
    ended_at: Optional[str]
    summary: str
    participants: tuple[str, ...]
    location: str
    outcome: str

    def __post_init__(self) -> None:
        if not isinstance(self.record_id, str) or not self.record_id:
            raise ValueError("record_id must be a non-empty string")
        if not isinstance(self.started_at, str) or not self.started_at.endswith("Z"):
            raise ValueError("started_at must be a UTC ISO-8601 string ending in 'Z'")
        if self.ended_at is not None:
            if not isinstance(self.ended_at, str) or not self.ended_at.endswith("Z"):
                raise ValueError("ended_at must be UTC ISO-8601 ending 'Z' or None")
            if self.ended_at <= self.started_at:
                raise ValueError("ended_at must be lexicographically > started_at")
        if not isinstance(self.summary, str) or not self.summary:
            raise ValueError("summary must be a non-empty string")
        if not isinstance(self.participants, tuple):
            raise ValueError("participants must be a tuple of opaque ids")
        for i, p in enumerate(self.participants):
            if not isinstance(p, str):
                raise ValueError(f"participants[{i}] must be str")
        if not isinstance(self.location, str):
            raise ValueError("location must be a string (may be empty)")
        if not isinstance(self.outcome, str):
            raise ValueError("outcome must be a string (may be empty)")


def to_canonical_bytes(record: TimelineActivity) -> bytes:
    if not isinstance(record, TimelineActivity):
        raise TypeError(
            f"record must be TimelineActivity, got {type(record).__name__}"
        )
    return to_canonical_json_bytes(record)


def from_canonical_bytes(payload: bytes) -> TimelineActivity:
    parsed = from_canonical_json_bytes(payload)
    raw_end = parsed.get("ended_at")
    return TimelineActivity(
        record_id=str(parsed["record_id"]),
        started_at=str(parsed["started_at"]),
        ended_at=str(raw_end) if raw_end is not None else None,
        summary=str(parsed["summary"]),
        participants=_coerce_str_tuple(
            parsed.get("participants", []), field="participants"
        ),
        location=str(parsed["location"]),
        outcome=str(parsed["outcome"]),
    )


def record_id_for(record: TimelineActivity) -> str:
    return record.record_id


__all__ = [
    "ADMIN_RISK_SEVERITY",
    "BLUEPRINT_DEPS",
    "INTENT",
    "SUB_KIND",
    "TimelineActivity",
    "VAULT_SUBTREE",
    "from_canonical_bytes",
    "record_id_for",
    "to_canonical_bytes",
]
