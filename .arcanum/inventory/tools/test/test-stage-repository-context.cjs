#!/usr/bin/env node
'use strict';

const assert = require('node:assert');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const candidateLibrary = path.resolve(process.argv[2] || '');
const candidateValidator = path.resolve(process.argv[3] || '');
const supportInventory = path.resolve(process.argv[4] || '');
if (![candidateLibrary, candidateValidator, supportInventory].every(fs.existsSync)) {
  throw new Error(
    'usage: test-stage-repository-context.cjs <candidate-library> <candidate-validator> <support-inventory>',
  );
}

const TS = '2026-08-09T22:06:00Z';

function digest(filePath) {
  return crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex');
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function entry(id, relativePath) {
  return {
    id,
    path: relativePath,
    kind: 'entry',
    type: 'synthesis',
    title: id,
    summary: `${id} fixture`,
    tags: ['inventory'],
    sources: [],
    updated: '2026-08-09',
    status: 'candidate',
    confidence: 'high',
    selectors: [],
    evidence_card_ids: [],
    evidence_set_ids: [],
    residue: ['fixture-only'],
  };
}

function mapsFor(entries) {
  const maps = {
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
  const arrayFields = {
    by_type: (item) => [item.type],
    by_tag: (item) => item.tags,
    by_source: (item) => item.sources,
    by_status: (item) => [item.status],
    by_evidence_card: (item) => item.evidence_card_ids,
    by_evidence_set: (item) => item.evidence_set_ids,
  };
  for (const item of entries) {
    maps.by_id[item.id] = item.path;
    for (const [mapName, values] of Object.entries(arrayFields)) {
      for (const value of values(item)) {
        if (!maps[mapName][value]) maps[mapName][value] = [];
        maps[mapName][value].push(item.id);
      }
    }
  }
  return maps;
}

function source(pathname, id) {
  fs.mkdirSync(path.dirname(pathname), { recursive: true });
  fs.writeFileSync(pathname, `---\nid: ${id}\n---\n\n# ${id}\n`);
}

function createFixture({ missingExternal = false, escapingPath = false } = {}) {
  const repository = fs.mkdtempSync(path.join(os.tmpdir(), 'inventory-context-fixture-'));
  const inventoryRoot = path.join(repository, '.arcanum', 'inventory');
  const stagingParent = path.join(repository, 'isolated-staging');
  for (const relative of ['lib', 'scripts', 'schemas', 'entries']) {
    fs.mkdirSync(path.join(inventoryRoot, relative), { recursive: true });
  }
  fs.mkdirSync(stagingParent);
  fs.copyFileSync(candidateLibrary, path.join(inventoryRoot, 'lib', 'inventory-update.cjs'));
  fs.copyFileSync(candidateValidator, path.join(inventoryRoot, 'scripts', 'validate_projection_conformance.py'));
  for (const relative of [
    'lib/operation-receipt.cjs',
    'schemas/inventory.operation-receipt.v1.schema.json',
    'scripts/validate-index-json.sh',
  ]) {
    fs.copyFileSync(path.join(supportInventory, relative), path.join(inventoryRoot, relative));
  }

  const externalEntries = [
    entry('ontology-map', '../ontology-vault/map.md'),
    entry('project-source', '../../projects/example.md'),
    entry('skill-source', '../../.claude/skills/test/SKILL.md'),
  ];
  if (escapingPath) externalEntries.push(entry('escape-source', '../../../outside.md'));
  source(path.join(repository, '.arcanum', 'ontology-vault', 'map.md'), 'ontology-map');
  if (!missingExternal) source(path.join(repository, 'projects', 'example.md'), 'project-source');
  source(path.join(repository, '.claude', 'skills', 'test', 'SKILL.md'), 'skill-source');
  source(path.join(inventoryRoot, 'entries', 'pending-entry.md'), 'pending-entry');

  writeJson(path.join(inventoryRoot, 'index.json'), {
    schema_version: 'inventory.index.v0.1',
    inventory_root: '.arcanum/inventory',
    generated_at: '2026-08-09T21:00:00Z',
    human_index: 'index.md',
    entries: externalEntries,
    indexes: mapsFor(externalEntries),
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
    path.join(inventoryRoot, 'index.md'),
    '# Inventory\n\n## Entries\n\n| Path | Type | Tags | Summary |\n| --- | --- | --- | --- |\n',
  );
  fs.writeFileSync(
    path.join(inventoryRoot, 'tags.md'),
    '# Tags\n\n| Tag | Meaning |\n| --- | --- |\n| `inventory` | Test tag. |\n',
  );
  const recordPath = path.join(repository, 'record.json');
  writeJson(recordPath, entry('pending-entry', 'entries/pending-entry.md'));
  return {
    repository,
    inventoryRoot,
    stagingParent,
    recordPath,
    projectSource: path.join(repository, 'projects', 'example.md'),
  };
}

function withFixture(options, callback) {
  const fixture = createFixture(options);
  const previousTmpdir = process.env.TMPDIR;
  process.env.TMPDIR = fixture.stagingParent;
  try {
    const modulePath = path.join(fixture.inventoryRoot, 'lib', 'inventory-update.cjs');
    delete require.cache[require.resolve(modulePath)];
    return callback(fixture, require(modulePath));
  } finally {
    if (previousTmpdir === undefined) delete process.env.TMPDIR;
    else process.env.TMPDIR = previousTmpdir;
    fs.rmSync(fixture.repository, { recursive: true, force: true });
  }
}

withFixture({}, (fixture, tool) => {
  const indexPath = path.join(fixture.inventoryRoot, 'index.json');
  const humanPath = path.join(fixture.inventoryRoot, 'index.md');
  const before = [digest(indexPath), digest(humanPath), digest(fixture.projectSource)];
  const originalCopy = fs.cpSync;
  fs.cpSync = () => { throw new Error('broad copy forbidden'); };
  let result;
  try {
    result = tool.runAppendDryRun({
      inventoryRoot: fixture.inventoryRoot,
      recordPath: fixture.recordPath,
      timestampInput: TS,
    });
  } finally {
    fs.cpSync = originalCopy;
  }
  assert.strictEqual(result.exitCode, 0);
  assert.strictEqual(result.receipt.status, 'dry-run-ready');
  assert.strictEqual(result.receipt.candidate.lookup_readiness, 'ready');
  assert.deepStrictEqual(
    [digest(indexPath), digest(humanPath), digest(fixture.projectSource)],
    before,
  );
  assert.deepStrictEqual(fs.readdirSync(fixture.stagingParent), []);
});

withFixture({ missingExternal: true }, (fixture, tool) => {
  const result = tool.runAppendDryRun({
    inventoryRoot: fixture.inventoryRoot,
    recordPath: fixture.recordPath,
    timestampInput: TS,
  });
  assert.strictEqual(result.exitCode, 1);
  assert.strictEqual(result.receipt.status, 'baseline-blocked');
  assert.deepStrictEqual(fs.readdirSync(fixture.stagingParent), []);
});

withFixture({ escapingPath: true }, (fixture, tool) => {
  const result = tool.runAppendDryRun({
    inventoryRoot: fixture.inventoryRoot,
    recordPath: fixture.recordPath,
    timestampInput: TS,
  });
  assert.strictEqual(result.exitCode, 1);
  assert.strictEqual(result.receipt.status, 'baseline-blocked');
  assert.deepStrictEqual(fs.readdirSync(fixture.stagingParent), []);
});

withFixture({}, (fixture, tool) => {
  const indexPath = path.join(fixture.inventoryRoot, 'index.json');
  const humanPath = path.join(fixture.inventoryRoot, 'index.md');
  const before = [digest(indexPath), digest(humanPath)];
  const result = tool.runAppendApply({
    inventoryRoot: fixture.inventoryRoot,
    recordPath: fixture.recordPath,
    timestampInput: TS,
    hooks: {
      beforeWrite: () => fs.appendFileSync(fixture.projectSource, '\nsource drift\n'),
    },
  });
  assert.strictEqual(result.exitCode, 1);
  assert.strictEqual(result.receipt.status, 'baseline-blocked');
  assert.strictEqual(result.receipt.reason_code, 'baseline-drift-before-write');
  assert.strictEqual(result.receipt.write.attempted, false);
  assert.deepStrictEqual([digest(indexPath), digest(humanPath)], before);
  assert.deepStrictEqual(fs.readdirSync(fixture.stagingParent), []);
});

withFixture({}, (fixture, tool) => {
  const result = tool.runAppendApply({
    inventoryRoot: fixture.inventoryRoot,
    recordPath: fixture.recordPath,
    timestampInput: TS,
  });
  assert.strictEqual(result.exitCode, 0);
  assert.strictEqual(result.receipt.status, 'applied');
  assert.strictEqual(result.receipt.write.committed, true);
  assert.deepStrictEqual(fs.readdirSync(fixture.stagingParent), []);
});

process.stdout.write(
  'PASS: split-root staging validates repository paths, forbids broad copy, fails closed on missing/escape/drift, cleans temp, and preserves dry-run bytes\n',
);
