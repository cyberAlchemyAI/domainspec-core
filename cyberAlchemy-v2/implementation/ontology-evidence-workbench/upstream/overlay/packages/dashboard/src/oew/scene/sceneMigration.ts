import {
  computeSourceGraphDigest,
  OEW_COMPILED_SOURCE_GRAPH_SCHEMA,
  OEW_SOURCE_GRAPH_RECEIPT_SCHEMA,
} from "./sourceGraph.ts";
import {
  OEW_COMPILED_VIEW_PACK_SCHEMA,
  OEW_VIEW_PACK_RECEIPT_SCHEMA,
} from "./viewPack.ts";
import {
  finalizeKnowledgeScene,
  OEW_KNOWLEDGE_SCENE_V12,
} from "./relationReference.ts";

export const OEW_SCENE_MIGRATION_RECEIPT_SCHEMA =
  "oew.scene-migration-receipt.v1";

const LEGACY_SCENE_SCHEMAS = new Set([
  "oew.knowledge-scene.v1",
  "oew.knowledge-scene.v1.1",
]);
const DIGEST = /^[a-f0-9]{64}$/;
const LEGACY_SCENE_KEYS = [
  "clusters",
  "cut_relations",
  "denominators",
  "graph_digest",
  "internal_relations",
  "legend",
  "navigation_frame",
  "nodes",
  "path_result",
  "portals",
  "scene_id",
  "schema_version",
  "scope",
  "view_pack_digest",
  "view_pack_id",
];
const REQUIRED_LEGACY_SCENE_KEYS = LEGACY_SCENE_KEYS.filter(
  (key) => key !== "path_result",
);
export const OEW_LEGACY_RELATION_FIELDS = Object.freeze([
  "source_relation_id",
  "source_node_id",
  "target_node_id",
  "exact_predicate",
  "source_direction",
  "presentation_family",
  "color_token",
  "pattern_token",
  "visible_label",
  "direction_label",
  "evidence_refs",
  "mapping_loss",
  "authority_effect",
]);

/** @typedef {Record<string, unknown>} JsonRecord */

export class SceneMigrationError extends Error {
  /** @type {string} */
  code;
  /** @type {readonly string[]} */
  issues;

  /** @param {readonly string[]} issues */
  constructor(issues) {
    const stableIssues = [...new Set(issues)].sort();
    super(`OEW scene migration rejected: ${stableIssues.join(", ")}`);
    this.name = "SceneMigrationError";
    this.code = "OEW_SCENE_MIGRATION_REJECTED";
    this.issues = Object.freeze(stableIssues);
  }
}

/** @param {unknown} value @returns {value is JsonRecord} */
const isRecord = (value) =>
  value !== null && typeof value === "object" && !Array.isArray(value);

/** @param {unknown} value */
const isNonemptyString = (value) =>
  typeof value === "string" && value.trim().length > 0;

/** @param {JsonRecord} value @param {readonly string[]} required @param {readonly string[]} allowed */
const hasDeclaredShape = (value, required, allowed) => {
  const keys = Object.keys(value);
  return (
    required.every((key) => Object.hasOwn(value, key)) &&
    keys.every((key) => allowed.includes(key))
  );
};

/** @param {unknown} value */
const cloneJson = (value) => {
  if (Array.isArray(value)) return value.map(cloneJson);
  if (isRecord(value)) {
    return Object.fromEntries(
      Object.entries(value).map(([key, child]) => [key, cloneJson(child)]),
    );
  }
  return value;
};

/** @param {unknown} value */
const deepFreeze = (value) => {
  if (value !== null && typeof value === "object" && !Object.isFrozen(value)) {
    for (const child of Object.values(value)) deepFreeze(child);
    Object.freeze(value);
  }
  return value;
};

/** @param {unknown} left @param {unknown} right */
const exactValue = (left, right) => JSON.stringify(left) === JSON.stringify(right);

/** @param {string} left @param {string} right */
const compareCodePoints = (left, right) => {
  const leftPoints = Array.from(left, (value) => value.codePointAt(0) ?? 0);
  const rightPoints = Array.from(right, (value) => value.codePointAt(0) ?? 0);
  const length = Math.min(leftPoints.length, rightPoints.length);
  for (let index = 0; index < length; index += 1) {
    if (leftPoints[index] !== rightPoints[index]) {
      return leftPoints[index] - rightPoints[index];
    }
  }
  return leftPoints.length - rightPoints.length;
};

/** @param {JsonRecord} sourceGraph */
const validateSourceGraph = async (sourceGraph) => {
  const issues = [];
  if (
    sourceGraph.schema_version !== OEW_COMPILED_SOURCE_GRAPH_SCHEMA ||
    !DIGEST.test(String(sourceGraph.graph_digest)) ||
    !isRecord(sourceGraph.source_digests) ||
    !Array.isArray(sourceGraph.nodes) ||
    !Array.isArray(sourceGraph.relations) ||
    !isRecord(sourceGraph.node_by_id) ||
    !isRecord(sourceGraph.relation_by_id) ||
    !isRecord(sourceGraph.receipt)
  ) {
    throw new SceneMigrationError(["MIGRATION_SOURCE_GRAPH_INVALID"]);
  }
  const sourceSchema = sourceGraph.receipt.source_schema_version;
  const actualDigest = await computeSourceGraphDigest({
    schema_version: sourceSchema,
    source_digests: sourceGraph.source_digests,
    nodes: sourceGraph.nodes,
    relations: sourceGraph.relations,
  });
  if (actualDigest !== sourceGraph.graph_digest) {
    issues.push("MIGRATION_SOURCE_GRAPH_DIGEST_MISMATCH");
  }
  if (
    sourceGraph.receipt.schema_version !== OEW_SOURCE_GRAPH_RECEIPT_SCHEMA ||
    sourceGraph.receipt.result !== "pass" ||
    sourceGraph.receipt.graph_digest !== sourceGraph.graph_digest ||
    sourceGraph.receipt.relation_count !== sourceGraph.relations.length
  ) {
    issues.push("MIGRATION_SOURCE_GRAPH_RECEIPT_INVALID");
  }
  const relationIds = [];
  for (const [index, relation] of sourceGraph.relations.entries()) {
    if (!isRecord(relation) || !isNonemptyString(relation.source_relation_id)) {
      issues.push(`MIGRATION_SOURCE_RELATION_INVALID:${index}`);
      continue;
    }
    const relationId = relation.source_relation_id;
    relationIds.push(relationId);
    if (sourceGraph.relation_by_id[relationId] !== relation) {
      issues.push(`MIGRATION_SOURCE_RELATION_INDEX_MISMATCH:${relationId}`);
    }
  }
  if (new Set(relationIds).size !== relationIds.length) {
    issues.push("MIGRATION_SOURCE_RELATION_IDS_DUPLICATE");
  }
  if (!exactValue(sourceGraph.receipt.relation_ids, relationIds)) {
    issues.push("MIGRATION_SOURCE_GRAPH_RECEIPT_INVALID");
  }
  if (issues.length > 0) throw new SceneMigrationError(issues);
};

/** @param {JsonRecord} viewPack @param {JsonRecord} sourceGraph */
const validateViewPack = async (viewPack, sourceGraph) => {
  const issues = [];
  if (
    viewPack.schema_version !== OEW_COMPILED_VIEW_PACK_SCHEMA ||
    !isNonemptyString(viewPack.source_schema_version) ||
    !DIGEST.test(String(viewPack.view_pack_digest)) ||
    !Array.isArray(viewPack.clusters) ||
    !Array.isArray(viewPack.sequences) ||
    !isRecord(viewPack.receipt)
  ) {
    throw new SceneMigrationError(["MIGRATION_VIEW_PACK_INVALID"]);
  }
  if (viewPack.graph_digest !== sourceGraph.graph_digest) {
    issues.push("MIGRATION_VIEW_PACK_GRAPH_MISMATCH");
  }
  if (!Object.isFrozen(viewPack) || !Object.isFrozen(viewPack.receipt)) {
    issues.push("MIGRATION_VIEW_PACK_NOT_ADMITTED");
  }
  if (
    viewPack.receipt.schema_version !== OEW_VIEW_PACK_RECEIPT_SCHEMA ||
    viewPack.receipt.result !== "pass" ||
    viewPack.receipt.graph_digest !== viewPack.graph_digest ||
    viewPack.receipt.view_pack_id !== viewPack.view_pack_id ||
    viewPack.receipt.view_pack_digest !== viewPack.view_pack_digest
  ) {
    issues.push("MIGRATION_VIEW_PACK_RECEIPT_INVALID");
  }
  if (issues.length > 0) throw new SceneMigrationError(issues);
};

/** @param {JsonRecord} legacyScene @param {JsonRecord} sourceGraph */
const validateLegacyRelations = (legacyScene, sourceGraph) => {
  const issues = [];
  const visibleNodeIds = new Set();
  if (!Array.isArray(legacyScene.nodes)) {
    throw new SceneMigrationError(["MIGRATION_LEGACY_NODES_INVALID"]);
  }
  for (const [index, node] of legacyScene.nodes.entries()) {
    if (!isRecord(node) || !isNonemptyString(node.source_node_id)) {
      issues.push(`MIGRATION_LEGACY_NODE_INVALID:${index}`);
      continue;
    }
    if (visibleNodeIds.has(node.source_node_id)) {
      issues.push(`MIGRATION_LEGACY_NODE_DUPLICATE:${node.source_node_id}`);
    }
    visibleNodeIds.add(node.source_node_id);
    if (!Object.hasOwn(sourceGraph.node_by_id, node.source_node_id)) {
      issues.push(`MIGRATION_LEGACY_NODE_MISSING:${node.source_node_id}`);
    }
  }

  if (
    !Array.isArray(legacyScene.internal_relations) ||
    !Array.isArray(legacyScene.cut_relations)
  ) {
    throw new SceneMigrationError(["MIGRATION_RELATION_PARTITIONS_INVALID"]);
  }
  const internalIds = new Set();
  const cutIds = new Set();
  const legacyById = new Map();
  const partitions = [
    ["internal", legacyScene.internal_relations],
    ["cut", legacyScene.cut_relations],
  ];
  for (const [partition, relations] of partitions) {
    for (const [index, legacyRelation] of relations.entries()) {
      if (!isRecord(legacyRelation) || !isNonemptyString(legacyRelation.source_relation_id)) {
        issues.push(`MIGRATION_RELATION_INVALID:${partition}:${index}`);
        continue;
      }
      const relationId = legacyRelation.source_relation_id;
      if (legacyById.has(relationId)) {
        issues.push(`MIGRATION_RELATION_DUPLICATE:${relationId}`);
        continue;
      }
      legacyById.set(relationId, legacyRelation);
      (partition === "internal" ? internalIds : cutIds).add(relationId);
      const sourceRelation = sourceGraph.relation_by_id[relationId];
      if (!isRecord(sourceRelation)) {
        issues.push(`MIGRATION_RELATION_MISSING:${relationId}`);
        continue;
      }
      for (const field of OEW_LEGACY_RELATION_FIELDS) {
        if (!Object.hasOwn(legacyRelation, field)) {
          issues.push(`MIGRATION_BINDING_FIELD_MISSING:${relationId}:${field}`);
        } else if (!exactValue(legacyRelation[field], sourceRelation[field])) {
          issues.push(`MIGRATION_BINDING_DRIFT:${relationId}:${field}`);
        }
      }
    }
  }

  const expectedIds = new Set();
  for (const relation of sourceGraph.relations) {
    const sourceVisible = visibleNodeIds.has(relation.source_node_id);
    const targetVisible = visibleNodeIds.has(relation.target_node_id);
    if (!sourceVisible && !targetVisible) continue;
    const relationId = relation.source_relation_id;
    expectedIds.add(relationId);
    const expectedPartition = sourceVisible && targetVisible ? internalIds : cutIds;
    const oppositePartition = sourceVisible && targetVisible ? cutIds : internalIds;
    if (!expectedPartition.has(relationId)) {
      issues.push(`MIGRATION_RELATION_PARTITION_MISSING:${relationId}`);
    }
    if (oppositePartition.has(relationId)) {
      issues.push(`MIGRATION_RELATION_PARTITION_MISMATCH:${relationId}`);
    }
  }
  for (const relationId of legacyById.keys()) {
    if (!expectedIds.has(relationId)) {
      issues.push(`MIGRATION_RELATION_EXTRA:${relationId}`);
    }
  }
  if (issues.length > 0) throw new SceneMigrationError(issues);
  return {
    internalIds: [...internalIds],
    cutIds: [...cutIds],
  };
};

/**
 * Admit a legacy scene only by comparison with its exact SourceGraph and
 * ViewPack, then compile a separate v1.2 scene. The legacy object is never
 * frozen, edited, or relabeled.
 *
 * @param {unknown} legacySceneInput
 * @param {unknown} sourceGraphInput
 * @param {unknown} viewPackInput
 */
export async function migrateKnowledgeScene(
  legacySceneInput,
  sourceGraphInput,
  viewPackInput,
) {
  if (!isRecord(legacySceneInput)) {
    throw new SceneMigrationError(["MIGRATION_LEGACY_SCENE_INVALID"]);
  }
  if (!isRecord(sourceGraphInput)) {
    throw new SceneMigrationError(["MIGRATION_SOURCE_GRAPH_INVALID"]);
  }
  if (!isRecord(viewPackInput)) {
    throw new SceneMigrationError(["MIGRATION_VIEW_PACK_INVALID"]);
  }
  if (!LEGACY_SCENE_SCHEMAS.has(String(legacySceneInput.schema_version))) {
    throw new SceneMigrationError(["MIGRATION_LEGACY_SCHEMA_UNSUPPORTED"]);
  }
  if (
    !hasDeclaredShape(
      legacySceneInput,
      REQUIRED_LEGACY_SCENE_KEYS,
      LEGACY_SCENE_KEYS,
    )
  ) {
    throw new SceneMigrationError(["MIGRATION_LEGACY_SCENE_SHAPE_INVALID"]);
  }

  await validateSourceGraph(sourceGraphInput);
  await validateViewPack(viewPackInput, sourceGraphInput);

  const identityIssues = [];
  if (legacySceneInput.graph_digest !== sourceGraphInput.graph_digest) {
    identityIssues.push("MIGRATION_SOURCE_MISMATCH");
  }
  if (legacySceneInput.view_pack_id !== viewPackInput.view_pack_id) {
    identityIssues.push("MIGRATION_VIEW_PACK_ID_MISMATCH");
  }
  if (legacySceneInput.view_pack_digest !== viewPackInput.view_pack_digest) {
    identityIssues.push("MIGRATION_VIEW_PACK_MISMATCH");
  }
  if (identityIssues.length > 0) throw new SceneMigrationError(identityIssues);

  const { internalIds, cutIds } = validateLegacyRelations(
    legacySceneInput,
    sourceGraphInput,
  );
  const legacyScene = cloneJson(legacySceneInput);
  const migratedSceneId = `${legacySceneInput.scene_id}:migration:${legacySceneInput.schema_version}:to-v1.2`;
  const migratedScene = await finalizeKnowledgeScene({
    ...legacyScene,
    schema_version: OEW_KNOWLEDGE_SCENE_V12,
    scene_id: migratedSceneId,
    internal_relations: internalIds.map(
      (relationId) => sourceGraphInput.relation_by_id[relationId],
    ),
    cut_relations: cutIds.map(
      (relationId) => sourceGraphInput.relation_by_id[relationId],
    ),
  });
  const relationIds = [...internalIds, ...cutIds].sort(compareCodePoints);
  const receipt = deepFreeze({
    schema_version: OEW_SCENE_MIGRATION_RECEIPT_SCHEMA,
    result: "pass",
    legacy_schema_version: legacySceneInput.schema_version,
    legacy_scene_id: legacySceneInput.scene_id,
    legacy_graph_digest: legacySceneInput.graph_digest,
    legacy_view_pack_id: legacySceneInput.view_pack_id,
    legacy_view_pack_digest: legacySceneInput.view_pack_digest,
    source_graph_digest: sourceGraphInput.graph_digest,
    view_pack_digest: viewPackInput.view_pack_digest,
    migrated_schema_version: OEW_KNOWLEDGE_SCENE_V12,
    migrated_scene_id: migratedScene.scene_id,
    migrated_scene_digest: migratedScene.scene_digest,
    relation_ids: relationIds,
    relation_count: relationIds.length,
    compared_relation_fields: [...OEW_LEGACY_RELATION_FIELDS],
    legacy_artifact_mutated: false,
    authority_effect: "none",
  });
  return Object.freeze({ scene: migratedScene, receipt });
}
