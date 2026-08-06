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

function observedBytes(value, key, typeCounts) {
  assert.notEqual(value, null, `missing database value: ${key}`);
  if (Buffer.isBuffer(value)) {
    typeCounts.buffer += 1;
    return value;
  }
  assert.equal(typeof value, 'string', `unexpected database value type: ${key}`);
  typeCounts.string += 1;
  return Buffer.from(value, 'utf8');
}

function verifyValue(observed, record, phase, typeCounts) {
  const actual = observedBytes(observed, record.key, typeCounts);
  assert.equal(actual.length, record.expectedBytes.length, `${phase} size mismatch: ${record.key}`);
  assert.equal(sha256(actual), record.sha256, `${phase} hash mismatch: ${record.key}`);
  assert.deepEqual(actual, record.expectedBytes, `${phase} bytes differ: ${record.key}`);
  return 3;
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

function stringRecord(key, value, kind, ledger) {
  const expectedBytes = Buffer.from(value, 'utf8');
  return { key, value, kind, ledger, expectedBytes, sha256: sha256(expectedBytes) };
}

async function main() {
  assert.ok(repoRootArg && scopeFileArg && storePathArg && resultPathArg && packageRootArg,
    'usage: node import-ledgers-byte-normalized.js <repo-root> <scope-file> <store-path> <result-path> <package-root>');
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
  const records = [stringRecord('craft/manifest/v1', JSON.stringify(manifest), 'manifest')];
  for (const ledger of ledgers) {
    const encodedPath = encodeKey(ledger.relativePath);
    records.push(stringRecord(
      `craft/meta/${encodedPath}`,
      JSON.stringify({
        path: ledger.relativePath,
        sizeBytes: ledger.sizeBytes,
        sha256: ledger.sha256,
        encoding: 'utf-8',
        authority: 'source-yaml'
      }),
      'metadata',
      ledger
    ));
    records.push(stringRecord(`craft/raw/${encodedPath}`, ledger.text, 'ledger', ledger));
  }

  fs.mkdirSync(path.dirname(storePath), { recursive: true });
  let assertions = 0;
  const immediateTypes = { string: 0, buffer: 0 };
  const reopenedTypes = { string: 0, buffer: 0 };
  const writer = new WaveDB(storePath);
  try {
    for (const record of records) {
      await writer.put(record.key, record.value);
    }
    writer.flush();
    for (const record of records) {
      assertions += verifyValue(await writer.get(record.key), record, 'immediate', immediateTypes);
    }
  } finally {
    writer.close();
  }

  const reader = new WaveDB(storePath);
  try {
    for (const record of records) {
      assertions += verifyValue(await reader.get(record.key), record, 'reopened', reopenedTypes);
    }
  } finally {
    reader.close();
  }

  for (const ledger of ledgers) {
    const after = fs.readFileSync(ledger.absolutePath);
    assert.equal(after.length, ledger.sizeBytes, `source ledger size changed: ${ledger.relativePath}`);
    assert.equal(sha256(after), ledger.sha256, `source ledger hash changed: ${ledger.relativePath}`);
    assert.deepEqual(after, ledger.sourceBytes, `source ledger bytes changed: ${ledger.relativePath}`);
    assertions += 3;
  }

  const finishedAt = new Date();
  writeJson(resultPath, {
    schemaVersion: 'craft-wavedb-import-test-receipt.v1',
    verdict: 'pass',
    attemptId: 'wcli-20260805-node26-04',
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
      inputEncoding: 'utf-8 strings',
      readbackNormalization: 'string-or-buffer to exact bytes',
      observedTypes: { immediate: immediateTypes, reopened: reopenedTypes },
      writeMode: 'sequential-async-put',
      explicitFlushBeforeClose: true,
      immediateCompleteReadback: true,
      reopenedCompleteReadback: true,
      manifestSha256: records[0].sha256
    },
    verification: {
      assertions,
      losslessUtf8Input: 'pass',
      completeImmediateByteReadback: 'pass',
      completeByteReadbackAfterReopen: 'pass',
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
      { attemptId: 'wcli-20260805-node26-02', result: 'block', reason: 'strict Buffer assertion failed after reopen' },
      { attemptId: 'wcli-20260805-node26-03', result: 'block', reason: 'strict string assertion failed because WaveDB returned a Buffer for a large string value' }
    ],
    claimCeiling: '27 current owner Craft ledger YAML files were stored sequentially and read back byte-for-byte before and after reopen from one local WaveDB snapshot under Node 26; atomic batch persistence, row-level querying, and Craft runtime integration remain unproven'
  });
}

main().catch((error) => {
  if (resultPathArg) {
    try {
      writeJson(path.resolve(resultPathArg), {
        schemaVersion: 'craft-wavedb-import-test-receipt.v1',
        verdict: 'block',
        attemptId: 'wcli-20260805-node26-04',
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
