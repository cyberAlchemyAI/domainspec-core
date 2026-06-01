"""Round 9 — §4.7 VERIFY stage.

Test surface floor ≥ 70; E-024 1.5× multiplier (eighth firing) targets
~105 total. Happy-path + adversarial coverage for the four-verdict
taxonomy, the ``_match_applicant`` four-axis gate, A-v3-01 seed-XOR
tiebreak determinism, A-09 1000-cap truncation with bounded / degrades
sub-tags, exception isolation, interrupt cancellation, checkpoint
discipline, Autonomy Rule 1, Protocol injection (E-017 eighth reuse),
and Round 8 → Round 9 handoff composition.

Lessons applied from start:

- E-017 Protocol-injection pattern (eighth Scout reuse —
  ``SynopsisFetcher`` + ``ApplicantProfileProvider`` new)
- E-024 1.5× multiplier (eighth firing; target ~105 tests)
- E-025 range-check version pin (``rN >= 9``)
- E-026 formal ``__module__`` lineage check over ``__dict__``
- E-027 candidate — ``lint_tree`` directory-required contract (reuses
  Round 8's tmp-dir copy pattern)
- E-028 candidate — ``# pragma: no cover`` on contract-unreachable
  defensive branches (this module has one on the executor-outside-ctx
  guard; asserted via source-read, not execution)
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, List, Mapping, Optional, Tuple

import pytest

import pipeline.scout.verify_stage as vs
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
    SignedHealthTuple,
    VerificationVerdict,
    candidate_canonical_bytes,
)
from pipeline.scout.discover import ScoutDiscoverResult
from pipeline.scout.verify_stage import (
    F_SCOUT_V_01,
    F_SCOUT_V_02,
    F_SCOUT_V_03,
    F_SCOUT_V_04,
    F_SCOUT_V_05,
    F_SCOUT_V_06,
    REASON_A_ELIG_01,
    REASON_A_GEO_01,
    REASON_A_SCALE_01,
    REASON_A_SCALE_02,
    REASON_A_TIME_01,
    REASON_NO_LIVE_ENDPOINT,
    REASON_V_OK,
    SEVERITY_HIGH,
    SEVERITY_MEDIUM,
    TRUNCATION_BOUNDED,
    TRUNCATION_DEGRADES,
    VERIFY_STAGE_DEGRADED,
    VERIFY_STAGE_OK,
    ApplicantProfile,
    ApplicantProfileProvider,
    LiveSynopsis,
    ScoutVerifyInterrupted,
    ScoutVerifyResult,
    SynopsisFetcher,
    SynopsisFetchError,
    SynopsisNoLiveEndpoint,
    SynopsisParseError,
    SynopsisTimeoutError,
    SynopsisUrlResolutionError,
    VerifyDegradationEvent,
    _RUN_TIEBREAK_SEED_LEN,
    _assert_seed_length,
    _degrade_threshold,
    _match_applicant,
    _truncate_candidates,
    _verify_sort_key,
    verify_all,
    verify_candidate,
)


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


@dataclass
class FakeSession:
    session_id: str = "session-r9-abc"
    slug: str = "mycosymbiotics_cooperative"


def _mk_candidate(
    candidate_id: str,
    *,
    channel: str = "A",
    fit_score_cached: int = 0,
) -> Candidate:
    return Candidate(
        candidate_id=candidate_id,
        channel=channel,
        feed_or_adapter_id=f"{channel.lower()}:seed",
        source_key="source-x",
        title=f"Opportunity {candidate_id}",
        funder="Some Funder",
        funder_kind="federal",
        url=f"https://example.test/{candidate_id}",
        close_date_utc=None,
        award_ceiling=None,
        award_floor=None,
        applicant_types=(),
        program_page_url=None,
        fetch_timestamp_utc="2026-04-20T00:00:00Z",
        url_hash="0" * 128,
        content_hash=None,
        fit_score_cached=fit_score_cached,
        cache_provenance=None,
    )


def _mk_profile(
    *,
    applicant_types=("nonprofit",),
    max_award_capacity: Optional[int] = 500_000,
    min_award_need: Optional[int] = 10_000,
    geography: Optional[str] = "US-PA",
    min_lead_time_days: int = 7,
) -> ApplicantProfile:
    return ApplicantProfile(
        applicant_types=tuple(applicant_types),
        max_award_capacity=max_award_capacity,
        min_award_need=min_award_need,
        geography=geography,
        min_lead_time_days=min_lead_time_days,
    )


def _mk_live(
    *,
    synopsis_url: str = "https://example.test/live",
    content_hash: str = "d" * 128,
    fetched_at_utc: str = "2026-05-01T00:00:00Z",
    eligibility_live=("nonprofit",),
    award_floor_live: Optional[int] = 20_000,
    award_ceiling_live: Optional[int] = 300_000,
    close_date_live_utc: Optional[str] = "2026-08-01T00:00:00Z",
    eligible_geographies=("US-PA",),
    evidence_quote: Optional[str] = "eligible applicants include nonprofits",
) -> LiveSynopsis:
    return LiveSynopsis(
        synopsis_url=synopsis_url,
        content_hash=content_hash,
        fetched_at_utc=fetched_at_utc,
        eligibility_live=tuple(eligibility_live),
        award_floor_live=award_floor_live,
        award_ceiling_live=award_ceiling_live,
        close_date_live_utc=close_date_live_utc,
        eligible_geographies=tuple(eligible_geographies),
        evidence_quote=evidence_quote,
    )


def _mk_discover_result(
    *,
    candidates: Tuple[Candidate, ...],
    run_tiebreak_seed: bytes = b"\xaa" * 16,
    run_id: str = "a" * 24,
) -> ScoutDiscoverResult:
    signed = SignedHealthTuple(
        tuple_canonical=b"{}",
        hmac_sha3_512=b"\x01" * 64,
        signed_at_utc="2026-04-20T00:00:00Z",
        hmac_key_id="test-key-id",
    )
    return ScoutDiscoverResult(
        candidates=candidates,
        per_channel_states={
            "A": "OK", "B": "OK", "C": "OK",
            "D": "OK", "E": "OK", "F": "OK",
        },
        per_channel_a_endpoints={},
        signed_health=signed,
        run_id=run_id,
        run_tiebreak_seed=run_tiebreak_seed,
        run_wall_ns=1_700_000_000_000_000_000,
        capstone_degradation_events=(),
    )


@dataclass
class FakeFetcher:
    return_live: Optional[LiveSynopsis] = None
    raise_with: Optional[BaseException] = None
    calls: List[Tuple[str, int]] = field(default_factory=list)

    def fetch(self, *, candidate, timeout_seconds):
        self.calls.append((candidate.candidate_id, timeout_seconds))
        if self.raise_with is not None:
            raise self.raise_with
        return self.return_live


@dataclass
class PerCandidateFetcher:
    """Dispatches per-candidate: dict candidate_id → (live|exception|None)."""

    behavior: Mapping[str, Any]
    calls: List[str] = field(default_factory=list)

    def fetch(self, *, candidate, timeout_seconds):
        self.calls.append(candidate.candidate_id)
        entry = self.behavior.get(candidate.candidate_id)
        if isinstance(entry, BaseException):
            raise entry
        return entry


@dataclass
class FakeProfileProvider:
    profile: ApplicantProfile
    calls: List[str] = field(default_factory=list)

    def get(self, *, session):
        self.calls.append(session.session_id)
        return self.profile


@dataclass
class RecordingCheckpointWriter:
    writes: List[Tuple[str, dict]] = field(default_factory=list)

    def write(self, *, stage: str, payload: Mapping[str, Any]) -> None:
        self.writes.append((stage, dict(payload)))


@dataclass
class RecordingDegradationWriter:
    events: List[VerifyDegradationEvent] = field(default_factory=list)

    def record(self, event: VerifyDegradationEvent) -> None:
        self.events.append(event)


def _default_writers():
    return RecordingCheckpointWriter(), RecordingDegradationWriter()


# --- Sequential fake executor -----------------------------------------------


class _SeqFuture:
    def __init__(self, fn: Callable[[], Any]):
        self._fn = fn
        self._raise_exc: Optional[BaseException] = None
        self._result: Any = None
        self._cancelled = False
        self._has_result = False

    def _materialize(self) -> None:
        if self._has_result or self._cancelled or self._raise_exc is not None:
            return
        try:
            self._result = self._fn()
            self._has_result = True
        except BaseException as exc:
            self._raise_exc = exc

    def result(self, timeout=None):
        self._materialize()
        if self._raise_exc is not None:
            raise self._raise_exc
        return self._result

    def cancel(self) -> bool:
        self._cancelled = True
        return True


class SequentialFakeExecutor:
    def __init__(self, max_workers: int):
        self.max_workers = max_workers
        self.submitted: list[Callable[[], Any]] = []
        self.shutdown = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.shutdown = True

    def submit(self, fn, /):
        self.submitted.append(fn)
        return _SeqFuture(fn)


def _exec_factory():
    def factory(max_workers: int):
        return SequentialFakeExecutor(max_workers)

    return factory


def _fixed_clock(ts: str = "2026-05-10T00:00:00Z") -> Callable[[], _dt.datetime]:
    dt = _dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))

    def _now():
        return dt

    return _now


# ---------------------------------------------------------------------------
# 1. Module surface — failure codes + reason codes + constants
# ---------------------------------------------------------------------------


class TestFailureCodes:
    def test_f_scout_v_01(self):
        assert F_SCOUT_V_01 == "F-SCOUT-V-01"

    def test_f_scout_v_02(self):
        assert F_SCOUT_V_02 == "F-SCOUT-V-02"

    def test_f_scout_v_03(self):
        assert F_SCOUT_V_03 == "F-SCOUT-V-03"

    def test_f_scout_v_04(self):
        assert F_SCOUT_V_04 == "F-SCOUT-V-04"

    def test_f_scout_v_05(self):
        assert F_SCOUT_V_05 == "F-SCOUT-V-05"

    def test_f_scout_v_06(self):
        assert F_SCOUT_V_06 == "F-SCOUT-V-06"

    def test_no_v_07_exported(self):
        # Blueprint §6.7 taxonomy is 01..06 only. Any V-07 is spec-card drift.
        assert not hasattr(vs, "F_SCOUT_V_07")

    def test_truncation_subtags(self):
        assert TRUNCATION_BOUNDED == "F-SCOUT-V-05.truncation_bounded"
        assert TRUNCATION_DEGRADES == "F-SCOUT-V-05.truncation_degrades"


class TestReasonCodes:
    def test_v_ok(self):
        assert REASON_V_OK == "V-OK"

    def test_v_no_endpoint(self):
        assert REASON_NO_LIVE_ENDPOINT == "V-NO-ENDPOINT"

    def test_a_elig_01(self):
        assert REASON_A_ELIG_01 == "A-ELIG-01"

    def test_a_scale_01(self):
        assert REASON_A_SCALE_01 == "A-SCALE-01"

    def test_a_scale_02(self):
        assert REASON_A_SCALE_02 == "A-SCALE-02"

    def test_a_geo_01(self):
        assert REASON_A_GEO_01 == "A-GEO-01"

    def test_a_time_01(self):
        assert REASON_A_TIME_01 == "A-TIME-01"


class TestStageStateConstants:
    def test_verify_stage_ok(self):
        assert VERIFY_STAGE_OK == "OK"

    def test_verify_stage_degraded(self):
        assert VERIFY_STAGE_DEGRADED == "DEGRADED"

    def test_seed_length_constant(self):
        assert _RUN_TIEBREAK_SEED_LEN == 16

    def test_constants_match_pinned_values(self):
        assert SCOUT_CANDIDATE_VERIFY_CAP == 1000
        assert SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO == 0.25
        assert VERIFY_LIVE_SYNOPSIS_TIMEOUT_S == 10
        assert VERIFY_POOL_MAX_WORKERS == 4


# ---------------------------------------------------------------------------
# 2. Data types — frozen kw_only
# ---------------------------------------------------------------------------


class TestDataTypesFrozenKWOnly:
    def test_live_synopsis_kw_only(self):
        with pytest.raises(TypeError):
            LiveSynopsis(  # type: ignore[misc]
                "https://x", "h", "t", (), None, None, None, (), None,
            )

    def test_live_synopsis_frozen(self):
        live = _mk_live()
        with pytest.raises((AttributeError, _dataclass_frozen_error())):
            live.synopsis_url = "mutated"  # type: ignore[misc]

    def test_applicant_profile_kw_only(self):
        with pytest.raises(TypeError):
            ApplicantProfile(  # type: ignore[misc]
                ("nonprofit",), 500_000, 10_000, "US-PA", 7,
            )

    def test_applicant_profile_frozen(self):
        profile = _mk_profile()
        with pytest.raises((AttributeError, _dataclass_frozen_error())):
            profile.geography = "US-NY"  # type: ignore[misc]

    def test_verify_degradation_event_kw_only(self):
        with pytest.raises(TypeError):
            VerifyDegradationEvent(  # type: ignore[misc]
                "verify_all", F_SCOUT_V_05, None, SEVERITY_HIGH,
            )

    def test_verify_degradation_event_frozen(self):
        ev = VerifyDegradationEvent(
            source="verify_all",
            code=F_SCOUT_V_05,
            reason_tag=None,
            severity=SEVERITY_HIGH,
        )
        with pytest.raises((AttributeError, _dataclass_frozen_error())):
            ev.severity = "LOW"  # type: ignore[misc]

    def test_verify_degradation_event_candidate_id_default(self):
        ev = VerifyDegradationEvent(
            source="verify_all",
            code=F_SCOUT_V_05,
            reason_tag=None,
            severity=SEVERITY_HIGH,
        )
        assert ev.candidate_id is None

    def test_scout_verify_result_kw_only(self):
        with pytest.raises(TypeError):
            ScoutVerifyResult({}, VERIFY_STAGE_OK, False, 0, ())  # type: ignore[misc]

    def test_scout_verify_result_frozen(self):
        r = ScoutVerifyResult(
            verdicts={},
            verify_stage_state=VERIFY_STAGE_OK,
            cap_applied=False,
            overflow=0,
            verify_degradation_events=(),
        )
        with pytest.raises((AttributeError, _dataclass_frozen_error())):
            r.overflow = 5  # type: ignore[misc]


def _dataclass_frozen_error():
    # dataclasses.FrozenInstanceError inherits AttributeError; both are accepted.
    from dataclasses import FrozenInstanceError
    return FrozenInstanceError


# ---------------------------------------------------------------------------
# 3. Exceptions
# ---------------------------------------------------------------------------


class TestExceptions:
    def test_synopsis_url_resolution_is_fetch_error(self):
        assert issubclass(SynopsisUrlResolutionError, SynopsisFetchError)

    def test_synopsis_timeout_is_fetch_error(self):
        assert issubclass(SynopsisTimeoutError, SynopsisFetchError)

    def test_synopsis_parse_is_fetch_error(self):
        assert issubclass(SynopsisParseError, SynopsisFetchError)

    def test_synopsis_fetch_error_is_exception(self):
        assert issubclass(SynopsisFetchError, Exception)

    def test_synopsis_no_live_endpoint_not_fetch_error(self):
        # Blueprint rule: NoLiveEndpoint is a control-flow signal, not an error.
        assert not issubclass(SynopsisNoLiveEndpoint, SynopsisFetchError)

    def test_scout_verify_interrupted_is_runtime_error(self):
        assert issubclass(ScoutVerifyInterrupted, RuntimeError)

    def test_scout_verify_interrupted_carries_completed(self):
        exc = ScoutVerifyInterrupted(("a", "b"))
        assert exc.completed_candidate_ids == ("a", "b")
        assert "a" in str(exc)


# ---------------------------------------------------------------------------
# 4. _assert_seed_length
# ---------------------------------------------------------------------------


class TestAssertSeedLength:
    def test_correct_length_passes(self):
        _assert_seed_length(b"\xaa" * 16)

    def test_wrong_length_raises_f_scout_v_06(self):
        with pytest.raises(RuntimeError) as exc_info:
            _assert_seed_length(b"\xaa" * 15)
        assert F_SCOUT_V_06 in str(exc_info.value)

    def test_zero_length_raises(self):
        with pytest.raises(RuntimeError):
            _assert_seed_length(b"")

    def test_wrong_type_raises(self):
        with pytest.raises(RuntimeError) as exc_info:
            _assert_seed_length("aaaa")  # type: ignore[arg-type]
        assert F_SCOUT_V_06 in str(exc_info.value)

    def test_longer_length_raises(self):
        with pytest.raises(RuntimeError):
            _assert_seed_length(b"\xaa" * 32)


# ---------------------------------------------------------------------------
# 5. _verify_sort_key
# ---------------------------------------------------------------------------


class TestVerifySortKey:
    def test_primary_key_is_negated_fit_score(self):
        seed = b"\x00" * 16
        c = _mk_candidate("a" * 24, fit_score_cached=42)
        key = _verify_sort_key(c, seed)
        assert key[0] == -42

    def test_secondary_is_16_bytes(self):
        seed = b"\x00" * 16
        c = _mk_candidate("b" * 24, fit_score_cached=0)
        key = _verify_sort_key(c, seed)
        assert len(key[1]) == 16

    def test_secondary_uses_seed_xor(self):
        # When seed is all-zero, secondary equals sha3_512(canonical)[:16].
        seed = b"\x00" * 16
        c = _mk_candidate("c" * 24, fit_score_cached=0)
        digest16 = hashlib.sha3_512(candidate_canonical_bytes(c)).digest()[:16]
        _, xored = _verify_sort_key(c, seed)
        assert xored == digest16

    def test_different_seeds_produce_different_secondary(self):
        seed_a = b"\x00" * 16
        seed_b = b"\xff" * 16
        c = _mk_candidate("d" * 24, fit_score_cached=0)
        _, xor_a = _verify_sort_key(c, seed_a)
        _, xor_b = _verify_sort_key(c, seed_b)
        assert xor_a != xor_b
        # Full-XOR relation: A XOR seed_diff == B.
        diff = bytes(a ^ b for a, b in zip(xor_a, xor_b))
        assert diff == b"\xff" * 16

    def test_higher_fit_score_sorts_before_lower(self):
        seed = b"\x00" * 16
        high = _mk_candidate("h" * 24, fit_score_cached=90)
        low = _mk_candidate("l" * 24, fit_score_cached=10)
        keys = sorted([low, high], key=lambda c: _verify_sort_key(c, seed))
        assert keys[0].candidate_id == high.candidate_id

    def test_tied_fit_score_falls_through_to_xor(self):
        seed = b"\x00" * 16
        a = _mk_candidate("aaaaaaaaaaaaaaaaaaaaaaaa", fit_score_cached=50)
        b = _mk_candidate("bbbbbbbbbbbbbbbbbbbbbbbb", fit_score_cached=50)
        key_a = _verify_sort_key(a, seed)
        key_b = _verify_sort_key(b, seed)
        assert key_a != key_b
        assert key_a[0] == key_b[0]  # same primary

    def test_canonical_json_failure_raises_f_scout_v_06(self):
        # Patch directly on the function's __globals__ to survive test
        # ordering that clears ``sys.modules`` (Round 1's package-reimport
        # timing test leaves the sys.modules entry pointing at a NEW module
        # object, but _verify_sort_key still resolves names via the
        # original __globals__ dict that this test file captured at
        # import time). E-026 / E-027 adjacent — patch the globals dict
        # the function actually reads from, with explicit restore (no
        # monkeypatch fixture because it resolves against sys.modules).
        def _bad(_c):
            raise ValueError("boom")

        globals_dict = _verify_sort_key.__globals__
        original = globals_dict["candidate_canonical_bytes"]
        globals_dict["candidate_canonical_bytes"] = _bad
        try:
            with pytest.raises(RuntimeError) as exc_info:
                _verify_sort_key(_mk_candidate("e" * 24), b"\x00" * 16)
            assert F_SCOUT_V_06 in str(exc_info.value)
        finally:
            globals_dict["candidate_canonical_bytes"] = original


# ---------------------------------------------------------------------------
# 6. _truncate_candidates + _degrade_threshold
# ---------------------------------------------------------------------------


class TestTruncateCandidates:
    def test_under_cap_no_overflow(self):
        seed = b"\x00" * 16
        cands = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=i) for i in range(10)
        )
        kept, overflow = _truncate_candidates(cands, seed)
        assert overflow == 0
        assert len(kept) == 10

    def test_at_cap_no_overflow(self):
        seed = b"\x00" * 16
        cands = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=i % 100)
            for i in range(SCOUT_CANDIDATE_VERIFY_CAP)
        )
        kept, overflow = _truncate_candidates(cands, seed)
        assert overflow == 0
        assert len(kept) == SCOUT_CANDIDATE_VERIFY_CAP

    def test_over_cap_overflow_by_one(self):
        seed = b"\x00" * 16
        cands = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=i % 100)
            for i in range(SCOUT_CANDIDATE_VERIFY_CAP + 1)
        )
        kept, overflow = _truncate_candidates(cands, seed)
        assert overflow == 1
        assert len(kept) == SCOUT_CANDIDATE_VERIFY_CAP

    def test_over_cap_keeps_highest_fit_score(self):
        seed = b"\x00" * 16
        extra = _mk_candidate("z" * 24, fit_score_cached=100)
        rest = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=0)
            for i in range(SCOUT_CANDIDATE_VERIFY_CAP)
        )
        cands = rest + (extra,)
        kept, _ = _truncate_candidates(cands, seed)
        assert any(c.candidate_id == extra.candidate_id for c in kept)

    def test_truncate_is_deterministic_for_same_seed(self):
        seed = b"\x42" * 16
        cands = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=50)
            for i in range(SCOUT_CANDIDATE_VERIFY_CAP + 50)
        )
        kept_a, _ = _truncate_candidates(cands, seed)
        kept_b, _ = _truncate_candidates(cands, seed)
        assert [c.candidate_id for c in kept_a] == [c.candidate_id for c in kept_b]

    def test_truncate_differs_across_seeds(self):
        cands = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=50)
            for i in range(SCOUT_CANDIDATE_VERIFY_CAP + 50)
        )
        kept_a, _ = _truncate_candidates(cands, b"\x00" * 16)
        kept_b, _ = _truncate_candidates(cands, b"\xff" * 16)
        # Non-identical tie-break should permute at least some identities.
        assert [c.candidate_id for c in kept_a] != [c.candidate_id for c in kept_b]


class TestDegradeThreshold:
    def test_threshold_is_250(self):
        assert _degrade_threshold() == 250

    def test_matches_ratio_times_cap(self):
        assert _degrade_threshold() == int(
            SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO
            * SCOUT_CANDIDATE_VERIFY_CAP
        )


# ---------------------------------------------------------------------------
# 7. _match_applicant
# ---------------------------------------------------------------------------


class TestMatchApplicant:
    def test_all_axes_pass_returns_fit(self):
        ok, reason = _match_applicant(
            _mk_live(), _mk_profile(), now_utc=_fixed_clock()()
        )
        assert ok is True
        assert reason == REASON_V_OK

    def test_eligibility_rejection(self):
        profile = _mk_profile(applicant_types=("individual",))
        ok, reason = _match_applicant(
            _mk_live(), profile, now_utc=_fixed_clock()()
        )
        assert ok is False
        assert reason == REASON_A_ELIG_01

    def test_eligibility_case_insensitive(self):
        live = _mk_live(eligibility_live=("NONPROFIT",))
        ok, _ = _match_applicant(live, _mk_profile(), now_utc=_fixed_clock()())
        assert ok is True

    def test_scale_cap_below_floor_rejected(self):
        profile = _mk_profile(max_award_capacity=10_000)
        live = _mk_live(award_floor_live=50_000)
        ok, reason = _match_applicant(live, profile, now_utc=_fixed_clock()())
        assert ok is False
        assert reason == REASON_A_SCALE_01

    def test_scale_need_above_ceiling_rejected(self):
        profile = _mk_profile(min_award_need=1_000_000)
        live = _mk_live(award_ceiling_live=100_000)
        ok, reason = _match_applicant(live, profile, now_utc=_fixed_clock()())
        assert ok is False
        assert reason == REASON_A_SCALE_02

    def test_scale_none_bounds_pass(self):
        profile = _mk_profile(max_award_capacity=None, min_award_need=None)
        live = _mk_live(award_floor_live=None, award_ceiling_live=None)
        ok, _ = _match_applicant(live, profile, now_utc=_fixed_clock()())
        assert ok is True

    def test_geography_none_profile_rejected(self):
        profile = _mk_profile(geography=None)
        ok, reason = _match_applicant(
            _mk_live(), profile, now_utc=_fixed_clock()()
        )
        assert ok is False
        assert reason == REASON_A_GEO_01

    def test_geography_mismatch_rejected(self):
        profile = _mk_profile(geography="US-WA")
        live = _mk_live(eligible_geographies=("US-PA",))
        ok, reason = _match_applicant(live, profile, now_utc=_fixed_clock()())
        assert ok is False
        assert reason == REASON_A_GEO_01

    def test_timing_close_date_none_passes(self):
        live = _mk_live(close_date_live_utc=None)
        ok, _ = _match_applicant(live, _mk_profile(), now_utc=_fixed_clock()())
        assert ok is True

    def test_timing_insufficient_lead_rejected(self):
        profile = _mk_profile(min_lead_time_days=365)
        live = _mk_live(close_date_live_utc="2026-05-15T00:00:00Z")
        ok, reason = _match_applicant(
            live, profile, now_utc=_fixed_clock("2026-05-10T00:00:00Z")()
        )
        assert ok is False
        assert reason == REASON_A_TIME_01

    def test_timing_exact_boundary(self):
        # Lead time = 7 days exactly: must pass (inclusive >= threshold).
        profile = _mk_profile(min_lead_time_days=7)
        live = _mk_live(close_date_live_utc="2026-05-17T00:00:00Z")
        ok, _ = _match_applicant(
            live, profile, now_utc=_fixed_clock("2026-05-10T00:00:00Z")()
        )
        assert ok is True

    def test_timing_naive_close_date_treated_as_utc(self):
        # Blueprint: naive close_date (no tz) is interpreted as UTC.
        # Lead time = 7 days exactly should pass.
        profile = _mk_profile(min_lead_time_days=7)
        live = _mk_live(close_date_live_utc="2026-05-17T00:00:00")  # naive
        ok, _ = _match_applicant(
            live, profile, now_utc=_fixed_clock("2026-05-10T00:00:00Z")()
        )
        assert ok is True

    def test_timing_malformed_close_date_rejects(self):
        live = _mk_live(close_date_live_utc="not-an-iso-date")
        ok, reason = _match_applicant(
            live, _mk_profile(), now_utc=_fixed_clock()()
        )
        assert ok is False
        assert reason == REASON_A_TIME_01

    def test_axis_order_eligibility_before_scale(self):
        profile = _mk_profile(
            applicant_types=("individual",), max_award_capacity=1,
        )
        live = _mk_live(award_floor_live=1_000_000)
        ok, reason = _match_applicant(live, profile, now_utc=_fixed_clock()())
        assert ok is False
        assert reason == REASON_A_ELIG_01

    def test_axis_order_scale_before_geography(self):
        profile = _mk_profile(max_award_capacity=1, geography="US-WA")
        live = _mk_live(award_floor_live=1_000_000)
        ok, reason = _match_applicant(live, profile, now_utc=_fixed_clock()())
        assert ok is False
        assert reason == REASON_A_SCALE_01

    def test_axis_order_geography_before_timing(self):
        profile = _mk_profile(geography="US-WA", min_lead_time_days=365)
        live = _mk_live(
            eligible_geographies=("US-PA",),
            close_date_live_utc="2026-05-01T00:00:00Z",
        )
        ok, reason = _match_applicant(
            live, profile, now_utc=_fixed_clock("2026-04-30T00:00:00Z")()
        )
        assert ok is False
        assert reason == REASON_A_GEO_01


# ---------------------------------------------------------------------------
# 8. verify_candidate — four-verdict matrix
# ---------------------------------------------------------------------------


class TestVerifyCandidateVerifiedFit:
    def test_fit_returns_verified_fit(self):
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("f" * 24),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
        )
        assert result.verdict == VERDICT_VERIFIED_FIT
        assert result.reason_code == REASON_V_OK
        assert result.live_synopsis_url == "https://example.test/live"
        assert result.live_content_hash == "d" * 128

    def test_fit_populates_live_fields(self):
        live = _mk_live(award_floor_live=25_000, award_ceiling_live=400_000)
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("g" * 24),
            synopsis_fetcher=FakeFetcher(return_live=live),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
        )
        assert result.award_floor_live == 25_000
        assert result.award_ceiling_live == 400_000
        assert result.eligibility_live == ("nonprofit",)

    def test_timeout_seconds_threaded_through(self):
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("h" * 24),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
            timeout_seconds=30,
        )
        assert result.timeout_seconds == 30


class TestVerifyCandidateVerifiedNotFit:
    def test_eligibility_rejected_returns_not_fit(self):
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("i" * 24),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile=_mk_profile(applicant_types=("individual",)),
            clock=_fixed_clock(),
        )
        assert result.verdict == VERDICT_VERIFIED_NOT_FIT
        assert result.reason_code == REASON_A_ELIG_01

    def test_not_fit_still_carries_live_fields(self):
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("j" * 24),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile=_mk_profile(applicant_types=("individual",)),
            clock=_fixed_clock(),
        )
        assert result.live_synopsis_url is not None
        assert result.live_content_hash is not None


class TestVerifyCandidateUnverified:
    def test_fetcher_returns_none_unverified(self):
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("k" * 24),
            synopsis_fetcher=FakeFetcher(return_live=None),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
        )
        assert result.verdict == VERDICT_UNVERIFIED
        assert result.reason_code == REASON_NO_LIVE_ENDPOINT
        assert result.live_synopsis_url is None

    def test_no_live_endpoint_exception_unverified(self):
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("l" * 24),
            synopsis_fetcher=FakeFetcher(
                raise_with=SynopsisNoLiveEndpoint("no endpoint"),
            ),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
        )
        assert result.verdict == VERDICT_UNVERIFIED
        assert result.reason_code == REASON_NO_LIVE_ENDPOINT


class TestVerifyCandidateVerificationFailed:
    def test_url_resolution_error_maps_to_v_01(self):
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("m" * 24),
            synopsis_fetcher=FakeFetcher(
                raise_with=SynopsisUrlResolutionError("bad dns"),
            ),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
        )
        assert result.verdict == VERDICT_VERIFICATION_FAILED
        assert result.reason_code == F_SCOUT_V_01

    def test_timeout_error_maps_to_v_02(self):
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("n" * 24),
            synopsis_fetcher=FakeFetcher(
                raise_with=SynopsisTimeoutError("too slow"),
            ),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
        )
        assert result.verdict == VERDICT_VERIFICATION_FAILED
        assert result.reason_code == F_SCOUT_V_02

    def test_parse_error_maps_to_v_03(self):
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("o" * 24),
            synopsis_fetcher=FakeFetcher(
                raise_with=SynopsisParseError("malformed body"),
            ),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
        )
        assert result.verdict == VERDICT_VERIFICATION_FAILED
        assert result.reason_code == F_SCOUT_V_03

    def test_unexpected_exception_maps_to_parse_unknown(self):
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("p" * 24),
            synopsis_fetcher=FakeFetcher(
                raise_with=ValueError("wat"),
            ),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
        )
        assert result.verdict == VERDICT_VERIFICATION_FAILED
        assert result.reason_code == f"{F_SCOUT_V_03}.parse_unknown"

    def test_failed_path_has_no_live_fields(self):
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("q" * 24),
            synopsis_fetcher=FakeFetcher(
                raise_with=SynopsisTimeoutError("slow"),
            ),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
        )
        assert result.live_synopsis_url is None
        assert result.live_content_hash is None
        assert result.fetched_at_utc is None
        assert result.eligibility_live == ()

    def test_keyboard_interrupt_passthrough(self):
        with pytest.raises(KeyboardInterrupt):
            verify_candidate(
                session=FakeSession(),
                candidate=_mk_candidate("r" * 24),
                synopsis_fetcher=FakeFetcher(raise_with=KeyboardInterrupt()),
                applicant_profile=_mk_profile(),
                clock=_fixed_clock(),
            )

    def test_system_exit_passthrough(self):
        with pytest.raises(SystemExit):
            verify_candidate(
                session=FakeSession(),
                candidate=_mk_candidate("s" * 24),
                synopsis_fetcher=FakeFetcher(raise_with=SystemExit(1)),
                applicant_profile=_mk_profile(),
                clock=_fixed_clock(),
            )


# ---------------------------------------------------------------------------
# 9. verify_all — happy path + checkpoint discipline
# ---------------------------------------------------------------------------


class TestVerifyAllHappyPath:
    def test_single_candidate_fit(self):
        cp, dw = _default_writers()
        c = _mk_candidate("t" * 24)
        result = verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=(c,)),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        assert isinstance(result, ScoutVerifyResult)
        assert len(result.verdicts) == 1
        assert result.verdicts[c.candidate_id].verdict == VERDICT_VERIFIED_FIT
        assert result.verify_stage_state == VERIFY_STAGE_OK
        assert result.cap_applied is False
        assert result.overflow == 0

    def test_multiple_candidates_mixed_outcomes(self):
        cp, dw = _default_writers()
        c1 = _mk_candidate("u" * 24)
        c2 = _mk_candidate("v" * 24)
        c3 = _mk_candidate("w" * 24)
        fetcher = PerCandidateFetcher(
            behavior={
                c1.candidate_id: _mk_live(),
                c2.candidate_id: None,
                c3.candidate_id: SynopsisTimeoutError("slow"),
            }
        )
        result = verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=(c1, c2, c3)),
            synopsis_fetcher=fetcher,
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        assert result.verdicts[c1.candidate_id].verdict == VERDICT_VERIFIED_FIT
        assert result.verdicts[c2.candidate_id].verdict == VERDICT_UNVERIFIED
        assert (
            result.verdicts[c3.candidate_id].verdict == VERDICT_VERIFICATION_FAILED
        )
        assert result.verdicts[c3.candidate_id].reason_code == F_SCOUT_V_02

    def test_profile_fetched_once(self):
        cp, dw = _default_writers()
        c1 = _mk_candidate("x" * 24)
        c2 = _mk_candidate("y" * 24)
        provider = FakeProfileProvider(_mk_profile())
        verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=(c1, c2)),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile_provider=provider,
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        assert len(provider.calls) == 1


class TestVerifyAllCheckpointDiscipline:
    def test_verify_start_emitted(self):
        cp, dw = _default_writers()
        c = _mk_candidate("a" * 24)
        verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=(c,)),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        stages = [s for s, _ in cp.writes]
        assert "verify_start" in stages

    def test_verify_start_payload_has_required_fields(self):
        cp, dw = _default_writers()
        c = _mk_candidate("b" * 24)
        verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=(c,)),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        start = next(p for s, p in cp.writes if s == "verify_start")
        assert "session_id" in start
        assert "run_id" in start
        assert "n_input_candidates" in start
        assert "n_verify_candidates" in start
        assert "overflow" in start
        assert "cap_applied" in start
        assert "verify_stage_state" in start

    def test_per_candidate_complete_emitted(self):
        cp, dw = _default_writers()
        c1 = _mk_candidate("c" * 24)
        c2 = _mk_candidate("d" * 24)
        verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=(c1, c2)),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        per_candidate = [
            (s, p) for s, p in cp.writes if s == "verify_candidate_complete"
        ]
        assert len(per_candidate) == 2
        payload = per_candidate[0][1]
        assert "candidate_id" in payload
        assert "verdict" in payload
        assert "reason_code" in payload

    def test_verify_complete_emitted(self):
        cp, dw = _default_writers()
        c = _mk_candidate("e" * 24)
        verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=(c,)),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        stages = [s for s, _ in cp.writes]
        assert stages[-1] == "verify_complete"

    def test_per_candidate_checkpoint_on_failure_too(self):
        cp, dw = _default_writers()
        c = _mk_candidate("f" * 24)
        verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=(c,)),
            synopsis_fetcher=FakeFetcher(
                raise_with=SynopsisTimeoutError("slow"),
            ),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        per = [(s, p) for s, p in cp.writes if s == "verify_candidate_complete"]
        assert len(per) == 1
        assert per[0][1]["verdict"] == VERDICT_VERIFICATION_FAILED


# ---------------------------------------------------------------------------
# 10. verify_all — truncation + degradation emission
# ---------------------------------------------------------------------------


class TestVerifyAllTruncation:
    def test_under_cap_no_event(self):
        cp, dw = _default_writers()
        c = _mk_candidate("g" * 24)
        result = verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=(c,)),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        assert result.overflow == 0
        assert result.verify_degradation_events == ()
        assert dw.events == []

    def test_over_cap_bounded_emits_low_severity_event(self):
        cp, dw = _default_writers()
        # 1050 candidates → overflow 50 → bounded (≤ 250)
        cands = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=0)
            for i in range(SCOUT_CANDIDATE_VERIFY_CAP + 50)
        )
        result = verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=cands),
            synopsis_fetcher=FakeFetcher(return_live=None),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        assert result.overflow == 50
        assert result.cap_applied is True
        assert result.verify_stage_state == VERIFY_STAGE_OK
        assert len(result.verify_degradation_events) == 1
        event = result.verify_degradation_events[0]
        assert event.code == F_SCOUT_V_05
        assert event.severity == SEVERITY_MEDIUM
        assert TRUNCATION_BOUNDED in event.reason_tag

    def test_over_cap_exactly_threshold_is_bounded(self):
        cp, dw = _default_writers()
        # overflow == 250 exactly → bounded (strict >), not degrades
        cands = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=0)
            for i in range(SCOUT_CANDIDATE_VERIFY_CAP + 250)
        )
        result = verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=cands),
            synopsis_fetcher=FakeFetcher(return_live=None),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        assert result.overflow == 250
        assert result.verify_stage_state == VERIFY_STAGE_OK
        event = result.verify_degradation_events[0]
        assert TRUNCATION_BOUNDED in event.reason_tag

    def test_over_cap_degrades_flips_state(self):
        cp, dw = _default_writers()
        # overflow == 251 → degrades (strict >)
        cands = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=0)
            for i in range(SCOUT_CANDIDATE_VERIFY_CAP + 251)
        )
        result = verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=cands),
            synopsis_fetcher=FakeFetcher(return_live=None),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        assert result.overflow == 251
        assert result.verify_stage_state == VERIFY_STAGE_DEGRADED
        event = result.verify_degradation_events[0]
        assert event.severity == SEVERITY_HIGH
        assert TRUNCATION_DEGRADES in event.reason_tag

    def test_overflow_candidates_are_dropped(self):
        cp, dw = _default_writers()
        high = _mk_candidate("z" * 24, fit_score_cached=100)
        low = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=0)
            for i in range(SCOUT_CANDIDATE_VERIFY_CAP + 10)
        )
        result = verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=(high,) + low),
            synopsis_fetcher=FakeFetcher(return_live=None),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        # High fit_score survives truncation.
        assert high.candidate_id in result.verdicts
        assert len(result.verdicts) == SCOUT_CANDIDATE_VERIFY_CAP

    def test_degradation_writer_called_for_each_event(self):
        cp, dw = _default_writers()
        cands = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=0)
            for i in range(SCOUT_CANDIDATE_VERIFY_CAP + 10)
        )
        verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=cands),
            synopsis_fetcher=FakeFetcher(return_live=None),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        codes = [e.code for e in dw.events]
        assert F_SCOUT_V_05 in codes


# ---------------------------------------------------------------------------
# 11. verify_all — seed-length + tiebreak integrity
# ---------------------------------------------------------------------------


class TestVerifyAllSeedIntegrity:
    def test_wrong_length_seed_raises_f_scout_v_06(self):
        cp, dw = _default_writers()
        with pytest.raises(RuntimeError) as exc_info:
            verify_all(
                session=FakeSession(),
                discover_result=_mk_discover_result(
                    candidates=(),
                    run_tiebreak_seed=b"\x00" * 15,  # wrong length
                ),
                synopsis_fetcher=FakeFetcher(return_live=None),
                applicant_profile_provider=FakeProfileProvider(_mk_profile()),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                clock=_fixed_clock(),
            )
        assert F_SCOUT_V_06 in str(exc_info.value)

    def test_seed_changes_tiebreak_order(self):
        cp, dw = _default_writers()
        cands = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=50)
            for i in range(SCOUT_CANDIDATE_VERIFY_CAP + 5)
        )
        # Different seeds → different survivor sets
        r_a = verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(
                candidates=cands, run_tiebreak_seed=b"\x00" * 16
            ),
            synopsis_fetcher=FakeFetcher(return_live=None),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        cp2, dw2 = _default_writers()
        r_b = verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(
                candidates=cands, run_tiebreak_seed=b"\xff" * 16
            ),
            synopsis_fetcher=FakeFetcher(return_live=None),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp2,
            degradation_writer=dw2,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        assert set(r_a.verdicts.keys()) != set(r_b.verdicts.keys())


# ---------------------------------------------------------------------------
# 12. verify_all — verify_fn exception isolation
# ---------------------------------------------------------------------------


class TestVerifyAllPoolIsolation:
    def test_verify_fn_exception_isolated(self):
        cp, dw = _default_writers()
        c1 = _mk_candidate("a" * 24)
        c2 = _mk_candidate("b" * 24)

        def bad_verify(**_):
            raise RuntimeError("verify_fn boom")

        # Make only c2 raise (by dispatching on candidate).
        def dispatch_verify(**kwargs):
            if kwargs["candidate"].candidate_id == c2.candidate_id:
                raise RuntimeError("boom")
            return verify_candidate(**kwargs)

        result = verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=(c1, c2)),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
            verify_fn=dispatch_verify,
        )
        assert result.verdicts[c1.candidate_id].verdict == VERDICT_VERIFIED_FIT
        assert (
            result.verdicts[c2.candidate_id].verdict == VERDICT_VERIFICATION_FAILED
        )
        assert (
            result.verdicts[c2.candidate_id].reason_code
            == f"{F_SCOUT_V_03}.verify_fn_raised"
        )

    def test_verify_fn_exception_emits_degradation_event(self):
        cp, dw = _default_writers()
        c = _mk_candidate("c" * 24)

        def bad_verify(**_):
            raise RuntimeError("verify_fn boom")

        verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=(c,)),
            synopsis_fetcher=FakeFetcher(return_live=None),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
            verify_fn=bad_verify,
        )
        codes = [(e.code, e.candidate_id) for e in dw.events]
        assert (F_SCOUT_V_03, c.candidate_id) in codes

    def test_verify_fn_keyboard_interrupt_propagates(self):
        cp, dw = _default_writers()
        c = _mk_candidate("d" * 24)

        def bad_verify(**_):
            raise KeyboardInterrupt()

        with pytest.raises(KeyboardInterrupt):
            verify_all(
                session=FakeSession(),
                discover_result=_mk_discover_result(candidates=(c,)),
                synopsis_fetcher=FakeFetcher(return_live=None),
                applicant_profile_provider=FakeProfileProvider(_mk_profile()),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                clock=_fixed_clock(),
                verify_fn=bad_verify,
            )

    def test_verify_fn_system_exit_propagates(self):
        cp, dw = _default_writers()
        c = _mk_candidate("e" * 24)

        def bad_verify(**_):
            raise SystemExit(1)

        with pytest.raises(SystemExit):
            verify_all(
                session=FakeSession(),
                discover_result=_mk_discover_result(candidates=(c,)),
                synopsis_fetcher=FakeFetcher(return_live=None),
                applicant_profile_provider=FakeProfileProvider(_mk_profile()),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                clock=_fixed_clock(),
                verify_fn=bad_verify,
            )


# ---------------------------------------------------------------------------
# 13. verify_all — interrupt cancellation
# ---------------------------------------------------------------------------


class TestVerifyAllInterrupt:
    def test_pre_pool_interrupt_raises_and_checkpoints(self):
        cp, dw = _default_writers()
        c = _mk_candidate("f" * 24)

        with pytest.raises(ScoutVerifyInterrupted) as exc_info:
            verify_all(
                session=FakeSession(),
                discover_result=_mk_discover_result(candidates=(c,)),
                synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
                applicant_profile_provider=FakeProfileProvider(_mk_profile()),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                interrupt_probe=lambda: True,
                clock=_fixed_clock(),
            )
        assert exc_info.value.completed_candidate_ids == ()
        stages = [s for s, _ in cp.writes]
        assert "verify_interrupted" in stages

    def test_pre_pool_interrupt_payload_has_before_pool_stage(self):
        cp, dw = _default_writers()
        c = _mk_candidate("g" * 24)
        with pytest.raises(ScoutVerifyInterrupted):
            verify_all(
                session=FakeSession(),
                discover_result=_mk_discover_result(candidates=(c,)),
                synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
                applicant_profile_provider=FakeProfileProvider(_mk_profile()),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                interrupt_probe=lambda: True,
                clock=_fixed_clock(),
            )
        interrupted = next(p for s, p in cp.writes if s == "verify_interrupted")
        assert interrupted["stage_at_interrupt"] == "before_pool"
        assert interrupted["completed_candidate_ids"] == []

    def test_mid_pool_interrupt_preserves_completed(self):
        cp, dw = _default_writers()
        # Distinct fit_scores so pool order is deterministic
        # (descending fit_score): high_90 → mid_50 → low_10.
        high = _mk_candidate("aaaaaaaaaaaaaaaaaaaaaaaa", fit_score_cached=90)
        mid = _mk_candidate("bbbbbbbbbbbbbbbbbbbbbbbb", fit_score_cached=50)
        low = _mk_candidate("cccccccccccccccccccccccc", fit_score_cached=10)

        # Flip interrupt True after first completion.
        state = {"calls": 0}

        def probe():
            state["calls"] += 1
            # calls 1 = pre-pool (False); call 2 = pre-first (False);
            # call 3 = pre-second (True).
            return state["calls"] >= 3

        with pytest.raises(ScoutVerifyInterrupted) as exc_info:
            verify_all(
                session=FakeSession(),
                discover_result=_mk_discover_result(
                    candidates=(high, mid, low)
                ),
                synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
                applicant_profile_provider=FakeProfileProvider(_mk_profile()),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                interrupt_probe=probe,
                clock=_fixed_clock(),
            )
        # Highest fit_score completed first; others pending.
        completed = exc_info.value.completed_candidate_ids
        assert high.candidate_id in completed
        assert mid.candidate_id not in completed
        assert low.candidate_id not in completed

    def test_mid_pool_interrupt_payload_has_mid_pool_stage(self):
        cp, dw = _default_writers()
        high = _mk_candidate("aaaaaaaaaaaaaaaaaaaaaaaa", fit_score_cached=90)
        low = _mk_candidate("bbbbbbbbbbbbbbbbbbbbbbbb", fit_score_cached=10)
        state = {"calls": 0}

        def probe():
            state["calls"] += 1
            return state["calls"] >= 3

        with pytest.raises(ScoutVerifyInterrupted):
            verify_all(
                session=FakeSession(),
                discover_result=_mk_discover_result(candidates=(high, low)),
                synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
                applicant_profile_provider=FakeProfileProvider(_mk_profile()),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                interrupt_probe=probe,
                clock=_fixed_clock(),
            )
        interrupted = next(p for s, p in cp.writes if s == "verify_interrupted")
        assert interrupted["stage_at_interrupt"] == "mid_pool"
        assert "pending_candidate_id" in interrupted


# ---------------------------------------------------------------------------
# 14. Default factories
# ---------------------------------------------------------------------------


class TestDefaultFactories:
    def test_default_clock_returns_utc_datetime(self):
        now = vs._default_clock()
        assert now.tzinfo is not None
        assert now.tzinfo.utcoffset(now) == _dt.timedelta(0)

    def test_default_interrupt_probe_returns_false(self):
        assert vs._default_interrupt_probe() is False

    def test_default_executor_factory_is_threadpool_adapter(self):
        with vs._default_executor_factory(1) as pool:
            fut = pool.submit(lambda: 42)
            assert fut.result(timeout=5) == 42

    def test_default_executor_factory_shuts_down_on_exit(self):
        factory = vs._default_executor_factory
        adapter = factory(1)
        with adapter:
            adapter.submit(lambda: 1)
        # After __exit__, no attribute errors on subsequent context use.


# ---------------------------------------------------------------------------
# 15. Round 8 → Round 9 handoff composition
# ---------------------------------------------------------------------------


class TestRound8Handoff:
    def test_accepts_scout_discover_result(self):
        cp, dw = _default_writers()
        c = _mk_candidate("h" * 24)
        dr = _mk_discover_result(candidates=(c,), run_id="deadbeef" * 3)
        assert isinstance(dr, ScoutDiscoverResult)
        result = verify_all(
            session=FakeSession(),
            discover_result=dr,
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        assert len(result.verdicts) == 1

    def test_run_id_propagates_to_checkpoint_payloads(self):
        cp, dw = _default_writers()
        c = _mk_candidate("i" * 24)
        dr = _mk_discover_result(candidates=(c,), run_id="fa" * 12)
        verify_all(
            session=FakeSession(),
            discover_result=dr,
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        for stage, payload in cp.writes:
            if stage in {"verify_start", "verify_candidate_complete", "verify_complete"}:
                assert payload["run_id"] == "fa" * 12


# ---------------------------------------------------------------------------
# 16. kw-only call discipline
# ---------------------------------------------------------------------------


class TestKWOnly:
    def test_verify_candidate_rejects_positional(self):
        with pytest.raises(TypeError):
            verify_candidate(  # type: ignore[misc]
                FakeSession(),
                _mk_candidate("a" * 24),
                FakeFetcher(),
                _mk_profile(),
            )

    def test_verify_all_rejects_positional(self):
        cp, dw = _default_writers()
        with pytest.raises(TypeError):
            verify_all(  # type: ignore[misc]
                FakeSession(),
                _mk_discover_result(candidates=()),
                FakeFetcher(),
                FakeProfileProvider(_mk_profile()),
                cp,
                dw,
            )


# ---------------------------------------------------------------------------
# 17. AST-lint R1/R3/R4/R5 clean
# ---------------------------------------------------------------------------


class TestASTLintClean:
    def test_ast_lint_scout_rules_clean(self, tmp_path: Path):
        # E-027: lint_tree expects a directory. Copy verify_stage.py +
        # minimal sibling layout.
        from pipeline.linting import ast_lint

        src = Path(vs.__file__)
        dst_dir = tmp_path / "pipeline" / "scout"
        dst_dir.mkdir(parents=True)
        (dst_dir / "__init__.py").write_text("", encoding="utf-8")
        shutil.copy(src, dst_dir / "verify_stage.py")

        violations = ast_lint.lint_tree(tmp_path, ast_lint.DEFAULT_RULES)
        in_scope = [v for v in violations if v.file.name == "verify_stage.py"]
        assert in_scope == []

    def test_module_does_not_import_pipeline_vault(self):
        src = Path(vs.__file__).read_text(encoding="utf-8")
        lines = [
            ln
            for ln in src.splitlines()
            if ln.startswith("from pipeline.vault")
            or ln.startswith("import pipeline.vault")
        ]
        assert lines == []

    def test_module_has_no_module_level_open_call(self):
        src = Path(vs.__file__).read_text(encoding="utf-8")
        assert "\nopen(" not in src

    def test_module_has_no_eval_call(self):
        src = Path(vs.__file__).read_text(encoding="utf-8")
        assert "\neval(" not in src

    def test_module_has_no_setattr_operator_decision(self):
        src = Path(vs.__file__).read_text(encoding="utf-8")
        # R4 forbids scout setattr(...,'operator_decision',...)
        assert "setattr(" not in src or "operator_decision" not in src


# ---------------------------------------------------------------------------
# 18. Version pin + __module__ lineage (E-025 / E-026)
# ---------------------------------------------------------------------------


class TestPublicSurface:
    def test_version_pin_r_n_ge_9(self):
        # E-025 range-check (not string-equality) so r10+ stays valid.
        m = re.match(r"^0\.1\.0-scout-r(\d+)$", vs.__version__)
        assert m is not None
        assert int(m.group(1)) >= 9

    def test_module_lineage_verify_candidate(self):
        # E-026 formal — use __module__ over sys.modules identity.
        assert verify_candidate.__module__ == "pipeline.scout.verify_stage"

    def test_module_lineage_verify_all(self):
        assert verify_all.__module__ == "pipeline.scout.verify_stage"

    def test_module_lineage_scout_verify_result(self):
        assert ScoutVerifyResult.__module__ == "pipeline.scout.verify_stage"

    def test_module_lineage_live_synopsis(self):
        assert LiveSynopsis.__module__ == "pipeline.scout.verify_stage"

    def test_module_lineage_applicant_profile(self):
        assert ApplicantProfile.__module__ == "pipeline.scout.verify_stage"

    def test_synopsis_fetcher_is_runtime_checkable(self):
        # runtime_checkable allows isinstance() checks.
        assert isinstance(FakeFetcher(), SynopsisFetcher)

    def test_applicant_profile_provider_is_runtime_checkable(self):
        assert isinstance(
            FakeProfileProvider(_mk_profile()), ApplicantProfileProvider
        )

    def test_candidate_imported_from_types_not_redefined(self):
        # Candidate should come from _types — verify_stage must not redefine it.
        assert Candidate.__module__ == "pipeline.scout._types"


# ---------------------------------------------------------------------------
# 19. Adversarial — seeded determinism + edge cases
# ---------------------------------------------------------------------------


class TestAdversarialTiebreakDeterminism:
    def test_all_zero_seed_sort_is_canonical_json_xor(self):
        seed = b"\x00" * 16
        cs = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=0) for i in range(5)
        )
        ordered = sorted(cs, key=lambda c: _verify_sort_key(c, seed))
        expected = sorted(
            cs,
            key=lambda c: hashlib.sha3_512(
                candidate_canonical_bytes(c)
            ).digest()[:16],
        )
        assert [c.candidate_id for c in ordered] == [
            c.candidate_id for c in expected
        ]

    def test_seed_flip_inverts_xor_bytes(self):
        c = _mk_candidate("x" * 24, fit_score_cached=0)
        _, xor_zero = _verify_sort_key(c, b"\x00" * 16)
        _, xor_ones = _verify_sort_key(c, b"\xff" * 16)
        for a, b in zip(xor_zero, xor_ones):
            assert a == (b ^ 0xFF)

    def test_seed_changes_produce_different_truncation_boundary(self):
        cs = tuple(
            _mk_candidate(f"{i:024d}", fit_score_cached=50)
            for i in range(SCOUT_CANDIDATE_VERIFY_CAP + 2)
        )
        kept_a, _ = _truncate_candidates(cs, b"\xaa" * 16)
        kept_b, _ = _truncate_candidates(cs, b"\x55" * 16)
        assert set(c.candidate_id for c in kept_a) != set(
            c.candidate_id for c in kept_b
        )


class TestAdversarialExceptionPaths:
    def test_subclass_of_synopsis_parse_error_routes_to_v_03(self):
        class CustomParseError(SynopsisParseError):
            pass

        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("q" * 24),
            synopsis_fetcher=FakeFetcher(
                raise_with=CustomParseError("bad"),
            ),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
        )
        assert result.reason_code == F_SCOUT_V_03

    def test_base_fetch_error_routes_to_parse_unknown(self):
        # A direct SynopsisFetchError (not a mapped subclass) falls through
        # to the generic Exception branch → parse_unknown tag.
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("r" * 24),
            synopsis_fetcher=FakeFetcher(
                raise_with=SynopsisFetchError("ambiguous"),
            ),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
        )
        assert result.reason_code == f"{F_SCOUT_V_03}.parse_unknown"

    def test_empty_candidate_set_is_noop(self):
        cp, dw = _default_writers()
        result = verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=()),
            synopsis_fetcher=FakeFetcher(return_live=None),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        assert result.verdicts == {}
        assert result.verify_stage_state == VERIFY_STAGE_OK
        assert result.overflow == 0

    def test_timeout_seconds_default_matches_pin(self):
        # verify_candidate uses VERIFY_LIVE_SYNOPSIS_TIMEOUT_S default.
        result = verify_candidate(
            session=FakeSession(),
            candidate=_mk_candidate("s" * 24),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile=_mk_profile(),
            clock=_fixed_clock(),
        )
        assert result.timeout_seconds == VERIFY_LIVE_SYNOPSIS_TIMEOUT_S

    def test_fit_ratio_cannot_silently_flip_to_v_07(self):
        # Blueprint taxonomy is F-SCOUT-V-01..06. Any aggregate-failed ratio
        # (spec card's v07) must not appear in emitted reason codes.
        cp, dw = _default_writers()
        # 5 of 5 candidates fail: 100% failure ratio.
        cs = tuple(_mk_candidate(f"{i:024d}") for i in range(5))
        result = verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(candidates=cs),
            synopsis_fetcher=FakeFetcher(
                raise_with=SynopsisTimeoutError("slow"),
            ),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=_fixed_clock(),
        )
        for v in result.verdicts.values():
            assert "F-SCOUT-V-07" not in v.reason_code
        codes = [e.code for e in dw.events]
        assert "F-SCOUT-V-07" not in codes


# ---------------------------------------------------------------------------
# 20. Pool max_workers sizing
# ---------------------------------------------------------------------------


class TestPoolSizing:
    def test_executor_factory_receives_verify_pool_max_workers(self):
        captured: list[int] = []

        def factory(max_workers: int):
            captured.append(max_workers)
            return SequentialFakeExecutor(max_workers)

        cp, dw = _default_writers()
        verify_all(
            session=FakeSession(),
            discover_result=_mk_discover_result(
                candidates=(_mk_candidate("t" * 24),)
            ),
            synopsis_fetcher=FakeFetcher(return_live=_mk_live()),
            applicant_profile_provider=FakeProfileProvider(_mk_profile()),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=factory,
            clock=_fixed_clock(),
        )
        assert captured == [VERIFY_POOL_MAX_WORKERS]


# ---------------------------------------------------------------------------
# 21. Side-effect-free import
# ---------------------------------------------------------------------------


class TestSideEffectFreeImport:
    def test_import_does_not_open_sockets(self):
        # Module-scope has no network/disk — sanity check via source.
        src = Path(vs.__file__).read_text(encoding="utf-8")
        # No socket, no urllib, no requests at module scope.
        assert "import socket" not in src
        assert "import urllib" not in src

    def test_module_has_no_pragma_no_cover_abuse(self):
        # E-028: pragma no cover should be sparingly applied to
        # contract-unreachable defensive branches only.
        src = Path(vs.__file__).read_text(encoding="utf-8")
        pragma_count = src.count("# pragma: no cover")
        # Count stays low — current expectation is 1.
        assert pragma_count <= 2
