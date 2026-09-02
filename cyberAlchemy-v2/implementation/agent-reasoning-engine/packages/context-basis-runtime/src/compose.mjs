import {admitRequestContext, routeRequest} from "../../request-decision-router/index.mjs";
import {canonicalizeJson, deepFreeze, digestValue, fail, isRecord} from "./canonical.mjs";
import {resolveDefinitionClosure} from "./definition-closure.mjs";
import {lockOntologySelectors} from "./ontology-selector-lock.mjs";
import {constructNecessaryContextBasis} from "./context-basis.mjs";
import {bindContextWindowView} from "./context-window-view.mjs";

const SCHEMA_VERSION = "are.context-basis-composition/v1";

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

export function composeContextBasis(input) {
  if (!isRecord(input)) return fail("composition", ["composition.input-required"]);
  const admitted = admitRequestContext(input.request_context);
  if (!admitted.ok) return fail("request-admission", admitted.reason_codes);
  const routeDecision = routeRequest(admitted.value, input.decision_profile);
  if (routeDecision.kind !== "direct") return stoppedRoute(routeDecision);

  const definitionInput = isRecord(input.definition) ? input.definition : {};
  const routeAdditions = isRecord(definitionInput.route_relation_classes_by_route)
    ? definitionInput.route_relation_classes_by_route[routeDecision.selected.route_id]
    : [];
  const closure = resolveDefinitionClosure({
    catalog: definitionInput.catalog,
    seed_definition_ids: definitionInput.seed_definition_ids,
    universal_relation_classes: definitionInput.universal_relation_classes,
    route_relation_classes: routeAdditions,
  });
  if (!closure.ok) return deepFreeze({...closure, stage_trace: ["request-admission", "route", "definition-closure"]});

  const ontologyInput = isRecord(input.ontology) ? input.ontology : {};
  const lock = lockOntologySelectors({
    snapshot: ontologyInput.snapshot,
    initial_node_ids: ontologyInput.initial_node_ids,
    required_edge_ids: ontologyInput.required_edge_ids,
    omission_candidate_ids: ontologyInput.omission_candidate_ids,
  });
  if (!lock.ok) return deepFreeze({...lock, stage_trace: ["request-admission", "route", "definition-closure", "ontology-selector-lock"]});

  const basis = constructNecessaryContextBasis({
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
  });
  if (!basis.ok) return deepFreeze({...basis, stage_trace: ["request-admission", "route", "definition-closure", "ontology-selector-lock", "context-basis"]});

  const viewInput = isRecord(input.view) ? input.view : {};
  const view = bindContextWindowView({...viewInput, basis: basis.value, basis_digest: basis.digest});
  if (!view.ok) return deepFreeze({...view, stage_trace: ["request-admission", "route", "definition-closure", "ontology-selector-lock", "context-basis", "context-window-view"]});

  const value = canonicalizeJson({
    schema_version: SCHEMA_VERSION,
    route_decision: routeDecision,
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
