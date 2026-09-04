import assert from "node:assert/strict";
import test from "node:test";

import {inspectProduct, materializeProductClosure} from "../src/product.mjs";

test("integrated ARE product has an exact runtime, verified profile, and complete component closure", () => {
  const health = inspectProduct({require_exact_runtime: true});
  assert.equal(health.status, "PASS", health.reason_codes.join(","));
  assert.equal(health.node.exact_match, true);
  assert.equal(health.repository_profile.verified, true);
  assert.equal(health.components.length, 14);
  assert.equal(health.components.every((component) => component.present && component.package_name), true);
  assert.equal(health.integrations.every((integration) => integration.present), true);
  assert.equal(health.authority_effect, "none");
  const replay = materializeProductClosure();
  assert.equal(health.source_closure.closure_digest, replay.closure_digest);
  assert.equal(replay.files.length > 100, true);
  assert.equal(replay.files.some((entry) => entry.path.includes("/evidence/")), false);
});
