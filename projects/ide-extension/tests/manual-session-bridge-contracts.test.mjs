import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { bridgeGrants, defaultGrants, normalizeL0Grants } from '../src/kernel/grants.mjs';
import { validateSchema } from '../src/kernel/schema-validation.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const fixtureDir = path.join(projectRoot, 'tests/fixtures/schemas');

async function fixture(name) {
  return JSON.parse(await readFile(path.join(fixtureDir, name), 'utf8'));
}

test('preserves legacy envelope, receipt, and dry-run grants', async () => {
  assert.deepEqual(
    await validateSchema('agent-envelope', await fixture('agent-envelope.valid.json')),
    { valid: true, errors: [] }
  );
  assert.deepEqual(
    await validateSchema('receipt', await fixture('receipt.valid.json')),
    { valid: true, errors: [] }
  );
  assert.deepEqual(defaultGrants(), ['dry-run.noop', 'preview.read']);
});

test('accepts only the exact read-only bridge grant profile', () => {
  assert.deepEqual(bridgeGrants(), ['preview.read', 'skill.invoke']);
  assert.deepEqual(
    normalizeL0Grants(['skill.invoke', 'preview.read']),
    ['preview.read', 'skill.invoke']
  );
  assert.throws(() => normalizeL0Grants(['skill.invoke']), /exact preview\.read bridge profile/);
  assert.throws(
    () => normalizeL0Grants(['preview.read', 'skill.invoke', 'dry-run.noop']),
    /exact preview\.read bridge profile/
  );
  assert.throws(
    () => normalizeL0Grants(['preview.read', 'skill.invoke', 'network.call']),
    /unknown L0 grants/
  );
});

test('accepts a versioned bridge envelope and enforces state bindings', async () => {
  const approved = await fixture('agent-envelope.valid.bridge.json');
  assert.equal(
    (await validateSchema('agent-envelope', approved)).valid,
    true
  );
  assert.equal(
    (await validateSchema(
      'agent-envelope',
      await fixture('agent-envelope.invalid.bridge-grants.json')
    )).valid,
    false
  );
  assert.equal(
    (await validateSchema(
      'agent-envelope',
      await fixture('agent-envelope.invalid.bridge-state-binding.json')
    )).valid,
    false
  );

  const rejected = structuredClone(approved);
  rejected.state = 'blocked';
  rejected.authorization_receipt_id = null;
  rejected.receipts = [];
  rejected.approval.actor = { kind: 'local_operator_action', assurance: 'unattested' };
  rejected.approval.approved_at = null;
  rejected.approval.rejected_at = '2026-07-12T00:03:00.000Z';
  assert.equal((await validateSchema('agent-envelope', rejected)).valid, true);

  const revoked = structuredClone(approved);
  revoked.state = 'blocked';
  revoked.approval.revoked_at = '2026-07-12T00:04:00.000Z';
  assert.equal((await validateSchema('agent-envelope', revoked)).valid, true);

  const ambiguousBlocked = structuredClone(approved);
  ambiguousBlocked.state = 'blocked';
  ambiguousBlocked.claim_id = null;
  ambiguousBlocked.result_id = null;
  assert.equal((await validateSchema('agent-envelope', ambiguousBlocked)).valid, false);
});

test('keeps bridge authorization active as a distinct approval state', async () => {
  assert.equal(
    (await validateSchema('approval-record', await fixture('approval-record.valid.bridge.json'))).valid,
    true
  );
  assert.equal(
    (await validateSchema(
      'approval-record',
      await fixture('approval-record.invalid.bridge-binding.json')
    )).valid,
    false
  );
});

test('keeps legacy, authorization, and execution receipts non-overlapping', async () => {
  const legacy = await fixture('receipt.valid.json');
  const authorization = await fixture('receipt.valid.authorization.json');
  const execution = await fixture('receipt.valid.execution.json');

  for (const value of [legacy, authorization, execution]) {
    assert.equal((await validateSchema('receipt', value)).valid, true);
  }

  assert.equal(Object.hasOwn(legacy, 'receipt_kind'), false);
  assert.equal(authorization.receipt_kind, 'authorization.receipt');
  assert.equal(Object.hasOwn(authorization, 'status'), false);
  assert.equal(execution.receipt_kind, 'skill.execution');

  assert.equal(
    (await validateSchema('receipt', { ...legacy, receipt_kind: 'authorization.receipt' })).valid,
    false
  );
  assert.equal(
    (await validateSchema('receipt', { ...authorization, status: 'passed' })).valid,
    false
  );
  assert.equal(
    (await validateSchema('receipt', await fixture('receipt.invalid.execution-binding.json'))).valid,
    false
  );
});

test('requires a nonblank task whenever a skill is prepared', async () => {
  const base = {
    requested_skill: 'decision-gate',
    requested_grants: ['preview.read', 'skill.invoke']
  };

  assert.equal((await validateSchema('prepare-request', base)).valid, false);
  assert.equal((await validateSchema('prepare-request', { ...base, task: '   ' })).valid, false);
  assert.equal(
    (await validateSchema('prepare-request', { ...base, task: 'Review the bridge' })).valid,
    true
  );
  assert.equal(
    (await validateSchema('prepare-request', { ...base, task: 'Review', requested_skill: '../x' })).valid,
    false
  );
});

test('validates all five bridge request families and rejects hostile fixtures', async () => {
  const cases = [
    ['bridge-claim-request', 'bridge-claim-request.invalid-agent-ref.json'],
    ['bridge-claim-request', 'bridge-claim-request.invalid-assurance.json'],
    ['bridge-interrupt-request', 'bridge-interrupt-request.invalid-session.json'],
    ['bridge-release-request', 'bridge-release-request.invalid-actor.json'],
    ['bridge-result-request', 'bridge-result-request.invalid-skill.json'],
    ['bridge-target-request', 'bridge-target-request.invalid-agent-ref.json'],
    ['bridge-target-request', 'bridge-target-request.invalid-actor.json']
  ];

  for (const [schemaName, invalidName] of cases) {
    assert.equal(
      (await validateSchema(schemaName, await fixture(`${schemaName}.valid.json`))).valid,
      true,
      schemaName
    );
    assert.equal(
      (await validateSchema(schemaName, await fixture(invalidName))).valid,
      false,
      invalidName
    );
  }
});
