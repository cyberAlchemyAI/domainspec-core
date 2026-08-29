import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(here, "../../../..");
const manifestPath = resolve(here, "CANONICAL-IMPLEMENTED-BASELINE.v3.json");
const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
let checks = 0;

const assert = (condition, message) => {
  checks += 1;
  if (!condition) throw new Error(message);
};
const sha256Bytes = (bytes) => createHash("sha256").update(bytes).digest("hex");

assert(manifest.schema_version === "domainspec.canonical-implemented-meta-type-baseline/v3", "schema drift");
assert(manifest.baseline_id === "domainspec-meta-types-current-implemented@3", "baseline identity drift");
assert(manifest.supersedes?.baseline_id === "domainspec-meta-types-current-implemented@2", "superseded baseline identity drift");
assert(manifest.supersedes?.baseline_digest === "10c29c2a4feb5039b6c90dcd7e2d44024757b4dd2414f9c0383c82387ec6e836", "superseded baseline digest drift");
assert(manifest.authority_effect === "project-local-canonical-baseline-admission", "authority effect drift");
assert(manifest.denominators.backend_meta_types === 13, "backend denominator drift");
assert(manifest.denominators.realization_rows === 39, "realization denominator drift");
assert(manifest.denominators.ui_state_rows === 11, "UI denominator drift");
assert(manifest.denominators.relationship_authority_rows === 31, "relationship denominator drift");
assert(manifest.denominators.compensation_runtime_contracts === 1, "compensation contract denominator drift");
assert(manifest.inventory.length === manifest.denominators.frozen_evidence_files, "inventory denominator drift");
assert(new Set(manifest.inventory.map(({ path }) => path)).size === manifest.inventory.length, "duplicate inventory path");
assert(manifest.realization_rows.length === 39, "realization row count drift");
assert(new Set(manifest.realization_rows.map(({ meta_type_id, language }) => `${meta_type_id}/${language}`)).size === 39, "duplicate realization row");

for (const required of [
  "projects/domainspec-v2/definitions/DEFINITIONS.md",
  "projects/domainspec-v2/definitions/DEFINITIONS-INDEX.md",
  "projects/domainspec-v2/definitions/DEFINITION-DRIFT-AUDIT.md",
  "projects/domainspec-v2/definitions/meta-types/meta-types.yml",
  "projects/domainspec-v2/definitions/meta-types/meta-types.md",
  "projects/domainspec-v2/definitions/meta-types/current-implementation.schema.json",
  "projects/domainspec-v2/definitions/meta-types/validate-current-implementation.mjs",
  "projects/domainspec-v2/definitions/relationships/relationships.yml",
  "projects/domainspec-v2/impl/architecture-conformance/targets/typescript/workflow-compensation-v1.md",
  "projects/domainspec-v2/impl/architecture-conformance/targets/typescript/workflow-compensation-v1.ts",
]) assert(manifest.inventory.some(({ path }) => path === required), `required canonical source absent:${required}`);

for (const excluded of [
  "projects/domainspec-v2/definitions/meta-types/current-implementation.json",
  "projects/domainspec-v2/definitions/meta-types/current-implementation.md",
  "projects/domainspec-v2/development/implementation-conformance/ontology-experiment/ontology.json",
  "projects/domainspec-v2/development/implementation-conformance/ontology-experiment/domain-meta-types.projection.json",
]) assert(!manifest.inventory.some(({ path }) => path === excluded), `digest-cycle view included:${excluded}`);

for (const entry of manifest.inventory) {
  const path = resolve(repoRoot, entry.path);
  assert(existsSync(path), `missing frozen file:${entry.path}`);
  const bytes = readFileSync(path);
  assert(bytes.length === entry.bytes, `frozen size drift:${entry.path}`);
  assert(sha256Bytes(bytes) === entry.sha256, `frozen digest drift:${entry.path}`);
}

for (const row of manifest.realization_rows) {
  for (const role of ["source", "provider", "binding"]) {
    const ref = row[role];
    const path = resolve(repoRoot, ref.path);
    assert(existsSync(path), `missing realization ${role}:${row.meta_type_id}/${row.language}`);
    assert(sha256Bytes(readFileSync(path)) === ref.sha256, `realization ${role} drift:${row.meta_type_id}/${row.language}`);
  }
}

const decisionPath = resolve(repoRoot, manifest.owner_decision.path);
assert(existsSync(decisionPath), "owner decision missing");
assert(sha256Bytes(readFileSync(decisionPath)) === manifest.owner_decision.sha256, "owner decision drift");

const { baseline_digest: recordedDigest, ...body } = manifest;
assert(sha256Bytes(Buffer.from(JSON.stringify(body))) === recordedDigest, "baseline digest drift");
assert(manifest.claim_ceiling.canonical_project_local_baseline === true, "canonical baseline not admitted");
assert(manifest.claim_ceiling.current_implementation_evidence_admitted === true, "implementation evidence not admitted");
assert(manifest.claim_ceiling.generated_target_conformance === false, "baseline conformance claim widened");
assert(manifest.claim_ceiling.compensation_runtime_contract_admitted === true, "compensation contract not admitted");
for (const field of ["generated_target_conformance", "durable_compensation_dispatch", "publication", "release", "deployment", "production"]) {
  assert(manifest.claim_ceiling[field] === false, `claim ceiling widened:${field}`);
}

process.stdout.write(`${JSON.stringify({
  status: "pass",
  baseline_id: manifest.baseline_id,
  baseline_digest: manifest.baseline_digest,
  checks,
  evidence_files: manifest.inventory.length,
  backend_meta_types: manifest.backend_meta_types.length,
  realization_rows: manifest.realization_rows.length,
  authority_effect: manifest.authority_effect,
}, null, 2)}\n`);
