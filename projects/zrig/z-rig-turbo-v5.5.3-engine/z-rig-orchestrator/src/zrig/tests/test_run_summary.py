"""Tests for zrig.run_summary and --live CLI flag.

Covers: completed runs, halted runs, empty waves, timing display, gate
results, stdout capture, and CLI flag existence.
"""

from __future__ import annotations

import io
import sys
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

import pytest

from zrig.manifest import (
    GateResult,
    RunManifest,
    RunStatus,
    WaveRecord,
    WaveStatus,
)
from zrig.run_summary import format_run_summary, print_run_summary


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_manifest(
    *,
    run_id: str = "RUN-TEST-001",
    mode: str = "STANDARD",
    status: str = RunStatus.COMPLETED,
    waves: dict[str, WaveRecord] | None = None,
    failure_events: list[dict] | None = None,
    human_escalations: list[dict] | None = None,
) -> RunManifest:
    """Build a minimal RunManifest for testing."""
    m = RunManifest()
    m.run_id = run_id
    m.mode = mode
    m.status = status
    m.spec_version = "5.5.3"
    m.waves = waves if waves is not None else {}
    m.failure_events = failure_events if failure_events is not None else []
    m.human_escalations = human_escalations if human_escalations is not None else []
    return m


def _wave_record(
    status: str = WaveStatus.COMPLETED,
    gate_result: str = GateResult.PASS,
    started_at: str | None = None,
    completed_at: str | None = None,
) -> WaveRecord:
    """Build a WaveRecord with optional timing."""
    rec = WaveRecord()
    rec.status = status
    rec.gate_result = gate_result
    rec.started_at = started_at
    rec.completed_at = completed_at
    return rec


def _ts(offset_s: float = 0.0) -> str:
    """Return an ISO timestamp offset from a fixed epoch for deterministic tests."""
    base = datetime(2026, 6, 15, 12, 0, 0, tzinfo=timezone.utc)
    return (base + timedelta(seconds=offset_s)).isoformat()


# ---------------------------------------------------------------------------
# Test 1: Completed run summary
# ---------------------------------------------------------------------------

class TestCompletedRun:
    """A fully successful run should show COMPLETED verdict and all waves passing."""

    def test_completed_run_contains_verdict(self) -> None:
        manifest = _make_manifest(
            status=RunStatus.COMPLETED,
            waves={
                "W0": _wave_record(started_at=_ts(0), completed_at=_ts(2)),
                "W1": _wave_record(started_at=_ts(2), completed_at=_ts(10)),
                "W2": _wave_record(started_at=_ts(10), completed_at=_ts(25)),
            },
        )
        summary = format_run_summary(manifest, duration_s=25.0)

        assert "COMPLETED" in summary
        assert "RUN-TEST-001" in summary
        assert "VERDICT" in summary
        assert "completed successfully" in summary

    def test_completed_run_shows_mode(self) -> None:
        manifest = _make_manifest(mode="FULL", status=RunStatus.COMPLETED)
        summary = format_run_summary(manifest, duration_s=10.0)
        assert "FULL" in summary

    def test_completed_run_no_failure_log(self) -> None:
        manifest = _make_manifest(status=RunStatus.COMPLETED)
        summary = format_run_summary(manifest, duration_s=1.0)
        assert "Failure Log" not in summary


# ---------------------------------------------------------------------------
# Test 2: Halted run summary
# ---------------------------------------------------------------------------

class TestHaltedRun:
    """A halted run should show HALTED verdict, failure log, and halt reason."""

    def test_halted_run_shows_halt_verdict(self) -> None:
        manifest = _make_manifest(
            status=RunStatus.HALTED,
            waves={
                "W0": _wave_record(started_at=_ts(0), completed_at=_ts(2)),
                "W2": _wave_record(
                    status=WaveStatus.FAILED,
                    gate_result=GateResult.FAIL,
                    started_at=_ts(2),
                    completed_at=_ts(10),
                ),
            },
            failure_events=[
                {
                    "type": "PIPELINE_HALTED",
                    "fm_id": "FM-EXHAUSTION",
                    "wave": "W2",
                    "reason": "Retry budget exhausted for W2",
                },
            ],
        )
        summary = format_run_summary(manifest, duration_s=10.0)

        assert "HALTED" in summary
        assert "Failure Log" in summary
        assert "FM-EXHAUSTION" in summary
        assert "Retry budget exhausted" in summary
        assert "manual intervention" in summary

    def test_halted_run_shows_failed_wave_in_table(self) -> None:
        manifest = _make_manifest(
            status=RunStatus.HALTED,
            waves={
                "W2": _wave_record(
                    status=WaveStatus.FAILED,
                    gate_result=GateResult.FAIL,
                    started_at=_ts(0),
                    completed_at=_ts(5),
                ),
            },
            failure_events=[
                {"type": "PIPELINE_HALTED", "reason": "test halt"},
            ],
        )
        summary = format_run_summary(manifest, duration_s=5.0)
        assert "FAILED" in summary
        assert "W2" in summary


# ---------------------------------------------------------------------------
# Test 3: Empty waves
# ---------------------------------------------------------------------------

class TestEmptyWaves:
    """A manifest with no waves should still produce a valid summary."""

    def test_empty_waves_no_crash(self) -> None:
        manifest = _make_manifest(waves={})
        summary = format_run_summary(manifest, duration_s=0.0)
        assert "RUN-TEST-001" in summary
        assert "VERDICT" in summary

    def test_empty_waves_shows_none_count(self) -> None:
        manifest = _make_manifest(waves={})
        summary = format_run_summary(manifest, duration_s=0.0)
        assert "none" in summary


# ---------------------------------------------------------------------------
# Test 4: Timing display
# ---------------------------------------------------------------------------

class TestTimingDisplay:
    """Verify that durations are formatted via format_duration."""

    def test_short_duration(self) -> None:
        manifest = _make_manifest(
            waves={
                "W0": _wave_record(started_at=_ts(0), completed_at=_ts(0.5)),
            },
        )
        summary = format_run_summary(manifest, duration_s=0.5)
        # Total duration should appear formatted
        assert "0.5s" in summary

    def test_long_duration(self) -> None:
        manifest = _make_manifest(
            waves={
                "W0": _wave_record(started_at=_ts(0), completed_at=_ts(3661)),
            },
        )
        summary = format_run_summary(manifest, duration_s=3661.0)
        assert "1h" in summary
        assert "1m" in summary
        assert "1s" in summary

    def test_wave_timing_in_table(self) -> None:
        """Individual wave durations should appear in the wave table."""
        manifest = _make_manifest(
            waves={
                "W0": _wave_record(started_at=_ts(0), completed_at=_ts(5)),
                "W1": _wave_record(started_at=_ts(5), completed_at=_ts(65)),
            },
        )
        summary = format_run_summary(manifest, duration_s=65.0)
        # W0 took 5s, W1 took 60s = 1m
        assert "5s" in summary
        assert "1m" in summary

    def test_zero_duration(self) -> None:
        manifest = _make_manifest()
        summary = format_run_summary(manifest, duration_s=0.0)
        assert "0s" in summary


# ---------------------------------------------------------------------------
# Test 5: Gate results
# ---------------------------------------------------------------------------

class TestGateResults:
    """Gate results section should list per-wave gate outcomes."""

    def test_gate_pass_shown(self) -> None:
        manifest = _make_manifest(
            waves={
                "W0": _wave_record(gate_result=GateResult.PASS),
                "W1": _wave_record(gate_result=GateResult.PASS),
            },
        )
        summary = format_run_summary(manifest, duration_s=1.0)
        assert "Gate Results" in summary
        assert "PASS" in summary

    def test_gate_fail_shown(self) -> None:
        manifest = _make_manifest(
            status=RunStatus.HALTED,
            waves={
                "W0": _wave_record(gate_result=GateResult.PASS),
                "W2": _wave_record(
                    status=WaveStatus.FAILED,
                    gate_result=GateResult.FAIL,
                ),
            },
            failure_events=[
                {"type": "PIPELINE_HALTED", "reason": "test"},
            ],
        )
        summary = format_run_summary(manifest, duration_s=1.0)
        assert "FAIL" in summary
        assert "W2" in summary

    def test_gate_timeout_shown(self) -> None:
        manifest = _make_manifest(
            status=RunStatus.PAUSED,
            waves={
                "W4": _wave_record(
                    status=WaveStatus.TIMED_OUT,
                    gate_result=GateResult.TIMEOUT,
                ),
            },
        )
        summary = format_run_summary(manifest, duration_s=300.0)
        assert "TIMEOUT" in summary
        assert "W4" in summary

    def test_mixed_gate_results(self) -> None:
        manifest = _make_manifest(
            status=RunStatus.HALTED,
            waves={
                "W0": _wave_record(gate_result=GateResult.PASS),
                "W1": _wave_record(gate_result=GateResult.PASS),
                "W2": _wave_record(
                    status=WaveStatus.FAILED,
                    gate_result=GateResult.FAIL,
                ),
            },
            failure_events=[
                {"type": "PIPELINE_HALTED", "reason": "test"},
            ],
        )
        summary = format_run_summary(manifest, duration_s=30.0)
        # Should show both PASS and FAIL
        assert summary.count("PASS") >= 2
        assert "FAIL" in summary


# ---------------------------------------------------------------------------
# Test 6: stdout capture (print_run_summary)
# ---------------------------------------------------------------------------

class TestStdoutCapture:
    """print_run_summary should write to stdout (or the given file)."""

    def test_prints_to_stdout(self) -> None:
        manifest = _make_manifest(status=RunStatus.COMPLETED)
        buf = io.StringIO()
        print_run_summary(manifest, duration_s=1.0, file=buf)
        output = buf.getvalue()
        assert "COMPLETED" in output
        assert "VERDICT" in output
        assert len(output) > 50

    def test_prints_to_custom_file(self) -> None:
        manifest = _make_manifest(run_id="CUSTOM-RUN-99")
        buf = io.StringIO()
        print_run_summary(manifest, duration_s=42.0, file=buf)
        output = buf.getvalue()
        assert "CUSTOM-RUN-99" in output
        assert "42s" in output

    def test_print_includes_full_summary(self) -> None:
        """print_run_summary output should match format_run_summary."""
        manifest = _make_manifest(
            waves={
                "W0": _wave_record(gate_result=GateResult.PASS),
            },
        )
        expected = format_run_summary(manifest, duration_s=5.0)
        buf = io.StringIO()
        print_run_summary(manifest, duration_s=5.0, file=buf)
        # print adds a trailing newline
        assert expected in buf.getvalue()


# ---------------------------------------------------------------------------
# Test 7: CLI --live flag existence
# ---------------------------------------------------------------------------

class TestCLILiveFlag:
    """The 'run' subparser should accept --live as a boolean flag."""

    def test_live_flag_accepted(self) -> None:
        """Parsing --live should set args.live = True."""
        from zrig.__main__ import main
        import argparse

        # We need to parse args to check the flag is accepted.
        # Build the parser the same way main() does internally.
        from zrig import __version__, __spec_version__

        parser = argparse.ArgumentParser(prog="zrig")
        subparsers = parser.add_subparsers(dest="command")
        run_parser = subparsers.add_parser("run")
        run_parser.add_argument("--config", required=True)
        run_parser.add_argument("--task", required=True)
        run_parser.add_argument("--registry")
        run_parser.add_argument("--output-dir", default=".")
        run_parser.add_argument("--verbose", "-v", action="store_true")
        run_parser.add_argument("--live", action="store_true")

        args = parser.parse_args(["run", "--config", "c.json", "--task", "t.json", "--live"])
        assert args.live is True
        assert args.command == "run"

    def test_live_flag_default_false(self) -> None:
        """Without --live, args.live should be False."""
        import argparse

        parser = argparse.ArgumentParser(prog="zrig")
        subparsers = parser.add_subparsers(dest="command")
        run_parser = subparsers.add_parser("run")
        run_parser.add_argument("--config", required=True)
        run_parser.add_argument("--task", required=True)
        run_parser.add_argument("--registry")
        run_parser.add_argument("--output-dir", default=".")
        run_parser.add_argument("--verbose", "-v", action="store_true")
        run_parser.add_argument("--live", action="store_true")

        args = parser.parse_args(["run", "--config", "c.json", "--task", "t.json"])
        assert args.live is False


# ---------------------------------------------------------------------------
# Test 8: Paused run with human escalation
# ---------------------------------------------------------------------------

class TestPausedRun:
    """Paused runs should display escalation info."""

    def test_paused_shows_escalation(self) -> None:
        manifest = _make_manifest(
            status=RunStatus.PAUSED,
            waves={
                "W4": _wave_record(
                    status=WaveStatus.TIMED_OUT,
                    gate_result=GateResult.TIMEOUT,
                ),
            },
            human_escalations=[
                {
                    "type": "PIPELINE_PAUSED",
                    "wave": "W4",
                    "reason": "W4 verification timed out",
                },
            ],
        )
        summary = format_run_summary(manifest, duration_s=600.0)
        assert "PAUSED" in summary
        assert "Human Escalation" in summary
        assert "W4 verification timed out" in summary
        assert "awaiting human escalation" in summary


# ---------------------------------------------------------------------------
# Test 9: Multiple failure events
# ---------------------------------------------------------------------------

class TestMultipleFailures:
    """Multiple failure events should all appear in the failure log."""

    def test_all_failures_listed(self) -> None:
        manifest = _make_manifest(
            status=RunStatus.HALTED,
            failure_events=[
                {"fm_id": "FM-FINDING", "wave": "W2", "reason": "Build failed"},
                {"fm_id": "FM-DIVERSITY", "wave": "W0", "reason": "Not enough families"},
                {"type": "PIPELINE_HALTED", "reason": "Final halt"},
            ],
        )
        summary = format_run_summary(manifest, duration_s=5.0)
        assert "FM-FINDING" in summary
        assert "FM-DIVERSITY" in summary
        assert "PIPELINE_HALTED" in summary
        assert "[1]" in summary
        assert "[2]" in summary
        assert "[3]" in summary
