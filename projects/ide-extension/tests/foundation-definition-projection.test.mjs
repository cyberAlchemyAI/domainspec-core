import assert from 'node:assert/strict';
import { mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { createServer } from '../src/server.mjs';
import { executeFoundationClaim } from '../src/adapters/foundation.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const foundationRoot = path.resolve(projectRoot, '../../../cyberalchemy-foundation');

function listen(server) {
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server.address().port)));
}

function close(server) {
  return new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}

async function requestJson(base, route, options = {}) {
  const response = await fetch(`${base}${route}`, {
    ...options,
    headers: { 'content-type': 'application/json', ...(options.headers || {}) }
  });
  return { response, body: JSON.parse(await response.text()) };
}

function postJson(base, route, body = {}) {
  return requestJson(base, route, { method: 'POST', body: JSON.stringify(body) });
}

async function withServer(run) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'foundation-projection-'));
  const server = createServer({ rootDir: projectRoot, stateDir, foundationRoot });
  await server.ready;
  const port = await listen(server);
  try {
    await run(`http://127.0.0.1:${port}`);
  } finally {
    await close(server);
    await rm(stateDir, { recursive: true, force: true });
  }
}

async function claimedFoundationRequest(base) {
  const prepared = await postJson(base, '/api/envelopes/prepare', {
    task: 'Project the exact current Foundation definitions',
    requested_skill: 'foundation-definition-projector',
    requested_grants: ['preview.read', 'skill.invoke'],
    context_refs: ['projects/ide-extension/src/adapters/foundation.mjs']
  });
  await postJson(base, `/api/approvals/${prepared.body.approval.approval_id}/approve`);
  await postJson(base, `/api/bridge/requests/${prepared.body.envelope.envelope_id}/ready`);
  const claimed = await postJson(base, `/api/bridge/requests/${prepared.body.envelope.envelope_id}/claim`, {
    schema_version: '2', envelope_id: prepared.body.envelope.envelope_id,
    agent_ref: 'foundation.local-adapter', session_ref: 'foundation-test-session', assurance: 'unattested'
  });
  return claimed.body.claim;
}

test('definition endpoint projects exact source identity without promoting authority', async () => {
  await withServer(async (base) => {
    const projection = await requestJson(base, '/api/foundation/definitions');
    assert.equal(projection.response.status, 200);
    assert.equal(projection.body.status, 'available');
    assert.equal(projection.body.authority_effect, 'none');
    assert.equal(projection.body.definitions.length, 13);
    assert.equal(projection.body.definitions[0].definition_id, 'CAF-D1');
    assert.equal(projection.body.source.claim_ceiling, 'projection-not-source-truth');
    const stale = await requestJson(base, `/api/foundation/definitions?expected_sha256=${'0'.repeat(64)}`);
    assert.equal(stale.response.status, 409);
    assert.equal(stale.body.status, 'stale');
  });
});

test('adapter consumes an active claim and returns through Workbench receipt custody', async () => {
  await withServer(async (base) => {
    const claim = await claimedFoundationRequest(base);
    const result = await executeFoundationClaim({
      baseUrl: base, claimId: claim.claim_id, foundationRoot, workbenchRoot: projectRoot,
      processRunner: async (_runtime, _args, invocation) => ({
        schema_version: 'caf.foundation-runtime-result/v1', status: 'passed',
        request_id: invocation.request_id, binding_id: invocation.binding_id,
        guest_result_sha256: 'a'.repeat(64), containment: { mechanism: 'test-double' },
        guest_result: {
          source: { sha256: invocation.invocation.input_artifact.sha256, currentness: 'verified-current' },
          definitions: Array.from({ length: 13 }, (_, index) => ({ definition_id: `CAF-D${index + 1}` }))
        }, authority_effect: 'none'
      })
    });
    assert.equal(result.admitted.receipt.receipt_kind, 'skill.execution');
    assert.equal(result.admitted.receipt.agent_ref, 'foundation.local-adapter');
    assert.equal(result.binding.ownership.foundation_may_commit_host_state, false);
    const state = await requestJson(base, '/api/state');
    assert.equal(state.body.bridge.claims[claim.claim_id].state, 'completed');
  });
});

test('real isolated guest returns its projection through the existing Workbench control plane', async () => {
  await withServer(async (base) => {
    const claim = await claimedFoundationRequest(base);
    const result = await executeFoundationClaim({
      baseUrl: base, claimId: claim.claim_id, foundationRoot, workbenchRoot: projectRoot
    });
    assert.equal(result.runtime.containment.mechanism, 'bubblewrap-v1');
    assert.equal(result.runtime.containment.workspace_mounted, false);
    assert.equal(result.runtime.guest_result.containment_probe.network_connect_blocked, true);
    assert.equal(result.runtime.guest_result.containment_probe.workspace_path_visible, false);
    assert.deepEqual(result.runtime.guest_result.containment_probe.environment_keys.sort(),
      ['CAF_CONTAINMENT', 'PWD']);
    assert.equal(result.runtime.guest_result.definitions.length, 13);
    assert.equal(result.admitted.receipt.receipt_kind, 'skill.execution');
    assert.equal(result.admitted.receipt.assurance, 'unattested');
  });
});

test('adapter fails closed before execution when no active claim exists', async () => {
  await withServer(async (base) => {
    await assert.rejects(
      executeFoundationClaim({ baseUrl: base, claimId: 'missing', foundationRoot, workbenchRoot: projectRoot }),
      (error) => error.code === 'foundation_claim_not_active'
    );
  });
});
