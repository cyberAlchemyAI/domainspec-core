"""Unit tests for pipeline.vault.metadata_homogenizer (§4.2 + §7.6).

Round O. Covers:
* Size-bucket selection boundaries (just-below, exact, just-above).
* Timestamp floor projection (mtime/ctime clamped to boot clock).
* atime suppression (atime == mtime).
* Xattr strip full sweep + post-check empty.
* Xattr strip raises on residual.
* Seed-vs-cache classification.
* Arg-type gates.
"""

from __future__ import annotations

import os
import platform
from pathlib import Path
from unittest import mock

import pytest

from pipeline.vault.error_codes import VaultXattrStripIncomplete
from pipeline.vault.metadata_homogenizer import (
    SIZE_BUCKETS,
    HomogenizedStat,
    homogenize_stat,
    is_cache_page_path,
    pick_size_bucket,
    strip_all_xattrs,
)


# ---------------------------------------------------------------------------
# Size buckets
# ---------------------------------------------------------------------------


class TestSizeBucket:
    def test_exact_bucket_passes_through(self) -> None:
        for b in SIZE_BUCKETS:
            assert pick_size_bucket(b) == b

    def test_just_below_bucket_rounds_up(self) -> None:
        assert pick_size_bucket(1) == 4 * 1024
        assert pick_size_bucket(4 * 1024 - 1) == 4 * 1024
        assert pick_size_bucket(4 * 1024 + 1) == 64 * 1024

    def test_empty_file_uses_smallest_bucket(self) -> None:
        assert pick_size_bucket(0) == 4 * 1024

    def test_above_largest_bucket_returned_unpadded(self) -> None:
        huge = 300 * 1024 * 1024
        assert pick_size_bucket(huge) == huge

    def test_negative_rejected(self) -> None:
        with pytest.raises(ValueError):
            pick_size_bucket(-1)

    def test_non_int_rejected(self) -> None:
        with pytest.raises(TypeError):
            pick_size_bucket("4096")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Timestamp homogenization
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_file(tmp_path: Path) -> Path:
    p = tmp_path / "sample.bin"
    p.write_bytes(b"x" * 100)
    return p


class TestHomogenizeStat:
    def test_mtime_clamped_to_boot_clock(self, sample_file: Path) -> None:
        raw = os.stat(sample_file)
        boot = raw.st_mtime - 10.0
        h = homogenize_stat(raw, vault_boot_wall_clock=boot)
        assert h.st_mtime <= boot
        assert h.st_ctime <= boot

    def test_mtime_floored_to_second(self, sample_file: Path) -> None:
        raw = os.stat(sample_file)
        boot = raw.st_mtime + 1000.5
        h = homogenize_stat(raw, vault_boot_wall_clock=boot)
        # Boot floor -> int second boundary
        assert h.st_mtime == float(int(raw.st_mtime))

    def test_atime_suppressed_to_mtime(self, sample_file: Path) -> None:
        raw = os.stat(sample_file)
        boot = raw.st_mtime + 1000
        h = homogenize_stat(raw, vault_boot_wall_clock=boot)
        assert h.st_atime == h.st_mtime

    def test_size_preserved_if_no_padding(self, sample_file: Path) -> None:
        raw = os.stat(sample_file)
        h = homogenize_stat(raw, vault_boot_wall_clock=raw.st_mtime + 1)
        assert h.st_size == raw.st_size

    def test_size_padded_when_requested(self, sample_file: Path) -> None:
        raw = os.stat(sample_file)
        h = homogenize_stat(
            raw, vault_boot_wall_clock=raw.st_mtime + 1, padded_size=4096
        )
        assert h.st_size == 4096

    def test_inode_and_dev_preserved(self, sample_file: Path) -> None:
        raw = os.stat(sample_file)
        h = homogenize_stat(raw, vault_boot_wall_clock=raw.st_mtime + 1)
        assert h.st_ino == raw.st_ino
        assert h.st_dev == raw.st_dev

    def test_rejects_non_stat_result(self) -> None:
        with pytest.raises(TypeError):
            homogenize_stat({}, vault_boot_wall_clock=0)  # type: ignore[arg-type]

    def test_rejects_non_number_boot_clock(self, sample_file: Path) -> None:
        raw = os.stat(sample_file)
        with pytest.raises(TypeError):
            homogenize_stat(raw, vault_boot_wall_clock="now")  # type: ignore[arg-type]

    def test_is_frozen_dataclass(self, sample_file: Path) -> None:
        raw = os.stat(sample_file)
        h = homogenize_stat(raw, vault_boot_wall_clock=raw.st_mtime + 1)
        with pytest.raises(Exception):
            h.st_size = 0  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Xattr strip
# ---------------------------------------------------------------------------


@pytest.fixture
def fd_for(tmp_path: Path):
    p = tmp_path / "xattr-target.bin"
    p.write_bytes(b"x")
    fd = os.open(str(p), os.O_RDWR)
    yield fd
    try:
        os.close(fd)
    except OSError:
        pass


class TestStripXattrs:
    def _can_setxattr(self, fd: int) -> bool:
        setxattr = getattr(os, "setxattr", None)
        if setxattr is None:
            return False
        try:
            setxattr(fd, "user.tilth.test", b"v")
            return True
        except (OSError, NotImplementedError):
            return False

    def test_noop_when_no_xattrs(self, fd_for: int) -> None:
        # Should not raise even if fs does not support xattrs.
        strip_all_xattrs(fd_for)

    def test_strips_user_xattr(self, fd_for: int) -> None:
        if not self._can_setxattr(fd_for):
            pytest.skip("fs does not support setting user xattrs")
        strip_all_xattrs(fd_for)
        assert not os.listxattr(fd_for)

    def test_residual_xattr_raises(self, fd_for: int) -> None:
        # Force a residual by making _remove_xattr a no-op.
        with mock.patch(
            "pipeline.vault.metadata_homogenizer._remove_xattr",
            side_effect=lambda fd, key: None,
        ), mock.patch(
            "pipeline.vault.metadata_homogenizer._list_xattrs",
            side_effect=[["user.stuck"], ["user.stuck"]],
        ):
            with pytest.raises(VaultXattrStripIncomplete) as exc:
                strip_all_xattrs(fd_for)
            assert "user.stuck" in exc.value.residual_keys

    def test_strip_rejects_non_int_fd(self) -> None:
        with pytest.raises(TypeError):
            strip_all_xattrs("not-an-fd")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Cache-page classification
# ---------------------------------------------------------------------------


class TestIsCachePagePath:
    @pytest.mark.parametrize(
        "path",
        [
            "cached_opportunities/x.json",
            "orgs/myco/cached_opportunities/x.json",
            "research_db/_cache/2026/opp.json",
            "research_db/foo.json",
        ],
    )
    def test_cache_paths(self, path: str) -> None:
        assert is_cache_page_path(path) is True

    @pytest.mark.parametrize(
        "path",
        [
            "research_db/seed/usda.json",
            "research_db/seed/foundations.yaml",
            "orgs/myco/vault/drafts/a.md",
            "vault_shared/seed.manifest.json",
        ],
    )
    def test_seed_and_non_cache_paths(self, path: str) -> None:
        assert is_cache_page_path(path) is False

    def test_rejects_non_str(self) -> None:
        with pytest.raises(TypeError):
            is_cache_page_path(b"bytes")  # type: ignore[arg-type]

# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS pin — drift-detection guard (§4.6 engineering_process_v0.1.md)
# ---------------------------------------------------------------------------


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        from pipeline.vault import metadata_homogenizer as _mod

        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
