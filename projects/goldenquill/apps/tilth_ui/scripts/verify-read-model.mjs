import { mkdtemp, readFile, rm } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { buildLocalProjection } from "../src/read-model/projection.mjs";
import { handleCommand } from "../src/read-model/commands.mjs";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function includes(label, text, needle) {
  if (!String(text).includes(needle)) throw new Error(`${label}: expected ${needle}`);
}

const clean = await buildLocalProjection({ eventLogPath: null });
assert(clean.projections.CycleProjection, "CycleProjection missing");
assert(clean.projections.ScoutProjection, "ScoutProjection missing");
assert(clean.projections.GateProjection, "GateProjection missing");
assert(clean.projections.EvidenceProjection, "EvidenceProjection missing");
assert(clean.projections.AuditProjection, "AuditProjection missing");
assert(clean.projections.ScoutProjection.counts.programs > 0, "ScoutProjection did not read SuperScout programs");
assert(clean.projections.ScoutProjection.counts.broken_url_queue > 0, "ScoutProjection did not read broken URL queue");
assert(clean.ui.scout_pipeline.every((candidate) => candidate.source_backing_tier !== "VERIFIED_FIT"), "Seed/staging must not emit VERIFIED_FIT without live verification");

// Note: app.mjs was retired in favor of serving direct Stitch HTML assets.
// Read-model projection checks follow.

const tempDir = await mkdtemp(join(tmpdir(), "tilth-ui-read-model-"));
try {
  const eventLogPath = join(tempDir, "events.jsonl");
  const rejected = await handleCommand({
    command_type: "EVIDENCE_COMMITTED",
    payload: {
      cycle_id: clean.ui.cycle.cycle_id,
      evidence_id: "ev_bad",
      classification: "CLASSIFICATION_REQUIRED",
      hash: "sha256-bad",
    },
  }, { eventLogPath });
  assert(rejected.status === "rejected", "invalid evidence commit must reject");

  const sourceRegistered = await handleCommand({
    command_type: "SOURCE_DOCUMENT_REGISTERED",
    payload: {
      cycle_id: clean.ui.cycle.cycle_id,
      source_document_id: "src_test_rfa",
      title: "Test NOFO",
      source_type: "RFA_NOFO",
      hash: "sha256-test-rfa",
      url: "https://example.invalid/nofo.pdf",
    },
  }, { eventLogPath, clock: () => "2026-05-22T09:00:00.000Z" });
  assert(sourceRegistered.status === "accepted", "source document command should append");
  assert(sourceRegistered.events.length === 1, "source document command should append one event");
  assert(sourceRegistered.ui.source_documents.some((doc) => doc.source_document_id === "src_test_rfa"), "source document missing from rebuilt projection");

  const cascade = await handleCommand({
    command_type: "GATE_CASCADE_STARTED",
    payload: { cycle_id: clean.ui.cycle.cycle_id, rationale: "verify read-model cascade" },
  }, { eventLogPath, clock: () => "2026-05-22T09:01:00.000Z" });
  assert(cascade.status === "accepted", "gate cascade command should append");
  includes("gate cascade", JSON.stringify(cascade.events), "gate.cascade_aborted");
  includes("gate cascade", JSON.stringify(cascade.projection.GateProjection.gates), "UNTESTED_DUE_TO_BLOCK");

  const scoutVerify = await handleCommand({
    command_type: "SCOUT_VERIFY_REQUESTED",
    payload: {
      cycle_id: clean.ui.cycle.cycle_id,
      candidate_id: clean.ui.scout_pipeline[0].program_id,
      source_url: clean.ui.scout_pipeline[0].source_url,
    },
  }, { eventLogPath, clock: () => "2026-05-22T09:02:00.000Z" });
  assert(scoutVerify.command_result === "VERIFICATION_FAILED", "Scout verify without allow_network should fail closed");
  assert(scoutVerify.projection.ScoutProjection.candidates.every((candidate) => candidate.source_backing_tier !== "VERIFIED_FIT"), "failed verification must not elevate to VERIFIED_FIT");

  const scribe = await handleCommand({
    command_type: "SCRIBE_RUN_REQUESTED",
    payload: {
      cycle_id: clean.ui.cycle.cycle_id,
      section_id: "sec_project_narrative",
    },
  }, { eventLogPath, clock: () => "2026-05-22T09:03:00.000Z" });
  assert(scribe.command_result === "REJECTED_FAIL_CLOSED", "Scribe command must fail closed while gates fail");
  includes("scribe audit", JSON.stringify(scribe.events), "seat.run.rejected");
} finally {
  await rm(tempDir, { recursive: true, force: true });
}

console.log("Read-model projection and command verification passed.");
