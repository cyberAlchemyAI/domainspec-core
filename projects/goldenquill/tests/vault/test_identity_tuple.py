"""Unit tests for pipeline.vault.identity_tuple (§2.1 + §7.3).

Round L. Covers mount-table parsing (Darwin + Linux), path→mount matching,
volume-UUID derivation, identity-tuple resolution, arg-type gates.
"""

from __future__ import annotations

import platform
from pathlib import Path
from unittest import mock

import pytest

from pipeline.vault.identity_tuple import (
    IdentityTupleUnavailable,
    _best_mount_match,
    _mount_id_hex,
    _parse_darwin_mounts,
    _parse_proc_mounts,
    _volume_uuid_hex,
    resolve_identity_tuple,
)
from pipeline.vault.schemas import IdentityTuple


_DARWIN_MOUNT_FIXTURE = """\
/dev/disk3s1s1 on / (apfs, sealed, local, read-only, journaled)
devfs on /dev (devfs, local, nobrowse)
/dev/disk3s6 on /System/Volumes/VM (apfs, local, noexec, journaled, noatime, nobrowse)
/dev/disk4 on /Users/goldenquill/workspace (apfs, local, journaled, nosuid)
"""

_PROC_MOUNTS_FIXTURE = """\
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
/dev/nvme0n1p2 / ext4 rw,relatime 0 0
tmpfs /tmp tmpfs rw,nosuid,nodev 0 0
/dev/nvme0n1p3 /home btrfs rw,relatime,space_cache=v2 0 0
"""


class TestParsers:
    def test_parse_darwin_mounts(self) -> None:
        rows = _parse_darwin_mounts(_DARWIN_MOUNT_FIXTURE)
        assert ("/dev/disk3s1s1", "/", "apfs") in rows
        assert ("devfs", "/dev", "devfs") in rows
        assert ("/dev/disk4", "/Users/goldenquill/workspace", "apfs") in rows

    def test_parse_proc_mounts(self) -> None:
        rows = _parse_proc_mounts(_PROC_MOUNTS_FIXTURE)
        assert ("/dev/nvme0n1p2", "/", "ext4") in rows
        assert ("tmpfs", "/tmp", "tmpfs") in rows
        assert ("/dev/nvme0n1p3", "/home", "btrfs") in rows


class TestBestMountMatch:
    def test_longest_prefix_wins_darwin(self, tmp_path: Path) -> None:
        rows = _parse_darwin_mounts(_DARWIN_MOUNT_FIXTURE)
        # tmp_path resolves somewhere under /; longest-prefix match is "/"
        device, mnt, fstype = _best_mount_match(rows, tmp_path)
        assert fstype == "apfs"
        assert mnt == "/"

    def test_deeper_mount_wins_over_root(self) -> None:
        rows = _parse_darwin_mounts(_DARWIN_MOUNT_FIXTURE)
        device, mnt, fstype = _best_mount_match(
            rows, Path("/Users/goldenquill/workspace/file")
        )
        assert mnt == "/Users/goldenquill/workspace"

    def test_no_match_raises(self) -> None:
        rows = [("tmpfs", "/proc", "tmpfs")]
        with pytest.raises(IdentityTupleUnavailable):
            _best_mount_match(rows, Path("/somewhere/else"))


class TestVolumeUuidDerivation:
    def test_changes_with_device(self) -> None:
        a = _volume_uuid_hex("/dev/disk1", "/", "apfs")
        b = _volume_uuid_hex("/dev/disk2", "/", "apfs")
        assert a != b
        assert len(a) == 32
        assert len(b) == 32

    def test_changes_with_fstype(self) -> None:
        a = _volume_uuid_hex("/dev/disk1", "/", "apfs")
        b = _volume_uuid_hex("/dev/disk1", "/", "ext4")
        assert a != b

    def test_stable_across_calls(self) -> None:
        a = _volume_uuid_hex("/dev/disk1", "/mnt", "ext4")
        b = _volume_uuid_hex("/dev/disk1", "/mnt", "ext4")
        assert a == b

    def test_mount_id_is_16_hex(self) -> None:
        mid = _mount_id_hex("/dev/disk1", "/")
        assert len(mid) == 16


class TestResolve:
    @pytest.mark.skipif(
        platform.system() not in ("Darwin", "Linux"),
        reason="identity_tuple is supported on Darwin + Linux only",
    )
    def test_resolve_live(self, tmp_path: Path) -> None:
        tup = resolve_identity_tuple(tmp_path)
        assert isinstance(tup, IdentityTuple)
        assert len(tup.volume_uuid) == 32
        assert len(tup.fs_file_id) == 16
        assert len(tup.mount_id) == 16
        assert tup.fs_type  # non-empty
        assert tup.captured_at.endswith("Z")

    def test_resolve_rejects_non_path(self) -> None:
        with pytest.raises(TypeError):
            resolve_identity_tuple("/tmp")  # type: ignore[arg-type]

    def test_resolve_unsupported_platform(self, tmp_path: Path) -> None:
        with mock.patch("pipeline.vault.identity_tuple.platform.system", return_value="Windows"):
            with pytest.raises(IdentityTupleUnavailable):
                resolve_identity_tuple(tmp_path)

    def test_resolve_nonexistent_file(self, tmp_path: Path) -> None:
        missing = tmp_path / "does_not_exist"
        # mount match works against tmp_path's parent, but stat fails
        with pytest.raises(IdentityTupleUnavailable):
            resolve_identity_tuple(missing)


class TestDarwinProbeFaked:
    def test_probe_routes_through_parser(self, tmp_path: Path) -> None:
        with mock.patch(
            "pipeline.vault.identity_tuple.platform.system", return_value="Darwin"
        ), mock.patch(
            "pipeline.vault.identity_tuple._mount_command_output",
            return_value="/dev/fake on / (apfs, local)\n",
        ):
            tup = resolve_identity_tuple(tmp_path)
            assert tup.fs_type == "apfs"


class TestLinuxProbeFaked:
    def test_probe_routes_through_proc_mounts(
        self, tmp_path: Path
    ) -> None:
        with mock.patch(
            "pipeline.vault.identity_tuple.platform.system", return_value="Linux"
        ), mock.patch(
            "pipeline.vault.identity_tuple.Path.read_text",
            return_value="/dev/sda1 / ext4 rw 0 0\n",
            create=True,
        ):
            tup = resolve_identity_tuple(tmp_path)
            assert tup.fs_type == "ext4"

# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS pin — drift-detection guard (§4.6 engineering_process_v0.1.md)
# ---------------------------------------------------------------------------


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        from pipeline.vault import identity_tuple as _mod

        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
