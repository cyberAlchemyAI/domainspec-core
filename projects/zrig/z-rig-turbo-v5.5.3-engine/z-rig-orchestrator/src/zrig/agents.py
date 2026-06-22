#!/usr/bin/env python3
"""
HRR-004 Builder 2 — agents.py
OpenClaw Integration: sessions_spawn wrapper for agent invocation.

Provides:
  - OpenClawAgentRunner: async callable bridging dispatch.py ↔ OpenClaw sessions_spawn
  - Output collection, schema validation, artifact storage wiring
  - Agent isolation: each agent gets its own output namespace

This module is the thin boundary between Z-Rig orchestrator logic and the
OpenClaw execution environment.  The rest of the orchestrator treats agents as
black boxes that receive a bundle and return a structured JSON output.

Spec refs: A.13, 5.2.3, 5.3
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from zrig.bundles import Bundle
from zrig.dispatch import SeatAssignment, ProviderError


# ---------------------------------------------------------------------------
# Agent output schema validation
# ---------------------------------------------------------------------------

REQUIRED_ENVELOPE_FIELDS = [
    "artifact_id",
    "run_id",
    "wave",
    "agent_isolation_id",
    "model_actual",
    "family_actual",
    "payload",
    "residue",
    "envelope_version",
    "completed_at",
]


def validate_agent_output(output: Dict, seat: SeatAssignment) -> List[str]:
    """
    Validate agent output against universal artifact envelope (spec A.4).
    Returns list of validation errors (empty = valid).

    Required fields per MECH-028 RESIDUE_VALID:
      - envelope_version
      - artifact_id
      - run_id, wave, agent_isolation_id
      - model_actual, family_actual
      - payload (non-null)
      - residue (list, may be empty)
      - completed_at (ISO-8601)
    """
    errors: List[str] = []

    for f in REQUIRED_ENVELOPE_FIELDS:
        if f not in output:
            errors.append(f"MISSING_FIELD: {f!r}")
        elif output[f] is None and f in ("payload", "residue"):
            errors.append(f"NULL_FIELD: {f!r}")

    # Residue must be a list (may be empty)
    if "residue" in output and not isinstance(output["residue"], list):
        errors.append(f"RESIDUE_TYPE: expected list, got {type(output['residue']).__name__}")

    # agent_isolation_id must match the assigned one
    if output.get("agent_isolation_id") != seat.agent_isolation_id:
        errors.append(
            f"ISOLATION_MISMATCH: output.agent_isolation_id={output.get('agent_isolation_id')!r} "
            f"!= seat.agent_isolation_id={seat.agent_isolation_id!r}"
        )

    return errors


def wrap_in_envelope(
    payload: Dict,
    seat: SeatAssignment,
    residue: Optional[List] = None,
) -> Dict:
    """
    Wrap agent payload in universal artifact envelope (spec A.4).
    Used for testing + for agents that return raw payloads.
    """
    return {
        "envelope_version": "5.5.2",
        "artifact_id": str(uuid.uuid4()),
        "spec_version": "5.5.2",
        "run_id": seat.wave,           # Caller should override with actual run_id
        "wave": seat.wave,
        "agent_isolation_id": seat.agent_isolation_id,
        "model_requested": seat.model_requested,
        "model_actual": seat.model_actual,
        "family_actual": seat.family_actual,
        "role": seat.role,
        "completed_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + "Z",
        "payload": payload,
        "residue": residue or [],
        "token_usage": None,
    }


# ---------------------------------------------------------------------------
# OpenClaw sessions_spawn integration
# ---------------------------------------------------------------------------

@dataclass
class SpawnConfig:
    """
    Configuration for spawning an agent via OpenClaw sessions_spawn.

    OpenClaw's sessions_spawn accepts:
      - model: model identifier string
      - task: the task description text (our bundle as JSON string)
      - timeout_ms: maximum execution time
      - workspace: optional workspace directory path
    """
    model: str
    task: str                           # Bundle.to_task_description()
    timeout_ms: int = 3_600_000
    workspace: Optional[str] = None
    env: Dict[str, str] = field(default_factory=dict)
    output_dir: Optional[str] = None    # where the agent should write output.json


class OpenClawAgentRunner:
    """
    Async callable that spawns an OpenClaw subagent for one seat.
    Implements the agent_runner protocol expected by AgentDispatcher.

    Usage:
        runner = OpenClawAgentRunner(run_dir=Path("runs/HRR-001"))
        dispatcher.agent_runner = runner

    The runner:
      1. Serializes the bundle as a structured task description.
      2. Spawns an OpenClaw subagent with sessions_spawn via CLI.
      3. Waits for completion (poll loop or await).
      4. Reads output.json from the agent's namespace.
      5. Validates the output envelope.
      6. Returns the validated dict.

    Agent contract:
      - Receives: JSON task description containing bundle payload
      - Must write: output.json to its output directory (path injected in task)
      - output.json MUST conform to universal artifact envelope (A.4)
    """

    def __init__(
        self,
        run_dir: Path,
        openclaw_cli: str = "openclaw",
        poll_interval_s: float = 2.0,
    ):
        self.run_dir = run_dir
        self.openclaw_cli = openclaw_cli
        self.poll_interval_s = poll_interval_s

    async def __call__(
        self,
        seat: SeatAssignment,
        bundle: Bundle,
        model: str,
    ) -> Dict:
        """
        Spawn agent for the given seat, wait for completion, return output.

        Raises:
            ProviderError on provider-level errors (bad JSON, 5xx, etc.)
            asyncio.TimeoutError on timeout (handled by caller)
        """
        output_dir = (
            self.run_dir
            / "agents"
            / seat.agent_isolation_id
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "output.json"

        # Build task description with output directory injected
        task_payload = {
            "bundle_id": bundle.bundle_id,
            "run_id": bundle.run_id,
            "wave": bundle.wave,
            "agent_isolation_id": seat.agent_isolation_id,
            "model": model,
            "role": seat.role,
            "output_path": str(output_path),
            "payload": bundle.payload,
        }
        task_description = json.dumps(task_payload, indent=2)

        spawn_config = SpawnConfig(
            model=model,
            task=task_description,
            timeout_ms=int(self.poll_interval_s * 1000 * 1000),
            output_dir=str(output_dir),
        )

        # Spawn via OpenClaw CLI
        try:
            session_id = await self._spawn_session(spawn_config)
        except Exception as e:
            raise ProviderError(f"Session spawn failed for {seat.seat_id}: {e}") from e

        # Poll for completion
        output = await self._await_completion(session_id, output_path, seat)
        return output

    async def _spawn_session(self, config: SpawnConfig) -> str:
        """
        Invoke OpenClaw sessions_spawn CLI.
        Returns a session_id that can be polled.

        In production: this calls `openclaw sessions spawn --model <model> --task-file <path>`
        and parses the returned session ID.
        """
        # Write task to temp file
        task_file = self.run_dir / f"task_{uuid.uuid4().hex}.json"
        task_file.write_text(config.task, encoding="utf-8")

        cmd = [
            self.openclaw_cli,
            "sessions", "spawn",
            "--model", config.model,
            "--task-file", str(task_file),
            "--output-json",
        ]
        if config.output_dir:
            cmd += ["--output-dir", config.output_dir]

        # Non-blocking subprocess spawn
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise ProviderError(
                f"openclaw sessions spawn failed (rc={proc.returncode}): "
                f"{stderr.decode(errors='replace')}"
            )

        response = json.loads(stdout.decode())
        session_id = response.get("session_id") or response.get("id")
        if not session_id:
            raise ProviderError(f"No session_id in spawn response: {stdout.decode()!r}")

        # Clean up task file
        task_file.unlink(missing_ok=True)
        return session_id

    async def _await_completion(
        self,
        session_id: str,
        output_path: Path,
        seat: SeatAssignment,
    ) -> Dict:
        """
        Poll OpenClaw session until complete, then read output.json.
        Raises ProviderError on agent failure.
        """
        while True:
            await asyncio.sleep(self.poll_interval_s)

            # Check if output file has appeared (agent writes it on completion)
            if output_path.exists():
                break

            # Also poll session status for early failure detection
            status = await self._poll_session_status(session_id)
            if status == "FAILED":
                raise ProviderError(f"Session {session_id} reported FAILED status.")
            if status == "COMPLETED":
                break

        if not output_path.exists():
            raise ProviderError(
                f"Session {session_id} completed but no output.json at {output_path}"
            )

        raw = output_path.read_text(encoding="utf-8")
        try:
            output = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ProviderError(f"Agent output is not valid JSON: {e}") from e

        # Validate envelope
        errors = validate_agent_output(output, seat)
        if errors:
            raise ProviderError(
                f"Agent output failed envelope validation for seat {seat.seat_id}: {errors}"
            )

        return output

    async def _poll_session_status(self, session_id: str) -> str:
        """Poll OpenClaw for session status: RUNNING | COMPLETED | FAILED."""
        try:
            proc = await asyncio.create_subprocess_exec(
                self.openclaw_cli,
                "sessions", "status", session_id,
                "--output-json",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            if proc.returncode != 0:
                return "UNKNOWN"
            data = json.loads(stdout.decode())
            return data.get("status", "UNKNOWN")
        except Exception:
            return "UNKNOWN"


# ---------------------------------------------------------------------------
# Dry-run / stub runner for testing and local development
# ---------------------------------------------------------------------------

class StubAgentRunner:
    """
    Stub agent runner that returns synthetic outputs for testing.
    Does NOT call OpenClaw — suitable for unit tests and CI.

    Usage:
        runner = StubAgentRunner(synthetic_payloads={"W2": {"build_status": "SUCCESS"}})
        dispatcher.agent_runner = runner
    """

    def __init__(
        self,
        synthetic_payloads: Optional[Dict[str, Any]] = None,
        always_fail: bool = False,
        fail_on_models: Optional[List[str]] = None,
        latency_s: float = 0.0,
    ):
        self.synthetic_payloads = synthetic_payloads or {}
        self.always_fail = always_fail
        self.fail_on_models = fail_on_models or []
        self.latency_s = latency_s

    async def __call__(
        self,
        seat: SeatAssignment,
        bundle: Bundle,
        model: str,
    ) -> Dict:
        if self.latency_s > 0:
            await asyncio.sleep(self.latency_s)

        if self.always_fail or model in self.fail_on_models:
            raise ProviderError(f"StubAgentRunner: simulated failure for model {model!r}")

        payload = self.synthetic_payloads.get(seat.wave, {
            "build_status": "SUCCESS",
            "stub": True,
        })

        return wrap_in_envelope(
            payload=payload,
            seat=seat,
            residue=[
                {
                    "residue_class": "stub",
                    "items": [],
                    "no_residue_reason": "Stub agent — no real decisions made",
                }
            ],
        )


# ---------------------------------------------------------------------------
# Output collector: reads from wave directory
# ---------------------------------------------------------------------------

class WaveOutputCollector:
    """
    Collects, validates, and stores agent outputs after a wave completes.
    Writes each output to HRR-NNN/waveN/<artifact_id>.json
    """

    def __init__(self, run_dir: Path):
        self.run_dir = run_dir

    def collect(
        self,
        wave: str,
        agent_isolation_ids: List[str],
        validate: bool = True,
    ) -> List[Dict]:
        """
        Collect outputs from all agents in a wave.
        Returns list of output dicts (envelope format).
        """
        wave_dir = self.run_dir / f"wave{wave.lstrip('W')}"
        wave_dir.mkdir(parents=True, exist_ok=True)

        outputs: List[Dict] = []
        for isolation_id in agent_isolation_ids:
            output_path = self.run_dir / "agents" / isolation_id / "output.json"
            if not output_path.exists():
                raise MissingAgentOutputError(
                    f"No output.json for agent {isolation_id} in wave {wave}"
                )
            output = json.loads(output_path.read_text(encoding="utf-8"))

            # Store in wave directory
            artifact_id = output.get("artifact_id") or str(uuid.uuid4())
            dest = wave_dir / f"{artifact_id}.json"
            dest.write_text(json.dumps(output, indent=2), encoding="utf-8")

            outputs.append(output)

        return outputs

    def store_output(self, wave: str, output: Dict) -> Path:
        """Store a single agent output in the wave directory."""
        wave_dir = self.run_dir / f"wave{wave.lstrip('W')}"
        wave_dir.mkdir(parents=True, exist_ok=True)
        artifact_id = output.get("artifact_id") or str(uuid.uuid4())
        dest = wave_dir / f"{artifact_id}.json"
        dest.write_text(json.dumps(output, indent=2), encoding="utf-8")
        return dest


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class MissingAgentOutputError(RuntimeError):
    """Raised when an agent has not written output.json."""


class EnvelopeValidationError(RuntimeError):
    """Raised when agent output fails universal artifact envelope validation."""
