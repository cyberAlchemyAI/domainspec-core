// §13 Data Collector — beneficiary_records PII discipline policy.
//
// Per §2 v7.2 LOCKED PII discipline (§2.3 sub-kind = beneficiary_records;
// HIGH PII classification) + §13.5.4 operational-data sub-kind writes +
// §13.16.2 RT-28 closure + §13.16.6.2 RT-C2-10 enum validation. The
// principal is the Data Collector seat invocation; the resource is a
// BeneficiaryRecord write; the action is Write.
//
// PERMIT path. A Data Collector seat invocation may write a
// BeneficiaryRecord only when ALL of the following hold:
//   * the calling principal is the data_collector_seat (Law 3 — no
//     other seat may write beneficiary_records), AND
//   * the resource carries a non-empty `consent_tier` field, AND
//   * the resource.consent_tier value is in the v7.0.5 §6 enumerated
//     literal set: {my_eyes_only, matchable_to_opportunities,
//     composable_with_others}, AND
//   * the resource.org_slug matches the calling principal's
//     invocation_org_slug.
//
// FORBID path. Writes that miss `consent_tier` OR carry an out-of-enum
// consent_tier value OR cross org boundaries fail-closed at the Cedar
// layer. Composes with AST-lint R-DATACOLLECTOR-BENEFICIARY-CONSENT-
// TIER-REQUIRED (compile-time) + Logician gate
// F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER (POST-write).
//
// READ path. Per §2 v7.2 §13.5.4 PII discipline: reads of beneficiary
// records are governed by Cedar attribute matching on consent_tier;
// `my_eyes_only` records are readable only by the data_collector_seat
// and intake_seat under invocation_org_slug = resource.org_slug.

permit (
    principal == DataCollectorSeat,
    action == Write,
    resource is BeneficiaryRecord
) when {
    principal.seat_id == "data_collector_seat" &&
    resource.consent_tier in ["my_eyes_only", "matchable_to_opportunities", "composable_with_others"] &&
    resource.org_slug == principal.invocation_org_slug
};

forbid (
    principal,
    action == Write,
    resource is BeneficiaryRecord
) unless {
    resource.consent_tier == "my_eyes_only" ||
    resource.consent_tier == "matchable_to_opportunities" ||
    resource.consent_tier == "composable_with_others"
};

forbid (
    principal == DataCollectorSeat,
    action == Read,
    resource is BeneficiaryRecord
) unless {
    principal.invocation_org_slug == resource.org_slug
};
