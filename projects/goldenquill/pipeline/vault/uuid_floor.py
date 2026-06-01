"""Stable-UUID floor — PRE-gate reject for ephemeral/volatile filesystems.

Blueprint §2.2 + §4 PRE-gate §7.4 + §9 step 2.

Accepts: ``apfs``, ``ext4``, ``btrfs``, ``zfs``, ``xfs``.
Rejects: ``tmpfs``, ``overlayfs-on-tmpfs``, ``fuse`` (non-allowlisted).

Rejection reason is carried as a short machine-readable tag inside the
returned :class:`StableUUIDFloor` record AND as the ``reason`` attribute on
the raised :class:`UUIDFloorRejected` exception — callers can inspect either.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Final

from pipeline.vault.error_codes import F_UUID_01, UUIDFloorError
from pipeline.vault.identity_tuple import resolve_identity_tuple
from pipeline.vault.schemas import StableUUIDFloor


BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§2.2 StableUUIDFloor — fs-type allowlist/denylist enforcement",
            "§4 PRE-gate §7.4 ephemeral-fs reject (tmpfs / overlay / fuse)",
            "§9 step 2 vault-boot PRE-gate hook (fail-closed on non-allowlisted fs)",
        ],
    },
}


# ---------------------------------------------------------------------------
# Allowlist / denylist
# ---------------------------------------------------------------------------

ACCEPTED_FS_TYPES: frozenset[str] = frozenset(
    {"apfs", "ext4", "btrfs", "zfs", "xfs"}
)
DENYLISTED_FS_TYPES: frozenset[str] = frozenset(
    {"tmpfs", "overlay", "fuse", "fuse.gvfsd-fuse", "fusectl", "ramfs"}
)


class UUIDFloorRejected(UUIDFloorError):
    """Raised when the filesystem under ``path`` is not on the allowlist."""

    code = F_UUID_01

    def __init__(self, message: str = "", *, reason: str = "") -> None:
        super().__init__(message)
        self.reason = reason


def _now_iso() -> str:
    return (
        _dt.datetime.now(_dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _volume_uuid_is_nonzero(volume_uuid: str) -> bool:
    return bool(volume_uuid) and any(c not in "0" for c in volume_uuid)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def evaluate(path: Path) -> StableUUIDFloor:
    """Return a StableUUIDFloor record (does not raise)."""
    if not isinstance(path, Path):
        raise TypeError(f"path must be pathlib.Path, got {type(path).__name__}")
    identity = resolve_identity_tuple(path)
    fs_type = identity.fs_type
    volume_uuid = identity.volume_uuid

    if fs_type in DENYLISTED_FS_TYPES:
        return StableUUIDFloor(
            fs_type=fs_type,
            volume_uuid=volume_uuid,
            accepted=False,
            rejection_reason=f"{fs_type}-not-allowed",
            evaluated_at=_now_iso(),
        )
    if fs_type not in ACCEPTED_FS_TYPES:
        return StableUUIDFloor(
            fs_type=fs_type,
            volume_uuid=volume_uuid,
            accepted=False,
            rejection_reason=f"{fs_type}-not-on-allowlist",
            evaluated_at=_now_iso(),
        )
    if not _volume_uuid_is_nonzero(volume_uuid):
        return StableUUIDFloor(
            fs_type=fs_type,
            volume_uuid=volume_uuid,
            accepted=False,
            rejection_reason="volume-uuid-zero",
            evaluated_at=_now_iso(),
        )
    return StableUUIDFloor(
        fs_type=fs_type,
        volume_uuid=volume_uuid,
        accepted=True,
        rejection_reason="",
        evaluated_at=_now_iso(),
    )


def enforce(path: Path) -> StableUUIDFloor:
    """Return StableUUIDFloor if accepted; raise UUIDFloorRejected otherwise."""
    floor = evaluate(path)
    if not floor.accepted:
        raise UUIDFloorRejected(
            f"UUID floor rejects {path}: {floor.rejection_reason}",
            reason=floor.rejection_reason,
        )
    return floor


__all__ = [
    "ACCEPTED_FS_TYPES",
    "DENYLISTED_FS_TYPES",
    "UUIDFloorRejected",
    "enforce",
    "evaluate",
]
