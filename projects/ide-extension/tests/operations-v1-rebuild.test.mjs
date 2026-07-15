import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtemp, mkdir, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { appendEvent } from '../src/kernel/audit.mjs';
import { htmlTransformEngine } from '../src/kernel/html-transform.mjs';
import { OPERATIONS_V1_LIMITS } from '../src/kernel/operations-contracts.mjs';
import { atomicWriteJson } from '../src/kernel/storage.mjs';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const cli = path.join(projectRoot, 'scripts/session-bridge.mjs');
const INITIAL_HTML = '<!DOCTYPE html><html><head><title>Initial</title></head><body><main>Initial</main></body></html>';
const REBUILD_HTML = '<!doctype html><title>Rebuilt</title><main><button>Rebuilt</button></main>';

function digest(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

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

async function fixture(prefix = 'ide-extension-operations-rebuild-') {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), `${prefix}state-`));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), `${prefix}workspace-`));
  const sourcePath = 'presentations/source.html';
  const rebuildPath = 'sources/rebuild.html';
  const sourceFile = path.join(workspaceRoot, sourcePath);
  const rebuildFile = path.join(workspaceRoot, rebuildPath);
  await mkdir(path.dirname(sourceFile), { recursive: true });
  await mkdir(path.dirname(rebuildFile), { recursive: true });
  await writeFile(sourceFile, INITIAL_HTML, 'utf8');
  await writeFile(rebuildFile, REBUILD_HTML, 'utf8');
  return { stateDir, workspaceRoot, sourcePath, rebuildPath, sourceFile, rebuildFile };
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

async function publishAndDerive(running, f, key = 'derive-rebuild-source') {
  const published = await post(running.base, '/api/canvas/publish', {
    schema_version: '1',
    path: f.sourcePath,
    title: 'Rebuild source',
    kind: 'generic'
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

function rebuildInput(surface, expectedRevisionId, operationId, sourcePath, expectedSha256) {
  return {
    schema_version: '1',
    operation_id: operationId,
    operations_surface_id: surface.operations_surface_id,
    expected_revision_id: expectedRevisionId,
    mode: 'rebuild',
    target: { kind: 'whole_document' },
    input: {
      kind: 'workspace_html',
      path: sourcePath,
      expected_sha256: expectedSha256
    }
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

test('rebuilds exact workspace bytes with lineage, stable identity, restart, and no implicit V0 sync', async () => {
  const f = await fixture();
  let running;
  try {
    running = await start(f);
    const { v0, derived } = await publishAndDerive(running, f);
    const sourceBytes = Buffer.from(REBUILD_HTML);
    const input = rebuildInput(
      derived.surface,
      derived.revision.revision_id,
      'operation-rebuild-exact',
      f.rebuildPath,
      digest(sourceBytes)
    );
    const rebuilt = await operate(running.base, derived.surface.operations_surface_id, input);
    const expected = htmlTransformEngine.replace(REBUILD_HTML);

    assert.equal(rebuilt.response.status, 201);
    assert.equal(rebuilt.body.operation.mode, 'rebuild');
    assert.deepEqual(rebuilt.body.operation.source_lineage, {
      kind: 'workspace_html',
      path: f.rebuildPath,
      expected_sha256: digest(sourceBytes)
    });
    assert.equal(rebuilt.body.operation.input_digest, digest(sourceBytes));
    assert.equal(rebuilt.body.surface.operations_surface_id, derived.surface.operations_surface_id);
    assert.deepEqual((await request(running.base, rebuilt.body.content_url)).body, expected.bytes);
    assert.equal(
      (await request(running.base, '/api/canvas/current')).body.current.revision.revision_id,
      v0.revision.revision_id
    );

    const publishedRebuildSource = await post(running.base, '/api/canvas/publish', {
      schema_version: '1',
      path: f.rebuildPath,
      title: 'Explicit V0 publication',
      kind: 'generic'
    });
    assert.equal(publishedRebuildSource.response.status, 201);
    const metadataRoute = `/api/canvas/operation-surfaces/${derived.surface.operations_surface_id}`;
    assert.equal(
      (await request(running.base, metadataRoute)).body.revision.revision_id,
      rebuilt.body.revision.revision_id
    );

    await close(running.server);
    running = await start(f);
    assert.deepEqual((await request(running.base, rebuilt.body.content_url)).body, expected.bytes);
    assert.equal(
      (await request(running.base, metadataRoute)).body.surface.operations_surface_id,
      derived.surface.operations_surface_id
    );
  } finally {
    await cleanup(f, running);
  }
});

test('returns exact retry after source changes and checks operation id and CAS before reread', async () => {
  const f = await fixture('ide-extension-operations-rebuild-retry-');
  let running;
  try {
    running = await start(f);
    const { derived } = await publishAndDerive(running, f, 'derive-rebuild-retry');
    const sourceDigest = digest(Buffer.from(REBUILD_HTML));
    const input = rebuildInput(
      derived.surface,
      derived.revision.revision_id,
      'operation-rebuild-retry',
      f.rebuildPath,
      sourceDigest
    );
    const first = (await operate(running.base, derived.surface.operations_surface_id, input)).body;
    await writeFile(f.rebuildFile, '<h1>changed after commit</h1>', 'utf8');

    const retry = await operate(running.base, derived.surface.operations_surface_id, input);
    assert.equal(retry.response.status, 200);
    assert.equal(retry.body.idempotent, true);
    assert.deepEqual(retry.body.surface, first.surface);
    assert.equal(retry.body.revision.revision_id, first.revision.revision_id);

    const conflict = await operate(running.base, derived.surface.operations_surface_id, {
      ...input,
      input: { ...input.input, expected_sha256: 'b'.repeat(64) }
    });
    assert.equal(conflict.response.status, 409);
    assert.equal(conflict.body.error, 'operation_id_conflict');

    await rm(f.rebuildFile);
    const stale = await operate(
      running.base,
      derived.surface.operations_surface_id,
      rebuildInput(
        first.surface,
        derived.revision.revision_id,
        'operation-rebuild-stale',
        f.rebuildPath,
        sourceDigest
      )
    );
    assert.equal(stale.response.status, 409);
    assert.equal(stale.body.error, 'revision_changed');
  } finally {
    await cleanup(f, running);
  }
});

test('rejects digest drift, missing, directory, and external-link sources without events', async () => {
  const f = await fixture('ide-extension-operations-rebuild-paths-');
  const outsideDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-rebuild-outside-'));
  let running;
  try {
    running = await start(f);
    const { derived } = await publishAndDerive(running, f, 'derive-rebuild-paths');
    const surfaceId = derived.surface.operations_surface_id;
    const revisionId = derived.revision.revision_id;
    const baseline = (await request(running.base, '/api/state')).body.event_count;

    const changed = await operate(
      running.base,
      surfaceId,
      rebuildInput(derived.surface, revisionId, 'operation-rebuild-drift', f.rebuildPath, 'a'.repeat(64))
    );
    assert.equal(changed.response.status, 409);
    assert.equal(changed.body.error, 'rebuild_source_changed');
    assert.equal(changed.body.actual_sha256, digest(Buffer.from(REBUILD_HTML)));

    const missing = await operate(
      running.base,
      surfaceId,
      rebuildInput(derived.surface, revisionId, 'operation-rebuild-missing', 'sources/missing.html', 'a'.repeat(64))
    );
    assert.equal(missing.response.status, 409);
    assert.equal(missing.body.error, 'rebuild_source_unavailable');

    const directoryPath = path.join(f.workspaceRoot, 'sources/directory.html');
    await mkdir(directoryPath);
    const directory = await operate(
      running.base,
      surfaceId,
      rebuildInput(derived.surface, revisionId, 'operation-rebuild-directory', 'sources/directory.html', 'a'.repeat(64))
    );
    assert.equal(directory.response.status, 409);
    assert.equal(directory.body.error, 'rebuild_source_unavailable');

    const outsideFile = path.join(outsideDir, 'outside.html');
    await writeFile(outsideFile, '<h1>outside</h1>', 'utf8');
    await symlink(outsideFile, path.join(f.workspaceRoot, 'sources/external.html'));
    const external = await operate(
      running.base,
      surfaceId,
      rebuildInput(derived.surface, revisionId, 'operation-rebuild-external', 'sources/external.html', digest(Buffer.from('<h1>outside</h1>')))
    );
    assert.equal(external.response.status, 409);
    assert.equal(external.body.error, 'rebuild_source_unavailable');
    assert.equal((await request(running.base, '/api/state')).body.event_count, baseline);
  } finally {
    await cleanup(f, running);
    await rm(outsideDir, { recursive: true, force: true });
  }
});

test('admits exact multibyte source limit and rejects plus-one bytes and invalid UTF-8', async () => {
  const f = await fixture('ide-extension-operations-rebuild-limits-');
  let running;
  try {
    running = await start(f);
    const { derived } = await publishAndDerive(running, f, 'derive-rebuild-limits');
    const prefix = '<p>a';
    const suffix = '</p>';
    const exactTextBytes = OPERATIONS_V1_LIMITS.source_html_bytes
      - Buffer.byteLength(prefix)
      - Buffer.byteLength(suffix);
    const exactHtml = `${prefix}${'\u00e9'.repeat(exactTextBytes / 2)}${suffix}`;
    assert.equal(Buffer.byteLength(exactHtml), OPERATIONS_V1_LIMITS.source_html_bytes);
    await writeFile(f.rebuildFile, exactHtml, 'utf8');
    const exactDigest = digest(Buffer.from(exactHtml));
    const exact = await operate(
      running.base,
      derived.surface.operations_surface_id,
      rebuildInput(
        derived.surface,
        derived.revision.revision_id,
        'operation-rebuild-limit-exact',
        f.rebuildPath,
        exactDigest
      )
    );
    assert.equal(exact.response.status, 201);

    await writeFile(f.rebuildFile, `${exactHtml}x`, 'utf8');
    const plusBytes = Buffer.from(`${exactHtml}x`);
    const beforePlus = (await request(running.base, '/api/state')).body.event_count;
    const plus = await operate(
      running.base,
      derived.surface.operations_surface_id,
      rebuildInput(
        exact.body.surface,
        exact.body.revision.revision_id,
        'operation-rebuild-limit-plus',
        f.rebuildPath,
        digest(plusBytes)
      )
    );
    assert.equal(plus.response.status, 413);
    assert.equal(plus.body.limit_name, 'source_html');
    assert.equal((await request(running.base, '/api/state')).body.event_count, beforePlus);

    const invalidBytes = Buffer.from([0xff, 0xfe, 0x3c, 0x70, 0x3e]);
    await writeFile(f.rebuildFile, invalidBytes);
    const invalid = await operate(
      running.base,
      derived.surface.operations_surface_id,
      rebuildInput(
        exact.body.surface,
        exact.body.revision.revision_id,
        'operation-rebuild-invalid-utf8',
        f.rebuildPath,
        digest(invalidBytes)
      )
    );
    assert.equal(invalid.response.status, 422);
    assert.equal(invalid.body.error, 'operations_source_invalid_utf8');
  } finally {
    await cleanup(f, running);
  }
});

test('allows rebuild to the same serialized digest with a new operation and revision', async () => {
  const f = await fixture('ide-extension-operations-rebuild-same-');
  let running;
  try {
    running = await start(f);
    const { derived } = await publishAndDerive(running, f, 'derive-rebuild-same');
    const current = await request(running.base, derived.content_url);
    await writeFile(f.rebuildFile, current.body);
    const rebuilt = await operate(
      running.base,
      derived.surface.operations_surface_id,
      rebuildInput(
        derived.surface,
        derived.revision.revision_id,
        'operation-rebuild-same',
        f.rebuildPath,
        digest(current.body)
      )
    );
    assert.equal(rebuilt.response.status, 201);
    assert.notEqual(rebuilt.body.revision.revision_id, derived.revision.revision_id);
    assert.equal(rebuilt.body.revision.blob_ref, derived.revision.blob_ref);
  } finally {
    await cleanup(f, running);
  }
});

test('reports orphan result on append failure and repairs projection failure', async () => {
  const orphanFixture = await fixture('ide-extension-operations-rebuild-orphan-');
  let appendCount = 0;
  const injectedAppend = async (...args) => {
    appendCount += 1;
    if (appendCount === 3) {
      const error = new Error('synthetic rebuild event failure');
      error.code = 'synthetic_append_failure';
      throw error;
    }
    return appendEvent(...args);
  };
  let orphanRunning;
  try {
    orphanRunning = await start(orphanFixture, { appendEvent: injectedAppend });
    const { derived } = await publishAndDerive(orphanRunning, orphanFixture, 'derive-rebuild-orphan');
    const failed = await operate(
      orphanRunning.base,
      derived.surface.operations_surface_id,
      rebuildInput(
        derived.surface,
        derived.revision.revision_id,
        'operation-rebuild-orphan',
        orphanFixture.rebuildPath,
        digest(Buffer.from(REBUILD_HTML))
      )
    );
    assert.equal(failed.response.status, 500);
    const state = (await request(orphanRunning.base, '/api/state')).body;
    assert.equal(state.event_count, 2);
    assert.deepEqual(
      state.reconciliation.canvas_blobs.unreferenced_blobs,
      [htmlTransformEngine.replace(REBUILD_HTML).sha256]
    );
  } finally {
    await cleanup(orphanFixture, orphanRunning);
  }

  const recoveryFixture = await fixture('ide-extension-operations-rebuild-recovery-');
  let writeCount = 0;
  const writeProjection = async (...args) => {
    writeCount += 1;
    if (writeCount === 4) {
      const error = new Error('synthetic rebuild projection failure');
      error.code = 'EIO';
      throw error;
    }
    return atomicWriteJson(...args);
  };
  let recoveryRunning;
  try {
    recoveryRunning = await start(recoveryFixture, { writeProjection });
    const { derived } = await publishAndDerive(recoveryRunning, recoveryFixture, 'derive-rebuild-recovery');
    const interrupted = await operate(
      recoveryRunning.base,
      derived.surface.operations_surface_id,
      rebuildInput(
        derived.surface,
        derived.revision.revision_id,
        'operation-rebuild-recovery',
        recoveryFixture.rebuildPath,
        digest(Buffer.from(REBUILD_HTML))
      )
    );
    assert.equal(interrupted.response.status, 503);
    const state = (await request(recoveryRunning.base, '/api/state')).body;
    assert.equal(state.event_count, 3);
    assert.equal(state.canvas.operations_v1.operations['operation-rebuild-recovery'].mode, 'rebuild');
    assert.equal(state.reconciliation.canvas_blobs.unreferenced_blobs.length, 0);
  } finally {
    await cleanup(recoveryFixture, recoveryRunning);
  }
});

test('runs rebuild through the generic one-shot CLI operate command', async () => {
  const f = await fixture('ide-extension-operations-rebuild-cli-');
  let running;
  try {
    running = await start(f);
    const { derived } = await publishAndDerive(running, f, 'derive-rebuild-cli');
    const input = rebuildInput(
      derived.surface,
      derived.revision.revision_id,
      'operation-rebuild-cli',
      f.rebuildPath,
      digest(Buffer.from(REBUILD_HTML))
    );
    const inputFile = path.join(f.workspaceRoot, 'rebuild-operation.json');
    await writeFile(inputFile, JSON.stringify(input), 'utf8');
    const result = await runCli([
      'operate',
      '--base-url', running.base,
      '--surface-id', derived.surface.operations_surface_id,
      '--input', inputFile
    ]);
    assert.equal(result.code, 0);
    assert.equal(result.stderr, '');
    const rebuilt = JSON.parse(result.stdout);
    assert.equal(rebuilt.operation.mode, 'rebuild');
    assert.equal(rebuilt.operation.source_lineage.path, f.rebuildPath);
  } finally {
    await cleanup(f, running);
  }
});
