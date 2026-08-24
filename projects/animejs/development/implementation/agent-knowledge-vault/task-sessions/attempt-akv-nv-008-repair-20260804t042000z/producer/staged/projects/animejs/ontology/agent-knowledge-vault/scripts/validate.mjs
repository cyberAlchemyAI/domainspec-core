#!/usr/bin/env node

import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, relative, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const REPOSITORY_ROOT = process.env.AKV_REPO_ROOT ? resolve(process.env.AKV_REPO_ROOT) : resolve(ROOT, '../../../..');

function sha256(data) {
  return createHash('sha256').update(data).digest('hex');
}

function loadJson(relativePath) {
  return JSON.parse(readFileSync(resolve(ROOT, relativePath), 'utf8'));
}

function walk(directory) {
  const rows = [];
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    const path = resolve(directory, entry.name);
    if (entry.isDirectory()) rows.push(...walk(path));
    else if (entry.isFile()) rows.push(path);
  }
  return rows;
}

function runCheck(commandId, argv) {
  const result = spawnSync(argv[0], argv.slice(1), { cwd: REPOSITORY_ROOT, encoding: 'utf8', timeout: 180_000, maxBuffer: 2 * 1024 * 1024 });
  assert.equal(result.status, 0, `${commandId} failed\nstdout=${result.stdout}\nstderr=${result.stderr}`);
  return { command_id: commandId, result: 'pass', stdout: result.stdout.trim() };
}

const profile = loadJson('profile.json');
const nodeVocabulary = loadJson('contracts/node-vocabulary.json');
const relationVocabulary = loadJson('contracts/relation-vocabulary.json');
const relationDecisions = loadJson('contracts/relation-decisions.json');
const nodes = loadJson('nodes/nodes.json');
const relations = loadJson('relations/relations.json');
const docsManifest = loadJson('sources/documentation-manifest.json');
const repoManifest = loadJson('sources/repository-manifest.json');
const coverage = loadJson('views/documentation-coverage.json');
const lessons = loadJson('views/work-lessons.json');
const search = loadJson('indexes/search.json');
const residue = loadJson('RESIDUE.json');
const receipt = loadJson('receipts/validation-receipt.json');

assert.equal(profile.authority.effect, 'none');
assert.equal(profile.publication.release_admission, 'not-granted');
assert.equal(nodeVocabulary.node_kind_count, 21);
assert.equal(relationVocabulary.relation_count, 17);
assert.deepEqual(relationDecisions.counts, { RETAIN: 17, MERGE: 5, DEFER: 3, KILL: 0 });
assert.equal(docsManifest.row_count, 418);
assert.equal(docsManifest.semantic_jsonl_sha256, '681f004e04a91ab1a3462e882edff24d09454297f34a41863e81df06e20066fb');
assert.equal(docsManifest.raw_page_set_sha256, '63125e931350f5dbf8552a289ac80d687bb1867e7c94c1e2d6e33904f16befcd');
assert.equal(docsManifest.semantic_match, true);
assert.equal(docsManifest.raw_set_match, true);
assert.equal(repoManifest.row_count, 348);
assert.deepEqual(repoManifest.counts, { source: 70, type: 70, test: 125, example: 81, 'package-documentation': 2 });
assert.equal(repoManifest.manifest_jsonl_sha256, 'f4026dec178de523262aca34dcddc5e419681b3494f37f496d9da8553d3ebcc0');
assert.equal(repoManifest.digest_match, true);
assert.equal(nodes.counts.total, 1185);
assert.equal(nodes.counts.Lesson, 0);
assert.equal(relations.relation_count, 418);
assert.equal(coverage.route_count, 418);
assert.equal(search.entry_count, 766);
assert.equal(lessons.verified_lesson_count, 0);
assert.equal(lessons.abstention_code, 'ABSTAIN_NO_VERIFIED_LESSON');
assert.equal(residue.open_count, 6);
assert.equal(new Set([nodes.graph_digest, relations.graph_digest, coverage.graph_digest, search.graph_digest]).size, 1);

const nodeById = new Map(nodes.nodes.map(node => [node.id, node]));
assert.equal(nodeById.size, nodes.nodes.length);
for (const edge of relations.relations) {
  assert.equal(nodeById.get(edge.source_id)?.kind, edge.source_kind, `source endpoint: ${edge.id}`);
  assert.equal(nodeById.get(edge.target_id)?.kind, edge.target_kind, `target endpoint: ${edge.id}`);
}
assert.ok(!relations.relations.some(edge => ['addresses', 'contains', 'yields', 'suggestsNextQuestion', 'citesEvidence', 'observes', 'applies', 'exposesGap'].includes(edge.type)));
assert.ok(!nodes.nodes.some(node => ['Lesson', 'WorkEpisode', 'Attempt', 'Outcome'].includes(node.kind)));
for (const node of nodes.nodes.filter(node => node.kind === 'EvidenceRecord')) assert.equal(node.payload.runtime_observed, false);

const receiptArtifacts = new Map(receipt.bound_artifacts.map(item => [item.path, item]));
assert.equal(receiptArtifacts.size, receipt.bound_artifacts.length);
for (const artifact of receipt.bound_artifacts) {
  const data = readFileSync(resolve(ROOT, artifact.path));
  assert.equal(data.length, artifact.size_bytes, `${artifact.path}: size`);
  assert.equal(sha256(data), artifact.sha256, `${artifact.path}: digest`);
}
const liveInventory = walk(ROOT)
  .map(path => relative(ROOT, path).replaceAll('\\', '/'))
  .filter(path => path !== 'receipts/validation-receipt.json')
  .sort();
assert.deepEqual([...receiptArtifacts.keys()].sort(), liveInventory, 'validation receipt inventory drift');
assert.equal(receipt.graph_digest, nodes.graph_digest);
assert.equal(receipt.status, 'candidate-local-binding-complete');
assert.equal(receipt.authority_effect, 'none');
assert.equal(receipt.release_admission, 'not-granted');

const rootRelative = 'projects/animejs/ontology/agent-knowledge-vault';
const checks = [
  runCheck('query-contract', ['node', `${rootRelative}/tests/query-contract.test.mjs`]),
  runCheck('relation-definitions', ['node', `${rootRelative}/scripts/validate-relations.mjs`, '--definitions-only']),
  runCheck('relation-witnesses', ['node', `${rootRelative}/tests/relation-witnesses.test.mjs`]),
  runCheck('documentation-ingest', ['node', `${rootRelative}/scripts/ingest-documentation.mjs`, '--check']),
  runCheck('repository-ingest', ['node', `${rootRelative}/scripts/ingest-repository.mjs`, '--check']),
  runCheck('graph-freshness', ['node', `${rootRelative}/scripts/build-graph.mjs`, '--check']),
  runCheck('view-freshness', ['node', `${rootRelative}/scripts/build-views.mjs`, '--check']),
  runCheck('coverage-smoke', ['node', `${rootRelative}/scripts/query.mjs`, 'coverage', '/documentation/animation/']),
];

console.log(`PASS ontology validation: ${checks.length}/8 checks, ${nodes.counts.total} nodes, ${relations.relation_count} relations, ${search.entry_count} search entries, graph ${nodes.graph_digest}`);
