"""Tests for pipeline.loop.cron_scheduler — §4.10 v2 fire_once + build_cron_task_id.

Blueprint §5 v6 §4.10 LOCKED 2026-04-19.

Happy-path coverage targets (spec card
``section_05_round_10_cron_scheduler.md``):

- First-fire success — flock acquired, stamp written first try, on_fire
  invoked, CronFireResult(fired=True, dedupe_layer=None, attempts=1).
- Flock contention — acquire yields False → dedupe_layer="flock",
  attempts=0, on_fire NOT called.
- Vault stamp already exists → dedupe_layer="vault_stamp", attempts=1,
  on_fire NOT called.
- Vault transient retry-and-win — first attempt raises
  VaultTransientError, second succeeds; attempts=2.
- ``build_cron_task_id`` DST-safe (two 08:30 local firings during fall-back
  map to distinct UTC-anchored ids).
- ``build_cron_task_id`` format pin.
- ``build_cron_task_id`` accepts ``Z`` suffix.
- Lock-directory creation — parents mkdir when absent.
- Back-off schedule pin — first retry sleeps 1000ms (min(30, 2**0)=1s).
- CronFireResult surface contract (immutability + field set).
"""

from __future__ import annotations

import pathlib
from contextlib import contextmanager
from typing import Any, Iterator

import pytest

from pipeline.loop.cron_scheduler import (
    CronFireResult,
    FlockAcquire,
    OnFireCallable,
    VaultTransientError,
    build_cron_task_id,
    fire_once,
)
from pipeline.vault import VaultWriteExists


# ---------------------------------------------------------------------------
# Fakes / fixtures
# ---------------------------------------------------------------------------


class _FakeClock:
    def __init__(self, *, now_ms: int = 1_000, now_iso: str = "2026-04-21T12:00:00+00:00") -> None:
        self._now_ms = now_ms
        self._now_iso = now_iso
        self.now_ms_calls = 0
        self.now_iso_calls = 0

    def advance(self, ms: int) -> None:
        self._now_ms += ms

    def now_ms(self) -> int:
        self.now_ms_calls += 1
        return self._now_ms

    def now_iso(self) -> str:
        self.now_iso_calls += 1
        return self._now_iso


class _FakeSleep:
    def __init__(self) -> None:
        self.calls: list[int] = []

    def __call__(self, ms: int) -> None:
        self.calls.append(ms)


class _FakeFlock:
    """Records context-manager observations without touching the filesystem."""

    def __init__(self, *, acquire: bool = True) -> None:
        self.acquire = acquire
        self.entries: list[pathlib.Path] = []
        self.exit_observations: list[tuple[type[BaseException] | None, str | None]] = []

    def __call__(self, lock_path: pathlib.Path):
        self.entries.append(lock_path)
        acquire = self.acquire
        exit_obs = self.exit_observations

        @contextmanager
        def _cm() -> Iterator[bool]:
            try:
                yield acquire
            except BaseException as exc:
                exit_obs.append((type(exc), repr(exc)))
                raise
            else:
                exit_obs.append((None, None))

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
    def __init__(self) -> None:
        self.calls: list[str] = []

    def __call__(self, *, cron_task_id: str) -> None:
        self.calls.append(cron_task_id)


# ---------------------------------------------------------------------------
# build_cron_task_id — happy paths
# ---------------------------------------------------------------------------


class TestBuildCronTaskId:
    def test_format_pin(self) -> None:
        tid = build_cron_task_id(
            prefix="fund_radar", utc_iso_anchor="2026-04-21T12:30:00+00:00"
        )
        assert tid == "fund_radar_2026-04-21_12_30"

    def test_z_suffix_accepted(self) -> None:
        tid = build_cron_task_id(
            prefix="fund_radar", utc_iso_anchor="2026-04-21T12:30:00Z"
        )
        assert tid == "fund_radar_2026-04-21_12_30"

    def test_dst_fall_back_distinguished(self) -> None:
        # US DST fall-back 2026-11-01 — local clocks run 01:30 EDT then
        # 01:30 EST. UTC anchors differ by one hour → distinct task-ids.
        first = build_cron_task_id(
            prefix="fund_radar", utc_iso_anchor="2026-11-01T05:30:00+00:00"
        )
        second = build_cron_task_id(
            prefix="fund_radar", utc_iso_anchor="2026-11-01T06:30:00+00:00"
        )
        assert first != second
        assert first == "fund_radar_2026-11-01_05_30"
        assert second == "fund_radar_2026-11-01_06_30"

    def test_different_prefix_produces_distinct_id(self) -> None:
        a = build_cron_task_id(
            prefix="fund_radar", utc_iso_anchor="2026-04-21T12:30:00+00:00"
        )
        b = build_cron_task_id(
            prefix="deep_brief", utc_iso_anchor="2026-04-21T12:30:00+00:00"
        )
        assert a != b


# ---------------------------------------------------------------------------
# fire_once — happy paths
# ---------------------------------------------------------------------------


class TestFireOnceHappyPaths:
    def test_first_fire_success(self, tmp_path: pathlib.Path) -> None:
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        vault.queue_success()
        clock = _FakeClock()
        sleep = _FakeSleep()
        on_fire = _FakeOnFire()

        result = fire_once(
            cron_task_id="fund_radar_2026-04-21_12_30",
            on_fire=on_fire,
            flock_acquire=flock,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
            lock_dir=tmp_path,
        )

        assert result == CronFireResult(
            cron_task_id="fund_radar_2026-04-21_12_30",
            fired=True,
            dedupe_layer=None,
            attempts=1,
        )
        assert on_fire.calls == ["fund_radar_2026-04-21_12_30"]
        assert len(vault.calls) == 1
        assert vault.calls[0]["path"] == "cron/fired/fund_radar_2026-04-21_12_30.stamp"
        assert vault.calls[0]["write_mode"] == "write-if-absent"
        assert vault.calls[0]["intent"] == "state-success"
        assert vault.calls[0]["expected_current_file_hash"] is None
        assert vault.calls[0]["payload"] == b"2026-04-21T12:00:00+00:00"
        assert sleep.calls == []
        assert flock.exit_observations == [(None, None)]

    def test_flock_contention_short_circuits(self, tmp_path: pathlib.Path) -> None:
        flock = _FakeFlock(acquire=False)
        vault = _FakeVault()
        clock = _FakeClock()
        sleep = _FakeSleep()
        on_fire = _FakeOnFire()

        result = fire_once(
            cron_task_id="fund_radar_2026-04-21_12_30",
            on_fire=on_fire,
            flock_acquire=flock,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
            lock_dir=tmp_path,
        )

        assert result.fired is False
        assert result.dedupe_layer == "flock"
        assert result.attempts == 0
        assert vault.calls == []
        assert on_fire.calls == []
        assert flock.exit_observations == [(None, None)]

    def test_vault_stamp_already_exists(self, tmp_path: pathlib.Path) -> None:
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        vault.queue_exception(VaultWriteExists("already fired"))
        clock = _FakeClock()
        sleep = _FakeSleep()
        on_fire = _FakeOnFire()

        result = fire_once(
            cron_task_id="fund_radar_2026-04-21_12_30",
            on_fire=on_fire,
            flock_acquire=flock,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
            lock_dir=tmp_path,
        )

        assert result.fired is False
        assert result.dedupe_layer == "vault_stamp"
        assert result.attempts == 1
        assert len(vault.calls) == 1
        assert on_fire.calls == []
        assert sleep.calls == []

    def test_transient_retry_and_win(self, tmp_path: pathlib.Path) -> None:
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        vault.queue_exception(VaultTransientError("connection reset"))
        vault.queue_success()
        clock = _FakeClock()
        sleep = _FakeSleep()
        on_fire = _FakeOnFire()

        result = fire_once(
            cron_task_id="fund_radar_2026-04-21_12_30",
            on_fire=on_fire,
            flock_acquire=flock,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
            lock_dir=tmp_path,
        )

        assert result.fired is True
        assert result.dedupe_layer is None
        assert result.attempts == 2
        assert sleep.calls == [1000]  # min(30, 2**0) * 1000
        assert on_fire.calls == ["fund_radar_2026-04-21_12_30"]

    def test_lock_directory_created_when_absent(self, tmp_path: pathlib.Path) -> None:
        nested = tmp_path / "a" / "b" / "c"
        assert not nested.exists()
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        vault.queue_success()
        clock = _FakeClock()
        sleep = _FakeSleep()
        on_fire = _FakeOnFire()

        result = fire_once(
            cron_task_id="fund_radar_2026-04-21_12_30",
            on_fire=on_fire,
            flock_acquire=flock,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
            lock_dir=nested,
        )
        assert result.fired is True
        assert nested.exists() and nested.is_dir()
        assert flock.entries == [nested / "fund_radar_2026-04-21_12_30.lock"]

    def test_back_off_schedule_first_second_third_retry(self, tmp_path: pathlib.Path) -> None:
        # Three transients then a win: sleep schedule = [1_000, 2_000, 4_000] ms
        flock = _FakeFlock(acquire=True)
        vault = _FakeVault()
        for _ in range(3):
            vault.queue_exception(VaultTransientError("transient"))
        vault.queue_success()
        clock = _FakeClock()
        sleep = _FakeSleep()
        on_fire = _FakeOnFire()

        result = fire_once(
            cron_task_id="fund_radar_2026-04-21_12_30",
            on_fire=on_fire,
            flock_acquire=flock,
            vault_write=vault,
            clock=clock,
            sleep=sleep,
            lock_dir=tmp_path,
        )
        assert result.fired is True
        assert result.attempts == 4
        # attempts 0,1,2 each sleep min(30, 2**attempt) * 1000
        assert sleep.calls == [1000, 2000, 4000]


# ---------------------------------------------------------------------------
# CronFireResult surface contract
# ---------------------------------------------------------------------------


class TestCronFireResult:
    def test_is_frozen_slotted(self) -> None:
        r = CronFireResult(
            cron_task_id="t", fired=True, dedupe_layer=None, attempts=1
        )
        with pytest.raises((AttributeError, Exception)):
            r.fired = False  # type: ignore[misc]

    def test_field_set(self) -> None:
        r = CronFireResult(
            cron_task_id="t", fired=False, dedupe_layer="flock", attempts=0
        )
        assert r.cron_task_id == "t"
        assert r.fired is False
        assert r.dedupe_layer == "flock"
        assert r.attempts == 0
