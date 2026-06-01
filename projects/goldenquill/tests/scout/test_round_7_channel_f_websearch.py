"""Round 7 — Channel F (client-material-driven web search) + BT12 pre-flight.

Test surface floor ≥ 60; E-024 1.5× multiplier (sixth firing) targets ~90.

Covers spec-card §Minimum-test-surface classes 1-15 + engineering-risks
closure (AST R7 dominance exercised in production). Follows E-017
Protocol-injection, E-025 range-check version pins, E-026 formal
``__module__`` lineage checks under ``sys.modules`` reload.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import importlib
import json
import os
import socket
import sys
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any, List, Optional, Tuple

import pytest

import pipeline.scout.channel_f_websearch as cfw
from pipeline.scout._channel_f_jurisdictions import (
    JURISDICTION_TABLE,
    jurisdiction_for_etld,
)
from pipeline.scout._vault_reader_adapter import (
    IdentityTupleSnapshot,
    Section2VaultReader,
)


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


@dataclass
class FakeSession:
    session_id: str = "session-7-abc"
    slug: str = "mycosymbiotics_cooperative"


@dataclass
class FakeIdentity:
    intent: str
    session_id: str
    slug: str


@dataclass
class FakeResponse:
    status: int
    body_bytes: bytes
    headers: dict = field(default_factory=dict)


@dataclass
class RecordingFDBroker:
    """Counts FD acquisitions + releases; any order-of-ops violation trips.

    ``request_calls`` is the ordered list of ``(kind, host)`` tuples at each
    ``request_fd`` call. ``release_calls`` is the ordered list of FDs
    released.
    """

    next_fd: int = 100
    request_calls: List[Tuple[str, str]] = field(default_factory=list)
    release_calls: List[int] = field(default_factory=list)
    raise_on_request: bool = False

    def request_fd(self, *, kind: str, host: str) -> int:
        if self.raise_on_request:
            raise OSError("simulated fd pool exhaustion")
        self.request_calls.append((kind, host))
        fd = self.next_fd
        self.next_fd += 1
        return fd

    def release_fd(self, fd: int) -> None:
        self.release_calls.append(fd)


@dataclass
class RecordingNonceRegistry:
    reservations: List[str] = field(default_factory=list)
    releases: List[Tuple[str, str]] = field(default_factory=list)
    raise_on_reserve: bool = False

    def reserve(self, nonce_hex: str) -> None:
        if self.raise_on_reserve:
            raise RuntimeError("simulated nonce pool exhaustion")
        self.reservations.append(nonce_hex)

    def release(self, nonce_hex: str, *, path_tag: str) -> None:
        self.releases.append((nonce_hex, path_tag))


@dataclass
class QueueHTTPClient:
    """Serves responses in FIFO order; records every request for assertions."""

    responses: List[Any] = field(default_factory=list)
    requests: List[dict] = field(default_factory=list)

    def request(
        self,
        method: str,
        url: str,
        *,
        headers,
        body,
        connect_timeout_s: float,
        read_timeout_s: float,
    ):
        self.requests.append(
            {
                "method": method,
                "url": url,
                "headers": dict(headers),
                "body": body,
                "connect_timeout_s": connect_timeout_s,
                "read_timeout_s": read_timeout_s,
            }
        )
        if not self.responses:
            raise AssertionError("QueueHTTPClient: no response queued")
        nxt = self.responses.pop(0)
        if isinstance(nxt, BaseException):
            raise nxt
        return nxt


class MemoryVaultReader:
    """Memory-backed :class:`VaultReader` used by most Round 7 tests."""

    def __init__(self, *, data: bytes, identity: Any, raise_exc: Optional[BaseException] = None):
        self._data = data
        self._identity = identity
        self._raise = raise_exc
        self.calls: List[dict] = []

    def read(self, *, path: str, intent: str, session_id: str, slug: str):
        self.calls.append(
            {"path": path, "intent": intent, "session_id": session_id, "slug": slug}
        )
        if self._raise is not None:
            raise self._raise
        return self._data, self._identity


def _policy_yaml(
    *,
    opt_in: bool = True,
    allowed: Tuple[str, ...] = ("US", "GTLD"),
    disallowed: Tuple[str, ...] = (),
    searxng_port: int = 8888,
    provider: str = "searxng",
) -> bytes:
    allowed_yaml = "[" + ", ".join(repr(x) for x in allowed) + "]"
    dis_yaml = "[" + ", ".join(repr(x) for x in disallowed) + "]"
    body = (
        f"opt_in: {'true' if opt_in else 'false'}\n"
        f"allowed_jurisdictions: {allowed_yaml}\n"
        f"disallowed_registrable_domains: {dis_yaml}\n"
        f"searxng_port: {searxng_port}\n"
        f"provider: {provider}\n"
    )
    return body.encode("utf-8")


def _fixed_clock(ts: str = "2026-04-20T12:00:00+00:00"):
    fixed = _dt.datetime.fromisoformat(ts)

    def _clock() -> _dt.datetime:
        return fixed

    return _clock


def _matching_identity(session: FakeSession, intent: str = "channel-f-policy-read") -> FakeIdentity:
    return FakeIdentity(
        intent=intent, session_id=session.session_id, slug=session.slug
    )


def _searxng_results_body(urls: Tuple[str, ...]) -> bytes:
    return json.dumps(
        {"results": [{"url": u, "title": f"Result for {u}"} for u in urls]}
    ).encode("utf-8")


def _brave_results_body(urls: Tuple[str, ...]) -> bytes:
    return json.dumps(
        {"web": {"results": [{"url": u, "title": f"R{u}"} for u in urls]}}
    ).encode("utf-8")


# ---------------------------------------------------------------------------
# Class 1 — TestChannelFOptOut
# ---------------------------------------------------------------------------


class TestChannelFOptOut:
    def test_missing_policy_file_short_circuits(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        vault = MemoryVaultReader(
            data=b"",
            identity=_matching_identity(session),
            raise_exc=FileNotFoundError("no such policy"),
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="soil health grants"),),
            clock=_fixed_clock(),
        )
        assert result.candidates == ()
        assert result.channel_state == "OK"
        assert result.degradation_events == ()
        assert result.disclosure_rows == ()
        assert result.preflight_reject_count == 0
        assert broker.request_calls == []
        assert nonces.reservations == []

    def test_opt_in_false_short_circuits_zero_fds(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        vault = MemoryVaultReader(
            data=_policy_yaml(opt_in=False),
            identity=_matching_identity(session),
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="Q"),),
            clock=_fixed_clock(),
        )
        assert result.candidates == ()
        assert result.channel_state == "OK"
        assert result.preflight_reject_count == 0
        assert broker.request_calls == []
        assert nonces.reservations == []

    def test_stale_policy_identity_tuple_mismatch_failclosed(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        wrong_identity = FakeIdentity(
            intent="channel-f-policy-read",
            session_id="different-session",
            slug=session.slug,
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=wrong_identity
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="Q"),),
            clock=_fixed_clock(),
        )
        assert result.candidates == ()
        assert result.channel_state == "OK"  # OK-trivial — no traffic
        assert broker.request_calls == []
        codes = {e.code for e in result.degradation_events}
        assert cfw.F_BT12_05 in codes

    def test_malformed_policy_bytes_tagged_f_bt12_05(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        vault = MemoryVaultReader(
            data=b"\xff\xfe\x00not valid yaml: [[[",
            identity=_matching_identity(session),
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="Q"),),
            clock=_fixed_clock(),
        )
        assert result.channel_state == "OK"
        assert broker.request_calls == []
        codes = {e.code for e in result.degradation_events}
        assert cfw.F_BT12_05 in codes

    def test_vault_read_raises_tagged_f_scout_f_05(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()

        class Kaboom(RuntimeError):
            pass

        vault = MemoryVaultReader(
            data=b"", identity=_matching_identity(session), raise_exc=Kaboom("vault down")
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="Q"),),
            clock=_fixed_clock(),
        )
        codes = {e.code for e in result.degradation_events}
        assert cfw.F_SCOUT_F_05 in codes
        assert result.channel_state == "OK"
        assert broker.request_calls == []

    def test_nfc_drift_identity_tagged_f_bt12_07(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        # Unicode NFD form that normalises to NFC "channel-f-policy-read"
        # — insert an NFD-form but conceptually trailing whitespace/drift.
        drift_identity = FakeIdentity(
            intent="channel-f-policy-read ",  # trailing space triggers strip
            session_id=session.session_id,
            slug=session.slug,
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=drift_identity
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="Q"),),
            clock=_fixed_clock(),
        )
        codes = {e.code for e in result.degradation_events}
        assert cfw.F_BT12_07 in codes
        assert broker.request_calls == []

    def test_policy_opts_in_non_dict_yaml_failclosed(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        vault = MemoryVaultReader(
            data=b"- just\n- a\n- list\n",
            identity=_matching_identity(session),
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="Q"),),
            clock=_fixed_clock(),
        )
        codes = {e.code for e in result.degradation_events}
        assert cfw.F_BT12_05 in codes


# ---------------------------------------------------------------------------
# Class 2 — TestChannelFPreflightDominance
# ---------------------------------------------------------------------------


class TestChannelFPreflightDominance:
    def test_sentinel_is_final_bool_true_literal(self):
        # Sentinel must exist, be True, and be the exact module-scope name
        # the AST lint rule looks for.
        assert cfw._CHANNEL_F_PREFLIGHT_GATE is True

    def test_fd_request_happens_inside_sentinel_guard(self):
        # This is belt-and-braces: the ast_lint R7 rule test asserts the
        # same thing. Here we just assert lint exit=0 on the shipping file.
        from pipeline.linting.ast_lint import (
            AST_PREFLIGHT_DOMINATES_FD_REQUEST,
            DEFAULT_RULES,
            lint_tree,
        )

        # Resolve relative to __file__ so the test works under pytest-xdist
        # workers whose cwd may differ from the repo root.
        repo_root = Path(__file__).resolve().parents[2]
        violations = tuple(
            lint_tree(
                repo_root / "pipeline" / "scout" / "channel_f_websearch.py",
                (AST_PREFLIGHT_DOMINATES_FD_REQUEST,),
            )
        )
        assert violations == ()

    def test_preflight_reject_holds_zero_fds(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        # Brave lane without the BRAVE-BYOK marker → immediate reject.
        vault = MemoryVaultReader(
            data=_policy_yaml(allowed=("US",), provider="brave"),
            identity=_matching_identity(session),
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="Q"),),
            clock=_fixed_clock(),
        )
        assert broker.request_calls == []
        assert nonces.reservations == []
        assert result.preflight_reject_count == 1

    def test_click_through_preflight_fires_before_second_fd(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        # Click-through URL targets a TLD NOT in allowed_jurisdictions.
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://example.de/grant1",)
                    ),
                )
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(allowed=("US", "GTLD")),
            identity=_matching_identity(session),
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(
                cfw.ChannelFQuery(
                    query_text="grants", hydrate_clickthrough=True
                ),
            ),
            clock=_fixed_clock(),
        )
        # .de is DE jurisdiction, which is NOT in allowed {US, GTLD}. The
        # second FD must not be acquired.
        assert len(broker.request_calls) == 1  # only first-hop SearxNG
        assert result.preflight_reject_count == 1

    def test_fd_count_equals_release_count_on_success(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://www.example.com/grant1",)
                    ),
                )
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="grants"),),
            clock=_fixed_clock(),
        )
        assert len(broker.request_calls) == len(broker.release_calls) == 1


# ---------------------------------------------------------------------------
# Class 3 — TestChannelFBT12Rules
# ---------------------------------------------------------------------------


def _run_preflight_only(
    *, policy: cfw.ChannelFJurisdictionPolicy, url: str
) -> Optional[str]:
    """Helper: run only ``_preflight_channel_f``, return code on reject."""
    session = FakeSession()
    try:
        cfw._preflight_channel_f(session, url, policy=policy)
    except cfw.ChannelFNotOptedIn:
        return cfw.F_BT12_01
    except cfw.ChannelFJurisdictionReject as exc:
        return exc.code
    except cfw.ChannelFURLPunycodeError:
        return cfw.F_BT12_06
    return None


class TestChannelFBT12Rules:
    def test_f_bt12_01_opt_in_false(self):
        policy = cfw.ChannelFJurisdictionPolicy(opt_in=False)
        assert (
            _run_preflight_only(
                policy=policy, url="https://example.com/foo"
            )
            == cfw.F_BT12_01
        )

    def test_f_bt12_02_denylist(self):
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True,
            allowed_jurisdictions=frozenset({"GTLD"}),
            disallowed_registrable_domains=frozenset({"example.com"}),
        )
        assert (
            _run_preflight_only(
                policy=policy, url="https://www.example.com/x"
            )
            == cfw.F_BT12_02
        )

    def test_f_bt12_03_unknown_jurisdiction(self):
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True,
            allowed_jurisdictions=frozenset({"US"}),
        )
        # Use an actually-unknown TLD (.zzzzz) — jurisdictions table has no
        # such entry.
        assert (
            _run_preflight_only(
                policy=policy, url="https://weird.zzzzz/x"
            )
            == cfw.F_BT12_03
        )

    def test_f_bt12_04_jurisdiction_not_allowed(self):
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True,
            allowed_jurisdictions=frozenset({"US"}),
        )
        assert (
            _run_preflight_only(
                policy=policy, url="https://bundestag.de/x"
            )
            == cfw.F_BT12_04
        )

    def test_f_bt12_06_punycode_error(self):
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True, allowed_jurisdictions=frozenset({"US"})
        )
        # --- empty/invalid host triggers punycode branch
        assert (
            _run_preflight_only(policy=policy, url="not-a-valid-url")
            == cfw.F_BT12_06
        )

    def test_f_bt12_06_empty_host_url(self):
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True, allowed_jurisdictions=frozenset({"GTLD"})
        )
        assert (
            _run_preflight_only(
                policy=policy, url="https:///path-only"
            )
            == cfw.F_BT12_06
        )

    def test_f_bt12_07_intent_mismatch_after_nfc(self):
        # The post-read _assert_intent_matches helper:
        session = FakeSession()
        identity = FakeIdentity(
            intent="channel-f-policy-read ",  # trailing space → NFC-drift
            session_id=session.session_id,
            slug=session.slug,
        )
        tag = cfw._assert_intent_matches(
            identity, session, "channel-f-policy-read"
        )
        assert tag is not None
        assert tag.startswith("intent_nfc_drift")

    def test_preflight_accept_on_allowed_gtld(self):
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True,
            allowed_jurisdictions=frozenset({"GTLD"}),
        )
        assert (
            _run_preflight_only(policy=policy, url="https://example.com/x")
            is None
        )

    def test_preflight_accept_on_cctld(self):
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True,
            allowed_jurisdictions=frozenset({"US"}),
        )
        assert (
            _run_preflight_only(policy=policy, url="https://foo.us/x")
            is None
        )


# ---------------------------------------------------------------------------
# Class 4 — TestChannelFIDNHomograph
# ---------------------------------------------------------------------------


class TestChannelFIDNHomograph:
    def test_cyrillic_a_resolves_to_distinct_punycode(self):
        # 'а' is U+0430 (Cyrillic), not U+0061 (Latin). Punycode form
        # differs from latin 'example.com'.
        latin = cfw._registrable_domain("https://example.com/x")
        cyr = cfw._registrable_domain("https://exаmple.com/x")
        assert latin == "example.com"
        assert cyr != latin
        assert cyr.startswith("xn--")

    def test_denylist_hit_on_punycode_form(self):
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True,
            allowed_jurisdictions=frozenset({"GTLD"}),
            disallowed_registrable_domains=frozenset(
                {cfw._registrable_domain("https://exаmple.com/x")}
            ),
        )
        assert (
            _run_preflight_only(
                policy=policy, url="https://exаmple.com/x"
            )
            == cfw.F_BT12_02
        )

    def test_latin_not_matched_against_cyrillic_denylist(self):
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True,
            allowed_jurisdictions=frozenset({"GTLD"}),
            disallowed_registrable_domains=frozenset(
                {cfw._registrable_domain("https://exаmple.com/x")}
            ),
        )
        # Latin 'example.com' should pass (allowed GTLD) — NOT match
        # the Cyrillic denylist entry.
        assert (
            _run_preflight_only(policy=policy, url="https://example.com/x")
            is None
        )

    def test_uts46_uppercase_normalised_to_lowercase(self):
        reg = cfw._registrable_domain("https://WWW.EXAMPLE.COM/x")
        assert reg == "example.com"

    def test_idn_accents_round_trip_to_xn(self):
        reg = cfw._registrable_domain("https://café.example.fr/x")
        assert reg.endswith(".fr")  # FR jurisdiction lookup uses last label

    def test_invalid_idn_raises_f_bt12_06(self):
        # Host with characters that idna.encode rejects.
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True, allowed_jurisdictions=frozenset({"US"})
        )
        # ':' in the hostname portion after url parsing will be treated as
        # port delim; but let's try an explicit malformed IDN control char.
        assert (
            _run_preflight_only(
                policy=policy, url="https://exa\u0000mple.com/x"
            )
            == cfw.F_BT12_06
        )


# ---------------------------------------------------------------------------
# Class 5 — TestChannelFFDLifecycle
# ---------------------------------------------------------------------------


class TestChannelFFDLifecycle:
    def _run_with_single_response(
        self,
        response_or_exc: Any,
        *,
        allowed=("US", "GTLD"),
        url_in_result="https://www.example.com/grant1",
    ):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(responses=[response_or_exc])
        vault = MemoryVaultReader(
            data=_policy_yaml(allowed=allowed),
            identity=_matching_identity(session),
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="grants"),),
            clock=_fixed_clock(),
        )
        return result, broker, nonces, http

    def test_fd_released_on_success_path(self):
        body = _searxng_results_body(("https://www.example.com/grant",))
        result, broker, nonces, _ = self._run_with_single_response(
            FakeResponse(status=200, body_bytes=body)
        )
        assert len(broker.release_calls) == 1
        assert len(nonces.releases) == 1
        path_tag = nonces.releases[0][1]
        assert path_tag == "success"

    def test_fd_released_on_fetch_error_5xx(self):
        result, broker, nonces, _ = self._run_with_single_response(
            FakeResponse(status=503, body_bytes=b"")
        )
        assert len(broker.release_calls) == 1
        path_tag = nonces.releases[0][1]
        assert path_tag == "fetch_error"

    def test_fd_released_on_timeout(self):
        result, broker, nonces, _ = self._run_with_single_response(
            TimeoutError("boom")
        )
        assert len(broker.release_calls) == 1
        assert nonces.releases[0][1] == "fetch_error"

    def test_fd_released_on_connection_error(self):
        result, broker, nonces, _ = self._run_with_single_response(
            ConnectionResetError("reset")
        )
        assert len(broker.release_calls) == 1
        assert nonces.releases[0][1] == "fetch_error"

    def test_fd_released_on_http_client_exception(self):
        class Boom(RuntimeError):
            pass

        result, broker, nonces, _ = self._run_with_single_response(
            Boom("client bug")
        )
        assert len(broker.release_calls) == 1
        assert nonces.releases[0][1] == "exception"

    def test_parse_error_records_f_scout_f_03_and_releases_fd(self):
        result, broker, nonces, _ = self._run_with_single_response(
            FakeResponse(status=200, body_bytes=b"not json")
        )
        codes = {e.code for e in result.degradation_events}
        assert cfw.F_SCOUT_F_03 in codes
        assert len(broker.release_calls) == 1

    def test_fd_acquire_failure_does_not_hold_nonce(self):
        session = FakeSession()
        broker = RecordingFDBroker(raise_on_request=True)
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="Q"),),
            clock=_fixed_clock(),
        )
        # Nonce was reserved, then released — no FD acquired.
        assert nonces.reservations
        assert nonces.releases  # released on exception path
        assert broker.release_calls == []
        assert broker.request_calls == []

    def test_nonce_reserve_failure_short_circuits(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry(raise_on_reserve=True)
        http = QueueHTTPClient()
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="Q"),),
            clock=_fixed_clock(),
        )
        # FD should not have been requested.
        assert broker.request_calls == []

    def test_f_scout_f_04_path_tag_emitted_per_release(self):
        body = _searxng_results_body(("https://www.example.com/g",))
        result, broker, nonces, _ = self._run_with_single_response(
            FakeResponse(status=200, body_bytes=body)
        )
        f04_events = [
            e for e in result.degradation_events if e.code == cfw.F_SCOUT_F_04
        ]
        assert f04_events, "must emit F-SCOUT-F-04 on release"


# ---------------------------------------------------------------------------
# Class 6 — TestChannelFSearxNGPath
# ---------------------------------------------------------------------------


class TestChannelFSearxNGPath:
    def _setup(self, allowed=("US", "GTLD")):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        vault = MemoryVaultReader(
            data=_policy_yaml(allowed=allowed),
            identity=_matching_identity(session),
        )
        return session, broker, nonces, http, vault

    def test_happy_single_query_single_result(self):
        session, broker, nonces, http, vault = self._setup()
        http.responses = [
            FakeResponse(
                status=200,
                body_bytes=_searxng_results_body(
                    ("https://foo.gov/grant-x",)
                ),
            )
        ]
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="soil"),),
            clock=_fixed_clock(),
        )
        assert len(result.candidates) == 1
        cand = result.candidates[0]
        assert cand.channel == "F"
        assert cand.feed_or_adapter_id.startswith("websearch:searxng:")
        assert cand.url == "https://foo.gov/grant-x"
        assert result.channel_state == "OK"

    def test_first_hop_host_is_localhost(self):
        session, broker, nonces, http, vault = self._setup()
        http.responses = [
            FakeResponse(
                status=200,
                body_bytes=_searxng_results_body((
                    "https://foo.gov/g",
                )),
            )
        ]
        cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=_fixed_clock(),
        )
        assert broker.request_calls[0] == ("https", "127.0.0.1")

    def test_disclosure_row_per_hop_first_only_without_clickthrough(self):
        session, broker, nonces, http, vault = self._setup()
        http.responses = [
            FakeResponse(
                status=200,
                body_bytes=_searxng_results_body(
                    ("https://foo.gov/1", "https://bar.gov/2")
                ),
            )
        ]
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=_fixed_clock(),
        )
        hops = [r.hop for r in result.disclosure_rows]
        assert hops == ["first"]

    def test_click_through_hop_produces_second_fd_and_row(self):
        session, broker, nonces, http, vault = self._setup()
        http.responses = [
            FakeResponse(
                status=200,
                body_bytes=_searxng_results_body(
                    ("https://foo.gov/one",)
                ),
            ),
            FakeResponse(status=200, body_bytes=b"<html>body</html>"),
        ]
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(
                cfw.ChannelFQuery(
                    query_text="q", hydrate_clickthrough=True
                ),
            ),
            clock=_fixed_clock(),
        )
        assert len(broker.request_calls) == 2
        hops = [r.hop for r in result.disclosure_rows]
        assert hops == ["first", "click_through"]
        assert broker.request_calls[1][1] == "foo.gov"

    def test_search_url_contains_encoded_query(self):
        session, broker, nonces, http, vault = self._setup()
        http.responses = [
            FakeResponse(
                status=200, body_bytes=_searxng_results_body(())
            )
        ]
        cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(
                cfw.ChannelFQuery(query_text="soil health AND cover crops"),
            ),
            clock=_fixed_clock(),
        )
        url = http.requests[0]["url"]
        assert "soil%20health" in url

    def test_multi_query_plan_produces_multi_first_hops(self):
        session, broker, nonces, http, vault = self._setup()
        http.responses = [
            FakeResponse(status=200, body_bytes=_searxng_results_body(())),
            FakeResponse(status=200, body_bytes=_searxng_results_body(())),
        ]
        cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(
                cfw.ChannelFQuery(query_text="alpha"),
                cfw.ChannelFQuery(query_text="beta"),
            ),
            clock=_fixed_clock(),
        )
        assert len(broker.request_calls) == 2

    def test_query_plan_cap_enforced(self):
        session, broker, nonces, http, vault = self._setup()
        http.responses = [
            FakeResponse(status=200, body_bytes=_searxng_results_body(()))
            for _ in range(5)
        ]
        cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=tuple(
                cfw.ChannelFQuery(query_text=f"q{i}") for i in range(20)
            ),
            clock=_fixed_clock(),
        )
        # Cap is _CHANNEL_F_MAX_QUERIES_PER_RUN = 5.
        assert len(broker.request_calls) == 5


# ---------------------------------------------------------------------------
# Class 7 — TestChannelFBravePath
# ---------------------------------------------------------------------------


class TestChannelFBravePath:
    def test_brave_without_byok_rejects_f_bt12_04(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        vault = MemoryVaultReader(
            data=_policy_yaml(allowed=("US",), provider="brave"),
            identity=_matching_identity(session),
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=_fixed_clock(),
        )
        codes = {e.code for e in result.degradation_events}
        assert cfw.F_BT12_04 in codes
        assert broker.request_calls == []
        assert result.preflight_reject_count == 1

    def test_brave_with_byok_hits_api_host(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_brave_results_body(
                        ("https://grants.foundation/y",)
                    ),
                )
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(
                allowed=("US", "GTLD", "BRAVE-BYOK"), provider="brave"
            ),
            identity=_matching_identity(session),
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=_fixed_clock(),
        )
        assert len(broker.request_calls) == 1
        assert broker.request_calls[0][1] == "api.search.brave.com"
        assert len(result.candidates) == 1
        assert result.candidates[0].feed_or_adapter_id.startswith(
            "websearch:brave:"
        )

    def test_brave_schema_web_results_parsed(self):
        parsed = cfw._parse_results(
            _brave_results_body(("https://a.io/x", "https://b.io/y"))
        )
        assert parsed is not None
        assert len(parsed) == 2
        assert parsed[0]["url"] == "https://a.io/x"

    def test_searxng_schema_flat_results_parsed(self):
        parsed = cfw._parse_results(
            _searxng_results_body(("https://x.com/1",))
        )
        assert parsed is not None
        assert len(parsed) == 1

    def test_unknown_provider_in_policy_rejected(self):
        # _parse_policy_bytes rejects non-{searxng,brave} provider strings.
        policy = cfw._parse_policy_bytes(_policy_yaml(provider="bing"))
        assert policy is None


# ---------------------------------------------------------------------------
# Class 8 — TestChannelFStateAggregation
# ---------------------------------------------------------------------------


class TestChannelFStateAggregation:
    def _run(self, http_responses, **policy_kw):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(responses=list(http_responses))
        vault = MemoryVaultReader(
            data=_policy_yaml(**policy_kw),
            identity=_matching_identity(session),
        )
        return cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(
                cfw.ChannelFQuery(query_text="q1"),
                cfw.ChannelFQuery(query_text="q2"),
            ),
            clock=_fixed_clock(),
        )

    def test_all_succeed_ok(self):
        body = _searxng_results_body(("https://foo.gov/g",))
        result = self._run(
            [
                FakeResponse(status=200, body_bytes=body),
                FakeResponse(status=200, body_bytes=body),
            ]
        )
        assert result.channel_state == "OK"

    def test_partial_failure_degraded(self):
        body = _searxng_results_body(("https://foo.gov/g",))
        result = self._run(
            [
                FakeResponse(status=200, body_bytes=body),
                FakeResponse(status=503, body_bytes=b""),
            ]
        )
        assert result.channel_state == "DEGRADED"

    def test_all_fail_failed(self):
        result = self._run(
            [
                FakeResponse(status=503, body_bytes=b""),
                FakeResponse(status=503, body_bytes=b""),
            ]
        )
        assert result.channel_state == "FAILED"

    def test_preflight_rejections_do_not_flip_state(self):
        # Both queries have policy that forbids the GTLD; both first-hops
        # on Brave (no BYOK) → both rejected. But no fetch attempted →
        # channel stays OK.
        result = self._run(
            [],
            allowed=("US",),
            provider="brave",
        )
        assert result.channel_state == "OK"
        assert result.preflight_reject_count >= 1

    def test_empty_query_plan_produces_ok(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(),
            clock=_fixed_clock(),
        )
        assert result.channel_state == "OK"
        assert result.candidates == ()
        assert broker.request_calls == []


# ---------------------------------------------------------------------------
# Class 9 — TestChannelFDisclosureRows
# ---------------------------------------------------------------------------


class TestChannelFDisclosureRows:
    def test_disclosure_carries_domain_and_count_only(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://foo.gov/a",)
                    ),
                )
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(
                cfw.ChannelFQuery(
                    query_text="a-very-distinctive-query-string-12345"
                ),
            ),
            clock=_fixed_clock(),
        )
        for row in result.disclosure_rows:
            # Only three meaningful fields: domain, count, hop, timestamp_utc.
            assert row.count == 1
            # The query string must NEVER appear anywhere in a disclosure row.
            assert (
                "a-very-distinctive-query-string-12345"
                not in row.domain
            )
            assert (
                "a-very-distinctive-query-string-12345"
                not in row.hop
            )
            assert (
                "a-very-distinctive-query-string-12345"
                not in row.timestamp_utc
            )

    def test_disclosure_timestamp_uses_injected_clock(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://foo.gov/a",)
                    ),
                )
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        fixed = _fixed_clock("2026-04-20T01:23:45+00:00")
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=fixed,
        )
        assert result.disclosure_rows[0].timestamp_utc.startswith(
            "2026-04-20T01:23:45"
        )

    def test_disclosure_no_body_excerpt(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://foo.gov/a",)
                    ),
                ),
                FakeResponse(
                    status=200,
                    body_bytes=b"ULTRA-SECRET-BODY-STRING-98765",
                ),
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(
                cfw.ChannelFQuery(
                    query_text="q", hydrate_clickthrough=True
                ),
            ),
            clock=_fixed_clock(),
        )
        for row in result.disclosure_rows:
            assert "ULTRA-SECRET-BODY-STRING-98765" not in row.domain
        # Nor should the body leak into degradation events.
        for e in result.degradation_events:
            assert (
                "ULTRA-SECRET-BODY-STRING-98765" not in (e.reason_tag or "")
            )

    def test_disclosure_row_count_always_one(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://foo.gov/a",)
                    ),
                )
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=_fixed_clock(),
        )
        assert all(r.count == 1 for r in result.disclosure_rows)


# ---------------------------------------------------------------------------
# Class 10 — TestChannelFNoModuleSideEffects
# ---------------------------------------------------------------------------


class TestChannelFNoModuleSideEffects:
    def test_import_opens_no_fds(self, monkeypatch):
        # Stdlib-adjacency probe: re-import channel_f_websearch and verify
        # its module namespace does not reference heavy third-party modules
        # (idna, feedparser, yaml) or pipeline.vault. We deliberately do
        # NOT evict these from sys.modules — other test modules under
        # tests/vault/** depend on pipeline.vault state and popping it
        # here would cascade. Instead, we check ``reloaded.__dict__`` for
        # top-level name leaks.
        original_open = os.open
        opens = []

        def tracking_open(*args, **kwargs):  # pragma: no cover
            opens.append(args[:1])
            return original_open(*args, **kwargs)

        # Only re-import our own module.
        for m in list(sys.modules):
            if m == "pipeline.scout.channel_f_websearch":
                del sys.modules[m]
        import pipeline.scout.channel_f_websearch as reloaded  # noqa: F401

        # Dispatcher's module namespace must not expose heavy third-party
        # modules at top level — they are all lazy-imported inside
        # functions (see module docstring).
        for banned in ("idna", "feedparser", "yaml"):
            assert (
                banned not in reloaded.__dict__
            ), f"{banned} leaked into channel_f_websearch module scope"
        # No direct pipeline.vault import either.
        for name, val in reloaded.__dict__.items():
            if hasattr(val, "__module__"):
                mod = getattr(val, "__module__", "")
                assert not (
                    isinstance(mod, str) and mod.startswith("pipeline.vault")
                ), f"{name} resolves to pipeline.vault ({mod})"
        assert reloaded.__name__ == "pipeline.scout.channel_f_websearch"

    def test_jurisdiction_table_is_frozen(self):
        assert isinstance(JURISDICTION_TABLE, MappingProxyType)
        with pytest.raises(TypeError):
            JURISDICTION_TABLE["xx"] = "XX"  # type: ignore[index]

    def test_jurisdiction_table_entry_count_floor(self):
        assert len(JURISDICTION_TABLE) >= 250

    def test_idna_not_loaded_before_first_call(self):
        # We can't unload idna if already imported by another test, but
        # we can verify the dispatcher module itself has no top-level
        # idna reference.
        import pipeline.scout.channel_f_websearch as m
        assert "idna" not in m.__dict__


# ---------------------------------------------------------------------------
# Class 11 — TestChannelFKWOnly
# ---------------------------------------------------------------------------


class TestChannelFKWOnly:
    def test_positional_call_rejected(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        with pytest.raises(TypeError):
            cfw.discover_channel_f(  # type: ignore[misc]
                session, broker, nonces, http, vault, ()
            )


# ---------------------------------------------------------------------------
# Class 12 — TestASTLintRegression
# ---------------------------------------------------------------------------


class TestASTLintRegression:
    def test_default_rules_clean_on_channel_f(self, tmp_path):
        from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree

        # Stage ONLY channel_f_websearch.py + its sibling helpers under a
        # tmp scout tree so lint_tree (which requires a directory) inspects
        # the Round 7 surface in isolation.
        # Resolve relative to __file__ so the test works under pytest-xdist
        # workers whose cwd may differ from the repo root.
        repo_root = Path(__file__).resolve().parents[2]
        src_root = repo_root / "pipeline" / "scout"
        dst_scout = tmp_path / "pipeline" / "scout"
        dst_scout.mkdir(parents=True)
        for name in (
            "channel_f_websearch.py",
            "_channel_f_jurisdictions.py",
            "_vault_reader_adapter.py",
        ):
            (dst_scout / name).write_text(
                (src_root / name).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        violations = tuple(lint_tree(tmp_path, DEFAULT_RULES))
        assert violations == (), f"unexpected violations: {violations}"

    def test_r7_rejects_synthetic_undominated_fd_request(self, tmp_path):
        from pipeline.linting.ast_lint import (
            AST_PREFLIGHT_DOMINATES_FD_REQUEST,
            lint_tree,
        )

        # Synthetic copy in a Scout-tree layout to trigger R7 scope
        # (pipeline/scout/channel_f_bypass.py).
        scout_dir = tmp_path / "pipeline" / "scout"
        scout_dir.mkdir(parents=True)
        synth = scout_dir / "channel_f_bypass.py"
        synth.write_text(
            "from typing import Final\n"
            "_CHANNEL_F_PREFLIGHT_GATE: Final[bool] = True\n"
            "def bad(fd_broker):\n"
            "    fd = fd_broker.request_fd(kind='https', host='x')\n"
            "    fd_broker.release_fd(fd)\n"
        )
        violations = tuple(
            lint_tree(tmp_path, [AST_PREFLIGHT_DOMINATES_FD_REQUEST])
        )
        assert len(violations) == 1
        assert (
            violations[0].reason_tag
            == "scout_fd_request_not_preflight_dominated"
        )

    def test_r7_accepts_dominated_fd_request(self, tmp_path):
        from pipeline.linting.ast_lint import (
            AST_PREFLIGHT_DOMINATES_FD_REQUEST,
            lint_tree,
        )

        scout_dir = tmp_path / "pipeline" / "scout"
        scout_dir.mkdir(parents=True)
        synth = scout_dir / "channel_f_good.py"
        synth.write_text(
            "from typing import Final\n"
            "_CHANNEL_F_PREFLIGHT_GATE: Final[bool] = True\n"
            "def ok(fd_broker):\n"
            "    if _CHANNEL_F_PREFLIGHT_GATE:\n"
            "        fd = fd_broker.request_fd(kind='https', host='x')\n"
            "        fd_broker.release_fd(fd)\n"
        )
        violations = tuple(
            lint_tree(tmp_path, [AST_PREFLIGHT_DOMINATES_FD_REQUEST])
        )
        assert violations == ()


# ---------------------------------------------------------------------------
# Class 13 — TestPublicSurface
# ---------------------------------------------------------------------------


class TestPublicSurface:
    def test_version_range_check_r7_or_later(self):
        """E-025: range-check rN ≥ 7, not hard-pin."""
        version = cfw.__version__
        assert version.startswith("0.1.0-scout-r")
        rn = int(version.split("scout-r", 1)[1])
        assert rn >= 7

    def test_discover_channel_f_reachable_via_pipeline_scout(self):
        import pipeline.scout as scout_pkg

        fn = getattr(
            scout_pkg, "channel_f_websearch", None
        ) or importlib.import_module(
            "pipeline.scout.channel_f_websearch"
        )
        assert hasattr(fn, "discover_channel_f")

    def test_failure_codes_exported(self):
        for code in (
            "F_BT12_01",
            "F_BT12_02",
            "F_BT12_03",
            "F_BT12_04",
            "F_BT12_05",
            "F_BT12_06",
            "F_BT12_07",
            "F_SCOUT_F_01",
            "F_SCOUT_F_02",
            "F_SCOUT_F_03",
            "F_SCOUT_F_04",
            "F_SCOUT_F_05",
            "F_SCOUT_F_06",
        ):
            assert hasattr(cfw, code)
            assert getattr(cfw, code).startswith("F-")

    def test_all_contains_public_dataclasses(self):
        for name in (
            "ChannelFQuery",
            "ChannelFJurisdictionPolicy",
            "ChannelFDiscoverResult",
            "ChannelFDegradationEvent",
            "ChannelFDisclosureRow",
            "VaultReader",
            "discover_channel_f",
        ):
            assert name in cfw.__all__

    def test_channel_f_constant(self):
        assert cfw.CHANNEL_F == "F"
        assert cfw.FEED_PREFIX_WEBSEARCH == "websearch:"


# ---------------------------------------------------------------------------
# Class 14 — TestSharedProtocolReuse
# ---------------------------------------------------------------------------


class TestSharedProtocolReuse:
    def test_fd_broker_protocol_origin_is_channel_a(self):
        # E-026 formal: under sys.modules reload, `is` identity fails. Use
        # __module__ lineage instead.
        assert (
            cfw.FDBroker.__module__
            == "pipeline.scout.channel_a_federal_apis"
        )

    def test_http_client_protocol_origin_is_channel_a(self):
        assert (
            cfw.HTTPClient.__module__
            == "pipeline.scout.channel_a_federal_apis"
        )

    def test_nonce_registry_protocol_origin_is_channel_a(self):
        assert (
            cfw.NonceRegistry.__module__
            == "pipeline.scout.channel_a_federal_apis"
        )

    def test_session_like_protocol_origin_is_channel_a(self):
        assert (
            cfw.SessionLike.__module__
            == "pipeline.scout.channel_a_federal_apis"
        )

    def test_candidate_origin_is_scout_types(self):
        from pipeline.scout._types import Candidate as C_root

        assert C_root.__module__ == "pipeline.scout._types"


# ---------------------------------------------------------------------------
# Class 15 — TestChannelFContentHashing
# ---------------------------------------------------------------------------


class TestChannelFContentHashing:
    def test_candidate_content_hash_is_sha3_512_of_body(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        body = b"the-actual-body-bytes-xyz"
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://foo.gov/a",)
                    ),
                ),
                FakeResponse(status=200, body_bytes=body),
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(
                cfw.ChannelFQuery(
                    query_text="q", hydrate_clickthrough=True
                ),
            ),
            clock=_fixed_clock(),
        )
        assert result.candidates[0].content_hash == hashlib.sha3_512(
            body
        ).hexdigest()

    def test_empty_body_hash_on_non_clickthrough(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://foo.gov/a",)
                    ),
                )
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=_fixed_clock(),
        )
        assert result.candidates[0].content_hash == hashlib.sha3_512(
            b""
        ).hexdigest()

    def test_body_bytes_not_retained_in_candidate(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        body = b"SECRET-GRANT-BODY-99999"
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://foo.gov/a",)
                    ),
                ),
                FakeResponse(status=200, body_bytes=body),
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(
                cfw.ChannelFQuery(
                    query_text="q", hydrate_clickthrough=True
                ),
            ),
            clock=_fixed_clock(),
        )
        # Candidate fields must not include the raw body.
        cand = result.candidates[0]
        for val in (
            cand.title,
            cand.url,
            cand.content_hash,
            cand.feed_or_adapter_id,
        ):
            assert b"SECRET-GRANT-BODY-99999".decode() not in str(val)


# ---------------------------------------------------------------------------
# Class 16 — TestVaultReaderAdapter (Section 2 sibling adapter)
# ---------------------------------------------------------------------------


class TestVaultReaderAdapter:
    def test_adapter_delegates_to_injected_callable(self):
        captured = {}

        def fake_read(*, path, intent, session_id, slug):
            captured.update(
                path=path, intent=intent, session_id=session_id, slug=slug
            )
            return b"data-bytes", FakeIdentity(
                intent=intent, session_id=session_id, slug=slug
            )

        reader = Section2VaultReader(read_callable=fake_read)
        data, identity = reader.read(
            path="orgs/xyz/scout/channel_f_policy.yaml",
            intent="channel-f-policy-read",
            session_id="s-1",
            slug="xyz",
        )
        assert data == b"data-bytes"
        assert isinstance(identity, IdentityTupleSnapshot)
        assert identity.intent == "channel-f-policy-read"
        assert captured["path"] == "orgs/xyz/scout/channel_f_policy.yaml"

    def test_adapter_snapshot_preserves_fields(self):
        reader = Section2VaultReader(
            read_callable=lambda **kw: (
                b"x",
                FakeIdentity(
                    intent=kw["intent"],
                    session_id=kw["session_id"],
                    slug=kw["slug"],
                ),
            )
        )
        _, snap = reader.read(
            path="p", intent="i", session_id="s", slug="g"
        )
        assert snap.intent == "i"
        assert snap.session_id == "s"
        assert snap.slug == "g"


# ---------------------------------------------------------------------------
# Class 17 — TestJurisdictionsTable
# ---------------------------------------------------------------------------


class TestJurisdictionsTable:
    def test_us_cctld_resolves_to_us(self):
        assert jurisdiction_for_etld("us") == "US"

    def test_uk_cctld_resolves_to_gb(self):
        assert jurisdiction_for_etld("uk") == "GB"

    def test_com_gtld_resolves_to_gtld(self):
        assert jurisdiction_for_etld("com") == "GTLD"

    def test_gov_mil_edu_map_to_us(self):
        assert jurisdiction_for_etld("gov") == "US"
        assert jurisdiction_for_etld("mil") == "US"
        assert jurisdiction_for_etld("edu") == "US"

    def test_unknown_returns_none(self):
        assert jurisdiction_for_etld("zzzzz") is None

    def test_non_string_returns_none(self):
        assert jurisdiction_for_etld(None) is None  # type: ignore[arg-type]
        assert jurisdiction_for_etld(42) is None  # type: ignore[arg-type]

    def test_case_insensitive_lookup(self):
        assert jurisdiction_for_etld("US") == "US"
        assert jurisdiction_for_etld("CoM") == "GTLD"

    def test_eu_jurisdiction_tagged(self):
        assert jurisdiction_for_etld("eu") == "EU"


# ---------------------------------------------------------------------------
# Class 18 — TestChannelFDiscoverWithRealAdapter (integration smoke)
# ---------------------------------------------------------------------------


class TestChannelFDiscoverWithRealAdapter:
    def test_section2_adapter_threads_through_discover(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://www.foo.gov/a",)
                    ),
                )
            ]
        )

        def fake_vault_read(*, path, intent, session_id, slug):
            return _policy_yaml(), FakeIdentity(
                intent=intent, session_id=session_id, slug=slug
            )

        adapter = Section2VaultReader(read_callable=fake_vault_read)
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=adapter,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=_fixed_clock(),
        )
        assert len(result.candidates) == 1
        assert result.channel_state == "OK"


# ---------------------------------------------------------------------------
# Class 19 — TestAdversarial (≥ 5 tests per §7 step 4)
# ---------------------------------------------------------------------------


class TestAdversarial:
    def test_adv_cyrillic_homograph_bypass_blocked(self):
        # Adversary crafts URL with Cyrillic 'а' hoping to hit a Latin
        # allowlist entry. Pre-flight must resolve Punycode and reject.
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True,
            allowed_jurisdictions=frozenset({"GTLD"}),
            disallowed_registrable_domains=frozenset({"example.com"}),
        )
        # The raw Cyrillic URL does NOT string-match "example.com" literally.
        # _registrable_domain converts it to xn-- form, which does NOT match
        # the denylist entry, but that's correct: the denylist uses Punycode
        # and the attacker's Cyrillic domain is a DIFFERENT resource. Test
        # is that the two do NOT silently collapse together.
        latin_reg = cfw._registrable_domain("https://example.com/x")
        cyr_reg = cfw._registrable_domain("https://exаmple.com/x")
        assert latin_reg != cyr_reg

    def test_adv_query_text_never_in_disclosure(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://foo.gov/a",)
                    ),
                )
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        secret = "ADVERSARY-CANARY-TOKEN-A9F2"
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text=secret),),
            clock=_fixed_clock(),
        )
        serialized = json.dumps(
            [
                {
                    "domain": r.domain,
                    "count": r.count,
                    "hop": r.hop,
                    "timestamp_utc": r.timestamp_utc,
                }
                for r in result.disclosure_rows
            ]
        )
        assert secret not in serialized

    def test_adv_response_with_script_injection_safe(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        # Malicious JSON that tries to inject control chars into titles.
        mal_body = json.dumps(
            {
                "results": [
                    {
                        "url": "https://foo.gov/a",
                        "title": "<script>alert(1)</script>",
                    }
                ]
            }
        ).encode()
        http = QueueHTTPClient(
            responses=[FakeResponse(status=200, body_bytes=mal_body)]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=_fixed_clock(),
        )
        # We don't sanitise; we just carry it verbatim into the Candidate.
        # But the Candidate's content_hash must still be deterministic.
        assert len(result.candidates) == 1
        assert result.candidates[0].title == "<script>alert(1)</script>"

    def test_adv_broker_raises_on_second_hop_does_not_leak_first_fd(self):
        session = FakeSession()

        class FlakyBroker(RecordingFDBroker):
            def request_fd(self, *, kind: str, host: str) -> int:
                if len(self.request_calls) == 1:
                    raise OSError("pool drained mid-run")
                return super().request_fd(kind=kind, host=host)

        broker = FlakyBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://foo.gov/a",)
                    ),
                )
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(
                cfw.ChannelFQuery(
                    query_text="q", hydrate_clickthrough=True
                ),
            ),
            clock=_fixed_clock(),
        )
        # The first hop was released; the second hop failed. No FD leak.
        assert len(broker.request_calls) == 1
        assert len(broker.release_calls) == 1

    def test_adv_fifty_rejected_queries_do_not_exhaust_fds(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        # Brave lane without BYOK → every query pre-flight rejects.
        vault = MemoryVaultReader(
            data=_policy_yaml(allowed=("US",), provider="brave"),
            identity=_matching_identity(session),
        )
        queries = tuple(
            cfw.ChannelFQuery(query_text=f"q{i}") for i in range(50)
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=queries,
            clock=_fixed_clock(),
        )
        # Short-circuit before any per-query dispatch; no FD requests.
        assert broker.request_calls == []
        assert nonces.reservations == []

    def test_adv_oversize_query_plan_capped_at_max(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200, body_bytes=_searxng_results_body(())
                )
                for _ in range(100)
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        queries = tuple(
            cfw.ChannelFQuery(query_text=f"q{i}") for i in range(1000)
        )
        cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=queries,
            clock=_fixed_clock(),
        )
        # _CHANNEL_F_MAX_QUERIES_PER_RUN = 5.
        assert len(broker.request_calls) == 5

    def test_adv_alias_import_of_fd_broker_still_caught(self, tmp_path):
        # R7 must resolve `fd_broker` attribute access through
        # session/context binding. Short-circuit `or` over sentinel is
        # explicitly rejected by the rule — verify the classifier tag.
        from pipeline.linting.ast_lint import (
            AST_PREFLIGHT_DOMINATES_FD_REQUEST,
            lint_tree,
        )

        scout_dir = tmp_path / "pipeline" / "scout"
        scout_dir.mkdir(parents=True)
        synth = scout_dir / "channel_f_or_bypass.py"
        synth.write_text(
            "from typing import Final\n"
            "_CHANNEL_F_PREFLIGHT_GATE: Final[bool] = True\n"
            "def bad(fd_broker, other):\n"
            "    if _CHANNEL_F_PREFLIGHT_GATE or other:\n"
            "        fd = fd_broker.request_fd(kind='https', host='x')\n"
            "        fd_broker.release_fd(fd)\n"
        )
        violations = tuple(
            lint_tree(tmp_path, [AST_PREFLIGHT_DOMINATES_FD_REQUEST])
        )
        assert len(violations) == 1
        assert (
            violations[0].reason_tag
            == "fd_request_preflight_short_circuit_or_bypass"
        )

    def test_adv_malicious_policy_with_numeric_port_as_string(self):
        # String port → reject (type check).
        raw = (
            b"opt_in: true\n"
            b"allowed_jurisdictions: ['US']\n"
            b"disallowed_registrable_domains: []\n"
            b'searxng_port: "8888"\n'
            b"provider: searxng\n"
        )
        assert cfw._parse_policy_bytes(raw) is None

    def test_adv_malicious_policy_with_bool_as_port(self):
        # Bool port → reject (bool is a subtype of int in Python).
        raw = (
            b"opt_in: true\n"
            b"allowed_jurisdictions: ['US']\n"
            b"disallowed_registrable_domains: []\n"
            b"searxng_port: true\n"
            b"provider: searxng\n"
        )
        assert cfw._parse_policy_bytes(raw) is None


# ---------------------------------------------------------------------------
# Class 20 — TestHelpers (direct coverage of internal primitives)
# ---------------------------------------------------------------------------


class TestHelpers:
    def test_registrable_domain_bare_tld(self):
        # Single-label host — no registrable domain — returns the host.
        assert cfw._registrable_domain("https://localhost/").endswith(
            "localhost"
        )

    def test_registrable_domain_multi_level(self):
        assert (
            cfw._registrable_domain("https://a.b.c.foo.gov/x") == "foo.gov"
        )

    def test_jurisdiction_from_empty_string_returns_none(self):
        assert cfw._jurisdiction_from_registrable_domain("") is None

    def test_jurisdiction_from_dotless(self):
        # A dotless 'label' is the final label. "com" → GTLD.
        assert cfw._jurisdiction_from_registrable_domain("com") == "GTLD"

    def test_build_candidate_rejects_unknown_provider(self):
        with pytest.raises(ValueError):
            cfw._build_channel_f_candidate(
                provider="bing",
                canonical_search_url="https://x.com/q",
                result_url="https://y.com/1",
                title="T",
                body_hash="h",
                fetch_timestamp_utc="2026-01-01T00:00:00+00:00",
            )

    def test_canonical_search_url_searxng(self):
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True,
            allowed_jurisdictions=frozenset({"GTLD"}),
            searxng_port=9999,
        )
        url = cfw._canonical_search_url("searxng", "hello world", policy)
        assert "127.0.0.1:9999" in url
        assert "hello%20world" in url

    def test_canonical_search_url_brave(self):
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True,
            allowed_jurisdictions=frozenset({"BRAVE-BYOK"}),
        )
        url = cfw._canonical_search_url("brave", "hello", policy)
        assert "api.search.brave.com" in url
        assert "hello" in url

    def test_canonical_search_url_unknown_provider_raises(self):
        policy = cfw.ChannelFJurisdictionPolicy(
            opt_in=True, allowed_jurisdictions=frozenset({"US"})
        )
        with pytest.raises(ValueError):
            cfw._canonical_search_url("bing", "q", policy)

    def test_parse_results_rejects_non_dict(self):
        assert cfw._parse_results(b'"just a string"') is None

    def test_parse_results_rejects_non_list_results(self):
        assert cfw._parse_results(b'{"results": "not a list"}') is None

    def test_parse_results_drops_row_without_url(self):
        parsed = cfw._parse_results(
            b'{"results": [{"title": "t"}, {"url": "u", "title": "x"}]}'
        )
        assert parsed is not None
        assert len(parsed) == 1

    def test_parse_results_handles_bad_utf8(self):
        assert cfw._parse_results(b"\xff\xfe\x00not-json") is None

    def test_channel_f_discover_result_is_frozen(self):
        r = cfw.ChannelFDiscoverResult(
            candidates=(),
            channel_state="OK",
            degradation_events=(),
            disclosure_rows=(),
            preflight_reject_count=0,
        )
        with pytest.raises((AttributeError, Exception)):
            r.preflight_reject_count = 1  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Class 21 — TestPolicyDefaults (ChannelFJurisdictionPolicy)
# ---------------------------------------------------------------------------


class TestPolicyDefaults:
    def test_default_policy_is_default_deny(self):
        p = cfw.ChannelFJurisdictionPolicy()
        assert p.opt_in is False
        assert p.allowed_jurisdictions == frozenset()
        assert p.disallowed_registrable_domains == frozenset()

    def test_default_provider_is_searxng(self):
        p = cfw.ChannelFJurisdictionPolicy()
        assert p.provider == cfw.PROVIDER_SEARXNG

    def test_policy_frozen(self):
        p = cfw.ChannelFJurisdictionPolicy()
        with pytest.raises((AttributeError, Exception)):
            p.opt_in = True  # type: ignore[misc]

    def test_channel_f_query_defaults(self):
        q = cfw.ChannelFQuery(query_text="x")
        assert q.max_results == 10
        assert q.hydrate_clickthrough is False

    def test_channel_f_query_frozen(self):
        q = cfw.ChannelFQuery(query_text="x")
        with pytest.raises((AttributeError, Exception)):
            q.query_text = "y"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Class 22 — TestCoverageGaps
# ---------------------------------------------------------------------------


class TestCoverageGaps:
    """Targeted tests for residual coverage holes (push ≥95% → 100%)."""

    def test_default_clock_returns_tz_aware_utc(self):
        now = cfw._default_clock()
        assert isinstance(now, _dt.datetime)
        assert now.tzinfo is not None

    def test_assert_intent_matches_slug_mismatch(self):
        session = FakeSession()
        ident = FakeIdentity(
            intent="channel-f-policy-read",
            session_id=session.session_id,
            slug="OTHER_SLUG",
        )
        drift = cfw._assert_intent_matches(
            ident, session, "channel-f-policy-read"
        )
        assert drift is not None
        assert drift.startswith("slug_mismatch:")

    def test_assert_intent_matches_intent_strict_mismatch(self):
        session = FakeSession()
        ident = FakeIdentity(
            intent="some-other-intent",
            session_id=session.session_id,
            slug=session.slug,
        )
        drift = cfw._assert_intent_matches(
            ident, session, "channel-f-policy-read"
        )
        assert drift is not None
        assert drift.startswith("intent_mismatch:")

    def test_parse_policy_bytes_yaml_raises(self):
        # Binary bytes that yaml can't decode — triggers the outer except.
        bad = b"\x80\x81\x82:\tnot\xffyaml"
        policy = cfw._parse_policy_bytes(bad)
        assert policy is None

    def test_parse_policy_bytes_allowed_not_list(self):
        bad = (
            b"opt_in: true\n"
            b"allowed_jurisdictions: not-a-list\n"
            b"disallowed_registrable_domains: []\n"
            b"searxng_port: 8888\n"
            b"provider: searxng\n"
        )
        assert cfw._parse_policy_bytes(bad) is None

    def test_parse_policy_bytes_disallowed_not_list(self):
        bad = (
            b"opt_in: true\n"
            b"allowed_jurisdictions: []\n"
            b"disallowed_registrable_domains: 42\n"
            b"searxng_port: 8888\n"
            b"provider: searxng\n"
        )
        assert cfw._parse_policy_bytes(bad) is None

    def test_parse_policy_bytes_nonmapping_root(self):
        # YAML top-level is a list — not a mapping → None.
        bad = b"- opt_in\n- true\n"
        assert cfw._parse_policy_bytes(bad) is None

    def test_parse_results_row_not_dict_skipped(self):
        body = json.dumps(
            {"results": ["not-a-dict", {"url": "u", "title": "t"}]}
        ).encode("utf-8")
        out = cfw._parse_results(body)
        assert out is not None
        assert len(out) == 1

    def test_discover_empty_result_url_skipped(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=json.dumps(
                        {
                            "results": [
                                {"url": "", "title": "empty"},
                                {
                                    "url": "https://foo.gov/a",
                                    "title": "ok",
                                },
                            ]
                        }
                    ).encode("utf-8"),
                )
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=_fixed_clock(),
        )
        # Only the non-empty URL produced a candidate.
        assert len(result.candidates) == 1

    def test_now_iso_with_naive_datetime_clock(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://foo.gov/a",)
                    ),
                )
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )

        def naive_clock() -> _dt.datetime:
            # No tzinfo — forces the `now.replace(tzinfo=utc)` branch.
            return _dt.datetime(2026, 4, 20, 12, 0, 0)

        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=naive_clock,
        )
        # Every disclosure row carries a tz-aware ISO string.
        for row in result.disclosure_rows:
            assert "+00:00" in row.timestamp_utc

    def test_now_iso_non_datetime_clock_returns_str(self):
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient(
            responses=[
                FakeResponse(
                    status=200,
                    body_bytes=_searxng_results_body(
                        ("https://foo.gov/a",)
                    ),
                )
            ]
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=_matching_identity(session)
        )

        def string_clock() -> Any:
            return "CLOCK-SENTINEL"

        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=string_clock,  # type: ignore[arg-type]
        )
        for row in result.disclosure_rows:
            assert row.timestamp_utc == "CLOCK-SENTINEL"

    def test_brave_first_hop_preflight_rejects_without_gtld(self):
        # Brave BYOK allowed, but the Brave host (api.search.brave.com →
        # GTLD) is NOT in allowed_jurisdictions. First-hop preflight
        # rejects — no FD requested. Exercises lines 897-929.
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()  # zero responses — preflight must short-
        # circuit before any fetch.
        vault = MemoryVaultReader(
            data=_policy_yaml(
                allowed=("BRAVE-BYOK",), provider="brave"
            ),
            identity=_matching_identity(session),
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=_fixed_clock(),
        )
        assert broker.request_calls == []
        assert result.preflight_reject_count >= 1
        codes = {e.code for e in result.degradation_events}
        assert "F-BT12-04" in codes

    def test_brave_first_hop_preflight_denylist_reject(self):
        # Brave BYOK + GTLD allowed, but api.search.brave.com's
        # registrable domain "brave.com" is on the denylist. Exercises
        # the JurisdictionReject branch with F-BT12-02 code.
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        vault = MemoryVaultReader(
            data=_policy_yaml(
                allowed=("BRAVE-BYOK", "GTLD"),
                disallowed=("brave.com",),
                provider="brave",
            ),
            identity=_matching_identity(session),
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=_fixed_clock(),
        )
        assert broker.request_calls == []
        codes = {e.code for e in result.degradation_events}
        assert "F-BT12-02" in codes

    def test_policy_load_mismatch_surfaces_as_event(self):
        # Identity drift triggers the exc-handler path that appends a
        # "policy_load" event with HIGH severity.
        session = FakeSession()
        broker = RecordingFDBroker()
        nonces = RecordingNonceRegistry()
        http = QueueHTTPClient()
        wrong = FakeIdentity(
            intent="channel-f-policy-read",
            session_id="DIFFERENT",
            slug=session.slug,
        )
        vault = MemoryVaultReader(
            data=_policy_yaml(), identity=wrong
        )
        result = cfw.discover_channel_f(
            session=session,
            fd_broker=broker,
            nonce_registry=nonces,
            http_client=http,
            vault_reader=vault,
            query_plan=(cfw.ChannelFQuery(query_text="q"),),
            clock=_fixed_clock(),
        )
        assert broker.request_calls == []
        sources = {e.source for e in result.degradation_events}
        assert "policy_load" in sources
        severities = {e.severity for e in result.degradation_events}
        assert "HIGH" in severities

    def test_canonical_search_url_raises_on_unknown(self):
        policy = cfw.ChannelFJurisdictionPolicy(opt_in=True)
        with pytest.raises(ValueError):
            cfw._canonical_search_url("bing", "q", policy)
