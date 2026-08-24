#!/usr/bin/env node

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { evaluateDecision, queryCoverage } from '../scripts/query.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const load = relative => JSON.parse(readFileSync(resolve(ROOT, relative), 'utf8'));
const profile = load('profile.json');
const nodes = load('nodes/nodes.json');
const relations = load('relations/relations.json');
const coverage = load('views/documentation-coverage.json');
const lessons = load('views/work-lessons.json');
const gaps = load('views/unresolved-gaps.json');
const search = load('indexes/search.json');

assert.equal(profile.ontology_type, 'knowledge-vault');
assert.equal(profile.authority.effect, 'none');
assert.equal(nodes.counts.total, 1185);
assert.equal(nodes.counts.DocumentationTopic, 418);
assert.equal(nodes.counts.EvidenceRecord, 766);
assert.equal(nodes.counts.VersionContext, 1);
assert.equal(nodes.counts.Lesson, 0);
assert.equal(relations.relation_count, 418);
assert.equal(new Set(relations.relations.map(edge => edge.id)).size, 418);
assert.ok(relations.relations.every(edge => edge.type === 'documents'));
assert.equal(coverage.routes.length, 418);
assert.ok(coverage.routes.every(row => row.validation_status === 'validated'));
assert.equal(search.entries.length, 766);
assert.equal(lessons.verified_lesson_count, 0);
assert.equal(lessons.lessons.length, 0);
assert.equal(gaps.gap_count, 7);

const animationCoverage = queryCoverage('/documentation/animation/', coverage);
assert.equal(animationCoverage.canonical_path, '/documentation/animation/');
assert.equal(animationCoverage.validation_status, 'validated');
assert.equal(animationCoverage.evidence_record_ids.length, 1);

const graphDigest = nodes.graph_digest;
const success = evaluateDecision({
  id: 'ontology-integration-js',
  graph_digest: graphDigest,
  generated_at: '2026-08-04T00:00:00.000Z',
  version_context: { exact_version: '4.5.0', lock_digest: 'fixture-lock' },
  intent_recognized: true,
  candidates: [{ id: 'api:animate:js', compatible: true, score: 1, evidence_record_ids: [coverage.routes[0].evidence_record_ids[0]] }],
});
assert.deepEqual(success.selected_ids, ['api:animate:js']);
assert.equal(success.abstention_code, null);

const performance = evaluateDecision({
  id: 'ontology-integration-performance',
  graph_digest: graphDigest,
  generated_at: '2026-08-04T00:00:00.000Z',
  version_context: { exact_version: '4.5.0', lock_digest: 'fixture-lock' },
  intent_recognized: true,
  performance_intent: true,
  executed_performance_witness: false,
  candidates: [{ id: 'api:animate:waapi', compatible: true, score: 1, evidence_record_ids: [] }],
});
assert.equal(performance.abstention_code, 'ABSTAIN_PERFORMANCE_EVIDENCE');
assert.deepEqual(performance.selected_ids, []);

console.log('PASS ontology integration tests: coverage, graph, search, abstention, authority');
