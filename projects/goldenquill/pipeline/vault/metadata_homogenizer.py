"""M14.2 — Metadata homogenization. [§4.2]

Seat-visible file metadata (mtime/ctime/atime, size, xattrs, path name) MUST
NOT leak operator cadence or cross-org correlation. This module provides the
three primitives the FD broker (Round S) applies between ``openat2`` /
``openat`` and FD hand-off:

1. **Timestamp floor.** ``st_mtime`` / ``st_ctime`` are projected to the
   most-recent second-boundary ≤ Vault-boot wall-clock. ``st_atime`` is
   suppressed (set equal to ``st_mtime``).
2. **Size bucketing for cache pages.** Files served from
   ``cached_opportunities/`` or ``research_db/`` caches are padded on-the-wire
   to the next bucket in {4 KiB, 64 KiB, 1 MiB, 16 MiB, 256 MiB}. Seed files
   pass through at true size — they are M15-signed and must re-verify
   byte-for-byte.
3. **Xattr strip.** All four Linux xattr namespaces (``user`` /
   ``trusted`` / ``security`` / ``system``) and every macOS xattr. After
   ``fremovexattr`` sweep, a post-check ``flistxattr`` must return empty; a
   non-empty residue raises ``F-VAULT-05`` (``VaultXattrStripIncomplete``).
"""

from __future__ import annotations

import os
import platform
from dataclasses import dataclass
from typing import Final, Optional

from pipeline.vault.error_codes import VaultXattrStripIncomplete


BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§4.2 M14.2 metadata homogenization — timestamp floor (mtime/ctime → ≤ vault-boot wall-clock; atime suppressed)",
            "§4.2 size bucketing for cache pages (4 KiB / 64 KiB / 1 MiB / 16 MiB / 256 MiB; seed files pass-through)",
            "§4.2 xattr strip across all 4 Linux namespaces + macOS xattrs; post-check empty or F-VAULT-05",
            "§6.1 VaultXattrStripIncomplete → F-VAULT-05 raise site",
        ],
    },
}


# ---------------------------------------------------------------------------
# Size-bucket table (§4.2)
# ---------------------------------------------------------------------------

SIZE_BUCKETS: tuple[int, ...] = (
    4 * 1024,
    64 * 1024,
    1 * 1024 * 1024,
    16 * 1024 * 1024,
    256 * 1024 * 1024,
)


def pick_size_bucket(true_size: int) -> int:
    """Return the smallest bucket ≥ ``true_size``.

    If ``true_size`` is larger than the largest bucket, the true size is
    returned unpadded — the blueprint does not specify a bucket above 256 MiB
    because single Vault files above that size are outside v0.1 scope.
    """
    if not isinstance(true_size, int):
        raise TypeError(f"true_size must be int, got {type(true_size).__name__}")
    if true_size < 0:
        raise ValueError(f"true_size must be non-negative, got {true_size}")
    for b in SIZE_BUCKETS:
        if true_size <= b:
            return b
    return true_size


# ---------------------------------------------------------------------------
# Timestamp homogenization
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class HomogenizedStat:
    """Seat-visible stat projection. All times are floored; size is padded.

    The FD broker returns this structure from its ``fstat`` shim in place of
    the kernel's raw ``os.stat_result``. ``st_ino`` and ``st_dev`` are
    preserved so the gate re-stat path can still detect drift; only the
    operator-fingerprinting fields are homogenized.
    """

    st_mode: int
    st_ino: int
    st_dev: int
    st_nlink: int
    st_uid: int
    st_gid: int
    st_size: int
    st_atime: float
    st_mtime: float
    st_ctime: float


def homogenize_stat(
    raw: os.stat_result,
    *,
    vault_boot_wall_clock: float,
    padded_size: Optional[int] = None,
) -> HomogenizedStat:
    """Project a raw ``stat_result`` into the seat-visible view.

    :param raw: the kernel-provided stat result.
    :param vault_boot_wall_clock: unix-timestamp boundary; all returned times
        are ≤ this value, floored to the next lower integer second.
    :param padded_size: if provided (cache-page case), overrides ``st_size``
        with this bucketed value; otherwise the true size is preserved.
    """
    if not isinstance(raw, os.stat_result):
        raise TypeError(
            f"raw must be os.stat_result, got {type(raw).__name__}"
        )
    if not isinstance(vault_boot_wall_clock, (int, float)):
        raise TypeError(
            "vault_boot_wall_clock must be number"
        )
    floor = float(int(vault_boot_wall_clock))
    mtime = min(float(int(raw.st_mtime)), floor)
    ctime = min(float(int(raw.st_ctime)), floor)
    atime = mtime  # atime suppressed — seats cannot distinguish access cadence.
    size = raw.st_size if padded_size is None else padded_size
    return HomogenizedStat(
        st_mode=raw.st_mode,
        st_ino=raw.st_ino,
        st_dev=raw.st_dev,
        st_nlink=raw.st_nlink,
        st_uid=raw.st_uid,
        st_gid=raw.st_gid,
        st_size=size,
        st_atime=atime,
        st_mtime=mtime,
        st_ctime=ctime,
    )


# ---------------------------------------------------------------------------
# Xattr strip
# ---------------------------------------------------------------------------


def _list_xattrs(fd: int) -> list[str]:
    """Return the FD's xattr keys. Returns empty list on platforms without xattrs."""
    listxattr = getattr(os, "listxattr", None)
    if listxattr is None:
        return []
    try:
        return list(listxattr(fd))
    except OSError:
        # ENOTSUP on some filesystems (e.g., tmpfs without xattr support).
        return []


def _remove_xattr(fd: int, key: str) -> None:
    removexattr = getattr(os, "removexattr", None)
    if removexattr is None:
        return
    try:
        removexattr(fd, key)
    except OSError:
        # Some kernel-managed xattrs (e.g., ``security.selinux``, macOS
        # ``com.apple.rootless``) refuse removal. The post-strip check
        # catches these as residuals → VaultXattrStripIncomplete.
        pass


def strip_all_xattrs(fd: int) -> None:
    """Strip every xattr on ``fd`` and verify empty.

    :raises VaultXattrStripIncomplete: F-VAULT-05 when any xattr remains
        after the removal sweep.
    """
    if not isinstance(fd, int):
        raise TypeError(f"fd must be int, got {type(fd).__name__}")
    for key in _list_xattrs(fd):
        _remove_xattr(fd, key)
    residue = _list_xattrs(fd)
    if residue:
        raise VaultXattrStripIncomplete(
            f"xattrs remain on fd after strip: {residue}",
            residual_keys=tuple(residue),
        )


# ---------------------------------------------------------------------------
# Cache-page helpers
# ---------------------------------------------------------------------------


def is_cache_page_path(canonical_path: str) -> bool:
    """Return True iff ``canonical_path`` is under a cache subtree.

    Cache subtrees (v0.1 scope):
      * ``cached_opportunities/…`` (anywhere under shared or per-org)
      * ``research_db/…`` when the path contains ``/_cache/`` OR sits outside
        the ``research_db/seed/`` partition.

    Seed files (``research_db/seed/…``) return False so they pass through at
    true size for M15 re-verification.
    """
    if not isinstance(canonical_path, str):
        raise TypeError(
            f"canonical_path must be str, got {type(canonical_path).__name__}"
        )
    if "cached_opportunities/" in canonical_path:
        return True
    if "research_db/seed/" in canonical_path:
        return False
    if "research_db/" in canonical_path:
        return True
    return False


__all__ = [
    "SIZE_BUCKETS",
    "HomogenizedStat",
    "homogenize_stat",
    "is_cache_page_path",
    "pick_size_bucket",
    "strip_all_xattrs",
]
