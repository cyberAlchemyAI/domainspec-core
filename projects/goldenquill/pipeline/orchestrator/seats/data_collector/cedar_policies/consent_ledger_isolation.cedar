// §13 Data Collector — consent ledger isolation policy.
//
// Per §13.5.3 pseudocode + §13.16.1 RT-06 + RT-08 + §13.10.3 cross-org
// isolation. The principal is the Data Collector seat invocation; the
// resource is a ConsentLedgerEntry; permitted actions are read + write.
//
// PERMIT path. A Data Collector seat invocation may read OR write a
// ConsentLedgerEntry only when:
//   * the entry's org_slug matches the invocation's org_slug
//     (Law 3 — Org Isolation), AND
//   * the entry's channel is in the invocation's channels_in_scope,
//     AND
//   * the entry's recipient_id is in the invocation's
//     recipient_id_list.
//
// FORBID path. Any access where principal.invocation_org_slug !=
// resource.org_slug fail-closes at the Cedar layer (cross-org leak
// guard); the Python predicate layer additionally fail-closes via
// F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.path_cross_org (defense in
// depth).
//
// Wire form (Cedar grammar):

permit (
    principal == DataCollectorSeat,
    action in [ConsentLedgerRead, ConsentLedgerWrite],
    resource is ConsentLedgerEntry
) when {
    resource.org_slug == principal.invocation_org_slug &&
    resource.channel in principal.invocation_channels_in_scope &&
    resource.recipient_id in principal.invocation_recipient_id_list
};

forbid (
    principal == DataCollectorSeat,
    action in [ConsentLedgerRead, ConsentLedgerWrite],
    resource is ConsentLedgerEntry
) unless {
    principal.invocation_org_slug == resource.org_slug
};
