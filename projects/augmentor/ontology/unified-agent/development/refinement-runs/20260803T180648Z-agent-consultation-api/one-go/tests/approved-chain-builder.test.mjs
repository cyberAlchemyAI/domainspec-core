import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const ONE_GO = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const REPO = path.resolve(ONE_GO, "../../../../../../../..");
const BUILDER = path.join(ONE_GO, "scripts/build-approved-chain.mjs");
const MANIFEST = path.join(ONE_GO, "audit/results-v2-execution-ready/objective-execution-manifest.json");

test("approved chain config binds the exact epoch and rejects drift", async () => {
  const fixture = await mkdtemp(path.join(ONE_GO, ".approved-chain-test-"));
  try {
    await mkdir(fixture, { recursive: true });
    const manifest = JSON.parse(await readFile(MANIFEST, "utf8"));
    const epoch = manifest.epoch_binding;
    const approval = {
      schema_version: "augmentor.consultation.decision-gate-approval@0.1.0",
      decision_id: "augmentor-consultation-l0-exact-epoch",
      selected_option: "APPROVE_EXACT_EPOCH",
      approval_status: "approved",
      approval_owner: "human-decision-gate",
      source: "current-user-explicit-confirmation",
      approved_at: "2026-08-03T00:00:00Z",
      epoch_binding: {
        epoch_id: epoch.epoch_id,
        audit_projection_digest: epoch.audit_projection_digest,
        canonical_semantic_digest: epoch.canonical_semantic_digest,
        source_snapshot_digest: epoch.source_snapshot_digest,
        finite_frontier: epoch.approved_frontier_ref,
        run_budget: epoch.run_budget.max_task_session_requests,
        risk_ceiling: "bounded-write"
      },
      scope: "candidate-local Agent Consultation API L0 only",
      constraints: { stop_on_first_blocker: true, network: false, deployment: false, publication: false, authority_change: false, l1_or_later: false },
      authority_effect: "none"
    };
    const approvalPath = path.join(fixture, "approval.json");
    const outputPath = path.join(fixture, "chain.json");
    await writeFile(approvalPath, `${JSON.stringify(approval, null, 2)}\n`);
    const accepted = spawnSync(process.execPath, [BUILDER, "--approval-receipt", approvalPath, "--output", outputPath], { cwd: REPO, encoding: "utf8" });
    assert.equal(accepted.status, 0, accepted.stdout || accepted.stderr);
    assert.equal(JSON.parse(accepted.stdout).terminal_code, "APPROVED_CHAIN_CONFIG_READY");
    const chain = JSON.parse(await readFile(outputPath, "utf8"));
    assert.deepEqual(chain.finite_frontier, epoch.approved_frontier_ref);
    assert.equal(chain.approved_epoch.epoch_id, epoch.epoch_id);

    approval.epoch_binding.audit_projection_digest = "0".repeat(64);
    const driftPath = path.join(fixture, "approval-drift.json");
    await writeFile(driftPath, `${JSON.stringify(approval, null, 2)}\n`);
    const blocked = spawnSync(process.execPath, [BUILDER, "--approval-receipt", driftPath, "--output", path.join(fixture, "drift-chain.json")], { cwd: REPO, encoding: "utf8" });
    assert.equal(blocked.status, 2, blocked.stdout || blocked.stderr);
    assert.equal(JSON.parse(blocked.stdout).terminal_code, "APPROVED_CHAIN_CONFIG_INVALID");
  } finally {
    await rm(fixture, { recursive: true, force: true });
  }
});
