import assert from 'node:assert/strict';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { appendEvent } from '../src/kernel/audit.mjs';
import { NAVIGATION_MAX_COMMANDS, NAVIGATION_RETENTION_MS } from '../src/kernel/canvas-navigation.mjs';
import { OPERATIONS_V1_EVENT_VERSION, OPERATIONS_V1_LIMITS } from '../src/kernel/operations-contracts.mjs';
import { atomicWriteJson } from '../src/kernel/storage.mjs';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const SOURCE_A = '<!doctype html><title>Source A</title><main>A</main>';
const SOURCE_B = '<!doctype html><title>Source B</title><main>B</main>';
const REPLACEMENT_A = '<!doctype html><title>Changed A</title><main>A2</main>';
const REPLACEMENT_B = '<!doctype html><title>Changed B</title><main>B2</main>';

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

async function fixture(prefix = 'ide-extension-operations-navigation-') {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), `${prefix}state-`));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), `${prefix}workspace-`));
  const paths = ['presentations/a.html', 'presentations/b.html'];
  const files = paths.map((relative) => path.join(workspaceRoot, relative));
  await mkdir(path.dirname(files[0]), { recursive: true });
  await writeFile(files[0], SOURCE_A, 'utf8');
  await writeFile(files[1], SOURCE_B, 'utf8');
  return { stateDir, workspaceRoot, paths, files };
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

async function publish(running, relative, title = 'Navigation source') {
  const result = await post(running.base, '/api/canvas/publish', {
    schema_version: '1',
    path: relative,
    title,
    kind: 'presentation'
  });
  assert.ok([200, 201].includes(result.response.status));
  return result.body.current;
}

async function derive(running, current, key) {
  const result = await post(running.base, '/api/canvas/operation-surfaces', {
    schema_version: '1',
    source_v0_surface_id: current.surface_id,
    source_revision_id: current.revision.revision_id,
    operation_surface_idempotency_key: key
  });
  assert.ok([200, 201].includes(result.response.status));
  return result.body;
}

function target(surfaceKind, surfaceId, revisionId) {
  return {
    kind: 'surface_revision',
    surface_kind: surfaceKind,
    surface_id: surfaceId,
    revision_id: revisionId
  };
}

function redirect(commandId, destination) {
  return {
    schema_version: '1',
    command_id: commandId,
    action: 'redirect',
    destination
  };
}

function refresh(commandId) {
  return { schema_version: '1', command_id: commandId, action: 'refresh' };
}

function operationInput(derived, operationId, html) {
  return {
    schema_version: '1',
    operation_id: operationId,
    operations_surface_id: derived.surface.operations_surface_id,
    expected_revision_id: derived.revision.revision_id,
    mode: 'replace',
    target: { kind: 'whole_document' },
    input: { kind: 'inline_html', html }
  };
}

function operate(running, input) {
  return post(
    running.base,
    `/api/canvas/operation-surfaces/${input.operations_surface_id}/operations`,
    input
  );
}

async function openNotifications(base) {
  const controller = new AbortController();
  const response = await fetch(`${base}/api/canvas/notifications`, { signal: controller.signal });
  assert.equal(response.status, 200);
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  const queue = [];
  const waiters = [];
  let buffer = '';

  function deliver(value) {
    const waiter = waiters.shift();
    if (waiter) waiter(value);
    else queue.push(value);
  }

  const pump = (async () => {
    while (true) {
      const { done, value } = await reader.read();
      if (done) return;
      buffer += decoder.decode(value, { stream: true });
      let boundary;
      while ((boundary = buffer.indexOf('\n\n')) !== -1) {
        const block = buffer.slice(0, boundary);
        buffer = buffer.slice(boundary + 2);
        const id = block.match(/^id: (.+)$/m)?.[1];
        const data = block.match(/^data: (.+)$/m)?.[1];
        if (data) deliver({ id: Number(id), data: JSON.parse(data) });
      }
    }
  })().catch((error) => {
    if (!controller.signal.aborted) throw error;
  });

  return {
    get receivedCount() {
      return queue.length;
    },
    next(timeout = 1000) {
      if (queue.length) return Promise.resolve(queue.shift());
      return new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
          const index = waiters.indexOf(deliverValue);
          if (index !== -1) waiters.splice(index, 1);
          reject(new Error('notification timeout'));
        }, timeout);
        function deliverValue(value) {
          clearTimeout(timer);
          resolve(value);
        }
        waiters.push(deliverValue);
      });
    },
    async close() {
      controller.abort();
      await reader.cancel().catch(() => {});
      await pump;
    }
  };
}

test('redirects durably while current stays V0 and transient status expires on restart', async () => {
  const f = await fixture();
  let running;
  let stream;
  try {
    running = await start(f);
    const v0 = await publish(running, f.paths[0]);
    const derived = await derive(running, v0, 'derive-navigation-durable');
    const initialDisplay = (await request(running.base, '/api/canvas/display')).body.display;
    assert.equal(initialDisplay.surface_kind, 'v0');
    assert.equal(initialDisplay.revision_id, v0.revision.revision_id);

    stream = await openNotifications(running.base);
    assert.equal((await stream.next()).data.revision_id, v0.revision.revision_id);
    const input = redirect(
      'command-navigation-durable',
      target(
        'operations_v1',
        derived.surface.operations_surface_id,
        derived.revision.revision_id
      )
    );
    const before = (await request(running.base, '/api/state')).body.event_count;
    const selected = await post(running.base, '/api/canvas/navigation', input);
    assert.equal(selected.response.status, 201);
    assert.equal(selected.body.idempotent, false);
    assert.equal(selected.body.display.surface_kind, 'operations_v1');
    assert.equal((await stream.next()).data.type, 'canvas.display.changed');
    assert.equal((await request(running.base, '/api/state')).body.event_count, before + 1);
    assert.equal(
      (await request(running.base, '/api/canvas/current')).body.current.revision.revision_id,
      v0.revision.revision_id
    );

    const acknowledged = await post(
      running.base,
      '/api/canvas/navigation/command-navigation-durable/ack',
      { schema_version: '1', status: 'loaded' }
    );
    assert.equal(acknowledged.body.command.status, 'loaded');
    await stream.close();
    stream = null;
    await close(running.server);
    running = await start(f);

    assert.equal(
      (await request(running.base, '/api/canvas/display')).body.display.surface_kind,
      'operations_v1'
    );
    assert.equal(
      (await request(running.base, '/api/canvas/navigation/command-navigation-durable')).response.status,
      404
    );
    const retryBefore = (await request(running.base, '/api/state')).body.event_count;
    const retry = await post(running.base, '/api/canvas/navigation', input);
    assert.equal(retry.response.status, 200);
    assert.equal(retry.body.idempotent, true);
    assert.equal((await request(running.base, '/api/state')).body.event_count, retryBefore);

    const conflict = await post(running.base, '/api/canvas/navigation', redirect(
      'command-navigation-durable',
      target('v0', v0.surface_id, v0.revision.revision_id)
    ));
    assert.equal(conflict.response.status, 409);
    assert.equal(conflict.body.error, 'navigation_command_conflict');
  } finally {
    await stream?.close();
    await cleanup(f, running);
  }
});

test('advances only the selected Operations display and later V0 publication selects V0', async () => {
  const f = await fixture('ide-extension-operations-navigation-selection-');
  let running;
  let stream;
  try {
    running = await start(f);
    const v0A = await publish(running, f.paths[0], 'A');
    const derivedA = await derive(running, v0A, 'derive-navigation-a');
    const v0B = await publish(running, f.paths[1], 'B');
    const derivedB = await derive(running, v0B, 'derive-navigation-b');
    await post(running.base, '/api/canvas/navigation', redirect(
      'command-select-a',
      target('operations_v1', derivedA.surface.operations_surface_id, derivedA.revision.revision_id)
    ));

    stream = await openNotifications(running.base);
    assert.equal((await stream.next()).data.revision_id, derivedA.revision.revision_id);
    const changedB = await operate(running, operationInput(derivedB, 'operation-navigation-b', REPLACEMENT_B));
    assert.equal(changedB.response.status, 201);
    await new Promise((resolve) => setTimeout(resolve, 100));
    assert.equal(stream.receivedCount, 0);
    assert.equal(
      (await request(running.base, '/api/canvas/display')).body.display.revision_id,
      derivedA.revision.revision_id
    );

    const changedA = await operate(running, operationInput(derivedA, 'operation-navigation-a', REPLACEMENT_A));
    assert.equal(changedA.response.status, 201);
    const revisionNotice = await stream.next();
    assert.equal(revisionNotice.data.type, 'canvas.revision.available');
    assert.equal(revisionNotice.data.revision_id, changedA.body.revision.revision_id);
    assert.equal(
      (await request(running.base, '/api/canvas/display')).body.display.revision_id,
      changedA.body.revision.revision_id
    );

    await writeFile(f.files[1], '<!doctype html><title>B3</title><main>B3</main>', 'utf8');
    const publishedB = await publish(running, f.paths[1], 'B3');
    assert.equal((await stream.next()).data.revision_id, publishedB.revision.revision_id);
    const display = (await request(running.base, '/api/canvas/display')).body.display;
    assert.equal(display.surface_kind, 'v0');
    assert.equal(display.surface_id, publishedB.surface_id);
    assert.equal(
      (await request(running.base, '/api/canvas/current')).body.current.surface_id,
      publishedB.surface_id
    );
  } finally {
    await stream?.close();
    await cleanup(f, running);
  }
});

test('rejects unknown, drifted, and pruned redirect targets without navigation events', async () => {
  const f = await fixture('ide-extension-operations-navigation-admission-');
  let running;
  try {
    running = await start(f);
    const v0 = await publish(running, f.paths[0]);
    const derived = await derive(running, v0, 'derive-navigation-admission');
    const changed = await operate(running, operationInput(
      derived,
      'operation-navigation-prune-source',
      REPLACEMENT_A
    ));
    assert.equal(changed.response.status, 201);
    const baseline = (await request(running.base, '/api/state')).body.event_count;

    const unknown = await post(running.base, '/api/canvas/navigation', redirect(
      'command-navigation-unknown',
      target('operations_v1', 'operations-surface-unknown', 'revision-unknown')
    ));
    assert.equal(unknown.response.status, 404);
    assert.equal(unknown.body.error, 'navigation_target_not_found');

    await writeFile(f.files[0], '<h1>workspace drift</h1>', 'utf8');
    const drift = await post(running.base, '/api/canvas/navigation', redirect(
      'command-navigation-drift',
      target('v0', v0.surface_id, v0.revision.revision_id)
    ));
    assert.equal(drift.response.status, 409);
    assert.equal(drift.body.error, 'navigation_target_unavailable');
    assert.equal(drift.body.reason, 'workspace_drift');
    assert.equal((await request(running.base, '/api/state')).body.event_count, baseline);

    await close(running.server);
    running = null;
    const requestedAt = '2026-07-14T22:50:00.000Z';
    await appendEvent(path.join(f.stateDir, 'events.jsonl'), {
      event_version: OPERATIONS_V1_EVENT_VERSION,
      event_id: 'event-navigation-pruning-requested',
      event_type: 'canvas.pruning_requested',
      pruning_request: {
        pruning_request_id: 'pruning-request-navigation',
        observed_bytes: OPERATIONS_V1_LIMITS.retention_soft_bytes,
        soft_limit_bytes: OPERATIONS_V1_LIMITS.retention_soft_bytes,
        hard_limit_bytes: OPERATIONS_V1_LIMITS.retention_hard_bytes,
        grace_deadline: '2026-07-21T22:50:00.000Z',
        requested_at: requestedAt
      },
      created_at: requestedAt
    });
    await appendEvent(path.join(f.stateDir, 'events.jsonl'), {
      event_version: OPERATIONS_V1_EVENT_VERSION,
      event_id: 'event-navigation-revision-pruned',
      event_type: 'canvas.revision_pruned',
      tombstone: {
        pruning_request_id: 'pruning-request-navigation',
        revision_id: derived.revision.revision_id,
        operations_surface_id: derived.surface.operations_surface_id,
        content_sha256: derived.revision.content_sha256,
        blob_ref: derived.revision.blob_ref,
        reason: 'manual',
        retention_state_after: 'normal',
        pruned_at: '2026-07-14T22:51:00.000Z'
      },
      created_at: '2026-07-14T22:51:00.000Z'
    });
    running = await start(f);
    const beforePruned = (await request(running.base, '/api/state')).body.event_count;
    const pruned = await post(running.base, '/api/canvas/navigation', redirect(
      'command-navigation-pruned',
      target('operations_v1', derived.surface.operations_surface_id, derived.revision.revision_id)
    ));
    assert.equal(pruned.response.status, 410);
    assert.equal(pruned.body.error, 'navigation_target_pruned');
    assert.equal((await request(running.base, '/api/state')).body.event_count, beforePruned);
  } finally {
    await cleanup(f, running);
  }
});

test('keeps refresh and acknowledgement bounded, transient, and event-free', async () => {
  const f = await fixture('ide-extension-operations-navigation-refresh-');
  let clock = Date.parse('2026-07-14T22:55:00.000Z');
  let running;
  let stream;
  try {
    assert.equal(NAVIGATION_RETENTION_MS, 15 * 60 * 1000);
    assert.equal(NAVIGATION_MAX_COMMANDS, 128);
    running = await start(f, {
      navigationNow: () => clock,
      navigationMaxCommands: 2
    });
    const empty = await post(running.base, '/api/canvas/navigation', refresh('command-refresh-empty'));
    assert.equal(empty.response.status, 409);
    assert.equal(empty.body.error, 'display_target_not_found');

    await publish(running, f.paths[0]);
    stream = await openNotifications(running.base);
    await stream.next();
    const baseline = (await request(running.base, '/api/state')).body.event_count;
    const firstInput = refresh('command-refresh-first');
    const first = await post(running.base, '/api/canvas/navigation', firstInput);
    assert.equal(first.response.status, 201);
    assert.equal((await stream.next()).data.type, 'canvas.refresh.requested');
    assert.equal((await request(running.base, '/api/state')).body.event_count, baseline);

    const retry = await post(running.base, '/api/canvas/navigation', firstInput);
    assert.equal(retry.response.status, 200);
    assert.equal(retry.body.idempotent, true);
    await new Promise((resolve) => setTimeout(resolve, 100));
    assert.equal(stream.receivedCount, 0);

    const acknowledged = await post(
      running.base,
      '/api/canvas/navigation/command-refresh-first/ack',
      { schema_version: '1', status: 'failed' }
    );
    assert.equal(acknowledged.body.command.status, 'failed');
    assert.equal(acknowledged.body.command.acknowledgement.status, 'failed');
    assert.equal('notification' in acknowledged.body, false);
    assert.equal((await request(
      running.base,
      '/api/canvas/navigation/command-refresh-first'
    )).body.command.status, 'failed');

    clock += 1000;
    await post(running.base, '/api/canvas/navigation', refresh('command-refresh-second'));
    await stream.next();
    clock += 1000;
    await post(running.base, '/api/canvas/navigation', refresh('command-refresh-third'));
    await stream.next();
    assert.equal((await request(
      running.base,
      '/api/canvas/navigation/command-refresh-first'
    )).response.status, 404);
    assert.equal(running.server.canvasNavigation.retainedCount, 2);

    clock += NAVIGATION_RETENTION_MS + 1;
    assert.equal((await request(
      running.base,
      '/api/canvas/navigation/command-refresh-third'
    )).response.status, 404);
    assert.equal(running.server.canvasNavigation.retainedCount, 0);
    assert.equal((await request(running.base, '/api/state')).body.event_count, baseline);
  } finally {
    await stream?.close();
    await cleanup(f, running);
  }
});

test('binds Operations interactions to the displayed V4 revision without weakening V0', async () => {
  const f = await fixture('ide-extension-operations-navigation-interaction-');
  let running;
  try {
    running = await start(f);
    const v0 = await publish(running, f.paths[0]);
    const derived = await derive(running, v0, 'derive-navigation-interaction');
    await post(running.base, '/api/canvas/navigation', redirect(
      'command-navigation-interaction',
      target('operations_v1', derived.surface.operations_surface_id, derived.revision.revision_id)
    ));
    const body = {
      schema_version: '1',
      operations_surface_id: derived.surface.operations_surface_id,
      revision_id: derived.revision.revision_id,
      event_name: 'decision.selected',
      payload: { value: 'approve' }
    };
    const route = `/api/canvas/operation-surfaces/${derived.surface.operations_surface_id}/events`;
    const recorded = await post(running.base, route, body);
    assert.equal(recorded.response.status, 201);
    assert.equal(recorded.body.interaction.operations_surface_id, derived.surface.operations_surface_id);
    const state = (await request(running.base, '/api/state')).body;
    assert.equal(state.canvas.interactions.length, 0);
    assert.equal(state.canvas.operations_v1.interactions.length, 1);

    const legacy = await post(running.base, '/api/canvas/events', body);
    assert.equal(legacy.response.status, 400);
    assert.equal(legacy.body.error, 'invalid_request');
    const mismatch = await post(
      running.base,
      '/api/canvas/operation-surfaces/operations-surface-other/events',
      body
    );
    assert.equal(mismatch.response.status, 409);
    assert.equal(mismatch.body.error, 'operations_surface_binding_mismatch');

    await writeFile(f.files[1], '<!doctype html><title>B selected</title>', 'utf8');
    await publish(running, f.paths[1], 'B selected');
    const stale = await post(running.base, route, {
      ...body,
      event_name: 'decision.changed'
    });
    assert.equal(stale.response.status, 409);
    assert.equal(stale.body.error, 'stale_canvas_revision');
  } finally {
    await cleanup(f, running);
  }
});

test('does not retain failed redirects and repairs durable selection after projection failure', async () => {
  const appendFixture = await fixture('ide-extension-operations-navigation-append-failure-');
  let appendCount = 0;
  const injectedAppend = async (...args) => {
    appendCount += 1;
    if (appendCount === 3) {
      const error = new Error('synthetic navigation append failure');
      error.code = 'synthetic_append_failure';
      throw error;
    }
    return appendEvent(...args);
  };
  let appendRunning;
  try {
    appendRunning = await start(appendFixture, { appendEvent: injectedAppend });
    const v0 = await publish(appendRunning, appendFixture.paths[0]);
    const derived = await derive(appendRunning, v0, 'derive-navigation-append-failure');
    const failed = await post(appendRunning.base, '/api/canvas/navigation', redirect(
      'command-navigation-append-failure',
      target('operations_v1', derived.surface.operations_surface_id, derived.revision.revision_id)
    ));
    assert.equal(failed.response.status, 500);
    assert.equal((await request(appendRunning.base, '/api/state')).body.event_count, 2);
    assert.equal((await request(
      appendRunning.base,
      '/api/canvas/navigation/command-navigation-append-failure'
    )).response.status, 404);
    assert.equal(
      (await request(appendRunning.base, '/api/canvas/display')).body.display.surface_kind,
      'v0'
    );
  } finally {
    await cleanup(appendFixture, appendRunning);
  }

  const recoveryFixture = await fixture('ide-extension-operations-navigation-recovery-');
  let writeCount = 0;
  const writeProjection = async (...args) => {
    writeCount += 1;
    if (writeCount === 4) {
      const error = new Error('synthetic navigation projection failure');
      error.code = 'EIO';
      throw error;
    }
    return atomicWriteJson(...args);
  };
  let recoveryRunning;
  try {
    recoveryRunning = await start(recoveryFixture, { writeProjection });
    const v0 = await publish(recoveryRunning, recoveryFixture.paths[0]);
    const derived = await derive(recoveryRunning, v0, 'derive-navigation-recovery');
    const input = redirect(
      'command-navigation-recovery',
      target('operations_v1', derived.surface.operations_surface_id, derived.revision.revision_id)
    );
    const interrupted = await post(recoveryRunning.base, '/api/canvas/navigation', input);
    assert.equal(interrupted.response.status, 503);
    assert.equal(interrupted.body.error, 'reconciliation_required');
    assert.equal(
      (await request(recoveryRunning.base, '/api/canvas/display')).body.display.surface_kind,
      'operations_v1'
    );
    const retry = await post(recoveryRunning.base, '/api/canvas/navigation', input);
    assert.equal(retry.response.status, 200);
    assert.equal(retry.body.idempotent, true);
    assert.equal((await request(recoveryRunning.base, '/api/state')).body.event_count, 3);
  } finally {
    await cleanup(recoveryFixture, recoveryRunning);
  }
});
