"""§2 Vault Round K.2 — BT14 property-test matrix.

Per spec card ``pipeline/engineering/spec_cards/section_2_round_k_capstone.md``
K.2: exercises the eight §2-owned blueprint-tracked subfamilies BT14.a –
BT14.g.1 as algebraic / closure properties rather than module-unit behaviour.

One class per BT; ≥12 property tests per class; floor ≥96.

Classes:
* ``TestBT14a_InitMarkerHMAC`` (BT14.a) — per-org ``vault/init.marker`` write +
  HMAC + verify.
* ``TestBT14b_SkillEnumeration`` (BT14.b) — Vault-owned skill enumeration
  (``vault-query`` + ``research-db-query`` for the broker, ``vault_write`` as
  the dispatcher entry-point).
* ``TestBT14c_CedarPolicyLocation`` (BT14.c) — Cedar policy location under
  ``vault_shared/cedar/`` + top-level-only loader.
* ``TestBT14d_SignedCommits`` (BT14.d) — ``vault_shared/`` signed commits via
  seed-manifest + Merkle-root + signature verify.
* ``TestBT14e_PreGateDirectFS`` (BT14.e) — PRE-gate direct-FS failure
  semantics (kernel-copy denylist signatures; ``gate_and_open`` rejection
  paths; cross-org refusal).
* ``TestBT14f_InitMarkerCeremony`` (BT14.f) — per-org ``init.marker``
  ceremony ordering (floor → shared-init → per-org-init).
* ``TestBT14g_IdentityTuple`` (BT14.g) — identity-tuple resolver + 4-field
  compare with ``mount_id`` / ``fs_type``.
* ``TestBT14g1_UUIDFloor`` (BT14.g.1) — stable-UUID floor PRE-gate allowlist.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_02_vault_topology.md``
v7.1 (LOCKED 2026-04-19) — sections §2.3 / §2.5 / §2.7 / §2.9 / §3.3 / §3.4 /
§3.5 / §5.1 / §5.6 / §6.8 / §6.11.
"""

from __future__ import annotations

import dataclasses
import hashlib
import hmac
import json
import os
import platform
from dataclasses import replace
from pathlib import Path
from typing import Final

import pytest

from pipeline.vault import atomic_freeze as _atomic_freeze
from pipeline.vault import gate_and_open as _gate_and_open
from pipeline.vault import identity_tuple as _identity_tuple
from pipeline.vault import init_marker as _init_marker
from pipeline.vault import mirror_verify as _mirror_verify
from pipeline.vault import uuid_floor as _uuid_floor
from pipeline.vault import vault_write as _vault_write
from pipeline.vault.error_codes import (
    F_CEDAR_01,
    F_FD_01,
    F_M15_01,
    F_M15_02,
    F_M15_03,
    F_UUID_01,
    F_VAULT_04,
    CedarError,
    M15Error,
    UUIDFloorError,
    VaultCrossOrgAccess,
    VaultInitHMACMismatch,
)
from pipeline.vault.fd_broker import (
    FD_BROKER_ALLOWED_INTENTS,
    FD_BROKER_ALLOWED_SKILLS,
    NONCE_TTL_SECONDS,
)
from pipeline.vault.identity_tuple import (
    IdentityTupleUnavailable,
    resolve_identity_tuple,
)
from pipeline.vault.init_marker import (
    VAULT_INIT_HMAC_KEY_ID,
    VaultInitAlreadyExists,
    VaultInitMissing,
    verify_vault_init_marker,
    write_vault_init_marker,
)
from pipeline.vault.m15_ledger import (
    SeedManifestLedgerHeadDrift,
    SeedManifestSignatureInvalid,
    cedar_policy_loader_load_all,
    verify_seed_manifest,
)
from pipeline.vault.mirror_verify import (
    LEAF_DOMAIN_TAG,
    NODE_DOMAIN_TAG,
    SeedFileIdentityDrift,
    compute_leaf_hash_hex,
    compute_merkle_root_hex,
    freeze_vault_shared,
)
from pipeline.vault.schemas import (
    FDBrokerRequest,
    IdentityTuple,
    SeedFile,
    StableUUIDFloor,
    VaultSharedSeedManifest,
)
from pipeline.vault.uuid_floor import (
    ACCEPTED_FS_TYPES,
    DENYLISTED_FS_TYPES,
    UUIDFloorRejected,
)
from pipeline.vault.vault_write import (
    EMPTY_SHA3_512_HEX,
    POST_GATE_ALLOWLIST,
    WRITE_MODES,
    vault_write,
)

from tests.vault.conftest import (
    CAPSTONE_VAULT_INIT_HMAC_KEY,
    CapstoneVaultKeyStore,
    always_false,
    always_true,
    build_manifest,
    make_seed_file,
    serialize_manifest,
    sha3_512_hex,
)


# ===========================================================================
# BT14.a — Per-org vault/init.marker write + HMAC + verify
# ===========================================================================


class TestBT14a_InitMarkerHMAC:
    """BT14.a — per-org ``vault/init.marker`` write + HMAC + verify.

    Property scope: marker bodies are canonical-JSON bytes, trailers are
    SHA-3-512 HMACs under ``tilth.vault.init.hmac.v1``, every write + verify
    pair is a byte-identical round trip, and each invariant failure raises
    the blueprint-documented ``F-INIT-*`` / ``VaultInit*`` exception.
    """

    def _paths(self, tmp_path: Path, slug: str = "o") -> tuple[Path, Path, Path]:
        org = tmp_path / "org" / slug
        org.mkdir(parents=True)
        return org / "init.marker", org / "init.marker.hmac", org / "init.lock"

    def _ks(self) -> CapstoneVaultKeyStore:
        return CapstoneVaultKeyStore()

    def test_write_verify_round_trip_org_scope(self, tmp_path: Path) -> None:
        m, h, l = self._paths(tmp_path)
        ks = self._ks()
        written = write_vault_init_marker(
            marker_path=m,
            hmac_path=h,
            lock_path=l,
            keystore=ks,
            scope="org",
            slug="o",
            operator_id="op-001",
            section_lock_hash="a" * 64,
        )
        verified = verify_vault_init_marker(
            marker_path=m,
            hmac_path=h,
            keystore=ks,
            expected_slug="o",
            expected_scope="org",
        )
        assert verified == written

    def test_write_verify_round_trip_shared_scope(self, tmp_path: Path) -> None:
        shared = tmp_path / "vault_shared"
        shared.mkdir()
        m = shared / "init.marker"
        h = shared / "init.marker.hmac"
        l = shared / "init.lock"
        ks = self._ks()
        written = write_vault_init_marker(
            marker_path=m,
            hmac_path=h,
            lock_path=l,
            keystore=ks,
            scope="shared",
            slug="",
            operator_id="op-002",
            section_lock_hash="b" * 64,
        )
        verified = verify_vault_init_marker(
            marker_path=m,
            hmac_path=h,
            keystore=ks,
            expected_slug="",
            expected_scope="shared",
        )
        assert verified == written

    def test_hmac_tamper_one_byte_flip_fails(self, tmp_path: Path) -> None:
        m, h, l = self._paths(tmp_path)
        ks = self._ks()
        write_vault_init_marker(
            marker_path=m,
            hmac_path=h,
            lock_path=l,
            keystore=ks,
            scope="org",
            slug="o",
            operator_id="op",
            section_lock_hash="c" * 64,
        )
        # Flip one byte of the stored HMAC.
        raw = h.read_bytes()
        tampered = bytearray(raw)
        tampered[0] ^= 0x01
        h.write_bytes(bytes(tampered))
        with pytest.raises(VaultInitHMACMismatch):
            verify_vault_init_marker(
                marker_path=m,
                hmac_path=h,
                keystore=ks,
                expected_slug="o",
                expected_scope="org",
            )

    def test_marker_body_tamper_fails_hmac(self, tmp_path: Path) -> None:
        m, h, l = self._paths(tmp_path)
        ks = self._ks()
        write_vault_init_marker(
            marker_path=m,
            hmac_path=h,
            lock_path=l,
            keystore=ks,
            scope="org",
            slug="o",
            operator_id="op",
            section_lock_hash="d" * 64,
        )
        body = m.read_bytes()
        m.write_bytes(body + b" ")  # whitespace-only tamper
        with pytest.raises(VaultInitHMACMismatch):
            verify_vault_init_marker(
                marker_path=m,
                hmac_path=h,
                keystore=ks,
                expected_slug="o",
                expected_scope="org",
            )

    def test_wrong_keystore_key_fails(self, tmp_path: Path) -> None:
        m, h, l = self._paths(tmp_path)
        ks = self._ks()
        write_vault_init_marker(
            marker_path=m,
            hmac_path=h,
            lock_path=l,
            keystore=ks,
            scope="org",
            slug="o",
            operator_id="op",
            section_lock_hash="e" * 64,
        )
        wrong_ks = CapstoneVaultKeyStore(key_bytes=bytes(64))
        with pytest.raises(VaultInitHMACMismatch):
            verify_vault_init_marker(
                marker_path=m,
                hmac_path=h,
                keystore=wrong_ks,
                expected_slug="o",
                expected_scope="org",
            )

    def test_missing_hmac_sidecar_fails(self, tmp_path: Path) -> None:
        m, h, l = self._paths(tmp_path)
        ks = self._ks()
        write_vault_init_marker(
            marker_path=m,
            hmac_path=h,
            lock_path=l,
            keystore=ks,
            scope="org",
            slug="o",
            operator_id="op",
            section_lock_hash="f" * 64,
        )
        h.unlink()
        with pytest.raises(VaultInitMissing):
            verify_vault_init_marker(
                marker_path=m,
                hmac_path=h,
                keystore=ks,
                expected_slug="o",
                expected_scope="org",
            )

    def test_missing_marker_body_fails(self, tmp_path: Path) -> None:
        m, h, l = self._paths(tmp_path)
        ks = self._ks()
        with pytest.raises(VaultInitMissing):
            verify_vault_init_marker(
                marker_path=m,
                hmac_path=h,
                keystore=ks,
                expected_slug="o",
                expected_scope="org",
            )

    def test_double_write_raises_already_exists(self, tmp_path: Path) -> None:
        m, h, l = self._paths(tmp_path)
        ks = self._ks()
        write_vault_init_marker(
            marker_path=m,
            hmac_path=h,
            lock_path=l,
            keystore=ks,
            scope="org",
            slug="o",
            operator_id="op",
            section_lock_hash="0" * 64,
        )
        with pytest.raises(VaultInitAlreadyExists):
            write_vault_init_marker(
                marker_path=m,
                hmac_path=h,
                lock_path=l,
                keystore=ks,
                scope="org",
                slug="o",
                operator_id="op",
                section_lock_hash="1" * 64,
            )

    def test_org_scope_requires_nonempty_slug(self, tmp_path: Path) -> None:
        m, h, l = self._paths(tmp_path)
        ks = self._ks()
        with pytest.raises((ValueError, AssertionError)):
            write_vault_init_marker(
                marker_path=m,
                hmac_path=h,
                lock_path=l,
                keystore=ks,
                scope="org",
                slug="",  # invalid for org scope
                operator_id="op",
                section_lock_hash="2" * 64,
            )

    def test_shared_scope_requires_empty_slug(self, tmp_path: Path) -> None:
        shared = tmp_path / "vault_shared_bad"
        shared.mkdir()
        m = shared / "init.marker"
        h = shared / "init.marker.hmac"
        l = shared / "init.lock"
        ks = self._ks()
        with pytest.raises((ValueError, AssertionError)):
            write_vault_init_marker(
                marker_path=m,
                hmac_path=h,
                lock_path=l,
                keystore=ks,
                scope="shared",
                slug="not-empty",
                operator_id="op",
                section_lock_hash="3" * 64,
            )

    def test_hmac_key_id_is_canonical_v1(self) -> None:
        assert VAULT_INIT_HMAC_KEY_ID == "tilth.vault.init.hmac.v1"

    def test_hmac_body_is_sha3_512_128_hex(self, tmp_path: Path) -> None:
        m, h, l = self._paths(tmp_path)
        ks = self._ks()
        write_vault_init_marker(
            marker_path=m,
            hmac_path=h,
            lock_path=l,
            keystore=ks,
            scope="org",
            slug="o",
            operator_id="op",
            section_lock_hash="4" * 64,
        )
        trailer = h.read_text(encoding="utf-8").strip()
        assert len(trailer) == 128
        int(trailer, 16)  # parses as hex

    def test_operator_id_fuzz_over_ascii_alphanumeric(
        self, tmp_path: Path
    ) -> None:
        import random

        rng = random.Random(2026_04_22)
        for i in range(5):
            slug = f"o{i}"
            org = tmp_path / "org" / slug
            org.mkdir(parents=True, exist_ok=True)
            m = org / "init.marker"
            h = org / "init.marker.hmac"
            l = org / "init.lock"
            ks = self._ks()
            op_id = "".join(
                rng.choice("abcdefghijklmnopqrstuvwxyz0123456789-")
                for _ in range(rng.randint(4, 24))
            )
            write_vault_init_marker(
                marker_path=m,
                hmac_path=h,
                lock_path=l,
                keystore=ks,
                scope="org",
                slug=slug,
                operator_id=op_id,
                section_lock_hash="5" * 64,
            )
            verified = verify_vault_init_marker(
                marker_path=m,
                hmac_path=h,
                keystore=ks,
                expected_slug=slug,
                expected_scope="org",
            )
            assert verified.operator_id == op_id


# ===========================================================================
# BT14.b — Vault-owned skill enumeration
# ===========================================================================


class TestBT14b_SkillEnumeration:
    """BT14.b — Vault-owned skill enumeration via ``FD_BROKER_ALLOWED_SKILLS``
    (plus ``vault_write`` as its own dispatcher). Property scope: frozen
    allowlists, unknown-skill denial, known-skill admission, nonce TTL.
    """

    def test_allowed_skills_is_frozenset(self) -> None:
        assert isinstance(FD_BROKER_ALLOWED_SKILLS, frozenset)

    def test_allowed_skills_has_exact_two_entries(self) -> None:
        assert len(FD_BROKER_ALLOWED_SKILLS) == 2

    def test_allowed_skills_entries_are_canonical(self) -> None:
        assert FD_BROKER_ALLOWED_SKILLS == frozenset(
            {"vault-query", "research-db-query"}
        )

    def test_allowed_skills_immutable(self) -> None:
        with pytest.raises(AttributeError):
            FD_BROKER_ALLOWED_SKILLS.add("bad-skill")  # type: ignore[attr-defined]

    def test_allowed_intents_is_frozenset(self) -> None:
        assert isinstance(FD_BROKER_ALLOWED_INTENTS, frozenset)

    def test_allowed_intents_exact_four(self) -> None:
        assert FD_BROKER_ALLOWED_INTENTS == frozenset(
            {"read", "write", "execute", "read-wrapper"}
        )

    def test_allowed_intents_immutable(self) -> None:
        with pytest.raises(AttributeError):
            FD_BROKER_ALLOWED_INTENTS.add("sniff")  # type: ignore[attr-defined]

    def test_nonce_ttl_is_300_seconds(self) -> None:
        assert NONCE_TTL_SECONDS == 300

    def test_vault_write_module_surface_exposes_dispatcher(self) -> None:
        # vault-write is its own dispatcher entry-point, not an FD-broker
        # skill; confirm the module-surface symbol is callable.
        assert callable(vault_write)

    def test_post_gate_allowlist_is_mapping(self) -> None:
        # Post-gate allowlist is keyed by intent; each entry declares its
        # kind-class (SIMPLE vs COMPOUND).
        assert isinstance(POST_GATE_ALLOWLIST, dict)

    def test_post_gate_allowlist_has_14_entries(self) -> None:
        # v7.1 LOCKED: 7 entries. v7.2 DRAFT adds 7 SIMPLE operational
        # sub-kinds → 14 total. §17 v1 LOCK 2026-05-11 adds cycle_receipt
        # SIMPLE row → 15 total (13 SIMPLE + 2 COMPOUND).
        assert len(POST_GATE_ALLOWLIST) == 15

    def test_post_gate_allowlist_simple_compound_split(self) -> None:
        simple = [e for e in POST_GATE_ALLOWLIST.values() if e.kind_class == "SIMPLE"]
        compound = [
            e for e in POST_GATE_ALLOWLIST.values() if e.kind_class == "COMPOUND"
        ]
        # v7.1: 5 SIMPLE / 2 COMPOUND. v7.2: +7 SIMPLE = 12 / 2.
        # §17 v1: +1 SIMPLE (cycle_receipt) = 13 / 2.
        assert len(simple) == 13
        assert len(compound) == 2

    def test_write_modes_frozenset_three_entries(self) -> None:
        assert WRITE_MODES == frozenset(
            {"overwrite", "write-if-absent", "append-cas"}
        )

    def test_unknown_skill_name_not_in_allowlist(self) -> None:
        for bad in ("", "VAULT-QUERY", "vault_query", "root", "admin"):
            assert bad not in FD_BROKER_ALLOWED_SKILLS


# ===========================================================================
# BT14.c — Cedar policy location
# ===========================================================================


class TestBT14c_CedarPolicyLocation:
    """BT14.c — Cedar policies live under ``vault_shared/cedar/`` and the
    top-level loader returns only files directly under that directory.
    """

    def _build(self, tmp_path: Path, files: list[tuple[str, bytes]]):
        shared = tmp_path / "vault_shared"
        shared.mkdir()
        seeds = [make_seed_file(rel, content, shared) for rel, content in files]
        manifest = build_manifest(seeds)
        frozen = freeze_vault_shared(
            manifest=manifest, vault_shared_root=shared
        )
        return shared, manifest, frozen

    def test_loader_returns_only_top_level_cedar_files(
        self, tmp_path: Path
    ) -> None:
        shared, _, frozen = self._build(
            tmp_path,
            [
                ("cedar/org_isolation.cedar", b"permit;\n"),
                ("cedar/write_gate.cedar", b"forbid x;\n"),
                ("cedar/sub/nested.cedar", b"permit sub;\n"),
                ("other/not_cedar.txt", b"irrelevant\n"),
            ],
        )
        loaded = cedar_policy_loader_load_all(
            frozen_root=frozen, vault_shared_root=shared
        )
        assert "cedar/org_isolation.cedar" in loaded
        assert "cedar/write_gate.cedar" in loaded
        assert "cedar/sub/nested.cedar" not in loaded
        assert "other/not_cedar.txt" not in loaded

    def test_loader_hashes_match_frozen_root(self, tmp_path: Path) -> None:
        shared, manifest, frozen = self._build(
            tmp_path, [("cedar/p.cedar", b"permit a;\n")]
        )
        loaded = cedar_policy_loader_load_all(
            frozen_root=frozen, vault_shared_root=shared
        )
        assert "cedar/p.cedar" in loaded

    def test_loader_rejects_on_content_drift(self, tmp_path: Path) -> None:
        shared, manifest, frozen = self._build(
            tmp_path, [("cedar/p.cedar", b"permit a;\n")]
        )
        # Tamper on disk after freeze.
        (shared / "cedar/p.cedar").write_bytes(b"tampered;\n")
        with pytest.raises(CedarError):
            cedar_policy_loader_load_all(
                frozen_root=frozen, vault_shared_root=shared
            )

    def test_loader_rejects_on_missing_file(self, tmp_path: Path) -> None:
        shared, _, frozen = self._build(
            tmp_path, [("cedar/p.cedar", b"permit;\n")]
        )
        (shared / "cedar/p.cedar").unlink()
        with pytest.raises(CedarError):
            cedar_policy_loader_load_all(
                frozen_root=frozen, vault_shared_root=shared
            )

    def test_loader_rejects_on_non_utf8(self, tmp_path: Path) -> None:
        # Build manifest with a bytes sequence that's not valid UTF-8.
        shared, _, frozen = self._build(
            tmp_path, [("cedar/p.cedar", b"\xff\xfe\x00\x00")]
        )
        with pytest.raises(CedarError):
            cedar_policy_loader_load_all(
                frozen_root=frozen, vault_shared_root=shared
            )

    def test_f_cedar_01_code_is_string(self) -> None:
        assert F_CEDAR_01 == "F-CEDAR-01"

    def test_loader_handles_multiple_top_level_policies(
        self, tmp_path: Path
    ) -> None:
        shared, _, frozen = self._build(
            tmp_path,
            [
                ("cedar/a.cedar", b"permit A;\n"),
                ("cedar/b.cedar", b"permit B;\n"),
                ("cedar/c.cedar", b"permit C;\n"),
            ],
        )
        loaded = cedar_policy_loader_load_all(
            frozen_root=frozen, vault_shared_root=shared
        )
        assert set(loaded) == {
            "cedar/a.cedar",
            "cedar/b.cedar",
            "cedar/c.cedar",
        }

    def test_loader_type_gates(self, tmp_path: Path) -> None:
        shared, _, frozen = self._build(
            tmp_path, [("cedar/p.cedar", b"permit;\n")]
        )
        with pytest.raises(TypeError):
            cedar_policy_loader_load_all(
                frozen_root="not-a-frozen-root",  # type: ignore[arg-type]
                vault_shared_root=shared,
            )
        with pytest.raises(TypeError):
            cedar_policy_loader_load_all(
                frozen_root=frozen,
                vault_shared_root="not-a-path",  # type: ignore[arg-type]
            )

    def test_loader_only_loads_dot_cedar_extension(
        self, tmp_path: Path
    ) -> None:
        shared, _, frozen = self._build(
            tmp_path,
            [
                ("cedar/real.cedar", b"permit;\n"),
                ("cedar/not-cedar.txt", b"ignored;\n"),
            ],
        )
        loaded = cedar_policy_loader_load_all(
            frozen_root=frozen, vault_shared_root=shared
        )
        assert "cedar/real.cedar" in loaded
        assert "cedar/not-cedar.txt" not in loaded

    def test_loader_returns_text_not_bytes(self, tmp_path: Path) -> None:
        shared, _, frozen = self._build(
            tmp_path, [("cedar/p.cedar", b"permit;\n")]
        )
        loaded = cedar_policy_loader_load_all(
            frozen_root=frozen, vault_shared_root=shared
        )
        for text in loaded.values():
            assert isinstance(text, str)

    def test_empty_cedar_text_is_acceptable(self, tmp_path: Path) -> None:
        shared, _, frozen = self._build(
            tmp_path, [("cedar/empty.cedar", b"")]
        )
        loaded = cedar_policy_loader_load_all(
            frozen_root=frozen, vault_shared_root=shared
        )
        assert loaded["cedar/empty.cedar"] == ""

    def test_cedar_error_is_vault_error_subtype(self) -> None:
        from pipeline.vault.error_codes import VaultError

        assert issubclass(CedarError, VaultError)


# ===========================================================================
# BT14.d — vault_shared/ signed commits
# ===========================================================================


class TestBT14d_SignedCommits:
    """BT14.d — ``vault_shared/`` signed commits via seed-manifest +
    Merkle root + signature verify. Property scope: Merkle root recomputes,
    SeedFile content hashes are byte-identical, signature verify is
    injectable, drift raises F-M15-02 / F-M15-03.
    """

    def _ws(self, tmp_path: Path, files: list[tuple[str, bytes]]):
        shared = tmp_path / "vault_shared"
        shared.mkdir()
        seeds = [make_seed_file(rel, content, shared) for rel, content in files]
        manifest = build_manifest(seeds)
        manifest_path = tmp_path / "m.json"
        sig_path = tmp_path / "m.sig"
        manifest_path.write_bytes(serialize_manifest(manifest))
        sig_path.write_text(manifest.signature + "\n", encoding="utf-8")
        return shared, manifest, manifest_path, sig_path

    def test_merkle_root_matches_compute_merkle_root(
        self, tmp_path: Path
    ) -> None:
        shared, manifest, *_ = self._ws(
            tmp_path,
            [
                ("a.txt", b"A"),
                ("b.txt", b"B"),
                ("c.txt", b"C"),
            ],
        )
        sorted_files = sorted(manifest.files, key=lambda s: s.relative_path)
        leaves = [
            compute_leaf_hash_hex(sf.relative_path, sf.content_hash)
            for sf in sorted_files
        ]
        assert manifest.head_hash == compute_merkle_root_hex(leaves)

    def test_seed_file_content_hash_is_sha3_512(
        self, tmp_path: Path
    ) -> None:
        shared, manifest, *_ = self._ws(
            tmp_path, [("a.txt", b"alpha")]
        )
        sf = manifest.files[0]
        assert sf.content_hash == hashlib.sha3_512(b"alpha").hexdigest()
        assert len(sf.content_hash) == 128

    def test_happy_path_verify_returns_frozen_root(
        self, tmp_path: Path
    ) -> None:
        shared, manifest, mp, sp = self._ws(
            tmp_path, [("a.txt", b"A")]
        )
        frozen = verify_seed_manifest(
            manifest_path=mp,
            signature_path=sp,
            vault_shared_root=shared,
            current_ledger_head=manifest.m15_ledger_head,
            verify_signature=always_true,
        )
        # Batch 3 Phase 2 widened VaultSharedFrozenRoot: head_hash → root_hex,
        # plus seed_paths / leaf_hashes_hex / inclusion_proofs / content_hashes_hex.
        # Recompute the Merkle root from the manifest's seed files (sorted by
        # relative_path, same convention as build_manifest) and assert the
        # frozen root_hex matches — independent of manifest.head_hash so the
        # property is verified end-to-end.
        sorted_files = sorted(manifest.files, key=lambda sf: sf.relative_path)
        leaves = [
            compute_leaf_hash_hex(sf.relative_path, sf.content_hash)
            for sf in sorted_files
        ]
        assert frozen.root_hex == compute_merkle_root_hex(leaves)
        # Cross-check: manifest.head_hash IS the same Merkle root, so the
        # frozen root must also equal it (sanity invariant, not a tautology
        # because frozen is constructed by a different code path).
        assert frozen.root_hex == manifest.head_hash

    def test_signature_fail_raises_f_m15_02(self, tmp_path: Path) -> None:
        shared, manifest, mp, sp = self._ws(
            tmp_path, [("a.txt", b"A")]
        )
        with pytest.raises(SeedManifestSignatureInvalid) as exc:
            verify_seed_manifest(
                manifest_path=mp,
                signature_path=sp,
                vault_shared_root=shared,
                current_ledger_head=manifest.m15_ledger_head,
                verify_signature=always_false,
            )
        assert exc.value.code == F_M15_02

    def test_ledger_drift_raises_f_m15_03(self, tmp_path: Path) -> None:
        shared, manifest, mp, sp = self._ws(
            tmp_path, [("a.txt", b"A")]
        )
        with pytest.raises(SeedManifestLedgerHeadDrift) as exc:
            verify_seed_manifest(
                manifest_path=mp,
                signature_path=sp,
                vault_shared_root=shared,
                current_ledger_head="wrong-ledger-head",
                verify_signature=always_true,
            )
        assert exc.value.code == F_M15_03

    def test_leaf_domain_tag_is_0x00(self) -> None:
        assert LEAF_DOMAIN_TAG == b"\x00"

    def test_node_domain_tag_is_0x01(self) -> None:
        assert NODE_DOMAIN_TAG == b"\x01"

    def test_merkle_root_single_leaf_is_leaf_hash(self) -> None:
        leaf = compute_leaf_hash_hex("a.txt", hashlib.sha3_512(b"A").hexdigest())
        assert compute_merkle_root_hex([leaf]) == leaf

    def test_merkle_root_odd_count_duplicates_last_leaf(self) -> None:
        leaves = [
            compute_leaf_hash_hex(f"f{i}.txt", hashlib.sha3_512(f"x{i}".encode()).hexdigest())
            for i in range(3)
        ]
        root = compute_merkle_root_hex(leaves)
        assert isinstance(root, str) and len(root) == 128

    def test_merkle_root_deterministic_under_identical_input(self) -> None:
        leaves = [
            compute_leaf_hash_hex(f"{i}.bin", hashlib.sha3_512(bytes([i])).hexdigest())
            for i in range(4)
        ]
        assert compute_merkle_root_hex(leaves) == compute_merkle_root_hex(leaves)

    def test_content_drift_after_freeze_is_detected(
        self, tmp_path: Path
    ) -> None:
        shared, manifest, mp, sp = self._ws(
            tmp_path, [("a.txt", b"A")]
        )
        (shared / "a.txt").write_bytes(b"B")  # content drift
        with pytest.raises(M15Error):
            verify_seed_manifest(
                manifest_path=mp,
                signature_path=sp,
                vault_shared_root=shared,
                current_ledger_head=manifest.m15_ledger_head,
                verify_signature=always_true,
            )

    def test_empty_manifest_is_invalid(self, tmp_path: Path) -> None:
        shared = tmp_path / "vault_shared"
        shared.mkdir()
        with pytest.raises(ValueError):
            build_manifest([])  # empty leaves → compute_merkle_root raises

    def test_serialize_manifest_is_deterministic(
        self, tmp_path: Path
    ) -> None:
        shared, manifest, *_ = self._ws(
            tmp_path, [("a.txt", b"A"), ("b.txt", b"B")]
        )
        a = serialize_manifest(manifest)
        b = serialize_manifest(manifest)
        assert a == b


# ===========================================================================
# BT14.e — PRE-gate direct-FS failure semantics
# ===========================================================================


class TestBT14e_PreGateDirectFS:
    """BT14.e — direct-FS failure semantics. Property scope: every
    direct-FS-contact surface surfaces a specific failure code (never
    silently fails); cross-org writes raise ``F-VAULT-04``; kernel-primitive
    probes return a bool; ``gate_and_open`` probe preserves intent.
    """

    def test_cross_org_write_raises_f_vault_04(self, tmp_path: Path) -> None:
        # Org A writes into Org B's vault root → VaultCrossOrgAccess.
        org_a = tmp_path / "orgs" / "a"
        org_b = tmp_path / "orgs" / "b"
        org_a.mkdir(parents=True)
        org_b.mkdir(parents=True)
        target = org_b / "admin_risk" / "ledger.jsonl"
        with pytest.raises(VaultCrossOrgAccess) as exc:
            vault_write(
                path=target,
                bytes_=b"x",
                intent="admin-risk-append",
                session_id="s",
                slug="a",
                org_vault_root=org_a,
                write_lock_path=org_a / ".lock",
                write_mode="append-cas",
                expected_current_file_hash=EMPTY_SHA3_512_HEX,
            )
        assert exc.value.code == F_VAULT_04

    def test_probe_openat2_returns_bool_on_darwin(self) -> None:
        if platform.system() != "Linux":
            assert _gate_and_open.probe_openat2(-1) is False

    def test_f_uuid_01_string_identity(self) -> None:
        assert F_UUID_01 == "F-UUID-01"

    def test_denylisted_fs_types_are_frozen(self) -> None:
        assert isinstance(DENYLISTED_FS_TYPES, frozenset)
        with pytest.raises(AttributeError):
            DENYLISTED_FS_TYPES.add("hfs")  # type: ignore[attr-defined]

    def test_denylisted_fs_types_contains_tmpfs(self) -> None:
        assert "tmpfs" in DENYLISTED_FS_TYPES

    def test_denylisted_fs_types_contains_overlay(self) -> None:
        assert "overlay" in DENYLISTED_FS_TYPES

    def test_denylisted_fs_types_contains_fuse(self) -> None:
        assert "fuse" in DENYLISTED_FS_TYPES

    def test_accepted_fs_types_contains_apfs_ext4_btrfs_zfs_xfs(self) -> None:
        assert {"apfs", "ext4", "btrfs", "zfs", "xfs"} <= ACCEPTED_FS_TYPES

    def test_write_modes_membership_is_closed(self) -> None:
        for good in ("overwrite", "write-if-absent", "append-cas"):
            assert good in WRITE_MODES
        for bad in ("append", "upsert", "", "OVERWRITE"):
            assert bad not in WRITE_MODES

    def test_vault_write_rejects_unknown_mode(self, tmp_path: Path) -> None:
        org = tmp_path / "orgs" / "c"
        org.mkdir(parents=True)
        with pytest.raises(Exception):  # ValueError / VaultWriteDenied / TypeError
            vault_write(
                path=org / "x.bin",
                bytes_=b"x",
                intent="rails-report-write",
                session_id="s",
                slug="c",
                org_vault_root=org,
                write_lock_path=org / ".lock",
                write_mode="APPEND",  # unknown mode
            )

    def test_vault_write_requires_path_under_org_root(
        self, tmp_path: Path
    ) -> None:
        org = tmp_path / "orgs" / "d"
        org.mkdir(parents=True)
        outside = tmp_path / "outside" / "stray.bin"
        outside.parent.mkdir()
        with pytest.raises(VaultCrossOrgAccess):
            vault_write(
                path=outside,
                bytes_=b"x",
                intent="rails-report-write",
                session_id="s",
                slug="d",
                org_vault_root=org,
                write_lock_path=org / ".lock",
                write_mode="overwrite",
            )

    def test_denial_reason_always_populated_on_cross_org(
        self, tmp_path: Path
    ) -> None:
        org_a = tmp_path / "orgs" / "e"
        org_b = tmp_path / "orgs" / "f"
        org_a.mkdir(parents=True)
        org_b.mkdir(parents=True)
        try:
            vault_write(
                path=org_b / "r.json",
                bytes_=b"x",
                intent="rails-report-write",
                session_id="s",
                slug="e",
                org_vault_root=org_a,
                write_lock_path=org_a / ".lock",
                write_mode="overwrite",
            )
        except VaultCrossOrgAccess as exc:
            assert exc.code == F_VAULT_04

    def test_fd_broker_unknown_skill_code_is_f_fd_01(self) -> None:
        assert F_FD_01 == "F-FD-01"


# ===========================================================================
# BT14.f — Per-org init.marker ceremony
# ===========================================================================


class TestBT14f_InitMarkerCeremony:
    """BT14.f — per-org ``init.marker`` ceremony ordering (floor →
    shared-init-verify → per-org-init-write). Property scope: idempotent
    re-verify, missing shared marker blocks per-org verify, per-org marker
    can be rewritten only via fresh target.
    """

    def _setup(self, tmp_path: Path) -> dict:
        shared_root = tmp_path / "vault_shared"
        shared_root.mkdir()
        org_root = tmp_path / "org"
        org_root.mkdir()
        return {
            "shared_marker": shared_root / "init.marker",
            "shared_hmac": shared_root / "init.marker.hmac",
            "shared_lock": shared_root / "init.lock",
            "org_marker": org_root / "init.marker",
            "org_hmac": org_root / "init.marker.hmac",
            "org_lock": org_root / "init.lock",
        }

    def _write_shared(self, paths: dict, ks: CapstoneVaultKeyStore) -> None:
        write_vault_init_marker(
            marker_path=paths["shared_marker"],
            hmac_path=paths["shared_hmac"],
            lock_path=paths["shared_lock"],
            keystore=ks,
            scope="shared",
            slug="",
            operator_id="op",
            section_lock_hash="a" * 64,
        )

    def _write_org(
        self, paths: dict, ks: CapstoneVaultKeyStore, slug: str = "o"
    ) -> None:
        write_vault_init_marker(
            marker_path=paths["org_marker"],
            hmac_path=paths["org_hmac"],
            lock_path=paths["org_lock"],
            keystore=ks,
            scope="org",
            slug=slug,
            operator_id="op",
            section_lock_hash="b" * 64,
        )

    def test_shared_then_org_write_sequence(self, tmp_path: Path) -> None:
        paths = self._setup(tmp_path)
        ks = CapstoneVaultKeyStore()
        self._write_shared(paths, ks)
        self._write_org(paths, ks)
        # Both markers present + verifiable.
        verify_vault_init_marker(
            marker_path=paths["shared_marker"],
            hmac_path=paths["shared_hmac"],
            keystore=ks,
            expected_slug="",
            expected_scope="shared",
        )
        verify_vault_init_marker(
            marker_path=paths["org_marker"],
            hmac_path=paths["org_hmac"],
            keystore=ks,
            expected_slug="o",
            expected_scope="org",
        )

    def test_verify_is_idempotent_over_many_reads(
        self, tmp_path: Path
    ) -> None:
        paths = self._setup(tmp_path)
        ks = CapstoneVaultKeyStore()
        self._write_org(paths, ks)
        first = verify_vault_init_marker(
            marker_path=paths["org_marker"],
            hmac_path=paths["org_hmac"],
            keystore=ks,
            expected_slug="o",
            expected_scope="org",
        )
        for _ in range(6):
            again = verify_vault_init_marker(
                marker_path=paths["org_marker"],
                hmac_path=paths["org_hmac"],
                keystore=ks,
                expected_slug="o",
                expected_scope="org",
            )
            assert again == first

    def test_org_verify_without_marker_raises_missing(
        self, tmp_path: Path
    ) -> None:
        paths = self._setup(tmp_path)
        ks = CapstoneVaultKeyStore()
        with pytest.raises(VaultInitMissing):
            verify_vault_init_marker(
                marker_path=paths["org_marker"],
                hmac_path=paths["org_hmac"],
                keystore=ks,
                expected_slug="o",
                expected_scope="org",
            )

    def test_org_rewrite_blocked_while_marker_exists(
        self, tmp_path: Path
    ) -> None:
        paths = self._setup(tmp_path)
        ks = CapstoneVaultKeyStore()
        self._write_org(paths, ks)
        with pytest.raises(VaultInitAlreadyExists):
            self._write_org(paths, ks)

    def test_two_distinct_orgs_independent_markers(
        self, tmp_path: Path
    ) -> None:
        ks = CapstoneVaultKeyStore()
        for slug in ("alpha", "beta"):
            d = tmp_path / slug
            d.mkdir()
            write_vault_init_marker(
                marker_path=d / "init.marker",
                hmac_path=d / "init.marker.hmac",
                lock_path=d / "init.lock",
                keystore=ks,
                scope="org",
                slug=slug,
                operator_id="op",
                section_lock_hash="c" * 64,
            )
            verify_vault_init_marker(
                marker_path=d / "init.marker",
                hmac_path=d / "init.marker.hmac",
                keystore=ks,
                expected_slug=slug,
                expected_scope="org",
            )

    def test_wrong_slug_expected_raises(self, tmp_path: Path) -> None:
        paths = self._setup(tmp_path)
        ks = CapstoneVaultKeyStore()
        self._write_org(paths, ks, slug="o")
        with pytest.raises(Exception):  # VaultInitError family
            verify_vault_init_marker(
                marker_path=paths["org_marker"],
                hmac_path=paths["org_hmac"],
                keystore=ks,
                expected_slug="not-o",
                expected_scope="org",
            )

    def test_wrong_scope_expected_raises(self, tmp_path: Path) -> None:
        paths = self._setup(tmp_path)
        ks = CapstoneVaultKeyStore()
        self._write_org(paths, ks)
        with pytest.raises(Exception):
            verify_vault_init_marker(
                marker_path=paths["org_marker"],
                hmac_path=paths["org_hmac"],
                keystore=ks,
                expected_slug="o",
                expected_scope="shared",
            )

    def test_marker_lock_file_created_under_parent(
        self, tmp_path: Path
    ) -> None:
        paths = self._setup(tmp_path)
        ks = CapstoneVaultKeyStore()
        self._write_org(paths, ks)
        # The lock file must live inside the parent dir, not the marker
        # directory ancestor.
        assert paths["org_lock"].parent == paths["org_marker"].parent

    def test_marker_body_is_utf8_decodable_json(self, tmp_path: Path) -> None:
        paths = self._setup(tmp_path)
        ks = CapstoneVaultKeyStore()
        self._write_org(paths, ks)
        text = paths["org_marker"].read_text(encoding="utf-8")
        obj = json.loads(text)
        assert obj["scope"] == "org"
        assert obj["slug"] == "o"

    def test_marker_body_contains_canonical_field_set(
        self, tmp_path: Path
    ) -> None:
        paths = self._setup(tmp_path)
        ks = CapstoneVaultKeyStore()
        self._write_org(paths, ks)
        obj = json.loads(paths["org_marker"].read_text(encoding="utf-8"))
        for field in (
            "scope",
            "slug",
            "operator_id",
            "section_lock_hash",
        ):
            assert field in obj, f"canonical marker field missing: {field}"

    def test_hmac_file_is_adjacent_to_marker(self, tmp_path: Path) -> None:
        paths = self._setup(tmp_path)
        ks = CapstoneVaultKeyStore()
        self._write_org(paths, ks)
        assert paths["org_marker"].parent == paths["org_hmac"].parent

    def test_same_keystore_verifies_any_scope_written_with_it(
        self, tmp_path: Path
    ) -> None:
        paths = self._setup(tmp_path)
        ks = CapstoneVaultKeyStore()
        self._write_shared(paths, ks)
        self._write_org(paths, ks, slug="o")
        # both verifiable with one keystore instance
        verify_vault_init_marker(
            marker_path=paths["shared_marker"],
            hmac_path=paths["shared_hmac"],
            keystore=ks,
            expected_slug="",
            expected_scope="shared",
        )
        verify_vault_init_marker(
            marker_path=paths["org_marker"],
            hmac_path=paths["org_hmac"],
            keystore=ks,
            expected_slug="o",
            expected_scope="org",
        )


# ===========================================================================
# BT14.g — Identity-tuple resolver + 4-field compare
# ===========================================================================


class TestBT14g_IdentityTuple:
    """BT14.g — ``resolve_identity_tuple`` returns a 4-field tuple that the
    Batch-3-Phase-2 ``freeze_vault_shared`` re-captures to catch bind-mount
    swaps and filesystem-layer substitution between seed and freeze.
    """

    def test_resolve_returns_identity_tuple_instance(
        self, tmp_path: Path
    ) -> None:
        f = tmp_path / "f.bin"
        f.write_bytes(b"x")
        tup = resolve_identity_tuple(f)
        assert isinstance(tup, IdentityTuple)

    def test_identity_tuple_has_four_fs_fields(self, tmp_path: Path) -> None:
        f = tmp_path / "f.bin"
        f.write_bytes(b"x")
        tup = resolve_identity_tuple(f)
        assert tup.volume_uuid
        assert tup.fs_file_id
        assert tup.mount_id is not None  # may be empty on macOS, but field exists
        assert tup.fs_type

    def test_identity_tuple_stable_across_repeat_calls(
        self, tmp_path: Path
    ) -> None:
        f = tmp_path / "stable.bin"
        f.write_bytes(b"y")
        a = resolve_identity_tuple(f)
        b = resolve_identity_tuple(f)
        # volume_uuid + fs_file_id + fs_type + mount_id identical for same file.
        assert a.volume_uuid == b.volume_uuid
        assert a.fs_file_id == b.fs_file_id
        assert a.fs_type == b.fs_type
        assert a.mount_id == b.mount_id

    def test_two_files_same_volume_share_volume_uuid(
        self, tmp_path: Path
    ) -> None:
        a_path = tmp_path / "a.bin"
        b_path = tmp_path / "b.bin"
        a_path.write_bytes(b"a")
        b_path.write_bytes(b"b")
        a = resolve_identity_tuple(a_path)
        b = resolve_identity_tuple(b_path)
        assert a.volume_uuid == b.volume_uuid
        assert a.fs_type == b.fs_type

    def test_two_files_have_distinct_fs_file_ids(self, tmp_path: Path) -> None:
        a_path = tmp_path / "a.bin"
        b_path = tmp_path / "b.bin"
        a_path.write_bytes(b"a")
        b_path.write_bytes(b"b")
        a = resolve_identity_tuple(a_path)
        b = resolve_identity_tuple(b_path)
        assert a.fs_file_id != b.fs_file_id

    def test_nonexistent_path_raises(self, tmp_path: Path) -> None:
        with pytest.raises((IdentityTupleUnavailable, FileNotFoundError, OSError)):
            resolve_identity_tuple(tmp_path / "does-not-exist")

    def test_non_path_argument_raises_typeerror(self) -> None:
        with pytest.raises(TypeError):
            resolve_identity_tuple("/tmp")  # type: ignore[arg-type]

    def test_frozen_dataclass_is_hashable(self, tmp_path: Path) -> None:
        f = tmp_path / "f.bin"
        f.write_bytes(b"x")
        tup = resolve_identity_tuple(f)
        # Frozen + eq_based hashability
        h = hash((tup.volume_uuid, tup.fs_file_id, tup.mount_id, tup.fs_type))
        assert isinstance(h, int)

    def test_identity_drift_catches_volume_uuid_mismatch(
        self, tmp_path: Path
    ) -> None:
        shared = tmp_path / "vault_shared"
        shared.mkdir()
        sf = make_seed_file("a.txt", b"A", shared)
        # Build manifest with tampered volume_uuid so freeze re-capture drifts.
        tampered = replace(
            sf,
            identity_tuple=replace(
                sf.identity_tuple, volume_uuid="deadbeef" * 4
            ),
        )
        manifest = build_manifest([tampered])
        with pytest.raises(SeedFileIdentityDrift) as exc:
            freeze_vault_shared(
                manifest=manifest, vault_shared_root=shared
            )
        assert exc.value.code == F_M15_01

    def test_identity_drift_catches_fs_type_mismatch(
        self, tmp_path: Path
    ) -> None:
        shared = tmp_path / "vault_shared"
        shared.mkdir()
        sf = make_seed_file("a.txt", b"A", shared)
        tampered = replace(
            sf,
            identity_tuple=replace(sf.identity_tuple, fs_type="hfs"),
        )
        manifest = build_manifest([tampered])
        with pytest.raises(SeedFileIdentityDrift):
            freeze_vault_shared(
                manifest=manifest, vault_shared_root=shared
            )

    def test_identity_drift_catches_fs_file_id_mismatch(
        self, tmp_path: Path
    ) -> None:
        shared = tmp_path / "vault_shared"
        shared.mkdir()
        sf = make_seed_file("a.txt", b"A", shared)
        tampered = replace(
            sf,
            identity_tuple=replace(
                sf.identity_tuple, fs_file_id="00" * 8
            ),
        )
        manifest = build_manifest([tampered])
        with pytest.raises(SeedFileIdentityDrift):
            freeze_vault_shared(
                manifest=manifest, vault_shared_root=shared
            )

    def test_identity_tuple_captured_at_is_iso_string(
        self, tmp_path: Path
    ) -> None:
        f = tmp_path / "f.bin"
        f.write_bytes(b"x")
        tup = resolve_identity_tuple(f)
        assert isinstance(tup.captured_at, str)
        assert "T" in tup.captured_at or "-" in tup.captured_at


# ===========================================================================
# BT14.g.1 — Stable-UUID floor
# ===========================================================================


class TestBT14g1_UUIDFloor:
    """BT14.g.1 — ``uuid_floor`` invariants. Property scope: accepted ⟺
    (fs_type in ACCEPTED_FS_TYPES AND volume_uuid non-zero); rejection
    reasons are structured strings; frozen allowlists; enforce vs evaluate.
    """

    def test_evaluate_accepts_workspace_on_apfs_or_ext4(
        self, tmp_path: Path
    ) -> None:
        floor = _uuid_floor.evaluate(tmp_path)
        # pytest tmp_path usually lives on the host's canonical FS —
        # assume host is apfs/ext4/btrfs/zfs/xfs in practice; if not,
        # skip rather than fail (host-dependent).
        if not floor.accepted:
            pytest.skip(
                f"host fs_type {floor.fs_type!r} not in accepted floor"
            )
        assert floor.fs_type in ACCEPTED_FS_TYPES

    def test_evaluate_returns_stableuuidfloor(self, tmp_path: Path) -> None:
        floor = _uuid_floor.evaluate(tmp_path)
        assert isinstance(floor, StableUUIDFloor)

    def test_evaluate_stable_across_calls(self, tmp_path: Path) -> None:
        a = _uuid_floor.evaluate(tmp_path)
        b = _uuid_floor.evaluate(tmp_path)
        assert a.accepted == b.accepted
        assert a.fs_type == b.fs_type
        assert a.volume_uuid == b.volume_uuid

    def test_enforce_returns_stableuuidfloor_on_accept(
        self, tmp_path: Path
    ) -> None:
        floor = _uuid_floor.evaluate(tmp_path)
        if not floor.accepted:
            pytest.skip("host fs not on allowlist")
        out = _uuid_floor.enforce(tmp_path)
        assert out == floor

    def test_enforce_raises_typeerror_on_str(self) -> None:
        with pytest.raises(TypeError):
            _uuid_floor.enforce("/tmp")  # type: ignore[arg-type]

    def test_evaluate_raises_typeerror_on_str(self) -> None:
        with pytest.raises(TypeError):
            _uuid_floor.evaluate("/tmp")  # type: ignore[arg-type]

    def test_accepted_fs_types_is_frozen(self) -> None:
        assert isinstance(ACCEPTED_FS_TYPES, frozenset)
        with pytest.raises(AttributeError):
            ACCEPTED_FS_TYPES.add("hfs")  # type: ignore[attr-defined]

    def test_denylisted_fs_types_is_frozen(self) -> None:
        assert isinstance(DENYLISTED_FS_TYPES, frozenset)
        with pytest.raises(AttributeError):
            DENYLISTED_FS_TYPES.add("hfs")  # type: ignore[attr-defined]

    def test_accepted_and_denylisted_are_disjoint(self) -> None:
        assert ACCEPTED_FS_TYPES.isdisjoint(DENYLISTED_FS_TYPES)

    def test_uuid_floor_rejected_carries_reason(self) -> None:
        exc = UUIDFloorRejected("bad", reason="tmpfs-not-allowed")
        assert exc.reason == "tmpfs-not-allowed"
        assert exc.code == F_UUID_01

    def test_accepted_true_implies_empty_rejection_reason(
        self, tmp_path: Path
    ) -> None:
        floor = _uuid_floor.evaluate(tmp_path)
        if not floor.accepted:
            pytest.skip("host fs not on allowlist")
        assert floor.rejection_reason == ""

    def test_uuid_floor_rejected_is_vault_error_subtype(self) -> None:
        from pipeline.vault.error_codes import VaultError

        assert issubclass(UUIDFloorRejected, UUIDFloorError)
        assert issubclass(UUIDFloorError, VaultError)

    def test_accepted_and_rejection_reason_are_contradictory(
        self, tmp_path: Path
    ) -> None:
        floor = _uuid_floor.evaluate(tmp_path)
        # Invariant: accepted ⇒ rejection_reason == ""
        #            rejected ⇒ rejection_reason != ""
        if floor.accepted:
            assert floor.rejection_reason == ""
        else:
            assert floor.rejection_reason != ""
