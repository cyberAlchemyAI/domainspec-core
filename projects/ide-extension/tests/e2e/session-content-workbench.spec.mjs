import { expect, test } from '@playwright/test';
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer } from '../../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const screenshotDir = path.join(
  projectRoot,
  'development/session-content-workbench-plan/work-pack/evidence/SWU-SCW-004-assets'
);
const liveScreenshotDir = path.join(
  projectRoot,
  'development/session-content-workbench-plan/work-pack/evidence/SWU-SCW-005-assets'
);
const presentationPath =
  'arcanum/development/craft/teaching/craft-causal-class-2026-07-11/CRAFT-CAUSAL-CLASS-PRESENTATION.html';

test('manual Refresh displays and operates the real Craft presentation', async ({ page, request }, testInfo) => {
  const published = await request.post('/api/canvas/publish', {
    data: {
      schema_version: '1',
      path: presentationPath,
      title: 'The Wobble We Chose',
      kind: 'presentation'
    }
  });
  expect(published.ok()).toBeTruthy();
  expect([200, 201]).toContain(published.status());

  await page.goto('/demo/l0');
  await expect(page.locator('#server-status')).toHaveText('Connected');
  await expect(page.locator('#canvas-status')).toHaveText('Available');
  await expect(page.locator('#canvas-title')).toHaveText('The Wobble We Chose');
  await expect(page.locator('#canvas-frame')).toBeVisible();

  const frame = page.frameLocator('#canvas-frame');
  await expect(frame.locator('#counter')).toHaveText('1 / 5');
  await expect(frame.locator('#title-0')).toHaveText('What Would You Need to Build This Table?');
  await frame.locator('[data-reveal-index="0"]').click();
  await frame.locator('[data-reveal-index="0"]').click();
  await expect(frame.locator('.slide.active .visible-list')).toContainText('materials');

  const layout = await page.evaluate(() => {
    const canvas = document.querySelector('[data-panel="canvas"]').getBoundingClientRect();
    const frameRect = document.querySelector('#canvas-frame').getBoundingClientRect();
    const controls = [...document.querySelectorAll('.canvas-controls > *')].map((element) => {
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
      canvasWidth: canvas.width,
      frameWidth: frameRect.width,
      frameHeight: frameRect.height,
      overlaps
    };
  });
  expect(layout.overflow).toBe(false);
  expect(layout.canvasWidth).toBeGreaterThan(300);
  expect(layout.frameWidth).toBeGreaterThan(300);
  expect(layout.frameHeight).toBeGreaterThan(450);
  expect(layout.overlaps).toBe(false);

  await mkdir(screenshotDir, { recursive: true });
  const screenshot = await page.screenshot({
    path: path.join(screenshotDir, `${testInfo.project.name}-canvas.png`),
    fullPage: true
  });
  expect(screenshot.byteLength).toBeGreaterThan(10_000);
});

function listen(server, port = 0) {
  return new Promise((resolve) => server.listen(port, '127.0.0.1', () => resolve(server.address().port)));
}

function close(server) {
  return new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}

function generatedHtml(version) {
  return `<!doctype html><html><head><title>Generated ${version}</title></head><body>
    <main><h1 id="version">Revision ${version}</h1><button id="counter" type="button">0</button>
      <button id="send-event" type="button">Choose</button><button id="send-invalid" type="button">Invalid</button></main>
    <script>
      document.querySelector('#counter').onclick = (event) => { event.target.textContent = String(Number(event.target.textContent) + 1); };
      document.querySelector('#send-event').onclick = () => parent.postMessage({ type: 'ide-extension.canvas.event', eventName: 'decision.selected', payload: { version: ${version}, value: 'approve' } }, '*');
      document.querySelector('#send-invalid').onclick = () => parent.postMessage({ type: 'wrong.type', eventName: 'decision.selected', payload: {} }, '*');
    <\/script>
  </body></html>`;
}

test('live Canvas converges after republish, reconnect, restart, and manual fallback', async ({ page }, testInfo) => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-live-e2e-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-live-e2e-workspace-'));
  const relative = 'generated/session-presentation.html';
  const file = path.join(workspaceRoot, relative);
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, generatedHtml(1), 'utf8');

  let server = createServer({ rootDir: projectRoot, stateDir, workspaceRoot });
  await server.ready;
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;
  const publish = (version) => fetch(`${base}/api/canvas/publish`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      schema_version: '1',
      path: relative,
      title: `Generated presentation ${version}`,
      kind: 'presentation'
    })
  });
  let manualPage;

  try {
    expect((await publish(1)).status).toBe(201);
    await page.goto(`${base}/demo/l0`);
    await expect(page.locator('#canvas-live-status')).toHaveText('Live');
    await expect(page.frameLocator('#canvas-frame').locator('#version')).toHaveText('Revision 1');

    await writeFile(file, generatedHtml(2), 'utf8');
    expect((await publish(2)).status).toBe(201);
    await expect(page.frameLocator('#canvas-frame').locator('#version')).toHaveText('Revision 2');
    await page.frameLocator('#canvas-frame').locator('#counter').click();
    await expect(page.frameLocator('#canvas-frame').locator('#counter')).toHaveText('1');

    await page.frameLocator('#canvas-frame').locator('#send-event').click();
    await expect(page.locator('#canvas-event-status')).toHaveText('Sent');
    let interactions = await (await fetch(`${base}/api/canvas/events?after=0`)).json();
    expect(interactions.events).toHaveLength(1);
    expect(interactions.events[0].event_name).toBe('decision.selected');
    expect(interactions.events[0].payload.version).toBe(2);

    await page.evaluate(() => window.postMessage({
      type: 'ide-extension.canvas.event', eventName: 'decision.selected', payload: { source: 'top' }
    }, '*'));
    await page.waitForTimeout(100);
    interactions = await (await fetch(`${base}/api/canvas/events?after=0`)).json();
    expect(interactions.events).toHaveLength(1);

    await page.frameLocator('#canvas-frame').locator('#send-invalid').click();
    await expect(page.locator('#canvas-event-status')).toHaveText('Rejected');
    interactions = await (await fetch(`${base}/api/canvas/events?after=0`)).json();
    expect(interactions.events).toHaveLength(1);

    await page.route('**/api/canvas/events', (route) => route.abort());
    await page.frameLocator('#canvas-frame').locator('#send-event').click();
    await expect(page.locator('#canvas-event-status')).toHaveText('Failed');
    await expect(page.locator('[data-action="canvas-event-retry"]')).toBeVisible();
    await page.unroute('**/api/canvas/events');
    await page.locator('[data-action="canvas-event-retry"]').click();
    await expect(page.locator('#canvas-event-status')).toHaveText('Sent');
    interactions = await (await fetch(`${base}/api/canvas/events?after=1`)).json();
    expect(interactions.events).toHaveLength(1);
    expect(interactions.events[0].cursor).toBe(2);

    await page.locator('#canvas-frame').evaluate((element) => { element.dataset.testMarker = 'stable'; });
    expect((await publish(2)).status).toBe(200);
    await page.waitForTimeout(200);
    await expect(page.locator('#canvas-frame')).toHaveAttribute('data-test-marker', 'stable');

    await close(server);
    await expect(page.locator('#canvas-live-status')).toHaveText('Reconnecting');
    await writeFile(file, generatedHtml(3), 'utf8');
    server = createServer({ rootDir: projectRoot, stateDir, workspaceRoot });
    await server.ready;
    await listen(server, port);
    expect((await publish(3)).status).toBe(201);
    await expect(page.locator('#canvas-live-status')).toHaveText('Live');
    await expect(page.frameLocator('#canvas-frame').locator('#version')).toHaveText('Revision 3');

    manualPage = await page.context().newPage();
    await manualPage.addInitScript(() => { delete window.EventSource; });
    await manualPage.goto(`${base}/demo/l0`);
    await expect(manualPage.locator('#canvas-live-status')).toHaveText('Manual');
    await expect(manualPage.frameLocator('#canvas-frame').locator('#version')).toHaveText('Revision 3');
    await writeFile(file, generatedHtml(4), 'utf8');
    expect((await publish(4)).status).toBe(201);
    await manualPage.waitForTimeout(200);
    await expect(manualPage.frameLocator('#canvas-frame').locator('#version')).toHaveText('Revision 3');
    await manualPage.locator('[data-action="canvas-refresh"]').click();
    await expect(manualPage.frameLocator('#canvas-frame').locator('#version')).toHaveText('Revision 4');

    await mkdir(liveScreenshotDir, { recursive: true });
    const screenshot = await manualPage.screenshot({
      path: path.join(liveScreenshotDir, `${testInfo.project.name}-manual-fallback.png`),
      fullPage: true
    });
    expect(screenshot.byteLength).toBeGreaterThan(10_000);
  } finally {
    await manualPage?.close();
    if (server.listening) await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
  }
});
