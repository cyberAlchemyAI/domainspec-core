"""
Z-Rig Manifest Module — Run manifest management per v5.5.3 spec.

Creates, updates, checkpoints, and persists the run manifest.
The manifest is the single source of truth for a pipeline run.
"""

from __future__ import annotations

import hashlib
import json
import os
from copy import deepcopy
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import __spec_version__
from .config import Mode, RunConfig, TaskDescription


# ---------------------------------------------------------------------------
# Wave status enum (string-based for JSON compat)
# ---------------------------------------------------------------------------

class WaveStatus:
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    TIMED_OUT = "TIMED_OUT"


class RunStatus:
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    HALTED = "HALTED"
    PAUSED = "PAUSED"


class GateResult:
    PASS = "PASS"
    FAIL = "FAIL"
    TIMEOUT = "TIMEOUT"


# ---------------------------------------------------------------------------
# Standard wave sequences by mode
# ---------------------------------------------------------------------------

STANDARD_WAVES = [
    "W0", "Wa-LOAD", "W1", "W2", "W3", "W4", "W5",
    "W5.5", "W8", "W8.5", "W9", "W10", "W11", "Wa-WRITE",
]

MICRO_WAVES = ["M0", "M1", "M2"]

FULL_WAVES = [
    "W0", "Wa-LOAD", "W1", "W2", "W3", "W4", "W5",
    "W5.5", "W6", "W7", "W8", "W8.5", "W9", "W10", "W11", "Wa-WRITE",
]


def waves_for_mode(mode: Mode) -> list[str]:
    if mode == Mode.MICRO:
        return list(MICRO_WAVES)
    elif mode == Mode.FULL:
        return list(FULL_WAVES)
    return list(STANDARD_WAVES)


# ---------------------------------------------------------------------------
# Wave record
# ---------------------------------------------------------------------------

@dataclass
class WaveRecord:
    status: str = WaveStatus.PENDING
    started_at: str | None = None
    completed_at: str | None = None
    gate_result: str | None = None
    gate_evaluation: dict[str, Any] = field(default_factory=dict)
    agents: list[dict[str, Any]] = field(default_factory=list)
    artifact_ids: list[str] = field(default_factory=list)
    findings: list[dict[str, Any]] = field(default_factory=list)
    residue: dict[str, Any] = field(default_factory=dict)
    failure_events: list[dict[str, Any]] = field(default_factory=list)
    metrics_contribution: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "gate_result": self.gate_result,
            "gate_evaluation": self.gate_evaluation,
            "agents": self.agents,
            "artifact_ids": self.artifact_ids,
            "findings": self.findings,
            "residue": self.residue,
            "failure_events": self.failure_events,
            "metrics_contribution": self.metrics_contribution,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WaveRecord:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# ---------------------------------------------------------------------------
# Loop counters
# ---------------------------------------------------------------------------

@dataclass
class LoopCounters:
    w2_reruns: int = 0
    w3_challenger_retries: int = 0
    w5_reruns: int = 0
    w5_5_reruns: int = 0
    w6_remediation_cycles: int = 0
    w9_returns: int = 0
    micro_discards: int = 0

    def to_dict(self) -> dict[str, int]:
        return {
            "w2_reruns": self.w2_reruns,
            "w3_challenger_retries": self.w3_challenger_retries,
            "w5_reruns": self.w5_reruns,
            "w5_5_reruns": self.w5_5_reruns,
            "w6_remediation_cycles": self.w6_remediation_cycles,
            "w9_returns": self.w9_returns,
            "micro_discards": self.micro_discards,
        }

    @classmethod
    def from_dict(cls, data: dict[str, int]) -> LoopCounters:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# ---------------------------------------------------------------------------
# Run Manifest
# ---------------------------------------------------------------------------

@dataclass
class RunManifest:
    """The single source of truth for a pipeline run."""
    manifest_version: str = __spec_version__
    run_id: str = ""
    spec_version: str = __spec_version__
    mode: str = Mode.STANDARD.value
    created_at: str = ""
    completed_at: str | None = None
    status: str = RunStatus.RUNNING

    run_config_summary: dict[str, Any] = field(default_factory=dict)
    registry_hash: str = ""
    pipeline_clean_run: bool | None = None

    waves: dict[str, WaveRecord] = field(default_factory=dict)
    loop_counters: LoopCounters = field(default_factory=LoopCounters)

    failure_events: list[dict[str, Any]] = field(default_factory=list)
    human_escalations: list[dict[str, Any]] = field(default_factory=list)
    structured_events: list[dict[str, Any]] = field(default_factory=list)
    pipeline_metrics: dict[str, Any] = field(default_factory=dict)
    cumulative_residue: dict[str, Any] = field(default_factory=dict)
    trigger_events: list[dict[str, Any]] = field(default_factory=list)
    operator_overrides: list[dict[str, Any]] = field(default_factory=list)

    micro_escalation: dict[str, Any] = field(default_factory=lambda: {
        "escalated_from_micro": False,
        "micro_run_id": None,
        "escalation_reason": None,
        "escalation_attempt_number": None,
        "micro_build_artifact_ref": None,
        "micro_residue_forwarded": False,
    })

    # --- Factory ---

    @classmethod
    def create(
        cls,
        run_config: RunConfig,
        mode: Mode,
        registry_hash: str,
    ) -> RunManifest:
        """Create a fresh manifest at W0 initialization."""
        now = datetime.now(timezone.utc).isoformat()

        wave_ids = waves_for_mode(mode)
        waves = {wid: WaveRecord() for wid in wave_ids}

        return cls(
            run_id=run_config.run_id,
            mode=mode.value,
            created_at=now,
            status=RunStatus.RUNNING,
            run_config_summary={
                "artifact_type": run_config.artifact_type,
                "artifact_domain_tags": run_config.artifact_domain_tags,
                "stakes_level": run_config.stakes_level.value,
                "scope_ambiguity": run_config.scope_ambiguity.value,
                "deterministic_metric_defined": run_config.deterministic_metric_defined,
                "deterministic_metric_id": run_config.deterministic_metric_id,
                "force_challenger": run_config.force_challenger,
                "w1_panel_size": run_config.w1_panel_size,
                "w2_builder_count": run_config.w2_builder_count,
                "w4_verifier_count": run_config.w4_verifier_count,
                "w5_squad_count": run_config.w5_squad_count,
                "w9_panel_size": run_config.w9_panel_size,
                "max_rework_cycles": run_config.max_rework_cycles,
                "provider_list": run_config.provider_list,
                "deployment_config": run_config.deployment_config,
                "custom_timeouts": run_config.custom_timeouts,
                "custom_bounds": run_config.custom_bounds,
            },
            registry_hash=registry_hash,
            waves=waves,
            loop_counters=LoopCounters(),
        )

    # --- Wave lifecycle ---

    def start_wave(self, wave_id: str) -> None:
        """Mark a wave as RUNNING."""
        if wave_id not in self.waves:
            self.waves[wave_id] = WaveRecord()
        self.waves[wave_id].status = WaveStatus.RUNNING
        self.waves[wave_id].started_at = datetime.now(timezone.utc).isoformat()

    def complete_wave(
        self,
        wave_id: str,
        gate_result: str,
        gate_evaluation: dict[str, Any] | None = None,
        artifacts: list[str] | None = None,
        findings: list[dict[str, Any]] | None = None,
        residue: dict[str, Any] | None = None,
        failure_events: list[dict[str, Any]] | None = None,
    ) -> None:
        """Mark a wave as completed (PASSED, FAILED, or TIMED_OUT)."""
        wave = self.waves[wave_id]
        now = datetime.now(timezone.utc).isoformat()
        wave.completed_at = now
        wave.gate_result = gate_result

        if gate_result == GateResult.PASS:
            wave.status = WaveStatus.COMPLETED
        elif gate_result == GateResult.TIMEOUT:
            wave.status = WaveStatus.TIMED_OUT
        else:
            wave.status = WaveStatus.FAILED

        if gate_evaluation:
            wave.gate_evaluation = gate_evaluation
        if artifacts:
            wave.artifact_ids = artifacts
        if findings:
            wave.findings = findings
        if residue:
            wave.residue = residue
        if failure_events:
            wave.failure_events = failure_events
            self.failure_events.extend(failure_events)

    def skip_wave(self, wave_id: str, reason: str = "") -> None:
        """Mark a wave as SKIPPED (e.g., clean run path)."""
        wave = self.waves[wave_id]
        wave.status = WaveStatus.SKIPPED
        wave.gate_result = GateResult.PASS
        wave.gate_evaluation = {"skipped": True, "reason": reason}
        wave.completed_at = datetime.now(timezone.utc).isoformat()

    def halt(self, reason: str, fm_id: str | None = None) -> None:
        """Halt the pipeline."""
        self.status = RunStatus.HALTED
        self.completed_at = datetime.now(timezone.utc).isoformat()
        event = {
            "type": "PIPELINE_HALTED",
            "reason": reason,
            "timestamp": self.completed_at,
        }
        if fm_id:
            event["fm_id"] = fm_id
        self.failure_events.append(event)
        self.structured_events.append(event)

    def pause(self, wave_id: str, reason: str, escalation_id: str = "") -> None:
        """Pause the pipeline for human intervention."""
        self.status = RunStatus.PAUSED
        event = {
            "type": "PIPELINE_PAUSED",
            "wave": wave_id,
            "reason": reason,
            "escalation_id": escalation_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.human_escalations.append(event)
        self.structured_events.append(event)

    def complete_run(self) -> None:
        """Mark the entire run as completed successfully."""
        self.status = RunStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc).isoformat()

    def add_failure_event(self, event: dict[str, Any]) -> None:
        """Record a failure event."""
        if "timestamp" not in event:
            event["timestamp"] = datetime.now(timezone.utc).isoformat()
        self.failure_events.append(event)
        self.structured_events.append(event)

    def add_structured_event(self, event: dict[str, Any]) -> None:
        """Record a structured event."""
        if "timestamp" not in event:
            event["timestamp"] = datetime.now(timezone.utc).isoformat()
        self.structured_events.append(event)

    # --- Serialization ---

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_version": self.manifest_version,
            "run_id": self.run_id,
            "spec_version": self.spec_version,
            "mode": self.mode,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "status": self.status,
            "run_config": self.run_config_summary,
            "registry_hash": self.registry_hash,
            "pipeline_clean_run": self.pipeline_clean_run,
            "waves": {wid: w.to_dict() for wid, w in self.waves.items()},
            "loop_counters": self.loop_counters.to_dict(),
            "failure_events": self.failure_events,
            "human_escalations": self.human_escalations,
            "structured_events": self.structured_events,
            "pipeline_metrics": self.pipeline_metrics,
            "cumulative_residue": self.cumulative_residue,
            "trigger_events": self.trigger_events,
            "operator_overrides": self.operator_overrides,
            "micro_escalation": self.micro_escalation,
        }

    def compute_hash(self) -> str:
        """Compute SHA-256 of the manifest for checkpoint integrity."""
        canonical = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RunManifest:
        waves = {}
        for wid, wdata in data.get("waves", {}).items():
            waves[wid] = WaveRecord.from_dict(wdata)

        m = cls(
            manifest_version=data.get("manifest_version", __spec_version__),
            run_id=data.get("run_id", ""),
            spec_version=data.get("spec_version", __spec_version__),
            mode=data.get("mode", "STANDARD"),
            created_at=data.get("created_at", ""),
            completed_at=data.get("completed_at"),
            status=data.get("status", RunStatus.RUNNING),
            run_config_summary=data.get("run_config", {}),
            registry_hash=data.get("registry_hash", ""),
            pipeline_clean_run=data.get("pipeline_clean_run"),
            waves=waves,
            loop_counters=LoopCounters.from_dict(data.get("loop_counters", {})),
            failure_events=data.get("failure_events", []),
            human_escalations=data.get("human_escalations", []),
            structured_events=data.get("structured_events", []),
            pipeline_metrics=data.get("pipeline_metrics", {}),
            cumulative_residue=data.get("cumulative_residue", {}),
            trigger_events=data.get("trigger_events", []),
            operator_overrides=data.get("operator_overrides", []),
            micro_escalation=data.get("micro_escalation", {}),
        )
        return m

    # --- Persistence ---

    def save(self, run_dir: Path) -> Path:
        """Save manifest to run directory as manifest.json."""
        run_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = run_dir / "manifest.json"
        # Atomic write: write to temp, then rename
        tmp_path = manifest_path.with_suffix(".tmp")
        with open(tmp_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        os.replace(tmp_path, manifest_path)
        return manifest_path

    def save_checkpoint(self, run_dir: Path, wave_id: str) -> Path:
        """Save a checkpoint after a wave completes."""
        run_dir.mkdir(parents=True, exist_ok=True)
        cp_path = run_dir / f"checkpoint_{wave_id.replace('.', '_')}.json"
        checkpoint = {
            "wave_id": wave_id,
            "manifest_hash": self.compute_hash(),
            "wave_status": self.waves[wave_id].to_dict() if wave_id in self.waves else None,
            "run_status": self.status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        with open(cp_path, "w") as f:
            json.dump(checkpoint, f, indent=2)
        # Also save full manifest
        self.save(run_dir)
        return cp_path

    @classmethod
    def load(cls, run_dir: Path) -> RunManifest:
        """Load manifest from run directory."""
        manifest_path = run_dir / "manifest.json"
        with open(manifest_path) as f:
            return cls.from_dict(json.load(f))
