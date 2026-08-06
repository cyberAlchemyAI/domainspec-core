import test from 'node:test';
import assert from 'node:assert/strict';
import { canonicalJson, sha256 } from '../src/canonical-json.mjs';
import { createEpisodeJournal } from '../src/journal.mjs';

const graph = 'a'.repeat(64);
const scope = { principal_id: 'principal:1', tenant_or_workspace_id: 'workspace:1', vault_scope: 'animejs-agent-knowledge-vault', capability_audience: 'animejs-work-episode-append', policy_epoch: 'policy:1', operation: 'open_episode' };
const proposed = (episodeId = 'episode:1', revision = 1, commandId = 'cmd:1') => ({ episode_id: episodeId, revision, event_type: 'EpisodeOpened', command_id: commandId, graph_digest: graph, payload: { goal: 'Learn timelines' } });
const append = (journal, options = {}) => journal.append({ scope, requestDigest: options.requestDigest ?? sha256({ command: options.command ?? 1 }), proposedEvent: options.proposedEvent ?? proposed(), expectedRevision: options.expectedRevision ?? 0, expectedTailDigest: options.expectedTailDigest ?? null, idempotencyKey: options.idempotencyKey ?? 'idem:1', failurePoint: options.failurePoint ?? null });

test('canonical JSON is stable and rejects ambiguous values', () => {
  assert.equal(canonicalJson({ z: 1, a: { d: 2, c: 3 } }), '{"a":{"c":3,"d":2},"z":1}');
  assert.equal(sha256({ b: 2, a: 1 }), sha256({ a: 1, b: 2 }));
  assert.throws(() => canonicalJson({ bad: undefined }), /undefined/);
  assert.throws(() => canonicalJson({ bad: Number.NaN }), /non-finite/);
});

test('identical idempotent retry replays one event', async () => {
  const journal = createEpisodeJournal({ clock: () => '2026-08-05T00:00:00Z' });
  const first = await append(journal);
  const replay = await append(journal);
  assert.deepEqual([first.status, replay.status, journal.events('episode:1').length], ['accepted', 'replayed', 1]);
  assert.deepEqual(replay.receipt, first.receipt);
});

test('same key with different request body appends nothing', async () => {
  const journal = createEpisodeJournal();
  await append(journal);
  const mismatch = await append(journal, { requestDigest: sha256({ different: true }) });
  assert.deepEqual([mismatch.status, mismatch.diagnostic.code, journal.events('episode:1').length], ['invalid_request', 'IDEMPOTENCY_MISMATCH', 1]);
});

test('two stale writers commit exactly one event', async () => {
  const journal = createEpisodeJournal();
  const [left, right] = await Promise.all([
    append(journal, { idempotencyKey: 'left', requestDigest: sha256({ writer: 'left' }) }),
    append(journal, { idempotencyKey: 'right', requestDigest: sha256({ writer: 'right' }) }),
  ]);
  assert.deepEqual([left.status, right.status].sort(), ['accepted', 'conflict']);
  assert.equal(journal.events('episode:1').length, 1);
});

test('crash before commit recovers not_committed and retry appends once', async () => {
  const journal = createEpisodeJournal();
  const failed = await append(journal, { failurePoint: 'before_commit' });
  assert.equal(failed.append_outcome, 'not_committed');
  assert.equal(journal.recover({ scope, recoveryHandle: failed.recovery_handle }).status, 'not_committed');
  const retry = await append(journal);
  assert.deepEqual([retry.status, journal.events('episode:1').length], ['accepted', 1]);
});

test('crash after commit recovers original receipt without second event', async () => {
  const journal = createEpisodeJournal();
  const failed = await append(journal, { failurePoint: 'after_commit' });
  assert.equal(failed.append_outcome, 'committed_receipt_unavailable');
  const recovered = journal.recover({ scope, recoveryHandle: failed.recovery_handle });
  assert.deepEqual([recovered.status, journal.events('episode:1').length], ['accepted', 1]);
  const foreign = journal.recover({ scope: { ...scope, principal_id: 'principal:foreign' }, recoveryHandle: failed.recovery_handle });
  assert.equal(foreign.status, 'denied');
});

test('journal event is digest chained and semantically inert', async () => {
  const journal = createEpisodeJournal({ clock: () => '2026-08-05T00:00:00Z' });
  const result = await append(journal);
  const event = journal.events('episode:1')[0];
  const { event_digest, ...withoutDigest } = event;
  assert.equal(event_digest, sha256(withoutDigest));
  assert.equal(event.prior_event_digest, null);
  assert.deepEqual([result.semantic_effect, result.task_state_unchanged, result.truth_status], ['none', true, 'not_assessed']);
});
