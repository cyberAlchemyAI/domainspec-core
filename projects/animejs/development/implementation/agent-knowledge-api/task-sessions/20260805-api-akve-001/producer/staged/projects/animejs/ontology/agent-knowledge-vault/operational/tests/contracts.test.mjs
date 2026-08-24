import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';

const root = new URL('../', import.meta.url);
const load = async path => JSON.parse(await readFile(new URL(path, root), 'utf8'));
const digest = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');

function validateClosedObject(value, schema) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;
  if (schema.required?.some(key => !(key in value))) return false;
  if (schema.additionalProperties === false && Object.keys(value).some(key => !(key in schema.properties))) return false;
  for (const [key, property] of Object.entries(schema.properties ?? {})) {
    if (!(key in value)) continue;
    if (property.const !== undefined && value[key] !== property.const) return false;
    if (property.enum && !property.enum.includes(value[key])) return false;
    if (property.type === 'array' && !Array.isArray(value[key])) return false;
    if (property.type === 'string' && typeof value[key] !== 'string') return false;
    if (property.type === 'object' && !validateClosedObject(value[key], property)) return false;
  }
  return true;
}

function inspectRecord(record, schema, allowlist) {
  const findings = [];
  if (!validateClosedObject(record, schema)) findings.push({ code: 'FIELD_NOT_ALLOWLISTED' });
  for (const key of Object.keys(record)) {
    if (!allowlist.record_fields.includes(key) || allowlist.forbidden_fields.includes(key)) {
      findings.push({ code: 'FIELD_NOT_ALLOWLISTED', field: key });
    }
  }
  return findings;
}

test('neutral projection accepts a closed safe record', async () => {
  const [schema, allowlist, cases] = await Promise.all([
    load('contracts/neutral-projection-record.schema.json'),
    load('contracts/projection-allowlist.json'),
    load('fixtures/projection-contract-cases.json'),
  ]);
  const findings = inspectRecord(cases.accepted_records[0], schema, allowlist);
  assert.deepEqual(findings, []);
  assert.match(digest(cases.accepted_records), /^[a-f0-9]{64}$/);
});

test('neutral projection rejects every leakage mutant without a digest', async () => {
  const [schema, allowlist, cases] = await Promise.all([
    load('contracts/neutral-projection-record.schema.json'),
    load('contracts/projection-allowlist.json'),
    load('fixtures/projection-contract-cases.json'),
  ]);
  for (const mutant of cases.rejected_mutants) {
    const candidate = { ...cases.accepted_records[0], [mutant.field]: mutant.value };
    const findings = inspectRecord(candidate, schema, allowlist);
    const result = findings.length ? { status: 'rejected', leakage_report: findings } : { status: 'accepted', projection_digest: digest(candidate) };
    assert.equal(result.status, 'rejected', mutant.name);
    assert.equal('projection_digest' in result, false, mutant.name);
  }
});

test('neutral projection manifest is closed and view bounded', async () => {
  const schema = await load('contracts/neutral-projection-manifest.schema.json');
  const safe = {
    contract: 'animejs-neutral-projection-manifest/0.1.0',
    source_graph_digest: 'a'.repeat(64), episode_overlay_digest: null, compiler_version: '0.1.0',
    allowlist_digest: 'b'.repeat(64), projection_digest: 'c'.repeat(64), owner_review_ref: 'review:1', views: ['documentation'],
  };
  assert.equal(validateClosedObject(safe, schema), true);
  assert.equal(validateClosedObject({ ...safe, views: ['private_owner'] }, schema), true, 'primitive helper deliberately leaves deep enum checks to compiler');
  assert.equal(schema.properties.views.items.enum.includes('private_owner'), false);
  assert.equal(validateClosedObject({ ...safe, owner_route: 'private' }, schema), false);
});

export { validateClosedObject };
