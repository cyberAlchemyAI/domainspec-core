"""Unit tests for pipeline.sovereignty.interrupted_state.

Round E LOCK gate. Probes checkpoint emission (§3.9.1 Vault boundary),
detect_interrupted, resume_or_discard policies, and the Phase-0 default
local fallback (tmp+rename with v3 st_dev double-check).

E-007 discipline: every monkeypatch targets names imported into the module
under test (interrupted_state), not source modules.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from pipeline.sovereignty import interrupted_state
from pipeline.sovereignty.interrupted_state import (
    CrossFilesystemRename,
    IntegrityError,
    InterruptedStateInvalid,
    OperatorDecisionRequired,
    checkpoint,
    detect_interrupted,
    register_resume_validator,
    register_vault_commit_hook,
    resume_or_discard,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@dataclass
class _FakeSession:
    session_id: str = "abc123"
    slug: str = "acme-coop"
    started_at: str = "2026-04-19T00:00:00+00:00"
    hmac_key_id: str = "tilth.session.abc123.hmac.v1"
    router_manifest_sha: str = "deadbeef" * 16
    pid: int = 1234
    status: str = "ACTIVE"
    interrupted_payload_path: str | None = None


@pytest.fixture()
def fake_session(tmp_path: Path) -> _FakeSession:
    s = _FakeSession()
    # Attach _repo_root so checkpoint can route to the default fallback.
    s._repo_root = tmp_path  # type: ignore[attr-defined]
    return s


@pytest.fixture(autouse=True)
def _clear_hooks_and_validators():
    interrupted_state._unlock_vault_commit_hook_for_tests()
    prior = register_vault_commit_hook(None)
    interrupted_state._clear_resume_validators()
    yield
    interrupted_state._unlock_vault_commit_hook_for_tests()
    register_vault_commit_hook(prior)
    interrupted_state._clear_resume_validators()


# ---------------------------------------------------------------------------
# Vault-hook registration (§3.9.1)
# ---------------------------------------------------------------------------


def test_register_vault_commit_hook_returns_prior_for_restore():
    def hook_a(**kw: Any) -> Path:
        return Path("/a")

    def hook_b(**kw: Any) -> Path:
        return Path("/b")

    assert register_vault_commit_hook(hook_a) is None
    assert register_vault_commit_hook(hook_b) is hook_a
    assert register_vault_commit_hook(None) is hook_b


def test_no_hook_registered_falls_back_to_default_local_vault_commit(
    fake_session, tmp_path
):
    # With no hook, the checkpoint path should write via _default_local_vault_commit.
    returned = checkpoint(fake_session, {"probe": 1})
    assert returned == tmp_path / "sovereignty" / "sessions" / "abc123.json"
    assert returned.exists()


def test_checkpoint_emits_vault_commit_call_not_direct_filesystem_write(
    fake_session, tmp_path
):
    """§3.9.1 required test — hook receives bytes + manifest, not a path."""
    captured: list[dict[str, Any]] = []

    def spy_hook(
        *, org_slug: str, sub_path: str, payload_bytes: bytes,
        manifest: dict[str, Any],
    ) -> Path:
        captured.append(
            {
                "org_slug": org_slug,
                "sub_path": sub_path,
                "payload_bytes": payload_bytes,
                "manifest": manifest,
            }
        )
        return tmp_path / "fake_vault_return.json"

    register_vault_commit_hook(spy_hook)
    checkpoint(fake_session, {"probe": 42})
    assert len(captured) == 1
    assert captured[0]["org_slug"] == "acme-coop"
    assert captured[0]["sub_path"] == "runs/abc123/interrupted/"
    assert isinstance(captured[0]["payload_bytes"], bytes)
    assert captured[0]["manifest"]["kind"] == "session_interrupted"
    assert captured[0]["manifest"]["sha3_512"]
    # Filesystem write must NOT have happened — only the hook was called.
    sessions_dir = tmp_path / "sovereignty" / "sessions"
    assert not sessions_dir.exists() or not any(
        p.name == "abc123.json" for p in sessions_dir.glob("*")
    )


def test_checkpoint_path_return_is_read_only_handle(fake_session, tmp_path):
    """§3.9.1 required test — the returned Path is what the hook yielded."""
    def hook(**kw: Any) -> Path:
        return Path("/vault/readonly/handle.json")

    register_vault_commit_hook(hook)
    got = checkpoint(fake_session, {"probe": 1})
    assert got == Path("/vault/readonly/handle.json")


def test_checkpoint_hook_must_return_path_raises_on_non_path(fake_session):
    def bad_hook(**kw: Any) -> Any:
        return "not a Path"

    register_vault_commit_hook(bad_hook)
    with pytest.raises(IntegrityError):
        checkpoint(fake_session, {"probe": 1})


def test_checkpoint_missing_repo_root_raises_integrity(tmp_path):
    sess = _FakeSession()  # no _repo_root
    with pytest.raises(IntegrityError):
        checkpoint(sess, {"probe": 1})


def test_checkpoint_non_dict_payload_raises_type_error(fake_session):
    with pytest.raises(TypeError):
        checkpoint(fake_session, "not-a-dict")  # type: ignore[arg-type]


def test_atomic_flush_integrity_error_before_vault_commit_raises_not_f_vault(
    fake_session, tmp_path, monkeypatch
):
    """§3.9.1 required test — §1-internal integrity error does NOT call §2."""
    vault_called: list[Any] = []

    def hook(**kw: Any) -> Path:
        vault_called.append(kw)
        return tmp_path / "x.json"

    register_vault_commit_hook(hook)

    # Force the integrity re-check to fail by patching the second sha3.
    from pipeline.sovereignty import interrupted_state as _mod

    call_count = {"n": 0}
    original = _mod._sha3_512_hex

    def tampered(data: bytes) -> str:
        call_count["n"] += 1
        if call_count["n"] == 2:
            return "ff" * 64  # arbitrary non-matching hash
        return original(data)

    monkeypatch.setattr(_mod, "_sha3_512_hex", tampered)
    with pytest.raises(IntegrityError):
        checkpoint(fake_session, {"probe": 1})
    assert vault_called == []  # hook NEVER invoked


def test_checkpoint_payload_canonical_json_sorted_keys(
    fake_session, tmp_path
):
    captured_bytes: list[bytes] = []

    def hook(
        *, org_slug: str, sub_path: str, payload_bytes: bytes,
        manifest: dict[str, Any],
    ) -> Path:
        captured_bytes.append(payload_bytes)
        return tmp_path / "x.json"

    register_vault_commit_hook(hook)
    checkpoint(fake_session, {"z_last": 1, "a_first": 2})
    # Canonical JSON → keys alphabetical. Round-trip parse must succeed.
    decoded = json.loads(captured_bytes[0].decode("utf-8"))
    assert decoded["interrupted_payload"]["a_first"] == 2
    # Sorted keys: "a_first" must precede "z_last" in raw bytes.
    raw = captured_bytes[0].decode()
    assert raw.index('"a_first"') < raw.index('"z_last"')


def test_checkpoint_manifest_contains_sha3_512_of_payload(
    fake_session, tmp_path
):
    captured: list[dict[str, Any]] = []

    def hook(
        *, org_slug: str, sub_path: str, payload_bytes: bytes,
        manifest: dict[str, Any],
    ) -> Path:
        captured.append({"bytes": payload_bytes, "manifest": manifest})
        return tmp_path / "x.json"

    register_vault_commit_hook(hook)
    checkpoint(fake_session, {"p": 1})
    import hashlib
    expected = hashlib.sha3_512(captured[0]["bytes"]).hexdigest()
    assert captured[0]["manifest"]["sha3_512"] == expected


# ---------------------------------------------------------------------------
# Default local Vault-commit fallback (Phase-0)
# ---------------------------------------------------------------------------


def test_default_local_vault_commit_performs_tmp_rename(
    fake_session, tmp_path
):
    # No hook registered → default fallback.
    p = checkpoint(fake_session, {"probe": 7})
    assert p.exists()
    record = json.loads(p.read_text())
    assert record["status"] == "INTERRUPTED"
    assert record["interrupted_payload"] == {"probe": 7}


def test_default_local_vault_commit_pre_create_st_dev_mismatch_raises_f_iso_06(
    fake_session, tmp_path, monkeypatch
):
    """Monkey-patch os.stat in the interrupted_state module to return divergent st_dev."""
    from pipeline.sovereignty import interrupted_state as _mod
    import os as _os

    original_stat = _os.stat

    def fake_stat(path, *args, **kwargs):
        r = original_stat(path, *args, **kwargs)

        class _St:
            st_dev = 99999
            def __init__(self, real): self._r = real
            def __getattr__(self, n): return getattr(self._r, n)

        return _St(r)

    monkeypatch.setattr(_mod.os, "stat", fake_stat)
    # Now both parents report st_dev=99999 so Check A would PASS (equal).
    # To force a mismatch, vary the return by path.
    call_count = {"n": 0}

    def flip_stat(path, *args, **kwargs):
        call_count["n"] += 1
        r = original_stat(path, *args, **kwargs)

        class _St:
            def __init__(self, real, dev): self._r = real; self.st_dev = dev
            def __getattr__(self, n): return getattr(self._r, n)

        # First call (tmp_parent) gets dev=1, second (final_parent) gets dev=2.
        dev = 1 if call_count["n"] % 2 == 1 else 2
        return _St(r, dev)

    monkeypatch.setattr(_mod.os, "stat", flip_stat)
    with pytest.raises(CrossFilesystemRename):
        checkpoint(fake_session, {"probe": 1})


def test_default_local_vault_commit_post_create_st_dev_mismatch_raises_f_iso_06(
    fake_session, tmp_path, monkeypatch
):
    """Pre-check passes; post-check (fstat vs final_parent stat) mismatches."""
    from pipeline.sovereignty import interrupted_state as _mod
    import os as _os

    original_stat = _os.stat
    original_fstat = _os.fstat

    def real_stat(*a, **k):
        return original_stat(*a, **k)

    class _St:
        def __init__(self, real, dev): self._r = real; self.st_dev = dev
        def __getattr__(self, n): return getattr(self._r, n)

    # Force fstat to return a different st_dev than real_stat(final_parent).
    def divergent_fstat(fd):
        r = original_fstat(fd)
        return _St(r, 9999)

    monkeypatch.setattr(_mod.os, "fstat", divergent_fstat)
    with pytest.raises(CrossFilesystemRename):
        checkpoint(fake_session, {"probe": 1})


def test_default_local_vault_commit_post_rename_is_atomic(
    fake_session, tmp_path
):
    """After checkpoint returns, either ONLY the final file exists (no tmp)."""
    checkpoint(fake_session, {"probe": 1})
    sessions_dir = tmp_path / "sovereignty" / "sessions"
    tmps = list(sessions_dir.glob("*.tmp.*"))
    assert tmps == []
    final = sessions_dir / "abc123.json"
    assert final.exists()


# ---------------------------------------------------------------------------
# detect_interrupted
# ---------------------------------------------------------------------------


def _write_session_record(
    repo_root: Path, session_id: str, status: str, started_at: str
) -> None:
    sessions_dir = repo_root / "sovereignty" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    rec = {
        "session_id": session_id,
        "slug": "acme-coop",
        "started_at": started_at,
        "hmac_key_id": f"tilth.session.{session_id}.hmac.v1",
        "router_manifest_sha": "ab" * 64,
        "pid": 1234,
        "status": status,
    }
    (sessions_dir / f"{session_id}.json").write_text(json.dumps(rec))


def test_detect_interrupted_returns_newest_interrupted_session(tmp_path):
    _write_session_record(tmp_path, "old", "INTERRUPTED", "2026-04-19T01:00:00+00:00")
    _write_session_record(tmp_path, "new", "INTERRUPTED", "2026-04-19T09:00:00+00:00")
    _write_session_record(tmp_path, "ended", "ENDED_CLEAN", "2026-04-19T10:00:00+00:00")
    got = detect_interrupted(tmp_path)
    assert got is not None
    assert got["session_id"] == "new"


def test_detect_interrupted_returns_none_when_no_interrupted(tmp_path):
    _write_session_record(tmp_path, "a", "ENDED_CLEAN", "2026-04-19T01:00:00+00:00")
    assert detect_interrupted(tmp_path) is None


def test_detect_interrupted_returns_none_when_no_dir(tmp_path):
    assert detect_interrupted(tmp_path) is None


def test_detect_interrupted_rejects_non_path():
    with pytest.raises(TypeError):
        detect_interrupted("/tmp")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# resume_or_discard
# ---------------------------------------------------------------------------


def test_prompt_policy_raises_operator_decision_required(tmp_path):
    s = _FakeSession()
    s._repo_root = tmp_path  # type: ignore[attr-defined]
    with pytest.raises(OperatorDecisionRequired):
        resume_or_discard(s, policy="prompt")


def test_resume_returns_payload_when_validators_pass(tmp_path, fake_session):
    checkpoint(fake_session, {"probe": 9})
    payload = resume_or_discard(fake_session, policy="resume")
    assert payload == {"probe": 9}


def test_resume_invokes_registered_validator(tmp_path, fake_session):
    checkpoint(fake_session, {"probe": 9})
    captured: list[dict[str, Any]] = []

    def validator(record: dict[str, Any]) -> None:
        captured.append(record)

    register_resume_validator("rfa_hash_check", validator)
    resume_or_discard(fake_session, policy="resume")
    assert len(captured) == 1
    assert captured[0]["session_id"] == "abc123"


def test_resume_raises_interrupted_state_invalid_on_validator_rejection(
    fake_session,
):
    checkpoint(fake_session, {"probe": 1})

    def rejecting_validator(record: dict[str, Any]) -> None:
        raise ValueError("hash mismatch")

    register_resume_validator("bad", rejecting_validator)
    with pytest.raises(InterruptedStateInvalid):
        resume_or_discard(fake_session, policy="resume")


def test_resume_raises_invalid_when_record_has_no_payload(tmp_path, fake_session):
    # Write a record WITHOUT interrupted_payload.
    sessions_dir = tmp_path / "sovereignty" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    (sessions_dir / "abc123.json").write_text(
        json.dumps({
            "session_id": "abc123", "slug": "acme-coop",
            "started_at": "x", "hmac_key_id": "y",
            "router_manifest_sha": "z", "pid": 1, "status": "ACTIVE",
        })
    )
    with pytest.raises(InterruptedStateInvalid):
        resume_or_discard(fake_session, policy="resume")


def test_discard_rewrites_ended_clean_and_clears_payload(fake_session, tmp_path):
    checkpoint(fake_session, {"probe": 1})
    result = resume_or_discard(fake_session, policy="discard")
    assert result is None
    rec = json.loads(
        (tmp_path / "sovereignty" / "sessions" / "abc123.json").read_text()
    )
    assert rec["status"] == "ENDED_CLEAN"
    assert "interrupted_payload" not in rec


def test_resume_rejects_bad_policy(fake_session):
    with pytest.raises(ValueError):
        resume_or_discard(fake_session, policy="nonsense")


def test_resume_requires_repo_root_via_kwarg_or_attr():
    s = _FakeSession()  # no _repo_root
    with pytest.raises(IntegrityError):
        resume_or_discard(s, policy="resume")


def test_resume_uses_repo_root_kwarg_override(fake_session, tmp_path):
    checkpoint(fake_session, {"probe": 7})
    # Clear attr to test kwarg path.
    delattr(fake_session, "_repo_root")
    payload = resume_or_discard(fake_session, policy="resume", repo_root=tmp_path)
    assert payload == {"probe": 7}
