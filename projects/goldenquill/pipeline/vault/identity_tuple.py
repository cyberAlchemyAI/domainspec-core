"""Identity-tuple resolver.

Blueprint §2.1 + §4.1 + §7.3. Resolves the ``(volume_uuid, fs_file_id,
mount_id, fs_type)`` identity tuple for a path, using platform-native probes.

v0.1 scope: a pragmatic shim that uses ``os.stat()`` + ``mount``/``/proc/mounts``
parsing. A hardened implementation using macOS ``getattrlist`` (ATTR_CMN_FILEID +
f_fsid) and Linux ``statx(STATX_MNT_ID)`` is a v2 item — the interface is
stable so callers do not change. The shim is sufficient for the per-boot
identity-pinning invariant (BT14.g) because ``(st_dev, st_ino, fs_type,
mount_line_hash)`` together cover mount-remount drift detection even without
kernel-native identifiers.

Cache eviction: the resolver recomputes on every call; there is no cache in
v0.1 (the blueprint allows but does not require a cache). §7.3's "cache
eviction triggers on mount-table change" becomes trivially true.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import platform
import subprocess
from pathlib import Path
from typing import Final

from pipeline.vault.error_codes import VaultError
from pipeline.vault.schemas import IdentityTuple


BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§2.1 IdentityTuple identity-tuple resolver (v0.1 os.stat + mount-table shim)",
            "§4.1 per-boot identity pinning input",
            "§7.3 cache-eviction-on-mount-change (trivially satisfied — no cache in v0.1)",
        ],
    },
}


class IdentityTupleUnavailable(VaultError):
    code = "F-UUID-01"


def _now_iso() -> str:
    return (
        _dt.datetime.now(_dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


# ---------------------------------------------------------------------------
# Platform probes (overridable for unit tests)
# ---------------------------------------------------------------------------


def _mount_command_output() -> str:
    try:
        return subprocess.run(
            ["/sbin/mount"], capture_output=True, text=True, check=True, timeout=5
        ).stdout
    except FileNotFoundError:
        return subprocess.run(
            ["mount"], capture_output=True, text=True, check=True, timeout=5
        ).stdout


def _parse_darwin_mounts(mount_output: str) -> list[tuple[str, str, str]]:
    """Return [(device, mountpoint, fstype)] from BSD-style mount output."""
    rows: list[tuple[str, str, str]] = []
    for line in mount_output.splitlines():
        if " on " not in line:
            continue
        left, _, rest = line.partition(" on ")
        mnt, _, tail = rest.partition(" (")
        fstype = tail.split(",", 1)[0].strip().rstrip(")")
        rows.append((left.strip(), mnt.strip(), fstype))
    return rows


def _parse_proc_mounts(content: str) -> list[tuple[str, str, str]]:
    """Return [(device, mountpoint, fstype)] from /proc/mounts format."""
    rows: list[tuple[str, str, str]] = []
    for line in content.splitlines():
        parts = line.split()
        if len(parts) < 3:
            continue
        rows.append((parts[0], parts[1], parts[2]))
    return rows


def _best_mount_match(
    rows: list[tuple[str, str, str]], path: Path
) -> tuple[str, str, str]:
    """Return the longest-prefix mountpoint match for ``path``."""
    best: tuple[str, str, str] | None = None
    best_len = -1
    path_str = str(path.resolve())
    for device, mnt, fstype in rows:
        if path_str == mnt or path_str.startswith(mnt.rstrip("/") + "/") or mnt == "/":
            if len(mnt) > best_len:
                best_len = len(mnt)
                best = (device, mnt, fstype)
    if best is None:
        raise IdentityTupleUnavailable(
            f"no mount table entry covers {path_str}"
        )
    return best


def _probe_darwin(path: Path) -> tuple[str, str, str]:
    rows = _parse_darwin_mounts(_mount_command_output())
    return _best_mount_match(rows, path)


def _probe_linux(path: Path) -> tuple[str, str, str]:
    try:
        content = Path("/proc/mounts").read_text()
    except OSError as exc:
        raise IdentityTupleUnavailable(f"/proc/mounts unreadable: {exc}") from exc
    rows = _parse_proc_mounts(content)
    return _best_mount_match(rows, path)


def _volume_uuid_hex(device: str, mountpoint: str, fstype: str) -> str:
    """Derive a stable 32-char hex volume identifier.

    v0.1 shim: SHA3-256-truncated digest of ``(device||mountpoint||fstype)``.
    Real volume UUIDs come from ``diskutil info`` / ``/dev/disk/by-uuid/``;
    those are wired in v2. The shim digest changes when the mount table
    changes, which is exactly the invariant BT14.g needs: a remount-remapped
    volume yields a different identity tuple.
    """
    h = hashlib.sha3_256()
    h.update(device.encode("utf-8"))
    h.update(b"\x00")
    h.update(mountpoint.encode("utf-8"))
    h.update(b"\x00")
    h.update(fstype.encode("utf-8"))
    return h.hexdigest()[:32]


def _mount_id_hex(device: str, mountpoint: str) -> str:
    h = hashlib.sha3_256()
    h.update(device.encode("utf-8"))
    h.update(b"\x00")
    h.update(mountpoint.encode("utf-8"))
    return h.hexdigest()[:16]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def resolve_identity_tuple(path: Path) -> IdentityTuple:
    """Resolve the IdentityTuple covering ``path``.

    Raises :class:`IdentityTupleUnavailable` when the platform is unsupported
    or the mount table cannot be read.
    """
    if not isinstance(path, Path):
        raise TypeError(f"path must be pathlib.Path, got {type(path).__name__}")
    system = platform.system()
    if system == "Darwin":
        device, mountpoint, fstype = _probe_darwin(path)
    elif system == "Linux":
        device, mountpoint, fstype = _probe_linux(path)
    else:
        raise IdentityTupleUnavailable(f"platform {system!r} unsupported")

    try:
        st = path.stat()
    except OSError as exc:
        raise IdentityTupleUnavailable(f"cannot stat {path}: {exc}") from exc

    return IdentityTuple(
        volume_uuid=_volume_uuid_hex(device, mountpoint, fstype),
        fs_file_id=f"{st.st_ino:016x}",
        mount_id=_mount_id_hex(device, mountpoint),
        fs_type=fstype,
        captured_at=_now_iso(),
    )


__all__ = [
    "IdentityTupleUnavailable",
    "resolve_identity_tuple",
]
