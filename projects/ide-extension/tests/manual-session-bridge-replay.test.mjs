import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import {
  BRIDGE_EVENT_VERSION,
  EVENT_VERSION,
  projectionChecksum,
  reduceEvents
} from '../src/kernel/projector.mjs';
import { createProjectionStore } from '../src/kernel/storage.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const schemaFixtures = path.join(projectRoot, 'tests/fixtures/schemas');
const eventFixtures = path.join(projectRoot, 'tests/fixtures/events');
const operator = { kind: 'local_operator_action', assurance: 'unattested' };

async function json(file) {
  return JSON.parse(await readFile(path.join(schemaFixtures, file), 'utf8'));
}

async function v1Events() {
  const raw = await readFile(path.join(eventFixtures, 'v1-lifecycle.jsonl'), 'utf8');
  return raw.trim().split('\n').map(JSON.parse);
}

function clone(value) {
  return structuredClone(value);
}

function suffixFixture(value, suffix) {
  return JSON.parse(JSON.stringify(value).replaceAll('-fixture', `-fixture-${suffix}`));
}

async function buildTerminalEvents(suffix = 'one') {
  const authorizedEnvelope = suffixFixture(
    await json('agent-envelope.valid.bridge.json'),
    suffix
  );
  const authorizedApproval = suffixFixture(
    await json('approval-record.valid.bridge.json'),
    suffix
  );
  const authorizationReceipt = suffixFixture(
    await json('receipt.valid.authorization.json'),
    suffix
  );
  const executionReceipt = suffixFixture(
    await json('receipt.valid.execution.json'),
    suffix
  );
  const result = suffixFixture(await json('bridge-result-request.valid.json'), suffix);

  const preparedEnvelope = clone(authorizedEnvelope);
  preparedEnvelope.state = 'awaiting_approval';
  preparedEnvelope.authorization_receipt_id = null;
  preparedEnvelope.receipts = [];
  preparedEnvelope.approval.actor = null;
  preparedEnvelope.approval.approved_at = null;

  const preparedApproval = clone(authorizedApproval);
  preparedApproval.state = 'pending';
  preparedApproval.actor = null;
  preparedApproval.authorized_at = null;
  preparedApproval.authorization_receipt_id = null;

  const prepared = {
    event_version: BRIDGE_EVENT_VERSION,
    event_id: `event-v2-${suffix}-prepared`,
    event_type: 'envelope.prepared',
    envelope: preparedEnvelope,
    approval: preparedApproval,
    created_at: '2026-07-11T23:59:00.000Z'
  };
  const authorized = {
    event_version: BRIDGE_EVENT_VERSION,
    event_id: `event-v2-${suffix}-authorized`,
    event_type: 'approval.granted',
    envelope: authorizedEnvelope,
    approval: authorizedApproval,
    receipt: authorizationReceipt,
    artifact_refs: [`artifact-auth-${suffix}`],
    created_at: '2026-07-12T00:00:00.000Z'
  };

  const readyEnvelope = clone(authorizedEnvelope);
  readyEnvelope.state = 'ready_for_poll';
  const targeted = {
    event_version: BRIDGE_EVENT_VERSION,
    event_id: `event-v2-${suffix}-targeted`,
    event_type: 'bridge.target_selected',
    envelope: readyEnvelope,
    approval_id: authorizedApproval.approval_id,
    actor: operator,
    created_at: '2026-07-12T00:00:30.000Z'
  };

  const claim = {
    schema_version: '2',
    claim_id: executionReceipt.claim_id,
    claim_attempt_id: executionReceipt.claim_attempt_id,
    envelope_id: authorizedEnvelope.envelope_id,
    run_id: authorizedEnvelope.run_id,
    approval_id: authorizedApproval.approval_id,
    agent_ref: executionReceipt.agent_ref,
    session_ref: executionReceipt.session_ref,
    assurance: 'unattested',
    state: 'claimed',
    claimed_at: executionReceipt.claimed_at,
    interrupted_at: null,
    interruption_reason: null,
    released_at: null,
    release_reason: null,
    result_id: null
  };
  const claimedEnvelope = clone(readyEnvelope);
  claimedEnvelope.state = 'claimed';
  claimedEnvelope.claim_id = claim.claim_id;
  const claimed = {
    event_version: BRIDGE_EVENT_VERSION,
    event_id: `event-v2-${suffix}-claimed`,
    event_type: 'bridge.claimed',
    envelope: claimedEnvelope,
    claim,
    artifact_refs: [`artifact-${claim.claim_id}-claim`],
    created_at: claim.claimed_at
  };

  result.result_id = `result-bridge-fixture-${suffix}`;
  result.result_at = executionReceipt.result_at;
  const terminalEnvelope = clone(claimedEnvelope);
  terminalEnvelope.state = result.status;
  terminalEnvelope.result_id = result.result_id;
  terminalEnvelope.receipts = [authorizationReceipt.receipt_id, executionReceipt.receipt_id];
  terminalEnvelope.approval.consumed_at = result.result_at;
  const consumedApproval = clone(authorizedApproval);
  consumedApproval.state = 'consumed';
  consumedApproval.consumed_at = result.result_at;
  const completedClaim = clone(claim);
  completedClaim.state = 'completed';
  completedClaim.result_id = result.result_id;
  const recorded = {
    event_version: BRIDGE_EVENT_VERSION,
    event_id: `event-v2-${suffix}-result`,
    event_type: 'bridge.result_recorded',
    envelope: terminalEnvelope,
    approval: consumedApproval,
    claim: completedClaim,
    result,
    receipt: executionReceipt,
    artifact_refs: [
      executionReceipt.before_ref,
      executionReceipt.after_ref,
      executionReceipt.result_ref
    ],
    created_at: result.result_at
  };

  return { prepared, authorized, targeted, claimed, recorded };
}

test('keeps the checked-in v1 replay projection field-for-field unchanged', async () => {
  const expected = JSON.parse(
    await readFile(path.join(eventFixtures, 'v1-lifecycle.projection.json'), 'utf8')
  );
  const events = await v1Events();

  assert.equal(EVENT_VERSION, 1);
  assert.equal(BRIDGE_EVENT_VERSION, 2);
  assert.deepEqual(reduceEvents(events), expected);
  assert.equal(Object.hasOwn(reduceEvents(events), 'bridge'), false);
});

test('replays the complete v2 authorization to terminal-result path', async () => {
  const stages = await buildTerminalEvents();
  const events = Object.values(stages);
  const projection = reduceEvents(events);
  const envelope = stages.recorded.envelope;

  assert.equal(projection.envelopes[envelope.envelope_id].state, 'passed');
  assert.equal(projection.approvals[stages.recorded.approval.approval_id].state, 'consumed');
  assert.equal(projection.bridge.ready_target_envelope_id, null);
  assert.deepEqual(projection.bridge.claim_order, [stages.claimed.claim.claim_id]);
  assert.equal(projection.bridge.claims[stages.claimed.claim.claim_id].state, 'completed');
  assert.equal(
    projection.bridge.claims[stages.claimed.claim.claim_id].agent_ref,
    'openrouter.local-session'
  );
  assert.equal(projection.bridge.results[stages.recorded.result.result_id].status, 'passed');
  assert.equal(
    projection.receipts.find((receipt) => receipt.receipt_kind === 'skill.execution').agent_ref,
    'openrouter.local-session'
  );
  assert.deepEqual(
    projection.receipts.map((receipt) => receipt.receipt_kind),
    ['authorization.receipt', 'skill.execution']
  );
});

test('preserves interrupted attempts and requires explicit operator release before retry', async () => {
  const stages = await buildTerminalEvents('recovery');
  const events = [stages.prepared, stages.authorized, stages.targeted, stages.claimed];
  const interruptedEnvelope = clone(stages.claimed.envelope);
  interruptedEnvelope.state = 'interrupted';
  const interruptedClaim = clone(stages.claimed.claim);
  interruptedClaim.state = 'interrupted';
  interruptedClaim.interrupted_at = '2026-07-12T00:01:20.000Z';
  interruptedClaim.interruption_reason = 'Session stopped before result.';
  events.push({
    event_version: 2,
    event_id: 'event-v2-recovery-interrupted',
    event_type: 'bridge.interrupted',
    envelope: interruptedEnvelope,
    claim: interruptedClaim,
    reason: interruptedClaim.interruption_reason,
    artifact_refs: ['artifact-recovery-interrupt'],
    created_at: interruptedClaim.interrupted_at
  });

  const releasedEnvelope = clone(interruptedEnvelope);
  releasedEnvelope.state = 'approved';
  releasedEnvelope.claim_id = null;
  const releasedClaim = clone(interruptedClaim);
  releasedClaim.state = 'released';
  releasedClaim.released_at = '2026-07-12T00:01:30.000Z';
  releasedClaim.release_reason = 'Operator approved read-only retry.';
  events.push({
    event_version: 2,
    event_id: 'event-v2-recovery-released',
    event_type: 'bridge.claim_released',
    envelope: releasedEnvelope,
    claim: releasedClaim,
    actor: operator,
    reason: releasedClaim.release_reason,
    artifact_refs: ['artifact-recovery-release'],
    created_at: releasedClaim.released_at
  });

  const readyAgain = clone(releasedEnvelope);
  readyAgain.state = 'ready_for_poll';
  events.push({
    event_version: 2,
    event_id: 'event-v2-recovery-retargeted',
    event_type: 'bridge.target_selected',
    envelope: readyAgain,
    approval_id: stages.authorized.approval.approval_id,
    actor: operator,
    created_at: '2026-07-12T00:01:40.000Z'
  });

  const retryClaim = clone(stages.claimed.claim);
  retryClaim.claim_id = 'claim-bridge-fixture-recovery-retry';
  retryClaim.claim_attempt_id = 'attempt-bridge-fixture-recovery-2';
  retryClaim.claimed_at = '2026-07-12T00:01:50.000Z';
  const retryEnvelope = clone(readyAgain);
  retryEnvelope.state = 'claimed';
  retryEnvelope.claim_id = retryClaim.claim_id;
  events.push({
    event_version: 2,
    event_id: 'event-v2-recovery-reclaimed',
    event_type: 'bridge.claimed',
    envelope: retryEnvelope,
    claim: retryClaim,
    artifact_refs: ['artifact-recovery-retry-claim'],
    created_at: retryClaim.claimed_at
  });

  const projection = reduceEvents(events);
  assert.deepEqual(
    projection.bridge.claim_order,
    [stages.claimed.claim.claim_id, retryClaim.claim_id]
  );
  assert.equal(projection.bridge.claims[stages.claimed.claim.claim_id].state, 'released');
  assert.equal(projection.bridge.claims[retryClaim.claim_id].state, 'claimed');
  assert.equal(projection.envelopes[retryEnvelope.envelope_id].authorization_receipt_id,
    stages.authorized.receipt.receipt_id);
});

test('replays pending rejection and authorized revocation without fake execution evidence', async () => {
  const rejectedStages = await buildTerminalEvents('rejected');
  const rejectedEnvelope = clone(rejectedStages.prepared.envelope);
  rejectedEnvelope.state = 'blocked';
  rejectedEnvelope.approval.actor = operator;
  rejectedEnvelope.approval.rejected_at = '2026-07-12T00:00:10.000Z';
  const rejectedApproval = clone(rejectedStages.prepared.approval);
  rejectedApproval.state = 'rejected';
  rejectedApproval.actor = operator;
  rejectedApproval.rejected_at = rejectedEnvelope.approval.rejected_at;
  const rejectedProjection = reduceEvents([
    rejectedStages.prepared,
    {
      event_version: 2,
      event_id: 'event-v2-rejected-disposition',
      event_type: 'approval.rejected',
      envelope: rejectedEnvelope,
      approval: rejectedApproval,
      created_at: rejectedEnvelope.approval.rejected_at
    }
  ]);
  assert.equal(rejectedProjection.envelopes[rejectedEnvelope.envelope_id].state, 'blocked');
  assert.equal(rejectedProjection.receipts.length, 0);

  const revokedStages = await buildTerminalEvents('revoked');
  const revokedEnvelope = clone(revokedStages.targeted.envelope);
  revokedEnvelope.state = 'blocked';
  revokedEnvelope.approval.revoked_at = '2026-07-12T00:00:40.000Z';
  const revokedApproval = clone(revokedStages.authorized.approval);
  revokedApproval.state = 'revoked';
  revokedApproval.revoked_at = revokedEnvelope.approval.revoked_at;
  revokedApproval.rejection_reason = 'Operator revoked the ready request.';
  const revokedProjection = reduceEvents([
    revokedStages.prepared,
    revokedStages.authorized,
    revokedStages.targeted,
    {
      event_version: 2,
      event_id: 'event-v2-revoked-disposition',
      event_type: 'approval.revoked',
      envelope: revokedEnvelope,
      approval: revokedApproval,
      actor: operator,
      reason: revokedApproval.rejection_reason,
      created_at: revokedApproval.revoked_at
    }
  ]);
  assert.equal(revokedProjection.bridge.ready_target_envelope_id, null);
  assert.equal(revokedProjection.receipts.length, 1);
  assert.equal(revokedProjection.receipts[0].receipt_kind, 'authorization.receipt');
});

test('replays mixed v1/v2 history without mutating source events', async () => {
  const legacy = await v1Events();
  const bridge = Object.values(await buildTerminalEvents('mixed'));
  const events = [...legacy, ...bridge];
  const before = JSON.stringify(events);
  const projection = reduceEvents(events);

  assert.equal(JSON.stringify(events), before);
  assert.equal(projection.receipts.length, 3);
  assert.equal(projection.envelopes['env-v1-fixture'].state, 'passed');
  assert.equal(projection.envelopes['env-bridge-fixture-mixed'].state, 'passed');
});

test('fails closed on version, duplicate, singleton, stale, and terminal replay errors', async () => {
  const one = await buildTerminalEvents('hostile-one');
  const two = await buildTerminalEvents('hostile-two');

  assert.throws(
    () => reduceEvents([{ ...one.prepared, event_version: 5 }]),
    /unsupported event_version 5/
  );
  assert.throws(
    () => reduceEvents([one.prepared, clone(one.prepared)]),
    /duplicate event_id/
  );
  assert.throws(
    () => reduceEvents([
      one.prepared,
      one.authorized,
      two.prepared,
      two.authorized,
      one.targeted,
      two.targeted
    ]),
    /ready target already exists/
  );

  const staleClear = {
    event_version: 2,
    event_id: 'event-v2-hostile-stale-clear',
    event_type: 'bridge.target_cleared',
    envelope: { ...clone(one.claimed.envelope), state: 'approved', claim_id: null },
    approval_id: one.authorized.approval.approval_id,
    actor: operator,
    created_at: '2026-07-12T00:03:00.000Z'
  };
  assert.throws(
    () => reduceEvents([one.prepared, one.authorized, one.targeted, one.claimed, staleClear]),
    /envelope must be ready_for_poll/
  );

  assert.throws(
    () => reduceEvents([
      ...Object.values(one),
      { ...clone(one.recorded), event_id: 'event-v2-hostile-result-replay' }
    ]),
    /result envelope is not claimed/
  );
});

test('storage restart rebuilds the same mixed projection and checksum', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-v2-replay-'));
  const eventsFile = path.join(stateDir, 'events.jsonl');
  const workbenchFile = path.join(stateDir, 'workbench.json');
  const artifactDir = path.join(stateDir, 'artifacts');

  try {
    const events = [...await v1Events(), ...Object.values(await buildTerminalEvents('restart'))];
    await writeFile(eventsFile, `${events.map((event) => JSON.stringify(event)).join('\n')}\n`, 'utf8');
    const store = createProjectionStore({ eventsFile, workbenchFile, artifactDir });
    const first = await store.reconcile();
    await rm(workbenchFile);
    const second = await store.reconcile();

    assert.deepEqual(second.projection, first.projection);
    assert.equal(second.projection_checksum, first.projection_checksum);
    assert.equal(second.projection_checksum, projectionChecksum(reduceEvents(events)));
    assert.equal(second.repaired, true);
  } finally {
    await rm(stateDir, { recursive: true, force: true });
  }
});
