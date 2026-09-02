import {
  canonicalJson,
  canonicalizeJson,
  deepFreeze,
  digestValue,
  fail,
  isRecord,
  nonEmptyString,
  uniqueStrings,
} from "./canonical.mjs";

const ITEM_SCHEMA = "are.context-item/v1";
const ENVELOPE_SCHEMA = "are.context-envelope/v1";
export const DEFAULT_MAX_INLINE_BYTES = 32 * 1024;

function contextItem(material) {
  const value = {
    schema_version: ITEM_SCHEMA,
    context_item_id: material.context_item_id,
    item_kind: material.item_kind,
    source_ref: material.source_ref ?? null,
    source_digest: material.source_digest,
    authority_posture: material.authority_posture,
    relevance_basis: material.relevance_basis,
    temporal_scope: material.temporal_scope,
    transform_refs: uniqueStrings(material.transform_refs),
    content: material.content ?? null,
    mandatory: true,
    authority_effect: "none",
  };
  return {...value, item_digest: digestValue(value)};
}

function normalizeSourceSnapshot(value) {
  return (Array.isArray(value) ? value : [])
    .filter((entry) => isRecord(entry) && nonEmptyString(entry.source_identity) && nonEmptyString(entry.source_digest))
    .map((entry) => ({source_identity: entry.source_identity.trim(), source_digest: entry.source_digest.trim()}))
    .sort((a, b) => a.source_identity.localeCompare(b.source_identity));
}

export function selectedDependenciesFromComposition(composition) {
  if (!isRecord(composition) || composition.ok !== true || !isRecord(composition.value)) return [];
  const value = composition.value;
  const route = value.route_decision ?? {};
  const basis = value.necessary_context_basis?.value ?? {};
  const closure = value.definition_closure?.value ?? {};
  const lock = value.ontology_selector_lock?.binding_lock ?? {};
  const dependencies = [
    {dependency_id: "request-context", dependency_kind: "request", digest: route.request_context_digest},
    {dependency_id: "decision-profile", dependency_kind: "route-profile", digest: route.decision_profile_digest},
    {dependency_id: `route:${route.selected?.route_id ?? "unresolved"}`, dependency_kind: "route", digest: route.decision_digest},
    {dependency_id: "definition-closure", dependency_kind: "closure", digest: value.definition_closure?.digest},
    {dependency_id: "ontology-selector-lock", dependency_kind: "selector-lock", digest: value.ontology_selector_lock?.digest},
    {dependency_id: "authority-posture", dependency_kind: "posture", digest: digestValue(basis.authority_posture ?? null)},
    {dependency_id: "effect-posture", dependency_kind: "posture", digest: digestValue(basis.effect_posture ?? null)},
  ];
  for (const definition of closure.definitions ?? []) {
    dependencies.push({dependency_id: `definition:${definition.definition_id}`, dependency_kind: "definition", digest: definition.digest, source_ref: definition.source_ref ?? null});
  }
  for (const node of lock.nodes ?? []) {
    dependencies.push({dependency_id: `ontology-node:${node.node_id}`, dependency_kind: "ontology-node", digest: node.source_digest, source_ref: node.source_ref ?? null});
  }
  for (const edge of lock.edges ?? []) {
    dependencies.push({dependency_id: `ontology-edge:${edge.edge_id}`, dependency_kind: "ontology-edge", digest: edge.source_digest, source_ref: edge.source_ref ?? null});
  }
  return dependencies
    .filter((dependency) => nonEmptyString(dependency.digest))
    .sort((a, b) => a.dependency_id.localeCompare(b.dependency_id));
}

export function assembleContextEnvelope(composition, projectionPolicy = {}) {
  if (!isRecord(composition) || composition.ok !== true || !isRecord(composition.value)) return fail("context-envelope", ["context.composition-required"]);
  const value = composition.value;
  const closure = value.definition_closure?.value;
  const lock = value.ontology_selector_lock?.binding_lock;
  const basis = value.necessary_context_basis?.value;
  const view = value.context_window_view?.value;
  if (!isRecord(closure) || !isRecord(lock) || !isRecord(basis) || !isRecord(view)) return fail("context-envelope", ["context.composition-incomplete"]);
  const maxInlineBytes = Number.isSafeInteger(projectionPolicy.max_inline_bytes) && projectionPolicy.max_inline_bytes > 0
    ? projectionPolicy.max_inline_bytes
    : DEFAULT_MAX_INLINE_BYTES;
  const sourceEpoch = nonEmptyString(view.source_epoch) ? view.source_epoch : "unresolved";
  const temporalScope = "source-epoch";
  const items = [];

  for (const definition of closure.definitions ?? []) {
    items.push(contextItem({
      context_item_id: `definition:${definition.definition_id}`,
      item_kind: "definition",
      source_ref: definition.source_ref,
      source_digest: definition.digest,
      authority_posture: definition.authority_posture,
      relevance_basis: closure.seed_definition_ids?.includes(definition.definition_id) ? "definition-closure-seed" : "definition-closure-required-relation",
      temporal_scope: temporalScope,
      transform_refs: ["definition-closure/v1"],
      content: {definition_id: definition.definition_id, version_or_revision: definition.version_or_revision, text: definition.definition_text ?? null},
    }));
  }
  for (const node of lock.nodes ?? []) {
    items.push(contextItem({
      context_item_id: `ontology-node:${node.node_id}`,
      item_kind: "ontology-node",
      source_ref: `ontology#node:${node.node_id}`,
      source_digest: node.source_digest,
      authority_posture: "basis-posture",
      relevance_basis: node.selection_reason ?? "selector-lock-required-node",
      temporal_scope: temporalScope,
      transform_refs: ["lock/v1"],
      content: {node_id: node.node_id, node_type: node.node_type, intent: node.content?.intent ?? node.content?.meaning ?? null},
    }));
  }
  for (const edge of lock.edges ?? []) {
    items.push(contextItem({
      context_item_id: `ontology-edge:${edge.edge_id}`,
      item_kind: "ontology-edge",
      source_ref: `ontology#edge:${edge.edge_id}`,
      source_digest: edge.source_digest,
      authority_posture: "basis-posture",
      relevance_basis: edge.selection_reason ?? "selector-lock-required-edge",
      temporal_scope: temporalScope,
      transform_refs: ["lock/v1"],
      content: {edge_id: edge.edge_id, edge_type: edge.edge_type, from_node_id: edge.from_node_id, to_node_id: edge.to_node_id},
    }));
  }
  items.sort((a, b) => a.context_item_id.localeCompare(b.context_item_id));
  const inlineBytes = Buffer.byteLength(canonicalJson(items), "utf8");
  if (inlineBytes > maxInlineBytes) {
    return fail("context-envelope", ["context.mandatory-budget-exceeded"], [{mandatory_bytes: inlineBytes, max_inline_bytes: maxInlineBytes, mandatory_item_count: items.length}]);
  }

  const exclusions = [
    ...(basis.exclusions ?? []),
    ...(value.ontology_selector_lock?.excluded_node_ids ?? []).map((ref) => ({ref: `ontology-node:${ref}`, reason: "not-selected"})),
    ...(value.ontology_selector_lock?.excluded_edge_ids ?? []).map((ref) => ({ref: `ontology-edge:${ref}`, reason: "not-selected"})),
    ...(value.ontology_selector_lock?.omission_audit?.candidates ?? []).map((candidate) => ({ref: candidate.selector_id, reason: candidate.posture})),
  ];
  const material = {
    schema_version: ENVELOPE_SCHEMA,
    request_digest: value.route_decision.request_context_digest,
    route_decision_digest: value.route_decision.decision_digest,
    basis_digest: value.necessary_context_basis.digest,
    view_id: view.view_id,
    view_lane: view.lane,
    predecessor_view_id: view.predecessor_view_id ?? null,
    source_epoch: sourceEpoch,
    authority_posture: basis.authority_posture,
    included_items: items,
    included_item_digests: items.map((entry) => entry.item_digest),
    exclusions,
    contradictions: basis.contradictions ?? [],
    gaps: basis.gaps ?? [],
    residue: basis.residue ?? [],
    selected_dependencies: selectedDependenciesFromComposition(composition),
    source_snapshot: normalizeSourceSnapshot(projectionPolicy.current_sources),
    freshness_state: projectionPolicy.freshness_state ?? "current",
    inline_bytes: inlineBytes,
    max_inline_bytes: maxInlineBytes,
    compression_method: "deterministic-structural-projection-no-summary",
    claim_ceiling: projectionPolicy.claim_ceiling ?? "Bounded context evidence only; no source truth, approval, admission, or effect authority.",
    authority_effect: "none",
  };
  const contextEpochId = `context-epoch:${digestValue(material)}`;
  const envelope = canonicalizeJson({...material, context_epoch_id: contextEpochId});
  return deepFreeze({schema_version: ENVELOPE_SCHEMA, ok: true, value: envelope, digest: digestValue(envelope), inline_bytes: inlineBytes, authority_effect: "none"});
}
