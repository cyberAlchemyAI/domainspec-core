import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import {
  BRIDGE_EVENT_VERSION,
  CANVAS_EVENT_VERSION,
  projectionChecksum,
  reduceEvents
} from '../src/kernel/projector.mjs';
import { createProjectionStore } from '../src/kernel/storage.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const eventDir = path.join(projectRoot, 'tests/fixtures/events');
const schemaDir = path.join(projectRoot, 'tests/fixtures/schemas');

async function jsonl(name) {
  const source = await readFile(path.join(eventDir, name), 'utf8');
  return source.trim().split('\n').map(JSON.parse);
}

async function json(name) {
  return JSON.parse(await readFile(path.join(schemaDir, name), 'utf8'));
}

async function v2AuthorizationEvents() {
  const envelope = await json('agent-envelope.valid.bridge.json');
  const approval = await json('approval-record.valid.bridge.json');
  const receipt = await json('receipt.valid.authorization.json');
  const preparedEnvelope = structuredClone(envelope);
  preparedEnvelope.state = 'awaiting_approval';
  preparedEnvelope.authorization_receipt_id = null;
  preparedEnvelope.receipts = [];
  preparedEnvelope.approval.actor = null;
  preparedEnvelope.approval.approved_at = null;
  const preparedApproval = structuredClone(approval);
  preparedApproval.state = 'pending';
  preparedApproval.actor = null;
  preparedApproval.authorized_at = null;
  preparedApproval.authorization_receipt_id = null;
  return [
    {
      event_version: BRIDGE_EVENT_VERSION,
      event_id: 'event-mixed-v2-prepared',
      event_type: 'envelope.prepared',
      envelope: preparedEnvelope,
      approval: preparedApproval,
      created_at: '2026-07-12T00:00:00.000Z'
    },
    {
      event_version: BRIDGE_EVENT_VERSION,
      event_id: 'event-mixed-v2-authorized',
      event_type: 'approval.granted',
      envelope,
      approval,
      receipt,
      artifact_refs: ['artifact-mixed-authorization'],
      created_at: receipt.created_at
    }
  ];
}

test('keeps legacy projection exact until the first canvas event', async () => {
  const legacy = await jsonl('v1-lifecycle.jsonl');
  const expected = JSON.parse(
    await readFile(path.join(eventDir, 'v1-lifecycle.projection.json'), 'utf8')
  );
  assert.deepEqual(reduceEvents(legacy), expected);
  assert.equal(Object.hasOwn(reduceEvents(legacy), 'canvas'), false);
  assert.equal(CANVAS_EVENT_VERSION, 3);
});

test('replays mixed v1, v2, and canvas history', async () => {
  const events = [
    ...await jsonl('v1-lifecycle.jsonl'),
    ...await v2AuthorizationEvents(),
    ...await jsonl('canvas-lifecycle.jsonl')
  ];
  const projection = reduceEvents(events);
  const surface = projection.canvas.surfaces['surface-craft-class'];

  assert.equal(projection.envelopes['env-v1-fixture'].state, 'passed');
  assert.equal(projection.receipts.length, 2);
  assert.equal(surface.title, 'Craft class revised');
  assert.deepEqual(surface.revision_ids, ['revision-craft-1', 'revision-craft-2']);
  assert.equal(projection.canvas.current_surface_id, surface.surface_id);
  assert.equal(projection.canvas.interaction_cursor, 2);
  assert.deepEqual(
    projection.canvas.interactions.map((interaction) => interaction.event_name),
    ['decision.selected', 'craft.action_requested']
  );
});

test('fails closed on duplicate hash, stale revision, cursor gap, and future version', async () => {
  const [published, interaction, republished] = await jsonl('canvas-lifecycle.jsonl');
  const duplicateHash = structuredClone(republished);
  duplicateHash.event_id = 'event-canvas-duplicate-hash';
  duplicateHash.revision.revision_id = 'revision-craft-duplicate';
  duplicateHash.surface.current_revision_id = duplicateHash.revision.revision_id;
  duplicateHash.surface.revision_ids = ['revision-craft-1', duplicateHash.revision.revision_id];
  duplicateHash.revision.content_sha256 = published.revision.content_sha256;
  assert.throws(() => reduceEvents([published, duplicateHash]), /duplicate canvas revision hash/);

  const stale = structuredClone(interaction);
  stale.event_id = 'event-canvas-stale';
  stale.interaction.event_id = stale.event_id;
  stale.interaction.revision_id = 'revision-unknown';
  assert.throws(() => reduceEvents([published, stale]), /interaction revision is not current/);

  const cursorGap = structuredClone(interaction);
  cursorGap.event_id = 'event-canvas-cursor-gap';
  cursorGap.interaction.event_id = cursorGap.event_id;
  cursorGap.interaction.cursor = 2;
  assert.throws(() => reduceEvents([published, cursorGap]), /interaction cursor is not monotonic/);

  assert.throws(
    () => reduceEvents([{ ...published, event_version: 5 }]),
    /unsupported event_version 5/
  );
});

test('storage restart rebuilds the same canvas projection and checksum', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-canvas-replay-'));
  const eventsFile = path.join(stateDir, 'events.jsonl');
  const workbenchFile = path.join(stateDir, 'workbench.json');
  const artifactDir = path.join(stateDir, 'artifacts');

  try {
    const events = [
      ...await jsonl('v1-lifecycle.jsonl'),
      ...await v2AuthorizationEvents(),
      ...await jsonl('canvas-lifecycle.jsonl')
    ];
    await writeFile(eventsFile, `${events.map(JSON.stringify).join('\n')}\n`, 'utf8');
    const store = createProjectionStore({ eventsFile, workbenchFile, artifactDir });
    const first = await store.reconcile();
    await rm(workbenchFile);
    const second = await store.reconcile();

    assert.deepEqual(second.projection, first.projection);
    assert.equal(second.projection_checksum, first.projection_checksum);
    assert.equal(second.projection_checksum, projectionChecksum(reduceEvents(events)));
    assert.equal(second.repaired, true);
  } finally {
    await rm(stateDir, { recursive: true, force: true });
  }
});
