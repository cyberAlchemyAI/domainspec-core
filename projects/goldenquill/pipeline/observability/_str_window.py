"""STR derivation and rolling per-seat distribution accumulation.

Blueprint §5 v6 §5.8 LOCKED 2026-04-19.
"""

from __future__ import annotations

import datetime
from collections import deque
from typing import Final, TypedDict

STR_WINDOW_MIN_SESSIONS: Final[int] = 5
STR_WINDOW_MAX_AGE_DAYS: Final[int] = 30

assert STR_WINDOW_MIN_SESSIONS == 5, (
    "STR_WINDOW_MIN_SESSIONS has been rebound at module load; "
    "refusing to load pipeline.observability._str_window"
)
assert STR_WINDOW_MAX_AGE_DAYS == 30, (
    "STR_WINDOW_MAX_AGE_DAYS has been rebound at module load; "
    "refusing to load pipeline.observability._str_window"
)


class STRWindowResult(TypedDict):
    seat: str
    n_sessions: int
    n_invocations: int
    quantiles: dict[str, float]


def compute_str(
    success_flag: int,
    token_count_input: int,
    token_count_output: int,
) -> float | None:
    """Per-invocation STR derivation (§5.8.1).

    Returns success_flag / (token_count_input + token_count_output),
    or None when the token sum is zero (e.g. cached response or pre-token error).

    Result is in [0.0, 1.0] when defined.
    """
    token_sum = token_count_input + token_count_output
    if token_sum == 0:
        return None
    return success_flag / token_sum


class STRWindow:
    """Rolling per-seat distribution accumulator (§5.8.2).

    Holds a deque of (session_id, session_date, [str_values]) tuples.
    session_date is the UTC date of the earliest InvocationRecord.timestamp in
    that session (i.e. the session start date).

    At query time:
    1. Evict sessions older than STR_WINDOW_MAX_AGE_DAYS days.
    2. If fewer than STR_WINDOW_MIN_SESSIONS sessions remain: return None.
    3. Else: compute quantile envelope over all str values in the window.

    Export discipline: quantile envelope only exits the telemetry commons.
    Per-invocation raw values are never exported (Canary harness reads
    them locally only per §5.8.3).
    """

    def __init__(self, seat: str) -> None:
        self._seat = seat
        # Deque of (session_id: str, session_date: datetime.date, values: list[float])
        self._sessions: deque[tuple[str, datetime.date, list[float]]] = deque()

    def add_session(
        self,
        session_id: str,
        session_date: datetime.date,
        str_values: list[float | None],
    ) -> None:
        """Register a completed session's STR values.

        str_values is the list of compute_str() outputs for all invocations in
        the session; None values (zero-token-sum records) are filtered out.

        session_date must be the UTC date derived from the earliest
        InvocationRecord.timestamp in the session (i.e. the session start date
        per §5.8.2). This is a caller convention in v0.1 (trusted-operator
        envelope); no enforcement is performed by STRWindow itself.

        session_id uniqueness is the caller's responsibility. Duplicate IDs
        will be counted as separate sessions toward the k=5 minimum.
        """
        defined_values = [v for v in str_values if v is not None]
        self._sessions.append((session_id, session_date, defined_values))

    def query(
        self,
        reference_date: datetime.date | None = None,
    ) -> STRWindowResult | None:
        """Compute the quantile envelope over the current window.

        Parameters
        ----------
        reference_date : datetime.date, optional
            Treat this date as "today" for eviction. Defaults to datetime.date.today().

        Returns None if the window has fewer than STR_WINDOW_MIN_SESSIONS
        non-evicted sessions (window not yet warm — not a failure).
        """
        today = reference_date or datetime.date.today()
        cutoff = today - datetime.timedelta(days=STR_WINDOW_MAX_AGE_DAYS)

        # Evict stale sessions in-place (rebuild deque without stale entries).
        live = [
            (sid, sdate, vals)
            for sid, sdate, vals in self._sessions
            if sdate >= cutoff
        ]
        self._sessions = deque(live)

        if len(self._sessions) < STR_WINDOW_MIN_SESSIONS:
            return None

        all_values: list[float] = []
        for _, _, vals in self._sessions:
            all_values.extend(vals)

        if not all_values:
            return None

        return STRWindowResult(
            seat=self._seat,
            n_sessions=len(self._sessions),
            n_invocations=len(all_values),
            quantiles=_compute_quantiles(all_values),
        )

    # Canary harness read — returns raw per-session arrays, local-only (§5.8.3).
    def _raw_sessions_for_canary(
        self,
    ) -> list[tuple[str, datetime.date, list[float]]]:
        return [(sid, sdate, list(vals)) for sid, sdate, vals in self._sessions]


def _compute_quantiles(values: list[float]) -> dict[str, float]:
    """Compute the required quantile envelope over a list of floats."""
    sorted_vals = sorted(values)
    n = len(sorted_vals)

    def percentile(p: float) -> float:
        if n == 1:
            return sorted_vals[0]
        idx = p / 100.0 * (n - 1)
        lo, hi = int(idx), min(int(idx) + 1, n - 1)
        frac = idx - lo
        return sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac

    return {
        "min": float(sorted_vals[0]),
        "p10": percentile(10),
        "p25": percentile(25),
        "p50": percentile(50),
        "p75": percentile(75),
        "p90": percentile(90),
        "max": float(sorted_vals[-1]),
    }
