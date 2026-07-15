import assert from 'node:assert/strict';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { appendEvent } from '../src/kernel/audit.mjs';
import { htmlTransformEngine } from '../src/kernel/html-transform.mjs';
import { OPERATIONS_V1_LIMITS } from '../src/kernel/operations-contracts.mjs';
import { atomicWriteJson } from '../src/kernel/storage.mjs';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const INITIAL_HTML = '<!doctype html><html><head><title>Append</title></head><body><main id="base">Base</main></body></html>';

function listen(server) {
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve(server.address().port));
  });
}

function close(server) {
  return new Promise((resolve, reject) => {
    server.close((error) => error ? reject(error) : resolve());
  });
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
      : Buffer.from(await response.arrayBuffer())
  };
}

function post(base, route, body) {
  return request(base, route, { method: 'POST', body: JSON.stringify(body) });
}

async function fixture(prefix = 'ide-extension-operations-append-', bytes = Buffer.from(INITIAL_HTML)) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), `${prefix}state-`));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), `${prefix}workspace-`));
  const relative = 'presentations/source.html';
  const file = path.join(workspaceRoot, relative);
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, bytes);
  return { stateDir, workspaceRoot, relative, file };
}

async function start(f, options = {}) {
  const server = createServer({
    rootDir: projectRoot,
    stateDir: f.stateDir,
    workspaceRoot: f.workspaceRoot,
    ...options
  });
  await server.ready;
  const port = await listen(server);
  return { server, base: `http://127.0.0.1:${port}` };
}

async function cleanup(f, running) {
  if (running?.server.listening) await close(running.server);
  await rm(f.stateDir, { recursive: true, force: true });
  await rm(f.workspaceRoot, { recursive: true, force: true });
}

async function publishAndDerive(running, f, key = 'derive-append-source') {
  const published = await post(running.base, '/api/canvas/publish', {
    schema_version: '1',
    path: f.relative,
    title: 'Append source',
    kind: 'generic'
  });
  const v0 = published.body.current;
  const derived = await post(running.base, '/api/canvas/operation-surfaces', {
    schema_version: '1',
    source_v0_surface_id: v0.surface_id,
    source_revision_id: v0.revision.revision_id,
    operation_surface_idempotency_key: key
  });
  return { v0, derived: derived.body };
}

function operationInput(surface, expectedRevisionId, operationId, html, mode = 'append') {
  return {
    schema_version: '1',
    operation_id: operationId,
    operations_surface_id: surface.operations_surface_id,
    expected_revision_id: expectedRevisionId,
    mode,
    target: { kind: 'whole_document' },
    input: { kind: 'inline_html', html }
  };
}

function operate(base, surfaceId, body) {
  return post(
    base,
    `/api/canvas/operation-surfaces/${encodeURIComponent(surfaceId)}/operations`,
    body
  );
}

test('appends the body-context parser corpus in exact serialized order', async () => {
  const f = await fixture();
  let running;
  try {
    running = await start(f);
    const { v0, derived } = await publishAndDerive(running, f);
    const fragments = [
      '',
      'plain text<span id="one">One</span><strong id="two">Two</strong>',
      '<style id="appended-style">.added{color:red}</style><script id="appended-script">window.__appendLoaded=true</script>',
      '<div id="malformed"><em>open',
      '<tr><td id="table-like">Cell</td></tr>',
      '<!--append-marker-->Ol\u00e1 \u4e16\u754c',
      '<svg id="vector"><circle cx="4" cy="4" r="2"></circle></svg><math id="formula"><mi>x</mi></math>'
    ];
    let surface = derived.surface;
    let revision = derived.revision;
    let expectedHtml = INITIAL_HTML;

    for (const [index, fragment] of fragments.entries()) {
      const expected = htmlTransformEngine.append(expectedHtml, fragment);
      const appended = await operate(
        running.base,
        surface.operations_surface_id,
        operationInput(surface, revision.revision_id, `operation-corpus-${index}`, fragment)
      );
      assert.equal(appended.response.status, 201);
      assert.equal(appended.body.operation.mode, 'append');
      assert.deepEqual((await request(running.base, appended.body.content_url)).body, expected.bytes);
      surface = appended.body.surface;
      revision = appended.body.revision;
      expectedHtml = expected.html;
    }

    assert.equal(surface.revision_ids.length, fragments.length + 1);
    assert.ok(expectedHtml.indexOf('id="one"') < expectedHtml.indexOf('id="two"'));
    assert.match(expectedHtml, /append-marker/);
    assert.match(expectedHtml, /Ol\u00e1 \u4e16\u754c/);
    assert.match(expectedHtml, /<svg id="vector"/);
    assert.match(expectedHtml, /<math id="formula"/);
    assert.equal(
      (await request(running.base, '/api/canvas/current')).body.current.revision.revision_id,
      v0.revision.revision_id
    );
  } finally {
    await cleanup(f, running);
  }
});

test('appends exactly once across retry, conflict, stale input, and concurrent writers', async () => {
  const f = await fixture('ide-extension-operations-append-retry-');
  let running;
  try {
    running = await start(f);
    const { derived } = await publishAndDerive(running, f, 'derive-append-retry');
    const surfaceId = derived.surface.operations_surface_id;
    const firstInput = operationInput(
      derived.surface,
      derived.revision.revision_id,
      'operation-append-once',
      '<p id="once">Once</p>'
    );
    const first = (await operate(running.base, surfaceId, firstInput)).body;
    const second = (await operate(
      running.base,
      surfaceId,
      operationInput(first.surface, first.revision.revision_id, 'operation-append-second', '<p id="second">Second</p>')
    )).body;

    const retry = await operate(running.base, surfaceId, firstInput);
    assert.equal(retry.response.status, 200);
    assert.equal(retry.body.idempotent, true);
    assert.deepEqual(retry.body.surface, first.surface);
    assert.equal(retry.body.revision.revision_id, first.revision.revision_id);

    const conflict = await operate(running.base, surfaceId, {
      ...firstInput,
      input: { kind: 'inline_html', html: '<p>Different</p>' }
    });
    assert.equal(conflict.response.status, 409);
    assert.equal(conflict.body.error, 'operation_id_conflict');

    const stale = await operate(
      running.base,
      surfaceId,
      operationInput(second.surface, derived.revision.revision_id, 'operation-append-stale', '<p>Stale</p>')
    );
    assert.equal(stale.response.status, 409);
    assert.equal(stale.body.error, 'revision_changed');

    const attempts = await Promise.all([
      operate(running.base, surfaceId, operationInput(
        second.surface,
        second.revision.revision_id,
        'operation-append-race-a',
        '<p id="race-a">A</p>'
      )),
      operate(running.base, surfaceId, operationInput(
        second.surface,
        second.revision.revision_id,
        'operation-append-race-b',
        '<p id="race-b">B</p>'
      ))
    ]);
    assert.equal(attempts.filter(({ response }) => response.status === 201).length, 1);
    assert.equal(attempts.filter(({ response }) => response.status === 409).length, 1);
    const state = (await request(running.base, '/api/state')).body;
    assert.equal(Object.keys(state.canvas.operations_v1.operations).length, 3);
    assert.equal(state.canvas.operations_v1.surfaces[surfaceId].revision_ids.length, 4);
  } finally {
    await cleanup(f, running);
  }
});

test('rejects fragment/result overflow and invalid UTF-8 current content without events', async () => {
  const f = await fixture('ide-extension-operations-append-limits-');
  let running;
  try {
    running = await start(f);
    const { derived } = await publishAndDerive(running, f, 'derive-append-limits');
    const surfaceId = derived.surface.operations_surface_id;
    const baseline = (await request(running.base, '/api/state')).body.event_count;
    const fragmentLimit = await operate(
      running.base,
      surfaceId,
      operationInput(
        derived.surface,
        derived.revision.revision_id,
        'operation-fragment-limit',
        'x'.repeat(OPERATIONS_V1_LIMITS.fragment_html_bytes + 1)
      )
    );
    assert.equal(fragmentLimit.response.status, 413);
    assert.equal(fragmentLimit.body.limit_name, 'fragment_html');
    assert.equal((await request(running.base, '/api/state')).body.event_count, baseline);

    const nearLimitHtml = `<!doctype html><p>${'&'.repeat(1_400_000)}</p>`;
    const replacement = await operate(
      running.base,
      surfaceId,
      operationInput(
        derived.surface,
        derived.revision.revision_id,
        'operation-near-result-limit',
        nearLimitHtml,
        'replace'
      )
    );
    assert.equal(replacement.response.status, 201);
    const beforeOverflow = (await request(running.base, '/api/state')).body.event_count;
    const resultLimit = await operate(
      running.base,
      surfaceId,
      operationInput(
        replacement.body.surface,
        replacement.body.revision.revision_id,
        'operation-append-result-limit',
        '&'.repeat(300_000)
      )
    );
    assert.equal(resultLimit.response.status, 413);
    assert.equal(resultLimit.body.limit_name, 'result_html');
    assert.equal((await request(running.base, '/api/state')).body.event_count, beforeOverflow);
  } finally {
    await cleanup(f, running);
  }

  const invalid = await fixture(
    'ide-extension-operations-append-invalid-utf8-',
    Buffer.from([0xff, 0xfe, 0x3c, 0x70, 0x3e])
  );
  let invalidRunning;
  try {
    invalidRunning = await start(invalid);
    const { derived } = await publishAndDerive(invalidRunning, invalid, 'derive-invalid-utf8');
    const before = (await request(invalidRunning.base, '/api/state')).body.event_count;
    const rejected = await operate(
      invalidRunning.base,
      derived.surface.operations_surface_id,
      operationInput(derived.surface, derived.revision.revision_id, 'operation-invalid-utf8', '<p>x</p>')
    );
    assert.equal(rejected.response.status, 422);
    assert.equal(rejected.body.error, 'operations_source_invalid_utf8');
    assert.equal((await request(invalidRunning.base, '/api/state')).body.event_count, before);
  } finally {
    await cleanup(invalid, invalidRunning);
  }
});

test('reports an append-result orphan when event append fails', async () => {
  const f = await fixture('ide-extension-operations-append-orphan-');
  let appendCount = 0;
  const injectedAppend = async (...args) => {
    appendCount += 1;
    if (appendCount === 3) {
      const error = new Error('synthetic append event failure');
      error.code = 'synthetic_append_failure';
      throw error;
    }
    return appendEvent(...args);
  };
  let running;
  try {
    running = await start(f, { appendEvent: injectedAppend });
    const { derived } = await publishAndDerive(running, f, 'derive-append-orphan');
    const fragment = '<p id="orphan">Orphan</p>';
    const failed = await operate(
      running.base,
      derived.surface.operations_surface_id,
      operationInput(derived.surface, derived.revision.revision_id, 'operation-append-orphan', fragment)
    );
    assert.equal(failed.response.status, 500);
    const state = (await request(running.base, '/api/state')).body;
    assert.equal(state.event_count, 2);
    assert.equal(state.reconciliation.canvas_blobs.unreferenced_blobs.length, 1);
    assert.equal(
      state.reconciliation.canvas_blobs.unreferenced_blobs[0],
      htmlTransformEngine.append(INITIAL_HTML, fragment).sha256
    );
  } finally {
    await cleanup(f, running);
  }
});

test('repairs an appended operation after projection failure', async () => {
  const f = await fixture('ide-extension-operations-append-recovery-');
  let writeCount = 0;
  const writeProjection = async (...args) => {
    writeCount += 1;
    if (writeCount === 4) {
      const error = new Error('synthetic append projection failure');
      error.code = 'EIO';
      throw error;
    }
    return atomicWriteJson(...args);
  };
  let running;
  try {
    running = await start(f, { writeProjection });
    const { derived } = await publishAndDerive(running, f, 'derive-append-recovery');
    const fragment = '<button id="recovered">Recovered</button>';
    const interrupted = await operate(
      running.base,
      derived.surface.operations_surface_id,
      operationInput(derived.surface, derived.revision.revision_id, 'operation-append-recovery', fragment)
    );
    assert.equal(interrupted.response.status, 503);
    const state = (await request(running.base, '/api/state')).body;
    const operation = state.canvas.operations_v1.operations['operation-append-recovery'];
    const contentUrl = `/api/canvas/operation-surfaces/${derived.surface.operations_surface_id}`
      + `/revisions/${operation.result_revision_id}/content`;
    assert.equal(state.event_count, 3);
    assert.deepEqual(
      (await request(running.base, contentUrl)).body,
      htmlTransformEngine.append(INITIAL_HTML, fragment).bytes
    );
    assert.equal(state.reconciliation.canvas_blobs.unreferenced_blobs.length, 0);
  } finally {
    await cleanup(f, running);
  }
});
