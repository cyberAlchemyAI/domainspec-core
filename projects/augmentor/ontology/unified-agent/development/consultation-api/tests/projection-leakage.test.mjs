import assert from "node:assert/strict";
import test from "node:test";
import { findLeakage } from "../scripts/validate-projection-leakage.mjs";

test("generated projection contains no blocked private fields or paths", async () => {
  assert.deepEqual(await findLeakage(), []);
});
