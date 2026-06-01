"""F-DATACOLLECTOR-CONSENT-MISSING — PRE pre-outbound + module-load + send-time gate.

Per §13 Data Collector v1 LOCKED 2026-05-10 (rows 196/197) §13.9.1 + Cycle-1
RT-22 closure (module-load discipline) + RT-01 closure (send-time consent
drift) + Cycle-2 RT-C2-09 closure (operator-config value validation).

Refuses outbound where the consent ledger row is absent, where consent is no
longer active, where consent capture method is unset, where the operator-
config signature is invalid (at module load OR at compose time), or where
the per-recipient consent state hash drifted between compose-time and
send-time.

Sub-tags (canonical at v1 LOCK):

* ``.ledger_absent`` — consent ledger file does not exist for the
  ``(recipient_id, channel)`` pair.
* ``.schema_invalid`` — ledger row exists but fails Pydantic validation.
* ``.consent_inactive`` — ledger row exists, ``consent_active=False``.
* ``.method_unset`` — ``consent_capture_method`` is None or not in the
  enumerated literal set.
* ``.config_signature_invalid`` — ``data_collector_config.yaml`` exists but
  its Ed25519 signature is missing, invalid, or signed by a retired key.
* ``.module_load_config_signature_invalid`` — RT-22 closure: same check at
  module-load time. Same predicate body, different invocation site.
* ``.send_time_consent_drift`` — RT-01 closure: per-recipient consent state
  hash at send time differs from the hash captured in the signed batch
  envelope at compose time.
* ``.config_value_invalid`` — RT-C2-09 closure: signed config carries a
  value outside the permitted range (e.g., ``frequency_cap_lookback_days <
  1``, ``whisper_model_size`` outside hardware-tier whitelist).

The predicate is pure-Python and deterministic. Substrate I/O (consent
ledger reads, signature verification, hardware-tier detection) is performed
by the seat module's helpers; this gate consumes already-parsed inputs.

Bypass: M13 (audited; admin-risk HIGH ``LAW3_VIOLATION``). CAN-SPAM / TCPA
exposure means M13 is operator-grade only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Mapping, Optional

F_DATACOLLECTOR_CONSENT_MISSING: Final[str] = "F-DATACOLLECTOR-CONSENT-MISSING"

PERMITTED_CHANNELS: Final[frozenset[str]] = frozenset({
    "email",
    "sms",
    "voice",
    "telegram",
    "whatsapp",
})

PERMITTED_CONSENT_CAPTURE_METHODS: Final[frozenset[str]] = frozenset({
    "award_acceptance_signed_form",
    "opt_in_link_email",
    "sms_double_opt_in",
    "voice_recorded_consent",
    "telegram_in_app_optin",
    "whatsapp_business_optin",
})

SUB_TAG_LEDGER_ABSENT: Final[str] = ".ledger_absent"
SUB_TAG_SCHEMA_INVALID: Final[str] = ".schema_invalid"
SUB_TAG_CONSENT_INACTIVE: Final[str] = ".consent_inactive"
SUB_TAG_METHOD_UNSET: Final[str] = ".method_unset"
SUB_TAG_CONFIG_SIGNATURE_INVALID: Final[str] = ".config_signature_invalid"
SUB_TAG_MODULE_LOAD_CONFIG_SIGNATURE_INVALID: Final[str] = (
    ".module_load_config_signature_invalid"
)
SUB_TAG_SEND_TIME_CONSENT_DRIFT: Final[str] = ".send_time_consent_drift"
SUB_TAG_CONFIG_VALUE_INVALID: Final[str] = ".config_value_invalid"


@dataclass(frozen=True, kw_only=True)
class ConsentMissingResult:
    """Result of an F-DATACOLLECTOR-CONSENT-MISSING sub-check."""

    success: bool
    failure_code: Optional[str]
    sub_tag: Optional[str]
    detail: str
    recipient_id: Optional[str] = None
    channel: Optional[str] = None


def check_consent_missing(
    *,
    recipient_id: str,
    channel: str,
    ledger_present: bool,
    ledger_entry: Optional[Mapping[str, object]] = None,
) -> ConsentMissingResult:
    """PRE pre-outbound consent-presence check.

    Parameters
    ----------
    recipient_id
        Per-recipient opaque identifier.
    channel
        One of ``PERMITTED_CHANNELS``.
    ledger_present
        Whether the per-(recipient, channel) ledger file exists.
    ledger_entry
        Already-parsed ledger row (Pydantic-validated upstream); ``None`` if
        the file is absent or schema-invalid (caller signals which via
        ``ledger_present`` + content of this argument).

    Returns
    -------
    ConsentMissingResult. PASS only when ledger present, schema valid,
    consent_active True, and consent_capture_method in the enumerated set.
    """
    if channel not in PERMITTED_CHANNELS:
        return ConsentMissingResult(
            success=False,
            failure_code=F_DATACOLLECTOR_CONSENT_MISSING,
            sub_tag=SUB_TAG_SCHEMA_INVALID,
            detail=(
                f"channel {channel!r} not in permitted set "
                f"{sorted(PERMITTED_CHANNELS)}"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    if not ledger_present:
        return ConsentMissingResult(
            success=False,
            failure_code=F_DATACOLLECTOR_CONSENT_MISSING,
            sub_tag=SUB_TAG_LEDGER_ABSENT,
            detail=(
                f"consent ledger absent for (recipient={recipient_id!r}, "
                f"channel={channel!r}) — refuse outbound"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    if ledger_entry is None:
        return ConsentMissingResult(
            success=False,
            failure_code=F_DATACOLLECTOR_CONSENT_MISSING,
            sub_tag=SUB_TAG_SCHEMA_INVALID,
            detail=(
                f"ledger present but Pydantic-invalid for "
                f"(recipient={recipient_id!r}, channel={channel!r})"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    if ledger_entry.get("consent_active") is not True:
        return ConsentMissingResult(
            success=False,
            failure_code=F_DATACOLLECTOR_CONSENT_MISSING,
            sub_tag=SUB_TAG_CONSENT_INACTIVE,
            detail=(
                f"consent_active is not True for "
                f"(recipient={recipient_id!r}, channel={channel!r})"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    method = ledger_entry.get("consent_capture_method")
    if not isinstance(method, str) or method not in PERMITTED_CONSENT_CAPTURE_METHODS:
        return ConsentMissingResult(
            success=False,
            failure_code=F_DATACOLLECTOR_CONSENT_MISSING,
            sub_tag=SUB_TAG_METHOD_UNSET,
            detail=(
                f"consent_capture_method {method!r} not in permitted set "
                f"for (recipient={recipient_id!r}, channel={channel!r})"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    return ConsentMissingResult(
        success=True,
        failure_code=None,
        sub_tag=None,
        detail=(
            f"consent ledger row valid for (recipient={recipient_id!r}, "
            f"channel={channel!r})"
        ),
        recipient_id=recipient_id,
        channel=channel,
    )


def check_config_signature(
    *,
    config_present: bool,
    config_signature_valid: Optional[bool],
    at_module_load: bool = False,
) -> ConsentMissingResult:
    """Operator-config Ed25519 signature check (per §13.4.1 + RT-22).

    Same predicate, different sub-tag depending on call site (compose-time
    vs module-load). Caller passes ``at_module_load=True`` when invoked at
    package import; ``False`` for per-cycle compose checks.
    """
    if not config_present:
        # No config file = nothing to verify; per §13.4.1 CLI per-run override
        # does not require signed config. PASS.
        return ConsentMissingResult(
            success=True,
            failure_code=None,
            sub_tag=None,
            detail="no operator-config file present; per-run CLI override mode",
        )
    if config_signature_valid is True:
        return ConsentMissingResult(
            success=True,
            failure_code=None,
            sub_tag=None,
            detail="operator-config Ed25519 signature verifies",
        )
    sub_tag = (
        SUB_TAG_MODULE_LOAD_CONFIG_SIGNATURE_INVALID
        if at_module_load
        else SUB_TAG_CONFIG_SIGNATURE_INVALID
    )
    return ConsentMissingResult(
        success=False,
        failure_code=F_DATACOLLECTOR_CONSENT_MISSING,
        sub_tag=sub_tag,
        detail=(
            "data_collector_config.yaml present but Ed25519 signature "
            f"verification returned {config_signature_valid!r} "
            f"(at_module_load={at_module_load})"
        ),
    )


def check_send_time_consent_drift(
    *,
    recipient_id: str,
    channel: str,
    consent_state_hash_at_compose: bytes,
    consent_state_hash_at_send: bytes,
) -> ConsentMissingResult:
    """RT-01 closure: send-time consent state hash must match compose-time.

    Per §13.4.2 + §13.16.1 RT-01 — full 512-bit (64-byte) digest comparison
    per RT-13 closure. Constant-time comparison via Python's ``hmac`` to
    avoid timing side-channel.
    """
    import hmac

    if not isinstance(consent_state_hash_at_compose, (bytes, bytearray)):
        return ConsentMissingResult(
            success=False,
            failure_code=F_DATACOLLECTOR_CONSENT_MISSING,
            sub_tag=SUB_TAG_SEND_TIME_CONSENT_DRIFT,
            detail=(
                "consent_state_hash_at_compose is not bytes — fail-closed; "
                f"got {type(consent_state_hash_at_compose).__name__}"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    if not isinstance(consent_state_hash_at_send, (bytes, bytearray)):
        return ConsentMissingResult(
            success=False,
            failure_code=F_DATACOLLECTOR_CONSENT_MISSING,
            sub_tag=SUB_TAG_SEND_TIME_CONSENT_DRIFT,
            detail=(
                "consent_state_hash_at_send is not bytes — fail-closed; "
                f"got {type(consent_state_hash_at_send).__name__}"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    if not hmac.compare_digest(
        bytes(consent_state_hash_at_compose),
        bytes(consent_state_hash_at_send),
    ):
        return ConsentMissingResult(
            success=False,
            failure_code=F_DATACOLLECTOR_CONSENT_MISSING,
            sub_tag=SUB_TAG_SEND_TIME_CONSENT_DRIFT,
            detail=(
                "per-recipient consent state hash drifted between compose "
                f"and send for (recipient={recipient_id!r}, "
                f"channel={channel!r}); recipient opted out or ledger "
                "mutated mid-batch — refuse send for this recipient"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    return ConsentMissingResult(
        success=True,
        failure_code=None,
        sub_tag=None,
        detail=(
            "send-time consent state hash matches compose-time hash for "
            f"(recipient={recipient_id!r}, channel={channel!r})"
        ),
        recipient_id=recipient_id,
        channel=channel,
    )


def check_config_value_ranges(
    *,
    config: Mapping[str, object],
    hardware_tier_whisper_whitelist: Optional[frozenset[str]] = None,
) -> ConsentMissingResult:
    """RT-C2-09 closure: per-field range validation on signed operator-config.

    Even a validly-signed config can carry dangerous values. This check
    enforces:

    * ``frequency_cap_lookback_days >= 1`` (no zero-day caps)
    * ``channel_switching_evasion_strict`` is bool (no None or string sentinel)
    * ``whisper_model_size`` in the hardware-tier whitelist (RT-16 closure)
    """
    cap_lookback = config.get("frequency_cap_lookback_days")
    if cap_lookback is not None:
        if not isinstance(cap_lookback, int) or cap_lookback < 1:
            return ConsentMissingResult(
                success=False,
                failure_code=F_DATACOLLECTOR_CONSENT_MISSING,
                sub_tag=SUB_TAG_CONFIG_VALUE_INVALID,
                detail=(
                    "frequency_cap_lookback_days must be int >= 1; got "
                    f"{cap_lookback!r}"
                ),
            )
    evasion_strict = config.get("channel_switching_evasion_strict")
    if evasion_strict is not None and not isinstance(evasion_strict, bool):
        return ConsentMissingResult(
            success=False,
            failure_code=F_DATACOLLECTOR_CONSENT_MISSING,
            sub_tag=SUB_TAG_CONFIG_VALUE_INVALID,
            detail=(
                "channel_switching_evasion_strict must be bool; got "
                f"{type(evasion_strict).__name__}={evasion_strict!r}"
            ),
        )
    whisper_size = config.get("whisper_model_size")
    if (
        whisper_size is not None
        and hardware_tier_whisper_whitelist is not None
        and whisper_size not in hardware_tier_whisper_whitelist
    ):
        return ConsentMissingResult(
            success=False,
            failure_code=F_DATACOLLECTOR_CONSENT_MISSING,
            sub_tag=SUB_TAG_CONFIG_VALUE_INVALID,
            detail=(
                f"whisper_model_size {whisper_size!r} not in hardware-tier "
                f"whitelist {sorted(hardware_tier_whisper_whitelist)}"
            ),
        )
    return ConsentMissingResult(
        success=True,
        failure_code=None,
        sub_tag=None,
        detail="operator-config field values within permitted ranges",
    )


__all__ = [
    "ConsentMissingResult",
    "F_DATACOLLECTOR_CONSENT_MISSING",
    "PERMITTED_CHANNELS",
    "PERMITTED_CONSENT_CAPTURE_METHODS",
    "SUB_TAG_CONFIG_SIGNATURE_INVALID",
    "SUB_TAG_CONFIG_VALUE_INVALID",
    "SUB_TAG_CONSENT_INACTIVE",
    "SUB_TAG_LEDGER_ABSENT",
    "SUB_TAG_METHOD_UNSET",
    "SUB_TAG_MODULE_LOAD_CONFIG_SIGNATURE_INVALID",
    "SUB_TAG_SCHEMA_INVALID",
    "SUB_TAG_SEND_TIME_CONSENT_DRIFT",
    "check_config_signature",
    "check_config_value_ranges",
    "check_consent_missing",
    "check_send_time_consent_drift",
]
