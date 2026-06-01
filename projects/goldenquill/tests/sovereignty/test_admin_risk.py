"""Unit + adversarial tests for pipeline.sovereignty.admin_risk.

Section 1 Round F3. Covers §2.5 + §3.7 + §4.8 M13 + §5.3 BT3 v2
critical-section discipline + §6.5 F-ADM-* codes + §7.3 regression triplet.

Named tests required by §7.3:

* ``test_admin_risk_fork_race_both_processes_blocked``
* ``test_admin_risk_day_counter_rebuilds_if_missing``
* ``test_admin_risk_day_counter_detects_inconsistency``
* ``test_ledger_hmac_trailer_written_on_every_append``
* ``test_rate_limit_green_yellow_red``
* ``test_red_requires_operator_retype_confirmation``
* ``test_bypass_is_active_wall_expires``
* ``test_bypass_is_active_monotonic_expires``
* ``test_bypass_clock_rollback_detected``
* ``test_bypass_orphan_boot_rejected``
"""

from __future__ import annotations

import datetime as _dt
import json
import multiprocessing as mp
import os
import time
from dataclasses import dataclass
from pathlib import Path

import pytest

from pipeline.sovereignty import admin_risk as ar
from pipeline.sovereignty.admin_risk import (
    AdminRiskEntry,
    BootClockRecord,
    BypassClockRollbackDetected,
    LedgerMissing,
    OperatorConfirmationRequired,
    RateLimitExceeded,
    SEVERITY_LIMITS,
    bypass_is_active,
    read_ledger_tail,
    record_admin_risk,
)
from pipeline.sovereignty.audit import LedgerTrailer, verify_ledger


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

LKEY = b"L" * 32
WKEY = b"W" * 32


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    return tmp_path


def _do_record(
    repo: Path,
    *,
    severity: str = "GREEN",
    entry_kind: str = "flagged_term_substitution",
    payload: dict | None = None,
    retype: str | None = None,
) -> AdminRiskEntry:
    return record_admin_risk(
        repo_root=repo,
        entry_kind=entry_kind,
        severity=severity,
        payload=payload if payload is not None else {"term": "foo"},
        operator_retype_confirmation=retype,
        hmac_key=LKEY,
        watermarks_hmac_key=WKEY,
    )


# ---------------------------------------------------------------------------
# E-001 arg-type gates
# ---------------------------------------------------------------------------


class TestArgGates:
    def test_repo_root_must_be_path(self, repo):
        with pytest.raises(TypeError):
            record_admin_risk(
                repo_root=str(repo),  # type: ignore[arg-type]
                entry_kind="flagged_term_substitution",
                severity="GREEN",
                payload={},
                hmac_key=LKEY,
                watermarks_hmac_key=WKEY,
            )

    def test_payload_must_be_dict(self, repo):
        with pytest.raises(TypeError):
            record_admin_risk(
                repo_root=repo,
                entry_kind="flagged_term_substitution",
                severity="GREEN",
                payload=[],  # type: ignore[arg-type]
                hmac_key=LKEY,
                watermarks_hmac_key=WKEY,
            )

    def test_unknown_severity_rejected(self, repo):
        with pytest.raises(ValueError):
            _do_record(repo, severity="PURPLE")

    def test_unknown_entry_kind_rejected(self, repo):
        with pytest.raises(ValueError):
            _do_record(repo, entry_kind="arbitrary")

    def test_hmac_key_must_be_bytes(self, repo):
        with pytest.raises(TypeError):
            record_admin_risk(
                repo_root=repo,
                entry_kind="flagged_term_substitution",
                severity="GREEN",
                payload={"x": 1},
                hmac_key="notbytes",  # type: ignore[arg-type]
                watermarks_hmac_key=WKEY,
            )


# ---------------------------------------------------------------------------
# Happy-path record
# ---------------------------------------------------------------------------


def test_record_green_happy_path(repo: Path) -> None:
    entry = _do_record(repo, severity="GREEN", payload={"term": "foo"})
    assert isinstance(entry, AdminRiskEntry)
    assert entry.severity == "GREEN"
    assert entry.entry_kind == "flagged_term_substitution"
    assert entry.seq_id == 1
    assert entry.operator_retype_hash is None
    # payload_json is canonical.
    assert entry.payload_json == '{"term":"foo"}'


def test_record_yellow_happy_path(repo: Path) -> None:
    entry = _do_record(repo, severity="YELLOW")
    assert entry.severity == "YELLOW"


def test_record_red_with_retype(repo: Path) -> None:
    entry = _do_record(
        repo,
        severity="RED",
        retype="I understand this is irreversible",
    )
    assert entry.severity == "RED"
    assert entry.operator_retype_hash is not None
    assert len(entry.operator_retype_hash) == 128  # sha3-512 hex


def test_red_requires_operator_retype_confirmation(repo: Path) -> None:
    with pytest.raises(OperatorConfirmationRequired) as excinfo:
        _do_record(repo, severity="RED", retype=None)
    assert excinfo.value.code == "F-ADM-01"


def test_red_empty_retype_also_rejected(repo: Path) -> None:
    with pytest.raises(OperatorConfirmationRequired):
        _do_record(repo, severity="RED", retype="")


def test_record_writes_jsonl_line(repo: Path) -> None:
    _do_record(repo, severity="GREEN")
    ledger = repo / "sovereignty" / "ledgers" / "admin_risk.jsonl"
    assert ledger.is_file()
    lines = [l for l in ledger.read_bytes().splitlines() if l.strip()]
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed["severity"] == "GREEN"
    assert parsed["seq_id"] == 1
    assert "entry_hash" in parsed and "prev_hash" in parsed


def _read_trailer_body(trailer_path: Path) -> dict:
    """audit.py writes the trailer as two canonical-JSON lines: body then hmac."""
    lines = trailer_path.read_bytes().splitlines()
    assert len(lines) >= 2
    return json.loads(lines[0])


def test_ledger_hmac_trailer_written_on_every_append(repo: Path) -> None:
    _do_record(repo, severity="GREEN")
    trailer = repo / "sovereignty" / "ledgers" / "admin_risk.hmac"
    assert trailer.is_file()
    body = _read_trailer_body(trailer)
    assert body["last_seq_id"] == 1
    assert body["ledger_name"] == "admin_risk"

    _do_record(repo, severity="YELLOW")
    body2 = _read_trailer_body(trailer)
    assert body2["last_seq_id"] == 2
    assert body2["last_entry_hash"] != body["last_entry_hash"]


def test_verify_ledger_passes_after_record(repo: Path) -> None:
    _do_record(repo, severity="GREEN")
    _do_record(repo, severity="YELLOW")
    # Sanity — Round-B verify_ledger accepts the ledger admin_risk wrote.
    trailer = verify_ledger(
        repo / "sovereignty" / "ledgers" / "admin_risk.jsonl",
        hmac_key=LKEY,
        trailer_path=repo / "sovereignty" / "ledgers" / "admin_risk.hmac",
    )
    assert isinstance(trailer, LedgerTrailer)
    assert trailer.last_seq_id == 2


# ---------------------------------------------------------------------------
# Rate limits (§5.3 BT3)
# ---------------------------------------------------------------------------


@pytest.fixture
def tiny_limits(monkeypatch):
    """Shrink SEVERITY_LIMITS so rate-limit tests are fast."""
    tiny = {"GREEN": 3, "YELLOW": 2, "RED": 1}
    monkeypatch.setitem(SEVERITY_LIMITS, "GREEN", tiny["GREEN"])
    monkeypatch.setitem(SEVERITY_LIMITS, "YELLOW", tiny["YELLOW"])
    monkeypatch.setitem(SEVERITY_LIMITS, "RED", tiny["RED"])
    return tiny


def test_rate_limit_green_yellow_red(repo: Path, tiny_limits) -> None:
    # GREEN: 3 ok, 4th blocked.
    for _ in range(tiny_limits["GREEN"]):
        _do_record(repo, severity="GREEN")
    with pytest.raises(RateLimitExceeded) as excinfo:
        _do_record(repo, severity="GREEN")
    assert excinfo.value.code == "F-ADM-02"
    assert excinfo.value.severity == "GREEN"
    assert excinfo.value.current == tiny_limits["GREEN"]

    # YELLOW: 2 ok, 3rd blocked.
    for _ in range(tiny_limits["YELLOW"]):
        _do_record(repo, severity="YELLOW")
    with pytest.raises(RateLimitExceeded):
        _do_record(repo, severity="YELLOW")

    # RED: 1 ok, 2nd blocked.
    _do_record(repo, severity="RED", retype="confirm")
    with pytest.raises(RateLimitExceeded):
        _do_record(repo, severity="RED", retype="confirm")


# ---------------------------------------------------------------------------
# Day-counter cache (§5.3 v3 read-through)
# ---------------------------------------------------------------------------


def _today() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")


def test_admin_risk_day_counter_rebuilds_if_missing(repo: Path) -> None:
    _do_record(repo, severity="GREEN")
    _do_record(repo, severity="YELLOW")

    counts_path = (
        repo / "sovereignty" / "ledgers" / f"admin_risk.counts.{_today()}.json"
    )
    assert counts_path.is_file()
    counts_path.unlink()

    # Rebuild on next record; still respects prior counts in ledger.
    _do_record(repo, severity="GREEN")
    parsed = json.loads(counts_path.read_text("utf-8"))
    assert parsed["GREEN"] == 2
    assert parsed["YELLOW"] == 1


def test_admin_risk_day_counter_detects_inconsistency(
    repo: Path, tiny_limits
) -> None:
    """If someone tampers with the counter cache to under-report, the next
    record call must detect the staleness (cached_seq != ledger_tail_seq)
    and rebuild from the ledger, not silently trust the stale cache.
    """
    for _ in range(tiny_limits["GREEN"]):
        _do_record(repo, severity="GREEN")

    counts_path = (
        repo / "sovereignty" / "ledgers" / f"admin_risk.counts.{_today()}.json"
    )
    parsed = json.loads(counts_path.read_text("utf-8"))
    # Tamper: lie that only 1 GREEN happened, and roll back the seq pointer.
    parsed["GREEN"] = 1
    parsed["ledger_seq_at_write"] = 1
    counts_path.write_text(json.dumps(parsed), encoding="utf-8")

    # Next record must rebuild from ledger — so the 4th GREEN attempt is
    # blocked by the real limit, not let through by the lie.
    with pytest.raises(RateLimitExceeded):
        _do_record(repo, severity="GREEN")


def test_counter_day_rollover_rebuilds(repo: Path) -> None:
    """If the cached 'date' is yesterday, next call rebuilds for today."""
    _do_record(repo, severity="GREEN")
    counts_path = (
        repo / "sovereignty" / "ledgers" / f"admin_risk.counts.{_today()}.json"
    )
    parsed = json.loads(counts_path.read_text("utf-8"))
    yesterday_path = (
        repo / "sovereignty" / "ledgers" / "admin_risk.counts.1999-01-01.json"
    )
    yesterday = {**parsed, "date": "1999-01-01"}
    yesterday_path.write_text(json.dumps(yesterday), encoding="utf-8")
    # Today's counter still exists, so today's path is used. The yesterday
    # write is a no-op distractor; this exists to prove we look up by today.
    _do_record(repo, severity="GREEN")
    today_parsed = json.loads(counts_path.read_text("utf-8"))
    assert today_parsed["GREEN"] == 2


# ---------------------------------------------------------------------------
# read_ledger_tail
# ---------------------------------------------------------------------------


class TestReadTail:
    def test_empty_returns_empty_list(self, repo: Path) -> None:
        assert read_ledger_tail(repo_root=repo, n=10) == []

    def test_returns_last_n(self, repo: Path) -> None:
        for i in range(5):
            _do_record(repo, severity="GREEN", payload={"i": i})
        tail = read_ledger_tail(repo_root=repo, n=3)
        assert [e.seq_id for e in tail] == [3, 4, 5]

    def test_n_larger_than_ledger_returns_all(self, repo: Path) -> None:
        _do_record(repo, severity="GREEN")
        _do_record(repo, severity="YELLOW")
        tail = read_ledger_tail(repo_root=repo, n=100)
        assert len(tail) == 2

    def test_bad_n_raises(self, repo: Path) -> None:
        with pytest.raises(ValueError):
            read_ledger_tail(repo_root=repo, n=0)
        with pytest.raises(ValueError):
            read_ledger_tail(repo_root=repo, n=-5)

    def test_bad_repo_type_raises(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            read_ledger_tail(repo_root=str(repo), n=1)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Fork-race BT3 (v2 critical section)
# ---------------------------------------------------------------------------


def _child_append_batch(
    repo_str: str, severity: str, count: int
) -> tuple[int, int]:
    """Child process: attempt `count` appends; return (successes, rate_limits)."""
    repo_p = Path(repo_str)
    ok = 0
    blocked = 0
    for _ in range(count):
        try:
            record_admin_risk(
                repo_root=repo_p,
                entry_kind="flagged_term_substitution",
                severity=severity,
                payload={"pid": os.getpid()},
                hmac_key=LKEY,
                watermarks_hmac_key=WKEY,
            )
            ok += 1
        except RateLimitExceeded:
            blocked += 1
    return ok, blocked


def test_admin_risk_fork_race_both_processes_blocked(
    repo: Path, tiny_limits
) -> None:
    """Two processes racing past the GREEN limit. Exactly `limit` successes
    across both should be admitted; the rest must raise RateLimitExceeded.
    BT3 v2 lock-first critical section — the outer admin_risk.lock serializes
    counter-read + append + counter-write, so the counter can't be
    double-consumed across the fork boundary.
    """
    ctx = mp.get_context("fork")
    with ctx.Pool(processes=2) as pool:
        results = pool.starmap(
            _child_append_batch,
            [(str(repo), "GREEN", tiny_limits["GREEN"]) for _ in range(2)],
        )
    total_ok = sum(ok for ok, _ in results)
    total_blocked = sum(b for _, b in results)
    # Exactly `limit` admitted, rest blocked.
    assert total_ok == tiny_limits["GREEN"]
    assert total_blocked == tiny_limits["GREEN"]  # 2*limit attempted


# ---------------------------------------------------------------------------
# §4.8 bypass_is_active predicate
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class _FakeEvent:
    """Ducktype of §2.6 DegradationEvent used until Round G lands the real type."""

    event_kind: str
    expires_at: str | None = None
    expires_monotonic_ns: int | None = None
    boot_epoch_ns_at_issuance: int | None = None


def _utc(s: str) -> _dt.datetime:
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return _dt.datetime.fromisoformat(s)


class TestBypassIsActive:
    def test_non_bypass_kind_returns_false(self) -> None:
        ev = _FakeEvent(event_kind="something_else")
        assert (
            bypass_is_active(
                ev,
                now_utc=_utc("2026-04-19T12:00:00Z"),
                now_mono_ns=10_000,
                boot_clock_history=[],
            )
            is False
        )

    def test_happy_path_returns_true(self) -> None:
        ev = _FakeEvent(
            event_kind="review_seat_bypass_active",
            expires_at="2026-04-19T13:00:00Z",
            expires_monotonic_ns=1_000_000,
            boot_epoch_ns_at_issuance=42,
        )
        hist = [
            BootClockRecord(boot_epoch_ns=42, wall_at_boot_utc="2026-04-19T11:00:00Z")
        ]
        assert (
            bypass_is_active(
                ev,
                now_utc=_utc("2026-04-19T12:00:00Z"),
                now_mono_ns=500_000,
                boot_clock_history=hist,
            )
            is True
        )

    def test_bypass_is_active_wall_expires(self) -> None:
        ev = _FakeEvent(
            event_kind="review_seat_bypass_active",
            expires_at="2026-04-19T12:00:00Z",
            expires_monotonic_ns=10**18,  # mono not expired
            boot_epoch_ns_at_issuance=1,
        )
        hist = [
            BootClockRecord(boot_epoch_ns=1, wall_at_boot_utc="2026-04-19T10:00:00Z")
        ]
        assert (
            bypass_is_active(
                ev,
                now_utc=_utc("2026-04-19T12:00:01Z"),
                now_mono_ns=100,
                boot_clock_history=hist,
            )
            is False
        )

    def test_bypass_is_active_monotonic_expires(self) -> None:
        ev = _FakeEvent(
            event_kind="review_seat_bypass_active",
            expires_at="2099-01-01T00:00:00Z",  # wall far in the future
            expires_monotonic_ns=500,  # mono already expired
            boot_epoch_ns_at_issuance=1,
        )
        hist = [
            BootClockRecord(boot_epoch_ns=1, wall_at_boot_utc="2026-04-19T10:00:00Z")
        ]
        assert (
            bypass_is_active(
                ev,
                now_utc=_utc("2026-04-19T12:00:00Z"),
                now_mono_ns=1_000,
                boot_clock_history=hist,
            )
            is False
        )

    def test_bypass_clock_rollback_detected(self) -> None:
        """Clock rolled back beyond NTP tolerance (5 min) relative to the
        highest wall_at_boot_utc in the history → F-DEG-03 raised."""
        ev = _FakeEvent(
            event_kind="review_seat_bypass_active",
            expires_at="2099-01-01T00:00:00Z",
            expires_monotonic_ns=10**18,
            boot_epoch_ns_at_issuance=1,
        )
        hist = [
            BootClockRecord(boot_epoch_ns=1, wall_at_boot_utc="2026-04-19T12:00:00Z")
        ]
        with pytest.raises(BypassClockRollbackDetected) as excinfo:
            bypass_is_active(
                ev,
                now_utc=_utc("2026-04-19T11:50:00Z"),  # 10 min rollback
                now_mono_ns=100,
                boot_clock_history=hist,
            )
        assert "rollback" in excinfo.value.reason

    def test_rollback_within_ntp_slop_ok(self) -> None:
        """Sub-tolerance rollback (<5 min) must not raise."""
        ev = _FakeEvent(
            event_kind="review_seat_bypass_active",
            expires_at="2099-01-01T00:00:00Z",
            expires_monotonic_ns=10**18,
            boot_epoch_ns_at_issuance=1,
        )
        hist = [
            BootClockRecord(boot_epoch_ns=1, wall_at_boot_utc="2026-04-19T12:00:00Z")
        ]
        assert (
            bypass_is_active(
                ev,
                now_utc=_utc("2026-04-19T11:58:00Z"),  # 2 min rollback
                now_mono_ns=100,
                boot_clock_history=hist,
            )
            is True
        )

    def test_bypass_orphan_boot_rejected(self) -> None:
        """issuance_boot_epoch_ns not present in current history → F-DEG-03."""
        ev = _FakeEvent(
            event_kind="review_seat_bypass_active",
            expires_at="2099-01-01T00:00:00Z",
            expires_monotonic_ns=10**18,
            boot_epoch_ns_at_issuance=999,  # not in history
        )
        hist = [
            BootClockRecord(boot_epoch_ns=1, wall_at_boot_utc="2026-04-19T10:00:00Z"),
            BootClockRecord(boot_epoch_ns=2, wall_at_boot_utc="2026-04-19T11:00:00Z"),
        ]
        with pytest.raises(BypassClockRollbackDetected) as excinfo:
            bypass_is_active(
                ev,
                now_utc=_utc("2026-04-19T12:00:00Z"),
                now_mono_ns=100,
                boot_clock_history=hist,
            )
        assert "issuance_boot_epoch_ns" in excinfo.value.reason

    def test_now_utc_must_be_tz_aware(self) -> None:
        ev = _FakeEvent(event_kind="review_seat_bypass_active")
        with pytest.raises(ValueError):
            bypass_is_active(
                ev,
                now_utc=_dt.datetime(2026, 4, 19, 12, 0, 0),
                now_mono_ns=0,
                boot_clock_history=[],
            )

    def test_now_utc_type_gate(self) -> None:
        ev = _FakeEvent(event_kind="review_seat_bypass_active")
        with pytest.raises(TypeError):
            bypass_is_active(
                ev,
                now_utc="2026-04-19T12:00:00Z",  # type: ignore[arg-type]
                now_mono_ns=0,
                boot_clock_history=[],
            )
