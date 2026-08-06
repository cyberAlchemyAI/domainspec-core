'use strict';

const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const [repoRootArg, scopeFileArg, storePathArg, resultPathArg, packageRootArg] = process.argv.slice(2);

function sha256(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function encodeKey(value) {
  return Buffer.from(value, 'utf8').toString('base64url');
}

function loadLedgers(repoRoot, scopeFile) {
  const excluded = new Set(['baselines', 'closeout', 'material', 'outputs', 'refresh', 'refreshes', 'staging']);
  const relativePaths = fs.readFileSync(scopeFile, 'utf8')
    .split(/\r?\n/u)
    .map((value) => value.trim())
    .filter(Boolean);
  assert.ok(relativePaths.length > 0, 'scope must not be empty');
  assert.equal(new Set(relativePaths).size, relativePaths.length, 'scope contains duplicate paths');

  return relativePaths.map((relativePath) => {
    assert.equal(path.isAbsolute(relativePath), false, `absolute path is forbidden: ${relativePath}`);
    assert.equal(relativePath.endsWith('/.craft/ledger.yml'), true, `not a Craft ledger: ${relativePath}`);
    for (const segment of relativePath.split('/')) {
      assert.equal(excluded.has(segment), false, `historical/staged path is forbidden: ${relativePath}`);
    }
    const absolutePath = path.resolve(repoRoot, relativePath);
    assert.equal(absolutePath.startsWith(`${repoRoot}${path.sep}`), true, `path escapes root: ${relativePath}`);
    const sourceBytes = fs.readFileSync(absolutePath);
    const text = sourceBytes.toString('utf8');
    assert.deepEqual(Buffer.from(text, 'utf8'), sourceBytes, `ledger is not lossless UTF-8: ${relativePath}`);
    return {
      relativePath,
      absolutePath,
      sourceBytes,
      text,
      sizeBytes: sourceBytes.length,
      sha256: sha256(sourceBytes)
    };
  });
}

async function main() {
  assert.ok(repoRootArg && scopeFileArg && storePathArg && resultPathArg && packageRootArg,
    'usage: node import-ledgers-text.js <repo-root> <scope-file> <store-path> <result-path> <package-root>');
  const startedAt = new Date();
  const repoRoot = fs.realpathSync(repoRootArg);
  const scopeFile = path.resolve(scopeFileArg);
  const storePath = path.resolve(storePathArg);
  const resultPath = path.resolve(resultPathArg);
  const packageRoot = fs.realpathSync(packageRootArg);
  const packageManifest = JSON.parse(fs.readFileSync(path.join(packageRoot, 'package.json'), 'utf8'));
  const resolvedPackage = require.resolve(packageRoot);
  const { WaveDB } = require(resolvedPackage);
  const ledgers = loadLedgers(repoRoot, scopeFile);
  const manifest = {
    schemaVersion: 'craft-wavedb-snapshot.v1',
    authority: 'derived-read-model-only',
    encoding: 'utf-8',
    importedAt: new Date().toISOString(),
    ledgers: ledgers.map((ledger) => ({
      path: ledger.relativePath,
      sizeBytes: ledger.sizeBytes,
      sha256: ledger.sha256
    }))
  };
  const records = [{ key: 'craft/manifest/v1', value: JSON.stringify(manifest), kind: 'manifest' }];
  for (const ledger of ledgers) {
    const encodedPath = encodeKey(ledger.relativePath);
    records.push({
      key: `craft/meta/${encodedPath}`,
      value: JSON.stringify({
        path: ledger.relativePath,
        sizeBytes: ledger.sizeBytes,
        sha256: ledger.sha256,
        encoding: 'utf-8',
        authority: 'source-yaml'
      }),
      kind: 'metadata'
    });
    records.push({ key: `craft/raw/${encodedPath}`, value: ledger.text, kind: 'ledger', ledger });
  }

  fs.mkdirSync(path.dirname(storePath), { recursive: true });
  let assertions = 0;
  const writer = new WaveDB(storePath);
  try {
    for (const record of records) {
      await writer.put(record.key, record.value);
    }
    writer.flush();
    for (const record of records) {
      const observed = await writer.get(record.key);
      assert.equal(observed, record.value, `immediate readback differs: ${record.key}`);
      assertions += 1;
    }
  } finally {
    writer.close();
  }

  const reader = new WaveDB(storePath);
  try {
    for (const record of records) {
      const observed = await reader.get(record.key);
      assert.equal(observed, record.value, `reopened readback differs: ${record.key}`);
      assertions += 1;
      if (record.kind === 'ledger') {
        assert.equal(sha256(Buffer.from(observed, 'utf8')), record.ledger.sha256,
          `reopened byte hash differs: ${record.ledger.relativePath}`);
        assertions += 1;
      }
    }
  } finally {
    reader.close();
  }

  for (const ledger of ledgers) {
    const after = fs.readFileSync(ledger.absolutePath);
    assert.deepEqual(after, ledger.sourceBytes, `source ledger changed: ${ledger.relativePath}`);
    assert.equal(sha256(after), ledger.sha256, `source ledger hash changed: ${ledger.relativePath}`);
    assertions += 2;
  }

  const finishedAt = new Date();
  writeJson(resultPath, {
    schemaVersion: 'craft-wavedb-import-test-receipt.v1',
    verdict: 'pass',
    attemptId: 'wcli-20260805-node26-03',
    startedAt: startedAt.toISOString(),
    finishedAt: finishedAt.toISOString(),
    durationMs: finishedAt.getTime() - startedAt.getTime(),
    environment: { node: process.version, platform: process.platform, architecture: process.arch },
    dependency: { name: packageManifest.name, version: packageManifest.version, resolvedPackage },
    scope: {
      ledgerCount: ledgers.length,
      totalSourceBytes: ledgers.reduce((sum, ledger) => sum + ledger.sizeBytes, 0),
      excludedHistoricalOrStagedCopies: true,
      ledgers: manifest.ledgers
    },
    database: {
      storePath,
      recordCount: records.length,
      valueEncoding: 'utf-8 strings',
      writeMode: 'sequential-async-put',
      explicitFlushBeforeClose: true,
      immediateCompleteReadback: true,
      reopenedCompleteReadback: true,
      manifestSha256: sha256(records[0].value)
    },
    verification: {
      assertions,
      losslessUtf8Input: 'pass',
      completeImmediateReadback: 'pass',
      completeReadbackAfterReopen: 'pass',
      reconstructedLedgerByteHashes: 'pass',
      sourceImmutabilityBeforeAfter: 'pass'
    },
    authority: {
      source: '.craft/ledger.yml files named in the preserved scope file',
      wavedbRole: 'disposable derived read model',
      craftFilesMutated: false,
      rowLevelSemanticNormalizationAttempted: false,
      integrationAdmitted: false
    },
    priorAttempts: [
      { attemptId: 'wcli-20260805-node26-01', result: 'block', reason: '55-record atomic batch reopened with a null manifest' },
      { attemptId: 'wcli-20260805-node26-02', result: 'block', reason: 'binary-value type/readback assertion failed after reopen' }
    ],
    claimCeiling: '27 current owner Craft ledger YAML files were stored as lossless UTF-8 strings and read back exactly before and after reopen from one local WaveDB snapshot under Node 26; atomic batch persistence, row-level querying, and Craft runtime integration remain unproven'
  });
}

main().catch((error) => {
  if (resultPathArg) {
    try {
      writeJson(path.resolve(resultPathArg), {
        schemaVersion: 'craft-wavedb-import-test-receipt.v1',
        verdict: 'block',
        attemptId: 'wcli-20260805-node26-03',
        failedAt: new Date().toISOString(),
        environment: { node: process.version },
        error: { name: error && error.name, message: error && error.message, stack: error && error.stack }
      });
    } catch (writeError) {
      process.stderr.write(`${writeError.stack || writeError}\n`);
    }
  }
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
