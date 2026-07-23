#!/usr/bin/env node
'use strict';

/*
 * toy_game falsification suite for inventory-update.cjs.
 *
 * The core promise is DETERMINISM. These tests are built to FALSIFY it:
 *   A. reproducibility  — two independent runs produce byte-identical output
 *   B. idempotency      — re-applying the same record is a byte-identical no-op
 *   C. known deltas     — exactly the expected map/entry changes, nothing else
 *   D. validity         — output round-trips through JSON.parse, ids unique
 *   E. golden snapshot  — output matches a committed regression baseline
 *   F. determinism input— omitting the timestamp throws (no wall-clock fallback)
 *   G. supported kinds  — entry/query inputs remain accepted and idempotent
 *   H. producer guard   — unsupported kind rejects without pure-input mutation
 *   I. CLI write safety — rejection changes neither JSON nor Markdown
 *
 * A failing A/B/C/D is a real falsification of the determinism contract.
 * E is a regression guard (baseline generated from the first correct run).
 */

const assert = require('assert');
const childProcess = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const tool = require('../inventory-update.cjs');
const {
  addRecord,
  serialize,
  validate,
  parseControlledTags,
  SUPPORTED_KINDS,
} = tool;

const HERE = __dirname;
const TOOL_PATH = path.join(HERE, '..', 'inventory-update.cjs');
const TS = '2026-06-29T12:00:00Z';
const fixture = JSON.parse(fs.readFileSync(path.join(HERE, 'fixture.index.json'), 'utf8'));
const record = JSON.parse(fs.readFileSync(path.join(HERE, 'record.sample.json'), 'utf8'));

let passed = 0;
function ok(name) { passed++; process.stdout.write('  ok   ' + name + '\n'); }

// ---- A. reproducibility: two independent runs are byte-identical ----------
{
  const a = serialize(addRecord(fixture, record, TS).index);
  const b = serialize(addRecord(fixture, record, TS).index);
  assert.strictEqual(a, b, 'two independent runs must be byte-identical');
  // and the input must not have been mutated
  assert.strictEqual(fixture.entries.length, 1, 'addRecord must not mutate its input');
  ok('A reproducibility (byte-identical across runs; input not mutated)');
}

// ---- B. idempotency: re-applying the same record is a no-op ----------------
{
  const r1 = addRecord(fixture, record, TS);
  const r2 = addRecord(r1.index, record, TS);
  assert.strictEqual(r2.changed, false, 're-apply must report changed=false');
  assert.strictEqual(r2.reason, 'already-present');
  assert.strictEqual(
    serialize(r2.index), serialize(r1.index),
    're-apply must be a byte-identical no-op (generated_at not bumped)'
  );
  assert.strictEqual(r2.index.entries.length, r1.index.entries.length, 'no duplicate entry push');
  ok('B idempotency (re-apply is a byte-identical no-op)');
}

// ---- C. known deltas: exactly the expected changes -------------------------
{
  const { index: idx } = addRecord(fixture, record, TS);
  const ix = idx.indexes;
  assert.strictEqual(idx.entries.length, fixture.entries.length + 1, 'entries +1');
  assert.strictEqual(idx.generated_at, TS, 'generated_at = passed timestamp');
  assert.strictEqual(ix.by_id['new-synthesis'], 'entries/new-synthesis.md', 'by_id = path string');
  assert.deepStrictEqual(ix.by_type['synthesis'], ['new-synthesis'], 'by_type new key');
  assert.deepStrictEqual(ix.by_type['concept'], ['seed-entry'], 'by_type existing key untouched');
  assert.deepStrictEqual(ix.by_tag['inventory'], ['seed-entry', 'new-synthesis'], 'by_tag append, no reorder');
  assert.deepStrictEqual(ix.by_tag['knowledge-system'], ['new-synthesis'], 'by_tag new key');
  assert.deepStrictEqual(ix.by_source['raw/example.md#h1'], ['new-synthesis'], 'by_source new key');
  assert.deepStrictEqual(ix.by_status['candidate'], ['seed-entry', 'new-synthesis'], 'by_status append');
  assert.deepStrictEqual(ix.by_evidence_card['card-x'], ['new-synthesis'], 'by_evidence_card new key (array)');
  // normalized new write: set-id -> [entry-id] (array), mirroring by_evidence_card
  assert.deepStrictEqual(ix.by_evidence_set['evset-new'], ['new-synthesis'], 'by_evidence_set normalized array form');
  // legacy old-form key is preserved untouched (migration is a separate SWU)
  assert.strictEqual(ix.by_evidence_set['old-form-set'], 'old-form-set', 'legacy by_evidence_set key preserved');
  ok('C known deltas (7 maps + entries + generated_at; legacy key preserved)');
}

// ---- D. validity: round-trips, ids unique ----------------------------------
{
  const { index: idx } = addRecord(fixture, record, TS);
  const out = serialize(idx);
  const reparsed = JSON.parse(out); // throws if not valid JSON
  const ids = reparsed.entries.map((e) => e.id);
  assert.strictEqual(new Set(ids).size, ids.length, 'entry ids unique');
  const report = validate(idx, parseControlledTags(path.join(HERE, '..', '..', 'tags.md')));
  assert.strictEqual(report.ok, true, 'validate() reports ok: ' + JSON.stringify(report.errors));
  ok('D validity (JSON round-trip, unique ids, validate ok)');
}

// ---- E. golden snapshot regression guard -----------------------------------
{
  const out = serialize(addRecord(fixture, record, TS).index);
  const goldenPath = path.join(HERE, 'expected.index.json');
  if (!fs.existsSync(goldenPath)) {
    fs.writeFileSync(goldenPath, out);
    process.stdout.write('  note SNAPSHOT CREATED (regression baseline) -> expected.index.json\n');
  } else {
    const golden = fs.readFileSync(goldenPath, 'utf8');
    assert.strictEqual(out, golden, 'output drifted from committed golden snapshot');
    ok('E golden snapshot (byte-identical to committed baseline)');
  }
}

// ---- F. timestamp is required (no wall-clock fallback) ----------------------
{
  assert.throws(() => addRecord(fixture, record, undefined), /timestamp.*required/i, 'missing timestamp must throw');
  assert.throws(() => addRecord(fixture, record, ''), /timestamp.*required/i, 'empty timestamp must throw');
  ok('F determinism input (missing/empty timestamp throws)');
}

// ---- G. supported entry/query controls remain accepted and idempotent -------
{
  assert.deepStrictEqual(
    SUPPORTED_KINDS,
    [
      'page',
      'entry',
      'query',
      'lint',
      'raw-manifest',
      'evidence-card-bundle',
      'evidence-set-bundle',
    ],
    'producer enum must match the canonical Inventory validator'
  );
  for (const kind of ['entry', 'query']) {
    const supported = {
      ...record,
      id: 'supported-' + kind,
      path: (kind === 'entry' ? 'entries/' : 'queries/') + 'supported-' + kind + '.md',
      kind,
    };
    const first = addRecord(fixture, supported, TS);
    assert.strictEqual(first.changed, true, kind + ' must be admitted');
    assert.strictEqual(first.entry.kind, kind);
    const second = addRecord(first.index, supported, TS);
    assert.strictEqual(second.changed, false, kind + ' re-apply must be a no-op');
    assert.strictEqual(
      serialize(second.index),
      serialize(first.index),
      kind + ' re-apply must be byte-identical'
    );
  }
  ok('G supported entry/query controls (admitted and idempotent)');
}

// ---- H. unsupported kind rejects before the pure input can change -----------
{
  const before = serialize(fixture);
  const unsupported = {
    ...record,
    id: 'unsupported-strategy-result',
    path: 'entries/unsupported-strategy-result.md',
    kind: 'strategy-result',
  };
  assert.throws(
    () => addRecord(fixture, unsupported, TS),
    /record\.kind must be one of/,
    'unsupported kind must reject at producer admission'
  );
  assert.strictEqual(
    serialize(fixture),
    before,
    'unsupported kind must not mutate the pure input'
  );
  ok('H unsupported kind admission (rejects before pure mutation)');
}

// ---- I. real CLI rejection leaves both projections byte-identical -----------
{
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'inventory-kind-guard-'));
  try {
    const indexPath = path.join(tempRoot, 'index.json');
    const mdPath = path.join(tempRoot, 'index.md');
    const tagsPath = path.join(tempRoot, 'tags.md');
    const recordPath = path.join(tempRoot, 'unsupported.json');
    const indexBytes = fs.readFileSync(path.join(HERE, 'fixture.index.json'));
    const mdBytes = fs.readFileSync(path.join(HERE, 'fixture.index.md'));
    fs.writeFileSync(indexPath, indexBytes);
    fs.writeFileSync(mdPath, mdBytes);
    fs.writeFileSync(tagsPath, '# Tags\n');
    fs.writeFileSync(
      recordPath,
      JSON.stringify(
        {
          ...record,
          id: 'unsupported-cli',
          path: 'entries/unsupported-cli.md',
          kind: 'strategy-result',
        },
        null,
        2
      ) + '\n'
    );

    const run = childProcess.spawnSync(
      process.execPath,
      [
        TOOL_PATH,
        'add',
        recordPath,
        '--timestamp',
        TS,
        '--index',
        tempRoot,
      ],
      { encoding: 'utf8' }
    );
    assert.notStrictEqual(run.status, 0, 'unsupported CLI input must exit non-zero');
    assert.match(run.stderr, /record\.kind must be one of/);
    assert.match(run.stderr, /nothing written/);
    assert.deepStrictEqual(
      fs.readFileSync(indexPath),
      indexBytes,
      'index.json must remain byte-identical'
    );
    assert.deepStrictEqual(
      fs.readFileSync(mdPath),
      mdBytes,
      'index.md must remain byte-identical'
    );
  } finally {
    fs.rmSync(tempRoot, { recursive: true, force: true });
  }
  ok('I CLI write safety (unsupported kind changes no projection)');
}

process.stdout.write('\n' + passed + ' assertions-groups passed\n');
