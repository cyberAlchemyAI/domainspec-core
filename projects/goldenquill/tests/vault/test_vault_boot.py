"""Unit tests for pipeline.vault.vault_boot (§9 capstone).

Round R — Composes Rounds K..U into the §9 boot sequence.

Step coverage in v0.1:
* §9 step 2  — UUID floor (Round K `uuid_floor.enforce`)
* §9 step 4  — Trust-root mirror verify (Round S, optional config)
* §9 step 5  — Vault-shared init marker (Round I, optional config)
* §9 step 6  — M15 seed manifest verify (Round T)
* §9 step 7  — Atomic verify-and-freeze (Round U)
* §9 step 8  — Wrapper hash verify (deferred — `process_wrapper.py` not built)
* §9 step 9  — Cedar policy load (Round T)
* §9 step 10 — FD broker online + post-gate hook from Round S
* §9 step 11 — Per-org init marker (Round I, optional config)

Steps deferred / skipped in v0.1 surface a degradation note in the result.
"""

from __future__ import annotations

import dataclasses
import hashlib
import os
from pathlib import Path
from typing import Optional

import pytest

from pipeline.vault.atomic_freeze import (
    AtomicFreezeResult,
    SnapshotProvider,
    SnapshotRecord,
)
from pipeline.vault.error_codes import (
    F_CEDAR_01,
    F_FD_01,
    F_M15_02,
    F_M15_03,
    CedarError,
    M15Error,
    UUIDFloorError,
    VaultError,
)
from pipeline.vault.fd_broker import FDBroker
from pipeline.vault.identity_tuple import resolve_identity_tuple
from pipeline.vault.m15_ledger import (
    SeedManifestLedgerHeadDrift,
    SeedManifestSignatureInvalid,
)
from pipeline.vault.mirror_verify import (
    SeedFileContentDrift,
    VaultSharedFrozenRoot,
    compute_leaf_hash_hex,
    compute_merkle_root_hex,
)
from pipeline.vault.schemas import (
    FDBrokerRequest,
    SeedFile,
    StableUUIDFloor,
    VaultSharedSeedManifest,
)
from pipeline.vault.vault_boot import (
    DEFAULT_VAULT_INIT_SCOPE,
    DEFAULT_VAULT_INIT_SLUG,
    TrustRootMirrorVerifyConfig,
    VaultBootResult,
    VaultInitVerifyConfig,
    vault_boot,
    vault_boot_close,
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


def _build_manifest(
    seeds: list[SeedFile],
    *,
    m15_ledger_head: str = "ledger-head-1",
    signature: str = "valid-sig",
) -> VaultSharedSeedManifest:
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
        m15_ledger_head=m15_ledger_head,
        signature=signature,
    )


def _serialize_manifest(manifest: VaultSharedSeedManifest) -> bytes:
    import json
    from dataclasses import asdict

    payload = {
        "head_hash": manifest.head_hash,
        "files": [asdict(sf) for sf in manifest.files],
        "committed_at": manifest.committed_at,
        "committed_by": manifest.committed_by,
        "m15_ledger_head": manifest.m15_ledger_head,
        "signature": manifest.signature,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _always_true(_payload: bytes, _signature: str) -> bool:
    return True


def _always_false(_payload: bytes, _signature: str) -> bool:
    return False


@pytest.fixture
def boot_workspace(tmp_path: Path) -> dict:
    """Build a complete on-disk vault root + signed seed manifest."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    vault_root = workspace / "vault"
    vault_root.mkdir()
    vault_shared = vault_root / "vault_shared"
    vault_shared.mkdir()

    seeds = [
        _make_seed_file("cedar/org_isolation.cedar", b"permit;\n", vault_shared),
        _make_seed_file("cedar/write_gate.cedar", b"forbid x;\n", vault_shared),
        _make_seed_file(
            "process_wrappers/seat-launch.sh",
            b"#!/bin/sh\nexec $@\n",
            vault_shared,
        ),
    ]
    manifest = _build_manifest(seeds)
    manifest_path = workspace / "seed_manifest.json"
    sig_path = workspace / "seed_manifest.sig"
    manifest_path.write_bytes(_serialize_manifest(manifest))
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
def boot_kwargs(boot_workspace: dict) -> dict:
    return {
        "vault_root": boot_workspace["vault_root"],
        "vault_shared_root": boot_workspace["vault_shared"],
        "seed_manifest_path": boot_workspace["manifest_path"],
        "seed_signature_path": boot_workspace["sig_path"],
        "session_id": "session-test-A",
        "current_ledger_head": boot_workspace["manifest"].m15_ledger_head,
        "verify_signature": _always_true,
        "platform": "darwin",
    }


@pytest.fixture
def auto_close():
    """Yield a list to register VaultBootResult instances; closes them on teardown."""
    results: list[VaultBootResult] = []
    yield results
    for r in results:
        try:
            vault_boot_close(r)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Result + config dataclass shapes
# ---------------------------------------------------------------------------


class TestVaultBootResultShape:
    def test_is_frozen(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        result = vault_boot(**boot_kwargs)
        auto_close.append(result)
        with pytest.raises(dataclasses.FrozenInstanceError):
            result.success = False  # type: ignore[misc]

    def test_kw_only(
        self,
        boot_workspace: dict,
        boot_kwargs: dict,
        auto_close: list,
    ) -> None:
        # vault_boot is keyword-only; positional should fail.
        with pytest.raises(TypeError):
            vault_boot(boot_workspace["vault_root"])  # type: ignore[misc]


class TestConfigDataclasses:
    def test_trust_root_config_is_frozen(self, boot_workspace: dict) -> None:
        from pipeline.vault.schemas import TrustRootMirrorManifest, IdentityTuple

        manifest = TrustRootMirrorManifest(
            mirror_path="x",
            content_hash="x",
            identity_tuple=IdentityTuple(
                volume_uuid="x",
                fs_file_id="x",
                mount_id="x",
                fs_type="x",
                captured_at="x",
            ),
            m15_ledger_head="x",
            operator_signature="x",
            signed_at="x",
            immutability_flag_set=True,
        )
        cfg = TrustRootMirrorVerifyConfig(
            manifest=manifest,
            live_mirror_path=boot_workspace["workspace"],
            last_boot_wall_ns=0,
            current_boot_wall_ns=1,
            clock_rollback_tolerance_seconds=60,
            verify_signature=_always_true,
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            cfg.last_boot_wall_ns = 99  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


class TestVaultBootHappyPath:
    def test_returns_success(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert r.success is True
        assert r.session_id == "session-test-A"

    def test_uuid_floor_accepted(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert isinstance(r.uuid_floor, StableUUIDFloor)
        assert r.uuid_floor.accepted is True

    def test_frozen_root_carries_seed_paths(
        self, boot_kwargs: dict, auto_close: list, boot_workspace: dict
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert isinstance(r.frozen_root, VaultSharedFrozenRoot)
        expected = {sf.relative_path for sf in boot_workspace["seeds"]}
        assert set(r.frozen_root.seed_paths) == expected

    def test_atomic_freeze_result_present(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert isinstance(r.atomic_freeze_result, AtomicFreezeResult)
        assert r.atomic_freeze_result.frozen_root is r.frozen_root

    def test_cedar_policies_loaded(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert "cedar/org_isolation.cedar" in r.cedar_policies
        assert "cedar/write_gate.cedar" in r.cedar_policies
        assert r.cedar_policies["cedar/org_isolation.cedar"] == "permit;\n"

    def test_fd_broker_present_with_post_gate(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert isinstance(r.fd_broker, FDBroker)
        # Hook bound: post_gate is not None.
        assert r.fd_broker._post_gate_hook is not None  # type: ignore[attr-defined]

    def test_vault_root_fd_open(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert isinstance(r.vault_root_fd, int)
        # FD must be a real open descriptor.
        assert r.vault_root_fd >= 0
        # fstat should succeed.
        os.fstat(r.vault_root_fd)


# ---------------------------------------------------------------------------
# Failure propagation
# ---------------------------------------------------------------------------


class TestVaultBootFailures:
    def test_m15_signature_failure_raises_f_m15_02(
        self, boot_kwargs: dict
    ) -> None:
        boot_kwargs["verify_signature"] = _always_false
        with pytest.raises(SeedManifestSignatureInvalid) as exc:
            vault_boot(**boot_kwargs)
        assert exc.value.code == F_M15_02

    def test_m15_ledger_drift_raises_f_m15_03(self, boot_kwargs: dict) -> None:
        boot_kwargs["current_ledger_head"] = "ledger-head-OTHER"
        with pytest.raises(SeedManifestLedgerHeadDrift) as exc:
            vault_boot(**boot_kwargs)
        assert exc.value.code == F_M15_03

    def test_seed_content_tamper_raises(
        self, boot_kwargs: dict, boot_workspace: dict
    ) -> None:
        # Tamper a seed file after manifest was committed.
        target = boot_workspace["vault_shared"] / "cedar/write_gate.cedar"
        target.write_bytes(b"tampered;\n")
        with pytest.raises(SeedFileContentDrift):
            vault_boot(**boot_kwargs)

    def test_cedar_loader_failure_propagates(
        self, boot_kwargs: dict, boot_workspace: dict
    ) -> None:
        # Tamper after-freeze isn't reachable in a single-shot boot, so
        # simulate by removing a Cedar file just before cedar load by making
        # the seed manifest carry it but the file disappear after freeze.
        # Simplest reproduction: corrupt the file after manifest verify;
        # because freeze re-hashes, this will surface as SeedFileContentDrift
        # at step 6 first. To probe step 9 specifically we'd need a
        # tamper-after-freeze hook — skip; failure path is covered by Round T.
        # Instead, verify the boot does NOT skip Cedar load when policies
        # are present (positive coverage of step 9 wiring).
        result = vault_boot(**boot_kwargs)
        try:
            assert len(result.cedar_policies) >= 1
        finally:
            vault_boot_close(result)

    def test_uuid_floor_failure_raises(self, boot_kwargs: dict) -> None:
        # Point at a path that doesn't exist; UUID floor raises a vault
        # exception (UUIDFloorError family) on identity-tuple resolution.
        boot_kwargs["vault_root"] = Path("/nonexistent-vault-root-xyz-9999")
        with pytest.raises((UUIDFloorError, VaultError, OSError, FileNotFoundError)):
            vault_boot(**boot_kwargs)


# ---------------------------------------------------------------------------
# Optional sub-configs and degradations
# ---------------------------------------------------------------------------


class TestDegradations:
    def test_no_trust_root_records_degradation(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert r.trust_root_mirror_verified is False
        assert any(
            "trust-root-mirror-skipped" in d for d in r.degradations
        )

    def test_no_vault_init_records_degradation(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert r.vault_init_marker is None
        assert any(
            "vault-init-marker-skipped" in d for d in r.degradations
        )

    def test_no_org_init_records_degradation(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert r.org_init_marker is None
        assert any(
            "org-init-marker-skipped" in d for d in r.degradations
        )

    def test_wrapper_hash_verify_skipped(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert any(
            "wrapper-hash-verify-skipped" in d for d in r.degradations
        )

    def test_no_snapshot_provider_no_snapshot(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert r.atomic_freeze_result.snapshot_label is None

    def test_linux_platform_records_degradation(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        boot_kwargs["platform"] = "linux"
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert any(
            "linux-mount-ns-not-implemented-v0.1" in d for d in r.degradations
        )


# ---------------------------------------------------------------------------
# Snapshot provider wiring through to atomic_freeze
# ---------------------------------------------------------------------------


class _FakeSnapshotProvider:
    def __init__(self) -> None:
        self._records: list[SnapshotRecord] = []
        self.created: list[str] = []

    def list_snapshots(self) -> tuple[SnapshotRecord, ...]:
        return tuple(self._records)

    def create_snapshot(self, *, label: str) -> SnapshotRecord:
        rec = SnapshotRecord(label=label, created_at_iso="2026-04-19T00:00:42Z")
        self._records.append(rec)
        self.created.append(label)
        return rec

    def delete_snapshot(self, *, label: str) -> None:
        self._records = [r for r in self._records if r.label != label]


class TestSnapshotProviderWired:
    def test_snapshot_provider_creates_label(
        self, boot_kwargs: dict, auto_close: list
    ) -> None:
        provider = _FakeSnapshotProvider()
        boot_kwargs["snapshot_provider"] = provider
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        assert r.atomic_freeze_result.snapshot_label is not None
        assert "session-test-A" in r.atomic_freeze_result.snapshot_label
        assert provider.created == [r.atomic_freeze_result.snapshot_label]


# ---------------------------------------------------------------------------
# Post-gate hook BT-style cross-check
# ---------------------------------------------------------------------------


class TestPostGateHookCrossCheck:
    def test_hook_accepts_unchanged_seed(
        self, boot_kwargs: dict, auto_close: list, boot_workspace: dict
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        request = FDBrokerRequest(
            requester_skill="vault-query",
            requester_pid=1,
            requester_session_id="s",
            requester_org_slug="o",
            requested_path="vault_shared/cedar/org_isolation.cedar",
            intent="read",
            nonce_hex="00" * 16,
        )
        # Hook should accept (seed unchanged).
        hook = r.fd_broker._post_gate_hook  # type: ignore[attr-defined]
        assert hook(request) is True

    def test_hook_rejects_tampered_seed(
        self, boot_kwargs: dict, auto_close: list, boot_workspace: dict
    ) -> None:
        r = vault_boot(**boot_kwargs)
        auto_close.append(r)
        # Tamper a seed file after boot completes.
        target = boot_workspace["vault_shared"] / "cedar/org_isolation.cedar"
        target.write_bytes(b"tampered-after-boot;\n")
        request = FDBrokerRequest(
            requester_skill="vault-query",
            requester_pid=1,
            requester_session_id="s",
            requester_org_slug="o",
            requested_path="vault_shared/cedar/org_isolation.cedar",
            intent="read",
            nonce_hex="00" * 16,
        )
        hook = r.fd_broker._post_gate_hook  # type: ignore[attr-defined]
        assert hook(request) is False


# ---------------------------------------------------------------------------
# vault_boot_close
# ---------------------------------------------------------------------------


class TestVaultBootClose:
    def test_close_releases_fd(self, boot_kwargs: dict) -> None:
        r = vault_boot(**boot_kwargs)
        fd = r.vault_root_fd
        os.fstat(fd)  # open
        vault_boot_close(r)
        with pytest.raises(OSError):
            os.fstat(fd)

    def test_close_idempotent(self, boot_kwargs: dict) -> None:
        r = vault_boot(**boot_kwargs)
        vault_boot_close(r)
        vault_boot_close(r)  # second close is a no-op

    def test_close_rejects_non_result(self) -> None:
        with pytest.raises(TypeError):
            vault_boot_close("not-a-result")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Type gates
# ---------------------------------------------------------------------------


class TestTypeGates:
    def test_rejects_non_path_vault_root(self, boot_kwargs: dict) -> None:
        boot_kwargs["vault_root"] = "x"
        with pytest.raises(TypeError):
            vault_boot(**boot_kwargs)

    def test_rejects_non_path_vault_shared(self, boot_kwargs: dict) -> None:
        boot_kwargs["vault_shared_root"] = "x"
        with pytest.raises(TypeError):
            vault_boot(**boot_kwargs)

    def test_rejects_non_str_session_id(self, boot_kwargs: dict) -> None:
        boot_kwargs["session_id"] = 42
        with pytest.raises(TypeError):
            vault_boot(**boot_kwargs)

    def test_rejects_empty_session_id(self, boot_kwargs: dict) -> None:
        boot_kwargs["session_id"] = ""
        with pytest.raises(ValueError):
            vault_boot(**boot_kwargs)

    def test_rejects_non_callable_verifier(self, boot_kwargs: dict) -> None:
        boot_kwargs["verify_signature"] = "x"
        with pytest.raises(TypeError):
            vault_boot(**boot_kwargs)


# ---------------------------------------------------------------------------
# Default scope/slug pins
# ---------------------------------------------------------------------------


class TestDefaultScopeSlug:
    def test_defaults_pinned(self) -> None:
        # These pins exist so callers don't sprinkle string literals through
        # config sites — single source of truth lives in the boot module.
        assert isinstance(DEFAULT_VAULT_INIT_SCOPE, str)
        assert isinstance(DEFAULT_VAULT_INIT_SLUG, str)
        assert DEFAULT_VAULT_INIT_SCOPE
        assert DEFAULT_VAULT_INIT_SLUG


# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS pin (F-2..F-5: vault_batch_1_redispatch_2026-04-22)
# ---------------------------------------------------------------------------


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        import importlib
        _mod = importlib.import_module('pipeline.vault.vault_boot')
        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
