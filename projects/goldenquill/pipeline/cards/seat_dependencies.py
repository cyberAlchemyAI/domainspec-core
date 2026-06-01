"""pipeline.cards.seat_dependencies — Per-seat card-field dependency registry.

Per architecture v7.0.11 §7.3 (resolved 2026-05-15 PM, operator directive
"whatever is best most solid most reliable most honest least error pronne").

Each consuming seat declares STATICALLY which card fields it reads at
runtime. The F-CARDS-COVERAGE-INCOMPLETE META gate (§4 v2.x card-hardening
§4.X.1.1) reads this registry at loader step 8 and fail-closes in production
when a loaded card is missing a field that a registered consumer seat
depends on.

Static declarations were chosen over Cedar-evaluable runtime introspection
because:

1. Drift-testable at build time via AST-lint R-CARDS-SEAT-DEPS-DRIFT (cross-
   checks each seat's declared dependencies against the seat's actual
   card reads).
2. Deterministic — every card load produces the same gate decision.
3. Auditable — operator can grep this single file to know exactly which
   seat reads which field.
4. Sovereignty-aligned — no opaque runtime instrumentation; the registry IS
   the contract.

The MappingProxyType wrapper mirrors §4 v2.x.1 row-198 R-ARCHIVIST-NO-CANONICAL-
MUTATE FORBIDDEN_PRIMITIVES pattern byte-for-byte for runtime immutability
against monkey-patching attacks (RT-14 fold-in precedent at v7.0.11).

DRAFT at v0.1 LOCK candidate state. The actual seat-by-seat field
dependency mappings populate at v0.2 first wave (Phase B runtime context
injection per architecture v7.0.11 §5) when each seat's card consumer
lands LIVE. At v0.1 Beta LOCK the registry exists with empty per-seat sets
so the META gate has the shape to read; the gate passes trivially when
every seat dependency set is empty.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final, Mapping


# Seat identifiers — must exactly match the consumer-seat identifiers used by
# pipeline.orchestrator.seats.* registration.
SEAT_NAMES: Final[frozenset[str]] = frozenset({
    "Scout",
    "Scribe",
    "Judge",
    "Logician_as_consumer",
    "Archivist",
    "ReportGenerator",
    "ModelRouter",
})


# Per-seat → per-axis → frozenset of card field paths the seat reads.
#
# Field paths use dot notation rooted at the card top level
# (e.g., "search_vocabulary.core_terms", "register_defaults.language_register").
#
# At v0.1 Beta LOCK the registry is empty per-seat — populates at v0.2 first
# wave (Phase B runtime context injection) when each seat's card consumer
# lands LIVE. The empty registry is intentional and shippable: it documents
# that no seat consumes card content at v0.1 Beta, which matches the
# "schema-ready, runtime wiring v0.2" customer-facing caveat (§18.19 open
# question).
#
# Population at v0.2 first wave proceeds seat-by-seat alongside the
# CardRuntimeContext wiring per blueprint §18.16.B. Each seat-binding LOCK
# round amends this file via a paired §0.5 sub-tag-extension at the seat's
# §4 v2.x.y amendment (precedent: §4 v2.x.3 row 219 sub-tag-extension pattern).
_SEAT_CARD_FIELD_DEPENDENCIES_RAW: Mapping[str, Mapping[str, frozenset[str]]] = {
    "Scout": {
        "CIC": frozenset(),       # populates v0.2 first wave; planned reads: search_vocabulary, evidence_signals, kfr_fact_classes, admin_risk_term_register
        "CLC": frozenset(),       # populates v0.2 first wave; planned reads: underwriting_criteria.criterion (for funder-side classification)
    },
    "Scribe": {
        "CIC": frozenset(),       # populates v0.2 first wave; planned: register_defaults, dialect_routing_table, admin_risk_term_register, narrative_sections_typical
        "CLC": frozenset(),       # populates v0.2 first wave; planned: narrative_section_patterns, evidence_weights, budget_structure_conventions
    },
    "Judge": {
        "CIC": frozenset(),       # populates v0.2 first wave; planned: capacity_signals_required, compliance_burdens
        "CLC": frozenset(),       # populates v0.2 first wave; planned: underwriting_criteria, scoring_weight_patterns, evidence_weights, reviewer_profile_typical, common_red_flags
    },
    "Logician_as_consumer": {
        "CIC": frozenset(),       # populates v0.2 first wave; planned: compliance_burdens, provenance_requirements
        "CLC": frozenset(),       # populates v0.2 first wave; planned: common_application_forms, compliance_obligations
    },
    "Archivist": {
        "CIC": frozenset(),       # populates v0.2 first wave (between-cycle Reflection sub-mode); planned: common_funders_observed, common_risk_register_entries
        "CLC": frozenset(),       # populates v0.2 first wave; planned: commitment_tracking_pattern, reporting_requirements_typical
    },
    "ReportGenerator": {
        "CIC": frozenset(),       # populates v0.2 horizon (§14 v0.2 first wave); planned: reporting_cadence_typical, metrics_table_template
        "CLC": frozenset(),       # populates v0.2 horizon; planned: reporting_requirements_typical, commitment_tracking_pattern
    },
    "ModelRouter": {
        "CIC": frozenset(),       # ModelRouter does not read card body fields; reads only card classification posture (shareable_by_construction)
        "CLC": frozenset(),       # same
    },
}


# MappingProxyType wrap — runtime-immutable. Mirrors §4 v2.x.1 row-198 RT-14
# fold-in precedent (R-ARCHIVIST-NO-CANONICAL-MUTATE FORBIDDEN_PRIMITIVES).
SEAT_CARD_FIELD_DEPENDENCIES: Final[Mapping[str, Mapping[str, frozenset[str]]]] = MappingProxyType({
    seat: MappingProxyType({axis: deps for axis, deps in axis_deps.items()})
    for seat, axis_deps in _SEAT_CARD_FIELD_DEPENDENCIES_RAW.items()
})


def all_declared_field_paths(*, axis: str) -> frozenset[str]:
    """Return the union of field paths declared across all seats for the
    given axis ('CIC' or 'CLC'). Used by F-CARDS-COVERAGE-INCOMPLETE
    coverage check.
    """

    result: set[str] = set()
    for seat_deps in SEAT_CARD_FIELD_DEPENDENCIES.values():
        result.update(seat_deps.get(axis, frozenset()))
    return frozenset(result)


def seats_depending_on(*, axis: str, field_path: str) -> frozenset[str]:
    """Return the set of seat names that depend on the given field path
    for the given axis. Used by F-CARDS-COVERAGE-INCOMPLETE to identify
    which seats break when a card omits the field.
    """

    return frozenset(
        seat
        for seat, axis_deps in SEAT_CARD_FIELD_DEPENDENCIES.items()
        if field_path in axis_deps.get(axis, frozenset())
    )
