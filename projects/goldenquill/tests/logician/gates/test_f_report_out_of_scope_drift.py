"""Tests for ``pipeline.logician.gates.f_report_out_of_scope_drift``.

Per §14.9.3 Cycle 1 + Cycle 2 closures (RT-6a/6c + RT-7a + RT-C2-03).
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from pipeline.logician.gates._report_protocols import PromotedCommitmentRow
from pipeline.logician.gates.f_report_out_of_scope_drift import (
    AGGREGATE_IDENTIFYING_THRESHOLD,
    AggregateBeneficiaryCountReference,
    BeneficiaryConsentInfo,
    F_REPORT_OUT_OF_SCOPE_DRIFT,
    PhotoConsentInfo,
    SUB_TAG_BENEFICIARY_AGGREGATE_IDENTIFYING,
    SUB_TAG_BENEFICIARY_CONSENT_TIER_VIOLATION,
    SUB_TAG_BENEFICIARY_PRIVACY_LEAK,
    SUB_TAG_CROSS_GRANT,
    SUB_TAG_CROSS_ORG,
    SUB_TAG_CROSS_PERIOD,
    SUB_TAG_PHOTO_CONSENT_TIER_VIOLATION,
    SUB_TAG_PHOTO_CONSENT_TIER_VIOLATION_CROSS_SECTION,
    SUB_TAG_RUNTIME_SCOPE_TAG_EXTRACTION_FAILED,
    SUB_TAG_SCOPE_TAG_NOT_IN_PROMOTED_SET,
    check_out_of_scope_drift,
)
from pipeline.orchestrator.seats.report_generator._schemas import (
    ClaimEntry,
    SourceRef,
)
from pipeline.orchestrator.seats.report_generator.claim_evidence_map import (
    assemble_claim_evidence_map,
)


def _build_map_with_source(source_path, claim_kind="narrative", sub_section="narrative",
                            claim_text="Trained farmers in PA"):
    src = SourceRef(
        kind="operational_data",
        sub_kind=("narrative_entries" if claim_kind == "narrative" else "metrics"),
        source_path=source_path,
        source_row_id="r1",
        source_content_sha3_512="a" * 128,
    )
    if claim_kind == "narrative":
        claim = ClaimEntry(
            claim_id="C1", sub_section=sub_section, claim_text=claim_text,
            claim_kind="narrative", sources=(src,),
        )
    else:
        src = SourceRef(
            kind="operational_data", sub_kind="metrics",
            source_path=source_path, source_row_id="r1",
            source_content_sha3_512="a" * 128, source_value=Decimal("50"),
        )
        claim = ClaimEntry(
            claim_id="C1", sub_section=sub_section, claim_text=claim_text,
            claim_kind="numeric", sources=(src,),
        )
    return assemble_claim_evidence_map(
        run_id="r", org_slug="myorg", grant_id="G1", period_n=1,
        draft_path="d", draft_version=1, draft_content_sha3_512="f" * 128,
        authored_at_utc="now", authored_by_seat="scribe", claims=(claim,),
    )


def _prom(*scope_tags):
    return [PromotedCommitmentRow(
        commitment_id="COMMIT-001", status="PROMOTED",
        scope_tags=scope_tags, required_sub_sections=("narrative",),
    )]


class TestHappyPath:
    def test_in_scope_passes(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("agriculture", "pennsylvania"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("agriculture", "pennsylvania"),
        )
        assert r.success


class TestScopeTagDrift:
    def test_scope_tag_not_in_promoted_fires(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("agriculture"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("agriculture", "unrelated_tag"),
        )
        assert not r.success
        assert SUB_TAG_SCOPE_TAG_NOT_IN_PROMOTED_SET in r.fired_sub_tags


class TestCrossOrgGrantPeriod:
    def test_cross_org_fires(self):
        m = _build_map_with_source(
            "orgs/otherorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("a",),
        )
        assert not r.success
        assert SUB_TAG_CROSS_ORG in r.fired_sub_tags

    def test_cross_grant_fires(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G2/period_1/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("a",),
        )
        assert not r.success
        assert SUB_TAG_CROSS_GRANT in r.fired_sub_tags

    def test_cross_period_without_sp0_fires(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_2/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("a",),
        )
        assert not r.success
        assert SUB_TAG_CROSS_PERIOD in r.fired_sub_tags

    def test_cross_period_with_sp0_passes(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_2/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=True,  # SP0 active
            scope_tag_extractor=lambda t: ("a",),
        )
        assert r.success or SUB_TAG_CROSS_PERIOD not in r.fired_sub_tags


class TestRuntimeScopeTagExtractionFailure:
    def test_extractor_raises_fires_advisory(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml"
        )
        def bad_extractor(t):
            raise RuntimeError("NER unavailable")
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=bad_extractor,
        )
        assert not r.success
        assert SUB_TAG_RUNTIME_SCOPE_TAG_EXTRACTION_FAILED in r.fired_sub_tags

    def test_extractor_returns_empty_fires(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: (),
        )
        assert not r.success
        assert SUB_TAG_RUNTIME_SCOPE_TAG_EXTRACTION_FAILED in r.fired_sub_tags


class TestBeneficiaryConsentTier:
    def test_no_narrative_in_narrative_fires(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("a",),
            beneficiary_consent_infos=(
                BeneficiaryConsentInfo(
                    beneficiary_id="b1", claim_id="C1",
                    consent_tier="no-narrative",
                    claim_sub_section="narrative",
                ),
            ),
        )
        assert not r.success
        assert SUB_TAG_BENEFICIARY_CONSENT_TIER_VIOLATION in r.fired_sub_tags

    def test_narrative_text_only_passes(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("a",),
            beneficiary_consent_infos=(
                BeneficiaryConsentInfo(
                    beneficiary_id="b1", claim_id="C1",
                    consent_tier="narrative-text-only",
                    claim_sub_section="narrative",
                ),
            ),
        )
        assert r.success


class TestPhotoConsentTier:
    def test_internal_only_in_gallery_fires(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("a",),
            photo_consent_infos=(
                PhotoConsentInfo(
                    photo_id="p1", consent_tier="internal_only",
                    referenced_in_sub_section="photo_gallery",
                ),
            ),
        )
        assert not r.success
        assert SUB_TAG_PHOTO_CONSENT_TIER_VIOLATION in r.fired_sub_tags

    def test_cross_section_funder_only_fires(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("a",),
            photo_consent_infos=(
                PhotoConsentInfo(
                    photo_id="p1", consent_tier="funder_only",
                    referenced_in_sub_section="narrative",
                ),
            ),
        )
        assert not r.success
        assert SUB_TAG_PHOTO_CONSENT_TIER_VIOLATION_CROSS_SECTION in r.fired_sub_tags


class TestAggregateIdentifying:
    def test_aggregate_count_le_threshold_without_signature_fires(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("a",),
            aggregate_references=(
                AggregateBeneficiaryCountReference(
                    claim_id="C1", aggregate_count=2,
                    operator_aggregate_signature_valid=False,
                ),
            ),
        )
        assert not r.success
        assert SUB_TAG_BENEFICIARY_AGGREGATE_IDENTIFYING in r.fired_sub_tags

    def test_aggregate_above_threshold_passes(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml"
        )
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("a",),
            aggregate_references=(
                AggregateBeneficiaryCountReference(
                    claim_id="C1", aggregate_count=AGGREGATE_IDENTIFYING_THRESHOLD + 1,
                    operator_aggregate_signature_valid=False,
                ),
            ),
        )
        assert r.success


class TestBeneficiaryPrivacyLeak:
    def test_name_match_in_narrative_fires(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml",
            claim_text="Jane Doe attended workshops.",
        )
        def name_dict():
            return {"b1": (("Jane Doe",), "metrics-only")}
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("a",),
            beneficiary_name_dictionary=name_dict,
        )
        assert not r.success
        assert SUB_TAG_BENEFICIARY_PRIVACY_LEAK in r.fired_sub_tags

    def test_narrative_text_only_tier_does_not_leak(self):
        m = _build_map_with_source(
            "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml",
            claim_text="Jane Doe attended workshops.",
        )
        def name_dict():
            return {"b1": (("Jane Doe",), "narrative-text-only")}
        r = check_out_of_scope_drift(
            claim_evidence_map=m,
            promoted_commitments=_prom("a"),
            report_grant_id="G1", report_org_slug="myorg", report_period_n=1,
            sp0_cross_period_authorized=False,
            scope_tag_extractor=lambda t: ("a",),
            beneficiary_name_dictionary=name_dict,
        )
        assert r.success
