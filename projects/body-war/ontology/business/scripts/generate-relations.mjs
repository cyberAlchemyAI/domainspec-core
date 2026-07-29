import { readFile, mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { relations } from "../authoring/relations.mjs";

const packageRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const relationRoot = path.join(packageRoot, "relations");
const sourceManifest = JSON.parse(
  await readFile(path.join(packageRoot, "sources.json"), "utf8"),
);
const sourceDigests = new Map(
  sourceManifest.sources.map((source) => [source.path, source.sha256]),
);

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
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

const seen = new Set();
const materialized = relations.map((entry) => {
  const relationId = `body-war.relation.${entry.suffix}`;
  if (seen.has(relationId)) throw new Error(`Duplicate relation: ${relationId}`);
  seen.add(relationId);
  const sha256 = sourceDigests.get(entry.source);
  if (!sha256) throw new Error(`Missing source digest: ${entry.source}`);
  return {
    schema_version: "body-war-business-relation/v1",
    relation_id: relationId,
    predicate: entry.predicate,
    source_concept: `body-war.business.${entry.sourceSuffix}`,
    target_concept: `body-war.business.${entry.targetSuffix}`,
    direction: entry.direction,
    owner_route: entry.owner,
    evidence_refs: [
      {
        path: entry.source,
        selector: entry.selector,
        sha256,
      },
    ],
    authority_effect: entry.authorityEffect,
    value_effect: entry.valueEffect,
    cycle_policy: entry.cyclePolicy,
    forbidden_collapse: [entry.forbidden],
  };
});

await mkdir(relationRoot, { recursive: true });
await writeFile(
  path.join(relationRoot, "relations.json"),
  render({
    schema_version: "body-war-business-relation-set/v1",
    relation_count: materialized.length,
    relations: materialized.sort((a, b) =>
      a.relation_id.localeCompare(b.relation_id),
    ),
  }),
);

process.stdout.write(`generated ${materialized.length} Body War relations\n`);
