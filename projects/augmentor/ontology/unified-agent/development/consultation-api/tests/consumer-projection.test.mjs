import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";

import { buildConsumerProjection } from "../scripts/build-consumer-projection.mjs";

const apiRoot = path.resolve(import.meta.dirname, "..");
const root = path.join(apiRoot, "generated", "consumer");
const anatomySourcePath = path.resolve(apiRoot, "..", "..", "visualization", "anatomy-map.json");

test("real ontology compiles to a strict, opaque, jargon-reduced consumer projection", async () => {
  await buildConsumerProjection({ outputRoot: root, check: true });
  const projection = JSON.parse(await readFile(path.join(root, "projection.json"), "utf8"));
  const glossary = JSON.parse(await readFile(path.join(root, "glossary.json"), "utf8"));
  const manifest = JSON.parse(await readFile(path.join(root, "projection-manifest.json"), "utf8"));
  const anatomyFocusMap = JSON.parse(await readFile(path.join(root, "anatomy-focus-map.json"), "utf8"));
  const anatomyFocusMapSchema = JSON.parse(await readFile(path.join(root, "schemas", "anatomy-focus-map.schema.json"), "utf8"));
  const anatomySource = JSON.parse(await readFile(anatomySourcePath, "utf8"));
  assert.equal(projection.records.length, 22);
  assert.equal(projection.schemaVersion, "augmentor.consultation.projection@1.2.0");
  assert.equal(manifest.recordCounts.records, 22);
  assert.equal(manifest.recordCounts.mappings, 9);
  assert.equal(manifest.schemaVersion, "augmentor.consultation.projection-manifest@1.2.0");
  assert.equal(manifest.schemaVersions.anatomyFocusMap, "augmentor.consultation.anatomy-focus-map@1.2.0");
  assert.match(manifest.anatomyFocusMapDigest, /^[a-f0-9]{64}$/);
  assert.equal(manifest.anatomyFocusMapVersion, anatomySource.schema);
  assert.equal(anatomyFocusMap.schemaVersion, "augmentor.consultation.anatomy-focus-map@1.2.0");
  assert.equal(anatomyFocusMapSchema.$id, anatomyFocusMap.schemaVersion);
  assert.deepEqual(anatomyFocusMap.mappings.map((mapping) => mapping.anatomyRegionId), anatomySource.regions.map((region) => region.id));
  assert.equal(new Set(anatomyFocusMap.mappings.map((mapping) => mapping.anatomyRegionId)).size, anatomySource.regions.length);
  assert.equal(glossary.terms.length, 14);
  assert.equal(manifest.recordCounts.terms, 14);
  assert.match(manifest.bundleDigest, /^[a-f0-9]{64}$/);
  assert.match(manifest.ownerApprovalRef, /^approval-[a-f0-9]{12}$/);
  const serialized = JSON.stringify({ projection, glossary, manifest });
  assert.doesNotMatch(serialized, /aug\.concept|\/home\/|domainspec-core|cyberAlchemy|concrete_example/i);
  for (const record of projection.records) {
    assert.match(record.id, /^rec-[a-f0-9]{12}$/);
    assert.ok(record.sourceHandles.every((handle) => /^src-[a-f0-9]{12}$/.test(handle)));
    assert.deepEqual(Object.keys(record.fields).sort(), ["boundary", "responsibility"]);
    assert.equal(record.explanationSupport.state.scope, "ontology-model");
    assert.ok(record.explanationSupport.analogy.limitation.length > 0);
    assert.ok(record.explanationSupport.glossaryRefs.length >= 2);
    assert.ok(record.explanationSupport.glossaryRefs.every((ref) => /^term-[a-f0-9]{12}$/.test(ref)));
  }
  const recordsById = new Map(projection.records.map((record) => [record.id, record]));
  for (const mapping of anatomyFocusMap.mappings) {
    assert.ok(mapping.recordIds.length > 0);
    assert.ok(mapping.viewIds.length > 0);
    assert.equal(new Set(mapping.recordIds).size, mapping.recordIds.length);
    assert.equal(new Set(mapping.viewIds).size, mapping.viewIds.length);
    for (const recordId of mapping.recordIds) {
      assert.match(recordId, /^rec-[a-f0-9]{12}$/);
      const record = recordsById.get(recordId);
      assert.ok(record, `${mapping.anatomyRegionId} must resolve ${recordId}`);
      assert.ok(mapping.viewIds.some((viewId) => record.viewIds.includes(viewId)), `${mapping.anatomyRegionId} must retain a compatible view for ${recordId}`);
    }
  }
  assert.doesNotMatch(JSON.stringify(anatomyFocusMap), /aug\.concept|addon-sdk/i);
});
