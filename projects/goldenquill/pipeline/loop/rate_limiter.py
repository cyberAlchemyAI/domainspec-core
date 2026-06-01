"""pipeline.loop.rate_limiter — §4.8 v2 TokenBucket CAS-reserve (Round 7).

Blueprint §5 v6 LOCKED 2026-04-19:
- §4.8 v2 reserve / can_reserve / release algorithm (lines 564-618).
- §3.2.5 ``RateLimiterState`` v2 lease fields (Round 1 dataclass).
- §8 ``RATE_LIMIT_JITTER_RANGE_MS=(0, 300)``,
      ``RATE_LIMIT_LEASE_TTL_SEC=30``,
      ``CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS=(50, 200, 800)``.
- §6 F-PIPE-06 ``rate_limit_exhausted``.

**Core design decisions (confirmed at Round 7 ORIENT — 2026-04-21)**

1. *Inline-literal rebind-resistance (V1 discipline).* The back-off schedule
   ``(50, 200, 800)``, the jitter range ``(0, 300)``, the lease TTL
   ``30`` seconds, and the max-attempts ceiling ``3`` are inline literals at
   every comparison/computation site. A rebind of
   ``pipeline.loop.config.CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS`` /
   ``RATE_LIMIT_JITTER_RANGE_MS`` / ``RATE_LIMIT_LEASE_TTL_SEC`` cannot
   alter runtime behaviour. Module-load asserts here catch rebind-before-load.

2. *``CHECKPOINT_CAS_RETRY_MAX`` does not exist as a §8 constant.* Blueprint
   §4.8 line 570 references the name; Round 1 ``config.py`` deliberately does
   not define it (the back-off schedule tuple length IS the ceiling).
   Round 7 inline-literals ``max_attempts: int = 3`` as a kwarg default —
   rebind-resistant and paired with the schedule length.

3. *Path is per-endpoint.* Blueprint §4.8 line 573 reads
   ``pipeline/rate_limiter/{endpoint}.json``. Each endpoint has its own
   ``RateLimiterState`` file; the lease fields are local to that file.
   Round 7 does NOT assume a single shared state across endpoints.

4. *Vault-write intent is ``state-success`` (interim).* Blueprint §4.8 line
   603 uses ``intent="state-success"`` until a dedicated
   ``rate-limiter-snapshot`` intent lands (ARCH-07 filed against §2 v8).
   Round 7 matches: ``intent="state-success"`` + ``write_mode="overwrite"`` +
   ``expected_current_file_hash=current_hash``.

5. *Canonical bytes use ``asdict`` + ``json.dumps(sort_keys=True)``.*
   ``TokenBucket`` is a concrete mutable dataclass; ``asdict`` recurses into
   the ``buckets`` dict values and produces a stable shape. Matches the
   Round 2 / Round 6 canonicalizer template.

6. *Auto-release ordering.* Blueprint §4.8 lines 579-583 clear expired lease
   BEFORE the someone-else-holds check. Round 7 preserves this so a process
   holding an expired lease re-acquires without blocking on its own stale
   lease.

7. *Refill formula.* Standard token-bucket:
   ``tokens = min(capacity, tokens + max(elapsed_sec, 0) × refill_rate)``.
   ``last_refill_iso`` is the wall-clock anchor; re-stamped at reserve
   commit time so the next caller's delta is from this reserve moment.
   The ``max(delta, 0)`` clamp defends against non-monotonic clocks.

8. *``can_reserve`` is read-only.* No vault_write, no sleep, no randint
   calls, no ``last_refill_iso`` mutation. Performs an in-memory refill
   for the probe result only; the next real ``reserve`` does a fresh
   refill from the unchanged persisted ``last_refill_iso``.

9. *``release`` is always a CAS write.* If the caller holds the lease the
   fields clear to ``None``; otherwise the state is written unchanged.
   Idempotent — empty-lease release is a no-op that still CAS-writes to
   refresh the hash.

**Threat model (§3.11 v5 trusted-operator envelope; E-023 closure)**

Round 7 is a §5 orchestrator primitive — no network, no subprocess, no
§4 Logician consumption. The following residuals are OUT-OF-SCOPE for
v0.1 and documented by explicit ``test_adv_*`` tests rather than
defended at this layer:

- **Malformed ``vault_read`` bytes.** Non-JSON or wrong-shape payload
  raises ``json.JSONDecodeError`` / ``TypeError`` / ``ValueError`` from
  ``_deserialize_rate_limiter_state``. Round 7 does NOT wrap — the vault
  is the source of truth and the error surfaces as a programmer/data
  contract violation to the caller.

- **Endpoint not in ``state.buckets``.** Per blueprint line 592,
  ``state.buckets[endpoint]`` is a dict access. Round 7 does NOT
  pre-validate the key. ``KeyError`` propagates unwrapped.

- **Half-present lease.** ``RateLimiterState.__post_init__`` raises
  ``ValueError`` on lease_holder / lease_expires asymmetry. Round 7
  lets it bubble — it is a data-corruption signal, not an
  ``F_PIPE_06`` case.

- **Zero-capacity / zero-refill buckets.** Round 7 never synthesizes
  tokens that do not exist. A zero-capacity bucket returns
  ``InsufficientTokens`` on every reserve; a zero-refill-rate bucket
  never recovers after exhaustion. Both are configuration choices,
  not Round 7 bugs.

Spec card: ``pipeline/engineering/spec_cards/section_05_round_7_rate_limiter.md``.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timezone
from typing import Any, Final, Protocol, runtime_checkable

from pipeline.loop.config import (
    CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS,
    RATE_LIMIT_JITTER_RANGE_MS,
    RATE_LIMIT_LEASE_TTL_SEC,
)
from pipeline.loop.errors import F_PIPE_06
from pipeline.loop.run_lifecycle import VaultReadCallable
from pipeline.loop.state_checkpoint import (
    ClockProtocol,
    SleepCallable,
    VaultWriteCallable,
)
from pipeline.loop.types import RateLimiterState, TokenBucketProtocol
from pipeline.vault import VaultCASHeadMismatch

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.8 v2 reserve / can_reserve / release",
            "§3.2.5 RateLimiterState v2 lease consumption",
            "§8 RATE_LIMIT_JITTER_RANGE_MS / RATE_LIMIT_LEASE_TTL_SEC pins",
            "§8 CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS mirror",
            "§6 F-PIPE-06 rate_limit_exhausted",
        ],
    },
}

# ---------------------------------------------------------------------------
# Inline-literal module-load integrity asserts (V1 discipline)
# ---------------------------------------------------------------------------

assert CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS == (50, 200, 800), (
    "pipeline.loop.config.CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS has been rebound "
    "before pipeline.loop.rate_limiter import; refusing to load"
)
assert RATE_LIMIT_JITTER_RANGE_MS == (0, 300), (
    "pipeline.loop.config.RATE_LIMIT_JITTER_RANGE_MS has been rebound "
    "before pipeline.loop.rate_limiter import; refusing to load"
)
assert RATE_LIMIT_LEASE_TTL_SEC == 30, (
    "pipeline.loop.config.RATE_LIMIT_LEASE_TTL_SEC has been rebound "
    "before pipeline.loop.rate_limiter import; refusing to load"
)


# ---------------------------------------------------------------------------
# Public Protocols (E-017 injected-callable pattern — eighth firing)
# ---------------------------------------------------------------------------


@runtime_checkable
class RandIntFn(Protocol):
    """Injected random-integer source — seam for deterministic jitter tests.

    Mirrors ``random.randint(a, b)`` — returns an int in the inclusive
    interval ``[a, b]``. Round 7 injects this rather than calling the
    stdlib directly so tests can pin jitter to zero (or to a specific
    sequence) without ``monkeypatch.setattr(random, ...)``.
    """

    def __call__(self, a: int, b: int) -> int: ...


# ---------------------------------------------------------------------------
# Public result dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class Reserved:
    """Successful reservation outcome from :func:`reserve`.

    ``committed_state_hash`` is the SHA-256 hex digest returned by the
    vault on the winning write — callers that plan a subsequent
    ``release`` may use it as a CAS pin.
    """

    endpoint: str
    tokens: int
    lease_holder_id: str
    lease_expires_at_iso: str
    committed_state_hash: str


@dataclass(frozen=True, kw_only=True, slots=True)
class InsufficientTokens:
    """Under-budget outcome from :func:`reserve` — NOT a failure.

    ``available`` is the refilled (post-refill) token count at the moment
    the under-budget check fired. ``requested`` is the caller's estimate.
    No vault_write occurred.
    """

    endpoint: str
    available: float
    requested: int


# ---------------------------------------------------------------------------
# Concrete TokenBucket — satisfies TokenBucketProtocol
# ---------------------------------------------------------------------------


@dataclass(kw_only=True, slots=True)
class TokenBucket:
    """§4.8 concrete token bucket — satisfies :class:`TokenBucketProtocol`.

    Mutable by design — ``reserve`` decrements ``tokens`` in-memory before
    CAS-writing the full ``RateLimiterState`` back to the vault. The
    authoritative bucket state is on disk; this class is the in-memory
    projection for one CAS attempt.
    """

    capacity: int
    tokens: float
    refill_rate_per_sec: float


# ---------------------------------------------------------------------------
# Path convention (blueprint §4.8 line 573)
# ---------------------------------------------------------------------------


def _path_for(endpoint: str) -> str:
    """Per-endpoint vault path — matches blueprint §4.8 line 573.

    ``pipeline/rate_limiter/{endpoint}.json``. Each endpoint has its own
    ``RateLimiterState`` file; the lease fields are local to that file.
    """
    return f"pipeline/rate_limiter/{endpoint}.json"


# ---------------------------------------------------------------------------
# ISO / epoch helpers
# ---------------------------------------------------------------------------


def _ms_to_iso(ms: int) -> str:
    """Convert epoch milliseconds → ISO-8601 UTC with millisecond precision.

    Form: ``2026-04-21T12:00:00.000+00:00``. ``datetime.fromisoformat`` on
    Python 3.11+ parses this back round-trip.
    """
    dt = datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc)
    return dt.isoformat(timespec="milliseconds")


def _iso_to_ms(iso: str) -> int:
    """Parse an ISO-8601 string to epoch milliseconds.

    Accepts both ``+00:00`` and ``Z`` suffixes (the ``Z`` variant via an
    explicit substitution). Empty string → 0 (treated as "no prior refill
    anchor" by the refill helper).
    """
    if not iso:
        return 0
    # datetime.fromisoformat in Python 3.11 handles "+00:00"; the "Z"
    # shorthand is accepted in 3.11+ but normalise for safety.
    normalised = iso.replace("Z", "+00:00") if iso.endswith("Z") else iso
    dt = datetime.fromisoformat(normalised)
    return int(dt.timestamp() * 1000)


def _is_past(iso: str, now_ms: int) -> bool:
    """Return True iff ``iso`` is strictly before ``now_ms`` (expired)."""
    return _iso_to_ms(iso) < now_ms


# ---------------------------------------------------------------------------
# Refill
# ---------------------------------------------------------------------------


def _refill_bucket(bucket: TokenBucket, elapsed_sec: float) -> None:
    """In-place refill per §4.8 line 590.

    ``tokens = min(capacity, tokens + max(elapsed_sec, 0) × refill_rate)``.
    ``elapsed_sec`` can be ``0.0`` (first call with empty ``last_refill_iso``)
    — then refill is a no-op. Non-monotonic clock delta is clamped at zero.
    """
    delta = max(elapsed_sec, 0.0) * bucket.refill_rate_per_sec
    bucket.tokens = min(float(bucket.capacity), bucket.tokens + delta)


def _apply_refill(state: RateLimiterState, now_ms: int) -> None:
    """Refill every bucket in the state against ``now_ms``.

    Does NOT mutate ``state.last_refill_iso`` — the caller stamps it at
    reserve commit time. Read-only probes (``can_reserve``) call this for
    the in-memory projection without writing back.
    """
    prev_ms = _iso_to_ms(state.last_refill_iso)
    elapsed_sec = max(now_ms - prev_ms, 0) / 1000.0
    for bucket in state.buckets.values():
        if isinstance(bucket, TokenBucket):
            _refill_bucket(bucket, elapsed_sec)


# ---------------------------------------------------------------------------
# Canonicalization + deserialization
# ---------------------------------------------------------------------------


def _rate_limiter_default(obj: Any) -> Any:
    """``json.dumps`` default handler — mirrors Round 2 shape."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    if isinstance(obj, (frozenset, set)):
        return sorted(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return {"__repr__": repr(obj)}


def _canonicalize_rate_limiter_state(state: RateLimiterState) -> bytes:
    """Deterministic bytes for a :class:`RateLimiterState`."""
    payload = asdict(state)
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        default=_rate_limiter_default,
    ).encode("utf-8")


def _deserialize_rate_limiter_state(raw: bytes) -> RateLimiterState:
    """Reverse of :func:`_canonicalize_rate_limiter_state`.

    Reconstructs :class:`TokenBucket` instances from serialized dict form
    for each entry in ``buckets``. Non-bucket fields pass through
    :class:`RateLimiterState.__post_init__` validation (half-present
    lease detection).
    """
    payload = json.loads(raw.decode("utf-8"))
    buckets_raw = payload.get("buckets", {})
    buckets: dict[str, TokenBucketProtocol] = {}
    for key, bucket_payload in buckets_raw.items():
        buckets[key] = TokenBucket(
            capacity=int(bucket_payload["capacity"]),
            tokens=float(bucket_payload["tokens"]),
            refill_rate_per_sec=float(
                bucket_payload["refill_rate_per_sec"]
            ),
        )
    return RateLimiterState(
        buckets=buckets,
        last_refill_iso=payload.get("last_refill_iso", ""),
        lease_holder_id=payload.get("lease_holder_id"),
        lease_expires_at_iso=payload.get("lease_expires_at_iso"),
    )


# ---------------------------------------------------------------------------
# Back-off + jitter
# ---------------------------------------------------------------------------


def _backoff_with_jitter_ms(attempt: int, randint: RandIntFn) -> int:
    """§4.8 lines 615-618 — inline-literal back-off schedule + jitter.

    ``attempt`` is 0-indexed; the schedule saturates at the last slot
    (mirrors the ``min(attempt, 2)`` idiom in the blueprint). The
    ``(50, 200, 800)`` tuple and the ``(0, 300)`` jitter range are both
    inline literals — rebinding the config-module attribute is a no-op.
    """
    base_ms = (50, 200, 800)[min(attempt, 2)]
    jitter_ms = randint(0, 300)
    return base_ms + jitter_ms


# ---------------------------------------------------------------------------
# Public API — reserve
# ---------------------------------------------------------------------------


def reserve(
    *,
    endpoint: str,
    estimated_tokens: int,
    process_id: str,
    vault_read: VaultReadCallable,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
    randint: RandIntFn,
    max_attempts: int = 3,
    lease_ttl_sec: int = 30,
) -> Reserved | InsufficientTokens:
    """§4.8 v2 reserve — vault-CAS-lock-protected token reservation.

    Per-endpoint file at ``pipeline/rate_limiter/{endpoint}.json``.
    Reads bytes + hash, auto-releases expired lease, sleeps if someone
    else holds an active lease, refills the bucket, checks capacity,
    decrements on reserve, re-stamps the lease, CAS-writes the new
    canonical bytes.

    Returns :class:`Reserved` on success, :class:`InsufficientTokens`
    when the refilled bucket can't cover ``estimated_tokens``. Raises
    :class:`F_PIPE_06` on CAS / lease-contention exhaustion
    (``max_attempts`` retries consumed).

    Parameters
    ----------
    endpoint
        Per-endpoint key — becomes both the path segment and the
        ``state.buckets`` dict key.
    estimated_tokens
        Caller's token budget for the upcoming LLM / API call.
    process_id
        Lease holder identifier stamped into ``RateLimiterState`` on
        reserve. The same ``process_id`` can re-acquire an expired lease
        without blocking.
    vault_read, vault_write, clock, sleep, randint
        Injected Protocols (see module-level docs).
    max_attempts
        CAS + lease-contention retry ceiling. Inline-literal default
        ``3`` (rebind-resistant; paired with the back-off schedule
        length).
    lease_ttl_sec
        Lease time-to-live from the reserve instant. Inline-literal
        default ``30`` (§8 ``RATE_LIMIT_LEASE_TTL_SEC`` pin).

    Raises
    ------
    F_PIPE_06
        ``max_attempts`` consumed without a successful CAS-write. The
        trigger string is
        ``cas_retry_exhausted:{endpoint}:{max_attempts}``.
    KeyError
        ``endpoint`` not present in ``state.buckets`` after read.
        Programmer/data contract violation — not wrapped.
    ValueError
        ``RateLimiterState.__post_init__`` surfaced a half-present
        lease. Data corruption signal — not wrapped.
    """
    path = _path_for(endpoint)

    for attempt in range(max_attempts):
        raw = vault_read(path=path)
        current_hash = hashlib.sha256(raw).hexdigest()
        state = _deserialize_rate_limiter_state(raw)

        now_ms = clock.now_ms()

        # Auto-release expired lease (B-v1-10) BEFORE the someone-else
        # check so a process holding its own expired lease re-acquires
        # without blocking on a stale self-lease.
        if (
            state.lease_holder_id is not None
            and state.lease_expires_at_iso is not None
            and _is_past(state.lease_expires_at_iso, now_ms)
        ):
            state.lease_holder_id = None
            state.lease_expires_at_iso = None

        # Someone-else-holds active lease — sleep + retry.
        if (
            state.lease_holder_id is not None
            and state.lease_holder_id != process_id
        ):
            sleep(_backoff_with_jitter_ms(attempt, randint))
            continue

        # Refill against wall-clock delta.
        _apply_refill(state, now_ms)

        bucket = state.buckets[endpoint]  # KeyError propagates.

        # Under-budget — no mutation, no vault_write.
        if bucket.tokens < float(estimated_tokens):
            return InsufficientTokens(
                endpoint=endpoint,
                available=float(bucket.tokens),
                requested=estimated_tokens,
            )

        # Reserve + stamp lease + stamp last_refill.
        bucket.tokens -= float(estimated_tokens)
        # lease_ttl_sec is an inline-literal kwarg default (30); a
        # rebind of pipeline.loop.config.RATE_LIMIT_LEASE_TTL_SEC does
        # not affect this computation.
        expires_ms = now_ms + lease_ttl_sec * 1000
        lease_expires_at_iso = _ms_to_iso(expires_ms)
        state.lease_holder_id = process_id
        state.lease_expires_at_iso = lease_expires_at_iso
        state.last_refill_iso = _ms_to_iso(now_ms)

        payload = _canonicalize_rate_limiter_state(state)
        try:
            committed_hash = vault_write(
                path=path,
                payload=payload,
                intent="state-success",
                write_mode="overwrite",
                expected_current_file_hash=current_hash,
            )
        except VaultCASHeadMismatch:
            sleep(_backoff_with_jitter_ms(attempt, randint))
            continue

        return Reserved(
            endpoint=endpoint,
            tokens=estimated_tokens,
            lease_holder_id=process_id,
            lease_expires_at_iso=lease_expires_at_iso,
            committed_state_hash=committed_hash,
        )

    raise F_PIPE_06(
        trigger=f"cas_retry_exhausted:{endpoint}:{max_attempts}",
        details={
            "endpoint": endpoint,
            "process_id": process_id,
            "estimated_tokens": estimated_tokens,
            "max_attempts": max_attempts,
        },
    )


# ---------------------------------------------------------------------------
# Public API — can_reserve
# ---------------------------------------------------------------------------


def can_reserve(
    *,
    endpoint: str,
    estimated_tokens: int,
    vault_read: VaultReadCallable,
    clock: ClockProtocol,
) -> bool:
    """§4.8 v2 read-only probe — "is capacity ≥ estimated_tokens?".

    Reads the current state + performs an in-memory refill against
    ``clock.now_ms()``. Returns True iff the refilled bucket can cover
    ``estimated_tokens``. Does NOT mutate vault state, does NOT sleep,
    does NOT call ``randint``, does NOT check the lease holder.

    Used by §4.9 cascade-selection (Round 8+) to pick the first level
    whose endpoint has capacity without committing to a reserve.

    Raises
    ------
    KeyError
        ``endpoint`` not present in ``state.buckets``.
    ValueError
        Half-present lease in the persisted state.
    """
    raw = vault_read(path=_path_for(endpoint))
    state = _deserialize_rate_limiter_state(raw)
    _apply_refill(state, clock.now_ms())
    bucket = state.buckets[endpoint]
    return bucket.tokens >= float(estimated_tokens)


# ---------------------------------------------------------------------------
# Public API — release
# ---------------------------------------------------------------------------


def release(
    *,
    endpoint: str,
    process_id: str,
    vault_read: VaultReadCallable,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
    randint: RandIntFn,
    max_attempts: int = 3,
) -> str:
    """Explicit lease close — CAS-writes lease fields back to ``None``.

    Idempotent: if no lease is held, or if the lease is held by another
    process, the state is CAS-written unchanged (returns the refreshed
    hash). If ``process_id`` matches ``state.lease_holder_id``, the
    lease fields clear to ``None`` and the new bytes CAS-write.

    Per §4.8 the lease also auto-releases on the next :func:`reserve`
    call whose ``clock.now_ms()`` is past ``lease_expires_at_iso``;
    ``release`` is the best-effort explicit close primitive.

    Returns the committed state hash. Raises :class:`F_PIPE_06` on CAS
    exhaustion.
    """
    path = _path_for(endpoint)

    for attempt in range(max_attempts):
        raw = vault_read(path=path)
        current_hash = hashlib.sha256(raw).hexdigest()
        state = _deserialize_rate_limiter_state(raw)

        if state.lease_holder_id == process_id:
            state.lease_holder_id = None
            state.lease_expires_at_iso = None
        # else: non-owner or no lease — CAS-write unchanged to confirm
        # the caller's view is current.

        # Touch clock so the (optional) caller that cares about
        # release-time auditing has a stable reading; no state mutation
        # when the lease is foreign.
        _ = clock.now_ms()

        payload = _canonicalize_rate_limiter_state(state)
        try:
            committed_hash = vault_write(
                path=path,
                payload=payload,
                intent="state-success",
                write_mode="overwrite",
                expected_current_file_hash=current_hash,
            )
        except VaultCASHeadMismatch:
            sleep(_backoff_with_jitter_ms(attempt, randint))
            continue

        return committed_hash

    raise F_PIPE_06(
        trigger=f"cas_retry_exhausted_release:{endpoint}:{max_attempts}",
        details={
            "endpoint": endpoint,
            "process_id": process_id,
            "max_attempts": max_attempts,
        },
    )


__all__ = [
    "BLUEPRINT_DEPS",
    "InsufficientTokens",
    "RandIntFn",
    "Reserved",
    "TokenBucket",
    "can_reserve",
    "release",
    "reserve",
]
