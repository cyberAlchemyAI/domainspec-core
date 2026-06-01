"""F-CARDS-SIGNATURE-INVALID — Ed25519 verification of card canonical-bytes against pinned publisher pubkey failed.

Per blueprint §4 v2.x card-hardening §4.X.1.4. PRE-load production-only gate.

Predicate body graduates LIVE at v0.2 first wave per architecture v7.0.11 §5.
At v0.1 Beta LOCK this raises NotImplementedError as part of the dormant-
primitive shape (mirrors v7.0.7 §5.1 F-CLASS-* + v7.0.9 F-REFLECTION-* +
§16 v1 F-PACKET-* + §17 v1 §17.6 F-WPFA-* family precedents byte-for-byte).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal, Mapping


GATE_ID: Final[str] = "F-CARDS-SIGNATURE-INVALID"


@dataclass(frozen=True, kw_only=True)
class GateOutcome:
    passed: bool
    message: str


def evaluate(*, card_path: str, canonical_bytes: bytes, ed25519_signature_hex: str, publisher_pubkey: bytes) -> GateOutcome:
    """Evaluate the gate.

    DRAFT predicate body. Raises NotImplementedError until v0.2 first wave
    graduation per architecture v7.0.11 §5 + blueprint §4 v2.x card-hardening
    §4 v2.x card-hardening §4.X.1.4.

    The signature shape IS LOCK-ready. Cycle 2 author-response at L-005 may
    fold-in additional sub-tags via row-170 transparent-disposition precedent.
    """

    raise NotImplementedError(
        f"{GATE_ID} predicate body graduates LIVE at v0.2 first wave per "
        f"architecture v7.0.11 §5. Cycle 2 author-response at L-005 may fold-in "
        f"additional sub-tags via row-170 precedent."
    )
