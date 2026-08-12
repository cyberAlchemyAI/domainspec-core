#!/usr/bin/env node
'use strict';

const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');

const candidateModule = path.resolve(process.argv[2] || '');
const supportInventory = path.resolve(process.argv[3] || '');
if (!fs.existsSync(candidateModule) || !fs.existsSync(supportInventory)) {
  throw new Error('usage: test-pending-source-admission.cjs <candidate-module> <support-inventory>');
}

const TS = '2026-08-09T22:06:00Z';

function sha256(filePath) {
  return crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex');
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function createFixture({ mismatch = false, extraGap = false } = {}) {
  const repository = fs.mkdtempSync(path.join(os.tmpdir(), 'inventory-pending-source-test-'));
  const root = path.join(repository, '.arcanum', 'inventory');
  for (const relative of ['lib', 'schemas', 'scripts', 'entries']) {
    fs.mkdirSync(path.join(root, relative), { recursive: true });
  }
  fs.copyFileSync(candidateModule, path.join(root, 'lib', 'inventory-update.cjs'));
  for (const relative of [
    'lib/operation-receipt.cjs',
    'schemas/inventory.operation-receipt.v1.schema.json',
    'scripts/validate-index-json.sh',
    'scripts/validate_projection_conformance.py',
  ]) {
    fs.copyFileSync(path.join(supportInventory, relative), path.join(root, relative));
  }
  const emptyMaps = {
    by_id: {},
    by_type: {},
    by_tag: {},
    by_source: {},
    by_status: {},
    by_evidence_card: {},
    by_evidence_set: {},
    by_namespace: {},
    by_record_class: {},
    by_concept: {},
  };
  writeJson(path.join(root, 'index.json'), {
    schema_version: 'inventory.index.v0.1',
    inventory_root: '.arcanum/inventory',
    generated_at: '2026-08-09T21:00:00Z',
    human_index: 'index.md',
    entries: [],
    indexes: emptyMaps,
    projections: [],
    validation: {
      parseable: true,
      source_coverage: 'complete',
      validation_boundary: 'inventory-read-model-only',
      projection_conformance: {
        schema_version: 'inventory.projection-conformance.config.v1',
        governed_sources: [{ root: 'entries', patterns: ['**/*.md'] }],
        human_indexed_prefixes: ['entries/'],
        uncontrolled_tags: 'warn',
      },
    },
  });
  fs.writeFileSync(
    path.join(root, 'index.md'),
    '# Inventory\n\n## Entries\n\n| Path | Type | Tags | Summary |\n| --- | --- | --- | --- |\n',
  );
  fs.writeFileSync(path.join(root, 'tags.md'), '# Tags\n\n| Tag | Meaning |\n| --- | --- |\n| `inventory` | Test tag. |\n');
  fs.writeFileSync(
    path.join(root, 'entries', 'pending-entry.md'),
    `---\nid: ${mismatch ? 'wrong-id' : 'pending-entry'}\n---\n\n# Pending entry\n`,
  );
  if (extraGap) {
    fs.writeFileSync(
      path.join(root, 'entries', 'unrelated-gap.md'),
      '---\nid: unrelated-gap\n---\n\n# Unrelated gap\n',
    );
  }
  const recordPath = path.join(repository, 'record.json');
  writeJson(recordPath, {
    id: 'pending-entry',
    path: 'entries/pending-entry.md',
    kind: 'entry',
    type: 'synthesis',
    title: 'Pending entry',
    summary: 'A pending source admission fixture.',
    tags: ['inventory'],
    sources: [],
    updated: '2026-08-09',
    status: 'candidate',
    confidence: 'high',
    selectors: [],
    evidence_card_ids: [],
    evidence_set_ids: [],
    residue: ['fixture-only'],
  });
  return { repository, root, recordPath };
}

function runScenario(options) {
  const fixture = createFixture(options);
  try {
    const modulePath = path.join(fixture.root, 'lib', 'inventory-update.cjs');
    delete require.cache[require.resolve(modulePath)];
    const { runAppendDryRun } = require(modulePath);
    const before = {
      index: sha256(path.join(fixture.root, 'index.json')),
      human: sha256(path.join(fixture.root, 'index.md')),
      source: sha256(path.join(fixture.root, 'entries', 'pending-entry.md')),
    };
    const result = runAppendDryRun({
      inventoryRoot: fixture.root,
      recordPath: fixture.recordPath,
      timestampInput: TS,
    });
    const after = {
      index: sha256(path.join(fixture.root, 'index.json')),
      human: sha256(path.join(fixture.root, 'index.md')),
      source: sha256(path.join(fixture.root, 'entries', 'pending-entry.md')),
    };
    assert.deepStrictEqual(after, before, 'dry-run must leave all fixture bytes unchanged');
    return result;
  } finally {
    fs.rmSync(fixture.repository, { recursive: true, force: true });
  }
}

const admitted = runScenario();
assert.strictEqual(admitted.exitCode, 0);
assert.strictEqual(admitted.receipt.status, 'dry-run-ready');
assert.strictEqual(admitted.receipt.baseline.lookup_readiness, 'blocked');
assert.strictEqual(admitted.receipt.baseline.failure_count, 1);
assert.strictEqual(admitted.receipt.candidate.lookup_readiness, 'ready');

const unrelated = runScenario({ extraGap: true });
assert.strictEqual(unrelated.exitCode, 1);
assert.strictEqual(unrelated.receipt.status, 'baseline-blocked');
assert.strictEqual(unrelated.receipt.candidate.evidence_state, 'not-reached');

const mismatch = runScenario({ mismatch: true });
assert.strictEqual(mismatch.exitCode, 1);
assert.strictEqual(mismatch.receipt.status, 'candidate-blocked');
assert.strictEqual(mismatch.receipt.candidate.lookup_readiness, 'blocked');

process.stdout.write('PASS: exact pending source admitted; unrelated baseline and identity mismatch fail closed; dry-run bytes unchanged\n');
