// §13 Data Collector — audit redaction policy.
//
// Per §13.5.1 outbound log + §13.5.2 inbound log + §13.10.3 cross-org
// isolation. The principal here is a workspace-wide audit consumer
// (operator-facing audit dump, cross-org reconciliation tooling, or
// the Logfire span exporter); the resource is a Data Collector audit
// entry that carries a `recipient_id` field. The action is Read.
//
// PERMIT path. An audit consumer may read a Data Collector audit
// entry only when:
//   * the consumer's invocation_org_slug matches the audit entry's
//     org_slug (same-org audit; full recipient_id visible), OR
//   * the consumer is operating under a redaction-required posture
//     (cross-org reconciliation tooling, Logfire span exporter), in
//     which case the recipient_id MUST be presented as
//     `recipient_<hashed_first_8_chars>` rather than the canonical
//     recipient_id. The hashing function is SHA3-256 over the
//     canonical recipient_id; the first 8 hex chars are surfaced.
//
// FORBID path. Cross-org audit reads that do NOT carry the
// redaction-required posture fail-closed at the Cedar layer. The
// caller's redact_recipient_id_required attribute is set by the
// invocation context (Logfire exporter sets it to true; same-org
// operator-facing audit dump sets it to false).

permit (
    principal == DataCollectorAuditConsumer,
    action == Read,
    resource is DataCollectorAuditEntry
) when {
    resource.org_slug == principal.invocation_org_slug
};

permit (
    principal == DataCollectorAuditConsumer,
    action == Read,
    resource is DataCollectorAuditEntry
) when {
    principal.redact_recipient_id_required == true &&
    resource.recipient_id_presentation == "hashed_first_8_chars"
};

forbid (
    principal == DataCollectorAuditConsumer,
    action == Read,
    resource is DataCollectorAuditEntry
) unless {
    resource.org_slug == principal.invocation_org_slug ||
    (principal.redact_recipient_id_required == true &&
     resource.recipient_id_presentation == "hashed_first_8_chars")
};
