import {canonicalJson, digestValue, fail, freezeResult, isRecord, nonEmptyString} from "./canonical.mjs";

export const PROTOCOL_VERSION = "2.0";
export const TURN_START = "turn/start";
export const TURN_STARTED = "turn/started";
export const TURN_COMPLETED = "turn/completed";
export const EFFECT_METHODS = Object.freeze([
  "item/commandExecution/requestApproval",
  "item/fileChange/requestApproval",
  "item/permissions/requestApproval",
]);
export const EVIDENCE_METHODS = Object.freeze([
  TURN_STARTED,
  "item/started",
  "item/completed",
  "hook/started",
  "hook/completed",
  TURN_COMPLETED,
]);
export const CONTEXT_KEY = "cyberalchemy.are.context-basis";
export const CONTEXT_ITEM_KEY_PREFIX = "cyberalchemy.are.context-item/";
export const DIRECTIVE_NOTIFICATION = "cyberalchemy/decision";
export const SUCCESSOR_NOTIFICATION = "cyberalchemy/successor";
export const SEMANTIC_NOTIFICATION = "cyberalchemy/semantic";

export function classifyMessage(message) {
  if (!isRecord(message) || (message.jsonrpc !== undefined && message.jsonrpc !== PROTOCOL_VERSION)) return "invalid";
  if (nonEmptyString(message.method)) return Object.hasOwn(message, "id") ? "request" : "notification";
  if (Object.hasOwn(message, "id") && (Object.hasOwn(message, "result") || Object.hasOwn(message, "error"))) return "response";
  return "invalid";
}

export function admitJsonRpcMessage(message) {
  const kind = classifyMessage(message);
  if (kind === "invalid") return fail("json-rpc", ["protocol.invalid-json-rpc-message"]);
  return freezeResult({ok: true, kind, value: message, message_digest: digestValue(message), authority_effect: "none"});
}

export function parseJsonLine(line) {
  try {
    return admitJsonRpcMessage(JSON.parse(line));
  } catch {
    return fail("json-rpc", ["protocol.invalid-json"]);
  }
}

export function jsonLine(message) {
  return `${JSON.stringify(message)}\n`;
}

export function jsonRpcError(id, code, message, data) {
  return freezeResult({jsonrpc: PROTOCOL_VERSION, id: id ?? null, error: {code, message, data}});
}

export function directiveNotification(directive) {
  return freezeResult({jsonrpc: PROTOCOL_VERSION, method: DIRECTIVE_NOTIFICATION, params: directive});
}

export function successorNotification(payload) {
  return freezeResult({jsonrpc: PROTOCOL_VERSION, method: SUCCESSOR_NOTIFICATION, params: payload});
}

export function semanticNotification(payload) {
  return freezeResult({jsonrpc: PROTOCOL_VERSION, method: SEMANTIC_NOTIFICATION, params: payload});
}

export function extractTurnIdentity(message) {
  const params = isRecord(message?.params) ? message.params : {};
  const turn = isRecord(params.turn) ? params.turn : {};
  return {
    thread_id: params.threadId ?? null,
    turn_id: params.turnId ?? turn.id ?? null,
    item_id: params.itemId ?? null,
    approval_id: params.approvalId ?? message?.id ?? null,
  };
}

export function contextFragment(lifecycle) {
  const composition = lifecycle.composition;
  const envelope = lifecycle.context_envelope.value;
  const refresh = lifecycle.refresh_assessment.value;
  const route = composition.value.route_decision;
  const basis = composition.value.necessary_context_basis;
  const view = composition.value.context_window_view;
  const allExclusions = envelope.exclusions ?? [];
  const exclusions = allExclusions.filter((entry) => entry.reason !== "not-selected" && !String(entry.reason ?? "").startsWith("diagnostic-only-"));
  return freezeResult({
    schema_version: "are.codex-context-fragment/v2",
    request_context_digest: route.request_context_digest,
    decision_profile_digest: route.decision_profile_digest,
    decision_digest: route.decision_digest,
    route_id: route.selected.route_id,
    capability_ref: route.selected.capability_ref,
    basis_digest: basis.digest,
    view_id: view.value.view_id,
    view_lane: view.value.lane,
    context_epoch_id: envelope.context_epoch_id,
    context_envelope_digest: lifecycle.context_envelope.digest,
    freshness_state: envelope.freshness_state,
    refresh_disposition: refresh.disposition,
    inline_bytes: envelope.inline_bytes,
    max_inline_bytes: envelope.max_inline_bytes,
    included_items: envelope.included_items,
    exclusions,
    exclusion_count: allExclusions.length,
    omitted_diagnostic_exclusion_count: allExclusions.length - exclusions.length,
    exclusions_digest: digestValue(allExclusions),
    contradictions: envelope.contradictions,
    gaps: envelope.gaps,
    residue: envelope.residue,
    claim_ceiling: envelope.claim_ceiling,
    authority_effect: "none",
  });
}

export function addContextFragment(message, fragment) {
  const params = isRecord(message.params) ? message.params : {};
  const additionalContext = isRecord(params.additionalContext) ? params.additionalContext : {};
  const includedItems = Array.isArray(fragment.included_items) ? fragment.included_items : [];
  const {included_items: _IncludedItems, ...fragmentFields} = fragment;
  const manifest = {
    ...fragmentFields,
    schema_version: "are.codex-context-manifest/v1",
    context_fragment_schema_version: fragment.schema_version,
    included_item_count: includedItems.length,
    included_item_refs: includedItems.map((item) => ({
      context_item_id: item.context_item_id,
      item_digest: item.item_digest,
      item_kind: item.item_kind,
    })),
  };
  const itemFragments = Object.fromEntries(includedItems.map((item) => [
    `${CONTEXT_ITEM_KEY_PREFIX}${item.context_item_id}`,
    {kind: "application", value: canonicalJson(item)},
  ]));
  return freezeResult({
    ...message,
    params: {
      ...params,
      additionalContext: {
        ...additionalContext,
        [CONTEXT_KEY]: {kind: "application", value: canonicalJson(manifest)},
        ...itemFragments,
      },
    },
  });
}

export function denyApprovalResult(method) {
  if (method === "item/commandExecution/requestApproval" || method === "item/fileChange/requestApproval") {
    return freezeResult({decision: "decline"});
  }
  if (method === "item/permissions/requestApproval") {
    return freezeResult({permissions: {}, scope: "turn", strictAutoReview: true});
  }
  return null;
}

export function approvalAccepted(method, result) {
  if (!isRecord(result)) return false;
  if (method === "item/commandExecution/requestApproval" || method === "item/fileChange/requestApproval") {
    return result.decision === "accept"
      || result.decision === "acceptForSession"
      || isRecord(result.decision?.acceptWithExecpolicyAmendment)
      || isRecord(result.decision?.applyNetworkPolicyAmendment);
  }
  if (method === "item/permissions/requestApproval") {
    if (!isRecord(result.permissions)) return false;
    const fileSystem = result.permissions.fileSystem;
    const network = result.permissions.network;
    return (isRecord(fileSystem) && Object.keys(fileSystem).length > 0)
      || (isRecord(network) && Object.keys(network).length > 0);
  }
  return false;
}

export function protocolBindingCheck(binding, observedVersion) {
  const reasons = [];
  if (!isRecord(binding)) reasons.push("protocol.binding-required");
  else {
    if (binding.observed_codex_version !== observedVersion) reasons.push("protocol.codex-version-drift");
    if (!nonEmptyString(binding.interface_sha256)) reasons.push("protocol.interface-digest-required");
    if (!nonEmptyString(binding.selected_projection_sha256)) reasons.push("protocol.projection-digest-required");
    if (!nonEmptyString(binding.observation_sha256)) reasons.push("protocol.observation-digest-required");
  }
  if (reasons.length > 0) return fail("protocol-binding", reasons);
  return freezeResult({ok: true, binding, authority_effect: "none"});
}
