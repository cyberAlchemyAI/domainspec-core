import { expect, test } from '@playwright/test';
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer } from '../../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const screenshotDir = path.join(
  projectRoot,
  'development/operations-v1-plan/task-sessions/20260714T232409Z-swu-ov1-011/assets'
);
const policy = Object.freeze({
  soft_bytes: 2500,
  hard_bytes: 10000,
  grace_ms: 7 * 24 * 60 * 60 * 1000,
  reclaim_below_bytes: 2500
});

function html(label, fill) {
  return `<!doctype html><html><head><title>${label}</title></head><body>`
    + `<main><h1>${label}</h1><p>${fill.repeat(1800)}</p></main></body></html>`;
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

async function request(base, route, options = {}) {
  const response = await fetch(`${base}${route}`, {
    ...options,
    headers: { 'content-type': 'application/json', ...(options.headers || {}) }
  });
  const text = await response.text();
  return {
    response,
    body: text && response.headers.get('content-type')?.includes('application/json')
      ? JSON.parse(text)
      : text
  };
}

function post(base, route, body) {
  return request(base, route, { method: 'POST', body: JSON.stringify(body) });
}

test('workbench previews and manually prunes replay-proven history', async ({ page }, testInfo) => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-retention-e2e-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-retention-e2e-workspace-'));
  const relative = 'generated/retention-source.html';
  const file = path.join(workspaceRoot, relative);
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, html('Retention source', 's'), 'utf8');

  let identifier = 0;
  let clock = Date.parse('2026-07-14T23:40:00.000Z');
  const server = createServer({
    rootDir: projectRoot,
    stateDir,
    workspaceRoot,
    retentionPolicy: policy,
    retentionNow: () => {
      const value = new Date(clock).toISOString();
      clock += 1000;
      return value;
    },
    retentionRandomId: () => `browser-${++identifier}`
  });
  await server.ready;
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;

  try {
    const published = await post(base, '/api/canvas/publish', {
      schema_version: '1',
      path: relative,
      title: 'Retention source',
      kind: 'presentation'
    });
    const derived = await post(base, '/api/canvas/operation-surfaces', {
      schema_version: '1',
      source_v0_surface_id: published.body.current.surface_id,
      source_revision_id: published.body.current.revision.revision_id,
      operation_surface_idempotency_key: 'derive-retention-browser'
    });
    expect(derived.response.status).toBe(201);

    await page.goto(`${base}/demo/l0`);
    await expect(page.locator('#canvas-live-status')).toHaveText('Live');
    await expect(page.locator('#canvas-storage-status')).toContainText('Normal');
    await expect(page.locator('[data-action="canvas-pruning-preview"]')).toBeHidden();

    const operation = await post(
      base,
      `/api/canvas/operation-surfaces/${derived.body.surface.operations_surface_id}/operations`,
      {
        schema_version: '1',
        operation_id: 'operation-retention-browser-replace',
        operations_surface_id: derived.body.surface.operations_surface_id,
        expected_revision_id: derived.body.revision.revision_id,
        mode: 'replace',
        target: { kind: 'whole_document' },
        input: { kind: 'inline_html', html: html('Retention current', 'c') }
      }
    );
    expect(operation.response.status).toBe(201);
    const opened = await request(base, '/api/canvas/storage');
    expect(opened.body.storage.state).toBe('grace');

    await expect(page.locator('#canvas-storage-status')).toContainText('Grace active');
    await expect(page.locator('#canvas-storage-meta')).toContainText('1 eligible');
    const previewButton = page.locator('[data-action="canvas-pruning-preview"]');
    await expect(previewButton).toBeVisible();

    const previewResponse = page.waitForResponse((response) => (
      response.url() === `${base}/api/canvas/pruning/preview`
      && response.request().method() === 'POST'
    ));
    await previewButton.click();
    const preview = await (await previewResponse).json();
    expect(preview.candidate.selected_revision_ids).toEqual([derived.body.revision.revision_id]);
    const commitButton = page.locator('[data-action="canvas-pruning-commit"]');
    await expect(commitButton).toHaveText('Prune 1 revision');

    const layout = await page.evaluate(() => {
      const storage = document.querySelector('[data-panel="canvas-storage"]').getBoundingClientRect();
      const controls = [...document.querySelectorAll('.canvas-storage-actions > :not([hidden])')]
        .map((element) => {
          const rect = element.getBoundingClientRect();
          return { left: rect.left, right: rect.right, top: rect.top, bottom: rect.bottom };
        });
      const overlaps = controls.some((left, index) => controls.some((right, other) => (
        other > index
        && left.left < right.right
        && left.right > right.left
        && left.top < right.bottom
        && left.bottom > right.top
      )));
      return {
        overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
        width: storage.width,
        height: storage.height,
        overlaps
      };
    });
    expect(layout.overflow).toBe(false);
    expect(layout.width).toBeGreaterThan(300);
    expect(layout.height).toBeGreaterThan(40);
    expect(layout.overlaps).toBe(false);

    await mkdir(screenshotDir, { recursive: true });
    const screenshot = await page.screenshot({
      path: path.join(screenshotDir, `${testInfo.project.name}-retention-preview.png`),
      fullPage: true
    });
    expect(screenshot.byteLength).toBeGreaterThan(10_000);

    page.once('dialog', (dialog) => dialog.accept());
    const commitResponse = page.waitForResponse((response) => (
      response.url() === `${base}/api/canvas/pruning/commit`
      && response.request().method() === 'POST'
    ));
    await commitButton.click();
    expect((await commitResponse).status()).toBe(201);
    await expect(page.locator('#canvas-storage-status')).toContainText('Normal');
    await expect(previewButton).toBeHidden();
    await expect(commitButton).toBeHidden();

    const oldContent = await request(base, derived.body.content_url);
    expect(oldContent.response.status).toBe(410);
    expect(oldContent.body.error).toBe('revision_pruned');
    expect(oldContent.body.tombstone.reason).toBe('manual');
  } finally {
    if (server.listening) await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
  }
});
