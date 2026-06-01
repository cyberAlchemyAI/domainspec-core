import { mkdtemp, rm } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { buildLocalProjection } from "../src/read-model/projection.mjs";
import { evaluateGateCascade } from "../src/read-model/gates.mjs";
import { handleCommand } from "../src/read-model/commands.mjs";

const baseData = (await buildLocalProjection({ eventLogPath: null })).ui;

function assert(condition, message) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

// 1. Judge stale in base mock data
assert(baseData.judge.score_state === "STALE", "Judge should be STALE in base data");

// 2. Scribe locked when gates fail closed
assert(baseData.cycle.scribe_access === "LOCKED", "Scribe should be locked in base data");

// 3. Unknown gate fails closed when RFA is missing
const unknownGateStress = JSON.parse(JSON.stringify(baseData));
unknownGateStress.opportunity.ingested_nofo_hash = "";
unknownGateStress.opportunity.nofo_url = "";
unknownGateStress.source_documents = [];
const unknownGateProjection = evaluateGateCascade(unknownGateStress);
assert(unknownGateProjection.gates[0].verdict === "FAIL_CLOSED", "E-101 must fail closed if RFA is missing");

// 4. Failed hard gate halts cascade
const haltedCascadeStress = JSON.parse(JSON.stringify(baseData));
const haltedCascade = evaluateGateCascade(haltedCascadeStress);
const e103 = haltedCascade.gates.find((gate) => gate.gate_id === "E-103");
assert(e103.verdict === "UNTESTED_DUE_TO_BLOCK", "Subsequent gates must show UNTESTED_DUE_TO_BLOCK");

// 5. Verify no candidate elevates to VERIFIED_FIT without live verification event
assert(
  baseData.scout_pipeline.every((candidate) => candidate.source_backing_tier !== "VERIFIED_FIT"),
  "Staging candidates must not emit VERIFIED_FIT without a live verification event"
);

const overrideStressDir = await mkdtemp(join(tmpdir(), "tilth-ui-stress-"));
try {
  // 6. Signed override unlocks Scribe but leaves gates as FAIL_CLOSED
  const eventLogPath = join(overrideStressDir, "events.jsonl");
  const signedOverride = await handleCommand({
    command_type: "OVERRIDE_SIGNED_PLACEHOLDER",
    payload: {
      cycle_id: baseData.cycle.cycle_id,
      gate_ids: ["E-102"],
      rationale: "Deadline risk accepted for stress test.",
      risk_acknowledged: true,
    },
  }, {
    eventLogPath,
    clock: () => "2026-05-22T10:00:00.000Z",
  });
  const e102AfterOverride = signedOverride.projection.GateProjection.gates.find((gate) => gate.gate_id === "E-102");
  assert(e102AfterOverride.verdict === "FAIL_CLOSED", "Signed override must not convert gate verdict to PASS");
  assert(signedOverride.ui.cycle.scribe_access === "RISK_UNLOCKED", "Signed override must set Scribe to RISK_UNLOCKED");

  // 7. Posture changed mid-cycle fails closed P-501
  const postureFailStress = JSON.parse(JSON.stringify(baseData));
  postureFailStress.evidence_items.push({
    evidence_id: "ev_sam_active_posture_stress",
    title: "Active SAM evidence",
    filename: "sam-active.pdf",
    classification: "SENSITIVE_INTERNAL",
    evidence_kind: "SAM_UEI_ACTIVE",
    commit_state: "COMMITTED",
    hash: "sha256-sam-active-posture-stress",
    linked_claims: [],
  });
  postureFailStress.budget.requested_total = 30000;
  postureFailStress.budget.max_request = 30000;
  postureFailStress.draft_sections.forEach((section) => {
    section.evidence_links = [];
  });
  postureFailStress.quarantine_items = [];
  postureFailStress.posture.changed_mid_cycle = true;

  const postureFailGate = evaluateGateCascade(postureFailStress).gates.find((gate) => gate.gate_id === "P-501");
  assert(postureFailGate.verdict === "FAIL_CLOSED", `Posture change mid-cycle must fail closed P-501, got ${postureFailGate.verdict}`);

  // 8. Command posture changed stales judge
  const postureEventLogPath = join(overrideStressDir, "posture-events.jsonl");
  const postureChanged = await handleCommand({
    command_type: "POSTURE_CHANGED",
    payload: {
      cycle_id: baseData.cycle.cycle_id,
      mode: "LOCAL_ONLY_SOVEREIGN",
    },
  }, { eventLogPath: postureEventLogPath, clock: () => "2026-05-22T10:03:00.000Z" });
  assert(postureChanged.ui.judge.score_state === "STALE", "Posture change command must stale judge");

  // 9. Scribe run rejected and fail-closed when gates are blocked
  const seatRejected = await handleCommand({
    command_type: "SCRIBE_RUN_REQUESTED",
    payload: {
      cycle_id: baseData.cycle.cycle_id,
      section_id: "sec_project_narrative",
    },
  }, {
    eventLogPath: join(overrideStressDir, "seat-events.jsonl"),
    clock: () => "2026-05-22T10:04:00.000Z",
  });
  assert(seatRejected.command_result === "REJECTED_FAIL_CLOSED", "Guarded scribe run must reject fail-closed");

  // 10. Scout verify without allow_network fails closed
  const verifyFailed = await handleCommand({
    command_type: "SCOUT_VERIFY_REQUESTED",
    payload: {
      cycle_id: baseData.cycle.cycle_id,
      candidate_id: baseData.scout_pipeline[0].program_id,
    },
  }, {
    eventLogPath: join(overrideStressDir, "verify-events.jsonl"),
    clock: () => "2026-05-22T10:05:00.000Z",
  });
  assert(verifyFailed.command_result === "VERIFICATION_FAILED", "Scout verify without allow_network must fail closed");

  // 11. REGRESSION: Local-Only / Sovereign posture strictly blocks network fetch (VULN-01)
  const localSovereignLogPath = join(overrideStressDir, "sovereign-events.jsonl");
  // Set posture to Local-Only / Sovereign
  await handleCommand({
    command_type: "POSTURE_CHANGED",
    payload: {
      cycle_id: baseData.cycle.cycle_id,
      mode: "Local-Only / Sovereign",
    },
  }, { eventLogPath: localSovereignLogPath });

  // Attempt verification with allow_network: true
  const sovereignVerify = await handleCommand({
    command_type: "SCOUT_VERIFY_REQUESTED",
    payload: {
      cycle_id: baseData.cycle.cycle_id,
      candidate_id: baseData.scout_pipeline[0].program_id,
      source_url: "https://example.invalid/nofo.pdf",
      allow_network: true,
    },
  }, { eventLogPath: localSovereignLogPath });

  assert(sovereignVerify.command_result === "VERIFICATION_FAILED", "Verify must fail when local-only posture blocks network fetch");
  const failedEvent = sovereignVerify.events.find((e) => e.event_type === "scout.verification_failed");
  assert(failedEvent, "Verification failed event must be emitted");
  assert(failedEvent.payload.reason === "SOVEREIGNTY_LEVEL_BLOCKED_NETWORK_FETCH", `Expected SOVEREIGNTY_LEVEL_BLOCKED_NETWORK_FETCH reason, got ${failedEvent.payload.reason}`);
  assert(failedEvent.payload.retry_state === "BLOCKED_BY_LOCAL_ONLY_POSTURE", `Expected BLOCKED_BY_LOCAL_ONLY_POSTURE retry_state, got ${failedEvent.payload.retry_state}`);

} finally {
  await rm(overrideStressDir, { recursive: true, force: true });
}

console.log("Fail-closed stress checks passed: read-model gates, quarantine, Scout verify, overrides, posture changes, and Local-Only fetch blocks.");
