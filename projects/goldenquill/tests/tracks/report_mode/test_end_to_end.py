"""Cross-composer integration tests for §14 Report Generator (WS-J Slice 3).

Per the WS-J §14 Slice 3 handoff (2026-05-11): end-to-end tests that
exercise the full pipeline shape:

* synthetic substrates injected via Protocol stubs,
* :func:`run_report_pipeline` → ``DRAFT_PENDING_OPERATOR_SIGN`` bundle,
* :func:`finalize_operator_signed_report` → ``FINALIZED`` bundle,
* adversarial probes (numeric drift, scope drift, template mismatch,
  post-sign mutation, Cedar deny).

The tests use deterministic stubs — no LLM, no real disk I/O. The
:class:`ReportPipelineDeps` bundle is constructed once per test fixture
and lightly mutated for adversarial cases.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Mapping, Optional

import pytest

from pipeline.logician.gates._report_protocols import (
    DraftIntegrityAtFinalize,
    PromotedCommitmentRow,
    ReportingTemplateSnapshot,
    SourceResolutionAtFinalize,
    WaiverRecord,
    WorkspacePublishedTemplateSnapshot,
)
from pipeline.logician.gates.f_report_numeric_drift import NumericClaimVsKfr
from pipeline.orchestrator.seats.report_generator._schemas import (
    BUNDLE_STATE_DRAFT_PENDING,
    BUNDLE_STATE_FINALIZED,
    OPERATOR_SIG_STATUS_PENDING,
    OPERATOR_SIG_STATUS_SIGNED,
    ClaimEntry,
    ClaimEvidenceMap,
    SourceRef,
)
from pipeline.orchestrator.seats.report_generator.claim_evidence_map import (
    assemble_claim_evidence_map,
    canonical_map_bytes,
)
from pipeline.orchestrator.tracks.report_mode import (
    FinalizeDeps,
    GrantReportBundle,
    JudgeVerdict,
    EditorVerdict,
    RedTeamVerdict,
    ReportGeneratorRunInput,
    ReportPipelineDeps,
    SubSectionComposerOutput,
    finalize_operator_signed_report,
    run_report_pipeline,
)


# ---------------------------------------------------------------------------
# Stub seats
# ---------------------------------------------------------------------------


class StubScribe:
    def compose_sub_section(self, **kwargs: Any) -> SubSectionComposerOutput:
        # Unused — the composer_dispatcher stub builds outputs directly.
        raise NotImplementedError("StubScribe.compose_sub_section unused in tests")


@dataclass
class StubEditor:
    success: bool = True
    detail: str = ""

    def review_sub_section(
        self, *, sub_section: str, draft: str, claims: tuple[ClaimEntry, ...]
    ) -> EditorVerdict:
        return EditorVerdict(success=self.success, detail=self.detail)


@dataclass
class StubJudge:
    success: bool = True
    score: int = 95
    detail: str = ""

    def score_sub_section(
        self,
        *,
        sub_section: str,
        draft: str,
        proposal_commitments_rubric: Any,
        funder_published_rubric: Any,
    ) -> JudgeVerdict:
        return JudgeVerdict(success=self.success, score=self.score, detail=self.detail)


@dataclass
class StubRedTeam:
    success: bool = True
    detail: str = ""

    def probe_sub_section(
        self, *, sub_section: str, draft: str, claims: tuple[ClaimEntry, ...]
    ) -> RedTeamVerdict:
        return RedTeamVerdict(success=self.success, detail=self.detail)


# ---------------------------------------------------------------------------
# Stub composer dispatcher
# ---------------------------------------------------------------------------


def _make_narrative_claims() -> tuple[ClaimEntry, ...]:
    return (
        ClaimEntry(
            claim_id="CLAIM-NARRATIVE-P0-S0-0001",
            sub_section="narrative",
            claim_text="The project delivered 100 deliverables on schedule.",
            claim_kind="narrative",
            sources=(
                SourceRef(
                    kind="operational_data",
                    sub_kind="narrative_entries",
                    source_path=(
                        "orgs/test_org/vault/operational/grants/test_grant/"
                        "period_1/narrative_entries/entry-001.yaml"
                    ),
                    source_row_id="entry-001",
                    source_content_sha3_512="a" * 128,
                ),
                # Link to COMMIT-001 so the F-REPORT-COMMITMENT-MISSED gate
                # sees narrative addressing the commitment.
                SourceRef(
                    kind="proposal_commitments",
                    commitment_id="COMMIT-001",
                    commitment_status="PROMOTED",
                    scope_tags_at_commitment=("workforce_development",),
                ),
            ),
        ),
    )


def _make_metrics_claims() -> tuple[ClaimEntry, ...]:
    return (
        ClaimEntry(
            claim_id="CLAIM-METRICS-TABLE-P0-S0-0001",
            sub_section="metrics_table",
            claim_text="participants_served=100",
            claim_kind="numeric",
            sources=(
                SourceRef(
                    kind="operational_data",
                    sub_kind="metrics",
                    source_path=(
                        "orgs/test_org/vault/operational/grants/test_grant/"
                        "period_1/metrics/row-001.yaml"
                    ),
                    source_row_id="row-001",
                    source_content_sha3_512="b" * 128,
                    source_value=Decimal("100"),
                ),
                # Link to COMMIT-001 so the F-REPORT-COMMITMENT-MISSED gate
                # sees the metrics_table sub-section addressed.
                SourceRef(
                    kind="proposal_commitments",
                    commitment_id="COMMIT-001",
                    commitment_status="PROMOTED",
                    scope_tags_at_commitment=("workforce_development",),
                ),
            ),
        ),
    )


_COMPOSER_FRAGMENTS: dict[str, str] = {
    "narrative": "The project delivered 100 deliverables on schedule.\n",
    "metrics_table": (
        "| metric_name | target | actual |\n"
        "|---|---|---|\n"
        "| participants_served | 100 | 100 |\n"
    ),
    "financial_summary": "All budget lines on track.\n",
    "photo_gallery": "(no photos this period)\n",
    "beneficiary_section": "5 beneficiaries served.\n",
}

_COMPOSER_CLAIMS: dict[str, tuple[ClaimEntry, ...]] = {
    "narrative": _make_narrative_claims(),
    "metrics_table": _make_metrics_claims(),
    "financial_summary": (),
    "photo_gallery": (),
    "beneficiary_section": (),
}


def stub_composer_dispatcher(
    *,
    sub_section: str,
    input: ReportGeneratorRunInput,
    proposal_commitments_promoted: tuple[PromotedCommitmentRow, ...],
    reporting_template: ReportingTemplateSnapshot,
    scribe: Any,
) -> SubSectionComposerOutput:
    return SubSectionComposerOutput(
        sub_section=sub_section,
        markdown_fragment=_COMPOSER_FRAGMENTS[sub_section],
        claims=_COMPOSER_CLAIMS[sub_section],
    )


# ---------------------------------------------------------------------------
# Stub loaders + assemblers
# ---------------------------------------------------------------------------


def _make_promoted_commitments() -> tuple[PromotedCommitmentRow, ...]:
    return (
        PromotedCommitmentRow(
            commitment_id="COMMIT-001",
            status="PROMOTED",
            scope_tags=("workforce_development", "training"),
            required_sub_sections=("narrative", "metrics_table"),
            evaluation_criteria=(
                {"field": "participants_served", "kind": "numeric"},
            ),
        ),
    )


def _make_reporting_template() -> ReportingTemplateSnapshot:
    return ReportingTemplateSnapshot(
        funder_id="VAPG",
        template_version="2026.1",
        template_captured_at_utc="2026-05-01T00:00:00Z",
        template_content_sha3_512="c" * 128,
        required_sub_sections=("narrative", "metrics_table"),
        required_fields_per_sub_section={
            "narrative": (
                {"field": "accomplishments_narrative"},
            ),
            "metrics_table": (
                {"field": "participants_served"},
            ),
        },
        required_period_cadence="quarterly",
        report_due_n_days_after_period_end=30,
    )


def stub_proposal_commitments_loader(
    *, path: str
) -> tuple[PromotedCommitmentRow, ...]:
    return _make_promoted_commitments()


def stub_reporting_template_loader(*, path: str) -> ReportingTemplateSnapshot:
    return _make_reporting_template()


def stub_workspace_published_loader_absent(
    *, funder_id: str, root: str
) -> Optional[WorkspacePublishedTemplateSnapshot]:
    """No workspace-published template. F-REPORT-TEMPLATE-MISMATCH downgrades
    to advisory for non-first-wave but fails-closed for first-wave funders.
    For VAPG this would normally FAIL. We use a non-first-wave funder for
    happy-path tests.
    """
    return None


def stub_workspace_published_loader_first_wave_valid(
    *, funder_id: str, root: str
) -> Optional[WorkspacePublishedTemplateSnapshot]:
    return WorkspacePublishedTemplateSnapshot(
        funder_id=funder_id,
        present=True,
        content_sha3_512="c" * 128,  # matches operator template
        first_wave=True,
        first_wave_marker_signature_valid=True,
        first_wave_marker_hash_bound_to_lock_history=True,
    )


def stub_waivers_loader(*, path: str) -> Mapping[str, WaiverRecord]:
    return {}


def stub_source_resolution_assembler(
    *,
    claim_evidence_map: ClaimEvidenceMap,
    input: ReportGeneratorRunInput,
) -> Mapping[tuple[str, int], SourceResolutionAtFinalize]:
    """Return resolutions matching every author-time source so the gate passes."""
    out: dict[tuple[str, int], SourceResolutionAtFinalize] = {}
    for claim in claim_evidence_map.claims:
        for idx, src in enumerate(claim.sources):
            out[(claim.claim_id, idx)] = SourceResolutionAtFinalize(
                claim_id=claim.claim_id,
                source_idx=idx,
                source_kind=src.kind,
                present=True,
                current_content_sha3_512=src.source_content_sha3_512,
                current_value=src.source_value,
                current_status=src.commitment_status,
                current_kfr_atomic_snapshot_id=src.kfr_atomic_snapshot_id,
            )
    return out


def stub_narrative_source_texts_assembler(
    *,
    claim_evidence_map: ClaimEvidenceMap,
    input: ReportGeneratorRunInput,
) -> Mapping[str, tuple[str, ...]]:
    """Return per-claim source texts that contain the claim text verbatim."""
    out: dict[str, tuple[str, ...]] = {}
    for claim in claim_evidence_map.claims:
        if claim.claim_kind == "narrative":
            # Provide a source text that contains the claim text verbatim.
            out[claim.claim_id] = (
                f"Background: {claim.claim_text} This is documented in the "
                "operational log.",
            )
    return out


def stub_draft_integrity_assembler_unchanged(captured_hash: dict[str, str]):
    """Returns an assembler that reports the draft hash unchanged."""

    def _assemble(*, draft_path: str, post_sign_read: bool) -> DraftIntegrityAtFinalize:
        return DraftIntegrityAtFinalize(
            draft_content_sha3_512_at_finalize=captured_hash["hash"],
            post_sign_read=post_sign_read,
        )

    return _assemble


def stub_draft_integrity_assembler_mutated(captured_hash: dict[str, str]):
    """Returns an assembler that reports a DRIFTED draft hash."""

    def _assemble(*, draft_path: str, post_sign_read: bool) -> DraftIntegrityAtFinalize:
        return DraftIntegrityAtFinalize(
            draft_content_sha3_512_at_finalize="f" * 128,
            post_sign_read=post_sign_read,
        )

    return _assemble


def stub_numeric_rows_assembler(
    *,
    claims: tuple[ClaimEntry, ...],
    input: ReportGeneratorRunInput,
) -> tuple[NumericClaimVsKfr, ...]:
    """Build NumericClaimVsKfr rows matching every numeric claim's value."""
    rows: list[NumericClaimVsKfr] = []
    for claim in claims:
        if claim.claim_kind != "numeric":
            continue
        for src in claim.sources:
            if src.source_value is None:
                continue
            assert isinstance(src.source_value, Decimal)
            rows.append(
                NumericClaimVsKfr(
                    claim_id=claim.claim_id,
                    field="participants_served",
                    claim_value=src.source_value,
                    kfr_value=src.source_value,  # exact match → no drift
                    kfr_field_present=True,
                    tolerance=Decimal("0"),
                )
            )
    return tuple(rows)


def stub_numeric_rows_assembler_drifted(
    *,
    claims: tuple[ClaimEntry, ...],
    input: ReportGeneratorRunInput,
) -> tuple[NumericClaimVsKfr, ...]:
    rows: list[NumericClaimVsKfr] = []
    for claim in claims:
        if claim.claim_kind != "numeric":
            continue
        for src in claim.sources:
            if src.source_value is None:
                continue
            assert isinstance(src.source_value, Decimal)
            rows.append(
                NumericClaimVsKfr(
                    claim_id=claim.claim_id,
                    field="participants_served",
                    claim_value=src.source_value,
                    kfr_value=Decimal("999"),  # massive drift
                    kfr_field_present=True,
                    tolerance=Decimal("0"),
                )
            )
    return tuple(rows)


def stub_scope_tag_extractor(claim_text: str) -> tuple[str, ...]:
    """Return scope tags that are all in the promoted set."""
    return ("workforce_development",)


def stub_scope_tag_extractor_out_of_scope(claim_text: str) -> tuple[str, ...]:
    """Return scope tags NOT in the promoted set."""
    return ("medical_research",)


@dataclass
class _Captured:
    drafts: dict[str, str] = field(default_factory=dict)
    maps: dict[str, bytes] = field(default_factory=dict)
    state: dict[str, dict] = field(default_factory=dict)
    sigs: dict[str, bytes] = field(default_factory=dict)
    locked_paths: list[str] = field(default_factory=list)
    captured_draft_hash: dict[str, str] = field(default_factory=dict)


def make_stub_writers(captured: _Captured):
    import hashlib

    def draft_writer(*, markdown: str, path: str) -> str:
        captured.drafts[path] = markdown
        digest = hashlib.sha3_512(markdown.encode("utf-8")).hexdigest()
        captured.captured_draft_hash["hash"] = digest
        return digest

    def map_writer(*, map_bytes: bytes, path: str) -> str:
        captured.maps[path] = map_bytes
        return hashlib.sha3_512(map_bytes).hexdigest()

    def state_writer(*, state_payload: dict, path: str) -> str:
        captured.state[path] = state_payload
        return path

    def operator_signature_writer(*, signed_yaml_bytes: bytes, path: str) -> str:
        captured.sigs[path] = signed_yaml_bytes
        return path

    def draft_post_sign_locker(*, draft_path: str) -> None:
        captured.locked_paths.append(draft_path)

    return (
        draft_writer,
        map_writer,
        state_writer,
        operator_signature_writer,
        draft_post_sign_locker,
    )


def stub_clock() -> str:
    return "2026-05-15T12:00:00Z"


def stub_hash_bytes(data: bytes) -> str:
    import hashlib

    return hashlib.sha3_512(data).hexdigest()


def stub_ed25519_signer(message_bytes: bytes) -> bytes:
    """Deterministic stub signer — returns SHA3-512 prefix as a 64-byte sig."""
    import hashlib

    return hashlib.sha3_512(b"stub-signer|" + message_bytes).digest()[:64]


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _make_input(sub_sections: tuple[str, ...] = ("narrative", "metrics_table")) -> ReportGeneratorRunInput:
    return ReportGeneratorRunInput(
        run_id="run-001",
        org_slug="test_org",
        grant_id="test_grant",
        period_n=1,
        proposal_commitments_path="/dev/null/proposal_commitments.yaml",
        reporting_template_path="/dev/null/reporting_template.yaml",
        operational_data_root="/dev/null/operational/",
        kfr_register_path="/dev/null/kfr/register.yaml",
        funder_intelligence_root="/dev/null/funder_intelligence/",
        benchmarks_root="/dev/null/benchmarks/",
        sub_sections_in_scope=sub_sections,
        trend_narrative_authorized=False,
        invoked_at_utc="2026-05-15T11:59:59Z",
    )


def _make_deps(
    captured: _Captured,
    *,
    editor: StubEditor = None,
    judge: StubJudge = None,
    red_team: StubRedTeam = None,
    workspace_published_loader=None,
    numeric_rows_assembler=stub_numeric_rows_assembler,
    scope_tag_extractor=stub_scope_tag_extractor,
    source_resolution_assembler=stub_source_resolution_assembler,
    narrative_source_texts_assembler=stub_narrative_source_texts_assembler,
) -> ReportPipelineDeps:
    (
        draft_writer,
        map_writer,
        state_writer,
        operator_signature_writer,
        draft_post_sign_locker,
    ) = make_stub_writers(captured)
    if workspace_published_loader is None:
        workspace_published_loader = stub_workspace_published_loader_first_wave_valid
    return ReportPipelineDeps(
        scribe=StubScribe(),
        editor=editor or StubEditor(),
        judge=judge or StubJudge(),
        red_team=red_team or StubRedTeam(),
        composer_dispatcher=stub_composer_dispatcher,
        proposal_commitments_loader=stub_proposal_commitments_loader,
        reporting_template_loader=stub_reporting_template_loader,
        workspace_published_loader=workspace_published_loader,
        waivers_loader=stub_waivers_loader,
        source_resolution_assembler=source_resolution_assembler,
        narrative_source_texts_assembler=narrative_source_texts_assembler,
        draft_integrity_assembler=stub_draft_integrity_assembler_unchanged(
            captured.captured_draft_hash
        ),
        numeric_rows_assembler=numeric_rows_assembler,
        scope_tag_extractor=scope_tag_extractor,
        draft_writer=draft_writer,
        claim_evidence_map_writer=map_writer,
        state_writer=state_writer,
        operator_signature_writer=operator_signature_writer,
        draft_post_sign_locker=draft_post_sign_locker,
        clock=stub_clock,
        hash_bytes=stub_hash_bytes,
        actual_period_cadence_months=3,
    )


# ---------------------------------------------------------------------------
# Tests — happy path round trip
# ---------------------------------------------------------------------------


class TestHappyPathRoundTrip:
    def test_run_pipeline_returns_draft_pending_bundle(self) -> None:
        captured = _Captured()
        deps = _make_deps(captured)
        input = _make_input()

        result = run_report_pipeline(input, deps=deps)

        assert result.cycle_completed is True, result.failure_reason
        assert result.bundle.bundle_state == BUNDLE_STATE_DRAFT_PENDING
        assert result.bundle.operator_signature_status == OPERATOR_SIG_STATUS_PENDING
        assert result.bundle.operator_signature == ""
        assert result.bundle.sub_sections_authored == (
            "narrative",
            "metrics_table",
        )
        assert "COMMIT-001" in result.bundle.proposal_commitments_consumed
        # State file written on success
        assert result.state_file_path
        assert result.state_file_path in captured.state
        assert captured.state[result.state_file_path]["cycle_completed"] is True

    def test_draft_written_to_vault(self) -> None:
        captured = _Captured()
        deps = _make_deps(captured)
        result = run_report_pipeline(_make_input(), deps=deps)

        assert result.bundle.draft_path
        assert result.bundle.draft_path in captured.drafts
        draft_md = captured.drafts[result.bundle.draft_path]
        assert "## narrative" in draft_md
        assert "## metrics_table" in draft_md

    def test_claim_evidence_map_written_pending(self) -> None:
        captured = _Captured()
        deps = _make_deps(captured)
        result = run_report_pipeline(_make_input(), deps=deps)

        assert result.bundle.claim_evidence_map_path
        assert result.bundle.claim_evidence_map_path in captured.maps
        # Map bytes are canonical JSON; should parse to a dict containing
        # operator_signature_status=PENDING_OPERATOR_REVIEW (per
        # canonical_map_bytes which includes signature fields).
        import json

        map_data = json.loads(captured.maps[result.bundle.claim_evidence_map_path])
        assert map_data["operator_signature_status"] == OPERATOR_SIG_STATUS_PENDING

    def test_finalize_promotes_to_finalized(self) -> None:
        captured = _Captured()
        deps = _make_deps(captured)
        result = run_report_pipeline(_make_input(), deps=deps)
        assert result.cycle_completed is True

        # Reconstruct the unsigned map from the captured bytes
        import json

        map_data = json.loads(captured.maps[result.bundle.claim_evidence_map_path])
        # We need the actual ClaimEvidenceMap dataclass for finalize.
        # Easier: invoke assemble_claim_evidence_map directly with the
        # same claims.
        all_claims = []
        for sub_section in result.bundle.sub_sections_authored:
            all_claims.extend(_COMPOSER_CLAIMS[sub_section])
        pending_map = assemble_claim_evidence_map(
            run_id=result.bundle.run_id,
            org_slug=result.bundle.org_slug,
            grant_id=result.bundle.grant_id,
            period_n=result.bundle.period_n,
            draft_path=result.bundle.draft_path,
            draft_version=result.bundle.draft_version,
            draft_content_sha3_512=captured.captured_draft_hash["hash"],
            authored_at_utc=stub_clock(),
            authored_by_seat="report_generator.scribe",
            claims=tuple(all_claims),
        )

        finalize_deps = FinalizeDeps(
            ed25519_signer=stub_ed25519_signer,
            source_resolution_assembler=stub_source_resolution_assembler,
            narrative_source_texts_assembler=stub_narrative_source_texts_assembler,
            draft_integrity_assembler=stub_draft_integrity_assembler_unchanged(
                captured.captured_draft_hash
            ),
            draft_post_sign_locker=deps.draft_post_sign_locker,
            operator_signature_writer=deps.operator_signature_writer,
            hash_bytes=stub_hash_bytes,
            clock=stub_clock,
        )

        finalized = finalize_operator_signed_report(
            bundle=result.bundle,
            claim_evidence_map=pending_map,
            input=_make_input(),
            deps=finalize_deps,
        )

        assert finalized.cycle_completed is True, finalized.failure_reason
        assert finalized.bundle.bundle_state == BUNDLE_STATE_FINALIZED
        assert (
            finalized.bundle.operator_signature_status == OPERATOR_SIG_STATUS_SIGNED
        )
        assert finalized.bundle.operator_signature  # non-empty hex
        assert finalized.bundle.finalized_at_utc
        # Post-sign immutability — locker recorded the draft path
        assert result.bundle.draft_path in captured.locked_paths
        # operator_signature.signed.yaml companion record written
        assert any(
            p.endswith("operator_signature.signed.yaml")
            for p in captured.sigs
        )


# ---------------------------------------------------------------------------
# Tests — adversarial paths
# ---------------------------------------------------------------------------


class TestAdversarialGates:
    def test_numeric_drift_fails_pipeline(self) -> None:
        captured = _Captured()
        deps = _make_deps(
            captured,
            numeric_rows_assembler=stub_numeric_rows_assembler_drifted,
        )
        result = run_report_pipeline(_make_input(), deps=deps)
        assert result.cycle_completed is False
        assert "F-REPORT-NUMERIC-DRIFT" in result.failure_reason

    def test_out_of_scope_drift_fails_pipeline(self) -> None:
        captured = _Captured()
        deps = _make_deps(
            captured,
            scope_tag_extractor=stub_scope_tag_extractor_out_of_scope,
        )
        result = run_report_pipeline(_make_input(), deps=deps)
        assert result.cycle_completed is False
        assert "F-REPORT-OUT-OF-SCOPE-DRIFT" in result.failure_reason

    def test_editor_rejection_fails_pipeline(self) -> None:
        captured = _Captured()
        deps = _make_deps(
            captured,
            editor=StubEditor(success=False, detail="too jargony"),
        )
        result = run_report_pipeline(_make_input(), deps=deps)
        assert result.cycle_completed is False
        assert "Editor rejected" in result.failure_reason

    def test_judge_rejection_fails_pipeline(self) -> None:
        captured = _Captured()
        deps = _make_deps(
            captured,
            judge=StubJudge(success=False, score=40, detail="below threshold"),
        )
        result = run_report_pipeline(_make_input(), deps=deps)
        assert result.cycle_completed is False
        assert "Judge rejected" in result.failure_reason

    def test_red_team_rejection_fails_pipeline(self) -> None:
        captured = _Captured()
        deps = _make_deps(
            captured,
            red_team=StubRedTeam(success=False, detail="commitment unaddressed"),
        )
        result = run_report_pipeline(_make_input(), deps=deps)
        assert result.cycle_completed is False
        assert "Red Team flagged" in result.failure_reason

    def test_state_writer_fires_on_failure(self) -> None:
        """Per Rule 1: state file written on success AND failure."""
        captured = _Captured()
        deps = _make_deps(
            captured,
            numeric_rows_assembler=stub_numeric_rows_assembler_drifted,
        )
        result = run_report_pipeline(_make_input(), deps=deps)
        assert result.cycle_completed is False
        assert result.state_file_path
        assert captured.state[result.state_file_path]["cycle_completed"] is False

    def test_post_sign_mutation_blocks_finalize(self) -> None:
        captured = _Captured()
        deps = _make_deps(captured)
        result = run_report_pipeline(_make_input(), deps=deps)
        assert result.cycle_completed is True

        all_claims = []
        for sub_section in result.bundle.sub_sections_authored:
            all_claims.extend(_COMPOSER_CLAIMS[sub_section])
        pending_map = assemble_claim_evidence_map(
            run_id=result.bundle.run_id,
            org_slug=result.bundle.org_slug,
            grant_id=result.bundle.grant_id,
            period_n=result.bundle.period_n,
            draft_path=result.bundle.draft_path,
            draft_version=result.bundle.draft_version,
            draft_content_sha3_512=captured.captured_draft_hash["hash"],
            authored_at_utc=stub_clock(),
            authored_by_seat="report_generator.scribe",
            claims=tuple(all_claims),
        )

        # Mutated draft integrity reports a drifted hash.
        finalize_deps = FinalizeDeps(
            ed25519_signer=stub_ed25519_signer,
            source_resolution_assembler=stub_source_resolution_assembler,
            narrative_source_texts_assembler=stub_narrative_source_texts_assembler,
            draft_integrity_assembler=stub_draft_integrity_assembler_mutated(
                captured.captured_draft_hash
            ),
            draft_post_sign_locker=deps.draft_post_sign_locker,
            operator_signature_writer=deps.operator_signature_writer,
            hash_bytes=stub_hash_bytes,
            clock=stub_clock,
        )

        finalized = finalize_operator_signed_report(
            bundle=result.bundle,
            claim_evidence_map=pending_map,
            input=_make_input(),
            deps=finalize_deps,
        )
        assert finalized.cycle_completed is False
        # Cedar verdict surfaces the F-REPORT-COMMITMENT-UNTRACED failure;
        # the failure_sub_tag includes .draft_post_sign_mutation_attempt
        assert ".draft_post_sign_mutation_attempt" in finalized.failure_sub_tag


class TestCedarEnforcement:
    def test_cedar_deny_on_commitment_untraced(self) -> None:
        """If a claim has no resolution, F-REPORT-COMMITMENT-UNTRACED fires
        and the Cedar evaluator DENIES the finalize action."""
        captured = _Captured()

        def empty_resolutions(**kwargs):
            return {}

        deps = _make_deps(
            captured,
            source_resolution_assembler=empty_resolutions,
        )
        result = run_report_pipeline(_make_input(), deps=deps)
        assert result.cycle_completed is False
        assert "F-REPORT-COMMITMENT-UNTRACED" in result.failure_reason


# ---------------------------------------------------------------------------
# Tests — track-mode constants + first-wave binding
# ---------------------------------------------------------------------------


class TestTrackModeConstants:
    def test_pipeline_shape_constant(self) -> None:
        from pipeline.orchestrator.tracks import report_mode

        assert (
            report_mode.REPORT_MODE_PIPELINE_SHAPE
            == "prior_commitments_to_council_to_signed_report"
        )

    def test_version_family_constant(self) -> None:
        from pipeline.orchestrator.tracks import report_mode

        assert report_mode.TILTH_VERSION_FAMILY == "v0.2"

    def test_first_wave_marker_binding_callable(self) -> None:
        """RT-C2-04 — the binding accessor is reachable and returns a Mapping."""
        from pipeline.orchestrator.tracks import report_mode

        binding = report_mode.get_first_wave_marker_binding_at_first_activation()
        assert isinstance(binding, Mapping)
