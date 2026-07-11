import assert from 'node:assert/strict';
import { mkdtemp } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
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

async function requestJson(base, route, options = {}) {
  const response = await fetch(`${base}${route}`, {
    ...options,
    headers: {
      'content-type': 'application/json',
      ...(options.headers || {})
    }
  });
  const body = await response.json();
  return { response, body };
}

test('L0 workbench prepares, blocks, approves, and receipts a dry run', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-smoke-'));
  const server = createServer({ rootDir: projectRoot, stateDir });
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;

  try {
    const html = await fetch(`${base}/demo/l0`);
    assert.equal(html.status, 200);
    assert.match(await html.text(), /L0 governed workbench/);

    const initial = await requestJson(base, '/api/state');
    assert.equal(initial.response.status, 200);
    assert.ok(initial.body.modules.some((module) => module.module_id === 'craft'));

    const prepared = await requestJson(base, '/api/envelopes/prepare', {
      method: 'POST',
      body: JSON.stringify({ task: 'Smoke dry run' })
    });
    assert.equal(prepared.response.status, 201);
    assert.equal(prepared.body.envelope.state, 'awaiting_approval');

    const blocked = await requestJson(base, '/api/envelopes/run', { method: 'POST' });
    assert.equal(blocked.response.status, 409);
    assert.equal(blocked.body.error, 'approval_required');

    const approvalId = prepared.body.approval.approval_id;
    const approved = await requestJson(base, `/api/approvals/${approvalId}/approve`, {
      method: 'POST',
      body: JSON.stringify({ approved_by: 'smoke-test' })
    });
    assert.equal(approved.response.status, 201);
    assert.equal(approved.body.receipt.status, 'passed');

    const finalState = await requestJson(base, '/api/state');
    assert.equal(finalState.body.current_envelope.state, 'passed');
    assert.equal(finalState.body.receipts.length, 1);
    assert.ok(finalState.body.event_count >= 2);
  } finally {
    await close(server);
  }
});
