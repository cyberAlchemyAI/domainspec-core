import assert from 'node:assert/strict';
import { mkdtemp, rm, unlink, writeFile } from 'node:fs/promises';
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

async function withServer(run, options = {}) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-workbench-'));
  const server = createServer({ rootDir: projectRoot, stateDir, ...options });
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
      'data-region="work"',
      'data-region="canvas"',
      'data-region="inspector"',
      'data-panel="craft"',
      'data-panel="canvas"',
      'data-action="prepare"',
      'data-action="approve"',
      'data-action="inspect"',
      'data-action="reject"',
      'data-action="ready"',
      'data-action="unready"',
      'data-action="release"',
      'data-action="craft-refresh"',
      'data-action="canvas-refresh"',
      'data-action="canvas-event-retry"',
      'data-action="canvas-pruning-preview"',
      'data-action="canvas-pruning-commit"',
      'data-field="task-input"',
      'data-field="skill-input"',
      'data-request-mode="agent-task"',
      'data-request-mode="dry-run"',
      'data-view="pending"',
      'data-view="history"',
      'data-mobile-view="work"',
      'data-mobile-view="canvas"',
      'data-mobile-view="evidence"',
      'data-list="craft-pending"',
      'data-list="bridge-safe-fields"',
      'data-list="bridge-commands"',
      'data-list="bridge-receipt-summary"',
      'data-list="grants"',
      'data-list="receipts"',
      'data-viewer="evidence"'
    ]) {
      assert.match(document, new RegExp(selector));
    }
    assert.match(document, /role="tablist"/);
    assert.match(document, /role="radiogroup" aria-label="Request mode"/);
    assert.match(document, /data-request-mode="agent-task"/);
    assert.match(document, /data-request-mode="dry-run"/);
    assert.match(document, /state\.requestMode/);
    assert.match(document, /setRequestMode\(state\.requestMode\)/);
    assert.match(document, /aria-label="Mobile workbench views"/);
    assert.match(document, /data-mobile-view="work"/);
    assert.match(document, /data-mobile-view="canvas"/);
    assert.match(document, /data-mobile-view="evidence"/);
    assert.match(document, /state\.mobileView/);
    assert.match(document, /setMobileView\(state\.mobileView\)/);
    assert.match(document, /<section id="work-region" class="work-region" data-region="work" role="region" aria-labelledby="work-region-heading">/);
    assert.match(document, /<h2 id="work-region-heading" class="visually-hidden">Work<\/h2>/);
    assert.match(document, /data-region="inspector" role="region" aria-labelledby="inspector-heading"/);
    assert.match(document, /<h2 id="inspector-heading" class="visually-hidden">Inspector<\/h2>/);
    assert.match(document, /data-region="canvas" role="region" aria-labelledby="canvas-title"/);
    assert.match(document, /src="\/assets\/cyber-alchemy-logo\.svg\?v=cyberalchemy-mark"/);
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
    assert.match(document, /Available to poll:/);
    assert.match(document, /Bridge demo/);
    assert.match(document, /workbench-poll --ready/);
    assert.match(document, /workbench-poll --claim --request-handle/);
    assert.match(document, /import \{ projectRunView \} from '\/ui\/run-view\.mjs';/);
    assert.match(document, /import \{ resolveRunActions \} from '\/ui\/run-actions\.mjs';/);
    assert.match(document, /import \{ renderRunTimeline \} from '\/ui\/run-timeline\.mjs';/);
    assert.match(document, /renderRunTimeline\(els\.bridgeFlow, runView\)/);
    assert.match(document, /No skill\.execution receipt admitted/);
    assert.match(document, /Chat output alone is not terminal proof/);
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
    assert.match(document, /\/api\/canvas\/display/);
    assert.match(document, /\/api\/canvas\/navigation/);
    assert.match(document, /\/api\/canvas\/storage/);
    assert.match(document, /\/api\/canvas\/pruning\/preview/);
    assert.match(document, /\/api\/canvas\/pruning\/commit/);
    assert.match(document, /\/api\/canvas\/operation-surfaces\/\$\{encodeURIComponent\(current\.surface_id\)\}\/events/);
    assert.match(document, /nextFrame\.dataset\.surfaceKind = current\.surface_kind/);
    assert.doesNotMatch(document, /api\('\/api\/canvas\/current'/);
    assert.match(document, /\/api\/canvas\/events/);
    assert.match(document, /\/api\/craft\/frontier/);
    assert.match(document, /ide-extension\.canvas\.event/);
    assert.match(document, /canvas-frame-pending/);
    assert.match(document, /canvas\.storage\.changed/);
    assert.match(document, /storage\.candidate_revision_count/);
    const moduleScript = document.match(/<script type="module">([\s\S]*?)<\/script>/);
    assert.ok(moduleScript);
    const staticScript = moduleScript[1].replace(
      /^\s*import .* from ['"]\/ui\/[^'\"]+['"];\s*$/gm,
      ''
    );
    assert.doesNotThrow(() => new Function(staticScript));

    for (const route of ['/ui/run-view.mjs', '/ui/run-timeline.mjs', '/ui/run-actions.mjs']) {
      const moduleResponse = await fetch(`${base}${route}`);
      assert.equal(moduleResponse.status, 200);
      assert.match(moduleResponse.headers.get('content-type'), /^text\/javascript/);
      assert.match(await moduleResponse.text(), /export /);
    }

    const logoResponse = await fetch(`${base}/assets/cyber-alchemy-logo.svg`);
    const logo = await logoResponse.text();
    assert.equal(logoResponse.status, 200);
    assert.match(logoResponse.headers.get('content-type'), /^image\/svg\+xml/);
    assert.match(logo, /<title id="title">CyberAlchemy Mark<\/title>/);

    const craft = await request(base, '/api/craft/frontier');
    assert.equal(craft.response.status, 200);
    assert.equal(craft.body.source.verified, true);
    assert.equal(craft.body.scope.context_id, 'CTX-IDEEXT-L0');
    assert.equal(craft.body.counts.total_pending, 7);
    assert.deepEqual(craft.body.next_moves.map((item) => item.id), [
      'CTX-IDEEXT-L0',
      'CTX-IDEEXT-WUI-V1'
    ]);
    assert.deepEqual(craft.body.pending.map((item) => item.id), [
      'GAP-IDEEXT-PLAYWRIGHT-MCP',
      'GAP-IDEEXT-VSCODIUM-WEBVIEW',
      'GAP-IDEEXT-MANIFEST-VALIDATOR',
      'GAP-IDEEXT-PROVIDER-ADAPTER',
      'GAP-IDEEXT-SCW-HUMAN-REVIEW'
    ]);
  });
});

test('craft frontier refuses a stale generated index', async () => {
  const craftDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-craft-'));
  try {
    await writeFile(path.join(craftDir, 'ledger.yml'), 'ledger_id: changed\n', 'utf8');
    await writeFile(path.join(craftDir, 'index.json'), JSON.stringify({
      schema_version: '1',
      source: {
        ledger_path: '.craft/ledger.yml',
        sha256: '0'.repeat(64)
      },
      ledger: { ledger_id: 'craft.stale' },
      scope: {
        context_id: 'CTX-STALE',
        title: 'Stale fixture',
        stage: 'test',
        gate: 'flag'
      },
      counts: {
        next_moves: 0,
        active_gaps: 0,
        active_blockers: 0,
        open_decisions: 0,
        total_pending: 0
      },
      next_moves: [],
      pending: []
    }), 'utf8');

    await withServer(async ({ base }) => {
      const craft = await request(base, '/api/craft/frontier');
      assert.equal(craft.response.status, 409);
      assert.equal(craft.body.error, 'craft_index_stale');
      assert.match(craft.body.message, /regenerate/);
    }, { craftDir });
  } finally {
    await rm(craftDir, { recursive: true, force: true });
  }
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
