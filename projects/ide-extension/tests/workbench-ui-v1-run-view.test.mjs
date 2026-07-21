import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import { projectRunView, RUN_VIEW_STAGES, SUPPORTED_RUN_STATES } from '../src/ui/run-view.mjs';

const baseEnvelope = {
  schema_version: '2',
  envelope_id: 'env-run-view',
  run_id: 'run-run-view',
  approval: { approval_id: 'approval-run-view' },
  claim_id: null
};

function inputFor(state, overrides = {}) {
  return {
    envelope: { ...baseEnvelope, state, ...overrides.envelope },
    approval: { approval_id: 'approval-run-view', state: 'pending', ...overrides.approval },
    activeClaim: overrides.activeClaim || null,
    result: overrides.result || null,
    receipts: overrides.receipts || []
  };
}

test('projects every supported typestate into one truthful stage and label', () => {
  const expected = {
    awaiting_approval: ['prepared', 'Awaiting approval'],
    approved: ['approved', 'Approved - make available to poll'],
    ready_for_poll: ['available', 'Available to poll'],
    claimed: ['running', 'Running'],
    interrupted: ['interrupted', 'Interrupted - operator recovery required'],
    passed: ['receipt', 'Completed'],
    flagged: ['result', 'Completed with residue'],
    blocked: ['result', 'Blocked'],
    failed: ['result', 'Failed'],
    completed: ['result', 'Completed']
  };

  assert.deepEqual(SUPPORTED_RUN_STATES.length, Object.keys(expected).length);
  for (const state of SUPPORTED_RUN_STATES) {
    const overrides = state === 'passed'
      ? {
          result: { result_id: 'result-run-view', status: 'passed', summary: 'Admitted result' },
          receipts: [{ receipt_id: 'receipt-run-view', receipt_kind: 'skill.execution' }]
        }
      : state === 'flagged'
        ? { result: { result_id: 'result-run-view', status: 'flagged', summary: 'Named residue' } }
        : {};
    const view = projectRunView(inputFor(state, overrides));
    assert.equal(view.stage, expected[state][0], state);
    assert.equal(view.label, expected[state][1], state);
    assert.ok(RUN_VIEW_STAGES.includes(view.stage), state);
  }
});

test('derives only legal actions from the current state', () => {
  assert.deepEqual(projectRunView(inputFor('awaiting_approval')).legal_actions, ['approve', 'reject']);
  assert.deepEqual(projectRunView(inputFor('approved', { approval: { state: 'authorized' } })).legal_actions, ['ready', 'reject']);
  assert.deepEqual(projectRunView(inputFor('ready_for_poll', { approval: { state: 'authorized' } })).legal_actions, ['unready', 'reject']);
  assert.deepEqual(projectRunView(inputFor('claimed', {
    approval: { state: 'authorized' },
    activeClaim: { claim_id: 'claim-run-view', state: 'claimed', session_ref: 'session-run-view', assurance: 'unattested' }
  })).legal_actions, ['interrupt']);
  assert.deepEqual(projectRunView(inputFor('interrupted', {
    approval: { state: 'authorized' },
    activeClaim: { claim_id: 'claim-run-view', state: 'interrupted' }
  })).legal_actions, ['release']);
  for (const state of ['passed', 'flagged', 'blocked', 'failed', 'completed']) {
    assert.deepEqual(projectRunView(inputFor(state)).legal_actions, [], state);
  }
});

test('keeps claimed work separate from admitted result and exposes evidence handles', () => {
  const claimed = projectRunView(inputFor('claimed', {
    approval: { state: 'authorized' },
    activeClaim: { claim_id: 'claim-run-view', state: 'claimed' }
  }));
  assert.equal(claimed.stage, 'running');
  assert.equal(claimed.label, 'Running');
  assert.equal(claimed.result.result_id, null);
  assert.equal(claimed.evidence.available, false);

  const completed = projectRunView(inputFor('passed', {
    approval: { state: 'consumed' },
    result: {
      result_id: 'result-run-view',
      status: 'passed',
      summary: 'Admitted result',
      evidence_refs: ['result.json']
    },
    receipts: [{
      receipt_id: 'receipt-run-view',
      receipt_kind: 'skill.execution',
      evidence_refs: ['before.json', 'result.json']
    }]
  }));
  assert.equal(completed.stage, 'receipt');
  assert.equal(completed.evidence.available, true);
  assert.deepEqual(completed.evidence.receipt_ids, ['receipt-run-view']);
  assert.deepEqual(completed.evidence.evidence_refs, ['result.json', 'before.json']);
});

test('does not mutate raw input and has no DOM dependency', async () => {
  const raw = inputFor('claimed', {
    approval: { state: 'authorized' },
    activeClaim: { claim_id: 'claim-run-view', state: 'claimed' },
    receipts: [{ receipt_id: 'receipt-run-view', evidence_refs: ['before.json'] }]
  });
  const before = structuredClone(raw);
  const view = projectRunView(raw);
  assert.deepEqual(raw, before);
  assert.doesNotThrow(() => JSON.stringify(view));

  const source = await readFile(new URL('../src/ui/run-view.mjs', import.meta.url), 'utf8');
  assert.doesNotMatch(source, /\b(document|window)\b/);
});

test('unknown or missing state fails closed with no legal action', () => {
  const unknown = projectRunView({ envelope: { state: 'future_state' } });
  const missing = projectRunView();
  for (const view of [unknown, missing]) {
    assert.equal(view.stage, 'unknown');
    assert.equal(view.label, 'Unknown request state');
    assert.deepEqual(view.legal_actions, []);
  }
});
