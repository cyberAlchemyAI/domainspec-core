import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

import { validateCandidate } from '../lib/validate-candidate.mjs';

const TEST_DIR = path.dirname(fileURLToPath(import.meta.url));
const RUN_ROOT = path.resolve(TEST_DIR, '../..');
const FIXTURES = path.resolve(RUN_ROOT, 'prototype/fixtures');

function locateRepository(start) {
  let cursor = path.resolve(start);
  while (true) {
    if (existsSync(path.resolve(cursor, '2026-08-03-ontology-authority-agent-context-presentation/educational-video-production-script.md'))) return cursor;
    const parent = path.dirname(cursor);
    if (parent === cursor) throw new Error('repository root with frozen source package was not found');
    cursor = parent;
  }
}

const REPOSITORY_ROOT = locateRepository(RUN_ROOT);

async function loadJson(file) {
  return JSON.parse(await readFile(file, 'utf8'));
}

async function sha256(file) {
  return createHash('sha256').update(await readFile(file)).digest('hex');
}

const schema = await loadJson(path.resolve(RUN_ROOT, 'prototype/contracts/animation-hypothesis-candidate.schema.json'));
const sourceSnapshot = await loadJson(path.resolve(FIXTURES, 'source-snapshot.json'));
const sourceBefore = Object.fromEntries(await Promise.all(sourceSnapshot.artifacts.map(async (artifact) => [artifact.path, await sha256(path.resolve(REPOSITORY_ROOT, artifact.path))])));

test('valid S6 candidate satisfies the bounded OAVA-001 contract', async () => {
  const candidate = await loadJson(path.resolve(FIXTURES, 'candidate.valid.json'));
  assert.deepEqual(await validateCandidate({ candidate, schema, sourceSnapshot, repositoryRoot: REPOSITORY_ROOT }), {
    valid: true,
    code: 'VALID',
    path: '$',
    message: 'candidate satisfies the OAVA-001 contract',
  });
});

for (const [fixture, code, expectedPath] of [
  ['candidate.source-drift.json', 'SOURCE_DRIFT', '$.scene_beat_ref'],
  ['candidate.unknown-field.json', 'SCHEMA_INVALID', '$.unexpected_oava_field'],
  ['candidate.proof-inflation.json', 'PROOF_INFLATION', '$.proof_ledger[1].proof_state'],
  ['candidate.missing-contradiction.json', 'SCHEMA_INVALID', '$.contradiction'],
  ['candidate.reduced-motion-mismatch.json', 'REDUCED_MOTION_MISMATCH', '$.semantic_contract.reduced_motion_state_machine'],
]) {
  test(`${fixture} fails for exactly ${code}`, async () => {
    const candidate = await loadJson(path.resolve(FIXTURES, fixture));
    const result = await validateCandidate({ candidate, schema, sourceSnapshot, repositoryRoot: REPOSITORY_ROOT });
    assert.equal(result.valid, false);
    assert.equal(result.code, code);
    assert.equal(result.path, expectedPath);
  });
}

test('validation leaves every frozen source artifact byte-identical', async () => {
  const sourceAfter = Object.fromEntries(await Promise.all(sourceSnapshot.artifacts.map(async (artifact) => [artifact.path, await sha256(path.resolve(REPOSITORY_ROOT, artifact.path))])));
  assert.deepEqual(sourceAfter, sourceBefore);
});
