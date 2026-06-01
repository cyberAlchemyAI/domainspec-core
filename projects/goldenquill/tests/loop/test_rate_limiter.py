"""Tests for pipeline.loop.rate_limiter — §4.8 v2 CAS-reserve + lease + refill.

Blueprint §5 v6 §4.8 LOCKED 2026-04-19.

Coverage targets (spec card ``section_05_round_7_rate_limiter.md``):
- Happy paths: single-attempt reserve success, under-budget, can_reserve,
  release.
- Lease management: B-v1-10 expired auto-release, someone-else-holds
  back-off, self re-acquire on expired lease.
- CAS retry: retry-and-win, exhaustion → F_PIPE_06, back-off schedule pin.
- Refill: wall-clock delta applied; capacity cap; last_refill_iso stamped.
- Factory / Protocol contract: RandIntFn satisfied, TokenBucket Protocol
  round-trip.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any

import pytest

from pipeline.loop.errors import F_PIPE_06, PipelineFailure
from pipeline.loop.rate_limiter import (
    InsufficientTokens,
    RandIntFn,
    Reserved,
    TokenBucket,
    can_reserve,
    release,
    reserve,
)
from pipeline.loop.types import RateLimiterState, TokenBucketProtocol
from pipeline.vault import VaultCASHeadMismatch


# ---------------------------------------------------------------------------
# Fixtures / fakes
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
    """In-process CAS-aware fake vault for rate_limiter.

    Holds a single path's bytes + head hash. ``head_mutations`` counts
    how many CAS-mismatches to raise before accepting a write; useful
    for retry-and-win scenarios.
    """

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


# ---------------------------------------------------------------------------
# Happy paths
# ---------------------------------------------------------------------------


class TestHappyPath:
    def test_reserve_first_try_succeeds(self) -> None:
        ep = "anthropic_scribe"
        vault = _FakeVault()
        _preload(vault, _mk_state(endpoint=ep), ep)
        clock = _FakeClock(values=[1_714_000_060_000, 1_714_000_060_001])
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        result = reserve(
            endpoint=ep,
            estimated_tokens=5,
            process_id="PID-A",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        assert isinstance(result, Reserved)
        assert result.endpoint == ep
        assert result.tokens == 5
        assert result.lease_holder_id == "PID-A"
        assert result.lease_expires_at_iso  # ISO string stamped
        assert len(result.committed_state_hash) == 64
        # Exactly one vault_write.
        assert len(vault.write_calls) == 1
        call = vault.write_calls[0]
        assert call["path"] == f"pipeline/rate_limiter/{ep}.json"
        assert call["intent"] == "state-success"
        assert call["write_mode"] == "overwrite"
        # expected_current_file_hash matches the pre-read hash.
        assert call["expected_current_file_hash"] == hashlib.sha256(
            _serialize(_mk_state(endpoint=ep))
        ).hexdigest()
        # No retry → no sleep.
        assert sleep.calls == []
        # randint not called on happy path (no back-off).
        assert randint.calls == []

    def test_reserve_insufficient_tokens_no_write(self) -> None:
        ep = "anthropic_scribe"
        # Bucket has 3 tokens; we request 100 — refilled by 1s × 10 = 13.
        pre = _mk_state(
            endpoint=ep, capacity=100, tokens=3.0, refill_rate_per_sec=10.0
        )
        vault = _FakeVault()
        _preload(vault, pre, ep)
        clock = _FakeClock(values=[1_714_000_001_000])  # +1 s
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        # last_refill_iso anchor is 2026-04-21T12:00:00.000+00:00 → ms
        # Our clock value is 1_714_000_001_000; the iso anchor parses to
        # epoch_ms 1_745_236_800_000. Delta is negative → clamp zero → no
        # refill. So available stays at 3.
        result = reserve(
            endpoint=ep,
            estimated_tokens=100,
            process_id="PID",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        assert isinstance(result, InsufficientTokens)
        assert result.endpoint == ep
        assert result.requested == 100
        assert result.available == 3.0
        # No vault_write on under-budget.
        assert vault.write_calls == []

    def test_can_reserve_true_when_capacity_sufficient(self) -> None:
        ep = "anthropic_scribe"
        vault = _FakeVault()
        _preload(vault, _mk_state(endpoint=ep, tokens=50.0), ep)
        clock = _FakeClock(values=[1_714_000_000_000])

        ok = can_reserve(
            endpoint=ep,
            estimated_tokens=10,
            vault_read=vault.read,
            clock=clock,
        )
        assert ok is True
        # Exactly one vault_read, zero writes.
        assert vault.read_calls == [f"pipeline/rate_limiter/{ep}.json"]
        assert vault.write_calls == []

    def test_can_reserve_false_when_under_budget(self) -> None:
        ep = "anthropic_scribe"
        vault = _FakeVault()
        _preload(vault, _mk_state(endpoint=ep, tokens=2.0), ep)
        clock = _FakeClock(values=[1_714_000_000_000])

        ok = can_reserve(
            endpoint=ep,
            estimated_tokens=10,
            vault_read=vault.read,
            clock=clock,
        )
        assert ok is False
        assert vault.write_calls == []

    def test_release_clears_lease_when_owner(self) -> None:
        ep = "anthropic_scribe"
        pre = _mk_state(
            endpoint=ep,
            lease_holder_id="PID-A",
            lease_expires_at_iso="2026-04-21T12:00:30.000+00:00",
        )
        vault = _FakeVault()
        _preload(vault, pre, ep)
        clock = _FakeClock(values=[1_714_000_000_000, 1_714_000_000_001])
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        new_hash = release(
            endpoint=ep,
            process_id="PID-A",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        assert len(new_hash) == 64
        assert len(vault.write_calls) == 1
        written = json.loads(vault.write_calls[0]["payload"])
        assert written["lease_holder_id"] is None
        assert written["lease_expires_at_iso"] is None


# ---------------------------------------------------------------------------
# Lease management
# ---------------------------------------------------------------------------


class TestLeaseManagement:
    def test_expired_lease_auto_released_no_sleep(self) -> None:
        ep = "anthropic_scribe"
        # Lease expired 5 minutes ago.
        pre = _mk_state(
            endpoint=ep,
            lease_holder_id="OTHER",
            lease_expires_at_iso="2026-04-21T11:55:00.000+00:00",
        )
        vault = _FakeVault()
        _preload(vault, pre, ep)
        # now_ms corresponds to 2026-04-21T12:00:00Z — 5 min past expiry.
        now_ms = int(
            __import__("datetime")
            .datetime.fromisoformat("2026-04-21T12:00:00+00:00")
            .timestamp()
            * 1000
        )
        clock = _FakeClock(values=[now_ms, now_ms + 1])
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        result = reserve(
            endpoint=ep,
            estimated_tokens=5,
            process_id="MINE",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        assert isinstance(result, Reserved)
        assert result.lease_holder_id == "MINE"
        # No contention-sleep occurred.
        assert sleep.calls == []

    def test_active_foreign_lease_retries_then_raises(self) -> None:
        ep = "anthropic_scribe"
        # Future-dated foreign lease.
        pre = _mk_state(
            endpoint=ep,
            lease_holder_id="OTHER",
            lease_expires_at_iso="2030-01-01T00:00:00.000+00:00",
        )
        vault = _FakeVault()
        _preload(vault, pre, ep)
        clock = _FakeClock(values=[1_714_000_000_000] * 10)
        sleep = _FakeSleep()
        randint = _FakeRandInt(sequence=[0, 0, 0])

        with pytest.raises(F_PIPE_06) as excinfo:
            reserve(
                endpoint=ep,
                estimated_tokens=5,
                process_id="MINE",
                vault_read=vault.read,
                vault_write=vault.write,
                clock=clock,
                sleep=sleep,
                randint=randint,
            )

        exc = excinfo.value
        assert exc.code == "F-PIPE-06"
        assert exc.trigger == f"cas_retry_exhausted:{ep}:3"
        # Three contention-sleeps — one per attempt.
        assert sleep.calls == [50, 200, 800]
        # No write ever landed.
        assert vault.write_calls == []

    def test_self_reacquire_on_expired_lease(self) -> None:
        ep = "anthropic_scribe"
        pre = _mk_state(
            endpoint=ep,
            lease_holder_id="MINE",
            # Expired an hour ago.
            lease_expires_at_iso="2026-04-21T11:00:00.000+00:00",
        )
        vault = _FakeVault()
        _preload(vault, pre, ep)
        now_ms = int(
            __import__("datetime")
            .datetime.fromisoformat("2026-04-21T12:00:00+00:00")
            .timestamp()
            * 1000
        )
        clock = _FakeClock(values=[now_ms, now_ms + 1])
        sleep = _FakeSleep()
        randint = _FakeRandInt()

        result = reserve(
            endpoint=ep,
            estimated_tokens=5,
            process_id="MINE",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep,
            randint=randint,
        )

        assert isinstance(result, Reserved)
        assert sleep.calls == []


# ---------------------------------------------------------------------------
# CAS retry
# ---------------------------------------------------------------------------


class TestCasRetry:
    def test_cas_mismatch_then_success(self) -> None:
        ep = "anthropic_scribe"
        path = f"pipeline/rate_limiter/{ep}.json"
        vault = _FakeVault(head_mutations={path: 1})
        _preload(vault, _mk_state(endpoint=ep), ep)
        clock = _FakeClock(values=[1_714_000_000_000] * 6)
        sleep = _FakeSleep()
        randint = _FakeRandInt(sequence=[0])

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

        assert isinstance(result, Reserved)
        # Two write attempts; one sleep at base 50.
        assert len(vault.write_calls) == 2
        assert sleep.calls == [50]
        # Two reads (one per attempt).
        assert len(vault.read_calls) == 2

    def test_cas_exhaustion_raises_f_pipe_06(self) -> None:
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
        assert isinstance(exc, PipelineFailure)
        # Three full attempts → three writes + three sleeps.
        assert len(vault.write_calls) == 3
        assert sleep.calls == [50, 200, 800]

    def test_backoff_schedule_pin_zero_jitter(self) -> None:
        """With randint always returning 0, sleeps are exactly (50, 200, 800)."""
        ep = "anthropic_scribe"
        path = f"pipeline/rate_limiter/{ep}.json"
        vault = _FakeVault(head_mutations={path: 99})
        _preload(vault, _mk_state(endpoint=ep), ep)
        clock = _FakeClock(values=[1_714_000_000_000] * 10)
        sleep = _FakeSleep()
        randint = _FakeRandInt()  # always returns 0 when sequence empty

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

        assert sleep.calls == [50, 200, 800]
        # randint called with (0, 300) — the inline-literal jitter range.
        assert randint.calls == [(0, 300)] * 3


# ---------------------------------------------------------------------------
# Refill
# ---------------------------------------------------------------------------


class TestRefill:
    def test_one_second_elapsed_refills_by_rate(self) -> None:
        ep = "anthropic_scribe"
        # Start with 5 tokens; refill_rate=10; elapsed=1s → 15 tokens.
        pre = _mk_state(
            endpoint=ep,
            capacity=100,
            tokens=5.0,
            refill_rate_per_sec=10.0,
            last_refill_iso="2026-04-21T12:00:00.000+00:00",
        )
        vault = _FakeVault()
        _preload(vault, pre, ep)
        # now_ms = last_refill + 1000 ms.
        anchor_ms = int(
            __import__("datetime")
            .datetime.fromisoformat("2026-04-21T12:00:00+00:00")
            .timestamp()
            * 1000
        )
        clock = _FakeClock(values=[anchor_ms + 1000, anchor_ms + 1001])
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

        assert isinstance(result, Reserved)
        # After reserve: 15 refilled − 10 reserved = 5.
        written = json.loads(vault.write_calls[0]["payload"])
        bucket_after = written["buckets"][ep]
        assert bucket_after["tokens"] == pytest.approx(5.0)

    def test_refill_capped_at_capacity(self) -> None:
        ep = "anthropic_scribe"
        pre = _mk_state(
            endpoint=ep,
            capacity=50,
            tokens=45.0,
            refill_rate_per_sec=100.0,
            last_refill_iso="2026-04-21T12:00:00.000+00:00",
        )
        vault = _FakeVault()
        _preload(vault, pre, ep)
        anchor_ms = int(
            __import__("datetime")
            .datetime.fromisoformat("2026-04-21T12:00:00+00:00")
            .timestamp()
            * 1000
        )
        # Huge elapsed — would overflow without capacity cap.
        clock = _FakeClock(values=[anchor_ms + 60_000, anchor_ms + 60_001])
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

        assert isinstance(result, Reserved)
        written = json.loads(vault.write_calls[0]["payload"])
        bucket_after = written["buckets"][ep]
        # capacity cap 50 − 10 reserved = 40.
        assert bucket_after["tokens"] == pytest.approx(40.0)
        # last_refill_iso stamped to now_ms.
        assert written["last_refill_iso"]


# ---------------------------------------------------------------------------
# Factory / Protocol contract
# ---------------------------------------------------------------------------


class TestFactoryAndProtocols:
    def test_randintfn_runtime_checkable(self) -> None:
        def f(a: int, b: int) -> int:
            return a

        assert isinstance(f, RandIntFn)

    def test_token_bucket_satisfies_protocol(self) -> None:
        bucket = TokenBucket(capacity=10, tokens=10.0, refill_rate_per_sec=1.0)
        assert isinstance(bucket, TokenBucketProtocol)

    def test_reserved_and_insufficient_tokens_are_distinct(self) -> None:
        # Pure shape check — different return-types, distinguishable via
        # isinstance by the caller.
        r = Reserved(
            endpoint="e",
            tokens=1,
            lease_holder_id="p",
            lease_expires_at_iso="t",
            committed_state_hash="h",
        )
        i = InsufficientTokens(endpoint="e", available=0.0, requested=1)
        assert not isinstance(r, InsufficientTokens)
        assert not isinstance(i, Reserved)
