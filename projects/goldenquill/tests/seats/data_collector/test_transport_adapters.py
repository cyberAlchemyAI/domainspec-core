"""§13.8.x — Production transport adapter tests.

Per §13.8.1 through §13.8.5 endpoint allowlist + lazy-import discipline.
F-CLASS-ROUTING-INDETERMINATE PRE-call enforcement at construction.

Coverage:
- Endpoint validation rejects out-of-allowlist hosts at construction.
- Provider library missing → graceful Python exception (no crash, no fall-through).
- Construction succeeds with valid endpoint + library; substrate Protocol
  conformance verified at runtime.
- Whisper hardware-tier whitelist (RT-16) rejects out-of-tier models.
"""

from __future__ import annotations

import pytest

from pipeline.orchestrator.seats.data_collector.email_channel import (
    EmailEndpointError,
    EmailProviderLibraryMissing,
    EmailTransportSubstrate,
    PERMITTED_EMAIL_PROVIDERS,
    PROVIDER_ENDPOINT_ALLOWLIST as EMAIL_ALLOWLIST,
    ProductionEmailTransport,
)
from pipeline.orchestrator.seats.data_collector.sms_channel import (
    PERMITTED_SMS_PROVIDERS,
    PROVIDER_ENDPOINT_ALLOWLIST as SMS_ALLOWLIST,
    ProductionSmsTransport,
    SmsEndpointError,
    SmsProviderLibraryMissing,
    SmsTransportSubstrate,
)
from pipeline.orchestrator.seats.data_collector.voice_channel import (
    LocalWhisperTranscriberSubstrate,
    PERMITTED_WHISPER_MODELS_DEV,
    PERMITTED_WHISPER_MODELS_PROD,
    ProductionLocalWhisperTranscriber,
    ProductionVoiceTransport,
    VOICE_OUTBOUND_ENDPOINT_ALLOWLIST,
    VoiceEndpointError,
    VoiceProviderLibraryMissing,
    VoiceTransportSubstrate,
    WHISPER_LOCAL_ENDPOINT_ALLOWLIST,
    WhisperHardwareTierError,
)
from pipeline.orchestrator.seats.data_collector.telegram_channel import (
    PERMITTED_TELEGRAM_LIBRARIES,
    ProductionTelegramBotSubstrate,
    TELEGRAM_ENDPOINT_ALLOWLIST,
    TelegramBotSubstrate,
    TelegramEndpointError,
    TelegramProviderLibraryMissing,
)
from pipeline.orchestrator.seats.data_collector.whatsapp_channel import (
    PERMITTED_WHATSAPP_LIBRARIES,
    ProductionWhatsAppTransport,
    WHATSAPP_ENDPOINT_ALLOWLIST,
    WhatsAppBusinessSubstrate,
    WhatsAppEndpointError,
    WhatsAppProviderLibraryMissing,
)


# ---------------------------------------------------------------------------
# Email — §13.8.1
# ---------------------------------------------------------------------------


def test_email_allowlist_includes_postmark_sendgrid_mailgun_smtp():
    assert "postmark" in PERMITTED_EMAIL_PROVIDERS
    assert "sendgrid" in PERMITTED_EMAIL_PROVIDERS
    assert "mailgun" in PERMITTED_EMAIL_PROVIDERS
    assert "smtp" in PERMITTED_EMAIL_PROVIDERS
    assert "api.postmarkapp.com" in EMAIL_ALLOWLIST["postmark"]
    assert "api.sendgrid.com" in EMAIL_ALLOWLIST["sendgrid"]
    assert "api.mailgun.net" in EMAIL_ALLOWLIST["mailgun"]


def test_email_endpoint_outside_allowlist_rejected():
    with pytest.raises(EmailEndpointError):
        ProductionEmailTransport(provider="postmark", endpoint="evil.example.com")


def test_email_unknown_provider_rejected():
    with pytest.raises(EmailEndpointError):
        ProductionEmailTransport(provider="hotmail", endpoint="api.postmarkapp.com")


def test_email_smtp_requires_host_allowlist():
    with pytest.raises(EmailEndpointError, match="smtp_host_allowlist"):
        ProductionEmailTransport(provider="smtp", endpoint="mail.example.com")


def test_email_smtp_endpoint_not_in_host_allowlist_rejected():
    with pytest.raises(EmailEndpointError, match="not in allowlist"):
        ProductionEmailTransport(
            provider="smtp",
            endpoint="mail.other.com",
            smtp_host_allowlist=frozenset({"mail.example.com"}),
        )


def test_email_postmark_construction_succeeds():
    t = ProductionEmailTransport(
        provider="postmark", endpoint="api.postmarkapp.com", api_key="dummy"
    )
    assert t.provider == "postmark"
    assert t.endpoint == "api.postmarkapp.com"


def test_email_substrate_protocol_conformance():
    t = ProductionEmailTransport(
        provider="postmark", endpoint="api.postmarkapp.com", api_key="dummy"
    )
    assert isinstance(t, EmailTransportSubstrate)


def test_email_lazy_import_missing_postmarker_raises():
    """``postmarker`` is not part of the dev environment; lazy-import should
    raise EmailProviderLibraryMissing on send_raw — not at construction."""
    t = ProductionEmailTransport(
        provider="postmark", endpoint="api.postmarkapp.com", api_key="dummy"
    )
    with pytest.raises(EmailProviderLibraryMissing, match="postmarker"):
        t.send_raw(
            rfc822_bytes=b"To: a@b\r\n\r\nhi",
            envelope_from="a@b",
            envelope_to="c@d",
        )


# ---------------------------------------------------------------------------
# SMS — §13.8.2
# ---------------------------------------------------------------------------


def test_sms_allowlist_includes_twilio_plivo():
    assert PERMITTED_SMS_PROVIDERS == frozenset({"twilio", "plivo"})
    assert "api.twilio.com" in SMS_ALLOWLIST["twilio"]
    assert "api.plivo.com" in SMS_ALLOWLIST["plivo"]


def test_sms_endpoint_outside_allowlist_rejected():
    with pytest.raises(SmsEndpointError):
        ProductionSmsTransport(provider="twilio", endpoint="api.attacker.com")


def test_sms_unknown_provider_rejected():
    with pytest.raises(SmsEndpointError):
        ProductionSmsTransport(provider="messagebird", endpoint="api.twilio.com")


def test_sms_twilio_construction_succeeds():
    t = ProductionSmsTransport(
        provider="twilio",
        endpoint="api.twilio.com",
        account_sid="dummy",
        auth_token="dummy",
    )
    assert t.provider == "twilio"


def test_sms_substrate_protocol_conformance():
    t = ProductionSmsTransport(provider="twilio", endpoint="api.twilio.com")
    assert isinstance(t, SmsTransportSubstrate)


def test_sms_lazy_import_missing_twilio_raises():
    t = ProductionSmsTransport(provider="twilio", endpoint="api.twilio.com")
    with pytest.raises(SmsProviderLibraryMissing, match="twilio"):
        t.send_raw(from_number="", to_number="", body_bytes=b"hi")


# ---------------------------------------------------------------------------
# Voice — §13.8.3
# ---------------------------------------------------------------------------


def test_voice_outbound_endpoint_allowlist_is_twilio_only():
    assert VOICE_OUTBOUND_ENDPOINT_ALLOWLIST == frozenset({"api.twilio.com"})


def test_voice_outbound_endpoint_outside_allowlist_rejected():
    with pytest.raises(VoiceEndpointError):
        ProductionVoiceTransport(endpoint="api.attacker.com")


def test_voice_outbound_construction_succeeds():
    t = ProductionVoiceTransport(endpoint="api.twilio.com")
    assert t.endpoint == "api.twilio.com"
    assert isinstance(t, VoiceTransportSubstrate)


def test_voice_outbound_lazy_import_missing_twilio_raises():
    t = ProductionVoiceTransport(endpoint="api.twilio.com")
    with pytest.raises(VoiceProviderLibraryMissing, match="twilio"):
        t.place_outbound_call(to_number="", from_number="", tts_script="")


def test_voice_recording_fetch_tls_pin_mismatch_raises():
    t = ProductionVoiceTransport(
        endpoint="api.twilio.com", tls_pin_fingerprint="sha256:expected"
    )
    with pytest.raises(VoiceEndpointError, match="TLS pin"):
        t.fetch_recording_bytes(
            recording_url="https://api.twilio.com/...",
            tls_pin_fingerprint="sha256:rogue",
        )


def test_whisper_local_endpoint_allowlist_localhost_unix_inprocess():
    assert "127.0.0.1" in WHISPER_LOCAL_ENDPOINT_ALLOWLIST
    assert "localhost" in WHISPER_LOCAL_ENDPOINT_ALLOWLIST
    assert "in-process" in WHISPER_LOCAL_ENDPOINT_ALLOWLIST


def test_whisper_remote_endpoint_rejected():
    with pytest.raises(VoiceEndpointError, match="always-local"):
        ProductionLocalWhisperTranscriber(endpoint="cloud.example.com")


def test_whisper_substrate_protocol_conformance():
    t = ProductionLocalWhisperTranscriber(endpoint="in-process")
    assert isinstance(t, LocalWhisperTranscriberSubstrate)


def test_whisper_hardware_tier_dev_rejects_medium_model():
    t = ProductionLocalWhisperTranscriber(
        endpoint="in-process",
        permitted_models=PERMITTED_WHISPER_MODELS_DEV,
    )
    with pytest.raises(WhisperHardwareTierError, match="medium.en"):
        t.transcribe(audio_bytes=b"", model_size="medium.en")


def test_whisper_hardware_tier_prod_accepts_large_model_but_lazy_import_missing():
    t = ProductionLocalWhisperTranscriber(
        endpoint="in-process",
        permitted_models=PERMITTED_WHISPER_MODELS_PROD,
    )
    with pytest.raises(VoiceProviderLibraryMissing, match="whisper"):
        t.transcribe(audio_bytes=b"", model_size="large-v3")


# ---------------------------------------------------------------------------
# Telegram — §13.8.4
# ---------------------------------------------------------------------------


def test_telegram_allowlist_is_api_telegram_only():
    assert TELEGRAM_ENDPOINT_ALLOWLIST == frozenset({"api.telegram.org"})


def test_telegram_endpoint_outside_allowlist_rejected():
    with pytest.raises(TelegramEndpointError):
        ProductionTelegramBotSubstrate(
            library="python-telegram-bot", endpoint="evil.example.com"
        )


def test_telegram_unknown_library_rejected():
    with pytest.raises(TelegramEndpointError):
        ProductionTelegramBotSubstrate(library="aiogram", endpoint="api.telegram.org")


def test_telegram_construction_succeeds():
    t = ProductionTelegramBotSubstrate(
        library="python-telegram-bot", endpoint="api.telegram.org", bot_token="dummy"
    )
    assert t.library == "python-telegram-bot"


def test_telegram_substrate_protocol_conformance():
    t = ProductionTelegramBotSubstrate(
        library="python-telegram-bot", endpoint="api.telegram.org"
    )
    assert isinstance(t, TelegramBotSubstrate)


def test_telegram_lazy_import_missing_raises():
    t = ProductionTelegramBotSubstrate(
        library="python-telegram-bot", endpoint="api.telegram.org"
    )
    with pytest.raises(TelegramProviderLibraryMissing, match="telegram"):
        t.send_message(chat_id=0, text="hi")


# ---------------------------------------------------------------------------
# WhatsApp — §13.8.5
# ---------------------------------------------------------------------------


def test_whatsapp_allowlist_is_graph_facebook_only():
    assert WHATSAPP_ENDPOINT_ALLOWLIST == frozenset({"graph.facebook.com"})


def test_whatsapp_endpoint_outside_allowlist_rejected():
    with pytest.raises(WhatsAppEndpointError):
        ProductionWhatsAppTransport(library="heyoo", endpoint="evil.example.com")


def test_whatsapp_unknown_library_rejected():
    with pytest.raises(WhatsAppEndpointError):
        ProductionWhatsAppTransport(library="unofficial", endpoint="graph.facebook.com")


def test_whatsapp_construction_succeeds():
    t = ProductionWhatsAppTransport(
        library="heyoo",
        endpoint="graph.facebook.com",
        access_token="dummy",
        phone_number_id="1234567890",
    )
    assert t.library == "heyoo"


def test_whatsapp_substrate_protocol_conformance():
    t = ProductionWhatsAppTransport(library="heyoo", endpoint="graph.facebook.com")
    assert isinstance(t, WhatsAppBusinessSubstrate)


def test_whatsapp_lazy_import_missing_heyoo_raises():
    t = ProductionWhatsAppTransport(library="heyoo", endpoint="graph.facebook.com")
    with pytest.raises(WhatsAppProviderLibraryMissing, match="heyoo"):
        t.send_message(to_phone="", body_text="")


# ---------------------------------------------------------------------------
# Cross-channel — F-CLASS-ROUTING-INDETERMINATE structural enforcement
# ---------------------------------------------------------------------------


def test_no_transport_adapter_accepts_arbitrary_endpoint():
    """Every production transport rejects out-of-allowlist endpoints at
    construction. F-CLASS-ROUTING-INDETERMINATE structural enforcement."""
    bad_endpoint = "169.254.169.254"  # AWS metadata service — should never resolve
    with pytest.raises(EmailEndpointError):
        ProductionEmailTransport(provider="postmark", endpoint=bad_endpoint)
    with pytest.raises(SmsEndpointError):
        ProductionSmsTransport(provider="twilio", endpoint=bad_endpoint)
    with pytest.raises(VoiceEndpointError):
        ProductionVoiceTransport(endpoint=bad_endpoint)
    with pytest.raises(VoiceEndpointError):
        ProductionLocalWhisperTranscriber(endpoint=bad_endpoint)
    with pytest.raises(TelegramEndpointError):
        ProductionTelegramBotSubstrate(library="python-telegram-bot", endpoint=bad_endpoint)
    with pytest.raises(WhatsAppEndpointError):
        ProductionWhatsAppTransport(library="heyoo", endpoint=bad_endpoint)
