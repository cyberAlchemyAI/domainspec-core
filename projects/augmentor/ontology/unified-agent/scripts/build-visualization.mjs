import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { validateAnatomyMap } from "./validate-anatomy-map.mjs";

const PACKAGE_ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const TEMPLATE_PATH = path.join(PACKAGE_ROOT, "visualization/template.html");
const OUTPUT_PATH = path.join(PACKAGE_ROOT, "ontology-visualization.html");
const DATA_MARKER = "/*__ONTOLOGY_DATA__*/";
const ROBOT_ASSET_MARKER = "/*__ROBOT_ASSET_DATA_URL__*/";
const ROBOT_ASSET_PATH = path.join(PACKAGE_ROOT, "visualization/assets/neural-torso.png");
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

export const ROBOT_ASSET_SHA256 = "804efd5d6d761efae90af519d2f6e3d1126cca7ff2cc53697dddb72f54b6d061";
export const ROBOT_ASSET_DIMENSIONS = Object.freeze({width: 1122, height: 1402});

const readJson = async (relativePath) =>
  JSON.parse(await readFile(path.join(PACKAGE_ROOT, relativePath), "utf8"));

const sha256 = (value) => createHash("sha256").update(value).digest("hex");

const escapeEmbeddedJson = (value) =>
  value
    .replaceAll("<", "\\u003c")
    .replaceAll(">", "\\u003e")
    .replaceAll("&", "\\u0026");

const markerCount = (source, marker) => source.split(marker).length - 1;

export const validateRobotAsset = (asset) => {
  if (!Buffer.isBuffer(asset) || asset.length < 24 || !asset.subarray(0, 8).equals(PNG_SIGNATURE)) {
    throw new Error("Robot asset must be a valid PNG");
  }
  if (asset.toString("ascii", 12, 16) !== "IHDR") {
    throw new Error("Robot asset is missing the PNG IHDR header");
  }
  const dimensions = {width: asset.readUInt32BE(16), height: asset.readUInt32BE(20)};
  if (
    dimensions.width !== ROBOT_ASSET_DIMENSIONS.width ||
    dimensions.height !== ROBOT_ASSET_DIMENSIONS.height
  ) {
    throw new Error(
      `Robot asset dimensions changed: expected ${ROBOT_ASSET_DIMENSIONS.width}x${ROBOT_ASSET_DIMENSIONS.height}, received ${dimensions.width}x${dimensions.height}`
    );
  }
  const digest = sha256(asset);
  if (digest !== ROBOT_ASSET_SHA256) {
    throw new Error(`Robot asset digest changed: expected ${ROBOT_ASSET_SHA256}, received ${digest}`);
  }
  return {digest, ...dimensions};
};

export const embedRobotAsset = (template, asset) => {
  const count = markerCount(template, ROBOT_ASSET_MARKER);
  if (count !== 1) {
    throw new Error(`Visualization template must contain exactly one ${ROBOT_ASSET_MARKER}; found ${count}`);
  }
  validateRobotAsset(asset);
  return template.replace(ROBOT_ASSET_MARKER, `data:image/png;base64,${asset.toString("base64")}`);
};

export const loadVisualizationData = async () => {
  const [profile, sources, nodes, relations, residue, beginnerExplanations, anatomy] = await Promise.all([
    readJson("profile.json"),
    readJson("sources.json"),
    readJson("nodes/nodes.json"),
    readJson("relations/relations.json"),
    readJson("residue.json"),
    readJson("explanations/beginner.json"),
    readJson("visualization/anatomy-map.json")
  ]);
  const anatomyValidation = validateAnatomyMap({anatomy, nodes: nodes.nodes, relations: relations.relations});
  if (anatomyValidation.status !== "pass") {
    throw new Error(`Anatomy map validation failed:\n${anatomyValidation.errors.join("\n")}`);
  }
  const views = await Promise.all(
    profile.views.map(async (descriptor) => ({
      descriptor,
      document: await readJson(descriptor.path)
    }))
  );

  const core = {
    visualization_contract: {
      schema: "augmentor.ontology-visualization@0.1.0",
      ontology_type: "authority-governance",
      ontology_type_selection_source: "inferred",
      ontology_type_selection_confidence: "high",
      ambiguity_candidates: [],
      user_selection_required: false,
      branch_scope: "mixed",
      authority_effect: "none",
      output_kind: "interpretive-read-model"
    },
    profile,
    sources,
    nodes: nodes.nodes,
    relations: relations.relations,
    views,
    residue: residue.items,
    beginner_explanations: beginnerExplanations,
    anatomy
  };

  return {
    ...core,
    visualization_bundle_digest: sha256(JSON.stringify(core))
  };
};

export const buildVisualization = async () => {
  const [template, data, robotAsset] = await Promise.all([
    readFile(TEMPLATE_PATH, "utf8"),
    loadVisualizationData(),
    readFile(ROBOT_ASSET_PATH)
  ]);
  const dataMarkerCount = markerCount(template, DATA_MARKER);
  if (dataMarkerCount !== 1) {
    throw new Error(`Visualization template must contain exactly one ${DATA_MARKER}; found ${dataMarkerCount}`);
  }
  const withData = template.replace(DATA_MARKER, escapeEmbeddedJson(JSON.stringify(data)));
  return embedRobotAsset(withData, robotAsset);
};

const isMain = process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;

if (isMain) {
  const html = await buildVisualization();
  if (process.argv.includes("--check")) {
    const current = await readFile(OUTPUT_PATH, "utf8").catch(() => "");
    if (current !== html) {
      process.stderr.write("VISUALIZATION=stale\n");
      process.exitCode = 1;
    } else {
      process.stdout.write(`VISUALIZATION=pass bytes=${Buffer.byteLength(html)} sha256=${sha256(html)}\n`);
    }
  } else {
    await writeFile(OUTPUT_PATH, html, "utf8");
    process.stdout.write(`VISUALIZATION=written path=${OUTPUT_PATH} bytes=${Buffer.byteLength(html)} sha256=${sha256(html)}\n`);
  }
}
