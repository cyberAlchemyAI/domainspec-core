"""
Z-Rig Orchestrator — Core Pipeline Unit Tests

Tests cover:
1. Config validation (run_config + task_description)
2. Mode classification (MECH-003, MECH-031)
3. Gate evaluation (G0, G1, G2, G3)
4. Pipeline bounds enforcement (MECH-021)
5. Failure routing
6. Manifest lifecycle
7. Full pipeline execution with default executor
8. Wave state machine transitions
"""

from __future__ import annotations

import asyncio
import json
import sys
import tempfile
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from zrig.config import (
    ConfigValidationError,
    FamilyRegistry,
    Mode,
    PipelineBounds,
    RunConfig,
    StakesLevel,
    TaskDescription,
    VerifierKind,
)
from zrig.classifier import classify_task, micro_eligible, mode_select
from zrig.gates import (
    GateEvaluation,
    GateResult,
    evaluate_g0,
    evaluate_g1,
    evaluate_g2,
    evaluate_g3,
    evaluate_gate,
)
from zrig.manifest import (
    LoopCounters,
    RunManifest,
    RunStatus,
    WaveRecord,
    WaveStatus,
)
from zrig.pipeline import (
    FailureAction,
    FailureRoute,
    Pipeline,
    PipelineResult,
    WaveState,
    check_pipeline_exhaustion,
    route_failure,
    run_pipeline,
)


# ---------------------------------------------------------------------------
# Fixtures — Minimal valid configs
# ---------------------------------------------------------------------------

def _minimal_run_config_dict(**overrides) -> dict:
    base = {
        "run_id": "HRR-TEST-001",
        "mode": "STANDARD",
        "artifact_type": "python-module",
        "artifact_domain_tags": ["orchestration"],
        "stakes_level": "routine",
        "scope_ambiguity": "none",
        "deterministic_metric_defined": True,
        "deterministic_metric_id": "pytest-pass-rate",
        "provider_list": ["anthropic", "openai", "google"],
        "w1_panel_size": 5,
        "w2_builder_count": 3,
        "w4_verifier_count": 3,
        "w5_squad_count": 2,
        "w9_panel_size": 5,
        "max_rework_cycles": 2,
        "human_escalation_timeout_ms": 86400000,
        "custom_timeouts": {},
        "custom_bounds": {},
        "deployment_config": {},
        "allowed_model_failover_map": {},
        "ignored_generated_files": [],
    }
    base.update(overrides)
    return base


def _minimal_task_dict(**overrides) -> dict:
    base = {
        "task_id": "TASK-001",
        "summary": "Implement core pipeline module",
        "requested_change": "Create pipeline.py with wave state machine",
        "acceptance_criteria": ["All waves execute", "Gates evaluate correctly"],
        "artifact_type": "python-module",
        "artifact_domain_tags": ["orchestration"],
        "stakes_level": "routine",
        "scope_ambiguity": "none",
        "target_files": ["src/pipeline.py"],
        "public_interface_impact": {
            "changes_public_surface": False,
            "surface_types": ["none"],
        },
        "deterministic_verifier": {
            "kind": "frozen_test_suite",
            "identifier": "pytest",
            "command_or_dispatch_key": "pytest tests/",
            "frozen_before_run": True,
            "coverage_of_changed_scope": 0.95,
        },
        "reversibility": {
            "fully_reversible": True,
            "requires_migration": False,
            "requires_cleanup": False,
        },
        "deployment_side_effects": "none",
        "security_relevance": {
            "is_security_relevant": False,
            "is_safety_relevant": False,
            "is_compliance_relevant": False,
        },
    }
    base.update(overrides)
    return base


def _make_config(**overrides) -> RunConfig:
    return RunConfig.from_dict(_minimal_run_config_dict(**overrides))


def _make_task(**overrides) -> TaskDescription:
    return TaskDescription.from_dict(_minimal_task_dict(**overrides))


def _make_registry() -> FamilyRegistry:
    return FamilyRegistry.default()


# Shared registry instance for deterministic hashing across tests
_SHARED_REGISTRY = FamilyRegistry.default()
_SHARED_REGISTRY_HASH = _SHARED_REGISTRY.compute_hash()


def _make_manifest(
    run_config: RunConfig | None = None,
    mode: Mode = Mode.STANDARD,
) -> RunManifest:
    rc = run_config or _make_config()
    return RunManifest.create(rc, mode, _SHARED_REGISTRY_HASH)


# ---------------------------------------------------------------------------
# Test 1: Config Validation
# ---------------------------------------------------------------------------

class TestConfigValidation:
    """Test run_config.json and task_description.json validation."""

    def test_valid_run_config(self):
        rc = _make_config()
        assert rc.run_id == "HRR-TEST-001"
        assert rc.mode == Mode.STANDARD
        assert len(rc.provider_list) == 3

    def test_invalid_run_id_rejected(self):
        with pytest.raises(ConfigValidationError) as exc_info:
            _make_config(run_id="INVALID-NO-HRR")
        assert any("run_id" in e for e in exc_info.value.errors)

    def test_missing_required_field(self):
        data = _minimal_run_config_dict()
        del data["mode"]
        with pytest.raises(ConfigValidationError):
            RunConfig.from_dict(data)

    def test_invalid_mode_rejected(self):
        with pytest.raises(ConfigValidationError):
            _make_config(mode="INVALID")

    def test_valid_task_description(self):
        task = _make_task()
        assert task.task_id == "TASK-001"
        assert task.stakes_level == StakesLevel.ROUTINE

    def test_micro_mode_requires_extra_fields(self):
        """MICRO mode requires changed_files_predicted etc."""
        with pytest.raises(ConfigValidationError) as exc_info:
            _make_config(mode="MICRO")
        # Should fail because MICRO-specific fields are missing
        assert any("MICRO" in e or "changed_files" in e for e in exc_info.value.errors)

    def test_micro_mode_with_all_fields(self):
        rc = _make_config(
            mode="MICRO",
            changed_files_predicted=1,
            lines_changed_predicted=50,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
        )
        assert rc.mode == Mode.MICRO

    def test_pipeline_bounds_defaults(self):
        bounds = PipelineBounds()
        assert bounds.max_w2_reruns == 2
        assert bounds.max_w5_reruns == 2
        assert bounds.total_pipeline_timeout_ms == 86_400_000

    def test_pipeline_bounds_custom(self):
        bounds = PipelineBounds.from_custom({"max_w2_reruns": 5})
        assert bounds.max_w2_reruns == 5
        assert bounds.max_w5_reruns == 2  # unchanged default


# ---------------------------------------------------------------------------
# Test 2: Mode Classification (MECH-003, MECH-031)
# ---------------------------------------------------------------------------

class TestModeClassification:
    """Test MECH-003 MODE_SELECT and MECH-031 MICRO_ELIGIBLE."""

    def test_standard_mode_passthrough(self):
        rc = _make_config(mode="STANDARD")
        task = _make_task()
        result = mode_select(rc, task)
        assert result.selected_mode == Mode.STANDARD
        assert not result.auto_escalated

    def test_full_mode_passthrough(self):
        rc = _make_config(mode="FULL")
        task = _make_task()
        result = mode_select(rc, task)
        assert result.selected_mode == Mode.FULL

    def test_micro_eligible_all_clauses_pass(self):
        rc = _make_config(
            mode="MICRO",
            changed_files_predicted=1,
            lines_changed_predicted=50,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
            deterministic_metric_defined=True,
        )
        task = _make_task()
        result = micro_eligible(task, rc)
        assert result.eligible is True
        assert result.scope_ok is True
        assert result.stakes_ok is True
        assert result.security_ok is True
        assert result.deterministic_ok is True
        assert result.coverage_ok is True

    def test_micro_eligible_3_files_300_lines(self):
        """MECH-031 HRR-005: ≤3 files and ≤300 lines should pass scope."""
        rc = _make_config(
            mode="MICRO",
            changed_files_predicted=3,
            lines_changed_predicted=300,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
            deterministic_metric_defined=True,
        )
        task = _make_task(target_files=["a.py", "b.py", "c.py"])
        result = micro_eligible(task, rc)
        assert result.scope_ok is True
        assert result.eligible is True

    def test_micro_fails_over_3_files(self):
        """MECH-031 HRR-005: >3 files should fail deterministic check."""
        rc = _make_config(
            mode="MICRO",
            changed_files_predicted=4,
            lines_changed_predicted=100,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
            deterministic_metric_defined=True,
        )
        task = _make_task(target_files=["a.py", "b.py", "c.py", "d.py"])
        result = micro_eligible(task, rc)
        assert result.scope_ok is False  # 4 > 3
        assert result.eligible is False

    def test_micro_fails_over_300_lines(self):
        """MECH-031 HRR-005: >300 lines should fail scope check."""
        rc = _make_config(
            mode="MICRO",
            changed_files_predicted=1,
            lines_changed_predicted=301,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
            deterministic_metric_defined=True,
        )
        task = _make_task()
        result = micro_eligible(task, rc)
        assert result.scope_ok is False
        assert result.eligible is False

    def test_micro_fails_on_critical_stakes(self):
        rc = _make_config(
            mode="MICRO",
            stakes_level="critical",
            changed_files_predicted=1,
            lines_changed_predicted=50,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
        )
        task = _make_task(stakes_level="critical")
        result = micro_eligible(task, rc)
        assert result.eligible is False
        assert result.stakes_ok is False

    def test_micro_fails_on_security_relevant(self):
        rc = _make_config(
            mode="MICRO",
            changed_files_predicted=1,
            lines_changed_predicted=50,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
        )
        task = _make_task(security_relevance={
            "is_security_relevant": True,
            "is_safety_relevant": False,
            "is_compliance_relevant": False,
        })
        result = micro_eligible(task, rc)
        assert result.eligible is False
        assert result.security_ok is False

    def test_micro_auto_escalation_to_standard(self):
        """MECH-003: Micro fails eligibility on scope → auto-escalate to Standard."""
        rc = _make_config(
            mode="MICRO",
            stakes_level="routine",
            changed_files_predicted=10,  # Too many files for micro
            lines_changed_predicted=50,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
        )
        task = _make_task()
        result = mode_select(rc, task)
        assert result.selected_mode == Mode.STANDARD
        assert result.auto_escalated is True
        assert result.failure_event is not None
        assert result.failure_event["fm_id"] == "FM-MICRO-MISUSE"

    def test_micro_auto_escalation_to_full_on_critical(self):
        """MECH-003 HRR-005: Micro fails + critical stakes → escalate to FULL."""
        rc = _make_config(
            mode="MICRO",
            stakes_level="critical",
            changed_files_predicted=1,
            lines_changed_predicted=50,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
        )
        task = _make_task(stakes_level="critical")
        result = mode_select(rc, task)
        # Should go all the way to FULL, not just STANDARD
        assert result.selected_mode == Mode.FULL
        assert result.auto_escalated is True
        assert result.failure_event is not None
        assert result.failure_event["fm_id"] == "FM-MICRO-MISUSE"
        assert result.failure_event["escalated_to"] == "FULL"

    def test_micro_coverage_fail_closed(self):
        """MECH-031: null coverage → fail-closed for frozen_test_suite."""
        rc = _make_config(
            mode="MICRO",
            changed_files_predicted=1,
            lines_changed_predicted=50,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
        )
        task = _make_task()
        # Set coverage to None
        task.deterministic_verifier.coverage_of_changed_scope = None
        result = micro_eligible(task, rc)
        assert result.eligible is False
        assert result.coverage_ok is False

    # -----------------------------------------------------------------------
    # AUTO Mode Tests (HRR-005)
    # -----------------------------------------------------------------------

    def test_auto_mode_accepted_by_config(self):
        """AUTO is a valid mode in config validation."""
        rc = _make_config(mode="AUTO")
        assert rc.mode == Mode.AUTO

    def test_auto_selects_micro_when_eligible(self):
        """AUTO mode: micro-eligible task → MICRO."""
        rc = _make_config(
            mode="AUTO",
            changed_files_predicted=1,
            lines_changed_predicted=50,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
            deterministic_metric_defined=True,
        )
        task = _make_task()
        result = mode_select(rc, task)
        assert result.selected_mode == Mode.MICRO
        assert result.recommended_mode == Mode.MICRO
        assert not result.auto_escalated

    def test_auto_selects_standard_default(self):
        """AUTO mode: non-micro, routine task → STANDARD."""
        rc = _make_config(mode="AUTO")
        task = _make_task()
        result = mode_select(rc, task)
        assert result.selected_mode == Mode.STANDARD
        assert result.recommended_mode == Mode.STANDARD

    def test_auto_escalates_to_full_on_critical_stakes(self):
        """AUTO mode: critical stakes → FULL."""
        rc = _make_config(mode="AUTO", stakes_level="critical")
        task = _make_task(stakes_level="critical")
        result = mode_select(rc, task)
        assert result.selected_mode == Mode.FULL
        assert result.recommended_mode == Mode.FULL
        assert result.auto_escalated is True
        assert "critical" in result.escalation_reason.lower()

    def test_auto_escalates_to_full_on_patent(self):
        """AUTO mode: patent artifact → FULL."""
        rc = _make_config(mode="AUTO", artifact_type="patent")
        task = _make_task(artifact_type="patent")
        result = mode_select(rc, task)
        assert result.selected_mode == Mode.FULL
        assert result.auto_escalated is True

    def test_auto_escalates_to_full_on_irreversible_high_ambiguity(self):
        """AUTO mode: irreversible deployment + high ambiguity → FULL."""
        rc = _make_config(mode="AUTO", scope_ambiguity="high")
        task = _make_task(
            deployment_side_effects="irreversible",
            scope_ambiguity="high",
        )
        result = mode_select(rc, task)
        assert result.selected_mode == Mode.FULL
        assert result.auto_escalated is True
        assert "irreversible" in result.escalation_reason.lower()

    def test_auto_standard_minimum_on_security_public_interface(self):
        """AUTO mode: security-relevant + public interface → STANDARD minimum."""
        rc = _make_config(
            mode="AUTO",
            changed_files_predicted=1,
            lines_changed_predicted=50,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
            deterministic_metric_defined=True,
        )
        task = _make_task(
            security_relevance={
                "is_security_relevant": True,
                "is_safety_relevant": False,
                "is_compliance_relevant": False,
            },
            public_interface_impact={
                "changes_public_surface": True,
                "surface_types": ["api"],
            },
        )
        result = mode_select(rc, task)
        # Should be at least STANDARD, not MICRO, even if micro_eligible passes some checks
        assert result.selected_mode in (Mode.STANDARD, Mode.FULL)
        assert result.selected_mode != Mode.MICRO

    # -----------------------------------------------------------------------
    # Advisory Warning Tests (HRR-005)
    # -----------------------------------------------------------------------

    def test_standard_config_with_critical_task_warns(self):
        """STANDARD config + critical task → advisory warns about FULL."""
        rc = _make_config(mode="STANDARD", stakes_level="critical")
        task = _make_task(stakes_level="critical")
        result = mode_select(rc, task)
        assert result.selected_mode == Mode.STANDARD  # Honors explicit config
        assert result.recommended_mode == Mode.FULL
        assert result.advisory is not None
        assert "FULL" in result.advisory
        assert "STANDARD" in result.advisory

    def test_standard_config_with_patent_task_warns(self):
        """STANDARD config + patent artifact → advisory warns about FULL."""
        rc = _make_config(mode="STANDARD", artifact_type="patent")
        task = _make_task(artifact_type="patent")
        result = mode_select(rc, task)
        assert result.selected_mode == Mode.STANDARD  # Honors explicit config
        assert result.recommended_mode == Mode.FULL
        assert result.advisory is not None
        assert "FULL" in result.advisory

    def test_full_config_with_routine_task_info(self):
        """FULL config + routine task → informational advisory."""
        rc = _make_config(mode="FULL")
        task = _make_task()
        result = mode_select(rc, task)
        assert result.selected_mode == Mode.FULL  # Honors explicit config
        # Recommended should be STANDARD (routine task)
        assert result.recommended_mode == Mode.STANDARD
        assert result.advisory is not None
        assert "STANDARD" in result.advisory

    def test_standard_config_matching_analysis_no_warning(self):
        """STANDARD config + routine task → no advisory (they agree)."""
        rc = _make_config(mode="STANDARD")
        task = _make_task()
        result = mode_select(rc, task)
        assert result.selected_mode == Mode.STANDARD
        assert result.recommended_mode == Mode.STANDARD
        assert result.advisory is None

    # -----------------------------------------------------------------------
    # classify_task() standalone tests (HRR-005)
    # -----------------------------------------------------------------------

    def test_classify_task_routine_recommends_standard(self):
        """classify_task: routine task with no micro fields → STANDARD."""
        rc = _make_config(mode="AUTO")
        task = _make_task()
        classification = classify_task(rc, task)
        assert classification.recommended_mode == Mode.STANDARD

    def test_classify_task_critical_recommends_full(self):
        """classify_task: critical stakes → FULL."""
        rc = _make_config(mode="AUTO", stakes_level="critical")
        task = _make_task(stakes_level="critical")
        classification = classify_task(rc, task)
        assert classification.recommended_mode == Mode.FULL
        assert len(classification.escalation_reasons) > 0

    def test_classify_task_patent_recommends_full(self):
        """classify_task: patent artifact → FULL."""
        rc = _make_config(mode="AUTO")
        task = _make_task(artifact_type="patent")
        classification = classify_task(rc, task)
        assert classification.recommended_mode == Mode.FULL

    def test_classify_task_micro_eligible_recommends_micro(self):
        """classify_task: micro-eligible task → MICRO."""
        rc = _make_config(
            mode="AUTO",
            changed_files_predicted=1,
            lines_changed_predicted=50,
            no_new_public_interfaces=True,
            change_is_fully_reversible=True,
            verifier_kind="frozen_test_suite",
            frozen_suite_qualifies=True,
            deterministic_metric_defined=True,
        )
        task = _make_task()
        classification = classify_task(rc, task)
        assert classification.recommended_mode == Mode.MICRO

    def test_classify_task_irreversible_high_ambiguity(self):
        """classify_task: irreversible + high ambiguity → FULL."""
        rc = _make_config(mode="AUTO", scope_ambiguity="high")
        task = _make_task(
            deployment_side_effects="irreversible",
            scope_ambiguity="high",
        )
        classification = classify_task(rc, task)
        assert classification.recommended_mode == Mode.FULL
        assert any("irreversible" in r.lower() for r in classification.escalation_reasons)

    def test_classify_task_security_public_interface(self):
        """classify_task: security-relevant + public interface → STANDARD minimum."""
        rc = _make_config(mode="AUTO")
        task = _make_task(
            security_relevance={
                "is_security_relevant": True,
                "is_safety_relevant": False,
                "is_compliance_relevant": False,
            },
            public_interface_impact={
                "changes_public_surface": True,
                "surface_types": ["api"],
            },
        )
        classification = classify_task(rc, task)
        assert classification.recommended_mode in (Mode.STANDARD, Mode.FULL)
        assert len(classification.minimum_reasons) > 0


# ---------------------------------------------------------------------------
# Test 3: Gate Evaluation
# ---------------------------------------------------------------------------

class TestGateEvaluation:
    """Test gate predicate evaluation."""

    def test_g0_passes_with_healthy_providers(self):
        rc = _make_config()
        reg = _SHARED_REGISTRY
        manifest = _make_manifest(rc)

        wave_output = {
            "probe_results": [
                {"model": "claude-opus-4", "status": "HEALTHY", "latency_ms": 100},
                {"model": "gpt-5.4", "status": "HEALTHY", "latency_ms": 150},
                {"model": "gemini-2.5-pro", "status": "HEALTHY", "latency_ms": 120},
            ],
            "mode_selected": "STANDARD",
            "registry_hash": manifest.registry_hash,
        }

        result = evaluate_g0(wave_output, rc, reg, manifest)
        assert result.passed is True
        assert result.result == GateResult.PASS

    def test_g0_fails_on_diversity(self):
        rc = _make_config()
        reg = _SHARED_REGISTRY
        manifest = _make_manifest(rc)

        # Only 2 families
        wave_output = {
            "probe_results": [
                {"model": "claude-opus-4", "status": "HEALTHY"},
                {"model": "claude-sonnet-4", "status": "HEALTHY"},
            ],
            "mode_selected": "STANDARD",
            "registry_hash": manifest.registry_hash,
        }

        result = evaluate_g0(wave_output, rc, reg, manifest)
        assert result.passed is False
        assert "FM-DIVERSITY" in result.failure_modes

    def test_g0_fails_on_timeout(self):
        rc = _make_config()
        reg = _SHARED_REGISTRY
        manifest = _make_manifest(rc)

        wave_output = {
            "probe_results": [
                {"model": "claude-opus-4", "status": "HEALTHY"},
                {"model": "gpt-5.4", "status": "HEALTHY"},
                {"model": "gemini-2.5-pro", "status": "HEALTHY"},
            ],
            "mode_selected": "STANDARD",
            "registry_hash": manifest.registry_hash,
        }

        result = evaluate_g0(wave_output, rc, reg, manifest, timed_out=True)
        assert result.passed is False
        assert "FM-TIMEOUT" in result.failure_modes

    def test_g1_passes_with_valid_blueprint(self):
        rc = _make_config()
        reg = _SHARED_REGISTRY
        manifest = _make_manifest(rc)

        wave_output = {
            "requirements": {
                "functional": [
                    {"id": f"REQ-{i:03d}", "priority": "MUST", "description": f"Requirement {i}"}
                    for i in range(5)
                ],
            },
            "failure_modes": [{"fm_id": "FM-001", "description": "Test failure"}],
            "rubric": [{"criterion_id": "RC-001", "weight": 1.0}],
            "user_journeys": [
                {"journey_id": f"UJ-{i:03d}", "description": f"Journey {i}", "steps": ["a", "b", "c"]}
                for i in range(3)
            ],
            "panel_consensus": {"agreement_level": "unanimous", "vote_counts": {}},
            "w1_synthesis_confidence": 0.85,
            "residue": {"minority_dissent": []},
        }

        result = evaluate_g1(wave_output, rc, reg, manifest)
        assert result.passed is True

    def test_g1_fails_on_insufficient_must_reqs(self):
        """MECH-037: Need ≥5 MUST reqs for Standard."""
        rc = _make_config()
        reg = _SHARED_REGISTRY
        manifest = _make_manifest(rc)

        wave_output = {
            "requirements": {
                "functional": [
                    {"id": "REQ-001", "priority": "MUST", "description": "Only one"}
                ],
            },
            "failure_modes": [{"fm_id": "FM-001"}],
            "rubric": [{"criterion_id": "RC-001"}],
            "user_journeys": [
                {"journey_id": f"UJ-{i:03d}", "description": f"J{i}", "steps": ["a", "b", "c"]}
                for i in range(3)
            ],
            "panel_consensus": {"agreement_level": "majority"},
            "w1_synthesis_confidence": 0.80,
            "residue": {"minority_dissent": []},
        }

        result = evaluate_g1(wave_output, rc, reg, manifest)
        assert result.passed is False
        assert "FM-BLUEPRINT-WEAK" in result.failure_modes

    def test_g2_passes_with_successful_builders(self):
        rc = _make_config()
        reg = _SHARED_REGISTRY
        manifest = _make_manifest(rc)

        wave_output = {
            "builders": [
                {"model_actual": "claude-opus-4", "family_actual": "anthropic",
                 "build_status": "SUCCESS", "artifact_id": "art-1", "residue": {}},
                {"model_actual": "gpt-5.4", "family_actual": "openai",
                 "build_status": "SUCCESS", "artifact_id": "art-2", "residue": {}},
                {"model_actual": "gemini-2.5-pro", "family_actual": "google",
                 "build_status": "SUCCESS", "artifact_id": "art-3", "residue": {}},
            ],
        }

        result = evaluate_g2(wave_output, rc, reg, manifest)
        assert result.passed is True

    def test_g2_fails_with_only_one_success(self):
        rc = _make_config()
        reg = _SHARED_REGISTRY
        manifest = _make_manifest(rc)

        wave_output = {
            "builders": [
                {"model_actual": "claude-opus-4", "family_actual": "anthropic",
                 "build_status": "SUCCESS", "artifact_id": "art-1", "residue": {}},
                {"model_actual": "gpt-5.4", "family_actual": "openai",
                 "build_status": "FAIL", "artifact_id": None},
                {"model_actual": "gemini-2.5-pro", "family_actual": "google",
                 "build_status": "FAIL", "artifact_id": None},
            ],
        }

        result = evaluate_g2(wave_output, rc, reg, manifest)
        assert result.passed is False
        assert "FM-FINDING" in result.failure_modes

    def test_registry_tamper_detected(self):
        """All gates must detect registry hash changes."""
        rc = _make_config()
        reg = _SHARED_REGISTRY
        manifest = _make_manifest(rc)

        # Tamper with registry after manifest was created
        reg.families["new_family"] = {"models": ["fake-model"], "organization": "Evil"}
        reg._hash = None  # Force recomputation

        wave_output = {
            "probe_results": [
                {"model": "claude-opus-4", "status": "HEALTHY"},
                {"model": "gpt-5.4", "status": "HEALTHY"},
                {"model": "gemini-2.5-pro", "status": "HEALTHY"},
            ],
            "mode_selected": "STANDARD",
            "registry_hash": manifest.registry_hash,  # Old hash from wave output
        }

        result = evaluate_g0(wave_output, rc, reg, manifest)
        # The registry object's hash no longer matches the manifest's hash
        assert result.passed is False
        assert "FM-REGISTRY-TAMPER" in result.failure_modes


# ---------------------------------------------------------------------------
# Test 4: Pipeline Bounds (MECH-021)
# ---------------------------------------------------------------------------

class TestPipelineBounds:
    """Test PIPELINE_EXHAUSTION_CHECK."""

    def test_no_exhaustion_on_fresh_run(self):
        manifest = _make_manifest()
        bounds = PipelineBounds()
        exhausted, reason = check_pipeline_exhaustion(manifest, bounds)
        assert exhausted is False
        assert reason is None

    def test_exhaustion_on_w2_reruns(self):
        manifest = _make_manifest()
        manifest.loop_counters.w2_reruns = 3  # exceeds default max of 2
        bounds = PipelineBounds()
        exhausted, reason = check_pipeline_exhaustion(manifest, bounds)
        assert exhausted is True
        assert "w2_reruns" in reason

    def test_exhaustion_on_w5_reruns(self):
        manifest = _make_manifest()
        manifest.loop_counters.w5_reruns = 3
        bounds = PipelineBounds()
        exhausted, reason = check_pipeline_exhaustion(manifest, bounds)
        assert exhausted is True
        assert "w5_reruns" in reason

    def test_custom_bounds_respected(self):
        manifest = _make_manifest()
        manifest.loop_counters.w2_reruns = 4
        bounds = PipelineBounds.from_custom({"max_w2_reruns": 5})
        exhausted, _ = check_pipeline_exhaustion(manifest, bounds)
        assert exhausted is False  # 4 < 5


# ---------------------------------------------------------------------------
# Test 5: Failure Routing
# ---------------------------------------------------------------------------

class TestFailureRouting:
    """Test failure routing logic."""

    def test_w0_failure_halts(self):
        manifest = _make_manifest()
        bounds = PipelineBounds()
        gate_eval = GateEvaluation(
            gate_id="G0", wave_id="W0",
            result=GateResult.FAIL,
            failure_modes=["FM-PROVIDER"],
        )
        route = route_failure("W0", gate_eval, manifest, bounds)
        assert route.action == FailureAction.HALT
        assert route.fm_id == "FM-PROVIDER"

    def test_w2_rework_on_finding(self):
        manifest = _make_manifest()
        bounds = PipelineBounds()
        gate_eval = GateEvaluation(
            gate_id="G2", wave_id="W2",
            result=GateResult.FAIL,
            failure_modes=["FM-FINDING"],
        )
        route = route_failure("W2", gate_eval, manifest, bounds)
        assert route.action == FailureAction.REWORK

    def test_w2_exhausted_escalates(self):
        manifest = _make_manifest()
        manifest.loop_counters.w2_reruns = 2  # at limit
        bounds = PipelineBounds()
        gate_eval = GateEvaluation(
            gate_id="G2", wave_id="W2",
            result=GateResult.FAIL,
            failure_modes=["FM-FINDING"],
        )
        route = route_failure("W2", gate_eval, manifest, bounds)
        assert route.action == FailureAction.ESCALATE
        assert "FM-EXHAUSTION" in route.fm_id

    def test_w3_returns_to_w2(self):
        manifest = _make_manifest()
        bounds = PipelineBounds()
        gate_eval = GateEvaluation(
            gate_id="G3", wave_id="W3",
            result=GateResult.FAIL,
            failure_modes=["FM-FINDING"],
        )
        route = route_failure("W3", gate_eval, manifest, bounds)
        assert route.action == FailureAction.RETURN
        assert route.target_wave == "W2"

    def test_w4_trace_gap_halts(self):
        manifest = _make_manifest()
        bounds = PipelineBounds()
        gate_eval = GateEvaluation(
            gate_id="G4", wave_id="W4",
            result=GateResult.FAIL,
            failure_modes=["FM-TRACE-GAP"],
        )
        route = route_failure("W4", gate_eval, manifest, bounds)
        assert route.action == FailureAction.HALT


# ---------------------------------------------------------------------------
# Test 6: Manifest Lifecycle
# ---------------------------------------------------------------------------

class TestManifestLifecycle:
    """Test manifest creation, updates, and persistence."""

    def test_manifest_creation(self):
        manifest = _make_manifest()
        assert manifest.run_id == "HRR-TEST-001"
        assert manifest.mode == "STANDARD"
        assert manifest.status == RunStatus.RUNNING
        assert "W0" in manifest.waves
        assert "W11" in manifest.waves

    def test_wave_lifecycle(self):
        manifest = _make_manifest()
        manifest.start_wave("W0")
        assert manifest.waves["W0"].status == WaveStatus.RUNNING
        assert manifest.waves["W0"].started_at is not None

        manifest.complete_wave("W0", GateResult.PASS)
        assert manifest.waves["W0"].status == WaveStatus.COMPLETED
        assert manifest.waves["W0"].gate_result == GateResult.PASS

    def test_manifest_halt(self):
        manifest = _make_manifest()
        manifest.halt("Test halt", "FM-CONFIG")
        assert manifest.status == RunStatus.HALTED
        assert manifest.completed_at is not None
        assert len(manifest.failure_events) > 0

    def test_manifest_persistence(self):
        manifest = _make_manifest()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = manifest.save(Path(tmpdir))
            loaded = RunManifest.load(Path(tmpdir))
            assert loaded.run_id == manifest.run_id
            assert loaded.mode == manifest.mode

    def test_manifest_checkpoint(self):
        manifest = _make_manifest()
        manifest.start_wave("W0")
        manifest.complete_wave("W0", GateResult.PASS)
        with tempfile.TemporaryDirectory() as tmpdir:
            cp_path = manifest.save_checkpoint(Path(tmpdir), "W0")
            assert cp_path.exists()
            # Verify checkpoint content
            with open(cp_path) as f:
                cp = json.load(f)
            assert cp["wave_id"] == "W0"
            assert "manifest_hash" in cp

    def test_micro_wave_sequence(self):
        manifest = _make_manifest(mode=Mode.MICRO)
        assert "M0" in manifest.waves
        assert "M1" in manifest.waves
        assert "M2" in manifest.waves
        assert "W0" not in manifest.waves


# ---------------------------------------------------------------------------
# Test 7: Full Pipeline Execution
# ---------------------------------------------------------------------------

class TestPipelineExecution:
    """Test full pipeline execution with default executor."""

    def test_standard_pipeline_completes(self):
        """Full standard pipeline with default stub executor should complete."""
        rc = _make_config()
        task = _make_task()

        with tempfile.TemporaryDirectory() as tmpdir:
            result = asyncio.run(run_pipeline(
                run_config=rc,
                task=task,
                output_dir=tmpdir,
            ))
            assert result.status == RunStatus.COMPLETED
            assert result.mode == "STANDARD"
            assert len(result.waves_completed) > 0
            assert result.manifest_path is not None

    def test_pipeline_halts_on_bad_config(self):
        """Pipeline should halt if W0 gate fails."""
        rc = _make_config(provider_list=["anthropic"])  # only 1 provider

        async def failing_w0_executor(wave_id, context, run_config, manifest):
            if wave_id == "W0":
                return {
                    "probe_results": [
                        {"model": "claude-opus-4", "status": "HEALTHY"},
                    ],
                    "mode_selected": "STANDARD",
                    "registry_hash": manifest.registry_hash,
                }
            return {"status": "completed", "residue": {}}

        task = _make_task()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = asyncio.run(run_pipeline(
                run_config=rc,
                task=task,
                output_dir=tmpdir,
                wave_executor=failing_w0_executor,
            ))
            # Should fail at G0 (diversity) and halt
            assert result.status in (RunStatus.HALTED, RunStatus.PAUSED)


# ---------------------------------------------------------------------------
# Test 8: Wave State Machine
# ---------------------------------------------------------------------------

class TestWaveStateMachine:
    """Test wave state transitions."""

    def test_wave_states_transitions(self):
        """Verify wave states follow PENDING → RUNNING → COMPLETED/FAILED."""
        manifest = _make_manifest()

        # Initially all PENDING
        for wid, wrec in manifest.waves.items():
            assert wrec.status == WaveStatus.PENDING

        # Start W0
        manifest.start_wave("W0")
        assert manifest.waves["W0"].status == WaveStatus.RUNNING

        # Complete W0
        manifest.complete_wave("W0", GateResult.PASS)
        assert manifest.waves["W0"].status == WaveStatus.COMPLETED

        # Fail W1
        manifest.start_wave("W1")
        manifest.complete_wave("W1", GateResult.FAIL)
        assert manifest.waves["W1"].status == WaveStatus.FAILED

        # Timeout W2
        manifest.start_wave("W2")
        manifest.complete_wave("W2", GateResult.TIMEOUT)
        assert manifest.waves["W2"].status == WaveStatus.TIMED_OUT

    def test_skip_wave(self):
        manifest = _make_manifest()
        manifest.skip_wave("W5.5", reason="clean run")
        assert manifest.waves["W5.5"].status == WaveStatus.SKIPPED

    def test_loop_counters_increment(self):
        manifest = _make_manifest()
        assert manifest.loop_counters.w2_reruns == 0
        manifest.loop_counters.w2_reruns += 1
        assert manifest.loop_counters.w2_reruns == 1

    def test_family_registry_hash(self):
        reg = _SHARED_REGISTRY
        h1 = reg.compute_hash()
        h2 = reg.compute_hash()
        assert h1 == h2
        assert len(h1) == 64  # SHA-256 hex

        # Modify registry → different hash
        reg.families["test"] = {"models": ["x"]}
        h3 = reg.compute_hash()
        assert h3 != h1


# ---------------------------------------------------------------------------
# Run tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
