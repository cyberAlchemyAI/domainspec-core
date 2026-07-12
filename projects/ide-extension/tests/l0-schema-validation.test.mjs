import assert from 'node:assert/strict';
import { copyFile, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import {
  assertAgentEnvelope,
  assertReceipt,
  createSchemaValidators,
  getSchemaValidators,
  SCHEMA_FILES,
  validateAgentEnvelope,
  validateModuleManifest,
  validateReceipt,
  validateSchema
} from '../src/kernel/schema-validation.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const schemaDir = path.join(projectRoot, 'schemas');
const fixtureDir = path.join(projectRoot, 'tests/fixtures/schemas');

async function readJson(file) {
  return JSON.parse(await readFile(path.join(fixtureDir, file), 'utf8'));
}

const schemaNames = [
  'agent-envelope',
  'approval-record',
  'approve-request',
  'bridge-claim-request',
  'bridge-interrupt-request',
  'bridge-release-request',
  'bridge-result-request',
  'bridge-target-request',
  'canvas-interaction-request',
  'canvas-publish-request',
  'module-manifest',
  'prepare-request',
  'receipt',
  'reject-request'
];

test('compiles the explicit Draft 2020-12 schemas once', async () => {
  const first = await getSchemaValidators();
  const second = await getSchemaValidators();

  assert.strictEqual(first, second);
  assert.deepEqual(first.schema_names, schemaNames);
});

test('accepts one valid fixture for every schema through named validators', async () => {
  const envelope = await readJson('agent-envelope.valid.json');
  const manifest = await readJson('module-manifest.valid.json');
  const receipt = await readJson('receipt.valid.json');

  assert.deepEqual(await validateAgentEnvelope(envelope), { valid: true, errors: [] });
  assert.deepEqual(await validateModuleManifest(manifest), { valid: true, errors: [] });
  assert.deepEqual(await validateReceipt(receipt), { valid: true, errors: [] });
  assert.strictEqual(await assertAgentEnvelope(envelope, 'valid-envelope'), envelope);

  for (const schemaName of schemaNames) {
    const fixture = await readJson(`${schemaName}.valid.json`);
    assert.deepEqual(await validateSchema(schemaName, fixture), { valid: true, errors: [] });
  }
});

test('returns stable structured errors for hostile fixtures', async () => {
  const cases = [
    ['agent-envelope', 'agent-envelope.invalid-missing.json', 'required'],
    ['agent-envelope', 'agent-envelope.invalid-additional.json', 'additionalProperties'],
    ['approval-record', 'approval-record.invalid-missing.json', 'required'],
    ['approval-record', 'approval-record.invalid-state.json', 'enum'],
    ['approval-record', 'approval-record.invalid.bridge-binding.json', 'type'],
    ['approve-request', 'approve-request.invalid-additional.json', 'additionalProperties'],
    ['approve-request', 'approve-request.invalid-type.json', 'type'],
    ['bridge-claim-request', 'bridge-claim-request.invalid-assurance.json', 'const'],
    ['bridge-interrupt-request', 'bridge-interrupt-request.invalid-session.json', 'pattern'],
    ['bridge-release-request', 'bridge-release-request.invalid-actor.json', 'const'],
    ['bridge-result-request', 'bridge-result-request.invalid-skill.json', 'pattern'],
    ['bridge-target-request', 'bridge-target-request.invalid-actor.json', 'const'],
    ['canvas-interaction-request', 'canvas-interaction-request.invalid-payload.json', 'type'],
    ['canvas-publish-request', 'canvas-publish-request.invalid-traversal.json', 'pattern'],
    ['module-manifest', 'module-manifest.invalid-missing.json', 'required'],
    ['module-manifest', 'module-manifest.invalid-additional.json', 'additionalProperties'],
    ['prepare-request', 'prepare-request.invalid-context.json', 'type'],
    ['prepare-request', 'prepare-request.invalid-additional.json', 'additionalProperties'],
    ['prepare-request', 'prepare-request.invalid-skill.json', 'pattern'],
    ['receipt', 'receipt.invalid-missing.json', 'required'],
    ['receipt', 'receipt.invalid-type.json', 'type'],
    ['reject-request', 'reject-request.invalid-type.json', 'type'],
    ['reject-request', 'reject-request.invalid-additional.json', 'additionalProperties']
  ];

  for (const [schemaName, fixture, expectedKeyword] of cases) {
    const result = await validateSchema(schemaName, await readJson(fixture));

    assert.equal(result.valid, false, fixture);
    assert.ok(result.errors.some((error) => error.keyword === expectedKeyword), fixture);
    for (const error of result.errors) {
      assert.deepEqual(
        Object.keys(error),
        ['instance_path', 'schema_path', 'keyword', 'message', 'params']
      );
      assert.equal(typeof error.instance_path, 'string');
      assert.equal(typeof error.schema_path, 'string');
      assert.equal(typeof error.keyword, 'string');
      assert.equal(typeof error.message, 'string');
      assert.equal(Object.hasOwn(error, 'stack'), false);
    }
  }
});

test('throws a stable assertion error without exposing validator internals', async () => {
  const invalidReceipt = await readJson('receipt.invalid-type.json');

  await assert.rejects(
    assertReceipt(invalidReceipt, 'hostile-receipt'),
    (error) => {
      assert.equal(error.code, 'schema_validation_failed');
      assert.equal(error.schema_name, 'receipt');
      assert.equal(error.source, 'hostile-receipt');
      assert.ok(error.validation_errors.some((entry) => entry.keyword === 'type'));
      assert.equal(Object.hasOwn(error.validation_errors[0], 'stack'), false);
      return true;
    }
  );
});

test('rejects unknown schema names with the available closed vocabulary', async () => {
  await assert.rejects(
    validateSchema('ambient-schema', {}),
    (error) => {
      assert.equal(error.code, 'unknown_schema');
      assert.equal(error.schema_name, 'ambient-schema');
      assert.deepEqual(error.available_schemas, schemaNames);
      return true;
    }
  );
});

test('fails setup when an explicit schema file is malformed', async () => {
  const temporarySchemaDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-schemas-'));

  try {
    for (const file of Object.values(SCHEMA_FILES)) {
      await copyFile(path.join(schemaDir, file), path.join(temporarySchemaDir, file));
    }
    await writeFile(
      path.join(temporarySchemaDir, SCHEMA_FILES.receipt),
      '{"type":',
      'utf8'
    );

    await assert.rejects(createSchemaValidators({ schemaDir: temporarySchemaDir }), SyntaxError);
  } finally {
    await rm(temporarySchemaDir, { recursive: true, force: true });
  }
});
