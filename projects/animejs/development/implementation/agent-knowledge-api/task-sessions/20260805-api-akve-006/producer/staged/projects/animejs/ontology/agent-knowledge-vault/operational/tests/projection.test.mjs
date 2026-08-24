import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readdir, readFile, stat } from 'node:fs/promises';
import { compileEpisodeOverlay } from '../src/overlay.mjs';
import { compileNeutralProjection } from '../src/projection.mjs';

const graph = 'a'.repeat(64);
const snapshot = {
  state: {
    episode_id: 'episode:1', revision: 5, lifecycle_state: 'completed', goal: 'Learn timelines', supersedes_episode_id: 'episode:old',
    attempts: [{ ordinal: 1, action_summary: 'Built a timeline', evidence: [{ handle: 'evidence:1', evidence_class: 'test', state: 'admissible' }], outcome: { classification: 'succeeded', observations: ['tests passed'] } }],
  },
};
const allowlistUrl = new URL('../contracts/projection-allowlist.json', import.meta.url);

async function treeDigest(url) {
  const hash = createHash('sha256');
  async function walk(current, prefix = '') {
    for (const name of (await readdir(current)).sort()) {
      const child = new URL(`${name}${(await stat(new URL(name, current))).isDirectory() ? '/' : ''}`, current);
      const relative = `${prefix}${name}`;
      const info = await stat(child);
      if (info.isDirectory()) await walk(child, `${relative}/`);
      else { hash.update(relative); hash.update(await readFile(child)); }
    }
  }
  await walk(url);
  return hash.digest('hex');
}

test('overlay is isolated, strips authority, and creates zero Lessons', () => {
  const overlay = compileEpisodeOverlay({ reductionResults: [{ status: 'current', snapshot }], canonicalGraphDigest: graph });
  assert.equal(overlay.canonical_graph_delta, 0);
  assert.equal(overlay.verified_lessons_created, 0);
  assert.ok(overlay.records.some(record => record.kind === 'supersession_reference'));
  assert.equal(JSON.stringify(overlay).includes('principal_id'), false);
  assert.equal(JSON.stringify(overlay).includes('canonical_relation_id'), false);
  assert.equal(JSON.stringify(overlay).includes('Lesson'), false);
});

test('revoked evidence changes only derived eligibility', () => {
  const original = JSON.stringify(snapshot);
  const overlay = compileEpisodeOverlay({ reductionResults: [{ status: 'current', snapshot }], evidenceEligibility: { 'evidence:1': 'revoked' }, canonicalGraphDigest: graph });
  const episode = overlay.records.find(record => record.kind === 'episode');
  assert.equal(episode.evidence_state, 'unconfirmed');
  assert.equal(JSON.stringify(snapshot), original);
});

test('projection is deterministic and view bounded', async () => {
  const allowlist = JSON.parse(await readFile(allowlistUrl, 'utf8'));
  const overlay = compileEpisodeOverlay({ reductionResults: [{ status: 'current', snapshot }], canonicalGraphDigest: graph });
  const input = { overlay, allowlist, requestedViews: ['operational_episode'], grantedViews: ['operational_episode'], ownerReviewRef: 'review:1' };
  const left = compileNeutralProjection(input);
  const right = compileNeutralProjection(structuredClone(input));
  assert.equal(left.status, 'current');
  assert.equal(left.projection_digest, right.projection_digest);
  assert.deepEqual(left.projection_bytes, right.projection_bytes);
  assert.ok(left.records.every(record => !('kind' in record)));
});

test('projection rejects forbidden owner, path, policy, and prompt-role fields without digest', async () => {
  const allowlist = JSON.parse(await readFile(allowlistUrl, 'utf8'));
  const overlay = compileEpisodeOverlay({ reductionResults: [], canonicalGraphDigest: graph });
  for (const field of ['owner_route', 'private_path', 'policy_epoch', 'role']) {
    const baseRecords = [{ record_id: `doc:${field}`, label: field, summary: 'inert data', record_kind: 'documentation', truth_status: 'not_assessed', clearing_criteria: [], [field]: 'forbidden' }];
    const result = compileNeutralProjection({ baseRecords, overlay, allowlist, requestedViews: ['documentation'], grantedViews: ['documentation'], ownerReviewRef: 'review:1' });
    assert.equal(result.status, 'rejected', field);
    assert.equal('projection_digest' in result, false, field);
  }
});

test('pending and corrupt episodes are explicit while unaffected records remain readable', async () => {
  const allowlist = JSON.parse(await readFile(allowlistUrl, 'utf8'));
  const pendingOverlay = compileEpisodeOverlay({ reductionResults: [{ status: 'pending' }], canonicalGraphDigest: graph });
  assert.equal(compileNeutralProjection({ overlay: pendingOverlay, allowlist, requestedViews: ['operational_episode'], grantedViews: ['operational_episode'], ownerReviewRef: 'review:1' }).diagnostic.code, 'PROJECTION_PENDING');
  const mixed = compileEpisodeOverlay({ reductionResults: [{ status: 'current', snapshot }, { status: 'quarantined', episode_id: 'episode:bad', diagnostic: { code: 'EVENT_DIGEST_MISMATCH' } }], canonicalGraphDigest: graph });
  const result = compileNeutralProjection({ overlay: mixed, allowlist, requestedViews: ['operational_episode'], grantedViews: ['operational_episode'], ownerReviewRef: 'review:1' });
  assert.equal(result.status, 'quarantined');
  assert.ok(result.records.some(record => record.record_id === 'episode:episode:1'));
  assert.equal(result.quarantined[0].episode_id, 'episode:bad');
});

test('projection compilation writes zero canonical vault bytes', async () => {
  const roots = ['../nodes/', '../relations/', '../sources/', '../views/'].map(path => new URL(path, import.meta.url));
  const before = await Promise.all(roots.map(treeDigest));
  const allowlist = JSON.parse(await readFile(allowlistUrl, 'utf8'));
  const overlay = compileEpisodeOverlay({ reductionResults: [{ status: 'current', snapshot }], canonicalGraphDigest: graph });
  compileNeutralProjection({ overlay, allowlist, requestedViews: ['operational_episode'], grantedViews: ['operational_episode'], ownerReviewRef: 'review:1' });
  const after = await Promise.all(roots.map(treeDigest));
  assert.deepEqual(after, before);
});
