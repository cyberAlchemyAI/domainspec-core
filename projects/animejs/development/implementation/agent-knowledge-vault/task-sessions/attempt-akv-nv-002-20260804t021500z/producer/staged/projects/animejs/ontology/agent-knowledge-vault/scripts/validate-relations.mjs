#!/usr/bin/env node

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const MERGED = new Set(['addresses', 'contains', 'yields', 'suggestsNextQuestion', 'citesEvidence']);
const DEFERRED = new Set(['observes', 'applies', 'exposesGap']);
const EXPECTED_MERGE_REPRESENTATIONS = Object.freeze({
  'AKV-REL-009': 'WorkEpisode.task_id canonical; addresses derived and never stored',
  'AKV-REL-011': 'Attempt.episode_id canonical; WorkEpisode.attempt_ids is a sorted derived index; contains never stored',
  'AKV-REL-018': 'Outcome.attempt_id canonical; Attempt.outcome_id is a unique reverse-derived lookup; yields never stored',
  'AKV-REL-024': 'NextQuestion.gap_id canonical; QueryReceipt.next_question_ids is derived; suggestsNextQuestion never stored',
  'AKV-REL-025': 'QueryReceipt.evidence_record_ids canonical; citesEvidence never stored',
});

export function loadRelationContracts(root = ROOT) {
  return {
    vocabulary: JSON.parse(readFileSync(resolve(root, 'contracts/relation-vocabulary.json'), 'utf8')),
    decisions: JSON.parse(readFileSync(resolve(root, 'contracts/relation-decisions.json'), 'utf8')),
    schema: JSON.parse(readFileSync(resolve(root, 'schemas/relation.schema.json'), 'utf8')),
  };
}

export function validateRelation(relation, nodesById, contracts = loadRelationContracts()) {
  const definition = contracts.vocabulary.relations.find(item => item.name === relation.type);
  assert.ok(definition, `undeclared or non-stored relation: ${relation.type}`);
  assert.ok(!MERGED.has(relation.type), `merged relation must not be stored: ${relation.type}`);
  assert.ok(!DEFERRED.has(relation.type), `deferred relation must not be stored: ${relation.type}`);
  assert.match(relation.id, /^edge:[a-z0-9:_./-]+$/);
  assert.ok(nodesById.has(relation.source_id), `missing source node: ${relation.source_id}`);
  assert.ok(nodesById.has(relation.target_id), `missing target node: ${relation.target_id}`);
  assert.equal(nodesById.get(relation.source_id).kind, relation.source_kind, `source kind mismatch: ${relation.id}`);
  assert.equal(nodesById.get(relation.target_id).kind, relation.target_kind, `target kind mismatch: ${relation.id}`);
  assert.ok(definition.source_kinds.includes(relation.source_kind), `invalid source endpoint: ${relation.id}`);
  if (definition.target_kinds.includes('$same-as-source')) {
    assert.equal(relation.target_kind, relation.source_kind, `supersedes endpoint kind mismatch: ${relation.id}`);
  } else {
    assert.ok(definition.target_kinds.includes(relation.target_kind), `invalid target endpoint: ${relation.id}`);
  }
  assert.equal(new Set(relation.evidence_record_ids).size, relation.evidence_record_ids.length, `duplicate evidence IDs: ${relation.id}`);
  return true;
}

export function validateDefinitions(root = ROOT) {
  const { vocabulary, decisions, schema } = loadRelationContracts(root);
  assert.equal(vocabulary.relation_count, 17);
  assert.equal(vocabulary.relations.length, 17);
  assert.equal(decisions.decisions.length, 25);
  assert.deepEqual(decisions.counts, { RETAIN: 17, MERGE: 5, DEFER: 3, KILL: 0 });
  assert.equal(new Set(vocabulary.relations.map(item => item.relation_id)).size, 17);
  assert.equal(new Set(vocabulary.relations.map(item => item.name)).size, 17);
  assert.equal(new Set(decisions.decisions.map(item => item.relation_id)).size, 25);
  const retained = decisions.decisions.filter(item => item.disposition === 'RETAIN');
  assert.deepEqual(retained.map(item => item.name).sort(), vocabulary.relations.map(item => item.name).sort());
  assert.deepEqual(schema.properties.type.enum.slice().sort(), vocabulary.relations.map(item => item.name).sort());
  for (const [relationId, representation] of Object.entries(EXPECTED_MERGE_REPRESENTATIONS)) {
    const decision = decisions.decisions.find(item => item.relation_id === relationId);
    assert.equal(decision.disposition, 'MERGE');
    assert.equal(decision.canonical_representation, representation);
    assert.ok(!vocabulary.relations.some(item => item.name === decision.name));
  }
  for (const name of DEFERRED) {
    const decision = decisions.decisions.find(item => item.name === name);
    assert.equal(decision.disposition, 'DEFER');
    assert.ok(!vocabulary.relations.some(item => item.name === name));
  }
  return { retained: 17, merged: 5, deferred: 3 };
}

if (process.argv.includes('--definitions-only')) {
  const result = validateDefinitions();
  console.log(`PASS relation definitions: ${result.retained} retained, ${result.merged} merged, ${result.deferred} deferred`);
}
