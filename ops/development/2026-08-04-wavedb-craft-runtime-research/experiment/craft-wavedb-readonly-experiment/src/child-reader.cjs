'use strict';

const { EXPECTED } = require('./constants.cjs');
const { openReadSession } = require('./read-session.cjs');
const { verifyPinnedInputs } = require('./identity.cjs');

async function main() {
  const storePath = process.argv[2];
  if (!storePath) throw new Error('usage: child-reader.cjs <isolated-store>');
  const pinned = verifyPinnedInputs();
  const session = openReadSession({ storePath, acceptedReceipt: pinned.receipt });
  const result = await session.verify();
  session.close();
  if (!result.ok) throw new Error(`${result.code}: ${result.message}`);
  if (
    result.value.ledgerCount !== EXPECTED.ledgerCount ||
    result.value.recordCount !== EXPECTED.recordCount
  ) {
    throw new Error('verified counts mismatch');
  }
  process.stdout.write(`${JSON.stringify({
    schemaVersion: 'craft-wavedb-fresh-reader.v1',
    verdict: 'pass',
    pid: process.pid,
    storePath,
    ...result.value
  })}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
