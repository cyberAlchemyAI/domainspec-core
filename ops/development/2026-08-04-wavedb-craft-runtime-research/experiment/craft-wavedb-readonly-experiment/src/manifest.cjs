'use strict';

const { EXPECTED } = require('./constants.cjs');
const { sha256 } = require('./identity.cjs');

function encodeKey(value) {
  return Buffer.from(value, 'utf8').toString('base64url');
}

function observedBytes(value, key) {
  if (value === null || value === undefined) {
    const error = new Error(`missing record: ${key}`);
    error.code = 'RECORD_MISSING';
    throw error;
  }
  if (Buffer.isBuffer(value)) return value;
  if (typeof value === 'string') return Buffer.from(value, 'utf8');
  const error = new Error(`unexpected record type for ${key}`);
  error.code = 'RECORD_TYPE_INVALID';
  throw error;
}

function exactManifest(bytes, acceptedReceipt) {
  if (sha256(bytes) !== EXPECTED.manifestSha256) {
    const error = new Error('manifest SHA-256 mismatch');
    error.code = 'MANIFEST_INVALID';
    throw error;
  }
  let manifest;
  try {
    manifest = JSON.parse(bytes.toString('utf8'));
  } catch {
    const error = new Error('manifest JSON invalid');
    error.code = 'MANIFEST_INVALID';
    throw error;
  }
  const expectedLedgers = acceptedReceipt.scope.ledgers;
  if (
    manifest.schemaVersion !== 'craft-wavedb-snapshot.v2' ||
    manifest.authority !== 'derived-read-model-only' ||
    manifest.encoding !== 'utf-8' ||
    manifest.package?.name !== EXPECTED.packageName ||
    manifest.package?.version !== EXPECTED.packageVersion ||
    manifest.package?.tarballSha256 !== EXPECTED.tarballSha256 ||
    manifest.package?.addonSha256 !== EXPECTED.addonSha256 ||
    JSON.stringify(manifest.ledgers) !== JSON.stringify(expectedLedgers)
  ) {
    const error = new Error('manifest contract mismatch');
    error.code = 'MANIFEST_INVALID';
    throw error;
  }
  return manifest;
}

async function readManifest(db, acceptedReceipt) {
  const bytes = observedBytes(await db.get(EXPECTED.manifestKey), EXPECTED.manifestKey);
  return { bytes, manifest: exactManifest(bytes, acceptedReceipt) };
}

async function verifySnapshot(db, acceptedReceipt) {
  const { manifest } = await readManifest(db, acceptedReceipt);
  const records = [{ key: EXPECTED.manifestKey, kind: 'manifest' }];
  for (const ledger of manifest.ledgers) {
    const encoded = encodeKey(ledger.path);
    const metaKey = `craft/meta/${encoded}`;
    const rawKey = `craft/raw/${encoded}`;
    const metaBytes = observedBytes(await db.get(metaKey), metaKey);
    const expectedMeta = Buffer.from(JSON.stringify({
      path: ledger.path,
      sizeBytes: ledger.sizeBytes,
      sha256: ledger.sha256,
      encoding: 'utf-8',
      authority: 'source-yaml'
    }), 'utf8');
    if (!metaBytes.equals(expectedMeta)) {
      const error = new Error(`metadata mismatch: ${ledger.path}`);
      error.code = 'RECORD_INVALID';
      throw error;
    }
    const rawBytes = observedBytes(await db.get(rawKey), rawKey);
    if (rawBytes.length !== ledger.sizeBytes || sha256(rawBytes) !== ledger.sha256) {
      const error = new Error(`raw record mismatch: ${ledger.path}`);
      error.code = 'RECORD_INVALID';
      throw error;
    }
    records.push({ key: metaKey, kind: 'metadata' }, { key: rawKey, kind: 'raw' });
  }
  if (records.length !== EXPECTED.recordCount) {
    const error = new Error('record count mismatch');
    error.code = 'RECORD_INVALID';
    throw error;
  }
  return {
    manifestSha256: EXPECTED.manifestSha256,
    ledgerCount: manifest.ledgers.length,
    recordCount: records.length,
    recordsVerified: records.length
  };
}

async function listLedgers(db, acceptedReceipt) {
  const { manifest } = await readManifest(db, acceptedReceipt);
  return manifest.ledgers.map((ledger) => ({ ...ledger }));
}

async function getRaw(db, acceptedReceipt, ledgerPath) {
  const { manifest } = await readManifest(db, acceptedReceipt);
  const ledger = manifest.ledgers.find((item) => item.path === ledgerPath);
  if (!ledger) {
    return { ok: false, code: 'NOT_FOUND', ledgerPath };
  }
  const key = `craft/raw/${encodeKey(ledger.path)}`;
  const bytes = observedBytes(await db.get(key), key);
  if (bytes.length !== ledger.sizeBytes || sha256(bytes) !== ledger.sha256) {
    const error = new Error(`raw record mismatch: ${ledger.path}`);
    error.code = 'RECORD_INVALID';
    throw error;
  }
  return { ok: true, ledger: { ...ledger }, bytes };
}

module.exports = {
  encodeKey,
  getRaw,
  listLedgers,
  observedBytes,
  readManifest,
  verifySnapshot
};
