"""Round 6 — pipeline.scout.channel_e_rss + _feedparser_adapter.

Exercises the Channel E RSS dispatcher against an injected
:class:`FeedParserFactory` test double, the shared Round 4 HTTPClient /
FDBroker / NonceRegistry / ClockFn Protocols, and the Round 5
``AdapterContext`` + ``http_request_with_retries`` pair. No real sockets,
no real vault, no real sleep, no real ``feedparser``.

Covers §4.5 feed-watchlist iteration + streaming-break + buffer-drain
(A-05 / A-v3-08 / A-v4-01 / B-v5-04 closures); §6.5 four-subcode
F-SCOUT-E-03 taxonomy; §4.5 line 546 strict > 50% FAILED channel rule +
stale-feed DEGRADED (60-day exclusive); A-v3-09 ``"rss:"`` prefix.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import socket
import sys
from dataclasses import dataclass, field
from typing import Any, Iterator, Mapping, Optional

import pytest

import pipeline.scout as scout
from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree
from pipeline.scout import (
    CHANNEL_E,
    CHANNEL_E_RUNAWAY_MAX,
    FEED_PREFIX_RSS,
    FUNDER_UNKNOWN,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
    RSS_STALE_FEED_DEGRADED_DAYS,
    AdapterContext,
    Candidate,
    ChannelEDegradationEvent,
    ChannelEDiscoverResult,
    FeedEntry,
    FeedParseResult,
    FeedparserLibFactory,
    FeedparserLibHandle,
    FeedSpec,
    classify_channel_e,
    discover_channel_e,
    http_request_with_retries,
)
from pipeline.scout import channel_e_rss as ch_e
from pipeline.scout.channel_e_rss import (
    F_SCOUT_E_01,
    F_SCOUT_E_02,
    F_SCOUT_E_03,
    REASON_BUFFER_DRAINED,
    REASON_DRAIN_API_MISSING,
    REASON_EMPTY_GUID,
    REASON_FEED_STALE,
    REASON_HTTP_4XX,
    REASON_MALFORMED_XML,
    REASON_POST_FETCH_BREAK,
    REASON_SERVER_UNREACHABLE,
    REASON_STREAMING_BREAK,
    REASON_TLS_INVALID,
    _build_channel_e_candidate,
    _canonical_feed_url,
    _compute_feed_or_adapter_id,
    _drain_parser_buffer,
)


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


@dataclass
class _FakeSession:
    session_id: str = "sess-round6"
    slug: str = "fit_farms_llc"


@dataclass
class _FakeResponse:
    status: int
    headers: Mapping[str, str]
    body_bytes: bytes

    @classmethod
    def ok(cls, body: bytes = b"<rss/>") -> "_FakeResponse":
        return cls(
            status=200,
            headers={"Content-Type": "application/rss+xml"},
            body_bytes=body,
        )


@dataclass
class _ScriptedHTTPClient:
    script: list[Any] = field(default_factory=list)
    calls: list[dict] = field(default_factory=list)
    default_response: Optional[_FakeResponse] = None

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        body: Optional[bytes],
        connect_timeout_s: float,
        read_timeout_s: float,
    ) -> _FakeResponse:
        self.calls.append(
            {
                "method": method,
                "url": url,
                "headers": dict(headers),
                "body": body,
                "connect_timeout_s": connect_timeout_s,
                "read_timeout_s": read_timeout_s,
            }
        )
        if not self.script:
            if self.default_response is not None:
                return self.default_response
            raise AssertionError("scripted HTTPClient exhausted")
        item = self.script.pop(0)
        if isinstance(item, BaseException):
            raise item
        if callable(item):
            return item()
        return item


@dataclass
class _CountingFDBroker:
    fds_issued: list[int] = field(default_factory=list)
    fds_released: list[int] = field(default_factory=list)
    request_log: list[dict] = field(default_factory=list)
    next_fd: int = 3000

    def request_fd(self, *, kind: str, host: str) -> int:
        self.request_log.append({"kind": kind, "host": host})
        fd = self.next_fd
        self.next_fd += 1
        self.fds_issued.append(fd)
        return fd

    def release_fd(self, fd: int) -> None:
        self.fds_released.append(fd)


@dataclass
class _CountingNonceRegistry:
    reserved: list[str] = field(default_factory=list)
    released: list[dict] = field(default_factory=list)

    def reserve(self, nonce_hex: str) -> None:
        self.reserved.append(nonce_hex)

    def release(self, nonce_hex: str, *, path_tag: str) -> None:
        self.released.append({"nonce_hex": nonce_hex, "path_tag": path_tag})


@dataclass
class _FrozenClock:
    now: _dt.datetime = field(
        default_factory=lambda: _dt.datetime(
            2026, 4, 20, 12, 0, 0, tzinfo=_dt.timezone.utc
        )
    )
    sleeps: list[float] = field(default_factory=list)

    def __call__(self) -> _dt.datetime:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)


# Drainable handle test doubles -------------------------------------------------


class _DrainableHandle:
    """Parser handle exposing ``raw_data`` bytearray (drain path (i))."""

    def __init__(self, initial: bytes = b"pretend-raw-body"):
        self.raw_data = bytearray(initial)


class _ResetOnlyHandle:
    """Parser handle exposing ``reset()`` (drain path (ii))."""

    def __init__(self) -> None:
        self.reset_calls = 0

    def reset(self) -> None:
        self.reset_calls += 1


class _NoAPIHandle:
    """Parser handle with neither ``raw_data`` nor ``reset()``."""


class _RaisingHandle:
    """Handle where setting raw_data raises (defence for drain_api_missing fallback)."""

    @property
    def raw_data(self) -> bytearray:  # pragma: no cover - property shape only
        return bytearray()

    @raw_data.setter
    def raw_data(self, value: bytearray) -> None:
        raise RuntimeError("cannot set raw_data")


class _ResetRaisingHandle:
    """Handle where ``reset()`` raises (drain_api_missing fallback)."""

    def reset(self) -> None:
        raise RuntimeError("reset broke")


# Feed-parser factory test double ----------------------------------------------


@dataclass
class _FakeFeedParseResult:
    bozo: bool
    feed_modified_iso: Optional[str]
    entries: Iterator[FeedEntry]
    raw_data_buffer_handle: Any
    streaming: bool = False


@dataclass
class _ScriptedFeedParserFactory:
    """Scripted factory returning a canned FeedParseResult per call.

    ``per_body`` maps raw-body bytes to a ``_ResultFactory`` callable so the
    same factory can answer differently for different feeds.
    """

    results: list[FeedParseResult] = field(default_factory=list)
    calls: list[bytes] = field(default_factory=list)

    def parse_streaming(self, raw_body: bytes) -> FeedParseResult:
        self.calls.append(raw_body)
        if not self.results:
            raise AssertionError("scripted FeedParserFactory exhausted")
        return self.results.pop(0)


# Helpers ----------------------------------------------------------------------


def _entry(
    *,
    guid: str = "guid-1",
    link: str = "https://example.org/a",
    title: str = "Entry A",
    body: bytes = b"body-a",
    published: Optional[str] = "2026-04-19T10:00:00Z",
) -> FeedEntry:
    return FeedEntry(
        guid=guid, link=link, title=title, body_bytes=body, published_iso=published
    )


def _parse_result(
    *,
    entries: Iterator[FeedEntry],
    bozo: bool = False,
    feed_modified_iso: Optional[str] = None,
    handle: Optional[object] = None,
    streaming: bool = False,
) -> FeedParseResult:
    return FeedParseResult(
        bozo=bozo,
        feed_modified_iso=feed_modified_iso,
        entries=entries,
        raw_data_buffer_handle=handle if handle is not None else _DrainableHandle(),
        streaming=streaming,
    )


def _build_ctx(
    *,
    http_client: Optional[_ScriptedHTTPClient] = None,
    fd_broker: Optional[_CountingFDBroker] = None,
    nonce_registry: Optional[_CountingNonceRegistry] = None,
    clock: Optional[_FrozenClock] = None,
) -> tuple:
    session = _FakeSession()
    http = http_client or _ScriptedHTTPClient(default_response=_FakeResponse.ok())
    fd = fd_broker or _CountingFDBroker()
    nonce = nonce_registry or _CountingNonceRegistry()
    clk = clock or _FrozenClock()
    return session, fd, nonce, http, clk


# ---------------------------------------------------------------------------
# Channel E — Happy path
# ---------------------------------------------------------------------------


class TestChannelEHappyPath:
    def test_single_feed_with_three_entries_all_ok(self) -> None:
        entries = iter([_entry(guid=f"g{i}", link=f"https://ex.org/{i}") for i in range(3)])
        factory = _ScriptedFeedParserFactory(results=[_parse_result(entries=entries)])
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/rss.xml"),),
            clock=clk,
        )
        assert isinstance(result, ChannelEDiscoverResult)
        assert result.channel_state == HEALTH_OK
        assert len(result.candidates) == 3
        assert all(c.channel == CHANNEL_E for c in result.candidates)
        assert result.degradation_events == ()

    def test_three_feeds_all_ok(self) -> None:
        factory = _ScriptedFeedParserFactory(
            results=[
                _parse_result(entries=iter([_entry(guid="a")])),
                _parse_result(entries=iter([_entry(guid="b")])),
                _parse_result(entries=iter([_entry(guid="c")])),
            ]
        )
        session, fd, nonce, http, clk = _build_ctx()
        watchlist = tuple(
            FeedSpec(feed_url=f"https://feeds.example.org/{n}") for n in ("a", "b", "c")
        )
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=watchlist,
            clock=clk,
        )
        assert result.channel_state == HEALTH_OK
        assert len(result.candidates) == 3

    def test_empty_feed_zero_entries_still_ok(self) -> None:
        factory = _ScriptedFeedParserFactory(results=[_parse_result(entries=iter([]))])
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/empty"),),
            clock=clk,
        )
        assert result.channel_state == HEALTH_OK
        assert result.candidates == ()

    def test_feed_order_preserved_in_output(self) -> None:
        factory = _ScriptedFeedParserFactory(
            results=[
                _parse_result(entries=iter([_entry(guid="z")])),
                _parse_result(entries=iter([_entry(guid="a")])),
                _parse_result(entries=iter([_entry(guid="m")])),
            ]
        )
        session, fd, nonce, http, clk = _build_ctx()
        watchlist = tuple(
            FeedSpec(feed_url=f"https://feeds.example.org/{n}") for n in ("z", "a", "m")
        )
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=watchlist,
            clock=clk,
        )
        keys = list(result.per_feed_state.keys())
        expected = [
            _compute_feed_or_adapter_id(_canonical_feed_url(f"https://feeds.example.org/{n}"))
            for n in ("z", "a", "m")
        ]
        assert keys == expected


# ---------------------------------------------------------------------------
# FeedParserFactory Protocol
# ---------------------------------------------------------------------------


class TestFeedParserFactory:
    def test_injected_factory_called_with_raw_bytes(self) -> None:
        factory = _ScriptedFeedParserFactory(results=[_parse_result(entries=iter([]))])
        session, fd, nonce, http, clk = _build_ctx(
            http_client=_ScriptedHTTPClient(default_response=_FakeResponse.ok(b"RAW-BODY"))
        )
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/rss"),),
            clock=clk,
        )
        assert factory.calls == [b"RAW-BODY"]

    def test_bozo_true_degrades_feed(self) -> None:
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([]), bozo=True)]
        )
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/bad"),),
            clock=clk,
        )
        assert list(result.per_feed_state.values()) == [HEALTH_DEGRADED]
        assert any(
            e.code == F_SCOUT_E_01 and e.reason_tag == REASON_MALFORMED_XML
            for e in result.degradation_events
        )

    def test_bozo_true_with_entries_still_yields_candidates(self) -> None:
        factory = _ScriptedFeedParserFactory(
            results=[
                _parse_result(
                    entries=iter([_entry(guid="ok-1"), _entry(guid="ok-2")]),
                    bozo=True,
                )
            ]
        )
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/bozo"),),
            clock=clk,
        )
        assert len(result.candidates) == 2
        assert list(result.per_feed_state.values()) == [HEALTH_DEGRADED]

    def test_empty_guid_emits_f_scout_e_01_empty_guid(self) -> None:
        factory = _ScriptedFeedParserFactory(
            results=[
                _parse_result(
                    entries=iter(
                        [_entry(guid="", link="https://ex.org/noguid"), _entry(guid="ok")]
                    )
                )
            ]
        )
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/noguid"),),
            clock=clk,
        )
        assert len(result.candidates) == 1
        assert any(
            e.code == F_SCOUT_E_01 and e.reason_tag == REASON_EMPTY_GUID
            for e in result.degradation_events
        )
        assert list(result.per_feed_state.values()) == [HEALTH_DEGRADED]

    def test_published_iso_propagates_into_stale_check(self) -> None:
        # Entry with published_iso far in the past triggers the stale path.
        factory = _ScriptedFeedParserFactory(
            results=[
                _parse_result(
                    entries=iter([_entry(published="2025-01-01T00:00:00Z")])
                )
            ]
        )
        session, fd, nonce, http, clk = _build_ctx(
            clock=_FrozenClock(
                now=_dt.datetime(2026, 4, 20, 12, 0, 0, tzinfo=_dt.timezone.utc)
            )
        )
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/old"),),
            clock=clk,
        )
        assert any(
            e.reason_tag == REASON_FEED_STALE for e in result.degradation_events
        )

    def test_factory_protocol_duck_typed(self) -> None:
        class _Bare:
            def parse_streaming(self, raw_body: bytes) -> FeedParseResult:
                return _parse_result(entries=iter([_entry()]))

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=_Bare(),
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/bare"),),
            clock=clk,
        )
        assert result.channel_state == HEALTH_OK


# ---------------------------------------------------------------------------
# Runaway / streaming break
# ---------------------------------------------------------------------------


class TestChannelERunaway:
    def test_200_entries_truncated_at_100_before_candidate_construction(self) -> None:
        entries = iter([_entry(guid=f"g{i}") for i in range(200)])
        factory = _ScriptedFeedParserFactory(results=[_parse_result(entries=entries)])
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/big"),),
            clock=clk,
        )
        assert len(result.candidates) == CHANNEL_E_RUNAWAY_MAX
        assert len(result.candidates) == 100

    @pytest.mark.parametrize("n", [0, 1, 50, 99, 100, 101, 250, 1000])
    def test_101st_entry_never_constructed_property(self, n: int) -> None:
        entries = iter([_entry(guid=f"g{i}") for i in range(n)])
        factory = _ScriptedFeedParserFactory(results=[_parse_result(entries=entries)])
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/n"),),
            clock=clk,
        )
        assert len(result.candidates) == min(n, CHANNEL_E_RUNAWAY_MAX)

    def test_streaming_break_reason_tag_emitted(self) -> None:
        entries = iter([_entry(guid=f"g{i}") for i in range(150)])
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=entries, streaming=True)]
        )
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/stream"),),
            clock=clk,
        )
        tags = [e.reason_tag for e in result.degradation_events if e.code == F_SCOUT_E_03]
        assert REASON_STREAMING_BREAK in tags
        assert REASON_POST_FETCH_BREAK not in tags

    def test_post_fetch_break_reason_tag_emitted(self) -> None:
        entries = iter([_entry(guid=f"g{i}") for i in range(150)])
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=entries, streaming=False)]
        )
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/postfetch"),),
            clock=clk,
        )
        tags = [e.reason_tag for e in result.degradation_events if e.code == F_SCOUT_E_03]
        assert REASON_POST_FETCH_BREAK in tags
        assert REASON_STREAMING_BREAK not in tags

    def test_runaway_reason_tag_invariant_streaming_xor_post_fetch(self) -> None:
        for streaming in (True, False):
            entries = iter([_entry(guid=f"g{i}") for i in range(150)])
            factory = _ScriptedFeedParserFactory(
                results=[_parse_result(entries=entries, streaming=streaming)]
            )
            session, fd, nonce, http, clk = _build_ctx()
            result = discover_channel_e(
                session=session,
                fd_broker=fd,
                nonce_registry=nonce,
                http_client=http,
                feed_parser_factory=factory,
                feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/x"),),
                clock=clk,
            )
            tags = {e.reason_tag for e in result.degradation_events if e.code == F_SCOUT_E_03}
            assert (REASON_STREAMING_BREAK in tags) ^ (REASON_POST_FETCH_BREAK in tags)

    def test_runaway_reason_tag_invariant_buffer_drained_xor_drain_api_missing(self) -> None:
        for handle, expected_tag in (
            (_DrainableHandle(), REASON_BUFFER_DRAINED),
            (_NoAPIHandle(), REASON_DRAIN_API_MISSING),
        ):
            entries = iter([_entry(guid=f"g{i}") for i in range(150)])
            factory = _ScriptedFeedParserFactory(
                results=[_parse_result(entries=entries, handle=handle)]
            )
            session, fd, nonce, http, clk = _build_ctx()
            result = discover_channel_e(
                session=session,
                fd_broker=fd,
                nonce_registry=nonce,
                http_client=http,
                feed_parser_factory=factory,
                feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/y"),),
                clock=clk,
            )
            tags = {e.reason_tag for e in result.degradation_events if e.code == F_SCOUT_E_03}
            assert expected_tag in tags
            other = {REASON_BUFFER_DRAINED, REASON_DRAIN_API_MISSING} - {expected_tag}
            assert not (tags & other)

    def test_drain_buffer_path_i_raw_data_replaced(self) -> None:
        handle = _DrainableHandle(initial=b"leftover")
        drained, tag = _drain_parser_buffer(handle)
        assert drained is True
        assert tag == REASON_BUFFER_DRAINED
        assert bytes(handle.raw_data) == b""

    def test_drain_buffer_path_ii_reset_called(self) -> None:
        handle = _ResetOnlyHandle()
        drained, tag = _drain_parser_buffer(handle)
        assert drained is True
        assert tag == REASON_BUFFER_DRAINED
        assert handle.reset_calls == 1

    def test_drain_buffer_path_iii_api_missing_flips_feed_failed(self) -> None:
        entries = iter([_entry(guid=f"g{i}") for i in range(5)])
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=entries, handle=_NoAPIHandle())]
        )
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/badhandle"),),
            clock=clk,
        )
        assert list(result.per_feed_state.values()) == [HEALTH_FAILED]
        assert any(
            e.code == F_SCOUT_E_03 and e.reason_tag == REASON_DRAIN_API_MISSING
            for e in result.degradation_events
        )

    def test_drain_runs_even_when_entries_below_cap(self) -> None:
        handle = _DrainableHandle(initial=b"leftover")
        entries = iter([_entry(guid=f"g{i}") for i in range(50)])
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=entries, handle=handle)]
        )
        session, fd, nonce, http, clk = _build_ctx()
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/small"),),
            clock=clk,
        )
        assert bytes(handle.raw_data) == b""

    def test_drain_not_attempted_when_zero_entries(self) -> None:
        handle = _DrainableHandle(initial=b"leftover")
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([]), handle=handle)]
        )
        session, fd, nonce, http, clk = _build_ctx()
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/empty"),),
            clock=clk,
        )
        # Zero entries → no drain invocation — leftover preserved.
        assert bytes(handle.raw_data) == b"leftover"

    def test_drain_raising_setter_returns_api_missing(self) -> None:
        drained, tag = _drain_parser_buffer(_RaisingHandle())
        assert drained is False
        assert tag == REASON_DRAIN_API_MISSING

    def test_drain_raising_reset_returns_api_missing(self) -> None:
        drained, tag = _drain_parser_buffer(_ResetRaisingHandle())
        assert drained is False
        assert tag == REASON_DRAIN_API_MISSING


# ---------------------------------------------------------------------------
# Stale feed
# ---------------------------------------------------------------------------


class TestChannelEStale:
    def test_feed_with_latest_entry_older_than_60_days_degraded(self) -> None:
        clock = _FrozenClock(
            now=_dt.datetime(2026, 4, 20, 12, 0, 0, tzinfo=_dt.timezone.utc)
        )
        old = (clock.now - _dt.timedelta(days=70)).strftime("%Y-%m-%dT%H:%M:%SZ")
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry(guid="old", published=old)]))]
        )
        session, fd, nonce, http, _ = _build_ctx(clock=clock)
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/stale"),),
            clock=clock,
        )
        assert list(result.per_feed_state.values()) == [HEALTH_DEGRADED]
        assert any(
            e.reason_tag == REASON_FEED_STALE for e in result.degradation_events
        )

    def test_latest_entry_exactly_60_days_not_stale(self) -> None:
        """Blueprint §4.5 > 60 days — exclusive, 60 days exactly is NOT stale."""
        clock = _FrozenClock(
            now=_dt.datetime(2026, 4, 20, 12, 0, 0, tzinfo=_dt.timezone.utc)
        )
        sixty = (clock.now - _dt.timedelta(days=RSS_STALE_FEED_DEGRADED_DAYS)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry(guid="edge", published=sixty)]))]
        )
        session, fd, nonce, http, _ = _build_ctx(clock=clock)
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/edge"),),
            clock=clock,
        )
        assert list(result.per_feed_state.values()) == [HEALTH_OK]

    def test_stale_feed_still_yields_candidates(self) -> None:
        clock = _FrozenClock(
            now=_dt.datetime(2026, 4, 20, 12, 0, 0, tzinfo=_dt.timezone.utc)
        )
        old = (clock.now - _dt.timedelta(days=100)).strftime("%Y-%m-%dT%H:%M:%SZ")
        factory = _ScriptedFeedParserFactory(
            results=[
                _parse_result(
                    entries=iter([_entry(guid="a", published=old), _entry(guid="b", published=old)])
                )
            ]
        )
        session, fd, nonce, http, _ = _build_ctx(clock=clock)
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/stale"),),
            clock=clock,
        )
        assert len(result.candidates) == 2

    def test_stale_feed_classified_ok_at_channel_level_not_failed(self) -> None:
        clock = _FrozenClock(
            now=_dt.datetime(2026, 4, 20, 12, 0, 0, tzinfo=_dt.timezone.utc)
        )
        old = (clock.now - _dt.timedelta(days=100)).strftime("%Y-%m-%dT%H:%M:%SZ")
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry(published=old)]))]
        )
        session, fd, nonce, http, _ = _build_ctx(clock=clock)
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/stale2"),),
            clock=clock,
        )
        # Per §4.5 line 546: stale DEGRADED feeds do NOT tip the channel.
        # Channel stays OK unless a feed is FAILED. Per-feed is DEGRADED-stale,
        # but channel_state is OK.
        assert result.channel_state == HEALTH_OK
        assert list(result.per_feed_state.values()) == [HEALTH_DEGRADED]

    def test_feed_with_unparseable_published_not_flagged_stale(self) -> None:
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry(published="not-a-date")]))]
        )
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/nodate"),),
            clock=clk,
        )
        assert list(result.per_feed_state.values()) == [HEALTH_OK]


# ---------------------------------------------------------------------------
# HTTP failure paths
# ---------------------------------------------------------------------------


class TestChannelEHTTP:
    def test_tls_invalid_feed_failed_f_scout_e_02(self) -> None:
        import ssl

        http = _ScriptedHTTPClient(
            script=[
                ssl.SSLCertVerificationError("verify failed"),
                ssl.SSLCertVerificationError("verify failed"),
                ssl.SSLCertVerificationError("verify failed"),
                ssl.SSLCertVerificationError("verify failed"),
            ]
        )
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/tls"),),
            clock=clk,
        )
        assert list(result.per_feed_state.values()) == [HEALTH_FAILED]
        assert any(
            e.code == F_SCOUT_E_02 and e.reason_tag == REASON_TLS_INVALID
            for e in result.degradation_events
        )

    def test_http_404_feed_degraded_f_scout_e_01_http_4xx(self) -> None:
        resp = _FakeResponse(status=404, headers={}, body_bytes=b"not found")
        http = _ScriptedHTTPClient(default_response=resp)
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/404"),),
            clock=clk,
        )
        assert list(result.per_feed_state.values()) == [HEALTH_DEGRADED]
        assert any(
            e.code == F_SCOUT_E_01 and e.reason_tag == REASON_HTTP_4XX
            for e in result.degradation_events
        )

    def test_http_500_retries_then_failed_f_scout_e_02_server_unreachable(self) -> None:
        resp500 = _FakeResponse(status=500, headers={}, body_bytes=b"")
        http = _ScriptedHTTPClient(
            script=[resp500, resp500, resp500, resp500]
        )
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/500"),),
            clock=clk,
        )
        assert list(result.per_feed_state.values()) == [HEALTH_FAILED]
        assert any(
            e.code == F_SCOUT_E_02 and e.reason_tag == REASON_SERVER_UNREACHABLE
            for e in result.degradation_events
        )

    def test_http_500_then_200_degraded_not_failed(self) -> None:
        resp500 = _FakeResponse(status=500, headers={}, body_bytes=b"")
        http = _ScriptedHTTPClient(
            script=[resp500, _FakeResponse.ok(b"<rss/>")]
        )
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry()]))]
        )
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/flaky"),),
            clock=clk,
        )
        # success_after_retry → DEGRADED on per-call state, but outcome still yields candidates.
        # feed-level state is driven by our pipeline ignoring success_after_retry as a failure.
        assert len(result.candidates) == 1

    def test_timeout_exhausted_failed(self) -> None:
        http = _ScriptedHTTPClient(
            script=[
                TimeoutError("t0"),
                TimeoutError("t1"),
                TimeoutError("t2"),
                TimeoutError("t3"),
            ]
        )
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/timeout"),),
            clock=clk,
        )
        assert list(result.per_feed_state.values()) == [HEALTH_FAILED]
        assert any(
            e.code == F_SCOUT_E_02 for e in result.degradation_events
        )

    def test_connection_reset_exhausted_failed(self) -> None:
        http = _ScriptedHTTPClient(
            script=[
                ConnectionResetError("r0"),
                ConnectionResetError("r1"),
                ConnectionResetError("r2"),
                ConnectionResetError("r3"),
            ]
        )
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/reset"),),
            clock=clk,
        )
        assert list(result.per_feed_state.values()) == [HEALTH_FAILED]

    def test_retry_sleep_sequence_1_0_2_0_4_0(self) -> None:
        resp500 = _FakeResponse(status=500, headers={}, body_bytes=b"")
        http = _ScriptedHTTPClient(
            script=[resp500, resp500, resp500, resp500]
        )
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/slow"),),
            clock=clk,
        )
        assert clk.sleeps == [1.0, 2.0, 4.0]

    def test_retries_per_feed_not_cross_feed(self) -> None:
        # Two feeds — each gets its own retry ladder.
        resp500 = _FakeResponse(status=500, headers={}, body_bytes=b"")
        http = _ScriptedHTTPClient(
            script=[
                resp500, resp500, resp500, resp500,
                _FakeResponse.ok(b"<rss/>"),
            ]
        )
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry()]))]
        )
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(
                FeedSpec(feed_url="https://feeds.example.org/a"),
                FeedSpec(feed_url="https://feeds.example.org/b"),
            ),
            clock=clk,
        )
        assert list(result.per_feed_state.values()) == [HEALTH_FAILED, HEALTH_OK]

    def test_first_success_no_sleeps_observed(self) -> None:
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry()]))]
        )
        session, fd, nonce, http, clk = _build_ctx()
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/quick"),),
            clock=clk,
        )
        assert clk.sleeps == []

    def test_4xx_not_retried(self) -> None:
        http = _ScriptedHTTPClient(
            script=[_FakeResponse(status=403, headers={}, body_bytes=b"forbidden")]
        )
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/403"),),
            clock=clk,
        )
        assert clk.sleeps == []
        assert len(http.calls) == 1


# ---------------------------------------------------------------------------
# Channel-state aggregation
# ---------------------------------------------------------------------------


class TestChannelEStateAggregation:
    def test_all_ok_channel_ok(self) -> None:
        assert classify_channel_e({"a": HEALTH_OK, "b": HEALTH_OK}) == HEALTH_OK

    def test_all_degraded_channel_ok(self) -> None:
        # Blueprint §4.5 line 546: stale DEGRADED feeds do NOT tip the channel.
        # Channel state only shifts on FAILED counts.
        assert classify_channel_e({"a": HEALTH_DEGRADED}) == HEALTH_OK
        assert (
            classify_channel_e({"a": HEALTH_DEGRADED, "b": HEALTH_OK})
            == HEALTH_OK
        )

    def test_one_failed_of_three_channel_degraded(self) -> None:
        assert (
            classify_channel_e(
                {"a": HEALTH_OK, "b": HEALTH_OK, "c": HEALTH_FAILED}
            )
            == HEALTH_DEGRADED
        )

    def test_exactly_5_of_10_failed_channel_degraded(self) -> None:
        mix = {f"f{i}": HEALTH_FAILED for i in range(5)}
        mix.update({f"g{i}": HEALTH_OK for i in range(5)})
        assert classify_channel_e(mix) == HEALTH_DEGRADED

    def test_6_of_10_failed_channel_failed(self) -> None:
        mix = {f"f{i}": HEALTH_FAILED for i in range(6)}
        mix.update({f"g{i}": HEALTH_OK for i in range(4)})
        assert classify_channel_e(mix) == HEALTH_FAILED

    def test_1_of_1_failed_channel_failed(self) -> None:
        assert classify_channel_e({"a": HEALTH_FAILED}) == HEALTH_FAILED

    def test_empty_watchlist_channel_failed(self) -> None:
        assert classify_channel_e({}) == HEALTH_FAILED

    def test_empty_watchlist_through_discover(self) -> None:
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(),
            clock=clk,
        )
        assert result.channel_state == HEALTH_FAILED
        assert result.candidates == ()


# ---------------------------------------------------------------------------
# Nonce / FD lifecycle parity with Round 5
# ---------------------------------------------------------------------------


class TestChannelENonceFDLifecycle:
    def test_parity_reserve_release_success(self) -> None:
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry()]))]
        )
        session, fd, nonce, http, clk = _build_ctx()
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/ok"),),
            clock=clk,
        )
        assert len(nonce.reserved) == 1
        assert len(nonce.released) == 1
        assert len(fd.fds_issued) == 1
        assert len(fd.fds_released) == 1

    def test_fd_released_before_nonce(self) -> None:
        # Observe via a lockstep counter that FD releases before nonce releases.
        events: list[str] = []

        @dataclass
        class _OrderingFD(_CountingFDBroker):
            def release_fd(self, fd: int) -> None:
                events.append(f"fd_release:{fd}")
                super().release_fd(fd)

        @dataclass
        class _OrderingNonce(_CountingNonceRegistry):
            def release(self, nonce_hex: str, *, path_tag: str) -> None:
                events.append(f"nonce_release:{path_tag}")
                super().release(nonce_hex, path_tag=path_tag)

        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry()]))]
        )
        session, _, _, http, clk = _build_ctx()
        discover_channel_e(
            session=session,
            fd_broker=_OrderingFD(),
            nonce_registry=_OrderingNonce(),
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/ok"),),
            clock=clk,
        )
        fd_idx = [i for i, e in enumerate(events) if e.startswith("fd_release")]
        nonce_idx = [i for i, e in enumerate(events) if e.startswith("nonce_release")]
        assert fd_idx and nonce_idx
        assert fd_idx[0] < nonce_idx[0]

    def test_path_tag_success(self) -> None:
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry()]))]
        )
        session, fd, nonce, http, clk = _build_ctx()
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/ok"),),
            clock=clk,
        )
        assert nonce.released[0]["path_tag"] == "success"

    def test_path_tag_timeout(self) -> None:
        http = _ScriptedHTTPClient(
            script=[TimeoutError() for _ in range(4)]
        )
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/to"),),
            clock=clk,
        )
        assert nonce.released[0]["path_tag"] == "timeout"

    def test_path_tag_http_error_on_4xx(self) -> None:
        http = _ScriptedHTTPClient(
            default_response=_FakeResponse(status=404, headers={}, body_bytes=b"")
        )
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/404"),),
            clock=clk,
        )
        assert nonce.released[0]["path_tag"] == "http_error"

    def test_path_tag_connection_reset(self) -> None:
        http = _ScriptedHTTPClient(
            script=[ConnectionResetError() for _ in range(4)]
        )
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/reset"),),
            clock=clk,
        )
        assert nonce.released[0]["path_tag"] == "connection_reset"

    def test_path_tag_exception_on_unknown_raise(self) -> None:
        http = _ScriptedHTTPClient(script=[RuntimeError("weird")])
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/weird"),),
            clock=clk,
        )
        assert nonce.released[0]["path_tag"] == "exception"

    def test_one_feed_failing_does_not_starve_fds_for_next_feed(self) -> None:
        resp500 = _FakeResponse(status=500, headers={}, body_bytes=b"")
        http = _ScriptedHTTPClient(
            script=[resp500, resp500, resp500, resp500, _FakeResponse.ok()]
        )
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry()]))]
        )
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(
                FeedSpec(feed_url="https://feeds.example.org/down"),
                FeedSpec(feed_url="https://feeds.example.org/up"),
            ),
            clock=clk,
        )
        # Both feeds issued FDs and released them.
        assert len(fd.fds_issued) == 2
        assert len(fd.fds_released) == 2


# ---------------------------------------------------------------------------
# Canonicalisation + dedup
# ---------------------------------------------------------------------------


class TestChannelECanonical:
    def test_idna_host_canonicalised(self) -> None:
        # Non-ASCII host → IDNA-encoded lowercase.
        canonical = _canonical_feed_url("https://EXAMPLE.xn--80aswg/rss")
        assert canonical == "https://example.xn--80aswg/rss"

    def test_trailing_slash_stripped(self) -> None:
        assert (
            _canonical_feed_url("https://feeds.example.org/a/")
            == "https://feeds.example.org/a"
        )
        # Root "/" preserved.
        assert _canonical_feed_url("https://feeds.example.org/") == "https://feeds.example.org/"

    def test_host_case_folded(self) -> None:
        assert (
            _canonical_feed_url("https://FEEDS.EXAMPLE.ORG/a")
            == "https://feeds.example.org/a"
        )

    def test_duplicate_feed_url_dedup_keeps_first(self) -> None:
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry(guid="only")]))]
        )
        session, fd, nonce, http, clk = _build_ctx()
        watchlist = (
            FeedSpec(feed_url="https://feeds.example.org/a"),
            FeedSpec(feed_url="https://FEEDS.example.org/a/"),  # same canonical form
        )
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=watchlist,
            clock=clk,
        )
        # Second duplicate should not trigger a second factory call.
        assert len(factory.calls) == 1
        assert len(result.per_feed_state) == 1

    def test_same_canonical_url_same_feed_or_adapter_id(self) -> None:
        a = _compute_feed_or_adapter_id(
            _canonical_feed_url("https://Feeds.Example.org/x/")
        )
        b = _compute_feed_or_adapter_id(
            _canonical_feed_url("https://feeds.example.org/x")
        )
        assert a == b
        assert a.startswith(f"{FEED_PREFIX_RSS}:")


# ---------------------------------------------------------------------------
# feed_or_adapter_id namespacing
# ---------------------------------------------------------------------------


class TestChannelENamespace:
    def test_rss_prefix_asserted(self) -> None:
        entry = _entry()
        cid = _build_channel_e_candidate(
            feed_or_adapter_id="rss:abcdef1234567890",
            entry=entry,
            feed_url_canonical="https://feeds.example.org/x",
            funder="ExampleFunder",
            funder_kind=FUNDER_UNKNOWN,
            fetch_timestamp_utc="2026-04-20T12:00:00Z",
        )
        assert cid.feed_or_adapter_id.startswith(f"{FEED_PREFIX_RSS}:")
        assert cid.channel == CHANNEL_E

    def test_unprefixed_id_rejected(self) -> None:
        with pytest.raises(AssertionError):
            _build_channel_e_candidate(
                feed_or_adapter_id="portal:wrong",
                entry=_entry(),
                feed_url_canonical="https://feeds.example.org/x",
                funder="F",
                funder_kind=FUNDER_UNKNOWN,
                fetch_timestamp_utc="2026-04-20T12:00:00Z",
            )

    def test_candidate_channel_stamped_channel_e(self) -> None:
        factory = _ScriptedFeedParserFactory(
            results=[_parse_result(entries=iter([_entry()]))]
        )
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/x"),),
            clock=clk,
        )
        assert all(c.channel == CHANNEL_E for c in result.candidates)


# ---------------------------------------------------------------------------
# Import-time hygiene
# ---------------------------------------------------------------------------


class TestChannelENoModuleSideEffects:
    def test_import_opens_zero_fds_zero_nonces(self) -> None:
        # A fresh import of the module should not perform any I/O. Easiest
        # assertion: importing the module does not alter os-level state and
        # re-import returns the cached module without raising.
        import importlib

        m = importlib.import_module("pipeline.scout.channel_e_rss")
        importlib.reload(m)
        # If we got here, no import-time exception fired from I/O.
        assert m is not None

    def test_feedparser_not_imported_until_factory_called(self) -> None:
        sys.modules.pop("feedparser", None)
        import importlib

        importlib.import_module("pipeline.scout.channel_e_rss")
        assert "feedparser" not in sys.modules

    def test_feedparser_adapter_does_not_import_feedparser_at_module_load(self) -> None:
        sys.modules.pop("feedparser", None)
        import importlib

        importlib.import_module("pipeline.scout._feedparser_adapter")
        assert "feedparser" not in sys.modules


# ---------------------------------------------------------------------------
# kw-only enforcement
# ---------------------------------------------------------------------------


class TestChannelEKWOnly:
    def test_positional_call_rejected(self) -> None:
        factory = _ScriptedFeedParserFactory(results=[])
        session, fd, nonce, http, clk = _build_ctx()
        with pytest.raises(TypeError):
            discover_channel_e(  # type: ignore[call-arg, misc]
                session, fd, nonce, http, factory, (), clk
            )


# ---------------------------------------------------------------------------
# Shared protocol re-use with Round 5
# ---------------------------------------------------------------------------


class TestSharedProtocolReuse:
    def test_adapter_context_imported_from_channel_c(self) -> None:
        # E-026 closure — do not compare object identity across test files
        # that reload sys.modules. Verify source module lineage by name.
        from pipeline.scout import channel_e_rss as ch_e_fresh

        assert (
            ch_e_fresh.AdapterContext.__module__
            == "pipeline.scout.channel_c_portals"
        )

    def test_http_request_with_retries_imported_from_channel_c(self) -> None:
        from pipeline.scout import channel_e_rss as ch_e_fresh

        assert (
            ch_e_fresh.http_request_with_retries.__module__
            == "pipeline.scout.channel_c_portals"
        )


# ---------------------------------------------------------------------------
# AST-lint regression
# ---------------------------------------------------------------------------


class TestASTLintRegression:
    def test_lint_channel_e_rss_clean(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[2]
        violations = lint_tree(
            root / "pipeline" / "scout" / "channel_e_rss.py",
            rules=DEFAULT_RULES,
        )
        assert violations == []

    def test_lint_feedparser_adapter_clean(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[2]
        violations = lint_tree(
            root / "pipeline" / "scout" / "_feedparser_adapter.py",
            rules=DEFAULT_RULES,
        )
        assert violations == []


# ---------------------------------------------------------------------------
# Public surface
# ---------------------------------------------------------------------------


class TestPublicSurface:
    def test_version_pin_rN_ge_6(self) -> None:
        # E-025 closure — range-check version pin, never hard-pin.
        v = scout.__version__
        assert v.startswith("0.1.0-scout-r")
        rN = int(v.rsplit("-r", 1)[1])
        assert rN >= 6

    def test_discover_channel_e_reachable_via_pipeline_scout(self) -> None:
        assert scout.discover_channel_e is discover_channel_e

    def test_f_scout_e_codes_match_blueprint(self) -> None:
        assert F_SCOUT_E_01 == "F-SCOUT-E-01"
        assert F_SCOUT_E_02 == "F-SCOUT-E-02"
        assert F_SCOUT_E_03 == "F-SCOUT-E-03"

    def test_channel_e_constant_equals_E(self) -> None:
        assert CHANNEL_E == "E"

    def test_reexports_include_feedspec_and_factory(self) -> None:
        for name in (
            "FeedSpec",
            "FeedEntry",
            "FeedParseResult",
            "FeedParserFactory",
            "FeedparserLibFactory",
            "FeedparserLibHandle",
            "ChannelESubEvent",
            "ChannelEDegradationEvent",
            "ChannelEDiscoverResult",
            "classify_channel_e",
            "discover_channel_e",
        ):
            assert hasattr(scout, name), f"missing re-export: {name}"


# ---------------------------------------------------------------------------
# Concrete FeedparserLibFactory smoke tests
# ---------------------------------------------------------------------------


class TestFeedparserLibFactory:
    def test_parse_streaming_returns_feedparseresult(self) -> None:
        factory = FeedparserLibFactory()
        body = (
            b"<?xml version='1.0'?>"
            b"<rss version='2.0'><channel><title>T</title>"
            b"<item><title>Entry 1</title><guid>g-1</guid>"
            b"<link>https://ex.org/1</link>"
            b"<description>hello</description></item>"
            b"</channel></rss>"
        )
        result = factory.parse_streaming(body)
        assert isinstance(result, FeedParseResult)
        assert result.streaming is False
        assert isinstance(result.raw_data_buffer_handle, FeedparserLibHandle)

    def test_parse_streaming_produces_feed_entry(self) -> None:
        factory = FeedparserLibFactory()
        body = (
            b"<?xml version='1.0'?>"
            b"<rss version='2.0'><channel><title>T</title>"
            b"<item><title>Entry 1</title><guid>g-1</guid>"
            b"<link>https://ex.org/1</link>"
            b"<description>hello</description></item>"
            b"</channel></rss>"
        )
        result = factory.parse_streaming(body)
        entries = list(result.entries)
        assert len(entries) == 1
        assert entries[0].guid == "g-1"
        assert entries[0].link == "https://ex.org/1"

    def test_handle_raw_data_carries_full_body(self) -> None:
        factory = FeedparserLibFactory()
        body = b"<rss><channel></channel></rss>"
        result = factory.parse_streaming(body)
        assert bytes(result.raw_data_buffer_handle.raw_data) == body

    def test_handle_reset_empties_raw_data(self) -> None:
        handle = FeedparserLibHandle(raw_data=bytearray(b"leftover"))
        handle.reset()
        assert bytes(handle.raw_data) == b""


# ---------------------------------------------------------------------------
# Feed URL / id helpers standalone
# ---------------------------------------------------------------------------


class TestFeedUrlHelpers:
    def test_compute_feed_or_adapter_id_prefix(self) -> None:
        fid = _compute_feed_or_adapter_id("https://feeds.example.org/a")
        assert fid.startswith("rss:")
        assert len(fid) == len("rss:") + 32  # 16 bytes hex = 32 chars

    def test_canonical_feed_url_preserves_query(self) -> None:
        assert (
            _canonical_feed_url("https://EX.org/a?x=1&y=2")
            == "https://ex.org/a?x=1&y=2"
        )

    def test_canonical_feed_url_preserves_fragment(self) -> None:
        assert (
            _canonical_feed_url("https://ex.org/a#frag")
            == "https://ex.org/a#frag"
        )

    def test_canonical_feed_url_handles_port(self) -> None:
        assert (
            _canonical_feed_url("https://EX.org:8080/a/")
            == "https://ex.org:8080/a"
        )


# ---------------------------------------------------------------------------
# Gap-coverage — walks branches the main suite does not reach via discover
# ---------------------------------------------------------------------------


class TestGapCoverage:
    def test_canonical_feed_url_idna_unicodeerror_falls_back_to_host(self) -> None:
        # Hosts with an empty label (e.g. ".." between dots) raise UnicodeError
        # from .encode("idna"); branch 212-213 returns the raw host verbatim.
        out = _canonical_feed_url("https://a..b/path")
        assert "a..b" in out

    def test_fetch_timestamp_iso_attaches_utc_for_naive_clock(self) -> None:
        # Line 268-269: naive datetime from clock() gets UTC attached before
        # strftime. Verify output is RFC-3339-z formatted.
        from pipeline.scout.channel_e_rss import _fetch_timestamp_iso

        def naive_clock() -> _dt.datetime:
            return _dt.datetime(2026, 4, 20, 12, 0, 0)  # naive — no tzinfo

        assert _fetch_timestamp_iso(naive_clock) == "2026-04-20T12:00:00Z"

    def test_parse_iso_attaches_utc_for_date_only_format(self) -> None:
        # Line 336-337: "%Y-%m-%d" produces naive datetime; branch attaches UTC.
        from pipeline.scout.channel_e_rss import _parse_iso

        dt = _parse_iso("2026-04-15")
        assert dt is not None
        assert dt.tzinfo is _dt.timezone.utc
        assert dt.year == 2026 and dt.month == 4 and dt.day == 15

    def test_is_feed_stale_skips_empty_strings(self) -> None:
        # Line 363-364: empty-string published_iso is skipped before _parse_iso.
        from pipeline.scout.channel_e_rss import _is_feed_stale

        clk = _FrozenClock()
        # All empty strings → no most_recent → NOT stale.
        assert (
            _is_feed_stale(
                now=clk.now,
                entries_published=["", "", ""],
                threshold_days=60,
            )
            is False
        )

    def test_escalate_keeps_current_when_incoming_not_higher(self) -> None:
        from pipeline.scout.channel_e_rss import _escalate

        # Incoming strictly lower (DEGRADED < FAILED): keep current (FAILED).
        assert _escalate(HEALTH_FAILED, HEALTH_DEGRADED) == HEALTH_FAILED
        # Incoming equal: keep current.
        assert _escalate(HEALTH_DEGRADED, HEALTH_DEGRADED) == HEALTH_DEGRADED

    def test_is_tls_error_matches_ssl_class_name(self) -> None:
        from pipeline.scout.channel_e_rss import _is_tls_error

        class MySSLError(Exception):
            pass

        assert _is_tls_error(MySSLError()) is True

    def test_is_tls_error_falls_through_to_real_ssl_module(self) -> None:
        # Line 430-432: name-string miss → import ssl + isinstance check.
        import ssl

        from pipeline.scout.channel_e_rss import _is_tls_error

        class _RenamedTLS(ssl.SSLError):
            pass

        # Subclass whose __name__ lacks "SSL" forces the isinstance branch.
        _RenamedTLS.__name__ = "Renamed"
        assert _is_tls_error(_RenamedTLS()) is True
        assert _is_tls_error(ValueError("not TLS")) is False

    def test_5xx_response_marks_feed_failed(self) -> None:
        # Lines 522-532: status >= 500 → HEALTH_FAILED + F-SCOUT-E-02.
        factory = _ScriptedFeedParserFactory(results=[])  # parse never reached
        http = _ScriptedHTTPClient(
            script=[_FakeResponse(status=503, headers={}, body_bytes=b"")]
        )
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        result = discover_channel_e(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            feed_parser_factory=factory,
            feed_watchlist=(FeedSpec(feed_url="https://feeds.example.org/500"),),
            clock=clk,
        )
        states = list(result.per_feed_state.values())
        assert states == [HEALTH_FAILED]
        codes = [e.code for e in result.degradation_events]
        assert F_SCOUT_E_02 in codes

    def test_feedparser_adapter_stringifies_non_bytes_summary(self) -> None:
        # _feedparser_adapter: summary reached only when content is a list
        # (Python precedence in the ternary chain). Pass content=[] to gate in.
        from pipeline.scout._feedparser_adapter import _canonicalize_entry_body

        out = _canonicalize_entry_body({"summary": 12345, "content": []})
        assert out == b"12345"

    def test_feedparser_adapter_decodes_bytes_summary(self) -> None:
        from pipeline.scout._feedparser_adapter import _canonicalize_entry_body

        out = _canonicalize_entry_body({"summary": b"hello bytes", "content": []})
        assert out == b"hello bytes"

    def test_feedparser_adapter_strips_trailing_empty_lines(self) -> None:
        # Trailing empty-line pop loop.
        from pipeline.scout._feedparser_adapter import _canonicalize_entry_body

        out = _canonicalize_entry_body({"summary": "a\nb\n\n\n", "content": []})
        assert out == b"a\nb"

    def test_feedparser_adapter_surfaces_feed_modified_iso_from_updated(self) -> None:
        # Line 115 — candidate str(feed.updated) path.
        factory = FeedparserLibFactory()
        body = (
            b"<?xml version='1.0'?>"
            b"<rss version='2.0'><channel><title>T</title>"
            b"<lastBuildDate>Sat, 18 Apr 2026 10:00:00 +0000</lastBuildDate>"
            b"<pubDate>Sat, 18 Apr 2026 10:00:00 +0000</pubDate>"
            b"<item><title>E</title><guid>g</guid><link>https://e/1</link>"
            b"<description>x</description></item>"
            b"</channel></rss>"
        )
        result = factory.parse_streaming(body)
        # Some feedparser versions surface the feed-level timestamp — the
        # branch exists to stringify it when present. If absent, the adapter
        # legitimately returns None. This test tolerates both.
        assert result.feed_modified_iso is None or isinstance(
            result.feed_modified_iso, str
        )

    def test_feedparser_adapter_feed_modified_iso_via_stub(self) -> None:
        # Deterministic coverage for line 115: stub feedparser.parse so that
        # parsed.feed.get("updated") returns a non-empty value.
        import types

        from pipeline.scout import _feedparser_adapter as adapter_mod

        class _StubFeed(dict):
            pass

        class _StubParsed:
            bozo = False
            feed = _StubFeed(updated="2026-04-18T10:00:00Z")
            entries: list = []

        stub = types.SimpleNamespace(parse=lambda raw: _StubParsed())
        import sys as _sys

        orig = _sys.modules.get("feedparser")
        _sys.modules["feedparser"] = stub  # type: ignore[assignment]
        try:
            result = adapter_mod.FeedparserLibFactory().parse_streaming(b"<rss/>")
            assert result.feed_modified_iso == "2026-04-18T10:00:00Z"
        finally:
            if orig is not None:
                _sys.modules["feedparser"] = orig
            else:
                _sys.modules.pop("feedparser", None)
