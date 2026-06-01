"""``metrics`` sub-kind — numerical time-series records. [§2.11.1, §2.13]

Schema, canonical-bytes encode/decode, and intent constant for operational
metric readings (e.g. soil moisture, throughput, yield). Severity GREEN —
metric numbers do not carry PII unless the operator explicitly puts identity
in tags or source labels (which is operator-policy, not schema enforcement).

Blueprint authority:
    - section_02_v7_2_amendment.md §2.11.1 (schema)
    - section_02_v7_2_amendment.md §2.13 (POST_GATE_ALLOWLIST row)
    - section_02_v7_2_amendment.md §2 (sub-kind table — admin-risk severity)
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
            "§2.11.1 MetricsRecord schema",
            "§2.13 operational-metrics-write allowlist row",
            "§1 scope sub-kind table — admin-risk severity GREEN",
        ],
    },
}

INTENT: Final[str] = "operational-metrics-write"
SUB_KIND: Final[str] = "metrics"
VAULT_SUBTREE: Final[str] = "operational/metrics/"
ADMIN_RISK_SEVERITY: Final[str] = "GREEN"


@dataclass(frozen=True, kw_only=True)
class MetricsRecord:
    """One metric reading. Round-tripped through canonical JSON.

    All fields are required; tuple-typed ``tags`` is enforced so a JSON
    decode cannot smuggle a list past the equality round-trip.
    """

    record_id: str
    metric_name: str
    value: float
    unit: str
    captured_at: str
    source: str
    tags: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.record_id, str) or not self.record_id:
            raise ValueError("record_id must be a non-empty string")
        if not isinstance(self.metric_name, str) or not self.metric_name:
            raise ValueError("metric_name must be a non-empty string")
        if not isinstance(self.value, (int, float)) or isinstance(self.value, bool):
            raise ValueError("value must be a number")
        if not isinstance(self.unit, str) or not self.unit:
            raise ValueError("unit must be a non-empty string")
        if not isinstance(self.captured_at, str) or not self.captured_at.endswith("Z"):
            raise ValueError("captured_at must be a UTC ISO-8601 string ending in 'Z'")
        if not isinstance(self.source, str):
            raise ValueError("source must be a string")
        if not isinstance(self.tags, tuple):
            raise ValueError("tags must be a tuple of strings")
        for i, t in enumerate(self.tags):
            if not isinstance(t, str):
                raise ValueError(f"tags[{i}] must be str")


def to_canonical_bytes(record: MetricsRecord) -> bytes:
    """Encode ``record`` to canonical JSON bytes."""
    if not isinstance(record, MetricsRecord):
        raise TypeError(
            f"record must be MetricsRecord, got {type(record).__name__}"
        )
    return to_canonical_json_bytes(record)


def from_canonical_bytes(payload: bytes) -> MetricsRecord:
    """Decode canonical JSON bytes to a :class:`MetricsRecord`.

    :raises ValueError: payload is not a metrics record (schema invariants
        re-validate via ``__post_init__``).
    """
    parsed = from_canonical_json_bytes(payload)
    return MetricsRecord(
        record_id=str(parsed["record_id"]),
        metric_name=str(parsed["metric_name"]),
        value=float(parsed["value"]),
        unit=str(parsed["unit"]),
        captured_at=str(parsed["captured_at"]),
        source=str(parsed["source"]),
        tags=_coerce_str_tuple(parsed.get("tags", []), field="tags"),
    )


def record_id_for(record: MetricsRecord) -> str:
    """Filename stem for the record's on-disk file."""
    return record.record_id


__all__ = [
    "ADMIN_RISK_SEVERITY",
    "BLUEPRINT_DEPS",
    "INTENT",
    "MetricsRecord",
    "SUB_KIND",
    "VAULT_SUBTREE",
    "from_canonical_bytes",
    "record_id_for",
    "to_canonical_bytes",
]
