import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const PACKAGE_ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const TEMPLATE_PATH = path.join(PACKAGE_ROOT, "visualization/template.html");
const OUTPUT_PATH = path.join(PACKAGE_ROOT, "ontology-visualization.html");
const DATA_MARKER = "/*__ONTOLOGY_DATA__*/";

const readJson = async (relativePath) =>
  JSON.parse(await readFile(path.join(PACKAGE_ROOT, relativePath), "utf8"));

const sha256 = (value) => createHash("sha256").update(value).digest("hex");

const escapeEmbeddedJson = (value) =>
  value
    .replaceAll("<", "\\u003c")
    .replaceAll(">", "\\u003e")
    .replaceAll("&", "\\u0026");

export const loadVisualizationData = async () => {
  const [profile, sources, nodes, relations, residue, beginnerExplanations] = await Promise.all([
    readJson("profile.json"),
    readJson("sources.json"),
    readJson("nodes/nodes.json"),
    readJson("relations/relations.json"),
    readJson("residue.json"),
    readJson("explanations/beginner.json")
  ]);
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
    beginner_explanations: beginnerExplanations
  };

  return {
    ...core,
    visualization_bundle_digest: sha256(JSON.stringify(core))
  };
};

export const buildVisualization = async () => {
  const [template, data] = await Promise.all([
    readFile(TEMPLATE_PATH, "utf8"),
    loadVisualizationData()
  ]);
  if (!template.includes(DATA_MARKER)) {
    throw new Error(`Visualization template is missing ${DATA_MARKER}`);
  }
  return template.replace(DATA_MARKER, escapeEmbeddedJson(JSON.stringify(data)));
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
