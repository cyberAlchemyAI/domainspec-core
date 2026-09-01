import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import {
  buildMintedProjectViews,
  verifyMintedProjectBuild,
} from "../../../domainspec-v2/impl/tools/minted-project/views";

type JsonObject = Record<string, any>;

const scriptDir = dirname(fileURLToPath(import.meta.url));
const implementationRoot = resolve(scriptDir, "..");
const authRoot = resolve(implementationRoot, "..");
const repositoryRoot = resolve(authRoot, "../..");
const domainspecRoot = resolve(implementationRoot, "domainspec");
const generatedRoot = resolve(domainspecRoot, "generated");
const runtimeRoot = resolve(implementationRoot, "runtime");
const constructionBindingPath = resolve(domainspecRoot, "construction-binding.json");
const authKernelToolPath = resolve(repositoryRoot, "projects/domainspec-v2/impl/cli/tools/auth-kernel.mjs");
const authKernelTemplatePath = resolve(repositoryRoot, "projects/domainspec-v2/impl/cli/templates/auth-kernel/lib.rs.tmpl");
const authKernelReceiptPath = resolve(runtimeRoot, "DOMAINSPEC-INSTANTIATION-RECEIPT.json");
const check = process.argv.includes("--check");

function sha256(value: string | Buffer): string {
  return createHash("sha256").update(value).digest("hex");
}

function bytes(value: unknown): string {
  return `${JSON.stringify(value, null, 2)}\n`;
}

function readJson(path: string): JsonObject {
  return JSON.parse(readFileSync(path, "utf8")) as JsonObject;
}

function assert(condition: unknown, code: string): asserts condition {
  if (!condition) throw new Error(code);
}

function sortedUnique(values: string[]): string[] {
  return [...new Set(values)].sort();
}

function sameMembers(actual: string[], expected: string[]): boolean {
  return JSON.stringify(sortedUnique(actual)) === JSON.stringify(sortedUnique(expected));
}

function resolveAuth(path: string): string {
  return resolve(authRoot, path);
}

function verifyPredecessors(binding: JsonObject): {
  capability: JsonObject;
  ontology: JsonObject;
  definitionIds: string[];
} {
  assert(binding.schema_version === "cav2-d65-domainspec-construction-binding/v1", "CONSTRUCTION_BINDING_SCHEMA_INVALID");
  assert(binding.route_id === "CA2-ROUTE-IMPLEMENT", "CONSTRUCTION_ROUTE_INVALID");
  const predecessors = binding.predecessors as JsonObject;

  for (const name of ["canonical_definitions", "language_context", "product_capability", "business_ontology", "formal_evidence"]) {
    const predecessor = predecessors[name] as JsonObject;
    assert(predecessor?.path && predecessor?.sha256, `PREDECESSOR_BINDING_MISSING:${name}`);
    const actual = sha256(readFileSync(resolveAuth(predecessor.path)));
    assert(actual === predecessor.sha256, `PREDECESSOR_DIGEST_DRIFT:${name}:${actual}`);
  }

  const definitions = readJson(resolveAuth(predecessors.canonical_definitions.path));
  const context = readJson(resolveAuth(predecessors.language_context.path));
  const capability = readJson(resolveAuth(predecessors.product_capability.path));
  const ontology = readJson(resolveAuth(predecessors.business_ontology.path));
  const theoremReceipt = readJson(resolveAuth(predecessors.formal_evidence.path));
  const definitionIds = sortedUnique((definitions.definitions as JsonObject[]).map((entry) => entry.definition_id));

  assert(definitions.status === "accepted", "CANONICAL_DEFINITIONS_NOT_ACCEPTED");
  assert(sameMembers(definitionIds, predecessors.canonical_definitions.selected_ids), "DEFINITION_SELECTION_MISMATCH");
  assert(sameMembers(context.bindings.map((entry: JsonObject) => entry.definition_id), definitionIds), "LANGUAGE_CONTEXT_COVERAGE_FAILED");
  assert(capability.capability_id === predecessors.product_capability.capability_id, "CAPABILITY_ID_MISMATCH");
  assert(capability.business_ontology_ref === predecessors.business_ontology.ontology_id, "CAPABILITY_ONTOLOGY_MISMATCH");
  assert(ontology.ontology_id === predecessors.business_ontology.ontology_id, "BUSINESS_ONTOLOGY_ID_MISMATCH");
  assert(ontology.capability_ref === capability.capability_id, "BUSINESS_ONTOLOGY_CAPABILITY_MISMATCH");
  assert(ontology.lifecycle_status === predecessors.business_ontology.required_lifecycle_status, "BUSINESS_ONTOLOGY_STATUS_MISMATCH");
  assert(ontology.definition_source.sha256 === predecessors.canonical_definitions.sha256, "BUSINESS_ONTOLOGY_DEFINITION_DIGEST_MISMATCH");
  assert(sameMembers(ontology.definition_source.definition_ids, definitionIds), "BUSINESS_ONTOLOGY_DEFINITION_COVERAGE_FAILED");
  assert(theoremReceipt.proof_status === predecessors.formal_evidence.proof_status, "FORMAL_EVIDENCE_STATUS_MISMATCH");
  assert(theoremReceipt.normalized_outcome === "theorem-checked", "FORMAL_EVIDENCE_OUTCOME_INVALID");
  return { capability, ontology, definitionIds };
}

function verifyCoverage(graph: JsonObject, capability: JsonObject, ontology: JsonObject, definitionIds: string[]) {
  const definitionRefs = sortedUnique(graph.nodes.flatMap((node: JsonObject) => node.body?.definition_refs ?? []));
  const semanticRefs = sortedUnique(graph.nodes.flatMap((node: JsonObject) => node.body?.semantic_refs ?? []));
  const allowedSemanticRefs = sortedUnique([
    capability.capability_id,
    ...ontology.nodes.map((entry: JsonObject) => entry.id),
    ...ontology.rules.map((entry: JsonObject) => entry.rule_id),
    ...ontology.proof_requirements.map((entry: JsonObject) => entry.proof_id),
  ]);
  const requiredSemanticRefs = sortedUnique([
    capability.capability_id,
    ...ontology.rules.map((entry: JsonObject) => entry.rule_id),
    ...ontology.proof_requirements.map((entry: JsonObject) => entry.proof_id),
  ]);
  assert(sameMembers(definitionRefs, definitionIds), "DOMAINSPEC_DEFINITION_COVERAGE_FAILED");
  assert(semanticRefs.every((ref) => allowedSemanticRefs.includes(ref)), "DOMAINSPEC_UNKNOWN_SEMANTIC_REF");
  assert(requiredSemanticRefs.every((ref) => semanticRefs.includes(ref)), "DOMAINSPEC_SEMANTIC_COVERAGE_FAILED");
  assert(graph.nodes.every((node: JsonObject) => node.body?.authority_effect === "none"), "DOMAINSPEC_NODE_AUTHORITY_INVALID");
  return { definitionRefs, semanticRefs, requiredSemanticRefs };
}

function buildArtifacts(): Record<string, string> {
  const binding = readJson(constructionBindingPath);
  const { capability, ontology, definitionIds } = verifyPredecessors(binding);
  execFileSync(process.execPath, [authKernelToolPath, check ? "check" : "generate", domainspecRoot, runtimeRoot], {
    cwd: repositoryRoot,
    stdio: "pipe",
  });
  const authKernelReceipt = readJson(authKernelReceiptPath);
  assert(authKernelReceipt.schema_version === "domainspec.auth-kernel-instantiation-receipt/v1", "AUTH_KERNEL_RECEIPT_SCHEMA_INVALID");
  assert(authKernelReceipt.baseline.id === "domainspec-meta-types-current-implemented@10", "AUTH_KERNEL_BASELINE_INVALID");
  const options = {
    developmentProfileRegistry: {
      path: resolve(domainspecRoot, "development-profile.json"),
      handle: "auth-foundation-development-explicit-v0.1",
    },
  };
  const first = buildMintedProjectViews(domainspecRoot, options);
  const second = buildMintedProjectViews(domainspecRoot, options);
  const firstVerification = verifyMintedProjectBuild(domainspecRoot, first);
  const secondVerification = verifyMintedProjectBuild(domainspecRoot, second);
  assert(firstVerification.status === "pass", `DOMAINSPEC_BUILD_INVALID:${firstVerification.codes.join(",")}`);
  assert(secondVerification.status === "pass", `DOMAINSPEC_BUILD_INVALID:${secondVerification.codes.join(",")}`);
  for (const key of ["graphBytes", "sourceManifestBytes", "markdownBytes", "markdownViewBytes", "buildReceiptBytes"] as const) {
    assert(first[key] === second[key], `NON_DETERMINISTIC_DOMAINSPEC_BUILD:${key}`);
  }
  const coverage = verifyCoverage(first.graph, capability, ontology, definitionIds);
  verifyCoverage(second.graph, capability, ontology, definitionIds);

  const compilerPath = resolve(repositoryRoot, "projects/domainspec-v2/impl/tools/minted-project/compiler.ts");
  const viewsPath = resolve(repositoryRoot, "projects/domainspec-v2/impl/tools/minted-project/views.ts");
  const constructionBindingDigest = sha256(readFileSync(constructionBindingPath));
  const graphDigest = sha256(first.graphBytes);
  const systemOntology = {
    schema_version: "auth-foundation.system-ontology/v1-candidate",
    ontology_id: "auth-foundation.system.exact-session-role-permission",
    ontology_type: "system",
    lifecycle_status: "validated-local-candidate",
    authority: "generated-system-ontology-read-model",
    authority_effect: "none",
    predecessor_bindings: binding.predecessors,
    construction_binding: {
      binding_id: binding.binding_id,
      path: "implementation/domainspec/construction-binding.json",
      sha256: constructionBindingDigest,
    },
    source_project_id: first.graph.project_id,
    source_set_digest: first.graph.source_set_digest,
    source_graph_digest: graphDigest,
    compiler: {
      id: "domainspec-v2-minted-project-tools",
      version: "minted-project-tools/v1",
      compiler_path: "projects/domainspec-v2/impl/tools/minted-project/compiler.ts",
      compiler_sha256: sha256(readFileSync(compilerPath)),
      views_path: "projects/domainspec-v2/impl/tools/minted-project/views.ts",
      views_sha256: sha256(readFileSync(viewsPath)),
      profile_id: first.buildReceipt.language.profile_id,
      profile_version: first.buildReceipt.language.profile_version,
      profile_digest: first.buildReceipt.language.profile_digest,
    },
    semantic_coverage: {
      selected_definition_ids: coverage.definitionRefs,
      required_semantic_refs: coverage.requiredSemanticRefs,
      authored_semantic_refs: coverage.semanticRefs,
      status: "closed",
    },
    nodes: first.graph.nodes,
    edges: first.graph.edges,
    implementation_contract: {
      operation: "authorize",
      input: "EvaluationContext",
      output: "AuthorizationDecision::{Allow,Deny}",
      allow_rule: "AF-RULE-ALLOW-IFF",
      fallback_rule: "AF-RULE-DEFAULT-DENY",
      exact_match_components: ["resource", "action", "scope"],
      external_boundaries: ["session-resolution", "role-resolution", "trusted-scope-construction", "authorization-revision-source"],
      side_effects: "none",
    },
  };
  const systemOntologyBytes = bytes(systemOntology);
  const systemOntologyDigest = sha256(systemOntologyBytes);
  const projectionReceipt = {
    schema_version: "auth-foundation.system-ontology-projection/v1",
    status: "pass",
    deterministic_runs: 2,
    equal_graph_bytes: first.graphBytes === second.graphBytes,
    equal_system_ontology_bytes: true,
    predecessor_verification: "pass",
    semantic_coverage: "closed",
    source_graph_digest: graphDigest,
    system_ontology_digest: systemOntologyDigest,
    authority_effect: "none",
    claim_limit: "Deterministic local candidate projection only.",
  };

  const runtimeFiles = {
    manifest: "implementation/runtime/Cargo.toml",
    lockfile: "implementation/runtime/Cargo.lock",
    source: "implementation/runtime/src/lib.rs",
    tests: "implementation/runtime/tests/kernel.rs",
    instantiation_receipt: "implementation/runtime/DOMAINSPEC-INSTANTIATION-RECEIPT.json",
  };
  const implementationBinding = {
    schema_version: "auth-foundation.rust-implementation-binding/v1-candidate",
    binding_id: "AUTH-D65-RUST-EXACT-PERMISSION-001",
    route_id: "CA2-ROUTE-IMPLEMENT",
    lifecycle_status: "implemented-local-candidate",
    bound_predecessor: {
      ontology_id: systemOntology.ontology_id,
      system_ontology_path: "implementation/domainspec/generated/system-ontology.json",
      system_ontology_sha256: systemOntologyDigest,
      source_graph_sha256: graphDigest,
    },
    implementation: {
      language: "rust",
      crate: "auth-foundation-kernel",
      generated: true,
      generator: {
        id: "domainspec-v2-auth-kernel-cli/v1",
        tool_path: "projects/domainspec-v2/impl/cli/tools/auth-kernel.mjs",
        tool_sha256: sha256(readFileSync(authKernelToolPath)),
        template_path: "projects/domainspec-v2/impl/cli/templates/auth-kernel/lib.rs.tmpl",
        template_sha256: sha256(readFileSync(authKernelTemplatePath)),
        receipt_path: "implementation/runtime/DOMAINSPEC-INSTANTIATION-RECEIPT.json",
        receipt_sha256: sha256(readFileSync(authKernelReceiptPath)),
        baseline_id: authKernelReceipt.baseline.id,
        source_aggregate_sha256: authKernelReceipt.source.aggregate_sha256,
      },
      files: Object.fromEntries(Object.entries(runtimeFiles).map(([name, path]) => [name, { path, sha256: sha256(readFileSync(resolveAuth(path))) }])),
      entrypoint: "auth_foundation_kernel::authorize",
    },
    boundaries: systemOntology.implementation_contract.external_boundaries,
    authority_effect: "none",
    external_effect: "none",
    claim_limit: "Deterministically generated local Rust source and authored conformance tests bound to the Auth system ontology; no service or production claim.",
  };
  const implementationBindingBytes = bytes(implementationBinding);

  return {
    "graph.json": first.graphBytes,
    "source-manifest.json": first.sourceManifestBytes,
    "SPEC.md": first.markdownBytes,
    "markdown-view.json": first.markdownViewBytes,
    "build-receipt.json": first.buildReceiptBytes,
    "system-ontology.json": systemOntologyBytes,
    "system-ontology-receipt.json": bytes(projectionReceipt),
    "../runtime/implementation-binding.json": implementationBindingBytes,
  };
}

const artifacts = buildArtifacts();
for (const [name, content] of Object.entries(artifacts)) {
  const path = name.startsWith("../runtime/")
    ? resolve(implementationRoot, name.slice(3))
    : resolve(generatedRoot, name);
  if (check) {
    assert(readFileSync(path, "utf8") === content, `GENERATED_ARTIFACT_DRIFT:${name}`);
  } else {
    mkdirSync(dirname(path), { recursive: true });
    writeFileSync(path, content, "utf8");
  }
}
process.stdout.write(`${check ? "checked" : "built"}=${Object.keys(artifacts).length}\n`);
