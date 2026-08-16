#!/usr/bin/env node
'use strict';

const assert = require('node:assert');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const sourceModule = path.resolve(process.argv[2] || '');
const supportInventory = path.resolve(process.argv[3] || '');
const sourceIsFile = fs.existsSync(sourceModule) && fs.statSync(sourceModule).isFile();
const supportIsDirectory = (
  fs.existsSync(supportInventory) && fs.statSync(supportInventory).isDirectory()
);
if (!sourceIsFile || !supportIsDirectory) {
  throw new Error('usage: test-relative-root-admission.cjs <inventory-update.cjs> <inventory-root>');
}

const originalRunValidator = `function runValidator(inventoryRoot, indexPath, { sourceInventoryRoot = null } = {}) {
  const validator = path.join(inventoryRoot, 'scripts', 'validate_projection_conformance.py');
  const args = [validator, indexPath, '--json'];
  if (sourceInventoryRoot) {
    args.push('--source-inventory-root', sourceInventoryRoot);
  }
  const result = spawnSync('python3', args, {
    encoding: 'utf8',
    cwd: inventoryRoot,
  });`;

const repairedRunValidator = `function runValidator(inventoryRoot, indexPath, { sourceInventoryRoot = null } = {}) {
  const resolvedInventoryRoot = path.resolve(inventoryRoot);
  const resolvedIndexPath = path.resolve(indexPath);
  const resolvedSourceInventoryRoot = sourceInventoryRoot
    ? path.resolve(sourceInventoryRoot)
    : null;
  const validator = path.join(
    resolvedInventoryRoot,
    'scripts',
    'validate_projection_conformance.py',
  );
  const args = [validator, resolvedIndexPath, '--json'];
  if (resolvedSourceInventoryRoot) {
    args.push('--source-inventory-root', resolvedSourceInventoryRoot);
  }
  const result = spawnSync('python3', args, {
    encoding: 'utf8',
    cwd: resolvedInventoryRoot,
  });`;

const liveSource = fs.readFileSync(sourceModule, 'utf8');
assert.ok(liveSource.includes(originalRunValidator), 'live source no longer matches candidate patch preimage');
const repairedSource = liveSource.replace(originalRunValidator, repairedRunValidator);

function sha256(filePath) {
  return crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex');
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function createFixture(moduleSource) {
  const repository = fs.mkdtempSync(path.join(os.tmpdir(), 'inventory-relative-root-'));
  const inventoryRoot = path.join(repository, '.arcanum', 'inventory');
  for (const relative of ['lib', 'schemas', 'scripts', 'entries']) {
    fs.mkdirSync(path.join(inventoryRoot, relative), { recursive: true });
  }
  fs.writeFileSync(path.join(inventoryRoot, 'lib', 'inventory-update.cjs'), moduleSource);
  for (const relative of [
    'lib/operation-receipt.cjs',
    'schemas/inventory.operation-receipt.v1.schema.json',
    'scripts/validate-index-json.sh',
    'scripts/validate_projection_conformance.py',
  ]) {
    fs.copyFileSync(path.join(supportInventory, relative), path.join(inventoryRoot, relative));
  }
  writeJson(path.join(inventoryRoot, 'index.json'), {
    schema_version: 'inventory.index.v0.1',
    inventory_root: '.arcanum/inventory',
    generated_at: '2026-08-10T19:00:00Z',
    human_index: 'index.md',
    entries: [],
    indexes: {
      by_id: {}, by_type: {}, by_tag: {}, by_source: {}, by_status: {},
      by_evidence_card: {}, by_evidence_set: {}, by_namespace: {},
      by_record_class: {}, by_concept: {},
    },
    projections: [],
    validation: {
      projection_conformance: {
        schema_version: 'inventory.projection-conformance.config.v1',
        governed_sources: [{ root: 'entries', patterns: ['**/*.md'] }],
        human_indexed_prefixes: ['entries/'],
        uncontrolled_tags: 'warn',
      },
    },
  });
  fs.writeFileSync(
    path.join(inventoryRoot, 'index.md'),
    '# Inventory\n\n## Entries\n\n| Path | Type | Tags | Summary |\n| --- | --- | --- | --- |\n',
  );
  fs.writeFileSync(
    path.join(inventoryRoot, 'tags.md'),
    '# Tags\n\n| Tag | Meaning |\n| --- | --- |\n| `inventory` | Fixture. |\n',
  );
  const entryPath = path.join(inventoryRoot, 'entries', 'pending-entry.md');
  fs.writeFileSync(entryPath, '---\nid: pending-entry\n---\n\n# Pending entry\n');
  const recordPath = path.join(repository, 'record.json');
  writeJson(recordPath, {
    id: 'pending-entry',
    path: 'entries/pending-entry.md',
    kind: 'entry',
    type: 'synthesis',
    title: 'Pending entry',
    summary: 'Relative-root regression fixture.',
    tags: ['inventory'],
    sources: [],
    updated: '2026-08-10',
    status: 'candidate',
    confidence: 'high',
    selectors: [],
    evidence_card_ids: [],
    evidence_set_ids: [],
    residue: ['fixture-only'],
  });
  return { repository, inventoryRoot, entryPath, recordPath };
}

function run(moduleSource) {
  const fixture = createFixture(moduleSource);
  const originalCwd = process.cwd();
  try {
    process.chdir(fixture.repository);
    const modulePath = path.join(fixture.inventoryRoot, 'lib', 'inventory-update.cjs');
    delete require.cache[require.resolve(modulePath)];
    const tool = require(modulePath);
    const before = {
      index: sha256(path.join(fixture.inventoryRoot, 'index.json')),
      human: sha256(path.join(fixture.inventoryRoot, 'index.md')),
      entry: sha256(fixture.entryPath),
    };
    const result = tool.runAppendDryRun({
      inventoryRoot: '.arcanum/inventory',
      recordPath: 'record.json',
      timestampInput: '2026-08-10T20:20:00Z',
    });
    const after = {
      index: sha256(path.join(fixture.inventoryRoot, 'index.json')),
      human: sha256(path.join(fixture.inventoryRoot, 'index.md')),
      entry: sha256(fixture.entryPath),
    };
    assert.deepStrictEqual(after, before, 'dry-run must not mutate fixture bytes');
    return result;
  } finally {
    process.chdir(originalCwd);
    fs.rmSync(fixture.repository, { recursive: true, force: true });
  }
}

const beforeRepair = run(liveSource);
assert.strictEqual(beforeRepair.receipt.status, 'baseline-blocked');
assert.strictEqual(beforeRepair.receipt.reason_code, 'baseline-not-ready');
assert.strictEqual(beforeRepair.receipt.baseline.warning_count, 0);

const afterRepair = run(repairedSource);
assert.strictEqual(afterRepair.exitCode, 0);
assert.strictEqual(afterRepair.receipt.status, 'dry-run-ready');
assert.strictEqual(afterRepair.receipt.baseline.failure_count, 1);
assert.strictEqual(afterRepair.receipt.candidate.lookup_readiness, 'ready');

process.stdout.write(
  'PASS: relative-root append reproduces synthetic validator failure before repair and reaches dry-run-ready after path normalization; bytes unchanged\n',
);
