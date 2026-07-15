import { expect, test } from '@playwright/test';
import { spawn } from 'node:child_process';
import { copyFile, mkdir, mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer } from '../../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const fixtureDir = path.join(projectRoot, 'tests/fixtures/canvas');
const cli = path.join(projectRoot, 'scripts/session-bridge.mjs');
const screenshotDir = path.join(
  projectRoot,
  'development/session-content-workbench-plan/work-pack/evidence/SWU-SCW-007-assets'
);

function listen(server) {
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server.address().port)));
}

function close(server) {
  return new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}

function runCli(base, after) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [cli, 'events', '--base-url', base, '--after', String(after)], {
      cwd: projectRoot
    });
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

test('presentation, Decision Gate, and Craft use one publish and event loop', async ({ page }, testInfo) => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-matrix-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-matrix-workspace-'));
  await mkdir(path.join(workspaceRoot, 'canvas'));
  for (const name of ['presentation.html', 'decision.html', 'craft.html']) {
    await copyFile(path.join(fixtureDir, name), path.join(workspaceRoot, 'canvas', name));
  }

  const server = createServer({ rootDir: projectRoot, stateDir, workspaceRoot });
  await server.ready;
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;
  const publish = async (name, title, kind) => {
    const response = await fetch(`${base}/api/canvas/publish`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ schema_version: '1', path: `canvas/${name}`, title, kind })
    });
    expect(response.status).toBe(201);
    return response.json();
  };

  try {
    await mkdir(screenshotDir, { recursive: true });
    await publish('presentation.html', 'Local Canvas Field Notes', 'presentation');
    await page.goto(`${base}/demo/l0`);
    let frame = page.frameLocator('#canvas-frame');
    await expect(frame.locator('h1').filter({ hasText: 'A shared visual workbench for Augmentor' })).toBeVisible();
    await frame.locator('body').click();
    await page.keyboard.press('ArrowRight');
    await expect(frame.locator('#counter')).toHaveText('2 / 6');
    await frame.locator('#previous').click();
    await expect(frame.locator('#counter')).toHaveText('1 / 6');

    await copyFile(
      path.join(fixtureDir, 'presentation-v2.html'),
      path.join(workspaceRoot, 'canvas/presentation.html')
    );
    await publish('presentation.html', 'Local Canvas Field Notes - Revised', 'presentation');
    frame = page.frameLocator('#canvas-frame');
    await expect(frame.locator('h2').filter({ hasText: 'updated without a refresh' })).toBeVisible();
    await page.screenshot({
      path: path.join(screenshotDir, `${testInfo.project.name}-presentation.png`), fullPage: true
    });

    await publish('decision.html', 'Decision Gate', 'decision');
    frame = page.frameLocator('#canvas-frame');
    await expect(frame.locator('h1')).toHaveText('Decision Gate');
    await frame.locator('[data-value="manual-first"]').click();
    await expect(page.locator('#canvas-event-status')).toHaveText('Sent');
    await page.screenshot({
      path: path.join(screenshotDir, `${testInfo.project.name}-decision.png`), fullPage: true
    });

    await page.reload();
    await expect(page.locator('#canvas-live-status')).toHaveText('Live');
    const decisionPoll = await runCli(base, 0);
    expect(decisionPoll.code).toBe(0);
    expect(decisionPoll.stderr).toBe('');
    const decision = JSON.parse(decisionPoll.stdout);
    expect(decision.events).toHaveLength(1);
    expect(decision.events[0].event_name).toBe('decision.selected');
    expect(decision.events[0].payload).toEqual({ decision_id: 'DG-MATRIX-001', value: 'manual-first' });
    expect(JSON.parse((await runCli(base, 0)).stdout)).toEqual(decision);

    await publish('craft.html', 'Craft Work Queue', 'craft');
    frame = page.frameLocator('#canvas-frame');
    await expect(frame.locator('h1')).toHaveText('Craft Work Queue');
    await frame.locator('[data-task="CRAFT-MATRIX-001"] [data-action="start"]').click();
    await expect(page.locator('#canvas-event-status')).toHaveText('Sent');
    await frame.locator('[data-task="CRAFT-MATRIX-002"] [data-action="defer"]').click();
    await expect(page.locator('#canvas-event-status')).toHaveText('Sent');
    await page.screenshot({
      path: path.join(screenshotDir, `${testInfo.project.name}-craft.png`), fullPage: true
    });

    await page.reload();
    const craftPoll = JSON.parse((await runCli(base, decision.next_cursor)).stdout);
    expect(craftPoll.events).toHaveLength(2);
    expect(craftPoll.events.map(({ event_name: eventName }) => eventName)).toEqual([
      'craft.action_requested', 'craft.action_requested'
    ]);
    expect(craftPoll.events.map(({ payload }) => payload)).toEqual([
      { task_id: 'CRAFT-MATRIX-001', action: 'start' },
      { task_id: 'CRAFT-MATRIX-002', action: 'defer' }
    ]);
    expect(new Set([...decision.events, ...craftPoll.events].map(({ event_id: id }) => id)).size).toBe(3);
  } finally {
    await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
  }
});
