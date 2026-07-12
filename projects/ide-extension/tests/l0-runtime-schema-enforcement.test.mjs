import assert from 'node:assert/strict';
import { mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { validateSchema } from '../src/kernel/schema-validation.mjs';
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
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-runtime-schema-'));
  const server = createServer({ rootDir: projectRoot, stateDir });
  await server.ready;
  const port = await listen(server);

  try {
    await run({ base: `http://127.0.0.1:${port}`, stateDir });
  } finally {
    await close(server);
    await rm(stateDir, { recursive: true, force: true });
  }
}

async function request(base, route, options = {}) {
  const response = await fetch(`${base}${route}`, {
    ...options,
    headers: {
      'content-type': 'application/json',
      ...(options.headers || {})
    }
  });
  const raw = await response.text();
  return { response, body: JSON.parse(raw) };
}

function postJson(base, route, body = {}) {
  return request(base, route, { method: 'POST', body: JSON.stringify(body) });
}

test('rejects malformed raw requests before creating durable state', async () => {
  await withServer(async ({ base, stateDir }) => {
    const hostileRequests = [
      [{ context_refs: 'ambient' }, 'prepare-request'],
      [{ task: 'extra field', ambient_authority: true }, 'prepare-request'],
      [{ requested_grants: [] }, 'prepare-request'],
      [{ requested_skill: '../hidden-skill' }, 'prepare-request']
    ];

    for (const [body, schemaName] of hostileRequests) {
      const result = await postJson(base, '/api/envelopes/prepare', body);
      assert.equal(result.response.status, 400);
      assert.equal(result.body.error, 'invalid_request');
      assert.equal(result.body.schema_name, schemaName);
      assert.ok(result.body.validation_errors.length > 0);
    }

    const invalidJson = await request(base, '/api/envelopes/prepare', {
      method: 'POST',
      body: '{"task":'
    });
    assert.equal(invalidJson.response.status, 400);
    assert.equal(invalidJson.body.error, 'invalid_json');
    assert.deepEqual(await readdir(stateDir), ['workbench.json']);
    const projection = JSON.parse(await readFile(path.join(stateDir, 'workbench.json'), 'utf8'));
    assert.deepEqual(projection.approval_queue, []);
    assert.deepEqual(projection.receipts, []);
  });
});

test('rejects caller approval fields without consuming the pending approval', async () => {
  await withServer(async ({ base, stateDir }) => {
    const prepared = await postJson(base, '/api/envelopes/prepare', { task: 'Closed approval' });
    const approvalId = prepared.body.approval.approval_id;
    const stateBefore = await request(base, '/api/state');
    const spoofed = await postJson(base, `/api/approvals/${approvalId}/approve`, {
      approved_by: 'same-principal'
    });
    const stateAfter = await request(base, '/api/state');

    assert.equal(spoofed.response.status, 400);
    assert.equal(spoofed.body.error, 'invalid_request');
    assert.equal(spoofed.body.schema_name, 'approve-request');
    assert.equal(stateAfter.body.approvals[approvalId].state, 'pending');
    assert.equal(stateAfter.body.event_count, stateBefore.body.event_count);
    await assert.rejects(readdir(path.join(stateDir, 'artifacts')), { code: 'ENOENT' });
  });
});

test('validates emitted envelope, approval, and receipt before persistence', async () => {
  await withServer(async ({ base }) => {
    const prepared = await postJson(base, '/api/envelopes/prepare', { task: 'Valid outputs' });
    const approvalId = prepared.body.approval.approval_id;
    const approved = await postJson(base, `/api/approvals/${approvalId}/approve`);
    const state = await request(base, '/api/state');

    assert.equal(approved.response.status, 201);
    assert.deepEqual(
      await validateSchema('agent-envelope', state.body.current_envelope),
      { valid: true, errors: [] }
    );
    assert.deepEqual(
      await validateSchema('approval-record', state.body.approvals[approvalId]),
      { valid: true, errors: [] }
    );
    assert.deepEqual(
      await validateSchema('receipt', approved.body.receipt),
      { valid: true, errors: [] }
    );
  });
});

test('fails closed when authoritative history contains an invalid record', async () => {
  await withServer(async ({ base, stateDir }) => {
    const prepared = await postJson(base, '/api/envelopes/prepare', { task: 'Tampered output' });
    const approvalId = prepared.body.approval.approval_id;
    const workbenchFile = path.join(stateDir, 'workbench.json');
    const eventsFile = path.join(stateDir, 'events.jsonl');
    const event = JSON.parse((await readFile(eventsFile, 'utf8')).trim());
    event.approval.ambient_authority = true;
    await writeFile(eventsFile, `${JSON.stringify(event)}\n`, 'utf8');
    const workbenchBefore = await readFile(workbenchFile, 'utf8');
    const eventsBefore = await readFile(eventsFile, 'utf8');

    const result = await postJson(base, `/api/approvals/${approvalId}/approve`);
    const workbenchAfter = await readFile(workbenchFile, 'utf8');
    const eventsAfter = await readFile(eventsFile, 'utf8');

    assert.equal(result.response.status, 500);
    assert.match(result.body.error, /approval-record schema validation failed/);
    assert.equal(workbenchAfter, workbenchBefore);
    assert.equal(eventsAfter, eventsBefore);
    await assert.rejects(readdir(path.join(stateDir, 'artifacts')), { code: 'ENOENT' });
  });
});

test('rejects invalid disposition payloads without appending events', async () => {
  await withServer(async ({ base, stateDir }) => {
    const prepared = await postJson(base, '/api/envelopes/prepare', { task: 'Closed rejection' });
    const approvalId = prepared.body.approval.approval_id;
    const invalid = await postJson(base, `/api/approvals/${approvalId}/reject`, {
      reason: 42,
      approved_by: 'caller-selected'
    });
    const state = await request(base, '/api/state');

    assert.equal(invalid.response.status, 400);
    assert.equal(invalid.body.error, 'invalid_request');
    assert.equal(invalid.body.schema_name, 'reject-request');
    assert.equal(state.body.approvals[approvalId].state, 'pending');
    assert.equal(state.body.event_count, 1);
    await assert.rejects(readdir(path.join(stateDir, 'artifacts')), { code: 'ENOENT' });
  });
});

test('fails readiness when a shipped module manifest violates its schema', async () => {
  const modulesDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-modules-'));
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-readiness-'));

  try {
    await writeFile(
      path.join(modulesDir, 'invalid.manifest.json'),
      `${JSON.stringify({ module_id: 'invalid.module', ambient_authority: true }, null, 2)}\n`,
      'utf8'
    );
    const server = createServer({ rootDir: projectRoot, modulesDir, stateDir });

    await assert.rejects(server.ready, (error) => {
      assert.equal(error.code, 'schema_validation_failed');
      assert.equal(error.schema_name, 'module-manifest');
      return true;
    });
    assert.equal(server.listening, false);
    assert.deepEqual(await readdir(stateDir), []);
  } finally {
    await rm(modulesDir, { recursive: true, force: true });
    await rm(stateDir, { recursive: true, force: true });
  }
});
