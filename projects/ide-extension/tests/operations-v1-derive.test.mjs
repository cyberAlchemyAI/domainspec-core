import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { appendEvent } from '../src/kernel/audit.mjs';
import { OPERATIONS_V1_LIMITS } from '../src/kernel/operations-contracts.mjs';
import { operationsDerivationDigest } from '../src/kernel/operations.mjs';
import { atomicWriteJson } from '../src/kernel/storage.mjs';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const cli = path.join(projectRoot, 'scripts/session-bridge.mjs');
const INITIAL_HTML = '<!doctype html><title>Source one</title><button>Next</button>';
const SECOND_HTML = '<!doctype html><title>Source two</title><button>Continue</button>';

function listen(server) {
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve(server.address().port));
  });
}

function close(server) {
  return new Promise((resolve, reject) => {
    server.close((error) => error ? reject(error) : resolve());
  });
}

async function request(base, route, options = {}) {
  const response = await fetch(`${base}${route}`, {
    ...options,
    headers: { 'content-type': 'application/json', ...(options.headers || {}) }
  });
  const contentType = response.headers.get('content-type') || '';
  return {
    response,
    body: contentType.includes('application/json')
      ? JSON.parse(await response.text())
      : await response.text()
  };
}

function post(base, route, body) {
  return request(base, route, { method: 'POST', body: JSON.stringify(body) });
}

function publish(base, pathValue, title = 'Derivation source') {
  return post(base, '/api/canvas/publish', {
    schema_version: '1',
    path: pathValue,
    title,
    kind: 'presentation'
  });
}

function derivationRequest(current, key = 'derive-source-1') {
  return {
    schema_version: '1',
    source_v0_surface_id: current.surface_id,
    source_revision_id: current.revision.revision_id,
    operation_surface_idempotency_key: key
  };
}

function derive(base, body) {
  return post(base, '/api/canvas/operation-surfaces', body);
}

async function fixture(prefix = 'ide-extension-operations-derive-') {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), `${prefix}state-`));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), `${prefix}workspace-`));
  const relative = 'presentations/source.html';
  const file = path.join(workspaceRoot, relative);
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, INITIAL_HTML, 'utf8');
  return { stateDir, workspaceRoot, relative, file };
}

async function start(f, options = {}) {
  const server = createServer({
    rootDir: projectRoot,
    stateDir: f.stateDir,
    workspaceRoot: f.workspaceRoot,
    ...options
  });
  await server.ready;
  const port = await listen(server);
  return { server, base: `http://127.0.0.1:${port}` };
}

async function cleanup(f, running) {
  if (running?.server.listening) await close(running.server);
  await rm(f.stateDir, { recursive: true, force: true });
  await rm(f.workspaceRoot, { recursive: true, force: true });
}

function runCli(args) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [cli, ...args], { cwd: projectRoot });
    const stdout = [];
    const stderr = [];
    child.stdout.on('data', (chunk) => stdout.push(chunk));
    child.stderr.on('data', (chunk) => stderr.push(chunk));
    child.on('error', reject);
    child.on('close', (code) => resolve({
      code,
      stdout: Buffer.concat(stdout).toString('utf8'),
      stderr: Buffer.concat(stderr).toString('utf8')
    }));
  });
}

test('derives exact bytes once, preserves V0, and restores metadata after restart', async () => {
  const f = await fixture();
  let running;
  try {
    running = await start(f);
    const published = await publish(running.base, f.relative);
    const source = published.body.current;
    const input = derivationRequest(source);
    const derived = await derive(running.base, input);

    assert.equal(derived.response.status, 201);
    assert.equal(derived.body.idempotent, false);
    assert.match(derived.body.surface.operations_surface_id, /^operations-surface-/);
    assert.notEqual(derived.body.surface.operations_surface_id, source.surface_id);
    assert.equal(derived.body.surface.source_v0_revision_id, source.revision.revision_id);
    assert.deepEqual(
      await readFile(path.join(f.stateDir, derived.body.revision.blob_ref)),
      Buffer.from(INITIAL_HTML)
    );
    assert.deepEqual((await request(running.base, '/api/canvas/current')).body.current, source);

    await writeFile(f.file, SECOND_HTML, 'utf8');
    const retry = await derive(running.base, input);
    assert.equal(retry.response.status, 200);
    assert.equal(retry.body.idempotent, true);
    assert.deepEqual(retry.body.surface, derived.body.surface);
    assert.deepEqual(retry.body.revision, derived.body.revision);

    const republished = await publish(running.base, f.relative, 'Updated V0 source');
    assert.equal(republished.response.status, 201);
    assert.notEqual(republished.body.current.revision.revision_id, source.revision.revision_id);
    const metadataRoute = `/api/canvas/operation-surfaces/${encodeURIComponent(derived.body.surface.operations_surface_id)}`;
    assert.deepEqual((await request(running.base, metadataRoute)).body.surface, derived.body.surface);

    const beforeRestart = (await request(running.base, metadataRoute)).body;
    await close(running.server);
    running = await start(f);
    assert.deepEqual((await request(running.base, metadataRoute)).body, beforeRestart);
    assert.equal(
      (await request(running.base, '/api/canvas/current')).body.current.revision.revision_id,
      republished.body.current.revision.revision_id
    );

    const state = (await request(running.base, '/api/state')).body;
    assert.equal(
      state.canvas.operations_v1.derivation_keys[input.operation_surface_idempotency_key]
        .normalized_input_digest,
      operationsDerivationDigest(input)
    );
  } finally {
    await cleanup(f, running);
  }
});

test('admits an exact historical source and rejects drift without blob or event', async () => {
  const f = await fixture('ide-extension-operations-historical-');
  let running;
  try {
    running = await start(f);
    const first = (await publish(running.base, f.relative)).body.current;
    await writeFile(f.file, SECOND_HTML, 'utf8');
    const second = (await publish(running.base, f.relative, 'Second source')).body.current;
    await writeFile(f.file, INITIAL_HTML, 'utf8');

    const historical = await derive(running.base, derivationRequest(first, 'derive-historical'));
    assert.equal(historical.response.status, 201);
    assert.equal(historical.body.surface.source_v0_revision_id, first.revision.revision_id);
    assert.equal(
      (await request(running.base, '/api/canvas/current')).body.current.revision.revision_id,
      second.revision.revision_id
    );

    await writeFile(f.file, '<h1>drifted</h1>', 'utf8');
    const before = (await request(running.base, '/api/state')).body;
    const drifted = await derive(running.base, derivationRequest(second, 'derive-drifted'));
    const after = (await request(running.base, '/api/state')).body;
    assert.equal(drifted.response.status, 409);
    assert.equal(drifted.body.error, 'source_revision_unavailable');
    assert.equal(drifted.body.reason, 'workspace_drift');
    assert.equal(after.event_count, before.event_count);
    assert.equal(after.reconciliation.canvas_blobs.blob_count, 1);

    await rm(f.file);
    const unavailable = await derive(
      running.base,
      derivationRequest(second, 'derive-unavailable')
    );
    assert.equal(unavailable.response.status, 409);
    assert.equal(unavailable.body.error, 'source_revision_unavailable');
    assert.equal(unavailable.body.reason, 'workspace_unavailable');
    assert.equal((await request(running.base, '/api/state')).body.event_count, before.event_count);
  } finally {
    await cleanup(f, running);
  }
});

test('serializes concurrent same-key derivation and rejects key reuse for new input', async () => {
  const f = await fixture('ide-extension-operations-race-');
  let running;
  try {
    running = await start(f);
    const first = (await publish(running.base, f.relative)).body.current;
    const input = derivationRequest(first, 'derive-race');
    const attempts = await Promise.all(Array.from({ length: 6 }, () => derive(running.base, input)));
    assert.equal(attempts.filter(({ response }) => response.status === 201).length, 1);
    assert.equal(attempts.filter(({ response }) => response.status === 200).length, 5);
    assert.equal(new Set(attempts.map(({ body }) => body.surface.operations_surface_id)).size, 1);

    await writeFile(f.file, SECOND_HTML, 'utf8');
    const second = (await publish(running.base, f.relative, 'Second source')).body.current;
    const conflict = await derive(running.base, derivationRequest(second, 'derive-race'));
    assert.equal(conflict.response.status, 409);
    assert.equal(conflict.body.error, 'derivation_key_conflict');
    const state = (await request(running.base, '/api/state')).body;
    assert.equal(Object.keys(state.canvas.operations_v1.derivation_keys).length, 1);
    assert.equal(Object.keys(state.canvas.operations_v1.surfaces).length, 1);
  } finally {
    await cleanup(f, running);
  }
});

test('rejects invalid, unknown, oversized source, and oversized HTTP input without effects', async () => {
  const f = await fixture('ide-extension-operations-limits-');
  let running;
  try {
    running = await start(f);
    const source = (await publish(running.base, f.relative)).body.current;
    const baseline = (await request(running.base, '/api/state')).body.event_count;

    const invalid = await derive(running.base, { schema_version: '1' });
    assert.equal(invalid.response.status, 400);
    assert.equal(invalid.body.error, 'invalid_request');

    const unknown = await derive(running.base, {
      ...derivationRequest(source, 'derive-unknown'),
      source_revision_id: 'revision-unknown'
    });
    assert.equal(unknown.response.status, 409);
    assert.equal(unknown.body.error, 'source_revision_unavailable');
    assert.equal(unknown.body.reason, 'projection_missing');

    const raw = JSON.stringify({
      ...derivationRequest(source, 'derive-http-limit'),
      padding: 'x'.repeat(OPERATIONS_V1_LIMITS.http_request_bytes)
    });
    const oversizedHttp = await request(running.base, '/api/canvas/operation-surfaces', {
      method: 'POST',
      body: raw
    });
    assert.equal(oversizedHttp.response.status, 413);
    assert.equal(oversizedHttp.body.error, 'request_too_large');

    await writeFile(
      f.file,
      Buffer.alloc(OPERATIONS_V1_LIMITS.source_html_bytes + 1, 0x78)
    );
    const largePublication = (await publish(running.base, f.relative, 'Large source')).body.current;
    const beforeLargeDerive = (await request(running.base, '/api/state')).body.event_count;
    const oversizedSource = await derive(
      running.base,
      derivationRequest(largePublication, 'derive-source-limit')
    );
    assert.equal(oversizedSource.response.status, 409);
    assert.equal(oversizedSource.body.error, 'source_revision_unavailable');
    assert.equal(oversizedSource.body.reason, 'source_limit_exceeded');
    assert.equal((await request(running.base, '/api/state')).body.event_count, beforeLargeDerive);
    assert.equal(beforeLargeDerive, baseline + 1);
    assert.equal(
      (await request(running.base, '/api/canvas/operation-surfaces/operations-surface-unknown')).response.status,
      404
    );
  } finally {
    await cleanup(f, running);
  }
});

test('reports the exact blob as orphan residue when derivation event append fails', async () => {
  const f = await fixture('ide-extension-operations-orphan-');
  let appendCount = 0;
  const injectedAppend = async (...args) => {
    appendCount += 1;
    if (appendCount === 2) {
      const error = new Error('synthetic derivation append failure');
      error.code = 'synthetic_append_failure';
      throw error;
    }
    return appendEvent(...args);
  };
  let running;
  try {
    running = await start(f, { appendEvent: injectedAppend });
    const source = (await publish(running.base, f.relative)).body.current;
    const failed = await derive(running.base, derivationRequest(source, 'derive-orphan'));
    assert.equal(failed.response.status, 500);

    const state = (await request(running.base, '/api/state')).body;
    assert.equal(state.event_count, 1);
    assert.equal(Object.hasOwn(state.canvas, 'operations_v1'), false);
    assert.equal(state.reconciliation.canvas_blobs.blob_count, 1);
    assert.equal(state.reconciliation.canvas_blobs.unreferenced_blobs.length, 1);
  } finally {
    await cleanup(f, running);
  }
});

test('recovers an appended derivation after projection failure and exposes CLI derive', async () => {
  const f = await fixture('ide-extension-operations-cli-recovery-');
  let writeCount = 0;
  const writeProjection = async (...args) => {
    writeCount += 1;
    if (writeCount === 3) {
      const error = new Error('synthetic derivation projection failure');
      error.code = 'EIO';
      throw error;
    }
    return atomicWriteJson(...args);
  };
  let running;
  try {
    running = await start(f, { writeProjection });
    const source = (await publish(running.base, f.relative)).body.current;
    const input = derivationRequest(source, 'derive-recovery');
    const interrupted = await derive(running.base, input);
    assert.equal(interrupted.response.status, 503);
    assert.equal(interrupted.body.error, 'reconciliation_required');

    const recoveredState = (await request(running.base, '/api/state')).body;
    const recoveredId = recoveredState.canvas.operations_v1
      .derivation_keys['derive-recovery'].result_operations_surface_id;
    assert.equal(recoveredState.event_count, 2);
    assert.equal(
      recoveredState.reconciliation.canvas_blobs.unreferenced_blobs.length,
      0
    );
    assert.equal(
      (await request(
        running.base,
        `/api/canvas/operation-surfaces/${encodeURIComponent(recoveredId)}`
      )).response.status,
      200
    );

    const cliResult = await runCli([
      'derive',
      '--base-url', running.base,
      '--source-surface-id', source.surface_id,
      '--source-revision-id', source.revision.revision_id,
      '--idempotency-key', 'derive-cli'
    ]);
    assert.equal(cliResult.code, 0);
    assert.equal(cliResult.stderr, '');
    assert.equal(JSON.parse(cliResult.stdout).idempotent, false);

    const invalidCli = await runCli(['derive', '--base-url', running.base]);
    assert.equal(invalidCli.code, 2);
    assert.equal(JSON.parse(invalidCli.stderr).error, 'invalid_arguments');
  } finally {
    await cleanup(f, running);
  }
});
