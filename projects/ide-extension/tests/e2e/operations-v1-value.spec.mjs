import { spawn } from 'node:child_process';
import { expect, test } from '@playwright/test';
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer } from '../../src/server.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const cli = path.join(projectRoot, 'scripts/session-bridge.mjs');
const evidenceDir = path.join(
  projectRoot,
  'development/operations-v1-plan/task-sessions/20260715T004506Z-swu-ov1-013/assets'
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
      const error = Buffer.concat(stderr).toString('utf8');
      if (code !== 0) {
        reject(new Error(`CLI failed (${code}): ${error}`));
        return;
      }
      resolve(JSON.parse(Buffer.concat(stdout).toString('utf8')));
    });
    child.stdin.end(input);
  });
}

async function request(base, route) {
  const response = await fetch(`${base}${route}`);
  return { response, body: JSON.parse(await response.text()) };
}

async function waitForCommand(base, commandId, status) {
  await expect.poll(async () => {
    const result = await request(
      base,
      `/api/canvas/navigation/${encodeURIComponent(commandId)}`
    );
    return result.response.ok ? result.body.command.status : result.response.status;
  }).toBe(status);
}

function draftHtml() {
  return `<!doctype html><html><head><title>Cyber Alchemy draft</title></head>
    <body><main><h1>Cyber Alchemy</h1><p>Draft presentation</p></main></body></html>`;
}

function presentationHtml() {
  return `<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Cyber Alchemy Workbench</title><style>
      *{box-sizing:border-box}body{margin:0;background:#f4f6f8;color:#18202a;font-family:Arial,sans-serif}
      main{min-height:100vh;padding:clamp(20px,5vw,64px);display:grid;align-content:center;gap:24px}
      header{display:flex;align-items:center;gap:16px;border-bottom:3px solid #d54b35;padding-bottom:16px}
      header img{width:64px;height:64px}.eyebrow{color:#196a63;font-weight:700;text-transform:uppercase}
      h1{font-size:clamp(32px,6vw,72px);margin:0;line-height:1.05}p{font-size:clamp(17px,2vw,24px);max-width:760px}
      .slide{display:none}.slide.active{display:block}.controls{display:flex;gap:12px;flex-wrap:wrap}
      button{border:0;background:#18202a;color:white;padding:12px 18px;font:inherit;font-weight:700;cursor:pointer}
      button.accent{background:#d54b35}output{align-self:center;font-weight:700;color:#196a63}
    </style></head><body><main>
      <header><img id="alchemy-logo" src="/assets/cyber-alchemy-logo.svg" alt="Cyber Alchemy logo">
        <div><div class="eyebrow">Agent to workbench</div><h1>Cyber Alchemy</h1></div></header>
      <section class="slide active" data-slide="1"><h2>Build the artifact</h2>
        <p>The agent commits complete HTML revisions. The workbench displays exactly what was committed.</p></section>
      <section class="slide" data-slide="2"><h2>Keep the conversation alive</h2>
        <p>The user can inspect, interact, decide, and send a generic event back into the session.</p></section>
      <div class="controls"><button id="next-slide" type="button">Next idea</button>
        <button id="send-decision" class="accent" type="button">Approve direction</button>
        <output id="deck-status">Slide 1</output></div>
    </main><script>
      let slide = 1;
      document.querySelector('#next-slide').onclick = () => {
        slide = slide === 1 ? 2 : 1;
        document.querySelectorAll('.slide').forEach((item) => item.classList.toggle('active', item.dataset.slide === String(slide)));
        document.querySelector('#deck-status').textContent = 'Slide ' + slide;
      };
      document.querySelector('#send-decision').onclick = () => parent.postMessage({
        type: 'ide-extension.canvas.event', eventName: 'decision.selected',
        payload: { decision_id: 'DEC-VALUE-WITNESS', value: 'approve', source: 'operations-value' }
      }, '*');
    <\/script></body></html>`;
}

function appendFragment() {
  return `<section id="agent-added"><h2>Added by the agent</h2>
    <button id="append-proof" type="button">Run appended control</button>
    <output id="append-status">idle</output></section>
    <script>document.querySelector('#append-proof').onclick = () => {
      document.querySelector('#append-status').textContent = 'active';
    };<\/script>`;
}

test('agent CLI sends an interactive presentation to the durable workbench', async ({ page }, testInfo) => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-value-e2e-state-'));
  const workspaceRoot = await mkdtemp(path.join(os.tmpdir(), 'ide-extension-value-e2e-workspace-'));
  const relative = 'presentations/cyber-alchemy.html';
  await mkdir(path.join(workspaceRoot, 'presentations'));
  await writeFile(path.join(workspaceRoot, relative), draftHtml(), 'utf8');
  let server = createServer({ rootDir: projectRoot, stateDir, workspaceRoot });
  await server.ready;
  const port = await listen(server);
  const base = `http://127.0.0.1:${port}`;

  try {
    const published = await runCli([
      'publish', '--base-url', base, '--path', relative,
      '--title', 'Cyber Alchemy Workbench', '--kind', 'presentation'
    ]);
    const derived = await runCli([
      'derive', '--base-url', base,
      '--source-surface-id', published.current.surface_id,
      '--source-revision-id', published.current.revision.revision_id,
      '--idempotency-key', `derive-value-${testInfo.project.name}`
    ]);
    const replaced = await runCli([
      'operate', '--base-url', base,
      '--surface-id', derived.surface.operations_surface_id, '--input', '-'
    ], JSON.stringify({
      schema_version: '1',
      operation_id: `operation-value-replace-${testInfo.project.name}`,
      operations_surface_id: derived.surface.operations_surface_id,
      expected_revision_id: derived.revision.revision_id,
      mode: 'replace',
      target: { kind: 'whole_document' },
      input: { kind: 'inline_html', html: presentationHtml() }
    }));
    const appended = await runCli([
      'operate', '--base-url', base,
      '--surface-id', derived.surface.operations_surface_id, '--input', '-'
    ], JSON.stringify({
      schema_version: '1',
      operation_id: `operation-value-append-${testInfo.project.name}`,
      operations_surface_id: derived.surface.operations_surface_id,
      expected_revision_id: replaced.revision.revision_id,
      mode: 'append',
      target: { kind: 'whole_document' },
      input: { kind: 'inline_html', html: appendFragment() }
    }));

    await page.goto(`${base}/demo/l0`);
    await expect(page.locator('#canvas-live-status')).toHaveText('Live');
    await expect(page.locator('#canvas-frame')).toHaveAttribute('data-surface-kind', 'v0');

    const commandId = `command-value-${testInfo.project.name}`;
    const navigated = await runCli([
      'navigate', '--base-url', base, '--input', '-'
    ], JSON.stringify({
      schema_version: '1', command_id: commandId, action: 'redirect',
      destination: {
        kind: 'surface_revision', surface_kind: 'operations_v1',
        surface_id: derived.surface.operations_surface_id,
        revision_id: appended.revision.revision_id
      }
    }));
    expect(navigated.command.command_id).toBe(commandId);
    await expect(page.locator('#canvas-frame')).toHaveAttribute(
      'data-revision-id',
      appended.revision.revision_id
    );
    await waitForCommand(base, commandId, 'loaded');

    const frame = page.frameLocator('#canvas-frame');
    await expect(frame.locator('h1')).toHaveText('Cyber Alchemy');
    await expect(frame.locator('#agent-added')).toBeVisible();
    await expect(frame.locator('#alchemy-logo')).toHaveJSProperty('complete', true);
    await frame.locator('#next-slide').click();
    await expect(frame.locator('#deck-status')).toHaveText('Slide 2');
    await frame.locator('#append-proof').click();
    await expect(frame.locator('#append-status')).toHaveText('active');
    await frame.locator('#send-decision').click();
    await expect(page.locator('#canvas-event-status')).toHaveText('Sent');

    await expect.poll(async () => {
      const projected = (await request(base, '/api/state')).body.canvas.operations_v1;
      return projected.interaction_cursor;
    }).toBe(1);
    const beforeRestart = (await request(base, '/api/state')).body.canvas.operations_v1;
    expect(beforeRestart.interactions[0].payload.value).toBe('approve');

    await close(server);
    server = createServer({ rootDir: projectRoot, stateDir, workspaceRoot });
    await server.ready;
    await listen(server, port);
    await page.reload();
    await expect(page.locator('#canvas-live-status')).toHaveText('Live');
    await expect(page.locator('#canvas-frame')).toHaveAttribute(
      'data-revision-id',
      appended.revision.revision_id
    );
    await expect(frame.locator('#agent-added')).toBeVisible();
    await expect(frame.locator('#append-status')).toHaveText('idle');

    const layout = await page.evaluate(() => ({
      overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      frameWidth: document.querySelector('#canvas-frame').getBoundingClientRect().width,
      frameHeight: document.querySelector('#canvas-frame').getBoundingClientRect().height
    }));
    expect(layout.overflow).toBe(false);
    expect(layout.frameWidth).toBeGreaterThan(250);
    expect(layout.frameHeight).toBeGreaterThan(400);

    await mkdir(evidenceDir, { recursive: true });
    const screenshotName = `${testInfo.project.name}-operations-value.png`;
    const screenshot = await page.screenshot({
      path: path.join(evidenceDir, screenshotName),
      fullPage: true
    });
    expect(screenshot.byteLength).toBeGreaterThan(10_000);
    await writeFile(
      path.join(evidenceDir, `${testInfo.project.name}-operations-value.json`),
      `${JSON.stringify({
        schema_version: '1',
        project: testInfo.project.name,
        commands: ['publish', 'derive', 'operate:replace', 'operate:append', 'navigate'],
        v0: {
          surface_id: published.current.surface_id,
          revision_id: published.current.revision.revision_id,
          content_sha256: published.current.revision.content_sha256
        },
        operations: {
          surface_id: derived.surface.operations_surface_id,
          revision_ids: [
            derived.revision.revision_id,
            replaced.revision.revision_id,
            appended.revision.revision_id
          ],
          final_revision_id: appended.revision.revision_id,
          final_content_sha256: appended.revision.content_sha256
        },
        navigation: { command_id: commandId, status: 'loaded' },
        interaction: beforeRestart.interactions[0],
        restart: { recovered_revision_id: appended.revision.revision_id },
        screenshot: `assets/${screenshotName}`
      }, null, 2)}\n`,
      'utf8'
    );
  } finally {
    if (server.listening) await close(server);
    await rm(stateDir, { recursive: true, force: true });
    await rm(workspaceRoot, { recursive: true, force: true });
  }
});
