"""Round 5 — pipeline.scout.channel_c_portals + channel_d_program_pages.

Exercises the Channel C portal adapter dispatcher and Channel D program-page
adapter dispatcher against fake adapters + the shared Round 4 HTTPClient /
FDBroker / NonceRegistry / ClockFn Protocols. No real sockets, no real
vault, no real sleep.

Covers §4.3 portal registry + state aggregation + portal opt-in roster;
§4.4 program-page registry + per-page cap (200) + per-adapter cumulative
cap (500); A-v3-09 feed_or_adapter_id namespacing; shared AdapterContext +
http_request_with_retries with Round 4 retry ladder + nonce/FD lifecycle
parity.
"""

from __future__ import annotations

import datetime as _dt
import socket
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator, Mapping, Optional

import pytest

import pipeline.scout as scout
from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree
from pipeline.scout import (
    CHANNEL_C,
    CHANNEL_D,
    CHANNEL_D_MAX_CANDIDATES_PER_PAGE,
    CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER,
    FEED_PREFIX_ALN,
    FEED_PREFIX_PORTAL,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
    AdapterContext,
    Candidate,
    ChannelCDegradationEvent,
    ChannelCDiscoverResult,
    ChannelDDegradationEvent,
    ChannelDDiscoverResult,
    PORTAL_ADAPTERS,
    PROGRAM_PAGE_ADAPTERS,
    PortalAdapterOutcome,
    PortalSubEvent,
    ProgramPageOutcome,
    ProgramPageSubEvent,
    ScoutConfigError,
    channel_c_reset_registry_for_tests,
    channel_d_reset_registry_for_tests,
    classify_channel_c,
    classify_channel_d,
    discover_channel_c,
    discover_channel_d,
    http_request_with_retries,
    register_portal,
    register_program_page,
)
from pipeline.scout import channel_c_portals as ch_c
from pipeline.scout import channel_d_program_pages as ch_d
from pipeline.scout.channel_c_portals import (
    F_SCOUT_C_01,
    F_SCOUT_C_02,
    F_SCOUT_C_03,
    _build_channel_c_candidate,
)
from pipeline.scout.channel_d_program_pages import (
    F_SCOUT_CHD_01,
    F_SCOUT_CHD_02,
    F_SCOUT_CHD_03,
    F_SCOUT_CHD_04,
    F_SCOUT_CHD_05,
    F_SCOUT_CHD_06,
    _build_channel_d_candidate,
    _normalize_aln,
)


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


@dataclass
class _FakeSession:
    session_id: str = "sess-round5"
    slug: str = "fit_farms_llc"


@dataclass
class _FakeResponse:
    status: int
    headers: Mapping[str, str]
    body_bytes: bytes

    @classmethod
    def ok(cls, body: bytes = b"{}") -> "_FakeResponse":
        return cls(
            status=200, headers={"Content-Type": "application/json"}, body_bytes=body
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
        if callable(item):
            item()
            raise AssertionError("script callable did not raise")
        return item


@dataclass
class _CountingFDBroker:
    fds_issued: list[int] = field(default_factory=list)
    fds_released: list[int] = field(default_factory=list)
    request_log: list[dict] = field(default_factory=list)
    next_fd: int = 2000
    raise_on_request: Optional[Exception] = None

    def request_fd(self, *, kind: str, host: str) -> int:
        self.request_log.append({"kind": kind, "host": host})
        if self.raise_on_request is not None:
            raise self.raise_on_request
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
    raise_on_reserve: Optional[Exception] = None

    def reserve(self, nonce_hex: str) -> None:
        if self.raise_on_reserve is not None:
            raise self.raise_on_reserve
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_candidate_c(cslug: str, source_key: str = "row-1") -> Candidate:
    return _build_channel_c_candidate(
        cslug=cslug,
        source_key=source_key,
        title=f"Test Portal {cslug}",
        funder="State of Example",
        funder_kind="state",
        url=f"https://example.gov/{source_key}",
        url_hash="a" * 32,
        content_hash="c" * 64,
        close_date_utc="2026-12-31T23:59:59Z",
        award_ceiling=100_000,
        award_floor=10_000,
        applicant_types=(),
        program_page_url=None,
        fetch_timestamp_utc="2026-04-20T12:00:00Z",
        fit_score_cached=0,
        cache_provenance=None,
        candidate_id=f"cid-{cslug}-{source_key}"[:24].ljust(24, "z"),
    )


def _make_candidate_d(aln: str, source_key: str = "opp-1") -> Candidate:
    return _build_channel_d_candidate(
        aln_number=aln,
        source_key=source_key,
        title=f"Program Page {aln}",
        funder="Federal Agency",
        funder_kind="federal",
        url=f"https://www.federalregister.gov/{aln}/{source_key}",
        url_hash="b" * 32,
        content_hash="d" * 64,
        close_date_utc="2026-12-31T23:59:59Z",
        award_ceiling=500_000,
        award_floor=50_000,
        applicant_types=(),
        program_page_url=None,
        fetch_timestamp_utc="2026-04-20T12:00:00Z",
        fit_score_cached=0,
        cache_provenance=None,
        candidate_id=f"cid-{aln}-{source_key}"[:24].ljust(24, "z"),
    )


def _build_ctx(
    *,
    http_client: Optional[_ScriptedHTTPClient] = None,
    fd_broker: Optional[_CountingFDBroker] = None,
    nonce_registry: Optional[_CountingNonceRegistry] = None,
    clock: Optional[_FrozenClock] = None,
) -> tuple:
    session = _FakeSession()
    http = http_client or _ScriptedHTTPClient(
        default_response=_FakeResponse.ok()
    )
    fd = fd_broker or _CountingFDBroker()
    nonce = nonce_registry or _CountingNonceRegistry()
    clk = clock or _FrozenClock()
    return session, fd, nonce, http, clk


@pytest.fixture(autouse=True)
def _reset_registries() -> Iterator[None]:
    # Clear the registries that the bound dispatchers will actually read
    # from. Round 1's test_package_import_runs_under_100ms reloads
    # pipeline.scout — after which sys.modules["...channel_c_portals"]
    # is a NEW module, but `discover_channel_{c,d}` imported into THIS
    # test file at module load are still bound to the OLD module's
    # PORTAL_ADAPTERS / PROGRAM_PAGE_ADAPTERS dicts. Reach through
    # __globals__ so reset actually clears the dict the dispatchers see.
    discover_channel_c.__globals__["PORTAL_ADAPTERS"].clear()
    discover_channel_d.__globals__["PROGRAM_PAGE_ADAPTERS"].clear()
    # Also clear the currently-live sys.modules view so tests that use
    # register_{portal,program_page} (which re-resolve the module each
    # call) see the same fresh slate.
    channel_c_reset_registry_for_tests()
    channel_d_reset_registry_for_tests()
    yield
    discover_channel_c.__globals__["PORTAL_ADAPTERS"].clear()
    discover_channel_d.__globals__["PROGRAM_PAGE_ADAPTERS"].clear()
    channel_c_reset_registry_for_tests()
    channel_d_reset_registry_for_tests()


# ---------------------------------------------------------------------------
# Channel C — Happy Path
# ---------------------------------------------------------------------------


class TestChannelCHappyPath:
    def test_single_adapter_ok(self) -> None:
        @register_portal("usda-grants-portal")
        def _fake(ctx: AdapterContext) -> PortalAdapterOutcome:
            return PortalAdapterOutcome(
                candidates=(_make_candidate_c("usda-grants-portal"),),
                state=HEALTH_OK,
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("usda-grants-portal",),
            clock=clk,
        )
        assert isinstance(result, ChannelCDiscoverResult)
        assert result.channel_state == HEALTH_OK
        assert result.per_adapter_state == {"usda-grants-portal": HEALTH_OK}
        assert len(result.candidates) == 1
        assert result.candidates[0].channel == CHANNEL_C
        assert result.candidates[0].feed_or_adapter_id == (
            f"{FEED_PREFIX_PORTAL}:usda-grants-portal"
        )
        assert result.degradation_events == ()

    def test_three_adapters_all_ok(self) -> None:
        for slug in ("portal-a", "portal-b", "portal-c"):
            s = slug

            @register_portal(s)
            def _fake(
                ctx: AdapterContext, _s: str = s
            ) -> PortalAdapterOutcome:
                return PortalAdapterOutcome(
                    candidates=(_make_candidate_c(_s),),
                    state=HEALTH_OK,
                )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("portal-a", "portal-b", "portal-c"),
            clock=clk,
        )
        assert result.channel_state == HEALTH_OK
        assert len(result.candidates) == 3

    def test_adapter_zero_candidates_still_ok(self) -> None:
        @register_portal("empty-portal")
        def _fake(ctx: AdapterContext) -> PortalAdapterOutcome:
            return PortalAdapterOutcome(candidates=(), state=HEALTH_OK)

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("empty-portal",),
            clock=clk,
        )
        assert result.channel_state == HEALTH_OK
        assert result.candidates == ()

    def test_roster_order_preserved_in_output(self) -> None:
        for slug in ("z-last", "a-first", "m-middle"):
            s = slug

            @register_portal(s)
            def _fake(
                ctx: AdapterContext, _s: str = s
            ) -> PortalAdapterOutcome:
                return PortalAdapterOutcome(
                    candidates=(_make_candidate_c(_s),),
                    state=HEALTH_OK,
                )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("a-first", "m-middle", "z-last"),
            clock=clk,
        )
        keys = list(result.per_adapter_state.keys())
        assert keys == ["a-first", "m-middle", "z-last"]


# ---------------------------------------------------------------------------
# Channel C — Registry
# ---------------------------------------------------------------------------


class TestChannelCRegistry:
    def test_register_portal_stores_under_canonical_slug(self) -> None:
        @register_portal("SBA Foundation")
        def _fake(ctx: AdapterContext) -> PortalAdapterOutcome:
            return PortalAdapterOutcome(candidates=(), state=HEALTH_OK)

        assert "sba-foundation" in PORTAL_ADAPTERS

    def test_duplicate_canonical_slug_raises_at_register(self) -> None:
        @register_portal("FooBar")
        def _first(ctx: AdapterContext) -> PortalAdapterOutcome:
            return PortalAdapterOutcome(candidates=(), state=HEALTH_OK)

        with pytest.raises(ScoutConfigError) as exc_info:

            @register_portal("foobar")
            def _second(ctx: AdapterContext) -> PortalAdapterOutcome:
                return PortalAdapterOutcome(candidates=(), state=HEALTH_OK)

        assert F_SCOUT_C_03 in str(exc_info.value)

    def test_nfc_drift_normalised_to_same_canonical(self) -> None:
        # canonical_slug rejects non-ASCII by design; verify the decorator
        # propagates that rejection rather than silently admitting.
        from pipeline.sovereignty.org_slug import InvalidSlug

        with pytest.raises(InvalidSlug):

            @register_portal("café")  # noqa: RUF001 — literal unicode for test
            def _fake(
                ctx: AdapterContext,
            ) -> PortalAdapterOutcome:  # pragma: no cover
                return PortalAdapterOutcome(candidates=(), state=HEALTH_OK)

    def test_portal_adapters_empty_after_reset(self) -> None:
        @register_portal("throwaway")
        def _fake(ctx: AdapterContext) -> PortalAdapterOutcome:
            return PortalAdapterOutcome(candidates=(), state=HEALTH_OK)

        assert "throwaway" in PORTAL_ADAPTERS
        channel_c_reset_registry_for_tests()
        assert "throwaway" not in PORTAL_ADAPTERS
        assert len(PORTAL_ADAPTERS) == 0

    def test_registry_is_module_level_ordereddict(self) -> None:
        from collections import OrderedDict

        assert isinstance(PORTAL_ADAPTERS, OrderedDict)


# ---------------------------------------------------------------------------
# Channel C — Adapter missing
# ---------------------------------------------------------------------------


class TestChannelCAdapterMissing:
    def test_missing_adapter_yields_failed_state(self) -> None:
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("not-registered",),
            clock=clk,
        )
        assert result.per_adapter_state == {"not-registered": HEALTH_FAILED}
        assert any(
            e.code == F_SCOUT_C_01 for e in result.degradation_events
        )

    def test_other_roster_adapters_continue_on_missing(self) -> None:
        @register_portal("registered-portal")
        def _fake(ctx: AdapterContext) -> PortalAdapterOutcome:
            return PortalAdapterOutcome(
                candidates=(_make_candidate_c("registered-portal"),),
                state=HEALTH_OK,
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("missing", "registered-portal"),
            clock=clk,
        )
        assert result.per_adapter_state["missing"] == HEALTH_FAILED
        assert result.per_adapter_state["registered-portal"] == HEALTH_OK
        assert len(result.candidates) == 1

    def test_missing_included_in_per_adapter_state(self) -> None:
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("ghost-portal",),
            clock=clk,
        )
        assert "ghost-portal" in result.per_adapter_state


# ---------------------------------------------------------------------------
# Channel C — Retry ladder (through http_request_with_retries)
# ---------------------------------------------------------------------------


class TestChannelCRetryLadder:
    def test_http_helper_5xx_then_success_degraded(self) -> None:
        http = _ScriptedHTTPClient(
            script=[
                _FakeResponse(status=500, headers={}, body_bytes=b""),
                _FakeResponse.ok(),
            ]
        )
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        ctx = AdapterContext(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            clock=clk,
        )
        result = http_request_with_retries(
            ctx, method="GET", url="https://example.gov/", host="example.gov"
        )
        assert result.state == HEALTH_DEGRADED
        assert result.outcome_tag == "success_after_retry"
        assert clk.sleeps == [1.0]

    def test_http_helper_5xx_exhausted_failed(self) -> None:
        http = _ScriptedHTTPClient(
            script=[
                _FakeResponse(status=503, headers={}, body_bytes=b"")
                for _ in range(4)
            ]
        )
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        ctx = AdapterContext(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            clock=clk,
        )
        result = http_request_with_retries(
            ctx, method="GET", url="https://example.gov/", host="example.gov"
        )
        assert result.state == HEALTH_FAILED
        assert result.outcome_tag == "retries_exhausted"
        assert clk.sleeps == [1.0, 2.0, 4.0]

    def test_http_helper_connection_reset_exhausted_failed(self) -> None:
        def _raise() -> None:
            raise ConnectionResetError("reset")

        http = _ScriptedHTTPClient(script=[_raise, _raise, _raise, _raise])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        ctx = AdapterContext(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            clock=clk,
        )
        result = http_request_with_retries(
            ctx, method="GET", url="https://example.gov/", host="example.gov"
        )
        assert result.state == HEALTH_FAILED
        assert result.path_tag == "connection_reset"

    def test_http_helper_timeout_exhausted_failed(self) -> None:
        def _raise() -> None:
            raise TimeoutError("slow")

        http = _ScriptedHTTPClient(script=[_raise, _raise, _raise, _raise])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        ctx = AdapterContext(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            clock=clk,
        )
        result = http_request_with_retries(
            ctx, method="GET", url="https://example.gov/", host="example.gov"
        )
        assert result.state == HEALTH_FAILED
        assert result.path_tag == "timeout"

    def test_http_helper_4xx_not_retried(self) -> None:
        http = _ScriptedHTTPClient(
            script=[_FakeResponse(status=404, headers={}, body_bytes=b"")]
        )
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        ctx = AdapterContext(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            clock=clk,
        )
        result = http_request_with_retries(
            ctx, method="GET", url="https://example.gov/", host="example.gov"
        )
        assert result.state == HEALTH_DEGRADED
        assert result.outcome_tag == "http_4xx"
        assert clk.sleeps == []  # no retry on 4xx
        assert len(http.calls) == 1

    def test_http_helper_first_success_no_sleep(self) -> None:
        http = _ScriptedHTTPClient(script=[_FakeResponse.ok()])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        ctx = AdapterContext(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            clock=clk,
        )
        result = http_request_with_retries(
            ctx, method="GET", url="https://example.gov/", host="example.gov"
        )
        assert result.state == HEALTH_OK
        assert clk.sleeps == []


# ---------------------------------------------------------------------------
# Channel C — State aggregation
# ---------------------------------------------------------------------------


class TestChannelCStateAggregation:
    def test_all_ok(self) -> None:
        assert classify_channel_c({"a": HEALTH_OK, "b": HEALTH_OK}) == HEALTH_OK

    def test_one_failed_of_three_degraded(self) -> None:
        assert (
            classify_channel_c(
                {"a": HEALTH_FAILED, "b": HEALTH_OK, "c": HEALTH_OK}
            )
            == HEALTH_DEGRADED
        )

    def test_two_failed_of_three_failed(self) -> None:
        # 2/3 ≥ 0.5 = threshold (2*2 ≥ 3 so counts).
        assert (
            classify_channel_c(
                {"a": HEALTH_FAILED, "b": HEALTH_FAILED, "c": HEALTH_OK}
            )
            == HEALTH_FAILED
        )

    def test_exactly_half_failed_of_ten_failed(self) -> None:
        state = {f"p{i}": HEALTH_FAILED for i in range(5)}
        state.update({f"q{i}": HEALTH_OK for i in range(5)})
        assert classify_channel_c(state) == HEALTH_FAILED

    def test_four_failed_of_ten_degraded(self) -> None:
        state = {f"p{i}": HEALTH_FAILED for i in range(4)}
        state.update({f"q{i}": HEALTH_OK for i in range(6)})
        assert classify_channel_c(state) == HEALTH_DEGRADED


# ---------------------------------------------------------------------------
# Channel C — Nonce + FD lifecycle parity
# ---------------------------------------------------------------------------


class TestChannelCNonceFDLifecycle:
    def test_nonce_fd_parity_on_success(self) -> None:
        http = _ScriptedHTTPClient(script=[_FakeResponse.ok()])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        ctx = AdapterContext(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            clock=clk,
        )
        http_request_with_retries(
            ctx, method="GET", url="https://example.gov/", host="example.gov"
        )
        assert len(nonce.reserved) == 1
        assert len(nonce.released) == 1
        assert len(fd.fds_issued) == 1
        assert len(fd.fds_released) == 1

    def test_fd_released_before_nonce(self) -> None:
        # FD release happens in the inner finally; nonce release happens in
        # the outer finally. We can't observe wall-clock ordering from the
        # counting fakes directly, but we can observe both were called.
        http = _ScriptedHTTPClient(script=[_FakeResponse.ok()])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        ctx = AdapterContext(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            clock=clk,
        )
        http_request_with_retries(
            ctx, method="GET", url="https://example.gov/", host="example.gov"
        )
        assert fd.fds_released == fd.fds_issued
        assert nonce.released[0]["nonce_hex"] == nonce.reserved[0]

    def test_fd_broker_raise_nonce_still_released(self) -> None:
        http = _ScriptedHTTPClient()
        fd = _CountingFDBroker(raise_on_request=RuntimeError("broker_down"))
        nonce = _CountingNonceRegistry()
        session, _, _, _, clk = _build_ctx(
            http_client=http, fd_broker=fd, nonce_registry=nonce
        )
        ctx = AdapterContext(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            clock=clk,
        )
        result = http_request_with_retries(
            ctx, method="GET", url="https://example.gov/", host="example.gov"
        )
        assert result.state == HEALTH_FAILED
        assert result.outcome_tag == "fd_error"
        assert len(nonce.reserved) == 1
        assert len(nonce.released) == 1  # nonce still released
        assert len(fd.fds_issued) == 0  # never got FD

    def test_nonce_reserve_raise_no_fd_requested(self) -> None:
        http = _ScriptedHTTPClient()
        fd = _CountingFDBroker()
        nonce = _CountingNonceRegistry(
            raise_on_reserve=RuntimeError("replay")
        )
        session, _, _, _, clk = _build_ctx(
            http_client=http, fd_broker=fd, nonce_registry=nonce
        )
        ctx = AdapterContext(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            clock=clk,
        )
        result = http_request_with_retries(
            ctx, method="GET", url="https://example.gov/", host="example.gov"
        )
        assert result.state == HEALTH_FAILED
        assert result.outcome_tag == "nonce_error"
        assert len(fd.request_log) == 0  # never called FD broker

    def test_http_client_exception_nonce_fd_still_released(self) -> None:
        def _raise() -> None:
            raise ValueError("unexpected")

        http = _ScriptedHTTPClient(script=[_raise])
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        ctx = AdapterContext(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            clock=clk,
        )
        result = http_request_with_retries(
            ctx, method="GET", url="https://example.gov/", host="example.gov"
        )
        # ValueError is NOT TimeoutError/ConnectionError — the inner
        # try/except in _do_request_with_retries does not catch it; the
        # outer wrapper in http_request_with_retries catches via
        # Exception, yielding state=FAILED + outcome_tag="exception".
        assert result.state == HEALTH_FAILED
        assert result.outcome_tag == "exception"
        assert len(nonce.released) == 1
        assert len(fd.fds_released) == 1

    def test_adapter_raise_tagged_f_scout_c_02(self) -> None:
        @register_portal("buggy")
        def _adapter(ctx: AdapterContext) -> PortalAdapterOutcome:
            raise RuntimeError("adapter blew up")

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("buggy",),
            clock=clk,
        )
        assert result.per_adapter_state == {"buggy": HEALTH_FAILED}
        assert any(
            e.code == F_SCOUT_C_02 for e in result.degradation_events
        )


# ---------------------------------------------------------------------------
# Channel C — Feed-adapter ID namespacing
# ---------------------------------------------------------------------------


class TestChannelCFeedAdapterIdNamespace:
    def test_helper_asserts_portal_prefix(self) -> None:
        cand = _build_channel_c_candidate(
            cslug="myportal",
            source_key="k1",
            title="t",
            funder="f",
            funder_kind="state",
            url="https://x.gov/",
            url_hash="h",
            content_hash=None,
            close_date_utc=None,
            award_ceiling=None,
            award_floor=None,
            applicant_types=(),
            program_page_url=None,
            fetch_timestamp_utc="2026-04-20T12:00:00Z",
            fit_score_cached=0,
            cache_provenance=None,
            candidate_id="c" * 24,
        )
        assert cand.feed_or_adapter_id == f"{FEED_PREFIX_PORTAL}:myportal"

    def test_candidate_channel_is_c(self) -> None:
        cand = _make_candidate_c("myportal")
        assert cand.channel == CHANNEL_C


# ---------------------------------------------------------------------------
# Channel C — No module side effects + KW-only
# ---------------------------------------------------------------------------


class TestChannelCNoModuleSideEffects:
    def test_import_opens_zero_fds_zero_nonces(self) -> None:
        # Fresh registries on import = empty.
        assert len(PORTAL_ADAPTERS) == 0
        assert len(PROGRAM_PAGE_ADAPTERS) == 0


class TestChannelCKWOnly:
    def test_positional_call_rejected(self) -> None:
        session, fd, nonce, http, clk = _build_ctx()
        with pytest.raises(TypeError):
            discover_channel_c(session, fd, nonce, http, ())  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Channel D — Happy Path
# ---------------------------------------------------------------------------


class TestChannelDHappyPath:
    def test_single_adapter_single_page_ok(self) -> None:
        @register_program_page("10.027")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(
                page_candidates=(_make_candidate_d("10.027"),),
                page_state=HEALTH_OK,
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.027",),
            clock=clk,
        )
        assert isinstance(result, ChannelDDiscoverResult)
        assert result.channel_state == HEALTH_OK
        assert result.per_adapter_state == {"10.027": HEALTH_OK}
        assert len(result.candidates) == 1
        assert result.candidates[0].channel == CHANNEL_D

    def test_single_adapter_multi_page_ok(self) -> None:
        @register_program_page("10.030")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            for i in range(3):
                yield ProgramPageOutcome(
                    page_candidates=(_make_candidate_d("10.030", f"p{i}"),),
                    page_state=HEALTH_OK,
                )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.030",),
            clock=clk,
        )
        assert result.channel_state == HEALTH_OK
        assert len(result.candidates) == 3

    def test_three_adapters_all_ok(self) -> None:
        for aln in ("10.001", "10.002", "10.003"):
            a = aln

            @register_program_page(a)
            def _fake(
                ctx: AdapterContext, _a: str = a
            ) -> Iterator[ProgramPageOutcome]:
                yield ProgramPageOutcome(
                    page_candidates=(_make_candidate_d(_a),),
                    page_state=HEALTH_OK,
                )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.001", "10.002", "10.003"),
            clock=clk,
        )
        assert result.channel_state == HEALTH_OK
        assert len(result.candidates) == 3

    def test_adapter_zero_rows_still_ok(self) -> None:
        @register_program_page("10.999")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(page_candidates=(), page_state=HEALTH_OK)

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.999",),
            clock=clk,
        )
        assert result.channel_state == HEALTH_OK
        assert result.candidates == ()


# ---------------------------------------------------------------------------
# Channel D — Registry
# ---------------------------------------------------------------------------


class TestChannelDRegistry:
    def test_register_stores_under_normalised_aln(self) -> None:
        @register_program_page("  10.027  ")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(page_candidates=(), page_state=HEALTH_OK)

        assert "10.027" in PROGRAM_PAGE_ADAPTERS

    def test_duplicate_aln_raises(self) -> None:
        @register_program_page("10.500")
        def _first(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(page_candidates=(), page_state=HEALTH_OK)

        with pytest.raises(ScoutConfigError) as exc_info:

            @register_program_page("10.500")
            def _second(
                ctx: AdapterContext,
            ) -> Iterator[ProgramPageOutcome]:
                yield ProgramPageOutcome(
                    page_candidates=(), page_state=HEALTH_OK
                )

        assert F_SCOUT_CHD_01 in str(exc_info.value)

    def test_program_page_adapters_empty_after_reset(self) -> None:
        @register_program_page("10.800")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(page_candidates=(), page_state=HEALTH_OK)

        assert "10.800" in PROGRAM_PAGE_ADAPTERS
        channel_d_reset_registry_for_tests()
        assert len(PROGRAM_PAGE_ADAPTERS) == 0

    def test_empty_aln_rejected(self) -> None:
        with pytest.raises(ValueError):

            @register_program_page("   ")
            def _fake(
                ctx: AdapterContext,
            ) -> Iterator[ProgramPageOutcome]:
                yield ProgramPageOutcome(
                    page_candidates=(), page_state=HEALTH_OK
                )


# ---------------------------------------------------------------------------
# Channel D — Per-page cap (200)
# ---------------------------------------------------------------------------


class TestChannelDPerPageCap:
    def test_200_rows_no_event(self) -> None:
        @register_program_page("10.010")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(
                page_candidates=tuple(
                    _make_candidate_d("10.010", f"r{i}") for i in range(200)
                ),
                page_state=HEALTH_OK,
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.010",),
            clock=clk,
        )
        assert len(result.candidates) == 200
        assert not any(
            e.code == F_SCOUT_CHD_02 for e in result.degradation_events
        )

    def test_201_rows_truncated_to_200_event_emitted(self) -> None:
        @register_program_page("10.011")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(
                page_candidates=tuple(
                    _make_candidate_d("10.011", f"r{i}") for i in range(201)
                ),
                page_state=HEALTH_OK,
                page_raw_count=201,
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.011",),
            clock=clk,
        )
        assert len(result.candidates) == CHANNEL_D_MAX_CANDIDATES_PER_PAGE
        evts = [
            e
            for e in result.degradation_events
            if e.code == F_SCOUT_CHD_02
        ]
        assert len(evts) == 1
        assert evts[0].overflow_count == 1
        assert result.per_adapter_state["10.011"] == HEALTH_DEGRADED

    def test_500_rows_page_cap_overflow_300(self) -> None:
        @register_program_page("10.012")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(
                page_candidates=tuple(
                    _make_candidate_d("10.012", f"r{i}") for i in range(500)
                ),
                page_state=HEALTH_OK,
                page_raw_count=500,
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.012",),
            clock=clk,
        )
        assert len(result.candidates) == 200
        evts = [
            e
            for e in result.degradation_events
            if e.code == F_SCOUT_CHD_02
        ]
        assert evts[0].overflow_count == 300

    def test_cap_applied_before_append(self) -> None:
        """Property test: random N ∈ [0, 1000] → len(candidates) = min(N, 200)."""
        import random

        rng = random.Random(42)
        for _ in range(10):
            n = rng.randint(0, 1000)
            aln = f"10.{n:03d}"
            channel_c_reset_registry_for_tests()
            channel_d_reset_registry_for_tests()

            @register_program_page(aln)
            def _fake(
                ctx: AdapterContext, _n: int = n, _aln: str = aln
            ) -> Iterator[ProgramPageOutcome]:
                yield ProgramPageOutcome(
                    page_candidates=tuple(
                        _make_candidate_d(_aln, f"r{i}") for i in range(_n)
                    ),
                    page_state=HEALTH_OK,
                    page_raw_count=_n,
                )

            session, fd, nonce, http, clk = _build_ctx()
            result = discover_channel_d(
                session=session,
                fd_broker=fd,
                nonce_registry=nonce,
                http_client=http,
                adapter_roster=(aln,),
                clock=clk,
            )
            expected = min(n, CHANNEL_D_MAX_CANDIDATES_PER_PAGE)
            assert len(result.candidates) == expected

    def test_multiple_pages_each_capped_independently(self) -> None:
        @register_program_page("10.013")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            # First page: 250 rows (50 overflow). Second page: 150 rows.
            # Note: cumulative cap is 500, so 200 + 150 = 350 < 500 fits.
            yield ProgramPageOutcome(
                page_candidates=tuple(
                    _make_candidate_d("10.013", f"p1r{i}")
                    for i in range(250)
                ),
                page_state=HEALTH_OK,
                page_raw_count=250,
            )
            yield ProgramPageOutcome(
                page_candidates=tuple(
                    _make_candidate_d("10.013", f"p2r{i}")
                    for i in range(150)
                ),
                page_state=HEALTH_OK,
                page_raw_count=150,
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.013",),
            clock=clk,
        )
        # 200 (capped) + 150 = 350.
        assert len(result.candidates) == 350
        page_cap_evts = [
            e for e in result.degradation_events if e.code == F_SCOUT_CHD_02
        ]
        assert len(page_cap_evts) == 1


# ---------------------------------------------------------------------------
# Channel D — Per-adapter cumulative cap (500)
# ---------------------------------------------------------------------------


class TestChannelDPerAdapterCap:
    def test_adapter_below_cap_ok(self) -> None:
        @register_program_page("10.020")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            for _ in range(2):
                yield ProgramPageOutcome(
                    page_candidates=tuple(
                        _make_candidate_d("10.020", f"r{i}") for i in range(200)
                    ),
                    page_state=HEALTH_OK,
                )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.020",),
            clock=clk,
        )
        assert len(result.candidates) == 400  # 2 × 200 < 500

    def test_adapter_hits_cap_mid_page(self) -> None:
        # First page 200 → counter = 200.
        # Second page 200 → counter = 400.
        # Third page 200 → counter would be 600; only 100 of the 200
        # get appended (500 cap), F-SCOUT-CHD-03 with overflow=100.
        @register_program_page("10.021")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            for _ in range(3):
                yield ProgramPageOutcome(
                    page_candidates=tuple(
                        _make_candidate_d("10.021", f"r{i}") for i in range(200)
                    ),
                    page_state=HEALTH_OK,
                )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.021",),
            clock=clk,
        )
        assert len(result.candidates) == CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER
        evts = [e for e in result.degradation_events if e.code == F_SCOUT_CHD_03]
        assert len(evts) == 1
        assert evts[0].overflow_count == 100
        assert result.per_adapter_state["10.021"] == HEALTH_DEGRADED

    def test_adapter_subsequent_pages_skipped_after_cap(self) -> None:
        calls: list[int] = []

        @register_program_page("10.022")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            for i in range(5):
                calls.append(i)
                yield ProgramPageOutcome(
                    page_candidates=tuple(
                        _make_candidate_d("10.022", f"p{i}r{j}")
                        for j in range(200)
                    ),
                    page_state=HEALTH_OK,
                )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.022",),
            clock=clk,
        )
        # Iterator should stop being consumed after cap hit; generator
        # produced pages 0, 1, 2 (the 3rd one triggered mid-page cap),
        # never got to page 3.
        assert max(calls) == 2
        assert len(result.candidates) == CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER

    def test_counter_is_local_to_run(self) -> None:
        @register_program_page("10.023")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(
                page_candidates=tuple(
                    _make_candidate_d("10.023", f"r{i}") for i in range(200)
                ),
                page_state=HEALTH_OK,
            )

        # Run 1 — fills 200.
        session, fd, nonce, http, clk = _build_ctx()
        r1 = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.023",),
            clock=clk,
        )
        # Run 2 — should start fresh (another 200), NOT continue from 200.
        session, fd, nonce, http, clk = _build_ctx()
        r2 = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.023",),
            clock=clk,
        )
        assert len(r1.candidates) == 200
        assert len(r2.candidates) == 200

    def test_other_adapters_continue_after_cap(self) -> None:
        @register_program_page("10.024")
        def _big(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            for _ in range(3):
                yield ProgramPageOutcome(
                    page_candidates=tuple(
                        _make_candidate_d("10.024", f"r{i}") for i in range(200)
                    ),
                    page_state=HEALTH_OK,
                )

        @register_program_page("10.025")
        def _small(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(
                page_candidates=(_make_candidate_d("10.025", "r1"),),
                page_state=HEALTH_OK,
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.024", "10.025"),
            clock=clk,
        )
        # 500 from the capped adapter + 1 from the small adapter.
        assert len(result.candidates) == CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER + 1
        assert result.per_adapter_state["10.024"] == HEALTH_DEGRADED
        assert result.per_adapter_state["10.025"] == HEALTH_OK


# ---------------------------------------------------------------------------
# Channel D — Retry ladder (adapter uses http_request_with_retries)
# ---------------------------------------------------------------------------


class TestChannelDRetryLadder:
    def test_adapter_using_http_5xx_exhausted_failed(self) -> None:
        http = _ScriptedHTTPClient(
            script=[
                _FakeResponse(status=500, headers={}, body_bytes=b"")
                for _ in range(4)
            ]
        )

        @register_program_page("10.030")
        def _adapter(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            r = http_request_with_retries(
                ctx, method="GET", url="https://x.gov/", host="x.gov"
            )
            yield ProgramPageOutcome(
                page_candidates=(),
                page_state=r.state,  # FAILED
            )

        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.030",),
            clock=clk,
        )
        assert result.per_adapter_state["10.030"] == HEALTH_FAILED

    def test_adapter_4xx_reports_degraded(self) -> None:
        http = _ScriptedHTTPClient(
            script=[_FakeResponse(status=404, headers={}, body_bytes=b"")]
        )

        @register_program_page("10.031")
        def _adapter(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            r = http_request_with_retries(
                ctx, method="GET", url="https://x.gov/", host="x.gov"
            )
            yield ProgramPageOutcome(
                page_candidates=(),
                page_state=r.state,  # DEGRADED for 4xx
            )

        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.031",),
            clock=clk,
        )
        assert result.per_adapter_state["10.031"] == HEALTH_DEGRADED

    def test_adapter_timeout_exhausted_failed(self) -> None:
        def _raise() -> None:
            raise TimeoutError("slow")

        http = _ScriptedHTTPClient(script=[_raise, _raise, _raise, _raise])

        @register_program_page("10.032")
        def _adapter(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            r = http_request_with_retries(
                ctx, method="GET", url="https://x.gov/", host="x.gov"
            )
            yield ProgramPageOutcome(
                page_candidates=(),
                page_state=r.state,
            )

        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.032",),
            clock=clk,
        )
        assert result.per_adapter_state["10.032"] == HEALTH_FAILED

    def test_sleep_sequence_observed(self) -> None:
        http = _ScriptedHTTPClient(
            script=[
                _FakeResponse(status=500, headers={}, body_bytes=b"")
                for _ in range(4)
            ]
        )
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        ctx = AdapterContext(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            clock=clk,
        )
        http_request_with_retries(
            ctx, method="GET", url="https://x.gov/", host="x.gov"
        )
        assert clk.sleeps == [1.0, 2.0, 4.0]

    def test_adapter_raising_tagged_f_scout_chd_04(self) -> None:
        @register_program_page("10.033")
        def _adapter(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            raise RuntimeError("adapter blew up")
            yield  # noqa: unreachable for generator discipline

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.033",),
            clock=clk,
        )
        assert result.per_adapter_state["10.033"] == HEALTH_FAILED
        assert any(
            e.code == F_SCOUT_CHD_04 for e in result.degradation_events
        )


# ---------------------------------------------------------------------------
# Channel D — State aggregation
# ---------------------------------------------------------------------------


class TestChannelDStateAggregation:
    def test_all_ok(self) -> None:
        assert classify_channel_d({"a": HEALTH_OK, "b": HEALTH_OK}) == HEALTH_OK

    def test_any_degraded_degraded(self) -> None:
        assert (
            classify_channel_d({"a": HEALTH_OK, "b": HEALTH_DEGRADED})
            == HEALTH_DEGRADED
        )

    def test_mixed_failed_ok_degraded(self) -> None:
        assert (
            classify_channel_d({"a": HEALTH_FAILED, "b": HEALTH_OK})
            == HEALTH_DEGRADED
        )

    def test_all_failed(self) -> None:
        assert (
            classify_channel_d({"a": HEALTH_FAILED, "b": HEALTH_FAILED})
            == HEALTH_FAILED
        )

    def test_empty_roster_failed(self) -> None:
        assert classify_channel_d({}) == HEALTH_FAILED


# ---------------------------------------------------------------------------
# Channel D — Nonce + FD lifecycle
# ---------------------------------------------------------------------------


class TestChannelDNonceFDLifecycle:
    def test_parity_per_http_call(self) -> None:
        @register_program_page("10.040")
        def _adapter(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            # Make three HTTP calls per adapter run.
            for _ in range(3):
                http_request_with_retries(
                    ctx, method="GET", url="https://x.gov/", host="x.gov"
                )
            yield ProgramPageOutcome(page_candidates=(), page_state=HEALTH_OK)

        http = _ScriptedHTTPClient(default_response=_FakeResponse.ok())
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.040",),
            clock=clk,
        )
        assert len(nonce.reserved) == len(nonce.released) == 3
        assert len(fd.fds_issued) == len(fd.fds_released) == 3

    def test_no_fd_leak_on_cap_reached(self) -> None:
        # Adapter that makes HTTP calls per page and then yields — after
        # cap hit, iterator is drained but no more HTTP calls are made.
        http_calls_per_page = 1

        @register_program_page("10.041")
        def _adapter(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            for i in range(3):
                http_request_with_retries(
                    ctx, method="GET", url="https://x.gov/", host="x.gov"
                )
                yield ProgramPageOutcome(
                    page_candidates=tuple(
                        _make_candidate_d("10.041", f"r{j}") for j in range(200)
                    ),
                    page_state=HEALTH_OK,
                )

        http = _ScriptedHTTPClient(default_response=_FakeResponse.ok())
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.041",),
            clock=clk,
        )
        # FD parity maintained even after cap hit.
        assert len(fd.fds_issued) == len(fd.fds_released)
        assert len(nonce.reserved) == len(nonce.released)

    def test_missing_adapter_no_fd_reserved(self) -> None:
        session, fd, nonce, http, clk = _build_ctx()
        discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.999",),
            clock=clk,
        )
        assert fd.fds_issued == []
        assert nonce.reserved == []

    def test_adapter_fd_broker_raise_nonce_released(self) -> None:
        fd = _CountingFDBroker(raise_on_request=RuntimeError("fd_down"))

        @register_program_page("10.042")
        def _adapter(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            r = http_request_with_retries(
                ctx, method="GET", url="https://x.gov/", host="x.gov"
            )
            yield ProgramPageOutcome(
                page_candidates=(),
                page_state=r.state,
            )

        session, _, nonce, http, clk = _build_ctx(fd_broker=fd)
        discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.042",),
            clock=clk,
        )
        # Nonce was reserved then released even though FD broker raised.
        assert len(nonce.reserved) == 1
        assert len(nonce.released) == 1
        assert len(fd.fds_issued) == 0

    def test_multiple_pages_release_fds_between_pages(self) -> None:
        @register_program_page("10.043")
        def _adapter(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            # Each page does one HTTP call.
            for _ in range(3):
                http_request_with_retries(
                    ctx, method="GET", url="https://x.gov/", host="x.gov"
                )
                yield ProgramPageOutcome(
                    page_candidates=(), page_state=HEALTH_OK
                )

        http = _ScriptedHTTPClient(default_response=_FakeResponse.ok())
        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.043",),
            clock=clk,
        )
        # 3 HTTP calls → 3 FDs issued and released in pairs.
        assert len(fd.fds_issued) == 3
        assert len(fd.fds_released) == 3


# ---------------------------------------------------------------------------
# Channel D — Feed-adapter ID namespacing
# ---------------------------------------------------------------------------


class TestChannelDFeedAdapterIdNamespace:
    def test_helper_prepends_aln_prefix(self) -> None:
        cand = _make_candidate_d("10.027")
        assert cand.feed_or_adapter_id == f"{FEED_PREFIX_ALN}:10.027"
        assert cand.channel == CHANNEL_D

    def test_normalize_aln_nfc_strip(self) -> None:
        assert _normalize_aln("  10.027  ") == "10.027"


# ---------------------------------------------------------------------------
# Channel D — No module side effects + KW-only
# ---------------------------------------------------------------------------


class TestChannelDNoModuleSideEffects:
    def test_import_leaves_registries_empty(self) -> None:
        assert len(PROGRAM_PAGE_ADAPTERS) == 0


class TestChannelDKWOnly:
    def test_positional_call_rejected(self) -> None:
        session, fd, nonce, http, clk = _build_ctx()
        with pytest.raises(TypeError):
            discover_channel_d(session, fd, nonce, http, ())  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Cross-module — shared Protocols + AST lint + surface
# ---------------------------------------------------------------------------


class TestSharedProtocolReuse:
    def test_both_dispatchers_accept_same_http_client(self) -> None:
        http = _ScriptedHTTPClient(default_response=_FakeResponse.ok())

        @register_portal("shared-portal")
        def _pc(ctx: AdapterContext) -> PortalAdapterOutcome:
            return PortalAdapterOutcome(candidates=(), state=HEALTH_OK)

        @register_program_page("99.999")
        def _pd(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(page_candidates=(), page_state=HEALTH_OK)

        session, fd, nonce, _, clk = _build_ctx(http_client=http)
        r_c = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("shared-portal",),
            clock=clk,
        )
        r_d = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("99.999",),
            clock=clk,
        )
        assert r_c.channel_state == HEALTH_OK
        assert r_d.channel_state == HEALTH_OK

    def test_adapter_context_is_shared_type(self) -> None:
        from pipeline.scout.channel_c_portals import AdapterContext as CtxC
        from pipeline.scout.channel_d_program_pages import AdapterContext as CtxD

        assert CtxC is CtxD

    def test_scout_config_error_shared_type(self) -> None:
        from pipeline.scout.channel_c_portals import ScoutConfigError as ErrC
        from pipeline.scout.channel_d_program_pages import ScoutConfigError as ErrD

        assert ErrC is ErrD


class TestASTLintRegression:
    def test_lint_channel_c_clean(self) -> None:
        import pathlib

        repo_root = pathlib.Path(__file__).resolve().parents[2]
        target = repo_root / "pipeline" / "scout" / "channel_c_portals.py"
        violations = [
            v
            for v in lint_tree(root=repo_root, rules=DEFAULT_RULES)
            if pathlib.Path(v.file).resolve() == target.resolve()
        ]
        assert violations == [], "\n".join(str(v) for v in violations)

    def test_lint_channel_d_clean(self) -> None:
        import pathlib

        repo_root = pathlib.Path(__file__).resolve().parents[2]
        target = (
            repo_root / "pipeline" / "scout" / "channel_d_program_pages.py"
        )
        violations = [
            v
            for v in lint_tree(root=repo_root, rules=DEFAULT_RULES)
            if pathlib.Path(v.file).resolve() == target.resolve()
        ]
        assert violations == [], "\n".join(str(v) for v in violations)


class TestPublicSurface:
    def test_version_bumped_to_round_5(self) -> None:
        assert scout.__version__.startswith("0.1.0-scout-r")
        assert int(scout.__version__.rsplit("r", 1)[1]) >= 5

    def test_discover_channel_c_reachable(self) -> None:
        from pipeline.scout import discover_channel_c as dc

        assert callable(dc)

    def test_discover_channel_d_reachable(self) -> None:
        from pipeline.scout import discover_channel_d as dd

        assert callable(dd)

    def test_registry_re_exports_reachable(self) -> None:
        assert scout.PORTAL_ADAPTERS is PORTAL_ADAPTERS
        assert scout.PROGRAM_PAGE_ADAPTERS is PROGRAM_PAGE_ADAPTERS


# ---------------------------------------------------------------------------
# Coverage gap closure — Channel C
# ---------------------------------------------------------------------------


class TestChannelCCoverageGaps:
    def test_classify_channel_c_empty_dict_failed(self) -> None:
        assert classify_channel_c({}) == HEALTH_FAILED

    def test_real_clock_callable_and_sleep(self) -> None:
        # Exercise _RealClock.__call__ and .sleep (default clock). Use
        # sleep(0) so the test never blocks.
        clk = ch_c._default_clock
        now = clk()
        assert isinstance(now, _dt.datetime)
        assert now.tzinfo is not None
        clk.sleep(0)  # no-op, but executes the body

    def test_invalid_roster_slug_emits_f_scout_c_01(self) -> None:
        # Canonical slug rejects non-ASCII — exercise the InvalidSlug branch.
        @register_portal("goodportal")
        def _good(ctx: AdapterContext) -> PortalAdapterOutcome:
            return PortalAdapterOutcome(candidates=(), state=HEALTH_OK)

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("café", "goodportal"),  # noqa: RUF001
            clock=clk,
        )
        evts = [e for e in result.degradation_events if e.code == F_SCOUT_C_01]
        assert any("roster_slug_invalid" in (e.reason_tag or "") for e in evts)
        # The good adapter still ran.
        assert result.per_adapter_state["goodportal"] == HEALTH_OK

    def test_duplicate_roster_slug_dispatched_once(self) -> None:
        calls: list[int] = []

        @register_portal("dupportal")
        def _fake(ctx: AdapterContext) -> PortalAdapterOutcome:
            calls.append(1)
            return PortalAdapterOutcome(candidates=(), state=HEALTH_OK)

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("dupportal", "dupportal", "DUPPORTAL"),
            clock=clk,
        )
        assert len(calls) == 1
        assert len(result.per_adapter_state) == 1

    def test_adapter_raising_scout_config_error_propagates(self) -> None:
        @register_portal("boom_portal")
        def _fake(ctx: AdapterContext) -> PortalAdapterOutcome:
            raise ScoutConfigError("bad wiring")

        session, fd, nonce, http, clk = _build_ctx()
        with pytest.raises(ScoutConfigError):
            discover_channel_c(
                session=session,
                fd_broker=fd,
                nonce_registry=nonce,
                http_client=http,
                portal_roster=("boom_portal",),
                clock=clk,
            )

    def test_adapter_returning_unknown_state_becomes_failed(self) -> None:
        @register_portal("weirdportal")
        def _fake(ctx: AdapterContext) -> PortalAdapterOutcome:
            return PortalAdapterOutcome(
                candidates=(), state="NONSENSE"  # type: ignore[arg-type]
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("weirdportal",),
            clock=clk,
        )
        assert result.per_adapter_state["weirdportal"] == HEALTH_FAILED
        evts = [e for e in result.degradation_events if e.code == F_SCOUT_C_02]
        assert any(
            "adapter_returned_unknown_state" in (e.reason_tag or "")
            for e in evts
        )

    def test_outcome_sub_events_propagated(self) -> None:
        @register_portal("subevportal")
        def _fake(ctx: AdapterContext) -> PortalAdapterOutcome:
            return PortalAdapterOutcome(
                candidates=(),
                state=HEALTH_DEGRADED,
                events=(
                    PortalSubEvent(
                        code="F-CUSTOM-01",
                        reason_tag="rt",
                        severity="LOW",
                    ),
                ),
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_c(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            portal_roster=("subevportal",),
            clock=clk,
        )
        custom = [
            e for e in result.degradation_events if e.code == "F-CUSTOM-01"
        ]
        assert len(custom) == 1
        assert custom[0].portal_slug == "subevportal"


# ---------------------------------------------------------------------------
# Coverage gap closure — Channel D
# ---------------------------------------------------------------------------


class TestChannelDCoverageGaps:
    def test_normalize_aln_type_error_on_non_str(self) -> None:
        with pytest.raises(TypeError):
            _normalize_aln(123)  # type: ignore[arg-type]

    def test_non_str_roster_entry_tagged_f_scout_chd_06(self) -> None:
        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=(42,),  # type: ignore[arg-type]
            clock=clk,
        )
        evts = [
            e for e in result.degradation_events if e.code == F_SCOUT_CHD_06
        ]
        assert any(
            "roster_aln_invalid" in (e.reason_tag or "") for e in evts
        )

    def test_duplicate_aln_in_roster_dispatched_once(self) -> None:
        calls: list[int] = []

        @register_program_page("10.055")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            calls.append(1)
            yield ProgramPageOutcome(
                page_candidates=(), page_state=HEALTH_OK
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.055", "10.055", " 10.055 "),
            clock=clk,
        )
        assert len(calls) == 1
        assert len(result.per_adapter_state) == 1

    def test_adapter_call_raises_before_iteration_tagged_chd_04(self) -> None:
        @register_program_page("10.056")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            raise RuntimeError("boom")
            yield  # pragma: no cover

        session, fd, nonce, http, clk = _build_ctx()
        # Channel D wraps the entire adapter lifecycle: because the
        # generator is lazy, the raise fires on first iteration (inside
        # the page loop try/except), which also maps to F-SCOUT-CHD-04.
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.056",),
            clock=clk,
        )
        assert result.per_adapter_state["10.056"] == HEALTH_FAILED
        evts = [
            e for e in result.degradation_events if e.code == F_SCOUT_CHD_04
        ]
        assert len(evts) >= 1

    def test_non_generator_adapter_raise_tagged_chd_04(self) -> None:
        # Non-generator callable that raises synchronously exercises the
        # outer `adapter(ctx)` try/except path (lines 403-417).
        def _raising_adapter(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            raise RuntimeError("outer raise")

        # IMPORTANT: Round 1's test_package_import_runs_under_100ms pops
        # pipeline.scout* from sys.modules and reloads. The test file here
        # bound `discover_channel_d` at module import, so its __globals__
        # points to the pre-reload module's dict. Inject via __globals__
        # so the dispatcher's name lookup sees our adapter.
        reg = discover_channel_d.__globals__["PROGRAM_PAGE_ADAPTERS"]
        reg["10.057"] = _raising_adapter  # type: ignore[assignment]
        try:
            session, fd, nonce, http, clk = _build_ctx()
            result = discover_channel_d(
                session=session,
                fd_broker=fd,
                nonce_registry=nonce,
                http_client=http,
                adapter_roster=("10.057",),
                clock=clk,
            )
            assert result.per_adapter_state["10.057"] == HEALTH_FAILED
            evts = [
                e
                for e in result.degradation_events
                if e.code == F_SCOUT_CHD_04
            ]
            assert len(evts) == 1
            assert "outer raise" in (evts[0].reason_tag or "")
        finally:
            reg.pop("10.057", None)

    def test_adapter_raising_scout_config_error_propagates(self) -> None:
        @register_program_page("10.058")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            raise ScoutConfigError("bad D wiring")
            yield  # pragma: no cover

        session, fd, nonce, http, clk = _build_ctx()
        with pytest.raises(ScoutConfigError):
            discover_channel_d(
                session=session,
                fd_broker=fd,
                nonce_registry=nonce,
                http_client=http,
                adapter_roster=("10.058",),
                clock=clk,
            )

    def test_outer_adapter_call_raises_scout_config_error_propagates(
        self,
    ) -> None:
        # Exercise the OUTER try/except ScoutConfigError re-raise (the
        # `adapter(ctx)` call, not page iteration).
        def _outer_cfg(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            raise ScoutConfigError("outer cfg")

        # See note above — inject via __globals__ to survive Round 1's
        # scout-module reload.
        reg = discover_channel_d.__globals__["PROGRAM_PAGE_ADAPTERS"]
        reg["10.059"] = _outer_cfg  # type: ignore[assignment]
        try:
            session, fd, nonce, http, clk = _build_ctx()
            with pytest.raises(ScoutConfigError):
                discover_channel_d(
                    session=session,
                    fd_broker=fd,
                    nonce_registry=nonce,
                    http_client=http,
                    adapter_roster=("10.059",),
                    clock=clk,
                )
        finally:
            reg.pop("10.059", None)

    def test_page_returning_unknown_state_tagged_chd_05(self) -> None:
        @register_program_page("10.060")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(
                page_candidates=(), page_state="GARBAGE"
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.060",),
            clock=clk,
        )
        assert result.per_adapter_state["10.060"] == HEALTH_FAILED
        evts = [
            e for e in result.degradation_events if e.code == F_SCOUT_CHD_05
        ]
        assert len(evts) == 1

    def test_page_sub_events_propagated(self) -> None:
        @register_program_page("10.061")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(
                page_candidates=(),
                page_state=HEALTH_OK,
                page_events=(
                    ProgramPageSubEvent(
                        code="F-PAGE-CUSTOM",
                        reason_tag="pr",
                        severity="LOW",
                    ),
                ),
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.061",),
            clock=clk,
        )
        custom = [
            e for e in result.degradation_events if e.code == "F-PAGE-CUSTOM"
        ]
        assert len(custom) == 1
        assert custom[0].aln_number == "10.061"

    def test_page_degraded_state_escalates_adapter_degraded(self) -> None:
        @register_program_page("10.062")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(
                page_candidates=(), page_state=HEALTH_DEGRADED
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.062",),
            clock=clk,
        )
        assert result.per_adapter_state["10.062"] == HEALTH_DEGRADED

    def test_remaining_zero_branch_emits_chd_03(self) -> None:
        # Fill to exactly 500 on page 0, then page 1 arrives → `remaining == 0`
        # branch fires with cumulative_overflow = len(page_allowed).
        @register_program_page("10.063")
        def _fake(ctx: AdapterContext) -> Iterator[ProgramPageOutcome]:
            yield ProgramPageOutcome(
                page_candidates=tuple(
                    _make_candidate_d("10.063", f"p0r{i}")
                    for i in range(200)
                ),
                page_state=HEALTH_OK,
            )
            yield ProgramPageOutcome(
                page_candidates=tuple(
                    _make_candidate_d("10.063", f"p1r{i}")
                    for i in range(200)
                ),
                page_state=HEALTH_OK,
            )
            yield ProgramPageOutcome(
                page_candidates=tuple(
                    _make_candidate_d("10.063", f"p2r{i}")
                    for i in range(100)
                ),
                page_state=HEALTH_OK,
            )
            # Page 3 hits `remaining <= 0` branch after 500 accumulated.
            yield ProgramPageOutcome(
                page_candidates=tuple(
                    _make_candidate_d("10.063", f"p3r{i}")
                    for i in range(50)
                ),
                page_state=HEALTH_OK,
            )

        session, fd, nonce, http, clk = _build_ctx()
        result = discover_channel_d(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            http_client=http,
            adapter_roster=("10.063",),
            clock=clk,
        )
        # Exactly 500 candidates after cap.
        assert len(result.candidates) == 500
        # At least one F-SCOUT-CHD-03 emission.
        chd03 = [
            e for e in result.degradation_events if e.code == F_SCOUT_CHD_03
        ]
        assert len(chd03) >= 1

    def test_escalate_state_no_escalation_path(self) -> None:
        # Exercise the `return current` branch in _escalate_state directly.
        from pipeline.scout.channel_d_program_pages import _escalate_state

        assert _escalate_state(HEALTH_FAILED, HEALTH_OK) == HEALTH_FAILED
        assert _escalate_state(HEALTH_DEGRADED, HEALTH_OK) == HEALTH_DEGRADED
        assert _escalate_state(HEALTH_OK, HEALTH_OK) == HEALTH_OK
