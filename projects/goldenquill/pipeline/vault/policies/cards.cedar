// pipeline/vault/policies/cards.cedar
//
// Cedar policies for the Card Cartridge System.
// Per blueprint §4 v2.x card-hardening §4.X.2.
//
// v7.0.11 LOCK ships:
//   - Rule 0: LIVE — META-gate body realization (F-CARDS-COVERAGE-INCOMPLETE).
//   - Rules 1-8: BINDING-placeholder; full Cedar conditions land at v0.2 first
//     wave alongside §4 v2.x card-hardening predicate-body graduation.
//
// Mirrors pipeline/vault/policies/reflection_packet.cedar pattern (LOCKED 2026-05-15
// row 222) byte-for-byte for the LIVE-META + 7-BINDING-placeholder shape.

// Rule 0 — LIVE — F-CARDS-COVERAGE-INCOMPLETE META gate body.
// Permits cartridge load only when (a) module + test coverage check passed AND
// (b) either coverage is complete OR environment is development OR missing
// fields are nonessential / forward-compat.
permit (
  principal == Cartridge::Loader,
  action == Action::"LoadCartridge",
  resource is Cartridge
) when {
  resource.module_coverage_complete == true &&
  (resource.cartridge_field_coverage_complete == true ||
   context.environment == "development" ||
   resource.missing_fields_all_nonessential_or_forward_compat == true)
};

// Rule 1 — BINDING-placeholder — F-CARDS-SCHEMA-INVALID.
// Full Cedar condition body lands at v0.2 first wave alongside f_cards_schema_invalid.py predicate body.
forbid (
  principal,
  action == Action::"LoadCartridge",
  resource is Cartridge
) when {
  resource.schema_valid == false
};

// Rule 2 — BINDING-placeholder — F-CARDS-UNSIGNED-PRODUCTION-LOAD.
forbid (
  principal,
  action == Action::"LoadCartridge",
  resource is Cartridge
) when {
  context.environment == "production" &&
  resource.signature_status != "signed"
};

// Rule 3 — BINDING-placeholder — F-CARDS-SIGNATURE-INVALID.
forbid (
  principal,
  action == Action::"LoadCartridge",
  resource is Cartridge
) when {
  context.environment == "production" &&
  resource.signature_verification_passed == false
};

// Rule 4 — BINDING-placeholder — F-CARDS-PRIVATE-DATA-IN-CARTRIDGE.
forbid (
  principal,
  action == Action::"LoadCartridge",
  resource is Cartridge
) when {
  resource.contains_private_org_data == true
};

// Rule 5 — BINDING-placeholder — F-CARDS-CROSS-ORG-NAMESPACE-LEAK.
forbid (
  principal,
  action == Action::"RetrieveFromMemory",
  resource is MemoryNamespace
) when {
  context.requesting_org_slug != context.target_org_slug &&
  resource.namespace_prefix == "orgs:" &&
  context.retrieval_mode != "explicit_allowlist"
};

// Rule 6 — BINDING-placeholder — F-CARDS-COUPLING-VIOLATION-EXTENSION.
forbid (
  principal,
  action == Action::"LoadCartridge",
  resource is Cartridge
) when {
  resource.contains_forbidden_coupling_field == true
};

// Rule 7 — BINDING-placeholder — F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY.
forbid (
  principal,
  action == Action::"ReadCartridgeField",
  resource is CartridgeField
) when {
  context.read_context in ["eligibility_evaluation", "fit_gating", "opportunity_ranking", "opportunity_exclusion"] &&
  resource.cartridge_axis == "MATRIX" &&
  context.reader_identity in ["Scout", "Scribe", "Judge", "Logician_as_evaluator"]
};

// Rule 8 — BINDING-placeholder — F-CARDS-LOAD-IN-WRONG-NAMESPACE.
forbid (
  principal,
  action == Action::"LoadCartridge",
  resource is Cartridge
) when {
  resource.declared_axis != context.target_namespace_axis
};
