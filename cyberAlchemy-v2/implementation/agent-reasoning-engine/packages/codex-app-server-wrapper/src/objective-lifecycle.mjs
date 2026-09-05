import {materializeObjectiveState, resolveObjectiveTransition, verifyObjectiveState, digestIntentMaterial} from "../../request-intent-runtime/index.mjs";
import {canonicalJson, digestValue, freezeResult, isRecord, nonEmptyString} from "./canonical.mjs";
import {selectObjectiveMeanings} from "./objective-meanings.mjs";

export const OBJECTIVE_CONTEXT_KEY = "cyberalchemy.are.objective";
const EVENT = "objective-transition-resolved";
const keyFor = (consumer, scope) => canonicalJson([consumer, scope]);
const requestKey = (consumer, scope, request) => digestValue([consumer, scope, request]);

// Interpretation history only: an objective is not a completion or permission.
export function createCodexObjectiveLifecycle({ledger, profile_id, configuration = {}, provider}) {
  const states = new Map(), requests = new Map();
  let fault = false;
  const scopeFor = thread => canonicalJson([profile_id, thread]);
  for (const event of ledger.snapshot()) {
    if (event.event_kind !== EVENT) continue;
    const resolution = event.content?.resolution;
    const next = resolution?.next_state;
    const {resolution_digest, ...material} = resolution ?? {};
    const meaningSelection = event.content?.meaning_selection;
    if (meaningSelection) {
      const {selection_digest, ...selectionMaterial} = meaningSelection;
      if (digestValue(selectionMaterial) !== selection_digest || meaningSelection.selected_context_digest !== resolution?.selected_context_digest
        || meaningSelection.authority_effect !== "none") throw new TypeError("Invalid recovered objective meaning selection");
    }
    if (!verifyObjectiveState(next) || resolution?.disposition !== "resolved" || digestIntentMaterial(material) !== resolution_digest
      || next.last_request?.request_ref !== resolution.request_ref || next.last_request?.request_digest !== resolution.request_digest
      || next.predecessor_state_digest !== resolution.previous_state_digest || resolution.authority_effect !== "none") throw new TypeError("Invalid recovered objective transition");
    const key = keyFor(next.consumer_ref, next.scope_ref);
    const previous = states.get(key) ?? materializeObjectiveState({consumer_ref: next.consumer_ref, scope_ref: next.scope_ref});
    if (previous.state_digest !== resolution.previous_state_digest) throw new TypeError("Recovered objective transition chain diverges");
    states.set(key, next);
    const replayKey = requestKey(next.consumer_ref, next.scope_ref, resolution.request_ref);
    if (requests.has(replayKey)) throw new TypeError("Duplicate recovered objective request");
    requests.set(replayKey, resolution);
  }
  return {
    async prepare(message, binding, loadSources = null) {
      if (configuration.enabled !== true) return {ok: true, disposition: "disabled", resolution: null};
      if (fault) return {ok: false, reason_codes: ["objective.ledger-write-failed-restart-required"]};
      if (!isRecord(message.params) || !nonEmptyString(message.params.threadId) || !Array.isArray(message.params.input)
        || message.params.input.some(item => !isRecord(item)) || !nonEmptyString(binding?.consumer_ref)
        || !["string", "number"].includes(typeof message.id)) return {ok: false, reason_codes: ["objective.codex-request-invalid"]};
      const consumer = binding.consumer_ref, scope = scopeFor(message.params.threadId);
      const request = (message.params.input ?? []).filter(item => item.type === "text" && typeof item.text === "string").map(item => item.text.trim()).join("\n");
      const requestRef = `codex-objective:${canonicalJson(message.params.clientUserMessageId ?? message.id)}`;
      const replayKey = requestKey(consumer, scope, requestRef);
      const priorRequest = requests.get(replayKey);
      if (priorRequest) return {ok: false, disposition: "replayed", reason_codes: [priorRequest.request_digest === digestIntentMaterial(request)
        ? "objective.request-already-recorded-dispatch-not-retried" : "objective.request-identity-conflict"], resolution: priorRequest};
      const key = keyFor(consumer, scope), state = states.get(key);
      const input = {request, request_ref: requestRef, consumer_ref: consumer, scope_ref: scope,
        ...(state ? {state, expected_state_digest: state.state_digest} : {}), provider_timeout_ms: configuration.provider_timeout_ms ?? 1000};
      let selection = null;
      let resolution;
      if (configuration.meaning_selection && typeof provider === "function") {
        resolution = await resolveObjectiveTransition(input);
        if (resolution.reason_codes.includes("objective.transition-evidence-required")) {
          let sources;
          try { sources = typeof loadSources === "function" ? await loadSources() : null; }
          catch { return {ok: false, reason_codes: ["objective.meaning-source-load-failed"]}; }
          selection = selectObjectiveMeanings(sources, configuration.meaning_selection);
          if (!selection.ok) return selection;
          resolution = await resolveObjectiveTransition({...input, selected_context: selection.selected_context}, provider);
        }
      } else resolution = await resolveObjectiveTransition(input, provider);
      if (resolution.disposition !== "resolved") return {ok: false, disposition: resolution.disposition, reason_codes: resolution.reason_codes, resolution};
      const appended = ledger.append({event_kind: EVENT, idempotency_key: `objective:${replayKey}`,
        content: {consumer_ref: consumer, thread_id: message.params.threadId, resolution, ...(selection ? {meaning_selection: selection.receipt} : {})}, provenance_refs: [requestRef]});
      if (!appended.ok) { fault = true; return appended; }
      const sealed = ledger.seal({event_digests: [appended.event.event_digest], consumer_ref: consumer, request_ref: requestRef});
      if (!sealed.ok) { fault = true; return sealed; }
      const checkpoint = ledger.checkpoint({checkpoint_kind: "manual", epoch: sealed.value, subject_digest: resolution.resolution_digest});
      if (!checkpoint.ok) { fault = true; return checkpoint; }
      states.set(key, resolution.next_state);
      requests.set(replayKey, resolution);
      return {ok: true, disposition: "resolved", resolution, event_digest: appended.event.event_digest};
    },
    inspect() {
      return [...states.values()].map(state => ({consumer_ref: state.consumer_ref, scope_ref: state.scope_ref, state_digest: state.state_digest,
        active_objective_id: state.active_objective?.objective_id, suspended_count: state.suspended_objectives.length}));
    },
  };
}

export function addObjectiveContext(message, objective) {
  if (!objective?.resolution) return message;
  const r = objective.resolution;
  return freezeResult({...message, params: {...message.params, additionalContext: {...message.params.additionalContext,
    [OBJECTIVE_CONTEXT_KEY]: {kind: "application", value: canonicalJson({schema_version: "are.codex-objective-fragment/v1",
      active_objective: r.next_state.active_objective, state_digest: r.next_state.state_digest, resolution_digest: r.resolution_digest,
      transition: r.transition, classification_basis: r.classification_basis, completion_criteria_posture: r.completion_criteria_posture,
      authority_effect: "none"})}}}});
}
