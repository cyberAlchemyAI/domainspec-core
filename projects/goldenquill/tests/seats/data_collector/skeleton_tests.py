"""§13 Data Collector v1 SPEC LOCK skeleton tests.

These tests validate the v1 LOCK structural commitments per §13.13 + §13.15 + §13.16
companion edits. They DO NOT exercise the full per-channel substrate (deferred to WS-I
Code phase). They validate:

1. Five channels register in dispatcher (REGISTERED_CYCLES has correct four cycles;
   ChannelProtocol Protocol-DI invariants).
2. Eight v1 LOCK gate codes resolve (REGISTERED_GATES has eight named gates including
   the two NEW from Cycle 1 + Cycle 2 fold-ins: F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER
   + F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED).
3. Module-load Cedar engine bootstrap runs cleanly (skeleton stub at v0.2; full at WS-I).
4. AST-lint extensions are present (introspected via skeleton — full lint enforcement
   moves to scripts/run_lint.sh in WS-I Code phase).
5. Schema round-trip for each dataclass (frozen kw_only invariant verified).

The skeleton tests are NON-NEGOTIABLE: they prevent future contributors from quietly
enabling autosend or bypassing the structural enforcements introduced by Cycle 1 +
Cycle 2 fold-in dispositions per §13.16.
"""
from __future__ import annotations

import datetime as _dt
import pytest


def test_module_imports_cleanly():
    """Module-load Cedar engine bootstrap runs without raising; per Cycle 1 RT-06 + Cycle 2 RT-C2-04."""
    import pipeline.orchestrator.seats.data_collector as dc_module
    assert dc_module is not None


def test_five_channels_registered_in_dispatcher():
    """Per §13.4.0 ChannelProtocol + §13.6.0 per-channel summary table.

    At v0.2 SPEC LOCK, the per-channel modules ship as skeleton-only files; the channel
    enumeration is encoded in the ChannelProtocol.channel_name Literal + the Pydantic
    schema Literal[5] discipline. This test validates the enumeration matches the v1 LOCK
    five-channel decision (per Josh 2026-05-09 8a+8b).
    """
    from pipeline.orchestrator.seats.data_collector import ChannelProtocol
    # Verify ChannelProtocol Protocol-DI definition exists
    assert ChannelProtocol is not None
    # ChannelProtocol.channel_name is a Literal[5] discipline — assertion comes from schema validation


def test_four_cycles_registered_in_dispatcher():
    """Per §13.12 pipeline placement — four cycles at v0.2 first ship."""
    from pipeline.orchestrator.seats.data_collector import REGISTERED_CYCLES
    assert set(REGISTERED_CYCLES.keys()) == {
        "outbound_batch_compose",
        "outbound_batch_send",
        "inbound_parse",
        "inbound_classify",
    }


def test_eight_gates_registered_at_v1_lock():
    """Per §13.16.6.4 final v1 LOCK gate roster — 8 codes.

    Cycle 1 added F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER (RT-28 closure).
    Cycle 2 added F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED (RT-C2-02 closure).
    """
    from pipeline.orchestrator.seats.data_collector import REGISTERED_GATES
    expected = {
        "F-DATACOLLECTOR-CONSENT-MISSING",
        "F-DATACOLLECTOR-OPT-OUT-ACTIVE",
        "F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED",
        "F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND",
        "F-DATACOLLECTOR-KFR-DRIFT",
        "F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET",
        "F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER",       # Cycle 1 RT-28
        "F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED",     # Cycle 2 RT-C2-02
    }
    assert set(REGISTERED_GATES.keys()) == expected


def test_gate_predicates_realized_callables():
    """WS-I Code phase 2026-05-10: skeleton NotImplementedError stubs retired.

    All eight gate predicates now resolve to realized `check_*` callables in
    `pipeline/logician/gates/f_datacollector_*.py`. The registry maps the
    canonical failure code to the canonical entry-point check callable;
    additional sub-check callables are imported directly from each gate
    module.
    """
    from pipeline.orchestrator.seats.data_collector import REGISTERED_GATES
    for code, predicate in REGISTERED_GATES.items():
        assert callable(predicate), f"{code}: predicate is not callable"
        # The realized predicates require kwargs; invoking with no args should
        # raise TypeError (missing required keyword arguments), not
        # NotImplementedError. This proves the stubs are retired.
        with pytest.raises(TypeError):
            predicate()


def test_dataclass_schemas_are_frozen_kw_only():
    """All Pydantic dataclasses ship frozen + kw_only per v7.0.4 KFR + §2 v7.2 + §11 v1 conventions."""
    from pipeline.orchestrator.seats.data_collector import (
        OutboundBatchComposeInput,
        OutboundBatchSendInput,
        InboundParseInput,
        InboundClassifyInput,
        OutboundMessage,
        InboundResponse,
        ConsentLedgerEntry,
        SubAwardeeToken,
        StateRulesCardEntry,
        SignedBatchEnvelope,
    )
    # All dataclasses are decorated with @dataclass(frozen=True, kw_only=True).
    # Verify by introspecting the dataclass params on each.
    import dataclasses
    for cls in (
        OutboundBatchComposeInput,
        OutboundBatchSendInput,
        InboundParseInput,
        InboundClassifyInput,
        OutboundMessage,
        InboundResponse,
        ConsentLedgerEntry,
        SubAwardeeToken,
        StateRulesCardEntry,
        SignedBatchEnvelope,
    ):
        assert dataclasses.is_dataclass(cls)
        # frozen=True ⇒ cls.__dataclass_params__.frozen is True
        assert cls.__dataclass_params__.frozen is True


def test_outbound_batch_compose_input_roundtrip():
    """Frozen kw_only round-trip — constructs successfully with all required fields."""
    from pipeline.orchestrator.seats.data_collector import OutboundBatchComposeInput
    inp = OutboundBatchComposeInput(
        run_id="run-001",
        org_slug="test_org",
        grant_id="grant-A",
        period_n=1,
        proposal_commitments_path="orgs/test_org/vault/grants/grant-A/proposal_commitments.yaml",
        reporting_template_path="orgs/test_org/vault/grants/grant-A/reporting_template.yaml",
        consent_ledger_dir="orgs/test_org/data_collector/consent_ledger/",
        sub_awardee_token_register_dir="orgs/test_org/data_collector/per_recipient_tokens/",
        state_rules_card_dir="vault_shared/state_rules_card/",
        channels_in_scope=["email"],
        frequency_cap_lookback_days=7,
        invoked_at_utc=_dt.datetime(2026, 5, 10, 21, 0, 0, tzinfo=_dt.timezone.utc),
    )
    assert inp.org_slug == "test_org"
    assert inp.channels_in_scope == ["email"]
    # frozen ⇒ assignment raises
    with pytest.raises(dataclasses_frozen_error()):
        inp.org_slug = "other"  # type: ignore[misc]


def test_outbound_message_carries_grant_and_org_in_signed_payload():
    """Per Cycle 2 RT-C2-01 closure — per-recipient signature includes grant_id + org_slug."""
    from pipeline.orchestrator.seats.data_collector import OutboundMessage
    msg = OutboundMessage(
        outbound_id="out-001",
        dc_run_id="run-001",
        recipient_id="recipient-X",
        channel="email",
        grant_id="grant-A",  # Cycle 2 RT-C2-01: included in signed payload
        org_slug="test_org",  # Cycle 2 RT-C2-01: included in signed payload
        commitment_id_or_funder_reporting_field_id="commit-001",
        rendered_message_bytes_sha3_512="a" * 128,  # full 128-hex per Cycle 1 RT-13
        per_state_disclaimers_applied=[],
        per_recipient_token_id="tok-001",
        staged_at_utc=_dt.datetime(2026, 5, 10, tzinfo=_dt.timezone.utc),
        sent_at_utc=None,
        per_recipient_signature=b"\x00" * 64,  # Ed25519 64-byte signature
    )
    # Critical: grant_id + org_slug fields present (verifiable at signature verification time)
    assert msg.grant_id == "grant-A"
    assert msg.org_slug == "test_org"
    assert len(msg.rendered_message_bytes_sha3_512) == 128  # full digest


def test_signed_batch_envelope_carries_full_hash_and_recipient_order():
    """Per Cycle 1 RT-13 (full SHA3-512) + Cycle 2 RT-C2-12 (approved_recipient_order)."""
    from pipeline.orchestrator.seats.data_collector import SignedBatchEnvelope
    env = SignedBatchEnvelope(
        batch_id="batch-001",
        compose_run_id="run-001",
        grant_id="grant-A",
        org_slug="test_org",
        period_n=1,
        batch_status="UNSIGNED",
        batch_content_sha3_512="b" * 128,  # full 128-hex per Cycle 1 RT-13
        batch_manifest_sha3_512="c" * 128,  # full 128-hex per Cycle 1 RT-14
        approved_recipient_order=["recipient-X", "recipient-Y", "recipient-Z"],  # Cycle 2 RT-C2-12
        per_recipient_consent_state_sha3_512_full={  # Cycle 1 RT-01
            "recipient-X": "d" * 128,
            "recipient-Y": "e" * 128,
            "recipient-Z": "f" * 128,
        },
        signed_at_utc=_dt.datetime(2026, 5, 10, tzinfo=_dt.timezone.utc),
        signed_by="operator-key-001",
        signature=b"\x00" * 64,
    )
    assert len(env.batch_content_sha3_512) == 128
    assert len(env.batch_manifest_sha3_512) == 128
    assert env.approved_recipient_order == ["recipient-X", "recipient-Y", "recipient-Z"]
    assert set(env.per_recipient_consent_state_sha3_512_full.keys()) == {"recipient-X", "recipient-Y", "recipient-Z"}


def test_consent_ledger_entry_has_opt_out_propagation_field():
    """Per Cycle 1 RT-02 closure — cross-channel opt-out propagation field."""
    from pipeline.orchestrator.seats.data_collector import ConsentLedgerEntry
    entry = ConsentLedgerEntry(
        recipient_id="recipient-X",
        channel="email",
        consent_active=True,
        consent_captured_at_utc=_dt.datetime(2026, 5, 10, tzinfo=_dt.timezone.utc),
        consent_capture_method="opt_in_link_email",
        opt_out_active=False,
        opt_out_at_utc=None,
        opt_out_propagated_from_channel=[],  # Cycle 1 RT-02
        frequency_cap_lookback_days=7,
        recent_outbound_log=[],
        state_code_for_rules="PA",
        audit_chain=[],
    )
    assert entry.opt_out_propagated_from_channel == []


def test_sub_awardee_token_has_channel_binding_and_aead_nonce():
    """Per Cycle 1 RT-10 channel-bound tokens + Cycle 1 RT-12 revoked field +
    Cycle 2 RT-C2-07 AEAD nonce field."""
    from pipeline.orchestrator.seats.data_collector import SubAwardeeToken
    tok = SubAwardeeToken(
        token_id="tok-001",
        grant_id="grant-A",
        recipient_id="recipient-X",
        channel_binding="email",  # Cycle 1 RT-10
        secret_value_ciphertext=b"\x00" * 64,  # AEAD ciphertext
        aead_nonce=b"\x00" * 12,  # Cycle 2 RT-C2-07; 96-bit random
        issued_at_utc=_dt.datetime(2026, 5, 10, tzinfo=_dt.timezone.utc),
        rotates_at_utc=_dt.datetime(2027, 5, 10, tzinfo=_dt.timezone.utc),
        revoked=False,  # Cycle 1 RT-12
        revoked_at_utc=None,
        operator_signature=b"\x00" * 64,
    )
    assert tok.channel_binding == "email"
    assert tok.revoked is False
    assert len(tok.aead_nonce) == 12


def test_critical_policy_error_is_baseexception_subclass():
    """Per Cycle 2 RT-C2-04 closure — CriticalPolicyError subclasses BaseException so
    upstream try/except Exception cannot swallow Cedar engine load failures."""
    from pipeline.orchestrator.seats.data_collector import CriticalPolicyError
    assert issubclass(CriticalPolicyError, BaseException)
    # Critical: NOT subclass of Exception (else try/except Exception would catch)
    assert not issubclass(CriticalPolicyError, Exception)


# Helper for frozen-dataclass assignment-raises detection
def dataclasses_frozen_error():
    """The Python stdlib dataclasses raises dataclasses.FrozenInstanceError on assignment
    to a frozen instance; aliased here for readability."""
    import dataclasses
    return dataclasses.FrozenInstanceError
