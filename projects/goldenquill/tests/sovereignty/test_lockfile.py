"""Unit tests for pipeline.sovereignty.lockfile.safe_open_lock_file.

Section 1 Round I. Covers §3.11c + §6.7 F-ISO-07 + §7.15 named tests.

Named tests per §7.15:

* ``test_safe_open_lock_file_rejects_symlink``
* ``test_safe_open_lock_file_rejects_swapped_inode_post_open``
* ``test_safe_open_lock_file_rejects_foreign_uid`` (uses monkeypatch,
  skipped without monkeypatching of ``os.fstat`` result since running
  under root is the alternative).
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from pipeline.sovereignty.lockfile import (
    LOCK_FILE_OPEN_FLAGS,
    LockFileSymlinkAttack,
    safe_open_lock_file,
)


class TestHappyPath:
    def test_creates_lock_file(self, tmp_path: Path) -> None:
        lock = tmp_path / "foo.lock"
        fd = safe_open_lock_file(lock)
        try:
            assert lock.is_file()
            assert os.fstat(fd).st_uid == os.getuid()
        finally:
            os.close(fd)

    def test_reopens_existing_lock(self, tmp_path: Path) -> None:
        lock = tmp_path / "foo.lock"
        lock.write_bytes(b"")
        fd = safe_open_lock_file(lock)
        try:
            assert lock.is_file()
        finally:
            os.close(fd)


class TestArgTypes:
    def test_type_error_on_str(self) -> None:
        with pytest.raises(TypeError):
            safe_open_lock_file("/tmp/foo.lock")  # type: ignore[arg-type]


class TestSymlinkGuards:
    def test_safe_open_lock_file_rejects_symlink(self, tmp_path: Path) -> None:
        target = tmp_path / "elsewhere.txt"
        target.write_bytes(b"evil")
        lock = tmp_path / "watermarks.lock"
        os.symlink(str(target), str(lock))
        with pytest.raises(LockFileSymlinkAttack) as exc:
            safe_open_lock_file(lock)
        assert exc.value.reason == "o_nofollow_eloop"
        assert exc.value.code == "F-ISO-07"

    def test_safe_open_lock_file_rejects_swapped_inode_post_open(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """§7.15 — simulate TOCTOU where lstat returns a different inode."""
        lock = tmp_path / "swap.lock"
        real_lstat = os.lstat

        fake_stat = os.stat_result(
            (0o100600, 9999999, 1234, 1, os.getuid(), os.getgid(), 0, 0, 0, 0)
        )

        def poisoned_lstat(path):
            p = str(path)
            if p.endswith("swap.lock"):
                return fake_stat
            return real_lstat(path)

        monkeypatch.setattr(os, "lstat", poisoned_lstat)
        with pytest.raises(LockFileSymlinkAttack) as exc:
            safe_open_lock_file(lock)
        assert exc.value.reason == "post_open_inode_mismatch"

    def test_safe_open_lock_file_rejects_foreign_uid(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """§7.15 — simulate a lock file owned by a foreign uid."""
        lock = tmp_path / "foreign.lock"
        real_fstat = os.fstat
        real_lstat = os.lstat

        def poisoned_fstat(fd):
            st = real_fstat(fd)
            return os.stat_result(
                (
                    st.st_mode, st.st_ino, st.st_dev, st.st_nlink,
                    os.getuid() + 1000,  # foreign uid
                    st.st_gid, st.st_size, st.st_atime, st.st_mtime, st.st_ctime,
                )
            )

        def matched_lstat(path):
            st = real_lstat(path)
            return os.stat_result(
                (
                    st.st_mode, st.st_ino, st.st_dev, st.st_nlink,
                    os.getuid() + 1000,
                    st.st_gid, st.st_size, st.st_atime, st.st_mtime, st.st_ctime,
                )
            )

        monkeypatch.setattr(os, "fstat", poisoned_fstat)
        monkeypatch.setattr(os, "lstat", matched_lstat)
        with pytest.raises(PermissionError):
            safe_open_lock_file(lock)

    def test_no_create_when_flag_disabled(self, tmp_path: Path) -> None:
        lock = tmp_path / "ghost.lock"
        with pytest.raises(FileNotFoundError):
            safe_open_lock_file(lock, create_if_missing=False)


class TestConstants:
    def test_open_flags_include_nofollow(self) -> None:
        assert LOCK_FILE_OPEN_FLAGS & os.O_NOFOLLOW
        assert LOCK_FILE_OPEN_FLAGS & os.O_RDWR
        assert LOCK_FILE_OPEN_FLAGS & os.O_CREAT
