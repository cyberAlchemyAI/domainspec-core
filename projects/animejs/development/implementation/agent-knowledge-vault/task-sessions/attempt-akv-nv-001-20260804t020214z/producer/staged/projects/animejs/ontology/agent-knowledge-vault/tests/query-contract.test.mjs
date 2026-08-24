#!/usr/bin/env node

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ABSTENTION_PRECEDENCE, ALGORITHM_VERSION, evaluateDecision } from '../scripts/query.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const fixtures = JSON.parse(readFileSync(resolve(root, 'fixtures/query-cases.json'), 'utf8'));
const schema = JSON.parse(readFileSync(resolve(root, 'schemas/query-receipt.schema.json'), 'utf8'));
const contracts = JSON.parse(readFileSync(resolve(root, 'contracts/query-contracts.json'), 'utf8'));

assert.equal(schema.properties.algorithm_version.type, 'string');
assert.equal(contracts.algorithm_version, ALGORITHM_VERSION);
assert.deepEqual(contracts.primary_precedence, ABSTENTION_PRECEDENCE);
assert.equal(fixtures.cases.length, 8);
assert.equal(new Set(fixtures.cases.map(item => item.id)).size, 8);

for (const fixture of fixtures.cases) {
  const receipt = evaluateDecision({
    id: fixture.id,
    graph_digest: fixtures.graph_digest,
    generated_at: fixtures.generated_at,
    ...fixture.input,
  });
  assert.match(receipt.receipt_id, /^qry:[a-f0-9]{24}$/);
  assert.equal(receipt.schema_version, 'animejs.agent-knowledge-vault.query-receipt.v1');
  assert.equal(receipt.algorithm_version, ALGORITHM_VERSION);
  assert.equal(receipt.graph_digest, fixtures.graph_digest);
  assert.deepEqual(receipt.selected_ids, fixture.expected.selected_ids, `${fixture.id}: selected_ids`);
  assert.equal(receipt.abstention_code, fixture.expected.abstention_code, `${fixture.id}: abstention_code`);
  assert.deepEqual(receipt.subordinate_gaps, fixture.expected.subordinate_gaps, `${fixture.id}: subordinate_gaps`);
  assert.equal(receipt.next_questions.length, fixture.expected.next_question_count, `${fixture.id}: next questions`);
  if (fixture.expected.conflict_count !== undefined) {
    assert.equal(receipt.conflicts.length, fixture.expected.conflict_count, `${fixture.id}: conflicts`);
  }
  if (receipt.abstention_code === null) assert.ok(receipt.selected_ids.length > 0, `${fixture.id}: success selects`);
  else assert.ok(ABSTENTION_PRECEDENCE.includes(receipt.abstention_code), `${fixture.id}: closed code`);
}

const tie = evaluateDecision({
  id: 'determinism-tie',
  graph_digest: fixtures.graph_digest,
  generated_at: fixtures.generated_at,
  version_context: { exact_version: '4.5.0', lock_digest: 'lock:fixture' },
  intent_recognized: true,
  candidates: [
    { id: 'api:animate:waapi', compatible: true, score: 1, evidence_record_ids: ['evidence:z'] },
    { id: 'api:animate:js', compatible: true, score: 1, evidence_record_ids: ['evidence:a'] },
  ],
});
assert.deepEqual(tie.selected_ids, ['api:animate:js', 'api:animate:waapi']);
assert.deepEqual(tie.evidence_record_ids, ['evidence:a', 'evidence:z']);
assert.equal(tie.abstention_code, 'ABSTAIN_AMBIGUOUS_INTENT');
assert.equal(tie.next_questions.length, 1);

console.log('PASS query contract fixtures: 8/8');
