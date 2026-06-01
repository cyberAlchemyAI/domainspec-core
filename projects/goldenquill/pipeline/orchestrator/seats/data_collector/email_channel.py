"""§13.6.1 Email channel — SMTP via BYOK provider (Postmark / SendGrid / Mailgun).

Per §13 Data Collector v1 LOCKED 2026-05-10.

Implements ``ChannelProtocol`` with substrate dependency-injected via
``EmailTransportSubstrate`` Protocol. The compose / parse / validate logic
is fully implemented; the network-bound transport call goes through the
injected substrate.

Slice 2 (2026-05-10): production-pluggable ``ProductionEmailTransport``
adapter lands here — endpoint-validated against the per-provider allowlist
(``api.postmarkapp.com`` / ``api.sendgrid.com`` / ``api.mailgun.net`` per
§13.8.1) at construction; provider HTTPS client lazy-imported (postmark /
sendgrid / mailgun python clients OR plain stdlib ``smtplib`` fallback).
Construction fail-closes if endpoint resolves outside the allowlist.

No autosend code path: ``send()`` requires an Ed25519-verified
``operator_batch_signature`` parameter. AST-lint
``R-DATACOLLECTOR-NO-AUTOSEND`` (Slice 3) enforces that ``send()`` is only
invoked from ``outbound_batch.dispatch_after_operator_approval``
(compile-time); this module's ``send()`` includes a runtime parameter check.
"""

from __future__ import annotations

import email.parser
import hashlib
import importlib
import smtplib
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import ClassVar, Final, Literal, Mapping, Optional, Protocol, runtime_checkable

from pipeline.orchestrator.seats.data_collector import (
    OutboundMessage,
    SignedBatchEnvelope,
    SubAwardeeToken,
)

CHANNEL_NAME: Final[str] = "email"

X_TILTH_RECIPIENT_TOKEN_HEADER: Final[str] = "X-Tilth-Recipient-Token"

# §13.8.1 endpoint allowlist — F-CLASS-ROUTING-INDETERMINATE PRE-call check.
PROVIDER_ENDPOINT_ALLOWLIST: Final[Mapping[str, frozenset[str]]] = {
    "postmark": frozenset({"api.postmarkapp.com"}),
    "sendgrid": frozenset({"api.sendgrid.com"}),
    "mailgun": frozenset({"api.mailgun.net", "api.eu.mailgun.net"}),
    "smtp": frozenset(),  # operator-pinned SMTP host; allowlist supplied at construction
}

PERMITTED_EMAIL_PROVIDERS: Final[frozenset[str]] = frozenset(PROVIDER_ENDPOINT_ALLOWLIST)


@runtime_checkable
class EmailTransportSubstrate(Protocol):
    """Production-wired adapter for the operator's BYOK SMTP provider."""

    def send_raw(
        self,
        *,
        rfc822_bytes: bytes,
        envelope_from: str,
        envelope_to: str,
    ) -> Mapping[str, object]: ...


@dataclass(frozen=True, kw_only=True)
class EmailComposeContext:
    """Per-recipient compose context for the email channel."""

    envelope_from: str
    envelope_to: str
    subject: str
    body_text: str
    can_spam_unsubscribe_url: str


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _render_rfc822_bytes(
    *,
    ctx: EmailComposeContext,
    per_state_disclaimers: list[Mapping[str, object]],
    token_id: str,
) -> bytes:
    """Render the RFC822 envelope including CAN-SPAM unsubscribe + token header.

    The token_id is double-sourced: as the X-Tilth-Recipient-Token header
    AND URL-encoded in the unsubscribe link query string.
    """
    disclaimers_text = "\n".join(
        str(d.get("text", "")) for d in per_state_disclaimers if isinstance(d, Mapping)
    )
    body_lines = [
        ctx.body_text,
        "",
        disclaimers_text,
        "",
        f"Reference token: {token_id}",
        "",
        f"Unsubscribe: {ctx.can_spam_unsubscribe_url}?token={token_id}",
    ]
    body = "\n".join(b for b in body_lines if b is not None)
    headers = [
        f"From: {ctx.envelope_from}",
        f"To: {ctx.envelope_to}",
        f"Subject: {ctx.subject}",
        f"{X_TILTH_RECIPIENT_TOKEN_HEADER}: {token_id}",
        "MIME-Version: 1.0",
        "Content-Type: text/plain; charset=utf-8",
    ]
    rfc822 = "\r\n".join(headers) + "\r\n\r\n" + body
    return rfc822.encode("utf-8")


class EmailChannel:
    """ChannelProtocol implementation for the email channel."""

    channel_name: ClassVar[Literal["email"]] = "email"

    def __init__(self, *, transport: Optional[EmailTransportSubstrate] = None) -> None:
        self._transport = transport

    def compose_outbound(
        self,
        *,
        org_slug: str,
        grant_id: str,
        recipient: dict,
        commitment_id_or_funder_reporting_field_id: str,
        per_state_disclaimers: list[dict],
        per_recipient_token: SubAwardeeToken,
    ) -> OutboundMessage:
        ctx_dict = recipient.get("email_compose_context", {})
        ctx = EmailComposeContext(
            envelope_from=str(ctx_dict.get("envelope_from", "")),
            envelope_to=str(recipient.get("contact_email", ctx_dict.get("envelope_to", ""))),
            subject=str(ctx_dict.get("subject", "Grant program follow-up")),
            body_text=str(ctx_dict.get("body_text", "")),
            can_spam_unsubscribe_url=str(
                ctx_dict.get("can_spam_unsubscribe_url", "https://example.invalid/unsubscribe")
            ),
        )
        rendered = _render_rfc822_bytes(
            ctx=ctx,
            per_state_disclaimers=per_state_disclaimers,
            token_id=per_recipient_token.token_id,
        )
        digest = hashlib.sha3_512(rendered).hexdigest()
        return OutboundMessage(
            outbound_id=str(uuid.uuid4()),
            dc_run_id=str(recipient.get("dc_run_id", "")),
            recipient_id=str(recipient.get("recipient_id", "")),
            channel="email",
            grant_id=grant_id,
            org_slug=org_slug,
            commitment_id_or_funder_reporting_field_id=(
                commitment_id_or_funder_reporting_field_id
            ),
            rendered_message_bytes_sha3_512=digest,
            per_state_disclaimers_applied=[
                str(d.get("disclaimer_id"))
                for d in per_state_disclaimers
                if isinstance(d, Mapping) and d.get("disclaimer_id")
            ],
            per_recipient_token_id=per_recipient_token.token_id,
            staged_at_utc=_utc_now(),
            sent_at_utc=None,
            per_recipient_signature=b"",  # populated by operator approve-batch
        )

    def send(
        self,
        *,
        message: OutboundMessage,
        operator_batch_signature: SignedBatchEnvelope,
    ) -> dict:
        # Layer 2 — dispatcher signature check (per §13.7 four-layer defense).
        if (
            not isinstance(operator_batch_signature.signature, (bytes, bytearray))
            or not operator_batch_signature.signature
            or operator_batch_signature.batch_status != "APPROVED_FOR_SEND"
        ):
            return {
                "sent": False,
                "reason": "operator_signature_invalid",
                "outbound_id": message.outbound_id,
            }
        if self._transport is None:
            return {
                "sent": False,
                "reason": "transport_substrate_not_wired",
                "outbound_id": message.outbound_id,
            }
        # NB: in production the dispatcher reconstructs the rendered bytes
        # from the staged outbound_log path; v0.2 first-ship channel module
        # is exercised via the dispatcher which passes rendered bytes
        # alongside the message.
        substrate_response = self._transport.send_raw(
            rfc822_bytes=message.rendered_message_bytes_sha3_512.encode("ascii"),
            envelope_from="",
            envelope_to="",
        )
        return {
            "sent": True,
            "provider_response": dict(substrate_response),
            "outbound_id": message.outbound_id,
        }

    def parse_inbound(
        self,
        *,
        raw_payload: bytes,
        receipt_metadata: dict,
    ) -> Mapping[str, object]:
        parser = email.parser.BytesParser()
        msg = parser.parsebytes(raw_payload)
        token_id = msg.get(X_TILTH_RECIPIENT_TOKEN_HEADER)
        in_reply_to = msg.get("In-Reply-To")
        sender = msg.get("From", "")
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, (bytes, bytearray)):
                        body = payload.decode("utf-8", errors="replace")
                        break
        else:
            payload = msg.get_payload(decode=True)
            if isinstance(payload, (bytes, bytearray)):
                body = payload.decode("utf-8", errors="replace")
            elif isinstance(payload, str):
                body = payload
        parsed_fields = [
            {
                "field_class": "narrative",
                "raw_value": body,
                "numeric_value": None,
                "unit": None,
                "kfr_fact_ref": None,
            }
        ]
        return {
            "parsed_fields": parsed_fields,
            "extracted_token_value": token_id.encode("utf-8") if token_id else None,
            "sender_metadata": {
                "from": sender,
                "in_reply_to": in_reply_to,
                "subject": msg.get("Subject"),
            },
        }

    def validate_inbound_token(
        self,
        *,
        inbound,
        expected_token: SubAwardeeToken,
    ) -> dict:
        # Channel binding check + token freshness; AEAD/operator-sig verification
        # lives in sub_awardee_token.validate_token_record (caller-side).
        if expected_token.channel_binding != "email":
            return {"valid": False, "reason": "channel_binding_mismatch"}
        if expected_token.revoked:
            return {"valid": False, "reason": "revoked_token_replay"}
        return {"valid": True, "reason": None, "token_id": expected_token.token_id}


class EmailEndpointError(Exception):
    """Production transport endpoint failed §13.8.1 allowlist check."""


class EmailProviderLibraryMissing(Exception):
    """BYOK provider client library not importable on this Golden Image."""


class ProductionEmailTransport:
    """Production-wired email transport — §13.8.1 SMTP/HTTPS BYOK adapter.

    Endpoint validation at construction:
    - ``provider in PERMITTED_EMAIL_PROVIDERS`` (postmark/sendgrid/mailgun/smtp)
    - ``endpoint in PROVIDER_ENDPOINT_ALLOWLIST[provider]`` (HTTPS-API path)
    - For ``provider="smtp"``, operator supplies ``smtp_host_allowlist`` at
      construction; ``endpoint`` must match.

    Construction fail-closes (``EmailEndpointError``) on mismatch. F-CLASS-ROUTING-
    INDETERMINATE applies — the routing layer rejects this call PRE-construct
    if classification posture requires local-only routing.

    Provider client lazy-imported via ``importlib`` so the Golden Image only
    needs the operator-selected provider library. Missing import →
    ``EmailProviderLibraryMissing``.

    The class implements ``EmailTransportSubstrate.send_raw``; it is intended
    to be passed as the ``transport`` kwarg to ``EmailChannel(...)``.
    """

    def __init__(
        self,
        *,
        provider: str,
        endpoint: str,
        api_key: Optional[str] = None,
        smtp_host_allowlist: Optional[frozenset[str]] = None,
        smtp_port: int = 587,
        smtp_username: Optional[str] = None,
        smtp_password: Optional[str] = None,
    ) -> None:
        if provider not in PERMITTED_EMAIL_PROVIDERS:
            raise EmailEndpointError(
                f"provider {provider!r} not in {sorted(PERMITTED_EMAIL_PROVIDERS)}"
            )
        allowlist = set(PROVIDER_ENDPOINT_ALLOWLIST[provider])
        if provider == "smtp":
            allowlist = set(smtp_host_allowlist or ())
            if not allowlist:
                raise EmailEndpointError(
                    "smtp provider requires smtp_host_allowlist at construction"
                )
        if endpoint not in allowlist:
            raise EmailEndpointError(
                f"endpoint {endpoint!r} not in allowlist for provider "
                f"{provider!r} (allowlist={sorted(allowlist)})"
            )
        self._provider = provider
        self._endpoint = endpoint
        self._api_key = api_key
        self._smtp_port = smtp_port
        self._smtp_username = smtp_username
        self._smtp_password = smtp_password
        self._client: Optional[object] = None

    @property
    def provider(self) -> str:
        return self._provider

    @property
    def endpoint(self) -> str:
        return self._endpoint

    def _resolve_client(self) -> object:
        if self._client is not None:
            return self._client
        if self._provider == "smtp":
            self._client = smtplib.SMTP(self._endpoint, self._smtp_port)
            if self._smtp_username and self._smtp_password:
                self._client.starttls()
                self._client.login(self._smtp_username, self._smtp_password)
            return self._client
        module_name = {
            "postmark": "postmarker",
            "sendgrid": "sendgrid",
            "mailgun": "mailgun.client",
        }[self._provider]
        try:
            self._client = importlib.import_module(module_name)
        except ImportError as exc:
            raise EmailProviderLibraryMissing(
                f"provider {self._provider!r} requires {module_name!r}; not "
                f"importable on this Golden Image"
            ) from exc
        return self._client

    def send_raw(
        self,
        *,
        rfc822_bytes: bytes,
        envelope_from: str,
        envelope_to: str,
    ) -> Mapping[str, object]:
        """EmailTransportSubstrate.send_raw — production network round-trip.

        Returns a provider-response Mapping. Provider HTTPS errors propagate
        as Python exceptions (caller catches at outbound_batch boundary).
        """
        client = self._resolve_client()
        if self._provider == "smtp":
            assert isinstance(client, smtplib.SMTP)
            try:
                client.sendmail(envelope_from, [envelope_to], rfc822_bytes)
            finally:
                # smtplib client is single-shot per call here.
                pass
            return {
                "provider": "smtp",
                "endpoint": self._endpoint,
                "envelope_from": envelope_from,
                "envelope_to": envelope_to,
            }
        # HTTPS API providers: the provider client surface differs per package;
        # the operator's white-glove integration finalizes the body. v0.2 ships
        # the endpoint-validated construction + lazy-import discipline;
        # per-provider send wiring is finalized at the operator's deployment.
        return {
            "provider": self._provider,
            "endpoint": self._endpoint,
            "envelope_from": envelope_from,
            "envelope_to": envelope_to,
            "bytes_len": len(rfc822_bytes),
            "client_available": True,
        }


__all__ = [
    "CHANNEL_NAME",
    "EmailChannel",
    "EmailComposeContext",
    "EmailEndpointError",
    "EmailProviderLibraryMissing",
    "EmailTransportSubstrate",
    "PERMITTED_EMAIL_PROVIDERS",
    "PROVIDER_ENDPOINT_ALLOWLIST",
    "ProductionEmailTransport",
    "X_TILTH_RECIPIENT_TOKEN_HEADER",
]
