'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { EXPECTED, EXPERIMENT_ROOT } = require('../src/constants.cjs');
const { verifyPinnedInputs } = require('../src/identity.cjs');

const MAXIMUM_CLAIM = 'A repeatable checkout-local, read-only experiment independently accessed the accepted derived Craft snapshot without changing canonical source or accepted store bytes.';

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(EXPERIMENT_ROOT, relativePath), 'utf8'));
}

function assertAllFalse(value, label) {
  assert.equal(value && typeof value === 'object' && !Array.isArray(value), true, `${label} must be an object`);
  for (const [key, observed] of Object.entries(value)) {
    assert.equal(observed, false, `${label}.${key} must be false`);
  }
  assert.equal(Object.keys(value).length > 0, true, `${label} must not be empty`);
}

function validateNodeReceipt(unit) {
  const receipt = readJson(`execution/${unit}/receipt.json`);
  assert.equal(receipt.schemaVersion, 'craft-wavedb-readonly-node-receipt.v1');
  assert.equal(receipt.unit, unit);
  assert.equal(receipt.verdict, 'pass');
  assert.equal(receipt.environment.node, EXPECTED.nodeVersion);
  assert.deepEqual(receipt.blockers, []);
  assertAllFalse(receipt.forbiddenEffects, `${unit}.forbiddenEffects`);
  const expectedSuccessor = unit === 'CWE-001' ? 'CWE-002' : unit === 'CWE-002' ? 'CWE-003' : null;
  assert.equal(receipt.successor, expectedSuccessor);
  return receipt;
}

function validateTaskTerminal(unit, required) {
  const relative = `execution/${unit}/task-session-terminal.json`;
  const absolute = path.join(EXPERIMENT_ROOT, relative);
  if (!fs.existsSync(absolute)) {
    assert.equal(required, false, `${unit} Task Session terminal is missing`);
    return null;
  }
  const receipt = readJson(relative);
  assert.equal(receipt.schemaVersion, 'craft-wavedb-task-session-terminal.v1');
  assert.equal(receipt.taskId, `TASK-${unit}`);
  assert.equal(receipt.swuId, unit);
  assert.equal(receipt.unit, unit);
  assert.equal(receipt.result, 'pass');
  assert.equal(receipt.authorityEffect, 'none');
  assertAllFalse(receipt.forbiddenEffects, `${unit}.taskSession.forbiddenEffects`);
  const expectedSuccessor = unit === 'CWE-001' ? 'CWE-002' : unit === 'CWE-002' ? 'CWE-003' : null;
  assert.equal(receipt.successor, expectedSuccessor);
  return receipt;
}

function validateTerminalSchema() {
  const schema = readJson('schemas/terminal-receipt.schema.json');
  assert.equal(schema.$schema, 'https://json-schema.org/draft/2020-12/schema');
  assert.equal(schema.type, 'object');
  assert.equal(schema.additionalProperties, false);
  assert.equal(schema.properties.schemaVersion.const, 'craft-wavedb-readonly-experiment-terminal.v1');
  return schema;
}

function main() {
  const nodes = ['CWE-001', 'CWE-002', 'CWE-003'].map(validateNodeReceipt);
  const taskTerminals = [
    validateTaskTerminal('CWE-001', true),
    validateTaskTerminal('CWE-002', true),
    validateTaskTerminal('CWE-003', false)
  ].filter(Boolean);
  validateTerminalSchema();
  const terminal = readJson('execution/terminal-receipt.json');
  assert.equal(terminal.schemaVersion, 'craft-wavedb-readonly-experiment-terminal.v1');
  assert.equal(terminal.experiment, 'craft-wavedb-readonly-experiment');
  assert.equal(terminal.workPackId, 'WP-CWE-20260806');
  assert.equal(terminal.result, 'pass');
  assert.deepEqual(terminal.completedUnits, ['CWE-001', 'CWE-002', 'CWE-003']);
  assert.equal(terminal.evidenceRefs.length, 5);
  for (const reference of terminal.evidenceRefs) {
    const bytes = fs.readFileSync(path.join(EXPERIMENT_ROOT, reference.path));
    assert.equal(require('node:crypto').createHash('sha256').update(bytes).digest('hex'), reference.sha256);
    assert.equal(bytes.length, reference.sizeBytes);
  }
  assert.equal(terminal.finalIdentity.acceptedReceiptSha256, EXPECTED.acceptedReceiptSha256);
  assert.equal(terminal.finalIdentity.canonicalLedgerCount, EXPECTED.ledgerCount);
  assert.equal(terminal.finalIdentity.canonicalSourceBytes, EXPECTED.totalSourceBytes);
  assert.equal(terminal.finalIdentity.originalStoreDigest, EXPECTED.storeDigest);
  assert.equal(terminal.finalIdentity.originalStoreFileCount, EXPECTED.storeFileCount);
  assert.equal(terminal.finalIdentity.originalStoreTotalBytes, EXPECTED.storeTotalBytes);
  assert.equal(terminal.maximumClaim, MAXIMUM_CLAIM);
  assertAllFalse(terminal.forbiddenSuccessors, 'terminal.forbiddenSuccessors');
  assertAllFalse(terminal.forbiddenEffects, 'terminal.forbiddenEffects');
  assert.equal(terminal.successor, null);
  assert.equal(terminal.authorityEffect, 'none');
  assert.deepEqual(terminal.blockers, []);
  const pinned = verifyPinnedInputs();
  assert.equal(pinned.store.digest, EXPECTED.storeDigest);
  process.stdout.write(`${JSON.stringify({
    result: 'pass',
    validatedNodeReceipts: nodes.length,
    validatedTaskSessionTerminals: taskTerminals.length,
    cwe003TaskSessionTerminalPending: taskTerminals.length === 2,
    validatedExperimentTerminal: true,
    finalInputsUnchanged: true
  })}\n`);
}

try {
  main();
} catch (error) {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
}
