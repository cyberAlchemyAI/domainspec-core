#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const TOOL_PATH = fileURLToPath(import.meta.url);
const DEFAULT_REPOSITORY_ROOT = path.resolve(path.dirname(TOOL_PATH), "../../../../..");
const FEATURE_ID = "auth-exact-permission";
const RECEIPT_PATH = "DOMAINSPEC-INSTANTIATION-RECEIPT.json";
const TEMPLATE_PATH = "projects/domainspec-v2/impl/cli/templates/auth-kernel/lib.rs.tmpl";

const REQUIRED_NODES = Object.freeze({
  "authorization-context": {
    source: "nodes/authorization-context.json",
    nodeId: "auth-exact-permission.AuthorizationContext",
    kind: "Entity",
    metaTypeId: "DS-D1.1",
    fields: [
      ["request_id", "string", true],
      ["session_id", "string", false],
      ["decision_time", "u64", false],
      ["current_authorization_revision", "u64", false],
      ["trusted_scope_evidence", "boolean", false],
      ["role_relation_complete", "boolean", false],
    ],
    semanticRefs: ["AUTH-AUTHORIZATION-REQUEST", "AF-RULE-UNIQUE-RESOLVED-SESSION", "AF-RULE-TRUSTED-SCOPE", "AF-RULE-COMPLETE-ACTIVE-ROLES"],
  },
  session: {
    source: "nodes/session.json",
    nodeId: "auth-exact-permission.Session",
    kind: "Entity",
    metaTypeId: "DS-D1.1",
    fields: [
      ["session_id", "string", true],
      ["user_id", "string", false],
      ["status", "SessionStatus", false],
      ["expires_at", "u64", false],
      ["authorization_revision", "u64", false],
      ["active_role_ids", "Set<string>", false],
    ],
    semanticRefs: ["AUTH-SESSION", "AF-RULE-SESSION-CURRENT"],
  },
  role: {
    source: "nodes/role.json",
    nodeId: "auth-exact-permission.Role",
    kind: "Entity",
    metaTypeId: "DS-D1.1",
    fields: [["role_id", "string", true], ["permissions", "Set<Permission>", false]],
    semanticRefs: ["AUTH-ROLE", "AF-RULE-COMPLETE-ACTIVE-ROLES"],
  },
  permission: {
    source: "nodes/permission.json",
    nodeId: "auth-exact-permission.Permission",
    kind: "Entity",
    metaTypeId: "DS-D1.1",
    fields: [["resource", "string", true], ["action", "string", true], ["scope", "string", true]],
    semanticRefs: ["AUTH-PERMISSION", "AF-RULE-EXACT-ACTIVE-ROLE-GRANT"],
  },
  "authorization-decision": {
    source: "nodes/authorization-decision.json",
    nodeId: "auth-exact-permission.AuthorizationDecision",
    kind: "Entity",
    metaTypeId: "DS-D1.1",
    fields: [["request_id", "string", true], ["value", "ALLOW|DENY", false], ["diagnostic_reason", "optional<string>", false]],
    semanticRefs: ["AUTH-AUTHORIZATION-DECISION", "AF-RULE-ALLOW-IFF", "AF-RULE-DEFAULT-DENY"],
  },
  "authorization-invariant": {
    source: "nodes/authorization-invariant.json",
    nodeId: "auth-exact-permission.AuthorizationInvariant",
    kind: "Rule",
    metaTypeId: "DS-D1.7",
    semanticRefs: [
      "CA2-CAP-DECIDE-EXACT-SESSION-ROLE-PERMISSION",
      "AF-RULE-UNIQUE-RESOLVED-SESSION",
      "AF-RULE-SESSION-CURRENT",
      "AF-RULE-TRUSTED-SCOPE",
      "AF-RULE-COMPLETE-ACTIVE-ROLES",
      "AF-RULE-AUTHORIZATION-ADMISSIBLE",
      "AF-RULE-EXACT-ACTIVE-ROLE-GRANT",
      "AF-RULE-ALLOW-IFF",
      "AF-RULE-DEFAULT-DENY",
    ],
  },
});

export class AuthKernelContractError extends Error {
  constructor(code, pointer, message) {
    super(`${code} ${pointer}: ${message}`);
    this.name = "AuthKernelContractError";
    this.code = code;
    this.pointer = pointer;
  }
}

function fail(code, pointer, message) {
  throw new AuthKernelContractError(code, pointer, message);
}

function sha256(bytes) {
  return crypto.createHash("sha256").update(bytes).digest("hex");
}

function prettyJson(value) {
  return `${JSON.stringify(value, null, 2)}\n`;
}

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function exactKeys(value, expected, pointer) {
  if (!isObject(value)) fail("AKC_SCHEMA", pointer, "expected object");
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  if (JSON.stringify(actual) !== JSON.stringify(wanted)) fail("AKC_SCHEMA", pointer, `expected keys ${wanted.join(", ")}`);
}

function same(actual, expected, pointer) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) fail("AKC_CONTRACT", pointer, `expected ${JSON.stringify(expected)}`);
}

function readRegular(root, relativePath, pointer) {
  const absolute = path.resolve(root, relativePath);
  const relative = path.relative(root, absolute);
  if (relative.startsWith("..") || path.isAbsolute(relative)) fail("AKC_PATH", pointer, "path escapes root");
  let stat;
  try {
    stat = fs.lstatSync(absolute);
  } catch {
    fail("AKC_MISSING", pointer, "file is missing");
  }
  if (stat.isSymbolicLink() || !stat.isFile()) fail("AKC_FILE", pointer, "expected regular non-symlink file");
  return { absolute, relativePath: relative.split(path.sep).join("/"), bytes: fs.readFileSync(absolute) };
}

function readJson(root, relativePath, pointer) {
  const source = readRegular(root, relativePath, pointer);
  try {
    return { ...source, value: JSON.parse(source.bytes.toString("utf8")) };
  } catch {
    fail("AKC_JSON", pointer, "invalid JSON");
  }
}

function validateEntity(node, expected, pointer) {
  exactKeys(node.body, ["fields", "definition_refs", "semantic_refs", "authority_effect"], `${pointer}/body`);
  same(node.body.authority_effect, "none", `${pointer}/body/authority_effect`);
  if (!Array.isArray(node.body.fields)) fail("AKC_SCHEMA", `${pointer}/body/fields`, "expected field array");
  const fields = node.body.fields.map((field, index) => {
    exactKeys(field, ["name", "type", "identity"], `${pointer}/body/fields/${index}`);
    return [field.name, field.type, field.identity];
  });
  same(fields, expected.fields, `${pointer}/body/fields`);
}

function validateRule(node, pointer) {
  exactKeys(node.body, ["formal_return_type", "definition_refs", "semantic_refs", "failure_behavior", "authority_effect"], `${pointer}/body`);
  same(node.body.formal_return_type, "boolean", `${pointer}/body/formal_return_type`);
  same(node.body.failure_behavior, "deny_without_state_change", `${pointer}/body/failure_behavior`);
  same(node.body.authority_effect, "none", `${pointer}/body/authority_effect`);
}

function validateNode(node, expected, pointer) {
  exactKeys(node, ["schema_version", "node_id", "feature_id", "kind", "intent", "body", "connections"], pointer);
  same(node.schema_version, "minted-node/v1", `${pointer}/schema_version`);
  same(node.node_id, expected.nodeId, `${pointer}/node_id`);
  same(node.feature_id, FEATURE_ID, `${pointer}/feature_id`);
  same(node.kind, expected.kind, `${pointer}/kind`);
  if (typeof node.intent !== "string" || node.intent.length === 0) fail("AKC_SCHEMA", `${pointer}/intent`, "expected nonempty intent");
  same(node.connections, [], `${pointer}/connections`);
  if (expected.kind === "Entity") validateEntity(node, expected, pointer);
  else validateRule(node, pointer);
  if (!Array.isArray(node.body.definition_refs) || node.body.definition_refs.length === 0) fail("AKC_SCHEMA", `${pointer}/body/definition_refs`, "expected nonempty definition refs");
  if (!Array.isArray(node.body.semantic_refs)) fail("AKC_SCHEMA", `${pointer}/body/semantic_refs`, "expected semantic refs");
  for (const semanticRef of expected.semanticRefs) {
    if (!node.body.semantic_refs.includes(semanticRef)) fail("AKC_SEMANTIC_REF", `${pointer}/body/semantic_refs`, `missing ${semanticRef}`);
  }
}

function verifyRealizationRow(repositoryRoot, baseline, metaTypeId) {
  const row = baseline.realization_rows.find((candidate) => candidate.meta_type_id === metaTypeId && candidate.language === "rust");
  if (!row) fail("AKC_BASELINE", `/realization_rows/${metaTypeId}/rust`, "missing Rust realization row");
  for (const key of ["source", "provider", "binding"]) {
    const record = row[key];
    if (!isObject(record) || typeof record.path !== "string" || typeof record.sha256 !== "string") fail("AKC_BASELINE", `/realization_rows/${metaTypeId}/rust/${key}`, "invalid bound file");
    const actual = sha256(readRegular(repositoryRoot, record.path, `/realization_rows/${metaTypeId}/rust/${key}`).bytes);
    same(actual, record.sha256, `/realization_rows/${metaTypeId}/rust/${key}/sha256`);
  }
  return row;
}

export function loadAuthKernelProject({ repositoryRoot = DEFAULT_REPOSITORY_ROOT, projectRoot }) {
  const repo = path.resolve(repositoryRoot);
  const root = path.resolve(projectRoot);
  const sources = [];
  const sourceJson = (relativePath, pointer) => {
    const source = readJson(root, relativePath, pointer);
    sources.push({ relativePath: source.relativePath, bytes: source.bytes });
    return source.value;
  };

  const instantiation = sourceJson("instantiation.json", "/instantiation.json");
  exactKeys(instantiation, ["schema_version", "profile_id", "baseline_ref", "product_capability_ref", "business_ontology_ref", "system_ontology_ref", "selected_meta_types", "language", "authority_effect", "external_effect"], "/instantiation.json");
  same(instantiation.schema_version, "domainspec.auth-kernel-instantiation/v1", "/instantiation.json/schema_version");
  same(instantiation.profile_id, "domainspec.rust-auth-exact-session-role-permission-kernel/v1", "/instantiation.json/profile_id");
  same(instantiation.product_capability_ref, "CA2-CAP-DECIDE-EXACT-SESSION-ROLE-PERMISSION", "/instantiation.json/product_capability_ref");
  same(instantiation.business_ontology_ref, "auth-foundation.business.exact-session-role-permission", "/instantiation.json/business_ontology_ref");
  same(instantiation.system_ontology_ref, "auth-foundation.system.exact-session-role-permission", "/instantiation.json/system_ontology_ref");
  same(instantiation.selected_meta_types, ["DS-D1.1", "DS-D1.7"], "/instantiation.json/selected_meta_types");
  same(instantiation.language, "rust", "/instantiation.json/language");
  same(instantiation.authority_effect, "none", "/instantiation.json/authority_effect");
  same(instantiation.external_effect, "none", "/instantiation.json/external_effect");

  const project = sourceJson("project.json", "/project.json");
  exactKeys(project, ["schema_version", "project_id", "language", "features", "generated_root"], "/project.json");
  same(project.schema_version, "minted-project/v1", "/project.json/schema_version");
  same(project.project_id, "auth-foundation-exact-permission", "/project.json/project_id");
  same(project.features, ["feature.json"], "/project.json/features");

  const feature = sourceJson("feature.json", "/feature.json");
  exactKeys(feature, ["schema_version", "feature_id", "source_layout", "node_sources"], "/feature.json");
  same(feature.schema_version, "minted-feature/v1", "/feature.json/schema_version");
  same(feature.feature_id, FEATURE_ID, "/feature.json/feature_id");
  same(feature.source_layout, "per-node-connections", "/feature.json/source_layout");
  same(feature.node_sources, Object.values(REQUIRED_NODES).map(({ source }) => source), "/feature.json/node_sources");

  const nodes = [];
  for (const expected of Object.values(REQUIRED_NODES)) {
    const node = sourceJson(expected.source, `/${expected.source}`);
    validateNode(node, expected, `/${expected.source}`);
    nodes.push(node);
  }

  exactKeys(instantiation.baseline_ref, ["id", "manifest", "manifest_sha256", "baseline_digest"], "/instantiation.json/baseline_ref");
  const baselineSource = readJson(repo, instantiation.baseline_ref.manifest, "/instantiation.json/baseline_ref/manifest");
  same(sha256(baselineSource.bytes), instantiation.baseline_ref.manifest_sha256, "/instantiation.json/baseline_ref/manifest_sha256");
  same(baselineSource.value.baseline_id, instantiation.baseline_ref.id, "/instantiation.json/baseline_ref/id");
  same(baselineSource.value.baseline_digest, instantiation.baseline_ref.baseline_digest, "/instantiation.json/baseline_ref/baseline_digest");
  const realizations = new Map([
    ["DS-D1.1", verifyRealizationRow(repo, baselineSource.value, "DS-D1.1")],
    ["DS-D1.7", verifyRealizationRow(repo, baselineSource.value, "DS-D1.7")],
  ]);

  const sourceRows = sources
    .sort((left, right) => left.relativePath.localeCompare(right.relativePath))
    .map(({ relativePath, bytes }) => ({ relative_path: relativePath, size_bytes: bytes.length, sha256: sha256(bytes) }));
  const sourceAggregate = sha256(sourceRows.map((row) => `${row.relative_path}\t${row.size_bytes}\t${row.sha256}\n`).join(""));
  return { instantiation, project, feature, nodes, sourceRows, sourceAggregate, realizations };
}

function renderTemplate(repositoryRoot, model) {
  const template = readRegular(repositoryRoot, TEMPLATE_PATH, "/template").bytes.toString("utf8");
  const replacements = new Map([
    ["{{BASELINE_ID}}", model.instantiation.baseline_ref.id],
    ["{{BASELINE_DIGEST}}", model.instantiation.baseline_ref.baseline_digest],
    ["{{SOURCE_AGGREGATE_SHA256}}", model.sourceAggregate],
    ["{{ENTITY_BINDING_SHA256}}", model.realizations.get("DS-D1.1").binding.sha256],
    ["{{RULE_BINDING_SHA256}}", model.realizations.get("DS-D1.7").binding.sha256],
  ]);
  let output = template;
  for (const [needle, value] of replacements) output = output.replaceAll(needle, value);
  if (output.includes("{{")) fail("AKC_TEMPLATE", "/template", "unresolved template placeholder");
  return Buffer.from(output);
}

function buildReceipt(model, libBytes) {
  return {
    schema_version: "domainspec.auth-kernel-instantiation-receipt/v1",
    project_id: model.project.project_id,
    feature_id: model.feature.feature_id,
    instantiation_profile: model.instantiation.profile_id,
    baseline: {
      id: model.instantiation.baseline_ref.id,
      manifest: model.instantiation.baseline_ref.manifest,
      manifest_sha256: model.instantiation.baseline_ref.manifest_sha256,
      baseline_digest: model.instantiation.baseline_ref.baseline_digest,
    },
    selected_dependencies: {
      product_capability_ref: model.instantiation.product_capability_ref,
      business_ontology_ref: model.instantiation.business_ontology_ref,
      system_ontology_ref: model.instantiation.system_ontology_ref,
      node_selectors: Object.values(REQUIRED_NODES).map(({ nodeId }) => `${FEATURE_ID}:${nodeId}`),
    },
    meta_type_bindings: Object.values(REQUIRED_NODES).map(({ nodeId, kind, metaTypeId }) => ({
      node_id: nodeId,
      kind,
      meta_type_id: metaTypeId,
      language: "rust",
      binding_sha256: model.realizations.get(metaTypeId).binding.sha256,
    })),
    source: { aggregate_sha256: model.sourceAggregate, files: model.sourceRows },
    artifacts: [{ relative_path: "src/lib.rs", size_bytes: libBytes.length, sha256: sha256(libBytes) }],
    deterministic_generation: true,
    authority_effect: "none",
    external_effect: "none",
    claim_ceiling: "candidate-static-rust-source-generation-and-local-conformance-evidence",
  };
}

export function renderAuthKernel(options) {
  const repositoryRoot = path.resolve(options.repositoryRoot ?? DEFAULT_REPOSITORY_ROOT);
  const model = loadAuthKernelProject({ repositoryRoot, projectRoot: options.projectRoot });
  const libBytes = renderTemplate(repositoryRoot, model);
  const outputs = new Map([
    ["src/lib.rs", libBytes],
    [RECEIPT_PATH, Buffer.from(prettyJson(buildReceipt(model, libBytes)))],
  ]);
  return { model, outputs };
}

function atomicWrite(target, bytes) {
  fs.mkdirSync(path.dirname(target), { recursive: true });
  const temporary = `${target}.tmp-${process.pid}`;
  fs.writeFileSync(temporary, bytes);
  fs.renameSync(temporary, target);
}

export function materializeAuthKernel(options) {
  const rendered = renderAuthKernel(options);
  const outputRoot = path.resolve(options.outputRoot);
  for (const [relativePath, bytes] of rendered.outputs) atomicWrite(path.join(outputRoot, relativePath), bytes);
  return rendered;
}

export function checkAuthKernel(options) {
  const rendered = renderAuthKernel(options);
  const outputRoot = path.resolve(options.outputRoot);
  const differences = [];
  for (const [relativePath, expected] of rendered.outputs) {
    const target = path.join(outputRoot, relativePath);
    if (!fs.existsSync(target)) differences.push({ relative_path: relativePath, status: "missing" });
    else if (!fs.readFileSync(target).equals(expected)) differences.push({ relative_path: relativePath, status: "drift" });
  }
  if (differences.length > 0) fail("AKC_TARGET_DRIFT", "/output", JSON.stringify(differences));
  return rendered;
}

function usage() {
  return "usage: auth-kernel.mjs <generate|check> <absolute-project-root> <absolute-output-root>";
}

if (process.argv[1] && path.resolve(process.argv[1]) === TOOL_PATH) {
  const [mode, projectRoot, outputRoot] = process.argv.slice(2);
  if (!["generate", "check"].includes(mode) || !path.isAbsolute(projectRoot ?? "") || !path.isAbsolute(outputRoot ?? "")) {
    console.error(usage());
    process.exitCode = 2;
  } else {
    try {
      const result = mode === "generate"
        ? materializeAuthKernel({ projectRoot, outputRoot })
        : checkAuthKernel({ projectRoot, outputRoot });
      console.log(JSON.stringify({
        status: "PASS",
        mode,
        project_id: result.model.project.project_id,
        source_aggregate_sha256: result.model.sourceAggregate,
        baseline_id: result.model.instantiation.baseline_ref.id,
        authority_effect: "none",
        external_effect: "none",
      }));
    } catch (error) {
      console.error(error instanceof Error ? error.message : String(error));
      process.exitCode = 1;
    }
  }
}
