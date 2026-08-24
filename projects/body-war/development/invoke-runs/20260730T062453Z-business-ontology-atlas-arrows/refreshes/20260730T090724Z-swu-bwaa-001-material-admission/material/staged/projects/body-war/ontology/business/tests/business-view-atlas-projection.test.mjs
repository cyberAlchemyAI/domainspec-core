import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  viewAtlasIsolateDispositions,
  viewAtlasLenses,
} from "../authoring/view-atlas-catalog.mjs";
import {
  ViewAtlasProjectionError,
  deriveLensFlows,
  projectViewAtlas,
} from "../scripts/view-atlas-projection.mjs";

const packageRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

async function source() {
  const nodeNames = (await readdir(path.join(packageRoot, "nodes")))
    .filter((name) => name.endsWith(".json") && name !== "manifest.json")
    .sort();
  const nodes = await Promise.all(
    nodeNames.map(async (name) =>
      JSON.parse(
        await readFile(path.join(packageRoot, "nodes", name), "utf8"),
      ),
    ),
  );
  const { relations } = JSON.parse(
    await readFile(
      path.join(packageRoot, "relations/relations.json"),
      "utf8",
    ),
  );
  return { nodes, relations };
}

function project(inputs, overrides = {}) {
  return projectViewAtlas({
    ...inputs,
    lenses: viewAtlasLenses,
    isolateDispositions: viewAtlasIsolateDispositions,
    ...overrides,
  });
}

function rejectsCode(fn, code) {
  assert.throws(
    fn,
    (error) =>
      error instanceof ViewAtlasProjectionError && error.code === code,
  );
}

test("six editorial lenses conserve every current node and relation", async () => {
  const inputs = await source();
  const projection = project(inputs);
  assert.deepEqual(projection.coverage, {
    lens_count: 6,
    business_kind_count: 17,
    node_count: 237,
    relation_count: 231,
    internal_relation_count: 122,
    portal_relation_count: 109,
    lens_flow_count: 13,
    lens_flow_relation_count: 109,
    zero_degree_node_count: 44,
  });
  assert.equal(
    new Set(projection.lenses.flatMap((lens) => lens.core_node_ids)).size,
    237,
  );
  assert.equal(
    new Set([
      ...projection.lenses.flatMap((lens) => lens.internal_relation_ids),
      ...projection.portals.map((portal) => portal.relation_id),
    ]).size,
    231,
  );
});

test("every observed kind maps once and missing or duplicate mappings reject", async () => {
  const inputs = await source();
  const mappedKinds = viewAtlasLenses.flatMap((lens) => lens.business_kinds);
  assert.equal(mappedKinds.length, 17);
  assert.equal(new Set(mappedKinds).size, 17);

  const withoutOutcome = viewAtlasLenses.map((lens) => ({
    ...lens,
    business_kinds: lens.business_kinds.filter((kind) => kind !== "outcome"),
  }));
  rejectsCode(
    () => project(inputs, { lenses: withoutOutcome }),
    "ATLAS_KIND_UNMAPPED",
  );

  const duplicateActor = viewAtlasLenses.map((lens, index) => ({
    ...lens,
    business_kinds:
      index === 1 ? [...lens.business_kinds, "actor"] : lens.business_kinds,
  }));
  rejectsCode(
    () => project(inputs, { lenses: duplicateActor }),
    "ATLAS_KIND_MULTIPLY_MAPPED",
  );
});

test("duplicate nodes, duplicate relations, and dangling endpoints reject", async () => {
  const inputs = await source();
  rejectsCode(
    () => project({ ...inputs, nodes: [...inputs.nodes, inputs.nodes[0]] }),
    "ATLAS_DUPLICATE_NODE",
  );
  rejectsCode(
    () =>
      project({
        ...inputs,
        relations: [...inputs.relations, inputs.relations[0]],
      }),
    "ATLAS_DUPLICATE_RELATION",
  );
  rejectsCode(
    () =>
      project({
        ...inputs,
        relations: [
          ...inputs.relations,
          {
            ...inputs.relations[0],
            relation_id: "body-war.relation.invalid-dangling-test",
            target_concept: "body-war.business.missing",
          },
        ],
      }),
    "ATLAS_UNKNOWN_ENDPOINT",
  );
});

test("the exact 44-node disposition set is complete and research-only", async () => {
  const inputs = await source();
  const projection = project(inputs);
  assert.equal(viewAtlasIsolateDispositions.length, 44);
  assert.deepEqual(
    projection.zero_degree_node_ids,
    viewAtlasIsolateDispositions
      .map((entry) => entry.concept_id)
      .sort((left, right) => left.localeCompare(right)),
  );

  rejectsCode(
    () =>
      project(inputs, {
        isolateDispositions: viewAtlasIsolateDispositions.slice(1),
      }),
    "ATLAS_DISPOSITION_MISSING",
  );
  rejectsCode(
    () =>
      project(inputs, {
        isolateDispositions: [
          ...viewAtlasIsolateDispositions,
          {
            concept_id: "body-war.business.actor.runner",
            disposition: "OWNER-DECISION",
          },
        ],
      }),
    "ATLAS_DISPOSITION_NON_ISOLATE",
  );
});

test("portals retain direction and parallel endpoint relations remain distinct", async () => {
  const inputs = await source();
  const projection = project(inputs);
  const portalById = new Map(
    projection.portals.map((portal) => [portal.relation_id, portal]),
  );
  for (const relation of inputs.relations) {
    const portal = portalById.get(relation.relation_id);
    if (!portal) continue;
    const sourceNode = inputs.nodes.find(
      (node) => node.concept_id === relation.source_concept,
    );
    const targetNode = inputs.nodes.find(
      (node) => node.concept_id === relation.target_concept,
    );
    const sourceLens = viewAtlasLenses.find((lens) =>
      lens.business_kinds.includes(sourceNode.business_kind),
    );
    const targetLens = viewAtlasLenses.find((lens) =>
      lens.business_kinds.includes(targetNode.business_kind),
    );
    assert.equal(portal.source_lens_id, sourceLens.lens_id);
    assert.equal(portal.target_lens_id, targetLens.lens_id);
  }

  assert.ok(portalById.has("body-war.relation.provider-belongs-runner"));
  assert.ok(portalById.has("body-war.relation.runner-owns-provider"));
  assert.notEqual(
    portalById.get("body-war.relation.provider-belongs-runner").relation_id,
    portalById.get("body-war.relation.runner-owns-provider").relation_id,
  );
});

test("directed lens flows partition all 109 portals in fixed lens order", async () => {
  const projection = project(await source());
  assert.deepEqual(
    projection.lens_flows.map(
      ({ source_lens_id, target_lens_id, relation_count }) => [
        source_lens_id,
        target_lens_id,
        relation_count,
      ],
    ),
    [
      ["participants-boundaries", "responsibilities", 1],
      ["participants-boundaries", "behavior", 12],
      ["participants-boundaries", "business-objects", 11],
      ["participants-boundaries", "governance-lifecycle", 1],
      ["behavior", "participants-boundaries", 2],
      ["behavior", "business-objects", 55],
      ["behavior", "governance-lifecycle", 13],
      ["behavior", "hypotheses-outcomes", 4],
      ["business-objects", "participants-boundaries", 1],
      ["business-objects", "governance-lifecycle", 5],
      ["business-objects", "hypotheses-outcomes", 2],
      ["hypotheses-outcomes", "business-objects", 1],
      ["hypotheses-outcomes", "governance-lifecycle", 1],
    ],
  );
  assert.deepEqual(
    projection.lens_flows.flatMap((flow) => flow.relation_ids).sort(),
    projection.portals.map((portal) => portal.relation_id).sort(),
  );
  for (const flow of projection.lens_flows) {
    assert.equal(flow.relation_count, flow.relation_ids.length);
    assert.deepEqual(flow.relation_ids, [...flow.relation_ids].sort());
    assert.notEqual(flow.source_lens_id, flow.target_lens_id);
  }
});

test("lens flow derivation rejects invalid groups and totals", () => {
  const lenses = [{ lens_id: "source" }, { lens_id: "target" }];
  const portal = {
    relation_id: "body-war.relation.synthetic",
    source_lens_id: "source",
    target_lens_id: "target",
  };
  assert.deepEqual(
    deriveLensFlows({
      lenses,
      portals: [portal],
      canonicalRelationIds: [portal.relation_id],
      expectedFlowCount: 1,
      expectedPortalCount: 1,
    }),
    [
      {
        source_lens_id: "source",
        target_lens_id: "target",
        relation_ids: ["body-war.relation.synthetic"],
        relation_count: 1,
      },
    ],
  );

  rejectsCode(
    () =>
      deriveLensFlows({
        lenses: [...lenses, lenses[0]],
        portals: [portal],
        canonicalRelationIds: [portal.relation_id],
        expectedFlowCount: 1,
        expectedPortalCount: 1,
      }),
    "ATLAS_DUPLICATE_LENS",
  );
  rejectsCode(
    () =>
      deriveLensFlows({
        lenses,
        portals: [{ ...portal, target_lens_id: "missing" }],
        canonicalRelationIds: [portal.relation_id],
        expectedFlowCount: 1,
        expectedPortalCount: 1,
      }),
    "ATLAS_FLOW_UNKNOWN_LENS",
  );
  rejectsCode(
    () =>
      deriveLensFlows({
        lenses,
        portals: [{ ...portal, target_lens_id: "source" }],
        canonicalRelationIds: [portal.relation_id],
        expectedFlowCount: 1,
        expectedPortalCount: 1,
      }),
    "ATLAS_FLOW_INTERNAL_PORTAL",
  );
  rejectsCode(
    () =>
      deriveLensFlows({
        lenses,
        portals: [portal, portal],
        canonicalRelationIds: [portal.relation_id],
        expectedFlowCount: 1,
        expectedPortalCount: 2,
      }),
    "ATLAS_FLOW_DUPLICATE_RELATION",
  );
  rejectsCode(
    () =>
      deriveLensFlows({
        lenses,
        portals: [portal],
        canonicalRelationIds: ["body-war.relation.other"],
        expectedFlowCount: 1,
        expectedPortalCount: 1,
      }),
    "ATLAS_FLOW_UNKNOWN_RELATION",
  );
  rejectsCode(
    () =>
      deriveLensFlows({
        lenses,
        portals: [portal],
        canonicalRelationIds: [portal.relation_id],
        expectedFlowCount: 2,
        expectedPortalCount: 1,
      }),
    "ATLAS_FLOW_GROUP_COUNT_MISMATCH",
  );
  rejectsCode(
    () =>
      deriveLensFlows({
        lenses,
        portals: [portal],
        canonicalRelationIds: [portal.relation_id],
        expectedFlowCount: 1,
        expectedPortalCount: 2,
      }),
    "ATLAS_FLOW_RELATION_COUNT_MISMATCH",
  );
});

test("all admitted authority effects and predicates remain covered", async () => {
  const inputs = await source();
  const projection = project(inputs);
  const covered = new Set([
    ...projection.lenses.flatMap((lens) => lens.internal_relation_ids),
    ...projection.portals.map((portal) => portal.relation_id),
  ]);
  for (const relation of inputs.relations) {
    assert.ok(covered.has(relation.relation_id), relation.relation_id);
  }
  assert.ok(
    inputs.relations.some(
      (relation) => relation.predicate === "does_not_promote",
    ),
  );
  assert.ok(inputs.relations.some((relation) => relation.predicate === "projects"));
});
