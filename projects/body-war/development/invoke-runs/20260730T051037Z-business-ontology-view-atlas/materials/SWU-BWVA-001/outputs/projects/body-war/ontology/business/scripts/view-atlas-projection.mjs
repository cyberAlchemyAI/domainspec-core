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
      zero_degree_node_count: zeroDegreeNodeIds.length,
    },
  };
}

