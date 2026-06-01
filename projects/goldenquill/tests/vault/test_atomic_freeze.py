"""Unit tests for pipeline.vault.atomic_freeze (§4.7 + §9 steps 7 + 11a).

Round U — Atomic verify-and-freeze.

v0.1 dev box is macOS, so the macOS-primary mechanism (verified-and-pinned
Merkle root, already produced by Round T `verify_seed_manifest`) is the
freeze. This module:

* Returns an :class:`AtomicFreezeResult` carrying the pinned root +
  CoV-snapshot disposition + degradation notes for the rails report.
* On macOS, optionally creates a CoV snapshot via an injected
  :type:`SnapshotProvider` (APFS in production; a fake in tests).
* Enforces the A-09 retention policy
  (``COV_SNAPSHOT_RETENTION_COUNT = 3``) — delete oldest snapshots before
  creating a new one so the post-create total equals retention.
* Snapshot-create / retention-prune failures are non-fatal and surface as
  ``snapshot_degraded`` / ``retention_degraded`` (F-FREEZE-03 / F-FREEZE-04).

Linux mount-namespace switch (`unshare(CLONE_NEWNS)` + remount ro) is
deferred past v0.1 (the dev box is macOS); on non-darwin platforms,
``apply()`` records ``namespace_active=False`` plus a degradation note so
the boot capstone (Round R) can surface it in the rails report. The Merkle
pin still holds because it is platform-agnostic.
"""

from __future__ import annotations

import dataclasses
import hashlib
import os
from pathlib import Path
from typing import Callable, Optional

import pytest

from pipeline.vault.atomic_freeze import (
    COV_SNAPSHOT_RETENTION_COUNT,
    AtomicFreezeFailed,
    AtomicFreezeResult,
    SnapshotProvider,
    SnapshotRecord,
    SnapshotRetentionCleanupFailed,
    apply,
    prune_snapshots,
)
from pipeline.vault.error_codes import (
    F_FREEZE_01,
    F_FREEZE_04,
    FreezeError,
)
from pipeline.vault.identity_tuple import resolve_identity_tuple
from pipeline.vault.mirror_verify import (
    VaultSharedFrozenRoot,
    compute_leaf_hash_hex,
    compute_merkle_root_hex,
    freeze_vault_shared,
)
from pipeline.vault.schemas import (
    SeedFile,
    VaultSharedSeedManifest,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sha3_512_hex(data: bytes) -> str:
    return hashlib.sha3_512(data).hexdigest()


def _make_seed_file(rel: str, content: bytes, vault_shared: Path) -> SeedFile:
    p = vault_shared / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content)
    os.chmod(p, 0o644)
    st = p.stat()
    return SeedFile(
        relative_path=rel,
        content_hash=_sha3_512_hex(content),
        size_bytes=st.st_size,
        mode=st.st_mode & 0o7777,
        identity_tuple=resolve_identity_tuple(p),
    )


def _build_manifest(seeds: list[SeedFile]) -> VaultSharedSeedManifest:
    sorted_seeds = tuple(sorted(seeds, key=lambda s: s.relative_path))
    leaf_hashes = [
        compute_leaf_hash_hex(s.relative_path, s.content_hash)
        for s in sorted_seeds
    ]
    return VaultSharedSeedManifest(
        head_hash=compute_merkle_root_hex(leaf_hashes),
        files=sorted_seeds,
        committed_at="2026-04-19T00:00:00Z",
        committed_by="operator",
        m15_ledger_head="ledger-head-1",
        signature="sig",
    )


@pytest.fixture
def vault_shared(tmp_path: Path) -> Path:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    shared = workspace / "vault_shared"
    shared.mkdir()
    return shared


@pytest.fixture
def frozen_root(vault_shared: Path) -> VaultSharedFrozenRoot:
    seeds = [
        _make_seed_file("cedar/x.cedar", b"permit;\n", vault_shared),
        _make_seed_file(
            "process_wrappers/seat-launch.sh", b"#!/bin/sh\n", vault_shared
        ),
    ]
    return freeze_vault_shared(
        manifest=_build_manifest(seeds), vault_shared_root=vault_shared
    )


# ---------------------------------------------------------------------------
# In-test fake snapshot provider
# ---------------------------------------------------------------------------


class _FakeSnapshotProvider:
    """In-memory SnapshotProvider for tests."""

    def __init__(
        self,
        *,
        existing: Optional[list[SnapshotRecord]] = None,
        create_raises: Optional[Exception] = None,
        delete_raises_on: Optional[set[str]] = None,
        list_raises: Optional[Exception] = None,
    ) -> None:
        self._records: list[SnapshotRecord] = list(existing or [])
        self._create_raises = create_raises
        self._delete_raises_on = set(delete_raises_on or set())
        self._list_raises = list_raises
        self.created: list[str] = []
        self.deleted: list[str] = []

    def list_snapshots(self) -> tuple[SnapshotRecord, ...]:
        if self._list_raises is not None:
            raise self._list_raises
        return tuple(self._records)

    def create_snapshot(self, *, label: str) -> SnapshotRecord:
        if self._create_raises is not None:
            raise self._create_raises
        rec = SnapshotRecord(label=label, created_at_iso="2026-04-19T00:00:42Z")
        self._records.append(rec)
        self.created.append(label)
        return rec

    def delete_snapshot(self, *, label: str) -> None:
        if label in self._delete_raises_on:
            raise OSError(f"deletion blocked: {label}")
        self._records = [r for r in self._records if r.label != label]
        self.deleted.append(label)


def _record(label: str, ts: str) -> SnapshotRecord:
    return SnapshotRecord(label=label, created_at_iso=ts)


# ---------------------------------------------------------------------------
# Constants + dataclass shape
# ---------------------------------------------------------------------------


class TestConstants:
    def test_retention_count_pinned_at_3(self) -> None:
        assert COV_SNAPSHOT_RETENTION_COUNT == 3


class TestSnapshotRecord:
    def test_is_frozen(self) -> None:
        rec = _record("a", "2026-04-19T00:00:00Z")
        with pytest.raises(dataclasses.FrozenInstanceError):
            rec.label = "b"  # type: ignore[misc]

    def test_kw_only(self) -> None:
        with pytest.raises(TypeError):
            SnapshotRecord("a", "b")  # type: ignore[misc]


class TestAtomicFreezeResult:
    def test_is_frozen(
        self, frozen_root: VaultSharedFrozenRoot
    ) -> None:
        out = AtomicFreezeResult(
            platform="darwin",
            frozen_root=frozen_root,
            namespace_active=False,
            snapshot_label=None,
            snapshots_pruned=(),
            snapshot_degraded=False,
            retention_degraded=False,
            degradations=(),
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            out.platform = "linux"  # type: ignore[misc]

    def test_kw_only(
        self, frozen_root: VaultSharedFrozenRoot
    ) -> None:
        with pytest.raises(TypeError):
            AtomicFreezeResult(
                "darwin",  # type: ignore[misc]
                frozen_root,
                False,
                None,
                (),
                False,
                False,
                (),
            )


# ---------------------------------------------------------------------------
# apply() — macOS primary path
# ---------------------------------------------------------------------------


class TestApplyMacOSPrimary:
    def test_no_snapshot_provider_returns_pinned_root(
        self, frozen_root: VaultSharedFrozenRoot, vault_shared: Path
    ) -> None:
        out = apply(
            frozen_root=frozen_root,
            vault_shared_root=vault_shared,
            session_id="session-A",
            platform="darwin",
            snapshot_provider=None,
        )
        assert out.platform == "darwin"
        assert out.frozen_root is frozen_root
        assert out.namespace_active is False
        assert out.snapshot_label is None
        assert out.snapshots_pruned == ()
        assert out.snapshot_degraded is False
        assert out.retention_degraded is False
        # No snapshot provider is not itself a degradation; the rails-report
        # author elsewhere may decide whether to surface it.
        assert "snapshot-provider-absent" not in out.degradations

    def test_with_snapshot_provider_creates_label(
        self, frozen_root: VaultSharedFrozenRoot, vault_shared: Path
    ) -> None:
        provider = _FakeSnapshotProvider()
        out = apply(
            frozen_root=frozen_root,
            vault_shared_root=vault_shared,
            session_id="abc123",
            platform="darwin",
            snapshot_provider=provider,
        )
        assert out.snapshot_label is not None
        assert "abc123" in out.snapshot_label
        assert out.snapshot_label in provider.created

    def test_retention_prune_runs_before_create(
        self, frozen_root: VaultSharedFrozenRoot, vault_shared: Path
    ) -> None:
        # Three existing snapshots; retention=3 means we must delete the oldest
        # so that after creating one, the total is 3.
        provider = _FakeSnapshotProvider(
            existing=[
                _record("snap-1-old", "2026-04-17T00:00:00Z"),
                _record("snap-2-mid", "2026-04-18T00:00:00Z"),
                _record("snap-3-new", "2026-04-19T00:00:00Z"),
            ]
        )
        out = apply(
            frozen_root=frozen_root,
            vault_shared_root=vault_shared,
            session_id="s",
            platform="darwin",
            snapshot_provider=provider,
        )
        # Oldest deleted; new created; total == retention.
        assert "snap-1-old" in out.snapshots_pruned
        assert provider.deleted == ["snap-1-old"]
        assert len(provider.list_snapshots()) == COV_SNAPSHOT_RETENTION_COUNT

    def test_existing_below_retention_does_not_prune(
        self, frozen_root: VaultSharedFrozenRoot, vault_shared: Path
    ) -> None:
        provider = _FakeSnapshotProvider(
            existing=[_record("snap-only", "2026-04-18T00:00:00Z")]
        )
        out = apply(
            frozen_root=frozen_root,
            vault_shared_root=vault_shared,
            session_id="s",
            platform="darwin",
            snapshot_provider=provider,
        )
        assert out.snapshots_pruned == ()
        assert provider.deleted == []
        assert out.retention_degraded is False

    def test_snapshot_create_failure_is_non_fatal(
        self, frozen_root: VaultSharedFrozenRoot, vault_shared: Path
    ) -> None:
        provider = _FakeSnapshotProvider(create_raises=OSError("apfs full"))
        out = apply(
            frozen_root=frozen_root,
            vault_shared_root=vault_shared,
            session_id="s",
            platform="darwin",
            snapshot_provider=provider,
        )
        assert out.snapshot_degraded is True
        assert out.snapshot_label is None
        assert any("snapshot-create-failed" in d for d in out.degradations)
        # Primary still succeeded.
        assert out.frozen_root is frozen_root

    def test_retention_prune_failure_is_non_fatal(
        self, frozen_root: VaultSharedFrozenRoot, vault_shared: Path
    ) -> None:
        provider = _FakeSnapshotProvider(
            existing=[
                _record("snap-1-old", "2026-04-17T00:00:00Z"),
                _record("snap-2-mid", "2026-04-18T00:00:00Z"),
                _record("snap-3-new", "2026-04-19T00:00:00Z"),
            ],
            delete_raises_on={"snap-1-old"},
        )
        out = apply(
            frozen_root=frozen_root,
            vault_shared_root=vault_shared,
            session_id="s",
            platform="darwin",
            snapshot_provider=provider,
        )
        assert out.retention_degraded is True
        assert any("retention-prune-failed" in d for d in out.degradations)
        # Primary still succeeded.
        assert out.frozen_root is frozen_root

    def test_list_snapshots_failure_degrades_retention(
        self, frozen_root: VaultSharedFrozenRoot, vault_shared: Path
    ) -> None:
        provider = _FakeSnapshotProvider(
            list_raises=OSError("listsnaps blew up")
        )
        out = apply(
            frozen_root=frozen_root,
            vault_shared_root=vault_shared,
            session_id="s",
            platform="darwin",
            snapshot_provider=provider,
        )
        assert out.retention_degraded is True
        assert out.snapshot_degraded is True


# ---------------------------------------------------------------------------
# apply() — non-darwin platform
# ---------------------------------------------------------------------------


class TestApplyLinux:
    def test_linux_returns_pin_with_degradation_note(
        self, frozen_root: VaultSharedFrozenRoot, vault_shared: Path
    ) -> None:
        out = apply(
            frozen_root=frozen_root,
            vault_shared_root=vault_shared,
            session_id="s",
            platform="linux",
            snapshot_provider=None,
        )
        assert out.platform == "linux"
        assert out.namespace_active is False
        assert any(
            "linux-mount-ns-not-implemented-v0.1" in d for d in out.degradations
        )
        assert out.frozen_root is frozen_root


# ---------------------------------------------------------------------------
# Type gates
# ---------------------------------------------------------------------------


class TestApplyTypeGates:
    def test_rejects_non_frozen_root(self, vault_shared: Path) -> None:
        with pytest.raises(TypeError):
            apply(
                frozen_root="x",  # type: ignore[arg-type]
                vault_shared_root=vault_shared,
                session_id="s",
                platform="darwin",
                snapshot_provider=None,
            )

    def test_rejects_non_path_root(
        self, frozen_root: VaultSharedFrozenRoot
    ) -> None:
        with pytest.raises(TypeError):
            apply(
                frozen_root=frozen_root,
                vault_shared_root="x",  # type: ignore[arg-type]
                session_id="s",
                platform="darwin",
                snapshot_provider=None,
            )

    def test_rejects_non_str_session_id(
        self, frozen_root: VaultSharedFrozenRoot, vault_shared: Path
    ) -> None:
        with pytest.raises(TypeError):
            apply(
                frozen_root=frozen_root,
                vault_shared_root=vault_shared,
                session_id=42,  # type: ignore[arg-type]
                platform="darwin",
                snapshot_provider=None,
            )

    def test_rejects_empty_session_id(
        self, frozen_root: VaultSharedFrozenRoot, vault_shared: Path
    ) -> None:
        with pytest.raises(ValueError):
            apply(
                frozen_root=frozen_root,
                vault_shared_root=vault_shared,
                session_id="",
                platform="darwin",
                snapshot_provider=None,
            )


# ---------------------------------------------------------------------------
# prune_snapshots — §9 step 11a standalone housekeeping
# ---------------------------------------------------------------------------


class TestPruneSnapshots:
    def test_below_retention_returns_empty(self) -> None:
        provider = _FakeSnapshotProvider(
            existing=[_record("snap-A", "2026-04-19T00:00:00Z")]
        )
        out = prune_snapshots(
            snapshot_provider=provider, retention_count=3
        )
        assert out == ()
        assert provider.deleted == []

    def test_at_retention_returns_empty(self) -> None:
        provider = _FakeSnapshotProvider(
            existing=[
                _record("snap-A", "2026-04-17T00:00:00Z"),
                _record("snap-B", "2026-04-18T00:00:00Z"),
                _record("snap-C", "2026-04-19T00:00:00Z"),
            ]
        )
        out = prune_snapshots(
            snapshot_provider=provider, retention_count=3
        )
        assert out == ()
        assert provider.deleted == []

    def test_above_retention_deletes_oldest_first(self) -> None:
        provider = _FakeSnapshotProvider(
            existing=[
                _record("snap-A", "2026-04-15T00:00:00Z"),
                _record("snap-B", "2026-04-16T00:00:00Z"),
                _record("snap-C", "2026-04-17T00:00:00Z"),
                _record("snap-D", "2026-04-18T00:00:00Z"),
                _record("snap-E", "2026-04-19T00:00:00Z"),
            ]
        )
        out = prune_snapshots(
            snapshot_provider=provider, retention_count=3
        )
        # Two oldest should be deleted: snap-A then snap-B.
        assert out == ("snap-A", "snap-B")
        assert provider.deleted == ["snap-A", "snap-B"]

    def test_empty_provider_returns_empty(self) -> None:
        provider = _FakeSnapshotProvider()
        assert prune_snapshots(
            snapshot_provider=provider, retention_count=3
        ) == ()

    def test_delete_failure_raises_retention_cleanup_failed(self) -> None:
        provider = _FakeSnapshotProvider(
            existing=[
                _record("snap-A", "2026-04-15T00:00:00Z"),
                _record("snap-B", "2026-04-16T00:00:00Z"),
                _record("snap-C", "2026-04-17T00:00:00Z"),
                _record("snap-D", "2026-04-18T00:00:00Z"),
            ],
            delete_raises_on={"snap-A"},
        )
        with pytest.raises(SnapshotRetentionCleanupFailed) as exc:
            prune_snapshots(
                snapshot_provider=provider, retention_count=3
            )
        assert exc.value.code == F_FREEZE_04

    def test_list_failure_raises_retention_cleanup_failed(self) -> None:
        provider = _FakeSnapshotProvider(
            list_raises=OSError("snapshot enumeration failed")
        )
        with pytest.raises(SnapshotRetentionCleanupFailed) as exc:
            prune_snapshots(
                snapshot_provider=provider, retention_count=3
            )
        assert exc.value.code == F_FREEZE_04

    def test_negative_retention_rejected(self) -> None:
        provider = _FakeSnapshotProvider()
        with pytest.raises(ValueError):
            prune_snapshots(
                snapshot_provider=provider, retention_count=-1
            )

    def test_rejects_non_provider(self) -> None:
        with pytest.raises(TypeError):
            prune_snapshots(
                snapshot_provider=None,  # type: ignore[arg-type]
                retention_count=3,
            )


# ---------------------------------------------------------------------------
# Exception taxonomy
# ---------------------------------------------------------------------------


class TestExceptionTaxonomy:
    def test_atomic_freeze_failed_inherits_freeze_error(self) -> None:
        assert issubclass(AtomicFreezeFailed, FreezeError)
        assert AtomicFreezeFailed.code == F_FREEZE_01

    def test_retention_cleanup_failed_inherits_freeze_error(self) -> None:
        assert issubclass(SnapshotRetentionCleanupFailed, FreezeError)
        assert SnapshotRetentionCleanupFailed.code == F_FREEZE_04


# ---------------------------------------------------------------------------
# SnapshotProvider protocol structural compatibility
# ---------------------------------------------------------------------------


class TestSnapshotProviderProtocol:
    def test_fake_satisfies_protocol(self) -> None:
        provider: SnapshotProvider = _FakeSnapshotProvider()
        # All three methods are accessible.
        assert callable(provider.list_snapshots)
        assert callable(provider.create_snapshot)
        assert callable(provider.delete_snapshot)


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        from pipeline.vault import atomic_freeze as _mod

        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
