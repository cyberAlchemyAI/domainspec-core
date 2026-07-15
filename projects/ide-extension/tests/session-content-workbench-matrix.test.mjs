import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const fixtureDir = path.join(projectRoot, 'tests/fixtures/canvas');

test('three standalone surfaces share one generic browser protocol and no specialized mutation route', async () => {
  const server = await readFile(path.join(projectRoot, 'src/server.mjs'), 'utf8');
  assert.doesNotMatch(server, /\/api\/decision(?:\/|')/);
  const craftRoutes = [...new Set(
    [...server.matchAll(/\/api\/craft\/[a-z0-9_/-]+/g)].map((match) => match[0])
  )];
  assert.deepEqual(craftRoutes, ['/api/craft/frontier']);

  const fixtures = await Promise.all([
    'presentation.html',
    'presentation-v2.html',
    'decision.html',
    'craft.html'
  ].map(async (name) => ({ name, source: await readFile(path.join(fixtureDir, name), 'utf8') })));

  for (const { name, source } of fixtures) {
    assert.match(source, /<!doctype html>/i, name);
    assert.match(source, /<meta name="viewport"/, name);
    assert.doesNotMatch(source, /\.innerHTML/, name);
    for (const script of source.matchAll(/<script>([\s\S]*?)<\/script>/g)) {
      assert.doesNotThrow(() => new Function(script[1]), name);
    }
  }

  for (const name of ['decision.html', 'craft.html']) {
    const source = fixtures.find((fixture) => fixture.name === name).source;
    assert.match(source, /ide-extension\.canvas\.event/);
    assert.match(source, /parent\.postMessage/);
    assert.doesNotMatch(source, /fetch\s*\(/);
  }
  assert.match(fixtures.find(({ name }) => name === 'decision.html').source, /decision\.selected/);
  assert.match(fixtures.find(({ name }) => name === 'craft.html').source, /craft\.action_requested/);
});
