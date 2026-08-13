'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');
const adapter = require('../src/adapter.cjs');
const { ORIGINAL_STORE } = require('../src/constants.cjs');
const { verifyPinnedInputs } = require('../src/identity.cjs');

test('adapter exports exactly four read operations', () => {
  assert.deepEqual(Object.keys(adapter).sort(), ['getRaw', 'listLedgers', 'status', 'verify']);
  for (const forbidden of ['WaveDB', 'put', 'flush', 'iterator', 'Subtree']) {
    assert.equal(Object.prototype.hasOwnProperty.call(adapter, forbidden), false);
  }
});

test('manifest-bounded getRaw returns Buffer or typed NOT_FOUND without bytes', async () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'cwe-002-test-'));
  const experimentWork = path.join(__dirname, '../.work/CWE-002-test');
  try {
    assert.equal(experimentWork.startsWith(path.resolve(__dirname, '..')), true);
    fs.cpSync(ORIGINAL_STORE, experimentWork, { recursive: true, errorOnExist: true, force: false });
    const receipt = verifyPinnedInputs().receipt;
    const known = receipt.scope.ledgers[0];
    const found = await adapter.getRaw(experimentWork, known.path);
    assert.equal(found.status, 'ok');
    assert.equal(Buffer.isBuffer(found.bytes), true);
    assert.equal(found.bytes.length, known.sizeBytes);
    const missing = await adapter.getRaw(experimentWork, `${tempRoot}/not-declared`);
    assert.equal(missing.status, 'not-found');
    assert.equal(missing.code, 'NOT_FOUND');
    assert.equal(missing.bytes, undefined);
  } finally {
    fs.rmSync(experimentWork, { recursive: true, force: true });
    fs.rmSync(tempRoot, { recursive: true, force: true });
  }
});
