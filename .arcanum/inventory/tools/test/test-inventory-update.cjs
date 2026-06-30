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
 *
 * A failing A/B/C/D is a real falsification of the determinism contract.
 * E is a regression guard (baseline generated from the first correct run).
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const tool = require('../inventory-update.cjs');
const { addRecord, serialize, validate, parseControlledTags } = tool;

const HERE = __dirname;
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

process.stdout.write('\n' + passed + ' assertions-groups passed\n');
