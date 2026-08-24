#!/usr/bin/env node

import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SOURCES = resolve(ROOT, 'sources');
const COMMIT = '2c9cf8ea00329f6768c7d7902252ed977d75ce42';
const TREE = '1511dce2d3e54de4c9c9cbfdb1d1dff2248d2c98';
const EXPECTED = 'f4026dec178de523262aca34dcddc5e419681b3494f37f496d9da8553d3ebcc0';
const COUNTS = Object.freeze({ source: 70, type: 70, test: 125, example: 81, 'package-documentation': 2 });
const sha256 = value => createHash('sha256').update(value).digest('hex');

function kind(path) {
  if (path === 'README.md' || path === 'package.json') return 'package-documentation';
  if (path.startsWith('src/')) return 'source';
  if (path.startsWith('dist/modules/') && path.endsWith('.d.ts')) return 'type';
  if (path.startsWith('tests/')) return 'test';
  if (path.startsWith('examples/')) return 'example';
  return null;
}

function evidenceStatus(value) {
  return {
    source: 'source-observed', type: 'type-present', test: 'test-present-not-executed',
    example: 'example-source-present-not-executed', 'package-documentation': 'source-observed',
  }[value];
}

async function build() {
  const response = await fetch(`https://api.github.com/repos/juliangarnier/anime/git/trees/${TREE}?recursive=1`, {
    headers: { Accept: 'application/vnd.github+json', 'User-Agent': 'domainspec-animejs-ontology' },
  });
  assert.equal(response.status, 200);
  const tree = await response.json();
  assert.equal(tree.sha, TREE); assert.equal(tree.truncated, false);
  const rows = tree.tree.filter(item => item.type === 'blob' && kind(item.path))
    .sort((left, right) => left.path.localeCompare(right.path))
    .map(item => {
      const artifactKind = kind(item.path);
      return {
        path: item.path, blob_sha1: item.sha, size: item.size, kind: artifactKind,
        structured_pointer: `git:${COMMIT}:${item.path}`, evidence_status: evidenceStatus(artifactKind),
      };
    });
  const counts = Object.fromEntries(Object.keys(COUNTS).map(value => [value, rows.filter(row => row.kind === value).length]));
  assert.equal(rows.length, 348); assert.deepEqual(counts, COUNTS);
  const jsonl = rows.map(row => `${JSON.stringify(row)}\n`).join('');
  assert.equal(sha256(jsonl), EXPECTED);
  mkdirSync(SOURCES, { recursive: true });
  writeFileSync(resolve(SOURCES, 'repository.jsonl'), jsonl);
  writeFileSync(resolve(SOURCES, 'repository-manifest.json'), `${JSON.stringify({
    schema_version: 'animejs.agent-knowledge-vault.repository-manifest.v2', version: '4.5.0', commit_sha: COMMIT,
    commit_tree_sha1: TREE, tree_truncated: false, row_count: 348, counts,
    manifest_jsonl_sha256: sha256(jsonl), expected_manifest_jsonl_sha256: EXPECTED, digest_match: true,
    materialization_status: 'reproduced-and-validated-candidate-local', authority_effect: 'none',
    presence_ceiling: 'tests and examples are present-not-executed',
  }, null, 2)}\n`);
  console.log(`BUILT repository manifest v2: 348 rows, digest ${sha256(jsonl)}`);
}

function check() {
  const bytes = readFileSync(resolve(SOURCES, 'repository.jsonl'));
  const rows = bytes.toString().trimEnd().split('\n').map(JSON.parse);
  const manifest = JSON.parse(readFileSync(resolve(SOURCES, 'repository-manifest.json')));
  assert.equal(rows.length, 348); assert.equal(new Set(rows.map(row => row.path)).size, 348);
  assert.deepEqual(manifest.counts, COUNTS); assert.equal(sha256(bytes), EXPECTED);
  assert.equal(manifest.manifest_jsonl_sha256, EXPECTED); assert.equal(manifest.tree_truncated, false);
  console.log('PASS repository ingest v2: 348 rows (70/70/125/81/2), exact returned digest reproduced');
}

try { if (process.argv.includes('--build')) await build(); else if (process.argv.includes('--check')) check(); else throw new Error('usage: --build | --check'); }
catch (error) { console.error(error.stack ?? error.message); process.exitCode = 2; }
