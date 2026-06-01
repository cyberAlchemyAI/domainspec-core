"""F-FUNDER-CORPUS-STALE — POST-cite gate (RFA-truth, P2).

Per architecture v7.0.5 §5.6 + companion `section_04_v7_0_5_companion.md`.
After Scout composes match reasoning OR Scribe completes KGIE preflight,
this gate fires on every Funder Intel doc cited. If the doc's
`last_relevance_event` is older than the per-funder-type stale threshold
AND no operator-confirmed promotion has occurred in the same window, the
citation is flagged for operator REVIEW and the downstream draft is held.

Per-funder-type thresholds (v7.0.5 §5.6 RT-07 closure):

| funder_type            | stale_threshold_days |
|------------------------|----------------------|
| federal_agency         | 365                  |
| regional_authority     | 365                  |
| state_agency           | 365                  |
| private_foundation     | 180                  |
| community_foundation   | 180                  |
| corporate_giving       | 90                   |
| cdfi                   | 180                  |
| county / city          | 365                  |

Operator can override per-doc via `expiry` field; the deterministic check
is `now - last_relevance_event > stale_threshold_days`.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Final, Mapping, Optional

from pipeline.logician.gates._protocols import ClockProtocol


F_FUNDER_CORPUS_STALE: Final[str] = "F-FUNDER-CORPUS-STALE"

# Per-funder-type stale-threshold defaults in days. Per v7.0.5 §5.6 / RT-07.
FUNDER_TYPE_STALE_THRESHOLD_DAYS: Final[Mapping[str, int]] = {
    "federal_agency": 365,
    "regional_authority": 365,
    "state_agency": 365,
    "private_foundation": 180,
    "community_foundation": 180,
    "corporate_giving": 90,
    "cdfi": 180,
    "county": 365,
    "city": 365,
}

# Conservative default for unknown funder types — same as the strictest
# (corporate_giving 90d). Safer to over-flag than under-flag stale corpus.
DEFAULT_STALE_THRESHOLD_DAYS: Final[int] = 90


@dataclass(frozen=True, kw_only=True)
class FunderCorpusStaleResult:
    """Result of F-FUNDER-CORPUS-STALE check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    age_days: Optional[int] = None
    threshold_days: Optional[int] = None


def check_funder_corpus_stale(
    *,
    funder_type: str,
    last_relevance_event: datetime,
    clock: Optional[ClockProtocol] = None,
    expiry_override_days: Optional[int] = None,
) -> FunderCorpusStaleResult:
    """POST-cite gate: cited Funder Intel doc must be within stale window.

    Parameters
    ----------
    funder_type
        Funder type per v7.0.5 schema (federal_agency / private_foundation /
        community_foundation / corporate_giving / cdfi / state_agency /
        regional_authority / county / city). Unknown types default to the
        conservative 90-day threshold.
    last_relevance_event
        UTC datetime when the doc was last operator-promoted or freshly
        cited by Scout. Naive datetimes are assumed UTC.
    clock
        Injected ClockProtocol for time-source. None → uses
        ``datetime.now(timezone.utc)``.
    expiry_override_days
        Operator override for the threshold (per `expiry` field on the
        funder doc schema). When provided, takes precedence over
        funder-type default.

    Returns
    -------
    FunderCorpusStaleResult. Passes when age <= threshold; fails (P2)
    otherwise.
    """
    if expiry_override_days is not None:
        threshold = expiry_override_days
    else:
        threshold = FUNDER_TYPE_STALE_THRESHOLD_DAYS.get(
            funder_type, DEFAULT_STALE_THRESHOLD_DAYS
        )

    now = clock.now() if clock is not None else datetime.now(timezone.utc)

    # Normalize: if last_relevance_event is naive, assume UTC.
    if last_relevance_event.tzinfo is None:
        last_relevance_event = last_relevance_event.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)

    age = now - last_relevance_event
    age_days = max(0, age.days)

    if age <= timedelta(days=threshold):
        return FunderCorpusStaleResult(
            success=True,
            failure_code=None,
            detail=(
                f"funder_type {funder_type!r} doc age {age_days}d "
                f"within threshold {threshold}d"
            ),
            age_days=age_days,
            threshold_days=threshold,
        )
    return FunderCorpusStaleResult(
        success=False,
        failure_code=F_FUNDER_CORPUS_STALE,
        detail=(
            f"funder_type {funder_type!r} doc age {age_days}d exceeds "
            f"threshold {threshold}d — citation flagged for operator REVIEW"
        ),
        age_days=age_days,
        threshold_days=threshold,
    )
