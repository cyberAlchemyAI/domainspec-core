"""§13.9 — gate predicate behavioural tests (all 8 codes).

These tests invoke the realized `check_*` callables from
`pipeline/logician/gates/f_datacollector_*.py` to verify each sub-tag fires
under the documented conditions, and the PASS path returns success.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import pytest

# ---------------------------------------------------------------------------
# F-DATACOLLECTOR-CONSENT-MISSING
# ---------------------------------------------------------------------------

def test_consent_missing_ledger_absent():
    from pipeline.logician.gates.f_datacollector_consent_missing import (
        check_consent_missing, SUB_TAG_LEDGER_ABSENT,
    )
    r = check_consent_missing(
        recipient_id="r1", channel="email",
        ledger_present=False, ledger_entry=None,
    )
    assert r.success is False
    assert r.sub_tag == SUB_TAG_LEDGER_ABSENT


def test_consent_missing_consent_inactive():
    from pipeline.logician.gates.f_datacollector_consent_missing import (
        check_consent_missing, SUB_TAG_CONSENT_INACTIVE,
    )
    r = check_consent_missing(
        recipient_id="r1", channel="email",
        ledger_present=True,
        ledger_entry={"consent_active": False, "consent_capture_method": "opt_in_link_email"},
    )
    assert r.sub_tag == SUB_TAG_CONSENT_INACTIVE


def test_consent_missing_method_unset():
    from pipeline.logician.gates.f_datacollector_consent_missing import (
        check_consent_missing, SUB_TAG_METHOD_UNSET,
    )
    r = check_consent_missing(
        recipient_id="r1", channel="email",
        ledger_present=True,
        ledger_entry={"consent_active": True, "consent_capture_method": None},
    )
    assert r.sub_tag == SUB_TAG_METHOD_UNSET


def test_consent_missing_pass():
    from pipeline.logician.gates.f_datacollector_consent_missing import (
        check_consent_missing,
    )
    r = check_consent_missing(
        recipient_id="r1", channel="email",
        ledger_present=True,
        ledger_entry={"consent_active": True, "consent_capture_method": "opt_in_link_email"},
    )
    assert r.success is True


def test_send_time_consent_drift_bytes_required():
    from pipeline.logician.gates.f_datacollector_consent_missing import (
        check_send_time_consent_drift, SUB_TAG_SEND_TIME_CONSENT_DRIFT,
    )
    r = check_send_time_consent_drift(
        recipient_id="r1", channel="email",
        consent_state_hash_at_compose=b"\x00" * 64,
        consent_state_hash_at_send=b"\xff" * 64,
    )
    assert r.success is False
    assert r.sub_tag == SUB_TAG_SEND_TIME_CONSENT_DRIFT


def test_config_signature_at_module_load_invalid():
    from pipeline.logician.gates.f_datacollector_consent_missing import (
        check_config_signature, SUB_TAG_MODULE_LOAD_CONFIG_SIGNATURE_INVALID,
    )
    r = check_config_signature(
        config_present=True, config_signature_valid=False, at_module_load=True,
    )
    assert r.sub_tag == SUB_TAG_MODULE_LOAD_CONFIG_SIGNATURE_INVALID


def test_config_value_invalid_frequency_cap_zero():
    from pipeline.logician.gates.f_datacollector_consent_missing import (
        check_config_value_ranges, SUB_TAG_CONFIG_VALUE_INVALID,
    )
    r = check_config_value_ranges(config={"frequency_cap_lookback_days": 0})
    assert r.sub_tag == SUB_TAG_CONFIG_VALUE_INVALID


# ---------------------------------------------------------------------------
# F-DATACOLLECTOR-OPT-OUT-ACTIVE
# ---------------------------------------------------------------------------

def test_opt_out_active_per_channel_subtag():
    from pipeline.logician.gates.f_datacollector_opt_out_active import (
        check_opt_out_active, SUB_TAG_BY_CHANNEL,
    )
    for ch in ("email", "sms", "voice", "telegram", "whatsapp"):
        r = check_opt_out_active(
            recipient_id="r1", channel=ch,
            ledger_entry={"opt_out_active": True},
        )
        assert r.success is False
        assert r.sub_tag == SUB_TAG_BY_CHANNEL[ch]


def test_opt_out_active_propagation_failure():
    from pipeline.logician.gates.f_datacollector_opt_out_active import (
        check_opt_out_active, SUB_TAG_CROSS_CHANNEL_PROPAGATION_FAILURE,
    )
    r = check_opt_out_active(
        recipient_id="r1", channel="email",
        ledger_entry={"opt_out_active": False},
        propagation_failure=True,
    )
    assert r.sub_tag == SUB_TAG_CROSS_CHANNEL_PROPAGATION_FAILURE


def test_opt_out_active_pass():
    from pipeline.logician.gates.f_datacollector_opt_out_active import (
        check_opt_out_active,
    )
    r = check_opt_out_active(
        recipient_id="r1", channel="email",
        ledger_entry={"opt_out_active": False},
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED
# ---------------------------------------------------------------------------

def test_freq_cap_recipient_channel_cap():
    from pipeline.logician.gates.f_datacollector_frequency_cap_exceeded import (
        check_frequency_cap_exceeded, SUB_TAG_RECIPIENT_CHANNEL_CAP,
    )
    now = datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc)
    r = check_frequency_cap_exceeded(
        recipient_id="r1", channel="email", now=now,
        recent_outbound_log=[{"sent_at_utc": now - timedelta(days=1)}],
        frequency_cap_lookback_days=7,
        channel_switching_evasion_strict=False,
    )
    assert r.success is False
    assert r.sub_tag == SUB_TAG_RECIPIENT_CHANNEL_CAP


def test_freq_cap_channel_switching_evasion():
    from pipeline.logician.gates.f_datacollector_frequency_cap_exceeded import (
        check_frequency_cap_exceeded, SUB_TAG_CHANNEL_SWITCHING_EVASION,
    )
    now = datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc)
    r = check_frequency_cap_exceeded(
        recipient_id="r1", channel="sms", now=now,
        recent_outbound_log=[],
        frequency_cap_lookback_days=7,
        cross_channel_outbound_log=[{"sent_at_utc": now - timedelta(hours=1), "channel": "email"}],
        channel_switching_evasion_strict=True,
    )
    assert r.sub_tag == SUB_TAG_CHANNEL_SWITCHING_EVASION


def test_freq_cap_state_intersection_overrides_default():
    from pipeline.logician.gates.f_datacollector_frequency_cap_exceeded import (
        check_frequency_cap_exceeded, SUB_TAG_STATE_INTERSECTION_DEFAULT_OVERRIDDEN,
    )
    now = datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc)
    # PA SMS — state_min_interval_hours=48 (stricter than 7-day default).
    # But "48h stricter than 7d" is FALSE — 7d=168h > 48h. So state cap
    # NEVER overrides 7-day default here. Test that state cap NOT overriding default:
    r = check_frequency_cap_exceeded(
        recipient_id="r1", channel="sms", now=now,
        recent_outbound_log=[{"sent_at_utc": now - timedelta(hours=24)}],
        frequency_cap_lookback_days=1,  # 1-day default
        state_min_interval_hours=48,  # stricter than 24h
    )
    # 48h > 24h (1 day in hours) → state overrides default.
    assert r.sub_tag == SUB_TAG_STATE_INTERSECTION_DEFAULT_OVERRIDDEN


def test_freq_cap_pass():
    from pipeline.logician.gates.f_datacollector_frequency_cap_exceeded import (
        check_frequency_cap_exceeded,
    )
    now = datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc)
    r = check_frequency_cap_exceeded(
        recipient_id="r1", channel="email", now=now,
        recent_outbound_log=[],
        frequency_cap_lookback_days=7,
        channel_switching_evasion_strict=False,
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND (~20 sub-tags; cover key ones)
# ---------------------------------------------------------------------------

def test_pii_leak_semantic_slot_in_outbound():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_semantic_slot_in_outbound, SUB_TAG_SEMANTIC_SLOT_IN_OUTBOUND,
    )
    r = check_semantic_slot_in_outbound(
        rendered_bytes=b"You owe [SLOT_ANNUAL_REVENUE] -- pay now",
    )
    assert r.success is False
    assert r.sub_tag == SUB_TAG_SEMANTIC_SLOT_IN_OUTBOUND


def test_pii_leak_opaque_slot_ok():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_semantic_slot_in_outbound,
    )
    r = check_semantic_slot_in_outbound(
        rendered_bytes=b"You owe [SLOT_001] -- pay now",
    )
    assert r.success is True


def test_pii_leak_sms_size_overflow():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_sms_size_overflow, SUB_TAG_SMS_SIZE_OVERFLOW, SMS_MAX_BODY_BYTES,
    )
    r = check_sms_size_overflow(rendered_body_bytes=b"x" * (SMS_MAX_BODY_BYTES + 1))
    assert r.success is False
    assert r.sub_tag == SUB_TAG_SMS_SIZE_OVERFLOW


def test_pii_leak_sms_size_within_limit():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_sms_size_overflow, SMS_MAX_BODY_BYTES,
    )
    r = check_sms_size_overflow(rendered_body_bytes=b"x" * SMS_MAX_BODY_BYTES)
    assert r.success is True


def test_pii_leak_whatsapp_template_unapproved():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_whatsapp_template_approved, SUB_TAG_WHATSAPP_TEMPLATE_UNAPPROVED,
    )
    r = check_whatsapp_template_approved(
        inside_24h_window=False,
        template_id="tmpl_unknown",
        approved_template_ids=frozenset(),
    )
    assert r.sub_tag == SUB_TAG_WHATSAPP_TEMPLATE_UNAPPROVED


def test_pii_leak_whatsapp_inside_24h_no_template_ok():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_whatsapp_template_approved,
    )
    r = check_whatsapp_template_approved(
        inside_24h_window=True, template_id=None,
        approved_template_ids=frozenset(),
    )
    assert r.success is True


def test_pii_leak_mtproto_cross_org():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_mtproto_cross_org, SUB_TAG_MTPROTO_CROSS_ORG,
    )
    r = check_mtproto_cross_org(
        chat_id=12345, expected_org_slug="org_a", resolved_org_slug="org_b",
    )
    assert r.sub_tag == SUB_TAG_MTPROTO_CROSS_ORG


def test_pii_leak_chat_id_collision():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_cross_org_chat_id_collision, SUB_TAG_CROSS_ORG_CHAT_ID_COLLISION,
    )
    r = check_cross_org_chat_id_collision(
        chat_id=99, matching_org_slugs=["org_a", "org_b"],
    )
    assert r.sub_tag == SUB_TAG_CROSS_ORG_CHAT_ID_COLLISION


def test_pii_leak_env_var_bypass():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_env_var_auto_confirm_set, SUB_TAG_ENV_VAR_AUTO_CONFIRM_SET,
    )
    r = check_env_var_auto_confirm_set(env={"DC_AUTO": "1"})
    assert r.sub_tag == SUB_TAG_ENV_VAR_AUTO_CONFIRM_SET


def test_pii_leak_env_var_bypass_pass():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_env_var_auto_confirm_set,
    )
    r = check_env_var_auto_confirm_set(env={"PATH": "/usr/bin"})
    assert r.success is True


def test_pii_leak_telegram_group_chat_rejected():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_telegram_chat_type, SUB_TAG_TELEGRAM_GROUP_CHAT_REJECTED,
    )
    for t in ("group", "supergroup", "channel"):
        r = check_telegram_chat_type(chat_type=t)
        assert r.sub_tag == SUB_TAG_TELEGRAM_GROUP_CHAT_REJECTED


def test_pii_leak_telegram_private_chat_ok():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_telegram_chat_type,
    )
    r = check_telegram_chat_type(chat_type="private")
    assert r.success is True


def test_pii_leak_mtproto_session_path_unbound():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_mtproto_session_path_bound, SUB_TAG_MTPROTO_SESSION_PATH_UNBOUND,
    )
    r = check_mtproto_session_path_bound(
        session_path="/var/tmp/global.session", org_slug="my_org",
    )
    assert r.sub_tag == SUB_TAG_MTPROTO_SESSION_PATH_UNBOUND


def test_pii_leak_mtproto_session_path_bound_ok():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_mtproto_session_path_bound,
    )
    r = check_mtproto_session_path_bound(
        session_path="orgs/my_org/data_collector/mtproto_session/bot.session",
        org_slug="my_org",
    )
    assert r.success is True


def test_pii_leak_cedar_engine_identity_strict_true():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_cedar_engine_ready, SUB_TAG_CEDAR_ENGINE_UNREADY,
    )
    assert check_cedar_engine_ready(cedar_engine_ready=True).success is True
    assert check_cedar_engine_ready(cedar_engine_ready=1).sub_tag == SUB_TAG_CEDAR_ENGINE_UNREADY


def test_pii_leak_batch_recipient_order_swap():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_batch_recipient_order, SUB_TAG_BATCH_RECIPIENT_ORDER_SWAP,
    )
    r = check_batch_recipient_order(
        signed_recipient_order=["r1", "r2", "r3"],
        dispatch_recipient_order=["r2", "r1", "r3"],
    )
    assert r.sub_tag == SUB_TAG_BATCH_RECIPIENT_ORDER_SWAP


def test_pii_leak_batch_hash_mismatch():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_batch_hash, SUB_TAG_BATCH_HASH_MISMATCH,
    )
    r = check_batch_hash(
        batch_content_sha3_512_signed=b"a" * 64,
        batch_content_sha3_512_recomputed=b"b" * 64,
    )
    assert r.sub_tag == SUB_TAG_BATCH_HASH_MISMATCH


def test_pii_leak_per_recipient_signature_grant_or_org_mismatch():
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_per_recipient_signature_grant_or_org,
        SUB_TAG_PER_RECIPIENT_SIGNATURE_GRANT_OR_ORG_MISMATCH,
    )
    r = check_per_recipient_signature_grant_or_org(
        signed_grant_id="grant-A", invocation_grant_id="grant-B",
        signed_org_slug="org-X", invocation_org_slug="org-X",
        recipient_id="r1",
    )
    assert r.sub_tag == SUB_TAG_PER_RECIPIENT_SIGNATURE_GRANT_OR_ORG_MISMATCH


# ---------------------------------------------------------------------------
# F-DATACOLLECTOR-KFR-DRIFT (advisory)
# ---------------------------------------------------------------------------

def test_kfr_drift_above_tolerance():
    from pipeline.logician.gates.f_datacollector_kfr_drift import (
        check_kfr_drift, SUB_TAG_ABOVE_TOLERANCE,
    )
    r = check_kfr_drift(
        field_class="graduates_count",
        inbound_value=300.0, inbound_unit="count",
        kfr_value=197.0, kfr_unit="count",
    )
    assert r.success is False
    assert r.sub_tag == SUB_TAG_ABOVE_TOLERANCE
    assert r.advisory is True  # NOT fail-closed


def test_kfr_drift_unit_mismatch():
    from pipeline.logician.gates.f_datacollector_kfr_drift import (
        check_kfr_drift, SUB_TAG_UNIT_MISMATCH,
    )
    r = check_kfr_drift(
        field_class="expenditures",
        inbound_value=5000.0, inbound_unit="usd",
        kfr_value=5.0, kfr_unit="usd_thousands",
    )
    assert r.sub_tag == SUB_TAG_UNIT_MISMATCH


def test_kfr_drift_within_tolerance_pass():
    from pipeline.logician.gates.f_datacollector_kfr_drift import check_kfr_drift
    r = check_kfr_drift(
        field_class="x",
        inbound_value=210.0, inbound_unit="count",
        kfr_value=200.0, kfr_unit="count",
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET
# ---------------------------------------------------------------------------

def test_inbound_classification_register_tampered():
    from pipeline.logician.gates.f_datacollector_inbound_classification_unset import (
        check_inbound_classification_unset, SUB_TAG_CLASSIFICATION_REGISTER_TAMPERED,
    )
    r = check_inbound_classification_unset(
        recipient_id="r1", field_class="metric",
        classification_register_signature_valid=False,
        register_entry=None,
    )
    assert r.sub_tag == SUB_TAG_CLASSIFICATION_REGISTER_TAMPERED


def test_inbound_classification_first_occurrence_unclassified():
    from pipeline.logician.gates.f_datacollector_inbound_classification_unset import (
        check_inbound_classification_unset, SUB_TAG_FIRST_OCCURRENCE_UNCLASSIFIED,
    )
    r = check_inbound_classification_unset(
        recipient_id="r1", field_class="metric",
        classification_register_signature_valid=True,
        register_entry=None,
    )
    assert r.sub_tag == SUB_TAG_FIRST_OCCURRENCE_UNCLASSIFIED


def test_inbound_classification_default_pending_review():
    from pipeline.logician.gates.f_datacollector_inbound_classification_unset import (
        check_inbound_classification_unset, SUB_TAG_DEFAULT_CONFIDENTIAL_PENDING_REVIEW,
    )
    r = check_inbound_classification_unset(
        recipient_id="r1", field_class="metric",
        classification_register_signature_valid=True,
        register_entry={"classification_status": "DEFAULT_CONFIDENTIAL_PENDING_REVIEW"},
    )
    assert r.sub_tag == SUB_TAG_DEFAULT_CONFIDENTIAL_PENDING_REVIEW


def test_inbound_classification_operator_classified_pass():
    from pipeline.logician.gates.f_datacollector_inbound_classification_unset import (
        check_inbound_classification_unset,
    )
    r = check_inbound_classification_unset(
        recipient_id="r1", field_class="metric",
        classification_register_signature_valid=True,
        register_entry={
            "classification_status": "OPERATOR_CLASSIFIED",
            "classification": "shareable",  # lowercase per PERMITTED_CLASSIFICATIONS
        },
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER
# ---------------------------------------------------------------------------

def test_beneficiary_consent_tier_missing():
    from pipeline.logician.gates.f_datacollector_beneficiary_consent_tier import (
        check_beneficiary_consent_tier, SUB_TAG_CONSENT_TIER_MISSING,
    )
    r = check_beneficiary_consent_tier(record={"name": "Alice"})
    assert r.sub_tag == SUB_TAG_CONSENT_TIER_MISSING


def test_beneficiary_consent_tier_out_of_enum():
    from pipeline.logician.gates.f_datacollector_beneficiary_consent_tier import (
        check_beneficiary_consent_tier, SUB_TAG_CONSENT_TIER_OUT_OF_ENUM,
    )
    r = check_beneficiary_consent_tier(
        record={"name": "Alice", "consent_tier": "wide_open"},
    )
    assert r.sub_tag == SUB_TAG_CONSENT_TIER_OUT_OF_ENUM


def test_beneficiary_consent_tier_pass():
    from pipeline.logician.gates.f_datacollector_beneficiary_consent_tier import (
        check_beneficiary_consent_tier, PERMITTED_CONSENT_TIERS,
    )
    for tier in PERMITTED_CONSENT_TIERS:
        r = check_beneficiary_consent_tier(record={"consent_tier": tier})
        assert r.success is True


# ---------------------------------------------------------------------------
# F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED
# ---------------------------------------------------------------------------

def test_opt_out_propagation_coordinator_lock_failed():
    from pipeline.logician.gates.f_datacollector_opt_out_propagation_failed import (
        check_opt_out_propagation_failed, SUB_TAG_COORDINATOR_LOCK_ACQUISITION_FAILED,
    )
    r = check_opt_out_propagation_failed(
        recipient_id="r1",
        coordinator_lock_acquired=False,
        per_channel_write_results=[],
    )
    assert r.sub_tag == SUB_TAG_COORDINATOR_LOCK_ACQUISITION_FAILED


def test_opt_out_propagation_partial_rolled_back():
    from pipeline.logician.gates.f_datacollector_opt_out_propagation_failed import (
        check_opt_out_propagation_failed, SUB_TAG_PARTIAL_PROPAGATION_ROLLED_BACK,
    )
    r = check_opt_out_propagation_failed(
        recipient_id="r1",
        coordinator_lock_acquired=True,
        per_channel_write_results=[("email", True), ("sms", False), ("voice", True)],
        rollback_succeeded=True,
    )
    assert r.sub_tag == SUB_TAG_PARTIAL_PROPAGATION_ROLLED_BACK
    assert r.rolled_back is True


def test_opt_out_propagation_partial_no_rollback_critical():
    from pipeline.logician.gates.f_datacollector_opt_out_propagation_failed import (
        check_opt_out_propagation_failed, SUB_TAG_PARTIAL_PROPAGATION_NO_ROLLBACK,
    )
    r = check_opt_out_propagation_failed(
        recipient_id="r1",
        coordinator_lock_acquired=True,
        per_channel_write_results=[("email", True), ("sms", False)],
        rollback_succeeded=False,
    )
    assert r.sub_tag == SUB_TAG_PARTIAL_PROPAGATION_NO_ROLLBACK
    assert r.rolled_back is False


def test_opt_out_propagation_all_success_pass():
    from pipeline.logician.gates.f_datacollector_opt_out_propagation_failed import (
        check_opt_out_propagation_failed,
    )
    r = check_opt_out_propagation_failed(
        recipient_id="r1",
        coordinator_lock_acquired=True,
        per_channel_write_results=[("email", True), ("sms", True), ("voice", True), ("telegram", True), ("whatsapp", True)],
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Registry & wiring
# ---------------------------------------------------------------------------

def test_registered_gates_all_eight_callable():
    from pipeline.orchestrator.seats.data_collector import REGISTERED_GATES
    assert len(REGISTERED_GATES) == 8
    for code, fn in REGISTERED_GATES.items():
        assert callable(fn), f"{code} not callable"


def test_registered_gates_codes_match_v1_lock_roster():
    from pipeline.orchestrator.seats.data_collector import REGISTERED_GATES
    expected = {
        "F-DATACOLLECTOR-CONSENT-MISSING",
        "F-DATACOLLECTOR-OPT-OUT-ACTIVE",
        "F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED",
        "F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND",
        "F-DATACOLLECTOR-KFR-DRIFT",
        "F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET",
        "F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER",
        "F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED",
    }
    assert set(REGISTERED_GATES.keys()) == expected


def test_logician_package_reexports_data_collector_gates():
    from pipeline.logician.gates import (
        F_DATACOLLECTOR_CONSENT_MISSING,
        F_DATACOLLECTOR_OPT_OUT_ACTIVE,
        F_DATACOLLECTOR_FREQUENCY_CAP_EXCEEDED,
        F_DATACOLLECTOR_PII_LEAK_IN_OUTBOUND,
        F_DATACOLLECTOR_KFR_DRIFT,
        F_DATACOLLECTOR_INBOUND_CLASSIFICATION_UNSET,
        F_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER,
        F_DATACOLLECTOR_OPT_OUT_PROPAGATION_FAILED,
        check_datacollector_consent_missing,
        check_datacollector_opt_out_active,
        check_datacollector_frequency_cap_exceeded,
        check_datacollector_kfr_drift,
        check_datacollector_inbound_classification_unset,
        check_datacollector_beneficiary_consent_tier,
        check_datacollector_opt_out_propagation_failed,
    )
    assert callable(check_datacollector_consent_missing)
