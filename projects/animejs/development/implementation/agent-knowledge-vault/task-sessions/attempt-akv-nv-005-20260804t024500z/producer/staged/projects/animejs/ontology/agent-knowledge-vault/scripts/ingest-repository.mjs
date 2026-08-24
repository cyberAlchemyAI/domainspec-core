#!/usr/bin/env node

import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SOURCES = resolve(ROOT, 'sources');
const VERSION = '4.5.0';
const COMMIT = '2c9cf8ea00329f6768c7d7902252ed977d75ce42';
const TREE_SHA1 = '1511dce2d3e54de4c9c9cbfdb1d1dff2248d2c98';
const API = `https://api.github.com/repos/juliangarnier/anime/git/trees/${TREE_SHA1}?recursive=1`;
const PRIOR_RETURNED_DIGEST = 'f4026dec178de523262aca34dcddc5e419681b3494f37f496d9da8553d3ebcc0';
const EXPECTED_COUNTS = Object.freeze({ source: 70, type: 70, test: 125, example: 81, package_documentation: 2 });

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

function classify(path) {
  if (path === 'README.md' || path === 'package.json') return 'package_documentation';
  if (path.startsWith('src/')) return 'source';
  if (path.startsWith('dist/modules/') && path.endsWith('.d.ts')) return 'type';
  if (path.startsWith('tests/')) return 'test';
  if (path.startsWith('examples/')) return 'example';
  return null;
}

function evidenceStatus(kind) {
  if (kind === 'test') return 'test-present-not-executed';
  if (kind === 'example') return 'example-source-present-not-executed';
  if (kind === 'package_documentation') return 'package-documentation-observed';
  return 'source-observed-not-runtime-executed';
}

async function build() {
  const response = await fetch(API, { headers: { Accept: 'application/vnd.github+json', 'User-Agent': 'domainspec-animejs-ontology' } });
  assert.equal(response.status, 200, `GitHub tree HTTP ${response.status}`);
  const tree = await response.json();
  assert.equal(tree.truncated, false, 'recursive tree is truncated');
  assert.equal(tree.sha, TREE_SHA1, 'commit tree identity changed');
  const selected = tree.tree
    .filter(item => item.type === 'blob' && classify(item.path))
    .sort((left, right) => left.path.localeCompare(right.path));
  const rows = selected.map(item => {
    const kind = classify(item.path);
    return {
      id: `artifact:repo:${sha256(`${COMMIT}\0${item.path}`).slice(0, 20)}`,
      path: item.path,
      blob_sha1: item.sha,
      size: item.size,
      kind,
      structured_pointer: `https://github.com/juliangarnier/anime/blob/${COMMIT}/${item.path}`,
      evidence_status: evidenceStatus(kind),
      commit_sha: COMMIT,
    };
  });
  const counts = Object.fromEntries(Object.keys(EXPECTED_COUNTS).map(kind => [kind, rows.filter(row => row.kind === kind).length]));
  assert.equal(rows.length, 348);
  assert.deepEqual(counts, EXPECTED_COUNTS);
  const jsonl = `${rows.map(row => JSON.stringify(row)).join('\n')}\n`;
  const candidateDigest = sha256(jsonl);
  mkdirSync(SOURCES, { recursive: true });
  writeFileSync(resolve(SOURCES, 'repository.jsonl'), jsonl);
  writeFileSync(resolve(SOURCES, 'repository-manifest.json'), `${JSON.stringify({
    schema_version: 'animejs.agent-knowledge-vault.repository-manifest.v1',
    repository: 'juliangarnier/anime',
    version: VERSION,
    commit_sha: COMMIT,
    commit_tree_sha1: tree.sha,
    tree_truncated: tree.truncated,
    selection: ['README.md', 'package.json', 'src/**', 'dist/modules/**/*.d.ts', 'tests/**', 'examples/**'],
    row_count: rows.length,
    counts,
    manifest_jsonl_sha256: candidateDigest,
    prior_returned_not_written_contract: {
      manifest_jsonl_sha256: PRIOR_RETURNED_DIGEST,
      match: candidateDigest === PRIOR_RETURNED_DIGEST,
      authority: 'historical-research-receipt-only',
    },
    presence_ceiling: 'tests and examples are present-not-executed; no runtime behavior is inferred',
    materialization_status: 'reproduced-and-validated-candidate-local',
    authority_effect: 'none',
  }, null, 2)}\n`);
  console.log(`BUILT repository manifest: ${rows.length} rows, digest ${candidateDigest}`);
}

function check() {
  const jsonl = readFileSync(resolve(SOURCES, 'repository.jsonl'));
  const rows = jsonl.toString().trimEnd().split('\n').map(line => JSON.parse(line));
  const manifest = JSON.parse(readFileSync(resolve(SOURCES, 'repository-manifest.json'), 'utf8'));
  assert.equal(manifest.version, VERSION);
  assert.equal(manifest.commit_sha, COMMIT);
  assert.equal(manifest.commit_tree_sha1, TREE_SHA1);
  assert.equal(manifest.tree_truncated, false);
  assert.equal(rows.length, 348);
  assert.equal(new Set(rows.map(row => row.path)).size, 348);
  assert.equal(new Set(rows.map(row => row.id)).size, 348);
  assert.deepEqual(manifest.counts, EXPECTED_COUNTS);
  assert.equal(manifest.manifest_jsonl_sha256, sha256(jsonl));
  for (const row of rows) {
    assert.equal(row.commit_sha, COMMIT);
    assert.match(row.blob_sha1, /^[a-f0-9]{40}$/);
    assert.equal(row.kind, classify(row.path));
    if (row.kind === 'test') assert.equal(row.evidence_status, 'test-present-not-executed');
    if (row.kind === 'example') assert.equal(row.evidence_status, 'example-source-present-not-executed');
  }
  console.log(`PASS repository ingest: 348 rows (70/70/125/81/2), digest ${manifest.manifest_jsonl_sha256}, prior-contract-match=${manifest.prior_returned_not_written_contract.match}`);
}

try {
  if (process.argv.includes('--build')) await build();
  else if (process.argv.includes('--check')) check();
  else throw new Error('usage: ingest-repository.mjs --build | --check');
} catch (error) {
  console.error(error.stack ?? error.message);
  process.exitCode = 2;
}
