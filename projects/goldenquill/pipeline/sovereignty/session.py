"""Session dataclass + lifecycle + M7 HMAC key + signal plumbing. [§2.4, §3.3, §4.5, §4.6, §4.7, §8]

Section 1 Round E. Owns:

* :class:`Session` frozen dataclass (§2.4).
* :func:`start_session` / :func:`end_session` (§3.3).
* :func:`rotate_hmac_key` (§4.6 rotation w/ 5 s grace timer).
* :func:`sign_health_tuple` (M7 signing primitive used by Scout).
* Unified SIGTERM/SIGINT handler (§4.5 v3 one-shot flag + v4 non-blocking
  checkpoint-lock).
* LLM-active checkpoint thread (30 s interval per §4.5).
* Module-level `_active_runtime` + `.active.lock` enforcing the
  single-active-session invariant.

Blueprint references:

* §2.4 Session schema
* §3.3 session lifecycle signatures
* §4.5 M6 signal plumbing (v3 unified, v4 non-blocking checkpoint lock)
* §4.6 M7 per-session HMAC key lifecycle (SecretBytes + 5 s grace)
* §4.7 M10 author-seat degradation threshold constant
* §6 F-SESSION-* + F-KEY-03 propagation
* §8 pinned constants

Under Round-E dependency scope, :func:`start_session` accepts a duck-typed
``envelope`` carrying ``router_manifest_sha`` + ``keystore`` + ``repo_root``,
plus ``rfa`` with ``session_bound_slug`` and ``project_context`` with
``slug``. When Rounds F/G/H land, their real envelope dataclasses will
satisfy the same shapes; tests use lightweight stand-in objects.

E-enforcement:

* E-001 arg-type validation before any I/O
* E-007 tests monkey-patch names AS IMPORTED INTO session.py
* E-010 mutable env-var state at construction → we snapshot ``TILTH_*`` at
  :func:`start_session`; no post-bind re-reads
"""

from __future__ import annotations

import datetime as _dt
import errno
import fcntl
import hashlib as _hashlib
import hmac as _stdlib_hmac
import json
import os
import secrets
import signal
import threading
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from pipeline.sovereignty import interrupted_state as _interrupted_state
from pipeline.sovereignty.crypto_primitives import zero_bytes
from pipeline.sovereignty.interrupted_state import (
    _atomic_write_with_st_dev_double_check,
    _canonical_json_bytes,
)
from pipeline.sovereignty.org_slug import canonical_slug

__all__ = [
    # Constants (§8)
    "HMAC_KEY_ROTATION_GRACE_SECONDS",
    "LLM_ACTIVE_CHECKPOINT_INTERVAL_SECONDS",
    "M10_AUTHOR_SEAT_DEGRADATION_THRESHOLD_SECONDS",
    "SESSION_HMAC_KEY_BYTES",
    "SIGNAL_HANDLER_CHECKPOINT_LOCK_NONBLOCKING",
    "SIGNAL_HANDLER_KEY_ZERO_FIRST",
    "SIGNAL_HANDLER_ONE_SHOT_FLAG_NAME",
    "SIGTERM_GRACE_SECONDS",
    # Exceptions
    "InvalidSlugError",
    "SessionAlreadyActive",
    "SessionError",
    "SessionRuntimeNotBound",
    "SessionSlugMismatch",
    # Primary surface
    "Session",
    "end_session",
    "rotate_hmac_key",
    "sign_health_tuple",
    "start_session",
]


# ---------------------------------------------------------------------------
# Constants (§8 — pinned values)
# ---------------------------------------------------------------------------

SESSION_HMAC_KEY_BYTES: int = 64  # ≤ SHA3-512 block size (72)
SIGTERM_GRACE_SECONDS: int = 5
LLM_ACTIVE_CHECKPOINT_INTERVAL_SECONDS: int = 30
M10_AUTHOR_SEAT_DEGRADATION_THRESHOLD_SECONDS: int = 1800  # 30 min — §4.7
HMAC_KEY_ROTATION_GRACE_SECONDS: int = 5  # v2 — reduced from 60 per Red Team [MEDIUM]
SIGNAL_HANDLER_KEY_ZERO_FIRST: bool = True
SIGNAL_HANDLER_ONE_SHOT_FLAG_NAME: str = "_shutting_down"
SIGNAL_HANDLER_CHECKPOINT_LOCK_NONBLOCKING: bool = True

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": [
            "§2.4 Session dataclass",
            "§3.3 start_session/end_session",
            "§4.5 M6 atomic flush + signal plumbing (v3 + v4)",
            "§4.6 M7 per-session HMAC key lifecycle (SecretBytes + 5 s grace)",
            "§4.7 M10 author-seat degradation threshold constant",
            "§6 F-SESSION-* + F-KEY-03 propagation",
            "§8 pinned constants",
        ],
        "hash_at_lock": "lock-round-E-v2-2026-04-19",
        "hash_source_version": "v6",
    },
}


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class SessionError(RuntimeError):
    """Base for all F-SESSION-* failure codes."""


class SessionAlreadyActive(SessionError):
    """F-SESSION-ALREADY-ACTIVE. Another session holds .active.lock."""


class SessionSlugMismatch(SessionError):
    """F-SESSION-SLUG-MISMATCH. rfa.session_bound_slug != project_context.slug."""


class InvalidSlugError(SessionError):
    """F-SESSION-INVALID-SLUG. project_context.slug fails canonicalization."""


class SessionRuntimeNotBound(SessionError):
    """F-SESSION-RUNTIME-NOT-BOUND. Runtime-only API called with no active runtime."""


# ---------------------------------------------------------------------------
# Session dataclass (§2.4)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class Session:
    """§2.4. Sovereignty session record written to sovereignty/sessions/{id}.json.

    Fields are the canonical v2-combined schema: session identity +
    binding (slug, started_at, hmac_key_id, router_manifest_sha, pid) +
    status. ``interrupted_payload_path`` is a telemetry Path handle set
    by :func:`checkpoint` when status transitions to ``INTERRUPTED``.

    The dataclass is frozen so tests cannot accidentally mutate the
    session identity after :func:`start_session`. The mutable runtime
    state (HMAC key buffer, last-checkpoint payload, rotation timer)
    lives in a module-level ``_active_runtime`` registry keyed by
    session_id.
    """

    session_id: str
    slug: str
    started_at: str
    hmac_key_id: str
    router_manifest_sha: str
    pid: int
    status: str
    interrupted_payload_path: str | None = None


# ---------------------------------------------------------------------------
# Duck-typed envelope protocols (Rounds F/G/H will implement the concrete types)
# ---------------------------------------------------------------------------


class _RFALike(Protocol):
    session_bound_slug: str


class _ProjectContextLike(Protocol):
    slug: str


class _EnvelopeLike(Protocol):
    router_manifest_sha: str
    # keystore + repo_root accessed via getattr so test stand-ins can use
    # either attribute names or __getitem__ — duck-typing is deliberate.


# ---------------------------------------------------------------------------
# Runtime state (mutable companion to the frozen Session)
# ---------------------------------------------------------------------------


@dataclass
class _SessionRuntime:
    session: Session
    keystore: Any
    repo_root: Path
    active_lock_fd: int
    _last_checkpoint_state: dict[str, Any] | None = None
    # Blueprint §4.5 v2 future-use slot: populated by future §4.6.1 M7 wire
    # layer when an LLM-signing call is mid-flight, cleared immediately
    # after. In v0.1 pre-M7-wire the field remains None because
    # `start_session` zeroes its local buffer right after `keystore.store`
    # and no other code holds a persistent bytearray copy. Signal-handler
    # step 1 is therefore a no-op today; step 3 (`keystore.zero`) is the
    # authoritative scrub. Test scaffold at
    # test_adv_signal_handler_zeroes_hmac_buffer_before_any_io simulates the
    # future active-signing window. Committee v2 GPT-OSS LOW acknowledged:
    # kept to preserve blueprint LOCK + forward-compat with §4.6.1.
    _hmac_key_buffer: bytearray | None = None
    # List not single-slot: rapid successive rotations must each schedule
    # their own grace zeroing; cancelling the prior timer leaked earlier
    # old keys past the 5s window (committee v1 GPT-OSS MED-B).
    _rotation_timers: list[threading.Timer] = field(default_factory=list)
    _old_hmac_key_ids: list[str] = field(default_factory=list)
    _checkpoint_thread: threading.Thread | None = None
    _checkpoint_stop: threading.Event = field(default_factory=threading.Event)
    _prev_sigterm_handler: Any = None
    _prev_sigint_handler: Any = None
    _signal_handlers_installed: bool = False


_shutting_down: threading.Event = threading.Event()
_checkpoint_lock: threading.Lock = threading.Lock()
_active_runtime: _SessionRuntime | None = None
_active_runtime_lock: threading.Lock = threading.Lock()


def _get_active_runtime() -> _SessionRuntime | None:
    with _active_runtime_lock:
        return _active_runtime


def _set_active_runtime(rt: _SessionRuntime | None) -> None:
    global _active_runtime
    with _active_runtime_lock:
        _active_runtime = rt


# ---------------------------------------------------------------------------
# Signal handler (§4.5 v3 + v4)
# ---------------------------------------------------------------------------


def _install_signal_handlers(runtime: _SessionRuntime) -> None:
    runtime._prev_sigterm_handler = signal.signal(
        signal.SIGTERM, _unified_signal_handler
    )
    runtime._prev_sigint_handler = signal.signal(
        signal.SIGINT, _unified_signal_handler
    )
    try:
        signal.siginterrupt(signal.SIGTERM, False)
        signal.siginterrupt(signal.SIGINT, False)
    except (AttributeError, OSError):
        pass
    runtime._signal_handlers_installed = True


def _restore_signal_handlers(runtime: _SessionRuntime) -> None:
    if not runtime._signal_handlers_installed:
        return
    try:
        signal.signal(signal.SIGTERM, runtime._prev_sigterm_handler)
        signal.signal(signal.SIGINT, runtime._prev_sigint_handler)
    except (TypeError, ValueError, OSError):
        pass
    runtime._signal_handlers_installed = False


def _unified_signal_handler(signum: int, frame: Any) -> None:
    """§4.5 v3 + v4. One-shot, zero-first, non-blocking checkpoint."""
    if _shutting_down.is_set():
        return
    _shutting_down.set()
    # Arm watchdog BEFORE any I/O so even a hang in step 1 still exits.
    try:
        signal.alarm(SIGTERM_GRACE_SECONDS)
    except (AttributeError, ValueError):
        pass
    try:
        runtime = _get_active_runtime()
        if runtime is None:
            return
        # Step 1 — ZERO FIRST (v2 ordering). Scrub the HMAC-key bytearray
        # before any I/O so a core-dump snapshot during the handler's own
        # I/O still cannot recover the key. In v0.1 pre-M7-wire the buffer
        # slot is None (see _SessionRuntime._hmac_key_buffer comment);
        # when §4.6.1 M7 wire populates it during active LLM signing, this
        # step becomes the critical scrub for that window. Authoritative
        # scrub path regardless is step 3 `keystore.zero`.
        if runtime._hmac_key_buffer is not None:
            try:
                zero_bytes(runtime._hmac_key_buffer)
            except Exception:
                pass
        # Step 2 — non-blocking checkpoint. (v4 RT-v3 LOW-1 closure.)
        if _checkpoint_lock.acquire(blocking=False):
            try:
                if runtime._last_checkpoint_state is not None:
                    try:
                        _interrupted_state.checkpoint(
                            runtime.session, runtime._last_checkpoint_state
                        )
                    except Exception:
                        pass
            finally:
                _checkpoint_lock.release()
        # Step 3 — best-effort keystore zero.
        try:
            runtime.keystore.zero(runtime.session.hmac_key_id)
        except Exception:
            pass
        # Step 3b — best-effort zero of every rotation-grace old key id.
        for old_id in list(runtime._old_hmac_key_ids):
            try:
                runtime.keystore.zero(old_id)
            except Exception:
                pass
    finally:
        try:
            if signum == signal.SIGINT:
                os._exit(130)
            else:
                os._exit(143)
        finally:
            # In production os._exit never returns. Tests monkeypatch it so
            # they can assert handler ordering in-process; clear the watchdog
            # there or a later test process can receive SIGALRM after the
            # suite has already passed.
            try:
                signal.alarm(0)
            except (AttributeError, ValueError):
                pass


# ---------------------------------------------------------------------------
# Checkpoint thread (30 s LLM-active interval)
# ---------------------------------------------------------------------------


def _checkpoint_loop(runtime: _SessionRuntime) -> None:
    while not runtime._checkpoint_stop.wait(
        LLM_ACTIVE_CHECKPOINT_INTERVAL_SECONDS
    ):
        if _checkpoint_lock.acquire(blocking=False):
            try:
                if runtime._last_checkpoint_state is not None:
                    try:
                        _interrupted_state.checkpoint(
                            runtime.session, runtime._last_checkpoint_state
                        )
                    except Exception:
                        pass
            finally:
                _checkpoint_lock.release()


# ---------------------------------------------------------------------------
# Active-lock + session-record helpers
# ---------------------------------------------------------------------------


def _sessions_dir(repo_root: Path) -> Path:
    return repo_root / "sovereignty" / "sessions"


def _acquire_active_lock(repo_root: Path) -> int:
    sessions_dir = _sessions_dir(repo_root)
    sessions_dir.mkdir(parents=True, exist_ok=True)
    lock_path = sessions_dir / ".active.lock"
    fd = os.open(str(lock_path), os.O_CREAT | os.O_WRONLY, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as e:
        os.close(fd)
        raise SessionAlreadyActive(
            f"F-SESSION-ALREADY-ACTIVE: .active.lock held at {lock_path}"
        ) from e
    except OSError as e:
        os.close(fd)
        raise SessionAlreadyActive(
            f"F-SESSION-ALREADY-ACTIVE: cannot flock .active.lock: {e}"
        ) from e
    return fd


def _release_active_lock(fd: int) -> None:
    try:
        fcntl.flock(fd, fcntl.LOCK_UN)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass


def _write_session_record(session: Session, repo_root: Path) -> Path:
    record = {
        "session_id": session.session_id,
        "slug": session.slug,
        "started_at": session.started_at,
        "hmac_key_id": session.hmac_key_id,
        "router_manifest_sha": session.router_manifest_sha,
        "pid": session.pid,
        "status": session.status,
    }
    if session.interrupted_payload_path is not None:
        record["interrupted_payload_path"] = session.interrupted_payload_path
    final_path = _sessions_dir(repo_root) / f"{session.session_id}.json"
    data = _canonical_json_bytes(record)
    _atomic_write_with_st_dev_double_check(final_path, data)
    return final_path


# ---------------------------------------------------------------------------
# Public API — start_session / end_session
# ---------------------------------------------------------------------------


def start_session(
    *, envelope: Any, rfa: Any, project_context: Any
) -> Session:
    """Boot a new sovereignty session. [§3.3]

    Duck-typed ``envelope`` must expose ``router_manifest_sha`` (str),
    ``keystore`` (KeyStore), and ``repo_root`` (Path). ``rfa`` must expose
    ``session_bound_slug``. ``project_context`` must expose ``slug``.

    Raises:
        :class:`SessionAlreadyActive` — .active.lock held.
        :class:`SessionSlugMismatch` — rfa/project_context slug divergence.
        :class:`InvalidSlugError` — slug fails canonicalization.
        any keystore-raised exception on F-KEY-03 (locked Keychain etc.).
    """
    if _get_active_runtime() is not None:
        raise SessionAlreadyActive(
            "F-SESSION-ALREADY-ACTIVE: an in-process runtime is bound; "
            "call end_session first"
        )

    # Extract + validate envelope inputs.
    router_manifest_sha = getattr(envelope, "router_manifest_sha", None)
    keystore = getattr(envelope, "keystore", None)
    repo_root = getattr(envelope, "repo_root", None)
    if (
        not isinstance(router_manifest_sha, str)
        or keystore is None
        or repo_root is None
    ):
        raise TypeError(
            "envelope must expose router_manifest_sha:str, keystore, repo_root"
        )
    repo_root = Path(repo_root)

    rfa_slug = getattr(rfa, "session_bound_slug", None)
    pc_slug = getattr(project_context, "slug", None)
    if not isinstance(rfa_slug, str) or not isinstance(pc_slug, str):
        raise TypeError(
            "rfa.session_bound_slug and project_context.slug must be str"
        )
    if rfa_slug != pc_slug:
        raise SessionSlugMismatch(
            f"F-SESSION-SLUG-MISMATCH: rfa.session_bound_slug={rfa_slug!r} "
            f"!= project_context.slug={pc_slug!r}"
        )
    try:
        canonical = canonical_slug(pc_slug)
    except Exception as e:
        raise InvalidSlugError(
            f"F-SESSION-INVALID-SLUG: project_context.slug={pc_slug!r} rejected: {e}"
        ) from e
    if canonical != pc_slug:
        raise InvalidSlugError(
            f"F-SESSION-INVALID-SLUG: project_context.slug={pc_slug!r} is not "
            f"canonical (would be {canonical!r}); caller must pre-canonicalize"
        )

    # Acquire .active.lock (cross-process invariant).
    active_lock_fd = _acquire_active_lock(repo_root)

    try:
        # M7 HMAC key issuance (§4.6).
        session_id = uuid.uuid4().hex
        hmac_key_id = f"tilth.session.{session_id}.hmac.v1"
        hmac_key_buffer = bytearray(secrets.token_bytes(SESSION_HMAC_KEY_BYTES))
        try:
            keystore.store(
                key_id=hmac_key_id,
                key_bytes=hmac_key_buffer,
                purpose="session_hmac",
            )
        finally:
            # v2 — zero the local bytearray IMMEDIATELY after keystore.store;
            # the keystore owns its own copy.
            zero_bytes(hmac_key_buffer)

        started_at = _dt.datetime.now(_dt.timezone.utc).isoformat(
            timespec="microseconds"
        )
        session = Session(
            session_id=session_id,
            slug=pc_slug,
            started_at=started_at,
            hmac_key_id=hmac_key_id,
            router_manifest_sha=router_manifest_sha,
            pid=os.getpid(),
            status="ACTIVE",
        )
        # Expose repo_root to interrupted_state.checkpoint via _repo_root.
        # Set on the frozen instance via object.__setattr__ — intentional.
        object.__setattr__(session, "_repo_root", repo_root)

        # Write ACTIVE record.
        _write_session_record(session, repo_root)

        # Build runtime + install handlers + start checkpoint thread.
        runtime = _SessionRuntime(
            session=session,
            keystore=keystore,
            repo_root=repo_root,
            active_lock_fd=active_lock_fd,
        )
        _shutting_down.clear()
        _install_signal_handlers(runtime)
        runtime._checkpoint_stop.clear()
        thread = threading.Thread(
            target=_checkpoint_loop,
            args=(runtime,),
            name=f"tilth-checkpoint-{session_id[:8]}",
            daemon=True,
        )
        runtime._checkpoint_thread = thread
        thread.start()
        _set_active_runtime(runtime)
        return session
    except BaseException:
        _release_active_lock(active_lock_fd)
        raise


def end_session(session: Session, *, status: str = "ENDED_CLEAN") -> None:
    """Tear down the active session and scrub the HMAC key. [§3.3, §4.6]"""
    if not isinstance(status, str):
        raise TypeError(f"status must be str; got {type(status).__name__}")
    if status not in {"ENDED_CLEAN", "INTERRUPTED"}:
        raise ValueError(
            f"end_session status must be 'ENDED_CLEAN'|'INTERRUPTED'; got {status!r}"
        )
    runtime = _get_active_runtime()
    if runtime is None:
        # Idempotent no-op — second end_session on the same session is fine.
        return
    if runtime.session.session_id != session.session_id:
        raise SessionError(
            f"end_session: session_id mismatch "
            f"(active={runtime.session.session_id}, got={session.session_id})"
        )

    # Stop checkpoint thread.
    runtime._checkpoint_stop.set()
    if runtime._checkpoint_thread is not None:
        runtime._checkpoint_thread.join(timeout=2.0)

    # Cancel every pending rotation grace timer + zero grace-old keys
    # immediately. Each timer was scheduled against its own old_key_id;
    # cancelling here is safe because we zero the same ids explicitly below.
    for t in list(runtime._rotation_timers):
        try:
            t.cancel()
        except Exception:
            pass
    runtime._rotation_timers.clear()
    for old_id in list(runtime._old_hmac_key_ids):
        try:
            runtime.keystore.zero(old_id)
        except Exception:
            pass
    runtime._old_hmac_key_ids.clear()

    # Zero the active HMAC key.
    try:
        runtime.keystore.zero(runtime.session.hmac_key_id)
    except Exception:
        pass

    # Rewrite session record with final status.
    final_session = Session(
        session_id=runtime.session.session_id,
        slug=runtime.session.slug,
        started_at=runtime.session.started_at,
        hmac_key_id=runtime.session.hmac_key_id,
        router_manifest_sha=runtime.session.router_manifest_sha,
        pid=runtime.session.pid,
        status=status,
    )
    object.__setattr__(final_session, "_repo_root", runtime.repo_root)
    _write_session_record(final_session, runtime.repo_root)

    # Restore handlers, release lock, clear runtime.
    _restore_signal_handlers(runtime)
    _release_active_lock(runtime.active_lock_fd)
    _set_active_runtime(None)


# ---------------------------------------------------------------------------
# rotate_hmac_key (§4.6)
# ---------------------------------------------------------------------------


def rotate_hmac_key(session: Session) -> Session:
    """Issue new HMAC key_id; schedule 5 s grace zero of the old. [§4.6]

    Returns a new :class:`Session` with the rotated ``hmac_key_id``.
    """
    runtime = _get_active_runtime()
    if runtime is None or runtime.session.session_id != session.session_id:
        raise SessionRuntimeNotBound(
            "F-SESSION-RUNTIME-NOT-BOUND: rotate_hmac_key requires the "
            "active session"
        )

    old_key_id = runtime.session.hmac_key_id
    # Version-bump the .v1 suffix; fall back to uuid suffix if no .v{n}.
    new_key_id = _bump_key_id_version(old_key_id)

    new_key_buffer = bytearray(secrets.token_bytes(SESSION_HMAC_KEY_BYTES))
    try:
        runtime.keystore.store(
            key_id=new_key_id, key_bytes=new_key_buffer, purpose="session_hmac"
        )
    finally:
        zero_bytes(new_key_buffer)

    # Swap active Session record.
    new_session = Session(
        session_id=runtime.session.session_id,
        slug=runtime.session.slug,
        started_at=runtime.session.started_at,
        hmac_key_id=new_key_id,
        router_manifest_sha=runtime.session.router_manifest_sha,
        pid=runtime.session.pid,
        status=runtime.session.status,
    )
    object.__setattr__(new_session, "_repo_root", runtime.repo_root)
    runtime.session = new_session
    _write_session_record(new_session, runtime.repo_root)

    # Schedule grace zero.
    runtime._old_hmac_key_ids.append(old_key_id)

    def _zero_old_key_on_grace() -> None:
        try:
            runtime.keystore.zero(old_key_id)
        except Exception:
            pass
        try:
            runtime._old_hmac_key_ids.remove(old_key_id)
        except ValueError:
            pass

    # Each rotation schedules its OWN grace timer. Prior timers continue
    # independently — they each captured their own old_key_id in the
    # closure. Cancelling a prior timer would leave its key un-zeroed past
    # the grace window (committee v1 GPT-OSS MED-B).
    timer = threading.Timer(
        HMAC_KEY_ROTATION_GRACE_SECONDS, _zero_old_key_on_grace
    )
    timer.daemon = True
    runtime._rotation_timers.append(timer)
    timer.start()
    return new_session


def _bump_key_id_version(old_key_id: str) -> str:
    # e.g. tilth.session.<id>.hmac.v1 → tilth.session.<id>.hmac.v2
    parts = old_key_id.rsplit(".v", 1)
    if len(parts) == 2 and parts[1].isdigit():
        return f"{parts[0]}.v{int(parts[1]) + 1}"
    return f"{old_key_id}.rot.{secrets.token_hex(4)}"


# ---------------------------------------------------------------------------
# sign_health_tuple (M7)
# ---------------------------------------------------------------------------


def sign_health_tuple(session: Session, tuple_bytes: bytes) -> bytes:
    """M7 signing primitive used by Scout. [§4.6]

    Retrieves the HMAC key as :class:`SecretBytes`; the context manager
    zeros the mutable bytearray on exit, even on exception.
    """
    if not isinstance(tuple_bytes, (bytes, bytearray, memoryview)):
        raise TypeError(
            f"tuple_bytes must be bytes-like; got {type(tuple_bytes).__name__}"
        )
    runtime = _get_active_runtime()
    if runtime is None or runtime.session.session_id != session.session_id:
        raise SessionRuntimeNotBound(
            "F-SESSION-RUNTIME-NOT-BOUND: sign_health_tuple requires the "
            "active session"
        )
    with runtime.keystore.retrieve(session.hmac_key_id) as key:
        # Pass the underlying bytearray directly (via memoryview.obj, a
        # documented Python API) to stdlib hmac.new — avoids the
        # bytes(key.view()) immutable copy that would linger past the
        # SecretBytes context exit (committee v1 GPT-OSS HIGH-A). hmac.new
        # rejects memoryview in 3.14 but accepts bytearray; the bytearray is
        # the same buffer SecretBytes.__exit__ zeroes. Enforce the 32-byte
        # floor hmac_sha3_512 does so short-key callers fail loudly.
        key_view = key.view()
        if len(key_view) < 32:
            raise ValueError(
                f"session HMAC key must be >= 32 bytes; got {len(key_view)}"
            )
        key_buf = key_view.obj
        assert isinstance(key_buf, bytearray)
        return _stdlib_hmac.new(
            key_buf, bytes(tuple_bytes), _hashlib.sha3_512
        ).digest()


# ---------------------------------------------------------------------------
# Test-only helpers (NOT public API — used by tests/sovereignty/*)
# ---------------------------------------------------------------------------


def _record_checkpoint_state_for_tests(payload: dict[str, Any]) -> None:
    """Test hook — record the payload the checkpoint thread will flush."""
    runtime = _get_active_runtime()
    if runtime is None:
        raise SessionRuntimeNotBound("no active runtime")
    runtime._last_checkpoint_state = payload
