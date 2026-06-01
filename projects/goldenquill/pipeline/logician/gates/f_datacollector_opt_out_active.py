"""F-DATACOLLECTOR-OPT-OUT-ACTIVE — PRE pre-outbound gate.

Per §13 Data Collector v1 LOCKED 2026-05-10 §13.9.2 + Cycle-1 RT-02 closure
(cross-channel opt-out propagation) + Cycle-2 RT-C2-05 closure (lock-held-
through-transport for same-day enforcement).

Refuses outbound where the recipient opted out post-consent. Same-day
enforcement: rolling-window opt-out re-acceptance disallowed without fresh
consent capture.

Sub-tags (canonical at v1 LOCK):

* ``.opt_out_active_email`` / ``.opt_out_active_sms`` /
  ``.opt_out_active_voice`` / ``.opt_out_active_telegram`` /
  ``.opt_out_active_whatsapp`` — per-channel opt-out flag set.
* ``.cross_channel_propagation_failure`` — RT-02 closure: a STOP signal on
  one channel was received but the propagated opt-out write to a sibling
  channel's ledger entry failed (caller surfaces this state to the gate via
  ``propagation_failure=True``).
* ``.recapture_signature_invalid`` — RT-02 closure: operator-explicit
  re-consent capture present but operator Ed25519 signature does not verify
  against the operator key active at recapture time.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Mapping, Optional

F_DATACOLLECTOR_OPT_OUT_ACTIVE: Final[str] = "F-DATACOLLECTOR-OPT-OUT-ACTIVE"

PERMITTED_CHANNELS: Final[frozenset[str]] = frozenset({
    "email",
    "sms",
    "voice",
    "telegram",
    "whatsapp",
})

SUB_TAG_BY_CHANNEL: Final[Mapping[str, str]] = {
    "email": ".opt_out_active_email",
    "sms": ".opt_out_active_sms",
    "voice": ".opt_out_active_voice",
    "telegram": ".opt_out_active_telegram",
    "whatsapp": ".opt_out_active_whatsapp",
}

SUB_TAG_CROSS_CHANNEL_PROPAGATION_FAILURE: Final[str] = (
    ".cross_channel_propagation_failure"
)
SUB_TAG_RECAPTURE_SIGNATURE_INVALID: Final[str] = (
    ".recapture_signature_invalid"
)


@dataclass(frozen=True, kw_only=True)
class OptOutActiveResult:
    """Result of an F-DATACOLLECTOR-OPT-OUT-ACTIVE sub-check."""

    success: bool
    failure_code: Optional[str]
    sub_tag: Optional[str]
    detail: str
    recipient_id: Optional[str] = None
    channel: Optional[str] = None


def check_opt_out_active(
    *,
    recipient_id: str,
    channel: str,
    ledger_entry: Mapping[str, object],
    propagation_failure: bool = False,
    recapture_signature_valid: Optional[bool] = None,
) -> OptOutActiveResult:
    """PRE pre-outbound opt-out check.

    Parameters
    ----------
    recipient_id
        Per-recipient opaque identifier.
    channel
        One of ``PERMITTED_CHANNELS``.
    ledger_entry
        Already-parsed ledger row.
    propagation_failure
        True iff caller (consent ledger atomic-update path) signals that an
        upstream cross-channel propagation failed; surfaces under
        ``.cross_channel_propagation_failure`` sub-tag.
    recapture_signature_valid
        Optional. None = no recapture record; True = signature verifies;
        False = signature missing/invalid → ``.recapture_signature_invalid``.

    Returns
    -------
    OptOutActiveResult. PASS only when ``opt_out_active=False`` and no
    propagation failure and (if recapture present) signature valid.
    """
    if channel not in PERMITTED_CHANNELS:
        return OptOutActiveResult(
            success=False,
            failure_code=F_DATACOLLECTOR_OPT_OUT_ACTIVE,
            sub_tag=None,
            detail=(
                f"channel {channel!r} not in permitted set "
                f"{sorted(PERMITTED_CHANNELS)}"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    if propagation_failure:
        return OptOutActiveResult(
            success=False,
            failure_code=F_DATACOLLECTOR_OPT_OUT_ACTIVE,
            sub_tag=SUB_TAG_CROSS_CHANNEL_PROPAGATION_FAILURE,
            detail=(
                "cross-channel opt-out propagation failed for "
                f"recipient={recipient_id!r}; refuse outbound on every "
                "channel until propagation is reconciled"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    if recapture_signature_valid is False:
        return OptOutActiveResult(
            success=False,
            failure_code=F_DATACOLLECTOR_OPT_OUT_ACTIVE,
            sub_tag=SUB_TAG_RECAPTURE_SIGNATURE_INVALID,
            detail=(
                "operator-explicit recapture record present but Ed25519 "
                f"signature invalid for recipient={recipient_id!r}, "
                f"channel={channel!r}"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    if ledger_entry.get("opt_out_active") is True:
        return OptOutActiveResult(
            success=False,
            failure_code=F_DATACOLLECTOR_OPT_OUT_ACTIVE,
            sub_tag=SUB_TAG_BY_CHANNEL[channel],
            detail=(
                f"opt_out_active=True for (recipient={recipient_id!r}, "
                f"channel={channel!r}); fresh consent capture required"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    return OptOutActiveResult(
        success=True,
        failure_code=None,
        sub_tag=None,
        detail=(
            "opt_out_active=False for "
            f"(recipient={recipient_id!r}, channel={channel!r})"
        ),
        recipient_id=recipient_id,
        channel=channel,
    )


__all__ = [
    "F_DATACOLLECTOR_OPT_OUT_ACTIVE",
    "OptOutActiveResult",
    "PERMITTED_CHANNELS",
    "SUB_TAG_BY_CHANNEL",
    "SUB_TAG_CROSS_CHANNEL_PROPAGATION_FAILURE",
    "SUB_TAG_RECAPTURE_SIGNATURE_INVALID",
    "check_opt_out_active",
]
