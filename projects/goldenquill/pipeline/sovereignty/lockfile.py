"""Anti-symlink safe open for fcntl lock files. [§3.11c, §6.7 F-ISO-07, v5 RT-v4 MED-1]

Every ``*.lock`` file in ``pipeline/sovereignty/`` MUST be opened through
:func:`safe_open_lock_file`. Direct ``os.open`` on a lock path is an
audit-time regression.

Guard discipline:

1. ``os.open`` with ``O_RDWR | O_CREAT | O_NOFOLLOW`` — if the path is a
   symlink, the kernel returns ``ELOOP`` and we raise
   :class:`LockFileSymlinkAttack(reason="o_nofollow_eloop")`.
2. Post-open ``fstat(fd).st_dev/st_ino`` ``==`` ``lstat(path).st_dev/st_ino``
   — catches a TOCTOU where an attacker deletes the real lock file and
   replaces it with a symlink between the ``O_NOFOLLOW``-safe ``open`` and
   the caller's first ``flock``.
3. Post-open ``fstat(fd).st_uid`` ``==`` ``os.getuid()`` — belt-and-suspenders
   against directory-permission misconfig on shared-uid deployments.

Blueprint refs: §3.11c (this helper), §6.7 F-ISO-07, §8 constants
``LOCK_FILE_OPEN_FLAGS`` / ``LOCK_FILE_POST_OPEN_INODE_CHECK`` /
``LOCK_FILE_POST_OPEN_UID_CHECK``.
"""

from __future__ import annotations

import errno
import os
from pathlib import Path

__all__ = [
    "LOCK_FILE_OPEN_FLAGS",
    "LOCK_FILE_POST_OPEN_INODE_CHECK",
    "LOCK_FILE_POST_OPEN_UID_CHECK",
    "LockFileSymlinkAttack",
    "safe_open_lock_file",
]

LOCK_FILE_OPEN_FLAGS: int = os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW
LOCK_FILE_POST_OPEN_INODE_CHECK: bool = True
LOCK_FILE_POST_OPEN_UID_CHECK: bool = True


class LockFileSymlinkAttack(OSError):
    """F-ISO-07 symlink or inode-swap on a ``*.lock`` path. [§6.7]"""

    code: str = "F-ISO-07"

    def __init__(self, *, reason: str, path: Path, extra: str | None = None) -> None:
        msg = f"F-ISO-07 safe_open_lock_file rejected {path}: {reason}"
        if extra:
            msg = f"{msg} ({extra})"
        super().__init__(msg)
        self.reason = reason
        self.path = path


def safe_open_lock_file(lock_path: Path, *, create_if_missing: bool = True) -> int:
    """Open a fcntl lock file under anti-symlink guards. [§3.11c]

    Returns an open file descriptor. Caller owns the fd and MUST close it
    (typically via ``os.close(fd)`` after ``fcntl.LOCK_UN``).

    :raises TypeError: E-001 — ``lock_path`` not ``pathlib.Path``.
    :raises LockFileSymlinkAttack: symlink trap triggered by O_NOFOLLOW,
        inode mismatch caught post-open, or uid mismatch caught post-open.
    :raises FileNotFoundError: only if ``create_if_missing=False`` and the
        file does not exist.
    :raises PermissionError: ``os.fstat`` shows a foreign uid owner.
    """
    if not isinstance(lock_path, Path):
        raise TypeError("lock_path must be pathlib.Path")

    flags = LOCK_FILE_OPEN_FLAGS
    if not create_if_missing:
        flags &= ~os.O_CREAT

    try:
        fd = os.open(str(lock_path), flags, 0o600)
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            raise LockFileSymlinkAttack(
                reason="o_nofollow_eloop",
                path=lock_path,
                extra=f"O_NOFOLLOW triggered ELOOP: {exc}",
            ) from exc
        raise

    # Post-open inode check.
    try:
        fd_stat = os.fstat(fd)
        try:
            path_stat = os.lstat(str(lock_path))
        except FileNotFoundError as exc:
            raise LockFileSymlinkAttack(
                reason="post_open_path_gone",
                path=lock_path,
                extra=f"lstat after open failed: {exc}",
            ) from exc
        if LOCK_FILE_POST_OPEN_INODE_CHECK and (
            fd_stat.st_dev != path_stat.st_dev or fd_stat.st_ino != path_stat.st_ino
        ):
            raise LockFileSymlinkAttack(
                reason="post_open_inode_mismatch",
                path=lock_path,
                extra=(
                    f"fstat(fd)=({fd_stat.st_dev},{fd_stat.st_ino}) "
                    f"lstat(path)=({path_stat.st_dev},{path_stat.st_ino})"
                ),
            )
        if LOCK_FILE_POST_OPEN_UID_CHECK and fd_stat.st_uid != os.getuid():
            raise PermissionError(
                f"F-ISO-07 lock file {lock_path} owned by uid {fd_stat.st_uid}, "
                f"expected {os.getuid()}"
            )
    except BaseException:
        os.close(fd)
        raise

    return fd
