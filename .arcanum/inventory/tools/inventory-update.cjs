#!/usr/bin/env node
'use strict';

/*
 * inventory-update — deterministic inventory record appender.
 *
 * Appends ONE record to .arcanum/inventory/index.json and updates all index
 * maps consistently. Built for SWU-1 of refine run 20260629T0700Z-inventory-js-updater.
 *
 * Determinism contract (the whole point):
 *   1. The timestamp is an INPUT, never wall-clock. No Date.now()/new Date().
 *      Same (index, record, timestamp) -> byte-identical output.
 *   2. Append-only map updates. Existing keys/arrays are never reordered; an id
 *      is appended (deduped) to each array map; a brand-new key is created at the
 *      end (insertion order). by_id[id] = path (string).
 *   3. Idempotent. If record.id already exists, this is a NO-OP: the index is
 *      returned unchanged (generated_at is NOT bumped), so re-running yields
 *      byte-identical output. (--replace is deferred to a follow-up SWU.)
 *   4. Canonical serialization: JSON.stringify(out, null, 2) + "\n".
 *
 * Scope (SWU-1): owns index.json only. The index.md row sync is SWU-2; the
 * by_evidence_set migration of legacy keys is SWU-3. Both deferred.
 */

const fs = require('fs');
const path = require('path');

// The seven index maps. by_id is a string map; the rest are array maps.
const ARRAY_MAP_SOURCES = [
  ['by_type', (e) => [e.type]],
  ['by_status', (e) => [e.status]],
  ['by_tag', (e) => e.tags],
  ['by_source', (e) => e.sources],
  ['by_evidence_card', (e) => e.evidence_card_ids],
  ['by_evidence_set', (e) => e.evidence_set_ids],
];
const ALL_MAP_NAMES = ['by_id', ...ARRAY_MAP_SOURCES.map(([n]) => n)];

// Canonical entry field order — matches the existing index.json entry shape.
// New entries are normalized to this order so output formatting is stable
// regardless of the input record's key order.
const ENTRY_FIELDS = [
  'id', 'path', 'kind', 'type', 'title', 'summary', 'tags', 'sources',
  'updated', 'status', 'confidence', 'selectors', 'evidence_card_ids',
  'evidence_set_ids', 'residue',
];

function isNonEmptyString(v) {
  return typeof v === 'string' && v.length > 0;
}

function clone(obj) {
  // Deterministic deep clone; preserves key insertion order.
  return JSON.parse(JSON.stringify(obj));
}

function asArray(v) {
  if (v === undefined || v === null) return [];
  if (!Array.isArray(v)) {
    throw new Error('expected an array but got ' + JSON.stringify(v));
  }
  return v;
}

// Build a canonical entry from an input record. Missing arrays default to [];
// missing scalars get conservative defaults. `updated` falls back to the date
// portion of the (input) timestamp, so it stays deterministic.
function normalizeEntry(record, timestamp) {
  if (!record || typeof record !== 'object') {
    throw new Error('record must be an object');
  }
  if (!isNonEmptyString(record.id)) throw new Error('record.id is required');
  if (!isNonEmptyString(record.path)) throw new Error('record.path is required');
  if (!isNonEmptyString(record.kind)) throw new Error('record.kind is required');
  if (!isNonEmptyString(record.type)) throw new Error('record.type is required');

  const entry = {
    id: record.id,
    path: record.path,
    kind: record.kind,
    type: record.type,
    title: isNonEmptyString(record.title) ? record.title : record.path,
    summary: typeof record.summary === 'string' ? record.summary : '',
    tags: asArray(record.tags),
    sources: asArray(record.sources),
    updated: isNonEmptyString(record.updated) ? record.updated : timestamp.slice(0, 10),
    status: isNonEmptyString(record.status) ? record.status : 'candidate',
    confidence: isNonEmptyString(record.confidence) ? record.confidence : 'unknown',
    selectors: asArray(record.selectors),
    evidence_card_ids: asArray(record.evidence_card_ids),
    evidence_set_ids: asArray(record.evidence_set_ids),
    residue: asArray(record.residue),
  };
  // Re-emit in canonical field order (defensive; object above is already ordered).
  const ordered = {};
  for (const f of ENTRY_FIELDS) ordered[f] = entry[f];
  return ordered;
}

function ensureMaps(index) {
  index.entries = index.entries || [];
  index.indexes = index.indexes || {};
  for (const name of ALL_MAP_NAMES) {
    if (!index.indexes[name]) index.indexes[name] = {};
  }
}

function appendToArrayMap(map, key, id) {
  if (!Object.prototype.hasOwnProperty.call(map, key)) map[key] = [];
  if (!map[key].includes(id)) map[key].push(id); // dedup, no reorder
}

/*
 * addRecord — pure: returns a NEW index object, never mutates the input.
 * Returns { index, changed, reason, entry }.
 *   - existing id  -> { changed: false, reason: 'already-present' } (no-op)
 *   - new id       -> { changed: true,  reason: 'added' }
 */
function addRecord(indexObj, record, timestamp, opts) {
  opts = opts || {};
  if (!isNonEmptyString(timestamp)) {
    throw new Error('timestamp (ISO-8601 string) is required — no wall-clock is used');
  }
  const out = clone(indexObj);
  ensureMaps(out);
  const entry = normalizeEntry(record, timestamp);

  if (Object.prototype.hasOwnProperty.call(out.indexes.by_id, entry.id)) {
    // Idempotent no-op. Do not bump generated_at -> output === input bytes.
    return { index: out, changed: false, reason: 'already-present', entry };
  }

  out.entries.push(entry);
  out.indexes.by_id[entry.id] = entry.path;
  for (const [mapName, pick] of ARRAY_MAP_SOURCES) {
    for (const key of asArray(pick(entry))) {
      appendToArrayMap(out.indexes[mapName], key, entry.id);
    }
  }
  out.generated_at = timestamp;
  return { index: out, changed: true, reason: 'added', entry };
}

function serialize(indexObj) {
  return JSON.stringify(indexObj, null, 2) + '\n';
}

// ---- validation (read-model self-check; tag mismatches WARN, not block) ----

function parseControlledTags(tagsMdPath) {
  const set = new Set();
  let text;
  try {
    text = fs.readFileSync(tagsMdPath, 'utf8');
  } catch (_e) {
    return set; // tags.md absent -> empty controlled set -> all tags "unknown" (warn only)
  }
  const re = /^\|\s*`([^`]+)`\s*\|/gm;
  let m;
  while ((m = re.exec(text)) !== null) set.add(m[1]);
  return set;
}

function validate(indexObj, controlledTags) {
  const errors = [];
  const warnings = [];
  const entries = indexObj.entries || [];

  const ids = entries.map((e) => e.id);
  const seen = new Set();
  for (const id of ids) {
    if (seen.has(id)) errors.push('duplicate entry id: ' + id);
    seen.add(id);
  }

  const byId = (indexObj.indexes && indexObj.indexes.by_id) || {};
  for (const e of entries) {
    if (byId[e.id] !== e.path) {
      errors.push('by_id mismatch for ' + e.id + ' (expected ' + e.path + ', got ' + byId[e.id] + ')');
    }
  }

  if (!isNonEmptyString(indexObj.generated_at)) errors.push('generated_at missing');

  if (controlledTags && controlledTags.size > 0) {
    const known = new Set();
    for (const e of entries) {
      for (const t of e.tags || []) {
        if (!controlledTags.has(t) && !known.has(t)) {
          warnings.push('tag not in tags.md controlled set: ' + t);
          known.add(t);
        }
      }
    }
  }

  return { ok: errors.length === 0, errors, warnings };
}

// ------------------------- index.md row sync (SWU-2) -------------------------
//
// Routing is by PATH PREFIX, not kind: the data proves `kind` is ambiguous
// (kind:page spans wiki/, entries/, and ../). Every row in the `## Entries`
// table is an entries/ path, so prefix is the reliable signal. External paths
// (../, raw/, ../../) were human-placed with no deterministic rule -> skip+warn.

const MD_TABLES = [
  { prefix: 'entries/', header: '## Entries' },
  { prefix: 'wiki/', header: '## Wiki Pages' },
  { prefix: 'queries/', header: '## Query Files' },
  { prefix: 'lint/', header: '## Lint Files' },
];

function tableForPath(p) {
  for (const t of MD_TABLES) {
    if (typeof p === 'string' && p.startsWith(t.prefix)) return t;
  }
  return null;
}

// Make a string safe inside a Markdown table cell: collapse newlines, escape `|`.
function mdCell(s) {
  return String(s === undefined || s === null ? '' : s)
    .replace(/\r?\n/g, ' ')
    .replace(/\|/g, '\\|')
    .trim();
}

function mdRowFor(entry) {
  const tags = (entry.tags || []).map((t) => '`' + mdCell(t) + '`').join(', ');
  return '| [' + entry.path + '](' + entry.path + ') | ' + mdCell(entry.type) + ' | ' + tags + ' | ' + mdCell(entry.summary) + ' |';
}

/*
 * addIndexMdRow — pure: append the entry's row to the matching index.md table.
 * Returns { md, changed, reason, table }.
 *   - no matching prefix          -> no-op, reason 'no-table-for-path' (caller warns)
 *   - table/separator not found   -> no-op, reason 'table-...-not-found'
 *   - link already in that table  -> no-op, reason 'row-already-present' (idempotent)
 *   - otherwise                   -> row appended at end of the table block
 */
function addIndexMdRow(mdText, entry) {
  const table = tableForPath(entry.path);
  if (!table) return { md: mdText, changed: false, reason: 'no-table-for-path', table: null };

  const lines = mdText.split('\n');
  const hi = lines.findIndex((l) => l.trim() === table.header);
  if (hi === -1) return { md: mdText, changed: false, reason: 'table-header-not-found', table: table.header };

  let si = -1;
  for (let i = hi + 1; i < lines.length; i++) {
    if (/^\|\s*-+/.test(lines[i])) { si = i; break; }
    if (/^## /.test(lines[i])) break; // next section, no table here
  }
  if (si === -1) return { md: mdText, changed: false, reason: 'table-separator-not-found', table: table.header };

  let last = si;
  for (let i = si + 1; i < lines.length; i++) {
    if (lines[i].startsWith('|')) last = i;
    else break;
  }

  const link = '[' + entry.path + '](' + entry.path + ')';
  for (let i = si + 1; i <= last; i++) {
    if (lines[i].includes(link)) return { md: mdText, changed: false, reason: 'row-already-present', table: table.header };
  }

  lines.splice(last + 1, 0, mdRowFor(entry));
  return { md: lines.join('\n'), changed: true, reason: 'row-added', table: table.header };
}

// ---------------------------------- CLI ----------------------------------

function parseArgs(argv) {
  const out = { _: [], replace: false, dryRun: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--timestamp') out.timestamp = argv[++i];
    else if (a === '--index') out.index = argv[++i];
    else if (a === '--dry-run') out.dryRun = true;
    else if (a === '--replace') out.replace = true;
    else out._.push(a);
  }
  return out;
}

function resolveIndexFile(indexArg) {
  // --index may be a dir (containing index.json) or the file itself.
  const base = indexArg
    ? path.resolve(indexArg)
    : path.resolve(__dirname, '..'); // default: inventory root (tools/..)
  if (fs.existsSync(base) && fs.statSync(base).isDirectory()) {
    return path.join(base, 'index.json');
  }
  return base;
}

function main(argv) {
  const args = parseArgs(argv);
  const cmd = args._[0];

  if (cmd !== 'add') {
    process.stderr.write(
      'usage: node inventory-update.cjs add <record.json> --timestamp <iso8601> [--index <dir|file>] [--dry-run]\n'
    );
    return 2;
  }
  if (args.replace) {
    process.stderr.write('error: --replace is not implemented in this MVP (deferred SWU)\n');
    return 2;
  }
  const recordPath = args._[1];
  if (!isNonEmptyString(recordPath)) {
    process.stderr.write('error: missing <record.json>\n');
    return 2;
  }
  if (!isNonEmptyString(args.timestamp)) {
    process.stderr.write('error: --timestamp <iso8601> is required (no wall-clock is used)\n');
    return 2;
  }

  const indexFile = resolveIndexFile(args.index);
  const indexObj = JSON.parse(fs.readFileSync(indexFile, 'utf8'));
  const record = JSON.parse(fs.readFileSync(path.resolve(recordPath), 'utf8'));

  const result = addRecord(indexObj, record, args.timestamp);

  // index.md row sync (SWU-2): runs on a json change, and as an idempotent
  // repair when json is a no-op but the md row is missing. Additive only.
  const mdFile = path.join(path.dirname(indexFile), 'index.md');
  let mdResult = { changed: false, reason: 'index.md-not-found', table: null };
  if (fs.existsSync(mdFile)) {
    mdResult = addIndexMdRow(fs.readFileSync(mdFile, 'utf8'), result.entry);
  }
  if (mdResult.reason === 'no-table-for-path') {
    process.stderr.write('warn: no index.md table for path ' + result.entry.path + ' (json updated; add the md row manually)\n');
  } else if (mdResult.reason !== 'index.md-not-found' && /not-found/.test(mdResult.reason)) {
    process.stderr.write('warn: index.md ' + mdResult.reason + ' for ' + (mdResult.table || '?') + ' (md row skipped)\n');
  }

  // Validate the json result before any write.
  if (result.changed) {
    const controlled = parseControlledTags(path.join(path.dirname(indexFile), 'tags.md'));
    const report = validate(result.index, controlled);
    for (const w of report.warnings) process.stderr.write('warn: ' + w + '\n');
    if (!report.ok) {
      for (const e of report.errors) process.stderr.write('error: ' + e + '\n');
      process.stderr.write('aborted: validation failed, nothing written\n');
      return 1;
    }
  }

  if (args.dryRun) {
    process.stdout.write('[dry-run] json: ' + (result.changed ? 'add ' + result.entry.id + ' (entries -> ' + result.index.entries.length + ')' : 'no-op (' + result.reason + ')') + '\n');
    process.stdout.write('[dry-run] index.md: ' + (mdResult.changed ? 'add row to ' + mdResult.table : 'no-op (' + mdResult.reason + ')') + '\n');
    return 0;
  }

  if (result.changed) fs.writeFileSync(indexFile, serialize(result.index));
  if (mdResult.changed) fs.writeFileSync(mdFile, mdResult.md);

  if (!result.changed && !mdResult.changed) {
    process.stdout.write('no-op: ' + result.entry.id + ' already present (json + index.md)\n');
  } else {
    process.stdout.write(
      'updated: ' + result.entry.id +
      ' [json: ' + (result.changed ? 'added' : 'no-op') +
      ', index.md: ' + (mdResult.changed ? mdResult.table : 'no-op') + ']\n'
    );
  }
  return 0;
}

module.exports = {
  addRecord,
  normalizeEntry,
  serialize,
  validate,
  parseControlledTags,
  addIndexMdRow,
  tableForPath,
  mdRowFor,
  ENTRY_FIELDS,
  ALL_MAP_NAMES,
};

if (require.main === module) {
  process.exit(main(process.argv.slice(2)));
}
