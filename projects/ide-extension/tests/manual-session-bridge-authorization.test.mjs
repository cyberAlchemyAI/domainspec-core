import assert from 'node:assert/strict';
import { mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { readEvents } from '../src/kernel/audit.mjs';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));

function listen(server) {
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve(server.address().port));
  });
}

function close(server) {
  return new Promise((resolve, reject) => {
    server.close((error) => (error ? reject(error) : resolve()));
  });
}

async function start(stateDir, options = {}) {
  const server = createServer({ rootDir: projectRoot, stateDir, ...options });
  await server.ready;
  const port = await listen(server);
  return { server, base: `http://127.0.0.1:${port}` };
}

async function withServer(run, options = {}) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-bridge-auth-'));
  const running = await start(stateDir, options);
  try {
    await run({ ...running, stateDir });
  } finally {
    if (running.server.listening) await close(running.server);
    await rm(stateDir, { recursive: true, force: true });
  }
}

async function requestJson(base, route, options = {}) {
  const response = await fetch(`${base}${route}`, {
    ...options,
    headers: { 'content-type': 'application/json', ...(options.headers || {}) }
  });
  return { response, body: JSON.parse(await response.text()) };
}

function postJson(base, route, body = {}) {
  return requestJson(base, route, { method: 'POST', body: JSON.stringify(body) });
}

function prepare(base, suffix = 'one') {
  return postJson(base, '/api/envelopes/prepare', {
    task: `Review bridge request ${suffix}`,
    requested_skill: 'decision-gate',
    requested_grants: ['skill.invoke', 'preview.read'],
    context_refs: ['projects/ide-extension/SPEC.md']
  });
}

function approve(base, approvalId, body = {}) {
  return postJson(base, `/api/approvals/${approvalId}/approve`, body);
}

function reject(base, approvalId, reason = 'Operator cancelled the request.') {
  return postJson(base, `/api/approvals/${approvalId}/reject`, { reason });
}

function target(base, envelopeId, action, body = {}) {
  return postJson(base, `/api/bridge/requests/${envelopeId}/${action}`, body);
}

function ready(base) {
  return requestJson(base, '/api/bridge/requests/ready');
}

test('approval creates authorization evidence without claiming execution', async () => {
  await withServer(async ({ base, stateDir }) => {
    const prepared = await prepare(base);
    assert.equal(prepared.response.status, 201);
    assert.equal(prepared.body.envelope.schema_version, '2');
    assert.equal(prepared.body.envelope.state, 'awaiting_approval');

    const authorized = await approve(base, prepared.body.approval.approval_id);
    assert.equal(authorized.response.status, 201);
    assert.equal(authorized.body.envelope.state, 'approved');
    assert.equal(authorized.body.approval.state, 'authorized');
    assert.equal(authorized.body.receipt.receipt_kind, 'authorization.receipt');
    assert.equal(Object.hasOwn(authorized.body.receipt, 'status'), false);
    assert.equal(Object.hasOwn(authorized.body.receipt, 'summary'), false);
    assert.equal(authorized.body.receipt.actor.assurance, 'unattested');

    const state = await requestJson(base, '/api/state');
    assert.equal(state.body.receipts.length, 1);
    assert.equal(state.body.receipts[0].receipt_kind, 'authorization.receipt');
    assert.equal(state.body.approvals[prepared.body.approval.approval_id].state, 'authorized');

    for (const kind of ['before', 'after', 'receipt']) {
      const evidence = await requestJson(
        base,
        `/api/receipts/${authorized.body.receipt.receipt_id}/evidence/${kind}`
      );
      assert.equal(evidence.response.status, 200, kind);
    }

    const events = await readEvents(path.join(stateDir, 'events.jsonl'));
    assert.deepEqual(events.map((event) => [event.event_version, event.event_type]), [
      [2, 'envelope.prepared'],
      [2, 'approval.granted']
    ]);
  });
});

test('serializes duplicate authorization and mints exactly one receipt', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepare(base, 'race');
    const attempts = await Promise.all(
      Array.from({ length: 8 }, () => approve(base, prepared.body.approval.approval_id))
    );
    assert.equal(attempts.filter(({ response }) => response.status === 201).length, 1);
    assert.equal(attempts.filter(({ response }) => response.status === 409).length, 7);
    const state = await requestJson(base, '/api/state');
    assert.equal(state.body.receipts.length, 1);
    assert.equal(state.body.event_count, 2);
  });
});

test('keeps one ready target private and stable across restart', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-target-restart-'));
  let running;
  try {
    running = await start(stateDir);
    const first = await prepare(running.base, 'first');
    const second = await prepare(running.base, 'second');
    await approve(running.base, first.body.approval.approval_id);
    await approve(running.base, second.body.approval.approval_id);

    const selected = await target(running.base, first.body.envelope.envelope_id, 'ready');
    assert.equal(selected.response.status, 201);
    const conflict = await target(running.base, second.body.envelope.envelope_id, 'ready');
    assert.equal(conflict.response.status, 409);
    assert.equal(conflict.body.error, 'ready_target_exists');

    const beforeRestart = await ready(running.base);
    assert.equal(beforeRestart.response.status, 200);
    const ignoredSelector = await requestJson(
      running.base,
      '/api/bridge/requests/ready?agent_ref=openrouter.local-session'
    );
    assert.deepEqual(ignoredSelector.body, beforeRestart.body);
    assert.deepEqual(Object.keys(beforeRestart.body.request).sort(), [
      'agent_ref',
      'assurance',
      'authorized_at',
      'created_at',
      'effect_profile',
      'request_handle',
      'schema_version',
      'selected_at',
      'state'
    ]);
    const serialized = JSON.stringify(beforeRestart.body);
    for (const secret of ['decision-gate', 'Review bridge request', 'requested_skill', 'task_sha256']) {
      assert.equal(serialized.includes(secret), false, secret);
    }

    await close(running.server);
    running = await start(stateDir);
    const afterRestart = await ready(running.base);
    assert.deepEqual(afterRestart.body, beforeRestart.body);

    const cleared = await target(running.base, first.body.envelope.envelope_id, 'unready');
    assert.equal(cleared.response.status, 200);
    assert.equal(cleared.body.envelope.state, 'approved');
    assert.deepEqual((await ready(running.base)).body, { request: null });
  } finally {
    if (running?.server.listening) await close(running.server);
    await rm(stateDir, { recursive: true, force: true });
  }
});

test('rejects stale, caller-attributed, and legacy target actions without writes', async () => {
  await withServer(async ({ base }) => {
    const bridge = await prepare(base, 'hostile');
    await approve(base, bridge.body.approval.approval_id);
    const before = await requestJson(base, '/api/state');

    const callerActor = await target(base, bridge.body.envelope.envelope_id, 'ready', {
      actor: { kind: 'local_operator_action', assurance: 'unattested' }
    });
    assert.equal(callerActor.response.status, 400);
    const stale = await target(base, bridge.body.envelope.envelope_id, 'unready');
    assert.equal(stale.response.status, 409);
    assert.equal(stale.body.error, 'not_ready_target');

    const legacy = await postJson(base, '/api/envelopes/prepare', { task: 'Legacy target' });
    const legacyTarget = await target(base, legacy.body.envelope.envelope_id, 'ready');
    assert.equal(legacyTarget.response.status, 409);
    assert.equal(legacyTarget.body.error, 'not_bridge_request');

    const after = await requestJson(base, '/api/state');
    assert.equal(after.body.event_count, before.body.event_count + 1);
    assert.equal(after.body.bridge.ready_target_envelope_id, null);
  });
});

test('rejects pending requests and revokes approved or ready requests truthfully', async () => {
  await withServer(async ({ base }) => {
    const pending = await prepare(base, 'pending-reject');
    const rejected = await reject(base, pending.body.approval.approval_id);
    assert.equal(rejected.response.status, 200);
    assert.equal(rejected.body.approval.state, 'rejected');
    assert.equal(rejected.body.envelope.state, 'blocked');

    const approved = await prepare(base, 'approved-revoke');
    const authorization = await approve(base, approved.body.approval.approval_id);
    const revoked = await reject(base, approved.body.approval.approval_id);
    assert.equal(revoked.response.status, 200);
    assert.equal(revoked.body.approval.state, 'revoked');
    assert.deepEqual(revoked.body.envelope.receipts, [authorization.body.receipt.receipt_id]);

    const selected = await prepare(base, 'ready-revoke');
    await approve(base, selected.body.approval.approval_id);
    await target(base, selected.body.envelope.envelope_id, 'ready');
    const readyRevoked = await reject(base, selected.body.approval.approval_id);
    assert.equal(readyRevoked.body.approval.state, 'revoked');
    assert.deepEqual((await ready(base)).body, { request: null });

    const state = await requestJson(base, '/api/state');
    assert.equal(state.body.receipts.length, 2);
    assert.ok(state.body.receipts.every((receipt) => receipt.receipt_kind === 'authorization.receipt'));
  });
});

test('requires task and skill for the bridge profile before persistence', async () => {
  await withServer(async ({ base }) => {
    for (const body of [
      { requested_grants: ['preview.read', 'skill.invoke'] },
      { task: 'Missing skill', requested_grants: ['preview.read', 'skill.invoke'] },
      { task: '   ', requested_skill: 'decision-gate', requested_grants: ['preview.read', 'skill.invoke'] }
    ]) {
      const response = await postJson(base, '/api/envelopes/prepare', body);
      assert.equal(response.response.status, 400);
      assert.equal(response.body.error, 'invalid_request');
    }
    assert.equal((await requestJson(base, '/api/state')).body.event_count, 0);
  });
});

test('append failure leaves authorization uncommitted and reportable', async () => {
  let appendCount = 0;
  const appendEvent = async (...args) => {
    appendCount += 1;
    if (appendCount === 2) {
      const error = new Error('injected bridge authorization append failure');
      error.code = 'EIO';
      throw error;
    }
    const { appendEvent: append } = await import('../src/kernel/audit.mjs');
    return append(...args);
  };

  await withServer(async ({ base }) => {
    const prepared = await prepare(base, 'append-failure');
    const failed = await approve(base, prepared.body.approval.approval_id);
    assert.equal(failed.response.status, 500);
    const state = await requestJson(base, '/api/state');
    assert.equal(state.body.event_count, 1);
    assert.equal(state.body.receipts.length, 0);
    assert.equal(state.body.approvals[prepared.body.approval.approval_id].state, 'pending');
    assert.equal(state.body.reconciliation.orphan_artifacts.length, 3);
  }, { appendEvent });
});
