import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { createServer } from '../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const cli = path.join(projectRoot, 'scripts/session-bridge.mjs');
const POLICY = Object.freeze({
  soft_bytes: 2500,
  hard_bytes: 10000,
  grace_ms: 100000,
  reclaim_below_bytes: 2500
});

function html(title, fill = 'x') {
  return `<!doctype html><html><head><title>${title}</title></head><body>`
    + `<main><h1>${title}</h1><p>${fill.repeat(1800)}</p></main></body></html>`;
}

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
    }, 5000);
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

async function successfulCli(args, input = '') {
  const result = await runCli(args, input);
  assert.equal(result.code, 0, result.stderr);
  assert.equal(result.stderr, '');
  return JSON.parse(result.stdout);
}

test('runs the complete Operations value workflow through one-shot JSON commands', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-value-cli-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-value-cli-workspace-'));
  const relative = 'presentations/value.html';
  await mkdir(path.join(workspaceRoot, 'presentations'));
  await writeFile(path.join(workspaceRoot, relative), html('Value draft', 'd'), 'utf8');
  const server = createServer({
    rootDir: projectRoot,
    stateDir,
    workspaceRoot,
    retentionPolicy: POLICY,
    retentionNow: () => '2026-07-15T00:50:00.000Z'
  });
  await server.ready;
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;

  try {
    const published = await successfulCli([
      'publish', '--base-url', base,
      '--path', relative,
      '--title', 'Operations value witness',
      '--kind', 'presentation'
    ]);
    const derived = await successfulCli([
      'derive', '--base-url', base,
      '--source-surface-id', published.current.surface_id,
      '--source-revision-id', published.current.revision.revision_id,
      '--idempotency-key', 'derive-value-cli'
    ]);

    const replacementInput = {
      schema_version: '1',
      operation_id: 'operation-value-replace',
      operations_surface_id: derived.surface.operations_surface_id,
      expected_revision_id: derived.revision.revision_id,
      mode: 'replace',
      target: { kind: 'whole_document' },
      input: { kind: 'inline_html', html: html('Value presentation', 'r') }
    };
    const replaced = await successfulCli([
      'operate', '--base-url', base,
      '--surface-id', derived.surface.operations_surface_id,
      '--input', '-'
    ], JSON.stringify(replacementInput));

    const appendInput = {
      schema_version: '1',
      operation_id: 'operation-value-append',
      operations_surface_id: derived.surface.operations_surface_id,
      expected_revision_id: replaced.revision.revision_id,
      mode: 'append',
      target: { kind: 'whole_document' },
      input: {
        kind: 'inline_html',
        html: '<section id="value-added"><button type="button">Approve</button></section>'
      }
    };
    const appended = await successfulCli([
      'operate', '--base-url', base,
      '--surface-id', derived.surface.operations_surface_id,
      '--input', '-'
    ], JSON.stringify(appendInput));

    const navigationInput = {
      schema_version: '1',
      command_id: 'command-value-navigate',
      action: 'redirect',
      destination: {
        kind: 'surface_revision',
        surface_kind: 'operations_v1',
        surface_id: derived.surface.operations_surface_id,
        revision_id: appended.revision.revision_id
      }
    };
    const navigated = await successfulCli([
      'navigate', '--base-url', base, '--input', '-'
    ], JSON.stringify(navigationInput));
    assert.equal(navigated.command.command_id, navigationInput.command_id);

    const storage = await successfulCli(['storage', '--base-url', base]);
    assert.equal(storage.storage.state, 'grace');
    assert.equal(storage.storage.candidate_revision_count >= 1, true);

    const preview = await successfulCli([
      'prune', '--base-url', base,
      '--action', 'preview', '--input', '-'
    ], JSON.stringify({
      schema_version: '1', command_id: 'command-value-prune-preview'
    }));
    assert.equal(preview.candidate.selected_revision_ids.includes(appended.revision.revision_id), false);
    const committed = await successfulCli([
      'prune', '--base-url', base,
      '--action', 'commit', '--input', '-'
    ], JSON.stringify({
      schema_version: '1',
      command_id: 'command-value-prune-commit',
      expected_candidate_digest: preview.candidate.candidate_digest
    }));
    assert.equal(committed.pruned_revisions.length >= 1, true);
    assert.equal(committed.storage.state, 'normal');

    const display = await (await fetch(`${base}/api/canvas/display`)).json();
    assert.equal(display.display.revision_id, appended.revision.revision_id);
    assert.equal(display.display.revision.content_sha256, appended.revision.content_sha256);
    assert.equal((await fetch(`${base}${appended.content_url}`)).status, 200);

    const invalidPrune = await runCli([
      'prune', '--base-url', base, '--action', 'erase', '--input', '-'
    ], '{}');
    assert.equal(invalidPrune.code, 2);
    assert.equal(JSON.parse(invalidPrune.stderr).error, 'invalid_arguments');
    const invalidStorage = await runCli(['storage', '--base-url', base, '--input', '-']);
    assert.equal(invalidStorage.code, 2);
  } finally {
    await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
  }
});
