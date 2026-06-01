"""F-CARDS-PRIVATE-DATA-IN-CARD — Card body contains a field matching the private-org-data shape (org_slug, client_name, EIN, UEI, address, banking, named individuals, named private clients, private cycle IDs).

Per blueprint §4 v2.x card-hardening §4.X.1.5. PRE-load all-environments gate.

Predicate body graduates LIVE at v0.2 first wave per architecture v7.0.11 §5.
At v0.1 Beta LOCK this raises NotImplementedError as part of the dormant-
primitive shape (mirrors v7.0.7 §5.1 F-CLASS-* + v7.0.9 F-REFLECTION-* +
§16 v1 F-PACKET-* + §17 v1 §17.6 F-WPFA-* family precedents byte-for-byte).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal, Mapping


GATE_ID: Final[str] = "F-CARDS-PRIVATE-DATA-IN-CARD"


@dataclass(frozen=True, kw_only=True)
class GateOutcome:
    passed: bool
    message: str


def evaluate(*, card_path: str, card_body: Mapping[str, object], private_data_field_pattern_registry: frozenset[str]) -> GateOutcome:
    """Evaluate the gate.

    DRAFT predicate body. Raises NotImplementedError until v0.2 first wave
    graduation per architecture v7.0.11 §5 + blueprint §4 v2.x card-hardening
    §4 v2.x card-hardening §4.X.1.5.

    The signature shape IS LOCK-ready. Cycle 2 author-response at L-005 may
    fold-in additional sub-tags via row-170 transparent-disposition precedent.
    """

    raise NotImplementedError(
        f"{GATE_ID} predicate body graduates LIVE at v0.2 first wave per "
        f"architecture v7.0.11 §5. Cycle 2 author-response at L-005 may fold-in "
        f"additional sub-tags via row-170 precedent."
    )
