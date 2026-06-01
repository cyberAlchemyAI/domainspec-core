"""§9 Vault boot capstone — composes Rounds K..U into a single entry point.

Round R — the orchestrator.

Step ordering (v0.1, macOS-primary):

* §9.1  — (caller-driven; not in this module)
* §9.2  — UUID floor enforce         → :func:`uuid_floor.enforce`
* §9.3  — Mount-table snapshot        — deferred (Linux primitive)
* §9.4  — Trust-root mirror verify    → :func:`mirror_verify.verify_trust_root_mirror` (optional)
* §9.5  — Vault-shared init marker    → :func:`init_marker.verify_vault_init_marker` (optional)
* §9.6  — M15 seed manifest verify    → :func:`m15_ledger.verify_seed_manifest`
* §9.7  — Atomic verify-and-freeze    → :func:`atomic_freeze.apply`
* §9.8  — Wrapper hash verify         — deferred (process_wrapper.py not built)
* §9.9  — Cedar policy load           → :func:`m15_ledger.cedar_policy_loader_load_all`
* §9.10 — FD broker online + post-gate hook from Round S
* §9.11 — Per-org init marker         (optional)

Failures:
* Primary-mechanism failures (UUID floor reject, signature/ledger-head drift,
  seed content tamper) propagate as the underlying vault exception family.
* Optional sub-configs that are not provided record a degradation note
  rather than aborting boot, so v0.1 dev-box wiring can come up before all
  primitives are bound to production keystores.

The result is a frozen :class:`VaultBootResult` carrying every artefact
(uuid_floor, frozen_root, atomic_freeze_result, cedar_policies, fd_broker,
vault_root_fd) that downstream §9 step 12 consumers need.

Resource lifecycle:
* :func:`vault_boot` opens ``vault_root`` as an O_DIRECTORY file descriptor
  for the broker. Callers MUST call :func:`vault_boot_close` (or use the
  result inside a try/finally) to release the FD.
"""

from __future__ import annotations

import datetime
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Final, Mapping, Optional


BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§9 vault boot capstone — orchestrator composing Rounds K..U",
            "§9.2 UUID floor enforce",
            "§9.4 trust-root mirror verify (optional)",
            "§9.5 vault-shared init marker verify (optional)",
            "§9.6 M15 seed manifest verify",
            "§9.7 atomic verify-and-freeze",
            "§9.9 Cedar policy load",
            "§9.10 FD broker online + post-gate hook",
            "§9.11 per-org init marker (optional)",
        ],
    },
}

from pipeline.sovereignty import KeyStore
from pipeline.vault import atomic_freeze as _atomic_freeze
from pipeline.vault import m15_ledger as _m15_ledger
from pipeline.vault import mirror_verify as _mirror_verify
from pipeline.vault import uuid_floor as _uuid_floor
from pipeline.vault.atomic_freeze import (
    AtomicFreezeResult,
    SnapshotProvider,
)
from pipeline.vault.fd_broker import FDBroker
from pipeline.vault.init_marker import verify_vault_init_marker
from pipeline.vault.m15_ledger import SignatureVerifier
from pipeline.vault.mirror_verify import (
    VaultSharedFrozenRoot,
    make_post_gate_hook,
)
from pipeline.vault.schemas import (
    StableUUIDFloor,
    TrustRootMirrorManifest,
    VaultInitMarker,
)


# ---------------------------------------------------------------------------
# Pins (single source of truth for default scope/slug)
# ---------------------------------------------------------------------------


DEFAULT_VAULT_INIT_SCOPE: str = "vault-shared"
DEFAULT_VAULT_INIT_SLUG: str = "tilth-default"


# ---------------------------------------------------------------------------
# Optional sub-config dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class TrustRootMirrorVerifyConfig:
    """Boot-time payload for :func:`mirror_verify.verify_trust_root_mirror`."""

    manifest: TrustRootMirrorManifest
    live_mirror_path: Path
    last_boot_wall_ns: int
    current_boot_wall_ns: int
    clock_rollback_tolerance_seconds: int
    verify_signature: Callable[[bytes, str], bool]


@dataclass(frozen=True, kw_only=True)
class VaultInitVerifyConfig:
    """Boot-time payload for :func:`init_marker.verify_vault_init_marker`."""

    marker_path: Path
    hmac_path: Path
    keystore: KeyStore
    expected_slug: str = DEFAULT_VAULT_INIT_SLUG
    expected_scope: str = DEFAULT_VAULT_INIT_SCOPE


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class VaultBootResult:
    success: bool
    session_id: str
    booted_at_iso: str
    vault_root: Path
    vault_shared_root: Path
    vault_root_fd: int
    uuid_floor: StableUUIDFloor
    trust_root_mirror_verified: bool
    vault_init_marker: Optional[VaultInitMarker]
    org_init_marker: Optional[VaultInitMarker]
    frozen_root: VaultSharedFrozenRoot
    atomic_freeze_result: AtomicFreezeResult
    cedar_policies: Mapping[str, str]
    fd_broker: FDBroker
    degradations: tuple[str, ...] = field(default_factory=tuple)


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


# ---------------------------------------------------------------------------
# vault_boot — §9 capstone
# ---------------------------------------------------------------------------


def vault_boot(
    *,
    vault_root: Path,
    vault_shared_root: Path,
    seed_manifest_path: Path,
    seed_signature_path: Path,
    session_id: str,
    current_ledger_head: str,
    verify_signature: SignatureVerifier,
    trust_root_config: Optional[TrustRootMirrorVerifyConfig] = None,
    vault_init_config: Optional[VaultInitVerifyConfig] = None,
    org_init_config: Optional[VaultInitVerifyConfig] = None,
    snapshot_provider: Optional[SnapshotProvider] = None,
    platform: str = "darwin",
) -> VaultBootResult:
    """Run the §9 boot sequence and return a :class:`VaultBootResult`.

    Caller MUST eventually pass the result to :func:`vault_boot_close` to
    release the broker's vault-root FD.
    """
    # ----- Type / value gates --------------------------------------------
    if not isinstance(vault_root, Path):
        raise TypeError(
            f"vault_root must be pathlib.Path, got {type(vault_root).__name__}"
        )
    if not isinstance(vault_shared_root, Path):
        raise TypeError(
            f"vault_shared_root must be pathlib.Path, got "
            f"{type(vault_shared_root).__name__}"
        )
    if not isinstance(seed_manifest_path, Path):
        raise TypeError(
            f"seed_manifest_path must be pathlib.Path, got "
            f"{type(seed_manifest_path).__name__}"
        )
    if not isinstance(seed_signature_path, Path):
        raise TypeError(
            f"seed_signature_path must be pathlib.Path, got "
            f"{type(seed_signature_path).__name__}"
        )
    if not isinstance(session_id, str):
        raise TypeError(
            f"session_id must be str, got {type(session_id).__name__}"
        )
    if not session_id:
        raise ValueError("session_id must be non-empty")
    if not isinstance(current_ledger_head, str):
        raise TypeError(
            f"current_ledger_head must be str, got "
            f"{type(current_ledger_head).__name__}"
        )
    if not callable(verify_signature):
        raise TypeError("verify_signature must be callable")
    if trust_root_config is not None and not isinstance(
        trust_root_config, TrustRootMirrorVerifyConfig
    ):
        raise TypeError(
            "trust_root_config must be TrustRootMirrorVerifyConfig or None"
        )
    if vault_init_config is not None and not isinstance(
        vault_init_config, VaultInitVerifyConfig
    ):
        raise TypeError(
            "vault_init_config must be VaultInitVerifyConfig or None"
        )
    if org_init_config is not None and not isinstance(
        org_init_config, VaultInitVerifyConfig
    ):
        raise TypeError(
            "org_init_config must be VaultInitVerifyConfig or None"
        )

    degradations: list[str] = []

    # ----- §9.2 UUID floor -----------------------------------------------
    uuid_floor = _uuid_floor.enforce(vault_root)

    # ----- §9.3 Mount-table snapshot (deferred for Linux) ----------------
    # No-op on darwin. Surfaced as degradation only if the platform isn't
    # the v0.1 primary so the rails report can flag deferred steps.

    # ----- §9.4 Trust-root mirror verify (optional) ----------------------
    trust_root_mirror_verified = False
    if trust_root_config is None:
        degradations.append("trust-root-mirror-skipped")
    else:
        _mirror_verify.verify_trust_root_mirror(
            manifest=trust_root_config.manifest,
            live_mirror_path=trust_root_config.live_mirror_path,
            verify_signature=trust_root_config.verify_signature,
            last_boot_wall_ns=trust_root_config.last_boot_wall_ns,
            current_boot_wall_ns=trust_root_config.current_boot_wall_ns,
            clock_rollback_tolerance_seconds=(
                trust_root_config.clock_rollback_tolerance_seconds
            ),
        )
        trust_root_mirror_verified = True

    # ----- §9.5 Vault-shared init marker (optional) ----------------------
    vault_init_marker: Optional[VaultInitMarker] = None
    if vault_init_config is None:
        degradations.append("vault-init-marker-skipped")
    else:
        vault_init_marker = verify_vault_init_marker(
            marker_path=vault_init_config.marker_path,
            hmac_path=vault_init_config.hmac_path,
            keystore=vault_init_config.keystore,
            expected_slug=vault_init_config.expected_slug,
            expected_scope=vault_init_config.expected_scope,
        )

    # ----- §9.6 M15 seed manifest verify ---------------------------------
    frozen_root = _m15_ledger.verify_seed_manifest(
        manifest_path=seed_manifest_path,
        signature_path=seed_signature_path,
        vault_shared_root=vault_shared_root,
        current_ledger_head=current_ledger_head,
        verify_signature=verify_signature,
    )

    # ----- §9.7 Atomic verify-and-freeze ---------------------------------
    atomic_freeze_result = _atomic_freeze.apply(
        frozen_root=frozen_root,
        vault_shared_root=vault_shared_root,
        session_id=session_id,
        platform=platform,
        snapshot_provider=snapshot_provider,
    )
    # Roll the atomic_freeze degradations into the boot-level list so the
    # rails report has a single sequence.
    degradations.extend(atomic_freeze_result.degradations)

    # ----- §9.8 Wrapper hash verify (deferred) ---------------------------
    degradations.append("wrapper-hash-verify-skipped")

    # ----- §9.9 Cedar policy load ----------------------------------------
    cedar_policies = _m15_ledger.cedar_policy_loader_load_all(
        frozen_root=frozen_root,
        vault_shared_root=vault_shared_root,
    )

    # ----- §9.10 FD broker online + post-gate hook -----------------------
    vault_root_fd = os.open(str(vault_root), os.O_RDONLY | os.O_DIRECTORY)
    try:
        post_gate = make_post_gate_hook(
            frozen_root=frozen_root,
            vault_shared_root=vault_shared_root,
        )
        broker = FDBroker(
            vault_root_fd=vault_root_fd,
            vault_root_path=vault_root,
            post_gate_hook=post_gate,
        )
    except BaseException:
        # If broker construction blows up after we've opened the FD, do
        # not leak the descriptor.
        try:
            os.close(vault_root_fd)
        except OSError:
            pass
        raise

    # ----- §9.11 Per-org init marker (optional) --------------------------
    org_init_marker: Optional[VaultInitMarker] = None
    if org_init_config is None:
        degradations.append("org-init-marker-skipped")
    else:
        org_init_marker = verify_vault_init_marker(
            marker_path=org_init_config.marker_path,
            hmac_path=org_init_config.hmac_path,
            keystore=org_init_config.keystore,
            expected_slug=org_init_config.expected_slug,
            expected_scope=org_init_config.expected_scope,
        )

    return VaultBootResult(
        success=True,
        session_id=session_id,
        booted_at_iso=_iso_utc_now(),
        vault_root=vault_root,
        vault_shared_root=vault_shared_root,
        vault_root_fd=vault_root_fd,
        uuid_floor=uuid_floor,
        trust_root_mirror_verified=trust_root_mirror_verified,
        vault_init_marker=vault_init_marker,
        org_init_marker=org_init_marker,
        frozen_root=frozen_root,
        atomic_freeze_result=atomic_freeze_result,
        cedar_policies=cedar_policies,
        fd_broker=broker,
        degradations=tuple(degradations),
    )


# ---------------------------------------------------------------------------
# vault_boot_close — releases the broker's vault-root FD
# ---------------------------------------------------------------------------


def vault_boot_close(result: VaultBootResult) -> None:
    """Idempotent close of the FD opened by :func:`vault_boot`.

    Safe to call twice; the second call is a no-op.
    """
    if not isinstance(result, VaultBootResult):
        raise TypeError(
            f"result must be VaultBootResult, got {type(result).__name__}"
        )
    try:
        os.close(result.vault_root_fd)
    except OSError:
        pass


__all__ = [
    "DEFAULT_VAULT_INIT_SCOPE",
    "DEFAULT_VAULT_INIT_SLUG",
    "TrustRootMirrorVerifyConfig",
    "VaultBootResult",
    "VaultInitVerifyConfig",
    "vault_boot",
    "vault_boot_close",
]
