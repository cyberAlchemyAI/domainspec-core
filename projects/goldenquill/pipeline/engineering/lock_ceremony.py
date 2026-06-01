"""pipeline.engineering.lock_ceremony — canonical LOCK-append entry point.

All future LOCKs (committee-attested code LOCKs, self-LOCKs, narrow-fix
backfills) compose ``record_verdict`` + ``append_lock_history`` from
``pipeline.harness.gates`` through this single function. Sessions that
hand-append rows to ``pipeline/engineering/lock_history.v1.jsonl`` bypass
the v2.2 amendment-enforcement gates (F-AMDT-02 / F-AMDT-03 / F-AMDT-12)
and will appear as ungated activity in the session-log audit.

Design posture per LOCK row 126 (Task 1 v2.2 wire-in, 2026-04-22): Option A
keeps the v2.2 gates **outside** the §4.4.1 runtime POST chain — they govern
engineering artifacts (reviewer verdicts, daily logs, lock_history rows) not
grant-draft output. ``pipeline.loop.post_gate_runner`` is therefore NOT
involved here; ``pipeline.engineering.lock_ceremony`` is the parallel
engineering-artifact path.

E-017 injected-seam pattern: production callers wire stdlib clock + a
filesystem reader for ``daily_logs/<today>.md`` + an atomic JSONL appender
via ``production_wiring()``. Tests inject deterministic stubs.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_v2_2_consolidated_amendment.md``
(v2.2 LOCKED 2026-04-21).
"""

from __future__ import annotations

import datetime as _dt
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Optional

from pipeline.harness.gates import (
    AppendLockHistoryResult,
    GateDenied,
    LockHistoryAppendCallable,
    RecordVerdictResult,
    append_lock_history,
    record_verdict,
)
from pipeline.logician.gates import (
    ClockProtocol,
    DailyLogReaderCallable,
    DraftReaderCallable,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_04_v2_2_consolidated_amendment.md": {
        "version": "v2.2",
        "hash_sha3_512_prefix16": "b643d0540a509715",
        "sections_implemented": (
            "F-AMDT-02 (verdict blocking key) — wrapped via record_verdict",
            "F-AMDT-03 (verdict dimensions cite draft evidence) — wrapped via record_verdict",
            "F-AMDT-12 (daily-log LOCK block present for today) — wrapped via append_lock_history",
        ),
    },
}


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class LockCeremonyResult:
    """Outcome of a PASS LOCK ceremony.

    ``record_verdict_result`` is None when no committee verdict accompanied
    the LOCK (self-LOCKs, narrow-fix backfills). ``append_lock_history_result``
    is always populated on success. On any v2.2 gate DENY, the function
    raises :class:`pipeline.harness.gates.GateDenied`; callers never receive
    a partial :class:`LockCeremonyResult`.
    """

    record_verdict_result: Optional[RecordVerdictResult]
    append_lock_history_result: AppendLockHistoryResult


# ---------------------------------------------------------------------------
# Public ceremony function
# ---------------------------------------------------------------------------


def lock(
    *,
    row: dict,
    lock_history_path: str,
    clock: ClockProtocol,
    daily_log_reader: DailyLogReaderCallable,
    append_callable: LockHistoryAppendCallable,
    verdict_json: object | None = None,
    draft_path: str | None = None,
    draft_reader: DraftReaderCallable | None = None,
) -> LockCeremonyResult:
    """Canonical LOCK-append ceremony.

    Sequence:

    1. If ``verdict_json`` is supplied, run :func:`record_verdict` first
       (F-AMDT-02 + optional F-AMDT-03 when both ``draft_path`` and
       ``draft_reader`` are provided). On DENY: raise :class:`GateDenied`
       and skip the append. This ordering is intentional — appending a
       LOCK row when its committee verdict failed gate hygiene would
       cement an unattested LOCK in lock_history.
    2. Run :func:`append_lock_history` (F-AMDT-12 + canonical JSONL append).
       On DENY: raise :class:`GateDenied`. The append callable is invoked
       only after F-AMDT-12 PASS.

    Args:
        row: staged LOCK row (dict; must carry ``module``).
        lock_history_path: absolute path to ``lock_history.v1.jsonl``.
        clock: injected clock — F-AMDT-12 derives today's ISO date.
        daily_log_reader: injected reader for ``daily_logs/<today>.md``.
        append_callable: injected JSONL appender.
        verdict_json: optional committee verdict to ingest first.
        draft_path: optional draft path (Judge verdicts). Requires
            ``draft_reader`` to also be supplied AND ``verdict_json`` to be
            supplied — asymmetric supply is a programmer error.
        draft_reader: optional draft reader. Same constraints as
            ``draft_path``.

    Returns:
        :class:`LockCeremonyResult` on PASS.

    Raises:
        GateDenied: F-AMDT-02 / F-AMDT-03 / F-AMDT-12 DENY.
        ValueError: ``draft_path`` / ``draft_reader`` supplied without
            ``verdict_json``, or supplied asymmetrically.
    """
    # Asymmetry guards — programmer-error class, raised before any I/O.
    draft_args_supplied = draft_path is not None or draft_reader is not None
    if draft_args_supplied and verdict_json is None:
        raise ValueError(
            "draft_path / draft_reader supplied without verdict_json — "
            "F-AMDT-03 only fires alongside a verdict ingest"
        )
    # record_verdict itself enforces the both-or-neither symmetry between
    # draft_path and draft_reader; we let it raise.

    record_result: Optional[RecordVerdictResult] = None
    if verdict_json is not None:
        record_result = record_verdict(
            verdict_json=verdict_json,
            draft_path=draft_path,
            draft_reader=draft_reader,
        )

    append_result = append_lock_history(
        row=row,
        lock_history_path=lock_history_path,
        clock=clock,
        daily_log_reader=daily_log_reader,
        append_callable=append_callable,
    )
    return LockCeremonyResult(
        record_verdict_result=record_result,
        append_lock_history_result=append_result,
    )


# ---------------------------------------------------------------------------
# Production wiring helpers
# ---------------------------------------------------------------------------


class _SystemClock:
    """Production ClockProtocol — wraps ``datetime.datetime.now(tz=UTC)``."""

    def now_utc(self) -> _dt.datetime:
        return _dt.datetime.now(tz=_dt.timezone.utc)

    def now_ms(self) -> int:  # pragma: no cover — present for ClockProtocol breadth
        # Some callers expect ms granularity. Implementation provided for
        # Protocol completeness even though F-AMDT-12 only consults now_utc().
        return int(self.now_utc().timestamp() * 1000)


def make_daily_log_reader(daily_logs_dir: str) -> DailyLogReaderCallable:
    """Production daily-log reader.

    Returns a callable that reads ``<daily_logs_dir>/<today_iso>.md`` (UTF-8).
    The file MUST exist — F-AMDT-12 requires the daily log for today's date
    to be present. Missing file raises ``FileNotFoundError`` which
    F-AMDT-12 surfaces as ``F-AMDT-12-READER-FAIL`` per gate contract.
    """

    base = Path(daily_logs_dir)

    def _read(today_iso: str) -> str:
        path = base / f"{today_iso}.md"
        return path.read_text(encoding="utf-8")

    return _read


def make_atomic_jsonl_append() -> LockHistoryAppendCallable:
    """Production JSONL appender.

    POSIX guarantees append-mode writes ≤ ``PIPE_BUF`` (typically 4096 bytes)
    are atomic with respect to other appenders. A single lock_history row
    is well under that ceiling. The path's parent directory MUST exist;
    creation here would mask a configuration error.
    """

    def _append(*, path: str, jsonl_line: str) -> None:
        if not jsonl_line.endswith("\n"):
            # F-AMDT-12 PASS guarantees harness adds the newline; this is a
            # belt-and-suspenders check against future drift. (Defensive;
            # no test exercises this branch — guarded against contract
            # regression, not user input.)
            jsonl_line = jsonl_line + "\n"  # pragma: no cover
        if len(jsonl_line.encode("utf-8")) > 4096:  # pragma: no cover
            # Lock_history rows are not expected to exceed PIPE_BUF.
            # If a future row format does, atomic append no longer holds
            # under concurrent writers — fail loud.
            raise RuntimeError(
                f"lock_history row exceeds PIPE_BUF (4096 bytes); "
                f"observed {len(jsonl_line.encode('utf-8'))} bytes — atomic "
                f"append guarantee no longer holds"
            )
        # O_APPEND | O_WRONLY | O_CREAT — atomic-append on POSIX.
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
        try:
            os.write(fd, jsonl_line.encode("utf-8"))
        finally:
            os.close(fd)

    return _append


def production_wiring(
    *,
    repo_root: str | Path,
) -> tuple[ClockProtocol, DailyLogReaderCallable, LockHistoryAppendCallable, str]:
    """Bundle production seams for a typical workspace layout.

    Returns ``(clock, daily_log_reader, append_callable, lock_history_path)``
    keyed off the standard repo layout:

    - ``<repo_root>/daily_logs/<today>.md``
    - ``<repo_root>/pipeline/engineering/lock_history.v1.jsonl``

    Use this when running the ceremony from a script. Tests should NOT
    use this — they inject their own seams.
    """
    root = Path(repo_root)
    daily_logs_dir = root / "daily_logs"
    lock_history_path = root / "pipeline" / "engineering" / "lock_history.v1.jsonl"
    return (
        _SystemClock(),
        make_daily_log_reader(str(daily_logs_dir)),
        make_atomic_jsonl_append(),
        str(lock_history_path),
    )


__all__ = [
    "BLUEPRINT_DEPS",
    "LockCeremonyResult",
    "lock",
    "make_atomic_jsonl_append",
    "make_daily_log_reader",
    "production_wiring",
]
