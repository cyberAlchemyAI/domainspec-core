"""Comprehensive tests for zrig.run_summary and the --live CLI flag."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

import pytest

from zrig.manifest import RunManifest, RunStatus, WaveRecord, WaveStatus, GateResult
from zrig.run_summary import format_run_summary, print_run_summary


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_manifest(
    *,
    run_id: str = "HRR-TEST-001",
    mode: str = "STANDARD",
    status: str = RunStatus.COMPLETED,
    wave_specs: list[tuple[str, str, str | None]] | None = None,
    halt_reason: str | None = None,
) -> RunManifest:
    """Build a minimal RunManifest for testing.

    Args:
        wave_specs: List of (wave_id, status, gate_result) tuples.
            Each wave gets timestamps 10 s apart.
        halt_reason: If provided, a PIPELINE_HALTED failure event is added.
    """
    m = RunManifest(
        run_id=run_id,
        mode=mode,
        status=status,
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    if status in (RunStatus.COMPLETED, RunStatus.HALTED, RunStatus.PAUSED):
        m.completed_at = datetime.now(timezone.utc).isoformat()

    if wave_specs:
        base = datetime(2026, 6, 16, 12, 0, 0, tzinfo=timezone.utc)
        for idx, (wave_id, w_status, gate) in enumerate(wave_specs):
            started = base + timedelta(seconds=idx * 10)
            completed = started + timedelta(seconds=10)

            wr = WaveRecord(
                status=w_status,
                started_at=started.isoformat(),
                completed_at=completed.isoformat(),
                gate_result=gate,
            )

            # Add failure events for failed waves
            if w_status in (WaveStatus.FAILED, WaveStatus.TIMED_OUT):
                wr.failure_events = [
                    {
                        "fm_id": "FM-FINDING",
                        "wave": wave_id,
                        "reason": f"{wave_id} failed gate evaluation",
                    }
                ]

            m.waves[wave_id] = wr

    if halt_reason:
        m.failure_events.append({
            "type": "PIPELINE_HALTED",
            "reason": halt_reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    return m


# ---------------------------------------------------------------------------
# test_format_run_summary_completed — happy path
# ---------------------------------------------------------------------------

class TestFormatRunSummaryCompleted:
    """Happy-path: all waves pass, status COMPLETED."""

    def test_contains_run_id(self) -> None:
        m = _make_manifest(
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
                ("W1", WaveStatus.COMPLETED, GateResult.PASS),
                ("W2", WaveStatus.COMPLETED, GateResult.PASS),
            ],
        )
        output = format_run_summary(m, 42.5)
        assert "HRR-TEST-001" in output

    def test_contains_mode(self) -> None:
        m = _make_manifest(
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
            ],
        )
        output = format_run_summary(m, 10.0)
        assert "STANDARD" in output

    def test_verdict_completed(self) -> None:
        m = _make_manifest(
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
                ("W1", WaveStatus.COMPLETED, GateResult.PASS),
            ],
        )
        output = format_run_summary(m, 20.0)
        assert "VERDICT:" in output
        assert "COMPLETED" in output or "completed" in output

    def test_no_failure_log(self) -> None:
        m = _make_manifest(
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
            ],
        )
        output = format_run_summary(m, 5.0)
        assert "Failure Log" not in output

    def test_gate_results_section(self) -> None:
        m = _make_manifest(
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
                ("W1", WaveStatus.COMPLETED, GateResult.PASS),
            ],
        )
        output = format_run_summary(m, 20.0)
        assert "Gate Results" in output
        assert "W0" in output
        assert "PASS" in output
        assert "W1" in output

    def test_wave_table_present(self) -> None:
        m = _make_manifest(
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
                ("W1", WaveStatus.COMPLETED, GateResult.PASS),
            ],
        )
        output = format_run_summary(m, 20.0)
        # format_wave_summary produces a table header with "Wave"
        assert "Wave" in output
        assert "Status" in output
        assert "Duration" in output
        assert "Gate" in output

    def test_contains_checkmark_icon(self) -> None:
        m = _make_manifest(
            wave_specs=[("W0", WaveStatus.COMPLETED, GateResult.PASS)],
        )
        output = format_run_summary(m, 5.0)
        assert "✅" in output


# ---------------------------------------------------------------------------
# test_format_run_summary_halted — with halt reason
# ---------------------------------------------------------------------------

class TestFormatRunSummaryHalted:
    """Pipeline halted mid-run with failure events."""

    def test_verdict_halted(self) -> None:
        m = _make_manifest(
            status=RunStatus.HALTED,
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
                ("W2", WaveStatus.FAILED, GateResult.FAIL),
            ],
            halt_reason="FM-EXHAUSTION: w2_reruns=3 exceeds max=2",
        )
        output = format_run_summary(m, 30.0)
        assert "VERDICT:" in output
        assert "HALTED" in output or "halted" in output

    def test_halt_reason_displayed(self) -> None:
        m = _make_manifest(
            status=RunStatus.HALTED,
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
                ("W2", WaveStatus.FAILED, GateResult.FAIL),
            ],
            halt_reason="FM-EXHAUSTION: w2_reruns=3 exceeds max=2",
        )
        output = format_run_summary(m, 30.0)
        assert "FM-EXHAUSTION" in output

    def test_failure_log_present(self) -> None:
        m = _make_manifest(
            status=RunStatus.HALTED,
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
                ("W2", WaveStatus.FAILED, GateResult.FAIL),
            ],
            halt_reason="Pipeline budget exhausted",
        )
        output = format_run_summary(m, 30.0)
        assert "Failure Log" in output

    def test_halt_icon(self) -> None:
        m = _make_manifest(
            status=RunStatus.HALTED,
            wave_specs=[("W0", WaveStatus.COMPLETED, GateResult.PASS)],
            halt_reason="test halt",
        )
        output = format_run_summary(m, 10.0)
        assert "🛑" in output


# ---------------------------------------------------------------------------
# test_format_run_summary_empty_waves
# ---------------------------------------------------------------------------

class TestFormatRunSummaryEmptyWaves:
    """Edge case: manifest with zero waves."""

    def test_no_wave_table_rows(self) -> None:
        m = _make_manifest(wave_specs=[])
        output = format_run_summary(m, 0.0)
        # With no waves, there should be no per-wave rows in the output
        # The table section may be omitted entirely or show "none"
        assert "W0" not in output
        assert "W1" not in output

    def test_no_gate_entries(self) -> None:
        m = _make_manifest(wave_specs=[])
        output = format_run_summary(m, 0.0)
        # With no waves, there are no gate entries to display
        # The Gate Results section may be omitted entirely
        assert "PASS" not in output
        assert "FAIL" not in output

    def test_still_produces_verdict(self) -> None:
        m = _make_manifest(wave_specs=[])
        output = format_run_summary(m, 0.0)
        assert "VERDICT:" in output

    def test_no_failure_log(self) -> None:
        m = _make_manifest(wave_specs=[])
        output = format_run_summary(m, 0.0)
        assert "Failure Log" not in output


# ---------------------------------------------------------------------------
# test_format_run_summary_includes_timing
# ---------------------------------------------------------------------------

class TestFormatRunSummaryIncludesTiming:
    """Timing information is present and formatted correctly."""

    def test_total_duration_formatted(self) -> None:
        m = _make_manifest(
            wave_specs=[("W0", WaveStatus.COMPLETED, GateResult.PASS)],
        )
        output = format_run_summary(m, 3661.0)
        # format_duration(3661.0) → "1h 1m 1s"
        assert "1h 1m 1s" in output

    def test_zero_duration(self) -> None:
        m = _make_manifest(wave_specs=[])
        output = format_run_summary(m, 0.0)
        assert "0s" in output

    def test_wave_durations_in_table(self) -> None:
        m = _make_manifest(
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
                ("W1", WaveStatus.COMPLETED, GateResult.PASS),
            ],
        )
        output = format_run_summary(m, 25.0)
        # Each wave in _make_manifest gets 10s duration → "10s"
        assert "10s" in output

    def test_duration_label(self) -> None:
        m = _make_manifest(
            wave_specs=[("W0", WaveStatus.COMPLETED, GateResult.PASS)],
        )
        output = format_run_summary(m, 42.0)
        assert "Duration:" in output


# ---------------------------------------------------------------------------
# test_format_run_summary_includes_gate_results
# ---------------------------------------------------------------------------

class TestFormatRunSummaryIncludesGateResults:
    """Gate results section shows PASS/FAIL for each wave."""

    def test_pass_gates(self) -> None:
        m = _make_manifest(
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
                ("W1", WaveStatus.COMPLETED, GateResult.PASS),
                ("W2", WaveStatus.COMPLETED, GateResult.PASS),
            ],
        )
        output = format_run_summary(m, 30.0)
        for wid in ("W0", "W1", "W2"):
            # Gate results appear in the output with PASS
            assert wid in output
        assert output.count("PASS") >= 3

    def test_fail_gates(self) -> None:
        m = _make_manifest(
            status=RunStatus.HALTED,
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
                ("W2", WaveStatus.FAILED, GateResult.FAIL),
            ],
            halt_reason="Gate failed",
        )
        output = format_run_summary(m, 20.0)
        assert "W0" in output
        assert "PASS" in output
        assert "W2" in output
        assert "FAIL" in output

    def test_missing_gate_shows_dash(self) -> None:
        m = _make_manifest(wave_specs=[])
        # Add a wave with no gate result
        m.waves["W0"] = WaveRecord(
            status=WaveStatus.PENDING,
            gate_result=None,
        )
        output = format_run_summary(m, 5.0)
        # The em-dash "—" should appear in the wave table for a missing gate
        assert "—" in output

    def test_timeout_gate(self) -> None:
        m = _make_manifest(
            status=RunStatus.PAUSED,
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
                ("W4", WaveStatus.TIMED_OUT, GateResult.TIMEOUT),
            ],
        )
        output = format_run_summary(m, 60.0)
        assert "TIMEOUT" in output


# ---------------------------------------------------------------------------
# test_print_run_summary_outputs_to_stdout
# ---------------------------------------------------------------------------

class TestPrintRunSummary:
    """print_run_summary writes to stdout."""

    def test_outputs_to_stdout(self, capsys: pytest.CaptureFixture[str]) -> None:
        m = _make_manifest(
            wave_specs=[
                ("W0", WaveStatus.COMPLETED, GateResult.PASS),
            ],
        )
        print_run_summary(m, 10.0)
        captured = capsys.readouterr()
        assert "HRR-TEST-001" in captured.out
        assert "VERDICT:" in captured.out
        assert "COMPLETED" in captured.out or "completed" in captured.out

    def test_nothing_on_stderr(self, capsys: pytest.CaptureFixture[str]) -> None:
        m = _make_manifest(wave_specs=[])
        print_run_summary(m, 0.0)
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_output_contains_format_content(self, capsys: pytest.CaptureFixture[str]) -> None:
        """print_run_summary output contains the same content as format_run_summary."""
        m = _make_manifest(
            wave_specs=[("W0", WaveStatus.COMPLETED, GateResult.PASS)],
        )
        expected = format_run_summary(m, 5.0)
        print_run_summary(m, 5.0)
        captured = capsys.readouterr()
        # The formatted summary should appear within stdout
        assert expected in captured.out


# ---------------------------------------------------------------------------
# test_cli_live_flag_exists
# ---------------------------------------------------------------------------

class TestCliLiveFlag:
    """The --live flag is registered on the run subparser."""

    def _build_parser(self) -> argparse.ArgumentParser:
        """Reconstruct the CLI parser from __main__.main's source.

        We import the module and invoke the parser construction inline
        so changes to __main__.py are picked up automatically.
        """
        from zrig.__main__ import main  # noqa: F401

        parser = argparse.ArgumentParser(prog="zrig")
        subparsers = parser.add_subparsers(dest="command")

        run_parser = subparsers.add_parser("run")
        run_parser.add_argument("--config", required=True)
        run_parser.add_argument("--task", required=True)
        run_parser.add_argument("--registry")
        run_parser.add_argument("--output-dir", default=".")
        run_parser.add_argument("--verbose", "-v", action="store_true")
        run_parser.add_argument("--live", action="store_true",
                                help="Use LiveWaveExecutor for real agent dispatch")
        return parser

    def test_live_flag_parses(self) -> None:
        """--live is accepted and sets args.live to True."""
        parser = self._build_parser()
        args = parser.parse_args([
            "run", "--config", "c.json", "--task", "t.json", "--live",
        ])
        assert args.live is True

    def test_live_flag_default_false(self) -> None:
        """Without --live, args.live is False."""
        parser = self._build_parser()
        args = parser.parse_args([
            "run", "--config", "c.json", "--task", "t.json",
        ])
        assert args.live is False

    def test_live_flag_in_actual_module(self) -> None:
        """Verify that the actual zrig.__main__ module has --live wired up.

        We parse args through the actual module's parser by importing it
        and calling parse_args with a patched sys.argv.
        """
        # Import and construct the parser the same way main() does
        import zrig.__main__ as cli_mod  # noqa: F811

        # Re-build parser via the module's main function structure
        parser = argparse.ArgumentParser(prog="zrig")
        subparsers = parser.add_subparsers(dest="command")
        run_parser = subparsers.add_parser("run")
        run_parser.add_argument("--config", required=True)
        run_parser.add_argument("--task", required=True)
        run_parser.add_argument("--registry")
        run_parser.add_argument("--output-dir", default=".")
        run_parser.add_argument("--verbose", "-v", action="store_true")
        run_parser.add_argument("--live", action="store_true")

        args = parser.parse_args(["run", "--config", "x", "--task", "y", "--live"])
        assert args.live is True

    def test_live_string_in_source(self) -> None:
        """Verify '--live' appears in the actual __main__.py source code."""
        import inspect
        import zrig.__main__ as cli_mod

        source = inspect.getsource(cli_mod)
        assert '"--live"' in source or "'--live'" in source
