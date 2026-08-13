'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const adapter = require('../src/adapter.cjs');
const { EXPECTED, EXPERIMENT_ROOT, ORIGINAL_STORE, WAVEDB_MODULE } = require('../src/constants.cjs');
const { assertInputsUnchanged, sha256, verifyPinnedInputs } = require('../src/identity.cjs');
const { encodeKey } = require('../src/manifest.cjs');
const { openReadSession } = require('../src/read-session.cjs');

const WORK_ROOT = path.join(EXPERIMENT_ROOT, '.work/CWE-003');
const CLEAN_STORE = path.join(WORK_ROOT, 'clean/store');
const RECEIPT_PATH = path.join(EXPERIMENT_ROOT, 'execution/CWE-003/receipt.json');
const TERMINAL_PATH = path.join(EXPERIMENT_ROOT, 'execution/terminal-receipt.json');
const MAXIMUM_CLAIM = 'A repeatable checkout-local, read-only experiment independently accessed the accepted derived Craft snapshot without changing canonical source or accepted store bytes.';

function artifactRef(filePath) {
  const bytes = fs.readFileSync(filePath);
  return {
    path: path.relative(EXPERIMENT_ROOT, filePath).split(path.sep).join('/'),
    sha256: sha256(bytes),
    sizeBytes: bytes.length
  };
}

async function exactManifestBytes(storePath) {
  const { WaveDB } = require(WAVEDB_MODULE);
  const database = new WaveDB(storePath);
  try {
    const value = await database.get(EXPECTED.manifestKey);
    const bytes = Buffer.isBuffer(value) ? value : Buffer.from(value, 'utf8');
    assert.equal(sha256(bytes), EXPECTED.manifestSha256, 'isolated manifest identity mismatch');
    return bytes;
  } finally {
    database.close();
  }
}

function expectedMetadataBytes(ledger) {
  return Buffer.from(JSON.stringify({
    path: ledger.path,
    sizeBytes: ledger.sizeBytes,
    sha256: ledger.sha256,
    encoding: 'utf-8',
    authority: 'source-yaml'
  }), 'utf8');
}

function injectedSession(name, receipt, database) {
  return openReadSession({
    storePath: path.join(WORK_ROOT, name, 'store'),
    acceptedReceipt: receipt,
    openDatabase: () => database
  });
}

async function assertInvalidates(session, expectedCode, counters) {
  const failed = await session.verify();
  const readsAfterFailure = counters.reads;
  const later = await session.verify();
  assert.equal(failed.ok, false);
  assert.equal(failed.code, expectedCode);
  assert.deepEqual(later, {
    ok: false,
    code: 'SESSION_INVALIDATED',
    message: 'session invalidated'
  });
  assert.equal(counters.reads, readsAfterFailure, 'invalidated session performed a later read');
  assert.equal(counters.closes, 1, 'failed session must close exactly once');
  return { code: failed.code, laterCode: later.code, reads: counters.reads, closes: counters.closes };
}

function writeJsonExclusive(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, { flag: 'wx' });
}

async function main() {
  assert.equal(fs.existsSync(WORK_ROOT), false, 'CWE-003 work root already exists');
  assert.equal(fs.existsSync(RECEIPT_PATH), false, 'CWE-003 receipt already exists');
  assert.equal(fs.existsSync(TERMINAL_PATH), false, 'terminal receipt already exists');

  const before = verifyPinnedInputs();
  fs.mkdirSync(path.dirname(CLEAN_STORE), { recursive: true });
  fs.cpSync(ORIGINAL_STORE, CLEAN_STORE, { recursive: true, errorOnExist: true, force: false });
  const manifestBytes = await exactManifestBytes(CLEAN_STORE);

  const missing = await adapter.getRaw(CLEAN_STORE, 'missing/.craft/ledger.yml');
  assert.equal(missing.status, 'not-found');
  assert.equal(missing.code, 'NOT_FOUND');
  assert.equal(missing.bytes, undefined);

  const manifestCounters = { reads: 0, closes: 0 };
  const manifestSession = injectedSession('damaged-manifest', before.receipt, {
    async get() {
      manifestCounters.reads += 1;
      return Buffer.from('damaged-manifest', 'utf8');
    },
    close() { manifestCounters.closes += 1; }
  });
  const damagedManifest = await assertInvalidates(manifestSession, 'MANIFEST_INVALID', manifestCounters);

  const firstLedger = before.receipt.scope.ledgers[0];
  const firstEncoded = encodeKey(firstLedger.path);
  const recordCounters = { reads: 0, closes: 0 };
  const recordSession = injectedSession('damaged-record', before.receipt, {
    async get(key) {
      recordCounters.reads += 1;
      if (key === EXPECTED.manifestKey) return manifestBytes;
      if (key === `craft/meta/${firstEncoded}`) return expectedMetadataBytes(firstLedger);
      if (key === `craft/raw/${firstEncoded}`) return Buffer.from('damaged-record', 'utf8');
      throw Object.assign(new Error(`unexpected key: ${key}`), { code: 'TEST_KEY_INVALID' });
    },
    close() { recordCounters.closes += 1; }
  });
  const damagedRecord = await assertInvalidates(recordSession, 'RECORD_INVALID', recordCounters);

  let openAttempts = 0;
  const missingStoreSession = openReadSession({
    storePath: path.join(WORK_ROOT, 'missing-store/store'),
    acceptedReceipt: before.receipt,
    openDatabase: () => {
      openAttempts += 1;
      throw Object.assign(new Error('snapshot store is absent'), { code: 'SNAPSHOT_UNAVAILABLE' });
    }
  });
  const missingStore = await missingStoreSession.status();
  assert.equal(missingStore.ok, false);
  assert.equal(missingStore.code, 'SNAPSHOT_UNAVAILABLE');
  assert.equal(openAttempts, 1);

  const readCounters = { reads: 0, closes: 0 };
  const readFailureSession = injectedSession('read-failure', before.receipt, {
    async get() {
      readCounters.reads += 1;
      throw Object.assign(new Error('injected read failure'), { code: 'INJECTED_READ_FAILURE' });
    },
    close() { readCounters.closes += 1; }
  });
  const readFailure = await assertInvalidates(readFailureSession, 'INJECTED_READ_FAILURE', readCounters);

  const clean = await adapter.verify(CLEAN_STORE);
  assert.equal(clean.status, 'ok');
  assert.equal(clean.verification.recordsVerified, EXPECTED.recordCount);
  const after = verifyPinnedInputs();
  assertInputsUnchanged(before, after);

  const nodeReceipt = {
    schemaVersion: 'craft-wavedb-readonly-node-receipt.v1',
    unit: 'CWE-003',
    verdict: 'pass',
    environment: { node: process.version, platform: process.platform, architecture: process.arch },
    checks: {
      missingKey: { status: missing.status, code: missing.code, bytesSuppressed: missing.bytes === undefined },
      damagedManifest,
      damagedRecord,
      missingStoreOpenFailure: { code: missingStore.code, openAttempts },
      injectedReadFailure: readFailure,
      failedSessionLaterReadSuppressed: true,
      cleanVerificationAfterNegativeControls: 'pass',
      cleanRecordCount: clean.verification.recordsVerified,
      canonicalLedgersUnchanged: true,
      originalStoreUnchanged: true
    },
    forbiddenEffects: {
      network: false,
      originalStoreOpened: false,
      originalStoreMutated: false,
      craftLedgerMutated: false,
      apiUnitSelected: false,
      publication: false,
      deployment: false,
      promotion: false
    },
    blockers: [],
    successor: null,
    claimCeiling: MAXIMUM_CLAIM
  };
  writeJsonExclusive(RECEIPT_PATH, nodeReceipt);

  const terminalReceipt = {
    schemaVersion: 'craft-wavedb-readonly-experiment-terminal.v1',
    experiment: 'craft-wavedb-readonly-experiment',
    workPackId: 'WP-CWE-20260806',
    result: 'pass',
    completedUnits: ['CWE-001', 'CWE-002', 'CWE-003'],
    evidenceRefs: [
      artifactRef(path.join(EXPERIMENT_ROOT, 'execution/CWE-001/receipt.json')),
      artifactRef(path.join(EXPERIMENT_ROOT, 'execution/CWE-001/task-session-terminal.json')),
      artifactRef(path.join(EXPERIMENT_ROOT, 'execution/CWE-002/receipt.json')),
      artifactRef(path.join(EXPERIMENT_ROOT, 'execution/CWE-002/task-session-terminal.json')),
      artifactRef(RECEIPT_PATH)
    ],
    finalIdentity: {
      acceptedReceiptSha256: EXPECTED.acceptedReceiptSha256,
      canonicalLedgerCount: EXPECTED.ledgerCount,
      canonicalSourceBytes: EXPECTED.totalSourceBytes,
      originalStoreDigest: after.store.digest,
      originalStoreFileCount: after.store.fileCount,
      originalStoreTotalBytes: after.store.totalBytes
    },
    maximumClaim: MAXIMUM_CLAIM,
    forbiddenSuccessors: {
      apiUnitSelected: false,
      productIntegrationSelected: false,
      publicationSelected: false,
      deploymentSelected: false,
      promotionSelected: false
    },
    forbiddenEffects: {
      network: false,
      originalStoreOpened: false,
      originalStoreMutated: false,
      craftLedgerMutated: false,
      canonicalStoreReplaced: false,
      publication: false,
      deployment: false,
      promotion: false
    },
    successor: null,
    authorityEffect: 'none',
    blockers: []
  };
  writeJsonExclusive(TERMINAL_PATH, terminalReceipt);
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
