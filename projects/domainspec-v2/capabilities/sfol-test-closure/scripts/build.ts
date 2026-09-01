import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { compileMintedProject } from "../../../impl/tools/minted-project/compiler.ts";

const capabilityRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const domainspecRoot = resolve(capabilityRoot, "domainspec");
const repositoryProjectsRoot = resolve(capabilityRoot, "../..");
const generatedRoot = resolve(capabilityRoot, "generated");
const profilePath = resolve(domainspecRoot, "development-profile.json");

function sha256(value: string | Buffer): string {
  return createHash("sha256").update(value).digest("hex");
}

function stable(value: unknown): string {
  return `${JSON.stringify(value, null, 2)}\n`;
}

function json(path: string): any {
  return JSON.parse(readFileSync(path, "utf8"));
}

function write(path: string, value: unknown): string {
  const bytes = stable(value);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, bytes);
  return sha256(bytes);
}

const first = compileMintedProject(domainspecRoot, {
  developmentProfileRegistry: {
    path: profilePath,
    handle: "sfol-test-closure-development-explicit-v0.1",
  },
});
const second = compileMintedProject(domainspecRoot, {
  developmentProfileRegistry: {
    path: profilePath,
    handle: "sfol-test-closure-development-explicit-v0.1",
  },
});
if (first.graphBytes !== second.graphBytes || first.sourceManifestBytes !== second.sourceManifestBytes) {
  throw new Error("SFOL_TEST_CLOSURE_NONDETERMINISTIC_COMPILE");
}

const graphDigest = sha256(first.graphBytes);
const manifestDigest = sha256(first.sourceManifestBytes);
const implementationMap = json(resolve(capabilityRoot, "implementation-map.json"));
const graphNodeIds = new Set(first.graph.nodes.map(({ node_id }) => node_id));
const components = implementationMap.components.map((component: any) => {
  for (const nodeId of component.operation_node_ids) {
    if (!graphNodeIds.has(nodeId)) throw new Error(`SFOL_IMPLEMENTATION_OPERATION_MISSING:${nodeId}`);
  }
  const bindings = component.implementation_paths.map((path: string) => {
    const absolute = resolve(repositoryProjectsRoot, path);
    return { path, sha256: sha256(readFileSync(absolute)) };
  });
  return { ...component, bindings };
}).sort((left: any, right: any) => left.component_id.localeCompare(right.component_id));

const systemOntology = {
  schema_version: "domainspec-compiled-system-ontology/v1",
  ontology_id: "DSV2-SYSTEM-ONTOLOGY-SFOL-TEST-CLOSURE",
  authority: "generated-candidate-read-model",
  source_graph_digest: graphDigest,
  source_manifest_digest: manifestDigest,
  development_profile_digest: sha256(readFileSync(profilePath)),
  components,
  admission: "not-granted",
};
const systemOntologyBytes = stable(systemOntology);
const systemOntologyDigest = sha256(systemOntologyBytes);
const graphPath = resolve(generatedRoot, "compiled-graph.json");
const manifestPath = resolve(generatedRoot, "source-manifest.json");
const ontologyPath = resolve(generatedRoot, "system-ontology.json");
mkdirSync(generatedRoot, { recursive: true });
writeFileSync(graphPath, first.graphBytes);
writeFileSync(manifestPath, first.sourceManifestBytes);
writeFileSync(ontologyPath, systemOntologyBytes);

const buildReceipt = {
  schema_version: "domainspec-sfol-test-closure-build-receipt/v1",
  result: "pass",
  compile_runs: 2,
  byte_identical: true,
  source_set_digest: first.graph.source_set_digest,
  compiled_graph_sha256: graphDigest,
  source_manifest_sha256: manifestDigest,
  system_ontology_sha256: systemOntologyDigest,
  development_profile_sha256: sha256(readFileSync(profilePath)),
  authority_effect: "none",
};
const buildReceiptDigest = write(resolve(generatedRoot, "build-receipt.json"), buildReceipt);

write(resolve(capabilityRoot, "construction-binding.json"), {
  schema_version: "cyberalchemy-construction-binding/v1",
  binding_id: "CAV2-D65-SFOL-TEST-CLOSURE-001",
  chain: {
    definitions: { path: "definition-candidates.json", status: "candidate-awaiting-decision" },
    product_capability: { path: "product-capability.json", status: "candidate-not-adopted" },
    business_ontology: { path: "business-ontology.json", status: "candidate-not-admitted" },
    domainspec_source: { path: "domainspec/project.json", source_set_digest: first.graph.source_set_digest, status: "compiled-development-candidate" },
    system_ontology: { path: "generated/system-ontology.json", sha256: systemOntologyDigest, status: "generated-candidate-not-admitted" },
    implementation_binding: { path: "implementation-map.json", sha256: sha256(readFileSync(resolve(capabilityRoot, "implementation-map.json"))), status: "exact-byte-bound" },
    conformance_evidence: { path: "conformance/evidence.json", status: "pending-validation-run" }
  },
  build_receipt: { path: "generated/build-receipt.json", sha256: buildReceiptDigest },
  result: "not_evaluable",
  blockers: ["definition admission", "Product Capability adoption", "business ontology admission", "system ontology admission", "conformance evidence"],
  claim_limit: "Development candidate compilation and exact implementation binding only; no admission, publication, deployment, or production-security authority."
});

process.stdout.write(`${stable({ result: "pass", nodes: first.graph.nodes.length, edges: first.graph.edges.length, graph_sha256: graphDigest, system_ontology_sha256: systemOntologyDigest })}`);
