export class ViewAtlasProjectionError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "ViewAtlasProjectionError";
    this.code = code;
  }
}

function fail(code, message) {
  throw new ViewAtlasProjectionError(code, message);
}

function stableIds(values) {
  return [...values].sort((left, right) => left.localeCompare(right));
}

function uniqueIndex(items, idField, duplicateCode, label) {
  const index = new Map();
  for (const item of items) {
    const id = item?.[idField];
    if (typeof id !== "string" || id.length === 0) {
      fail(duplicateCode, `${label} is missing ${idField}`);
    }
    if (index.has(id)) {
      fail(duplicateCode, `duplicate ${label} id: ${id}`);
    }
    index.set(id, item);
  }
  return index;
}

export function deriveLensFlows({
  lenses,
  portals,
  canonicalRelationIds,
  expectedFlowCount = 13,
  expectedPortalCount = 109,
}) {
  if (
    !Array.isArray(lenses) ||
    !Array.isArray(portals) ||
    !Array.isArray(canonicalRelationIds)
  ) {
    fail(
      "ATLAS_FLOW_INPUT_INVALID",
      "lenses, portals, and canonical relation ids are arrays",
    );
  }

  const lensOrder = new Map();
  for (const [index, lens] of lenses.entries()) {
    const lensId = lens?.lens_id;
    if (typeof lensId !== "string" || lensId.length === 0) {
      fail("ATLAS_DUPLICATE_LENS", "lens is missing lens_id");
    }
    if (lensOrder.has(lensId)) {
      fail("ATLAS_DUPLICATE_LENS", `duplicate lens id: ${lensId}`);
    }
    lensOrder.set(lensId, index);
  }

  const flowByPair = new Map();
  const assignedRelationIds = new Set();
  const canonicalRelationIdSet = new Set();
  for (const relationId of canonicalRelationIds) {
    if (typeof relationId !== "string" || relationId.length === 0) {
      fail(
        "ATLAS_FLOW_RELATION_INVALID",
        "canonical portal relation id is invalid",
      );
    }
    if (canonicalRelationIdSet.has(relationId)) {
      fail(
        "ATLAS_FLOW_DUPLICATE_RELATION",
        `canonical portal relation id is duplicated: ${relationId}`,
      );
    }
    canonicalRelationIdSet.add(relationId);
  }
  for (const portal of portals) {
    const relationId = portal?.relation_id;
    const sourceLensId = portal?.source_lens_id;
    const targetLensId = portal?.target_lens_id;
    if (typeof relationId !== "string" || relationId.length === 0) {
      fail(
        "ATLAS_FLOW_RELATION_INVALID",
        "portal is missing relation_id",
      );
    }
    if (!canonicalRelationIdSet.has(relationId)) {
      fail(
        "ATLAS_FLOW_UNKNOWN_RELATION",
        `portal relation is not in the canonical portal set: ${relationId}`,
      );
    }
    if (!lensOrder.has(sourceLensId) || !lensOrder.has(targetLensId)) {
      fail(
        "ATLAS_FLOW_UNKNOWN_LENS",
        `${relationId} references unknown lens ${sourceLensId} -> ${targetLensId}`,
      );
    }
    if (sourceLensId === targetLensId) {
      fail(
        "ATLAS_FLOW_INTERNAL_PORTAL",
        `${relationId} incorrectly classifies same-lens endpoints as a portal`,
      );
    }
    if (assignedRelationIds.has(relationId)) {
      fail(
        "ATLAS_FLOW_DUPLICATE_RELATION",
        `portal relation is assigned more than once: ${relationId}`,
      );
    }
    assignedRelationIds.add(relationId);

    const pairKey = `${sourceLensId}\u0000${targetLensId}`;
    if (!flowByPair.has(pairKey)) {
      flowByPair.set(pairKey, {
        source_lens_id: sourceLensId,
        target_lens_id: targetLensId,
        relation_ids: [],
      });
    }
    flowByPair.get(pairKey).relation_ids.push(relationId);
  }

  const lensFlows = [...flowByPair.values()]
    .sort(
      (left, right) =>
        lensOrder.get(left.source_lens_id) -
          lensOrder.get(right.source_lens_id) ||
        lensOrder.get(left.target_lens_id) -
          lensOrder.get(right.target_lens_id),
    )
    .map((flow) => {
      const relationIds = stableIds(flow.relation_ids);
      return Object.freeze({
        source_lens_id: flow.source_lens_id,
        target_lens_id: flow.target_lens_id,
        relation_ids: Object.freeze(relationIds),
        relation_count: relationIds.length,
      });
    });

  if (lensFlows.length !== expectedFlowCount) {
    fail(
      "ATLAS_FLOW_GROUP_COUNT_MISMATCH",
      `lens flow count expected ${expectedFlowCount}, received ${lensFlows.length}`,
    );
  }
  const relationCount = lensFlows.reduce(
    (total, flow) => total + flow.relation_count,
    0,
  );
  if (relationCount !== expectedPortalCount) {
    fail(
      "ATLAS_FLOW_RELATION_COUNT_MISMATCH",
      `lens flow relation count expected ${expectedPortalCount}, received ${relationCount}`,
    );
  }

  const projectedRelationIds = stableIds(
    lensFlows.flatMap((flow) => flow.relation_ids),
  );
  const portalRelationIds = stableIds(
    portals.map((portal) => portal.relation_id),
  );
  const canonicalIds = stableIds(canonicalRelationIdSet);
  if (
    projectedRelationIds.length !== portalRelationIds.length ||
    projectedRelationIds.length !== canonicalIds.length ||
    projectedRelationIds.some(
      (relationId, index) => relationId !== portalRelationIds[index],
    ) ||
    projectedRelationIds.some(
      (relationId, index) => relationId !== canonicalIds[index],
    )
  ) {
    fail(
      "ATLAS_FLOW_PARTITION_MISMATCH",
      "lens flows do not exactly partition portal relation ids",
    );
  }

  return Object.freeze(lensFlows);
}

export function projectViewAtlas({
  nodes,
  relations,
  lenses,
  isolateDispositions,
}) {
  if (
    !Array.isArray(nodes) ||
    !Array.isArray(relations) ||
    !Array.isArray(lenses) ||
    !Array.isArray(isolateDispositions)
  ) {
    fail("ATLAS_INPUT_INVALID", "nodes, relations, lenses, and dispositions are arrays");
  }

  const nodeById = uniqueIndex(
    nodes,
    "concept_id",
    "ATLAS_DUPLICATE_NODE",
    "node",
  );
  const relationById = uniqueIndex(
    relations,
    "relation_id",
    "ATLAS_DUPLICATE_RELATION",
    "relation",
  );
  const lensById = uniqueIndex(
    lenses,
    "lens_id",
    "ATLAS_DUPLICATE_LENS",
    "lens",
  );
  const observedKinds = new Set(nodes.map((node) => node.business_kind));
  const kindToLens = new Map();

  for (const lens of lenses) {
    if (
      !Array.isArray(lens.business_kinds) ||
      lens.business_kinds.length === 0
    ) {
      fail("ATLAS_KIND_MAP_INVALID", `${lens.lens_id} has no kinds`);
    }
    for (const kind of lens.business_kinds) {
      if (kindToLens.has(kind)) {
        fail(
          "ATLAS_KIND_MULTIPLY_MAPPED",
          `${kind} maps to ${kindToLens.get(kind)} and ${lens.lens_id}`,
        );
      }
      kindToLens.set(kind, lens.lens_id);
    }
  }

  for (const kind of observedKinds) {
    if (!kindToLens.has(kind)) {
      fail("ATLAS_KIND_UNMAPPED", `observed kind is unmapped: ${kind}`);
    }
  }
  for (const kind of kindToLens.keys()) {
    if (!observedKinds.has(kind)) {
      fail("ATLAS_KIND_ABSENT", `catalog kind is absent from source: ${kind}`);
    }
  }

  const projectedLenses = new Map(
    lenses.map((lens) => [
      lens.lens_id,
      {
        lens_id: lens.lens_id,
        title: lens.title,
        question: lens.question,
        description: lens.description,
        business_kinds: [...lens.business_kinds],
        core_node_ids: [],
        internal_relation_ids: [],
        outbound_portal_ids: [],
        inbound_portal_ids: [],
        zero_degree_node_ids: [],
      },
    ]),
  );
  const nodeLensById = new Map();
  for (const node of nodes) {
    const lensId = kindToLens.get(node.business_kind);
    projectedLenses.get(lensId).core_node_ids.push(node.concept_id);
    nodeLensById.set(node.concept_id, lensId);
  }

  const degree = new Map(nodes.map((node) => [node.concept_id, 0]));
  const portals = [];
  for (const relation of relations) {
    if (!nodeById.has(relation.source_concept)) {
      fail(
        "ATLAS_UNKNOWN_ENDPOINT",
        `${relation.relation_id} has unknown source ${relation.source_concept}`,
      );
    }
    if (!nodeById.has(relation.target_concept)) {
      fail(
        "ATLAS_UNKNOWN_ENDPOINT",
        `${relation.relation_id} has unknown target ${relation.target_concept}`,
      );
    }
    degree.set(
      relation.source_concept,
      degree.get(relation.source_concept) + 1,
    );
    degree.set(
      relation.target_concept,
      degree.get(relation.target_concept) + 1,
    );
    const sourceLensId = nodeLensById.get(relation.source_concept);
    const targetLensId = nodeLensById.get(relation.target_concept);
    if (sourceLensId === targetLensId) {
      projectedLenses
        .get(sourceLensId)
        .internal_relation_ids.push(relation.relation_id);
    } else {
      portals.push({
        relation_id: relation.relation_id,
        source_lens_id: sourceLensId,
        target_lens_id: targetLensId,
      });
      projectedLenses
        .get(sourceLensId)
        .outbound_portal_ids.push(relation.relation_id);
      projectedLenses
        .get(targetLensId)
        .inbound_portal_ids.push(relation.relation_id);
    }
  }

  const dispositionById = uniqueIndex(
    isolateDispositions,
    "concept_id",
    "ATLAS_DUPLICATE_DISPOSITION",
    "isolate disposition",
  );
  const zeroDegreeNodeIds = stableIds(
    [...degree.entries()]
      .filter(([, count]) => count === 0)
      .map(([conceptId]) => conceptId),
  );
  for (const conceptId of zeroDegreeNodeIds) {
    if (!dispositionById.has(conceptId)) {
      fail(
        "ATLAS_DISPOSITION_MISSING",
        `zero-degree node has no disposition: ${conceptId}`,
      );
    }
  }
  for (const conceptId of dispositionById.keys()) {
    if (!nodeById.has(conceptId)) {
      fail(
        "ATLAS_DISPOSITION_UNKNOWN_NODE",
        `disposition references unknown node: ${conceptId}`,
      );
    }
    if (degree.get(conceptId) !== 0) {
      fail(
        "ATLAS_DISPOSITION_NON_ISOLATE",
        `disposition references incident node: ${conceptId}`,
      );
    }
  }
  if (dispositionById.size !== zeroDegreeNodeIds.length) {
    fail(
      "ATLAS_DISPOSITION_SET_MISMATCH",
      "disposition set does not equal zero-degree set",
    );
  }

  for (const conceptId of zeroDegreeNodeIds) {
    projectedLenses
      .get(nodeLensById.get(conceptId))
      .zero_degree_node_ids.push(conceptId);
  }

  const orderedLenses = lenses.map((lens) => {
    const projected = projectedLenses.get(lens.lens_id);
    for (const field of [
      "core_node_ids",
      "internal_relation_ids",
      "outbound_portal_ids",
      "inbound_portal_ids",
      "zero_degree_node_ids",
    ]) {
      projected[field] = stableIds(projected[field]);
    }
    return projected;
  });
  portals.sort((left, right) =>
    left.relation_id.localeCompare(right.relation_id),
  );
  const lensFlows = deriveLensFlows({
    lenses,
    portals,
    canonicalRelationIds: portals.map((portal) => portal.relation_id),
  });

  const internalRelationIds = stableIds(
    orderedLenses.flatMap((lens) => lens.internal_relation_ids),
  );
  const portalRelationIds = portals.map((portal) => portal.relation_id);
  const coveredRelationIds = stableIds([
    ...internalRelationIds,
    ...portalRelationIds,
  ]);
  if (
    coveredRelationIds.length !== relationById.size ||
    new Set(coveredRelationIds).size !== relationById.size
  ) {
    fail(
      "ATLAS_RELATION_PARTITION_MISMATCH",
      "relations are missing from or duplicated across the partition",
    );
  }

  return {
    schema_version: "body-war-view-atlas-projection/v1",
    authority_effect: "none",
    lenses: orderedLenses,
    portals,
    lens_flows: lensFlows,
    zero_degree_node_ids: zeroDegreeNodeIds,
    isolate_dispositions: zeroDegreeNodeIds.map((conceptId) => ({
      concept_id: conceptId,
      disposition: dispositionById.get(conceptId).disposition,
    })),
    coverage: {
      lens_count: lensById.size,
      business_kind_count: observedKinds.size,
      node_count: nodeById.size,
      relation_count: relationById.size,
      internal_relation_count: internalRelationIds.length,
      portal_relation_count: portalRelationIds.length,
      lens_flow_count: lensFlows.length,
      lens_flow_relation_count: lensFlows.reduce(
        (total, flow) => total + flow.relation_count,
        0,
      ),
      zero_degree_node_count: zeroDegreeNodeIds.length,
    },
  };
}
