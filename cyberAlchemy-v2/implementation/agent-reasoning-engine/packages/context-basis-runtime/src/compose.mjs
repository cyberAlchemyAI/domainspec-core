import {admitRequestContext, routeRequest} from "../../request-decision-router/index.mjs";
import {canonicalizeJson, deepFreeze, digestValue, fail, isRecord} from "./canonical.mjs";
import {resolveDefinitionClosure} from "./definition-closure.mjs";
import {lockOntologySelectors} from "./ontology-selector-lock.mjs";
import {constructNecessaryContextBasis} from "./context-basis.mjs";
import {bindContextWindowView} from "./context-window-view.mjs";
import {selectRequestContext} from "./request-context-selector.mjs";

const SCHEMA_VERSION = "are.context-basis-composition/v1";

function observedPhase(options, phaseId, operation) {
  const observer = options?.phase_observer;
  if (typeof observer !== "function") return operation();
  const started = performance.now();
  try {
    const result = operation();
    try {
      observer(Object.freeze({phase_id: phaseId, elapsed_ms: performance.now() - started, outcome: result?.ok === false ? "not-ok" : "ok", authority_effect: "none"}));
    } catch {}
    return result;
  } catch (error) {
    try {
      observer(Object.freeze({phase_id: phaseId, elapsed_ms: performance.now() - started, outcome: "error", authority_effect: "none"}));
    } catch {}
    throw error;
  }
}

function stoppedRoute(routeDecision) {
  return deepFreeze(canonicalizeJson({
    schema_version: SCHEMA_VERSION,
    ok: false,
    stage: "route",
    route_decision: routeDecision,
    stage_trace: ["request-admission", "route"],
    downstream_calls: {definition_closure: 0, ontology_selector_lock: 0, context_basis: 0, context_window_view: 0},
    strategy_calls: 0,
    tool_calls: 0,
    filesystem_calls: 0,
    network_calls: 0,
    model_calls: 0,
    ontology_runtime_calls: 0,
    effect_calls: 0,
    authority_effect: "none",
  }));
}

export function composeContextBasis(input, options = {}) {
  if (!isRecord(input)) return fail("composition", ["composition.input-required"]);
  const admitted = observedPhase(options, "request-admission", () => admitRequestContext(input.request_context));
  if (!admitted.ok) return fail("request-admission", admitted.reason_codes);
  const routeDecision = observedPhase(options, "request-routing", () => routeRequest(admitted.value, input.decision_profile));
  if (routeDecision.kind !== "direct") return stoppedRoute(routeDecision);

  const definitionInput = isRecord(input.definition) ? input.definition : {};
  const ontologyInput = isRecord(input.ontology) ? input.ontology : {};
  const requestSelection = observedPhase(options, "request-context-selection", () => selectRequestContext({
    raw_request: admitted.value.raw_request,
    catalog: definitionInput.catalog,
    snapshot: ontologyInput.snapshot,
    context_items: input.supplemental_context_items,
    policy: input.request_selection_policy,
  }));
  if (!requestSelection.ok) return deepFreeze({...requestSelection, stage_trace: ["request-admission", "route", "request-context-selection"]});
  const routeAdditions = isRecord(definitionInput.route_relation_classes_by_route)
    ? definitionInput.route_relation_classes_by_route[routeDecision.selected.route_id]
    : [];
  const closure = observedPhase(options, "definition-closure", () => resolveDefinitionClosure({
    catalog: definitionInput.catalog,
    seed_definition_ids: [...(definitionInput.seed_definition_ids ?? []), ...requestSelection.value.definition_matches.map((match) => match.definition_id)],
    universal_relation_classes: definitionInput.universal_relation_classes,
    route_relation_classes: routeAdditions,
  }));
  if (!closure.ok) return deepFreeze({...closure, stage_trace: ["request-admission", "route", "definition-closure"]});

  const lock = observedPhase(options, "ontology-selector-lock", () => lockOntologySelectors({
    snapshot: ontologyInput.snapshot,
    initial_node_ids: [...(ontologyInput.initial_node_ids ?? []), ...requestSelection.value.ontology_node_matches.map((match) => match.node_id)],
    required_edge_ids: [...(ontologyInput.required_edge_ids ?? []), ...requestSelection.value.ontology_edge_matches.map((match) => match.edge_id)],
    omission_candidate_ids: ontologyInput.omission_candidate_ids,
  }));
  if (!lock.ok) return deepFreeze({...lock, stage_trace: ["request-admission", "route", "definition-closure", "ontology-selector-lock"]});

  const basis = observedPhase(options, "context-basis-construction", () => constructNecessaryContextBasis({
    request_context: admitted.value,
    request_context_digest: admitted.digest,
    capability_selection: routeDecision,
    definition_closure: closure.value,
    definition_closure_digest: closure.digest,
    ontology_selector_lock: lock.binding_lock,
    ontology_selector_lock_digest: lock.digest,
    authority_posture: input.authority_posture ?? "candidate-context-only",
    effect_posture: input.effect_posture ?? "non-effectful",
    constraints: [...admitted.value.constraints, ...(Array.isArray(input.constraints) ? input.constraints : [])],
    exclusions: input.exclusions,
    contradictions: input.contradictions,
    gaps: input.gaps,
    residue: input.residue,
    instructions: input.instructions,
    supplemental_context_items: (input.supplemental_context_items ?? []).filter((item) => requestSelection.value.context_item_matches.some((match) => match.context_item_id === item.context_item_id)),
  }));
  if (!basis.ok) return deepFreeze({...basis, stage_trace: ["request-admission", "route", "definition-closure", "ontology-selector-lock", "context-basis"]});

  const viewInput = isRecord(input.view) ? input.view : {};
  const view = observedPhase(options, "context-window-view-binding", () => bindContextWindowView({...viewInput, basis: basis.value, basis_digest: basis.digest}));
  if (!view.ok) return deepFreeze({...view, stage_trace: ["request-admission", "route", "definition-closure", "ontology-selector-lock", "context-basis", "context-window-view"]});

  const value = canonicalizeJson({
    schema_version: SCHEMA_VERSION,
    route_decision: routeDecision,
    request_context_selection: requestSelection,
    definition_closure: closure,
    ontology_selector_lock: lock,
    necessary_context_basis: basis,
    context_window_view: view,
    stage_trace: ["request-admission", "route", "definition-closure", "ontology-selector-lock", "context-basis", "context-window-view"],
    strategy_calls: 0,
    tool_calls: 0,
    filesystem_calls: 0,
    network_calls: 0,
    model_calls: 0,
    ontology_runtime_calls: 0,
    effect_calls: 0,
    authority_effect: "none",
  });
  return deepFreeze({schema_version: SCHEMA_VERSION, ok: true, value, digest: digestValue(value), authority_effect: "none"});
}
