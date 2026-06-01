"""KFR canonicalization layer (architecture v7.0.4-M1 §2).

Three modules:

* :mod:`pipeline.logician.canonicalization.kfr_canonical` — deterministic
  canonical-JSON serializer per §2.2.1.
* :mod:`pipeline.logician.canonicalization.kfr_safe_loader` — SafeLoader
  subclass rejecting YAML constructs forbidden by §2.2.2 (anchors, aliases,
  merge-keys, custom tags).
* :mod:`pipeline.logician.canonicalization.legacy_migration` — pre-M1 KFR
  signature dual-verification mode + ``_migration_state.yaml`` shape per §2.6.
"""

from pipeline.logician.canonicalization.kfr_canonical import (
    CANONICALIZATION_SCHEMA_VERSION,
    CanonicalizationError,
    canonical_dump,
    canonicalize,
)
from pipeline.logician.canonicalization.kfr_safe_loader import (
    KFR_FORBIDDEN_TAGS,
    KfrConstructError,
    KfrSafeLoader,
    load_kfr_safe,
    load_kfr_safe_bytes,
)
from pipeline.logician.canonicalization.legacy_migration import (
    LEGACY_ACCEPT_DISABLED,
    LEGACY_ACCEPT_ENABLED,
    MIGRATION_STATE_SCHEMA_VERSION,
    LegacyAcceptMode,
    MigrationState,
    load_migration_state,
    serialize_migration_state,
    verify_kfr_signature_with_migration,
)

__all__ = [
    "CANONICALIZATION_SCHEMA_VERSION",
    "CanonicalizationError",
    "KFR_FORBIDDEN_TAGS",
    "KfrConstructError",
    "KfrSafeLoader",
    "LEGACY_ACCEPT_DISABLED",
    "LEGACY_ACCEPT_ENABLED",
    "LegacyAcceptMode",
    "MIGRATION_STATE_SCHEMA_VERSION",
    "MigrationState",
    "canonical_dump",
    "canonicalize",
    "load_kfr_safe",
    "load_kfr_safe_bytes",
    "load_migration_state",
    "serialize_migration_state",
    "verify_kfr_signature_with_migration",
]
