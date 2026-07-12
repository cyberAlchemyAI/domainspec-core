import assert from 'node:assert/strict';
import { access, mkdtemp, readFile, readdir, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import {
  artifactRefFor,
  evidenceArtifactIds,
  readArtifactRef,
  resolveArtifactRef,
  validateArtifactRef,
  validateEvidenceRefs,
  writeArtifactRef
} from '../src/kernel/artifacts.mjs';
import { readEvents } from '../src/kernel/audit.mjs';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const evidenceRoot = path.resolve(projectRoot, '../..');

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

async function start(stateDir, options = {}) {
  const server = createServer({ rootDir: projectRoot, stateDir, ...options });
  await server.ready;
  const port = await listen(server);
  return { server, base: `http://127.0.0.1:${port}` };
}

async function request(base, route, options = {}) {
  const response = await fetch(`${base}${route}`, {
    ...options,
    headers: {
      'content-type': 'application/json',
      ...(options.headers || {})
    }
  });
  return { response, body: JSON.parse(await response.text()) };
}

function postJson(base, route, body = {}) {
  return request(base, route, { method: 'POST', body: JSON.stringify(body) });
}

test('derives bound artifact ids and refuses overwrite', async () => {
  const artifactDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-artifacts-'));

  try {
    const ids = evidenceArtifactIds({ run_id: 'run-1', approval_id: 'approval-1' });
    assert.deepEqual(ids, {
      before: 'artifact-run-1-approval-1-before',
      after: 'artifact-run-1-approval-1-after',
      receipt: 'artifact-run-1-approval-1-receipt'
    });
    const first = { kind: 'approval.before', run_id: 'run-1' };
    const ref = await writeArtifactRef(artifactDir, ids.before, first);

    await assert.rejects(
      writeArtifactRef(artifactDir, ids.before, { overwritten: true }),
      (error) => error.code === 'artifact_exists'
    );
    assert.deepEqual(await readArtifactRef(artifactDir, ref), first);
  } finally {
    await rm(artifactDir, { recursive: true, force: true });
  }
});

test('rejects path escape, missing, malformed, and mismatched artifacts', async () => {
  const artifactDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-hostile-artifacts-'));
  const outsideDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-outside-artifacts-'));

  try {
    assert.throws(
      () => resolveArtifactRef(artifactDir, '../outside.json'),
      (error) => error.code === 'artifact_path_escape'
    );
    assert.throws(
      () => artifactRefFor(artifactDir, '../outside'),
      (error) => error.code === 'invalid_artifact_id'
    );

    const missingRef = artifactRefFor(artifactDir, 'missing');
    await assert.rejects(
      readArtifactRef(artifactDir, missingRef),
      (error) => error.code === 'artifact_not_found'
    );

    const malformedRef = artifactRefFor(artifactDir, 'malformed');
    await writeFile(resolveArtifactRef(artifactDir, malformedRef), '{"broken":', 'utf8');
    await assert.rejects(
      readArtifactRef(artifactDir, malformedRef),
      (error) => error.code === 'malformed_artifact'
    );

    const outsideFile = path.join(outsideDir, 'outside.json');
    await writeFile(outsideFile, '{}\n', 'utf8');
    const linkedRef = artifactRefFor(artifactDir, 'linked');
    await symlink(outsideFile, resolveArtifactRef(artifactDir, linkedRef));
    await assert.rejects(
      readArtifactRef(artifactDir, linkedRef),
      (error) => error.code === 'artifact_path_escape'
    );

    const boundRef = await writeArtifactRef(artifactDir, 'bound', {
      run_id: 'run-1',
      approval_id: 'approval-1'
    });
    await assert.rejects(
      validateArtifactRef(artifactDir, boundRef, { run_id: 'run-2' }),
      (error) => error.code === 'artifact_binding_mismatch' && error.field === 'run_id'
    );
  } finally {
    await rm(artifactDir, { recursive: true, force: true });
    await rm(outsideDir, { recursive: true, force: true });
  }
});

test('validates source evidence inside its configured root', async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-evidence-root-'));
  const outsideRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-outside-evidence-'));

  try {
    await writeFile(path.join(root, 'evidence.txt'), 'evidence\n', 'utf8');
    assert.deepEqual(await validateEvidenceRefs(root, ['evidence.txt']), ['evidence.txt']);
    await assert.rejects(
      validateEvidenceRefs(root, ['../outside.txt']),
      (error) => error.code === 'evidence_path_escape'
    );
    await assert.rejects(
      validateEvidenceRefs(root, ['missing.txt']),
      (error) => error.code === 'evidence_not_found'
    );
    const outsideFile = path.join(outsideRoot, 'outside.txt');
    await writeFile(outsideFile, 'outside\n', 'utf8');
    await symlink(outsideFile, path.join(root, 'linked.txt'));
    await assert.rejects(
      validateEvidenceRefs(root, ['linked.txt']),
      (error) => error.code === 'evidence_path_escape'
    );
  } finally {
    await rm(root, { recursive: true, force: true });
    await rm(outsideRoot, { recursive: true, force: true });
  }
});

test('commits only fully bound, resolvable before, after, and receipt evidence', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-bound-evidence-'));
  let running;

  try {
    running = await start(stateDir);
    const prepared = await postJson(running.base, '/api/envelopes/prepare', {
      task: 'Resolve all evidence',
      requested_skill: 'blind-skill-fixture'
    });
    const envelope = prepared.body.envelope;
    const approvalId = prepared.body.approval.approval_id;
    const approved = await postJson(running.base, `/api/approvals/${approvalId}/approve`);
    assert.equal(approved.response.status, 201);

    const { receipt, artifact_refs: artifactRefs } = approved.body;
    assert.equal(receipt.run_id, envelope.run_id);
    assert.equal(receipt.envelope_id, envelope.envelope_id);
    assert.equal(receipt.approval_id, approvalId);
    assert.deepEqual(receipt.requested_grants, envelope.requested_grants);
    assert.equal(receipt.requested_skill, 'blind-skill-fixture');
    assert.equal(receipt.disposition, 'approved');
    assert.equal(receipt.before_ref, artifactRefs.before);
    assert.equal(receipt.after_ref, artifactRefs.after);
    await validateEvidenceRefs(evidenceRoot, receipt.evidence_refs);

    const artifactDir = path.join(stateDir, 'artifacts');
    const before = await readArtifactRef(artifactDir, artifactRefs.before);
    const after = await readArtifactRef(artifactDir, artifactRefs.after);
    const receiptArtifact = await readArtifactRef(artifactDir, artifactRefs.receipt);
    assert.equal(before.state, 'awaiting_approval');
    assert.equal(before.requested_skill, 'blind-skill-fixture');
    assert.equal(before.approval.state, 'pending');
    assert.equal(after.state, 'passed');
    assert.equal(after.requested_skill, 'blind-skill-fixture');
    assert.equal(after.approval.state, 'consumed');
    assert.deepEqual(receiptArtifact.receipt, receipt);
    assert.equal(receiptArtifact.requested_skill, 'blind-skill-fixture');

    for (const ref of Object.values(artifactRefs)) {
      await access(resolveArtifactRef(artifactDir, ref));
    }
    const events = await readEvents(path.join(stateDir, 'events.jsonl'));
    const receiptEvent = events.find((event) => event.event_type === 'receipt.appended');
    assert.deepEqual(new Set(receiptEvent.artifact_refs), new Set(Object.values(artifactRefs)));

    const beforeRestart = await request(running.base, '/api/state');
    assert.deepEqual(beforeRestart.body.reconciliation.orphan_artifacts, []);
    await close(running.server);
    running = await start(stateDir);
    const afterRestart = await request(running.base, '/api/state');
    assert.equal(afterRestart.body.receipts.length, 1);
    assert.deepEqual(afterRestart.body.reconciliation.orphan_artifacts, []);
  } finally {
    if (running?.server.listening) await close(running.server);
    await rm(stateDir, { recursive: true, force: true });
  }
});

test('unresolved source evidence prevents receipt commit and leaves reportable residue', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-missing-evidence-'));
  const emptyEvidenceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-empty-evidence-'));
  let running;

  try {
    running = await start(stateDir, { evidenceRoot: emptyEvidenceRoot });
    const prepared = await postJson(running.base, '/api/envelopes/prepare', {
      task: 'Missing source evidence'
    });
    const approvalId = prepared.body.approval.approval_id;
    const failed = await postJson(running.base, `/api/approvals/${approvalId}/approve`);
    assert.equal(failed.response.status, 500);
    assert.match(failed.body.error, /evidence ref does not resolve/);

    const state = await request(running.base, '/api/state');
    assert.equal(state.body.approvals[approvalId].state, 'pending');
    assert.equal(state.body.receipts.length, 0);
    assert.equal(state.body.event_count, 1);
    assert.equal(state.body.reconciliation.orphan_artifacts.length, 2);
  } finally {
    if (running?.server.listening) await close(running.server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(emptyEvidenceRoot, { recursive: true, force: true });
  }
});

test('rejection writes no passed receipt or evidence artifact', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-rejection-evidence-'));
  let running;

  try {
    running = await start(stateDir);
    const prepared = await postJson(running.base, '/api/envelopes/prepare', {
      task: 'Reject without receipt'
    });
    const rejected = await postJson(
      running.base,
      `/api/approvals/${prepared.body.approval.approval_id}/reject`,
      { reason: 'not approved' }
    );
    assert.equal(rejected.response.status, 200);
    const state = await request(running.base, '/api/state');
    assert.equal(state.body.receipts.length, 0);
    await assert.rejects(readdir(path.join(stateDir, 'artifacts')), { code: 'ENOENT' });
  } finally {
    if (running?.server.listening) await close(running.server);
    await rm(stateDir, { recursive: true, force: true });
  }
});
