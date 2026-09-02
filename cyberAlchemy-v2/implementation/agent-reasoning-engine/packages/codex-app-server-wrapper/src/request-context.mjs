import {canonicalJson, digestValue, fail, freezeResult, isRecord, nonEmptyString, uniqueStrings} from "./canonical.mjs";

function describeInput(item) {
  if (!isRecord(item) || !nonEmptyString(item.type)) return canonicalJson(item);
  if (item.type === "text" && typeof item.text === "string") return item.text;
  if (item.type === "image" && nonEmptyString(item.url)) return `[image:${item.url}]`;
  if (item.type === "localImage" && nonEmptyString(item.path)) return `[local-image:${item.path}]`;
  if (item.type === "audio" && nonEmptyString(item.url)) return `[audio:${item.url}]`;
  if (item.type === "localAudio" && nonEmptyString(item.path)) return `[local-audio:${item.path}]`;
  if ((item.type === "skill" || item.type === "mention") && nonEmptyString(item.name) && nonEmptyString(item.path)) return `[${item.type}:${item.name}:${item.path}]`;
  return canonicalJson(item);
}

export function buildRequestContext(message, turnBinding) {
  if (!isRecord(message) || message.method !== "turn/start" || !isRecord(message.params)) {
    return fail("request-context", ["request.turn-start-required"]);
  }
  if (!isRecord(turnBinding)) return fail("request-context", ["request.turn-binding-required"]);
  const input = message.params.input;
  if (!Array.isArray(input) || input.length === 0) return fail("request-context", ["request.input-required"]);
  if (!nonEmptyString(message.params.threadId)) return fail("request-context", ["request.thread-id-required"]);
  const rawRequest = input.map(describeInput).join("\n").trim();
  if (!rawRequest) return fail("request-context", ["request.raw-request-empty"]);
  const requestId = nonEmptyString(turnBinding.request_id)
    ? turnBinding.request_id.trim()
    : `codex-request:${digestValue({rpc_id: message.id ?? null, thread_id: message.params.threadId, input})}`;
  const value = freezeResult({
    schema_version: "are.request-context/v1",
    request_id: requestId,
    raw_request: rawRequest,
    objective_kind: nonEmptyString(turnBinding.objective_kind) ? turnBinding.objective_kind.trim() : null,
    requested_effects: uniqueStrings(turnBinding.requested_effects),
    target_refs: uniqueStrings(turnBinding.target_refs),
    constraints: uniqueStrings(turnBinding.constraints),
    evidence_refs: uniqueStrings([...(turnBinding.evidence_refs ?? []), `codex-input:${digestValue(input)}`]),
  });
  return freezeResult({
    ok: true,
    value,
    raw_input: input,
    raw_input_digest: digestValue(input),
    authority_effect: "none",
  });
}
