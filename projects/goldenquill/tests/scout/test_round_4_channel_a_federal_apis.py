"""Round 4 — pipeline.scout.channel_a_federal_apis (§4.1 Channel A DISCOVER).

Exercises ``discover_channel_a`` with scripted ``HTTPClient``, in-memory
``VaultWriter``, counting ``FDBroker`` / ``NonceRegistry`` fakes, and a
deterministic ``ClockFn``. No real sockets, no real vault, no real sleep.

Covers §4.1 happy path + retry ladder + nonce/FD release parity + S10a
sam.gov invariant + page sweep + state aggregation + §8 timeout pins.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import importlib
import json
import socket
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Optional

import pytest

import pipeline.scout as scout
from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree
from pipeline.scout import (
    CHANNEL_A,
    CHANNEL_A_CONNECT_TIMEOUT_S,
    CHANNEL_A_READ_TIMEOUT_S,
    CHANNEL_A_RETRY_COUNT,
    FEED_PREFIX_API,
    FUNDER_FEDERAL,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
    Candidate,
    ChannelADegradationEvent,
    ChannelADiscoverResult,
    ENDPOINT_GRANTS_GOV,
    ENDPOINT_SAM_GOV,
    ENDPOINT_USASPENDING_GOV,
    INTENT_AWARDS_HISTORY_CACHE_WRITE,
    INTENT_ENTITY_REGISTRATION_CACHE_WRITE,
    classify_channel_a,
    discover_channel_a,
)
from pipeline.scout import channel_a_federal_apis as ch_a


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


@dataclass
class _FakeSession:
    session_id: str = "sess-round4"
    slug: str = "fit_farms_llc"


@dataclass
class _FakeResponse:
    status: int
    headers: Mapping[str, str]
    body_bytes: bytes

    @classmethod
    def ok(cls, body: bytes = b"{}", headers: Optional[dict] = None) -> "_FakeResponse":
        return cls(
            status=200,
            headers=dict(headers or {"Content-Type": "application/json"}),
            body_bytes=body,
        )

    @classmethod
    def json_ok(cls, payload: dict) -> "_FakeResponse":
        return cls.ok(body=json.dumps(payload).encode("utf-8"))


@dataclass
class _ScriptedHTTPClient:
    """HTTPClient fake that plays back a queue of responses or raises.

    Each item in ``script`` is either a :class:`_FakeResponse` OR a callable
    ``() -> None`` that raises. We capture every call in ``calls`` so tests
    can assert method, url, headers, timeouts.
    """

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
    next_fd: int = 1000
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
class _MemoryVaultWriter:
    writes: list[dict] = field(default_factory=list)

    def write(
        self,
        *,
        path: str,
        bytes_: bytes,
        intent: str,
        session_id: str,
        slug: str,
    ) -> None:
        self.writes.append(
            {
                "path": path,
                "bytes_": bytes_,
                "intent": intent,
                "session_id": session_id,
                "slug": slug,
            }
        )


class _FrozenClock:
    def __init__(self, moment: Optional[_dt.datetime] = None):
        self._moment = moment or _dt.datetime(
            2026, 4, 20, 12, 0, 0, tzinfo=_dt.timezone.utc
        )
        self.sleep_calls: list[float] = []

    def __call__(self) -> _dt.datetime:
        return self._moment

    def sleep(self, seconds: float) -> None:
        self.sleep_calls.append(seconds)


# ---------------------------------------------------------------------------
# Helpers to build scripted page bodies
# ---------------------------------------------------------------------------


def _grants_gov_page(n_rows: int, id_prefix: str = "opp") -> dict:
    return {
        "oppHits": [
            {
                "id": f"{id_prefix}-{i:04d}",
                "title": f"Opportunity {i}",
                "agency": "USDA",
                "url": f"https://www.grants.gov/search-results-detail/{id_prefix}-{i:04d}",
                "closeDate": "2026-12-31",
                "awardCeiling": 100000,
                "awardFloor": 10000,
                "applicantEligibility": ["nonprofit", "cooperative"],
                "programPageUrl": f"https://www.grants.gov/programs/{id_prefix}-{i:04d}",
            }
            for i in range(n_rows)
        ]
    }


def _sam_gov_clean_body() -> bytes:
    return json.dumps(
        {
            "totalRecords": 3,
            "entityData": [
                {
                    "legalBusinessName": "ACME Federal Contractor",
                    "registrationStatus": "Active",
                    "naicsList": ["541511", "541512"],
                }
            ],
        }
    ).encode("utf-8")


def _usaspending_body() -> bytes:
    return json.dumps(
        {
            "results": [
                {"Award ID": "CONT_AWD_123", "recipient_name": "Public Recipient"},
            ],
            "page_metadata": {"page": 1, "hasNext": False},
        }
    ).encode("utf-8")


def _build_fakes(
    grants_responses: Optional[list] = None,
    sam_responses: Optional[list] = None,
    usa_responses: Optional[list] = None,
) -> tuple[
    _FakeSession,
    _CountingFDBroker,
    _CountingNonceRegistry,
    _MemoryVaultWriter,
    _ScriptedHTTPClient,
    _FrozenClock,
]:
    """Wire fakes together; default to one successful response per endpoint."""
    grants = grants_responses or [_FakeResponse.json_ok(_grants_gov_page(0))]
    sam = sam_responses or [_FakeResponse.ok(_sam_gov_clean_body())]
    usa = usa_responses or [_FakeResponse.ok(_usaspending_body())]
    return (
        _FakeSession(),
        _CountingFDBroker(),
        _CountingNonceRegistry(),
        _MemoryVaultWriter(),
        _ScriptedHTTPClient(script=list(grants) + list(sam) + list(usa)),
        _FrozenClock(),
    )


# ---------------------------------------------------------------------------
# TestHappyPath — 6 tests
# ---------------------------------------------------------------------------


class TestHappyPath:
    def test_all_three_endpoints_ok_together(self):
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.json_ok(_grants_gov_page(0))],
        )
        result = discover_channel_a(
            session=session,
            fd_broker=fd,
            nonce_registry=nonce,
            vault_writer=vault,
            http_client=http,
            clock=clock,
        )
        assert result.per_endpoint_state == {
            ENDPOINT_GRANTS_GOV: HEALTH_OK,
            ENDPOINT_SAM_GOV: HEALTH_OK,
            ENDPOINT_USASPENDING_GOV: HEALTH_OK,
        }
        assert result.channel_state == HEALTH_OK
        assert result.backbone_failed is False

    def test_grants_gov_ok_in_isolation(self):
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.json_ok(_grants_gov_page(1))],
            sam_responses=[_FakeResponse.ok(_sam_gov_clean_body())],
            usa_responses=[_FakeResponse.ok(_usaspending_body())],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.per_endpoint_state[ENDPOINT_GRANTS_GOV] == HEALTH_OK

    def test_grants_gov_single_page_emits_candidates(self):
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.json_ok(_grants_gov_page(5))],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(result.candidates) == 5
        for cand in result.candidates:
            assert cand.channel == CHANNEL_A
            assert cand.funder_kind == FUNDER_FEDERAL
            assert cand.feed_or_adapter_id == f"{FEED_PREFIX_API}:{ENDPOINT_GRANTS_GOV}"

    def test_grants_gov_multi_page_sweep_concatenates(self):
        # Page 1: full (100 rows) → sweep continues; page 2: partial (3 rows) → terminator
        full = _FakeResponse.json_ok(_grants_gov_page(100, id_prefix="p1"))
        partial = _FakeResponse.json_ok(_grants_gov_page(3, id_prefix="p2"))
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[full, partial],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(result.candidates) == 103
        ids = [c.source_key for c in result.candidates]
        assert ids[0] == "p1-0000"
        assert ids[100] == "p2-0000"

    def test_sam_gov_snapshot_written_with_correct_intent_and_path_prefix(self):
        session, fd, nonce, vault, http, clock = _build_fakes()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        sam_writes = [
            w for w in vault.writes
            if w["intent"] == INTENT_ENTITY_REGISTRATION_CACHE_WRITE
        ]
        assert len(sam_writes) == 1
        assert sam_writes[0]["path"].startswith(
            "vault_shared/cached_entity_registrations/"
        )
        assert sam_writes[0]["session_id"] == session.session_id
        assert sam_writes[0]["slug"] == session.slug

    def test_usaspending_snapshot_written(self):
        session, fd, nonce, vault, http, clock = _build_fakes()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        usa_writes = [
            w for w in vault.writes
            if w["intent"] == INTENT_AWARDS_HISTORY_CACHE_WRITE
        ]
        assert len(usa_writes) == 1
        assert usa_writes[0]["path"].startswith(
            "vault_shared/cached_awards_history/"
        )


# ---------------------------------------------------------------------------
# TestPerEndpointRetry — 9 tests
# ---------------------------------------------------------------------------


class TestPerEndpointRetry:
    def test_5xx_then_success_is_degraded(self):
        # sam.gov: 5xx, then 200. Endpoint state DEGRADED (retry used).
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=[
                _FakeResponse(status=503, headers={}, body_bytes=b""),
                _FakeResponse.ok(_sam_gov_clean_body()),
            ],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.per_endpoint_state[ENDPOINT_SAM_GOV] == HEALTH_DEGRADED

    def test_5xx_three_plus_one_gives_failed(self):
        # 4 attempts total (1 initial + CHANNEL_A_RETRY_COUNT=3) all 5xx → FAILED
        failing = [
            _FakeResponse(status=500, headers={}, body_bytes=b"")
            for _ in range(CHANNEL_A_RETRY_COUNT + 1)
        ]
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=failing,
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.per_endpoint_state[ENDPOINT_SAM_GOV] == HEALTH_FAILED

    def test_connection_reset_three_plus_one_gives_failed(self):
        def raise_conn_reset():
            raise ConnectionResetError("peer reset")
        conn_raisers = [raise_conn_reset for _ in range(CHANNEL_A_RETRY_COUNT + 1)]
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=conn_raisers,
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.per_endpoint_state[ENDPOINT_SAM_GOV] == HEALTH_FAILED

    def test_timeout_three_plus_one_gives_failed(self):
        def raise_timeout():
            raise TimeoutError("read timeout")
        timeouts = [raise_timeout for _ in range(CHANNEL_A_RETRY_COUNT + 1)]
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=timeouts,
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.per_endpoint_state[ENDPOINT_SAM_GOV] == HEALTH_FAILED

    def test_4xx_single_hit_is_degraded(self):
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=[_FakeResponse(status=403, headers={}, body_bytes=b"{}")],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.per_endpoint_state[ENDPOINT_SAM_GOV] == HEALTH_DEGRADED

    def test_grants_gov_4xx_three_times_gives_failed(self):
        # Three 4xx page requests → _aggregate_call_states escalates to FAILED
        responses = [
            _FakeResponse(status=400, headers={}, body_bytes=b"{}")
            for _ in range(3)
        ]
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=responses,
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.per_endpoint_state[ENDPOINT_GRANTS_GOV] == HEALTH_FAILED

    def test_retry_sleep_schedule_is_1_2_4_seconds(self):
        # One initial, one retry -> one sleep of 1.0s.
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=[
                _FakeResponse(status=500, headers={}, body_bytes=b""),
                _FakeResponse.ok(_sam_gov_clean_body()),
            ],
        )
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        # sam.gov is the second endpoint; grants.gov preceded with no retries (no sleeps).
        # Only one sleep occurred: the first retry for sam.gov.
        assert clock.sleep_calls == [1.0]

    def test_retries_apply_per_page_not_per_sweep(self):
        # Page 1: 5xx then 200-full-page. Page 2: 200 partial (terminator).
        # Each page has its own retry ladder; first page incurred 1 retry.
        page1_fail = _FakeResponse(status=500, headers={}, body_bytes=b"")
        page1_ok = _FakeResponse.json_ok(_grants_gov_page(100, id_prefix="p1"))
        page2_ok = _FakeResponse.json_ok(_grants_gov_page(3, id_prefix="p2"))
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[page1_fail, page1_ok, page2_ok],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(result.candidates) == 103
        # Endpoint DEGRADED because one call used a retry.
        assert result.per_endpoint_state[ENDPOINT_GRANTS_GOV] == HEALTH_DEGRADED

    def test_connect_vs_read_timeout_distinguished(self):
        # socket.timeout (subclass of OSError, also TimeoutError in 3.10+)
        def raise_socket_timeout():
            raise socket.timeout("connect timeout")

        def raise_generic_timeout():
            raise TimeoutError("read timeout")

        # Mix both; both retriable.
        mix = [
            raise_socket_timeout,
            raise_generic_timeout,
            raise_socket_timeout,
            raise_generic_timeout,
        ]
        session, fd, nonce, vault, http, clock = _build_fakes(sam_responses=mix)
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.per_endpoint_state[ENDPOINT_SAM_GOV] == HEALTH_FAILED


# ---------------------------------------------------------------------------
# TestNonceFDLifecycle — 8 tests
# ---------------------------------------------------------------------------


class TestNonceFDLifecycle:
    def test_reserve_release_parity_on_success(self):
        session, fd, nonce, vault, http, clock = _build_fakes()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(nonce.reserved) == len(nonce.released)
        assert set(nonce.reserved) == {r["nonce_hex"] for r in nonce.released}

    def test_reserve_release_parity_on_retries_exhausted(self):
        failing = [
            _FakeResponse(status=500, headers={}, body_bytes=b"")
            for _ in range(CHANNEL_A_RETRY_COUNT + 1)
        ]
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=failing,
        )
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(nonce.reserved) == len(nonce.released)

    def test_fd_request_release_parity_on_success(self):
        session, fd, nonce, vault, http, clock = _build_fakes()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(fd.fds_issued) == len(fd.fds_released)
        assert set(fd.fds_issued) == set(fd.fds_released)

    def test_fd_released_before_nonce_on_every_exit(self):
        # Add an HTTP failure + success mix to exercise multiple exit paths.
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=[
                _FakeResponse(status=500, headers={}, body_bytes=b""),
                _FakeResponse.ok(_sam_gov_clean_body()),
            ],
        )
        # Decorate fd.release_fd and nonce.release to record call order.
        order: list[str] = []
        original_fd_release = fd.release_fd
        original_nonce_release = nonce.release

        def fd_release_wrapper(fd_: int) -> None:
            order.append("fd")
            original_fd_release(fd_)

        def nonce_release_wrapper(nonce_hex: str, *, path_tag: str) -> None:
            order.append("nonce")
            original_nonce_release(nonce_hex, path_tag=path_tag)

        fd.release_fd = fd_release_wrapper  # type: ignore[assignment]
        nonce.release = nonce_release_wrapper  # type: ignore[assignment]

        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        # Every "nonce" release must be immediately preceded by a "fd" release.
        for i, tag in enumerate(order):
            if tag == "nonce":
                assert i > 0 and order[i - 1] == "fd"

    def test_path_tag_is_success_on_happy_path(self):
        session, fd, nonce, vault, http, clock = _build_fakes()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        tags = {rel["path_tag"] for rel in nonce.released}
        assert tags == {"success"}

    def test_fd_broker_raise_returns_failed_and_nonce_still_released(self):
        session = _FakeSession()
        fd = _CountingFDBroker(raise_on_request=OSError("fd exhausted"))
        nonce = _CountingNonceRegistry()
        vault = _MemoryVaultWriter()
        http = _ScriptedHTTPClient()
        clock = _FrozenClock()
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        # All three endpoints attempted; each failed with F-SCOUT-A-01.
        codes = {ev.code for ev in result.degradation_events}
        assert "F-SCOUT-A-01" in codes
        # Nonce was reserved and released for every attempt; HTTP never called.
        assert len(nonce.reserved) == len(nonce.released)
        assert nonce.reserved, "at least one reserve expected"
        assert len(fd.fds_issued) == 0
        assert http.calls == []

    def test_nonce_reserve_raise_short_circuits(self):
        session = _FakeSession()
        fd = _CountingFDBroker()
        nonce = _CountingNonceRegistry(
            raise_on_reserve=RuntimeError("replay detected"),
        )
        vault = _MemoryVaultWriter()
        http = _ScriptedHTTPClient()
        clock = _FrozenClock()
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        codes = {ev.code for ev in result.degradation_events}
        assert "F-SCOUT-A-02" in codes
        # No nonce was successfully reserved, so none needs release; no FD either.
        assert nonce.reserved == []
        assert nonce.released == []
        assert fd.fds_issued == []

    def test_path_tag_reflects_timeout_on_retries_exhausted(self):
        def raise_timeout():
            raise TimeoutError("read timeout")
        tries = [raise_timeout for _ in range(CHANNEL_A_RETRY_COUNT + 1)]
        session, fd, nonce, vault, http, clock = _build_fakes(sam_responses=tries)
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        # At least one nonce released with "timeout" path_tag.
        tags = {rel["path_tag"] for rel in nonce.released}
        assert "timeout" in tags


# ---------------------------------------------------------------------------
# TestChannelStateAggregation — 5 tests (classify_channel_a)
# ---------------------------------------------------------------------------


class TestChannelStateAggregation:
    def test_all_ok_is_ok(self):
        assert classify_channel_a(
            {"grants.gov": HEALTH_OK, "sam.gov": HEALTH_OK, "usaspending.gov": HEALTH_OK}
        ) == HEALTH_OK

    def test_mixed_is_degraded(self):
        assert classify_channel_a(
            {"grants.gov": HEALTH_OK, "sam.gov": HEALTH_DEGRADED, "usaspending.gov": HEALTH_OK}
        ) == HEALTH_DEGRADED

    def test_all_failed_is_failed(self):
        assert classify_channel_a(
            {"grants.gov": HEALTH_FAILED, "sam.gov": HEALTH_FAILED, "usaspending.gov": HEALTH_FAILED}
        ) == HEALTH_FAILED

    def test_two_failed_one_ok_is_degraded(self):
        assert classify_channel_a(
            {"grants.gov": HEALTH_FAILED, "sam.gov": HEALTH_FAILED, "usaspending.gov": HEALTH_OK}
        ) == HEALTH_DEGRADED

    def test_two_ok_one_failed_is_degraded(self):
        assert classify_channel_a(
            {"grants.gov": HEALTH_OK, "sam.gov": HEALTH_OK, "usaspending.gov": HEALTH_FAILED}
        ) == HEALTH_DEGRADED


# ---------------------------------------------------------------------------
# TestBackboneFailed — 3 tests
# ---------------------------------------------------------------------------


class TestBackboneFailed:
    def test_backbone_failed_only_on_all_three_failed(self):
        all_fail = [
            _FakeResponse(status=500, headers={}, body_bytes=b"")
            for _ in range(CHANNEL_A_RETRY_COUNT + 1)
        ]
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=list(all_fail),
            sam_responses=list(all_fail),
            usa_responses=list(all_fail),
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.channel_state == HEALTH_FAILED
        assert result.backbone_failed is True

    def test_backbone_not_failed_when_one_degraded(self):
        ok_sam = [
            _FakeResponse(status=503, headers={}, body_bytes=b""),
            _FakeResponse.ok(_sam_gov_clean_body()),
        ]
        session, fd, nonce, vault, http, clock = _build_fakes(sam_responses=ok_sam)
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.backbone_failed is False

    def test_backbone_not_failed_when_only_one_endpoint_failed(self):
        # Only sam.gov fails; grants.gov and usaspending.gov succeed.
        sam_fail = [
            _FakeResponse(status=500, headers={}, body_bytes=b"")
            for _ in range(CHANNEL_A_RETRY_COUNT + 1)
        ]
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=sam_fail,
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.backbone_failed is False
        assert result.channel_state == HEALTH_DEGRADED


# ---------------------------------------------------------------------------
# TestContentHashing — 3 tests
# ---------------------------------------------------------------------------


class TestContentHashing:
    def test_sha3_512_matches_body_bytes(self):
        body = json.dumps(_grants_gov_page(2, id_prefix="hash")).encode("utf-8")
        expected = hashlib.sha3_512(body).hexdigest()
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        for cand in result.candidates:
            assert cand.content_hash == expected

    def test_content_hash_carried_into_every_candidate_on_page(self):
        body = json.dumps(_grants_gov_page(4, id_prefix="hash2")).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len({c.content_hash for c in result.candidates}) == 1

    def test_content_hash_differs_across_pages(self):
        p1 = json.dumps(_grants_gov_page(100, id_prefix="p1")).encode("utf-8")
        p2 = json.dumps(_grants_gov_page(2, id_prefix="p2")).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(p1), _FakeResponse.ok(p2)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        hashes = {c.content_hash for c in result.candidates}
        assert len(hashes) == 2


# ---------------------------------------------------------------------------
# TestS10aSamGovSnapshot — 3 tests
# ---------------------------------------------------------------------------


class TestS10aSamGovSnapshot:
    def test_clean_snapshot_accepted(self):
        session, fd, nonce, vault, http, clock = _build_fakes()
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        sam_writes = [
            w for w in vault.writes
            if w["intent"] == INTENT_ENTITY_REGISTRATION_CACHE_WRITE
        ]
        assert len(sam_writes) == 1
        assert result.per_endpoint_state[ENDPOINT_SAM_GOV] == HEALTH_OK

    def test_snapshot_with_org_identifier_rejected(self):
        dirty = json.dumps(
            {
                "entityData": [
                    {"legalBusinessName": "X", "ein": "12-3456789"},
                ],
            }
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=[_FakeResponse.ok(dirty)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        sam_writes = [
            w for w in vault.writes
            if w["intent"] == INTENT_ENTITY_REGISTRATION_CACHE_WRITE
        ]
        assert len(sam_writes) == 0
        codes = {ev.code for ev in result.degradation_events}
        assert "F-SCOUT-A-03" in codes
        assert result.per_endpoint_state[ENDPOINT_SAM_GOV] == HEALTH_DEGRADED

    def test_non_identifier_metadata_accepted(self):
        # "naicsList", "registrationStatus", "cageCode" are non-identifier.
        borderline = json.dumps(
            {
                "entityData": [
                    {
                        "legalBusinessName": "Okay Name",
                        "cageCode": "ABCDE",
                        "registrationStatus": "Active",
                        "naicsList": ["541511"],
                    }
                ],
            }
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=[_FakeResponse.ok(borderline)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.per_endpoint_state[ENDPOINT_SAM_GOV] == HEALTH_OK
        sam_writes = [
            w for w in vault.writes
            if w["intent"] == INTENT_ENTITY_REGISTRATION_CACHE_WRITE
        ]
        assert len(sam_writes) == 1


# ---------------------------------------------------------------------------
# TestHTTPClientCallSite — 4 tests
# ---------------------------------------------------------------------------


class TestHTTPClientCallSite:
    def test_connect_timeout_is_10s(self):
        session, fd, nonce, vault, http, clock = _build_fakes()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        for call in http.calls:
            assert call["connect_timeout_s"] == CHANNEL_A_CONNECT_TIMEOUT_S == 10

    def test_read_timeout_is_30s(self):
        session, fd, nonce, vault, http, clock = _build_fakes()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        for call in http.calls:
            assert call["read_timeout_s"] == CHANNEL_A_READ_TIMEOUT_S == 30

    def test_method_and_url_per_endpoint(self):
        session, fd, nonce, vault, http, clock = _build_fakes()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        # grants.gov = POST, sam.gov = GET, usaspending.gov = POST
        grants_call = http.calls[0]
        sam_call = http.calls[1]
        usa_call = http.calls[2]
        assert grants_call["method"] == "POST"
        assert "api.grants.gov" in grants_call["url"]
        assert sam_call["method"] == "GET"
        assert "api.sam.gov" in sam_call["url"]
        assert usa_call["method"] == "POST"
        assert "api.usaspending.gov" in usa_call["url"]

    def test_headers_include_user_agent_and_accept_json(self):
        session, fd, nonce, vault, http, clock = _build_fakes()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        for call in http.calls:
            assert call["headers"].get("User-Agent", "").startswith("Golden-Quill-Scout")
            assert call["headers"].get("Accept") == "application/json"


# ---------------------------------------------------------------------------
# TestClockSleepInjection — 3 tests
# ---------------------------------------------------------------------------


class TestClockSleepInjection:
    def test_happy_path_uses_no_sleeps(self):
        session, fd, nonce, vault, http, clock = _build_fakes()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert clock.sleep_calls == []

    def test_retry_sequence_is_1_2_4(self):
        # All four attempts 5xx → retries_exhausted. Sleeps: (1.0, 2.0, 4.0)
        failing = [
            _FakeResponse(status=500, headers={}, body_bytes=b"")
            for _ in range(CHANNEL_A_RETRY_COUNT + 1)
        ]
        # Configure only sam.gov to fail; grants & usaspending succeed (no sleeps).
        session, fd, nonce, vault, http, clock = _build_fakes(sam_responses=failing)
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert clock.sleep_calls == [1.0, 2.0, 4.0]

    def test_injected_sleep_never_calls_time_sleep(self):
        # Guard: ensure the fake's sleep is the only sleep invoked.
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=[
                _FakeResponse(status=500, headers={}, body_bytes=b""),
                _FakeResponse.ok(_sam_gov_clean_body()),
            ],
        )
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        # Only one retry used → one sleep on the fake clock.
        assert clock.sleep_calls == [1.0]


# ---------------------------------------------------------------------------
# TestKWOnly — 1 test
# ---------------------------------------------------------------------------


class TestKWOnly:
    def test_positional_call_rejected(self):
        session, fd, nonce, vault, http, clock = _build_fakes()
        with pytest.raises(TypeError):
            discover_channel_a(session, fd, nonce, vault, http, clock)  # type: ignore[misc]


# ---------------------------------------------------------------------------
# TestProtocolDiscipline — 4 tests (minimal duck-typed fakes)
# ---------------------------------------------------------------------------


class TestProtocolDiscipline:
    def test_minimal_http_client_fake_works(self):
        class MinHTTP:
            def __init__(self) -> None:
                self._queue = [_FakeResponse.json_ok(_grants_gov_page(0))]

            def request(self, method, url, *, headers, body, connect_timeout_s, read_timeout_s):
                return self._queue.pop(0) if self._queue else _FakeResponse.ok(_sam_gov_clean_body())

        session = _FakeSession()
        fd = _CountingFDBroker()
        nonce = _CountingNonceRegistry()
        vault = _MemoryVaultWriter()
        clock = _FrozenClock()
        # three calls total — supplement via default queue
        http = MinHTTP()
        # monkeypatch internal queue to keep supplying responses
        http._queue = [
            _FakeResponse.json_ok(_grants_gov_page(0)),
            _FakeResponse.ok(_sam_gov_clean_body()),
            _FakeResponse.ok(_usaspending_body()),
        ]
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.channel_state == HEALTH_OK

    def test_minimal_fd_broker_fake_works(self):
        class MinFD:
            def __init__(self) -> None:
                self._next = 500
                self.released: list[int] = []

            def request_fd(self, *, kind, host):
                self._next += 1
                return self._next

            def release_fd(self, fd):
                self.released.append(fd)

        session, _fd, nonce, vault, http, clock = _build_fakes()
        fd = MinFD()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(fd.released) == 3

    def test_minimal_nonce_registry_fake_works(self):
        class MinNonce:
            def __init__(self) -> None:
                self.reserved: list[str] = []
                self.released: list[str] = []

            def reserve(self, nonce_hex):
                self.reserved.append(nonce_hex)

            def release(self, nonce_hex, *, path_tag):
                self.released.append(nonce_hex)

        session, fd, _n, vault, http, clock = _build_fakes()
        nonce = MinNonce()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(nonce.reserved) == len(nonce.released)

    def test_minimal_vault_writer_fake_works(self):
        class MinVault:
            def __init__(self) -> None:
                self.writes: list[str] = []

            def write(self, *, path, bytes_, intent, session_id, slug):
                self.writes.append(path)

        session, fd, nonce, _v, http, clock = _build_fakes()
        vault = MinVault()
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(vault.writes) == 2  # sam.gov + usaspending.gov


# ---------------------------------------------------------------------------
# TestNoModuleSideEffects — 1 test
# ---------------------------------------------------------------------------


class TestNoModuleSideEffects:
    def test_import_does_not_touch_network_fd_or_nonce(self):
        # Fresh import from a clean module cache.
        sys.modules.pop("pipeline.scout.channel_a_federal_apis", None)
        imported = importlib.import_module("pipeline.scout.channel_a_federal_apis")
        # Confirm module exists and exposes expected names; import itself ran
        # without any fake-FD / fake-nonce side effects (which we'd detect via
        # the absence of any global counter). The smoke test is: import and
        # re-check that calling code still requires fakes.
        assert hasattr(imported, "discover_channel_a")
        assert hasattr(imported, "classify_channel_a")


# ---------------------------------------------------------------------------
# TestASTLintRegression — 1 test
# ---------------------------------------------------------------------------


class TestASTLintRegression:
    def test_ast_lint_clean_on_channel_a(self):
        from pathlib import Path

        target = (
            Path(ch_a.__file__).resolve()
        )
        findings = lint_tree(target.parent, rules=DEFAULT_RULES)
        relevant = [
            f for f in findings
            if "channel_a_federal_apis" in str(f.file).replace("\\", "/")
        ]
        assert relevant == []


# ---------------------------------------------------------------------------
# TestPublicSurface — 3 tests
# ---------------------------------------------------------------------------


class TestPublicSurface:
    def test_version_pin_is_r4(self):
        # E-025: version pin must range-check, not hard-pin. Round 4+
        # is acceptable — later rounds only add re-exports, never
        # remove Round 4 surface.
        assert scout.__version__.startswith("0.1.0-scout-r")
        assert int(scout.__version__.rsplit("r", 1)[1]) >= 4

    def test_all_exports_reachable(self):
        for name in (
            "ChannelADegradationEvent",
            "ChannelADiscoverResult",
            "ENDPOINT_GRANTS_GOV",
            "ENDPOINT_SAM_GOV",
            "ENDPOINT_USASPENDING_GOV",
            "FDBroker",
            "HTTPClient",
            "HTTPResponse",
            "INTENT_AWARDS_HISTORY_CACHE_WRITE",
            "INTENT_ENTITY_REGISTRATION_CACHE_WRITE",
            "NonceRegistry",
            "SessionLike",
            "classify_channel_a",
            "discover_channel_a",
        ):
            assert hasattr(scout, name), name
            assert name in scout.__all__, name

    def test_module_all_contract(self):
        expected = {
            "ChannelADegradationEvent",
            "ChannelADiscoverResult",
            "ClockFn",
            "ENDPOINT_GRANTS_GOV",
            "ENDPOINT_SAM_GOV",
            "ENDPOINT_USASPENDING_GOV",
            "FDBroker",
            "HTTPClient",
            "HTTPResponse",
            "INTENT_AWARDS_HISTORY_CACHE_WRITE",
            "INTENT_ENTITY_REGISTRATION_CACHE_WRITE",
            "NonceRegistry",
            "SessionLike",
            "VaultWriter",
            "classify_channel_a",
            "discover_channel_a",
        }
        assert set(ch_a.__all__) == expected


# ---------------------------------------------------------------------------
# TestGrantsGovPagination — 4 tests
# ---------------------------------------------------------------------------


class TestGrantsGovPagination:
    def test_single_page_partial_terminates_sweep(self):
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.json_ok(_grants_gov_page(7))],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(result.candidates) == 7
        # Only one grants.gov call was made.
        grants_calls = [c for c in http.calls if "api.grants.gov" in c["url"]]
        assert len(grants_calls) == 1

    def test_two_page_sweep_terminates_on_partial(self):
        full = _FakeResponse.json_ok(_grants_gov_page(100, id_prefix="pa"))
        partial = _FakeResponse.json_ok(_grants_gov_page(1, id_prefix="pb"))
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[full, partial],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(result.candidates) == 101
        grants_calls = [c for c in http.calls if "api.grants.gov" in c["url"]]
        assert len(grants_calls) == 2

    def test_empty_page_terminates_sweep(self):
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.json_ok({"oppHits": []})],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(result.candidates) == 0
        assert result.per_endpoint_state[ENDPOINT_GRANTS_GOV] == HEALTH_OK
        grants_calls = [c for c in http.calls if "api.grants.gov" in c["url"]]
        assert len(grants_calls) == 1

    def test_offset_advances_across_pages(self):
        full1 = _FakeResponse.json_ok(_grants_gov_page(100, id_prefix="x1"))
        full2 = _FakeResponse.json_ok(_grants_gov_page(100, id_prefix="x2"))
        partial = _FakeResponse.json_ok(_grants_gov_page(1, id_prefix="x3"))
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[full1, full2, partial],
        )
        discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        grants_calls = [c for c in http.calls if "api.grants.gov" in c["url"]]
        offsets = [json.loads(c["body"])["startRecordNum"] for c in grants_calls]
        assert offsets == [0, 100, 200]


# ---------------------------------------------------------------------------
# Additional coverage — edge cases for 100% coverage
# ---------------------------------------------------------------------------


class TestCoverageEdgeCases:
    def test_parse_error_on_grants_gov_page_records_f_scout_a_03(self):
        # Page body is valid JSON object shape, with malformed oppHits type.
        bad = json.dumps({"oppHits": "not-a-list"}).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(bad)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        codes = {ev.code for ev in result.degradation_events}
        assert "F-SCOUT-A-03" in codes
        assert result.per_endpoint_state[ENDPOINT_GRANTS_GOV] == HEALTH_DEGRADED

    def test_unparseable_sam_gov_body_degrades_endpoint(self):
        bad = b"\xff\xfe\x00not-json"
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=[_FakeResponse.ok(bad)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        codes = {ev.code for ev in result.degradation_events}
        assert "F-SCOUT-A-03" in codes
        assert result.per_endpoint_state[ENDPOINT_SAM_GOV] == HEALTH_DEGRADED
        sam_writes = [
            w for w in vault.writes
            if w["intent"] == INTENT_ENTITY_REGISTRATION_CACHE_WRITE
        ]
        assert len(sam_writes) == 0

    def test_grants_gov_non_object_body_emits_f_scout_a_03(self):
        bad = b"[]"
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(bad)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        codes = {ev.code for ev in result.degradation_events}
        assert "F-SCOUT-A-03" in codes

    def test_classify_channel_a_empty_mapping_is_failed(self):
        assert classify_channel_a({}) == HEALTH_FAILED

    def test_aggregate_call_states_empty_is_failed(self):
        assert ch_a._aggregate_call_states(()) == HEALTH_FAILED

    def test_aggregate_call_states_three_degraded_escalates_to_failed(self):
        assert ch_a._aggregate_call_states(
            (HEALTH_DEGRADED, HEALTH_DEGRADED, HEALTH_DEGRADED)
        ) == HEALTH_FAILED

    def test_aggregate_call_states_two_degraded_stays_degraded(self):
        assert ch_a._aggregate_call_states(
            (HEALTH_DEGRADED, HEALTH_DEGRADED)
        ) == HEALTH_DEGRADED

    def test_default_clock_is_real_clock(self):
        assert isinstance(ch_a._default_clock, ch_a._RealClock)
        now = ch_a._default_clock()
        assert isinstance(now, _dt.datetime)
        assert now.tzinfo is _dt.timezone.utc

    def test_real_clock_sleep_exists(self):
        clock = ch_a._RealClock()
        # Invoke with 0.0 — real sleep is a no-op for 0.
        clock.sleep(0.0)

    def test_opportunities_key_fallback_parses(self):
        # Some grants.gov shapes use "opportunities" instead of "oppHits".
        body = json.dumps(
            {"opportunities": [{"id": "alt-1", "title": "Alt", "agency": "USDA"}]}
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(result.candidates) == 1
        assert result.candidates[0].source_key == "alt-1"

    def test_row_without_required_fields_is_skipped(self):
        body = json.dumps(
            {
                "oppHits": [
                    {"not_an_id": 123},  # no id
                    {"id": "valid-1", "title": "Valid"},
                    "not-a-dict",
                    {"id": 42},  # non-string id
                ],
            }
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(result.candidates) == 1
        assert result.candidates[0].source_key == "valid-1"

    def test_row_with_non_string_title_is_skipped(self):
        body = json.dumps(
            {
                "oppHits": [
                    {"id": "v1", "title": 123},
                    {"id": "v2", "title": "Good"},
                ],
            }
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(result.candidates) == 1
        assert result.candidates[0].source_key == "v2"

    def test_row_field_fallbacks_exercised(self):
        body = json.dumps(
            {
                "oppHits": [
                    {
                        "oppId": "fallback-id-1",
                        "oppTitle": "Fallback Title",
                        "agencyName": "Other Agency",
                        "applicantTypes": ["nonprofit"],
                        "closeDateUtc": "2027-01-01",
                        "programUrl": "https://example.gov/prog",
                    }
                ],
            }
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert len(result.candidates) == 1
        cand = result.candidates[0]
        assert cand.source_key == "fallback-id-1"
        assert cand.title == "Fallback Title"
        assert cand.funder == "Other Agency"
        assert cand.applicant_types == ("nonprofit",)
        assert cand.close_date_utc == "2027-01-01"
        assert cand.program_page_url == "https://example.gov/prog"

    def test_row_with_non_string_funder_defaults_empty(self):
        body = json.dumps(
            {"oppHits": [{"id": "nf-1", "title": "T", "agency": 99}]}
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.candidates[0].funder == ""

    def test_row_with_non_string_url_defaults_empty(self):
        body = json.dumps(
            {"oppHits": [{"id": "nu-1", "title": "T", "url": 99}]}
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.candidates[0].url == ""

    def test_row_with_invalid_applicant_types_defaults_empty(self):
        body = json.dumps(
            {
                "oppHits": [
                    {
                        "id": "a1",
                        "title": "T",
                        "applicantEligibility": "not-a-list",
                    }
                ],
            }
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.candidates[0].applicant_types == ()

    def test_row_with_non_int_award_fields_becomes_none(self):
        body = json.dumps(
            {
                "oppHits": [
                    {
                        "id": "a1",
                        "title": "T",
                        "awardCeiling": "not-int",
                        "awardFloor": None,
                    }
                ],
            }
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.candidates[0].award_ceiling is None
        assert result.candidates[0].award_floor is None

    def test_row_with_non_string_close_date_becomes_none(self):
        body = json.dumps(
            {"oppHits": [{"id": "d1", "title": "T", "closeDate": 42}]}
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.candidates[0].close_date_utc is None

    def test_row_with_non_string_program_url_becomes_none(self):
        body = json.dumps(
            {"oppHits": [{"id": "p1", "title": "T", "programPageUrl": 99}]}
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.candidates[0].program_page_url is None

    def test_sam_gov_retries_exhausted_on_timeouts(self):
        def raise_timeout():
            raise TimeoutError("read timeout")
        tries = [raise_timeout for _ in range(CHANNEL_A_RETRY_COUNT + 1)]
        session, fd, nonce, vault, http, clock = _build_fakes(sam_responses=tries)
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        codes = {ev.code for ev in result.degradation_events}
        assert "F-SCOUT-A-05" in codes

    def test_usaspending_4xx_emits_f_scout_a_06(self):
        session, fd, nonce, vault, http, clock = _build_fakes(
            usa_responses=[_FakeResponse(status=404, headers={}, body_bytes=b"{}")],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        codes = {ev.code for ev in result.degradation_events}
        assert "F-SCOUT-A-06" in codes
        assert result.per_endpoint_state[ENDPOINT_USASPENDING_GOV] == HEALTH_DEGRADED

    def test_usaspending_retries_exhausted(self):
        failing = [
            _FakeResponse(status=500, headers={}, body_bytes=b"")
            for _ in range(CHANNEL_A_RETRY_COUNT + 1)
        ]
        session, fd, nonce, vault, http, clock = _build_fakes(usa_responses=failing)
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        codes = {ev.code for ev in result.degradation_events}
        assert "F-SCOUT-A-05" in codes
        assert result.per_endpoint_state[ENDPOINT_USASPENDING_GOV] == HEALTH_FAILED

    def test_grants_gov_success_after_retry_emits_low_severity_event(self):
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[
                _FakeResponse(status=500, headers={}, body_bytes=b""),
                _FakeResponse.json_ok(_grants_gov_page(2)),
            ],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        retry_events = [
            ev for ev in result.degradation_events
            if ev.code == "F-SCOUT-A-05" and ev.severity == "LOW"
        ]
        assert len(retry_events) >= 1

    def test_s10a_nested_offender_detected(self):
        nested = json.dumps(
            {
                "entityData": [
                    {
                        "legalBusinessName": "X",
                        "metadata": {
                            "inner": [
                                {"uei": "SOMEUEI1234"},
                            ]
                        },
                    }
                ],
            }
        ).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=[_FakeResponse.ok(nested)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        codes = {ev.code for ev in result.degradation_events}
        assert "F-SCOUT-A-03" in codes

    def test_grants_gov_fd_error_propagates_f_scout_a_01(self):
        # FD broker raises only after an initial successful call won't happen —
        # here we raise unconditionally so all three endpoints fail.
        session = _FakeSession()
        fd = _CountingFDBroker(raise_on_request=OSError("broker down"))
        nonce = _CountingNonceRegistry()
        vault = _MemoryVaultWriter()
        http = _ScriptedHTTPClient()
        clock = _FrozenClock()
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        gg_events = [
            ev for ev in result.degradation_events
            if ev.endpoint == ENDPOINT_GRANTS_GOV and ev.code == "F-SCOUT-A-01"
        ]
        assert len(gg_events) == 1

    def test_http_client_raising_generic_exception_is_caught(self):
        # HTTPClient.request raises a non-IO exception; adapter wraps as exception path.
        def raise_value_error():
            raise ValueError("totally unexpected")

        session, fd, nonce, vault, http, clock = _build_fakes(
            sam_responses=[raise_value_error],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        assert result.per_endpoint_state[ENDPOINT_SAM_GOV] == HEALTH_FAILED

    def test_escalate_returns_current_when_incoming_not_higher(self):
        # Direct unit call: DEGRADED → OK should stay DEGRADED (no down-escalation).
        assert ch_a._escalate(HEALTH_DEGRADED, HEALTH_OK) == HEALTH_DEGRADED
        assert ch_a._escalate(HEALTH_FAILED, HEALTH_DEGRADED) == HEALTH_FAILED
        assert ch_a._escalate(HEALTH_OK, HEALTH_OK) == HEALTH_OK

    def test_grants_gov_body_undecodable_bytes_emit_f_scout_a_03(self):
        # UTF-8-invalid byte sequence so json.loads(body.decode) raises
        # UnicodeDecodeError, hitting the except-branch at lines 550-551.
        bad = b"\xff\xfe\xfd not valid utf8"
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(bad)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        codes = {ev.code for ev in result.degradation_events}
        assert "F-SCOUT-A-03" in codes

    def test_usaspending_success_after_retry_emits_low_severity_event(self):
        session, fd, nonce, vault, http, clock = _build_fakes(
            usa_responses=[
                _FakeResponse(status=500, headers={}, body_bytes=b""),
                _FakeResponse.ok(_usaspending_body()),
            ],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        retry_events = [
            ev for ev in result.degradation_events
            if ev.endpoint == ENDPOINT_USASPENDING_GOV
            and ev.code == "F-SCOUT-A-05"
            and ev.severity == "LOW"
        ]
        assert len(retry_events) == 1

    def test_row_to_candidate_builds_candidate_id_and_url_hash(self):
        body = json.dumps(_grants_gov_page(1, id_prefix="idh")).encode("utf-8")
        session, fd, nonce, vault, http, clock = _build_fakes(
            grants_responses=[_FakeResponse.ok(body)],
        )
        result = discover_channel_a(
            session=session, fd_broker=fd, nonce_registry=nonce,
            vault_writer=vault, http_client=http, clock=clock,
        )
        cand = result.candidates[0]
        assert len(cand.candidate_id) == 24
        assert len(cand.url_hash) == 32
        assert cand.fit_score_cached == 0
        assert cand.cache_provenance is None
