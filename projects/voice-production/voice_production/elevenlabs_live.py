"""Effect-owning ElevenLabs direct-TTS adapter for bounded local auditions.

This module is deliberately separate from the pure L0/L1 preparation modules.
It performs one provider request only when a caller supplies a bounded secret
consumer.  Secret material is never returned by this API, and provider errors
are reduced to status metadata rather than echoing response bodies.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Callable, Mapping, cast

from .canonical import JsonValue, canonical_sha256


LIVE_ADAPTER_ID = "elevenlabs-direct-tts-live"
LIVE_ADAPTER_VERSION = "1"
ELEVENLABS_API_ORIGIN = "https://api.elevenlabs.io"
SUPPORTED_MODEL_ID = "eleven_v3"
SUPPORTED_MODEL_IDS = frozenset({SUPPORTED_MODEL_ID, "eleven_multilingual_v2"})
SUPPORTED_OUTPUT_FORMAT = "mp3_44100_128"
MAX_AUDIO_BYTES = 50 * 1024 * 1024

_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
_VOICE_ID_RE = re.compile(r"[A-Za-z0-9]{10,64}\Z")
_SAFE_PROVIDER_STATUS_RE = re.compile(r"[a-z0-9_-]{1,96}\Z")


class LiveAdapterError(RuntimeError):
    """Base failure for a rejected or unsuccessful live request."""


class LiveRequestInvalid(LiveAdapterError):
    """Raised before secret resolution when request input is invalid."""


class ProviderRequestFailed(LiveAdapterError):
    """Raised when ElevenLabs rejects a request or returns invalid audio."""

    def __init__(self, http_status: int, provider_status: str | None = None) -> None:
        self.http_status = http_status
        self.provider_status = provider_status
        suffix = f" ({provider_status})" if provider_status else ""
        super().__init__(f"ElevenLabs request failed with HTTP {http_status}{suffix}")


@dataclass(frozen=True, slots=True)
class DirectTtsRequest:
    """One exact source segment bound to one non-secret provider voice."""

    segment_id: str
    speaker: str
    exact_text: str
    exact_text_sha256: str
    voice_id: str
    voice_label: str
    model_id: str = SUPPORTED_MODEL_ID
    output_format: str = SUPPORTED_OUTPUT_FORMAT
    language_code: str | None = "en"
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True
    speed: float | None = None
    seed: int | None = None
    previous_text: str | None = None
    next_text: str | None = None

    def __post_init__(self) -> None:
        for label, value in (
            ("segment_id", self.segment_id),
            ("speaker", self.speaker),
            ("exact_text", self.exact_text),
            ("voice_label", self.voice_label),
        ):
            if type(value) is not str or not value or value.strip() != value:
                raise LiveRequestInvalid(f"{label} must be non-empty trimmed text")
        if type(self.exact_text_sha256) is not str or _SHA256_RE.fullmatch(
            self.exact_text_sha256
        ) is None:
            raise LiveRequestInvalid("exact_text_sha256 must be lowercase SHA-256")
        if hashlib.sha256(self.exact_text.encode("utf-8")).hexdigest() != self.exact_text_sha256:
            raise LiveRequestInvalid("exact text does not match its digest")
        if len(self.exact_text) > 5000:
            raise LiveRequestInvalid("TTS input exceeds the local 5000-character cap")
        if type(self.voice_id) is not str or _VOICE_ID_RE.fullmatch(self.voice_id) is None:
            raise LiveRequestInvalid("voice_id has invalid syntax")
        if self.model_id not in SUPPORTED_MODEL_IDS:
            raise LiveRequestInvalid(
                f"model_id must be one of {sorted(SUPPORTED_MODEL_IDS)}"
            )
        if self.output_format != SUPPORTED_OUTPUT_FORMAT:
            raise LiveRequestInvalid(
                f"output_format must be {SUPPORTED_OUTPUT_FORMAT}"
            )
        if self.language_code is not None:
            if (
                type(self.language_code) is not str
                or not self.language_code
                or self.language_code.strip() != self.language_code
            ):
                raise LiveRequestInvalid("language_code must be null or trimmed text")
            if self.language_code != "en":
                raise LiveRequestInvalid(
                    "the pilot adapter currently supports only language_code en"
                )
        if self.model_id == "eleven_multilingual_v2" and self.language_code is not None:
            raise LiveRequestInvalid(
                "language_code must be null for eleven_multilingual_v2"
            )
        for label, value in (
            ("previous_text", self.previous_text),
            ("next_text", self.next_text),
        ):
            if value is None:
                continue
            if type(value) is not str or not value or value.strip() != value:
                raise LiveRequestInvalid(f"{label} must be null or non-empty trimmed text")
            if len(value) > 5000:
                raise LiveRequestInvalid(f"{label} exceeds the local 5000-character cap")
        for label, value in (
            ("stability", self.stability),
            ("similarity_boost", self.similarity_boost),
            ("style", self.style),
        ):
            if type(value) is not float or not 0.0 <= value <= 1.0:
                raise LiveRequestInvalid(f"{label} must be a float between 0 and 1")
        if type(self.use_speaker_boost) is not bool:
            raise LiveRequestInvalid("use_speaker_boost must be boolean")
        if self.speed is not None and (
            type(self.speed) is not float or not 0.7 <= self.speed <= 1.2
        ):
            raise LiveRequestInvalid("speed must be null or a float from 0.7 to 1.2")
        if self.seed is not None and (
            type(self.seed) is not int or not 0 <= self.seed <= 4_294_967_295
        ):
            raise LiveRequestInvalid("seed must be an integer from 0 to 4294967295")

    @property
    def body(self) -> dict[str, JsonValue]:
        voice_settings: dict[str, JsonValue] = {
            "similarity_boost": self.similarity_boost,
            "stability": self.stability,
            "style": self.style,
            "use_speaker_boost": self.use_speaker_boost,
        }
        if self.speed is not None:
            voice_settings["speed"] = self.speed
        value: dict[str, JsonValue] = {
            "model_id": self.model_id,
            "text": self.exact_text,
            "voice_settings": voice_settings,
        }
        if self.language_code is not None:
            value["language_code"] = self.language_code
        if self.seed is not None:
            value["seed"] = self.seed
        if self.previous_text is not None:
            value["previous_text"] = self.previous_text
        if self.next_text is not None:
            value["next_text"] = self.next_text
        return value

    @property
    def request_digest(self) -> str:
        return canonical_sha256(
            {
                "adapter_id": LIVE_ADAPTER_ID,
                "adapter_version": LIVE_ADAPTER_VERSION,
                "body": self.body,
                "method": "POST",
                "output_format": self.output_format,
                "path_template": "/v1/text-to-speech/{voice_id}",
                "segment_id": self.segment_id,
                "speaker": self.speaker,
                "voice_id": self.voice_id,
            }
        )


@dataclass(frozen=True, slots=True)
class TransportResponse:
    status_code: int
    headers: Mapping[str, str]
    body: bytes


@dataclass(frozen=True, slots=True)
class LiveSynthesisResult:
    """Audio bytes plus a deliberately redacted provider observation."""

    request_digest: str
    audio_bytes: bytes
    content_type: str
    request_id: str | None
    history_item_id: str | None
    character_cost: int | None
    secret_execution_receipt_digest: str | None

    @property
    def audio_sha256(self) -> str:
        return hashlib.sha256(self.audio_bytes).hexdigest()

    def safe_summary(self) -> dict[str, JsonValue]:
        return {
            "adapter_id": LIVE_ADAPTER_ID,
            "adapter_version": LIVE_ADAPTER_VERSION,
            "audio_sha256": self.audio_sha256,
            "audio_size_bytes": len(self.audio_bytes),
            "character_cost": self.character_cost,
            "content_type": self.content_type,
            "history_item_id": self.history_item_id,
            "http_status": 200,
            "request_digest": self.request_digest,
            "request_id": self.request_id,
            "secret_execution_receipt_digest": self.secret_execution_receipt_digest,
        }


Transport = Callable[[str, Mapping[str, str], bytes, float], TransportResponse]
SecretConsumer = Callable[
    [str, Callable[[memoryview], None]], Mapping[str, JsonValue]
]


def _safe_provider_status(payload: bytes) -> str | None:
    try:
        value = json.loads(payload.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if type(value) is not dict:
        return None
    detail = value.get("detail")
    status: object = detail.get("status") if type(detail) is dict else None
    if type(status) is str and _SAFE_PROVIDER_STATUS_RE.fullmatch(status):
        return status
    return None


def urllib_transport(
    url: str,
    headers: Mapping[str, str],
    body: bytes,
    timeout_seconds: float,
) -> TransportResponse:
    """Perform the pinned HTTPS POST and retain only response bytes/headers."""

    if not url.startswith(f"{ELEVENLABS_API_ORIGIN}/v1/text-to-speech/"):
        raise LiveRequestInvalid("transport target is outside the ElevenLabs origin")
    request = urllib.request.Request(
        url,
        data=body,
        headers=dict(headers),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return TransportResponse(
                status_code=response.status,
                headers={key.casefold(): value for key, value in response.headers.items()},
                body=response.read(MAX_AUDIO_BYTES + 1),
            )
    except urllib.error.HTTPError as error:
        return TransportResponse(
            status_code=error.code,
            headers={key.casefold(): value for key, value in error.headers.items()},
            body=error.read(8192),
        )
    except urllib.error.URLError:
        return TransportResponse(
            status_code=599,
            headers={"content-type": "application/json"},
            body=b'{"detail":{"status":"transport_error"}}',
        )


def _header(headers: Mapping[str, str], *names: str) -> str | None:
    lowered = {str(key).casefold(): str(value) for key, value in headers.items()}
    for name in names:
        value = lowered.get(name.casefold())
        if value:
            return value
    return None


def _optional_nonnegative_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        parsed = int(value)
    except ValueError:
        return None
    return parsed if parsed >= 0 else None


def _looks_like_mp3(payload: bytes) -> bool:
    return len(payload) >= 4 and (
        payload.startswith(b"ID3")
        or (payload[0] == 0xFF and payload[1] & 0xE0 == 0xE0)
    )


def synthesize_direct_tts(
    request: DirectTtsRequest,
    *,
    secret_consumer: SecretConsumer,
    transport: Transport = urllib_transport,
    timeout_seconds: float = 30.0,
) -> LiveSynthesisResult:
    """Resolve one credential and submit exactly one direct-TTS request."""

    if type(request) is not DirectTtsRequest:
        raise LiveRequestInvalid("request must be DirectTtsRequest")
    if not callable(secret_consumer) or not callable(transport):
        raise LiveRequestInvalid("secret consumer and transport must be callable")
    if type(timeout_seconds) is not float or not 1.0 <= timeout_seconds <= 120.0:
        raise LiveRequestInvalid("timeout_seconds must be a float from 1 to 120")

    body = json.dumps(
        request.body,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    encoded_voice_id = urllib.parse.quote(request.voice_id, safe="")
    query = urllib.parse.urlencode({"output_format": request.output_format})
    url = f"{ELEVENLABS_API_ORIGIN}/v1/text-to-speech/{encoded_voice_id}?{query}"
    observed: list[TransportResponse] = []

    def perform(secret: memoryview) -> None:
        if observed:
            raise LiveAdapterError("secret consumer invoked callback more than once")
        key_bytes = bytearray(secret)
        try:
            try:
                key_text = key_bytes.decode("ascii", errors="strict")
            except UnicodeDecodeError as error:
                raise LiveRequestInvalid("API key is not ASCII") from error
            response = transport(
                url,
                {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": key_text,
                },
                body,
                timeout_seconds,
            )
            observed.append(response)
            key_text = ""
        finally:
            for index in range(len(key_bytes)):
                key_bytes[index] = 0

    secret_receipt = secret_consumer(request.request_digest, perform)
    if len(observed) != 1:
        raise LiveAdapterError("secret consumer did not execute exactly one request")
    response = observed[0]
    if response.status_code != 200:
        raise ProviderRequestFailed(
            response.status_code,
            _safe_provider_status(response.body),
        )
    if len(response.body) > MAX_AUDIO_BYTES:
        raise ProviderRequestFailed(502, "audio_response_too_large")
    content_type = (_header(response.headers, "content-type") or "").split(";", 1)[0]
    if content_type not in {"audio/mpeg", "audio/mp3"} or not _looks_like_mp3(
        response.body
    ):
        raise ProviderRequestFailed(502, "invalid_mp3_response")
    receipt_digest: str | None = None
    if type(secret_receipt) is dict:
        candidate = secret_receipt.get("digest")
        if type(candidate) is str and _SHA256_RE.fullmatch(candidate):
            receipt_digest = candidate
    return LiveSynthesisResult(
        request_digest=request.request_digest,
        audio_bytes=bytes(response.body),
        content_type=content_type,
        request_id=_header(response.headers, "request-id", "x-request-id"),
        history_item_id=_header(response.headers, "history-item-id"),
        character_cost=_optional_nonnegative_int(
            _header(response.headers, "character-cost", "x-character-count")
        ),
        secret_execution_receipt_digest=receipt_digest,
    )


__all__ = [
    "DirectTtsRequest",
    "ELEVENLABS_API_ORIGIN",
    "LIVE_ADAPTER_ID",
    "LIVE_ADAPTER_VERSION",
    "LiveAdapterError",
    "LiveRequestInvalid",
    "LiveSynthesisResult",
    "ProviderRequestFailed",
    "SUPPORTED_MODEL_ID",
    "SUPPORTED_MODEL_IDS",
    "SUPPORTED_OUTPUT_FORMAT",
    "TransportResponse",
    "synthesize_direct_tts",
    "urllib_transport",
]
