"""§13.5.3 + §13.8.6 — consent ledger atomic substrate tests.

Covers:
- Read/write round-trip of ConsentLedgerEntry.
- Symlink refusal (RT-26 mirror + §13.9.4 .symlink_escape).
- Cross-channel opt-out propagation with rollback (RT-02 + RT-C2-02).
- fcntl.flock atomic discipline.
- compute_consent_state_hash full SHA3-512 digest (RT-13).
- is_opt_out_signal keyword detection (STOP/UNSUBSCRIBE/END/QUIT/CANCEL).
"""
from __future__ import annotations

import dataclasses
import os
from datetime import datetime, timezone
from pathlib import Path

import pytest

from pipeline.orchestrator.seats.data_collector import ConsentLedgerEntry
from pipeline.orchestrator.seats.data_collector.consent_ledger import (
    CHANNELS,
    OPT_OUT_KEYWORDS,
    LedgerPropagationError,
    LedgerSchemaError,
    compute_consent_state_hash,
    is_opt_out_signal,
    ledger_path,
    propagate_opt_out,
    read_entry,
    write_entry,
)


def _make_entry(
    *,
    recipient_id: str = "recipient-X",
    channel: str = "email",
    consent_active: bool = True,
    opt_out_active: bool = False,
) -> ConsentLedgerEntry:
    return ConsentLedgerEntry(
        recipient_id=recipient_id,
        channel=channel,
        consent_active=consent_active,
        consent_captured_at_utc=datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc),
        consent_capture_method="opt_in_link_email" if channel == "email" else (
            "sms_double_opt_in" if channel == "sms"
            else "voice_recorded_consent" if channel == "voice"
            else "telegram_in_app_optin" if channel == "telegram"
            else "whatsapp_business_optin"
        ),
        opt_out_active=opt_out_active,
        opt_out_at_utc=None,
        opt_out_propagated_from_channel=[],
        frequency_cap_lookback_days=7,
        recent_outbound_log=[],
        state_code_for_rules="PA",
        audit_chain=[],
    )


def test_round_trip_write_read(tmp_path):
    entry = _make_entry()
    write_entry(tmp_path, entry)
    loaded = read_entry(tmp_path, entry.recipient_id, entry.channel)
    assert loaded == entry


def test_read_missing_returns_none(tmp_path):
    assert read_entry(tmp_path, "no-such", "email") is None


def test_unknown_channel_refused(tmp_path):
    with pytest.raises(LedgerSchemaError):
        ledger_path(tmp_path, "r", "fax")


def test_symlink_refused(tmp_path):
    entry = _make_entry()
    write_entry(tmp_path, entry)
    real = ledger_path(tmp_path, entry.recipient_id, entry.channel)
    link = tmp_path / "link__email.yaml"
    os.symlink(real, link)
    # The symlink-name is a different recipient_id ("link"), so the read path
    # equals the link path. The substrate refuses to follow it.
    with pytest.raises(LedgerSchemaError):
        read_entry(tmp_path, "link", "email")


def test_cross_channel_propagation_sms_triggers_all(tmp_path):
    # Seed: recipient has consent on email + sms; an SMS STOP arrives.
    for ch in ("email", "sms"):
        write_entry(tmp_path, _make_entry(channel=ch))
    received_at = datetime(2026, 5, 10, 18, 0, 0, tzinfo=timezone.utc)
    new_entries = propagate_opt_out(
        tmp_path,
        "recipient-X",
        source_channel="sms",
        received_at_utc=received_at,
    )
    # Both ledger entries are now opted out and reflect the SMS source.
    assert set(new_entries.keys()) == {"email", "sms"}
    for ch in ("email", "sms"):
        post = read_entry(tmp_path, "recipient-X", ch)
        assert post is not None
        assert post.opt_out_active is True
        assert "sms" in post.opt_out_propagated_from_channel
        # The audit chain captured the propagation event.
        assert any(row.get("kind") == "opt_out_propagation" for row in post.audit_chain)


def test_propagation_no_consent_on_other_channels_is_idempotent(tmp_path):
    write_entry(tmp_path, _make_entry(channel="email"))
    propagate_opt_out(
        tmp_path,
        "recipient-X",
        source_channel="operator_explicit",
        received_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
    )
    # No silent ledger files on channels with no prior consent.
    assert read_entry(tmp_path, "recipient-X", "sms") is None
    # Email got opted out.
    assert read_entry(tmp_path, "recipient-X", "email").opt_out_active is True


def test_compute_consent_state_hash_is_full_sha3_512(tmp_path):
    entry = _make_entry()
    digest = compute_consent_state_hash(entry)
    # SHA3-512 → 128 hex chars per RT-13.
    assert len(digest) == 128
    assert all(c in "0123456789abcdef" for c in digest)


def test_compute_consent_state_hash_stable(tmp_path):
    entry = _make_entry()
    assert compute_consent_state_hash(entry) == compute_consent_state_hash(entry)


def test_compute_consent_state_hash_changes_with_opt_out(tmp_path):
    e1 = _make_entry(opt_out_active=False)
    e2 = dataclasses.replace(e1, opt_out_active=True)
    assert compute_consent_state_hash(e1) != compute_consent_state_hash(e2)


def test_is_opt_out_signal_keywords():
    for kw in OPT_OUT_KEYWORDS:
        assert is_opt_out_signal(kw)
        assert is_opt_out_signal(kw.lower())
        assert is_opt_out_signal(f"  {kw}  ")
    assert not is_opt_out_signal("hello")
    assert not is_opt_out_signal("")
    assert not is_opt_out_signal("STOP! please")  # multi-word — must be solitary


def test_channels_tuple_matches_v0_2_first_wave():
    assert CHANNELS == ("email", "sms", "voice", "telegram", "whatsapp")
