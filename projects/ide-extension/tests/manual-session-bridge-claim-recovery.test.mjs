import assert from 'node:assert/strict';
import { mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { appendEvent as appendAuditEvent, readEvents } from '../src/kernel/audit.mjs';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));

function listen(server) {
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server.address().port)));
}

function close(server) {
  return new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}

async function start(stateDir, options = {}) {
  const server = createServer({ rootDir: projectRoot, stateDir, ...options });
  await server.ready;
  const port = await listen(server);
  return { server, base: `http://127.0.0.1:${port}` };
}

async function withServer(run, options = {}) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-bridge-claim-'));
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

async function prepareReady(base, suffix = 'one') {
  const prepared = await postJson(base, '/api/envelopes/prepare', {
    task: `Execute private bridge task ${suffix}`,
    requested_skill: 'decision-gate',
    requested_grants: ['preview.read', 'skill.invoke'],
    context_refs: ['projects/ide-extension/SPEC.md']
  });
  await postJson(base, `/api/approvals/${prepared.body.approval.approval_id}/approve`);
  await postJson(base, `/api/bridge/requests/${prepared.body.envelope.envelope_id}/ready`);
  return prepared.body;
}

function claimBody(envelopeId, sessionRef = 'session-local-one') {
  return {
    schema_version: '2',
    envelope_id: envelopeId,
    agent_ref: 'codex.current-session',
    session_ref: sessionRef,
    assurance: 'unattested'
  };
}

function claim(base, envelopeId, sessionRef) {
  return postJson(
    base,
    `/api/bridge/requests/${envelopeId}/claim`,
    claimBody(envelopeId, sessionRef)
  );
}

function interrupt(base, claimRecord, overrides = {}) {
  return postJson(base, `/api/bridge/claims/${claimRecord.claim_id}/interrupt`, {
    schema_version: '2',
    claim_id: claimRecord.claim_id,
    envelope_id: claimRecord.envelope_id,
    session_ref: claimRecord.session_ref,
    assurance: 'unattested',
    reason: 'Active session stopped before posting a result.',
    ...overrides
  });
}

test('reveals the execution packet only after durable atomic claim', async () => {
  await withServer(async ({ base, stateDir }) => {
    const prepared = await prepareReady(base);
    const preclaim = await requestJson(
      base,
      '/api/bridge/requests/ready?agent_ref=codex.current-session'
    );
    assert.equal(JSON.stringify(preclaim.body).includes('decision-gate'), false);

    const claimed = await claim(base, prepared.envelope.envelope_id, 'session-local-one');
    assert.equal(claimed.response.status, 201);
    assert.equal(claimed.body.claim.assurance, 'unattested');
    assert.equal(claimed.body.execution.requested_skill, 'decision-gate');
    assert.match(claimed.body.execution.task, /private bridge task/);

    const events = await readEvents(path.join(stateDir, 'events.jsonl'));
    assert.equal(events.at(-1).event_type, 'bridge.claimed');
    assert.equal(events.at(-1).artifact_refs.length, 1);
    assert.deepEqual(
      (await requestJson(base, '/api/bridge/requests/ready?agent_ref=codex.current-session')).body,
      { request: null }
    );
  });
});

test('permits one concurrent claim and discloses nothing to losers', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepareReady(base, 'race');
    const attempts = await Promise.all(
      Array.from({ length: 10 }, (_, index) => (
        claim(base, prepared.envelope.envelope_id, `session-race-${index}`)
      ))
    );
    const winners = attempts.filter(({ response }) => response.status === 201);
    const losers = attempts.filter(({ response }) => response.status === 409);
    assert.equal(winners.length, 1);
    assert.equal(losers.length, 9);
    for (const loser of losers) {
      const serialized = JSON.stringify(loser.body);
      assert.equal(serialized.includes('decision-gate'), false);
      assert.equal(serialized.includes('private bridge task'), false);
      assert.equal(Object.hasOwn(loser.body, 'execution'), false);
    }
    const state = await requestJson(base, '/api/state');
    assert.equal(state.body.bridge.claim_order.length, 1);
  });
});

test('binds interruption to the claimant and requires operator release plus retarget', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepareReady(base, 'recovery');
    const claimed = await claim(base, prepared.envelope.envelope_id, 'session-recovery');

    const wrongSession = await interrupt(base, claimed.body.claim, {
      session_ref: 'session-wrong'
    });
    assert.equal(wrongSession.response.status, 409);
    assert.equal(wrongSession.body.error, 'claim_binding_mismatch');

    const interrupted = await interrupt(base, claimed.body.claim);
    assert.equal(interrupted.response.status, 200);
    assert.equal(interrupted.body.claim.state, 'interrupted');

    const sessionRelease = await postJson(
      base,
      `/api/bridge/claims/${claimed.body.claim.claim_id}/release`,
      { session_ref: 'session-recovery', reason: 'self release' }
    );
    assert.equal(sessionRelease.response.status, 400);

    const released = await postJson(
      base,
      `/api/bridge/claims/${claimed.body.claim.claim_id}/release`,
      { reason: 'Operator confirmed a read-only retry.' }
    );
    assert.equal(released.response.status, 200);
    assert.equal(released.body.envelope.state, 'approved');
    assert.equal(released.body.claim.state, 'released');

    const premature = await claim(base, prepared.envelope.envelope_id, 'session-retry');
    assert.equal(premature.response.status, 409);
    assert.equal(premature.body.error, 'not_ready_target');
    await postJson(base, `/api/bridge/requests/${prepared.envelope.envelope_id}/ready`);
    const retried = await claim(base, prepared.envelope.envelope_id, 'session-retry');
    assert.equal(retried.response.status, 201);
    assert.notEqual(retried.body.claim.claim_id, claimed.body.claim.claim_id);

    const state = await requestJson(base, '/api/state');
    assert.deepEqual(state.body.bridge.claim_order, [
      claimed.body.claim.claim_id,
      retried.body.claim.claim_id
    ]);
    assert.equal(
      state.body.envelopes[prepared.envelope.envelope_id].authorization_receipt_id,
      released.body.envelope.authorization_receipt_id
    );
  });
});

test('restarts deterministically in claimed and interrupted states', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-claim-restart-'));
  let running;
  try {
    running = await start(stateDir);
    const prepared = await prepareReady(running.base, 'restart');
    const claimed = await claim(running.base, prepared.envelope.envelope_id, 'session-restart');
    await close(running.server);
    running = await start(stateDir);
    let status = await requestJson(running.base, `/api/bridge/claims/${claimed.body.claim.claim_id}`);
    assert.equal(status.body.claim.state, 'claimed');

    await interrupt(running.base, claimed.body.claim);
    await close(running.server);
    running = await start(stateDir);
    status = await requestJson(running.base, `/api/bridge/claims/${claimed.body.claim.claim_id}`);
    assert.equal(status.body.claim.state, 'interrupted');
    const state = await requestJson(running.base, '/api/state');
    assert.equal(state.body.envelopes[prepared.envelope.envelope_id].state, 'interrupted');
  } finally {
    if (running?.server.listening) await close(running.server);
    await rm(stateDir, { recursive: true, force: true });
  }
});

test('claim append failure preserves the ready target and leaks no packet', async () => {
  let appendCount = 0;
  const appendEvent = async (...args) => {
    appendCount += 1;
    if (appendCount === 4) {
      const error = new Error('injected claim append failure');
      error.code = 'EIO';
      throw error;
    }
    return appendAuditEvent(...args);
  };

  await withServer(async ({ base }) => {
    const prepared = await prepareReady(base, 'append-failure');
    const failed = await claim(base, prepared.envelope.envelope_id, 'session-failure');
    assert.equal(failed.response.status, 500);
    assert.equal(Object.hasOwn(failed.body, 'execution'), false);
    const readyState = await requestJson(
      base,
      '/api/bridge/requests/ready?agent_ref=codex.current-session'
    );
    assert.equal(readyState.body.request.request_handle, prepared.envelope.envelope_id);
    const state = await requestJson(base, '/api/state');
    assert.equal(state.body.bridge.claim_order.length, 0);
    assert.equal(state.body.reconciliation.orphan_artifacts.length, 1);
  }, { appendEvent });
});
