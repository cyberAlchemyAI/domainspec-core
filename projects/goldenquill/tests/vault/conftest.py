"""Shared fixtures for §2 Vault Round K capstone tests.

Round K packages a cross-module test surface that exercises §2's public
surface (schemas + layout + identity_tuple + uuid_floor + init_marker +
m15_ledger + mirror_verify + atomic_freeze + fd_broker + gate_and_open +
vault_write + compound_txn + metadata_homogenizer + vault_boot) as one
boot → post-gate → compound-txn lifecycle. Fixtures here promote the
``_make_seed_file`` / ``_build_manifest`` / ``_serialize_manifest`` /
``_always_true`` / ``_FakeSnapshotProvider`` helpers established by
``tests/vault/test_vault_boot.py`` so the three Round K test files
reuse one canonical definition.

Per spec card ``pipeline/engineering/spec_cards/section_2_round_k_capstone.md``
K.4 bullet 4 ("fixture library — clean vault root, operator keypair,
sample VaultSharedSeedManifest, sample IdentityTuple, CapstoneKeyStore
pattern, SnapshotProvider stub, FDBroker stub, isolate_active_runtime-
equivalent seam"). Mirrors ``tests/sovereignty/conftest.py`` shape from
the §1 Round J precedent.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Callable, Iterator, Optional

import pytest

from pipeline.sovereignty.keys import KeyStore
from pipeline.vault.atomic_freeze import SnapshotProvider, SnapshotRecord
from pipeline.vault.identity_tuple import resolve_identity_tuple
from pipeline.vault.mirror_verify import (
    compute_leaf_hash_hex,
    compute_merkle_root_hex,
)
from pipeline.vault.schemas import (
    IdentityTuple,
    SeedFile,
    VaultSharedSeedManifest,
)
from pipeline.vault.vault_boot import VaultBootResult, vault_boot_close


# ---------------------------------------------------------------------------
# Canonical HMAC-key constants (Round J pattern, 64 bytes for HMAC key)
# ---------------------------------------------------------------------------

# 64-byte key — matches `init_marker.VAULT_INIT_HMAC_KEY_ID` expectation.
CAPSTONE_VAULT_INIT_HMAC_KEY: bytes = bytes(range(64))


# ---------------------------------------------------------------------------
# Canonical hashing helper
# ---------------------------------------------------------------------------


def sha3_512_hex(data: bytes) -> str:
    """SHA-3-512 hex-digest of ``data``. Matches the ``_sha3_512_hex`` helper
    in ``tests/vault/test_vault_boot.py``; promoted here so every Round K
    test file imports one canonical definition.
    """
    return hashlib.sha3_512(data).hexdigest()


# ---------------------------------------------------------------------------
# Seed-file + manifest builders (promoted from test_vault_boot.py)
# ---------------------------------------------------------------------------


def make_seed_file(rel: str, content: bytes, vault_shared: Path) -> SeedFile:
    """Write ``content`` under ``vault_shared/<rel>`` with 0o644 and build the
    matching :class:`SeedFile` (content hash, size, mode, identity tuple).

    Every Round K test file uses this to construct post-seed-layout state
    without reinventing the mode-bit + identity-tuple dance.
    """
    p = vault_shared / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content)
    os.chmod(p, 0o644)
    st = p.stat()
    return SeedFile(
        relative_path=rel,
        content_hash=sha3_512_hex(content),
        size_bytes=st.st_size,
        mode=st.st_mode & 0o7777,
        identity_tuple=resolve_identity_tuple(p),
    )


def build_manifest(
    seeds: list[SeedFile],
    *,
    m15_ledger_head: str = "ledger-head-1",
    signature: str = "valid-sig",
    committed_at: str = "2026-04-22T00:00:00Z",
    committed_by: str = "operator",
) -> VaultSharedSeedManifest:
    """Build a :class:`VaultSharedSeedManifest` with canonical Merkle root."""
    sorted_seeds = tuple(sorted(seeds, key=lambda s: s.relative_path))
    leaf_hashes = [
        compute_leaf_hash_hex(s.relative_path, s.content_hash)
        for s in sorted_seeds
    ]
    return VaultSharedSeedManifest(
        head_hash=compute_merkle_root_hex(leaf_hashes),
        files=sorted_seeds,
        committed_at=committed_at,
        committed_by=committed_by,
        m15_ledger_head=m15_ledger_head,
        signature=signature,
    )


def serialize_manifest(manifest: VaultSharedSeedManifest) -> bytes:
    """Canonical JSON bytes of ``manifest`` (sort_keys + compact separators).

    Matches the on-disk bytes :func:`m15_ledger.verify_seed_manifest` will
    ingest; any drift in key order / whitespace fails signature verify.
    """
    payload = {
        "head_hash": manifest.head_hash,
        "files": [asdict(sf) for sf in manifest.files],
        "committed_at": manifest.committed_at,
        "committed_by": manifest.committed_by,
        "m15_ledger_head": manifest.m15_ledger_head,
        "signature": manifest.signature,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


# ---------------------------------------------------------------------------
# Signature stubs (promoted from test_vault_boot.py)
# ---------------------------------------------------------------------------


def always_true(_payload: bytes, _signature: str) -> bool:
    """SignatureVerifier stub that accepts every payload. Round K default."""
    return True


def always_false(_payload: bytes, _signature: str) -> bool:
    """SignatureVerifier stub that rejects every payload (F-M15-02 probe)."""
    return False


# ---------------------------------------------------------------------------
# KeyStore stub (mirrors CapstoneKeyStore from tests/sovereignty/conftest.py)
# ---------------------------------------------------------------------------


class CapstoneVaultKeyStore(KeyStore):
    """Minimal ``KeyStore`` suitable for §2 Round K integration tests.

    Serves the canonical 64-byte :data:`CAPSTONE_VAULT_INIT_HMAC_KEY` for
    every ``_retrieve_raw`` call unless a key was explicitly ``store``-d,
    and answers ``True`` for ``exists`` on every id. Matches the
    ``_StubKeyStore`` shape used by ``tests/vault/test_init_marker.py`` and
    ``tests/sovereignty/conftest.py``'s ``CapstoneKeyStore``.

    Session HMAC lifecycle (store / zero / retrieve) is implemented so
    the vault-init-marker ceremony works end-to-end.
    """

    def __init__(self, *, key_bytes: bytes = CAPSTONE_VAULT_INIT_HMAC_KEY) -> None:
        self._default_bytes = key_bytes
        self._store: dict[str, bytearray] = {}

    def _retrieve_raw(self, key_id: str) -> bytearray:
        stored = self._store.get(key_id)
        if stored is not None:
            return bytearray(stored)
        return bytearray(self._default_bytes)

    def store(self, *, key_id: str, key_bytes, purpose: str) -> None:  # noqa: ARG002
        self._store[key_id] = bytearray(bytes(key_bytes))

    def rotate(self, key_id: str) -> str:
        return key_id

    def zero(self, key_id: str) -> None:
        buf = self._store.get(key_id)
        if buf is not None:
            for i in range(len(buf)):
                buf[i] = 0
            del self._store[key_id]

    def exists(self, key_id: str) -> bool:  # noqa: ARG002
        return True

    def provider(self) -> str:
        return "capstone-vault-stub"


# ---------------------------------------------------------------------------
# Snapshot-provider stub (promoted from test_vault_boot.py)
# ---------------------------------------------------------------------------


class FakeSnapshotProvider(SnapshotProvider):
    """In-memory :class:`SnapshotProvider` for atomic-freeze integration tests.

    Matches the ``_FakeSnapshotProvider`` shape from
    ``tests/vault/test_vault_boot.py`` — promoted so Round K integration
    and property-based tests can share one implementation.
    """

    def __init__(self) -> None:
        self._records: list[SnapshotRecord] = []
        self.created: list[str] = []
        self.deleted: list[str] = []

    def list_snapshots(self) -> tuple[SnapshotRecord, ...]:
        return tuple(self._records)

    def create_snapshot(self, *, label: str) -> SnapshotRecord:
        rec = SnapshotRecord(
            label=label,
            created_at_iso="2026-04-22T00:00:42Z",
        )
        self._records.append(rec)
        self.created.append(label)
        return rec

    def delete_snapshot(self, *, label: str) -> None:
        self._records = [r for r in self._records if r.label != label]
        self.deleted.append(label)


# ---------------------------------------------------------------------------
# Core fixtures — §2 vault workspace
# ---------------------------------------------------------------------------


DEFAULT_SEED_SPEC: tuple[tuple[str, bytes], ...] = (
    ("cedar/org_isolation.cedar", b"permit;\n"),
    ("cedar/write_gate.cedar", b"forbid x;\n"),
    ("process_wrappers/seat-launch.sh", b"#!/bin/sh\nexec $@\n"),
)


@pytest.fixture
def capstone_vault_workspace(tmp_path: Path) -> dict:
    """Build a complete on-disk vault root + signed seed manifest.

    Layout:

    * ``workspace/``                    — parent
    * ``workspace/vault/``              — vault_root
    * ``workspace/vault/vault_shared/`` — vault_shared (contains seeds)
    * ``workspace/seed_manifest.json``  — canonical manifest bytes
    * ``workspace/seed_manifest.sig``   — "valid-sig\\n" stub signature

    Mirrors ``boot_workspace`` in ``tests/vault/test_vault_boot.py``,
    promoted for Round K. Returns a dict so tests can cherry-pick paths
    (``vault_root`` / ``vault_shared`` / ``manifest`` / ``manifest_path`` /
    ``sig_path`` / ``seeds``).
    """
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    vault_root = workspace / "vault"
    vault_root.mkdir()
    vault_shared = vault_root / "vault_shared"
    vault_shared.mkdir()

    seeds = [
        make_seed_file(rel, content, vault_shared)
        for rel, content in DEFAULT_SEED_SPEC
    ]
    manifest = build_manifest(seeds)
    manifest_path = workspace / "seed_manifest.json"
    sig_path = workspace / "seed_manifest.sig"
    manifest_path.write_bytes(serialize_manifest(manifest))
    sig_path.write_text(manifest.signature + "\n", encoding="utf-8")

    return {
        "workspace": workspace,
        "vault_root": vault_root,
        "vault_shared": vault_shared,
        "seeds": seeds,
        "manifest": manifest,
        "manifest_path": manifest_path,
        "sig_path": sig_path,
    }


@pytest.fixture
def capstone_boot_kwargs(capstone_vault_workspace: dict) -> dict:
    """Ready-to-call kwargs for :func:`vault_boot`.

    Uses :func:`always_true` as the signature verifier and the workspace's
    ledger-head baseline. Tests mutate copies of this dict to probe failure
    propagation (signature fail → F-M15-02; ledger drift → F-M15-03).
    """
    return {
        "vault_root": capstone_vault_workspace["vault_root"],
        "vault_shared_root": capstone_vault_workspace["vault_shared"],
        "seed_manifest_path": capstone_vault_workspace["manifest_path"],
        "seed_signature_path": capstone_vault_workspace["sig_path"],
        "session_id": "session-capstone-K",
        "current_ledger_head": capstone_vault_workspace["manifest"].m15_ledger_head,
        "verify_signature": always_true,
        "platform": "darwin",
    }


@pytest.fixture
def capstone_keystore() -> CapstoneVaultKeyStore:
    """Default keystore used by the majority of Round K tests.

    Serves :data:`CAPSTONE_VAULT_INIT_HMAC_KEY` (64 bytes) for every
    ``_retrieve_raw`` call; answers ``True`` for ``exists`` unconditionally.
    """
    return CapstoneVaultKeyStore()


@pytest.fixture
def capstone_snapshot_provider() -> FakeSnapshotProvider:
    """In-memory :class:`SnapshotProvider` for atomic-freeze integration."""
    return FakeSnapshotProvider()


@pytest.fixture
def capstone_identity_tuple(tmp_path: Path) -> IdentityTuple:
    """Canonical :class:`IdentityTuple` resolved against ``tmp_path``.

    The volume_uuid / mount_id / fs_type values are whatever the test host
    carries — the tuple is stable for the duration of a single pytest
    process, which is all Round K invariants require.
    """
    return resolve_identity_tuple(tmp_path)


@pytest.fixture
def capstone_auto_close() -> Iterator[list[VaultBootResult]]:
    """Yield a list to register :class:`VaultBootResult` instances; closes
    them on teardown so ``vault_root_fd`` never leaks between tests.

    Mirrors the ``auto_close`` fixture from ``tests/vault/test_vault_boot.py``.
    """
    results: list[VaultBootResult] = []
    yield results
    for r in results:
        try:
            vault_boot_close(r)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Multi-org workspace fixture (for K.3 parametric fuzz)
# ---------------------------------------------------------------------------


@pytest.fixture
def capstone_multi_org_workspace(
    capstone_vault_workspace: dict,
) -> Callable[[int, str], list[Path]]:
    """Factory that provisions N per-org directories under ``vault_root``.

    Returns a callable ``(n: int, prefix: str = "org") -> list[Path]``
    producing ``vault_root/<prefix>-<i>/`` for ``i in range(n)`` with an
    empty ``PROJECT_CONTEXT.md`` sentinel each. The §2.4 Law-3 cross-org
    rejection invariant test in ``test_section_2_boot_sequence_property``
    parametrises this over N ∈ {2, 8, 16, 32}.
    """

    vault_root: Path = capstone_vault_workspace["vault_root"]

    def _make(n: int, prefix: str = "org") -> list[Path]:
        dirs: list[Path] = []
        for i in range(n):
            d = vault_root / f"{prefix}-{i:04d}"
            d.mkdir(parents=True, exist_ok=True)
            (d / "PROJECT_CONTEXT.md").write_text(
                f"# PROJECT_CONTEXT — {prefix}-{i:04d}\n\nseed: {i}\n",
                encoding="utf-8",
            )
            dirs.append(d)
        return dirs

    return _make


# ---------------------------------------------------------------------------
# Public re-exports (keep helpers importable from test modules)
# ---------------------------------------------------------------------------


__all__ = [
    "CAPSTONE_VAULT_INIT_HMAC_KEY",
    "CapstoneVaultKeyStore",
    "DEFAULT_SEED_SPEC",
    "FakeSnapshotProvider",
    "always_false",
    "always_true",
    "build_manifest",
    "make_seed_file",
    "serialize_manifest",
    "sha3_512_hex",
]
