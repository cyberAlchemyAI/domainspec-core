import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';

const root = new URL('../', import.meta.url);
const read = (relative) => readFile(new URL(relative, root), 'utf8').then(JSON.parse);

test('projection contract closes the static, privacy-filtered output seam', async () => {
  const [schema, policy, contract] = await Promise.all([
    read('schemas/projection.schema.json'), read('privacy/privacy-policy.json'), read('projection/projection-contract.json')
  ]);
  assert.equal(schema.authority_effect, 'none');
  assert.ok(schema.required_keys.includes('adjacency'));
  assert.ok(policy.classes.synthetic.denied_keys.includes('private_locator'));
  assert.ok(policy.denied_value_sentinels.includes('PRIVATE-CONTENT'));
  assert.deepEqual(contract.reserved_consumer_contract.forbidden, ['POST', 'publication', 'effectful_transport']);
  assert.equal(contract.projection_rules.replace_on_failure, false);
});
