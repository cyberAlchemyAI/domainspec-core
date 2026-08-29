#!/usr/bin/env node

import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const projectRoot = resolve(here, "../..");
const repoRoot = resolve(projectRoot, "../..");
const statePath = resolve(here, "current-implementation.json");
const schemaPath = resolve(here, "current-implementation.schema.json");
const humanPath = resolve(here, "current-implementation.md");
const ontologyPath = resolve(projectRoot, "ontology/profile.json");
const registryPath = resolve(here, "meta-types.yml");
const definitionsPath = resolve(projectRoot, "definitions/DEFINITIONS.md");
const indexPath = resolve(projectRoot, "definitions/DEFINITIONS-INDEX.md");
let checks = 0;

const assert = (condition, message) => {
  checks += 1;
  if (!condition) throw new Error(message);
};
const sha256 = (path) => createHash("sha256").update(readFileSync(path)).digest("hex");
const state = JSON.parse(readFileSync(statePath, "utf8"));
const schema = JSON.parse(readFileSync(schemaPath, "utf8"));
const human = readFileSync(humanPath, "utf8");
const registry = readFileSync(registryPath, "utf8");
const definitions = readFileSync(definitionsPath, "utf8");
const index = readFileSync(indexPath, "utf8");
const ontology = JSON.parse(readFileSync(ontologyPath, "utf8"));

const schemaRun = spawnSync("python3", ["-c", [
  "import json,sys",
  "from jsonschema import Draft202012Validator",
  "schema=json.load(open(sys.argv[1],encoding='utf-8'))",
  "value=json.load(open(sys.argv[2],encoding='utf-8'))",
  "Draft202012Validator.check_schema(schema)",
  "Draft202012Validator(schema).validate(value)",
].join(";"), schemaPath, statePath], { encoding: "utf8" });
assert(schemaRun.status === 0, `current-state schema validation failed:${(schemaRun.stderr || schemaRun.stdout).trim()}`);

const manifestPath = resolve(repoRoot, state.baseline.manifest);
const ownerDecisionPath = resolve(repoRoot, state.baseline.owner_decision);
assert(existsSync(manifestPath), "current baseline manifest missing");
assert(existsSync(ownerDecisionPath), "current baseline owner decision missing");
const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
assert(sha256(manifestPath) === state.baseline.manifest_sha256, "current baseline manifest file digest drift");
assert(sha256(ownerDecisionPath) === state.baseline.owner_decision_sha256, "current baseline decision digest drift");
assert(manifest.baseline_id === state.baseline.id, "current baseline identity drift");
assert(manifest.baseline_digest === state.baseline.baseline_digest, "current baseline body digest drift");
assert(JSON.stringify(manifest.denominators) === JSON.stringify(state.scope), "current baseline scope drift");

const expectedIds = manifest.backend_meta_types.map(({ id }) => id).sort();
const actualIds = state.backend_meta_types.map(({ id }) => id).sort();
assert(JSON.stringify(expectedIds) === JSON.stringify(actualIds), "current backend meta-type set drift");
assert(new Set(actualIds).size === 13, "duplicate current backend meta-type id");
for (const row of state.backend_meta_types) {
  const realized = manifest.realization_rows.filter(({ meta_type_id }) => meta_type_id === row.id);
  assert(realized.length === row.realization_rows, `realization count drift:${row.id}`);
  assert(
    JSON.stringify(realized.map(({ language }) => language).sort()) === JSON.stringify(row.realization_languages),
    `realization language drift:${row.id}`,
  );
}

for (const obligation of [
  "declared read set",
  "declared write set",
  "declared effect set",
  "guard executes before state mutation",
  "atomic state-and-outbox behavior",
  "explicit failure continuation",
  "no undeclared read, write or effect",
  "typed relationships to Rule, Event and Workflow",
]) assert(state.operation_contract.obligations.includes(obligation), `missing Operation obligation:${obligation}`);

assert(registry.includes("current_implementation_state: current-implementation.json"), "DS-D1 registry current-state pointer missing");
for (const id of ["domainspec-v2-D31", "domainspec-v2-D32", "domainspec-v2-D33", "domainspec-v2-D34", "domainspec-v2-D35", "domainspec-v2-D36"]) {
  assert(definitions.includes(`## ${id}.`), `definition card missing:${id}`);
  assert(index.includes(`\`${id}\``), `definition index row missing:${id}`);
}
assert(ontology.current_implementation?.baseline_id === state.baseline.id, "ontology current baseline identity drift");
assert(ontology.current_implementation?.state_ref === "projects/domainspec-v2/definitions/meta-types/current-implementation.json", "ontology current-state ref drift");
assert(human.includes(state.baseline.id), "human current-state identity drift");
assert(human.includes(state.baseline.baseline_digest), "human current-state digest drift");
assert(human.includes("target instantiation and static conformance are implemented"), "human product frontier missing");
assert(state.compensation_contract.definition_id === "domainspec-v2-D36", "compensation definition drift");
assert(state.compensation_contract.executor_owner === "external-runtime", "compensation executor owner drift");
assert(state.claim_ceiling.generated_target_conformance === true, "generated target conformance admission missing");
assert(state.target_conformance.status === "admitted-static-generated-target", "target conformance state drift");
assert(JSON.stringify(state.target_conformance.profiles) === JSON.stringify(["python", "rust", "typescript"]), "target conformance profiles drift");
assert(state.claim_ceiling.durable_compensation_dispatch === false, "durable compensation boundary widened");

process.stdout.write(`${JSON.stringify({
  status: "pass",
  state_id: state.state_id,
  baseline_id: state.baseline.id,
  baseline_digest: state.baseline.baseline_digest,
  checks,
  backend_meta_types: state.backend_meta_types.length,
  realization_rows: state.scope.realization_rows,
  authority_effect: state.authority_effect,
}, null, 2)}\n`);
