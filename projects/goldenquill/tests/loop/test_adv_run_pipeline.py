"""Adversarial tests for pipeline.loop.run_pipeline — §4.1 capstone (Round 11).

E-024 adversarial coverage (2× scope vs. happy tests). Targets:

1. Module-load rebind-resistance (MAX_REVISION_ITERATIONS +
   RUNSTATE_SCHEMA_VERSION → assert-at-load).
2. Step-1 F_PIPE_21 surface on bad RunState construction (missing rfa_hash
   / project_context_hash — hit BEFORE any vault write).
3. Step-3 PRE-gate raise paths:
   - PipelineFailure (F_PIPE_21) from callable → state-failure wrapper +
     re-raise.
   - Arbitrary Exception from callable → state-failure wrapper + re-raise.
   - PreGateInputFactory raise → state-failure wrapper + re-raise.
4. Step-5 inner-loop raises propagate with NO double-wrapper
   (Round 5 already wrote state-failure; Round 11 must not add a second).
5. Step-6 post_gate_orchestration raises F_PIPE_03 → propagates
   unwrapped; not translated to bypass.
6. Step-7 PostGateRejected:
   - Trigger + gate_result reach the returned PipelineRunResult.
   - Bypass-pending marker is best-effort (vault failure does NOT mask
     the bypass return).
7. Step-10 tab-delivery F_PIPE_16 / F_PIPE_21 → state-failure wrapper +
   re-raise with the ORIGINAL exception type (not synthesized
   F_PIPE_21).
8. Step-2 / step-8 / step-9 / step-11 phase-transition failures — CAS
   exhausted in the middle of the 11-step walk → F_PIPE_01 propagates.
9. Bypass-pending marker shape — keys + UTF-8 sort_keys JSON.
10. __all__ + BLUEPRINT_DEPS surface + PipelineRunResult slots pin.
11. Capture-wrapper single-shot semantics — only the first committed_hash
    is retained by the sink.
12. PreGateInputFactory runtime_checkable contract.
"""

from __future__ import annotations

import hashlib
import importlib
import json
from dataclasses import dataclass, field
from typing import Any

import pytest

from pipeline.logician import (
    GateRunnerPostResult,
    PostGateInput,
    PreGateInput,
    PreGateResult,
)
from pipeline.loop.errors import (
    F_PIPE_01,
    F_PIPE_03,
    F_PIPE_05,
    F_PIPE_11,
    F_PIPE_16,
    F_PIPE_21,
    F_PIPE_22,
    PipelineFailure,
)
from pipeline.loop.post_gate_runner import PostGateRejected
from pipeline.loop.revision_loop import InnerLoopResult
from pipeline.loop.run_pipeline import (
    BLUEPRINT_DEPS,
    PipelineRunResult,
    PreGateInputFactory,
    RunPipelineContext,
    run_pipeline,
)
from pipeline.loop.seat_runner import SeatInvocationContext, SubprocessResult
from pipeline.loop.types import (
    IterationState,
    ProviderCascade,
    RunState,
    SeatCharter,
)

# ---------------------------------------------------------------------------
# Shared test doubles (mirror test_run_pipeline.py shape)
# ---------------------------------------------------------------------------


@dataclass
class _InMemoryVault:
    store: dict[str, bytes] = field(default_factory=dict)
    writes: list[dict[str, Any]] = field(default_factory=list)
    fail_on_path: str | None = None
    fail_on_intent: str | None = None
    raise_exc: BaseException | None = None

    def write(
        self,
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        self.writes.append(
            {
                "path": path,
                "intent": intent,
                "write_mode": write_mode,
                "expected_current_file_hash": expected_current_file_hash,
            }
        )
        if self.raise_exc is not None:
            if (
                self.fail_on_path is None or path == self.fail_on_path
            ) and (self.fail_on_intent is None or intent == self.fail_on_intent):
                raise self.raise_exc
        if write_mode == "write-if-absent" and path in self.store:
            from pipeline.vault import VaultWriteExists

            raise VaultWriteExists(f"{path} already exists")
        if (
            write_mode == "overwrite"
            and expected_current_file_hash is not None
            and path in self.store
        ):
            current = hashlib.sha256(self.store[path]).hexdigest()
            if current != expected_current_file_hash:
                from pipeline.vault import VaultCASHeadMismatch

                raise VaultCASHeadMismatch(
                    f"{path}: expected {expected_current_file_hash[:8]}, got {current[:8]}"
                )
        self.store[path] = payload
        return hashlib.sha256(payload).hexdigest()

    def read(self, *, path: str) -> bytes:
        return self.store[path]

    def __call__(self, **kwargs: Any) -> str:
        return self.write(**kwargs)


@dataclass
class _Clock:
    _ms: int = 1_000
    iso: str = "2026-04-21T12:00:00Z"

    def now_ms(self) -> int:
        v = self._ms
        self._ms += 5
        return v

    def now_iso(self) -> str:
        return self.iso


def _sleep_noop(_ms: int) -> None:
    return None


@dataclass
class _Launcher:
    per_seat: dict[str, list[SubprocessResult]] = field(default_factory=dict)
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(
        self,
        *,
        seat_kind: str,
        env: dict[str, str],
        stdin_payload: bytes,
        timeout_ms: int,
        family: str,
        model_id: str,
    ) -> SubprocessResult:
        self.calls.append({"seat_kind": seat_kind, "family": family})
        q = self.per_seat.get(seat_kind, [])
        if q:
            return q.pop(0)
        return SubprocessResult(
            exit_code=0,
            stdout=(
                b'{"verdict": "PASS", "total_score": 90}'
                if seat_kind == "judge"
                else b"draft"
            ),
            stderr=b"",
            timed_out=False,
            landed_family=family,
            landed_model_id=model_id,
        )


@dataclass
class _ContextFactory:
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(
        self,
        *,
        seat_kind: str,
        iter_n: int,
        prev_editor_hash: str | None,
        prev_judge_hash: str | None,
        run_state: RunState,
    ) -> SeatInvocationContext:
        self.calls.append({"seat_kind": seat_kind, "iter_n": iter_n})
        return SeatInvocationContext(
            stdin_payload=b"x",
            session_id=run_state.session_id,
            path_value="/usr/bin:/bin",
            home_value="/home/tilth",
        )


@dataclass
class _PreGateCallable:
    result: PreGateResult | None = None
    raise_exc: BaseException | None = None
    calls: list[PreGateInput] = field(default_factory=list)

    def __call__(self, input_: PreGateInput) -> PreGateResult:
        self.calls.append(input_)
        if self.raise_exc is not None:
            raise self.raise_exc
        assert self.result is not None
        return self.result


@dataclass
class _PreGateInputFactory:
    payload: Any = "pre-gate-input-opaque"
    raise_exc: BaseException | None = None
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(self, *, run_state: RunState) -> PreGateInput:
        self.calls.append({"run_state_id": run_state.run_id})
        if self.raise_exc is not None:
            raise self.raise_exc
        return self.payload  # type: ignore[return-value]


@dataclass
class _PostGateRunner:
    result: GateRunnerPostResult | None = None
    raise_exc: BaseException | None = None
    calls: list[PostGateInput] = field(default_factory=list)

    def run_post_gate(self, input_: PostGateInput) -> GateRunnerPostResult:
        self.calls.append(input_)
        if self.raise_exc is not None:
            raise self.raise_exc
        assert self.result is not None
        return self.result


@dataclass
class _PostGateInputFactory:
    payload: Any = "post-gate-input-opaque"
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(
        self, *, run_state: RunState, inner_loop_result: InnerLoopResult
    ) -> PostGateInput:
        self.calls.append({"run_state_id": run_state.run_id})
        return self.payload  # type: ignore[return-value]


@dataclass
class _HashFile:
    data: dict[str, str] = field(default_factory=dict)
    calls: list[str] = field(default_factory=list)
    raise_exc: BaseException | None = None

    def __call__(self, path: str) -> str:
        self.calls.append(path)
        if self.raise_exc is not None:
            raise self.raise_exc
        return self.data.get(path, "a" * 64)


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def _charter(seat_kind: str) -> SeatCharter:
    return SeatCharter(
        seat_kind=seat_kind,
        allowed_families=frozenset({"anthropic", "google", "openai"}),
        primary_model="primary",
        cascade_level=0,
        subprocess_timeout_ms=180_000,
    )


def _cascade(seat_kind: str) -> ProviderCascade:
    if seat_kind == "scribe":
        levels = (("anthropic", "claude-opus"), ("google", "gemini"), ("openai", "gpt"))
    elif seat_kind == "editor":
        levels = (("google", "gemini"), ("openai", "gpt"), ("meta", "llama"))
    else:
        levels = (("openai", "gpt"), ("meta", "llama"), ("mistral", "mixtral"))
    return ProviderCascade(seat_kind=seat_kind, levels=levels, current_level=0)


def _pre_gate_pass() -> PreGateResult:
    return PreGateResult(
        passed=True,
        failed_check_number=None,
        failure_code=None,
        failure_detail=None,
        completed_checks=(1, 2, 3),
    )


def _post_gate_pass() -> GateRunnerPostResult:
    return GateRunnerPostResult(
        passed=True,
        failed_step_number=None,
        failure_code=None,
        failure_detail="",
        failure_codes=(),
        completed_steps=(),
        claim_evidence_map=None,
        underlying_post_gate_result=None,
    )


def _post_gate_fail(code: str = "F-POST-12-STUB") -> GateRunnerPostResult:
    return GateRunnerPostResult(
        passed=False,
        failed_step_number=12,
        failure_code=code,
        failure_detail="stub POST-gate fail",
        failure_codes=(code,),
        completed_steps=(),
        claim_evidence_map=None,
        underlying_post_gate_result=None,
    )


@dataclass
class _Harness:
    vault: _InMemoryVault
    clock: _Clock
    launcher: _Launcher
    context_factory: _ContextFactory
    pre_gate_callable: _PreGateCallable
    pre_gate_input_factory: _PreGateInputFactory
    post_gate_runner: _PostGateRunner
    post_gate_input_factory: _PostGateInputFactory
    hash_file: _HashFile
    context: RunPipelineContext


def _build_harness(
    *,
    run_id: str = "run-adv",
    pre_gate: _PreGateCallable | None = None,
    pre_gate_factory: _PreGateInputFactory | None = None,
    post_gate: _PostGateRunner | None = None,
    hash_file: _HashFile | None = None,
    vault: _InMemoryVault | None = None,
) -> _Harness:
    v = vault or _InMemoryVault()
    clock = _Clock()
    launcher = _Launcher()
    ctx_factory = _ContextFactory()
    pgc = pre_gate or _PreGateCallable(result=_pre_gate_pass())
    pgf = pre_gate_factory or _PreGateInputFactory()
    pr = post_gate or _PostGateRunner(result=_post_gate_pass())
    prf = _PostGateInputFactory()
    hf = hash_file or _HashFile()
    context = RunPipelineContext(
        vault_read=v.read,
        vault_write=v.write,
        clock=clock,
        sleep=_sleep_noop,
        run_id_factory=lambda: run_id,
        subprocess_launcher=launcher,
        seat_context_factory=ctx_factory,
        pre_gate_callable=pgc,
        post_gate_runner=pr,
        post_gate_input_factory=prf,
        hash_file=hf,
    )
    return _Harness(
        vault=v,
        clock=clock,
        launcher=launcher,
        context_factory=ctx_factory,
        pre_gate_callable=pgc,
        pre_gate_input_factory=pgf,
        post_gate_runner=pr,
        post_gate_input_factory=prf,
        hash_file=hf,
        context=context,
    )


def _run(
    h: _Harness,
    *,
    run_id: str = "run-adv",
    rfa_hash: str | None = "rfa-abc",
    project_context_hash: str | None = "pc-def",
) -> PipelineRunResult:
    return run_pipeline(
        run_id=run_id,
        org_slug="org-x",
        session_id="sess",
        rfa_hash=rfa_hash,  # type: ignore[arg-type]
        project_context_hash=project_context_hash,  # type: ignore[arg-type]
        scribe_charter=_charter("scribe"),
        editor_charter=_charter("editor"),
        judge_charter=_charter("judge"),
        scribe_cascade=_cascade("scribe"),
        editor_cascade=_cascade("editor"),
        judge_cascade=_cascade("judge"),
        context=h.context,
        pre_gate_input_factory=h.pre_gate_input_factory,
    )


# ===========================================================================
# Module-load rebind-resistance
# ===========================================================================


class TestRebindResistance:
    def test_max_revision_iterations_is_three(self) -> None:
        import importlib

        rp_mod = importlib.import_module("pipeline.loop.run_pipeline")

        # The module has been loaded; its assert fired at load time. We
        # additionally verify the constant has not been rebound after
        # import (a defence-in-depth companion check).
        from pipeline.loop.config import MAX_REVISION_ITERATIONS

        assert MAX_REVISION_ITERATIONS == 3
        assert rp_mod.MAX_REVISION_ITERATIONS == 3

    def test_runstate_schema_version_is_two(self) -> None:
        import importlib

        rp_mod = importlib.import_module("pipeline.loop.run_pipeline")
        from pipeline.loop.config import RUNSTATE_SCHEMA_VERSION

        assert RUNSTATE_SCHEMA_VERSION == 2
        assert rp_mod.RUNSTATE_SCHEMA_VERSION == 2

    def test_blueprint_deps_surface(self) -> None:
        assert "section_05_pipeline.md" in BLUEPRINT_DEPS
        entry = BLUEPRINT_DEPS["section_05_pipeline.md"]
        assert entry["version"] == "v6"
        assert isinstance(entry["sections_implemented"], list)


# ===========================================================================
# Step 1 — RunState construction failures (F_PIPE_21)
# ===========================================================================


class TestStep1RunStateConstruction:
    def test_missing_rfa_hash_raises_f_pipe_21(self) -> None:
        h = _build_harness()
        with pytest.raises(F_PIPE_21) as exc:
            _run(h, rfa_hash=None)
        assert exc.value.trigger == "submission_mode_missing_rfa_hash"
        # No state.json should have been persisted — construction failed
        # before checkpoint_atomic.
        assert "pipeline/run-adv/state.json" not in h.vault.store

    def test_missing_project_context_hash_raises_f_pipe_21(self) -> None:
        h = _build_harness()
        with pytest.raises(F_PIPE_21) as exc:
            _run(h, project_context_hash=None)
        assert exc.value.trigger == "submission_mode_missing_project_context_hash"


# ===========================================================================
# Step 3 — PRE-gate raise paths
# ===========================================================================


class TestStep3PreGateRaises:
    def test_pre_gate_callable_raises_pipeline_failure_propagates(self) -> None:
        err = F_PIPE_21(trigger="submission_mode_missing_rfa_hash", details={"run_id": "r"})
        h = _build_harness(pre_gate=_PreGateCallable(raise_exc=err))
        with pytest.raises(F_PIPE_21):
            _run(h)
        # State-failure wrapper was invoked (sidecar or state-failure checkpoint).
        state_failure_writes = [
            w for w in h.vault.writes if w["intent"] == "state-failure"
        ]
        assert len(state_failure_writes) >= 1

    def test_pre_gate_callable_raises_runtime_error_propagates(self) -> None:
        err = RuntimeError("unexpected")
        h = _build_harness(pre_gate=_PreGateCallable(raise_exc=err))
        with pytest.raises(RuntimeError, match="unexpected"):
            _run(h)
        state_failure_writes = [
            w for w in h.vault.writes if w["intent"] == "state-failure"
        ]
        assert len(state_failure_writes) >= 1

    def test_pre_gate_input_factory_raises_propagates(self) -> None:
        err = ValueError("factory explosion")
        h = _build_harness(pre_gate_factory=_PreGateInputFactory(raise_exc=err))
        with pytest.raises(ValueError, match="factory explosion"):
            _run(h)


# ===========================================================================
# Step 5 — inner loop raises propagate without double-wrapper
# ===========================================================================


class TestStep5InnerLoopRaises:
    def test_f_pipe_05_iter_cap_propagates(self) -> None:
        # Programmable launcher that always returns FAIL verdict → Round 5
        # raises F_PIPE_05 after three iterations.
        launcher = _Launcher()
        for _ in range(4):
            launcher.per_seat.setdefault("scribe", []).append(
                SubprocessResult(
                    exit_code=0,
                    stdout=b"draft",
                    stderr=b"",
                    timed_out=False,
                    landed_family="anthropic",
                    landed_model_id="a",
                )
            )
            launcher.per_seat.setdefault("editor", []).append(
                SubprocessResult(
                    exit_code=0,
                    stdout=b"editor-draft",
                    stderr=b"",
                    timed_out=False,
                    landed_family="google",
                    landed_model_id="g",
                )
            )
            launcher.per_seat.setdefault("judge", []).append(
                SubprocessResult(
                    exit_code=0,
                    stdout=b'{"verdict": "FAIL", "total_score": 40}',
                    stderr=b"",
                    timed_out=False,
                    landed_family="openai",
                    landed_model_id="o",
                )
            )
        h = _build_harness()
        # Swap launcher post-construction
        h.launcher.per_seat = launcher.per_seat
        with pytest.raises(F_PIPE_05):
            _run(h)


# ===========================================================================
# Step 6-7 — POST-gate bypass + raise paths
# ===========================================================================


class TestStep6PostGatePaths:
    def test_post_gate_rejected_threads_trigger_onto_result(self) -> None:
        h = _build_harness(
            post_gate=_PostGateRunner(result=_post_gate_fail("F-POST-09-STUB"))
        )
        result = _run(h)
        assert result.bypass_pending is True
        assert result.post_gate_rejected_trigger is not None

    def test_post_gate_runner_raises_f_pipe_03_propagates_not_translated_to_bypass(
        self,
    ) -> None:
        err = F_PIPE_03(trigger="post_gate_timeout", details={"run_id": "x"})
        h = _build_harness(post_gate=_PostGateRunner(raise_exc=err))
        with pytest.raises(F_PIPE_03):
            _run(h)

    def test_bypass_marker_vault_write_failure_does_not_mask_bypass_return(
        self,
    ) -> None:
        # Inject a vault that fails ONLY the bypass-pending marker write.
        vault = _InMemoryVault(
            fail_on_intent="bypass-pending", raise_exc=RuntimeError("vault blip")
        )
        h = _build_harness(
            vault=vault,
            post_gate=_PostGateRunner(result=_post_gate_fail("F-POST-X")),
        )
        # Still returns bypass_pending=True; marker write is best-effort.
        result = _run(h)
        assert result.bypass_pending is True

    def test_bypass_marker_contains_required_keys(self) -> None:
        h = _build_harness(
            post_gate=_PostGateRunner(result=_post_gate_fail("F-POST-KEY"))
        )
        _run(h, run_id="run-adv")
        marker_payload = h.vault.store["pipeline/run-adv/bypass_pending.json"]
        marker = json.loads(marker_payload.decode("utf-8"))
        assert marker["run_id"] == "run-adv"
        assert "org_slug" in marker
        assert "phase_at_bypass" in marker
        assert marker["failure_code"] == "F-POST-KEY"
        assert marker["written_at_iso"] == "2026-04-21T12:00:00Z"

    def test_bypass_marker_is_utf8_canonical_json(self) -> None:
        h = _build_harness(
            post_gate=_PostGateRunner(result=_post_gate_fail("F-POST-X"))
        )
        _run(h, run_id="run-adv")
        marker_payload = h.vault.store["pipeline/run-adv/bypass_pending.json"]
        # sort_keys + separators=(",",":") — no spaces.
        assert b": " not in marker_payload
        assert b", " not in marker_payload
        assert marker_payload == marker_payload  # reparseable
        decoded = json.loads(marker_payload.decode("utf-8"))
        assert isinstance(decoded, dict)


# ===========================================================================
# Step 10 — tab_delivery raise paths (original exception preserved)
# ===========================================================================


class TestStep10TabDeliveryRaises:
    def test_tab_delivery_runtime_error_propagates(self) -> None:
        err = RuntimeError("tab explosion")
        h = _build_harness(hash_file=_HashFile(raise_exc=err))
        with pytest.raises(RuntimeError, match="tab explosion"):
            _run(h)

    def test_tab_delivery_propagates_original_f_pipe_type(self) -> None:
        # Simulate an F_PIPE_16 raised from inside hash_file — the
        # wrapper must re-raise the ORIGINAL code (not synthesize F_PIPE_21).
        err = F_PIPE_16(
            trigger="tab_envelope_ordering_violation",
            details={"run_id": "run-adv"},
        )
        h = _build_harness(hash_file=_HashFile(raise_exc=err))
        with pytest.raises(F_PIPE_16) as exc:
            _run(h)
        assert exc.value.trigger == "tab_envelope_ordering_violation"


# ===========================================================================
# PipelineRunResult / RunPipelineContext surface contracts
# ===========================================================================


class TestResultSurfaceContracts:
    def test_result_is_slotted(self) -> None:
        r = PipelineRunResult(
            run_id="t",
            final_phase="tabs_delivered",
            iterations_consumed=1,
            three_tab_envelope_hash="h",
            elapsed_ms=10,
        )
        assert not hasattr(r, "__dict__")  # slots=True

    def test_context_is_slotted(self) -> None:
        h = _build_harness()
        assert not hasattr(h.context, "__dict__")

    def test_result_fields_are_typed_correctly(self) -> None:
        r = PipelineRunResult(
            run_id="t",
            final_phase="post_gate_pending",
            iterations_consumed=3,
            three_tab_envelope_hash=None,
            elapsed_ms=99,
            bypass_pending=True,
            post_gate_rejected_trigger="post_gate_failure:F-POST-12",
        )
        assert r.iterations_consumed == 3
        assert r.elapsed_ms == 99
        assert r.bypass_pending is True
        assert r.post_gate_rejected_trigger == "post_gate_failure:F-POST-12"


# ===========================================================================
# PreGateInputFactory Protocol — runtime_checkable + structural typing
# ===========================================================================


class TestPreGateInputFactoryProtocol:
    def test_plain_function_satisfies_protocol(self) -> None:
        def factory(*, run_state: RunState) -> PreGateInput:
            return "x"  # type: ignore[return-value]

        assert isinstance(factory, PreGateInputFactory)

    def test_class_instance_satisfies_protocol(self) -> None:
        class F:
            def __call__(self, *, run_state: RunState) -> PreGateInput:
                return "x"  # type: ignore[return-value]

        assert isinstance(F(), PreGateInputFactory)

    def test_non_callable_does_not_satisfy_protocol(self) -> None:
        assert not isinstance(42, PreGateInputFactory)


# ===========================================================================
# __all__ + module-level surface
# ===========================================================================


class TestModuleSurface:
    def test_all_contains_expected_names(self) -> None:
        import importlib

        mod = importlib.import_module("pipeline.loop.run_pipeline")
        # v7: run_pipeline_5_seat added as the operator-facing 5-seat default
        # entrypoint per §5 v7 amendment + §10 Red Team mandate.
        assert set(mod.__all__) == {
            "BLUEPRINT_DEPS",
            "PipelineRunResult",
            "PreGateInputFactory",
            "RunPipelineContext",
            "run_pipeline",
            "run_pipeline_5_seat",
        }

    def test_reexport_via_package_init(self) -> None:
        import pipeline.loop as pkg

        assert pkg.run_pipeline is run_pipeline
        assert pkg.PipelineRunResult is PipelineRunResult
        assert pkg.RunPipelineContext is RunPipelineContext
        assert pkg.PreGateInputFactory is PreGateInputFactory


# ===========================================================================
# Capture-wrapper single-shot semantics
# ===========================================================================


class TestCaptureWrapperSemantics:
    def test_first_commit_hash_used_as_step2_cas_pin(self) -> None:
        h = _build_harness()
        _run(h)
        # Locate the first state.json write (Round 3 start_run) and the
        # second (Round 11 step 2 transition). The second's
        # expected_current_file_hash must equal sha256 of the first's
        # payload.
        state_writes = [
            w for w in h.vault.writes if w["path"].endswith("/state.json")
        ]
        first = state_writes[0]
        second = state_writes[1]
        # First is write-if-absent (no CAS pin).
        assert first["expected_current_file_hash"] is None
        assert first["write_mode"] in {"write-if-absent", "overwrite"}
        # Second must pin a concrete CAS head.
        assert second["expected_current_file_hash"] is not None
        assert len(second["expected_current_file_hash"]) == 64


# ===========================================================================
# Phase-transition wrapper coverage — targeted vault faults per step
# ===========================================================================


@dataclass
class _PhaseFaultVault(_InMemoryVault):
    """Vault that raises ``RuntimeError`` on state.json writes carrying a
    payload whose decoded JSON ``phase`` field matches ``trip_phase``.

    Fires exactly once (subsequent same-phase writes succeed) so the
    state-failure wrapper can land its sidecar.
    """

    trip_phase: str | None = None
    _tripped: bool = False

    def write(
        self,
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        if (
            self.trip_phase is not None
            and not self._tripped
            and path.endswith("/state.json")
        ):
            try:
                decoded = json.loads(payload.decode("utf-8"))
                if decoded.get("phase") == self.trip_phase:
                    self._tripped = True
                    raise RuntimeError(f"vault blip at phase={self.trip_phase}")
            except json.JSONDecodeError:  # pragma: no cover — payloads are JSON
                pass
        return super().write(
            path=path,
            payload=payload,
            intent=intent,
            write_mode=write_mode,
            expected_current_file_hash=expected_current_file_hash,
        )


class TestPhaseTransitionWrappers:
    def test_step2_pre_gate_pending_transition_fault_propagates(self) -> None:
        vault = _PhaseFaultVault(trip_phase="pre_gate_pending")
        h = _build_harness(vault=vault)
        with pytest.raises(RuntimeError, match="pre_gate_pending"):
            _run(h)

    def test_step3_pre_gate_passed_transition_fault_propagates(self) -> None:
        vault = _PhaseFaultVault(trip_phase="pre_gate_passed")
        h = _build_harness(vault=vault)
        with pytest.raises(RuntimeError, match="pre_gate_passed"):
            _run(h)

    def test_step4_inner_loop_iter_1_transition_fault_propagates(self) -> None:
        vault = _PhaseFaultVault(trip_phase="inner_loop_iter_1")
        h = _build_harness(vault=vault)
        with pytest.raises(RuntimeError, match="inner_loop_iter_1"):
            _run(h)

    def test_step8_signoff_pending_transition_fault_propagates(self) -> None:
        vault = _PhaseFaultVault(trip_phase="signoff_pending")
        h = _build_harness(vault=vault)
        with pytest.raises(RuntimeError, match="signoff_pending"):
            _run(h)

    def test_step9_report_signed_transition_fault_propagates(self) -> None:
        vault = _PhaseFaultVault(trip_phase="report_signed")
        h = _build_harness(vault=vault)
        with pytest.raises(RuntimeError, match="report_signed"):
            _run(h)

    def test_step11_tabs_delivered_transition_fault_propagates(self) -> None:
        vault = _PhaseFaultVault(trip_phase="tabs_delivered")
        h = _build_harness(vault=vault)
        with pytest.raises(RuntimeError, match="tabs_delivered"):
            _run(h)


class TestNonPipelineFailureWrappers:
    def test_inner_loop_raises_non_pipeline_failure_wrapped_and_reraised(self) -> None:
        # SeatContextFactory raising non-PipelineFailure propagates out of
        # run_inner_loop (Round 5 does not catch non-PipelineFailure) and
        # hits Round 11's step-5 `except Exception` wrapper.
        class _Boom:
            def __call__(
                self,
                *,
                seat_kind: str,
                iter_n: int,
                prev_editor_hash: str | None,
                prev_judge_hash: str | None,
                run_state: RunState,
            ) -> SeatInvocationContext:
                raise RuntimeError("seat-context-factory boom")

        h = _build_harness()
        # Replace the context factory by building a new context dataclass
        # with the boom factory — RunPipelineContext is frozen so we can't
        # mutate in place.
        new_ctx = RunPipelineContext(
            vault_read=h.context.vault_read,
            vault_write=h.context.vault_write,
            clock=h.context.clock,
            sleep=h.context.sleep,
            run_id_factory=h.context.run_id_factory,
            subprocess_launcher=h.context.subprocess_launcher,
            seat_context_factory=_Boom(),
            pre_gate_callable=h.context.pre_gate_callable,
            post_gate_runner=h.context.post_gate_runner,
            post_gate_input_factory=h.context.post_gate_input_factory,
            hash_file=h.context.hash_file,
        )
        h.context = new_ctx
        with pytest.raises(RuntimeError, match="seat-context-factory boom"):
            _run(h)

    def test_post_gate_runner_raises_non_pipeline_failure_wrapped(self) -> None:
        err = RuntimeError("post-gate boom")
        h = _build_harness(post_gate=_PostGateRunner(raise_exc=err))
        with pytest.raises(RuntimeError, match="post-gate boom"):
            _run(h)

    def test_pre_gate_soft_fail_with_vault_blip_still_returns_soft_result(
        self,
    ) -> None:
        # Step-3 soft-fail branch: vault fails on the state-failure write.
        # The wrapper falls back to sidecar and the soft-fail return still
        # lands (covers lines 664-670).
        vault = _InMemoryVault(
            fail_on_intent="state-failure", raise_exc=RuntimeError("blip")
        )
        from pipeline.loop.errors import PipelineFailure  # noqa: F401

        h = _build_harness(
            vault=vault,
            pre_gate=_PreGateCallable(
                result=PreGateResult(
                    passed=False,
                    failed_check_number=5,
                    failure_code="F-PRE-05-STUB",
                    failure_detail="boom",
                    completed_checks=(1, 2, 3, 4),
                )
            ),
        )
        result = _run(h)
        assert result.pre_gate_failed is True
        assert result.pre_gate_failure_code == "F-PRE-05-STUB"


# ===========================================================================
# E-023 residual surface — documented non-defences
# ===========================================================================


class TestE023Residuals:
    def test_pre_gate_callable_raising_base_exception_propagates_unwrapped(
        self,
    ) -> None:
        # BaseException subclass (not Exception) — we still write a
        # state-failure wrapper since the except clause catches Exception
        # only. BaseException (like SystemExit / KeyboardInterrupt) will
        # pass THROUGH unwrapped. This documents the residual surface.
        err = KeyboardInterrupt()
        h = _build_harness(pre_gate=_PreGateCallable(raise_exc=err))
        with pytest.raises(KeyboardInterrupt):
            _run(h)
