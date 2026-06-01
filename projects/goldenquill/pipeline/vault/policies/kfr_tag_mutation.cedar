// pipeline/vault/policies/kfr_tag_mutation.cedar
// SKELETON — paired with pipeline/logician/gates/f_kfr_tag_modified.py
// (and the atomic-read discipline in
// pipeline/logician/gates/f_kfr_path_symlink_forbidden.py).
//
// Architecture authority:
//   - architecture v7.0.4-M1 §4 (CF-RT-04 closure)
//   - architecture v7.0.4-M1 §4.2.2 (Cycle-2 RT-05 atomic-read)
//   - blueprint section_04_v2_x_amendment.md §6 row M1-4, M1-5
//
// Denies surface as:
//   F-KFR-TAG-MODIFIED
//   F-KFR-PATH-SYMLINK-FORBIDDEN
//
// Tracked metadata fields per §4.2:
//   - required_for_category, required_for_funder, key_credentials.

// Rule 1 — tag_mutation_with_signed_ledger
// Permits KFR write that mutates tracked tag fields ONLY when an
// admin-risk-ledger row of kind ``kfr_tag_modified`` carries the
// matching tag_set_hash_before/after pair AND operator signature.
permit (
  principal,
  action == VaultAction::"kfr-tag-mutate",
  resource
)
when {
  resource has tag_set_hash_before &&
  resource has tag_set_hash_after &&
  resource has ledger_row_present &&
  resource.ledger_row_present == true &&
  resource has operator_signed &&
  resource.operator_signed == true
};

// Rule 2 — kfr_atomic_read_disciplined
// Permits KFR read pair (KFR file + ledger entry) ONLY when neither
// path is a symlink AND the read happened under shared advisory
// lock with O_NOFOLLOW.
permit (
  principal,
  action == VaultAction::"kfr-atomic-read",
  resource
)
when {
  resource has kfr_path_is_symlink &&
  resource.kfr_path_is_symlink == false &&
  resource has ledger_path_is_symlink &&
  resource.ledger_path_is_symlink == false &&
  resource has shared_lock_held &&
  resource.shared_lock_held == true &&
  resource has open_nofollow &&
  resource.open_nofollow == true
};
