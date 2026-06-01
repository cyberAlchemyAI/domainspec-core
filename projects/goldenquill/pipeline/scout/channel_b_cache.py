"""Channel B DISCOVER adapter — curated cached datasets (§4.2).

Read-only, zero network. Produces ``list[Candidate]`` from ``vault_read``-
backed JSONL cache files plus a per-channel health state for M7 consumption.

Blueprint anchors:
- §4.2 Channel B full spec (implementation target)
- §2.1 Candidate schema (Round 1 ``_types.py``)
- §4.6 post-read intent equality check (defence-in-depth primitive)
- §6.2 F-SCOUT-B-01..05 failure codes
- §8 CACHE_WATERMARK_DEGRADED_DAYS = 14
- §9 cache intent = "cache-read"

The vault-read seam is a :class:`VaultReader` Protocol (E-017 pattern mirrored
from Round 2's ``VaultWriter``). Production binding adapts
:func:`pipeline.vault.vault_read`; tests inject a memory reader. The
``list_cache_paths`` callable is the enumeration seam — production binding
globs the four source families (``vault_shared/cached_opportunities/
{federal,state,foundation}/*.jsonl`` + ``orgs/{slug}/vault/subscribed_feeds/
*.jsonl``); tests return a fixed tuple.

S10a invariant read-time check is scoped to ARCH-02: Round 3 accepts rows
with or without org-identifier fields. The F-SCOUT-B-03 code is reserved for
when the architectural locus moves from Section 2 write-time to Section 3
read-time. Two test cases (``TestS10aRowKind``) document the current locus.
"""

from __future__ import annotations

import datetime as _dt
import json
import unicodedata
from dataclasses import dataclass
from typing import Callable, Final, Optional, Protocol

from pipeline.scout._constants import (
    CACHE_WATERMARK_DEGRADED_DAYS,
    CHANNEL_B,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
)
from pipeline.scout._types import Candidate

__all__ = [
    "ChannelBDiscoverResult",
    "ChannelBIdentityTupleMismatch",
    "DegradationEvent",
    "IdentityTupleLike",
    "INTENT_CACHE_READ",
    "PathListerFn",
    "SessionLike",
    "VaultReader",
    "discover_channel_b",
]


# ---------------------------------------------------------------------------
# §9 vault intent — distinct from Scout's INTENT_READ (see §4.2 line 491)
# ---------------------------------------------------------------------------

INTENT_CACHE_READ: Final[str] = "cache-read"

_MALFORMED_ROW_DEGRADE_RATIO: Final[float] = 0.10


# ---------------------------------------------------------------------------
# Injection Protocols (E-017 pattern mirrored from Round 2)
# ---------------------------------------------------------------------------


class IdentityTupleLike(Protocol):
    intent: str
    session_id: str
    slug: str


class SessionLike(Protocol):
    session_id: str
    slug: str


class VaultReader(Protocol):
    """§2 vault-read seam.

    Production binding adapts :func:`pipeline.vault.vault_read`. Tests
    inject a memory reader that returns pre-seeded bytes + IdentityTuple.
    """

    def read(
        self,
        *,
        path: str,
        intent: str,
        session_id: str,
        slug: str,
    ) -> tuple[bytes, IdentityTupleLike]: ...


PathListerFn = Callable[[str], tuple[str, ...]]
ClockFn = Callable[[], _dt.datetime]


# ---------------------------------------------------------------------------
# Public dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class DegradationEvent:
    """One-line per-file event record for M7 aggregation.

    ``severity`` ∈ {LOW, MEDIUM, HIGH}. Channel B maps events to severity:
    F-SCOUT-B-01 → LOW (single malformed row), F-SCOUT-B-02 → MEDIUM
    (header/watermark issue), F-SCOUT-B-04/-05 → HIGH (vault identity).
    """

    path: str
    code: str
    reason_tag: Optional[str]
    severity: str


@dataclass(frozen=True, kw_only=True)
class ChannelBDiscoverResult:
    candidates: tuple[Candidate, ...]
    channel_state: str
    per_file_events: tuple[DegradationEvent, ...]


class ChannelBIdentityTupleMismatch(RuntimeError):
    """Raised for vault IdentityTuple mismatch on a cache read.

    ``code`` is always ``F-SCOUT-B-04``; ``sub_tag`` is the NFC-drift tag
    when the caller wishes to distinguish F-SCOUT-B-05 in-band. Channel B
    never propagates this out of ``discover_channel_b`` — it is caught
    internally and recorded as a ``DegradationEvent``.
    """

    def __init__(
        self,
        message: str,
        *,
        code: str = "F-SCOUT-B-04",
        sub_tag: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.sub_tag = sub_tag


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


_REQUIRED_ROW_FIELDS: frozenset[str] = frozenset(
    {
        "candidate_id",
        "feed_or_adapter_id",
        "source_key",
        "title",
        "funder",
        "funder_kind",
        "url",
        "applicant_types",
        "fetch_timestamp_utc",
        "url_hash",
        "fit_score_cached",
    }
)


_STATE_PRIORITY: dict[str, int] = {
    HEALTH_OK: 0,
    HEALTH_DEGRADED: 1,
    HEALTH_FAILED: 2,
}


def _default_clock() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


def _escalate(current: str, incoming: str) -> str:
    if _STATE_PRIORITY[incoming] > _STATE_PRIORITY[current]:
        return incoming
    return current


def _assert_intent_matches(
    identity: IdentityTupleLike,
    session: SessionLike,
    expected_intent: str,
) -> Optional[tuple[str, str]]:
    """Mirrors §4.6 post-read intent check.

    Returns ``None`` on strict-equality match. Returns
    ``(code, reason_tag)`` on any mismatch. ``F-SCOUT-B-05`` is raised
    when the intent matches after NFC + strip normalisation but differs
    strictly (defence-in-depth against a silently buggy vault).
    """
    if identity.session_id != session.session_id:
        return (
            "F-SCOUT-B-04",
            f"session_id_mismatch:expected={session.session_id!r}"
            f" got={identity.session_id!r}",
        )
    if identity.slug != session.slug:
        return (
            "F-SCOUT-B-04",
            f"slug_mismatch:expected={session.slug!r} got={identity.slug!r}",
        )
    if identity.intent == expected_intent:
        return None
    normalized = unicodedata.normalize("NFC", identity.intent).strip()
    if normalized == expected_intent:
        return ("F-SCOUT-B-05", f"intent_nfc_drift:{identity.intent!r}")
    return ("F-SCOUT-B-04", f"intent_mismatch:{identity.intent!r}")


def _parse_iso_utc(value: object) -> _dt.datetime:
    if not isinstance(value, str):
        raise ValueError(f"watermark_utc not a string: {type(value).__name__}")
    raw = value
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    parsed = _dt.datetime.fromisoformat(raw)
    if parsed.tzinfo is None:
        raise ValueError("watermark_utc is naive (no timezone)")
    return parsed.astimezone(_dt.timezone.utc)


def _parse_row(line: str) -> Optional[dict]:
    stripped = line.strip()
    if not stripped:
        return None
    try:
        row = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    if not isinstance(row, dict):
        return None
    return row


def _row_to_candidate(row: dict) -> Optional[Candidate]:
    for field in _REQUIRED_ROW_FIELDS:
        if field not in row:
            return None
    try:
        applicant_types_raw = row["applicant_types"]
        if not isinstance(applicant_types_raw, (list, tuple)):
            return None
        return Candidate(
            candidate_id=row["candidate_id"],
            channel=CHANNEL_B,
            feed_or_adapter_id=row["feed_or_adapter_id"],
            source_key=row["source_key"],
            title=row["title"],
            funder=row["funder"],
            funder_kind=row["funder_kind"],
            url=row["url"],
            close_date_utc=row.get("close_date_utc"),
            award_ceiling=row.get("award_ceiling"),
            award_floor=row.get("award_floor"),
            applicant_types=tuple(applicant_types_raw),
            program_page_url=row.get("program_page_url"),
            fetch_timestamp_utc=row["fetch_timestamp_utc"],
            url_hash=row["url_hash"],
            content_hash=row.get("content_hash"),
            fit_score_cached=int(row["fit_score_cached"]),
            cache_provenance=row.get("cache_provenance"),
        )
    except (TypeError, ValueError):
        return None


def _parse_file(
    path: str,
    data: bytes,
    *,
    now: _dt.datetime,
) -> tuple[list[Candidate], list[DegradationEvent], str]:
    """Parse a cache file's bytes into candidates + events + file state."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return (
            [],
            [
                DegradationEvent(
                    path=path,
                    code="F-SCOUT-B-02",
                    reason_tag="utf8_decode_error",
                    severity="MEDIUM",
                )
            ],
            HEALTH_DEGRADED,
        )

    lines = text.splitlines()
    if not lines:
        return [], [], HEALTH_OK

    events: list[DegradationEvent] = []
    header_line = lines[0].strip()
    if not header_line:
        events.append(
            DegradationEvent(
                path=path,
                code="F-SCOUT-B-02",
                reason_tag="header_line_blank",
                severity="MEDIUM",
            )
        )
        return [], events, HEALTH_DEGRADED

    try:
        header = json.loads(header_line)
    except json.JSONDecodeError:
        events.append(
            DegradationEvent(
                path=path,
                code="F-SCOUT-B-02",
                reason_tag="header_unparseable",
                severity="MEDIUM",
            )
        )
        return [], events, HEALTH_DEGRADED

    if not isinstance(header, dict) or "watermark_utc" not in header:
        events.append(
            DegradationEvent(
                path=path,
                code="F-SCOUT-B-02",
                reason_tag="missing_watermark_utc",
                severity="MEDIUM",
            )
        )
        return [], events, HEALTH_DEGRADED

    file_state = HEALTH_OK
    try:
        watermark = _parse_iso_utc(header["watermark_utc"])
    except (ValueError, TypeError) as exc:
        events.append(
            DegradationEvent(
                path=path,
                code="F-SCOUT-B-02",
                reason_tag=f"watermark_unparseable:{exc}",
                severity="MEDIUM",
            )
        )
        return [], events, HEALTH_DEGRADED

    age_days = (now - watermark).total_seconds() / 86400.0
    if age_days > float(CACHE_WATERMARK_DEGRADED_DAYS):
        events.append(
            DegradationEvent(
                path=path,
                code="F-SCOUT-B-02",
                reason_tag="cache_stale_channel_b",
                severity="MEDIUM",
            )
        )
        file_state = _escalate(file_state, HEALTH_DEGRADED)

    data_rows = lines[1:]
    total_rows = len(data_rows)
    malformed_count = 0
    candidates: list[Candidate] = []

    for idx, raw_line in enumerate(data_rows, start=1):
        row = _parse_row(raw_line)
        if row is None:
            malformed_count += 1
            events.append(
                DegradationEvent(
                    path=path,
                    code="F-SCOUT-B-01",
                    reason_tag=f"malformed_json_row:line={idx + 1}",
                    severity="LOW",
                )
            )
            continue
        cand = _row_to_candidate(row)
        if cand is None:
            malformed_count += 1
            events.append(
                DegradationEvent(
                    path=path,
                    code="F-SCOUT-B-01",
                    reason_tag=f"invalid_row_fields:line={idx + 1}",
                    severity="LOW",
                )
            )
            continue
        candidates.append(cand)

    if total_rows > 0:
        ratio = malformed_count / total_rows
        if ratio >= _MALFORMED_ROW_DEGRADE_RATIO:
            events.append(
                DegradationEvent(
                    path=path,
                    code="F-SCOUT-B-05",
                    reason_tag=(
                        f"malformed_ratio:{malformed_count}/{total_rows}"
                    ),
                    severity="MEDIUM",
                )
            )
            file_state = _escalate(file_state, HEALTH_DEGRADED)

    return candidates, events, file_state


# ---------------------------------------------------------------------------
# Public entry — discover_channel_b
# ---------------------------------------------------------------------------


def discover_channel_b(
    *,
    session: SessionLike,
    vault_reader: VaultReader,
    list_cache_paths: PathListerFn,
    clock: ClockFn = _default_clock,
) -> ChannelBDiscoverResult:
    """Enumerate Channel B cache files, read each, and emit DISCOVER rows.

    Never raises on a malformed or stale file. IdentityTuple mismatches are
    caught and recorded as ``DegradationEvent(code="F-SCOUT-B-04")`` (or
    ``-05`` on NFC drift); the file is aborted (no rows consumed) and
    ``channel_state`` flips to ``FAILED`` for the run. Per-row malformed
    JSON is recorded as ``F-SCOUT-B-01`` and row-skipped; a file whose
    malformed rate ≥ 10 % additionally emits ``F-SCOUT-B-05`` and degrades
    that file's state. ``F-SCOUT-B-03`` (S10a row-kind) is reserved —
    ARCH-02 currently locates S10a at Section 2 write-time.
    """
    paths = tuple(sorted(list_cache_paths(session.slug)))
    now = clock()

    all_candidates: list[Candidate] = []
    all_events: list[DegradationEvent] = []
    channel_state: str = HEALTH_OK

    for path in paths:
        data, identity = vault_reader.read(
            path=path,
            intent=INTENT_CACHE_READ,
            session_id=session.session_id,
            slug=session.slug,
        )

        drift = _assert_intent_matches(identity, session, INTENT_CACHE_READ)
        if drift is not None:
            code, reason = drift
            all_events.append(
                DegradationEvent(
                    path=path,
                    code=code,
                    reason_tag=reason,
                    severity="HIGH",
                )
            )
            channel_state = _escalate(channel_state, HEALTH_FAILED)
            continue

        file_candidates, file_events, file_state = _parse_file(
            path, data, now=now
        )
        all_events.extend(file_events)
        all_candidates.extend(file_candidates)
        channel_state = _escalate(channel_state, file_state)

    return ChannelBDiscoverResult(
        candidates=tuple(all_candidates),
        channel_state=channel_state,
        per_file_events=tuple(all_events),
    )
