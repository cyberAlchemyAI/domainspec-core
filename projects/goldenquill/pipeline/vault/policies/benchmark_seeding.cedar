// pipeline/vault/policies/benchmark_seeding.cedar
// SKELETON — paired with pipeline/logician/benchmarks/cross_check.py +
// pipeline/logician/benchmarks/seeding_allowlist_loader.py.
//
// Architecture authority:
//   - architecture v7.0.4-M1 §5 (DC-CF-04 closure)
//   - architecture v7.0.4-M1 §5.2.3 (RT-09 allowlist signature)
//   - blueprint section_04_v2_x_amendment.md §6 row M1-9, M1-10, M1-11
//
// Denies surface as:
//   F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING
//   F-BENCHMARK-SEEDING-SOURCE-UNAUTHORIZED
//   F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID

// Rule 1 — benchmark_seed_authorized
// Permits a benchmark seed ONLY when source_doc matches the
// SN-LLC seeding allowlist (signed Ed25519 + canonical-JSON).
permit (
  principal,
  action == VaultAction::"benchmark-seed",
  resource
)
when {
  resource has allowlist_signature_verified &&
  resource.allowlist_signature_verified == true &&
  resource has source_doc_authorized &&
  resource.source_doc_authorized == true
};

// Rule 2 — benchmark_cross_check_audited
// Permits a benchmark cross-check fire ONLY when both the placeholder
// row and the result row are durably committed to the audit log.
permit (
  principal,
  action == VaultAction::"benchmark-cross-check",
  resource
)
when {
  resource has placeholder_row_present &&
  resource.placeholder_row_present == true &&
  resource has result_row_present &&
  resource.result_row_present == true &&
  resource has constant_time_compare &&
  resource.constant_time_compare == true
};

// Rule 3 — benchmark_seeding_allowlist_signed
// Permits the loader to read the SN-LLC seeding allowlist when the
// Ed25519 signature is verified AND the canonicalization version
// pins to kfr_canonical.v1.
permit (
  principal,
  action == VaultAction::"benchmark-allowlist-load",
  resource
)
when {
  resource has signature_verified &&
  resource.signature_verified == true &&
  resource has canonicalization &&
  resource.canonicalization == "kfr_canonical.v1"
};
