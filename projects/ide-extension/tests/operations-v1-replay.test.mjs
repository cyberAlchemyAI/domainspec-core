import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { readEvents } from '../src/kernel/audit.mjs';
import { createCanvasBlobStore } from '../src/kernel/canvas-blobs.mjs';
import {
  OPERATIONS_EVENT_VERSION,
  projectionChecksum,
  reduceEvents
} from '../src/kernel/projector.mjs';
import { atomicWriteJson, createProjectionStore } from '../src/kernel/storage.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const eventDir = path.join(projectRoot, 'tests/fixtures/events');
const INITIAL_HTML = '<!doctype html><p>Initial</p>';
const REPLACEMENT_HTML = '<!DOCTYPE html><html><head></head><body><p>Replacement</p></body></html>';

async function jsonl(name) {
  const source = await readFile(path.join(eventDir, name), 'utf8');
  return source.trim().split('\n').map(JSON.parse);
}

async function writeEvents(file, events) {
  await writeFile(file, `${events.map(JSON.stringify).join('\n')}\n`, 'utf8');
}

async function createState(prefix) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), prefix));
  return {
    stateDir,
    eventsFile: path.join(stateDir, 'events.jsonl'),
    workbenchFile: path.join(stateDir, 'workbench.json'),
    artifactDir: path.join(stateDir, 'artifacts'),
    blobStore: createCanvasBlobStore({ stateDir })
  };
}

async function putLifecycleBlobs(blobStore, includeReplacement = true) {
  const initial = await blobStore.put(Buffer.from(INITIAL_HTML));
  const replacement = includeReplacement
    ? await blobStore.put(Buffer.from(REPLACEMENT_HTML))
    : null;
  return { initial, replacement };
}

function lifecycleExtensions() {
  return [
    {
      event_version: OPERATIONS_EVENT_VERSION,
      event_id: 'event-operations-display-selected',
      event_type: 'canvas.display_target_selected',
      command: {
        command_id: 'command-display-operations-2',
        action: 'redirect',
        normalized_request_digest: '1111111111111111111111111111111111111111111111111111111111111111',
        target: {
          kind: 'surface_revision',
          surface_kind: 'operations_v1',
          surface_id: 'operations-surface-demo',
          revision_id: 'revision-operations-2'
        },
        selected_at: '2026-07-14T20:03:00.000Z'
      },
      created_at: '2026-07-14T20:03:00.000Z'
    },
    {
      event_version: OPERATIONS_EVENT_VERSION,
      event_id: 'event-operations-interaction-1',
      event_type: 'canvas.interaction_recorded',
      interaction: {
        event_id: 'event-operations-interaction-1',
        cursor: 1,
        operations_surface_id: 'operations-surface-demo',
        revision_id: 'revision-operations-2',
        event_name: 'decision.selected',
        payload: { decision_id: 'DG-OV1', value: 'approve' },
        received_at: '2026-07-14T20:04:00.000Z'
      },
      created_at: '2026-07-14T20:04:00.000Z'
    },
    {
      event_version: OPERATIONS_EVENT_VERSION,
      event_id: 'event-operations-pruning-requested',
      event_type: 'canvas.pruning_requested',
      pruning_request: {
        pruning_request_id: 'pruning-request-1',
        observed_bytes: 1073741824,
        soft_limit_bytes: 1073741824,
        hard_limit_bytes: 2147483648,
        grace_deadline: '2026-07-21T20:05:00.000Z',
        requested_at: '2026-07-14T20:05:00.000Z'
      },
      created_at: '2026-07-14T20:05:00.000Z'
    },
    {
      event_version: OPERATIONS_EVENT_VERSION,
      event_id: 'event-operations-revision-pruned',
      event_type: 'canvas.revision_pruned',
      tombstone: {
        pruning_request_id: 'pruning-request-1',
        revision_id: 'revision-operations-1',
        operations_surface_id: 'operations-surface-demo',
        content_sha256: '1a90555dca5c3adc610b5c3f2b979378d3eda283ee0745ef4eaa51ddc345f833',
        blob_ref: 'canvas/blobs/1a90555dca5c3adc610b5c3f2b979378d3eda283ee0745ef4eaa51ddc345f833.html',
        reason: 'manual',
        retention_state_after: 'normal',
        pruned_at: '2026-07-14T20:06:00.000Z'
      },
      created_at: '2026-07-14T20:06:00.000Z'
    }
  ];
}

function pruningCompletion(overrides = {}) {
  const { completion: completionOverrides = {}, ...eventOverrides } = overrides;
  return {
    event_version: OPERATIONS_EVENT_VERSION,
    event_id: 'event-operations-pruning-completed',
    event_type: 'canvas.pruning_completed',
    completion: {
      pruning_request_id: 'pruning-request-1',
      trigger: 'recovery',
      reclaimed_orphan_bytes: 128,
      reclaimed_temporary_bytes: 32,
      final_total_bytes: 1024,
      completed_at: '2026-07-14T20:06:00.000Z',
      ...completionOverrides
    },
    created_at: '2026-07-14T20:06:00.000Z',
    ...eventOverrides
  };
}

test('keeps exact V1 and V3 projections unchanged without V4 events', async () => {
  const legacy = await jsonl('v1-lifecycle.jsonl');
  const expected = JSON.parse(
    await readFile(path.join(eventDir, 'v1-lifecycle.projection.json'), 'utf8')
  );
  assert.deepEqual(reduceEvents(legacy), expected);

  const canvasEvents = await jsonl('canvas-lifecycle.jsonl');
  const canvasProjection = reduceEvents(canvasEvents);
  assert.equal(Object.hasOwn(canvasProjection.canvas, 'operations_v1'), false);
  assert.equal(canvasProjection.canvas.interaction_cursor, 2);
  assert.equal(canvasProjection.canvas.current_surface_id, 'surface-craft-class');
});

test('purely reduces mixed V3/V4 derivation and replacement history', async () => {
  const events = await jsonl('operations-v1-lifecycle.jsonl');
  const projection = reduceEvents(events);
  const operations = projection.canvas.operations_v1;

  assert.equal(OPERATIONS_EVENT_VERSION, 4);
  assert.equal(projection.canvas.current_surface_id, 'surface-operations-source');
  assert.equal(projection.canvas.surfaces['surface-operations-source'].current_revision_id, 'revision-v0-source-1');
  assert.equal(operations.derivation_keys['derive-operations-source-1'].result_operations_surface_id, 'operations-surface-demo');
  assert.deepEqual(
    operations.surfaces['operations-surface-demo'].revision_ids,
    ['revision-operations-1', 'revision-operations-2']
  );
  assert.equal(operations.operations['operation-replace-1'].result_revision_id, 'revision-operations-2');
  assert.equal(operations.revisions['revision-operations-2'].byte_length, 72);
});

test('reduces durable display, V4 interaction, grace, and prune tombstone shapes', async () => {
  const events = [
    ...await jsonl('operations-v1-lifecycle.jsonl'),
    ...lifecycleExtensions()
  ];
  const operations = reduceEvents(events).canvas.operations_v1;

  assert.equal(operations.redirect_commands['command-display-operations-2'].action, 'redirect');
  assert.equal(operations.display_target.revision_id, 'revision-operations-2');
  assert.equal(operations.interaction_cursor, 1);
  assert.equal(operations.interactions[0].event_name, 'decision.selected');
  assert.equal(operations.pruning.state, 'normal');
  assert.equal(operations.pruning.active_request, null);
  assert.equal(operations.pruning.requests['pruning-request-1'].observed_bytes, 1073741824);
  assert.equal(operations.prune_tombstones['revision-operations-1'].reason, 'manual');
});

test('durably completes cleanup-only pruning only for the active request below soft', async () => {
  const lifecycle = await jsonl('operations-v1-lifecycle.jsonl');
  const pruningRequest = lifecycleExtensions()[2];
  const completion = pruningCompletion();
  const operations = reduceEvents([...lifecycle, pruningRequest, completion]).canvas.operations_v1;

  assert.equal(operations.pruning.state, 'normal');
  assert.equal(operations.pruning.active_request, null);
  assert.deepEqual(
    operations.pruning.completions['pruning-request-1'],
    completion.completion
  );

  assert.throws(
    () => reduceEvents([...lifecycle, completion]),
    /pruning completion request is not active/
  );
  assert.throws(
    () => reduceEvents([
      ...lifecycle,
      pruningRequest,
      pruningCompletion({ completion: { final_total_bytes: 1073741824 } })
    ]),
    /pruning completion total is not below soft limit/
  );
  const extra = pruningCompletion();
  extra.completion.unexpected = true;
  assert.throws(
    () => reduceEvents([...lifecycle, pruningRequest, extra]),
    /pruning completion expected fields/
  );
});

test('fails closed on unknown versions/types, duplicate identities, stale lineage, and unsafe targets', async () => {
  const lifecycle = await jsonl('operations-v1-lifecycle.jsonl');
  const [published, derived, committed] = lifecycle;

  assert.throws(() => reduceEvents([{ ...published, event_version: 5 }]), /unsupported event_version 5/);
  assert.throws(
    () => reduceEvents([published, { ...derived, event_id: 'event-unknown-v4', event_type: 'canvas.unknown' }]),
    /unknown v4 event_type canvas\.unknown/
  );

  const duplicateDerivation = structuredClone(derived);
  duplicateDerivation.event_id = 'event-duplicate-derivation';
  duplicateDerivation.surface.operations_surface_id = 'operations-surface-other';
  duplicateDerivation.surface.current_revision_id = 'revision-operations-other';
  duplicateDerivation.surface.revision_ids = ['revision-operations-other'];
  duplicateDerivation.revision.operations_surface_id = 'operations-surface-other';
  duplicateDerivation.revision.revision_id = 'revision-operations-other';
  duplicateDerivation.derivation.result_operations_surface_id = 'operations-surface-other';
  duplicateDerivation.derivation.result_revision_id = 'revision-operations-other';
  assert.throws(() => reduceEvents([published, derived, duplicateDerivation]), /duplicate derivation idempotency key/);

  const duplicateOperation = structuredClone(committed);
  duplicateOperation.event_id = 'event-duplicate-operation';
  assert.throws(() => reduceEvents([...lifecycle, duplicateOperation]), /duplicate operation id/);

  const stale = structuredClone(committed);
  stale.event_id = 'event-stale-operation';
  stale.operation.source_revision_id = 'revision-unknown';
  assert.throws(() => reduceEvents([published, derived, stale]), /operation source revision is not current/);

  const outsideLineage = structuredClone(committed);
  outsideLineage.event_id = 'event-outside-lineage';
  outsideLineage.surface.revision_ids = ['revision-operations-2'];
  assert.throws(() => reduceEvents([published, derived, outsideLineage]), /operation revision order mismatch/);

  const [display, interaction, pruning, tombstone] = lifecycleExtensions();
  const pruneCurrent = structuredClone(tombstone);
  pruneCurrent.event_id = 'event-prune-current';
  pruneCurrent.tombstone.revision_id = 'revision-operations-2';
  pruneCurrent.tombstone.content_sha256 = committed.revision.content_sha256;
  pruneCurrent.tombstone.blob_ref = committed.revision.blob_ref;
  assert.throws(
    () => reduceEvents([...lifecycle, pruning, pruneCurrent]),
    /current operations revision cannot be pruned/
  );

  const mismatchedInteraction = structuredClone(interaction);
  mismatchedInteraction.event_id = 'event-mismatched-interaction';
  mismatchedInteraction.interaction.event_id = mismatchedInteraction.event_id;
  mismatchedInteraction.interaction.revision_id = 'revision-operations-1';
  assert.throws(
    () => reduceEvents([...lifecycle, display, mismatchedInteraction]),
    /operations interaction display target mismatch/
  );
});

test('rebuilds the same projection after restart and reports valid orphan blobs', async () => {
  const state = await createState('ide-extension-operations-replay-');
  try {
    const events = await jsonl('operations-v1-lifecycle.jsonl');
    await writeEvents(state.eventsFile, events);
    await putLifecycleBlobs(state.blobStore);
    const orphan = await state.blobStore.put(Buffer.from('<p>orphan</p>'));
    const store = createProjectionStore({ ...state, canvasBlobStore: state.blobStore });

    const first = await store.reconcile();
    await rm(state.workbenchFile);
    const second = await store.reconcile();

    assert.deepEqual(second.projection, first.projection);
    assert.equal(second.projection_checksum, first.projection_checksum);
    assert.equal(second.projection_checksum, projectionChecksum(reduceEvents(events)));
    assert.equal(second.repaired, true);
    assert.deepEqual(second.canvas_blobs.missing_references, []);
    assert.deepEqual(second.canvas_blobs.unreferenced_blobs, [orphan.sha256]);
  } finally {
    await rm(state.stateDir, { recursive: true, force: true });
  }
});

test('fails closed before append when a committed blob is missing or no store is configured', async () => {
  const state = await createState('ide-extension-operations-missing-');
  try {
    const events = await jsonl('operations-v1-lifecycle.jsonl');
    await writeEvents(state.eventsFile, events.slice(0, 2));
    await putLifecycleBlobs(state.blobStore, false);

    const store = createProjectionStore({ ...state, canvasBlobStore: state.blobStore });
    await assert.rejects(store.commitEvent(events[2]), (error) => {
      assert.equal(error.code, 'canvas_blob_reference_invalid');
      assert.equal(error.cause_code, 'canvas_blob_not_found');
      assert.equal(error.revision_id, 'revision-operations-2');
      return true;
    });
    assert.equal((await readEvents(state.eventsFile)).length, 2);

    const withoutBlobStore = createProjectionStore(state);
    await assert.rejects(withoutBlobStore.reconcile(), (error) => {
      assert.equal(error.code, 'canvas_blob_store_required');
      return true;
    });
  } finally {
    await rm(state.stateDir, { recursive: true, force: true });
  }
});

test('fails closed when a referenced blob is corrupt', async () => {
  const state = await createState('ide-extension-operations-corrupt-');
  try {
    const events = await jsonl('operations-v1-lifecycle.jsonl');
    await writeEvents(state.eventsFile, events);
    const { replacement } = await putLifecycleBlobs(state.blobStore);
    await writeFile(path.join(state.blobStore.blob_dir, `${replacement.sha256}.html`), 'corrupt', 'utf8');

    const store = createProjectionStore({ ...state, canvasBlobStore: state.blobStore });
    await assert.rejects(store.reconcile(), (error) => {
      assert.equal(error.code, 'canvas_blob_reference_invalid');
      assert.equal(error.cause_code, 'canvas_blob_corrupt');
      assert.equal(error.revision_id, 'revision-operations-2');
      return true;
    });
  } finally {
    await rm(state.stateDir, { recursive: true, force: true });
  }
});

test('keeps an appended V4 event authoritative across projection failure', async () => {
  const state = await createState('ide-extension-operations-projection-failure-');
  let writeCount = 0;
  const writeProjection = async (...args) => {
    writeCount += 1;
    if (writeCount === 2) {
      const error = new Error('injected projection failure');
      error.code = 'EIO';
      throw error;
    }
    return atomicWriteJson(...args);
  };

  try {
    const events = await jsonl('operations-v1-lifecycle.jsonl');
    await writeEvents(state.eventsFile, events.slice(0, 2));
    await putLifecycleBlobs(state.blobStore);
    const failingStore = createProjectionStore({
      ...state,
      canvasBlobStore: state.blobStore,
      writeProjection
    });
    await failingStore.reconcile();
    await assert.rejects(failingStore.commitEvent(events[2]), (error) => {
      assert.equal(error.code, 'reconciliation_required');
      assert.equal(error.event_id, 'event-operations-replaced');
      return true;
    });
    assert.equal((await readEvents(state.eventsFile)).length, 3);

    const recovered = await createProjectionStore({
      ...state,
      canvasBlobStore: state.blobStore
    }).reconcile();
    assert.equal(recovered.event_count, 3);
    assert.equal(recovered.projection.canvas.operations_v1.surfaces['operations-surface-demo'].current_revision_id, 'revision-operations-2');
    assert.equal(recovered.canvas_blobs.unreferenced_blobs.includes(events[2].operation.result_digest), false);
  } finally {
    await rm(state.stateDir, { recursive: true, force: true });
  }
});
