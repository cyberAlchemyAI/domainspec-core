import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { decideTransition, applyEpisodeEvent } from '../src/transition-oracle.mjs';

const graph = 'a'.repeat(64);
const bindings = {
  episode_id: 'episode:1', principal_id: 'principal:1', tenant_or_workspace_id: 'workspace:1',
  vault_scope: 'animejs-agent-knowledge-vault', capability_audience: 'animejs-work-episode-append', delegation_id: null,
  task_snapshot: { id: 'task:1', title: 'Use timelines' }, task_digest: 'b'.repeat(64),
  version_context_snapshot: { id: 'version:1', animejs: '4.5.0' }, version_context_digest: 'c'.repeat(64),
};
const command = (operation, episode_id, expected_revision, payload) => ({ command_id: `cmd:${operation}:${expected_revision}`, operation, episode_id, expected_revision, expected_graph_digest: graph, payload });
const openCommand = command('open_episode', null, 0, { task_handle: 'task:h', version_context_handle: 'version:h', goal: 'Learn timelines', started_at: '2026-08-05T00:00:00Z', tags: [], supersedes_episode_id: null });

function opened() {
  const result = decideTransition({ command: openCommand, bindings });
  assert.equal(result.accepted, true);
  return applyEpisodeEvent(null, result.event);
}

function withAttempt() {
  const state = opened();
  const result = decideTransition({ state, command: command('append_attempt', state.episode_id, 1, { ordinal: 1, action_summary: 'Try a timeline', input_artifact_handles: [] }), bindings });
  assert.equal(result.accepted, true);
  return applyEpisodeEvent(state, result.event);
}

test('open binds inert Task and VersionContext snapshots', () => {
  const state = opened();
  assert.equal(state.task_digest, bindings.task_digest);
  assert.equal(state.version_context_digest, bindings.version_context_digest);
  assert.equal(state.opening_graph_digest, graph);
  assert.equal(state.owner_binding.capability_audience, 'animejs-work-episode-append');
});

test('transition rejects cross-attempt evidence rebind', () => {
  const state = withAttempt();
  const result = decideTransition({
    state,
    command: command('attach_evidence', state.episode_id, 2, { attempt_ordinal: 1, evidence_handle: 'evidence:foreign' }),
    bindings,
    resolvedEvidence: { handle: 'evidence:foreign', target_episode_id: state.episode_id, target_attempt_ordinal: 2, task_digest: state.task_digest, version_context_digest: state.version_context_digest, state: 'admissible', evidence_class: 'test' },
  });
  assert.deepEqual([result.accepted, result.code], [false, 'EVIDENCE_TARGET_MISMATCH']);
  assert.equal(result.event, null);
});

test('transition enforces evidence-backed success and one outcome', () => {
  let state = withAttempt();
  const withoutEvidence = decideTransition({ state, command: command('record_outcome', state.episode_id, 2, { attempt_ordinal: 1, classification: 'succeeded', observations: [], witness_handles: [] }), bindings });
  assert.equal(withoutEvidence.code, 'EVIDENCE_REQUIRED');
  const attach = decideTransition({ state, command: command('attach_evidence', state.episode_id, 2, { attempt_ordinal: 1, evidence_handle: 'evidence:1' }), bindings, resolvedEvidence: { handle: 'evidence:1', target_episode_id: state.episode_id, target_attempt_ordinal: 1, task_digest: state.task_digest, version_context_digest: state.version_context_digest, state: 'admissible', evidence_class: 'test' } });
  state = applyEpisodeEvent(state, attach.event);
  const outcome = decideTransition({ state, command: command('record_outcome', state.episode_id, 3, { attempt_ordinal: 1, classification: 'succeeded', observations: ['passed'], witness_handles: ['evidence:1'] }), bindings });
  state = applyEpisodeEvent(state, outcome.event);
  const duplicate = decideTransition({ state, command: command('record_outcome', state.episode_id, 4, { attempt_ordinal: 1, classification: 'failed', observations: [], witness_handles: [] }), bindings });
  assert.deepEqual([outcome.accepted, duplicate.code], [true, 'DUPLICATE_OUTCOME']);
});

test('transition rejects dangling close and post-terminal append', () => {
  let state = withAttempt();
  const dangling = decideTransition({ state, command: command('close_episode', state.episode_id, 2, { disposition: 'blocked' }), bindings });
  assert.equal(dangling.code, 'DANGLING_ATTEMPT');
  const outcome = decideTransition({ state, command: command('record_outcome', state.episode_id, 2, { attempt_ordinal: 1, classification: 'blocked', observations: [], witness_handles: [] }), bindings });
  state = applyEpisodeEvent(state, outcome.event);
  const close = decideTransition({ state, command: command('close_episode', state.episode_id, 3, { disposition: 'blocked' }), bindings });
  state = applyEpisodeEvent(state, close.event);
  const after = decideTransition({ state, command: command('append_attempt', state.episode_id, 4, { ordinal: 2, action_summary: 'forbidden', input_artifact_handles: [] }), bindings });
  assert.deepEqual([close.accepted, after.code], [true, 'EPISODE_TERMINAL']);
});

test('transition rejects reopen and supersession cycle', () => {
  const state = opened();
  assert.equal(decideTransition({ state, command: openCommand, bindings }).code, 'REOPEN_FORBIDDEN');
  const superseding = { ...openCommand, command_id: 'cmd:supersede', payload: { ...openCommand.payload, supersedes_episode_id: 'episode:old' } };
  const cycle = decideTransition({ command: superseding, bindings: { ...bindings, superseded_episode: { terminal: true }, supersession_cycle: true } });
  assert.equal(cycle.code, 'SUPERSESSION_CYCLE');
});

test('transition fixture declares all oracle scenario witnesses', async () => {
  const fixture = JSON.parse(await readFile(new URL('../fixtures/transition-cases.json', import.meta.url), 'utf8'));
  assert.deepEqual(fixture.covered_scenarios, ['TS-15', 'TS-17', 'TS-18', 'TS-19', 'TS-20', 'TS-21']);
  assert.equal(Object.keys(fixture.expected_codes).length, 6);
});
