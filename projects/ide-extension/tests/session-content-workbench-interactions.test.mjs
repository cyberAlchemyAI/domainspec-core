import assert from 'node:assert/strict';
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { appendEvent } from '../src/kernel/audit.mjs';
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
  return { response, body: JSON.parse(await response.text()) };
}

function post(base, route, body) {
  return request(base, route, { method: 'POST', body: JSON.stringify(body) });
}

async function setup(options = {}) {
  const rootDir = path.resolve(new URL('..', import.meta.url).pathname);
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-events-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-events-workspace-'));
  const relative = 'surfaces/interaction.html';
  await mkdir(path.join(workspaceRoot, 'surfaces'));
  await writeFile(path.join(workspaceRoot, relative), '<h1>Interaction</h1>', 'utf8');
  const server = createServer({ rootDir, stateDir, workspaceRoot, ...options });
  await server.ready;
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;
  const published = await post(base, '/api/canvas/publish', {
    schema_version: '1', path: relative, title: 'Interaction', kind: 'generic'
  });
  return { rootDir, stateDir, workspaceRoot, server, base, current: published.body.current };
}

function interaction(current, eventName = 'decision.selected', payload = { value: 'approve' }) {
  return {
    schema_version: '1',
    surface_id: current.surface_id,
    revision_id: current.revision.revision_id,
    event_name: eventName,
    payload
  };
}

async function cleanup(fixture) {
  if (fixture.server.listening) await close(fixture.server);
  await rm(fixture.stateDir, { recursive: true, force: true });
  await rm(fixture.workspaceRoot, { recursive: true, force: true });
}

test('admits current interactions and returns stable ordered cursor polls across restart', async () => {
  const f = await setup();
  try {
    assert.deepEqual((await request(f.base, '/api/canvas/events?after=0')).body, {
      schema_version: '1', events: [], next_cursor: 0
    });

    const [first, second] = await Promise.all([
      post(f.base, '/api/canvas/events', interaction(f.current)),
      post(f.base, '/api/canvas/events', interaction(
        f.current,
        'craft.action_requested',
        { task_id: 'TASK-1', action: 'start' }
      ))
    ]);
    assert.equal(first.response.status, 201);
    assert.equal(second.response.status, 201);

    const initialPoll = (await request(f.base, '/api/canvas/events?after=0')).body;
    assert.deepEqual(initialPoll.events.map(({ cursor }) => cursor), [1, 2]);
    assert.equal(new Set(initialPoll.events.map(({ event_id }) => event_id)).size, 2);
    assert.equal(initialPoll.next_cursor, 2);
    assert.deepEqual((await request(f.base, '/api/canvas/events?after=0')).body, initialPoll);
    assert.deepEqual(
      (await request(f.base, '/api/canvas/events?after=1')).body.events.map(({ cursor }) => cursor),
      [2]
    );
    assert.deepEqual((await request(f.base, '/api/canvas/events?after=99')).body, {
      schema_version: '1', events: [], next_cursor: 99
    });

    await close(f.server);
    f.server = createServer({ rootDir: f.rootDir, stateDir: f.stateDir, workspaceRoot: f.workspaceRoot });
    await f.server.ready;
    const port = await listen(f.server);
    f.base = `http://127.0.0.1:${port}`;
    assert.deepEqual((await request(f.base, '/api/canvas/events?after=0')).body, initialPoll);
  } finally {
    await cleanup(f);
  }
});

test('rejects stale, malformed, oversized, and invalid-cursor input without appending', async () => {
  const f = await setup();
  try {
    const stale = interaction(f.current);
    stale.revision_id = 'revision-stale';
    assert.equal((await post(f.base, '/api/canvas/events', stale)).response.status, 409);

    const arrayPayload = interaction(f.current);
    arrayPayload.payload = [];
    assert.equal((await post(f.base, '/api/canvas/events', arrayPayload)).response.status, 400);

    const oversized = interaction(f.current, 'generic.large', { text: 'x'.repeat(17_000) });
    const oversizedResponse = await fetch(`${f.base}/api/canvas/events`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(oversized)
    });
    assert.equal(oversizedResponse.status, 413);
    assert.equal((await oversizedResponse.json()).error, 'request_too_large');

    for (const cursor of ['-1', '1.5', 'abc', '1&after=2']) {
      assert.equal((await request(f.base, `/api/canvas/events?after=${cursor}`)).response.status, 400);
    }
    assert.deepEqual((await request(f.base, '/api/canvas/events?after=0')).body.events, []);
  } finally {
    await cleanup(f);
  }
});

test('append failure leaves no pollable interaction and permits explicit retry', async () => {
  let failInteraction = false;
  const f = await setup({
    appendEvent: async (file, event) => {
      if (failInteraction && event.event_type === 'canvas.interaction_recorded') {
        const error = new Error('synthetic interaction append failure');
        error.code = 'synthetic_append_failure';
        throw error;
      }
      return appendEvent(file, event);
    }
  });
  try {
    failInteraction = true;
    assert.equal((await post(f.base, '/api/canvas/events', interaction(f.current))).response.status, 500);
    assert.deepEqual((await request(f.base, '/api/canvas/events?after=0')).body.events, []);
    failInteraction = false;
    const retried = await post(f.base, '/api/canvas/events', interaction(f.current));
    assert.equal(retried.response.status, 201);
    assert.equal(retried.body.interaction.cursor, 1);
  } finally {
    await cleanup(f);
  }
});
