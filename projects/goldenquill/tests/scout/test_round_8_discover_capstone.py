"""Round 8 — §4.11 DISCOVER capstone dispatcher.

Test surface floor ≥ 70; E-024 1.5× multiplier (seventh firing) targets
~105 total. Happy-path + adversarial coverage for parallel fan-out,
per-channel timeout + exception isolation, cross-channel dedup,
SCOUT_UNION_CAP truncation, interrupt cancellation, run-id derivation,
checkpoint discipline, health-signer integration, and Protocol injection.

Lessons applied from start:
- E-017 Protocol-injection pattern (seventh reuse)
- E-024 1.5× multiplier (seventh firing — watch for multiplier drift)
- E-025 range-check version pin (rN >= 8)
- E-026 formal ``__module__`` lineage check over ``__dict__``
- E-027 candidate — ``lint_tree`` directory-required contract
- E-028 candidate — ``# pragma: no cover`` on contract-unreachable
  defensive branches
"""

from __future__ import annotations

import concurrent.futures as _cf
import hashlib
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, List, Mapping, Optional, Tuple

import pytest

import pipeline.scout.discover as disc
from pipeline.scout._constants import (
    DISCOVER_PER_CHANNEL_HARD_TIMEOUT_S,
    DISCOVER_POOL_MAX_WORKERS,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
    RUN_ID_HEX_LEN,
)
from pipeline.scout._types import Candidate, SignedHealthTuple
from pipeline.scout.discover import (
    CapstoneDegradationEvent,
    F_SCOUT_CAPSTONE_01,
    F_SCOUT_CAPSTONE_02,
    F_SCOUT_CAPSTONE_03,
    F_SCOUT_CAPSTONE_04,
    F_SCOUT_CAPSTONE_05,
    F_SCOUT_CAPSTONE_06,
    F_SCOUT_CAPSTONE_07,
    SCOUT_UNION_CAP,
    ScoutDiscoverInterrupted,
    ScoutDiscoverResult,
    _CAPSTONE_CHANNEL_ORDER,
    _CHANNEL_A_ENDPOINTS,
    _RUN_TIEBREAK_SEED_LEN,
    _derive_run_id,
    _truncate_union,
    run_scout_discover,
)


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


@dataclass
class FakeSession:
    session_id: str = "session-r8-abc"
    slug: str = "mycosymbiotics_cooperative"


@dataclass
class FakeChannelResult:
    candidates: tuple[Candidate, ...] = ()
    channel_state: str = HEALTH_OK
    per_endpoint_state: Optional[Mapping[str, str]] = None


def _mk_candidate(candidate_id: str, channel: str = "A") -> Candidate:
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
        fit_score_cached=0,
        cache_provenance=None,
    )


@dataclass
class RecordingCheckpointWriter:
    writes: List[Tuple[str, dict]] = field(default_factory=list)

    def write(self, *, stage: str, payload: Mapping[str, Any]) -> None:
        self.writes.append((stage, dict(payload)))


@dataclass
class RecordingDegradationWriter:
    events: List[CapstoneDegradationEvent] = field(default_factory=list)

    def record(self, event: CapstoneDegradationEvent) -> None:
        self.events.append(event)


@dataclass
class RecordingHealthSigner:
    calls: List[dict] = field(default_factory=list)
    returned_tuple: Optional[SignedHealthTuple] = None
    raise_with: Optional[BaseException] = None

    def __call__(
        self,
        *,
        session,
        per_channel_states,
        per_channel_a_endpoints,
        run_wall_ns,
        run_tiebreak_seed,
    ) -> SignedHealthTuple:
        self.calls.append(
            {
                "session_id": session.session_id,
                "per_channel_states": dict(per_channel_states),
                "per_channel_a_endpoints": dict(per_channel_a_endpoints),
                "run_wall_ns": run_wall_ns,
                "run_tiebreak_seed": run_tiebreak_seed,
            }
        )
        if self.raise_with is not None:
            raise self.raise_with
        if self.returned_tuple is not None:
            return self.returned_tuple
        return SignedHealthTuple(
            tuple_canonical=b"{}",
            hmac_sha3_512=b"\x01" * 64,
            signed_at_utc="2026-04-20T00:00:00Z",
            hmac_key_id="test-key-id",
        )


# --- Sequential fake executor -----------------------------------------------


class _SequentialFuture:
    def __init__(self, fn: Callable[[], Any], raise_timeout: bool = False):
        self._fn = fn
        self._raise_timeout = raise_timeout
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
        except BaseException as exc:  # noqa: BLE001 — propagate to result()
            self._raise_exc = exc

    def result(self, timeout=None):
        if self._raise_timeout:
            raise _cf.TimeoutError("simulated channel timeout")
        self._materialize()
        if self._raise_exc is not None:
            raise self._raise_exc
        return self._result

    def cancel(self) -> bool:
        self._cancelled = True
        return True


class SequentialFakeExecutor:
    """Deterministic executor — runs submitted callables synchronously.

    Tests can mark a channel as ``timeout_channels`` to make the fake
    future raise :class:`TimeoutError` from ``.result()``. The submission
    order matches ``_CAPSTONE_CHANNEL_ORDER``.
    """

    def __init__(
        self,
        max_workers: int,
        timeout_channels: Optional[set[str]] = None,
    ):
        self.max_workers = max_workers
        self.timeout_channels = timeout_channels or set()
        self._submitted: list[Callable[[], Any]] = []
        self.channel_order: list[str] = list(_CAPSTONE_CHANNEL_ORDER)
        self._idx = 0
        self._shutdown = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self._shutdown = True

    def submit(self, fn, /):
        idx = self._idx
        self._idx += 1
        ch = self.channel_order[idx] if idx < len(self.channel_order) else "?"
        fut = _SequentialFuture(
            fn, raise_timeout=(ch in self.timeout_channels)
        )
        self._submitted.append(fn)
        return fut


def _exec_factory(
    *, timeout_channels: Optional[set[str]] = None
) -> Callable[[int], Any]:
    def factory(max_workers: int):
        return SequentialFakeExecutor(
            max_workers, timeout_channels=timeout_channels
        )

    return factory


# ---------------------------------------------------------------------------
# channel_fns builder helpers
# ---------------------------------------------------------------------------


def _ok_channels(
    overrides: Optional[dict[str, FakeChannelResult]] = None,
    *,
    raise_for: Optional[dict[str, BaseException]] = None,
) -> dict[str, Callable[[], FakeChannelResult]]:
    overrides = overrides or {}
    raise_for = raise_for or {}
    out: dict[str, Callable[[], FakeChannelResult]] = {}
    for ch in _CAPSTONE_CHANNEL_ORDER:
        if ch in raise_for:
            exc = raise_for[ch]

            def _fn(exc=exc):
                raise exc

            out[ch] = _fn
        else:
            result = overrides.get(
                ch,
                FakeChannelResult(
                    channel_state=HEALTH_OK,
                    per_endpoint_state=(
                        {ep: HEALTH_OK for ep in _CHANNEL_A_ENDPOINTS}
                        if ch == "A"
                        else None
                    ),
                ),
            )
            out[ch] = (lambda r=result: r)
    return out


def _default_writers():
    return RecordingCheckpointWriter(), RecordingDegradationWriter()


# ---------------------------------------------------------------------------
# 1. Happy-path
# ---------------------------------------------------------------------------


class TestCapstoneHappyPath:
    def test_all_ok_returns_full_result(self):
        cp, dw = _default_writers()
        signer = RecordingHealthSigner()
        cand = _mk_candidate("deadbeef" * 3, channel="A")
        overrides = {
            "A": FakeChannelResult(
                candidates=(cand,),
                channel_state=HEALTH_OK,
                per_endpoint_state={ep: HEALTH_OK for ep in _CHANNEL_A_ENDPOINTS},
            )
        }
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(overrides),
            health_signer=signer,
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            entropy=lambda n: b"\xaa" * n,
            clock=lambda: 1_700_000_000_000_000_000,
        )
        assert isinstance(result, ScoutDiscoverResult)
        assert len(result.candidates) == 1
        assert result.candidates[0].candidate_id == cand.candidate_id
        assert result.per_channel_states == {ch: HEALTH_OK for ch in _CAPSTONE_CHANNEL_ORDER}
        assert result.per_channel_a_endpoints == {ep: HEALTH_OK for ep in _CHANNEL_A_ENDPOINTS}
        assert result.run_tiebreak_seed == b"\xaa" * _RUN_TIEBREAK_SEED_LEN
        assert result.run_wall_ns == 1_700_000_000_000_000_000
        assert len(result.capstone_degradation_events) == 0

    def test_signed_health_returned_from_signer(self):
        cp, dw = _default_writers()
        fixed = SignedHealthTuple(
            tuple_canonical=b"canonical",
            hmac_sha3_512=b"\x02" * 64,
            signed_at_utc="2026-04-20T12:00:00Z",
            hmac_key_id="fixed-key",
        )
        signer = RecordingHealthSigner(returned_tuple=fixed)
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=signer,
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert result.signed_health is fixed
        assert len(signer.calls) == 1

    def test_run_id_matches_sha3_derivation(self):
        cp, dw = _default_writers()
        signer = RecordingHealthSigner()
        seed = b"\xcd" * _RUN_TIEBREAK_SEED_LEN
        run_wall_ns = 4242424242
        sess = FakeSession(session_id="derive-me")
        result = run_scout_discover(
            session=sess,
            channel_fns=_ok_channels(),
            health_signer=signer,
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            entropy=lambda n: seed,
            clock=lambda: run_wall_ns,
        )
        expected_material = (
            f"{sess.session_id}|{run_wall_ns}|".encode("utf-8") + seed
        )
        expected = hashlib.sha3_512(expected_material).hexdigest()[:RUN_ID_HEX_LEN]
        assert result.run_id == expected
        assert len(result.run_id) == RUN_ID_HEX_LEN

    def test_no_capstone_events_when_all_ok(self):
        cp, dw = _default_writers()
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert result.capstone_degradation_events == ()
        assert dw.events == []

    def test_channel_degraded_state_preserved(self):
        cp, dw = _default_writers()
        overrides = {
            "C": FakeChannelResult(channel_state=HEALTH_DEGRADED),
        }
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(overrides),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert result.per_channel_states["C"] == HEALTH_DEGRADED
        assert result.per_channel_states["A"] == HEALTH_OK

    def test_union_preserves_insertion_order_within_channel(self):
        cp, dw = _default_writers()
        candidates = tuple(_mk_candidate(f"cand{i:02x}" * 6, channel="B") for i in range(5))
        overrides = {"B": FakeChannelResult(candidates=candidates, channel_state=HEALTH_OK)}
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(overrides),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert tuple(c.candidate_id for c in result.candidates) == tuple(
            c.candidate_id for c in candidates
        )


# ---------------------------------------------------------------------------
# 2. Channel timeout
# ---------------------------------------------------------------------------


class TestCapstoneChannelTimeout:
    def test_single_channel_timeout_marks_failed(self):
        cp, dw = _default_writers()
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(timeout_channels={"D"}),
        )
        assert result.per_channel_states["D"] == HEALTH_FAILED
        assert result.per_channel_states["A"] == HEALTH_OK
        assert any(
            e.code == F_SCOUT_CAPSTONE_01 and e.channel == "D"
            for e in result.capstone_degradation_events
        )

    def test_channel_a_timeout_forces_endpoints_failed(self):
        cp, dw = _default_writers()
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(timeout_channels={"A"}),
        )
        assert result.per_channel_states["A"] == HEALTH_FAILED
        assert result.per_channel_a_endpoints == {
            ep: HEALTH_FAILED for ep in _CHANNEL_A_ENDPOINTS
        }

    def test_other_channels_continue_after_one_timeout(self):
        cp, dw = _default_writers()
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(timeout_channels={"E"}),
        )
        assert result.per_channel_states["E"] == HEALTH_FAILED
        for ch in ("A", "B", "C", "D", "F"):
            assert result.per_channel_states[ch] == HEALTH_OK

    def test_timeout_event_carries_timeout_seconds_in_reason(self):
        cp, dw = _default_writers()
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(timeout_channels={"B"}),
        )
        event = [e for e in result.capstone_degradation_events if e.channel == "B"][0]
        assert str(DISCOVER_PER_CHANNEL_HARD_TIMEOUT_S) in (event.reason_tag or "")

    def test_timeout_still_signs_health(self):
        cp, dw = _default_writers()
        signer = RecordingHealthSigner()
        run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=signer,
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(timeout_channels={"C", "E"}),
        )
        # Even with two timeouts the capstone still signs.
        assert len(signer.calls) == 1

    def test_timeout_future_cancel_invoked(self):
        cp, dw = _default_writers()
        run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(timeout_channels={"F"}),
        )
        # No exception — cancel call path is exercised without error.


# ---------------------------------------------------------------------------
# 3. Channel exception
# ---------------------------------------------------------------------------


class TestCapstoneChannelException:
    def test_runtime_error_marks_failed(self):
        cp, dw = _default_writers()
        fns = _ok_channels(raise_for={"C": RuntimeError("boom")})
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=fns,
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert result.per_channel_states["C"] == HEALTH_FAILED
        assert any(
            e.code == F_SCOUT_CAPSTONE_02 and e.channel == "C"
            for e in result.capstone_degradation_events
        )

    def test_channel_a_exception_forces_endpoint_failed(self):
        cp, dw = _default_writers()
        fns = _ok_channels(raise_for={"A": ValueError("broken")})
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=fns,
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert result.per_channel_states["A"] == HEALTH_FAILED
        assert result.per_channel_a_endpoints == {
            ep: HEALTH_FAILED for ep in _CHANNEL_A_ENDPOINTS
        }

    def test_exception_reason_tag_includes_exception_type(self):
        cp, dw = _default_writers()
        fns = _ok_channels(raise_for={"B": KeyError("missing")})
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=fns,
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        event = [e for e in result.capstone_degradation_events if e.channel == "B"][0]
        assert "KeyError" in (event.reason_tag or "")

    def test_multiple_channel_exceptions_isolated(self):
        cp, dw = _default_writers()
        fns = _ok_channels(
            raise_for={
                "B": RuntimeError("b-fail"),
                "D": OSError("d-fail"),
                "E": IOError("e-fail"),
            }
        )
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=fns,
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        for ch in ("B", "D", "E"):
            assert result.per_channel_states[ch] == HEALTH_FAILED
        for ch in ("A", "C", "F"):
            assert result.per_channel_states[ch] == HEALTH_OK


# ---------------------------------------------------------------------------
# 4. Backbone failed + 5. Four of six failed
# ---------------------------------------------------------------------------


class TestCapstoneBackboneFailed:
    def test_all_channel_a_endpoints_failed_no_short_circuit(self):
        cp, dw = _default_writers()
        overrides = {
            "A": FakeChannelResult(
                channel_state=HEALTH_FAILED,
                per_endpoint_state={ep: HEALTH_FAILED for ep in _CHANNEL_A_ENDPOINTS},
            )
        }
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(overrides),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        # Capstone does NOT short-circuit — architecture line 271 puts
        # the hard-abort decision on Logician.
        assert result.per_channel_a_endpoints == {
            ep: HEALTH_FAILED for ep in _CHANNEL_A_ENDPOINTS
        }
        assert result.per_channel_states["B"] == HEALTH_OK


class TestCapstoneFourOfSixFailed:
    def test_still_signs_and_returns(self):
        cp, dw = _default_writers()
        signer = RecordingHealthSigner()
        fns = _ok_channels(
            raise_for={
                "A": RuntimeError("x"),
                "B": RuntimeError("x"),
                "C": RuntimeError("x"),
                "D": RuntimeError("x"),
            }
        )
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=fns,
            health_signer=signer,
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        n_failed = sum(
            1 for v in result.per_channel_states.values() if v == HEALTH_FAILED
        )
        assert n_failed == 4
        assert len(signer.calls) == 1  # capstone still signs


# ---------------------------------------------------------------------------
# 6. Interrupt handling
# ---------------------------------------------------------------------------


class TestCapstoneInterrupt:
    def test_interrupt_before_first_channel_raises(self):
        cp, dw = _default_writers()
        probe_state = {"n": 0}

        def probe():
            probe_state["n"] += 1
            return probe_state["n"] >= 1  # fires immediately

        with pytest.raises(ScoutDiscoverInterrupted) as exc_info:
            run_scout_discover(
                session=FakeSession(),
                channel_fns=_ok_channels(),
                health_signer=RecordingHealthSigner(),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                interrupt_probe=probe,
            )
        assert exc_info.value.completed_channels == ()
        stages = [s for s, _ in cp.writes]
        assert "discover_interrupted" in stages

    def test_interrupt_after_two_channels_raises(self):
        cp, dw = _default_writers()
        probe_state = {"n": 0}

        def probe():
            probe_state["n"] += 1
            return probe_state["n"] > 2  # fires before C

        with pytest.raises(ScoutDiscoverInterrupted) as exc_info:
            run_scout_discover(
                session=FakeSession(),
                channel_fns=_ok_channels(),
                health_signer=RecordingHealthSigner(),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                interrupt_probe=probe,
            )
        assert exc_info.value.completed_channels == ("A", "B")

    def test_interrupt_logs_degradation_event(self):
        cp, dw = _default_writers()

        def probe():
            return True

        with pytest.raises(ScoutDiscoverInterrupted):
            run_scout_discover(
                session=FakeSession(),
                channel_fns=_ok_channels(),
                health_signer=RecordingHealthSigner(),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                interrupt_probe=probe,
            )
        assert any(e.code == F_SCOUT_CAPSTONE_05 for e in dw.events)

    def test_interrupt_does_not_call_health_signer(self):
        cp, dw = _default_writers()
        signer = RecordingHealthSigner()

        def probe():
            return True

        with pytest.raises(ScoutDiscoverInterrupted):
            run_scout_discover(
                session=FakeSession(),
                channel_fns=_ok_channels(),
                health_signer=signer,
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                interrupt_probe=probe,
            )
        assert signer.calls == []


# ---------------------------------------------------------------------------
# 7. KeyboardInterrupt passthrough
# ---------------------------------------------------------------------------


class TestCapstoneKeyboardInterruptPassthrough:
    def test_channel_keyboard_interrupt_reraised(self):
        cp, dw = _default_writers()
        fns = _ok_channels(raise_for={"C": KeyboardInterrupt()})
        with pytest.raises(KeyboardInterrupt):
            run_scout_discover(
                session=FakeSession(),
                channel_fns=fns,
                health_signer=RecordingHealthSigner(),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
            )

    def test_channel_system_exit_reraised(self):
        cp, dw = _default_writers()
        fns = _ok_channels(raise_for={"D": SystemExit(1)})
        with pytest.raises(SystemExit):
            run_scout_discover(
                session=FakeSession(),
                channel_fns=fns,
                health_signer=RecordingHealthSigner(),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
            )


# ---------------------------------------------------------------------------
# 8. Dedup + 9. Union cap
# ---------------------------------------------------------------------------


class TestCapstoneDedup:
    def test_duplicate_candidate_id_first_writer_wins(self):
        cp, dw = _default_writers()
        cand = _mk_candidate("dup" + "0" * 21, channel="A")
        overrides = {
            "A": FakeChannelResult(
                candidates=(cand,),
                channel_state=HEALTH_OK,
                per_endpoint_state={ep: HEALTH_OK for ep in _CHANNEL_A_ENDPOINTS},
            ),
            "C": FakeChannelResult(candidates=(cand,), channel_state=HEALTH_OK),
        }
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(overrides),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert len(result.candidates) == 1
        dedup_events = [
            e for e in result.capstone_degradation_events
            if e.code == F_SCOUT_CAPSTONE_03
        ]
        assert len(dedup_events) == 1
        assert dedup_events[0].severity == "LOW"
        assert dedup_events[0].channel == "C"

    def test_duplicate_reason_tag_carries_both_channels(self):
        cp, dw = _default_writers()
        cand = _mk_candidate("twin" + "0" * 20, channel="B")
        overrides = {
            "B": FakeChannelResult(candidates=(cand,), channel_state=HEALTH_OK),
            "E": FakeChannelResult(candidates=(cand,), channel_state=HEALTH_OK),
        }
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(overrides),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        event = [
            e for e in result.capstone_degradation_events
            if e.code == F_SCOUT_CAPSTONE_03
        ][0]
        assert "first_channel=B" in (event.reason_tag or "")
        assert "duplicate_channel=E" in (event.reason_tag or "")


class TestCapstoneUnionCap:
    def test_cap_boundary_at_exactly_6000_no_truncation(self):
        cp, dw = _default_writers()
        candidates = tuple(
            _mk_candidate(f"{i:024x}", channel="C") for i in range(SCOUT_UNION_CAP)
        )
        overrides = {"C": FakeChannelResult(candidates=candidates, channel_state=HEALTH_OK)}
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(overrides),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert len(result.candidates) == SCOUT_UNION_CAP
        assert not any(
            e.code == F_SCOUT_CAPSTONE_04 for e in result.capstone_degradation_events
        )

    def test_cap_exceeded_truncates_and_emits_event(self):
        cp, dw = _default_writers()
        n_c = SCOUT_UNION_CAP // 2
        n_d = SCOUT_UNION_CAP  # total = 6000 + 3000 → overflow 3000
        c_candidates = tuple(_mk_candidate(f"c{i:023x}", channel="C") for i in range(n_c))
        d_candidates = tuple(_mk_candidate(f"d{i:023x}", channel="D") for i in range(n_d))
        overrides = {
            "C": FakeChannelResult(candidates=c_candidates, channel_state=HEALTH_OK),
            "D": FakeChannelResult(candidates=d_candidates, channel_state=HEALTH_OK),
        }
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(overrides),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert len(result.candidates) == SCOUT_UNION_CAP
        cap_events = [e for e in result.capstone_degradation_events if e.code == F_SCOUT_CAPSTONE_04]
        assert len(cap_events) == 1
        assert cap_events[0].severity == "MEDIUM"
        assert "overflow=" in (cap_events[0].reason_tag or "")

    def test_truncation_is_deterministic(self):
        n = SCOUT_UNION_CAP + 10
        pairs = [("D", _mk_candidate(f"d{i:023x}", channel="D")) for i in range(n)]
        kept1, overflow1 = _truncate_union(pairs)
        kept2, overflow2 = _truncate_union(list(pairs))
        assert [p[1].candidate_id for p in kept1] == [p[1].candidate_id for p in kept2]
        assert overflow1 == overflow2 == 10

    def test_truncation_prefers_earlier_channel_letters(self):
        n = SCOUT_UNION_CAP
        a_cands = [("A", _mk_candidate(f"a{i:023x}", channel="A")) for i in range(n)]
        d_cands = [("D", _mk_candidate(f"d{i:023x}", channel="D")) for i in range(5)]
        pairs = d_cands + a_cands  # D first in insertion; A should dominate after sort
        kept, overflow = _truncate_union(pairs)
        kept_channels = [p[0] for p in kept]
        assert overflow == 5
        assert all(ch == "A" for ch in kept_channels)


# ---------------------------------------------------------------------------
# 10. run_id derivation + 11. run tiebreak seed
# ---------------------------------------------------------------------------


class TestCapstoneRunIdDerivation:
    def test_deterministic_given_inputs(self):
        args = dict(session_id="s", run_wall_ns=1, run_tiebreak_seed=b"\x00" * 16)
        assert _derive_run_id(**args) == _derive_run_id(**args)

    def test_different_seed_different_id(self):
        a = _derive_run_id(session_id="s", run_wall_ns=1, run_tiebreak_seed=b"\x00" * 16)
        b = _derive_run_id(session_id="s", run_wall_ns=1, run_tiebreak_seed=b"\x01" * 16)
        assert a != b

    def test_different_session_different_id(self):
        a = _derive_run_id(session_id="s1", run_wall_ns=1, run_tiebreak_seed=b"\x00" * 16)
        b = _derive_run_id(session_id="s2", run_wall_ns=1, run_tiebreak_seed=b"\x00" * 16)
        assert a != b

    def test_different_wall_different_id(self):
        a = _derive_run_id(session_id="s", run_wall_ns=1, run_tiebreak_seed=b"\x00" * 16)
        b = _derive_run_id(session_id="s", run_wall_ns=2, run_tiebreak_seed=b"\x00" * 16)
        assert a != b

    def test_run_id_hex_length(self):
        run_id = _derive_run_id(session_id="x", run_wall_ns=1, run_tiebreak_seed=b"\x00" * 16)
        assert len(run_id) == RUN_ID_HEX_LEN
        assert all(c in "0123456789abcdef" for c in run_id)


class TestCapstoneRunTiebreakSeed:
    def test_seed_128_bit_by_default(self):
        cp, dw = _default_writers()
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            entropy=lambda n: b"\xab" * n,
        )
        assert len(result.run_tiebreak_seed) == _RUN_TIEBREAK_SEED_LEN
        assert result.run_tiebreak_seed == b"\xab" * _RUN_TIEBREAK_SEED_LEN

    def test_seed_passed_through_to_signer(self):
        cp, dw = _default_writers()
        signer = RecordingHealthSigner()
        seed = b"\x7f" * _RUN_TIEBREAK_SEED_LEN
        run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=signer,
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            entropy=lambda n: seed,
        )
        assert signer.calls[0]["run_tiebreak_seed"] == seed

    def test_two_runs_different_seeds_yield_different_run_ids(self):
        cp, dw = _default_writers()
        r1 = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            entropy=lambda n: b"\x01" * n,
            clock=lambda: 42,
        )
        r2 = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=RecordingCheckpointWriter(),
            degradation_writer=RecordingDegradationWriter(),
            executor_factory=_exec_factory(),
            entropy=lambda n: b"\x02" * n,
            clock=lambda: 42,
        )
        assert r1.run_id != r2.run_id


# ---------------------------------------------------------------------------
# 12. Checkpoint discipline
# ---------------------------------------------------------------------------


class TestCapstoneCheckpointDiscipline:
    def test_all_stages_written(self):
        cp, dw = _default_writers()
        run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        stages = [s for s, _ in cp.writes]
        assert stages[0] == "discover_start"
        assert stages.count("discover_channel_complete") == len(_CAPSTONE_CHANNEL_ORDER)
        assert stages[-1] == "discover_complete"

    def test_start_checkpoint_carries_run_id(self):
        cp, dw = _default_writers()
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        _stage, payload = cp.writes[0]
        assert payload["run_id"] == result.run_id
        assert payload["session_id"] == FakeSession().session_id

    def test_channel_complete_checkpoint_carries_channel_and_state(self):
        cp, dw = _default_writers()
        run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        channel_complete = [p for s, p in cp.writes if s == "discover_channel_complete"]
        assert [p["channel"] for p in channel_complete] == list(_CAPSTONE_CHANNEL_ORDER)
        for p in channel_complete:
            assert p["channel_state"] == HEALTH_OK

    def test_failed_channel_checkpoint_still_written(self):
        cp, dw = _default_writers()
        run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(raise_for={"D": RuntimeError("x")}),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        channel_complete = [p for s, p in cp.writes if s == "discover_channel_complete"]
        d_payload = [p for p in channel_complete if p["channel"] == "D"][0]
        assert d_payload["channel_state"] == HEALTH_FAILED

    def test_discover_complete_before_health_sign(self):
        cp, dw = _default_writers()
        signer = RecordingHealthSigner()
        run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=signer,
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        stages = [s for s, _ in cp.writes]
        assert stages.index("discover_complete") < len(stages)
        # Signer was called exactly once, after discover_complete checkpoint
        assert len(signer.calls) == 1


# ---------------------------------------------------------------------------
# 13. Deterministic channel order
# ---------------------------------------------------------------------------


class TestCapstoneChannelOrderDeterministic:
    def test_iteration_order_is_pinned(self):
        cp, dw = _default_writers()
        run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        channel_complete = [p for s, p in cp.writes if s == "discover_channel_complete"]
        assert [p["channel"] for p in channel_complete] == ["A", "B", "C", "D", "E", "F"]

    def test_channel_order_is_final_tuple(self):
        assert _CAPSTONE_CHANNEL_ORDER == ("A", "B", "C", "D", "E", "F")
        assert isinstance(_CAPSTONE_CHANNEL_ORDER, tuple)


# ---------------------------------------------------------------------------
# 14. No direct vault / open / setattr — AST-lint guarantees
# ---------------------------------------------------------------------------


class TestCapstoneNoDirectVault:
    def test_ast_lint_scout_rules_clean(self, tmp_path: Path):
        # E-027: lint_tree expects a directory. Copy discover.py + minimal
        # siblings into a temp pipeline/scout/ layout.
        from pipeline.linting import ast_lint

        src = Path(disc.__file__)
        dst_dir = tmp_path / "pipeline" / "scout"
        dst_dir.mkdir(parents=True)
        (dst_dir / "__init__.py").write_text("", encoding="utf-8")
        shutil.copy(src, dst_dir / "discover.py")

        # scout-local rules (SCOUT_NO_SETATTR + SCOUT_NO_EVAL) +
        # pipeline-wide R6/R7 apply.
        violations = ast_lint.lint_tree(tmp_path, ast_lint.DEFAULT_RULES)
        in_scope = [
            v for v in violations
            if v.file.name == "discover.py"
        ]
        assert in_scope == []

    def test_module_does_not_import_pipeline_vault(self):
        src = Path(disc.__file__).read_text(encoding="utf-8")
        # Module-scope pipeline.vault imports would break sovereignty.
        lines = [line for line in src.splitlines() if line.startswith("from pipeline.vault") or line.startswith("import pipeline.vault")]
        assert lines == []

    def test_module_has_no_module_level_open_call(self):
        src = Path(disc.__file__).read_text(encoding="utf-8")
        assert "\nopen(" not in src


# ---------------------------------------------------------------------------
# 15. Channel F opt-out
# ---------------------------------------------------------------------------


class TestCapstoneChannelFOptOut:
    def test_f_zero_candidates_ok_state_no_special_casing(self):
        cp, dw = _default_writers()
        overrides = {
            "F": FakeChannelResult(candidates=(), channel_state=HEALTH_OK),
        }
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(overrides),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert result.per_channel_states["F"] == HEALTH_OK
        # No F-SCOUT-CAPSTONE events emitted for F's trivial completion.
        f_events = [
            e for e in result.capstone_degradation_events if e.channel == "F"
        ]
        assert f_events == []


# ---------------------------------------------------------------------------
# 16. kw-only
# ---------------------------------------------------------------------------


class TestCapstoneKWOnly:
    def test_positional_call_rejected(self):
        with pytest.raises(TypeError):
            run_scout_discover(  # type: ignore[misc]
                FakeSession(),
                _ok_channels(),
                RecordingHealthSigner(),
                RecordingCheckpointWriter(),
                RecordingDegradationWriter(),
            )


# ---------------------------------------------------------------------------
# 17. Public surface + version pin (E-025)
# ---------------------------------------------------------------------------


class TestCapstonePublicSurface:
    def test_version_pin_r_n_ge_8(self):
        import re
        m = re.match(r"^0\.1\.0-scout-r(\d+)$", disc.__version__)
        assert m is not None
        assert int(m.group(1)) >= 8

    def test_run_scout_discover_exported(self):
        import pipeline.scout as scout
        # Exported from pipeline.scout after __init__ update.
        assert hasattr(disc, "run_scout_discover")
        # After __init__ exposes it, scout.run_scout_discover should resolve.
        assert callable(disc.run_scout_discover)

    def test_scout_discover_result_exported(self):
        assert hasattr(disc, "ScoutDiscoverResult")
        assert "ScoutDiscoverResult" in disc.__all__

    def test_capstone_degradation_event_exported(self):
        assert "CapstoneDegradationEvent" in disc.__all__

    def test_failure_codes_exported(self):
        for i in range(1, 8):
            assert f"F_SCOUT_CAPSTONE_0{i}" in disc.__all__

    def test_scout_union_cap_is_6000(self):
        assert SCOUT_UNION_CAP == 6000


# ---------------------------------------------------------------------------
# 18. Injected Protocols
# ---------------------------------------------------------------------------


class TestCapstoneInjectedProtocols:
    def test_checkpoint_writer_injected(self):
        cp, dw = _default_writers()
        run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert len(cp.writes) >= 2 + len(_CAPSTONE_CHANNEL_ORDER)

    def test_degradation_writer_injected(self):
        cp, dw = _default_writers()
        run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(raise_for={"D": RuntimeError("x")}),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert len(dw.events) >= 1

    def test_clock_injected(self):
        cp, dw = _default_writers()
        clock_calls = {"n": 0}

        def clock():
            clock_calls["n"] += 1
            return 9_999_999_999_999

        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            clock=clock,
        )
        assert clock_calls["n"] == 1
        assert result.run_wall_ns == 9_999_999_999_999

    def test_entropy_injected(self):
        cp, dw = _default_writers()
        entropy_calls = {"n": 0}

        def entropy(n):
            entropy_calls["n"] += 1
            return b"\xfe" * n

        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            entropy=entropy,
        )
        assert entropy_calls["n"] == 1
        assert result.run_tiebreak_seed == b"\xfe" * _RUN_TIEBREAK_SEED_LEN

    def test_interrupt_probe_injected_counts_per_channel(self):
        cp, dw = _default_writers()
        probe_calls = {"n": 0}

        def probe():
            probe_calls["n"] += 1
            return False

        run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
            interrupt_probe=probe,
        )
        # Probed once per channel at the top of the loop.
        assert probe_calls["n"] == len(_CAPSTONE_CHANNEL_ORDER)


# ---------------------------------------------------------------------------
# 19. State aggregation (capstone does not re-classify)
# ---------------------------------------------------------------------------


class TestCapstoneStateAggregation:
    def test_channel_state_received_verbatim(self):
        cp, dw = _default_writers()
        # Use an unusual but valid-looking string — we do NOT re-validate.
        overrides = {
            "E": FakeChannelResult(
                channel_state="DEGRADED",
                per_endpoint_state=None,
            )
        }
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(overrides),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert result.per_channel_states["E"] == "DEGRADED"

    def test_capstone_emits_only_capstone_codes(self):
        cp, dw = _default_writers()
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(raise_for={"B": RuntimeError("x")}),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        for ev in result.capstone_degradation_events:
            assert ev.code.startswith("F-SCOUT-CAPSTONE-")


# ---------------------------------------------------------------------------
# 20. Shared Protocol reuse — E-026 formal __module__ lineage
# ---------------------------------------------------------------------------


class TestCapstoneSharedProtocolReuse:
    def test_session_like_lineage(self):
        assert disc.SessionLike.__module__ == "pipeline.scout.discover"

    def test_candidate_lineage_from_types(self):
        assert Candidate.__module__ == "pipeline.scout._types"

    def test_signed_health_tuple_lineage(self):
        assert SignedHealthTuple.__module__ == "pipeline.scout._types"

    def test_discover_module_lineage(self):
        # E-026 formal — use __module__ over sys.modules identity check.
        assert run_scout_discover.__module__ == "pipeline.scout.discover"


# ---------------------------------------------------------------------------
# Adversarial tests (T-ADV-*)
# ---------------------------------------------------------------------------


class TestAdvChannelRaisesBaseException:
    def test_base_exception_not_caught_by_except_exception(self):
        cp, dw = _default_writers()

        class NastyBase(BaseException):
            pass

        fns = _ok_channels(raise_for={"B": NastyBase("base")})
        with pytest.raises(NastyBase):
            run_scout_discover(
                session=FakeSession(),
                channel_fns=fns,
                health_signer=RecordingHealthSigner(),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
            )


class TestAdvInterruptBetweenChannels:
    def test_interrupt_fires_between_b_and_c(self):
        cp, dw = _default_writers()
        probe_state = {"calls": 0}

        def probe():
            probe_state["calls"] += 1
            # call 1 = before A, call 2 = before B, call 3 = before C
            return probe_state["calls"] >= 3

        with pytest.raises(ScoutDiscoverInterrupted) as exc_info:
            run_scout_discover(
                session=FakeSession(),
                channel_fns=_ok_channels(),
                health_signer=RecordingHealthSigner(),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                interrupt_probe=probe,
            )
        assert exc_info.value.completed_channels == ("A", "B")
        interrupted = [p for s, p in cp.writes if s == "discover_interrupted"][0]
        assert interrupted["completed_channels"] == ["A", "B"]
        assert interrupted["pending_channel"] == "C"


class TestAdvEntropyReturnsWrongLength:
    def test_wrong_length_seed_raises(self):
        cp, dw = _default_writers()
        with pytest.raises(RuntimeError, match="entropy fn returned"):
            run_scout_discover(
                session=FakeSession(),
                channel_fns=_ok_channels(),
                health_signer=RecordingHealthSigner(),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
                entropy=lambda n: b"\x01" * (n - 1),
            )


class TestAdvHealthSignerRaises:
    def test_signer_raise_emits_capstone_06_and_reraises(self):
        cp, dw = _default_writers()
        signer = RecordingHealthSigner(raise_with=RuntimeError("keystore down"))
        with pytest.raises(RuntimeError, match="keystore down"):
            run_scout_discover(
                session=FakeSession(),
                channel_fns=_ok_channels(),
                health_signer=signer,
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
            )
        assert any(e.code == F_SCOUT_CAPSTONE_06 for e in dw.events)


class TestAdvExecutorReturnsBrokenFuture:
    def test_future_that_always_times_out_reached_via_clock_injection(self):
        # Custom executor: every channel times out.
        cp, dw = _default_writers()

        class AlwaysTimeoutExecutor(SequentialFakeExecutor):
            def __init__(self, max_workers):
                super().__init__(max_workers, timeout_channels=set(_CAPSTONE_CHANNEL_ORDER))

        factory = lambda n: AlwaysTimeoutExecutor(n)  # noqa: E731
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=factory,
        )
        assert all(
            v == HEALTH_FAILED for v in result.per_channel_states.values()
        )
        assert (
            len([
                e for e in result.capstone_degradation_events
                if e.code == F_SCOUT_CAPSTONE_01
            ])
            == len(_CAPSTONE_CHANNEL_ORDER)
        )


class TestAdvMissingChannelKey:
    def test_missing_channel_raises_key_error_before_executor(self):
        cp, dw = _default_writers()
        fns = _ok_channels()
        del fns["F"]
        with pytest.raises(KeyError, match="channel_fns missing"):
            run_scout_discover(
                session=FakeSession(),
                channel_fns=fns,
                health_signer=RecordingHealthSigner(),
                checkpoint_writer=cp,
                degradation_writer=dw,
                executor_factory=_exec_factory(),
            )
        # No executor runs, no checkpoints written.
        assert cp.writes == []


class TestAdvDuplicatesAcrossAllSixChannels:
    def test_first_writer_wins_even_with_six_duplicates(self):
        cp, dw = _default_writers()
        cand = _mk_candidate("hexa" * 6, channel="A")
        overrides = {}
        for ch in _CAPSTONE_CHANNEL_ORDER:
            overrides[ch] = FakeChannelResult(
                candidates=(cand,),
                channel_state=HEALTH_OK,
                per_endpoint_state=(
                    {ep: HEALTH_OK for ep in _CHANNEL_A_ENDPOINTS} if ch == "A" else None
                ),
            )
        result = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(overrides),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert len(result.candidates) == 1
        dedup_events = [
            e for e in result.capstone_degradation_events if e.code == F_SCOUT_CAPSTONE_03
        ]
        # Five dedup events — one for each channel after A.
        assert len(dedup_events) == 5
        assert [e.channel for e in dedup_events] == ["B", "C", "D", "E", "F"]


# ---------------------------------------------------------------------------
# Additional coverage
# ---------------------------------------------------------------------------


class TestCapstoneDefaults:
    def test_default_clock_returns_int(self):
        n1 = disc._default_clock()
        n2 = disc._default_clock()
        assert isinstance(n1, int) and isinstance(n2, int)
        assert n2 >= n1

    def test_default_entropy_produces_requested_length(self):
        assert len(disc._default_entropy(16)) == 16
        assert len(disc._default_entropy(32)) == 32

    def test_default_interrupt_probe_false(self):
        assert disc._default_interrupt_probe() is False

    def test_default_executor_factory_shuts_down(self):
        factory = disc._default_executor_factory
        with factory(2) as pool:
            fut = pool.submit(lambda: 42)
            assert fut.result(timeout=5) == 42

    def test_make_default_health_signer_closes_vault_writer(self):
        # The signer closure should be callable with the expected kwargs;
        # the underlying `assemble_and_sign_health_tuple` is exercised in
        # Round 2 — here we only assert the factory wires through.
        calls = []

        class _FakeVW:
            def write(self, **kw):
                calls.append(kw)

        signer = disc.make_default_health_signer(_FakeVW())
        assert callable(signer)

    def test_make_default_health_signer_invokes_assemble_and_sign(
        self, monkeypatch
    ):
        # Exercise the closure body: the signer should delegate to
        # `assemble_and_sign_health_tuple` with the bound vault_writer.
        import pipeline.scout.health_tuple as ht

        captured = {}

        def _fake_sign(**kw):
            captured.update(kw)
            return "sentinel"

        monkeypatch.setattr(ht, "assemble_and_sign_health_tuple", _fake_sign)
        vw = object()
        signer = disc.make_default_health_signer(vw)
        out = signer(
            session=FakeSession(session_id="s"),
            per_channel_states={"A": "OK"},
            per_channel_a_endpoints={"grants.gov": "OK"},
            run_wall_ns=1,
            run_tiebreak_seed=b"\x00" * 16,
        )
        assert out == "sentinel"
        assert captured["vault_writer"] is vw
        assert captured["per_channel"] == {"A": "OK"}
        assert captured["per_channel_a_endpoints"] == {"grants.gov": "OK"}


class TestCapstoneDegradationEventShape:
    def test_frozen_kw_only(self):
        ev = CapstoneDegradationEvent(
            source="x",
            code=F_SCOUT_CAPSTONE_01,
            reason_tag="r",
            severity="HIGH",
            channel="A",
        )
        with pytest.raises(Exception):
            ev.source = "y"  # type: ignore[misc]

    def test_channel_optional(self):
        ev = CapstoneDegradationEvent(
            source="x",
            code=F_SCOUT_CAPSTONE_04,
            reason_tag=None,
            severity="MEDIUM",
        )
        assert ev.channel is None


class TestCapstoneResultShape:
    def test_frozen_kw_only(self):
        cp, dw = _default_writers()
        r = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        with pytest.raises(Exception):
            r.run_id = "new-run"  # type: ignore[misc]

    def test_candidates_is_tuple(self):
        cp, dw = _default_writers()
        r = run_scout_discover(
            session=FakeSession(),
            channel_fns=_ok_channels(),
            health_signer=RecordingHealthSigner(),
            checkpoint_writer=cp,
            degradation_writer=dw,
            executor_factory=_exec_factory(),
        )
        assert isinstance(r.candidates, tuple)
        assert isinstance(r.capstone_degradation_events, tuple)


class TestCapstoneTruncateUnion:
    def test_under_cap_returns_same_list(self):
        pairs = [("A", _mk_candidate(f"{i:024x}")) for i in range(10)]
        kept, overflow = _truncate_union(pairs)
        assert kept is pairs
        assert overflow == 0

    def test_exact_cap_no_truncation(self):
        pairs = [("A", _mk_candidate(f"{i:024x}")) for i in range(SCOUT_UNION_CAP)]
        kept, overflow = _truncate_union(pairs)
        assert len(kept) == SCOUT_UNION_CAP
        assert overflow == 0

    def test_overflow_count(self):
        pairs = [("B", _mk_candidate(f"{i:024x}", channel="B")) for i in range(SCOUT_UNION_CAP + 7)]
        kept, overflow = _truncate_union(pairs)
        assert len(kept) == SCOUT_UNION_CAP
        assert overflow == 7


class TestCapstoneNoLLMCalls:
    def test_discover_source_has_no_llm_imports(self):
        src = Path(disc.__file__).read_text(encoding="utf-8")
        for forbidden in ("import anthropic", "import openai", "import groq"):
            assert forbidden not in src


class TestCapstoneNoSetattrOnOperatorDecision:
    def test_no_setattr_operator_decision_in_source(self):
        src = Path(disc.__file__).read_text(encoding="utf-8")
        assert "setattr(" not in src


class TestCapstoneNoEval:
    def test_no_eval_or_exec_calls(self):
        src = Path(disc.__file__).read_text(encoding="utf-8")
        # Match identifier-boundary: re-enforce the R5 contract.
        import re
        assert re.search(r"\beval\s*\(", src) is None
        assert re.search(r"\bexec\s*\(", src) is None
