"""F-PACKET-CYCLE-ID-UNRESOLVABLE — PRE-emission gate. [§4 v2.x.y.1 row 16, LIVE]

packet.cycle_id MUST resolve to a cycle in Logfire export. Resolution = at
least one span in the cycle's trace tree carries
attribute.cycle_id == packet.cycle_id.

Composition with F-PACKET-CADENCE-VIOLATION: this predicate fires
PRE-emission; CADENCE-VIOLATION fires PRE-write. Both must pass for emission.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.16
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Iterable, Optional


F_PACKET_CYCLE_ID_UNRESOLVABLE: Final[str] = "F-PACKET-CYCLE-ID-UNRESOLVABLE"


@dataclass(frozen=True, kw_only=True)
class CycleIdUnresolvableResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_cycle_id_unresolvable(
    *,
    packet_cycle_id: str,
    known_cycle_ids: Iterable[str],
) -> CycleIdUnresolvableResult:
    """PRE-emission: packet.cycle_id appears in Logfire's known cycle set."""
    if not isinstance(packet_cycle_id, str) or not packet_cycle_id:
        return CycleIdUnresolvableResult(
            success=False,
            failure_code=F_PACKET_CYCLE_ID_UNRESOLVABLE,
            detail="packet_cycle_id empty",
        )
    if packet_cycle_id not in set(known_cycle_ids):
        return CycleIdUnresolvableResult(
            success=False,
            failure_code=F_PACKET_CYCLE_ID_UNRESOLVABLE,
            sub_tag="cycle_id_not_in_logfire",
            detail=(
                f"packet.cycle_id {packet_cycle_id!r} does not resolve to "
                "any cycle in Logfire export"
            ),
        )
    return CycleIdUnresolvableResult(
        success=True,
        failure_code=None,
        detail=f"packet.cycle_id {packet_cycle_id!r} resolves in Logfire",
    )


predicate_cycle_id_unresolvable = check_f_packet_cycle_id_unresolvable


__all__ = [
    "F_PACKET_CYCLE_ID_UNRESOLVABLE",
    "CycleIdUnresolvableResult",
    "check_f_packet_cycle_id_unresolvable",
    "predicate_cycle_id_unresolvable",
]
