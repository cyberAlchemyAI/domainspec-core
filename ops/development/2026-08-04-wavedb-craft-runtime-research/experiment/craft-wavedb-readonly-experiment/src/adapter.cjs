'use strict';

const crypto = require('node:crypto');
const { EXPECTED } = require('./constants.cjs');
const { verifyPinnedInputs } = require('./identity.cjs');
const { openReadSession } = require('./read-session.cjs');

function unavailable(error) {
  return {
    status: 'unavailable',
    code: error.code || 'SNAPSHOT_UNAVAILABLE',
    message: error.message || String(error)
  };
}

async function withSession(storePath, operation) {
  let pinned;
  try {
    pinned = verifyPinnedInputs();
  } catch (error) {
    return unavailable(error);
  }
  const session = openReadSession({ storePath, acceptedReceipt: pinned.receipt });
  try {
    const result = await operation(session, pinned);
    if (!result.ok) return unavailable(result);
    return result.value;
  } finally {
    session.close();
  }
}

async function status(storePath) {
  return withSession(storePath, async (session) => {
    const result = await session.status();
    if (!result.ok) return result;
    return {
      ok: true,
      value: {
        status: 'ok',
        runtime: { node: process.version },
        dependency: { name: EXPECTED.packageName, version: EXPECTED.packageVersion },
        snapshot: result.value,
        store: { originalOpened: false, isolated: true }
      }
    };
  });
}

async function verify(storePath) {
  return withSession(storePath, async (session) => {
    const result = await session.verify();
    return result.ok
      ? { ok: true, value: { status: 'ok', verification: result.value } }
      : result;
  });
}

async function listLedgers(storePath) {
  return withSession(storePath, async (session) => {
    const result = await session.listLedgers();
    if (!result.ok) return result;
    return {
      ok: true,
      value: {
        status: 'ok',
        ledgers: [...result.value].sort((left, right) => left.path.localeCompare(right.path))
      }
    };
  });
}

async function getRaw(storePath, ledgerPath) {
  if (typeof ledgerPath !== 'string' || ledgerPath.length === 0) {
    return { status: 'not-found', code: 'NOT_FOUND', ledgerPath, bytes: undefined };
  }
  return withSession(storePath, async (session) => {
    const result = await session.getRaw(ledgerPath);
    if (!result.ok) return result;
    if (!result.value.ok) {
      return {
        ok: true,
        value: { status: 'not-found', code: 'NOT_FOUND', ledgerPath, bytes: undefined }
      };
    }
    const bytes = result.value.bytes;
    return {
      ok: true,
      value: {
        status: 'ok',
        ledger: result.value.ledger,
        bytes,
        sizeBytes: bytes.length,
        sha256: crypto.createHash('sha256').update(bytes).digest('hex')
      }
    };
  });
}

module.exports = Object.freeze({ status, verify, listLedgers, getRaw });
