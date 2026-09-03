import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {dirname, resolve} from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import {
  bindContextWindowView,
  composeContextLifecycle,
  composeContextBasis,
  lockOntologySelectors,
  resolveDefinitionClosure,
  selectRequestContext,
} from "../index.mjs";
import {loadVerifiedDecisionProfile} from "../../request-decision-router/index.mjs";
import {canonicalJson} from "../../intent-route-resolver/index.mjs";

const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = resolve(packageRoot, "../../../../..");
const profileResult = loadVerifiedDecisionProfile(resolve(packageRoot, "../request-decision-router/profiles/cyberalchemy-v1.json"), repositoryRoot);
assert.equal(profileResult.ok, true, profileResult.reason_codes?.join(","));
const profile = profileResult.value;
const catalog = JSON.parse(readFileSync(resolve(packageRoot, "test/fixtures/definition-catalog.json"), "utf8"));
const snapshot = JSON.parse(readFileSync(resolve(packageRoot, "test/fixtures/ontology-snapshot.json"), "utf8"));

function request(raw_request, objective_kind = null) {
  return {schema_version: "are.request-context/v1", request_id: "REQ-1", raw_request, objective_kind, requested_effects: [], target_refs: [], constraints: [], evidence_refs: ["user"]};
}

function lifecycle(overrides = {}) {
  return composeContextLifecycle({...composition(), current_sources: [
    {source_identity: catalog.source_identity, source_digest: catalog.source_digest},
    {source_identity: snapshot.source_identity, source_digest: snapshot.snapshot_digest},
  ], ...overrides});
}

function composition(overrides = {}) {
  return {
    request_context: request("Research current context management approaches."),
    decision_profile: profile,
    definition: {
      catalog,
      seed_definition_ids: ["RequestContext"],
      universal_relation_classes: ["requires"],
      route_relation_classes_by_route: {"CA2-ROUTE-RESEARCH": ["route-context"]},
    },
    ontology: {snapshot, initial_node_ids: ["Request"], required_edge_ids: [], omission_candidate_ids: ["Unrelated"]},
    authority_posture: "candidate-context-only",
    effect_posture: "non-effectful",
    view: {lane: "plan-bound", consumer_ref: "plan:WP-1", window_ref: "window:1", purpose: "research-planning", source_epoch: "epoch:1", turn_id: "turn:1"},
    ...overrides,
  };
}

test("obvious Research routes directly without Goal fallback", () => {
  const result = composeContextBasis(composition());
  assert.equal(result.ok, true);
  assert.equal(result.value.route_decision.selected.route_id, "CA2-ROUTE-RESEARCH");
  assert.equal(result.value.route_decision.candidates.includes("CA2-ROUTE-PLAN"), false);
});

test("request context selection resolves matching definitions and ontology structure without model or runtime calls", () => {
  const result = selectRequestContext({
    raw_request: "Explain the request context ontology.",
    catalog,
    snapshot,
    policy: {max_definition_matches: 4, max_ontology_node_matches: 4, max_ontology_edge_matches: 4},
  });
  assert.equal(result.ok, true);
  assert.equal(result.value.definition_matches.some((match) => match.definition_id === "RequestContext"), true);
  assert.equal(result.value.ontology_node_matches.some((match) => match.node_id === "Request"), true);
  assert.equal(result.value.model_calls, 0);
  assert.equal(result.value.filesystem_calls, 0);
  assert.equal(result.value.ontology_runtime_calls, 0);
});

test("exact primary definition terms remain selectable when their token is a fuzzy-match stop word", () => {
  const projectCatalog = structuredClone(catalog);
  projectCatalog.definitions.push({definition_id: "Project", primary_term: "Project", aliases: ["Project"], lookup_terms: ["project"]});
  const exact = selectRequestContext({raw_request: "What is a Project?", catalog: projectCatalog, snapshot});
  assert.equal(exact.value.definition_matches.some((match) => match.definition_id === "Project"), true);

  const substring = selectRequestContext({raw_request: "Which projector should I use?", catalog: projectCatalog, snapshot});
  assert.equal(substring.value.definition_matches.some((match) => match.definition_id === "Project"), false);
});

test("exact primary definition matches suppress weaker alias-token competitors", () => {
  const competingCatalog = structuredClone(catalog);
  competingCatalog.definitions.push(
    {definition_id: "ProductCapability", primary_term: "Product Capability", aliases: ["Product Capability"], lookup_terms: ["product capability", "product", "capability"]},
    {definition_id: "CapabilityOwnership", primary_term: "Capability Ownership", aliases: ["Capability Ownership"], lookup_terms: ["capability ownership", "capability", "ownership"]},
  );
  const result = selectRequestContext({raw_request: "What is a Product Capability?", catalog: competingCatalog, snapshot});
  assert.deepEqual(result.value.definition_matches.map((match) => match.definition_id), ["ProductCapability"]);
});

test("the most specific exact primary phrase suppresses its nested generic primary term", () => {
  const nestedCatalog = structuredClone(catalog);
  nestedCatalog.definitions.push(
    {definition_id: "Context", primary_term: "Context", aliases: ["Context"], lookup_terms: ["context"]},
    {definition_id: "ContextWindowView", primary_term: "Context Window View", aliases: ["Context Window View"], lookup_terms: ["context window view", "context", "window", "view"]},
  );
  const result = selectRequestContext({raw_request: "Explain the Context Window View.", catalog: nestedCatalog, snapshot});
  assert.deepEqual(result.value.definition_matches.map((match) => match.definition_id), ["ContextWindowView"]);
});

test("qualified ontology node tails outrank generic token ties within the node budget", () => {
  const nodeIds = ["ContextAssembly", "ContextBasisConstruction", "ContextBoundSemanticIntegrity", "ContextEnvelope", "ContextWindowView"];
  const rankedSnapshot = {
    ontology_id: "qualified-node-ranking",
    source_identity: "fixture:qualified-node-ranking",
    snapshot_digest: "qualified-node-ranking-v1",
    nodes: nodeIds.map((name) => ({
      node_id: `agent-reasoning-engine.${name}`,
      lookup_terms: ["context"],
      search_terms: [`agent-reasoning-engine.${name}`],
    })),
    edges: [],
  };
  const input = {
    raw_request: "Explain the Context Window View.",
    catalog,
    snapshot: rankedSnapshot,
    policy: {max_ontology_node_matches: 4},
  };
  const selected = selectRequestContext(input);
  const permuted = selectRequestContext({...input, snapshot: {...rankedSnapshot, nodes: [...rankedSnapshot.nodes].reverse()}});
  assert.equal(selected.ok, true);
  assert.equal(selected.value.ontology_node_matches[0].node_id, "agent-reasoning-engine.ContextWindowView");
  assert.equal(selected.value.ontology_node_matches[0].matched_terms.includes("context window view"), true);
  assert.deepEqual(selected.value.ontology_node_matches, permuted.value.ontology_node_matches);
});

test("disjoint exact primary concepts remain selected together", () => {
  const disjointCatalog = structuredClone(catalog);
  disjointCatalog.definitions.push(
    {definition_id: "CyberAlchemyV2", primary_term: "CyberAlchemy v2", aliases: ["CyberAlchemy v2"], lookup_terms: ["cyberalchemy v2"]},
    {definition_id: "Ontology", primary_term: "Ontology", aliases: ["Ontology"], lookup_terms: ["ontology"]},
  );
  const result = selectRequestContext({
    raw_request: "I want to understand the ontology already present in CyberAlchemy v2.",
    catalog: disjointCatalog,
    snapshot,
    policy: {max_definition_matches: 2},
  });
  assert.deepEqual(result.value.definition_matches.map((match) => match.definition_id), ["CyberAlchemyV2", "Ontology"]);
});

test("ambiguous routing gates before closure and selector work", () => {
  const result = composeContextBasis(composition({request_context: request("Research and validate this evidence.")}));
  assert.equal(result.ok, false);
  assert.equal(result.route_decision.kind, "gate");
  assert.deepEqual(result.stage_trace, ["request-admission", "route"]);
  assert.deepEqual(result.downstream_calls, {definition_closure: 0, ontology_selector_lock: 0, context_basis: 0, context_window_view: 0});
});

test("definition closure is a permutation-stable least fixed point", () => {
  const base = {catalog, seed_definition_ids: ["RequestContext"], universal_relation_classes: ["requires"], route_relation_classes: ["route-context"]};
  const first = resolveDefinitionClosure(base);
  const permuted = resolveDefinitionClosure({...base, catalog: {...catalog, definitions: [...catalog.definitions].reverse()}, universal_relation_classes: ["requires"], route_relation_classes: ["route-context"]});
  assert.equal(first.ok, true);
  assert.equal(first.digest, permuted.digest);
  assert.deepEqual(first.value.definitions.map((item) => item.definition_id), ["CapabilitySelection", "ContextWindowView", "NecessaryContextBasis", "RequestContext", "ResearchStrategy"]);
});

test("definition closure permits an empty request-relative seed set", () => {
  const result = resolveDefinitionClosure({catalog, seed_definition_ids: [], universal_relation_classes: ["requires"], route_relation_classes: []});
  assert.equal(result.ok, true);
  assert.deepEqual(result.value.definitions, []);
  assert.deepEqual(result.value.traversed_relations, []);
});

test("cycles terminate by full canonical definition identity", () => {
  const result = resolveDefinitionClosure({catalog, seed_definition_ids: ["RequestContext"], universal_relation_classes: ["requires"], route_relation_classes: []});
  assert.equal(result.ok, true);
  assert.equal(result.value.definitions.length, 4);
});

test("missing required definition target blocks with typed residue", () => {
  const broken = structuredClone(catalog);
  broken.definitions.find((item) => item.definition_id === "CapabilitySelection").relations[0].target_definition_id = "MissingDefinition";
  const result = resolveDefinitionClosure({catalog: broken, seed_definition_ids: ["RequestContext"], universal_relation_classes: ["requires"]});
  assert.equal(result.ok, false);
  assert.equal(result.reason_codes.includes("definition.required-target-missing"), true);
  assert.equal(result.residue[0].kind, "partial-closure");
});

test("declared ontology closure recursively includes endpoints and excludes adjacent edges", () => {
  const result = lockOntologySelectors({snapshot, initial_node_ids: ["Request"], required_edge_ids: []});
  assert.equal(result.ok, true);
  assert.deepEqual(result.binding_lock.nodes.map((item) => item.node_id), ["Basis", "Request", "Route"]);
  assert.deepEqual(result.binding_lock.edges.map((item) => item.edge_id), ["edge-basis", "edge-route"]);
  assert.equal(result.excluded_edge_ids.includes("edge-unrelated"), true);
});

test("omission audit cannot widen or change the binding lock digest", () => {
  const base = lockOntologySelectors({snapshot, initial_node_ids: ["Request"], required_edge_ids: []});
  const audited = lockOntologySelectors({snapshot, initial_node_ids: ["Request"], required_edge_ids: [], omission_candidate_ids: ["Unrelated", "edge-unrelated"]});
  assert.equal(base.digest, audited.digest);
  assert.equal(audited.omission_audit.widened_binding, false);
});

test("unrelated ontology drift leaves lock and basis identities valid", () => {
  const drifted = structuredClone(snapshot);
  drifted.snapshot_digest = "changed-ambient-snapshot";
  drifted.nodes.find((item) => item.node_id === "Unrelated").source_digest = "changed-unrelated-node";
  drifted.edges.find((item) => item.edge_id === "edge-unrelated").source_digest = "changed-unrelated-edge";
  const first = composeContextBasis(composition());
  const second = composeContextBasis(composition({ontology: {snapshot: drifted, initial_node_ids: ["Request"], required_edge_ids: [], omission_candidate_ids: []}}));
  assert.equal(first.ok, true);
  assert.equal(second.ok, true);
  assert.equal(first.value.ontology_selector_lock.digest, second.value.ontology_selector_lock.digest);
  assert.equal(first.value.necessary_context_basis.digest, second.value.necessary_context_basis.digest);
});

test("selected dependency drift creates a successor plan view", () => {
  const first = composeContextBasis(composition());
  const drifted = structuredClone(snapshot);
  drifted.nodes.find((item) => item.node_id === "Basis").source_digest = "changed-selected-node";
  const secondInput = composition({ontology: {snapshot: drifted, initial_node_ids: ["Request"], required_edge_ids: []}});
  secondInput.view = {...secondInput.view, turn_id: "turn:2", predecessor_view: first.value.context_window_view.value, reuse_predicate: {equal: true, current: true}};
  const second = composeContextBasis(secondInput);
  assert.equal(second.ok, true);
  assert.notEqual(first.value.necessary_context_basis.digest, second.value.necessary_context_basis.digest);
  assert.notEqual(first.value.context_window_view.value.view_id, second.value.context_window_view.value.view_id);
  assert.equal(second.value.context_window_view.reused, false);
});

test("unchanged plan-bound input retains identity only with a reuse receipt", () => {
  const first = composeContextBasis(composition());
  const nextInput = composition();
  nextInput.view = {...nextInput.view, turn_id: "turn:2", predecessor_view: first.value.context_window_view.value, reuse_predicate: {equal: true, current: true, digest: "predicate:1"}};
  const second = composeContextBasis(nextInput);
  assert.equal(second.ok, true);
  assert.equal(second.value.context_window_view.value.view_id, first.value.context_window_view.value.view_id);
  assert.equal(second.value.context_window_view.reused, true);
  assert.equal(second.value.context_window_view.value.reuse_receipt.identity_retained, true);
  assert.equal(second.value.context_window_view.value.reuse_receipt.turn_id, "turn:2");
});

test("plan-bound predecessor without current equality becomes a successor", () => {
  const first = composeContextBasis(composition());
  const nextInput = composition();
  nextInput.view = {...nextInput.view, turn_id: "turn:2", predecessor_view: first.value.context_window_view.value, reuse_predicate: {equal: true, current: false}};
  const second = composeContextBasis(nextInput);
  assert.notEqual(second.value.context_window_view.value.view_id, first.value.context_window_view.value.view_id);
  assert.equal(second.value.context_window_view.value.reuse_receipt, null);
});

test("every interaction-bound turn creates an immutable successor identity", () => {
  const common = {basis: {schema_version: "test-basis"}, basis_digest: "basis:same", lane: "interaction-bound", consumer_ref: "chat:user", purpose: "answer", source_epoch: "epoch:1"};
  const first = bindContextWindowView({...common, interaction_id: "interaction:1", turn_id: "turn:1"});
  const second = bindContextWindowView({...common, interaction_id: "interaction:2", turn_id: "turn:2", predecessor_view: first.value});
  assert.equal(first.ok, true);
  assert.equal(second.ok, true);
  assert.notEqual(first.value.view_id, second.value.view_id);
  assert.equal(second.value.predecessor_view_id, first.value.view_id);
  assert.equal(Object.isFrozen(second.value), true);
});

test("lane ambiguity blocks instead of defaulting", () => {
  const result = bindContextWindowView({basis: {}, basis_digest: "basis:1", lane: ["plan-bound", "interaction-bound"]});
  assert.equal(result.ok, false);
  assert.deepEqual(result.reason_codes, ["view.exactly-one-lane-required"]);
});

test("canonical output bytes and digest are stable across clean compositions", () => {
  const first = composeContextBasis(composition());
  const second = composeContextBasis(composition());
  assert.equal(first.digest, second.digest);
  assert.equal(canonicalJson(first), canonicalJson(second));
  assert.equal(first.value.strategy_calls, 0);
  assert.equal(first.value.tool_calls, 0);
  assert.equal(first.value.filesystem_calls, 0);
  assert.equal(first.value.network_calls, 0);
  assert.equal(first.value.model_calls, 0);
  assert.equal(first.value.ontology_runtime_calls, 0);
  assert.equal(first.value.effect_calls, 0);
});

test("context lifecycle emits frozen inline definitions and selector-locked ontology items", () => {
  const result = lifecycle({constraints: ["constraint:1"], contradictions: [{ref: "conflict:1"}], exclusions: [{ref: "optional:1", reason: "not-required"}], gaps: [{ref: "gap:1"}], residue: [{ref: "residue:1"}]});
  assert.equal(result.ok, true);
  const envelope = result.value.context_envelope.value;
  assert.equal(envelope.schema_version, "are.context-envelope/v1");
  assert.equal(envelope.included_items.some((item) => item.item_kind === "definition" && item.content.text?.includes("preserved request")), true);
  assert.equal(envelope.included_items.some((item) => item.item_kind === "ontology-node" && item.content.intent === "The necessary context basis."), true);
  assert.equal(envelope.included_items.some((item) => item.item_kind === "request" && item.content.raw_request.includes("Research current")), true);
  assert.equal(envelope.included_items.some((item) => item.item_kind === "constraint"), true);
  assert.equal(envelope.included_items.some((item) => item.item_kind === "gap"), true);
  assert.equal(envelope.included_items.some((item) => item.item_kind === "residue"), true);
  assert.deepEqual(envelope.contradictions, [{ref: "conflict:1"}]);
  assert.deepEqual(envelope.gaps, [{ref: "gap:1"}]);
  assert.deepEqual(envelope.residue, [{ref: "residue:1"}]);
  assert.equal(envelope.exclusions.some((entry) => entry.ref === "optional:1"), true);
  assert.equal(Object.isFrozen(envelope), true);
});

test("stable plan-bound lifecycle reuse requires a current selected-dependency assessment", () => {
  const first = lifecycle();
  const next = composition();
  next.view = {...next.view, turn_id: "turn:2", predecessor_view: first.value.composition.value.context_window_view.value};
  const second = composeContextLifecycle({...next, previous_envelope: first.value.context_envelope.value, current_sources: first.value.context_envelope.value.source_snapshot});
  assert.equal(second.ok, true);
  assert.equal(second.value.refresh_assessment.value.disposition, "reuse-current");
  assert.equal(second.value.composition.value.context_window_view.reused, true);
  assert.equal(second.value.composition.value.context_window_view.value.view_id, first.value.composition.value.context_window_view.value.view_id);
});

test("selected dependency drift requires a successor while unrelated source drift is diagnostic", () => {
  const first = lifecycle();
  const drifted = structuredClone(snapshot);
  drifted.nodes.find((node) => node.node_id === "Basis").source_digest = "selected-drift";
  const selectedInput = composition({ontology: {snapshot: drifted, initial_node_ids: ["Request"], required_edge_ids: []}});
  selectedInput.view = {...selectedInput.view, turn_id: "turn:2", predecessor_view: first.value.composition.value.context_window_view.value};
  const selected = composeContextLifecycle({...selectedInput, previous_envelope: first.value.context_envelope.value, current_sources: first.value.context_envelope.value.source_snapshot});
  assert.equal(selected.value.refresh_assessment.value.disposition, "successor-required");
  assert.equal(selected.value.refresh_assessment.value.changed_selected_dependencies.some((change) => change.identity === "ontology-node:Basis"), true);
  assert.notEqual(selected.value.composition.value.context_window_view.value.view_id, first.value.composition.value.context_window_view.value.view_id);

  const unrelated = composeContextLifecycle({...composition(), previous_envelope: first.value.context_envelope.value, current_sources: [
    ...first.value.context_envelope.value.source_snapshot,
    {source_identity: "ambient:unselected", source_digest: "changed"},
  ]});
  assert.equal(unrelated.value.refresh_assessment.value.disposition, "reuse-current");
  assert.equal(unrelated.value.refresh_assessment.value.unrelated_source_drift.length, 1);
});

test("interaction-bound lifecycle always creates a successor even when selected dependencies are current", () => {
  const input = composition();
  input.view = {lane: "interaction-bound", consumer_ref: "chat:user", purpose: "answer", source_epoch: "epoch:1", interaction_id: "i:1", turn_id: "turn:1"};
  const first = composeContextLifecycle({...input, current_sources: []});
  const secondInput = composition();
  secondInput.view = {...input.view, interaction_id: "i:2", turn_id: "turn:2", predecessor_view: first.value.composition.value.context_window_view.value};
  const second = composeContextLifecycle({...secondInput, previous_envelope: first.value.context_envelope.value, current_sources: []});
  assert.equal(second.value.refresh_assessment.value.disposition, "reuse-current");
  assert.equal(second.value.composition.value.context_window_view.reused, false);
  assert.notEqual(second.value.context_envelope.value.context_epoch_id, first.value.context_envelope.value.context_epoch_id);
});

test("mandatory context overflow blocks without truncating items", () => {
  const result = lifecycle({projection_policy: {max_inline_bytes: 64}});
  assert.equal(result.ok, false);
  assert.equal(result.stage, "context-envelope");
  assert.deepEqual(result.context_envelope.reason_codes, ["context.mandatory-budget-exceeded"]);
  assert.equal(result.context_envelope.residue[0].mandatory_item_count > 0, true);
});

test("lifecycle bytes are deterministic under definition and ontology permutation", () => {
  const first = lifecycle();
  const permutedCatalog = {...catalog, definitions: [...catalog.definitions].reverse()};
  const permutedSnapshot = {...snapshot, nodes: [...snapshot.nodes].reverse(), edges: [...snapshot.edges].reverse()};
  const second = lifecycle({definition: {...composition().definition, catalog: permutedCatalog}, ontology: {...composition().ontology, snapshot: permutedSnapshot}});
  assert.equal(first.digest, second.digest);
  assert.equal(canonicalJson(first), canonicalJson(second));
});
