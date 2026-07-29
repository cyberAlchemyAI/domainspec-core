import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  buildReceipt,
  renderDeterministicJson,
  validateBusinessOntology,
  validateNodeShape,
  validateRelationShape,
  validateTransition,
} from "../scripts/validate.mjs";

const packageRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

async function readJson(relativePath) {
  return JSON.parse(
    await readFile(path.join(packageRoot, relativePath), "utf8"),
  );
}

test("T-BWO-001 validates the complete candidate business graph without authority effect", async () => {
  const validation = await validateBusinessOntology();
  assert.equal(validation.status, "pass");
  assert.deepEqual(validation.diagnostics, []);
  assert.ok(validation.counts.nodes >= 100);
  assert.ok(validation.counts.relations >= 100);
  assert.ok(validation.counts.lifecycle_policies >= 6);

  const receipt = buildReceipt(validation, {
    direct_promotion: { result: "rejected" },
  });
  assert.equal(receipt.ontology_status, "candidate-local");
  assert.equal(receipt.authority_effect, "none");
  assert.equal(receipt.release_admission, "not-granted");
});

test("deterministic package digests and receipt bytes are order-insensitive", async () => {
  const first = await validateBusinessOntology();
  const second = await validateBusinessOntology();
  assert.deepEqual(second.digests, first.digests);
  assert.equal(
    renderDeterministicJson(
      buildReceipt(first, { direct_promotion: { result: "rejected" } }),
    ),
    renderDeterministicJson(
      buildReceipt(second, { direct_promotion: { result: "rejected" } }),
    ),
  );
});

test("direct needs-evidence to source-backed promotion is rejected", async () => {
  const validation = await validateBusinessOntology();
  const policy = validation.loaded.lifecyclePolicies.find(
    (item) => item.policy_id === "body-war.lifecycle.suggested-track",
  );
  const legal = await readJson("fixtures/valid/legal-transition.json");
  const invalid = await readJson(
    "fixtures/invalid/direct-promotion-transition.json",
  );
  assert.deepEqual(validateTransition(legal, policy), []);
  assert.deepEqual(
    validateTransition(invalid, policy).map((item) => item.code),
    ["BWO_TRANSITION_FORBIDDEN"],
  );
});

test("dangling endpoints and dangerous value cycles fail closed", async () => {
  const validation = await validateBusinessOntology();
  const conceptIds = new Set(
    validation.loaded.nodes.map((node) => node.concept_id),
  );
  const dangling = await readJson(
    "fixtures/invalid/dangling-relation.json",
  );
  const valueCycle = await readJson(
    "fixtures/invalid/value-cycle-relation.json",
  );
  assert.ok(
    validateRelationShape(dangling, conceptIds).some(
      (item) => item.code === "BWO_RELATION_ENDPOINT_MISSING",
    ),
  );
  assert.ok(
    validateRelationShape(valueCycle, conceptIds).some(
      (item) => item.code === "BWO_VALUE_CYCLE_BLOCKED",
    ),
  );
});

test("ontology nodes reject embedded executable logic", async () => {
  const validation = await validateBusinessOntology();
  const fragment = await readJson(
    "fixtures/invalid/executable-node-fragment.json",
  );
  const invalid = structuredClone(validation.loaded.nodes[0]);
  Object.assign(invalid, fragment);
  assert.ok(
    validateNodeShape(invalid).some(
      (item) => item.code === "BWO_EXECUTABLE_LOGIC_FORBIDDEN",
    ),
  );
});

test("checked-in schemas remain closed and retain the CAV2 contract fields", async () => {
  const nodeSchema = await readJson("schemas/node.schema.json");
  const relationSchema = await readJson("schemas/relation.schema.json");
  const branchSchema = await readJson("schemas/branch-view.schema.json");
  const lifecycleSchema = await readJson(
    "schemas/lifecycle-policy.schema.json",
  );
  for (const schema of [
    nodeSchema,
    relationSchema,
    branchSchema,
    lifecycleSchema,
  ]) {
    assert.equal(schema.additionalProperties, false);
  }
  assert.ok(nodeSchema.required.includes("challenge_contract"));
  assert.ok(nodeSchema.required.includes("forbidden_collapse"));
  assert.ok(relationSchema.required.includes("value_effect"));
  assert.ok(relationSchema.required.includes("cycle_policy"));
  assert.ok(branchSchema.required.includes("forbidden_authority_moves"));
  assert.ok(lifecycleSchema.required.includes("state_concepts"));
});
