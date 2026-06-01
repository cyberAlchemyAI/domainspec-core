"""§13.13.11 — Outbound batch dispatcher tests.

Per §13.4.2 + §13.7 four-layer defense + Cycle-1/Cycle-2 closure surface.

Coverage:
- Layer 2 Ed25519 signature verify at function entry (RT-14 + RT-C2-01)
- ``batch_status_not_approved_for_send`` blanket fail (Layer-2 PRE-gate)
- ``operator_signature_invalid`` blanket fail
- ``operator_signature_grant_or_org_mismatch`` per-recipient fail (RT-C2-01)
- ``per_recipient_signature_invalid`` per-recipient fail (RT-14)
- ``per_recipient_signature_grant_or_org_mismatch`` per-recipient fail (RT-C2-01)
- ``send_time_consent_drift`` per-recipient fail (RT-01)
- ``batch_recipient_order_swap`` per-recipient fail (RT-C2-12)
- ``channel_not_registered`` per-recipient fail
- ``ledger_absent`` per-recipient fail
- Lock-hold-through-transport — transport call happens while lock is held
  (RT-C2-05)
- Per-recipient ``SendResult`` returned in ``approved_recipient_order``
"""

from __future__ import annotations

import json
import shutil
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Mapping, Optional

import pytest
import yaml
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from pipeline.orchestrator.seats.data_collector import (
    ConsentLedgerEntry,
    OutboundMessage,
    SendResult,
    SignedBatchEnvelope,
)
from pipeline.orchestrator.seats.data_collector.consent_ledger import (
    compute_consent_state_hash,
    write_entry,
)
from pipeline.orchestrator.seats.data_collector.outbound_batch import (
    canonical_envelope_payload,
    canonical_outbound_message_payload,
    dispatch_after_operator_approval,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def operator_keypair():
    sk = Ed25519PrivateKey.generate()
    return sk, sk.public_key()


@pytest.fixture
def recipient_keypair():
    sk = Ed25519PrivateKey.generate()
    return sk, sk.public_key()


@pytest.fixture
def ledger_root(tmp_path):
    root = tmp_path / "consent_ledger"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _make_consent_entry(
    *,
    recipient_id: str = "r_001",
    channel: str = "email",
    opt_out: bool = False,
) -> ConsentLedgerEntry:
    return ConsentLedgerEntry(
        recipient_id=recipient_id,
        channel=channel,  # type: ignore[arg-type]
        consent_active=not opt_out,
        consent_captured_at_utc=datetime(2026, 1, 1, tzinfo=timezone.utc),
        consent_capture_method="award_acceptance_signed_form",
        opt_out_active=opt_out,
        opt_out_at_utc=datetime(2026, 5, 1, tzinfo=timezone.utc) if opt_out else None,
        opt_out_propagated_from_channel=[],
        frequency_cap_lookback_days=30,
        recent_outbound_log=[],
        state_code_for_rules="PA",
        audit_chain=[],
    )


def _make_outbound_message(
    *,
    outbound_id: str = "o_001",
    recipient_id: str = "r_001",
    channel: str = "email",
    grant_id: str = "g_001",
    org_slug: str = "o_acme",
    per_recipient_signature: bytes = b"\x00" * 64,
) -> OutboundMessage:
    return OutboundMessage(
        outbound_id=outbound_id,
        dc_run_id="run_001",
        recipient_id=recipient_id,
        channel=channel,  # type: ignore[arg-type]
        grant_id=grant_id,
        org_slug=org_slug,
        commitment_id_or_funder_reporting_field_id="c_001",
        rendered_message_bytes_sha3_512="ab" * 64,
        per_state_disclaimers_applied=["PA_CONSENT"],
        per_recipient_token_id="t_001",
        staged_at_utc=datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc),
        sent_at_utc=None,
        per_recipient_signature=per_recipient_signature,
    )


def _make_signed_batch(
    *,
    operator_sk: Ed25519PrivateKey,
    recipient_ids: list[str],
    consent_state_hashes: dict[str, str],
    grant_id: str = "g_001",
    org_slug: str = "o_acme",
    batch_status: str = "APPROVED_FOR_SEND",
    tamper_signature: bool = False,
) -> SignedBatchEnvelope:
    envelope = SignedBatchEnvelope(
        batch_id="b_001",
        compose_run_id="run_001",
        grant_id=grant_id,
        org_slug=org_slug,
        period_n=1,
        batch_status=batch_status,  # type: ignore[arg-type]
        batch_content_sha3_512="cd" * 64,
        batch_manifest_sha3_512="ef" * 64,
        approved_recipient_order=list(recipient_ids),
        per_recipient_consent_state_sha3_512_full=dict(consent_state_hashes),
        signed_at_utc=datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc),
        signed_by="operator_acme_2026",
        signature=b"\x00" * 64,  # placeholder; replaced below
    )
    # Sign canonical payload
    sig = operator_sk.sign(canonical_envelope_payload(envelope))
    if tamper_signature:
        sig = bytes(b ^ 0xFF for b in sig)
    # Rebuild envelope with real signature (frozen dataclass).
    return SignedBatchEnvelope(
        batch_id=envelope.batch_id,
        compose_run_id=envelope.compose_run_id,
        grant_id=envelope.grant_id,
        org_slug=envelope.org_slug,
        period_n=envelope.period_n,
        batch_status=envelope.batch_status,
        batch_content_sha3_512=envelope.batch_content_sha3_512,
        batch_manifest_sha3_512=envelope.batch_manifest_sha3_512,
        approved_recipient_order=envelope.approved_recipient_order,
        per_recipient_consent_state_sha3_512_full=envelope.per_recipient_consent_state_sha3_512_full,
        signed_at_utc=envelope.signed_at_utc,
        signed_by=envelope.signed_by,
        signature=sig,
    )


class _FakeChannel:
    """Minimal ChannelProtocol-compatible recorder for the dispatcher."""

    def __init__(self, *, channel_name: str = "email", outcome: str = "ok"):
        self.channel_name = channel_name
        self.send_calls: list[OutboundMessage] = []
        self._outcome = outcome

    def compose_outbound(self, **kwargs):
        raise NotImplementedError  # dispatcher never invokes compose

    def parse_inbound(self, **kwargs):
        raise NotImplementedError

    def validate_inbound_token(self, **kwargs):
        raise NotImplementedError

    def send(self, *, message, operator_batch_signature):
        self.send_calls.append(message)
        if self._outcome == "ok":
            return {"sent": True, "outbound_id": message.outbound_id, "provider": "fake"}
        return {"sent": False, "reason": self._outcome, "outbound_id": message.outbound_id}


# ---------------------------------------------------------------------------
# Layer-2 Ed25519 signature verification
# ---------------------------------------------------------------------------


def test_signature_invalid_blanket_fail_no_transport_invoked(
    operator_keypair, recipient_keypair, ledger_root
):
    operator_sk, operator_pk = operator_keypair
    _, recipient_pk = recipient_keypair
    entry = _make_consent_entry()
    write_entry(ledger_root, entry)
    consent_hash = compute_consent_state_hash(entry)
    envelope = _make_signed_batch(
        operator_sk=operator_sk,
        recipient_ids=["r_001"],
        consent_state_hashes={"r_001": consent_hash},
        tamper_signature=True,
    )
    msg = _make_outbound_message()
    channel = _FakeChannel()
    results = dispatch_after_operator_approval(
        signed_batch=envelope,
        outbound_messages=[msg],
        channel_registry={"email": channel},
        operator_public_key=operator_pk,
        per_recipient_public_keys={"r_001": recipient_pk},
        consent_ledger_root=ledger_root,
    )
    assert len(results) == 1
    assert results[0].sent is False
    assert results[0].reason == "operator_signature_invalid"
    assert channel.send_calls == []


def test_batch_status_unsigned_blanket_fail(
    operator_keypair, recipient_keypair, ledger_root
):
    operator_sk, operator_pk = operator_keypair
    _, recipient_pk = recipient_keypair
    entry = _make_consent_entry()
    write_entry(ledger_root, entry)
    consent_hash = compute_consent_state_hash(entry)
    envelope = _make_signed_batch(
        operator_sk=operator_sk,
        recipient_ids=["r_001"],
        consent_state_hashes={"r_001": consent_hash},
        batch_status="UNSIGNED",
    )
    msg = _make_outbound_message()
    channel = _FakeChannel()
    results = dispatch_after_operator_approval(
        signed_batch=envelope,
        outbound_messages=[msg],
        channel_registry={"email": channel},
        operator_public_key=operator_pk,
        per_recipient_public_keys={"r_001": recipient_pk},
        consent_ledger_root=ledger_root,
    )
    assert results[0].reason == "batch_status_not_approved_for_send"
    assert channel.send_calls == []


# ---------------------------------------------------------------------------
# Per-recipient signature + grant/org binding
# ---------------------------------------------------------------------------


def _sign_message(message: OutboundMessage, sk: Ed25519PrivateKey) -> OutboundMessage:
    payload = canonical_outbound_message_payload(message)
    sig = sk.sign(payload)
    return OutboundMessage(
        outbound_id=message.outbound_id,
        dc_run_id=message.dc_run_id,
        recipient_id=message.recipient_id,
        channel=message.channel,
        grant_id=message.grant_id,
        org_slug=message.org_slug,
        commitment_id_or_funder_reporting_field_id=message.commitment_id_or_funder_reporting_field_id,
        rendered_message_bytes_sha3_512=message.rendered_message_bytes_sha3_512,
        per_state_disclaimers_applied=message.per_state_disclaimers_applied,
        per_recipient_token_id=message.per_recipient_token_id,
        staged_at_utc=message.staged_at_utc,
        sent_at_utc=message.sent_at_utc,
        per_recipient_signature=sig,
    )


def test_per_recipient_signature_invalid_rejected(
    operator_keypair, recipient_keypair, ledger_root
):
    operator_sk, operator_pk = operator_keypair
    _, recipient_pk = recipient_keypair
    entry = _make_consent_entry()
    write_entry(ledger_root, entry)
    consent_hash = compute_consent_state_hash(entry)
    envelope = _make_signed_batch(
        operator_sk=operator_sk,
        recipient_ids=["r_001"],
        consent_state_hashes={"r_001": consent_hash},
    )
    msg = _make_outbound_message(per_recipient_signature=b"\xFF" * 64)
    channel = _FakeChannel()
    results = dispatch_after_operator_approval(
        signed_batch=envelope,
        outbound_messages=[msg],
        channel_registry={"email": channel},
        operator_public_key=operator_pk,
        per_recipient_public_keys={"r_001": recipient_pk},
        consent_ledger_root=ledger_root,
    )
    assert results[0].reason == "per_recipient_signature_invalid"
    assert channel.send_calls == []


def test_grant_id_mismatch_recipient_fails(
    operator_keypair, recipient_keypair, ledger_root
):
    operator_sk, operator_pk = operator_keypair
    recipient_sk, recipient_pk = recipient_keypair
    entry = _make_consent_entry()
    write_entry(ledger_root, entry)
    consent_hash = compute_consent_state_hash(entry)
    envelope = _make_signed_batch(
        operator_sk=operator_sk,
        recipient_ids=["r_001"],
        consent_state_hashes={"r_001": consent_hash},
        grant_id="g_001",
    )
    # Message references different grant_id
    raw_msg = _make_outbound_message(grant_id="g_002")
    msg = _sign_message(raw_msg, recipient_sk)
    channel = _FakeChannel()
    results = dispatch_after_operator_approval(
        signed_batch=envelope,
        outbound_messages=[msg],
        channel_registry={"email": channel},
        operator_public_key=operator_pk,
        per_recipient_public_keys={"r_001": recipient_pk},
        consent_ledger_root=ledger_root,
    )
    assert results[0].reason == "operator_signature_grant_or_org_mismatch"
    assert channel.send_calls == []


def test_per_recipient_signature_replay_across_grants_rejected(
    operator_keypair, recipient_keypair, ledger_root
):
    """RT-C2-01: signature for grant A presented in grant-B batch is rejected."""
    operator_sk, operator_pk = operator_keypair
    recipient_sk, recipient_pk = recipient_keypair
    entry = _make_consent_entry()
    write_entry(ledger_root, entry)
    consent_hash = compute_consent_state_hash(entry)
    # Sign for grant A
    raw_msg_a = _make_outbound_message(grant_id="g_A")
    signed_a = _sign_message(raw_msg_a, recipient_sk)
    # Tamper: switch grant_id but reuse signature
    replayed = OutboundMessage(
        outbound_id=signed_a.outbound_id,
        dc_run_id=signed_a.dc_run_id,
        recipient_id=signed_a.recipient_id,
        channel=signed_a.channel,
        grant_id="g_B",  # cross-grant replay
        org_slug=signed_a.org_slug,
        commitment_id_or_funder_reporting_field_id=signed_a.commitment_id_or_funder_reporting_field_id,
        rendered_message_bytes_sha3_512=signed_a.rendered_message_bytes_sha3_512,
        per_state_disclaimers_applied=signed_a.per_state_disclaimers_applied,
        per_recipient_token_id=signed_a.per_recipient_token_id,
        staged_at_utc=signed_a.staged_at_utc,
        sent_at_utc=signed_a.sent_at_utc,
        per_recipient_signature=signed_a.per_recipient_signature,
    )
    envelope = _make_signed_batch(
        operator_sk=operator_sk,
        recipient_ids=["r_001"],
        consent_state_hashes={"r_001": consent_hash},
        grant_id="g_B",
    )
    channel = _FakeChannel()
    results = dispatch_after_operator_approval(
        signed_batch=envelope,
        outbound_messages=[replayed],
        channel_registry={"email": channel},
        operator_public_key=operator_pk,
        per_recipient_public_keys={"r_001": recipient_pk},
        consent_ledger_root=ledger_root,
    )
    # Caught at the per-recipient signature check (recomputed canonical-JSON
    # binds grant_id+org_slug differently from the original signature payload).
    assert results[0].reason == "per_recipient_signature_invalid"
    assert channel.send_calls == []


# ---------------------------------------------------------------------------
# RT-01 — send-time consent drift
# ---------------------------------------------------------------------------


def test_send_time_consent_drift_aborts_recipient_keeps_remainder(
    operator_keypair, recipient_keypair, ledger_root
):
    operator_sk, operator_pk = operator_keypair
    recipient_sk, recipient_pk = recipient_keypair
    # Compose-time consent: active.
    entry = _make_consent_entry(recipient_id="r_001")
    write_entry(ledger_root, entry)
    consent_hash_compose = compute_consent_state_hash(entry)
    raw_msg = _make_outbound_message(recipient_id="r_001")
    msg = _sign_message(raw_msg, recipient_sk)
    envelope = _make_signed_batch(
        operator_sk=operator_sk,
        recipient_ids=["r_001"],
        consent_state_hashes={"r_001": consent_hash_compose},
    )
    # Between compose and send: recipient opted out.
    opted_out = _make_consent_entry(recipient_id="r_001", opt_out=True)
    write_entry(ledger_root, opted_out)

    channel = _FakeChannel()
    results = dispatch_after_operator_approval(
        signed_batch=envelope,
        outbound_messages=[msg],
        channel_registry={"email": channel},
        operator_public_key=operator_pk,
        per_recipient_public_keys={"r_001": recipient_pk},
        consent_ledger_root=ledger_root,
    )
    assert results[0].reason == "send_time_consent_drift"
    assert results[0].consent_state_hash_at_compose == consent_hash_compose
    assert results[0].consent_state_hash_at_send != consent_hash_compose
    assert channel.send_calls == []


def test_ledger_absent_recipient_fails(
    operator_keypair, recipient_keypair, ledger_root
):
    operator_sk, operator_pk = operator_keypair
    recipient_sk, recipient_pk = recipient_keypair
    raw_msg = _make_outbound_message(recipient_id="r_missing")
    msg = _sign_message(raw_msg, recipient_sk)
    envelope = _make_signed_batch(
        operator_sk=operator_sk,
        recipient_ids=["r_missing"],
        consent_state_hashes={"r_missing": "deadbeef"},
    )
    channel = _FakeChannel()
    results = dispatch_after_operator_approval(
        signed_batch=envelope,
        outbound_messages=[msg],
        channel_registry={"email": channel},
        operator_public_key=operator_pk,
        per_recipient_public_keys={"r_missing": recipient_pk},
        consent_ledger_root=ledger_root,
    )
    assert results[0].reason == "ledger_absent"
    assert channel.send_calls == []


# ---------------------------------------------------------------------------
# RT-C2-12 — approved_recipient_order
# ---------------------------------------------------------------------------


def test_batch_recipient_order_swap_missing_message(
    operator_keypair, recipient_keypair, ledger_root
):
    operator_sk, operator_pk = operator_keypair
    recipient_sk, recipient_pk = recipient_keypair
    entry_a = _make_consent_entry(recipient_id="r_A")
    entry_b = _make_consent_entry(recipient_id="r_B")
    write_entry(ledger_root, entry_a)
    write_entry(ledger_root, entry_b)
    consent_hash_a = compute_consent_state_hash(entry_a)
    consent_hash_b = compute_consent_state_hash(entry_b)
    raw_a = _make_outbound_message(recipient_id="r_A", outbound_id="o_A")
    msg_a = _sign_message(raw_a, recipient_sk)
    # Envelope approves order [r_A, r_B] but only r_A's message supplied.
    envelope = _make_signed_batch(
        operator_sk=operator_sk,
        recipient_ids=["r_A", "r_B"],
        consent_state_hashes={"r_A": consent_hash_a, "r_B": consent_hash_b},
    )
    channel = _FakeChannel()
    results = dispatch_after_operator_approval(
        signed_batch=envelope,
        outbound_messages=[msg_a],
        channel_registry={"email": channel},
        operator_public_key=operator_pk,
        per_recipient_public_keys={
            "r_A": recipient_pk,
            "r_B": recipient_pk,
        },
        consent_ledger_root=ledger_root,
    )
    assert [r.recipient_id for r in results] == ["r_A", "r_B"]
    assert results[1].reason == "batch_recipient_order_swap"


def test_results_returned_in_approved_recipient_order(
    operator_keypair, recipient_keypair, ledger_root
):
    operator_sk, operator_pk = operator_keypair
    recipient_sk, recipient_pk = recipient_keypair
    consent_hashes: dict[str, str] = {}
    messages: list[OutboundMessage] = []
    for rid in ("r_03", "r_01", "r_02"):
        entry = _make_consent_entry(recipient_id=rid)
        write_entry(ledger_root, entry)
        consent_hashes[rid] = compute_consent_state_hash(entry)
        raw = _make_outbound_message(recipient_id=rid, outbound_id=f"o_{rid}")
        messages.append(_sign_message(raw, recipient_sk))
    # Approved order is deliberately not the message list order:
    envelope = _make_signed_batch(
        operator_sk=operator_sk,
        recipient_ids=["r_01", "r_02", "r_03"],
        consent_state_hashes=consent_hashes,
    )
    channel = _FakeChannel()
    results = dispatch_after_operator_approval(
        signed_batch=envelope,
        outbound_messages=messages,
        channel_registry={"email": channel},
        operator_public_key=operator_pk,
        per_recipient_public_keys={rid: recipient_pk for rid in consent_hashes},
        consent_ledger_root=ledger_root,
    )
    assert [r.recipient_id for r in results] == ["r_01", "r_02", "r_03"]
    assert [m.recipient_id for m in channel.send_calls] == ["r_01", "r_02", "r_03"]


# ---------------------------------------------------------------------------
# Channel registry
# ---------------------------------------------------------------------------


def test_channel_not_registered_recipient_fails(
    operator_keypair, recipient_keypair, ledger_root
):
    operator_sk, operator_pk = operator_keypair
    recipient_sk, recipient_pk = recipient_keypair
    entry = _make_consent_entry(channel="sms")
    write_entry(ledger_root, entry)
    consent_hash = compute_consent_state_hash(entry)
    raw = _make_outbound_message(channel="sms")
    msg = _sign_message(raw, recipient_sk)
    envelope = _make_signed_batch(
        operator_sk=operator_sk,
        recipient_ids=["r_001"],
        consent_state_hashes={"r_001": consent_hash},
    )
    # No "sms" entry in registry.
    results = dispatch_after_operator_approval(
        signed_batch=envelope,
        outbound_messages=[msg],
        channel_registry={"email": _FakeChannel(channel_name="email")},
        operator_public_key=operator_pk,
        per_recipient_public_keys={"r_001": recipient_pk},
        consent_ledger_root=ledger_root,
    )
    assert results[0].reason == "channel_not_registered"


# ---------------------------------------------------------------------------
# Happy path + lock-hold-through-transport (RT-C2-05)
# ---------------------------------------------------------------------------


def test_happy_path_send_called_with_message_and_envelope(
    operator_keypair, recipient_keypair, ledger_root
):
    operator_sk, operator_pk = operator_keypair
    recipient_sk, recipient_pk = recipient_keypair
    entry = _make_consent_entry()
    write_entry(ledger_root, entry)
    consent_hash = compute_consent_state_hash(entry)
    raw = _make_outbound_message()
    msg = _sign_message(raw, recipient_sk)
    envelope = _make_signed_batch(
        operator_sk=operator_sk,
        recipient_ids=["r_001"],
        consent_state_hashes={"r_001": consent_hash},
    )
    channel = _FakeChannel()
    results = dispatch_after_operator_approval(
        signed_batch=envelope,
        outbound_messages=[msg],
        channel_registry={"email": channel},
        operator_public_key=operator_pk,
        per_recipient_public_keys={"r_001": recipient_pk},
        consent_ledger_root=ledger_root,
    )
    assert results[0].sent is True
    assert results[0].reason is None
    assert results[0].consent_state_hash_at_compose == consent_hash
    assert results[0].consent_state_hash_at_send == consent_hash
    assert len(channel.send_calls) == 1
    assert channel.send_calls[0].outbound_id == "o_001"


class _LockObservingChannel:
    """Channel whose .send() checks that the ledger lock is held during call."""

    channel_name = "email"

    def __init__(self, ledger_root: Path, recipient_id: str, channel: str):
        self.ledger_root = ledger_root
        self.recipient_id = recipient_id
        self.channel = channel
        self.lock_was_blocking_during_send: Optional[bool] = None

    def compose_outbound(self, **kwargs):
        raise NotImplementedError

    def parse_inbound(self, **kwargs):
        raise NotImplementedError

    def validate_inbound_token(self, **kwargs):
        raise NotImplementedError

    def send(self, *, message, operator_batch_signature):
        # Probe the lock state while the dispatcher is holding it.
        import errno
        import fcntl
        path = (
            self.ledger_root
            / f"{self.recipient_id}__{self.channel}.yaml"
        )
        with open(path, "rb") as fp:
            try:
                fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                # Was acquired without blocking — dispatcher NOT holding lock.
                fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
                self.lock_was_blocking_during_send = False
            except OSError as exc:
                if exc.errno in (errno.EWOULDBLOCK, errno.EAGAIN):
                    self.lock_was_blocking_during_send = True
                else:
                    raise
        return {"sent": True, "outbound_id": message.outbound_id}


def test_lock_held_through_transport_call(
    operator_keypair, recipient_keypair, ledger_root
):
    """RT-C2-05: the per-recipient consent ledger LOCK_EX is held while
    transport ``send()`` is invoked (no TOCTOU window between re-read and send).
    """
    operator_sk, operator_pk = operator_keypair
    recipient_sk, recipient_pk = recipient_keypair
    entry = _make_consent_entry()
    write_entry(ledger_root, entry)
    consent_hash = compute_consent_state_hash(entry)
    raw = _make_outbound_message()
    msg = _sign_message(raw, recipient_sk)
    envelope = _make_signed_batch(
        operator_sk=operator_sk,
        recipient_ids=["r_001"],
        consent_state_hashes={"r_001": consent_hash},
    )
    observer = _LockObservingChannel(ledger_root, "r_001", "email")
    results = dispatch_after_operator_approval(
        signed_batch=envelope,
        outbound_messages=[msg],
        channel_registry={"email": observer},
        operator_public_key=operator_pk,
        per_recipient_public_keys={"r_001": recipient_pk},
        consent_ledger_root=ledger_root,
    )
    assert results[0].sent is True
    assert observer.lock_was_blocking_during_send is True


# ---------------------------------------------------------------------------
# Canonical-JSON envelopes — stable encoding
# ---------------------------------------------------------------------------


def test_canonical_envelope_payload_sort_keys_stable(operator_keypair):
    sk, _ = operator_keypair
    envelope = _make_signed_batch(
        operator_sk=sk,
        recipient_ids=["r_B", "r_A"],  # order preserved in approved_recipient_order
        consent_state_hashes={"r_B": "h_B", "r_A": "h_A"},
    )
    payload = canonical_envelope_payload(envelope)
    parsed = json.loads(payload)
    # approved_recipient_order is a list — original order preserved.
    assert parsed["approved_recipient_order"] == ["r_B", "r_A"]
    # per_recipient_consent_state_sha3_512_full is a dict — keys sorted.
    payload_str = payload.decode("utf-8")
    consent_segment = payload_str[
        payload_str.index("per_recipient_consent_state_sha3_512_full"):
        payload_str.index("period_n")
    ]
    assert consent_segment.index('"r_A"') < consent_segment.index('"r_B"')
    # Re-encoding the same envelope produces identical bytes.
    assert canonical_envelope_payload(envelope) == payload


def test_canonical_outbound_message_payload_includes_grant_and_org():
    msg = _make_outbound_message(grant_id="g_999", org_slug="o_zzz")
    payload = canonical_outbound_message_payload(msg)
    parsed = json.loads(payload)
    assert parsed["grant_id"] == "g_999"
    assert parsed["org_slug"] == "o_zzz"
    assert "per_recipient_signature" not in parsed
    assert "sent_at_utc" not in parsed
