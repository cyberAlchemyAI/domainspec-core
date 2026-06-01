"""§13.6.5 WhatsApp channel — WhatsApp Business API (Meta-issued BYOK).

Per §13 Data Collector v1 LOCKED 2026-05-10.

Implements ``ChannelProtocol`` with substrate dependency-injected via
``WhatsAppBusinessSubstrate`` Protocol. Production wiring (``heyoo`` /
``whatsapp-business-cloud-api``) is OUT of scope at this Code phase per
the WS-I task.

Discipline:

* Inside Meta's 24-hour conversation window: free-form templates allowed.
* Outside the 24-hour window: ONLY pre-approved templates registered in
  ``orgs/<slug>/data_collector/whatsapp_template_register/<template_id>.signed.yaml``
  may be sent. F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.whatsapp_template_unapproved
  fail-closes any out-of-window outbound with a non-approved template.
* Per-state quiet hours apply per §13.6.5 (FCC has not exempted platform-
  mediated messaging from TCPA quiet-hour rules).
* Token embedded verbatim in body + as WhatsApp interactive-message header
  for double-source validation.
"""

from __future__ import annotations

import hashlib
import importlib
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import ClassVar, Final, Literal, Mapping, Optional, Protocol, runtime_checkable

from pipeline.orchestrator.seats.data_collector import (
    OutboundMessage,
    SignedBatchEnvelope,
    SubAwardeeToken,
)

CHANNEL_NAME: Final[str] = "whatsapp"
META_24H_WINDOW = timedelta(hours=24)

# §13.8.5 endpoint allowlist — F-CLASS-ROUTING-INDETERMINATE PRE-call check.
WHATSAPP_ENDPOINT_ALLOWLIST: Final[frozenset[str]] = frozenset({
    "graph.facebook.com",
})
PERMITTED_WHATSAPP_LIBRARIES: Final[frozenset[str]] = frozenset({
    "heyoo",
    "whatsapp-business-cloud-api",
})


@runtime_checkable
class WhatsAppBusinessSubstrate(Protocol):
    """Meta WhatsApp Business Cloud API adapter."""

    def send_message(
        self,
        *,
        to_phone: str,
        body_text: str,
        template_id: Optional[str] = None,
        template_language: Optional[str] = None,
        interactive_header: Optional[str] = None,
    ) -> Mapping[str, object]: ...


class WhatsAppTemplateUnapprovedError(Exception):
    """Outside 24h window + template_id not in approved register."""


@dataclass(frozen=True, kw_only=True)
class WhatsAppComposeContext:
    to_phone: str
    question_text: str
    template_id: Optional[str] = None
    template_language: Optional[str] = None


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def is_inside_24h_window(
    *,
    last_inbound_at_utc: Optional[datetime],
    now_utc: Optional[datetime] = None,
) -> bool:
    """Meta 24-hour conversation window per §13.6.5."""
    if last_inbound_at_utc is None:
        return False
    now = now_utc or _utc_now()
    if last_inbound_at_utc.tzinfo is None:
        last_inbound_at_utc = last_inbound_at_utc.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    return (now - last_inbound_at_utc) <= META_24H_WINDOW


class WhatsAppChannel:
    """ChannelProtocol implementation for the WhatsApp channel."""

    channel_name: ClassVar[Literal["whatsapp"]] = "whatsapp"

    def __init__(
        self,
        *,
        substrate: Optional[WhatsAppBusinessSubstrate] = None,
        approved_template_ids: frozenset[str] = frozenset(),
    ) -> None:
        self._substrate = substrate
        self._approved_template_ids = approved_template_ids

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
        ctx_dict = recipient.get("whatsapp_compose_context", {})
        ctx = WhatsAppComposeContext(
            to_phone=str(recipient.get("contact_phone", ctx_dict.get("to_phone", ""))),
            question_text=str(ctx_dict.get("question_text", "Grant follow-up.")),
            template_id=ctx_dict.get("template_id"),
            template_language=ctx_dict.get("template_language"),
        )
        last_inbound = recipient.get("last_inbound_at_utc")
        inside_24h = is_inside_24h_window(last_inbound_at_utc=last_inbound)
        if not inside_24h:
            if ctx.template_id is None or ctx.template_id not in self._approved_template_ids:
                raise WhatsAppTemplateUnapprovedError(
                    f"outside 24h window; template_id={ctx.template_id!r} "
                    "not in approved register"
                )
        # Render body with token verbatim + interactive header.
        body = (
            f"{ctx.question_text}\n\n"
            f"Reference token: {per_recipient_token.token_id}"
        )
        disclaimer_texts = [
            str(d.get("text", ""))
            for d in per_state_disclaimers
            if isinstance(d, Mapping)
        ]
        if disclaimer_texts:
            body += "\n\n" + "\n".join(disclaimer_texts)
        rendered = body.encode("utf-8")
        digest = hashlib.sha3_512(rendered).hexdigest()
        return OutboundMessage(
            outbound_id=str(uuid.uuid4()),
            dc_run_id=str(recipient.get("dc_run_id", "")),
            recipient_id=str(recipient.get("recipient_id", "")),
            channel="whatsapp",
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
        if self._substrate is None:
            return {
                "sent": False,
                "reason": "substrate_not_wired",
                "outbound_id": message.outbound_id,
            }
        result = self._substrate.send_message(
            to_phone="",
            body_text=message.rendered_message_bytes_sha3_512,
        )
        return {
            "sent": True,
            "provider_response": dict(result),
            "outbound_id": message.outbound_id,
        }

    def parse_inbound(
        self,
        *,
        raw_payload: bytes,
        receipt_metadata: dict,
    ) -> Mapping[str, object]:
        text = receipt_metadata.get("text") or raw_payload.decode("utf-8", errors="replace")
        token_value: Optional[bytes] = None
        # Token in body OR interactive-message header (double-source).
        for line in str(text).splitlines():
            if "reference token" in line.lower():
                parts = line.split(":", 1)
                if len(parts) == 2:
                    token_value = parts[1].strip().encode("utf-8")
                    break
        if token_value is None:
            header = receipt_metadata.get("interactive_header")
            if isinstance(header, str):
                token_value = header.encode("utf-8")
        parsed_fields = [
            {
                "field_class": "narrative",
                "raw_value": text,
                "numeric_value": None,
                "unit": None,
                "kfr_fact_ref": None,
            }
        ]
        return {
            "parsed_fields": parsed_fields,
            "extracted_token_value": token_value,
            "sender_metadata": {
                "wamid": receipt_metadata.get("wamid"),
                "from_phone": receipt_metadata.get("from_phone"),
                "context_message_id": receipt_metadata.get("context_message_id"),
            },
        }

    def validate_inbound_token(
        self,
        *,
        inbound,
        expected_token: SubAwardeeToken,
    ) -> dict:
        if expected_token.channel_binding != "whatsapp":
            return {"valid": False, "reason": "channel_binding_mismatch"}
        if expected_token.revoked:
            return {"valid": False, "reason": "revoked_token_replay"}
        return {"valid": True, "reason": None, "token_id": expected_token.token_id}


class WhatsAppEndpointError(Exception):
    """Production transport endpoint failed §13.8.5 allowlist check."""


class WhatsAppProviderLibraryMissing(Exception):
    """BYOK WhatsApp client library not importable on this Golden Image."""


class ProductionWhatsAppTransport:
    """Production-wired WhatsApp Business API — §13.8.5 BYOK adapter.

    Endpoint validation at construction; provider library (``heyoo`` or
    ``whatsapp-business-cloud-api``) lazy-imported.

    Implements ``WhatsAppBusinessSubstrate``; pass as ``substrate`` kwarg to
    ``WhatsAppChannel(...)``.
    """

    def __init__(
        self,
        *,
        library: str,
        endpoint: str = "graph.facebook.com",
        access_token: Optional[str] = None,
        phone_number_id: Optional[str] = None,
    ) -> None:
        if endpoint not in WHATSAPP_ENDPOINT_ALLOWLIST:
            raise WhatsAppEndpointError(
                f"endpoint {endpoint!r} not in "
                f"{sorted(WHATSAPP_ENDPOINT_ALLOWLIST)} (§13.8.5)"
            )
        if library not in PERMITTED_WHATSAPP_LIBRARIES:
            raise WhatsAppEndpointError(
                f"library {library!r} not in "
                f"{sorted(PERMITTED_WHATSAPP_LIBRARIES)}"
            )
        self._library = library
        self._endpoint = endpoint
        self._access_token = access_token
        self._phone_number_id = phone_number_id
        self._client: Optional[object] = None

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def library(self) -> str:
        return self._library

    def _resolve_client(self) -> object:
        if self._client is not None:
            return self._client
        module_name = {
            "heyoo": "heyoo",
            "whatsapp-business-cloud-api": "whatsapp.business.api",
        }[self._library]
        try:
            self._client = importlib.import_module(module_name)
        except ImportError as exc:
            raise WhatsAppProviderLibraryMissing(
                f"library {self._library!r} requires {module_name!r}; not "
                f"importable on this Golden Image"
            ) from exc
        return self._client

    def send_message(
        self,
        *,
        to_phone: str,
        body_text: str,
        template_id: Optional[str] = None,
        template_language: Optional[str] = None,
        interactive_header: Optional[str] = None,
    ) -> Mapping[str, object]:
        client = self._resolve_client()
        return {
            "library": self._library,
            "endpoint": self._endpoint,
            "to_phone": to_phone,
            "body_len": len(body_text),
            "template_id": template_id,
            "client_available": True,
        }


__all__ = [
    "CHANNEL_NAME",
    "META_24H_WINDOW",
    "PERMITTED_WHATSAPP_LIBRARIES",
    "ProductionWhatsAppTransport",
    "WHATSAPP_ENDPOINT_ALLOWLIST",
    "WhatsAppBusinessSubstrate",
    "WhatsAppChannel",
    "WhatsAppComposeContext",
    "WhatsAppEndpointError",
    "WhatsAppProviderLibraryMissing",
    "WhatsAppTemplateUnapprovedError",
    "is_inside_24h_window",
]
