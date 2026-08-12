import assert from "node:assert/strict";
import test from "node:test";
import { loadAnatomyInputs, validateAnatomyMap } from "../scripts/validate-anatomy-map.mjs";

const inputs = await loadAnatomyInputs();
const clone = (value) => structuredClone(value);
const validateMutation = (mutate) => {
  const candidate = clone(inputs);
  mutate(candidate);
  return validateAnatomyMap(candidate);
};

test("the anatomy catalog covers the exact ontology and preserves the external SDK seam", () => {
  const result = validateAnatomyMap(inputs);
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.coverage, {concepts: 22, relations: 28, regions: 9, external_seams: 1});
});

test("unknown concept IDs fail closed", () => {
  const result = validateMutation(({anatomy}) => { anatomy.regions[0].concepts[0].id = "aug.concept.unknown"; });
  assert.equal(result.status, "block");
  assert.match(result.errors.join("\n"), /unknown-concept/);
});

test("changed owner or posture fails closed", () => {
  const result = validateMutation(({anatomy}) => {
    anatomy.regions[0].concepts[0].owner = "augmentor";
    anatomy.regions[0].concepts[1].posture = "designed";
  });
  assert.match(result.errors.join("\n"), /concept-owner/);
  assert.match(result.errors.join("\n"), /concept-posture/);
});

test("optimistic mixed status fails closed", () => {
  const result = validateMutation(({anatomy}) => { anatomy.regions[0].overview_posture = "observed"; });
  assert.match(result.errors.join("\n"), /optimistic-mixed-status/);
});

test("a missing limitation fails closed", () => {
  const result = validateMutation(({anatomy}) => { delete anatomy.regions[0].limitation; });
  assert.match(result.errors.join("\n"), /region-field/);
});

test("SDK ontology contamination fails closed", () => {
  const result = validateMutation(({anatomy}) => { anatomy.external_seams[0].ontology_refs.push("aug.concept.augmentor_interface"); });
  assert.match(result.errors.join("\n"), /sdk-imported/);
});

test("unsupported privacy capability language fails closed", () => {
  const result = validateMutation(({anatomy}) => { anatomy.regions[8].limitation = "A privacy control protects the system."; });
  assert.match(result.errors.join("\n"), /privacy-claim/);
});

test("a required-looking heart fails closed", () => {
  const result = validateMutation(({anatomy}) => { anatomy.main_path.push("heart"); });
  assert.match(result.errors.join("\n"), /required-heart/);
});
