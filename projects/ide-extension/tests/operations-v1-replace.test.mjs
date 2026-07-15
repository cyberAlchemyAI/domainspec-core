import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { appendEvent } from '../src/kernel/audit.mjs';
import { htmlTransformEngine } from '../src/kernel/html-transform.mjs';
import { OPERATIONS_V1_EVENT_VERSION, OPERATIONS_V1_LIMITS } from '../src/kernel/operations-contracts.mjs';
import { atomicWriteJson } from '../src/kernel/storage.mjs';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const cli = path.join(projectRoot, 'scripts/session-bridge.mjs');
const INITIAL_HTML = '<!doctype html><title>Source</title><main>Initial</main>';
const REPLACEMENT_A = '<!doctype html><title>Replacement A</title><main><button>A</button></main>';
const REPLACEMENT_B = '<!doctype html><title>Replacement B</title><main><button>B</button></main>';

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
      : Buffer.from(await response.arrayBuffer())
  };
}

function post(base, route, body) {
  return request(base, route, { method: 'POST', body: JSON.stringify(body) });
}

async function fixture(prefix = 'ide-extension-operations-replace-') {
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

async function publishAndDerive(running, f, key = 'derive-replace-source') {
  const published = await post(running.base, '/api/canvas/publish', {
    schema_version: '1',
    path: f.relative,
    title: 'Replacement source',
    kind: 'presentation'
  });
  const v0 = published.body.current;
  const derived = await post(running.base, '/api/canvas/operation-surfaces', {
    schema_version: '1',
    source_v0_surface_id: v0.surface_id,
    source_revision_id: v0.revision.revision_id,
    operation_surface_idempotency_key: key
  });
  return { v0, derived: derived.body };
}

function operationInput(surface, expectedRevisionId, operationId, html, mode = 'replace') {
  return {
    schema_version: '1',
    operation_id: operationId,
    operations_surface_id: surface.operations_surface_id,
    expected_revision_id: expectedRevisionId,
    mode,
    target: { kind: 'whole_document' },
    input: { kind: 'inline_html', html }
  };
}

function operate(base, surfaceId, body) {
  return post(
    base,
    `/api/canvas/operation-surfaces/${encodeURIComponent(surfaceId)}/operations`,
    body
  );
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

test('replaces through parse5 and serves immutable old/new content after restart', async () => {
  const f = await fixture();
  let running;
  try {
    running = await start(f);
    const { v0, derived } = await publishAndDerive(running, f);
    const input = operationInput(
      derived.surface,
      derived.revision.revision_id,
      'operation-replace-a',
      REPLACEMENT_A
    );
    const replaced = await operate(running.base, derived.surface.operations_surface_id, input);
    const expected = htmlTransformEngine.replace(REPLACEMENT_A);

    assert.equal(replaced.response.status, 201);
    assert.equal(replaced.body.idempotent, false);
    assert.equal(replaced.body.surface.operations_surface_id, derived.surface.operations_surface_id);
    assert.deepEqual(
      replaced.body.surface.revision_ids,
      [derived.revision.revision_id, replaced.body.revision.revision_id]
    );
    assert.equal(replaced.body.revision.content_sha256, expected.sha256);
    assert.deepEqual((await request(running.base, replaced.body.content_url)).body, expected.bytes);
    assert.deepEqual((await request(running.base, derived.content_url)).body, Buffer.from(INITIAL_HTML));
    assert.equal(
      (await request(running.base, '/api/canvas/current')).body.current.revision.revision_id,
      v0.revision.revision_id
    );

    const metadataRoute = `/api/canvas/operation-surfaces/${encodeURIComponent(derived.surface.operations_surface_id)}`;
    assert.equal((await request(running.base, metadataRoute)).body.content_url, replaced.body.content_url);
    await close(running.server);
    running = await start(f);
    assert.deepEqual((await request(running.base, replaced.body.content_url)).body, expected.bytes);
    assert.deepEqual((await request(running.base, derived.content_url)).body, Buffer.from(INITIAL_HTML));
  } finally {
    await cleanup(f, running);
  }
});

test('returns exact retries after advance, rejects conflicts/stale input, and shares result blobs', async () => {
  const f = await fixture('ide-extension-operations-retry-');
  let running;
  try {
    running = await start(f);
    const { derived } = await publishAndDerive(running, f, 'derive-retry-source');
    const surfaceId = derived.surface.operations_surface_id;
    const opA = operationInput(
      derived.surface,
      derived.revision.revision_id,
      'operation-retry-a',
      REPLACEMENT_A
    );
    const first = (await operate(running.base, surfaceId, opA)).body;
    const opB = operationInput(first.surface, first.revision.revision_id, 'operation-retry-b', REPLACEMENT_B);
    const second = (await operate(running.base, surfaceId, opB)).body;

    const retry = await operate(running.base, surfaceId, opA);
    assert.equal(retry.response.status, 200);
    assert.equal(retry.body.idempotent, true);
    assert.equal(retry.body.revision.revision_id, first.revision.revision_id);
    assert.equal(retry.body.operation.operation_id, first.operation.operation_id);
    assert.deepEqual(retry.body.surface, first.surface);

    const conflict = await operate(
      running.base,
      surfaceId,
      { ...opA, input: { kind: 'inline_html', html: '<h1>different</h1>' } }
    );
    assert.equal(conflict.response.status, 409);
    assert.equal(conflict.body.error, 'operation_id_conflict');

    const stale = await operate(
      running.base,
      surfaceId,
      operationInput(second.surface, derived.revision.revision_id, 'operation-stale', '<h1>stale</h1>')
    );
    assert.equal(stale.response.status, 409);
    assert.equal(stale.body.error, 'revision_changed');
    assert.equal(stale.body.current_revision_id, second.revision.revision_id);

    const sameResult = await operate(
      running.base,
      surfaceId,
      operationInput(second.surface, second.revision.revision_id, 'operation-same-result', REPLACEMENT_B)
    );
    assert.equal(sameResult.response.status, 201);
    assert.notEqual(sameResult.body.revision.revision_id, second.revision.revision_id);
    assert.equal(sameResult.body.revision.blob_ref, second.revision.blob_ref);
    assert.equal(sameResult.body.surface.revision_ids.length, 4);
  } finally {
    await cleanup(f, running);
  }
});

test('allows one of two concurrent stale writers to commit', async () => {
  const f = await fixture('ide-extension-operations-cas-race-');
  let running;
  try {
    running = await start(f);
    const { derived } = await publishAndDerive(running, f, 'derive-cas-race');
    const surfaceId = derived.surface.operations_surface_id;
    const attempts = await Promise.all([
      operate(running.base, surfaceId, operationInput(
        derived.surface,
        derived.revision.revision_id,
        'operation-race-a',
        REPLACEMENT_A
      )),
      operate(running.base, surfaceId, operationInput(
        derived.surface,
        derived.revision.revision_id,
        'operation-race-b',
        REPLACEMENT_B
      ))
    ]);
    assert.equal(attempts.filter(({ response }) => response.status === 201).length, 1);
    assert.equal(attempts.filter(({ response }) => response.status === 409).length, 1);
    assert.equal(attempts.find(({ response }) => response.status === 409).body.error, 'revision_changed');
    const state = (await request(running.base, '/api/state')).body;
    assert.equal(Object.keys(state.canvas.operations_v1.operations).length, 1);
    assert.equal(state.canvas.operations_v1.surfaces[surfaceId].revision_ids.length, 2);
  } finally {
    await cleanup(f, running);
  }
});

test('rejects missing rebuild sources, bindings, unknown surfaces, and input/result limits without events', async () => {
  const f = await fixture('ide-extension-operations-replace-limits-');
  let running;
  try {
    running = await start(f);
    const { derived } = await publishAndDerive(running, f, 'derive-replace-limits');
    const surfaceId = derived.surface.operations_surface_id;
    const revisionId = derived.revision.revision_id;
    const baseline = (await request(running.base, '/api/state')).body.event_count;

    const rebuild = await operate(running.base, surfaceId, {
      schema_version: '1',
      operation_id: 'operation-rebuild-unavailable',
      operations_surface_id: surfaceId,
      expected_revision_id: revisionId,
      mode: 'rebuild',
      target: { kind: 'whole_document' },
      input: {
        kind: 'workspace_html',
        path: 'presentations/rebuild.html',
        expected_sha256: 'a'.repeat(64)
      }
    });
    assert.equal(rebuild.response.status, 409);
    assert.equal(rebuild.body.error, 'rebuild_source_unavailable');

    const binding = await operate(
      running.base,
      'operations-surface-other',
      operationInput(derived.surface, revisionId, 'operation-binding', REPLACEMENT_A)
    );
    assert.equal(binding.response.status, 409);
    assert.equal(binding.body.error, 'operations_surface_binding_mismatch');

    const unknown = await operate(running.base, 'operations-surface-unknown', {
      ...operationInput(derived.surface, revisionId, 'operation-unknown', REPLACEMENT_A),
      operations_surface_id: 'operations-surface-unknown'
    });
    assert.equal(unknown.response.status, 404);
    assert.equal(unknown.body.error, 'operations_surface_not_found');

    const inputLimit = await operate(
      running.base,
      surfaceId,
      operationInput(
        derived.surface,
        revisionId,
        'operation-input-limit',
        'x'.repeat(OPERATIONS_V1_LIMITS.source_html_bytes + 1)
      )
    );
    assert.equal(inputLimit.response.status, 413);
    assert.equal(inputLimit.body.error, 'operations_byte_limit_exceeded');
    assert.equal(inputLimit.body.limit_name, 'source_html');

    const expandingHtml = `<!doctype html><p>${'&'.repeat(2 * 1024 * 1024)}</p>`;
    const resultLimit = await operate(
      running.base,
      surfaceId,
      operationInput(derived.surface, revisionId, 'operation-result-limit', expandingHtml)
    );
    assert.equal(resultLimit.response.status, 413);
    assert.equal(resultLimit.body.error, 'operations_byte_limit_exceeded');
    assert.equal(resultLimit.body.limit_name, 'result_html');
    assert.equal((await request(running.base, '/api/state')).body.event_count, baseline);
  } finally {
    await cleanup(f, running);
  }
});

test('reports an unreferenced result blob when operation event append fails', async () => {
  const f = await fixture('ide-extension-operations-replace-orphan-');
  let appendCount = 0;
  const injectedAppend = async (...args) => {
    appendCount += 1;
    if (appendCount === 3) {
      const error = new Error('synthetic operation append failure');
      error.code = 'synthetic_append_failure';
      throw error;
    }
    return appendEvent(...args);
  };
  let running;
  try {
    running = await start(f, { appendEvent: injectedAppend });
    const { derived } = await publishAndDerive(running, f, 'derive-operation-orphan');
    const failed = await operate(
      running.base,
      derived.surface.operations_surface_id,
      operationInput(derived.surface, derived.revision.revision_id, 'operation-orphan', REPLACEMENT_A)
    );
    assert.equal(failed.response.status, 500);
    const state = (await request(running.base, '/api/state')).body;
    assert.equal(state.event_count, 2);
    assert.equal(Object.keys(state.canvas.operations_v1.operations).length, 0);
    assert.equal(state.reconciliation.canvas_blobs.unreferenced_blobs.length, 1);
    assert.equal(
      state.reconciliation.canvas_blobs.unreferenced_blobs[0],
      htmlTransformEngine.replace(REPLACEMENT_A).sha256
    );
  } finally {
    await cleanup(f, running);
  }
});

test('repairs an appended operation after projection failure', async () => {
  const f = await fixture('ide-extension-operations-replace-recovery-');
  let writeCount = 0;
  const writeProjection = async (...args) => {
    writeCount += 1;
    if (writeCount === 4) {
      const error = new Error('synthetic operation projection failure');
      error.code = 'EIO';
      throw error;
    }
    return atomicWriteJson(...args);
  };
  let running;
  try {
    running = await start(f, { writeProjection });
    const { derived } = await publishAndDerive(running, f, 'derive-operation-recovery');
    const interrupted = await operate(
      running.base,
      derived.surface.operations_surface_id,
      operationInput(derived.surface, derived.revision.revision_id, 'operation-recovery', REPLACEMENT_A)
    );
    assert.equal(interrupted.response.status, 503);
    assert.equal(interrupted.body.error, 'reconciliation_required');

    const state = (await request(running.base, '/api/state')).body;
    const operation = state.canvas.operations_v1.operations['operation-recovery'];
    const contentUrl = `/api/canvas/operation-surfaces/${derived.surface.operations_surface_id}`
      + `/revisions/${operation.result_revision_id}/content`;
    assert.equal(state.event_count, 3);
    assert.deepEqual(
      (await request(running.base, contentUrl)).body,
      htmlTransformEngine.replace(REPLACEMENT_A).bytes
    );
    assert.equal(state.reconciliation.canvas_blobs.unreferenced_blobs.length, 0);
  } finally {
    await cleanup(f, running);
  }
});

test('operates through the CLI and returns 410 after a durable prune tombstone', async () => {
  const f = await fixture('ide-extension-operations-replace-cli-prune-');
  let running;
  try {
    running = await start(f);
    const { derived } = await publishAndDerive(running, f, 'derive-cli-prune');
    const input = operationInput(
      derived.surface,
      derived.revision.revision_id,
      'operation-cli-replace',
      REPLACEMENT_A
    );
    const inputFile = path.join(f.workspaceRoot, 'operation.json');
    await writeFile(inputFile, JSON.stringify(input), 'utf8');
    const cliResult = await runCli([
      'operate',
      '--base-url', running.base,
      '--surface-id', derived.surface.operations_surface_id,
      '--input', inputFile
    ]);
    assert.equal(cliResult.code, 0);
    assert.equal(cliResult.stderr, '');
    assert.equal(JSON.parse(cliResult.stdout).operation.operation_id, 'operation-cli-replace');

    const invalidCli = await runCli(['operate', '--base-url', running.base]);
    assert.equal(invalidCli.code, 2);
    assert.equal(JSON.parse(invalidCli.stderr).error, 'invalid_arguments');

    await close(running.server);
    running = null;
    const requestedAt = '2026-07-14T22:30:00.000Z';
    await appendEvent(path.join(f.stateDir, 'events.jsonl'), {
      event_version: OPERATIONS_V1_EVENT_VERSION,
      event_id: 'event-test-pruning-requested',
      event_type: 'canvas.pruning_requested',
      pruning_request: {
        pruning_request_id: 'pruning-request-test',
        observed_bytes: OPERATIONS_V1_LIMITS.retention_soft_bytes,
        soft_limit_bytes: OPERATIONS_V1_LIMITS.retention_soft_bytes,
        hard_limit_bytes: OPERATIONS_V1_LIMITS.retention_hard_bytes,
        grace_deadline: '2026-07-21T22:30:00.000Z',
        requested_at: requestedAt
      },
      created_at: requestedAt
    });
    await appendEvent(path.join(f.stateDir, 'events.jsonl'), {
      event_version: OPERATIONS_V1_EVENT_VERSION,
      event_id: 'event-test-revision-pruned',
      event_type: 'canvas.revision_pruned',
      tombstone: {
        pruning_request_id: 'pruning-request-test',
        revision_id: derived.revision.revision_id,
        operations_surface_id: derived.surface.operations_surface_id,
        content_sha256: derived.revision.content_sha256,
        blob_ref: derived.revision.blob_ref,
        reason: 'manual',
        retention_state_after: 'normal',
        pruned_at: '2026-07-14T22:31:00.000Z'
      },
      created_at: '2026-07-14T22:31:00.000Z'
    });
    running = await start(f);
    const pruned = await request(running.base, derived.content_url);
    assert.equal(pruned.response.status, 410);
    assert.equal(pruned.body.error, 'revision_pruned');
    assert.equal(pruned.body.tombstone.revision_id, derived.revision.revision_id);
    assert.equal(
      (await request(running.base, JSON.parse(cliResult.stdout).content_url)).response.status,
      200
    );
  } finally {
    await cleanup(f, running);
  }
});
