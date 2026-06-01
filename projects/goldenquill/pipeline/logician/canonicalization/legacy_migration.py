"""Legacy KFR signature dual-verification mode (architecture v7.0.4-M1 §2.6).

Pre-M1 KFR files were signed under v7.0.4 §1.1's raw-YAML-bytes
contract.  Under M1, signatures cover canonical-JSON bytes (§2.2.1).
First M1 read of a pre-M1 KFR would otherwise fail-closed with
``F-KFR-CANONICAL-SIGNATURE-INVALID``, blocking deployments that
already have populated KFRs.

This module ships the migration-mode primitives:

* :class:`MigrationState` — dataclass mirroring the on-disk
  ``orgs/<slug>/vault/kfr/_migration_state.yaml`` shape per §2.6.2.
* :func:`load_migration_state` / :func:`serialize_migration_state` —
  parse/render helpers that go through the canonicalization-disciplined
  loader.
* :func:`verify_kfr_signature_with_migration` — the dual-verification
  helper a Logician PRE-gate calls when ``legacy_accept_mode`` is
  ``enabled``.  Tries canonical-JSON first; falls back to raw-YAML iff
  legacy-accept mode is enabled.

Re-enabling ``legacy_accept_mode`` from ``disabled``/``completed`` to
``enabled`` is a tamper event guarded by
``F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED`` — that gate lives in
:mod:`pipeline.logician.gates.f_kfr_legacy_accept_re_enabled_unsigned`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Final, Literal, Optional

from pipeline.logician.canonicalization.kfr_canonical import (
    CANONICALIZATION_SCHEMA_VERSION,
    canonical_dump,
)
from pipeline.logician.canonicalization.kfr_safe_loader import (
    KfrConstructError,
    load_kfr_safe_bytes,
)


MIGRATION_STATE_SCHEMA_VERSION: Final[str] = "kfr_migration_state.v1"

LEGACY_ACCEPT_ENABLED: Final[str] = "enabled"
LEGACY_ACCEPT_DISABLED: Final[str] = "disabled"
LEGACY_ACCEPT_COMPLETED: Final[str] = "completed"

_PERMITTED_MODES: Final[frozenset[str]] = frozenset({
    LEGACY_ACCEPT_ENABLED,
    LEGACY_ACCEPT_DISABLED,
    LEGACY_ACCEPT_COMPLETED,
})

LegacyAcceptMode = Literal["enabled", "disabled", "completed"]


@dataclass(frozen=True, kw_only=True)
class MigrationState:
    """On-disk migration-state shape per §2.6.2."""

    org_slug: str
    legacy_accept_mode: str  # one of LEGACY_ACCEPT_*
    migration_started_at_utc: str
    migration_completed_at_utc: Optional[str] = None
    operator_key_id_at_migration: str
    entries_migrated: int = 0
    entries_pending: int = 0
    audit_chain: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.legacy_accept_mode not in _PERMITTED_MODES:
            raise ValueError(
                f"legacy_accept_mode={self.legacy_accept_mode!r} not in "
                f"{sorted(_PERMITTED_MODES)!r}"
            )
        if not self.org_slug.strip():
            raise ValueError("org_slug must be non-empty")
        if not self.migration_started_at_utc.strip():
            raise ValueError("migration_started_at_utc must be non-empty ISO-8601")
        if not self.operator_key_id_at_migration.strip():
            raise ValueError("operator_key_id_at_migration must be non-empty")
        if self.entries_migrated < 0 or self.entries_pending < 0:
            raise ValueError("entry counts must be non-negative")


def load_migration_state(data: bytes) -> MigrationState:
    """Parse migration-state bytes under :class:`KfrSafeLoader`.

    Raises :class:`KfrConstructError` on YAML construct issues, or
    :class:`ValueError` on schema mismatch.
    """
    try:
        parsed = load_kfr_safe_bytes(data)
    except KfrConstructError:
        raise
    if not isinstance(parsed, dict):
        raise ValueError(
            f"migration-state expected mapping, got {type(parsed).__name__}"
        )
    if parsed.get("schema_version") != MIGRATION_STATE_SCHEMA_VERSION:
        raise ValueError(
            f"migration-state schema_version mismatch: expected "
            f"{MIGRATION_STATE_SCHEMA_VERSION!r}, got "
            f"{parsed.get('schema_version')!r}"
        )
    audit_chain_raw = parsed.get("audit_chain") or []
    if not isinstance(audit_chain_raw, list):
        raise ValueError("audit_chain must be a list of strings")
    return MigrationState(
        org_slug=str(parsed["org_slug"]),
        legacy_accept_mode=str(parsed["legacy_accept_mode"]),
        migration_started_at_utc=str(parsed["migration_started_at_utc"]),
        migration_completed_at_utc=(
            str(parsed["migration_completed_at_utc"])
            if parsed.get("migration_completed_at_utc") is not None
            else None
        ),
        operator_key_id_at_migration=str(parsed["operator_key_id_at_migration"]),
        entries_migrated=int(parsed.get("entries_migrated", 0)),
        entries_pending=int(parsed.get("entries_pending", 0)),
        audit_chain=tuple(str(row) for row in audit_chain_raw),
    )


def serialize_migration_state(state: MigrationState) -> bytes:
    """Render migration-state to canonical-JSON bytes for signing.

    The on-disk file format is YAML for operator readability, but the
    signature surface (audit_chain entries) signs canonical-JSON bytes
    per §2.2.1.  This helper is the single source of truth for the
    signing surface.
    """
    payload: dict[str, Any] = {
        "schema_version": MIGRATION_STATE_SCHEMA_VERSION,
        "canonicalization": CANONICALIZATION_SCHEMA_VERSION,
        "org_slug": state.org_slug,
        "legacy_accept_mode": state.legacy_accept_mode,
        "migration_started_at_utc": state.migration_started_at_utc,
        "migration_completed_at_utc": state.migration_completed_at_utc,
        "operator_key_id_at_migration": state.operator_key_id_at_migration,
        "entries_migrated": state.entries_migrated,
        "entries_pending": state.entries_pending,
        "audit_chain": list(state.audit_chain),
    }
    return canonical_dump(payload)


CanonicalVerifyCallable = Callable[[bytes, bytes, bytes], bool]
"""Ed25519 verifier signature: (message_bytes, signature, public_key) → bool.

Mirrors :class:`pipeline.logician.gates._protocols.SignatureVerifyCallable`
to avoid a hard import dependency from the canonicalization layer.
"""


@dataclass(frozen=True, kw_only=True)
class DualVerifyResult:
    """Result of canonical-then-legacy dual verification."""

    success: bool
    used_legacy_path: bool
    detail: str


def verify_kfr_signature_with_migration(
    *,
    canonical_bytes: bytes,
    raw_yaml_bytes: bytes,
    signature: bytes,
    public_key: bytes,
    legacy_accept_mode: str,
    canonical_verify: CanonicalVerifyCallable,
    legacy_verify: Optional[CanonicalVerifyCallable] = None,
) -> DualVerifyResult:
    """§2.6.1 dual-verification helper.

    Tries canonical-JSON verification first.  When it fails AND
    ``legacy_accept_mode == "enabled"``, falls back to raw-YAML
    verification (legacy v7.0.4 §1.1 path).  When ``legacy_verify`` is
    None, ``canonical_verify`` is reused on the raw-YAML bytes (most
    deployments use the same Ed25519 verifier; the parameter is provided
    so tests can inject distinct primitives).
    """
    if legacy_accept_mode not in _PERMITTED_MODES:
        return DualVerifyResult(
            success=False,
            used_legacy_path=False,
            detail=(
                f"legacy_accept_mode={legacy_accept_mode!r} not one of "
                f"{sorted(_PERMITTED_MODES)!r}"
            ),
        )

    try:
        canonical_ok = canonical_verify(canonical_bytes, signature, public_key)
    except Exception as exc:  # noqa: BLE001 — fail-closed
        canonical_ok = False
        canonical_detail = (
            f"canonical-verify raised {type(exc).__name__}: {exc}"
        )
    else:
        canonical_detail = (
            "canonical-verify succeeded"
            if canonical_ok
            else "canonical-verify returned False"
        )

    if canonical_ok:
        return DualVerifyResult(
            success=True,
            used_legacy_path=False,
            detail=canonical_detail,
        )

    if legacy_accept_mode != LEGACY_ACCEPT_ENABLED:
        return DualVerifyResult(
            success=False,
            used_legacy_path=False,
            detail=(
                f"{canonical_detail}; legacy_accept_mode="
                f"{legacy_accept_mode!r} → fail-closed without legacy fallback"
            ),
        )

    verifier = legacy_verify or canonical_verify
    try:
        legacy_ok = verifier(raw_yaml_bytes, signature, public_key)
    except Exception as exc:  # noqa: BLE001 — fail-closed
        return DualVerifyResult(
            success=False,
            used_legacy_path=True,
            detail=(
                f"{canonical_detail}; legacy-verify raised "
                f"{type(exc).__name__}: {exc}"
            ),
        )
    if legacy_ok:
        return DualVerifyResult(
            success=True,
            used_legacy_path=True,
            detail=(
                f"{canonical_detail}; legacy raw-YAML signature accepted "
                "(operator must re-sign at next SP0 per §2.6.1)"
            ),
        )
    return DualVerifyResult(
        success=False,
        used_legacy_path=True,
        detail=(
            f"{canonical_detail}; legacy raw-YAML verify also returned False"
        ),
    )


__all__ = [
    "CanonicalVerifyCallable",
    "DualVerifyResult",
    "LEGACY_ACCEPT_COMPLETED",
    "LEGACY_ACCEPT_DISABLED",
    "LEGACY_ACCEPT_ENABLED",
    "LegacyAcceptMode",
    "MIGRATION_STATE_SCHEMA_VERSION",
    "MigrationState",
    "load_migration_state",
    "serialize_migration_state",
    "verify_kfr_signature_with_migration",
]
