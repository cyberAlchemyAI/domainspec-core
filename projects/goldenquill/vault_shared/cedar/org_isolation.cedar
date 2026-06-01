// vault_shared/cedar/org_isolation.cedar
// SKELETON — NOT YET SIGNED. M15 signed-commit + M15.3 HIGH-severity admin-risk
// ledger entry required before this file is load-bearing at boot.
//
// Blueprint authority:
//   - Section 2 v7.1 §2.6 (Cedar entity shapes)
//   - Section 2 v7.1 §3 (seed-file ledger: `vault_shared/cedar/org_isolation.cedar`)
//   - Section 4 v2.1 §4.2.1 row #17 (PRE-gate compile check, M14)
//   - Section 4 v2.1 §4.2.1 row #4 (PRE-gate signature + ledger-head check)
//
// Load path (boot, §9 step 9):
//   pipeline/vault/m15_ledger.py::cedar_policy_loader_load_all reads this file
//   from the frozen vault_shared partition, re-hashes SHA-3-512 against the
//   pinned VaultSharedFrozenRoot.content_hashes_hex, returns the text to
//   Section 4 CedarEvaluator. Any drift → CedarPolicyLoadFailed (F-CEDAR-01)
//   → hard abort.
//
// Fallback evaluator (Python, authoritative at v0.1 until this file is M15-sealed):
//   pipeline/logician/cedar_eval.py::evaluate_org_isolation
//
// Denies surface as:
//   F-CEDAR-01.org_isolation_deny  (see cedar_eval.py)
//
// Cedar is default-deny; below are two `permit` rules that together model the
// Python evaluator semantics:
//   1. any resource flagged is_shared (vault_shared/ subtree) permits both
//      read and write for any session principal.
//   2. any resource whose org_slug_hint matches the session principal's
//      org_slug permits both read and write.
// Anything else → deny → F-CEDAR-01.org_isolation_deny.
//
// The compile check in pipeline/logician/cedar_eval.py::compile_cedar_policy
// requires at least one `permit` or `forbid` effect keyword; both rules below
// satisfy that surface.

// Rule 1 — shared vault access. vault_shared/ is Law-3-neutral by design
// (seed policies, calibration artifacts, cached opportunities manifests).
permit (
  principal,
  action in [VaultAction::"read", VaultAction::"write"],
  resource
)
when {
  resource has is_shared &&
  resource.is_shared == true
};

// Rule 2 — same-org access. A session bound to org_slug S may read/write
// any VaultPath whose org_slug_hint is S. Enforcement is belt-and-suspenders
// with Section 2's canonical_path-vs-org_root filesystem check; Cedar handles
// the fast path and the human-auditable rule surface.
permit (
  principal,
  action in [VaultAction::"read", VaultAction::"write"],
  resource
)
when {
  principal has org_slug &&
  resource has org_slug_hint &&
  principal.org_slug == resource.org_slug_hint
};
