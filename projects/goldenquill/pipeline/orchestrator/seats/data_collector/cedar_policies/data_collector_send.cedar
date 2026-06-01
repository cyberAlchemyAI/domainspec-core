// §13 Data Collector — send authorization policy.
//
// Per §13.7 Layer 3 (four-layer defense against silent-auto-send) and
// §13.16.1 RT-06 + RT-26 closure. The principal is the Data Collector
// seat invocation; the resource is an OutboundMessage staged for
// dispatch; the only permitted action is Send.
//
// PERMIT path. A Data Collector seat invocation may dispatch an
// OutboundMessage only when ALL of the following hold:
//   * the calling principal carries
//     `operator_batch_signature_verified == true` (the Layer-2
//     dispatcher signature check has succeeded), AND
//   * the calling principal's invocation_org_slug matches the
//     OutboundMessage.org_slug (Law 3 + RT-C2-01 binding), AND
//   * the calling principal's invocation_grant_id matches the
//     OutboundMessage.grant_id (RT-C2-01 binding), AND
//   * the calling principal's caller_module is
//     "pipeline.orchestrator.seats.data_collector.outbound_batch"
//     (mirrors the R-DATACOLLECTOR-NO-AUTOSEND Layer-1 compile-time
//     enforcement at the Cedar policy layer for defense in depth),
//     AND
//   * the calling principal's mtproto_session_path (when channel ==
//     telegram) contains the org_slug substring (RT-26 closure;
//     Cedar enforces structurally — Python predicate layer raises
//     RuntimeError + admin-risk ledger entry).
//
// FORBID path. Any send without operator_batch_signature_verified ==
// true fail-closes at the Cedar layer.

permit (
    principal == DataCollectorSeat,
    action == Send,
    resource is OutboundMessage
) when {
    principal.operator_batch_signature_verified == true &&
    resource.org_slug == principal.invocation_org_slug &&
    resource.grant_id == principal.invocation_grant_id &&
    principal.caller_module == "pipeline.orchestrator.seats.data_collector.outbound_batch"
};

forbid (
    principal == DataCollectorSeat,
    action == Send,
    resource is OutboundMessage
) unless {
    principal.operator_batch_signature_verified == true
};

// RT-26 — MTProto session path MUST contain org_slug for telegram channel.
forbid (
    principal == DataCollectorSeat,
    action == Send,
    resource is OutboundMessage
) when {
    resource.channel == "telegram" &&
    !(principal.mtproto_session_path like ("*" + principal.invocation_org_slug + "*"))
};
