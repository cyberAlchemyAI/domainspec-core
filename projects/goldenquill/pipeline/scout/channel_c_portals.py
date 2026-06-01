"""Channel C — Seeded state + foundation portals (§4.3).

Adapter-per-portal registry dispatcher. Each adapter is a small callable
registered at module-import time in a module-level ``OrderedDict`` keyed by
canonical slug. Per-org opt-in is expressed as a ``portal_roster`` tuple
passed to :func:`discover_channel_c`; no portal is auto-enabled.

Blueprint anchors:
- §4.3 Channel C full spec (lines 493-519) — implementation target
- §2.1 ``Candidate`` schema (Round 1 ``_types.py``)
- §6.2 F-SCOUT-C-01..03 failure codes (+ F-SCOUT-C-02 wrapper for runtime
  adapter exceptions)
- §8 no Channel C-specific pins in Round 5 (timeouts reuse §8's
  ``CHANNEL_A_*`` constants per the Round 5 spec card §7)
- §2.1 Candidate.feed_or_adapter_id prefix ``"portal:"`` (A-v3-09 closure)

Registration model — A-v3-09 closure.
  ``register_portal(portal_slug)`` canonicalises the raw slug via the
  Section 1 primitive ``canonical_slug`` (``pipeline.sovereignty.org_slug``)
  then rejects any duplicate canonical slug with
  ``ScoutConfigError(F-SCOUT-C-03)``. Detection is import-time deterministic
  — operator-typo collisions surface immediately, not at run-time.

Adapter contract.
  Adapters are plain callables ``(AdapterContext) -> PortalAdapterOutcome``.
  They MAY use :func:`http_request_with_retries` for HTTP fetches (shared
  with Channel D, reuses Round 4's retry ladder). Adapters MUST build each
  ``Candidate.feed_or_adapter_id`` as ``"portal:<cslug>"`` — the helper
  :func:`_build_channel_c_candidate` asserts this.

Channel-C state aggregation — §4.3 line 517.
  ``≥ 50 %`` of registered portals FAILED → FAILED; any other partial
  failure → DEGRADED; all OK → OK. Denominator is the roster length, not
  the registry length — a portal in the roster but missing from the
  registry counts as FAILED toward the 50 % threshold.

No module-level side effects on import. Zero network, zero FD reservation,
zero nonce reservation. Registration decorators store adapter callables in
the module-level ``PORTAL_ADAPTERS`` dict — that is the intended side
effect of the import, and is idempotent under re-import.
"""

from __future__ import annotations

import datetime as _dt
import os
import socket
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Callable, Final, Iterator, Mapping, Optional, Protocol

from pipeline.scout._constants import (
    CHANNEL_A_CONNECT_TIMEOUT_S,
    CHANNEL_A_READ_TIMEOUT_S,
    CHANNEL_A_RETRY_COUNT,
    CHANNEL_C,
    FEED_PREFIX_PORTAL,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
)
from pipeline.scout._types import Candidate
from pipeline.scout.channel_a_federal_apis import (
    ClockFn,
    FDBroker,
    HTTPClient,
    HTTPResponse,
    NonceRegistry,
    SessionLike,
)
from pipeline.sovereignty import (
    InvalidSlug,
    ReservedSlug,
    canonical_slug,
)

__all__ = [
    "AdapterContext",
    "ChannelCDegradationEvent",
    "ChannelCDiscoverResult",
    "PORTAL_ADAPTERS",
    "PortalAdapter",
    "PortalAdapterOutcome",
    "PortalSubEvent",
    "ScoutConfigError",
    "_build_channel_c_candidate",
    "_canonical_portal_slug",
    "channel_c_reset_registry_for_tests",
    "classify_channel_c",
    "discover_channel_c",
    "http_request_with_retries",
    "register_portal",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


_RETRY_SLEEP_SCHEDULE: Final[tuple[float, ...]] = (1.0, 2.0, 4.0)

SEVERITY_LOW: Final[str] = "LOW"
SEVERITY_MEDIUM: Final[str] = "MEDIUM"
SEVERITY_HIGH: Final[str] = "HIGH"

F_SCOUT_C_01: Final[str] = "F-SCOUT-C-01"
F_SCOUT_C_02: Final[str] = "F-SCOUT-C-02"
F_SCOUT_C_03: Final[str] = "F-SCOUT-C-03"


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ScoutConfigError(Exception):
    """Import-time configuration error raised by Channel C/D registry.

    Raised on duplicate canonical slug at ``register_portal`` and on
    duplicate ALN at ``register_program_page``. Always carries a failure
    code prefix in ``args[0]``.
    """


# ---------------------------------------------------------------------------
# Shared adapter infrastructure (imported by Channel D)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class AdapterContext:
    """Per-run context handed to each adapter callable.

    Adapters MAY use :func:`http_request_with_retries` against the bundled
    ``http_client`` + ``fd_broker`` + ``nonce_registry``. They SHOULD NOT
    call the protocols directly — doing so bypasses the retry ladder and
    path-tag discipline.

    Held by reference; adapters MUST NOT mutate ``session`` / ``clock``.
    """

    session: SessionLike
    fd_broker: FDBroker
    nonce_registry: NonceRegistry
    http_client: HTTPClient
    clock: ClockFn


@dataclass(frozen=True, kw_only=True)
class _CallResult:
    """Outcome of one logical HTTP request through the shared retry ladder."""

    state: str
    response: Optional[HTTPResponse]
    outcome_tag: str  # "success" / "success_after_retry" / "http_4xx" / "retries_exhausted" / "fd_error" / "nonce_error" / "exception"
    path_tag: str
    error_tag: Optional[str]


def _fresh_nonce() -> str:
    return os.urandom(32).hex()


def _do_request_with_retries(
    *,
    http_client: HTTPClient,
    clock: ClockFn,
    method: str,
    url: str,
    headers: Mapping[str, str],
    body: Optional[bytes],
) -> tuple[Optional[HTTPResponse], str, str, Optional[str]]:
    """Run the retry ladder for a single logical request.

    Returns ``(response, outcome_tag, path_tag, error_tag)``. Matches
    Round 4's ``_do_request_with_retries`` shape; ``outcome_tag`` ∈
    ``{success, success_after_retry, http_4xx, retries_exhausted}``.
    """
    error_tag: Optional[str] = None
    path_tag = "http_error"

    for attempt in range(CHANNEL_A_RETRY_COUNT + 1):
        if attempt > 0:
            clock.sleep(_RETRY_SLEEP_SCHEDULE[attempt - 1])

        try:
            response = http_client.request(
                method,
                url,
                headers=headers,
                body=body,
                connect_timeout_s=CHANNEL_A_CONNECT_TIMEOUT_S,
                read_timeout_s=CHANNEL_A_READ_TIMEOUT_S,
            )
        except (TimeoutError, socket.timeout) as exc:
            path_tag = "timeout"
            error_tag = f"timeout:attempt={attempt}:{type(exc).__name__}"
            continue
        except (ConnectionResetError, ConnectionError) as exc:
            path_tag = "connection_reset"
            error_tag = (
                f"connection_reset:attempt={attempt}:{type(exc).__name__}"
            )
            continue

        status = response.status
        if 200 <= status < 300:
            return (
                response,
                "success" if attempt == 0 else "success_after_retry",
                "success",
                error_tag,
            )
        if 400 <= status < 500:
            return (
                response,
                "http_4xx",
                "http_error",
                f"http_{status}",
            )
        path_tag = "http_error"
        error_tag = f"http_{status}:attempt={attempt}"

    return (None, "retries_exhausted", path_tag, error_tag)


def http_request_with_retries(
    ctx: AdapterContext,
    *,
    method: str,
    url: str,
    host: str,
    headers: Optional[Mapping[str, str]] = None,
    body: Optional[bytes] = None,
) -> _CallResult:
    """Adapter-visible HTTP helper sharing Round 4's nonce + FD + retry discipline.

    Reserves a nonce BEFORE requesting an FD, releases FD first then nonce
    at every exit path (including exception paths). Runs the retry ladder
    ``CHANNEL_A_RETRY_COUNT + 1`` attempts with ``(1.0, 2.0, 4.0)`` s
    sleeps via ``ctx.clock.sleep``. Returns a :class:`_CallResult` whose
    ``state`` is the per-call HEALTH_* value and ``response`` carries the
    HTTPResponse on 2xx/4xx (None on retries_exhausted / FD / nonce /
    exception paths).

    ``host`` is the hostname passed to ``ctx.fd_broker.request_fd`` so the
    FD broker can enforce per-host policy.
    """
    nonce_hex = _fresh_nonce()
    path_tag_final = "exception"
    request_headers: Mapping[str, str] = headers if headers is not None else {}

    try:
        ctx.nonce_registry.reserve(nonce_hex)
    except Exception as exc:
        return _CallResult(
            state=HEALTH_FAILED,
            response=None,
            outcome_tag="nonce_error",
            path_tag="exception",
            error_tag=f"nonce_reserve_failed:{type(exc).__name__}:{exc}",
        )

    try:
        try:
            fd = ctx.fd_broker.request_fd(kind="https", host=host)
        except Exception as exc:
            path_tag_final = "exception"
            return _CallResult(
                state=HEALTH_FAILED,
                response=None,
                outcome_tag="fd_error",
                path_tag="exception",
                error_tag=f"fd_request_failed:{type(exc).__name__}:{exc}",
            )

        try:
            try:
                (
                    response,
                    outcome_tag,
                    path_tag_retry,
                    error_tag,
                ) = _do_request_with_retries(
                    http_client=ctx.http_client,
                    clock=ctx.clock,
                    method=method,
                    url=url,
                    headers=request_headers,
                    body=body,
                )
            except Exception as exc:
                path_tag_final = "exception"
                return _CallResult(
                    state=HEALTH_FAILED,
                    response=None,
                    outcome_tag="exception",
                    path_tag="exception",
                    error_tag=(
                        f"http_client_raised:{type(exc).__name__}:{exc}"
                    ),
                )

            path_tag_final = path_tag_retry

            if outcome_tag == "success":
                state = HEALTH_OK
            elif outcome_tag == "success_after_retry":
                state = HEALTH_DEGRADED
            elif outcome_tag == "http_4xx":
                state = HEALTH_DEGRADED
            else:  # retries_exhausted
                state = HEALTH_FAILED

            return _CallResult(
                state=state,
                response=response,
                outcome_tag=outcome_tag,
                path_tag=path_tag_final,
                error_tag=error_tag,
            )
        finally:
            ctx.fd_broker.release_fd(fd)
    finally:
        ctx.nonce_registry.release(nonce_hex, path_tag=path_tag_final)


# ---------------------------------------------------------------------------
# Channel C protocols + dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PortalSubEvent:
    """Per-adapter internal event propagated up through AdapterOutcome.

    Adapter authors use this to report finer-grained degradations (e.g.
    "paginator exhausted mid-sweep") while still reporting a single
    aggregate ``state`` for the adapter as a whole.
    """

    code: str
    reason_tag: Optional[str]
    severity: str


@dataclass(frozen=True, kw_only=True)
class PortalAdapterOutcome:
    """Return shape for a Channel C portal adapter.

    ``state`` ∈ {HEALTH_OK, HEALTH_DEGRADED, HEALTH_FAILED}. ``events``
    may be empty; the dispatcher folds each event into
    :class:`ChannelCDegradationEvent` tagged with the portal's canonical
    slug.
    """

    candidates: tuple[Candidate, ...]
    state: str
    events: tuple[PortalSubEvent, ...] = ()


class PortalAdapter(Protocol):
    def __call__(self, ctx: AdapterContext) -> PortalAdapterOutcome: ...


@dataclass(frozen=True, kw_only=True)
class ChannelCDegradationEvent:
    portal_slug: str
    code: str
    reason_tag: Optional[str]
    severity: str


@dataclass(frozen=True, kw_only=True)
class ChannelCDiscoverResult:
    candidates: tuple[Candidate, ...]
    per_adapter_state: Mapping[str, str]
    channel_state: str
    degradation_events: tuple[ChannelCDegradationEvent, ...]


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


PORTAL_ADAPTERS: "OrderedDict[str, PortalAdapter]" = OrderedDict()


def _canonical_portal_slug(raw: str) -> str:
    """Section 1 primitive wrapper — delegates to org_slug.canonical_slug.

    Per the Round 5 spec card design decision 4, the blueprint's "NFC +
    lowercase + strip" narrative is realised by the existing org_slug
    primitive, which additionally collapses non-[a-z0-9] runs to ``-`` and
    rejects reserved / all-non-alphanum / over-long inputs. Reusing the
    same primitive across org slugs and portal slugs keeps canonicalisation
    discipline uniform.
    """
    return canonical_slug(raw)


def register_portal(portal_slug: str) -> Callable[[PortalAdapter], PortalAdapter]:
    """Decorator — registers a Channel C portal adapter under its canonical slug.

    ``portal_slug`` is the operator-facing raw slug. The decorator
    canonicalises it and stores the wrapped callable in
    :data:`PORTAL_ADAPTERS`. Duplicate canonical slugs raise
    :class:`ScoutConfigError` tagged ``F-SCOUT-C-03`` immediately — no
    deferred detection at run-time.

    Any :class:`InvalidSlug` / :class:`ReservedSlug` from the canonicaliser
    propagates as-is; operators see it at import and fix the slug.
    """

    cslug = _canonical_portal_slug(portal_slug)

    def _wrap(fn: PortalAdapter) -> PortalAdapter:
        if cslug in PORTAL_ADAPTERS:
            existing = PORTAL_ADAPTERS[cslug]
            existing_name = getattr(existing, "__qualname__", repr(existing))
            raise ScoutConfigError(
                f"{F_SCOUT_C_03}: duplicate portal adapter "
                f"canonical_slug={cslug!r} (raw={portal_slug!r}); "
                f"existing adapter={existing_name}"
            )
        PORTAL_ADAPTERS[cslug] = fn
        return fn

    return _wrap


def channel_c_reset_registry_for_tests() -> None:
    """Clear :data:`PORTAL_ADAPTERS` — test-only escape hatch.

    Not part of the production contract. Tests invoke this in fixtures to
    isolate registration between cases; the production pipeline relies on
    adapter modules being imported exactly once.
    """
    PORTAL_ADAPTERS.clear()


# ---------------------------------------------------------------------------
# Candidate-builder helper (A-v3-09 prefix assertion)
# ---------------------------------------------------------------------------


def _build_channel_c_candidate(
    *,
    cslug: str,
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
    """Construct a Channel C ``Candidate`` with the ``"portal:"`` prefix asserted.

    The adapter is free to derive ``candidate_id`` however it likes (per
    §4.3's own discipline), but the ``feed_or_adapter_id`` is composed
    here from ``FEED_PREFIX_PORTAL`` + ``cslug`` to close A-v3-09 at the
    build boundary — a misbehaving adapter cannot forge a non-namespaced
    ``feed_or_adapter_id``.
    """
    feed_or_adapter_id = f"{FEED_PREFIX_PORTAL}:{cslug}"
    assert feed_or_adapter_id.startswith(
        f"{FEED_PREFIX_PORTAL}:"
    ), f"Channel C feed_or_adapter_id must start with {FEED_PREFIX_PORTAL}:"
    return Candidate(
        candidate_id=candidate_id,
        channel=CHANNEL_C,
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
# Channel-C state aggregation — §4.3 line 517
# ---------------------------------------------------------------------------


def classify_channel_c(per_adapter_state: Mapping[str, str]) -> str:
    """≥ 50 % FAILED → FAILED; all OK → OK; any other partial → DEGRADED.

    Empty roster → FAILED (no DISCOVER work attempted; treated as the
    worst case so that a misconfigured org doesn't silently report OK).
    """
    values = list(per_adapter_state.values())
    if not values:
        return HEALTH_FAILED
    if all(v == HEALTH_OK for v in values):
        return HEALTH_OK
    failed_count = sum(1 for v in values if v == HEALTH_FAILED)
    if failed_count * 2 >= len(values):
        return HEALTH_FAILED
    return HEALTH_DEGRADED


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


class _RealClock:
    def __call__(self) -> _dt.datetime:
        return _dt.datetime.now(_dt.timezone.utc)

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)


_default_clock: ClockFn = _RealClock()


def discover_channel_c(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    http_client: HTTPClient,
    portal_roster: tuple[str, ...],
    clock: ClockFn = _default_clock,
) -> ChannelCDiscoverResult:
    """Dispatch registered Channel C portal adapters in ``portal_roster`` order.

    ``portal_roster`` carries raw or canonical portal slugs; each entry is
    canonicalised and looked up in :data:`PORTAL_ADAPTERS`. A missing
    adapter → FAILED with ``F-SCOUT-C-01``. An adapter raising an
    exception → FAILED with ``F-SCOUT-C-02`` (exception message carried in
    ``reason_tag``; the exception is otherwise swallowed so one bad
    adapter does not starve the channel).

    ``per_adapter_state`` keys use the canonical slug. Duplicate entries
    in ``portal_roster`` (same canonical slug twice) are deduplicated:
    each canonical slug is dispatched at most once, its first roster
    position.

    All candidates emitted by the adapter pass through
    :func:`_build_channel_c_candidate` at the adapter's own call site;
    the dispatcher trusts the adapter to have enforced the namespacing.
    An assertion-level re-check here would require round-tripping every
    candidate's ``feed_or_adapter_id`` — the contract is that the
    ``_build_channel_c_candidate`` helper is the only Candidate builder
    adapters use.
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
    events: list[ChannelCDegradationEvent] = []

    seen_cslugs: set[str] = set()

    for raw_slug in portal_roster:
        try:
            cslug = _canonical_portal_slug(raw_slug)
        except (InvalidSlug, ReservedSlug) as exc:
            # Malformed roster entry — treat as a missing adapter bound
            # to the raw slug for auditability. Keeps the dispatcher
            # robust against operator typos in portals.yaml.
            per_adapter_state[raw_slug] = HEALTH_FAILED
            events.append(
                ChannelCDegradationEvent(
                    portal_slug=raw_slug,
                    code=F_SCOUT_C_01,
                    reason_tag=(
                        f"roster_slug_invalid:{type(exc).__name__}:{exc}"
                    ),
                    severity=SEVERITY_HIGH,
                )
            )
            continue

        if cslug in seen_cslugs:
            continue
        seen_cslugs.add(cslug)

        adapter = PORTAL_ADAPTERS.get(cslug)
        if adapter is None:
            per_adapter_state[cslug] = HEALTH_FAILED
            events.append(
                ChannelCDegradationEvent(
                    portal_slug=cslug,
                    code=F_SCOUT_C_01,
                    reason_tag="no_adapter_registered",
                    severity=SEVERITY_HIGH,
                )
            )
            continue

        try:
            outcome = adapter(ctx)
        except ScoutConfigError:
            raise
        except Exception as exc:
            per_adapter_state[cslug] = HEALTH_FAILED
            events.append(
                ChannelCDegradationEvent(
                    portal_slug=cslug,
                    code=F_SCOUT_C_02,
                    reason_tag=f"adapter_raised:{type(exc).__name__}:{exc}",
                    severity=SEVERITY_HIGH,
                )
            )
            continue

        if outcome.state not in {HEALTH_OK, HEALTH_DEGRADED, HEALTH_FAILED}:
            per_adapter_state[cslug] = HEALTH_FAILED
            events.append(
                ChannelCDegradationEvent(
                    portal_slug=cslug,
                    code=F_SCOUT_C_02,
                    reason_tag=(
                        f"adapter_returned_unknown_state:{outcome.state!r}"
                    ),
                    severity=SEVERITY_HIGH,
                )
            )
            continue

        per_adapter_state[cslug] = outcome.state
        for sub in outcome.events:
            events.append(
                ChannelCDegradationEvent(
                    portal_slug=cslug,
                    code=sub.code,
                    reason_tag=sub.reason_tag,
                    severity=sub.severity,
                )
            )
        all_candidates.extend(outcome.candidates)

    channel_state = classify_channel_c(per_adapter_state)

    return ChannelCDiscoverResult(
        candidates=tuple(all_candidates),
        per_adapter_state=dict(per_adapter_state),
        channel_state=channel_state,
        degradation_events=tuple(events),
    )
