"""Unit tests for pipeline.vault.uuid_floor (§2.2 + §7.4).

Round L. Covers allowlist acceptance, denylist rejection (tmpfs/overlay/fuse),
UUID-zero rejection, evaluate-vs-enforce split, arg-type gates.
"""

from __future__ import annotations

import platform
from pathlib import Path
from unittest import mock

import pytest

from pipeline.vault import schemas
from pipeline.vault.error_codes import F_UUID_01
from pipeline.vault.uuid_floor import (
    ACCEPTED_FS_TYPES,
    DENYLISTED_FS_TYPES,
    UUIDFloorRejected,
    enforce,
    evaluate,
)


def _make_tuple(fs_type: str, volume_uuid: str = "a" * 32) -> schemas.IdentityTuple:
    return schemas.IdentityTuple(
        volume_uuid=volume_uuid,
        fs_file_id="0" * 16,
        mount_id="0" * 16,
        fs_type=fs_type,
        captured_at="2026-04-19T00:00:00Z",
    )


@pytest.fixture
def patched(monkeypatch: pytest.MonkeyPatch):
    """Override the identity_tuple probe with a fixture-controlled return."""
    box: dict[str, schemas.IdentityTuple] = {}

    def fake(path: Path) -> schemas.IdentityTuple:
        return box["tuple"]

    monkeypatch.setattr("pipeline.vault.uuid_floor.resolve_identity_tuple", fake)
    return box


class TestAllowlist:
    # sorted() not list() — frozenset iteration order depends on PYTHONHASHSEED,
    # which means parametrize IDs differ between Python processes. xdist's
    # collection-equivalence check fails on the differing IDs. sorted gives a
    # deterministic test set across workers and CI runs.
    @pytest.mark.parametrize("fs_type", sorted(ACCEPTED_FS_TYPES))
    def test_accepted(self, fs_type: str, patched, tmp_path: Path) -> None:
        patched["tuple"] = _make_tuple(fs_type)
        floor = evaluate(tmp_path)
        assert floor.accepted is True
        assert floor.rejection_reason == ""
        assert floor.fs_type == fs_type


class TestDenylist:
    @pytest.mark.parametrize("fs_type", sorted(DENYLISTED_FS_TYPES))
    def test_rejected_with_reason(
        self, fs_type: str, patched, tmp_path: Path
    ) -> None:
        patched["tuple"] = _make_tuple(fs_type)
        floor = evaluate(tmp_path)
        assert floor.accepted is False
        assert fs_type in floor.rejection_reason

    def test_tmpfs_enforce_raises(self, patched, tmp_path: Path) -> None:
        patched["tuple"] = _make_tuple("tmpfs")
        with pytest.raises(UUIDFloorRejected) as exc:
            enforce(tmp_path)
        assert exc.value.code == F_UUID_01
        assert "tmpfs" in exc.value.reason


class TestUnknownFs:
    def test_unknown_fs_rejected(self, patched, tmp_path: Path) -> None:
        patched["tuple"] = _make_tuple("exfat")
        floor = evaluate(tmp_path)
        assert floor.accepted is False
        assert "exfat" in floor.rejection_reason
        assert "not-on-allowlist" in floor.rejection_reason


class TestZeroUUID:
    def test_zero_uuid_rejected_even_on_apfs(
        self, patched, tmp_path: Path
    ) -> None:
        patched["tuple"] = _make_tuple("apfs", volume_uuid="0" * 32)
        floor = evaluate(tmp_path)
        assert floor.accepted is False
        assert floor.rejection_reason == "volume-uuid-zero"


class TestEnforce:
    def test_enforce_returns_accepted_floor(
        self, patched, tmp_path: Path
    ) -> None:
        patched["tuple"] = _make_tuple("apfs")
        floor = enforce(tmp_path)
        assert floor.accepted is True

    def test_enforce_raises_on_reject(self, patched, tmp_path: Path) -> None:
        patched["tuple"] = _make_tuple("fuse")
        with pytest.raises(UUIDFloorRejected):
            enforce(tmp_path)


class TestArgTypes:
    def test_evaluate_rejects_str(self) -> None:
        with pytest.raises(TypeError):
            evaluate("/tmp")  # type: ignore[arg-type]


class TestLive:
    @pytest.mark.skipif(
        platform.system() not in ("Darwin", "Linux"),
        reason="UUID floor is platform-conditional",
    )
    def test_real_fs_evaluation(self, tmp_path: Path) -> None:
        floor = evaluate(tmp_path)
        # Real dev-box APFS must be accepted; a CI Linux runner mounting ext4
        # will also be accepted. A runner on tmpfs would be rejected.
        # We assert whatever the floor says is internally consistent.
        if floor.accepted:
            assert floor.fs_type in ACCEPTED_FS_TYPES
            assert floor.rejection_reason == ""
        else:
            assert floor.rejection_reason != ""

# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS pin — drift-detection guard (§4.6 engineering_process_v0.1.md)
# ---------------------------------------------------------------------------


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        from pipeline.vault import uuid_floor as _mod

        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
