"""Channel D — Federal program pages (§4.4).

Adapter-per-ALN registry dispatcher. Each adapter yields one or more
:class:`ProgramPageOutcome` page outcomes; the dispatcher applies the
per-adapter cumulative candidate cap (``CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER
= 500``) BEFORE appending any candidate to the run-level list
(A-v3-05 / RT-v2-HIGH-03 closure).

Blueprint anchors:
- §4.4 Channel D full spec (lines 521-531) — implementation target
- §2.1 ``Candidate`` schema (Round 1 ``_types.py``)
- §6.2 F-SCOUT-CHD-01..03 failure codes (+ F-SCOUT-CHD-04 / 05 / 06
  wrappers for runtime fetch / 4xx / missing adapter — see taxonomy below)
- §8 ``CHANNEL_D_MAX_CANDIDATES_PER_PAGE = 200``,
  ``CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER = 500`` (Round 1
  ``_constants.py``)
- §2.1 Candidate.feed_or_adapter_id prefix ``"aln:"`` (A-v3-09 closure)

Registration model.
  ``register_program_page(aln_number)`` NFC-strip-normalises the raw ALN
  (e.g. ``" 10.027 "`` → ``"10.027"``) and stores the wrapped callable in
  :data:`PROGRAM_PAGE_ADAPTERS`. Duplicate normalised ALNs raise
  :class:`ScoutConfigError` tagged ``F-SCOUT-CHD-01``.

Adapter contract.
  Adapters are callables ``(AdapterContext) -> Iterator[ProgramPageOutcome]``.
  Each yielded outcome represents one page; the dispatcher checks the
  per-adapter cumulative budget before appending the page's candidates
  and truncates the final page mid-stream if the cap is hit. Adapters
  SHOULD enforce the per-page cap of 200 locally (A-04 memory invariant)
  so the ``ProgramPageOutcome.page_candidates`` tuple never exceeds 200
  rows; the dispatcher also caps per-page defensively — a misbehaving
  adapter returning 10 000 rows in one page still cannot overshoot 200
  candidates appended from that single page call.

Channel-D state aggregation — §4.4 line 531.
  OK if all adapters succeeded with zero cap / fetch events; DEGRADED on
  any single fetch failure OR any page hit of ``F-SCOUT-CHD-02`` OR any
  adapter hit of ``F-SCOUT-CHD-03``; FAILED only if all registered
  adapters failed.

No module-level side effects on import.
"""

from __future__ import annotations

import unicodedata
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Callable, Final, Iterator, Mapping, Optional, Protocol

from pipeline.scout._constants import (
    CHANNEL_D,
    CHANNEL_D_MAX_CANDIDATES_PER_PAGE,
    CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER,
    FEED_PREFIX_ALN,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
)
from pipeline.scout._types import Candidate
from pipeline.scout.channel_a_federal_apis import (
    ClockFn,
    FDBroker,
    HTTPClient,
    NonceRegistry,
    SessionLike,
)
from pipeline.scout.channel_c_portals import (
    AdapterContext,
    PortalSubEvent,
    ScoutConfigError,
    _default_clock,
    http_request_with_retries,
)

__all__ = [
    "ChannelDDegradationEvent",
    "ChannelDDiscoverResult",
    "PROGRAM_PAGE_ADAPTERS",
    "ProgramPageAdapter",
    "ProgramPageOutcome",
    "ProgramPageSubEvent",
    "_build_channel_d_candidate",
    "_normalize_aln",
    "channel_d_reset_registry_for_tests",
    "classify_channel_d",
    "discover_channel_d",
    "register_program_page",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


SEVERITY_LOW: Final[str] = "LOW"
SEVERITY_MEDIUM: Final[str] = "MEDIUM"
SEVERITY_HIGH: Final[str] = "HIGH"

F_SCOUT_CHD_01: Final[str] = "F-SCOUT-CHD-01"  # duplicate adapter at register
F_SCOUT_CHD_02: Final[str] = "F-SCOUT-CHD-02"  # per-page cap hit
F_SCOUT_CHD_03: Final[str] = "F-SCOUT-CHD-03"  # per-adapter cumulative cap hit
F_SCOUT_CHD_04: Final[str] = "F-SCOUT-CHD-04"  # adapter raised / fetch exhausted
F_SCOUT_CHD_05: Final[str] = "F-SCOUT-CHD-05"  # adapter returned unknown state (reserved)
F_SCOUT_CHD_06: Final[str] = "F-SCOUT-CHD-06"  # roster ALN has no adapter


# ---------------------------------------------------------------------------
# Channel D dataclasses + Protocols
# ---------------------------------------------------------------------------


# Reuse the same sub-event shape as Channel C. The alias keeps Channel D's
# adapter-authoring surface self-documenting without forcing a Channel-D-
# specific type.
ProgramPageSubEvent = PortalSubEvent


@dataclass(frozen=True, kw_only=True)
class ProgramPageOutcome:
    """One page yielded by a Channel D program-page adapter.

    ``page_candidates`` SHOULD be capped at
    ``CHANNEL_D_MAX_CANDIDATES_PER_PAGE = 200`` by the adapter itself (A-04
    memory invariant). The dispatcher caps defensively anyway.

    ``page_state`` ∈ {HEALTH_OK, HEALTH_DEGRADED, HEALTH_FAILED}. Per-page
    state feeds the adapter's aggregate state: any HEALTH_FAILED page
    propagates FAILED to the adapter; DEGRADED pages keep the adapter
    DEGRADED; all-OK pages keep the adapter OK.

    Adapters MAY set ``page_raw_count`` to the number of rows the source
    actually produced BEFORE the 200-cap truncation; the dispatcher uses
    this for the F-SCOUT-CHD-02 overflow telemetry. If omitted (None),
    the dispatcher uses ``len(page_candidates)`` as the raw count.
    """

    page_candidates: tuple[Candidate, ...]
    page_state: str
    page_events: tuple[ProgramPageSubEvent, ...] = ()
    page_raw_count: Optional[int] = None


class ProgramPageAdapter(Protocol):
    def __call__(
        self, ctx: AdapterContext
    ) -> Iterator[ProgramPageOutcome]: ...


@dataclass(frozen=True, kw_only=True)
class ChannelDDegradationEvent:
    aln_number: str
    code: str
    reason_tag: Optional[str]
    severity: str
    overflow_count: int = 0


@dataclass(frozen=True, kw_only=True)
class ChannelDDiscoverResult:
    candidates: tuple[Candidate, ...]
    per_adapter_state: Mapping[str, str]
    channel_state: str
    degradation_events: tuple[ChannelDDegradationEvent, ...]


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


PROGRAM_PAGE_ADAPTERS: "OrderedDict[str, ProgramPageAdapter]" = OrderedDict()


def _normalize_aln(raw: str) -> str:
    """Lightweight ALN normalisation — NFC + strip only.

    Unlike Channel C's portal-slug canonicalisation, ALN numbers have a
    fixed format (e.g. ``10.027``) and don't need lossy transliteration
    handling. NFC + strip is sufficient to catch operator-typo whitespace
    collisions.
    """
    if not isinstance(raw, str):
        raise TypeError(f"ALN must be str; got {type(raw).__name__}")
    return unicodedata.normalize("NFC", raw).strip()


def register_program_page(
    aln_number: str,
) -> Callable[[ProgramPageAdapter], ProgramPageAdapter]:
    """Decorator — registers a Channel D program-page adapter under an ALN.

    Duplicate normalised ALNs raise :class:`ScoutConfigError` tagged
    ``F-SCOUT-CHD-01``. Empty / whitespace-only ALNs raise ``ValueError``
    at registration time.
    """

    key = _normalize_aln(aln_number)
    if not key:
        raise ValueError(
            f"register_program_page: aln_number must be non-empty "
            f"after NFC+strip (raw={aln_number!r})"
        )

    def _wrap(fn: ProgramPageAdapter) -> ProgramPageAdapter:
        if key in PROGRAM_PAGE_ADAPTERS:
            existing = PROGRAM_PAGE_ADAPTERS[key]
            existing_name = getattr(existing, "__qualname__", repr(existing))
            raise ScoutConfigError(
                f"{F_SCOUT_CHD_01}: duplicate program-page adapter "
                f"aln_number={key!r} (raw={aln_number!r}); "
                f"existing adapter={existing_name}"
            )
        PROGRAM_PAGE_ADAPTERS[key] = fn
        return fn

    return _wrap


def channel_d_reset_registry_for_tests() -> None:
    """Clear :data:`PROGRAM_PAGE_ADAPTERS` — test-only escape hatch."""
    PROGRAM_PAGE_ADAPTERS.clear()


# ---------------------------------------------------------------------------
# Candidate-builder helper (A-v3-09 prefix assertion)
# ---------------------------------------------------------------------------


def _build_channel_d_candidate(
    *,
    aln_number: str,
    source_key: str,
    title: str,
    funder: str,
    funder_kind: str,
    url: str,
    url_hash: str,
    content_hash: Optional[str],
    close_date_utc: Optional[str],
    award_ceiling: Optional[int],
    award_floor: Optional[int],
    applicant_types: tuple[str, ...],
    program_page_url: Optional[str],
    fetch_timestamp_utc: str,
    fit_score_cached: int,
    cache_provenance: Optional[str],
    candidate_id: str,
) -> Candidate:
    """Construct a Channel D ``Candidate`` with the ``"aln:"`` prefix asserted."""
    feed_or_adapter_id = f"{FEED_PREFIX_ALN}:{aln_number}"
    assert feed_or_adapter_id.startswith(
        f"{FEED_PREFIX_ALN}:"
    ), f"Channel D feed_or_adapter_id must start with {FEED_PREFIX_ALN}:"
    return Candidate(
        candidate_id=candidate_id,
        channel=CHANNEL_D,
        feed_or_adapter_id=feed_or_adapter_id,
        source_key=source_key,
        title=title,
        funder=funder,
        funder_kind=funder_kind,
        url=url,
        close_date_utc=close_date_utc,
        award_ceiling=award_ceiling,
        award_floor=award_floor,
        applicant_types=applicant_types,
        program_page_url=program_page_url,
        fetch_timestamp_utc=fetch_timestamp_utc,
        url_hash=url_hash,
        content_hash=content_hash,
        fit_score_cached=fit_score_cached,
        cache_provenance=cache_provenance,
    )


# ---------------------------------------------------------------------------
# Channel-D state aggregation — §4.4 line 531
# ---------------------------------------------------------------------------


def classify_channel_d(per_adapter_state: Mapping[str, str]) -> str:
    """All OK → OK; any fetch-fail or cap-event → DEGRADED; all FAILED → FAILED.

    Empty roster → FAILED (matches Channel C convention — a misconfigured
    org shouldn't silently report OK).
    """
    values = list(per_adapter_state.values())
    if not values:
        return HEALTH_FAILED
    if all(v == HEALTH_OK for v in values):
        return HEALTH_OK
    if all(v == HEALTH_FAILED for v in values):
        return HEALTH_FAILED
    return HEALTH_DEGRADED


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


def _escalate_state(current: str, incoming: str) -> str:
    priority = {HEALTH_OK: 0, HEALTH_DEGRADED: 1, HEALTH_FAILED: 2}
    if priority.get(incoming, 0) > priority.get(current, 0):
        return incoming
    return current


def discover_channel_d(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    http_client: HTTPClient,
    adapter_roster: tuple[str, ...],
    clock: ClockFn = _default_clock,
) -> ChannelDDiscoverResult:
    """Dispatch registered Channel D program-page adapters.

    The per-adapter cumulative candidate counter is local to this call —
    NOT module-level — so consecutive runs cannot leak budget from one
    run into the next. Roster ALNs are normalised; duplicates dedupe to
    their first roster position.

    Per-adapter accounting:
      * Adapter raises → FAILED + F-SCOUT-CHD-04 (no partial candidates
        from that adapter are kept).
      * Adapter yields pages until exhausted OR per-adapter cap hits.
      * Each page's candidates are truncated to
        ``min(page_raw_count, CHANNEL_D_MAX_CANDIDATES_PER_PAGE)``
        defensively; if the adapter supplied more than 200 rows,
        F-SCOUT-CHD-02 is emitted.
      * Each page's (possibly per-page-truncated) candidates are further
        truncated by the per-adapter cumulative remaining budget; if
        cumulative cap hits mid-page, F-SCOUT-CHD-03 is emitted with the
        total overflow count (across remaining candidates from this page
        + any un-consumed pages that the adapter might still have yielded).
      * Adapter iteration stops as soon as the per-adapter cap hits.

    Per-adapter state:
      * All pages OK + no cap events → OK.
      * Any page FAILED OR adapter raised → FAILED.
      * Any page DEGRADED or any cap event → DEGRADED (unless already FAILED).
    """
    ctx = AdapterContext(
        session=session,
        fd_broker=fd_broker,
        nonce_registry=nonce_registry,
        http_client=http_client,
        clock=clock,
    )

    all_candidates: list[Candidate] = []
    per_adapter_state: "OrderedDict[str, str]" = OrderedDict()
    events: list[ChannelDDegradationEvent] = []
    adapter_counts: dict[str, int] = {}

    seen_alns: set[str] = set()

    for raw_aln in adapter_roster:
        try:
            aln_key = _normalize_aln(raw_aln)
        except TypeError as exc:
            per_adapter_state[str(raw_aln)] = HEALTH_FAILED
            events.append(
                ChannelDDegradationEvent(
                    aln_number=str(raw_aln),
                    code=F_SCOUT_CHD_06,
                    reason_tag=(
                        f"roster_aln_invalid:{type(exc).__name__}:{exc}"
                    ),
                    severity=SEVERITY_HIGH,
                )
            )
            continue

        if not aln_key or aln_key in seen_alns:
            continue
        seen_alns.add(aln_key)

        adapter = PROGRAM_PAGE_ADAPTERS.get(aln_key)
        if adapter is None:
            per_adapter_state[aln_key] = HEALTH_FAILED
            events.append(
                ChannelDDegradationEvent(
                    aln_number=aln_key,
                    code=F_SCOUT_CHD_06,
                    reason_tag="no_adapter_registered",
                    severity=SEVERITY_HIGH,
                )
            )
            continue

        adapter_counts.setdefault(aln_key, 0)
        adapter_state = HEALTH_OK
        cap_hit = False

        try:
            page_iter = adapter(ctx)
        except ScoutConfigError:
            raise
        except Exception as exc:
            per_adapter_state[aln_key] = HEALTH_FAILED
            events.append(
                ChannelDDegradationEvent(
                    aln_number=aln_key,
                    code=F_SCOUT_CHD_04,
                    reason_tag=(
                        f"adapter_raised:{type(exc).__name__}:{exc}"
                    ),
                    severity=SEVERITY_HIGH,
                )
            )
            continue

        try:
            for page in page_iter:
                # cap_hit check lives at the BOTTOM of the loop body
                # (after state/sub-events are recorded) so that the
                # `for page in page_iter` line never pulls a fresh page
                # from the generator after the cap has been hit.

                raw_count = (
                    page.page_raw_count
                    if page.page_raw_count is not None
                    else len(page.page_candidates)
                )

                # Per-page cap (A-04) — defensive truncation at dispatcher
                # level. Adapter SHOULD enforce this itself; if it didn't,
                # we still cap at 200 and emit F-SCOUT-CHD-02.
                if raw_count > CHANNEL_D_MAX_CANDIDATES_PER_PAGE:
                    page_overflow = raw_count - CHANNEL_D_MAX_CANDIDATES_PER_PAGE
                    events.append(
                        ChannelDDegradationEvent(
                            aln_number=aln_key,
                            code=F_SCOUT_CHD_02,
                            reason_tag="per_page_cap_reached",
                            severity=SEVERITY_MEDIUM,
                            overflow_count=page_overflow,
                        )
                    )
                    adapter_state = _escalate_state(
                        adapter_state, HEALTH_DEGRADED
                    )

                page_allowed = page.page_candidates[
                    :CHANNEL_D_MAX_CANDIDATES_PER_PAGE
                ]

                # Per-adapter cumulative cap (A-v3-05).
                remaining = (
                    CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER
                    - adapter_counts[aln_key]
                )
                if remaining <= 0:
                    cumulative_overflow = len(page_allowed)
                    events.append(
                        ChannelDDegradationEvent(
                            aln_number=aln_key,
                            code=F_SCOUT_CHD_03,
                            reason_tag="per_adapter_cap_reached",
                            severity=SEVERITY_MEDIUM,
                            overflow_count=cumulative_overflow,
                        )
                    )
                    adapter_state = _escalate_state(
                        adapter_state, HEALTH_DEGRADED
                    )
                    cap_hit = True
                    break

                if len(page_allowed) > remaining:
                    cumulative_overflow = len(page_allowed) - remaining
                    kept = page_allowed[:remaining]
                    all_candidates.extend(kept)
                    adapter_counts[aln_key] += len(kept)
                    events.append(
                        ChannelDDegradationEvent(
                            aln_number=aln_key,
                            code=F_SCOUT_CHD_03,
                            reason_tag="per_adapter_cap_reached",
                            severity=SEVERITY_MEDIUM,
                            overflow_count=cumulative_overflow,
                        )
                    )
                    adapter_state = _escalate_state(
                        adapter_state, HEALTH_DEGRADED
                    )
                    cap_hit = True
                else:
                    all_candidates.extend(page_allowed)
                    adapter_counts[aln_key] += len(page_allowed)

                if page.page_state == HEALTH_FAILED:
                    adapter_state = HEALTH_FAILED
                elif page.page_state == HEALTH_DEGRADED:
                    adapter_state = _escalate_state(
                        adapter_state, HEALTH_DEGRADED
                    )
                elif page.page_state == HEALTH_OK:
                    pass
                else:
                    adapter_state = HEALTH_FAILED
                    events.append(
                        ChannelDDegradationEvent(
                            aln_number=aln_key,
                            code=F_SCOUT_CHD_05,
                            reason_tag=(
                                f"page_returned_unknown_state:"
                                f"{page.page_state!r}"
                            ),
                            severity=SEVERITY_HIGH,
                        )
                    )

                for sub in page.page_events:
                    events.append(
                        ChannelDDegradationEvent(
                            aln_number=aln_key,
                            code=sub.code,
                            reason_tag=sub.reason_tag,
                            severity=sub.severity,
                        )
                    )

                # Hard break AFTER the current page's state + sub-events are
                # recorded — prevents the `for page in page_iter` line from
                # pulling (and executing the side effects of) the NEXT page
                # before the loop-top `if cap_hit: break` guard can fire.
                if cap_hit:
                    break
        except ScoutConfigError:
            raise
        except Exception as exc:
            adapter_state = HEALTH_FAILED
            events.append(
                ChannelDDegradationEvent(
                    aln_number=aln_key,
                    code=F_SCOUT_CHD_04,
                    reason_tag=(
                        f"page_iter_raised:{type(exc).__name__}:{exc}"
                    ),
                    severity=SEVERITY_HIGH,
                )
            )

        per_adapter_state[aln_key] = adapter_state

    channel_state = classify_channel_d(per_adapter_state)

    return ChannelDDiscoverResult(
        candidates=tuple(all_candidates),
        per_adapter_state=dict(per_adapter_state),
        channel_state=channel_state,
        degradation_events=tuple(events),
    )
