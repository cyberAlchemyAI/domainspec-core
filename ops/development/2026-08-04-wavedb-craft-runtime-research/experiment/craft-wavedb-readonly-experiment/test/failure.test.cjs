'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const adapter = require('../src/adapter.cjs');
const { EXPECTED, EXPERIMENT_ROOT, ORIGINAL_STORE, WAVEDB_MODULE } = require('../src/constants.cjs');
const { sha256, verifyPinnedInputs } = require('../src/identity.cjs');
const { encodeKey } = require('../src/manifest.cjs');
const { openReadSession } = require('../src/read-session.cjs');

async function manifestBytes(storePath) {
  const { WaveDB } = require(WAVEDB_MODULE);
  const database = new WaveDB(storePath);
  try {
    const value = await database.get(EXPECTED.manifestKey);
    const bytes = Buffer.isBuffer(value) ? value : Buffer.from(value, 'utf8');
    assert.equal(sha256(bytes), EXPECTED.manifestSha256);
    return bytes;
  } finally {
    database.close();
  }
}

function metadataBytes(ledger) {
  return Buffer.from(JSON.stringify({
    path: ledger.path,
    sizeBytes: ledger.sizeBytes,
    sha256: ledger.sha256,
    encoding: 'utf-8',
    authority: 'source-yaml'
  }), 'utf8');
}

async function assertInvalidated(session, expectedCode, counters) {
  const failed = await session.verify();
  const reads = counters.reads;
  const later = await session.verify();
  assert.equal(failed.ok, false);
  assert.equal(failed.code, expectedCode);
  assert.equal(later.ok, false);
  assert.equal(later.code, 'SESSION_INVALIDATED');
  assert.equal(counters.reads, reads);
  assert.equal(counters.closes, 1);
}

test('damaged manifest returns MANIFEST_INVALID and suppresses later reads', async () => {
  const receipt = verifyPinnedInputs().receipt;
  const counters = { reads: 0, closes: 0 };
  const session = openReadSession({
    storePath: path.join(EXPERIMENT_ROOT, '.work/CWE-003-test/damaged-manifest/store'),
    acceptedReceipt: receipt,
    openDatabase: () => ({
      async get() { counters.reads += 1; return Buffer.from('damaged'); },
      close() { counters.closes += 1; }
    })
  });
  await assertInvalidated(session, 'MANIFEST_INVALID', counters);
});

test('damaged raw record returns RECORD_INVALID and suppresses later reads', async () => {
  const receipt = verifyPinnedInputs().receipt;
  const first = receipt.scope.ledgers[0];
  const encoded = encodeKey(first.path);
  const sourceStore = path.join(EXPERIMENT_ROOT, '.work/CWE-003-test/manifest-source/store');
  fs.mkdirSync(path.dirname(sourceStore), { recursive: true });
  fs.cpSync(ORIGINAL_STORE, sourceStore, { recursive: true, errorOnExist: true, force: false });
  const exactManifest = await manifestBytes(sourceStore);
  const counters = { reads: 0, closes: 0 };
  try {
    const session = openReadSession({
      storePath: path.join(EXPERIMENT_ROOT, '.work/CWE-003-test/damaged-record/store'),
      acceptedReceipt: receipt,
      openDatabase: () => ({
        async get(key) {
          counters.reads += 1;
          if (key === EXPECTED.manifestKey) return exactManifest;
          if (key === `craft/meta/${encoded}`) return metadataBytes(first);
          if (key === `craft/raw/${encoded}`) return Buffer.from('damaged');
          throw new Error(`unexpected key: ${key}`);
        },
        close() { counters.closes += 1; }
      })
    });
    await assertInvalidated(session, 'RECORD_INVALID', counters);
  } finally {
    fs.rmSync(path.join(EXPERIMENT_ROOT, '.work/CWE-003-test/manifest-source'), { recursive: true, force: true });
  }
});

test('missing-store opener returns typed SNAPSHOT_UNAVAILABLE', async () => {
  let opens = 0;
  const session = openReadSession({
    storePath: path.join(EXPERIMENT_ROOT, '.work/CWE-003-test/missing-store/store'),
    acceptedReceipt: verifyPinnedInputs().receipt,
    openDatabase: () => {
      opens += 1;
      throw Object.assign(new Error('snapshot store is absent'), { code: 'SNAPSHOT_UNAVAILABLE' });
    }
  });
  const result = await session.status();
  assert.equal(result.ok, false);
  assert.equal(result.code, 'SNAPSHOT_UNAVAILABLE');
  assert.equal(opens, 1);
});

test('injected read failure closes once and permits no later read', async () => {
  const counters = { reads: 0, closes: 0 };
  const session = openReadSession({
    storePath: path.join(EXPERIMENT_ROOT, '.work/CWE-003-test/read-failure/store'),
    acceptedReceipt: verifyPinnedInputs().receipt,
    openDatabase: () => ({
      async get() {
        counters.reads += 1;
        throw Object.assign(new Error('injected read failure'), { code: 'INJECTED_READ_FAILURE' });
      },
      close() { counters.closes += 1; }
    })
  });
  await assertInvalidated(session, 'INJECTED_READ_FAILURE', counters);
});

test('unknown manifest-bounded key returns typed NOT_FOUND on an isolated copy', async () => {
  const store = path.join(EXPERIMENT_ROOT, '.work/CWE-003-test/missing-key/store');
  try {
    fs.mkdirSync(path.dirname(store), { recursive: true });
    fs.cpSync(ORIGINAL_STORE, store, { recursive: true, errorOnExist: true, force: false });
    const result = await adapter.getRaw(store, 'missing/.craft/ledger.yml');
    assert.equal(result.status, 'not-found');
    assert.equal(result.code, 'NOT_FOUND');
    assert.equal(result.bytes, undefined);
  } finally {
    fs.rmSync(path.join(EXPERIMENT_ROOT, '.work/CWE-003-test/missing-key'), { recursive: true, force: true });
  }
});
