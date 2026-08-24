import test from 'node:test';
import assert from 'node:assert/strict';
import { createCapabilityAdapters } from '../src/capability-adapters.mjs';

const capabilities = [
  ['animejs-knowledge-consult-read', 'animejs-knowledge-consult-request/0.1.0', 'consult'],
  ['animejs-work-episode-append', 'animejs-work-episode-command/0.1.0', 'append'],
  ['animejs-work-episode-receipt-read', 'animejs-work-episode-receipt-request/0.1.0', 'receipt'],
  ['animejs-work-episode-project-read', 'animejs-work-episode-project-request/0.1.0', 'project'],
];
const hostContext = { principal_id: 'principal:1', tenant_or_workspace_id: 'workspace:1', capabilities: [], policy_epoch: 'policy:1', vault_scope: 'animejs-agent-knowledge-vault', request_id: 'request:1', received_at: '2026-08-05T00:00:00Z' };

function harness({ authorized = true } = {}) {
  const calls = { authorize: 0, consult: 0, append: 0, receipt: 0, project: 0 };
  const audits = [];
  const adapters = createCapabilityAdapters({
    authorize: async () => { calls.authorize += 1; return { authorized, views: ['documentation'], limits: { max_results: 12, max_hops: 2, max_response_bytes: 65536 } }; },
    consultationService: { consult: async () => { calls.consult += 1; return { status: 'ok' }; } },
    episodeService: {
      appendCommand: async () => { calls.append += 1; return { status: 'accepted' }; },
      recoverReceipt: async () => { calls.receipt += 1; return { status: 'accepted' }; },
    },
    projectReader: { read: async () => { calls.project += 1; return { status: 'current', project: {} }; } },
    audit: async row => { audits.push(row); },
  });
  return { adapters, calls, audits };
}

function body(contract, kind) {
  if (kind === 'consult') return { contract, operation: 'search', query: { text: '', node_ids: [], task_id: null, episode_id: null, version_context_id: null, relation_types: [], evidence_states: [] }, limits: { max_results: 1, max_hops: 0, max_response_bytes: 1024 }, expected: { graph_digest: null, projection_digest: null } };
  if (kind === 'append') return { contract, command_id: 'cmd:1', idempotency_key: 'idem:1', operation: 'close_episode', episode_id: 'episode:1', expected_revision: 1, expected_graph_digest: 'a'.repeat(64), payload: { disposition: 'blocked' } };
  if (kind === 'receipt') return { contract, recovery_handle: 'recovery:opaque' };
  return { contract, episode_id: 'episode:1' };
}

test('four exact capability audiences route only to their named port', async () => {
  for (const [capability, contract, kind] of capabilities) {
    const h = harness();
    const result = await h.adapters.invoke({ descriptor: { capability }, credential: { audience: capability }, hostContext, body: body(contract, kind) });
    assert.equal(['ok', 'accepted', 'current'].includes(result.status), true, capability);
    assert.equal(h.calls[kind], 1, capability);
    assert.equal(Object.entries(h.calls).filter(([key, value]) => !['authorize', kind].includes(key) && value !== 0).length, 0, capability);
    assert.equal(h.audits[0].dimension, kind);
  }
});

test('complete cross-audience matrix denies before service dispatch', async () => {
  for (const [routeCapability, contract, kind] of capabilities) {
    for (const [credentialCapability] of capabilities) {
      if (credentialCapability === routeCapability) continue;
      const h = harness();
      const result = await h.adapters.invoke({ descriptor: { capability: routeCapability }, credential: { audience: credentialCapability }, hostContext, body: body(contract, kind) });
      assert.equal(result.status, 'denied');
      assert.deepEqual(h.calls, { authorize: 0, consult: 0, append: 0, receipt: 0, project: 0 });
    }
  }
});

test('append body under read token is denied with zero journal and projection calls', async () => {
  const h = harness();
  const result = await h.adapters.invoke({ descriptor: { capability: 'animejs-knowledge-consult-read' }, credential: { audience: 'animejs-knowledge-consult-read' }, hostContext, body: body('animejs-work-episode-command/0.1.0', 'append') });
  assert.equal(result.status, 'denied');
  assert.deepEqual(h.calls, { authorize: 1, consult: 0, append: 0, receipt: 0, project: 0 });
});

test('foreign target probe is denied before target parsing and leaks nothing', async () => {
  const h = harness({ authorized: false });
  const target = 'episode:foreign-secret';
  const result = await h.adapters.invoke({ descriptor: { capability: 'animejs-work-episode-append' }, credential: { audience: 'animejs-work-episode-append' }, hostContext, body: { ...body('animejs-work-episode-command/0.1.0', 'append'), episode_id: target } });
  assert.equal(result.status, 'denied');
  assert.equal(h.calls.append, 0);
  assert.equal(JSON.stringify(result).includes(target), false);
});

test('wildcard, generic, unknown, and body-directed grants cannot dispatch', async () => {
  for (const audience of ['*', 'animejs-*', 'generic']) {
    const h = harness();
    const result = await h.adapters.invoke({ descriptor: { capability: 'animejs-work-episode-append' }, credential: { audience }, hostContext, body: body('animejs-work-episode-command/0.1.0', 'append') });
    assert.equal(result.status, 'denied', audience);
    assert.equal(h.calls.authorize, 0, audience);
  }
  const unknown = harness();
  assert.equal((await unknown.adapters.invoke({ descriptor: { capability: 'body-selected' }, credential: { audience: 'body-selected' }, hostContext, body: { contract: 'body-selected' } })).status, 'denied');
  assert.equal(unknown.calls.authorize, 0);
});

test('host field spoofing fails after authorization but before service dispatch', async () => {
  const h = harness();
  const result = await h.adapters.invoke({ descriptor: { capability: 'animejs-work-episode-append' }, credential: { audience: 'animejs-work-episode-append' }, hostContext, body: { ...body('animejs-work-episode-command/0.1.0', 'append'), principal_id: 'self' } });
  assert.equal(result.status, 'invalid_request');
  assert.equal(h.calls.append, 0);
});

test('receipt and project bodies are closed before target dispatch', async () => {
  for (const [capability, contract, kind] of capabilities.filter(([, , candidate]) => ['receipt', 'project'].includes(candidate))) {
    const h = harness();
    const result = await h.adapters.invoke({ descriptor: { capability }, credential: { audience: capability }, hostContext, body: { ...body(contract, kind), unexpected: true } });
    assert.equal(result.status, 'invalid_request', kind);
    assert.equal(h.calls[kind], 0, kind);
  }
});

test('project read normalizes unknown reducer state to a closed failure', async () => {
  const calls = { project: 0 };
  const adapters = createCapabilityAdapters({
    authorize: async () => ({ authorized: true }),
    consultationService: { consult: async () => ({ status: 'ok' }) },
    episodeService: { appendCommand: async () => ({ status: 'accepted' }), recoverReceipt: async () => ({ status: 'accepted' }) },
    projectReader: { read: async () => { calls.project += 1; return { status: 'mystery' }; } },
  });
  const result = await adapters.invoke({ descriptor: { capability: 'animejs-work-episode-project-read' }, credential: { audience: 'animejs-work-episode-project-read' }, hostContext, body: body('animejs-work-episode-project-request/0.1.0', 'project') });
  assert.deepEqual([result.status, result.diagnostic.code, calls.project], ['temporary_failure', 'PROJECTION_CORRUPT', 1]);
});
