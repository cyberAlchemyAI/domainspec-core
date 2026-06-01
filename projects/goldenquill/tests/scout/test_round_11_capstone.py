"""Round 11 — §4.11 capstone-of-capstones (``pipeline.scout.run``).

Composition-heavy capstone test suite. Per-stage primitives carry their
own suites; this file targets composition invariants only — stage
sequencing, per-VERIFIED_FIT rationale fan-out, run-level checkpoint
discipline, AST invariants per blueprint §7.16.

Spec card: ``pipeline/engineering/spec_cards/scout_round_11_capstone.md``
v1. Floor ≥ 30 + adversarial ≥ 5 per handoff
``pipeline/handoffs/scout_round_11_capstone_dispatch_2026-04-21.md``.
"""

from __future__ import annotations

import ast
import re
import shutil
from dataclasses import FrozenInstanceError, dataclass, field, replace
from pathlib import Path
from typing import Any, Callable, List, Mapping, Optional, Tuple

import pytest

import pipeline.scout as scout_pkg
import pipeline.scout.run as run_module
from pipeline.scout._constants import (
    CHANNEL_A,
    CHANNEL_B,
    CHANNEL_C,
    CHANNEL_D,
    CHANNEL_E,
    CHANNEL_F,
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
from pipeline.scout.discover import (
    CapstoneDegradationEvent,
    ScoutDiscoverInterrupted,
    ScoutDiscoverResult,
)
from pipeline.scout.review_stage import ReviewEnqueueRejected
from pipeline.scout.run import (
    BLUEPRINT_DEPS,
    F_SCOUT_RUN_01,
    F_SCOUT_RUN_02,
    F_SCOUT_RUN_03,
    F_SCOUT_RUN_04,
    F_SCOUT_RUN_05,
    MAX_FIT_RATIONALE_BYTES,
    BuildFitRationale,
    RationaleBudgetExceeded,
    RationaleBuildFailed,
    RunDegradationEvent,
    ScoutRunInterrupted,
    ScoutRunResult,
    _build_fit_rationale,
    run_scout_discover_verify,
    run_scout_discover_verify_review,
)
from pipeline.scout.verify_stage import (
    ScoutVerifyInterrupted,
    ScoutVerifyResult,
    VERIFY_STAGE_OK,
)


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


@dataclass
class FakeSession:
    session_id: str = "session-r11-abc"
    slug: str = "mycosymbiotics_cooperative"
    operator_id: str = "josh"


@dataclass
class WriteCall:
    path: str
    bytes_: bytes
    intent: str
    session_id: str
    slug: str


@dataclass
class RecordingVaultWriter:
    calls: List[WriteCall] = field(default_factory=list)
    raise_with: Optional[BaseException] = None

    def write(
        self,
        *,
        path: str,
        bytes_: bytes,
        intent: str,
        session_id: str,
        slug: str,
    ) -> None:
        if self.raise_with is not None:
            raise self.raise_with
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
    """One checkpoint sink — works for discover / verify / review writers."""

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


def _mk_candidate(cid: str = "cid-001", *, channel: str = "A", title: str = "Opp") -> Candidate:
    return Candidate(
        candidate_id=cid,
        channel=channel,
        feed_or_adapter_id=f"api:{channel.lower()}",
        source_key=f"src-{cid}",
        title=title,
        funder="Some Funder",
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
        fit_score_cached=80,
        cache_provenance=None,
    )


def _mk_verdict(
    *,
    cid: str = "cid-001",
    verdict: str = VERDICT_VERIFIED_FIT,
    reason: str = "V-OK",
) -> VerificationVerdict:
    return VerificationVerdict(
        candidate_id=cid,
        verdict=verdict,
        reason_code=reason,
        live_synopsis_url="https://example.test/live",
        live_content_hash="a" * 128,
        fetched_at_utc="2026-04-20T01:00:00Z",
        timeout_seconds=10,
        eligibility_live=("nonprofit",),
        award_floor_live=50_000,
        award_ceiling_live=500_000,
        close_date_live_utc="2026-12-01T00:00:00Z",
        evidence_quote="excellent fit indicator",
    )


def _mk_signed_health() -> SignedHealthTuple:
    return SignedHealthTuple(
        tuple_canonical=b"{}",
        hmac_sha3_512=b"\x00" * 64,
        signed_at_utc="2026-04-20T02:00:00Z",
        hmac_key_id="key-r11",
    )


def _mk_discover_result(
    candidates: tuple[Candidate, ...],
    *,
    run_id: str = "0123456789abcdef01234567",
    capstone_events: tuple[CapstoneDegradationEvent, ...] = (),
) -> ScoutDiscoverResult:
    return ScoutDiscoverResult(
        candidates=candidates,
        per_channel_states={
            CHANNEL_A: HEALTH_OK,
            CHANNEL_B: HEALTH_OK,
            CHANNEL_C: HEALTH_OK,
            CHANNEL_D: HEALTH_OK,
            CHANNEL_E: HEALTH_OK,
            CHANNEL_F: HEALTH_OK,
        },
        per_channel_a_endpoints={
            "grants.gov": HEALTH_OK,
            "sam.gov": HEALTH_OK,
            "usaspending.gov": HEALTH_OK,
        },
        signed_health=_mk_signed_health(),
        run_id=run_id,
        run_tiebreak_seed=b"\x01" * 16,
        run_wall_ns=1_700_000_000_000_000_000,
        capstone_degradation_events=capstone_events,
    )


def _mk_verify_result(
    verdicts: dict[str, VerificationVerdict],
    *,
    state: str = VERIFY_STAGE_OK,
    overflow: int = 0,
) -> ScoutVerifyResult:
    return ScoutVerifyResult(
        verdicts=verdicts,
        verify_stage_state=state,
        cap_applied=overflow > 0,
        overflow=overflow,
        verify_degradation_events=(),
    )


def _channel_fns_dummy() -> dict[str, Any]:
    """Dispatcher map with all six required keys; values not invoked when
    DISCOVER is patched to return a canned ``ScoutDiscoverResult``."""
    return {ch: (lambda: None) for ch in (CHANNEL_A, CHANNEL_B, CHANNEL_C, CHANNEL_D, CHANNEL_E, CHANNEL_F)}


@dataclass
class StagePatch:
    """Patches `run_scout_discover` and `verify_all` in ``pipeline.scout.run``
    via monkeypatch — bypasses the per-stage primitives so R11 tests assert
    composition behavior without depending on R8/R9 internals.

    Each patch records the call kwargs it received so sequencing tests can
    assert order + propagation.
    """

    discover_calls: List[Mapping[str, Any]] = field(default_factory=list)
    verify_calls: List[Mapping[str, Any]] = field(default_factory=list)
    discover_return: Optional[ScoutDiscoverResult] = None
    verify_return: Optional[ScoutVerifyResult] = None
    discover_raise: Optional[BaseException] = None
    verify_raise: Optional[BaseException] = None

    def install(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def _fake_discover(**kwargs: Any) -> ScoutDiscoverResult:
            self.discover_calls.append(dict(kwargs))
            if self.discover_raise is not None:
                raise self.discover_raise
            assert self.discover_return is not None
            return self.discover_return

        def _fake_verify(**kwargs: Any) -> ScoutVerifyResult:
            self.verify_calls.append(dict(kwargs))
            if self.verify_raise is not None:
                raise self.verify_raise
            assert self.verify_return is not None
            return self.verify_return

        monkeypatch.setattr(run_module, "run_scout_discover", _fake_discover)
        monkeypatch.setattr(run_module, "verify_all", _fake_verify)


# ---------------------------------------------------------------------------
# Constants + public-surface tests
# ---------------------------------------------------------------------------


class TestConstantsAndPublicSurface:
    def test_max_fit_rationale_bytes_pin(self) -> None:
        assert MAX_FIT_RATIONALE_BYTES == 4096

    def test_failure_codes_are_distinct(self) -> None:
        codes = {F_SCOUT_RUN_01, F_SCOUT_RUN_02, F_SCOUT_RUN_03, F_SCOUT_RUN_04, F_SCOUT_RUN_05}
        assert len(codes) == 5

    def test_failure_codes_have_run_namespace(self) -> None:
        for c in (F_SCOUT_RUN_01, F_SCOUT_RUN_02, F_SCOUT_RUN_03, F_SCOUT_RUN_04, F_SCOUT_RUN_05):
            assert c.startswith("F-SCOUT-RUN-")

    def test_blueprint_deps_pin(self) -> None:
        anchor = BLUEPRINT_DEPS["section_03_scout.md"]
        assert anchor["hash_sha3_512_prefix16"] == "0a82d955f95b0fca"

    def test_run_module_version_pin(self) -> None:
        m = re.match(r"^0\.1\.0-scout-r(\d+)$", run_module.__version__)
        assert m is not None
        assert int(m.group(1)) >= 11

    def test_scout_pkg_version_pin(self) -> None:
        m = re.match(r"^0\.1\.0-scout-r(\d+)$", scout_pkg.__version__)
        assert m is not None
        assert int(m.group(1)) >= 11

    def test_alias_is_identity(self) -> None:
        assert run_scout_discover_verify is run_scout_discover_verify_review

    def test_module_lineage(self) -> None:
        assert run_scout_discover_verify_review.__module__ == "pipeline.scout.run"
        assert ScoutRunResult.__module__ == "pipeline.scout.run"
        assert RunDegradationEvent.__module__ == "pipeline.scout.run"

    def test_public_surface_reachable_via_pkg(self) -> None:
        for name in (
            "BuildFitRationale",
            "F_SCOUT_RUN_01",
            "F_SCOUT_RUN_02",
            "F_SCOUT_RUN_03",
            "F_SCOUT_RUN_04",
            "F_SCOUT_RUN_05",
            "MAX_FIT_RATIONALE_BYTES",
            "RationaleBudgetExceeded",
            "RationaleBuildFailed",
            "RunDegradationEvent",
            "ScoutRunInterrupted",
            "ScoutRunResult",
            "run_scout_discover_verify",
            "run_scout_discover_verify_review",
        ):
            assert hasattr(scout_pkg, name), f"missing: {name}"

    def test_default_rationale_is_module_local_not_pkg_exported(self) -> None:
        """`_build_fit_rationale` is the implementation symbol per blueprint
        §4.11 line 1067 (underscore prefix). It is NOT exported via
        ``pipeline.scout.__all__`` — custom builders bind via the
        ``build_fit_rationale`` kwarg + ``BuildFitRationale`` Protocol.
        """
        # Must NOT appear in either __all__ list.
        assert "_build_fit_rationale" not in run_module.__all__
        assert "_build_fit_rationale" not in scout_pkg.__all__
        # The symbol still exists on the module for callers that import
        # from pipeline.scout.run directly (production wiring).
        assert hasattr(run_module, "_build_fit_rationale")

    def test_run_module_all_matches_documented_surface(self) -> None:
        documented = {
            "BLUEPRINT_DEPS",
            "BuildFitRationale",
            "F_SCOUT_RUN_01",
            "F_SCOUT_RUN_02",
            "F_SCOUT_RUN_03",
            "F_SCOUT_RUN_04",
            "F_SCOUT_RUN_05",
            "MAX_FIT_RATIONALE_BYTES",
            "RationaleBudgetExceeded",
            "RationaleBuildFailed",
            "RunDegradationEvent",
            "ScoutRunInterrupted",
            "ScoutRunResult",
            "SEVERITY_HIGH",
            "SEVERITY_LOW",
            "SEVERITY_MEDIUM",
            "__version__",
            "run_scout_discover_verify",
            "run_scout_discover_verify_review",
        }
        assert set(run_module.__all__) == documented


# ---------------------------------------------------------------------------
# Default _build_fit_rationale tests
# ---------------------------------------------------------------------------


class TestDefaultBuildFitRationale:
    def test_returns_str(self) -> None:
        s = FakeSession()
        c = _mk_candidate()
        v = _mk_verdict()
        out = _build_fit_rationale(session=s, candidate=c, verdict=v)
        assert isinstance(out, str)

    def test_handles_none_fields(self) -> None:
        """Candidate/Verdict fields that are None render as the placeholder
        glyph (`—`); does not raise and stays under budget.
        """
        s = FakeSession()
        c = replace(
            _mk_candidate(),
            close_date_utc=None,
            award_floor=None,
            award_ceiling=None,
        )
        v = replace(
            _mk_verdict(),
            live_synopsis_url=None,
            fetched_at_utc=None,
            evidence_quote=None,
        )
        out = _build_fit_rationale(session=s, candidate=c, verdict=v)
        assert isinstance(out, str)
        # placeholder glyph appears for the None fields
        assert "—" in out
        assert len(out.encode("utf-8")) <= MAX_FIT_RATIONALE_BYTES

    def test_is_deterministic(self) -> None:
        s = FakeSession()
        c = _mk_candidate()
        v = _mk_verdict()
        out_1 = _build_fit_rationale(session=s, candidate=c, verdict=v)
        out_2 = _build_fit_rationale(session=s, candidate=c, verdict=v)
        assert out_1 == out_2

    def test_contains_candidate_id_verdict_funder(self) -> None:
        s = FakeSession()
        c = _mk_candidate(cid="cid-zz")
        v = _mk_verdict(cid="cid-zz", reason="V-OK")
        out = _build_fit_rationale(session=s, candidate=c, verdict=v)
        assert "cid-zz" in out
        assert "V-OK" in out
        assert "Some Funder" in out
        assert "federal" in out

    def test_under_byte_budget_for_long_inputs(self) -> None:
        s = FakeSession(slug="x" * 1000)
        c = _mk_candidate()
        c = replace(c, title="A" * 5000, funder="B" * 5000, url="C" * 5000)
        v = _mk_verdict()
        v = replace(v, evidence_quote="D" * 5000, live_synopsis_url="E" * 5000)
        out = _build_fit_rationale(session=s, candidate=c, verdict=v)
        assert len(out.encode("utf-8")) <= MAX_FIT_RATIONALE_BYTES


# ---------------------------------------------------------------------------
# Composition / sequencing tests
# ---------------------------------------------------------------------------


def _run_kwargs(
    *,
    session: Optional[FakeSession] = None,
    channel_fns: Optional[Mapping[str, Any]] = None,
    rationale_builder: Optional[Callable[..., str]] = None,
    interrupt_probe_run: Optional[Callable[[], bool]] = None,
    vault_raise: Optional[BaseException] = None,
) -> dict[str, Any]:
    """Common kwargs for run.py invocation under StagePatch."""
    return {
        "session": session or FakeSession(),
        "channel_fns": channel_fns or _channel_fns_dummy(),
        "synopsis_fetcher": object(),
        "applicant_profile_provider": object(),
        "vault_writer": RecordingVaultWriter(raise_with=vault_raise),
        "health_signer": object(),
        "checkpoint_writer_discover": RecordingCheckpoint("discover"),
        "checkpoint_writer_verify": RecordingCheckpoint("verify"),
        "checkpoint_writer_review": RecordingCheckpoint("review"),
        "degradation_writer_discover": RecordingDegradation("discover"),
        "degradation_writer_verify": RecordingDegradation("verify"),
        "build_fit_rationale": rationale_builder if rationale_builder is not None else _build_fit_rationale,
        "interrupt_probe_run": interrupt_probe_run,
    }


class TestRunHappyPath:
    def test_end_to_end_one_verified_fit(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="fit-001")
        verdict = _mk_verdict(cid="fit-001")
        patch = StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"fit-001": verdict}),
        )
        patch.install(monkeypatch)
        kw = _run_kwargs()
        result = run_scout_discover_verify_review(**kw)
        assert isinstance(result, ScoutRunResult)
        assert len(result.review_queue_items) == 1
        assert result.review_queue_items[0].candidate_id == "fit-001"
        assert "fit-001" in result.fit_rationales
        assert len(kw["vault_writer"].calls) == 1

    def test_propagates_discover_fields_unchanged(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="fit-002")
        d = _mk_discover_result((cand,), run_id="abcdef0123456789abcdef01")
        v = _mk_verify_result({"fit-002": _mk_verdict(cid="fit-002")})
        StagePatch(discover_return=d, verify_return=v).install(monkeypatch)
        result = run_scout_discover_verify_review(**_run_kwargs())
        assert result.run_id == d.run_id
        assert result.run_wall_ns == d.run_wall_ns
        assert result.run_tiebreak_seed == d.run_tiebreak_seed
        assert result.signed_health is d.signed_health
        assert result.candidates is d.candidates
        assert dict(result.per_channel_states) == dict(d.per_channel_states)
        assert dict(result.per_channel_a_endpoints) == dict(d.per_channel_a_endpoints)
        assert result.discover_capstone_events is d.capstone_degradation_events

    def test_propagates_verify_fields_unchanged(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="fit-003")
        verdicts = {"fit-003": _mk_verdict(cid="fit-003")}
        v = _mk_verify_result(verdicts, overflow=42, state=VERIFY_STAGE_OK)
        StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=v,
        ).install(monkeypatch)
        result = run_scout_discover_verify_review(**_run_kwargs())
        assert result.verify_stage_state == VERIFY_STAGE_OK
        assert result.verify_overflow == 42
        assert result.verify_degradation_events == ()
        assert dict(result.verdicts) == verdicts

    def test_stage_order_discover_then_verify_then_review(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="fit-ord-1")
        verdict = _mk_verdict(cid="fit-ord-1")
        patch = StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"fit-ord-1": verdict}),
        )
        patch.install(monkeypatch)
        kw = _run_kwargs()
        run_scout_discover_verify_review(**kw)
        # review checkpoint sees run_review_start AFTER verify call.
        review_stages = kw["checkpoint_writer_review"].stages()
        assert "run_review_start" in review_stages
        assert "run_review_complete" in review_stages
        assert review_stages.index("run_review_start") < review_stages.index(
            "run_review_complete"
        )
        assert len(patch.discover_calls) == 1
        assert len(patch.verify_calls) == 1


class TestRunSkipsNonFitVerdicts:
    @pytest.mark.parametrize(
        "verdict_value",
        [
            VERDICT_VERIFIED_NOT_FIT,
            VERDICT_UNVERIFIED,
            VERDICT_VERIFICATION_FAILED,
        ],
    )
    def test_no_enqueue_for_non_verified_fit(
        self, monkeypatch: pytest.MonkeyPatch, verdict_value: str
    ) -> None:
        cand = _mk_candidate(cid="not-fit")
        verdict = _mk_verdict(cid="not-fit", verdict=verdict_value)
        StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"not-fit": verdict}),
        ).install(monkeypatch)
        kw = _run_kwargs()
        result = run_scout_discover_verify_review(**kw)
        assert len(result.review_queue_items) == 0
        assert "not-fit" not in result.fit_rationales
        assert len(kw["vault_writer"].calls) == 0


class TestRunRationaleFanOut:
    def test_rationale_built_once_per_verified_fit(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand_a = _mk_candidate(cid="fit-A", channel="A")
        cand_b = _mk_candidate(cid="not-fit", channel="B")
        cand_c = _mk_candidate(cid="fit-C", channel="C")
        verdicts = {
            "fit-A": _mk_verdict(cid="fit-A"),
            "not-fit": _mk_verdict(cid="not-fit", verdict=VERDICT_UNVERIFIED),
            "fit-C": _mk_verdict(cid="fit-C"),
        }
        StagePatch(
            discover_return=_mk_discover_result((cand_a, cand_b, cand_c)),
            verify_return=_mk_verify_result(verdicts),
        ).install(monkeypatch)
        calls: List[str] = []

        def builder(*, session, candidate, verdict):
            calls.append(candidate.candidate_id)
            return f"rationale-for-{candidate.candidate_id}"

        kw = _run_kwargs(rationale_builder=builder)
        result = run_scout_discover_verify_review(**kw)
        assert calls == ["fit-A", "fit-C"]
        assert set(result.fit_rationales) == {"fit-A", "fit-C"}

    def test_rationale_budget_exceeded_skips_enqueue(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="oversize")
        StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"oversize": _mk_verdict(cid="oversize")}),
        ).install(monkeypatch)
        kw = _run_kwargs(rationale_builder=lambda **_: "x" * (MAX_FIT_RATIONALE_BYTES + 1))
        result = run_scout_discover_verify_review(**kw)
        assert len(result.review_queue_items) == 0
        assert "oversize" not in result.fit_rationales
        assert len(result.run_degradation_events) == 1
        assert result.run_degradation_events[0].code == F_SCOUT_RUN_01
        assert "rationale_oversize" in (result.run_degradation_events[0].reason_tag or "")
        assert len(kw["vault_writer"].calls) == 0

    def test_rationale_at_budget_is_accepted(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="atbudget")
        StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"atbudget": _mk_verdict(cid="atbudget")}),
        ).install(monkeypatch)
        kw = _run_kwargs(rationale_builder=lambda **_: "x" * MAX_FIT_RATIONALE_BYTES)
        result = run_scout_discover_verify_review(**kw)
        assert len(result.review_queue_items) == 1
        assert len(result.fit_rationales["atbudget"].encode("utf-8")) == MAX_FIT_RATIONALE_BYTES
        assert len(result.run_degradation_events) == 0

    def test_rationale_build_failed_logged(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="boom")
        StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"boom": _mk_verdict(cid="boom")}),
        ).install(monkeypatch)

        def bad_builder(**_):
            raise ValueError("bad rationale state")

        kw = _run_kwargs(rationale_builder=bad_builder)
        result = run_scout_discover_verify_review(**kw)
        assert len(result.review_queue_items) == 0
        assert "boom" not in result.fit_rationales
        assert len(result.run_degradation_events) == 1
        ev = result.run_degradation_events[0]
        assert ev.code == F_SCOUT_RUN_02
        assert ev.candidate_id == "boom"
        assert "ValueError" in (ev.reason_tag or "")
        assert "bad rationale state" in (ev.reason_tag or "")

    def test_rationale_keyboard_interrupt_propagates(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="kbd")
        StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"kbd": _mk_verdict(cid="kbd")}),
        ).install(monkeypatch)

        def kbd_builder(**_):
            raise KeyboardInterrupt()

        kw = _run_kwargs(rationale_builder=kbd_builder)
        with pytest.raises(KeyboardInterrupt):
            run_scout_discover_verify_review(**kw)
        review_stages = kw["checkpoint_writer_review"].stages()
        # run_review_start fired; run_review_complete must NOT have fired
        # (KeyboardInterrupt re-raises before either failure or success
        # complete-checkpoint).
        assert "run_review_start" in review_stages
        assert all(
            "complete" not in stage or stage == "run_review_start"
            for stage in review_stages
            if stage.startswith("run_review_")
        )

    def test_rationale_system_exit_propagates(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="sysexit")
        StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"sysexit": _mk_verdict(cid="sysexit")}),
        ).install(monkeypatch)

        def sysexit_builder(**_):
            raise SystemExit(1)

        kw = _run_kwargs(rationale_builder=sysexit_builder)
        with pytest.raises(SystemExit):
            run_scout_discover_verify_review(**kw)


class TestRunChannelDispatchValidation:
    @pytest.mark.parametrize("missing_key", [CHANNEL_A, CHANNEL_C, CHANNEL_F])
    def test_missing_key_raises_before_any_work(
        self, monkeypatch: pytest.MonkeyPatch, missing_key: str
    ) -> None:
        # Patch stages so any accidental dispatch is detected.
        StagePatch(
            discover_return=_mk_discover_result(()),
            verify_return=_mk_verify_result({}),
        ).install(monkeypatch)
        ch = _channel_fns_dummy()
        del ch[missing_key]
        kw = _run_kwargs(channel_fns=ch)
        with pytest.raises(KeyError) as exc:
            run_scout_discover_verify_review(**kw)
        assert F_SCOUT_RUN_03 in str(exc.value)
        assert missing_key in str(exc.value)
        # Discover/verify must not have been called.
        assert kw["checkpoint_writer_discover"].calls == []
        assert kw["checkpoint_writer_verify"].calls == []

    def test_dispatch_with_extra_key_accepted(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        StagePatch(
            discover_return=_mk_discover_result(()),
            verify_return=_mk_verify_result({}),
        ).install(monkeypatch)
        ch = _channel_fns_dummy()
        ch["X"] = lambda: None
        kw = _run_kwargs(channel_fns=ch)
        result = run_scout_discover_verify_review(**kw)
        assert isinstance(result, ScoutRunResult)


class TestRunCheckpointDiscipline:
    def test_run_review_start_and_complete_on_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="ck-1")
        StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"ck-1": _mk_verdict(cid="ck-1")}),
        ).install(monkeypatch)
        kw = _run_kwargs()
        run_scout_discover_verify_review(**kw)
        stages = kw["checkpoint_writer_review"].stages()
        starts = [i for i, s in enumerate(stages) if s == "run_review_start"]
        completes = [i for i, s in enumerate(stages) if s == "run_review_complete"]
        assert len(starts) == 1
        assert len(completes) == 1
        assert starts[0] < completes[0]
        complete_payload = kw["checkpoint_writer_review"].calls[completes[0]][1]
        assert complete_payload["outcome"] == "success"
        assert complete_payload["n_review_items"] == 1

    def test_complete_checkpoint_carries_run_id(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="ck-2")
        d = _mk_discover_result((cand,), run_id="abcdef0123456789abcdef01")
        StagePatch(
            discover_return=d,
            verify_return=_mk_verify_result({"ck-2": _mk_verdict(cid="ck-2")}),
        ).install(monkeypatch)
        kw = _run_kwargs()
        run_scout_discover_verify_review(**kw)
        complete = next(
            payload
            for stage, payload in kw["checkpoint_writer_review"].calls
            if stage == "run_review_complete"
        )
        assert complete["run_id"] == d.run_id

    def test_failure_at_verify_writes_run_review_complete_failure(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        StagePatch(
            discover_return=_mk_discover_result((_mk_candidate(),)),
            verify_raise=RuntimeError("verify exploded"),
        ).install(monkeypatch)
        kw = _run_kwargs()
        with pytest.raises(RuntimeError, match="verify exploded"):
            run_scout_discover_verify_review(**kw)
        stages = kw["checkpoint_writer_review"].stages()
        assert "run_review_complete" in stages
        complete = next(
            payload
            for stage, payload in kw["checkpoint_writer_review"].calls
            if stage == "run_review_complete"
        )
        assert complete["outcome"] == "verify_failed"

    def test_failure_at_discover_writes_run_review_complete_failure(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        StagePatch(
            discover_raise=RuntimeError("discover exploded"),
        ).install(monkeypatch)
        kw = _run_kwargs()
        with pytest.raises(RuntimeError, match="discover exploded"):
            run_scout_discover_verify_review(**kw)
        complete = next(
            payload
            for stage, payload in kw["checkpoint_writer_review"].calls
            if stage == "run_review_complete"
        )
        assert complete["outcome"] == "discover_failed"
        assert complete["code"] == F_SCOUT_RUN_05


class TestRunInterrupt:
    def test_interrupt_between_verified_fit_candidates(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand_1 = _mk_candidate(cid="cid-1")
        cand_2 = _mk_candidate(cid="cid-2", channel="B")
        verdicts = {
            "cid-1": _mk_verdict(cid="cid-1"),
            "cid-2": _mk_verdict(cid="cid-2"),
        }
        StagePatch(
            discover_return=_mk_discover_result((cand_1, cand_2)),
            verify_return=_mk_verify_result(verdicts),
        ).install(monkeypatch)

        # First call (before cid-1) → False; second call (before cid-2) → True.
        flips = iter([False, True, True, True])
        probe = lambda: next(flips)
        kw = _run_kwargs(interrupt_probe_run=probe)
        with pytest.raises(ScoutRunInterrupted) as exc:
            run_scout_discover_verify_review(**kw)
        assert exc.value.completed_candidate_ids == ("cid-1",)
        # Vault writer saw exactly one write (cid-1) before interrupt.
        assert len(kw["vault_writer"].calls) == 1
        # run_review_interrupted checkpoint payload carries the right ids.
        interrupt_payload = next(
            payload
            for stage, payload in kw["checkpoint_writer_review"].calls
            if stage == "run_review_interrupted"
        )
        assert interrupt_payload["completed_candidate_ids"] == ["cid-1"]
        assert interrupt_payload["pending_candidate_id"] == "cid-2"

    def test_discover_interrupt_propagates_unchanged(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        StagePatch(
            discover_raise=ScoutDiscoverInterrupted(("A",)),
        ).install(monkeypatch)
        kw = _run_kwargs()
        with pytest.raises(ScoutDiscoverInterrupted):
            run_scout_discover_verify_review(**kw)
        # Capstone did NOT add its own complete-failure checkpoint for
        # ScoutDiscoverInterrupted (per-stage interrupt is the stage's
        # responsibility).
        assert "run_review_complete" not in kw["checkpoint_writer_review"].stages()

    def test_verify_interrupt_propagates_unchanged(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        StagePatch(
            discover_return=_mk_discover_result(()),
            verify_raise=ScoutVerifyInterrupted(()),
        ).install(monkeypatch)
        kw = _run_kwargs()
        with pytest.raises(ScoutVerifyInterrupted):
            run_scout_discover_verify_review(**kw)
        assert "run_review_complete" not in kw["checkpoint_writer_review"].stages()


# ---------------------------------------------------------------------------
# Result shape tests
# ---------------------------------------------------------------------------


class TestScoutRunResult:
    def test_is_frozen(self) -> None:
        cand = _mk_candidate()
        d = _mk_discover_result((cand,))
        v = _mk_verify_result({"cid-001": _mk_verdict()})
        result = ScoutRunResult(
            candidates=d.candidates,
            verdicts=v.verdicts,
            signed_health=d.signed_health,
            run_id=d.run_id,
            run_tiebreak_seed=d.run_tiebreak_seed,
            run_wall_ns=d.run_wall_ns,
            per_channel_states=d.per_channel_states,
            per_channel_a_endpoints=d.per_channel_a_endpoints,
            discover_capstone_events=d.capstone_degradation_events,
            verify_stage_state=v.verify_stage_state,
            verify_overflow=v.overflow,
            verify_degradation_events=v.verify_degradation_events,
            review_queue_items=(),
            fit_rationales={},
            run_degradation_events=(),
        )
        with pytest.raises(FrozenInstanceError):
            result.candidates = ()  # type: ignore[misc]

    def test_run_degradation_event_is_frozen(self) -> None:
        ev = RunDegradationEvent(
            source="x", code=F_SCOUT_RUN_01, reason_tag="r", severity="HIGH"
        )
        with pytest.raises(FrozenInstanceError):
            ev.code = "Y"  # type: ignore[misc]

    def test_review_queue_items_preserve_candidate_order(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cands = (
            _mk_candidate(cid="cid-z"),
            _mk_candidate(cid="cid-a"),
            _mk_candidate(cid="cid-m"),
        )
        verdicts = {c.candidate_id: _mk_verdict(cid=c.candidate_id) for c in cands}
        StagePatch(
            discover_return=_mk_discover_result(cands),
            verify_return=_mk_verify_result(verdicts),
        ).install(monkeypatch)
        result = run_scout_discover_verify_review(**_run_kwargs())
        assert tuple(it.candidate_id for it in result.review_queue_items) == (
            "cid-z", "cid-a", "cid-m",
        )

    def test_fit_rationales_excludes_non_fit(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cands = (
            _mk_candidate(cid="cid-fit"),
            _mk_candidate(cid="cid-nf"),
        )
        verdicts = {
            "cid-fit": _mk_verdict(cid="cid-fit"),
            "cid-nf": _mk_verdict(cid="cid-nf", verdict=VERDICT_VERIFIED_NOT_FIT),
        }
        StagePatch(
            discover_return=_mk_discover_result(cands),
            verify_return=_mk_verify_result(verdicts),
        ).install(monkeypatch)
        result = run_scout_discover_verify_review(**_run_kwargs())
        assert set(result.fit_rationales.keys()) == {"cid-fit"}


# ---------------------------------------------------------------------------
# AST regression invariants (§7.16)
# ---------------------------------------------------------------------------


class TestASTNoLLMImports:
    """``pipeline/scout/run.py`` must NOT import any LLM provider module.
    Spec-card §7.16 — LLM imports are confined to deployment-supplied
    ``BuildFitRationale`` implementations, which live OUTSIDE the Scout
    package. The module must remain stdlib + intra-package only.
    """

    LLM_MODULES = {
        "anthropic",
        "openai",
        "google.generativeai",
        "google_generativeai",
        "groq",
        "ollama",
        "litellm",
    }

    def test_no_top_level_import(self) -> None:
        path = Path(__file__).resolve().parents[2] / "pipeline" / "scout" / "run.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name not in self.LLM_MODULES, (
                        f"forbidden top-level import: {alias.name}"
                    )
            if isinstance(node, ast.ImportFrom):
                if node.module is not None:
                    assert node.module not in self.LLM_MODULES, (
                        f"forbidden ImportFrom: {node.module}"
                    )


class TestASTNoSetattrOperatorDecisionInRun:
    """Per §7.16 / R10 invariant: only ``record_operator_decision`` may
    write the ``operator_decision`` field. The capstone must not contain
    any attribute-store nor ``setattr(..., "operator_decision", ...)``
    targeting that attribute.
    """

    def test_no_assign_no_setattr(self) -> None:
        path = Path(__file__).resolve().parents[2] / "pipeline" / "scout" / "run.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Attribute) and target.attr == "operator_decision":
                        pytest.fail(f"forbidden Assign to .operator_decision at line {node.lineno}")
            if isinstance(node, ast.AugAssign):
                if isinstance(node.target, ast.Attribute) and node.target.attr == "operator_decision":
                    pytest.fail(f"forbidden AugAssign to .operator_decision at line {node.lineno}")
            if isinstance(node, ast.Call):
                func = node.func
                # setattr(item, "operator_decision", X)
                if (
                    isinstance(func, ast.Name)
                    and func.id == "setattr"
                    and len(node.args) >= 3
                    and isinstance(node.args[1], ast.Constant)
                    and node.args[1].value == "operator_decision"
                ):
                    pytest.fail(f"forbidden setattr(operator_decision) at line {node.lineno}")


class TestASTNoEvalExecCompileInRun:
    def test_no_eval_exec_compile(self) -> None:
        path = Path(__file__).resolve().parents[2] / "pipeline" / "scout" / "run.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in {"eval", "exec", "compile"}, (
                    f"forbidden builtin call {node.func.id} at line {node.lineno}"
                )


class TestASTNoOpenInRun:
    """Per §7.16 — direct filesystem I/O must not appear in
    ``pipeline/scout/run.py``. All persistence flows through injected
    Protocols.
    """

    def test_no_open_no_path_io(self) -> None:
        path = Path(__file__).resolve().parents[2] / "pipeline" / "scout" / "run.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        forbidden = {"open"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id in forbidden:
                    pytest.fail(f"forbidden bare {func.id}() at line {node.lineno}")
                if isinstance(func, ast.Attribute):
                    # forbid Path(...).read_text / Path(...).write_text /
                    # os.open / os.write / os.read at the run.py layer.
                    if func.attr in {"read_text", "write_text"}:
                        pytest.fail(
                            f"forbidden {func.attr} at line {node.lineno}"
                        )
                    if isinstance(func.value, ast.Name) and func.value.id == "os":
                        if func.attr in {"open", "write", "read", "fdopen"}:
                            pytest.fail(
                                f"forbidden os.{func.attr} at line {node.lineno}"
                            )


class TestASTLintCleanRun:
    """E-027 directory-contract — copy ``run.py`` into a tmp-tree with
    empty ``__init__.py`` and run ``lint_tree`` over the directory. R1-R7
    must report zero violations.
    """

    def test_lint_tree_clean(self, tmp_path: Path) -> None:
        from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree

        scout_dir = tmp_path / "pipeline" / "scout"
        scout_dir.mkdir(parents=True)
        (tmp_path / "pipeline" / "__init__.py").write_text("")
        (scout_dir / "__init__.py").write_text("")
        src = Path(__file__).resolve().parents[2] / "pipeline" / "scout" / "run.py"
        shutil.copy(src, scout_dir / "run.py")
        violations = lint_tree(tmp_path, DEFAULT_RULES)
        assert violations == [], f"AST-lint violations: {violations}"


# ---------------------------------------------------------------------------
# Adversarial tests
# ---------------------------------------------------------------------------


class TestAdv:
    def test_adv_rationale_byte_count_over_not_char(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Emoji-heavy strings: byte count > char count. A ~1500-emoji
        string is well under 4096 chars but well over 4096 bytes.
        """
        cand = _mk_candidate(cid="emoji")
        StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"emoji": _mk_verdict(cid="emoji")}),
        ).install(monkeypatch)
        emoji = "🌱"  # 4 UTF-8 bytes per char
        oversize_bytes = "\n" + emoji * 1200
        # confirm test fixture: char count well under cap, byte count over.
        assert len(oversize_bytes) < MAX_FIT_RATIONALE_BYTES
        assert len(oversize_bytes.encode("utf-8")) > MAX_FIT_RATIONALE_BYTES
        kw = _run_kwargs(rationale_builder=lambda **_: oversize_bytes)
        result = run_scout_discover_verify_review(**kw)
        assert result.run_degradation_events[0].code == F_SCOUT_RUN_01

    def test_adv_simultaneous_rationale_and_enqueue_failure(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Candidate A → rationale build raises (recorded; skipped).
        Candidate B → vault_writer raises (run aborts on B).
        """
        cand_a = _mk_candidate(cid="cid-A")
        cand_b = _mk_candidate(cid="cid-B", channel="B")
        verdicts = {
            "cid-A": _mk_verdict(cid="cid-A"),
            "cid-B": _mk_verdict(cid="cid-B"),
        }
        StagePatch(
            discover_return=_mk_discover_result((cand_a, cand_b)),
            verify_return=_mk_verify_result(verdicts),
        ).install(monkeypatch)

        def rationale(*, session, candidate, verdict):
            if candidate.candidate_id == "cid-A":
                raise ValueError("A bad")
            return f"ok-{candidate.candidate_id}"

        kw = _run_kwargs(
            rationale_builder=rationale,
            vault_raise=RuntimeError("vault exploded"),
        )
        with pytest.raises(RuntimeError, match="vault exploded"):
            run_scout_discover_verify_review(**kw)
        # run_review_complete with outcome=review_failed
        complete_payload = next(
            payload
            for stage, payload in kw["checkpoint_writer_review"].calls
            if stage == "run_review_complete"
        )
        assert complete_payload["outcome"] == "review_failed"
        # Cand-A must have its degradation event recorded; we cannot verify
        # via ScoutRunResult because the call raised, but the kw dict's
        # vault_writer was never called (the writer raised on first attempt).
        assert kw["vault_writer"].calls == []

    def test_adv_rationale_replay_deterministic(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Two runs with identical inputs produce identical default
        rationales (replay invariant).
        """
        cand = _mk_candidate(cid="replay")
        verdict = _mk_verdict(cid="replay")
        d = _mk_discover_result((cand,))
        v = _mk_verify_result({"replay": verdict})

        StagePatch(discover_return=d, verify_return=v).install(monkeypatch)
        kw = _run_kwargs()
        result1 = run_scout_discover_verify_review(**kw)
        rat1 = result1.fit_rationales["replay"]

        # Reset the writer recorder; reinstall stages.
        StagePatch(discover_return=d, verify_return=v).install(monkeypatch)
        kw = _run_kwargs()
        result2 = run_scout_discover_verify_review(**kw)
        rat2 = result2.fit_rationales["replay"]
        assert rat1 == rat2

    def test_adv_all_verified_fit_get_fan_out_even_when_one_fails(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand_1 = _mk_candidate(cid="c1")
        cand_2 = _mk_candidate(cid="c2", channel="B")
        cand_3 = _mk_candidate(cid="c3", channel="C")
        verdicts = {
            "c1": _mk_verdict(cid="c1"),
            "c2": _mk_verdict(cid="c2"),
            "c3": _mk_verdict(cid="c3"),
        }
        StagePatch(
            discover_return=_mk_discover_result((cand_1, cand_2, cand_3)),
            verify_return=_mk_verify_result(verdicts),
        ).install(monkeypatch)

        def builder(*, session, candidate, verdict):
            if candidate.candidate_id == "c2":
                raise RuntimeError("c2 boom")
            return f"r-{candidate.candidate_id}"

        kw = _run_kwargs(rationale_builder=builder)
        result = run_scout_discover_verify_review(**kw)
        assert {it.candidate_id for it in result.review_queue_items} == {"c1", "c3"}
        # c2 has the degradation event recorded.
        assert any(
            ev.candidate_id == "c2" and ev.code == F_SCOUT_RUN_02
            for ev in result.run_degradation_events
        )

    def test_adv_rationale_returning_non_str_logged_as_run_02(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A custom builder that returns ``bytes`` instead of ``str`` is a
        deployment bug. The capstone catches this at the type guard
        (record F_SCOUT_RUN_02; do not call ``encode`` on the bytes).
        """
        cand = _mk_candidate(cid="bytes")
        StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"bytes": _mk_verdict(cid="bytes")}),
        ).install(monkeypatch)
        kw = _run_kwargs(rationale_builder=lambda **_: b"raw bytes")
        result = run_scout_discover_verify_review(**kw)
        assert len(result.review_queue_items) == 0
        assert result.run_degradation_events[0].code == F_SCOUT_RUN_02
        assert "rationale_non_str" in (result.run_degradation_events[0].reason_tag or "")


# ---------------------------------------------------------------------------
# Shared-Protocol / dataclass lineage checks (E-026 formal)
# ---------------------------------------------------------------------------


class TestInjectedSeams:
    """Per-stage Protocol injection: optional kwargs pass through to
    Round 8/9 + Round 10 entries when supplied. Closes the
    coverage gap on the eight optional-injection branches.
    """

    def test_all_optional_injections_passed_through(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="inject-1")
        patch = StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"inject-1": _mk_verdict(cid="inject-1")}),
        )
        patch.install(monkeypatch)
        d_factory = lambda n: object()  # noqa: E731 — sentinel
        d_probe = lambda: False  # noqa: E731
        d_entropy = lambda n: b"\x02" * n  # noqa: E731
        d_clock = lambda: 1_700_000_000_000_000_000  # noqa: E731
        v_factory = lambda n: object()  # noqa: E731
        v_probe = lambda: False  # noqa: E731
        v_clock = lambda: "2026-04-29T00:00:00Z"  # noqa: E731
        r_clock = lambda: "2026-04-29T01:00:00Z"  # noqa: E731

        kw = _run_kwargs()
        kw.update(
            executor_factory_discover=d_factory,
            interrupt_probe_discover=d_probe,
            entropy=d_entropy,
            clock_ns=d_clock,
            executor_factory_verify=v_factory,
            interrupt_probe_verify=v_probe,
            clock_iso_verify=v_clock,
            clock_iso_review=r_clock,
            timeout_seconds=42,
        )
        run_scout_discover_verify_review(**kw)
        assert len(patch.discover_calls) == 1
        d_call = patch.discover_calls[0]
        assert d_call["executor_factory"] is d_factory
        assert d_call["interrupt_probe"] is d_probe
        assert d_call["entropy"] is d_entropy
        assert d_call["clock"] is d_clock
        assert len(patch.verify_calls) == 1
        v_call = patch.verify_calls[0]
        assert v_call["executor_factory"] is v_factory
        assert v_call["interrupt_probe"] is v_probe
        assert v_call["clock"] is v_clock
        assert v_call["timeout_seconds"] == 42

    def test_optional_injections_omitted_use_stage_defaults(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cand = _mk_candidate(cid="inject-2")
        patch = StagePatch(
            discover_return=_mk_discover_result((cand,)),
            verify_return=_mk_verify_result({"inject-2": _mk_verdict(cid="inject-2")}),
        )
        patch.install(monkeypatch)
        run_scout_discover_verify_review(**_run_kwargs())
        d_call = patch.discover_calls[0]
        # Optional kwargs absent so defaults apply downstream.
        for absent in ("executor_factory", "interrupt_probe", "entropy", "clock"):
            assert absent not in d_call, f"{absent} unexpectedly forwarded"
        v_call = patch.verify_calls[0]
        for absent in ("executor_factory", "interrupt_probe", "clock", "timeout_seconds"):
            assert absent not in v_call, f"{absent} unexpectedly forwarded"


class TestSharedProtocolReuse:
    """Per E-026 — shared symbols carry their __module__ from origin.
    No `is` identity (fragile under sys.modules eviction).
    """

    def test_session_like_origin_review_stage(self) -> None:
        from pipeline.scout.run import SessionLike as RunSessionLike
        # Round 11 imports from review_stage (with operator_id).
        assert RunSessionLike.__module__ == "pipeline.scout.review_stage"

    def test_candidate_origin(self) -> None:
        assert Candidate.__module__ == "pipeline.scout._types"

    def test_verification_verdict_origin(self) -> None:
        assert VerificationVerdict.__module__ == "pipeline.scout._types"

    def test_review_queue_item_origin(self) -> None:
        assert ReviewQueueItem.__module__ == "pipeline.scout._types"

    def test_signed_health_tuple_origin(self) -> None:
        assert SignedHealthTuple.__module__ == "pipeline.scout._types"


# ---------------------------------------------------------------------------
# Defensive surface: exception class hierarchy
# ---------------------------------------------------------------------------


class TestExceptionHierarchy:
    def test_scout_run_interrupted_is_runtime_error(self) -> None:
        assert issubclass(ScoutRunInterrupted, RuntimeError)

    def test_rationale_budget_exceeded_carries_completed_ids(self) -> None:
        # ScoutRunInterrupted exposes completed_candidate_ids; verify shape.
        e = ScoutRunInterrupted(("a", "b"))
        assert e.completed_candidate_ids == ("a", "b")
        assert F_SCOUT_RUN_04 in str(e)

    def test_rationale_budget_exceeded_class(self) -> None:
        assert issubclass(RationaleBudgetExceeded, Exception)

    def test_rationale_build_failed_class(self) -> None:
        assert issubclass(RationaleBuildFailed, Exception)
