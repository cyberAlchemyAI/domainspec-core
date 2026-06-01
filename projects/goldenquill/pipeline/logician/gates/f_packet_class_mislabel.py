"""F-PACKET-CLASS-MISLABEL — PRE-emission gate. [§4 v2.x.y.1 row 5, LIVE]

packet.classification_register_version (128-hex SHA3-512) MUST match the
operator-signed classification register's hash at cycle start. Mid-cycle
relabeling attack (MINJA-shaped) closed at this predicate.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.5
"""

from __future__ import annotations

import hmac
from dataclasses import dataclass
from typing import Final, Optional


F_PACKET_CLASS_MISLABEL: Final[str] = "F-PACKET-CLASS-MISLABEL"


@dataclass(frozen=True, kw_only=True)
class ClassMislabelResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_class_mislabel(
    *,
    packet_classification_register_version: str,
    register_at_cycle_start_hash: str,
) -> ClassMislabelResult:
    """PRE-emission: constant-time match of packet field vs cycle-start hash."""
    if (
        not isinstance(packet_classification_register_version, str)
        or not packet_classification_register_version
    ):
        return ClassMislabelResult(
            success=False,
            failure_code=F_PACKET_CLASS_MISLABEL,
            detail="packet_classification_register_version empty",
        )
    if (
        not isinstance(register_at_cycle_start_hash, str)
        or not register_at_cycle_start_hash
    ):
        return ClassMislabelResult(
            success=False,
            failure_code=F_PACKET_CLASS_MISLABEL,
            detail="register_at_cycle_start_hash empty",
        )
    # Constant-time compare per v7.0.4-M1 §6
    if not hmac.compare_digest(
        packet_classification_register_version.lower(),
        register_at_cycle_start_hash.lower(),
    ):
        return ClassMislabelResult(
            success=False,
            failure_code=F_PACKET_CLASS_MISLABEL,
            sub_tag="register_version_drift",
            detail=(
                "packet.classification_register_version does not match "
                "operator-signed classification register hash at cycle "
                "start; MINJA-shaped mid-cycle relabel guard fires"
            ),
        )
    return ClassMislabelResult(
        success=True,
        failure_code=None,
        detail="classification register version matches cycle-start hash",
    )


predicate_class_mislabel = check_f_packet_class_mislabel


__all__ = [
    "F_PACKET_CLASS_MISLABEL",
    "ClassMislabelResult",
    "check_f_packet_class_mislabel",
    "predicate_class_mislabel",
]
