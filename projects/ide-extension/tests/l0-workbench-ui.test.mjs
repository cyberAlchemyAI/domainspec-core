import assert from 'node:assert/strict';
import { mkdtemp, rm, unlink } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { resolveArtifactRef } from '../src/kernel/artifacts.mjs';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));

function listen(server) {
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve(server.address().port));
  });
}

function close(server) {
  return new Promise((resolve, reject) => {
    server.close((error) => (error ? reject(error) : resolve()));
  });
}

async function withServer(run) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-workbench-'));
  const server = createServer({ rootDir: projectRoot, stateDir });
  await server.ready;
  const port = await listen(server);

  try {
    await run({ base: `http://127.0.0.1:${port}`, stateDir });
  } finally {
    await close(server);
    await rm(stateDir, { recursive: true, force: true });
  }
}

async function request(base, route, options = {}) {
  const response = await fetch(`${base}${route}`, {
    ...options,
    headers: {
      'content-type': 'application/json',
      ...(options.headers || {})
    }
  });
  const raw = await response.text();
  let body;
  try {
    body = JSON.parse(raw);
  } catch {
    body = { raw };
  }
  return { response, body };
}

function postJson(base, route, body = {}) {
  return request(base, route, { method: 'POST', body: JSON.stringify(body) });
}

test('document exposes semantic stable selectors and text-only dynamic rendering', async () => {
  await withServer(async ({ base }) => {
    const response = await fetch(`${base}/demo/l0`);
    const document = await response.text();

    assert.equal(response.status, 200);
    for (const selector of [
      'data-panel="proposals"',
      'data-panel="detail"',
      'data-panel="evidence"',
      'data-panel="canvas"',
      'data-action="prepare"',
      'data-action="approve"',
      'data-action="reject"',
      'data-action="ready"',
      'data-action="unready"',
      'data-action="release"',
      'data-action="canvas-refresh"',
      'data-action="canvas-event-retry"',
      'data-field="task-input"',
      'data-field="skill-input"',
      'data-view="pending"',
      'data-view="history"',
      'data-list="grants"',
      'data-list="receipts"',
      'data-viewer="evidence"'
    ]) {
      assert.match(document, new RegExp(selector));
    }
    assert.match(document, /role="tablist"/);
    assert.match(document, /src="\/assets\/cyber-alchemy-logo\.svg"/);
    assert.match(document, /<h1>Cyber Alchemy<\/h1>/);
    assert.match(document, /aria-live="polite"/);
    assert.match(document, /:focus-visible/);
    assert.match(document, /@media \(max-width: 720px\)/);
    assert.match(document, /local operator action/);
    assert.match(document, /<label for="task-input">Task<\/label>/);
    assert.match(document, /id="task-input"[^>]+required/);
    assert.doesNotMatch(document, /value="Prepare L0 dry-run receipt"/);
    assert.doesNotMatch(document, /Approve no-op/);
    assert.match(document, /Approve request/);
    assert.match(document, /requested_grants: \['preview\.read', 'skill\.invoke'\]/);
    assert.match(document, /authorization\.receipt/);
    assert.match(document, /skill\.execution/);
    assert.match(document, /Ready target:/);
    assert.match(document, /Claimed by unattested local session/);
    assert.match(document, /Release and requeue/);
    assert.match(document, /release_reason/);
    assert.doesNotMatch(document, /data-action="claim"/);
    assert.doesNotMatch(document, /data-action="interrupt"/);
    assert.doesNotMatch(document, /data-action="result"/);
    assert.match(document, /receipt_kind/);
    assert.match(document, /\.prepare-field/);
    assert.match(document, /overflow-wrap: anywhere/);
    assert.doesNotMatch(document, /verified human/i);
    assert.doesNotMatch(document, /\.innerHTML/);
    assert.match(document, /\.textContent/);
    assert.match(document, /nextFrame\.id = 'canvas-frame'/);
    assert.match(document, /\/api\/canvas\/current/);
    assert.match(document, /\/api\/canvas\/events/);
    assert.match(document, /ide-extension\.canvas\.event/);
    assert.match(document, /canvas-frame-pending/);
    const moduleScript = document.match(/<script type="module">([\s\S]*?)<\/script>/);
    assert.ok(moduleScript);
    assert.doesNotThrow(() => new Function(moduleScript[1]));

    const logoResponse = await fetch(`${base}/assets/cyber-alchemy-logo.svg`);
    const logo = await logoResponse.text();
    assert.equal(logoResponse.status, 200);
    assert.match(logoResponse.headers.get('content-type'), /^image\/svg\+xml/);
    assert.match(logo, /<title id="title">Cyber Alchemy<\/title>/);
  });
});

test('bridge proposal detail projects target, recovery attempts, and terminal result', async () => {
  await withServer(async ({ base }) => {
    const prepared = await postJson(base, '/api/envelopes/prepare', {
      task: 'Inspect recovery and terminal evidence in the workbench',
      requested_skill: 'decision-gate',
      requested_grants: ['preview.read', 'skill.invoke']
    });
    const envelopeId = prepared.body.envelope.envelope_id;
    await postJson(base, `/api/approvals/${prepared.body.approval.approval_id}/approve`);

    let detail = await request(base, `/api/proposals/${envelopeId}`);
    assert.equal(detail.body.envelope.state, 'approved');
    assert.deepEqual(detail.body.claims, []);
    assert.equal(detail.body.result, null);

    await postJson(base, `/api/bridge/requests/${envelopeId}/ready`);
    const firstClaimed = await postJson(base, `/api/bridge/requests/${envelopeId}/claim`, {
      schema_version: '2',
      envelope_id: envelopeId,
      agent_ref: 'codex.current-session',
      session_ref: 'session-workbench-first',
      assurance: 'unattested'
    });
    const firstClaim = firstClaimed.body.claim;
    await postJson(base, `/api/bridge/claims/${firstClaim.claim_id}/interrupt`, {
      schema_version: '2',
      claim_id: firstClaim.claim_id,
      envelope_id: envelopeId,
      session_ref: firstClaim.session_ref,
      assurance: 'unattested',
      reason: 'Manual session stopped before returning evidence.'
    });

    detail = await request(base, `/api/proposals/${envelopeId}`);
    assert.equal(detail.body.envelope.state, 'interrupted');
    assert.equal(detail.body.active_claim.assurance, 'unattested');
    assert.match(detail.body.active_claim.interruption_reason, /stopped/);

    await postJson(base, `/api/bridge/claims/${firstClaim.claim_id}/release`, {
      reason: 'Operator approved a fresh read-only attempt.'
    });
    await postJson(base, `/api/bridge/requests/${envelopeId}/ready`);
    const secondClaimed = await postJson(base, `/api/bridge/requests/${envelopeId}/claim`, {
      schema_version: '2',
      envelope_id: envelopeId,
      agent_ref: 'codex.current-session',
      session_ref: 'session-workbench-second',
      assurance: 'unattested'
    });
    const claim = secondClaimed.body.claim;
    await postJson(base, `/api/bridge/claims/${claim.claim_id}/result`, {
      schema_version: '2',
      claim_id: claim.claim_id,
      claim_attempt_id: claim.claim_attempt_id,
      envelope_id: envelopeId,
      run_id: claim.run_id,
      approval_id: claim.approval_id,
      session_ref: claim.session_ref,
      assurance: 'unattested',
      requested_skill: 'decision-gate',
      skill_sha256: 'd'.repeat(64),
      status: 'flagged',
      summary: 'Decision evidence returned with one named residue.',
      validation: ['operator states inspected'],
      evidence_refs: ['projects/ide-extension/SPEC.md']
    });

    detail = await request(base, `/api/proposals/${envelopeId}`);
    assert.equal(detail.body.envelope.state, 'flagged');
    assert.equal(detail.body.claims.length, 2);
    assert.equal(detail.body.claims[0].state, 'released');
    assert.equal(detail.body.active_claim.state, 'completed');
    assert.equal(detail.body.result.status, 'flagged');
    assert.deepEqual(detail.body.result.validation, ['operator states inspected']);
    assert.deepEqual(detail.body.result.evidence_refs, ['projects/ide-extension/SPEC.md']);
  });
});

test('bridge proposal detail keeps authorization and execution receipts distinct', async () => {
  await withServer(async ({ base }) => {
    const prepared = await postJson(base, '/api/envelopes/prepare', {
      task: 'Workbench bridge receipt distinction',
      requested_skill: 'decision-gate',
      requested_grants: ['preview.read', 'skill.invoke'],
      context_refs: ['projects/ide-extension/SPEC.md']
    });
    const authorized = await postJson(
      base,
      `/api/approvals/${prepared.body.approval.approval_id}/approve`
    );
    await postJson(base, `/api/bridge/requests/${prepared.body.envelope.envelope_id}/ready`);
    const claimed = await postJson(base, `/api/bridge/requests/${prepared.body.envelope.envelope_id}/claim`, {
      schema_version: '2',
      envelope_id: prepared.body.envelope.envelope_id,
      agent_ref: 'codex.current-session',
      session_ref: 'session-workbench-receipts',
      assurance: 'unattested'
    });
    const claim = claimed.body.claim;
    const executed = await postJson(base, `/api/bridge/claims/${claim.claim_id}/result`, {
      schema_version: '2',
      claim_id: claim.claim_id,
      claim_attempt_id: claim.claim_attempt_id,
      envelope_id: claim.envelope_id,
      run_id: claim.run_id,
      approval_id: claim.approval_id,
      session_ref: claim.session_ref,
      assurance: 'unattested',
      requested_skill: 'decision-gate',
      skill_sha256: 'c'.repeat(64),
      status: 'passed',
      summary: 'Workbench receipt distinction completed.',
      validation: ['receipt kinds checked'],
      evidence_refs: ['projects/ide-extension/SPEC.md']
    });
    assert.equal(executed.response.status, 201);

    const detail = await request(
      base,
      `/api/proposals/${prepared.body.envelope.envelope_id}`
    );
    assert.deepEqual(detail.body.receipts.map((receipt) => receipt.receipt_kind), [
      'authorization.receipt',
      'skill.execution'
    ]);
    assert.equal(Object.hasOwn(detail.body.receipts[0], 'status'), false);
    assert.equal(detail.body.receipts[1].status, 'passed');
    assert.equal(detail.body.receipts[0].receipt_id, authorized.body.receipt.receipt_id);
    assert.deepEqual(Object.keys(detail.body.receipts[1].evidence).sort(), [
      'after', 'before', 'receipt', 'result'
    ]);
  });
});

test('two proposals remain selectable through approve, reject, history, and evidence', async () => {
  await withServer(async ({ base }) => {
    const hostileTask = '<img src=x onerror=alert(1)> long proposal';
    const first = await postJson(base, '/api/envelopes/prepare', {
      task: hostileTask,
      requested_skill: 'blind-skill-fixture'
    });
    const second = await postJson(base, '/api/envelopes/prepare', { task: 'Reject this proposal' });
    assert.equal(first.response.status, 201);
    assert.equal(second.response.status, 201);

    const initial = await request(base, '/api/state');
    assert.equal(initial.body.approval_queue.length, 2);
    assert.equal(initial.body.approval_queue.filter((item) => item.state === 'pending').length, 2);

    const firstDetail = await request(
      base,
      `/api/proposals/${encodeURIComponent(first.body.envelope.envelope_id)}`
    );
    const secondDetail = await request(
      base,
      `/api/proposals/${encodeURIComponent(second.body.envelope.envelope_id)}`
    );
    assert.equal(firstDetail.body.envelope.task, hostileTask);
    assert.equal(firstDetail.body.envelope.requested_skill, 'blind-skill-fixture');
    assert.equal(firstDetail.body.approval.state, 'pending');
    assert.equal(secondDetail.body.approval.state, 'pending');

    const approved = await postJson(
      base,
      `/api/approvals/${first.body.approval.approval_id}/approve`
    );
    const rejected = await postJson(
      base,
      `/api/approvals/${second.body.approval.approval_id}/reject`,
      { reason: 'not ready' }
    );
    assert.equal(approved.response.status, 201);
    assert.equal(rejected.response.status, 200);

    const approvedDetail = await request(
      base,
      `/api/proposals/${encodeURIComponent(first.body.envelope.envelope_id)}`
    );
    const rejectedDetail = await request(
      base,
      `/api/proposals/${encodeURIComponent(second.body.envelope.envelope_id)}`
    );
    assert.equal(approvedDetail.body.approval.state, 'consumed');
    assert.equal(approvedDetail.body.receipts[0].requested_skill, 'blind-skill-fixture');
    assert.equal(approvedDetail.body.receipts.length, 1);
    assert.equal(Object.hasOwn(approvedDetail.body.receipts[0], 'before_ref'), false);
    assert.equal(Object.hasOwn(approvedDetail.body.receipts[0], 'after_ref'), false);
    assert.equal(rejectedDetail.body.approval.state, 'rejected');
    assert.equal(rejectedDetail.body.approval.rejection_reason, 'not ready');
    assert.deepEqual(rejectedDetail.body.receipts, []);

    const receipt = approvedDetail.body.receipts[0];
    for (const [kind, route] of Object.entries(receipt.evidence)) {
      const evidence = await request(base, route);
      assert.equal(evidence.response.status, 200);
      assert.equal(evidence.body.kind, `approval.${kind}`);
      assert.equal(evidence.body.run_id, first.body.envelope.run_id);
      assert.equal(evidence.body.envelope_id, first.body.envelope.envelope_id);
      assert.equal(evidence.body.approval_id, first.body.approval.approval_id);
      assert.equal(JSON.stringify(evidence.body).includes(approved.body.receipt.before_ref), false);
    }

    const replay = await postJson(
      base,
      `/api/approvals/${first.body.approval.approval_id}/approve`
    );
    assert.equal(replay.response.status, 409);
    assert.equal(replay.body.error, 'already_resolved');

    const finalState = await request(base, '/api/state');
    assert.equal(finalState.body.approval_queue.filter((item) => item.state !== 'pending').length, 2);
    assert.equal(finalState.body.receipts.length, 1);
  });
});

test('bounded detail and evidence routes return stable not-found errors', async () => {
  await withServer(async ({ base, stateDir }) => {
    const missingProposal = await request(base, '/api/proposals/envelope-missing');
    const missingReceipt = await request(base, '/api/receipts/receipt-missing/evidence/before');
    assert.equal(missingProposal.response.status, 404);
    assert.equal(missingProposal.body.error, 'proposal_not_found');
    assert.equal(missingReceipt.response.status, 404);
    assert.equal(missingReceipt.body.error, 'receipt_not_found');

    const prepared = await postJson(base, '/api/envelopes/prepare', { task: 'Missing evidence view' });
    const approved = await postJson(
      base,
      `/api/approvals/${prepared.body.approval.approval_id}/approve`
    );
    await unlink(resolveArtifactRef(
      path.join(stateDir, 'artifacts'),
      approved.body.artifact_refs.after
    ));
    const unavailable = await request(
      base,
      `/api/receipts/${approved.body.receipt.receipt_id}/evidence/after`
    );
    assert.equal(unavailable.response.status, 404);
    assert.deepEqual(unavailable.body, { error: 'evidence_unavailable' });
  });
});
