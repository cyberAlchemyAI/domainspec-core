"""F-DAILY-LOG-LOCK-BLOCK-MISSING (F-AMDT-12) — POST-gate on lock_history append.

Closes the F-03 residual-gap: every ``lock_history.v1.jsonl`` append must
be paired with a canonical ``## LOCK: {module}`` block in today's daily log
at the moment of LOCK. Authoring discipline becomes structural — a session
that LOCKs a module without writing the daily-log block is DENIED at the
append, not discovered by an audit weeks later.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(parent LOCK); v2.2 wave-2 delta rows for F-AMDT-12-MISSING /
F-AMDT-12-MALFORMED / F-AMDT-12-READER-FAIL.

Semantics (spec card v1, 2026-04-20):
  * Staged row missing or empty ``module`` → FAIL.
  * Backfill carve-out: ``backfilled is True`` AND
    ``verdict == "LOCKED-backfilled"`` → PASS without daily-log check.
    Only both-markers-present qualifies; a half-marked backfill (one
    without the other) runs the full gate.
  * Clock raises → FAIL F-AMDT-12-READER-FAIL.
  * Reader raises → FAIL F-AMDT-12-READER-FAIL.
  * Reader returns ``None`` (today's daily log does not exist) → FAIL
    F-AMDT-12-MISSING.
  * Block heading ``## LOCK: {module}`` must appear on a line by itself
    (trailing whitespace tolerated on the heading line only).
  * Block body ranges from the heading line to the next ``## `` heading
    or EOF.
  * All seven required fields must appear as ``- `{field}`:`` bullet
    lines with non-empty (post-strip) values. Field order not enforced.
  * Missing or empty field → FAIL F-AMDT-12-MALFORMED (detail carries
    which fields).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from pipeline.logician.gates._protocols import (
    ClockProtocol,
    DailyLogReaderCallable,
)


F_AMDT_12: str = "F-AMDT-12"
F_AMDT_12_MISSING: str = "F-AMDT-12-MISSING"
F_AMDT_12_MALFORMED: str = "F-AMDT-12-MALFORMED"
F_AMDT_12_READER_FAIL: str = "F-AMDT-12-READER-FAIL"


_REQUIRED_FIELDS: tuple[str, ...] = (
    "lock_timestamp_utc",
    "committee_round",
    "verdict",
    "code_sha3_512_prefix",
    "tests_added_this_module",
    "lines_of_code",
    "findings_surfaced_at_lock",
)


_REASON_MODULE_MISSING: str = "staged_row_module_missing"
_REASON_DAILY_LOG_ABSENT: str = "daily_log_absent_for_today"
_REASON_BLOCK_NOT_FOUND: str = "lock_block_heading_not_found"
_REASON_FIELDS_MISSING: str = "lock_block_required_fields_missing"
_REASON_CLOCK_RAISED: str = "clock_raised"
_REASON_READER_RAISED: str = "daily_log_reader_raised"


@dataclass(frozen=True, kw_only=True)
class DailyLogBlockDetail:
    reason_tag: str
    staged_module: Optional[str]
    today_iso: Optional[str]
    missing_fields: tuple[str, ...]
    reader_error: Optional[str]


@dataclass(frozen=True, kw_only=True)
class DailyLogBlockResult:
    success: bool
    failure_code: Optional[str]
    detail: Optional[DailyLogBlockDetail]


def _fail(
    *,
    failure_code: str,
    reason_tag: str,
    staged_module: Optional[str] = None,
    today_iso: Optional[str] = None,
    missing_fields: tuple[str, ...] = (),
    reader_error: Optional[str] = None,
) -> DailyLogBlockResult:
    return DailyLogBlockResult(
        success=False,
        failure_code=failure_code,
        detail=DailyLogBlockDetail(
            reason_tag=reason_tag,
            staged_module=staged_module,
            today_iso=today_iso,
            missing_fields=missing_fields,
            reader_error=reader_error,
        ),
    )


def _ok() -> DailyLogBlockResult:
    return DailyLogBlockResult(success=True, failure_code=None, detail=None)


def _get_nonempty_str(d: dict, key: str) -> Optional[str]:
    v = d.get(key)
    if isinstance(v, str) and v != "":
        return v
    return None


def _is_backfill_carveout(staged_row: dict) -> bool:
    return (
        staged_row.get("backfilled") is True
        and staged_row.get("verdict") == "LOCKED-backfilled"
    )


def _extract_block_body(daily_log_text: str, module: str) -> Optional[str]:
    """Return the text of the LOCK block for ``module`` (without the heading
    line), or ``None`` if no block heading is found.

    The block body starts on the line AFTER the ``## LOCK: {module}`` heading
    and ends at the next line beginning with ``## `` (another second-level
    heading) or EOF.
    """
    lines = daily_log_text.splitlines()
    heading_idx: Optional[int] = None
    for i, line in enumerate(lines):
        # Heading line: '## LOCK: {module}' with optional trailing whitespace
        stripped = line.rstrip()
        if stripped == f"## LOCK: {module}":
            heading_idx = i
            break
    if heading_idx is None:
        return None
    end_idx = len(lines)
    for j in range(heading_idx + 1, len(lines)):
        if lines[j].startswith("## "):
            end_idx = j
            break
    body_lines = lines[heading_idx + 1 : end_idx]
    return "\n".join(body_lines)


_FIELD_LINE_RE = re.compile(r"^-\s+`(?P<field>[^`]+)`\s*:\s*(?P<value>.*)$")


def _parse_field_values(block_body: str) -> dict[str, str]:
    """Extract field→value dict from bullet lines of the form
    ``- `field`: value`` inside the block body. Values are returned as
    post-strip strings (may be empty; caller checks for emptiness)."""
    result: dict[str, str] = {}
    for line in block_body.splitlines():
        m = _FIELD_LINE_RE.match(line)
        if m is None:
            continue
        field = m.group("field")
        value = m.group("value").strip()
        # First occurrence wins (duplicates are caller's concern)
        if field not in result:
            result[field] = value
    return result


def check_daily_log_lock_block(
    *,
    staged_row: dict,
    clock: ClockProtocol,
    daily_log_reader: DailyLogReaderCallable,
) -> DailyLogBlockResult:
    """POST-gate F-DAILY-LOG-LOCK-BLOCK-MISSING (F-AMDT-12).

    Returns PASS if today's daily log contains a canonical
    ``## LOCK: {module}`` block with all seven required non-empty fields.
    Returns a backfill-carve-out PASS when ``backfilled is True`` AND
    ``verdict == "LOCKED-backfilled"``.
    """
    module = _get_nonempty_str(staged_row, "module")
    if module is None:
        return _fail(
            failure_code=F_AMDT_12,
            reason_tag=_REASON_MODULE_MISSING,
        )

    # Backfill carve-out (narrow — both markers required)
    if _is_backfill_carveout(staged_row):
        return _ok()

    try:
        now = clock.now_utc()
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_12_READER_FAIL,
            reason_tag=_REASON_CLOCK_RAISED,
            staged_module=module,
            reader_error=f"clock: {type(exc).__name__}: {exc}"[:500],
        )

    today_iso = now.date().isoformat()

    try:
        log_text = daily_log_reader(today_iso)
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_12_READER_FAIL,
            reason_tag=_REASON_READER_RAISED,
            staged_module=module,
            today_iso=today_iso,
            reader_error=f"daily_log_reader: {type(exc).__name__}: {exc}"[:500],
        )

    if log_text is None:
        return _fail(
            failure_code=F_AMDT_12_MISSING,
            reason_tag=_REASON_DAILY_LOG_ABSENT,
            staged_module=module,
            today_iso=today_iso,
        )

    block_body = _extract_block_body(log_text, module)
    if block_body is None:
        return _fail(
            failure_code=F_AMDT_12_MISSING,
            reason_tag=_REASON_BLOCK_NOT_FOUND,
            staged_module=module,
            today_iso=today_iso,
        )

    field_values = _parse_field_values(block_body)
    missing: list[str] = []
    for field in _REQUIRED_FIELDS:
        value = field_values.get(field)
        if value is None or value == "":
            missing.append(field)

    if missing:
        return _fail(
            failure_code=F_AMDT_12_MALFORMED,
            reason_tag=_REASON_FIELDS_MISSING,
            staged_module=module,
            today_iso=today_iso,
            missing_fields=tuple(missing),
        )

    return _ok()
