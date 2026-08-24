import assert from "node:assert/strict";
import test from "node:test";
import { compileFixture } from "../scripts/build-fixture-projection.mjs";

test("fixture compiler is deterministic and allowlisted", async () => {
  const first = await compileFixture();
  const second = await compileFixture();
  assert.equal(first.outputBytes, second.outputBytes);
  assert.equal(first.manifestBytes, second.manifestBytes);
  assert.equal(first.projection.records.length, 3);
  assert.ok(first.projection.records.every((record) => record.id.startsWith("rec-") && !Object.hasOwn(record, "private_id") && !Object.hasOwn(record, "internal_note")));
});

test("manifest binds compiler, source, allowlist, and output", async () => {
  const { manifest } = await compileFixture();
  assert.equal(manifest.compilerVersion, "fixture-compiler@0.1.0");
  assert.match(manifest.outputDigest, /^[a-f0-9]{64}$/);
  assert.equal(manifest.ownerApprovalRef, "fixture-only:aug-consultation-l0");
});
