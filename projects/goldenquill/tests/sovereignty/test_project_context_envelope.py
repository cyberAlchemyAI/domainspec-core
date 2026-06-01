"""Unit + adversarial tests for pipeline.sovereignty.project_context_envelope.

Section 1 Round F2. Covers §4.2 M2 per-slug lock + §6.2 F-PC-01..03 +
§7.6 test criterion (test_m2_project_context_binding).

Probes the seal path, the Logician mid-session verify path, and several
adversarial TOCTOU / symlink / cross-org cases.
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path

import pytest

from pipeline.sovereignty.isolation import IsolationError
from pipeline.sovereignty.project_context_envelope import (
    CrossOrgViolation,
    OrgRootEscape,
    PROJECTContextEnvelope,
    ProjectContextDrift,
    ProjectContextError,
    seal_project_context,
    verify_project_context,
)
from pipeline.sovereignty.session import SessionSlugMismatch


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def repo_root(tmp_path: Path) -> Path:
    """Repo root with orgs/acme-coop/PROJECT_CONTEXT.md already populated."""
    md = tmp_path / "orgs" / "acme-coop" / "PROJECT_CONTEXT.md"
    md.parent.mkdir(parents=True)
    md.write_text(
        "# Acme Coop context\n\nEIN: 12-3456789\nMission: regenerative.\n",
        encoding="utf-8",
    )
    return tmp_path


@pytest.fixture()
def sealed(repo_root: Path) -> PROJECTContextEnvelope:
    return seal_project_context(
        slug="acme-coop",
        session_id="ses-001",
        repo_root=repo_root,
    )


# ---------------------------------------------------------------------------
# Seal path
# ---------------------------------------------------------------------------


def test_seal_produces_populated_envelope(sealed, repo_root):
    assert sealed.slug == "acme-coop"
    assert sealed.bound_session_id == "ses-001"
    assert sealed.inode > 0
    assert sealed.device != 0
    assert len(sealed.content_hash) == 128
    assert len(sealed.nonce_hex) == 64
    assert sealed.sealed_at.endswith("Z")
    md = repo_root / "orgs" / "acme-coop" / "PROJECT_CONTEXT.md"
    assert sealed.canonical_path == str(md.resolve())


def test_seal_writes_envelope_json(sealed, repo_root):
    env_path = repo_root / "sovereignty" / "envelopes" / "project_context" / "acme-coop.json"
    assert env_path.is_file()
    parsed = json.loads(env_path.read_text("utf-8"))
    assert parsed["slug"] == "acme-coop"
    assert parsed["bound_session_id"] == "ses-001"


def test_seal_creates_lock_file(sealed, repo_root):
    lock_path = (
        repo_root / "sovereignty" / "envelopes" / "project_context" / "acme-coop.json.lock"
    )
    assert lock_path.is_file()


@pytest.mark.parametrize(
    "kwarg,value,exc",
    [
        ("slug", 42, TypeError),
        ("session_id", None, TypeError),
        ("repo_root", "/tmp", TypeError),
        ("expected_session_bound_slug", 5, TypeError),
        ("slug", "", ValueError),
        ("session_id", "", ValueError),
    ],
)
def test_seal_rejects_bad_args(repo_root, kwarg, value, exc):
    base = dict(
        slug="acme-coop",
        session_id="ses-001",
        repo_root=repo_root,
    )
    base[kwarg] = value
    with pytest.raises(exc):
        seal_project_context(**base)


def test_seal_raises_file_not_found_when_md_missing(tmp_path):
    (tmp_path / "orgs" / "acme-coop").mkdir(parents=True)  # org exists, md does not
    with pytest.raises(FileNotFoundError):
        seal_project_context(
            slug="acme-coop",
            session_id="ses-001",
            repo_root=tmp_path,
        )


# ---------------------------------------------------------------------------
# Slug equality / session binding (§7.6 test_m2_project_context_binding)
# ---------------------------------------------------------------------------


def test_m2_project_context_binding_mismatched_expected_slug(repo_root):
    with pytest.raises(SessionSlugMismatch):
        seal_project_context(
            slug="acme-coop",
            session_id="ses-001",
            repo_root=repo_root,
            expected_session_bound_slug="mystic-mamas",
        )


def test_m2_project_context_binding_matching_expected_slug(repo_root):
    env = seal_project_context(
        slug="acme-coop",
        session_id="ses-001",
        repo_root=repo_root,
        expected_session_bound_slug="acme-coop",
    )
    assert env.slug == "acme-coop"


# ---------------------------------------------------------------------------
# Verify path (mid-session)
# ---------------------------------------------------------------------------


def test_verify_happy_path(sealed, repo_root):
    assert verify_project_context(sealed, repo_root=repo_root) is None


def test_verify_detects_content_change(sealed, repo_root):
    md = repo_root / "orgs" / "acme-coop" / "PROJECT_CONTEXT.md"
    # Rewrite in-place via O_WRONLY (preserves inode).
    data = bytearray(md.read_bytes())
    data[0] ^= 0xFF
    fd = os.open(str(md), os.O_WRONLY)
    try:
        os.pwrite(fd, bytes(data), 0)
    finally:
        os.close(fd)
    with pytest.raises(ProjectContextDrift) as excinfo:
        verify_project_context(sealed, repo_root=repo_root)
    assert excinfo.value.reason == "content_hash_mismatch"


def test_verify_detects_inode_swap(sealed, repo_root):
    md = repo_root / "orgs" / "acme-coop" / "PROJECT_CONTEXT.md"
    original = md.read_bytes()
    md.rename(str(md) + ".bak")
    md.write_bytes(original)
    with pytest.raises(ProjectContextDrift) as excinfo:
        verify_project_context(sealed, repo_root=repo_root)
    assert excinfo.value.reason == "inode_changed"


def test_verify_missing_file_raises_drift(sealed, repo_root):
    (repo_root / "orgs" / "acme-coop" / "PROJECT_CONTEXT.md").unlink()
    with pytest.raises(ProjectContextDrift) as excinfo:
        verify_project_context(sealed, repo_root=repo_root)
    assert excinfo.value.reason == "project_context_missing"


def test_verify_cross_org_session_id_mismatch(sealed, repo_root):
    with pytest.raises(CrossOrgViolation):
        verify_project_context(
            sealed,
            repo_root=repo_root,
            expected_session_id="a-different-session",
        )


def test_verify_rejects_non_envelope_arg(repo_root):
    with pytest.raises(TypeError):
        verify_project_context({"not": "an envelope"}, repo_root=repo_root)


# ---------------------------------------------------------------------------
# Escape / symlink failure modes (F-PC-02 / F-ISO-*)
# ---------------------------------------------------------------------------


def test_seal_rejects_symlinked_pc_md(tmp_path):
    """PROJECT_CONTEXT.md as a symlink → O_NOFOLLOW → OrgRootEscape."""
    org = tmp_path / "orgs" / "acme-coop"
    org.mkdir(parents=True)
    outside = tmp_path / "outside.md"
    outside.write_text("rogue\n")
    (org / "PROJECT_CONTEXT.md").symlink_to(outside)
    with pytest.raises(OrgRootEscape):
        seal_project_context(
            slug="acme-coop",
            session_id="ses-001",
            repo_root=tmp_path,
        )


# ---------------------------------------------------------------------------
# Adversarial: lock contention, rapid reseals, schema
# ---------------------------------------------------------------------------


def test_adv_envelope_is_frozen(sealed):
    with pytest.raises(Exception):
        sealed.slug = "hostile"  # type: ignore[misc]


def test_adv_repeated_seals_overwrite_atomically(repo_root):
    e1 = seal_project_context(
        slug="acme-coop", session_id="ses-001", repo_root=repo_root
    )
    e2 = seal_project_context(
        slug="acme-coop", session_id="ses-002", repo_root=repo_root
    )
    assert e1.nonce_hex != e2.nonce_hex
    assert e1.bound_session_id != e2.bound_session_id
    # Envelope on disk reflects the most recent seal.
    env_path = (
        repo_root / "sovereignty" / "envelopes" / "project_context" / "acme-coop.json"
    )
    parsed = json.loads(env_path.read_text("utf-8"))
    assert parsed["bound_session_id"] == "ses-002"


def test_adv_concurrent_seals_serialize_via_fcntl_lock(repo_root):
    """Two threads sealing the same slug should produce two valid envelopes
    without interleaving; the fcntl LOCK_EX serializes them.
    """
    results: list[PROJECTContextEnvelope] = []
    errors: list[BaseException] = []
    barrier = threading.Barrier(2)

    def seal_once(sid: str) -> None:
        try:
            barrier.wait(timeout=5)
            env = seal_project_context(
                slug="acme-coop", session_id=sid, repo_root=repo_root
            )
            results.append(env)
        except BaseException as exc:
            errors.append(exc)

    t1 = threading.Thread(target=seal_once, args=("t1",))
    t2 = threading.Thread(target=seal_once, args=("t2",))
    t1.start()
    t2.start()
    t1.join(timeout=10)
    t2.join(timeout=10)
    assert not errors, errors
    assert len(results) == 2
    # Both succeeded; nonces differ (lock forces one to re-seal).
    assert results[0].nonce_hex != results[1].nonce_hex


def test_adv_empty_pc_md_content_still_hashes(tmp_path):
    org = tmp_path / "orgs" / "acme-coop"
    org.mkdir(parents=True)
    (org / "PROJECT_CONTEXT.md").write_bytes(b"")
    env = seal_project_context(
        slug="acme-coop", session_id="ses-001", repo_root=tmp_path
    )
    assert len(env.content_hash) == 128


def test_adv_verify_after_reseal_with_stale_envelope_detects_inode_or_content_change(
    repo_root, sealed
):
    """If the PC is re-sealed under a new session, the stale envelope's
    verify must fire drift because the new seal rewrites content + nonce
    inherently only on the envelope JSON; the on-disk PC.md is UNCHANGED,
    so verify against stale envelope still works (sealed nonce+hash still
    match on-disk content). BUT if the on-disk content changes mid-session,
    the stale envelope should now drift."""
    # Re-seal (no content change) — stale envelope still valid.
    _ = seal_project_context(
        slug="acme-coop", session_id="ses-002", repo_root=repo_root
    )
    verify_project_context(sealed, repo_root=repo_root)  # happy

    # Now tamper with content; stale envelope should drift.
    md = repo_root / "orgs" / "acme-coop" / "PROJECT_CONTEXT.md"
    data = bytearray(md.read_bytes())
    data.append(0x41)
    md.write_bytes(bytes(data))
    with pytest.raises(ProjectContextDrift):
        verify_project_context(sealed, repo_root=repo_root)
