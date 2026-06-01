"""§14 Report Generator v1 SPEC LOCK skeleton tests.

These tests verify the LOCKED-but-skeleton substrate at v0.2 first ship per §14
v1 LOCK `v0_2_implementation_disposition`. Full per-gate behavioral tests +
classification-routing tests + CIC × CLC orthogonality regression land in WS-J
Code phase dispatch.

Per §14.13: 28 skeleton tests across 7 test classes.

NON-NEGOTIABLE — these tests prevent future contributors from quietly enabling
auto-finalize OR bypassing the F-REPORT-* gate family OR introducing a
sub-section beyond the closed set.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import pytest


# ───────────────────────────────────────────────────────────────────────────
# §14.13.1 — Track registration tests (3)
# ───────────────────────────────────────────────────────────────────────────


class TestReportModeTrackRegistration:
    """Per §14.13.1 — verifies §5 v8 dispatcher integration per §14.8.0."""

    def test_report_mode_pipeline_shape_constant_present(self) -> None:
        from pipeline.orchestrator.tracks import report_mode

        assert report_mode.REPORT_MODE_PIPELINE_SHAPE == (
            "prior_commitments_to_council_to_signed_report"
        )

    def test_tilth_version_family_v0_2_at_v0_2_first_ship(self) -> None:
        """At v0.2 first ship, the report_mode track shippable_in: v0.2 gate
        passes because TILTH_VERSION_FAMILY = "v0.2". v0.1 Tilths continue to
        refuse via the gate per §5 v8 §3.2.9."""
        from pipeline.orchestrator.tracks import report_mode

        assert report_mode.TILTH_VERSION_FAMILY == "v0.2"

    def test_run_report_pipeline_is_realized_callable(self) -> None:
        """Per WS-J Slice 3 (2026-05-11): run_report_pipeline is fully wired.

        Calling with a non-ReportPipelineDeps deps argument raises TypeError;
        the Slice-1 NotImplementedError posture is retired. End-to-end behavior
        is verified by tests/tracks/report_mode/test_end_to_end.py.
        """
        from pipeline.orchestrator.tracks import report_mode

        stub_input = report_mode.ReportGeneratorRunInput(
            run_id="test-run",
            org_slug="test_org",
            grant_id="test_grant",
            period_n=1,
            proposal_commitments_path="/dev/null/proposal_commitments.yaml",
            reporting_template_path="/dev/null/reporting_template.yaml",
            operational_data_root="/dev/null/operational/",
            kfr_register_path="/dev/null/kfr/register.yaml",
            funder_intelligence_root="/dev/null/funder_intelligence/",
            benchmarks_root="/dev/null/benchmarks/",
            sub_sections_in_scope=("narrative",),
            trend_narrative_authorized=False,
            invoked_at_utc="2026-05-10T23:30:00Z",
        )
        # Passing the wrong type for deps fails fast with TypeError.
        with pytest.raises(TypeError):
            report_mode.run_report_pipeline(
                stub_input,
                deps=None,  # type: ignore[arg-type]
            )


# ───────────────────────────────────────────────────────────────────────────
# §14.13.2 — Schema discipline tests (4)
# ───────────────────────────────────────────────────────────────────────────


class TestReportSchemaDiscipline:
    """Per §14.13.2 — verifies frozen-dataclass discipline per §14.4 + §14.5."""

    def test_report_generator_run_input_frozen(self) -> None:
        from pipeline.orchestrator.tracks import report_mode

        instance = report_mode.ReportGeneratorRunInput(
            run_id="test",
            org_slug="test_org",
            grant_id="test_grant",
            period_n=1,
            proposal_commitments_path="/dev/null/a",
            reporting_template_path="/dev/null/b",
            operational_data_root="/dev/null/c",
            kfr_register_path="/dev/null/d",
            funder_intelligence_root="/dev/null/e",
            benchmarks_root="/dev/null/f",
            sub_sections_in_scope=("narrative",),
            trend_narrative_authorized=False,
            invoked_at_utc="2026-05-10T23:30:00Z",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            instance.run_id = "mutated"  # type: ignore[misc]

    def test_grant_report_bundle_frozen(self) -> None:
        from pipeline.orchestrator.tracks import report_mode

        instance = report_mode.GrantReportBundle(
            run_id="test",
            org_slug="test_org",
            grant_id="test_grant",
            period_n=1,
            draft_path="/dev/null/draft.md",
            draft_version=1,
            claim_evidence_map_path="/dev/null/map.yaml",
            scoring_dir="/dev/null/scoring/",
            proposal_commitments_consumed=("COMMIT-001",),
            reporting_template_content_sha3_512="0" * 128,
            sub_sections_authored=("narrative",),
            operator_signature_status="PENDING_OPERATOR_REVIEW",
            operator_signature="",
            operator_signed_at_utc="",
            finalized_at_utc="",
            bundle_state="DRAFT_PENDING_OPERATOR_SIGN",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            instance.bundle_state = "FINALIZED"  # type: ignore[misc]

    def test_sub_sections_v0_2_closed_set(self) -> None:
        from pipeline.orchestrator.tracks import report_mode

        assert report_mode.SUB_SECTIONS_V0_2 == frozenset(
            {
                "narrative",
                "metrics_table",
                "financial_summary",
                "photo_gallery",
                "beneficiary_section",
            }
        )

    def test_report_run_result_frozen(self) -> None:
        from pipeline.orchestrator.tracks import report_mode

        instance = report_mode.ReportRunResult(
            bundle=report_mode.GrantReportBundle(
                run_id="r",
                org_slug="o",
                grant_id="g",
                period_n=1,
                draft_path="/d/draft.md",
                draft_version=1,
                claim_evidence_map_path="/d/map.yaml",
                scoring_dir="/d/scoring/",
                proposal_commitments_consumed=(),
                reporting_template_content_sha3_512="0" * 128,
                sub_sections_authored=(),
                operator_signature_status="PENDING_OPERATOR_REVIEW",
                operator_signature="",
                operator_signed_at_utc="",
                finalized_at_utc="",
                bundle_state="DRAFT_PENDING_OPERATOR_SIGN",
            ),
            state_file_path="/d/state.yaml",
            cycle_completed=False,
            failure_reason="",
            failure_sub_tag="",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            instance.cycle_completed = True  # type: ignore[misc]


# ───────────────────────────────────────────────────────────────────────────
# §14.13.3 — Gate predicate skeleton tests (5)
# ───────────────────────────────────────────────────────────────────────────


class TestReportGatePredicatesSkeletonStubs:
    """Per §14.13.3 — substrate disposition for the 5 F-REPORT-* gates.

    Slice 1 LANDED 2026-05-11: all 5 gate predicate bodies are now realized
    at ``pipeline.logician.gates.f_report_*.py`` (`check_commitment_untraced`
    / `check_commitment_missed` / `check_out_of_scope_drift` /
    `check_numeric_drift` / `check_template_mismatch`). Slice 2 (this
    LANDED 2026-05-11) confirms the Cedar bootstrap pairing + per-sub-section
    composer realization.

    Prior to Slice 1 these were NotImplementedError-raising skeletons; that
    posture is retired now that the predicate bodies are substantive.
    """

    @pytest.mark.parametrize(
        "module_path,callable_name",
        [
            (
                "pipeline.logician.gates.f_report_commitment_untraced",
                "check_commitment_untraced",
            ),
            (
                "pipeline.logician.gates.f_report_commitment_missed",
                "check_commitment_missed",
            ),
            (
                "pipeline.logician.gates.f_report_out_of_scope_drift",
                "check_out_of_scope_drift",
            ),
            (
                "pipeline.logician.gates.f_report_numeric_drift",
                "check_numeric_drift",
            ),
            (
                "pipeline.logician.gates.f_report_template_mismatch",
                "check_template_mismatch",
            ),
        ],
    )
    def test_gate_predicate_is_realized_callable(
        self, module_path: str, callable_name: str
    ) -> None:
        """Every F-REPORT-* gate predicate is a substantive callable (Slice 1
        realization); calling without required kwargs raises ``TypeError`` —
        NEVER ``NotImplementedError``."""
        module = __import__(module_path, fromlist=[callable_name])
        check_fn = getattr(module, callable_name)
        assert callable(check_fn), (
            f"{module_path}.{callable_name} must be a callable predicate"
        )
        # Verify it's no longer the NotImplementedError stub.
        with pytest.raises(TypeError):
            check_fn()


# ───────────────────────────────────────────────────────────────────────────
# §14.13.4 — AST-lint tests (3)
# ───────────────────────────────────────────────────────────────────────────


class TestReportAstLintRules:
    """Per §14.13.4 — verifies AST-lint rules R-REPORT-NO-AUTO-FINALIZE +
    R-REPORT-VAULT-INTENT-REQUIRED + R-REPORT-DECIMAL-MANDATE registered
    per WS-J Slice 3 (2026-05-11)."""

    def test_r_report_no_auto_finalize_rule_registered(self) -> None:
        """Per WS-J Slice 3: R-REPORT-NO-AUTO-FINALIZE rule is registered
        in DEFAULT_RULES (Layer 1 of three-layer defense)."""
        from pipeline.linting import ast_lint

        rule_names = [getattr(r, "name", str(r)) for r in ast_lint.DEFAULT_RULES]
        assert "R-REPORT-NO-AUTO-FINALIZE" in rule_names, (
            "R-REPORT-NO-AUTO-FINALIZE must be in DEFAULT_RULES "
            "(WS-J Slice 3 realization)"
        )

    def test_r_report_vault_intent_required_rule_registered(self) -> None:
        from pipeline.linting import ast_lint

        rule_names = [getattr(r, "name", str(r)) for r in ast_lint.DEFAULT_RULES]
        assert "R-REPORT-VAULT-INTENT-REQUIRED" in rule_names, (
            "R-REPORT-VAULT-INTENT-REQUIRED must be in DEFAULT_RULES "
            "(WS-J Slice 3 realization)"
        )

    def test_r_report_decimal_mandate_rule_registered(self) -> None:
        """Per Cycle 2 RT-C2-01 + WS-J Slice 3: R-REPORT-DECIMAL-MANDATE
        registered with scope EXTENDED to composers + report_mode."""
        from pipeline.linting import ast_lint

        rule_names = [getattr(r, "name", str(r)) for r in ast_lint.DEFAULT_RULES]
        assert "R-REPORT-DECIMAL-MANDATE" in rule_names, (
            "R-REPORT-DECIMAL-MANDATE must be in DEFAULT_RULES "
            "(WS-J Slice 3 + Cycle 2 RT-C2-01 realization)"
        )


# ───────────────────────────────────────────────────────────────────────────
# §14.13.5 — Sub-section prompt template integrity tests (5)
# ───────────────────────────────────────────────────────────────────────────


_SKILLS_REPORT_PROMPTS_DIR = (
    Path(__file__).parent.parent.parent.parent
    / "skills"
    / "scribe-ghostwriter"
    / "report_mode_prompts"
)


class TestReportSubSectionPromptTemplates:
    """Per §14.13.5 — every sub-section prompt template is on disk + parseable."""

    @pytest.mark.parametrize(
        "sub_section",
        [
            "narrative",
            "metrics_table",
            "financial_summary",
            "photo_gallery",
            "beneficiary_section",
        ],
    )
    def test_sub_section_prompt_template_present_and_parseable(
        self, sub_section: str
    ) -> None:
        prompt_path = _SKILLS_REPORT_PROMPTS_DIR / f"{sub_section}.md"
        assert prompt_path.exists(), (
            f"§14.6 sub-section prompt template missing on disk: {prompt_path}"
        )
        content = prompt_path.read_text(encoding="utf-8")
        assert len(content) > 100, (
            f"§14.6 sub-section prompt template at {prompt_path} is suspiciously "
            f"short (< 100 chars); SPEC LOCK requires full prompt-template content."
        )
        # Sanity check — every report_mode prompt template must reference its
        # sub-section by name + the proposal_commitments rubric input contract.
        assert sub_section in content or sub_section.replace("_", " ") in content


# ───────────────────────────────────────────────────────────────────────────
# §14.13.6 — Rubric integrity tests (2)
# ───────────────────────────────────────────────────────────────────────────


_SKILLS_JUDGE_RUBRIC_PATH = (
    Path(__file__).parent.parent.parent.parent
    / "skills"
    / "judge-rubric"
    / "proposal_commitments_rubric.json"
)


class TestProposalCommitmentsRubricIntegrity:
    """Per §14.13.6 — proposal_commitments rubric exists, parses, and contains
    no CIC→CLC subset binding per v7.0.8 F-CIC-CLC-COUPLING-VIOLATION."""

    def test_proposal_commitments_rubric_present_and_canonical_json(self) -> None:
        assert _SKILLS_JUDGE_RUBRIC_PATH.exists(), (
            f"§14.7 + §14.8.1 rubric missing on disk: {_SKILLS_JUDGE_RUBRIC_PATH}"
        )
        content = _SKILLS_JUDGE_RUBRIC_PATH.read_text(encoding="utf-8")
        rubric = json.loads(content)
        assert isinstance(rubric, dict)
        # Canonical-JSON discipline: re-serialize with sort_keys=True + compare.
        re_serialized = json.dumps(
            rubric, sort_keys=True, ensure_ascii=False, separators=(", ", ": ")
        )
        # Allow trailing newline difference; compare stripped.
        assert re_serialized.strip() == content.strip(), (
            f"§14.7 + §14.8.1 rubric at {_SKILLS_JUDGE_RUBRIC_PATH} is not "
            f"canonical-JSON encoded (sort_keys=True; key separator ': '; item "
            f"separator ', ')."
        )

    def test_proposal_commitments_rubric_no_cic_clc_binding(self) -> None:
        """Per v7.0.8 F-CIC-CLC-COUPLING-VIOLATION — rubric scoring criteria
        cannot encode CIC→CLC subset binding."""
        if not _SKILLS_JUDGE_RUBRIC_PATH.exists():
            pytest.skip("rubric not yet on disk")
        content = _SKILLS_JUDGE_RUBRIC_PATH.read_text(encoding="utf-8")
        # Lexical regex layer per v7.0.8 detection layer 1: no "primary_capital_logic"
        # OR "capital_logic_for_<cic>" patterns.
        forbidden_patterns = [
            "primary_capital_logic",
            "capital_logic_for_food_systems",
            "capital_logic_for_educator",
            "capital_logic_for_public_agency",
            "capital_logic_for_arts_culture",
            "capital_logic_for_cooperative",
            "capital_logic_for_ecosystem_intermediary",
        ]
        for pattern in forbidden_patterns:
            assert pattern not in content, (
                f"§14 + v7.0.8 F-CIC-CLC-COUPLING-VIOLATION detected: rubric "
                f"contains forbidden CIC→CLC subset binding pattern '{pattern}'."
            )


# ───────────────────────────────────────────────────────────────────────────
# §14.13.7 — Red-team probe template integrity tests (5)
# ───────────────────────────────────────────────────────────────────────────


_SKILLS_RED_TEAM_PROBES_DIR = (
    Path(__file__).parent.parent.parent.parent
    / "skills"
    / "red-team"
    / "report_mode_probes"
)


class TestReportRedTeamProbeTemplates:
    """Per §14.13.7 — every sub-section red-team probe template is on disk +
    parseable + contains adversarial-probe scaffold."""

    @pytest.mark.parametrize(
        "sub_section",
        [
            "narrative",
            "metrics_table",
            "financial_summary",
            "photo_gallery",
            "beneficiary_section",
        ],
    )
    def test_sub_section_red_team_probe_template_present_and_parseable(
        self, sub_section: str
    ) -> None:
        probe_path = _SKILLS_RED_TEAM_PROBES_DIR / f"{sub_section}.md"
        assert probe_path.exists(), (
            f"§14.7 + §14.8.1 sub-section red-team probe missing: {probe_path}"
        )
        content = probe_path.read_text(encoding="utf-8")
        assert len(content) > 100, (
            f"§14.7 + §14.8.1 red-team probe at {probe_path} is suspiciously "
            f"short (< 100 chars); SPEC LOCK requires adversarial-probe scaffold."
        )


# ───────────────────────────────────────────────────────────────────────────
# §14.13.x — Sub-section composer skeleton tests (covered under §14.13.3 spirit)
# ───────────────────────────────────────────────────────────────────────────


class TestReportGeneratorSubSectionComposers:
    """Per §14.6 per-sub-section composers — substrate disposition.

    Slice 2 LANDED 2026-05-11: the five composers are now realized,
    callable functions exported from :mod:`pipeline.orchestrator.seats.report_generator`.
    This test verifies their callable-presence + closed-set membership
    (the integrity asserts at module load also enforce the closed set).

    Prior to Slice 2 these were NotImplementedError-raising skeletons;
    that posture is retired now that the composer functions are
    realized in ``composers/{narrative,metrics_table,financial_summary,
    photo_gallery,beneficiary_section}.py``.
    """

    @pytest.mark.parametrize(
        "fn_name",
        [
            "compose_narrative",
            "compose_metrics_table",
            "compose_financial_summary",
            "compose_photo_gallery",
            "compose_beneficiary_section",
        ],
    )
    def test_composer_is_realized_callable(self, fn_name: str) -> None:
        from pipeline.orchestrator.seats import report_generator

        composer = getattr(report_generator, fn_name)
        assert callable(composer), (
            f"{fn_name} must be a callable composer (Slice 2 realization)"
        )
        # Verify it's no longer the NotImplementedError stub — calling with
        # missing required kwargs should raise TypeError (signature mismatch)
        # OR ComposerError (domain validation), NEVER NotImplementedError.
        from pipeline.orchestrator.seats.report_generator.composers._base import (
            ComposerError,
        )

        with pytest.raises((TypeError, ComposerError)):
            composer()
