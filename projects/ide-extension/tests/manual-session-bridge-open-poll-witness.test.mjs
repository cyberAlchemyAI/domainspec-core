import assert from 'node:assert/strict';
import { mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const skillHash = 'c'.repeat(64);

function listen(server) {
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server.address().port)));
}

function close(server) {
  return new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}

async function start(stateDir) {
  const server = createServer({ rootDir: projectRoot, stateDir });
  await server.ready;
  const port = await listen(server);
  return { server, base: `http://127.0.0.1:${port}` };
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

async function prepareAvailable(base) {
  const prepared = await postJson(base, '/api/envelopes/prepare', {
    task: 'Open-poll witness hidden task',
    requested_skill: 'decision-gate',
    requested_grants: ['preview.read', 'skill.invoke'],
    context_refs: ['projects/ide-extension/SPEC.md']
  });
  await postJson(base, `/api/approvals/${prepared.body.approval.approval_id}/approve`);
  await postJson(base, `/api/bridge/requests/${prepared.body.envelope.envelope_id}/ready`);
  return prepared.body;
}

function claimInput(envelopeId, index) {
  return {
    schema_version: '2',
    envelope_id: envelopeId,
    agent_ref: 'openrouter.local-session',
    session_ref: `openrouter-witness-${index}`,
    assurance: 'unattested'
  };
}

function resultInput(packet) {
  const { claim, execution } = packet;
  return {
    schema_version: '2',
    claim_id: claim.claim_id,
    claim_attempt_id: claim.claim_attempt_id,
    envelope_id: claim.envelope_id,
    run_id: claim.run_id,
    approval_id: claim.approval_id,
    session_ref: claim.session_ref,
    assurance: claim.assurance,
    requested_skill: execution.requested_skill,
    skill_sha256: skillHash,
    status: 'passed',
    summary: 'Open-poll witness completed.',
    validation: ['queryless ready', 'one non-Codex claimant', 'claim-bound receipt'],
    evidence_refs: ['projects/ide-extension/SPEC.md']
  };
}

test('open singleton poll witness preserves non-Codex claim identity through result and restart', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-open-poll-witness-'));
  let running;

  try {
    running = await start(stateDir);
    const prepared = await prepareAvailable(running.base);
    const envelopeId = prepared.envelope.envelope_id;

    const ready = await requestJson(running.base, '/api/bridge/requests/ready');
    assert.equal(ready.response.status, 200);
    assert.equal(ready.body.request.request_handle, envelopeId);
    assert.equal(JSON.stringify(ready.body).includes('decision-gate'), false);
    assert.equal(JSON.stringify(ready.body).includes('Open-poll witness hidden task'), false);

    const readyWithIgnoredSelector = await requestJson(
      running.base,
      '/api/bridge/requests/ready?agent_ref=some.other-session'
    );
    assert.deepEqual(readyWithIgnoredSelector.body, ready.body);

    const attempts = await Promise.all(Array.from({ length: 10 }, (_, index) => (
      postJson(
        running.base,
        `/api/bridge/requests/${envelopeId}/claim`,
        claimInput(envelopeId, index)
      )
    )));
    const winners = attempts.filter(({ response }) => response.status === 201);
    const losers = attempts.filter(({ response }) => response.status === 409);

    assert.equal(winners.length, 1);
    assert.equal(losers.length, 9);
    for (const loser of losers) {
      const serialized = JSON.stringify(loser.body);
      assert.equal(serialized.includes('decision-gate'), false);
      assert.equal(serialized.includes('Open-poll witness hidden task'), false);
      assert.equal(Object.hasOwn(loser.body, 'execution'), false);
    }

    const packet = winners[0].body;
    assert.equal(packet.claim.agent_ref, 'openrouter.local-session');

    const admitted = await postJson(
      running.base,
      `/api/bridge/claims/${packet.claim.claim_id}/result`,
      resultInput(packet)
    );
    assert.equal(admitted.response.status, 201);
    assert.equal(admitted.body.receipt.agent_ref, 'openrouter.local-session');

    let state = await requestJson(running.base, '/api/state');
    assert.equal(state.body.bridge.claim_order.length, 1);
    assert.equal(state.body.bridge.claims[packet.claim.claim_id].state, 'completed');
    assert.equal(state.body.bridge.claims[packet.claim.claim_id].agent_ref, 'openrouter.local-session');
    assert.equal(
      state.body.receipts.find((receipt) => receipt.receipt_kind === 'skill.execution').agent_ref,
      'openrouter.local-session'
    );

    await close(running.server);
    running = await start(stateDir);
    state = await requestJson(running.base, '/api/state');
    assert.equal(state.body.bridge.ready_target_envelope_id, null);
    assert.equal(state.body.bridge.claims[packet.claim.claim_id].state, 'completed');
    assert.equal(state.body.bridge.claims[packet.claim.claim_id].agent_ref, 'openrouter.local-session');
  } finally {
    if (running?.server.listening) await close(running.server);
    await rm(stateDir, { recursive: true, force: true });
  }
});
