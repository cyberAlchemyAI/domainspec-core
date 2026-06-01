"""§13.13.12 — InboundParserDispatcher tests.

Verify channel-agnostic dispatch + ParsedField normalization.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from pipeline.orchestrator.seats.data_collector.inbound_parser import (
    InboundParserDispatcher,
    PERMITTED_CHANNELS,
    ParsedField,
    ParsedInbound,
)


def _email_parser(*, raw_payload: bytes, receipt_metadata: dict) -> dict:
    return {
        "parsed_fields": [
            {
                "field_class": "narrative",
                "raw_value": raw_payload.decode("utf-8", errors="replace"),
                "numeric_value": None,
                "unit": None,
                "kfr_fact_ref": None,
            }
        ],
        "extracted_token_value": b"t_001",
        "sender_metadata": {"from": "alice@example.invalid"},
    }


def _sms_parser(*, raw_payload: bytes, receipt_metadata: dict) -> dict:
    return {
        "parsed_fields": [
            {
                "field_class": "numeric_metric",
                "raw_value": "312",
                "numeric_value": "312",
                "unit": "graduates",
                "kfr_fact_ref": "kfr_grad_count",
            }
        ],
        "extracted_token_value": b"t_002",
        "sender_metadata": {"From": receipt_metadata.get("From")},
    }


def test_dispatcher_rejects_unknown_channel_at_register_time():
    with pytest.raises(ValueError, match="not in"):
        InboundParserDispatcher(parsers={"slack": _email_parser})  # type: ignore[dict-item]


def test_dispatcher_registered_channels():
    dispatcher = InboundParserDispatcher(
        parsers={"email": _email_parser, "sms": _sms_parser},
    )
    assert dispatcher.registered_channels() == frozenset({"email", "sms"})


def test_dispatcher_dispatches_email():
    dispatcher = InboundParserDispatcher(parsers={"email": _email_parser})
    parsed = dispatcher.parse(
        channel="email",
        raw_payload=b"Hello",
        receipt_metadata={},
    )
    assert isinstance(parsed, ParsedInbound)
    assert parsed.channel == "email"
    assert parsed.extracted_token_value == b"t_001"
    assert len(parsed.parsed_fields) == 1
    assert isinstance(parsed.parsed_fields[0], ParsedField)
    assert parsed.parsed_fields[0].field_class == "narrative"
    assert len(parsed.raw_payload_sha3_512) == 64  # SHA3-512 = 64 bytes


def test_dispatcher_normalizes_numeric_value_string_to_decimal():
    from decimal import Decimal

    dispatcher = InboundParserDispatcher(parsers={"sms": _sms_parser})
    parsed = dispatcher.parse(
        channel="sms",
        raw_payload=b"312",
        receipt_metadata={"From": "+15555550199"},
    )
    field = parsed.parsed_fields[0]
    assert field.field_class == "numeric_metric"
    assert field.numeric_value == Decimal("312")
    assert field.unit == "graduates"
    assert field.kfr_fact_ref == "kfr_grad_count"


def test_dispatcher_unknown_channel_raises():
    dispatcher = InboundParserDispatcher(parsers={"email": _email_parser})
    with pytest.raises(ValueError, match="not registered"):
        dispatcher.parse(channel="sms", raw_payload=b"", receipt_metadata={})


def test_permitted_channels_immutable_set():
    assert PERMITTED_CHANNELS == frozenset(
        {"email", "sms", "voice", "telegram", "whatsapp"}
    )
