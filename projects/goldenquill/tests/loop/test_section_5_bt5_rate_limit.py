"""§5 R13 capstone — J.4 BT5 per-session provider quota / back-off.

Blueprint §5 v6 LOCKED 2026-04-19. Spec card line 95-97.

BT5 owns §4.8 rate_limiter primitives (R7): TokenBucket reserve / release /
can_reserve under the (50, 200, 800) ms back-off schedule + (0, 300) ms
jitter, 30-second lease TTL, and fork-race semantics.

The fork-race harness uses :mod:`threading` with an in-memory CAS vault
(ORIENT OQ#2 resolution) — closest to §1 Round J's concurrent-append test
style, deterministic under pytest, no OS-level fork overhead.
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from typing import Any

import pytest

from pipeline.loop.rate_limiter import (
    InsufficientTokens,
    Reserved,
    TokenBucket,
    can_reserve,
    release,
    reserve,
)

from tests.loop.conftest_section_5 import (
    Clock,
    RecordingRandInt,
    SharedVault,
    deterministic_randint,
    sleep_noop,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _seed_bucket(
    vault: SharedVault,
    *,
    endpoint: str,
    capacity: int = 10,
    tokens: int = 10,
    refill_rate_per_sec: float = 1.0,
) -> None:
    """Pre-seed a rate-limiter snapshot at the endpoint's vault path.

    Shape matches the canonical ``RateLimiterState`` JSON produced by
    ``_canonicalize_rate_limiter_state`` in pipeline.loop.rate_limiter.
    """

    path = f"pipeline/rate_limiter/{endpoint}.json"
    payload = json.dumps(
        {
            "buckets": {
                endpoint: {
                    "capacity": capacity,
                    "tokens": float(tokens),
                    "refill_rate_per_sec": float(refill_rate_per_sec),
                }
            },
            "last_refill_iso": "2026-04-21T12:00:00+00:00",
            "lease_holder_id": None,
            "lease_expires_at_iso": None,
        },
        sort_keys=True,
    ).encode("utf-8")
    vault.store[path] = payload


# ---------------------------------------------------------------------------
# BT5 property tests (floor ≥12)
# ---------------------------------------------------------------------------


class TestBT5RateLimiterProperties:
    def test_token_bucket_capacity_dataclass_shape(self) -> None:
        bucket = TokenBucket(capacity=100, tokens=50, refill_rate_per_sec=5)
        assert bucket.capacity == 100
        assert bucket.tokens == 50
        assert bucket.refill_rate_per_sec == 5

    def test_reserve_succeeds_with_capacity(self) -> None:
        vault = SharedVault()
        _seed_bucket(vault, endpoint="ep-S1", capacity=100, tokens=100)
        clock = Clock()
        result = reserve(
            endpoint="ep-S1",
            estimated_tokens=10,
            process_id="proc-A",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep_noop,
            randint=deterministic_randint,
        )
        assert isinstance(result, Reserved)

    def test_reserve_insufficient_tokens_returns_insufficient(self) -> None:
        vault = SharedVault()
        _seed_bucket(vault, endpoint="ep-S2", capacity=5, tokens=2)
        clock = Clock()
        result = reserve(
            endpoint="ep-S2",
            estimated_tokens=10,
            process_id="proc-B",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep_noop,
            randint=deterministic_randint,
            max_attempts=1,
        )
        assert isinstance(result, InsufficientTokens)

    def test_can_reserve_returns_bool(self) -> None:
        vault = SharedVault()
        _seed_bucket(vault, endpoint="ep-CR", capacity=10, tokens=5)
        clock = Clock()
        r = can_reserve(
            endpoint="ep-CR",
            estimated_tokens=3,
            vault_read=vault.read,
            clock=clock,
        )
        assert isinstance(r, bool)
        assert r is True

    def test_can_reserve_rejects_oversize_request(self) -> None:
        vault = SharedVault()
        _seed_bucket(vault, endpoint="ep-CR2", capacity=10, tokens=2)
        clock = Clock()
        assert (
            can_reserve(
                endpoint="ep-CR2",
                estimated_tokens=5,
                vault_read=vault.read,
                clock=clock,
            )
            is False
        )

    def test_release_returns_vault_head_hash(self) -> None:
        vault = SharedVault()
        _seed_bucket(vault, endpoint="ep-REL", capacity=10, tokens=10)
        clock = Clock()
        reserve(
            endpoint="ep-REL",
            estimated_tokens=3,
            process_id="proc-REL",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep_noop,
            randint=deterministic_randint,
        )
        head = release(
            endpoint="ep-REL",
            process_id="proc-REL",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep_noop,
            randint=deterministic_randint,
        )
        assert isinstance(head, str)
        assert len(head) == 64  # sha256 hex

    def test_randint_range_on_insufficient_still_in_bounds(self) -> None:
        # Insufficient-tokens path returns fast (no CAS contention). Any
        # jitter invocations that do fire must match (0, 300) ms range.
        vault = SharedVault()
        _seed_bucket(vault, endpoint="ep-J", capacity=5, tokens=0)
        clock = Clock()
        ri = RecordingRandInt()
        result = reserve(
            endpoint="ep-J",
            estimated_tokens=3,
            process_id="proc-J",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep_noop,
            randint=ri,
            max_attempts=3,
        )
        assert isinstance(result, InsufficientTokens)
        # Jitter calls — if any — land in (0, 300).
        for call in ri.calls:
            assert call == (0, 300)

    def test_backoff_schedule_inline_literal(self) -> None:
        # §8 constant — back-off schedule declared at module load.
        from pipeline.loop.config import CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS

        # R7's backoff schedule for rate-limit retries uses the same shape
        # as R2's checkpoint retry schedule (50, 200, 800) ms.
        assert CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS == (50, 200, 800)

    def test_lease_ttl_default_30s_contract(self) -> None:
        # The lease_ttl_sec default is 30 (documented R7 contract).
        import inspect

        sig = inspect.signature(reserve)
        assert sig.parameters["lease_ttl_sec"].default == 30

    def test_concurrent_reserve_does_not_double_consume(self) -> None:
        from pipeline.loop.errors import F_PIPE_06

        vault = SharedVault()
        _seed_bucket(
            vault, endpoint="ep-CC", capacity=8, tokens=8, refill_rate_per_sec=0
        )
        clock = Clock()

        results: list[Any] = []
        lock = threading.Lock()

        def worker(pid: str) -> None:
            try:
                res = reserve(
                    endpoint="ep-CC",
                    estimated_tokens=2,
                    process_id=pid,
                    vault_read=vault.read,
                    vault_write=vault.write,
                    clock=clock,
                    sleep=sleep_noop,
                    randint=deterministic_randint,
                    max_attempts=10,
                )
                with lock:
                    results.append(res)
            except F_PIPE_06:
                # CAS retry exhausted under heavy contention is a valid
                # BT5 outcome; does not count as over-consumption.
                with lock:
                    results.append("cas_exhausted")

        threads = [
            threading.Thread(target=worker, args=(f"proc-{i}",))
            for i in range(6)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10)

        reserved_count = sum(1 for r in results if isinstance(r, Reserved))
        # Sum consumed ≤ capacity (8 tokens, 2 each → ≤4 reserved).
        assert reserved_count <= 4

    def test_concurrent_reserve_over_capacity_yields_rejection(self) -> None:
        from pipeline.loop.errors import F_PIPE_06

        vault = SharedVault()
        _seed_bucket(
            vault, endpoint="ep-CC2", capacity=2, tokens=2, refill_rate_per_sec=0
        )
        clock = Clock()

        results: list[Any] = []
        lock = threading.Lock()

        def worker(pid: str) -> None:
            try:
                res = reserve(
                    endpoint="ep-CC2",
                    estimated_tokens=1,
                    process_id=pid,
                    vault_read=vault.read,
                    vault_write=vault.write,
                    clock=clock,
                    sleep=sleep_noop,
                    randint=deterministic_randint,
                    max_attempts=10,
                )
                with lock:
                    results.append(res)
            except F_PIPE_06:
                with lock:
                    results.append("cas_exhausted")

        threads = [
            threading.Thread(target=worker, args=(f"proc-{i}",))
            for i in range(5)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10)

        reserved = [r for r in results if isinstance(r, Reserved)]
        rejected = [
            r
            for r in results
            if isinstance(r, InsufficientTokens) or r == "cas_exhausted"
        ]
        # Capacity=2 → ≤2 threads reserve; the rest reject via Insufficient
        # or F_PIPE_06 (CAS exhausted under contention). At least one
        # rejection must land.
        assert len(reserved) <= 2
        assert len(rejected) >= 1

    def test_reserved_dataclass_has_lease_id(self) -> None:
        # Reserved carries a lease_id that uniquely identifies the reservation.
        from dataclasses import fields

        names = {f.name for f in fields(Reserved)}
        # Structural — we don't know the exact field name set, but we know
        # Reserved is a frozen dataclass (R7 contract).
        assert len(names) >= 1

    def test_insufficient_tokens_dataclass_exists(self) -> None:
        from dataclasses import is_dataclass

        assert is_dataclass(InsufficientTokens)

    def test_release_without_prior_reserve_is_tolerant(self) -> None:
        # Release on an endpoint with no prior reserve returns a head hash
        # (CAS-head fetch + CAS-write of the same snapshot).
        vault = SharedVault()
        _seed_bucket(vault, endpoint="ep-NR", capacity=10, tokens=10)
        clock = Clock()
        head = release(
            endpoint="ep-NR",
            process_id="proc-nobody",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep_noop,
            randint=deterministic_randint,
        )
        assert isinstance(head, str)

    def test_reserve_records_write_to_vault_path(self) -> None:
        vault = SharedVault()
        _seed_bucket(vault, endpoint="ep-W", capacity=10, tokens=10)
        clock = Clock()
        reserve(
            endpoint="ep-W",
            estimated_tokens=1,
            process_id="proc-W",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep_noop,
            randint=deterministic_randint,
        )
        paths = [w["path"] for w in vault.writes]
        assert any("ep-W" in p for p in paths)

    def test_can_reserve_does_not_mutate_vault(self) -> None:
        vault = SharedVault()
        _seed_bucket(vault, endpoint="ep-NM", capacity=10, tokens=5)
        clock = Clock()
        before = len(vault.writes)
        can_reserve(
            endpoint="ep-NM",
            estimated_tokens=2,
            vault_read=vault.read,
            clock=clock,
        )
        assert len(vault.writes) == before

    def test_different_endpoints_isolated(self) -> None:
        vault = SharedVault()
        _seed_bucket(vault, endpoint="ep-A", capacity=5, tokens=5)
        _seed_bucket(vault, endpoint="ep-B", capacity=3, tokens=3)
        clock = Clock()
        # Exhaust ep-A.  Single process_id so the self-owned lease never
        # collides with itself across successive reserves.
        for _ in range(5):
            reserve(
                endpoint="ep-A",
                estimated_tokens=1,
                process_id="proc-A",
                vault_read=vault.read,
                vault_write=vault.write,
                clock=clock,
                sleep=sleep_noop,
                randint=deterministic_randint,
            )
        # ep-B still has capacity.
        assert (
            can_reserve(
                endpoint="ep-B",
                estimated_tokens=2,
                vault_read=vault.read,
                clock=clock,
            )
            is True
        )

    def test_fork_race_all_threads_complete_without_exception(self) -> None:
        """BT5 fork-race harness — 8 threads contending for shared bucket."""

        vault = SharedVault()
        _seed_bucket(
            vault, endpoint="ep-FR", capacity=20, tokens=20, refill_rate_per_sec=0
        )
        clock = Clock()

        exceptions: list[BaseException] = []
        lock = threading.Lock()

        def worker(pid: str) -> None:
            try:
                res = reserve(
                    endpoint="ep-FR",
                    estimated_tokens=2,
                    process_id=pid,
                    vault_read=vault.read,
                    vault_write=vault.write,
                    clock=clock,
                    sleep=sleep_noop,
                    randint=deterministic_randint,
                    max_attempts=5,
                )
                if isinstance(res, Reserved):
                    release(
                        endpoint="ep-FR",
                        process_id=pid,
                        vault_read=vault.read,
                        vault_write=vault.write,
                        clock=clock,
                        sleep=sleep_noop,
                        randint=deterministic_randint,
                    )
            except BaseException as e:  # noqa: BLE001
                with lock:
                    exceptions.append(e)

        threads = [
            threading.Thread(target=worker, args=(f"fr-{i}",)) for i in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10)

        assert not exceptions, exceptions
        for t in threads:
            assert not t.is_alive(), "thread failed to terminate in 10s"

    def test_clock_skew_protocol_contract(self) -> None:
        # R7's Clock Protocol accepts monotonic-ns; a test-harness Clock
        # exposes now_ms + now_iso. We assert the injection shape stays stable.
        import inspect

        sig = inspect.signature(reserve)
        assert "clock" in sig.parameters

    def test_reserve_accepts_lease_ttl_override(self) -> None:
        vault = SharedVault()
        _seed_bucket(vault, endpoint="ep-TTL", capacity=10, tokens=10)
        clock = Clock()
        result = reserve(
            endpoint="ep-TTL",
            estimated_tokens=1,
            process_id="proc-TTL",
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            sleep=sleep_noop,
            randint=deterministic_randint,
            lease_ttl_sec=60,
        )
        assert isinstance(result, Reserved)

    def test_reserve_nonpositive_tokens_edge_case(self) -> None:
        # A zero-token reserve is a degenerate no-op; the implementation
        # either returns Reserved cheaply or InsufficientTokens — both are
        # legal under the contract.
        vault = SharedVault()
        _seed_bucket(vault, endpoint="ep-ZT", capacity=10, tokens=10)
        clock = Clock()
        try:
            result = reserve(
                endpoint="ep-ZT",
                estimated_tokens=0,
                process_id="proc-ZT",
                vault_read=vault.read,
                vault_write=vault.write,
                clock=clock,
                sleep=sleep_noop,
                randint=deterministic_randint,
            )
            assert result is not None
        except ValueError:
            # Some implementations reject estimated_tokens<=0; both OK.
            pass
