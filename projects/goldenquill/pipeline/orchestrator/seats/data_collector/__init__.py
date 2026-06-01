"""§13 Data Collector seat — v1 SPEC LOCKED 2026-05-10.

This module is the seat-lifecycle wrapper around the five-channel outbound + inbound
data-gathering substrate spec'd at `pipeline/blueprint/v0.1/section_13_data_collector.md`
(LOCKED 2026-05-10 — L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor).

v0.2 first ship disposition:
- Pydantic dataclass schemas LANDED (frozen kw_only; matches §13.5.0 schema delta).
- ChannelProtocol Protocol-DI definition LANDED.
- Mode dispatcher with four cycles registered (compose-batch, send-batch, parse-inbound, classify-inbound).
- AST-lint extensions LANDED via skeleton tests assertion.
- Per-channel substrate (SMTP / Twilio / MTProto / WhatsApp Business API) skeleton stubs raise
  NotImplementedError; full implementation in WS-I Code phase follow-on dispatch after this LOCK.
- Eight F-DATACOLLECTOR-* gate predicates skeleton stubs raise NotImplementedError; activated
  from §4 v2.x §5.1 HORIZON to live PRE/POST positions at this LOCK; predicate bodies realized
  in WS-I Code phase + §4 v2.x.1 follow-on minor amendment.
- Cedar engine mandatory instantiation at module load (per Cycle 1 RT-06 + Cycle 2 RT-C2-04
  closures) — wired here at module import; raises CriticalPolicyError(BaseException) on
  failure.

Non-negotiable structural enforcement (verified by skeleton tests at LOCK):
- R-DATACOLLECTOR-NO-AUTOSEND: no per-channel send() invocation outside
  outbound_batch.dispatch_after_operator_approval.
- R-DATACOLLECTOR-VAULT-INTENT-REQUIRED: no raw open() against vault paths; all reads/writes
  through vault read/write intents.
- R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT: no import of cultivator.consent_ledger.*
  from any Data Collector module.
- R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED + R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-ENUM:
  every write to beneficiary_records sub-kind MUST set consent_tier from the enumerated literal set.
- R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY: no CIC token in templates or schemas (four-layer audit
  at LOCK + CI re-run per Cycle 2 RT-C2-08).
- R-DATACOLLECTOR-NO-RAW-TELEGRAM-BOT-IMPORT: only OrgScopedBot import permitted.
- R-DATACOLLECTOR-CARD-MANDATORY-SIG-VERIFY: every card load through signature-verifying wrapper.
- R-DATACOLLECTOR-CARD-SAFE-LOAD: no yaml.load(); only yaml.safe_load() permitted.
- R-DATACOLLECTOR-ORGSCOPEDBOT-FINAL: no subclassing of OrgScopedBot.
- R-DATACOLLECTOR-CEDAR-NO-CATCH: no try/except wrapping data_collector imports.
- R-DATACOLLECTOR-TOKEN-NONCE-UNIQUE: AEAD nonces unique per token (per Cycle 2 RT-C2-07).
- R-DATACOLLECTOR-ENV-VAR-PROHIBIT-BYPASS: no env-var auto-confirm path (per Cycle 1 RT-23 + Cycle 2 RT-C2-13).

See `pipeline/blueprint/v0.1/section_13_data_collector.md` §13.16.6.4 for the final v1 LOCK
gate roster (8 codes) + AST-lint roster (13 extensions).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import ClassVar, Literal, Optional, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Input contract dataclasses — frozen, kw_only (per §13.4 input contracts)
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class OutboundBatchComposeInput:
    """Per §13.4.1; PRE-gate enforced bundle invariants per §13.4.1 invariants section."""
    run_id: str
    org_slug: str
    grant_id: str
    period_n: int
    proposal_commitments_path: str
    reporting_template_path: str
    consent_ledger_dir: str
    sub_awardee_token_register_dir: str
    state_rules_card_dir: str
    channels_in_scope: list[str]
    frequency_cap_lookback_days: int
    invoked_at_utc: datetime


@dataclass(frozen=True, kw_only=True)
class OutboundBatchSendInput:
    """Per §13.4.2; signed batch envelope path required."""
    run_id: str
    org_slug: str
    grant_id: str
    period_n: int
    signed_batch_path: str
    invoked_at_utc: datetime


@dataclass(frozen=True, kw_only=True)
class InboundParseInput:
    """Per §13.4.3; org_slug resolved via per-channel recipient resolver."""
    run_id: str
    org_slug: str
    grant_id: str | None
    channel: Literal["email", "sms", "voice", "telegram", "whatsapp"]
    raw_payload: bytes
    receipt_metadata: dict
    received_at_utc: datetime


@dataclass(frozen=True, kw_only=True)
class InboundClassifyInput:
    """Per §13.4.4; TTY required (no --yes/--force/env-var-bypass)."""
    run_id: str
    org_slug: str
    grant_id: str
    inbound_log_dir: str
    invoked_at_utc: datetime


# ---------------------------------------------------------------------------
# Data contract dataclasses (per §13.5 output contracts)
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class OutboundMessage:
    """Per outbound_message.v1 schema (§13.5.0); per-recipient signed by operator
    including grant_id+org_slug per Cycle 2 RT-C2-01 closure."""
    outbound_id: str
    dc_run_id: str
    recipient_id: str
    channel: Literal["email", "sms", "voice", "telegram", "whatsapp"]
    grant_id: str
    org_slug: str
    commitment_id_or_funder_reporting_field_id: str
    rendered_message_bytes_sha3_512: str  # full 128-hex-char digest per Cycle 1 RT-13
    per_state_disclaimers_applied: list[str]
    per_recipient_token_id: str
    staged_at_utc: datetime
    sent_at_utc: datetime | None
    per_recipient_signature: bytes  # Ed25519 over canonical-JSON including grant_id+org_slug per Cycle 2 RT-C2-01


@dataclass(frozen=True, kw_only=True)
class InboundResponse:
    """Per inbound_response.v1 schema (§13.5.0)."""
    inbound_id: str
    dc_run_id: str
    recipient_id: str
    channel: Literal["email", "sms", "voice", "telegram", "whatsapp"]
    outbound_id_ref: str | None
    raw_payload_sha3_512: str
    token_validated_at_utc: datetime | None
    parsed_fields: dict
    classification_status: Literal["UNSET", "OPERATOR_CLASSIFIED", "DEFAULT_CONFIDENTIAL_PENDING_REVIEW"]
    kfr_drift_advisory: dict | None


@dataclass(frozen=True, kw_only=True)
class ConsentLedgerEntry:
    """Per consent_ledger_entry.v1 schema (§13.5.0 + §13.5.3); cross-channel propagation per Cycle 1 RT-02."""
    recipient_id: str
    channel: Literal["email", "sms", "voice", "telegram", "whatsapp"]
    consent_active: bool
    consent_captured_at_utc: datetime
    consent_capture_method: Literal[
        "award_acceptance_signed_form",
        "opt_in_link_email",
        "sms_double_opt_in",
        "voice_recorded_consent",
        "telegram_in_app_optin",
        "whatsapp_business_optin",
    ]
    opt_out_active: bool
    opt_out_at_utc: datetime | None
    opt_out_propagated_from_channel: list[str]  # Cycle 1 RT-02 closure
    frequency_cap_lookback_days: int
    recent_outbound_log: list[dict]
    state_code_for_rules: str | None
    audit_chain: list[dict]


@dataclass(frozen=True, kw_only=True)
class SubAwardeeToken:
    """Per sub_awardee_token.v1 schema (§13.5.0 + §13.6.0 + §13.8.8); channel-bound per Cycle 1 RT-10;
    revoked field per Cycle 1 RT-12; AEAD-encrypted with per-token nonce per Cycle 2 RT-C2-07."""
    token_id: str
    grant_id: str
    recipient_id: str
    channel_binding: Literal["email", "sms", "voice", "telegram", "whatsapp"]  # Cycle 1 RT-10
    secret_value_ciphertext: bytes
    aead_nonce: bytes  # 12-byte random; Cycle 2 RT-C2-07
    issued_at_utc: datetime
    rotates_at_utc: datetime
    revoked: bool  # Cycle 1 RT-12
    revoked_at_utc: datetime | None
    operator_signature: bytes


@dataclass(frozen=True, kw_only=True)
class StateRulesCardEntry:
    """Per state_rules_card_entry.v1 schema (§13.8.7); SN-LLC Ed25519-signed; mandatory signature verification."""
    state_code: Literal["PA", "CA", "FL", "TX", "NY"]  # v0.2 first wave; expandable via SN-LLC release
    email_disclaimers: list[dict]
    sms_quiet_hours: tuple[str, str]
    sms_required_opt_out_shortcodes: list[str]
    sms_minimum_consent_age_days: int
    voice_quiet_hours: tuple[str, str]
    voice_automated_call_disclosure_script: str
    voice_state_dnc_check_required: bool
    whatsapp_disclaimers: list[dict]
    card_version: str
    signed_by_sn_llc_at_utc: datetime
    signed_by_sn_llc_pubkey_fingerprint: str
    signature: bytes


@dataclass(frozen=True, kw_only=True)
class SendResult:
    """Per-recipient SendResult per §13.4.2 + §13.7 four-layer defense.

    Returned by ``outbound_batch.dispatch_after_operator_approval`` for each
    recipient in ``approved_recipient_order``. ``sent=True`` indicates the
    transport substrate accepted the outbound; ``sent=False`` carries a
    structured reason tag matching one of the fail-closed sub-tags enumerated
    in §13.9.4 + §13.16 Cycle 1/2 dispositions:

    - ``operator_signature_invalid`` (Layer-2 dispatcher signature check)
    - ``operator_signature_grant_or_org_mismatch`` (RT-C2-01 closure)
    - ``per_recipient_signature_invalid`` (RT-14 closure)
    - ``per_recipient_signature_grant_or_org_mismatch`` (RT-C2-01 closure)
    - ``send_time_consent_drift`` (RT-01 closure)
    - ``batch_status_not_approved_for_send`` (Layer-2 PRE-gate)
    - ``batch_recipient_order_swap`` (RT-C2-12 closure)
    - ``transport_timeout_during_send_lock_hold`` (RT-C2-05 closure)
    - ``transport_substrate_not_wired`` (production binding pending)
    - ``channel_not_registered`` (dispatcher channel registry mismatch)
    - ``ledger_absent`` (F-DATACOLLECTOR-CONSENT-MISSING.ledger_absent)
    """
    outbound_id: str
    recipient_id: str
    channel: Literal["email", "sms", "voice", "telegram", "whatsapp"]
    sent: bool
    reason: str | None
    provider_response: dict | None = None
    consent_state_hash_at_compose: str | None = None
    consent_state_hash_at_send: str | None = None


@dataclass(frozen=True, kw_only=True)
class SignedBatchEnvelope:
    """Per signed_batch_envelope.v1 schema (§13.4.2 + §13.5.0); per-recipient signatures including
    grant_id+org_slug per Cycle 2 RT-C2-01; approved_recipient_order per Cycle 2 RT-C2-12."""
    batch_id: str
    compose_run_id: str
    grant_id: str
    org_slug: str
    period_n: int
    batch_status: Literal["UNSIGNED", "APPROVED_FOR_SEND", "SENT", "ABORTED"]
    batch_content_sha3_512: str  # full 128-hex-char digest per Cycle 1 RT-13
    batch_manifest_sha3_512: str  # per Cycle 1 RT-14
    approved_recipient_order: list[str]  # ordered recipient_id list; Cycle 2 RT-C2-12
    per_recipient_consent_state_sha3_512_full: dict  # Cycle 1 RT-01 send-time consent re-read
    signed_at_utc: datetime
    signed_by: str  # operator key ID
    signature: bytes  # Ed25519 over canonical-JSON of envelope contents


# ---------------------------------------------------------------------------
# ChannelProtocol Protocol-DI definition (per §13.4.0)
# ---------------------------------------------------------------------------

@runtime_checkable
class ChannelProtocol(Protocol):
    """Per §13.4.0 common ChannelProtocol contract.

    Every per-channel module implements this Protocol. No autosend code path; send() invocation
    only from outbound_batch.dispatch_after_operator_approval per R-DATACOLLECTOR-NO-AUTOSEND
    AST-lint extension.
    """
    channel_name: ClassVar[Literal["email", "sms", "voice", "telegram", "whatsapp"]]

    def compose_outbound(
        self,
        *,
        org_slug: str,
        grant_id: str,
        recipient: dict,
        commitment_id_or_funder_reporting_field_id: str,
        per_state_disclaimers: list[dict],
        per_recipient_token: SubAwardeeToken,
    ) -> OutboundMessage: ...

    def send(
        self,
        *,
        message: OutboundMessage,
        operator_batch_signature: SignedBatchEnvelope,
    ) -> dict: ...

    def parse_inbound(
        self,
        *,
        raw_payload: bytes,
        receipt_metadata: dict,
    ) -> InboundResponse: ...

    def validate_inbound_token(
        self,
        *,
        inbound: InboundResponse,
        expected_token: SubAwardeeToken,
    ) -> dict: ...


# ---------------------------------------------------------------------------
# Mode dispatcher — four cycles registered (per §13.12 pipeline placement)
# ---------------------------------------------------------------------------

REGISTERED_CYCLES: dict[str, str] = {
    "outbound_batch_compose": "compose_batch",
    "outbound_batch_send": "send_batch",
    "inbound_parse": "parse_inbound",
    "inbound_classify": "classify_inbound",
}


# ---------------------------------------------------------------------------
# Cedar engine mandatory instantiation at module load (per Cycle 1 RT-06 +
# Cycle 2 RT-C2-04 closures). At v0.2 first ship the Cedar engine is a skeleton;
# Code phase realizes the full engine instantiation.
# ---------------------------------------------------------------------------

class CriticalPolicyError(BaseException):
    """Raised on Cedar engine load failure; subclasses BaseException so upstream
    try/except Exception blocks cannot swallow per Cycle 2 RT-C2-04 closure."""


# Module-level handle to the loaded Cedar engine. Populated by
# ``_bootstrap_cedar_engine`` at module load. Tests can introspect via the
# canonical name ``_cedar_engine`` (not part of the public API; the engine
# itself is accessible via :func:`get_cedar_engine` for downstream consumers).
_cedar_engine: Optional["CedarEngineRef"] = None  # type: ignore[name-defined]


class CedarEngineRef(Protocol):
    """Structural alias for ``pipeline.logician.cedar_eval.CedarEngine``.

    Defined inline so that the data_collector seat does not eager-import the
    Cedar engine module at type-checking time; the actual engine class is
    imported lazily inside ``_bootstrap_cedar_engine``.
    """

    def load_all(self) -> None: ...

    def is_ready(self) -> bool: ...

    def loaded_policy_names(self) -> tuple[str, ...]: ...


_CEDAR_POLICY_DIR: Path = Path(__file__).parent / "cedar_policies"


def _bootstrap_cedar_engine() -> None:
    """Mandatory Cedar engine instantiation at module load.

    WS-I Code phase Slice 3 (2026-05-11): full CedarEngine wiring per
    §13.16.1 RT-06 + §13.16.6.2 RT-C2-04 closures.

    The Cedar engine is loaded from the bundled policy directory shipped
    alongside this module (``./cedar_policies/``). Load failure raises
    :class:`CriticalPolicyError` which subclasses :class:`BaseException` so
    upstream ``try/except Exception`` blocks cannot silently swallow Cedar
    engine load failures (Cycle 2 RT-C2-04). The readiness check is
    identity-strict (``engine.is_ready() is True``) per v7.0.7 §4.3.4
    identity-strict pattern (Cycle 2 RT-C2-04 + RT-06 mirror).
    """
    # Lazy import so the data_collector package remains importable even if
    # downstream Cedar engine substrate were unavailable at packaging time
    # (the load failure still fail-closes here; the import deferral exists to
    # avoid eager type-checking coupling).
    from pipeline.logician.cedar_eval import CedarEngine

    engine = CedarEngine(policy_dir=_CEDAR_POLICY_DIR)
    try:
        engine.load_all()
    except BaseException as exc:
        raise CriticalPolicyError(
            f"Cedar engine load failure at module load: {exc}"
        ) from exc
    if engine.is_ready() is not True:
        # Identity-strict per v7.0.7 §4.3.4 + Cycle 2 RT-C2-04 closure.
        raise CriticalPolicyError(
            "CedarEngine.is_ready() returned non-True; fail-closed"
        )
    globals()["_cedar_engine"] = engine


def get_cedar_engine() -> CedarEngineRef:
    """Return the module-load Cedar engine handle.

    Raises :class:`CriticalPolicyError` if the engine is not available — this
    branch is unreachable in practice because ``_bootstrap_cedar_engine`` is
    invoked at module import and any failure aborts the import. Defensive
    helper kept so downstream callers do not need to introspect module
    globals directly.
    """
    engine = globals().get("_cedar_engine")
    if engine is None:
        raise CriticalPolicyError(
            "Cedar engine not initialised; _bootstrap_cedar_engine() did not "
            "run or aborted before assignment"
        )
    return engine


_bootstrap_cedar_engine()


# ---------------------------------------------------------------------------
# Gate predicate registry — WS-I Code phase 2026-05-10
#
# All eight predicates are realized at `pipeline/logician/gates/f_datacollector_*.py`.
# Skeleton stubs were retired here; REGISTERED_GATES now points to the
# canonical `check_*` callables from the logician package. Modules are imported
# lazily inside `_load_gate_registry` so that the data_collector package
# remains importable even if an individual gate module fails to import (which
# in turn would surface its own ImportError at first use, not at module load).
# ---------------------------------------------------------------------------

GATE_CODE_CONSENT_MISSING: str = "F-DATACOLLECTOR-CONSENT-MISSING"
GATE_CODE_OPT_OUT_ACTIVE: str = "F-DATACOLLECTOR-OPT-OUT-ACTIVE"
GATE_CODE_FREQUENCY_CAP_EXCEEDED: str = "F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED"
GATE_CODE_PII_LEAK_IN_OUTBOUND: str = "F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND"
GATE_CODE_KFR_DRIFT: str = "F-DATACOLLECTOR-KFR-DRIFT"
GATE_CODE_INBOUND_CLASSIFICATION_UNSET: str = "F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET"
GATE_CODE_BENEFICIARY_CONSENT_TIER: str = "F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER"
GATE_CODE_OPT_OUT_PROPAGATION_FAILED: str = "F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED"


def _load_gate_registry() -> dict[str, object]:
    """Lazy-import the eight realized gate predicates and return the registry."""
    from pipeline.logician.gates.f_datacollector_consent_missing import (
        check_consent_missing,
    )
    from pipeline.logician.gates.f_datacollector_opt_out_active import (
        check_opt_out_active,
    )
    from pipeline.logician.gates.f_datacollector_frequency_cap_exceeded import (
        check_frequency_cap_exceeded,
    )
    from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
        check_semantic_slot_in_outbound,
    )
    from pipeline.logician.gates.f_datacollector_kfr_drift import check_kfr_drift
    from pipeline.logician.gates.f_datacollector_inbound_classification_unset import (
        check_inbound_classification_unset,
    )
    from pipeline.logician.gates.f_datacollector_beneficiary_consent_tier import (
        check_beneficiary_consent_tier,
    )
    from pipeline.logician.gates.f_datacollector_opt_out_propagation_failed import (
        check_opt_out_propagation_failed,
    )
    return {
        GATE_CODE_CONSENT_MISSING: check_consent_missing,
        GATE_CODE_OPT_OUT_ACTIVE: check_opt_out_active,
        GATE_CODE_FREQUENCY_CAP_EXCEEDED: check_frequency_cap_exceeded,
        # The PII-LEAK gate is consolidated; the package exports a callable per
        # sub-check. The semantic-slot check is the canonical default entry
        # point (mirrors F-CLASS-SLOT-ID-NON-OPAQUE); other sub-checks are
        # exported from the gate module directly.
        GATE_CODE_PII_LEAK_IN_OUTBOUND: check_semantic_slot_in_outbound,
        GATE_CODE_KFR_DRIFT: check_kfr_drift,
        GATE_CODE_INBOUND_CLASSIFICATION_UNSET: check_inbound_classification_unset,
        GATE_CODE_BENEFICIARY_CONSENT_TIER: check_beneficiary_consent_tier,
        GATE_CODE_OPT_OUT_PROPAGATION_FAILED: check_opt_out_propagation_failed,
    }


REGISTERED_GATES: dict[str, object] = _load_gate_registry()


# ---------------------------------------------------------------------------
# Outbound batch dispatcher — Slice 2 (2026-05-10)
# ---------------------------------------------------------------------------
# Lazy-imported so the package remains importable even if cryptography or
# other downstream substrates are missing on a partial Golden Image. The
# AST-lint rule R-DATACOLLECTOR-NO-AUTOSEND (Slice 3) recognizes
# ``outbound_batch.dispatch_after_operator_approval`` by name; re-export here
# also makes it the canonical import path for the operator-approval surface.

def _load_outbound_batch():  # pragma: no cover — exercised by tests
    from pipeline.orchestrator.seats.data_collector.outbound_batch import (
        dispatch_after_operator_approval,
    )
    return dispatch_after_operator_approval


__all__ = [
    "OutboundBatchComposeInput",
    "OutboundBatchSendInput",
    "InboundParseInput",
    "InboundClassifyInput",
    "OutboundMessage",
    "InboundResponse",
    "ConsentLedgerEntry",
    "SubAwardeeToken",
    "StateRulesCardEntry",
    "SendResult",
    "SignedBatchEnvelope",
    "ChannelProtocol",
    "REGISTERED_CYCLES",
    "REGISTERED_GATES",
    "GATE_CODE_BENEFICIARY_CONSENT_TIER",
    "GATE_CODE_CONSENT_MISSING",
    "GATE_CODE_FREQUENCY_CAP_EXCEEDED",
    "GATE_CODE_INBOUND_CLASSIFICATION_UNSET",
    "GATE_CODE_KFR_DRIFT",
    "GATE_CODE_OPT_OUT_ACTIVE",
    "GATE_CODE_OPT_OUT_PROPAGATION_FAILED",
    "GATE_CODE_PII_LEAK_IN_OUTBOUND",
    "CriticalPolicyError",
    "CedarEngineRef",
    "get_cedar_engine",
    "_load_outbound_batch",
]
