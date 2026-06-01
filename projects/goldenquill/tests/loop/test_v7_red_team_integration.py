"""§5 v7 amendment integration test — Red Team in inner loop alongside Judge.

Exercises the v7 production-code wiring added to:
- pipeline/loop/types.py (RunState v7 fields + signoff_pending_council_split phase + red_team SeatKind)
- pipeline/loop/seat_runner.py (invoke_red_team thin wrapper + 3-way distinct check)
- pipeline/loop/revision_loop.py (Red Team after Judge each iteration; council-split early exit)
- pipeline/loop/run_lifecycle.py (signoff_pending_council_split in allowed_resume_phases)
- pipeline/loop/run_pipeline.py (council-split routing to signoff_pending_council_split sub-phase)

Backward compat: existing 1010 §5 tests pass unchanged because Red Team
parameters in run_inner_loop default to None (v6 4-seat behavior preserved).
This file's tests exercise ONLY the new v7 5-seat path with red_team_charter
+ red_team_cascade provided.
"""

from __future__ import annotations

import json

import pytest

from pipeline.loop.revision_loop import InnerLoopResult, run_inner_loop
from pipeline.loop.seat_runner import SubprocessResult
from pipeline.loop.types import IterationState, ProviderCascade, SeatCharter
from tests.loop.conftest_section_5 import (
    Clock,
    ContextFactory,
    InMemoryVault,
    Launcher,
    make_cascade,
    make_charter,
    sleep_noop,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_red_team_cascade() -> ProviderCascade:
    """Red Team cascade — distinct families from scribe + judge cascades."""
    return ProviderCascade(
        seat_kind="red_team",
        levels=(
            ("openai-oss", "gpt-oss-120b"),  # primary
            ("anthropic", "claude-haiku"),  # fallback (3-way check skips when scribe is anthropic)
            ("mistral", "mixtral"),
        ),
        current_level=0,
    )


def _make_red_team_charter() -> SeatCharter:
    return SeatCharter(
        seat_kind="red_team",
        allowed_families=frozenset(
            {"anthropic", "google", "openai", "openai-oss", "mistral"}
        ),
        primary_model="gpt-oss-120b",
        cascade_level=0,
        subprocess_timeout_ms=180_000,
    )


def _make_run_state():
    """Submission-mode RunState in inner_loop_iter_1 ready for run_inner_loop."""
    from pipeline.loop.types import RunState

    return RunState(
        schema_version=2,  # v6 schema; v7 fields are optional add-ons
        run_id="run-v7-int",
        mode="submission",
        rfa_hash="a" * 64,
        project_context_hash="b" * 64,
        golden_set_ref=None,
        org_slug="fit_farms",
        session_id="sess-v7",
        phase="inner_loop_iter_1",
    )


def _make_launcher_with_council_split() -> Launcher:
    """Configure launcher: Judge returns 90; Red Team returns 70 (delta=20 ≥ 10)."""
    judge_stdout = json.dumps({"verdict": "REVISE", "total_score": 90}).encode("utf-8")
    red_team_stdout = json.dumps(
        {"recommendation": "marginal", "total_score": 70}
    ).encode("utf-8")
    launcher = Launcher()
    launcher.per_seat = {
        "judge": [
            SubprocessResult(
                exit_code=0,
                stdout=judge_stdout,
                stderr=b"",
                timed_out=False,
                landed_family="google",
                landed_model_id="gemini-2.5-pro",
            )
        ] * 3,
        "red_team": [
            SubprocessResult(
                exit_code=0,
                stdout=red_team_stdout,
                stderr=b"",
                timed_out=False,
                landed_family="openai-oss",
                landed_model_id="gpt-oss-120b",
            )
        ] * 3,
    }
    return launcher


def _make_launcher_no_council_split() -> Launcher:
    """Configure launcher: Judge returns 90; Red Team returns 88 (delta=2 < 10)."""
    judge_stdout = json.dumps({"verdict": "PASS", "total_score": 90}).encode("utf-8")
    red_team_stdout = json.dumps(
        {"recommendation": "competitive", "total_score": 88}
    ).encode("utf-8")
    launcher = Launcher()
    launcher.per_seat = {
        "judge": [
            SubprocessResult(
                exit_code=0,
                stdout=judge_stdout,
                stderr=b"",
                timed_out=False,
                landed_family="google",
                landed_model_id="gemini-2.5-pro",
            )
        ],
        "red_team": [
            SubprocessResult(
                exit_code=0,
                stdout=red_team_stdout,
                stderr=b"",
                timed_out=False,
                landed_family="openai-oss",
                landed_model_id="gpt-oss-120b",
            )
        ],
    }
    return launcher


def _make_inner_loop_kwargs(
    run_state, launcher, *, with_red_team: bool, vault, clock
):
    """Build run_inner_loop kwargs with optional Red Team charter/cascade."""
    kwargs = dict(
        run_state=run_state,
        scribe_charter=make_charter("scribe"),
        editor_charter=make_charter("editor"),
        judge_charter=make_charter("judge"),
        scribe_cascade=make_cascade("scribe"),
        editor_cascade=make_cascade("editor"),
        judge_cascade=make_cascade("judge"),
        context_factory=ContextFactory(),
        subprocess_launcher=launcher,
        vault_write=vault.write,
        clock=clock,
        sleep=sleep_noop,
        initial_checkpoint_hash=None,
    )
    if with_red_team:
        kwargs["red_team_charter"] = _make_red_team_charter()
        kwargs["red_team_cascade"] = _make_red_team_cascade()
    return kwargs


# ---------------------------------------------------------------------------
# v6 backward compat (red_team_charter=None → 4-seat path identical to v6)
# ---------------------------------------------------------------------------


class TestV6BackwardCompat:
    def test_run_inner_loop_without_red_team_runs_4_seat_council(self) -> None:
        """red_team_charter=None → behavior identical to v6."""
        run_state = _make_run_state()
        vault = InMemoryVault()
        clock = Clock()
        launcher = Launcher(default_judge_stdout=json.dumps({"verdict": "PASS", "total_score": 92}).encode())
        result = run_inner_loop(
            **_make_inner_loop_kwargs(run_state, launcher, with_red_team=False, vault=vault, clock=clock)
        )
        assert isinstance(result, InnerLoopResult)
        assert result.converged_on == "score_threshold"
        # No red_team in run_iteration_families_so_far
        assert "red_team" not in run_state.run_iteration_families_so_far
        # No red_team_verdict on the IterationState
        assert result.final_iteration.red_team_verdict is None
        # red_team not in seat_draft_hashes
        assert "red_team" not in result.final_iteration.seat_draft_hashes


# ---------------------------------------------------------------------------
# v7 5-seat happy path (no council-split; converges on score_threshold)
# ---------------------------------------------------------------------------


class TestV7HappyPath:
    def test_run_inner_loop_with_red_team_converges_normally(self) -> None:
        """Judge=90, Red Team=88 (delta=2) → no council-split; normal convergence."""
        run_state = _make_run_state()
        vault = InMemoryVault()
        clock = Clock()
        launcher = _make_launcher_no_council_split()
        result = run_inner_loop(
            **_make_inner_loop_kwargs(run_state, launcher, with_red_team=True, vault=vault, clock=clock)
        )
        assert result.converged_on == "score_threshold"  # Judge said PASS
        assert result.final_iteration.red_team_verdict is not None
        assert result.final_iteration.red_team_verdict.get("total_score") == 88
        assert "red_team" in run_state.run_iteration_families_so_far
        assert run_state.run_iteration_families_so_far["red_team"] == (
            "openai-oss",
            "gpt-oss-120b",
        )
        assert "red_team" in result.final_iteration.seat_draft_hashes
        assert result.final_iteration.exit_reason == ""  # not council_split

    def test_red_team_invoked_after_judge(self) -> None:
        run_state = _make_run_state()
        vault = InMemoryVault()
        clock = Clock()
        launcher = _make_launcher_no_council_split()
        run_inner_loop(
            **_make_inner_loop_kwargs(run_state, launcher, with_red_team=True, vault=vault, clock=clock)
        )
        # Walk launcher.calls — red_team must come AFTER judge in the same iteration.
        seat_order = [c["seat_kind"] for c in launcher.calls]
        # First iteration: scribe → editor → judge → red_team
        assert seat_order[:4] == ["scribe", "editor", "judge", "red_team"]


# ---------------------------------------------------------------------------
# v7 council-split path (delta ≥ 10 → early exit with converged_on=council_split)
# ---------------------------------------------------------------------------


class TestV7CouncilSplitPath:
    def test_council_split_detected_at_threshold(self) -> None:
        """Judge=90, Red Team=70 (delta=20 ≥ 10) → council_split early exit."""
        run_state = _make_run_state()
        vault = InMemoryVault()
        clock = Clock()
        launcher = _make_launcher_with_council_split()
        result = run_inner_loop(
            **_make_inner_loop_kwargs(run_state, launcher, with_red_team=True, vault=vault, clock=clock)
        )
        assert result.converged_on == "council_split"
        assert result.iterations_run == 1  # exited on iteration 1
        assert result.final_iteration.exit_reason == "council_split"
        assert result.final_iteration.red_team_verdict is not None
        assert result.final_iteration.red_team_verdict.get("total_score") == 70
        assert result.final_iteration.judge_verdict.get("total_score") == 90

    def test_council_split_boundary_inclusive_at_10(self) -> None:
        """Judge=15, Red Team=5 (delta=10 EXACTLY) → council_split fires (inclusive)."""
        run_state = _make_run_state()
        vault = InMemoryVault()
        clock = Clock()
        launcher = Launcher()
        launcher.per_seat = {
            "judge": [
                SubprocessResult(
                    exit_code=0,
                    stdout=json.dumps({"verdict": "REVISE", "total_score": 15}).encode(),
                    stderr=b"",
                    timed_out=False,
                    landed_family="google",
                    landed_model_id="gemini",
                )
            ] * 3,
            "red_team": [
                SubprocessResult(
                    exit_code=0,
                    stdout=json.dumps({"recommendation": "marginal", "total_score": 5}).encode(),
                    stderr=b"",
                    timed_out=False,
                    landed_family="openai-oss",
                    landed_model_id="gpt-oss",
                )
            ] * 3,
        }
        result = run_inner_loop(
            **_make_inner_loop_kwargs(run_state, launcher, with_red_team=True, vault=vault, clock=clock)
        )
        assert result.converged_on == "council_split"

    def test_council_split_below_threshold_does_not_fire(self) -> None:
        """Judge=15, Red Team=6 (delta=9 < 10) → council_split does NOT fire."""
        run_state = _make_run_state()
        vault = InMemoryVault()
        clock = Clock()
        launcher = Launcher()
        launcher.per_seat = {
            "judge": [
                SubprocessResult(
                    exit_code=0,
                    stdout=json.dumps({"verdict": "PASS", "total_score": 15}).encode(),
                    stderr=b"",
                    timed_out=False,
                    landed_family="google",
                    landed_model_id="gemini",
                )
            ],
            "red_team": [
                SubprocessResult(
                    exit_code=0,
                    stdout=json.dumps({"recommendation": "marginal", "total_score": 6}).encode(),
                    stderr=b"",
                    timed_out=False,
                    landed_family="openai-oss",
                    landed_model_id="gpt-oss",
                )
            ],
        }
        result = run_inner_loop(
            **_make_inner_loop_kwargs(run_state, launcher, with_red_team=True, vault=vault, clock=clock)
        )
        # Judge said PASS → score_threshold convergence, NOT council_split
        assert result.converged_on == "score_threshold"
        assert result.final_iteration.exit_reason == ""

    def test_custom_threshold_override(self) -> None:
        """Operator override: rt_disagreement_threshold=5 → delta=6 fires split."""
        run_state = _make_run_state()
        vault = InMemoryVault()
        clock = Clock()
        launcher = Launcher()
        launcher.per_seat = {
            "judge": [
                SubprocessResult(
                    exit_code=0,
                    stdout=json.dumps({"verdict": "REVISE", "total_score": 15}).encode(),
                    stderr=b"",
                    timed_out=False,
                    landed_family="google",
                    landed_model_id="gemini",
                )
            ] * 3,
            "red_team": [
                SubprocessResult(
                    exit_code=0,
                    stdout=json.dumps({"recommendation": "marginal", "total_score": 9}).encode(),
                    stderr=b"",
                    timed_out=False,
                    landed_family="openai-oss",
                    landed_model_id="gpt-oss",
                )
            ] * 3,
        }
        kwargs = _make_inner_loop_kwargs(run_state, launcher, with_red_team=True, vault=vault, clock=clock)
        kwargs["rt_disagreement_threshold"] = 5
        result = run_inner_loop(**kwargs)
        assert result.converged_on == "council_split"


# ---------------------------------------------------------------------------
# v7 type system additions (signoff_pending_council_split phase + red_team SeatKind)
# ---------------------------------------------------------------------------


class TestV7TypeSystem:
    def test_signoff_pending_council_split_phase_accepted(self) -> None:
        """RunState accepts the new v7 phase Literal."""
        from pipeline.loop.types import RunState

        rs = RunState(
            schema_version=2,
            run_id="r",
            mode="submission",
            rfa_hash="a" * 64,
            project_context_hash="b" * 64,
            golden_set_ref=None,
            org_slug="x",
            session_id="s",
            phase="signoff_pending_council_split",
        )
        assert rs.phase == "signoff_pending_council_split"

    def test_red_team_seat_kind_accepted(self) -> None:
        """SeatCharter accepts seat_kind=red_team."""
        sc = SeatCharter(
            seat_kind="red_team",
            allowed_families=frozenset({"openai-oss"}),
            primary_model="gpt-oss-120b",
            cascade_level=0,
            subprocess_timeout_ms=180_000,
        )
        assert sc.seat_kind == "red_team"

    def test_iteration_state_red_team_verdict_field(self) -> None:
        """IterationState.red_team_verdict + exit_reason are v7 NEW fields."""
        ist = IterationState(
            iter_number=1,
            red_team_verdict={"total_score": 70},
            exit_reason="council_split",
        )
        assert ist.red_team_verdict == {"total_score": 70}
        assert ist.exit_reason == "council_split"
        # Backward compat: defaults work.
        ist_v6 = IterationState(iter_number=1)
        assert ist_v6.red_team_verdict is None
        assert ist_v6.exit_reason == ""

    def test_run_state_v7_fields_default_none(self) -> None:
        """v7 RunState fields default to None (v6 backward compat)."""
        from pipeline.loop.types import RunState

        rs = RunState(
            schema_version=2,
            run_id="r",
            mode="submission",
            rfa_hash="a" * 64,
            project_context_hash="b" * 64,
            golden_set_ref=None,
            org_slug="x",
            session_id="s",
            phase="initialized",
        )
        assert rs.red_team_verdict_ref is None
        assert rs.council_split_decision is None
        assert rs.red_team_bypass_authorization_ref is None
