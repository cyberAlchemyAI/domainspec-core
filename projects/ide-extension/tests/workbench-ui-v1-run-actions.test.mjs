import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import { resolveRunActions } from '../src/ui/run-actions.mjs';

const matrix = {
  awaiting_approval: {
    legal_actions: ['approve', 'reject'],
    primary: ['approve', 'command'],
    browser: ['approve', 'reject'],
    secondary: ['reject'],
    delegated: []
  },
  approved: {
    legal_actions: ['ready', 'reject'],
    primary: ['ready', 'command'],
    browser: ['ready', 'reject'],
    secondary: ['reject'],
    delegated: []
  },
  ready_for_poll: {
    legal_actions: ['unready', 'reject'],
    primary: ['available', 'status'],
    browser: ['unready', 'reject'],
    secondary: ['unready', 'reject'],
    delegated: []
  },
  claimed: {
    legal_actions: ['interrupt'],
    primary: ['running', 'status'],
    browser: [],
    secondary: [],
    delegated: ['interrupt']
  },
  interrupted: {
    legal_actions: ['release'],
    primary: ['review-interruption', 'status'],
    browser: ['release'],
    secondary: ['release'],
    delegated: []
  },
  passed: { legal_actions: [], primary: ['inspect', 'navigation'], browser: [], secondary: [], delegated: [] },
  flagged: { legal_actions: [], primary: ['inspect', 'navigation'], browser: [], secondary: [], delegated: [] },
  blocked: { legal_actions: [], primary: ['inspect', 'navigation'], browser: [], secondary: [], delegated: [] },
  failed: { legal_actions: [], primary: ['inspect', 'navigation'], browser: [], secondary: [], delegated: [] },
  completed: { legal_actions: [], primary: ['inspect', 'navigation'], browser: [], secondary: [], delegated: [] }
};

test('resolves one truthful primary affordance and legal browser commands per typestate', () => {
  for (const [typestate, expected] of Object.entries(matrix)) {
    const result = resolveRunActions({ typestate, legal_actions: expected.legal_actions });
    assert.deepEqual(
      [result.primary_action.id, result.primary_action.kind],
      expected.primary,
      typestate
    );
    assert.deepEqual(result.legal_actions, expected.legal_actions, typestate);
    assert.deepEqual(result.browser_commands, expected.browser, typestate);
    assert.deepEqual(result.secondary_actions, expected.secondary, typestate);
    assert.deepEqual(result.delegated_actions, expected.delegated, typestate);
    for (const action of result.browser_commands) {
      assert.ok(result.legal_actions.includes(action), `${typestate}: ${action} is legal`);
    }
  }
});

test('keeps terminal inspection separate from execution commands', () => {
  const result = resolveRunActions({
    typestate: 'passed',
    legal_actions: [],
    result: { result_id: 'result-1' }
  });
  assert.equal(result.terminal, true);
  assert.equal(result.primary_action.id, 'inspect');
  assert.deepEqual(result.browser_commands, []);
  assert.deepEqual(result.delegated_actions, []);
});

test('preserves claimant-owned interrupt as delegated and fails closed for unknown state', async () => {
  const claimed = resolveRunActions({ typestate: 'claimed', legal_actions: ['interrupt'] });
  assert.deepEqual(claimed.delegated_actions, ['interrupt']);
  assert.equal(resolveRunActions({ typestate: 'future_state', legal_actions: ['approve'] }).primary_action.id, 'none');

  const source = await readFile(new URL('../src/ui/run-actions.mjs', import.meta.url), 'utf8');
  assert.doesNotMatch(source, /\b(document|window)\b/);
});
