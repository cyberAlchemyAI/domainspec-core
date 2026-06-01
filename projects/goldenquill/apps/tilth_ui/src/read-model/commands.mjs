import { createHash } from "node:crypto";
import { appendJsonl, readJsonl, sha256Json } from "./events.mjs";
import { DEFAULT_EVENT_LOG_PATH, buildLocalProjection } from "./projection.mjs";
import { runScoutDiscovery } from "../openclaw.mjs";

const COMMAND_EVENT_TYPES = {
  SOURCE_DOCUMENT_REGISTERED: "source.document.registered",
  EVIDENCE_INTAKE_STARTED: "evidence.intake.started",
  CLASSIFICATION_REQUIRED: "evidence.classification.required",
  ONTOLOGY_CONFLICT_DETECTED: "evidence.ontology_conflict.detected",
  EVIDENCE_QUARANTINED: "evidence.quarantined",
  EVIDENCE_COMMITTED: "evidence.committed",
  GATE_CASCADE_STARTED: "gate.cascade.started",
  GATE_PASS: "gate.pass",
  GATE_FAIL_CLOSED: "gate.fail_closed",
  GATE_CASCADE_ABORTED: "gate.cascade_aborted",
  OVERRIDE_REQUESTED: "override.requested",
  OVERRIDE_SIGNED_PLACEHOLDER: "override.signed_placeholder",
  AUDIT_EVENT_APPENDED: "audit.event.appended",
  SCOUT_VERIFY_REQUESTED: "scout.verify.requested",
  BUDGET_UPDATED: "budget.updated",
  POSTURE_CHANGED: "posture.changed",
  SCRIBE_RUN_REQUESTED: "seat.scribe.requested",
  JUDGE_PANEL_RUN_REQUESTED: "seat.judge.requested",
  RED_TEAM_PROBE_RUN_REQUESTED: "seat.red_team.requested",
  SCOUT_DISCOVERY_REQUESTED: "scout.discovery.requested",
};

function normalizeCommandType(type) {
  return String(type || "")
    .trim()
    .replace(/[-.\s]+/g, "_")
    .toUpperCase();
}

function required(payload, fields) {
  return fields.filter((field) => payload[field] === undefined || payload[field] === null || payload[field] === "");
}

function validateCommand(commandType, payload) {
  const commonCycleRequired = !["AUDIT_EVENT_APPENDED"].includes(commandType);
  if (commonCycleRequired && !payload.cycle_id) return "cycle_id is required.";

  const missingByCommand = {
    SOURCE_DOCUMENT_REGISTERED: ["hash"],
    EVIDENCE_INTAKE_STARTED: ["evidence_id", "filename"],
    CLASSIFICATION_REQUIRED: ["evidence_id"],
    ONTOLOGY_CONFLICT_DETECTED: ["evidence_id", "description"],
    EVIDENCE_QUARANTINED: ["evidence_id", "reason"],
    EVIDENCE_COMMITTED: ["evidence_id", "classification", "hash"],
    GATE_PASS: ["gate_id", "evidence_ref"],
    GATE_FAIL_CLOSED: ["gate_id", "reason"],
    GATE_CASCADE_ABORTED: ["reason"],
    OVERRIDE_REQUESTED: ["gate_ids", "rationale"],
    OVERRIDE_SIGNED_PLACEHOLDER: ["gate_ids", "rationale", "risk_acknowledged"],
    AUDIT_EVENT_APPENDED: ["audit_event"],
    SCOUT_VERIFY_REQUESTED: ["candidate_id"],
    BUDGET_UPDATED: ["budget"],
    POSTURE_CHANGED: ["mode"],
    SCOUT_DISCOVERY_REQUESTED: ["context"],
  }[commandType] || [];
  const missing = required(payload, missingByCommand);
  if (missing.length) return `${missing.join(", ")} required for ${commandType}.`;

  if (commandType === "EVIDENCE_COMMITTED" && payload.classification === "CLASSIFICATION_REQUIRED") {
    return "Evidence cannot be committed with CLASSIFICATION_REQUIRED classification.";
  }
  if (commandType === "SCOUT_DISCOVERY_REQUESTED") {
    if (!payload.context || !payload.context.org_slug) {
      return "context.org_slug required for SCOUT_DISCOVERY_REQUESTED.";
    }
  }
  if (commandType === "OVERRIDE_SIGNED_PLACEHOLDER" && payload.risk_acknowledged !== true) {
    return "risk_acknowledged must be true before a placeholder override signature is accepted.";
  }
  if (commandType === "POSTURE_CHANGED") {
    const allowed = new Set(["FRONTIER_ELIGIBLE", "SPLIT_CONTEXT_HYBRID", "LOCAL_ONLY_SOVEREIGN", "Frontier-Eligible", "Split-Context Hybrid", "Local-Only / Sovereign"]);
    if (!allowed.has(payload.mode)) return "mode must use the three-posture vocabulary.";
  }
  return "";
}

async function nextEventIndex(eventLogPath) {
  return (await readJsonl(eventLogPath)).length + 1;
}

function makeEvent({ index, event_type, command_type, payload, actor = "LOCAL_COMMAND_HANDLER", timestamp, posture }) {
  const event = {
    event_id: `evt_local_${String(index).padStart(4, "0")}`,
    event_type,
    command_type,
    timestamp,
    actor,
    cycle_id: payload.cycle_id,
    payload,
    signature_status: payload.signature_status || "VERIFIED",
    posture: posture || payload.posture || "SPLIT_CONTEXT_HYBRID",
  };
  event.artifact_hash = sha256Json({
    event_id: event.event_id,
    event_type: event.event_type,
    command_type: event.command_type,
    timestamp: event.timestamp,
    actor: event.actor,
    cycle_id: event.cycle_id,
    payload: event.payload,
  });
  return event;
}

async function appendEvents(eventLogPath, events) {
  for (const event of events) {
    await appendJsonl(eventLogPath, event);
  }
}

async function scoutVerifyEvents({ payload, baseIndex, timestamp, posture }) {
  const requested = makeEvent({
    index: baseIndex,
    event_type: "scout.verify.requested",
    command_type: "SCOUT_VERIFY_REQUESTED",
    payload,
    timestamp,
    posture,
  });

  const cleanPosture = String(posture || "").trim().toUpperCase().replace(/[^A-Z0-9]+/g, "_");
  if (cleanPosture === "LOCAL_ONLY_SOVEREIGN" || cleanPosture === "LOCAL_ONLY") {
    return [
      requested,
      makeEvent({
        index: baseIndex + 1,
        event_type: "scout.verification_failed",
        command_type: "SCOUT_VERIFY_REQUESTED",
        payload: {
          ...payload,
          reason: "SOVEREIGNTY_LEVEL_BLOCKED_NETWORK_FETCH",
          retry_state: "BLOCKED_BY_LOCAL_ONLY_POSTURE",
        },
        timestamp,
        posture,
      }),
    ];
  }

  if (!payload.allow_network) {
    return [
      requested,
      makeEvent({
        index: baseIndex + 1,
        event_type: "scout.verification_failed",
        command_type: "SCOUT_VERIFY_REQUESTED",
        payload: {
          ...payload,
          reason: "LIVE_FETCH_NOT_ENABLED",
          retry_state: "OPERATOR_CAN_RETRY_WITH_ALLOW_NETWORK",
        },
        timestamp,
        posture,
      }),
    ];
  }

  if (!payload.source_url) {
    return [
      requested,
      makeEvent({
        index: baseIndex + 1,
        event_type: "scout.verification_failed",
        command_type: "SCOUT_VERIFY_REQUESTED",
        payload: {
          ...payload,
          reason: "SOURCE_URL_MISSING",
          retry_state: "REGISTER_SOURCE_URL",
        },
        timestamp,
        posture,
      }),
    ];
  }

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8_000);
    const response = await fetch(payload.source_url, { signal: controller.signal });
    clearTimeout(timeout);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const body = await response.text();
    const content_hash = `sha256-${createHash("sha256").update(body).digest("hex")}`;
    return [
      requested,
      makeEvent({
        index: baseIndex + 1,
        event_type: "scout.live_fetch.verified",
        command_type: "SCOUT_VERIFY_REQUESTED",
        payload: {
          ...payload,
          fetched_at: timestamp,
          content_hash,
          fit_state: "LIVE_SOURCE_VERIFIED",
          verification_note: "Live source fetched and hashed. Semantic fit elevation requires a separate verifier; caller-supplied VERIFIED_FIT is ignored.",
        },
        timestamp,
        posture,
      }),
    ];
  } catch (err) {
    return [
      requested,
      makeEvent({
        index: baseIndex + 1,
        event_type: "scout.verification_failed",
        command_type: "SCOUT_VERIFY_REQUESTED",
        payload: {
          ...payload,
          reason: `LIVE_FETCH_FAILED: ${err.message}`,
          retry_state: "RETRYABLE",
        },
        timestamp,
        posture,
      }),
    ];
  }
}

function seatGuardFailure(seat, projection) {
  const gates = projection.projections.GateProjection.gates;
  const failedGate = gates.find((gate) => gate.verdict === "FAIL_CLOSED");
  const untested = gates.find((gate) => gate.verdict === "UNTESTED_DUE_TO_BLOCK");
  if (seat === "scribe") {
    if (failedGate) return `Scribe blocked by ${failedGate.gate_id}; Logician gate is ${failedGate.verdict}.`;
    if (projection.ui.evidence_projection.unavailable_evidence_ids.length) return "Scribe blocked because quarantined evidence is present.";
  }
  if (seat === "judge") {
    if (failedGate || untested) return "Judge panel cannot run until gate cascade is clear and current.";
    if (projection.ui.judge?.score_state === "STALE") return "Judge panel is stale and requires a clean draft/evidence envelope.";
  }
  if (seat === "red_team") {
    if (failedGate || untested) return "Red Team probe cannot run until Scribe/Judge prerequisites are current.";
    if (projection.ui.judge?.score_state !== "READY") return "Red Team requires a current Judge panel envelope.";
  }
  return "";
}

async function seatStubEvents({ commandType, payload, baseIndex, timestamp, posture, projection }) {
  const seat = commandType === "SCRIBE_RUN_REQUESTED" ? "scribe" : commandType === "JUDGE_PANEL_RUN_REQUESTED" ? "judge" : "red_team";
  const reason = seatGuardFailure(seat, projection) || "Runner contract exists, but this local UI pass only prepares guarded command envelopes.";
  return [
    makeEvent({
      index: baseIndex,
      event_type: `seat.${seat}.requested`,
      command_type: commandType,
      payload: {
        ...payload,
        seat,
        model_binding_ref: `/router.yaml#tilth.${seat === "red_team" ? "red_team" : seat}`,
      },
      timestamp,
      posture,
    }),
    makeEvent({
      index: baseIndex + 1,
      event_type: "seat.run.rejected",
      command_type: commandType,
      payload: {
        ...payload,
        seat,
        reason,
        result: "REJECTED_FAIL_CLOSED",
      },
      timestamp,
      posture,
    }),
  ];
}

async function gateCascadeEvents({ payload, baseIndex, timestamp, posture, projection }) {
  const events = [
    makeEvent({
      index: baseIndex,
      event_type: "gate.cascade.started",
      command_type: "GATE_CASCADE_STARTED",
      payload,
      timestamp,
      posture,
    }),
  ];
  let next = baseIndex + 1;
  for (const gate of projection.projections.GateProjection.gates) {
    if (gate.verdict === "PASS") {
      events.push(makeEvent({
        index: next,
        event_type: "gate.pass",
        command_type: "GATE_CASCADE_STARTED",
        payload: { ...payload, gate_id: gate.gate_id, evidence_ref: gate.evidence_ref, rationale: gate.source_excerpt },
        timestamp,
        posture,
      }));
      next += 1;
    } else if (gate.verdict === "FAIL_CLOSED") {
      events.push(makeEvent({
        index: next,
        event_type: "gate.fail_closed",
        command_type: "GATE_CASCADE_STARTED",
        payload: { ...payload, gate_id: gate.gate_id, reason: gate.remediation || gate.source_excerpt, rationale: gate.source_excerpt },
        timestamp,
        posture,
      }));
      next += 1;
      events.push(makeEvent({
        index: next,
        event_type: "gate.cascade_aborted",
        command_type: "GATE_CASCADE_STARTED",
        payload: { ...payload, reason: `Cascade halted at ${gate.gate_id}. Remaining gates UNTESTED_DUE_TO_BLOCK.`, halted_at_gate_id: gate.gate_id },
        timestamp,
        posture,
      }));
      break;
    }
  }
  return events;
}

export async function handleCommand(input, options = {}) {
  const eventLogPath = options.eventLogPath || DEFAULT_EVENT_LOG_PATH;
  const clock = options.clock || (() => new Date().toISOString());
  const commandType = normalizeCommandType(input.command_type || input.type);
  const payload = input.payload || {};
  const event_type = COMMAND_EVENT_TYPES[commandType];

  if (!event_type) {
    return { status: "rejected", reason: `Unknown command_type: ${commandType || "(missing)"}` };
  }
  const validationError = validateCommand(commandType, payload);
  if (validationError) {
    return { status: "rejected", reason: validationError };
  }

  const projectionBefore = await buildLocalProjection({ ...options, eventLogPath });
  const timestamp = clock();
  const posture = projectionBefore.ui.posture?.mode || payload.posture;
  const baseIndex = await nextEventIndex(eventLogPath);
  let events;

  if (commandType === "SCOUT_VERIFY_REQUESTED") {
    events = await scoutVerifyEvents({ payload, baseIndex, timestamp, posture });
  } else if (commandType === "SCOUT_DISCOVERY_REQUESTED") {
    const scoutResult = await runScoutDiscovery({
      cycle_id: payload.cycle_id,
      query: payload.query || "",
      context: payload.context || {},
    });

    const requested = makeEvent({
      index: baseIndex,
      event_type: "scout.discovery.requested",
      command_type: commandType,
      payload,
      timestamp,
      posture,
    });

    const completed = makeEvent({
      index: baseIndex + 1,
      event_type: scoutResult.ok ? "scout.discovery.completed" : "scout.discovery.failed",
      command_type: commandType,
      payload: {
        ...payload,
        opportunities: scoutResult.opportunities,
        totals: scoutResult.totals,
        reason: scoutResult.reason,
      },
      timestamp,
      posture,
    });

    events = [requested, completed];
  } else if (["SCRIBE_RUN_REQUESTED", "JUDGE_PANEL_RUN_REQUESTED", "RED_TEAM_PROBE_RUN_REQUESTED"].includes(commandType)) {
    events = await seatStubEvents({ commandType, payload, baseIndex, timestamp, posture, projection: projectionBefore });
  } else if (commandType === "GATE_CASCADE_STARTED") {
    events = await gateCascadeEvents({ payload, baseIndex, timestamp, posture, projection: projectionBefore });
  } else {
    events = [makeEvent({ index: baseIndex, event_type, command_type: commandType, payload, timestamp, posture })];
  }

  await appendEvents(eventLogPath, events);
  const projection = await buildLocalProjection({ ...options, eventLogPath });
  const rejectedStub = events.find((event) => event.event_type === "seat.run.rejected");
  const failedVerification = events.find((event) => event.event_type === "scout.verification_failed");
  const failedDiscovery = events.find((event) => event.event_type === "scout.discovery.failed");

  return {
    status: "accepted",
    command_type: commandType,
    command_result: rejectedStub
      ? "REJECTED_FAIL_CLOSED"
      : failedVerification
        ? "VERIFICATION_FAILED"
        : failedDiscovery
          ? "DISCOVERY_FAILED"
          : "ACCEPTED",
    events,
    projection: projection.projections,
    ui: projection.ui,
  };
}

export { COMMAND_EVENT_TYPES };
