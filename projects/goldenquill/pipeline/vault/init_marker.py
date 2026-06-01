"""Vault init marker — BT14.a + BT14.f ceremony.

Blueprint §2.3 + §5.1 + §5.6 + §6.11.

Ceremony ordering (§5.6):
    1. Stable-UUID floor (uuid_floor.enforce).
    2. Shared init verification (``vault_shared/init.marker``).
    3. Per-org marker write (or verify on subsequent boots).

HMAC keyed by ``tilth.vault.init.hmac.v1`` from the keystore. Body + trailer
both computed over ``canonical_json_bytes`` so whitespace-only tamper cannot
evade. A single ``fcntl.LOCK_EX`` is held across body write + trailer write +
fsync so the two artefacts commit atomically with respect to any other boot.
"""

from __future__ import annotations

import datetime as _dt
import fcntl
import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Final


BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§2.3 vault init marker schema",
            "§5.1 vault_shared init verification",
            "§5.6 per-org init marker ceremony (BT14.a + BT14.f)",
            "§6.11 F-INIT-01 / F-INIT-02 / F-INIT-03 failure codes",
        ],
    },
}

from pipeline.sovereignty import (
    KeyStore,
    canonical_json_bytes,
    hmac_sha3_512,
)
from pipeline.vault.error_codes import (
    F_INIT_01,
    F_INIT_02,
    F_INIT_03,
    VaultInitError,
    VaultInitHMACMismatch,
    VaultInitIdentityDrift,
)
from pipeline.vault.identity_tuple import resolve_identity_tuple
from pipeline.vault.schemas import IdentityTuple, VaultInitMarker

VAULT_INIT_HMAC_KEY_ID = "tilth.vault.init.hmac.v1"


class VaultInitMissing(VaultInitError):
    code = F_INIT_01


class VaultInitAlreadyExists(VaultInitError):
    code = F_INIT_01


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    return (
        _dt.datetime.now(_dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _atomic_write(target: Path, payload: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + f".tmp.{os.getpid()}")
    with open(tmp, "wb") as fh:
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(str(tmp), str(target))
    parent_fd = os.open(str(target.parent), os.O_RDONLY)
    try:
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)


def _identity_tuple_from_mapping(m: dict) -> IdentityTuple:
    return IdentityTuple(
        volume_uuid=m["volume_uuid"],
        fs_file_id=m["fs_file_id"],
        mount_id=m["mount_id"],
        fs_type=m["fs_type"],
        captured_at=m["captured_at"],
    )


def _marker_from_mapping(m: dict) -> VaultInitMarker:
    return VaultInitMarker(
        scope=m["scope"],
        slug=m["slug"],
        created_at=m["created_at"],
        created_under_uuid=m["created_under_uuid"],
        identity_tuple=_identity_tuple_from_mapping(m["identity_tuple"]),
        operator_id=m["operator_id"],
        section_lock_hash=m["section_lock_hash"],
    )


def _compute_hmac(body_bytes: bytes, keystore: KeyStore) -> str:
    raw = keystore._retrieve_raw(VAULT_INIT_HMAC_KEY_ID)  # noqa: SLF001
    try:
        key = bytes(raw)
        digest = hmac_sha3_512(key, body_bytes)
        return digest.hex()
    finally:
        for i in range(len(raw)):
            raw[i] = 0


# ---------------------------------------------------------------------------
# Write (ceremony — first time only)
# ---------------------------------------------------------------------------


def write_vault_init_marker(
    *,
    marker_path: Path,
    hmac_path: Path,
    lock_path: Path,
    keystore: KeyStore,
    scope: str,
    slug: str,
    operator_id: str,
    section_lock_hash: str,
) -> VaultInitMarker:
    """Create a VaultInitMarker + HMAC trailer on a fresh target.

    Raises :class:`VaultInitAlreadyExists` if either artefact is already on
    disk. Single ``fcntl.LOCK_EX`` held across both writes.
    """
    for name, val in (
        ("marker_path", marker_path),
        ("hmac_path", hmac_path),
        ("lock_path", lock_path),
    ):
        if not isinstance(val, Path):
            raise TypeError(f"{name} must be pathlib.Path")
    if not isinstance(keystore, KeyStore):
        raise TypeError("keystore must be a KeyStore instance")
    if scope not in ("shared", "org"):
        raise ValueError(f"scope must be 'shared' or 'org', got {scope!r}")
    if not isinstance(slug, str):
        raise TypeError("slug must be str")
    if scope == "shared" and slug != "":
        raise ValueError("shared scope requires slug=''")
    if scope == "org" and slug == "":
        raise ValueError("org scope requires non-empty slug")

    marker_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        if marker_path.exists() or hmac_path.exists():
            raise VaultInitAlreadyExists(
                f"init marker already present at {marker_path} / {hmac_path}"
            )

        identity = resolve_identity_tuple(marker_path.parent)
        body = VaultInitMarker(
            scope=scope,
            slug=slug,
            created_at=_now_iso(),
            created_under_uuid=identity.volume_uuid,
            identity_tuple=identity,
            operator_id=operator_id,
            section_lock_hash=section_lock_hash,
        )
        body_bytes = canonical_json_bytes(asdict(body))
        _atomic_write(marker_path, body_bytes)
        hmac_hex = _compute_hmac(body_bytes, keystore)
        _atomic_write(hmac_path, (hmac_hex + "\n").encode("ascii"))
        return body
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        finally:
            os.close(lock_fd)


# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------


def verify_vault_init_marker(
    *,
    marker_path: Path,
    hmac_path: Path,
    keystore: KeyStore,
    expected_slug: str,
    expected_scope: str,
) -> VaultInitMarker:
    """Verify an existing marker + HMAC. Raises on any failure.

    :raises VaultInitMissing: F-INIT-01 marker or hmac file absent.
    :raises VaultInitHMACMismatch: F-INIT-02 HMAC digest mismatch.
    :raises VaultInitIdentityDrift: F-INIT-03 identity tuple or UUID drift.
    """
    for name, val in (("marker_path", marker_path), ("hmac_path", hmac_path)):
        if not isinstance(val, Path):
            raise TypeError(f"{name} must be pathlib.Path")
    if not isinstance(keystore, KeyStore):
        raise TypeError("keystore must be a KeyStore instance")

    if not marker_path.is_file():
        raise VaultInitMissing(f"marker absent: {marker_path}")
    if not hmac_path.is_file():
        raise VaultInitMissing(f"hmac absent: {hmac_path}")

    body_bytes = marker_path.read_bytes()
    try:
        body = _marker_from_mapping(json.loads(body_bytes))
    except (json.JSONDecodeError, KeyError) as exc:
        raise VaultInitError(f"marker body unparseable: {exc}") from exc

    # Recompute canonical bytes from parsed body; whitespace-only tamper fails here.
    canonical = canonical_json_bytes(asdict(body))
    if canonical != body_bytes:
        raise VaultInitHMACMismatch(
            "marker body is not canonical — tamper or whitespace drift"
        )

    expected_hmac_hex = _compute_hmac(canonical, keystore)
    actual = hmac_path.read_text(encoding="ascii").strip()
    if actual != expected_hmac_hex:
        raise VaultInitHMACMismatch(f"hmac mismatch for {marker_path}")

    if body.scope != expected_scope:
        raise VaultInitError(
            f"scope mismatch: marker says {body.scope!r}, expected {expected_scope!r}"
        )
    if body.slug != expected_slug:
        raise VaultInitError(
            f"slug mismatch: marker says {body.slug!r}, expected {expected_slug!r}"
        )

    current_identity = resolve_identity_tuple(marker_path.parent)
    if current_identity.volume_uuid != body.created_under_uuid:
        raise VaultInitIdentityDrift(
            f"volume UUID drifted: marker={body.created_under_uuid}, "
            f"current={current_identity.volume_uuid}"
        )
    if current_identity.fs_type != body.identity_tuple.fs_type:
        raise VaultInitIdentityDrift(
            f"fs_type drifted: marker={body.identity_tuple.fs_type}, "
            f"current={current_identity.fs_type}"
        )

    return body


__all__ = [
    "VAULT_INIT_HMAC_KEY_ID",
    "VaultInitAlreadyExists",
    "VaultInitMissing",
    "verify_vault_init_marker",
    "write_vault_init_marker",
]
