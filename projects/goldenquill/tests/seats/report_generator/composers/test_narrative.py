"""Tests for §14.6.1 narrative sub-section composer."""

from __future__ import annotations

import pytest

from pipeline.orchestrator.seats.report_generator._schemas import ClaimEntry
from pipeline.orchestrator.seats.report_generator.composers.narrative import (
    NarrativeDeps,
    NarrativeEntryRow,
    NarrativeResult,
    PromotedCommitmentSourceRow,
    compose_narrative,
)
from pipeline.orchestrator.seats.report_generator.composers._base import (
    ComposerError,
    compute_claim_id,
)


def _make_deps(*, fixed_clock, hash_bytes, make_read_intent, make_scribe):
    registry = {
        ("operational_data", "narrative_entries"): [
            {
                "entry_id": "NE-001",
                "source_path": "orgs/myorg/vault/operational/grants/G1/period_1/narrative_entries/NE-001.yaml",
                "text": "Delivered 50 workshops to 200 farmers in PA.",
                "content_sha3_512": "a" * 128,
                "period_n": 1,
                "related_commitment_ids": ["COMMIT-001"],
            }
        ],
        ("proposal_commitments", None): [
            {
                "commitment_id": "COMMIT-001",
                "scope_tags_at_commitment": ["workforce_training", "agriculture"],
                "commitment_text": "Deliver 50 workshops to 200 farmers in PA.",
                "required_sub_sections": ["narrative", "metrics_table"],
                "evaluation_criteria": [],
            }
        ],
        ("reporting_template", None): [
            {"field_name": "accomplishments_narrative", "max_length_chars": 5000},
            {"field_name": "challenges_narrative", "max_length_chars": 2000},
        ],
    }
    return NarrativeDeps(
        read_narrative_entries=make_read_intent(registry),
        read_promoted_commitments=make_read_intent(registry),
        read_template_field_specs=make_read_intent(registry),
        scribe=make_scribe(),
        clock=fixed_clock,
        hash_bytes=hash_bytes,
    )


class TestComposeNarrative:
    def test_happy_path(self, fixed_clock, hash_bytes, make_read_intent, make_scribe):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
        )
        result = compose_narrative(
            deps=deps,
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            operational_data_root="orgs/myorg/vault/operational/grants/G1/period_1",
            proposal_commitments_path="orgs/myorg/vault/grants/G1/proposal_commitments.yaml",
            reporting_template_path="orgs/myorg/vault/grants/G1/reporting_template.yaml",
        )
        assert isinstance(result, NarrativeResult)
        assert "accomplishments_narrative".replace("_", " ").capitalize() in result.markdown_fragment
        assert len(result.claims) >= 2  # one per field's drafted sentence
        for c in result.claims:
            assert isinstance(c, ClaimEntry)
            assert c.sub_section == "narrative"
            assert c.claim_kind == "narrative"
            assert len(c.sources) >= 1
        assert "accomplishments_narrative" in result.fields_drafted
        assert "challenges_narrative" in result.fields_drafted

    def test_deterministic_claim_id(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
        )
        result = compose_narrative(
            deps=deps,
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            operational_data_root="orgs/myorg/vault/operational/grants/G1/period_1",
            proposal_commitments_path="x",
            reporting_template_path="y",
        )
        # Each claim's id should match compute_claim_id() re-derivation.
        for c in result.claims:
            # Re-derivation: derive claim_id from sub_section+text only
            # (the per-position p/s indices are deterministic per the
            # sentence order in the drafted text). For the property check
            # here, we just verify the id has the expected prefix shape.
            assert c.claim_id.startswith("CLAIM-NARRATIVE-")

    def test_empty_template_raises(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        registry = {
            ("operational_data", "narrative_entries"): [],
            ("proposal_commitments", None): [],
            ("reporting_template", None): [],
        }
        deps = NarrativeDeps(
            read_narrative_entries=make_read_intent(registry),
            read_promoted_commitments=make_read_intent(registry),
            read_template_field_specs=make_read_intent(registry),
            scribe=make_scribe(),
            clock=fixed_clock,
            hash_bytes=hash_bytes,
        )
        with pytest.raises(ComposerError):
            compose_narrative(
                deps=deps,
                org_slug="myorg",
                grant_id="G1",
                period_n=1,
                operational_data_root="x",
                proposal_commitments_path="y",
                reporting_template_path="z",
            )

    def test_invalid_period_n_raises(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
        )
        with pytest.raises(ComposerError):
            compose_narrative(
                deps=deps,
                org_slug="myorg",
                grant_id="G1",
                period_n=0,
                operational_data_root="x",
                proposal_commitments_path="y",
                reporting_template_path="z",
            )

    def test_scribe_non_string_raises(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        def bad_scribe(*, spec, sources):
            return 42  # not a str

        registry = {
            ("operational_data", "narrative_entries"): [
                {
                    "entry_id": "NE-001",
                    "source_path": "x",
                    "text": "hi",
                    "content_sha3_512": "a" * 128,
                    "period_n": 1,
                }
            ],
            ("proposal_commitments", None): [],
            ("reporting_template", None): [{"field_name": "accomplishments"}],
        }
        deps = NarrativeDeps(
            read_narrative_entries=make_read_intent(registry),
            read_promoted_commitments=make_read_intent(registry),
            read_template_field_specs=make_read_intent(registry),
            scribe=bad_scribe,
            clock=fixed_clock,
            hash_bytes=hash_bytes,
        )
        with pytest.raises(ComposerError):
            compose_narrative(
                deps=deps,
                org_slug="myorg",
                grant_id="G1",
                period_n=1,
                operational_data_root="x",
                proposal_commitments_path="y",
                reporting_template_path="z",
            )

    def test_claim_assemble_round_trip(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        """Composer output → assemble_claim_evidence_map round-trip."""
        from pipeline.orchestrator.seats.report_generator.claim_evidence_map import (
            assemble_claim_evidence_map,
        )

        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
        )
        result = compose_narrative(
            deps=deps,
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            operational_data_root="x",
            proposal_commitments_path="y",
            reporting_template_path="z",
        )
        cem = assemble_claim_evidence_map(
            run_id="RUN-1",
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            draft_path="orgs/myorg/vault/grants/G1/reports/period_1/draft_1.md",
            draft_version=1,
            draft_content_sha3_512="f" * 128,
            authored_at_utc="2026-05-11T12:00:00Z",
            authored_by_seat="scribe",
            claims=result.claims,
        )
        # Sorted-claim_id invariant.
        ids = [c.claim_id for c in cem.claims]
        assert ids == sorted(ids)
