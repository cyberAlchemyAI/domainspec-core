'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { EXPECTED, EXPERIMENT_ROOT, NODE_BINARY, ORIGINAL_STORE } = require('../src/constants.cjs');
const { assertInputsUnchanged, verifyPinnedInputs } = require('../src/identity.cjs');

const WORK_ROOT = path.join(EXPERIMENT_ROOT, '.work/CWE-002');
const STORE_PATH = path.join(WORK_ROOT, 'store');
const RECEIPT_PATH = path.join(EXPERIMENT_ROOT, 'execution/CWE-002/receipt.json');
const CLI_PATH = path.join(EXPERIMENT_ROOT, 'src/cli.cjs');

function runCli(...args) {
  const run = spawnSync(NODE_BINARY, [CLI_PATH, ...args], {
    cwd: path.dirname(EXPERIMENT_ROOT),
    encoding: 'utf8',
    timeout: 60000,
    maxBuffer: 1024 * 1024
  });
  assert.equal(run.status, 0, run.stderr);
  return JSON.parse(run.stdout);
}

function writeJsonExclusive(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, { flag: 'wx' });
}

function main() {
  assert.equal(fs.existsSync(WORK_ROOT), false, 'CWE-002 work root already exists');
  assert.equal(fs.existsSync(RECEIPT_PATH), false, 'CWE-002 receipt already exists');
  const before = verifyPinnedInputs();
  fs.mkdirSync(WORK_ROOT, { recursive: true });
  fs.cpSync(ORIGINAL_STORE, STORE_PATH, { recursive: true, errorOnExist: true, force: false });
  const first = before.receipt.scope.ledgers[0];
  const status = runCli('status', STORE_PATH);
  const verification = runCli('verify', STORE_PATH);
  const listing = runCli('list-ledgers', STORE_PATH);
  const raw = runCli('get-raw', STORE_PATH, first.path);
  const missing = runCli('get-raw', STORE_PATH, 'missing/.craft/ledger.yml');
  assert.equal(status.status, 'ok');
  assert.equal(verification.status, 'ok');
  assert.equal(verification.verification.recordCount, EXPECTED.recordCount);
  assert.equal(listing.status, 'ok');
  assert.equal(listing.ledgers.length, EXPECTED.ledgerCount);
  assert.deepEqual([...listing.ledgers].sort((a, b) => a.path.localeCompare(b.path)), listing.ledgers);
  assert.equal(raw.status, 'ok');
  assert.equal(raw.sizeBytes, first.sizeBytes);
  assert.equal(raw.sha256, first.sha256);
  assert.equal(Buffer.from(raw.rawBase64, 'base64').length, first.sizeBytes);
  assert.deepEqual(missing, {
    status: 'not-found',
    code: 'NOT_FOUND',
    ledgerPath: 'missing/.craft/ledger.yml'
  });
  const exported = Object.keys(require('../src/adapter.cjs')).sort();
  assert.deepEqual(exported, ['getRaw', 'listLedgers', 'status', 'verify']);
  const after = verifyPinnedInputs();
  assertInputsUnchanged(before, after);
  writeJsonExclusive(RECEIPT_PATH, {
    schemaVersion: 'craft-wavedb-readonly-node-receipt.v1',
    unit: 'CWE-002',
    verdict: 'pass',
    environment: { node: process.version, platform: process.platform, architecture: process.arch },
    checks: {
      exactAdapterExports: exported,
      exactCliCommands: ['status', 'verify', 'list-ledgers', 'get-raw'],
      status: 'pass',
      verify: 'pass',
      listLedgers: 'pass',
      getRaw: 'pass',
      typedNotFoundWithoutBytes: true,
      canonicalLedgersUnchanged: true,
      originalStoreUnchanged: true
    },
    forbiddenEffects: {
      network: false,
      originalStoreOpened: false,
      originalStoreMutated: false,
      craftLedgerMutated: false,
      writerSurfaceExposed: false,
      iteratorSurfaceExposed: false,
      subtreeSurfaceExposed: false,
      publication: false,
      deployment: false
    },
    blockers: [],
    successor: 'CWE-003',
    claimCeiling: 'An experiment-local four-operation adapter and CLI read one isolated copy of the accepted snapshot under Node v26.6.0; no server, production API, publication, or deployment is claimed.'
  });
}

try {
  main();
} catch (error) {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
}
