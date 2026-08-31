import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { buildMintedProjectViews } from "../../../projects/domainspec-v2/impl/tools/minted-project/views";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const packageRoot = resolve(scriptDir, "..");
const repositoryRoot = resolve(packageRoot, "../..");
const projectRoot = resolve(packageRoot, "domainspec");
const generatedRoot = resolve(projectRoot, "generated");

function sha256(value: string | Buffer): string {
  return createHash("sha256").update(value).digest("hex");
}

function bytes(value: unknown): string {
  return `${JSON.stringify(value, null, 2)}\n`;
}

type SemanticBinding = {
  id: string;
  path: string;
  scope_kind: "whole-file" | "heading-section";
  selector: string | null;
  sha256: string;
};

function headingSection(path: string, selector: string): Buffer {
  const lines = readFileSync(path, "utf8").match(/.*(?:\r?\n|$)/g)?.filter(Boolean) ?? [];
  const start = lines.findIndex((line) => line.replace(/\r?\n$/, "") === selector);
  if (start < 0) throw new Error(`SEMANTIC_SELECTOR_NOT_FOUND:${selector}`);
  let end = lines.length;
  for (let index = start + 1; index < lines.length; index += 1) {
    if (lines[index].startsWith("## ")) {
      end = index;
      break;
    }
  }
  return Buffer.from(lines.slice(start, end).join(""));
}

function verifySemanticBindings(): SemanticBinding[] {
  const nodePath = resolve(projectRoot, "nodes/cyberalchemy-route-resolution.json");
  const node = JSON.parse(readFileSync(nodePath, "utf8"));
  const bindings = node?.body?.semantic_bindings as SemanticBinding[];
  if (!Array.isArray(bindings) || bindings.length === 0) {
    throw new Error("SEMANTIC_BINDINGS_MISSING");
  }
  for (const binding of bindings) {
    const path = resolve(repositoryRoot, binding.path);
    const selected = binding.scope_kind === "whole-file"
      ? readFileSync(path)
      : headingSection(path, String(binding.selector));
    const actual = sha256(selected);
    if (actual !== binding.sha256) {
      throw new Error(`SEMANTIC_BINDING_DRIFT:${binding.id}:${actual}`);
    }
  }
  return bindings;
}

function build() {
  const semanticBindings = verifySemanticBindings();
  const options = {
    developmentProfileRegistry: {
      path: resolve(projectRoot, "development-profile.json"),
      handle: "cyberalchemy-agent-routing-development-explicit-v0.1",
    },
  };
  const first = buildMintedProjectViews(projectRoot, options);
  const second = buildMintedProjectViews(projectRoot, options);
  for (const key of ["graphBytes", "sourceManifestBytes", "markdownBytes", "markdownViewBytes", "buildReceiptBytes"] as const) {
    if (first[key] !== second[key]) {
      throw new Error(`NON_DETERMINISTIC_DOMAINSPEC_BUILD:${key}`);
    }
  }

  const compilerPath = resolve(repositoryRoot, "projects/domainspec-v2/impl/tools/minted-project/compiler.ts");
  const viewsPath = resolve(repositoryRoot, "projects/domainspec-v2/impl/tools/minted-project/views.ts");
  const projectionBuilderPath = resolve(packageRoot, "scripts/build.ts");
  const routesPath = resolve(packageRoot, "routes.json");
  const validatorPath = resolve(packageRoot, "scripts/validate.py");
  const agentsPath = resolve(repositoryRoot, "AGENTS.md");
  const sourceMapPath = resolve(repositoryRoot, "cyberAlchemy-v2/SOURCE-MAP.md");
  const systemOntology = {
    schema_version: "cav2-agent-routing-system-ontology/v1",
    ontology_id: "cav2.agent-routing.system",
    authority: "generated-system-ontology-read-model",
    authority_effect: "none",
    source_project_id: first.graph.project_id,
    source_set_digest: first.graph.source_set_digest,
    source_graph_digest: sha256(first.graphBytes),
    construction_inputs: semanticBindings,
    compiler: {
      id: "domainspec-v2-minted-project-tools",
      version: "minted-project-tools/v1",
      compiler_path: "projects/domainspec-v2/impl/tools/minted-project/compiler.ts",
      compiler_sha256: sha256(readFileSync(compilerPath)),
      views_path: "projects/domainspec-v2/impl/tools/minted-project/views.ts",
      views_sha256: sha256(readFileSync(viewsPath)),
      projection_builder_path: "cyberAlchemy-v2/agent-routing/scripts/build.ts",
      projection_builder_sha256: sha256(readFileSync(projectionBuilderPath)),
    },
    nodes: first.graph.nodes,
    edges: first.graph.edges,
    implementation_contract: {
      product_capability_ref: "CA2-CAP-ROUTE-REPOSITORY-WORK",
      route_registry_ref: "cyberAlchemy-v2/agent-routing/routes.json",
      route_registry_sha256: sha256(readFileSync(routesPath)),
      ontology_enforcement: "suspended-pending-governed-rust-binding",
      validator_ref: "cyberAlchemy-v2/agent-routing/scripts/validate.py",
      validator_sha256: sha256(readFileSync(validatorPath)),
      root_instruction_ref: "AGENTS.md",
      root_instruction_sha256: sha256(readFileSync(agentsPath)),
      source_map_ref: "cyberAlchemy-v2/SOURCE-MAP.md",
      source_map_sha256: sha256(readFileSync(sourceMapPath)),
      fallback_policy: "forbidden",
      accepted_baseline_required: true,
      authority_effect: "none",
    },
  };
  const systemOntologyBytes = bytes(systemOntology);
  const projectionReceipt = {
    schema_version: "cav2-agent-routing-system-ontology-projection/v1",
    status: "candidate",
    deterministic_runs: 2,
    equal_graph_bytes: true,
    equal_system_ontology_bytes: true,
    source_graph_digest: sha256(first.graphBytes),
    system_ontology_digest: sha256(systemOntologyBytes),
    profile_id: first.buildReceipt.language.profile_id,
    profile_version: first.buildReceipt.language.profile_version,
    profile_digest: first.buildReceipt.language.profile_digest,
    profile_release_admission: "not-granted",
    authority_effect: "none",
    claim_limit: "Deterministic candidate router projection only; no profile or system-ontology admission, complete capability realization, conformance, publication, release, deployment, or external effect.",
  };

  return {
    "graph.json": first.graphBytes,
    "source-manifest.json": first.sourceManifestBytes,
    "SPEC.md": first.markdownBytes,
    "markdown-view.json": first.markdownViewBytes,
    "build-receipt.json": first.buildReceiptBytes,
    "system-ontology.json": systemOntologyBytes,
    "system-ontology-receipt.json": bytes(projectionReceipt),
  };
}

const artifacts = build();
if (process.argv.includes("--emit-json")) {
  process.stdout.write(bytes(artifacts));
} else {
  mkdirSync(generatedRoot, { recursive: true });
  for (const [name, content] of Object.entries(artifacts)) {
    writeFileSync(resolve(generatedRoot, name), content, "utf8");
  }
  process.stdout.write(`built=${Object.keys(artifacts).length}\n`);
}
