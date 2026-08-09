import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';

const root = new URL('../', import.meta.url);
const docs = ['README.md', 'TOWER.md', 'levels/L0-corpus.md', 'levels/L1-residue-map.md', 'levels/L2-closure-plan.md', 'gates/closure-gates.md', 'residue/open-residue.md'];
const readJson = (relative) => readFile(new URL(relative, root), 'utf8').then(JSON.parse);

test('candidate navigation spine carries one honest L0 ceiling', async () => {
  for (const relative of docs) {
    const content = (await readFile(new URL(relative, root), 'utf8')).toLowerCase();
    for (const token of ['candidate', 'synthetic', 'authority_effect: none']) assert.ok(content.includes(token), `${relative} lacks ${token}`);
  }
});

test('control plane keeps selection open, residue open, validation not-run, and promotion blocked', async () => {
  const [residue, definition, promotion, expected] = await Promise.all([
    readJson('residue/residue-items.json'), readJson('definitions/definition-bindings.json'), readJson('promotions/blocked-promotion.json'), readJson('validation/expected-validation-records.json')
  ]);
  assert.equal(residue.items[0].status, 'open');
  assert.equal(definition.bindings[0].binding_status, 'reference-only');
  assert.equal(promotion.records[0].gate_result, 'block');
  assert.equal(expected.expected[0].status, 'not-run');
});
