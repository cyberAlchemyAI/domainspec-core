"""F-PACKET-CLASS-SLOT-LEAK — PRE-emission gate. [§4 v2.x.y.1 row 4, LIVE]

Mirror of ``F-CLASS-SLOT-ID-NON-OPAQUE`` from v7.0.7 §5.1 byte-for-byte.
Semantic-slot regex applied to canonical-JSON bytes of any cloud-routable
field. Reflection Packet routing is always-local at v0.2, so firing this
predicate indicates a routing bug or attack — defense-in-depth.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.4
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final, Optional


F_PACKET_CLASS_SLOT_LEAK: Final[str] = "F-PACKET-CLASS-SLOT-LEAK"

# Mirrors v7.0.10 broadened regex pattern byte-for-byte
_SLOT_RE: Final[re.Pattern[bytes]] = re.compile(rb"\[SLOT_[^\]]*\]")


@dataclass(frozen=True, kw_only=True)
class ClassSlotLeakResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_class_slot_leak(
    *,
    packet_json_bytes: bytes,
) -> ClassSlotLeakResult:
    """PRE-emission: canonical-bytes carry no [SLOT_*] markers."""
    if not isinstance(packet_json_bytes, bytes):
        return ClassSlotLeakResult(
            success=False,
            failure_code=F_PACKET_CLASS_SLOT_LEAK,
            detail=(
                f"packet_json_bytes must be bytes, got "
                f"{type(packet_json_bytes).__name__}"
            ),
        )
    m = _SLOT_RE.search(packet_json_bytes)
    if m is not None:
        return ClassSlotLeakResult(
            success=False,
            failure_code=F_PACKET_CLASS_SLOT_LEAK,
            sub_tag="slot_id_in_canonical_bytes",
            detail=(
                f"[SLOT_*] marker detected in canonical bytes at offset "
                f"{m.start()}; v7.0.10 §1 deprecates opaque-slot tokens"
            ),
        )
    return ClassSlotLeakResult(
        success=True,
        failure_code=None,
        detail="canonical bytes contain no [SLOT_*] markers",
    )


predicate_class_slot_leak = check_f_packet_class_slot_leak


__all__ = [
    "F_PACKET_CLASS_SLOT_LEAK",
    "ClassSlotLeakResult",
    "check_f_packet_class_slot_leak",
    "predicate_class_slot_leak",
]
