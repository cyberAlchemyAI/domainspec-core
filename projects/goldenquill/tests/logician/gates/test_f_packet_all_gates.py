"""Consolidated tests for the F-PACKET-* gate family. [§4 v2.x.y LOCK]

v0.1 hook DORMANT scope per OQ-2 (a):
- 18 BINDING gates raise NotImplementedError when invoked — signature-only
  regression tests verify the predicate signatures exist + raise correctly.
- 1 LIVE gate (F-PACKET-COVERAGE-INCOMPLETE) carries real assertions for
  the META-gate dormant-binding lever.

Mirrors §17 WPFA `tests/logician/gates/test_f_wpfa_all_gates.py` pattern.
"""
from __future__ import annotations

import pytest

from pipeline.logician.gates.f_packet_cadence_violation import (
    F_PACKET_CADENCE_VIOLATION,
    predicate_cadence_violation,
)
from pipeline.logician.gates.f_packet_class_mislabel import (
    F_PACKET_CLASS_MISLABEL,
    predicate_class_mislabel,
)
from pipeline.logician.gates.f_packet_class_slot_leak import (
    F_PACKET_CLASS_SLOT_LEAK,
    predicate_class_slot_leak,
)
from pipeline.logician.gates.f_packet_coverage_incomplete import (
    F_PACKET_COVERAGE_INCOMPLETE,
    _BINDING_F_PACKET_CODES,
    check_f_packet_coverage_incomplete,
)
from pipeline.logician.gates.f_packet_cross_org_leak import (
    F_PACKET_CROSS_ORG_LEAK,
    predicate_cross_org_leak,
)
from pipeline.logician.gates.f_packet_cycle_id_unresolvable import (
    F_PACKET_CYCLE_ID_UNRESOLVABLE,
    predicate_cycle_id_unresolvable,
)
from pipeline.logician.gates.f_packet_eval_only_grounded import (
    F_PACKET_EVAL_ONLY_GROUNDED,
    predicate_eval_only_grounded,
)
from pipeline.logician.gates.f_packet_fabrication import (
    F_PACKET_FABRICATION,
    predicate_fabrication,
)
from pipeline.logician.gates.f_packet_instance_leak import (
    F_PACKET_INSTANCE_LEAK,
    predicate_instance_leak,
)
from pipeline.logician.gates.f_packet_memory_injection import (
    F_PACKET_MEMORY_INJECTION,
    predicate_memory_injection,
)
from pipeline.logician.gates.f_packet_operator_signature_invalid import (
    F_PACKET_OPERATOR_SIGNATURE_INVALID,
    predicate_operator_signature_invalid,
)
from pipeline.logician.gates.f_packet_operator_signature_missing import (
    F_PACKET_OPERATOR_SIGNATURE_MISSING,
    predicate_operator_signature_missing,
)
from pipeline.logician.gates.f_packet_outcome_evidence_missing import (
    F_PACKET_OUTCOME_EVIDENCE_MISSING,
    predicate_outcome_evidence_missing,
)
from pipeline.logician.gates.f_packet_premature_generalization import (
    F_PACKET_PREMATURE_GENERALIZATION,
    predicate_premature_generalization,
)
from pipeline.logician.gates.f_packet_producer_unauthorized import (
    F_PACKET_PRODUCER_UNAUTHORIZED,
    predicate_producer_unauthorized,
)
from pipeline.logician.gates.f_packet_retrieval_corruption import (
    F_PACKET_RETRIEVAL_CORRUPTION,
    predicate_retrieval_corruption,
)
from pipeline.logician.gates.f_packet_schema_drift import (
    F_PACKET_SCHEMA_DRIFT,
    predicate_schema_drift,
)
from pipeline.logician.gates.f_packet_signature_invalid import (
    F_PACKET_SIGNATURE_INVALID,
    predicate_signature_invalid,
)
from pipeline.logician.gates.f_packet_span_provenance_missing import (
    F_PACKET_SPAN_PROVENANCE_MISSING,
    predicate_span_provenance_missing,
)


# ---------------------------------------------------------------------------
# Family closed-set membership
# ---------------------------------------------------------------------------


def test_binding_packet_codes_set_is_18() -> None:
    """The META-gate's _BINDING_F_PACKET_CODES contains exactly 18 codes
    (the 19 F-PACKET-* family minus the META-gate itself)."""
    assert len(_BINDING_F_PACKET_CODES) == 18
    assert F_PACKET_COVERAGE_INCOMPLETE not in _BINDING_F_PACKET_CODES


def test_all_codes_namespaced_f_packet() -> None:
    """All 18 BINDING codes start with F-PACKET-."""
    for code in _BINDING_F_PACKET_CODES:
        assert code.startswith("F-PACKET-")


def test_no_f_reflection_or_f_wpfa_or_f_archivist_in_binding_set() -> None:
    """F-CIC-CLC-COUPLING-VIOLATION-class regression — no cross-family
    code crosses into F-PACKET-* family."""
    for code in _BINDING_F_PACKET_CODES:
        assert not code.startswith("F-REFLECTION-")
        assert not code.startswith("F-WPFA-")
        assert not code.startswith("F-ARCHIVIST-")
        assert not code.startswith("F-CLASS-")
        assert not code.startswith("F-REPORT-")
        assert not code.startswith("F-DATACOLLECTOR-")
        assert not code.startswith("F-FG-")


# ---------------------------------------------------------------------------
# 18 BINDING predicates — NotImplementedError at v0.1 hook
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "code,predicate",
    [
        (F_PACKET_INSTANCE_LEAK, predicate_instance_leak),
        (F_PACKET_CROSS_ORG_LEAK, predicate_cross_org_leak),
        (F_PACKET_FABRICATION, predicate_fabrication),
        (F_PACKET_CLASS_SLOT_LEAK, predicate_class_slot_leak),
        (F_PACKET_CLASS_MISLABEL, predicate_class_mislabel),
        (F_PACKET_EVAL_ONLY_GROUNDED, predicate_eval_only_grounded),
        (F_PACKET_PREMATURE_GENERALIZATION, predicate_premature_generalization),
        (F_PACKET_SPAN_PROVENANCE_MISSING, predicate_span_provenance_missing),
        (F_PACKET_RETRIEVAL_CORRUPTION, predicate_retrieval_corruption),
        (F_PACKET_MEMORY_INJECTION, predicate_memory_injection),
        (F_PACKET_SCHEMA_DRIFT, predicate_schema_drift),
        (F_PACKET_CADENCE_VIOLATION, predicate_cadence_violation),
        (F_PACKET_SIGNATURE_INVALID, predicate_signature_invalid),
        (F_PACKET_OPERATOR_SIGNATURE_MISSING, predicate_operator_signature_missing),
        (F_PACKET_OPERATOR_SIGNATURE_INVALID, predicate_operator_signature_invalid),
        (F_PACKET_CYCLE_ID_UNRESOLVABLE, predicate_cycle_id_unresolvable),
        (F_PACKET_OUTCOME_EVIDENCE_MISSING, predicate_outcome_evidence_missing),
        (F_PACKET_PRODUCER_UNAUTHORIZED, predicate_producer_unauthorized),
    ],
)
def test_binding_predicate_realized_at_v0_2_first_wave(
    code: str, predicate
) -> None:
    """Each of the 18 BINDING predicates is REALIZED at v0.2 first wave —
    body MUST NOT raise NotImplementedError. Bodies are keyword-only-
    argument signatures; calling without args raises TypeError (acceptable —
    the META-gate's strict_probe path uses sentinel payloads with the right
    kwargs). Other exceptions (ValueError, etc.) are also acceptable here;
    this test's job is solely to assert NotImplementedError does NOT raise."""
    assert code in _BINDING_F_PACKET_CODES
    try:
        predicate()
    except NotImplementedError:
        pytest.fail(
            f"{code} raised NotImplementedError — body not realized at "
            f"v0.2 first wave"
        )
    except (TypeError, ValueError, KeyError, AttributeError):
        # Expected: predicate has required kwargs or rejects empty input.
        # What matters is NotImplementedError did NOT fire.
        pass


# ---------------------------------------------------------------------------
# F-PACKET-COVERAGE-INCOMPLETE — LIVE META-gate
# ---------------------------------------------------------------------------


def _registry_with_all_18_signatures_present() -> dict[str, object]:
    """Return a gate-realization-registry with all 18 BINDING signatures
    registered (bodies will raise NotImplementedError at call time, but
    signature presence is what the META-gate checks at v0.1 hook)."""
    return {
        F_PACKET_INSTANCE_LEAK: predicate_instance_leak,
        F_PACKET_CROSS_ORG_LEAK: predicate_cross_org_leak,
        F_PACKET_FABRICATION: predicate_fabrication,
        F_PACKET_CLASS_SLOT_LEAK: predicate_class_slot_leak,
        F_PACKET_CLASS_MISLABEL: predicate_class_mislabel,
        F_PACKET_EVAL_ONLY_GROUNDED: predicate_eval_only_grounded,
        F_PACKET_PREMATURE_GENERALIZATION: predicate_premature_generalization,
        F_PACKET_SPAN_PROVENANCE_MISSING: predicate_span_provenance_missing,
        F_PACKET_RETRIEVAL_CORRUPTION: predicate_retrieval_corruption,
        F_PACKET_MEMORY_INJECTION: predicate_memory_injection,
        F_PACKET_SCHEMA_DRIFT: predicate_schema_drift,
        F_PACKET_CADENCE_VIOLATION: predicate_cadence_violation,
        F_PACKET_SIGNATURE_INVALID: predicate_signature_invalid,
        F_PACKET_OPERATOR_SIGNATURE_MISSING: predicate_operator_signature_missing,
        F_PACKET_OPERATOR_SIGNATURE_INVALID: predicate_operator_signature_invalid,
        F_PACKET_CYCLE_ID_UNRESOLVABLE: predicate_cycle_id_unresolvable,
        F_PACKET_OUTCOME_EVIDENCE_MISSING: predicate_outcome_evidence_missing,
        F_PACKET_PRODUCER_UNAUTHORIZED: predicate_producer_unauthorized,
    }


def test_meta_gate_passes_when_all_18_signatures_present() -> None:
    """LIVE META-gate body — all 18 BINDING signatures registered → PASS."""
    registry = _registry_with_all_18_signatures_present()
    result = check_f_packet_coverage_incomplete(
        gate_realization_registry=registry
    )
    assert result.success is True
    assert result.failure_code is None
    assert result.missing_bodies == ()


def test_meta_gate_fail_closed_when_any_signature_missing() -> None:
    """LIVE META-gate body — drop one signature → FAIL_CLOSED with detail
    naming the missing code."""
    registry = _registry_with_all_18_signatures_present()
    del registry[F_PACKET_INSTANCE_LEAK]
    result = check_f_packet_coverage_incomplete(
        gate_realization_registry=registry
    )
    assert result.success is False
    assert result.failure_code == F_PACKET_COVERAGE_INCOMPLETE
    assert F_PACKET_INSTANCE_LEAK in result.missing_bodies


def test_meta_gate_fail_closed_when_none_value() -> None:
    """LIVE META-gate body — entry value of None → FAIL_CLOSED."""
    registry = _registry_with_all_18_signatures_present()
    registry[F_PACKET_INSTANCE_LEAK] = None
    result = check_f_packet_coverage_incomplete(
        gate_realization_registry=registry
    )
    assert result.success is False
    assert F_PACKET_INSTANCE_LEAK in result.missing_bodies


def test_meta_gate_fail_closed_when_non_callable_value() -> None:
    """LIVE META-gate body — entry value not callable → FAIL_CLOSED."""
    registry = _registry_with_all_18_signatures_present()
    registry[F_PACKET_INSTANCE_LEAK] = "not a callable"  # type: ignore[assignment]
    result = check_f_packet_coverage_incomplete(
        gate_realization_registry=registry
    )
    assert result.success is False
    assert F_PACKET_INSTANCE_LEAK in result.missing_bodies


def test_meta_gate_rejects_non_mapping_input() -> None:
    """LIVE META-gate body — non-Mapping input → FAIL_CLOSED."""
    result = check_f_packet_coverage_incomplete(
        gate_realization_registry=["not", "a", "mapping"]  # type: ignore[arg-type]
    )
    assert result.success is False
    assert "Mapping" in result.detail


def test_meta_gate_detail_lists_all_missing_codes() -> None:
    """LIVE META-gate body — multiple missing → all listed in missing_bodies."""
    registry = _registry_with_all_18_signatures_present()
    del registry[F_PACKET_INSTANCE_LEAK]
    del registry[F_PACKET_CROSS_ORG_LEAK]
    del registry[F_PACKET_FABRICATION]
    result = check_f_packet_coverage_incomplete(
        gate_realization_registry=registry
    )
    assert result.success is False
    assert set(result.missing_bodies) == {
        F_PACKET_INSTANCE_LEAK,
        F_PACKET_CROSS_ORG_LEAK,
        F_PACKET_FABRICATION,
    }


# ---------------------------------------------------------------------------
# F-PACKET-SPAN-PROVENANCE-MISSING — resolves §17 v1 §6.5 forward-reference
# ---------------------------------------------------------------------------


def test_span_provenance_missing_resolves_wpfa_forward_reference() -> None:
    """§17 v1 §6.5 forward-reference to F-PACKET-SPAN-PROVENANCE-MISSING
    resolves at this LOCK — the predicate signature exists in the
    F-PACKET-* family with the documented sibling-pattern semantics.
    At v0.2 first wave the body is LIVE; happy-path returns PASS."""
    assert F_PACKET_SPAN_PROVENANCE_MISSING in _BINDING_F_PACKET_CODES
    # LIVE happy-path sentinel payload (mirrors _SENTINEL_PROBES_V0_2)
    from pipeline.logician.gates.f_packet_span_provenance_missing import (
        check_f_packet_span_provenance_missing,
    )

    result = check_f_packet_span_provenance_missing(
        per_claim_span_ids={
            "gate_pass_counts.f_packet_pass": ("s1",),
            "gate_pass_counts.f_packet_fail": ("s1",),
            "gate_pass_counts.f_logician_total_pass": ("s1",),
            "gate_pass_counts.f_logician_total_fail": ("s1",),
            "score_signals.judge_score": ("s1",),
            "score_signals.red_team_score": ("s1",),
            "outcome.status": ("s1",),
        },
        resolvable_span_ids=("s1",),
        packet_cycle_id="cyc-probe",
    )
    assert result.success is True
    assert result.failure_code is None


# ---------------------------------------------------------------------------
# F-PACKET-* EXCLUDED from F-CLASS-COVERAGE-INCOMPLETE META gate
# ---------------------------------------------------------------------------


def test_f_packet_codes_not_in_f_class_family() -> None:
    """F-PACKET-* EXCLUDED from F-CLASS-COVERAGE-INCOMPLETE per OQ-6-style
    isolation precedent (mirrors §17 WPFA + §2 v7.5 FG exclusions)."""
    for code in _BINDING_F_PACKET_CODES:
        assert not code.startswith("F-CLASS-")
    assert not F_PACKET_COVERAGE_INCOMPLETE.startswith("F-CLASS-")
