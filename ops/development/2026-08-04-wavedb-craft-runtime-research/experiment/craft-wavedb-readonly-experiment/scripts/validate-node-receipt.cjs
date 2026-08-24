'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');

const [receiptPath, expectedUnit] = process.argv.slice(2);
assert.ok(receiptPath && expectedUnit, 'usage: validate-node-receipt.cjs <receipt> <unit>');
const receipt = JSON.parse(fs.readFileSync(receiptPath, 'utf8'));
assert.equal(receipt.schemaVersion, 'craft-wavedb-readonly-node-receipt.v1');
assert.equal(receipt.unit, expectedUnit);
assert.equal(receipt.verdict, 'pass');
assert.deepEqual(receipt.blockers, []);
assert.equal(receipt.environment.node, 'v26.6.0');
assert.equal(receipt.checks.canonicalLedgersUnchanged, true);
assert.equal(receipt.checks.originalStoreUnchanged, true);
for (const value of Object.values(receipt.forbiddenEffects)) assert.equal(value, false);
if (expectedUnit === 'CWE-003') assert.equal(receipt.successor, null);
else assert.match(receipt.successor, /^CWE-00[23]$/);
process.stdout.write(`validated ${expectedUnit}\n`);
