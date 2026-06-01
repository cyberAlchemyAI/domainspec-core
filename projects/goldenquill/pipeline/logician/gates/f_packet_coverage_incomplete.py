"""F-PACKET-COVERAGE-INCOMPLETE — META PRE-cycle gate. [§4 v2.x.y.1 row 19, LIVE STRENGTHENED]

The dormant-binding lever for the F-PACKET-* family. STRENGTHENED at v0.2
first wave per RT-01 fold-in contract 7: dry-run probe each BINDING
predicate with a minimal sentinel payload AND reject NotImplementedError.

This is the only LIVE-body F-PACKET-* predicate at v0.1 hook. At v0.2 first
wave it STRENGTHENS but stays LIVE. Mirrors:
- ``F-CLASS-COVERAGE-INCOMPLETE`` from architecture v7.0.7 §5.1
- ``F-REFLECTION-COVERAGE-INCOMPLETE`` from §0.5 v18 row 404 (§4 v2.x.2)

F-PACKET-* is EXCLUDED from F-CLASS-COVERAGE-INCOMPLETE per OQ-6-style
isolation precedent (§17 WPFA row 207 + §2 v7.5 FG row 213).

Blueprint authority:
    - section_04_v2_x_y_packet_amendment.md §2 row 19
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.2 (strengthening)
    - section_16_reflection_packet.md §16.8
    - section_16_reflection_packet.md §16.10.1 RT-01 fold-in
    - section_16_v1_1_amendment.md §16.v1.1.7
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Callable, Final, Mapping, Optional, Tuple


F_PACKET_COVERAGE_INCOMPLETE: Final[str] = "F-PACKET-COVERAGE-INCOMPLETE"

# The 18 BINDING F-PACKET-* codes that REQUIRE realized bodies.
# F-PACKET-COVERAGE-INCOMPLETE itself is the lever — not registered here.
_BINDING_F_PACKET_CODES: Final[frozenset[str]] = frozenset(
    {
        "F-PACKET-INSTANCE-LEAK",
        "F-PACKET-CROSS-ORG-LEAK",
        "F-PACKET-FABRICATION",
        "F-PACKET-CLASS-SLOT-LEAK",
        "F-PACKET-CLASS-MISLABEL",
        "F-PACKET-EVAL-ONLY-GROUNDED",
        "F-PACKET-PREMATURE-GENERALIZATION",
        "F-PACKET-SPAN-PROVENANCE-MISSING",
        "F-PACKET-RETRIEVAL-CORRUPTION",
        "F-PACKET-MEMORY-INJECTION",
        "F-PACKET-SCHEMA-DRIFT",
        "F-PACKET-CADENCE-VIOLATION",
        "F-PACKET-SIGNATURE-INVALID",
        "F-PACKET-OPERATOR-SIGNATURE-MISSING",
        "F-PACKET-OPERATOR-SIGNATURE-INVALID",
        "F-PACKET-CYCLE-ID-UNRESOLVABLE",
        "F-PACKET-OUTCOME-EVIDENCE-MISSING",
        "F-PACKET-PRODUCER-UNAUTHORIZED",
    }
)


# Sentinel payloads for the dry-run probe per RT-01 fold-in contract 7.
# Each entry: (args_tuple, kwargs_dict). The payload exercises the predicate
# signature without triggering substantive logic — if the body raises
# NotImplementedError on this minimal input, the body is un-realized.
#
# RT-13 fix-in-place at v0.2 first wave Cycle 1: wrap in MappingProxyType to
# prevent runtime mutation. Sentinel-mapping mutation attack class
# (malicious module replaces own entry to evade dry-run) closed at
# canonicalization step. AST-lint R-PACKET-SENTINEL-COVERAGE verifies
# 18-code completeness at source-form layer (defense-in-depth).
#
# Cycle 2 RT-C2-01 + RT-C2-02 noted: MappingProxyType wraps the outer mapping
# but does NOT prevent (a) module-level rebinding `module._SENTINEL_PROBES_V0_2
# = mutable_dict` or (b) mutation of inner kwargs dicts retrieved via lookup.
# BOTH bounded by v7-LOCKED A1 (single-client) + A4 (operator-trusted preflight)
# — module-level rebinding requires write access to the running process which
# is the same envelope as the AST-lint dynamic-import bypass class (RT-02 →
# v2 multi-tenant Section O.5 mitigation track). Inner-kwargs mutation has no
# cross-cycle persistence because the META-gate iterates fresh each call;
# no caller caches the lookup result.
_SENTINEL_PROBES_V0_2: Final[
    Mapping[str, Tuple[tuple, Mapping[str, Any]]]
] = MappingProxyType({
    "F-PACKET-INSTANCE-LEAK": ((), {"texts": ("ok",)}),
    "F-PACKET-CROSS-ORG-LEAK": (
        (),
        {
            "target_write_path": "orgs/probe/vault/operational/reflection_packets/p.json",
            "packet_org_slug": "probe",
            "span_provenance_org_slugs": (),
        },
    ),
    "F-PACKET-FABRICATION": (
        (),
        {
            "packet_gate_pass_counts": {},
            "packet_score_signals": {},
            "packet_outcome": {"status": "PENDING"},
            "span_tree_aggregates": {},
        },
    ),
    "F-PACKET-CLASS-SLOT-LEAK": ((), {"packet_json_bytes": b"{}"}),
    "F-PACKET-CLASS-MISLABEL": (
        (),
        {
            "packet_classification_register_version": "a" * 128,
            "register_at_cycle_start_hash": "a" * 128,
        },
    ),
    "F-PACKET-EVAL-ONLY-GROUNDED": (
        (),
        {"grounding_signal_classes": frozenset({"operator_approval"})},
    ),
    "F-PACKET-PREMATURE-GENERALIZATION": ((), {"lessons_proposed": ()}),
    "F-PACKET-SPAN-PROVENANCE-MISSING": (
        (),
        {
            "per_claim_span_ids": {
                "gate_pass_counts.f_packet_pass": ("s1",),
                "gate_pass_counts.f_packet_fail": ("s1",),
                "gate_pass_counts.f_logician_total_pass": ("s1",),
                "gate_pass_counts.f_logician_total_fail": ("s1",),
                "score_signals.judge_score": ("s1",),
                "score_signals.red_team_score": ("s1",),
                "outcome.status": ("s1",),
            },
            "resolvable_span_ids": ("s1",),
            "packet_cycle_id": "cyc-probe",
        },
    ),
    "F-PACKET-RETRIEVAL-CORRUPTION": ((), {"packet_text_payload": b"hello"}),
    "F-PACKET-MEMORY-INJECTION": ((), {"texts": ("clean text",)}),
    "F-PACKET-SCHEMA-DRIFT": (
        (),
        {"packet_schema_version": "1.1.0", "consumer_known_max": "1.1.0"},
    ),
    "F-PACKET-CADENCE-VIOLATION": (
        (),
        {
            "packet_cycle_id": "cyc-probe",
            "packet_cycle_close_marker_span_id": "marker-1",
            "cycle_close_marker_spans": {
                "marker-1": {
                    "event_type": "cycle_close_marker",
                    "cycle_id": "cyc-probe",
                }
            },
        },
    ),
    "F-PACKET-SIGNATURE-INVALID": (
        (),
        {
            "canonical_bytes": b"{}",
            "packet_canonical_bytes_hash": "0" * 128,
            "packet_producer_signature_hex": "0" * 128,
            "producer_pubkey_bytes": b"\x00" * 32,
        },
    ),
    "F-PACKET-OPERATOR-SIGNATURE-MISSING": (
        (),
        {
            "packet_outcome_status": "PENDING",
            "packet_operator_signature": None,
        },
    ),
    "F-PACKET-OPERATOR-SIGNATURE-INVALID": (
        (),
        {
            "canonical_bytes": b"{}",
            "packet_operator_signature_hex": None,
            "operator_pubkey_bytes": b"\x00" * 32,
        },
    ),
    "F-PACKET-CYCLE-ID-UNRESOLVABLE": (
        (),
        {"packet_cycle_id": "cyc-probe", "known_cycle_ids": ("cyc-probe",)},
    ),
    "F-PACKET-OUTCOME-EVIDENCE-MISSING": (
        (),
        {
            "packet_outcome_status": "PENDING",
            "outcome_evidence_span_ids": (),
            "packet_cycle_id": "cyc-probe",
            "resolvable_span_ids": (),
        },
    ),
    "F-PACKET-PRODUCER-UNAUTHORIZED": (
        (),
        {"packet_emitted_by_seat": "archivist.reflection_submode"},
    ),
})


@dataclass(frozen=True, kw_only=True)
class CoverageIncompleteResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    missing_bodies: tuple[str, ...] = ()
    notimplementederror_bodies: tuple[str, ...] = ()


def check_f_packet_coverage_incomplete(
    *,
    gate_realization_registry: Mapping[str, Callable[..., object] | None],
    strict_probe: bool = True,
) -> CoverageIncompleteResult:
    """META PRE-cycle: every BINDING F-PACKET-* code has a realized body.

    v0.2 STRENGTHENED per RT-01 contract 7:
      1. registry entry exists for each of the 18 BINDING codes
      2. registry entry is callable
      3. ``strict_probe=True`` (v0.2 default): dry-run each callable with
         a minimal sentinel payload AND verify the body does NOT raise
         NotImplementedError; any NotImplementedError signals an un-realized
         body (the dormant-binding lever).
    """
    if not isinstance(gate_realization_registry, Mapping):
        return CoverageIncompleteResult(
            success=False,
            failure_code=F_PACKET_COVERAGE_INCOMPLETE,
            detail=(
                "gate_realization_registry must be a Mapping; got "
                f"{type(gate_realization_registry).__name__}"
            ),
        )
    missing: list[str] = []
    notimplemented: list[str] = []
    for code in sorted(_BINDING_F_PACKET_CODES):
        entry = gate_realization_registry.get(code)
        if entry is None:
            missing.append(code)
            continue
        if not callable(entry):
            missing.append(code)
            continue
        if strict_probe:
            probe = _SENTINEL_PROBES_V0_2.get(code)
            if probe is None:
                # No sentinel registered — coverage incomplete at probe layer
                missing.append(code)
                continue
            args, kwargs = probe
            try:
                _ = entry(*args, **kwargs)
            except NotImplementedError:
                notimplemented.append(code)
            except Exception:
                # Other exceptions OK — body is realized, just may not handle
                # this specific probe shape; the META-gate's job is solely
                # to detect NotImplementedError stub bodies.
                pass
    if missing or notimplemented:
        return CoverageIncompleteResult(
            success=False,
            failure_code=F_PACKET_COVERAGE_INCOMPLETE,
            detail=(
                "F-PACKET-* BINDING gates fail coverage. "
                f"missing: {missing!r}; NotImplementedError: {notimplemented!r}"
            ),
            missing_bodies=tuple(missing),
            notimplementederror_bodies=tuple(notimplemented),
        )
    return CoverageIncompleteResult(
        success=True,
        failure_code=None,
        detail=(
            "all 18 F-PACKET-* BINDING gates have realized bodies "
            "(dry-run probe confirmed no NotImplementedError)"
        ),
    )


__all__ = [
    "F_PACKET_COVERAGE_INCOMPLETE",
    "CoverageIncompleteResult",
    "check_f_packet_coverage_incomplete",
    "_BINDING_F_PACKET_CODES",
    "_SENTINEL_PROBES_V0_2",
]
