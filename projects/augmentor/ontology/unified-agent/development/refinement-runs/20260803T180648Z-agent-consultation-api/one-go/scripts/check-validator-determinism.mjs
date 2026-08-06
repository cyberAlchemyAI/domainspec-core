import { spawnSync } from "node:child_process";

const target = "projects/augmentor/ontology/unified-agent/scripts/validate.mjs";
let expected = null;
for (let index = 0; index < 12; index += 1) {
  const run = spawnSync(process.execPath, [target], { encoding: "utf8", timeout: 10000 });
  if (run.status !== 0) throw new Error(`validator run ${index + 1} failed: ${run.stdout}${run.stderr}`);
  const receipt = JSON.parse(run.stdout);
  const signature = JSON.stringify({ status: receipt.status, digests: receipt.digests, violations: receipt.violations });
  if (expected === null) expected = signature;
  if (signature !== expected) throw new Error(`validator run ${index + 1} changed output ordering or values`);
}
console.log("VALIDATOR_DETERMINISM=pass runs=12");
