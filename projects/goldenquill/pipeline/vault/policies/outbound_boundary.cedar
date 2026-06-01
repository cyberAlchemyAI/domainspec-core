// pipeline/vault/policies/outbound_boundary.cedar
// Companion code to §4 v2.x.5 amendment (LOCKED 2026-05-16 row 232).
// CC-007 closure — Cedar second-layer defense for F-CLASS outbound boundary.
//
// Blueprint authority:
//   - section_04_v2_x_5_provider_boundary_amendment.md §5 (Cedar policy)
//   - section_04_v2_x_5_provider_boundary_amendment.md §11.4 (RT-20 + RT-21
//     fold-in: runtime Cedar load + split_context.cedar include)
//   - section_04_v2_x_5_provider_boundary_amendment.md §12.7 (RT-C2-05 +
//     RT-21 PARTIAL closure: include precedence pin)
//
// Lifecycle:
//   Loaded at startup by pipeline.logician.cedar_engine._load_cedar_policy.
//   Load failure → _CEDAR_LOAD_SUCCEEDED=False → wrapper invocation
//   fail-closed with F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.cedar_load_failure
//   (§12.6 RT-C2-04). This file is the second-layer defense; the Python
//   wrapper at provider_boundary.py::enforce_outbound_boundary is the
//   first-layer.
//
// Denies surface as:
//   F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_classification_deny
//     (PRE-class refusals: Local-Only / missing context / confidential input /
//      payload-commitment mismatch / runtime-integrity fail)
//   F-CLASS-POSTURE-MID-CYCLE-CHANGE.outbound_boundary_posture_mismatch
//     (envelope posture vs register posture mismatch)
//
// Cedar is default-deny. The single forbid rule below models the Python
// wrapper's combined PRE refusal surface; any drift between this rule and
// provider_boundary.py is the F-CEDAR-CONSISTENCY-DIVERGENCE audit-finding
// surface (RT-20 + Cycle 2 §12.6 contract).

// RT-21 fold-in: compose with v7.0.10 §5.3 split-context Cedar rules.
// Cedar's `include` semantics under the project's pinned Cedar 3.x
// vocabulary: include directives appear BEFORE forbid clauses so first-
// match-forbid evaluates last in textual order. The include is documentary
// here — the Python evaluator pre-merges policies at load time.
// (Cedar reference implementations vary on include semantics; this file
// is parsed by pipeline.logician.cedar_engine which composes both files
// in-memory.)
//
// include "split_context.cedar"

// Rule 1 — outbound_boundary_combined_forbid
// Forbids http_egress under any of the wrapper's PRE refusal conditions.
// The Python evaluator at pipeline.logician.cedar_engine.evaluate_outbound_
// boundary_cedar populates the resource attributes from the wrapper's
// runtime state before evaluation; any True attribute fires this forbid.
forbid (
  principal,
  action == Action::"http_egress",
  resource
)
when {
  // Local-Only posture refuses cloud egress structurally.
  (resource has posture && resource.posture == "local_only_sovereign") ||

  // PRE-2 missing classification context.
  (!(resource has classification_context_provided)) ||
  (resource has classification_context_provided &&
   resource.classification_context_provided == false) ||

  // PRE-2a (RT-01 + §12.4): runtime identity pin failed.
  (resource has runtime_integrity_failed &&
   resource.runtime_integrity_failed == true) ||

  // PRE-2c (RT-05): payload sha3-512 commitment mismatch.
  (resource has payload_sha3_512_commitment_mismatch &&
   resource.payload_sha3_512_commitment_mismatch == true) ||

  // PRE-2b (RT-07): envelope posture vs signed register posture mismatch.
  (resource has posture_mismatch_with_register &&
   resource.posture_mismatch_with_register == true) ||

  // PRE-3 confidential / operator_flagged input class.
  (resource has classified_input_classes &&
   (resource.classified_input_classes.contains("confidential") ||
    resource.classified_input_classes.contains("operator_flagged")))
};

// Rule 2 — outbound_boundary_split_context_forbid
// Under split_context_hybrid posture, the allow-list miss + applicant-fact
// leak scan are second-layer-enforced here. The Python wrapper's
// _enforce_pre composes the v7.0.10 §5.3 predicate chain; this rule
// duplicates the gate for Cedar-second-layer-defense.
forbid (
  principal,
  action == Action::"http_egress",
  resource
)
when {
  resource has posture &&
  resource.posture == "split_context_hybrid" &&
  ((resource has split_context_allowlist_miss &&
    resource.split_context_allowlist_miss == true) ||
   (resource has split_context_applicant_fact_leak &&
    resource.split_context_applicant_fact_leak == true))
};
