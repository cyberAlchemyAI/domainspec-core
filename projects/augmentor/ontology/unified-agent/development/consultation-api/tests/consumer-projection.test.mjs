import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";

import { buildConsumerProjection } from "../scripts/build-consumer-projection.mjs";

const root = path.resolve(import.meta.dirname, "..", "generated", "consumer");

test("real ontology compiles to a strict, opaque, jargon-reduced consumer projection", async () => {
  await buildConsumerProjection({ outputRoot: root, check: true });
  const projection = JSON.parse(await readFile(path.join(root, "projection.json"), "utf8"));
  const glossary = JSON.parse(await readFile(path.join(root, "glossary.json"), "utf8"));
  const manifest = JSON.parse(await readFile(path.join(root, "projection-manifest.json"), "utf8"));
  assert.equal(projection.records.length, 22);
  assert.equal(manifest.recordCounts.records, 22);
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
});
