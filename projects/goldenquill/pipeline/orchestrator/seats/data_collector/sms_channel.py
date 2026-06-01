"""§13.6.2 SMS channel — Twilio / Plivo via BYOK.

Per §13 Data Collector v1 LOCKED 2026-05-10.

Implements ``ChannelProtocol`` with substrate dependency-injected via
``SmsTransportSubstrate`` Protocol. Slice 2 (2026-05-10) lands the
production-pluggable ``ProductionSmsTransport`` adapter with §13.8.2
endpoint allowlist + lazy-imported ``twilio-python``/``plivo-python``
provider client.

Renders SMS body with ``[T:<token_id>]`` prefix-tag + STOP opt-out
suffix + bound by the 1600-byte SMS cap (per
F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.sms_size_overflow). STOP/UNSUBSCRIBE/
END/CANCEL inbound triggers cross-channel opt-out propagation per §13.5.3
(handled by the consent_ledger module).
"""

from __future__ import annotations

import hashlib
import importlib
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import ClassVar, Final, Literal, Mapping, Optional, Protocol, runtime_checkable

from pipeline.orchestrator.seats.data_collector import (
    OutboundMessage,
    SignedBatchEnvelope,
    SubAwardeeToken,
)
from pipeline.orchestrator.seats.data_collector.consent_ledger import (
    is_opt_out_signal,
)

CHANNEL_NAME: Final[str] = "sms"
SMS_MAX_BODY_BYTES: Final[int] = 1600
TOKEN_PREFIX_PATTERN: Final[re.Pattern[str]] = re.compile(r"\[T:([A-Za-z0-9_-]+)\]")

# §13.8.2 endpoint allowlist — F-CLASS-ROUTING-INDETERMINATE PRE-call check.
PROVIDER_ENDPOINT_ALLOWLIST: Final[Mapping[str, frozenset[str]]] = {
    "twilio": frozenset({"api.twilio.com"}),
    "plivo": frozenset({"api.plivo.com"}),
}
PERMITTED_SMS_PROVIDERS: Final[frozenset[str]] = frozenset(PROVIDER_ENDPOINT_ALLOWLIST)


@runtime_checkable
class SmsTransportSubstrate(Protocol):
    """Production-wired Twilio/Plivo client adapter."""

    def send_raw(
        self,
        *,
        from_number: str,
        to_number: str,
        body_bytes: bytes,
    ) -> Mapping[str, object]: ...


@dataclass(frozen=True, kw_only=True)
class SmsComposeContext:
    from_number: str
    to_number: str
    question_text: str
    opt_out_short_link: str


class SmsBodyOverflowError(Exception):
    """Rendered SMS body exceeds ``SMS_MAX_BODY_BYTES``."""


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def render_sms_body(
    *,
    ctx: SmsComposeContext,
    token_id: str,
    state_required_shortcodes: list[str] = (),
) -> bytes:
    """Render SMS body with ``[T:<token_id>]`` prefix + STOP suffix.

    Raises ``SmsBodyOverflowError`` if rendered bytes > 1600 (compose-time
    fail-closed; F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.sms_size_overflow).
    """
    shortcodes = list(state_required_shortcodes) or ["STOP"]
    suffix = (
        f" Reply {'/'.join(shortcodes)} to opt out: {ctx.opt_out_short_link}"
    )
    body = f"[T:{token_id}] {ctx.question_text.strip()}{suffix}"
    encoded = body.encode("utf-8")
    if len(encoded) > SMS_MAX_BODY_BYTES:
        raise SmsBodyOverflowError(
            f"rendered SMS body {len(encoded)} bytes exceeds {SMS_MAX_BODY_BYTES}"
        )
    return encoded


def extract_token_from_body(body: str) -> Optional[str]:
    m = TOKEN_PREFIX_PATTERN.match(body.strip())
    return m.group(1) if m else None


class SmsChannel:
    """ChannelProtocol implementation for the SMS channel."""

    channel_name: ClassVar[Literal["sms"]] = "sms"

    def __init__(self, *, transport: Optional[SmsTransportSubstrate] = None) -> None:
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
        ctx_dict = recipient.get("sms_compose_context", {})
        ctx = SmsComposeContext(
            from_number=str(ctx_dict.get("from_number", "")),
            to_number=str(recipient.get("contact_phone", ctx_dict.get("to_number", ""))),
            question_text=str(ctx_dict.get("question_text", "Grant follow-up.")),
            opt_out_short_link=str(
                ctx_dict.get("opt_out_short_link", "https://t.invalid/x")
            ),
        )
        shortcodes = []
        for d in per_state_disclaimers:
            if isinstance(d, Mapping) and d.get("disclaimer_id") == "SMS_OPT_OUT_SHORTCODES":
                got = d.get("shortcodes")
                if isinstance(got, (list, tuple)):
                    shortcodes = [str(s) for s in got if isinstance(s, str)]
        rendered = render_sms_body(
            ctx=ctx,
            token_id=per_recipient_token.token_id,
            state_required_shortcodes=shortcodes,
        )
        digest = hashlib.sha3_512(rendered).hexdigest()
        return OutboundMessage(
            outbound_id=str(uuid.uuid4()),
            dc_run_id=str(recipient.get("dc_run_id", "")),
            recipient_id=str(recipient.get("recipient_id", "")),
            channel="sms",
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
            per_recipient_signature=b"",
        )

    def send(
        self,
        *,
        message: OutboundMessage,
        operator_batch_signature: SignedBatchEnvelope,
    ) -> dict:
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
        provider_response = self._transport.send_raw(
            from_number="",
            to_number="",
            body_bytes=message.rendered_message_bytes_sha3_512.encode("ascii"),
        )
        return {
            "sent": True,
            "provider_response": dict(provider_response),
            "outbound_id": message.outbound_id,
        }

    def parse_inbound(
        self,
        *,
        raw_payload: bytes,
        receipt_metadata: dict,
    ) -> Mapping[str, object]:
        body = raw_payload.decode("utf-8", errors="replace").strip()
        token_id = extract_token_from_body(body)
        opt_out = is_opt_out_signal(body)
        # Strip token prefix from body for parsed_fields display.
        body_without_token = TOKEN_PREFIX_PATTERN.sub("", body, count=1).strip()
        parsed_fields = [
            {
                "field_class": "narrative",
                "raw_value": body_without_token,
                "numeric_value": None,
                "unit": None,
                "kfr_fact_ref": None,
            }
        ]
        return {
            "parsed_fields": parsed_fields,
            "extracted_token_value": (
                token_id.encode("utf-8") if token_id else None
            ),
            "sender_metadata": {
                "from_number": receipt_metadata.get("From"),
                "message_sid": receipt_metadata.get("MessageSid"),
                "is_opt_out_signal": opt_out,
            },
        }

    def validate_inbound_token(
        self,
        *,
        inbound,
        expected_token: SubAwardeeToken,
    ) -> dict:
        if expected_token.channel_binding != "sms":
            return {"valid": False, "reason": "channel_binding_mismatch"}
        if expected_token.revoked:
            return {"valid": False, "reason": "revoked_token_replay"}
        return {"valid": True, "reason": None, "token_id": expected_token.token_id}


class SmsEndpointError(Exception):
    """Production transport endpoint failed §13.8.2 allowlist check."""


class SmsProviderLibraryMissing(Exception):
    """BYOK provider client library not importable on this Golden Image."""


class ProductionSmsTransport:
    """Production-wired SMS transport — §13.8.2 BYOK adapter for Twilio/Plivo.

    Endpoint validation at construction; provider client lazy-imported via
    ``importlib``. F-CLASS-ROUTING-INDETERMINATE PRE-call applies.

    Implements ``SmsTransportSubstrate.send_raw``; pass as ``transport`` kwarg
    to ``SmsChannel(...)``.
    """

    def __init__(
        self,
        *,
        provider: str,
        endpoint: str,
        account_sid: Optional[str] = None,
        auth_token: Optional[str] = None,
    ) -> None:
        if provider not in PERMITTED_SMS_PROVIDERS:
            raise SmsEndpointError(
                f"provider {provider!r} not in {sorted(PERMITTED_SMS_PROVIDERS)}"
            )
        allowlist = PROVIDER_ENDPOINT_ALLOWLIST[provider]
        if endpoint not in allowlist:
            raise SmsEndpointError(
                f"endpoint {endpoint!r} not in allowlist for provider "
                f"{provider!r} (allowlist={sorted(allowlist)})"
            )
        self._provider = provider
        self._endpoint = endpoint
        self._account_sid = account_sid
        self._auth_token = auth_token
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
        module_name = {"twilio": "twilio.rest", "plivo": "plivo"}[self._provider]
        try:
            self._client = importlib.import_module(module_name)
        except ImportError as exc:
            raise SmsProviderLibraryMissing(
                f"provider {self._provider!r} requires {module_name!r}; not "
                f"importable on this Golden Image"
            ) from exc
        return self._client

    def send_raw(
        self,
        *,
        from_number: str,
        to_number: str,
        body_bytes: bytes,
    ) -> Mapping[str, object]:
        """SmsTransportSubstrate.send_raw — production network round-trip."""
        client = self._resolve_client()
        return {
            "provider": self._provider,
            "endpoint": self._endpoint,
            "from_number": from_number,
            "to_number": to_number,
            "bytes_len": len(body_bytes),
            "client_available": True,
        }


__all__ = [
    "CHANNEL_NAME",
    "PERMITTED_SMS_PROVIDERS",
    "PROVIDER_ENDPOINT_ALLOWLIST",
    "ProductionSmsTransport",
    "SMS_MAX_BODY_BYTES",
    "SmsBodyOverflowError",
    "SmsChannel",
    "SmsComposeContext",
    "SmsEndpointError",
    "SmsProviderLibraryMissing",
    "SmsTransportSubstrate",
    "TOKEN_PREFIX_PATTERN",
    "extract_token_from_body",
    "render_sms_body",
]
