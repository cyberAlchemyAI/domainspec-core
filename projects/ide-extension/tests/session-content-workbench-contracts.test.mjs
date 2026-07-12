import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { validateSchema } from '../src/kernel/schema-validation.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const fixtureDir = path.join(projectRoot, 'tests/fixtures/schemas');

async function fixture(name) {
  return JSON.parse(await readFile(path.join(fixtureDir, name), 'utf8'));
}

test('accepts the canvas publish and interaction contracts', async () => {
  assert.deepEqual(
    await validateSchema(
      'canvas-publish-request',
      await fixture('canvas-publish-request.valid.json')
    ),
    { valid: true, errors: [] }
  );
  assert.deepEqual(
    await validateSchema(
      'canvas-interaction-request',
      await fixture('canvas-interaction-request.valid.json')
    ),
    { valid: true, errors: [] }
  );
});

test('rejects non-normalized and non-HTML publish paths', async () => {
  for (const name of [
    'canvas-publish-request.invalid-absolute.json',
    'canvas-publish-request.invalid-traversal.json',
    'canvas-publish-request.invalid-backslash.json',
    'canvas-publish-request.invalid-percent.json',
    'canvas-publish-request.invalid-extension.json'
  ]) {
    const result = await validateSchema('canvas-publish-request', await fixture(name));
    assert.equal(result.valid, false, name);
    assert.ok(result.errors.some((error) => error.keyword === 'pattern'), name);
  }
});

test('rejects unknown publish kinds and caller authority fields', async () => {
  const kind = await validateSchema(
    'canvas-publish-request',
    await fixture('canvas-publish-request.invalid-kind.json')
  );
  assert.equal(kind.valid, false);
  assert.ok(kind.errors.some((error) => error.keyword === 'enum'));

  const additional = await validateSchema(
    'canvas-publish-request',
    await fixture('canvas-publish-request.invalid-additional.json')
  );
  assert.equal(additional.valid, false);
  assert.ok(additional.errors.some((error) => error.keyword === 'additionalProperties'));
});

test('rejects malformed interaction bindings and payload shape', async () => {
  const cases = [
    ['canvas-interaction-request.invalid-payload.json', 'type'],
    ['canvas-interaction-request.invalid-event-name.json', 'pattern'],
    ['canvas-interaction-request.invalid-surface.json', 'pattern'],
    ['canvas-interaction-request.invalid-additional.json', 'additionalProperties']
  ];

  for (const [name, keyword] of cases) {
    const result = await validateSchema('canvas-interaction-request', await fixture(name));
    assert.equal(result.valid, false, name);
    assert.ok(result.errors.some((error) => error.keyword === keyword), name);
  }
});
