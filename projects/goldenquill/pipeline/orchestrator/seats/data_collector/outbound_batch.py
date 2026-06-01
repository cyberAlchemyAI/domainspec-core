"""§13.4.2 + §13.7 — Operator-approved outbound batch dispatcher.

Per §13 Data Collector v1 LOCKED 2026-05-10.

This is the single dispatch surface for the entire Data Collector outbound
path. Channel modules expose ``send(...)`` but AST-lint
``R-DATACOLLECTOR-NO-AUTOSEND`` (Slice 3) statically forbids any module other
than ``outbound_batch.dispatch_after_operator_approval`` from invoking
``<channel>_channel.send(...)``. The four-layer defense pattern from §13.7:

1. **Layer 1 — AST-lint** (compile-time; ``R-DATACOLLECTOR-NO-AUTOSEND``, Slice 3).
2. **Layer 2 — Dispatcher signature check** (this module): Ed25519 verify the
   ``signed_batch`` envelope at function entry; signature-invalid →
   ``SendResult{sent=False, reason="operator_signature_invalid"}`` for EVERY
   recipient; no transport substrate invoked.
3. **Layer 3 — Cedar policy** (``data_collector_send.cedar``; Slice 3 engine
   bootstrap finalizes the policy attribute).
4. **Layer 4 — TTY check** (CLI argparse rejects ``--yes``/``--force``;
   landed in operator approval surface, not this module).

The dispatcher additionally enforces every Cycle-1/Cycle-2 closure that lives
in the send path:

- **RT-01 (send-time consent drift):** per-recipient consent ledger row
  re-read from disk IMMEDIATELY before the transport call; ``compute_consent_state_hash``
  compared against ``signed_batch.per_recipient_consent_state_sha3_512_full[recipient_id]``;
  mismatch → ``send_time_consent_drift``.
- **RT-C2-05 (lock-hold-through-transport):** the fcntl.flock(LOCK_EX) on the
  per-recipient consent ledger entry is held THROUGH the transport substrate
  call (no release between re-read and send). 30s timeout per recipient;
  timeout → ``transport_timeout_during_send_lock_hold``.
- **RT-14 (per-recipient signature):** every outbound message in the batch
  carries its own per-recipient Ed25519 signature over canonical-JSON of the
  ``OutboundMessage`` record; verified at PRE-per-recipient-send.
- **RT-C2-01 (grant_id+org_slug binding):** the per-recipient signed canonical-JSON
  MUST carry ``grant_id`` + ``org_slug`` matching the invocation; mismatch →
  ``per_recipient_signature_grant_or_org_mismatch``.
- **RT-C2-12 (approved_recipient_order):** the dispatch order MUST match
  ``signed_batch.approved_recipient_order``; deviation →
  ``batch_recipient_order_swap``.

The Ed25519 verification uses the ``cryptography`` library (canonical for the
project per ``sub_awardee_token.py``). Signature blobs are 64 bytes (Ed25519).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Optional, Sequence

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from pipeline.orchestrator.seats.data_collector import (
    ChannelProtocol,
    ConsentLedgerEntry,
    OutboundMessage,
    SendResult,
    SignedBatchEnvelope,
)
from pipeline.orchestrator.seats.data_collector.consent_ledger import (
    LedgerLockTimeout,
    compute_consent_state_hash,
    locked_read_entry,
)


SEND_LOCK_TIMEOUT_SECONDS: int = 30  # RT-C2-05


# ---------------------------------------------------------------------------
# Canonical-JSON envelopes (signing surface)
# ---------------------------------------------------------------------------


def canonical_envelope_payload(envelope: SignedBatchEnvelope) -> bytes:
    """Canonical bytes for the batch-envelope signature.

    The signed payload covers every batch-level field that is structurally
    load-bearing — batch identifier, compose run id, grant id, org slug,
    period, status, content hash, manifest hash, approved order, per-recipient
    consent hashes, sign-time. The ``signature`` and ``signed_by`` fields are
    explicitly excluded (the former is the signature, the latter is the key
    identifier used to resolve the public key).
    """
    payload = {
        "batch_id": envelope.batch_id,
        "compose_run_id": envelope.compose_run_id,
        "grant_id": envelope.grant_id,
        "org_slug": envelope.org_slug,
        "period_n": envelope.period_n,
        "batch_status": envelope.batch_status,
        "batch_content_sha3_512": envelope.batch_content_sha3_512,
        "batch_manifest_sha3_512": envelope.batch_manifest_sha3_512,
        "approved_recipient_order": list(envelope.approved_recipient_order),
        "per_recipient_consent_state_sha3_512_full": dict(
            envelope.per_recipient_consent_state_sha3_512_full,
        ),
        "signed_at_utc": envelope.signed_at_utc.isoformat(),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_outbound_message_payload(message: OutboundMessage) -> bytes:
    """Canonical bytes for the per-recipient Ed25519 signature.

    Per RT-14 + RT-C2-01 the per-recipient signed canonical-JSON MUST include
    ``grant_id`` + ``org_slug`` + ``rendered_message_bytes_sha3_512`` + per-recipient
    identifiers. The ``per_recipient_signature`` and ``sent_at_utc`` fields are
    excluded (the former is the signature, the latter is set after send).
    """
    payload = {
        "outbound_id": message.outbound_id,
        "dc_run_id": message.dc_run_id,
        "recipient_id": message.recipient_id,
        "channel": message.channel,
        "grant_id": message.grant_id,
        "org_slug": message.org_slug,
        "commitment_id_or_funder_reporting_field_id": (
            message.commitment_id_or_funder_reporting_field_id
        ),
        "rendered_message_bytes_sha3_512": message.rendered_message_bytes_sha3_512,
        "per_state_disclaimers_applied": list(message.per_state_disclaimers_applied),
        "per_recipient_token_id": message.per_recipient_token_id,
        "staged_at_utc": message.staged_at_utc.isoformat(),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _verify_ed25519(public_key: Ed25519PublicKey, signature: bytes, payload: bytes) -> bool:
    """Wrapper around Ed25519PublicKey.verify; returns bool."""
    if not isinstance(signature, (bytes, bytearray)) or len(signature) != 64:
        return False
    try:
        public_key.verify(bytes(signature), payload)
    except InvalidSignature:
        return False
    return True


def _failure_for_every_recipient(
    *,
    envelope: SignedBatchEnvelope,
    messages_by_recipient: Mapping[str, OutboundMessage],
    reason: str,
) -> list[SendResult]:
    """Layer-2 fail-closed: blanket fail every approved recipient on envelope-level rejection."""
    results: list[SendResult] = []
    for recipient_id in envelope.approved_recipient_order:
        message = messages_by_recipient.get(recipient_id)
        if message is None:
            results.append(
                SendResult(
                    outbound_id="",
                    recipient_id=recipient_id,
                    channel="email",  # placeholder; never reached on real send
                    sent=False,
                    reason=reason,
                )
            )
            continue
        results.append(
            SendResult(
                outbound_id=message.outbound_id,
                recipient_id=recipient_id,
                channel=message.channel,
                sent=False,
                reason=reason,
            )
        )
    return results


# ---------------------------------------------------------------------------
# Operator-approved batch dispatcher
# ---------------------------------------------------------------------------


def dispatch_after_operator_approval(
    *,
    signed_batch: SignedBatchEnvelope,
    outbound_messages: Sequence[OutboundMessage],
    channel_registry: Mapping[str, ChannelProtocol],
    operator_public_key: Ed25519PublicKey,
    per_recipient_public_keys: Mapping[str, Ed25519PublicKey],
    consent_ledger_root: Path,
    send_lock_timeout_seconds: int = SEND_LOCK_TIMEOUT_SECONDS,
) -> list[SendResult]:
    """Layer-2 + RT-01/RT-C2-05/RT-14/RT-C2-01/RT-C2-12 closure surface.

    Per §13.4.2 invariants + §13.7 four-layer defense.

    Args:
        signed_batch: operator-Ed25519-signed batch envelope.
        outbound_messages: per-recipient ``OutboundMessage`` records; must
            cover every recipient_id in ``signed_batch.approved_recipient_order``.
        channel_registry: mapping ``channel_name -> ChannelProtocol``.
        operator_public_key: operator's Ed25519 verification key (pinned at
            white-glove).
        per_recipient_public_keys: per-recipient Ed25519 verification keys; if
            a single operator signed every recipient, supply the same key per
            recipient_id (the schema permits per-recipient signing keys for
            multi-operator orgs at v1.x).
        consent_ledger_root: per-org consent_ledger directory; resolved per
            ``orgs/<slug>/data_collector/consent_ledger/``.
        send_lock_timeout_seconds: per-recipient lock-hold timeout (default 30s
            per RT-C2-05).

    Returns:
        list[SendResult] — one entry per recipient in dispatch order. Per
        ``approved_recipient_order``; never reordered.

    Layer-2 contract:
        - operator signature invalid → blanket
          ``SendResult{sent=False, reason="operator_signature_invalid"}`` for
          every approved recipient; transport substrate NOT invoked.
        - ``batch_status != "APPROVED_FOR_SEND"`` → blanket
          ``batch_status_not_approved_for_send`` for every approved recipient.
        - ``message.grant_id``/``org_slug`` disagree with envelope → recipient
          specific ``operator_signature_grant_or_org_mismatch`` (defense in
          depth alongside per-recipient signature check).
    """
    messages_by_recipient: dict[str, OutboundMessage] = {
        m.recipient_id: m for m in outbound_messages
    }

    # Layer 2 — batch-status check (PRE-signature; cheap predicate).
    if signed_batch.batch_status != "APPROVED_FOR_SEND":
        return _failure_for_every_recipient(
            envelope=signed_batch,
            messages_by_recipient=messages_by_recipient,
            reason="batch_status_not_approved_for_send",
        )

    # Layer 2 — operator Ed25519 signature verification at function entry.
    envelope_payload = canonical_envelope_payload(signed_batch)
    if not _verify_ed25519(operator_public_key, signed_batch.signature, envelope_payload):
        return _failure_for_every_recipient(
            envelope=signed_batch,
            messages_by_recipient=messages_by_recipient,
            reason="operator_signature_invalid",
        )

    results: list[SendResult] = []

    # RT-C2-12 — dispatch order MUST match approved_recipient_order;
    # iterate in that exact order (no reordering, no implicit sort).
    for recipient_id in signed_batch.approved_recipient_order:
        message = messages_by_recipient.get(recipient_id)
        if message is None:
            results.append(
                SendResult(
                    outbound_id="",
                    recipient_id=recipient_id,
                    channel="email",
                    sent=False,
                    reason="batch_recipient_order_swap",
                )
            )
            continue

        # RT-C2-01 — grant_id + org_slug binding (envelope vs message).
        if (
            message.grant_id != signed_batch.grant_id
            or message.org_slug != signed_batch.org_slug
        ):
            results.append(
                SendResult(
                    outbound_id=message.outbound_id,
                    recipient_id=recipient_id,
                    channel=message.channel,
                    sent=False,
                    reason="operator_signature_grant_or_org_mismatch",
                )
            )
            continue

        # RT-14 + RT-C2-01 — per-recipient signature verification.
        per_recipient_key = per_recipient_public_keys.get(recipient_id)
        if per_recipient_key is None:
            results.append(
                SendResult(
                    outbound_id=message.outbound_id,
                    recipient_id=recipient_id,
                    channel=message.channel,
                    sent=False,
                    reason="per_recipient_signature_invalid",
                )
            )
            continue
        per_recipient_payload = canonical_outbound_message_payload(message)
        if not _verify_ed25519(
            per_recipient_key,
            message.per_recipient_signature,
            per_recipient_payload,
        ):
            results.append(
                SendResult(
                    outbound_id=message.outbound_id,
                    recipient_id=recipient_id,
                    channel=message.channel,
                    sent=False,
                    reason="per_recipient_signature_invalid",
                )
            )
            continue

        # Channel dispatch — channel must be registered.
        channel_impl = channel_registry.get(message.channel)
        if channel_impl is None:
            results.append(
                SendResult(
                    outbound_id=message.outbound_id,
                    recipient_id=recipient_id,
                    channel=message.channel,
                    sent=False,
                    reason="channel_not_registered",
                )
            )
            continue

        # RT-01 + RT-C2-05 — lock-hold-through-transport.
        # The lock is acquired on the per-recipient consent ledger entry; the
        # transport call happens with the lock HELD; the lock releases when
        # the context manager exits (after the transport returns or raises).
        signed_consent_hash = signed_batch.per_recipient_consent_state_sha3_512_full.get(
            recipient_id
        )
        try:
            with locked_read_entry(
                consent_ledger_root,
                recipient_id,
                message.channel,
                timeout_seconds=send_lock_timeout_seconds,
            ) as live_entry:
                if live_entry is None:
                    results.append(
                        SendResult(
                            outbound_id=message.outbound_id,
                            recipient_id=recipient_id,
                            channel=message.channel,
                            sent=False,
                            reason="ledger_absent",
                            consent_state_hash_at_compose=signed_consent_hash,
                            consent_state_hash_at_send=None,
                        )
                    )
                    continue
                live_hash = compute_consent_state_hash(live_entry)
                if signed_consent_hash != live_hash:
                    results.append(
                        SendResult(
                            outbound_id=message.outbound_id,
                            recipient_id=recipient_id,
                            channel=message.channel,
                            sent=False,
                            reason="send_time_consent_drift",
                            consent_state_hash_at_compose=signed_consent_hash,
                            consent_state_hash_at_send=live_hash,
                        )
                    )
                    continue

                # Lock is held; transport substrate invoked with operator
                # batch envelope alongside per-recipient OutboundMessage.
                provider_response = channel_impl.send(
                    message=message,
                    operator_batch_signature=signed_batch,
                )
                sent_flag = bool(provider_response.get("sent", False))
                reason = provider_response.get("reason") if not sent_flag else None
                results.append(
                    SendResult(
                        outbound_id=message.outbound_id,
                        recipient_id=recipient_id,
                        channel=message.channel,
                        sent=sent_flag,
                        reason=reason,
                        provider_response=dict(provider_response),
                        consent_state_hash_at_compose=signed_consent_hash,
                        consent_state_hash_at_send=live_hash,
                    )
                )
        except LedgerLockTimeout:
            results.append(
                SendResult(
                    outbound_id=message.outbound_id,
                    recipient_id=recipient_id,
                    channel=message.channel,
                    sent=False,
                    reason="transport_timeout_during_send_lock_hold",
                    consent_state_hash_at_compose=signed_consent_hash,
                )
            )

    return results


__all__ = [
    "SEND_LOCK_TIMEOUT_SECONDS",
    "canonical_envelope_payload",
    "canonical_outbound_message_payload",
    "dispatch_after_operator_approval",
]
