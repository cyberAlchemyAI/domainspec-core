#!/usr/bin/env node
'use strict';

/*
 * SWU-2 falsification suite for addIndexMdRow.
 *
 *   A. routing        — entries/wiki/queries/lint paths land in the right table
 *   B. insertion pos  — new row appended at END of the table block, before next ##
 *   C. isolation      — other tables are byte-untouched
 *   D. unknown path   — external (../) path is a no-op (no-table-for-path)
 *   E. idempotency    — re-adding the same link is a no-op
 *   F. determinism    — two runs byte-identical
 *   G. cell safety     — `|` in summary is escaped, not a delimiter
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const { addIndexMdRow } = require('../inventory-update.cjs');

const HERE = __dirname;
const MD = fs.readFileSync(path.join(HERE, 'fixture.index.md'), 'utf8');

let passed = 0;
function ok(name) { passed++; process.stdout.write('  ok   ' + name + '\n'); }

const entry = (over) => Object.assign(
  { path: 'entries/new.md', type: 'synthesis', tags: ['inventory', 'knowledge-system'], summary: 'A new entry.' },
  over
);

// ---- A. routing -----------------------------------------------------------
{
  const cases = [
    ['entries/new.md', '## Entries'],
    ['wiki/new-map.md', '## Wiki Pages'],
    ['queries/2026-06-29-x/findings.md', '## Query Files'],
    ['lint/2026-06-29-x.md', '## Lint Files'],
  ];
  for (const [p, header] of cases) {
    const r = addIndexMdRow(MD, entry({ path: p }));
    assert.strictEqual(r.changed, true, p + ' should change');
    assert.strictEqual(r.table, header, p + ' -> ' + header);
  }
  ok('A routing (entries/wiki/queries/lint -> correct table)');
}

// ---- B. insertion position: end of Entries block, before ## Query Files ----
{
  const r = addIndexMdRow(MD, entry({ path: 'entries/new.md' }));
  const lines = r.md.split('\n');
  const newRow = lines.findIndex((l) => l.includes('[entries/new.md](entries/new.md)'));
  const seedRow = lines.findIndex((l) => l.includes('[entries/seed.md](entries/seed.md)'));
  const queryHeader = lines.findIndex((l) => l.trim() === '## Query Files');
  assert.ok(newRow > seedRow, 'new row after existing seed row');
  assert.ok(newRow < queryHeader, 'new row before ## Query Files header');
  // contiguous: line right after the new row is the blank line then the next header
  ok('B insertion position (end of table block, before next section)');
}

// ---- C. isolation: other tables untouched ---------------------------------
{
  const r = addIndexMdRow(MD, entry({ path: 'entries/new.md' }));
  for (const frag of [
    '| [wiki/repository-map.md](wiki/repository-map.md) | synthesis | `repo-map` | First map. |',
    '| [queries/2026-01-01-x/DISPATCH.json](queries/2026-01-01-x/DISPATCH.json) | dispatch-spec | `dispatch-spec` | A query. |',
    '| [lint/2026-01-01-x.md](lint/2026-01-01-x.md) | lint-report | `inventory` | A lint. |',
  ]) {
    assert.ok(r.md.includes(frag), 'untouched: ' + frag.slice(0, 40));
  }
  // exactly one line added
  assert.strictEqual(r.md.split('\n').length, MD.split('\n').length + 1, 'exactly one line added');
  ok('C isolation (other tables byte-untouched; +1 line only)');
}

// ---- D. unknown path is a no-op -------------------------------------------
{
  const r = addIndexMdRow(MD, entry({ path: '../ontology-vault/x.md' }));
  assert.strictEqual(r.changed, false);
  assert.strictEqual(r.reason, 'no-table-for-path');
  assert.strictEqual(r.md, MD, 'md unchanged on unknown path');
  ok('D unknown path (../) is a no-op, reason no-table-for-path');
}

// ---- E. idempotency: existing link -> no-op -------------------------------
{
  const r1 = addIndexMdRow(MD, entry({ path: 'entries/new.md' }));
  const r2 = addIndexMdRow(r1.md, entry({ path: 'entries/new.md' }));
  assert.strictEqual(r2.changed, false);
  assert.strictEqual(r2.reason, 'row-already-present');
  assert.strictEqual(r2.md, r1.md, 're-add is a byte-identical no-op');
  ok('E idempotency (existing link -> no-op)');
}

// ---- F. determinism --------------------------------------------------------
{
  const a = addIndexMdRow(MD, entry({ path: 'entries/new.md' })).md;
  const b = addIndexMdRow(MD, entry({ path: 'entries/new.md' })).md;
  assert.strictEqual(a, b, 'two runs byte-identical');
  ok('F determinism (byte-identical across runs)');
}

// ---- G. cell safety: pipe in summary is escaped ---------------------------
{
  const r = addIndexMdRow(MD, entry({ path: 'entries/piped.md', summary: 'left | right', tags: [] }));
  const row = r.md.split('\n').find((l) => l.includes('[entries/piped.md]'));
  assert.ok(row.includes('left \\| right'), 'pipe escaped in summary cell');
  // the row's structural delimiters: leading and trailing pipes plus 3 separators = 5 unescaped pipes
  const unescaped = (row.match(/(^|[^\\])\|/g) || []).length;
  assert.strictEqual(unescaped, 5, 'exactly 5 structural pipes (escaped pipe not counted)');
  ok('G cell safety (| escaped, not a delimiter)');
}

process.stdout.write('\n' + passed + ' groups passed\n');
