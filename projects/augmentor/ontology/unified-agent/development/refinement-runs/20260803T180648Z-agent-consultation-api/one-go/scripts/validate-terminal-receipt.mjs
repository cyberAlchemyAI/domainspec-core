import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";

const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const arg = (name) => { const index = process.argv.indexOf(name); return index >= 0 ? process.argv[index + 1] : null; };
const receiptPath = arg("--receipt");
const expectedUnit = arg("--unit");
const expectedSuccessorRaw = arg("--successor");
const expectedSuccessor = expectedSuccessorRaw === "__complete__" ? null : expectedSuccessorRaw;
const workPackPath = arg("--work-pack") ?? "projects/augmentor/ontology/unified-agent/development/refinement-runs/20260803T180648Z-agent-consultation-api/WORK-PACK.md";
if (!receiptPath || !expectedUnit || expectedSuccessorRaw === null) throw new Error("--receipt, --unit, and --successor are required");
const receipt = JSON.parse(await readFile(receiptPath, "utf8"));
const workPackBytes = await readFile(workPackPath);
const errors = [];
if (receipt.unit_id !== expectedUnit) errors.push("unit mismatch");
if (receipt.step_id !== `l0-${expectedUnit.slice(-3)}`) errors.push("step mismatch");
if (receipt.work_pack_sha256 !== sha(workPackBytes)) errors.push("work-pack digest mismatch");
if (receipt.successor !== expectedSuccessor) errors.push("successor mismatch");
if (receipt.status === "pass" && (receipt.validation_result !== "pass" || receipt.blockers.length || !receipt.artifacts.length || !receipt.validation.length)) errors.push("pass semantics are incomplete");
for (const key of ["task_session_terminal_ref", "closeout_owner_ref", "router_verification_ref"]) {
  const ref = receipt[key];
  if (!ref?.path || !/^[a-f0-9]{64}$/.test(ref.sha256)) errors.push(`${key} missing`);
  else {
    try { const bytes = await readFile(path.resolve(ref.path)); if (sha(bytes) !== ref.sha256) errors.push(`${key} digest mismatch`); }
    catch { errors.push(`${key} unavailable`); }
  }
}
console.log(JSON.stringify({ status: errors.length ? "block" : "pass", unit_id: expectedUnit, errors }, null, 2));
if (errors.length) process.exitCode = 1;
