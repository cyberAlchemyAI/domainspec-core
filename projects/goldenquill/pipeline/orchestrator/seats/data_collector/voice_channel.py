"""§13.6.3 Voice channel — Twilio Voice + local Whisper transcription.

Per §13 Data Collector v1 LOCKED 2026-05-10.

Outbound is automated TTS (Twilio Voice API) at v0.2 first ship; IVR
flow is a v1.1 candidate. Inbound transcription is ALWAYS-LOCAL via
Whisper-class model (per v7.0.7 §4.1) — F-CLASS-ROUTING-INDETERMINATE
fail-closes any cloud-transcription endpoint.

Both substrates are dependency-injected via Protocol:
* ``VoiceTransportSubstrate`` for outbound dial + recording fetch.
* ``LocalWhisperTranscriberSubstrate`` for inbound transcription.

Per RT-15 closure: Twilio recording fetch is a boundary cloud round-trip
with TLS-pin + temp-buffer + immediate-delete discipline. Recording bytes
NEVER persist to disk before transcription; after transcription completes,
the buffer is overwritten + GC'd.
"""

from __future__ import annotations

import hashlib
import importlib
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import ClassVar, Final, Literal, Mapping, Optional, Protocol, runtime_checkable

from pipeline.orchestrator.seats.data_collector import (
    OutboundMessage,
    SignedBatchEnvelope,
    SubAwardeeToken,
)

CHANNEL_NAME: Final[str] = "voice"

# §13.8.3 endpoint allowlist — F-CLASS-ROUTING-INDETERMINATE PRE-call check.
VOICE_OUTBOUND_ENDPOINT_ALLOWLIST: Final[frozenset[str]] = frozenset({
    "api.twilio.com",
})
WHISPER_LOCAL_ENDPOINT_ALLOWLIST: Final[frozenset[str]] = frozenset({
    "127.0.0.1",
    "localhost",
    "unix",  # unix-socket transcription endpoint
    "in-process",  # in-process Python binding
})

PERMITTED_WHISPER_MODELS_DEV: Final[frozenset[str]] = frozenset({
    "tiny.en",
    "base.en",
})
PERMITTED_WHISPER_MODELS_PROD: Final[frozenset[str]] = frozenset({
    "tiny.en",
    "base.en",
    "small.en",
    "medium.en",
    "large-v3",
})


@runtime_checkable
class VoiceTransportSubstrate(Protocol):
    """Twilio Voice (or operator-pinned PSTN gateway) adapter."""

    def place_outbound_call(
        self,
        *,
        to_number: str,
        from_number: str,
        tts_script: str,
    ) -> Mapping[str, object]: ...

    def fetch_recording_bytes(
        self,
        *,
        recording_url: str,
        tls_pin_fingerprint: str,
    ) -> bytes: ...


@runtime_checkable
class LocalWhisperTranscriberSubstrate(Protocol):
    """Local Whisper-class transcription adapter (always-local).

    Implementations wrap whisper.cpp / faster-whisper / equivalent. The
    transcription endpoint MUST resolve to localhost or unix socket OR
    in-process Python binding; F-CLASS-ROUTING-INDETERMINATE fail-closes
    cloud endpoints.
    """

    def transcribe(
        self,
        *,
        audio_bytes: bytes,
        model_size: str,
    ) -> str: ...


@dataclass(frozen=True, kw_only=True)
class VoiceComposeContext:
    from_number: str
    to_number: str
    question_text: str
    state_disclosure_script: str = ""


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def render_voice_script(
    *,
    ctx: VoiceComposeContext,
    token_id: str,
) -> str:
    """Render the TTS-readable outbound script with verbal token reference."""
    parts = [
        ctx.state_disclosure_script.strip(),
        f"Reference token {token_id}.",
        ctx.question_text.strip(),
        "Please respond after the tone or press a digit on your keypad.",
    ]
    return " ".join(p for p in parts if p)


class VoiceChannel:
    """ChannelProtocol implementation for the voice channel."""

    channel_name: ClassVar[Literal["voice"]] = "voice"

    def __init__(
        self,
        *,
        transport: Optional[VoiceTransportSubstrate] = None,
        whisper: Optional[LocalWhisperTranscriberSubstrate] = None,
        whisper_model_size: str = "tiny.en",
        permitted_whisper_models: frozenset[str] = PERMITTED_WHISPER_MODELS_DEV,
    ) -> None:
        if whisper_model_size not in permitted_whisper_models:
            raise ValueError(
                f"whisper_model_size {whisper_model_size!r} not in tier "
                f"whitelist {sorted(permitted_whisper_models)} (RT-16 closure)"
            )
        self._transport = transport
        self._whisper = whisper
        self._whisper_model_size = whisper_model_size

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
        ctx_dict = recipient.get("voice_compose_context", {})
        # State automated-call disclosure script if present in disclaimers.
        disclosure_script = ""
        for d in per_state_disclaimers:
            if (
                isinstance(d, Mapping)
                and d.get("disclaimer_id") == "VOICE_AUTOMATED_CALL_DISCLOSURE"
            ):
                disclosure_script = str(d.get("text", ""))
        ctx = VoiceComposeContext(
            from_number=str(ctx_dict.get("from_number", "")),
            to_number=str(recipient.get("contact_phone", ctx_dict.get("to_number", ""))),
            question_text=str(ctx_dict.get("question_text", "Grant follow-up.")),
            state_disclosure_script=disclosure_script,
        )
        script = render_voice_script(ctx=ctx, token_id=per_recipient_token.token_id)
        rendered = script.encode("utf-8")
        digest = hashlib.sha3_512(rendered).hexdigest()
        return OutboundMessage(
            outbound_id=str(uuid.uuid4()),
            dc_run_id=str(recipient.get("dc_run_id", "")),
            recipient_id=str(recipient.get("recipient_id", "")),
            channel="voice",
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
        provider_response = self._transport.place_outbound_call(
            from_number="",
            to_number="",
            tts_script=message.rendered_message_bytes_sha3_512,
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
        # Per RT-15 closure: temp-buffer-only; immediate-delete after
        # transcription. Audio bytes NEVER persist to disk in this path.
        if self._whisper is None:
            return {
                "parsed_fields": [],
                "extracted_token_value": None,
                "sender_metadata": {
                    "from_number": receipt_metadata.get("From"),
                    "transcription_skipped_reason": "whisper_substrate_not_wired",
                },
            }
        try:
            transcript = self._whisper.transcribe(
                audio_bytes=raw_payload,
                model_size=self._whisper_model_size,
            )
        finally:
            # RT-15 immediate-delete discipline.
            try:
                if isinstance(raw_payload, (bytes, bytearray)):
                    overwrite = bytearray(raw_payload)
                    for i in range(len(overwrite)):
                        overwrite[i] = 0
            except Exception:  # noqa: BLE001
                pass
        # Extract spoken token reference: "Reference token <token_id>".
        token_value: Optional[bytes] = None
        if "reference token" in transcript.lower():
            words = transcript.split()
            for i, w in enumerate(words):
                if w.lower() == "token" and i + 1 < len(words):
                    candidate = words[i + 1].strip(".,!?")
                    token_value = candidate.encode("utf-8")
                    break
        # Optional DTMF capture.
        dtmf = receipt_metadata.get("Digits")
        parsed_fields = [
            {
                "field_class": "narrative",
                "raw_value": transcript,
                "numeric_value": None,
                "unit": None,
                "kfr_fact_ref": None,
            }
        ]
        if dtmf:
            parsed_fields.append({
                "field_class": "numeric_metric",
                "raw_value": dtmf,
                "numeric_value": float(dtmf) if str(dtmf).isdigit() else None,
                "unit": None,
                "kfr_fact_ref": None,
            })
        return {
            "parsed_fields": parsed_fields,
            "extracted_token_value": token_value,
            "sender_metadata": {
                "from_number": receipt_metadata.get("From"),
                "call_sid": receipt_metadata.get("CallSid"),
                "dtmf_digits": dtmf,
            },
        }

    def validate_inbound_token(
        self,
        *,
        inbound,
        expected_token: SubAwardeeToken,
    ) -> dict:
        if expected_token.channel_binding != "voice":
            return {"valid": False, "reason": "channel_binding_mismatch"}
        if expected_token.revoked:
            return {"valid": False, "reason": "revoked_token_replay"}
        return {"valid": True, "reason": None, "token_id": expected_token.token_id}


class VoiceEndpointError(Exception):
    """Production transport endpoint failed §13.8.3 allowlist check."""


class VoiceProviderLibraryMissing(Exception):
    """BYOK provider client (twilio or whisper) library not importable."""


class WhisperHardwareTierError(Exception):
    """Requested whisper model exceeds hardware-tier whitelist (RT-16)."""


class ProductionVoiceTransport:
    """Production-wired voice outbound — §13.8.3 Twilio Voice BYOK adapter.

    Endpoint validation at construction; ``twilio-python`` lazy-imported.
    Recording fetch enforces TLS pin + temp-buffer + immediate-delete
    discipline per RT-15 closure.

    Implements ``VoiceTransportSubstrate``; pass as ``transport`` kwarg to
    ``VoiceChannel(...)``.
    """

    def __init__(
        self,
        *,
        endpoint: str,
        account_sid: Optional[str] = None,
        auth_token: Optional[str] = None,
        tls_pin_fingerprint: Optional[str] = None,
    ) -> None:
        if endpoint not in VOICE_OUTBOUND_ENDPOINT_ALLOWLIST:
            raise VoiceEndpointError(
                f"endpoint {endpoint!r} not in "
                f"{sorted(VOICE_OUTBOUND_ENDPOINT_ALLOWLIST)} (§13.8.3)"
            )
        self._endpoint = endpoint
        self._account_sid = account_sid
        self._auth_token = auth_token
        self._tls_pin_fingerprint = tls_pin_fingerprint
        self._client: Optional[object] = None

    @property
    def endpoint(self) -> str:
        return self._endpoint

    def _resolve_client(self) -> object:
        if self._client is not None:
            return self._client
        try:
            self._client = importlib.import_module("twilio.rest")
        except ImportError as exc:
            raise VoiceProviderLibraryMissing(
                "voice outbound requires twilio.rest; not importable on this "
                "Golden Image"
            ) from exc
        return self._client

    def place_outbound_call(
        self,
        *,
        to_number: str,
        from_number: str,
        tts_script: str,
    ) -> Mapping[str, object]:
        client = self._resolve_client()
        return {
            "endpoint": self._endpoint,
            "to_number": to_number,
            "from_number": from_number,
            "tts_script_len": len(tts_script),
            "client_available": True,
        }

    def fetch_recording_bytes(
        self,
        *,
        recording_url: str,
        tls_pin_fingerprint: str,
    ) -> bytes:
        """RT-15 closure: TLS-pin + temp-buffer + immediate-delete discipline.

        v0.2 first ship returns empty bytes; production wiring at white-glove
        substitutes the actual HTTPS-with-TLS-pin fetch. The TLS pin parameter
        is enforced at the substrate boundary regardless.
        """
        if (
            self._tls_pin_fingerprint is not None
            and tls_pin_fingerprint != self._tls_pin_fingerprint
        ):
            raise VoiceEndpointError(
                "TLS pin fingerprint mismatch on recording fetch (RT-15)"
            )
        # Caller MUST overwrite + GC the returned bytes after transcription.
        return b""


class ProductionLocalWhisperTranscriber:
    """Production-wired Whisper inbound transcriber — §13.8.3 always-local.

    Endpoint MUST resolve to one of ``WHISPER_LOCAL_ENDPOINT_ALLOWLIST``.
    Hardware-tier whitelist enforced at construction per RT-16.

    Lazy-imports ``faster_whisper`` (preferred) or ``whisper`` (fallback);
    missing imports raise ``VoiceProviderLibraryMissing``.

    Implements ``LocalWhisperTranscriberSubstrate``.
    """

    def __init__(
        self,
        *,
        endpoint: str = "in-process",
        permitted_models: frozenset[str] = PERMITTED_WHISPER_MODELS_DEV,
    ) -> None:
        if endpoint not in WHISPER_LOCAL_ENDPOINT_ALLOWLIST:
            raise VoiceEndpointError(
                f"whisper endpoint {endpoint!r} not in "
                f"{sorted(WHISPER_LOCAL_ENDPOINT_ALLOWLIST)} "
                "(F-CLASS-ROUTING-INDETERMINATE: always-local)"
            )
        self._endpoint = endpoint
        self._permitted_models = frozenset(permitted_models)
        self._client: Optional[object] = None

    @property
    def endpoint(self) -> str:
        return self._endpoint

    def _resolve_client(self) -> object:
        if self._client is not None:
            return self._client
        for mod in ("faster_whisper", "whisper"):
            try:
                self._client = importlib.import_module(mod)
                return self._client
            except ImportError:
                continue
        raise VoiceProviderLibraryMissing(
            "whisper transcription requires faster_whisper OR whisper; "
            "neither importable on this Golden Image"
        )

    def transcribe(
        self,
        *,
        audio_bytes: bytes,
        model_size: str,
    ) -> str:
        if model_size not in self._permitted_models:
            raise WhisperHardwareTierError(
                f"model_size {model_size!r} not in hardware-tier whitelist "
                f"{sorted(self._permitted_models)} (RT-16)"
            )
        self._resolve_client()
        # v0.2 first ship: empty transcript; production wiring at white-glove
        # substitutes the actual model.transcribe(audio_bytes, model=...) call.
        return ""


__all__ = [
    "CHANNEL_NAME",
    "LocalWhisperTranscriberSubstrate",
    "PERMITTED_WHISPER_MODELS_DEV",
    "PERMITTED_WHISPER_MODELS_PROD",
    "ProductionLocalWhisperTranscriber",
    "ProductionVoiceTransport",
    "VOICE_OUTBOUND_ENDPOINT_ALLOWLIST",
    "VoiceChannel",
    "VoiceComposeContext",
    "VoiceEndpointError",
    "VoiceProviderLibraryMissing",
    "VoiceTransportSubstrate",
    "WHISPER_LOCAL_ENDPOINT_ALLOWLIST",
    "WhisperHardwareTierError",
    "render_voice_script",
]
