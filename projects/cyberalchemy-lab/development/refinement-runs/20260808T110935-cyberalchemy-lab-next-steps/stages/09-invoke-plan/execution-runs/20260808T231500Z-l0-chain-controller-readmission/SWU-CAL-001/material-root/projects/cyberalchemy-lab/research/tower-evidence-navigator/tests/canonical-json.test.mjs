import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';

import {
  CanonicalJsonError,
  PROFILE_ID,
  PROFILE_SCHEMA_VERSION,
  canonicalize,
  canonicalizeJsonText,
  digestCanonical,
  digestCanonicalJsonText,
  parseCanonicalJson
} from '../tools/canonical-json.mjs';

const PROFILE_PATH = new URL('../schemas/canonical-json-profile.json', import.meta.url);

function expectCode(operation, code) {
  assert.throws(operation, (error) => error instanceof CanonicalJsonError && error.code === code);
}

test('profile document closes the canonical vocabulary and authority ceiling', async () => {
  const profile = JSON.parse(await readFile(PROFILE_PATH, 'utf8'));
  assert.equal(profile.profile_id, PROFILE_ID);
  assert.equal(profile.schema_version, PROFILE_SCHEMA_VERSION);
  assert.equal(profile.authority_effect, 'none');
  assert.deepEqual(profile.accepted_values, ['null', 'boolean', 'string', 'array', 'object', 'safe-integer']);
  assert.equal(profile.parsing.duplicate_key_check, 'before-json-parse-materialization');
  assert.deepEqual(profile.digest.preimage_fields, [
    'profile_id',
    'profile_schema_version',
    'value_schema_version',
    'canonical_utf8_bytes'
  ]);
});

test('golden vector 1 normalizes object order and binds digest domain', () => {
  const left = digestCanonicalJsonText('{"b":2,"a":1}', 'fixture-record/v1');
  const right = digestCanonical({ a: 1, b: 2 }, 'fixture-record/v1');
  assert.equal(left.bytes.toString('utf8'), '{"a":1,"b":2}');
  assert.deepEqual(left, right);
  assert.equal(left.sha256, '42a23dc02bed6e7eee45f79e06a928fd48cf3e138c560abd8d1e75395111c089');
});

test('golden vector 2 preserves arrays and ECMAScript string escaping', () => {
  const value = { z: [true, null, 'é\n'], A: -9007199254740991 };
  const result = digestCanonical(value, 'fixture-record/v2');
  assert.equal(result.bytes.toString('utf8'), '{"A":-9007199254740991,"z":[true,null,"é\\n"]}');
  assert.equal(result.sha256, '7e8a3903aa336ebc87b364aec45913cdbc162f0fc4343ef1322e9a259bcadb44');
});

test('equivalent nested objects produce identical bytes', () => {
  const first = canonicalize({ z: { b: 2, a: 1 }, a: [] });
  const second = canonicalizeJsonText('{ "a": [], "z": { "a": 1, "b": 2 } }');
  assert.deepEqual(first, second);
});

test('raw parser rejects decoded duplicate keys before materialization', () => {
  expectCode(() => parseCanonicalJson('{"a":1,"\\u0061":2}'), 'CAL_JSON_DUPLICATE_KEY');
});

test('raw parser rejects forbidden number forms and unsafe integers', () => {
  expectCode(() => parseCanonicalJson('1.0'), 'CAL_JSON_NUMBER_FORM_FORBIDDEN');
  expectCode(() => parseCanonicalJson('1e0'), 'CAL_JSON_NUMBER_FORM_FORBIDDEN');
  expectCode(() => parseCanonicalJson('-0'), 'CAL_JSON_NEGATIVE_ZERO');
  expectCode(() => parseCanonicalJson('9007199254740992'), 'CAL_JSON_UNSAFE_INTEGER');
});

test('object keys are restricted to printable ASCII', () => {
  expectCode(() => parseCanonicalJson('{"é":1}'), 'CAL_JSON_KEY_NOT_PRINTABLE_ASCII');
  expectCode(() => canonicalize({ '\n': 1 }), 'CAL_JSON_KEY_NOT_PRINTABLE_ASCII');
});

test('direct JavaScript values reject unsupported values and cycles', () => {
  expectCode(() => canonicalize(undefined), 'CAL_JSON_UNSUPPORTED_VALUE');
  expectCode(() => canonicalize(1.5), 'CAL_JSON_NUMBER_FORM_FORBIDDEN');
  expectCode(() => canonicalize(-0), 'CAL_JSON_NEGATIVE_ZERO');
  expectCode(() => canonicalize(9007199254740992), 'CAL_JSON_UNSAFE_INTEGER');
  expectCode(() => canonicalize(new Date()), 'CAL_JSON_UNSUPPORTED_VALUE');
  expectCode(() => canonicalize([, 1]), 'CAL_JSON_UNSUPPORTED_VALUE');
  const symbolObject = { a: 1 };
  symbolObject[Symbol('hidden')] = 2;
  expectCode(() => canonicalize(symbolObject), 'CAL_JSON_UNSUPPORTED_VALUE');
  const cyclic = {};
  cyclic.self = cyclic;
  expectCode(() => canonicalize(cyclic), 'CAL_JSON_CYCLE');
});

test('digest requires an explicit non-empty value schema version', () => {
  expectCode(() => digestCanonical({}, ''), 'CAL_JSON_SCHEMA_VERSION_REQUIRED');
  expectCode(() => digestCanonical({}), 'CAL_JSON_SCHEMA_VERSION_REQUIRED');
});
