"""F-PACKET-PRODUCER-UNAUTHORIZED — PRE-emission gate. [§4 v2.x.y.1 row 18, LIVE]

Closed-set membership check. v0.2 producer registry =
``frozenset({"archivist.reflection_submode"})``. Schema-layer invariant 7
enforces at construction; predicate body is the runtime failure-code surface.

Forward-extension marker: if v1.x adds new producers (Cultivator Stage 2),
the registry extends additively.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.18
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional


F_PACKET_PRODUCER_UNAUTHORIZED: Final[str] = "F-PACKET-PRODUCER-UNAUTHORIZED"

_PRODUCER_REGISTRY_V0_2: Final[frozenset[str]] = frozenset(
    {"archivist.reflection_submode"}
)


@dataclass(frozen=True, kw_only=True)
class ProducerUnauthorizedResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_producer_unauthorized(
    *,
    packet_emitted_by_seat: str,
    producer_registry: frozenset[str] = _PRODUCER_REGISTRY_V0_2,
) -> ProducerUnauthorizedResult:
    """PRE-emission: emitted_by_seat in producer_registry closed set."""
    if not isinstance(packet_emitted_by_seat, str) or not packet_emitted_by_seat:
        return ProducerUnauthorizedResult(
            success=False,
            failure_code=F_PACKET_PRODUCER_UNAUTHORIZED,
            detail="packet_emitted_by_seat empty",
        )
    if packet_emitted_by_seat not in producer_registry:
        return ProducerUnauthorizedResult(
            success=False,
            failure_code=F_PACKET_PRODUCER_UNAUTHORIZED,
            sub_tag="seat_not_in_registry",
            detail=(
                f"emitted_by_seat {packet_emitted_by_seat!r} not in "
                f"producer registry {sorted(producer_registry)!r}"
            ),
        )
    return ProducerUnauthorizedResult(
        success=True,
        failure_code=None,
        detail=(
            f"emitted_by_seat {packet_emitted_by_seat!r} in producer registry"
        ),
    )


predicate_producer_unauthorized = check_f_packet_producer_unauthorized


__all__ = [
    "F_PACKET_PRODUCER_UNAUTHORIZED",
    "_PRODUCER_REGISTRY_V0_2",
    "ProducerUnauthorizedResult",
    "check_f_packet_producer_unauthorized",
    "predicate_producer_unauthorized",
]
