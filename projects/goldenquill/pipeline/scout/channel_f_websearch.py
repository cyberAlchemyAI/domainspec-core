"""Channel F — Client-material-driven web search (§4.6).

The only Scout channel that runs LLM- or operator-initiated queries. BT12
jurisdiction pre-flight gates every outbound fetch and **strictly dominates
every FD acquisition** — enforced at build-time by ARCH-05 R7
``AST_PREFLIGHT_DOMINATES_FD_REQUEST``.

Blueprint anchors:
- §4.6 Channel F full spec (lines 548-602) — implementation target.
- §5.1 BT12 M11 Channel F domain pre-flight (lines 1084-1095).
- §6.6 F-BT12-01..07 + F-SCOUT-F-01..06 failure-code taxonomy.
- §8 constants re-verified at build time.
- A-v3-07 → ARCH-05 R7 (preflight-dominance CFG rule; this module is the
  first production consumer).
- A-06 → pre-flight strictly before FD request, ``try/finally`` release on
  every exit path (``F-SCOUT-F-04`` path tag).
- A-08 → policy loaded via :class:`VaultReader` (intent-bound vault_read).
- A-14 → ``_registrable_domain`` uses ``idna.encode(host, uts46=True)``
  before eTLD+1 extraction. Punycode homograph attacks cannot slip.
- A-v3-04 → post-``vault_read`` strict-equality intent check after NFC
  normalisation + whitespace strip.

Providers:
- **Default:** SearxNG self-hosted on the Golden Quill (localhost).
- **Fallback:** Brave Search API BYOK — opt-in per policy + ``BRAVE-BYOK``
  jurisdiction tag.

Default-deny posture: a missing policy file (or ``opt_in=False``) short-
circuits the whole channel; ``channel_state="OK"`` trivially, zero FDs
requested, zero nonces reserved.

No retries (policy decision). BT12 rejections are terminal. Fetch failures
are terminal. Retrying invites rate-limiting from SearxNG upstream engines.

No module-level side effects on import. Zero network, zero FD reservation,
zero nonce reservation, zero ``vault_read``. ``idna`` is lazy-imported
inside :func:`_registrable_domain` — the dispatcher module itself does not
pull ``idna`` into ``sys.modules`` at import time.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import os
import socket
import unicodedata
import urllib.parse
from dataclasses import dataclass, field
from typing import Callable, Final, Mapping, Optional, Protocol

from pipeline.scout._constants import (
    CHANNEL_F,
    FEED_PREFIX_BRAVE,
    FEED_PREFIX_SEARXNG,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
)
from pipeline.scout._types import Candidate
from pipeline.scout.channel_a_federal_apis import (
    FDBroker,
    HTTPClient,
    HTTPResponse,
    NonceRegistry,
    SessionLike,
)

# Channel F only needs ``now()`` — no ``sleep`` (no retries). Type the seam
# as a plain nullary callable returning ``datetime``, mirroring Channel C's
# local ``ClockFn`` shape without re-importing Channel A's sleep-bearing
# Protocol.
ClockFn = Callable[[], _dt.datetime]


__version__ = "0.1.0-scout-r7"


__all__ = [
    "BRAVE_HOST",
    "CHANNEL_F",
    "ChannelFDegradationEvent",
    "ChannelFDiscoverResult",
    "ChannelFDisclosureRow",
    "ChannelFJurisdictionPolicy",
    "ChannelFJurisdictionReject",
    "ChannelFNotOptedIn",
    "ChannelFPolicyVaultReadMismatch",
    "ChannelFQuery",
    "ChannelFURLPunycodeError",
    "FEED_PREFIX_WEBSEARCH",
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
    "IdentityTupleLike",
    "PROVIDER_BRAVE",
    "PROVIDER_SEARXNG",
    "SEARXNG_HOST",
    "VaultReader",
    "__version__",
    "discover_channel_f",
]


# ---------------------------------------------------------------------------
# Constants (re-verified at build time per spec-card §Constants-to-pin)
# ---------------------------------------------------------------------------


FEED_PREFIX_WEBSEARCH: Final[str] = "websearch:"

_INTENT_CHANNEL_F_POLICY_READ: Final[str] = "channel-f-policy-read"

# ARCH-05 R7 sentinel — module-scope `Final[bool]` with literal-only init.
# Every ``fd_broker.request_fd`` sink in this module is CFG-dominated by an
# ``if _CHANNEL_F_PREFLIGHT_GATE:`` guard (B-v5-01 literal init).
# ARCH-05 R7 lint rejects non-literal initializers; this assignment MUST
# remain a bare ``True`` / ``False`` constant.
_CHANNEL_F_PREFLIGHT_GATE: Final[bool] = True

_CHANNEL_F_MAX_RESULTS_PER_QUERY: Final[int] = 10
_CHANNEL_F_MAX_QUERIES_PER_RUN: Final[int] = 5

# First-hop host constants.
SEARXNG_HOST: Final[str] = "127.0.0.1"
BRAVE_HOST: Final[str] = "api.search.brave.com"

# Provider tokens used in ``feed_or_adapter_id``.
PROVIDER_SEARXNG: Final[str] = FEED_PREFIX_SEARXNG
PROVIDER_BRAVE: Final[str] = FEED_PREFIX_BRAVE

# Policy marker meaning "the operator has opted into the Brave BYOK lane."
_BRAVE_BYOK_JURISDICTION: Final[str] = "BRAVE-BYOK"

# Per-request timeout ceilings (§4.6 line 600; reuse Channel-A defaults).
_CHANNEL_F_CONNECT_TIMEOUT_S: Final[float] = 5.0
_CHANNEL_F_READ_TIMEOUT_S: Final[float] = 8.0

# Severity labels used in degradation events.
SEVERITY_LOW: Final[str] = "LOW"
SEVERITY_MEDIUM: Final[str] = "MEDIUM"
SEVERITY_HIGH: Final[str] = "HIGH"

# Failure codes.
F_BT12_01: Final[str] = "F-BT12-01"  # opt_in=False
F_BT12_02: Final[str] = "F-BT12-02"  # per-org denylist hit
F_BT12_03: Final[str] = "F-BT12-03"  # unknown jurisdiction
F_BT12_04: Final[str] = "F-BT12-04"  # jurisdiction not in allowlist
F_BT12_05: Final[str] = "F-BT12-05"  # vault_read malformed / identity mismatch
F_BT12_06: Final[str] = "F-BT12-06"  # Punycode / UTS46 failure
F_BT12_07: Final[str] = "F-BT12-07"  # post-read intent mismatch

F_SCOUT_F_01: Final[str] = "F-SCOUT-F-01"  # fetch failed post pre-flight
F_SCOUT_F_02: Final[str] = "F-SCOUT-F-02"  # first-hop unreachable
F_SCOUT_F_03: Final[str] = "F-SCOUT-F-03"  # parse error
F_SCOUT_F_04: Final[str] = "F-SCOUT-F-04"  # FD release path tag (informational)
F_SCOUT_F_05: Final[str] = "F-SCOUT-F-05"  # vault_read raised before identity check
F_SCOUT_F_06: Final[str] = "F-SCOUT-F-06"  # content-body hash mismatch (future)


# ---------------------------------------------------------------------------
# Injection Protocols (E-017 pattern mirrored from Round 2 / Round 6)
# ---------------------------------------------------------------------------


class IdentityTupleLike(Protocol):
    """Duck-type mirror of Section 2 IdentityTuple for vault_read returns.

    Kept here (not re-imported from :mod:`channel_b_cache`) so Channel F
    owns its read-path contract end-to-end and can evolve independently
    without cross-channel coupling.
    """

    intent: str
    session_id: str
    slug: str


class VaultReader(Protocol):
    """§2 vault-read seam — loads the per-org policy file only.

    Production binding is :class:`Section2VaultReader` in
    :mod:`pipeline.scout._vault_reader_adapter`. Tests inject a memory
    reader that returns pre-seeded bytes + IdentityTuple (E-017).
    """

    def read(
        self,
        *,
        path: str,
        intent: str,
        session_id: str,
        slug: str,
    ) -> tuple[bytes, IdentityTupleLike]: ...


# ---------------------------------------------------------------------------
# Exceptions — all fail-closed, one per reason tag
# ---------------------------------------------------------------------------


class ChannelFNotOptedIn(RuntimeError):
    """Raised when the per-org policy has ``opt_in=False`` (F-BT12-01)."""


class ChannelFJurisdictionReject(RuntimeError):
    """Raised for F-BT12-02..04 (denylist / unknown / not-allowed)."""

    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code


class ChannelFURLPunycodeError(RuntimeError):
    """Raised when ``idna.encode`` rejects the URL's host (F-BT12-06)."""


class ChannelFPolicyVaultReadMismatch(RuntimeError):
    """Raised for malformed / identity-mismatched vault_read (F-BT12-05 / -07)."""

    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ChannelFQuery:
    """Operator-approved single query plan entry.

    Scout does NOT construct queries — it receives an operator-approved
    ``ChannelFQuery`` plan. Query construction is Scribe / operator
    responsibility.
    """

    query_text: str
    max_results: int = _CHANNEL_F_MAX_RESULTS_PER_QUERY
    hydrate_clickthrough: bool = False


@dataclass(frozen=True, kw_only=True)
class ChannelFJurisdictionPolicy:
    """Per-org Channel F policy file contents.

    Parsed from ``orgs/{slug}/scout/channel_f_policy.yaml`` via
    :class:`VaultReader`. Default-deny posture: every field defaults to
    the most restrictive value.
    """

    opt_in: bool = False
    allowed_jurisdictions: frozenset[str] = field(default_factory=frozenset)
    disallowed_registrable_domains: frozenset[str] = field(
        default_factory=frozenset
    )
    searxng_port: int = 8888
    provider: str = PROVIDER_SEARXNG  # "searxng" | "brave"


@dataclass(frozen=True, kw_only=True)
class ChannelFDegradationEvent:
    """One-line per-request event record (M7 aggregation)."""

    source: str
    code: str
    reason_tag: Optional[str]
    severity: str


@dataclass(frozen=True, kw_only=True)
class ChannelFDisclosureRow:
    """Per-outbound-hop disclosure record. Domain + count only.

    No query text. No body excerpt. §4.6 line 598 guards against exfiltration
    via the disclosure surface; R3 AST-lint blocks the most obvious escape
    path, the tests in ``TestChannelFDisclosureRows`` nail it down.
    """

    domain: str
    count: int
    hop: str  # "first" | "click_through"
    timestamp_utc: str


@dataclass(frozen=True, kw_only=True)
class ChannelFDiscoverResult:
    candidates: tuple[Candidate, ...]
    channel_state: str
    degradation_events: tuple[ChannelFDegradationEvent, ...]
    disclosure_rows: tuple[ChannelFDisclosureRow, ...]
    preflight_reject_count: int


# ---------------------------------------------------------------------------
# Helpers — pure, deterministic
# ---------------------------------------------------------------------------


def _default_clock() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


def _fresh_nonce() -> str:
    return os.urandom(32).hex()


def _assert_intent_matches(
    identity: IdentityTupleLike,
    session: SessionLike,
    expected_intent: str,
) -> Optional[str]:
    """Return ``None`` on strict-equality match, or a reason tag on drift.

    NFC-normalised equality is the fallback diagnosis: an NFC-matched but
    strictly-different intent is still rejected (defence-in-depth per
    A-v3-04).
    """
    if identity.session_id != session.session_id:
        return f"session_id_mismatch:expected={session.session_id!r}"
    if identity.slug != session.slug:
        return f"slug_mismatch:expected={session.slug!r}"
    if identity.intent == expected_intent:
        return None
    normalized = unicodedata.normalize("NFC", identity.intent).strip()
    if normalized == expected_intent:
        return f"intent_nfc_drift:{identity.intent!r}"
    return f"intent_mismatch:{identity.intent!r}"


def _parse_policy_bytes(data: bytes) -> Optional[ChannelFJurisdictionPolicy]:
    """Parse the vault-returned policy YAML into :class:`ChannelFJurisdictionPolicy`.

    Returns ``None`` on any parse / type error. Callers convert that into
    a ``F-BT12-05`` fail-closed response.
    """
    try:
        import yaml  # Lazy — only imported when policy parsing runs.

        parsed = yaml.safe_load(data)
    except Exception:
        return None
    if not isinstance(parsed, Mapping):
        return None
    try:
        opt_in = bool(parsed.get("opt_in", False))
        allowed_raw = parsed.get("allowed_jurisdictions", [])
        disallowed_raw = parsed.get("disallowed_registrable_domains", [])
        if not isinstance(allowed_raw, (list, tuple, set, frozenset)):
            return None
        if not isinstance(disallowed_raw, (list, tuple, set, frozenset)):
            return None
        allowed = frozenset(str(x) for x in allowed_raw)
        disallowed = frozenset(str(x) for x in disallowed_raw)
        searxng_port_raw = parsed.get("searxng_port", 8888)
        if not isinstance(searxng_port_raw, int) or isinstance(
            searxng_port_raw, bool
        ):
            return None
        provider = str(parsed.get("provider", PROVIDER_SEARXNG))
        if provider not in (PROVIDER_SEARXNG, PROVIDER_BRAVE):
            return None
        return ChannelFJurisdictionPolicy(
            opt_in=opt_in,
            allowed_jurisdictions=allowed,
            disallowed_registrable_domains=disallowed,
            searxng_port=searxng_port_raw,
            provider=provider,
        )
    except (TypeError, ValueError):  # pragma: no cover - defensive fallback
        return None


def _load_channel_f_policy(
    session: SessionLike,
    vault_reader: VaultReader,
) -> ChannelFJurisdictionPolicy:
    """Load + validate the per-org policy. Fail-closed on every error path.

    Raises :class:`ChannelFPolicyVaultReadMismatch` (F-BT12-05 / F-BT12-07)
    when the vault returns malformed bytes or a mismatched IdentityTuple,
    and re-raises :class:`FileNotFoundError` unchanged so callers can
    opt-out-short-circuit on a missing policy.
    """
    path = f"orgs/{session.slug}/scout/channel_f_policy.yaml"
    try:
        data, identity = vault_reader.read(
            path=path,
            intent=_INTENT_CHANNEL_F_POLICY_READ,
            session_id=session.session_id,
            slug=session.slug,
        )
    except FileNotFoundError:
        raise
    except Exception as exc:
        raise ChannelFPolicyVaultReadMismatch(
            f"{F_SCOUT_F_05}: vault_read raised before identity check: "
            f"{type(exc).__name__}:{exc}",
            code=F_SCOUT_F_05,
        ) from exc

    drift = _assert_intent_matches(
        identity, session, _INTENT_CHANNEL_F_POLICY_READ
    )
    if drift is not None:
        code = (
            F_BT12_07
            if drift.startswith("intent_nfc_drift")
            or drift.startswith("intent_mismatch")
            else F_BT12_05
        )
        raise ChannelFPolicyVaultReadMismatch(
            f"{code}: identity-tuple drift: {drift}", code=code
        )

    policy = _parse_policy_bytes(data)
    if policy is None:
        raise ChannelFPolicyVaultReadMismatch(
            f"{F_BT12_05}: policy bytes did not parse to a valid policy mapping",
            code=F_BT12_05,
        )
    return policy


def _registrable_domain(candidate_url: str) -> str:
    """Return the registrable domain in lower-cased ASCII Punycode form.

    Raises :class:`ChannelFURLPunycodeError` (F-BT12-06) on invalid URL
    or Punycode/UTS46 failure. ``idna`` is lazy-imported to keep the
    dispatcher's import footprint stdlib-adjacent.
    """
    try:
        import idna  # Lazy — see module docstring.

        parsed = urllib.parse.urlsplit(candidate_url)
        host = parsed.hostname
        if not host:
            raise ChannelFURLPunycodeError(
                f"{F_BT12_06}: url has no hostname component: {candidate_url!r}"
            )
        ascii_host = idna.encode(host, uts46=True).decode("ascii").lower()
    except ChannelFURLPunycodeError:
        raise
    except Exception as exc:
        raise ChannelFURLPunycodeError(
            f"{F_BT12_06}: idna.encode rejected host "
            f"{candidate_url!r}: {type(exc).__name__}:{exc}"
        ) from exc
    labels = ascii_host.split(".")
    if len(labels) < 2:
        # A bare TLD isn't registrable — default-deny.
        return ascii_host
    return ".".join(labels[-2:])


def _jurisdiction_from_registrable_domain(reg: str) -> Optional[str]:
    """Resolve a registrable domain to its ISO-3166-1 alpha-2 jurisdiction.

    Returns ``None`` for unknown eTLDs — BT12 default-deny applies.
    """
    from pipeline.scout._channel_f_jurisdictions import jurisdiction_for_etld

    if not reg:
        return None
    last_label = reg.rsplit(".", 1)[-1]
    return jurisdiction_for_etld(last_label)


def _is_loopback_host(candidate_url: str) -> bool:
    """Return True when ``candidate_url``'s host is an IPv4/IPv6 loopback.

    The SearxNG first-hop is always loopback (``127.0.0.1`` / ``::1`` on
    the Golden Quill). Loopback traffic never leaves the host, so §4.6
    treats it as the jurisdiction-neutral lane and BT12 pre-flight
    accepts it trivially (opt_in still required).
    """
    try:
        import ipaddress

        host = urllib.parse.urlsplit(candidate_url).hostname or ""
        if not host:
            return False
        return ipaddress.ip_address(host).is_loopback
    except (ValueError, TypeError):
        return False


def _preflight_channel_f(
    session: SessionLike,
    candidate_url: str,
    policy: ChannelFJurisdictionPolicy,
) -> None:
    """Run BT12 pre-flight on ``candidate_url`` against ``policy``.

    Raises one of :class:`ChannelFNotOptedIn`,
    :class:`ChannelFJurisdictionReject`, or
    :class:`ChannelFURLPunycodeError` on any rejection. Returns ``None``
    on accept. Caller MUST invoke this BEFORE any ``fd_broker.request_fd``.
    """
    if not policy.opt_in:
        raise ChannelFNotOptedIn(
            f"{F_BT12_01}: slug={session.slug} has not opted into Channel F"
        )
    # Loopback lane: SearxNG runs on the Golden Quill itself. Traffic never
    # leaves the box — no jurisdiction applies. Still fail-closed on opt_in
    # (checked above).
    if _is_loopback_host(candidate_url):
        return
    reg = _registrable_domain(candidate_url)
    if reg in policy.disallowed_registrable_domains:
        raise ChannelFJurisdictionReject(
            f"{F_BT12_02}: domain {reg} is on per-org denylist",
            code=F_BT12_02,
        )
    tld_jurisdiction = _jurisdiction_from_registrable_domain(reg)
    if tld_jurisdiction is None:
        raise ChannelFJurisdictionReject(
            f"{F_BT12_03}: domain {reg} has no known jurisdiction "
            f"— default-deny",
            code=F_BT12_03,
        )
    if tld_jurisdiction not in policy.allowed_jurisdictions:
        raise ChannelFJurisdictionReject(
            f"{F_BT12_04}: domain {reg} jurisdiction {tld_jurisdiction} "
            f"not in allowed_jurisdictions "
            f"{sorted(policy.allowed_jurisdictions)}",
            code=F_BT12_04,
        )


def _build_channel_f_candidate(
    *,
    provider: str,
    canonical_search_url: str,
    result_url: str,
    title: str,
    body_hash: str,
    fetch_timestamp_utc: str,
) -> Candidate:
    """Compose a :class:`Candidate` for a single Channel F hit.

    A-v3-09 analogue: ``feed_or_adapter_id`` is
    ``f"{FEED_PREFIX_WEBSEARCH}{provider}:{sha3_512(canonical_search_url)[:16]}"``.
    """
    if provider not in (PROVIDER_SEARXNG, PROVIDER_BRAVE):
        raise ValueError(
            f"provider must be one of {{{PROVIDER_SEARXNG!r}, "
            f"{PROVIDER_BRAVE!r}}}, got {provider!r}"
        )
    canonical_hash = hashlib.sha3_512(
        canonical_search_url.encode("utf-8")
    ).hexdigest()[:16]
    feed_id = f"{FEED_PREFIX_WEBSEARCH}{provider}:{canonical_hash}"
    url_hash = hashlib.sha3_512(result_url.encode("utf-8")).hexdigest()
    return Candidate(
        candidate_id=f"channel-f:{canonical_hash}:{url_hash[:16]}",
        channel=CHANNEL_F,
        feed_or_adapter_id=feed_id,
        source_key=canonical_search_url,
        title=title,
        funder="",
        funder_kind="unknown",
        url=result_url,
        close_date_utc=None,
        award_ceiling=None,
        award_floor=None,
        applicant_types=(),
        program_page_url=None,
        fetch_timestamp_utc=fetch_timestamp_utc,
        url_hash=url_hash,
        content_hash=body_hash,
        fit_score_cached=0,
        cache_provenance=None,
    )


# ---------------------------------------------------------------------------
# FD-owning fetch helpers — EVERY ``fd_broker.request_fd`` LIVES INSIDE
# ``if _CHANNEL_F_PREFLIGHT_GATE:`` (ARCH-05 R7 dominance).
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class _FetchOutcome:
    response: Optional[HTTPResponse]
    path_tag: str  # one of F-SCOUT-F-04 taxonomy
    error_tag: Optional[str]


def _fetch_one(
    *,
    http_client: HTTPClient,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    host: str,
    method: str,
    url: str,
    headers: Mapping[str, str],
    body: Optional[bytes],
) -> _FetchOutcome:
    """Single-try fetch with strict ``try/finally`` FD + nonce release.

    **Preflight MUST have run in the caller before we reach this function.**
    The call to ``fd_broker.request_fd`` is CFG-dominated by
    ``_CHANNEL_F_PREFLIGHT_GATE`` to satisfy ARCH-05 R7. No retries (§4.6
    Channel F policy decision).
    """
    nonce_hex = _fresh_nonce()
    path_tag_final = "exception"

    try:
        nonce_registry.reserve(nonce_hex)
    except Exception as exc:
        return _FetchOutcome(
            response=None,
            path_tag="exception",
            error_tag=f"nonce_reserve_failed:{type(exc).__name__}:{exc}",
        )

    try:
        if _CHANNEL_F_PREFLIGHT_GATE:
            try:
                fd = fd_broker.request_fd(kind="https", host=host)
            except Exception as exc:
                path_tag_final = "exception"
                return _FetchOutcome(
                    response=None,
                    path_tag="exception",
                    error_tag=f"fd_request_failed:{type(exc).__name__}:{exc}",
                )
            try:
                try:
                    response = http_client.request(
                        method,
                        url,
                        headers=headers,
                        body=body,
                        connect_timeout_s=_CHANNEL_F_CONNECT_TIMEOUT_S,
                        read_timeout_s=_CHANNEL_F_READ_TIMEOUT_S,
                    )
                except (TimeoutError, socket.timeout) as exc:
                    path_tag_final = "fetch_error"
                    return _FetchOutcome(
                        response=None,
                        path_tag="fetch_error",
                        error_tag=f"timeout:{type(exc).__name__}",
                    )
                except (ConnectionResetError, ConnectionError) as exc:
                    path_tag_final = "fetch_error"
                    return _FetchOutcome(
                        response=None,
                        path_tag="fetch_error",
                        error_tag=f"connection_error:{type(exc).__name__}",
                    )
                except Exception as exc:  # noqa: BLE001
                    path_tag_final = "exception"
                    return _FetchOutcome(
                        response=None,
                        path_tag="exception",
                        error_tag=(
                            f"http_client_raised:{type(exc).__name__}:{exc}"
                        ),
                    )
                status = response.status
                if 200 <= status < 300:
                    path_tag_final = "success"
                    return _FetchOutcome(
                        response=response,
                        path_tag="success",
                        error_tag=None,
                    )
                path_tag_final = "fetch_error"
                return _FetchOutcome(
                    response=response,
                    path_tag="fetch_error",
                    error_tag=f"http_{status}",
                )
            finally:
                fd_broker.release_fd(fd)
        else:  # pragma: no cover - sentinel is Final[bool]=True
            return _FetchOutcome(
                response=None,
                path_tag="preflight_reject_after_acquire",
                error_tag="preflight_gate_disabled",
            )
    finally:
        nonce_registry.release(nonce_hex, path_tag=path_tag_final)


# ---------------------------------------------------------------------------
# Result parsing (SearxNG / Brave — identical shape for Round 7)
# ---------------------------------------------------------------------------


def _parse_results(body: bytes) -> Optional[tuple[dict, ...]]:
    """Parse JSON result bodies.

    Both SearxNG (``/search?format=json``) and Brave
    (``/res/v1/web/search``) return JSON with a top-level ``results``
    array whose entries carry ``url`` + ``title``. Brave's schema nests
    under ``web.results``; SearxNG's is flat. Returns ``None`` on any
    decode error — caller emits ``F-SCOUT-F-03``.
    """
    import json

    try:
        parsed = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    if not isinstance(parsed, dict):
        return None
    results = parsed.get("results")
    if results is None:
        web = parsed.get("web")
        if isinstance(web, dict):
            results = web.get("results")
    if not isinstance(results, list):
        return None
    out: list[dict] = []
    for row in results:
        if not isinstance(row, dict):
            continue
        if "url" not in row or "title" not in row:
            continue
        out.append(row)
    return tuple(out)


# ---------------------------------------------------------------------------
# Main dispatcher
# ---------------------------------------------------------------------------


def _canonical_search_url(provider: str, query: str, policy: ChannelFJurisdictionPolicy) -> str:
    if provider == PROVIDER_SEARXNG:
        return (
            f"https://{SEARXNG_HOST}:{policy.searxng_port}/search?"
            f"format=json&q={urllib.parse.quote(query)}"
        )
    if provider == PROVIDER_BRAVE:
        return (
            f"https://{BRAVE_HOST}/res/v1/web/search?"
            f"q={urllib.parse.quote(query)}"
        )
    raise ValueError(f"unknown provider {provider!r}")


def discover_channel_f(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    http_client: HTTPClient,
    vault_reader: VaultReader,
    query_plan: tuple[ChannelFQuery, ...],
    clock: ClockFn = _default_clock,  # type: ignore[assignment]
) -> ChannelFDiscoverResult:
    """§4.6 Channel F DISCOVER entry point.

    Two guarantees the public test surface leans on:

    1. **Pre-flight strictly dominates every FD request** (A-06 + ARCH-05 R7).
    2. **Opt-out short-circuit is silent** — missing policy or
       ``opt_in=False`` returns an empty OK-trivially result with zero FD
       requests, zero nonces reserved, zero downstream work.
    """
    events: list[ChannelFDegradationEvent] = []
    disclosures: list[ChannelFDisclosureRow] = []
    candidates: list[Candidate] = []
    preflight_reject_count = 0
    channel_state = HEALTH_OK

    def _now_iso() -> str:
        now = clock() if callable(clock) else _default_clock()
        if isinstance(now, _dt.datetime):
            if now.tzinfo is None:
                now = now.replace(tzinfo=_dt.timezone.utc)
            return now.astimezone(_dt.timezone.utc).isoformat()
        return str(now)

    # -- Policy load + opt-out short-circuit ---------------------------------

    try:
        policy = _load_channel_f_policy(session, vault_reader)
    except FileNotFoundError:
        return ChannelFDiscoverResult(
            candidates=(),
            channel_state=HEALTH_OK,
            degradation_events=(),
            disclosure_rows=(),
            preflight_reject_count=0,
        )
    except ChannelFPolicyVaultReadMismatch as exc:
        events.append(
            ChannelFDegradationEvent(
                source="policy_load",
                code=exc.code,
                reason_tag=str(exc),
                severity=SEVERITY_HIGH,
            )
        )
        return ChannelFDiscoverResult(
            candidates=(),
            channel_state=HEALTH_OK,
            degradation_events=tuple(events),
            disclosure_rows=(),
            preflight_reject_count=0,
        )

    if not policy.opt_in:
        # Opt-out short-circuit: no traffic, state OK-trivially.
        return ChannelFDiscoverResult(
            candidates=(),
            channel_state=HEALTH_OK,
            degradation_events=(),
            disclosure_rows=(),
            preflight_reject_count=0,
        )

    provider = policy.provider
    if provider == PROVIDER_BRAVE:
        if _BRAVE_BYOK_JURISDICTION not in policy.allowed_jurisdictions:
            events.append(
                ChannelFDegradationEvent(
                    source="brave_byok_guard",
                    code=F_BT12_04,
                    reason_tag=(
                        f"provider=brave but {_BRAVE_BYOK_JURISDICTION!r} "
                        "not in allowed_jurisdictions"
                    ),
                    severity=SEVERITY_LOW,
                )
            )
            preflight_reject_count += 1
            return ChannelFDiscoverResult(
                candidates=(),
                channel_state=HEALTH_OK,
                degradation_events=tuple(events),
                disclosure_rows=(),
                preflight_reject_count=preflight_reject_count,
            )

    capped_plan = query_plan[:_CHANNEL_F_MAX_QUERIES_PER_RUN]

    any_first_hop_attempted = False
    any_first_hop_succeeded = False
    any_first_hop_failed = False

    # -- Per-query dispatch --------------------------------------------------

    for query in capped_plan:
        search_url = _canonical_search_url(provider, query.query_text, policy)
        first_host = SEARXNG_HOST if provider == PROVIDER_SEARXNG else BRAVE_HOST

        # First-hop pre-flight — trivially accept for SearxNG localhost (we
        # still run the full pre-flight call to keep the dominance discipline
        # uniform).
        if provider == PROVIDER_SEARXNG:
            # SearxNG pre-flight runs the full guard, but ``_is_loopback_host``
            # short-circuits accept for 127.0.0.1 / ::1. We still run the call
            # so the dominance discipline stays uniform across providers — if
            # the loopback accept is ever removed, the rejection branch below
            # is the fail-closed path.
            try:
                _preflight_channel_f(session, search_url, policy=policy)
            except (  # pragma: no cover - unreachable under loopback-accept
                ChannelFNotOptedIn,
                ChannelFJurisdictionReject,
                ChannelFURLPunycodeError,
            ):
                preflight_reject_count += 1
                events.append(
                    ChannelFDegradationEvent(
                        source="first_hop_preflight",
                        code=F_SCOUT_F_04,
                        reason_tag="searxng_first_hop_preflight_reject",
                        severity=SEVERITY_LOW,
                    )
                )
                continue
        else:
            try:
                _preflight_channel_f(session, search_url, policy=policy)
            except ChannelFNotOptedIn as exc:  # pragma: no cover - opt_in already checked above
                preflight_reject_count += 1
                events.append(
                    ChannelFDegradationEvent(
                        source="first_hop_preflight",
                        code=F_BT12_01,
                        reason_tag=str(exc),
                        severity=SEVERITY_LOW,
                    )
                )
                continue
            except ChannelFJurisdictionReject as exc:
                preflight_reject_count += 1
                events.append(
                    ChannelFDegradationEvent(
                        source="first_hop_preflight",
                        code=exc.code,
                        reason_tag=str(exc),
                        severity=SEVERITY_LOW,
                    )
                )
                continue
            except ChannelFURLPunycodeError as exc:  # pragma: no cover - BRAVE_HOST constant is always valid
                preflight_reject_count += 1
                events.append(
                    ChannelFDegradationEvent(
                        source="first_hop_preflight",
                        code=F_BT12_06,
                        reason_tag=str(exc),
                        severity=SEVERITY_LOW,
                    )
                )
                continue

        any_first_hop_attempted = True

        # Disclosure row for first-hop (regardless of fetch outcome — we
        # record the attempt).
        disclosures.append(
            ChannelFDisclosureRow(
                domain=first_host,
                count=1,
                hop="first",
                timestamp_utc=_now_iso(),
            )
        )

        outcome = _fetch_one(
            http_client=http_client,
            fd_broker=fd_broker,
            nonce_registry=nonce_registry,
            host=first_host,
            method="GET",
            url=search_url,
            headers={},
            body=None,
        )

        events.append(
            ChannelFDegradationEvent(
                source="first_hop_release",
                code=F_SCOUT_F_04,
                reason_tag=outcome.path_tag,
                severity=SEVERITY_LOW,
            )
        )

        if outcome.response is None or outcome.path_tag != "success":
            any_first_hop_failed = True
            events.append(
                ChannelFDegradationEvent(
                    source="first_hop",
                    code=F_SCOUT_F_01,
                    reason_tag=outcome.error_tag,
                    severity=SEVERITY_MEDIUM,
                )
            )
            continue

        any_first_hop_succeeded = True

        parsed = _parse_results(outcome.response.body_bytes)
        if parsed is None:
            any_first_hop_failed = True
            events.append(
                ChannelFDegradationEvent(
                    source="parse",
                    code=F_SCOUT_F_03,
                    reason_tag="json_decode_or_schema_error",
                    severity=SEVERITY_MEDIUM,
                )
            )
            continue

        # -- Click-through loop ---------------------------------------------

        for row in parsed[: query.max_results]:
            result_url = str(row.get("url", ""))
            title = str(row.get("title", ""))
            if not result_url:
                continue

            if query.hydrate_clickthrough:
                # Second-hop pre-flight — MUST run before the second FD.
                try:
                    _preflight_channel_f(session, result_url, policy=policy)
                except (
                    ChannelFNotOptedIn,
                    ChannelFJurisdictionReject,
                    ChannelFURLPunycodeError,
                ) as exc:
                    preflight_reject_count += 1
                    code = getattr(exc, "code", F_BT12_01)
                    events.append(
                        ChannelFDegradationEvent(
                            source="click_through_preflight",
                            code=code,
                            reason_tag=str(exc),
                            severity=SEVERITY_LOW,
                        )
                    )
                    continue

                click_host = (
                    urllib.parse.urlsplit(result_url).hostname or ""
                )
                disclosures.append(
                    ChannelFDisclosureRow(
                        domain=click_host,
                        count=1,
                        hop="click_through",
                        timestamp_utc=_now_iso(),
                    )
                )
                click_outcome = _fetch_one(
                    http_client=http_client,
                    fd_broker=fd_broker,
                    nonce_registry=nonce_registry,
                    host=click_host,
                    method="GET",
                    url=result_url,
                    headers={},
                    body=None,
                )
                events.append(
                    ChannelFDegradationEvent(
                        source="click_through_release",
                        code=F_SCOUT_F_04,
                        reason_tag=click_outcome.path_tag,
                        severity=SEVERITY_LOW,
                    )
                )
                if click_outcome.response is None or click_outcome.path_tag != "success":
                    any_first_hop_failed = True
                    events.append(
                        ChannelFDegradationEvent(
                            source="click_through",
                            code=F_SCOUT_F_01,
                            reason_tag=click_outcome.error_tag,
                            severity=SEVERITY_MEDIUM,
                        )
                    )
                    continue
                body_bytes_local = click_outcome.response.body_bytes
            else:
                body_bytes_local = b""

            body_hash = hashlib.sha3_512(body_bytes_local).hexdigest()
            candidates.append(
                _build_channel_f_candidate(
                    provider=provider,
                    canonical_search_url=search_url,
                    result_url=result_url,
                    title=title,
                    body_hash=body_hash,
                    fetch_timestamp_utc=_now_iso(),
                )
            )

    # -- Channel state aggregation ------------------------------------------

    if any_first_hop_attempted:
        if any_first_hop_failed and any_first_hop_succeeded:
            channel_state = HEALTH_DEGRADED
        elif any_first_hop_failed and not any_first_hop_succeeded:
            channel_state = HEALTH_FAILED
        else:
            channel_state = HEALTH_OK
    else:
        # Everything was pre-flight-rejected before any fetch. State OK per
        # spec-card §14 ("Pre-flight rejections do NOT flip channel state").
        channel_state = HEALTH_OK

    return ChannelFDiscoverResult(
        candidates=tuple(candidates),
        channel_state=channel_state,
        degradation_events=tuple(events),
        disclosure_rows=tuple(disclosures),
        preflight_reject_count=preflight_reject_count,
    )
