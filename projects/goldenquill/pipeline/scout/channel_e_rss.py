"""Channel E — RSS / newsletter watchlists (§4.5).

Dispatcher-less-registry DISCOVER adapter. Each feed in ``feed_watchlist`` is
polled via an injected :class:`FeedParserFactory` so the ``feedparser``
library is isolated to :mod:`pipeline.scout._feedparser_adapter`. All the
load-bearing invariants under test are dispatcher-local:

* A-05 / RT-v1-CRIT-05 — 100-entry cap enforced during iteration (101st yield
  breaks BEFORE :func:`_build_channel_e_candidate`).
* A-v3-08 / RT-v2-MED-04 — entry-token streaming break with
  ``.streaming_break`` vs ``.post_fetch_break`` reason-tag dispatch.
* A-v4-01 — mandatory parser-buffer drain on any feed with ``entries_seen > 0``.
* B-v5-04 — :func:`_drain_parser_buffer` hasattr-dispatch across
  ``raw_data`` / ``reset`` / ``drain_api_missing``.

Blueprint anchors:
- §4.5 Channel E full spec (lines 533–546).
- §2.1 ``Candidate`` schema — ``channel == "E"``,
  ``feed_or_adapter_id = "rss:" + sha3_512(feed_url_canonical)[:16].hex()``.
- §6.5 F-SCOUT-E-01..03 + reason-tag sub-codes.
- §8 pins — ``CHANNEL_E_RUNAWAY_MAX = 100``, ``RSS_STALE_FEED_DEGRADED_DAYS = 60``.

No module-level side effects on import: zero network, zero FD reservation,
zero nonce reservation, and — critically — no ``import feedparser`` anywhere
inside this file (the import-hygiene regression depends on it).
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import urllib.parse
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Final, Iterable, Iterator, Mapping, Optional, Protocol

from pipeline.scout._constants import (
    CANDIDATE_ID_HEX_LEN,
    CHANNEL_E,
    CHANNEL_E_RUNAWAY_MAX,
    FEED_PREFIX_RSS,
    FUNDER_UNKNOWN,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
    RSS_STALE_FEED_DEGRADED_DAYS,
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
    ScoutConfigError,
    _default_clock,
    http_request_with_retries,
)

__all__ = [
    "AdapterContext",
    "ChannelEDegradationEvent",
    "ChannelEDiscoverResult",
    "ChannelESubEvent",
    "FeedEntry",
    "FeedParseResult",
    "FeedParserFactory",
    "FeedSpec",
    "ScoutConfigError",
    "_build_channel_e_candidate",
    "_canonical_feed_url",
    "_compute_feed_or_adapter_id",
    "_drain_parser_buffer",
    "classify_channel_e",
    "discover_channel_e",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


SEVERITY_LOW: Final[str] = "LOW"
SEVERITY_MEDIUM: Final[str] = "MEDIUM"
SEVERITY_HIGH: Final[str] = "HIGH"

F_SCOUT_E_01: Final[str] = "F-SCOUT-E-01"
F_SCOUT_E_02: Final[str] = "F-SCOUT-E-02"
F_SCOUT_E_03: Final[str] = "F-SCOUT-E-03"

REASON_MALFORMED_XML: Final[str] = "malformed_xml"
REASON_EMPTY_GUID: Final[str] = "empty_guid"
REASON_HTTP_4XX: Final[str] = "http_4xx"
REASON_FEED_STALE: Final[str] = "feed_stale_channel_e"
REASON_TLS_INVALID: Final[str] = "tls_invalid"
REASON_SERVER_UNREACHABLE: Final[str] = "server_unreachable"
REASON_STREAMING_BREAK: Final[str] = "streaming_break"
REASON_POST_FETCH_BREAK: Final[str] = "post_fetch_break"
REASON_BUFFER_DRAINED: Final[str] = "buffer_drained"
REASON_DRAIN_API_MISSING: Final[str] = "drain_api_missing"


# ---------------------------------------------------------------------------
# Protocols + dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class FeedSpec:
    """Per-feed watchlist entry.

    ``feed_url`` is the raw URL as written in ``rss_watchlist.yaml``. The
    dispatcher canonicalises it via :func:`_canonical_feed_url` at entry
    and the canonical form drives the ``rss:`` :attr:`Candidate.feed_or_adapter_id`
    namespace. ``funder`` / ``funder_kind`` / ``title`` let the roster
    propagate publisher-level metadata onto each emitted Candidate without
    Scout having to synthesise it.
    """

    feed_url: str
    funder: str = ""
    funder_kind: str = FUNDER_UNKNOWN
    title: str = ""
    admin_risk_carry: Optional[str] = None


@dataclass(frozen=True, kw_only=True)
class FeedEntry:
    """One parsed entry yielded by a :class:`FeedParserFactory`.

    Lazily produced — the dispatcher counts ``next()`` yields and breaks at
    101 before the 101st entry is constructed into a :class:`Candidate`.
    """

    guid: str
    link: str
    title: str
    body_bytes: bytes
    published_iso: Optional[str]


@dataclass(frozen=True, kw_only=True)
class FeedParseResult:
    """Return shape of :meth:`FeedParserFactory.parse_streaming`.

    ``entries`` is a lazy iterator; the dispatcher's break on entry-101 pulls
    through a ``next()`` call, so the iterator does not need to materialise
    the whole feed in memory.

    ``streaming`` distinguishes the two reason-tag paths on truncation:
    ``True`` → ``.streaming_break``, ``False`` → ``.post_fetch_break``. The
    production :class:`FeedparserLibFactory` fetches the whole body before
    parsing (``False``); a future streaming factory would set ``True``.
    """

    bozo: bool
    feed_modified_iso: Optional[str]
    entries: Iterator[FeedEntry]
    raw_data_buffer_handle: Any
    streaming: bool = False


class FeedParserFactory(Protocol):
    def parse_streaming(self, raw_body: bytes) -> FeedParseResult: ...


@dataclass(frozen=True, kw_only=True)
class ChannelESubEvent:
    feed_or_adapter_id: str
    code: str
    reason_tag: Optional[str]
    severity: str


@dataclass(frozen=True, kw_only=True)
class ChannelEDegradationEvent:
    feed_or_adapter_id: str
    code: str
    reason_tag: Optional[str]
    severity: str
    overflow_count: int = 0


@dataclass(frozen=True, kw_only=True)
class ChannelEDiscoverResult:
    candidates: tuple[Candidate, ...]
    per_feed_state: Mapping[str, str]
    channel_state: str
    degradation_events: tuple[ChannelEDegradationEvent, ...]


# ---------------------------------------------------------------------------
# Canonicalisation helpers
# ---------------------------------------------------------------------------


def _canonical_feed_url(raw: str) -> str:
    """IDNA + lowercase host; strip trailing ``/`` on path; percent-decode.

    Two feeds whose raw strings differ only in host-case, trailing slash, or
    percent-encoding of reserved path characters produce the same canonical
    form — and therefore the same ``feed_or_adapter_id``.
    """
    parsed = urllib.parse.urlsplit(raw)
    host = parsed.hostname or ""
    try:
        host_idna = host.encode("idna").decode("ascii") if host else ""
    except UnicodeError:
        host_idna = host
    host_lower = host_idna.lower()
    if parsed.port:
        netloc = f"{host_lower}:{parsed.port}"
    else:
        netloc = host_lower
    path = urllib.parse.unquote(parsed.path or "")
    if path.endswith("/") and path != "/":
        path = path.rstrip("/")
    return urllib.parse.urlunsplit(
        (parsed.scheme.lower(), netloc, path, parsed.query, parsed.fragment)
    )


def _compute_feed_or_adapter_id(feed_url_canonical: str) -> str:
    """``"rss:" + sha3_512(canonical_bytes)[:16].hex()``. A-v3-09 closure."""
    digest = hashlib.sha3_512(feed_url_canonical.encode("utf-8")).digest()[:16]
    return f"{FEED_PREFIX_RSS}:{digest.hex()}"


# ---------------------------------------------------------------------------
# Parser-buffer drain (A-v4-01 + B-v5-04)
# ---------------------------------------------------------------------------


def _drain_parser_buffer(parser_handle: object) -> tuple[bool, str]:
    """Zero the parser's internal buffer; return ``(drained, reason_tag)``.

    Dispatch order (B-v5-04):
      1. ``hasattr(parser_handle, "raw_data")`` → set to empty ``bytearray``.
      2. ``hasattr(parser_handle, "reset")`` → call ``reset()``.
      3. neither → ``(False, "drain_api_missing")`` — caller flips feed FAILED.
    """
    if hasattr(parser_handle, "raw_data"):
        try:
            setattr(parser_handle, "raw_data", bytearray())
        except Exception:
            return (False, REASON_DRAIN_API_MISSING)
        return (True, REASON_BUFFER_DRAINED)
    if hasattr(parser_handle, "reset"):
        try:
            parser_handle.reset()  # type: ignore[attr-defined]
        except Exception:
            return (False, REASON_DRAIN_API_MISSING)
        return (True, REASON_BUFFER_DRAINED)
    return (False, REASON_DRAIN_API_MISSING)


# ---------------------------------------------------------------------------
# Candidate builder (A-v3-09 prefix assertion)
# ---------------------------------------------------------------------------


def _fetch_timestamp_iso(clock: ClockFn) -> str:
    now = clock()
    if now.tzinfo is None:
        now = now.replace(tzinfo=_dt.timezone.utc)
    return now.astimezone(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_channel_e_candidate(
    *,
    feed_or_adapter_id: str,
    entry: FeedEntry,
    feed_url_canonical: str,
    funder: str,
    funder_kind: str,
    fetch_timestamp_utc: str,
) -> Candidate:
    """Construct a Channel E ``Candidate``; assert ``rss:`` prefix (A-v3-09).

    ``candidate_id`` is ``sha3_512(feed_or_adapter_id + guid).hex()[:24]``
    so identical feed+guid pairs collapse deterministically.
    """
    assert feed_or_adapter_id.startswith(
        f"{FEED_PREFIX_RSS}:"
    ), f"Channel E feed_or_adapter_id must start with {FEED_PREFIX_RSS}:"
    url = entry.link or feed_url_canonical
    composite = f"{feed_or_adapter_id}|{entry.guid}".encode("utf-8")
    cid_hex = hashlib.sha3_512(composite).hexdigest()[:CANDIDATE_ID_HEX_LEN]
    url_hash = hashlib.sha3_512(url.encode("utf-8")).hexdigest()[:32]
    content_hash = hashlib.sha3_512(entry.body_bytes).hexdigest()[:64]
    title = entry.title or feed_url_canonical
    return Candidate(
        candidate_id=cid_hex,
        channel=CHANNEL_E,
        feed_or_adapter_id=feed_or_adapter_id,
        source_key=entry.guid,
        title=title,
        funder=funder,
        funder_kind=funder_kind,
        url=url,
        close_date_utc=None,
        award_ceiling=None,
        award_floor=None,
        applicant_types=(),
        program_page_url=None,
        fetch_timestamp_utc=fetch_timestamp_utc,
        url_hash=url_hash,
        content_hash=content_hash,
        fit_score_cached=0,
        cache_provenance=None,
    )


# ---------------------------------------------------------------------------
# Stale-feed predicate
# ---------------------------------------------------------------------------


_ISO_FORMATS: Final[tuple[str, ...]] = (
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S.%fZ",
    "%Y-%m-%d",
)


def _parse_iso(ts: str) -> Optional[_dt.datetime]:
    for fmt in _ISO_FORMATS:
        try:
            dt = _dt.datetime.strptime(ts, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=_dt.timezone.utc)
            return dt.astimezone(_dt.timezone.utc)
        except ValueError:
            continue
    try:
        return _dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(
            _dt.timezone.utc
        )
    except (ValueError, AttributeError):
        return None


def _is_feed_stale(
    *,
    now: _dt.datetime,
    entries_published: Iterable[Optional[str]],
    threshold_days: int,
) -> bool:
    """``True`` iff the feed's most recent entry is STRICTLY older than threshold.

    Blueprint §4.5 says "> 60 days" — exclusive; exactly 60 days is NOT stale.
    A feed with no parseable published timestamps is NOT flagged stale (we
    cannot prove dormancy without evidence).
    """
    most_recent: Optional[_dt.datetime] = None
    for ts in entries_published:
        if not ts:
            continue
        parsed = _parse_iso(ts)
        if parsed is None:
            continue
        if most_recent is None or parsed > most_recent:
            most_recent = parsed
    if most_recent is None:
        return False
    delta = now - most_recent
    return delta > _dt.timedelta(days=threshold_days)


# ---------------------------------------------------------------------------
# Channel-E state aggregation — §4.5 line 546
# ---------------------------------------------------------------------------


def classify_channel_e(per_feed_state: Mapping[str, str]) -> str:
    """Strictly > 50% FAILED → FAILED; any FAILED ≤ 50% → DEGRADED; else OK.

    Empty roster → FAILED (symmetric with Channels C / D — a misconfigured
    org should not silently report OK). DEGRADED feeds (stale or otherwise)
    do not tip the channel — blueprint §4.5 line 546: "OK if all feeds OK or
    DEGRADED-stale; DEGRADED if any feed FAILED".
    """
    values = list(per_feed_state.values())
    if not values:
        return HEALTH_FAILED
    failed_count = sum(1 for v in values if v == HEALTH_FAILED)
    if failed_count == 0:
        return HEALTH_OK
    if failed_count * 2 > len(values):
        return HEALTH_FAILED
    return HEALTH_DEGRADED


# ---------------------------------------------------------------------------
# Per-feed pipeline
# ---------------------------------------------------------------------------


@dataclass
class _FeedOutcome:
    feed_or_adapter_id: str
    state: str
    candidates: list[Candidate] = field(default_factory=list)
    events: list[ChannelEDegradationEvent] = field(default_factory=list)


def _escalate(current: str, incoming: str) -> str:
    priority = {HEALTH_OK: 0, HEALTH_DEGRADED: 1, HEALTH_FAILED: 2}
    if priority.get(incoming, 0) > priority.get(current, 0):
        return incoming
    return current


def _is_tls_error(exc: BaseException) -> bool:
    """Best-effort TLS-class detection without importing ``ssl`` eagerly.

    Modules that synthesise TLS errors through :class:`ConnectionError` are
    caught by the generic connection-error branch; only classes whose name
    says "SSL" land here.
    """
    name = type(exc).__name__
    if "SSL" in name:
        return True
    import ssl

    return isinstance(exc, ssl.SSLError)


def _process_one_feed(
    *,
    spec: FeedSpec,
    feed_or_adapter_id: str,
    feed_url_canonical: str,
    ctx: AdapterContext,
    feed_parser_factory: FeedParserFactory,
    clock: ClockFn,
    fetch_timestamp_utc: str,
) -> _FeedOutcome:
    """Fetch + parse one feed; return the per-feed outcome.

    Hands back the buffer-drain path (``buffer_drained`` vs
    ``drain_api_missing``) as a degradation event whose reason-tag feeds
    straight into the aggregated :class:`ChannelEDiscoverResult`.
    """
    outcome = _FeedOutcome(feed_or_adapter_id=feed_or_adapter_id, state=HEALTH_OK)

    host = urllib.parse.urlsplit(feed_url_canonical).hostname or ""

    try:
        call_result = http_request_with_retries(
            ctx,
            method="GET",
            url=feed_url_canonical,
            host=host,
            headers={"User-Agent": "Golden-Quill-Scout/0.1"},
        )
    except Exception as exc:  # pragma: no cover - http helper swallows
        if _is_tls_error(exc):
            outcome.state = HEALTH_FAILED
            outcome.events.append(
                ChannelEDegradationEvent(
                    feed_or_adapter_id=feed_or_adapter_id,
                    code=F_SCOUT_E_02,
                    reason_tag=REASON_TLS_INVALID,
                    severity=SEVERITY_HIGH,
                )
            )
            return outcome
        outcome.state = HEALTH_FAILED
        outcome.events.append(
            ChannelEDegradationEvent(
                feed_or_adapter_id=feed_or_adapter_id,
                code=F_SCOUT_E_02,
                reason_tag=REASON_SERVER_UNREACHABLE,
                severity=SEVERITY_HIGH,
            )
        )
        return outcome

    if call_result.response is None:
        err_tag = call_result.error_tag or ""
        if "SSL" in err_tag or "certificate" in err_tag.lower():
            outcome.state = HEALTH_FAILED
            outcome.events.append(
                ChannelEDegradationEvent(
                    feed_or_adapter_id=feed_or_adapter_id,
                    code=F_SCOUT_E_02,
                    reason_tag=REASON_TLS_INVALID,
                    severity=SEVERITY_HIGH,
                )
            )
            return outcome
        outcome.state = HEALTH_FAILED
        outcome.events.append(
            ChannelEDegradationEvent(
                feed_or_adapter_id=feed_or_adapter_id,
                code=F_SCOUT_E_02,
                reason_tag=REASON_SERVER_UNREACHABLE,
                severity=SEVERITY_HIGH,
            )
        )
        return outcome

    response = call_result.response
    if 400 <= response.status < 500:
        outcome.state = HEALTH_DEGRADED
        outcome.events.append(
            ChannelEDegradationEvent(
                feed_or_adapter_id=feed_or_adapter_id,
                code=F_SCOUT_E_01,
                reason_tag=REASON_HTTP_4XX,
                severity=SEVERITY_MEDIUM,
            )
        )
        return outcome
    if response.status >= 500 or call_result.outcome_tag == "retries_exhausted":
        outcome.state = HEALTH_FAILED
        outcome.events.append(
            ChannelEDegradationEvent(
                feed_or_adapter_id=feed_or_adapter_id,
                code=F_SCOUT_E_02,
                reason_tag=REASON_SERVER_UNREACHABLE,
                severity=SEVERITY_HIGH,
            )
        )
        return outcome

    parse_result = feed_parser_factory.parse_streaming(response.body_bytes)

    if parse_result.bozo:
        outcome.state = _escalate(outcome.state, HEALTH_DEGRADED)
        outcome.events.append(
            ChannelEDegradationEvent(
                feed_or_adapter_id=feed_or_adapter_id,
                code=F_SCOUT_E_01,
                reason_tag=REASON_MALFORMED_XML,
                severity=SEVERITY_MEDIUM,
            )
        )

    entries_seen = 0
    truncation_fired = False
    streaming_hint = parse_result.streaming
    published_timestamps: list[Optional[str]] = []

    try:
        while True:
            try:
                entry = next(parse_result.entries)
            except StopIteration:
                break
            entries_seen += 1
            if entries_seen > CHANNEL_E_RUNAWAY_MAX:
                break_tag = (
                    REASON_STREAMING_BREAK if streaming_hint else REASON_POST_FETCH_BREAK
                )
                outcome.events.append(
                    ChannelEDegradationEvent(
                        feed_or_adapter_id=feed_or_adapter_id,
                        code=F_SCOUT_E_03,
                        reason_tag=break_tag,
                        severity=SEVERITY_MEDIUM,
                        overflow_count=1,
                    )
                )
                outcome.state = _escalate(outcome.state, HEALTH_DEGRADED)
                truncation_fired = True
                break
            if not entry.guid:
                outcome.state = _escalate(outcome.state, HEALTH_DEGRADED)
                outcome.events.append(
                    ChannelEDegradationEvent(
                        feed_or_adapter_id=feed_or_adapter_id,
                        code=F_SCOUT_E_01,
                        reason_tag=REASON_EMPTY_GUID,
                        severity=SEVERITY_MEDIUM,
                    )
                )
                published_timestamps.append(entry.published_iso)
                continue
            published_timestamps.append(entry.published_iso)
            outcome.candidates.append(
                _build_channel_e_candidate(
                    feed_or_adapter_id=feed_or_adapter_id,
                    entry=entry,
                    feed_url_canonical=feed_url_canonical,
                    funder=spec.funder or feed_url_canonical,
                    funder_kind=spec.funder_kind or FUNDER_UNKNOWN,
                    fetch_timestamp_utc=fetch_timestamp_utc,
                )
            )
    finally:
        if entries_seen > 0:
            drained, drain_reason = _drain_parser_buffer(
                parse_result.raw_data_buffer_handle
            )
            if truncation_fired:
                outcome.events.append(
                    ChannelEDegradationEvent(
                        feed_or_adapter_id=feed_or_adapter_id,
                        code=F_SCOUT_E_03,
                        reason_tag=drain_reason,
                        severity=(
                            SEVERITY_MEDIUM if drained else SEVERITY_MEDIUM
                        ),
                    )
                )
            elif not drained:
                outcome.events.append(
                    ChannelEDegradationEvent(
                        feed_or_adapter_id=feed_or_adapter_id,
                        code=F_SCOUT_E_03,
                        reason_tag=drain_reason,
                        severity=SEVERITY_MEDIUM,
                    )
                )
            if not drained:
                outcome.state = HEALTH_FAILED

    if outcome.state != HEALTH_FAILED and _is_feed_stale(
        now=clock(),
        entries_published=published_timestamps,
        threshold_days=RSS_STALE_FEED_DEGRADED_DAYS,
    ):
        outcome.state = _escalate(outcome.state, HEALTH_DEGRADED)
        outcome.events.append(
            ChannelEDegradationEvent(
                feed_or_adapter_id=feed_or_adapter_id,
                code=F_SCOUT_E_01,
                reason_tag=REASON_FEED_STALE,
                severity=SEVERITY_LOW,
            )
        )

    return outcome


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


def discover_channel_e(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    http_client: HTTPClient,
    feed_parser_factory: FeedParserFactory,
    feed_watchlist: tuple[FeedSpec, ...],
    clock: ClockFn = _default_clock,
) -> ChannelEDiscoverResult:
    """Dispatch Channel E feed fetches across ``feed_watchlist``.

    Dedupes by canonical URL (first-occurrence-wins). Missing GUID, 4xx,
    malformed XML, stale-feed, and runaway truncation all surface as
    degradation events. Each feed passes through
    :func:`http_request_with_retries` so the Round 4 nonce / FD lifecycle
    + retry ladder apply verbatim.
    """
    ctx = AdapterContext(
        session=session,
        fd_broker=fd_broker,
        nonce_registry=nonce_registry,
        http_client=http_client,
        clock=clock,
    )

    all_candidates: list[Candidate] = []
    per_feed_state: "OrderedDict[str, str]" = OrderedDict()
    events: list[ChannelEDegradationEvent] = []

    fetch_timestamp_utc = _fetch_timestamp_iso(clock)

    seen_ids: set[str] = set()
    for spec in feed_watchlist:
        canonical = _canonical_feed_url(spec.feed_url)
        feed_id = _compute_feed_or_adapter_id(canonical)
        if feed_id in seen_ids:
            continue
        seen_ids.add(feed_id)

        outcome = _process_one_feed(
            spec=spec,
            feed_or_adapter_id=feed_id,
            feed_url_canonical=canonical,
            ctx=ctx,
            feed_parser_factory=feed_parser_factory,
            clock=clock,
            fetch_timestamp_utc=fetch_timestamp_utc,
        )

        per_feed_state[feed_id] = outcome.state
        all_candidates.extend(outcome.candidates)
        events.extend(outcome.events)

    channel_state = classify_channel_e(per_feed_state)

    return ChannelEDiscoverResult(
        candidates=tuple(all_candidates),
        per_feed_state=dict(per_feed_state),
        channel_state=channel_state,
        degradation_events=tuple(events),
    )
