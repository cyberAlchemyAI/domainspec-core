"""Tests for ``pipeline.memory.auto_consolidate_trigger``.

Trigger thresholds
------------------
* 250-line fixture → fires (over default 200-line threshold).
* 100-line fixture → does NOT fire (under default 200-line threshold).
* Exactly-200-line fixture → does NOT fire (boundary inclusive on the
  *under* side; mirrors the engine's ``consolidate_index`` semantics).
* 13 KiB fixture under 100 lines → fires on byte threshold.
* 11 KiB fixture under 100 lines → does NOT fire.

Configurability
---------------
* ``MEMORY_TRIGGER_LINES`` env var overrides the default line threshold.
* ``MEMORY_TRIGGER_BYTES`` env var overrides the default byte threshold.
* Explicit function args override env vars and defaults.

Side effects
------------
* Fired triggers append a JSONL line to the log path.
* ``--log-clean`` mode also logs under_threshold events.
* The trigger log parent directory is created on demand.

CLI surface
-----------
* ``tilth memory auto-trigger`` exit code 10 when fires, 0 when under.
* ``--run`` flag invokes the engine when threshold crossed.

The fixtures are synthesized per-test so the suite is hermetic — no
dependency on the live MEMORY.md on disk.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from pipeline.memory.auto_consolidate_trigger import (
    DEFAULT_BYTE_THRESHOLD,
    DEFAULT_LINE_THRESHOLD,
    EXIT_TRIGGER_FIRED,
    EXIT_UNDER_THRESHOLD,
    MemoryTriggerError,
    AutoTriggerResult,
    check_memory_size,
    log_trigger_event,
    measure_memory,
    resolve_thresholds,
    run_auto_trigger,
)


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------


def _write_memory(
    tmp_path: Path,
    *,
    lines: int,
    line_payload: str = "- [Entry](file.md) — short hook line\n",
) -> Path:
    """Write a MEMORY.md fixture with ``lines`` lines.

    Each line is ``line_payload`` (which must end in a newline). The
    file's line count matches ``wc -l`` semantics.
    """
    assert line_payload.endswith("\n"), "payload must end in newline"
    path = tmp_path / "MEMORY.md"
    path.write_text(line_payload * lines, encoding="utf-8")
    return path


def _write_memory_bytes(
    tmp_path: Path,
    *,
    size_bytes: int,
) -> Path:
    """Write a MEMORY.md fixture of approx ``size_bytes`` bytes, low line count.

    Uses one very long line so byte threshold can be tested independent
    of the line threshold.
    """
    path = tmp_path / "MEMORY.md"
    # Two newlines so wc -l = 2 (header + body), well under any sane
    # line threshold even when bytes are large.
    header = "# title\n"
    body_size = max(0, size_bytes - len(header) - 1)
    body = ("x" * body_size) + "\n"
    path.write_text(header + body, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Threshold resolution
# ---------------------------------------------------------------------------


def test_defaults_match_spec():
    assert DEFAULT_LINE_THRESHOLD == 200
    assert DEFAULT_BYTE_THRESHOLD == 12288


def test_resolve_thresholds_uses_defaults(monkeypatch):
    monkeypatch.delenv("MEMORY_TRIGGER_LINES", raising=False)
    monkeypatch.delenv("MEMORY_TRIGGER_BYTES", raising=False)
    lines, byte = resolve_thresholds()
    assert lines == DEFAULT_LINE_THRESHOLD
    assert byte == DEFAULT_BYTE_THRESHOLD


def test_resolve_thresholds_env_overrides(monkeypatch):
    monkeypatch.setenv("MEMORY_TRIGGER_LINES", "300")
    monkeypatch.setenv("MEMORY_TRIGGER_BYTES", "20000")
    lines, byte = resolve_thresholds()
    assert lines == 300
    assert byte == 20000


def test_resolve_thresholds_explicit_overrides_env(monkeypatch):
    monkeypatch.setenv("MEMORY_TRIGGER_LINES", "300")
    monkeypatch.setenv("MEMORY_TRIGGER_BYTES", "20000")
    lines, byte = resolve_thresholds(line_threshold=50, byte_threshold=99)
    assert lines == 50
    assert byte == 99


def test_resolve_thresholds_rejects_nonpositive():
    with pytest.raises(MemoryTriggerError):
        resolve_thresholds(line_threshold=0)
    with pytest.raises(MemoryTriggerError):
        resolve_thresholds(byte_threshold=-1)


def test_resolve_thresholds_bad_env_falls_back(monkeypatch):
    monkeypatch.setenv("MEMORY_TRIGGER_LINES", "not-a-number")
    lines, _ = resolve_thresholds()
    assert lines == DEFAULT_LINE_THRESHOLD


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------


def test_measure_memory_counts_lines_like_wc(tmp_path):
    path = _write_memory(tmp_path, lines=42)
    size_bytes, line_count = measure_memory(path)
    assert line_count == 42
    assert size_bytes > 0


def test_measure_memory_missing_file(tmp_path):
    with pytest.raises(MemoryTriggerError):
        measure_memory(tmp_path / "absent.md")


# ---------------------------------------------------------------------------
# Trigger threshold semantics (LINE axis)
# ---------------------------------------------------------------------------


def test_trigger_fires_at_250_lines(tmp_path, monkeypatch):
    monkeypatch.delenv("MEMORY_TRIGGER_LINES", raising=False)
    monkeypatch.delenv("MEMORY_TRIGGER_BYTES", raising=False)
    path = _write_memory(tmp_path, lines=250)
    outcome = check_memory_size(memory_path=path)
    assert outcome.fired is True
    assert outcome.line_count == 250
    assert "lines=" in outcome.reason


def test_trigger_does_not_fire_at_100_lines(tmp_path, monkeypatch):
    monkeypatch.delenv("MEMORY_TRIGGER_LINES", raising=False)
    monkeypatch.delenv("MEMORY_TRIGGER_BYTES", raising=False)
    path = _write_memory(
        tmp_path,
        lines=100,
        # Short payload to keep bytes under 12 KiB:
        line_payload="x\n",
    )
    outcome = check_memory_size(memory_path=path)
    assert outcome.fired is False
    assert outcome.line_count == 100
    assert outcome.reason == ""


def test_trigger_boundary_exactly_at_line_threshold_does_not_fire(
    tmp_path, monkeypatch
):
    """Strict ``>`` semantics: equal to threshold is NOT over."""
    monkeypatch.delenv("MEMORY_TRIGGER_LINES", raising=False)
    monkeypatch.delenv("MEMORY_TRIGGER_BYTES", raising=False)
    path = _write_memory(
        tmp_path,
        lines=DEFAULT_LINE_THRESHOLD,
        line_payload="x\n",  # keep bytes well under 12 KiB
    )
    outcome = check_memory_size(memory_path=path)
    assert outcome.fired is False
    assert outcome.line_count == DEFAULT_LINE_THRESHOLD


# ---------------------------------------------------------------------------
# Trigger threshold semantics (BYTE axis)
# ---------------------------------------------------------------------------


def test_trigger_fires_on_byte_threshold(tmp_path, monkeypatch):
    monkeypatch.delenv("MEMORY_TRIGGER_LINES", raising=False)
    monkeypatch.delenv("MEMORY_TRIGGER_BYTES", raising=False)
    # 13 KiB → over the 12 KiB default
    path = _write_memory_bytes(tmp_path, size_bytes=13312)
    outcome = check_memory_size(memory_path=path)
    assert outcome.fired is True
    assert outcome.size_bytes > DEFAULT_BYTE_THRESHOLD
    assert "bytes=" in outcome.reason


def test_trigger_does_not_fire_under_byte_threshold(tmp_path, monkeypatch):
    monkeypatch.delenv("MEMORY_TRIGGER_LINES", raising=False)
    monkeypatch.delenv("MEMORY_TRIGGER_BYTES", raising=False)
    # 11 KiB, low line count → under both
    path = _write_memory_bytes(tmp_path, size_bytes=11264)
    outcome = check_memory_size(memory_path=path)
    assert outcome.fired is False


def test_explicit_threshold_arg_wins_over_env(tmp_path, monkeypatch):
    monkeypatch.setenv("MEMORY_TRIGGER_LINES", "50")
    path = _write_memory(tmp_path, lines=100, line_payload="x\n")
    # Env says 50, would fire at 100. Explicit arg 1000 → does not fire.
    outcome = check_memory_size(memory_path=path, line_threshold=1000)
    assert outcome.fired is False


# ---------------------------------------------------------------------------
# Env-var memory_path resolution
# ---------------------------------------------------------------------------


def test_env_memory_path_resolves(tmp_path, monkeypatch):
    path = _write_memory(tmp_path, lines=10, line_payload="x\n")
    monkeypatch.setenv("MEMORY_PATH", str(path))
    monkeypatch.delenv("MEMORY_TRIGGER_LINES", raising=False)
    monkeypatch.delenv("MEMORY_TRIGGER_BYTES", raising=False)
    outcome = check_memory_size()
    assert outcome.memory_path == path
    assert outcome.fired is False


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def test_log_trigger_event_writes_jsonl(tmp_path):
    path = _write_memory(tmp_path, lines=250)
    outcome = check_memory_size(memory_path=path)
    log_path = tmp_path / "subdir" / "memory_log.jsonl"
    written = log_trigger_event(
        outcome,
        action="trigger_signaled",
        log_path=log_path,
    )
    assert written == log_path
    assert log_path.is_file()
    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["action"] == "trigger_signaled"
    assert record["fired"] is True
    assert record["line_count"] == 250
    assert "ts_utc" in record


def test_log_trigger_event_appends(tmp_path):
    path = _write_memory(tmp_path, lines=250)
    outcome = check_memory_size(memory_path=path)
    log_path = tmp_path / "memory_log.jsonl"
    log_trigger_event(outcome, action="trigger_signaled", log_path=log_path)
    log_trigger_event(outcome, action="trigger_signaled", log_path=log_path)
    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2


def test_log_trigger_event_extra_merges(tmp_path):
    path = _write_memory(tmp_path, lines=250)
    outcome = check_memory_size(memory_path=path)
    log_path = tmp_path / "memory_log.jsonl"
    log_trigger_event(
        outcome,
        action="trigger_ran",
        log_path=log_path,
        extra={"engine_summary": {"entries_archived": 7}},
    )
    record = json.loads(log_path.read_text(encoding="utf-8").splitlines()[0])
    assert record["engine_summary"] == {"entries_archived": 7}


# ---------------------------------------------------------------------------
# High-level run_auto_trigger
# ---------------------------------------------------------------------------


def test_run_auto_trigger_signal_only_path(tmp_path, monkeypatch):
    monkeypatch.delenv("MEMORY_TRIGGER_LINES", raising=False)
    monkeypatch.delenv("MEMORY_TRIGGER_BYTES", raising=False)
    path = _write_memory(tmp_path, lines=250)
    log_path = tmp_path / "log.jsonl"
    result = run_auto_trigger(memory_path=path, log_path=log_path)
    assert isinstance(result, AutoTriggerResult)
    assert result.outcome.fired is True
    assert result.action == "trigger_signaled"
    assert result.consolidation_summary is None
    assert result.log_path == log_path
    assert log_path.is_file()


def test_run_auto_trigger_under_threshold_quiet(tmp_path, monkeypatch):
    monkeypatch.delenv("MEMORY_TRIGGER_LINES", raising=False)
    monkeypatch.delenv("MEMORY_TRIGGER_BYTES", raising=False)
    path = _write_memory(tmp_path, lines=10, line_payload="x\n")
    log_path = tmp_path / "log.jsonl"
    result = run_auto_trigger(memory_path=path, log_path=log_path)
    assert result.outcome.fired is False
    assert result.action == "under_threshold"
    assert result.log_path is None
    # log_clean=False default → no log file
    assert not log_path.exists()


def test_run_auto_trigger_log_clean_writes_under_threshold(
    tmp_path, monkeypatch
):
    monkeypatch.delenv("MEMORY_TRIGGER_LINES", raising=False)
    monkeypatch.delenv("MEMORY_TRIGGER_BYTES", raising=False)
    path = _write_memory(tmp_path, lines=10, line_payload="x\n")
    log_path = tmp_path / "log.jsonl"
    result = run_auto_trigger(
        memory_path=path,
        log_path=log_path,
        log_clean=True,
    )
    assert result.outcome.fired is False
    assert result.log_path == log_path
    record = json.loads(log_path.read_text().splitlines()[0])
    assert record["action"] == "under_threshold"
    assert record["fired"] is False


# ---------------------------------------------------------------------------
# CLI surface
# ---------------------------------------------------------------------------


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _cli_run(args, env_extra=None, cwd=None):
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    # Use sys.executable so the test runs under the same interpreter
    # pytest is using (the pinned .venv per scripts/run_tests.sh).
    return subprocess.run(
        [sys.executable, "-m", "pipeline.cli.tilth_memory", *args],
        env=env,
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
    )


def test_cli_auto_trigger_fires_returns_10(tmp_path):
    path = _write_memory(tmp_path, lines=250)
    log_path = tmp_path / "log.jsonl"
    proc = _cli_run(
        [
            "auto-trigger",
            "--memory-path",
            str(path),
            "--log-path",
            str(log_path),
            "--json-output",
        ]
    )
    assert proc.returncode == EXIT_TRIGGER_FIRED, proc.stderr
    summary = json.loads(proc.stdout)
    assert summary["fired"] is True
    assert summary["action"] == "trigger_signaled"
    assert summary["line_count"] == 250
    assert log_path.is_file()


def test_cli_auto_trigger_under_returns_0(tmp_path):
    path = _write_memory(tmp_path, lines=10, line_payload="x\n")
    proc = _cli_run(
        [
            "auto-trigger",
            "--memory-path",
            str(path),
            "--json-output",
        ]
    )
    assert proc.returncode == EXIT_UNDER_THRESHOLD, proc.stderr
    summary = json.loads(proc.stdout)
    assert summary["fired"] is False


def test_cli_auto_trigger_threshold_override(tmp_path):
    path = _write_memory(tmp_path, lines=50, line_payload="x\n")
    # Lower threshold so 50 lines fires.
    proc = _cli_run(
        [
            "auto-trigger",
            "--memory-path",
            str(path),
            "--threshold-lines",
            "30",
            "--threshold-bytes",
            "1000000",
            "--json-output",
        ]
    )
    assert proc.returncode == EXIT_TRIGGER_FIRED, proc.stderr
    summary = json.loads(proc.stdout)
    assert summary["fired"] is True
    assert summary["line_threshold"] == 30


def test_cli_auto_trigger_env_override(tmp_path):
    path = _write_memory(tmp_path, lines=50, line_payload="x\n")
    log_path = tmp_path / "log.jsonl"
    proc = _cli_run(
        [
            "auto-trigger",
            "--memory-path",
            str(path),
            "--log-path",
            str(log_path),
            "--json-output",
        ],
        env_extra={
            "MEMORY_TRIGGER_LINES": "30",
            "MEMORY_TRIGGER_BYTES": "1000000",
        },
    )
    assert proc.returncode == EXIT_TRIGGER_FIRED, proc.stderr
    summary = json.loads(proc.stdout)
    assert summary["line_threshold"] == 30


def test_cli_auto_trigger_quiet_mode(tmp_path):
    path = _write_memory(tmp_path, lines=10, line_payload="x\n")
    proc = _cli_run(
        [
            "auto-trigger",
            "--memory-path",
            str(path),
            "--quiet",
        ]
    )
    assert proc.returncode == EXIT_UNDER_THRESHOLD
    # Quiet suppresses the CLI's own auto-trigger banner. Other modules
    # in the import chain (e.g., the logfire shim) may still emit warnings
    # on stderr — assert only that our human-readable banner is absent.
    assert "MEMORY.md auto-trigger" not in proc.stderr
    assert "under threshold" not in proc.stderr
