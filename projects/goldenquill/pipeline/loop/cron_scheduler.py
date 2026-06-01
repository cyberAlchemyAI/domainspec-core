"""pipeline.loop.cron_scheduler — §4.10 v2 flock + vault-stamp two-layer dedupe (Round 10).

Blueprint §5 v6 LOCKED 2026-04-19:
- §4.10 v2 ``fire_once`` (lines 651-687) — two-layer dedupe (local flock +
  durable vault stamp), DST-safe task-id, CRON_VAULT_RETRY window.
- §8 ``CRON_VAULT_RETRY_ATTEMPTS=6``, ``CRON_VAULT_RETRY_WINDOW_SEC=300``,
  ``CRON_STAMP_TTL_HOURS=36``.
- §6 F-PIPE-15 (``cron_dedupe_failure``).
- §2 vault ``write-if-absent`` + ``VaultWriteExists``.

**Core design decisions (confirmed at Round 10 ORIENT — 2026-04-21)**

1. *Spec-card arithmetic drift corrected.* The spec card pre-staged at Round 8
   proposed ``max_attempts=3`` / ``total_window_sec=60``. Round 1 ``config.py``
   pins ``CRON_VAULT_RETRY_ATTEMPTS=6`` / ``CRON_VAULT_RETRY_WINDOW_SEC=300``
   and Round 1 is LOCKED. The blueprint pseudo-code references the config
   constants directly. Round 10 follows config + blueprint (6 / 300) as the
   source of truth and documents the spec-card drift in ``lock_history``.

2. *Inline-literal rebind-resistance (V1 discipline).* Defaults ``6`` and
   ``300`` appear as inline literals at the kwarg default site; the back-off
   formula ``min(30, 2 ** attempt)`` inline-literals ``30`` and ``2``. A
   rebind of ``pipeline.loop.config.CRON_VAULT_RETRY_ATTEMPTS`` /
   ``CRON_VAULT_RETRY_WINDOW_SEC`` / ``CRON_STAMP_TTL_HOURS`` cannot alter
   runtime behaviour. Module-load asserts here catch rebind-before-load.

3. *``VaultTransientError`` owned by this module.* Blueprint §4.10 line 679
   references ``VaultTransientError`` but the §2 vault package does not
   export such a class. Transient network/IO failures are transport-layer
   concerns, not vault-intrinsic (cf. ``VaultCASHeadMismatch`` which IS a
   vault-primary concept). Round 10 ships :class:`VaultTransientError` as
   a module-level marker — production ``vault_write`` adapters raise it
   when they detect transient conditions (e.g. ``ConnectionError``,
   ``TimeoutError``, ``OSError.EAGAIN``). The injected Protocol contract
   is: raise ``VaultWriteExists`` on duplicate, ``VaultTransientError`` on
   retry-worthy, any other ``Exception`` on terminal.

4. *``FlockAcquire`` is a Protocol, not a concrete import of ``fcntl``.*
   Ninth E-017 firing. Production wiring supplies a ``contextlib.contextmanager``
   that wraps ``fcntl.flock(..., LOCK_EX | LOCK_NB)``; tests inject a fake
   that yields ``True`` / ``False`` to exercise both branches. Round 10
   itself imports neither ``fcntl`` nor the ``filelock`` package — keeps
   the module POSIX-portable and sovereign.

5. *Flock retained on F_PIPE_15 raise.* Blueprint line 682 is explicit:
   transient-exhaustion raises WITHOUT releasing the flock. Round 10 raises
   inside the ``with flock_acquire(...)`` block; the ``__exit__`` call runs
   as normal exception unwinding AFTER the raise is observed. The adversarial
   test verifies the raise-time state by inspecting ``__exit__``'s
   ``exc_type`` argument — at the point the context manager is entered with
   the exception, the flock is still held.

6. *Total-window secondary guard.* The blueprint pseudo-code relies purely
   on ``attempt + 1 == CRON_VAULT_RETRY_ATTEMPTS``; the wall-clock budget
   is implicit in the back-off sum (1+2+4+8+16 = 31s ≪ 300s). Round 10
   adds an EXPLICIT secondary check ``clock.now_ms() - start_ms > 300_000``
   before every attempt, raising F_PIPE_15 with trigger
   ``cron_dedupe_failure:{cron_task_id}:window_exceeded`` if a pathologically
   slow clock or an externally mutated sleep callable blows the budget. The
   normal exhaustion path uses trigger ``cron_dedupe_failure:{cron_task_id}``.

7. *``on_fire`` exceptions propagate; stamp is NOT rolled back.* Spec-card
   OQ-2: the stamp is the durable "this task FIRED" record. Downstream
   failure is the caller's problem. ``on_fire`` executes AFTER the stamp
   lands inside the flock context; its exceptions propagate and the flock
   releases via context-manager unwinding. ``CronFireResult`` is NOT
   returned on this path (the exception short-circuits the return).

8. *Mode-isolation.* ``fire_once`` is SUBMISSION-MODE; eval-mode does not
   fire crons. Round 10 does NOT assert mode here — ``fire_once`` is called
   BEFORE ``start_run`` and there is no ``RunState`` yet. Mode enforcement
   is the caller's responsibility.

9. *Stale lock-file hygiene.* Round 10 does NOT sweep stale ``.lock`` files
   from crashed processes. An operator boot script or a separate janitor
   primitive handles that. The ``flock_acquire`` Protocol is blueprint-
   idiomatic; its production implementation decides retention policy.

**Threat model (§3.11 v5 trusted-operator envelope; E-023 closure)**

Round 10 is a §5 orchestrator primitive — no network, no subprocess, no
§4 Logician consumption. The following residuals are OUT-OF-SCOPE for
v0.1 and documented by explicit ``test_adv_*`` tests rather than
defended at this layer:

- **Stale ``.lock`` file from a crashed previous process.** ``flock_acquire``
  returns ``False`` until the kernel-level advisory lock is released; the
  file's presence alone is not a lock. Round 10 does not unlink the file.

- **``on_fire`` raising ``F_PIPE_15``.** If the caller-supplied ``on_fire``
  itself raises an exception TYPED as ``F_PIPE_15``, it propagates unchanged
  — Round 10 does NOT inspect/wrap the exception. Trigger taxonomy pinning
  is the caller's discipline.

- **Non-monotonic ``clock.now_ms``.** The elapsed-time computation clamps
  the delta at zero; the budget check cannot report a negative elapsed.
  A backward clock never triggers the window-exceeded path but may starve
  it (we would simply run through all ``max_attempts``).

- **``flock_acquire`` raising on probe.** Round 10 does NOT wrap the
  ``with`` entry in a try/except. Any exception from ``flock_acquire``
  propagates unwrapped — operator/wiring bug.

- **Task-id collision across prefixes.** Spec-card OQ-4: two cron triggers
  with different prefixes produce distinct task_ids by construction. No
  cross-prefix collision defense needed.

Spec card: ``pipeline/engineering/spec_cards/section_05_round_10_cron_scheduler.md``.
"""

from __future__ import annotations

import pathlib
from contextlib import AbstractContextManager
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Final, Protocol, runtime_checkable

from pipeline.loop.config import (
    CRON_STAMP_TTL_HOURS,
    CRON_VAULT_RETRY_ATTEMPTS,
    CRON_VAULT_RETRY_WINDOW_SEC,
)
from pipeline.loop.errors import F_PIPE_15
from pipeline.loop.state_checkpoint import (
    ClockProtocol,
    SleepCallable,
    VaultWriteCallable,
)
from pipeline.vault import VaultWriteExists

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.10 v2 fire_once (flock + vault-stamp + retry + F-PIPE-15)",
            "§4.10 v2 build_cron_task_id (DST-safe UTC-anchored id)",
            "§8 CRON_VAULT_RETRY_ATTEMPTS / CRON_VAULT_RETRY_WINDOW_SEC / "
            "CRON_STAMP_TTL_HOURS pins",
            "§6 F-PIPE-15 cron_dedupe_failure",
        ],
    },
}

# ---------------------------------------------------------------------------
# Inline-literal module-load integrity asserts (V1 discipline)
# ---------------------------------------------------------------------------

assert CRON_VAULT_RETRY_ATTEMPTS == 6, (
    "pipeline.loop.config.CRON_VAULT_RETRY_ATTEMPTS has been rebound "
    "before pipeline.loop.cron_scheduler import; refusing to load"
)
assert CRON_VAULT_RETRY_WINDOW_SEC == 300, (
    "pipeline.loop.config.CRON_VAULT_RETRY_WINDOW_SEC has been rebound "
    "before pipeline.loop.cron_scheduler import; refusing to load"
)
assert CRON_STAMP_TTL_HOURS == 36, (
    "pipeline.loop.config.CRON_STAMP_TTL_HOURS has been rebound "
    "before pipeline.loop.cron_scheduler import; refusing to load"
)
assert F_PIPE_15.CODE == "F-PIPE-15", (
    "pipeline.loop.errors.F_PIPE_15.CODE has been rebound before "
    "pipeline.loop.cron_scheduler import; refusing to load"
)


# ---------------------------------------------------------------------------
# Transient-error marker (owned by Round 10 — see design decision #3)
# ---------------------------------------------------------------------------


class VaultTransientError(Exception):
    """Marker for retry-worthy transient failures from an injected vault_write.

    Production ``vault_write`` wiring raises this when a write fails due to
    a transport-layer condition (connection reset, timeout, EAGAIN). The
    retry loop in :func:`fire_once` catches it and backs off exponentially;
    on exhaustion the loop raises :class:`F_PIPE_15`.

    NOT a ``VaultError`` subclass — transient conditions are transport-layer,
    not vault-intrinsic. Keeps the vault package's error taxonomy clean.
    """


# ---------------------------------------------------------------------------
# Public Protocols (E-017 injected-callable pattern — ninth firing)
# ---------------------------------------------------------------------------


@runtime_checkable
class FlockAcquire(Protocol):
    """Injected flock primitive.

    Returns a context manager that yields a boolean: ``True`` if the
    advisory exclusive lock on ``lock_path`` was acquired non-blocking,
    ``False`` if another process holds it. On exit the context manager
    releases the lock if it was acquired (no-op otherwise).

    Production wiring wraps ``fcntl.flock(fd, LOCK_EX | LOCK_NB)`` under a
    ``contextlib.contextmanager``. Tests inject a fake that yields the
    desired boolean and records ``__exit__`` observations.
    """

    def __call__(
        self, lock_path: pathlib.Path
    ) -> AbstractContextManager[bool]: ...


@runtime_checkable
class OnFireCallable(Protocol):
    """Injected fire-action callable.

    Invoked iff the flock was acquired AND the vault stamp landed. Receives
    the already-deduped ``cron_task_id`` as a keyword argument so the callee
    can log / correlate. Return value is ignored; exceptions propagate
    unchanged (stamp is NOT rolled back — spec-card OQ-2).
    """

    def __call__(self, *, cron_task_id: str) -> None: ...


# ---------------------------------------------------------------------------
# Public result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class CronFireResult:
    """Returned on any non-raising :func:`fire_once` outcome.

    Attributes
    ----------
    cron_task_id
        The (validated) task-id threaded through dedupe + on_fire.
    fired
        ``True`` iff ``on_fire`` was invoked (flock acquired + stamp landed).
    dedupe_layer
        ``None`` when fired is True; ``"flock"`` when the local flock
        short-circuited; ``"vault_stamp"`` when the vault reported an
        existing stamp (durable dedupe hit).
    attempts
        Number of vault-write attempts consumed. ``0`` when dedupe_layer is
        ``"flock"`` (no vault I/O); ``1..max_attempts`` otherwise. On
        ``"vault_stamp"`` dedupe this is the attempt count on which
        ``VaultWriteExists`` surfaced.
    """

    cron_task_id: str
    fired: bool
    dedupe_layer: str | None
    attempts: int


# ---------------------------------------------------------------------------
# Public helper — DST-safe task-id
# ---------------------------------------------------------------------------


def build_cron_task_id(*, prefix: str, utc_iso_anchor: str) -> str:
    """Build a DST-safe cron task-id (B-v1-03 closure).

    Format: ``f"{prefix}_{YYYY-MM-DD}_{HH_MM}"``. Local TZ is NEVER
    consulted — the UTC ``HH_MM`` component distinguishes two 08:30 local
    firings during DST fall-back.

    Strict validation:
    - ``prefix`` must be non-empty.
    - ``utc_iso_anchor`` must be non-empty.
    - ``utc_iso_anchor`` must contain ``"T"`` (ISO date/time separator).
    - ``utc_iso_anchor`` must end with ``"+00:00"`` or ``"Z"`` (UTC offset).
    - The parsed ``datetime`` must have ``tzinfo == timezone.utc``.

    Any violation raises :class:`ValueError`. Caller is responsible for
    catching / propagating.
    """
    if not prefix:
        raise ValueError("build_cron_task_id: prefix must be non-empty")
    if not utc_iso_anchor:
        raise ValueError("build_cron_task_id: utc_iso_anchor must be non-empty")
    if "T" not in utc_iso_anchor:
        raise ValueError(
            f"build_cron_task_id: utc_iso_anchor must contain 'T'; "
            f"got {utc_iso_anchor!r}"
        )
    if not (utc_iso_anchor.endswith("+00:00") or utc_iso_anchor.endswith("Z")):
        raise ValueError(
            f"build_cron_task_id: utc_iso_anchor must end with '+00:00' or "
            f"'Z'; got {utc_iso_anchor!r}"
        )
    normalised = (
        utc_iso_anchor.replace("Z", "+00:00")
        if utc_iso_anchor.endswith("Z")
        else utc_iso_anchor
    )
    try:
        dt = datetime.fromisoformat(normalised)
    except ValueError as e:
        raise ValueError(
            f"build_cron_task_id: utc_iso_anchor not parseable as ISO-8601: "
            f"{utc_iso_anchor!r}"
        ) from e
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError(
            f"build_cron_task_id: utc_iso_anchor must be UTC "
            f"(offset +00:00); got offset {dt.utcoffset()}"
        )
    date_str = dt.strftime("%Y-%m-%d")
    hhmm = dt.strftime("%H_%M")
    return f"{prefix}_{date_str}_{hhmm}"


# ---------------------------------------------------------------------------
# Public entry — fire_once
# ---------------------------------------------------------------------------


def fire_once(
    *,
    cron_task_id: str,
    on_fire: OnFireCallable,
    flock_acquire: FlockAcquire,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
    lock_dir: pathlib.Path,
    max_attempts: int = 6,
    total_window_sec: int = 300,
) -> CronFireResult:
    """§4.10 v2 two-layer dedupe cron fire-once primitive.

    Order of operations (blueprint lines 658-687):

    1. Compute ``lock_path = lock_dir / f"{cron_task_id}.lock"``; mkdir
       parents if absent.
    2. Acquire non-blocking exclusive flock. Not acquired → return
       ``CronFireResult(fired=False, dedupe_layer="flock", attempts=0)``.
    3. Under the flock, write ``cron/fired/{cron_task_id}.stamp`` via
       ``write_mode="write-if-absent"``. Retry up to ``max_attempts`` times
       on :class:`VaultTransientError` with back-off
       ``sleep_ms = min(30, 2 ** attempt) * 1000``. Secondary budget guard:
       if ``clock.now_ms() - start_ms > total_window_sec * 1000`` before any
       attempt, raise :class:`F_PIPE_15` with trigger suffix
       ``:window_exceeded``.
    4. ``VaultWriteExists`` → return
       ``CronFireResult(fired=False, dedupe_layer="vault_stamp", attempts=N)``.
    5. On successful stamp, invoke ``on_fire(cron_task_id=...)``. Its
       exceptions propagate; stamp is NOT rolled back.
    6. Return ``CronFireResult(fired=True, dedupe_layer=None, attempts=N)``.

    Parameters
    ----------
    cron_task_id
        Output of :func:`build_cron_task_id`, e.g. ``"fund_radar_2026-04-21_12_30"``.
    on_fire
        Caller's fire-action (e.g. scout radar entry). Invoked only on
        successful dedupe-free path.
    flock_acquire
        Injected :class:`FlockAcquire` — yields acquired-bool.
    vault_write
        Injected :class:`VaultWriteCallable` — mirrors §2 vault_write.
    clock
        Injected :class:`ClockProtocol` for monotonic-ms + ISO timestamps.
    sleep
        Injected :class:`SleepCallable` — ms granularity.
    lock_dir
        Directory holding ``.lock`` files. Tests pass ``tmp_path``;
        production passes ``Path.home() / ".tilth" / "cron_locks"``.
    max_attempts
        Per-task vault-write retry ceiling. Default ``6`` mirrors
        ``CRON_VAULT_RETRY_ATTEMPTS`` (inline-literal).
    total_window_sec
        Wall-clock budget ceiling. Default ``300`` mirrors
        ``CRON_VAULT_RETRY_WINDOW_SEC`` (inline-literal).

    Raises
    ------
    F_PIPE_15
        Transient retries exhausted OR total-window exceeded. Flock is
        still held at raise-time (context-manager unwinds after the raise
        propagates, releasing the lock on the way out).
    """
    if not cron_task_id:
        raise ValueError("fire_once: cron_task_id must be non-empty")
    if max_attempts <= 0:
        raise ValueError(
            f"fire_once: max_attempts must be positive; got {max_attempts}"
        )
    if total_window_sec <= 0:
        raise ValueError(
            f"fire_once: total_window_sec must be positive; "
            f"got {total_window_sec}"
        )

    lock_path = lock_dir / f"{cron_task_id}.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    start_ms = clock.now_ms()
    window_ms = total_window_sec * 1000

    with flock_acquire(lock_path) as acquired:
        if not acquired:
            return CronFireResult(
                cron_task_id=cron_task_id,
                fired=False,
                dedupe_layer="flock",
                attempts=0,
            )

        attempts_used = 0
        for attempt in range(max_attempts):
            elapsed_ms = max(clock.now_ms() - start_ms, 0)
            if elapsed_ms > window_ms:
                raise F_PIPE_15(
                    trigger=(
                        f"cron_dedupe_failure:{cron_task_id}:window_exceeded"
                    ),
                    details={
                        "cron_task_id": cron_task_id,
                        "attempts": attempts_used,
                        "elapsed_ms": elapsed_ms,
                        "last_error": "window_exceeded",
                    },
                )
            attempts_used = attempt + 1
            try:
                vault_write(
                    path=f"cron/fired/{cron_task_id}.stamp",
                    payload=clock.now_iso().encode("utf-8"),
                    intent="state-success",
                    write_mode="write-if-absent",
                    expected_current_file_hash=None,
                )
                break
            except VaultWriteExists:
                return CronFireResult(
                    cron_task_id=cron_task_id,
                    fired=False,
                    dedupe_layer="vault_stamp",
                    attempts=attempts_used,
                )
            except VaultTransientError as transient:
                if attempt + 1 == max_attempts:
                    final_elapsed = max(clock.now_ms() - start_ms, 0)
                    raise F_PIPE_15(
                        trigger=f"cron_dedupe_failure:{cron_task_id}",
                        details={
                            "cron_task_id": cron_task_id,
                            "attempts": attempts_used,
                            "elapsed_ms": final_elapsed,
                            "last_error": type(transient).__name__,
                        },
                    ) from transient
                sleep_ms = min(30, 2 ** attempt) * 1000
                sleep(sleep_ms)

        on_fire(cron_task_id=cron_task_id)

    return CronFireResult(
        cron_task_id=cron_task_id,
        fired=True,
        dedupe_layer=None,
        attempts=attempts_used,
    )
