import assert from "node:assert/strict";
import test from "node:test";
import { loadFixtureBoundary } from "../src/consultation-boundary.mjs";

const limits = { maxCandidates: 100, maxRecords: 20, maxSources: 20, maxBytes: 65536, maxTokens: 8192, maxMillis: 1000 };
const query = (overrides = {}) => ({ schemaVersion: "augmentor.consultation.query@0.1.0", requestId: "r", questionId: "q", operation: "search", query: { text: "session router" }, scope: { viewIds: ["runtime"] }, limits, ...overrides });
const context = (digest, overrides = {}) => ({ principal: { opaquePrincipalRef: "principal-1", audience: "augmentor-consultation" }, policy: { digest: "policy-1", projectionDigest: digest, allowedViews: ["runtime", "knowledge"], limits }, deadlineAt: "2030-01-01T00:00:00Z", projectionAgeSeconds: 0, now: Date.parse("2026-08-03T00:00:00Z"), ...overrides });

test("consultation returns typed source-bound evidence", async () => {
  const boundary = await loadFixtureBoundary(limits);
  const result = boundary.consult(query(), context(boundary.manifest.outputDigest));
  assert.equal(result.status, "ok");
  assert.ok(result.result.statements.length > 0);
  assert.ok(result.result.statements.every((statement) => statement.sourceHandles.length && statement.claimCeiling));
});

test("verified identity is out of band and denial is minimal", async () => {
  const boundary = await loadFixtureBoundary(limits);
  const result = boundary.consult(query(), null);
  assert.deepEqual(Object.keys(result).sort(), ["questionId", "reasonCode", "requestId", "retryable", "schemaVersion", "status"]);
  assert.equal(result.status, "denied");
});

test("forbidden operations and unknown fields fail closed", async () => {
  const boundary = await loadFixtureBoundary(limits);
  const bad = query({ operation: "write", principal: { token: "x" } });
  assert.equal(boundary.consult(bad, context(boundary.manifest.outputDigest)).status, "invalid_request");
});
