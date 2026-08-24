import test from 'node:test';
import assert from 'node:assert/strict';
import { createEpisodeJournal } from '../src/journal.mjs';
import { reduceEpisode } from '../src/reducer.mjs';
import { createEpisodeService } from '../src/episode-service.mjs';

const graph = 'a'.repeat(64);
const hostContext = { principal_id: 'principal:1', tenant_or_workspace_id: 'workspace:1', capabilities: ['animejs-work-episode-append'], policy_epoch: 'policy:1', vault_scope: 'animejs-agent-knowledge-vault', request_id: 'request:1', received_at: '2026-08-05T00:00:00Z' };
const appendGrant = { authorized: true, capability_audience: 'animejs-work-episode-append', delegation_id: null };
const receiptGrant = { authorized: true, capability_audience: 'animejs-work-episode-receipt-read' };
const command = (operation, episode_id, expected_revision, payload, key = `idem:${operation}:${expected_revision}`) => ({ contract: 'animejs-work-episode-command/0.1.0', command_id: `cmd:${operation}:${expected_revision}`, idempotency_key: key, operation, episode_id, expected_revision, expected_graph_digest: graph, payload });
const open = () => command('open_episode', null, 0, { task_handle: 'task:h', version_context_handle: 'version:h', goal: 'Learn timelines', started_at: '2026-08-05T00:00:00Z', tags: [], supersedes_episode_id: null }, 'idem:open');

function harness({ schedulerStatus = 'current' } = {}) {
  const journal = createEpisodeJournal({ clock: () => '2026-08-05T00:00:00Z' });
  const states = new Map();
  const taskSource = { id: 'task:1', title: 'Learn timelines', owner_route: 'private', approval: 'private' };
  const versionSource = { id: 'version:1', animejs: '4.5.0', policy_epoch: 'private' };
  let taskResolutions = 0;
  let versionResolutions = 0;
  const reducerScheduler = { schedule: async episodeId => {
    if (schedulerStatus !== 'current') return schedulerStatus;
    const reduced = reduceEpisode({ events: journal.events(episodeId) });
    if (reduced.status === 'current') states.set(episodeId, { ...reduced.snapshot.state, last_event_digest: reduced.snapshot.last_event_digest });
    return reduced.status;
  } };
  const service = createEpisodeService({
    journal,
    taskResolver: { resolve: async () => { taskResolutions += 1; return { snapshot: taskSource, digest: 'b'.repeat(64) }; } },
    versionContextResolver: { resolve: async () => { versionResolutions += 1; return { snapshot: versionSource, digest: 'c'.repeat(64) }; } },
    evidenceResolver: { resolve: async (handle, target) => handle.startsWith('/') || handle.startsWith('http')
      ? { accepted: false, code: 'EVIDENCE_HANDLE_REVOKED' }
      : { accepted: true, binding: { handle, target_episode_id: target.episode_id, target_attempt_ordinal: target.attempt_ordinal, task_digest: target.task_digest, version_context_digest: target.version_context_digest, producer_episode_id: target.episode_id, producer_attempt_ordinal: target.attempt_ordinal, criterion: 'tests pass', evidence_class: 'test', scope: 'attempt', state: 'admissible' } } },
    episodeReader: { readState: async episodeId => states.get(episodeId) ?? null },
    reducerScheduler,
  });
  return { service, journal, states, taskSource, versionSource, counts: () => ({ taskResolutions, versionResolutions }) };
}

test('open resolves and stores inert Task and VersionContext snapshots once', async () => {
  const h = harness();
  const result = await h.service.appendCommand({ hostContext, grant: appendGrant, command: open() });
  assert.equal(result.status, 'accepted');
  assert.equal(result.receipt.reducer_status, 'current');
  assert.deepEqual(h.counts(), { taskResolutions: 1, versionResolutions: 1 });
  const episodeId = result.receipt.episode_id;
  h.taskSource.title = 'mutated later';
  assert.equal(h.states.get(episodeId).task_snapshot.title, 'Learn timelines');
  assert.equal('owner_route' in h.states.get(episodeId).task_snapshot, false);
  assert.equal('policy_epoch' in h.states.get(episodeId).version_context_snapshot, false);
});

test('identical open retry replays the original episode and event', async () => {
  const h = harness();
  const first = await h.service.appendCommand({ hostContext, grant: appendGrant, command: open() });
  const replay = await h.service.appendCommand({ hostContext, grant: appendGrant, command: open() });
  assert.deepEqual([first.status, replay.status, first.receipt.episode_id, replay.receipt.episode_id, h.journal.events(first.receipt.episode_id).length], ['accepted', 'replayed', first.receipt.episode_id, first.receipt.episode_id, 1]);
  assert.deepEqual(h.counts(), { taskResolutions: 1, versionResolutions: 1 });
});

test('episode lifecycle binds evidence, outcome, and close with zero Task effect', async () => {
  const h = harness();
  const opened = await h.service.appendCommand({ hostContext, grant: appendGrant, command: open() });
  const id = opened.receipt.episode_id;
  const attempt = await h.service.appendCommand({ hostContext, grant: appendGrant, command: command('append_attempt', id, 1, { ordinal: 1, action_summary: 'Try timeline', input_artifact_handles: [] }) });
  const premature = await h.service.appendCommand({ hostContext, grant: appendGrant, command: command('record_outcome', id, 2, { attempt_ordinal: 1, classification: 'succeeded', observations: [], witness_handles: [] }) });
  assert.equal(premature.diagnostic.code, 'EVIDENCE_REQUIRED');
  const evidence = await h.service.appendCommand({ hostContext, grant: appendGrant, command: command('attach_evidence', id, 2, { attempt_ordinal: 1, evidence_handle: 'evidence:1' }) });
  const outcome = await h.service.appendCommand({ hostContext, grant: appendGrant, command: command('record_outcome', id, 3, { attempt_ordinal: 1, classification: 'succeeded', observations: ['passed'], witness_handles: ['evidence:1'] }) });
  const duplicate = await h.service.appendCommand({ hostContext, grant: appendGrant, command: command('record_outcome', id, 4, { attempt_ordinal: 1, classification: 'failed', observations: [], witness_handles: [] }, 'idem:duplicate') });
  const closed = await h.service.appendCommand({ hostContext, grant: appendGrant, command: command('close_episode', id, 4, { disposition: 'completed' }) });
  const terminal = await h.service.appendCommand({ hostContext, grant: appendGrant, command: command('append_attempt', id, 5, { ordinal: 2, action_summary: 'forbidden', input_artifact_handles: [] }) });
  assert.deepEqual([attempt.status, evidence.status, outcome.status, duplicate.diagnostic.code, closed.status, terminal.diagnostic.code], ['accepted', 'accepted', 'accepted', 'DUPLICATE_OUTCOME', 'accepted', 'EPISODE_TERMINAL']);
  assert.deepEqual([closed.semantic_effect, closed.task_state_unchanged, closed.truth_status], ['none', true, 'not_assessed']);
  assert.equal(h.journal.events(id).length, 5);
});

test('raw path evidence and host-field spoofing append nothing', async () => {
  const h = harness();
  const opened = await h.service.appendCommand({ hostContext, grant: appendGrant, command: open() });
  const id = opened.receipt.episode_id;
  await h.service.appendCommand({ hostContext, grant: appendGrant, command: command('append_attempt', id, 1, { ordinal: 1, action_summary: 'Try', input_artifact_handles: [] }) });
  const before = h.journal.events(id).length;
  const forged = await h.service.appendCommand({ hostContext, grant: appendGrant, command: command('attach_evidence', id, 2, { attempt_ordinal: 1, evidence_handle: '/tmp/result' }) });
  const spoof = await h.service.appendCommand({ hostContext, grant: appendGrant, command: { ...command('close_episode', id, 2, { disposition: 'abandoned' }), principal_id: 'self' } });
  assert.deepEqual([forged.status, spoof.status, h.journal.events(id).length], ['evidence_rejected', 'invalid_request', before]);
});

test('committed receipt loss is recoverable only under receipt capability', async () => {
  const h = harness();
  const failed = await h.service.appendCommand({ hostContext, grant: appendGrant, command: open(), failurePoint: 'after_commit' });
  assert.deepEqual([failed.status, failed.diagnostic.code], ['temporary_failure', 'RECEIPT_UNAVAILABLE']);
  const denied = h.service.recoverReceipt({ hostContext, grant: appendGrant, recoveryHandle: failed.recovery_handle });
  assert.equal(denied.status, 'denied');
  const recovered = h.service.recoverReceipt({ hostContext, grant: receiptGrant, recoveryHandle: failed.recovery_handle });
  assert.equal(recovered.status, 'accepted');
  assert.equal(h.journal.events(recovered.receipt.episode_id).length, 1);
});

test('accepted append receipt remains stable when projection is pending', async () => {
  const h = harness({ schedulerStatus: 'pending' });
  const result = await h.service.appendCommand({ hostContext, grant: appendGrant, command: open() });
  assert.deepEqual([result.status, result.receipt.reducer_status, result.semantic_effect], ['accepted', 'pending', 'none']);
});

test('denial happens before episode lookup and leaks no target metadata', async () => {
  const h = harness();
  const result = await h.service.appendCommand({ hostContext, grant: { ...appendGrant, authorized: false }, command: command('close_episode', 'episode:secret', 9, { disposition: 'blocked' }) });
  assert.deepEqual([result.status, result.diagnostic.code, result.receipt], ['denied', 'DENIED', null]);
  assert.equal(JSON.stringify(result).includes('episode:secret'), false);
});
