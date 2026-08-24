import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const ONE_GO = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const REPO = path.resolve(ONE_GO, "../../../../../../../..");
const GATE = path.join(ONE_GO, "scripts/run-transition-gate.mjs");
const WORK_PACK = path.resolve(ONE_GO, "../WORK-PACK.md");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const rel = (absolute) => path.relative(REPO, absolute).replaceAll(path.sep, "/");
const writeJson = async (target, value) => {
  const bytes = Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
  await writeFile(target, bytes);
  return bytes;
};
const legacyRef = (target, bytes) => ({ path: rel(target), sha256: sha(bytes) });
const exactRef = (target, bytes) => ({ ...legacyRef(target, bytes), size_bytes: bytes.length });

test("transition gate admits exact joined receipts and blocks drift", async () => {
  const fixture = await mkdtemp(path.join(ONE_GO, ".transition-gate-test-"));
  try {
    await mkdir(fixture, { recursive: true });
    const taskPath = path.join(fixture, "task-session.json");
    const ownerPath = path.join(fixture, "owner.json");
    const routerPath = path.join(fixture, "router.json");
    const receiptPath = path.join(fixture, "normalized.json");
    const transitionPath = path.join(fixture, "transition.json");
    const [taskBytes, ownerBytes, routerBytes, workPackBytes] = await Promise.all([
      writeJson(taskPath, { status: "PASS" }),
      writeJson(ownerPath, { status: "PASS", owner: "invoke-refresh" }),
      writeJson(routerPath, { status: "verified", successor: "SWU-ACAPI-001" }),
      readFile(WORK_PACK)
    ]);
    const receipt = {
      schema_version: "augmentor.consultation.chain-terminal-receipt@0.1.0",
      unit_id: "SWU-ACAPI-000",
      step_id: "l0-000",
      status: "pass",
      work_pack_sha256: sha(workPackBytes),
      artifacts: [{ path: "synthetic-output", sha256: "0".repeat(64) }],
      validation: [{ argv: ["node", "synthetic-check.mjs"], exit_code: 0 }],
      validation_result: "pass",
      blockers: [],
      task_session_terminal_ref: legacyRef(taskPath, taskBytes),
      closeout_owner_ref: legacyRef(ownerPath, ownerBytes),
      router_verification_ref: legacyRef(routerPath, routerBytes),
      continuity_cursor: "cursor-l0-000",
      successor: "SWU-ACAPI-001"
    };
    const receiptBytes = await writeJson(receiptPath, receipt);
    const transition = {
      schema_version: "1.0.0",
      chain_id: "augmentor-consultation-l0",
      transition_id: "transition-l0-000",
      transition_digest: null,
      previous_transition_digest: null,
      epoch_id: `epoch-${"0".repeat(24)}`,
      cursor: "cursor-l0-000",
      selector: "SWU-ACAPI-000",
      request_ordinal: 1,
      risk_class: "bounded-write",
      task_session_result: "PASS",
      task_session_flags: [],
      terminal_receipt_ref: exactRef(receiptPath, receiptBytes),
      closeout: {
        result: "PASS",
        owner_receipt_ref: exactRef(ownerPath, ownerBytes),
        no_op_proof: null,
        continuation_router_verification_receipt_ref: exactRef(routerPath, routerBytes)
      },
      successor: {
        unit_id: "SWU-ACAPI-001",
        candidate_count: 1,
        declared: true,
        dependency_ready: true,
        scope_digest: "0".repeat(64)
      },
      observed_frontier_digest: "0".repeat(64)
    };
    await writeJson(transitionPath, transition);

    const accepted = spawnSync(process.execPath, [GATE, "--config", WORK_PACK, "--transition", transitionPath, "--validate-only"], { cwd: REPO, encoding: "utf8" });
    assert.equal(accepted.status, 0, accepted.stdout || accepted.stderr);
    assert.equal(JSON.parse(accepted.stdout).terminal_code, "TRANSITION_RECEIPTS_JOINED");

    await writeJson(ownerPath, { status: "tampered" });
    const blocked = spawnSync(process.execPath, [GATE, "--config", WORK_PACK, "--transition", transitionPath, "--validate-only"], { cwd: REPO, encoding: "utf8" });
    assert.equal(blocked.status, 2, blocked.stdout || blocked.stderr);
    assert.equal(JSON.parse(blocked.stdout).terminal_code, "TRANSITION_RECEIPT_JOIN_INVALID");
  } finally {
    await rm(fixture, { recursive: true, force: true });
  }
});
