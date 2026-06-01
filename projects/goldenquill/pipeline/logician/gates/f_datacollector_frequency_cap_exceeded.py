"""F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED — PRE pre-outbound gate.

Per §13 Data Collector v1 LOCKED 2026-05-10 §13.9.3 + Cycle-1 RT-04 closure
(strict-default channel-switching-evasion at v0.2 first ship) + RT-05
closure (state-cap intersects-with default; never relaxes).

Refuses outbound where:
  (a) per-recipient × per-channel frequency cap exceeded within the rolling
      ``frequency_cap_lookback_days`` window, OR
  (b) per-state card ``<channel>_min_interval_hours`` cap exceeded
      (intersection-with-default per RT-05; stricter wins), OR
  (c) channel-switching evasion strict mode enabled and recipient has
      cross-channel outbound within the lookback window (RT-04 — default
      ``True`` at v0.2 first ship).

Sub-tags (canonical at v1 LOCK):

* ``.recipient_channel_cap`` — default 7-day rolling-window per-channel cap.
* ``.state_cap`` — per-state card override (e.g., PA SMS 48h).
* ``.channel_switching_evasion`` — recipient hit on a different channel
  within window AND strict mode active.
* ``.state_intersection_default_overridden`` — RT-05 closure: state cap is
  STRICTER than default 7-day; cap evaluated against ``max(default,
  state_min_interval)``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Final, Mapping, Optional, Sequence

F_DATACOLLECTOR_FREQUENCY_CAP_EXCEEDED: Final[str] = (
    "F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED"
)

PERMITTED_CHANNELS: Final[frozenset[str]] = frozenset({
    "email",
    "sms",
    "voice",
    "telegram",
    "whatsapp",
})

SUB_TAG_RECIPIENT_CHANNEL_CAP: Final[str] = ".recipient_channel_cap"
SUB_TAG_STATE_CAP: Final[str] = ".state_cap"
SUB_TAG_CHANNEL_SWITCHING_EVASION: Final[str] = ".channel_switching_evasion"
SUB_TAG_STATE_INTERSECTION_DEFAULT_OVERRIDDEN: Final[str] = (
    ".state_intersection_default_overridden"
)


@dataclass(frozen=True, kw_only=True)
class FrequencyCapResult:
    """Result of an F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED sub-check."""

    success: bool
    failure_code: Optional[str]
    sub_tag: Optional[str]
    detail: str
    recipient_id: Optional[str] = None
    channel: Optional[str] = None


def _coerce_utc(value: object) -> Optional[datetime]:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
    if isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            return None
    return None


def check_frequency_cap_exceeded(
    *,
    recipient_id: str,
    channel: str,
    now: datetime,
    recent_outbound_log: Sequence[Mapping[str, object]],
    frequency_cap_lookback_days: int,
    state_min_interval_hours: Optional[int] = None,
    cross_channel_outbound_log: Sequence[Mapping[str, object]] = (),
    channel_switching_evasion_strict: bool = True,
) -> FrequencyCapResult:
    """PRE pre-outbound frequency-cap check.

    Parameters
    ----------
    recipient_id
        Per-recipient opaque identifier.
    channel
        One of ``PERMITTED_CHANNELS``.
    now
        Compose-time UTC timestamp.
    recent_outbound_log
        Per-(recipient, channel) outbound entries with at least
        ``sent_at_utc`` field; gate filters to the lookback window.
    frequency_cap_lookback_days
        Default per-recipient × per-channel rolling-window cap (days). At
        v0.2 first ship the default is 7 per §13.4.1.
    state_min_interval_hours
        Per-state card override (e.g., PA SMS = 48h). ``None`` = no
        state-specific override.
    cross_channel_outbound_log
        Per-recipient outbound entries on OTHER channels within the lookback
        window; consulted only when ``channel_switching_evasion_strict=True``.
    channel_switching_evasion_strict
        RT-04 closure default at v0.2 first ship: ``True``. Operator-signed
        config may set False.
    """
    if channel not in PERMITTED_CHANNELS:
        return FrequencyCapResult(
            success=False,
            failure_code=F_DATACOLLECTOR_FREQUENCY_CAP_EXCEEDED,
            sub_tag=None,
            detail=(
                f"channel {channel!r} not in permitted set "
                f"{sorted(PERMITTED_CHANNELS)}"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    if frequency_cap_lookback_days < 1:
        return FrequencyCapResult(
            success=False,
            failure_code=F_DATACOLLECTOR_FREQUENCY_CAP_EXCEEDED,
            sub_tag=SUB_TAG_RECIPIENT_CHANNEL_CAP,
            detail=(
                f"frequency_cap_lookback_days={frequency_cap_lookback_days} "
                "must be >= 1 (per RT-C2-09 closure); fail-closed"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    default_window = timedelta(days=frequency_cap_lookback_days)
    state_window = (
        timedelta(hours=state_min_interval_hours)
        if state_min_interval_hours is not None
        else None
    )
    # Effective window per RT-05: stricter wins.
    effective_window = default_window
    state_overrides_default = False
    if state_window is not None and state_window > default_window:
        effective_window = state_window
        state_overrides_default = True

    cutoff = now - effective_window
    in_window: list[datetime] = []
    for entry in recent_outbound_log:
        ts = _coerce_utc(entry.get("sent_at_utc"))
        if ts is None:
            continue
        if ts >= cutoff:
            in_window.append(ts)
    if in_window:
        if state_overrides_default:
            sub_tag = SUB_TAG_STATE_INTERSECTION_DEFAULT_OVERRIDDEN
        elif state_min_interval_hours is not None:
            sub_tag = SUB_TAG_STATE_CAP
        else:
            sub_tag = SUB_TAG_RECIPIENT_CHANNEL_CAP
        return FrequencyCapResult(
            success=False,
            failure_code=F_DATACOLLECTOR_FREQUENCY_CAP_EXCEEDED,
            sub_tag=sub_tag,
            detail=(
                f"{len(in_window)} outbound(s) within effective window "
                f"{effective_window} for (recipient={recipient_id!r}, "
                f"channel={channel!r}); cap=1; most recent at "
                f"{max(in_window).isoformat()}"
            ),
            recipient_id=recipient_id,
            channel=channel,
        )
    if channel_switching_evasion_strict and cross_channel_outbound_log:
        cross_in_window: list[tuple[str, datetime]] = []
        for entry in cross_channel_outbound_log:
            ts = _coerce_utc(entry.get("sent_at_utc"))
            other_channel = entry.get("channel")
            if ts is None or not isinstance(other_channel, str):
                continue
            if other_channel == channel:
                continue
            if ts >= cutoff:
                cross_in_window.append((other_channel, ts))
        if cross_in_window:
            return FrequencyCapResult(
                success=False,
                failure_code=F_DATACOLLECTOR_FREQUENCY_CAP_EXCEEDED,
                sub_tag=SUB_TAG_CHANNEL_SWITCHING_EVASION,
                detail=(
                    "channel_switching_evasion_strict=True and recipient "
                    f"has {len(cross_in_window)} cross-channel outbound(s) "
                    f"within window: "
                    + ", ".join(
                        f"{ch}@{ts.isoformat()}" for ch, ts in cross_in_window[:3]
                    )
                ),
                recipient_id=recipient_id,
                channel=channel,
            )
    return FrequencyCapResult(
        success=True,
        failure_code=None,
        sub_tag=None,
        detail=(
            f"frequency cap clear for (recipient={recipient_id!r}, "
            f"channel={channel!r}); 0 outbound in window {effective_window}"
        ),
        recipient_id=recipient_id,
        channel=channel,
    )


__all__ = [
    "F_DATACOLLECTOR_FREQUENCY_CAP_EXCEEDED",
    "FrequencyCapResult",
    "PERMITTED_CHANNELS",
    "SUB_TAG_CHANNEL_SWITCHING_EVASION",
    "SUB_TAG_RECIPIENT_CHANNEL_CAP",
    "SUB_TAG_STATE_CAP",
    "SUB_TAG_STATE_INTERSECTION_DEFAULT_OVERRIDDEN",
    "check_frequency_cap_exceeded",
]
