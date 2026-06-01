"""Unit tests for pipeline.vault.m15_ledger (§4.6 + §9 boot steps 6 + 9).

Round T — M15 signed-commit discipline for ``vault_shared/``.

Scope:
* On-disk readers for ``seed_manifest.json`` and ``seed_manifest.sig``.
* Canonical signature-payload serializer (so caller-side signers and our
  verifier agree byte-for-byte).
* ``verify_seed_manifest`` — §9 step 6 entry point. Loads the manifest +
  signature, runs the operator-signature primitive (injected
  :type:`SignatureVerifier`), enforces the ``m15_ledger_head`` against the
  caller-provided current ledger head, then delegates to
  :func:`mirror_verify.freeze_vault_shared` for the Merkle pin.
* ``cedar_policy_loader_load_all`` — §9 step 9. Reads every ``cedar/*.cedar``
  text from a ``VaultSharedFrozenRoot``-pinned vault and re-checks bytes
  against the pinned content hash. Defence-in-depth post-freeze read.

Out of scope (deferred):
* M15.3 ``commit_cedar`` operator workflow (HIGH-severity admin_risk re-type).
  Boot reads/loads only; commits live in a later operator-tooling round.
* Privileged broker bootstrap mode used by §9 step 6 to open seed files —
  Round T uses the Path-based reader; the broker hookup belongs to Round R
  vault_boot capstone.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Callable, Optional

import pytest

from pipeline.vault.error_codes import (
    F_CEDAR_01,
    F_M15_01,
    F_M15_02,
    F_M15_03,
    CedarError,
    M15Error,
)
from pipeline.vault.identity_tuple import resolve_identity_tuple
from pipeline.vault.m15_ledger import (
    CedarPolicyLoadFailed,
    SeedManifestLedgerHeadDrift,
    SeedManifestSignatureInvalid,
    SignatureVerifier,
    cedar_policy_loader_load_all,
    load_seed_manifest,
    load_signature,
    serialize_signature_payload,
    verify_seed_manifest,
)
from pipeline.vault.mirror_verify import (
    SeedFileContentDrift,
    SeedFileExtraOnDisk,
    SeedManifestHeadDrift,
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


def _canonical(obj: object) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


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


def _build_manifest(
    seeds: list[SeedFile],
    *,
    head_hash: Optional[str] = None,
    signature: str = "valid-sig",
    m15_ledger_head: str = "ledger-head-1",
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


def _serialize_manifest_to_json(manifest: VaultSharedSeedManifest) -> bytes:
    """Mirror what an operator-side committer would write to disk."""
    payload = {
        "head_hash": manifest.head_hash,
        "files": [asdict(sf) for sf in manifest.files],
        "committed_at": manifest.committed_at,
        "committed_by": manifest.committed_by,
        "m15_ledger_head": manifest.m15_ledger_head,
        "signature": manifest.signature,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _write_manifest_files(
    vault_shared: Path, manifest: VaultSharedSeedManifest
) -> tuple[Path, Path]:
    """Write seed_manifest.json + seed_manifest.sig under the workspace
    parent of ``vault_shared`` (NOT under ``vault_shared`` itself, so the
    seed-partition walk doesn't see them as extras)."""
    holder = vault_shared.parent
    manifest_path = holder / "seed_manifest.json"
    sig_path = holder / "seed_manifest.sig"
    manifest_path.write_bytes(_serialize_manifest_to_json(manifest))
    sig_path.write_text(manifest.signature + "\n", encoding="utf-8")
    return manifest_path, sig_path


def _make_verifier(
    expected_payload: bytes, valid_signature: str
) -> SignatureVerifier:
    def verify(payload: bytes, signature: str) -> bool:
        return payload == expected_payload and signature == valid_signature

    return verify


def _always_true(_payload: bytes, _signature: str) -> bool:
    return True


def _always_false(_payload: bytes, _signature: str) -> bool:
    return False


def _raising(_payload: bytes, _signature: str) -> bool:
    raise RuntimeError("verifier-blew-up")


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
        _make_seed_file("cedar/org_isolation.cedar", b"permit(principal, action, resource);\n", vault_shared),
        _make_seed_file("cedar/write_gate.cedar", b"permit;\nforbid x;\n", vault_shared),
        _make_seed_file("sandbox_profiles/scout.sbpl", b"(version 1)\n", vault_shared),
        _make_seed_file(
            "process_wrappers/fallback-shell/seat-launch.sh",
            b"#!/bin/sh\nexec $@\n",
            vault_shared,
        ),
    ]
    return vault_shared, seeds


# ---------------------------------------------------------------------------
# load_seed_manifest
# ---------------------------------------------------------------------------


class TestLoadSeedManifest:
    def test_round_trips_to_dataclass(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        manifest_path, _ = _write_manifest_files(shared, manifest)
        loaded = load_seed_manifest(manifest_path)
        assert isinstance(loaded, VaultSharedSeedManifest)
        assert loaded.head_hash == manifest.head_hash
        assert loaded.m15_ledger_head == manifest.m15_ledger_head
        assert loaded.signature == manifest.signature
        assert loaded.files == manifest.files

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises((OSError, FileNotFoundError)):
            load_seed_manifest(tmp_path / "nope.json")

    def test_malformed_json_raises(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.json"
        bad.write_text("not-json", encoding="utf-8")
        with pytest.raises(json.JSONDecodeError):
            load_seed_manifest(bad)

    def test_missing_required_field_raises(self, tmp_path: Path) -> None:
        bad = tmp_path / "missing.json"
        bad.write_text(json.dumps({"head_hash": "x"}), encoding="utf-8")
        with pytest.raises((KeyError, TypeError)):
            load_seed_manifest(bad)

    def test_rejects_non_path(self) -> None:
        with pytest.raises(TypeError):
            load_seed_manifest("not-a-path")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# load_signature
# ---------------------------------------------------------------------------


class TestLoadSignature:
    def test_reads_text_and_strips_whitespace(self, tmp_path: Path) -> None:
        p = tmp_path / "x.sig"
        p.write_text("  abcd1234  \n", encoding="utf-8")
        assert load_signature(p) == "abcd1234"

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises((OSError, FileNotFoundError)):
            load_signature(tmp_path / "nope.sig")

    def test_rejects_non_path(self) -> None:
        with pytest.raises(TypeError):
            load_signature("not-a-path")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# serialize_signature_payload
# ---------------------------------------------------------------------------


class TestSerializeSignaturePayload:
    def test_canonical_json_form(self) -> None:
        out = serialize_signature_payload(
            head_hash="aa" * 64, m15_ledger_head="bb" * 32
        )
        assert out == _canonical(
            {"head_hash": "aa" * 64, "m15_ledger_head": "bb" * 32}
        )

    def test_deterministic(self) -> None:
        a = serialize_signature_payload(head_hash="x", m15_ledger_head="y")
        b = serialize_signature_payload(head_hash="x", m15_ledger_head="y")
        assert a == b

    def test_rejects_non_str_head(self) -> None:
        with pytest.raises(TypeError):
            serialize_signature_payload(
                head_hash=b"x", m15_ledger_head="y"  # type: ignore[arg-type]
            )

    def test_rejects_non_str_ledger_head(self) -> None:
        with pytest.raises(TypeError):
            serialize_signature_payload(
                head_hash="x", m15_ledger_head=42  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# verify_seed_manifest
# ---------------------------------------------------------------------------


class TestVerifySeedManifest:
    def test_happy_path_returns_frozen_root(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        manifest_path, sig_path = _write_manifest_files(shared, manifest)
        expected_payload = serialize_signature_payload(
            head_hash=manifest.head_hash,
            m15_ledger_head=manifest.m15_ledger_head,
        )
        verifier = _make_verifier(expected_payload, manifest.signature)
        frozen = verify_seed_manifest(
            manifest_path=manifest_path,
            signature_path=sig_path,
            vault_shared_root=shared,
            current_ledger_head=manifest.m15_ledger_head,
            verify_signature=verifier,
        )
        assert isinstance(frozen, VaultSharedFrozenRoot)
        assert frozen.root_hex == manifest.head_hash
        assert set(frozen.seed_paths) == {sf.relative_path for sf in seeds}

    def test_signature_invalid_raises_f_m15_02(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        manifest_path, sig_path = _write_manifest_files(shared, manifest)
        with pytest.raises(SeedManifestSignatureInvalid) as exc:
            verify_seed_manifest(
                manifest_path=manifest_path,
                signature_path=sig_path,
                vault_shared_root=shared,
                current_ledger_head=manifest.m15_ledger_head,
                verify_signature=_always_false,
            )
        assert exc.value.code == F_M15_02

    def test_signature_verifier_raising_is_f_m15_02(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        manifest_path, sig_path = _write_manifest_files(shared, manifest)
        with pytest.raises(SeedManifestSignatureInvalid) as exc:
            verify_seed_manifest(
                manifest_path=manifest_path,
                signature_path=sig_path,
                vault_shared_root=shared,
                current_ledger_head=manifest.m15_ledger_head,
                verify_signature=_raising,
            )
        assert exc.value.code == F_M15_02

    def test_ledger_head_drift_raises_f_m15_03(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds, m15_ledger_head="ledger-head-OLD")
        manifest_path, sig_path = _write_manifest_files(shared, manifest)
        with pytest.raises(SeedManifestLedgerHeadDrift) as exc:
            verify_seed_manifest(
                manifest_path=manifest_path,
                signature_path=sig_path,
                vault_shared_root=shared,
                current_ledger_head="ledger-head-NEW",
                verify_signature=_always_true,
            )
        assert exc.value.code == F_M15_03

    def test_ledger_head_check_runs_before_freeze(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        # Tamper a seed file so freeze would fail; confirm the ledger-drift
        # raise wins (head check is gate 3, freeze is gate 4 per §4.6 order).
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds, m15_ledger_head="ledger-head-OLD")
        manifest_path, sig_path = _write_manifest_files(shared, manifest)
        (shared / seeds[0].relative_path).write_bytes(b"tampered")
        with pytest.raises(SeedManifestLedgerHeadDrift):
            verify_seed_manifest(
                manifest_path=manifest_path,
                signature_path=sig_path,
                vault_shared_root=shared,
                current_ledger_head="ledger-head-NEW",
                verify_signature=_always_true,
            )

    def test_signature_check_runs_before_ledger_check(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds, m15_ledger_head="ledger-head-OLD")
        manifest_path, sig_path = _write_manifest_files(shared, manifest)
        with pytest.raises(SeedManifestSignatureInvalid):
            verify_seed_manifest(
                manifest_path=manifest_path,
                signature_path=sig_path,
                vault_shared_root=shared,
                current_ledger_head="ledger-head-NEW",
                verify_signature=_always_false,
            )

    def test_delegates_content_drift_to_mirror_verify(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        manifest_path, sig_path = _write_manifest_files(shared, manifest)
        # Tamper after committing the manifest.
        (shared / seeds[0].relative_path).write_bytes(b"tampered")
        with pytest.raises(SeedFileContentDrift) as exc:
            verify_seed_manifest(
                manifest_path=manifest_path,
                signature_path=sig_path,
                vault_shared_root=shared,
                current_ledger_head=manifest.m15_ledger_head,
                verify_signature=_always_true,
            )
        assert exc.value.code == F_M15_01

    def test_delegates_extra_unlisted_to_mirror_verify(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        manifest_path, sig_path = _write_manifest_files(shared, manifest)
        # Plant an unlisted file in the seed partition.
        (shared / "cedar" / "extra.cedar").write_bytes(b"surprise;\n")
        with pytest.raises(SeedFileExtraOnDisk):
            verify_seed_manifest(
                manifest_path=manifest_path,
                signature_path=sig_path,
                vault_shared_root=shared,
                current_ledger_head=manifest.m15_ledger_head,
                verify_signature=_always_true,
            )

    def test_missing_manifest_file_raises(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, _ = seeded_shared
        with pytest.raises((OSError, FileNotFoundError)):
            verify_seed_manifest(
                manifest_path=shared.parent / "no-manifest.json",
                signature_path=shared.parent / "no-sig.sig",
                vault_shared_root=shared,
                current_ledger_head="x",
                verify_signature=_always_true,
            )

    def test_missing_signature_file_raises(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        manifest_path, sig_path = _write_manifest_files(shared, manifest)
        sig_path.unlink()
        with pytest.raises((OSError, FileNotFoundError)):
            verify_seed_manifest(
                manifest_path=manifest_path,
                signature_path=sig_path,
                vault_shared_root=shared,
                current_ledger_head=manifest.m15_ledger_head,
                verify_signature=_always_true,
            )

    def test_rejects_non_path_manifest(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, _ = seeded_shared
        with pytest.raises(TypeError):
            verify_seed_manifest(
                manifest_path="x",  # type: ignore[arg-type]
                signature_path=shared / "y",
                vault_shared_root=shared,
                current_ledger_head="x",
                verify_signature=_always_true,
            )

    def test_rejects_non_callable_verifier(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        manifest = _build_manifest(seeds)
        manifest_path, sig_path = _write_manifest_files(shared, manifest)
        with pytest.raises(TypeError):
            verify_seed_manifest(
                manifest_path=manifest_path,
                signature_path=sig_path,
                vault_shared_root=shared,
                current_ledger_head=manifest.m15_ledger_head,
                verify_signature="not-callable",  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# cedar_policy_loader_load_all
# ---------------------------------------------------------------------------


class TestCedarPolicyLoader:
    def _freeze(
        self, shared: Path, seeds: list[SeedFile]
    ) -> VaultSharedFrozenRoot:
        return freeze_vault_shared(
            manifest=_build_manifest(seeds), vault_shared_root=shared
        )

    def test_returns_dict_keyed_by_relative_path(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        frozen = self._freeze(shared, seeds)
        policies = cedar_policy_loader_load_all(
            frozen_root=frozen, vault_shared_root=shared
        )
        assert "cedar/org_isolation.cedar" in policies
        assert "cedar/write_gate.cedar" in policies
        assert policies["cedar/org_isolation.cedar"].startswith("permit(")

    def test_excludes_non_cedar_seed_paths(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        frozen = self._freeze(shared, seeds)
        policies = cedar_policy_loader_load_all(
            frozen_root=frozen, vault_shared_root=shared
        )
        assert "sandbox_profiles/scout.sbpl" not in policies
        assert "process_wrappers/fallback-shell/seat-launch.sh" not in policies

    def test_only_top_level_cedar_dot_cedar_files(
        self, vault_shared: Path
    ) -> None:
        # Top-level cedar/*.cedar should load; nested cedar/sub/*.cedar should
        # be carried in the frozen root but skipped here (Section 4 routes
        # nested policy categories explicitly).
        seeds = [
            _make_seed_file("cedar/top.cedar", b"permit;\n", vault_shared),
            _make_seed_file(
                "cedar/sub/nested.cedar", b"forbid;\n", vault_shared
            ),
        ]
        frozen = freeze_vault_shared(
            manifest=_build_manifest(seeds), vault_shared_root=vault_shared
        )
        policies = cedar_policy_loader_load_all(
            frozen_root=frozen, vault_shared_root=vault_shared
        )
        assert policies == {"cedar/top.cedar": "permit;\n"}

    def test_post_freeze_tamper_raises_f_cedar_01(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        frozen = self._freeze(shared, seeds)
        # Post-freeze tamper of a Cedar file. atomic_freeze isn't applied
        # here so the bytes are mutable; defence-in-depth re-hash catches it.
        (shared / "cedar/write_gate.cedar").write_bytes(b"forbid all;\n")
        with pytest.raises(CedarPolicyLoadFailed) as exc:
            cedar_policy_loader_load_all(
                frozen_root=frozen, vault_shared_root=shared
            )
        assert exc.value.code == F_CEDAR_01

    def test_missing_file_raises_f_cedar_01(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        frozen = self._freeze(shared, seeds)
        (shared / "cedar/write_gate.cedar").unlink()
        with pytest.raises(CedarPolicyLoadFailed) as exc:
            cedar_policy_loader_load_all(
                frozen_root=frozen, vault_shared_root=shared
            )
        assert exc.value.code == F_CEDAR_01

    def test_no_cedar_files_returns_empty_dict(
        self, vault_shared: Path
    ) -> None:
        seeds = [
            _make_seed_file(
                "process_wrappers/fallback-shell/seat-launch.sh",
                b"#!/bin/sh\n",
                vault_shared,
            ),
        ]
        frozen = freeze_vault_shared(
            manifest=_build_manifest(seeds), vault_shared_root=vault_shared
        )
        assert cedar_policy_loader_load_all(
            frozen_root=frozen, vault_shared_root=vault_shared
        ) == {}

    def test_rejects_non_frozen_root(self, vault_shared: Path) -> None:
        with pytest.raises(TypeError):
            cedar_policy_loader_load_all(
                frozen_root="not-a-frozen-root",  # type: ignore[arg-type]
                vault_shared_root=vault_shared,
            )

    def test_rejects_non_path_root(
        self, seeded_shared: tuple[Path, list[SeedFile]]
    ) -> None:
        shared, seeds = seeded_shared
        frozen = self._freeze(shared, seeds)
        with pytest.raises(TypeError):
            cedar_policy_loader_load_all(
                frozen_root=frozen,
                vault_shared_root="x",  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# Exception taxonomy
# ---------------------------------------------------------------------------


class TestExceptionTaxonomy:
    def test_signature_invalid_inherits_m15_error(self) -> None:
        assert issubclass(SeedManifestSignatureInvalid, M15Error)
        assert SeedManifestSignatureInvalid.code == F_M15_02

    def test_ledger_head_drift_inherits_m15_error(self) -> None:
        assert issubclass(SeedManifestLedgerHeadDrift, M15Error)
        assert SeedManifestLedgerHeadDrift.code == F_M15_03

    def test_cedar_load_failed_inherits_cedar_error(self) -> None:
        assert issubclass(CedarPolicyLoadFailed, CedarError)
        assert CedarPolicyLoadFailed.code == F_CEDAR_01


# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS pin (F-2..F-5: vault_batch_1_redispatch_2026-04-22)
# ---------------------------------------------------------------------------


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        import importlib
        _mod = importlib.import_module('pipeline.vault.m15_ledger')
        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
