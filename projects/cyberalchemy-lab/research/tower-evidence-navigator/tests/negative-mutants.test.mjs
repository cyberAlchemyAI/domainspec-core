import assert from 'node:assert/strict';
import { mkdtemp, readFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { compileToFile } from '../tools/compile-projection.mjs';

const root = new URL('../', import.meta.url);
const fixture = await readFile(new URL('fixtures/valid/synthetic-one-tower.json', root), 'utf8').then(JSON.parse);
const matrix = await readFile(new URL('fixtures/invalid/mutant-matrix.json', root), 'utf8').then(JSON.parse);
const clone = () => structuredClone(fixture);

function mutate(value, mutation) {
  switch (mutation) {
    case 'source_digest': value.source_snapshots[0].content_digest = '0'.repeat(64); break;
    case 'selector': value.evidence_anchors[0].selector.end_byte_exclusive = 999; break;
    case 'identity': value.source_snapshots[1].logical_source_id = value.source_snapshots[0].logical_source_id; break;
    case 'tower_snapshot': [value.tower_package_snapshot.ordered_artifacts[0], value.tower_package_snapshot.ordered_artifacts[1]] = [value.tower_package_snapshot.ordered_artifacts[1], value.tower_package_snapshot.ordered_artifacts[0]]; break;
    case 'relation': value.relations[0].to_id = 'missing:record'; break;
    case 'kind': value.relations[0].kind = 'same_as'; break;
    case 'privacy': value.ontology_candidates[0].private_content = 'PRIVATE-CONTENT'; break;
    case 'projection': value.expected_projection_revision = '0'.repeat(64); break;
    case 'validation': value.validation_records = [{ result: 'pass' }]; break;
    case 'residue': value.residue_items[0].status = 'cleared'; break;
    case 'authority': value.promotion_records[0].gate_result = 'allow'; break;
    case 'transport': value.reserved_consumer_contract = { transport: 'POST' }; break;
    case 'allowlist': value.tower_logical_id = 'tower:not-allowed'; break;
    case 'manifest': value.package_snapshot_check = 'stale'; break;
    case 'independent_validator': value.validation_records = [{ validator_id: 'cal-projection-compiler-v1', exact_inputs: { fixture: 'locked' }, result: 'pass' }]; break;
    default: throw new Error(`unknown mutation ${mutation}`);
  }
}

test('M01 through M15 fail closed without replacing a prior projection', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'cal-mutants-'));
  const output = join(directory, 'projection.json');
  await compileToFile({ input: new URL('fixtures/valid/synthetic-one-tower.json', root), output, sourceRoot: new URL('.', root).pathname });
  const baseline = await readFile(output);
  for (const mutant of matrix.mutants) {
    const input = join(directory, `${mutant.id}.json`);
    const value = clone();
    mutate(value, mutant.mutation);
    await (await import('node:fs/promises')).writeFile(input, JSON.stringify(value));
    await assert.rejects(() => compileToFile({ input, output, sourceRoot: new URL('.', root).pathname }), (error) => error.code === mutant.expected_code);
    assert.deepEqual(await readFile(output), baseline, `${mutant.id} replaced output`);
  }
});
