// pipeline/logician/cedar_policies/compound_commit.cedar
// SKELETON — NOT YET DEPLOYED. Accompanies pipeline/logician/compound_commit.py
// (also not yet on disk; cited in gpp_det_report_2026-04-19 as blueprint-pinned,
// target-missing). Section 4 v2.1 LOCK 2026-04-19 is the authoring event.
//
// Blueprint authority:
//   - Section 4 v2.1 §4.11 (compound-commit predicate + Cedar companion)
//   - Section 2 v7.1 §4.10.5 (signed compound-kind registry; references this file)
//   - Section 4 v2.1 §6.13 (failure-code family)
//   - Section 4 v2.1 §9.8 (test vectors 9.8.1-9.8.4)
//
// Lifecycle note — asymmetry with vault_shared/cedar/*.cedar:
//   This file is a CODE-side Cedar policy. It is NOT loaded by
//   pipeline/vault/m15_ledger.py::cedar_policy_loader_load_all (which only
//   walks top-level cedar/*.cedar under the frozen vault_shared partition).
//   It is loaded by the Section 4 CedarEvaluator at Section-4 module boot
//   and is covered by the code-tree integrity surface (AST lint + the
//   signed blueprint hash that covers pipeline/blueprint/v0.1/section_04*),
//   not by the M15 seed-manifest ledger. Changes here require a new
//   Section 4 LOCK cycle, not an M15.3 operator re-type.
//
// Denies surface as:
//   F-CEDAR-COMPOUND-DENIED.unknown_kind     — resource not in v0.1 enumeration
//   F-CEDAR-COMPOUND-DENIED.predicate_denied — context booleans unsatisfied
//
// Principal: Section 2 vault dispatcher (only seat permitted to commit a
// compound transaction). Action: commit_compound_txn (the §4.10.7 entry
// point). Resource: the enumerated CompoundTxnKind set; v0.1 = exactly
// {index_amendment}. Additional compound kinds (e.g. eventual
// report-submission, content-vertical publish) require a Section 4 LOCK
// cycle to add a new permit rule below — the v0.1 enumeration is a lock,
// not a default.
//
// Context booleans (all three must be true): these flags are the stored
// outcomes of the first three phases of compound_commit_predicate
// (Counter-equality over staged_writes, stored-equality over hash
// bindings, session_id match). Cedar does not re-derive them; it
// affirmatively signs off on them as the fourth and final commit gate.

permit (
  principal in Seat::"Dispatcher",
  action == VaultAction::"commit_compound_txn",
  resource == CompoundTxn::"index_amendment"
)
when {
  context.required_intents_present == true &&
  context.hash_bindings_valid == true &&
  context.session_matches == true
};
