import assert from 'node:assert/strict';
import {
  access,
  mkdir,
  mkdtemp,
  readFile,
  rm,
  writeFile
} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { appendEvent, readEvents } from '../src/kernel/audit.mjs';
import { createCanvasBlobStore } from '../src/kernel/canvas-blobs.mjs';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const BASE_POLICY = Object.freeze({
  soft_bytes: 2500,
  hard_bytes: 3500,
  grace_ms: 100,
  reclaim_below_bytes: 2500
});

function html(label, fill = 'x') {
  return `<!doctype html><html><head><title>${label}</title></head><body>`
    + `<main data-label="${label}">${label}-${fill.repeat(1800)}</main></body></html>`;
}

function mutableClock(start = Date.parse('2026-07-15T00:30:00.000Z')) {
  let value = start;
  return {
    now: () => new Date(value).toISOString(),
    advance: (milliseconds) => { value += milliseconds; }
  };
}

function retentionIds(prefix = 'retention-auto') {
  let value = 0;
  return () => `${prefix}-${++value}`;
}

function fakeTimers() {
  let sequence = 0;
  const tasks = new Map();
  return {
    setTimer(callback, delay) {
      const handle = { id: ++sequence, unref() {} };
      tasks.set(handle, { callback, delay });
      return handle;
    },
    clearTimer(handle) {
      tasks.delete(handle);
    },
    fireNext() {
      const entry = tasks.entries().next().value;
      assert.ok(entry, 'expected one scheduled retention timer');
      const [handle, task] = entry;
      tasks.delete(handle);
      task.callback();
      return task.delay;
    },
    get size() {
      return tasks.size;
    }
  };
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
  const body = contentType.includes('application/json')
    ? JSON.parse(await response.text())
    : Buffer.from(await response.arrayBuffer());
  return { response, body };
}

function post(base, route, body) {
  return request(base, route, { method: 'POST', body: JSON.stringify(body) });
}

async function fixture(prefix) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), `${prefix}-state-`));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), `${prefix}-workspace-`));
  const relative = 'presentations/source.html';
  const file = path.join(workspaceRoot, relative);
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, html('source', 's'), 'utf8');
  return { stateDir, workspaceRoot, relative };
}

async function start(f, options = {}) {
  const clock = options.clock || mutableClock();
  const policy = options.policy || BASE_POLICY;
  const server = createServer({
    rootDir: projectRoot,
    stateDir: f.stateDir,
    workspaceRoot: f.workspaceRoot,
    retentionPolicy: policy,
    retentionNow: clock.now,
    retentionRandomId: retentionIds(),
    canvasBlobStore: options.canvasBlobStore,
    appendEvent: options.appendEvent,
    retentionSetTimeout: options.timers?.setTimer.bind(options.timers),
    retentionClearTimeout: options.timers?.clearTimer.bind(options.timers)
  });
  const runtime = await server.ready;
  const port = await listen(server);
  return { server, runtime, clock, base: `http://127.0.0.1:${port}` };
}

async function cleanup(f, running) {
  if (running?.server.listening) await close(running.server);
  else running?.server.canvasRetention.close();
  await rm(f.stateDir, { recursive: true, force: true });
  await rm(f.workspaceRoot, { recursive: true, force: true });
}

async function publishAndDerive(running, f, key = 'derive-retention-auto') {
  const published = await post(running.base, '/api/canvas/publish', {
    schema_version: '1',
    path: f.relative,
    title: 'Automatic retention source',
    kind: 'presentation'
  });
  assert.equal(published.response.status, 201);
  const derived = await post(running.base, '/api/canvas/operation-surfaces', {
    schema_version: '1',
    source_v0_surface_id: published.body.current.surface_id,
    source_revision_id: published.body.current.revision.revision_id,
    operation_surface_idempotency_key: key
  });
  assert.equal(derived.response.status, 201);
  return derived.body;
}

async function operate(running, current, operationId, replacement) {
  const result = await post(
    running.base,
    `/api/canvas/operation-surfaces/${current.surface.operations_surface_id}/operations`,
    {
      schema_version: '1',
      operation_id: operationId,
      operations_surface_id: current.surface.operations_surface_id,
      expected_revision_id: current.revision.revision_id,
      mode: 'replace',
      target: { kind: 'whole_document' },
      input: { kind: 'inline_html', html: replacement }
    }
  );
  assert.equal(result.response.status, 201);
  return result.body;
}

async function state(running) {
  return (await request(running.base, '/api/state')).body;
}

async function waitFor(predicate, timeoutMs = 2000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (await predicate()) return;
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
  assert.fail('timed out waiting for automatic retention');
}

test('hard crossing prunes shared history once and completes below soft', async () => {
  const f = await fixture('ide-extension-retention-auto-hard');
  let running;
  try {
    running = await start(f, {
      policy: { ...BASE_POLICY, hard_bytes: 5000, grace_ms: 100000 }
    });
    const derived = await publishAndDerive(running, f);
    const source = await request(running.base, derived.content_url);
    const normalized = await operate(
      running,
      derived,
      'operation-auto-normalized',
      source.body.toString('utf8')
    );
    const normalizedSource = await request(running.base, normalized.content_url);
    const shared = await operate(
      running,
      normalized,
      'operation-auto-shared',
      normalizedSource.body.toString('utf8')
    );
    assert.equal(shared.revision.content_sha256, normalized.revision.content_sha256);
    await operate(running, shared, 'operation-auto-unique', html('unique', 'u'));

    const projection = (await state(running)).canvas.operations_v1;
    const events = await readEvents(path.join(f.stateDir, 'events.jsonl'));
    const tombstones = events.filter((event) => event.event_type === 'canvas.revision_pruned');
    const completion = events.find((event) => event.event_type === 'canvas.pruning_completed');
    assert.equal(running.server.canvasRetention.lastAutomaticResult.status, 'completed');
    assert.equal(running.server.canvasRetention.lastAutomaticResult.trigger, 'hard_threshold');
    assert.equal(tombstones.length, 3);
    assert.equal(
      tombstones.filter((event) => (
        event.tombstone.content_sha256 === shared.revision.content_sha256
      )).length,
      2
    );
    assert.equal(tombstones.every((event) => event.tombstone.reason === 'automatic'), true);
    assert.equal(tombstones.every((event) => event.tombstone.retention_state_after === 'reclaiming'), true);
    assert.ok(completion);
    assert.equal(projection.pruning.state, 'normal');
    assert.equal(projection.pruning.active_request, null);
  } finally {
    await cleanup(f, running);
  }
});

test('restart after grace expiry reclaims immediately and close cancels its timer', async () => {
  const f = await fixture('ide-extension-retention-auto-restart');
  const clock = mutableClock();
  const timers = fakeTimers();
  const policy = { ...BASE_POLICY, hard_bytes: 10000 };
  let running;
  try {
    running = await start(f, { clock, timers, policy });
    const derived = await publishAndDerive(running, f);
    await operate(running, derived, 'operation-auto-grace', html('grace', 'g'));
    assert.equal(running.server.canvasRetention.lastAutomaticResult.status, 'scheduled');
    assert.equal(timers.size, 1);
    await close(running.server);
    assert.equal(timers.size, 0);
    clock.advance(policy.grace_ms + 1);

    running = await start(f, { clock, policy });
    assert.equal(running.runtime.automaticRetention.status, 'completed');
    assert.equal(running.runtime.automaticRetention.trigger, 'grace_expired');
    const projection = (await state(running)).canvas.operations_v1;
    assert.equal(projection.pruning.state, 'normal');
    assert.equal(projection.pruning.active_request, null);
  } finally {
    await cleanup(f, running);
  }
});

test('orphan and temporary cleanup alone emits durable pruning completion', async () => {
  const f = await fixture('ide-extension-retention-auto-orphan');
  const blobStore = createCanvasBlobStore({ stateDir: f.stateDir });
  const policy = { ...BASE_POLICY, hard_bytes: 5000 };
  let running;
  try {
    running = await start(f, { canvasBlobStore: blobStore, policy });
    await publishAndDerive(running, f);
    const orphan = await blobStore.put(Buffer.from(`<p>${'o'.repeat(4000)}</p>`));
    const temporaryPath = path.join(blobStore.blob_dir, '.stale-retention.tmp');
    await writeFile(temporaryPath, 't'.repeat(123), 'utf8');

    const result = await running.server.canvasRetention.evaluateAutomatic(
      running.runtime.reduceOptions,
      { source: 'orphan-only-test' }
    );
    const events = await readEvents(path.join(f.stateDir, 'events.jsonl'));
    assert.equal(result.status, 'completed');
    assert.equal(result.trigger, 'hard_threshold');
    assert.equal(result.reclaimed.orphan_bytes, orphan.byte_length);
    assert.equal(result.reclaimed.temporary_bytes, 123);
    assert.equal(events.some((event) => event.event_type === 'canvas.revision_pruned'), false);
    assert.equal(events.some((event) => event.event_type === 'canvas.pruning_completed'), true);
    await assert.rejects(access(temporaryPath));
    await assert.rejects(blobStore.read(orphan.sha256), { code: 'canvas_blob_not_found' });
  } finally {
    await cleanup(f, running);
  }
});

test('deadline timer and manual commit serialize without duplicate pruning', async () => {
  const f = await fixture('ide-extension-retention-auto-race');
  const clock = mutableClock();
  const timers = fakeTimers();
  const policy = { ...BASE_POLICY, hard_bytes: 10000 };
  let running;
  try {
    running = await start(f, { clock, timers, policy });
    const derived = await publishAndDerive(running, f);
    await operate(running, derived, 'operation-auto-race', html('race', 'r'));
    const preview = await post(running.base, '/api/canvas/pruning/preview', {
      schema_version: '1', command_id: 'command-auto-race-preview'
    });
    assert.equal(preview.response.status, 200);
    clock.advance(policy.grace_ms + 1);
    timers.fireNext();
    const manual = await post(running.base, '/api/canvas/pruning/commit', {
      schema_version: '1',
      command_id: 'command-auto-race-commit',
      expected_candidate_digest: preview.body.candidate.candidate_digest
    });
    assert.equal([201, 409].includes(manual.response.status), true);
    await waitFor(async () => (await state(running)).canvas.operations_v1.pruning.active_request === null);

    const events = await readEvents(path.join(f.stateDir, 'events.jsonl'));
    const tombstones = events.filter((event) => event.event_type === 'canvas.revision_pruned');
    assert.equal(tombstones.length, 1);
    assert.equal(new Set(tombstones.map((event) => event.tombstone.revision_id)).size, 1);
    assert.equal(timers.size, 0);
  } finally {
    await cleanup(f, running);
  }
});

test('automatic append failure preserves the committed operation and retryable request', async () => {
  const f = await fixture('ide-extension-retention-auto-append');
  const injectedAppend = async (...args) => {
    if (args[1]?.event_type === 'canvas.revision_pruned'
      && args[1].tombstone.reason === 'automatic') {
      const error = new Error('synthetic automatic tombstone failure');
      error.code = 'synthetic_auto_append_failure';
      throw error;
    }
    return appendEvent(...args);
  };
  let running;
  try {
    running = await start(f, { appendEvent: injectedAppend });
    const derived = await publishAndDerive(running, f);
    const operated = await operate(running, derived, 'operation-auto-append-fail', html('append', 'a'));
    const result = running.server.canvasRetention.lastAutomaticResult;
    const events = await readEvents(path.join(f.stateDir, 'events.jsonl'));
    const projection = (await state(running)).canvas.operations_v1;
    assert.equal(result.status, 'failed');
    assert.equal(result.error.code, 'synthetic_auto_append_failure');
    assert.ok(projection.operations['operation-auto-append-fail']);
    assert.equal(projection.pruning.active_request !== null, true);
    assert.equal(events.some((event) => event.event_type === 'canvas.revision_pruned'), false);
    assert.equal(operated.operation.operation_id, 'operation-auto-append-fail');
  } finally {
    await cleanup(f, running);
  }
});

test('restart recovers a tombstone committed before blob deletion', async () => {
  const f = await fixture('ide-extension-retention-auto-delete');
  const baseBlobStore = createCanvasBlobStore({ stateDir: f.stateDir });
  let failDelete = true;
  const failingBlobStore = Object.freeze({
    ...baseBlobStore,
    async delete(digest) {
      if (failDelete) {
        failDelete = false;
        const error = new Error('synthetic automatic delete failure');
        error.code = 'EACCES';
        throw error;
      }
      return baseBlobStore.delete(digest);
    }
  });
  const clock = mutableClock();
  let running;
  try {
    running = await start(f, { clock, canvasBlobStore: failingBlobStore });
    const derived = await publishAndDerive(running, f);
    await operate(running, derived, 'operation-auto-delete-fail', html('delete', 'd'));
    let projection = (await state(running)).canvas.operations_v1;
    assert.equal(running.server.canvasRetention.lastAutomaticResult.status, 'failed');
    assert.equal(running.server.canvasRetention.lastAutomaticResult.error.tombstone_committed, true);
    assert.equal(projection.pruning.state, 'reclaiming');
    const unavailable = await request(running.base, derived.content_url);
    assert.equal(unavailable.response.status, 410);
    await close(running.server);

    running = await start(f, { clock, canvasBlobStore: baseBlobStore });
    assert.equal(running.runtime.automaticRetention.status, 'completed');
    projection = (await state(running)).canvas.operations_v1;
    assert.equal(projection.pruning.state, 'normal');
    assert.equal(projection.pruning.active_request, null);
    await assert.rejects(baseBlobStore.read(derived.revision.content_sha256), {
      code: 'canvas_blob_not_found'
    });
  } finally {
    await cleanup(f, running);
  }
});

test('all-current storage reports explicit non-convergence without deleting current', async () => {
  const f = await fixture('ide-extension-retention-auto-current');
  const policy = {
    soft_bytes: 1000,
    hard_bytes: 1500,
    grace_ms: 100,
    reclaim_below_bytes: 1000
  };
  let running;
  try {
    running = await start(f, { policy });
    const derived = await publishAndDerive(running, f);
    const result = running.server.canvasRetention.lastAutomaticResult;
    const projection = (await state(running)).canvas.operations_v1;
    assert.equal(result.status, 'blocked');
    assert.equal(result.blocked_reason, 'no_eligible_revisions');
    assert.equal(Object.keys(projection.prune_tombstones).length, 0);
    assert.equal(projection.surfaces[derived.surface.operations_surface_id].current_revision_id, derived.revision.revision_id);
    const current = await request(running.base, derived.content_url);
    assert.equal(current.response.status, 200);
  } finally {
    await cleanup(f, running);
  }
});

test('malformed history and corrupt committed blobs block startup before deletion', async () => {
  for (const scenario of ['malformed', 'corrupt']) {
    const f = await fixture(`ide-extension-retention-auto-${scenario}`);
    const baseBlobStore = createCanvasBlobStore({ stateDir: f.stateDir });
    let deletes = 0;
    const witnessingStore = Object.freeze({
      ...baseBlobStore,
      async delete(digest) {
        deletes += 1;
        return baseBlobStore.delete(digest);
      }
    });
    const eventsFile = path.join(f.stateDir, 'events.jsonl');
    await mkdir(path.dirname(eventsFile), { recursive: true });
    if (scenario === 'malformed') {
      await writeFile(eventsFile, `${JSON.stringify({
        event_version: 4,
        event_id: 'event-malformed-auto',
        event_type: 'canvas.unknown',
        created_at: '2026-07-15T00:00:00.000Z'
      })}\n`, 'utf8');
    } else {
      const fixtureEvents = await readFile(
        path.join(projectRoot, 'tests/fixtures/events/operations-v1-lifecycle.jsonl'),
        'utf8'
      );
      await writeFile(eventsFile, fixtureEvents, 'utf8');
      const parsed = fixtureEvents.trim().split('\n').map(JSON.parse);
      const digests = parsed
        .filter((event) => event.event_version === 4)
        .map((event) => event.revision?.content_sha256)
        .filter(Boolean);
      await mkdir(baseBlobStore.blob_dir, { recursive: true });
      for (const digest of new Set(digests)) {
        await writeFile(path.join(baseBlobStore.blob_dir, `${digest}.html`), 'corrupt', 'utf8');
      }
    }

    const server = createServer({
      rootDir: projectRoot,
      stateDir: f.stateDir,
      workspaceRoot: f.workspaceRoot,
      retentionPolicy: BASE_POLICY,
      canvasBlobStore: witnessingStore
    });
    await assert.rejects(server.ready);
    assert.equal(deletes, 0);
    assert.equal(server.canvasRetention.timerState().scheduled, false);
    server.canvasRetention.close();
    await cleanup(f, null);
  }
});
