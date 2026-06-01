"""F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING — benchmark POST-check gate (M1 §5.4).

DC-CF-04 leg 2.  Every benchmark cross-check MUST emit two audit-log
rows (placeholder + result, per §5.2.2).  At the next read the gate
verifies the audit trail is intact: missing or unmatched rows fire
fail-closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional, Sequence

from pipeline.logician.benchmarks.cross_check import (
    AUDIT_LOG_LEDGER_KIND,
    AUDIT_LOG_LEDGER_KIND_RESULT,
    AUDIT_LOG_RESULT_MATCHED,
    AUDIT_LOG_RESULT_NOT_MATCHED,
    AUDIT_LOG_RESULT_PENDING,
)


F_BENCHMARK_CROSS_CHECK_AUDIT_MISSING: Final[str] = (
    "F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING"
)


@dataclass(frozen=True, kw_only=True)
class CrossCheckAuditResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    placeholder_id: Optional[str] = None


def check_benchmark_cross_check_audit_missing(
    *,
    placeholder_id: str,
    audit_log_rows: Sequence[Mapping[str, Any]],
) -> CrossCheckAuditResult:
    """POST-check gate: verify the audit-log row pair for ``placeholder_id``.

    The verification is strict — both rows (placeholder + result)
    must exist and the result row must carry one of the canonical
    fixed-width result tokens.
    """
    placeholder_seen = False
    result_seen = False
    result_token: Optional[str] = None
    for row in audit_log_rows:
        if not isinstance(row, Mapping):
            continue
        if row.get("placeholder_id") != placeholder_id:
            continue
        kind = row.get("ledger_kind")
        if kind == AUDIT_LOG_LEDGER_KIND:
            placeholder_seen = True
        elif kind == AUDIT_LOG_LEDGER_KIND_RESULT:
            result_seen = True
            token = row.get("result")
            if isinstance(token, str):
                result_token = token

    if not placeholder_seen:
        return CrossCheckAuditResult(
            success=False,
            failure_code=F_BENCHMARK_CROSS_CHECK_AUDIT_MISSING,
            detail=(
                f"placeholder row missing for placeholder_id="
                f"{placeholder_id!r}; cross-check audit trail broken"
            ),
            placeholder_id=placeholder_id,
        )
    if not result_seen:
        return CrossCheckAuditResult(
            success=False,
            failure_code=F_BENCHMARK_CROSS_CHECK_AUDIT_MISSING,
            detail=(
                f"result row missing for placeholder_id={placeholder_id!r}"
                "; cross-check audit trail broken"
            ),
            placeholder_id=placeholder_id,
        )
    if result_token not in {
        AUDIT_LOG_RESULT_MATCHED,
        AUDIT_LOG_RESULT_NOT_MATCHED,
    }:
        # PENDING token at the result row indicates the comparison
        # never finalized — also treated as audit missing.
        return CrossCheckAuditResult(
            success=False,
            failure_code=F_BENCHMARK_CROSS_CHECK_AUDIT_MISSING,
            detail=(
                f"result row for placeholder_id={placeholder_id!r} carries "
                f"unrecognized result token {result_token!r} (expected "
                f"matched / not_matched, or pending which is treated as "
                f"unfinalized) — found {result_token!r}"
            ),
            placeholder_id=placeholder_id,
        )
    return CrossCheckAuditResult(
        success=True,
        failure_code=None,
        detail=(
            f"audit-log pair present for placeholder_id={placeholder_id!r} "
            f"(result={result_token!r})"
        ),
        placeholder_id=placeholder_id,
    )


__all__ = [
    "AUDIT_LOG_RESULT_PENDING",
    "F_BENCHMARK_CROSS_CHECK_AUDIT_MISSING",
    "CrossCheckAuditResult",
    "check_benchmark_cross_check_audit_missing",
]
