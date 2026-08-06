import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
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
  assert.equal(projection.schemaVersion, matrix.families.richCandidate.projection);
  assert.equal(manifest.schemaVersion, matrix.families.richCandidate.manifest);

  const contractUrl = pathToFileURL(path.join(CONSUMER_ROOT, "browser-first/host/augmentor-consultation-contract.mjs"));
  const consumer = await import(contractUrl.href);
  const liveVersions = {
    query: consumer.CONSULTATION_QUERY_VERSION,
    result: consumer.CONSULTATION_RESULT_VERSION,
    projection: consumer.CONSULTATION_PROJECTION_VERSION,
    manifest: consumer.CONSULTATION_MANIFEST_VERSION,
    evidenceStatement: consumer.CONSULTATION_EVIDENCE_STATEMENT_VERSION,
  };
  for (const [kind, version] of Object.entries(liveVersions)) {
    assert.equal(version, matrix.families.richCandidate[kind]);
  }
  assert.equal(matrix.compatibilityPolicy.implicitCrossVersionCompatibility, false);
  assert.equal(Object.values(matrix.families.live).includes("augmentor.consultation.query@0.1.0"), false);
});
