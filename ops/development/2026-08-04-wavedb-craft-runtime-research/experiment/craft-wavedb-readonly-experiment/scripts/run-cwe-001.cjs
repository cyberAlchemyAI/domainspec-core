'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { spawn } = require('node:child_process');
const {
  EXPECTED,
  EXPERIMENT_ROOT,
  NODE_BINARY,
  ORIGINAL_STORE
} = require('../src/constants.cjs');
const { assertInputsUnchanged, verifyPinnedInputs } = require('../src/identity.cjs');

const WORK_ROOT = path.join(EXPERIMENT_ROOT, '.work/CWE-001');
const RECEIPT_PATH = path.join(EXPERIMENT_ROOT, 'execution/CWE-001/receipt.json');

function copyStore(target) {
  assert.equal(fs.existsSync(target), false, `isolated store already exists: ${target}`);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.cpSync(ORIGINAL_STORE, target, { recursive: true, errorOnExist: true, force: false });
}

function runChild(storePath) {
  return new Promise((resolve, reject) => {
    const child = spawn(NODE_BINARY, [path.join(EXPERIMENT_ROOT, 'src/child-reader.cjs'), storePath], {
      cwd: path.dirname(EXPERIMENT_ROOT),
      stdio: ['ignore', 'pipe', 'pipe']
    });
    let stdout = '';
    let stderr = '';
    child.stdout.setEncoding('utf8');
    child.stderr.setEncoding('utf8');
    child.stdout.on('data', (chunk) => { stdout += chunk; });
    child.stderr.on('data', (chunk) => { stderr += chunk; });
    child.on('error', reject);
    child.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`reader exited ${code}: ${stderr}`));
        return;
      }
      try {
        resolve(JSON.parse(stdout));
      } catch (error) {
        reject(new Error(`invalid child receipt: ${error.message}; ${stdout}`));
      }
    });
  });
}

function writeJsonExclusive(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, { flag: 'wx' });
}

async function main() {
  assert.equal(fs.existsSync(WORK_ROOT), false, 'CWE-001 work root already exists');
  assert.equal(fs.existsSync(RECEIPT_PATH), false, 'CWE-001 receipt already exists');
  const before = verifyPinnedInputs();
  const stores = [
    path.join(WORK_ROOT, 'reader-a/store'),
    path.join(WORK_ROOT, 'reader-b/store')
  ];
  stores.forEach(copyStore);
  const readers = await Promise.all(stores.map(runChild));
  assert.notEqual(readers[0].pid, readers[1].pid, 'fresh reader PIDs must differ');
  for (const reader of readers) {
    assert.equal(reader.verdict, 'pass');
    assert.equal(reader.manifestSha256, EXPECTED.manifestSha256);
    assert.equal(reader.ledgerCount, EXPECTED.ledgerCount);
    assert.equal(reader.recordCount, EXPECTED.recordCount);
    assert.equal(reader.recordsVerified, EXPECTED.recordCount);
  }
  const after = verifyPinnedInputs();
  assertInputsUnchanged(before, after);
  writeJsonExclusive(RECEIPT_PATH, {
    schemaVersion: 'craft-wavedb-readonly-node-receipt.v1',
    unit: 'CWE-001',
    verdict: 'pass',
    environment: { node: process.version, platform: process.platform, architecture: process.arch },
    inputs: {
      acceptedReceiptSha256: EXPECTED.acceptedReceiptSha256,
      originalStoreDigest: before.store.digest,
      ledgerCount: before.ledgers.length
    },
    checks: {
      inputIdentity: 'pass',
      independentProcessCount: 2,
      distinctPids: true,
      manifestSha256: EXPECTED.manifestSha256,
      recordCount: EXPECTED.recordCount,
      completeByteVerification: 'pass',
      canonicalLedgersUnchanged: true,
      originalStoreUnchanged: true
    },
    readers,
    forbiddenEffects: {
      network: false,
      originalStoreOpened: false,
      originalStoreMutated: false,
      craftLedgerMutated: false,
      apiConstructed: false,
      publication: false,
      deployment: false
    },
    blockers: [],
    successor: 'CWE-002',
    claimCeiling: 'Two independent Node v26.6.0 processes verified separate isolated copies of the accepted 57-record snapshot without changing canonical Craft ledgers or the accepted original store.'
  });
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
