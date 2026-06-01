"""Adversarial tests for pipeline.loop.rate_limiter — E-024 2× multiplier.

Spec card: ``section_05_round_7_rate_limiter.md``.

Covers (non-exhaustively):

- V1 inline-literal discipline: rebinding
  ``CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS`` / ``RATE_LIMIT_JITTER_RANGE_MS`` /
  ``RATE_LIMIT_LEASE_TTL_SEC`` on :mod:`pipeline.loop.config` is a no-op
  for runtime behaviour.
- Non-monotonic clock → refill delta clamped at zero.
- Half-present lease → ``ValueError`` from
  ``RateLimiterState.__post_init__`` bubbles unwrapped (E-023 residual).
- Zero-capacity / zero-refill buckets — degenerate configurations never
  synthesize tokens.
- ``F_PIPE_06`` sub-trigger taxonomy pin for both reserve + release
  exhaustion paths.
- ``release`` idempotency (non-owner, no-lease).
- ``can_reserve`` purity (no writes, no sleeps, no randint).
- A-v1-09 concurrent-reserve regression: two processes, first wins.
- Empty ``buckets`` dict → ``KeyError``.
- Malformed vault bytes → ``json.JSONDecodeError``.
- Jitter additivity pin: sleep values reflect the injected jitter.
- Lease TTL stamp pin: ``lease_expires_at_iso`` is exactly
  ``now + 30 s`` in iso ms.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

import pytest

from pipeline.loop import config as loop_config
from pipeline.loop.errors import F_PIPE_06, PipelineFailure
from pipeline.loop.rate_limiter import (
    TokenBucket,
    can_reserve,
    release,
    reserve,
)
from pipeline.loop.types import RateLimiterState
from pipeline.vault import VaultCASHeadMismatch


# ---------------------------------------------------------------------------
# Fixtures / fakes (trimmed clones of test_rate_limiter.py helpers)
# ---------------------------------------------------------------------------


def _mk_state(
    *,
    endpoint: str = "anthropic_scribe",
    capacity: int = 100,
    tokens: float = 100.0,
    refill_rate_per_sec: float = 10.0,
    last_refill_iso: str = "2026-04-21T12:00:00.000+00:00",
    lease_holder_id: str | None = None,
    lease_expires_at_iso: str | None = None,
) -> RateLimiterState:
    return RateLimiterState(
        buckets={
            endpoint: TokenBucket(
                capacity=capacity,
                tokens=tokens,
                refill_rate_per_sec=refill_rate_per_sec,
            )
        },
        last_refill_iso=last_refill_iso,
        lease_holder_id=lease_holder_id,
        lease_expires_at_iso=lease_expires_at_iso,
    )


def _serialize(state: RateLimiterState) -> bytes:
    return json.dumps(
        asdict(state), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


@dataclass
class _FakeClock:
    values: list[int] = field(default_factory=lambda: [1_714_000_000_000])
    _i: int = 0

    def now_ms(self) -> int:
        if self._i >= len(self.values):
            return self.values[-1] if self.values else 0
        v = self.values[self._i]
        self._i += 1
        return v

    def now_iso(self) -> str:
        return "2026-04-21T12:00:00.000+00:00"


@dataclass
class _FakeSleep:
    calls: list[int] = field(default_factory=list)

    def __call__(self, ms: int) -> None:
        self.calls.append(ms)


@dataclass
class _FakeRandInt:
    sequence: list[int] = field(default_factory=list)
    calls: list[tuple[int, int]] = field(default_factory=list)
    _i: int = 0

    def __call__(self, a: int, b: int) -> int:
        self.calls.append((a, b))
        if self._i >= len(self.sequence):
            return 0
        v = self.sequence[self._i]
        self._i += 1
        return v


@dataclass
class _FakeVault:
    store: dict[str, bytes] = field(default_factory=dict)
    head_mutations: dict[str, int] = field(default_factory=dict)
    write_attempts: dict[str, int] = field(default_factory=dict)
    read_calls: list[str] = field(default_factory=list)
    write_calls: list[dict[str, Any]] = field(default_factory=list)

    def read(self, *, path: str) -> bytes:
        self.read_calls.append(path)
        if path not in self.store:
            raise KeyError(path)
        return self.store[path]

    def write(
        self,
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        self.write_calls.append(
            dict(
                path=path,
                payload=payload,
                intent=intent,
                write_mode=write_mode,
                expected_current_file_hash=expected_current_file_hash,
            )
        )
        self.write_attempts[path] = self.write_attempts.get(path, 0) + 1
        mismatches_before_win = self.head_mutations.get(path, 0)
        if self.write_attempts[path] <= mismatches_before_win:
            raise VaultCASHeadMismatch(
                "cas mismatch (fake)",
                expected_current_file_hash=expected_current_file_hash or "",
                actual_current_file_hash=hashlib.sha256(b"actual").hexdigest(),
            )
        new_hash = hashlib.sha256(payload).hexdigest()
        self.store[path] = payload
        return new_hash


def _preload(vault: _FakeVault, state: RateLimiterState, endpoint: str) -> None:
    vault.store[f"pipeline/rate_limiter/{endpoint}.json"] = _serialize(state)


def _iso_to_ms(iso: str) -> int:
    return int(datetime.fromisoformat(iso).timestamp() * 1000)


# ---------------------------------------------------------------------------
# V1 rebind-resistance (inline-literal discipline)
# ---------------------------------------------------------------------------


class TestRebindResistance:
    def test_backoff_schedule_rebind_no_effect(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Rebinding config.CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS is a no-op.

        Rate-limiter inlines (50, 200, 800); the rebound value is never read.
        """
        monkeypatch.setattr(
            loop_config, "CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS", (1, 2, 3)
        )

        ep = "anthropic_scribe"
        path = f"pipeline/rate_limiter/{ep}.json"
        vault = _FakeVault(head_mutations={path: 99})
        _preload(vault, _mk_state(endpoint=ep), ep)
        clock = _FakeClock(values=[1_714_000_000_000] * 10)
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        with pytest.raises(F_PIPE_06):
            reserve(
                endpoint=ep,
                estimated_tokens=5,
                process_id="PID",
                vault_read=vault.read,
                vault_write=vault.write,
                clock=clock,
                sleep=sleep,
                randint=randint,
            )

        # Inline literals (50, 200, 800) — NOT the rebound (1, 2, 3).
        assert sleep.calls == [50, 200, 800]

    def test_jitter_range_rebind_no_effect(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Rebinding config.RATE_LIMIT_JITTER_RANGE_MS is a no-op."""
        monkeypatch.setattr(
            loop_config, "RATE_LIMIT_JITTER_RANGE_MS", (9999, 9999)
        )

        ep = "anthropic_scribe"
        path = f"pipeline/rate_limiter/{ep}.json"
        vault = _FakeVault(head_mutations={path: 99})
        _preload(vault, _mk_state(endpoint=ep), ep)
        clock = _FakeClock(values=[1_714_000_000_000] * 10)
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        with pytest.raises(F_PIPE_06):
            reserve(
                endpoint=ep,
                estimated_tokens=5,
                process_id="PID",
                vault_read=vault.read,
                vault_write=vault.write,
                clock=clock,
                sleep=sleep,
                randint=randint,
            )

        # randint always called with inline (0, 300) — NOT (9999, 9999).
        assert randint.calls == [(0, 300)] * 3

    def test_lease_ttl_rebind_no_effect(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Rebinding config.RATE_LIMIT_LEASE_TTL_SEC is a no-op.

        ``lease_expires_at_iso`` always lands at ``now + 30 s`` regardless
        of what the config attribute now says.
        """
        monkeypatch.setattr(loop_config, "RATE_LIMIT_LEASE_TTL_SEC", 999_999)

        ep = "anthropic_scribe"
        vault = _FakeVault()
        _preload(vault, _mk_state(endpoint=ep), ep)
        now_ms = 1_745_236_800_000  # 2026-04-21T12:00:00Z
        clock = _FakeClock(values=[now_ms, now_ms + 1])
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        result = reserve(
            endpoint=ep,
            estimated_tokens=5,
            process_id="PID",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        from pipeline.loop.rate_limiter import Reserved

        assert isinstance(result, Reserved)
        expected_expiry_ms = now_ms + 30 * 1000  # inline 30 s
        assert _iso_to_ms(result.lease_expires_at_iso) == expected_expiry_ms


# ---------------------------------------------------------------------------
# Clock / refill / edge-case bucket shapes
# ---------------------------------------------------------------------------


class TestRefillEdgeCases:
    def test_non_monotonic_clock_clamp_no_negative_refill(self) -> None:
        """Clock goes backward → refill delta clamps at 0, no token loss."""
        ep = "anthropic_scribe"
        # last_refill far in the future relative to the clock.
        pre = _mk_state(
            endpoint=ep,
            tokens=50.0,
            last_refill_iso="2030-01-01T00:00:00.000+00:00",
        )
        vault = _FakeVault()
        _preload(vault, pre, ep)
        now_ms = 1_714_000_000_000  # 2024 (well before 2030)
        clock = _FakeClock(values=[now_ms, now_ms + 1])
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        result = reserve(
            endpoint=ep,
            estimated_tokens=10,
            process_id="PID",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        from pipeline.loop.rate_limiter import Reserved

        assert isinstance(result, Reserved)
        written = json.loads(vault.write_calls[0]["payload"])
        # Pre=50, clamp no refill, reserve 10 → 40. No negative refill.
        assert written["buckets"][ep]["tokens"] == pytest.approx(40.0)

    def test_zero_capacity_bucket_always_insufficient(self) -> None:
        ep = "anthropic_scribe"
        pre = _mk_state(
            endpoint=ep, capacity=0, tokens=0.0, refill_rate_per_sec=100.0
        )
        vault = _FakeVault()
        _preload(vault, pre, ep)
        clock = _FakeClock(values=[1_714_000_060_000])
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        result = reserve(
            endpoint=ep,
            estimated_tokens=1,
            process_id="PID",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        from pipeline.loop.rate_limiter import InsufficientTokens

        assert isinstance(result, InsufficientTokens)
        assert result.available == pytest.approx(0.0)
        assert vault.write_calls == []

    def test_zero_refill_rate_no_recovery(self) -> None:
        """A bucket with refill_rate_per_sec=0 never refills."""
        ep = "anthropic_scribe"
        pre = _mk_state(
            endpoint=ep,
            capacity=100,
            tokens=2.0,
            refill_rate_per_sec=0.0,
            last_refill_iso="2026-04-21T12:00:00.000+00:00",
        )
        vault = _FakeVault()
        _preload(vault, pre, ep)
        anchor_ms = _iso_to_ms("2026-04-21T12:00:00+00:00")
        # +1 hour — would be huge refill if rate > 0.
        clock = _FakeClock(values=[anchor_ms + 3_600_000])
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        result = reserve(
            endpoint=ep,
            estimated_tokens=10,
            process_id="PID",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        from pipeline.loop.rate_limiter import InsufficientTokens

        assert isinstance(result, InsufficientTokens)
        assert result.available == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# E-023 residuals — trusted-operator envelope; errors bubble unwrapped
# ---------------------------------------------------------------------------


class TestResiduals:
    def test_half_present_lease_raises_valueerror(self) -> None:
        """Lease holder without expiry → RateLimiterState.__post_init__
        raises ValueError; Round 7 does not wrap."""
        ep = "anthropic_scribe"
        # Hand-craft malformed state (bypass _mk_state which goes through
        # __post_init__ and would fail).
        malformed = json.dumps(
            {
                "buckets": {
                    ep: {
                        "capacity": 100,
                        "tokens": 50.0,
                        "refill_rate_per_sec": 10.0,
                    }
                },
                "last_refill_iso": "2026-04-21T12:00:00.000+00:00",
                "lease_holder_id": "SOMEONE",
                "lease_expires_at_iso": None,  # half-present!
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

        vault = _FakeVault()
        vault.store[f"pipeline/rate_limiter/{ep}.json"] = malformed
        clock = _FakeClock(values=[1_714_000_000_000])
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        with pytest.raises(ValueError):
            reserve(
                endpoint=ep,
                estimated_tokens=5,
                process_id="PID",
                vault_read=vault.read,
                vault_write=vault.write,
                clock=clock,
                sleep=sleep,
                randint=randint,
            )

    def test_empty_buckets_raises_keyerror(self) -> None:
        ep = "anthropic_scribe"
        # State has no buckets for ``ep``.
        empty = json.dumps(
            {
                "buckets": {},
                "last_refill_iso": "2026-04-21T12:00:00.000+00:00",
                "lease_holder_id": None,
                "lease_expires_at_iso": None,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        vault = _FakeVault()
        vault.store[f"pipeline/rate_limiter/{ep}.json"] = empty
        clock = _FakeClock(values=[1_714_000_000_000])
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        with pytest.raises(KeyError):
            reserve(
                endpoint=ep,
                estimated_tokens=5,
                process_id="PID",
                vault_read=vault.read,
                vault_write=vault.write,
                clock=clock,
                sleep=sleep,
                randint=randint,
            )

    def test_malformed_vault_bytes_raises_json_decode_error(self) -> None:
        ep = "anthropic_scribe"
        vault = _FakeVault()
        vault.store[f"pipeline/rate_limiter/{ep}.json"] = b"not-json"
        clock = _FakeClock(values=[1_714_000_000_000])

        with pytest.raises(json.JSONDecodeError):
            can_reserve(
                endpoint=ep,
                estimated_tokens=1,
                vault_read=vault.read,
                clock=clock,
            )


# ---------------------------------------------------------------------------
# F_PIPE_06 taxonomy pin
# ---------------------------------------------------------------------------


class TestFailureTaxonomy:
    def test_reserve_cas_exhaust_trigger_string(self) -> None:
        ep = "anthropic_scribe"
        path = f"pipeline/rate_limiter/{ep}.json"
        vault = _FakeVault(head_mutations={path: 99})
        _preload(vault, _mk_state(endpoint=ep), ep)
        clock = _FakeClock(values=[1_714_000_000_000] * 10)
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        with pytest.raises(F_PIPE_06) as excinfo:
            reserve(
                endpoint=ep,
                estimated_tokens=5,
                process_id="PID",
                vault_read=vault.read,
                vault_write=vault.write,
                clock=clock,
                sleep=sleep,
                randint=randint,
            )

        exc = excinfo.value
        assert exc.code == "F-PIPE-06"
        assert exc.trigger == f"cas_retry_exhausted:{ep}:3"
        assert exc.details["endpoint"] == ep
        assert exc.details["process_id"] == "PID"
        assert exc.details["estimated_tokens"] == 5
        assert exc.details["max_attempts"] == 3
        assert isinstance(exc, PipelineFailure)

    def test_release_cas_exhaust_trigger_string(self) -> None:
        ep = "anthropic_scribe"
        path = f"pipeline/rate_limiter/{ep}.json"
        vault = _FakeVault(head_mutations={path: 99})
        _preload(
            vault,
            _mk_state(
                endpoint=ep,
                lease_holder_id="PID",
                lease_expires_at_iso="2030-01-01T00:00:00.000+00:00",
            ),
            ep,
        )
        clock = _FakeClock(values=[1_714_000_000_000] * 10)
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        with pytest.raises(F_PIPE_06) as excinfo:
            release(
                endpoint=ep,
                process_id="PID",
                vault_read=vault.read,
                vault_write=vault.write,
                clock=clock,
                sleep=sleep,
                randint=randint,
            )

        exc = excinfo.value
        assert exc.code == "F-PIPE-06"
        # Distinct trigger prefix from reserve to aid incident triage.
        assert exc.trigger == f"cas_retry_exhausted_release:{ep}:3"
        assert sleep.calls == [50, 200, 800]


# ---------------------------------------------------------------------------
# release idempotency
# ---------------------------------------------------------------------------


class TestReleaseIdempotency:
    def test_release_non_owner_writes_unchanged_state(self) -> None:
        ep = "anthropic_scribe"
        pre = _mk_state(
            endpoint=ep,
            lease_holder_id="OTHER",
            lease_expires_at_iso="2030-01-01T00:00:00.000+00:00",
        )
        vault = _FakeVault()
        _preload(vault, pre, ep)
        clock = _FakeClock(values=[1_714_000_000_000] * 3)
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        new_hash = release(
            endpoint=ep,
            process_id="MINE",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        assert len(new_hash) == 64
        written = json.loads(vault.write_calls[0]["payload"])
        # Lease untouched — OTHER still holds it.
        assert written["lease_holder_id"] == "OTHER"
        assert written["lease_expires_at_iso"] == (
            "2030-01-01T00:00:00.000+00:00"
        )

    def test_release_no_lease_writes_unchanged(self) -> None:
        ep = "anthropic_scribe"
        pre = _mk_state(endpoint=ep)  # No lease.
        vault = _FakeVault()
        _preload(vault, pre, ep)
        clock = _FakeClock(values=[1_714_000_000_000] * 3)
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        new_hash = release(
            endpoint=ep,
            process_id="MINE",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        assert len(new_hash) == 64
        written = json.loads(vault.write_calls[0]["payload"])
        assert written["lease_holder_id"] is None
        assert written["lease_expires_at_iso"] is None


# ---------------------------------------------------------------------------
# can_reserve purity + concurrent-reserve regression + jitter + lease stamp
# ---------------------------------------------------------------------------


class TestCanReservePurity:
    def test_can_reserve_never_writes_or_sleeps(self) -> None:
        ep = "anthropic_scribe"
        vault = _FakeVault()
        _preload(vault, _mk_state(endpoint=ep, tokens=50.0), ep)
        clock = _FakeClock(values=[1_714_000_000_000])

        # Does not take sleep/randint at all — compile-time surface test.
        ok = can_reserve(
            endpoint=ep,
            estimated_tokens=5,
            vault_read=vault.read,
            clock=clock,
        )

        assert ok is True
        assert vault.write_calls == []  # No vault mutation.
        # Exactly one read; last_refill_iso in persisted state is
        # unchanged (implicit via no write).
        assert vault.read_calls == [f"pipeline/rate_limiter/{ep}.json"]


class TestConcurrentReserveRegression:
    def test_a_v1_09_concurrent_reserve_first_wins(self) -> None:
        """Two processes race on the same endpoint; the second sees CAS
        mismatch and retries, eventually succeeding against the updated
        head hash."""
        ep = "anthropic_scribe"
        path = f"pipeline/rate_limiter/{ep}.json"
        # head_mutations=1 → first write attempt sees stale hash and is
        # rejected, second attempt re-reads the updated store and wins.
        vault = _FakeVault(head_mutations={path: 1})
        _preload(vault, _mk_state(endpoint=ep, tokens=100.0), ep)
        clock = _FakeClock(values=[1_714_000_000_000] * 6)
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        result = reserve(
            endpoint=ep,
            estimated_tokens=10,
            process_id="PID-B",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        from pipeline.loop.rate_limiter import Reserved

        assert isinstance(result, Reserved)
        # Two writes (one rejected, one accepted); one retry sleep.
        assert len(vault.write_calls) == 2
        assert sleep.calls == [50]
        # And the stored state reflects the winning payload only.
        stored = json.loads(vault.store[path])
        assert stored["lease_holder_id"] == "PID-B"


class TestJitterAndLeaseStamp:
    def test_jitter_additive_pins_sleep_value(self) -> None:
        """With randint returning 77, sleeps are (50+77, 200+77, 800+77)."""
        ep = "anthropic_scribe"
        path = f"pipeline/rate_limiter/{ep}.json"
        vault = _FakeVault(head_mutations={path: 99})
        _preload(vault, _mk_state(endpoint=ep), ep)
        clock = _FakeClock(values=[1_714_000_000_000] * 10)
        sleep = _FakeSleep()
        randint = _FakeRandInt(sequence=[77, 77, 77])

        with pytest.raises(F_PIPE_06):
            reserve(
                endpoint=ep,
                estimated_tokens=5,
                process_id="PID",
                vault_read=vault.read,
                vault_write=vault.write,
                clock=clock,
                sleep=sleep,
                randint=randint,
            )

        assert sleep.calls == [127, 277, 877]

    def test_empty_last_refill_iso_means_no_refill_anchor(self) -> None:
        """When ``last_refill_iso`` is empty, prev_ms is 0.

        ``max(now_ms - 0, 0) / 1000`` is a huge elapsed; the capacity cap
        still holds, so behaviour matches a fresh-bucket boot.
        """
        ep = "anthropic_scribe"
        payload = json.dumps(
            {
                "buckets": {
                    ep: {
                        "capacity": 50,
                        "tokens": 40.0,
                        "refill_rate_per_sec": 1.0,
                    }
                },
                "last_refill_iso": "",  # empty → 0
                "lease_holder_id": None,
                "lease_expires_at_iso": None,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        vault = _FakeVault()
        vault.store[f"pipeline/rate_limiter/{ep}.json"] = payload
        clock = _FakeClock(values=[1_714_000_000_000, 1_714_000_000_001])
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        result = reserve(
            endpoint=ep,
            estimated_tokens=5,
            process_id="PID",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        from pipeline.loop.rate_limiter import Reserved

        assert isinstance(result, Reserved)
        written = json.loads(vault.write_calls[0]["payload"])
        # Capacity cap 50 − 5 reserved = 45.
        assert written["buckets"][ep]["tokens"] == pytest.approx(45.0)

    def test_rate_limiter_default_handles_set_tuple_and_opaque(self) -> None:
        """Defensive ``_rate_limiter_default`` fallback handles unusual
        JSON-hostile inputs — dataclass, frozenset, set, tuple, and opaque."""
        from pipeline.loop.rate_limiter import _rate_limiter_default

        # frozenset → sorted list
        assert _rate_limiter_default(frozenset({3, 1, 2})) == [1, 2, 3]
        # set → sorted list
        assert _rate_limiter_default({3, 1, 2}) == [1, 2, 3]
        # tuple → list
        assert _rate_limiter_default((1, 2, 3)) == [1, 2, 3]
        # dataclass instance (non-state) → asdict
        bucket = TokenBucket(capacity=10, tokens=5.0, refill_rate_per_sec=1.0)
        assert _rate_limiter_default(bucket) == {
            "capacity": 10,
            "tokens": 5.0,
            "refill_rate_per_sec": 1.0,
        }
        # Opaque object → repr fallback.
        class _Opaque:
            def __repr__(self) -> str:
                return "<opaque>"

        assert _rate_limiter_default(_Opaque()) == {"__repr__": "<opaque>"}

    def test_lease_expires_at_iso_exact_stamp(self) -> None:
        """``lease_expires_at_iso`` is exactly ``now_ms + 30 s`` in iso."""
        ep = "anthropic_scribe"
        vault = _FakeVault()
        _preload(vault, _mk_state(endpoint=ep), ep)
        now_ms = _iso_to_ms("2026-04-21T12:00:00+00:00")
        clock = _FakeClock(values=[now_ms, now_ms + 1])
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        result = reserve(
            endpoint=ep,
            estimated_tokens=5,
            process_id="PID",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        from pipeline.loop.rate_limiter import Reserved

        assert isinstance(result, Reserved)
        expected_iso = (
            datetime.fromtimestamp(
                (now_ms + 30_000) / 1000.0, tz=timezone.utc
            ).isoformat(timespec="milliseconds")
        )
        assert result.lease_expires_at_iso == expected_iso
