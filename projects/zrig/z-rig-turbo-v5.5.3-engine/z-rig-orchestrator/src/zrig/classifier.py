"""
Z-Rig Classifier Module — Mode Classification (MECH-003 + MECH-031)

Implements MODE_SELECT and MICRO_ELIGIBLE predicates per the v5.5.3 spec.

Changes (HRR-005):
- Added AUTO mode support: full task analysis to determine optimal mode
- When mode is explicitly set (MICRO/STANDARD/FULL), classification still runs
  and logs advisory warnings if task analysis disagrees
- MICRO_ELIGIBLE thresholds updated: ≤3 files, ≤300 lines (MECH-031)
- Escalation rules: critical stakes → FULL, irreversible + high ambiguity → FULL,
  security_relevant + public_interface → STANDARD minimum
- classify_task() function for standalone task analysis without config override
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from .config import (
    Mode,
    RunConfig,
    ScopeAmbiguity,
    StakesLevel,
    TaskDescription,
    VerifierKind,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# MECH-031: MICRO_ELIGIBLE result
# ---------------------------------------------------------------------------

@dataclass
class MicroEligibilityResult:
    """Result of MICRO_ELIGIBLE predicate evaluation."""
    eligible: bool = False
    scope_ok: bool = False
    stakes_ok: bool = False
    security_ok: bool = False
    deterministic_ok: bool = False
    coverage_ok: bool = False
    failing_clauses: list[str] = field(default_factory=list)
    operator_override_applied: bool = False

    @property
    def all_clauses(self) -> dict[str, bool]:
        return {
            "scope_ok": self.scope_ok,
            "stakes_ok": self.stakes_ok,
            "security_ok": self.security_ok,
            "deterministic_ok": self.deterministic_ok,
            "coverage_ok": self.coverage_ok,
        }


# ---------------------------------------------------------------------------
# MECH-031: MICRO_ELIGIBLE
# ---------------------------------------------------------------------------

_RESTRICTED_ARTIFACT_TYPES = frozenset({
    "patent", "safety-critical-code", "legal-contract",
})


def micro_eligible(
    task: TaskDescription,
    run_config: RunConfig,
) -> MicroEligibilityResult:
    """
    MECH-031: Evaluate whether a task qualifies for Micro Mode.

    Returns a detailed result with per-clause evaluation.

    Thresholds (HRR-005 update):
    - ≤3 changed files predicted
    - ≤300 lines changed predicted
    - scope_ambiguity = none
    - no_new_public_interfaces = true
    - change_is_fully_reversible = true
    - stakes ≠ critical
    - not security/safety/compliance relevant
    - deterministic verifier required
    """
    result = MicroEligibilityResult()
    failing: list[str] = []

    # --- Scope Clauses ---
    scope_checks = []
    if run_config.scope_ambiguity.value != "none":
        scope_checks.append(f"scope_ambiguity must be 'none', got '{run_config.scope_ambiguity.value}'")
    if run_config.changed_files_predicted is not None and run_config.changed_files_predicted > 3:
        scope_checks.append(f"changed_files_predicted must be ≤3, got {run_config.changed_files_predicted}")
    elif run_config.changed_files_predicted is None:
        scope_checks.append("changed_files_predicted is not declared")
    if run_config.lines_changed_predicted is not None and run_config.lines_changed_predicted > 300:
        scope_checks.append(f"lines_changed_predicted must be ≤300, got {run_config.lines_changed_predicted}")
    elif run_config.lines_changed_predicted is None:
        scope_checks.append("lines_changed_predicted is not declared")
    if run_config.no_new_public_interfaces is not True:
        scope_checks.append("no_new_public_interfaces must be true")
    if run_config.change_is_fully_reversible is not True:
        scope_checks.append("change_is_fully_reversible must be true")

    result.scope_ok = len(scope_checks) == 0
    failing.extend(scope_checks)

    # --- Stakes Clauses ---
    stakes_checks = []
    if run_config.stakes_level == StakesLevel.CRITICAL:
        stakes_checks.append("stakes_level is 'critical' (disqualifies Micro)")
    if task.artifact_type in _RESTRICTED_ARTIFACT_TYPES:
        stakes_checks.append(f"artifact_type '{task.artifact_type}' is in restricted set")

    result.stakes_ok = len(stakes_checks) == 0
    failing.extend(stakes_checks)

    # --- Security Clause ---
    security_checks = []
    if task.security_relevance.is_security_relevant:
        security_checks.append("task is security-relevant")
    if task.security_relevance.is_safety_relevant:
        security_checks.append("task is safety-relevant")
    if task.security_relevance.is_compliance_relevant:
        security_checks.append("task is compliance-relevant")

    result.security_ok = len(security_checks) == 0
    failing.extend(security_checks)

    # --- Verifier / Deterministic Clause ---
    det_checks = []
    if not run_config.deterministic_metric_defined:
        det_checks.append("deterministic_metric_defined is false")
    allowed_verifiers = {
        VerifierKind.FROZEN_TEST_SUITE,
        VerifierKind.DETERMINISTIC_CHECKER,
        VerifierKind.SINGLE_INDEPENDENT_VERIFIER,
    }
    if run_config.verifier_kind not in allowed_verifiers:
        det_checks.append(f"verifier_kind '{run_config.verifier_kind}' not in allowed set")
    if len(task.target_files) > 3:
        det_checks.append(f"target_files count must be ≤3, got {len(task.target_files)}")
    if not task.deterministic_verifier.frozen_before_run:
        det_checks.append("frozen_verifier_hash_locked (frozen_before_run) is false")
    if task.deployment_side_effects.value != "none":
        det_checks.append(f"deployment_side_effects must be 'none', got '{task.deployment_side_effects.value}'")

    result.deterministic_ok = len(det_checks) == 0
    failing.extend(det_checks)

    # --- Coverage Clause (hard gate for frozen_test_suite) ---
    coverage_checks = []
    if run_config.verifier_kind == VerifierKind.FROZEN_TEST_SUITE:
        if run_config.frozen_suite_qualifies is not True:
            coverage_checks.append("frozen_suite_qualifies must be true for frozen_test_suite verifier")
        cov = task.deterministic_verifier.coverage_of_changed_scope
        if cov is None:
            coverage_checks.append("coverage_of_changed_scope is null — fail-closed for Micro")
        elif cov < 0.80:
            coverage_checks.append(
                f"coverage_of_changed_scope must be ≥0.80, got {cov:.2f}"
            )
        result.coverage_ok = len(coverage_checks) == 0
    else:
        # Non-suite verifiers exempt from 80% coverage check
        result.coverage_ok = True

    failing.extend(coverage_checks)

    # --- Final eligibility ---
    result.eligible = all([
        result.scope_ok,
        result.stakes_ok,
        result.security_ok,
        result.deterministic_ok,
        result.coverage_ok,
    ])
    result.failing_clauses = failing

    # --- Operator Override ---
    if not result.eligible and run_config.operator_micro_override:
        # Override does NOT bypass coverage requirement for frozen_test_suite
        if run_config.verifier_kind == VerifierKind.FROZEN_TEST_SUITE and not result.coverage_ok:
            # Cannot override coverage gate
            pass
        else:
            result.eligible = True
            result.operator_override_applied = True

    return result


# ---------------------------------------------------------------------------
# Task Analysis — classify_task (MECH-003 helper)
# ---------------------------------------------------------------------------

@dataclass
class TaskClassification:
    """Result of pure task analysis — what mode SHOULD be used based on signals."""
    recommended_mode: Mode = Mode.STANDARD
    micro_result: MicroEligibilityResult | None = None
    escalation_reasons: list[str] = field(default_factory=list)
    minimum_reasons: list[str] = field(default_factory=list)


def classify_task(
    run_config: RunConfig,
    task: TaskDescription,
) -> TaskClassification:
    """
    Analyze task signals to determine recommended mode, independent of config override.

    Escalation rules (highest priority first):
    1. critical stakes → FULL
    2. restricted artifact type (patent, safety-critical-code, legal-contract) → FULL
    3. irreversible deployment + high scope ambiguity → FULL
    4. security_relevant + changes_public_surface → STANDARD minimum
    5. MICRO_ELIGIBLE satisfied → MICRO
    6. Default → STANDARD
    """
    result = TaskClassification()
    escalation_reasons: list[str] = []
    minimum_reasons: list[str] = []

    # --- Check MICRO eligibility ---
    micro_result = micro_eligible(task, run_config)
    result.micro_result = micro_result

    # --- Check FULL escalation triggers ---
    # 1. Critical stakes → FULL
    if run_config.stakes_level == StakesLevel.CRITICAL:
        escalation_reasons.append("stakes_level is 'critical'")
    if task.stakes_level == StakesLevel.CRITICAL:
        escalation_reasons.append("task stakes_level is 'critical'")

    # 2. Restricted artifact type → FULL
    if task.artifact_type in _RESTRICTED_ARTIFACT_TYPES:
        escalation_reasons.append(f"artifact_type '{task.artifact_type}' is restricted")
    if run_config.artifact_type in _RESTRICTED_ARTIFACT_TYPES:
        escalation_reasons.append(f"config artifact_type '{run_config.artifact_type}' is restricted")

    # 3. Irreversible + high ambiguity → FULL
    if (task.deployment_side_effects.value == "irreversible"
            and task.scope_ambiguity == ScopeAmbiguity.HIGH):
        escalation_reasons.append("irreversible deployment + high scope ambiguity")
    if (not task.reversibility.fully_reversible
            and run_config.scope_ambiguity == ScopeAmbiguity.HIGH):
        escalation_reasons.append("non-reversible change + high scope ambiguity (config)")

    # --- Check STANDARD minimum triggers ---
    # 4. Security-relevant + public interface changes → STANDARD minimum
    if (task.security_relevance.is_security_relevant
            and task.public_interface_impact.changes_public_surface):
        minimum_reasons.append("security-relevant task changes public interface")
    if task.security_relevance.is_safety_relevant:
        minimum_reasons.append("task is safety-relevant")

    # --- Determine recommended mode ---
    result.escalation_reasons = escalation_reasons
    result.minimum_reasons = minimum_reasons

    if escalation_reasons:
        result.recommended_mode = Mode.FULL
    elif minimum_reasons:
        # STANDARD minimum — could still be eligible for STANDARD (not MICRO)
        result.recommended_mode = Mode.STANDARD
    elif micro_result.eligible:
        result.recommended_mode = Mode.MICRO
    else:
        result.recommended_mode = Mode.STANDARD

    return result


# ---------------------------------------------------------------------------
# MECH-003: MODE_SELECT
# ---------------------------------------------------------------------------

@dataclass
class ModeSelectResult:
    """Result of MODE_SELECT."""
    selected_mode: Mode = Mode.STANDARD
    recommended_mode: Mode | None = None
    micro_result: MicroEligibilityResult | None = None
    auto_escalated: bool = False
    escalation_reason: str | None = None
    failure_event: dict[str, Any] | None = None
    advisory: str | None = None


def mode_select(
    run_config: RunConfig,
    task: TaskDescription,
) -> ModeSelectResult:
    """
    MECH-003: MODE_SELECT — Determine the pipeline mode.

    Behavior (HRR-005 update):
    1. mode=AUTO: Full task analysis determines mode (MICRO → STANDARD → FULL)
    2. mode=MICRO: Evaluate MICRO_ELIGIBLE; auto-escalate to STANDARD if ineligible
    3. mode=STANDARD: Use STANDARD but run analysis; log advisory if analysis disagrees
    4. mode=FULL: Use FULL but run analysis; log advisory if analysis disagrees

    Advisory warnings are logged but do NOT override explicit mode selections
    (except MICRO → STANDARD auto-escalation which is a safety mechanism).
    """
    result = ModeSelectResult()

    # --- AUTO mode: full task analysis drives selection ---
    if run_config.mode == Mode.AUTO:
        classification = classify_task(run_config, task)
        result.recommended_mode = classification.recommended_mode
        result.micro_result = classification.micro_result

        if classification.recommended_mode == Mode.MICRO:
            result.selected_mode = Mode.MICRO
        elif classification.recommended_mode == Mode.FULL:
            result.selected_mode = Mode.FULL
            result.auto_escalated = True
            result.escalation_reason = "; ".join(classification.escalation_reasons)
        else:
            result.selected_mode = Mode.STANDARD

        return result

    # --- Explicit MICRO: evaluate eligibility ---
    if run_config.mode == Mode.MICRO:
        micro_result = micro_eligible(task, run_config)
        result.micro_result = micro_result

        if micro_result.eligible:
            result.selected_mode = Mode.MICRO

            # Still run classification for advisory
            classification = classify_task(run_config, task)
            result.recommended_mode = classification.recommended_mode
            if classification.recommended_mode.rank > Mode.MICRO.rank:
                advisory = (
                    f"⚠️ Task analysis recommends {classification.recommended_mode.value} "
                    f"but config requests MICRO (override logged)"
                )
                result.advisory = advisory
                logger.warning(advisory)
        else:
            # Auto-escalation: not a halt
            result.selected_mode = Mode.STANDARD
            result.auto_escalated = True
            result.escalation_reason = "; ".join(micro_result.failing_clauses)
            result.failure_event = {
                "fm_id": "FM-MICRO-MISUSE",
                "reason": result.escalation_reason,
                "escalated_to": "STANDARD",
                "operator_override_attempted": micro_result.operator_override_applied,
            }

            # Check if task analysis would recommend FULL
            classification = classify_task(run_config, task)
            result.recommended_mode = classification.recommended_mode
            if classification.recommended_mode == Mode.FULL:
                result.selected_mode = Mode.FULL
                result.failure_event["escalated_to"] = "FULL"
                result.escalation_reason += (
                    f"; further escalated to FULL: "
                    + "; ".join(classification.escalation_reasons)
                )
                advisory = (
                    f"⚠️ Task analysis recommends FULL "
                    f"(MICRO failed eligibility, further escalated past STANDARD)"
                )
                result.advisory = advisory
                logger.warning(advisory)

        return result

    # --- Explicit STANDARD or FULL: use it, but run analysis for advisory ---
    classification = classify_task(run_config, task)
    result.recommended_mode = classification.recommended_mode
    result.micro_result = classification.micro_result
    result.selected_mode = run_config.mode  # Honor explicit selection

    if classification.recommended_mode != run_config.mode:
        if classification.recommended_mode.rank > run_config.mode.rank:
            # Analysis recommends stricter mode than configured
            advisory = (
                f"⚠️ Task analysis recommends {classification.recommended_mode.value} "
                f"but config requests {run_config.mode.value} (override logged)"
            )
            if classification.escalation_reasons:
                advisory += f" — reasons: {'; '.join(classification.escalation_reasons)}"
            result.advisory = advisory
            logger.warning(advisory)
        elif classification.recommended_mode.rank < run_config.mode.rank:
            # Analysis recommends less strict mode — informational only
            advisory = (
                f"ℹ️ Task analysis suggests {classification.recommended_mode.value} "
                f"would suffice, but config requests {run_config.mode.value} (no issue)"
            )
            result.advisory = advisory
            logger.info(advisory)

    return result
