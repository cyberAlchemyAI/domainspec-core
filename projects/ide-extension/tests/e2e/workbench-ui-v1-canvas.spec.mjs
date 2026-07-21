import { expect, test } from '@playwright/test';
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer } from '../../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const screenshotDir = path.join(
  projectRoot,
  'development/workbench-ui-v1/task-sessions/20260720T165903Z-swu-wui-008'
);

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

async function request(base, route, options = {}) {
  const response = await fetch(`${base}${route}`, {
    ...options,
    headers: { 'content-type': 'application/json', ...(options.headers || {}) }
  });
  const text = await response.text();
  return {
    response,
    body: text ? JSON.parse(text) : null
  };
}

function canvasHtml(version) {
  return `<!doctype html><html><head><title>WUI Canvas ${version}</title></head><body>
    <main><h1 id="canvas-version">${version}</h1>
      <button id="counter" type="button">0</button>
    </main>
    <script>
      document.querySelector('#counter').addEventListener('click', (event) => {
        event.target.textContent = String(Number(event.target.textContent) + 1);
      });
    <\/script>
  </body></html>`;
}

test('primary Canvas keeps revision identity and the last good frame on failed navigation', async ({ page }, testInfo) => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-wui008-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-wui008-workspace-'));
  const relativePath = 'generated/wui-008-canvas.html';
  const filePath = path.join(workspaceRoot, relativePath);
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, canvasHtml('Revision A'), 'utf8');

  let server = createServer({ rootDir: projectRoot, stateDir, workspaceRoot });
  await server.ready;
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;

  try {
    const firstPublish = await request(base, '/api/canvas/publish', {
      method: 'POST',
      body: JSON.stringify({
        schema_version: '1',
        path: relativePath,
        title: 'WUI-008 Primary Canvas',
        kind: 'presentation'
      })
    });
    expect(firstPublish.response.status).toBe(201);
    const first = firstPublish.body.current;

    await page.goto(`${base}/demo/l0`);
    await expect(page.locator('#canvas-live-status')).toHaveText('Live');
    await expect(page.locator('#canvas-status')).toHaveText('Available');
    await expect(page.locator('#canvas-title')).toHaveText('WUI-008 Primary Canvas');
    await expect(page.locator('#canvas-meta')).toContainText(first.revision.revision_id);
    await expect(page.locator('#canvas-frame')).toHaveAttribute('data-surface-id', first.surface_id);
    await expect(page.locator('#canvas-frame')).toHaveAttribute('data-revision-id', first.revision.revision_id);
    await expect(page.frameLocator('#canvas-frame').locator('#canvas-version')).toHaveText('Revision A');

    if (testInfo.project.name === 'mobile') {
      await page.getByRole('tab', { name: 'Canvas', exact: true }).click();
      await expect(page.locator('#canvas-region')).toBeVisible();
      await expect(page.locator('#work-region')).toBeHidden();
      await expect(page.locator('#evidence-region')).toBeHidden();
      await expect(page.getByRole('tab', { name: 'Canvas', exact: true })).toHaveAttribute('aria-selected', 'true');
    }
    const placement = await page.evaluate(() => {
      const visible = (element) => {
        const rect = element.getBoundingClientRect();
        return getComputedStyle(element).display !== 'none'
          && getComputedStyle(element).visibility !== 'hidden'
          && rect.width > 0
          && rect.height > 0;
      };
      const work = document.querySelector('[data-region="work"]').getBoundingClientRect();
      const canvas = document.querySelector('[data-region="canvas"]').getBoundingClientRect();
      const inspector = document.querySelector('.inspector-column').getBoundingClientRect();
      return {
        canvasPrimary: canvas.left >= work.right - 1 && canvas.right <= inspector.left + 1,
        canvasWidth: canvas.width,
        canvasHeight: canvas.height,
        frameVisible: visible(document.querySelector('#canvas-frame')),
        horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
      };
    });
    if (testInfo.project.name === 'mobile') {
      expect(placement.horizontalOverflow).toBe(false);
      expect(placement.frameVisible).toBe(true);
    } else {
      expect(placement.canvasPrimary).toBe(true);
      expect(placement.canvasWidth).toBeGreaterThan(500);
      expect(placement.canvasHeight).toBeGreaterThan(450);
      expect(placement.horizontalOverflow).toBe(false);
    }

    const firstFrame = page.frameLocator('#canvas-frame');
    await firstFrame.locator('#counter').click();
    await expect(firstFrame.locator('#counter')).toHaveText('1');

    await writeFile(filePath, canvasHtml('Revision B'), 'utf8');
    await page.route(/\/api\/canvas\/surfaces\/[^/]+\/revisions\/[^/]+\/content$/, (route) => route.abort());
    const secondPublish = await request(base, '/api/canvas/publish', {
      method: 'POST',
      body: JSON.stringify({
        schema_version: '1',
        path: relativePath,
        title: 'WUI-008 Primary Canvas',
        kind: 'presentation'
      })
    });
    expect(secondPublish.response.status).toBe(201);
    const second = secondPublish.body.current;
    expect(second.revision.revision_id).not.toBe(first.revision.revision_id);

    await expect(page.locator('#canvas-status')).toHaveText('Unavailable');
    await expect(page.locator('#canvas-frame')).toHaveAttribute('data-revision-id', first.revision.revision_id);
    await expect(page.locator('#canvas-meta')).toContainText(first.revision.revision_id);
    await expect(page.frameLocator('#canvas-frame').locator('#canvas-version')).toHaveText('Revision A');
    await expect(page.frameLocator('#canvas-frame').locator('#counter')).toHaveText('1');

    await page.unroute(/\/api\/canvas\/surfaces\/[^/]+\/revisions\/[^/]+\/content$/);
    await page.locator('[data-action="canvas-refresh"]').click();
    await expect(page.locator('#canvas-status')).toHaveText('Available');
    await expect(page.locator('#canvas-frame')).toHaveAttribute('data-revision-id', second.revision.revision_id);
    await expect(page.locator('#canvas-meta')).toContainText(second.revision.revision_id);
    await expect(page.frameLocator('#canvas-frame').locator('#canvas-version')).toHaveText('Revision B');

    await mkdir(screenshotDir, { recursive: true });
    const screenshot = await page.screenshot({
      path: path.join(screenshotDir, `${testInfo.project.name}-canvas.png`),
      fullPage: true
    });
    expect(screenshot.byteLength).toBeGreaterThan(10_000);
  } finally {
    await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
  }
});
