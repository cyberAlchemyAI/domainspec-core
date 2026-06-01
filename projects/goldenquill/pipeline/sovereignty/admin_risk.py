"""Admin-risk ledger — rate-limited RED/YELLOW/GREEN entries + M13 bypass predicate. [§2.5, §3.7, §4.8, §5.3 BT3, §6.5, §7.3]

Section 1 Round F3. Owns:

* :class:`AdminRiskEntry` — §2.5 schema frozen dataclass.
* :func:`record_admin_risk` — rate-limited append under an outer
  ``admin_risk.lock`` (BT3 v2 critical-section discipline). Composes the
  Round B :func:`pipeline.sovereignty.audit.append_to_ledger` primitive
  for the actual HMAC-trailered write.
* :func:`read_ledger_tail` — O(n) tail scan for the last ``n`` entries.
* :func:`bypass_is_active` — M13 predicate with v2 dual-clock gate + v3
  boot-clock-history rollback oracle. Takes a frozen dataclass for the
  degradation event and an iterable of :class:`BootClockRecord`.

Blueprint references:

* §2.5   AdminRiskEntry schema
* §3.7   admin_risk public API
* §4.8   M13 review-seat outage escape-valve recording
* §5.3   BT3 rate limits + v2 lock-first critical section
* §6.5   F-ADM-01..12 failure codes + F-DEG-02/03 bypass failures
* §7.3   unit tests

E-enforcement:

* E-001 arg-type validation before any I/O
* E-005 canonical JSON (sorted keys + ASCII + no whitespace)
* E-014 family exception taxonomy (:class:`AdminRiskError` parent)

v0.1 scope (deferred):

* Boot-time watermark verification — owned by Round I boot.py.
* Full keystore integration — callers pass raw HMAC key bytes; Round I
  wires keystore.retrieve into the record_admin_risk entrypoint.
"""

from __future__ import annotations

import datetime as _dt
import errno
import fcntl
import hashlib
import hmac as _stdlib_hmac
import json
import os
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from pipeline.sovereignty.audit import (
    LedgerChainBroken,
    LedgerUnreadable,
    append_to_ledger,
    canonical_json_bytes,
)

__all__ = [
    "AdminRiskEntry",
    "BootClockRecord",
    "AdminRiskError",
    "RateLimitExceeded",
    "OperatorConfirmationRequired",
    "LedgerMissing",
    "BypassClockRollbackDetected",
    "M13_BYPASS_CEILING_HOURS",
    "CLOCK_ROLLBACK_TOLERANCE_SECONDS",
    "SEVERITY_LIMITS",
    "record_admin_risk",
    "read_ledger_tail",
    "bypass_is_active",
    "admin_risk_entry_from_json",
    "admin_risk_ledger_path",
    "admin_risk_trailer_path",
]

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": [
            "§2.5 AdminRiskEntry",
            "§3.7 admin_risk public API",
            "§4.8 M13 review-seat bypass recording",
            "§5.3 BT3 rate limits + v2 lock-first critical section",
            "§6.5 F-ADM-01..12",
            "§7.3 unit tests",
        ],
        "hash_at_lock": None,
        "hash_source_version": "v6",
    },
}

# --- Constants (§5.3 BT3 + §4.8 M13) ---
SEVERITY_LIMITS: dict[str, int] = {"GREEN": 100, "YELLOW": 50, "RED": 10}
_VALID_SEVERITIES = frozenset(SEVERITY_LIMITS.keys())
# M13 ceiling — v2 enforces against monotonic; default 24 h, operator-override
# to 72 h per §4.8. Section 1 publishes the default; Section 5 chooses per call.
M13_BYPASS_CEILING_HOURS: int = 72
CLOCK_ROLLBACK_TOLERANCE_SECONDS: int = 300  # §4.8 v3 — 5 minutes NTP slop

_ENTRY_KIND_FLAGGED_TERM = "flagged_term_substitution"
_ENTRY_KIND_REVIEW_SEAT_BYPASS = "review_seat_bypass"
_VALID_ENTRY_KINDS = frozenset(
    [_ENTRY_KIND_FLAGGED_TERM, _ENTRY_KIND_REVIEW_SEAT_BYPASS]
)


# ---------------------------------------------------------------------------
# Exceptions (E-014 family taxonomy)
# ---------------------------------------------------------------------------


class AdminRiskError(RuntimeError):
    """Common parent for F-ADM-01..12. Carries a ``code`` attribute."""

    code: str = "F-ADM"


class OperatorConfirmationRequired(AdminRiskError):
    """F-ADM-01. RED severity entry without operator_retype_confirmation."""

    code = "F-ADM-01"


class RateLimitExceeded(AdminRiskError):
    """F-ADM-02. Rate limit hit for the given severity."""

    code = "F-ADM-02"

    def __init__(self, *, severity: str, current: int, limit: int) -> None:
        super().__init__(
            f"F-ADM-02 rate-limit exceeded for severity={severity}: "
            f"{current}/{limit} in current window"
        )
        self.severity = severity
        self.current = current
        self.limit = limit


class LedgerMissing(AdminRiskError):
    """F-ADM-* Ledger file absent when one is expected (boot-time)."""

    code = "F-ADM-03"


class BypassClockRollbackDetected(AdminRiskError):
    """F-ADM-09 / F-DEG-03. Clock rollback or orphan-boot bypass attempt."""

    code = "F-DEG-03"

    def __init__(self, *, reason: str) -> None:
        super().__init__(f"F-DEG-03 {reason}")
        self.reason = reason


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class AdminRiskEntry:
    """§2.5 schema. Frozen.

    ``payload_json`` is canonical JSON (sorted keys, ASCII, no whitespace).
    ``operator_retype_hash`` is HMAC-SHA3-512(operator_key, typed_string),
    hex-encoded. Required for RED; absent for GREEN/YELLOW.
    """

    seq_id: int
    timestamp_utc: str
    issued_monotonic_ns: int
    severity: str
    entry_kind: str
    payload_json: str
    operator_retype_hash: str | None
    prev_hash: str
    entry_hash: str


@dataclass(frozen=True, kw_only=True)
class BootClockRecord:
    """One line of ``boot_clock_history.jsonl``. [§4.8 v3]

    Section 1 publishes the shape so Round I boot.py can materialize the
    on-disk format. F3 consumes only ``boot_epoch_ns`` + ``wall_at_boot_utc``
    in :func:`bypass_is_active`.
    """

    boot_epoch_ns: int
    wall_at_boot_utc: str


# ---------------------------------------------------------------------------
# Path helpers (§2.8)
# ---------------------------------------------------------------------------


def _ledger_dir(repo_root: Path) -> Path:
    return repo_root / "sovereignty" / "ledgers"


def _ledger_path(repo_root: Path) -> Path:
    return _ledger_dir(repo_root) / "admin_risk.jsonl"


def _data_lock_path(repo_root: Path) -> Path:
    """Inner data-level lock used BY :func:`audit.append_to_ledger`."""
    return _ledger_dir(repo_root) / "admin_risk.data.lock"


def _rate_lock_path(repo_root: Path) -> Path:
    """Outer rate-limit lock held across counter-read + append + counter-write.

    Blueprint §2.8 names this ``admin_risk.lock``. The inner data lock
    ``admin_risk.data.lock`` (sibling) is what audit.append_to_ledger
    grabs; this outer lock serializes rate-check + append + counter update
    so the v2 fork-race BT3 HIGH cannot recur.
    """
    return _ledger_dir(repo_root) / "admin_risk.lock"


def _trailer_path(repo_root: Path) -> Path:
    return _ledger_dir(repo_root) / "admin_risk.hmac"


def _counts_path(repo_root: Path, date_str: str) -> Path:
    return _ledger_dir(repo_root) / f"admin_risk.counts.{date_str}.json"


def _watermarks_path(repo_root: Path) -> Path:
    return repo_root / "sovereignty" / "watermarks" / "ledger_watermarks.json"


def _watermarks_hmac_path(repo_root: Path) -> Path:
    return repo_root / "sovereignty" / "watermarks" / "ledger_watermarks.hmac"


def _watermarks_lock_path(repo_root: Path) -> Path:
    return repo_root / "sovereignty" / "watermarks" / "ledger_watermarks.lock"


# ---------------------------------------------------------------------------
# Lock discipline
# ---------------------------------------------------------------------------


@contextmanager
def _rate_lock(repo_root: Path) -> Iterator[None]:
    """fcntl.LOCK_EX on the outer rate-limit lock. [§5.3 v2]"""
    path = _rate_lock_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(path), os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


# ---------------------------------------------------------------------------
# Day-counter cache (read-through only; ledger is source of truth)
# ---------------------------------------------------------------------------


def _today_utc_str() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")


def _fresh_counts(date_str: str) -> dict[str, object]:
    return {
        "date": date_str,
        "GREEN": 0,
        "YELLOW": 0,
        "RED": 0,
        "ledger_seq_at_write": 0,
    }


def _rebuild_counts_from_ledger(
    ledger_path: Path, date_str: str
) -> dict[str, object]:
    """O(N) tail scan — only runs on counter-miss or cache-stale detection.

    Counts entries whose timestamp_utc starts with ``date_str``. The ledger
    is the SOLE source of truth per §5.3 v3 invariant.
    """
    counts = _fresh_counts(date_str)
    if not ledger_path.is_file():
        return counts
    try:
        with open(ledger_path, "rb") as fh:
            last_seq = 0
            for raw_line in fh:
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line.decode("utf-8"))
                except json.JSONDecodeError as exc:
                    raise LedgerUnreadable(
                        path=ledger_path, reason=str(exc)
                    ) from exc
                ts = entry.get("timestamp_utc", "")
                if ts.startswith(date_str):
                    sev = entry.get("severity")
                    if sev in SEVERITY_LIMITS:
                        counts[sev] = int(counts[sev]) + 1  # type: ignore[arg-type]
                seq = entry.get("seq_id", 0)
                if isinstance(seq, int) and seq > last_seq:
                    last_seq = seq
            counts["ledger_seq_at_write"] = last_seq
    except OSError as exc:
        raise LedgerUnreadable(path=ledger_path, reason=str(exc)) from exc
    return counts


def _read_counts_or_rebuild(
    repo_root: Path, date_str: str
) -> dict[str, object]:
    """v3 read-through cache. Reads counter or rebuilds on miss / stale."""
    counts_path = _counts_path(repo_root, date_str)
    if not counts_path.is_file():
        return _rebuild_counts_from_ledger(_ledger_path(repo_root), date_str)
    try:
        parsed = json.loads(counts_path.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        return _rebuild_counts_from_ledger(_ledger_path(repo_root), date_str)
    if parsed.get("date") != date_str:
        # Day rolled over. Rebuild from ledger for today.
        return _rebuild_counts_from_ledger(_ledger_path(repo_root), date_str)
    # Staleness probe: if the ledger has more entries than the counter knows
    # about, rebuild. This closes the crash-between-append-and-counter race.
    cached_seq = int(parsed.get("ledger_seq_at_write", 0))
    current_seq = _tail_seq(_ledger_path(repo_root))
    if cached_seq != current_seq:
        return _rebuild_counts_from_ledger(_ledger_path(repo_root), date_str)
    return parsed


def _tail_seq(ledger_path: Path) -> int:
    """Return the seq_id of the last ledger line, or 0 if empty."""
    if not ledger_path.is_file():
        return 0
    last_seq = 0
    try:
        with open(ledger_path, "rb") as fh:
            for raw_line in fh:
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line.decode("utf-8"))
                except json.JSONDecodeError as exc:
                    raise LedgerUnreadable(
                        path=ledger_path, reason=str(exc)
                    ) from exc
                seq = entry.get("seq_id", 0)
                if isinstance(seq, int) and seq > last_seq:
                    last_seq = seq
    except OSError as exc:
        raise LedgerUnreadable(path=ledger_path, reason=str(exc)) from exc
    return last_seq


def _write_counts(repo_root: Path, counts: dict[str, object]) -> None:
    """Atomic tmp+rename of the counter file. Held under the rate-lock."""
    counts_path = _counts_path(repo_root, str(counts["date"]))
    counts_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = counts_path.with_suffix(
        counts_path.suffix + f".tmp.{os.getpid()}.{int(time.monotonic_ns())}"
    )
    data = canonical_json_bytes(counts) + b"\n"
    fd = os.open(str(tmp), os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
    try:
        os.write(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)
    os.rename(str(tmp), str(counts_path))


# ---------------------------------------------------------------------------
# Public API — record
# ---------------------------------------------------------------------------


def _canonicalize_payload(payload: dict) -> str:
    return canonical_json_bytes(payload).decode("utf-8")


def record_admin_risk(
    *,
    repo_root: Path,
    entry_kind: str,
    severity: str,
    payload: dict,
    operator_retype_confirmation: str | None = None,
    hmac_key: bytes,
    watermarks_hmac_key: bytes,
) -> AdminRiskEntry:
    """Lock-first rate-checked append. [§5.3 v2 + §4.8 M13]

    Critical-section protocol (§5.3 v2):

    1. Acquire outer ``admin_risk.lock`` exclusive (blocking).
    2. Read or rebuild today's day counter (ledger is SoT).
    3. Rate-limit gate against ``SEVERITY_LIMITS[severity]``.
    4. RED requires ``operator_retype_confirmation`` non-empty.
    5. Build canonical-JSON payload + hash retype string.
    6. Call :func:`audit.append_to_ledger` which adds chain metadata
       and writes HMAC trailer + watermark atomically.
    7. Bump and write the day counter.
    8. Release lock.

    :raises TypeError: bad args (E-001).
    :raises ValueError: unknown severity/entry_kind.
    :raises OperatorConfirmationRequired: RED without retype.
    :raises RateLimitExceeded: window full for this severity.
    :raises LedgerUnreadable: pre-append chain verify failed.
    """
    # E-001 gate.
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    if not isinstance(entry_kind, str):
        raise TypeError("entry_kind must be str")
    if not isinstance(severity, str):
        raise TypeError("severity must be str")
    if not isinstance(payload, dict):
        raise TypeError("payload must be dict")
    if operator_retype_confirmation is not None and not isinstance(
        operator_retype_confirmation, str
    ):
        raise TypeError("operator_retype_confirmation must be str or None")
    if not isinstance(hmac_key, (bytes, bytearray)):
        raise TypeError("hmac_key must be bytes")
    if not isinstance(watermarks_hmac_key, (bytes, bytearray)):
        raise TypeError("watermarks_hmac_key must be bytes")

    if severity not in _VALID_SEVERITIES:
        raise ValueError(
            f"severity must be one of {sorted(_VALID_SEVERITIES)}; got {severity!r}"
        )
    if entry_kind not in _VALID_ENTRY_KINDS:
        raise ValueError(
            f"entry_kind must be one of {sorted(_VALID_ENTRY_KINDS)}; got {entry_kind!r}"
        )

    # Normalize keys to immutable bytes for audit.append_to_ledger.
    hmac_key_b = bytes(hmac_key)
    watermarks_hmac_key_b = bytes(watermarks_hmac_key)

    with _rate_lock(repo_root):
        today = _today_utc_str()
        counts = _read_counts_or_rebuild(repo_root, today)
        current = int(counts[severity])
        limit = SEVERITY_LIMITS[severity]
        if current >= limit:
            raise RateLimitExceeded(
                severity=severity, current=current, limit=limit
            )
        if severity == "RED" and not operator_retype_confirmation:
            raise OperatorConfirmationRequired(
                f"F-ADM-01: RED severity requires operator_retype_confirmation; "
                f"entry_kind={entry_kind!r}"
            )

        # Build payload + retype hash.
        payload_json = _canonicalize_payload(payload)
        retype_hash: str | None = None
        if operator_retype_confirmation is not None:
            retype_hash = _stdlib_hmac.new(
                hmac_key_b,
                operator_retype_confirmation.encode("utf-8"),
                hashlib.sha3_512,
            ).hexdigest()

        entry_fields = {
            "severity": severity,
            "entry_kind": entry_kind,
            "payload_json": payload_json,
            "operator_retype_hash": retype_hash,
        }

        # Delegate to audit for chain+trailer+watermark. audit acquires its
        # own data-level lock (inner admin_risk.data.lock); that's ok because
        # it's a distinct file from our outer rate-lock.
        trailer = append_to_ledger(
            _ledger_path(repo_root),
            entry_fields,
            ledger_name="admin_risk",
            hmac_key=hmac_key_b,
            lock_path=_data_lock_path(repo_root),
            trailer_path=_trailer_path(repo_root),
            watermarks_path=_watermarks_path(repo_root),
            watermarks_hmac_key=watermarks_hmac_key_b,
            watermarks_hmac_path=_watermarks_hmac_path(repo_root),
            watermarks_lock_path=_watermarks_lock_path(repo_root),
        )

        # Bump day counter under the outer lock; ledger is authoritative.
        counts[severity] = current + 1
        counts["ledger_seq_at_write"] = trailer.last_seq_id
        _write_counts(repo_root, counts)

        # Read back the just-appended entry from the ledger tail for the return.
        return _read_entry_by_seq(
            _ledger_path(repo_root), trailer.last_seq_id
        )


# ---------------------------------------------------------------------------
# Public API — read_ledger_tail
# ---------------------------------------------------------------------------


def _entry_from_json(line_bytes: bytes) -> AdminRiskEntry:
    obj = json.loads(line_bytes.decode("utf-8"))
    return AdminRiskEntry(
        seq_id=int(obj["seq_id"]),
        timestamp_utc=str(obj["timestamp_utc"]),
        issued_monotonic_ns=int(obj["issued_monotonic_ns"]),
        severity=str(obj["severity"]),
        entry_kind=str(obj["entry_kind"]),
        payload_json=str(obj["payload_json"]),
        operator_retype_hash=obj.get("operator_retype_hash"),
        prev_hash=str(obj["prev_hash"]),
        entry_hash=str(obj["entry_hash"]),
    )


def _read_entry_by_seq(ledger_path: Path, seq_id: int) -> AdminRiskEntry:
    """Scan tail-ward for the entry with the given seq_id."""
    if not ledger_path.is_file():
        raise LedgerMissing(f"F-ADM-03: ledger missing at {ledger_path}")
    try:
        with open(ledger_path, "rb") as fh:
            for raw_line in fh:
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line.decode("utf-8"))
                except json.JSONDecodeError as exc:
                    raise LedgerUnreadable(
                        path=ledger_path, reason=str(exc)
                    ) from exc
                if int(obj.get("seq_id", -1)) == seq_id:
                    return _entry_from_json(line)
    except OSError as exc:
        raise LedgerUnreadable(path=ledger_path, reason=str(exc)) from exc
    raise LedgerChainBroken(
        f"admin_risk ledger: seq_id={seq_id} not found after append"
    )


def read_ledger_tail(
    *, repo_root: Path, n: int = 50
) -> list[AdminRiskEntry]:
    """Return the last ``n`` entries in ledger order (oldest → newest).

    :raises TypeError / ValueError: bad args.
    :raises LedgerUnreadable: JSON parse failure mid-scan.
    """
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if n <= 0:
        raise ValueError("n must be positive")

    ledger_path = _ledger_path(repo_root)
    if not ledger_path.is_file():
        return []
    lines: list[bytes] = []
    try:
        with open(ledger_path, "rb") as fh:
            for raw_line in fh:
                stripped = raw_line.strip()
                if stripped:
                    lines.append(stripped)
    except OSError as exc:
        raise LedgerUnreadable(path=ledger_path, reason=str(exc)) from exc
    tail = lines[-n:]
    return [_entry_from_json(line) for line in tail]


# ---------------------------------------------------------------------------
# Public API — bypass_is_active (M13 predicate)
# ---------------------------------------------------------------------------


def _parse_iso(ts: str) -> _dt.datetime:
    """ISO-8601 with or without trailing Z, UTC-aware."""
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    dt = _dt.datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_dt.timezone.utc)
    return dt


@dataclass(frozen=True, kw_only=True)
class _DegradationEventShape:
    """Ducktype of §2.6 DegradationEvent — only the fields bypass_is_active reads.

    Published as an internal shape; Round G degradation_log.py will own the
    canonical DegradationEvent type. Until then, bypass_is_active accepts
    any object whose attributes match this shape.
    """

    event_kind: str
    expires_at: str | None
    expires_monotonic_ns: int | None
    boot_epoch_ns_at_issuance: int | None


def bypass_is_active(
    event,
    *,
    now_utc: _dt.datetime,
    now_mono_ns: int,
    boot_clock_history,
) -> bool:
    """§4.8 v2/v3 M13 bypass predicate. [§7.3 BT3]

    Returns True iff the bypass event is presently active:

    * ``event.event_kind == "review_seat_bypass_active"``.
    * Wall-clock ``expires_at`` not yet past (v2 primary gate).
    * Monotonic ``expires_monotonic_ns`` not yet past (v2 clock-tamper guard).
    * Boot-clock history does not show a post-issuance wall-clock rollback
      beyond the 5-minute NTP tolerance (v3 oracle).
    * ``boot_epoch_ns_at_issuance`` still appears in the current boot-clock
      history (v3 orphan-boot oracle).

    :raises BypassClockRollbackDetected: v3 rollback or orphan-boot.
    :raises TypeError: bad args (E-001).
    """
    if not isinstance(now_utc, _dt.datetime):
        raise TypeError("now_utc must be datetime")
    if now_utc.tzinfo is None:
        raise ValueError("now_utc must be tz-aware UTC")
    if not isinstance(now_mono_ns, int):
        raise TypeError("now_mono_ns must be int")

    event_kind = getattr(event, "event_kind", None)
    if event_kind != "review_seat_bypass_active":
        return False

    expires_at = getattr(event, "expires_at", None)
    expires_mono = getattr(event, "expires_monotonic_ns", None)
    issuance_boot = getattr(event, "boot_epoch_ns_at_issuance", None)

    # v2 — dual clock primary gate.
    wall_ok = expires_at is None or now_utc < _parse_iso(expires_at)
    mono_ok = expires_mono is None or now_mono_ns < int(expires_mono)
    if not (wall_ok and mono_ok):
        return False

    # v3 — rollback detection.
    history = list(boot_clock_history)
    if history:
        max_wall = max(_parse_iso(r.wall_at_boot_utc) for r in history)
        if now_utc + _dt.timedelta(
            seconds=CLOCK_ROLLBACK_TOLERANCE_SECONDS
        ) < max_wall:
            raise BypassClockRollbackDetected(
                reason=(
                    "wall-clock rollback beyond NTP slop "
                    f"(now={now_utc.isoformat()} < max_wall={max_wall.isoformat()})"
                )
            )

    # v3 — issuance-from-dead-boot.
    if issuance_boot is not None:
        known = {r.boot_epoch_ns for r in history}
        if issuance_boot not in known:
            raise BypassClockRollbackDetected(
                reason=(
                    f"issuance_boot_epoch_ns={issuance_boot} not in "
                    f"current boot_clock_history"
                )
            )

    return True


# ---------------------------------------------------------------------------
# Public aliases for Section 4 Logician verifier (§4.7 / M8)
# ---------------------------------------------------------------------------
# The Logician admin-risk verifier (`pipeline.logician.admin_risk`) is the
# section-boundary counterpart of this writer and legitimately needs the
# ledger/trailer path helpers and the entry parser. These aliases expose
# them through the sovereignty public API so the Logician consumer can
# satisfy the "import from `pipeline.sovereignty` only" discipline.

admin_risk_entry_from_json = _entry_from_json
admin_risk_ledger_path = _ledger_path
admin_risk_trailer_path = _trailer_path
