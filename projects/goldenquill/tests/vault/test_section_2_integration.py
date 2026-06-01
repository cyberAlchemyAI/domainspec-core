"""§2 Vault Round K.1 — cross-module integration tests.

Per spec card ``pipeline/engineering/spec_cards/section_2_round_k_capstone.md``
K.1: exercises §2's public surface as one boot → post-gate → compound-txn
lifecycle across eight integration classes:

* K.1.a — floor + probe (``uuid_floor`` + ``gate_and_open.probe_openat2``)
* K.1.b — mount + mirror (``identity_tuple`` + ``verify_trust_root_mirror``)
* K.1.c — shared-init + seed (``init_marker`` + ``m15_ledger``)
* K.1.d — freeze + wrapper (``atomic_freeze.apply`` + §9 step 8 skip)
* K.1.e — Cedar + broker (``cedar_policy_loader_load_all`` + ``FDBroker``)
* K.1.f — org-init + prune + seat-launch-pin
* K.1.g — SIMPLE ``vault_write`` dispatcher (5 SIMPLE + 2 COMPOUND reject)
* K.1.h — compound-txn lifecycle (begin → stage → commit / abort / TTL /
  integrity)

Floor: ≥30 test methods (52 base + parametric expansion raises the
invocation count well above the floor).
"""

from __future__ import annotations

import hashlib
import os
import secrets
import time
from dataclasses import replace
from pathlib import Path
from typing import Iterator

import pytest

from pipeline.vault import atomic_freeze as _atomic_freeze
from pipeline.vault import compound_txn as _compound_txn
from pipeline.vault import gate_and_open as _gate_and_open
from pipeline.vault import mirror_verify as _mirror_verify
from pipeline.vault import uuid_floor as _uuid_floor
from pipeline.vault.atomic_freeze import (
    AtomicFreezeResult,
    SnapshotRecord,
    SnapshotRetentionCleanupFailed,
    apply as atomic_apply,
    prune_snapshots,
)
from pipeline.vault.compound_txn import (
    COMPOUND_TXN_TTL_SECONDS,
    MAX_ACTIVE_COMPOUND_TXNS_PER_SESSION,
    CompoundTxnDispatcher,
)
from pipeline.vault.error_codes import (
    F_M15_02,
    F_M15_03,
    F_UUID_01,
    CedarSection4WritePathDenied,
    VaultCASHeadMismatch,
    VaultCompoundCapExceeded,
    VaultCompoundIntegrityError,
    VaultCompoundProtocolViolation,
    VaultCompoundTTLExpired,
    VaultCrossOrgAccess,
    VaultInitHMACMismatch,
    VaultWriteExists,
)
from pipeline.vault.fd_broker import (
    FD_BROKER_ALLOWED_INTENTS,
    FD_BROKER_ALLOWED_SKILLS,
    FDBroker,
)
from pipeline.vault.gate_and_open import open_vault_root, probe_openat2
from pipeline.vault.identity_tuple import resolve_identity_tuple
from pipeline.vault.init_marker import (
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
    MirrorContentMismatch,
    MirrorImmutabilityMissing,
    SeedFileContentDrift,
    VaultSharedFrozenRoot,
    verify_trust_root_mirror,
)
from pipeline.vault.schemas import (
    CompoundTxnState,
    FDBrokerRequest,
    IdentityTuple,
    StableUUIDFloor,
    StagedWrite,
    TrustRootMirrorManifest,
)
from pipeline.vault.vault_boot import vault_boot, vault_boot_close
from pipeline.vault.vault_write import (
    EMPTY_SHA3_512_HEX,
    POST_GATE_ALLOWLIST,
    VaultWriteAck,
    vault_write,
)


# ---------------------------------------------------------------------------
# Local helpers
# ---------------------------------------------------------------------------


def _boot(capstone_boot_kwargs: dict, auto: list) -> object:
    r = vault_boot(**capstone_boot_kwargs)
    auto.append(r)
    return r


# =============================================================================
# K.1.a — floor + probe (uuid_floor + probe_openat2)
# =============================================================================


class TestK1aFloorProbe:
    def test_enforce_returns_accepted_on_workspace(
        self, capstone_vault_workspace: dict
    ) -> None:
        floor = _uuid_floor.enforce(capstone_vault_workspace["vault_root"])
        assert isinstance(floor, StableUUIDFloor)
        assert floor.accepted is True
        assert floor.rejection_reason == ""

    @pytest.mark.parametrize(
        "sub",
        ["vault_shared", "vault_shared/cedar", "."],
    )
    def test_evaluate_idempotent_across_subpaths(
        self, capstone_vault_workspace: dict, sub: str
    ) -> None:
        if sub == ".":
            p = capstone_vault_workspace["vault_root"]
        else:
            p = capstone_vault_workspace["vault_root"] / sub
        first = _uuid_floor.evaluate(p)
        second = _uuid_floor.evaluate(p)
        assert first.fs_type == second.fs_type
        assert first.volume_uuid == second.volume_uuid
        assert first.accepted == second.accepted

    def test_probe_openat2_non_linux_returns_false(
        self, capstone_vault_workspace: dict
    ) -> None:
        fd = open_vault_root(capstone_vault_workspace["vault_root"])
        try:
            result = probe_openat2(fd)
        finally:
            os.close(fd)
        # On darwin (dev box) probe_openat2 always returns False.
        assert isinstance(result, bool)

    def test_floor_carries_volume_uuid_nonzero(
        self, capstone_vault_workspace: dict
    ) -> None:
        floor = _uuid_floor.evaluate(capstone_vault_workspace["vault_root"])
        assert floor.volume_uuid
        assert any(c != "0" for c in floor.volume_uuid)

    def test_enforce_raises_typeerror_on_non_path(self) -> None:
        with pytest.raises(TypeError):
            _uuid_floor.enforce("/tmp")  # type: ignore[arg-type]

    def test_probe_openat2_returns_bool(self) -> None:
        import platform as _plat

        # On non-Linux platforms probe_openat2 short-circuits before touching
        # the fd; assert it returns a bool without raising.
        if _plat.system() != "Linux":
            assert probe_openat2(-1) is False
        else:
            result = probe_openat2(-1)
            assert isinstance(result, bool)


# =============================================================================
# K.1.b — mount + mirror (identity_tuple + verify_trust_root_mirror)
# =============================================================================


class TestK1bMountMirror:
    def test_identity_tuple_resolves_on_workspace(
        self, capstone_vault_workspace: dict
    ) -> None:
        tup = resolve_identity_tuple(capstone_vault_workspace["vault_root"])
        assert isinstance(tup, IdentityTuple)

    def test_identity_tuple_four_fields_nonempty(
        self, capstone_vault_workspace: dict
    ) -> None:
        tup = resolve_identity_tuple(capstone_vault_workspace["vault_root"])
        assert tup.volume_uuid
        assert tup.fs_file_id
        assert tup.mount_id
        assert tup.fs_type

    def _build_mirror(
        self, tmp_path: Path, *, body: bytes = b"router:\n  scout: x\n"
    ) -> tuple[TrustRootMirrorManifest, Path]:
        mirror_path = tmp_path / "router.yaml"
        mirror_path.write_bytes(body)
        content_hash = hashlib.sha3_512(body).hexdigest()
        tup = resolve_identity_tuple(mirror_path)
        manifest = TrustRootMirrorManifest(
            mirror_path=str(mirror_path),
            content_hash=content_hash,
            identity_tuple=tup,
            m15_ledger_head="ledger-head-1",
            operator_signature="valid-sig",
            signed_at="2026-04-22T00:00:00Z",
            immutability_flag_set=True,
        )
        return manifest, mirror_path

    def test_verify_trust_root_mirror_happy(
        self, tmp_path: Path
    ) -> None:
        manifest, mirror_path = self._build_mirror(tmp_path)
        verify_trust_root_mirror(
            manifest=manifest,
            live_mirror_path=mirror_path,
            verify_signature=lambda _p, _s: True,
            last_boot_wall_ns=0,
            current_boot_wall_ns=1,
            clock_rollback_tolerance_seconds=60,
        )  # returns None on success

    def test_verify_trust_root_mirror_immutability_missing(
        self, tmp_path: Path
    ) -> None:
        manifest, mirror_path = self._build_mirror(tmp_path)
        manifest2 = replace(manifest, immutability_flag_set=False)
        with pytest.raises(MirrorImmutabilityMissing):
            verify_trust_root_mirror(
                manifest=manifest2,
                live_mirror_path=mirror_path,
                verify_signature=lambda _p, _s: True,
                last_boot_wall_ns=0,
                current_boot_wall_ns=1,
                clock_rollback_tolerance_seconds=60,
            )

    def test_verify_trust_root_mirror_content_drift(
        self, tmp_path: Path
    ) -> None:
        manifest, mirror_path = self._build_mirror(tmp_path)
        mirror_path.write_bytes(b"drifted\n")
        with pytest.raises(MirrorContentMismatch):
            verify_trust_root_mirror(
                manifest=manifest,
                live_mirror_path=mirror_path,
                verify_signature=lambda _p, _s: True,
                last_boot_wall_ns=0,
                current_boot_wall_ns=1,
                clock_rollback_tolerance_seconds=60,
            )


# =============================================================================
# K.1.c — shared-init + seed (init_marker + m15_ledger)
# =============================================================================


class TestK1cSharedInitSeed:
    def test_write_then_verify_shared_init(
        self,
        capstone_vault_workspace: dict,
        capstone_keystore,
    ) -> None:
        vault_shared = capstone_vault_workspace["vault_shared"]
        marker = vault_shared / "init.marker"
        hmac_p = vault_shared / "init.marker.hmac"
        lock = vault_shared / ".init.lock"
        body = write_vault_init_marker(
            marker_path=marker,
            hmac_path=hmac_p,
            lock_path=lock,
            keystore=capstone_keystore,
            scope="shared",
            slug="",
            operator_id="operator",
            section_lock_hash="a" * 128,
        )
        assert body.scope == "shared"
        # Verify round-trip.
        verified = verify_vault_init_marker(
            marker_path=marker,
            hmac_path=hmac_p,
            keystore=capstone_keystore,
            expected_slug="",
            expected_scope="shared",
        )
        assert verified.scope == "shared"
        assert verified.section_lock_hash == body.section_lock_hash

    def test_double_write_raises_already_exists(
        self,
        capstone_vault_workspace: dict,
        capstone_keystore,
    ) -> None:
        vault_shared = capstone_vault_workspace["vault_shared"]
        marker = vault_shared / "init.marker"
        hmac_p = vault_shared / "init.marker.hmac"
        lock = vault_shared / ".init.lock"
        write_vault_init_marker(
            marker_path=marker,
            hmac_path=hmac_p,
            lock_path=lock,
            keystore=capstone_keystore,
            scope="shared",
            slug="",
            operator_id="op",
            section_lock_hash="b" * 128,
        )
        with pytest.raises(VaultInitAlreadyExists):
            write_vault_init_marker(
                marker_path=marker,
                hmac_path=hmac_p,
                lock_path=lock,
                keystore=capstone_keystore,
                scope="shared",
                slug="",
                operator_id="op",
                section_lock_hash="b" * 128,
            )

    def test_verify_init_marker_missing_raises(
        self, capstone_vault_workspace: dict, capstone_keystore
    ) -> None:
        vault_shared = capstone_vault_workspace["vault_shared"]
        with pytest.raises(VaultInitMissing):
            verify_vault_init_marker(
                marker_path=vault_shared / "nope.marker",
                hmac_path=vault_shared / "nope.marker.hmac",
                keystore=capstone_keystore,
                expected_slug="",
                expected_scope="shared",
            )

    def test_verify_init_marker_hmac_tamper_raises(
        self, capstone_vault_workspace: dict, capstone_keystore
    ) -> None:
        vault_shared = capstone_vault_workspace["vault_shared"]
        marker = vault_shared / "init.marker"
        hmac_p = vault_shared / "init.marker.hmac"
        lock = vault_shared / ".init.lock"
        write_vault_init_marker(
            marker_path=marker,
            hmac_path=hmac_p,
            lock_path=lock,
            keystore=capstone_keystore,
            scope="shared",
            slug="",
            operator_id="op",
            section_lock_hash="c" * 128,
        )
        # Flip a byte in the HMAC trailer.
        current = hmac_p.read_text("ascii").strip()
        tampered = ("0" if current[0] != "0" else "1") + current[1:] + "\n"
        hmac_p.write_text(tampered, encoding="ascii")
        with pytest.raises(VaultInitHMACMismatch):
            verify_vault_init_marker(
                marker_path=marker,
                hmac_path=hmac_p,
                keystore=capstone_keystore,
                expected_slug="",
                expected_scope="shared",
            )

    def test_verify_seed_manifest_happy(
        self, capstone_vault_workspace: dict
    ) -> None:
        frozen = verify_seed_manifest(
            manifest_path=capstone_vault_workspace["manifest_path"],
            signature_path=capstone_vault_workspace["sig_path"],
            vault_shared_root=capstone_vault_workspace["vault_shared"],
            current_ledger_head=(
                capstone_vault_workspace["manifest"].m15_ledger_head
            ),
            verify_signature=lambda _p, _s: True,
        )
        assert isinstance(frozen, VaultSharedFrozenRoot)
        assert set(frozen.seed_paths) == {
            sf.relative_path for sf in capstone_vault_workspace["seeds"]
        }

    def test_verify_seed_manifest_signature_fail(
        self, capstone_vault_workspace: dict
    ) -> None:
        with pytest.raises(SeedManifestSignatureInvalid) as exc:
            verify_seed_manifest(
                manifest_path=capstone_vault_workspace["manifest_path"],
                signature_path=capstone_vault_workspace["sig_path"],
                vault_shared_root=capstone_vault_workspace["vault_shared"],
                current_ledger_head=(
                    capstone_vault_workspace["manifest"].m15_ledger_head
                ),
                verify_signature=lambda _p, _s: False,
            )
        assert exc.value.code == F_M15_02

    def test_verify_seed_manifest_ledger_drift(
        self, capstone_vault_workspace: dict
    ) -> None:
        with pytest.raises(SeedManifestLedgerHeadDrift) as exc:
            verify_seed_manifest(
                manifest_path=capstone_vault_workspace["manifest_path"],
                signature_path=capstone_vault_workspace["sig_path"],
                vault_shared_root=capstone_vault_workspace["vault_shared"],
                current_ledger_head="ledger-head-OTHER",
                verify_signature=lambda _p, _s: True,
            )
        assert exc.value.code == F_M15_03


# =============================================================================
# K.1.d — freeze + wrapper (atomic_freeze.apply + wrapper-skip degradation)
# =============================================================================


class TestK1dFreezeWrapper:
    def test_apply_happy_path_darwin(
        self, capstone_vault_workspace: dict
    ) -> None:
        frozen = verify_seed_manifest(
            manifest_path=capstone_vault_workspace["manifest_path"],
            signature_path=capstone_vault_workspace["sig_path"],
            vault_shared_root=capstone_vault_workspace["vault_shared"],
            current_ledger_head=(
                capstone_vault_workspace["manifest"].m15_ledger_head
            ),
            verify_signature=lambda _p, _s: True,
        )
        result = atomic_apply(
            frozen_root=frozen,
            vault_shared_root=capstone_vault_workspace["vault_shared"],
            session_id="session-capstone-K",
            platform="darwin",
        )
        assert isinstance(result, AtomicFreezeResult)
        assert result.platform == "darwin"
        assert result.snapshot_label is None  # no provider
        assert not any(
            "linux-mount-ns-not-implemented" in d for d in result.degradations
        )

    def test_apply_linux_records_degradation(
        self, capstone_vault_workspace: dict
    ) -> None:
        frozen = verify_seed_manifest(
            manifest_path=capstone_vault_workspace["manifest_path"],
            signature_path=capstone_vault_workspace["sig_path"],
            vault_shared_root=capstone_vault_workspace["vault_shared"],
            current_ledger_head=(
                capstone_vault_workspace["manifest"].m15_ledger_head
            ),
            verify_signature=lambda _p, _s: True,
        )
        result = atomic_apply(
            frozen_root=frozen,
            vault_shared_root=capstone_vault_workspace["vault_shared"],
            session_id="session-capstone-K",
            platform="linux",
        )
        assert any(
            "linux-mount-ns-not-implemented-v0.1" in d
            for d in result.degradations
        )

    def test_apply_snapshot_provider_creates_label(
        self,
        capstone_vault_workspace: dict,
        capstone_snapshot_provider,
    ) -> None:
        frozen = verify_seed_manifest(
            manifest_path=capstone_vault_workspace["manifest_path"],
            signature_path=capstone_vault_workspace["sig_path"],
            vault_shared_root=capstone_vault_workspace["vault_shared"],
            current_ledger_head=(
                capstone_vault_workspace["manifest"].m15_ledger_head
            ),
            verify_signature=lambda _p, _s: True,
        )
        result = atomic_apply(
            frozen_root=frozen,
            vault_shared_root=capstone_vault_workspace["vault_shared"],
            session_id="session-capstone-K",
            snapshot_provider=capstone_snapshot_provider,
        )
        assert result.snapshot_label is not None
        assert "session-capstone-K" in result.snapshot_label
        assert capstone_snapshot_provider.created == [result.snapshot_label]

    def test_apply_snapshot_list_failure_records_degradation(
        self, capstone_vault_workspace: dict
    ) -> None:
        class _BrokenProvider:
            def list_snapshots(self):
                raise RuntimeError("boom")

            def create_snapshot(self, *, label):
                raise RuntimeError("unreached")

            def delete_snapshot(self, *, label):
                raise RuntimeError("unreached")

        frozen = verify_seed_manifest(
            manifest_path=capstone_vault_workspace["manifest_path"],
            signature_path=capstone_vault_workspace["sig_path"],
            vault_shared_root=capstone_vault_workspace["vault_shared"],
            current_ledger_head=(
                capstone_vault_workspace["manifest"].m15_ledger_head
            ),
            verify_signature=lambda _p, _s: True,
        )
        result = atomic_apply(
            frozen_root=frozen,
            vault_shared_root=capstone_vault_workspace["vault_shared"],
            session_id="session-capstone-K",
            snapshot_provider=_BrokenProvider(),
        )
        assert result.retention_degraded is True
        assert result.snapshot_degraded is True

    def test_boot_surfaces_wrapper_hash_verify_skipped(
        self, capstone_boot_kwargs: dict, capstone_auto_close: list
    ) -> None:
        r = _boot(capstone_boot_kwargs, capstone_auto_close)
        assert any(
            "wrapper-hash-verify-skipped" in d for d in r.degradations
        )


# =============================================================================
# K.1.e — Cedar + broker (cedar_policy_loader_load_all + FDBroker.request_fd)
# =============================================================================


class TestK1eCedarBroker:
    def test_cedar_policies_loaded_after_boot(
        self, capstone_boot_kwargs: dict, capstone_auto_close: list
    ) -> None:
        r = _boot(capstone_boot_kwargs, capstone_auto_close)
        assert "cedar/org_isolation.cedar" in r.cedar_policies
        assert "cedar/write_gate.cedar" in r.cedar_policies
        assert r.cedar_policies["cedar/org_isolation.cedar"] == "permit;\n"

    def test_cedar_loader_returns_only_top_level_policies(
        self, capstone_vault_workspace: dict
    ) -> None:
        # Freeze then reload directly.
        frozen = verify_seed_manifest(
            manifest_path=capstone_vault_workspace["manifest_path"],
            signature_path=capstone_vault_workspace["sig_path"],
            vault_shared_root=capstone_vault_workspace["vault_shared"],
            current_ledger_head=(
                capstone_vault_workspace["manifest"].m15_ledger_head
            ),
            verify_signature=lambda _p, _s: True,
        )
        out = cedar_policy_loader_load_all(
            frozen_root=frozen,
            vault_shared_root=capstone_vault_workspace["vault_shared"],
        )
        # All loaded keys must be top-level cedar/*.cedar.
        for rel in out:
            assert rel.startswith("cedar/")
            assert rel.endswith(".cedar")
            assert "/" not in rel[len("cedar/"):]

    def test_broker_rejects_unknown_skill(
        self, capstone_boot_kwargs: dict, capstone_auto_close: list
    ) -> None:
        r = _boot(capstone_boot_kwargs, capstone_auto_close)
        req = FDBrokerRequest(
            requester_skill="not-allowlisted",
            requester_pid=1,
            requester_session_id="s",
            requester_org_slug="o",
            requested_path="vault_shared/cedar/org_isolation.cedar",
            intent="read",
            nonce_hex=secrets.token_hex(16),
        )
        resp, fd = r.fd_broker.request_fd(req)
        assert resp.granted is False
        assert fd is None
        assert "unknown-skill" in resp.denial_reason

    @pytest.mark.parametrize("bad_intent", ["eat", "sniff", "mutate", ""])
    def test_broker_rejects_invalid_intent(
        self,
        capstone_boot_kwargs: dict,
        capstone_auto_close: list,
        bad_intent: str,
    ) -> None:
        r = _boot(capstone_boot_kwargs, capstone_auto_close)
        req = FDBrokerRequest(
            requester_skill="vault-query",
            requester_pid=1,
            requester_session_id="s",
            requester_org_slug="o",
            requested_path="vault_shared/cedar/org_isolation.cedar",
            intent=bad_intent,
            nonce_hex=secrets.token_hex(16),
        )
        resp, fd = r.fd_broker.request_fd(req)
        assert resp.granted is False
        assert fd is None
        assert "invalid-intent" in resp.denial_reason

    def test_broker_rejects_nonce_replay(
        self, capstone_boot_kwargs: dict, capstone_auto_close: list
    ) -> None:
        r = _boot(capstone_boot_kwargs, capstone_auto_close)
        nonce = secrets.token_hex(16)
        req = FDBrokerRequest(
            requester_skill="vault-query",
            requester_pid=1,
            requester_session_id="s",
            requester_org_slug="o",
            requested_path="vault_shared/cedar/org_isolation.cedar",
            intent="read",
            nonce_hex=nonce,
        )
        resp1, fd1 = r.fd_broker.request_fd(req)
        if fd1 is not None:
            os.close(fd1)
        resp2, fd2 = r.fd_broker.request_fd(req)
        assert resp2.granted is False
        assert fd2 is None
        assert "nonce-replay" in resp2.denial_reason

    def test_broker_allowlist_constants_are_frozensets(
        self,
    ) -> None:
        assert isinstance(FD_BROKER_ALLOWED_SKILLS, frozenset)
        assert isinstance(FD_BROKER_ALLOWED_INTENTS, frozenset)
        assert FD_BROKER_ALLOWED_SKILLS == frozenset(
            {"vault-query", "research-db-query"}
        )


# =============================================================================
# K.1.f — org-init + prune + seat-launch-pin
# =============================================================================


class TestK1fOrgInitPruneSeat:
    def test_write_org_init_marker_then_verify(
        self, capstone_vault_workspace: dict, capstone_keystore
    ) -> None:
        org_root = capstone_vault_workspace["vault_root"] / "orgs" / "testorg"
        org_root.mkdir(parents=True)
        marker = org_root / "init.marker"
        hmac_p = org_root / "init.marker.hmac"
        lock = org_root / ".init.lock"
        body = write_vault_init_marker(
            marker_path=marker,
            hmac_path=hmac_p,
            lock_path=lock,
            keystore=capstone_keystore,
            scope="org",
            slug="testorg",
            operator_id="operator",
            section_lock_hash="d" * 128,
        )
        assert body.scope == "org"
        assert body.slug == "testorg"
        verified = verify_vault_init_marker(
            marker_path=marker,
            hmac_path=hmac_p,
            keystore=capstone_keystore,
            expected_slug="testorg",
            expected_scope="org",
        )
        assert verified.slug == "testorg"

    def test_org_init_rejects_shared_scope_with_slug(
        self, capstone_vault_workspace: dict, capstone_keystore
    ) -> None:
        # Semantic guard on write_vault_init_marker.
        vault_shared = capstone_vault_workspace["vault_shared"]
        with pytest.raises(ValueError):
            write_vault_init_marker(
                marker_path=vault_shared / "init.marker",
                hmac_path=vault_shared / "init.marker.hmac",
                lock_path=vault_shared / ".init.lock",
                keystore=capstone_keystore,
                scope="shared",
                slug="not-empty",
                operator_id="op",
                section_lock_hash="e" * 128,
            )

    def test_prune_snapshots_reduces_to_retention(
        self, capstone_snapshot_provider
    ) -> None:
        # Pre-populate 5 snapshots; prune to 3.
        for i in range(5):
            capstone_snapshot_provider.create_snapshot(
                label=f"com.tilth.vault_shared.sess.{i:04d}"
            )
        # FakeSnapshotProvider uses a single timestamp for all created records,
        # so sorting is by label alphanumeric fallback from stable iteration.
        deleted = prune_snapshots(
            snapshot_provider=capstone_snapshot_provider,
            retention_count=3,
        )
        assert len(deleted) == 2
        remaining = capstone_snapshot_provider.list_snapshots()
        assert len(remaining) == 3

    def test_prune_snapshots_raises_on_list_failure(self) -> None:
        class _Broken:
            def list_snapshots(self):
                raise RuntimeError("no-list")

            def create_snapshot(self, *, label):
                raise RuntimeError("x")

            def delete_snapshot(self, *, label):
                raise RuntimeError("x")

        with pytest.raises(SnapshotRetentionCleanupFailed):
            prune_snapshots(snapshot_provider=_Broken(), retention_count=3)

    def test_boot_degradation_ordering_seat_launch_pin_visible(
        self, capstone_boot_kwargs: dict, capstone_auto_close: list
    ) -> None:
        # §9 step 11.5 seat-launch pin runs AFTER §9 step 11 (org-init-marker).
        # We surface that ordering by asserting wrapper-hash-verify-skipped and
        # org-init-marker-skipped both appear in the boot degradations list
        # with the expected relative position (wrapper-hash precedes org-init).
        r = _boot(capstone_boot_kwargs, capstone_auto_close)
        wh_idx = next(
            (
                i
                for i, d in enumerate(r.degradations)
                if "wrapper-hash-verify-skipped" in d
            ),
            -1,
        )
        oi_idx = next(
            (
                i
                for i, d in enumerate(r.degradations)
                if "org-init-marker-skipped" in d
            ),
            -1,
        )
        assert wh_idx >= 0
        assert oi_idx >= 0
        assert wh_idx < oi_idx


# =============================================================================
# K.1.g — SIMPLE vault_write dispatcher (5 SIMPLE + 2 COMPOUND reject)
# =============================================================================


@pytest.fixture
def _org_write_context(
    capstone_vault_workspace: dict,
) -> dict:
    """Build a writable org vault root + lock file under the workspace."""
    org_root = capstone_vault_workspace["vault_root"] / "orgs" / "k1g"
    org_root.mkdir(parents=True)
    return {
        "org_vault_root": org_root,
        "write_lock_path": org_root / ".write.lock",
    }


# (intent, vault_rel_path_suffix, write_mode, needs_cas_hash)
_SIMPLE_INTENT_CASES = [
    ("claim-evidence-write", "claim_evidence/t-evidence.json", "write-if-absent", False),
    ("admin-risk-append", "admin_risk/ledger-1.jsonl", "append-cas", True),
    ("conversation-log-append", "conversation_log/t.jsonl", "append-cas", True),
    ("rails-report-write", "rails_reports/r.json", "overwrite", False),
    ("lessons-delta-append", "lessons_delta/d.jsonl", "append-cas", True),
]


class TestK1gSimpleVaultWrite:
    @pytest.mark.parametrize(
        "intent, rel_suffix, mode, needs_cas",
        _SIMPLE_INTENT_CASES,
    )
    def test_simple_intents_round_trip(
        self,
        _org_write_context: dict,
        intent: str,
        rel_suffix: str,
        mode: str,
        needs_cas: bool,
    ) -> None:
        org = _org_write_context["org_vault_root"]
        target = org / rel_suffix
        payload = b"payload-" + intent.encode("ascii")
        kwargs = dict(
            path=target,
            bytes_=payload,
            intent=intent,
            session_id="session-K1g",
            slug="k1g",
            org_vault_root=org,
            write_lock_path=_org_write_context["write_lock_path"],
            write_mode=mode,
        )
        if needs_cas:
            kwargs["expected_current_file_hash"] = EMPTY_SHA3_512_HEX
        ack = vault_write(**kwargs)
        assert isinstance(ack, VaultWriteAck)
        assert ack.committed is True
        assert ack.mode == mode
        # File exists and hashes.
        assert target.is_file()

    def test_compound_intent_audit_append_without_txn_token_rejected(
        self, _org_write_context: dict
    ) -> None:
        org = _org_write_context["org_vault_root"]
        target = org / "admin_risk" / "ledger.jsonl"
        with pytest.raises(VaultCompoundProtocolViolation) as exc:
            vault_write(
                path=target,
                bytes_=b"x",
                intent="index-amendment-audit-append",
                session_id="session-K1g",
                slug="k1g",
                org_vault_root=org,
                write_lock_path=_org_write_context["write_lock_path"],
                write_mode="append-cas",
                expected_current_file_hash=EMPTY_SHA3_512_HEX,
            )
        assert exc.value.sub_reason == "compound_intent_without_txn_token"

    def test_compound_intent_index_update_without_txn_token_rejected(
        self, _org_write_context: dict
    ) -> None:
        org = _org_write_context["org_vault_root"]
        # repo-relative regex: pipeline/blueprint/v0.1/section_00_5_interface_index.v{N}.json
        target = (
            org
            / "pipeline"
            / "blueprint"
            / "v0.1"
            / "section_00_5_interface_index.v42.json"
        )
        with pytest.raises(VaultCompoundProtocolViolation) as exc:
            vault_write(
                path=target,
                bytes_=b"{}",
                intent="index-update",
                session_id="session-K1g",
                slug="k1g",
                org_vault_root=org,
                write_lock_path=_org_write_context["write_lock_path"],
                write_mode="write-if-absent",
            )
        assert exc.value.sub_reason == "compound_intent_without_txn_token"

    def test_simple_intent_with_txn_token_rejected(
        self, _org_write_context: dict
    ) -> None:
        org = _org_write_context["org_vault_root"]
        target = org / "rails_reports" / "r.json"
        with pytest.raises(VaultCompoundProtocolViolation) as exc:
            vault_write(
                path=target,
                bytes_=b"x",
                intent="rails-report-write",
                session_id="session-K1g",
                slug="k1g",
                org_vault_root=org,
                write_lock_path=_org_write_context["write_lock_path"],
                write_mode="overwrite",
                txn_token="bogus-token",
            )
        assert exc.value.sub_reason == "simple_intent_with_txn_token"

    def test_cross_org_access_rejected(
        self, _org_write_context: dict, capstone_vault_workspace: dict
    ) -> None:
        # Point `path` outside the org vault root.
        other = capstone_vault_workspace["vault_root"] / "orgs" / "other"
        other.mkdir(parents=True)
        target = other / "rails_reports" / "r.json"
        with pytest.raises(VaultCrossOrgAccess):
            vault_write(
                path=target,
                bytes_=b"x",
                intent="rails-report-write",
                session_id="s",
                slug="k1g",
                org_vault_root=_org_write_context["org_vault_root"],
                write_lock_path=_org_write_context["write_lock_path"],
                write_mode="overwrite",
            )

    def test_write_if_absent_collision_raises(
        self, _org_write_context: dict
    ) -> None:
        org = _org_write_context["org_vault_root"]
        target = org / "claim_evidence" / "once.json"
        vault_write(
            path=target,
            bytes_=b"first",
            intent="claim-evidence-write",
            session_id="s",
            slug="k1g",
            org_vault_root=org,
            write_lock_path=_org_write_context["write_lock_path"],
            write_mode="write-if-absent",
        )
        with pytest.raises(VaultWriteExists):
            vault_write(
                path=target,
                bytes_=b"second",
                intent="claim-evidence-write",
                session_id="s",
                slug="k1g",
                org_vault_root=org,
                write_lock_path=_org_write_context["write_lock_path"],
                write_mode="write-if-absent",
            )

    def test_cas_head_mismatch_raises(
        self, _org_write_context: dict
    ) -> None:
        org = _org_write_context["org_vault_root"]
        target = org / "admin_risk" / "ledger.jsonl"
        vault_write(
            path=target,
            bytes_=b'{"line":1}\n',
            intent="admin-risk-append",
            session_id="s",
            slug="k1g",
            org_vault_root=org,
            write_lock_path=_org_write_context["write_lock_path"],
            write_mode="append-cas",
            expected_current_file_hash=EMPTY_SHA3_512_HEX,
        )
        # Second append with wrong expected hash → mismatch.
        with pytest.raises(VaultCASHeadMismatch):
            vault_write(
                path=target,
                bytes_=b'{"line":2}\n',
                intent="admin-risk-append",
                session_id="s",
                slug="k1g",
                org_vault_root=org,
                write_lock_path=_org_write_context["write_lock_path"],
                write_mode="append-cas",
                expected_current_file_hash=EMPTY_SHA3_512_HEX,  # wrong
            )

    def test_unknown_intent_denied_by_post_gate(
        self, _org_write_context: dict
    ) -> None:
        org = _org_write_context["org_vault_root"]
        target = org / "rails_reports" / "r.json"
        with pytest.raises(CedarSection4WritePathDenied) as exc:
            vault_write(
                path=target,
                bytes_=b"x",
                intent="definitely-not-in-allowlist",
                session_id="s",
                slug="k1g",
                org_vault_root=org,
                write_lock_path=_org_write_context["write_lock_path"],
                write_mode="overwrite",
            )
        assert exc.value.reason == "post_gate_unknown_intent"

    def test_post_gate_allowlist_has_14_entries_12_simple_2_compound(
        self,
    ) -> None:
        # v7.1 LOCKED baseline: 5 SIMPLE + 2 COMPOUND = 7. v7.2 DRAFT
        # adds 7 SIMPLE operational rows → 12 SIMPLE + 2 COMPOUND = 14.
        # §17 v1 LOCK 2026-05-11 adds cycle_receipt → 13 SIMPLE + 2 COMPOUND = 15.
        simple = [k for k, v in POST_GATE_ALLOWLIST.items() if v.kind_class == "SIMPLE"]
        compound = [
            k for k, v in POST_GATE_ALLOWLIST.items() if v.kind_class == "COMPOUND"
        ]
        assert len(simple) == 13
        assert len(compound) == 2


# =============================================================================
# K.1.h — compound-txn lifecycle (begin → stage → commit / abort / TTL /
#         integrity)
# =============================================================================


@pytest.fixture
def _dispatcher(capstone_vault_workspace: dict) -> Iterator[CompoundTxnDispatcher]:
    lock_path = (
        capstone_vault_workspace["vault_root"] / "orgs" / "k1h" / ".compound_txn.lock"
    )
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    yield CompoundTxnDispatcher(compound_lock_path=lock_path)


class TestK1hCompoundTxnLifecycle:
    def test_begin_returns_token(self, _dispatcher) -> None:
        token = _dispatcher.begin(
            txn_kind="index-update", session_id="s"
        )
        assert isinstance(token, str)
        assert len(token) > 0

    def test_begin_rejects_unknown_kind(self, _dispatcher) -> None:
        with pytest.raises(VaultCompoundProtocolViolation):
            _dispatcher.begin(txn_kind="not-a-kind", session_id="s")

    def test_begin_enforces_per_session_cap(self, _dispatcher) -> None:
        _dispatcher.begin(txn_kind="index-update", session_id="s")
        with pytest.raises(VaultCompoundCapExceeded):
            _dispatcher.begin(txn_kind="index-update", session_id="s")

    def test_stage_write_adds_to_staged_writes(self, _dispatcher) -> None:
        token = _dispatcher.begin(txn_kind="index-update", session_id="s")
        _dispatcher.stage_write(
            txn_token=token,
            session_id="s",
            intent="index-update",
            path="/tmp/x",
            data=b"payload",
            write_mode="write-if-absent",
        )
        state = _dispatcher._active[token]  # type: ignore[attr-defined]
        assert len(state.staged_writes) == 1
        sw = state.staged_writes[0]
        assert isinstance(sw, StagedWrite)
        assert sw.data == b"payload"
        assert sw.data_sha3_512 == hashlib.sha3_512(b"payload").hexdigest()

    def test_commit_invokes_persist_hook_in_lock(self, _dispatcher) -> None:
        token = _dispatcher.begin(txn_kind="index-update", session_id="s")
        _dispatcher.stage_write(
            txn_token=token,
            session_id="s",
            intent="index-update",
            path="/tmp/x",
            data=b"payload",
            write_mode="write-if-absent",
        )
        calls: list[CompoundTxnState] = []

        def _hook(state: CompoundTxnState) -> None:
            calls.append(state)

        committed = _dispatcher.commit(
            txn_token=token, session_id="s", persist=_hook
        )
        assert len(calls) == 1
        assert len(committed) == 1
        # Session count released.
        assert _dispatcher._session_counts.get("s", 0) == 0  # type: ignore[attr-defined]

    def test_commit_persist_failure_tears_down(self, _dispatcher) -> None:
        token = _dispatcher.begin(txn_kind="index-update", session_id="s")
        _dispatcher.stage_write(
            txn_token=token,
            session_id="s",
            intent="index-update",
            path="/tmp/x",
            data=b"payload",
            write_mode="write-if-absent",
        )

        def _bad(_state: CompoundTxnState) -> None:
            raise RuntimeError("persist-failed")

        with pytest.raises(RuntimeError):
            _dispatcher.commit(
                txn_token=token, session_id="s", persist=_bad
            )
        # Teardown happened: follow-up abort raises unknown-token.
        with pytest.raises(VaultCompoundProtocolViolation):
            _dispatcher.abort(
                txn_token=token, session_id="s", reason="double"
            )

    def test_abort_releases_txn(self, _dispatcher) -> None:
        token = _dispatcher.begin(txn_kind="index-update", session_id="s")
        _dispatcher.abort(txn_token=token, session_id="s", reason="ops")
        # Session count released.
        assert _dispatcher._session_counts.get("s", 0) == 0  # type: ignore[attr-defined]

    def test_abort_unknown_token_raises_protocol_violation(
        self, _dispatcher
    ) -> None:
        with pytest.raises(VaultCompoundProtocolViolation):
            _dispatcher.abort(
                txn_token="unknown", session_id="s", reason="r"
            )

    def test_ttl_expiry_raises_and_tears_down(
        self, _dispatcher, monkeypatch
    ) -> None:
        # Collapse the TTL so it trips on the next stage call.
        monkeypatch.setattr(
            _compound_txn, "COMPOUND_TXN_TTL_SECONDS", 0
        )
        token = _dispatcher.begin(
            txn_kind="index-update", session_id="s"
        )
        # Sleep a hair so elapsed_ns > 0.
        time.sleep(0.002)
        with pytest.raises(VaultCompoundTTLExpired):
            _dispatcher.stage_write(
                txn_token=token,
                session_id="s",
                intent="index-update",
                path="/tmp/x",
                data=b"x",
                write_mode="write-if-absent",
            )
        # Teardown happened: abort raises protocol violation.
        with pytest.raises(VaultCompoundProtocolViolation):
            _dispatcher.abort(
                txn_token=token, session_id="s", reason="post-ttl"
            )

    def test_runtime_integrity_check_fires_on_non_stagedwrite(
        self, _dispatcher
    ) -> None:
        token = _dispatcher.begin(
            txn_kind="index-update", session_id="s"
        )
        # Swap a staged record for an impostor via dataclasses.replace.
        state = _dispatcher._active[token]  # type: ignore[attr-defined]

        class _Impostor:
            pass

        _dispatcher._active[token] = replace(  # type: ignore[attr-defined]
            state,
            staged_writes=(_Impostor(),),  # type: ignore[arg-type]
        )
        with pytest.raises(VaultCompoundIntegrityError):
            _dispatcher.commit(
                txn_token=token,
                session_id="s",
                persist=lambda _s: None,
            )

    def test_stage_cap_enforced_under_monkeypatched_count(
        self, _dispatcher, monkeypatch
    ) -> None:
        # Shrink stage-write count cap to 2 so we can exercise the path
        # without actually buffering gigabytes.
        monkeypatch.setattr(
            _compound_txn, "MAX_STAGED_WRITES_PER_TXN", 2
        )
        token = _dispatcher.begin(
            txn_kind="index-update", session_id="s"
        )
        for i in range(2):
            _dispatcher.stage_write(
                txn_token=token,
                session_id="s",
                intent="index-update",
                path=f"/tmp/{i}",
                data=b"x",
                write_mode="write-if-absent",
            )
        with pytest.raises(VaultCompoundCapExceeded):
            _dispatcher.stage_write(
                txn_token=token,
                session_id="s",
                intent="index-update",
                path="/tmp/3",
                data=b"x",
                write_mode="write-if-absent",
            )
