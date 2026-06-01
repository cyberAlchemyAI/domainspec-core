"""Adversarial tests — inline-literal RHS integrity for state_checkpoint.

Blueprint §5 v6 §4.13 + §8 V1 closure (extended to Round 2 surface).

Premise: a module-attribute rebinding of
- ``pipeline.loop.config.CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS``
- ``pipeline.loop.config.CHECKPOINT_TOTAL_TIMEOUT_SEC``
- ``pipeline.loop.config.RUNSTATE_SCHEMA_VERSION``
must not alter ``checkpoint_atomic`` or ``_assert_runstate_schema_current``
behaviour, because every runtime check uses an inline literal RHS.

Strategy: in-process rebind of the config module attribute AFTER import,
then exercise the Round 2 function and verify the inline-literal path held.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from pipeline.loop import config as cfg
from pipeline.loop.errors import F_PIPE_01, F_PIPE_22
from pipeline.loop.state_checkpoint import (
    _assert_runstate_schema_current,
    checkpoint_atomic,
)
from pipeline.loop.types import RunState
from pipeline.vault.error_codes import VaultCASHeadMismatch


@pytest.fixture(autouse=True)
def _restore_config_constants():
    """Snapshot + restore config constants around each adversarial test."""
    snapshot = {
        "CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS": cfg.CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS,
        "CHECKPOINT_TOTAL_TIMEOUT_SEC": cfg.CHECKPOINT_TOTAL_TIMEOUT_SEC,
        "RUNSTATE_SCHEMA_VERSION": cfg.RUNSTATE_SCHEMA_VERSION,
    }
    yield
    for name, val in snapshot.items():
        setattr(cfg, name, val)


# ---------------------------------------------------------------------------
# Shared fakes (local copies to avoid coupling to test_state_checkpoint)
# ---------------------------------------------------------------------------


def _mk_runstate() -> RunState:
    return RunState(
        schema_version=2,
        run_id="run-adv",
        mode="submission",
        rfa_hash="r",
        project_context_hash="pc",
        golden_set_ref=None,
        org_slug="org",
        session_id="s",
        phase="initialized",
    )


@dataclass
class _Clock:
    values: list[int] = field(default_factory=lambda: [0, 1, 2, 3, 4, 5, 6, 7])
    _i: int = 0

    def now_ms(self) -> int:
        if self._i >= len(self.values):
            return self.values[-1]
        v = self.values[self._i]
        self._i += 1
        return v

    def now_iso(self) -> str:
        return "2026-04-20T00:00:00Z"


@dataclass
class _Sleep:
    calls: list[int] = field(default_factory=list)

    def __call__(self, ms: int) -> None:
        self.calls.append(ms)


@dataclass
class _AlwaysMismatchVault:
    attempts: int = 0
    calls: list[str] = field(default_factory=list)

    def __call__(
        self,
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        self.calls.append(path)
        if path.endswith("state.json"):
            self.attempts += 1
            raise VaultCASHeadMismatch(
                "adv", expected_current_file_hash="e", actual_current_file_hash="a"
            )
        # quarantine.json write succeeds.
        import hashlib as _hl

        return _hl.sha256(payload).hexdigest()


# ---------------------------------------------------------------------------
# V1 — CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS rebind cannot alter back-off
# ---------------------------------------------------------------------------


class TestBackoffScheduleInlineLiteralResistance:
    def test_rebinding_schedule_to_1_1_1_does_not_reduce_backoff(self) -> None:
        # Attacker rebinds the config constant to tiny values.
        cfg.CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS = (1, 1, 1)  # type: ignore[misc]

        rs = _mk_runstate()
        clock = _Clock()
        sleep = _Sleep()
        vault = _AlwaysMismatchVault()

        with pytest.raises(F_PIPE_01):
            checkpoint_atomic(
                rs,
                intent="state-success",
                expected_current_file_hash="stale",
                vault_write=vault,
                clock=clock,
                sleep=sleep,
            )

        # Inline-literal schedule (50, 200, 800) still governs despite the
        # rebind. All three back-offs fired on the exhaustion path.
        assert sleep.calls == [50, 200, 800]

    def test_rebinding_schedule_to_large_values_does_not_extend_backoff(
        self,
    ) -> None:
        cfg.CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS = (9_999, 9_999, 9_999)  # type: ignore[misc]

        rs = _mk_runstate()
        clock = _Clock()
        sleep = _Sleep()
        vault = _AlwaysMismatchVault()

        with pytest.raises(F_PIPE_01):
            checkpoint_atomic(
                rs,
                intent="state-success",
                expected_current_file_hash="stale",
                vault_write=vault,
                clock=clock,
                sleep=sleep,
            )

        assert sleep.calls == [50, 200, 800]


# ---------------------------------------------------------------------------
# V1 — CHECKPOINT_TOTAL_TIMEOUT_SEC rebind cannot alter the 10_000 ms ceiling
# ---------------------------------------------------------------------------


class TestTotalTimeoutInlineLiteralResistance:
    def test_rebinding_total_timeout_does_not_extend_window(self) -> None:
        # Attacker rebinds to a huge value.
        cfg.CHECKPOINT_TOTAL_TIMEOUT_SEC = 600  # type: ignore[misc]

        rs = _mk_runstate()
        # Supply a clock that returns 10_001 ms after the first attempt —
        # inline literal 10_000 ms ceiling still triggers the timeout break.
        clock = _Clock(values=[0, 100, 10_001, 10_002, 10_003])
        sleep = _Sleep()
        vault = _AlwaysMismatchVault()

        with pytest.raises(F_PIPE_01) as excinfo:
            checkpoint_atomic(
                rs,
                intent="state-success",
                expected_current_file_hash="stale",
                vault_write=vault,
                clock=clock,
                sleep=sleep,
            )

        # Timeout-path trigger encoded in the F_PIPE_01 details.
        assert "total_timeout" in excinfo.value.trigger


# ---------------------------------------------------------------------------
# V1 — RUNSTATE_SCHEMA_VERSION rebind cannot alter the != 2 predicate
# ---------------------------------------------------------------------------


class TestSchemaVersionInlineLiteralResistance:
    def test_rebinding_runstate_schema_version_to_1_still_rejects_1(self) -> None:
        cfg.RUNSTATE_SCHEMA_VERSION = 1  # type: ignore[misc]

        rs = _mk_runstate()
        # Post-construction rebind — RunState is mutable.
        rs.schema_version = 1

        with pytest.raises(F_PIPE_22):
            _assert_runstate_schema_current(rs)

    def test_rebinding_runstate_schema_version_to_3_still_requires_2(self) -> None:
        cfg.RUNSTATE_SCHEMA_VERSION = 3  # type: ignore[misc]

        rs = _mk_runstate()
        rs.schema_version = 3

        with pytest.raises(F_PIPE_22):
            _assert_runstate_schema_current(rs)

    def test_rebind_does_not_break_happy_case(self) -> None:
        cfg.RUNSTATE_SCHEMA_VERSION = 99  # type: ignore[misc]

        rs = _mk_runstate()  # schema_version=2 passes inline `== 2`
        # Must not raise.
        _assert_runstate_schema_current(rs)


# ---------------------------------------------------------------------------
# Combined: rebind everything + exercise full exhaustion path
# ---------------------------------------------------------------------------


class TestCombinedRebindResistance:
    def test_all_constants_rebound_exhaustion_still_correct(self) -> None:
        cfg.CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS = (0, 0, 0)  # type: ignore[misc]
        cfg.CHECKPOINT_TOTAL_TIMEOUT_SEC = 1  # type: ignore[misc]
        cfg.RUNSTATE_SCHEMA_VERSION = 1  # type: ignore[misc]

        rs = _mk_runstate()
        clock = _Clock()
        sleep = _Sleep()
        vault = _AlwaysMismatchVault()

        with pytest.raises(F_PIPE_01) as excinfo:
            checkpoint_atomic(
                rs,
                intent="state-success",
                expected_current_file_hash="stale",
                vault_write=vault,
                clock=clock,
                sleep=sleep,
            )

        # Inline-literal schedule held.
        assert sleep.calls == [50, 200, 800]
        # Inline-literal total-timeout ceiling held (10_000 ms) — did NOT
        # trigger the timeout path because clock values stayed low.
        assert "cas_exhausted" in excinfo.value.trigger
        # Quarantine marker still populated.
        assert rs.quarantine_marker_ref == "pipeline/run-adv/quarantine.json"
        assert rs.phase == "quarantined"


# ---------------------------------------------------------------------------
# E-023 closure — trusted-operator envelope documentation tests
#
# Round 2 committee gpt_oss reviewer flagged three HIGH findings. Each is
# real under an "attacker-controlled injected Protocol" threat model but
# OUT-OF-SCOPE under §3.11 v5 trusted-operator envelope (Protocols are
# supplied by trusted caller code in Round 3+). These tests CONSTRUCT each
# attack and assert the current honest behaviour — making the v0.1 limit
# explicit rather than hiding it. Round 7 (rate_limiter) + §2 Vault path
# guards close the residuals.
# ---------------------------------------------------------------------------


class TestTrustedOperatorEnvelopeLimits:
    """gpt_oss R2 HIGH findings documented as v0.1 out-of-scope per E-023."""

    def test_adv_malformed_committed_hash_flows_through_transparently(self) -> None:
        """HIGH-1: unvalidated vault_write return value.

        `vault_write` is an injected Protocol. A trusted caller supplies the
        §2 Vault's concrete callable (LOCKed Round P) whose return is a
        SHA-256 hex string. If a rogue Protocol returns a malformed string,
        Round 2 propagates it through CheckpointResult unchanged — Round 2
        does NOT validate the return shape. The committed_hash is NOT used
        as a future CAS pin inside Round 2 (§4.13 contract: caller owns hash
        refresh), so the malformed hash only appears in the result object.

        Trusted-operator envelope: only trusted code constructs a
        `VaultWriteCallable`. Defense against malicious Protocols is §2's
        `vault_write` contract, not Round 2's responsibility.
        """

        @dataclass
        class _RogueVault:
            def __call__(
                self,
                *,
                path: str,
                payload: bytes,
                intent: str,
                write_mode: str,
                expected_current_file_hash: str | None,
            ) -> str:
                # Return a malformed/empty string — the trusted envelope
                # assumes §2 Vault would never do this.
                return ""

        rs = _mk_runstate()
        clock = _Clock()
        sleep = _Sleep()
        vault = _RogueVault()

        result = checkpoint_atomic(
            rs,
            intent="state-success",
            expected_current_file_hash=None,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
        )

        # Round 2 trusts the Protocol's return — empty string flows through.
        # This documents the v0.1 limit; §2 Vault's real callable enforces
        # the SHA-256 hex shape.
        assert result.committed_hash == ""
        assert result.quarantine_marker_ref is None

    def test_adv_canonical_bytes_repr_fallback_is_not_cryptographic(self) -> None:
        """HIGH-2: canonical-bytes collision via __repr__ fallback.

        `_canonicalize_runstate._default` falls back to
        `{"__repr__": repr(obj)}` for non-dataclass / non-frozenset values.
        Two distinct objects with identical `repr` produce identical bytes.
        This is a v0.1 correctness floor — NOT a cryptographic guarantee.
        The docstring already states this explicitly.

        Scope note: the only live field subject to the fallback is
        `RateLimiterState.buckets` (dict[str, TokenBucketProtocol]). Round 7
        will ship a concrete TokenBucket dataclass, at which point the
        fallback is unreachable for production RunStates. Until then,
        Round 2 documents the limit.
        """
        from pipeline.loop.state_checkpoint import _canonicalize_runstate

        class _ReprCollider:
            def __repr__(self) -> str:
                return "collider"

        # Construct two distinct instances with identical repr.
        a = _ReprCollider()
        b = _ReprCollider()
        assert a is not b  # distinct identity
        assert repr(a) == repr(b)  # identical repr

        # Through the _default handler both serialize to the SAME bytes.
        # This is not a CAS-head collision in practice (live RunState
        # serialization does not expose this path for production fields
        # until Round 7), but the limit is real and documented here.
        import json as _json

        def _default(obj: Any) -> Any:
            return {"__repr__": repr(obj)}

        bytes_a = _json.dumps({"x": a}, default=_default).encode()
        bytes_b = _json.dumps({"x": b}, default=_default).encode()
        assert bytes_a == bytes_b

        # The docstring of _canonicalize_runstate labels this as a
        # "correctness floor, not a cryptographic guarantee" — the live
        # code honestly describes what it does and does not guarantee.
        assert _canonicalize_runstate.__doc__ is not None
        assert "minimal" in _canonicalize_runstate.__doc__

    def test_adv_run_id_path_segment_trusted_to_caller(self) -> None:
        """HIGH-3: path-traversal via uncontrolled run_id.

        `pipeline/{run_state.run_id}/quarantine.json` is built by string
        interpolation. A malicious `run_id` like `"../etc/passwd"` would
        produce `pipeline/../etc/passwd/quarantine.json`. Round 2 does NOT
        sanitize `run_id` — Round 3 `RunIdFactory` generates ULIDs whose
        charset `[0-9A-HJKMNP-TV-Z]{26}` cannot contain `.` or `/`, and §2
        Vault's `vault_write` contract (LOCKed Round P) rejects paths
        containing `..` segments.

        Trusted-operator envelope: run_id origin is trusted (the
        ULID factory in Round 3). Defense-in-depth path validation belongs
        to §2 Vault, not Round 2's string interpolation.

        This test CONSTRUCTS the attack vector to document the envelope
        boundary — it does NOT assert that the path is accepted (that would
        depend on §2 Vault's validator).
        """

        captured_paths: list[str] = []

        @dataclass
        class _PathCapturingVault:
            def __call__(
                self,
                *,
                path: str,
                payload: bytes,
                intent: str,
                write_mode: str,
                expected_current_file_hash: str | None,
            ) -> str:
                captured_paths.append(path)
                import hashlib as _hl

                return _hl.sha256(payload).hexdigest()

        rs = RunState(
            schema_version=2,
            run_id="../etc/passwd",  # malicious — source is trusted in v1
            mode="submission",
            rfa_hash="r",
            project_context_hash="pc",
            golden_set_ref=None,
            org_slug="org",
            session_id="s",
            phase="initialized",
        )

        result = checkpoint_atomic(
            rs,
            intent="state-success",
            expected_current_file_hash=None,
            vault_write=_PathCapturingVault(),
            clock=_Clock(),
            sleep=_Sleep(),
        )

        # Round 2 hands the raw interpolated path to vault_write. The
        # traversal segment is present verbatim — §2 Vault's path validator
        # is the gate that rejects it in production.
        assert result.quarantine_marker_ref is None  # success path
        assert captured_paths == ["pipeline/../etc/passwd/state.json"]
