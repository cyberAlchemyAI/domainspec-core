import assert from 'node:assert/strict';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
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

function runCli(args) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [cli, ...args], { cwd: projectRoot });
    const stdout = [];
    const stderr = [];
    child.stdout.on('data', (chunk) => stdout.push(chunk));
    child.stderr.on('data', (chunk) => stderr.push(chunk));
    child.on('error', reject);
    child.on('close', (code) => resolve({
      code,
      stdout: Buffer.concat(stdout).toString('utf8'),
      stderr: Buffer.concat(stderr).toString('utf8')
    }));
  });
}

test('publishes project HTML through one bounded CLI process', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-canvas-cli-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-canvas-cli-workspace-'));
  await mkdir(path.join(workspaceRoot, 'slides'));
  await writeFile(path.join(workspaceRoot, 'slides/demo.html'), '<h1>CLI canvas</h1>', 'utf8');
  const server = createServer({ rootDir: projectRoot, stateDir, workspaceRoot });
  await server.ready;
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;
  try {
    const result = await runCli([
      'publish', '--base-url', base,
      '--path', 'slides/demo.html',
      '--title', 'CLI canvas',
      '--kind', 'presentation'
    ]);
    assert.equal(result.code, 0);
    assert.equal(result.stderr, '');
    const current = JSON.parse(result.stdout).current;
    assert.equal(current.path, 'slides/demo.html');

    const admitted = await fetch(`${base}/api/canvas/events`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        schema_version: '1',
        surface_id: current.surface_id,
        revision_id: current.revision.revision_id,
        event_name: 'decision.selected',
        payload: { value: 'approve' }
      })
    });
    assert.equal(admitted.status, 201);
    const apiPoll = await (await fetch(`${base}/api/canvas/events?after=0`)).json();
    const cliPoll = await runCli(['events', '--base-url', base, '--after', '0']);
    assert.equal(cliPoll.code, 0);
    assert.equal(cliPoll.stderr, '');
    assert.deepEqual(JSON.parse(cliPoll.stdout), apiPoll);

    const emptyPoll = await runCli(['events', '--base-url', base, '--after', '1']);
    assert.deepEqual(JSON.parse(emptyPoll.stdout), {
      schema_version: '1', events: [], next_cursor: 1
    });

    const invalidCursor = await runCli(['events', '--base-url', base, '--after', '-1']);
    assert.equal(invalidCursor.code, 2);
    assert.equal(JSON.parse(invalidCursor.stderr).error, 'invalid_arguments');

    const invalid = await runCli(['publish', '--base-url', base, '--path', 'slides/demo.html']);
    assert.equal(invalid.code, 2);
    assert.equal(JSON.parse(invalid.stderr).error, 'invalid_arguments');
  } finally {
    await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
  }
});
