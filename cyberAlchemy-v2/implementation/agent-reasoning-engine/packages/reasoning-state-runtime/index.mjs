import {
  closeSync,
  existsSync,
  fsyncSync,
  mkdirSync,
  openSync,
  readFileSync,
  writeSync,
} from "node:fs";
import {dirname, resolve} from "node:path";

import {
  canonicalJson,
  canonicalizeJson,
  deepFreeze,
  sha256HexText,
} from "../intent-route-resolver/index.mjs";

export const REASONING_STATE_EVENT_SCHEMA = "are.reasoning-state-event/v1";
export const REASONING_STATE_EPOCH_SCHEMA = "are.reasoning-state-epoch/v1";
export const REASONING_STATE_CHECKPOINT_SCHEMA = "are.reasoning-state-checkpoint/v1";
export const REASONING_REQUEST_HEADER_SCHEMA = "are.reasoning-request-series-header/v1";
export const REASONING_DISPATCH_SCHEMA = "are.reasoning-dispatch/v1";
export const REASONING_DISPATCH_VERIFICATION_SCHEMA = "are.reasoning-dispatch-verification/v1";
export const REASONING_STATE_INDEX_SCHEMA = "are.reasoning-state-derived-index/v1";
export const REASONING_STATE_LOG_VERIFICATION_SCHEMA = "are.reasoning-state-log-verification/v1";
export const REASONING_STATE_RECOVERY_SCHEMA = "are.reasoning-state-recovery-assessment/v1";
export const REASONING_STATE_FRONTIER_SCHEMA = "are.reasoning-state-frontier/v1";

const ledgers = new WeakSet();
const sinks = new WeakSet();
const CHECKPOINT_KINDS = new Set(["before-model-request", "before-effect", "before-continuation", "after-turn-completion", "manual"]);

function freeze(value) {
  return deepFreeze(canonicalizeJson(value));
}

function digest(value) {
  return sha256HexText(canonicalJson(canonicalizeJson(value)));
}

function record(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function text(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function fail(stage, reasonCodes, residue = []) {
  return freeze({
    schema_version: "are.reasoning-state-failure/v1",
    ok: false,
    stage,
    reason_codes: [...new Set(reasonCodes)].sort(),
    residue,
    authority_effect: "none",
  });
}

function canonicalOrder(values) {
  return [...values].map((value) => canonicalizeJson(value)).sort((left, right) => canonicalJson(left).localeCompare(canonicalJson(right)));
}

function sinkResult(operation, disposition, details = {}) {
  return freeze({ok: true, operation, disposition, ...details, authority_effect: "none"});
}

export function createMemoryReasoningStateSink() {
  const state = {records: [], flushCount: 0, closed: false};
  const sink = Object.freeze({
    durability: "process-memory",
    append(value) {
      if (state.closed) return fail("sink-append", ["reasoning.sink-closed"]);
      state.records.push(freeze(value));
      return sinkResult("append", "appended", {record_count: state.records.length});
    },
    flush() {
      if (state.closed) return fail("sink-flush", ["reasoning.sink-closed"]);
      state.flushCount += 1;
      return sinkResult("flush", "flushed", {flush_count: state.flushCount, durability: "process-memory"});
    },
    snapshot: () => freeze([...state.records]),
    inspect: () => freeze({durability: "process-memory", record_count: state.records.length, flush_count: state.flushCount, closed: state.closed, authority_effect: "none"}),
    close() {
      state.closed = true;
      return sinkResult("close", "closed");
    },
  });
  sinks.add(sink);
  return sink;
}

export function createAppendOnlyFileReasoningStateSink({path, create_parent = true, initial_record_count = 0} = {}) {
  if (!text(path)) throw new TypeError("An explicit reasoning-state log path is required.");
  if (!Number.isSafeInteger(initial_record_count) || initial_record_count < 0) throw new TypeError("The initial reasoning-state record count must be a non-negative safe integer.");
  const absolutePath = resolve(path);
  if (create_parent) mkdirSync(dirname(absolutePath), {recursive: true, mode: 0o700});
  const descriptor = openSync(absolutePath, "a", 0o600);
  const state = {descriptor, path: absolutePath, records: initial_record_count, flushCount: 0, closed: false};
  const sink = Object.freeze({
    durability: "append-only-file-fsync",
    path: absolutePath,
    append(value) {
      if (state.closed) return fail("sink-append", ["reasoning.sink-closed"]);
      try {
        const bytes = `${canonicalJson(canonicalizeJson(value))}\n`;
        writeSync(state.descriptor, bytes, null, "utf8");
        state.records += 1;
        return sinkResult("append", "appended", {record_count: state.records, byte_count: Buffer.byteLength(bytes)});
      } catch (error) {
        return fail("sink-append", ["reasoning.sink-append-failed"], [{message: error.message}]);
      }
    },
    flush() {
      if (state.closed) return fail("sink-flush", ["reasoning.sink-closed"]);
      try {
        fsyncSync(state.descriptor);
        state.flushCount += 1;
        return sinkResult("flush", "flushed", {flush_count: state.flushCount, durability: "append-only-file-fsync"});
      } catch (error) {
        return fail("sink-flush", ["reasoning.sink-flush-failed"], [{message: error.message}]);
      }
    },
    inspect: () => freeze({durability: "append-only-file-fsync", path: state.path, record_count: state.records, flush_count: state.flushCount, closed: state.closed, authority_effect: "none"}),
    close() {
      if (!state.closed) closeSync(state.descriptor);
      state.closed = true;
      return sinkResult("close", "closed");
    },
  });
  sinks.add(sink);
  return sink;
}

function verifiedSink(sink) {
  return sinks.has(sink) && typeof sink.append === "function" && typeof sink.flush === "function";
}

function ledgerState(ledger) {
  if (!ledgers.has(ledger)) throw new TypeError("A verified reasoning-state ledger is required.");
  return ledger._state;
}

function eventMaterial(event) {
  const {event_digest: _eventDigest, ...material} = event;
  return material;
}

function checkpointMaterial(checkpoint) {
  const {checkpoint_digest: _checkpointDigest, ...material} = checkpoint;
  return material;
}

function frontierMaterial(frontier) {
  const {frontier_digest: _frontierDigest, frontier_id: _frontierId, ...material} = frontier;
  return material;
}

export function verifyReasoningStateFrontier(frontier) {
  const reasons = [];
  if (!record(frontier) || frontier.schema_version !== REASONING_STATE_FRONTIER_SCHEMA) reasons.push("reasoning.frontier-schema-invalid");
  if (!text(frontier?.ledger_id)) reasons.push("reasoning.frontier-ledger-id-required");
  if (!text(frontier?.frontier_key)) reasons.push("reasoning.frontier-key-required");
  if (!text(frontier?.subject_digest)) reasons.push("reasoning.frontier-subject-digest-required");
  if (!record(frontier?.state)) reasons.push("reasoning.frontier-state-required");
  if (frontier?.authority_effect !== "none") reasons.push("reasoning.frontier-authority-effect-invalid");
  if (record(frontier)) {
    const expectedDigest = digest(frontierMaterial(frontier));
    if (frontier.frontier_digest !== expectedDigest) reasons.push("reasoning.frontier-digest-invalid");
    if (frontier.frontier_id !== `reasoning-frontier:${expectedDigest}`) reasons.push("reasoning.frontier-id-invalid");
  }
  return reasons.length > 0
    ? fail("frontier-verification", reasons)
    : freeze({ok: true, value: frontier, digest: frontier.frontier_digest, authority_effect: "none"});
}

function verifyCheckpoint(checkpoint) {
  return record(checkpoint)
    && checkpoint.schema_version === REASONING_STATE_CHECKPOINT_SCHEMA
    && text(checkpoint.checkpoint_digest)
    && digest(checkpointMaterial(checkpoint)) === checkpoint.checkpoint_digest
    && text(checkpoint.ledger_id)
    && CHECKPOINT_KINDS.has(checkpoint.checkpoint_kind)
    && text(checkpoint.epoch_id)
    && text(checkpoint.epoch_digest)
    && checkpoint.epoch_id === `reasoning-state:${checkpoint.epoch_digest}`
    && (checkpoint.subject_digest === null || text(checkpoint.subject_digest))
    && (checkpoint.head_event_digest === null || text(checkpoint.head_event_digest))
    && ["process-memory", "append-only-file-fsync"].includes(checkpoint.durability)
    && checkpoint.authority_effect === "none";
}

function verifyEvent(event) {
  return record(event)
    && event.schema_version === REASONING_STATE_EVENT_SCHEMA
    && text(event.event_digest)
    && digest(eventMaterial(event)) === event.event_digest
    && text(event.event_kind)
    && text(event.idempotency_key)
    && Number.isSafeInteger(event.sequence)
    && event.sequence > 0
    && digest(event.content) === event.content_digest
    && event.authority_effect === "none";
}

export function appendReasoningStateEvent(ledger, input) {
  const state = ledgerState(ledger);
  const reasons = [];
  if (!record(input)) reasons.push("reasoning.event-input-required");
  if (!text(input?.event_kind)) reasons.push("reasoning.event-kind-required");
  if (!record(input?.content)) reasons.push("reasoning.event-content-required");
  if (reasons.length > 0) return fail("event-append", reasons);
  const content = canonicalizeJson(input.content);
  const contentDigest = digest(content);
  const idempotencyKey = text(input.idempotency_key)
    ? input.idempotency_key.trim()
    : `${input.event_kind.trim()}:${contentDigest}`;
  const existing = state.eventsByKey.get(idempotencyKey);
  if (existing) {
    if (existing.content_digest !== contentDigest || existing.event_kind !== input.event_kind.trim()) {
      return fail("event-append", ["reasoning.event-idempotency-conflict"], [{idempotency_key: idempotencyKey, existing_event_digest: existing.event_digest}]);
    }
    return freeze({ok: true, disposition: "duplicate", event: existing, authority_effect: "none"});
  }
  const material = canonicalizeJson({
    schema_version: REASONING_STATE_EVENT_SCHEMA,
    ledger_id: state.ledgerId,
    sequence: state.events.length + 1,
    event_kind: input.event_kind.trim(),
    idempotency_key: idempotencyKey,
    predecessor_digest: state.events.at(-1)?.event_digest ?? null,
    content,
    content_digest: contentDigest,
    provenance_refs: [...new Set(Array.isArray(input.provenance_refs) ? input.provenance_refs.filter(text).map((value) => value.trim()) : [])].sort(),
    authority_effect: "none",
  });
  const event = freeze({...material, event_digest: digest(material)});
  const persisted = state.sink.append({record_kind: "reasoning-state-event", value: event});
  if (!persisted?.ok) return fail("event-append", persisted?.reason_codes ?? ["reasoning.sink-append-failed"], persisted?.residue ?? []);
  state.events.push(event);
  state.eventsByKey.set(idempotencyKey, event);
  state.eventsByDigest.set(event.event_digest, event);
  return freeze({ok: true, disposition: "appended", event, authority_effect: "none"});
}

function epochMaterial(epoch) {
  const {epoch_digest: _epochDigest, epoch_id: _epochId, ...material} = epoch;
  return material;
}

export function verifyReasoningStateEpoch(epoch, events = null) {
  const reasons = [];
  if (!record(epoch) || epoch.schema_version !== REASONING_STATE_EPOCH_SCHEMA) reasons.push("reasoning.epoch-schema-invalid");
  if (!text(epoch?.epoch_digest) || (record(epoch) && digest(epochMaterial(epoch)) !== epoch.epoch_digest)) reasons.push("reasoning.epoch-digest-invalid");
  if (!text(epoch?.epoch_id) || epoch?.epoch_id !== `reasoning-state:${epoch?.epoch_digest}`) reasons.push("reasoning.epoch-id-invalid");
  if (!Array.isArray(epoch?.event_digests) || epoch.event_digests.length === 0 || new Set(epoch.event_digests).size !== epoch.event_digests.length) reasons.push("reasoning.epoch-events-invalid");
  if (Array.isArray(epoch?.event_digests) && digest(epoch.event_digests) !== epoch.event_set_digest) reasons.push("reasoning.epoch-event-set-digest-invalid");
  if (events !== null) {
    if (!Array.isArray(events) || events.some((event) => !verifyEvent(event)) || events.map((event) => event.event_digest).some((value, index) => value !== epoch?.event_digests?.[index])) {
      reasons.push("reasoning.epoch-event-binding-invalid");
    }
  }
  if (epoch?.authority_effect !== "none") reasons.push("reasoning.epoch-authority-effect-invalid");
  return reasons.length > 0
    ? fail("epoch-verification", reasons)
    : freeze({ok: true, value: epoch, digest: epoch.epoch_digest, authority_effect: "none"});
}

export function sealReasoningStateEpoch(ledger, input = {}) {
  const state = ledgerState(ledger);
  if (!record(input)) return fail("epoch-seal", ["reasoning.epoch-input-invalid"]);
  const eventDigests = Array.isArray(input.event_digests) ? [...input.event_digests] : state.events.map((event) => event.event_digest);
  if (eventDigests.length === 0 || new Set(eventDigests).size !== eventDigests.length) return fail("epoch-seal", ["reasoning.epoch-events-invalid"]);
  const events = eventDigests.map((eventDigest) => state.eventsByDigest.get(eventDigest));
  if (events.some((event) => !event)) return fail("epoch-seal", ["reasoning.epoch-event-missing"]);
  const materialWithoutIdentity = canonicalizeJson({
    schema_version: REASONING_STATE_EPOCH_SCHEMA,
    ledger_id: state.ledgerId,
    consumer_ref: text(input.consumer_ref) ? input.consumer_ref.trim() : null,
    request_ref: text(input.request_ref) ? input.request_ref.trim() : null,
    event_digests: eventDigests,
    event_set_digest: digest(eventDigests),
    selected_dependencies: Array.isArray(input.selected_dependencies) ? canonicalOrder(input.selected_dependencies) : [],
    context_envelope_digest: text(input.context_envelope_digest) ? input.context_envelope_digest.trim() : null,
    frontier: record(input.frontier) ? input.frontier : {},
    authority_effect: "none",
  });
  const stableDigest = digest(materialWithoutIdentity);
  const stableEpoch = freeze({...materialWithoutIdentity, epoch_id: `reasoning-state:${stableDigest}`, epoch_digest: stableDigest});
  const existing = state.epochs.get(stableEpoch.epoch_digest);
  if (existing) return freeze({ok: true, disposition: "duplicate", value: existing, digest: existing.epoch_digest, authority_effect: "none"});
  const persisted = state.sink.append({record_kind: "reasoning-state-epoch", value: stableEpoch});
  if (!persisted?.ok) return fail("epoch-seal", persisted?.reason_codes ?? ["reasoning.sink-append-failed"], persisted?.residue ?? []);
  state.epochs.set(stableEpoch.epoch_digest, stableEpoch);
  return freeze({ok: true, disposition: "sealed", value: stableEpoch, digest: stableEpoch.epoch_digest, authority_effect: "none"});
}

export function replayReasoningStateEpoch(ledger, epoch) {
  const state = ledgerState(ledger);
  const events = Array.isArray(epoch?.event_digests) ? epoch.event_digests.map((eventDigest) => state.eventsByDigest.get(eventDigest)) : [];
  const verified = verifyReasoningStateEpoch(epoch, events);
  if (!verified.ok) return verified;
  const material = canonicalizeJson({
    schema_version: "are.reasoning-state-replay/v1",
    ledger_id: state.ledgerId,
    epoch_id: epoch.epoch_id,
    epoch_digest: epoch.epoch_digest,
    events,
    external_calls: 0,
    authority_effect: "none",
  });
  return freeze({ok: true, value: {...material, replay_digest: digest(material)}, authority_effect: "none"});
}

export function checkpointReasoningState(ledger, input = {}) {
  const state = ledgerState(ledger);
  if (!record(input) || !CHECKPOINT_KINDS.has(input.checkpoint_kind)) return fail("checkpoint", ["reasoning.checkpoint-kind-invalid"]);
  const epoch = input.epoch;
  const events = Array.isArray(epoch?.event_digests) ? epoch.event_digests.map((eventDigest) => state.eventsByDigest.get(eventDigest)) : [];
  const verified = verifyReasoningStateEpoch(epoch, events);
  if (!verified.ok) return fail("checkpoint", verified.reason_codes, verified.residue);
  const material = canonicalizeJson({
    schema_version: REASONING_STATE_CHECKPOINT_SCHEMA,
    ledger_id: state.ledgerId,
    checkpoint_kind: input.checkpoint_kind,
    epoch_id: epoch.epoch_id,
    epoch_digest: epoch.epoch_digest,
    subject_digest: text(input.subject_digest) ? input.subject_digest.trim() : null,
    head_event_digest: state.events.at(-1)?.event_digest ?? null,
    durability: state.sink.durability,
    authority_effect: "none",
  });
  const checkpoint = freeze({...material, checkpoint_digest: digest(material)});
  if (!state.checkpoints.has(checkpoint.checkpoint_digest)) {
    const persisted = state.sink.append({record_kind: "reasoning-state-checkpoint", value: checkpoint});
    if (!persisted?.ok) return fail("checkpoint", persisted?.reason_codes ?? ["reasoning.sink-append-failed"], persisted?.residue ?? []);
    state.checkpoints.set(checkpoint.checkpoint_digest, checkpoint);
  }
  const flushed = state.sink.flush();
  if (!flushed?.ok) return fail("checkpoint", flushed?.reason_codes ?? ["reasoning.sink-flush-failed"], flushed?.residue ?? []);
  return freeze({ok: true, value: checkpoint, digest: checkpoint.checkpoint_digest, flush: flushed, authority_effect: "none"});
}

function inspectReasoningStateRecords(records, expectedLedgerId = null) {
  const reasons = [];
  const residue = [];
  const events = [];
  const eventsByKey = new Map();
  const eventsByDigest = new Map();
  const epochs = new Map();
  const checkpoints = new Map();
  const frontierEvents = [];
  const frontiers = new Map();
  let ledgerId = text(expectedLedgerId) ? expectedLedgerId.trim() : null;

  if (!Array.isArray(records)) return {ok: false, failure: fail("log-verification", ["reasoning.log-records-invalid"])};
  for (let index = 0; index < records.length; index += 1) {
    const wrapper = records[index];
    const recordNumber = index + 1;
    if (!record(wrapper) || Object.keys(wrapper).sort().join(",") !== "record_kind,value" || !text(wrapper.record_kind) || !record(wrapper.value)) {
      reasons.push("reasoning.log-record-wrapper-invalid");
      residue.push({record_number: recordNumber});
      continue;
    }
    const value = wrapper.value;
    const valueLedgerId = text(value.ledger_id) ? value.ledger_id.trim() : null;
    if (ledgerId === null && valueLedgerId !== null) ledgerId = valueLedgerId;
    if (valueLedgerId === null || (ledgerId !== null && valueLedgerId !== ledgerId)) {
      reasons.push("reasoning.log-ledger-id-mismatch");
      residue.push({record_number: recordNumber, expected_ledger_id: ledgerId, actual_ledger_id: valueLedgerId});
      continue;
    }

    if (wrapper.record_kind === "reasoning-state-event") {
      if (!verifyEvent(value)) {
        reasons.push("reasoning.log-event-invalid");
        residue.push({record_number: recordNumber});
        continue;
      }
      const expectedSequence = events.length + 1;
      const expectedPredecessor = events.at(-1)?.event_digest ?? null;
      if (value.sequence !== expectedSequence) reasons.push("reasoning.log-event-sequence-invalid");
      if (value.predecessor_digest !== expectedPredecessor) reasons.push("reasoning.log-event-chain-invalid");
      if (eventsByDigest.has(value.event_digest)) reasons.push("reasoning.log-event-digest-duplicate");
      if (eventsByKey.has(value.idempotency_key)) reasons.push("reasoning.log-event-idempotency-duplicate");
      if (value.sequence !== expectedSequence || value.predecessor_digest !== expectedPredecessor || eventsByDigest.has(value.event_digest) || eventsByKey.has(value.idempotency_key)) {
        residue.push({record_number: recordNumber, event_digest: value.event_digest});
        continue;
      }
      events.push(value);
      eventsByDigest.set(value.event_digest, value);
      eventsByKey.set(value.idempotency_key, value);
      if (value.event_kind === "reasoning-frontier-sealed") frontierEvents.push({event: value, recordNumber});
      continue;
    }

    if (wrapper.record_kind === "reasoning-state-epoch") {
      const selectedEvents = Array.isArray(value.event_digests) ? value.event_digests.map((eventDigest) => eventsByDigest.get(eventDigest)) : [];
      if (!verifyReasoningStateEpoch(value, selectedEvents).ok || selectedEvents.some((event) => !event)) {
        reasons.push("reasoning.log-epoch-invalid");
        residue.push({record_number: recordNumber, epoch_digest: value.epoch_digest ?? null});
        continue;
      }
      if (epochs.has(value.epoch_digest)) {
        reasons.push("reasoning.log-epoch-duplicate");
        residue.push({record_number: recordNumber, epoch_digest: value.epoch_digest});
        continue;
      }
      epochs.set(value.epoch_digest, value);
      continue;
    }

    if (wrapper.record_kind === "reasoning-state-checkpoint") {
      const epoch = epochs.get(value.epoch_digest);
      if (!verifyCheckpoint(value) || !epoch || value.epoch_id !== epoch.epoch_id || value.head_event_digest !== (events.at(-1)?.event_digest ?? null)) {
        reasons.push("reasoning.log-checkpoint-invalid");
        residue.push({record_number: recordNumber, checkpoint_digest: value.checkpoint_digest ?? null});
        continue;
      }
      if (checkpoints.has(value.checkpoint_digest)) {
        reasons.push("reasoning.log-checkpoint-duplicate");
        residue.push({record_number: recordNumber, checkpoint_digest: value.checkpoint_digest});
        continue;
      }
      checkpoints.set(value.checkpoint_digest, value);
      continue;
    }

    reasons.push("reasoning.log-record-kind-unknown");
    residue.push({record_number: recordNumber, record_kind: wrapper.record_kind});
  }

  for (const {event, recordNumber} of frontierEvents) {
    const frontier = event.content;
    const verifiedFrontier = verifyReasoningStateFrontier(frontier);
    if (!verifiedFrontier.ok || frontier.ledger_id !== ledgerId) {
      reasons.push("reasoning.log-frontier-invalid");
      residue.push({record_number: recordNumber, frontier_key: frontier?.frontier_key ?? null});
      continue;
    }
    if (frontiers.has(frontier.frontier_key)) {
      reasons.push("reasoning.log-frontier-key-duplicate");
      residue.push({record_number: recordNumber, frontier_key: frontier.frontier_key});
      continue;
    }
    const matchingEpochs = [...epochs.values()].filter((epoch) => epoch.event_digests.length === 1
      && epoch.event_digests[0] === event.event_digest
      && epoch.frontier?.reasoning_frontier_digest === frontier.frontier_digest);
    const matchingCheckpoints = matchingEpochs.flatMap((epoch) => [...checkpoints.values()].filter((checkpoint) => checkpoint.checkpoint_kind === "after-turn-completion"
      && checkpoint.epoch_digest === epoch.epoch_digest
      && checkpoint.subject_digest === frontier.subject_digest));
    if (matchingEpochs.length !== 1 || matchingCheckpoints.length !== 1) {
      reasons.push("reasoning.log-frontier-checkpoint-missing");
      residue.push({record_number: recordNumber, frontier_key: frontier.frontier_key});
      continue;
    }
    frontiers.set(frontier.frontier_key, freeze({frontier, event, epoch: matchingEpochs[0], checkpoint: matchingCheckpoints[0]}));
  }

  if (reasons.length > 0) return {ok: false, failure: fail("log-verification", reasons, residue)};
  const indexMaterial = canonicalizeJson({
    schema_version: REASONING_STATE_INDEX_SCHEMA,
    ledger_id: ledgerId,
    record_count: records.length,
    event_count: events.length,
    epoch_count: epochs.size,
    checkpoint_count: checkpoints.size,
    frontier_count: frontiers.size,
    head_event_digest: events.at(-1)?.event_digest ?? null,
    event_digests: events.map((event) => event.event_digest),
    epoch_digests: [...epochs.keys()],
    checkpoint_digests: [...checkpoints.keys()],
    frontier_digests: [...frontiers.values()].map((entry) => entry.frontier.frontier_digest),
    latest_checkpoint_digest: [...checkpoints.keys()].at(-1) ?? null,
    record_stream_digest: digest(records),
    derived: true,
    authority_effect: "none",
  });
  const index = freeze({...indexMaterial, index_digest: digest(indexMaterial)});
  return {ok: true, ledgerId, events, eventsByKey, eventsByDigest, epochs, checkpoints, frontiers, index};
}

function logValue(input, options = {}) {
  if (text(input)) return verifyReasoningStateLog(input, options);
  if (record(input) && input.schema_version === REASONING_STATE_LOG_VERIFICATION_SCHEMA && Array.isArray(input.records)) {
    return freeze({ok: true, value: input, authority_effect: "none"});
  }
  if (record(input) && input.ok === true && record(input.value) && input.value.schema_version === REASONING_STATE_LOG_VERIFICATION_SCHEMA) return input;
  return fail("log-verification", ["reasoning.log-input-invalid"]);
}

export function verifyReasoningStateLog(path, {allow_missing = false, expected_ledger_id = null} = {}) {
  if (!text(path)) return fail("log-verification", ["reasoning.log-path-required"]);
  const absolutePath = resolve(path);
  const present = existsSync(absolutePath);
  if (!present && !allow_missing) return fail("log-verification", ["reasoning.log-missing"], [{path: absolutePath}]);
  let bytes = Buffer.alloc(0);
  if (present) {
    try {
      bytes = readFileSync(absolutePath);
    } catch (error) {
      return fail("log-verification", ["reasoning.log-read-failed"], [{path: absolutePath, message: error.message}]);
    }
  }
  let source;
  try {
    source = new TextDecoder("utf-8", {fatal: true}).decode(bytes);
  } catch {
    return fail("log-verification", ["reasoning.log-utf8-invalid"], [{path: absolutePath}]);
  }
  if (source.length > 0 && !source.endsWith("\n")) return fail("log-verification", ["reasoning.log-torn-tail"], [{path: absolutePath, byte_count: bytes.length}]);
  const lines = source.length === 0 ? [] : source.slice(0, -1).split("\n");
  const records = [];
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    if (line.length === 0) return fail("log-verification", ["reasoning.log-blank-record"], [{line_number: index + 1}]);
    let parsed;
    try {
      parsed = JSON.parse(line);
    } catch {
      return fail("log-verification", ["reasoning.log-json-invalid"], [{line_number: index + 1}]);
    }
    if (canonicalJson(canonicalizeJson(parsed)) !== line) return fail("log-verification", ["reasoning.log-record-noncanonical"], [{line_number: index + 1}]);
    records.push(parsed);
  }
  const inspected = inspectReasoningStateRecords(records, expected_ledger_id);
  if (!inspected.ok) return inspected.failure;
  const material = canonicalizeJson({
    schema_version: REASONING_STATE_LOG_VERIFICATION_SCHEMA,
    path: absolutePath,
    source_state: present ? "present" : "absent",
    byte_count: bytes.length,
    log_digest: sha256HexText(source),
    records,
    index: inspected.index,
    external_calls: 0,
    authority_effect: "none",
  });
  return freeze({ok: true, value: {...material, verification_digest: digest(material)}, authority_effect: "none"});
}

export function rebuildReasoningStateIndexes(log, options = {}) {
  const verified = logValue(log, options);
  if (!verified.ok) return verified;
  const inspected = inspectReasoningStateRecords(verified.value.records, options.expected_ledger_id ?? null);
  if (!inspected.ok) return inspected.failure;
  return freeze({ok: true, value: inspected.index, digest: inspected.index.index_digest, external_calls: 0, authority_effect: "none"});
}

export function selectRecoverableCheckpoint(log, options = {}) {
  const verified = logValue(log, options);
  if (!verified.ok) return verified;
  const records = verified.value.records;
  if (records.length === 0) return freeze({ok: true, disposition: "empty", value: null, log_digest: verified.value.log_digest, authority_effect: "none"});
  const last = records.at(-1);
  if (last.record_kind !== "reasoning-state-checkpoint") {
    return fail("checkpoint-selection", ["reasoning.log-uncheckpointed-tail"], [{record_count: records.length, last_record_kind: last.record_kind}]);
  }
  return freeze({ok: true, disposition: "recoverable", value: last.value, digest: last.value.checkpoint_digest, log_digest: verified.value.log_digest, authority_effect: "none"});
}

export function recoverReasoningStateLedger(input, options = {}) {
  const configured = text(input) ? {path: input, ...options} : input;
  if (!record(configured) || !text(configured.path)) return fail("recovery", ["reasoning.log-path-required"]);
  const expectedLedgerId = text(configured.ledger_id) ? configured.ledger_id.trim() : null;
  const verified = verifyReasoningStateLog(configured.path, {allow_missing: configured.create_if_missing !== false, expected_ledger_id: expectedLedgerId});
  if (!verified.ok) return verified;
  const selected = selectRecoverableCheckpoint(verified);
  if (!selected.ok) return selected;
  const inspected = inspectReasoningStateRecords(verified.value.records, expectedLedgerId);
  if (!inspected.ok) return inspected.failure;
  const ledgerId = inspected.ledgerId ?? expectedLedgerId;
  if (!text(ledgerId)) return fail("recovery", ["reasoning.recovery-ledger-id-required"]);
  let sink;
  try {
    sink = createAppendOnlyFileReasoningStateSink({path: verified.value.path, initial_record_count: verified.value.records.length});
  } catch (error) {
    return fail("recovery", ["reasoning.recovery-sink-open-failed"], [{message: error.message}]);
  }
  let currentSource;
  try {
    currentSource = new TextDecoder("utf-8", {fatal: true}).decode(readFileSync(verified.value.path));
  } catch (error) {
    sink.close();
    return fail("recovery", ["reasoning.recovery-source-recheck-failed"], [{message: error.message}]);
  }
  if (sha256HexText(currentSource) !== verified.value.log_digest) {
    sink.close();
    return fail("recovery", ["reasoning.recovery-source-drift"], [{expected_log_digest: verified.value.log_digest, actual_log_digest: sha256HexText(currentSource)}]);
  }
  const assessmentMaterial = canonicalizeJson({
    schema_version: REASONING_STATE_RECOVERY_SCHEMA,
    ledger_id: ledgerId,
    log_path: verified.value.path,
    source_state: verified.value.source_state,
    log_digest: verified.value.log_digest,
    record_count: verified.value.records.length,
    derived_index_digest: inspected.index.index_digest,
    recovered_checkpoint_digest: selected.value?.checkpoint_digest ?? null,
    disposition: selected.disposition === "empty" ? "empty-ledger-ready" : "recovered",
    external_calls: 0,
    authority_effect: "none",
  });
  const assessment = freeze({...assessmentMaterial, recovery_digest: digest(assessmentMaterial)});
  const ledger = createReasoningStateLedger({ledger_id: ledgerId, sink});
  const state = ledgerState(ledger);
  state.events.push(...inspected.events);
  for (const [key, value] of inspected.eventsByKey) state.eventsByKey.set(key, value);
  for (const [key, value] of inspected.eventsByDigest) state.eventsByDigest.set(key, value);
  for (const [key, value] of inspected.epochs) state.epochs.set(key, value);
  for (const [key, value] of inspected.checkpoints) state.checkpoints.set(key, value);
  for (const [key, value] of inspected.frontiers) state.frontiers.set(key, value);
  state.recovery = assessment;
  return Object.freeze({ok: true, ledger, assessment, checkpoint: selected.value, authority_effect: "none"});
}

function requestConfiguration(params) {
  if (!record(params)) return {};
  const excluded = new Set(["input", "additionalContext"]);
  return Object.fromEntries(Object.entries(params).filter(([key]) => !excluded.has(key)));
}

export function createRequestSeriesHeader(message, overrides = {}) {
  if (!record(message) || !text(message.method)) return fail("request-header", ["reasoning.dispatch-message-invalid"]);
  const params = record(message.params) ? message.params : {};
  const material = canonicalizeJson({
    schema_version: REASONING_REQUEST_HEADER_SCHEMA,
    protocol: message.jsonrpc ?? null,
    method: message.method,
    provider_ref: overrides.provider_ref ?? params.provider ?? null,
    model_ref: overrides.model_ref ?? params.model ?? null,
    system_digest: digest(overrides.system ?? params.developerInstructions ?? params.systemInstructions ?? null),
    tools_digest: digest(overrides.tools ?? params.tools ?? null),
    configuration_digest: digest(overrides.configuration ?? requestConfiguration(params)),
    authority_effect: "none",
  });
  return freeze({...material, request_header_digest: digest(material)});
}

function dispatchMaterial(dispatch) {
  const {dispatch_digest: _dispatchDigest, ...material} = dispatch;
  return material;
}

export function materializeReasoningDispatch({epoch, message, request_header = null} = {}) {
  const epochVerified = verifyReasoningStateEpoch(epoch);
  if (!epochVerified.ok) return fail("dispatch-materialization", epochVerified.reason_codes);
  if (!record(message) || !text(message.method)) return fail("dispatch-materialization", ["reasoning.dispatch-message-invalid"]);
  const header = request_header ?? createRequestSeriesHeader(message);
  if (!record(header) || header.schema_version !== REASONING_REQUEST_HEADER_SCHEMA) return fail("dispatch-materialization", ["reasoning.request-header-invalid"]);
  const {request_header_digest: headerDigest, ...headerMaterial} = header;
  if (digest(headerMaterial) !== headerDigest) return fail("dispatch-materialization", ["reasoning.request-header-digest-invalid"]);
  const canonicalRequest = canonicalJson(canonicalizeJson(message));
  const material = canonicalizeJson({
    schema_version: REASONING_DISPATCH_SCHEMA,
    epoch_id: epoch.epoch_id,
    epoch_digest: epoch.epoch_digest,
    request_header: header,
    request_header_digest: header.request_header_digest,
    canonical_request: canonicalRequest,
    canonical_request_bytes: Buffer.byteLength(canonicalRequest),
    message_digest: sha256HexText(canonicalRequest),
    authority_effect: "none",
  });
  const value = freeze({...material, dispatch_digest: digest(material)});
  return freeze({ok: true, value, digest: value.dispatch_digest, authority_effect: "none"});
}

export function verifyReasoningDispatch(dispatch, {epoch = null, message = null} = {}) {
  const reasons = [];
  if (!record(dispatch) || dispatch.schema_version !== REASONING_DISPATCH_SCHEMA) reasons.push("reasoning.dispatch-schema-invalid");
  if (!text(dispatch?.dispatch_digest) || (record(dispatch) && digest(dispatchMaterial(dispatch)) !== dispatch.dispatch_digest)) reasons.push("reasoning.dispatch-digest-invalid");
  let reconstructed = null;
  try {
    reconstructed = JSON.parse(dispatch?.canonical_request);
    if (canonicalJson(canonicalizeJson(reconstructed)) !== dispatch.canonical_request) reasons.push("reasoning.dispatch-canonical-request-invalid");
  } catch {
    reasons.push("reasoning.dispatch-request-invalid");
  }
  if (text(dispatch?.canonical_request) && sha256HexText(dispatch.canonical_request) !== dispatch.message_digest) reasons.push("reasoning.dispatch-message-digest-invalid");
  if (Buffer.byteLength(dispatch?.canonical_request ?? "") !== dispatch?.canonical_request_bytes) reasons.push("reasoning.dispatch-byte-count-invalid");
  const header = dispatch?.request_header;
  if (!record(header)) reasons.push("reasoning.request-header-invalid");
  else {
    const {request_header_digest: headerDigest, ...headerMaterial} = header;
    if (digest(headerMaterial) !== headerDigest || headerDigest !== dispatch.request_header_digest) reasons.push("reasoning.request-header-digest-invalid");
  }
  if (epoch && (dispatch?.epoch_id !== epoch.epoch_id || dispatch?.epoch_digest !== epoch.epoch_digest)) reasons.push("reasoning.dispatch-epoch-mismatch");
  if (message && canonicalJson(canonicalizeJson(message)) !== dispatch?.canonical_request) reasons.push("reasoning.dispatch-message-mismatch");
  const material = canonicalizeJson({
    schema_version: REASONING_DISPATCH_VERIFICATION_SCHEMA,
    dispatch_digest: dispatch?.dispatch_digest ?? null,
    epoch_digest: dispatch?.epoch_digest ?? null,
    message_digest: dispatch?.message_digest ?? null,
    request_header_digest: dispatch?.request_header_digest ?? null,
    valid: reasons.length === 0,
    reason_codes: [...new Set(reasons)].sort(),
    authority_effect: "none",
  });
  const verification = freeze({...material, verification_digest: digest(material)});
  return reasons.length > 0
    ? freeze({ok: false, stage: "dispatch-verification", reason_codes: verification.reason_codes, verification, authority_effect: "none"})
    : freeze({ok: true, value: verification, reconstructed_message: freeze(reconstructed), digest: verification.verification_digest, authority_effect: "none"});
}

export function reconstructReasoningDispatch(dispatch, options = {}) {
  const verified = verifyReasoningDispatch(dispatch, options);
  if (!verified.ok) return verified;
  return freeze({ok: true, value: verified.reconstructed_message, dispatch_digest: dispatch.dispatch_digest, verification_digest: verified.digest, authority_effect: "none"});
}

export function sealReasoningStateFrontier(ledger, input = {}) {
  const state = ledgerState(ledger);
  const reasons = [];
  if (!record(input)) reasons.push("reasoning.frontier-input-required");
  if (!text(input?.frontier_key)) reasons.push("reasoning.frontier-key-required");
  if (!text(input?.subject_digest)) reasons.push("reasoning.frontier-subject-digest-required");
  if (!record(input?.state)) reasons.push("reasoning.frontier-state-required");
  if (reasons.length > 0) return fail("frontier-seal", reasons);
  const material = canonicalizeJson({
    schema_version: REASONING_STATE_FRONTIER_SCHEMA,
    ledger_id: state.ledgerId,
    frontier_key: input.frontier_key.trim(),
    subject_digest: input.subject_digest.trim(),
    consumer_ref: text(input.consumer_ref) ? input.consumer_ref.trim() : null,
    request_ref: text(input.request_ref) ? input.request_ref.trim() : null,
    context_envelope_digest: text(input.context_envelope_digest) ? input.context_envelope_digest.trim() : null,
    prior_reasoning_epoch_digest: text(input.prior_reasoning_epoch_digest) ? input.prior_reasoning_epoch_digest.trim() : null,
    state: canonicalizeJson(input.state),
    authority_effect: "none",
  });
  const frontierDigest = digest(material);
  const frontier = freeze({...material, frontier_id: `reasoning-frontier:${frontierDigest}`, frontier_digest: frontierDigest});
  const existing = state.frontiers.get(frontier.frontier_key);
  if (existing) {
    if (existing.frontier.frontier_digest !== frontier.frontier_digest) {
      return fail("frontier-seal", ["reasoning.frontier-idempotency-conflict"], [{frontier_key: frontier.frontier_key, existing_frontier_digest: existing.frontier.frontier_digest}]);
    }
    return freeze({ok: true, disposition: "duplicate", ...existing, authority_effect: "none"});
  }
  const appended = appendReasoningStateEvent(ledger, {
    event_kind: "reasoning-frontier-sealed",
    idempotency_key: `reasoning-frontier:${frontier.frontier_key}`,
    content: frontier,
    provenance_refs: Array.isArray(input.provenance_refs) ? input.provenance_refs : [],
  });
  if (!appended.ok) return appended;
  const sealed = sealReasoningStateEpoch(ledger, {
    event_digests: [appended.event.event_digest],
    consumer_ref: frontier.consumer_ref,
    request_ref: frontier.request_ref,
    context_envelope_digest: frontier.context_envelope_digest,
    frontier: {reasoning_frontier_digest: frontier.frontier_digest, frontier_key: frontier.frontier_key},
  });
  if (!sealed.ok) return sealed;
  const checkpointed = checkpointReasoningState(ledger, {
    checkpoint_kind: "after-turn-completion",
    epoch: sealed.value,
    subject_digest: frontier.subject_digest,
  });
  if (!checkpointed.ok) return checkpointed;
  const entry = freeze({frontier, event: appended.event, epoch: sealed.value, checkpoint: checkpointed.value});
  state.frontiers.set(frontier.frontier_key, entry);
  return freeze({ok: true, disposition: "sealed", ...entry, authority_effect: "none"});
}

export function getReasoningStateFrontier(ledger, frontierKey) {
  const state = ledgerState(ledger);
  if (!text(frontierKey)) return fail("frontier-get", ["reasoning.frontier-key-required"]);
  const entry = state.frontiers.get(frontierKey.trim());
  return entry
    ? freeze({ok: true, disposition: "found", ...entry, authority_effect: "none"})
    : freeze({ok: true, disposition: "absent", value: null, authority_effect: "none"});
}

export function listReasoningStateFrontiers(ledger) {
  const state = ledgerState(ledger);
  return freeze([...state.frontiers.values()].sort((left, right) => left.frontier.frontier_key.localeCompare(right.frontier.frontier_key)));
}

export function createReasoningStateLedger({ledger_id = "are-reasoning-state:local", sink = createMemoryReasoningStateSink()} = {}) {
  if (!text(ledger_id)) throw new TypeError("A reasoning-state ledger id is required.");
  if (!verifiedSink(sink)) throw new TypeError("A verified reasoning-state sink is required.");
  const state = {
    ledgerId: ledger_id.trim(),
    sink,
    events: [],
    eventsByKey: new Map(),
    eventsByDigest: new Map(),
    epochs: new Map(),
    checkpoints: new Map(),
    frontiers: new Map(),
    recovery: null,
  };
  const ledger = Object.freeze({
    _state: state,
    append: (input) => appendReasoningStateEvent(ledger, input),
    seal: (input) => sealReasoningStateEpoch(ledger, input),
    replay: (epoch) => replayReasoningStateEpoch(ledger, epoch),
    checkpoint: (input) => checkpointReasoningState(ledger, input),
    sealFrontier: (input) => sealReasoningStateFrontier(ledger, input),
    getFrontier: (frontierKey) => getReasoningStateFrontier(ledger, frontierKey),
    frontiers: () => listReasoningStateFrontiers(ledger),
    snapshot: () => freeze([...state.events]),
    inspect: () => freeze({ledger_id: state.ledgerId, event_count: state.events.length, epoch_count: state.epochs.size, checkpoint_count: state.checkpoints.size, frontier_count: state.frontiers.size, head_event_digest: state.events.at(-1)?.event_digest ?? null, durability: state.sink.durability, sink: state.sink.inspect?.() ?? null, recovery: state.recovery, authority_effect: "none"}),
    close: () => state.sink.close?.() ?? sinkResult("close", "unsupported"),
  });
  ledgers.add(ledger);
  return ledger;
}
