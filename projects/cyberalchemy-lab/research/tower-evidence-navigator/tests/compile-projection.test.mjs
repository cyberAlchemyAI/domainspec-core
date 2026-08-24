import assert from 'node:assert/strict';
import { mkdtemp, readFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { compileToFile } from '../tools/compile-projection.mjs';

const root = new URL('../', import.meta.url);
const input = new URL('fixtures/valid/synthetic-one-tower.json', root);

test('compiler creates byte-stable static projection without writing sources', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'cal-compile-'));
  const first = join(directory, 'first.json');
  const second = join(directory, 'second.json');
  const projection = await compileToFile({ input, output: first, sourceRoot: new URL('.', root).pathname });
  await compileToFile({ input, output: second, sourceRoot: new URL('.', root).pathname });
  assert.equal(projection.authority_effect, 'none');
  assert.equal(projection.invalid, false);
  assert.equal(projection.stale, false);
  assert.deepEqual(await readFile(first), await readFile(second));
});
