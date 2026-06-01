"""§4.7 VERIFY stage — live-synopsis elevation gate.

Scout Round 9. Implements architecture D.1 STAGE 2 verbatim per the LOCKED
blueprint §4.7 / §6.7 / §8. Consumes Round 8's :class:`ScoutDiscoverResult`
(candidates + ``run_tiebreak_seed`` + per-channel states + signed health
tuple). Emits a per-candidate :class:`VerificationVerdict` plus an
aggregate :class:`ScoutVerifyResult` that Section 5 (Pipeline) hands to
Round 10 (REVIEW) and Round 11 (capstone-of-capstones) for enqueue + LLM
rationale.

Blueprint anchors:

- §4.7 VERIFY stage — primary implementation target. Four-verdict taxonomy
  ``VERIFIED_FIT`` / ``VERIFIED_NOT_FIT`` / ``UNVERIFIED`` /
  ``VERIFICATION_FAILED``; L-001 precedent (cache fit score never
  elevates); S6 precedent (VERIFY wins over DISCOVER).
- §6.7 F-SCOUT-V-01..06 — the only failure codes this module emits.
- §8 numeric pins: ``SCOUT_CANDIDATE_VERIFY_CAP = 1000``,
  ``SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO = 0.25``,
  ``VERIFY_LIVE_SYNOPSIS_TIMEOUT_S = 10``,
  ``VERIFY_POOL_MAX_WORKERS = 4``.
- A-09 / RT-v1-MED-03 — global 1000-cap before the pool.
- A-v3-01 / RT-v2-HIGH-01 + MED-02 + LOW-02 — per-run-seeded tiebreak
  (``seed XOR sha3_512(canonical_json(c))[:16]``) + DEGRADE-on-overflow
  above ``ratio × cap``.
- Architecture line 275-278 — VERIFY records facts (synopsis hash,
  timestamp, verdict); Section 4 Logician decides admissibility.
- Autonomy Rule 1 — checkpoint at ``verify_start`` / every
  ``verify_candidate_complete`` (on success AND failure) /
  ``verify_complete`` / ``verify_interrupted``.

Spec-card deviation notes (from pre-staged
``spec_cards/scout_round_9_verify.md`` v1):

- Spec card's proposed F-SCOUT-V-01..07 taxonomy diverged from the LOCKED
  blueprint §6.7 six-code surface. Build follows the blueprint; the spec
  card's V-07 aggregate-failed-ratio has no blueprint row and is NOT
  emitted. The spec card's V-03 cap-degraded collides with blueprint
  V-03 body-parse — build uses the blueprint V-05 ``.truncation_degrades``
  sub-code instead. Disposition: blueprint wins per L-001 (RFA/blueprint
  is truth).
- Spec card's A→F + ``candidate_id`` truncation order is the v2 design
  A-v3-01 explicitly replaces (blueprint line 662). Build implements the
  v3 ``(-fit_score_cached, seed XOR sha3_512(canonical_json(c))[:16])``
  key as the blueprint code sketch at §4.7 line 670 dictates.
- Spec card's ``DEGRADE_RATIO = 1.1`` contradicts the pinned
  ``_constants.py:41`` value of ``0.25``. Build uses the pinned constant.
- Structural FIT gate implements the full ``_match_applicant`` surface
  from blueprint §4.7 lines 642-652: eligibility, scale, geography,
  timing. :class:`ApplicantProfileProvider` is a new E-017 seam;
  concrete materialisation from Section 1's ``PROJECTContextEnvelope``
  is Round 11 capstone scope. Verify_stage threads the profile through
  — it does not construct it.
- ``ApplicantProfile`` geography model: ``None`` geographies (either
  profile or live) pass the timing/scale axes but do not satisfy the
  geography axis. Explicit geography pin required for FIT.

No module-level side effects on import. Zero network, zero FD
reservation, zero nonce reservation, zero vault_read. All persistence
routes through injected Protocols (E-017 — eighth reuse). AST-lint
R1/R3/R4/R5 clean.
"""

from __future__ import annotations

import concurrent.futures as _cf
import datetime as _dt
import hashlib
import time
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    ContextManager,
    Final,
    Mapping,
    Optional,
    Protocol,
    runtime_checkable,
)

from pipeline.scout._constants import (
    SCOUT_CANDIDATE_VERIFY_CAP,
    SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO,
    VERDICT_UNVERIFIED,
    VERDICT_VERIFICATION_FAILED,
    VERDICT_VERIFIED_FIT,
    VERDICT_VERIFIED_NOT_FIT,
    VERIFY_LIVE_SYNOPSIS_TIMEOUT_S,
    VERIFY_POOL_MAX_WORKERS,
)
from pipeline.scout._types import (
    Candidate,
    VerificationVerdict,
    candidate_canonical_bytes,
)
from pipeline.scout.discover import ScoutDiscoverResult

__version__: Final[str] = "0.1.0-scout-r9"

__all__ = [
    "ApplicantProfile",
    "ApplicantProfileProvider",
    "CheckpointWriter",
    "ClockFn",
    "DegradationWriter",
    "ExecutorFactory",
    "ExecutorLike",
    "F_SCOUT_V_01",
    "F_SCOUT_V_02",
    "F_SCOUT_V_03",
    "F_SCOUT_V_04",
    "F_SCOUT_V_05",
    "F_SCOUT_V_06",
    "FutureLike",
    "InterruptProbe",
    "LiveSynopsis",
    "REASON_A_ELIG_01",
    "REASON_A_GEO_01",
    "REASON_A_SCALE_01",
    "REASON_A_SCALE_02",
    "REASON_A_TIME_01",
    "REASON_NO_LIVE_ENDPOINT",
    "REASON_V_OK",
    "SEVERITY_HIGH",
    "SEVERITY_LOW",
    "SEVERITY_MEDIUM",
    "ScoutVerifyInterrupted",
    "ScoutVerifyResult",
    "SessionLike",
    "SynopsisFetcher",
    "SynopsisFetchError",
    "SynopsisNoLiveEndpoint",
    "SynopsisParseError",
    "SynopsisTimeoutError",
    "SynopsisUrlResolutionError",
    "TRUNCATION_BOUNDED",
    "TRUNCATION_DEGRADES",
    "VerifyCandidateCallable",
    "VerifyDegradationEvent",
    "VerifyStageState",
    "VERIFY_STAGE_DEGRADED",
    "VERIFY_STAGE_OK",
    "_RUN_TIEBREAK_SEED_LEN",
    "__version__",
    "verify_all",
    "verify_candidate",
]


# ---------------------------------------------------------------------------
# Failure codes (blueprint §6.7 — verbatim)
# ---------------------------------------------------------------------------

F_SCOUT_V_01: Final[str] = "F-SCOUT-V-01"  # live endpoint URL resolution failed
F_SCOUT_V_02: Final[str] = "F-SCOUT-V-02"  # live fetch timed out
F_SCOUT_V_03: Final[str] = "F-SCOUT-V-03"  # live synopsis body parse failed
F_SCOUT_V_04: Final[str] = "F-SCOUT-V-04"  # double-fetch content_hash drift
F_SCOUT_V_05: Final[str] = "F-SCOUT-V-05"  # cap overflow truncation
F_SCOUT_V_06: Final[str] = "F-SCOUT-V-06"  # tiebreak integrity


# ---------------------------------------------------------------------------
# Reason codes (blueprint §4.7 _match_applicant + §2.2 VerificationVerdict)
# ---------------------------------------------------------------------------

REASON_V_OK: Final[str] = "V-OK"
REASON_NO_LIVE_ENDPOINT: Final[str] = "V-NO-ENDPOINT"
REASON_A_ELIG_01: Final[str] = "A-ELIG-01"
REASON_A_SCALE_01: Final[str] = "A-SCALE-01"
REASON_A_SCALE_02: Final[str] = "A-SCALE-02"
REASON_A_GEO_01: Final[str] = "A-GEO-01"
REASON_A_TIME_01: Final[str] = "A-TIME-01"


# ---------------------------------------------------------------------------
# Severity tags (mirror Round 8 capstone severity scale)
# ---------------------------------------------------------------------------

SEVERITY_LOW: Final[str] = "LOW"
SEVERITY_MEDIUM: Final[str] = "MEDIUM"
SEVERITY_HIGH: Final[str] = "HIGH"


# ---------------------------------------------------------------------------
# F-SCOUT-V-05 reason-tag sub-codes (blueprint §4.7 + §6.7)
# ---------------------------------------------------------------------------

TRUNCATION_BOUNDED: Final[str] = "F-SCOUT-V-05.truncation_bounded"
TRUNCATION_DEGRADES: Final[str] = "F-SCOUT-V-05.truncation_degrades"


# ---------------------------------------------------------------------------
# Verify-stage state (blueprint §4.7: DEGRADED iff truncation_degrades)
# ---------------------------------------------------------------------------

VerifyStageState = str
VERIFY_STAGE_OK: Final[str] = "OK"
VERIFY_STAGE_DEGRADED: Final[str] = "DEGRADED"


# ---------------------------------------------------------------------------
# Internal constants
# ---------------------------------------------------------------------------

_RUN_TIEBREAK_SEED_LEN: Final[int] = 16


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class SynopsisFetchError(Exception):
    """Base for fetcher-signalled transport/parse errors.

    Concrete subclasses map 1:1 to blueprint §6.7 codes:

    - :class:`SynopsisUrlResolutionError` → F-SCOUT-V-01
    - :class:`SynopsisTimeoutError`       → F-SCOUT-V-02
    - :class:`SynopsisParseError`         → F-SCOUT-V-03

    A fetcher that wants to indicate "no live endpoint for this channel"
    raises :class:`SynopsisNoLiveEndpoint` (which maps to UNVERIFIED, not
    FAILED) — or returns ``None``; both paths are equivalent.
    """


class SynopsisUrlResolutionError(SynopsisFetchError):
    """F-SCOUT-V-01 — live endpoint URL resolution failed."""


class SynopsisTimeoutError(SynopsisFetchError):
    """F-SCOUT-V-02 — live fetch exceeded ``timeout_seconds``."""


class SynopsisParseError(SynopsisFetchError):
    """F-SCOUT-V-03 — live synopsis body did not parse."""


class SynopsisNoLiveEndpoint(Exception):
    """No live-synopsis endpoint exists for this candidate's channel.

    Maps to ``VerificationVerdict.verdict = "UNVERIFIED"`` (L-001
    precedent: UNVERIFIED is a deterministic fallback, not a failure).
    """


class ScoutVerifyInterrupted(RuntimeError):
    """``interrupt_probe()`` fired mid-pool; pending futures cancelled.

    Carries the ordered tuple of candidate_ids whose verify completed
    before the interrupt was observed. Section 5's resume path reads
    the ``verify_interrupted`` checkpoint, not this object.
    """

    def __init__(self, completed_candidate_ids: tuple[str, ...]):
        self.completed_candidate_ids = completed_candidate_ids
        super().__init__(
            f"VERIFY interrupted after completed_candidate_ids="
            f"{completed_candidate_ids!r}"
        )


# ---------------------------------------------------------------------------
# Injection Protocols (E-017 — eighth reuse in Scout)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class LiveSynopsis:
    """Fetcher-returned payload — §4.7 ``LiveSynopsis`` shape.

    ``synopsis_url`` is the exact URL that was fetched (never a search
    URL). ``content_hash`` is sha3_512 of the bytes the fetcher parsed.
    Tuples over lists for hashability and canonical-JSON stability.
    """

    synopsis_url: str
    content_hash: str
    fetched_at_utc: str
    eligibility_live: tuple[str, ...]
    award_floor_live: Optional[int]
    award_ceiling_live: Optional[int]
    close_date_live_utc: Optional[str]
    eligible_geographies: tuple[str, ...]
    evidence_quote: Optional[str]


@dataclass(frozen=True, kw_only=True)
class ApplicantProfile:
    """Session applicant profile — §4.7 ``ApplicantProfile`` shape.

    Materialised from Section 1's ``PROJECTContextEnvelope`` by the
    Round 11 capstone via :class:`ApplicantProfileProvider`. Verify
    stage never mutates the profile; per blueprint "Scout does not
    mutate it" (§4.7 line 654).

    Axes — every axis must pass for FIT:

    - ``applicant_types`` — intersect with live.eligibility_live
    - ``max_award_capacity`` / ``min_award_need`` — scale bounds
    - ``geography`` — must be in live.eligible_geographies
    - ``min_lead_time_days`` — close_date minus now must exceed this

    ``geography=None`` does not satisfy the geography axis; profiles
    that do not pin a geography cannot pass VERIFY FIT.
    """

    applicant_types: tuple[str, ...]
    max_award_capacity: Optional[int]
    min_award_need: Optional[int]
    geography: Optional[str]
    min_lead_time_days: int


class SessionLike(Protocol):
    """Duck-type shape this module needs from a sovereignty session.

    Narrower than :class:`pipeline.sovereignty.session.Session`. The
    full Section 1 Session satisfies this Protocol. Tests inject a
    dataclass with the two string fields.
    """

    session_id: str
    slug: str


@runtime_checkable
class SynopsisFetcher(Protocol):
    """Per-candidate live-synopsis fetch seam (NEW — E-017 eighth firing).

    Implementations bind to a higher-level fetch helper that wraps
    Round 4's :class:`HTTPClient` + :class:`FDBroker` + nonce registry
    + parser. Verify stage stays transport-agnostic.

    Contract:

    - Returning ``None`` or raising :class:`SynopsisNoLiveEndpoint`
      signals UNVERIFIED (deterministic; the channel has no live
      endpoint).
    - Raising :class:`SynopsisUrlResolutionError` → F-SCOUT-V-01.
    - Raising :class:`SynopsisTimeoutError` → F-SCOUT-V-02.
    - Raising :class:`SynopsisParseError` → F-SCOUT-V-03.
    - Any other :class:`Exception` propagates to ``verify_all`` which
      assigns VERIFICATION_FAILED with reason-code
      ``"F-SCOUT-V-03.parse_unknown"`` — a programming bug on the
      fetcher side, not a runtime condition.

    ``timeout_seconds`` is handed through so the fetcher can bind its
    transport timeout — the module does NOT enforce a wall-clock kill
    (that is the fetcher's responsibility to bind into its client).
    """

    def fetch(
        self,
        *,
        candidate: Candidate,
        timeout_seconds: int,
    ) -> Optional[LiveSynopsis]: ...


@runtime_checkable
class ApplicantProfileProvider(Protocol):
    """Session applicant-profile seam (NEW — E-017 eighth firing).

    Production binding reads Section 1's ``PROJECTContextEnvelope``
    at session start and caches the profile for the run. Tests inject
    a recording fake.

    The provider is invoked once per ``verify_all`` call (not once per
    candidate) — profile is constant across a VERIFY pass.
    """

    def get(self, *, session: SessionLike) -> ApplicantProfile: ...


class CheckpointWriter(Protocol):
    """Autonomy Rule 1 — save state always.

    Production binding wraps
    :func:`pipeline.sovereignty.interrupted_state.checkpoint`. Tests
    inject an in-memory recorder that captures ``(stage, payload)``
    tuples for assertion.
    """

    def write(self, *, stage: str, payload: Mapping[str, Any]) -> None: ...


class DegradationWriter(Protocol):
    """Injected sink for verify-stage degradation events.

    Production binding wraps
    :func:`pipeline.sovereignty.degradation_log.record_degradation`
    with per-session keys + repo_root closed over. Tests inject a
    recorder that captures :class:`VerifyDegradationEvent` instances.
    """

    def record(self, event: "VerifyDegradationEvent") -> None: ...


class FutureLike(Protocol):
    """Minimal future surface the pool loop requires.

    Matches Round 8's Protocol so production ``ThreadPoolExecutor``
    futures satisfy both modules without adapter code.
    """

    def result(self, timeout: Optional[float] = None) -> Any: ...
    def cancel(self) -> bool: ...


class ExecutorLike(Protocol):
    """Context-manager-compatible executor with ``.submit`` semantics."""

    def submit(self, fn: Callable[[], Any], /) -> FutureLike: ...
    def __enter__(self) -> "ExecutorLike": ...
    def __exit__(self, exc_type, exc, tb) -> Optional[bool]: ...


ExecutorFactory = Callable[[int], ContextManager[ExecutorLike]]
"""Factory returning an executor sized for ``max_workers`` verifies.

Production default binds to ``ThreadPoolExecutor(max_workers=4)``
(``VERIFY_POOL_MAX_WORKERS`` pin per §8). Tests inject
:class:`SequentialFakeExecutor` (Round 8 pattern) for deterministic
scheduling without thread non-determinism.
"""


class InterruptProbe(Protocol):
    """Nullary predicate — True iff an interrupt has been signalled.

    Production binding wraps
    :func:`pipeline.sovereignty.interrupted_state.detect_interrupted`.
    Tests inject a toggle.
    """

    def __call__(self) -> bool: ...


ClockFn = Callable[[], _dt.datetime]
"""Clock returning UTC-aware ``datetime``.

Production default binds to ``lambda: datetime.datetime.now(UTC)``.
Tests inject a :class:`MockClock` that returns a fixed sequence.
"""


VerifyCandidateCallable = Callable[..., VerificationVerdict]
"""Injected-seat typing for :func:`verify_candidate`.

Tests that want to bypass the full verify_candidate pathway (e.g. to
inject a forced exception per candidate) pass a fake via the
``verify_fn`` argument of :func:`verify_all`.
"""


# ---------------------------------------------------------------------------
# VerifyDegradationEvent
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class VerifyDegradationEvent:
    """One-line verify-stage event.

    Scope: events INTRODUCED by the verify stage (cap overflow,
    tiebreak-integrity, structural-gate rejection of a single
    candidate is NOT a degradation — it is a verdict outcome). The
    structural-gate reason is carried on :class:`VerificationVerdict`
    itself via ``reason_code``.
    """

    source: str
    code: str
    reason_tag: Optional[str]
    severity: str
    candidate_id: Optional[str] = None


# ---------------------------------------------------------------------------
# ScoutVerifyResult — capstone return shape
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ScoutVerifyResult:
    """VERIFY-stage output consumed by Round 10 (REVIEW) + Round 11.

    ``verdicts`` is keyed by ``candidate_id``; the mapping carries the
    post-truncation set only (overflow candidates are not verified).
    ``overflow`` is the count of candidates dropped by the cap.
    ``verify_stage_state`` follows the blueprint §4.7 rule: DEGRADED
    iff ``overflow > ratio × cap``.
    """

    verdicts: Mapping[str, VerificationVerdict]
    verify_stage_state: VerifyStageState
    cap_applied: bool
    overflow: int
    verify_degradation_events: tuple[VerifyDegradationEvent, ...]


# ---------------------------------------------------------------------------
# Default factories — bound to production primitives at call-site
# ---------------------------------------------------------------------------


def _default_clock() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


def _default_interrupt_probe() -> bool:
    return False


class _ThreadPoolExecutorAdapter:
    """Context-manager adapter returning a real stdlib ThreadPoolExecutor.

    Mirrors Round 8's pattern so the default ``ExecutorFactory`` is a
    plain callable — tests replace the factory without monkey-patching
    ``concurrent.futures``.
    """

    def __init__(self, max_workers: int) -> None:
        self._max_workers = max_workers
        self._pool: Optional[_cf.ThreadPoolExecutor] = None

    def __enter__(self) -> "_ThreadPoolExecutorAdapter":
        self._pool = _cf.ThreadPoolExecutor(max_workers=self._max_workers)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._pool is not None:
            self._pool.shutdown(wait=True, cancel_futures=True)

    def submit(self, fn: Callable[[], Any], /) -> FutureLike:
        if self._pool is None:  # pragma: no cover - contract-unreachable; context-manager guarded
            raise RuntimeError("executor used outside context-manager scope")
        return self._pool.submit(fn)


def _default_executor_factory(max_workers: int) -> ContextManager[ExecutorLike]:
    return _ThreadPoolExecutorAdapter(max_workers)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _verify_sort_key(candidate: Candidate, seed: bytes) -> tuple[int, bytes]:
    """Blueprint §4.7 line 670 — primary fit_score desc, secondary seed-XOR.

    Primary negated so ``sorted(..., key=_verify_sort_key)`` yields
    descending ``fit_score_cached``. Secondary XORs the 16-byte seed
    with ``sha3_512(canonical_json(candidate))[:16]`` — any field an
    attacker controls is covered by the hash input, and the per-run
    seed makes the attacker unable to target a low secondary key
    (A-v3-01 / RT-v2-HIGH-01 closure).

    Raises :class:`RuntimeError` tagged ``F-SCOUT-V-06`` if
    ``candidate_canonical_bytes`` raises — tiebreak integrity event.
    """
    try:
        canonical = candidate_canonical_bytes(candidate)
    except Exception as exc:
        raise RuntimeError(
            f"{F_SCOUT_V_06}: canonical_json(candidate="
            f"{candidate.candidate_id!r}) raised "
            f"{type(exc).__name__}: {exc}"
        ) from exc
    digest16 = hashlib.sha3_512(canonical).digest()[:16]
    xored = bytes(a ^ b for a, b in zip(seed, digest16))
    return (-candidate.fit_score_cached, xored)


def _assert_seed_length(seed: bytes) -> None:
    """F-SCOUT-V-06 — ``run_tiebreak_seed`` length invariant.

    Raises :class:`RuntimeError` tagged ``F-SCOUT-V-06`` on any
    deviation from 16 bytes. A Round 8 invariant violation at the
    handoff boundary is HIGH admin-risk (internal bug).
    """
    if not isinstance(seed, bytes):
        raise RuntimeError(
            f"{F_SCOUT_V_06}: run_tiebreak_seed is "
            f"{type(seed).__name__}, expected bytes"
        )
    if len(seed) != _RUN_TIEBREAK_SEED_LEN:
        raise RuntimeError(
            f"{F_SCOUT_V_06}: run_tiebreak_seed length="
            f"{len(seed)} (expected {_RUN_TIEBREAK_SEED_LEN})"
        )


def _truncate_candidates(
    candidates: tuple[Candidate, ...],
    seed: bytes,
) -> tuple[tuple[Candidate, ...], int]:
    """Blueprint §4.7 lines 681-683 — truncate to top-cap by sort key.

    Returns the kept candidates (ordered by sort key) plus the
    overflow count. Overflow candidates are dropped here; the
    operator-facing record is emitted by ``verify_all`` via
    :class:`DegradationWriter` with reason-tag sub-code.
    """
    ordered = sorted(candidates, key=lambda c: _verify_sort_key(c, seed))
    overflow = max(0, len(ordered) - SCOUT_CANDIDATE_VERIFY_CAP)
    kept = ordered[:SCOUT_CANDIDATE_VERIFY_CAP]
    return tuple(kept), overflow


def _degrade_threshold() -> int:
    """int(ratio × cap) — blueprint §4.7 lines 688 + 694.

    ``int(0.25 * 1000) = 250``. Overflow STRICTLY greater than this
    flips verify-stage to DEGRADED; ``overflow == 250`` stays
    ``.truncation_bounded``.
    """
    return int(SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO * SCOUT_CANDIDATE_VERIFY_CAP)


def _normalize_applicant_token(token: str) -> str:
    """Narrow normalization for eligibility-token intersection.

    Blueprint §4.7 line 645 references ``_normalize_applicant_type``
    without specifying the shape. Verify stage uses a defensible
    lower+strip normalization; broader normalization (e.g. mapping
    "nonprofit" ↔ "non-profit") is deferred to the optional
    normalization hook the profile provider can bake into its
    ``applicant_types`` tuple. This is documented as a spec-card
    deviation in the module docstring.
    """
    return token.strip().lower()


def _match_applicant(
    live: LiveSynopsis,
    profile: ApplicantProfile,
    *,
    now_utc: _dt.datetime,
) -> tuple[bool, str]:
    """Blueprint §4.7 lines 642-652 — deterministic four-axis FIT gate.

    Every axis must pass for ``(True, "V-OK")``; short-circuits on
    first failure and returns ``(False, reason_code)``. Reason-code
    order mirrors the blueprint code sketch: eligibility → scale →
    geography → timing.
    """
    # Eligibility
    live_tokens = {_normalize_applicant_token(t) for t in live.eligibility_live}
    profile_tokens = {_normalize_applicant_token(t) for t in profile.applicant_types}
    if not live_tokens & profile_tokens:
        return (False, REASON_A_ELIG_01)
    # Scale
    if (
        profile.max_award_capacity is not None
        and live.award_floor_live is not None
        and profile.max_award_capacity < live.award_floor_live
    ):
        return (False, REASON_A_SCALE_01)
    if (
        profile.min_award_need is not None
        and live.award_ceiling_live is not None
        and profile.min_award_need > live.award_ceiling_live
    ):
        return (False, REASON_A_SCALE_02)
    # Geography
    if profile.geography is None or profile.geography not in live.eligible_geographies:
        return (False, REASON_A_GEO_01)
    # Timing
    if live.close_date_live_utc is not None:
        try:
            close_dt = _dt.datetime.fromisoformat(
                live.close_date_live_utc.replace("Z", "+00:00")
            )
        except ValueError:
            # Malformed close-date is a parse concern, not a timing
            # concern. The fetcher is responsible for well-formed
            # dates; if it emits an ISO-8601 string we cannot parse,
            # treat as a timing failure rather than a silent pass.
            return (False, REASON_A_TIME_01)
        if close_dt.tzinfo is None:
            close_dt = close_dt.replace(tzinfo=_dt.timezone.utc)
        lead_td = close_dt - now_utc
        if lead_td.total_seconds() < profile.min_lead_time_days * 86400:
            return (False, REASON_A_TIME_01)
    return (True, REASON_V_OK)


def _mk_verdict(
    *,
    candidate: Candidate,
    verdict: str,
    reason_code: str,
    timeout_seconds: int,
    live: Optional[LiveSynopsis],
) -> VerificationVerdict:
    """Assemble a VerificationVerdict from the four outcome paths.

    For UNVERIFIED / VERIFICATION_FAILED paths, ``live`` is ``None``
    — the verdict carries ``live_synopsis_url=None``,
    ``live_content_hash=None``, ``fetched_at_utc=None``, and empty
    ``eligibility_live``. For VERIFIED_* paths, the live fields are
    copied directly from :class:`LiveSynopsis`.
    """
    if live is None:
        return VerificationVerdict(
            candidate_id=candidate.candidate_id,
            verdict=verdict,
            reason_code=reason_code,
            live_synopsis_url=None,
            live_content_hash=None,
            fetched_at_utc=None,
            timeout_seconds=timeout_seconds,
            eligibility_live=(),
            award_floor_live=None,
            award_ceiling_live=None,
            close_date_live_utc=None,
            evidence_quote=None,
        )
    return VerificationVerdict(
        candidate_id=candidate.candidate_id,
        verdict=verdict,
        reason_code=reason_code,
        live_synopsis_url=live.synopsis_url,
        live_content_hash=live.content_hash,
        fetched_at_utc=live.fetched_at_utc,
        timeout_seconds=timeout_seconds,
        eligibility_live=live.eligibility_live,
        award_floor_live=live.award_floor_live,
        award_ceiling_live=live.award_ceiling_live,
        close_date_live_utc=live.close_date_live_utc,
        evidence_quote=live.evidence_quote,
    )


# ---------------------------------------------------------------------------
# Public entry — verify_candidate
# ---------------------------------------------------------------------------


def verify_candidate(
    *,
    session: SessionLike,
    candidate: Candidate,
    synopsis_fetcher: SynopsisFetcher,
    applicant_profile: ApplicantProfile,
    clock: ClockFn = _default_clock,
    timeout_seconds: int = VERIFY_LIVE_SYNOPSIS_TIMEOUT_S,
) -> VerificationVerdict:
    """Single-candidate verify — blueprint §4.7 ``verify_candidate``.

    Never raises on fetch failure (per blueprint line 620) — returns
    :class:`VerificationVerdict` tagged with the right verdict class
    and reason code.

    Dispatch:

    - Fetcher returns ``None`` OR raises :class:`SynopsisNoLiveEndpoint`
      → UNVERIFIED + ``V-NO-ENDPOINT``.
    - Fetcher raises :class:`SynopsisUrlResolutionError` →
      VERIFICATION_FAILED + F-SCOUT-V-01.
    - Fetcher raises :class:`SynopsisTimeoutError` →
      VERIFICATION_FAILED + F-SCOUT-V-02.
    - Fetcher raises :class:`SynopsisParseError` →
      VERIFICATION_FAILED + F-SCOUT-V-03.
    - Fetcher raises any other :class:`Exception` → VERIFICATION_FAILED
      + ``F-SCOUT-V-03.parse_unknown`` (unexpected fetcher bug; the
      module treats this defensively rather than propagating — L-001
      precedent that VERIFY never crashes the Scout run).
    - Fetcher returns :class:`LiveSynopsis` → dispatch to
      :func:`_match_applicant`: FIT → VERIFIED_FIT + ``V-OK``;
      NOT_FIT → VERIFIED_NOT_FIT + axis-specific reason code.

    ``(KeyboardInterrupt, SystemExit)`` propagate unchanged. The
    ``session`` argument is threaded for future log-correlation hooks
    but is not dereferenced in v0.1 — verify_stage is session-aware
    by contract, not by field access.
    """
    _ = session  # reserved for future log-correlation
    try:
        live = synopsis_fetcher.fetch(
            candidate=candidate, timeout_seconds=timeout_seconds
        )
    except SynopsisNoLiveEndpoint:
        return _mk_verdict(
            candidate=candidate,
            verdict=VERDICT_UNVERIFIED,
            reason_code=REASON_NO_LIVE_ENDPOINT,
            timeout_seconds=timeout_seconds,
            live=None,
        )
    except SynopsisUrlResolutionError:
        return _mk_verdict(
            candidate=candidate,
            verdict=VERDICT_VERIFICATION_FAILED,
            reason_code=F_SCOUT_V_01,
            timeout_seconds=timeout_seconds,
            live=None,
        )
    except SynopsisTimeoutError:
        return _mk_verdict(
            candidate=candidate,
            verdict=VERDICT_VERIFICATION_FAILED,
            reason_code=F_SCOUT_V_02,
            timeout_seconds=timeout_seconds,
            live=None,
        )
    except SynopsisParseError:
        return _mk_verdict(
            candidate=candidate,
            verdict=VERDICT_VERIFICATION_FAILED,
            reason_code=F_SCOUT_V_03,
            timeout_seconds=timeout_seconds,
            live=None,
        )
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception:
        return _mk_verdict(
            candidate=candidate,
            verdict=VERDICT_VERIFICATION_FAILED,
            reason_code=f"{F_SCOUT_V_03}.parse_unknown",
            timeout_seconds=timeout_seconds,
            live=None,
        )

    if live is None:
        return _mk_verdict(
            candidate=candidate,
            verdict=VERDICT_UNVERIFIED,
            reason_code=REASON_NO_LIVE_ENDPOINT,
            timeout_seconds=timeout_seconds,
            live=None,
        )

    is_fit, reason = _match_applicant(
        live, applicant_profile, now_utc=clock()
    )
    if is_fit:
        return _mk_verdict(
            candidate=candidate,
            verdict=VERDICT_VERIFIED_FIT,
            reason_code=reason,
            timeout_seconds=timeout_seconds,
            live=live,
        )
    return _mk_verdict(
        candidate=candidate,
        verdict=VERDICT_VERIFIED_NOT_FIT,
        reason_code=reason,
        timeout_seconds=timeout_seconds,
        live=live,
    )


# ---------------------------------------------------------------------------
# Public entry — verify_all
# ---------------------------------------------------------------------------


def verify_all(
    *,
    session: SessionLike,
    discover_result: ScoutDiscoverResult,
    synopsis_fetcher: SynopsisFetcher,
    applicant_profile_provider: ApplicantProfileProvider,
    checkpoint_writer: CheckpointWriter,
    degradation_writer: DegradationWriter,
    executor_factory: ExecutorFactory = _default_executor_factory,
    interrupt_probe: InterruptProbe = _default_interrupt_probe,
    clock: ClockFn = _default_clock,
    verify_fn: VerifyCandidateCallable = verify_candidate,
    timeout_seconds: int = VERIFY_LIVE_SYNOPSIS_TIMEOUT_S,
) -> ScoutVerifyResult:
    """Blueprint §4.7 ``verify_all`` — parallel bounded-pool VERIFY pass.

    1. Validate ``run_tiebreak_seed`` length (F-SCOUT-V-06).
    2. Truncate to ``SCOUT_CANDIDATE_VERIFY_CAP`` by the A-v3-01 sort
       key. Emit F-SCOUT-V-05 with ``.truncation_bounded`` or
       ``.truncation_degrades`` sub-tag on overflow.
    3. Materialise the applicant profile once.
    4. Submit each surviving candidate to an injected executor
       (``VERIFY_POOL_MAX_WORKERS = 4`` workers). Each submission is a
       closure over ``verify_fn`` + the shared profile/fetcher/clock.
    5. Pre-submit + inter-candidate interrupt checks: on True, cancel
       pending futures and raise :class:`ScoutVerifyInterrupted` with
       the completed ids.
    6. Per-candidate checkpoint on success AND failure. An internal
       exception from ``verify_fn`` is caught (module contract:
       VERIFY never crashes the Scout run) — the candidate is tagged
       VERIFICATION_FAILED with reason ``F-SCOUT-V-03.verify_fn_raised``.
    7. ``verify_complete`` checkpoint + :class:`ScoutVerifyResult`.

    :raises RuntimeError: F-SCOUT-V-06 — ``run_tiebreak_seed`` length
        invariant violated at the handoff boundary (bug).
    :raises ScoutVerifyInterrupted: interrupt observed mid-pool; any
        completed verdicts are recorded in the ``verify_interrupted``
        checkpoint payload, not on the raised exception.
    :raises KeyboardInterrupt / SystemExit: re-raised unchanged when
        a pool thread raises one — never caught by ``except Exception``.
    """
    seed = discover_result.run_tiebreak_seed
    _assert_seed_length(seed)

    total = len(discover_result.candidates)
    truncated, overflow = _truncate_candidates(
        discover_result.candidates, seed
    )

    events: list[VerifyDegradationEvent] = []
    cap_applied = overflow > 0
    verify_stage_state: VerifyStageState = VERIFY_STAGE_OK

    if cap_applied:
        threshold = _degrade_threshold()
        crossed = overflow > threshold
        sub_tag = TRUNCATION_DEGRADES if crossed else TRUNCATION_BOUNDED
        event = VerifyDegradationEvent(
            source="verify_all",
            code=F_SCOUT_V_05,
            reason_tag=(
                f"{sub_tag}; input={total} cap={SCOUT_CANDIDATE_VERIFY_CAP} "
                f"overflow={overflow} threshold={threshold}"
            ),
            severity=SEVERITY_HIGH if crossed else SEVERITY_MEDIUM,
            candidate_id=None,
        )
        events.append(event)
        degradation_writer.record(event)
        if crossed:
            verify_stage_state = VERIFY_STAGE_DEGRADED

    checkpoint_writer.write(
        stage="verify_start",
        payload={
            "session_id": session.session_id,
            "slug": session.slug,
            "run_id": discover_result.run_id,
            "n_input_candidates": total,
            "n_verify_candidates": len(truncated),
            "overflow": overflow,
            "cap_applied": cap_applied,
            "verify_stage_state": verify_stage_state,
        },
    )

    profile = applicant_profile_provider.get(session=session)

    verdicts: dict[str, VerificationVerdict] = {}
    completed: list[str] = []

    # Pre-submit interrupt check keeps the discover-verify boundary
    # consistent with Round 8's checkpoint-before-cancel pattern.
    if interrupt_probe():
        checkpoint_writer.write(
            stage="verify_interrupted",
            payload={
                "run_id": discover_result.run_id,
                "completed_candidate_ids": [],
                "stage_at_interrupt": "before_pool",
            },
        )
        raise ScoutVerifyInterrupted(())

    def _invoke(c: Candidate) -> VerificationVerdict:
        return verify_fn(
            session=session,
            candidate=c,
            synopsis_fetcher=synopsis_fetcher,
            applicant_profile=profile,
            clock=clock,
            timeout_seconds=timeout_seconds,
        )

    with executor_factory(VERIFY_POOL_MAX_WORKERS) as pool:
        futures: list[tuple[Candidate, FutureLike]] = []
        for candidate in truncated:
            futures.append((candidate, pool.submit(lambda c=candidate: _invoke(c))))

        for candidate, fut in futures:
            if interrupt_probe():
                for _c, pending in futures:
                    if _c.candidate_id not in completed:
                        pending.cancel()
                checkpoint_writer.write(
                    stage="verify_interrupted",
                    payload={
                        "run_id": discover_result.run_id,
                        "completed_candidate_ids": list(completed),
                        "stage_at_interrupt": "mid_pool",
                        "pending_candidate_id": candidate.candidate_id,
                    },
                )
                raise ScoutVerifyInterrupted(tuple(completed))

            try:
                verdict = fut.result()
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as exc:
                verdict = _mk_verdict(
                    candidate=candidate,
                    verdict=VERDICT_VERIFICATION_FAILED,
                    reason_code=f"{F_SCOUT_V_03}.verify_fn_raised",
                    timeout_seconds=timeout_seconds,
                    live=None,
                )
                event = VerifyDegradationEvent(
                    source="verify_all",
                    code=F_SCOUT_V_03,
                    reason_tag=(
                        f"verify_fn raised {type(exc).__name__}: {exc}"
                    ),
                    severity=SEVERITY_HIGH,
                    candidate_id=candidate.candidate_id,
                )
                events.append(event)
                degradation_writer.record(event)

            verdicts[candidate.candidate_id] = verdict
            completed.append(candidate.candidate_id)
            checkpoint_writer.write(
                stage="verify_candidate_complete",
                payload={
                    "run_id": discover_result.run_id,
                    "candidate_id": candidate.candidate_id,
                    "verdict": verdict.verdict,
                    "reason_code": verdict.reason_code,
                    "n_completed": len(completed),
                },
            )

    checkpoint_writer.write(
        stage="verify_complete",
        payload={
            "run_id": discover_result.run_id,
            "n_verdicts": len(verdicts),
            "n_events": len(events),
            "verify_stage_state": verify_stage_state,
            "overflow": overflow,
        },
    )

    return ScoutVerifyResult(
        verdicts=dict(verdicts),
        verify_stage_state=verify_stage_state,
        cap_applied=cap_applied,
        overflow=overflow,
        verify_degradation_events=tuple(events),
    )


# ---------------------------------------------------------------------------
# Side-effect-free import invariant
# ---------------------------------------------------------------------------


# Explicitly reference ``time`` so linters do not strip the import; the
# default-clock path uses ``datetime.datetime.now`` but the time module
# may be imported by test-injected clock shims that wrap monotonic_ns.
_ = time  # noqa: F841
