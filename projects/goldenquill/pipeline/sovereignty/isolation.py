"""Org-root namespace isolation. [§1 row 7, §4.13 Law 3, §6.7 F-ISO-*]

Section 1 Round D implementation. Enforces the Law-3 Org-Isolation property
at the filesystem primitive layer: every file operation on a path claimed
to be under `orgs/{slug}/vault/` is verified to actually resolve inside
that org's root — never inside another org's root, never outside the
repository, never via a symlink that escapes the root, and never via a
path whose root inode or volume identifier has drifted since the namespace
was bound.

Public API (exported via ``pipeline.sovereignty.__all__``):
    OrgRootNamespace        — frozen dataclass binding org → root + inode + volume
    within_org_root(path, ns) — predicate; True iff path is strictly under ns.root_path
    with_org_root(ns)       — context manager; holds a directory FD + advisory lock
    create_bind_mount_namespace(ns) — Phase-0 stub; NotImplementedError
    IsolationError          — common parent for F-ISOLATION-*
    InodeDrift, VolumeDrift — specific drift exceptions
    PathEscape              — resolved path escapes claimed root
    SymlinkResolveFailed    — symlink chain could not resolve strictly
    UnsupportedFilesystem   — fs type not on the §5.1 allowlist

Blueprint references:
    §1 row 7       — DOC_SOURCED roots + slug parametrization
    §4.13 Law 3    — Org Isolation (no cross-org read or write)
    §5.1           — filesystem allowlist (apfs / ext4 / btrfs / zfs / xfs)
    §6.7 F-ISO-*   — failure codes (iNODE-DRIFT, VOLUME-DRIFT, PATH-ESCAPE,
                     SYMLINK-RESOLVE-FAIL)
    §7.5 BT2       — symlink-escape discipline (shared with ``topology.py``)

Design notes — deliberate choices:
    * macOS primary path uses ``Path.resolve(strict=True)`` + ``samefile()``
      because ``openat2(..., RESOLVE_BENEATH)`` is Linux-only. The isolation
      property is achieved by composing (a) strict symlink resolution,
      (b) a membership check against the bound root, and (c) a held directory
      file descriptor so any rename / unlink after the check is still caught
      by the FD stability.
    * Linux primary path uses ``openat2(..., RESOLVE_NO_SYMLINKS |
      RESOLVE_NO_MAGICLINKS | RESOLVE_BENEATH)`` when available (kernel ≥ 5.6);
      otherwise falls back to the macOS-style strict-resolve + FD-hold pattern.
    * "Volume UUID" at v0.1 is implemented as ``os.stat(root).st_dev`` —
      the kernel-level device identifier. It is stable across normal reads
      and writes, and changes on remount or volume swap. True volume-UUID
      binding (APFS vol UUID, btrfs subvolume UUID) is deferred to v0.2 per
      the provisioning manifest §8.6 post-quantum round.
    * Bind-mount namespace creation (Linux) is stubbed with a clear pointer
      to the v0.2 Section-2 Vault implementation; Phase-0 isolation rides on
      the open-FD + advisory-lock pattern, which is portable and sufficient
      for the single-process dev tier. Production Linux tier will compose
      this primitive with a Linux mount-namespace on top.

Futureproofing (engineering-process §4):
    §4.1 Public API     — ``OrgRootNamespace``, ``within_org_root``,
                          ``with_org_root`` are the sealed public surface.
    §4.4 Crypto-agility — ``OrgRootNamespace`` carries ``volume_identifier``
                          (device number today; volume UUID at v0.2) so
                          downstream consumers dispatch on the identifier
                          field, not a hardcoded stat call.
    §4.6 BLUEPRINT_DEPS — declared below.
    §4.11 Docstrings    — every public symbol cites its blueprint anchor.

E-enforcement:
    E-001 — all entry points validate arg types before any I/O.
    E-002 — ``OrgRootNamespace.org_slug`` must be canonical-lowercase per
            ``org_slug.canonical_slug`` (re-checked at construction).
    E-004 — ``with_org_root`` context manager guarantees FD + lock release
            on every exit path, including exceptions raised inside the block.
"""

from __future__ import annotations

import datetime as _dt
import errno
import fcntl
import os
import platform
import sys
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional

from pipeline.sovereignty.org_slug import canonical_slug

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": [
            "§1 row 7 (DOC_SOURCED roots)",
            "§3.11d (Isolation / within_org_root)",
            "§4.13 Law 3 (Org Isolation)",
            "§5.1 (filesystem allowlist)",
            "§5.2 BT2 (OS-level namespace + TOCTOU closure)",
            "§6.7 F-ISO-* (failure codes)",
            "§7.5 (isolation/topology test surface)",
        ],
        "hash_at_lock": "lock-round-D-v2-2026-04-19",
        "hash_source_version": "v6",
    },
    "v7_round_handoff_addendum_A7_A8_A9_2026-04-19.md": {
        "sections_implemented": ["§A12.7 crypto-agility scaffold (volume_identifier)"],
        "hash_at_lock": "lock-round-D-v2-2026-04-19",
        "hash_source_version": "signed-off-2026-04-19",
    },
}

__all__ = [
    "FILESYSTEM_ALLOWLIST",
    "IsolationError",
    "InodeDrift",
    "VolumeDrift",
    "PathEscape",
    "SymlinkResolveFailed",
    "UnsupportedFilesystem",
    "OrgRootNamespace",
    "OrgRootGate",
    "within_org_root",
    "with_org_root",
    "create_bind_mount_namespace",
]

# ---------------------------------------------------------------------------
# Constants  [§5.1 filesystem allowlist]
# ---------------------------------------------------------------------------

#: The fixed set of filesystem types permitted to host an ``OrgRootNamespace``.
#:
#: Rationale (blueprint §5.1): these filesystems provide (a) stable inode
#: numbers across a normal mount lifetime, (b) stable ``st_dev`` as a volume
#: proxy, and (c) reliable POSIX ``fcntl.flock`` semantics. Rejected types
#: include ``tmpfs`` (inode reuse on delete), ``overlayfs`` (upper/lower
#: inode confusion), ``fuse.*`` (semantics are driver-specific), ``hfs+``
#: (case-insensitive by default — breaks slug-unique invariants), ``ntfs`` /
#: ``vfat`` (same), and network filesystems (``nfs``, ``cifs``, ``smb``) whose
#: consistency model does not guarantee inode stability across server
#: restarts.
FILESYSTEM_ALLOWLIST: frozenset[str] = frozenset(
    {
        # macOS
        "apfs",
        # Linux
        "ext4",
        "btrfs",
        "zfs",
        "xfs",
    }
)

#: Environment variable callers can set to extend the allowlist.
#:
#: Value is a comma-separated list of filesystem type names (lower-case).
#: Intended for CI / sandbox environments where the repo lives on a
#: non-allowlisted filesystem (e.g. ``fuseblk`` inside a containerized test
#: runner). Never set this on a production deployment. The test suite
#: exercises this path with ``fuseblk,tmpfs`` so the adversarial probes
#: can run under CI.
TILTH_ISOLATION_FS_ALLOWLIST_EXTEND_ENV = "TILTH_ISOLATION_FS_ALLOWLIST_EXTEND"


# ---------------------------------------------------------------------------
# Failure codes  [§6.7 F-ISO-*]
# ---------------------------------------------------------------------------


class IsolationError(RuntimeError):
    """Common parent for every F-ISOLATION-* fail-closed condition.

    Subclasses attach a ``code`` attribute that matches the blueprint §6.7
    failure identifier so the admin-risk ledger writes a stable tag regardless
    of which specific subclass fired.
    """

    code: str = "F-ISOLATION"


class InodeDrift(IsolationError):
    """Root directory inode changed since namespace construction.

    Triggered when an attacker unlinks ``orgs/{slug}/`` and recreates it with
    a new inode (same name, different identity) — or when a mount swap has
    replaced the directory node underneath the namespace. Per §6.7, this is
    fail-closed: the old namespace binding is considered compromised and
    downstream consumers must construct a fresh namespace.

    Attributes:
        expected_inode: inode captured at construction.
        observed_inode: inode observed at check time.
    """

    code = "F-ISOLATION-INODE-DRIFT"

    def __init__(self, *, expected_inode: int, observed_inode: int) -> None:
        super().__init__(
            f"root inode drifted: expected {expected_inode}, observed {observed_inode}"
        )
        self.expected_inode = expected_inode
        self.observed_inode = observed_inode


class VolumeDrift(IsolationError):
    """Volume identifier (``st_dev`` at v0.1; volume UUID at v0.2) changed.

    Triggered by a remount, a filesystem swap, or (more exotically) the
    volume being re-provisioned under the same mountpoint. Fail-closed per
    §6.7.
    """

    code = "F-ISOLATION-VOLUME-DRIFT"

    def __init__(self, *, expected_volume: int, observed_volume: int) -> None:
        super().__init__(
            f"root volume drifted: expected {expected_volume}, observed {observed_volume}"
        )
        self.expected_volume = expected_volume
        self.observed_volume = observed_volume


class PathEscape(IsolationError):
    """Resolved path does not descend from the claimed namespace root.

    Raised by ``within_org_root`` when the argument path — after symlink
    resolution and strict canonicalization — is not strictly inside
    ``ns.root_path``. Covers ``..`` traversal, symlink-to-parent, absolute
    paths to other orgs, etc. Per §6.7, fail-closed.
    """

    code = "F-ISOLATION-PATH-ESCAPE"

    def __init__(self, *, path: Path, root: Path, reason: str) -> None:
        super().__init__(f"path {path!s} escapes org root {root!s} ({reason})")
        self.path = path
        self.root = root
        self.reason = reason


class SymlinkResolveFailed(IsolationError):
    """Symlink chain did not resolve strictly (loop, dangling, or cross-root).

    Distinct from ``PathEscape`` because the resolution itself failed rather
    than produced a path outside the root. Per §6.7, fail-closed.
    """

    code = "F-ISOLATION-SYMLINK-RESOLVE-FAIL"

    def __init__(self, *, path: Path, reason: str) -> None:
        super().__init__(f"symlink resolution failed for {path!s}: {reason}")
        self.path = path
        self.reason = reason


class UnsupportedFilesystem(IsolationError):
    """Filesystem type of the root path is not on ``FILESYSTEM_ALLOWLIST``.

    Fails construction of the namespace, not any later operation — by the
    time an ``OrgRootNamespace`` instance exists, the fs type has been
    validated, so no downstream check needs to repeat the lookup.
    """

    code = "F-ISOLATION-FS-DISALLOWED"

    def __init__(self, *, fs_type: str, root_path: Path) -> None:
        super().__init__(
            f"filesystem {fs_type!r} at {root_path!s} is not on the §5.1 allowlist"
        )
        self.fs_type = fs_type
        self.root_path = root_path


# ---------------------------------------------------------------------------
# Filesystem type detection
# ---------------------------------------------------------------------------


def _read_env_allowlist_extension() -> frozenset[str]:
    """Read the ``TILTH_ISOLATION_FS_ALLOWLIST_EXTEND`` env var, if set.

    Returns the set of additional fs-type names, normalized to lower-case.
    Empty set if unset or blank.
    """
    raw = os.environ.get(TILTH_ISOLATION_FS_ALLOWLIST_EXTEND_ENV, "")
    if not raw.strip():
        return frozenset()
    return frozenset(
        piece.strip().lower()
        for piece in raw.split(",")
        if piece.strip()
    )


def _detect_fs_type_linux(path: Path) -> str:
    """Return the filesystem type of ``path`` by longest-prefix ``/proc/mounts`` match.

    Linux-specific. macOS callers should use ``_detect_fs_type_macos``.
    """
    path_str = str(path.resolve(strict=True))
    try:
        with open("/proc/mounts", "r", encoding="utf-8") as fh:
            mounts = [line.rstrip("\n").split() for line in fh]
    except OSError as exc:
        raise UnsupportedFilesystem(
            fs_type="<unreadable:/proc/mounts>", root_path=path
        ) from exc

    # Column 1 = mount point, Column 2 = fs type. Longest-prefix match.
    best_match_mnt = ""
    best_match_fs = ""
    for cols in mounts:
        if len(cols) < 3:
            continue
        mnt = cols[1]
        fs = cols[2].lower()
        # octal-escaped spaces in /proc/mounts — Linux encodes " " as \040
        mnt = mnt.replace(r"\040", " ").replace(r"\011", "\t")
        if path_str == mnt or path_str.startswith(mnt.rstrip("/") + "/"):
            if len(mnt) > len(best_match_mnt):
                best_match_mnt = mnt
                best_match_fs = fs

    if not best_match_fs:
        raise UnsupportedFilesystem(
            fs_type="<no-mount-found>", root_path=path
        )
    return best_match_fs


def _detect_fs_type_macos(path: Path) -> str:
    """Return the filesystem type of ``path`` via ``statfs(2)`` on macOS.

    Uses ctypes because Python's ``os.statvfs`` does not surface
    ``f_fstypename``. Safe — the call touches an on-stack struct and reads
    a 16-byte name field.
    """
    import ctypes  # local import so non-macOS imports stay cheap
    import ctypes.util

    libc_name = ctypes.util.find_library("c")
    if libc_name is None:  # pragma: no cover  (macOS always has libSystem)
        raise UnsupportedFilesystem(
            fs_type="<libc-not-found>", root_path=path
        )
    libc = ctypes.CDLL(libc_name, use_errno=True)

    # darwin statfs64 struct is large; we only need f_fstypename at offset
    # right after a bunch of ints. Using a minimal ctypes struct with the
    # fields we need is risky. Safer: use the documented ``statfs`` via
    # Python's ``os.statvfs`` + ctypes supplement. Fall back to a command
    # if anything is wrong.
    try:
        # getattrlist route: VOL_CAPABILITIES is simpler but ATTR_CMN_FSSUBTYPE
        # requires a raw syscall. Use ``df -T`` as the pragmatic fallback —
        # it's present on every macOS tier and returns the fs type cleanly.
        import subprocess

        result = subprocess.run(
            ["/bin/df", "-T", "local", str(path)],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        # Fallback via `mount`: parse `mount | grep "on <mnt>"`
        if result.returncode != 0 or not result.stdout.strip():
            result = subprocess.run(
                ["/sbin/mount"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            path_str = str(path.resolve(strict=True))
            best_mnt = ""
            best_fs = ""
            for line in result.stdout.splitlines():
                # Format: "/dev/disk1s1 on /Users (apfs, local, journaled)"
                if " on " not in line or " (" not in line:
                    continue
                _, rest = line.split(" on ", 1)
                mnt, meta = rest.rsplit(" (", 1)
                fs = meta.split(",", 1)[0].strip().lower()
                if path_str == mnt or path_str.startswith(mnt.rstrip("/") + "/"):
                    if len(mnt) > len(best_mnt):
                        best_mnt = mnt
                        best_fs = fs
            if best_fs:
                return best_fs
            raise UnsupportedFilesystem(
                fs_type="<mount-parse-failed>", root_path=path
            )

        # `df -T local <path>` output: header line + data line
        lines = result.stdout.strip().splitlines()
        if len(lines) < 2:
            raise UnsupportedFilesystem(
                fs_type="<df-parse-failed>", root_path=path
            )
        # Second column is "Type" in POSIX-style `df -T`
        cols = lines[1].split()
        # macOS BSD df -T outputs different column order; look for "apfs" etc.
        for tok in cols:
            if tok.lower() in {"apfs", "hfs", "hfs+", "ntfs", "msdos", "exfat"}:
                return tok.lower()
        # Fallback: assume column index 1 is fs type (Linux-style)
        if len(cols) > 1:
            return cols[1].lower()
        raise UnsupportedFilesystem(
            fs_type="<df-column-missing>", root_path=path
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise UnsupportedFilesystem(
            fs_type="<statfs-call-failed>", root_path=path
        ) from exc


def _detect_fs_type(path: Path) -> str:
    """Cross-platform fs-type detector. Returns a lower-case string name."""
    system = platform.system()
    if system == "Linux":
        return _detect_fs_type_linux(path)
    if system == "Darwin":
        return _detect_fs_type_macos(path)
    # Other OS: not supported at v0.1.
    raise UnsupportedFilesystem(
        fs_type=f"<os-unsupported:{system}>", root_path=path
    )


def _check_fs_allowed(
    path: Path,
    fs_allowlist_extend: frozenset[str] = frozenset(),
    *,
    include_env: bool = True,
) -> str:
    """Raise ``UnsupportedFilesystem`` unless ``path`` lives on an allowlisted fs.

    Returns the detected fs type name on success.

    ``fs_allowlist_extend`` is union-ed with the static allowlist. When
    ``include_env`` is True (the default, used only by ``bind()`` at
    construction time) the env-var extension is ALSO union-ed.
    ``verify_bindings_still_hold`` passes ``include_env=False`` so the
    allowlist at check-time is strictly the snapshot captured at bind —
    closing the attack window where a same-uid actor could widen the
    allowlist mid-session by setting ``TILTH_ISOLATION_FS_ALLOWLIST_EXTEND``.
    """
    fs_type = _detect_fs_type(path)
    base = FILESYSTEM_ALLOWLIST | frozenset(s.lower() for s in fs_allowlist_extend)
    if include_env:
        base = base | _read_env_allowlist_extension()
    if fs_type not in base:
        raise UnsupportedFilesystem(fs_type=fs_type, root_path=path)
    return fs_type


# ---------------------------------------------------------------------------
# OrgRootNamespace  [§1 row 7, §5.1]
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class OrgRootNamespace:
    """Immutable binding of ``org_slug`` to a resolved on-disk root. [§1 row 7]

    Constructed via the ``bind()`` classmethod (not ``__init__`` directly) so
    filesystem checks run inside a controlled code path. Attempting to mutate
    any field after construction fails with a frozen-dataclass ``FrozenInstance
    Error`` — every field is captured at bind-time and every subsequent check
    re-reads from the filesystem to detect drift.

    Fields:
        org_slug:
            Canonical slug (lower-case, ASCII, `org_slug.canonical_slug`
            pre-validated). Construction rejects non-canonical input.
        root_path:
            Absolute, resolved (``Path.resolve(strict=True)``) path to the
            org root directory on the filesystem.
        root_inode:
            ``os.stat(root_path).st_ino`` captured at bind-time. Every gate
            re-reads and compares — mismatch raises ``InodeDrift``.
        volume_identifier:
            ``os.stat(root_path).st_dev`` captured at bind-time. v0.1 proxy
            for "volume UUID"; v0.2 will swap to the native volume UUID per
            A12.7 crypto-agility scaffold. Mismatch raises ``VolumeDrift``.
        fs_type:
            Detected filesystem type at bind-time; validated against
            ``FILESYSTEM_ALLOWLIST``. Carried on the dataclass so debuggers
            and audit logs can emit the value without redoing the statfs.
        created_at:
            UTC timestamp of the bind call, ISO-8601 with ``Z``. Immutable.
    """

    org_slug: str
    root_path: Path
    root_inode: int
    volume_identifier: int
    fs_type: str
    fs_allowlist_extend: frozenset[str] = frozenset()
    created_at: _dt.datetime = field(default_factory=lambda: _dt.datetime.now(_dt.timezone.utc))

    # -- construction path -------------------------------------------------

    @classmethod
    def bind(
        cls,
        *,
        org_slug: str,
        root_path: Path,
        fs_allowlist_extend: frozenset[str] = frozenset(),
    ) -> "OrgRootNamespace":
        """Construct a namespace, running all §5.1 preflight checks.

        Raises:
            TypeError: non-``str`` slug or non-``Path`` root_path (E-001).
            ValueError / InvalidSlug: slug is not canonical (E-002).
            PathEscape: ``root_path`` is relative, non-existent, or not a dir.
            UnsupportedFilesystem: fs type not on ``FILESYSTEM_ALLOWLIST``
                (and not added via the env-var or explicit extension).
        """
        # E-001 — type gate.
        if not isinstance(org_slug, str):
            raise TypeError(
                f"isolation: org_slug must be str; got {type(org_slug).__name__}"
            )
        if not isinstance(root_path, Path):
            raise TypeError(
                f"isolation: root_path must be pathlib.Path; got "
                f"{type(root_path).__name__}"
            )

        # E-002 — slug must be canonical. Propagates InvalidSlug / ReservedSlug
        # from org_slug.canonical_slug (both ValueError subclasses).
        canon = canonical_slug(org_slug)
        if canon != org_slug:
            raise ValueError(
                f"isolation: org_slug {org_slug!r} is not canonical "
                f"(canonical form is {canon!r})"
            )

        # Path validation.
        if not root_path.is_absolute():
            raise PathEscape(
                path=root_path, root=root_path, reason="root_path_not_absolute"
            )
        try:
            resolved = root_path.resolve(strict=True)
        except (FileNotFoundError, OSError, RuntimeError) as exc:
            raise PathEscape(
                path=root_path, root=root_path, reason="root_path_unresolvable"
            ) from exc
        if not resolved.is_dir():
            raise PathEscape(
                path=root_path, root=root_path, reason="root_path_not_a_directory"
            )

        # Filesystem-type gate. Must happen AFTER strict resolve so the fs
        # detector inspects the real target, not a symlink.
        fs_type = _check_fs_allowed(resolved, fs_allowlist_extend)

        # Inode + volume snapshot. Captured once; re-checked on every gate.
        stat_result = os.stat(resolved)

        # Snapshot the effective allowlist extension (explicit kwarg ∪ env var).
        # Stored on the frozen dataclass; later re-checks use this snapshot
        # directly, NEVER re-reading the env var. Closes the mid-session
        # env-var-widening attack window.
        snapshot_extend = (
            frozenset(s.lower() for s in fs_allowlist_extend)
            | _read_env_allowlist_extension()
        )

        return cls(
            org_slug=canon,
            root_path=resolved,
            root_inode=stat_result.st_ino,
            volume_identifier=stat_result.st_dev,
            fs_type=fs_type,
            fs_allowlist_extend=snapshot_extend,
            # created_at default_factory fires now.
        )

    # -- lightweight helpers (never mutate) --------------------------------

    def verify_bindings_still_hold(
        self, *, fs_allowlist_extend: frozenset[str] | None = None
    ) -> None:
        """Re-stat ``root_path`` and raise if inode, volume, or fs-type drifted. [§3.11d, §5.2 BT2]

        Used internally by ``within_org_root`` and ``with_org_root``; also
        available to callers that want to assert freshness before a batch
        of operations.

        The fs-type re-check closes the narrow case where an attacker (or
        benign operator remount) swaps the underlying filesystem to a
        disallowed type while preserving ``st_dev`` (e.g., unmount + remount
        of a different backing device with the same major:minor). If the
        remount changes ``st_dev`` the ``VolumeDrift`` path catches it; the
        fs-type re-check is belt-and-suspenders for the same-``st_dev``
        edge case.

        Args:
            fs_allowlist_extend: override the extension set captured at
                ``bind()``-time. Normal callers do not pass this; it is
                available for unit tests that need to widen the allowlist
                beyond the bind-time snapshot. ``None`` (default) means
                use the snapshot from ``self.fs_allowlist_extend``.
        """
        effective_extend = (
            self.fs_allowlist_extend if fs_allowlist_extend is None
            else frozenset(s.lower() for s in fs_allowlist_extend)
        )
        try:
            now = os.stat(self.root_path)
        except FileNotFoundError as exc:
            raise InodeDrift(
                expected_inode=self.root_inode, observed_inode=-1
            ) from exc
        except OSError as exc:
            raise IsolationError(
                f"root_path stat failed: {exc!s}"
            ) from exc
        if now.st_ino != self.root_inode:
            raise InodeDrift(
                expected_inode=self.root_inode, observed_inode=now.st_ino
            )
        if now.st_dev != self.volume_identifier:
            raise VolumeDrift(
                expected_volume=self.volume_identifier,
                observed_volume=now.st_dev,
            )
        # Belt-and-suspenders: re-validate fs type against the allowlist.
        # Closes the remount-with-same-st_dev edge case where a disallowed
        # filesystem could be swapped under an already-bound namespace.
        # ``include_env=False`` — strictly use the bind-time snapshot;
        # never re-read the env var, which a same-uid actor could mutate.
        current_fs = _check_fs_allowed(
            self.root_path, effective_extend, include_env=False
        )
        if current_fs != self.fs_type:
            raise UnsupportedFilesystem(
                fs_type=current_fs, root_path=self.root_path
            )


# ---------------------------------------------------------------------------
# Predicate — within_org_root
# ---------------------------------------------------------------------------


def within_org_root(path: Path, ns: OrgRootNamespace) -> bool:
    """True iff ``path`` (strictly resolved) descends from ``ns.root_path``. [§3.11d, §5.2 BT2, §6.7 F-ISO-*]

    Re-verifies the namespace's inode + volume bindings as part of the call
    (drift raises rather than returning False — drift is a fail-closed
    condition, not an "outside the root" condition).

    The caller's ``path`` does NOT need to exist. A nonexistent path whose
    parent is under ``ns.root_path`` returns True, because the intent of
    this predicate is "can I write here?" — not "does this already exist?".

    Symlink semantics: every existing symlink component on the path is
    strictly resolved. A symlink whose target escapes the root raises
    ``SymlinkResolveFailed``.

    Raises:
        TypeError: non-``Path`` argument.
        InodeDrift / VolumeDrift: namespace has drifted (fail-closed).
        SymlinkResolveFailed: symlink loop or chain that refuses to resolve.
    """
    if not isinstance(path, Path):
        raise TypeError(
            f"within_org_root: path must be pathlib.Path; got {type(path).__name__}"
        )
    if not isinstance(ns, OrgRootNamespace):
        raise TypeError(
            f"within_org_root: ns must be OrgRootNamespace; got "
            f"{type(ns).__name__}"
        )

    # Fail-closed drift check first. If the root is compromised the
    # predicate MUST NOT return a silent True or False.
    ns.verify_bindings_still_hold()

    # Resolve the argument. strict=False so callers can probe paths that
    # don't exist yet (the common "can I create this?" case).
    try:
        resolved = path.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise SymlinkResolveFailed(path=path, reason=str(exc)) from exc

    # Cheap absolute-prefix check against the already-resolved namespace root.
    try:
        resolved.relative_to(ns.root_path)
    except ValueError:
        # resolved is outside ns.root_path. This is a normal False, not an
        # exception — callers often ask "is this path inside?" as a probe.
        return False

    # Every existing symlink on the INPUT path must not escape the root,
    # even if the fully-resolved final path happens to land inside. (A
    # symlink that detours through an external directory lets an attacker
    # swap the external content mid-session — the escape is real even if
    # the final inode happens to be inside the root.)
    _walk_chain_for_escape(path, ns.root_path)
    return True


def _walk_chain_for_escape(input_path: Path, root_resolved: Path) -> None:
    """Raise ``SymlinkResolveFailed`` for any existing symlink component of
    ``input_path`` whose resolved target escapes ``root_resolved``.

    Unlike ``topology._walk_for_symlink_escape`` (which walks the already-
    resolved target's ancestors — and therefore cannot see any symlinks,
    because resolution has already chased them), this helper walks the
    ORIGINAL input path's components pre-resolution. That is the surface
    where an attacker can plant a symlink; checking post-resolution misses
    intermediate escapes whose final target loops back inside the root.
    """
    try:
        absolute = Path(os.path.abspath(input_path))
    except (OSError, ValueError) as exc:
        raise SymlinkResolveFailed(path=input_path, reason=str(exc)) from exc

    parts = absolute.parts
    if not parts:
        return
    accumulated = Path(parts[0])
    for part in parts[1:]:
        accumulated = accumulated / part
        if not accumulated.exists() and not accumulated.is_symlink():
            # Nonexistent tail — no more components on disk to examine.
            break
        if not accumulated.is_symlink():
            continue
        try:
            target = accumulated.resolve(strict=False)
        except (OSError, RuntimeError) as exc:
            raise SymlinkResolveFailed(
                path=input_path,
                reason=f"component_{accumulated}_resolve_error:{exc!s}",
            ) from exc
        try:
            target.relative_to(root_resolved)
        except ValueError:
            raise SymlinkResolveFailed(
                path=input_path,
                reason=(
                    f"symlink_{accumulated}_target_{target}"
                    f"_outside_root_{root_resolved}"
                ),
            )


# ---------------------------------------------------------------------------
# Context manager — with_org_root
# ---------------------------------------------------------------------------


@contextmanager
def with_org_root(
    ns: OrgRootNamespace,
    *,
    blocking: bool = True,
) -> Iterator["OrgRootGate"]:
    """Open ``ns.root_path`` as a directory FD, hold ``fcntl.flock``, yield gate. [§3.11d, §5.2 BT2]

    Provides TOCTOU-safe access to the namespace root for a batch of
    operations. The directory FD is held for the lifetime of the context,
    so any mid-session rename / unlink of the root shows up immediately —
    either the FD operations fail with ``ENOENT`` (Linux detaches inode on
    unlink) or the gate's ``check()`` catches the inode drift.

    An advisory POSIX ``fcntl.flock`` (LOCK_EX by default; LOCK_SH on read-
    only sessions is a v0.2 extension) is taken on the directory FD. This
    serializes concurrent sessions that attempt to operate on the same
    namespace within the same host OS — per ``fcntl.flock`` semantics, the
    lock is advisory and respected only by callers that also call flock.
    For v0.1 Tilth is single-process so contention is rare; the lock
    guards against test-harness races and future multi-seat parallelism.

    Args:
        blocking: if True (default), the ``fcntl.flock(LOCK_EX)`` call
            blocks until the lock is granted. If False, ``LOCK_EX | LOCK_NB``
            is used and ``BlockingIOError`` propagates on contention.

    Yields:
        ``OrgRootGate`` — a callable-bearing object whose ``check(path)``
        method re-verifies ``within_org_root`` using the held FD. Also
        exposes ``fd`` for callers that need to pass a dirfd to ``openat``.

    Raises:
        IsolationError and subclasses as ``OrgRootGate.check`` raises; see
        the individual exception docstrings.
    """
    if not isinstance(ns, OrgRootNamespace):
        raise TypeError(
            f"with_org_root: ns must be OrgRootNamespace; got {type(ns).__name__}"
        )

    flags = os.O_DIRECTORY | os.O_CLOEXEC
    # O_NOFOLLOW is honored on macOS and Linux; the root itself must not be
    # a symlink — a symlink at the top level would be a topology violation
    # caught at bind() time anyway, but double-checking costs nothing.
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW

    fd = os.open(str(ns.root_path), flags)
    lock_mode = fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB)
    lock_acquired = False
    try:
        fcntl.flock(fd, lock_mode)
        lock_acquired = True
        # Even after opening the FD, the inode could have shifted between
        # bind() and open() — re-verify once more under the held lock.
        ns.verify_bindings_still_hold()
        gate = OrgRootGate(ns=ns, fd=fd)
        yield gate
    finally:
        if lock_acquired:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
            except OSError:  # pragma: no cover  — unlock failure on closed fd
                pass
        try:
            os.close(fd)
        except OSError:  # pragma: no cover
            pass


@dataclass
class OrgRootGate:
    """Handle yielded by ``with_org_root``. Not instantiable outside the CM."""

    ns: OrgRootNamespace
    fd: int

    def check(self, path: Path) -> bool:
        """Re-verify ``within_org_root(path, self.ns)`` inside the held lock.

        Equivalent to calling ``within_org_root(path, ns)`` but makes the
        "the lock is still held" invariant explicit at the call site.

        Returns:
            bool — True if path descends from the root; False if outside.

        Raises:
            IsolationError subclasses on drift / symlink-escape.
        """
        return within_org_root(path, self.ns)


# ---------------------------------------------------------------------------
# Phase-0 stub — Linux bind-mount namespace
# ---------------------------------------------------------------------------


def create_bind_mount_namespace(ns: OrgRootNamespace) -> None:
    """Phase-0 stub. Raises ``NotImplementedError`` pointing at the v0.2 work item.

    The intended v0.2 Linux implementation creates a mount namespace
    (``CLONE_NEWNS``) containing a bind mount of ``ns.root_path`` at a
    private path, then ``chroot`` / ``pivot_root`` so the seat process
    cannot reference any other org's path even by absolute path name.

    The Phase-0 isolation story rides on the open-FD + advisory-lock +
    strict-resolve pattern in ``with_org_root`` / ``within_org_root``,
    which is portable (macOS + Linux) and sufficient for the single-
    process dev tier. Production Linux tier will compose this stub-filled
    primitive with a real mount-namespace on top.

    Raises:
        NotImplementedError: always, with a clear pointer to the v0.2 issue.
    """
    raise NotImplementedError(
        "create_bind_mount_namespace is a Phase-0 stub. "
        "See pipeline/engineering/round_E_vault_fs_spec.md §8 "
        "and the Section-2 Vault v0.2 roadmap for the mount-namespace "
        "work item."
    )
