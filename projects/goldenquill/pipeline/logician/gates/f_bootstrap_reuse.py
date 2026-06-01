"""F-BOOTSTRAP-REUSE (F-AMDT-01) — POST-gate on ``lock_history.v1.jsonl`` append.

The TSIP v0.1 bootstrap exception is a one-time mechanism that authorises the
very first LOCK-sealed write of the workspace to bypass the normal amendment
discipline. Once consumed, the exception is spent — any subsequent row that
reuses it is either careless duplication or a deliberate attempt to framea
late amendment as a "bootstrap" event and launder through the discipline.

The gate is a strict counter: after the staged row is placed in the reader's
output, the gate counts rows where ``bootstrap_exception is True`` (strict
``bool`` identity — not truthy) and DENIES the write if the count exceeds
one. Reader failures are DENY-by-default; the gate refuses to conflate "no
history" with "cannot read history".

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(parent LOCK); v2.2 wave-2 delta row for F-AMDT-01.

Semantics (spec card v1, 2026-04-20):
  * Strict ``is True`` counting — ``1``, ``"true"``, ``"True"`` do NOT count.
  * Reader exception → fail-closed DENY with ``reason_tag='reader_raised'``.
  * Reader returns non-list → fail-closed DENY with ``reason_tag='reader_contract_violation'``.
  * Count ≤ 1 → PASS (zero or single legitimate bootstrap).
  * Count > 1 → DENY with ``reason_tag='bootstrap_reuse_detected'`` and the
    full list of indices where ``bootstrap_exception is True``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pipeline.logician.gates._protocols import LockHistoryReaderCallable


F_AMDT_01: str = "F-AMDT-01"


_REASON_REUSE_DETECTED: str = "bootstrap_reuse_detected"
_REASON_READER_RAISED: str = "reader_raised"
_REASON_READER_CONTRACT: str = "reader_contract_violation"


@dataclass(frozen=True, kw_only=True)
class BootstrapReuseDetail:
    reason_tag: str
    bootstrap_count: int
    offending_indices: tuple[int, ...]
    reader_error: Optional[str]


@dataclass(frozen=True, kw_only=True)
class BootstrapReuseResult:
    success: bool
    failure_code: Optional[str]
    detail: Optional[BootstrapReuseDetail]


def _fail(
    *,
    reason_tag: str,
    bootstrap_count: int = 0,
    offending_indices: tuple[int, ...] = (),
    reader_error: Optional[str] = None,
) -> BootstrapReuseResult:
    return BootstrapReuseResult(
        success=False,
        failure_code=F_AMDT_01,
        detail=BootstrapReuseDetail(
            reason_tag=reason_tag,
            bootstrap_count=bootstrap_count,
            offending_indices=offending_indices,
            reader_error=reader_error,
        ),
    )


def check_bootstrap_reuse(
    *, lock_history_reader: LockHistoryReaderCallable
) -> BootstrapReuseResult:
    """POST-gate F-BOOTSTRAP-REUSE (F-AMDT-01).

    Counts rows in ``lock_history.v1.jsonl`` (as returned by the injected
    reader) whose ``bootstrap_exception`` field is strictly the Python
    ``True`` singleton. Returns PASS iff the count is 0 or 1.

    Args:
      lock_history_reader: callable matching
        :class:`LockHistoryReaderCallable`. Must return a ``list[dict]`` of
        all rows (including the staged row about to be committed).

    Returns:
      :class:`BootstrapReuseResult` — ``success=True`` iff ≤1 bootstrap row
      is present. Otherwise ``success=False`` with ``failure_code='F-AMDT-01'``
      and a populated detail.
    """
    try:
        rows = lock_history_reader()
    except Exception as exc:  # fail-closed per spec
        return _fail(
            reason_tag=_REASON_READER_RAISED,
            reader_error=f"{type(exc).__name__}: {exc}"[:500],
        )

    if not isinstance(rows, list):
        return _fail(
            reason_tag=_REASON_READER_CONTRACT,
            reader_error=f"reader returned {type(rows).__name__}, expected list",
        )

    offending: list[int] = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            return _fail(
                reason_tag=_REASON_READER_CONTRACT,
                reader_error=f"row {i} is {type(row).__name__}, expected dict",
            )
        if row.get("bootstrap_exception") is True:
            offending.append(i)

    if len(offending) > 1:
        return _fail(
            reason_tag=_REASON_REUSE_DETECTED,
            bootstrap_count=len(offending),
            offending_indices=tuple(offending),
        )

    return BootstrapReuseResult(success=True, failure_code=None, detail=None)
