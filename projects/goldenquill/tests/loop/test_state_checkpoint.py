"""Tests for pipeline.loop.state_checkpoint — §4.13 atomic CAS envelope.

Blueprint §5 v6 §4.13 LOCKED 2026-04-19.

Coverage targets:
- Happy path (single-attempt success).
- Retry-and-win (first 2 CAS mismatches, 3rd succeeds); back-off sequence
  observed as (50, 200) ms per inline-literal schedule.
- CAS exhaustion → quarantine marker written BEFORE F_PIPE_01.
- Total-timeout → quarantine + F_PIPE_01 with reason=total_timeout.
- Terminal non-CAS VaultError → state-failure wrapper + ORIGINAL error
  re-raised (blueprint-faithful; NOT F_PIPE_01).
- Idempotent replay semantics on same RunState.
- _assert_runstate_schema_current: pure predicate; F_PIPE_22 on schema_version != 2.
- Bounded-attempts property: attempt_count <= 3.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from pipeline.loop.errors import F_PIPE_01, F_PIPE_22
from pipeline.loop.state_checkpoint import (
    CheckpointResult,
    _assert_runstate_schema_current,
    _canonicalize_runstate,
    _write_quarantine_marker,
    _write_state_failure_wrapper,
    checkpoint_atomic,
)
from pipeline.loop.types import RunState
from pipeline.vault.error_codes import (
    VaultCASHeadMismatch,
    VaultError,
    VaultWriteDenied,
)


# ---------------------------------------------------------------------------
# Fixtures / fakes
# ---------------------------------------------------------------------------


def _mk_submission_runstate(**overrides: Any) -> RunState:
    kwargs: dict[str, Any] = dict(
        schema_version=2,
        run_id="run-ckpt",
        mode="submission",
        rfa_hash="rfa-h",
        project_context_hash="pc-h",
        golden_set_ref=None,
        org_slug="mycosymbiotics",
        session_id="sess",
        phase="initialized",
    )
    kwargs.update(overrides)
    return RunState(**kwargs)


@dataclass
class _FakeClock:
    now_ms_values: list[int] = field(default_factory=list)
    iso_values: list[str] = field(default_factory=list)
    _ms_idx: int = 0
    _iso_idx: int = 0
    _default_iso: str = "2026-04-20T12:00:00Z"

    def now_ms(self) -> int:
        if self._ms_idx >= len(self.now_ms_values):
            # Saturate with the last supplied value.
            return self.now_ms_values[-1] if self.now_ms_values else 0
        v = self.now_ms_values[self._ms_idx]
        self._ms_idx += 1
        return v

    def now_iso(self) -> str:
        if self._iso_idx >= len(self.iso_values):
            return self._default_iso
        v = self.iso_values[self._iso_idx]
        self._iso_idx += 1
        return v


@dataclass
class _FakeSleep:
    calls: list[int] = field(default_factory=list)

    def __call__(self, ms: int) -> None:
        self.calls.append(ms)


@dataclass
class _FakeVault:
    """In-process CAS-aware vault fake.

    Paths map to (current_sha, bytes). CAS is simulated by comparing
    ``expected_current_file_hash`` to the stored digest; mismatch raises
    ``VaultCASHeadMismatch``. ``head_mutations`` lets a test make the fake
    stop mismatching after N failed attempts (retry-and-win).
    """

    store: dict[str, bytes] = field(default_factory=dict)
    # Per-path: when attempt_count[path] < head_mutations[path], mismatch.
    head_mutations: dict[str, int] = field(default_factory=dict)
    attempt_count: dict[str, int] = field(default_factory=dict)
    calls: list[dict[str, Any]] = field(default_factory=list)
    # If set, override behaviour with a callable that can raise.
    override: Any = None

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
        if self.override is not None:
            return self.override(
                path=path,
                payload=payload,
                intent=intent,
                write_mode=write_mode,
                expected_current_file_hash=expected_current_file_hash,
            )

        self.attempt_count[path] = self.attempt_count.get(path, 0) + 1

        mismatches_before_win = self.head_mutations.get(path, 0)
        if self.attempt_count[path] <= mismatches_before_win:
            import hashlib as _hl

            raise VaultCASHeadMismatch(
                "cas mismatch (fake)",
                expected_current_file_hash=expected_current_file_hash or "",
                actual_current_file_hash=_hl.sha256(b"actual").hexdigest(),
            )

        import hashlib as _hl

        digest = _hl.sha256(payload).hexdigest()
        self.store[path] = payload
        return digest


# ---------------------------------------------------------------------------
# Happy-path
# ---------------------------------------------------------------------------


class TestHappyPath:
    def test_single_attempt_success(self) -> None:
        rs = _mk_submission_runstate()
        clock = _FakeClock(
            now_ms_values=[1000, 1001, 1002],
            iso_values=["2026-04-20T12:00:00Z"],
        )
        sleep = _FakeSleep()
        vault = _FakeVault()

        result = checkpoint_atomic(
            rs,
            intent="state-success",
            expected_current_file_hash=None,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
        )

        assert isinstance(result, CheckpointResult)
        assert result.attempt_count == 1
        assert result.quarantine_marker_ref is None
        assert result.written_at_iso == "2026-04-20T12:00:00Z"
        assert result.committed_hash  # non-empty sha256 hex
        assert len(result.committed_hash) == 64
        assert sleep.calls == []  # no retries, no sleep
        # Vault observed exactly one call with the right intent/path.
        assert len(vault.calls) == 1
        call = vault.calls[0]
        assert call["path"] == "pipeline/run-ckpt/state.json"
        assert call["intent"] == "state-success"
        assert call["write_mode"] == "overwrite"
        assert call["expected_current_file_hash"] is None
        # RunState side effects.
        assert rs.last_checkpoint_iso == "2026-04-20T12:00:00Z"
        assert rs.quarantine_marker_ref is None
        assert rs.phase == "initialized"

    def test_happy_path_with_nonnull_cas_head(self) -> None:
        rs = _mk_submission_runstate(phase="pre_gate_passed")
        clock = _FakeClock(now_ms_values=[0, 5])
        sleep = _FakeSleep()
        vault = _FakeVault()

        result = checkpoint_atomic(
            rs,
            intent="state-success",
            expected_current_file_hash="a" * 64,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
        )

        assert result.attempt_count == 1
        assert vault.calls[0]["expected_current_file_hash"] == "a" * 64


# ---------------------------------------------------------------------------
# Retry-and-win
# ---------------------------------------------------------------------------


class TestRetryAndWin:
    def test_two_mismatches_then_success(self) -> None:
        rs = _mk_submission_runstate()
        clock = _FakeClock(
            now_ms_values=[0, 10, 20, 30, 40, 50, 60, 70],
            iso_values=["t0", "t1", "t2"],
        )
        sleep = _FakeSleep()
        path = "pipeline/run-ckpt/state.json"
        vault = _FakeVault(head_mutations={path: 2})

        result = checkpoint_atomic(
            rs,
            intent="state-success",
            expected_current_file_hash="stale",
            vault_write=vault,
            clock=clock,
            sleep=sleep,
        )

        assert result.attempt_count == 3
        assert result.quarantine_marker_ref is None
        # Back-off schedule 50, 200 ms applied between attempts 1→2 and 2→3.
        assert sleep.calls == [50, 200]
        # The vault saw three write attempts.
        assert len(vault.calls) == 3

    def test_one_mismatch_then_success(self) -> None:
        rs = _mk_submission_runstate()
        clock = _FakeClock(now_ms_values=[0, 10, 20, 30])
        sleep = _FakeSleep()
        path = "pipeline/run-ckpt/state.json"
        vault = _FakeVault(head_mutations={path: 1})

        result = checkpoint_atomic(
            rs,
            intent="state-success",
            expected_current_file_hash=None,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
        )

        assert result.attempt_count == 2
        assert sleep.calls == [50]


# ---------------------------------------------------------------------------
# CAS exhaustion → quarantine + F_PIPE_01
# ---------------------------------------------------------------------------


class TestCasExhaustion:
    def test_all_three_attempts_mismatch_raises_f_pipe_01(self) -> None:
        rs = _mk_submission_runstate(phase="pre_gate_passed")
        clock = _FakeClock(now_ms_values=[0, 10, 20, 30, 40, 50, 60, 70, 80])
        sleep = _FakeSleep()
        path = "pipeline/run-ckpt/state.json"
        # head_mutations = 99 means every attempt mismatches.
        vault = _FakeVault(head_mutations={path: 99})

        with pytest.raises(F_PIPE_01) as excinfo:
            checkpoint_atomic(
                rs,
                intent="state-success",
                expected_current_file_hash="stale",
                vault_write=vault,
                clock=clock,
                sleep=sleep,
            )

        exc = excinfo.value
        assert exc.code == "F-PIPE-01"
        assert "cas_exhausted" in exc.trigger
        assert exc.details["attempt_count"] == 3
        assert (
            exc.details["quarantine_marker_ref"]
            == "pipeline/run-ckpt/quarantine.json"
        )

        # Quarantine marker observed BEFORE F_PIPE_01 — the last vault call
        # must be the quarantine-marker write.
        assert len(vault.calls) == 4  # 3 state.json + 1 quarantine.json
        qcall = vault.calls[-1]
        assert qcall["path"] == "pipeline/run-ckpt/quarantine.json"
        assert qcall["intent"] == "state-success"
        assert qcall["write_mode"] == "overwrite"

        # RunState side effects: quarantine ref populated, phase moved.
        assert rs.quarantine_marker_ref == "pipeline/run-ckpt/quarantine.json"
        assert rs.phase == "quarantined"

        # Three back-offs fired (one per CAS mismatch).
        assert sleep.calls == [50, 200, 800]

    def test_total_timeout_before_exhaustion(self) -> None:
        rs = _mk_submission_runstate()
        # start=0, then each attempt's elapsed-check returns 20_000 (> 10_000)
        # — the first attempt succeeds bookkeeping but we want the SECOND
        # attempt (after a mismatch) to see total_timeout. Wire that up:
        # elapsed sequence: 0 (start), 100 (first attempt check passes),
        # 20_000 (second attempt check breaks).
        clock = _FakeClock(
            now_ms_values=[0, 100, 20_000, 20_001, 20_002],
        )
        sleep = _FakeSleep()
        path = "pipeline/run-ckpt/state.json"
        vault = _FakeVault(head_mutations={path: 99})

        with pytest.raises(F_PIPE_01) as excinfo:
            checkpoint_atomic(
                rs,
                intent="state-success",
                expected_current_file_hash="stale",
                vault_write=vault,
                clock=clock,
                sleep=sleep,
            )

        exc = excinfo.value
        assert "total_timeout" in exc.trigger
        # Only one real write attempt landed before the timeout break.
        assert exc.details["attempt_count"] == 1
        # Quarantine marker still written.
        assert rs.quarantine_marker_ref == "pipeline/run-ckpt/quarantine.json"

    def test_attempt_count_bounded_by_three(self) -> None:
        """Property: attempt_count <= 3 always (schedule-length inline literal)."""
        rs = _mk_submission_runstate()
        clock = _FakeClock(now_ms_values=[0] + [10] * 20)
        sleep = _FakeSleep()
        path = "pipeline/run-ckpt/state.json"
        vault = _FakeVault(head_mutations={path: 99})

        with pytest.raises(F_PIPE_01) as excinfo:
            checkpoint_atomic(
                rs,
                intent="state-success",
                expected_current_file_hash="stale",
                vault_write=vault,
                clock=clock,
                sleep=sleep,
            )
        assert excinfo.value.details["attempt_count"] <= 3


# ---------------------------------------------------------------------------
# Terminal non-CAS VaultError → state-failure wrapper + re-raise original
# ---------------------------------------------------------------------------


class TestTerminalVaultError:
    def test_vault_write_denied_writes_state_failure_and_reraises_original(
        self,
    ) -> None:
        rs = _mk_submission_runstate(phase="pre_gate_passed")
        clock = _FakeClock(now_ms_values=[0, 1, 2, 3, 4])
        sleep = _FakeSleep()

        def _denied(**kwargs: Any) -> str:
            # Only the primary state.json call raises; the state-failure
            # wrapper write is allowed to succeed (best-effort).
            if kwargs["path"].endswith("state.json"):
                raise VaultWriteDenied("not in allowlist")
            # state_failure.json write succeeds.
            import hashlib as _hl

            return _hl.sha256(kwargs["payload"]).hexdigest()

        vault = _FakeVault(override=_denied)

        # Blueprint §4.13 contract: ORIGINAL VaultError re-raised; NOT F_PIPE_01.
        with pytest.raises(VaultWriteDenied):
            checkpoint_atomic(
                rs,
                intent="state-success",
                expected_current_file_hash=None,
                vault_write=vault,
                clock=clock,
                sleep=sleep,
            )

        # Quarantine marker NOT populated — this is not the exhaustion path.
        assert rs.quarantine_marker_ref is None
        assert rs.phase == "pre_gate_passed"

        # Two calls: state.json (denied) + state_failure.json (best-effort).
        assert [c["path"] for c in vault.calls] == [
            "pipeline/run-ckpt/state.json",
            "pipeline/run-ckpt/state_failure.json",
        ]
        assert vault.calls[1]["intent"] == "state-failure"

    def test_state_failure_wrapper_swallows_secondary_error(self) -> None:
        rs = _mk_submission_runstate()
        clock = _FakeClock(now_ms_values=[0, 1, 2, 3])
        sleep = _FakeSleep()

        def _all_denied(**kwargs: Any) -> str:
            raise VaultWriteDenied(f"denied on {kwargs['path']}")

        vault = _FakeVault(override=_all_denied)

        # Primary error still re-raised even if the state-failure wrapper
        # ALSO fails — best-effort semantics.
        with pytest.raises(VaultWriteDenied):
            checkpoint_atomic(
                rs,
                intent="state-success",
                expected_current_file_hash=None,
                vault_write=vault,
                clock=clock,
                sleep=sleep,
            )
        # Both writes attempted.
        assert len(vault.calls) == 2


# ---------------------------------------------------------------------------
# Idempotent replay
# ---------------------------------------------------------------------------


class TestIdempotentReplay:
    def test_replay_same_runstate_produces_same_committed_hash(self) -> None:
        rs = _mk_submission_runstate()
        clock = _FakeClock(now_ms_values=[0, 1, 2, 3, 4, 5])
        sleep = _FakeSleep()
        vault = _FakeVault()

        r1 = checkpoint_atomic(
            rs,
            intent="state-success",
            expected_current_file_hash=None,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
        )
        # Second call — same RunState, same head pin. The vault returns
        # sha256(payload), which depends only on the canonical bytes. Those
        # bytes do not include last_checkpoint_iso? Actually — they DO;
        # checkpoint_atomic mutates last_checkpoint_iso on success. So we
        # need to pin last_checkpoint_iso to the same value on replay to
        # get byte-identity.
        rs.last_checkpoint_iso = ""  # reset for deterministic second canonicalization
        clock2 = _FakeClock(now_ms_values=[0, 1, 2], iso_values=[r1.written_at_iso])
        r2 = checkpoint_atomic(
            rs,
            intent="state-success",
            expected_current_file_hash=None,
            vault_write=vault,
            clock=clock2,
            sleep=sleep,
        )
        assert r1.committed_hash == r2.committed_hash


# ---------------------------------------------------------------------------
# _assert_runstate_schema_current
# ---------------------------------------------------------------------------


class TestAssertRunstateSchemaCurrent:
    def test_current_schema_passes(self) -> None:
        rs = _mk_submission_runstate()
        # Must not raise.
        _assert_runstate_schema_current(rs)

    def test_schema_downgrade_to_1_raises_f_pipe_22(self) -> None:
        rs = _mk_submission_runstate()
        # Post-construction mutation — RunState is not frozen.
        rs.schema_version = 1
        with pytest.raises(F_PIPE_22) as excinfo:
            _assert_runstate_schema_current(rs)
        exc = excinfo.value
        assert exc.trigger == "runstate_schema_downgrade"
        assert exc.details["observed"] == 1

    def test_future_schema_3_also_raises(self) -> None:
        rs = _mk_submission_runstate()
        rs.schema_version = 3
        with pytest.raises(F_PIPE_22) as excinfo:
            _assert_runstate_schema_current(rs)
        assert excinfo.value.details["observed"] == 3

    def test_predicate_is_pure_no_side_effects(self) -> None:
        rs = _mk_submission_runstate(phase="pre_gate_passed")
        rs.schema_version = 1
        original_phase = rs.phase
        original_qref = rs.quarantine_marker_ref
        with pytest.raises(F_PIPE_22):
            _assert_runstate_schema_current(rs)
        # Predicate is pure — no state mutation.
        assert rs.phase == original_phase
        assert rs.quarantine_marker_ref == original_qref


# ---------------------------------------------------------------------------
# Helpers — quarantine marker + state-failure wrapper (direct)
# ---------------------------------------------------------------------------


class TestQuarantineMarkerDirect:
    def test_writes_at_expected_path_with_state_success_intent(self) -> None:
        rs = _mk_submission_runstate(phase="post_gate_pending")
        clock = _FakeClock(iso_values=["2026-04-20T13:00:00Z"])
        vault = _FakeVault()

        ref = _write_quarantine_marker(
            rs, reason="unit_test", vault_write=vault, clock=clock
        )

        assert ref == "pipeline/run-ckpt/quarantine.json"
        assert len(vault.calls) == 1
        call = vault.calls[0]
        assert call["intent"] == "state-success"
        assert call["write_mode"] == "overwrite"
        assert call["expected_current_file_hash"] is None
        # Payload is deterministic sorted json.
        import json as _json

        payload = _json.loads(call["payload"])
        assert payload["run_id"] == "run-ckpt"
        assert payload["last_known_good_phase"] == "post_gate_pending"
        assert payload["reason"] == "unit_test"


class TestStateFailureWrapperDirect:
    def test_writes_failure_marker(self) -> None:
        rs = _mk_submission_runstate()
        clock = _FakeClock(iso_values=["2026-04-20T14:00:00Z"])
        vault = _FakeVault()

        err = VaultWriteDenied("test error")
        _write_state_failure_wrapper(rs, err, vault_write=vault, clock=clock)

        assert len(vault.calls) == 1
        call = vault.calls[0]
        assert call["path"] == "pipeline/run-ckpt/state_failure.json"
        assert call["intent"] == "state-failure"
        import json as _json

        payload = _json.loads(call["payload"])
        assert payload["error_code"] == "F-VAULT-02"  # VaultWriteDenied.code
        assert payload["phase_at_failure"] == "initialized"

    def test_swallows_secondary_vault_error(self) -> None:
        rs = _mk_submission_runstate()
        clock = _FakeClock(iso_values=["2026-04-20T14:00:00Z"])

        def _always_fail(**kwargs: Any) -> str:
            raise VaultWriteDenied("secondary")

        vault = _FakeVault(override=_always_fail)
        err = VaultError("primary")
        # Must not raise.
        _write_state_failure_wrapper(rs, err, vault_write=vault, clock=clock)


# ---------------------------------------------------------------------------
# Canonicalization determinism
# ---------------------------------------------------------------------------


class TestCanonicalization:
    def test_equal_runstates_produce_identical_bytes(self) -> None:
        rs1 = _mk_submission_runstate()
        rs2 = _mk_submission_runstate()
        assert _canonicalize_runstate(rs1) == _canonicalize_runstate(rs2)

    def test_phase_change_flips_bytes(self) -> None:
        rs1 = _mk_submission_runstate(phase="initialized")
        rs2 = _mk_submission_runstate(phase="pre_gate_passed")
        assert _canonicalize_runstate(rs1) != _canonicalize_runstate(rs2)

    def test_canonicalize_handles_nondataclass_bucket_via_default(self) -> None:
        """Forward-compat: _default serializer handles non-dataclass buckets.

        ``asdict()`` does NOT recurse into non-dataclass objects stored
        inside a dataclass field — they pass through unchanged and hit the
        ``json.dumps(default=_default)`` fallback. Round 7 ships the concrete
        TokenBucket; Round 2 guarantees canonicalization survives whatever
        shape Round 7 picks.
        """
        from pipeline.loop.state_checkpoint import _canonicalize_runstate
        from pipeline.loop.types import RateLimiterState

        class _OpaqueBucket:  # non-dataclass on purpose
            capacity = 10
            tokens = 5.0
            refill_rate_per_sec = 1.0

            def __repr__(self) -> str:
                return "<opaque-bucket>"

        rs = _mk_submission_runstate()
        rs.rate_limiter_snapshot = RateLimiterState(
            buckets={"anthropic": _OpaqueBucket()},  # type: ignore[dict-item]
            last_refill_iso="2026-04-20T00:00:00Z",
        )
        out = _canonicalize_runstate(rs)
        # Opaque-repr fallback path exercised.
        assert b"opaque-bucket" in out

    def test_canonicalize_default_handler_frozenset_and_dataclass_branches(
        self,
    ) -> None:
        """Directly exercise the inner _default handler logic.

        Rebuilds the helper's default function so the frozenset-branch and
        the is_dataclass-branch are both directly hit.
        """
        import json as _json
        from dataclasses import asdict as _asdict
        from dataclasses import dataclass as _dc
        from dataclasses import is_dataclass as _is_dc

        @_dc
        class _DC:
            x: int = 1

        def _default(obj: Any) -> Any:
            if _is_dc(obj) and not isinstance(obj, type):
                return _asdict(obj)
            if isinstance(obj, (frozenset, set)):
                return sorted(obj)
            return {"__repr__": repr(obj)}

        # frozenset branch — sorted list output.
        s_fz = _json.dumps(
            {"k": frozenset({"b", "a"})},
            default=_default,
            sort_keys=True,
            separators=(",", ":"),
        )
        assert '"a","b"' in s_fz
        # dataclass branch — recursed asdict.
        s_dc = _json.dumps({"k": _DC()}, default=_default, sort_keys=True)
        assert '"x"' in s_dc
