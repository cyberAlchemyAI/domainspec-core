"""Tests for ``pipeline.logician.gates.f_report_commitment_untraced``.

Per §14.9.1 Cycle 1 + Cycle 2 closures (RT-1a/1b/1c + RT-6c + RT-7b
+ RT-8b + RT-C2-09/10). Run-all-then-collect verdict per §14.9.0 +
RT-10a closure.
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from pipeline.logician.gates._report_protocols import (
    CaptionResolutionAtFinalize,
    DraftIntegrityAtFinalize,
    PriorPeriodMapIntegrity,
    SourceResolutionAtFinalize,
)
from pipeline.logician.gates.f_report_commitment_untraced import (
    F_REPORT_COMMITMENT_UNTRACED,
    SUB_TAG_BENEFICIARY_REFERENCE_CONSENT_TIER_UNVERIFIED,
    SUB_TAG_COMMITMENT_ID_NOT_PROMOTED,
    SUB_TAG_CROSS_PERIOD_SIGNATURE_INVALID,
    SUB_TAG_DRAFT_POST_SIGN_MUTATION_ATTEMPT,
    SUB_TAG_KFR_SOURCE_CANONICAL_DRIFT,
    SUB_TAG_NARRATIVE_CLAIM_NO_NARRATIVE_SOURCE,
    SUB_TAG_NARRATIVE_PARAPHRASE_UNFLAGGED,
    SUB_TAG_PRIOR_PERIOD_MAP_INTEGRITY_FAILURE,
    SUB_TAG_SOURCE_CONTENT_DRIFT,
    SUB_TAG_SOURCE_VALUE_DRIFT,
    check_commitment_untraced,
)
from pipeline.orchestrator.seats.report_generator._schemas import (
    ClaimEntry,
    SourceRef,
)
from pipeline.orchestrator.seats.report_generator.claim_evidence_map import (
    assemble_claim_evidence_map,
)


def _build_simple_map():
    src = SourceRef(
        kind="operational_data",
        sub_kind="metrics",
        source_path="orgs/myorg/vault/operational/grants/G1/period_1/metrics/x.yaml",
        source_row_id="r1",
        source_content_sha3_512="a" * 128,
        source_value=Decimal("50"),
    )
    claim = ClaimEntry(
        claim_id="CLAIM-001",
        sub_section="metrics_table",
        claim_text="50 workshops",
        claim_kind="numeric",
        sources=(src,),
    )
    return assemble_claim_evidence_map(
        run_id="r", org_slug="myorg", grant_id="G1", period_n=1,
        draft_path="d", draft_version=1, draft_content_sha3_512="f" * 128,
        authored_at_utc="now", authored_by_seat="scribe", claims=(claim,),
    )


def _good_resolution():
    return SourceResolutionAtFinalize(
        claim_id="CLAIM-001",
        source_idx=0,
        source_kind="operational_data",
        present=True,
        current_content_sha3_512="a" * 128,
        current_value=Decimal("50"),
    )


def _good_draft_integrity(post_sign=False):
    return DraftIntegrityAtFinalize(
        draft_content_sha3_512_at_finalize="f" * 128,
        post_sign_read=post_sign,
    )


class TestHappyPath:
    def test_clean_map_passes(self):
        m = _build_simple_map()
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("CLAIM-001", 0): _good_resolution()},
            narrative_source_texts={},
            caption_resolutions={},
            draft_integrity=_good_draft_integrity(),
        )
        assert r.success
        assert r.findings == ()


class TestContentDrift:
    def test_content_hash_mismatch_fires(self):
        m = _build_simple_map()
        drifted = SourceResolutionAtFinalize(
            claim_id="CLAIM-001", source_idx=0, source_kind="operational_data",
            present=True, current_content_sha3_512="b" * 128, current_value=Decimal("50"),
        )
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("CLAIM-001", 0): drifted},
            narrative_source_texts={},
            caption_resolutions={},
            draft_integrity=_good_draft_integrity(),
        )
        assert not r.success
        assert SUB_TAG_SOURCE_CONTENT_DRIFT in r.fired_sub_tags

    def test_source_not_readable_fires_content_drift(self):
        m = _build_simple_map()
        unreadable = SourceResolutionAtFinalize(
            claim_id="CLAIM-001", source_idx=0, source_kind="operational_data",
            present=False, read_error="FileNotFoundError",
        )
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("CLAIM-001", 0): unreadable},
            narrative_source_texts={},
            caption_resolutions={},
            draft_integrity=_good_draft_integrity(),
        )
        assert not r.success
        assert SUB_TAG_SOURCE_CONTENT_DRIFT in r.fired_sub_tags


class TestSourceValueDrift:
    def test_numeric_value_mismatch_fires(self):
        m = _build_simple_map()
        drifted = SourceResolutionAtFinalize(
            claim_id="CLAIM-001", source_idx=0, source_kind="operational_data",
            present=True, current_content_sha3_512="a" * 128, current_value=Decimal("51"),
        )
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("CLAIM-001", 0): drifted},
            narrative_source_texts={},
            caption_resolutions={},
            draft_integrity=_good_draft_integrity(),
        )
        assert not r.success
        assert SUB_TAG_SOURCE_VALUE_DRIFT in r.fired_sub_tags

    def test_float_in_value_path_fires_drift(self):
        # Force a non-Decimal in the numeric source path.
        src = SourceRef(
            kind="operational_data", sub_kind="metrics",
            source_path="orgs/myorg/vault/operational/grants/G1/period_1/metrics/x.yaml",
            source_row_id="r1", source_content_sha3_512="a" * 128,
            source_value="50",  # str instead of Decimal — defense fires
        )
        claim = ClaimEntry(
            claim_id="CLAIM-001", sub_section="metrics_table",
            claim_text="50", claim_kind="numeric", sources=(src,),
        )
        m = assemble_claim_evidence_map(
            run_id="r", org_slug="myorg", grant_id="G1", period_n=1,
            draft_path="d", draft_version=1, draft_content_sha3_512="f" * 128,
            authored_at_utc="now", authored_by_seat="scribe", claims=(claim,),
        )
        resolution = SourceResolutionAtFinalize(
            claim_id="CLAIM-001", source_idx=0, source_kind="operational_data",
            present=True, current_content_sha3_512="a" * 128, current_value=Decimal("50"),
        )
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("CLAIM-001", 0): resolution},
            narrative_source_texts={},
            caption_resolutions={},
            draft_integrity=_good_draft_integrity(),
        )
        assert not r.success
        assert SUB_TAG_SOURCE_VALUE_DRIFT in r.fired_sub_tags


class TestKfrAtomicSnapshot:
    def test_kfr_snapshot_drift_fires(self):
        src = SourceRef(
            kind="kfr", source_path="orgs/myorg/vault/kfr/register.yaml",
            source_row_id="r1", source_content_sha3_512="a" * 128,
            kfr_atomic_snapshot_id="snap-1", source_value=Decimal("50"),
        )
        claim = ClaimEntry(
            claim_id="C", sub_section="metrics_table",
            claim_text="x", claim_kind="numeric", sources=(src,),
        )
        m = assemble_claim_evidence_map(
            run_id="r", org_slug="myorg", grant_id="G1", period_n=1,
            draft_path="d", draft_version=1, draft_content_sha3_512="f" * 128,
            authored_at_utc="now", authored_by_seat="scribe", claims=(claim,),
        )
        resolution = SourceResolutionAtFinalize(
            claim_id="C", source_idx=0, source_kind="kfr",
            present=True, current_content_sha3_512="a" * 128,
            current_value=Decimal("50"), current_kfr_atomic_snapshot_id="snap-2",
        )
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("C", 0): resolution},
            narrative_source_texts={},
            caption_resolutions={},
            draft_integrity=_good_draft_integrity(),
        )
        assert not r.success
        assert SUB_TAG_KFR_SOURCE_CANONICAL_DRIFT in r.fired_sub_tags


class TestProposalCommitmentStatus:
    def test_commitment_not_promoted_at_finalize_fires(self):
        src = SourceRef(
            kind="proposal_commitments",
            commitment_id="COMMIT-001",
            commitment_status="PROMOTED",
            scope_tags_at_commitment=("a",),
        )
        claim = ClaimEntry(
            claim_id="C", sub_section="narrative", claim_text="x",
            claim_kind="narrative", sources=(src,),
        )
        m = assemble_claim_evidence_map(
            run_id="r", org_slug="myorg", grant_id="G1", period_n=1,
            draft_path="d", draft_version=1, draft_content_sha3_512="f" * 128,
            authored_at_utc="now", authored_by_seat="scribe", claims=(claim,),
        )
        resolution = SourceResolutionAtFinalize(
            claim_id="C", source_idx=0, source_kind="proposal_commitments",
            present=True, current_status="RETIRED",
        )
        # narrative entailment match prevents .narrative_paraphrase_unflagged here
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("C", 0): resolution},
            narrative_source_texts={"C": ("x text body",)},
            caption_resolutions={},
            draft_integrity=_good_draft_integrity(),
        )
        assert not r.success
        assert SUB_TAG_COMMITMENT_ID_NOT_PROMOTED in r.fired_sub_tags


class TestDraftPostSignMutation:
    def test_draft_drift_at_post_sign_read_fires(self):
        m = _build_simple_map()
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("CLAIM-001", 0): _good_resolution()},
            narrative_source_texts={},
            caption_resolutions={},
            draft_integrity=DraftIntegrityAtFinalize(
                draft_content_sha3_512_at_finalize="e" * 128, post_sign_read=True,
            ),
        )
        assert not r.success
        assert SUB_TAG_DRAFT_POST_SIGN_MUTATION_ATTEMPT in r.fired_sub_tags

    def test_pre_sign_drift_does_not_fire(self):
        m = _build_simple_map()
        # post_sign_read=False means we're in the PRE-pre-finalize stage
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("CLAIM-001", 0): _good_resolution()},
            narrative_source_texts={},
            caption_resolutions={},
            draft_integrity=DraftIntegrityAtFinalize(
                draft_content_sha3_512_at_finalize="e" * 128, post_sign_read=False,
            ),
        )
        # Should pass — pre-sign drift is not a violation
        assert r.success or SUB_TAG_DRAFT_POST_SIGN_MUTATION_ATTEMPT not in r.fired_sub_tags


class TestPriorPeriodIntegrity:
    def test_sp0_signature_invalid_fires(self):
        m = _build_simple_map()
        prior = PriorPeriodMapIntegrity(
            prior_period_n=0,
            map_path="d",
            sp0_signature_valid=False,
            map_content_sha3_512_matches_signature_record=True,
            sources_all_under_same_org_slug=True,
        )
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("CLAIM-001", 0): _good_resolution()},
            narrative_source_texts={},
            caption_resolutions={},
            draft_integrity=_good_draft_integrity(),
            prior_period_integrity=prior,
        )
        assert not r.success
        assert SUB_TAG_CROSS_PERIOD_SIGNATURE_INVALID in r.fired_sub_tags

    def test_prior_period_map_tamper_fires(self):
        m = _build_simple_map()
        prior = PriorPeriodMapIntegrity(
            prior_period_n=0,
            map_path="d",
            sp0_signature_valid=True,
            map_content_sha3_512_matches_signature_record=False,
            sources_all_under_same_org_slug=True,
        )
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("CLAIM-001", 0): _good_resolution()},
            narrative_source_texts={},
            caption_resolutions={},
            draft_integrity=_good_draft_integrity(),
            prior_period_integrity=prior,
        )
        assert not r.success
        assert SUB_TAG_PRIOR_PERIOD_MAP_INTEGRITY_FAILURE in r.fired_sub_tags


class TestNarrativeEntailment:
    def test_unflagged_paraphrase_fires(self):
        src = SourceRef(
            kind="operational_data", sub_kind="narrative_entries",
            source_path="orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml",
            source_row_id="r1", source_content_sha3_512="a" * 128,
        )
        claim = ClaimEntry(
            claim_id="C", sub_section="narrative",
            claim_text="The project pivoted to virtual delivery in Q3.",
            claim_kind="narrative", sources=(src,),
        )
        m = assemble_claim_evidence_map(
            run_id="r", org_slug="myorg", grant_id="G1", period_n=1,
            draft_path="d", draft_version=1, draft_content_sha3_512="f" * 128,
            authored_at_utc="now", authored_by_seat="scribe", claims=(claim,),
        )
        resolution = SourceResolutionAtFinalize(
            claim_id="C", source_idx=0, source_kind="operational_data",
            present=True, current_content_sha3_512="a" * 128,
        )
        # Source text completely unrelated — no verbatim match, no paraphrase flag
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("C", 0): resolution},
            narrative_source_texts={"C": ("we built a barn.",)},
            caption_resolutions={},
            draft_integrity=_good_draft_integrity(),
        )
        assert not r.success
        assert SUB_TAG_NARRATIVE_PARAPHRASE_UNFLAGGED in r.fired_sub_tags

    def test_verbatim_match_passes(self):
        src = SourceRef(
            kind="operational_data", sub_kind="narrative_entries",
            source_path="orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/n.yaml",
            source_row_id="r1", source_content_sha3_512="a" * 128,
        )
        claim = ClaimEntry(
            claim_id="C", sub_section="narrative",
            claim_text="50 workshops delivered",
            claim_kind="narrative", sources=(src,),
        )
        m = assemble_claim_evidence_map(
            run_id="r", org_slug="myorg", grant_id="G1", period_n=1,
            draft_path="d", draft_version=1, draft_content_sha3_512="f" * 128,
            authored_at_utc="now", authored_by_seat="scribe", claims=(claim,),
        )
        resolution = SourceResolutionAtFinalize(
            claim_id="C", source_idx=0, source_kind="operational_data",
            present=True, current_content_sha3_512="a" * 128,
        )
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("C", 0): resolution},
            narrative_source_texts={"C": ("Field notes: 50 workshops delivered to farmers.",)},
            caption_resolutions={},
            draft_integrity=_good_draft_integrity(),
        )
        assert r.success


class TestRunAllThenCollect:
    def test_multiple_findings_collected(self):
        """RT-10a closure — gate collects every fired sub-tag, not first-fired-returns."""
        m = _build_simple_map()
        drifted = SourceResolutionAtFinalize(
            claim_id="CLAIM-001", source_idx=0, source_kind="operational_data",
            present=True, current_content_sha3_512="b" * 128, current_value=Decimal("51"),
        )
        r = check_commitment_untraced(
            claim_evidence_map=m,
            source_resolutions={("CLAIM-001", 0): drifted},
            narrative_source_texts={},
            caption_resolutions={},
            draft_integrity=DraftIntegrityAtFinalize(
                draft_content_sha3_512_at_finalize="e" * 128, post_sign_read=True,
            ),
        )
        assert not r.success
        # Should have at least: source_content_drift + source_value_drift + post_sign_mutation
        sub_tags = set(r.fired_sub_tags)
        assert SUB_TAG_SOURCE_CONTENT_DRIFT in sub_tags
        assert SUB_TAG_SOURCE_VALUE_DRIFT in sub_tags
        assert SUB_TAG_DRAFT_POST_SIGN_MUTATION_ATTEMPT in sub_tags
        assert r.failure_code == F_REPORT_COMMITMENT_UNTRACED
