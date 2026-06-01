// pipeline/vault/policies/kfr_canonical.cedar
// SKELETON — paired with the Python implementation at
// pipeline/logician/canonicalization/kfr_canonical.py +
// pipeline/logician/canonicalization/kfr_safe_loader.py.
//
// Architecture authority:
//   - architecture v7.0.4-M1 §2 (CF-RT-01 closure)
//   - blueprint section_04_v2_x_amendment.md §6 row M1-1, M1-2
//
// Lifecycle note: at v0.1, the Python predicates are authoritative;
// this Cedar policy file is the human-auditable surface.  Any drift
// between this file and the Python implementation is the audit
// finding surface.
//
// Denies surface as:
//   F-KFR-YAML-CONSTRUCT-FORBIDDEN.<construct_class>
//   F-KFR-CANONICAL-SIGNATURE-INVALID
//   F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED

// Rule 1 — kfr_canonical_load_allowed
// Permits a KFR file load when no forbidden YAML construct is present
// AND the SafeLoader subclass refused nothing at construction time.
permit (
  principal,
  action == VaultAction::"kfr-load",
  resource
)
when {
  resource has yaml_constructs_present &&
  resource.yaml_constructs_present == false &&
  resource has canonicalization &&
  resource.canonicalization == "kfr_canonical.v1"
};

// Rule 2 — kfr_canonical_signature_verifies
// Permits a KFR entry read when the Ed25519 signature verifies on the
// canonical-JSON bytes (post §2.2.1 pipeline).
permit (
  principal,
  action == VaultAction::"kfr-read",
  resource
)
when {
  resource has signature_surface &&
  resource.signature_surface == "canonical_json" &&
  resource has signature_verified &&
  resource.signature_verified == true
};

// Rule 3 — kfr_legacy_accept_dual_verify
// Permits dual-verification (canonical-JSON, then raw-YAML legacy
// fallback) ONLY when legacy_accept_mode is enabled AND the operator
// has acknowledged migration via _migration_state.yaml.
permit (
  principal,
  action == VaultAction::"kfr-read",
  resource
)
when {
  resource has legacy_accept_mode &&
  resource.legacy_accept_mode == "enabled" &&
  resource has migration_state_signed &&
  resource.migration_state_signed == true &&
  resource has signature_verified &&
  resource.signature_verified == true
};
