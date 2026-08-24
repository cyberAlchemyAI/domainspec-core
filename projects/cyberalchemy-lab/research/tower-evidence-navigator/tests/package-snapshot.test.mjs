import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import { buildSnapshot, validateSnapshot } from '../tools/build-package-snapshot.mjs';

const root = new URL('../', import.meta.url);

test('the explicit package manifest is complete and normalized-self-valid', async () => {
  const saved = await readFile(new URL('PACKAGE-SNAPSHOT.json', root), 'utf8').then(JSON.parse);
  validateSnapshot(saved);
  const rebuilt = await buildSnapshot({ root: new URL('.', root).pathname, check: true });
  assert.deepEqual(rebuilt, saved);
  assert.equal(saved.artifacts.some((artifact) => artifact.path === 'projection/generated-projection.json'), false);
});

test('a changed normalized manifest is rejected', async () => {
  const saved = await readFile(new URL('PACKAGE-SNAPSHOT.json', root), 'utf8').then(JSON.parse);
  saved.artifacts[0].content_digest = 'f'.repeat(64);
  assert.throws(() => validateSnapshot(saved), (error) => error.code === 'CAL_PACKAGE_MANIFEST_STALE');
});
