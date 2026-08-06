import test from 'node:test';
import assert from 'node:assert/strict';
import { sha256 } from '../src/canonical-json.mjs';
import { reduceEpisode } from '../src/reducer.mjs';

const graph = 'a'.repeat(64);
function makeEvent({ revision, event_type, payload, prior_event_digest = null }) {
  const event = {
    contract: 'animejs-work-episode-event/0.1.0', event_id: `event:${revision}`, episode_id: 'episode:1', revision,
    event_type, command_id: `command:${revision}`, request_digest: sha256({ revision }), principal_id: 'principal:1',
    policy_epoch: 'policy:1', graph_digest: graph, recorded_at: `2026-08-05T00:00:0${revision}Z`, payload, prior_event_digest,
  };
  event.event_digest = sha256(event);
  return event;
}

function journal() {
  const events = [];
  events.push(makeEvent({ revision: 1, event_type: 'EpisodeOpened', payload: {
    goal: 'Learn timelines', started_at: '2026-08-05T00:00:00Z', tags: [],
    task_snapshot: { id: 'task:1' }, task_digest: 'b'.repeat(64),
    version_context_snapshot: { id: 'version:1', animejs: '4.5.0' }, version_context_digest: 'c'.repeat(64),
    owner_binding: { principal_id: 'principal:1', tenant_or_workspace_id: 'workspace:1', vault_scope: 'animejs-agent-knowledge-vault', capability_audience: 'animejs-work-episode-append', delegation_id: null },
    supersedes_episode_id: null,
  } }));
  events.push(makeEvent({ revision: 2, event_type: 'AttemptAppended', payload: { ordinal: 1, action_summary: 'Try timeline', input_artifact_handles: [] }, prior_event_digest: events[0].event_digest }));
  events.push(makeEvent({ revision: 3, event_type: 'OutcomeRecorded', payload: { attempt_ordinal: 1, classification: 'blocked', observations: ['missing browser'], witness_handles: [] }, prior_event_digest: events[1].event_digest }));
  events.push(makeEvent({ revision: 4, event_type: 'EpisodeClosed', payload: { disposition: 'blocked' }, prior_event_digest: events[2].event_digest }));
  return events;
}

test('reducer is byte deterministic and preserves inert opening context', () => {
  const events = journal();
  const left = reduceEpisode({ events, reducerVersion: '1.0.0' });
  const right = reduceEpisode({ events: structuredClone(events), reducerVersion: '1.0.0' });
  assert.equal(left.status, 'current');
  assert.deepEqual(left.snapshot_bytes, right.snapshot_bytes);
  assert.equal(left.snapshot_digest, right.snapshot_digest);
  assert.equal(left.snapshot.state.task_digest, 'b'.repeat(64));
  assert.equal(left.snapshot.truth_status, 'not_assessed');
});

test('reducer quarantines a gap without synthesizing history', () => {
  const events = journal();
  const result = reduceEpisode({ events: [events[0], events[2]] });
  assert.deepEqual([result.status, result.diagnostic.code, result.snapshot], ['quarantined', 'JOURNAL_GAP', null]);
});

test('reducer quarantines a fork', () => {
  const events = journal();
  const result = reduceEpisode({ events: [events[0], { ...events[0], event_id: 'fork' }] });
  assert.deepEqual([result.status, result.diagnostic.code], ['quarantined', 'JOURNAL_FORK']);
});

test('reducer rejects shuffled order instead of sorting', () => {
  const events = journal();
  const result = reduceEpisode({ events: [events[1], events[0], events[2], events[3]] });
  assert.deepEqual([result.status, result.diagnostic.code], ['quarantined', 'JOURNAL_ORDER_INVALID']);
});

test('reducer rejects event digest mismatch', () => {
  const events = journal();
  events[2] = { ...events[2], payload: { ...events[2].payload, classification: 'succeeded' } };
  const result = reduceEpisode({ events });
  assert.deepEqual([result.status, result.diagnostic.code], ['quarantined', 'EVENT_DIGEST_MISMATCH']);
});

test('reducer upgrade retains prior snapshot identity', () => {
  const events = journal();
  const oldResult = reduceEpisode({ events, reducerVersion: '1.0.0' });
  const oldRecord = { reducer_version: '1.0.0', last_event_digest: oldResult.snapshot.last_event_digest, snapshot_digest: oldResult.snapshot_digest };
  const upgraded = reduceEpisode({ events, reducerVersion: '2.0.0', previousSnapshots: [oldRecord] });
  assert.equal(upgraded.status, 'current');
  assert.equal(upgraded.migration_receipt.prior_snapshot_retained, true);
  assert.equal(upgraded.migration_receipt.prior_snapshot_digest, oldResult.snapshot_digest);
  assert.notEqual(upgraded.snapshot_key, oldResult.snapshot_key);
});

test('empty journal emits no apparent snapshot', () => {
  const result = reduceEpisode({ events: [] });
  assert.deepEqual([result.status, result.snapshot], ['empty', null]);
});
