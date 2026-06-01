"""Constant-time benchmark cross-check + audit-log (architecture v7.0.4-M1 §5).

DC-CF-04 closure: replace short-circuit ``==`` on cross-check value
hashes with :func:`hmac.compare_digest`.  Combined with mandatory
audit-log discipline (write-before-compare + dummy-pad + fsync) the
gate eliminates the boolean-oracle path the cross-family verification
surfaced.

Audit-log row shape per §5.2.2 (fixed-width result placeholders so
both branches execute identical I/O):

```
{"ledger_kind": "benchmark_cross_check",
 "result": "PENDING_____",
 "benchmark_id": "...",
 "target_org_kfr_namespace": "orgs/<slug>/vault/kfr/",
 "operator_key_id": "...",
 "checked_at_utc": "2026-05-10T...",
 "caller_seat": "scout"}
{"ledger_kind": "benchmark_cross_check_result",
 "placeholder_id": "...",
 "result": "matched_____" | "not_matched_"}
```

The fixed-width result token (``matched_____`` / ``not_matched_``)
keeps the second-row payload identical in length for both branches —
the audit-log writer cannot leak the boolean outcome via byte count.
"""

from __future__ import annotations

import hmac
import json
import os
import secrets
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Final, Optional


AUDIT_LOG_LEDGER_KIND: Final[str] = "benchmark_cross_check"
AUDIT_LOG_LEDGER_KIND_RESULT: Final[str] = "benchmark_cross_check_result"

# Fixed-width result tokens — both branches must serialize to the
# exact same byte count to keep the audit-log row size identical.
AUDIT_LOG_RESULT_PENDING: Final[str] = "PENDING_____"
AUDIT_LOG_RESULT_MATCHED: Final[str] = "matched_____"
AUDIT_LOG_RESULT_NOT_MATCHED: Final[str] = "not_matched_"

# Sanity: the three result tokens are the same length (so the JSON
# row is the same byte count regardless of branch).
assert (
    len(AUDIT_LOG_RESULT_PENDING)
    == len(AUDIT_LOG_RESULT_MATCHED)
    == len(AUDIT_LOG_RESULT_NOT_MATCHED)
)


@dataclass(frozen=True, kw_only=True)
class CrossCheckRecord:
    """One audit-log entry pair (placeholder + result row)."""

    placeholder_id: str
    benchmark_id: str
    target_org_kfr_namespace: str
    operator_key_id: str
    checked_at_utc: str
    caller_seat: str
    matched: bool


# AuditLogWriter accepts a JSONL row (one record) and persists it
# durably (write + fsync).  Production injection wraps an open file
# descriptor; tests inject an in-memory list.
AuditLogWriter = Callable[[dict], None]


def _default_audit_log_writer(audit_log_path: Path) -> AuditLogWriter:
    """Return a writer that appends + fsyncs ``audit_log_path``.

    The writer opens the file in append mode, flushes, and ``os.fsync``s
    on every row to make the audit-log entry durable before
    :func:`hmac.compare_digest` runs (write-before-compare per §5.2.2).
    """

    def _writer(row: dict) -> None:
        # Encode through canonical-JSON-style sorted keys so the audit
        # log is reproducible across operators / runs.
        line = json.dumps(row, sort_keys=True, separators=(", ", ": "))
        with open(audit_log_path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
            fh.flush()
            os.fsync(fh.fileno())

    return _writer


def value_hash_match(benchmark_hash: bytes, kfr_hash: bytes) -> bool:
    """Constant-time hash compare via :func:`hmac.compare_digest`.

    Raw helper used by callers that have already produced the audit
    log entry separately.  Most callers should use
    :func:`cross_check_with_audit` to get audit + compare in one call.
    """
    if not isinstance(benchmark_hash, (bytes, bytearray)):
        raise TypeError(
            f"benchmark_hash must be bytes, got {type(benchmark_hash).__name__}"
        )
    if not isinstance(kfr_hash, (bytes, bytearray)):
        raise TypeError(
            f"kfr_hash must be bytes, got {type(kfr_hash).__name__}"
        )
    return hmac.compare_digest(bytes(benchmark_hash), bytes(kfr_hash))


def cross_check_with_audit(
    *,
    benchmark_hash: bytes,
    kfr_hash: bytes,
    benchmark_id: str,
    target_org_kfr_namespace: str,
    operator_key_id: str,
    caller_seat: str,
    audit_log_writer: Optional[AuditLogWriter] = None,
    audit_log_path: Optional[Path] = None,
    clock_now: Optional[Callable[[], str]] = None,
) -> CrossCheckRecord:
    """Constant-time cross-check with timing-equalized audit-log write.

    Discipline per §5.2.2:

    1. Write audit-log placeholder row first (fixed-size payload).
    2. ``fsync`` (durably commits the probe attempt).
    3. Run :func:`hmac.compare_digest`.
    4. Write the result row (fixed-size payload — token width identical
       across branches).
    5. ``fsync`` again.

    Both branches execute identical syscalls; the audit-log writer
    cannot leak the boolean outcome via timing.

    Parameters
    ----------
    audit_log_writer
        Injected writer.  When None, ``audit_log_path`` is required and
        :func:`_default_audit_log_writer` is bound.
    audit_log_path
        Used when ``audit_log_writer`` is None — the writer appends to
        this path under JSONL semantics.
    clock_now
        Optional UTC-iso8601 string source.  When None, :func:`time.gmtime`
        + :func:`time.strftime` produce a deterministic-shape string.
    """
    if audit_log_writer is None:
        if audit_log_path is None:
            raise ValueError(
                "cross_check_with_audit requires either audit_log_writer "
                "or audit_log_path"
            )
        audit_log_writer = _default_audit_log_writer(audit_log_path)

    if clock_now is None:
        def _utc_now() -> str:
            return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        clock_now = _utc_now

    placeholder_id = secrets.token_hex(16)
    checked_at_utc = clock_now()

    placeholder_row = {
        "ledger_kind": AUDIT_LOG_LEDGER_KIND,
        "placeholder_id": placeholder_id,
        "result": AUDIT_LOG_RESULT_PENDING,
        "benchmark_id": benchmark_id,
        "target_org_kfr_namespace": target_org_kfr_namespace,
        "operator_key_id": operator_key_id,
        "checked_at_utc": checked_at_utc,
        "caller_seat": caller_seat,
    }
    audit_log_writer(placeholder_row)

    # Constant-time comparison.
    matched = value_hash_match(benchmark_hash, kfr_hash)

    result_token = (
        AUDIT_LOG_RESULT_MATCHED if matched else AUDIT_LOG_RESULT_NOT_MATCHED
    )
    result_row = {
        "ledger_kind": AUDIT_LOG_LEDGER_KIND_RESULT,
        "placeholder_id": placeholder_id,
        "result": result_token,
    }
    audit_log_writer(result_row)

    return CrossCheckRecord(
        placeholder_id=placeholder_id,
        benchmark_id=benchmark_id,
        target_org_kfr_namespace=target_org_kfr_namespace,
        operator_key_id=operator_key_id,
        checked_at_utc=checked_at_utc,
        caller_seat=caller_seat,
        matched=matched,
    )


__all__ = [
    "AUDIT_LOG_LEDGER_KIND",
    "AUDIT_LOG_LEDGER_KIND_RESULT",
    "AUDIT_LOG_RESULT_MATCHED",
    "AUDIT_LOG_RESULT_NOT_MATCHED",
    "AUDIT_LOG_RESULT_PENDING",
    "AuditLogWriter",
    "CrossCheckRecord",
    "cross_check_with_audit",
    "value_hash_match",
]
