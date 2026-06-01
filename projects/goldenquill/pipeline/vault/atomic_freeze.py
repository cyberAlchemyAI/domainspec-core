"""Atomic verify-and-freeze for `vault_shared/`. [§4.7 + §9 steps 7 + 11a]

Round U entry points:

* :func:`apply` (§9 step 7) — accepts the verified Merkle pin produced by
  Round T :func:`pipeline.vault.m15_ledger.verify_seed_manifest`, optionally
  takes a CoV snapshot via an injected :type:`SnapshotProvider`, enforces
  the A-09 retention policy, and returns an :class:`AtomicFreezeResult` for
  the rails report.
* :func:`prune_snapshots` (§9 step 11a) — standalone CoV housekeeping
  invoked late in the boot sequence; deletes the oldest snapshots above
  ``retention_count``.

Platform support:

* macOS (darwin) — primary. The ``VaultSharedFrozenRoot`` IS the freeze
  (per-FD re-walk via Round S :func:`make_post_gate_hook`); the optional
  APFS snapshot is defence-in-depth.
* Linux — primary mount-namespace switch is documented but deferred past
  v0.1 (the dev box is macOS). On Linux, ``apply()`` returns
  ``namespace_active=False`` plus a degradation note. The Merkle pin still
  holds because it's platform-agnostic.

Failure-mode discipline:

* Primary failure (Merkle pin invalid, type errors) → :class:`AtomicFreezeFailed`
  (F-FREEZE-01) — fatal, raised.
* Snapshot create failure → ``snapshot_degraded=True`` + degradation note
  (F-FREEZE-03 in the rails report) — non-fatal, primary still holds.
* Retention prune failure inside :func:`apply` → ``retention_degraded=True``
  + degradation note (F-FREEZE-04) — non-fatal.
* Standalone :func:`prune_snapshots` raises :class:`SnapshotRetentionCleanupFailed`
  (F-FREEZE-04) on failure because the §9 step 11a caller decides the
  policy.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Optional, Protocol, Sequence

from pipeline.vault.error_codes import F_FREEZE_01, F_FREEZE_04, FreezeError
from pipeline.vault.mirror_verify import VaultSharedFrozenRoot

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§4.7 macOS-primary verify-and-freeze mechanism over vault_shared/",
            "§9 step 7 atomic-freeze ceremony (apply)",
            "§9 step 11a CoV snapshot retention housekeeping (prune_snapshots)",
            "§8 A-09 retention policy (count=3)",
        ],
    },
}


# ---------------------------------------------------------------------------
# Constants (§8 pins)
# ---------------------------------------------------------------------------


COV_SNAPSHOT_RETENTION_COUNT: int = 3
"""§8 — count of CoV snapshots retained per A-09 policy."""

PLATFORM_DARWIN: str = "darwin"
PLATFORM_LINUX: str = "linux"

_SNAPSHOT_LABEL_PREFIX: str = "com.tilth.vault_shared"


# ---------------------------------------------------------------------------
# Exception family
# ---------------------------------------------------------------------------


class AtomicFreezeFailed(FreezeError):
    """Primary mechanism failed — boot must abort."""

    code = F_FREEZE_01


class SnapshotRetentionCleanupFailed(FreezeError):
    """A-09 retention prune failed — non-fatal at boot but raised by the
    standalone :func:`prune_snapshots` so callers can decide policy."""

    code = F_FREEZE_04


# ---------------------------------------------------------------------------
# Snapshot provider protocol + records
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class SnapshotRecord:
    label: str
    created_at_iso: str


class SnapshotProvider(Protocol):
    """Minimal CoV-snapshot interface.

    Production callers wire this to ``tmutil`` (APFS), ``btrfs subvolume``,
    or ``zfs snapshot``. v0.1 ships no production implementation; tests
    inject a fake.
    """

    def list_snapshots(self) -> Sequence[SnapshotRecord]: ...

    def create_snapshot(self, *, label: str) -> SnapshotRecord: ...

    def delete_snapshot(self, *, label: str) -> None: ...


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class AtomicFreezeResult:
    platform: str
    frozen_root: VaultSharedFrozenRoot
    namespace_active: bool
    snapshot_label: Optional[str]
    snapshots_pruned: tuple[str, ...]
    snapshot_degraded: bool
    retention_degraded: bool
    degradations: tuple[str, ...]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _iso_utc_now() -> str:
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _build_label(*, session_id: str, ts_iso: str) -> str:
    safe_ts = ts_iso.replace(":", "").replace("-", "")
    return f"{_SNAPSHOT_LABEL_PREFIX}.{session_id}.{safe_ts}"


def _is_snapshot_provider_like(obj: object) -> bool:
    return (
        callable(getattr(obj, "list_snapshots", None))
        and callable(getattr(obj, "create_snapshot", None))
        and callable(getattr(obj, "delete_snapshot", None))
    )


def _delete_oldest(
    provider: SnapshotProvider,
    records: Sequence[SnapshotRecord],
    *,
    target_count: int,
) -> tuple[str, ...]:
    """Delete oldest snapshots until ``len(records) <= target_count``.

    Returns the labels deleted in deletion order (oldest first). Raises
    whatever the provider raises if a delete fails.
    """
    if len(records) <= target_count:
        return ()
    sorted_oldest_first = sorted(records, key=lambda r: r.created_at_iso)
    excess = len(records) - target_count
    to_delete = sorted_oldest_first[:excess]
    deleted: list[str] = []
    for rec in to_delete:
        provider.delete_snapshot(label=rec.label)
        deleted.append(rec.label)
    return tuple(deleted)


# ---------------------------------------------------------------------------
# apply — §9 step 7
# ---------------------------------------------------------------------------


def apply(
    *,
    frozen_root: VaultSharedFrozenRoot,
    vault_shared_root: Path,
    session_id: str,
    platform: str = PLATFORM_DARWIN,
    snapshot_provider: Optional[SnapshotProvider] = None,
    clock_iso_now=_iso_utc_now,
    retention_count: int = COV_SNAPSHOT_RETENTION_COUNT,
) -> AtomicFreezeResult:
    """§9 step 7 — atomic verify-and-freeze.

    The macOS primary mechanism is the per-FD Merkle re-walk wired by Round
    S :func:`make_post_gate_hook`. ``apply()`` accepts the already-verified
    :class:`VaultSharedFrozenRoot`, optionally takes a CoV snapshot, and
    enforces A-09 retention. Snapshot/retention failures are non-fatal
    (degradations recorded in the result).
    """
    if not isinstance(frozen_root, VaultSharedFrozenRoot):
        raise TypeError(
            f"frozen_root must be VaultSharedFrozenRoot, got {type(frozen_root).__name__}"
        )
    if not isinstance(vault_shared_root, Path):
        raise TypeError(
            f"vault_shared_root must be pathlib.Path, got {type(vault_shared_root).__name__}"
        )
    if not isinstance(session_id, str):
        raise TypeError(
            f"session_id must be str, got {type(session_id).__name__}"
        )
    if not session_id:
        raise ValueError("session_id must be non-empty")
    if snapshot_provider is not None and not _is_snapshot_provider_like(
        snapshot_provider
    ):
        raise TypeError("snapshot_provider must implement SnapshotProvider")
    if retention_count < 0:
        raise ValueError(
            f"retention_count must be >= 0, got {retention_count}"
        )

    degradations: list[str] = []
    namespace_active = False

    # Linux mount-namespace switch is deferred past v0.1.
    if platform != PLATFORM_DARWIN:
        degradations.append(
            f"linux-mount-ns-not-implemented-v0.1:{platform}"
        )

    snapshot_label: Optional[str] = None
    snapshots_pruned: tuple[str, ...] = ()
    snapshot_degraded = False
    retention_degraded = False

    if snapshot_provider is not None:
        # Step 1: prune so post-create count == retention.
        try:
            existing = tuple(snapshot_provider.list_snapshots())
        except Exception as exc:  # F-FREEZE-04 + downstream F-FREEZE-03
            retention_degraded = True
            snapshot_degraded = True
            degradations.append(
                f"retention-prune-failed:list-snapshots:{type(exc).__name__}"
            )
            degradations.append(
                f"snapshot-create-failed:list-snapshots-prerequisite:{type(exc).__name__}"
            )
            return AtomicFreezeResult(
                platform=platform,
                frozen_root=frozen_root,
                namespace_active=namespace_active,
                snapshot_label=None,
                snapshots_pruned=(),
                snapshot_degraded=snapshot_degraded,
                retention_degraded=retention_degraded,
                degradations=tuple(degradations),
            )

        # Make room for one more by reducing to retention - 1 (clamped >= 0).
        target_after_prune = max(retention_count - 1, 0)
        try:
            snapshots_pruned = _delete_oldest(
                snapshot_provider, existing, target_count=target_after_prune
            )
        except Exception as exc:
            retention_degraded = True
            degradations.append(
                f"retention-prune-failed:{type(exc).__name__}"
            )
            # Keep going — snapshot create may still succeed and the rails
            # report surfaces the prune failure.

        # Step 2: create the new snapshot.
        try:
            new_label = _build_label(
                session_id=session_id, ts_iso=clock_iso_now()
            )
            rec = snapshot_provider.create_snapshot(label=new_label)
            snapshot_label = rec.label
        except Exception as exc:
            snapshot_degraded = True
            degradations.append(
                f"snapshot-create-failed:{type(exc).__name__}"
            )

    return AtomicFreezeResult(
        platform=platform,
        frozen_root=frozen_root,
        namespace_active=namespace_active,
        snapshot_label=snapshot_label,
        snapshots_pruned=snapshots_pruned,
        snapshot_degraded=snapshot_degraded,
        retention_degraded=retention_degraded,
        degradations=tuple(degradations),
    )


# ---------------------------------------------------------------------------
# prune_snapshots — §9 step 11a
# ---------------------------------------------------------------------------


def prune_snapshots(
    *,
    snapshot_provider: SnapshotProvider,
    retention_count: int = COV_SNAPSHOT_RETENTION_COUNT,
) -> tuple[str, ...]:
    """§9 step 11a — standalone CoV housekeeping.

    Deletes the oldest snapshots until ``count <= retention_count``. Returns
    the labels deleted in deletion order. Raises
    :class:`SnapshotRetentionCleanupFailed` (F-FREEZE-04) if the provider
    raises (list or delete) — caller decides whether to escalate to the
    rails report or swallow.
    """
    if not _is_snapshot_provider_like(snapshot_provider):
        raise TypeError("snapshot_provider must implement SnapshotProvider")
    if retention_count < 0:
        raise ValueError(
            f"retention_count must be >= 0, got {retention_count}"
        )

    try:
        existing = tuple(snapshot_provider.list_snapshots())
    except Exception as exc:
        raise SnapshotRetentionCleanupFailed(
            f"list_snapshots raised {type(exc).__name__}: {exc}"
        ) from exc

    try:
        return _delete_oldest(
            snapshot_provider, existing, target_count=retention_count
        )
    except Exception as exc:
        raise SnapshotRetentionCleanupFailed(
            f"delete_snapshot raised {type(exc).__name__}: {exc}"
        ) from exc


__all__ = [
    "COV_SNAPSHOT_RETENTION_COUNT",
    "PLATFORM_DARWIN",
    "PLATFORM_LINUX",
    "AtomicFreezeFailed",
    "AtomicFreezeResult",
    "SnapshotProvider",
    "SnapshotRecord",
    "SnapshotRetentionCleanupFailed",
    "apply",
    "prune_snapshots",
]
