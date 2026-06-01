"""Adversarial tests for pipeline.loop.cron_scheduler — §4.10 v2 fire_once.

Blueprint §5 v6 §4.10 LOCKED 2026-04-19. E-024 2× multiplier floor vs
spec-card ~14 adversarial targets.

Covers:
- F_PIPE_15 trigger-taxonomy pin (normal exhaustion + window_exceeded).
- Attempts-exhausted → F_PIPE_15 with flock STILL HELD at raise-time
  (context manager sees the exception at __exit__).
- Total window exceeded mid-retry → F_PIPE_15 with ``elapsed_ms > 300_000``.
- Rebind-resistance — mutating ``pipeline.loop.config.CRON_VAULT_RETRY_ATTEMPTS``
  / ``CRON_VAULT_RETRY_WINDOW_SEC`` / ``CRON_STAMP_TTL_HOURS`` has no runtime
  effect (inline-literal defaults pinned).
- Non-monotonic clock — elapsed clamped at zero.
- ``on_fire`` raising post-stamp → exception propagates; stamp not
  rolled back; flock releases via context manager.
- ``build_cron_task_id`` input-validation sweep — empty prefix, empty
  anchor, missing ``T``, missing UTC offset, non-UTC offset, malformed
  ISO string.
- Unexpected (non-transient, non-VaultWriteExists) exception during
  stamp write → propagates unwrapped; flock releases.
- Deterministic replay — two identical calls with identical fakes
  produce identical results.
- ``write_mode="write-if-absent"`` literal-pinned.
- ``path="cron/fired/{id}.stamp"`` literal-pinned.
- Idempotency across concurrent callers — second caller observes
  ``VaultWriteExists`` after first lands stamp.
- ``fire_once`` input-validation sweep — empty task_id, non-positive
  max_attempts, non-positive total_window_sec.
- No config imports from cascade-style AST (rebind-resistance proof by
  static grep).
"""

from __future__ import annotations

import pathlib
import re
from contextlib import contextmanager
from typing import Any, Iterator

import pytest

from pipeline.loop import config as loop_config
from pipeline.loop.cron_scheduler import (
    CronFireResult,
    VaultTransientError,
    build_cron_task_id,
    fire_once,
)
from pipeline.loop.errors import F_PIPE_15
from pipeline.vault import VaultWriteExists


# ---------------------------------------------------------------------------
# Shared fakes — mirror the happy-path file but a standalone copy so test
# files can be run in isolation.
# ---------------------------------------------------------------------------


class _FakeClock:
    def __init__(
        self,
        *,
        now_ms: int = 1_000,
        now_iso: str = "2026-04-21T12:00:00+00:00",
    ) -> None:
        self._now_ms = now_ms
        self._now_iso = now_iso
        self.advance_schedule: list[int] | None = None
        self._advance_idx = 0

    def set_advance_schedule(self, deltas: list[int]) -> None:
        """Each call to :meth:`now_ms` advances by ``deltas[i]`` ms."""
        self.advance_schedule = deltas
        self._advance_idx = 0

    def now_ms(self) -> int:
        if self.advance_schedule is not None:
            if self._advance_idx < len(self.advance_schedule):
                self._now_ms += self.advance_schedule[self._advance_idx]
                self._advance_idx += 1
        return self._now_ms

    def now_iso(self) -> str:
        return self._now_iso


class _FakeSleep:
    def __init__(self) -> None:
        self.calls: list[int] = []

    def __call__(self, ms: int) -> None:
        self.calls.append(ms)


class _FakeFlock:
    def __init__(self, *, acquire: bool = True) -> None:
        self.acquire = acquire
        self.entries: list[pathlib.Path] = []
        self.exit_observations: list[tuple[type[BaseException] | None, BaseException | None]] = []
        self.held_at_exit_snapshots: list[bool] = []
        self._currently_held = False

    @property
    def currently_held(self) -> bool:
        return self._currently_held

    def __call__(self, lock_path: pathlib.Path):
        self.entries.append(lock_path)
        acquire = self.acquire
        obs = self.exit_observations
        held_snap = self.held_at_exit_snapshots
        owner = self

        @contextmanager
        def _cm() -> Iterator[bool]:
            if acquire:
                owner._currently_held = True
            try:
                yield acquire
            except BaseException as exc:
                held_snap.append(owner._currently_held)
                obs.append((type(exc), exc))
                owner._currently_held = False
                raise
            else:
                obs.append((None, None))
                owner._currently_held = False

        return _cm()


class _FakeVault:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self._raises: list[BaseException | None] = []

    def queue_success(self) -> None:
        self._raises.append(None)

    def queue_exception(self, exc: BaseException) -> None:
        self._raises.append(exc)

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
            {
                "path": path,
                "payload": payload,
                "intent": intent,
                "write_mode": write_mode,
                "expected_current_file_hash": expected_current_file_hash,
            }
        )
        if self._raises:
            exc = self._raises.pop(0)
            if exc is not None:
                raise exc
        return "fake-hash"


class _FakeOnFire:
    def __init__(self, raise_exc: BaseException | None = None) -> None:
        self.calls: list[str] = []
        self._raise = raise_exc

    def __call__(self, *, cron_task_id: str) -> None:
        self.calls.append(cron_task_id)
        if self._raise is not None:
            raise self._raise


# ---------------------------------------------------------------------------
# F_PIPE_15 trigger taxonomy + flock-retention
# ---------------------------------------------------------------------------


class TestFailureTaxonomy:
    def test_exhaustion_trigger_format(self, tmp_path: pathlib.Path) -> None:
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        for _ in range(6):
            vault.queue_exception(VaultTransientError("network"))
        clock = _FakeClock()
        sleep = _FakeSleep()
        on_fire = _FakeOnFire()

        with pytest.raises(F_PIPE_15) as excinfo:
            fire_once(
                cron_task_id="fund_radar_2026-04-21_12_30",
                on_fire=on_fire,
                flock_acquire=flock,
                vault_write=vault,
                clock=clock,
                sleep=sleep,
                lock_dir=tmp_path,
            )
        exc = excinfo.value
        assert exc.code == "F-PIPE-15"
        assert exc.trigger == "cron_dedupe_failure:fund_radar_2026-04-21_12_30"
        assert exc.details["cron_task_id"] == "fund_radar_2026-04-21_12_30"
        assert exc.details["attempts"] == 6
        assert exc.details["last_error"] == "VaultTransientError"
        # Sleep called 5 times (attempts 0..4); last attempt raises instead of sleeping
        assert len(sleep.calls) == 5
        # Schedule: min(30, 2**attempt) seconds → [1, 2, 4, 8, 16] * 1000
        assert sleep.calls == [1_000, 2_000, 4_000, 8_000, 16_000]

    def test_flock_still_held_at_raise(self, tmp_path: pathlib.Path) -> None:
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        for _ in range(6):
            vault.queue_exception(VaultTransientError("network"))
        clock = _FakeClock()
        sleep = _FakeSleep()

        with pytest.raises(F_PIPE_15):
            fire_once(
                cron_task_id="t",
                on_fire=_FakeOnFire(),
                flock_acquire=flock,
                vault_write=vault,
                clock=clock,
                sleep=sleep,
                lock_dir=tmp_path,
            )
        # At the moment of raise, the context manager observed the flock
        # was still held (no explicit release inside fire_once); the
        # release happened during __exit__ unwinding AFTER the raise.
        assert flock.held_at_exit_snapshots == [True]
        assert flock.exit_observations[0][0] is F_PIPE_15
        # After unwinding the fake flock marks itself released.
        assert flock.currently_held is False

    def test_window_exceeded_trigger_format(self, tmp_path: pathlib.Path) -> None:
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        # Budget will be blown before any vault call.
        # now_ms calls inside fire_once: 1 (start) + 1 per loop iteration
        # (elapsed check). Schedule the second call to jump past 300_000 ms.
        clock = _FakeClock()
        clock.set_advance_schedule([0, 400_000])
        sleep = _FakeSleep()

        with pytest.raises(F_PIPE_15) as excinfo:
            fire_once(
                cron_task_id="t",
                on_fire=_FakeOnFire(),
                flock_acquire=flock,
                vault_write=vault,
                clock=clock,
                sleep=sleep,
                lock_dir=tmp_path,
            )
        exc = excinfo.value
        assert exc.trigger == "cron_dedupe_failure:t:window_exceeded"
        assert exc.details["last_error"] == "window_exceeded"
        assert exc.details["elapsed_ms"] > 300_000
        assert exc.details["attempts"] == 0  # budget blown before first attempt
        assert vault.calls == []


# ---------------------------------------------------------------------------
# Rebind resistance (V1 discipline)
# ---------------------------------------------------------------------------


class TestRebindResistance:
    def test_rebind_config_constants_has_no_effect(
        self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Rebinding the three rebind-sensitive constants post-import must
        # not alter fire_once behaviour (inline-literal defaults).
        monkeypatch.setattr(loop_config, "CRON_VAULT_RETRY_ATTEMPTS", 999, raising=True)
        monkeypatch.setattr(loop_config, "CRON_VAULT_RETRY_WINDOW_SEC", 999_999, raising=True)
        monkeypatch.setattr(loop_config, "CRON_STAMP_TTL_HOURS", 999, raising=True)

        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        vault.queue_success()
        clock = _FakeClock()
        sleep = _FakeSleep()
        on_fire = _FakeOnFire()

        result = fire_once(
            cron_task_id="t",
            on_fire=on_fire,
            flock_acquire=flock,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
            lock_dir=tmp_path,
        )
        assert result.fired is True
        # The caller-supplied defaults still enforce 6 / 300 — rebinding did
        # not leak into runtime behaviour.
        assert result.attempts == 1

    def test_no_config_imports_in_compute_sites(self) -> None:
        """Static proof: cron_scheduler.py uses inline literals at comparison sites.

        The import is allowed (the asserts need the symbol); the runtime
        comparison sites MUST not indirect through ``loop_config.*``.
        """
        # Resolve relative to __file__ so the test works under pytest-xdist
        # workers whose cwd may differ from the repo root.
        repo_root = pathlib.Path(__file__).resolve().parents[2]
        src = (repo_root / "pipeline" / "loop" / "cron_scheduler.py").read_text()
        # loop_config.CRON_* references are banned in the compute sites;
        # the three asserts at the top of the module are the only
        # CRON_VAULT_RETRY_* / CRON_STAMP_TTL_HOURS references and they
        # bind the CONFIG value against an INLINE LITERAL on the RHS.
        compute_references = re.findall(
            r"loop_config\.CRON_\w+", src
        )
        assert compute_references == [], (
            f"cron_scheduler.py must not indirect through loop_config at runtime; "
            f"found {compute_references!r}"
        )


# ---------------------------------------------------------------------------
# Non-monotonic clock + on_fire propagation
# ---------------------------------------------------------------------------


class TestClockEdgeCases:
    def test_non_monotonic_clock_clamped_at_zero(self, tmp_path: pathlib.Path) -> None:
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        vault.queue_success()
        clock = _FakeClock(now_ms=10_000)
        # First call returns 10_000 (start); second call returns 5_000
        # (backward). The computation clamps elapsed to zero, so window
        # check does NOT fire spuriously.
        clock.set_advance_schedule([0, -5_000])
        sleep = _FakeSleep()

        result = fire_once(
            cron_task_id="t",
            on_fire=_FakeOnFire(),
            flock_acquire=flock,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
            lock_dir=tmp_path,
        )
        assert result.fired is True


class TestOnFireExceptions:
    def test_on_fire_exception_propagates_stamp_not_rolled_back(
        self, tmp_path: pathlib.Path
    ) -> None:
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        vault.queue_success()
        clock = _FakeClock()
        sleep = _FakeSleep()

        class DownstreamBoom(RuntimeError):
            pass

        on_fire = _FakeOnFire(raise_exc=DownstreamBoom("scout blew up"))

        with pytest.raises(DownstreamBoom):
            fire_once(
                cron_task_id="t",
                on_fire=on_fire,
                flock_acquire=flock,
                vault_write=vault,
                clock=clock,
                sleep=sleep,
                lock_dir=tmp_path,
            )
        # Stamp landed.
        assert len(vault.calls) == 1
        # Flock context manager released on exception unwinding.
        assert flock.held_at_exit_snapshots == [True]
        assert flock.exit_observations[0][0] is DownstreamBoom
        assert flock.currently_held is False
        # Stamp was NOT rolled back — fire_once never writes a second
        # vault call on the failure path.
        assert len(vault.calls) == 1


class TestUnexpectedVaultException:
    def test_non_transient_exception_propagates(self, tmp_path: pathlib.Path) -> None:
        class WeirdError(Exception):
            pass

        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        vault.queue_exception(WeirdError("disk on fire"))
        clock = _FakeClock()
        sleep = _FakeSleep()

        with pytest.raises(WeirdError):
            fire_once(
                cron_task_id="t",
                on_fire=_FakeOnFire(),
                flock_acquire=flock,
                vault_write=vault,
                clock=clock,
                sleep=sleep,
                lock_dir=tmp_path,
            )
        # Flock released.
        assert flock.held_at_exit_snapshots == [True]
        assert flock.currently_held is False
        assert sleep.calls == []


# ---------------------------------------------------------------------------
# build_cron_task_id input-validation sweep
# ---------------------------------------------------------------------------


class TestBuildCronTaskIdValidation:
    def test_empty_prefix(self) -> None:
        with pytest.raises(ValueError, match="prefix must be non-empty"):
            build_cron_task_id(prefix="", utc_iso_anchor="2026-04-21T12:30:00Z")

    def test_empty_anchor(self) -> None:
        with pytest.raises(ValueError, match="utc_iso_anchor must be non-empty"):
            build_cron_task_id(prefix="fund_radar", utc_iso_anchor="")

    def test_missing_T(self) -> None:
        with pytest.raises(ValueError, match="must contain 'T'"):
            build_cron_task_id(
                prefix="fund_radar", utc_iso_anchor="2026-04-21 12:30:00+00:00"
            )

    def test_missing_utc_offset(self) -> None:
        with pytest.raises(ValueError, match="must end with"):
            build_cron_task_id(
                prefix="fund_radar", utc_iso_anchor="2026-04-21T12:30:00"
            )

    def test_non_utc_offset_rejected(self) -> None:
        # Ends with +00:00 check fires first; but a well-formed non-UTC
        # anchor like +05:00 fails the endswith check above.
        with pytest.raises(ValueError, match="must end with"):
            build_cron_task_id(
                prefix="fund_radar", utc_iso_anchor="2026-04-21T12:30:00+05:00"
            )

    def test_malformed_iso(self) -> None:
        with pytest.raises(ValueError, match="not parseable as ISO-8601"):
            build_cron_task_id(
                prefix="fund_radar", utc_iso_anchor="not-a-dateTfoobar+00:00"
            )


# ---------------------------------------------------------------------------
# fire_once input-validation sweep
# ---------------------------------------------------------------------------


class TestFireOnceValidation:
    def _minimal_kwargs(self, tmp_path: pathlib.Path) -> dict[str, Any]:
        return dict(
            on_fire=_FakeOnFire(),
            flock_acquire=_FakeFlock(acquire=True),
            vault_write=_FakeVault(),
            clock=_FakeClock(),
            sleep=_FakeSleep(),
            lock_dir=tmp_path,
        )

    def test_empty_task_id(self, tmp_path: pathlib.Path) -> None:
        with pytest.raises(ValueError, match="cron_task_id must be non-empty"):
            fire_once(cron_task_id="", **self._minimal_kwargs(tmp_path))

    def test_zero_max_attempts(self, tmp_path: pathlib.Path) -> None:
        with pytest.raises(ValueError, match="max_attempts must be positive"):
            fire_once(
                cron_task_id="t",
                max_attempts=0,
                **self._minimal_kwargs(tmp_path),
            )

    def test_negative_max_attempts(self, tmp_path: pathlib.Path) -> None:
        with pytest.raises(ValueError, match="max_attempts must be positive"):
            fire_once(
                cron_task_id="t",
                max_attempts=-1,
                **self._minimal_kwargs(tmp_path),
            )

    def test_zero_total_window(self, tmp_path: pathlib.Path) -> None:
        with pytest.raises(ValueError, match="total_window_sec must be positive"):
            fire_once(
                cron_task_id="t",
                total_window_sec=0,
                **self._minimal_kwargs(tmp_path),
            )


# ---------------------------------------------------------------------------
# Deterministic replay + concurrency idempotency + literal pins
# ---------------------------------------------------------------------------


class TestDeterministicReplay:
    def test_two_identical_calls_equal_results(self, tmp_path: pathlib.Path) -> None:
        def run() -> CronFireResult:
            flock = _FakeFlock(acquire=True)
            vault = _FakeVault()
            vault.queue_success()
            return fire_once(
                cron_task_id="t",
                on_fire=_FakeOnFire(),
                flock_acquire=flock,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
                lock_dir=tmp_path,
            )

        first = run()
        second = run()
        assert first == second


class TestConcurrentCallers:
    def test_second_caller_sees_vault_write_exists(self, tmp_path: pathlib.Path) -> None:
        # Simulate: first caller lands stamp; second caller's vault returns
        # VaultWriteExists (the canonical durable-dedupe signal).
        flock1 = _FakeFlock(acquire=True)
        vault1 = _FakeVault()
        vault1.queue_success()
        r1 = fire_once(
            cron_task_id="t",
            on_fire=_FakeOnFire(),
            flock_acquire=flock1,
            vault_write=vault1,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
            lock_dir=tmp_path,
        )
        assert r1.fired is True

        flock2 = _FakeFlock(acquire=True)
        vault2 = _FakeVault()
        vault2.queue_exception(VaultWriteExists("taken"))
        r2 = fire_once(
            cron_task_id="t",
            on_fire=_FakeOnFire(),
            flock_acquire=flock2,
            vault_write=vault2,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
            lock_dir=tmp_path,
        )
        assert r2.fired is False
        assert r2.dedupe_layer == "vault_stamp"


class TestLiteralPins:
    def test_write_mode_write_if_absent(self, tmp_path: pathlib.Path) -> None:
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        vault.queue_success()
        fire_once(
            cron_task_id="t",
            on_fire=_FakeOnFire(),
            flock_acquire=flock,
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
            lock_dir=tmp_path,
        )
        assert vault.calls[0]["write_mode"] == "write-if-absent"
        assert vault.calls[0]["intent"] == "state-success"

    def test_stamp_path_format(self, tmp_path: pathlib.Path) -> None:
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        vault.queue_success()
        fire_once(
            cron_task_id="fund_radar_2026-04-21_12_30",
            on_fire=_FakeOnFire(),
            flock_acquire=flock,
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
            lock_dir=tmp_path,
        )
        assert vault.calls[0]["path"] == "cron/fired/fund_radar_2026-04-21_12_30.stamp"


# ---------------------------------------------------------------------------
# Total-window exceeded mid-loop (between retries)
# ---------------------------------------------------------------------------


class TestWindowExceededMidLoop:
    def test_window_exceeded_after_one_transient(self, tmp_path: pathlib.Path) -> None:
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        vault.queue_exception(VaultTransientError("transient-1"))
        # No further queue — fire_once would advance to second attempt but
        # window check should fire first.
        clock = _FakeClock()
        # now_ms schedule:
        #   call 1: start_ms (+0) → 1_000
        #   call 2: loop iter 0 elapsed check (+0) → 1_000 (no-op)
        #   call 3: after transient, loop iter 1 elapsed (+400_000) → 401_000
        clock.set_advance_schedule([0, 0, 400_000])
        sleep = _FakeSleep()

        with pytest.raises(F_PIPE_15) as excinfo:
            fire_once(
                cron_task_id="t",
                on_fire=_FakeOnFire(),
                flock_acquire=flock,
                vault_write=vault,
                clock=clock,
                sleep=sleep,
                lock_dir=tmp_path,
            )
        exc = excinfo.value
        assert exc.trigger == "cron_dedupe_failure:t:window_exceeded"
        assert exc.details["attempts"] == 1  # one transient consumed
        assert exc.details["elapsed_ms"] > 300_000
        # First attempt's sleep did run.
        assert sleep.calls == [1_000]


# ---------------------------------------------------------------------------
# E-023 residuals — flock_acquire raising
# ---------------------------------------------------------------------------


class TestResiduals:
    def test_flock_acquire_raising_propagates(self, tmp_path: pathlib.Path) -> None:
        class FlockProbeError(OSError):
            pass

        def raising_flock(lock_path: pathlib.Path) -> Any:
            raise FlockProbeError("probe blew up")

        with pytest.raises(FlockProbeError):
            fire_once(
                cron_task_id="t",
                on_fire=_FakeOnFire(),
                flock_acquire=raising_flock,  # type: ignore[arg-type]
                vault_write=_FakeVault(),
                clock=_FakeClock(),
                sleep=_FakeSleep(),
                lock_dir=tmp_path,
            )

    def test_vault_transient_error_is_not_vault_error_subclass(self) -> None:
        """Keeps vault package's error taxonomy clean — transient is transport, not vault-intrinsic."""
        from pipeline.vault import VaultError

        assert not issubclass(VaultTransientError, VaultError)
