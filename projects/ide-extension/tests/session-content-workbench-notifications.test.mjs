import assert from 'node:assert/strict';
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { createServer } from '../src/server.mjs';

function listen(server, port = 0) {
  return new Promise((resolve) => server.listen(port, '127.0.0.1', () => resolve(server.address().port)));
}

function close(server) {
  return new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}

async function publish(base, pathValue, title) {
  return fetch(`${base}/api/canvas/publish`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ schema_version: '1', path: pathValue, title, kind: 'presentation' })
  });
}

async function openNotifications(base) {
  const controller = new AbortController();
  const response = await fetch(`${base}/api/canvas/notifications`, { signal: controller.signal });
  assert.equal(response.status, 200);
  assert.match(response.headers.get('content-type'), /^text\/event-stream/);
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  const queue = [];
  const waiters = [];
  let buffer = '';

  function deliver(value) {
    const waiter = waiters.shift();
    if (waiter) waiter(value);
    else queue.push(value);
  }

  const pump = (async () => {
    while (true) {
      const { done, value } = await reader.read();
      if (done) return;
      buffer += decoder.decode(value, { stream: true });
      let boundary;
      while ((boundary = buffer.indexOf('\n\n')) !== -1) {
        const block = buffer.slice(0, boundary);
        buffer = buffer.slice(boundary + 2);
        const id = block.match(/^id: (.+)$/m)?.[1];
        const data = block.match(/^data: (.+)$/m)?.[1];
        if (data) deliver({ id: Number(id), data: JSON.parse(data) });
      }
    }
  })().catch((error) => {
    if (!controller.signal.aborted) throw error;
  });

  return {
    get receivedCount() {
      return queue.length;
    },
    next(timeout = 1000) {
      if (queue.length) return Promise.resolve(queue.shift());
      return new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
          const index = waiters.indexOf(deliverValue);
          if (index !== -1) waiters.splice(index, 1);
          reject(new Error('notification timeout'));
        }, timeout);
        function deliverValue(value) {
          clearTimeout(timer);
          resolve(value);
        }
        waiters.push(deliverValue);
      });
    },
    async close() {
      controller.abort();
      await reader.cancel().catch(() => {});
      await pump;
    }
  };
}

async function waitFor(check, timeout = 1000) {
  const deadline = Date.now() + timeout;
  while (!check()) {
    if (Date.now() >= deadline) throw new Error('condition timeout');
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
}

test('notifications follow committed revisions and reconnect to durable current state', async () => {
  const rootDir = path.resolve(new URL('..', import.meta.url).pathname);
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-live-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-live-workspace-'));
  const relative = 'generated/live.html';
  const file = path.join(workspaceRoot, relative);
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, '<!doctype html><title>One</title>', 'utf8');

  let server = createServer({ rootDir, stateDir, workspaceRoot });
  await server.ready;
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;
  let stream = await openNotifications(base);

  try {
    assert.equal(server.canvasNotifications.clientCount, 1);
    const firstResponse = await publish(base, relative, 'One');
    assert.equal(firstResponse.status, 201);
    const first = await stream.next();
    assert.equal(first.data.type, 'canvas.revision.available');
    assert.equal(first.data.revision_id, (await firstResponse.json()).current.revision.revision_id);

    const duplicate = await publish(base, relative, 'Duplicate');
    assert.equal(duplicate.status, 200);
    await new Promise((resolve) => setTimeout(resolve, 100));
    assert.equal(stream.receivedCount, 0);

    await writeFile(file, '<!doctype html><title>Two</title>', 'utf8');
    const secondResponse = await publish(base, relative, 'Two');
    const secondBody = await secondResponse.json();
    const second = await stream.next();
    assert.equal(second.data.revision_id, secondBody.current.revision.revision_id);
    assert.ok(second.id > first.id);

    await stream.close();
    await waitFor(() => server.canvasNotifications.clientCount === 0);
    await writeFile(file, '<!doctype html><title>Three</title>', 'utf8');
    const thirdResponse = await publish(base, relative, 'Three');
    const thirdBody = await thirdResponse.json();

    stream = await openNotifications(base);
    assert.equal((await stream.next()).data.revision_id, thirdBody.current.revision.revision_id);
    await stream.close();

    await close(server);
    server = createServer({ rootDir, stateDir, workspaceRoot });
    await server.ready;
    await listen(server, port);
    stream = await openNotifications(base);
    assert.equal((await stream.next()).data.revision_id, thirdBody.current.revision.revision_id);
  } finally {
    await stream?.close();
    if (server.listening) await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
  }
});
