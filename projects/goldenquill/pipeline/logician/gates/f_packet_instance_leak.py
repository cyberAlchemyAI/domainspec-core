"""F-PACKET-INSTANCE-LEAK — PRE-emission gate. [§4 v2.x.y.1 row 1, LIVE at v0.2]

Three-layer detection per §15.9.2 RT-07 precedent:
  1. NFKC normalization (closes homoglyph + ZWJ + RTL-override at canonicalization)
  2. Signed entity-name blocklist scan (deterministic; v0.2 = regex over operator-
     signed YAML; v1.x may upgrade to spaCy / local NER)
  3. Static regex closed-set (SSN, award-specific dollar formats, known
     instance patterns)

Fail-closed iff any layer surfaces a match. Sub-tags:
``.client_name_present``, ``.funder_specific_with_client``,
``.ner_entity_match``, ``.unicode_homoglyph``, ``.zwj_obfuscation``.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.1
    - section_16_reflection_packet.md §16.2.3 invariant 9
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Final, Iterable, Optional


F_PACKET_INSTANCE_LEAK: Final[str] = "F-PACKET-INSTANCE-LEAK"

# Layer 3 static regex — closed-set instance markers
_SSN_RE: Final[re.Pattern[str]] = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_DOLLAR_AMOUNT_RE: Final[re.Pattern[str]] = re.compile(
    r"\$\s?\d+(?:,\d{3})*(?:\.\d{2})?"
)
# ZWJ + RTL-override + bidi-control marks — surface even after NFKC since
# these are control chars not always normalized away
_ZERO_WIDTH_RE: Final[re.Pattern[str]] = re.compile(
    r"[​-‏‪-‮⁠-⁤]"
)


@dataclass(frozen=True, kw_only=True)
class InstanceLeakResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def _nfkc(text: str) -> str:
    return unicodedata.normalize("NFKC", text)


def check_f_packet_instance_leak(
    *,
    texts: Iterable[str],
    entity_blocklist: frozenset[str] = frozenset(),
) -> InstanceLeakResult:
    """PRE-emission: every ``texts`` element passes three-layer detection.

    ``entity_blocklist`` is the operator-signed closed set of instance-level
    entity names (client names, funder-specific identifiers); at v0.2 the
    blocklist is loaded from
    ``vault_shared/reflection_packet/instance_blocklist.signed.yaml`` after
    signature verification. Empty default is admissible (no entities pinned).
    """
    for raw in texts:
        if not isinstance(raw, str):
            return InstanceLeakResult(
                success=False,
                failure_code=F_PACKET_INSTANCE_LEAK,
                detail=f"text element is non-str: {type(raw).__name__}",
            )
        # Layer 1 — NFKC normalize
        normalized = _nfkc(raw)
        # ZWJ / RTL guard fires on the RAW text (not normalized) since these
        # marks may be the carrier of the obfuscation
        zwj_match = _ZERO_WIDTH_RE.search(raw)
        if zwj_match is not None:
            return InstanceLeakResult(
                success=False,
                failure_code=F_PACKET_INSTANCE_LEAK,
                sub_tag="zwj_obfuscation",
                detail=(
                    f"zero-width / bidi control char detected at offset "
                    f"{zwj_match.start()}"
                ),
            )
        # Detect homoglyphs by checking if NFKC normalization changed the text
        if normalized != raw and any(
            ord(c) > 127 for c in raw
        ):
            # Homoglyph (e.g., Cyrillic 'а' → Latin 'a' after NFKC) suspicious
            # only if the raw contained non-ASCII that NFKC altered
            return InstanceLeakResult(
                success=False,
                failure_code=F_PACKET_INSTANCE_LEAK,
                sub_tag="unicode_homoglyph",
                detail=(
                    f"NFKC normalization altered non-ASCII content; "
                    f"possible homoglyph"
                ),
            )
        # Layer 2 — signed entity blocklist (case-insensitive substring)
        normalized_lower = normalized.lower()
        for entity in entity_blocklist:
            if not isinstance(entity, str):
                continue
            if entity.lower() in normalized_lower:
                return InstanceLeakResult(
                    success=False,
                    failure_code=F_PACKET_INSTANCE_LEAK,
                    sub_tag="ner_entity_match",
                    detail=f"blocklisted entity {entity!r} detected",
                )
        # Layer 3 — static regex
        if _SSN_RE.search(normalized):
            return InstanceLeakResult(
                success=False,
                failure_code=F_PACKET_INSTANCE_LEAK,
                sub_tag="client_name_present",
                detail="SSN-shaped pattern detected",
            )
        if _DOLLAR_AMOUNT_RE.search(normalized):
            return InstanceLeakResult(
                success=False,
                failure_code=F_PACKET_INSTANCE_LEAK,
                sub_tag="funder_specific_with_client",
                detail="instance-level dollar amount detected",
            )
    return InstanceLeakResult(
        success=True,
        failure_code=None,
        detail="three-layer instance-leak scan clean",
    )


# Legacy name preserved for v0.1-hook test scaffold compatibility
predicate_instance_leak = check_f_packet_instance_leak


__all__ = [
    "F_PACKET_INSTANCE_LEAK",
    "InstanceLeakResult",
    "check_f_packet_instance_leak",
    "predicate_instance_leak",
]
