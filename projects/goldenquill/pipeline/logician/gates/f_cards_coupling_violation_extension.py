"""F-CARDS-COUPLING-VIOLATION-EXTENSION — extends v7.0.8 F-CIC-CLC-COUPLING-VIOLATION
to card file format.

Per blueprint §4 v2.x card-hardening §4.X.1.7. Fails closed when:
  - CIC card body includes CLC allowlists, deny-lists, ranking preferences,
    win-rate fields, frequency fields, or any field implying CIC→CLC pairing
    preference. Explicitly includes common_clc_patterns_observed and any
    equivalent renaming.
  - CLC card body includes CIC allowlists, deny-lists, ranking preferences,
    win-rate fields, or any field implying CLC→CIC restriction.
  - Matrix card body declares binding_eligibility: true or omits
    status: "FORWARD_COMPAT_ONLY" before the v1.x matrix-phase explicit amendment.

Predicate body graduates LIVE at v0.2 first wave; FORBIDDEN_FIELD_REGISTRY is
LIVE at v7.0.11 LOCK to support drift testing via R-CARDS-NO-COUPLING-FIELD
AST-lint at build time.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Final, Literal, Mapping


GATE_ID: Final[str] = "F-CARDS-COUPLING-VIOLATION-EXTENSION"


# Forbidden top-level card field names per axis.
# MappingProxyType-wrapped per §4 v2.x.1 row-198 RT-14 fold-in precedent
# (immutability against runtime monkey-patching).
_FORBIDDEN_FIELD_REGISTRY_RAW: Mapping[str, frozenset[str]] = {
    "CIC": frozenset({
        "common_clc_patterns_observed",       # killed at v7.0.11 LOCK per arch §6.1
        "eligible_clc_subset",
        "clc_allowlist",
        "clc_denylist",
        "preferred_clcs",
        "clc_win_rate",
        "clc_ranking_preferences",
    }),
    "CLC": frozenset({
        "eligible_cic_subset",
        "cic_allowlist",
        "cic_denylist",
        "preferred_cics",
        "cic_win_rate",
        "cic_ranking_preferences",
    }),
    "MATRIX": frozenset(),  # matrix-specific structural rules enforced in evaluate()
}

FORBIDDEN_FIELD_REGISTRY: Final[Mapping[str, frozenset[str]]] = MappingProxyType(_FORBIDDEN_FIELD_REGISTRY_RAW)


@dataclass(frozen=True, kw_only=True)
class GateOutcome:
    passed: bool
    message: str
    violations: tuple[str, ...] = ()


def evaluate(
    *,
    card_path: str,
    card_body: Mapping[str, object],
    declared_axis: Literal["CIC", "CLC", "MATRIX"],
    v1_x_matrix_phase_active: bool = False,
) -> GateOutcome:
    """Evaluate the gate.

    DRAFT predicate body. Raises NotImplementedError until v0.2 first wave
    graduation. The FORBIDDEN_FIELD_REGISTRY constant IS LIVE at v7.0.11 LOCK
    so R-CARDS-NO-COUPLING-FIELD AST-lint can scan card files at build
    time even before the runtime gate body lands.
    """

    raise NotImplementedError(
        f"{GATE_ID} predicate body graduates LIVE at v0.2 first wave per "
        f"architecture v7.0.11 §5. FORBIDDEN_FIELD_REGISTRY constant is LIVE "
        f"at v0.1 Beta LOCK for AST-lint scan support."
    )
