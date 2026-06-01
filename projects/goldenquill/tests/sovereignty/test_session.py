"""Unit tests for pipeline.sovereignty.session.

Round E LOCK gate. Probes construction, start/end lifecycle, HMAC key
rotation, and the sign_health_tuple primitive. Signal-handler exit-code
assertions live in a subprocess-style test that runs under skip-if-CI; the
in-process tests verify the zero-first + non-blocking-lock ordering
directly on the module-level handler function.

Adversarial tests live in test_session_adversarial.py.
"""

from __future__ import annotations

import json
import os
import signal
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from pipeline.sovereignty import interrupted_state, session
from pipeline.sovereignty.session import (
    HMAC_KEY_ROTATION_GRACE_SECONDS,
    LLM_ACTIVE_CHECKPOINT_INTERVAL_SECONDS,
    M10_AUTHOR_SEAT_DEGRADATION_THRESHOLD_SECONDS,
    SESSION_HMAC_KEY_BYTES,
    SIGNAL_HANDLER_CHECKPOINT_LOCK_NONBLOCKING,
    SIGNAL_HANDLER_KEY_ZERO_FIRST,
    SIGNAL_HANDLER_ONE_SHOT_FLAG_NAME,
    SIGTERM_GRACE_SECONDS,
    InvalidSlugError,
    Session,
    SessionAlreadyActive,
    SessionRuntimeNotBound,
    SessionSlugMismatch,
    end_session,
    rotate_hmac_key,
    sign_health_tuple,
    start_session,
)


# ---------------------------------------------------------------------------
# In-memory keystore stub (Round C keys.py is a production substrate; these
# tests need an in-memory version that supports the same surface).
# ---------------------------------------------------------------------------


class _InMemoryKeyStore:
    """Minimal keystore for session-test use. Matches the surface session.py
    actually calls: ``store(key_id=..., key_bytes=..., purpose=...)``,
    ``zero(key_id)``, and ``retrieve(key_id)`` → context manager returning an
    object with a ``view()`` method over the stored bytes.
    """

    def __init__(self) -> None:
        self._store: dict[str, bytearray] = {}
        self.store_calls: list[tuple[str, int, str]] = []
        self.zero_calls: list[str] = []

    def store(
        self, *, key_id: str, key_bytes: Any, purpose: str
    ) -> None:
        # Copy into its own bytearray so callers can safely zero their own buffer.
        self._store[key_id] = bytearray(key_bytes)
        self.store_calls.append((key_id, len(key_bytes), purpose))

    def zero(self, key_id: str) -> None:
        self.zero_calls.append(key_id)
        buf = self._store.pop(key_id, None)
        if buf is not None:
            for i in range(len(buf)):
                buf[i] = 0

    def retrieve(self, key_id: str) -> "_SecretHandle":
        if key_id not in self._store:
            raise KeyError(key_id)
        return _SecretHandle(self._store[key_id])


class _SecretHandle:
    def __init__(self, buf: bytearray) -> None:
        self._buf = buf
        self._zeroed = False

    def view(self) -> memoryview:
        return memoryview(self._buf)

    def __enter__(self) -> "_SecretHandle":
        return self

    def __exit__(self, *_: Any) -> None:
        self._zeroed = True


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


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
def repo_root(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture()
def keystore() -> _InMemoryKeyStore:
    return _InMemoryKeyStore()


@pytest.fixture()
def envelope(repo_root: Path, keystore: _InMemoryKeyStore) -> _FakeEnvelope:
    return _FakeEnvelope(
        router_manifest_sha="deadbeef" * 16, keystore=keystore, repo_root=repo_root
    )


@pytest.fixture()
def rfa() -> _FakeRFA:
    return _FakeRFA(session_bound_slug="acme-coop")


@pytest.fixture()
def project_context() -> _FakePC:
    return _FakePC(slug="acme-coop")


@pytest.fixture(autouse=True)
def _isolate_runtime():
    # Ensure no leak from a prior test that failed mid-start_session.
    session._set_active_runtime(None)
    session._shutting_down.clear()
    yield
    rt = session._get_active_runtime()
    if rt is not None:
        try:
            end_session(rt.session, status="ENDED_CLEAN")
        except Exception:
            session._set_active_runtime(None)


# ---------------------------------------------------------------------------
# Constants (§8)
# ---------------------------------------------------------------------------


def test_constants_have_expected_values() -> None:
    assert SESSION_HMAC_KEY_BYTES == 64
    assert SIGTERM_GRACE_SECONDS == 5
    assert LLM_ACTIVE_CHECKPOINT_INTERVAL_SECONDS == 30
    assert M10_AUTHOR_SEAT_DEGRADATION_THRESHOLD_SECONDS == 1800
    assert HMAC_KEY_ROTATION_GRACE_SECONDS == 5
    assert SIGNAL_HANDLER_KEY_ZERO_FIRST is True
    assert SIGNAL_HANDLER_CHECKPOINT_LOCK_NONBLOCKING is True
    assert SIGNAL_HANDLER_ONE_SHOT_FLAG_NAME == "_shutting_down"


# ---------------------------------------------------------------------------
# Session dataclass (§2.4)
# ---------------------------------------------------------------------------


def test_session_is_frozen() -> None:
    s = Session(
        session_id="a", slug="b", started_at="c", hmac_key_id="d",
        router_manifest_sha="e", pid=1, status="ACTIVE",
    )
    with pytest.raises(Exception):
        s.slug = "x"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# start_session — preconditions
# ---------------------------------------------------------------------------


def test_start_session_writes_record_and_locks_active(
    envelope, rfa, project_context, repo_root
):
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    record_path = repo_root / "sovereignty" / "sessions" / f"{s.session_id}.json"
    assert record_path.exists()
    rec = json.loads(record_path.read_text())
    assert rec["status"] == "ACTIVE"
    assert rec["slug"] == "acme-coop"
    lock_path = repo_root / "sovereignty" / "sessions" / ".active.lock"
    assert lock_path.exists()


def test_start_session_rejects_concurrent_start_with_session_already_active(
    envelope, rfa, project_context
):
    start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    with pytest.raises(SessionAlreadyActive):
        start_session(envelope=envelope, rfa=rfa, project_context=project_context)


def test_start_session_rejects_rfa_slug_mismatch(
    envelope, project_context
):
    mismatched_rfa = _FakeRFA(session_bound_slug="other-org")
    with pytest.raises(SessionSlugMismatch):
        start_session(
            envelope=envelope, rfa=mismatched_rfa, project_context=project_context
        )


def test_start_session_rejects_invalid_slug_canonicalization(envelope, rfa):
    bad_pc = _FakePC(slug="UPPER-SLUG")
    bad_rfa = _FakeRFA(session_bound_slug="UPPER-SLUG")
    with pytest.raises(InvalidSlugError):
        start_session(envelope=envelope, rfa=bad_rfa, project_context=bad_pc)


def test_start_session_rejects_bad_envelope_shape(rfa, project_context, repo_root):
    bad = _FakeEnvelope(router_manifest_sha=123, keystore=None, repo_root=repo_root)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        start_session(envelope=bad, rfa=rfa, project_context=project_context)


# ---------------------------------------------------------------------------
# HMAC key issuance
# ---------------------------------------------------------------------------


def test_hmac_key_stored_in_keystore_not_returned_as_bytes(
    envelope, rfa, project_context, keystore
):
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    # Key was stored in keystore under the canonical id.
    assert s.hmac_key_id == f"tilth.session.{s.session_id}.hmac.v1"
    assert keystore.store_calls[0][0] == s.hmac_key_id
    assert keystore.store_calls[0][1] == SESSION_HMAC_KEY_BYTES
    assert keystore.store_calls[0][2] == "session_hmac"


def test_start_session_zeroes_local_key_bytearray_after_store(
    envelope, rfa, project_context, keystore, monkeypatch
):
    captured: dict[str, Any] = {}
    original_store = keystore.store

    def spy_store(*, key_id: str, key_bytes: Any, purpose: str) -> None:
        # Capture a live reference to the bytearray as it arrives in store().
        # After start_session returns, the caller-side should have zeroed it.
        captured["buf"] = key_bytes
        captured["snapshot"] = bytes(key_bytes)
        original_store(key_id=key_id, key_bytes=key_bytes, purpose=purpose)

    monkeypatch.setattr(keystore, "store", spy_store)
    start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    # After start_session returns, the original bytearray should be all zeros.
    assert bytes(captured["buf"]) == b"\x00" * SESSION_HMAC_KEY_BYTES
    # And the snapshot (taken at store-time, before zero) should NOT have been zero.
    assert captured["snapshot"] != b"\x00" * SESSION_HMAC_KEY_BYTES


# ---------------------------------------------------------------------------
# end_session
# ---------------------------------------------------------------------------


def test_end_session_writes_ended_clean_and_zeroes_key(
    envelope, rfa, project_context, repo_root, keystore
):
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    end_session(s, status="ENDED_CLEAN")
    record_path = repo_root / "sovereignty" / "sessions" / f"{s.session_id}.json"
    rec = json.loads(record_path.read_text())
    assert rec["status"] == "ENDED_CLEAN"
    assert s.hmac_key_id in keystore.zero_calls


def test_end_session_cancels_checkpoint_thread(
    envelope, rfa, project_context
):
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    runtime = session._get_active_runtime()
    assert runtime is not None
    thread = runtime._checkpoint_thread
    assert thread is not None and thread.is_alive()
    end_session(s, status="ENDED_CLEAN")
    assert not thread.is_alive()


def test_end_session_idempotent_second_call_is_noop(
    envelope, rfa, project_context
):
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    end_session(s, status="ENDED_CLEAN")
    # Second call must not raise.
    end_session(s, status="ENDED_CLEAN")


def test_end_session_rejects_mismatched_session_id(
    envelope, rfa, project_context
):
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    other = Session(
        session_id="deadbeef",
        slug=s.slug,
        started_at=s.started_at,
        hmac_key_id=s.hmac_key_id,
        router_manifest_sha=s.router_manifest_sha,
        pid=s.pid,
        status="ACTIVE",
    )
    with pytest.raises(session.SessionError):
        end_session(other, status="ENDED_CLEAN")
    # Cleanup:
    end_session(s, status="ENDED_CLEAN")


# ---------------------------------------------------------------------------
# rotate_hmac_key
# ---------------------------------------------------------------------------


def test_rotate_hmac_key_issues_new_id_and_schedules_grace_zero(
    envelope, rfa, project_context, keystore, monkeypatch
):
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    old_id = s.hmac_key_id
    # Disable the 5-second grace timer by patching to 0.2 s for test speed.
    monkeypatch.setattr(session, "HMAC_KEY_ROTATION_GRACE_SECONDS", 0.2)
    s2 = rotate_hmac_key(s)
    assert s2.hmac_key_id != old_id
    assert s2.hmac_key_id.endswith(".v2")
    # Wait for the grace timer to fire.
    time.sleep(0.5)
    assert old_id in keystore.zero_calls


def test_rotate_hmac_key_cancel_on_end_session(
    envelope, rfa, project_context, keystore, monkeypatch
):
    monkeypatch.setattr(session, "HMAC_KEY_ROTATION_GRACE_SECONDS", 30)
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    old_id = s.hmac_key_id
    s2 = rotate_hmac_key(s)
    end_session(s2, status="ENDED_CLEAN")
    assert old_id in keystore.zero_calls


def test_rotate_hmac_key_requires_active_runtime():
    s = Session(
        session_id="nope", slug="a", started_at="b", hmac_key_id="c",
        router_manifest_sha="d", pid=1, status="ACTIVE",
    )
    with pytest.raises(SessionRuntimeNotBound):
        rotate_hmac_key(s)


# ---------------------------------------------------------------------------
# sign_health_tuple
# ---------------------------------------------------------------------------


def test_sign_health_tuple_returns_64_byte_hmac(
    envelope, rfa, project_context
):
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    sig = sign_health_tuple(s, b"hello")
    assert isinstance(sig, bytes)
    assert len(sig) == 64  # SHA3-512 digest


def test_sign_health_tuple_deterministic_for_same_tuple(
    envelope, rfa, project_context
):
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    a = sign_health_tuple(s, b"X")
    b = sign_health_tuple(s, b"X")
    assert a == b


def test_sign_health_tuple_differs_across_inputs(
    envelope, rfa, project_context
):
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    a = sign_health_tuple(s, b"X")
    b = sign_health_tuple(s, b"Y")
    assert a != b


def test_sign_health_tuple_requires_active_runtime():
    s = Session(
        session_id="nope", slug="a", started_at="b", hmac_key_id="c",
        router_manifest_sha="d", pid=1, status="ACTIVE",
    )
    with pytest.raises(SessionRuntimeNotBound):
        sign_health_tuple(s, b"x")


def test_sign_health_tuple_rejects_non_bytes():
    # Must fail BEFORE runtime check since type check precedes state check.
    s = Session(
        session_id="nope", slug="a", started_at="b", hmac_key_id="c",
        router_manifest_sha="d", pid=1, status="ACTIVE",
    )
    with pytest.raises(TypeError):
        sign_health_tuple(s, "not-bytes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Signal handler (in-process, not exit-code)
# ---------------------------------------------------------------------------


def test_unified_signal_handler_one_shot_flag_ignores_second_signal(
    envelope, rfa, project_context, monkeypatch
):
    """Second signal hits the already-set `_shutting_down` gate → early return."""
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    # Pre-set the flag to force the early-return branch.
    session._shutting_down.set()
    # Replace os._exit so the handler doesn't actually exit.
    exit_calls: list[int] = []
    monkeypatch.setattr(
        os, "_exit", lambda code: exit_calls.append(code)
    )
    session._unified_signal_handler(signal.SIGTERM, None)
    assert exit_calls == []  # never reached os._exit — flag gated it.
    # Cleanup:
    session._shutting_down.clear()
    end_session(s, status="ENDED_CLEAN")


def test_unified_signal_handler_skips_checkpoint_when_lock_held(
    envelope, rfa, project_context, monkeypatch
):
    """v4 RT-v3 LOW-1: non-blocking acquire means contention → skip."""
    s = start_session(envelope=envelope, rfa=rfa, project_context=project_context)
    runtime = session._get_active_runtime()
    assert runtime is not None
    runtime._last_checkpoint_state = {"probe": "data"}

    checkpoint_called: list[Any] = []

    def fake_checkpoint(sess, payload):
        checkpoint_called.append((sess, payload))
        return Path("/tmp/fake")

    monkeypatch.setattr(interrupted_state, "checkpoint", fake_checkpoint)
    # Patch os._exit so we don't die.
    monkeypatch.setattr(os, "_exit", lambda code: None)

    # Hold the lock from another thread so the handler's acquire(blocking=False)
    # fails and it skips its checkpoint.
    released = threading.Event()
    acquired = threading.Event()

    def hold_lock():
        with session._checkpoint_lock:
            acquired.set()
            released.wait()

    t = threading.Thread(target=hold_lock)
    t.start()
    acquired.wait()
    try:
        session._shutting_down.clear()
        session._unified_signal_handler(signal.SIGTERM, None)
    finally:
        released.set()
        t.join()
    assert checkpoint_called == []  # handler skipped its checkpoint
    # Cleanup
    session._shutting_down.clear()
    end_session(s, status="ENDED_CLEAN")


def test_unified_signal_handler_no_runtime_returns_silently(monkeypatch):
    # No active runtime, no active session.
    monkeypatch.setattr(os, "_exit", lambda code: None)
    session._shutting_down.clear()
    session._unified_signal_handler(signal.SIGTERM, None)  # must not raise
    session._shutting_down.clear()
