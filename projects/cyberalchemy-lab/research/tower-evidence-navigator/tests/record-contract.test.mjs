import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';

const root = new URL('../', import.meta.url);
const read = (relative) => readFile(new URL(relative, root), 'utf8').then(JSON.parse);

test('closed record vocabulary and shared invariants are explicit', async () => {
  const schema = await read('schemas/lab-records.schema.json');
  assert.deepEqual(schema.record_kinds, ['SourceSnapshot', 'TowerPackageSnapshot', 'Claim', 'EvidenceAnchor', 'DefinitionReference', 'ResidueItem', 'OntologyCandidate', 'ValidationRecord', 'PromotionRecord', 'Relation']);
  assert.equal(schema.authority_effect, 'none');
  assert.ok(schema.common_required.includes('record_snapshot_id'));
  assert.equal(schema.kind_requirements.PromotionRecord.includes('gate_result'), true);
});

test('relation registry is closed and rejects unsupported endpoint pairs', async () => {
  const registry = await read('ontology/relation-registry.json');
  const kinds = new Set(registry.relations.map((entry) => entry.kind));
  assert.deepEqual([...kinds], ['package_contains', 'anchored_by', 'supports', 'references_definition', 'derived_from', 'blocked_by', 'contradicts']);
  const anchored = registry.relations.find((entry) => entry.kind === 'anchored_by');
  assert.deepEqual(anchored.from, ['Claim', 'OntologyCandidate']);
  assert.deepEqual(anchored.to, ['EvidenceAnchor']);
  assert.equal(kinds.has('same_as'), false);
});
