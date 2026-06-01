"""F-PACKET-CADENCE-VIOLATION — PRE-emission gate. [§4 v2.x.y.1 row 12, LIVE]

Two-axis defense:
  Axis A — cycle-close-marker resolution. cycle_close_marker_span_id MUST
  resolve to a span in Logfire export AND attribute event_type ==
  "cycle_close_marker" AND span belongs to packet.cycle_id.
  Axis B — packet_id collision per RT-13 fold-in. Pre-write check uses
  atomic POSIX O_CREAT | O_EXCL (operator-resolved OQ-3 2026-05-15).

Sub-tag ``.packet_id_collision`` per RT-13.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.12
    - section_16_reflection_packet.md §16.10.1 RT-13 fold-in
"""

from __future__ import annotations

import errno
import os
from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional


F_PACKET_CADENCE_VIOLATION: Final[str] = "F-PACKET-CADENCE-VIOLATION"


@dataclass(frozen=True, kw_only=True)
class CadenceViolationResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None
    colliding_path: Optional[str] = None


def check_f_packet_cadence_violation(
    *,
    packet_cycle_id: str,
    packet_cycle_close_marker_span_id: str,
    cycle_close_marker_spans: Mapping[str, Mapping[str, Any]],
) -> CadenceViolationResult:
    """Axis A: validate cycle-close marker resolution.

    ``cycle_close_marker_spans`` maps span_id → span attributes
    (e.g., {"event_type": "cycle_close_marker", "cycle_id": "cyc-001"}).
    """
    span_attrs = cycle_close_marker_spans.get(packet_cycle_close_marker_span_id)
    if span_attrs is None:
        return CadenceViolationResult(
            success=False,
            failure_code=F_PACKET_CADENCE_VIOLATION,
            sub_tag="no_cycle_close_marker",
            detail=(
                f"packet.cycle_close_marker_span_id "
                f"{packet_cycle_close_marker_span_id!r} not in Logfire export"
            ),
        )
    if span_attrs.get("event_type") != "cycle_close_marker":
        return CadenceViolationResult(
            success=False,
            failure_code=F_PACKET_CADENCE_VIOLATION,
            sub_tag="no_cycle_close_marker",
            detail=(
                f"span {packet_cycle_close_marker_span_id!r} event_type "
                f"{span_attrs.get('event_type')!r} != 'cycle_close_marker'"
            ),
        )
    span_cycle = span_attrs.get("cycle_id")
    if span_cycle != packet_cycle_id:
        return CadenceViolationResult(
            success=False,
            failure_code=F_PACKET_CADENCE_VIOLATION,
            sub_tag="no_cycle_close_marker",
            detail=(
                f"span cycle_id {span_cycle!r} != packet.cycle_id "
                f"{packet_cycle_id!r}"
            ),
        )
    return CadenceViolationResult(
        success=True,
        failure_code=None,
        detail="cycle-close-marker resolved + cycle match confirmed",
    )


def atomic_create_or_collision(*, target_path: str) -> CadenceViolationResult:
    """Axis B: atomic POSIX O_CREAT | O_EXCL collision detect per RT-13.

    Closes target_path immediately (caller writes through the SUB_KIND_REGISTRY
    write path; this is a defense-in-depth pre-write atomic existence check).
    On EEXIST → fail-closed sub-tag .packet_id_collision.
    """
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        fd = os.open(target_path, flags, mode=0o600)
        os.close(fd)
        # Remove the empty file we just created — real write happens via
        # vault_write dispatch; this fn is the existence-precheck only.
        try:
            os.unlink(target_path)
        except FileNotFoundError:
            pass
        return CadenceViolationResult(
            success=True,
            failure_code=None,
            detail=f"target path {target_path!r} did not exist (atomic create OK)",
        )
    except FileExistsError:
        return CadenceViolationResult(
            success=False,
            failure_code=F_PACKET_CADENCE_VIOLATION,
            sub_tag="packet_id_collision",
            detail=f"packet path {target_path!r} already exists (RT-13)",
            colliding_path=target_path,
        )
    except OSError as e:
        if e.errno == errno.EEXIST:
            return CadenceViolationResult(
                success=False,
                failure_code=F_PACKET_CADENCE_VIOLATION,
                sub_tag="packet_id_collision",
                detail=f"packet path {target_path!r} already exists (RT-13)",
                colliding_path=target_path,
            )
        return CadenceViolationResult(
            success=False,
            failure_code=F_PACKET_CADENCE_VIOLATION,
            detail=f"OS error during atomic create: {e!r}",
        )


predicate_cadence_violation = check_f_packet_cadence_violation


__all__ = [
    "F_PACKET_CADENCE_VIOLATION",
    "CadenceViolationResult",
    "check_f_packet_cadence_violation",
    "atomic_create_or_collision",
    "predicate_cadence_violation",
]
