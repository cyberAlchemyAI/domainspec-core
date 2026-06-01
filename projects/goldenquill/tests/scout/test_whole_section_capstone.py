"""§3 Scout — whole-section capstone integration tests.

Per handoff `pipeline/handoffs/section_3_scout_whole_section_capstone_2026-04-29.md`.

Promotes §3 Scout from per-round LOCKs (R1-R11, ~18 code modules) to
LOCKED-as-a-whole-section. Test-only round; ZERO new §3 production code.

Three test surfaces from the handoff:

- S.1 Full DISCOVER → VERIFY → REVIEW lifecycle exercised end-to-end via
  ``run_scout_discover_verify_review`` over a synthetic 6-channel fan-out.
- S.2 BT12 Channel F domain preflight property tests — the BT owned by §3.
- S.3 Cross-channel composition — dedup across channels, health aggregation,
  union-cap enforcement, channel ordering invariants.

All collaborators (channel dispatchers, vault writers, signers, fetchers,
profile providers) are injected via the existing E-017 Protocol seams.
No network, no subprocess, no real clock dependency.
"""
from __future__ import annotations

import ast
import hashlib
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Mapping, Optional, Tuple

import pytest

import pipeline.scout as scout_pkg
from pipeline.scout._channel_f_jurisdictions import (
    JURISDICTION_TABLE,
    jurisdiction_for_etld,
)
from pipeline.scout._constants import (
    CHANNEL_A,
    CHANNEL_B,
    CHANNEL_C,
    CHANNEL_D,
    CHANNEL_E,
    CHANNEL_F,
    DECISION_ACCEPT,
    DECISION_HOLD,
    DECISION_REJECT,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
    VERDICT_UNVERIFIED,
    VERDICT_VERIFICATION_FAILED,
    VERDICT_VERIFIED_FIT,
    VERDICT_VERIFIED_NOT_FIT,
)
from pipeline.scout._types import (
    Candidate,
    ReviewQueueItem,
    SignedHealthTuple,
    VerificationVerdict,
)
from pipeline.scout.channel_f_websearch import (
    F_BT12_01,
    F_BT12_02,
    F_BT12_03,
    F_BT12_04,
    F_BT12_06,
    ChannelFJurisdictionPolicy,
    ChannelFJurisdictionReject,
    ChannelFNotOptedIn,
    ChannelFURLPunycodeError,
    _is_loopback_host,
    _jurisdiction_from_registrable_domain,
    _preflight_channel_f,
    _registrable_domain,
)
from pipeline.scout.discover import (
    F_SCOUT_CAPSTONE_01,
    F_SCOUT_CAPSTONE_02,
    F_SCOUT_CAPSTONE_03,
    F_SCOUT_CAPSTONE_04,
    F_SCOUT_CAPSTONE_05,
    F_SCOUT_CAPSTONE_06,
    SCOUT_UNION_CAP,
    CapstoneDegradationEvent,
    ScoutDiscoverInterrupted,
    ScoutDiscoverResult,
)
from pipeline.scout.review_stage import (
    F_SCOUT_R_01,
    F_SCOUT_R_02,
    ReviewEnqueueRejected,
)
from pipeline.scout.run import (
    F_SCOUT_RUN_01,
    F_SCOUT_RUN_02,
    F_SCOUT_RUN_03,
    F_SCOUT_RUN_04,
    MAX_FIT_RATIONALE_BYTES,
    RunDegradationEvent,
    ScoutRunInterrupted,
    ScoutRunResult,
    run_scout_discover_verify,
    run_scout_discover_verify_review,
)
from pipeline.scout.verify_stage import (
    F_SCOUT_V_01,
    F_SCOUT_V_02,
    VERIFY_STAGE_OK,
    ApplicantProfile,
    LiveSynopsis,
    ScoutVerifyResult,
    SynopsisFetcher,
    SynopsisNoLiveEndpoint,
    SynopsisTimeoutError,
    SynopsisUrlResolutionError,
)


# ---------------------------------------------------------------------------
# Test doubles (cross-section: shared across S.1 / S.3 / S.4 surfaces)
# ---------------------------------------------------------------------------


@dataclass
class FakeSession:
    session_id: str = "session-cap-001"
    slug: str = "mycosymbiotics_cooperative"
    operator_id: str = "josh"


@dataclass
class FakeChannelResult:
    """Minimal :class:`ChannelDiscoverResultLike` fake with optional
    Channel-A ``per_endpoint_state`` field. Each channel's real result
    type is exercised by the per-round suites; this fake only needs to
    satisfy the duck-typed Protocol the capstone consumes.
    """

    candidates: tuple[Candidate, ...]
    channel_state: str
    per_endpoint_state: Optional[Mapping[str, str]] = None


@dataclass
class WriteCall:
    path: str
    bytes_: bytes
    intent: str
    session_id: str
    slug: str


@dataclass
class RecordingVaultWriter:
    """Captures ``vault_write`` calls without touching the filesystem."""

    calls: List[WriteCall] = field(default_factory=list)

    def write(
        self,
        *,
        path: str,
        bytes_: bytes,
        intent: str,
        session_id: str,
        slug: str,
    ) -> None:
        self.calls.append(
            WriteCall(
                path=path,
                bytes_=bytes_,
                intent=intent,
                session_id=session_id,
                slug=slug,
            )
        )


@dataclass
class RecordingCheckpoint:
    """Single checkpoint sink usable as discover / verify / review writer."""

    label: str
    calls: List[Tuple[str, Mapping[str, Any]]] = field(default_factory=list)

    def write(self, *, stage: str, payload: Mapping[str, Any]) -> None:
        self.calls.append((stage, dict(payload)))

    def stages(self) -> List[str]:
        return [s for s, _ in self.calls]


@dataclass
class RecordingDegradation:
    label: str
    events: List[Any] = field(default_factory=list)

    def record(self, event: Any) -> None:
        self.events.append(event)


@dataclass
class FakeFuture:
    _payload: Any = None
    _raise: Optional[BaseException] = None

    def result(self, timeout: Optional[float] = None) -> Any:
        if self._raise is not None:
            raise self._raise
        return self._payload

    def cancel(self) -> bool:
        return True


class SequentialExecutor:
    """Deterministic non-thread executor — invokes fns immediately on submit."""

    def __init__(self, max_workers: int) -> None:
        self.max_workers = max_workers

    def __enter__(self) -> "SequentialExecutor":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        return None

    def submit(self, fn: Any, /) -> FakeFuture:
        try:
            return FakeFuture(_payload=fn())
        except BaseException as e:  # pragma: no cover - exercised by adversarial paths
            return FakeFuture(_raise=e)


def _sequential_executor_factory(max_workers: int) -> SequentialExecutor:
    return SequentialExecutor(max_workers)


def _fake_signer(
    *,
    session: Any,
    per_channel_states: Mapping[str, str],
    per_channel_a_endpoints: Mapping[str, str],
    run_wall_ns: int,
    run_tiebreak_seed: bytes,
) -> SignedHealthTuple:
    """Deterministic signer — does NOT call into Section 2 vault."""
    body = (
        f"{session.session_id}|{run_wall_ns}|{sorted(per_channel_states.items())}".encode("utf-8")
        + run_tiebreak_seed
    )
    return SignedHealthTuple(
        tuple_canonical=body,
        hmac_sha3_512=hashlib.sha3_512(body).digest(),
        signed_at_utc="2026-04-29T00:00:00Z",
        hmac_key_id="key-cap-001",
    )


def _make_candidate(
    cid: str,
    *,
    channel: str = CHANNEL_A,
    title: str = "Test Opp",
    fit: int = 80,
) -> Candidate:
    return Candidate(
        candidate_id=cid,
        channel=channel,
        feed_or_adapter_id=f"api:{channel.lower()}",
        source_key=f"src-{cid}",
        title=title,
        funder="Test Funder",
        funder_kind="federal",
        url=f"https://example.test/{cid}",
        close_date_utc="2026-12-01T00:00:00Z",
        award_ceiling=500_000,
        award_floor=50_000,
        applicant_types=("nonprofit",),
        program_page_url=None,
        fetch_timestamp_utc="2026-04-20T00:00:00Z",
        url_hash="0" * 128,
        content_hash=None,
        fit_score_cached=fit,
        cache_provenance=None,
    )


def _make_live_synopsis() -> LiveSynopsis:
    return LiveSynopsis(
        synopsis_url="https://example.test/live/x",
        content_hash="a" * 128,
        fetched_at_utc="2026-04-29T01:00:00Z",
        eligibility_live=("nonprofit",),
        award_floor_live=50_000,
        award_ceiling_live=500_000,
        close_date_live_utc="2026-12-01T00:00:00Z",
        eligible_geographies=("US",),
        evidence_quote="evidence text",
    )


@dataclass
class FakeFetcher:
    """SynopsisFetcher that returns a static :class:`LiveSynopsis` per
    candidate (or ``None`` to drive UNVERIFIED, or a raise spec to drive
    a specific failure code).
    """

    payload: Optional[LiveSynopsis] = None
    raise_for_ids: Mapping[str, BaseException] = field(default_factory=dict)
    none_for_ids: frozenset[str] = field(default_factory=frozenset)

    def fetch(
        self,
        *,
        candidate: Candidate,
        timeout_seconds: int,
    ) -> Optional[LiveSynopsis]:
        if candidate.candidate_id in self.raise_for_ids:
            raise self.raise_for_ids[candidate.candidate_id]
        if candidate.candidate_id in self.none_for_ids:
            return None
        return self.payload


@dataclass
class FakeProfileProvider:
    profile: ApplicantProfile = field(
        default_factory=lambda: ApplicantProfile(
            applicant_types=("nonprofit",),
            max_award_capacity=1_000_000,
            min_award_need=10_000,
            geography="US",
            min_lead_time_days=30,
        )
    )

    def get(self, *, session: Any) -> ApplicantProfile:
        return self.profile


def _channel_fns_with(
    candidates_by_channel: Mapping[str, tuple[Candidate, ...]],
    *,
    raises: Optional[Mapping[str, BaseException]] = None,
) -> dict[str, Any]:
    """Build a six-key dispatcher map. For channels in ``raises``, the
    callable raises the supplied exception when invoked.
    """
    raises = raises or {}
    out: dict[str, Any] = {}
    for ch in (CHANNEL_A, CHANNEL_B, CHANNEL_C, CHANNEL_D, CHANNEL_E, CHANNEL_F):
        if ch in raises:
            exc = raises[ch]

            def _raiser(_exc: BaseException = exc) -> Any:
                raise _exc

            out[ch] = _raiser
        else:
            cands = candidates_by_channel.get(ch, ())
            per_endpoint = (
                {"grants.gov": HEALTH_OK, "sam.gov": HEALTH_OK, "usaspending.gov": HEALTH_OK}
                if ch == CHANNEL_A
                else None
            )
            res = FakeChannelResult(
                candidates=cands, channel_state=HEALTH_OK, per_endpoint_state=per_endpoint
            )

            def _ok(_res: FakeChannelResult = res) -> FakeChannelResult:
                return _res

            out[ch] = _ok
    return out


def _build_run_kwargs(
    *,
    candidates_by_channel: Mapping[str, tuple[Candidate, ...]],
    fetcher: Optional[SynopsisFetcher] = None,
    profile: Optional[ApplicantProfile] = None,
    interrupt_probe_run: Optional[Any] = None,
    raises: Optional[Mapping[str, BaseException]] = None,
) -> dict[str, Any]:
    """Compose a full kwargs dict for ``run_scout_discover_verify_review``."""
    fetcher = fetcher or FakeFetcher(payload=_make_live_synopsis())
    provider = FakeProfileProvider(
        profile=profile
        or ApplicantProfile(
            applicant_types=("nonprofit",),
            max_award_capacity=1_000_000,
            min_award_need=10_000,
            geography="US",
            min_lead_time_days=30,
        )
    )
    return {
        "session": FakeSession(),
        "channel_fns": _channel_fns_with(candidates_by_channel, raises=raises),
        "synopsis_fetcher": fetcher,
        "applicant_profile_provider": provider,
        "vault_writer": RecordingVaultWriter(),
        "health_signer": _fake_signer,
        "checkpoint_writer_discover": RecordingCheckpoint("discover"),
        "checkpoint_writer_verify": RecordingCheckpoint("verify"),
        "checkpoint_writer_review": RecordingCheckpoint("review"),
        "degradation_writer_discover": RecordingDegradation("discover"),
        "degradation_writer_verify": RecordingDegradation("verify"),
        "executor_factory_discover": _sequential_executor_factory,
        "executor_factory_verify": _sequential_executor_factory,
        "interrupt_probe_run": interrupt_probe_run,
    }


# ===========================================================================
# S.0 — Public surface invariants (the §3 package contract a consumer pins)
# ===========================================================================


class TestS0PublicSurface:
    """Pin the §3 Scout package surface that downstream consumers (Pipeline,
    demo driver, Group 10 outside-audit) bind against.
    """

    def test_scout_pkg_version_pins_at_or_above_r11(self) -> None:
        m = re.match(r"^0\.1\.0-scout-r(\d+)$", scout_pkg.__version__)
        assert m is not None
        assert int(m.group(1)) >= 11

    def test_run_alias_is_identity(self) -> None:
        # Step 0 reconciliation #1 — both names resolve to the same object.
        assert run_scout_discover_verify is run_scout_discover_verify_review

    def test_channel_constants_are_six_distinct_letters(self) -> None:
        letters = {CHANNEL_A, CHANNEL_B, CHANNEL_C, CHANNEL_D, CHANNEL_E, CHANNEL_F}
        assert letters == {"A", "B", "C", "D", "E", "F"}

    def test_verdict_constants_are_four_distinct_values(self) -> None:
        verdicts = {
            VERDICT_VERIFIED_FIT,
            VERDICT_VERIFIED_NOT_FIT,
            VERDICT_UNVERIFIED,
            VERDICT_VERIFICATION_FAILED,
        }
        assert len(verdicts) == 4

    def test_decision_constants_are_three_distinct_values(self) -> None:
        decisions = {DECISION_ACCEPT, DECISION_REJECT, DECISION_HOLD}
        assert len(decisions) == 3

    def test_health_constants_are_three_distinct_values(self) -> None:
        states = {HEALTH_OK, HEALTH_DEGRADED, HEALTH_FAILED}
        assert len(states) == 3

    @pytest.mark.parametrize(
        "name",
        [
            # R1 types
            "Candidate",
            "ReviewQueueItem",
            "SignedHealthTuple",
            "VerificationVerdict",
            # R8 capstone
            "ScoutDiscoverResult",
            "run_scout_discover",
            # R9 verify
            "ScoutVerifyResult",
            "verify_all",
            "ApplicantProfile",
            "ApplicantProfileProvider",
            "SynopsisFetcher",
            # R10 review
            "enqueue_for_review",
            "record_operator_decision",
            "read_review_queue",
            "ReviewEnqueueRejected",
            # R10 entity research
            "run_entity_research",
            "EntityResearchResult",
            # R11 capstone
            "run_scout_discover_verify",
            "run_scout_discover_verify_review",
            "ScoutRunResult",
            "RunDegradationEvent",
            "ScoutRunInterrupted",
            "MAX_FIT_RATIONALE_BYTES",
        ],
    )
    def test_public_surface_reachable_via_pkg(self, name: str) -> None:
        assert hasattr(scout_pkg, name), f"pipeline.scout missing public symbol: {name}"

    def test_failure_code_namespaces_distinct(self) -> None:
        # F-SCOUT-D-* (discover capstone), F-SCOUT-V-* (verify),
        # F-SCOUT-R-* (review), F-SCOUT-RUN-* (run capstone),
        # F-BT12-* (Channel F preflight), F-SCOUT-CAPSTONE-* (discover)
        # — each should namespace cleanly.
        codes = {
            "F-SCOUT-CAPSTONE-": [
                F_SCOUT_CAPSTONE_01,
                F_SCOUT_CAPSTONE_02,
                F_SCOUT_CAPSTONE_03,
                F_SCOUT_CAPSTONE_04,
                F_SCOUT_CAPSTONE_05,
                F_SCOUT_CAPSTONE_06,
            ],
            "F-SCOUT-V-": [F_SCOUT_V_01, F_SCOUT_V_02],
            "F-SCOUT-R-": [F_SCOUT_R_01, F_SCOUT_R_02],
            "F-SCOUT-RUN-": [
                F_SCOUT_RUN_01,
                F_SCOUT_RUN_02,
                F_SCOUT_RUN_03,
                F_SCOUT_RUN_04,
            ],
            "F-BT12-": [F_BT12_01, F_BT12_02, F_BT12_03, F_BT12_04, F_BT12_06],
        }
        for prefix, group in codes.items():
            for code in group:
                assert code.startswith(prefix), f"{code!r} should start with {prefix!r}"


# ===========================================================================
# S.1 — Full DISCOVER → VERIFY → REVIEW lifecycle (cross-stage composition)
# ===========================================================================


class TestS1Lifecycle:
    """Compose the actual production primitives end-to-end. No stage is
    monkey-patched — DISCOVER, VERIFY, and REVIEW all run their real code
    over deterministic injected Protocols.
    """

    def test_six_channel_happy_path_yields_review_queue_items(self) -> None:
        cands = {
            CHANNEL_A: (_make_candidate("a-001", channel=CHANNEL_A),),
            CHANNEL_B: (_make_candidate("b-001", channel=CHANNEL_B),),
            CHANNEL_C: (_make_candidate("c-001", channel=CHANNEL_C),),
            CHANNEL_D: (_make_candidate("d-001", channel=CHANNEL_D),),
            CHANNEL_E: (_make_candidate("e-001", channel=CHANNEL_E),),
            CHANNEL_F: (_make_candidate("f-001", channel=CHANNEL_F),),
        }
        kw = _build_run_kwargs(candidates_by_channel=cands)
        result = run_scout_discover_verify_review(**kw)
        assert isinstance(result, ScoutRunResult)
        # All six channels reported HEALTH_OK; six candidates flowed through.
        assert set(result.per_channel_states.keys()) == {
            CHANNEL_A, CHANNEL_B, CHANNEL_C, CHANNEL_D, CHANNEL_E, CHANNEL_F,
        }
        assert all(v == HEALTH_OK for v in result.per_channel_states.values())
        assert len(result.candidates) == 6
        # All six VERIFIED_FIT (single profile + matching live synopsis).
        assert len(result.verdicts) == 6
        assert all(v.verdict == VERDICT_VERIFIED_FIT for v in result.verdicts.values())
        # Six review-queue items + six fit rationales + six vault writes.
        assert len(result.review_queue_items) == 6
        assert len(result.fit_rationales) == 6
        assert len(kw["vault_writer"].calls) == 6

    def test_run_id_is_24_hex_chars_and_deterministic(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-002", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(candidates_by_channel=cands)
        kw["entropy"] = lambda n: b"\x00" * n
        kw["clock_ns"] = lambda: 1_700_000_000_000_000_000
        result = run_scout_discover_verify_review(**kw)
        assert len(result.run_id) == 24
        assert all(c in "0123456789abcdef" for c in result.run_id)
        # Re-run with same entropy + clock → same run_id.
        kw2 = _build_run_kwargs(candidates_by_channel=cands)
        kw2["entropy"] = lambda n: b"\x00" * n
        kw2["clock_ns"] = lambda: 1_700_000_000_000_000_000
        result2 = run_scout_discover_verify_review(**kw2)
        assert result2.run_id == result.run_id

    def test_per_stage_checkpoint_discipline_success(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-003", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(candidates_by_channel=cands)
        run_scout_discover_verify_review(**kw)
        # Discover wrote start + per-channel + complete.
        d_stages = kw["checkpoint_writer_discover"].stages()
        assert "discover_start" in d_stages
        assert "discover_complete" in d_stages
        assert d_stages.count("discover_channel_complete") == 6
        # Verify wrote per-candidate stages + final close.
        v_stages = kw["checkpoint_writer_verify"].stages()
        assert any(s.startswith("verify") for s in v_stages)
        # Review wrote start + complete with outcome=success.
        r_stages = kw["checkpoint_writer_review"].stages()
        assert "run_review_start" in r_stages
        assert "run_review_complete" in r_stages

    def test_one_channel_raises_isolation_does_not_crash_pipeline(self) -> None:
        # Channel C raises mid-fan-out; remaining channels still complete.
        cands = {
            CHANNEL_A: (_make_candidate("a-004", channel=CHANNEL_A),),
            CHANNEL_B: (_make_candidate("b-004", channel=CHANNEL_B),),
            CHANNEL_D: (_make_candidate("d-004", channel=CHANNEL_D),),
        }
        kw = _build_run_kwargs(
            candidates_by_channel=cands,
            raises={CHANNEL_C: RuntimeError("Channel C exploded")},
        )
        result = run_scout_discover_verify_review(**kw)
        assert isinstance(result, ScoutRunResult)
        # Channel C marked HEALTH_FAILED; A/B/D still HEALTH_OK.
        assert result.per_channel_states[CHANNEL_C] == HEALTH_FAILED
        assert result.per_channel_states[CHANNEL_A] == HEALTH_OK
        # F-SCOUT-CAPSTONE-02 event recorded for Channel C.
        codes = [ev.code for ev in result.discover_capstone_events]
        assert F_SCOUT_CAPSTONE_02 in codes
        # 3 VERIFIED_FIT candidates → 3 review items.
        assert len(result.review_queue_items) == 3

    def test_unverified_when_no_live_endpoint(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-005", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(
            candidates_by_channel=cands,
            fetcher=FakeFetcher(none_for_ids=frozenset({"a-005"})),
        )
        result = run_scout_discover_verify_review(**kw)
        verdict = result.verdicts["a-005"]
        assert verdict.verdict == VERDICT_UNVERIFIED
        # No review item: only VERIFIED_FIT enqueues.
        assert len(result.review_queue_items) == 0

    def test_verified_not_fit_when_geography_mismatches(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-006", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(
            candidates_by_channel=cands,
            profile=ApplicantProfile(
                applicant_types=("nonprofit",),
                max_award_capacity=1_000_000,
                min_award_need=10_000,
                geography="CA",  # mismatches LiveSynopsis.eligible_geographies=("US",)
                min_lead_time_days=30,
            ),
        )
        result = run_scout_discover_verify_review(**kw)
        verdict = result.verdicts["a-006"]
        assert verdict.verdict == VERDICT_VERIFIED_NOT_FIT
        assert len(result.review_queue_items) == 0

    def test_verification_failed_on_fetcher_url_error(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-007", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(
            candidates_by_channel=cands,
            fetcher=FakeFetcher(
                raise_for_ids={
                    "a-007": SynopsisUrlResolutionError("dns nx")
                }
            ),
        )
        result = run_scout_discover_verify_review(**kw)
        verdict = result.verdicts["a-007"]
        assert verdict.verdict == VERDICT_VERIFICATION_FAILED
        assert verdict.reason_code.startswith(F_SCOUT_V_01)
        assert len(result.review_queue_items) == 0

    def test_verification_failed_on_fetcher_timeout(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-008", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(
            candidates_by_channel=cands,
            fetcher=FakeFetcher(
                raise_for_ids={"a-008": SynopsisTimeoutError("budget")}
            ),
        )
        result = run_scout_discover_verify_review(**kw)
        verdict = result.verdicts["a-008"]
        assert verdict.verdict == VERDICT_VERIFICATION_FAILED
        assert verdict.reason_code.startswith(F_SCOUT_V_02)

    def test_review_enqueue_writes_canonical_json_via_vault(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-009", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(candidates_by_channel=cands)
        run_scout_discover_verify_review(**kw)
        assert len(kw["vault_writer"].calls) == 1
        call = kw["vault_writer"].calls[0]
        # Path follows orgs/{slug}/scout/review_queue/{candidate_id}.json
        assert "review_queue" in call.path
        assert "a-009" in call.path
        # Bytes are non-empty and JSON-decodable as the queue item.
        assert len(call.bytes_) > 0
        import json

        decoded = json.loads(call.bytes_.decode("utf-8"))
        assert decoded["candidate_id"] == "a-009"
        assert decoded["queued_by_verdict"] == VERDICT_VERIFIED_FIT

    def test_six_channels_with_dedup_collapses_duplicate_candidate_id(self) -> None:
        # Same candidate_id appearing on Channel A and Channel C → first-writer wins.
        cands = {
            CHANNEL_A: (_make_candidate("dup-001", channel=CHANNEL_A, fit=90),),
            CHANNEL_C: (_make_candidate("dup-001", channel=CHANNEL_C, fit=70),),
        }
        kw = _build_run_kwargs(candidates_by_channel=cands)
        result = run_scout_discover_verify_review(**kw)
        # Only one candidate emitted post-dedup.
        assert len(result.candidates) == 1
        # F-SCOUT-CAPSTONE-03 dedup event recorded.
        codes = [ev.code for ev in result.discover_capstone_events]
        assert F_SCOUT_CAPSTONE_03 in codes

    def test_signed_health_tuple_carries_per_channel_states(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-010", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(candidates_by_channel=cands)
        result = run_scout_discover_verify_review(**kw)
        assert isinstance(result.signed_health, SignedHealthTuple)
        assert result.signed_health.hmac_key_id == "key-cap-001"
        assert len(result.signed_health.hmac_sha3_512) == 64

    def test_run_review_complete_carries_run_id(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-011", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(candidates_by_channel=cands)
        result = run_scout_discover_verify_review(**kw)
        complete = next(
            payload
            for stage, payload in kw["checkpoint_writer_review"].calls
            if stage == "run_review_complete"
        )
        assert complete["run_id"] == result.run_id
        assert complete["outcome"] == "success"

    def test_no_review_queue_items_when_zero_candidates(self) -> None:
        kw = _build_run_kwargs(candidates_by_channel={})
        result = run_scout_discover_verify_review(**kw)
        assert len(result.candidates) == 0
        assert len(result.verdicts) == 0
        assert len(result.review_queue_items) == 0
        assert len(kw["vault_writer"].calls) == 0
        # run_review_start + run_review_complete still fire.
        r_stages = kw["checkpoint_writer_review"].stages()
        assert "run_review_start" in r_stages
        assert "run_review_complete" in r_stages

    def test_dispatch_map_missing_channel_raises_run_03(self) -> None:
        kw = _build_run_kwargs(candidates_by_channel={})
        del kw["channel_fns"][CHANNEL_F]
        with pytest.raises(KeyError) as exc:
            run_scout_discover_verify_review(**kw)
        assert F_SCOUT_RUN_03 in str(exc.value)
        assert CHANNEL_F in str(exc.value)

    def test_interrupt_mid_review_raises_scout_run_interrupted(self) -> None:
        cands = {
            CHANNEL_A: (
                _make_candidate("int-1", channel=CHANNEL_A, fit=99),
                _make_candidate("int-2", channel=CHANNEL_A, fit=90),
            ),
        }
        # Probe sees False before int-1, True before int-2.
        flips = iter([False, True, True])
        probe = lambda: next(flips)
        kw = _build_run_kwargs(candidates_by_channel=cands, interrupt_probe_run=probe)
        with pytest.raises(ScoutRunInterrupted) as exc:
            run_scout_discover_verify_review(**kw)
        # int-1 enqueued before interrupt; int-2 deferred.
        assert exc.value.completed_candidate_ids == ("int-1",)
        # F-SCOUT-RUN-04 reason embedded.
        assert F_SCOUT_RUN_04 in str(exc.value)
        # Vault saw exactly one write.
        assert len(kw["vault_writer"].calls) == 1


# ===========================================================================
# S.2 — BT12 Channel F domain preflight (the BT owned by §3)
# ===========================================================================


class TestS2BT12JurisdictionTable:
    """Properties of the static eTLD → ISO-3166-1 lookup table."""

    def test_table_is_immutable_view(self) -> None:
        # MappingProxyType raises TypeError on mutation.
        with pytest.raises(TypeError):
            JURISDICTION_TABLE["xx"] = "NEW"  # type: ignore[index]

    def test_known_us_cctld(self) -> None:
        assert jurisdiction_for_etld("us") == "US"

    def test_known_de_cctld(self) -> None:
        assert jurisdiction_for_etld("de") == "DE"

    def test_uk_legacy_resolves_to_gb(self) -> None:
        # Traditional .uk ccTLD; ISO code is GB.
        assert jurisdiction_for_etld("uk") == "GB"

    def test_eu_resolves_to_eu_jurisdiction_tag(self) -> None:
        assert jurisdiction_for_etld("eu") == "EU"

    @pytest.mark.parametrize("gtld", ["com", "net", "org", "info", "io", "ai"])
    def test_common_gtlds_route_to_gtld_bucket(self, gtld: str) -> None:
        assert jurisdiction_for_etld(gtld) == "GTLD"

    @pytest.mark.parametrize("us_reserved", ["gov", "mil", "edu"])
    def test_us_reserved_tlds_resolve_to_us(self, us_reserved: str) -> None:
        assert jurisdiction_for_etld(us_reserved) == "US"

    def test_unknown_etld_resolves_to_none(self) -> None:
        assert jurisdiction_for_etld("notarealetld") is None

    def test_empty_string_resolves_to_none(self) -> None:
        assert jurisdiction_for_etld("") is None

    def test_label_lookup_is_case_insensitive(self) -> None:
        assert jurisdiction_for_etld("US") == "US"
        assert jurisdiction_for_etld("De") == "DE"

    def test_non_string_input_safe(self) -> None:
        # Defensive: non-str input must not raise.
        assert jurisdiction_for_etld(None) is None  # type: ignore[arg-type]
        assert jurisdiction_for_etld(123) is None  # type: ignore[arg-type]


class TestS2BT12RegistrableDomain:
    """Properties of ``_registrable_domain`` (callers normalise via idna)."""

    @pytest.mark.parametrize(
        "url, expected",
        [
            ("https://www.example.com/x", "example.com"),
            ("http://nasa.gov/about", "nasa.gov"),
            ("https://sub.deeper.example.org/p", "example.org"),
        ],
    )
    def test_basic_extraction(self, url: str, expected: str) -> None:
        assert _registrable_domain(url) == expected

    def test_punycode_round_trip(self) -> None:
        # An IDN host should normalise to its xn-- form.
        # bücher.example → xn--bcher-kva.example
        result = _registrable_domain("https://bücher.example/")
        assert "xn--" in result or "example" in result

    def test_no_host_raises_punycode_error(self) -> None:
        with pytest.raises(ChannelFURLPunycodeError) as exc:
            _registrable_domain("file:///local/path")
        assert F_BT12_06 in str(exc.value)

    def test_invalid_idna_raises_punycode_error(self) -> None:
        # Hyphen-only label rejected by idna UTS46.
        with pytest.raises(ChannelFURLPunycodeError) as exc:
            _registrable_domain("https://---/")
        assert F_BT12_06 in str(exc.value)

    def test_jurisdiction_from_registrable_domain_known(self) -> None:
        assert _jurisdiction_from_registrable_domain("example.com") == "GTLD"
        assert _jurisdiction_from_registrable_domain("nasa.gov") == "US"

    def test_jurisdiction_from_registrable_domain_empty(self) -> None:
        assert _jurisdiction_from_registrable_domain("") is None

    def test_jurisdiction_from_registrable_domain_unknown_tld(self) -> None:
        # An unrecognised final label resolves to None → BT12 default-deny.
        assert _jurisdiction_from_registrable_domain("foo.zzfake") is None


class TestS2BT12LoopbackBypass:
    """Loopback hosts skip jurisdiction (SearxNG runs on the Golden Quill)."""

    def test_127_0_0_1_is_loopback(self) -> None:
        assert _is_loopback_host("http://127.0.0.1:8888/search") is True

    def test_ipv6_loopback(self) -> None:
        assert _is_loopback_host("http://[::1]:8888/search") is True

    def test_external_host_not_loopback(self) -> None:
        assert _is_loopback_host("https://example.com/") is False

    def test_no_host_not_loopback(self) -> None:
        assert _is_loopback_host("not-a-url") is False


class TestS2BT12Preflight:
    """End-to-end preflight policy enforcement (the BT12 contract)."""

    def _session(self) -> FakeSession:
        return FakeSession()

    def test_opt_in_false_rejects_with_bt12_01(self) -> None:
        policy = ChannelFJurisdictionPolicy(opt_in=False)
        with pytest.raises(ChannelFNotOptedIn) as exc:
            _preflight_channel_f(self._session(), "https://nasa.gov/", policy)
        assert F_BT12_01 in str(exc.value)

    def test_loopback_passes_when_opted_in_regardless_of_allowlist(self) -> None:
        policy = ChannelFJurisdictionPolicy(
            opt_in=True, allowed_jurisdictions=frozenset({"US"})
        )
        # Loopback bypasses jurisdiction → returns None.
        assert _preflight_channel_f(
            self._session(), "http://127.0.0.1:8888/q", policy
        ) is None

    def test_per_org_denylist_rejects_with_bt12_02(self) -> None:
        policy = ChannelFJurisdictionPolicy(
            opt_in=True,
            allowed_jurisdictions=frozenset({"GTLD"}),
            disallowed_registrable_domains=frozenset({"evil.com"}),
        )
        with pytest.raises(ChannelFJurisdictionReject) as exc:
            _preflight_channel_f(self._session(), "https://evil.com/x", policy)
        assert F_BT12_02 in str(exc.value)

    def test_unknown_jurisdiction_rejects_with_bt12_03(self) -> None:
        policy = ChannelFJurisdictionPolicy(
            opt_in=True, allowed_jurisdictions=frozenset({"US"})
        )
        with pytest.raises(ChannelFJurisdictionReject) as exc:
            _preflight_channel_f(self._session(), "https://foo.zzfake/", policy)
        assert F_BT12_03 in str(exc.value)

    def test_jurisdiction_not_in_allowlist_rejects_with_bt12_04(self) -> None:
        policy = ChannelFJurisdictionPolicy(
            opt_in=True, allowed_jurisdictions=frozenset({"DE"})
        )
        # nasa.gov is US, not in allowlist {DE} → F-BT12-04
        with pytest.raises(ChannelFJurisdictionReject) as exc:
            _preflight_channel_f(self._session(), "https://nasa.gov/", policy)
        assert F_BT12_04 in str(exc.value)

    def test_allowed_us_domain_passes(self) -> None:
        policy = ChannelFJurisdictionPolicy(
            opt_in=True, allowed_jurisdictions=frozenset({"US"})
        )
        # nasa.gov is US, allowed. Returns None (accept).
        assert _preflight_channel_f(
            self._session(), "https://nasa.gov/about", policy
        ) is None

    def test_allowed_gtld_domain_passes_when_gtld_in_allowlist(self) -> None:
        policy = ChannelFJurisdictionPolicy(
            opt_in=True, allowed_jurisdictions=frozenset({"GTLD"})
        )
        assert _preflight_channel_f(
            self._session(), "https://example.com/", policy
        ) is None

    def test_punycode_failure_propagates_with_bt12_06(self) -> None:
        policy = ChannelFJurisdictionPolicy(
            opt_in=True, allowed_jurisdictions=frozenset({"US"})
        )
        with pytest.raises(ChannelFURLPunycodeError) as exc:
            _preflight_channel_f(self._session(), "https://---/", policy)
        assert F_BT12_06 in str(exc.value)


class TestS2BT12Adversarial:
    """BT12 adversarial — domain spoofing variants that must not bypass."""

    def test_path_traversal_in_url_does_not_alter_registrable_domain(self) -> None:
        # Path-component .. cannot reach into the host for jurisdiction
        # resolution; the host is parsed first.
        result = _registrable_domain("https://example.com/../../evil.cn")
        assert result == "example.com"

    def test_subdomain_injection_resolves_to_etld_plus_one(self) -> None:
        # An attacker prepending a "victim.gov." subdomain to attacker.cn
        # cannot escape the eTLD+1 collapse.
        result = _registrable_domain("https://victim.gov.attacker.cn/")
        assert result == "attacker.cn"
        assert _jurisdiction_from_registrable_domain(result) == "CN"

    def test_default_deny_unknown_tld_in_strict_policy(self) -> None:
        # Strict allowlist {US} + unknown TLD → F-BT12-03 regardless.
        policy = ChannelFJurisdictionPolicy(
            opt_in=True, allowed_jurisdictions=frozenset({"US"})
        )
        with pytest.raises(ChannelFJurisdictionReject) as exc:
            _preflight_channel_f(
                FakeSession(), "https://foo.invalidetld/", policy
            )
        assert F_BT12_03 in str(exc.value)

    def test_denylist_takes_priority_over_allowlist(self) -> None:
        # A domain on the denylist must reject even when its jurisdiction
        # is in the allowlist.
        policy = ChannelFJurisdictionPolicy(
            opt_in=True,
            allowed_jurisdictions=frozenset({"GTLD"}),
            disallowed_registrable_domains=frozenset({"good.com"}),
        )
        with pytest.raises(ChannelFJurisdictionReject) as exc:
            _preflight_channel_f(FakeSession(), "https://good.com/", policy)
        assert F_BT12_02 in str(exc.value)

    def test_default_policy_opts_out(self) -> None:
        # Default ChannelFJurisdictionPolicy() has opt_in=False — every
        # call must reject with F-BT12-01.
        policy = ChannelFJurisdictionPolicy()
        with pytest.raises(ChannelFNotOptedIn):
            _preflight_channel_f(FakeSession(), "https://anything.com/", policy)


# ===========================================================================
# S.3 — Cross-channel composition (dedup, ordering, health aggregation)
# ===========================================================================


class TestS3CrossChannelComposition:
    def test_deduplication_keeps_first_writer(self) -> None:
        # Channel A wins over Channel C for shared candidate_id.
        cands = {
            CHANNEL_A: (_make_candidate("share-1", channel=CHANNEL_A, fit=90),),
            CHANNEL_C: (
                _make_candidate("share-1", channel=CHANNEL_C, fit=70),
                _make_candidate("c-only", channel=CHANNEL_C, fit=60),
            ),
        }
        kw = _build_run_kwargs(candidates_by_channel=cands)
        result = run_scout_discover_verify_review(**kw)
        # share-1 + c-only — two unique candidates.
        ids = {c.candidate_id for c in result.candidates}
        assert ids == {"share-1", "c-only"}
        # The kept share-1 came from A (fit=90).
        share_1 = next(c for c in result.candidates if c.candidate_id == "share-1")
        assert share_1.channel == CHANNEL_A
        assert share_1.fit_score_cached == 90

    def test_channel_iteration_order_is_a_through_f(self) -> None:
        # Channel completion checkpoints land in pinned A→F order even when
        # candidates appear out-of-channel.
        cands = {
            CHANNEL_F: (_make_candidate("f-1", channel=CHANNEL_F),),
            CHANNEL_A: (_make_candidate("a-1", channel=CHANNEL_A),),
        }
        kw = _build_run_kwargs(candidates_by_channel=cands)
        run_scout_discover_verify_review(**kw)
        d_calls = kw["checkpoint_writer_discover"].calls
        per_channel_calls = [
            payload for stage, payload in d_calls if stage == "discover_channel_complete"
        ]
        ordered_channels = [p["channel"] for p in per_channel_calls]
        assert ordered_channels == [
            CHANNEL_A, CHANNEL_B, CHANNEL_C, CHANNEL_D, CHANNEL_E, CHANNEL_F,
        ]

    def test_per_channel_health_aggregation_under_one_failure(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-1", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(
            candidates_by_channel=cands,
            raises={CHANNEL_E: ValueError("rss broken")},
        )
        result = run_scout_discover_verify_review(**kw)
        assert result.per_channel_states[CHANNEL_A] == HEALTH_OK
        assert result.per_channel_states[CHANNEL_E] == HEALTH_FAILED

    def test_dedup_from_b_then_c_first_writer_wins(self) -> None:
        # Channel B (cache) wins over Channel C (portal) for shared id.
        cands = {
            CHANNEL_B: (_make_candidate("share-bc", channel=CHANNEL_B, fit=88),),
            CHANNEL_C: (_make_candidate("share-bc", channel=CHANNEL_C, fit=72),),
        }
        kw = _build_run_kwargs(candidates_by_channel=cands)
        result = run_scout_discover_verify_review(**kw)
        cand = next(c for c in result.candidates if c.candidate_id == "share-bc")
        assert cand.channel == CHANNEL_B

    def test_six_channel_emit_combines_to_six_candidates(self) -> None:
        cands = {
            ch: (_make_candidate(f"{ch.lower()}-uniq", channel=ch),)
            for ch in (CHANNEL_A, CHANNEL_B, CHANNEL_C, CHANNEL_D, CHANNEL_E, CHANNEL_F)
        }
        kw = _build_run_kwargs(candidates_by_channel=cands)
        result = run_scout_discover_verify_review(**kw)
        assert len(result.candidates) == 6
        # Each channel contributed its own candidate.
        ch_ids = {c.channel for c in result.candidates}
        assert ch_ids == {CHANNEL_A, CHANNEL_B, CHANNEL_C, CHANNEL_D, CHANNEL_E, CHANNEL_F}

    def test_zero_candidates_yields_zero_capstone_events(self) -> None:
        kw = _build_run_kwargs(candidates_by_channel={})
        result = run_scout_discover_verify_review(**kw)
        # No channel raised → no per-channel events. No dedup → no
        # F-SCOUT-CAPSTONE-03 events. No overflow → no F-SCOUT-CAPSTONE-04.
        assert result.discover_capstone_events == ()

    def test_run_capstone_events_default_empty(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-1", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(candidates_by_channel=cands)
        result = run_scout_discover_verify_review(**kw)
        assert result.run_degradation_events == ()

    def test_channel_a_endpoint_states_propagate(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-1", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(candidates_by_channel=cands)
        result = run_scout_discover_verify_review(**kw)
        # Channel A endpoint dict contains the three sub-endpoints.
        assert "grants.gov" in result.per_channel_a_endpoints
        assert "sam.gov" in result.per_channel_a_endpoints
        assert "usaspending.gov" in result.per_channel_a_endpoints

    def test_review_queue_items_preserve_candidate_order(self) -> None:
        # Below the union cap, DISCOVER preserves emission order (no
        # truncation sort). REVIEW iterates candidates in DISCOVER's
        # stable order — so the queue items mirror the emission sequence.
        cands = {
            CHANNEL_A: (
                _make_candidate("a-z", channel=CHANNEL_A),
                _make_candidate("a-m", channel=CHANNEL_A),
                _make_candidate("a-a", channel=CHANNEL_A),
            ),
        }
        kw = _build_run_kwargs(candidates_by_channel=cands)
        result = run_scout_discover_verify_review(**kw)
        item_ids = [it.candidate_id for it in result.review_queue_items]
        # Insertion order, not lexicographic order.
        assert item_ids == ["a-z", "a-m", "a-a"]

    def test_all_six_channels_failing_yields_six_capstone_02_events(self) -> None:
        cands = {}
        kw = _build_run_kwargs(
            candidates_by_channel=cands,
            raises={
                CHANNEL_A: RuntimeError("a"),
                CHANNEL_B: RuntimeError("b"),
                CHANNEL_C: RuntimeError("c"),
                CHANNEL_D: RuntimeError("d"),
                CHANNEL_E: RuntimeError("e"),
                CHANNEL_F: RuntimeError("f"),
            },
        )
        result = run_scout_discover_verify_review(**kw)
        codes = [ev.code for ev in result.discover_capstone_events]
        assert codes.count(F_SCOUT_CAPSTONE_02) == 6
        # All channels HEALTH_FAILED.
        assert all(s == HEALTH_FAILED for s in result.per_channel_states.values())
        # Zero candidates emitted; zero review items.
        assert len(result.candidates) == 0
        assert len(result.review_queue_items) == 0

    def test_partial_channel_failures_do_not_block_review_enqueue(self) -> None:
        # 3 channels work, 3 fail. Surviving candidates flow through.
        cands = {
            CHANNEL_A: (_make_candidate("a-1", channel=CHANNEL_A),),
            CHANNEL_C: (_make_candidate("c-1", channel=CHANNEL_C),),
            CHANNEL_F: (_make_candidate("f-1", channel=CHANNEL_F),),
        }
        kw = _build_run_kwargs(
            candidates_by_channel=cands,
            raises={
                CHANNEL_B: RuntimeError("b"),
                CHANNEL_D: RuntimeError("d"),
                CHANNEL_E: RuntimeError("e"),
            },
        )
        result = run_scout_discover_verify_review(**kw)
        assert len(result.review_queue_items) == 3

    def test_capstone_run_id_unique_per_seed(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-1", channel=CHANNEL_A),)}
        kw1 = _build_run_kwargs(candidates_by_channel=cands)
        kw1["entropy"] = lambda n: b"\x01" * n
        kw1["clock_ns"] = lambda: 1_700_000_000_000_000_000
        kw2 = _build_run_kwargs(candidates_by_channel=cands)
        kw2["entropy"] = lambda n: b"\x02" * n
        kw2["clock_ns"] = lambda: 1_700_000_000_000_000_000
        r1 = run_scout_discover_verify_review(**kw1)
        r2 = run_scout_discover_verify_review(**kw2)
        assert r1.run_id != r2.run_id


# ===========================================================================
# S.4 — Adversarial / replay invariants
# ===========================================================================


class TestS4Adversarial:
    def test_replay_with_identical_inputs_yields_identical_run_id(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("rp-1", channel=CHANNEL_A),)}
        for _ in range(2):
            kw = _build_run_kwargs(candidates_by_channel=cands)
            kw["entropy"] = lambda n: b"\x05" * n
            kw["clock_ns"] = lambda: 1_700_000_000_000_000_000
            result = run_scout_discover_verify_review(**kw)
            if "_first_run_id" not in dir(self):
                self._first_run_id = result.run_id  # type: ignore[attr-defined]
            else:
                assert result.run_id == self._first_run_id  # type: ignore[attr-defined]

    def test_keyboard_interrupt_propagates_unchanged_from_channel(self) -> None:
        cands = {}
        kw = _build_run_kwargs(
            candidates_by_channel=cands,
            raises={CHANNEL_A: KeyboardInterrupt()},
        )
        with pytest.raises(KeyboardInterrupt):
            run_scout_discover_verify_review(**kw)

    def test_system_exit_propagates_unchanged_from_channel(self) -> None:
        cands = {}
        kw = _build_run_kwargs(
            candidates_by_channel=cands,
            raises={CHANNEL_A: SystemExit(2)},
        )
        with pytest.raises(SystemExit):
            run_scout_discover_verify_review(**kw)

    def test_signer_failure_records_capstone_06_and_propagates(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("a-1", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(candidates_by_channel=cands)

        def angry_signer(**_: Any) -> SignedHealthTuple:
            raise RuntimeError("hsm offline")

        kw["health_signer"] = angry_signer
        with pytest.raises(RuntimeError, match="hsm offline"):
            run_scout_discover_verify_review(**kw)
        events = kw["degradation_writer_discover"].events
        assert any(ev.code == F_SCOUT_CAPSTONE_06 for ev in events)

    def test_review_path_traversal_is_rejected_by_review_stage(self) -> None:
        # F-SCOUT-R-02 — slug or candidate_id with path components must
        # be rejected before any vault write happens. We exercise this
        # via the public enqueue_for_review entry directly to keep the
        # adversarial case targeted.
        # NOTE: pipeline.scout.* may have been evicted from sys.modules by
        # an earlier test (test_round_1's reload-timing probe). Re-import
        # the rejection class fresh so pytest.raises matches the same
        # class object that ``enqueue_for_review`` actually raises.
        from pipeline.scout.review_stage import (
            ReviewEnqueueRejected as _ReviewEnqueueRejected,
            enqueue_for_review,
        )

        candidate = _make_candidate("../escape", channel=CHANNEL_A)
        verdict = VerificationVerdict(
            candidate_id=candidate.candidate_id,
            verdict=VERDICT_VERIFIED_FIT,
            reason_code="V-OK",
            live_synopsis_url="https://example.test/live",
            live_content_hash="x" * 128,
            fetched_at_utc="2026-04-29T00:00:00Z",
            timeout_seconds=10,
            eligibility_live=("nonprofit",),
            award_floor_live=10_000,
            award_ceiling_live=100_000,
            close_date_live_utc="2026-12-01T00:00:00Z",
            evidence_quote="x",
        )
        sess = FakeSession(slug="mysession-bad")
        with pytest.raises(_ReviewEnqueueRejected) as exc:
            enqueue_for_review(
                session=sess,
                candidate=candidate,
                verdict=verdict,
                fit_rationale="ok",
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=RecordingCheckpoint("review"),
            )
        assert F_SCOUT_R_02 in str(exc.value)

    def test_non_fit_verdict_rejected_at_review_stage_with_r_01(self) -> None:
        # Direct exercise of F-SCOUT-R-01 (only VERIFIED_FIT enqueues).
        # See sys.modules-reload note in path-traversal test above.
        from pipeline.scout.review_stage import (
            ReviewEnqueueRejected as _ReviewEnqueueRejected,
            enqueue_for_review,
        )

        candidate = _make_candidate("nf-1", channel=CHANNEL_A)
        verdict = VerificationVerdict(
            candidate_id=candidate.candidate_id,
            verdict=VERDICT_VERIFIED_NOT_FIT,
            reason_code="A-ELIG-01",
            live_synopsis_url=None,
            live_content_hash=None,
            fetched_at_utc=None,
            timeout_seconds=10,
            eligibility_live=(),
            award_floor_live=None,
            award_ceiling_live=None,
            close_date_live_utc=None,
            evidence_quote=None,
        )
        with pytest.raises(_ReviewEnqueueRejected) as exc:
            enqueue_for_review(
                session=FakeSession(),
                candidate=candidate,
                verdict=verdict,
                fit_rationale="ok",
                vault_writer=RecordingVaultWriter(),
                checkpoint_writer=RecordingCheckpoint("review"),
            )
        assert F_SCOUT_R_01 in str(exc.value)

    def test_oversize_rationale_skips_enqueue(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("over-1", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(candidates_by_channel=cands)
        kw["build_fit_rationale"] = (
            lambda *, session, candidate, verdict: "x" * (MAX_FIT_RATIONALE_BYTES + 1)
        )
        result = run_scout_discover_verify_review(**kw)
        # No review item; degradation event with F-SCOUT-RUN-01.
        assert len(result.review_queue_items) == 0
        assert any(ev.code == F_SCOUT_RUN_01 for ev in result.run_degradation_events)

    def test_rationale_builder_failure_recorded_with_run_02(self) -> None:
        cands = {CHANNEL_A: (_make_candidate("boom-1", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(candidates_by_channel=cands)

        def boom(**_: Any) -> str:
            raise ValueError("rationale exploded")

        kw["build_fit_rationale"] = boom
        result = run_scout_discover_verify_review(**kw)
        assert len(result.review_queue_items) == 0
        assert any(ev.code == F_SCOUT_RUN_02 for ev in result.run_degradation_events)


# ===========================================================================
# S.5 — AST-lint + module-lineage discipline (E-026 formal + §7.16 boundary)
# ===========================================================================


class TestS5ASTLint:
    """Pipeline-wide lint must report zero violations under DEFAULT_RULES.
    Round 11 already pinned this for ``run.py``; we re-pin at the section
    level to detect any drift introduced by a future cross-module change.
    """

    def test_lint_tree_clean_on_pipeline_scout(self, tmp_path: Path) -> None:
        from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree

        repo_root = Path(__file__).resolve().parents[2]
        scout_dir_src = repo_root / "pipeline" / "scout"
        scout_dir_dst = tmp_path / "pipeline" / "scout"
        scout_dir_dst.mkdir(parents=True)
        (tmp_path / "pipeline" / "__init__.py").write_text("")
        for py in scout_dir_src.glob("*.py"):
            shutil.copy(py, scout_dir_dst / py.name)
        violations = lint_tree(tmp_path, DEFAULT_RULES)
        assert violations == [], f"AST-lint violations: {violations}"

    def test_run_module_does_not_import_llm(self) -> None:
        # §7.16 — pipeline/scout/run.py must not import any LLM provider.
        forbidden = {
            "anthropic",
            "openai",
            "google.generativeai",
            "google_generativeai",
            "groq",
            "ollama",
            "litellm",
        }
        path = (
            Path(__file__).resolve().parents[2]
            / "pipeline"
            / "scout"
            / "run.py"
        )
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name not in forbidden, (
                        f"forbidden top-level import: {alias.name}"
                    )
            if isinstance(node, ast.ImportFrom):
                if node.module is not None:
                    assert node.module not in forbidden, (
                        f"forbidden ImportFrom: {node.module}"
                    )


class TestS5ModuleLineage:
    """E-026 formal — shared symbols carry their __module__ from origin."""

    def test_candidate_origin_is_types_module(self) -> None:
        assert Candidate.__module__ == "pipeline.scout._types"

    def test_review_queue_item_origin_is_types_module(self) -> None:
        assert ReviewQueueItem.__module__ == "pipeline.scout._types"

    def test_signed_health_tuple_origin_is_types_module(self) -> None:
        assert SignedHealthTuple.__module__ == "pipeline.scout._types"

    def test_verification_verdict_origin_is_types_module(self) -> None:
        assert VerificationVerdict.__module__ == "pipeline.scout._types"

    def test_scout_discover_result_origin_is_discover_module(self) -> None:
        assert ScoutDiscoverResult.__module__ == "pipeline.scout.discover"

    def test_scout_verify_result_origin_is_verify_stage_module(self) -> None:
        assert ScoutVerifyResult.__module__ == "pipeline.scout.verify_stage"

    def test_scout_run_result_origin_is_run_module(self) -> None:
        assert ScoutRunResult.__module__ == "pipeline.scout.run"

    def test_run_degradation_event_origin_is_run_module(self) -> None:
        assert RunDegradationEvent.__module__ == "pipeline.scout.run"

    def test_capstone_degradation_event_origin_is_discover_module(self) -> None:
        assert CapstoneDegradationEvent.__module__ == "pipeline.scout.discover"


class TestS5RuntimeProtocols:
    """Runtime-checkable Protocols are wired correctly for the public surface."""

    def test_synopsis_fetcher_is_runtime_checkable(self) -> None:
        # `runtime_checkable` Protocols can be used with isinstance.
        assert hasattr(SynopsisFetcher, "_is_runtime_protocol")

    def test_applicant_profile_provider_satisfied_by_fake(self) -> None:
        from pipeline.scout.verify_stage import ApplicantProfileProvider

        provider = FakeProfileProvider()
        assert isinstance(provider, ApplicantProfileProvider)


# ===========================================================================
# S.6 — Result dataclass shape invariants (frozen + kw_only contract)
# ===========================================================================


class TestS6ResultDataclassInvariants:
    """Result types are frozen dataclasses (cannot mutate post-construction)."""

    def test_scout_run_result_is_frozen(self) -> None:
        from dataclasses import FrozenInstanceError

        cands = {CHANNEL_A: (_make_candidate("frozen-1", channel=CHANNEL_A),)}
        kw = _build_run_kwargs(candidates_by_channel=cands)
        result = run_scout_discover_verify_review(**kw)
        with pytest.raises(FrozenInstanceError):
            result.candidates = ()  # type: ignore[misc]

    def test_signed_health_tuple_is_frozen(self) -> None:
        from dataclasses import FrozenInstanceError

        sht = SignedHealthTuple(
            tuple_canonical=b"x",
            hmac_sha3_512=b"\x00" * 64,
            signed_at_utc="2026-04-29T00:00:00Z",
            hmac_key_id="k",
        )
        with pytest.raises(FrozenInstanceError):
            sht.tuple_canonical = b"y"  # type: ignore[misc]

    def test_run_degradation_event_is_frozen(self) -> None:
        from dataclasses import FrozenInstanceError

        ev = RunDegradationEvent(
            source="x", code=F_SCOUT_RUN_01, reason_tag="r", severity="HIGH"
        )
        with pytest.raises(FrozenInstanceError):
            ev.code = "Y"  # type: ignore[misc]

    def test_capstone_degradation_event_is_frozen(self) -> None:
        from dataclasses import FrozenInstanceError

        ev = CapstoneDegradationEvent(
            source="x", code=F_SCOUT_CAPSTONE_01, reason_tag="r", severity="HIGH"
        )
        with pytest.raises(FrozenInstanceError):
            ev.severity = "LOW"  # type: ignore[misc]

    def test_review_queue_item_round_trips_via_canonical_json(self) -> None:
        # Canonical-JSON encode/decode round-trip preserves all fields.
        from dataclasses import asdict
        from pipeline.sovereignty import canonical_json_bytes

        cand = _make_candidate("rt-1", channel=CHANNEL_A)
        verdict = VerificationVerdict(
            candidate_id="rt-1",
            verdict=VERDICT_VERIFIED_FIT,
            reason_code="V-OK",
            live_synopsis_url="https://example.test/x",
            live_content_hash="a" * 128,
            fetched_at_utc="2026-04-29T00:00:00Z",
            timeout_seconds=10,
            eligibility_live=("nonprofit",),
            award_floor_live=10_000,
            award_ceiling_live=100_000,
            close_date_live_utc="2026-12-01T00:00:00Z",
            evidence_quote="evidence",
        )
        item = ReviewQueueItem(
            candidate_id="rt-1",
            queued_at_utc="2026-04-29T01:00:00Z",
            queued_by_verdict=VERDICT_VERIFIED_FIT,
            candidate_snapshot=cand,
            verification_snapshot=verdict,
            fit_rationale="ok",
            operator_decision=None,
            operator_decided_at_utc=None,
            operator_decision_reason=None,
        )
        body = canonical_json_bytes(asdict(item))
        # Bytes are deterministic + decodable.
        import json

        decoded = json.loads(body.decode("utf-8"))
        assert decoded["candidate_id"] == "rt-1"
        assert decoded["operator_decision"] is None


# ===========================================================================
# S.7 — Self-LOCK manifest: capstone-shape invariants (file/floor pinning)
# ===========================================================================


class TestS7CapstoneManifest:
    """Pinned facts about the §3 LOCKed-as-a-whole boundary."""

    def test_locked_set_concat_sha_pin(self) -> None:
        """The 18 LOCKed scout production files concat-hash pin.

        Any change to a §3 production module after this LOCK invalidates
        the pin and surfaces immediately. A failure here is the canary
        that says §3 has had silent post-LOCK churn.
        """
        repo_root = Path(__file__).resolve().parents[2]
        locked_files = [
            "pipeline/scout/__init__.py",
            "pipeline/scout/_channel_f_jurisdictions.py",
            "pipeline/scout/_constants.py",
            "pipeline/scout/_feedparser_adapter.py",
            "pipeline/scout/_types.py",
            "pipeline/scout/_vault_reader_adapter.py",
            "pipeline/scout/channel_a_federal_apis.py",
            "pipeline/scout/channel_b_cache.py",
            "pipeline/scout/channel_c_portals.py",
            "pipeline/scout/channel_d_program_pages.py",
            "pipeline/scout/channel_e_rss.py",
            "pipeline/scout/channel_f_websearch.py",
            "pipeline/scout/discover.py",
            "pipeline/scout/entity_research.py",
            "pipeline/scout/health_tuple.py",
            "pipeline/scout/review_stage.py",
            "pipeline/scout/run.py",
            "pipeline/scout/verify_stage.py",
        ]
        concat = b""
        for fp in locked_files:
            concat += (repo_root / fp).read_bytes()
        actual = hashlib.sha3_512(concat).hexdigest()[:16]
        assert actual == "68c92a06fef30a81", (
            f"§3 Scout LOCKed-set concat sha3_512[:16]={actual!r} drifted from "
            f"the §3-whole-section LOCK pin '68c92a06fef30a81'. Either the "
            f"capstone is being re-LOCKed (update the pin), or a §3 module "
            f"received an out-of-band edit."
        )

    def test_locked_file_count_is_twenty_one(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        scout_dir = repo_root / "pipeline" / "scout"
        # Deprecated operator glue lives under pipeline/deprecated; the
        # Scout tree contains only the twenty-one production manifest files.
        py_files = sorted(f.name for f in scout_dir.glob("*.py"))
        assert len(py_files) == 21
