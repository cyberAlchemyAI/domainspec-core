import { createHash } from "node:crypto";
import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  viewAtlasBoundary,
  viewAtlasIsolateDispositions,
  viewAtlasLenses,
} from "../authoring/view-atlas-catalog.mjs";
import { projectViewAtlas } from "./view-atlas-projection.mjs";

const packageRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const receiptPath = path.join(
  packageRoot,
  "receipts/view-atlas-coverage-receipt.json",
);

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

async function digestFile(filePath) {
  return sha256(await readFile(filePath));
}

async function digestDirectory(directory) {
  const members = [];
  async function walk(current) {
    const entries = await readdir(current, { withFileTypes: true });
    for (const entry of entries.sort((a, b) => a.name.localeCompare(b.name))) {
      const absolute = path.join(current, entry.name);
      if (entry.isDirectory()) {
        await walk(absolute);
      } else if (entry.isFile()) {
        members.push({
          path: path.relative(directory, absolute).split(path.sep).join("/"),
          sha256: await digestFile(absolute),
        });
      }
    }
  }
  await walk(directory);
  return sha256(JSON.stringify(members));
}

async function readSource() {
  const nodeRoot = path.join(packageRoot, "nodes");
  const nodeNames = (await readdir(nodeRoot))
    .filter((name) => name.endsWith(".json") && name !== "manifest.json")
    .sort();
  const nodes = await Promise.all(
    nodeNames.map(async (name) =>
      JSON.parse(await readFile(path.join(nodeRoot, name), "utf8")),
    ),
  );
  const relationDocument = JSON.parse(
    await readFile(
      path.join(packageRoot, "relations/relations.json"),
      "utf8",
    ),
  );
  return { nodes, relations: relationDocument.relations };
}

const { nodes, relations } = await readSource();
const projection = projectViewAtlas({
  nodes,
  relations,
  lenses: viewAtlasLenses,
  isolateDispositions: viewAtlasIsolateDispositions,
});

const expected = {
  lens_count: 6,
  business_kind_count: 17,
  node_count: 237,
  relation_count: 231,
  internal_relation_count: 122,
  portal_relation_count: 109,
  zero_degree_node_count: 44,
};
for (const [field, value] of Object.entries(expected)) {
  if (projection.coverage[field] !== value) {
    throw new Error(
      `${field} expected ${value}, received ${projection.coverage[field]}`,
    );
  }
}

const receipt = {
  schema_version: "body-war-view-atlas-coverage-receipt/v1",
  status: "pass",
  generated_at: new Date().toISOString(),
  source_digests: {
    nodes: await digestDirectory(path.join(packageRoot, "nodes")),
    relations: await digestFile(
      path.join(packageRoot, "relations/relations.json"),
    ),
    lifecycle_policies: await digestDirectory(
      path.join(packageRoot, "lifecycle-policies"),
    ),
    profile: await digestFile(path.join(packageRoot, "profile.json")),
    residue: await digestFile(path.join(packageRoot, "residue.json")),
    business_view: await digestFile(
      path.join(packageRoot, "views/business.json"),
    ),
    atlas_catalog: await digestFile(
      path.join(packageRoot, "authoring/view-atlas-catalog.mjs"),
    ),
    projection_module: await digestFile(
      path.join(packageRoot, "scripts/view-atlas-projection.mjs"),
    ),
  },
  coverage: projection.coverage,
  invariants: [
    "six editorial lenses and seventeen literal kinds mapped exactly once",
    "237 unique core nodes assigned exactly once",
    "231 unique relations partitioned into 122 internal and 109 portal relations",
    "portal indexes preserve one canonical relation identity and direction",
    "44 zero-degree nodes equal the exact research disposition registry",
    "no node relation lifecycle profile residue or branch input was mutated",
  ],
  authority_effect: viewAtlasBoundary.authority_effect,
  release_admission: viewAtlasBoundary.release_admission,
  claim_ceiling:
    "Deterministic candidate projection coverage only; no ontology promotion, comprehension, release, deployment, or production evidence.",
};

await mkdir(path.dirname(receiptPath), { recursive: true });
await writeFile(receiptPath, `${JSON.stringify(receipt, null, 2)}\n`);
process.stdout.write(
  `view atlas coverage pass: ${projection.coverage.node_count} nodes, ${projection.coverage.relation_count} relations, ${projection.coverage.zero_degree_node_count} zero-degree\n`,
);

