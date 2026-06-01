import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { join, resolve } from "node:path";
import { readJsonl, eventAuditRow } from "./events.mjs";
import { buildScoutProjection } from "./staging.mjs";
import { evaluateGateCascade, usableEvidenceItems } from "./gates.mjs";

const APP_ROOT = fileURLToPath(new URL("../../", import.meta.url));
const SEED_EVENTS_PATH = fileURLToPath(new URL("../data/events/seed-events.jsonl", import.meta.url));
const DEFAULT_EVENT_LOG_PATH = join(APP_ROOT, ".local", "events.jsonl");

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function nowIso() {
  return new Date().toISOString();
}

function pushUniqueById(items, idKey, nextItem) {
  const index = items.findIndex((item) => item[idKey] === nextItem[idKey]);
  if (index >= 0) {
    items[index] = { ...items[index], ...nextItem };
  } else {
    items.push(nextItem);
  }
}

function normalizePosture(mode) {
  const clean = String(mode || "").trim();
  const byValue = {
    "Frontier-Eligible": "FRONTIER_ELIGIBLE",
    "Split-Context Hybrid": "SPLIT_CONTEXT_HYBRID",
    "Local-Only / Sovereign": "LOCAL_ONLY_SOVEREIGN",
    frontier_eligible: "FRONTIER_ELIGIBLE",
    split_context_hybrid: "SPLIT_CONTEXT_HYBRID",
    local_only_sovereign: "LOCAL_ONLY_SOVEREIGN",
  };
  return byValue[clean] || clean.toUpperCase().replace(/[^A-Z0-9]+/g, "_");
}

async function loadFixtureFromSeedEvent(event) {
  const fixturePath = event.payload?.fixture_path || "../mock/DEMO_DATA.json";
  const resolved = resolve(join(APP_ROOT, "src/data/events"), fixturePath);
  return JSON.parse(await readFile(resolved, "utf8"));
}

function applyEvidenceEvent(data, event) {
  const payload = event.payload || {};
  data.evidence_items ||= [];
  const evidence_id = payload.evidence_id || `ev_${event.event_id}`;
  const base = {
    evidence_id,
    title: payload.title || payload.filename || evidence_id,
    filename: payload.filename || `${evidence_id}.unknown`,
    classification: payload.classification || "",
    commit_state: payload.commit_state || "PARSING",
    evidence_kind: payload.evidence_kind || payload.source_type || "",
    source_type: payload.source_type || "",
    hash: payload.hash || payload.content_hash || "",
    linked_claims: payload.linked_claims || [],
  };

  if (event.event_type === "evidence.intake.started") {
    pushUniqueById(data.evidence_items, "evidence_id", base);
  }

  if (event.event_type === "evidence.classification.required") {
    pushUniqueById(data.evidence_items, "evidence_id", {
      ...base,
      classification: "CLASSIFICATION_REQUIRED",
      commit_state: "CLASSIFICATION_REQUIRED",
    });
  }

  if (event.event_type === "evidence.ontology_conflict.detected") {
    pushUniqueById(data.evidence_items, "evidence_id", {
      ...base,
      classification: payload.classification || "ORG_CONTEXT",
      commit_state: "ONTOLOGY_CONFLICT",
      conflicts: payload.conflicts || [{
        conflict_id: payload.conflict_id || `conf_${event.event_id}`,
        description: payload.description || "Ontology conflict detected.",
        requires_operator_resolution: true,
      }],
    });
  }

  if (event.event_type === "evidence.quarantined") {
    pushUniqueById(data.evidence_items, "evidence_id", {
      ...base,
      commit_state: payload.commit_state || "ONTOLOGY_CONFLICT",
    });
    data.quarantine_items ||= [];
    pushUniqueById(data.quarantine_items, "quarantine_id", {
      quarantine_id: payload.quarantine_id || `qtn_${event.event_id}`,
      evidence_id,
      reason: payload.reason || "Evidence quarantined by command.",
      state: payload.state || "QUARANTINED",
      hash: payload.hash || payload.content_hash || base.hash,
      created_at: event.timestamp,
      auto_moved_at: payload.auto_moved_at || event.timestamp,
      operator_action_required: payload.operator_action_required ?? true,
      linked_cycle_id: payload.cycle_id || event.cycle_id || data.cycle?.cycle_id,
    });
  }

  if (event.event_type === "evidence.committed") {
    pushUniqueById(data.evidence_items, "evidence_id", {
      ...base,
      classification: payload.classification,
      commit_state: "COMMITTED",
      hash: payload.hash || payload.content_hash,
    });
  }
}

function applyEvent(data, event) {
  const payload = event.payload || {};
  if (event.event_type.startsWith("evidence.")) {
    applyEvidenceEvent(data, event);
  }

  if (event.event_type === "source.document.registered") {
    data.source_documents ||= [];
    pushUniqueById(data.source_documents, "source_document_id", {
      source_document_id: payload.source_document_id || `src_${event.event_id}`,
      cycle_id: payload.cycle_id || event.cycle_id || data.cycle?.cycle_id,
      source_type: payload.source_type || "RFA_NOFO",
      title: payload.title || "Registered source document",
      url: payload.url || payload.source_url || "",
      hash: payload.hash || payload.content_hash,
      registered_at: event.timestamp,
    });
    data.opportunity.nofo_url = payload.url || payload.source_url || data.opportunity.nofo_url;
    data.opportunity.ingested_nofo_hash = payload.hash || payload.content_hash || data.opportunity.ingested_nofo_hash;
  }

  if (event.event_type === "override.requested") {
    data.override = {
      ...(data.override || {}),
      state: "REQUESTED",
      requested_at: event.timestamp,
      rationale: payload.rationale,
      affected_gate_ids: payload.gate_ids || [],
    };
  }

  if (event.event_type === "override.signed_placeholder") {
    data.override = {
      ...(data.override || {}),
      state: "OVERRIDE_SIGNED",
      signed_at: event.timestamp,
      signature_status: "PLACEHOLDER_SIGNED",
      signature_event_id: event.event_id,
      affected_gate_ids: payload.gate_ids || data.override?.affected_gate_ids || [],
      rationale: payload.rationale || data.override?.rationale,
    };
  }

  if (event.event_type === "budget.updated") {
    data.budget = {
      ...(data.budget || {}),
      ...payload.budget,
    };
    data.judge = {
      ...(data.judge || {}),
      score_state: "STALE",
      stale_reason: "Budget changed after last Judge scoring pass.",
    };
  }

  if (event.event_type === "posture.changed") {
    data.posture = {
      ...(data.posture || {}),
      mode: normalizePosture(payload.mode),
      changed_mid_cycle: true,
      last_confirmed_at: event.timestamp,
      data_boundary_note: payload.data_boundary_note || "Posture changed mid-cycle; unsafe work must be revalidated.",
    };
    data.judge = {
      ...(data.judge || {}),
      score_state: "STALE",
      stale_reason: "Posture changed after last Judge scoring pass.",
    };
  }

  if (event.event_type === "audit.event.appended" && payload.audit_event) {
    data.audit_events ||= [];
    pushUniqueById(data.audit_events, "event_id", payload.audit_event);
  }
}

function appendAuditRows(data, events) {
  data.audit_events ||= [];
  for (const event of events) {
    if (event.event_type === "fixture.demo_data_loaded") continue;
    if (event.event_type === "audit.event.appended" && event.payload?.audit_event) continue;
    pushUniqueById(data.audit_events, "event_id", eventAuditRow(event));
  }
}

function applyDerivedState(data, gateProjection, scoutProjection, events) {
  data.logician_gates = gateProjection.gates;
  data.scout_pipeline = scoutProjection.candidates;
  data.scout_totals = scoutProjection.totals;
  data.scout_projection = scoutProjection;

  // Shape ui.scout for the Stitch Scout screen.
  //
  // Preference order:
  //   1. Latest scout.discovery.completed event payload (live Tilth/Scout
  //      output via runScoutDiscovery → openclaw agent --agent tilth).
  //   2. Staging-CSV-derived ScoutProjection (fallback when no discovery
  //      event exists yet, or when the latest discovery FAILED).
  //
  // The live-discovery payload is already shaped to the spec
  // (apps/tilth_ui/SCOUT_INTEGRATION_SPEC.md §2) by runScoutDiscovery, so
  // we surface it verbatim with default totals fill-in.
  const latestDiscovery = [...events].reverse().find(
    (event) => event.event_type === "scout.discovery.completed",
  );
  if (latestDiscovery && Array.isArray(latestDiscovery.payload?.opportunities)) {
    const defaultTotals = { value: 0, signals: 0, blocked_value: 0, tracked: 0, new_today: 0 };
    data.scout = {
      opportunities: latestDiscovery.payload.opportunities,
      totals: { ...defaultTotals, ...(latestDiscovery.payload.totals || {}) },
      source: "scout.discovery.completed",
      generated_at: latestDiscovery.timestamp,
    };
  } else {
  const scoutCandidates = scoutProjection.candidates || [];
  data.scout = {
    opportunities: scoutCandidates.map((candidate) => {
      const deadlineText = candidate.deadline || "";
      let urgency = "";
      let urgent = false;
      if (deadlineText) {
        const now = new Date();
        const deadline = new Date(deadlineText);
        if (!Number.isNaN(deadline.getTime())) {
          const diffDays = Math.round((deadline.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
          if (diffDays <= 14) {
            urgent = true;
            urgency = "🔴 < 14 days";
          } else if (diffDays <= 30) {
            urgency = "🟡 < 30 days";
          } else {
            urgency = "🟢 ≥ 30 days";
          }
        }
      }

      const backing = candidate.source_backing_tier || "STAGING_NEEDS_REVIEW";
      const confidence = backing === "VERIFIED_FIT" ? 96 : backing === "STAGING_SOURCE_QUALIFIED" ? 88 : 72;

      return {
        id: candidate.opportunity_id,
        program: candidate.title,
        agency: candidate.funder,
        level: "", // level not yet modeled in staging; left blank rather than fabricated
        who_applies: "", // kept empty until modeled in staging
        what_it_funds: candidate.topics || "", // rough proxy for subject
        award_size: candidate.estimated_value || 0,
        match: "", // not yet modeled
        deadline: deadlineText,
        urgency,
        url: candidate.source_url || "",
        amount: candidate.estimated_value || 0,
        urgent,
        confidence,
        backing,
        code: candidate.program_code,
        summary: candidate.next_action,
        rationale: candidate.value_basis,
        quote: candidate.source_backing_note,
      };
    }),
    totals: {
      value: scoutProjection.totals.total_tracked_value,
      signals: scoutProjection.totals.opportunities_found,
      blocked_value: scoutProjection.totals.blocked_value,
      tracked: scoutProjection.totals.opportunities_tracking,
      new_today: scoutProjection.totals.opportunities_added,
    },
    source: "staging_csv_projection",
  };
  }

  const firstCandidate = scoutProjection.candidates[0];
  if (firstCandidate) {
    data.opportunity = {
      ...(data.opportunity || {}),
      opportunity_id: firstCandidate.opportunity_id,
      title: firstCandidate.title,
      funder: firstCandidate.funder,
      program_code: firstCandidate.program_code,
      deadline: firstCandidate.deadline || data.opportunity?.deadline,
      nofo_url: firstCandidate.source_url || data.opportunity?.nofo_url,
      source_backing_tier: firstCandidate.source_backing_tier,
      verification_state: firstCandidate.verification_state,
      rationale: `${firstCandidate.source_backing_tier}: ${firstCandidate.next_action}`,
      evidence_gaps: [
        "Live source fetch before VERIFIED_FIT elevation",
        "Active SAM.gov/UEI evidence",
        "Committed source-classified evidence for claims",
      ],
    };
  }

  const hardFailed = gateProjection.hard_gate_failed;
  const overrideSigned = data.override?.state === "OVERRIDE_SIGNED" || data.override?.state === "FORCED_OVERRIDE_SIGNED";
  data.cycle = {
    ...(data.cycle || {}),
    status: hardFailed ? (overrideSigned ? "SCRIBE_UNLOCKED_WITH_RISK" : "GATE_FAILED_CLOSED") : "GATE_PASSED",
    scribe_access: hardFailed ? (overrideSigned ? "RISK_UNLOCKED" : "LOCKED") : "UNLOCKABLE",
    updated_at: events.at(-1)?.timestamp || data.cycle?.updated_at || nowIso(),
  };

  const failedGate = gateProjection.gates.find((gate) => gate.verdict === "FAIL_CLOSED");
  for (const section of data.draft_sections || []) {
    if (failedGate && !overrideSigned && section.lease_state?.status === "LOCKED_BY_GATE") {
      section.lease_state.locked_by_gate_id = failedGate.gate_id;
      section.eligibility_risk_mark = false;
    }
    if (failedGate && overrideSigned) {
      section.eligibility_risk_mark = true;
      if (section.lease_state?.status === "LOCKED_BY_GATE") {
        section.lease_state.status = "RISK_UNLOCKED";
        section.lease_state.locked_by_gate_id = failedGate.gate_id;
      }
    }
  }

  const usableIds = new Set(usableEvidenceItems(data).map((item) => item.evidence_id));
  data.evidence_projection = {
    projection_type: "EvidenceProjection",
    cycle_id: data.cycle?.cycle_id,
    committed_count: usableIds.size,
    quarantined_count: (data.quarantine_items || []).length,
    usable_evidence_ids: [...usableIds],
    unavailable_evidence_ids: (data.quarantine_items || []).map((item) => item.evidence_id),
  };

  const auditEvents = data.audit_events || [];
  const lastAudit = auditEvents.at(-1);
  data.audit_state = {
    ...(data.audit_state || {}),
    last_event: lastAudit?.event_type || data.audit_state?.last_event,
    last_verified_event_id: lastAudit?.event_id || data.audit_state?.last_verified_event_id,
    lock_history_count: auditEvents.length,
    unsigned_change_count: auditEvents.filter((event) => event.signature_status !== "VERIFIED").length,
  };
  if (!data.audit_state.signature_status) data.audit_state.signature_status = "UNSIGNED_CHANGES_PENDING";

  data.projections = {
    CycleProjection: {
      projection_type: "CycleProjection",
      cycle_id: data.cycle?.cycle_id,
      status: data.cycle?.status,
      scribe_access: data.cycle?.scribe_access,
      posture: data.posture?.mode,
      source: "append_only_jsonl_plus_staging_adapter",
    },
    ScoutProjection: scoutProjection,
    GateProjection: gateProjection,
    EvidenceProjection: data.evidence_projection,
    AuditProjection: {
      projection_type: "AuditProjection",
      last_event: data.audit_state.last_event,
      last_verified_event_id: data.audit_state.last_verified_event_id,
      event_count: auditEvents.length,
      local_event_count: events.filter((event) => event.event_type !== "fixture.demo_data_loaded").length,
    },
  };
  data.meta = {
    ...(data.meta || {}),
    projection_source: "local_read_model",
    projection_generated_at: nowIso(),
    runtime_seed_fixture: "src/data/events/seed-events.jsonl",
  };
  return data;
}

export async function readProjectionEvents({ seedEventsPath = SEED_EVENTS_PATH, eventLogPath = DEFAULT_EVENT_LOG_PATH } = {}) {
  const seedEvents = await readJsonl(seedEventsPath);
  const localEvents = await readJsonl(eventLogPath);
  return [...seedEvents, ...localEvents];
}

export async function buildLocalProjection(options = {}) {
  const events = await readProjectionEvents(options);
  let data = null;
  for (const event of events) {
    if (event.event_type === "fixture.demo_data_loaded") {
      data = await loadFixtureFromSeedEvent(event);
      break;
    }
  }
  if (!data) throw new Error("No fixture.demo_data_loaded seed event found.");
  data = clone(data);

  const localEvents = events.filter((event) => event.event_type !== "fixture.demo_data_loaded");
  for (const event of localEvents) {
    applyEvent(data, event);
  }
  appendAuditRows(data, localEvents);

  const liveVerificationEvents = localEvents.filter((event) => event.event_type === "scout.live_fetch.verified");
  const scoutProjection = await buildScoutProjection({
    stagingDir: options.stagingDir,
    liveVerificationEvents,
    maxCandidates: options.maxCandidates,
  });
  const gateProjection = evaluateGateCascade(data);
  const ui = applyDerivedState(data, gateProjection, scoutProjection, localEvents);

  return {
    events,
    localEvents,
    ui,
    projections: ui.projections,
  };
}

export { APP_ROOT, SEED_EVENTS_PATH, DEFAULT_EVENT_LOG_PATH };
