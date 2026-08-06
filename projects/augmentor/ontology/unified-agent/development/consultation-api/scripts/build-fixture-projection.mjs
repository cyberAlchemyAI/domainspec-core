import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const SOURCE = path.join(ROOT, "fixtures/source/ontology.json");
const OUTPUT = path.join(ROOT, "fixtures/generated/projection.json");
const MANIFEST = path.join(ROOT, "fixtures/generated/projection-manifest.json");
const ALLOWLIST = ["kind", "label", "summary", "view_ids", "responsibility", "boundary", "confidence"];
const sha = (value) => createHash("sha256").update(value).digest("hex");
const canonical = (value) => JSON.stringify(value, Object.keys(value).sort());
const opaque = (prefix, value) => `${prefix}-${sha(value).slice(0, 12)}`;

export const compileFixture = async () => {
  const sourceBytes = await readFile(SOURCE);
  const source = JSON.parse(sourceBytes);
  const sourceHandle = opaque("src", source.source_id);
  const records = source.records.map((record) => {
    const id = opaque("rec", record.private_id);
    const fields = { responsibility: record.responsibility, boundary: record.boundary };
    return {
      id,
      kind: record.kind,
      label: record.label,
      summary: record.summary,
      viewIds: record.view_ids,
      fields,
      fieldProvenance: Object.fromEntries(["label", "summary", ...Object.keys(fields)].map((field) => [field, sourceHandle])),
      sourceHandles: [sourceHandle],
      confidence: { level: record.confidence, ownerRef: source.owner_ref, basis: "fixture owner assertion", assessedAt: source.assessed_at, sourceHandle }
    };
  });
  const projection = {
    schemaVersion: "augmentor.consultation.projection@0.1.0",
    records,
    structuredConflicts: source.structured_conflicts
  };
  const outputBytes = `${JSON.stringify(projection, null, 2)}\n`;
  const counts = records.reduce((result, record) => ({ ...result, [record.kind]: (result[record.kind] ?? 0) + 1 }), {});
  const manifest = {
    schemaVersion: "augmentor.consultation.projection-manifest@0.1.0",
    compilerVersion: "fixture-compiler@0.1.0",
    allowlistDigest: sha(canonical(ALLOWLIST)),
    opaqueIdMapVersion: "sha256-prefix@1.0.0",
    inputSources: [{ sourceHandle, sha256: sha(sourceBytes) }],
    recordCounts: counts,
    generatedAt: source.assessed_at,
    outputDigest: sha(outputBytes),
    ownerApprovalRef: "fixture-only:aug-consultation-l0"
  };
  return { outputBytes, manifestBytes: `${JSON.stringify(manifest, null, 2)}\n`, projection, manifest };
};

const main = async () => {
  const expected = await compileFixture();
  if (process.argv.includes("--check")) {
    const [actualOutput, actualManifest] = await Promise.all([readFile(OUTPUT, "utf8"), readFile(MANIFEST, "utf8")]);
    if (actualOutput !== expected.outputBytes || actualManifest !== expected.manifestBytes) throw new Error("generated fixture projection is stale");
    console.log(`PROJECTION_CHECK=pass sha256=${expected.manifest.outputDigest}`);
    return;
  }
  await mkdir(path.dirname(OUTPUT), { recursive: true });
  await Promise.all([writeFile(OUTPUT, expected.outputBytes), writeFile(MANIFEST, expected.manifestBytes)]);
  console.log(`PROJECTION_BUILD=pass sha256=${expected.manifest.outputDigest}`);
};

if (process.argv[1] === fileURLToPath(import.meta.url)) await main();
