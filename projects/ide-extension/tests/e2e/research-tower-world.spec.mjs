import { expect, test } from '@playwright/test';

const WORLD_URL = '/demo/research-tower';

test.beforeEach(async ({ page }) => {
  const ledger = { pageErrors: [], externalRequests: [], mutationRequests: [] };
  page.__calWorldRequestLedger = ledger;
  page.on('pageerror', (error) => ledger.pageErrors.push(error.message));
  page.on('request', (request) => {
    const url = new URL(request.url());
    if (url.hostname !== '127.0.0.1') ledger.externalRequests.push(request.url());
    if (request.method() !== 'GET') ledger.mutationRequests.push(`${request.method()} ${request.url()}`);
  });
});

test.afterEach(async ({ page }) => {
  expect(page.__calWorldRequestLedger).toEqual({ pageErrors: [], externalRequests: [], mutationRequests: [] });
});

async function openWorld(page, suffix = '') {
  await page.goto(`${WORLD_URL}${suffix}`);
  await expect(page.locator('#connection-status')).toHaveText('Locked synthetic witness loaded');
  const firstFloor = page.locator('[data-scene-id="evidence-l0-corpus"]');
  await firstFloor.click();
  const host = page.locator('[data-world-host]');
  await expect(host).toHaveAttribute('data-world-state', 'ready');
  const surface = page.locator('[data-world-surface]');
  await expect(surface).toBeVisible();
  return { firstFloor, host, surface };
}

async function semanticSnapshot(page) {
  return page.evaluate(() => window.__calWorldProbe.getSemanticState());
}

async function projectionState(page) {
  return page.evaluate(() => window.__calWorldProbe.getProjectionState());
}

async function pressTrace(page, surface, keys) {
  await surface.focus();
  for (const key of keys) await page.keyboard.press(key);
  return projectionState(page);
}

async function worldPointToClient(surface, x, y) {
  return surface.evaluate((svg, point) => {
    const candidate = svg.createSVGPoint();
    candidate.x = point.x;
    candidate.y = point.y;
    const client = candidate.matrixTransform(svg.getScreenCTM());
    return { x: client.x, y: client.y };
  }, { x, y });
}

test('world mounts after semantic readiness and remains an optional semantic projection', async ({ page }) => {
  await page.goto(WORLD_URL);
  await expect(page.locator('#connection-status')).toHaveText('Locked synthetic witness loaded');
  await expect(page.locator('[data-world-projection]')).toBeHidden();
  await expect(page.locator('[data-world-surface]')).toHaveCount(0);
  await expect(page.locator('#ontology-candidate-control')).toBeEnabled();

  const { host, surface } = await openWorld(page);
  await expect(page.locator('[data-world-projection]')).toBeVisible();
  await expect(surface).toHaveAttribute('aria-label', /Arrow keys or WASD/);
  await expect(page.locator('[data-world-move]')).toHaveCount(4);
  await expect(page.locator('[data-world-action="activate"]')).toBeEnabled();
  await expect(page.locator('[data-world-action="pause"]')).toBeEnabled();
  expect(await surface.evaluate((node) => node.closest('[aria-hidden="true"]') === null)).toBe(true);
  expect(await page.evaluate(() => window.__calWorldProbe.getLifecycle())).toMatchObject({
    generation: 1,
    activeSubscriptions: 1,
    totalSubscriptions: 1,
    status: 'ready',
    ownedCallbacks: 0
  });

  await page.locator('[data-world-move="down"]').click();
  await expect.poll(() => projectionState(page)).toMatchObject({ pose: { x: 48, y: 72 } });
  await surface.focus();
  await page.keyboard.press('Tab');
  await expect(surface).not.toBeFocused();
  await page.locator('#ontology-candidate-control').focus();
  await expect(page.locator('#ontology-candidate-control')).toBeFocused();

  await expect(host).toHaveAttribute('data-world-state', 'ready');
});

test('real keyboard and pointer geometry move the robot and request the same owned semantic action', async ({ page }) => {
  const { surface } = await openWorld(page);
  const toggle = page.locator('[data-action="toggle-floor-room"]');
  const source = page.locator('[data-source-id="source:toy:l0"]');
  const candidate = page.locator('#ontology-candidate-control');

  const replayTrace = ['ArrowDown', 's', 'ArrowDown', 'ArrowRight', 'd', 'ArrowRight', 'd'];
  const firstReplay = await pressTrace(page, surface, replayTrace);
  expect(firstReplay.pose).toEqual({ x: 80, y: 88 });
  await toggle.click();
  await expect(page.locator('[data-world-surface]')).toHaveCount(0);
  await toggle.click();
  const replaySurface = page.locator('[data-world-surface]');
  await expect(replaySurface).toBeVisible();
  const secondReplay = await pressTrace(page, replaySurface, replayTrace);
  expect(secondReplay).toEqual(firstReplay);

  await toggle.click();
  await toggle.click();
  const collisionSurface = page.locator('[data-world-surface]');
  const collisionState = await pressTrace(page, collisionSurface, Array(6).fill('ArrowRight'));
  expect(collisionState.pose).toEqual({ x: 88, y: 64 });

  await toggle.click();
  await toggle.click();
  const keyboardSurface = page.locator('[data-world-surface]');
  await source.click();
  await expect(source).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-panel="source-detail"]')).toContainText('fixtures/source/toy-tower/levels/L0-corpus.md');
  await pressTrace(page, keyboardSurface, [...Array(3).fill('ArrowDown'), ...Array(11).fill('ArrowRight')]);
  await page.keyboard.press('Enter');
  await expect(candidate).toHaveAttribute('aria-pressed', 'true');
  const keyboardSemantic = await semanticSnapshot(page);
  expect(keyboardSemantic).toMatchObject({ inspectionKind: 'candidate' });

  await source.click();
  await expect(source).toHaveAttribute('aria-pressed', 'true');
  await keyboardSurface.scrollIntoViewIfNeeded();
  const outside = await worldPointToClient(keyboardSurface, 119, 88);
  await page.mouse.click(outside.x, outside.y);
  await expect(source).toHaveAttribute('aria-pressed', 'true');
  const inside = await worldPointToClient(keyboardSurface, 136, 88);
  await page.mouse.click(inside.x, inside.y);
  await expect(candidate).toHaveAttribute('aria-pressed', 'true');
  const pointerSemantic = await semanticSnapshot(page);
  expect(pointerSemantic).toEqual(keyboardSemantic);

  const semanticBeforeCamera = await semanticSnapshot(page);
  await page.evaluate(() => window.__calWorldProbe.setCamera(16, -16));
  await expect.poll(() => projectionState(page)).toMatchObject({ camera: { x: 16, y: -16 } });
  expect(await semanticSnapshot(page)).toEqual(semanticBeforeCamera);
});

test('controlled full wall and occluded hotspot stay non-vacuous in the rendered world', async ({ page }) => {
  let opened = await openWorld(page, '?world_fixture=full-wall');
  const fullWallState = await pressTrace(page, opened.surface, Array(12).fill('ArrowRight'));
  expect(fullWallState.pose).toEqual({ x: 88, y: 64 });

  opened = await openWorld(page, '?world_fixture=occluded');
  const source = page.locator('[data-source-id="source:toy:l0"]');
  await source.click();
  await expect(source).toHaveAttribute('aria-pressed', 'true');
  await opened.surface.scrollIntoViewIfNeeded();
  const inside = await worldPointToClient(opened.surface, 136, 88);
  await page.mouse.click(inside.x, inside.y);
  await expect(source).toHaveAttribute('aria-pressed', 'true');
  expect((await projectionState(page)).active_hotspot_id).toBeNull();
});

test('SVG matrix pointer activation remains correct at device scale factor two', async ({ browser }, testInfo) => {
  const context = await browser.newContext({
    baseURL: testInfo.project.use.baseURL,
    viewport: { width: 960, height: 720 },
    deviceScaleFactor: 2
  });
  const page = await context.newPage();
  const ledger = { pageErrors: [], externalRequests: [], mutationRequests: [] };
  page.on('pageerror', (error) => ledger.pageErrors.push(error.message));
  page.on('request', (request) => {
    const url = new URL(request.url());
    if (url.hostname !== '127.0.0.1') ledger.externalRequests.push(request.url());
    if (request.method() !== 'GET') ledger.mutationRequests.push(`${request.method()} ${request.url()}`);
  });
  try {
    const { surface } = await openWorld(page);
    expect(await page.evaluate(() => devicePixelRatio)).toBe(2);
    const source = page.locator('[data-source-id="source:toy:l0"]');
    await source.click();
    await surface.scrollIntoViewIfNeeded();
    const inside = await worldPointToClient(surface, 136, 88);
    await page.mouse.click(inside.x, inside.y);
    await expect(page.locator('#ontology-candidate-control')).toHaveAttribute('aria-pressed', 'true');
    expect(ledger).toEqual({ pageErrors: [], externalRequests: [], mutationRequests: [] });
  } finally {
    await context.close();
  }
});

test('world lifecycle destroys cleanly, remounts fresh, and isolates declared failures', async ({ page }) => {
  const { surface } = await openWorld(page);
  const lifecycle = () => page.evaluate(() => window.__calWorldProbe.getLifecycle());
  const toggle = page.locator('[data-action="toggle-floor-room"]');
  const pause = page.locator('[data-world-action="pause"]');

  const initial = await lifecycle();
  await toggle.click();
  await expect.poll(lifecycle).toMatchObject({ activeSubscriptions: 0, status: 'inactive', ownedCallbacks: 0 });
  await toggle.click();
  await expect(page.locator('[data-world-surface]')).toBeVisible();
  await expect.poll(lifecycle).toMatchObject({ generation: initial.generation + 1, activeSubscriptions: 1, ownedCallbacks: 0 });

  await page.locator('[data-system-level-id="system-l1-substrate"]').click();
  await expect.poll(lifecycle).toMatchObject({ activeSubscriptions: 0, status: 'inactive', ownedCallbacks: 0 });
  await page.locator('[data-action="return-to-floor"]').click();
  await expect(page.locator('[data-world-surface]')).toBeVisible();
  const afterSystem = await lifecycle();
  expect(afterSystem.activeSubscriptions).toBe(1);

  await pause.click();
  await expect.poll(lifecycle).toMatchObject({ activeSubscriptions: 0, status: 'paused', ownedCallbacks: 0 });
  await expect(pause).toHaveText('Resume world');
  await pause.click();
  await expect(page.locator('[data-world-surface]')).toBeVisible();
  await expect.poll(lifecycle).toMatchObject({ activeSubscriptions: 1, status: 'ready', ownedCallbacks: 0 });

  await page.emulateMedia({ reducedMotion: 'reduce' });
  await expect(page.locator('[data-world-surface]')).toHaveAttribute('data-reduced-motion', 'true');
  await surface.focus().catch(() => {});
  await page.emulateMedia({ reducedMotion: 'no-preference' });

  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, value: 'hidden' });
    document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect.poll(lifecycle).toMatchObject({ activeSubscriptions: 0, ownedCallbacks: 0 });
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, value: 'visible' });
    document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect(page.locator('[data-world-surface]')).toBeVisible();
  await expect.poll(lifecycle).toMatchObject({ activeSubscriptions: 1, status: 'ready', ownedCallbacks: 0 });

  const source = page.locator('[data-source-id="source:toy:l0"]');
  await source.click();
  const semanticBeforeFailure = await semanticSnapshot(page);
  await page.evaluate(() => window.__calWorldProbe.injectUnknownIntent());
  await expect(page.locator('[data-world-host]')).toHaveAttribute('data-world-state', 'failed');
  expect(await semanticSnapshot(page)).toEqual(semanticBeforeFailure);
  await expect(source).toBeEnabled();
  await expect(page.locator('[data-world-status]')).toContainText('Textual evidence controls remain available');
  await page.locator('[data-world-action="retry"]').click();
  await expect(page.locator('[data-world-surface]')).toBeVisible();
  await expect.poll(lifecycle).toMatchObject({ activeSubscriptions: 1, status: 'ready', ownedCallbacks: 0 });

  for (const mode of ['manifest', 'binding', 'render']) {
    await page.goto(`${WORLD_URL}?inject_world_failure=${mode}`);
    await expect(page.locator('#connection-status')).toHaveText('Locked synthetic witness loaded');
    await page.locator('[data-scene-id="evidence-l0-corpus"]').click();
    await expect(page.locator('[data-world-host]')).toHaveAttribute('data-world-state', 'failed');
    await expect(page.locator('#ontology-candidate-control')).toBeEnabled();
    await page.locator('[data-world-action="retry"]').click();
    await expect(page.locator('[data-world-surface]')).toBeVisible();
    await expect.poll(lifecycle).toMatchObject({ activeSubscriptions: 1, status: 'ready', ownedCallbacks: 0 });
  }

  await page.goto(`${WORLD_URL}?inject_render_failure=after-build`);
  await expect(page.locator('#connection-status')).toHaveText('Witness unavailable');
  await expect(page.locator('[data-world-surface]')).toHaveCount(0);
  await expect(page.locator('[data-world-projection]')).toBeHidden();
});

test('world and semantic controls remain contained at wide and narrow profiles', async ({ page }) => {
  for (const viewport of [{ width: 1440, height: 900 }, { width: 390, height: 844 }, { width: 320, height: 568 }]) {
    await page.setViewportSize(viewport);
    await openWorld(page);
    await page.locator('[data-world-projection]').scrollIntoViewIfNeeded();
    const geometry = await page.evaluate(() => {
      const world = document.querySelector('[data-world-projection]').getBoundingClientRect();
      const tower = document.querySelector('[data-panel="tower-elevation"]').getBoundingClientRect();
      const room = document.querySelector('#floor-room').getBoundingClientRect();
      return {
        viewportWidth: innerWidth,
        scrollWidth: document.documentElement.scrollWidth,
        world: { left: world.left, right: world.right, width: world.width },
        tower: { left: tower.left, right: tower.right },
        room: { left: room.left, right: room.right }
      };
    });
    expect(geometry.scrollWidth).toBeLessThanOrEqual(geometry.viewportWidth + 1);
    expect(geometry.world.left).toBeGreaterThanOrEqual(0);
    expect(geometry.world.right).toBeLessThanOrEqual(geometry.viewportWidth + 1);
    expect(geometry.world.width).toBeGreaterThanOrEqual(200);
    if (viewport.width >= 900) expect(geometry.room.left).toBeGreaterThan(geometry.tower.left);
    await page.locator('[data-world-move="right"]').focus();
    await expect(page.locator('[data-world-move="right"]')).toBeFocused();
    await page.locator('#ontology-candidate-control').focus();
    await expect(page.locator('#ontology-candidate-control')).toBeFocused();
  }
});

test('@performance desktop reference profile records the amended measured-quantum verdict', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'desktop', 'The accepted reference profile is desktop-only.');
  const { surface } = await openWorld(page);
  await surface.focus();

  await page.evaluate(() => {
    window.__worldLongTasks = [];
    window.__worldLongTaskSupported = PerformanceObserver.supportedEntryTypes.includes('longtask');
    if (window.__worldLongTaskSupported) {
      window.__worldLongTaskObserver = new PerformanceObserver((list) => {
        window.__worldLongTasks.push(...list.getEntries().map((entry) => ({ startTime: entry.startTime, duration: entry.duration })));
      });
      window.__worldLongTaskObserver.observe({ type: 'longtask' });
    }
  });

  const timing = await page.evaluate(async () => {
    const timerProbeTimestamps = [performance.now()];
    let reads = 0;
    while (timerProbeTimestamps.length < 65 && reads < 200000) {
      const current = performance.now();
      if (current > timerProbeTimestamps.at(-1)) timerProbeTimestamps.push(current);
      reads += 1;
    }
    const rawRafTimestamps = [];
    await new Promise((resolve) => {
      let frames = 0;
      const sample = (timestamp) => {
        frames += 1;
        if (frames > 120) rawRafTimestamps.push(timestamp);
        if (rawRafTimestamps.length === 601) resolve();
        else requestAnimationFrame(sample);
      };
      requestAnimationFrame(sample);
    });
    return { timerProbeTimestamps, timerProbeReads: reads, rawRafTimestamps };
  });

  expect(timing.timerProbeTimestamps).toHaveLength(65);
  expect(timing.timerProbeReads).toBeLessThanOrEqual(200000);
  const timerAdvancesUs = timing.timerProbeTimestamps.slice(1).map((value, index) => Math.round((value - timing.timerProbeTimestamps[index]) * 1000));
  const timerQuantumUs = Math.min(...timerAdvancesUs.filter((value) => value > 0));
  expect(timerQuantumUs).toBeGreaterThanOrEqual(1);
  expect(timerQuantumUs).toBeLessThanOrEqual(100);

  const measuredIntervalsMs = timing.rawRafTimestamps.slice(1).map((value, index) => value - timing.rawRafTimestamps[index]);
  const canonicalIntervalsUs = measuredIntervalsMs.map((value) => Math.round(value * 1000));
  expect(canonicalIntervalsUs).toHaveLength(600);
  const rawFrameClassesUs = {
    on_budget: canonicalIntervalsUs.filter((value) => value <= 16700),
    quantized_over_budget: canonicalIntervalsUs.filter((value) => value >= 16701 && value <= 33300),
    critical: canonicalIntervalsUs.filter((value) => value > 33300)
  };
  expect(Object.values(rawFrameClassesUs).reduce((total, values) => total + values.length, 0)).toBe(600);
  const sortedFrames = [...canonicalIntervalsUs].sort((left, right) => left - right);
  const rawP95Us = sortedFrames[569];
  const comparisonP95Us = Math.max(0, rawP95Us - timerQuantumUs);

  const inputLatenciesMs = [];
  for (let index = 0; index < 100; index += 1) {
    await page.keyboard.press(index % 2 === 0 ? 'ArrowLeft' : 'ArrowRight');
    const sample = await page.evaluate(() => new Promise((resolve) => {
      requestAnimationFrame((renderedAt) => {
        const startedAt = Number(document.querySelector('[data-world-surface]').getAttribute('data-last-input-start-ms'));
        resolve(Math.max(0, renderedAt - startedAt));
      });
    }));
    inputLatenciesMs.push(sample);
  }
  const sortedInputs = [...inputLatenciesMs].sort((left, right) => left - right);
  const inputP95Ms = sortedInputs[94];
  await page.waitForTimeout(1000);
  const observation = await page.evaluate(() => {
    window.__worldLongTaskObserver?.disconnect();
    return {
      supported: window.__worldLongTaskSupported,
      entries: window.__worldLongTasks,
      lifecycle: window.__calWorldProbe.getLifecycle()
    };
  });

  const evidence = {
    contract_id: 'measured-quantum-frame-verdict.v1',
    timer_probe_timestamps_ms: timing.timerProbeTimestamps,
    timer_probe_reads: timing.timerProbeReads,
    timer_quantum_us: timerQuantumUs,
    raw_raf_timestamps_ms: timing.rawRafTimestamps,
    measured_intervals_ms: measuredIntervalsMs,
    canonical_intervals_us: canonicalIntervalsUs,
    raw_frame_classes_us: rawFrameClassesUs,
    raw_p95_us: rawP95Us,
    comparison_p95_us: comparisonP95Us,
    input_latencies_ms: inputLatenciesMs,
    input_p95_ms: inputP95Ms,
    long_task_supported: observation.supported,
    long_tasks_over_50ms: observation.entries.filter((entry) => entry.duration > 50),
    owned_callbacks_after_1000ms: observation.lifecycle.ownedCallbacks
  };
  await testInfo.attach('performance-evidence.json', {
    body: Buffer.from(`${JSON.stringify(evidence, null, 2)}\n`),
    contentType: 'application/json'
  });

  expect(comparisonP95Us).toBeLessThanOrEqual(16700);
  expect(rawP95Us).toBeLessThanOrEqual(16800);
  expect(rawFrameClassesUs.critical).toHaveLength(0);
  expect(inputP95Ms).toBeLessThanOrEqual(100);
  expect(observation.supported).toBe(true);
  expect(evidence.long_tasks_over_50ms).toHaveLength(0);
  expect(observation.lifecycle.ownedCallbacks).toBe(0);
});
