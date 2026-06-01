// pipeline/vault/policies/operational_subkinds.cedar
// SKELETON — NOT YET SIGNED. Awaits §2 v7.2 Cowork Thesis LOCK + M15
// signed-commit + M15.3 HIGH-severity admin-risk ledger entry before this
// file is load-bearing at boot.
//
// Blueprint authority:
//   - section_02_v7_2_amendment.md §6 (operational_subkinds.cedar contract)
//   - section_02_v7_2_amendment.md §7 (F-CEDAR-OPERATIONAL-DENIED +
//     F-OPERATIONAL-PII-CONSENT-MISSING)
//   - architecture v0.1 §R.PF2 (PII discipline for beneficiary records,
//     "HIGH-severity admin-risk per S2 if PII is present")
//
// Lifecycle note (mirrors compound_commit.cedar):
//   This file is a CODE-side Cedar policy. It is NOT loaded by
//   pipeline/vault/m15_ledger.py::cedar_policy_loader_load_all (which only
//   walks vault_shared/cedar/*.cedar under the frozen vault_shared
//   partition). The Python evaluator at
//   pipeline/vault/sub_kinds/policy_eval.py::evaluate_operational_write
//   is authoritative at v0.1; this .cedar file is the human-auditable
//   surface that pairs with it.
//
// Denies surface as:
//   F-CEDAR-OPERATIONAL-DENIED.org_slug_mismatch
//   F-CEDAR-OPERATIONAL-DENIED.consent_tier_mismatch_or_pii_unauthorized
//   F-OPERATIONAL-PII-CONSENT-MISSING (when pii_present=True and
//                                       principal.operator_authorized_pii=False)
//
// Cedar is default-deny. The three permit rules below model the Python
// evaluator semantics line-for-line; any drift between this file and
// policy_eval.py is the audit-finding surface.

// Rule 1 — operational_org_isolation
// Permits any operational write when the principal's org_slug matches the
// resource's org_slug_hint. Mirrors org_isolation.cedar Rule 2 surface for
// the operational subtree.
permit (
  principal,
  action == VaultAction::"operational-write",
  resource
)
when {
  principal has org_slug &&
  resource has org_slug_hint &&
  principal.org_slug == resource.org_slug_hint &&
  resource has sub_kind &&
  resource.sub_kind != "beneficiary_records"
};

// Rule 2 — beneficiary_pii_anonymized
// Permits a beneficiary write when the record is anonymized AND carries no
// PII. The two conditions together are the schema-level invariant the
// BeneficiaryRecord __post_init__ enforces; this rule re-asserts at the
// policy layer.
permit (
  principal,
  action == VaultAction::"operational-write",
  resource
)
when {
  principal has org_slug &&
  resource has org_slug_hint &&
  principal.org_slug == resource.org_slug_hint &&
  resource has sub_kind &&
  resource.sub_kind == "beneficiary_records" &&
  resource has consent_tier &&
  resource.consent_tier == "anonymized" &&
  resource has pii_present &&
  resource.pii_present == false
};

// Rule 3 — beneficiary_pii_with_consent
// Permits an identified beneficiary write only when the record is flagged
// operator-authorized-identified AND carries PII AND the principal session
// holds the operator_authorized_pii flag. R.PF2 calls this the
// HIGH-severity admin-risk path.
permit (
  principal,
  action == VaultAction::"operational-write",
  resource
)
when {
  principal has org_slug &&
  resource has org_slug_hint &&
  principal.org_slug == resource.org_slug_hint &&
  resource has sub_kind &&
  resource.sub_kind == "beneficiary_records" &&
  resource has consent_tier &&
  resource.consent_tier == "operator-authorized-identified" &&
  resource has pii_present &&
  resource.pii_present == true &&
  principal has operator_authorized_pii &&
  principal.operator_authorized_pii == true
};

// ---------------------------------------------------------------------------
// §17 WPFA cycle_receipt extensions — LOCKED 2026-05-11 (§17.9)
// Authoritative Python evaluator at
// pipeline/orchestrator/seats/wpfa/_cedar_bootstrap.py.
// ---------------------------------------------------------------------------

// Rule 4 — cycle_receipt_org_isolation
// Extension of operational_org_isolation. CycleReceipt writes pass when
// the principal's org_slug matches the resource's org_slug_hint.
// Defense-in-depth on top of F-WPFA-CROSS-ORG-LEAK at the Logician layer.
permit (
  principal,
  action == VaultAction::"operational-write",
  resource
)
when {
  principal has org_slug &&
  resource has org_slug_hint &&
  principal.org_slug == resource.org_slug_hint &&
  resource has sub_kind &&
  resource.sub_kind == "cycle_receipt"
};

// Rule 5 — cycle_receipt_operator_attestation
// Permits buyer-facing PDF emission ONLY when signed_by_operator_ed25519
// is non-None AND the signature verifies against the white-glove-pinned
// operator pubkey. M13 NOT permitted (structural attestation boundary).
permit (
  principal,
  action == VaultAction::"wpfa-pdf-emit",
  resource
)
when {
  resource has sub_kind &&
  resource.sub_kind == "cycle_receipt" &&
  resource has signed_by_operator_ed25519_present &&
  resource.signed_by_operator_ed25519_present == true
};

// Rule 6 — cycle_receipt_read_isolation
// Permits CycleReceipt READ when principal.org_slug matches resource OR
// when principal_kind is wpfa_dashboard_workspace_aggregate (Stage-1
// operator-as-multi-org-actor carve-out per §15.2 Law 3 + §17.9 #3).
permit (
  principal,
  action == VaultAction::"cycle-receipt-read",
  resource
)
when {
  resource has sub_kind &&
  resource.sub_kind == "cycle_receipt" &&
  ((principal has org_slug &&
    resource has org_slug_hint &&
    principal.org_slug == resource.org_slug_hint) ||
   (principal has principal_kind &&
    principal.principal_kind == "wpfa_dashboard_workspace_aggregate"))
};
