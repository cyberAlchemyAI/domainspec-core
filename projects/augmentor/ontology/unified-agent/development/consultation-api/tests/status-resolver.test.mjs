import assert from "node:assert/strict";
import test from "node:test";
import { resolveStatus, STATUS_PRECEDENCE } from "../src/status-resolver.mjs";

test("status precedence is deterministic", () => {
  assert.deepEqual(STATUS_PRECEDENCE, ["denied", "invalid_request", "temporary_failure", "stale", "conflict", "budget_exceeded", "insufficient_evidence", "no_match", "partial"]);
  assert.equal(resolveStatus({ denied: true, conflict: true }), "denied");
  assert.equal(resolveStatus({ conflict: true, partial: true }), "conflict");
  assert.equal(resolveStatus({ partial: true }), "partial");
  assert.equal(resolveStatus({}), "ok");
});
