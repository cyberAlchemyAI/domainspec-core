import assert from 'node:assert/strict';
import { mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { appendEvent as appendAuditEvent, readEvents } from '../src/kernel/audit.mjs';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const skillHash = 'a'.repeat(64);

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
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-bridge-result-'));
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

async function activeClaim(base, suffix = 'one') {
  const prepared = await postJson(base, '/api/envelopes/prepare', {
    task: `Return a bounded result ${suffix}`,
    requested_skill: 'decision-gate',
    requested_grants: ['preview.read', 'skill.invoke'],
    context_refs: ['projects/ide-extension/SPEC.md']
  });
  const authorized = await postJson(
    base,
    `/api/approvals/${prepared.body.approval.approval_id}/approve`
  );
  await postJson(base, `/api/bridge/requests/${prepared.body.envelope.envelope_id}/ready`);
  const claimed = await postJson(base, `/api/bridge/requests/${prepared.body.envelope.envelope_id}/claim`, {
    schema_version: '2',
    envelope_id: prepared.body.envelope.envelope_id,
    agent_ref: 'openrouter.local-session',
    session_ref: `session-result-${suffix}`,
    assurance: 'unattested'
  });
  return { prepared: prepared.body, authorized: authorized.body, claimed: claimed.body };
}

function resultBody(flow, overrides = {}) {
  const { claim } = flow.claimed;
  return {
    schema_version: '2',
    claim_id: claim.claim_id,
    claim_attempt_id: claim.claim_attempt_id,
    envelope_id: claim.envelope_id,
    run_id: claim.run_id,
    approval_id: claim.approval_id,
    session_ref: claim.session_ref,
    assurance: 'unattested',
    requested_skill: 'decision-gate',
    skill_sha256: skillHash,
    status: 'passed',
    summary: 'The bounded read-only skill completed successfully.',
    validation: ['approved decision record inspected'],
    evidence_refs: ['projects/ide-extension/SPEC.md'],
    ...overrides
  };
}

function submitResult(base, flow, overrides = {}) {
  return postJson(
    base,
    `/api/bridge/claims/${flow.claimed.claim.claim_id}/result`,
    resultBody(flow, overrides)
  );
}

test('admits one bound result and mints a resolvable execution receipt', async () => {
  await withServer(async ({ base, stateDir }) => {
    const flow = await activeClaim(base);
    const admitted = await submitResult(base, flow);
    assert.equal(admitted.response.status, 201);
    assert.equal(admitted.body.envelope.state, 'passed');
    assert.equal(admitted.body.result.status, 'passed');
    assert.equal(admitted.body.receipt.receipt_kind, 'skill.execution');
    assert.equal(admitted.body.receipt.agent_ref, 'openrouter.local-session');
    assert.equal(admitted.body.receipt.authorization_receipt_id,
      flow.authorized.receipt.receipt_id);
    assert.equal(admitted.body.receipt.skill_sha256, skillHash);
    assert.equal(admitted.body.receipt.assurance, 'unattested');

    const state = await requestJson(base, '/api/state');
    assert.deepEqual(state.body.receipts.map((receipt) => receipt.receipt_kind), [
      'authorization.receipt',
      'skill.execution'
    ]);
    assert.equal(state.body.approvals[flow.claimed.claim.approval_id].state, 'consumed');
    assert.equal(state.body.bridge.claims[flow.claimed.claim.claim_id].state, 'completed');
    assert.equal(
      state.body.bridge.claims[flow.claimed.claim.claim_id].agent_ref,
      'openrouter.local-session'
    );
    assert.equal(
      state.body.receipts.find((receipt) => receipt.receipt_kind === 'skill.execution').agent_ref,
      'openrouter.local-session'
    );

    for (const kind of ['before', 'after', 'result', 'receipt']) {
      const evidence = await requestJson(
        base,
        `/api/receipts/${admitted.body.receipt.receipt_id}/evidence/${kind}`
      );
      assert.equal(evidence.response.status, 200, kind);
    }
    const events = await readEvents(path.join(stateDir, 'events.jsonl'));
    assert.equal(events.at(-1).event_type, 'bridge.result_recorded');
    assert.equal(events.at(-1).artifact_refs.length, 4);
  });
});

test('rejects mismatched, unsupported, malformed, and unresolved results without mutation', async () => {
  await withServer(async ({ base }) => {
    const flow = await activeClaim(base, 'hostile');
    const baseline = await requestJson(base, '/api/state');
    const cases = [
      [{ session_ref: 'session-wrong' }, 409, 'result_binding_mismatch'],
      [{ claim_attempt_id: 'attempt-wrong' }, 409, 'result_binding_mismatch'],
      [{ requested_skill: 'other-skill' }, 409, 'result_binding_mismatch'],
      [{ status: 'failed' }, 409, 'unsupported_result_status'],
      [{ evidence_refs: ['projects/ide-extension/does-not-exist.md'] }, 400, 'evidence_not_found'],
      [{ skill_sha256: 'not-a-hash' }, 400, 'invalid_request']
    ];
    for (const [override, status, error] of cases) {
      const rejected = await submitResult(base, flow, override);
      assert.equal(rejected.response.status, status, JSON.stringify(override));
      assert.equal(rejected.body.error, error, JSON.stringify(override));
    }
    const state = await requestJson(base, '/api/state');
    assert.equal(state.body.event_count, baseline.body.event_count);
    assert.equal(state.body.receipts.length, 1);
    assert.equal(state.body.bridge.claims[flow.claimed.claim.claim_id].state, 'claimed');
  });
});

test('rejects duplicate and post-release results', async () => {
  await withServer(async ({ base }) => {
    const completed = await activeClaim(base, 'duplicate');
    assert.equal((await submitResult(base, completed)).response.status, 201);
    const duplicate = await submitResult(base, completed);
    assert.equal(duplicate.response.status, 409);
    assert.equal(duplicate.body.error, 'claim_not_active');

    const released = await activeClaim(base, 'released');
    const claim = released.claimed.claim;
    await postJson(base, `/api/bridge/claims/${claim.claim_id}/interrupt`, {
      schema_version: '2',
      claim_id: claim.claim_id,
      envelope_id: claim.envelope_id,
      session_ref: claim.session_ref,
      assurance: 'unattested',
      reason: 'Stop before result.'
    });
    await postJson(base, `/api/bridge/claims/${claim.claim_id}/release`, {
      reason: 'Operator released read-only attempt.'
    });
    const late = await submitResult(base, released);
    assert.equal(late.response.status, 409);
    assert.equal(late.body.error, 'claim_not_active');
  });
});

test('serializes result against interruption', async () => {
  await withServer(async ({ base }) => {
    const flow = await activeClaim(base, 'race');
    const claim = flow.claimed.claim;
    const [result, interruption] = await Promise.all([
      submitResult(base, flow),
      postJson(base, `/api/bridge/claims/${claim.claim_id}/interrupt`, {
        schema_version: '2',
        claim_id: claim.claim_id,
        envelope_id: claim.envelope_id,
        session_ref: claim.session_ref,
        assurance: 'unattested',
        reason: 'Concurrent interruption.'
      })
    ]);
    assert.equal([result.response.status, interruption.response.status].filter((s) => s < 300).length, 1);
    assert.equal([result.response.status, interruption.response.status].filter((s) => s === 409).length, 1);
    const state = await requestJson(base, '/api/state');
    assert.ok(['passed', 'interrupted'].includes(
      state.body.envelopes[claim.envelope_id].state
    ));
  });
});

test('result survives restart with both receipt types and evidence', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-result-restart-'));
  let running;
  try {
    running = await start(stateDir);
    const flow = await activeClaim(running.base, 'restart');
    const admitted = await submitResult(running.base, flow, { status: 'flagged' });
    await close(running.server);
    running = await start(stateDir);
    const status = await requestJson(
      running.base,
      `/api/bridge/claims/${flow.claimed.claim.claim_id}`
    );
    assert.equal(status.body.claim.state, 'completed');
    assert.equal(status.body.result.status, 'flagged');
    const receiptEvidence = await requestJson(
      running.base,
      `/api/receipts/${admitted.body.receipt.receipt_id}/evidence/receipt`
    );
    assert.equal(receiptEvidence.response.status, 200);
    assert.equal(receiptEvidence.body.receipt.agent_ref, 'openrouter.local-session');
  } finally {
    if (running?.server.listening) await close(running.server);
    await rm(stateDir, { recursive: true, force: true });
  }
});

test('append failure leaves claim active and permits a fresh evidence retry', async () => {
  let appendCount = 0;
  const appendEvent = async (...args) => {
    appendCount += 1;
    if (appendCount === 5) {
      const error = new Error('injected result append failure');
      error.code = 'EIO';
      throw error;
    }
    return appendAuditEvent(...args);
  };

  await withServer(async ({ base }) => {
    const flow = await activeClaim(base, 'append-failure');
    const failed = await submitResult(base, flow);
    assert.equal(failed.response.status, 500);
    let state = await requestJson(base, '/api/state');
    assert.equal(state.body.bridge.claims[flow.claimed.claim.claim_id].state, 'claimed');
    assert.equal(state.body.receipts.length, 1);
    assert.equal(state.body.reconciliation.orphan_artifacts.length, 3);

    const retried = await submitResult(base, flow);
    assert.equal(retried.response.status, 201);
    state = await requestJson(base, '/api/state');
    assert.equal(state.body.receipts.length, 2);
  }, { appendEvent });
});
