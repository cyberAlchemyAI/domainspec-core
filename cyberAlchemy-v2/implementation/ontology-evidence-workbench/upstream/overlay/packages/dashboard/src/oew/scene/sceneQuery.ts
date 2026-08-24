import {
  finalizeKnowledgeScene,
  OEW_KNOWLEDGE_SCENE_V12,
} from "./relationReference.ts";

export const OEW_KNOWLEDGE_SCENE_SCHEMA = OEW_KNOWLEDGE_SCENE_V12;

const SOURCE_GRAPH_SCHEMA = "oew.compiled-source-graph.v1";
const VIEW_PACK_SCHEMA = "oew.compiled-view-pack.v1";
const SCOPE_CAPS = {
  home: { nodes: 24, internal_relations: 48, portals: 12 },
  focus: { nodes: 32, internal_relations: 64, portals: 16 },
};

/** @typedef {Record<string, unknown>} JsonRecord */

export class SceneQueryError extends Error {
  /** @type {string} */
  code;
  /** @type {string[]} */
  issues;

  /** @param {string[]} issues */
  constructor(issues = []) {
    const stableIssues = [...new Set(issues)].sort();
    super(`OEW scene query rejected: ${stableIssues.join(", ")}`);
    this.name = "SceneQueryError";
    this.code = "OEW_SCENE_QUERY_REJECTED";
    this.issues = stableIssues;
  }
}

/** @param {unknown} value @returns {value is JsonRecord} */
const isRecord = (value) =>
  value !== null && typeof value === "object" && !Array.isArray(value);

/** @param {unknown} value */
const isNonemptyString = (value) =>
  typeof value === "string" && value.trim().length > 0;

/** @param {JsonRecord} node */
const sceneNode = (node) => {
  const result = {
    source_node_id: node.source_node_id,
    label: node.label,
    node_kind: node.node_kind,
    role: node.role,
    icon_token: node.icon_token,
    evidence_refs: [...node.evidence_refs],
    authority_effect: node.authority_effect,
  };
  if (Object.hasOwn(node, "summary")) result.summary = node.summary;
  return result;
};

/** @param {JsonRecord} relation */
const sceneRelation = (relation) => ({
  source_relation_id: relation.source_relation_id,
  source_node_id: relation.source_node_id,
  target_node_id: relation.target_node_id,
  exact_predicate: relation.exact_predicate,
  source_direction: relation.source_direction,
  presentation_family: relation.presentation_family,
  color_token: relation.color_token,
  pattern_token: relation.pattern_token,
  visible_label: relation.visible_label,
  direction_label: relation.direction_label,
  evidence_refs: [...relation.evidence_refs],
  source_refs: [...relation.source_refs],
  mapping_loss: relation.mapping_loss,
  authority_effect: relation.authority_effect,
  source_digest: relation.source_digest,
});

/** @param {JsonRecord} sourceGraph @param {JsonRecord} viewPack */
const validateCompiledInputs = (sourceGraph, viewPack) => {
  const issues = [];
  if (
    sourceGraph.schema_version !== SOURCE_GRAPH_SCHEMA ||
    !isNonemptyString(sourceGraph.graph_digest) ||
    !Array.isArray(sourceGraph.nodes) ||
    !Array.isArray(sourceGraph.relations) ||
    !isRecord(sourceGraph.node_by_id)
  ) {
    issues.push("SCENE_SOURCE_GRAPH_INVALID");
  }
  if (
    viewPack.schema_version !== VIEW_PACK_SCHEMA ||
    !isNonemptyString(viewPack.view_pack_id) ||
    !isNonemptyString(viewPack.view_pack_digest) ||
    !Array.isArray(viewPack.clusters) ||
    !isRecord(viewPack.cluster_by_id) ||
    !isRecord(viewPack.cluster_id_by_node_id) ||
    !isNonemptyString(viewPack.default_cluster_id)
  ) {
    issues.push("SCENE_VIEW_PACK_INVALID");
  }
  if (sourceGraph.graph_digest !== viewPack.graph_digest) {
    issues.push("SCENE_REVISION_MISMATCH");
  }
  return issues;
};

/** @param {JsonRecord} viewPack @param {JsonRecord} query @param {string[]} issues */
const resolveCluster = (viewPack, query, issues) => {
  if (!Object.hasOwn(SCOPE_CAPS, query.scope)) {
    issues.push("SCENE_SCOPE_UNSUPPORTED");
    return null;
  }
  if (query.scope === "home") {
    const clusterId = query.cluster_id ?? viewPack.default_cluster_id;
    if (!isNonemptyString(clusterId) || !viewPack.cluster_by_id[clusterId]) {
      issues.push(`SCENE_CLUSTER_UNKNOWN:${String(clusterId)}`);
      return null;
    }
    return clusterId;
  }
  if (!isNonemptyString(query.focus_node_id)) {
    issues.push("SCENE_FOCUS_REQUIRED");
    return null;
  }
  const clusterId = viewPack.cluster_id_by_node_id[query.focus_node_id];
  if (!clusterId) {
    issues.push(`SCENE_FOCUS_UNKNOWN:${query.focus_node_id}`);
    return null;
  }
  if (query.cluster_id !== undefined && query.cluster_id !== clusterId) {
    issues.push(`SCENE_FOCUS_CLUSTER_MISMATCH:${query.focus_node_id}:${query.cluster_id}`);
    return null;
  }
  return clusterId;
};

/**
 * Derive a bounded semantic scene. The relevant relation denominator is every
 * exact source relation with at least one endpoint in the visible node set.
 *
 * @param {unknown} sourceGraphInput
 * @param {unknown} viewPackInput
 * @param {unknown} queryInput
 */
export async function deriveScene(sourceGraphInput, viewPackInput, queryInput) {
  if (!isRecord(sourceGraphInput)) {
    throw new SceneQueryError(["SCENE_SOURCE_GRAPH_INVALID"]);
  }
  if (!isRecord(viewPackInput)) {
    throw new SceneQueryError(["SCENE_VIEW_PACK_INVALID"]);
  }
  if (!isRecord(queryInput)) throw new SceneQueryError(["SCENE_QUERY_INVALID"]);

  const sourceGraph = sourceGraphInput;
  const viewPack = viewPackInput;
  const query = queryInput;
  const issues = validateCompiledInputs(sourceGraph, viewPack);
  const clusterId = resolveCluster(viewPack, query, issues);
  if (issues.length) throw new SceneQueryError(issues);

  const cluster = viewPack.cluster_by_id[clusterId];
  if (!isRecord(cluster) || !Array.isArray(cluster.member_node_ids)) {
    throw new SceneQueryError([`SCENE_CLUSTER_INVALID:${clusterId}`]);
  }
  const visibleNodeIds = [...cluster.member_node_ids].sort((left, right) =>
    left.localeCompare(right),
  );
  if (visibleNodeIds.length === 0) {
    throw new SceneQueryError([`SCENE_EMPTY:${clusterId}`]);
  }
  const caps = SCOPE_CAPS[query.scope];
  if (visibleNodeIds.length > caps.nodes) {
    issues.push(`SCENE_NODE_CAP_EXCEEDED:${visibleNodeIds.length}:${caps.nodes}`);
  }

  const visible = new Set(visibleNodeIds);
  const nodes = [];
  for (const nodeId of visibleNodeIds) {
    const node = sourceGraph.node_by_id[nodeId];
    if (!isRecord(node)) {
      issues.push(`SCENE_NODE_UNRESOLVED:${nodeId}`);
    } else {
      nodes.push(sceneNode(node));
    }
  }

  const internalRelations = [];
  const cutRelations = [];
  const relevantRelationIds = [];
  const destinationClusterIds = new Set();
  for (const relation of sourceGraph.relations) {
    if (!isRecord(relation) || !isNonemptyString(relation.source_relation_id)) {
      issues.push("SCENE_RELATION_INVALID");
      continue;
    }
    const sourceVisible = visible.has(relation.source_node_id);
    const targetVisible = visible.has(relation.target_node_id);
    if (!sourceVisible && !targetVisible) continue;
    relevantRelationIds.push(relation.source_relation_id);
    if (sourceVisible && targetVisible) {
      internalRelations.push(sceneRelation(relation));
      continue;
    }
    cutRelations.push(sceneRelation(relation));
    const outsideNodeId = sourceVisible
      ? relation.target_node_id
      : relation.source_node_id;
    const destinationClusterId = viewPack.cluster_id_by_node_id[outsideNodeId];
    if (!destinationClusterId) {
      issues.push(`SCENE_BOUNDARY_CLUSTER_UNRESOLVED:${outsideNodeId}`);
    } else {
      destinationClusterIds.add(destinationClusterId);
    }
  }

  internalRelations.sort((left, right) =>
    left.source_relation_id.localeCompare(right.source_relation_id),
  );
  cutRelations.sort((left, right) =>
    left.source_relation_id.localeCompare(right.source_relation_id),
  );
  relevantRelationIds.sort((left, right) => left.localeCompare(right));
  if (internalRelations.length > caps.internal_relations) {
    issues.push(
      `SCENE_INTERNAL_RELATION_CAP_EXCEEDED:${internalRelations.length}:${caps.internal_relations}`,
    );
  }
  if (destinationClusterIds.size > caps.portals) {
    issues.push(`SCENE_PORTAL_CAP_EXCEEDED:${destinationClusterIds.size}:${caps.portals}`);
  }

  const internalIds = new Set(
    internalRelations.map((relation) => relation.source_relation_id),
  );
  const cutIds = new Set(cutRelations.map((relation) => relation.source_relation_id));
  const partitionIds = [...internalIds, ...cutIds].sort((left, right) =>
    left.localeCompare(right),
  );
  if ([...internalIds].some((relationId) => cutIds.has(relationId))) {
    issues.push("SCENE_PARTITION_OVERLAP");
  }
  if (JSON.stringify(partitionIds) !== JSON.stringify(relevantRelationIds)) {
    issues.push("SCENE_PARTITION_NOT_TOTAL");
  }
  if (issues.length) throw new SceneQueryError(issues);

  const scopeToken =
    query.scope === "focus" ? `${clusterId}:${query.focus_node_id}` : clusterId;
  const frameId = `frame:${viewPack.view_pack_id}:${query.scope}:${scopeToken}`;
  const sceneId = `scene:${viewPack.view_pack_id}:${query.scope}:${scopeToken}`;
  const navigationFrame = {
    frame_id: frameId,
    graph_digest: sourceGraph.graph_digest,
    view_pack_id: viewPack.view_pack_id,
    view_pack_digest: viewPack.view_pack_digest,
    scope: query.scope,
    selected: { kind: "none" },
    filters: {},
    index_state: {
      query: "",
      sort_key: "source-id",
      sort_direction: "ascending",
    },
    viewport: { x: 0, y: 0, zoom: 1 },
    panel: { id: "none", modal: false },
    expanded_portal_ids: [],
    focus_fallback_order: [
      "initiating-control",
      "selected-entity",
      "scene-heading",
      "workbench-heading",
    ],
  };
  if (query.scope === "focus") {
    navigationFrame.focus_node_id = query.focus_node_id;
  }

  const completeIndexRows = sourceGraph.nodes.length + sourceGraph.relations.length;
  return finalizeKnowledgeScene({
    schema_version: OEW_KNOWLEDGE_SCENE_SCHEMA,
    scene_id: sceneId,
    graph_digest: sourceGraph.graph_digest,
    view_pack_id: viewPack.view_pack_id,
    view_pack_digest: viewPack.view_pack_digest,
    scope: query.scope,
    nodes,
    internal_relations: internalRelations,
    cut_relations: cutRelations,
    clusters: [
      { cluster_id: clusterId, visible_member_node_ids: visibleNodeIds },
    ],
    portals: [],
    legend: [],
    navigation_frame: navigationFrame,
    denominators: {
      source_nodes: sourceGraph.nodes.length,
      source_relations: sourceGraph.relations.length,
      scene_nodes: nodes.length,
      internal_relations: internalRelations.length,
      cut_relations: cutRelations.length,
      complete_index_rows: completeIndexRows,
      filtered_index_rows: completeIndexRows,
    },
  });
}
