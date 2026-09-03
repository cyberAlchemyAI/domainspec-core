import assert from "node:assert/strict";
import {fileURLToPath} from "node:url";
import {dirname, resolve} from "node:path";
import test from "node:test";

import {evaluateContinuation, loadVerifiedDecisionProfile, routeRequest} from "../index.mjs";

const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = resolve(packageRoot, "../../../../..");
const loaded = loadVerifiedDecisionProfile(resolve(packageRoot, "profiles/cyberalchemy-v1.json"), repositoryRoot);
assert.equal(loaded.ok, true, loaded.reason_codes?.join(","));
const profile = loaded.value;

function context(raw_request, objective_kind = null) {
  return {schema_version: "are.request-context/v1", request_id: "R-1", raw_request, objective_kind, requested_effects: [], target_refs: [], constraints: [], evidence_refs: ["user"]};
}

test("Define routes directly without Goal", () => {
  const result = routeRequest(context("Please clarify intent and define this concept."), profile);
  assert.equal(result.kind, "direct");
  assert.equal(result.selected.route_id, "CA2-ROUTE-DEFINE");
  assert.equal(result.candidates.includes("CA2-ROUTE-PLAN"), false);
});

test("Goal participates only on goal-specific evidence and retains Goal profile provenance", () => {
  const result = routeRequest(context("Decompose goal into a work graph."), profile);
  assert.equal(result.kind, "direct");
  assert.equal(result.selected.route_id, "CA2-ROUTE-PLAN");
  assert.ok(result.selected.provenance_ids.includes("goal-profile"));
  assert.ok(result.provenance.some((item) => item.id === "goal-profile"));
});

test("implementation does not route through Goal", () => {
  const result = routeRequest(context("Implement the bounded repair."), profile);
  assert.equal(result.kind, "direct");
  assert.equal(result.selected.route_id, "CA2-ROUTE-IMPLEMENT");
});

test("overlap becomes a gate and no-match blocks", () => {
  const gate = routeRequest(context("Research and validate this evidence."), profile);
  assert.equal(gate.kind, "gate");
  assert.equal(gate.candidate_details.length, gate.candidates.length);
  assert.ok(gate.candidate_details.every((candidate) => Object.hasOwn(candidate, "owner_gate_ref")));
  assert.ok(gate.candidate_details.every((candidate) => candidate.provenance_ids.includes("route-registry")));
  assert.equal(routeRequest(context("Have a pleasant afternoon."), profile).kind, "block");
});

test("explicit objective kind is stronger than absent lexical signals", () => {
  const result = routeRequest(context("Handle this bounded request.", "validate"), profile);
  assert.equal(result.kind, "direct");
  assert.equal(result.selected.route_id, "CA2-ROUTE-VALIDATE");
});

test("explicit objective suppresses incidental lexical candidates", () => {
  const goalDefinition = routeRequest(context("What is a Goal?", "define"), profile);
  assert.equal(goalDefinition.kind, "direct");
  assert.equal(goalDefinition.selected.route_id, "CA2-ROUTE-DEFINE");
  assert.deepEqual(goalDefinition.suppressed_lexical_candidates, ["CA2-ROUTE-PLAN"]);
  assert.deepEqual(goalDefinition.reason_codes, ["selection.explicit-objective-priority"]);

  const researchDefinition = routeRequest(context("Define a research DAO rewards system.", "define"), profile);
  assert.equal(researchDefinition.kind, "direct");
  assert.equal(researchDefinition.selected.route_id, "CA2-ROUTE-DEFINE");
  assert.deepEqual(researchDefinition.suppressed_lexical_candidates, ["CA2-ROUTE-RESEARCH"]);
});

test("explicit objective does not suppress structured effect conflicts or exclusions", () => {
  const effectConflict = context("Explain this architecture.", "explain");
  effectConflict.requested_effects = ["publication"];
  const gated = routeRequest(effectConflict, profile);
  assert.equal(gated.kind, "gate");
  assert.deepEqual(gated.candidates, ["CA2-ROUTE-PUBLISH", "CA2-ROUTE-UNDERSTAND"]);

  const negatedAction = routeRequest(context("Explain only; do not implement.", "explain"), profile);
  assert.equal(negatedAction.kind, "direct");
  assert.equal(negatedAction.selected.route_id, "CA2-ROUTE-UNDERSTAND");
  assert.equal(negatedAction.evaluated_routes.find((route) => route.route_id === "CA2-ROUTE-IMPLEMENT").posture, "rejected");

  const explicitExclusion = routeRequest(context("Implement the repair read only.", "implement"), profile);
  assert.equal(explicitExclusion.kind, "block");
  assert.ok(explicitExclusion.evaluated_routes.find((route) => route.route_id === "CA2-ROUTE-IMPLEMENT").reason_codes.includes("route.explicit-exclusion"));
});

test("negated lexical actions never become positive route evidence", () => {
  const result = routeRequest(context("Do not implement this."), profile);
  assert.equal(result.kind, "block");
  assert.deepEqual(result.evaluated_routes.find((route) => route.route_id === "CA2-ROUTE-IMPLEMENT").matched_signals, []);
});

test("unverified profiles cannot route or classify continuation", () => {
  const unverified = JSON.parse(JSON.stringify(profile));
  assert.equal(routeRequest(context("Explain this."), unverified).kind, "block");
  assert.deepEqual(routeRequest(context("Explain this."), unverified).reason_codes, ["profile.unverified"]);
  const continuation = evaluateContinuation({completion: {completion_id: "C", status: "completed", continuation_required: true}, options: []}, unverified);
  assert.equal(continuation.kind, "block");
  assert.deepEqual(continuation.reason_codes, ["profile.unverified"]);
});

test("structured requested effects and constraints participate in routing", () => {
  const mixed = context("Explain architecture.");
  mixed.requested_effects = ["publication"];
  assert.equal(routeRequest(mixed, profile).kind, "gate");
  const constrained = context("Implement the repair.");
  constrained.constraints = ["read only"];
  assert.equal(routeRequest(constrained, profile).kind, "block");
});

test("canonical Definitions route is reachable and blocked Session remains visible", () => {
  assert.equal(routeRequest(context("Audit canonical term vocabulary."), profile).selected.route_id, "CA2-ROUTE-DEFINITIONS");
  assert.equal(routeRequest(context("Create a durable repository session."), profile).kind, "block");
});
