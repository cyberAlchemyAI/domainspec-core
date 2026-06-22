"""
Z-Rig Pipeline Module — Wave state machine, failure routing, and pipeline execution.

This is the core engine that drives a Z-Rig pipeline run through its wave
sequence, evaluating gates, enforcing bounds, routing failures, and maintaining
checkpoints.

State Machine:
  PENDING → RUNNING → GATED → PASSED | FAILED | TIMED_OUT
  Checkpoint at every wave boundary.

Failure Routing:
  Per the spec's failure routing table, gates that fail route to:
  - REWORK: retry the same wave (bounded by loop counters)
  - RETURN: return to a prior wave with directives
  - ESCALATE: human escalation (PIPELINE_PAUSED)
  - HALT: PIPELINE_HALTED (unrecoverable)
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Awaitable

from .config import FamilyRegistry, Mode, PipelineBounds, RunConfig, TaskDescription
from .classifier import mode_select, ModeSelectResult
from .gates import (
    GateEvaluation,
    GateResult,
    evaluate_gate,
    PASSTHROUGH_WAVES,
    WAVE_GATE_MAP,
)
from .manifest import (
    RunManifest,
    RunStatus,
    WaveRecord,
    WaveStatus,
    waves_for_mode,
)
from .residue import ResidueStore, PerWaveResidue


logger = logging.getLogger("zrig.pipeline")


# ---------------------------------------------------------------------------
# Wave execution state
# ---------------------------------------------------------------------------

class WaveState(str, Enum):
    """Internal wave state for the state machine."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    GATED = "GATED"       # Gate evaluation in progress
    PASSED = "PASSED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    SKIPPED = "SKIPPED"


# ---------------------------------------------------------------------------
# Failure routing
# ---------------------------------------------------------------------------

class FailureAction(str, Enum):
    """What to do when a gate fails."""
    REWORK = "REWORK"        # Retry this wave
    RETURN = "RETURN"        # Return to a prior wave
    ESCALATE = "ESCALATE"    # Human escalation
    HALT = "HALT"            # Pipeline halt


@dataclass
class FailureRoute:
    """Routing decision for a gate failure."""
    action: FailureAction
    target_wave: str | None = None   # For RETURN: which wave to go back to
    fm_id: str = ""                  # Failure mode ID
    reason: str = ""
    loop_counter_field: str | None = None  # Which counter to increment
    max_retries: int = 0             # Max retries before escalation


# Standard Mode failure routing table per the spec
_FAILURE_ROUTING: dict[str, list[FailureRoute]] = {
    "W0": [
        FailureRoute(FailureAction.HALT, fm_id="FM-PROVIDER", reason="Provider unavailable, no failover"),
        FailureRoute(FailureAction.HALT, fm_id="FM-DIVERSITY", reason="Diversity unsatisfiable"),
        FailureRoute(FailureAction.HALT, fm_id="FM-CONFIG", reason="Invalid run_config"),
        FailureRoute(FailureAction.HALT, fm_id="FM-TIMEOUT", reason="W0 timeout"),
    ],
    "W1": [
        FailureRoute(FailureAction.REWORK, fm_id="FM-SPEC", reason="No MUST requirements",
                     loop_counter_field="w2_reruns", max_retries=1),
        FailureRoute(FailureAction.REWORK, fm_id="FM-BLUEPRINT-WEAK", reason="Blueprint specificity insufficient",
                     loop_counter_field="w2_reruns", max_retries=1),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-EXHAUSTION", reason="No consensus after retries"),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-TIMEOUT", reason="W1 timeout"),
    ],
    "W2": [
        FailureRoute(FailureAction.REWORK, fm_id="FM-FINDING", reason="<2 builders succeed",
                     loop_counter_field="w2_reruns", max_retries=2),
        FailureRoute(FailureAction.HALT, fm_id="FM-EXHAUSTION", reason="<2 builders, no reruns left"),
        FailureRoute(FailureAction.HALT, fm_id="FM-DIVERSITY", reason="Diversity violation"),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-TIMEOUT", reason="W2 timeout"),
    ],
    "W3": [
        FailureRoute(FailureAction.RETURN, target_wave="W2", fm_id="FM-FINDING",
                     reason="MUST gap", loop_counter_field="w2_reruns", max_retries=1),
        FailureRoute(FailureAction.REWORK, fm_id="FM-SYNTHESIS-CEILING", reason="Adjudication ceiling breach",
                     loop_counter_field="w3_challenger_retries", max_retries=1),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-OVERSIZE-PACK", reason="Section pack exceeds limits"),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-TIMEOUT", reason="W3 timeout"),
    ],
    "W4": [
        FailureRoute(FailureAction.HALT, fm_id="FM-TRACE-GAP", reason="Trace failure is a BLOCKER"),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-FINDING", reason="FATAL findings"),
        FailureRoute(FailureAction.REWORK, fm_id="FM-INDEPENDENCE", reason="Cross-assignment violation"),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-TIMEOUT", reason="W4 timeout"),
    ],
    "W5": [
        FailureRoute(FailureAction.REWORK, fm_id="FM-FINDING", reason="Critical findings need remediation",
                     loop_counter_field="w5_reruns", max_retries=2),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-INDEPENDENCE", reason="Independence violation"),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-TIMEOUT", reason="W5 timeout"),
    ],
    "W5.5": [
        FailureRoute(FailureAction.REWORK, fm_id="FM-INCLUSION-FAILURE", reason="Inclusion proof failure"),
        FailureRoute(FailureAction.REWORK, fm_id="FM-FINDING", reason="Remaining CRITICAL findings",
                     loop_counter_field="w5_5_reruns", max_retries=1),
        FailureRoute(FailureAction.HALT, fm_id="FM-REWORK-SPIRAL", reason="max_rework_cycles exceeded"),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-TIMEOUT", reason="W5.5 timeout"),
    ],
    "W8": [
        FailureRoute(FailureAction.REWORK, fm_id="FM-FINDING", reason="User testing failures"),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-TIMEOUT", reason="W8 timeout"),
    ],
    "W8.5": [
        FailureRoute(FailureAction.HALT, fm_id="FM-ORCHESTRATOR", reason="FDL phase1 preservation failure"),
        FailureRoute(FailureAction.HALT, fm_id="FM-TIMEOUT", reason="W8.5 timeout"),
    ],
    "W9": [
        FailureRoute(FailureAction.RETURN, target_wave="W2", fm_id="FM-FINDING",
                     reason="Panel REJECT → rework", loop_counter_field="w9_returns", max_retries=1),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-TIMEOUT", reason="W9 timeout"),
    ],
    "W10": [
        FailureRoute(FailureAction.HALT, fm_id="FM-FINDING", reason="Deployment failure"),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-TIMEOUT", reason="W10 timeout"),
    ],
    "W11": [
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-FINDING", reason="Sentinel findings"),
        FailureRoute(FailureAction.ESCALATE, fm_id="FM-TIMEOUT", reason="W11 timeout"),
    ],
}


def route_failure(
    wave_id: str,
    gate_eval: GateEvaluation,
    manifest: RunManifest,
    bounds: PipelineBounds,
) -> FailureRoute:
    """
    Determine the failure routing for a gate that failed.

    Uses the spec's failure routing tables and checks loop counters
    against pipeline bounds.
    """
    fm_ids = gate_eval.failure_modes
    routes = _FAILURE_ROUTING.get(wave_id, [])

    # Find the first matching route by FM-ID
    for route in routes:
        if route.fm_id in fm_ids:
            # Check if we've exhausted retries for rework/return actions
            if route.action in (FailureAction.REWORK, FailureAction.RETURN):
                current_count = _get_loop_counter(manifest, route.loop_counter_field)
                max_allowed = _get_bound(bounds, route.loop_counter_field, route.max_retries)
                if current_count >= max_allowed:
                    # Exhausted → escalate or halt
                    return FailureRoute(
                        action=FailureAction.ESCALATE,
                        fm_id="FM-EXHAUSTION",
                        reason=f"Retry budget exhausted for {wave_id} ({current_count}/{max_allowed})",
                    )
            return route

    # Default: first FM → escalate
    if fm_ids:
        return FailureRoute(
            action=FailureAction.ESCALATE,
            fm_id=fm_ids[0],
            reason=f"No specific route for {fm_ids[0]} at {wave_id}",
        )

    # Ultimate fallback
    return FailureRoute(
        action=FailureAction.ESCALATE,
        fm_id="FM-SPEC",
        reason=f"Gate failed at {wave_id} with no classified failure mode",
    )


def _get_loop_counter(manifest: RunManifest, counter_field: str | None) -> int:
    if not counter_field:
        return 0
    return getattr(manifest.loop_counters, counter_field, 0)


def _get_bound(bounds: PipelineBounds, counter_field: str | None, default: int) -> int:
    if not counter_field:
        return default
    bound_field = f"max_{counter_field}"
    return getattr(bounds, bound_field, default)


def _increment_loop_counter(manifest: RunManifest, counter_field: str | None) -> None:
    if counter_field and hasattr(manifest.loop_counters, counter_field):
        current = getattr(manifest.loop_counters, counter_field)
        setattr(manifest.loop_counters, counter_field, current + 1)


# ---------------------------------------------------------------------------
# Pipeline exhaustion check (MECH-021)
# ---------------------------------------------------------------------------

def check_pipeline_exhaustion(
    manifest: RunManifest,
    bounds: PipelineBounds,
) -> tuple[bool, str | None]:
    """
    MECH-021: PIPELINE_EXHAUSTION_CHECK

    Verify no loop counter has exceeded its maximum bound.
    Returns (exhausted: bool, reason: str | None).
    """
    checks = [
        ("w2_reruns", bounds.max_w2_reruns),
        ("w3_challenger_retries", bounds.max_w3_challenger_retries),
        ("w5_reruns", bounds.max_w5_reruns),
        ("w5_5_reruns", bounds.max_w5_5_reruns),
        ("w6_remediation_cycles", bounds.max_w6_remediation_cycles),
        ("w9_returns", bounds.max_w9_returns),
        ("micro_discards", bounds.max_micro_discards),
    ]
    for counter_name, max_val in checks:
        current = getattr(manifest.loop_counters, counter_name, 0)
        if current > max_val:
            return True, f"FM-EXHAUSTION: {counter_name}={current} exceeds max={max_val}"
    return False, None


# ---------------------------------------------------------------------------
# Wave executor type
# ---------------------------------------------------------------------------

# A wave executor is an async function that receives the wave context and
# returns the wave output dict. In a real deployment, this dispatches to
# actual LLM agents. For testing, stubs return predefined outputs.
WaveExecutor = Callable[
    [str, dict[str, Any], RunConfig, RunManifest],
    Awaitable[dict[str, Any]],
]


# ---------------------------------------------------------------------------
# Pipeline Runner
# ---------------------------------------------------------------------------

@dataclass
class PipelineResult:
    """Result of a complete pipeline run."""
    run_id: str = ""
    status: str = ""
    mode: str = ""
    waves_completed: list[str] = field(default_factory=list)
    waves_failed: list[str] = field(default_factory=list)
    waves_skipped: list[str] = field(default_factory=list)
    failure_events: list[dict[str, Any]] = field(default_factory=list)
    manifest_path: str | None = None
    halt_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "status": self.status,
            "mode": self.mode,
            "waves_completed": self.waves_completed,
            "waves_failed": self.waves_failed,
            "waves_skipped": self.waves_skipped,
            "failure_events": self.failure_events,
            "manifest_path": self.manifest_path,
            "halt_reason": self.halt_reason,
        }


class Pipeline:
    """
    The Z-Rig pipeline engine.

    Drives a run through its wave sequence, evaluating gates at each boundary,
    routing failures, enforcing bounds, and checkpointing state.
    """

    def __init__(
        self,
        run_config: RunConfig,
        task: TaskDescription,
        registry: FamilyRegistry | None = None,
        output_dir: str | Path = ".",
        wave_executor: WaveExecutor | None = None,
    ):
        self.run_config = run_config
        self.task = task
        self.registry = registry or FamilyRegistry.default()
        self.output_dir = Path(output_dir)
        self.run_dir = self.output_dir / run_config.run_id
        self._wave_executor = wave_executor or _default_wave_executor

        # These are set during run()
        self.manifest: RunManifest | None = None
        self.mode_result: ModeSelectResult | None = None
        self.effective_mode: Mode = Mode.STANDARD

    async def run(self) -> PipelineResult:
        """
        Execute the full pipeline.

        Returns a PipelineResult with the outcome.
        """
        result = PipelineResult(run_id=self.run_config.run_id)

        try:
            # --- Phase 1: Mode selection ---
            self.mode_result = mode_select(self.run_config, self.task)
            self.effective_mode = self.mode_result.selected_mode
            result.mode = self.effective_mode.value

            logger.info(
                "Mode selected: %s (requested: %s, auto_escalated: %s)",
                self.effective_mode.value,
                self.run_config.mode.value,
                self.mode_result.auto_escalated,
            )

            # --- Phase 2: Initialize manifest ---
            registry_hash = self.registry.compute_hash()
            self.manifest = RunManifest.create(
                self.run_config,
                self.effective_mode,
                registry_hash,
            )

            # Record mode escalation if it happened
            if self.mode_result.auto_escalated:
                self.manifest.micro_escalation = {
                    "escalated_from_micro": True,
                    "micro_run_id": None,
                    "escalation_reason": self.mode_result.escalation_reason,
                    "escalation_attempt_number": 1,
                    "micro_build_artifact_ref": None,
                    "micro_residue_forwarded": False,
                }
                if self.mode_result.failure_event:
                    self.manifest.add_failure_event(self.mode_result.failure_event)

            # Create run directory
            self.run_dir.mkdir(parents=True, exist_ok=True)

            # --- Phase 3: Execute waves ---
            wave_sequence = waves_for_mode(self.effective_mode)

            _timeout_count = 0  # MECH-015: consecutive timeout tracker

            wave_idx = 0
            while wave_idx < len(wave_sequence):
                wave_id = wave_sequence[wave_idx]

                # Check pipeline exhaustion before each wave
                exhausted, exhaust_reason = check_pipeline_exhaustion(
                    self.manifest, self.run_config.bounds
                )
                if exhausted:
                    self.manifest.halt(exhaust_reason or "Pipeline exhaustion", "FM-EXHAUSTION")
                    result.status = RunStatus.HALTED
                    result.halt_reason = exhaust_reason
                    result.failure_events = self.manifest.failure_events
                    break

                # Execute wave
                wave_result = await self._execute_wave(wave_id)

                if wave_result == WaveState.PASSED or wave_result == WaveState.SKIPPED:
                    _timeout_count = 0  # MECH-015: reset on success
                    result.waves_completed.append(wave_id)
                    wave_idx += 1
                    continue
                elif wave_result == WaveState.FAILED:
                    result.waves_failed.append(wave_id)

                    # Get the gate evaluation for failure routing
                    gate_eval = self.manifest.waves[wave_id].gate_evaluation
                    gate_eval_obj = GateEvaluation(
                        gate_id=gate_eval.get("gate_id", ""),
                        wave_id=wave_id,
                        result=GateResult.FAIL,
                        failure_modes=gate_eval.get("failure_modes", []),
                        failure_reasons=gate_eval.get("failure_reasons", []),
                    )

                    route = route_failure(
                        wave_id, gate_eval_obj,
                        self.manifest, self.run_config.bounds,
                    )

                    logger.info(
                        "Gate FAIL at %s: action=%s, fm=%s, reason=%s",
                        wave_id, route.action.value, route.fm_id, route.reason,
                    )

                    if route.action == FailureAction.HALT:
                        self.manifest.halt(route.reason, route.fm_id)
                        result.status = RunStatus.HALTED
                        result.halt_reason = route.reason
                        break

                    elif route.action == FailureAction.ESCALATE:
                        self.manifest.pause(wave_id, route.reason, str(uuid.uuid4()))
                        result.status = RunStatus.PAUSED
                        result.halt_reason = f"Human escalation required: {route.reason}"
                        break

                    elif route.action == FailureAction.REWORK:
                        _increment_loop_counter(self.manifest, route.loop_counter_field)
                        # Re-execute the same wave (don't advance wave_idx)
                        logger.info("Reworking wave %s (attempt %d)",
                                    wave_id,
                                    _get_loop_counter(self.manifest, route.loop_counter_field))
                        # Reset wave status for rework
                        self.manifest.waves[wave_id] = WaveRecord()
                        continue

                    elif route.action == FailureAction.RETURN:
                        _increment_loop_counter(self.manifest, route.loop_counter_field)
                        if route.target_wave and route.target_wave in wave_sequence:
                            target_idx = wave_sequence.index(route.target_wave)
                            logger.info("Returning to wave %s from %s", route.target_wave, wave_id)
                            # Reset target wave and all subsequent waves
                            for reset_idx in range(target_idx, wave_idx + 1):
                                reset_wid = wave_sequence[reset_idx]
                                self.manifest.waves[reset_wid] = WaveRecord()
                            wave_idx = target_idx
                            continue
                        else:
                            # Can't return to target — escalate
                            self.manifest.pause(wave_id, f"Cannot return to {route.target_wave}")
                            result.status = RunStatus.PAUSED
                            break

                elif wave_result == WaveState.TIMED_OUT:
                    result.waves_failed.append(wave_id)
                    _timeout_count += 1  # MECH-015

                    # MECH-015: timeout cascade — auto-HALT after 3 consecutive
                    if _timeout_count >= 3:
                        cascade_reason = "MECH-015: timeout cascade — 3 consecutive timeouts"
                        logger.error(cascade_reason)
                        self.manifest.halt(cascade_reason, "FM-TIMEOUT-CASCADE")
                        result.status = RunStatus.HALTED
                        result.halt_reason = cascade_reason
                        break

                    # Route through failure table
                    timeout_gate = GateEvaluation(
                        gate_id=f"G-{wave_id}",
                        wave_id=wave_id,
                        result=GateResult.TIMEOUT,
                        failure_modes=["FM-TIMEOUT"],
                        failure_reasons=[f"Wave {wave_id} timed out"],
                    )
                    route = route_failure(
                        wave_id, timeout_gate,
                        self.manifest, self.run_config.bounds,
                    )
                    if route.action == FailureAction.HALT:
                        self.manifest.halt(route.reason, route.fm_id)
                        result.status = RunStatus.HALTED
                        result.halt_reason = route.reason
                        break
                    elif route.action == FailureAction.REWORK:
                        _increment_loop_counter(self.manifest, route.loop_counter_field)
                        self.manifest.waves[wave_id] = WaveRecord()
                        continue  # retry same wave
                    else:
                        self.manifest.pause(wave_id, f"Timeout at {wave_id}", str(uuid.uuid4()))
                        result.status = RunStatus.PAUSED
                        result.halt_reason = f"Timeout at {wave_id}"
                        break

            else:
                # All waves completed successfully
                self.manifest.complete_run()
                result.status = RunStatus.COMPLETED

        except Exception as e:
            logger.exception("Pipeline execution error: %s", e)
            if self.manifest:
                self.manifest.halt(f"Orchestrator error: {e}", "FM-ORCHESTRATOR")
            result.status = RunStatus.HALTED
            result.halt_reason = str(e)

        # MECH-035/036: Necronomicon Memory Loop — write residue
        if self.manifest:
            try:
                residue_store = ResidueStore(self.run_dir / "residue_store.jsonl")
                wave_residues = []
                for wid, wrec in self.manifest.waves.items():
                    raw = getattr(wrec, "residue", None) or []
                    if raw:
                        wave_residues.append(PerWaveResidue(
                            run_id=self.manifest.run_id, wave_id=wid,
                            entries=raw if isinstance(raw, list) else [str(raw)],
                        ))
                if wave_residues:
                    residue_store.write_residue(wave_residues, {}, self.manifest.registry_hash)
                    logger.info("Necronomicon: wrote %d residue records", len(wave_residues))
            except Exception as e:
                logger.warning("Residue write failed (non-fatal): %s", e)

        # Save final manifest
        if self.manifest:
            manifest_path = self.manifest.save(self.run_dir)
            self.manifest.save_checkpoint(self.run_dir, "FINAL")
            result.manifest_path = str(manifest_path)
            result.failure_events = self.manifest.failure_events

        return result

    async def _execute_wave(self, wave_id: str) -> WaveState:
        """Execute a single wave and evaluate its gate."""
        manifest = self.manifest
        assert manifest is not None

        # Skip conditional waves on clean run path
        if wave_id in ("W5.5", "W8.5") and manifest.pipeline_clean_run:
            manifest.skip_wave(wave_id, reason="pipeline_clean_run")
            manifest.save_checkpoint(self.run_dir, wave_id)
            return WaveState.SKIPPED

        # Start wave
        manifest.start_wave(wave_id)
        logger.info("Starting wave %s", wave_id)

        manifest.add_structured_event({
            "type": "WAVE_STARTED",
            "wave": wave_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        try:
            # Build context for wave executor
            context = self._build_wave_context(wave_id)

            # Execute wave (dispatch to agents)
            wave_output = await self._wave_executor(
                wave_id, context, self.run_config, manifest,
            )

            # Evaluate gate
            timed_out = wave_output.get("_timed_out", False)
            gate_eval = evaluate_gate(
                wave_id=wave_id,
                wave_output=wave_output,
                run_config=self.run_config,
                registry=self.registry,
                manifest=manifest,
                timed_out=timed_out,
            )

            # Determine clean run status after W5
            if wave_id == "W5" and gate_eval.passed:
                # Check if any findings require remediation
                findings = wave_output.get("findings", [])
                critical_or_fatal = [
                    f for f in findings
                    if f.get("severity") in ("CRITICAL", "FATAL")
                ]
                if not critical_or_fatal:
                    manifest.pipeline_clean_run = True
                    logger.info("Clean run path: no critical/fatal findings in W4+W5")

            # Record gate result
            gate_result = gate_eval.result
            manifest.complete_wave(
                wave_id=wave_id,
                gate_result=gate_result,
                gate_evaluation=gate_eval.to_dict(),
                artifacts=wave_output.get("artifact_ids", []),
                findings=wave_output.get("findings", []),
                residue=wave_output.get("residue", {}),
                failure_events=[
                    {"fm_id": fm, "wave": wave_id}
                    for fm in gate_eval.failure_modes
                ] if not gate_eval.passed else None,
            )

            # Checkpoint
            manifest.save_checkpoint(self.run_dir, wave_id)

            if gate_result == GateResult.PASS:
                logger.info("Gate %s PASSED for wave %s", gate_eval.gate_id, wave_id)
                return WaveState.PASSED
            elif gate_result == GateResult.TIMEOUT:
                logger.warning("Gate %s TIMEOUT for wave %s", gate_eval.gate_id, wave_id)
                return WaveState.TIMED_OUT
            else:
                logger.warning(
                    "Gate %s FAILED for wave %s: %s",
                    gate_eval.gate_id, wave_id,
                    "; ".join(gate_eval.failure_reasons),
                )
                return WaveState.FAILED

        except Exception as e:
            logger.exception("Wave %s execution error: %s", wave_id, e)
            manifest.complete_wave(
                wave_id=wave_id,
                gate_result=GateResult.FAIL,
                gate_evaluation={"error": str(e)},
                failure_events=[{
                    "fm_id": "FM-ORCHESTRATOR",
                    "wave": wave_id,
                    "error": str(e),
                }],
            )
            manifest.save_checkpoint(self.run_dir, wave_id)
            return WaveState.FAILED

    def _build_wave_context(self, wave_id: str) -> dict[str, Any]:
        """Build the input context for a wave executor."""
        assert self.manifest is not None
        context: dict[str, Any] = {
            "wave_id": wave_id,
            "run_id": self.run_config.run_id,
            "mode": self.effective_mode.value,
            "task_description": self.task._raw,
            "run_config": self.run_config._raw,
            "registry_hash": self.manifest.registry_hash,
        }

        # Add prior wave outputs as context (respecting strip lists)
        # This is a simplified version — full implementation would use
        # the B.5 Bundle Transition Matrix
        prior_waves = {}
        for wid, wrec in self.manifest.waves.items():
            if wrec.status == WaveStatus.COMPLETED and wid != wave_id:
                prior_waves[wid] = {
                    "gate_result": wrec.gate_result,
                    "artifact_ids": wrec.artifact_ids,
                    "residue": wrec.residue,
                }
        context["prior_waves"] = prior_waves

        return context


# ---------------------------------------------------------------------------
# Default wave executor (stub for testing)
# ---------------------------------------------------------------------------

async def _default_wave_executor(
    wave_id: str,
    context: dict[str, Any],
    run_config: RunConfig,
    manifest: RunManifest,
) -> dict[str, Any]:
    """
    Default wave executor stub.

    In production, this dispatches to actual LLM agents.
    For the orchestrator core, it returns a minimal passing output
    so the state machine and gate evaluation can be tested.
    """
    mode = context.get("mode", "STANDARD")

    if wave_id == "W0":
        providers = run_config.provider_list
        return {
            "probe_results": [
                {"model": p, "family": p, "status": "HEALTHY", "latency_ms": 100}
                for p in providers
            ],
            "summary": {
                "healthy_family_count": len(providers),
                "mode_selected": mode,
            },
            "mode_selected": mode,
            "diversity_check": {"min_required": 3, "available": len(providers), "satisfiable": True},
            "registry_hash": manifest.registry_hash,
            "healthy_families": providers,
        }

    elif wave_id in PASSTHROUGH_WAVES:
        return {"status": "OK", "wave": wave_id}

    elif wave_id == "W1":
        return {
            "requirements": {
                "functional": [
                    {"id": f"REQ-{i:03d}", "priority": "MUST", "description": f"Requirement {i}"}
                    for i in range(5)
                ],
            },
            "failure_modes": [{"fm_id": "FM-001", "description": "Stub failure mode"}],
            "rubric": [{"criterion_id": "RC-001", "weight": 1.0, "pass_condition": "Tests pass"}],
            "user_journeys": [
                {"journey_id": f"UJ-{i:03d}", "description": f"Journey {i}", "steps": ["a", "b", "c"]}
                for i in range(3)
            ],
            "panel_consensus": {"agreement_level": "unanimous", "vote_counts": {}},
            "w1_synthesis_confidence": 0.85,
            "residue": {"minority_dissent": [], "wave_id": "W1"},
        }

    elif wave_id == "W2":
        return {
            "builders": [
                {"model_actual": p, "family_actual": p,
                 "build_status": "SUCCESS", "artifact_id": f"art-{i}",
                 "residue": {"wave_id": "W2"}}
                for i, p in enumerate(run_config.provider_list[:3])
            ],
            "residue": {"wave_id": "W2"},
        }

    elif wave_id == "W3":
        return {
            "primary_completed": True,
            "selection_basis": {"must_satisfied": 5, "must_total": 5, "coverage_rate": 0.98},
            "synthesis_confidence": 0.85,
            "challenger_invoked": False,
            "canonical_implementation": {"files": []},
            "residue": {"wave_id": "W3"},
        }

    # Generic passing output for other waves
    return {
        "status": "completed",
        "wave": wave_id,
        "primary_completed": True,
        "residue": {"wave_id": wave_id, "no_residue_reason": "stub executor"},
    }


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------

async def run_pipeline(
    run_config: RunConfig,
    task: TaskDescription,
    registry: FamilyRegistry | None = None,
    output_dir: str | Path = ".",
    wave_executor: WaveExecutor | None = None,
) -> PipelineResult:
    """
    High-level entry point to run a Z-Rig pipeline.

    Args:
        run_config: Parsed run configuration
        task: Parsed task description
        registry: Family registry (default if not provided)
        output_dir: Directory for run artifacts
        wave_executor: Custom wave executor (uses stub if not provided)

    Returns:
        PipelineResult with the outcome
    """
    pipeline = Pipeline(
        run_config=run_config,
        task=task,
        registry=registry,
        output_dir=output_dir,
        wave_executor=wave_executor,
    )
    return await pipeline.run()
