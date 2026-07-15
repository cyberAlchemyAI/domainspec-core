import { expect, test } from '@playwright/test';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer } from '../../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));

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

test('an appended trusted-local control executes from the committed complete revision', async ({ page }) => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-append-e2e-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-append-e2e-workspace-'));
  const relative = 'canvas/append.html';
  await mkdir(path.join(workspaceRoot, 'canvas'));
  await writeFile(
    path.join(workspaceRoot, relative),
    '<!doctype html><html><head><title>Append witness</title></head><body><h1>Append witness</h1><main id="base">Base</main></body></html>',
    'utf8'
  );
  const server = createServer({ rootDir: projectRoot, stateDir, workspaceRoot });
  await server.ready;
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;

  try {
    const published = await fetch(`${base}/api/canvas/publish`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        schema_version: '1',
        path: relative,
        title: 'Append witness',
        kind: 'generic'
      })
    });
    expect(published.status).toBe(201);
    const current = (await published.json()).current;
    const derivedResponse = await fetch(`${base}/api/canvas/operation-surfaces`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        schema_version: '1',
        source_v0_surface_id: current.surface_id,
        source_revision_id: current.revision.revision_id,
        operation_surface_idempotency_key: 'derive-append-browser'
      })
    });
    expect(derivedResponse.status).toBe(201);
    const derived = await derivedResponse.json();
    const fragment = [
      '<section id="appended">',
      '<button id="activate" type="button">Activate</button>',
      '<output id="status">idle</output>',
      '</section>',
      '<script>',
      "document.querySelector('#activate').addEventListener('click', () => {",
      "document.querySelector('#status').textContent = 'active';",
      "document.body.dataset.appendWitness = 'passed';",
      '});',
      '</script>'
    ].join('');
    const operatedResponse = await fetch(
      `${base}/api/canvas/operation-surfaces/${derived.surface.operations_surface_id}/operations`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          schema_version: '1',
          operation_id: 'operation-append-browser',
          operations_surface_id: derived.surface.operations_surface_id,
          expected_revision_id: derived.revision.revision_id,
          mode: 'append',
          target: { kind: 'whole_document' },
          input: { kind: 'inline_html', html: fragment }
        })
      }
    );
    expect(operatedResponse.status).toBe(201);
    const operated = await operatedResponse.json();

    await page.goto(`${base}${operated.content_url}`);
    await expect(page.locator('body > *')).toHaveCount(4);
    await expect(page.locator('#base')).toHaveText('Base');
    await expect(page.locator('#status')).toHaveText('idle');
    await page.locator('#activate').click();
    await expect(page.locator('#status')).toHaveText('active');
    await expect(page.locator('body')).toHaveAttribute('data-append-witness', 'passed');
  } finally {
    await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
  }
});
