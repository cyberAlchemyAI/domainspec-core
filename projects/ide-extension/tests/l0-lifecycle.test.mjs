import assert from 'node:assert/strict';
import { mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { approveDryRunEnvelope, prepareDryRunEnvelope } from '../src/envelopes/dry-run-envelope.mjs';
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
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-lifecycle-'));
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

function prepare(base, task) {
  return postJson(base, '/api/envelopes/prepare', { task });
}

function approve(base, approvalId) {
  return postJson(base, `/api/approvals/${approvalId}/approve`);
}

function readState(base) {
  return requestJson(base, '/api/state');
}

test('indexes envelopes and approvals by id and targets run by envelope id', async () => {
  await withServer(async ({ base }) => {
    const first = await prepare(base, 'Indexed A');
    const second = await prepare(base, 'Indexed B');
    const state = await readState(base);

    assert.equal(state.body.envelopes[first.body.envelope.envelope_id].task, 'Indexed A');
    assert.equal(state.body.envelopes[second.body.envelope.envelope_id].task, 'Indexed B');
    assert.equal(
      state.body.approvals[first.body.approval.approval_id].envelope_id,
      first.body.envelope.envelope_id
    );
    assert.equal(state.body.current_envelope_id, second.body.envelope.envelope_id);

    const blocked = await postJson(
      base,
      `/api/envelopes/${first.body.envelope.envelope_id}/run`
    );
    assert.equal(blocked.response.status, 409);
    assert.equal(blocked.body.approval_id, first.body.approval.approval_id);

    const ambiguous = await postJson(base, '/api/envelopes/run');
    assert.equal(ambiguous.response.status, 404);
  });
});

test('does not promote a legacy workbench-only projection into authority', async () => {
  await withServer(async ({ base, stateDir }) => {
    const envelope = prepareDryRunEnvelope({ task: 'Legacy singleton' });
    const approved = approveDryRunEnvelope(envelope);
    const legacyEnvelope = structuredClone(approved.envelope);
    legacyEnvelope.approval = {
      required: true,
      approval_id: envelope.approval.approval_id,
      approved_by: 'legacy-human',
      approved_at: approved.receipt.created_at
    };
    const approvalItem = {
      approval_id: envelope.approval.approval_id,
      run_id: envelope.run_id,
      state: 'approved',
      title: envelope.task,
      required_for: envelope.requested_grants,
      created_at: envelope.created_at,
      approved_at: approved.receipt.created_at
    };
    const legacyState = {
      project: 'ide-extension',
      boundary: 'l0-witness',
      approval_queue: [approvalItem],
      receipts: [approved.receipt],
      current_envelope: legacyEnvelope,
      evidence_refs: []
    };
    await writeFile(
      path.join(stateDir, 'workbench.json'),
      `${JSON.stringify(legacyState, null, 2)}\n`,
      'utf8'
    );

    const state = await readState(base);

    assert.equal(state.body.current_envelope_id, null);
    assert.deepEqual(state.body.envelopes, {});
    assert.deepEqual(state.body.approvals, {});
    assert.deepEqual(state.body.receipts, []);
    assert.equal(state.body.event_count, 0);
  });
});

test('consumes an approval once and rejects sequential replay without writes', async () => {
  await withServer(async ({ base, stateDir }) => {
    const prepared = await prepare(base, 'Sequential exact once');
    const approvalId = prepared.body.approval.approval_id;
    const first = await approve(base, approvalId);
    const afterFirst = await readState(base);
    const artifactsAfterFirst = await readdir(path.join(stateDir, 'artifacts'));

    const replay = await approve(base, approvalId);
    const afterReplay = await readState(base);
    const artifactsAfterReplay = await readdir(path.join(stateDir, 'artifacts'));

    assert.equal(first.response.status, 201);
    assert.equal(replay.response.status, 409);
    assert.equal(replay.body.error, 'already_resolved');
    assert.equal(afterReplay.body.approvals[approvalId].state, 'consumed');
    assert.equal(afterReplay.body.receipts.length, 1);
    assert.equal(afterReplay.body.event_count, afterFirst.body.event_count);
    assert.deepEqual(artifactsAfterReplay.sort(), artifactsAfterFirst.sort());
  });
});

test('permits exactly one concurrent approval transition', async () => {
  await withServer(async ({ base }) => {
    const prepared = await prepare(base, 'Concurrent exact once');
    const approvalId = prepared.body.approval.approval_id;
    const attempts = await Promise.all(
      Array.from({ length: 8 }, () => approve(base, approvalId))
    );
    const statuses = attempts.map(({ response }) => response.status);
    const state = await readState(base);

    assert.equal(statuses.filter((status) => status === 201).length, 1);
    assert.equal(statuses.filter((status) => status === 409).length, 7);
    assert.equal(state.body.receipts.length, 1);
    assert.equal(state.body.approvals[approvalId].state, 'consumed');
  });
});

test('resolves an older pending approval without replacing the current projection', async () => {
  await withServer(async ({ base }) => {
    const first = await prepare(base, 'Older A');
    const second = await prepare(base, 'Current B');
    const approved = await approve(base, first.body.approval.approval_id);
    const state = await readState(base);

    assert.equal(approved.response.status, 201);
    assert.equal(state.body.envelopes[first.body.envelope.envelope_id].state, 'passed');
    assert.equal(state.body.envelopes[second.body.envelope.envelope_id].state, 'awaiting_approval');
    assert.equal(state.body.approvals[first.body.approval.approval_id].state, 'consumed');
    assert.equal(state.body.approvals[second.body.approval.approval_id].state, 'pending');
    assert.equal(state.body.current_envelope_id, second.body.envelope.envelope_id);
    assert.equal(state.body.current_envelope.envelope_id, second.body.envelope.envelope_id);
  });
});

test('repairs a stale mismatched projection before disposition', async () => {
  await withServer(async ({ base, stateDir }) => {
    const prepared = await prepare(base, 'Binding mismatch');
    const approvalId = prepared.body.approval.approval_id;
    const workbenchFile = path.join(stateDir, 'workbench.json');
    const workbench = JSON.parse(await readFile(workbenchFile, 'utf8'));
    workbench.approvals[approvalId].run_id = 'run-mismatch';
    await writeFile(workbenchFile, `${JSON.stringify(workbench, null, 2)}\n`, 'utf8');

    const result = await approve(base, approvalId);
    const state = await readState(base);

    assert.equal(result.response.status, 201);
    assert.equal(state.body.approvals[approvalId].run_id, prepared.body.envelope.run_id);
    assert.equal(state.body.approvals[approvalId].state, 'consumed');
    assert.equal(state.body.receipts.length, 1);
  });
});

test('envelope approval helper rejects a non-pending envelope', () => {
  const envelope = prepareDryRunEnvelope({ task: 'Helper guard' });
  const first = approveDryRunEnvelope(envelope);

  assert.throws(
    () => approveDryRunEnvelope(first.envelope),
    (error) => error.code === 'already_resolved'
  );
});
