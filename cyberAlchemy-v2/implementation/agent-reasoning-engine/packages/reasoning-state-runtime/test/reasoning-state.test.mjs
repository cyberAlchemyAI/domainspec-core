import assert from "node:assert/strict";
import {appendFileSync, mkdtempSync, readFileSync, rmSync, writeFileSync} from "node:fs";
import {tmpdir} from "node:os";
import {resolve} from "node:path";
import test from "node:test";

import {
  checkpointReasoningState,
  createAppendOnlyFileReasoningStateSink,
  createMemoryReasoningStateSink,
  createReasoningStateLedger,
  createRequestSeriesHeader,
  materializeReasoningDispatch,
  getReasoningStateFrontier,
  listReasoningStateFrontiers,
  rebuildReasoningStateIndexes,
  recoverReasoningStateLedger,
  reconstructReasoningDispatch,
  sealReasoningStateFrontier,
  selectRecoverableCheckpoint,
  verifyReasoningDispatch,
  verifyReasoningStateLog,
  verifyReasoningStateEpoch,
  verifyReasoningStateFrontier,
} from "../index.mjs";

function state() {
  const sink = createMemoryReasoningStateSink();
  const ledger = createReasoningStateLedger({ledger_id: "reasoning:test", sink});
  const request = ledger.append({event_kind: "request-interpreted", content: {request_id: "request:1", route_id: "CA2-ROUTE-RESEARCH"}});
  const context = ledger.append({event_kind: "context-projected", content: {context_envelope_digest: "context:1", selected_dependencies: ["definition:1"]}});
  const epoch = ledger.seal({event_digests: [request.event.event_digest, context.event.event_digest], consumer_ref: "codex:test", request_ref: "request:1", context_envelope_digest: "context:1", selected_dependencies: ["definition:1"], frontier: {continuation: "open"}});
  return {sink, ledger, request, context, epoch};
}

test("append-only events are hash-chained, immutable, and idempotent", () => {
  const {ledger, request, context} = state();
  assert.equal(request.ok, true);
  assert.equal(context.event.predecessor_digest, request.event.event_digest);
  assert.equal(Object.isFrozen(request.event), true);
  const duplicate = ledger.append({event_kind: "request-interpreted", content: {request_id: "request:1", route_id: "CA2-ROUTE-RESEARCH"}});
  assert.equal(duplicate.disposition, "duplicate");
  assert.equal(ledger.inspect().event_count, 2);
});

test("sealed epochs select exact events and replay deterministically", () => {
  const {ledger, epoch} = state();
  assert.equal(epoch.ok, true);
  assert.equal(verifyReasoningStateEpoch(epoch.value).ok, true);
  const first = ledger.replay(epoch.value);
  const second = ledger.replay(epoch.value);
  assert.deepEqual(first, second);
  assert.equal(first.value.events.length, 2);
  const changed = structuredClone(epoch.value);
  changed.event_digests.reverse();
  assert.equal(verifyReasoningStateEpoch(changed).ok, false);
});

test("selected dependency ordering does not change epoch identity", () => {
  const {ledger, request, context} = state();
  const input = {event_digests: [request.event.event_digest, context.event.event_digest], selected_dependencies: [{id: "b", digest: "2"}, {id: "a", digest: "1"}]};
  const left = ledger.seal(input);
  const right = ledger.seal({...input, selected_dependencies: [...input.selected_dependencies].reverse()});
  assert.equal(left.digest, right.digest);
  assert.equal(right.disposition, "duplicate");
});

test("checkpoints flush only after epoch verification", () => {
  const {sink, ledger, epoch} = state();
  const checkpoint = checkpointReasoningState(ledger, {checkpoint_kind: "before-model-request", epoch: epoch.value, subject_digest: "dispatch:1"});
  assert.equal(checkpoint.ok, true);
  assert.equal(checkpoint.value.durability, "process-memory");
  assert.equal(sink.inspect().flush_count, 1);
  const tampered = structuredClone(epoch.value);
  tampered.epoch_digest = "0".repeat(64);
  assert.equal(ledger.checkpoint({checkpoint_kind: "before-effect", epoch: tampered}).ok, false);
  assert.equal(sink.inspect().flush_count, 1);
});

test("file sink appends canonical records and fsyncs at checkpoints", () => {
  const directory = mkdtempSync(resolve(tmpdir(), "are-reasoning-state-"));
  const path = resolve(directory, "events.jsonl");
  try {
    const sink = createAppendOnlyFileReasoningStateSink({path});
    const ledger = createReasoningStateLedger({ledger_id: "reasoning:file", sink});
    const appended = ledger.append({event_kind: "request-interpreted", content: {request_id: "file:1"}});
    const epoch = ledger.seal({event_digests: [appended.event.event_digest], request_ref: "file:1"});
    const checkpoint = ledger.checkpoint({checkpoint_kind: "before-model-request", epoch: epoch.value});
    assert.equal(checkpoint.ok, true);
    ledger.close();
    const lines = readFileSync(path, "utf8").trim().split("\n").map(JSON.parse);
    assert.deepEqual(lines.map((line) => line.record_kind), ["reasoning-state-event", "reasoning-state-epoch", "reasoning-state-checkpoint"]);
    assert.equal(lines[0].value.event_digest, appended.event.event_digest);
  } finally {
    rmSync(directory, {recursive: true, force: true});
  }
});

test("dispatch reconstruction binds exact request, header, and epoch", () => {
  const {epoch} = state();
  const message = {jsonrpc: "2.0", id: 7, method: "turn/start", params: {threadId: "thread:1", model: "gpt-test", input: [{type: "text", text: "Research it."}], tools: [{name: "search"}]}};
  const header = createRequestSeriesHeader(message);
  const dispatch = materializeReasoningDispatch({epoch: epoch.value, message, request_header: header});
  assert.equal(dispatch.ok, true);
  const verified = verifyReasoningDispatch(dispatch.value, {epoch: epoch.value, message});
  assert.equal(verified.ok, true);
  assert.deepEqual(reconstructReasoningDispatch(dispatch.value, {epoch: epoch.value}).value, message);
  const changed = structuredClone(message);
  changed.params.model = "different";
  assert.deepEqual(verifyReasoningDispatch(dispatch.value, {epoch: epoch.value, message: changed}).reason_codes, ["reasoning.dispatch-message-mismatch"]);
});

test("idempotency conflicts and invalid dispatches fail closed", () => {
  const {ledger, epoch} = state();
  ledger.append({event_kind: "fact", idempotency_key: "same", content: {value: 1}});
  const conflict = ledger.append({event_kind: "fact", idempotency_key: "same", content: {value: 2}});
  assert.deepEqual(conflict.reason_codes, ["reasoning.event-idempotency-conflict"]);
  assert.equal(materializeReasoningDispatch({epoch: epoch.value, message: null}).ok, false);
});

test("a checkpointed file recovers its exact ledger and continues the hash chain", () => {
  const directory = mkdtempSync(resolve(tmpdir(), "are-reasoning-recovery-"));
  const path = resolve(directory, "reasoning.jsonl");
  try {
    const sink = createAppendOnlyFileReasoningStateSink({path});
    const ledger = createReasoningStateLedger({ledger_id: "reasoning:recover", sink});
    const event = ledger.append({event_kind: "request-interpreted", content: {request_id: "recover:1"}});
    const epoch = ledger.seal({event_digests: [event.event.event_digest], request_ref: "recover:1"});
    const checkpoint = ledger.checkpoint({checkpoint_kind: "before-model-request", epoch: epoch.value, subject_digest: "dispatch:recover:1"});
    ledger.close();

    const verified = verifyReasoningStateLog(path, {expected_ledger_id: "reasoning:recover"});
    assert.equal(verified.ok, true);
    assert.equal(verified.value.index.event_count, 1);
    assert.equal(rebuildReasoningStateIndexes(verified).value.index_digest, verified.value.index.index_digest);
    assert.equal(selectRecoverableCheckpoint(verified).digest, checkpoint.digest);

    const recovered = recoverReasoningStateLedger({path, ledger_id: "reasoning:recover"});
    assert.equal(recovered.ok, true);
    assert.equal(recovered.assessment.disposition, "recovered");
    assert.equal(recovered.ledger.inspect().sink.record_count, 3);
    assert.deepEqual(recovered.ledger.replay(epoch.value).value.events, [event.event]);
    const successor = recovered.ledger.append({event_kind: "request-interpreted", content: {request_id: "recover:2"}});
    assert.equal(successor.event.sequence, 2);
    assert.equal(successor.event.predecessor_digest, event.event.event_digest);
    recovered.ledger.close();
  } finally {
    rmSync(directory, {recursive: true, force: true});
  }
});

test("recovery creates a new empty file only when an explicit ledger identity is supplied", () => {
  const directory = mkdtempSync(resolve(tmpdir(), "are-reasoning-empty-"));
  const path = resolve(directory, "new.jsonl");
  try {
    assert.deepEqual(verifyReasoningStateLog(path).reason_codes, ["reasoning.log-missing"]);
    assert.deepEqual(recoverReasoningStateLedger(path).reason_codes, ["reasoning.recovery-ledger-id-required"]);
    const recovered = recoverReasoningStateLedger({path, ledger_id: "reasoning:new"});
    assert.equal(recovered.ok, true);
    assert.equal(recovered.assessment.disposition, "empty-ledger-ready");
    assert.equal(recovered.ledger.inspect().event_count, 0);
    recovered.ledger.close();
  } finally {
    rmSync(directory, {recursive: true, force: true});
  }
});

test("torn, malformed, noncanonical, and unknown records fail closed", () => {
  const directory = mkdtempSync(resolve(tmpdir(), "are-reasoning-corrupt-"));
  try {
    const torn = resolve(directory, "torn.jsonl");
    writeFileSync(torn, "{\"record_kind\":");
    assert.deepEqual(verifyReasoningStateLog(torn).reason_codes, ["reasoning.log-torn-tail"]);

    const malformed = resolve(directory, "malformed.jsonl");
    writeFileSync(malformed, "not-json\n");
    assert.deepEqual(verifyReasoningStateLog(malformed).reason_codes, ["reasoning.log-json-invalid"]);

    const noncanonical = resolve(directory, "noncanonical.jsonl");
    writeFileSync(noncanonical, "{ \"record_kind\": \"other\", \"value\": {} }\n");
    assert.deepEqual(verifyReasoningStateLog(noncanonical).reason_codes, ["reasoning.log-record-noncanonical"]);

    const unknown = resolve(directory, "unknown.jsonl");
    writeFileSync(unknown, '{"record_kind":"other","value":{"authority_effect":"none","ledger_id":"reasoning:unknown"}}\n');
    assert.deepEqual(verifyReasoningStateLog(unknown).reason_codes, ["reasoning.log-record-kind-unknown"]);

    const leftPath = resolve(directory, "left.jsonl");
    const rightPath = resolve(directory, "right.jsonl");
    const left = createReasoningStateLedger({ledger_id: "reasoning:left", sink: createAppendOnlyFileReasoningStateSink({path: leftPath})});
    const right = createReasoningStateLedger({ledger_id: "reasoning:right", sink: createAppendOnlyFileReasoningStateSink({path: rightPath})});
    left.append({event_kind: "fact", content: {side: "left"}});
    right.append({event_kind: "fact", content: {side: "right"}});
    left.close();
    right.close();
    const mixed = resolve(directory, "mixed.jsonl");
    writeFileSync(mixed, `${readFileSync(leftPath, "utf8")}${readFileSync(rightPath, "utf8")}`);
    assert.equal(verifyReasoningStateLog(mixed).reason_codes.includes("reasoning.log-ledger-id-mismatch"), true);
  } finally {
    rmSync(directory, {recursive: true, force: true});
  }
});

test("tampering and an uncheckpointed crash tail block recovery without truncation", () => {
  const directory = mkdtempSync(resolve(tmpdir(), "are-reasoning-tail-"));
  const path = resolve(directory, "reasoning.jsonl");
  try {
    const sink = createAppendOnlyFileReasoningStateSink({path});
    const ledger = createReasoningStateLedger({ledger_id: "reasoning:tail", sink});
    const event = ledger.append({event_kind: "request-interpreted", content: {request_id: "tail:1"}});
    const epoch = ledger.seal({event_digests: [event.event.event_digest]});
    ledger.checkpoint({checkpoint_kind: "manual", epoch: epoch.value});
    ledger.append({event_kind: "uncommitted", content: {request_id: "tail:2"}});
    ledger.close();
    const before = readFileSync(path);
    assert.deepEqual(recoverReasoningStateLedger({path, ledger_id: "reasoning:tail"}).reason_codes, ["reasoning.log-uncheckpointed-tail"]);
    assert.deepEqual(readFileSync(path), before);

    const lines = readFileSync(path, "utf8").trimEnd().split("\n").map(JSON.parse);
    lines[0].value.content.request_id = "tampered";
    writeFileSync(path, `${lines.map(JSON.stringify).join("\n")}\n`);
    assert.equal(verifyReasoningStateLog(path).reason_codes.includes("reasoning.log-event-invalid"), true);
  } finally {
    rmSync(directory, {recursive: true, force: true});
  }
});

test("blank records and bytes appended after a checkpoint remain visible blockers", () => {
  const directory = mkdtempSync(resolve(tmpdir(), "are-reasoning-visible-tail-"));
  const path = resolve(directory, "reasoning.jsonl");
  try {
    const sink = createAppendOnlyFileReasoningStateSink({path});
    const ledger = createReasoningStateLedger({ledger_id: "reasoning:visible", sink});
    const event = ledger.append({event_kind: "request-interpreted", content: {request_id: "visible:1"}});
    const epoch = ledger.seal({event_digests: [event.event.event_digest]});
    ledger.checkpoint({checkpoint_kind: "manual", epoch: epoch.value});
    ledger.close();
    appendFileSync(path, "\n");
    assert.deepEqual(verifyReasoningStateLog(path).reason_codes, ["reasoning.log-blank-record"]);
  } finally {
    rmSync(directory, {recursive: true, force: true});
  }
});

test("a completed reasoning frontier seals one exact epoch and after-completion checkpoint", () => {
  const ledger = createReasoningStateLedger({ledger_id: "reasoning:frontier"});
  const input = {
    frontier_key: "codex-turn:thread-1:turn-1",
    subject_digest: "completion:1",
    consumer_ref: "codex:human-chat",
    request_ref: "turn:turn-1",
    context_envelope_digest: "context:1",
    prior_reasoning_epoch_digest: "epoch:request:1",
    state: {kind: "codex-turn-completion", semantic: {disposition: "not-applicable"}, continuation: {directive_kind: "complete"}},
  };
  const sealed = sealReasoningStateFrontier(ledger, input);
  assert.equal(sealed.ok, true);
  assert.equal(sealed.checkpoint.checkpoint_kind, "after-turn-completion");
  assert.equal(sealed.checkpoint.subject_digest, input.subject_digest);
  assert.equal(verifyReasoningStateFrontier(sealed.frontier).ok, true);
  assert.equal(getReasoningStateFrontier(ledger, input.frontier_key).frontier.frontier_digest, sealed.frontier.frontier_digest);
  assert.equal(listReasoningStateFrontiers(ledger).length, 1);
  const duplicate = ledger.sealFrontier(input);
  assert.equal(duplicate.disposition, "duplicate");
  assert.equal(ledger.inspect().frontier_count, 1);
  const conflict = ledger.sealFrontier({...input, state: {kind: "changed"}});
  assert.deepEqual(conflict.reason_codes, ["reasoning.frontier-idempotency-conflict"]);
});

test("checkpointed completion frontiers recover exactly and rebuild their disposable index", () => {
  const directory = mkdtempSync(resolve(tmpdir(), "are-reasoning-frontier-recovery-"));
  const path = resolve(directory, "reasoning.jsonl");
  try {
    const ledger = createReasoningStateLedger({ledger_id: "reasoning:frontier-recover", sink: createAppendOnlyFileReasoningStateSink({path})});
    const sealed = ledger.sealFrontier({
      frontier_key: "codex-turn:thread-r:turn-r",
      subject_digest: "completion:r",
      consumer_ref: "codex:human-chat",
      request_ref: "turn:turn-r",
      state: {kind: "codex-turn-completion", semantic: {evaluator_calls: 0}, continuation: {directive_kind: "gate"}},
    });
    ledger.close();
    const verified = verifyReasoningStateLog(path, {expected_ledger_id: "reasoning:frontier-recover"});
    assert.equal(verified.ok, true);
    assert.equal(verified.value.index.frontier_count, 1);
    assert.deepEqual(verified.value.index.frontier_digests, [sealed.frontier.frontier_digest]);
    const recovered = recoverReasoningStateLedger({path, ledger_id: "reasoning:frontier-recover"});
    assert.equal(recovered.ok, true);
    const restored = recovered.ledger.getFrontier("codex-turn:thread-r:turn-r");
    assert.equal(restored.disposition, "found");
    assert.deepEqual(restored.frontier, sealed.frontier);
    assert.deepEqual(recovered.ledger.replay(restored.epoch).value.events, [restored.event]);
    recovered.ledger.close();
  } finally {
    rmSync(directory, {recursive: true, force: true});
  }
});

test("a frontier event without its exact completion checkpoint is not recoverable", () => {
  const directory = mkdtempSync(resolve(tmpdir(), "are-reasoning-frontier-incomplete-"));
  const path = resolve(directory, "reasoning.jsonl");
  try {
    const ledger = createReasoningStateLedger({ledger_id: "reasoning:frontier-incomplete", sink: createAppendOnlyFileReasoningStateSink({path})});
    const appended = ledger.append({
      event_kind: "reasoning-frontier-sealed",
      content: {
        schema_version: "are.reasoning-state-frontier/v1",
        ledger_id: "reasoning:frontier-incomplete",
        frontier_key: "codex-turn:thread-i:turn-i",
        subject_digest: "completion:i",
        consumer_ref: null,
        request_ref: null,
        context_envelope_digest: null,
        prior_reasoning_epoch_digest: null,
        state: {kind: "incomplete"},
        authority_effect: "none",
        frontier_id: "invalid",
        frontier_digest: "invalid",
      },
    });
    const epoch = ledger.seal({event_digests: [appended.event.event_digest]});
    ledger.checkpoint({checkpoint_kind: "manual", epoch: epoch.value});
    ledger.close();
    const before = readFileSync(path);
    assert.equal(verifyReasoningStateLog(path).reason_codes.includes("reasoning.log-frontier-invalid"), true);
    assert.equal(recoverReasoningStateLedger({path, ledger_id: "reasoning:frontier-incomplete"}).ok, false);
    assert.deepEqual(readFileSync(path), before);
  } finally {
    rmSync(directory, {recursive: true, force: true});
  }
});
