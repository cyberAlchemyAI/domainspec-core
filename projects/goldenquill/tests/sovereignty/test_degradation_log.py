"""Unit + adversarial tests for pipeline.sovereignty.degradation_log.

Section 1 Round G. Covers §2.6 + §3.8 + §4.7 M10 + §4.8 M13 recording
+ §6.5 F-DEG-01..03 + §7.3 test criteria.

Named tests per §7.3 / §7.12-§7.13:

* ``test_m13_bypass_wall_clock_rollback_detected_via_boot_history``
* ``test_m13_bypass_process_restart_monotonic_reset_does_not_extend``
* ``test_m13_clock_forward_jump_does_not_extend_bypass``
* ``test_m10_author_seat_degraded_run_recorded``
* ``test_verify_chain_detects_tamper``
* ``test_review_seat_bypass_requires_signed_by_operator``
"""

from __future__ import annotations

import datetime as _dt
import json
import time
from pathlib import Path

import pytest

from pipeline.sovereignty import (
    BypassClockRollbackDetected,
    BootClockRecord,
    DegradationEvent,
    DegradationLogCorrupt,
    LedgerChainBroken,
    LedgerHMACTrailerMismatch,
    LedgerTrailer,
    bypass_is_active,
    read_degradation_tail,
    record_degradation,
    verify_chain,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

LKEY = b"L" * 32
WKEY = b"W" * 32


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    return tmp_path


def _record(repo: Path, **overrides) -> DegradationEvent:
    base: dict = dict(
        repo_root=repo,
        event_kind="author_seat_degraded_run",
        seat="scribe",
        reason_code="family_outage_30m",
        hmac_key=LKEY,
        watermarks_hmac_key=WKEY,
        duration_seconds=1800,
        signed_by_operator=False,
    )
    base.update(overrides)
    return record_degradation(**base)


# ---------------------------------------------------------------------------
# E-001 arg-type gates
# ---------------------------------------------------------------------------


class TestArgGates:
    def test_repo_root_must_be_path(self, repo):
        with pytest.raises(TypeError):
            _record(repo, repo_root=str(repo))

    def test_event_kind_must_be_known(self, repo):
        with pytest.raises(ValueError):
            _record(repo, event_kind="unknown_kind")

    def test_seat_must_be_known(self, repo):
        with pytest.raises(ValueError):
            _record(repo, seat="sommelier")

    def test_empty_reason_code_rejected(self, repo):
        with pytest.raises(ValueError):
            _record(repo, reason_code="")

    def test_hmac_key_must_be_bytes(self, repo):
        with pytest.raises(TypeError):
            _record(repo, hmac_key="abc")

    def test_authorization_id_type_gate(self, repo):
        with pytest.raises(TypeError):
            _record(repo, authorization_id="42")

    def test_boot_epoch_ns_type_gate(self, repo):
        with pytest.raises(TypeError):
            _record(repo, boot_epoch_ns_at_issuance="555")

    def test_signed_by_operator_must_be_bool(self, repo):
        with pytest.raises(TypeError):
            _record(repo, signed_by_operator="yes")


# ---------------------------------------------------------------------------
# Happy-path record (M10 author-seat degraded run)
# ---------------------------------------------------------------------------


def test_m10_author_seat_degraded_run_recorded(repo: Path) -> None:
    event = _record(
        repo,
        event_kind="author_seat_degraded_run",
        seat="scout",
        reason_code="family_outage_30m",
        duration_seconds=1800,
    )
    assert isinstance(event, DegradationEvent)
    assert event.event_kind == "author_seat_degraded_run"
    assert event.seat == "scout"
    assert event.reason_code == "family_outage_30m"
    assert event.duration_seconds == 1800
    assert event.signed_by_operator is False
    assert event.seq_id == 1
    assert len(event.entry_hash) == 128


def test_writes_jsonl_line(repo: Path) -> None:
    _record(repo)
    ledger = repo / "sovereignty" / "ledgers" / "degradation.jsonl"
    assert ledger.is_file()
    lines = [l for l in ledger.read_bytes().splitlines() if l.strip()]
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed["event_kind"] == "author_seat_degraded_run"
    assert parsed["seq_id"] == 1


def test_multiple_records_chain(repo: Path) -> None:
    e1 = _record(repo, seat="scout")
    e2 = _record(repo, seat="scribe")
    e3 = _record(repo, seat="editor")
    assert e1.seq_id == 1
    assert e2.seq_id == 2
    assert e3.seq_id == 3
    # Hash chain continuity: each prev_hash links to the previous entry_hash.
    assert e2.prev_hash == e1.entry_hash
    assert e3.prev_hash == e2.entry_hash


# ---------------------------------------------------------------------------
# M13 bypass recording (§4.8)
# ---------------------------------------------------------------------------


def _bypass_kwargs(
    repo: Path,
    *,
    boot_epoch: int = 111,
    expires_at: str = "2099-01-01T00:00:00Z",
    mono: int | None = None,
) -> dict:
    if mono is None:
        mono = time.monotonic_ns() + 60 * 60 * 10**9  # +1h
    return dict(
        event_kind="review_seat_bypass_active",
        seat="judge",
        reason_code="operator_m13_auth",
        duration_seconds=3600,
        authorization_id=42,
        expires_at=expires_at,
        expires_monotonic_ns=mono,
        boot_epoch_ns_at_issuance=boot_epoch,
        signed_by_operator=True,
    )


def test_review_seat_bypass_recorded_with_operator_signature(repo: Path) -> None:
    event = _record(repo, **_bypass_kwargs(repo))
    assert event.event_kind == "review_seat_bypass_active"
    assert event.signed_by_operator is True
    assert event.authorization_id == 42
    assert event.boot_epoch_ns_at_issuance == 111


def test_review_seat_bypass_requires_signed_by_operator(repo: Path) -> None:
    kwargs = _bypass_kwargs(repo)
    kwargs["signed_by_operator"] = False
    with pytest.raises(ValueError, match="signed_by_operator"):
        _record(repo, **kwargs)


# ---------------------------------------------------------------------------
# M13 bypass_is_active composition — Round F admin_risk owns the predicate,
# Round G degradation_log persists the event that feeds it. Verify the two
# compose correctly through a real on-disk round-trip.
# ---------------------------------------------------------------------------


def test_m13_bypass_is_active_through_persisted_event(repo: Path) -> None:
    now_mono = time.monotonic_ns()
    event = _record(
        repo,
        **_bypass_kwargs(
            repo, boot_epoch=111, mono=now_mono + 60 * 60 * 10**9
        ),
    )
    tail = read_degradation_tail(repo_root=repo, n=1)
    assert tail == [event]

    hist = [
        BootClockRecord(
            boot_epoch_ns=111, wall_at_boot_utc="2026-04-19T10:00:00Z"
        )
    ]
    assert (
        bypass_is_active(
            event,
            now_utc=_dt.datetime(
                2026, 4, 19, 11, 0, 0, tzinfo=_dt.timezone.utc
            ),
            now_mono_ns=now_mono,
            boot_clock_history=hist,
        )
        is True
    )


def test_m13_clock_forward_jump_does_not_extend_bypass(repo: Path) -> None:
    """Wall clock jumps past expires_at → bypass_is_active returns False even
    though monotonic is still within the window."""
    now_mono = time.monotonic_ns()
    event = _record(
        repo,
        **_bypass_kwargs(
            repo,
            boot_epoch=111,
            expires_at="2026-04-19T12:00:00Z",
            mono=now_mono + 10 * 60 * 60 * 10**9,  # +10h monotonic, huge window
        ),
    )
    hist = [
        BootClockRecord(
            boot_epoch_ns=111, wall_at_boot_utc="2026-04-19T10:00:00Z"
        )
    ]
    # Wall now == one second past expiry, monotonic still fine.
    assert (
        bypass_is_active(
            event,
            now_utc=_dt.datetime(
                2026, 4, 19, 12, 0, 1, tzinfo=_dt.timezone.utc
            ),
            now_mono_ns=now_mono,
            boot_clock_history=hist,
        )
        is False
    )


def test_m13_bypass_wall_clock_rollback_detected_via_boot_history(
    repo: Path,
) -> None:
    """Issue a bypass, boot_clock_history shows a boot at t=12:00:00, then
    now_utc is rolled back to t=11:50:00 (10min before). Beyond NTP 5-min
    slop → BypassClockRollbackDetected."""
    now_mono = time.monotonic_ns()
    event = _record(
        repo,
        **_bypass_kwargs(
            repo,
            boot_epoch=111,
            expires_at="2099-01-01T00:00:00Z",
            mono=now_mono + 10 * 10**18,
        ),
    )
    hist = [
        BootClockRecord(
            boot_epoch_ns=111, wall_at_boot_utc="2026-04-19T12:00:00Z"
        )
    ]
    with pytest.raises(BypassClockRollbackDetected):
        bypass_is_active(
            event,
            now_utc=_dt.datetime(
                2026, 4, 19, 11, 50, 0, tzinfo=_dt.timezone.utc
            ),
            now_mono_ns=now_mono,
            boot_clock_history=hist,
        )


def test_m13_bypass_process_restart_monotonic_reset_does_not_extend(
    repo: Path,
) -> None:
    """Bypass issued under boot_epoch_ns=111; after a restart the current
    boot_clock_history only shows boot_epoch_ns=222. The issuance is
    orphaned → BypassClockRollbackDetected.

    Also confirms wall-clock expiry still holds within the window
    (belt-and-suspenders: if an attacker pins the wall clock inside the
    window after the restart, the orphan-boot check still fires)."""
    event = _record(
        repo,
        **_bypass_kwargs(
            repo,
            boot_epoch=111,
            expires_at="2099-01-01T00:00:00Z",
            mono=10 * 10**18,
        ),
    )
    # New boot — boot_epoch_ns=111 is no longer in history.
    hist = [
        BootClockRecord(
            boot_epoch_ns=222, wall_at_boot_utc="2026-04-19T14:00:00Z"
        )
    ]
    with pytest.raises(BypassClockRollbackDetected) as excinfo:
        bypass_is_active(
            event,
            now_utc=_dt.datetime(
                2026, 4, 19, 14, 5, 0, tzinfo=_dt.timezone.utc
            ),
            now_mono_ns=0,  # fresh monotonic; reset at restart
            boot_clock_history=hist,
        )
    assert "issuance_boot_epoch_ns" in excinfo.value.reason


# ---------------------------------------------------------------------------
# read_degradation_tail
# ---------------------------------------------------------------------------


class TestReadTail:
    def test_empty_returns_empty_list(self, repo: Path) -> None:
        assert read_degradation_tail(repo_root=repo, n=10) == []

    def test_returns_last_n(self, repo: Path) -> None:
        for _ in range(5):
            _record(repo)
        tail = read_degradation_tail(repo_root=repo, n=3)
        assert [e.seq_id for e in tail] == [3, 4, 5]

    def test_bad_n_raises(self, repo: Path) -> None:
        with pytest.raises(ValueError):
            read_degradation_tail(repo_root=repo, n=0)
        with pytest.raises(ValueError):
            read_degradation_tail(repo_root=repo, n=-1)

    def test_bad_repo_type_raises(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            read_degradation_tail(repo_root=str(repo), n=1)


# ---------------------------------------------------------------------------
# verify_chain
# ---------------------------------------------------------------------------


def test_verify_chain_passes_after_records(repo: Path) -> None:
    _record(repo, seat="scout")
    _record(repo, seat="scribe")
    _record(repo, seat="editor")
    trailer = verify_chain(repo_root=repo, hmac_key=LKEY)
    assert isinstance(trailer, LedgerTrailer)
    assert trailer.last_seq_id == 3
    assert trailer.ledger_name == "degradation"


def test_verify_chain_detects_tamper(repo: Path) -> None:
    _record(repo, seat="scout")
    _record(repo, seat="scribe")
    ledger = repo / "sovereignty" / "ledgers" / "degradation.jsonl"
    data = bytearray(ledger.read_bytes())
    # Flip one byte somewhere inside the second entry's JSON.
    # Target a character safely inside a string value — "scribe" is there.
    idx = data.index(b"scribe") + 1
    data[idx] ^= 0x20
    ledger.write_bytes(bytes(data))
    with pytest.raises((LedgerHMACTrailerMismatch, LedgerChainBroken)):
        verify_chain(repo_root=repo, hmac_key=LKEY)


def test_verify_chain_rejects_bad_hmac_key(repo: Path) -> None:
    _record(repo)
    with pytest.raises(LedgerHMACTrailerMismatch):
        verify_chain(repo_root=repo, hmac_key=b"X" * 32)


# ---------------------------------------------------------------------------
# Exception hierarchy — E-014 family
# ---------------------------------------------------------------------------


def test_exception_family_has_codes() -> None:
    assert DegradationLogCorrupt.code == "F-DEG-01"
    # BypassExpired code asserted via import
    from pipeline.sovereignty.degradation_log import (
        BypassExpired,
        DegradationError,
    )

    assert BypassExpired.code == "F-DEG-02"
    assert issubclass(DegradationLogCorrupt, DegradationError)
    assert issubclass(BypassExpired, DegradationError)
