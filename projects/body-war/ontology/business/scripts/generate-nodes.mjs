import { readFile, mkdir, readdir, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { catalog } from "../authoring/catalog.mjs";

const packageRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const nodesRoot = path.join(packageRoot, "nodes");
const sourceManifest = JSON.parse(
  await readFile(path.join(packageRoot, "sources.json"), "utf8"),
);
const sourceDigests = new Map(
  sourceManifest.sources.map((source) => [source.path, source.sha256]),
);

function canonicalize(value) {
  if (Array.isArray(value)) {
    return value.map(canonicalize);
  }
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, canonicalize(value[key])]),
    );
  }
  return value;
}

function render(value) {
  return `${JSON.stringify(canonicalize(value), null, 2)}\n`;
}

function materialize(entry) {
  const digest = sourceDigests.get(entry.source);
  if (!digest) {
    throw new Error(`Missing source digest for ${entry.source}`);
  }
  const conceptId = `body-war.business.${entry.suffix}`;
  return {
    schema_version: "body-war-business-node/v1",
    concept_id: conceptId,
    label: entry.label,
    definition: entry.definition,
    concept_role: entry.conceptRole,
    business_kind: entry.businessKind,
    branch_roles: ["business"],
    source_refs: [
      {
        path: entry.source,
        selector: entry.selector,
        sha256: digest,
      },
    ],
    owner_route: entry.owner,
    candidate_status: entry.status,
    confidence: {
      evidence_confidence: entry.evidenceConfidence,
      commitment_confidence: entry.commitmentConfidence,
      basis: entry.basis,
    },
    challenge_contract: {
      challenge_response: entry.challengeResponse,
      valid_challenge_modes: [
        "evidence",
        "contradiction",
        "owner_review",
      ],
      contradiction_edges: [],
      validation_edges: [],
      owner_route: entry.owner,
      resolution_gate: entry.nextGate,
      blocking_questions: entry.blockingQuestions,
      challenge_residue_route: "projects/body-war/ontology/business/residue.json",
    },
    residue: entry.residue,
    forbidden_collapse: [entry.forbidden],
  };
}

const seen = new Set();
for (const entry of catalog) {
  const id = `body-war.business.${entry.suffix}`;
  if (seen.has(id)) {
    throw new Error(`Duplicate catalog concept: ${id}`);
  }
  seen.add(id);
}

await mkdir(nodesRoot, { recursive: true });
for (const name of await readdir(nodesRoot).catch(() => [])) {
  if (name.endsWith(".json")) {
    await rm(path.join(nodesRoot, name));
  }
}

for (const entry of [...catalog].sort((a, b) =>
  a.suffix.localeCompare(b.suffix),
)) {
  const filename = `${entry.suffix}.json`;
  await writeFile(path.join(nodesRoot, filename), render(materialize(entry)));
}

await writeFile(
  path.join(nodesRoot, "manifest.json"),
  render({
    schema_version: "body-war-business-node-manifest/v1",
    generated_from: "authoring/catalog.mjs",
    node_count: catalog.length,
    concept_ids: [...seen].sort(),
  }),
);

process.stdout.write(`generated ${catalog.length} Body War business nodes\n`);
