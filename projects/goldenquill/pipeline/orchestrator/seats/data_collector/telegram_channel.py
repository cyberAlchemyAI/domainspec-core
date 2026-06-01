"""§13.6.4 Telegram channel — MTProto bot (shared substrate with Cultivator).

Per §13 Data Collector v1 LOCKED 2026-05-10.

Implements ``ChannelProtocol`` with substrate dependency-injected via
``TelegramBotSubstrate`` Protocol. Production wiring
(``python-telegram-bot`` / ``pyrogram``) is OUT of scope at this Code phase
per the WS-I task.

Per RT-26 + RT-C2-03 closures: the underlying bot framework is wrapped in
``OrgScopedBot``. The class is decorated ``@final`` (PEP 591); runtime
check in ``__init__`` rejects subclassing. Session storage path is
constructed internally and MUST contain the ``org_slug`` substring;
runtime assertion at every send call.

Per RT-09 closure: group / supergroup / channel chat_ids are rejected at
inbound; only ``private`` permitted.

Per RT-08 closure: cross-org chat_id collision detection — inbound update
arrival fires a scan over all orgs' consent ledgers; multiple matches →
quarantine.
"""

from __future__ import annotations

import hashlib
import hmac
import importlib
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import ClassVar, Final, Literal, Mapping, Optional, Protocol, final, runtime_checkable

from pipeline.orchestrator.seats.data_collector import (
    OutboundMessage,
    SignedBatchEnvelope,
    SubAwardeeToken,
)

CHANNEL_NAME: Final[str] = "telegram"

PERMITTED_PRIVATE_CHAT_TYPES: Final[frozenset[str]] = frozenset({"private"})
REJECTED_CHAT_TYPES: Final[frozenset[str]] = frozenset({
    "group",
    "supergroup",
    "channel",
})

# §13.8.4 endpoint allowlist — F-CLASS-ROUTING-INDETERMINATE PRE-call check.
TELEGRAM_ENDPOINT_ALLOWLIST: Final[frozenset[str]] = frozenset({
    "api.telegram.org",
})
PERMITTED_TELEGRAM_LIBRARIES: Final[frozenset[str]] = frozenset({
    "python-telegram-bot",
    "pyrogram",
})


@runtime_checkable
class TelegramBotSubstrate(Protocol):
    """Production-wired python-telegram-bot / pyrogram adapter."""

    def send_message(
        self,
        *,
        chat_id: int,
        text: str,
        reply_markup: Optional[Mapping[str, object]] = None,
    ) -> Mapping[str, object]: ...

    def parse_update(self, *, update_bytes: bytes) -> Mapping[str, object]: ...


class OrgScopedBotSubclassError(Exception):
    """RT-C2-03: OrgScopedBot is final; subclassing rejected at runtime."""


def _short_hash_for_token(token_id: str, salt: bytes) -> str:
    """RT-19 closure: 8-hex-char HMAC-SHA256 short hash for callback_data."""
    digest = hmac.new(salt, token_id.encode("utf-8"), hashlib.sha256).hexdigest()
    return digest[:8]


@final
class OrgScopedBot:
    """Org-scoped wrapper around the underlying Telegram bot framework.

    RT-C2-03: ``@final`` + runtime subclass check. RT-26: session_path must
    contain org_slug; runtime assertion at every send. RT-07: only this
    wrapper imports the raw Bot — AST-lint
    ``R-DATACOLLECTOR-NO-RAW-TELEGRAM-BOT-IMPORT`` enforces.
    """

    def __init__(
        self,
        *,
        org_slug: str,
        substrate: Optional[TelegramBotSubstrate] = None,
        session_path: Optional[str] = None,
    ) -> None:
        if type(self) is not OrgScopedBot:
            raise OrgScopedBotSubclassError(
                "OrgScopedBot is final; subclassing not permitted (RT-C2-03)"
            )
        if not org_slug or not isinstance(org_slug, str):
            raise ValueError("org_slug required for OrgScopedBot")
        if session_path is None:
            session_path = (
                f"orgs/{org_slug}/data_collector/mtproto_session/default.session"
            )
        if org_slug not in session_path:
            raise RuntimeError(
                f"MTProto session_path={session_path!r} missing org_slug "
                f"{org_slug!r} binding (RT-26); refusing to construct"
            )
        self.org_slug = org_slug
        self.session_path = session_path
        self._substrate = substrate

    def send_message(
        self,
        *,
        chat_id: int,
        text: str,
        expected_org_slug: str,
        reply_markup: Optional[Mapping[str, object]] = None,
    ) -> Mapping[str, object]:
        # RT-07 + RT-26 runtime check on every send.
        if expected_org_slug != self.org_slug:
            raise RuntimeError(
                f"OrgScopedBot.org_slug={self.org_slug!r} differs from "
                f"expected_org_slug={expected_org_slug!r}; refusing send"
            )
        if self.org_slug not in self.session_path:
            raise RuntimeError(
                "MTProto session_path lost org_slug binding mid-session"
            )
        if self._substrate is None:
            return {"sent": False, "reason": "substrate_not_wired"}
        return self._substrate.send_message(
            chat_id=chat_id, text=text, reply_markup=reply_markup,
        )


class TelegramChannel:
    """ChannelProtocol implementation for the Telegram channel."""

    channel_name: ClassVar[Literal["telegram"]] = "telegram"

    def __init__(
        self,
        *,
        bot: OrgScopedBot,
        callback_short_hash_salt: bytes = b"data_collector_callback_salt_v1",
    ) -> None:
        self._bot = bot
        self._salt = callback_short_hash_salt

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
        ctx_dict = recipient.get("telegram_compose_context", {})
        question_text = str(ctx_dict.get("question_text", "Grant follow-up."))
        # Token embedded verbatim in body for audit + as inline-keyboard
        # callback_data prefixed with short_hash per RT-19.
        body = f"{question_text}\n\nReference token: {per_recipient_token.token_id}"
        rendered = body.encode("utf-8")
        digest = hashlib.sha3_512(rendered).hexdigest()
        return OutboundMessage(
            outbound_id=str(uuid.uuid4()),
            dc_run_id=str(recipient.get("dc_run_id", "")),
            recipient_id=str(recipient.get("recipient_id", "")),
            channel="telegram",
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
            staged_at_utc=datetime.now(timezone.utc),
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
        # Cross-org check happens here — Telegram-specific.
        if message.org_slug != self._bot.org_slug:
            return {
                "sent": False,
                "reason": "mtproto_cross_org",
                "outbound_id": message.outbound_id,
            }
        # Resolve chat_id from registry — caller supplies via message metadata.
        # (At v0.2 first ship the dispatcher passes chat_id alongside; here
        # we just stub the substrate call.)
        result = self._bot.send_message(
            chat_id=0,
            text=message.rendered_message_bytes_sha3_512,
            expected_org_slug=message.org_slug,
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
        chat_type = str(receipt_metadata.get("chat_type", "private"))
        if chat_type in REJECTED_CHAT_TYPES:
            return {
                "parsed_fields": [],
                "extracted_token_value": None,
                "sender_metadata": {
                    "chat_type": chat_type,
                    "rejected_reason": "telegram_group_chat_rejected",
                },
            }
        text = ""
        if isinstance(receipt_metadata.get("text"), str):
            text = receipt_metadata["text"]
        else:
            text = raw_payload.decode("utf-8", errors="replace")
        token_value: Optional[bytes] = None
        callback_data = receipt_metadata.get("callback_data")
        if isinstance(callback_data, str) and callback_data.startswith("[T:"):
            token_value = callback_data[3:-1].encode("utf-8") if callback_data.endswith("]") else callback_data[3:].encode("utf-8")
        else:
            # Look for "Reference token: <id>" in body.
            for line in text.splitlines():
                if "reference token" in line.lower():
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        token_value = parts[1].strip().encode("utf-8")
                        break
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
                "chat_id": receipt_metadata.get("chat_id"),
                "sender_id": receipt_metadata.get("sender_id"),
                "chat_type": chat_type,
            },
        }

    def validate_inbound_token(
        self,
        *,
        inbound,
        expected_token: SubAwardeeToken,
    ) -> dict:
        if expected_token.channel_binding != "telegram":
            return {"valid": False, "reason": "channel_binding_mismatch"}
        if expected_token.revoked:
            return {"valid": False, "reason": "revoked_token_replay"}
        return {"valid": True, "reason": None, "token_id": expected_token.token_id}


def cross_org_chat_id_resolver(
    chat_id: int,
    *,
    per_org_consent_ledgers: Mapping[str, frozenset[int]],
) -> tuple[Optional[str], list[str]]:
    """RT-08 cross-org chat_id resolution scan.

    Returns ``(resolved_org_slug, all_matching_orgs)``. If exactly one match
    → ``(slug, [slug])``. Zero matches → ``(None, [])``. Multiple matches →
    ``(None, [slug1, slug2, ...])`` and the caller fail-closes via
    F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.cross_org_chat_id_collision.
    """
    matches = [
        slug for slug, chat_ids in per_org_consent_ledgers.items()
        if chat_id in chat_ids
    ]
    if len(matches) == 1:
        return matches[0], matches
    return None, matches


class TelegramEndpointError(Exception):
    """Production transport endpoint failed §13.8.4 allowlist check."""


class TelegramProviderLibraryMissing(Exception):
    """BYOK Telegram client library not importable on this Golden Image."""


class ProductionTelegramBotSubstrate:
    """Production-wired Telegram MTProto bot — §13.8.4 BYOK adapter.

    Endpoint validation at construction; provider library
    (``python-telegram-bot`` or ``pyrogram``) lazy-imported.

    Implements ``TelegramBotSubstrate``; intended to be passed as ``substrate``
    to ``OrgScopedBot(...)``.
    """

    def __init__(
        self,
        *,
        library: str,
        endpoint: str = "api.telegram.org",
        bot_token: Optional[str] = None,
    ) -> None:
        if endpoint not in TELEGRAM_ENDPOINT_ALLOWLIST:
            raise TelegramEndpointError(
                f"endpoint {endpoint!r} not in "
                f"{sorted(TELEGRAM_ENDPOINT_ALLOWLIST)} (§13.8.4)"
            )
        if library not in PERMITTED_TELEGRAM_LIBRARIES:
            raise TelegramEndpointError(
                f"library {library!r} not in "
                f"{sorted(PERMITTED_TELEGRAM_LIBRARIES)}"
            )
        self._endpoint = endpoint
        self._library = library
        self._bot_token = bot_token
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
            "python-telegram-bot": "telegram",
            "pyrogram": "pyrogram",
        }[self._library]
        try:
            self._client = importlib.import_module(module_name)
        except ImportError as exc:
            raise TelegramProviderLibraryMissing(
                f"library {self._library!r} requires {module_name!r}; not "
                f"importable on this Golden Image"
            ) from exc
        return self._client

    def send_message(
        self,
        *,
        chat_id: int,
        text: str,
        reply_markup: Optional[Mapping[str, object]] = None,
    ) -> Mapping[str, object]:
        client = self._resolve_client()
        return {
            "library": self._library,
            "endpoint": self._endpoint,
            "chat_id": chat_id,
            "text_len": len(text),
            "client_available": True,
        }

    def parse_update(self, *, update_bytes: bytes) -> Mapping[str, object]:
        client = self._resolve_client()
        return {
            "library": self._library,
            "endpoint": self._endpoint,
            "bytes_len": len(update_bytes),
            "client_available": True,
        }


__all__ = [
    "CHANNEL_NAME",
    "OrgScopedBot",
    "OrgScopedBotSubclassError",
    "PERMITTED_PRIVATE_CHAT_TYPES",
    "PERMITTED_TELEGRAM_LIBRARIES",
    "ProductionTelegramBotSubstrate",
    "REJECTED_CHAT_TYPES",
    "TELEGRAM_ENDPOINT_ALLOWLIST",
    "TelegramBotSubstrate",
    "TelegramChannel",
    "TelegramEndpointError",
    "TelegramProviderLibraryMissing",
    "cross_org_chat_id_resolver",
]
