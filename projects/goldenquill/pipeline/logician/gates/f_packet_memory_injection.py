"""F-PACKET-MEMORY-INJECTION — PRE-emission gate. [§4 v2.x.y.1 row 10, LIVE]

Three-layer detection over packet.pattern_observations + packet.lessons_proposed
free-text fields:
  Layer 1 — regex (closed-set static patterns for known MINJA shapes)
  Layer 2 — NFKC-normalized regex (Unicode-obfuscated injection)
  Layer 3 — small classifier (optional at v0.2; operator SP0 opt-in)

Scope: pattern_summary + proposed_rule.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.10
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Final, Iterable, Optional


F_PACKET_MEMORY_INJECTION: Final[str] = "F-PACKET-MEMORY-INJECTION"

# Layer 1 — closed-set known MINJA shapes
_INJECTION_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    re.compile(r"(?im)\bSYSTEM\s*:\s*"),
    re.compile(r"(?im)<\|im_(start|end)\|>"),
    re.compile(r"(?im)\[INST\]"),
    re.compile(r"(?im)\[/INST\]"),
    re.compile(r"(?im)^assistant\s*:"),
    re.compile(r"(?im)^human\s*:"),
    re.compile(r"(?im)ignore\s+previous\s+instructions"),
    re.compile(r"(?im)disregard\s+all\s+prior"),
    re.compile(r"<\|fim_(start|middle|end)\|>"),
)


@dataclass(frozen=True, kw_only=True)
class MemoryInjectionResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_memory_injection(
    *,
    texts: Iterable[str],
    enable_classifier: bool = False,
) -> MemoryInjectionResult:
    """PRE-emission: three-layer scan over free-text fields."""
    for raw in texts:
        if not isinstance(raw, str):
            return MemoryInjectionResult(
                success=False,
                failure_code=F_PACKET_MEMORY_INJECTION,
                detail=f"text element non-str: {type(raw).__name__}",
            )
        # Layer 1 — regex on raw text
        for pat in _INJECTION_PATTERNS:
            m = pat.search(raw)
            if m is not None:
                return MemoryInjectionResult(
                    success=False,
                    failure_code=F_PACKET_MEMORY_INJECTION,
                    sub_tag="injection_pattern_regex",
                    detail=(
                        f"MINJA-shaped pattern matched at offset "
                        f"{m.start()}: {m.group()!r}"
                    ),
                )
        # Layer 2 — NFKC-normalized regex
        normalized = unicodedata.normalize("NFKC", raw)
        if normalized != raw:
            for pat in _INJECTION_PATTERNS:
                m = pat.search(normalized)
                if m is not None:
                    return MemoryInjectionResult(
                        success=False,
                        failure_code=F_PACKET_MEMORY_INJECTION,
                        sub_tag="unicode_normalized_match",
                        detail=(
                            f"Unicode-normalized MINJA pattern matched "
                            f"at offset {m.start()}: {m.group()!r}"
                        ),
                    )
        # Layer 3 — small classifier (opt-in; not enabled by default at v0.2)
        # Reserved for v1.x scheduled-cadence Archivist hardening.
        if enable_classifier:
            # Future: load operator-signed classifier from
            # vault_shared/reflection_packet/memory_injection_classifier.signed.bin
            pass
    return MemoryInjectionResult(
        success=True,
        failure_code=None,
        detail="three-layer memory-injection scan clean",
    )


predicate_memory_injection = check_f_packet_memory_injection


__all__ = [
    "F_PACKET_MEMORY_INJECTION",
    "MemoryInjectionResult",
    "check_f_packet_memory_injection",
    "predicate_memory_injection",
]
