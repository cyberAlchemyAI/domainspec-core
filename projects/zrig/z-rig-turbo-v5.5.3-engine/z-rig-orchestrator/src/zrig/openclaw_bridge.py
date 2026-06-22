#!/usr/bin/env python3
"""
HRR-005 Builder 3 — openclaw_bridge.py

File-based bridge protocol between Z-Rig orchestrator and Analog 6 (OpenClaw runtime).

When the orchestrator runs inside OpenClaw (embedded mode via z-rig skill):

1. Orchestrator writes `wave_dispatch_request.json` to the wave directory.
2. Analog 6 reads the request, spawns real subagents via sessions_spawn.
3. Analog 6 writes results to `wave_output/<agent_isolation_id>.json`.
4. Orchestrator polls/reads the output files.

This keeps the orchestrator pure Python while delegating actual spawning to the host runtime.

Protocol version: 1.0
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Protocol data structures
# ---------------------------------------------------------------------------

@dataclass
class WaveDispatchRequest:
    """
    Written by orchestrator to request Analog 6 to spawn agents for a wave.
    """
    request_id: str
    run_id: str
    wave: str
    seats: List[Dict[str, Any]]          # List of SeatAssignment dicts
    bundles: List[Dict[str, Any]]        # List of Bundle payloads (aligned)
    timeout_ms: int
    created_at: str
    protocol_version: str = "1.0"


@dataclass
class AgentOutputEnvelope:
    """
    Expected output written by each spawned subagent.
    Must conform to universal artifact envelope (A.4).
    """
    artifact_id: str
    run_id: str
    wave: str
    agent_isolation_id: str
    model_actual: str
    family_actual: str
    payload: Dict[str, Any]
    residue: List[Dict[str, Any]]
    envelope_version: str
    completed_at: str
    token_usage: Optional[Dict] = None


@dataclass
class WaveOutputManifest:
    """
    Written by Analog 6 after all agents in a wave complete (or timeout).
    """
    request_id: str
    run_id: str
    wave: str
    completed_at: str
    successful_count: int
    failed_count: int
    outputs: List[Dict[str, Any]]        # List of AgentOutputEnvelope dicts
    errors: List[Dict[str, Any]] = field(default_factory=list)
    protocol_version: str = "1.0"


# ---------------------------------------------------------------------------
# Bridge paths (relative to wave directory)
# ---------------------------------------------------------------------------

def get_request_path(wave_dir: Path) -> Path:
    return wave_dir / "wave_dispatch_request.json"


def get_output_dir(wave_dir: Path) -> Path:
    return wave_dir / "wave_output"


def get_manifest_path(wave_dir: Path) -> Path:
    return wave_dir / "wave_output_manifest.json"


def get_agent_output_path(wave_dir: Path, agent_isolation_id: str) -> Path:
    return get_output_dir(wave_dir) / f"{agent_isolation_id}.json"


# ---------------------------------------------------------------------------
# Request writer (orchestrator side)
# ---------------------------------------------------------------------------

def write_dispatch_request(
    wave_dir: Path,
    request: WaveDispatchRequest,
) -> Path:
    """
    Orchestrator writes the dispatch request for Analog 6 to consume.
    """
    wave_dir.mkdir(parents=True, exist_ok=True)
    path = get_request_path(wave_dir)
    path.write_text(json.dumps(asdict(request), indent=2), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Output reader (orchestrator side)
# ---------------------------------------------------------------------------

def wait_for_wave_output(
    wave_dir: Path,
    expected_agent_ids: List[str],
    poll_interval_s: float = 3.0,
    max_wait_s: float = 3600.0,
) -> WaveOutputManifest:
    """
    Orchestrator polls for Analog 6 to write wave_output_manifest.json
    or individual agent output files.

    Returns the manifest when ready.
    Raises TimeoutError if max_wait exceeded.
    """
    manifest_path = get_manifest_path(wave_dir)
    start = time.time()

    while time.time() - start < max_wait_s:
        if manifest_path.exists():
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            return WaveOutputManifest(**data)

        # Fallback: check if all individual outputs exist
        output_dir = get_output_dir(wave_dir)
        if output_dir.exists():
            present = [
                p.stem for p in output_dir.glob("*.json")
                if p.stem in expected_agent_ids
            ]
            if len(present) == len(expected_agent_ids):
                # Synthesize manifest from individual files
                outputs = []
                for aid in expected_agent_ids:
                    p = get_agent_output_path(wave_dir, aid)
                    if p.exists():
                        outputs.append(json.loads(p.read_text(encoding="utf-8")))

                return WaveOutputManifest(
                    request_id="unknown",
                    run_id=outputs[0]["run_id"] if outputs else "",
                    wave=outputs[0]["wave"] if outputs else "",
                    completed_at=datetime.now(timezone.utc).isoformat() + "Z",
                    successful_count=len(outputs),
                    failed_count=0,
                    outputs=outputs,
                )

        time.sleep(poll_interval_s)

    raise TimeoutError(f"Timed out waiting for wave output in {wave_dir}")


def read_agent_output(
    wave_dir: Path,
    agent_isolation_id: str,
) -> Optional[Dict[str, Any]]:
    """Read a single agent's output envelope if present."""
    path = get_agent_output_path(wave_dir, agent_isolation_id)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


# ---------------------------------------------------------------------------
# Analog 6 side helpers (invoked by z-rig skill)
# ---------------------------------------------------------------------------

def read_dispatch_request(wave_dir: Path) -> Optional[WaveDispatchRequest]:
    """Analog 6 reads the pending dispatch request."""
    path = get_request_path(wave_dir)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        return WaveDispatchRequest(**data)
    return None


def write_agent_output(
    wave_dir: Path,
    agent_isolation_id: str,
    envelope: Dict[str, Any],
) -> Path:
    """Each spawned subagent (or Analog 6 on its behalf) writes its envelope."""
    output_dir = get_output_dir(wave_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = get_agent_output_path(wave_dir, agent_isolation_id)
    path.write_text(json.dumps(envelope, indent=2), encoding="utf-8")
    return path


def write_wave_manifest(
    wave_dir: Path,
    manifest: WaveOutputManifest,
) -> Path:
    """Analog 6 writes the final manifest after wave completion."""
    path = get_manifest_path(wave_dir)
    path.write_text(json.dumps(asdict(manifest), indent=2), encoding="utf-8")
    return path
