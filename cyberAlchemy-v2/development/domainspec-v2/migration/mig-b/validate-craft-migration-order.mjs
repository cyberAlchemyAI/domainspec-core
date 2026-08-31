#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const repositoryRoot = resolve(dirname(fileURLToPath(import.meta.url)), "../../../../..");
const orderPath = "cyberAlchemy-v2/development/domainspec-v2/migration/mig-b/map/CRAFT-MIGRATION-ORDER.json";
const errors = [];

function readJson(relativePath) {
  return JSON.parse(readFileSync(resolve(repositoryRoot, relativePath), "utf8"));
}

function sha256(relativePath) {
  return createHash("sha256")
    .update(readFileSync(resolve(repositoryRoot, relativePath)))
    .digest("hex");
}

function requireCondition(condition, message) {
  if (!condition) errors.push(message);
}

const order = readJson(orderPath);

requireCondition(order.schema_version === "cav2.craft-migration-order/v1", "unexpected order schema");
requireCondition(order.status === "planned", "migration order must remain planned before execution");
requireCondition(order.authority_effect === "none", "migration order must not claim authority effect");
requireCondition(order.identity?.product_id === "CA2-PRODUCT-CRAFT", "Craft Product identity is missing");
requireCondition(order.identity?.current_name === "Craft", "current Product name must be Craft");
requireCondition(order.identity?.former_name === "DomainSpec v2", "former Product name must be DomainSpec v2");
requireCondition(order.identity?.continuity === "same-product-renamed", "Product continuity must be same-product-renamed");
requireCondition(order.route?.numbered_candidate_policy === "forbidden-as-migration-control-loop", "numbered candidate loop must be forbidden");
requireCondition(order.route?.source_deletion_policy === "forbidden-by-this-order", "source deletion must remain forbidden");

for (const binding of order.source_bindings ?? []) {
  requireCondition(sha256(binding.path) === binding.sha256, `source binding drift: ${binding.role}`);
}

const bindingByRole = new Map((order.source_bindings ?? []).map((binding) => [binding.role, binding]));
const projectMap = readJson(bindingByRole.get("validated-project-map").path);
const matrix = readJson(bindingByRole.get("development-directory-matrix").path);
const sourceManifest = readJson(bindingByRole.get("source-file-inventory").path);
const pathConsumers = readJson(bindingByRole.get("literal-path-consumer-inventory").path);
const identityDecision = readJson(bindingByRole.get("craft-rename-decision").path);

requireCondition(projectMap.semantic_digest === bindingByRole.get("validated-project-map").semantic_digest, "project map semantic digest drift");
requireCondition(matrix.semantic_digest === bindingByRole.get("development-directory-matrix").semantic_digest, "migration matrix semantic digest drift");
requireCondition(sourceManifest.content_digest === bindingByRole.get("source-file-inventory").content_digest, "source inventory content digest drift");
requireCondition(matrix.source_map_semantic_digest === projectMap.semantic_digest, "matrix does not bind the selected project map");
requireCondition(matrix.rows?.length === order.observed_source_epoch?.development_directories, "development directory count mismatch");
requireCondition(sourceManifest.summary?.entry_count === order.observed_source_epoch?.source_file_entries, "source entry count mismatch");
requireCondition(sourceManifest.summary?.present_bytes === order.observed_source_epoch?.source_bytes, "source byte count mismatch");
requireCondition(pathConsumers.summary?.consumer_file_count === order.observed_source_epoch?.literal_path_consumer_files, "path consumer file count mismatch");
requireCondition(pathConsumers.summary?.occurrence_count === order.observed_source_epoch?.literal_path_occurrences, "path occurrence count mismatch");

requireCondition(identityDecision.identities?.product_id === order.identity.product_id, "identity decision Product mismatch");
requireCondition(identityDecision.identities?.project_id === order.identity.project_id, "identity decision Project mismatch");
requireCondition(identityDecision.identities?.method_ref === order.identity.method_ref, "identity decision Method mismatch");
requireCondition(identityDecision.product_lineage?.current_name === order.identity.current_name, "identity decision current name mismatch");
requireCondition(identityDecision.product_lineage?.former_name === order.identity.former_name, "identity decision former name mismatch");
requireCondition(identityDecision.product_lineage?.continuity === order.identity.continuity, "identity decision continuity mismatch");

const activeRoots = Object.values(order.destination_policy?.active_roots ?? {});
requireCondition(activeRoots.length === 7, "all seven active Craft roots must be declared");
for (const activeRoot of activeRoots) {
  requireCondition(activeRoot.startsWith("cyberAlchemy-v2/"), `active destination is outside CyberAlchemy: ${activeRoot}`);
  requireCondition(activeRoot.endsWith("/craft"), `active destination does not use the Craft name: ${activeRoot}`);
}

const phases = order.phases ?? [];
const phaseIds = new Set(phases.map((phase) => phase.id));
requireCondition(phaseIds.size === phases.length, "phase IDs must be unique");
for (let index = 0; index < phases.length; index += 1) {
  const phase = phases[index];
  requireCondition(phase.order === index, `phase order is not contiguous at ${phase.id}`);
  for (const dependency of phase.depends_on ?? []) {
    const dependencyIndex = phases.findIndex((candidate) => candidate.id === dependency);
    requireCondition(dependencyIndex >= 0, `unknown dependency ${dependency} for ${phase.id}`);
    requireCondition(dependencyIndex < index, `dependency ${dependency} must precede ${phase.id}`);
  }
}

const m00 = phases.find((phase) => phase.id === "M00-REFRESH-AND-FREEZE");
requireCondition(m00?.status === "completed", "M00 must be marked completed");
requireCondition(Boolean(m00?.receipt_ref), "M00 completion receipt is missing");
const m00Receipt = m00?.receipt_ref ? readJson(m00.receipt_ref) : null;
if (m00Receipt) {
  requireCondition(m00Receipt.order_id === order.order_id, "M00 receipt order identity mismatch");
  requireCondition(m00Receipt.phase_id === m00.id, "M00 receipt phase identity mismatch");
  requireCondition(m00Receipt.status === "PASS", "M00 receipt is not PASS");
  requireCondition(m00Receipt.authority_effect === "none", "M00 receipt exceeds its authority ceiling");
  requireCondition(m00Receipt.source_epoch?.source_bytes_unchanged === true, "M00 receipt does not prove stable source bytes");
  requireCondition(m00Receipt.source_epoch?.source_content_digest_after === sourceManifest.content_digest, "M00 receipt source digest mismatch");
  requireCondition(m00Receipt.refreshed_observations?.project_map_semantic_digest === projectMap.semantic_digest, "M00 receipt project map digest mismatch");
  requireCondition(m00Receipt.refreshed_observations?.migration_matrix_semantic_digest === matrix.semantic_digest, "M00 receipt matrix digest mismatch");
  requireCondition(m00Receipt.refreshed_observations?.literal_path_consumer_files_after === pathConsumers.summary?.consumer_file_count, "M00 receipt consumer file count mismatch");
  requireCondition(m00Receipt.refreshed_observations?.literal_path_occurrences_after === pathConsumers.summary?.occurrence_count, "M00 receipt occurrence count mismatch");
  requireCondition(m00Receipt.validation?.craft_migration_order === "pass", "M00 receipt does not record the Craft order validation");
  requireCondition(m00Receipt.validation?.scoped_content_check === "pass", "M00 receipt does not record the scoped content check");
  requireCondition(m00Receipt.artifact_hashes?.["CRAFT-MIGRATION-ORDER.json"] === sha256(orderPath), "M00 receipt order hash mismatch");
  requireCondition(
    m00Receipt.artifact_hashes?.["validate-craft-migration-order.mjs"] ===
      sha256("cyberAlchemy-v2/development/domainspec-v2/migration/mig-b/validate-craft-migration-order.mjs"),
    "M00 receipt order-validator hash mismatch",
  );
}

const directoryWaves = order.directory_waves ?? [];
const selectedDirectories = new Map();
for (let index = 0; index < directoryWaves.length; index += 1) {
  const wave = directoryWaves[index];
  requireCondition(wave.order === index + 1, `directory wave order is not contiguous at ${wave.id}`);
  const { field, equals } = wave.selector ?? {};
  requireCondition(field === "migration_disposition", `unsupported directory selector field in ${wave.id}`);
  const matches = (matrix.rows ?? []).filter((row) => row[field] === equals);
  requireCondition(matches.length === wave.expected_count, `${wave.id} expected ${wave.expected_count} rows but selected ${matches.length}`);
  for (const row of matches) {
    const prior = selectedDirectories.get(row.directory);
    requireCondition(!prior, `directory selected by both ${prior} and ${wave.id}: ${row.directory}`);
    selectedDirectories.set(row.directory, wave.id);
  }
}

for (const row of matrix.rows ?? []) {
  requireCondition(selectedDirectories.has(row.directory), `directory omitted from migration order: ${row.directory}`);
}
requireCondition(selectedDirectories.size === matrix.rows?.length, "directory waves do not partition the matrix exactly once");

const referencedDirectoryWaves = new Set(phases.map((phase) => phase.directory_wave_ref).filter(Boolean));
for (const wave of directoryWaves) {
  requireCondition(referencedDirectoryWaves.has(wave.id), `directory wave is not scheduled by a phase: ${wave.id}`);
}

const latestCandidate = readJson(bindingByRole.get("latest-numbered-candidate-evidence-only").path);
requireCondition(latestCandidate.status === "candidate-unadmitted", "latest numbered candidate posture changed");
requireCondition(latestCandidate.baseline?.admission === "pending", "latest numbered candidate admission is no longer pending");
requireCondition(bindingByRole.get("latest-numbered-candidate-evidence-only").use === "diagnostic-evidence-not-migration-source", "latest numbered candidate must remain diagnostic only");

const result = {
  schema_version: "cav2.craft-migration-order-validation/v1",
  status: errors.length === 0 ? "PASS" : "BLOCK",
  authority_effect: "none",
  order_id: order.order_id,
  counts: {
    source_bindings: order.source_bindings?.length ?? 0,
    phases: phases.length,
    directory_waves: directoryWaves.length,
    development_directories_selected: selectedDirectories.size,
    source_entries_bound: sourceManifest.summary?.entry_count ?? 0,
    literal_path_consumer_files: pathConsumers.summary?.consumer_file_count ?? 0,
    literal_path_occurrences: pathConsumers.summary?.occurrence_count ?? 0
  },
  identity: order.identity,
  errors
};

process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
process.exitCode = errors.length === 0 ? 0 : 1;
