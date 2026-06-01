"""§13.5.2 + §13.6.x Inbound parser dispatcher.

Per §13 Data Collector v1 LOCKED 2026-05-10.

Channel-agnostic dispatcher to per-channel parser. Inbound parsing is
ALWAYS-LOCAL per §13.10.2 — voice transcription via local Whisper, all
other channels via standard library / local parsing tools.

Each channel module registers its parser as a callable conforming to the
``ChannelInboundParserCallable`` Protocol; this dispatcher delegates by
channel name, normalizes to ``InboundResponse``, and feeds the result to
the field-validator + token-validator pipeline.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Final, Mapping, Optional, Protocol, runtime_checkable

# Re-export ParsedField from field_validator so both modules share one
# canonical dataclass and the inbound-parser dispatcher can hand a ParsedField
# directly to validate / drift helpers.
from pipeline.orchestrator.seats.data_collector.field_validator import (
    ParsedField,
)

PERMITTED_CHANNELS: Final[frozenset[str]] = frozenset({
    "email",
    "sms",
    "voice",
    "telegram",
    "whatsapp",
})


@runtime_checkable
class ChannelInboundParserCallable(Protocol):
    """Per-channel inbound parser callable."""

    def __call__(
        self,
        *,
        raw_payload: bytes,
        receipt_metadata: Mapping[str, object],
    ) -> Mapping[str, object]: ...


@dataclass(frozen=True, kw_only=True)
class ParsedInbound:
    """Output of the inbound parser dispatcher."""

    channel: str
    parsed_fields: tuple[ParsedField, ...]
    raw_payload_sha3_512: bytes
    received_at_utc: datetime
    extracted_token_value: Optional[bytes] = None
    sender_metadata: Mapping[str, object] = field(default_factory=dict)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class InboundParserDispatcher:
    """Channel-agnostic dispatcher.

    Per-channel parser callables are registered at construction (keyed by
    channel name); ``parse(channel, raw_payload, receipt_metadata)``
    delegates to the registered parser and normalizes the output to
    ``ParsedInbound``.
    """

    def __init__(
        self,
        *,
        parsers: Mapping[str, ChannelInboundParserCallable],
    ) -> None:
        for ch in parsers:
            if ch not in PERMITTED_CHANNELS:
                raise ValueError(
                    f"channel {ch!r} not in {sorted(PERMITTED_CHANNELS)}"
                )
        self._parsers = dict(parsers)

    def registered_channels(self) -> frozenset[str]:
        return frozenset(self._parsers.keys())

    def parse(
        self,
        *,
        channel: str,
        raw_payload: bytes,
        receipt_metadata: Mapping[str, object],
        received_at_utc: Optional[datetime] = None,
    ) -> ParsedInbound:
        if channel not in self._parsers:
            raise ValueError(
                f"channel {channel!r} not registered in dispatcher; "
                f"registered={sorted(self._parsers)}"
            )
        parser = self._parsers[channel]
        result = parser(raw_payload=raw_payload, receipt_metadata=receipt_metadata)
        if not isinstance(result, Mapping):
            raise TypeError(
                f"channel {channel!r} parser returned non-Mapping "
                f"{type(result).__name__}"
            )

        fields_raw = result.get("parsed_fields", [])
        parsed_fields: list[ParsedField] = []
        if isinstance(fields_raw, (list, tuple)):
            for item in fields_raw:
                if isinstance(item, ParsedField):
                    parsed_fields.append(item)
                    continue
                if not isinstance(item, Mapping):
                    continue
                field_class = item.get("field_class")
                if not isinstance(field_class, str):
                    continue
                raw_value = item.get("raw_value", item.get("value"))
                numeric_value: Optional[Decimal] = None
                num_raw = item.get("numeric_value", raw_value)
                if isinstance(num_raw, Decimal):
                    numeric_value = num_raw
                elif isinstance(num_raw, (int, float)) and not isinstance(num_raw, bool):
                    try:
                        numeric_value = Decimal(repr(num_raw))
                    except (TypeError, ValueError):
                        numeric_value = None
                elif isinstance(num_raw, str):
                    try:
                        numeric_value = Decimal(num_raw)
                    except Exception:  # noqa: BLE001
                        numeric_value = None
                unit = item.get("unit")
                kfr_ref = item.get("kfr_fact_ref")
                parsed_fields.append(
                    ParsedField(
                        field_class=field_class,
                        raw_value=raw_value,
                        numeric_value=numeric_value,
                        unit=unit if isinstance(unit, str) else None,
                        kfr_fact_ref=kfr_ref if isinstance(kfr_ref, str) else None,
                    )
                )
        token_raw = result.get("extracted_token_value")
        token_bytes: Optional[bytes] = None
        if isinstance(token_raw, (bytes, bytearray)):
            token_bytes = bytes(token_raw)
        elif isinstance(token_raw, str):
            try:
                token_bytes = bytes.fromhex(token_raw)
            except ValueError:
                token_bytes = token_raw.encode("utf-8")

        sender_metadata = result.get("sender_metadata", {})
        if not isinstance(sender_metadata, Mapping):
            sender_metadata = {}

        return ParsedInbound(
            channel=channel,
            parsed_fields=tuple(parsed_fields),
            raw_payload_sha3_512=hashlib.sha3_512(raw_payload).digest(),
            received_at_utc=received_at_utc or _utc_now(),
            extracted_token_value=token_bytes,
            sender_metadata=dict(sender_metadata),
        )


__all__ = [
    "PERMITTED_CHANNELS",
    "ChannelInboundParserCallable",
    "InboundParserDispatcher",
    "ParsedField",
    "ParsedInbound",
]
