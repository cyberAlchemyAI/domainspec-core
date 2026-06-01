"""Tests for §14.6.5 beneficiary_section sub-section composer."""

from __future__ import annotations

import pytest

from pipeline.orchestrator.seats.report_generator.composers._base import ComposerError
from pipeline.orchestrator.seats.report_generator.composers.beneficiary_section import (
    AGGREGATE_IDENTIFYING_THRESHOLD,
    BeneficiarySectionDeps,
    compose_beneficiary_section,
)


def _registry(*, tier="narrative-text-only", history_signed=True, n=3):
    rows = []
    for i in range(n):
        rows.append(
            {
                "record_id": f"BR-{i:03d}",
                "source_path": f"orgs/myorg/vault/operational/grants/G1/period_1/beneficiary_records/BR-{i:03d}.yaml",
                "beneficiary_opaque_id": f"OPAQUE-{i:03d}",
                "outcome_summary": f"Beneficiary {i} completed the workshop.",
                "consent_tier": tier,
                "content_sha3_512": "a" * 128,
                "consent_tier_history_signed_valid": history_signed,
            }
        )
    return {
        ("operational_data", "beneficiary_records"): rows,
        ("reporting_template", None): [{"field_name": "beneficiary_outcomes"}],
    }


def _noop_cedar_assert() -> None:
    """Test fixture — Cedar engine readiness is a no-op."""
    return None


def _make_deps(
    *,
    fixed_clock,
    hash_bytes,
    make_read_intent,
    make_scribe,
    tier="narrative-text-only",
    history_signed=True,
    n=3,
):
    reg = _registry(tier=tier, history_signed=history_signed, n=n)
    return BeneficiarySectionDeps(
        read_beneficiary_records=make_read_intent(reg),
        read_template_field_specs=make_read_intent(reg),
        scribe=make_scribe(),
        clock=fixed_clock,
        hash_bytes=hash_bytes,
        cedar_engine_assert_ready=_noop_cedar_assert,
    )


class TestComposeBeneficiarySection:
    def test_narrative_text_only_inclusion(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe, fixed_clock_value
    ):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
            n=3,
        )
        r = compose_beneficiary_section(
            deps=deps,
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            operational_data_root="orgs/myorg/vault/operational/grants/G1/period_1",
            reporting_template_path="x",
        )
        assert r.aggregate_count == 3
        assert len(r.claims) == 3
        for c in r.claims:
            assert c.sub_section == "beneficiary_section"
            assert c.claim_kind == "beneficiary_reference"
            assert c.consent_tier_history_at_read_utc == fixed_clock_value

    def test_metrics_only_no_per_beneficiary_text(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
            tier="metrics-only",
            n=2,
        )
        r = compose_beneficiary_section(
            deps=deps,
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            operational_data_root="x",
            reporting_template_path="y",
        )
        assert r.aggregate_count == 2
        assert len(r.claims) == 0  # no per-beneficiary text claims
        # aggregate count ≤ AGGREGATE_IDENTIFYING_THRESHOLD → advisory.
        assert r.aggregate_identifying_advisory is True

    def test_no_narrative_exclusion(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
            tier="no-narrative",
            n=5,
        )
        r = compose_beneficiary_section(
            deps=deps,
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            operational_data_root="x",
            reporting_template_path="y",
        )
        assert r.aggregate_count == 0
        assert len(r.claims) == 0
        assert r.aggregate_identifying_advisory is False

    def test_unsigned_history_raises(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
            history_signed=False,
            n=1,
        )
        with pytest.raises(ComposerError):
            compose_beneficiary_section(
                deps=deps,
                org_slug="myorg",
                grant_id="G1",
                period_n=1,
                operational_data_root="x",
                reporting_template_path="y",
            )

    def test_aggregate_advisory_threshold(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        # n=4 → above threshold, no advisory.
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
            n=4,
        )
        r = compose_beneficiary_section(
            deps=deps,
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            operational_data_root="x",
            reporting_template_path="y",
        )
        assert r.aggregate_count == 4
        assert r.aggregate_count > AGGREGATE_IDENTIFYING_THRESHOLD
        assert r.aggregate_identifying_advisory is False
