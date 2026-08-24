'use strict';

const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const [
  repoRootArg,
  baselineReceiptArg,
  storePathArg,
  resultPathArg,
  packageRootArg,
  diagnosticReceiptArg,
  tarballPathArg
] = process.argv.slice(2);

const ATTEMPT_ID = 'wcli-20260805-node26-0.15.9-01';
const EXPECTED = Object.freeze({
  node: 'v26.6.0',
  packageName: '@vijayee/wavedb',
  packageVersion: '0.15.9',
  ledgerCount: 27,
  recordCount: 55,
  baselineReceiptSha256: '97dd371843771bf752124fbe7d6cbc886d785128ab690dc31da48813d228810f',
  diagnosticReceiptSha256: '6243febc06f345d0fa22b8b1210742c19e7d4cda74ca6a840e36f8d32428918c',
  diagnosticTaskSessionSha256: 'eb07d1a14c4dacb30a272240057432c87f8acc430a6b064e0096f99e6107553c',
  tarballSha256: 'e8156c107117c8bc7f3394ceb16dff439c87c0cb4f8991033dad960b13ae396f',
  tarballSri: 'sha512-qoRqZUti9Rjs9UT4rj8cQKNv2Gdr8bJ25p6miU4dKojLeBMfzkgQqp+D/fd2PsaItXyhgMLrlx/wQUmyj/W8hA==',
  addonSha256: '4846a91117cfeaee42011e401e65448216d85c0ebd04fc860585e3a32e17bb3b'
});

const RELATIVE = Object.freeze({
  builder: `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/.work/${ATTEMPT_ID}/import-ledgers-byte-normalized.js`,
  store: `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/.work/${ATTEMPT_ID}/store`,
  receipt: `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/execution/${ATTEMPT_ID}/receipt.json`,
  diagnosticTaskSession: 'ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/source-build/npm-diagnostic/execution/task-sessions/SWU-WCND-002/terminal-receipt.json',
  apiRoot: 'implementation/domainspec/tools/craft-consultation-api'
});

function sha256(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function canonicalBytes(value) {
  return Buffer.from(JSON.stringify(value, Object.keys(value).sort()), 'utf8');
}

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, { flag: 'wx' });
}

function readJsonWithIdentity(filePath, expectedDigest, label) {
  const bytes = fs.readFileSync(filePath);
  assert.equal(sha256(bytes), expectedDigest, `${label} SHA-256 mismatch`);
  return JSON.parse(bytes.toString('utf8'));
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

function relativeToRepo(repoRoot, absolutePath) {
  const relative = path.relative(repoRoot, absolutePath).split(path.sep).join('/');
  assert.equal(relative.startsWith('../'), false, `path escapes repository: ${absolutePath}`);
  return relative;
}

function collectLedgerPaths(repoRoot) {
  const roots = ['arcanum', 'cyberAlchemy-v2', 'implementation', 'projects'];
  const excluded = new Set([
    '.git', 'baselines', 'closeout', 'material', 'node_modules', 'outputs',
    'refresh', 'refreshes', 'staging'
  ]);
  const found = [];

  function visit(directory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      if (entry.isSymbolicLink()) continue;
      const absolute = path.join(directory, entry.name);
      if (entry.isDirectory()) {
        if (excluded.has(entry.name)) continue;
        if (entry.name === '.craft') {
          const ledger = path.join(absolute, 'ledger.yml');
          if (fs.existsSync(ledger) && fs.statSync(ledger).isFile()) {
            found.push(relativeToRepo(repoRoot, ledger));
          }
          continue;
        }
        visit(absolute);
      }
    }
  }

  for (const root of roots) {
    const absolute = path.join(repoRoot, root);
    if (fs.existsSync(absolute) && fs.statSync(absolute).isDirectory()) visit(absolute);
  }
  return found.sort();
}

function loadLedgers(repoRoot, baselineReceipt) {
  const expectedLedgers = baselineReceipt.scope.ledgers;
  assert.equal(baselineReceipt.verdict, 'pass', 'baseline receipt is not passing');
  assert.equal(expectedLedgers.length, EXPECTED.ledgerCount, 'baseline ledger count mismatch');
  const expectedPaths = expectedLedgers.map((item) => item.path).sort();
  const observedPaths = collectLedgerPaths(repoRoot);
  assert.deepEqual(observedPaths, expectedPaths, 'current Craft ledger inventory differs from preserved baseline');

  return expectedLedgers.map((expected) => {
    const absolutePath = path.resolve(repoRoot, expected.path);
    const sourceBytes = fs.readFileSync(absolutePath);
    assert.equal(sourceBytes.length, expected.sizeBytes, `source size drift: ${expected.path}`);
    assert.equal(sha256(sourceBytes), expected.sha256, `source hash drift: ${expected.path}`);
    const text = sourceBytes.toString('utf8');
    assert.deepEqual(Buffer.from(text, 'utf8'), sourceBytes, `ledger is not lossless UTF-8: ${expected.path}`);
    return {
      relativePath: expected.path,
      absolutePath,
      sourceBytes,
      text,
      sizeBytes: sourceBytes.length,
      sha256: expected.sha256
    };
  });
}

function stringRecord(key, value, kind, ledger) {
  const expectedBytes = Buffer.from(value, 'utf8');
  return { key, value, kind, ledger, expectedBytes, sha256: sha256(expectedBytes) };
}

function treeSnapshot(rootPath, excludedPrefixes = []) {
  if (!fs.existsSync(rootPath)) return { state: 'absent', digest: null, fileCount: 0, totalBytes: 0 };
  const files = [];
  function visit(directory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const absolute = path.join(directory, entry.name);
      if (excludedPrefixes.some((prefix) => absolute === prefix || absolute.startsWith(`${prefix}${path.sep}`))) continue;
      if (entry.isSymbolicLink()) {
        const bytes = Buffer.from(fs.readlinkSync(absolute), 'utf8');
        files.push({ path: path.relative(rootPath, absolute), type: 'symlink', sizeBytes: bytes.length, sha256: sha256(bytes) });
      } else if (entry.isDirectory()) {
        visit(absolute);
      } else if (entry.isFile()) {
        const bytes = fs.readFileSync(absolute);
        files.push({ path: path.relative(rootPath, absolute), type: 'file', sizeBytes: bytes.length, sha256: sha256(bytes) });
      }
    }
  }
  if (fs.statSync(rootPath).isDirectory()) visit(rootPath);
  else {
    const bytes = fs.readFileSync(rootPath);
    files.push({ path: path.basename(rootPath), type: 'file', sizeBytes: bytes.length, sha256: sha256(bytes) });
  }
  files.sort((left, right) => left.path.localeCompare(right.path));
  return {
    state: 'present',
    digest: sha256(Buffer.from(JSON.stringify(files), 'utf8')),
    fileCount: files.length,
    totalBytes: files.reduce((sum, item) => sum + item.sizeBytes, 0)
  };
}

function gitSnapshot(repoRoot) {
  const gitDirectory = path.join(repoRoot, '.git');
  const headBytes = fs.readFileSync(path.join(gitDirectory, 'HEAD'));
  const indexPath = path.join(gitDirectory, 'index');
  return {
    headSha256: sha256(headBytes),
    indexSha256: fs.existsSync(indexPath) ? sha256(fs.readFileSync(indexPath)) : null
  };
}

function nvmDefaultSnapshot() {
  const defaultPath = '/home/vrondelli/.nvm/alias/default';
  if (!fs.existsSync(defaultPath)) return { state: 'absent', value: null };
  const value = fs.lstatSync(defaultPath).isSymbolicLink()
    ? fs.readlinkSync(defaultPath)
    : fs.readFileSync(defaultPath, 'utf8');
  return { state: 'present', value };
}

function scopeGuardSnapshot(repoRoot, storePath, resultPath) {
  const importRoot = path.join(repoRoot, 'ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import');
  const publicCraftRoots = [
    path.join(repoRoot, 'arcanum/arcana/craft'),
    path.join(repoRoot, 'arcanum/development/craft')
  ];
  const apiRoot = path.join(repoRoot, RELATIVE.apiRoot);
  const excluded = [path.dirname(storePath), path.dirname(resultPath)];
  return {
    git: gitSnapshot(repoRoot),
    nvmDefault: nvmDefaultSnapshot(),
    priorCraftImportEvidence: treeSnapshot(importRoot, excluded),
    publicCraft: publicCraftRoots.map((root) => ({ path: relativeToRepo(repoRoot, root), ...treeSnapshot(root) })),
    apiRoot: treeSnapshot(apiRoot)
  };
}

async function main() {
  assert.ok(
    repoRootArg && baselineReceiptArg && storePathArg && resultPathArg && packageRootArg && diagnosticReceiptArg && tarballPathArg,
    'usage: node import-ledgers-byte-normalized.js <repo-root> <baseline-receipt> <store-path> <result-path> <package-root> <diagnostic-receipt> <tarball>'
  );
  assert.equal(process.version, EXPECTED.node, 'unexpected Node runtime');

  const startedAt = new Date();
  const repoRoot = fs.realpathSync(repoRootArg);
  const baselineReceiptPath = path.resolve(baselineReceiptArg);
  const storePath = path.resolve(storePathArg);
  const resultPath = path.resolve(resultPathArg);
  const packageRoot = fs.realpathSync(packageRootArg);
  const diagnosticReceiptPath = path.resolve(diagnosticReceiptArg);
  const tarballPath = path.resolve(tarballPathArg);
  assert.equal(relativeToRepo(repoRoot, __filename), RELATIVE.builder, 'builder path does not match admitted target');
  assert.equal(relativeToRepo(repoRoot, storePath), RELATIVE.store, 'store path does not match admitted target');
  assert.equal(relativeToRepo(repoRoot, resultPath), RELATIVE.receipt, 'receipt path does not match admitted target');
  assert.equal(fs.existsSync(storePath), false, 'immutable attempt store already exists');
  assert.equal(fs.existsSync(resultPath), false, 'immutable attempt receipt already exists');

  const baselineReceipt = readJsonWithIdentity(
    baselineReceiptPath, EXPECTED.baselineReceiptSha256, 'baseline receipt'
  );
  const diagnosticReceipt = readJsonWithIdentity(
    diagnosticReceiptPath, EXPECTED.diagnosticReceiptSha256, 'diagnostic receipt'
  );
  const diagnosticTaskSessionPath = path.join(repoRoot, RELATIVE.diagnosticTaskSession);
  const diagnosticTaskSession = readJsonWithIdentity(
    diagnosticTaskSessionPath, EXPECTED.diagnosticTaskSessionSha256, 'diagnostic Task Session receipt'
  );
  assert.equal(diagnosticReceipt.executionResult, 'pass', 'diagnostic receipt is not passing');
  assert.equal(diagnosticTaskSession.execution_result, 'pass', 'diagnostic Task Session did not pass');
  assert.equal(diagnosticReceipt.artifact.specifier, `${EXPECTED.packageName}@${EXPECTED.packageVersion}`);
  assert.equal(diagnosticReceipt.artifact.sha256, EXPECTED.tarballSha256);
  assert.equal(diagnosticReceipt.artifact.sri, EXPECTED.tarballSri);
  assert.equal(diagnosticReceipt.environment.node, EXPECTED.node);
  assert.equal(sha256(fs.readFileSync(tarballPath)), EXPECTED.tarballSha256, 'tarball SHA-256 mismatch');

  const packageManifest = JSON.parse(fs.readFileSync(path.join(packageRoot, 'package.json'), 'utf8'));
  assert.equal(packageManifest.name, EXPECTED.packageName);
  assert.equal(packageManifest.version, EXPECTED.packageVersion);
  const addonPath = path.join(packageRoot, 'build/Release/wavedb.node');
  assert.equal(sha256(fs.readFileSync(addonPath)), EXPECTED.addonSha256, 'native addon SHA-256 mismatch');
  const resolvedPackage = require.resolve(packageRoot);
  const { WaveDB } = require(resolvedPackage);

  const beforeGuards = scopeGuardSnapshot(repoRoot, storePath, resultPath);
  const ledgers = loadLedgers(repoRoot, baselineReceipt);
  const manifest = {
    schemaVersion: 'craft-wavedb-snapshot.v2',
    authority: 'derived-read-model-only',
    encoding: 'utf-8',
    importedAt: new Date().toISOString(),
    package: {
      name: EXPECTED.packageName,
      version: EXPECTED.packageVersion,
      tarballSha256: EXPECTED.tarballSha256,
      addonSha256: EXPECTED.addonSha256
    },
    ledgers: ledgers.map((ledger) => ({
      path: ledger.relativePath,
      sizeBytes: ledger.sizeBytes,
      sha256: ledger.sha256
    }))
  };
  const records = [stringRecord('craft/manifest/v2', JSON.stringify(manifest), 'manifest')];
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
  assert.equal(ledgers.length, EXPECTED.ledgerCount);
  assert.equal(records.length, EXPECTED.recordCount);

  fs.mkdirSync(path.dirname(storePath), { recursive: true });
  let assertions = 0;
  const immediateTypes = { string: 0, buffer: 0 };
  const reopenedTypes = { string: 0, buffer: 0 };
  const writer = new WaveDB(storePath);
  try {
    for (const record of records) await writer.put(record.key, record.value);
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
  assert.deepEqual(collectLedgerPaths(repoRoot), manifest.ledgers.map((item) => item.path).sort());

  const afterGuards = scopeGuardSnapshot(repoRoot, storePath, resultPath);
  assert.deepEqual(afterGuards, beforeGuards, 'a protected scope changed during snapshot construction');
  const finishedAt = new Date();
  writeJson(resultPath, {
    schemaVersion: 'craft-wavedb-import-test-receipt.v2',
    verdict: 'pass',
    attemptId: ATTEMPT_ID,
    startedAt: startedAt.toISOString(),
    finishedAt: finishedAt.toISOString(),
    durationMs: finishedAt.getTime() - startedAt.getTime(),
    environment: { node: process.version, platform: process.platform, architecture: process.arch },
    dependency: {
      name: packageManifest.name,
      version: packageManifest.version,
      resolvedPackage,
      tarballSha256: EXPECTED.tarballSha256,
      tarballSri: EXPECTED.tarballSri,
      addonSha256: EXPECTED.addonSha256
    },
    dependencyReceipts: {
      diagnostic: { path: relativeToRepo(repoRoot, diagnosticReceiptPath), sha256: EXPECTED.diagnosticReceiptSha256 },
      diagnosticTaskSession: { path: RELATIVE.diagnosticTaskSession, sha256: EXPECTED.diagnosticTaskSessionSha256 },
      scopeBaseline: { path: relativeToRepo(repoRoot, baselineReceiptPath), sha256: EXPECTED.baselineReceiptSha256 }
    },
    scope: {
      ledgerCount: ledgers.length,
      totalSourceBytes: ledgers.reduce((sum, ledger) => sum + ledger.sizeBytes, 0),
      exactBaselineInventory: true,
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
      manifestKey: 'craft/manifest/v2',
      manifestSha256: records[0].sha256,
      storeTree: treeSnapshot(storePath)
    },
    verification: {
      assertions,
      packageIdentity: 'pass',
      exactSourceInventory: 'pass',
      losslessUtf8Input: 'pass',
      completeImmediateByteReadback: 'pass',
      completeByteReadbackAfterReopen: 'pass',
      sourceImmutabilityBeforeAfter: 'pass',
      protectedScopeImmutability: 'pass'
    },
    scopeGuards: { before: beforeGuards, after: afterGuards, equal: true },
    authority: {
      source: '.craft/ledger.yml files named in the preserved baseline receipt',
      wavedbRole: 'disposable derived read model',
      craftFilesMutated: false,
      rowLevelSemanticNormalizationAttempted: false,
      apiCodeMutated: false,
      integrationAdmitted: false,
      publication: false,
      deployment: false
    },
    closeout: {
      synchronizationRequired: true,
      nextOwner: 'invoke:refresh:apply-approved',
      successorAdmitted: false
    },
    claimCeiling: 'One local @vijayee/wavedb@0.15.9 derived snapshot stored the exact 27-ledger/55-record baseline and passed byte-exact immediate and same-process reopen checks under Node v26.6.0; fresh-process reads and Craft API integration remain unproven.'
  });
}

main().catch((error) => {
  if (resultPathArg) {
    const resultPath = path.resolve(resultPathArg);
    if (!fs.existsSync(resultPath)) {
      try {
        writeJson(resultPath, {
          schemaVersion: 'craft-wavedb-import-test-receipt.v2',
          verdict: 'block',
          attemptId: ATTEMPT_ID,
          failedAt: new Date().toISOString(),
          environment: { node: process.version },
          error: { name: error && error.name, message: error && error.message, stack: error && error.stack },
          successorAdmitted: false
        });
      } catch (writeError) {
        process.stderr.write(`${writeError.stack || writeError}\n`);
      }
    }
  }
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
