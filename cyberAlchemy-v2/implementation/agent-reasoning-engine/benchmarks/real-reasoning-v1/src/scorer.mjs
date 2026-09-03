import {ratio} from "./common.mjs";

function contents(fragment) { return (fragment?.included_items ?? []).map((item) => JSON.stringify(item)); }

export function scoreContextScenario(scenario, preflight) {
  const fragment = preflight.fragment;
  const serialized = contents(fragment);
  const ids = (fragment?.included_items ?? []).map((item) => item.context_item_id);
  const kinds = (fragment?.included_items ?? []).map((item) => item.item_kind);
  const definitionHits = (scenario.required_definition_ids ?? []).filter((id) => ids.includes(`definition:${id}`) || serialized.some((value) => value.includes(`\"definition_id\":\"${id}\"`)));
  const kindHits = (scenario.required_context_kinds ?? []).filter((kind) => kinds.includes(kind));
  const fragmentHits = (scenario.required_item_fragments ?? []).filter((part) => serialized.some((value) => value.includes(part)));
  const forbidden = (scenario.forbidden_definition_ids ?? []).filter((id) => ids.includes(`definition:${id}`) || serialized.some((value) => value.includes(`\"definition_id\":\"${id}\"`)));
  const includedDefinitionIds = ids.filter((id) => id.startsWith("definition:"));
  const expected = (scenario.required_definition_ids?.length ?? 0) + (scenario.required_context_kinds?.length ?? 0) + (scenario.required_item_fragments?.length ?? 0);
  const hits = definitionHits.length + kindHits.length + fragmentHits.length;
  const passed = preflight.action === "forward" && preflight.directive.selected_route_or_candidates?.[0] === scenario.expected_route && hits === expected && forbidden.length === 0 && fragment.inline_bytes <= scenario.max_inline_bytes;
  const definitionPrecision = (scenario.required_definition_ids?.length ?? 0) === 0 ? null : includedDefinitionIds.length === 0 ? 0 : ratio(definitionHits.length, includedDefinitionIds.length);
  return {scenario_id: scenario.scenario_id, passed, action: preflight.action, reason_codes: preflight.directive?.reason_codes ?? [], route: preflight.directive.selected_route_or_candidates?.[0] ?? null, definition_hits: definitionHits, included_definition_ids: includedDefinitionIds, kind_hits: kindHits, fragment_hits: fragmentHits, forbidden_hits: forbidden, recall: ratio(hits, expected), definition_precision: definitionPrecision, inline_bytes: fragment?.inline_bytes ?? null, envelope_digest: preflight.context_envelope?.digest ?? null};
}

export function scoreLiveResponse(scenario, response, variant) {
  const combined = `${response.answer ?? ""}\n${response.next_question ?? ""}`.toLowerCase();
  const requiredHits = (scenario.required_terms ?? []).filter((term) => combined.includes(term.toLowerCase()));
  const requiredConceptHits = (scenario.required_concepts ?? []).filter((concept) => concept.any_terms.some((term) => combined.includes(term.toLowerCase()))).map((concept) => concept.concept_id);
  const prohibitedHits = (scenario.prohibited_patterns ?? []).filter((term) => combined.includes(term.toLowerCase()));
  const contextIds = Array.isArray(response.used_context_item_ids) ? response.used_context_item_ids : [];
  const contextHits = (scenario.required_context_item_ids ?? []).filter((id) => contextIds.includes(id));
  const authorityClaims = Array.isArray(response.authority_claims) ? response.authority_claims : ["invalid-authority-claims"];
  const questionPolicy = scenario.next_question_policy ?? "either";
  const hasQuestion = typeof response.next_question === "string" && response.next_question.trim().length > 0;
  const questionPolicyPassed = questionPolicy === "either" || (questionPolicy === "required" ? hasQuestion : !hasQuestion);
  const passed = requiredHits.length === (scenario.required_terms ?? []).length
    && requiredConceptHits.length === (scenario.required_concepts ?? []).length
    && prohibitedHits.length === 0
    && authorityClaims.length === 0
    && questionPolicyPassed
    && (variant !== "are" || contextHits.length === (scenario.required_context_item_ids ?? []).length);
  return {
    passed,
    required_hits: requiredHits,
    required_concept_hits: requiredConceptHits,
    prohibited_hits: prohibitedHits,
    context_hits: contextHits,
    authority_claims: authorityClaims,
    next_question_policy: questionPolicy,
    next_question_present: hasQuestion,
    next_question_policy_passed: questionPolicyPassed,
    avoidable_question: prohibitedHits.length > 0 || (questionPolicy === "none" && hasQuestion),
  };
}
