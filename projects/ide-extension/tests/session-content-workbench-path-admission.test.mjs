import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdir, mkdtemp, realpath, rm, symlink, unlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { readWorkspaceHtml } from '../src/kernel/canvas.mjs';
import { createServer } from '../src/server.mjs';

async function symlinkOrSkip(t, target, linkPath, type = 'file') {
  try {
    await symlink(target, linkPath, type);
    return true;
  } catch (error) {
    if (['EPERM', 'EACCES', 'ENOSYS'].includes(error.code)) {
      t.skip(`symlinks unavailable: ${error.code}`);
      return false;
    }
    throw error;
  }
}

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

function publish(base, pathName, title = 'Path admission') {
  return request(base, '/api/canvas/publish', {
    method: 'POST',
    body: JSON.stringify({
      schema_version: '1',
      path: pathName,
      title,
      kind: 'generic'
    })
  });
}

test('reads regular and in-root linked HTML through the canonical target', async (t) => {
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-path-workspace-'));
  try {
    await mkdir(path.join(workspaceRoot, 'pages'));
    const target = path.join(workspaceRoot, 'pages', 'inside.html');
    const bytes = Buffer.from('<!doctype html><title>Inside</title>');
    await writeFile(target, bytes);

    const direct = await readWorkspaceHtml(workspaceRoot, 'pages/inside.html');
    assert.equal(direct.absolute_path, await realpath(target));
    assert.deepEqual(direct.bytes, bytes);
    assert.equal(direct.content_sha256, createHash('sha256').update(bytes).digest('hex'));

    const linked = path.join(workspaceRoot, 'pages', 'linked.html');
    if (!await symlinkOrSkip(t, 'inside.html', linked)) return;
    const admitted = await readWorkspaceHtml(workspaceRoot, 'pages/linked.html');
    assert.equal(admitted.path, 'pages/linked.html');
    assert.equal(admitted.absolute_path, await realpath(target));
    assert.deepEqual(admitted.bytes, bytes);
  } finally {
    await rm(workspaceRoot, { recursive: true, force: true });
  }
});

test('rejects final and nested links whose canonical target is outside the workspace', async (t) => {
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-path-workspace-'));
  const externalRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-path-external-'));
  try {
    await mkdir(path.join(workspaceRoot, 'pages'));
    const secret = path.join(externalRoot, 'secret.html');
    await writeFile(secret, '<!doctype html><title>Secret</title>');

    const finalLink = path.join(workspaceRoot, 'pages', 'external.html');
    if (!await symlinkOrSkip(t, secret, finalLink)) return;
    await assert.rejects(
      readWorkspaceHtml(workspaceRoot, 'pages/external.html'),
      (error) => error.code === 'canvas_path_escape'
    );

    const nestedLink = path.join(workspaceRoot, 'linked-directory');
    if (!await symlinkOrSkip(t, externalRoot, nestedLink, 'dir')) return;
    await assert.rejects(
      readWorkspaceHtml(workspaceRoot, 'linked-directory/secret.html'),
      (error) => error.code === 'canvas_path_escape'
    );
  } finally {
    await rm(workspaceRoot, { recursive: true, force: true });
    await rm(externalRoot, { recursive: true, force: true });
  }
});

test('publish rejects external final and nested links without appending events', async (t) => {
  const rootDir = path.resolve(new URL('..', import.meta.url).pathname);
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-path-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-path-workspace-'));
  const externalRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-path-external-'));
  let server;
  try {
    await mkdir(path.join(workspaceRoot, 'pages'));
    const secret = path.join(externalRoot, 'secret.html');
    await writeFile(secret, '<!doctype html><title>Secret</title>');
    if (!await symlinkOrSkip(t, secret, path.join(workspaceRoot, 'pages', 'external.html'))) return;
    if (!await symlinkOrSkip(t, externalRoot, path.join(workspaceRoot, 'linked-directory'), 'dir')) return;

    server = createServer({ rootDir, stateDir, workspaceRoot });
    await server.ready;
    const port = await listen(server);
    const base = `http://127.0.0.1:${port}`;

    for (const pathName of ['pages/external.html', 'linked-directory/secret.html']) {
      const rejected = await publish(base, pathName);
      assert.equal(rejected.response.status, 400);
      assert.equal(rejected.body.error, 'canvas_path_escape');
    }
    const state = (await request(base, '/api/state')).body;
    assert.equal(state.event_count, 0);
    assert.deepEqual((await request(base, '/api/canvas/current')).body, { current: null });
  } finally {
    if (server?.listening) await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
    await rm(externalRoot, { recursive: true, force: true });
  }
});

test('publish preserves bounded missing-file and non-file responses', async () => {
  const rootDir = path.resolve(new URL('..', import.meta.url).pathname);
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-path-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-path-workspace-'));
  let server;
  try {
    await mkdir(path.join(workspaceRoot, 'pages'));
    await mkdir(path.join(workspaceRoot, 'pages', 'folder.html'));
    server = createServer({ rootDir, stateDir, workspaceRoot });
    await server.ready;
    const port = await listen(server);
    const base = `http://127.0.0.1:${port}`;

    const missing = await publish(base, 'pages/missing.html');
    assert.equal(missing.response.status, 404);
    assert.equal(missing.body.error, 'canvas_file_not_found');

    const directory = await publish(base, 'pages/folder.html');
    assert.equal(directory.response.status, 400);
    assert.equal(directory.body.error, 'canvas_not_file');

    assert.equal((await request(base, '/api/state')).body.event_count, 0);
  } finally {
    if (server?.listening) await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
  }
});

test('a published in-root link retargeted outside becomes unavailable without leaking bytes', async (t) => {
  const rootDir = path.resolve(new URL('..', import.meta.url).pathname);
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-path-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-path-workspace-'));
  const externalRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-path-external-'));
  let server;
  try {
    await mkdir(path.join(workspaceRoot, 'pages'));
    await writeFile(path.join(workspaceRoot, 'pages', 'inside.html'), '<!doctype html><title>Inside</title>');
    const link = path.join(workspaceRoot, 'pages', 'current.html');
    if (!await symlinkOrSkip(t, 'inside.html', link)) return;

    const secretBody = '<!doctype html><title>Outside secret</title>';
    const secret = path.join(externalRoot, 'secret.html');
    await writeFile(secret, secretBody);

    server = createServer({ rootDir, stateDir, workspaceRoot });
    await server.ready;
    const port = await listen(server);
    const base = `http://127.0.0.1:${port}`;
    const published = await publish(base, 'pages/current.html', 'Linked page');
    assert.equal(published.response.status, 201);
    const available = await request(base, published.body.current.content_url);
    assert.equal(available.response.status, 200);
    assert.equal(available.body.includes('<title>Inside</title>'), true);

    await unlink(link);
    await symlink(secret, link);
    const unavailable = await request(base, published.body.current.content_url);
    assert.equal(unavailable.response.status, 404);
    assert.deepEqual(unavailable.body, { error: 'canvas_file_unavailable' });
    assert.equal(JSON.stringify(unavailable.body).includes(secretBody), false);
    assert.equal(JSON.stringify(unavailable.body).includes(externalRoot), false);
  } finally {
    if (server?.listening) await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
    await rm(externalRoot, { recursive: true, force: true });
  }
});
