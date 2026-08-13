import assert from "node:assert/strict";
import { cp, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

const TEST_ROOT = path.dirname(fileURLToPath(import.meta.url));
const API_ROOT = path.resolve(TEST_ROOT, "..");
const REPOSITORY_ROOT = path.resolve(TEST_ROOT, "../../../../../../..");
const CONSUMER_ROOT = process.env.RESONANTOS_CONSUMER_ROOT
  ? path.resolve(process.env.RESONANTOS_CONSUMER_ROOT)
  : path.resolve(REPOSITORY_ROOT, "../workspace-resonant/2.0.0-alpha");

const load = async (relative) => JSON.parse(await readFile(path.join(API_ROOT, relative), "utf8"));
const contractUrl = pathToFileURL(path.join(CONSUMER_ROOT, "browser-first/host/augmentor-consultation-contract.mjs"));
const consumer = await import(contractUrl.href);

async function withBundleCopy(run) {
  const parent = await mkdtemp(path.join(os.tmpdir(), "augmentor-focus-bundle-"));
  const root = path.join(parent, "bundle");
  try {
    await cp(path.join(API_ROOT, "generated", "consumer"), root, { recursive: true });
    return await run(root);
  } finally {
    await rm(parent, { recursive: true, force: true });
  }
}

test("fixture and live consultation contract families remain explicit and fail closed", async () => {
  const matrix = await load("schemas/contract-families.json");
  const schemaFiles = {
    query: "query.schema.json",
    result: "result.schema.json",
    projection: "projection.schema.json",
    manifest: "projection-manifest.schema.json",
    evidenceStatement: "evidence-statement.schema.json",
  };
  for (const [kind, name] of Object.entries(schemaFiles)) {
    const schema = await load(`schemas/${name}`);
    assert.equal(schema.$id, matrix.families.fixtureOnly[kind]);
  }

  const projection = await load("generated/consumer/projection.json");
  const manifest = await load("generated/consumer/projection-manifest.json");
  const anatomyFocusMap = await load("generated/consumer/anatomy-focus-map.json");
  const anatomyFocusMapSchema = await load("schemas/anatomy-focus-map.schema.json");
  assert.equal(projection.schemaVersion, matrix.families.richCandidate.projection);
  assert.equal(manifest.schemaVersion, matrix.families.richCandidate.manifest);
  assert.equal(anatomyFocusMap.schemaVersion, matrix.families.richCandidate.anatomyFocusMap);
  assert.equal(anatomyFocusMapSchema.$id, matrix.families.richCandidate.anatomyFocusMap);

  const focusVersions = {
    query: consumer.CONSULTATION_FOCUS_QUERY_VERSION,
    result: consumer.CONSULTATION_FOCUS_RESULT_VERSION,
    projection: consumer.CONSULTATION_FOCUS_PROJECTION_VERSION,
    manifest: consumer.CONSULTATION_FOCUS_MANIFEST_VERSION,
    evidenceStatement: consumer.CONSULTATION_EVIDENCE_STATEMENT_VERSION,
    glossary: consumer.CONSULTATION_GLOSSARY_VERSION,
    explanationSupport: consumer.CONSULTATION_EXPLANATION_SUPPORT_VERSION,
    anatomyFocusMap: consumer.CONSULTATION_ANATOMY_FOCUS_MAP_VERSION,
  };
  for (const [kind, version] of Object.entries(focusVersions)) {
    assert.equal(version, matrix.families.richCandidate[kind]);
  }
  assert.equal(matrix.compatibilityPolicy.implicitCrossVersionCompatibility, false);
  assert.equal(Object.values(matrix.families.live).includes("augmentor.consultation.query@0.1.0"), false);
  const bundle = await consumer.loadConsultationProjectionBundle({ root: path.join(API_ROOT, "generated", "consumer") });
  assert.equal(bundle.manifest.schemaVersion, consumer.CONSULTATION_FOCUS_MANIFEST_VERSION);
  assert.equal(bundle.anatomyFocusMap.mappings.length, bundle.manifest.recordCounts.mappings);
});

test("focused bundle fails closed for missing, malformed, unknown, incompatible, and digest-mismatched anatomy maps", async () => {
  await withBundleCopy(async (root) => {
    await rm(path.join(root, "anatomy-focus-map.json"));
    await assert.rejects(consumer.loadConsultationProjectionBundle({ root }), /ENOENT/);
  });
  await withBundleCopy(async (root) => {
    await writeFile(path.join(root, "anatomy-focus-map.json"), "{}\n");
    await assert.rejects(consumer.loadConsultationProjectionBundle({ root }), /Invalid consultation projection/);
  });
  await withBundleCopy(async (root) => {
    const mapPath = path.join(root, "anatomy-focus-map.json");
    const map = JSON.parse(await readFile(mapPath, "utf8"));
    map.mappings[0].recordIds = ["rec-000000000000"];
    await writeFile(mapPath, `${JSON.stringify(map)}\n`);
    await assert.rejects(consumer.loadConsultationProjectionBundle({ root }), /unknown record/);
  });
  await withBundleCopy(async (root) => {
    const mapPath = path.join(root, "anatomy-focus-map.json");
    const map = JSON.parse(await readFile(mapPath, "utf8"));
    map.mappings[0].viewIds = ["not-a-view"];
    await writeFile(mapPath, `${JSON.stringify(map)}\n`);
    await assert.rejects(consumer.loadConsultationProjectionBundle({ root }), /has no mapped view/);
  });
  await withBundleCopy(async (root) => {
    const manifestPath = path.join(root, "projection-manifest.json");
    const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
    manifest.anatomyFocusMapDigest = "0".repeat(64);
    await writeFile(manifestPath, `${JSON.stringify(manifest)}\n`);
    await assert.rejects(consumer.loadConsultationProjectionBundle({ root }), /anatomy focus map digest mismatch/);
  });
});
