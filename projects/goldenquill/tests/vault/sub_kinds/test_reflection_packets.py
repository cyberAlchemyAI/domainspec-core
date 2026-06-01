"""Tests for `pipeline.vault.sub_kinds.reflection_packets`. [§16 v1 LOCK]

v0.1 hook DORMANT scope per OQ-2 (a):
- Dataclass mechanics (frozen + kw_only) — LIVE assertions.
- Canonical-codec round-trip — LIVE assertions.
- 21 invariants enforced at __post_init__ (length/grammar/type/closed-set/
  signature shape) — LIVE assertions covering the scaffold-testable
  subset; semantic invariants requiring runtime substrate stay under
  predicate-body NotImplementedError at the F-PACKET-* gate layer.

SUB_KIND_REGISTRY entry is DEFERRED to v0.2 first wave — NOT registered
at v0.1 hook. This test verifies the deferral marker.
"""
from __future__ import annotations

import json

import pytest

from pipeline.vault.sub_kinds.reflection_packets import (
    SUB_KIND_REGISTRY_REGISTERED_AT_V0_1,
    BLUEPRINT_DEPS,
    CycleOutcome,
    GatePassCounts,
    INTENT,
    PacketSpanProvenance,
    PatternObservation,
    ProposedLesson,
    ReflectionPacket,
    ScoreSignals,
    SUB_KIND,
    VAULT_SUBTREE,
    from_canonical_bytes,
    to_canonical_bytes,
)


# ---------------------------------------------------------------------------
# Helpers — minimal valid record fixtures
# ---------------------------------------------------------------------------


def _make_pattern() -> PatternObservation:
    return PatternObservation(
        pattern_summary="pattern level summary text",
        cic="food_systems",
        clc="market_access",
        frequency=1,
        severity="LOW",
        first_observed_cycle_id="CYCLE_2026Q3_001",
        supporting_span_ids=("span_abc123",),
    )


def _make_lesson(*, frequency: int = 2, severity: str = "MEDIUM") -> ProposedLesson:
    return ProposedLesson(
        lesson_id="LESSON_001",
        pattern_summary="pattern-rolled lesson text",
        proposed_rule="actionable rule text",
        frequency=frequency,
        severity=severity,
        supporting_pattern_observation_ids=("obs_001",),
        supporting_cycle_ids=tuple(f"CYCLE_{i:03d}" for i in range(frequency)),
    )


def _make_counts() -> GatePassCounts:
    return GatePassCounts(
        f_class_pass=10,
        f_class_fail=0,
        f_archivist_pass=5,
        f_archivist_fail=0,
        f_reflection_pass=8,
        f_reflection_fail=0,
        f_packet_pass=0,
        f_packet_fail=0,
        f_logician_total_pass=23,
        f_logician_total_fail=0,
    )


def _make_signals() -> ScoreSignals:
    return ScoreSignals(
        judge_score=95,
        red_team_score=88,
        editor_verdict="READY",
        judge_red_team_divergence=7,
        council_split_fired=False,
        cross_family_satisfied=True,
    )


def _make_outcome_pending() -> CycleOutcome:
    return CycleOutcome(
        status="PENDING",
        funder_id=None,
        award_amount_minor_units=None,
        award_currency=None,
        decision_observed_at=None,
        outcome_evidence_span_ids=(),
    )


def _make_outcome_awarded() -> CycleOutcome:
    return CycleOutcome(
        status="AWARDED",
        funder_id="USDA_VAPG",
        award_amount_minor_units=25000000,  # $250,000.00
        award_currency="USD",
        decision_observed_at="2026-08-15T14:30:00Z",
        outcome_evidence_span_ids=("evidence_span_001",),
    )


def _make_provenance() -> PacketSpanProvenance:
    return PacketSpanProvenance(
        trace_ids=("trace_abc",),
        logfire_export_uri=None,
        per_claim_span_ids={
            "gate_pass_counts.f_logician_total_pass": ("span_001",),
        },
    )


_HEX_128 = "0" * 128  # placeholder SHA3-512 / Ed25519 sig (128 hex chars)


def _make_packet_pending() -> ReflectionPacket:
    return ReflectionPacket(
        packet_id="PACKET_001",
        cycle_id="CYCLE_2026Q3_001",
        org_slug="fit_farms",
        schema_version="1.0.0",
        classification_register_version=_HEX_128,
        emitted_at="2026-08-01T12:00:00Z",
        emitted_by_seat="archivist.reflection_submode",
        cycle_close_marker_span_id="cycle_close_span_001",
        pattern_observations=(_make_pattern(),),
        lessons_proposed=(_make_lesson(),),
        gate_pass_counts=_make_counts(),
        score_signals=_make_signals(),
        outcome=_make_outcome_pending(),
        grounding_signal_classes=frozenset({"operator_approval"}),
        span_provenance=_make_provenance(),
        canonical_bytes_hash=_HEX_128,
        producer_signature_ed25519=_HEX_128,
        operator_signature_ed25519=None,
    )


def _make_packet_backfill_awarded() -> ReflectionPacket:
    return ReflectionPacket(
        packet_id="PACKET_002",
        cycle_id="CYCLE_2026Q3_001",
        org_slug="fit_farms",
        schema_version="1.0.0",
        classification_register_version=_HEX_128,
        emitted_at="2026-08-15T15:00:00Z",
        emitted_by_seat="archivist.reflection_submode",
        cycle_close_marker_span_id="cycle_close_span_001",
        pattern_observations=(_make_pattern(),),
        lessons_proposed=(_make_lesson(),),
        gate_pass_counts=_make_counts(),
        score_signals=_make_signals(),
        outcome=_make_outcome_awarded(),
        grounding_signal_classes=frozenset({"external_funder_outcome"}),
        span_provenance=_make_provenance(),
        canonical_bytes_hash=_HEX_128,
        producer_signature_ed25519=_HEX_128,
        operator_signature_ed25519=_HEX_128,
    )


# ---------------------------------------------------------------------------
# Module-level invariants
# ---------------------------------------------------------------------------


def test_sub_kind_registry_dormant_at_v0_1_hook() -> None:
    """OQ-2 (a) — registration deferred to v0.2 first wave."""
    assert SUB_KIND_REGISTRY_REGISTERED_AT_V0_1 is False
    assert SUB_KIND == "reflection_packet"
    assert VAULT_SUBTREE == "operational/reflection_packets/"
    assert INTENT == "operational-reflection-packet-write"


def test_blueprint_deps_register_section_16_lock() -> None:
    deps = BLUEPRINT_DEPS["section_16_reflection_packet.md"]
    assert "LOCKED" in deps["version"]
    assert "§16.2.1 ReflectionPacket schema" in deps["sections_implemented"]


# ---------------------------------------------------------------------------
# Dataclass mechanics — frozen + kw_only
# ---------------------------------------------------------------------------


def test_packet_is_frozen_dataclass() -> None:
    pkt = _make_packet_pending()
    with pytest.raises(Exception):  # FrozenInstanceError subclass of AttributeError
        pkt.packet_id = "MUTATED"  # type: ignore[misc]


def test_packet_requires_kw_only_construction() -> None:
    with pytest.raises(TypeError):
        ReflectionPacket(  # type: ignore[call-arg]
            "PACKET_001",  # positional — should raise
        )


def test_pattern_observation_frozen() -> None:
    obs = _make_pattern()
    with pytest.raises(Exception):
        obs.cic = "educator"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Canonical-bytes codec round-trip
# ---------------------------------------------------------------------------


def test_canonical_codec_round_trip_pending() -> None:
    pkt = _make_packet_pending()
    cb = to_canonical_bytes(pkt)
    assert isinstance(cb, bytes)
    decoded = from_canonical_bytes(cb)
    assert isinstance(decoded, dict)
    # canonical bytes exclude signature fields
    assert "canonical_bytes_hash" not in decoded
    assert "producer_signature_ed25519" not in decoded
    assert "operator_signature_ed25519" not in decoded
    # canonical bytes include cycle_id (RT-04/RT-05 closure)
    assert decoded["cycle_id"] == "CYCLE_2026Q3_001"
    assert decoded["packet_id"] == "PACKET_001"
    assert decoded["classification_register_version"] == _HEX_128


def test_canonical_codec_round_trip_awarded() -> None:
    pkt = _make_packet_backfill_awarded()
    cb = to_canonical_bytes(pkt)
    decoded = from_canonical_bytes(cb)
    assert decoded["outcome"]["status"] == "AWARDED"
    assert decoded["outcome"]["award_amount_minor_units"] == 25000000


def test_canonical_codec_sorts_keys_for_stability() -> None:
    pkt = _make_packet_pending()
    cb1 = to_canonical_bytes(pkt)
    cb2 = to_canonical_bytes(pkt)
    assert cb1 == cb2  # stable across re-encode
    # also json.dumps sort_keys produces lexicographic ordering
    decoded = json.loads(cb1.decode("utf-8"))
    keys = list(decoded.keys())
    assert keys == sorted(keys)


def test_canonical_codec_serializes_frozenset_deterministically() -> None:
    pkt = _make_packet_pending()
    cb = to_canonical_bytes(pkt)
    decoded = json.loads(cb.decode("utf-8"))
    assert decoded["grounding_signal_classes"] == ["operator_approval"]


# ---------------------------------------------------------------------------
# Invariant 1 — cycle_id grammar (path-traversal defense)
# ---------------------------------------------------------------------------


def test_cycle_id_path_traversal_rejected() -> None:
    with pytest.raises(ValueError, match="cycle_id"):
        ReflectionPacket(
            packet_id="PACKET_001",
            cycle_id="../etc/passwd",  # path-traversal attempt
            org_slug="fit_farms",
            schema_version="1.0.0",
            classification_register_version=_HEX_128,
            emitted_at="2026-08-01T12:00:00Z",
            emitted_by_seat="archivist.reflection_submode",
            cycle_close_marker_span_id="cycle_close_span_001",
            pattern_observations=(),
            lessons_proposed=(),
            gate_pass_counts=_make_counts(),
            score_signals=_make_signals(),
            outcome=_make_outcome_pending(),
            grounding_signal_classes=frozenset({"operator_approval"}),
            span_provenance=_make_provenance(),
            canonical_bytes_hash=_HEX_128,
            producer_signature_ed25519=_HEX_128,
            operator_signature_ed25519=None,
        )


def test_cycle_id_empty_rejected() -> None:
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["cycle_id"] = ""
    with pytest.raises(ValueError, match="cycle_id"):
        ReflectionPacket(**pkt_kwargs)


# ---------------------------------------------------------------------------
# Invariant 2 — packet_id grammar
# ---------------------------------------------------------------------------


def test_packet_id_grammar_enforced() -> None:
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["packet_id"] = "../../../etc/passwd"
    with pytest.raises(ValueError, match="packet_id"):
        ReflectionPacket(**pkt_kwargs)


# ---------------------------------------------------------------------------
# Invariant 3 — org_slug grammar
# ---------------------------------------------------------------------------


def test_org_slug_grammar_enforced() -> None:
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["org_slug"] = "INVALID-SLUG"  # uppercase + hyphen
    with pytest.raises(ValueError, match="org_slug"):
        ReflectionPacket(**pkt_kwargs)


# ---------------------------------------------------------------------------
# Invariant 4 — semver
# ---------------------------------------------------------------------------


def test_schema_version_semver_enforced() -> None:
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["schema_version"] = "1.0"
    with pytest.raises(ValueError, match="semver"):
        ReflectionPacket(**pkt_kwargs)


# ---------------------------------------------------------------------------
# Invariant 5 — classification_register_version SHA3-512 hex
# ---------------------------------------------------------------------------


def test_classification_register_version_must_be_sha3_512_hex() -> None:
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["classification_register_version"] = "deadbeef"
    with pytest.raises(ValueError, match="classification_register_version"):
        ReflectionPacket(**pkt_kwargs)


# ---------------------------------------------------------------------------
# Invariant 6 — UTC ISO-8601 'Z' on emitted_at
# ---------------------------------------------------------------------------


def test_emitted_at_iso_format() -> None:
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["emitted_at"] = "2026-08-01 12:00:00"  # no T / Z
    with pytest.raises(ValueError, match="emitted_at"):
        ReflectionPacket(**pkt_kwargs)


# ---------------------------------------------------------------------------
# Invariant 7 — emitted_by_seat closed set
# ---------------------------------------------------------------------------


def test_emitted_by_seat_closed_set_v0_1() -> None:
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["emitted_by_seat"] = "scribe"
    with pytest.raises(ValueError, match="emitted_by_seat"):
        ReflectionPacket(**pkt_kwargs)


# ---------------------------------------------------------------------------
# Invariant 8 — CIC + CLC closed sets (PatternObservation)
# ---------------------------------------------------------------------------


def test_pattern_observation_cic_closed_set() -> None:
    with pytest.raises(ValueError, match="cic"):
        PatternObservation(
            pattern_summary="text",
            cic="invalid_cic",
            clc="market_access",
            frequency=1,
            severity="HIGH",
            first_observed_cycle_id="CYCLE_001",
            supporting_span_ids=("span_001",),
        )


def test_pattern_observation_clc_closed_set() -> None:
    with pytest.raises(ValueError, match="clc"):
        PatternObservation(
            pattern_summary="text",
            cic="food_systems",
            clc="invalid_clc",
            frequency=1,
            severity="HIGH",
            first_observed_cycle_id="CYCLE_001",
            supporting_span_ids=("span_001",),
        )


# ---------------------------------------------------------------------------
# Invariant 10 — frequency==1 requires severity=='HIGH' (ProposedLesson)
# ---------------------------------------------------------------------------


def test_proposed_lesson_frequency_one_requires_high() -> None:
    with pytest.raises(ValueError, match="frequency==1"):
        ProposedLesson(
            lesson_id="L1",
            pattern_summary="text",
            proposed_rule="rule",
            frequency=1,
            severity="LOW",  # should be HIGH
            supporting_pattern_observation_ids=("obs1",),
            supporting_cycle_ids=("CYCLE_001",),
        )


def test_proposed_lesson_frequency_one_high_passes() -> None:
    # frequency==1 with severity=HIGH passes
    lesson = ProposedLesson(
        lesson_id="L1",
        pattern_summary="text",
        proposed_rule="rule",
        frequency=1,
        severity="HIGH",
        supporting_pattern_observation_ids=("obs1",),
        supporting_cycle_ids=("CYCLE_001",),
    )
    assert lesson.frequency == 1


# ---------------------------------------------------------------------------
# Invariant 11 — grounding_signal_classes rules
# ---------------------------------------------------------------------------


def test_grounding_signal_classes_must_be_non_empty() -> None:
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["grounding_signal_classes"] = frozenset()
    with pytest.raises(ValueError, match="grounding_signal_classes"):
        ReflectionPacket(**pkt_kwargs)


def test_grounding_signal_classes_rejects_unknown_class() -> None:
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["grounding_signal_classes"] = frozenset({"bogus_class"})
    with pytest.raises(ValueError, match="unknown class"):
        ReflectionPacket(**pkt_kwargs)


def test_grounding_signal_classes_rejects_llm_eval_only_subset() -> None:
    """F-PACKET-EVAL-ONLY-GROUNDED invariant — schema-level."""
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["grounding_signal_classes"] = frozenset(
        {"judge_score", "red_team_score"}
    )
    with pytest.raises(ValueError, match="LLM-eval-only"):
        ReflectionPacket(**pkt_kwargs)


def test_grounding_signal_classes_mixed_passes() -> None:
    """At least one non-LLM-eval-only class admits the LLM-eval-only ones."""
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["grounding_signal_classes"] = frozenset(
        {"operator_approval", "judge_score"}
    )
    pkt = ReflectionPacket(**pkt_kwargs)
    assert pkt.grounding_signal_classes == frozenset(
        {"operator_approval", "judge_score"}
    )


# ---------------------------------------------------------------------------
# Invariant 13-14 — gate counts + score signals int-only (A12 mandate)
# ---------------------------------------------------------------------------


def test_gate_pass_counts_rejects_float() -> None:
    with pytest.raises(ValueError, match="A12"):
        GatePassCounts(
            f_class_pass=10.5,  # type: ignore[arg-type]
            f_class_fail=0,
            f_archivist_pass=0,
            f_archivist_fail=0,
            f_reflection_pass=0,
            f_reflection_fail=0,
            f_packet_pass=0,
            f_packet_fail=0,
            f_logician_total_pass=0,
            f_logician_total_fail=0,
        )


def test_gate_pass_counts_rejects_bool() -> None:
    with pytest.raises(ValueError, match="bool excluded"):
        GatePassCounts(
            f_class_pass=True,  # type: ignore[arg-type]
            f_class_fail=0,
            f_archivist_pass=0,
            f_archivist_fail=0,
            f_reflection_pass=0,
            f_reflection_fail=0,
            f_packet_pass=0,
            f_packet_fail=0,
            f_logician_total_pass=0,
            f_logician_total_fail=0,
        )


def test_score_signals_rejects_out_of_range() -> None:
    with pytest.raises(ValueError, match="judge_score"):
        ScoreSignals(
            judge_score=150,  # out of 0..100
            red_team_score=80,
            editor_verdict="READY",
            judge_red_team_divergence=10,
            council_split_fired=False,
            cross_family_satisfied=True,
        )


# ---------------------------------------------------------------------------
# Invariant 15-16-17 — CycleOutcome status rules
# ---------------------------------------------------------------------------


def test_cycle_outcome_status_closed_set() -> None:
    with pytest.raises(ValueError, match="status"):
        CycleOutcome(
            status="INVALID",
            funder_id=None,
            award_amount_minor_units=None,
            award_currency=None,
            decision_observed_at=None,
            outcome_evidence_span_ids=(),
        )


def test_cycle_outcome_awarded_requires_amount_and_currency() -> None:
    with pytest.raises(ValueError, match="AWARDED"):
        CycleOutcome(
            status="AWARDED",
            funder_id="USDA",
            award_amount_minor_units=None,  # missing
            award_currency="USD",
            decision_observed_at="2026-08-15T14:30:00Z",
            outcome_evidence_span_ids=("span_001",),
        )


def test_cycle_outcome_non_pending_requires_evidence() -> None:
    with pytest.raises(ValueError, match="outcome_evidence"):
        CycleOutcome(
            status="DECLINED",
            funder_id=None,
            award_amount_minor_units=None,
            award_currency=None,
            decision_observed_at="2026-08-15T14:30:00Z",
            outcome_evidence_span_ids=(),  # empty
        )


def test_cycle_outcome_pending_forbids_evidence() -> None:
    with pytest.raises(ValueError, match="PENDING"):
        CycleOutcome(
            status="PENDING",
            funder_id=None,
            award_amount_minor_units=None,
            award_currency=None,
            decision_observed_at=None,
            outcome_evidence_span_ids=("span_001",),  # forbidden
        )


# ---------------------------------------------------------------------------
# Invariant 16 — outcome.status non-PENDING requires operator signature
# ---------------------------------------------------------------------------


def test_outcome_non_pending_requires_operator_signature() -> None:
    pkt_kwargs = _make_packet_backfill_awarded().__dict__.copy()
    pkt_kwargs["operator_signature_ed25519"] = None
    with pytest.raises(ValueError, match="operator_signature"):
        ReflectionPacket(**pkt_kwargs)


def test_outcome_pending_forbids_operator_signature() -> None:
    """Cycle 2 RT-C2-02 fold-in — defensive symmetry."""
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["operator_signature_ed25519"] = _HEX_128
    with pytest.raises(ValueError, match="signature_present_for_pending"):
        ReflectionPacket(**pkt_kwargs)


# ---------------------------------------------------------------------------
# Invariant 18-19-20 — signature hex grammar
# ---------------------------------------------------------------------------


def test_canonical_bytes_hash_must_be_sha3_512_hex() -> None:
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["canonical_bytes_hash"] = "short"
    with pytest.raises(ValueError, match="canonical_bytes_hash"):
        ReflectionPacket(**pkt_kwargs)


def test_producer_signature_must_be_ed25519_hex() -> None:
    pkt_kwargs = _make_packet_pending().__dict__.copy()
    pkt_kwargs["producer_signature_ed25519"] = "short"
    with pytest.raises(ValueError, match="producer_signature"):
        ReflectionPacket(**pkt_kwargs)


# ---------------------------------------------------------------------------
# Smoke — minimum valid Packet 1 (PENDING) + Packet 2 (BACKFILL) construct
# ---------------------------------------------------------------------------


def test_pending_packet_smoke() -> None:
    pkt = _make_packet_pending()
    assert pkt.outcome.status == "PENDING"
    assert pkt.operator_signature_ed25519 is None


def test_backfill_awarded_packet_smoke() -> None:
    pkt = _make_packet_backfill_awarded()
    assert pkt.outcome.status == "AWARDED"
    assert pkt.operator_signature_ed25519 == _HEX_128
    assert pkt.outcome.award_amount_minor_units == 25000000
