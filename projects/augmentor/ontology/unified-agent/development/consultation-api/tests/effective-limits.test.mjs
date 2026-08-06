import assert from "node:assert/strict";
import test from "node:test";
import { effectiveLimits, estimateTokens, requestLifetime, TOKEN_ESTIMATOR } from "../src/effective-limits.mjs";

const limits = (value) => ({ maxCandidates: value, maxRecords: value, maxSources: value, maxBytes: value, maxTokens: value, maxMillis: value });

test("effective caps are minimums before reads", () => {
  assert.deepEqual(effectiveLimits({ service: limits(100), policy: limits(20), request: limits(50) }), limits(20));
  assert.throws(() => effectiveLimits({ service: limits(100), policy: limits(20), request: { ...limits(50), maxBytes: 0 } }), /invalid limit/);
});

test("request lifetime stops on cancellation or deadline", () => {
  assert.deepEqual(requestLifetime({ deadlineAt: "2026-08-03T00:00:01Z", now: Date.parse("2026-08-03T00:00:00Z") }), { active: true, remainingMillis: 1000 });
  assert.deepEqual(requestLifetime({ deadlineAt: "2026-08-03T00:00:01Z", cancelled: true }), { active: false, reasonCode: "CANCELLED" });
  assert.deepEqual(requestLifetime({ deadlineAt: "2026-08-03T00:00:00Z", now: Date.parse("2026-08-03T00:00:00Z") }), { active: false, reasonCode: "DEADLINE_REACHED" });
});

test("token estimate names a stable algorithm", () => {
  assert.deepEqual(TOKEN_ESTIMATOR, { id: "utf8-bytes-div-4", version: "1.0.0" });
  assert.equal(estimateTokens("12345"), 2);
});
