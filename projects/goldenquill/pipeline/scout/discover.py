"""§4.11 DISCOVER capstone dispatcher — parallel six-channel fan-out.

Scout Round 8 capstone. Composes Rounds 1–7 primitives into the single
entry point Section 5 (Pipeline) invokes for the DISCOVER stage. The
capstone orchestrates the A/B/C/D/E/F channel family in parallel under a
bounded executor, isolates per-channel exceptions, enforces per-channel
hard timeouts, unions candidates with deterministic cross-channel dedup,
caps the run-level union surface, and assembles + signs the health tuple.

VERIFY, REVIEW, and entity research remain scope for Rounds 9–11. This
capstone's handoff is ``ScoutDiscoverResult`` — the DISCOVER union plus
the signed health tuple plus the per-run tiebreak seed that Round 9
VERIFY consumes.

Blueprint anchors:
- §4.11 Scout run orchestration — primary implementation target
- §4.10 M7 health-tuple signing (delegated via ``HealthTupleSigner``)
- §4.1–§4.6 per-channel DISCOVER entries (injected via ``ChannelDispatchMap``)
- §6 F-SCOUT-CAPSTONE-01..07 — capstone-introduced failure taxonomy
- §8 numeric pins — ``DISCOVER_POOL_MAX_WORKERS = 6`` +
  ``DISCOVER_PER_CHANNEL_HARD_TIMEOUT_S = 120``
- Architecture line 270–271 — capstone records facts; Logician decides
  the ≥4/6 hard abort downstream
- Autonomy Rule 1 — checkpoint on every completed channel + discover_complete
- A-04 — per-channel caps hold; the capstone adds ``SCOUT_UNION_CAP`` at
  the run-level union boundary as a second safety net

No module-level side effects on import: zero network, zero FD reservation,
zero nonce reservation, zero vault_read. All persistence routes through
injected ``CheckpointWriter`` / ``DegradationWriter`` / ``HealthTupleSigner``
Protocols (E-017 — seventh reuse).
"""

from __future__ import annotations

import concurrent.futures as _cf
import datetime as _dt
import hashlib
import os
import time
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    ContextManager,
    Final,
    Mapping,
    Optional,
    Protocol,
    runtime_checkable,
)

from pipeline.scout._constants import (
    CHANNEL_A,
    CHANNEL_B,
    CHANNEL_C,
    CHANNEL_D,
    CHANNEL_E,
    CHANNEL_F,
    DISCOVER_PER_CHANNEL_HARD_TIMEOUT_S,
    DISCOVER_POOL_MAX_WORKERS,
    HEALTH_FAILED,
    HEALTH_OK,
    RUN_ID_HEX_LEN,
)
from pipeline.scout._types import Candidate, SignedHealthTuple

__all__ = [
    "CapstoneDegradationEvent",
    "ChannelDiscoverCallable",
    "ChannelDiscoverResultLike",
    "CheckpointWriter",
    "ClockFn",
    "DegradationWriter",
    "EntropyFn",
    "ExecutorFactory",
    "ExecutorLike",
    "FutureLike",
    "F_SCOUT_CAPSTONE_01",
    "F_SCOUT_CAPSTONE_02",
    "F_SCOUT_CAPSTONE_03",
    "F_SCOUT_CAPSTONE_04",
    "F_SCOUT_CAPSTONE_05",
    "F_SCOUT_CAPSTONE_06",
    "F_SCOUT_CAPSTONE_07",
    "HealthTupleSigner",
    "InterruptProbe",
    "SCOUT_UNION_CAP",
    "ScoutDiscoverInterrupted",
    "ScoutDiscoverResult",
    "SessionLike",
    "SEVERITY_HIGH",
    "SEVERITY_LOW",
    "SEVERITY_MEDIUM",
    "__version__",
    "run_scout_discover",
]


# ---------------------------------------------------------------------------
# Version + capstone-introduced constants (re-verified against §8 at build)
# ---------------------------------------------------------------------------

__version__: Final[str] = "0.1.0-scout-r8"

SCOUT_UNION_CAP: Final[int] = 6000
"""Global run-level union cap — 6 channels × 1000 per-channel ceiling.

Capstone-introduced safety net layered above per-channel caps
(``CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER`` etc.). Protects VERIFY
from DISCOVER surge before Round 9's ``SCOUT_CANDIDATE_VERIFY_CAP = 1000``
takes over.
"""

_CAPSTONE_CHANNEL_ORDER: Final[tuple[str, ...]] = (
    CHANNEL_A,
    CHANNEL_B,
    CHANNEL_C,
    CHANNEL_D,
    CHANNEL_E,
    CHANNEL_F,
)

_CHANNEL_A_ENDPOINTS: Final[tuple[str, ...]] = (
    "grants.gov",
    "sam.gov",
    "usaspending.gov",
)

_RUN_TIEBREAK_SEED_LEN: Final[int] = 16

SEVERITY_LOW: Final[str] = "LOW"
SEVERITY_MEDIUM: Final[str] = "MEDIUM"
SEVERITY_HIGH: Final[str] = "HIGH"

# Capstone-introduced failure codes.
F_SCOUT_CAPSTONE_01: Final[str] = "F-SCOUT-CAPSTONE-01"  # channel timeout
F_SCOUT_CAPSTONE_02: Final[str] = "F-SCOUT-CAPSTONE-02"  # channel exception
F_SCOUT_CAPSTONE_03: Final[str] = "F-SCOUT-CAPSTONE-03"  # duplicate candidate
F_SCOUT_CAPSTONE_04: Final[str] = "F-SCOUT-CAPSTONE-04"  # union cap exceeded
F_SCOUT_CAPSTONE_05: Final[str] = "F-SCOUT-CAPSTONE-05"  # interrupt mid-fan-out
F_SCOUT_CAPSTONE_06: Final[str] = "F-SCOUT-CAPSTONE-06"  # health-signer raised
F_SCOUT_CAPSTONE_07: Final[str] = "F-SCOUT-CAPSTONE-07"  # run_id invariant


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ScoutDiscoverInterrupted(RuntimeError):
    """Raised when ``interrupt_probe()`` fires mid-fan-out (F-SCOUT-CAPSTONE-05).

    Carries the ordered tuple of channels that completed before interrupt.
    The checkpoint is written before the exception raises — Section 5's
    resume path reads the interrupted checkpoint, not this object.
    """

    def __init__(self, completed_channels: tuple[str, ...]):
        self.completed_channels = completed_channels
        super().__init__(
            f"{F_SCOUT_CAPSTONE_05}: DISCOVER interrupted after channels="
            f"{completed_channels!r}"
        )


# ---------------------------------------------------------------------------
# Injection Protocols (E-017 pattern — seventh reuse in Scout)
# ---------------------------------------------------------------------------


@runtime_checkable
class ChannelDiscoverResultLike(Protocol):
    """Minimal shape the capstone consumes from each channel's result.

    Channel A additionally exposes ``per_endpoint_state`` — the capstone
    reads that via ``getattr`` so the uniform Protocol does not have to
    model a field only one channel has.
    """

    candidates: tuple[Candidate, ...]
    channel_state: str


ChannelDiscoverCallable = Callable[[], ChannelDiscoverResultLike]
"""Zero-arg closure binding a channel's ``discover_channel_*`` entry.

Callers pre-bind per-channel dependencies (session, FD broker, nonces,
HTTP client, vault reader, roster, etc.) via ``functools.partial`` or
closures. The capstone does not inspect channel dependencies — it only
invokes the nullary dispatcher.
"""


class SessionLike(Protocol):
    """Duck-type shape the capstone needs from a sovereignty session.

    Narrower than :class:`pipeline.sovereignty.session.Session`. The full
    Section 1 Session satisfies this Protocol. Tests inject a dataclass
    with the two string fields.
    """

    session_id: str
    slug: str


class FutureLike(Protocol):
    """Minimal future surface the capstone requires.

    Returns whatever the channel's ``discover_channel_*`` returns (a
    :class:`ChannelDiscoverResultLike`). ``result(timeout=...)`` raises
    :class:`concurrent.futures.TimeoutError` on timeout; any exception
    raised inside the channel is re-raised at ``result(...)`` per stdlib
    ``Future`` semantics.
    """

    def result(self, timeout: Optional[float] = None) -> Any: ...
    def cancel(self) -> bool: ...


class ExecutorLike(Protocol):
    """Context-manager-compatible executor with ``.submit`` semantics."""

    def submit(self, fn: Callable[[], Any], /) -> FutureLike: ...
    def __enter__(self) -> "ExecutorLike": ...
    def __exit__(self, exc_type, exc, tb) -> Optional[bool]: ...


ExecutorFactory = Callable[[int], ContextManager[ExecutorLike]]
"""Factory returning an executor sized for ``max_workers`` channels.

Production default binds to
``concurrent.futures.ThreadPoolExecutor(max_workers=6)``. Tests inject
:class:`SequentialFakeExecutor` for deterministic scheduling without
thread non-determinism.
"""


class CheckpointWriter(Protocol):
    """Autonomy Rule 1 — save state always.

    Production binding wraps :func:`pipeline.sovereignty.interrupted_state.checkpoint`.
    Tests inject an in-memory recorder that captures ``(stage, payload)``
    tuples for assertion.
    """

    def write(self, *, stage: str, payload: Mapping[str, Any]) -> None: ...


class DegradationWriter(Protocol):
    """Injected sink for capstone-level degradation events.

    Production binding wraps
    :func:`pipeline.sovereignty.degradation_log.record_degradation` with
    the per-session keys and repo_root closed over. Tests inject a
    recorder that captures ``CapstoneDegradationEvent`` instances.
    """

    def record(self, event: "CapstoneDegradationEvent") -> None: ...


class HealthTupleSigner(Protocol):
    """§4.10 assemble + sign seam.

    Production factory :func:`make_default_health_signer` closes a
    :class:`pipeline.scout.health_tuple.VaultWriter` into a closure that
    calls :func:`pipeline.scout.health_tuple.assemble_and_sign_health_tuple`.
    Tests inject a deterministic signer that returns a fixed
    :class:`SignedHealthTuple`.
    """

    def __call__(
        self,
        *,
        session: SessionLike,
        per_channel_states: Mapping[str, str],
        per_channel_a_endpoints: Mapping[str, str],
        run_wall_ns: int,
        run_tiebreak_seed: bytes,
    ) -> SignedHealthTuple: ...


class InterruptProbe(Protocol):
    """Nullary predicate — True iff an interrupt has been signalled.

    Production binding wraps
    :func:`pipeline.sovereignty.interrupted_state.detect_interrupted`.
    Tests inject a toggle that flips to True between channels.
    """

    def __call__(self) -> bool: ...


EntropyFn = Callable[[int], bytes]
ClockFn = Callable[[], int]
"""Clock returning monotonic-ish wall nanoseconds.

Production default binds to :func:`time.time_ns`. Tests inject a
:class:`MockClock` that returns a fixed sequence of ns values.
"""


# ---------------------------------------------------------------------------
# CapstoneDegradationEvent
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class CapstoneDegradationEvent:
    """One-line capstone-level event for §4.10 aggregation.

    Scope: events INTRODUCED by the capstone (timeout, exception, dedup,
    union cap, interrupt). Per-channel events are emitted by the channel
    itself and carried in the channel's own result.
    """

    source: str
    code: str
    reason_tag: Optional[str]
    severity: str
    channel: Optional[str] = None


# ---------------------------------------------------------------------------
# ScoutDiscoverResult — capstone return shape
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ScoutDiscoverResult:
    """DISCOVER-stage output consumed by Round 9 (VERIFY).

    ``run_tiebreak_seed`` is the 128-bit per-run entropy embedded in the
    signed health tuple under ``run_entropy.run_tiebreak_seed_hex``.
    Round 9 VERIFY consumes the same seed to derive its secondary
    tiebreak on the ``SCOUT_CANDIDATE_VERIFY_CAP`` truncation.
    """

    candidates: tuple[Candidate, ...]
    per_channel_states: Mapping[str, str]
    per_channel_a_endpoints: Mapping[str, str]
    signed_health: SignedHealthTuple
    run_id: str
    run_tiebreak_seed: bytes
    run_wall_ns: int
    capstone_degradation_events: tuple[CapstoneDegradationEvent, ...]


# ---------------------------------------------------------------------------
# Default factories — bound to production primitives at call-site
# ---------------------------------------------------------------------------


def _default_clock() -> int:
    return time.time_ns()


def _default_entropy(n: int) -> bytes:
    return os.urandom(n)


def _default_interrupt_probe() -> bool:
    return False


class _ThreadPoolExecutorAdapter:
    """Context-manager adapter returning a real stdlib ThreadPoolExecutor.

    The adapter only exists so the default ``ExecutorFactory`` is a
    plain callable — tests can replace the factory without monkey-
    patching ``concurrent.futures``.
    """

    def __init__(self, max_workers: int) -> None:
        self._max_workers = max_workers
        self._pool: Optional[_cf.ThreadPoolExecutor] = None

    def __enter__(self) -> "_ThreadPoolExecutorAdapter":
        self._pool = _cf.ThreadPoolExecutor(max_workers=self._max_workers)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._pool is not None:
            self._pool.shutdown(wait=True, cancel_futures=True)

    def submit(self, fn: Callable[[], Any], /) -> FutureLike:
        if self._pool is None:  # pragma: no cover - context-manager guarded
            raise RuntimeError("executor used outside context-manager scope")
        return self._pool.submit(fn)


def _default_executor_factory(max_workers: int) -> ContextManager[ExecutorLike]:
    return _ThreadPoolExecutorAdapter(max_workers)


def make_default_health_signer(vault_writer: Any) -> HealthTupleSigner:
    """Production binding for :class:`HealthTupleSigner`.

    Closes ``vault_writer`` (a :class:`pipeline.scout.health_tuple.VaultWriter`)
    into a closure that delegates to
    :func:`pipeline.scout.health_tuple.assemble_and_sign_health_tuple`.

    Lazy-imports the sibling module so this module stays stdlib-adjacent
    when ``make_default_health_signer`` is never called (test harnesses).
    """
    from pipeline.scout.health_tuple import (
        assemble_and_sign_health_tuple as _sign,
    )

    def signer(
        *,
        session: SessionLike,
        per_channel_states: Mapping[str, str],
        per_channel_a_endpoints: Mapping[str, str],
        run_wall_ns: int,
        run_tiebreak_seed: bytes,
    ) -> SignedHealthTuple:
        return _sign(
            session=session,  # type: ignore[arg-type]
            per_channel=dict(per_channel_states),
            per_channel_a_endpoints=dict(per_channel_a_endpoints),
            run_wall_ns=run_wall_ns,
            run_tiebreak_seed=run_tiebreak_seed,
            vault_writer=vault_writer,
        )

    return signer


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _derive_run_id(
    *, session_id: str, run_wall_ns: int, run_tiebreak_seed: bytes
) -> str:
    """Deterministic ``run_id`` from ``(session_id, run_wall_ns, seed)``.

    Reproducible given the same three inputs; unpredictable without the
    seed. F-SCOUT-CAPSTONE-07 enforces the 24-hex-char length invariant
    (``RUN_ID_HEX_LEN``) — a violation is a programming error, not an
    operator-visible failure.
    """
    material = (
        f"{session_id}|{run_wall_ns}|".encode("utf-8") + run_tiebreak_seed
    )
    run_id = hashlib.sha3_512(material).hexdigest()[:RUN_ID_HEX_LEN]
    if len(run_id) != RUN_ID_HEX_LEN or not all(
        c in "0123456789abcdef" for c in run_id
    ):  # pragma: no cover - invariant; sha3 hex output is always valid
        raise RuntimeError(
            f"{F_SCOUT_CAPSTONE_07}: run_id derivation yielded "
            f"{run_id!r} (expected {RUN_ID_HEX_LEN} hex chars)"
        )
    return run_id


def _channel_a_endpoints_from_result(
    result: ChannelDiscoverResultLike,
) -> Mapping[str, str]:
    """Read Channel A's ``per_endpoint_state`` defensively.

    Channel A's :class:`ChannelADiscoverResult` always carries the field.
    The fall-through branch ``_all_channel_a_failed()`` exists because a
    fake returned by tests may omit it — in production the attribute is
    guaranteed by the Round 4 dataclass.
    """
    per = getattr(result, "per_endpoint_state", None)
    if per is None:  # pragma: no cover - contract-unreachable; Round 4 dataclass guarantees the attribute
        return _all_channel_a_failed()
    return dict(per)


def _all_channel_a_failed() -> Mapping[str, str]:
    return {ep: HEALTH_FAILED for ep in _CHANNEL_A_ENDPOINTS}


def _truncate_union(
    candidates: list[tuple[str, Candidate]],
) -> tuple[list[tuple[str, Candidate]], int]:
    """Deterministic truncation by ``(channel, candidate_id)`` ascending.

    Stable sort keeps the within-channel insertion order for ties; the
    channel letter provides the primary key so A-contributed candidates
    survive preferentially when the cap bites. Returns the kept pairs
    and the overflow count.
    """
    if len(candidates) <= SCOUT_UNION_CAP:
        return candidates, 0
    ordered = sorted(candidates, key=lambda p: (p[0], p[1].candidate_id))
    kept = ordered[:SCOUT_UNION_CAP]
    overflow = len(candidates) - SCOUT_UNION_CAP
    return kept, overflow


# ---------------------------------------------------------------------------
# Public entry — run_scout_discover
# ---------------------------------------------------------------------------


def run_scout_discover(
    *,
    session: SessionLike,
    channel_fns: Mapping[str, ChannelDiscoverCallable],
    health_signer: HealthTupleSigner,
    checkpoint_writer: CheckpointWriter,
    degradation_writer: DegradationWriter,
    interrupt_probe: InterruptProbe = _default_interrupt_probe,
    executor_factory: ExecutorFactory = _default_executor_factory,
    entropy: EntropyFn = _default_entropy,
    clock: ClockFn = _default_clock,
) -> ScoutDiscoverResult:
    """Execute the §4.11 DISCOVER capstone.

    Parallel fan-out across six channels under a bounded executor,
    per-channel timeout + exception isolation, cross-channel union with
    first-writer-wins dedup, run-level cap enforcement, health-tuple
    assembly + sign, interrupt-aware cancellation.

    Channel ordering for iteration is pinned to ``_CAPSTONE_CHANNEL_ORDER``;
    degradation-event emission order and checkpoint payloads are stable
    across runs regardless of future-completion order.

    :raises ScoutDiscoverInterrupted: ``interrupt_probe`` returned True
        between two channels; pending futures cancelled before raise.
    :raises KeyboardInterrupt / SystemExit: re-raised unchanged when a
        channel dispatcher raises one — never caught by ``except Exception``.
    :raises Exception: re-raised when ``health_signer`` fails (F-SCOUT-
        CAPSTONE-06) — DISCOVER has no recovery path after signing.
    """
    # -- Pre-executor run state (A-v3-01 + A-v3-10 closure) -----------------
    run_wall_ns = clock()
    seed = entropy(_RUN_TIEBREAK_SEED_LEN)
    if len(seed) != _RUN_TIEBREAK_SEED_LEN:
        raise RuntimeError(
            f"entropy fn returned {len(seed)} bytes "
            f"(expected {_RUN_TIEBREAK_SEED_LEN})"
        )
    run_id = _derive_run_id(
        session_id=session.session_id,
        run_wall_ns=run_wall_ns,
        run_tiebreak_seed=seed,
    )

    # Validate dispatch-map completeness before any work.
    missing = [c for c in _CAPSTONE_CHANNEL_ORDER if c not in channel_fns]
    if missing:
        raise KeyError(
            f"channel_fns missing keys {missing!r}; "
            f"required={list(_CAPSTONE_CHANNEL_ORDER)}"
        )

    checkpoint_writer.write(
        stage="discover_start",
        payload={
            "run_id": run_id,
            "run_wall_ns": run_wall_ns,
            "session_id": session.session_id,
            "slug": session.slug,
            "channels": list(_CAPSTONE_CHANNEL_ORDER),
        },
    )

    per_channel_states: dict[str, str] = {}
    per_channel_a_endpoints: dict[str, str] = _all_channel_a_failed()
    events: list[CapstoneDegradationEvent] = []
    union: list[tuple[str, Candidate]] = []
    seen_ids: dict[str, str] = {}  # candidate_id -> first-writer channel
    completed: list[str] = []

    # -- Parallel fan-out ---------------------------------------------------
    with executor_factory(DISCOVER_POOL_MAX_WORKERS) as pool:
        futs: dict[str, FutureLike] = {}
        for ch in _CAPSTONE_CHANNEL_ORDER:
            futs[ch] = pool.submit(channel_fns[ch])

        for ch in _CAPSTONE_CHANNEL_ORDER:
            if interrupt_probe():
                # Cancel remaining + write interrupted checkpoint.
                for remaining_ch, fut in futs.items():
                    if remaining_ch not in completed:
                        fut.cancel()
                event = CapstoneDegradationEvent(
                    source="run_scout_discover",
                    code=F_SCOUT_CAPSTONE_05,
                    reason_tag=(
                        f"interrupt signalled before channel={ch} "
                        f"after completed={tuple(completed)}"
                    ),
                    severity=SEVERITY_HIGH,
                    channel=None,
                )
                events.append(event)
                degradation_writer.record(event)
                checkpoint_writer.write(
                    stage="discover_interrupted",
                    payload={
                        "run_id": run_id,
                        "completed_channels": list(completed),
                        "pending_channel": ch,
                    },
                )
                raise ScoutDiscoverInterrupted(tuple(completed))

            fut = futs[ch]
            try:
                result = fut.result(
                    timeout=DISCOVER_PER_CHANNEL_HARD_TIMEOUT_S
                )
            except _cf.TimeoutError:
                fut.cancel()
                per_channel_states[ch] = HEALTH_FAILED
                if ch == CHANNEL_A:
                    per_channel_a_endpoints = dict(_all_channel_a_failed())
                event = CapstoneDegradationEvent(
                    source="run_scout_discover",
                    code=F_SCOUT_CAPSTONE_01,
                    reason_tag=(
                        f"channel={ch} exceeded "
                        f"{DISCOVER_PER_CHANNEL_HARD_TIMEOUT_S}s timeout"
                    ),
                    severity=SEVERITY_HIGH,
                    channel=ch,
                )
                events.append(event)
                degradation_writer.record(event)
            except (KeyboardInterrupt, SystemExit):
                # Base-exception passthrough — never caught.
                raise
            except Exception as exc:
                per_channel_states[ch] = HEALTH_FAILED
                if ch == CHANNEL_A:
                    per_channel_a_endpoints = dict(_all_channel_a_failed())
                event = CapstoneDegradationEvent(
                    source="run_scout_discover",
                    code=F_SCOUT_CAPSTONE_02,
                    reason_tag=(
                        f"channel={ch} raised "
                        f"{type(exc).__name__}: {exc}"
                    ),
                    severity=SEVERITY_HIGH,
                    channel=ch,
                )
                events.append(event)
                degradation_writer.record(event)
            else:
                per_channel_states[ch] = result.channel_state
                if ch == CHANNEL_A:
                    per_channel_a_endpoints = dict(
                        _channel_a_endpoints_from_result(result)
                    )
                for cand in result.candidates:
                    prior = seen_ids.get(cand.candidate_id)
                    if prior is None:
                        seen_ids[cand.candidate_id] = ch
                        union.append((ch, cand))
                    else:
                        event = CapstoneDegradationEvent(
                            source="run_scout_discover",
                            code=F_SCOUT_CAPSTONE_03,
                            reason_tag=(
                                f"candidate_id={cand.candidate_id} "
                                f"first_channel={prior} "
                                f"duplicate_channel={ch}"
                            ),
                            severity=SEVERITY_LOW,
                            channel=ch,
                        )
                        events.append(event)
                        degradation_writer.record(event)

            completed.append(ch)
            checkpoint_writer.write(
                stage="discover_channel_complete",
                payload={
                    "run_id": run_id,
                    "channel": ch,
                    "channel_state": per_channel_states.get(ch, HEALTH_FAILED),
                    "n_candidates_so_far": len(union),
                    "n_events_so_far": len(events),
                },
            )

    # -- Union cap (A-04 run-level safety net) ------------------------------
    truncated_pairs, overflow = _truncate_union(union)
    if overflow > 0:
        event = CapstoneDegradationEvent(
            source="run_scout_discover",
            code=F_SCOUT_CAPSTONE_04,
            reason_tag=(
                f"union size={len(union)} cap={SCOUT_UNION_CAP} "
                f"overflow={overflow}"
            ),
            severity=SEVERITY_MEDIUM,
            channel=None,
        )
        events.append(event)
        degradation_writer.record(event)

    final_candidates = tuple(cand for _ch, cand in truncated_pairs)

    checkpoint_writer.write(
        stage="discover_complete",
        payload={
            "run_id": run_id,
            "n_candidates": len(final_candidates),
            "n_events": len(events),
            "per_channel_states": dict(per_channel_states),
        },
    )

    # -- Health-tuple sign (delegated to Section 1 + §2 via Protocol) ------
    try:
        signed = health_signer(
            session=session,
            per_channel_states=per_channel_states,
            per_channel_a_endpoints=per_channel_a_endpoints,
            run_wall_ns=run_wall_ns,
            run_tiebreak_seed=seed,
        )
    except Exception as exc:
        event = CapstoneDegradationEvent(
            source="run_scout_discover",
            code=F_SCOUT_CAPSTONE_06,
            reason_tag=(
                f"health_signer raised {type(exc).__name__}: {exc}"
            ),
            severity=SEVERITY_HIGH,
            channel=None,
        )
        events.append(event)
        degradation_writer.record(event)
        raise

    return ScoutDiscoverResult(
        candidates=final_candidates,
        per_channel_states=dict(per_channel_states),
        per_channel_a_endpoints=dict(per_channel_a_endpoints),
        signed_health=signed,
        run_id=run_id,
        run_tiebreak_seed=seed,
        run_wall_ns=run_wall_ns,
        capstone_degradation_events=tuple(events),
    )
