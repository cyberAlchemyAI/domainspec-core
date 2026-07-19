import assert from 'node:assert/strict';
import { mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const cli = path.join(projectRoot, 'scripts/session-bridge.mjs');

function listen(server) {
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server.address().port)));
}

function close(server) {
  return new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}

async function withServer(run) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-bridge-cli-'));
  const server = createServer({ rootDir: projectRoot, stateDir });
  await server.ready;
  const port = await listen(server);
  try {
    await run({ base: `http://127.0.0.1:${port}` });
  } finally {
    if (server.listening) await close(server);
    await rm(stateDir, { recursive: true, force: true });
  }
}

function runCli(args, input = '') {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [cli, ...args], {
      cwd: projectRoot,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    const stdout = [];
    const stderr = [];
    const timer = setTimeout(() => {
      child.kill('SIGKILL');
      reject(new Error(`CLI did not exit: ${args.join(' ')}`));
    }, 3000);
    child.stdout.on('data', (chunk) => stdout.push(chunk));
    child.stderr.on('data', (chunk) => stderr.push(chunk));
    child.on('error', reject);
    child.on('close', (code) => {
      clearTimeout(timer);
      resolve({
        code,
        stdout: Buffer.concat(stdout).toString('utf8'),
        stderr: Buffer.concat(stderr).toString('utf8')
      });
    });
    child.stdin.end(input);
  });
}

async function post(base, route, body = {}) {
  const response = await fetch(`${base}${route}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body)
  });
  return { response, body: JSON.parse(await response.text()) };
}

async function preparedTarget(base, suffix = 'cli') {
  const prepared = await post(base, '/api/envelopes/prepare', {
    task: `Run CLI bridge ${suffix}`,
    requested_skill: 'decision-gate',
    requested_grants: ['preview.read', 'skill.invoke'],
    context_refs: ['projects/ide-extension/SPEC.md']
  });
  await post(base, `/api/approvals/${prepared.body.approval.approval_id}/approve`);
  await post(base, `/api/bridge/requests/${prepared.body.envelope.envelope_id}/ready`);
  return prepared.body.envelope;
}

test('uses stable exit classes for usage, loopback, empty, and connection failures', async () => {
  assert.equal((await runCli(['release'])).code, 2);
  assert.equal((await runCli(['ready', '--base-url', 'https://example.com'])).code, 2);
  assert.equal((await runCli(['ready', '--base-url', 'http://127.0.0.1:9'])).code, 4);

  await withServer(async ({ base }) => {
    const empty = await runCli(['ready', '--base-url', base]);
    assert.equal(empty.code, 3);
    assert.equal(empty.stdout, '');
    assert.equal(JSON.parse(empty.stderr).error, 'no_ready_request');
  });
});

test('runs ready, claim, and result as separate one-shot processes', async () => {
  await withServer(async ({ base }) => {
    const envelope = await preparedTarget(base, 'result');
    const ready = await runCli(['ready', '--base-url', base]);
    assert.equal(ready.code, 0);
    assert.equal(JSON.parse(ready.stdout).request.request_handle, envelope.envelope_id);
    assert.equal(ready.stderr, '');

    const claimed = await runCli([
      'claim',
      '--base-url', base,
      '--request-handle', envelope.envelope_id,
      '--agent-ref', 'openrouter.local-session',
      '--session-ref', 'session-cli-result'
    ]);
    assert.equal(claimed.code, 0);
    const packet = JSON.parse(claimed.stdout);
    assert.equal(packet.claim.agent_ref, 'openrouter.local-session');
    assert.equal(packet.execution.requested_skill, 'decision-gate');

    const duplicate = await runCli([
      'claim',
      '--base-url', base,
      '--request-handle', envelope.envelope_id,
      '--session-ref', 'session-cli-loser'
    ]);
    assert.equal(duplicate.code, 3);
    assert.equal(duplicate.stdout, '');
    assert.equal(duplicate.stderr.includes('decision-gate'), false);
    assert.equal(duplicate.stderr.includes('Run CLI bridge'), false);

    const resultInput = {
      schema_version: '2',
      claim_id: packet.claim.claim_id,
      claim_attempt_id: packet.claim.claim_attempt_id,
      envelope_id: packet.claim.envelope_id,
      run_id: packet.claim.run_id,
      approval_id: packet.claim.approval_id,
      session_ref: packet.claim.session_ref,
      assurance: 'unattested',
      requested_skill: packet.execution.requested_skill,
      skill_sha256: 'b'.repeat(64),
      status: 'passed',
      summary: 'CLI submitted the bounded result.',
      validation: ['one-shot process completed'],
      evidence_refs: ['projects/ide-extension/SPEC.md']
    };
    const result = await runCli([
      'result',
      '--base-url', base,
      '--claim-id', packet.claim.claim_id,
      '--input', '-'
    ], JSON.stringify(resultInput));
    assert.equal(result.code, 0);
    const resultPacket = JSON.parse(result.stdout);
    assert.equal(resultPacket.receipt.receipt_kind, 'skill.execution');
    assert.equal(resultPacket.receipt.agent_ref, 'openrouter.local-session');
    assert.equal(result.stderr, '');
  });
});

test('submits a claimant-bound interrupt without exposing operator commands', async () => {
  await withServer(async ({ base }) => {
    const envelope = await preparedTarget(base, 'interrupt');
    const claimed = await runCli([
      'claim',
      '--base-url', base,
      '--request-handle', envelope.envelope_id,
      '--agent-ref', 'openrouter.local-session',
      '--session-ref', 'session-cli-interrupt'
    ]);
    const packet = JSON.parse(claimed.stdout);
    assert.equal(packet.claim.agent_ref, 'openrouter.local-session');
    const interrupted = await runCli([
      'interrupt',
      '--base-url', base,
      '--claim-id', packet.claim.claim_id,
      '--input', '-'
    ], JSON.stringify({
      schema_version: '2',
      claim_id: packet.claim.claim_id,
      envelope_id: packet.claim.envelope_id,
      session_ref: packet.claim.session_ref,
      assurance: 'unattested',
      reason: 'CLI session stopped before result.'
    }));
    assert.equal(interrupted.code, 0);
    assert.equal(JSON.parse(interrupted.stdout).claim.state, 'interrupted');
    assert.equal((await runCli(['approve'])).code, 2);
    assert.equal((await runCli(['unready'])).code, 2);
  });
});
