import assert from 'node:assert/strict';
import { mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { appendEvent, readEvents } from '../src/kernel/audit.mjs';
import { projectionChecksum, reduceEvents } from '../src/kernel/projector.mjs';
import { atomicWriteJson } from '../src/kernel/storage.mjs';
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

async function start(stateDir, options = {}) {
  const server = createServer({ rootDir: projectRoot, stateDir, ...options });
  const readiness = await server.ready;
  const port = await listen(server);
  return { server, readiness, base: `http://127.0.0.1:${port}` };
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

test('repeated races and restarts reproduce the event-derived projection', async () => {
  for (let repetition = 0; repetition < 3; repetition += 1) {
    const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-race-restart-'));
    let running;

    try {
      running = await start(stateDir);
      const prepared = await Promise.all(
        Array.from({ length: 8 }, (_, index) => (
          postJson(running.base, '/api/envelopes/prepare', { task: `Race ${repetition}-${index}` })
        ))
      );
      assert.ok(prepared.every(({ response }) => response.status === 201));

      const approvalId = prepared[0].body.approval.approval_id;
      const attempts = await Promise.all(
        Array.from({ length: 8 }, () => (
          postJson(running.base, `/api/approvals/${approvalId}/approve`)
        ))
      );
      assert.equal(attempts.filter(({ response }) => response.status === 201).length, 1);
      assert.equal(attempts.filter(({ response }) => response.status === 409).length, 7);

      const beforeRestart = await request(running.base, '/api/state');
      const events = await readEvents(path.join(stateDir, 'events.jsonl'));
      const reduced = reduceEvents(events);
      assert.equal(beforeRestart.body.event_count, 9);
      assert.equal(beforeRestart.body.receipts.length, 1);
      assert.equal(beforeRestart.body.projection_checksum, projectionChecksum(reduced));
      assert.deepEqual(beforeRestart.body.reconciliation.orphan_artifacts, []);

      await close(running.server);
      running = await start(stateDir);
      const afterRestart = await request(running.base, '/api/state');
      assert.equal(afterRestart.body.projection_checksum, beforeRestart.body.projection_checksum);
      assert.equal(afterRestart.body.event_count, beforeRestart.body.event_count);
      assert.equal(afterRestart.body.receipts.length, 1);
      assert.equal(Object.keys(afterRestart.body.envelopes).length, 8);
    } finally {
      if (running?.server.listening) await close(running.server);
      await rm(stateDir, { recursive: true, force: true });
    }
  }
});

test('startup repairs a stale projection from authoritative events', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-stale-projection-'));
  let running;

  try {
    running = await start(stateDir);
    const prepared = await postJson(running.base, '/api/envelopes/prepare', { task: 'Repair me' });
    await postJson(running.base, `/api/approvals/${prepared.body.approval.approval_id}/approve`);
    const expected = await request(running.base, '/api/state');
    await close(running.server);
    running = null;

    await writeFile(
      path.join(stateDir, 'workbench.json'),
      `${JSON.stringify({ project: 'stale', receipts: [] }, null, 2)}\n`,
      'utf8'
    );

    running = await start(stateDir);
    assert.equal(running.readiness.reconciliation.repaired, true);
    const repaired = await request(running.base, '/api/state');
    assert.equal(repaired.body.projection_checksum, expected.body.projection_checksum);
    assert.equal(repaired.body.receipts.length, 1);
  } finally {
    if (running?.server.listening) await close(running.server);
    await rm(stateDir, { recursive: true, force: true });
  }
});

test('truncated authoritative history fails readiness instead of guessing', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-truncated-history-'));

  try {
    await writeFile(path.join(stateDir, 'events.jsonl'), '{"event_version":1', 'utf8');
    const server = createServer({ rootDir: projectRoot, stateDir });
    await assert.rejects(server.ready, (error) => {
      assert.equal(error.code, 'invalid_event_history');
      assert.equal(error.reason, 'truncated_final_line');
      return true;
    });
    assert.equal(server.listening, false);
  } finally {
    await rm(stateDir, { recursive: true, force: true });
  }
});

test('a committed event survives projection failure and the next read reconciles it', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-projection-failure-'));
  let writeCount = 0;
  const writeProjection = async (...args) => {
    writeCount += 1;
    if (writeCount === 2) {
      const error = new Error('injected projection failure');
      error.code = 'EIO';
      throw error;
    }
    return atomicWriteJson(...args);
  };
  let running;

  try {
    running = await start(stateDir, { writeProjection });
    const prepared = await postJson(running.base, '/api/envelopes/prepare', {
      task: 'Projection interruption'
    });
    assert.equal(prepared.response.status, 503);
    assert.equal(prepared.body.error, 'reconciliation_required');
    assert.equal(prepared.body.recoverable, true);

    const recovered = await request(running.base, '/api/state');
    assert.equal(recovered.response.status, 200);
    assert.equal(recovered.body.event_count, 1);
    assert.equal(recovered.body.approval_queue.length, 1);
    assert.equal(recovered.body.reconciliation.repaired, true);
  } finally {
    if (running?.server.listening) await close(running.server);
    await rm(stateDir, { recursive: true, force: true });
  }
});

test('append failure leaves projection pending and reports unreferenced artifacts', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-orphan-artifacts-'));
  let appendCount = 0;
  const injectedAppend = async (...args) => {
    appendCount += 1;
    if (appendCount === 2) {
      const error = new Error('injected append failure');
      error.code = 'EIO';
      throw error;
    }
    return appendEvent(...args);
  };
  let running;

  try {
    running = await start(stateDir, { appendEvent: injectedAppend });
    const prepared = await postJson(running.base, '/api/envelopes/prepare', {
      task: 'Orphan report'
    });
    const failed = await postJson(
      running.base,
      `/api/approvals/${prepared.body.approval.approval_id}/approve`
    );
    assert.equal(failed.response.status, 500);

    const state = await request(running.base, '/api/state');
    assert.equal(state.body.event_count, 1);
    assert.equal(state.body.approvals[prepared.body.approval.approval_id].state, 'pending');
    assert.equal(state.body.receipts.length, 0);
    assert.equal(state.body.reconciliation.orphan_artifacts.length, 3);
    assert.ok(state.body.reconciliation.orphan_artifacts.every((ref) => ref.startsWith('artifacts/')));
  } finally {
    if (running?.server.listening) await close(running.server);
    await rm(stateDir, { recursive: true, force: true });
  }
});

test('atomic projection writes leave no temporary files after success', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-atomic-projection-'));
  let running;

  try {
    running = await start(stateDir);
    await postJson(running.base, '/api/envelopes/prepare', { task: 'Atomic projection' });
    const entries = await readdir(stateDir);
    assert.equal(entries.some((entry) => entry.endsWith('.tmp')), false);
    JSON.parse(await readFile(path.join(stateDir, 'workbench.json'), 'utf8'));
  } finally {
    if (running?.server.listening) await close(running.server);
    await rm(stateDir, { recursive: true, force: true });
  }
});
