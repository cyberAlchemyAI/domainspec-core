import assert from 'node:assert/strict';
import { mkdtemp, readdir, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { bridgeGrants, defaultGrants, normalizeL0Grants } from '../src/kernel/grants.mjs';
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

async function withServer(run) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-disposition-'));
  const server = createServer({ rootDir: projectRoot, stateDir });
  const port = await listen(server);

  try {
    await run({ base: `http://127.0.0.1:${port}`, stateDir });
  } finally {
    await close(server);
    await rm(stateDir, { recursive: true, force: true });
  }
}

async function requestJson(base, route, options = {}) {
  const response = await fetch(`${base}${route}`, {
    ...options,
    headers: {
      'content-type': 'application/json',
      ...(options.headers || {})
    }
  });
  const raw = await response.text();
  let body;

  try {
    body = JSON.parse(raw);
  } catch {
    body = { raw };
  }

  return { response, body };
}

function postJson(base, route, body = {}) {
  return requestJson(base, route, {
    method: 'POST',
    body: JSON.stringify(body)
  });
}

function prepare(base, input = {}) {
  return postJson(base, '/api/envelopes/prepare', input);
}

function approve(base, approvalId, body = {}) {
  return postJson(base, `/api/approvals/${approvalId}/approve`, body);
}

function reject(base, approvalId, body = {}) {
  return postJson(base, `/api/approvals/${approvalId}/reject`, body);
}

function readState(base) {
  return requestJson(base, '/api/state');
}

function isInvalidGrants(error) {
  return error.code === 'invalid_grants';
}

test('normalizes only the closed versioned L0 grant vocabulary', () => {
  assert.deepEqual(defaultGrants(), ['dry-run.noop', 'preview.read']);
  assert.deepEqual(
    normalizeL0Grants(['preview.read', 'dry-run.noop']),
    ['dry-run.noop', 'preview.read']
  );
  assert.deepEqual(bridgeGrants(), ['preview.read', 'skill.invoke']);
  assert.deepEqual(
    normalizeL0Grants(['skill.invoke', 'preview.read']),
    ['preview.read', 'skill.invoke']
  );
  assert.throws(() => normalizeL0Grants([]), isInvalidGrants);
  assert.throws(() => normalizeL0Grants('preview.read'), isInvalidGrants);
  assert.throws(() => normalizeL0Grants(['preview.read', 'preview.read']), isInvalidGrants);
  assert.throws(() => normalizeL0Grants(['root.anything']), isInvalidGrants);
  assert.throws(() => normalizeL0Grants(['skill.invoke']), isInvalidGrants);
  assert.throws(
    () => normalizeL0Grants(['skill.invoke', 'preview.read', 'dry-run.noop']),
    isInvalidGrants
  );
});

test('rejects invalid grant declarations before persistence', async () => {
  await withServer(async ({ base }) => {
    const invalidInputs = [
      [{ requested_grants: [] }, 'invalid_request'],
      [{ requested_grants: 'preview.read' }, 'invalid_request'],
      [{ requested_grants: ['preview.read', 'preview.read'] }, 'invalid_request'],
      [{ requested_grants: ['root.anything'] }, 'invalid_grants']
    ];

    for (const [input, expectedError] of invalidInputs) {
      const result = await prepare(base, input);
      assert.equal(result.response.status, 400);
      assert.equal(result.body.error, expectedError);
      if (expectedError === 'invalid_grants') {
        assert.equal(result.body.policy_version, '1');
      }
    }

    const state = await readState(base);
    assert.equal(state.body.approval_queue.length, 0);
    assert.equal(state.body.event_count, 0);
  });
});

test('uses normalized defaults when requested grants are omitted', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepare(base, { task: 'Default grants' });

    assert.equal(prepared.response.status, 201);
    assert.deepEqual(prepared.body.envelope.requested_grants, ['dry-run.noop', 'preview.read']);
    assert.deepEqual(prepared.body.approval.required_for, ['dry-run.noop', 'preview.read']);
  });
});

test('rejects caller identity and records an unattested local operator action', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepare(base, { task: 'Honest attribution' });
    const approvalId = prepared.body.approval.approval_id;
    const spoofed = await approve(base, approvalId, { approved_by: 'same-principal' });
    const approved = await approve(base, approvalId);
    const state = await readState(base);
    const envelopeApproval = state.body.envelopes[prepared.body.envelope.envelope_id].approval;

    assert.equal(spoofed.response.status, 400);
    assert.equal(spoofed.body.error, 'invalid_request');
    assert.equal(approved.response.status, 201);
    assert.equal(Object.hasOwn(envelopeApproval, 'approved_by'), false);
    assert.deepEqual(envelopeApproval.actor, {
      kind: 'local_operator_action',
      assurance: 'unattested'
    });
    assert.deepEqual(state.body.approvals[approvalId].actor, envelopeApproval.actor);
  });
});

test('rejects once with bounded evidence and no success receipt or artifact', async () => {
  await withServer(async ({ base, stateDir }) => {
    const prepared = await prepare(base, { task: 'Reject proposal' });
    const approvalId = prepared.body.approval.approval_id;
    const rejected = await reject(base, approvalId, { reason: '  not ready  ' });
    const stateAfterReject = await readState(base);

    assert.equal(rejected.response.status, 200);
    assert.equal(rejected.body.envelope.state, 'blocked');
    assert.equal(rejected.body.approval.state, 'rejected');
    assert.equal(rejected.body.approval.rejection_reason, 'not ready');
    assert.deepEqual(rejected.body.approval.actor, {
      kind: 'local_operator_action',
      assurance: 'unattested'
    });
    assert.equal(stateAfterReject.body.receipts.length, 0);
    assert.equal(stateAfterReject.body.event_count, 2);
    await assert.rejects(readdir(path.join(stateDir, 'artifacts')), { code: 'ENOENT' });

    const replay = await reject(base, approvalId);
    const conflictingApprove = await approve(base, approvalId);
    const stateAfterReplay = await readState(base);
    assert.equal(replay.response.status, 409);
    assert.equal(replay.body.error, 'already_resolved');
    assert.equal(conflictingApprove.response.status, 409);
    assert.equal(conflictingApprove.body.error, 'already_resolved');
    assert.equal(stateAfterReplay.body.event_count, stateAfterReject.body.event_count);
  });
});

test('rejects invalid reason values without consuming approval', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepare(base, { task: 'Invalid rejection reason' });
    const approvalId = prepared.body.approval.approval_id;

    const scalar = await reject(base, approvalId, { reason: 42 });
    const tooLong = await reject(base, approvalId, { reason: 'x'.repeat(501) });
    const state = await readState(base);

    assert.equal(scalar.response.status, 400);
    assert.equal(scalar.body.error, 'invalid_request');
    assert.equal(tooLong.response.status, 400);
    assert.equal(tooLong.body.error, 'invalid_request');
    assert.equal(state.body.approvals[approvalId].state, 'pending');
    assert.equal(state.body.event_count, 1);
  });
});

test('serializes conflicting approve and reject commands', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepare(base, { task: 'Disposition race' });
    const approvalId = prepared.body.approval.approval_id;
    const results = await Promise.all([
      approve(base, approvalId),
      reject(base, approvalId, { reason: 'race' })
    ]);
    const statuses = results.map(({ response }) => response.status);
    const state = await readState(base);
    const terminalApproval = state.body.approvals[approvalId];

    assert.equal(statuses.filter((status) => status === 200 || status === 201).length, 1);
    assert.equal(statuses.filter((status) => status === 409).length, 1);
    assert.ok(['consumed', 'rejected'].includes(terminalApproval.state));
    assert.equal(state.body.receipts.length, terminalApproval.state === 'consumed' ? 1 : 0);
    assert.equal(state.body.event_count, 2);
  });
});

test('returns stable not-found errors for unknown disposition ids', async () => {
  await withServer(async ({ base }) => {
    const approved = await approve(base, 'approval-missing');
    const rejected = await reject(base, 'approval-missing');

    assert.equal(approved.response.status, 404);
    assert.equal(approved.body.error, 'approval_not_found');
    assert.equal(rejected.response.status, 404);
    assert.equal(rejected.body.error, 'approval_not_found');
  });
});
