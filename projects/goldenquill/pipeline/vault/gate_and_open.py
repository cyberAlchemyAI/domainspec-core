"""M14.1 — atomic gate-and-open. [§4.1]

Section 2 Vault primitive. Every file open inside the Vault resolves path
components, symlinks, and magic links in a single kernel-atomic operation so
that no attacker can swap a path component between resolve and open.

Pre-gate validation (both platforms):
    * reject embedded ``\\x00`` (A-12 / F-GATE-05).
    * reject percent-encoded ``%00`` (C-03 v3 / F-GATE-09).
    * reject Unicode Cf/Cc/Co/Mn/Me codepoints (G-01 v4 / F-GATE-08).
    * reject paths not byte-identical to their NFC form (B-03 / F-GATE-07).
    * reject paths whose NFC and NFKC forms diverge (C-06 v3 / F-GATE-10).
    * reject ``/dev/fd/*`` / ``/dev/stdin|stdout|stderr`` (A-15 / F-GATE-06).
    * reject reserved or absolute canonical forms (``""``, ``.``, ``..``,
      leading ``/``) at the validator — downstream openers trust the
      canonical form. Applied uniformly on Linux + macOS.
    * reject depth > MAX_VAULT_RELATIVE_PATH_DEPTH (12).

Linux primary path: ``openat2(vault_root_fd, relative_path, how)`` with
``RESOLVE_NO_SYMLINKS | RESOLVE_NO_MAGICLINKS | RESOLVE_BENEATH``. ``ENOSYS``
(kernel < 5.6) is fail-closed — no legacy fallback (A-01).

macOS primary path: ancestor-chain ``openat`` walk with ``O_NOFOLLOW`` at each
step, pre-capture of each ancestor's ``(st_dev, st_ino)``, post-open re-stat of
every ancestor FD to detect mid-walk mount-over (A-02 / F-GATE-03).

Identity-tuple pinning: v0.1 exposes an optional ``identity_pinning`` dict
keyed by canonical relative path → ``(st_dev, st_ino)``. When supplied, the
final FD's ``fstat`` is compared and any drift raises
``F-GATE-02 GateIdentityTupleMismatch``. The full pinning table lives behind
the FD broker (Round S).
"""

from __future__ import annotations

import errno
import os
import platform
import unicodedata
from pathlib import Path
from typing import Final, Optional

from pipeline.vault.error_codes import (
    F_GATE_01,
    GateAncestorMountMismatch,
    GateDevFdRejected,
    GateIdentityTupleMismatch,
    GateNFCNFKCDivergence,
    GateOpenRejected,
    GatePathNullByte,
    GatePathUnicodeForbidden,
    GatePathUnicodeNonNormal,
    GatePercentNullRejected,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§4.1 M14.1 atomic gate-and-open — Linux openat2 + macOS openat-walk primary paths",
            "§4.1 pre-gate validation — NUL / %00 / Unicode Cf-Cc-Co-Mn-Me / NFC / NFC-NFKC divergence / /dev/fd / reserved components / depth cap",
            "§4.1 A-01 ENOSYS fail-closed (no legacy-fallback)",
            "§4.1 A-02 macOS ancestor-chain mount-over detection (F-GATE-03)",
            "§4.1 A-15 /dev/fd / /dev/std{in,out,err} reject (F-GATE-06)",
            "§6.2 F-GATE-01..F-GATE-10 raise sites",
            "§9 step 2a boot-time openat2 kernel-floor probe (F-GATE-01 openat2-unavailable on ENOSYS)",
        ],
    },
}


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_VAULT_RELATIVE_PATH_DEPTH: int = 12

_UNICODE_FORBIDDEN_CATEGORIES: frozenset[str] = frozenset(
    {"Cf", "Cc", "Co", "Mn", "Me"}
)

# Linux openat2 resolve flags. os.RESOLVE_* constants were added in 3.10;
# they are absent on macOS, so lookup is conditional.
_RESOLVE_NO_SYMLINKS = getattr(os, "RESOLVE_NO_SYMLINKS", 0x04)
_RESOLVE_NO_MAGICLINKS = getattr(os, "RESOLVE_NO_MAGICLINKS", 0x02)
_RESOLVE_BENEATH = getattr(os, "RESOLVE_BENEATH", 0x08)
RESOLVE_FLAGS: int = (
    _RESOLVE_NO_SYMLINKS | _RESOLVE_NO_MAGICLINKS | _RESOLVE_BENEATH
)

_DEV_FD_PREFIXES = ("/dev/fd/", "/dev/stdin", "/dev/stdout", "/dev/stderr")


# ---------------------------------------------------------------------------
# Pre-gate validator
# ---------------------------------------------------------------------------


def _validate_relative_path(relative_path: str) -> str:
    """Run every pre-gate check. Returns the NFC-canonical, normpath-ed path.

    Raises the appropriate Gate* exception on the first failure encountered.
    """
    if not isinstance(relative_path, str):
        raise TypeError(
            f"relative_path must be str, got {type(relative_path).__name__}"
        )
    if "\x00" in relative_path:
        raise GatePathNullByte(
            "path contains embedded null byte",
            path=relative_path,
            reason="path-contains-null",
        )
    if "%00" in relative_path.lower():
        raise GatePercentNullRejected(
            "path contains percent-encoded null (%00)",
            path=relative_path,
            reason="path-contains-percent-null",
        )
    for ch in relative_path:
        cat = unicodedata.category(ch)
        if cat in _UNICODE_FORBIDDEN_CATEGORIES:
            raise GatePathUnicodeForbidden(
                f"path contains forbidden Unicode category {cat}",
                path=relative_path,
                reason=f"path-unicode-forbidden-category-{cat}-{ord(ch):04x}",
            )
    if unicodedata.normalize("NFC", relative_path) != relative_path:
        raise GatePathUnicodeNonNormal(
            "path is not in NFC canonical form",
            path=relative_path,
            reason="path-unicode-nonnormal",
        )
    if unicodedata.normalize("NFC", relative_path) != unicodedata.normalize(
        "NFKC", relative_path
    ):
        raise GateNFCNFKCDivergence(
            "path NFC and NFKC forms diverge",
            path=relative_path,
            reason="path-nfc-nfkc-divergence",
        )
    canon = os.path.normpath(relative_path)
    if canon.startswith(_DEV_FD_PREFIXES):
        raise GateDevFdRejected(
            "path resolves to /dev/fd synthetic FD",
            path=relative_path,
            reason="dev-fd-synthetic",
        )
    # F-2 closure (Batch 2 carry-forward): reject reserved and absolute
    # canonical forms at the validator. os.path.normpath("") -> "." on Linux,
    # which would otherwise hand openat2(".") a bare vault-root FD (docstring
    # promises rejection; parts-filter previously dropped "" and "." before
    # the depth check ever saw them). Belt-and-braces: also reject absolute
    # canonical forms (including `/etc/passwd`) in case normpath preserves a
    # leading slash. /dev/fd branch above keeps its specific F_GATE_06 verdict
    # (more-specific-reject-wins).
    if canon in ("", ".") or canon.startswith("/"):
        raise GateOpenRejected(
            f"reserved or absolute path component {canon!r}",
            path=relative_path,
            reason="reserved-component",
        )
    # Depth cap — vault paths must not exceed MAX_VAULT_RELATIVE_PATH_DEPTH.
    parts = [p for p in canon.split("/") if p not in ("", ".")]
    if len(parts) > MAX_VAULT_RELATIVE_PATH_DEPTH:
        raise GateOpenRejected(
            f"path exceeds max depth {MAX_VAULT_RELATIVE_PATH_DEPTH}",
            path=relative_path,
            reason="path-too-deep",
        )
    if ".." in parts:
        raise GateOpenRejected(
            "path contains reserved `..` component",
            path=relative_path,
            reason="reserved-component",
        )
    return canon


# ---------------------------------------------------------------------------
# Linux path (openat2 via ctypes; v0.1 probe-based)
# ---------------------------------------------------------------------------


def _openat2_syscall(
    dirfd: int, path: str, flags: int, mode: int, resolve: int
) -> int:
    """Invoke ``openat2(2)`` via ctypes. Returns FD or -errno on error.

    A-01 closure: we probe syscall support and surface ENOSYS to the caller
    so the Vault boot path can fail closed on kernels < 5.6.
    """
    import ctypes
    import ctypes.util

    class OpenHow(ctypes.Structure):
        _fields_ = [
            ("flags", ctypes.c_uint64),
            ("mode", ctypes.c_uint64),
            ("resolve", ctypes.c_uint64),
        ]

    SYS_OPENAT2 = 437  # x86_64 / aarch64 agree on this number
    libc = ctypes.CDLL(ctypes.util.find_library("c") or "libc.so.6", use_errno=True)
    syscall = libc.syscall
    syscall.restype = ctypes.c_long
    how = OpenHow(flags=flags, mode=mode, resolve=resolve)
    ret = syscall(
        ctypes.c_long(SYS_OPENAT2),
        ctypes.c_int(dirfd),
        ctypes.c_char_p(path.encode("utf-8")),
        ctypes.byref(how),
        ctypes.c_size_t(ctypes.sizeof(OpenHow)),
    )
    if ret < 0:
        return -ctypes.get_errno()
    return int(ret)


def _gate_and_open_linux(
    vault_root_fd: int,
    relative_path: str,
    flags: int,
) -> int:
    fd_or_err = _openat2_syscall(
        vault_root_fd,
        relative_path,
        flags | os.O_CLOEXEC,
        0,
        RESOLVE_FLAGS,
    )
    if fd_or_err == -errno.ENOSYS:
        raise GateOpenRejected(
            "openat2 unavailable on this kernel (< 5.6); no fallback",
            path=relative_path,
            reason="openat2-unavailable",
            detail="Tilth v0.1 requires openat2 (A-01); upgrade kernel to >= 5.6.",
        )
    if fd_or_err == -errno.ELOOP:
        raise GateOpenRejected(
            "symlink component rejected (RESOLVE_NO_SYMLINKS)",
            path=relative_path,
            reason="symlink-in-path",
        )
    if fd_or_err == -errno.EXDEV:
        raise GateOpenRejected(
            "path escapes beneath (RESOLVE_BENEATH)",
            path=relative_path,
            reason="path-escape",
        )
    if fd_or_err < 0:
        raise GateOpenRejected(
            f"kernel refused open (errno {-fd_or_err})",
            path=relative_path,
            reason=f"errno-{-fd_or_err}",
        )
    return fd_or_err


def probe_openat2(vault_root_fd: int) -> bool:
    """Return True iff ``openat2`` is supported on the running kernel.

    Called by the Vault boot-step 2a gate. On non-Linux platforms returns
    False (openat2 is Linux-only).
    """
    if platform.system() != "Linux":
        return False
    fd_or_err = _openat2_syscall(
        vault_root_fd,
        ".",
        os.O_PATH | os.O_DIRECTORY,
        0,
        RESOLVE_FLAGS,
    )
    if fd_or_err == -errno.ENOSYS:
        return False
    if fd_or_err >= 0:
        os.close(fd_or_err)
        return True
    # Other errors still indicate openat2 is wired up.
    return True


# ---------------------------------------------------------------------------
# macOS path (ancestor-chain openat + O_NOFOLLOW + post-open re-stat)
# ---------------------------------------------------------------------------


def _close_all(fds: list[int]) -> None:
    for fd in fds:
        try:
            os.close(fd)
        except OSError:
            pass


def _gate_and_open_darwin(
    vault_root_fd: int,
    relative_path: str,
    flags: int,
) -> int:
    parts = [p for p in relative_path.split("/") if p]
    if not parts:
        raise GateOpenRejected(
            "empty relative path",
            path=relative_path,
            reason="empty-path",
        )
    ancestor_fds: list[int] = []
    ancestor_tuples_pre: list[tuple[int, int]] = []
    try:
        for name in parts[:-1]:
            if name in (".", ".."):
                raise GateOpenRejected(
                    f"reserved path component {name!r}",
                    path=relative_path,
                    reason="reserved-component",
                )
            parent_fd = ancestor_fds[-1] if ancestor_fds else vault_root_fd
            next_fd = os.open(
                name,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_DIRECTORY,
                dir_fd=parent_fd,
            )
            pre_stat = os.fstat(next_fd)
            ancestor_tuples_pre.append((pre_stat.st_dev, pre_stat.st_ino))
            ancestor_fds.append(next_fd)
        leaf = parts[-1]
        if leaf in (".", ".."):
            raise GateOpenRejected(
                f"reserved leaf component {leaf!r}",
                path=relative_path,
                reason="reserved-component",
            )
        parent_fd = ancestor_fds[-1] if ancestor_fds else vault_root_fd
        fd = os.open(
            leaf,
            flags | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=parent_fd,
        )
        # A-02: post-open re-stat of every ancestor FD.
        for idx, (pre_dev, pre_ino) in enumerate(ancestor_tuples_pre):
            post_stat = os.fstat(ancestor_fds[idx])
            if (post_stat.st_dev, post_stat.st_ino) != (pre_dev, pre_ino):
                os.close(fd)
                raise GateAncestorMountMismatch(
                    f"ancestor[{idx}] drift during walk",
                    path=relative_path,
                    reason="ancestor-mount-over",
                    detail=(
                        f"{pre_dev}:{pre_ino} -> "
                        f"{post_stat.st_dev}:{post_stat.st_ino}"
                    ),
                )
        return fd
    except OSError as exc:
        reason = "errno-" + (
            errno.errorcode.get(exc.errno, str(exc.errno)) if exc.errno else "unknown"
        )
        if exc.errno == errno.ELOOP:
            raise GateOpenRejected(
                "symlink component refused by O_NOFOLLOW",
                path=relative_path,
                reason="symlink-in-path",
            ) from exc
        raise GateOpenRejected(
            f"kernel refused open ({exc.strerror})",
            path=relative_path,
            reason=reason,
        ) from exc
    finally:
        _close_all(ancestor_fds)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def gate_and_open(
    vault_root_fd: int,
    relative_path: str,
    flags: int,
    *,
    identity_pinning: Optional[dict[str, tuple[int, int]]] = None,
) -> int:
    """Open ``relative_path`` beneath ``vault_root_fd`` fail-closed.

    :param vault_root_fd: FD obtained by the Vault boot after mount-namespace
        entry. All resolution is rooted here.
    :param relative_path: vault-relative path; absolute paths and ``..`` are
        rejected.
    :param flags: open flags (``os.O_RDONLY`` / ``O_WRONLY`` / ``O_RDWR`` /
        etc.); ``O_CLOEXEC`` is forced in the kernel call.
    :param identity_pinning: optional ``{canonical_path: (st_dev, st_ino)}``.
        When supplied, the final FD's fstat is compared against the pinning;
        any drift raises :class:`GateIdentityTupleMismatch`.
    :returns: an open FD. The caller owns the FD and must close it.
    :raises GateOpenRejected: F-GATE-01 kernel refusal / reserved-component.
    :raises GateIdentityTupleMismatch: F-GATE-02 pinning drift.
    :raises GateAncestorMountMismatch: F-GATE-03 macOS mount-over mid-walk.
    :raises GatePathNullByte: F-GATE-05 embedded null.
    :raises GateDevFdRejected: F-GATE-06 /dev/fd rejection.
    :raises GatePathUnicodeNonNormal: F-GATE-07 non-NFC path.
    :raises GatePathUnicodeForbidden: F-GATE-08 Cf/Cc/Co/Mn/Me codepoint.
    :raises GatePercentNullRejected: F-GATE-09 %00.
    :raises GateNFCNFKCDivergence: F-GATE-10 NFC/NFKC divergence.
    """
    if not isinstance(vault_root_fd, int):
        raise TypeError(
            f"vault_root_fd must be int, got {type(vault_root_fd).__name__}"
        )
    if not isinstance(flags, int):
        raise TypeError(f"flags must be int, got {type(flags).__name__}")

    canon = _validate_relative_path(relative_path)

    system = platform.system()
    if system == "Darwin":
        fd = _gate_and_open_darwin(vault_root_fd, canon, flags)
    elif system == "Linux":
        fd = _gate_and_open_linux(vault_root_fd, canon, flags)
    else:
        raise GateOpenRejected(
            f"platform {system!r} unsupported",
            path=relative_path,
            reason="platform-unsupported",
        )

    if identity_pinning is not None:
        expected = identity_pinning.get(canon)
        if expected is not None:
            st = os.fstat(fd)
            if (st.st_dev, st.st_ino) != expected:
                os.close(fd)
                raise GateIdentityTupleMismatch(
                    "post-open identity tuple drift",
                    path=relative_path,
                    reason="identity-tuple-drift",
                    detail=(
                        f"pinned={expected}, actual={(st.st_dev, st.st_ino)}"
                    ),
                )
    return fd


def open_vault_root(root: Path) -> int:
    """Open a Vault-root directory FD with ``O_NOFOLLOW | O_CLOEXEC``.

    Callers are responsible for closing the returned FD at shutdown.

    F-1 closure (Batch 2 carry-forward): kernel refusals (ELOOP on symlink
    roots, EACCES, ENOENT, etc.) are translated to
    :class:`GateOpenRejected` so the Vault surface exception contract is
    uniform. Fail-closed IS preserved either way; this wrap replaces the
    raw-OSError leak with a structured gate reason.
    """
    if not isinstance(root, Path):
        raise TypeError(f"root must be pathlib.Path, got {type(root).__name__}")
    # Platform-agnostic symlink-root reject: Linux returns ELOOP for
    # O_NOFOLLOW|O_DIRECTORY on a dir-symlink; macOS returns ENOTDIR. The
    # lstat-based islink check is uniform and fires before kernel errno
    # divergence matters.
    if root.is_symlink():
        raise GateOpenRejected(
            "vault root is a symlink (refused by O_NOFOLLOW)",
            path=str(root),
            reason="root-is-symlink",
        )
    if not root.is_dir():
        raise GateOpenRejected(
            f"vault root {root} is not a directory",
            path=str(root),
            reason="root-not-directory",
        )
    try:
        return os.open(
            str(root),
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_DIRECTORY,
        )
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            raise GateOpenRejected(
                "vault root is a symlink (refused by O_NOFOLLOW)",
                path=str(root),
                reason="root-is-symlink",
            ) from exc
        code = (
            errno.errorcode.get(exc.errno, str(exc.errno))
            if exc.errno
            else "unknown"
        )
        raise GateOpenRejected(
            f"kernel refused vault-root open ({exc.strerror})",
            path=str(root),
            reason=f"errno-{code}",
        ) from exc


__all__ = [
    "MAX_VAULT_RELATIVE_PATH_DEPTH",
    "RESOLVE_FLAGS",
    "gate_and_open",
    "open_vault_root",
    "probe_openat2",
]
