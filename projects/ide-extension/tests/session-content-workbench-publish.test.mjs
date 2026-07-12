import assert from 'node:assert/strict';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { createServer } from '../src/server.mjs';

function listen(server) {
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server.address().port)));
}

function close(server) {
  return new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}

async function request(base, route, options = {}) {
  const response = await fetch(`${base}${route}`, {
    ...options,
    headers: { 'content-type': 'application/json', ...(options.headers || {}) }
  });
  const contentType = response.headers.get('content-type') || '';
  return {
    response,
    body: contentType.includes('application/json')
      ? JSON.parse(await response.text())
      : await response.text()
  };
}

function publish(base, body) {
  return request(base, '/api/canvas/publish', {
    method: 'POST',
    body: JSON.stringify({ schema_version: '1', ...body })
  });
}

async function start(rootDir, stateDir, workspaceRoot, options = {}) {
  const server = createServer({ rootDir, stateDir, workspaceRoot, ...options });
  await server.ready;
  const port = await listen(server);
  return { server, base: `http://127.0.0.1:${port}` };
}

async function fixture() {
  const rootDir = path.resolve(new URL('..', import.meta.url).pathname);
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-canvas-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-canvas-workspace-'));
  await mkdir(path.join(workspaceRoot, 'presentations'));
  const relative = 'presentations/demo.html';
  const file = path.join(workspaceRoot, relative);
  await writeFile(file, '<!doctype html><title>One</title><button>Next</button>', 'utf8');
  return { rootDir, stateDir, workspaceRoot, relative, file };
}

test('publishes, serves, republishes, and restores one workspace HTML surface', async () => {
  const f = await fixture();
  let running;
  try {
    running = await start(f.rootDir, f.stateDir, f.workspaceRoot);
    assert.deepEqual((await request(running.base, '/api/canvas/current')).body, { current: null });

    const first = await publish(running.base, {
      path: f.relative,
      title: 'Demo presentation',
      kind: 'presentation'
    });
    assert.equal(first.response.status, 201);
    assert.equal(first.body.idempotent, false);
    const firstCurrent = first.body.current;
    assert.equal(firstCurrent.path, f.relative);
    assert.equal((await request(running.base, firstCurrent.content_url)).body.includes('<title>One</title>'), true);

    const duplicate = await publish(running.base, {
      path: f.relative,
      title: 'Ignored duplicate title',
      kind: 'presentation'
    });
    assert.equal(duplicate.response.status, 200);
    assert.equal(duplicate.body.idempotent, true);
    assert.equal(duplicate.body.current.revision.revision_id, firstCurrent.revision.revision_id);

    await writeFile(f.file, '<!doctype html><title>Two</title><button>Continue</button>', 'utf8');
    const changed = await request(running.base, firstCurrent.content_url);
    assert.equal(changed.response.status, 409);
    assert.equal(changed.body.error, 'revision_changed');

    const second = await publish(running.base, {
      path: f.relative,
      title: 'Demo presentation revised',
      kind: 'presentation'
    });
    assert.equal(second.response.status, 201);
    assert.equal(second.body.current.surface_id, firstCurrent.surface_id);
    assert.notEqual(second.body.current.revision.revision_id, firstCurrent.revision.revision_id);
    assert.equal(second.body.current.revision_ids.length, 2);

    const beforeRestart = (await request(running.base, '/api/canvas/current')).body;
    await close(running.server);
    running = await start(f.rootDir, f.stateDir, f.workspaceRoot);
    assert.deepEqual((await request(running.base, '/api/canvas/current')).body, beforeRestart);
  } finally {
    if (running?.server.listening) await close(running.server);
    await rm(f.stateDir, { recursive: true, force: true });
    await rm(f.workspaceRoot, { recursive: true, force: true });
  }
});

test('serializes same-file races and leaves invalid inputs uncommitted', async () => {
  const f = await fixture();
  const running = await start(f.rootDir, f.stateDir, f.workspaceRoot);
  try {
    const attempts = await Promise.all(Array.from({ length: 6 }, () => publish(running.base, {
      path: f.relative,
      title: 'Race presentation',
      kind: 'presentation'
    })));
    assert.equal(attempts.filter(({ response }) => response.status === 201).length, 1);
    assert.equal(attempts.filter(({ response }) => response.status === 200).length, 5);
    const state = (await request(running.base, '/api/state')).body;
    assert.equal(state.event_count, 1);
    assert.equal(state.canvas.surfaces[state.canvas.current_surface_id].revision_ids.length, 1);

    for (const body of [
      { path: '../escape.html', title: 'Escape', kind: 'presentation' },
      { path: 'presentations/missing.html', title: 'Missing', kind: 'presentation' },
      { path: 'presentations', title: 'Directory', kind: 'presentation' }
    ]) {
      assert.notEqual((await publish(running.base, body)).response.status, 201);
    }
    assert.equal((await request(running.base, '/api/state')).body.event_count, 1);
  } finally {
    await close(running.server);
    await rm(f.stateDir, { recursive: true, force: true });
    await rm(f.workspaceRoot, { recursive: true, force: true });
  }
});

test('append failure exposes no current canvas revision', async () => {
  const f = await fixture();
  const running = await start(f.rootDir, f.stateDir, f.workspaceRoot, {
    appendEvent: async () => {
      const error = new Error('synthetic append failure');
      error.code = 'synthetic_append_failure';
      throw error;
    }
  });
  try {
    const failed = await publish(running.base, {
      path: f.relative,
      title: 'Failed append',
      kind: 'presentation'
    });
    assert.equal(failed.response.status, 500);
    assert.deepEqual((await request(running.base, '/api/canvas/current')).body, { current: null });
  } finally {
    await close(running.server);
    await rm(f.stateDir, { recursive: true, force: true });
    await rm(f.workspaceRoot, { recursive: true, force: true });
  }
});
