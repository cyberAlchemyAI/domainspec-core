"""Run summary formatting for Z-Rig pipeline results.

Formats completed (or halted/paused) run manifests into human-readable
terminal output.  Uses :mod:`zrig.format_utils` for duration and wave
table formatting.

Typical usage::

    from zrig.run_summary import print_run_summary
    from zrig.manifest import RunManifest

    manifest = RunManifest.load(run_dir)
    print_run_summary(manifest, duration_s=elapsed)
"""

from __future__ import annotations

import sys
from typing import Any, TextIO

from .format_utils import format_duration, format_wave_summary
from .manifest import RunManifest, RunStatus, WaveStatus, GateResult


# ---------------------------------------------------------------------------
# Status emoji / label maps
# ---------------------------------------------------------------------------

_STATUS_ICONS: dict[str, str] = {
    RunStatus.COMPLETED: "✅",
    RunStatus.HALTED: "🛑",
    RunStatus.PAUSED: "⏸️ ",
    RunStatus.RUNNING: "🔄",
}

_STATUS_LABELS: dict[str, str] = {
    RunStatus.COMPLETED: "COMPLETED",
    RunStatus.HALTED: "HALTED",
    RunStatus.PAUSED: "PAUSED",
    RunStatus.RUNNING: "RUNNING",
}

_WAVE_STATUS_ICONS: dict[str, str] = {
    WaveStatus.COMPLETED: "✅",
    WaveStatus.FAILED: "❌",
    WaveStatus.SKIPPED: "⏭️ ",
    WaveStatus.TIMED_OUT: "⏰",
    WaveStatus.RUNNING: "🔄",
    WaveStatus.PENDING: "⬜",
}

_GATE_RESULT_ICONS: dict[str, str] = {
    GateResult.PASS: "✅",
    GateResult.FAIL: "❌",
    GateResult.TIMEOUT: "⏰",
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _compute_wave_timings(manifest: RunManifest) -> dict[str, float]:
    """Compute per-wave duration in seconds from started_at / completed_at.

    Returns a dict mapping wave_id → duration_s.  Waves without timing
    data are omitted.
    """
    from datetime import datetime, timezone

    timings: dict[str, float] = {}
    for wave_id, record in manifest.waves.items():
        if record.started_at and record.completed_at:
            try:
                start = datetime.fromisoformat(record.started_at)
                end = datetime.fromisoformat(record.completed_at)
                timings[wave_id] = max((end - start).total_seconds(), 0.0)
            except (ValueError, TypeError):
                continue
    return timings


def _build_wave_results(manifest: RunManifest) -> list[dict[str, Any]]:
    """Build the list-of-dicts expected by :func:`format_wave_summary`.

    Each dict has keys: ``wave_id``, ``status``, ``duration_s``,
    ``gate_result``.
    """
    timings = _compute_wave_timings(manifest)
    results: list[dict[str, Any]] = []
    for wave_id, record in manifest.waves.items():
        results.append({
            "wave_id": wave_id,
            "status": record.status,
            "duration_s": timings.get(wave_id, 0.0),
            "gate_result": record.gate_result or "—",
        })
    return results


def _count_waves_by_status(manifest: RunManifest) -> dict[str, int]:
    """Count waves by their status."""
    counts: dict[str, int] = {}
    for record in manifest.waves.values():
        counts[record.status] = counts.get(record.status, 0) + 1
    return counts


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def format_run_summary(manifest: RunManifest, duration_s: float) -> str:
    """Format a completed run manifest into a multi-line terminal summary.

    The summary includes:

    * Header with run ID and overall status.
    * Mode and total wall-clock duration.
    * Wave status table (via :func:`format_wave_summary`).
    * Gate results per wave.
    * Failure log (if any failure events exist).
    * Final verdict line.

    Args:
        manifest: The run manifest to summarise.
        duration_s: Total wall-clock duration of the run in seconds.

    Returns:
        A multi-line string ready for terminal display.
    """
    lines: list[str] = []
    separator = "=" * 64

    # --- Header ---
    icon = _STATUS_ICONS.get(manifest.status, "❓")
    label = _STATUS_LABELS.get(manifest.status, manifest.status)
    lines.append("")
    lines.append(separator)
    lines.append(f"  {icon} Z-Rig Pipeline {label} — {manifest.run_id}")
    lines.append(separator)

    # --- Run metadata ---
    lines.append(f"  Mode:     {manifest.mode}")
    lines.append(f"  Duration: {format_duration(duration_s)}")
    lines.append(f"  Spec:     v{manifest.spec_version}")

    # Wave counts
    counts = _count_waves_by_status(manifest)
    count_parts: list[str] = []
    for status in (WaveStatus.COMPLETED, WaveStatus.FAILED, WaveStatus.SKIPPED,
                   WaveStatus.TIMED_OUT, WaveStatus.PENDING, WaveStatus.RUNNING):
        n = counts.get(status, 0)
        if n > 0:
            count_parts.append(f"{n} {status.lower()}")
    lines.append(f"  Waves:    {', '.join(count_parts) if count_parts else 'none'}")
    lines.append("")

    # --- Wave status table ---
    wave_results = _build_wave_results(manifest)
    if wave_results:
        lines.append("  Wave Status Table")
        lines.append("  " + "-" * 50)
        table = format_wave_summary(wave_results)
        for table_line in table.split("\n"):
            lines.append(f"  {table_line}")
        lines.append("")

    # --- Gate results ---
    gate_entries: list[str] = []
    for wave_id, record in manifest.waves.items():
        if record.gate_result and record.gate_result != "—":
            gate_icon = _GATE_RESULT_ICONS.get(record.gate_result, "❓")
            gate_entries.append(f"    {gate_icon} {wave_id}: {record.gate_result}")
    if gate_entries:
        lines.append("  Gate Results")
        lines.append("  " + "-" * 50)
        lines.extend(gate_entries)
        lines.append("")

    # --- Failure log ---
    if manifest.failure_events:
        lines.append("  Failure Log")
        lines.append("  " + "-" * 50)
        for i, event in enumerate(manifest.failure_events, 1):
            fm_id = event.get("fm_id", event.get("type", "UNKNOWN"))
            reason = event.get("reason", event.get("error", "—"))
            wave = event.get("wave", "—")
            lines.append(f"    [{i}] {fm_id} @ {wave}: {reason}")
        lines.append("")

    # --- Halt reason ---
    if manifest.status == RunStatus.HALTED:
        halt_reasons = [
            e.get("reason", "")
            for e in manifest.failure_events
            if e.get("type") == "PIPELINE_HALTED"
        ]
        if halt_reasons:
            lines.append(f"  Halt Reason: {halt_reasons[-1]}")
            lines.append("")

    # --- Human escalations ---
    if manifest.human_escalations:
        lines.append("  Human Escalations")
        lines.append("  " + "-" * 50)
        for esc in manifest.human_escalations:
            wave = esc.get("wave", "—")
            reason = esc.get("reason", "—")
            lines.append(f"    {wave}: {reason}")
        lines.append("")

    # --- Final verdict ---
    lines.append(separator)
    if manifest.status == RunStatus.COMPLETED:
        lines.append(f"  ✅ VERDICT: Pipeline completed successfully")
    elif manifest.status == RunStatus.HALTED:
        lines.append(f"  🛑 VERDICT: Pipeline halted — manual intervention required")
    elif manifest.status == RunStatus.PAUSED:
        lines.append(f"  ⏸️  VERDICT: Pipeline paused — awaiting human escalation")
    else:
        lines.append(f"  ❓ VERDICT: Pipeline status: {manifest.status}")
    lines.append(separator)
    lines.append("")

    return "\n".join(lines)


def print_run_summary(
    manifest: RunManifest,
    duration_s: float,
    file: TextIO | None = None,
) -> None:
    """Print a formatted run summary to stdout (or the given file handle).

    This is a convenience wrapper around :func:`format_run_summary` that
    writes the result directly.

    Args:
        manifest: The run manifest to summarise.
        duration_s: Total wall-clock duration in seconds.
        file: Output stream.  Defaults to ``sys.stdout``.
    """
    output = file if file is not None else sys.stdout
    summary = format_run_summary(manifest, duration_s)
    print(summary, file=output)
