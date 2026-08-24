import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const PACKAGE_ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const readJson = async (relativePath) => JSON.parse(await readFile(path.join(PACKAGE_ROOT, relativePath), "utf8"));

const expectedLabels = {
  observed: "Found in sources",
  designed: "Designed, not a live Augmentor path",
  absent: "Not built",
  blocked: "Blocked at named gate",
  deferred: "Planned for later",
  mixed: "Mixed state — inspect each part",
  "selection-ready": "External · planned · not installed"
};

export const loadAnatomyInputs = async () => {
  const [anatomy, nodeDocument, relationDocument] = await Promise.all([
    readJson("visualization/anatomy-map.json"),
    readJson("nodes/nodes.json"),
    readJson("relations/relations.json")
  ]);
  return { anatomy, nodes: nodeDocument.nodes, relations: relationDocument.relations };
};

export const validateAnatomyMap = ({ anatomy, nodes, relations }) => {
  const errors = [];
  const fail = (code, detail) => errors.push(`${code}: ${detail}`);
  if (anatomy?.schema !== "augmentor.ontology-anatomy-map@0.1.0") fail("schema", "unsupported anatomy schema");
  for (const [posture, label] of Object.entries(expectedLabels)) {
    if (anatomy?.status_grammar?.[posture] !== label) fail("status-label", `${posture} must be labelled ${label}`);
  }

  const nodeById = new Map(nodes.map((item) => [item.concept_id, item]));
  const relationById = new Map(relations.map((item) => [item.relation_id, item]));
  const mappedNodes = new Map();
  const mappedRelations = new Map();
  const regions = anatomy?.regions ?? [];

  for (const region of regions) {
    for (const field of ["id", "label", "plain_explanation", "overview_posture", "owner_summary", "limitation"]) {
      if (!region[field]) fail("region-field", `${region.id ?? "unknown"} lacks ${field}`);
    }
    if (!Array.isArray(region.source_refs) || !region.source_refs.length) fail("source-ref", `${region.id} lacks a source reference`);
    if (![...(region.concepts ?? []), ...(region.relations ?? [])].length) fail("technical-target", `${region.id} lacks an exact Technical Map target`);

    // The organ overview is a summary of mapped concepts. Relations keep their
    // own exact posture in the inspector and must not optimistically repaint an
    // absent concept (for example an absent gate with a designed stop edge).
    const postures = new Set((region.concepts ?? []).map((item) => item.posture));
    if (postures.size > 1 && region.overview_posture !== "mixed") fail("optimistic-mixed-status", `${region.id} must expose mixed child state`);
    if (postures.size === 1 && ![...postures].includes(region.overview_posture)) fail("posture-summary", `${region.id} summary differs from its children`);

    for (const binding of region.concepts ?? []) {
      const source = nodeById.get(binding.id);
      if (!source) { fail("unknown-concept", binding.id); continue; }
      if (mappedNodes.has(binding.id)) fail("duplicate-concept", `${binding.id} appears in ${mappedNodes.get(binding.id)} and ${region.id}`);
      mappedNodes.set(binding.id, region.id);
      if (binding.posture !== source.runtime_posture) fail("concept-posture", `${binding.id} expected ${source.runtime_posture}, received ${binding.posture}`);
      if (binding.owner !== source.owner_route) fail("concept-owner", `${binding.id} expected ${source.owner_route}, received ${binding.owner}`);
    }
    for (const binding of region.relations ?? []) {
      const source = relationById.get(binding.id);
      if (!source) { fail("unknown-relation", binding.id); continue; }
      if (mappedRelations.has(binding.id)) fail("duplicate-relation", `${binding.id} appears in ${mappedRelations.get(binding.id)} and ${region.id}`);
      mappedRelations.set(binding.id, region.id);
      if (binding.posture !== source.runtime_posture) fail("relation-posture", `${binding.id} expected ${source.runtime_posture}, received ${binding.posture}`);
      if (binding.owner !== source.owner_route) fail("relation-owner", `${binding.id} expected ${source.owner_route}, received ${binding.owner}`);
    }
    for (const id of region.shared_concepts ?? []) {
      if (!nodeById.has(id)) fail("unknown-shared-concept", id);
    }
  }

  for (const id of nodeById.keys()) if (!mappedNodes.has(id)) fail("missing-concept", id);
  for (const id of mappedNodes.keys()) if (!nodeById.has(id)) fail("unknown-concept", id);
  for (const id of relationById.keys()) if (!mappedRelations.has(id)) fail("missing-relation", id);
  for (const id of mappedRelations.keys()) if (!relationById.has(id)) fail("unknown-relation", id);

  const heart = regions.find((region) => region.id === "heart");
  if (!heart || !/deferred/i.test(heart.label) || heart.overview_posture !== "deferred") fail("heart-label", "heart must be explicitly deferred");
  if (!heart?.topology?.detached || !heart?.topology?.optional || heart?.topology?.animated || heart?.topology?.interrupts_main_path) fail("heart-topology", "heart must be detached, optional, dormant, and outside the main path");
  if (anatomy?.main_path?.includes("heart")) fail("required-heart", "heart cannot interrupt the current route/evidence path");

  const sdk = anatomy?.external_seams?.find((item) => item.id === "addon-sdk");
  if (!sdk || !/planned/i.test(sdk.label) || !/not installed/i.test(sdk.limitation)) fail("sdk-label", "SDK must be planned and not installed");
  if (sdk?.ontology_refs?.length) fail("sdk-imported", "external SDK cannot be inserted into ontology records");
  if (!sdk?.topology?.disconnected || sdk?.topology?.hands || sdk?.topology?.action_pose) fail("sdk-topology", "SDK seam must stay disconnected and non-capable-looking");

  const normalized = JSON.stringify(anatomy).toLowerCase();
  if (/privacy (?:gate|control|protection|enforcement|mechanism is implemented)/.test(normalized)) fail("privacy-claim", "no privacy mechanism is supported by the mapped sources");
  if (anatomy?.package_disclaimer?.authority_effect !== "none") fail("authority-effect", "package authority effect must remain none");
  if (anatomy?.package_disclaimer?.release_admission !== "not-granted") fail("release-admission", "release must remain not granted");

  return {
    status: errors.length ? "block" : "pass",
    errors,
    coverage: {concepts: mappedNodes.size, relations: mappedRelations.size, regions: regions.length, external_seams: anatomy?.external_seams?.length ?? 0}
  };
};

const isMain = process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;
if (isMain) {
  const result = validateAnatomyMap(await loadAnatomyInputs());
  if (result.status !== "pass") {
    process.stderr.write(`${result.errors.join("\n")}\n`);
    process.exitCode = 1;
  } else {
    process.stdout.write(`ANATOMY_MAP=pass concepts=${result.coverage.concepts} relations=${result.coverage.relations} regions=${result.coverage.regions} external_seams=${result.coverage.external_seams}\n`);
  }
}
