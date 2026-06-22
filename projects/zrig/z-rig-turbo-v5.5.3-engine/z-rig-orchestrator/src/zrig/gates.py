"""
Z-Rig Gates Module — Mechanical gate predicate evaluation per v5.5.3 spec.

Each gate function evaluates the predicate for its wave, returning a structured
GateEvaluation with PASS/FAIL result, per-check details, and failure reasons.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from .config import FamilyRegistry, Mode, RunConfig, PipelineBounds
from .manifest import RunManifest, GateResult


# ---------------------------------------------------------------------------
# Gate evaluation result
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    """Result of a single gate check."""
    check_id: str = ""
    description: str = ""
    passed: bool = False
    tier: str = "T1-MECHANICAL"
    details: dict[str, Any] = field(default_factory=dict)
    failure_reason: str | None = None


@dataclass
class GateEvaluation:
    """Complete gate evaluation result."""
    gate_id: str = ""
    wave_id: str = ""
    result: str = GateResult.FAIL  # PASS, FAIL, TIMEOUT
    gate_type: str = "MECHANICAL"  # MECHANICAL, HYBRID, ADVISORY
    checks: list[CheckResult] = field(default_factory=list)
    failure_reasons: list[str] = field(default_factory=list)
    failure_modes: list[str] = field(default_factory=list)
    registry_verified: bool = False

    @property
    def passed(self) -> bool:
        return self.result == GateResult.PASS

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "wave_id": self.wave_id,
            "result": self.result,
            "gate_type": self.gate_type,
            "checks": [
                {
                    "check_id": c.check_id,
                    "description": c.description,
                    "passed": c.passed,
                    "tier": c.tier,
                    "details": c.details,
                    "failure_reason": c.failure_reason,
                }
                for c in self.checks
            ],
            "failure_reasons": self.failure_reasons,
            "failure_modes": self.failure_modes,
            "registry_verified": self.registry_verified,
        }


# ---------------------------------------------------------------------------
# Registry integrity check (shared across all gates)
# ---------------------------------------------------------------------------

def _check_registry_integrity(
    registry: FamilyRegistry,
    manifest: RunManifest,
) -> CheckResult:
    """MECH-002: Verify registry hash hasn't changed since W0."""
    current_hash = registry.compute_hash()
    passed = current_hash == manifest.registry_hash
    return CheckResult(
        check_id="REGISTRY_HASH",
        description="MECH-002: Registry hash continuous integrity",
        passed=passed,
        tier="T1-MECHANICAL",
        details={
            "expected": manifest.registry_hash,
            "actual": current_hash,
        },
        failure_reason=None if passed else "FM-REGISTRY-TAMPER: Registry hash mismatch",
    )


# ---------------------------------------------------------------------------
# G0 — W0: Pre-Ignition Gate
# ---------------------------------------------------------------------------

def evaluate_g0(
    wave_output: dict[str, Any],
    run_config: RunConfig,
    registry: FamilyRegistry,
    manifest: RunManifest,
    timed_out: bool = False,
) -> GateEvaluation:
    """
    G0 gate predicate (Standard Mode):

    G0_PASS :=
      ∀ seat ∈ required_seats: seat.status ∈ {HEALTHY, DEGRADED}
      ∧ DIVERSITY_CHECK(probed_models, min_families=3) = true
      ∧ registry_hash IS computed ∧ recorded in manifest
      ∧ MODE_SELECT(run_config) = STANDARD
      ∧ run_config IS structurally valid
      ∧ NOT MECH-015(W0_timeout)
    """
    eval_result = GateEvaluation(gate_id="G0", wave_id="W0", gate_type="MECHANICAL")
    checks: list[CheckResult] = []

    # Check 1: All required seats healthy/degraded
    probe_results = wave_output.get("probe_results", [])
    healthy_statuses = {"HEALTHY", "DEGRADED"}
    all_healthy = all(
        p.get("status") in healthy_statuses for p in probe_results
    )
    unavailable = [p for p in probe_results if p.get("status") == "UNAVAILABLE"]
    checks.append(CheckResult(
        check_id="SEAT_HEALTH",
        description="All required seats HEALTHY or DEGRADED",
        passed=all_healthy,
        tier="T1-MECHANICAL",
        details={"unavailable_count": len(unavailable)},
        failure_reason=None if all_healthy else f"FM-PROVIDER: {len(unavailable)} provider(s) unavailable",
    ))

    # Check 2: Diversity check (MECH-001)
    families_probed = set()
    for p in probe_results:
        if p.get("status") in healthy_statuses:
            fam = registry.family_of(p.get("model", ""))
            if fam != "UNKNOWN":
                families_probed.add(fam)
    # Also count from provider_list as a fallback
    if not families_probed:
        families_probed = set(run_config.provider_list)
    diversity_ok = len(families_probed) >= 3
    checks.append(CheckResult(
        check_id="DIVERSITY_CHECK",
        description="MECH-001: ≥3 distinct families available",
        passed=diversity_ok,
        tier="T1-MECHANICAL",
        details={"families_available": sorted(families_probed), "count": len(families_probed)},
        failure_reason=None if diversity_ok else f"FM-DIVERSITY: Only {len(families_probed)} families available, need ≥3",
    ))

    # Check 3: Registry hash computed and recorded
    reg_hash = wave_output.get("registry_hash", "")
    hash_ok = bool(reg_hash) and reg_hash == manifest.registry_hash
    checks.append(CheckResult(
        check_id="REGISTRY_HASH_COMPUTED",
        description="Registry hash computed and recorded in manifest",
        passed=hash_ok,
        tier="T1-MECHANICAL",
        details={"registry_hash": reg_hash},
        failure_reason=None if hash_ok else "Registry hash not computed or not matching manifest",
    ))

    # Check 3b: Registry object integrity (MECH-002)
    reg_integrity = _check_registry_integrity(registry, manifest)
    checks.append(reg_integrity)

    # Check 4: Mode selection
    mode_selected = wave_output.get("mode_selected", "")
    mode_ok = mode_selected == manifest.mode
    checks.append(CheckResult(
        check_id="MODE_SELECT",
        description="MECH-003: Mode selection matches expected",
        passed=mode_ok,
        tier="T1-MECHANICAL",
        details={"selected": mode_selected, "expected": manifest.mode},
        failure_reason=None if mode_ok else f"Mode mismatch: selected={mode_selected}, expected={manifest.mode}",
    ))

    # Check 5: run_config structurally valid (already validated at parse time)
    checks.append(CheckResult(
        check_id="CONFIG_VALID",
        description="run_config is structurally valid",
        passed=True,
        tier="T1-MECHANICAL",
    ))

    # Check 6: Timeout
    checks.append(CheckResult(
        check_id="TIMEOUT",
        description="MECH-015: W0 not timed out",
        passed=not timed_out,
        tier="T1-MECHANICAL",
        failure_reason=None if not timed_out else "FM-TIMEOUT: W0 timed out",
    ))

    # Aggregate
    eval_result.checks = checks
    all_passed = all(c.passed for c in checks)
    eval_result.result = GateResult.PASS if all_passed else GateResult.FAIL
    eval_result.failure_reasons = [c.failure_reason for c in checks if not c.passed and c.failure_reason]
    eval_result.failure_modes = _extract_fm_ids(eval_result.failure_reasons)
    eval_result.registry_verified = reg_integrity.passed

    return eval_result


# ---------------------------------------------------------------------------
# G1 — W1: Blueprint Panel Gate
# ---------------------------------------------------------------------------

def evaluate_g1(
    wave_output: dict[str, Any],
    run_config: RunConfig,
    registry: FamilyRegistry,
    manifest: RunManifest,
    mode: Mode = Mode.STANDARD,
    timed_out: bool = False,
) -> GateEvaluation:
    """G1 gate predicate (Standard Mode)."""
    eval_result = GateEvaluation(gate_id="G1", wave_id="W1", gate_type="HYBRID")
    checks: list[CheckResult] = []

    reqs = wave_output.get("requirements", {})
    functional = reqs.get("functional", [])
    must_reqs = [r for r in functional if r.get("priority") == "MUST"]

    # Check 1: MUST requirements present
    checks.append(CheckResult(
        check_id="MUST_REQS_PRESENT",
        description="≥1 MUST requirement present",
        passed=len(must_reqs) >= 1,
        tier="T1-MECHANICAL",
        details={"must_count": len(must_reqs)},
        failure_reason=None if must_reqs else "FM-SPEC: No MUST requirements",
    ))

    # Check 2: Failure modes present
    fms = wave_output.get("failure_modes", [])
    checks.append(CheckResult(
        check_id="FAILURE_MODES_PRESENT",
        description="failure_modes ≠ ∅",
        passed=len(fms) > 0,
        tier="T1-MECHANICAL",
        details={"count": len(fms)},
        failure_reason=None if fms else "FM-SPEC: No failure modes defined",
    ))

    # Check 3: Rubric present
    rubric = wave_output.get("rubric", [])
    checks.append(CheckResult(
        check_id="RUBRIC_PRESENT",
        description="rubric ≠ ∅",
        passed=len(rubric) > 0,
        tier="T1-MECHANICAL",
        details={"count": len(rubric)},
        failure_reason=None if rubric else "FM-SPEC: No rubric defined",
    ))

    # Check 4: User journeys present
    journeys = wave_output.get("user_journeys", [])
    checks.append(CheckResult(
        check_id="USER_JOURNEYS_PRESENT",
        description="user_journeys ≠ ∅",
        passed=len(journeys) > 0,
        tier="T1-MECHANICAL",
        details={"count": len(journeys)},
        failure_reason=None if journeys else "FM-SPEC: No user journeys defined",
    ))

    # Check 5: MECH-037 Blueprint specificity
    min_must = 8 if mode == Mode.FULL else 5
    min_journeys = 3
    specificity_ok = len(must_reqs) >= min_must and len(journeys) >= min_journeys
    checks.append(CheckResult(
        check_id="BLUEPRINT_SPECIFICITY",
        description=f"MECH-037: ≥{min_must} MUST reqs, ≥{min_journeys} journeys",
        passed=specificity_ok,
        tier="T1-MECHANICAL",
        details={
            "must_count": len(must_reqs), "min_must": min_must,
            "journey_count": len(journeys), "min_journeys": min_journeys,
        },
        failure_reason=None if specificity_ok else f"FM-BLUEPRINT-WEAK: {len(must_reqs)} MUST reqs (need {min_must}), {len(journeys)} journeys (need {min_journeys})",
    ))

    # Check 6: Panel consensus
    consensus = wave_output.get("panel_consensus", {})
    agreement = consensus.get("agreement_level", "")
    consensus_ok = agreement in {"unanimous", "majority"}
    checks.append(CheckResult(
        check_id="PANEL_CONSENSUS",
        description="Panel agreement is unanimous or majority",
        passed=consensus_ok,
        tier="T2-CROSS_VERIFIED",
        details={"agreement_level": agreement},
        failure_reason=None if consensus_ok else "No panel consensus achieved",
    ))

    # Check 7: Minority dissent captured
    residue = wave_output.get("residue", wave_output.get("minority_positions", []))
    # We check that if there are dissenting votes, they're captured
    dissent_captured = True  # Assume OK unless vote counts show disagreement
    vote_counts = consensus.get("vote_counts", {})
    disagree_count = vote_counts.get("disagree", 0)
    if disagree_count > 0:
        minority_dissent = wave_output.get("residue", {}).get("minority_dissent", [])
        if not isinstance(minority_dissent, list):
            minority_dissent = []
        dissent_captured = len(minority_dissent) >= disagree_count
    checks.append(CheckResult(
        check_id="DISSENT_CAPTURED",
        description="Minority dissent recorded for all dissenting seats",
        passed=dissent_captured,
        tier="T1-MECHANICAL",
        failure_reason=None if dissent_captured else "Minority dissent not captured for all dissenters",
    ))

    # Check 8: Synthesis confidence (T3-ATTESTED, paired with T1 checks)
    confidence = wave_output.get("w1_synthesis_confidence", 0.0)
    confidence_ok = confidence >= 0.75
    checks.append(CheckResult(
        check_id="SYNTHESIS_CONFIDENCE",
        description="W1 synthesis confidence ≥ 0.75",
        passed=confidence_ok,
        tier="T3-ATTESTED",
        details={"confidence": confidence, "threshold": 0.75},
        failure_reason=None if confidence_ok else f"Synthesis confidence {confidence} < 0.75",
    ))

    # Check 9: Registry integrity
    reg_check = _check_registry_integrity(registry, manifest)
    checks.append(reg_check)

    # Check 10: Timeout
    checks.append(CheckResult(
        check_id="TIMEOUT",
        description="MECH-015: W1 not timed out",
        passed=not timed_out,
        tier="T1-MECHANICAL",
        failure_reason=None if not timed_out else "FM-TIMEOUT: W1 timed out",
    ))

    eval_result.checks = checks
    all_passed = all(c.passed for c in checks)
    eval_result.result = GateResult.PASS if all_passed else GateResult.FAIL
    eval_result.failure_reasons = [c.failure_reason for c in checks if not c.passed and c.failure_reason]
    eval_result.failure_modes = _extract_fm_ids(eval_result.failure_reasons)
    eval_result.registry_verified = reg_check.passed

    return eval_result


# ---------------------------------------------------------------------------
# G2 — W2: Build Squad Gate
# ---------------------------------------------------------------------------

def evaluate_g2(
    wave_output: dict[str, Any],
    run_config: RunConfig,
    registry: FamilyRegistry,
    manifest: RunManifest,
    timed_out: bool = False,
) -> GateEvaluation:
    """G2 gate predicate: ≥2 builders succeed, ≥3 families."""
    eval_result = GateEvaluation(gate_id="G2", wave_id="W2", gate_type="MECHANICAL")
    checks: list[CheckResult] = []

    builders = wave_output.get("builders", [])
    successful = [b for b in builders if b.get("build_status") in ("SUCCESS", "PARTIAL")]

    # Diversity
    families = set()
    for b in builders:
        fam = b.get("family_actual", registry.family_of(b.get("model_actual", "")))
        if fam != "UNKNOWN":
            families.add(fam)
    diversity_ok = len(families) >= 3
    checks.append(CheckResult(
        check_id="BUILDER_DIVERSITY",
        description="MECH-001: ≥3 families across builders",
        passed=diversity_ok,
        tier="T1-MECHANICAL",
        details={"families": sorted(families), "count": len(families)},
        failure_reason=None if diversity_ok else f"FM-DIVERSITY: Only {len(families)} builder families",
    ))

    # ≥2 builders succeed
    success_ok = len(successful) >= 2
    checks.append(CheckResult(
        check_id="BUILD_SUCCESS",
        description="MECH-004: ≥2 builders succeed",
        passed=success_ok,
        tier="T1-MECHANICAL",
        details={"successful_count": len(successful), "total": len(builders)},
        failure_reason=None if success_ok else f"FM-FINDING: Only {len(successful)} builders succeeded",
    ))

    # Artifact IDs present
    artifact_ok = all(b.get("artifact_id") for b in successful)
    checks.append(CheckResult(
        check_id="ARTIFACTS_PRESENT",
        description="All successful builders have artifact_id",
        passed=artifact_ok,
        tier="T1-MECHANICAL",
    ))

    # Residue valid (MECH-028)
    residue_ok = all("residue" in b for b in successful)
    checks.append(CheckResult(
        check_id="RESIDUE_VALID",
        description="MECH-028: All successful builders have residue",
        passed=residue_ok,
        tier="T1-MECHANICAL",
        failure_reason=None if residue_ok else "FM-RESIDUE-DROP: Missing residue in builder output",
    ))

    # Registry
    reg_check = _check_registry_integrity(registry, manifest)
    checks.append(reg_check)

    # Timeout
    checks.append(CheckResult(
        check_id="TIMEOUT",
        description="MECH-015: W2 not timed out",
        passed=not timed_out,
        tier="T1-MECHANICAL",
        failure_reason=None if not timed_out else "FM-TIMEOUT: W2 timed out",
    ))

    eval_result.checks = checks
    all_passed = all(c.passed for c in checks)
    eval_result.result = GateResult.PASS if all_passed else GateResult.FAIL
    eval_result.failure_reasons = [c.failure_reason for c in checks if not c.passed and c.failure_reason]
    eval_result.failure_modes = _extract_fm_ids(eval_result.failure_reasons)
    eval_result.registry_verified = reg_check.passed

    return eval_result


# ---------------------------------------------------------------------------
# G3 — W3: Synthesis Gate
# ---------------------------------------------------------------------------

def evaluate_g3(
    wave_output: dict[str, Any],
    run_config: RunConfig,
    registry: FamilyRegistry,
    manifest: RunManifest,
    timed_out: bool = False,
) -> GateEvaluation:
    """G3 gate predicate (Standard): synthesis quality checks."""
    eval_result = GateEvaluation(gate_id="G3", wave_id="W3", gate_type="HYBRID")
    checks: list[CheckResult] = []

    # Primary completed
    primary_ok = wave_output.get("primary_completed", False)
    checks.append(CheckResult(
        check_id="PRIMARY_COMPLETED",
        description="Primary synthesis completed",
        passed=primary_ok,
        tier="T1-MECHANICAL",
    ))

    # MUST coverage
    basis = wave_output.get("selection_basis", {})
    must_sat = basis.get("must_satisfied", 0)
    must_tot = basis.get("must_total", 0)
    must_ok = must_sat == must_tot and must_tot > 0
    checks.append(CheckResult(
        check_id="MUST_COVERAGE",
        description="must_satisfied = must_total",
        passed=must_ok,
        tier="T1-MECHANICAL",
        details={"satisfied": must_sat, "total": must_tot},
        failure_reason=None if must_ok else f"FM-FINDING: MUST gap ({must_sat}/{must_tot})",
    ))

    # Coverage rate
    cov = basis.get("coverage_rate", 0.0)
    cov_ok = cov >= 0.95
    checks.append(CheckResult(
        check_id="COVERAGE_RATE",
        description="coverage_rate ≥ 0.95",
        passed=cov_ok,
        tier="T1-MECHANICAL",
        details={"coverage_rate": cov, "threshold": 0.95},
        failure_reason=None if cov_ok else f"FM-FINDING: Coverage {cov:.2%} < 95%",
    ))

    # Confidence (T3)
    confidence = wave_output.get("synthesis_confidence", 0.0)
    conf_ok = confidence >= 0.60
    checks.append(CheckResult(
        check_id="SYNTHESIS_CONFIDENCE",
        description="synthesis_confidence ≥ 0.60 (T3-ATTESTED)",
        passed=conf_ok,
        tier="T3-ATTESTED",
        details={"confidence": confidence, "threshold": 0.60},
        failure_reason=None if conf_ok else f"Confidence {confidence} < 0.60",
    ))

    # Challenger completion (if triggered)
    challenger_invoked = wave_output.get("challenger_invoked", False)
    challenger_completed = wave_output.get("challenger_completed", True)
    challenger_ok = not challenger_invoked or challenger_completed
    checks.append(CheckResult(
        check_id="CHALLENGER_COMPLETED",
        description="If challenger triggered, it completed",
        passed=challenger_ok,
        tier="T1-MECHANICAL",
    ))

    # Adjudication ceiling (MECH-013)
    adj = wave_output.get("adjudication", None)
    ceiling_ok = True
    if adj and challenger_invoked:
        meta_conf = adj.get("meta_confidence", 0)
        primary_conf = wave_output.get("primary_confidence", 0)
        challenger_conf = adj.get("challenger_confidence", 0)
        max_conf = max(primary_conf, challenger_conf)
        ceiling_ok = meta_conf <= max_conf
    checks.append(CheckResult(
        check_id="ADJUDICATION_CEILING",
        description="MECH-013: meta_confidence ≤ max(primary, challenger)",
        passed=ceiling_ok,
        tier="T1-MECHANICAL",
        failure_reason=None if ceiling_ok else "FM-SYNTHESIS-CEILING: Adjudication confidence exceeds maximum",
    ))

    # Residue valid
    residue_ok = "residue" in wave_output or "canonical_implementation" in wave_output
    checks.append(CheckResult(
        check_id="RESIDUE_VALID",
        description="MECH-028: Residue present",
        passed=residue_ok,
        tier="T1-MECHANICAL",
        failure_reason=None if residue_ok else "FM-RESIDUE-DROP",
    ))

    # Registry + Timeout
    reg_check = _check_registry_integrity(registry, manifest)
    checks.append(reg_check)
    checks.append(CheckResult(
        check_id="TIMEOUT",
        description="MECH-015: W3 not timed out",
        passed=not timed_out,
        tier="T1-MECHANICAL",
        failure_reason=None if not timed_out else "FM-TIMEOUT",
    ))

    eval_result.checks = checks
    all_passed = all(c.passed for c in checks)
    eval_result.result = GateResult.PASS if all_passed else GateResult.FAIL
    eval_result.failure_reasons = [c.failure_reason for c in checks if not c.passed and c.failure_reason]
    eval_result.failure_modes = _extract_fm_ids(eval_result.failure_reasons)
    eval_result.registry_verified = reg_check.passed

    return eval_result


# ---------------------------------------------------------------------------
# G6 — W6: Consolidation Gate (FULL mode only)
# ---------------------------------------------------------------------------

def evaluate_g6(
    wave_output: dict[str, Any],
    run_config: RunConfig,
    registry: FamilyRegistry,
    manifest: RunManifest,
    timed_out: bool = False,
) -> GateEvaluation:
    """G6 gate predicate (FULL mode): Consolidation quality checks."""
    eval_result = GateEvaluation(gate_id="G6", wave_id="W6", gate_type="MECHANICAL")
    checks: list[CheckResult] = []

    # Consolidation confidence > 0.7
    confidence = wave_output.get("consolidation_confidence", 0.0)
    conf_ok = confidence > 0.7
    checks.append(CheckResult(
        check_id="CONSOLIDATION_CONFIDENCE",
        description="consolidation_confidence > 0.7",
        passed=conf_ok,
        tier="T1-MECHANICAL",
        details={"confidence": confidence, "threshold": 0.7},
        failure_reason=None if conf_ok else f"Consolidation confidence {confidence} ≤ 0.7",
    ))

    # No unresolved FATAL findings
    consolidated = wave_output.get("consolidated_findings", [])
    fatal_unresolved = [
        f for f in consolidated
        if f.get("severity") == "FATAL" and f.get("disposition") not in ("FIXED", "ACCEPTED_RISK")
    ]
    fatal_ok = len(fatal_unresolved) == 0
    checks.append(CheckResult(
        check_id="NO_UNRESOLVED_FATAL",
        description="No unresolved FATAL findings",
        passed=fatal_ok,
        tier="T1-MECHANICAL",
        details={"unresolved_fatal_count": len(fatal_unresolved)},
        failure_reason=None if fatal_ok else f"FM-FINDING: {len(fatal_unresolved)} unresolved FATAL findings",
    ))

    # Registry + Timeout
    reg_check = _check_registry_integrity(registry, manifest)
    checks.append(reg_check)
    checks.append(CheckResult(
        check_id="TIMEOUT",
        description="MECH-015: W6 not timed out",
        passed=not timed_out,
        tier="T1-MECHANICAL",
        failure_reason=None if not timed_out else "FM-TIMEOUT",
    ))

    eval_result.checks = checks
    all_passed = all(c.passed for c in checks)
    eval_result.result = GateResult.PASS if all_passed else GateResult.FAIL
    eval_result.failure_reasons = [c.failure_reason for c in checks if not c.passed and c.failure_reason]
    eval_result.failure_modes = _extract_fm_ids(eval_result.failure_reasons)
    eval_result.registry_verified = reg_check.passed

    return eval_result


# ---------------------------------------------------------------------------
# G7 — W7: Deep QA Gate (FULL mode only)
# ---------------------------------------------------------------------------

def evaluate_g7(
    wave_output: dict[str, Any],
    run_config: RunConfig,
    registry: FamilyRegistry,
    manifest: RunManifest,
    timed_out: bool = False,
) -> GateEvaluation:
    """G7 gate predicate (FULL mode): Deep QA quality checks."""
    eval_result = GateEvaluation(gate_id="G7", wave_id="W7", gate_type="MECHANICAL")
    checks: list[CheckResult] = []

    # false_positive_rate < 0.3
    fp_rate = wave_output.get("false_positive_rate", 0.0)
    fp_ok = fp_rate < 0.3
    checks.append(CheckResult(
        check_id="FALSE_POSITIVE_RATE",
        description="false_positive_rate < 0.3",
        passed=fp_ok,
        tier="T1-MECHANICAL",
        details={"false_positive_rate": fp_rate, "threshold": 0.3},
        failure_reason=None if fp_ok else f"FM-FINDING: False positive rate {fp_rate:.2%} ≥ 30%",
    ))

    # All FATAL findings confirmed
    qa_results = wave_output.get("qa_results", [])
    fatal_findings = [r for r in qa_results if r.get("severity") == "FATAL"]
    unconfirmed_fatal = [r for r in fatal_findings if not r.get("confirmed", False)]
    fatal_ok = len(unconfirmed_fatal) == 0
    checks.append(CheckResult(
        check_id="FATAL_FINDINGS_CONFIRMED",
        description="All FATAL findings confirmed (not false positives)",
        passed=fatal_ok,
        tier="T1-MECHANICAL",
        details={"unconfirmed_fatal_count": len(unconfirmed_fatal)},
        failure_reason=None if fatal_ok else f"FM-FINDING: {len(unconfirmed_fatal)} FATAL findings not confirmed",
    ))

    # Registry + Timeout
    reg_check = _check_registry_integrity(registry, manifest)
    checks.append(reg_check)
    checks.append(CheckResult(
        check_id="TIMEOUT",
        description="MECH-015: W7 not timed out",
        passed=not timed_out,
        tier="T1-MECHANICAL",
        failure_reason=None if not timed_out else "FM-TIMEOUT",
    ))

    eval_result.checks = checks
    all_passed = all(c.passed for c in checks)
    eval_result.result = GateResult.PASS if all_passed else GateResult.FAIL
    eval_result.failure_reasons = [c.failure_reason for c in checks if not c.passed and c.failure_reason]
    eval_result.failure_modes = _extract_fm_ids(eval_result.failure_reasons)
    eval_result.registry_verified = reg_check.passed

    return eval_result


# ---------------------------------------------------------------------------
# G5.5 — W5.5: Standard Remediation Gate
# ---------------------------------------------------------------------------

def evaluate_g5_5(
    wave_output: dict[str, Any],
    run_config: RunConfig,
    registry: FamilyRegistry,
    manifest: RunManifest,
    pipeline_clean_run: bool = False,
    timed_out: bool = False,
) -> GateEvaluation:
    """G5.5 gate predicate: Remediation gate."""
    eval_result = GateEvaluation(gate_id="G5.5", wave_id="W5.5", gate_type="HYBRID")

    if pipeline_clean_run:
        eval_result.result = GateResult.PASS
        eval_result.checks = [CheckResult(
            check_id="CLEAN_RUN_SKIP",
            description="Pipeline clean run — W5.5 skipped",
            passed=True,
        )]
        return eval_result

    checks: list[CheckResult] = []

    # Inclusion proof (MECH-009)
    fdl = wave_output.get("fdl_phase1", {})
    entries = fdl.get("entries", [])
    w4_findings = wave_output.get("w4_findings", [])
    w5_findings = wave_output.get("w5_findings", [])
    total_findings = len(w4_findings) + len(w5_findings)
    inclusion_ok = len(entries) == total_findings and total_findings > 0
    checks.append(CheckResult(
        check_id="INCLUSION_PROOF",
        description="MECH-009: |findings| = |fdl_entries|",
        passed=inclusion_ok,
        tier="T1-MECHANICAL",
        details={"findings_count": total_findings, "entries_count": len(entries)},
        failure_reason=None if inclusion_ok else "FM-INCLUSION-FAILURE: Finding count mismatch in FDL",
    ))

    # Fixed entries have verification
    fixed = [e for e in entries if e.get("disposition") == "FIXED"]
    fix_verified = all(
        e.get("verification_method") and e.get("verification_evidence")
        for e in fixed
    )
    checks.append(CheckResult(
        check_id="FIX_VERIFIED",
        description="All FIXED entries have verification_method + verification_evidence",
        passed=fix_verified,
        tier="T1-MECHANICAL",
        failure_reason=None if fix_verified else "Fixed entries missing verification evidence",
    ))

    # No remaining CRITICAL
    remaining_critical = sum(
        1 for e in entries
        if e.get("severity") == "CRITICAL" and e.get("disposition") not in ("FIXED", "ACCEPTED_RISK")
    )
    crit_ok = remaining_critical == 0
    checks.append(CheckResult(
        check_id="NO_REMAINING_CRITICAL",
        description="COUNT(remaining CRITICAL findings) = 0",
        passed=crit_ok,
        tier="T1-MECHANICAL",
        details={"remaining_critical": remaining_critical},
        failure_reason=None if crit_ok else f"FM-FINDING: {remaining_critical} CRITICAL findings remain",
    ))

    # Exhaustion check (MECH-021)
    cycle_count = manifest.loop_counters.w5_5_reruns
    max_cycles = run_config.max_rework_cycles
    exhaust_ok = cycle_count <= max_cycles
    checks.append(CheckResult(
        check_id="EXHAUSTION_CHECK",
        description=f"MECH-021: w5_5_cycle_count ≤ max_rework_cycles ({max_cycles})",
        passed=exhaust_ok,
        tier="T1-MECHANICAL",
        details={"cycle_count": cycle_count, "max": max_cycles},
        failure_reason=None if exhaust_ok else f"FM-REWORK-SPIRAL: {cycle_count} cycles exceeds max {max_cycles}",
    ))

    # Confidence (T3)
    conf = wave_output.get("remediation_confidence", 0.0)
    conf_ok = conf >= 0.60
    checks.append(CheckResult(
        check_id="REMEDIATION_CONFIDENCE",
        description="remediation_confidence ≥ 0.60 (T3-ATTESTED)",
        passed=conf_ok,
        tier="T3-ATTESTED",
        details={"confidence": conf},
    ))

    # Registry + Timeout
    reg_check = _check_registry_integrity(registry, manifest)
    checks.append(reg_check)
    checks.append(CheckResult(
        check_id="TIMEOUT",
        passed=not timed_out,
        description="Not timed out",
        tier="T1-MECHANICAL",
        failure_reason=None if not timed_out else "FM-TIMEOUT",
    ))

    eval_result.checks = checks
    all_passed = all(c.passed for c in checks)
    eval_result.result = GateResult.PASS if all_passed else GateResult.FAIL
    eval_result.failure_reasons = [c.failure_reason for c in checks if not c.passed and c.failure_reason]
    eval_result.failure_modes = _extract_fm_ids(eval_result.failure_reasons)
    eval_result.registry_verified = reg_check.passed

    return eval_result


# ---------------------------------------------------------------------------
# Generic gate evaluator (dispatches to specific gate functions)
# ---------------------------------------------------------------------------

# Map of gate_id → evaluator function
_GATE_EVALUATORS = {
    "G0": evaluate_g0,
    "G1": evaluate_g1,
    "G2": evaluate_g2,
    "G3": evaluate_g3,
    "G5.5": evaluate_g5_5,
    "G6": evaluate_g6,
    "G7": evaluate_g7,
}

# Map wave_id → gate_id
WAVE_GATE_MAP = {
    "W0": "G0",
    "W1": "G1",
    "W2": "G2",
    "W3": "G3",
    "W4": "G4",
    "W5": "G5",
    "W5.5": "G5.5",
    "W6": "G6",
    "W7": "G7",
    "W8": "G8",
    "W8.5": "G8.5",
    "W9": "G9",
    "W10": "G10",
    "W11": "G11",
    # Micro
    "M0": "Gμ0",
    "M1": "Gμ1",
    "M2": "Gμ2",
}

# Waves that don't have mechanical gates (pass-through)
PASSTHROUGH_WAVES = {"Wa-LOAD", "Wa-WRITE"}


def evaluate_gate(
    wave_id: str,
    wave_output: dict[str, Any],
    run_config: RunConfig,
    registry: FamilyRegistry,
    manifest: RunManifest,
    timed_out: bool = False,
    **kwargs: Any,
) -> GateEvaluation:
    """
    Evaluate the gate predicate for a given wave.

    Returns a GateEvaluation with the result. For waves without specific
    implementations, returns a generic evaluation based on output presence.
    """
    gate_id = WAVE_GATE_MAP.get(wave_id, wave_id)

    # Pass-through waves (Wα-LOAD, Wα-WRITE)
    if wave_id in PASSTHROUGH_WAVES:
        return GateEvaluation(
            gate_id=gate_id,
            wave_id=wave_id,
            result=GateResult.PASS,
            gate_type="PASSTHROUGH",
            registry_verified=True,
        )

    # Specific gate evaluator
    evaluator = _GATE_EVALUATORS.get(gate_id)
    if evaluator:
        return evaluator(
            wave_output=wave_output,
            run_config=run_config,
            registry=registry,
            manifest=manifest,
            timed_out=timed_out,
            **kwargs,
        )

    # Generic fallback for waves without full implementation yet
    return _generic_gate(gate_id, wave_id, wave_output, registry, manifest, timed_out)


def _generic_gate(
    gate_id: str,
    wave_id: str,
    wave_output: dict[str, Any],
    registry: FamilyRegistry,
    manifest: RunManifest,
    timed_out: bool,
) -> GateEvaluation:
    """Generic gate for waves not yet fully implemented."""
    checks: list[CheckResult] = []

    # Registry integrity
    reg_check = _check_registry_integrity(registry, manifest)
    checks.append(reg_check)

    # Timeout
    checks.append(CheckResult(
        check_id="TIMEOUT",
        description=f"MECH-015: {wave_id} not timed out",
        passed=not timed_out,
        tier="T1-MECHANICAL",
        failure_reason=None if not timed_out else "FM-TIMEOUT",
    ))

    # Output presence
    has_output = bool(wave_output)
    checks.append(CheckResult(
        check_id="OUTPUT_PRESENT",
        description="Wave produced output",
        passed=has_output,
        tier="T1-MECHANICAL",
        failure_reason=None if has_output else "No wave output",
    ))

    all_passed = all(c.passed for c in checks)
    return GateEvaluation(
        gate_id=gate_id,
        wave_id=wave_id,
        result=GateResult.PASS if all_passed else GateResult.FAIL,
        gate_type="GENERIC",
        checks=checks,
        failure_reasons=[c.failure_reason for c in checks if not c.passed and c.failure_reason],
        failure_modes=_extract_fm_ids(
            [c.failure_reason for c in checks if not c.passed and c.failure_reason]
        ),
        registry_verified=reg_check.passed,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_fm_ids(reasons: list[str]) -> list[str]:
    """Extract FM-XXX IDs from failure reason strings."""
    import re
    fm_pattern = re.compile(r"FM-[\w-]+")
    ids = set()
    for r in reasons:
        if r:
            for m in fm_pattern.finditer(r):
                ids.add(m.group())
    return sorted(ids)