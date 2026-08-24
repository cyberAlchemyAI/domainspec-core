'use strict';

const path = require('node:path');
const { EXPERIMENT_ROOT, ORIGINAL_STORE, WAVEDB_MODULE } = require('./constants.cjs');
const manifest = require('./manifest.cjs');

function ensureIsolatedStore(storePath) {
  const resolved = path.resolve(storePath);
  const root = path.resolve(EXPERIMENT_ROOT);
  if (resolved === path.resolve(ORIGINAL_STORE)) {
    const error = new Error('accepted original store may not be opened');
    error.code = 'ORIGINAL_STORE_FORBIDDEN';
    throw error;
  }
  if (!(resolved === root || resolved.startsWith(`${root}${path.sep}`))) {
    const error = new Error('store path escapes experiment root');
    error.code = 'STORE_SCOPE_INVALID';
    throw error;
  }
  return resolved;
}

function defaultOpenDatabase(storePath) {
  const { WaveDB } = require(WAVEDB_MODULE);
  return new WaveDB(storePath);
}

function failure(code, message) {
  return { ok: false, code, message };
}

function openReadSession({ storePath, acceptedReceipt, openDatabase = defaultOpenDatabase }) {
  let state = 'active';
  let database;
  try {
    database = openDatabase(ensureIsolatedStore(storePath));
  } catch (error) {
    state = 'open-failed';
    return Object.freeze({
      async status() { return failure(error.code || 'SNAPSHOT_UNAVAILABLE', error.message); },
      async verify() { return failure(error.code || 'SNAPSHOT_UNAVAILABLE', error.message); },
      async listLedgers() { return failure(error.code || 'SNAPSHOT_UNAVAILABLE', error.message); },
      async getRaw() { return failure(error.code || 'SNAPSHOT_UNAVAILABLE', error.message); },
      close() {},
      get state() { return state; }
    });
  }

  function invalidate() {
    if (state === 'active') {
      state = 'invalidated';
      try { database.close(); } catch {}
    }
  }

  async function invoke(operation) {
    if (state === 'invalidated') return failure('SESSION_INVALIDATED', 'session invalidated');
    if (state === 'closed') return failure('SESSION_CLOSED', 'session closed');
    try {
      return { ok: true, value: await operation(database) };
    } catch (error) {
      invalidate();
      return failure(error.code || 'READ_FAILED', error.message);
    }
  }

  return Object.freeze({
    status() {
      return invoke(async (db) => {
        const { manifest: value } = await manifest.readManifest(db, acceptedReceipt);
        return {
          available: true,
          package: value.package,
          ledgerCount: value.ledgers.length,
          recordCount: EXPECTED_RECORD_COUNT(value)
        };
      });
    },
    verify() {
      return invoke((db) => manifest.verifySnapshot(db, acceptedReceipt));
    },
    listLedgers() {
      return invoke((db) => manifest.listLedgers(db, acceptedReceipt));
    },
    getRaw(ledgerPath) {
      return invoke((db) => manifest.getRaw(db, acceptedReceipt, ledgerPath));
    },
    close() {
      if (state === 'active') {
        state = 'closed';
        database.close();
      }
    },
    get state() { return state; }
  });
}

function EXPECTED_RECORD_COUNT(value) {
  return 1 + (value.ledgers.length * 2);
}

module.exports = { openReadSession };
