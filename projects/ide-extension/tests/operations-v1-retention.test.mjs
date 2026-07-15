import assert from 'node:assert/strict';
import { access, mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { appendEvent, readEvents } from '../src/kernel/audit.mjs';
import { createCanvasBlobStore } from '../src/kernel/canvas-blobs.mjs';
import {
  buildRetentionCandidate,
  createRetentionPolicy,
  DEFAULT_RETENTION_POLICY
} from '../src/kernel/canvas-retention.mjs';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const POLICY = Object.freeze({
  soft_bytes: 2500,
  hard_bytes: 10000,
  grace_ms: 7 * 24 * 60 * 60 * 1000,
  reclaim_below_bytes: 2500
});

function html(label, fill = 'x') {
  return `<!doctype html><html><head><title>${label}</title></head><body>`
    + `<main data-label="${label}">${label}-${fill.repeat(1800)}</main></body></html>`;
}

function listen(server, port = 0) {
  return new Promise((resolve) => {
    server.listen(port, '127.0.0.1', () => resolve(server.address().port));
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

async function fixture(prefix = 'ide-extension-operations-retention-') {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), `${prefix}state-`));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), `${prefix}workspace-`));
  const relative = 'presentations/source.html';
  const file = path.join(workspaceRoot, relative);
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, html('source', 's'), 'utf8');
  return { stateDir, workspaceRoot, relative, file };
}

function retentionClock(start = Date.parse('2026-07-14T23:30:00.000Z')) {
  let value = start;
  return () => {
    const result = new Date(value).toISOString();
    value += 1000;
    return result;
  };
}

function retentionIds(prefix = 'retention') {
  let value = 0;
  return () => `${prefix}-${++value}`;
}

async function start(f, options = {}, port = 0) {
  const server = createServer({
    rootDir: projectRoot,
    stateDir: f.stateDir,
    workspaceRoot: f.workspaceRoot,
    retentionPolicy: POLICY,
    retentionNow: retentionClock(),
    retentionRandomId: retentionIds(),
    ...options
  });
  await server.ready;
  const actualPort = await listen(server, port);
  return { server, base: `http://127.0.0.1:${actualPort}`, port: actualPort };
}

async function cleanup(f, running) {
  if (running?.server.listening) await close(running.server);
  await rm(f.stateDir, { recursive: true, force: true });
  await rm(f.workspaceRoot, { recursive: true, force: true });
}

async function publishAndDerive(running, f, key = 'derive-retention-source') {
  const published = await post(running.base, '/api/canvas/publish', {
    schema_version: '1',
    path: f.relative,
    title: 'Retention source',
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

function operationInput(current, operationId, replacement) {
  return {
    schema_version: '1',
    operation_id: operationId,
    operations_surface_id: current.surface.operations_surface_id,
    expected_revision_id: current.revision.revision_id,
    mode: 'replace',
    target: { kind: 'whole_document' },
    input: { kind: 'inline_html', html: replacement }
  };
}

async function operate(running, current, operationId, replacement) {
  const input = operationInput(current, operationId, replacement);
  const result = await post(
    running.base,
    `/api/canvas/operation-surfaces/${current.surface.operations_surface_id}/operations`,
    input
  );
  assert.equal(result.response.status, 201);
  return { ...result.body, input };
}

async function storage(running) {
  return request(running.base, '/api/canvas/storage');
}

async function preview(running, commandId = 'command-retention-preview') {
  return post(running.base, '/api/canvas/pruning/preview', {
    schema_version: '1',
    command_id: commandId
  });
}

async function commit(running, candidateDigest, commandId = 'command-retention-commit') {
  return post(running.base, '/api/canvas/pruning/commit', {
    schema_version: '1',
    command_id: commandId,
    expected_candidate_digest: candidateDigest
  });
}

test('keeps production policy fixed and derives shared-reference candidates deterministically', () => {
  assert.deepEqual(createRetentionPolicy(), DEFAULT_RETENTION_POLICY);
  assert.throws(
    () => createRetentionPolicy({ soft_bytes: 10, hard_bytes: 10 }),
    (error) => error.code === 'retention_policy_invalid'
  );
  const first = {
    revision_id: 'revision-a', operations_surface_id: 'operations-surface-a',
    content_sha256: 'a'.repeat(64), blob_ref: `canvas/blobs/${'a'.repeat(64)}.html`,
    byte_length: 100, committed_at: '2026-01-01T00:00:00.000Z'
  };
  const shared = { ...first, revision_id: 'revision-b', committed_at: '2026-01-02T00:00:00.000Z' };
  const current = {
    ...first, revision_id: 'revision-c', content_sha256: 'b'.repeat(64),
    blob_ref: `canvas/blobs/${'b'.repeat(64)}.html`, committed_at: '2026-01-03T00:00:00.000Z'
  };
  const reconciliation = {
    event_count: 4,
    projection: { canvas: { operations_v1: {
      surfaces: { 'operations-surface-a': {
        operations_surface_id: 'operations-surface-a', current_revision_id: 'revision-c'
      } },
      revisions: { 'revision-a': first, 'revision-b': shared, 'revision-c': current },
      prune_tombstones: {}, display_target: null,
      pruning: { state: 'grace', active_request: { pruning_request_id: 'pruning-request-a' } }
    } } },
    canvas_blobs: {
      total_bytes: 200,
      blobs: [
        { sha256: 'a'.repeat(64), byte_length: 100, referenced: true },
        { sha256: 'b'.repeat(64), byte_length: 100, referenced: true }
      ]
    }
  };
  const policy = { soft_bytes: 150, hard_bytes: 300, grace_ms: 1000, reclaim_below_bytes: 150 };
  const one = buildRetentionCandidate(reconciliation, policy);
  const two = buildRetentionCandidate(structuredClone(reconciliation), policy);
  assert.deepEqual(one.selected_revision_ids, ['revision-a', 'revision-b']);
  assert.equal(one.reclaimable_bytes, 100);
  assert.equal(one.projected_referenced_bytes, 100);
  assert.equal(one.candidate_digest, two.candidate_digest);
  reconciliation.projection.canvas.operations_v1.display_target = {
    kind: 'surface_revision',
    surface_kind: 'operations_v1',
    surface_id: 'operations-surface-a',
    revision_id: 'revision-a'
  };
  const displayProtected = buildRetentionCandidate(reconciliation, policy);
  assert.deepEqual(displayProtected.selected_revision_ids, ['revision-b']);
  assert.equal(displayProtected.reclaimable_bytes, 0);
  assert.equal(displayProtected.blocked_reason, 'protected_bytes_above_target');
});

test('opens one durable grace request at soft threshold and preserves it over restart', async () => {
  const f = await fixture('ide-extension-retention-grace-');
  let running;
  try {
    running = await start(f);
    let current = await publishAndDerive(running, f);
    const below = await storage(running);
    assert.equal(below.response.status, 200);
    assert.equal(below.body.storage.state, 'normal');
    assert.equal(below.body.storage.total_bytes < POLICY.soft_bytes, true);
    const eventCount = below.body.storage.event_cursor;

    current = await operate(running, current, 'operation-retention-large', html('large', 'l'));
    const opened = await storage(running);
    assert.equal(opened.response.status, 200);
    assert.equal(opened.body.storage.state, 'grace');
    assert.equal(opened.body.storage.event_cursor, eventCount + 2);
    assert.equal(opened.body.storage.active_request.observed_bytes >= POLICY.soft_bytes, true);
    assert.equal(
      Date.parse(opened.body.storage.active_request.grace_deadline)
        - Date.parse(opened.body.storage.active_request.requested_at),
      POLICY.grace_ms
    );
    const requestId = opened.body.storage.active_request.pruning_request_id;
    const repeated = await storage(running);
    assert.equal(repeated.body.storage.event_cursor, opened.body.storage.event_cursor);
    assert.equal(repeated.body.storage.active_request.pruning_request_id, requestId);

    const port = running.port;
    await close(running.server);
    running = await start(f, {}, port);
    const restored = await storage(running);
    assert.equal(restored.body.storage.event_cursor, opened.body.storage.event_cursor);
    assert.equal(restored.body.storage.active_request.pruning_request_id, requestId);
    assert.equal(restored.body.storage.referenced_bytes > 0, true);
    assert.equal(restored.body.storage.orphan_bytes, 0);
    assert.equal(restored.body.storage.candidate_revision_count, 1);
    assert.equal(restored.body.storage.largest_blob.byte_length > 0, true);
  } finally {
    await cleanup(f, running);
  }
});

test('manually tombstones before delete, returns 410, and marks exact retry unavailable', async () => {
  const f = await fixture('ide-extension-retention-manual-');
  const baseBlobStore = createCanvasBlobStore({ stateDir: f.stateDir });
  const deletionWitnesses = [];
  const canvasBlobStore = Object.freeze({
    ...baseBlobStore,
    async delete(digest) {
      const events = await readEvents(path.join(f.stateDir, 'events.jsonl'));
      const tombstone = events.find((event) => (
        event.event_type === 'canvas.revision_pruned'
        && event.tombstone.content_sha256 === digest
      ));
      assert.ok(tombstone, `blob ${digest} must have a durable tombstone before deletion`);
      deletionWitnesses.push(tombstone.tombstone.revision_id);
      return baseBlobStore.delete(digest);
    }
  });
  let running;
  try {
    running = await start(f, { canvasBlobStore });
    const derived = await publishAndDerive(running, f);
    const first = await operate(running, derived, 'operation-retention-first', html('first', 'f'));
    await operate(running, first, 'operation-retention-second', html('second', 'z'));
    const opened = await storage(running);
    assert.equal(opened.body.storage.state, 'grace');

    const planned = await preview(running);
    assert.equal(planned.response.status, 200);
    assert.deepEqual(
      planned.body.candidate.selected_revision_ids,
      [derived.revision.revision_id, first.revision.revision_id]
    );
    const retriedPreview = await preview(running);
    assert.equal(retriedPreview.body.idempotent, true);
    assert.equal(
      retriedPreview.body.candidate.candidate_digest,
      planned.body.candidate.candidate_digest
    );

    const pruned = await commit(running, planned.body.candidate.candidate_digest);
    assert.equal(pruned.response.status, 201);
    assert.equal(pruned.body.pruned_revisions.length, 2);
    assert.equal(pruned.body.pruned_revisions.every((item) => item.body_deleted), true);
    assert.deepEqual(deletionWitnesses, planned.body.candidate.selected_revision_ids);
    assert.equal(pruned.body.storage.state, 'normal');
    assert.equal(pruned.body.storage.total_bytes < POLICY.soft_bytes, true);

    const oldContent = await request(running.base, first.content_url);
    assert.equal(oldContent.response.status, 410);
    assert.equal(oldContent.body.error, 'revision_pruned');
    assert.equal(oldContent.body.tombstone.revision_id, first.revision.revision_id);

    const exactRetry = await post(
      running.base,
      `/api/canvas/operation-surfaces/${first.input.operations_surface_id}/operations`,
      first.input
    );
    assert.equal(exactRetry.response.status, 200);
    assert.equal(exactRetry.body.idempotent, true);
    assert.equal(exactRetry.body.result_body_status, 'operation_result_pruned');
    assert.equal(exactRetry.body.result_body_available, false);
    assert.equal(exactRetry.body.tombstone.revision_id, first.revision.revision_id);

    const retryCommit = await commit(running, planned.body.candidate.candidate_digest);
    assert.equal(retryCommit.response.status, 200);
    assert.equal(retryCommit.body.idempotent, true);
    const conflict = await commit(running, 'f'.repeat(64));
    assert.equal(conflict.response.status, 409);
    assert.equal(conflict.body.error, 'pruning_command_conflict');
  } finally {
    await cleanup(f, running);
  }
});

test('accounts for shared blobs and rejects a preview made stale by a later operation', async () => {
  const f = await fixture('ide-extension-retention-shared-');
  let running;
  try {
    running = await start(f);
    const derived = await publishAndDerive(running, f);
    const source = await request(running.base, derived.content_url);
    const shared = await operate(
      running,
      derived,
      'operation-retention-shared',
      source.body.toString('utf8')
    );
    const current = await operate(running, shared, 'operation-retention-unique', html('unique', 'u'));
    await storage(running);
    const planned = await preview(running, 'command-retention-shared-preview');
    assert.deepEqual(
      planned.body.candidate.selected_revision_ids,
      [derived.revision.revision_id, shared.revision.revision_id]
    );

    const changed = await operate(running, current, 'operation-retention-after-preview', html('later', 'q'));
    assert.equal(changed.revision.revision_id !== current.revision.revision_id, true);
    const stale = await commit(
      running,
      planned.body.candidate.candidate_digest,
      'command-retention-stale-commit'
    );
    assert.equal(stale.response.status, 409);
    assert.equal(stale.body.error, 'pruning_candidate_changed');
    assert.notEqual(stale.body.actual_candidate_digest, planned.body.candidate.candidate_digest);
  } finally {
    await cleanup(f, running);
  }
});

test('stops a manual batch after append failure and leaves un-tombstoned bodies intact', async () => {
  const f = await fixture('ide-extension-retention-append-failure-');
  let pruneAppends = 0;
  const injectedAppend = async (...args) => {
    if (args[1]?.event_type === 'canvas.revision_pruned') {
      pruneAppends += 1;
      if (pruneAppends === 2) {
        const error = new Error('synthetic second tombstone failure');
        error.code = 'synthetic_tombstone_failure';
        throw error;
      }
    }
    return appendEvent(...args);
  };
  let running;
  try {
    running = await start(f, { appendEvent: injectedAppend });
    const derived = await publishAndDerive(running, f);
    const first = await operate(running, derived, 'operation-retention-partial-a', html('partial-a', 'a'));
    await operate(running, first, 'operation-retention-partial-b', html('partial-b', 'b'));
    await storage(running);
    const planned = await preview(running, 'command-retention-partial-preview');
    const result = await commit(
      running,
      planned.body.candidate.candidate_digest,
      'command-retention-partial-commit'
    );
    assert.equal(result.response.status, 500);
    assert.equal(result.body.error, 'synthetic second tombstone failure');

    const state = (await request(running.base, '/api/state')).body;
    const tombstones = state.canvas.operations_v1.prune_tombstones;
    assert.equal(Object.keys(tombstones).length, 1);
    const untouchedId = planned.body.candidate.selected_revision_ids[1];
    assert.equal(tombstones[untouchedId], undefined);
    const untouched = state.canvas.operations_v1.revisions[untouchedId];
    await access(path.join(f.stateDir, untouched.blob_ref));
  } finally {
    await cleanup(f, running);
  }
});

test('keeps a committed tombstone and explicit orphan residue when body deletion fails', async () => {
  const f = await fixture('ide-extension-retention-delete-failure-');
  const blobStore = createCanvasBlobStore({
    stateDir: f.stateDir,
    fileSystem: {
      rm: async (file, options) => {
        if (file.endsWith('.html')) {
          const error = new Error('synthetic blob delete failure');
          error.code = 'EACCES';
          throw error;
        }
        return rm(file, options);
      }
    }
  });
  let running;
  try {
    running = await start(f, { canvasBlobStore: blobStore });
    const derived = await publishAndDerive(running, f);
    const current = await operate(running, derived, 'operation-retention-delete-fail', html('delete-fail', 'd'));
    await storage(running);
    const planned = await preview(running, 'command-retention-delete-preview');
    const selected = planned.body.candidate.selected_revisions[0];
    const result = await commit(
      running,
      planned.body.candidate.candidate_digest,
      'command-retention-delete-commit'
    );
    assert.equal(result.response.status, 503);
    assert.equal(result.body.error, 'retention_blob_delete_failed');
    assert.equal(result.body.tombstone_committed, true);
    assert.deepEqual(result.body.pruned_revisions, [selected.revision_id]);

    const oldContent = await request(
      running.base,
      `/api/canvas/operation-surfaces/${selected.operations_surface_id}`
        + `/revisions/${selected.revision_id}/content`
    );
    assert.equal(oldContent.response.status, 410);
    await access(path.join(f.stateDir, selected.blob_ref));
    const state = (await request(running.base, '/api/state')).body;
    assert.equal(
      state.canvas.operations_v1.prune_tombstones[selected.revision_id].revision_id,
      selected.revision_id
    );
    assert.equal(current.revision.revision_id !== selected.revision_id, true);
  } finally {
    await cleanup(f, running);
  }
});
