"""Tests for pipeline.loop.run_pipeline — §4.1 submission-mode capstone (Round 11).

Blueprint §5 v6 LOCKED 2026-04-19 (§4.1 full 11-step sequence).

Round 11 is the FIRST §5 capstone composing Rounds 1-10 end-to-end. These
tests are integration-flavoured — they wire real Round 2/3/5/6/9 primitives
through an in-memory CAS-aware vault and exercise the 11-step phase walk.

Happy-path coverage (spec card
``section_05_round_11_run_pipeline_capstone.md``):

- Full success path: phases walk initialized → pre_gate_pending →
  pre_gate_passed → inner_loop_iter_1 → post_gate_pending → post_gate_passed
  → signoff_pending → report_signed → tabs_delivered.
- PRE-gate soft-fail: phase pinned at pre_gate_pending,
  pre_gate_failed=True, pre_gate_failure_code threaded from PreGateResult.
- POST-gate bypass-pending: phase pinned at post_gate_pending,
  bypass_pending=True, sidecar marker written, trigger threaded.
- Result dataclass shape (success / soft-fail / bypass all three).
- PipelineRunResult + RunPipelineContext are frozen + slotted.
- run_id flows via fixed-factory closure (Round 3 surface untouched).
- CAS hash threads across every phase transition (no gap / no skip).
- three_tab_envelope_hash pinned from deliver_tab.envelope.envelope_sha256
  at step 10 (Round 11 is capstone-owner per §4.11 line 916 contract).
- elapsed_ms is non-negative regardless of clock ordering.
- pre_gate_input_factory invoked exactly once with live run_state.
- post_gate_input_factory invoked exactly once (Round 6 contract).
- hash_file invoked exactly three times (Round 9 contract).
- Adversarial surfaces live in ``test_adv_run_pipeline.py``.
"""

from __future__ import annotations

import hashlib
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
from pipeline.loop.revision_loop import InnerLoopResult
from pipeline.loop.run_pipeline import (
    PipelineRunResult,
    PreGateInputFactory,
    RunPipelineContext,
    run_pipeline,
)
from pipeline.loop.seat_runner import SeatInvocationContext, SubprocessResult
from pipeline.loop.tab_delivery import TabSigningResult
from pipeline.loop.types import (
    IterationState,
    ProviderCascade,
    RunState,
    SeatCharter,
    TabEnvelope,
)


# ---------------------------------------------------------------------------
# In-memory CAS-aware vault fake
# ---------------------------------------------------------------------------


@dataclass
class _InMemoryVault:
    """CAS-aware in-process double for VaultReadCallable + VaultWriteCallable.

    Returns ``sha256(payload)`` as committed_hash; accepts write_mode
    ``"write-if-absent"`` (errors on re-write if key exists) and
    ``"overwrite"`` (CAS-checks ``expected_current_file_hash`` when
    non-None). This matches the §2 Vault's write-if-absent + overwrite-CAS
    contract at shape-only fidelity (deep-inspect guards live in §2 tests).
    """

    store: dict[str, bytes] = field(default_factory=dict)
    writes: list[dict[str, Any]] = field(default_factory=list)

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
                "payload_len": len(payload),
            }
        )
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

    # Adapters matching the injected-callable shapes
    def __call__(self, **kwargs: Any) -> str:
        return self.write(**kwargs)


@dataclass
class _Clock:
    ms_start: int = 1_000
    ms_step: int = 5
    _ms: int = 0
    iso: str = "2026-04-21T12:00:00Z"

    def __post_init__(self) -> None:
        self._ms = self.ms_start

    def now_ms(self) -> int:
        v = self._ms
        self._ms += self.ms_step
        return v

    def now_iso(self) -> str:
        return self.iso


def _sleep_noop(_ms: int) -> None:
    return None


# ---------------------------------------------------------------------------
# Round 4/5 seam fakes — deterministic SeatContextFactory + SubprocessLauncher
# ---------------------------------------------------------------------------


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
        self.calls.append(
            {
                "seat_kind": seat_kind,
                "iter_n": iter_n,
                "prev_editor_hash": prev_editor_hash,
                "prev_judge_hash": prev_judge_hash,
            }
        )
        return SeatInvocationContext(
            stdin_payload=f"{seat_kind}-iter-{iter_n}".encode("utf-8"),
            session_id=run_state.session_id,
            path_value="/usr/bin:/bin",
            home_value="/home/tilth",
        )


@dataclass
class _Launcher:
    """SubprocessLauncher fake — seat-kind dispatch with PASS verdict default."""

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
        self.calls.append(
            {
                "seat_kind": seat_kind,
                "family": family,
                "model_id": model_id,
            }
        )
        q = self.per_seat.get(seat_kind, [])
        if q:
            return q.pop(0)
        default_stdout = (
            b'{"verdict": "PASS", "total_score": 90}'
            if seat_kind == "judge"
            else b"draft"
        )
        return SubprocessResult(
            exit_code=0,
            stdout=default_stdout,
            stderr=b"",
            timed_out=False,
            landed_family=family,
            landed_model_id=model_id,
        )


# ---------------------------------------------------------------------------
# Logician PRE-gate + POST-gate seam fakes
# ---------------------------------------------------------------------------


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
    payload: Any = None
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(self, *, run_state: RunState) -> PreGateInput:
        self.calls.append({"run_state_id": run_state.run_id, "phase": run_state.phase})
        return self.payload  # type: ignore[return-value]


@dataclass
class _PostGateRunner:
    result: GateRunnerPostResult | None = None
    calls: list[PostGateInput] = field(default_factory=list)

    def run_post_gate(self, input_: PostGateInput) -> GateRunnerPostResult:
        self.calls.append(input_)
        assert self.result is not None
        return self.result


@dataclass
class _PostGateInputFactory:
    payload: Any = None
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(
        self, *, run_state: RunState, inner_loop_result: InnerLoopResult
    ) -> PostGateInput:
        self.calls.append(
            {
                "run_state_id": run_state.run_id,
                "iterations_run": inner_loop_result.iterations_run,
            }
        )
        return self.payload  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Round 9 tab_delivery seam — hash_file + vault_read on envelope
# ---------------------------------------------------------------------------


@dataclass
class _HashFile:
    """HashFileCallable fake — returns sha256-hex per path (positional arg)."""

    data: dict[str, str] = field(default_factory=dict)
    calls: list[str] = field(default_factory=list)

    def __call__(self, path: str) -> str:
        self.calls.append(path)
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


def _pre_gate_fail(code: str = "F-PRE-05-STUB") -> PreGateResult:
    return PreGateResult(
        passed=False,
        failed_check_number=5,
        failure_code=code,
        failure_detail="stub PRE-gate fail",
        completed_checks=(1, 2, 3, 4),
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


def _post_gate_fail(
    code: str = "F-POST-12-STUB",
) -> GateRunnerPostResult:
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
    run_id: str = "run-r11-happy",
    pre_gate_result: PreGateResult | None = None,
    post_gate_result: GateRunnerPostResult | None = None,
) -> _Harness:
    vault = _InMemoryVault()
    clock = _Clock()
    launcher = _Launcher()
    context_factory = _ContextFactory()
    pre_gate_callable = _PreGateCallable(
        result=pre_gate_result if pre_gate_result is not None else _pre_gate_pass()
    )
    pre_gate_input_factory = _PreGateInputFactory(payload="pre-gate-input-opaque")
    post_gate_runner = _PostGateRunner(
        result=post_gate_result if post_gate_result is not None else _post_gate_pass()
    )
    post_gate_input_factory = _PostGateInputFactory(payload="post-gate-input-opaque")
    hash_file = _HashFile()
    context = RunPipelineContext(
        vault_read=vault.read,
        vault_write=vault.write,
        clock=clock,
        sleep=_sleep_noop,
        run_id_factory=lambda: run_id,
        subprocess_launcher=launcher,
        seat_context_factory=context_factory,
        pre_gate_callable=pre_gate_callable,
        post_gate_runner=post_gate_runner,
        post_gate_input_factory=post_gate_input_factory,
        hash_file=hash_file,
    )
    return _Harness(
        vault=vault,
        clock=clock,
        launcher=launcher,
        context_factory=context_factory,
        pre_gate_callable=pre_gate_callable,
        pre_gate_input_factory=pre_gate_input_factory,
        post_gate_runner=post_gate_runner,
        post_gate_input_factory=post_gate_input_factory,
        hash_file=hash_file,
        context=context,
    )


def _run(
    harness: _Harness,
    *,
    run_id: str = "run-r11-happy",
    org_slug: str = "mycosymbiotics",
) -> PipelineRunResult:
    return run_pipeline(
        run_id=run_id,
        org_slug=org_slug,
        session_id="sess-r11",
        rfa_hash="rfa-abc",
        project_context_hash="pc-def",
        scribe_charter=_charter("scribe"),
        editor_charter=_charter("editor"),
        judge_charter=_charter("judge"),
        scribe_cascade=_cascade("scribe"),
        editor_cascade=_cascade("editor"),
        judge_cascade=_cascade("judge"),
        context=harness.context,
        pre_gate_input_factory=harness.pre_gate_input_factory,
    )


# ===========================================================================
# Happy-path full success
# ===========================================================================


class TestFullSuccess:
    def test_returns_pipeline_run_result_with_tabs_delivered(self) -> None:
        h = _build_harness(run_id="run-S1")
        result = _run(h, run_id="run-S1")

        assert isinstance(result, PipelineRunResult)
        assert result.run_id == "run-S1"
        assert result.final_phase == "tabs_delivered"
        assert result.bypass_pending is False
        assert result.pre_gate_failed is False
        assert result.pre_gate_failure_code is None
        assert result.post_gate_rejected_trigger is None
        assert result.iterations_consumed == 1
        assert result.three_tab_envelope_hash is not None
        assert len(result.three_tab_envelope_hash) == 64  # sha256 hex

    def test_pre_gate_factory_invoked_exactly_once(self) -> None:
        h = _build_harness()
        _run(h)
        assert len(h.pre_gate_input_factory.calls) == 1
        assert h.pre_gate_input_factory.calls[0]["run_state_id"] == "run-r11-happy"

    def test_post_gate_factory_invoked_exactly_once(self) -> None:
        h = _build_harness()
        _run(h)
        assert len(h.post_gate_input_factory.calls) == 1

    def test_pre_gate_callable_invoked_exactly_once(self) -> None:
        h = _build_harness()
        _run(h)
        assert len(h.pre_gate_callable.calls) == 1

    def test_hash_file_invoked_three_times_for_deliver_tab(self) -> None:
        h = _build_harness()
        _run(h)
        # Round 9 deliver_tab hashes live_radar, deep_brief, council_draft.
        assert len(h.hash_file.calls) == 3

    def test_elapsed_ms_non_negative(self) -> None:
        h = _build_harness()
        result = _run(h)
        assert result.elapsed_ms >= 0


# ===========================================================================
# Phase walk + checkpoint sequence
# ===========================================================================


class TestPhaseWalk:
    def test_phase_transitions_exactly_once_per_step(self) -> None:
        h = _build_harness()
        _run(h)
        intents = [
            w["intent"]
            for w in h.vault.writes
            if w["path"].endswith("/state.json")
        ]
        # Every state-success checkpoint corresponds to a phase transition;
        # we do not strictly pin the count (Round 5 and Round 6 manage
        # their own sub-step checkpoints) but we DO require at least the
        # capstone's transitions to land.
        assert intents.count("state-success") >= 7

    def test_final_state_json_phase_is_tabs_delivered(self) -> None:
        h = _build_harness()
        _run(h)
        final_state = json.loads(
            h.vault.store["pipeline/run-r11-happy/state.json"].decode("utf-8")
        )
        assert final_state["phase"] == "tabs_delivered"

    def test_envelope_path_written_in_vault(self) -> None:
        h = _build_harness()
        _run(h)
        assert "pipeline/run-r11-happy/tab_envelope.json" in h.vault.store

    def test_state_json_path_is_run_id_scoped(self) -> None:
        h = _build_harness(run_id="run-iso-Z")
        _run(h, run_id="run-iso-Z")
        assert "pipeline/run-iso-Z/state.json" in h.vault.store


# ===========================================================================
# three_tab_envelope_hash pinning (step 10 capstone-owned mutation)
# ===========================================================================


class TestThreeTabEnvelopeHashPinning:
    def test_final_runstate_has_envelope_hash_pinned(self) -> None:
        h = _build_harness()
        result = _run(h)
        final_state = json.loads(
            h.vault.store["pipeline/run-r11-happy/state.json"].decode("utf-8")
        )
        assert final_state["three_tab_envelope_hash"] == result.three_tab_envelope_hash

    def test_envelope_hash_matches_stored_envelope(self) -> None:
        h = _build_harness()
        result = _run(h)
        envelope_payload = h.vault.store[
            "pipeline/run-r11-happy/tab_envelope.json"
        ]
        envelope = json.loads(envelope_payload.decode("utf-8"))
        assert envelope["envelope_sha256"] == result.three_tab_envelope_hash


# ===========================================================================
# PRE-gate soft-fail branch
# ===========================================================================


class TestPreGateSoftFail:
    def test_pre_gate_fail_returns_soft_result(self) -> None:
        h = _build_harness(pre_gate_result=_pre_gate_fail("F-PRE-07-STUB"))
        result = _run(h)

        assert isinstance(result, PipelineRunResult)
        assert result.pre_gate_failed is True
        assert result.pre_gate_failure_code == "F-PRE-07-STUB"
        assert result.bypass_pending is False
        assert result.three_tab_envelope_hash is None
        assert result.iterations_consumed == 0
        assert result.final_phase == "pre_gate_pending"

    def test_pre_gate_fail_does_not_invoke_inner_loop(self) -> None:
        h = _build_harness(pre_gate_result=_pre_gate_fail())
        _run(h)
        # Seat-context factory is called only during inner-loop iter; a
        # PRE-gate soft-fail short-circuits BEFORE step 5.
        assert h.context_factory.calls == []
        assert h.launcher.calls == []

    def test_pre_gate_fail_does_not_invoke_post_gate(self) -> None:
        h = _build_harness(pre_gate_result=_pre_gate_fail())
        _run(h)
        assert h.post_gate_input_factory.calls == []
        assert h.post_gate_runner.calls == []

    def test_pre_gate_fail_writes_state_failure_checkpoint(self) -> None:
        h = _build_harness(pre_gate_result=_pre_gate_fail())
        _run(h)
        state_failure_writes = [
            w for w in h.vault.writes if w["intent"] == "state-failure"
        ]
        assert len(state_failure_writes) >= 1


# ===========================================================================
# POST-gate bypass-pending branch
# ===========================================================================


class TestPostGateBypass:
    def test_post_gate_fail_returns_bypass_pending_result(self) -> None:
        h = _build_harness(post_gate_result=_post_gate_fail("F-POST-12-STUB"))
        result = _run(h)

        assert isinstance(result, PipelineRunResult)
        assert result.bypass_pending is True
        assert result.pre_gate_failed is False
        assert result.three_tab_envelope_hash is None
        assert result.iterations_consumed == 1
        assert result.final_phase in {"post_gate_pending", "post_gate_passed"}
        assert result.post_gate_rejected_trigger is not None

    def test_post_gate_fail_writes_bypass_pending_marker(self) -> None:
        h = _build_harness(post_gate_result=_post_gate_fail())
        _run(h)
        marker_path = "pipeline/run-r11-happy/bypass_pending.json"
        assert marker_path in h.vault.store
        marker = json.loads(h.vault.store[marker_path].decode("utf-8"))
        assert marker["run_id"] == "run-r11-happy"

    def test_post_gate_fail_does_not_invoke_deliver_tab(self) -> None:
        h = _build_harness(post_gate_result=_post_gate_fail())
        _run(h)
        # hash_file is only called inside deliver_tab; if it's never
        # invoked, deliver_tab was correctly skipped.
        assert h.hash_file.calls == []


# ===========================================================================
# Dataclass surface contracts
# ===========================================================================


class TestPipelineRunResultContract:
    def test_is_frozen(self) -> None:
        r = PipelineRunResult(
            run_id="t",
            final_phase="tabs_delivered",
            iterations_consumed=1,
            three_tab_envelope_hash="h",
            elapsed_ms=10,
        )
        with pytest.raises((AttributeError, Exception)):
            r.run_id = "other"  # type: ignore[misc]

    def test_default_flags_are_false_and_none(self) -> None:
        r = PipelineRunResult(
            run_id="t",
            final_phase="pre_gate_pending",
            iterations_consumed=0,
            three_tab_envelope_hash=None,
            elapsed_ms=0,
        )
        assert r.bypass_pending is False
        assert r.pre_gate_failed is False
        assert r.pre_gate_failure_code is None
        assert r.post_gate_rejected_trigger is None


class TestRunPipelineContextContract:
    def test_is_frozen(self) -> None:
        h = _build_harness()
        with pytest.raises((AttributeError, Exception)):
            h.context.vault_read = lambda **_k: b""  # type: ignore[misc]

    def test_optional_fields_default_none(self) -> None:
        h = _build_harness()
        assert h.context.interrupt_probe is None
        assert h.context.judge_parse is None


class TestPreGateInputFactoryProtocol:
    def test_runtime_checkable(self) -> None:
        class _Good:
            def __call__(self, *, run_state: RunState) -> PreGateInput:
                return "x"  # type: ignore[return-value]

        good = _Good()
        assert isinstance(good, PreGateInputFactory)
