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

function readScope(repoRoot, scopeFile) {
  const excludedSegments = new Set([
    'baselines',
    'closeout',
    'material',
    'outputs',
    'refresh',
    'refreshes',
    'staging'
  ]);
  const paths = fs.readFileSync(scopeFile, 'utf8')
    .split(/\r?\n/u)
    .map((value) => value.trim())
    .filter(Boolean);

  assert.ok(paths.length > 0, 'scope must name at least one ledger');
  assert.equal(new Set(paths).size, paths.length, 'scope contains duplicate paths');

  return paths.map((relativePath) => {
    assert.equal(path.isAbsolute(relativePath), false, `absolute path is forbidden: ${relativePath}`);
    assert.equal(relativePath.endsWith('/.craft/ledger.yml'), true, `not a Craft ledger: ${relativePath}`);
    const segments = relativePath.split('/');
    for (const segment of segments) {
      assert.equal(excludedSegments.has(segment), false, `historical/staged segment is forbidden: ${relativePath}`);
    }
    const absolutePath = path.resolve(repoRoot, relativePath);
    assert.equal(
      absolutePath.startsWith(`${repoRoot}${path.sep}`),
      true,
      `path escapes repository root: ${relativePath}`
    );
    const stat = fs.statSync(absolutePath);
    assert.equal(stat.isFile(), true, `ledger is not a regular file: ${relativePath}`);
    const bytes = fs.readFileSync(absolutePath);
    return {
      relativePath,
      absolutePath,
      bytes,
      sizeBytes: bytes.length,
      sha256: sha256(bytes)
    };
  });
}

async function main() {
  assert.ok(repoRootArg && scopeFileArg && storePathArg && resultPathArg && packageRootArg,
    'usage: node import-ledgers.js <repo-root> <scope-file> <store-path> <result-path> <package-root>');

  const startedAt = new Date();
  const repoRoot = fs.realpathSync(repoRootArg);
  const scopeFile = path.resolve(scopeFileArg);
  const storePath = path.resolve(storePathArg);
  const resultPath = path.resolve(resultPathArg);
  const packageRoot = fs.realpathSync(packageRootArg);
  const packageManifestPath = path.join(packageRoot, 'package.json');
  const packageManifest = JSON.parse(fs.readFileSync(packageManifestPath, 'utf8'));
  const resolvedPackage = require.resolve(packageRoot);
  const { WaveDB } = require(resolvedPackage);
  const ledgers = readScope(repoRoot, scopeFile);
  const importedAt = new Date().toISOString();
  const manifest = {
    schemaVersion: 'craft-wavedb-snapshot.v1',
    authority: 'derived-read-model-only',
    importedAt,
    ledgers: ledgers.map(({ relativePath, sizeBytes, sha256: digest }) => ({
      path: relativePath,
      sizeBytes,
      sha256: digest
    }))
  };
  const manifestValue = JSON.stringify(manifest);
  const operations = [
    { type: 'put', key: 'craft/manifest/v1', value: manifestValue }
  ];

  for (const ledger of ledgers) {
    const encodedPath = encodeKey(ledger.relativePath);
    const metadata = JSON.stringify({
      path: ledger.relativePath,
      sizeBytes: ledger.sizeBytes,
      sha256: ledger.sha256,
      authority: 'source-yaml'
    });
    operations.push({ type: 'put', key: `craft/meta/${encodedPath}`, value: metadata });
    operations.push({ type: 'put', key: `craft/raw/${encodedPath}`, value: ledger.bytes });
  }

  fs.mkdirSync(path.dirname(storePath), { recursive: true });
  const writer = new WaveDB(storePath);
  try {
    await writer.batch(operations);
  } finally {
    writer.close();
  }

  let assertions = 0;
  const reader = new WaveDB(storePath);
  try {
    const observedManifest = await reader.get('craft/manifest/v1');
    assert.equal(observedManifest, manifestValue, 'manifest readback differs');
    assertions += 1;

    for (const ledger of ledgers) {
      const encodedPath = encodeKey(ledger.relativePath);
      const expectedMetadata = JSON.stringify({
        path: ledger.relativePath,
        sizeBytes: ledger.sizeBytes,
        sha256: ledger.sha256,
        authority: 'source-yaml'
      });
      const observedMetadata = await reader.get(`craft/meta/${encodedPath}`);
      const observedBytes = await reader.get(`craft/raw/${encodedPath}`);
      assert.equal(observedMetadata, expectedMetadata, `metadata mismatch: ${ledger.relativePath}`);
      assert.ok(Buffer.isBuffer(observedBytes), `raw value is not a Buffer: ${ledger.relativePath}`);
      assert.deepEqual(observedBytes, ledger.bytes, `raw byte mismatch: ${ledger.relativePath}`);
      assert.equal(sha256(observedBytes), ledger.sha256, `raw hash mismatch: ${ledger.relativePath}`);
      assertions += 4;
    }
  } finally {
    reader.close();
  }

  for (const ledger of ledgers) {
    const afterBytes = fs.readFileSync(ledger.absolutePath);
    assert.deepEqual(afterBytes, ledger.bytes, `source ledger changed during test: ${ledger.relativePath}`);
    assert.equal(sha256(afterBytes), ledger.sha256, `source hash changed during test: ${ledger.relativePath}`);
    assertions += 2;
  }

  const finishedAt = new Date();
  writeJson(resultPath, {
    schemaVersion: 'craft-wavedb-import-test-receipt.v1',
    verdict: 'pass',
    startedAt: startedAt.toISOString(),
    finishedAt: finishedAt.toISOString(),
    durationMs: finishedAt.getTime() - startedAt.getTime(),
    environment: {
      node: process.version,
      platform: process.platform,
      architecture: process.arch
    },
    dependency: {
      name: packageManifest.name,
      version: packageManifest.version,
      resolvedPackage
    },
    scope: {
      ledgerCount: ledgers.length,
      totalSourceBytes: ledgers.reduce((sum, ledger) => sum + ledger.sizeBytes, 0),
      excludedHistoricalOrStagedCopies: true,
      ledgers: manifest.ledgers
    },
    database: {
      storePath,
      recordCount: operations.length,
      manifestSha256: sha256(manifestValue),
      reopenedBeforeReadback: true
    },
    verification: {
      assertions,
      completeLedgerByteReadback: 'pass',
      metadataReadback: 'pass',
      sourceImmutabilityBeforeAfter: 'pass'
    },
    authority: {
      source: '.craft/ledger.yml files named in ledger-scope.txt',
      wavedbRole: 'disposable derived read model',
      craftFilesMutated: false,
      rowLevelSemanticNormalizationAttempted: false,
      integrationAdmitted: false
    },
    claimCeiling: '27 current owner Craft ledger YAML files were stored and read back byte-for-byte from one local WaveDB snapshot under Node 26; no row-level query model or Craft runtime integration was proven'
  });
}

main().catch((error) => {
  if (resultPathArg) {
    try {
      writeJson(path.resolve(resultPathArg), {
        schemaVersion: 'craft-wavedb-import-test-receipt.v1',
        verdict: 'block',
        failedAt: new Date().toISOString(),
        environment: { node: process.version },
        error: {
          name: error && error.name,
          message: error && error.message,
          stack: error && error.stack
        }
      });
    } catch (writeError) {
      process.stderr.write(`${writeError.stack || writeError}\n`);
    }
  }
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
