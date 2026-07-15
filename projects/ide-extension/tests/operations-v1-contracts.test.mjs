import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import {
  assertUtf8ByteLimit,
  OPERATIONS_V1_EVENT_TYPES,
  OPERATIONS_V1_EVENT_VERSION,
  OPERATIONS_V1_LIMITS,
  utf8ByteLength
} from '../src/kernel/operations-contracts.mjs';
import { validateSchema } from '../src/kernel/schema-validation.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const fixtureDir = path.join(projectRoot, 'tests/fixtures/schemas');

async function fixture(name) {
  return JSON.parse(await readFile(path.join(fixtureDir, name), 'utf8'));
}

async function assertFixture(schemaName, name, expectedValid) {
  const result = await validateSchema(schemaName, await fixture(name));
  assert.equal(result.valid, expectedValid, `${name}: ${JSON.stringify(result.errors)}`);
  return result;
}

test('admits exact derivation and operation request variants', async () => {
  await assertFixture(
    'operations-surface-derive-request',
    'operations-surface-derive-request.valid.json',
    true
  );
  for (const mode of ['append', 'replace', 'rebuild']) {
    await assertFixture(
      'content-operation-request',
      `content-operation-request.valid.${mode}.json`,
      true
    );
  }
});

test('rejects authority fields, invalid ids, regions, missing digests, and mode/input mismatch', async () => {
  await assertFixture(
    'operations-surface-derive-request',
    'operations-surface-derive-request.invalid-additional.json',
    false
  );
  for (const name of [
    'content-operation-request.invalid-mode-input.json',
    'content-operation-request.invalid-region.json',
    'content-operation-request.invalid-additional.json',
    'content-operation-request.invalid-id.json',
    'content-operation-request.invalid-missing-digest.json'
  ]) {
    const result = await assertFixture('content-operation-request', name, false);
    assert.ok(result.errors.some((error) => ['oneOf', 'const', 'required', 'pattern', 'additionalProperties'].includes(error.keyword)));
  }
});

test('binds navigation actions to exact destination shapes', async () => {
  await assertFixture(
    'canvas-navigation-request',
    'canvas-navigation-request.valid.redirect.json',
    true
  );
  await assertFixture(
    'canvas-navigation-request',
    'canvas-navigation-request.valid.refresh.json',
    true
  );
  await assertFixture(
    'canvas-navigation-request',
    'canvas-navigation-request.invalid-target-binding.json',
    false
  );
  await assertFixture(
    'canvas-navigation-request',
    'canvas-navigation-request.invalid-refresh-destination.json',
    false
  );
});

test('freezes transient acknowledgement and pruning command contracts', async () => {
  const cases = [
    ['canvas-navigation-ack-request', 'canvas-navigation-ack-request.valid.json', true],
    ['canvas-navigation-ack-request', 'canvas-navigation-ack-request.invalid-status.json', false],
    ['canvas-pruning-preview-request', 'canvas-pruning-preview-request.valid.json', true],
    ['canvas-pruning-preview-request', 'canvas-pruning-preview-request.invalid-additional.json', false],
    ['canvas-pruning-commit-request', 'canvas-pruning-commit-request.valid.json', true],
    ['canvas-pruning-commit-request', 'canvas-pruning-commit-request.invalid-digest.json', false]
  ];
  for (const [schemaName, name, expectedValid] of cases) {
    await assertFixture(schemaName, name, expectedValid);
  }
});

test('freezes Operations V1 byte, retention, and event constants', () => {
  assert.deepEqual(OPERATIONS_V1_LIMITS, {
    http_request_bytes: 5 * 1024 * 1024,
    source_html_bytes: 4 * 1024 * 1024,
    fragment_html_bytes: 512 * 1024,
    result_html_bytes: 8 * 1024 * 1024,
    retention_soft_bytes: 1024 * 1024 * 1024,
    retention_hard_bytes: 2 * 1024 * 1024 * 1024,
    retention_grace_ms: 7 * 24 * 60 * 60 * 1000,
    retention_reclaim_below_bytes: 1024 * 1024 * 1024
  });
  assert.equal(OPERATIONS_V1_EVENT_VERSION, 4);
  assert.deepEqual(OPERATIONS_V1_EVENT_TYPES, [
    'canvas.operations_surface_derived',
    'canvas.content_operation_committed',
    'canvas.display_target_selected',
    'canvas.pruning_requested',
    'canvas.revision_pruned',
    'canvas.pruning_completed',
    'canvas.interaction_recorded'
  ]);
  assert.equal(Object.isFrozen(OPERATIONS_V1_LIMITS), true);
  assert.equal(Object.isFrozen(OPERATIONS_V1_EVENT_TYPES), true);
});

test('admits limit minus one and exact, then rejects plus one UTF-8 byte', () => {
  const byteLimits = [
    ['http_request', OPERATIONS_V1_LIMITS.http_request_bytes],
    ['source_html', OPERATIONS_V1_LIMITS.source_html_bytes],
    ['fragment_html', OPERATIONS_V1_LIMITS.fragment_html_bytes],
    ['result_html', OPERATIONS_V1_LIMITS.result_html_bytes]
  ];

  for (const [name, maxBytes] of byteLimits) {
    assert.equal(assertUtf8ByteLimit('a'.repeat(maxBytes - 1), maxBytes, name), maxBytes - 1);
    assert.equal(assertUtf8ByteLimit('a'.repeat(maxBytes), maxBytes, name), maxBytes);
    assert.throws(
      () => assertUtf8ByteLimit('a'.repeat(maxBytes + 1), maxBytes, name),
      (error) => error.code === 'operations_byte_limit_exceeded'
        && error.limit_name === name
        && error.max_bytes === maxBytes
        && error.actual_bytes === maxBytes + 1
    );
  }
});

test('uses UTF-8 bytes rather than JavaScript character counts', async () => {
  const maxBytes = OPERATIONS_V1_LIMITS.fragment_html_bytes;
  const exactMultibyte = '\u00e9'.repeat(maxBytes / 2);
  assert.equal(exactMultibyte.length, maxBytes / 2);
  assert.equal(utf8ByteLength(exactMultibyte), maxBytes);
  assert.equal(assertUtf8ByteLimit(exactMultibyte, maxBytes, 'fragment_html'), maxBytes);
  assert.throws(
    () => assertUtf8ByteLimit(`${exactMultibyte}\u00e9`, maxBytes, 'fragment_html'),
    (error) => error.actual_bytes === maxBytes + 2
  );

  const oversizedByBytes = await fixture('content-operation-request.valid.append.json');
  oversizedByBytes.input.html = `${exactMultibyte}\u00e9`;
  const schemaResult = await validateSchema('content-operation-request', oversizedByBytes);
  assert.equal(schemaResult.valid, true);
});

test('rejects invalid byte helper inputs without coercion', () => {
  assert.throws(() => utf8ByteLength(Buffer.from('html')), TypeError);
  assert.throws(() => assertUtf8ByteLimit('html', -1, 'source_html'), TypeError);
  assert.throws(() => assertUtf8ByteLimit('html', 4, ''), TypeError);
});
