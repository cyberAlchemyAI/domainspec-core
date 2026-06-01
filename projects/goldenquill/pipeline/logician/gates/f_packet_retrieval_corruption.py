"""F-PACKET-RETRIEVAL-CORRUPTION — PRE-load gate. [§4 v2.x.y.1 row 9, LIVE]

PRE-load defense for Consumer C (v1.x scheduled-cadence Archivist). At v0.2
first wave the predicate body is LIVE but Consumer C runtime is deferred
to v1.x. Schema is forward-compatible.

Detection:
  - High-entropy burst: Shannon entropy > 7.5 bits/byte over 200-byte
    rolling window (cryptographic-payload smuggling).
  - Optimized-trigger fingerprint: substring scan against operator-signed
    trigger fingerprint registry (AgentPoison + PoisonedRAG defense).

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.9
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Final, Iterable, Optional


F_PACKET_RETRIEVAL_CORRUPTION: Final[str] = "F-PACKET-RETRIEVAL-CORRUPTION"

_ENTROPY_THRESHOLD: Final[float] = 7.5
_WINDOW_SIZE: Final[int] = 200


def _shannon_entropy_bits_per_byte(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy


@dataclass(frozen=True, kw_only=True)
class RetrievalCorruptionResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_retrieval_corruption(
    *,
    packet_text_payload: bytes,
    trigger_fingerprints: Iterable[bytes] = (),
) -> RetrievalCorruptionResult:
    """PRE-load (Consumer C): entropy-burst + trigger-fingerprint scan."""
    if not isinstance(packet_text_payload, bytes):
        return RetrievalCorruptionResult(
            success=False,
            failure_code=F_PACKET_RETRIEVAL_CORRUPTION,
            detail=(
                f"packet_text_payload must be bytes, got "
                f"{type(packet_text_payload).__name__}"
            ),
        )
    # Rolling-window entropy scan
    if len(packet_text_payload) >= _WINDOW_SIZE:
        for start in range(0, len(packet_text_payload) - _WINDOW_SIZE + 1, _WINDOW_SIZE // 4):
            window = packet_text_payload[start : start + _WINDOW_SIZE]
            ent = _shannon_entropy_bits_per_byte(window)
            if ent > _ENTROPY_THRESHOLD:
                return RetrievalCorruptionResult(
                    success=False,
                    failure_code=F_PACKET_RETRIEVAL_CORRUPTION,
                    sub_tag="high_entropy_burst",
                    detail=(
                        f"window starting at offset {start} entropy "
                        f"{ent:.2f} > threshold {_ENTROPY_THRESHOLD}"
                    ),
                )
    # Trigger-fingerprint substring scan
    for fp in trigger_fingerprints:
        if not isinstance(fp, bytes) or not fp:
            continue
        if fp in packet_text_payload:
            return RetrievalCorruptionResult(
                success=False,
                failure_code=F_PACKET_RETRIEVAL_CORRUPTION,
                sub_tag="optimized_trigger_match",
                detail=f"trigger fingerprint matched (len {len(fp)})",
            )
    return RetrievalCorruptionResult(
        success=True,
        failure_code=None,
        detail="entropy-burst + trigger-fingerprint scan clean",
    )


predicate_retrieval_corruption = check_f_packet_retrieval_corruption


__all__ = [
    "F_PACKET_RETRIEVAL_CORRUPTION",
    "RetrievalCorruptionResult",
    "check_f_packet_retrieval_corruption",
    "predicate_retrieval_corruption",
]
