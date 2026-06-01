"""Unit tests for pipeline.vault.mirror_verify (§2.5 + §4.7 macOS-primary).

Round S — Verified-and-pinned Merkle root over `vault_shared/`, plus the
§2.5 TrustRootMirrorManifest verification surface.

Scope:
* Deterministic SHA-3-512 Merkle tree (RFC 6962 leaf/internal domain
  separators, last-leaf duplication for odd counts).
* Inclusion proofs that verify against the pinned root.
* `VaultSharedFrozenRoot` immutable dataclass holding root + per-leaf proofs.
* `freeze_vault_shared` builds the frozen root from a seed manifest, refusing
  on (a) computed-vs-manifest head_hash drift, (b) on-disk content drift, and
  (c) extra unlisted files (tamper evidence per §2.4 invariant).
* `make_post_gate_hook` returns a Callable[[FDBrokerRequest], bool] suitable
  for `FDBroker.register_post_gate(...)`. The hook re-verifies any request
  for a path under `vault_shared/` (seed partition only) on every issue.
* `verify_trust_root_mirror` enforces §2.5 invariants
  (F-MIRROR-01..05).

Out of scope (deferred to Round T m15_ledger and beyond):
* M15 ledger-head verify (§4.6) — caller-supplied for now.
* Operator-signature primitive — injected as a callable so this module does
  not bind to a specific keystore in v0.1.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
from pathlib import Path
from typing import Callable, Iterator, Optional

import pytest

from pipeline.vault.error_codes import (
    F_M15_01,
    F_MIRROR_01,
    F_MIRROR_02,
    F_MIRROR_03,
    F_MIRROR_04,
    F_MIRROR_05,
    M15Error,
    MirrorError,
)
from pipeline.vault.identity_tuple import resolve_identity_tuple
from pipeline.vault.mirror_verify import (
    LEAF_DOMAIN_TAG,
    NODE_DOMAIN_TAG,
    InclusionProofStep,
    MirrorClockRollback,
    MirrorContentMismatch,
    MirrorIdentityMismatch,
    MirrorImmutabilityMissing,
    MirrorSignatureInvalid,
    SeedFileExtraOnDisk,
    SeedFileIdentityDrift,
    SeedManifestHeadDrift,
    VaultSharedFrozenRoot,
    canonical_leaf_bytes,
    compute_inclusion_proof,
    compute_leaf_hash_hex,
    compute_merkle_root_hex,
    freeze_vault_shared,
    make_post_gate_hook,
    reverify_path,
    verify_inclusion,
    verify_trust_root_mirror,
)
from pipeline.vault.schemas import (
    FDBrokerRequest,
    IdentityTuple,
    SeedFile,
    TrustRootMirrorManifest,
    VaultSharedSeedManifest,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sha3_512_hex(data: bytes) -> str:
    return hashlib.sha3_512(data).hexdigest()


def _canonical(obj: object) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _make_seed_file(rel: str, content: bytes, vault_shared: Path) -> SeedFile:
    """Write a file under vault_shared and return its SeedFile entry."""
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


def _build_manifest(
    seeds: list[SeedFile],
    *,
    head_hash: Optional[str] = None,
    signature: str = "sig",
    m15_ledger_head: str = "ledger-head",
    committed_at: str = "2026-04-19T00:00:00Z",
    committed_by: str = "operator",
) -> VaultSharedSeedManifest:
    sorted_seeds = tuple(sorted(seeds, key=lambda s: s.relative_path))
    if head_hash is None:
        leaf_hashes = [
            compute_leaf_hash_hex(s.relative_path, s.content_hash)
            for s in sorted_seeds
        ]
        head_hash = compute_merkle_root_hex(leaf_hashes)
    return VaultSharedSeedManifest(
        head_hash=head_hash,
        files=sorted_seeds,
        committed_at=committed_at,
        committed_by=committed_by,
        m15_ledger_head=m15_ledger_head,
        signature=signature,
    )


@pytest.fixture
def vault_shared(tmp_path: Path) -> Path:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    shared = workspace / "vault_shared"
    shared.mkdir()
    return shared


@pytest.fixture
def seeded_shared(vault_shared: Path) -> tuple[Path, list[SeedFile]]:
    seeds = [
        _make_seed_file("cedar/org_isolation.cedar", b"permit;\n", vault_shared),
        _make_seed_file("cedar/write_gate.cedar", b"permit;\nforbid x;\n", vault_shared),
        _make_seed_file("sandbox_profiles/scout.sbpl", b"(version 1)\n", vault_shared),
        _make_seed_file(
            "process_wrappers/fallback-shell/seat-launch.sh", b"#!/bin/sh\nexec $@\n", vault_shared
        ),
    ]
    return vault_shared, seeds


# ---------------------------------------------------------------------------
# Domain-tag constants (RFC 6962-ish)
# ---------------------------------------------------------------------------


class TestDomainTags:
    def test_leaf_tag_is_zero(self) -> None:
        assert LEAF_DOMAIN_TAG == b"\x00"

    def test_node_tag_is_one(self) -> None:
        assert NODE_DOMAIN_TAG == b"\x01"


# ---------------------------------------------------------------------------
# Canonical leaf bytes
# ---------------------------------------------------------------------------


class TestCanonicalLeafBytes:
    def test_returns_canonical_json_bytes(self) -> None:
        out = canonical_leaf_bytes("cedar/org_isolation.cedar", "ab" * 64)
        assert out == _canonical({"hash": "ab" * 64, "path": "cedar/org_isolation.cedar"})

    def test_key_order_is_irrelevant_to_caller(self) -> None:
        a = canonical_leaf_bytes("a/b", "00" * 64)
        b = canonical_leaf_bytes("a/b", "00" * 64)
        assert a == b

    def test_rejects_non_str_path(self) -> None:
        with pytest.raises(TypeError):
            canonical_leaf_bytes(b"a/b", "00" * 64)  # type: ignore[arg-type]

    def test_rejects_non_str_hash(self) -> None:
        with pytest.raises(TypeError):
            canonical_leaf_bytes("a/b", b"00" * 64)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Merkle root primitives
# ---------------------------------------------------------------------------


class TestComputeLeafHash:
    def test_hashes_with_leaf_tag(self) -> None:
        path = "cedar/x.cedar"
        content_hash = "11" * 64
        expected = _sha3_512_hex(LEAF_DOMAIN_TAG + canonical_leaf_bytes(path, content_hash))
        assert compute_leaf_hash_hex(path, content_hash) == expected

    def test_changes_when_content_hash_changes(self) -> None:
        a = compute_leaf_hash_hex("p", "11" * 64)
        b = compute_leaf_hash_hex("p", "22" * 64)
        assert a != b

    def test_changes_when_path_changes(self) -> None:
        a = compute_leaf_hash_hex("p1", "11" * 64)
        b = compute_leaf_hash_hex("p2", "11" * 64)
        assert a != b


class TestComputeMerkleRoot:
    def test_empty_list_raises(self) -> None:
        with pytest.raises(ValueError):
            compute_merkle_root_hex([])

    def test_single_leaf_returns_leaf_hash(self) -> None:
        leaf = compute_leaf_hash_hex("only", "aa" * 64)
        assert compute_merkle_root_hex([leaf]) == leaf

    def test_two_leaves_matches_handcomputed_root(self) -> None:
        l1 = compute_leaf_hash_hex("a", "11" * 64)
        l2 = compute_leaf_hash_hex("b", "22" * 64)
        expected = _sha3_512_hex(
            NODE_DOMAIN_TAG + bytes.fromhex(l1) + bytes.fromhex(l2)
        )
        assert compute_merkle_root_hex([l1, l2]) == expected

    def test_three_leaves_duplicates_last(self) -> None:
        l1 = compute_leaf_hash_hex("a", "11" * 64)
        l2 = compute_leaf_hash_hex("b", "22" * 64)
        l3 = compute_leaf_hash_hex("c", "33" * 64)
        # level 1: H(l1,l2), H(l3,l3)
        a = _sha3_512_hex(NODE_DOMAIN_TAG + bytes.fromhex(l1) + bytes.fromhex(l2))
        b = _sha3_512_hex(NODE_DOMAIN_TAG + bytes.fromhex(l3) + bytes.fromhex(l3))
        # root: H(a,b)
        root = _sha3_512_hex(NODE_DOMAIN_TAG + bytes.fromhex(a) + bytes.fromhex(b))
        assert compute_merkle_root_hex([l1, l2, l3]) == root

    def test_root_is_deterministic_across_calls(self) -> None:
        leaves = [compute_leaf_hash_hex(f"p{i}", f"{i:02x}" * 64) for i in range(7)]
        assert compute_merkle_root_hex(leaves) == compute_merkle_root_hex(list(leaves))

    def test_root_changes_when_any_leaf_changes(self) -> None:
        leaves = [compute_leaf_hash_hex(f"p{i}", f"{i:02x}" * 64) for i in range(5)]
        original_root = compute_merkle_root_hex(leaves)
        leaves[2] = compute_leaf_hash_hex("p2", "ff" * 64)
        assert compute_merkle_root_hex(leaves) != original_root

    def test_rejects_non_hex_leaf(self) -> None:
        with pytest.raises(ValueError):
            compute_merkle_root_hex(["zz" * 64])


# ---------------------------------------------------------------------------
# Inclusion proof
# ---------------------------------------------------------------------------


class TestInclusionProof:
    def test_proof_for_each_leaf_verifies_against_root(self) -> None:
        leaves = [compute_leaf_hash_hex(f"p{i}", f"{i:02x}" * 64) for i in range(8)]
        root = compute_merkle_root_hex(leaves)
        for idx, leaf in enumerate(leaves):
            proof = compute_inclusion_proof(leaves, idx)
            assert verify_inclusion(leaf, idx, proof, root) is True

    def test_proof_for_odd_count_works_for_last_leaf(self) -> None:
        leaves = [compute_leaf_hash_hex(f"p{i}", f"{i:02x}" * 64) for i in range(5)]
        root = compute_merkle_root_hex(leaves)
        proof = compute_inclusion_proof(leaves, 4)
        assert verify_inclusion(leaves[4], 4, proof, root) is True

    def test_proof_rejects_wrong_leaf(self) -> None:
        leaves = [compute_leaf_hash_hex(f"p{i}", f"{i:02x}" * 64) for i in range(4)]
        root = compute_merkle_root_hex(leaves)
        proof = compute_inclusion_proof(leaves, 1)
        wrong_leaf = compute_leaf_hash_hex("p1", "ff" * 64)
        assert verify_inclusion(wrong_leaf, 1, proof, root) is False

    def test_proof_rejects_wrong_root(self) -> None:
        leaves = [compute_leaf_hash_hex(f"p{i}", f"{i:02x}" * 64) for i in range(4)]
        proof = compute_inclusion_proof(leaves, 2)
        bogus_root = "00" * 64
        assert verify_inclusion(leaves[2], 2, proof, bogus_root) is False

    def test_proof_rejects_index_out_of_range(self) -> None:
        leaves = [compute_leaf_hash_hex(f"p{i}", f"{i:02x}" * 64) for i in range(4)]
        with pytest.raises(IndexError):
            compute_inclusion_proof(leaves, 4)

    def test_proof_step_carries_side_and_sibling(self) -> None:
        leaves = [compute_leaf_hash_hex(f"p{i}", f"{i:02x}" * 64) for i in range(2)]
        proof = compute_inclusion_proof(leaves, 0)
        assert isinstance(proof[0], InclusionProofStep)
        assert proof[0].sibling_hash_hex == leaves[1]
        assert proof[0].side == "right"


# ---------------------------------------------------------------------------
# VaultSharedFrozenRoot frozen-ness
# ---------------------------------------------------------------------------


class TestFrozenRoot:
    def test_root_is_frozen_dataclass(self) -> None:
        assert dataclasses.is_dataclass(VaultSharedFrozenRoot)
        # frozen = True means assignment raises FrozenInstanceError
        seeds: tuple[SeedFile, ...] = ()
        fr = VaultSharedFrozenRoot(
            root_hex="aa" * 64,
            seed_paths=(),
            leaf_hashes_hex=(),
            inclusion_proofs={},
            content_hashes_hex={},
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            fr.root_hex = "bb" * 64  # type: ignore[misc]

    def test_root_carries_per_path_proof_map(self) -> None:
        leaves = [
            compute_leaf_hash_hex("a/x", "11" * 64),
            compute_leaf_hash_hex("a/y", "22" * 64),
        ]
        root = compute_merkle_root_hex(leaves)
        proofs = {
            "a/x": compute_inclusion_proof(leaves, 0),
            "a/y": compute_inclusion_proof(leaves, 1),
        }
        fr = VaultSharedFrozenRoot(
            root_hex=root,
            seed_paths=("a/x", "a/y"),
            leaf_hashes_hex=tuple(leaves),
            inclusion_proofs=proofs,
            content_hashes_hex={"a/x": "11" * 64, "a/y": "22" * 64},
        )
        assert fr.root_hex == root
        assert verify_inclusion(leaves[0], 0, fr.inclusion_proofs["a/x"], fr.root_hex)


# ---------------------------------------------------------------------------
# freeze_vault_shared
# ---------------------------------------------------------------------------


class TestFreezeVaultShared:
    def test_happy_path_returns_frozen_root(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        fr = freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        assert isinstance(fr, VaultSharedFrozenRoot)
        assert fr.root_hex == manifest.head_hash
        assert set(fr.seed_paths) == {s.relative_path for s in seeds}
        for s in seeds:
            assert fr.content_hashes_hex[s.relative_path] == s.content_hash

    def test_rejects_manifest_head_hash_drift(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds, head_hash="00" * 64)
        with pytest.raises(SeedManifestHeadDrift) as excinfo:
            freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        assert excinfo.value.code == F_MIRROR_02

    def test_rejects_when_disk_content_hash_differs_from_manifest(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        # Tamper one file *after* manifest is built — disk now disagrees.
        target = shared / seeds[0].relative_path
        target.write_bytes(b"tampered\n")
        with pytest.raises(M15Error) as excinfo:
            freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        assert excinfo.value.code == F_M15_01

    def test_rejects_when_extra_unlisted_file_under_seed_partition(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        rogue = shared / "cedar" / "rogue.cedar"
        rogue.write_bytes(b"rogue\n")
        with pytest.raises(SeedFileExtraOnDisk) as excinfo:
            freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        assert excinfo.value.code == F_M15_01

    def test_skips_cache_partition_files(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        # cached_opportunities/ is a CACHE partition — extra files there are OK.
        cache_dir = shared / "cached_opportunities"
        cache_dir.mkdir()
        (cache_dir / "rfa-1.json").write_bytes(b"{}")
        # research_db/ minus seed/ is also CACHE.
        rdb = shared / "research_db" / "index.sqlite"
        rdb.parent.mkdir(parents=True)
        rdb.write_bytes(b"sqlite-stub")
        # Should still freeze cleanly.
        fr = freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        assert fr.root_hex == manifest.head_hash

    def test_rejects_when_listed_seed_file_missing_on_disk(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        (shared / seeds[0].relative_path).unlink()
        with pytest.raises(M15Error) as excinfo:
            freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        assert excinfo.value.code == F_M15_01

    def test_arg_type_gate(self) -> None:
        with pytest.raises(TypeError):
            freeze_vault_shared(manifest=None, vault_shared_root=Path("/tmp"))  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            freeze_vault_shared(manifest="not-a-manifest", vault_shared_root=Path("/tmp"))  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# §9 step 6 — defence-in-depth identity-tuple re-capture on seed files
# ---------------------------------------------------------------------------


def _forge_identity_tuple(
    base: IdentityTuple, *, field: str, poison: str
) -> IdentityTuple:
    """Return a copy of ``base`` with one field mutated to ``poison``.

    Used to simulate filesystem-layer substitution (bind-mount swap, mount-
    table manipulation) that preserves content bytes but changes the
    underlying inode identity.
    """
    kwargs = {
        "volume_uuid": base.volume_uuid,
        "fs_file_id": base.fs_file_id,
        "mount_id": base.mount_id,
        "fs_type": base.fs_type,
        "captured_at": base.captured_at,
    }
    kwargs[field] = poison
    return IdentityTuple(**kwargs)


class TestFreezeVaultSharedIdentityDrift:
    """§9 step 6 — identity-tuple re-capture per-seed-file.

    Each seed file's manifest-recorded identity tuple must match the
    freshly-resolved tuple at freeze time; any drift in volume_uuid,
    fs_file_id, mount_id, or fs_type raises SeedFileIdentityDrift.
    """

    @pytest.mark.parametrize(
        "field",
        ["volume_uuid", "fs_file_id", "mount_id", "fs_type"],
    )
    def test_identity_drift_on_any_of_four_fields_raises(
        self,
        seeded_shared: tuple[Path, list[SeedFile]],
        field: str,
    ) -> None:
        shared, seeds = seeded_shared
        # Re-seed one file with a forged identity tuple that will not match
        # resolve_identity_tuple at freeze time.
        bogus_tuple = _forge_identity_tuple(
            seeds[0].identity_tuple, field=field, poison="POISON_VALUE"
        )
        poisoned = SeedFile(
            relative_path=seeds[0].relative_path,
            content_hash=seeds[0].content_hash,
            size_bytes=seeds[0].size_bytes,
            mode=seeds[0].mode,
            identity_tuple=bogus_tuple,
        )
        replaced = [poisoned] + list(seeds[1:])
        manifest = _build_manifest(replaced)
        with pytest.raises(SeedFileIdentityDrift) as excinfo:
            freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        assert excinfo.value.code == F_M15_01
        assert seeds[0].relative_path in str(excinfo.value)

    def test_identity_drift_error_subclasses_m15_error(self) -> None:
        """Ensures the new exception participates in the existing F-M15-*
        family-catch idiom the caller uses at §9 step 6."""
        assert issubclass(SeedFileIdentityDrift, M15Error)

    def test_all_four_fields_matching_passes(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        # Sanity: when the manifest identity tuple matches live, freeze passes.
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        fr = freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        assert isinstance(fr, VaultSharedFrozenRoot)


# ---------------------------------------------------------------------------
# reverify_path
# ---------------------------------------------------------------------------


class TestReverifyPath:
    def test_unchanged_file_reverifies_true(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        fr = freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        assert reverify_path(
            frozen_root=fr,
            vault_shared_root=shared,
            relative_path=seeds[0].relative_path,
        ) is True

    def test_post_freeze_mutation_reverifies_false(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        fr = freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        # tamper after freeze
        (shared / seeds[1].relative_path).write_bytes(b"after-freeze-tamper\n")
        assert reverify_path(
            frozen_root=fr,
            vault_shared_root=shared,
            relative_path=seeds[1].relative_path,
        ) is False

    def test_unknown_path_reverifies_false(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        fr = freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        assert reverify_path(
            frozen_root=fr,
            vault_shared_root=shared,
            relative_path="cedar/never_listed.cedar",
        ) is False


# ---------------------------------------------------------------------------
# make_post_gate_hook (binds to FDBroker)
# ---------------------------------------------------------------------------


def _hook_request(
    requested_path: str,
    *,
    skill: str = "vault-query",
    intent: str = "read",
) -> FDBrokerRequest:
    return FDBrokerRequest(
        requester_skill=skill,
        requester_pid=os.getpid(),
        requester_session_id="sess-hook",
        requester_org_slug="demo",
        requested_path=requested_path,
        intent=intent,
        nonce_hex="b" * 64,
    )


class TestPostGateHook:
    def test_hook_passes_paths_outside_vault_shared(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        fr = freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        hook = make_post_gate_hook(frozen_root=fr, vault_shared_root=shared)
        req = _hook_request("orgs/demo/vault/note.txt")
        assert hook(req) is True

    def test_hook_passes_cache_partition_under_vault_shared(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        fr = freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        hook = make_post_gate_hook(frozen_root=fr, vault_shared_root=shared)
        # cached_opportunities/ is cache → hook must allow.
        req = _hook_request("vault_shared/cached_opportunities/rfa-1.json")
        assert hook(req) is True

    def test_hook_passes_seed_path_when_unchanged(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        fr = freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        hook = make_post_gate_hook(frozen_root=fr, vault_shared_root=shared)
        req = _hook_request(f"vault_shared/{seeds[0].relative_path}")
        assert hook(req) is True

    def test_hook_vetoes_seed_path_when_tampered_after_freeze(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        fr = freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        hook = make_post_gate_hook(frozen_root=fr, vault_shared_root=shared)
        (shared / seeds[2].relative_path).write_bytes(b"tampered-mid-session\n")
        req = _hook_request(f"vault_shared/{seeds[2].relative_path}")
        assert hook(req) is False

    def test_hook_vetoes_seed_path_for_unlisted_seed_file(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        fr = freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        hook = make_post_gate_hook(frozen_root=fr, vault_shared_root=shared)
        # Even if a file appears later under a seed-partition path, it's not in
        # the manifest → the hook must veto access.
        late = shared / "cedar" / "after_boot.cedar"
        late.write_bytes(b"late\n")
        req = _hook_request("vault_shared/cedar/after_boot.cedar")
        assert hook(req) is False

    def test_hook_signature_is_callable_taking_request(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        fr = freeze_vault_shared(manifest=manifest, vault_shared_root=shared)
        hook = make_post_gate_hook(frozen_root=fr, vault_shared_root=shared)
        # match the broker's PostGateHook protocol.
        from pipeline.vault.fd_broker import FDBroker
        from pipeline.vault.gate_and_open import open_vault_root

        # Use a workspace-rooted broker — vault_shared lives under the workspace.
        workspace = shared.parent
        root_fd = open_vault_root(workspace)
        try:
            broker = FDBroker(
                vault_root_fd=root_fd, vault_root_path=workspace, post_gate_hook=hook
            )
            assert broker is not None
        finally:
            os.close(root_fd)


# ---------------------------------------------------------------------------
# verify_trust_root_mirror (§2.5)
# ---------------------------------------------------------------------------


@pytest.fixture
def mirror_setup(tmp_path: Path) -> tuple[Path, bytes, IdentityTuple]:
    mirror_dir = tmp_path / "logician_trust_root"
    mirror_dir.mkdir()
    mirror_file = mirror_dir / "router.yaml"
    body = b"version: v1\nseats:\n  scribe: anthropic\n"
    mirror_file.write_bytes(body)
    tup = resolve_identity_tuple(mirror_file)
    return mirror_file, body, tup


def _signature_verifier_factory(
    *, ok: bool
) -> Callable[[bytes, str], bool]:
    def _verify(payload: bytes, signature: str) -> bool:
        # Treat signature 'GOOD' / 'BAD' for tests; ignore actual crypto.
        if not ok:
            return False
        return signature == "GOOD"

    return _verify


class TestVerifyTrustRootMirror:
    def test_happy_path_returns_none(
        self, mirror_setup: tuple[Path, bytes, IdentityTuple]
    ) -> None:
        mirror_path, body, tup = mirror_setup
        manifest = TrustRootMirrorManifest(
            mirror_path=str(mirror_path),
            content_hash=_sha3_512_hex(body),
            identity_tuple=tup,
            m15_ledger_head="ledger",
            operator_signature="GOOD",
            signed_at="2026-04-19T00:00:00Z",
            immutability_flag_set=True,
        )
        # Returns None on success (raise on failure pattern).
        assert (
            verify_trust_root_mirror(
                manifest=manifest,
                live_mirror_path=mirror_path,
                verify_signature=_signature_verifier_factory(ok=True),
                last_boot_wall_ns=0,
                current_boot_wall_ns=10,
                clock_rollback_tolerance_seconds=300,
            )
            is None
        )

    def test_content_mismatch_raises_f_mirror_02(
        self, mirror_setup: tuple[Path, bytes, IdentityTuple]
    ) -> None:
        mirror_path, body, tup = mirror_setup
        manifest = TrustRootMirrorManifest(
            mirror_path=str(mirror_path),
            content_hash="00" * 64,  # wrong
            identity_tuple=tup,
            m15_ledger_head="ledger",
            operator_signature="GOOD",
            signed_at="2026-04-19T00:00:00Z",
            immutability_flag_set=True,
        )
        with pytest.raises(MirrorContentMismatch) as excinfo:
            verify_trust_root_mirror(
                manifest=manifest,
                live_mirror_path=mirror_path,
                verify_signature=_signature_verifier_factory(ok=True),
                last_boot_wall_ns=0,
                current_boot_wall_ns=10,
                clock_rollback_tolerance_seconds=300,
            )
        assert excinfo.value.code == F_MIRROR_02

    def test_identity_mismatch_raises_f_mirror_01(
        self, mirror_setup: tuple[Path, bytes, IdentityTuple]
    ) -> None:
        mirror_path, body, tup = mirror_setup
        bogus_tup = dataclasses.replace(tup, fs_file_id="ff" * 8)
        manifest = TrustRootMirrorManifest(
            mirror_path=str(mirror_path),
            content_hash=_sha3_512_hex(body),
            identity_tuple=bogus_tup,
            m15_ledger_head="ledger",
            operator_signature="GOOD",
            signed_at="2026-04-19T00:00:00Z",
            immutability_flag_set=True,
        )
        with pytest.raises(MirrorIdentityMismatch) as excinfo:
            verify_trust_root_mirror(
                manifest=manifest,
                live_mirror_path=mirror_path,
                verify_signature=_signature_verifier_factory(ok=True),
                last_boot_wall_ns=0,
                current_boot_wall_ns=10,
                clock_rollback_tolerance_seconds=300,
            )
        assert excinfo.value.code == F_MIRROR_01

    def test_bad_signature_raises_f_mirror_03(
        self, mirror_setup: tuple[Path, bytes, IdentityTuple]
    ) -> None:
        mirror_path, body, tup = mirror_setup
        manifest = TrustRootMirrorManifest(
            mirror_path=str(mirror_path),
            content_hash=_sha3_512_hex(body),
            identity_tuple=tup,
            m15_ledger_head="ledger",
            operator_signature="BAD",
            signed_at="2026-04-19T00:00:00Z",
            immutability_flag_set=True,
        )
        with pytest.raises(MirrorSignatureInvalid) as excinfo:
            verify_trust_root_mirror(
                manifest=manifest,
                live_mirror_path=mirror_path,
                verify_signature=_signature_verifier_factory(ok=True),
                last_boot_wall_ns=0,
                current_boot_wall_ns=10,
                clock_rollback_tolerance_seconds=300,
            )
        assert excinfo.value.code == F_MIRROR_03

    def test_immutability_missing_raises_f_mirror_04(
        self, mirror_setup: tuple[Path, bytes, IdentityTuple]
    ) -> None:
        mirror_path, body, tup = mirror_setup
        manifest = TrustRootMirrorManifest(
            mirror_path=str(mirror_path),
            content_hash=_sha3_512_hex(body),
            identity_tuple=tup,
            m15_ledger_head="ledger",
            operator_signature="GOOD",
            signed_at="2026-04-19T00:00:00Z",
            immutability_flag_set=False,
        )
        with pytest.raises(MirrorImmutabilityMissing) as excinfo:
            verify_trust_root_mirror(
                manifest=manifest,
                live_mirror_path=mirror_path,
                verify_signature=_signature_verifier_factory(ok=True),
                last_boot_wall_ns=0,
                current_boot_wall_ns=10,
                clock_rollback_tolerance_seconds=300,
            )
        assert excinfo.value.code == F_MIRROR_04

    def test_clock_rollback_raises_f_mirror_05(
        self, mirror_setup: tuple[Path, bytes, IdentityTuple]
    ) -> None:
        mirror_path, body, tup = mirror_setup
        manifest = TrustRootMirrorManifest(
            mirror_path=str(mirror_path),
            content_hash=_sha3_512_hex(body),
            identity_tuple=tup,
            m15_ledger_head="ledger",
            operator_signature="GOOD",
            signed_at="2026-04-19T00:00:00Z",
            immutability_flag_set=True,
        )
        # current boot wall is far earlier than last recorded boot → rollback.
        last_boot = 10 * 10**9  # 10 s in ns
        current_boot = 1  # ns
        with pytest.raises(MirrorClockRollback) as excinfo:
            verify_trust_root_mirror(
                manifest=manifest,
                live_mirror_path=mirror_path,
                verify_signature=_signature_verifier_factory(ok=True),
                last_boot_wall_ns=last_boot,
                current_boot_wall_ns=current_boot,
                clock_rollback_tolerance_seconds=1,
            )
        assert excinfo.value.code == F_MIRROR_05

    def test_arg_type_gates(
        self, mirror_setup: tuple[Path, bytes, IdentityTuple]
    ) -> None:
        mirror_path, body, tup = mirror_setup
        manifest = TrustRootMirrorManifest(
            mirror_path=str(mirror_path),
            content_hash=_sha3_512_hex(body),
            identity_tuple=tup,
            m15_ledger_head="ledger",
            operator_signature="GOOD",
            signed_at="2026-04-19T00:00:00Z",
            immutability_flag_set=True,
        )
        with pytest.raises(TypeError):
            verify_trust_root_mirror(
                manifest=manifest,
                live_mirror_path="not-a-path",  # type: ignore[arg-type]
                verify_signature=_signature_verifier_factory(ok=True),
                last_boot_wall_ns=0,
                current_boot_wall_ns=10,
                clock_rollback_tolerance_seconds=300,
            )
        with pytest.raises(TypeError):
            verify_trust_root_mirror(
                manifest=manifest,
                live_mirror_path=mirror_path,
                verify_signature="not-callable",  # type: ignore[arg-type]
                last_boot_wall_ns=0,
                current_boot_wall_ns=10,
                clock_rollback_tolerance_seconds=300,
            )


# ---------------------------------------------------------------------------
# Exception class taxonomy (anchors back to MirrorError parent)
# ---------------------------------------------------------------------------


class TestExceptionTaxonomy:
    def test_all_mirror_exceptions_inherit_mirror_error(self) -> None:
        for cls in (
            MirrorContentMismatch,
            MirrorIdentityMismatch,
            MirrorSignatureInvalid,
            MirrorImmutabilityMissing,
            MirrorClockRollback,
            SeedManifestHeadDrift,
        ):
            assert issubclass(cls, MirrorError)

    def test_seed_extra_inherits_m15_error(self) -> None:
        assert issubclass(SeedFileExtraOnDisk, M15Error)


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        from pipeline.vault import mirror_verify as _mod

        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
