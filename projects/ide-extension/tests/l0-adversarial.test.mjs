import assert from 'node:assert/strict';
import { access, mkdtemp, readFile, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
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

async function requestJson(base, route, options = {}) {
  const response = await fetch(`${base}${route}`, {
    ...options,
    headers: {
      'content-type': 'application/json',
      ...(options.headers || {})
    }
  });
  const body = await response.json();
  return { response, body };
}

async function withServer(run) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-adversarial-'));
  const server = createServer({ rootDir: projectRoot, stateDir });
  const port = await listen(server);

  try {
    await run({ base: `http://127.0.0.1:${port}`, stateDir });
  } finally {
    await close(server);
    await rm(stateDir, { recursive: true, force: true });
  }
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

function readState(base) {
  return requestJson(base, '/api/state');
}

test('AR-CAND-001 does not persist caller-selected approval attribution', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepare(base, { task: 'Attribution boundary' });
    const approvalId = prepared.body.approval.approval_id;
    const spoofed = await approve(base, approvalId, { approved_by: 'same-principal' });
    assert.equal(spoofed.response.status, 400);
    assert.equal(spoofed.body.error, 'invalid_request');

    const approved = await approve(base, approvalId);
    assert.equal(approved.response.status, 201);

    const state = await readState(base);
    assert.equal(Object.hasOwn(state.body.current_envelope.approval, 'approved_by'), false);
    assert.deepEqual(state.body.current_envelope.approval.actor, {
      kind: 'local_operator_action',
      assurance: 'unattested'
    });
  });
});

test('AR-CAND-002 rejects sequential approval replay before writing', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepare(base, { task: 'Sequential replay' });
    const approvalId = prepared.body.approval.approval_id;

    const first = await approve(base, approvalId);
    const replay = await approve(base, approvalId);
    const state = await readState(base);

    assert.equal(first.response.status, 201);
    assert.equal(replay.response.status, 409);
    assert.equal(replay.body.error, 'already_resolved');
    assert.equal(state.body.receipts.length, 1);
  });
});

test('AR-CAND-002 permits exactly one concurrent approval', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepare(base, { task: 'Concurrent replay' });
    const approvalId = prepared.body.approval.approval_id;
    const attempts = await Promise.all(
      Array.from({ length: 8 }, () => approve(base, approvalId))
    );
    const statuses = attempts.map(({ response }) => response.status);
    const state = await readState(base);

    assert.equal(statuses.filter((status) => status === 201).length, 1);
    assert.equal(statuses.filter((status) => status === 409).length, 7);
    assert.equal(state.body.receipts.length, 1);
  });
});

test('AR-CAND-004 rejects grants outside the closed L0 vocabulary', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepare(base, {
      task: 'Unknown grant',
      requested_grants: ['root.anything']
    });
    const state = await readState(base);

    assert.equal(prepared.response.status, 400);
    assert.equal(prepared.body.error, 'invalid_grants');
    assert.equal(state.body.approval_queue.length, 0);
  });
});

test('AR-CAND-005 keeps every pending approval reachable by id', async () => {
  await withServer(async ({ base }) => {
    const first = await prepare(base, { task: 'Pending A' });
    const second = await prepare(base, { task: 'Pending B' });
    assert.equal(first.response.status, 201);
    assert.equal(second.response.status, 201);

    const approvedFirst = await approve(base, first.body.approval.approval_id);
    const state = await readState(base);

    assert.equal(approvedFirst.response.status, 201);
    assert.equal(
      state.body.approval_queue.find(
        (item) => item.approval_id === first.body.approval.approval_id
      )?.state,
      'consumed'
    );
    assert.equal(
      state.body.approval_queue.find(
        (item) => item.approval_id === second.body.approval.approval_id
      )?.state,
      'pending'
    );
  });
});

test('AR-CAND-006 keeps receipt events and projected receipts consistent', async () => {
  await withServer(async ({ base, stateDir }) => {
    const prepared = await prepare(base, { task: 'Persistence race' });
    const approvalId = prepared.body.approval.approval_id;
    await Promise.all(Array.from({ length: 12 }, () => approve(base, approvalId)));

    const state = await readState(base);
    const eventLines = (await readFile(path.join(stateDir, 'events.jsonl'), 'utf8'))
      .split('\n')
      .filter((line) => line.trim() !== '');
    const receiptEvents = eventLines
      .map((line) => JSON.parse(line))
      .filter((event) => event.event_type === 'receipt.appended');

    assert.equal(receiptEvents.length, state.body.receipts.length);
    assert.deepEqual(
      new Set(receiptEvents.map((event) => event.receipt.receipt_id)),
      new Set(state.body.receipts.map((receipt) => receipt.receipt_id))
    );
  });
});

test('AR-CAND-007 materializes a resolvable after-state artifact', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepare(base, { task: 'After evidence' });
    const approved = await approve(base, prepared.body.approval.approval_id);
    assert.equal(approved.response.status, 201);

    const afterRef = approved.body.receipt.after_ref;
    assert.doesNotMatch(afterRef, /^state:/);
    await access(path.resolve(process.cwd(), afterRef));
  });
});

test('AR-CAND-008 rejects schema-invalid context refs before persistence', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepare(base, {
      task: 'Malformed context',
      context_refs: 'not-an-array'
    });
    const state = await readState(base);

    assert.equal(prepared.response.status, 400);
    assert.equal(prepared.body.error, 'invalid_request');
    assert.equal(state.body.approval_queue.length, 0);
  });
});
