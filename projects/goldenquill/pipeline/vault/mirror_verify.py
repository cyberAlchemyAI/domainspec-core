"""Verified-and-pinned Merkle root over `vault_shared/` + §2.5 trust-root mirror.

Blueprint:

* §2.4 ``VaultSharedSeedManifest`` is the operator-signed manifest committed
  via M15. It carries a ``head_hash`` (Merkle root over canonical seed leaves)
  and per-file ``SeedFile`` entries.
* §2.5 ``TrustRootMirrorManifest`` covers the
  ``~/.tilth/logician_trust_root/router.yaml`` mirror.
* §4.7 macOS-primary mechanism: compute the Merkle root over `vault_shared/`
  seed at boot, freeze the root in an in-process immutable dataclass
  (``VaultSharedFrozenRoot``), and on every ``fd_broker.request_fd()`` for a
  path under ``vault_shared/`` re-walk the inclusion proof to confirm the
  live file still hashes to the manifest's ``content_hash``.

Round S surface (locked here):

``compute_leaf_hash_hex``, ``compute_merkle_root_hex``,
``compute_inclusion_proof``, ``verify_inclusion``, ``VaultSharedFrozenRoot``,
``freeze_vault_shared``, ``reverify_path``, ``make_post_gate_hook``,
``verify_trust_root_mirror``.

Out of scope (deferred):

* M15 ledger-head verification (Round T ``m15_ledger.py``) — the manifest's
  ``m15_ledger_head`` is carried but not chain-checked here.
* Operator signature primitive — injected as a callable so this module does
  not bind to a specific keystore in v0.1.
* Atomic-freeze ceremony (Round U ``atomic_freeze.py``) — `freeze_vault_shared`
  prepares the immutable root, but the actual mount-namespace switch /
  ``chflags uchg`` of `vault_shared/` is the next round's job.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Final, Mapping, Optional

from pipeline.vault.error_codes import (
    F_M15_01,
    F_MIRROR_01,
    F_MIRROR_02,
    F_MIRROR_03,
    F_MIRROR_04,
    F_MIRROR_05,
    M15Error,
    MirrorError,
)
from pipeline.vault.layout import is_seed_partition
from pipeline.vault.schemas import (
    FDBrokerRequest,
    SeedFile,
    TrustRootMirrorManifest,
    VaultSharedSeedManifest,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§2.4 VaultSharedSeedManifest + SeedFile (content verification)",
            "§2.5 TrustRootMirrorManifest (logician trust-root router.yaml mirror)",
            "§4.7 macOS-primary Merkle compute + inclusion proof + per-FD re-walk",
            "§3.6 SectionLockMarker (handshake artefact cross-ref)",
            "§9 step 6 defence-in-depth identity-tuple re-capture on seed files",
        ],
    },
}


# ---------------------------------------------------------------------------
# Domain-tag constants (RFC 6962-style separation of leaf vs. internal hashes)
# ---------------------------------------------------------------------------

LEAF_DOMAIN_TAG: bytes = b"\x00"
NODE_DOMAIN_TAG: bytes = b"\x01"

_VAULT_SHARED_PREFIX = "vault_shared/"


# ---------------------------------------------------------------------------
# Exception family
# ---------------------------------------------------------------------------


class MirrorContentMismatch(MirrorError):
    code = F_MIRROR_02


class MirrorIdentityMismatch(MirrorError):
    code = F_MIRROR_01


class MirrorSignatureInvalid(MirrorError):
    code = F_MIRROR_03


class MirrorImmutabilityMissing(MirrorError):
    code = F_MIRROR_04


class MirrorClockRollback(MirrorError):
    code = F_MIRROR_05


class SeedManifestHeadDrift(MirrorError):
    """Computed Merkle root over manifest leaves != manifest.head_hash."""

    code = F_MIRROR_02


class SeedFileExtraOnDisk(M15Error):
    """A file under the seed partition is not in the manifest (tamper)."""

    code = F_M15_01


class SeedFileContentDrift(M15Error):
    """A file's on-disk hash != SeedFile.content_hash."""

    code = F_M15_01


class SeedFileMissingOnDisk(M15Error):
    """A SeedFile listed in the manifest is missing on disk."""

    code = F_M15_01


class SeedFileIdentityDrift(M15Error):
    """A SeedFile's re-captured identity_tuple does not match the manifest (§9 step 6).

    Defence-in-depth against filesystem-layer substitution (bind-mount swap,
    mount-table manipulation) that would preserve the content hash but change
    the underlying inode identity. Closes the gap between the blueprint §9
    step 6 mandate ("re-capture identity tuple, compare") and the pre-
    remediation freeze-side implementation which only re-hashed bytes.
    """

    code = F_M15_01


# ---------------------------------------------------------------------------
# Inclusion proof step + frozen root
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class InclusionProofStep:
    sibling_hash_hex: str
    side: str  # "left" if sibling is on the left of `current`, else "right"


@dataclass(frozen=True, kw_only=True)
class VaultSharedFrozenRoot:
    """Immutable in-process structure pinning the verified Merkle root.

    `seed_paths` and `leaf_hashes_hex` are tuples (positional, sorted by path).
    `inclusion_proofs[path]` lists the proof steps from leaf to root.
    `content_hashes_hex[path]` is the SeedFile.content_hash captured at boot.
    """

    root_hex: str
    seed_paths: tuple[str, ...]
    leaf_hashes_hex: tuple[str, ...]
    inclusion_proofs: Mapping[str, tuple[InclusionProofStep, ...]] = field(default_factory=dict)
    content_hashes_hex: Mapping[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Canonical leaf bytes + hashing primitives
# ---------------------------------------------------------------------------


def canonical_leaf_bytes(relative_path: str, content_hash_hex: str) -> bytes:
    """Canonical JSON representation of a seed leaf — input to leaf hash."""
    if not isinstance(relative_path, str):
        raise TypeError(
            f"relative_path must be str, got {type(relative_path).__name__}"
        )
    if not isinstance(content_hash_hex, str):
        raise TypeError(
            f"content_hash_hex must be str, got {type(content_hash_hex).__name__}"
        )
    return json.dumps(
        {"hash": content_hash_hex, "path": relative_path},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def compute_leaf_hash_hex(relative_path: str, content_hash_hex: str) -> str:
    """SHA-3-512 hex of (LEAF_TAG || canonical_leaf_bytes)."""
    payload = canonical_leaf_bytes(relative_path, content_hash_hex)
    return hashlib.sha3_512(LEAF_DOMAIN_TAG + payload).hexdigest()


def _internal_hash_hex(left_hex: str, right_hex: str) -> str:
    return hashlib.sha3_512(
        NODE_DOMAIN_TAG + bytes.fromhex(left_hex) + bytes.fromhex(right_hex)
    ).hexdigest()


def _validate_hex_leaves(leaf_hashes_hex: list[str]) -> None:
    for i, h in enumerate(leaf_hashes_hex):
        if not isinstance(h, str):
            raise TypeError(
                f"leaf_hashes_hex[{i}] must be str, got {type(h).__name__}"
            )
        try:
            bytes.fromhex(h)
        except ValueError as exc:
            raise ValueError(
                f"leaf_hashes_hex[{i}] is not valid hex: {h!r}"
            ) from exc


def compute_merkle_root_hex(leaf_hashes_hex: list[str]) -> str:
    """Compute the Merkle root over a list of leaf hashes (already domain-tagged).

    Convention: bottom-up pairing; if a level has odd count, the last node is
    duplicated (RFC 6962-style). Single-leaf list returns that leaf hash.
    Empty list raises ``ValueError`` — there is no canonical root for "no
    seed".
    """
    if not leaf_hashes_hex:
        raise ValueError("leaf_hashes_hex must contain at least one leaf")
    _validate_hex_leaves(leaf_hashes_hex)
    level: list[str] = list(leaf_hashes_hex)
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        next_level: list[str] = []
        for i in range(0, len(level), 2):
            next_level.append(_internal_hash_hex(level[i], level[i + 1]))
        level = next_level
    return level[0]


def compute_inclusion_proof(
    leaf_hashes_hex: list[str], leaf_index: int
) -> tuple[InclusionProofStep, ...]:
    """Build the inclusion proof for ``leaf_hashes_hex[leaf_index]``.

    Steps are ordered from leaf level upward. ``side`` says where the sibling
    sits relative to the current node at that level.
    """
    if not leaf_hashes_hex:
        raise ValueError("leaf_hashes_hex must contain at least one leaf")
    if not 0 <= leaf_index < len(leaf_hashes_hex):
        raise IndexError(
            f"leaf_index {leaf_index} out of range for {len(leaf_hashes_hex)} leaves"
        )
    _validate_hex_leaves(leaf_hashes_hex)
    proof: list[InclusionProofStep] = []
    level: list[str] = list(leaf_hashes_hex)
    idx = leaf_index
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        if idx % 2 == 0:
            sibling = level[idx + 1]
            proof.append(InclusionProofStep(sibling_hash_hex=sibling, side="right"))
        else:
            sibling = level[idx - 1]
            proof.append(InclusionProofStep(sibling_hash_hex=sibling, side="left"))
        next_level: list[str] = []
        for i in range(0, len(level), 2):
            next_level.append(_internal_hash_hex(level[i], level[i + 1]))
        level = next_level
        idx //= 2
    return tuple(proof)


def verify_inclusion(
    leaf_hash_hex: str,
    leaf_index: int,
    proof: tuple[InclusionProofStep, ...],
    expected_root_hex: str,
) -> bool:
    """Walk ``proof`` from leaf to root, return True iff result matches root."""
    current = leaf_hash_hex
    for step in proof:
        if step.side == "right":
            current = _internal_hash_hex(current, step.sibling_hash_hex)
        elif step.side == "left":
            current = _internal_hash_hex(step.sibling_hash_hex, current)
        else:
            return False
    return current == expected_root_hex


# ---------------------------------------------------------------------------
# Seed-vs-cache partition discovery on disk
# ---------------------------------------------------------------------------


def _walk_seed_partition(vault_shared_root: Path) -> set[str]:
    """Return relative paths of all SEED-partition files actually on disk.

    Cache-partition files (cached_opportunities/, research_db/ except
    research_db/seed/, any directory ending in /_cache/) are excluded
    via ``layout.is_seed_partition``.
    """
    seen: set[str] = set()
    for dirpath, dirnames, filenames in os.walk(vault_shared_root):
        # Stable iteration order (defence-in-depth; not load-bearing).
        dirnames.sort()
        filenames.sort()
        for fn in filenames:
            full = Path(dirpath) / fn
            try:
                rel = str(full.relative_to(vault_shared_root))
            except ValueError:
                continue
            if not is_seed_partition(rel):
                continue
            seen.add(rel)
    return seen


# ---------------------------------------------------------------------------
# freeze_vault_shared — boot-time Merkle pin
# ---------------------------------------------------------------------------


def freeze_vault_shared(
    *,
    manifest: VaultSharedSeedManifest,
    vault_shared_root: Path,
) -> VaultSharedFrozenRoot:
    """Verify the manifest against on-disk content and produce a frozen root.

    Steps:
    1. Sort manifest files by ``relative_path`` (canonical order).
    2. For each SeedFile:
       * Re-read the on-disk file.
       * Confirm SHA-3-512 of bytes matches ``SeedFile.content_hash``.
       * Re-capture ``identity_tuple`` via
         :func:`pipeline.vault.identity_tuple.resolve_identity_tuple` and
         compare the four filesystem fields (``volume_uuid``, ``fs_file_id``,
         ``mount_id``, ``fs_type``) against ``SeedFile.identity_tuple``.
         Drift raises :class:`SeedFileIdentityDrift` (F-M15-01) per §9
         step 6 — defence-in-depth against filesystem-layer substitution
         (bind-mount swap, mount-table manipulation).
    3. Confirm no extra files exist under the SEED partition that are not in
       the manifest (tamper evidence per §2.4).
    4. Compute Merkle root over canonical leaf hashes; assert it equals
       ``manifest.head_hash``.
    5. Build inclusion proofs for every seed path; return immutable
       ``VaultSharedFrozenRoot``.
    """
    if not isinstance(manifest, VaultSharedSeedManifest):
        raise TypeError(
            f"manifest must be VaultSharedSeedManifest, got {type(manifest).__name__}"
        )
    if not isinstance(vault_shared_root, Path):
        raise TypeError(
            f"vault_shared_root must be pathlib.Path, got "
            f"{type(vault_shared_root).__name__}"
        )

    sorted_files: tuple[SeedFile, ...] = tuple(
        sorted(manifest.files, key=lambda s: s.relative_path)
    )

    # Step 2 — content drift + identity-tuple drift check.
    # Identity-tuple re-capture closes the §9 step 6 defence-in-depth gap:
    # a content-hash match alone cannot detect a bind-mount-swap attack that
    # preserves the file's bytes but changes the underlying inode. Mirrors
    # the §2.5 invariant pattern already implemented in
    # :func:`verify_trust_root_mirror`.
    from pipeline.vault.identity_tuple import resolve_identity_tuple

    for sf in sorted_files:
        target = vault_shared_root / sf.relative_path
        if not target.is_file():
            raise SeedFileMissingOnDisk(
                f"seed file missing on disk: {sf.relative_path}"
            )
        try:
            actual_hash = hashlib.sha3_512(target.read_bytes()).hexdigest()
        except OSError as exc:
            raise SeedFileMissingOnDisk(
                f"seed file unreadable: {sf.relative_path}: {exc}"
            ) from exc
        if actual_hash != sf.content_hash:
            raise SeedFileContentDrift(
                f"seed file content drifted: {sf.relative_path} "
                f"expected={sf.content_hash[:16]}… actual={actual_hash[:16]}…"
            )
        # §9 step 6 — re-capture identity tuple + compare the four
        # filesystem-layer fields. Mirrors the §2.5 TrustRootMirror pattern.
        try:
            live_tuple = resolve_identity_tuple(target)
        except OSError as exc:
            raise SeedFileIdentityDrift(
                f"seed file identity tuple unresolvable: "
                f"{sf.relative_path}: {exc}"
            ) from exc
        if (
            live_tuple.volume_uuid != sf.identity_tuple.volume_uuid
            or live_tuple.fs_file_id != sf.identity_tuple.fs_file_id
            or live_tuple.mount_id != sf.identity_tuple.mount_id
            or live_tuple.fs_type != sf.identity_tuple.fs_type
        ):
            raise SeedFileIdentityDrift(
                f"seed file identity tuple drifted: {sf.relative_path}"
            )

    # Step 3 — extra-file check (tamper evidence).
    on_disk = _walk_seed_partition(vault_shared_root)
    listed = {sf.relative_path for sf in sorted_files}
    extras = on_disk - listed
    if extras:
        raise SeedFileExtraOnDisk(
            "unlisted seed-partition files: " + ", ".join(sorted(extras))
        )

    # Step 4 — Merkle root check.
    leaf_hashes = [
        compute_leaf_hash_hex(sf.relative_path, sf.content_hash)
        for sf in sorted_files
    ]
    computed_root = compute_merkle_root_hex(leaf_hashes)
    if computed_root != manifest.head_hash:
        raise SeedManifestHeadDrift(
            f"manifest head_hash {manifest.head_hash[:16]}… does not match "
            f"computed root {computed_root[:16]}…"
        )

    # Step 5 — build inclusion proofs.
    proofs = {
        sf.relative_path: compute_inclusion_proof(leaf_hashes, idx)
        for idx, sf in enumerate(sorted_files)
    }
    content_hashes = {sf.relative_path: sf.content_hash for sf in sorted_files}
    seed_paths = tuple(sf.relative_path for sf in sorted_files)

    return VaultSharedFrozenRoot(
        root_hex=computed_root,
        seed_paths=seed_paths,
        leaf_hashes_hex=tuple(leaf_hashes),
        inclusion_proofs=proofs,
        content_hashes_hex=content_hashes,
    )


# ---------------------------------------------------------------------------
# reverify_path — per-request Merkle re-walk
# ---------------------------------------------------------------------------


def reverify_path(
    *,
    frozen_root: VaultSharedFrozenRoot,
    vault_shared_root: Path,
    relative_path: str,
) -> bool:
    """Re-hash ``vault_shared_root/relative_path`` and walk its inclusion proof.

    Returns ``True`` iff (a) the path is in the frozen root's seed map AND
    (b) the on-disk content still matches the captured ``content_hash`` AND
    (c) the inclusion proof verifies against the pinned root.
    """
    if relative_path not in frozen_root.inclusion_proofs:
        return False
    target = vault_shared_root / relative_path
    if not target.is_file():
        return False
    try:
        live_bytes = target.read_bytes()
    except OSError:
        return False
    live_hash = hashlib.sha3_512(live_bytes).hexdigest()
    expected_hash = frozen_root.content_hashes_hex.get(relative_path)
    if expected_hash is None or live_hash != expected_hash:
        return False
    leaf_hash = compute_leaf_hash_hex(relative_path, live_hash)
    leaf_index = frozen_root.seed_paths.index(relative_path)
    proof = frozen_root.inclusion_proofs[relative_path]
    return verify_inclusion(leaf_hash, leaf_index, proof, frozen_root.root_hex)


# ---------------------------------------------------------------------------
# make_post_gate_hook — fd_broker post-gate adapter
# ---------------------------------------------------------------------------


def make_post_gate_hook(
    *,
    frozen_root: VaultSharedFrozenRoot,
    vault_shared_root: Path,
) -> Callable[[FDBrokerRequest], bool]:
    """Return a PostGateHook suitable for ``FDBroker.register_post_gate(...)``.

    Behaviour:
    * Requests for paths NOT under ``vault_shared/`` are out of scope → True.
    * Requests for paths under the CACHE partition are out of scope → True.
    * Requests for SEED-partition paths run the full inclusion re-verify; on
      mismatch the hook returns ``False`` so the broker vetoes FD issuance.
    """
    if not isinstance(frozen_root, VaultSharedFrozenRoot):
        raise TypeError(
            f"frozen_root must be VaultSharedFrozenRoot, got {type(frozen_root).__name__}"
        )
    if not isinstance(vault_shared_root, Path):
        raise TypeError(
            f"vault_shared_root must be pathlib.Path, got "
            f"{type(vault_shared_root).__name__}"
        )

    def _hook(request: FDBrokerRequest) -> bool:
        path = request.requested_path
        if not path.startswith(_VAULT_SHARED_PREFIX):
            return True
        rel = path[len(_VAULT_SHARED_PREFIX):]
        if not is_seed_partition(rel):
            return True
        return reverify_path(
            frozen_root=frozen_root,
            vault_shared_root=vault_shared_root,
            relative_path=rel,
        )

    return _hook


# ---------------------------------------------------------------------------
# verify_trust_root_mirror (§2.5)
# ---------------------------------------------------------------------------


def verify_trust_root_mirror(
    *,
    manifest: TrustRootMirrorManifest,
    live_mirror_path: Path,
    verify_signature: Callable[[bytes, str], bool],
    last_boot_wall_ns: int,
    current_boot_wall_ns: int,
    clock_rollback_tolerance_seconds: int,
) -> None:
    """Per §2.5 invariants — raise on failure, return None on success.

    `verify_signature(payload_bytes, signature_str) -> bool` is injected so
    this module does not bind to a specific keystore in v0.1. Round T's
    keystore-backed verifier will be wired in at the boot orchestrator level.
    """
    if not isinstance(manifest, TrustRootMirrorManifest):
        raise TypeError(
            f"manifest must be TrustRootMirrorManifest, got {type(manifest).__name__}"
        )
    if not isinstance(live_mirror_path, Path):
        raise TypeError(
            f"live_mirror_path must be pathlib.Path, got "
            f"{type(live_mirror_path).__name__}"
        )
    if not callable(verify_signature):
        raise TypeError("verify_signature must be callable")
    if not isinstance(last_boot_wall_ns, int):
        raise TypeError("last_boot_wall_ns must be int")
    if not isinstance(current_boot_wall_ns, int):
        raise TypeError("current_boot_wall_ns must be int")
    if not isinstance(clock_rollback_tolerance_seconds, int):
        raise TypeError("clock_rollback_tolerance_seconds must be int")

    # F-MIRROR-04 — immutability flag must have been set at manifest creation.
    if not manifest.immutability_flag_set:
        raise MirrorImmutabilityMissing(
            f"trust-root mirror immutability flag missing for {manifest.mirror_path}"
        )

    # F-MIRROR-05 — clock-rollback sanity check.
    tolerance_ns = clock_rollback_tolerance_seconds * 1_000_000_000
    if last_boot_wall_ns - current_boot_wall_ns > tolerance_ns:
        raise MirrorClockRollback(
            f"current boot wall {current_boot_wall_ns}ns is earlier than "
            f"last recorded {last_boot_wall_ns}ns by more than tolerance "
            f"{clock_rollback_tolerance_seconds}s"
        )

    # F-MIRROR-01 — identity tuple drift on the mirror file.
    from pipeline.vault.identity_tuple import resolve_identity_tuple

    live_tuple = resolve_identity_tuple(live_mirror_path)
    if (
        live_tuple.volume_uuid != manifest.identity_tuple.volume_uuid
        or live_tuple.fs_file_id != manifest.identity_tuple.fs_file_id
        or live_tuple.mount_id != manifest.identity_tuple.mount_id
        or live_tuple.fs_type != manifest.identity_tuple.fs_type
    ):
        raise MirrorIdentityMismatch(
            f"trust-root mirror identity tuple drifted for {manifest.mirror_path}"
        )

    # F-MIRROR-02 — content hash drift on the mirror file.
    try:
        body = live_mirror_path.read_bytes()
    except OSError as exc:
        raise MirrorContentMismatch(
            f"trust-root mirror unreadable: {live_mirror_path}: {exc}"
        ) from exc
    live_hash = hashlib.sha3_512(body).hexdigest()
    if live_hash != manifest.content_hash:
        raise MirrorContentMismatch(
            f"trust-root mirror content hash drifted for {manifest.mirror_path}"
        )

    # F-MIRROR-03 — operator signature must verify against the canonical
    # signed payload (content_hash, identity_tuple, m15_ledger_head).
    payload = json.dumps(
        {
            "content_hash": manifest.content_hash,
            "identity_tuple": {
                "captured_at": manifest.identity_tuple.captured_at,
                "fs_file_id": manifest.identity_tuple.fs_file_id,
                "fs_type": manifest.identity_tuple.fs_type,
                "mount_id": manifest.identity_tuple.mount_id,
                "volume_uuid": manifest.identity_tuple.volume_uuid,
            },
            "m15_ledger_head": manifest.m15_ledger_head,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    if not verify_signature(payload, manifest.operator_signature):
        raise MirrorSignatureInvalid(
            f"trust-root mirror operator signature failed for {manifest.mirror_path}"
        )

    return None


__all__ = [
    "LEAF_DOMAIN_TAG",
    "NODE_DOMAIN_TAG",
    "InclusionProofStep",
    "MirrorClockRollback",
    "MirrorContentMismatch",
    "MirrorIdentityMismatch",
    "MirrorImmutabilityMissing",
    "MirrorSignatureInvalid",
    "SeedFileContentDrift",
    "SeedFileExtraOnDisk",
    "SeedFileMissingOnDisk",
    "SeedManifestHeadDrift",
    "VaultSharedFrozenRoot",
    "canonical_leaf_bytes",
    "compute_inclusion_proof",
    "compute_leaf_hash_hex",
    "compute_merkle_root_hex",
    "freeze_vault_shared",
    "make_post_gate_hook",
    "reverify_path",
    "verify_inclusion",
    "verify_trust_root_mirror",
]
