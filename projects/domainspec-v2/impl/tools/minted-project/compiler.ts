import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { dirname, posix, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import {
  resolveMintedProjectSources,
  type MintedProjectSourceRecord,
} from "./resolver";
import { validateJsonSchema, type JsonObject, type JsonSchemaViolation } from "./schema-validator";

export const MINTED_PROJECT_COMPILER_ERROR_CODES = [
  "PROJECT_SCHEMA_INVALID",
  "FEATURE_SCHEMA_INVALID",
  "NODE_SCHEMA_INVALID",
  "PROFILE_UNSUPPORTED",
  "PROFILE_DIGEST_MISMATCH",
  "REGISTRY_DIGEST_MISMATCH",
  "PROFILE_RELATIONSHIP_INVALID",
  "KIND_UNSUPPORTED",
  "FORMATION_INVALID",
  "NODE_FEATURE_MISMATCH",
  "NODE_ID_DUPLICATE",
  "EDGE_ID_DUPLICATE",
  "EDGE_TYPE_UNKNOWN",
  "EDGE_TYPE_GENERATED",
  "EDGE_TYPE_DEPRECATED",
  "EDGE_TYPE_DEFERRED",
  "EDGE_TYPE_UNSUPPORTED_PROFILE",
  "EDGE_ENDPOINT_MISSING",
  "EDGE_ENDPOINT_KIND_MISMATCH",
  "CROSS_FEATURE_UNSUPPORTED",
  "GENERATED_GRAPH_INVALID",
  "GENERATED_MANIFEST_INVALID",
] as const;

export type MintedProjectCompilerErrorCode =
  (typeof MINTED_PROJECT_COMPILER_ERROR_CODES)[number];

export class MintedProjectCompilerError extends Error {
  readonly code: MintedProjectCompilerErrorCode;
  readonly sourcePath: string;

  constructor(code: MintedProjectCompilerErrorCode, sourcePath: string, detail: string) {
    super(`${code}:${sourcePath}:${detail}`);
    this.name = "MintedProjectCompilerError";
    this.code = code;
    this.sourcePath = sourcePath;
  }
}

type RelationshipSignature = {
  id: string;
  status?: string;
  source_type?: string;
  source_types?: string[];
  target_type?: string;
  target_types?: string[];
};

export type RelationshipRegistrySlice = {
  signatures: RelationshipSignature[];
  generated_views?: Array<{ id: string }>;
};

type ProfileRelationship = {
  id: string;
  source_kind: string;
  target_kind: string;
  registry_status: string;
};

type SupportedProfile = {
  id: string;
  version: string;
  status: string;
  source_layout: string;
  kinds: string[];
  formation_schemas: Record<string, string>;
  relationships: ProfileRelationship[];
};

type ProfileRegistry = {
  registry_bindings: {
    kinds: { path: string; sha256: string };
    relationships: { path: string; sha256: string };
  };
  profiles: SupportedProfile[];
};

type SourceNode = {
  schema_version: string;
  node_id: string;
  feature_id: string;
  kind: string;
  intent: string;
  body: JsonObject;
  connections: Array<{ edge_id: string; type: string; to: string }>;
};

export interface MintedGraph {
  schema_version: "minted-graph/v1";
  authority: "generated-semantic-read-model";
  project_id: string;
  language: {
    profile_digest: string;
    kinds_digest: string;
    relationships_digest: string;
  };
  source_set_digest: string;
  nodes: Array<Omit<SourceNode, "schema_version" | "connections">>;
  edges: Array<{ edge_id: string; type: string; from: string; to: string }>;
}

export interface MintedSourceManifest {
  schema_version: "minted-source-manifest/v1";
  authority: "generated-provenance-read-model";
  project_id: string;
  source_set_digest: string;
  inputs: MintedProjectSourceRecord[];
  records: Array<{
    record_type: "node" | "edge";
    graph_id: string;
    source_path: string;
    source_digest: string;
  }>;
}

export interface CompiledMintedProject {
  graph: MintedGraph;
  sourceManifest: MintedSourceManifest;
  graphBytes: string;
  sourceManifestBytes: string;
}

const implRoot = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const domainspecRoot = resolve(implRoot, "..");

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8")) as T;
}

function sha256File(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function failSchema(
  code: MintedProjectCompilerErrorCode,
  sourcePath: string,
  violations: JsonSchemaViolation[],
): never {
  throw new MintedProjectCompilerError(code, sourcePath, JSON.stringify(violations));
}

function sourcePath(declaringPath: string, reference: string): string {
  return posix.normalize(posix.join(posix.dirname(declaringPath), reference.replaceAll("\\", "/")));
}

function signatureTypes(signature: RelationshipSignature, side: "source" | "target"): string[] {
  const singular = side === "source" ? signature.source_type : signature.target_type;
  const plural = side === "source" ? signature.source_types : signature.target_types;
  return singular ? [singular] : plural ?? [];
}

export function classifyRelationshipType(
  type: string,
  registry: RelationshipRegistrySlice,
  profileRelationships: ProfileRelationship[],
): MintedProjectCompilerErrorCode | "active-profile" {
  if ((registry.generated_views ?? []).some((entry) => entry.id === type)) {
    return "EDGE_TYPE_GENERATED";
  }
  const signatures = registry.signatures.filter((entry) => entry.id === type);
  if (signatures.length === 0) {
    return "EDGE_TYPE_UNKNOWN";
  }
  if (signatures.some((entry) => entry.status === "deprecated")) {
    return "EDGE_TYPE_DEPRECATED";
  }
  if (signatures.some((entry) => entry.status === "deferred")) {
    return "EDGE_TYPE_DEFERRED";
  }
  if (!profileRelationships.some((entry) => entry.id === type)) {
    return "EDGE_TYPE_UNSUPPORTED_PROFILE";
  }
  return "active-profile";
}

export function compileMintedProject(projectRoot: string): CompiledMintedProject {
  const resolution = resolveMintedProjectSources(projectRoot);
  const profilePath = resolve(domainspecRoot, "definitions/minted-project/supported-profiles.yml");
  const profileRegistry = readJson<ProfileRegistry>(profilePath);
  const relationshipsPath = resolve(
    domainspecRoot,
    profileRegistry.registry_bindings.relationships.path,
  );
  const kindsPath = resolve(domainspecRoot, profileRegistry.registry_bindings.kinds.path);
  const relationships = readJson<RelationshipRegistrySlice>(relationshipsPath);
  if (
    sha256File(kindsPath) !== profileRegistry.registry_bindings.kinds.sha256 ||
    sha256File(relationshipsPath) !== profileRegistry.registry_bindings.relationships.sha256
  ) {
    throw new MintedProjectCompilerError(
      "REGISTRY_DIGEST_MISMATCH",
      resolution.projectPath,
      "supported-profile registry bindings do not match authority bytes",
    );
  }

  const project = readJson<JsonObject>(resolve(resolution.projectRoot, resolution.projectPath));
  const projectViolations = validateJsonSchema(
    resolve(implRoot, "spec/minted-project/project.schema.json"),
    project,
  );
  if (projectViolations.length > 0) {
    failSchema("PROJECT_SCHEMA_INVALID", resolution.projectPath, projectViolations);
  }
  const profile = profileRegistry.profiles.find(
    (entry) =>
      entry.id === project.language.profile.id && entry.version === project.language.profile.version,
  );
  if (!profile) {
    throw new MintedProjectCompilerError(
      "PROFILE_UNSUPPORTED",
      resolution.projectPath,
      `${project.language.profile.id}@${project.language.profile.version}`,
    );
  }
  const profileDigest = sha256File(profilePath);
  if (project.language.profile.digest !== profileDigest) {
    throw new MintedProjectCompilerError(
      "PROFILE_DIGEST_MISMATCH",
      resolution.projectPath,
      "project profile digest does not match evaluated registry",
    );
  }
  if (
    project.language.registries.kinds_digest !== profileRegistry.registry_bindings.kinds.sha256 ||
    project.language.registries.relationships_digest !==
      profileRegistry.registry_bindings.relationships.sha256
  ) {
    throw new MintedProjectCompilerError(
      "REGISTRY_DIGEST_MISMATCH",
      resolution.projectPath,
      "project registry digests do not match the supported profile",
    );
  }

  for (const admitted of profile.relationships) {
    const signatures = relationships.signatures.filter(
      (entry) => entry.id === admitted.id && entry.status !== "deprecated" && entry.status !== "deferred",
    );
    if (
      !signatures.some(
        (signature) =>
          signatureTypes(signature, "source").includes(admitted.source_kind) &&
          signatureTypes(signature, "target").includes(admitted.target_kind),
      )
    ) {
      throw new MintedProjectCompilerError(
        "PROFILE_RELATIONSHIP_INVALID",
        profilePath,
        `${admitted.source_kind}-${admitted.id}->${admitted.target_kind}`,
      );
    }
  }

  const inputByPath = new Map(resolution.records.map((record) => [record.path, record]));
  const nodeById = new Map<string, { node: SourceNode; path: string }>();
  for (const featureReference of project.features as string[]) {
    const featurePath = sourcePath(resolution.projectPath, featureReference);
    const feature = readJson<JsonObject>(resolve(resolution.projectRoot, featurePath));
    const featureViolations = validateJsonSchema(
      resolve(implRoot, "spec/minted-project/feature.schema.json"),
      feature,
    );
    if (featureViolations.length > 0) {
      failSchema("FEATURE_SCHEMA_INVALID", featurePath, featureViolations);
    }
    for (const nodeReference of feature.node_sources as string[]) {
      const nodePath = sourcePath(featurePath, nodeReference);
      const node = readJson<SourceNode>(resolve(resolution.projectRoot, nodePath));
      const baseViolations = validateJsonSchema(
        resolve(implRoot, "spec/minted-project/node.schema.json"),
        node,
      );
      if (!profile.kinds.includes(node.kind)) {
        throw new MintedProjectCompilerError("KIND_UNSUPPORTED", nodePath, node.kind);
      }
      const formationPath = profile.formation_schemas[node.kind];
      const formationViolations = validateJsonSchema(resolve(domainspecRoot, formationPath), node.body);
      if (formationViolations.length > 0) {
        failSchema("FORMATION_INVALID", nodePath, formationViolations);
      }
      const nonFormationViolations = baseViolations.filter(
        (violation) => !violation.path.startsWith("$.body"),
      );
      if (nonFormationViolations.length > 0) {
        failSchema("NODE_SCHEMA_INVALID", nodePath, nonFormationViolations);
      }
      if (node.feature_id !== feature.feature_id) {
        throw new MintedProjectCompilerError(
          "NODE_FEATURE_MISMATCH",
          nodePath,
          `${node.feature_id} != ${feature.feature_id}`,
        );
      }
      if (nodeById.has(node.node_id)) {
        throw new MintedProjectCompilerError("NODE_ID_DUPLICATE", nodePath, node.node_id);
      }
      nodeById.set(node.node_id, { node, path: nodePath });
    }
  }

  const edges: MintedGraph["edges"] = [];
  const edgeIds = new Set<string>();
  for (const { node, path } of nodeById.values()) {
    for (const connection of node.connections) {
      if (edgeIds.has(connection.edge_id)) {
        throw new MintedProjectCompilerError("EDGE_ID_DUPLICATE", path, connection.edge_id);
      }
      edgeIds.add(connection.edge_id);
      const classification = classifyRelationshipType(
        connection.type,
        relationships,
        profile.relationships,
      );
      if (classification !== "active-profile") {
        throw new MintedProjectCompilerError(classification, path, connection.type);
      }
      const target = nodeById.get(connection.to);
      if (!target) {
        throw new MintedProjectCompilerError("EDGE_ENDPOINT_MISSING", path, connection.to);
      }
      if (node.feature_id !== target.node.feature_id) {
        throw new MintedProjectCompilerError(
          "CROSS_FEATURE_UNSUPPORTED",
          path,
          `${node.node_id}->${target.node.node_id}`,
        );
      }
      const admitted = profile.relationships.find((entry) => entry.id === connection.type);
      if (
        !admitted ||
        admitted.source_kind !== node.kind ||
        admitted.target_kind !== target.node.kind
      ) {
        throw new MintedProjectCompilerError(
          "EDGE_ENDPOINT_KIND_MISMATCH",
          path,
          `${node.kind}-${connection.type}->${target.node.kind}`,
        );
      }
      edges.push({
        edge_id: connection.edge_id,
        type: connection.type,
        from: node.node_id,
        to: connection.to,
      });
    }
  }

  const nodes = [...nodeById.values()]
    .map(({ node }) => ({
      node_id: node.node_id,
      feature_id: node.feature_id,
      kind: node.kind,
      intent: node.intent,
      body: node.body,
    }))
    .sort((left, right) => left.node_id.localeCompare(right.node_id));
  edges.sort((left, right) => left.edge_id.localeCompare(right.edge_id));

  const graph: MintedGraph = {
    schema_version: "minted-graph/v1",
    authority: "generated-semantic-read-model",
    project_id: project.project_id,
    language: {
      profile_digest: profileDigest,
      kinds_digest: profileRegistry.registry_bindings.kinds.sha256,
      relationships_digest: profileRegistry.registry_bindings.relationships.sha256,
    },
    source_set_digest: resolution.sourceSetDigest,
    nodes,
    edges,
  };
  const records: MintedSourceManifest["records"] = [];
  for (const { node, path } of nodeById.values()) {
    const input = inputByPath.get(path);
    if (!input) {
      throw new MintedProjectCompilerError("GENERATED_MANIFEST_INVALID", path, "missing input digest");
    }
    records.push({
      record_type: "node",
      graph_id: node.node_id,
      source_path: path,
      source_digest: input.digest,
    });
    for (const connection of node.connections) {
      records.push({
        record_type: "edge",
        graph_id: connection.edge_id,
        source_path: path,
        source_digest: input.digest,
      });
    }
  }
  records.sort((left, right) =>
    left.record_type.localeCompare(right.record_type) || left.graph_id.localeCompare(right.graph_id),
  );
  const sourceManifest: MintedSourceManifest = {
    schema_version: "minted-source-manifest/v1",
    authority: "generated-provenance-read-model",
    project_id: project.project_id,
    source_set_digest: resolution.sourceSetDigest,
    inputs: resolution.records,
    records,
  };

  const graphViolations = validateJsonSchema(
    resolve(implRoot, "spec/minted-project/graph.schema.json"),
    graph,
  );
  if (graphViolations.length > 0) {
    failSchema("GENERATED_GRAPH_INVALID", "graph.json", graphViolations);
  }
  const manifestViolations = validateJsonSchema(
    resolve(implRoot, "spec/minted-project/source-manifest.schema.json"),
    sourceManifest,
  );
  if (manifestViolations.length > 0) {
    failSchema("GENERATED_MANIFEST_INVALID", "source-manifest.json", manifestViolations);
  }

  return {
    graph,
    sourceManifest,
    graphBytes: `${JSON.stringify(graph, null, 2)}\n`,
    sourceManifestBytes: `${JSON.stringify(sourceManifest, null, 2)}\n`,
  };
}
