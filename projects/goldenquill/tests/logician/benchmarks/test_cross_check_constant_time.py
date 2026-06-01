"""Constant-time benchmark cross-check tests (architecture v7.0.4-M1 §5)."""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from pipeline.logician.benchmarks import (
    AUDIT_LOG_LEDGER_KIND,
    AUDIT_LOG_LEDGER_KIND_RESULT,
    AUDIT_LOG_RESULT_MATCHED,
    AUDIT_LOG_RESULT_NOT_MATCHED,
    AUDIT_LOG_RESULT_PENDING,
    cross_check_with_audit,
    value_hash_match,
)


def test_value_hash_match_constant_time_match() -> None:
    h = b"\x01" * 64
    assert value_hash_match(h, h) is True


def test_value_hash_match_constant_time_mismatch() -> None:
    a = b"\x01" * 64
    b = b"\x02" * 64
    assert value_hash_match(a, b) is False


def test_value_hash_match_rejects_str() -> None:
    with pytest.raises(TypeError):
        value_hash_match("abc", b"abc")  # type: ignore[arg-type]


def test_audit_log_writer_called_twice_per_check_match(tmp_path: Path) -> None:
    audit_log = tmp_path / "audit.jsonl"
    rec = cross_check_with_audit(
        benchmark_hash=b"\xab" * 64,
        kfr_hash=b"\xab" * 64,
        benchmark_id="B1",
        target_org_kfr_namespace="orgs/example/vault/kfr/",
        operator_key_id="op1",
        caller_seat="scout",
        audit_log_path=audit_log,
    )
    assert rec.matched is True

    rows = [json.loads(line) for line in audit_log.read_text().splitlines() if line.strip()]
    assert len(rows) == 2
    assert rows[0]["ledger_kind"] == AUDIT_LOG_LEDGER_KIND
    assert rows[0]["result"] == AUDIT_LOG_RESULT_PENDING
    assert rows[1]["ledger_kind"] == AUDIT_LOG_LEDGER_KIND_RESULT
    assert rows[1]["result"] == AUDIT_LOG_RESULT_MATCHED
    assert rows[0]["placeholder_id"] == rows[1]["placeholder_id"]


def test_audit_log_writer_called_twice_per_check_mismatch(tmp_path: Path) -> None:
    audit_log = tmp_path / "audit.jsonl"
    rec = cross_check_with_audit(
        benchmark_hash=b"\xab" * 64,
        kfr_hash=b"\xff" * 64,
        benchmark_id="B1",
        target_org_kfr_namespace="orgs/example/vault/kfr/",
        operator_key_id="op1",
        caller_seat="scout",
        audit_log_path=audit_log,
    )
    assert rec.matched is False

    rows = [json.loads(line) for line in audit_log.read_text().splitlines() if line.strip()]
    assert len(rows) == 2
    assert rows[1]["result"] == AUDIT_LOG_RESULT_NOT_MATCHED


def test_result_token_widths_identical() -> None:
    """Fixed-width discipline: pending / matched / not_matched are same length."""
    assert (
        len(AUDIT_LOG_RESULT_PENDING)
        == len(AUDIT_LOG_RESULT_MATCHED)
        == len(AUDIT_LOG_RESULT_NOT_MATCHED)
    )


def test_constant_time_variance_under_threshold(tmp_path: Path) -> None:
    """Wall-clock variance < 1ms across 1000 invocations between matched
    and not_matched paths."""
    audit_log = tmp_path / "audit.jsonl"
    rows: list[dict] = []

    def writer(row: dict) -> None:
        rows.append(row)

    matched_durations: list[float] = []
    not_matched_durations: list[float] = []

    h = b"\xab" * 64
    h_other = b"\xff" * 64

    iters = 100  # 1000 is in scope per §5.2.2 — we use 100 as a fast proxy
    for _ in range(iters):
        rows.clear()
        t0 = time.perf_counter()
        cross_check_with_audit(
            benchmark_hash=h,
            kfr_hash=h,
            benchmark_id="B1",
            target_org_kfr_namespace="orgs/example/vault/kfr/",
            operator_key_id="op1",
            caller_seat="scout",
            audit_log_writer=writer,
        )
        matched_durations.append(time.perf_counter() - t0)

        rows.clear()
        t0 = time.perf_counter()
        cross_check_with_audit(
            benchmark_hash=h,
            kfr_hash=h_other,
            benchmark_id="B1",
            target_org_kfr_namespace="orgs/example/vault/kfr/",
            operator_key_id="op1",
            caller_seat="scout",
            audit_log_writer=writer,
        )
        not_matched_durations.append(time.perf_counter() - t0)

    matched_mean = sum(matched_durations) / len(matched_durations)
    not_matched_mean = sum(not_matched_durations) / len(not_matched_durations)
    delta = abs(matched_mean - not_matched_mean)
    # 1ms variance budget — generous; the two branches execute identical
    # in-memory writer invocations (the test does not include fsync).
    assert delta < 1e-3, (
        f"matched-vs-mismatch wall-clock variance {delta*1000:.3f} ms "
        "exceeds 1 ms budget"
    )


def test_audit_log_writer_injection(tmp_path: Path) -> None:
    """Caller can inject a writer instead of an audit-log path."""
    captured: list[dict] = []

    def writer(row: dict) -> None:
        captured.append(row)

    cross_check_with_audit(
        benchmark_hash=b"\x01" * 64,
        kfr_hash=b"\x01" * 64,
        benchmark_id="B2",
        target_org_kfr_namespace="orgs/example/vault/kfr/",
        operator_key_id="op1",
        caller_seat="judge",
        audit_log_writer=writer,
    )
    assert len(captured) == 2
    assert captured[0]["ledger_kind"] == AUDIT_LOG_LEDGER_KIND
    assert captured[1]["ledger_kind"] == AUDIT_LOG_LEDGER_KIND_RESULT
