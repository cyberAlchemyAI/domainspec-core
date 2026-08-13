'use strict';

const adapter = require('./adapter.cjs');

const COMMANDS = new Set(['status', 'verify', 'list-ledgers', 'get-raw']);

function jsonValue(value) {
  if (value?.status === 'ok' && Buffer.isBuffer(value.bytes)) {
    const { bytes, ...rest } = value;
    return { ...rest, rawBase64: bytes.toString('base64') };
  }
  return value;
}

async function main() {
  const [command, storePath, ledgerPath, ...extra] = process.argv.slice(2);
  if (!COMMANDS.has(command) || !storePath || extra.length > 0) {
    process.stderr.write('usage: cli.cjs <status|verify|list-ledgers|get-raw> <isolated-store> [ledger-path]\n');
    process.exitCode = 2;
    return;
  }
  if ((command === 'get-raw') !== Boolean(ledgerPath)) {
    process.stderr.write('get-raw requires exactly one ledger path; other commands accept none\n');
    process.exitCode = 2;
    return;
  }
  const result = command === 'status'
    ? await adapter.status(storePath)
    : command === 'verify'
      ? await adapter.verify(storePath)
      : command === 'list-ledgers'
        ? await adapter.listLedgers(storePath)
        : await adapter.getRaw(storePath, ledgerPath);
  process.stdout.write(`${JSON.stringify(jsonValue(result))}\n`);
  if (result.status === 'unavailable') process.exitCode = 1;
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
