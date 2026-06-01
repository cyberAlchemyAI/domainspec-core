"""pipeline.harness.gates — canonical call sites for v2.2 engineering-artifact gates.

The v2.2 amendment-enforcement gates F-AMDT-02 (verdict blocking key),
F-AMDT-03 (verdict dimensions cite draft evidence), and F-AMDT-12 (daily-log
LOCK block present for today) are pure predicates living in
``pipeline.logician.gates``. They do not fit the §4.4.1 13-step POST-gate
sequence — they validate *engineering artifacts* (reviewer verdicts, daily
logs) not grant-draft outputs — so they are not called from
``pipeline.loop.post_gate_runner``. This module exposes the two helpers that
wrap them at their canonical call boundaries:

``record_verdict``
    Invoked by committee-dispatch scripts when a reviewer verdict JSON is
    ingested into ``pipeline/validation/code_reviews/<round>/r_<seat>.raw.json``.
    Runs F-AMDT-02 on every verdict. When a ``draft_path`` + ``draft_reader``
    pair is supplied (Judge verdicts), additionally runs F-AMDT-03. Raises
    :class:`GateDenied` on FAIL.

``append_lock_history``
    Invoked by every LOCK ceremony BEFORE appending to
    ``pipeline/engineering/lock_history.v1.jsonl``. Runs F-AMDT-12 on the
    staged row. On PASS, dispatches the append via an injected callable.
    Raises :class:`GateDenied` on FAIL.

Both helpers are pure composition over the v2.2 gate predicates; neither
performs policy I/O directly. I/O is routed through injected Protocols per
the E-017 injected-callable pattern so test doubles pass through
``isinstance()`` at the call layer.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_v2_2_consolidated_amendment.md``
(v2.2 LOCKED 2026-04-21, sha3_512[:16] ``b643d0540a509715``).

Spec card: derived inline — Task 1 of the MVP-runnable closeout round.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional, Protocol, runtime_checkable

from pipeline.logician.gates import (
    BlockingMissingResult,
    CitationMissingResult,
    ClockProtocol,
    DailyLogBlockResult,
    DailyLogReaderCallable,
    DraftReaderCallable,
    check_daily_log_lock_block,
    check_verdict_blocking,
    check_verdict_citations,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_04_v2_2_consolidated_amendment.md": {
        "version": "v2.2 LOCKED 2026-04-21",
        "hash_sha3_512_prefix16": "b643d0540a509715",
        "gates_wired": (
            "F-AMDT-02 (verdict blocking key + bool)",
            "F-AMDT-03 (verdict dimensions cite draft evidence)",
            "F-AMDT-12 (daily-log LOCK block present for today)",
        ),
    },
}


# ---------------------------------------------------------------------------
# GateDenied exception
# ---------------------------------------------------------------------------


class GateDenied(RuntimeError):
    """Raised by harness helpers when an underlying v2.2 gate DENIES.

    ``code`` carries the top-level failure code (``F-AMDT-02`` / ``F-AMDT-03``
    / ``F-AMDT-12`` or a sub-code such as ``F-AMDT-12-MISSING``).
    ``gate_result`` carries the full underlying gate result dataclass for
    telemetry / operator surfacing. ``summary`` is a human-readable one-line
    description suitable for log messages; the full detail lives on
    ``gate_result.detail``.
    """

    def __init__(
        self, *, code: str, gate_result: object, summary: str
    ) -> None:
        super().__init__(f"{code}: {summary}")
        self.code: str = code
        self.gate_result: object = gate_result
        self.summary: str = summary


# ---------------------------------------------------------------------------
# LockHistoryAppendCallable Protocol (E-017 injected-callable pattern)
# ---------------------------------------------------------------------------


@runtime_checkable
class LockHistoryAppendCallable(Protocol):
    """Appends one JSONL row to the lock_history file.

    Production callers wrap ``open(path, "a", encoding="utf-8")`` — POSIX
    guarantees append atomicity for writes ≤ ``PIPE_BUF`` bytes (typically
    4096), and a single lock_history row is well under that ceiling. Tests
    substitute an in-memory capture that records the ``(path, jsonl_line)``
    tuple for later assertion.

    The callable is invoked exactly once per successful F-AMDT-12 PASS.
    Exceptions propagate unwrapped — the LOCK ceremony treats append
    failure as its own fault category, not a gate denial.
    """

    def __call__(self, *, path: str, jsonl_line: str) -> None: ...


# ---------------------------------------------------------------------------
# record_verdict — wraps F-AMDT-02 + F-AMDT-03
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class RecordVerdictResult:
    """Outcome of a PASS ``record_verdict`` call.

    Carries the verdict dict reference back to the caller unchanged (so
    downstream can consume without re-parsing) plus the extracted
    ``blocking`` flag and whether F-AMDT-03 was exercised. On FAIL,
    :func:`record_verdict` raises :class:`GateDenied` — callers never
    receive a FAIL ``RecordVerdictResult``.
    """

    verdict_json: Mapping[str, Any]
    blocking: bool
    citation_check_performed: bool


def record_verdict(
    *,
    verdict_json: object,
    draft_path: Optional[str] = None,
    draft_reader: Optional[DraftReaderCallable] = None,
) -> RecordVerdictResult:
    """Canonical verdict-ingest gate for the harness.

    F-AMDT-02 runs on every verdict. F-AMDT-03 runs only when *both*
    ``draft_path`` and ``draft_reader`` are supplied — Judge verdicts carry
    an evidence-citation obligation; Editor / Red Team verdicts do not.

    Args:
      verdict_json: parsed reviewer verdict (any object; F-AMDT-02
        validates structure).
      draft_path: path to the draft under review (Judge verdicts only).
      draft_reader: injected reader that returns the draft text (Judge
        verdicts only).

    Returns:
      :class:`RecordVerdictResult` on PASS.

    Raises:
      GateDenied: F-AMDT-02 or F-AMDT-03 DENIES. ``code`` carries the
        originating failure code.
      ValueError: ``draft_path`` and ``draft_reader`` are not both-supplied
        or both-None (asymmetric caller contract is a programmer error).
    """
    if (draft_path is None) != (draft_reader is None):
        raise ValueError(
            "draft_path and draft_reader must both be supplied or both be None"
        )

    blocking_result = check_verdict_blocking(verdict_json)
    if not blocking_result.success:
        raise GateDenied(
            code=blocking_result.failure_code or "F-AMDT-02",
            gate_result=blocking_result,
            summary=_summarize_blocking(blocking_result),
        )

    # F-AMDT-02 PASS guarantees verdict_json is a dict with bool "blocking".
    if not isinstance(verdict_json, dict):  # pragma: no cover — F-AMDT-02 invariant
        raise AssertionError(
            "invariant broken: F-AMDT-02 PASS on non-dict verdict"
        )

    citation_check_performed = False
    if draft_path is not None and draft_reader is not None:
        citation_result = check_verdict_citations(
            verdict_json=verdict_json,
            draft_path=draft_path,
            draft_reader=draft_reader,
        )
        citation_check_performed = True
        if not citation_result.success:
            raise GateDenied(
                code=citation_result.failure_code or "F-AMDT-03",
                gate_result=citation_result,
                summary=_summarize_citation(citation_result),
            )

    blocking_value = verdict_json["blocking"]
    if not isinstance(blocking_value, bool):  # pragma: no cover — F-AMDT-02 invariant
        raise AssertionError(
            "invariant broken: F-AMDT-02 PASS with non-bool blocking"
        )
    return RecordVerdictResult(
        verdict_json=verdict_json,
        blocking=blocking_value,
        citation_check_performed=citation_check_performed,
    )


def _summarize_blocking(r: BlockingMissingResult) -> str:
    if r.detail is None:  # pragma: no cover — gate always populates detail on FAIL
        return "F-AMDT-02 DENIED (no detail)"
    return (
        f"verdict blocking-key check failed: {r.detail.reason_tag} "
        f"(observed type={r.detail.observed_type})"
    )


def _summarize_citation(r: CitationMissingResult) -> str:
    if r.detail is None:  # pragma: no cover — gate always populates detail on FAIL
        return "F-AMDT-03 DENIED (no detail)"
    if r.detail.reason_tag == "draft_reader_raised":
        return f"draft reader raised: {r.detail.reader_error}"
    if r.detail.failed_dimensions:
        n = len(r.detail.failed_dimensions)
        return f"{n} dimension(s) failed citation check: {r.detail.reason_tag}"
    return f"citation check failed: {r.detail.reason_tag}"


# ---------------------------------------------------------------------------
# append_lock_history — wraps F-AMDT-12
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class AppendLockHistoryResult:
    """Outcome of a PASS ``append_lock_history`` call.

    Carries the LOCKed module name + today's ISO date (``None`` when the
    backfill carve-out was applied, since F-AMDT-12 skipped the daily-log
    inspection in that branch) + whether the carve-out fired. On FAIL,
    :func:`append_lock_history` raises :class:`GateDenied`. If the append
    callable raises, that exception propagates unwrapped — append failure
    is the LOCK ceremony's own fault category, not a gate denial.
    """

    module: str
    today_iso: Optional[str]
    backfill_carveout_applied: bool


def append_lock_history(
    *,
    row: dict,
    lock_history_path: str,
    clock: ClockProtocol,
    daily_log_reader: DailyLogReaderCallable,
    append_callable: LockHistoryAppendCallable,
) -> AppendLockHistoryResult:
    """Canonical LOCK-append gate for the harness.

    Invoked BEFORE every append to ``pipeline/engineering/lock_history.v1.jsonl``.
    Runs F-AMDT-12 on the staged row (checks that today's daily log has a
    canonical ``## LOCK: {module}`` block with all seven required
    non-empty fields, or that the row is a legitimate backfill carve-out).
    On PASS, dispatches the append via the injected callable, serialising
    the row with ``json.dumps(sort_keys=True, separators=(",", ":"))`` to
    match the lock_history canonicalisation convention.

    Args:
      row: staged lock_history row (dict; must carry ``module``).
      lock_history_path: absolute path to ``lock_history.v1.jsonl``.
      clock: injected clock. Gate uses ``clock.now_utc()`` to derive today's
        ISO date for daily-log lookup.
      daily_log_reader: injected reader. Gate calls
        ``daily_log_reader(today_iso)`` to fetch today's daily log text.
      append_callable: injected callable that performs the actual append.

    Returns:
      :class:`AppendLockHistoryResult` on PASS.

    Raises:
      GateDenied: F-AMDT-12 DENIES. ``code`` carries the originating failure
        code (``F-AMDT-12`` / ``F-AMDT-12-MISSING`` / ``F-AMDT-12-MALFORMED``
        / ``F-AMDT-12-READER-FAIL``).
    """
    gate_result = check_daily_log_lock_block(
        staged_row=row,
        clock=clock,
        daily_log_reader=daily_log_reader,
    )
    if not gate_result.success:
        raise GateDenied(
            code=gate_result.failure_code or "F-AMDT-12",
            gate_result=gate_result,
            summary=_summarize_daily_log_block(gate_result),
        )

    jsonl_line = json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
    append_callable(path=lock_history_path, jsonl_line=jsonl_line)

    # F-AMDT-12 PASS guarantees row has non-empty string "module".
    module = row.get("module")
    if not isinstance(module, str) or module == "":  # pragma: no cover — F-AMDT-12 invariant
        raise AssertionError(
            "invariant broken: F-AMDT-12 PASS with missing module"
        )

    backfill = (
        row.get("backfilled") is True
        and row.get("verdict") == "LOCKED-backfilled"
    )
    today_iso: Optional[str] = None
    if not backfill:
        today_iso = clock.now_utc().date().isoformat()

    return AppendLockHistoryResult(
        module=module,
        today_iso=today_iso,
        backfill_carveout_applied=backfill,
    )


def _summarize_daily_log_block(r: DailyLogBlockResult) -> str:
    if r.detail is None:  # pragma: no cover — gate always populates detail on FAIL
        return "F-AMDT-12 DENIED (no detail)"
    d = r.detail
    if d.reason_tag == "lock_block_required_fields_missing":
        missing = ", ".join(d.missing_fields)
        return (
            f"LOCK block malformed for module={d.staged_module!r} "
            f"on daily log {d.today_iso}: missing fields [{missing}]"
        )
    if d.reason_tag == "lock_block_heading_not_found":
        return (
            f"no '## LOCK: {d.staged_module}' heading in daily log for {d.today_iso}"
        )
    if d.reason_tag == "daily_log_absent_for_today":
        return f"daily log for {d.today_iso} does not exist"
    if d.reason_tag == "staged_row_module_missing":
        return "staged lock_history row has no 'module' field"
    if d.reason_tag == "clock_raised":
        return f"clock raised: {d.reader_error}"
    if d.reason_tag == "daily_log_reader_raised":
        return f"daily log reader raised: {d.reader_error}"
    return f"F-AMDT-12 DENIED: {d.reason_tag}"  # pragma: no cover — exhaustive


__all__ = [
    "AppendLockHistoryResult",
    "BLUEPRINT_DEPS",
    "GateDenied",
    "LockHistoryAppendCallable",
    "RecordVerdictResult",
    "append_lock_history",
    "record_verdict",
]
