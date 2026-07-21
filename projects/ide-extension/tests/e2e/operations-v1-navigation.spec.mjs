import { expect, test } from '@playwright/test';
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer } from '../../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const screenshotDir = path.join(
  projectRoot,
  'development/operations-v1-plan/task-sessions/20260714T230133Z-swu-ov1-010/assets'
);

function listen(server, port = 0) {
  return new Promise((resolve) => {
    server.listen(port, '127.0.0.1', () => resolve(server.address().port));
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
    body: text ? JSON.parse(text) : null
  };
}

function post(base, route, body) {
  return request(base, route, { method: 'POST', body: JSON.stringify(body) });
}

function interactiveHtml() {
  return `<!doctype html><html><head><title>Operations browser witness</title></head><body>
    <main><h1 id="version">Revision 1</h1><button id="counter" type="button">0</button>
      <button id="send-event" type="button">Choose</button></main>
    <script>
      document.querySelector('#counter').onclick = (event) => {
        event.target.textContent = String(Number(event.target.textContent) + 1);
      };
      document.querySelector('#send-event').onclick = () => parent.postMessage({
        type: 'ide-extension.canvas.event',
        eventName: 'decision.selected',
        payload: { value: 'approve', source: 'operations-browser' }
      }, '*');
    <\/script>
  </body></html>`;
}

function target(derived) {
  return {
    kind: 'surface_revision',
    surface_kind: 'operations_v1',
    surface_id: derived.surface.operations_surface_id,
    revision_id: derived.revision.revision_id
  };
}

function operationInput(derived, operationId, fragment) {
  return {
    schema_version: '1',
    operation_id: operationId,
    operations_surface_id: derived.surface.operations_surface_id,
    expected_revision_id: derived.revision.revision_id,
    mode: 'append',
    target: { kind: 'whole_document' },
    input: { kind: 'inline_html', html: fragment }
  };
}

async function waitForCommand(base, commandId, expectedStatus) {
  await expect.poll(async () => {
    const result = await request(
      base,
      `/api/canvas/navigation/${encodeURIComponent(commandId)}`
    );
    return result.response.ok ? result.body.command.status : result.response.status;
  }).toBe(expectedStatus);
}

test('workbench delivers durable Operations display without losing the last good frame', async ({ page }, testInfo) => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-navigation-e2e-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-navigation-e2e-workspace-'));
  const relative = 'generated/navigation-witness.html';
  const file = path.join(workspaceRoot, relative);
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, interactiveHtml(), 'utf8');

  let server = createServer({ rootDir: projectRoot, stateDir, workspaceRoot });
  await server.ready;
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;

  try {
    const published = await post(base, '/api/canvas/publish', {
      schema_version: '1',
      path: relative,
      title: 'Operations browser witness',
      kind: 'presentation'
    });
    expect(published.response.status).toBe(201);
    const v0 = published.body.current;

    const derive = (key) => post(base, '/api/canvas/operation-surfaces', {
      schema_version: '1',
      source_v0_surface_id: v0.surface_id,
      source_revision_id: v0.revision.revision_id,
      operation_surface_idempotency_key: key
    });
    const derivedA = (await derive('derive-browser-navigation-a')).body;
    const derivedB = (await derive('derive-browser-navigation-b')).body;

    await page.goto(`${base}/demo/l0`);
    if (testInfo.project.name === 'mobile') {
      await page.getByRole('tab', { name: 'Canvas', exact: true }).click();
    }
    await expect(page.locator('#canvas-live-status')).toHaveText('Live');
    await expect(page.locator('#canvas-status')).toHaveText('Available');
    await expect(page.locator('#canvas-frame')).toHaveAttribute('data-surface-kind', 'v0');
    await expect(page.frameLocator('#canvas-frame').locator('#version')).toHaveText('Revision 1');

    const selectA = 'command-browser-select-a';
    const selectedA = await post(base, '/api/canvas/navigation', {
      schema_version: '1',
      command_id: selectA,
      action: 'redirect',
      destination: target(derivedA)
    });
    expect(selectedA.response.status).toBe(201);
    await expect(page.locator('#canvas-frame')).toHaveAttribute(
      'data-surface-id',
      derivedA.surface.operations_surface_id
    );
    await waitForCommand(base, selectA, 'loaded');
    await expect(page.locator('#canvas-open')).toHaveAttribute('href', derivedA.content_url);

    await page.frameLocator('#canvas-frame').locator('#send-event').click();
    await expect(page.locator('#canvas-event-status')).toHaveText('Sent');
    await expect.poll(async () => {
      const state = (await request(base, '/api/state')).body;
      return state.canvas.operations_v1.interactions.length;
    }).toBe(1);

    const nonSelected = await post(
      base,
      `/api/canvas/operation-surfaces/${derivedB.surface.operations_surface_id}/operations`,
      operationInput(
        derivedB,
        'operation-browser-non-selected',
        '<section id="non-selected">Not selected</section>'
      )
    );
    expect(nonSelected.response.status).toBe(201);
    await page.waitForTimeout(150);
    await expect(page.locator('#canvas-frame')).toHaveAttribute(
      'data-revision-id',
      derivedA.revision.revision_id
    );
    await expect(page.frameLocator('#canvas-frame').locator('#non-selected')).toHaveCount(0);

    const selected = await post(
      base,
      `/api/canvas/operation-surfaces/${derivedA.surface.operations_surface_id}/operations`,
      operationInput(
        derivedA,
        'operation-browser-selected',
        `<section id="appended"><button id="appended-action" type="button">idle</button></section>
          <script>document.querySelector('#appended-action').onclick = (event) => {
            event.target.textContent = 'active';
          };<\/script>`
      )
    );
    expect(selected.response.status).toBe(201);
    await expect(page.locator('#canvas-frame')).toHaveAttribute(
      'data-revision-id',
      selected.body.revision.revision_id
    );
    await page.frameLocator('#canvas-frame').locator('#appended-action').click();
    await expect(page.frameLocator('#canvas-frame').locator('#appended-action')).toHaveText('active');
    await expect(page.locator('#canvas-open')).toHaveAttribute('href', selected.body.content_url);

    await page.frameLocator('#canvas-frame').locator('#counter').click();
    await expect(page.frameLocator('#canvas-frame').locator('#counter')).toHaveText('1');
    const navigationResponse = page.waitForResponse((response) => (
      response.url() === `${base}/api/canvas/navigation`
      && response.request().method() === 'POST'
    ));
    await page.locator('[data-action="canvas-refresh"]').click();
    const manualRefresh = await (await navigationResponse).json();
    await expect(page.frameLocator('#canvas-frame').locator('#counter')).toHaveText('0');
    await waitForCommand(base, manualRefresh.command.command_id, 'loaded');

    const retainedRevision = selected.body.revision.revision_id;
    await page.route(`**${nonSelected.body.content_url}`, (route) => route.abort());
    const failedCommand = 'command-browser-failed-target';
    const failedRedirect = await post(base, '/api/canvas/navigation', {
      schema_version: '1',
      command_id: failedCommand,
      action: 'redirect',
      destination: {
        ...target(derivedB),
        revision_id: nonSelected.body.revision.revision_id
      }
    });
    expect(failedRedirect.response.status).toBe(201);
    await waitForCommand(base, failedCommand, 'failed');
    await expect(page.locator('#canvas-frame')).toHaveAttribute('data-revision-id', retainedRevision);
    await expect(page.frameLocator('#canvas-frame').locator('#appended-action')).toHaveText('idle');

    await page.unroute(`**${nonSelected.body.content_url}`);
    const selectB = 'command-browser-select-b';
    await post(base, '/api/canvas/navigation', {
      schema_version: '1',
      command_id: selectB,
      action: 'redirect',
      destination: {
        ...target(derivedB),
        revision_id: nonSelected.body.revision.revision_id
      }
    });
    await expect(page.locator('#canvas-frame')).toHaveAttribute(
      'data-revision-id',
      nonSelected.body.revision.revision_id
    );
    await expect(page.frameLocator('#canvas-frame').locator('#non-selected')).toHaveText('Not selected');
    await waitForCommand(base, selectB, 'loaded');
    await expect(page.locator('#canvas-open')).toHaveAttribute('href', nonSelected.body.content_url);

    await page.locator('#canvas-frame').evaluate((frame) => {
      frame.dataset.restartMarker = 'retained';
    });
    await close(server);
    await expect(page.locator('#canvas-live-status')).toHaveText('Reconnecting');
    server = createServer({ rootDir: projectRoot, stateDir, workspaceRoot });
    await server.ready;
    await listen(server, port);
    await expect(page.locator('#canvas-live-status')).toHaveText('Live');
    await expect(page.locator('#canvas-frame')).toHaveAttribute('data-restart-marker', 'retained');
    await expect(page.frameLocator('#canvas-frame').locator('#non-selected')).toHaveText('Not selected');

    const layout = await page.evaluate(() => {
      const stage = document.querySelector('#canvas-stage').getBoundingClientRect();
      const frames = [...document.querySelectorAll('.canvas-frame')];
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
        frameCount: frames.length,
        visibleFrameCount: frames.filter((frame) => getComputedStyle(frame).visibility !== 'hidden').length,
        stageWidth: stage.width,
        stageHeight: stage.height,
        overlaps
      };
    });
    expect(layout.overflow).toBe(false);
    expect(layout.frameCount).toBe(1);
    expect(layout.visibleFrameCount).toBe(1);
    expect(layout.stageWidth).toBeGreaterThan(300);
    expect(layout.stageHeight).toBeGreaterThan(450);
    expect(layout.overlaps).toBe(false);

    await mkdir(screenshotDir, { recursive: true });
    const screenshot = await page.screenshot({
      path: path.join(screenshotDir, `${testInfo.project.name}-operations-navigation.png`),
      fullPage: true
    });
    expect(screenshot.byteLength).toBeGreaterThan(10_000);
  } finally {
    if (server.listening) await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
  }
});
