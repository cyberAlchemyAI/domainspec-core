"""§13.6.x — Per-channel behavioral tests.

Per §13 Data Collector v1 LOCKED 2026-05-10 §13.13.1 channel dispatch tests
+ per-channel sanity tests covering compose / parse / token validation
under the substrate-DI Protocol pattern.

These tests do NOT invoke real Twilio / SMTP / MTProto / WhatsApp
substrates — production transport adapters are out of scope per the WS-I
task. Substrates are stubbed via test doubles conforming to the channel
substrate Protocols.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from pipeline.orchestrator.seats.data_collector import (
    ChannelProtocol,
    OutboundMessage,
    SignedBatchEnvelope,
    SubAwardeeToken,
)
from pipeline.orchestrator.seats.data_collector.email_channel import (
    CHANNEL_NAME as EMAIL_CHANNEL_NAME,
    EmailChannel,
    EmailComposeContext,
    X_TILTH_RECIPIENT_TOKEN_HEADER,
)
from pipeline.orchestrator.seats.data_collector.sms_channel import (
    CHANNEL_NAME as SMS_CHANNEL_NAME,
    SMS_MAX_BODY_BYTES,
    SmsBodyOverflowError,
    SmsChannel,
    SmsComposeContext,
    extract_token_from_body,
    render_sms_body,
)
from pipeline.orchestrator.seats.data_collector.voice_channel import (
    CHANNEL_NAME as VOICE_CHANNEL_NAME,
    PERMITTED_WHISPER_MODELS_DEV,
    PERMITTED_WHISPER_MODELS_PROD,
    VoiceChannel,
    VoiceComposeContext,
    render_voice_script,
)
from pipeline.orchestrator.seats.data_collector.telegram_channel import (
    CHANNEL_NAME as TELEGRAM_CHANNEL_NAME,
    OrgScopedBot,
    OrgScopedBotSubclassError,
    REJECTED_CHAT_TYPES,
    TelegramChannel,
    cross_org_chat_id_resolver,
)
from pipeline.orchestrator.seats.data_collector.whatsapp_channel import (
    CHANNEL_NAME as WHATSAPP_CHANNEL_NAME,
    WhatsAppChannel,
    WhatsAppComposeContext,
    WhatsAppTemplateUnapprovedError,
    is_inside_24h_window,
)


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _make_token(channel: str) -> SubAwardeeToken:
    now = datetime.now(timezone.utc)
    return SubAwardeeToken(
        token_id="t_test_001",
        grant_id="g_test",
        recipient_id="r_test",
        channel_binding=channel,  # type: ignore[arg-type]
        secret_value_ciphertext=b"\x00" * 32,
        aead_nonce=b"\x00" * 12,
        issued_at_utc=now,
        rotates_at_utc=now + timedelta(days=365),
        revoked=False,
        revoked_at_utc=None,
        operator_signature=b"\x00" * 64,
    )


def _make_signed_batch(
    *,
    grant_id: str = "g_test",
    org_slug: str = "o_test",
    status: str = "APPROVED_FOR_SEND",
    signature: bytes = b"\x01" * 64,
) -> SignedBatchEnvelope:
    return SignedBatchEnvelope(
        batch_id="b_test_001",
        compose_run_id="r_compose_001",
        grant_id=grant_id,
        org_slug=org_slug,
        period_n=1,
        batch_status=status,  # type: ignore[arg-type]
        batch_content_sha3_512="0" * 128,
        batch_manifest_sha3_512="0" * 128,
        approved_recipient_order=["r_test"],
        per_recipient_consent_state_sha3_512_full={"r_test": "0" * 128},
        signed_at_utc=datetime.now(timezone.utc),
        signed_by="op_test",
        signature=signature,
    )


# ---------------------------------------------------------------------------
# Email channel
# ---------------------------------------------------------------------------


def test_email_channel_implements_protocol():
    ch = EmailChannel()
    assert isinstance(ch, ChannelProtocol)
    assert ch.channel_name == "email"
    assert EMAIL_CHANNEL_NAME == "email"


def test_email_compose_includes_token_header():
    ch = EmailChannel()
    token = _make_token("email")
    recipient = {
        "recipient_id": "r_test",
        "contact_email": "alice@example.invalid",
        "email_compose_context": {
            "envelope_from": "grants@example.invalid",
            "envelope_to": "alice@example.invalid",
            "subject": "Test",
            "body_text": "How many graduates this period?",
            "can_spam_unsubscribe_url": "https://example.invalid/u",
        },
    }
    msg = ch.compose_outbound(
        org_slug="o_test",
        grant_id="g_test",
        recipient=recipient,
        commitment_id_or_funder_reporting_field_id="commit_001",
        per_state_disclaimers=[],
        per_recipient_token=token,
    )
    assert msg.channel == "email"
    assert msg.per_recipient_token_id == token.token_id
    assert len(msg.rendered_message_bytes_sha3_512) == 128


def test_email_send_refuses_unsigned_batch():
    ch = EmailChannel()
    msg = OutboundMessage(
        outbound_id="o_001",
        dc_run_id="r_001",
        recipient_id="r_test",
        channel="email",
        grant_id="g_test",
        org_slug="o_test",
        commitment_id_or_funder_reporting_field_id="c_001",
        rendered_message_bytes_sha3_512="a" * 128,
        per_state_disclaimers_applied=[],
        per_recipient_token_id="t_001",
        staged_at_utc=datetime.now(timezone.utc),
        sent_at_utc=None,
        per_recipient_signature=b"",
    )
    sig_envelope = _make_signed_batch(signature=b"")
    result = ch.send(message=msg, operator_batch_signature=sig_envelope)
    assert result["sent"] is False
    assert result["reason"] == "operator_signature_invalid"


def test_email_parse_inbound_extracts_x_tilth_token():
    ch = EmailChannel()
    rfc822 = (
        "From: alice@example.invalid\r\n"
        "To: grants@example.invalid\r\n"
        "Subject: Re: question\r\n"
        f"{X_TILTH_RECIPIENT_TOKEN_HEADER}: t_test_001\r\n"
        "MIME-Version: 1.0\r\n"
        "Content-Type: text/plain; charset=utf-8\r\n"
        "\r\n"
        "We had 312 graduates this period.\r\n"
    ).encode("utf-8")
    parsed = ch.parse_inbound(raw_payload=rfc822, receipt_metadata={})
    assert parsed["extracted_token_value"] == b"t_test_001"
    assert parsed["sender_metadata"]["from"] == "alice@example.invalid"
    assert parsed["parsed_fields"][0]["field_class"] == "narrative"


def test_email_validate_inbound_token_channel_binding_mismatch():
    ch = EmailChannel()
    token = _make_token("sms")  # wrong channel
    result = ch.validate_inbound_token(inbound=None, expected_token=token)
    assert result["valid"] is False
    assert result["reason"] == "channel_binding_mismatch"


# ---------------------------------------------------------------------------
# SMS channel
# ---------------------------------------------------------------------------


def test_sms_channel_implements_protocol():
    ch = SmsChannel()
    assert isinstance(ch, ChannelProtocol)
    assert ch.channel_name == "sms"
    assert SMS_CHANNEL_NAME == "sms"


def test_sms_render_body_within_size_cap():
    ctx = SmsComposeContext(
        from_number="+15555550100",
        to_number="+15555550199",
        question_text="How many?",
        opt_out_short_link="https://t.invalid/x",
    )
    rendered = render_sms_body(ctx=ctx, token_id="t_001")
    assert len(rendered) <= SMS_MAX_BODY_BYTES
    assert b"[T:t_001]" in rendered


def test_sms_render_body_overflow_raises():
    ctx = SmsComposeContext(
        from_number="+15555550100",
        to_number="+15555550199",
        question_text="X" * 2000,
        opt_out_short_link="https://t.invalid/x",
    )
    with pytest.raises(SmsBodyOverflowError):
        render_sms_body(ctx=ctx, token_id="t_001")


def test_sms_extract_token_from_body():
    body = "[T:abc-123] Reply with the count."
    assert extract_token_from_body(body) == "abc-123"


def test_sms_parse_inbound_detects_stop_signal():
    ch = SmsChannel()
    parsed = ch.parse_inbound(
        raw_payload=b"STOP",
        receipt_metadata={"From": "+15555550199", "MessageSid": "SM123"},
    )
    assert parsed["sender_metadata"]["is_opt_out_signal"] is True


# ---------------------------------------------------------------------------
# Voice channel
# ---------------------------------------------------------------------------


def test_voice_channel_implements_protocol():
    ch = VoiceChannel()
    assert isinstance(ch, ChannelProtocol)
    assert ch.channel_name == "voice"
    assert VOICE_CHANNEL_NAME == "voice"


def test_voice_dev_tier_rejects_large_v3():
    with pytest.raises(ValueError, match="not in tier whitelist"):
        VoiceChannel(whisper_model_size="large-v3")


def test_voice_prod_tier_accepts_large_v3():
    ch = VoiceChannel(
        whisper_model_size="large-v3",
        permitted_whisper_models=PERMITTED_WHISPER_MODELS_PROD,
    )
    assert ch.channel_name == "voice"


def test_voice_render_script_includes_token_reference():
    ctx = VoiceComposeContext(
        from_number="+15555550100",
        to_number="+15555550199",
        question_text="How many?",
        state_disclosure_script="This is an automated message.",
    )
    script = render_voice_script(ctx=ctx, token_id="t_001")
    assert "Reference token t_001" in script
    assert "automated message" in script.lower()


def test_voice_parse_inbound_without_whisper_returns_skipped_reason():
    ch = VoiceChannel()  # no whisper substrate injected
    parsed = ch.parse_inbound(
        raw_payload=b"\x00\x00\x00",  # fake audio
        receipt_metadata={"From": "+15555550199"},
    )
    assert parsed["sender_metadata"]["transcription_skipped_reason"] == (
        "whisper_substrate_not_wired"
    )


# ---------------------------------------------------------------------------
# Telegram channel + OrgScopedBot
# ---------------------------------------------------------------------------


def test_orgscoped_bot_requires_org_slug_in_session_path():
    with pytest.raises(RuntimeError, match="missing org_slug"):
        OrgScopedBot(
            org_slug="orgA",
            session_path="/tmp/random/session.session",  # no orgA
        )


def test_orgscoped_bot_default_session_path_includes_org_slug():
    bot = OrgScopedBot(org_slug="orgA")
    assert "orgA" in bot.session_path


def test_orgscoped_bot_subclass_rejected():
    with pytest.raises(OrgScopedBotSubclassError):
        class _Sub(OrgScopedBot):  # noqa: N801
            pass

        _Sub(org_slug="orgA")


def test_telegram_channel_implements_protocol():
    bot = OrgScopedBot(org_slug="orgA")
    ch = TelegramChannel(bot=bot)
    assert isinstance(ch, ChannelProtocol)
    assert ch.channel_name == "telegram"
    assert TELEGRAM_CHANNEL_NAME == "telegram"


def test_telegram_parse_inbound_rejects_group_chat():
    bot = OrgScopedBot(org_slug="orgA")
    ch = TelegramChannel(bot=bot)
    parsed = ch.parse_inbound(
        raw_payload=b"hello",
        receipt_metadata={"chat_type": "group", "chat_id": 123},
    )
    assert parsed["sender_metadata"]["rejected_reason"] == (
        "telegram_group_chat_rejected"
    )
    assert parsed["parsed_fields"] == []


def test_telegram_send_refuses_cross_org():
    bot = OrgScopedBot(org_slug="orgA")
    ch = TelegramChannel(bot=bot)
    msg = OutboundMessage(
        outbound_id="o_001",
        dc_run_id="r_001",
        recipient_id="r_test",
        channel="telegram",
        grant_id="g_test",
        org_slug="orgB",  # different from bot's orgA
        commitment_id_or_funder_reporting_field_id="c_001",
        rendered_message_bytes_sha3_512="a" * 128,
        per_state_disclaimers_applied=[],
        per_recipient_token_id="t_001",
        staged_at_utc=datetime.now(timezone.utc),
        sent_at_utc=None,
        per_recipient_signature=b"",
    )
    sig = _make_signed_batch(org_slug="orgB", signature=b"\x01" * 64)
    result = ch.send(message=msg, operator_batch_signature=sig)
    assert result["sent"] is False
    assert result["reason"] == "mtproto_cross_org"


def test_cross_org_chat_id_resolver_collision_returns_multiple_matches():
    resolved, matches = cross_org_chat_id_resolver(
        chat_id=123,
        per_org_consent_ledgers={
            "orgA": frozenset({123, 456}),
            "orgB": frozenset({123}),
        },
    )
    assert resolved is None
    assert sorted(matches) == ["orgA", "orgB"]


def test_cross_org_chat_id_resolver_single_match():
    resolved, matches = cross_org_chat_id_resolver(
        chat_id=456,
        per_org_consent_ledgers={
            "orgA": frozenset({456}),
            "orgB": frozenset({999}),
        },
    )
    assert resolved == "orgA"


# ---------------------------------------------------------------------------
# WhatsApp channel
# ---------------------------------------------------------------------------


def test_whatsapp_channel_implements_protocol():
    ch = WhatsAppChannel()
    assert isinstance(ch, ChannelProtocol)
    assert ch.channel_name == "whatsapp"
    assert WHATSAPP_CHANNEL_NAME == "whatsapp"


def test_whatsapp_24h_window_inside_returns_true():
    last_inbound = datetime.now(timezone.utc) - timedelta(hours=12)
    assert is_inside_24h_window(last_inbound_at_utc=last_inbound) is True


def test_whatsapp_24h_window_outside_returns_false():
    last_inbound = datetime.now(timezone.utc) - timedelta(hours=48)
    assert is_inside_24h_window(last_inbound_at_utc=last_inbound) is False


def test_whatsapp_24h_window_no_prior_inbound_returns_false():
    assert is_inside_24h_window(last_inbound_at_utc=None) is False


def test_whatsapp_compose_outside_window_unapproved_template_raises():
    ch = WhatsAppChannel(approved_template_ids=frozenset({"approved_001"}))
    token = _make_token("whatsapp")
    recipient = {
        "recipient_id": "r_test",
        "contact_phone": "+15555550199",
        "last_inbound_at_utc": datetime.now(timezone.utc) - timedelta(hours=48),
        "whatsapp_compose_context": {
            "to_phone": "+15555550199",
            "question_text": "How many?",
            "template_id": "not_approved",
        },
    }
    with pytest.raises(WhatsAppTemplateUnapprovedError):
        ch.compose_outbound(
            org_slug="o_test",
            grant_id="g_test",
            recipient=recipient,
            commitment_id_or_funder_reporting_field_id="c_001",
            per_state_disclaimers=[],
            per_recipient_token=token,
        )


def test_whatsapp_compose_inside_window_no_template_required():
    ch = WhatsAppChannel()
    token = _make_token("whatsapp")
    recipient = {
        "recipient_id": "r_test",
        "contact_phone": "+15555550199",
        "last_inbound_at_utc": datetime.now(timezone.utc) - timedelta(hours=2),
        "whatsapp_compose_context": {
            "to_phone": "+15555550199",
            "question_text": "How many graduates?",
        },
    }
    msg = ch.compose_outbound(
        org_slug="o_test",
        grant_id="g_test",
        recipient=recipient,
        commitment_id_or_funder_reporting_field_id="c_001",
        per_state_disclaimers=[],
        per_recipient_token=token,
    )
    assert msg.channel == "whatsapp"
    assert msg.per_recipient_token_id == token.token_id


# ---------------------------------------------------------------------------
# Cross-channel — five channels register and dispatcher coverage
# ---------------------------------------------------------------------------


def test_five_channels_all_implement_protocol():
    channels: dict[str, ChannelProtocol] = {
        "email": EmailChannel(),
        "sms": SmsChannel(),
        "voice": VoiceChannel(),
        "telegram": TelegramChannel(bot=OrgScopedBot(org_slug="orgA")),
        "whatsapp": WhatsAppChannel(),
    }
    assert len(channels) == 5
    for name, ch in channels.items():
        assert isinstance(ch, ChannelProtocol), f"{name} fails Protocol check"
        assert ch.channel_name == name
