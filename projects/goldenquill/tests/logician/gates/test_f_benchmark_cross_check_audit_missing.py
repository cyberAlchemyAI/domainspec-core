"""F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING tests (M1 §5.4)."""

from __future__ import annotations

from pipeline.logician.benchmarks.cross_check import (
    AUDIT_LOG_LEDGER_KIND,
    AUDIT_LOG_LEDGER_KIND_RESULT,
    AUDIT_LOG_RESULT_MATCHED,
    AUDIT_LOG_RESULT_NOT_MATCHED,
    AUDIT_LOG_RESULT_PENDING,
)
from pipeline.logician.gates.f_benchmark_cross_check_audit_missing import (
    F_BENCHMARK_CROSS_CHECK_AUDIT_MISSING,
    check_benchmark_cross_check_audit_missing,
)


def _placeholder_row(pid: str = "X") -> dict:
    return {
        "ledger_kind": AUDIT_LOG_LEDGER_KIND,
        "placeholder_id": pid,
        "result": AUDIT_LOG_RESULT_PENDING,
    }


def _result_row(pid: str = "X", result: str = AUDIT_LOG_RESULT_MATCHED) -> dict:
    return {
        "ledger_kind": AUDIT_LOG_LEDGER_KIND_RESULT,
        "placeholder_id": pid,
        "result": result,
    }


def test_failure_code_constant() -> None:
    assert (
        F_BENCHMARK_CROSS_CHECK_AUDIT_MISSING
        == "F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING"
    )


def test_complete_pair_passes() -> None:
    r = check_benchmark_cross_check_audit_missing(
        placeholder_id="X",
        audit_log_rows=[_placeholder_row(), _result_row()],
    )
    assert r.success is True


def test_missing_placeholder_fails() -> None:
    r = check_benchmark_cross_check_audit_missing(
        placeholder_id="X",
        audit_log_rows=[_result_row()],
    )
    assert r.success is False
    assert r.failure_code == F_BENCHMARK_CROSS_CHECK_AUDIT_MISSING


def test_missing_result_fails() -> None:
    r = check_benchmark_cross_check_audit_missing(
        placeholder_id="X",
        audit_log_rows=[_placeholder_row()],
    )
    assert r.success is False
    assert r.failure_code == F_BENCHMARK_CROSS_CHECK_AUDIT_MISSING


def test_pending_result_token_fails() -> None:
    """Result row with pending token = not finalized."""
    r = check_benchmark_cross_check_audit_missing(
        placeholder_id="X",
        audit_log_rows=[
            _placeholder_row(),
            _result_row(result=AUDIT_LOG_RESULT_PENDING),
        ],
    )
    assert r.success is False
    assert r.failure_code == F_BENCHMARK_CROSS_CHECK_AUDIT_MISSING


def test_unrecognized_result_token_fails() -> None:
    r = check_benchmark_cross_check_audit_missing(
        placeholder_id="X",
        audit_log_rows=[
            _placeholder_row(),
            _result_row(result="GARBAGE_____"),
        ],
    )
    assert r.success is False


def test_not_matched_token_passes() -> None:
    r = check_benchmark_cross_check_audit_missing(
        placeholder_id="X",
        audit_log_rows=[
            _placeholder_row(),
            _result_row(result=AUDIT_LOG_RESULT_NOT_MATCHED),
        ],
    )
    assert r.success is True


def test_other_placeholders_ignored() -> None:
    r = check_benchmark_cross_check_audit_missing(
        placeholder_id="X",
        audit_log_rows=[
            _placeholder_row("Y"),
            _result_row("Y"),
            _placeholder_row("X"),
            _result_row("X"),
        ],
    )
    assert r.success is True
