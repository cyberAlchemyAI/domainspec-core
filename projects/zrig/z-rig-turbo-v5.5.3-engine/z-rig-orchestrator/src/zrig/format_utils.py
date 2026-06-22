"""Format utilities for the Z-Rig orchestrator.

Provides human-readable formatting for durations, timestamps, and wave
result summaries used throughout the pipeline reporting layer.

Synthesized from HRR-006 W2 builders B1 (Sonnet) + B2 (Opus).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def format_duration(seconds: float) -> str:
    """Convert a duration in seconds to a compact human-readable string.

    Args:
        seconds: Non-negative number of seconds.

    Returns:
        Formatted string such as ``"1h 5m 3s"`` or ``"0s"``.

    Raises:
        ValueError: If *seconds* is negative.
        TypeError: If *seconds* is not a number.
    """
    if not isinstance(seconds, (int, float)):
        raise TypeError(f"Expected int or float, got {type(seconds).__name__}")
    if seconds < 0:
        raise ValueError(f"Duration must be non-negative, got {seconds}")

    if seconds == 0:
        return "0s"

    # Handle sub-second values without decomposition (from B2)
    if seconds < 1:
        return f"{seconds:g}s"

    total = int(seconds)
    frac = seconds - total

    days, remainder = divmod(total, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)

    # Re-add fractional part to seconds
    secs_f: float = secs + frac

    parts: list[str] = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if secs_f:
        if secs_f == int(secs_f):
            parts.append(f"{int(secs_f)}s")
        else:
            parts.append(f"{secs_f:g}s")

    return " ".join(parts) if parts else "0s"


def format_timestamp(dt: datetime | None = None) -> str:
    """Format a datetime to an ISO-8601 string with timezone info.

    Args:
        dt: Datetime to format.  If ``None``, the current UTC time is used.
            Naive datetimes (no ``tzinfo``) are treated as UTC.

    Returns:
        ISO-8601 formatted string including timezone offset.

    Raises:
        TypeError: If *dt* is not a ``datetime`` instance or ``None``.
    """
    if dt is not None and not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime or None, got {type(dt).__name__}")

    if dt is None:
        dt = datetime.now(timezone.utc)
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.isoformat()


def format_wave_summary(wave_results: list[dict[str, Any]]) -> str:
    """Format wave results into an aligned text table.

    Args:
        wave_results: List of dicts each containing the keys
            ``wave_id``, ``status``, ``duration_s``, and ``gate_result``.

    Returns:
        Multi-line string with a header row, separator, and one data row
        per wave result.  Returns a header-only table when the list is empty.

    Raises:
        TypeError: If *wave_results* is not a list or contains non-dict items.
        KeyError: If a required key is missing from any result dict.
    """
    if not isinstance(wave_results, list):
        raise TypeError(f"Expected list, got {type(wave_results).__name__}")

    required_keys = ("wave_id", "status", "duration_s", "gate_result")
    headers = ("Wave", "Status", "Duration", "Gate")

    # Pre-format rows so we can compute column widths.
    rows: list[tuple[str, str, str, str]] = []
    for i, entry in enumerate(wave_results):
        if not isinstance(entry, dict):
            raise TypeError(f"Item {i} is not a dict: {type(entry).__name__}")
        missing = [k for k in required_keys if k not in entry]
        if missing:
            raise KeyError(f"Item {i} missing keys: {', '.join(missing)}")
        rows.append((
            str(entry["wave_id"]),
            str(entry["status"]),
            format_duration(entry["duration_s"]),
            str(entry["gate_result"]),
        ))

    # Compute column widths (at least as wide as headers).
    widths = [len(h) for h in headers]
    for row in rows:
        for col_idx, cell in enumerate(row):
            widths[col_idx] = max(widths[col_idx], len(cell))

    def _fmt_row(cells: tuple[str, ...]) -> str:
        return "  ".join(cell.ljust(widths[idx]) for idx, cell in enumerate(cells))

    lines: list[str] = [_fmt_row(headers)]
    lines.append("  ".join("-" * w for w in widths))
    for row in rows:
        lines.append(_fmt_row(row))

    return "\n".join(lines)
