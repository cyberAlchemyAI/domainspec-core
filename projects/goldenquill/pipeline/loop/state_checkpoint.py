"""pipeline.loop.state_checkpoint — §4.13 atomic CAS envelope (Round 2).

Blueprint §5 v6 LOCKED 2026-04-19:
- §4.1 step 2 ``checkpoint_atomic`` call-site
- §4.13 atomic CAS-swap + quarantine marker + read-retry + total-timeout
- §3.2.1 ``quarantine_marker_ref`` field population
- §6 F-PIPE-01 CRIT
- §8 ``CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS=(50, 200, 800)`` +
      ``CHECKPOINT_TOTAL_TIMEOUT_SEC=10``

**Core design decisions (reaffirmed at Round 2 build time)**

1. *Back-off and total-timeout use INLINE LITERALS.* V1 discipline — a
   module-attribute rebinding of ``pipeline.loop.config`` constants cannot
   alter runtime behaviour because the comparison/schedule uses a fresh
   literal at each site.

2. *Quarantine marker writes BEFORE* ``F_PIPE_01`` *is raised* (A-v1-01
   closure, §4.13 lines 819-823). ``RunState.quarantine_marker_ref`` +
   ``RunState.phase = "quarantined"`` mutate first.

3. *Vault I/O is injected.* Every call goes through ``VaultWriteCallable``;
   every timestamp through ``ClockProtocol``; every sleep through
   ``SleepCallable``. Tests drive the full CAS loop with zero real I/O.
   Exception contract: the callable raises ``VaultCASHeadMismatch`` on CAS
   mismatch (retry) and any other ``VaultError`` on terminal failure
   (state-failure wrapper → re-raise original). Matches §4.13 pseudo-code
   two-branch ``except`` structure.

4. *Terminal non-CAS vault errors DO NOT reach the quarantine path.*
   Blueprint §4.13 lines 813-817: ``VaultWriteUnauthorizedIntent``
   (now: ``VaultError`` subclass other than ``VaultCASHeadMismatch``) writes
   a ``state-failure`` checkpoint then RE-RAISES THE ORIGINAL VAULT ERROR
   — no ``F_PIPE_01`` synthesis. Quarantine marker is reserved for CAS
   exhaustion and total-timeout (§4.13 lines 819-823).

5. *``_assert_runstate_schema_current`` is pure.* The state-failure
   checkpoint on schema downgrade is the caller's responsibility (Round 3
   ``resume_run``). This Round ships the predicate only.

**Threat model (§3.11 v5 trusted-operator envelope; E-023 closure)**

Round 2 is an internal primitive consumed only by trusted Round 3+ code
that constructs the injected Protocols (``VaultWriteCallable``,
``ClockProtocol``, ``SleepCallable``) and supplies the ``run_state``.
The following residuals are OUT-OF-SCOPE for v0.1 and documented by
explicit ``test_adv_*`` tests rather than defended at this layer:

- **Malformed ``vault_write`` return.** Round 2 trusts the callable's
  return shape. §2 Vault's concrete ``vault_write`` (LOCKed Round P)
  returns a SHA-256 hex string; a rogue Protocol could return anything.
  ``committed_hash`` is returned in ``CheckpointResult`` unchanged and
  is NOT used as a future CAS pin inside Round 2 (caller owns refresh).

- **``_canonicalize_runstate._default`` repr fallback.** Two non-dataclass
  objects with identical ``repr`` produce identical canonical bytes.
  This is a correctness floor, not a cryptographic guarantee. The only
  live field subject to the fallback is
  ``RateLimiterState.buckets`` (``dict[str, TokenBucketProtocol]``);
  Round 7 will ship a concrete ``TokenBucket`` dataclass, closing the
  residual for production RunStates.

- **``run_id`` path-segment interpolation.** ``pipeline/{run_id}/…`` is
  string-interpolated. Source sanitization is Round 3's
  ``RunIdFactory`` (ULID charset) AND §2 Vault's path validator
  (``vault_write`` LOCKed to reject ``..`` segments). Round 2 trusts
  both upstream guards.

Spec card: pre-staged 2026-04-20 during §5 Round 1 LOCK; v1 in this commit.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Final, Protocol, runtime_checkable

from pipeline.loop.config import (
    CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS,
    CHECKPOINT_TOTAL_TIMEOUT_SEC,
    RUNSTATE_SCHEMA_VERSION,
)
from pipeline.loop.errors import F_PIPE_01, F_PIPE_22
from pipeline.loop.types import RunState
from pipeline.vault import VaultCASHeadMismatch, VaultError

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.1 step 2 checkpoint_atomic entry",
            "§4.13 atomic CAS + quarantine + back-off + total-timeout",
            "§3.2.1 quarantine_marker_ref mutation",
        ],
    },
    "section_05_v6_amendment.md": {
        "version": "LOCK-READY",
        "hash_sha3_512_prefix16": "52ae6b3b97b159b5",
        "sections_implemented": [
            "pointer-only: no amendment-owned behaviour in this round",
        ],
    },
}


# ---------------------------------------------------------------------------
# Inline-literal module-load integrity asserts
# ---------------------------------------------------------------------------
# Mirror the pattern in ``pipeline.loop.config``: at import time, verify that
# the imported constants match the inline-literal values baked into this
# module. A rebind of the config module attribute AFTER this module loads
# cannot subvert checkpoint_atomic's runtime checks because every such check
# uses a fresh literal RHS. But we also catch the case where someone
# rebinds-before-load here, just as the config module does.

assert CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS == (50, 200, 800), (
    "pipeline.loop.config.CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS has been rebound "
    "before pipeline.loop.state_checkpoint import; refusing to load"
)
assert CHECKPOINT_TOTAL_TIMEOUT_SEC == 10, (
    "pipeline.loop.config.CHECKPOINT_TOTAL_TIMEOUT_SEC has been rebound "
    "before pipeline.loop.state_checkpoint import; refusing to load"
)
assert RUNSTATE_SCHEMA_VERSION == 2, (
    "pipeline.loop.config.RUNSTATE_SCHEMA_VERSION has been rebound "
    "before pipeline.loop.state_checkpoint import; refusing to load"
)


# ---------------------------------------------------------------------------
# Public Protocols (E-017 injected-callable pattern)
# ---------------------------------------------------------------------------


@runtime_checkable
class ClockProtocol(Protocol):
    """Injected clock — deterministic monotonic and ISO timestamps.

    ``now_ms`` is a monotonic millisecond counter; total-timeout is checked
    against the delta between two calls. ``now_iso`` is the wall-clock ISO
    string stamped on ``RunState.last_checkpoint_iso`` and the
    ``CheckpointResult.written_at_iso`` field.
    """

    def now_ms(self) -> int: ...
    def now_iso(self) -> str: ...


@runtime_checkable
class SleepCallable(Protocol):
    """Injected sleep — milliseconds.

    Used between CAS retries. Tests inject a fake that records the sequence
    of sleep durations rather than blocking on wall-clock time.
    """

    def __call__(self, ms: int) -> None: ...


@runtime_checkable
class VaultWriteCallable(Protocol):
    """Injected vault-write — mirrors Section 2 v7 ``vault_write`` signature.

    Contract:

    - On success, returns the committed-bytes SHA-256 hex digest string.
    - On CAS head mismatch, raises ``VaultCASHeadMismatch`` (retry).
    - On any other terminal vault error, raises a ``VaultError`` subclass.
      ``checkpoint_atomic`` writes a ``state-failure`` checkpoint via the
      same callable (best-effort, swallows secondary errors) and re-raises
      the ORIGINAL exception.

    Parameters mirror Section 2 v7 vault_write:

    - ``path``: vault-relative path (e.g. ``pipeline/{run_id}/state.json``).
    - ``payload``: canonical bytes to commit.
    - ``intent``: ``state-success`` / ``state-failure`` / ``state-quarantine``
      (Cedar-allowlisted).
    - ``write_mode``: ``write-if-absent`` or ``overwrite``.
    - ``expected_current_file_hash``: CAS head pin; ``None`` for new files.
    """

    def __call__(
        self,
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str: ...


# ---------------------------------------------------------------------------
# Public result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class CheckpointResult:
    """Returned on successful ``checkpoint_atomic`` commit.

    Never returned on failure — failure paths raise ``F_PIPE_01``,
    ``F_PIPE_22``, or re-raise an original ``VaultError``.
    """

    written_at_iso: str
    committed_hash: str
    attempt_count: int
    elapsed_ms: int
    quarantine_marker_ref: str | None


# ---------------------------------------------------------------------------
# Internal canonicalization
# ---------------------------------------------------------------------------


def _canonicalize_runstate(rs: RunState) -> bytes:
    """Deterministic canonical-bytes for a RunState.

    Round 2 uses a stable ``json.dumps(sort_keys=True)`` over
    ``dataclasses.asdict(rs)`` with a conservative ``default=`` handler for
    non-JSON-native fields (TokenBucketProtocol instances inside
    RateLimiterState.buckets). Two structurally-equal RunStates produce
    byte-identical output; any structural change flips the CAS head.

    This implementation is intentionally minimal — it is the Round 2
    hashable-shape primitive. Round 7 (rate_limiter) may tighten the
    TokenBucketProtocol serialization when concrete bucket classes land.
    """

    def _default(obj: Any) -> Any:
        # Dataclasses (e.g. TokenBucket instances once Round 7 lands) fall
        # through to asdict.
        if is_dataclass(obj) and not isinstance(obj, type):
            return asdict(obj)
        # frozenset → sorted list (json can't serialize either directly).
        if isinstance(obj, (frozenset, set)):
            return sorted(obj)
        # Protocol instances without a dataclass shape: fall back to a
        # stable repr so two equal-by-repr instances produce equal bytes.
        # This is a correctness floor, not a cryptographic guarantee.
        return {"__repr__": repr(obj)}

    payload = asdict(rs)
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), default=_default
    ).encode("utf-8")


# ---------------------------------------------------------------------------
# Quarantine marker + state-failure wrapper
# ---------------------------------------------------------------------------


def _write_quarantine_marker(
    run_state: RunState,
    reason: str,
    *,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
) -> str:
    """§4.13 A-v1-01 helper — write vault/pipeline/{run_id}/quarantine.json.

    Uses ``intent="state-success"`` + ``write_mode="overwrite"`` per blueprint
    §4.13 line 828 prose ("the operator's recovery hook"). Returns the
    vault-relative path as the marker reference stored on
    ``run_state.quarantine_marker_ref``.

    If the vault_write itself fails here, the caller is already on the
    exhaustion path — we propagate the secondary error because the operator
    MUST know the vault is wedged; swallowing it would be worse than a
    loud abort.
    """
    marker = {
        "run_id": run_state.run_id,
        "org_slug": run_state.org_slug,
        "last_known_good_phase": run_state.phase,
        "schema_version": run_state.schema_version,
        "reason": reason,
        "written_at_iso": clock.now_iso(),
    }
    payload = json.dumps(marker, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    path = f"pipeline/{run_state.run_id}/quarantine.json"
    vault_write(
        path=path,
        payload=payload,
        intent="state-success",
        write_mode="overwrite",
        expected_current_file_hash=None,
    )
    return path


def _write_state_failure_wrapper(
    run_state: RunState,
    error: BaseException,
    *,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
) -> None:
    """§4.13 A-v1-08 helper — best-effort state-failure checkpoint.

    Writes ``pipeline/{run_id}/state_failure.json`` via
    ``intent="state-failure"``. Secondary failures inside this wrapper are
    SWALLOWED — the original error always wins. (If the vault is so wedged
    that even the failure checkpoint won't land, the caller is about to
    re-raise the primary error; do not mask it.)
    """
    err_code = getattr(error, "code", None) or type(error).__name__
    marker = {
        "run_id": run_state.run_id,
        "org_slug": run_state.org_slug,
        "phase_at_failure": run_state.phase,
        "error_code": err_code,
        "error_repr": repr(error),
        "written_at_iso": clock.now_iso(),
    }
    payload = json.dumps(marker, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    path = f"pipeline/{run_state.run_id}/state_failure.json"
    try:
        vault_write(
            path=path,
            payload=payload,
            intent="state-failure",
            write_mode="overwrite",
            expected_current_file_hash=None,
        )
    except Exception:
        # Best-effort — do not mask the primary failure.
        return


# ---------------------------------------------------------------------------
# Resume-entry schema predicate
# ---------------------------------------------------------------------------


def _assert_runstate_schema_current(rs: RunState) -> None:
    """§4.1 step 1 (v5 MA-07 / MB-05) — resume-time schema enforcement.

    Called at the top of ``resume_run`` BEFORE any phase-set membership
    check. A schema downgrade means the ``phase`` field itself may have
    been renamed or removed; validating phase against a distrusted schema
    is unsafe.

    Both comparisons use INLINE-LITERAL RHS (V1 discipline). Rebinding
    ``pipeline.loop.config.RUNSTATE_SCHEMA_VERSION`` in-memory does not
    alter this predicate's behaviour. The imported symbol is used only for
    the module-load sanity assert above.

    The predicate is pure — on raise, the caller (``resume_run``) is
    responsible for writing the ``state-failure`` checkpoint before
    re-raising. Round 2 does not wrap this call.
    """
    # Inline-literal 2 — rebind-resistant.
    if rs.schema_version != 2:
        raise F_PIPE_22(
            trigger="runstate_schema_downgrade",
            details={
                "observed": rs.schema_version,
                "expected": 2,
                "run_id": rs.run_id,
            },
        )
    # Explicit legacy-rejection branch (blueprint §4.1 step 1 line 426-431).
    # Unreachable today — the `!= 2` branch above catches schema_version == 1
    # first. Encoded separately so that a future schema_version == 3 bump
    # has a clear place to list legacy rejections; the explicit frozenset
    # is the blueprint-mandated shape.
    if rs.schema_version in frozenset({1}):  # pragma: no cover
        raise F_PIPE_22(
            trigger="runstate_schema_downgrade",
            details={
                "observed": rs.schema_version,
                "reason": "legacy version explicitly rejected",
                "run_id": rs.run_id,
            },
        )


# ---------------------------------------------------------------------------
# Public API — checkpoint_atomic
# ---------------------------------------------------------------------------


def checkpoint_atomic(
    run_state: RunState,
    intent: str,
    *,
    expected_current_file_hash: str | None,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
) -> CheckpointResult:
    """§4.13 atomic CAS-swap envelope.

    Writes ``pipeline/{run_state.run_id}/state.json`` via the injected
    ``vault_write`` callable with CAS semantics (caller provides
    ``expected_current_file_hash``). On CAS mismatch, sleeps
    ``CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS[min(attempt, 2)]`` ms and retries,
    bounded by the schedule length (3) AND the total wall-clock timeout
    (``CHECKPOINT_TOTAL_TIMEOUT_SEC = 10`` seconds).

    Failure modes:

    - **CAS exhaustion or total-timeout.** Writes a quarantine marker
      (``_write_quarantine_marker``) BEFORE raising ``F_PIPE_01``. Mutates
      ``run_state.quarantine_marker_ref`` and ``run_state.phase =
      "quarantined"`` before the raise.
    - **Terminal non-CAS ``VaultError``.** Writes a ``state-failure``
      checkpoint via ``_write_state_failure_wrapper`` (best-effort) and
      RE-RAISES THE ORIGINAL ``VaultError``. Does NOT raise ``F_PIPE_01``;
      does NOT write a quarantine marker.

    Success:

    - Mutates ``run_state.last_checkpoint_iso = clock.now_iso()``.
    - Returns a ``CheckpointResult`` frozen dataclass.

    Parameters
    ----------
    run_state
        The live ``RunState`` to persist. Mutated on both success (last
        checkpoint iso) and CAS-exhausted/timeout (quarantine ref + phase).
    intent
        One of ``state-success``, ``state-failure``, ``state-quarantine``.
        Not validated here — Cedar at the vault layer is the source of
        truth; passing an unauthorized intent surfaces as a terminal
        ``VaultError``.
    expected_current_file_hash
        CAS head pin. ``None`` for write-if-absent (first checkpoint of a
        run); a hex SHA-256 digest for subsequent overwrites.
    vault_write, clock, sleep
        Injected Protocols (see module-level docs).
    """
    # Canonicalize + hash once. The hash is informational (returned in the
    # CheckpointResult) — the authoritative post-write hash is what
    # vault_write itself returns on success.
    canonical = _canonicalize_runstate(run_state)
    payload_sha256 = hashlib.sha256(canonical).hexdigest()

    # Wall-clock window. Inline-literal 10_000 — rebind-resistant.
    start_ms = clock.now_ms()
    path = f"pipeline/{run_state.run_id}/state.json"

    # Back-off schedule as INLINE LITERAL. Rebinding
    # pipeline.loop.config.CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS has no effect.
    # Schedule length (3) also governs the CAS retry ceiling per §8.
    backoff_schedule_ms: Final[tuple[int, int, int]] = (50, 200, 800)

    attempt_count = 0
    last_cas_err: VaultCASHeadMismatch | None = None

    # Attempt loop bounded by schedule length (V1 inline-literal 3).
    for attempt in range(3):
        # Total-timeout check — inline literal 10_000 ms.
        elapsed_ms = clock.now_ms() - start_ms
        if elapsed_ms > 10_000:
            break
        attempt_count += 1
        try:
            committed_hash = vault_write(
                path=path,
                payload=canonical,
                intent=intent,
                write_mode="overwrite",
                expected_current_file_hash=expected_current_file_hash,
            )
        except VaultCASHeadMismatch as cerr:
            last_cas_err = cerr
            # Back-off per inline-literal schedule.
            backoff_ms = backoff_schedule_ms[min(attempt, 2)]
            sleep(backoff_ms)
            continue
        except VaultError as terminal_err:
            # §4.13 lines 813-817: state-failure wrapper + re-raise ORIGINAL.
            # Never synthesize F_PIPE_01 on this branch — blueprint-faithful.
            _write_state_failure_wrapper(
                run_state,
                terminal_err,
                vault_write=vault_write,
                clock=clock,
            )
            raise
        else:
            # Success path.
            written_iso = clock.now_iso()
            run_state.last_checkpoint_iso = written_iso
            return CheckpointResult(
                written_at_iso=written_iso,
                committed_hash=committed_hash,
                attempt_count=attempt_count,
                elapsed_ms=clock.now_ms() - start_ms,
                quarantine_marker_ref=None,
            )

    # CAS exhausted (or total-timeout triggered a break). A-v1-01 closure:
    # quarantine marker writes BEFORE F_PIPE_01 is raised.
    final_elapsed_ms = clock.now_ms() - start_ms
    reason = (
        "total_timeout"
        if final_elapsed_ms > 10_000
        else "cas_exhausted"
    )
    quarantine_ref = _write_quarantine_marker(
        run_state,
        reason=reason,
        vault_write=vault_write,
        clock=clock,
    )
    run_state.quarantine_marker_ref = quarantine_ref
    run_state.phase = "quarantined"
    raise F_PIPE_01(
        trigger=f"run_state_corrupt_{reason}",
        details={
            "run_id": run_state.run_id,
            "attempt_count": attempt_count,
            "elapsed_ms": final_elapsed_ms,
            "quarantine_marker_ref": quarantine_ref,
            "payload_sha256": payload_sha256,
            "last_cas_mismatch_expected": (
                getattr(last_cas_err, "expected_current_file_hash", None)
                if last_cas_err is not None
                else None
            ),
            "last_cas_mismatch_actual": (
                getattr(last_cas_err, "actual_current_file_hash", None)
                if last_cas_err is not None
                else None
            ),
        },
    )


__all__ = [
    "BLUEPRINT_DEPS",
    "CheckpointResult",
    "ClockProtocol",
    "SleepCallable",
    "VaultWriteCallable",
    "checkpoint_atomic",
    "_assert_runstate_schema_current",
    "_write_quarantine_marker",
    "_write_state_failure_wrapper",
]
