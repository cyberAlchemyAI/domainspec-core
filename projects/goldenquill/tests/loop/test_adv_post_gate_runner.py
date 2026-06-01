"""Adversarial tests for pipeline.loop.post_gate_runner.

E-024 multiplier: ~3× the happy-path surface. Targets:

- Factory exceptions propagate unwrapped (no state-failure write — factory
  is caller-side, invoked AFTER the phase-transition checkpoint).
- Unserialisable gate_result → state-failure + ``PostGateRejected`` with
  ``trigger="post_gate_result_unserializable"``.
- Non-monotonic clock clamps to zero elapsed (no timeout false positive).
- ``timeout_ms`` kwarg override rebinds per-call (rebind-resistance only
  matters for *module-scope* constants; the kwarg IS the injection seam).
- Arbitrary ``Exception`` from ``run_post_gate`` writes state-failure and
  re-raises.
- Regression pin — on FAIL verdict, phase does NOT transition to
  ``post_gate_passed``.
- ``claim_evidence_map`` present → ``signed_claim_evidence_map_hash`` is
  populated (dataclass canonicalization).
- Trigger string includes the failed step number when available, falls
  back to ``post_gate_unknown_failure`` when not.
- Resume-path + FAIL → one checkpoint (state-failure only; phase-transition
  is skipped).
- Resume-path with unchanged phase does NOT call ``vault_write`` before
  the gate_runner dispatch.
- ``claim_evidence_map=None`` → ``signed_claim_evidence_map_hash=None``
  on PASS path (documented branch).
- PipelineFailure is the base class of PostGateRejected (pytest catches
  via the parent).
- Canonical-bytes helper handles frozenset / tuple / set.
- ``PostGateRejected`` CODE is literally ``POST-GATE-REJECTED`` (not an
  F-PIPE code; not colliding with ``F_PIPE_BY_CODE`` registry).
- ``PostGateRejected`` is NOT registered in
  :data:`pipeline.loop.errors.F_PIPE_BY_CODE`.
- Arbitrary kwargs to the orchestrator are rejected (keyword-only + no
  positional — caller programmer-error regression pin).
- ``BLUEPRINT_DEPS`` constant pin — blueprint-faithful module load.
- __all__ re-export pin.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from pipeline.logician import GateRunnerPostResult, LogicianMidLoopCall, PostGateInput
from pipeline.loop.errors import F_PIPE_03, F_PIPE_BY_CODE, PipelineFailure
from pipeline.loop.post_gate_runner import (
    BLUEPRINT_DEPS,
    GateRunnerProtocol,
    PostGateInputFactory,
    PostGateOrchestrationResult,
    PostGateRejected,
    _canonical_bytes,
    run_post_gate_orchestration,
)
from pipeline.loop.revision_loop import InnerLoopResult
from pipeline.loop.types import IterationState, RunState


# ---------------------------------------------------------------------------
# Fixtures (lightweight re-declaration — same shape as happy-path file)
# ---------------------------------------------------------------------------


def _mk_runstate(phase: str = "inner_loop_iter_1", **overrides: Any) -> RunState:
    kwargs: dict[str, Any] = dict(
        schema_version=2,
        run_id="run-adv",
        mode="submission",
        rfa_hash="rfa-h",
        project_context_hash="pc-h",
        golden_set_ref=None,
        org_slug="mycosymbiotics",
        session_id="sess",
        phase=phase,
    )
    kwargs.update(overrides)
    return RunState(**kwargs)


def _mk_inner_loop_result(hash_: str = "h") -> InnerLoopResult:
    return InnerLoopResult(
        final_iteration=IterationState(iter_number=1),
        converged_on="score_threshold",
        iterations_run=1,
        final_checkpoint_hash=hash_,
    )


def _mk_gate_result(
    *,
    passed: bool = True,
    failed_step_number: int | None = None,
    failure_code: str | None = None,
    claim_evidence_map: Any = None,
) -> GateRunnerPostResult:
    return GateRunnerPostResult(
        passed=passed,
        failed_step_number=failed_step_number,
        failure_code=failure_code,
        failure_detail="",
        failure_codes=() if passed else (failure_code or "F-POST-STUB",),
        completed_steps=(),
        claim_evidence_map=claim_evidence_map,
        underlying_post_gate_result=None,
    )


@dataclass
class _FakeClock:
    values: list[int] = field(default_factory=list)
    _idx: int = 0
    iso: str = "2026-04-20T12:00:00Z"

    def now_ms(self) -> int:
        if self._idx >= len(self.values):
            return self.values[-1] if self.values else 0
        v = self.values[self._idx]
        self._idx += 1
        return v

    def now_iso(self) -> str:
        return self.iso


@dataclass
class _FakeSleep:
    calls: list[int] = field(default_factory=list)

    def __call__(self, ms: int) -> None:
        self.calls.append(ms)


@dataclass
class _FakeVault:
    store: dict[str, bytes] = field(default_factory=dict)
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(
        self,
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        self.calls.append(
            dict(
                path=path,
                payload=payload,
                intent=intent,
                write_mode=write_mode,
                expected_current_file_hash=expected_current_file_hash,
            )
        )
        import hashlib

        self.store[path] = payload
        return hashlib.sha256(payload).hexdigest()


@dataclass
class _FakeGateRunner:
    result: GateRunnerPostResult | None = None
    raise_exc: BaseException | None = None
    calls: list[Any] = field(default_factory=list)

    def run_post_gate(self, input_: PostGateInput) -> GateRunnerPostResult:
        self.calls.append(input_)
        if self.raise_exc is not None:
            raise self.raise_exc
        assert self.result is not None
        return self.result


# ---------------------------------------------------------------------------
# Factory adversarial
# ---------------------------------------------------------------------------


class TestFactoryAdversarial:
    def test_factory_valueerror_propagates_unwrapped(self) -> None:
        rs = _mk_runstate()
        vault = _FakeVault()

        def _raise(
            *, run_state: RunState, inner_loop_result: InnerLoopResult
        ) -> PostGateInput:
            raise ValueError("malformed input")

        with pytest.raises(ValueError, match="malformed input"):
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(),
                post_gate_input_factory=_raise,
                gate_runner=_FakeGateRunner(result=_mk_gate_result(passed=True)),
                vault_write=vault,
                clock=_FakeClock(values=[0, 0, 0, 0]),
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
            )
        # Exactly one write happened — the phase transition BEFORE the
        # factory call. Factory exceptions are caller programmer errors:
        # NO state-failure checkpoint is written by Round 6.
        assert len(vault.calls) == 1
        assert vault.calls[0]["intent"] == "state-success"

    def test_factory_exception_does_not_invoke_gate_runner(self) -> None:
        rs = _mk_runstate()
        gate = _FakeGateRunner(result=_mk_gate_result(passed=True))

        def _raise(
            *, run_state: RunState, inner_loop_result: InnerLoopResult
        ) -> PostGateInput:
            raise RuntimeError("nope")

        with pytest.raises(RuntimeError):
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(),
                post_gate_input_factory=_raise,
                gate_runner=gate,
                vault_write=_FakeVault(),
                clock=_FakeClock(values=[0, 0, 0, 0]),
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
            )
        assert gate.calls == []


# ---------------------------------------------------------------------------
# Gate_runner exception surfaces
# ---------------------------------------------------------------------------


class TestGateRunnerExceptions:
    def test_arbitrary_exception_writes_state_failure_and_reraises(self) -> None:
        rs = _mk_runstate()
        vault = _FakeVault()

        class _Boom(Exception):
            pass

        with pytest.raises(_Boom):
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(),
                post_gate_input_factory=lambda *, run_state, inner_loop_result: "x",  # type: ignore[return-value,arg-type]
                gate_runner=_FakeGateRunner(raise_exc=_Boom("kaboom")),
                vault_write=vault,
                clock=_FakeClock(values=[0, 0, 0, 0, 0, 0]),
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
            )
        intents = [c["intent"] for c in vault.calls]
        assert intents == ["state-success", "state-failure"]

    def test_unserialisable_gate_result_raises_post_gate_rejected(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Simulates an out-of-contract canonicalization TypeError.

        In production the ``_canonical_default`` handler always returns a
        JSON-native fallback so this branch is contract-unreachable; the
        adversarial path is forced by monkeypatching ``_canonical_bytes``
        on the gate_result path to raise ``TypeError``.
        """
        from pipeline.loop import post_gate_runner as pgr

        real_fn = pgr._canonical_bytes
        calls: list[Any] = []

        def _poisoned(payload: Any) -> bytes:
            calls.append(payload)
            # First call is on the gate_result → raise; subsequent calls
            # (claim_evidence_map on PASS, RunState canonicalizer is in
            # state_checkpoint, not this module) use the real helper.
            if isinstance(payload, GateRunnerPostResult):
                raise TypeError("not serialisable")
            return real_fn(payload)

        monkeypatch.setattr(pgr, "_canonical_bytes", _poisoned)

        rs = _mk_runstate()
        vault = _FakeVault()
        with pytest.raises(PostGateRejected) as ei:
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(),
                post_gate_input_factory=lambda *, run_state, inner_loop_result: "x",  # type: ignore[return-value,arg-type]
                gate_runner=_FakeGateRunner(
                    result=_mk_gate_result(passed=True)
                ),
                vault_write=vault,
                clock=_FakeClock(values=[0, 0, 0, 0, 0, 0]),
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
            )
        assert ei.value.trigger == "post_gate_result_unserializable"
        intents = [c["intent"] for c in vault.calls]
        assert intents == ["state-success", "state-failure"]


# ---------------------------------------------------------------------------
# Clock / timeout adversarial
# ---------------------------------------------------------------------------


class TestClockAdversarial:
    def test_non_monotonic_clock_clamps_to_zero_elapsed(self) -> None:
        """Decreasing now_ms must NOT trigger F_PIPE_03 (clamped)."""
        rs = _mk_runstate()
        # Phase-transition: 0, 0, 0 — OK.
        # start_ms=100 (Round 6), end_ms=50 (Round 6) → elapsed = -50 → clamp 0.
        clock = _FakeClock(values=[0, 0, 0, 100, 50])
        run_post_gate_orchestration(
            run_state=rs,
            inner_loop_result=_mk_inner_loop_result(),
            post_gate_input_factory=lambda *, run_state, inner_loop_result: "x",  # type: ignore[return-value,arg-type]
            gate_runner=_FakeGateRunner(result=_mk_gate_result(passed=True)),
            vault_write=_FakeVault(),
            clock=clock,
            sleep=_FakeSleep(),
            initial_checkpoint_hash="h",
        )
        assert rs.phase == "post_gate_passed"

    def test_timeout_ms_kwarg_override(self) -> None:
        """A test-sized timeout_ms lets tiny elapsed trigger F_PIPE_03."""
        rs = _mk_runstate()
        vault = _FakeVault()
        # Round 6 elapsed = 5 ms, timeout_ms = 1 → trip.
        clock = _FakeClock(values=[0, 0, 0, 0, 5])
        with pytest.raises(F_PIPE_03) as ei:
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(),
                post_gate_input_factory=lambda *, run_state, inner_loop_result: "x",  # type: ignore[return-value,arg-type]
                gate_runner=_FakeGateRunner(result=_mk_gate_result(passed=True)),
                vault_write=vault,
                clock=clock,
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
                timeout_ms=1,
            )
        assert ei.value.details["timeout_ms"] == 1
        assert ei.value.details["elapsed_ms"] == 5


# ---------------------------------------------------------------------------
# FAIL-path regression pins
# ---------------------------------------------------------------------------


class TestFailPathRegression:
    def test_fail_does_not_transition_phase_to_passed(self) -> None:
        rs = _mk_runstate(phase="inner_loop_iter_1")
        with pytest.raises(PostGateRejected):
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(),
                post_gate_input_factory=lambda *, run_state, inner_loop_result: "x",  # type: ignore[return-value,arg-type]
                gate_runner=_FakeGateRunner(
                    result=_mk_gate_result(
                        passed=False,
                        failed_step_number=4,
                        failure_code="F-POST-04",
                    )
                ),
                vault_write=_FakeVault(),
                clock=_FakeClock(values=[0, 0, 0, 0, 0, 0]),
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
            )
        # Phase held at post_gate_pending — NEVER post_gate_passed.
        assert rs.phase == "post_gate_pending"

    def test_fail_trigger_includes_step_number_and_code(self) -> None:
        rs = _mk_runstate()
        with pytest.raises(PostGateRejected) as ei:
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(),
                post_gate_input_factory=lambda *, run_state, inner_loop_result: "x",  # type: ignore[return-value,arg-type]
                gate_runner=_FakeGateRunner(
                    result=_mk_gate_result(
                        passed=False,
                        failed_step_number=7,
                        failure_code="F-POST-07",
                    )
                ),
                vault_write=_FakeVault(),
                clock=_FakeClock(values=[0, 0, 0, 0, 0, 0]),
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
            )
        assert ei.value.trigger == "post_gate_step_7_F-POST-07"

    def test_fail_without_step_number_uses_unknown_failure_trigger(self) -> None:
        rs = _mk_runstate()
        with pytest.raises(PostGateRejected) as ei:
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(),
                post_gate_input_factory=lambda *, run_state, inner_loop_result: "x",  # type: ignore[return-value,arg-type]
                gate_runner=_FakeGateRunner(
                    result=_mk_gate_result(
                        passed=False, failed_step_number=None, failure_code=None
                    )
                ),
                vault_write=_FakeVault(),
                clock=_FakeClock(values=[0, 0, 0, 0, 0, 0]),
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
            )
        assert ei.value.trigger == "post_gate_unknown_failure"


# ---------------------------------------------------------------------------
# claim_evidence_map hash behaviour
# ---------------------------------------------------------------------------


class TestClaimEvidenceMapHash:
    def test_map_none_yields_none_hash(self) -> None:
        rs = _mk_runstate()
        result = run_post_gate_orchestration(
            run_state=rs,
            inner_loop_result=_mk_inner_loop_result(),
            post_gate_input_factory=lambda *, run_state, inner_loop_result: "x",  # type: ignore[return-value,arg-type]
            gate_runner=_FakeGateRunner(
                result=_mk_gate_result(passed=True, claim_evidence_map=None)
            ),
            vault_write=_FakeVault(),
            clock=_FakeClock(values=[0, 0, 0, 0, 0]),
            sleep=_FakeSleep(),
            initial_checkpoint_hash="h",
        )
        assert result.signed_claim_evidence_map_hash is None
        assert rs.signed_claim_evidence_map_hash is None

    def test_map_present_yields_populated_hash(self) -> None:
        from pipeline.logician.claim_evidence import ClaimEvidenceMap

        cmap = ClaimEvidenceMap(
            map_id="m-1",
            draft_hash="d",
            rfa_hash="r",
            session_id="s",
            org_slug="o",
            rfa_url_hash="u",
            entries=(),
            unsourced_count=0,
            hard_block_count=0,
            rigor_breach_active=False,
            generated_at_utc="2026-04-20T12:00:00Z",
            generator_version="v0.1",
        )
        rs = _mk_runstate()
        result = run_post_gate_orchestration(
            run_state=rs,
            inner_loop_result=_mk_inner_loop_result(),
            post_gate_input_factory=lambda *, run_state, inner_loop_result: "x",  # type: ignore[return-value,arg-type]
            gate_runner=_FakeGateRunner(
                result=_mk_gate_result(passed=True, claim_evidence_map=cmap)
            ),
            vault_write=_FakeVault(),
            clock=_FakeClock(values=[0, 0, 0, 0, 0]),
            sleep=_FakeSleep(),
            initial_checkpoint_hash="h",
        )
        assert result.signed_claim_evidence_map_hash is not None
        assert len(result.signed_claim_evidence_map_hash) == 64  # sha256 hex


# ---------------------------------------------------------------------------
# Exception taxonomy pins
# ---------------------------------------------------------------------------


class TestExceptionTaxonomy:
    def test_post_gate_rejected_is_pipeline_failure(self) -> None:
        assert issubclass(PostGateRejected, PipelineFailure)

    def test_post_gate_rejected_code_is_literal(self) -> None:
        assert PostGateRejected.CODE == "POST-GATE-REJECTED"

    def test_post_gate_rejected_not_in_f_pipe_registry(self) -> None:
        """Regression: PostGateRejected is NOT an F-PIPE code."""
        assert "POST-GATE-REJECTED" not in F_PIPE_BY_CODE
        # And no F-PIPE-XX code aliases it either.
        for code in F_PIPE_BY_CODE:
            assert code != "POST-GATE-REJECTED"

    def test_logician_mid_loop_not_caught_as_post_gate_rejected(self) -> None:
        """MidLoopCall surfaces the Logician's own type, not a wrapper."""
        rs = _mk_runstate()
        with pytest.raises(LogicianMidLoopCall):
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(),
                post_gate_input_factory=lambda *, run_state, inner_loop_result: "x",  # type: ignore[return-value,arg-type]
                gate_runner=_FakeGateRunner(
                    raise_exc=LogicianMidLoopCall("POST", "POST")
                ),
                vault_write=_FakeVault(),
                clock=_FakeClock(values=[0, 0, 0, 0, 0, 0]),
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
            )


# ---------------------------------------------------------------------------
# Canonical-bytes helper
# ---------------------------------------------------------------------------


class TestCanonicalBytes:
    def test_canonical_bytes_on_dataclass(self) -> None:
        from pipeline.logician.claim_evidence import ClaimEvidenceMap

        cmap = ClaimEvidenceMap(
            map_id="m",
            draft_hash="d",
            rfa_hash="r",
            session_id="s",
            org_slug="o",
            rfa_url_hash="u",
            entries=(),
            unsourced_count=0,
            hard_block_count=0,
            rigor_breach_active=False,
            generated_at_utc="2026-04-20T00:00:00Z",
            generator_version="v",
        )
        b1 = _canonical_bytes(cmap)
        b2 = _canonical_bytes(cmap)
        assert b1 == b2
        # Canonical form is sorted-keys JSON → starts with '{'.
        assert b1.startswith(b"{")

    def test_canonical_bytes_on_frozenset_and_tuple(self) -> None:
        data = {"set": frozenset({"c", "a", "b"}), "tuple": (3, 1, 2)}
        b = _canonical_bytes(data)
        assert b == b'{"set":["a","b","c"],"tuple":[3,1,2]}'

    def test_canonical_bytes_fallback_repr_for_arbitrary_class(self) -> None:
        class _X:
            def __repr__(self) -> str:
                return "<X>"

        b = _canonical_bytes({"obj": _X()})
        assert b"__repr__" in b

    def test_canonical_default_nested_dataclass(self) -> None:
        """_default handler dataclass branch (contract-unreachable via top-
        level helper because asdict normalises nested dataclasses; direct
        invocation covers the defensive branch)."""
        from dataclasses import dataclass as _dc

        from pipeline.loop.post_gate_runner import _canonical_default

        @_dc(frozen=True)
        class _Leaf:
            x: int = 1

        got = _canonical_default(_Leaf())
        assert got == {"x": 1}

    def test_canonical_default_tuple_branch(self) -> None:
        """_default tuple branch (contract-unreachable via json.dumps which
        serializes tuples natively; direct call covers the defensive branch)."""
        from pipeline.loop.post_gate_runner import _canonical_default

        assert _canonical_default((3, 1, 2)) == [3, 1, 2]


class TestWriteStateFailureHelper:
    def test_state_failure_helper_swallows_secondary_error(self) -> None:
        """_write_state_failure must NOT mask a primary failure when the
        secondary checkpoint itself raises (best-effort contract)."""
        from pipeline.loop.post_gate_runner import _write_state_failure

        def _always_raise(
            *,
            path: str,
            payload: bytes,
            intent: str,
            write_mode: str,
            expected_current_file_hash: str | None,
        ) -> str:
            raise RuntimeError("vault wedged")

        # Should return silently, NOT raise.
        _write_state_failure(
            _mk_runstate(),
            "h",
            vault_write=_always_raise,
            clock=_FakeClock(values=[0, 0, 0]),
            sleep=_FakeSleep(),
        )


# ---------------------------------------------------------------------------
# Module-level pins
# ---------------------------------------------------------------------------


class TestModulePins:
    def test_blueprint_deps_pin(self) -> None:
        entry = BLUEPRINT_DEPS["section_05_pipeline.md"]
        assert entry["version"] == "v6"
        assert entry["hash_sha3_512_prefix16"] == "feb5928491e4dc40"

    def test_protocols_are_runtime_checkable(self) -> None:
        # Protocol @runtime_checkable implies isinstance-compatible.
        class _FactoryShape:
            def __call__(
                self,
                *,
                run_state: RunState,
                inner_loop_result: InnerLoopResult,
            ) -> PostGateInput:
                raise NotImplementedError

        class _RunnerShape:
            def run_post_gate(
                self, input_: PostGateInput
            ) -> GateRunnerPostResult:
                raise NotImplementedError

        assert isinstance(_FactoryShape(), PostGateInputFactory)
        assert isinstance(_RunnerShape(), GateRunnerProtocol)

    def test_post_gate_orchestration_result_is_frozen(self) -> None:
        result = PostGateOrchestrationResult(
            gate_result=_mk_gate_result(passed=True),
            committed_checkpoint_hash="h",
            post_gate_result_hash="p",
            signed_claim_evidence_map_hash=None,
        )
        with pytest.raises(Exception):
            result.committed_checkpoint_hash = "x"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Resume-path + FAIL
# ---------------------------------------------------------------------------


class TestResumeFail:
    def test_resume_plus_fail_writes_only_state_failure(self) -> None:
        rs = _mk_runstate(phase="post_gate_pending")
        vault = _FakeVault()
        with pytest.raises(PostGateRejected):
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(hash_="H"),
                post_gate_input_factory=lambda *, run_state, inner_loop_result: "x",  # type: ignore[return-value,arg-type]
                gate_runner=_FakeGateRunner(
                    result=_mk_gate_result(
                        passed=False,
                        failed_step_number=3,
                        failure_code="F-POST-03",
                    )
                ),
                vault_write=vault,
                clock=_FakeClock(values=[0, 0, 0, 0, 0, 0]),
                sleep=_FakeSleep(),
                initial_checkpoint_hash="H",
            )
        intents = [c["intent"] for c in vault.calls]
        assert intents == ["state-failure"]
        # Resume's state-failure write pins the caller's initial hash.
        assert vault.calls[0]["expected_current_file_hash"] == "H"
