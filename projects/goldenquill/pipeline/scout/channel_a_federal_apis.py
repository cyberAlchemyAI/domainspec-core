"""Channel A Federal APIs — DISCOVER adapter (§4.1).

First Scout round with network I/O. Three parallel endpoints (grants.gov,
sam.gov, usaspending.gov); each independently OK / DEGRADED / FAILED.
``backbone_failed = True`` iff all three FAILED.

Only ``grants.gov`` search2 produces :class:`Candidate` rows. ``sam.gov``
writes a cached entity-registration snapshot through the injected
:class:`VaultWriter`; ``usaspending.gov`` writes a historical-awards
snapshot. Both snapshot paths enforce the §4.2 S10a invariant (no
org-identifier keys in the cached body).

Blueprint anchors:
- §4.1 Channel A full spec (lines 412-471) — implementation target
- §2.1 ``Candidate`` schema (Round 1 ``_types.py``)
- §6.1 F-SCOUT-A-01..05 failure codes
- §7.1 test surface
- §8 ``CHANNEL_A_CONNECT_TIMEOUT_S = 10``, ``CHANNEL_A_READ_TIMEOUT_S = 30``,
  ``CHANNEL_A_RETRY_COUNT = 3``
- §9 intent strings for cached snapshot writes

Nonce + FD lifecycle — A-01 / RT-v1-CRIT-01 closure: one try/finally ladder
per logical request (one per page for grants.gov sweep). Nonce reserved
BEFORE FD obtained; release order at every exit path is FD first, then
nonce. Every exit path is tagged with one of
``{"success", "success_after_retry", "timeout", "connection_reset",
"http_error", "retries_exhausted", "exception"}``.

Retry ladder — one initial attempt plus ``CHANNEL_A_RETRY_COUNT`` retries
(4 attempts total). Sleeps ``(1.0, 2.0, 4.0)`` seconds injected via the
``ClockFn`` protocol so tests can skip wall-clock time. 5xx responses,
``TimeoutError``, and ``ConnectionError`` are retriable; 4xx responses are
not retried.

S10a invariant — the sam.gov entity-registration snapshot body must NOT
carry org-identifier keys at write time (``slug``, ``org_id``, ``ein``,
``uei``, ``duns``, ``tax_id``, and common variants). Violations are
rejected with ``F-SCOUT-A-03`` before ``vault_writer.write`` is called.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import socket
import time
from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional, Protocol

from pipeline.scout._constants import (
    CHANNEL_A,
    CHANNEL_A_CONNECT_TIMEOUT_S,
    CHANNEL_A_READ_TIMEOUT_S,
    CHANNEL_A_RETRY_COUNT,
    FEED_PREFIX_API,
    FUNDER_FEDERAL,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
)
from pipeline.scout._types import Candidate

__all__ = [
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
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ENDPOINT_GRANTS_GOV: Final[str] = "grants.gov"
ENDPOINT_SAM_GOV: Final[str] = "sam.gov"
ENDPOINT_USASPENDING_GOV: Final[str] = "usaspending.gov"

INTENT_ENTITY_REGISTRATION_CACHE_WRITE: Final[str] = (
    "cached-entity-registration-write"
)
INTENT_AWARDS_HISTORY_CACHE_WRITE: Final[str] = "cached-awards-history-write"

_RETRY_SLEEP_SCHEDULE: Final[tuple[float, ...]] = (1.0, 2.0, 4.0)

_GRANTS_GOV_PAGE_SIZE: Final[int] = 100
_GRANTS_GOV_PAGE_HARD_CAP: Final[int] = 100
_GRANTS_GOV_MAX_ERROR_STREAK: Final[int] = 3

_GRANTS_GOV_HOST: Final[str] = "api.grants.gov"
_SAM_GOV_HOST: Final[str] = "api.sam.gov"
_USASPENDING_GOV_HOST: Final[str] = "api.usaspending.gov"

_GRANTS_GOV_URL: Final[str] = (
    "https://api.grants.gov/v1/api/search2"
)
_SAM_GOV_URL: Final[str] = (
    "https://api.sam.gov/entity-information/v4/entities"
)
_USASPENDING_GOV_URL: Final[str] = (
    "https://api.usaspending.gov/api/v2/search/spending_by_award/"
)

_USER_AGENT: Final[str] = "Golden-Quill-Scout/0.1"
_ACCEPT_JSON: Final[str] = "application/json"

_SAM_GOV_SNAPSHOT_PREFIX: Final[str] = "vault_shared/cached_entity_registrations"
_USASPENDING_SNAPSHOT_PREFIX: Final[str] = "vault_shared/cached_awards_history"

_FORBIDDEN_ORG_IDENTIFIER_KEYS: Final[frozenset[str]] = frozenset(
    {
        "slug",
        "org_slug",
        "organization_slug",
        "org_id",
        "organization_id",
        "ein",
        "uei",
        "tax_id",
        "taxid",
        "duns",
        "duns_number",
    }
)

_STATE_PRIORITY: Final[dict[str, int]] = {
    HEALTH_OK: 0,
    HEALTH_DEGRADED: 1,
    HEALTH_FAILED: 2,
}


# ---------------------------------------------------------------------------
# Protocols (E-017 pattern)
# ---------------------------------------------------------------------------


class HTTPResponse(Protocol):
    status: int
    headers: Mapping[str, str]
    body_bytes: bytes


class HTTPClient(Protocol):
    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        body: Optional[bytes],
        connect_timeout_s: float,
        read_timeout_s: float,
    ) -> HTTPResponse: ...


class NonceRegistry(Protocol):
    def reserve(self, nonce_hex: str) -> None: ...
    def release(self, nonce_hex: str, *, path_tag: str) -> None: ...


class FDBroker(Protocol):
    def request_fd(self, *, kind: str, host: str) -> int: ...
    def release_fd(self, fd: int) -> None: ...


class VaultWriter(Protocol):
    def write(
        self,
        *,
        path: str,
        bytes_: bytes,
        intent: str,
        session_id: str,
        slug: str,
    ) -> None: ...


class SessionLike(Protocol):
    session_id: str
    slug: str


class ClockFn(Protocol):
    def __call__(self) -> _dt.datetime: ...
    def sleep(self, seconds: float) -> None: ...


class _RealClock:
    """Production binding — wraps ``datetime.now`` and ``time.sleep``."""

    def __call__(self) -> _dt.datetime:
        return _dt.datetime.now(_dt.timezone.utc)

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)


_default_clock: ClockFn = _RealClock()


# ---------------------------------------------------------------------------
# Public dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ChannelADegradationEvent:
    """One-line per-call degradation record for §4.10 aggregation.

    Named ``ChannelADegradationEvent`` rather than ``DegradationEvent`` to
    avoid collision with Round 3's ``DegradationEvent`` (different shape:
    Round 3 carries ``path``, Round 4 carries ``endpoint``).
    """

    endpoint: str
    code: str
    reason_tag: Optional[str]
    severity: str


@dataclass(frozen=True, kw_only=True)
class ChannelADiscoverResult:
    candidates: tuple[Candidate, ...]
    per_endpoint_state: Mapping[str, str]
    channel_state: str
    backbone_failed: bool
    degradation_events: tuple[ChannelADegradationEvent, ...]


# ---------------------------------------------------------------------------
# Internal result carrier for a single HTTP request (possibly with retries)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class _CallResult:
    """Outcome of one logical HTTP request (one page or one endpoint call).

    ``state`` is the per-call HEALTH_* value. ``response`` is the HTTPResponse
    on success (2xx) or 4xx (server responded); None on retries_exhausted or
    broker / nonce errors.
    """

    state: str
    response: Optional[HTTPResponse]
    outcome_tag: str  # "success" / "success_after_retry" / "http_4xx" / "retries_exhausted" / "fd_error" / "nonce_error"
    path_tag: str
    error_tag: Optional[str]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fresh_nonce() -> str:
    """32-byte hex nonce for a single request. One reservation per call."""
    return os.urandom(32).hex()


def _sha3_512_hex(data: bytes) -> str:
    return hashlib.sha3_512(data).hexdigest()


def _utc_now_iso(clock: ClockFn) -> str:
    return clock().isoformat().replace("+00:00", "Z")


def _escalate(current: str, incoming: str) -> str:
    if _STATE_PRIORITY[incoming] > _STATE_PRIORITY[current]:
        return incoming
    return current


def _contains_org_identifier(body: Any) -> tuple[bool, str]:
    """Recursively walk a JSON-decoded body for forbidden org-identifier keys.

    Returns ``(True, offending_key_path)`` on the first hit, else
    ``(False, "")``. Path strings are dotted for dicts, bracketed for lists.
    """
    stack: list[tuple[Any, str]] = [(body, "")]
    while stack:
        obj, path = stack.pop()
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(key, str) and key in _FORBIDDEN_ORG_IDENTIFIER_KEYS:
                    return True, f"{path}.{key}" if path else key
                stack.append((value, f"{path}.{key}" if path else key))
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                stack.append((item, f"{path}[{idx}]"))
    return False, ""


def _default_headers() -> dict[str, str]:
    return {
        "User-Agent": _USER_AGENT,
        "Accept": _ACCEPT_JSON,
        "Content-Type": _ACCEPT_JSON,
    }


# ---------------------------------------------------------------------------
# Retry ladder — inside a single reserved nonce + held FD
# ---------------------------------------------------------------------------


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

    Returns ``(response, outcome_tag, path_tag, error_tag)``. ``outcome_tag``
    is one of ``success`` / ``success_after_retry`` / ``http_4xx`` /
    ``retries_exhausted``. ``path_tag`` is the nonce-release tag.
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
        # 5xx and anything else — retry
        path_tag = "http_error"
        error_tag = f"http_{status}:attempt={attempt}"

    return (None, "retries_exhausted", path_tag, error_tag)


def _invoke_one_request(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    http_client: HTTPClient,
    clock: ClockFn,
    host: str,
    method: str,
    url: str,
    headers: Mapping[str, str],
    body: Optional[bytes],
) -> _CallResult:
    """One logical request with nonce + FD lifecycle + retry ladder.

    Nonce is reserved before FD; released after FD on every exit path. If
    ``nonce_registry.reserve`` raises, no FD is requested and the call
    returns early with ``F-SCOUT-A-02``.
    """
    nonce_hex = _fresh_nonce()
    path_tag_final = "exception"

    try:
        nonce_registry.reserve(nonce_hex)
    except Exception as exc:
        return _CallResult(
            state=HEALTH_FAILED,
            response=None,
            outcome_tag="nonce_error",
            path_tag="exception",
            error_tag=(
                f"nonce_reserve_failed:{type(exc).__name__}:{exc}"
            ),
        )

    try:
        try:
            fd = fd_broker.request_fd(kind="https", host=host)
        except Exception as exc:
            path_tag_final = "exception"
            return _CallResult(
                state=HEALTH_FAILED,
                response=None,
                outcome_tag="fd_error",
                path_tag="exception",
                error_tag=(
                    f"fd_request_failed:{type(exc).__name__}:{exc}"
                ),
            )

        try:
            try:
                (
                    response,
                    outcome_tag,
                    path_tag_retry,
                    error_tag,
                ) = _do_request_with_retries(
                    http_client=http_client,
                    clock=clock,
                    method=method,
                    url=url,
                    headers=headers,
                    body=body,
                )
            except Exception as exc:
                path_tag_final = "exception"
                return _CallResult(
                    state=HEALTH_FAILED,
                    response=None,
                    outcome_tag="exception",
                    path_tag="exception",
                    error_tag=f"http_client_raised:{type(exc).__name__}:{exc}",
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
            fd_broker.release_fd(fd)
    finally:
        nonce_registry.release(nonce_hex, path_tag=path_tag_final)


# ---------------------------------------------------------------------------
# Endpoint state aggregation — persistent non-success across >=3 calls
# escalates DEGRADED to FAILED (A §6.1 F-SCOUT-A-06 closure test).
# ---------------------------------------------------------------------------


def _aggregate_call_states(call_states: tuple[str, ...]) -> str:
    if not call_states:
        return HEALTH_FAILED
    if any(s == HEALTH_FAILED for s in call_states):
        return HEALTH_FAILED
    if all(s == HEALTH_OK for s in call_states):
        return HEALTH_OK
    if (
        len(call_states) >= 3
        and all(s == HEALTH_DEGRADED for s in call_states)
        and not any(s == HEALTH_OK for s in call_states)
    ):
        return HEALTH_FAILED
    return HEALTH_DEGRADED


# ---------------------------------------------------------------------------
# Channel-A state aggregation — §4.1 line 462 verbatim.
# ---------------------------------------------------------------------------


def classify_channel_a(per_endpoint: Mapping[str, str]) -> str:
    """All-OK → OK; all-FAILED → FAILED; otherwise DEGRADED.

    Mirrors the blueprint §4.1 snippet exactly. Callers may pass a ``dict``
    or any ``Mapping`` shape.
    """
    values = list(per_endpoint.values())
    if not values:
        return HEALTH_FAILED
    if all(v == HEALTH_OK for v in values):
        return HEALTH_OK
    if all(v == HEALTH_FAILED for v in values):
        return HEALTH_FAILED
    return HEALTH_DEGRADED


# ---------------------------------------------------------------------------
# grants.gov — page sweep producing Candidate rows
# ---------------------------------------------------------------------------


def _parse_grants_gov_page(
    body_bytes: bytes,
    content_hash: str,
    clock: ClockFn,
) -> tuple[tuple[Candidate, ...], Optional[str]]:
    """Parse a grants.gov search2 page body into Candidate rows.

    Returns ``(candidates, error_reason)``. ``error_reason`` is non-None
    when the page body is not parseable JSON or the shape is wrong —
    caller flags F-SCOUT-A-03 but keeps endpoint in the existing state
    (individual row / page parse failure does not escalate endpoint
    beyond the retry ladder's own escalation).
    """
    try:
        decoded = json.loads(body_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return (), f"body_parse_failed:{type(exc).__name__}:{exc}"

    if not isinstance(decoded, dict):
        return (), "body_not_object"

    hits = decoded.get("oppHits")
    if hits is None:
        hits = decoded.get("opportunities", [])
    if not isinstance(hits, list):
        return (), "oppHits_not_list"

    fetch_ts = _utc_now_iso(clock)
    candidates: list[Candidate] = []

    for row in hits:
        if not isinstance(row, dict):
            continue
        cand = _row_to_candidate(
            row=row,
            content_hash=content_hash,
            fetch_ts=fetch_ts,
        )
        if cand is not None:
            candidates.append(cand)

    return tuple(candidates), None


def _row_to_candidate(
    *,
    row: dict[str, Any],
    content_hash: str,
    fetch_ts: str,
) -> Optional[Candidate]:
    """Build one Candidate from a grants.gov search2 row.

    Returns None on missing required fields. ``source_key`` = opportunity
    id. ``feed_or_adapter_id`` is namespaced ``"api:grants.gov"`` per
    A-v3-09.
    """
    opp_id = row.get("id") or row.get("oppId") or row.get("opportunityId")
    if not isinstance(opp_id, str) or not opp_id:
        return None

    title = row.get("title") or row.get("oppTitle") or ""
    if not isinstance(title, str):
        return None

    funder = row.get("agency") or row.get("agencyName") or row.get(
        "agencyCode"
    ) or ""
    if not isinstance(funder, str):
        funder = ""

    url = row.get("url") or (
        f"https://www.grants.gov/search-results-detail/{opp_id}"
    )
    if not isinstance(url, str):
        url = ""

    url_hash = _sha3_512_hex(url.encode("utf-8"))[:32]
    candidate_id = _sha3_512_hex(
        f"{CHANNEL_A}|api:{ENDPOINT_GRANTS_GOV}|{opp_id}".encode("utf-8")
    )[:24]

    applicant_types_raw = row.get("applicantEligibility") or row.get(
        "applicantTypes"
    ) or []
    if not isinstance(applicant_types_raw, (list, tuple)):
        applicant_types_raw = []
    applicant_types = tuple(
        a for a in applicant_types_raw if isinstance(a, str)
    )

    award_ceiling = row.get("awardCeiling")
    award_floor = row.get("awardFloor")
    if not isinstance(award_ceiling, int):
        award_ceiling = None
    if not isinstance(award_floor, int):
        award_floor = None

    close_date = row.get("closeDate") or row.get("closeDateUtc")
    if not isinstance(close_date, str):
        close_date = None

    program_page = row.get("programPageUrl") or row.get("programUrl")
    if not isinstance(program_page, str):
        program_page = None

    feed_or_adapter_id = f"{FEED_PREFIX_API}:{ENDPOINT_GRANTS_GOV}"

    return Candidate(
        candidate_id=candidate_id,
        channel=CHANNEL_A,
        feed_or_adapter_id=feed_or_adapter_id,
        source_key=opp_id,
        title=title,
        funder=funder,
        funder_kind=FUNDER_FEDERAL,
        url=url,
        close_date_utc=close_date,
        award_ceiling=award_ceiling,
        award_floor=award_floor,
        applicant_types=applicant_types,
        program_page_url=program_page,
        fetch_timestamp_utc=fetch_ts,
        url_hash=url_hash,
        content_hash=content_hash,
        fit_score_cached=0,
        cache_provenance=None,
    )


def _grants_gov_request_body(offset: int) -> bytes:
    return json.dumps(
        {
            "keyword": "",
            "rows": _GRANTS_GOV_PAGE_SIZE,
            "startRecordNum": offset,
        },
        separators=(",", ":"),
    ).encode("utf-8")


def _discover_grants_gov(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    http_client: HTTPClient,
    clock: ClockFn,
) -> tuple[
    tuple[Candidate, ...],
    str,
    tuple[ChannelADegradationEvent, ...],
]:
    """Sweep grants.gov search2 pages. Returns per-endpoint aggregation."""
    all_candidates: list[Candidate] = []
    events: list[ChannelADegradationEvent] = []
    call_states: list[str] = []
    headers = _default_headers()

    offset = 0
    pages_fetched = 0
    consecutive_error_streak = 0

    while pages_fetched < _GRANTS_GOV_PAGE_HARD_CAP:
        body = _grants_gov_request_body(offset)
        call = _invoke_one_request(
            session=session,
            fd_broker=fd_broker,
            nonce_registry=nonce_registry,
            http_client=http_client,
            clock=clock,
            host=_GRANTS_GOV_HOST,
            method="POST",
            url=_GRANTS_GOV_URL,
            headers=headers,
            body=body,
        )
        call_states.append(call.state)
        pages_fetched += 1

        if call.outcome_tag in ("fd_error", "nonce_error", "exception"):
            events.append(
                ChannelADegradationEvent(
                    endpoint=ENDPOINT_GRANTS_GOV,
                    code=(
                        "F-SCOUT-A-01"
                        if call.outcome_tag == "fd_error"
                        else "F-SCOUT-A-02"
                    ),
                    reason_tag=call.error_tag,
                    severity="HIGH",
                )
            )
            break

        if call.outcome_tag == "retries_exhausted":
            events.append(
                ChannelADegradationEvent(
                    endpoint=ENDPOINT_GRANTS_GOV,
                    code="F-SCOUT-A-05",
                    reason_tag=call.error_tag,
                    severity="HIGH",
                )
            )
            break

        if call.outcome_tag == "http_4xx":
            events.append(
                ChannelADegradationEvent(
                    endpoint=ENDPOINT_GRANTS_GOV,
                    code="F-SCOUT-A-06",
                    reason_tag=call.error_tag,
                    severity="MEDIUM",
                )
            )
            consecutive_error_streak += 1
            if consecutive_error_streak >= _GRANTS_GOV_MAX_ERROR_STREAK:
                break
            offset += _GRANTS_GOV_PAGE_SIZE
            continue

        # Success or success-after-retry: parse body
        if call.outcome_tag == "success_after_retry":
            events.append(
                ChannelADegradationEvent(
                    endpoint=ENDPOINT_GRANTS_GOV,
                    code="F-SCOUT-A-05",
                    reason_tag=(
                        call.error_tag
                        or "retry_used_before_success"
                    ),
                    severity="LOW",
                )
            )

        consecutive_error_streak = 0

        response = call.response
        assert response is not None  # guaranteed by outcome_tag filter
        body_bytes = response.body_bytes
        content_hash = _sha3_512_hex(body_bytes)
        page_candidates, parse_err = _parse_grants_gov_page(
            body_bytes, content_hash, clock
        )

        if parse_err is not None:
            events.append(
                ChannelADegradationEvent(
                    endpoint=ENDPOINT_GRANTS_GOV,
                    code="F-SCOUT-A-03",
                    reason_tag=parse_err,
                    severity="MEDIUM",
                )
            )
            # Parse failure escalates this call to DEGRADED even if HTTP was OK.
            call_states[-1] = _escalate(call_states[-1], HEALTH_DEGRADED)
            break

        all_candidates.extend(page_candidates)

        if len(page_candidates) < _GRANTS_GOV_PAGE_SIZE:
            break

        offset += len(page_candidates)

    endpoint_state = _aggregate_call_states(tuple(call_states))
    return tuple(all_candidates), endpoint_state, tuple(events)


# ---------------------------------------------------------------------------
# sam.gov — single fetch + cached snapshot write
# ---------------------------------------------------------------------------


def _sam_gov_snapshot_path(session: SessionLike, clock: ClockFn) -> str:
    ts = clock().strftime("%Y%m%dT%H%M%SZ")
    key = _sha3_512_hex(
        f"{session.session_id}|{ts}|sam.gov".encode("utf-8")
    )[:16]
    return f"{_SAM_GOV_SNAPSHOT_PREFIX}/{ts}_{key}.json"


def _discover_sam_gov(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    vault_writer: VaultWriter,
    http_client: HTTPClient,
    clock: ClockFn,
) -> tuple[str, tuple[ChannelADegradationEvent, ...]]:
    """Fetch sam.gov entity-registration snapshot; write if S10a passes."""
    events: list[ChannelADegradationEvent] = []
    headers = _default_headers()
    call = _invoke_one_request(
        session=session,
        fd_broker=fd_broker,
        nonce_registry=nonce_registry,
        http_client=http_client,
        clock=clock,
        host=_SAM_GOV_HOST,
        method="GET",
        url=_SAM_GOV_URL,
        headers=headers,
        body=None,
    )

    if call.outcome_tag in ("fd_error", "nonce_error", "exception"):
        events.append(
            ChannelADegradationEvent(
                endpoint=ENDPOINT_SAM_GOV,
                code=(
                    "F-SCOUT-A-01"
                    if call.outcome_tag == "fd_error"
                    else "F-SCOUT-A-02"
                ),
                reason_tag=call.error_tag,
                severity="HIGH",
            )
        )
        return HEALTH_FAILED, tuple(events)

    if call.outcome_tag == "retries_exhausted":
        events.append(
            ChannelADegradationEvent(
                endpoint=ENDPOINT_SAM_GOV,
                code="F-SCOUT-A-05",
                reason_tag=call.error_tag,
                severity="HIGH",
            )
        )
        return HEALTH_FAILED, tuple(events)

    if call.outcome_tag == "http_4xx":
        events.append(
            ChannelADegradationEvent(
                endpoint=ENDPOINT_SAM_GOV,
                code="F-SCOUT-A-06",
                reason_tag=call.error_tag,
                severity="MEDIUM",
            )
        )
        return HEALTH_DEGRADED, tuple(events)

    if call.outcome_tag == "success_after_retry":
        events.append(
            ChannelADegradationEvent(
                endpoint=ENDPOINT_SAM_GOV,
                code="F-SCOUT-A-05",
                reason_tag=call.error_tag or "retry_used_before_success",
                severity="LOW",
            )
        )

    response = call.response
    assert response is not None

    # Parse body to run S10a check.
    try:
        decoded = json.loads(response.body_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        events.append(
            ChannelADegradationEvent(
                endpoint=ENDPOINT_SAM_GOV,
                code="F-SCOUT-A-03",
                reason_tag=(
                    f"body_parse_failed:{type(exc).__name__}:{exc}"
                ),
                severity="MEDIUM",
            )
        )
        # Parse failure → degrade (snapshot not written).
        final_state = _escalate(call.state, HEALTH_DEGRADED)
        return final_state, tuple(events)

    has_id, offender = _contains_org_identifier(decoded)
    if has_id:
        events.append(
            ChannelADegradationEvent(
                endpoint=ENDPOINT_SAM_GOV,
                code="F-SCOUT-A-03",
                reason_tag=f"s10a_violation:{offender}",
                severity="HIGH",
            )
        )
        final_state = _escalate(call.state, HEALTH_DEGRADED)
        return final_state, tuple(events)

    # Snapshot body passes S10a. Write via vault.
    path = _sam_gov_snapshot_path(session, clock)
    vault_writer.write(
        path=path,
        bytes_=response.body_bytes,
        intent=INTENT_ENTITY_REGISTRATION_CACHE_WRITE,
        session_id=session.session_id,
        slug=session.slug,
    )

    return call.state, tuple(events)


# ---------------------------------------------------------------------------
# usaspending.gov — single fetch + cached snapshot write
# ---------------------------------------------------------------------------


def _usaspending_snapshot_path(session: SessionLike, clock: ClockFn) -> str:
    ts = clock().strftime("%Y%m%dT%H%M%SZ")
    key = _sha3_512_hex(
        f"{session.session_id}|{ts}|usaspending.gov".encode("utf-8")
    )[:16]
    return f"{_USASPENDING_SNAPSHOT_PREFIX}/{ts}_{key}.json"


def _usaspending_request_body() -> bytes:
    return json.dumps(
        {
            "filters": {},
            "fields": ["Award ID"],
            "limit": 100,
        },
        separators=(",", ":"),
    ).encode("utf-8")


def _discover_usaspending_gov(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    vault_writer: VaultWriter,
    http_client: HTTPClient,
    clock: ClockFn,
) -> tuple[str, tuple[ChannelADegradationEvent, ...]]:
    events: list[ChannelADegradationEvent] = []
    headers = _default_headers()
    call = _invoke_one_request(
        session=session,
        fd_broker=fd_broker,
        nonce_registry=nonce_registry,
        http_client=http_client,
        clock=clock,
        host=_USASPENDING_GOV_HOST,
        method="POST",
        url=_USASPENDING_GOV_URL,
        headers=headers,
        body=_usaspending_request_body(),
    )

    if call.outcome_tag in ("fd_error", "nonce_error", "exception"):
        events.append(
            ChannelADegradationEvent(
                endpoint=ENDPOINT_USASPENDING_GOV,
                code=(
                    "F-SCOUT-A-01"
                    if call.outcome_tag == "fd_error"
                    else "F-SCOUT-A-02"
                ),
                reason_tag=call.error_tag,
                severity="HIGH",
            )
        )
        return HEALTH_FAILED, tuple(events)

    if call.outcome_tag == "retries_exhausted":
        events.append(
            ChannelADegradationEvent(
                endpoint=ENDPOINT_USASPENDING_GOV,
                code="F-SCOUT-A-05",
                reason_tag=call.error_tag,
                severity="HIGH",
            )
        )
        return HEALTH_FAILED, tuple(events)

    if call.outcome_tag == "http_4xx":
        events.append(
            ChannelADegradationEvent(
                endpoint=ENDPOINT_USASPENDING_GOV,
                code="F-SCOUT-A-06",
                reason_tag=call.error_tag,
                severity="MEDIUM",
            )
        )
        return HEALTH_DEGRADED, tuple(events)

    if call.outcome_tag == "success_after_retry":
        events.append(
            ChannelADegradationEvent(
                endpoint=ENDPOINT_USASPENDING_GOV,
                code="F-SCOUT-A-05",
                reason_tag=call.error_tag or "retry_used_before_success",
                severity="LOW",
            )
        )

    response = call.response
    assert response is not None

    # usaspending.gov snapshot is written as-is (S10a not applicable —
    # awards data is historical public records keyed by award id, not org
    # identifier in Scout's sense).
    path = _usaspending_snapshot_path(session, clock)
    vault_writer.write(
        path=path,
        bytes_=response.body_bytes,
        intent=INTENT_AWARDS_HISTORY_CACHE_WRITE,
        session_id=session.session_id,
        slug=session.slug,
    )

    return call.state, tuple(events)


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------


def discover_channel_a(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    vault_writer: VaultWriter,
    http_client: HTTPClient,
    clock: ClockFn = _default_clock,
) -> ChannelADiscoverResult:
    """Channel A DISCOVER adapter — §4.1 line 412.

    Executes three endpoints serially (Pipeline §5 provides the cross-
    channel parallelism). Each endpoint reports OK / DEGRADED / FAILED
    independently. ``backbone_failed = True`` iff all three FAILED.

    Only grants.gov produces :class:`Candidate` rows. sam.gov and
    usaspending.gov write cached snapshots through the injected
    ``VaultWriter``; their contribution to the return is the
    per-endpoint state only.
    """
    all_candidates: list[Candidate] = []
    all_events: list[ChannelADegradationEvent] = []
    per_endpoint: dict[str, str] = {}

    gg_candidates, gg_state, gg_events = _discover_grants_gov(
        session=session,
        fd_broker=fd_broker,
        nonce_registry=nonce_registry,
        http_client=http_client,
        clock=clock,
    )
    all_candidates.extend(gg_candidates)
    all_events.extend(gg_events)
    per_endpoint[ENDPOINT_GRANTS_GOV] = gg_state

    sam_state, sam_events = _discover_sam_gov(
        session=session,
        fd_broker=fd_broker,
        nonce_registry=nonce_registry,
        vault_writer=vault_writer,
        http_client=http_client,
        clock=clock,
    )
    all_events.extend(sam_events)
    per_endpoint[ENDPOINT_SAM_GOV] = sam_state

    usa_state, usa_events = _discover_usaspending_gov(
        session=session,
        fd_broker=fd_broker,
        nonce_registry=nonce_registry,
        vault_writer=vault_writer,
        http_client=http_client,
        clock=clock,
    )
    all_events.extend(usa_events)
    per_endpoint[ENDPOINT_USASPENDING_GOV] = usa_state

    channel_state = classify_channel_a(per_endpoint)
    backbone_failed = channel_state == HEALTH_FAILED

    return ChannelADiscoverResult(
        candidates=tuple(all_candidates),
        per_endpoint_state=dict(per_endpoint),
        channel_state=channel_state,
        backbone_failed=backbone_failed,
        degradation_events=tuple(all_events),
    )
