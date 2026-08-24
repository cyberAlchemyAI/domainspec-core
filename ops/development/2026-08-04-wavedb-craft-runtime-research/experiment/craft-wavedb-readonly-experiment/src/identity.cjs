'use strict';

const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const {
  ACCEPTED_RECEIPT,
  EXPECTED,
  NODE_BINARY,
  ORIGINAL_STORE,
  REPO_ROOT,
  WAVEDB_ADDON,
  WAVEDB_MODULE,
  WAVEDB_PACKAGE_ROOT
} = require('./constants.cjs');

function sha256(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function treeSnapshot(rootPath) {
  if (!fs.existsSync(rootPath)) {
    return { state: 'absent', digest: null, fileCount: 0, totalBytes: 0 };
  }
  const files = [];
  function visit(directory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const absolute = path.join(directory, entry.name);
      if (entry.isSymbolicLink()) {
        const bytes = Buffer.from(fs.readlinkSync(absolute), 'utf8');
        files.push({
          path: path.relative(rootPath, absolute),
          type: 'symlink',
          sizeBytes: bytes.length,
          sha256: sha256(bytes)
        });
      } else if (entry.isDirectory()) {
        visit(absolute);
      } else if (entry.isFile()) {
        const bytes = fs.readFileSync(absolute);
        files.push({
          path: path.relative(rootPath, absolute),
          type: 'file',
          sizeBytes: bytes.length,
          sha256: sha256(bytes)
        });
      }
    }
  }
  visit(rootPath);
  files.sort((left, right) => left.path.localeCompare(right.path));
  return {
    state: 'present',
    digest: sha256(Buffer.from(JSON.stringify(files), 'utf8')),
    fileCount: files.length,
    totalBytes: files.reduce((sum, item) => sum + item.sizeBytes, 0)
  };
}

function exactJson(filePath, expectedDigest, label) {
  const bytes = fs.readFileSync(filePath);
  assert.equal(sha256(bytes), expectedDigest, `${label} SHA-256 mismatch`);
  return JSON.parse(bytes.toString('utf8'));
}

function ledgerSnapshot(receipt) {
  return receipt.scope.ledgers.map((ledger) => {
    const absolute = path.join(REPO_ROOT, ledger.path);
    const bytes = fs.readFileSync(absolute);
    assert.equal(bytes.length, ledger.sizeBytes, `ledger size drift: ${ledger.path}`);
    assert.equal(sha256(bytes), ledger.sha256, `ledger hash drift: ${ledger.path}`);
    return { path: ledger.path, sizeBytes: bytes.length, sha256: ledger.sha256 };
  });
}

function verifyPinnedInputs() {
  assert.equal(process.version, EXPECTED.nodeVersion, 'Node runtime mismatch');
  assert.equal(sha256(fs.readFileSync(NODE_BINARY)), EXPECTED.nodeBinarySha256, 'Node binary mismatch');
  const receipt = exactJson(
    ACCEPTED_RECEIPT,
    EXPECTED.acceptedReceiptSha256,
    'accepted import receipt'
  );
  assert.equal(receipt.verdict, 'pass');
  assert.equal(receipt.environment.node, EXPECTED.nodeVersion);
  assert.equal(receipt.dependency.name, EXPECTED.packageName);
  assert.equal(receipt.dependency.version, EXPECTED.packageVersion);
  assert.equal(receipt.dependency.tarballSha256, EXPECTED.tarballSha256);
  assert.equal(receipt.dependency.addonSha256, EXPECTED.addonSha256);
  assert.equal(receipt.database.manifestKey, EXPECTED.manifestKey);
  assert.equal(receipt.database.manifestSha256, EXPECTED.manifestSha256);
  assert.equal(receipt.database.recordCount, EXPECTED.recordCount);
  assert.equal(receipt.scope.ledgerCount, EXPECTED.ledgerCount);
  assert.equal(receipt.scope.totalSourceBytes, EXPECTED.totalSourceBytes);
  assert.equal(sha256(fs.readFileSync(WAVEDB_MODULE)), EXPECTED.moduleSha256, 'WaveDB module mismatch');
  assert.equal(sha256(fs.readFileSync(WAVEDB_ADDON)), EXPECTED.addonSha256, 'WaveDB addon mismatch');
  const packageJson = JSON.parse(fs.readFileSync(path.join(WAVEDB_PACKAGE_ROOT, 'package.json'), 'utf8'));
  assert.equal(packageJson.name, EXPECTED.packageName);
  assert.equal(packageJson.version, EXPECTED.packageVersion);
  const store = treeSnapshot(ORIGINAL_STORE);
  assert.deepEqual(store, {
    state: 'present',
    digest: EXPECTED.storeDigest,
    fileCount: EXPECTED.storeFileCount,
    totalBytes: EXPECTED.storeTotalBytes
  });
  const ledgers = ledgerSnapshot(receipt);
  return { ledgers, receipt, store };
}

function assertInputsUnchanged(before, after) {
  assert.deepEqual(after.store, before.store, 'accepted original store changed');
  assert.deepEqual(after.ledgers, before.ledgers, 'canonical Craft ledgers changed');
}

module.exports = {
  assertInputsUnchanged,
  sha256,
  treeSnapshot,
  verifyPinnedInputs
};
