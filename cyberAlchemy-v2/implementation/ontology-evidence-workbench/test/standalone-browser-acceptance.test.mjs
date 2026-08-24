import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const receipt = JSON.parse(await readFile(new URL("../generated/runs/WP-SOEW-001/full-body-war-browser-acceptance.json", import.meta.url), "utf8"));
test("standalone Body War browser receipt is terminal and bounded", () => {
  assert.equal(receipt.schema_version, "oew.standalone-browser-acceptance.v1");
  assert.equal(receipt.work_pack_id, "WP-SOEW-001");
  assert.equal(receipt.result, "pass");
  assert.equal(receipt.authority_effect, "none");
  assert.equal(receipt.dataset.nodes, 237);
  assert.equal(receipt.dataset.relations, 231);
  assert.equal(receipt.errors.length, 0);
  assert.ok(receipt.journeys.length >= 8);
  assert.ok(receipt.journeys.every((journey) => journey.result === "pass"));
  assert.ok(receipt.artifacts.length >= 2);
});
