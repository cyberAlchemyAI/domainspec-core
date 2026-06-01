"""MEMORY.md auto-consolidation **trigger** layer.

Scope
-----
The :mod:`pipeline.memory.consolidate_index` module already exposes a
deterministic consolidation engine and CLI verb (``tilth memory
consolidate-index``). The engine fires when ``MEMORY.md`` exceeds a soft
threshold (default 20 KiB; hard cap 24 KiB at the Cowork auto-memory
loader). But the engine only runs on **explicit invocation** — there is no
ambient watchdog that says "you should consolidate now."

This module is that watchdog. It is intended to run as a preflight check
during the workspace wake-up sequence (per ``AGENTS.md`` step 6) and at
the start of any session-close audit. It compares the live ``MEMORY.md``
against a *lower* early-warning threshold (default 200 lines / 12 KiB)
and signals a trigger event. The trigger can either:

* **Signal only** (default) — print a human-readable trigger banner and
  exit with code 10 so a calling shell can react (e.g., emit a Cowork
  hint to fire the ``consolidate-memory`` skill).
* **Run** (``--run``) — invoke :func:`run_consolidation` from the engine
  directly. Useful for unattended / scheduled-task contexts.

The early-warning threshold sits *below* the engine's own threshold by
design — it nudges the operator (or the agent) to consolidate before the
file slides past the 20 KiB threshold and well before the 24 KiB hard cap
where Cowork silently truncates. Layered defense-in-depth:

* ``MEMORY_TRIGGER_*`` (this module)  → 12 KiB / 200 lines → early warning
* ``DEFAULT_THRESHOLD_BYTES``         → 20 KiB              → actual consolidation
* ``HARD_LOAD_LIMIT_BYTES``           → 24 KiB              → Cowork hard cap

Discipline
----------
* Pure-Python, no third-party imports. Same substrate-pin discipline as
  the engine.
* Every fired trigger appends a JSONL line to the trigger log at
  ``pipeline/institutional_memory/memory_consolidation_log.jsonl`` so the
  trigger history is auditable.
* Configurable via env vars and CLI flags. Env vars used at module-import
  time as defaults; CLI flags override; explicit function args override
  both.

Configuration
-------------
Env vars (all optional):

* ``MEMORY_TRIGGER_LINES`` — int line threshold (default 200).
* ``MEMORY_TRIGGER_BYTES`` — int byte threshold (default 12288 = 12 KiB).
* ``MEMORY_PATH``          — absolute path to ``MEMORY.md`` (default
  ``./MEMORY.md`` resolved against current working directory).
* ``MEMORY_TRIGGER_LOG``   — absolute path to the JSONL trigger log
  (default ``./pipeline/institutional_memory/memory_consolidation_log.jsonl``).

A trigger fires when **either** of the two thresholds (lines OR bytes) is
crossed — whichever hits first wins.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------


# Early-warning thresholds. Per CLAUDE.md memory hygiene + the
# consolidate-memory SKILL.md guidance ("MEMORY.md ... under 200 lines and
# ~25KB"), the line-budget hint is 200. The byte budget is set tighter
# (12 KiB) so the early-warning fires before the engine's 20 KiB threshold.
DEFAULT_LINE_THRESHOLD: int = 200
DEFAULT_BYTE_THRESHOLD: int = 12288  # 12 KiB


# Repo-relative path to the trigger log. The log is JSONL — one event per
# line — so it can be grep'd / tailed / appended without locking.
DEFAULT_LOG_RELATIVE: Path = Path(
    "pipeline/institutional_memory/memory_consolidation_log.jsonl"
)


# Exit-code convention for the CLI:
EXIT_UNDER_THRESHOLD: int = 0   # no-op
EXIT_TRIGGER_FIRED: int = 10    # over threshold; trigger signaled (or ran)
EXIT_ERROR: int = 1             # input error


# Repo-relative path to MEMORY.md.
DEFAULT_MEMORY_RELATIVE: Path = Path("MEMORY.md")


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class MemoryTriggerError(Exception):
    """Raised when the trigger cannot inspect MEMORY.md."""


# ---------------------------------------------------------------------------
# Outcome dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TriggerOutcome:
    """Outcome of one ``check_memory_size`` call.

    Attributes
    ----------
    fired
        True iff the byte OR line threshold was crossed.
    memory_path
        Absolute path to the inspected MEMORY.md.
    size_bytes
        Observed UTF-8 byte size of MEMORY.md.
    line_count
        Observed line count of MEMORY.md (count of ``\\n`` boundaries plus
        one for the trailing content if any; matches ``wc -l`` semantics
        when the file ends in a newline).
    byte_threshold
        Threshold the byte size was compared against.
    line_threshold
        Threshold the line count was compared against.
    reason
        Human-readable reason string when ``fired``; empty string when
        not fired.
    """

    fired: bool
    memory_path: Path
    size_bytes: int
    line_count: int
    byte_threshold: int
    line_threshold: int
    reason: str


# ---------------------------------------------------------------------------
# Env resolution
# ---------------------------------------------------------------------------


def _env_int(name: str, default: int) -> int:
    """Resolve an int env var; fall back to ``default`` on absence / bad value."""
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        value = int(raw.strip())
    except ValueError:
        return default
    if value <= 0:
        return default
    return value


def _env_path(name: str, default: Path) -> Path:
    """Resolve a path env var; fall back to ``default`` on absence."""
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    return Path(raw.strip()).expanduser()


def resolve_thresholds(
    *,
    line_threshold: Optional[int] = None,
    byte_threshold: Optional[int] = None,
) -> tuple[int, int]:
    """Resolve thresholds in priority order: explicit arg > env var > default.

    Returns (line_threshold, byte_threshold).
    """
    line = (
        line_threshold
        if line_threshold is not None
        else _env_int("MEMORY_TRIGGER_LINES", DEFAULT_LINE_THRESHOLD)
    )
    byte = (
        byte_threshold
        if byte_threshold is not None
        else _env_int("MEMORY_TRIGGER_BYTES", DEFAULT_BYTE_THRESHOLD)
    )
    if line <= 0:
        raise MemoryTriggerError(
            f"line_threshold must be > 0; got {line}"
        )
    if byte <= 0:
        raise MemoryTriggerError(
            f"byte_threshold must be > 0; got {byte}"
        )
    return line, byte


def resolve_memory_path(memory_path: Optional[Path] = None) -> Path:
    """Resolve MEMORY.md path: explicit arg > env var > ./MEMORY.md."""
    if memory_path is not None:
        return memory_path
    return _env_path("MEMORY_PATH", Path.cwd() / DEFAULT_MEMORY_RELATIVE)


def resolve_log_path(log_path: Optional[Path] = None) -> Path:
    """Resolve trigger-log path: explicit arg > env var > default relative."""
    if log_path is not None:
        return log_path
    return _env_path(
        "MEMORY_TRIGGER_LOG",
        Path.cwd() / DEFAULT_LOG_RELATIVE,
    )


# ---------------------------------------------------------------------------
# Size measurement
# ---------------------------------------------------------------------------


def measure_memory(memory_path: Path) -> tuple[int, int]:
    """Read ``MEMORY.md`` and return ``(size_bytes, line_count)``.

    Line count matches ``wc -l`` semantics: it counts newline characters.
    A trailing line without a newline is not counted as a separate line.
    """
    if not memory_path.is_file():
        raise MemoryTriggerError(
            f"MEMORY.md not found at {memory_path!s}"
        )
    raw = memory_path.read_bytes()
    size_bytes = len(raw)
    line_count = raw.count(b"\n")
    return size_bytes, line_count


# ---------------------------------------------------------------------------
# Core check
# ---------------------------------------------------------------------------


def check_memory_size(
    *,
    memory_path: Optional[Path] = None,
    line_threshold: Optional[int] = None,
    byte_threshold: Optional[int] = None,
) -> TriggerOutcome:
    """Inspect MEMORY.md against thresholds; return outcome.

    A trigger fires when **either** threshold is crossed (size strictly
    greater than threshold). Boundary semantics: at exactly the threshold,
    the trigger does NOT fire — only when the file is *over* it. This
    mirrors the engine's ``consolidate_index`` boundary semantics so the
    two layers stay consistent.
    """
    resolved_path = resolve_memory_path(memory_path)
    resolved_lines, resolved_bytes = resolve_thresholds(
        line_threshold=line_threshold,
        byte_threshold=byte_threshold,
    )
    size_bytes, line_count = measure_memory(resolved_path)

    over_bytes = size_bytes > resolved_bytes
    over_lines = line_count > resolved_lines
    fired = over_bytes or over_lines

    reason_parts: list[str] = []
    if over_bytes:
        reason_parts.append(
            f"bytes={size_bytes} > byte_threshold={resolved_bytes}"
        )
    if over_lines:
        reason_parts.append(
            f"lines={line_count} > line_threshold={resolved_lines}"
        )
    reason = "; ".join(reason_parts)

    return TriggerOutcome(
        fired=fired,
        memory_path=resolved_path,
        size_bytes=size_bytes,
        line_count=line_count,
        byte_threshold=resolved_bytes,
        line_threshold=resolved_lines,
        reason=reason,
    )


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def _utc_now_iso() -> str:
    """ISO-8601 UTC timestamp at second precision, ``Z``-suffixed."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_trigger_event(
    outcome: TriggerOutcome,
    *,
    action: str,
    log_path: Optional[Path] = None,
    extra: Optional[dict] = None,
) -> Path:
    """Append a JSONL line to the trigger log; return the log path used.

    The parent directory is created on demand (``mkdir(parents=True,
    exist_ok=True)``). The function is idempotent at the line level —
    each call appends one line.

    Parameters
    ----------
    outcome
        The trigger outcome to record.
    action
        Free-form action label. Typical values:

        * ``"trigger_signaled"`` — CLI exited code 10 to nudge a caller.
        * ``"trigger_ran"`` — CLI invoked ``run_consolidation`` directly.
        * ``"under_threshold"`` — recorded a clean preflight pass
          (optional; controlled by ``--log-clean`` at the CLI).

    log_path
        Absolute path to the JSONL log. Defaults to env / repo-relative.
    extra
        Optional dict merged into the JSONL record under arbitrary keys
        (e.g., consolidation result fields when ``action="trigger_ran"``).
    """
    resolved_log = resolve_log_path(log_path)
    resolved_log.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts_utc": _utc_now_iso(),
        "action": action,
        "fired": outcome.fired,
        "memory_path": str(outcome.memory_path),
        "size_bytes": outcome.size_bytes,
        "line_count": outcome.line_count,
        "byte_threshold": outcome.byte_threshold,
        "line_threshold": outcome.line_threshold,
        "reason": outcome.reason,
    }
    if extra:
        record.update(extra)
    with open(resolved_log, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return resolved_log


# ---------------------------------------------------------------------------
# High-level entry point
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AutoTriggerResult:
    """Combined trigger + (optional) consolidation outcome."""

    outcome: TriggerOutcome
    action: str
    consolidation_summary: Optional[dict]
    log_path: Optional[Path]


def run_auto_trigger(
    *,
    memory_path: Optional[Path] = None,
    line_threshold: Optional[int] = None,
    byte_threshold: Optional[int] = None,
    do_consolidate: bool = False,
    log_clean: bool = False,
    log_path: Optional[Path] = None,
    repo_root: Optional[Path] = None,
) -> AutoTriggerResult:
    """Top-level entry: check threshold, optionally consolidate, log.

    When ``do_consolidate`` is True and the trigger fires, this function
    invokes :func:`pipeline.memory.consolidate_index.run_consolidation`
    against the parent directory of ``MEMORY.md`` with the engine's own
    threshold (20 KiB). When False, only the trigger event is logged and
    the caller is expected to react to ``EXIT_TRIGGER_FIRED``.

    When the trigger does NOT fire:

    * If ``log_clean`` is True, append an ``under_threshold`` event and
      return. Useful when the preflight is part of an audited wake-up.
    * Otherwise, return without writing anything (low-noise default).
    """
    outcome = check_memory_size(
        memory_path=memory_path,
        line_threshold=line_threshold,
        byte_threshold=byte_threshold,
    )

    if not outcome.fired:
        log_written: Optional[Path] = None
        if log_clean:
            log_written = log_trigger_event(
                outcome,
                action="under_threshold",
                log_path=log_path,
            )
        return AutoTriggerResult(
            outcome=outcome,
            action="under_threshold",
            consolidation_summary=None,
            log_path=log_written,
        )

    consolidation_summary: Optional[dict] = None
    action: str

    if do_consolidate:
        # Local import keeps the trigger module importable even if the
        # engine is being refactored.
        from pipeline.memory.consolidate_index import run_consolidation

        memory_dir = outcome.memory_path.parent
        engine_outcome = run_consolidation(
            memory_dir=memory_dir,
            repo_root=repo_root,
        )
        consolidation_summary = {
            "engine_fired": engine_outcome.result.fired,
            "entries_kept": engine_outcome.result.entries_kept,
            "entries_archived": engine_outcome.result.entries_archived,
            "original_size_bytes": engine_outcome.result.original_size_bytes,
            "new_size_bytes": engine_outcome.result.new_size_bytes,
            "archive_path": (
                str(engine_outcome.archive_path)
                if engine_outcome.archive_path is not None
                else None
            ),
            "lock_history_row_appended": (
                engine_outcome.lock_history_row_appended
            ),
        }
        action = "trigger_ran"
    else:
        action = "trigger_signaled"

    log_written = log_trigger_event(
        outcome,
        action=action,
        log_path=log_path,
        extra=(
            {"consolidation": consolidation_summary}
            if consolidation_summary is not None
            else None
        ),
    )

    return AutoTriggerResult(
        outcome=outcome,
        action=action,
        consolidation_summary=consolidation_summary,
        log_path=log_written,
    )
