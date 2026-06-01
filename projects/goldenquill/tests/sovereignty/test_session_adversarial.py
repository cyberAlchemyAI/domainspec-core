"""Adversarial probes for pipeline.sovereignty.session + interrupted_state.

Round E adversarial gate. Exercises the attacker-model clauses stated in
§4.5 v3/v4 + §4.6 M7 + §6 F-SESSION-*. Per Autonomy Rule 2 and E-007..E-010
engineering-review lessons, every monkey-patch targets names imported INTO
the module-under-test.
"""

from __future__ import annotations

import multiprocessing
import os
import signal
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from pipeline.sovereignty import interrupted_state, session
from pipeline.sovereignty.session import (
    HMAC_KEY_ROTATION_GRACE_SECONDS,
    Session,
    SessionAlreadyActive,
    SessionRuntimeNotBound,
    end_session,
    rotate_hmac_key,
    sign_health_tuple,
    start_session,
)


# ---------------------------------------------------------------------------
# In-memory keystore + envelopes (mirrors test_session.py shape)
# ---------------------------------------------------------------------------


class _InMemoryKeyStore:
    def __init__(self) -> None:
        self._store: dict[str, bytearray] = {}
        self.zero_calls: list[str] = []

    def store(self, *, key_id: str, key_bytes: Any, purpose: str) -> None:
        self._store[key_id] = bytearray(key_bytes)

    def zero(self, key_id: str) -> None:
        self.zero_calls.append(key_id)
        buf = self._store.pop(key_id, None)
        if buf is not None:
            for i in range(len(buf)):
                buf[i] = 0

    def retrieve(self, key_id: str) -> "_SecretHandle":
        if key_id not in self._store:
            raise KeyError(f"F-KEY-03 or key absent: {key_id}")
        return _SecretHandle(self._store[key_id])


class _SecretHandle:
    def __init__(self, buf: bytearray) -> None:
        self._buf = buf

    def view(self) -> memoryview:
        return memoryview(self._buf)

    def __enter__(self) -> "_SecretHandle":
        return self

    def __exit__(self, *_: Any) -> None:
        pass


@dataclass
class _FakeEnvelope:
    router_manifest_sha: str
    keystore: Any
    repo_root: Path


@dataclass
class _FakeRFA:
    session_bound_slug: str


@dataclass
class _FakePC:
    slug: str


@pytest.fixture()
def envelope(tmp_path):
    return _FakeEnvelope(
        router_manifest_sha="ab" * 64,
        keystore=_InMemoryKeyStore(),
        repo_root=tmp_path,
    )


@pytest.fixture()
def rfa():
    return _FakeRFA(session_bound_slug="acme-coop")


@pytest.fixture()
def project_context():
    return _FakePC(slug="acme-coop")


@pytest.fixture(autouse=True)
def _isolate_runtime():
    session._set_active_runtime(None)
    session._shutting_down.clear()
    interrupted_state._unlock_vault_commit_hook_for_tests()
    interrupted_state.register_vault_commit_hook(None)
    yield
    rt = session._get_active_runtime()
    if rt is not None:
        try:
            end_session(rt.session, status="ENDED_CLEAN")
        except Exception:
            session._set_active_runtime(None)
    session._shutting_down.clear()
    interrupted_state._unlock_vault_commit_hook_for_tests()
    interrupted_state.register_vault_commit_hook(None)


# ---------------------------------------------------------------------------
# Active-lock contention
# ---------------------------------------------------------------------------


def _child_try_acquire_active_lock(repo_root_str: str, result_queue):
    """Helper for cross-process lock contention."""
    from pipeline.sovereignty import session as _s

    try:
        fd = _s._acquire_active_lock(Path(repo_root_str))
        result_queue.put(("got", fd))
    except _s.SessionAlreadyActive as e:
        result_queue.put(("blocked", str(e)))


def test_adv_two_processes_race_for_active_lock_only_one_wins(
    envelope, rfa, project_context, tmp_path
):
    """A second process trying to bind the same .active.lock must get SessionAlreadyActive."""
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    # Spawn a child process that tries to acquire the same active lock.
    ctx = multiprocessing.get_context("spawn")
    q = ctx.Queue()
    p = ctx.Process(target=_child_try_acquire_active_lock, args=(str(tmp_path), q))
    p.start()
    p.join(timeout=10)
    assert not p.is_alive()
    outcome = q.get(timeout=2)
    assert outcome[0] == "blocked"
    # Cleanup
    end_session(s, status="ENDED_CLEAN")


def test_adv_second_start_session_while_active_raises(
    envelope, rfa, project_context
):
    """In-process second start_session without end_session must reject."""
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    with pytest.raises(SessionAlreadyActive):
        start_session(
            envelope=envelope, rfa=rfa, project_context=project_context
        )
    end_session(s, status="ENDED_CLEAN")


# ---------------------------------------------------------------------------
# Signal handler — zero-first ordering
# ---------------------------------------------------------------------------


def test_adv_signal_handler_zeroes_hmac_buffer_before_any_io(
    envelope, rfa, project_context, monkeypatch
):
    """Zero-first (v2 ordering). Patch checkpoint to assert the buffer is
    already zero BEFORE any I/O branch of the handler runs.
    """
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    runtime = session._get_active_runtime()
    assert runtime is not None
    # Attach a fake HMAC buffer to the runtime (start_session already zeroed
    # the real one, but the field is expected to be populated during active
    # LLM signing in production; we simulate it here).
    runtime._hmac_key_buffer = bytearray(b"\xff" * 64)
    runtime._last_checkpoint_state = {"x": 1}

    captured_state: list[bytes] = []

    def observing_checkpoint(sess, payload):
        # At this point the handler has already hit Step 1 (zero key) and is
        # in Step 2 (checkpoint). The buffer should already be zero.
        captured_state.append(bytes(runtime._hmac_key_buffer))
        return Path("/tmp/x")

    monkeypatch.setattr(interrupted_state, "checkpoint", observing_checkpoint)
    monkeypatch.setattr(os, "_exit", lambda code: None)
    session._shutting_down.clear()
    session._unified_signal_handler(signal.SIGTERM, None)
    # The HMAC buffer should be zero at checkpoint invocation time.
    assert captured_state == [b"\x00" * 64]
    session._shutting_down.clear()
    end_session(s, status="ENDED_CLEAN")


def test_adv_signal_handler_clears_watchdog_when_exit_is_monkeypatched(
    envelope, rfa, project_context, monkeypatch
):
    """In-process tests monkeypatch os._exit; the armed SIGALRM must not leak."""
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    runtime = session._get_active_runtime()
    assert runtime is not None

    calls: list[tuple[str, int]] = []

    def fake_alarm(seconds: int) -> int:
        calls.append(("alarm", seconds))
        return 0

    monkeypatch.setattr(signal, "alarm", fake_alarm)
    monkeypatch.setattr(os, "_exit", lambda code: None)
    session._shutting_down.clear()
    session._unified_signal_handler(signal.SIGTERM, None)

    assert calls[0] == ("alarm", session.SIGTERM_GRACE_SECONDS)
    assert calls[-1] == ("alarm", 0)
    session._shutting_down.clear()
    end_session(s, status="ENDED_CLEAN")


def test_adv_signal_handler_calls_keystore_zero_even_when_checkpoint_lock_contended(
    envelope, rfa, project_context, monkeypatch
):
    """v4 — handler skips checkpoint on lock contention but STILL zeroes keystore."""
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    runtime = session._get_active_runtime()
    assert runtime is not None
    runtime._last_checkpoint_state = {"x": 1}

    monkeypatch.setattr(os, "_exit", lambda code: None)

    # Hold the checkpoint_lock from a helper thread.
    acquired = threading.Event()
    release = threading.Event()

    def hold():
        with session._checkpoint_lock:
            acquired.set()
            release.wait()

    t = threading.Thread(target=hold)
    t.start()
    acquired.wait()
    try:
        session._shutting_down.clear()
        session._unified_signal_handler(signal.SIGTERM, None)
    finally:
        release.set()
        t.join()
    # Keystore zero DID run despite lock contention.
    assert s.hmac_key_id in envelope.keystore.zero_calls
    session._shutting_down.clear()
    # Cleanup
    end_session(s, status="ENDED_CLEAN")


def test_adv_second_sigterm_during_handler_is_noop(monkeypatch):
    """One-shot flag: second SIGTERM must early-return. Closes RT-v2 LOW-2."""
    exits: list[int] = []
    monkeypatch.setattr(os, "_exit", lambda code: exits.append(code))

    # Pre-set the flag (simulates "another handler is already running").
    session._shutting_down.set()
    session._unified_signal_handler(signal.SIGTERM, None)
    assert exits == []  # Early-returned before os._exit.
    session._shutting_down.clear()


# ---------------------------------------------------------------------------
# HMAC key lifecycle adversarial
# ---------------------------------------------------------------------------


def test_adv_rotation_then_end_session_zeroes_both_keys(
    envelope, rfa, project_context, monkeypatch
):
    """Grace-timer cancellation on end_session must still zero the old key."""
    monkeypatch.setattr(session, "HMAC_KEY_ROTATION_GRACE_SECONDS", 60)
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    old_id = s.hmac_key_id
    s2 = rotate_hmac_key(s)
    # end_session before grace elapses; must still zero old_id.
    end_session(s2, status="ENDED_CLEAN")
    assert old_id in envelope.keystore.zero_calls
    assert s2.hmac_key_id in envelope.keystore.zero_calls


def test_adv_sign_health_tuple_after_end_session_raises_runtime_not_bound(
    envelope, rfa, project_context
):
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    end_session(s, status="ENDED_CLEAN")
    with pytest.raises(SessionRuntimeNotBound):
        sign_health_tuple(s, b"x")


def test_adv_sign_health_tuple_with_unrelated_session_rejected(
    envelope, rfa, project_context
):
    """A stale Session instance from a prior end_session cannot sign against
    a DIFFERENT active session — session_id binds."""
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    intruder = Session(
        session_id="deadbeef", slug=s.slug, started_at=s.started_at,
        hmac_key_id=s.hmac_key_id, router_manifest_sha=s.router_manifest_sha,
        pid=s.pid, status="ACTIVE",
    )
    with pytest.raises(SessionRuntimeNotBound):
        sign_health_tuple(intruder, b"x")
    end_session(s, status="ENDED_CLEAN")


# ---------------------------------------------------------------------------
# Cross-fs rename adversarial
# ---------------------------------------------------------------------------


def test_adv_cross_fs_rename_mid_write_raises_f_iso_06_in_checkpoint(
    envelope, rfa, project_context, monkeypatch, tmp_path
):
    """Simulate a mid-write remount: fstat returns a different st_dev than
    the final_parent stat. Post-creation check must raise F-ISO-06 and the
    write must NOT land on disk.
    """
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    runtime = session._get_active_runtime()
    runtime._last_checkpoint_state = {"x": 1}

    from pipeline.sovereignty import interrupted_state as _mod
    import os as _os

    original_fstat = _os.fstat

    class _St:
        def __init__(self, r, dev):
            self._r = r
            self.st_dev = dev

        def __getattr__(self, n):
            return getattr(self._r, n)

    monkeypatch.setattr(
        _mod.os, "fstat", lambda fd: _St(original_fstat(fd), 0xDEADBEEF)
    )
    with pytest.raises(interrupted_state.CrossFilesystemRename):
        interrupted_state.checkpoint(s, {"x": 1})
    # Undo fstat patch BEFORE end_session — otherwise fixture teardown's
    # end_session would hit the same st_dev-mismatch trap.
    monkeypatch.undo()
    # Final session record must still be the ACTIVE version.
    record_path = (
        tmp_path / "sovereignty" / "sessions" / f"{s.session_id}.json"
    )
    import json as _json

    rec = _json.loads(record_path.read_text())
    assert rec["status"] == "ACTIVE"
    end_session(s, status="ENDED_CLEAN")


# ---------------------------------------------------------------------------
# Vault hook adversarial — integrity error NEVER calls §2
# ---------------------------------------------------------------------------


def test_adv_integrity_error_never_calls_vault_hook(
    envelope, rfa, project_context, monkeypatch
):
    """If §1-internal integrity re-check fails, §2 Vault MUST NOT be called."""
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    vault_calls: list[Any] = []

    def bad_hook(**kw: Any) -> Path:
        vault_calls.append(kw)
        return Path("/x")

    interrupted_state.register_vault_commit_hook(bad_hook)
    # Force integrity check to fail.
    call_count = {"n": 0}
    original = interrupted_state._sha3_512_hex

    def tampered(data: bytes) -> str:
        call_count["n"] += 1
        return ("ff" * 64) if call_count["n"] == 2 else original(data)

    monkeypatch.setattr(interrupted_state, "_sha3_512_hex", tampered)
    with pytest.raises(interrupted_state.IntegrityError):
        interrupted_state.checkpoint(s, {"x": 1})
    assert vault_calls == []
    interrupted_state.register_vault_commit_hook(None)
    end_session(s, status="ENDED_CLEAN")


def test_adv_vault_hook_raises_propagates_not_swallowed(
    envelope, rfa, project_context, monkeypatch
):
    """F-VAULT-COMMIT-* style failures from the hook must propagate, not be
    swallowed by the integrity layer.
    """
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)

    class FVaultCommitFailed(RuntimeError):
        pass

    def failing_hook(**kw: Any) -> Path:
        raise FVaultCommitFailed("F-VAULT-COMMIT-CAS-MISMATCH")

    interrupted_state.register_vault_commit_hook(failing_hook)
    with pytest.raises(FVaultCommitFailed):
        interrupted_state.checkpoint(s, {"x": 1})
    interrupted_state.register_vault_commit_hook(None)
    end_session(s, status="ENDED_CLEAN")


# ---------------------------------------------------------------------------
# Committee v1 fix-verification probes
# ---------------------------------------------------------------------------


def test_adv_rapid_rotations_every_old_key_zeroed_after_own_grace(
    envelope, rfa, project_context, monkeypatch
):
    """Committee v1 GPT-OSS MED-B closure.

    Three rapid rotations within the 5s grace window must schedule three
    independent timers; each must zero its own old key id. Previously the
    single-slot ``_rotation_timer`` cancelled prior timers, leaking older
    keys past the grace window.
    """
    # Shrink the grace window for the test to avoid a 15s wait.
    monkeypatch.setattr(session, "HMAC_KEY_ROTATION_GRACE_SECONDS", 0.05)
    s0 = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    s1 = rotate_hmac_key(s0)
    s2 = rotate_hmac_key(s1)
    s3 = rotate_hmac_key(s2)
    # Wait for all three independent grace timers to fire.
    time.sleep(0.25)
    ks = envelope.keystore
    # Every old key id (s0, s1, s2 hmac key ids) must have been zero()'d
    # by its own grace timer — no prior key may linger.
    assert s0.hmac_key_id in ks.zero_calls
    assert s1.hmac_key_id in ks.zero_calls
    assert s2.hmac_key_id in ks.zero_calls
    end_session(s3, status="ENDED_CLEAN")


def test_adv_vault_hook_registration_after_lock_raises(
    envelope, rfa, project_context
):
    """Committee v1 GPT-OSS HIGH-C closure.

    Section 2 Vault calls lock_vault_commit_hook at boot; subsequent
    register calls must raise VaultCommitHookLocked.
    """
    def legit_hook(**kw: Any) -> Path:
        return Path("/legit")

    def hostile_hook(**kw: Any) -> Path:
        return Path("/hostile")

    interrupted_state.register_vault_commit_hook(legit_hook)
    interrupted_state.lock_vault_commit_hook()
    with pytest.raises(interrupted_state.VaultCommitHookLocked):
        interrupted_state.register_vault_commit_hook(hostile_hook)
    # Current hook is still the legit one — lock preserved it.
    assert interrupted_state._current_vault_commit_hook() is legit_hook


def test_adv_sign_health_tuple_does_not_materialize_bytes_key_copy(
    envelope, rfa, project_context, monkeypatch
):
    """Committee v1 GPT-OSS HIGH-A closure.

    sign_health_tuple must pass the SecretBytes memoryview directly to
    ``hmac.new``; it must NOT materialize an immutable ``bytes`` copy of
    the key, which would linger past the SecretBytes context exit.
    """
    observed_key_types: list[str] = []
    real_new = session._stdlib_hmac.new

    def spy_new(key, msg, digestmod):
        observed_key_types.append(type(key).__name__)
        return real_new(bytes(key) if not isinstance(key, (bytes, bytearray)) else key, msg, digestmod)

    monkeypatch.setattr(session._stdlib_hmac, "new", spy_new)
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    try:
        sig = sign_health_tuple(s, b"probe-tuple-bytes")
        assert isinstance(sig, bytes) and len(sig) == 64
        # Key must NOT be a `bytes` object (which would indicate the prior
        # leak pattern). Acceptable types: memoryview (direct SecretBytes
        # view) or bytearray (pre-conversion within SecretBytes). `bytes`
        # would indicate an immutable persistent copy.
        assert "bytes" not in observed_key_types, (
            f"sign_health_tuple leaked key as bytes: observed={observed_key_types}"
        )
    finally:
        end_session(s, status="ENDED_CLEAN")
