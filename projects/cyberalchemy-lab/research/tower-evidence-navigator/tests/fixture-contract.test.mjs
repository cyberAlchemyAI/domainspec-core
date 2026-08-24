import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { test } from 'node:test';

const root = new URL('../', import.meta.url);
const fixture = await readFile(new URL('fixtures/valid/synthetic-one-tower.json', root), 'utf8').then(JSON.parse);
const sha256 = (value) => createHash('sha256').update(value).digest('hex');

test('synthetic fixture closes the declared L0 record cardinality', () => {
  assert.equal(fixture.tower_package_snapshot.kind, 'TowerPackageSnapshot');
  assert.equal(fixture.source_snapshots.length, 7);
  assert.equal(fixture.claims.length, 1);
  assert.equal(fixture.definition_references.length, 1);
  assert.equal(fixture.residue_items.length, 1);
  assert.equal(fixture.evidence_anchors.length, 2);
  assert.equal(fixture.ontology_candidates.length, 1);
  assert.equal(fixture.promotion_records.length, 1);
  assert.equal(fixture.promotion_records[0].gate_result, 'block');
  assert.equal(fixture.residue_items[0].status, 'open');
});

test('source and byte-range evidence bindings are exact', async () => {
  for (const source of fixture.source_snapshots) {
    const bytes = await readFile(new URL(source.locator, root));
    assert.equal(sha256(bytes), source.content_digest, source.id);
    assert.equal(bytes.length, source.byte_size, source.id);
  }
  for (const anchor of fixture.evidence_anchors) {
    const source = fixture.source_snapshots.find((item) => item.id === anchor.source_snapshot_id);
    const bytes = await readFile(new URL(source.locator, root));
    const selected = bytes.subarray(anchor.selector.start_byte, anchor.selector.end_byte_exclusive);
    assert.equal(sha256(selected), anchor.selected_bytes_sha256, anchor.id);
  }
});

test('fixture retains logical source identity and a closed relation vocabulary', () => {
  assert.equal(new Set(fixture.source_snapshots.map((item) => item.logical_source_id)).size, 7);
  assert.equal(fixture.relations.some((item) => item.kind === 'same_as'), false);
  assert.equal(fixture.relations.every((item) => item.authority_effect === 'none'), true);
});
