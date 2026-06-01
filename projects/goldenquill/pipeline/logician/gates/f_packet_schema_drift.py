"""F-PACKET-SCHEMA-DRIFT — PRE-load gate. [§4 v2.x.y.1 row 11, LIVE]

OQ-5a tolerant-reader pattern at v0.2 first wave: returns ADVISORY
(GateOutcome.PASS with detail field carrying advisory message) when
packet.schema_version major exceeds consumer's known max. v1.x flips to
fail-closed.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.11
    - section_16_reflection_packet.md §16.6 (OQ-5a tolerant-reader)
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final, Optional


F_PACKET_SCHEMA_DRIFT: Final[str] = "F-PACKET-SCHEMA-DRIFT"

_SEMVER_RE: Final[re.Pattern[str]] = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


@dataclass(frozen=True, kw_only=True)
class SchemaDriftResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    advisory_only: bool = False
    sub_tag: Optional[str] = None


def check_f_packet_schema_drift(
    *,
    packet_schema_version: str,
    consumer_known_max: str = "1.1.0",
) -> SchemaDriftResult:
    """PRE-load: advisory at v0.2 if packet major exceeds consumer max."""
    if not isinstance(packet_schema_version, str):
        return SchemaDriftResult(
            success=False,
            failure_code=F_PACKET_SCHEMA_DRIFT,
            detail=(
                f"packet_schema_version must be str, got "
                f"{type(packet_schema_version).__name__}"
            ),
        )
    pkt_m = _SEMVER_RE.match(packet_schema_version)
    cons_m = _SEMVER_RE.match(consumer_known_max)
    if pkt_m is None:
        return SchemaDriftResult(
            success=False,
            failure_code=F_PACKET_SCHEMA_DRIFT,
            sub_tag="unknown_schema_version",
            detail=f"packet_schema_version {packet_schema_version!r} not semver",
        )
    if cons_m is None:
        return SchemaDriftResult(
            success=False,
            failure_code=F_PACKET_SCHEMA_DRIFT,
            detail=f"consumer_known_max {consumer_known_max!r} not semver",
        )
    pkt_major = int(pkt_m.group(1))
    cons_major = int(cons_m.group(1))
    if pkt_major > cons_major:
        # v0.2 first wave: ADVISORY only (tolerant-reader per OQ-5a)
        return SchemaDriftResult(
            success=True,
            failure_code=None,
            detail=(
                f"ADVISORY (v0.2 tolerant-reader per OQ-5a): "
                f"packet_schema_version {packet_schema_version!r} major "
                f"exceeds consumer_known_max {consumer_known_max!r}; "
                "v1.x flips this to fail-closed"
            ),
            advisory_only=True,
            sub_tag="unknown_schema_version",
        )
    return SchemaDriftResult(
        success=True,
        failure_code=None,
        detail=(
            f"packet_schema_version {packet_schema_version!r} compatible "
            f"with consumer_known_max {consumer_known_max!r}"
        ),
    )


predicate_schema_drift = check_f_packet_schema_drift


__all__ = [
    "F_PACKET_SCHEMA_DRIFT",
    "SchemaDriftResult",
    "check_f_packet_schema_drift",
    "predicate_schema_drift",
]
