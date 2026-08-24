'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');
const { openReadSession } = require('../src/read-session.cjs');

test('read failure invalidates one session and prevents a second database read', async () => {
  let reads = 0;
  let closes = 0;
  const fake = {
    async get() {
      reads += 1;
      throw Object.assign(new Error('injected read failure'), { code: 'INJECTED_READ_FAILURE' });
    },
    close() { closes += 1; }
  };
  const session = openReadSession({
    storePath: require('node:path').join(
      require('../src/constants.cjs').EXPERIMENT_ROOT,
      '.work/CWE-001/injected/store'
    ),
    acceptedReceipt: { scope: { ledgers: [] } },
    openDatabase: () => fake
  });
  const first = await session.verify();
  const second = await session.verify();
  assert.equal(first.ok, false);
  assert.equal(first.code, 'INJECTED_READ_FAILURE');
  assert.deepEqual(second, {
    ok: false,
    code: 'SESSION_INVALIDATED',
    message: 'session invalidated'
  });
  assert.equal(reads, 1);
  assert.equal(closes, 1);
});

test('original store is rejected before an opener is called', async () => {
  let opened = false;
  const constants = require('../src/constants.cjs');
  const session = openReadSession({
    storePath: constants.ORIGINAL_STORE,
    acceptedReceipt: { scope: { ledgers: [] } },
    openDatabase: () => { opened = true; }
  });
  const result = await session.status();
  assert.equal(result.ok, false);
  assert.equal(result.code, 'ORIGINAL_STORE_FORBIDDEN');
  assert.equal(opened, false);
});
