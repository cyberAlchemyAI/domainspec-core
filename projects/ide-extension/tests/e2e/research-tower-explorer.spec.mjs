import { expect, test } from '@playwright/test';
import { buildVerificationPromptProjections } from '../../src/research-tower/l0-witness.mjs';

test('cutaway tower opens one stable room and keeps floor, System, and inspector state separate', async ({ page }, testInfo) => {
  const pageErrors = [];
  const consoleErrors = [];
  const failedRequests = [];
  const mutationRequests = [];
  const externalRequests = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));
  page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  page.on('requestfailed', (request) => failedRequests.push(request.url()));
  page.on('request', (request) => {
    if (request.method() !== 'GET') mutationRequests.push(`${request.method()} ${request.url()}`);
    if (new URL(request.url()).hostname !== '127.0.0.1') externalRequests.push(request.url());
  });

  await page.goto('/demo/research-tower');

  const canvas = page.locator('[data-workbench="tower-scene-canvas"]');
  const tower = page.locator('[data-object="research-tower"]');
  const elevation = page.locator('[data-panel="tower-elevation"]');
  const room = page.locator('#floor-room[data-panel="floor-room"]');
  const toggle = page.locator('[data-action="toggle-floor-room"]');
  const systemReference = page.locator('[data-region="system-reference"]');
  const systemRefusal = page.locator('[data-panel="system-refusal"]');
  const floors = page.locator('[data-list="levels"] .tower-floor');
  const systems = page.locator('[data-list="system-levels"] [data-system-level-id]');
  const firstFloor = page.getByRole('button', { name: 'Evidence floor 1 of 3 — Synthetic corpus anchors. locked-synthetic. candidate-local.' });
  const residueFloor = page.getByRole('button', { name: 'Evidence floor 2 of 3 — Open representative-selection residue. open. candidate-local.' });
  const closureFloor = page.getByRole('button', { name: 'Evidence floor 3 of 3 — Closure plan, blocked. blocked. candidate-local.' });

  await expect(canvas).toBeVisible();
  await expect(canvas).toHaveAttribute('data-layout', 'cutaway-tower');
  await expect(page.locator('#connection-status')).toHaveText('Locked synthetic witness loaded');
  await expect(page.locator('[data-panel="witness-binding"]')).toContainText('validation:l0-synthetic-001-independent');
  await expect(tower).toHaveCount(1);
  await expect(elevation).toBeVisible();
  await expect(room).toHaveCount(1);
  await expect(room).toBeHidden();
  await expect(systemReference).toBeVisible();
  expect(await systemReference.evaluate((node) => node.closest('[data-object="research-tower"]') === null)).toBe(true);
  expect(await room.evaluate((node) => node.parentElement.matches('[data-object="research-tower"]'))).toBe(true);
  await expect(floors).toHaveCount(3);
  await expect(systems).toHaveCount(5);
  await expect(page.locator('[role="status"]')).toHaveCount(1);
  await expect(firstFloor).toHaveAttribute('aria-pressed', 'true');
  await expect(firstFloor).toHaveAttribute('aria-expanded', 'false');
  await expect(firstFloor).toHaveAttribute('aria-controls', 'floor-room');
  await expect(toggle).toHaveText('Open selected floor room');
  await expect(toggle).toHaveAttribute('aria-expanded', 'false');
  await expect(page.locator('[data-panel="active-floor-summary"]')).toContainText('room closed');
  await page.evaluate(() => {
    window.__selectionMutations = 0;
    new MutationObserver((records) => { window.__selectionMutations += records.length; })
      .observe(document.querySelector('#selection-status'), { childList: true });
  });
  const expectOneAnnouncement = async (action) => {
    await page.evaluate(() => { window.__selectionMutations = 0; });
    await action();
    await expect.poll(() => page.evaluate(() => window.__selectionMutations)).toBe(1);
  };

  await residueFloor.focus();
  await page.keyboard.press('Space');
  await expect.poll(() => page.evaluate(() => window.__selectionMutations)).toBe(1);
  await expect(residueFloor).toBeFocused();
  await expect(residueFloor).toHaveAttribute('aria-pressed', 'true');
  await expect(residueFloor).toHaveAttribute('aria-expanded', 'true');
  await expect(firstFloor).toHaveAttribute('aria-pressed', 'false');
  await expect(room).toBeVisible();
  await expect(room).toHaveAttribute('data-origin-floor', 'evidence-l1-residue');
  await expect(room).toHaveAccessibleName(/Evidence floor 2 of 3 .* research room/);
  await expect(page.locator('[data-panel="scene-id"]')).toHaveText('evidence-l1-residue');
  await expect(page.locator('[data-panel="scene-status"]')).toHaveText('open');
  await expect(page.locator('[data-panel="scene-content"]')).toContainText('must never be presented as completed progress');
  await expect(page.locator('[data-media="room-still"]')).toBeVisible();
  await expect(page.locator('[data-media="room-still"]')).toHaveAttribute('src', '/assets/research-tower-concepts/autonomous-observatory-lab.png');
  await expect(page.locator('[data-media="ambient-tableau"]')).toBeHidden();
  await expect(page.locator('[data-panel="scene-caveat"]')).toHaveText('Illustrative room scene · no live workers or workflow');
  await expect(page.locator('[data-verification-field="selected-floor"]')).toHaveText('evidence-l1-residue');
  await expect(page.locator('[data-verification-field="question"]')).toHaveText('Which real tower, if any, should later be selected?');
  await expect(page.locator('[data-verification-field="route"]')).toContainText('descriptive only');
  await expect(page.locator('[data-verification-field="executable"]')).toHaveText('false');
  await expect(page.locator('[data-list="verification-bindings"] li')).toHaveCount(2);
  await expect(page.locator('[data-list="verification-bindings"] li').first()).toContainText('verified');
  await expect(toggle).toHaveText('Return to tower overview');
  await expect(toggle).toHaveAttribute('aria-expanded', 'true');

  const source = page.locator('[data-source-id="source:toy:l0"]');
  await expectOneAnnouncement(() => source.click());
  await expect(source).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-panel="source-detail"]')).toContainText('fixtures/source/toy-tower/levels/L0-corpus.md');

  await expectOneAnnouncement(() => toggle.click());
  await expect(room).toBeHidden();
  await expectOneAnnouncement(() => toggle.click());
  await expect(room).toBeVisible();
  const relationFilter = page.locator('[data-field="relation-filter"]');
  await expectOneAnnouncement(() => relationFilter.selectOption('supports'));
  await expect(page.locator('#relation-count')).toContainText('relation paths');
  await expectOneAnnouncement(() => relationFilter.selectOption('all'));
  await expect(page.locator('#relation-count')).toContainText('relation paths');
  const preservedInspection = await page.evaluate(() => ({
    candidatePressed: document.querySelector('[data-action="show-candidate"]').getAttribute('aria-pressed'),
    sourcePressed: document.querySelector('[data-source-id="source:toy:l0"]').getAttribute('aria-pressed'),
    sourceDetail: document.querySelector('[data-panel="source-detail"]').textContent,
    relationFilter: document.querySelector('[data-field="relation-filter"]').value,
    relationCount: document.querySelector('#relation-count').textContent
  }));

  await closureFloor.focus();
  await expectOneAnnouncement(() => page.keyboard.press('Enter'));
  await expect(closureFloor).toBeFocused();
  await expect(room).toHaveAttribute('data-origin-floor', 'evidence-l2-closure');
  await expect(page.locator('[data-panel="scene-status"]')).toHaveText('blocked');
  await expect(page.locator('[data-panel="scene-unavailable"]')).toContainText('No representative source is selected');
  await expect(page.locator('[data-media="room-still"]')).toHaveAttribute('src', '/assets/research-tower-concepts/night-knowledge-observatory.png');
  await expect(page.locator('[data-verification-field="selected-floor"]')).toHaveText('evidence-l2-closure');
  await expect(page.locator('[data-list="unbound-evidence"]')).toContainText('No representative source, closure decision, or independent closure witness is bound.');
  expect(await page.evaluate(() => ({
    candidatePressed: document.querySelector('[data-action="show-candidate"]').getAttribute('aria-pressed'),
    sourcePressed: document.querySelector('[data-source-id="source:toy:l0"]').getAttribute('aria-pressed'),
    sourceDetail: document.querySelector('[data-panel="source-detail"]').textContent,
    relationFilter: document.querySelector('[data-field="relation-filter"]').value,
    relationCount: document.querySelector('#relation-count').textContent
  }))).toEqual(preservedInspection);

  await expectOneAnnouncement(() => toggle.click());
  await expect(toggle).toBeFocused();
  await expect(room).toBeHidden();
  await expect(closureFloor).toHaveAttribute('aria-pressed', 'true');
  await expect(closureFloor).toHaveAttribute('aria-expanded', 'false');
  await expect(toggle).toHaveText('Open selected floor room');
  await expectOneAnnouncement(() => toggle.click());
  await expect(room).toBeVisible();
  await expect(room).toHaveAttribute('data-origin-floor', 'evidence-l2-closure');
  await expect(relationFilter).toHaveValue('all');

  const systemCases = [
    { id: 'system-l1-substrate', label: 'System L1 · Substrate', status: 'unproven-in-lab', reason: 'runtime-queryable graph and persona artifacts' },
    { id: 'system-l2-construction', label: 'System L2 · Construction', status: 'prior-work-not-live-here', reason: 'Construction methods are not active builders' },
    { id: 'system-l3-application', label: 'System L3 · Application', status: 'unavailable-in-lab', reason: 'No debate, dispatch, or persona operation' },
    { id: 'system-lphi-policy', label: 'System Lφ · Decision policy', status: 'design-stage-unproven', reason: 'MOGT has no live Lab run' },
    { id: 'system-l4-adjudication', label: 'System L4 · Adjudication', status: 'governance-only', reason: 'cannot score, select a winner, or emit a verdict' }
  ];
  for (const systemCase of systemCases) {
    const control = page.locator(`[data-system-level-id="${systemCase.id}"]`);
    await expectOneAnnouncement(() => control.click());
    await expect(page.locator('#system-refusal-title')).toBeFocused();
    await expect(control).toHaveAttribute('aria-pressed', 'true');
    expect(await systems.evaluateAll((items) => items.filter((item) => item.getAttribute('aria-pressed') === 'true').length)).toBe(1);
    await expect(closureFloor).toHaveAttribute('aria-pressed', 'true');
    await expect(closureFloor).toHaveAttribute('aria-expanded', 'false');
    expect(await floors.evaluateAll((items) => items.filter((item) => item.getAttribute('aria-pressed') === 'true').length)).toBe(1);
    await expect(room).toBeHidden();
    await expect(page.locator('[data-media="room-still"]')).not.toHaveAttribute('src');
    await expect(toggle).toBeDisabled();
    await expect(systemRefusal).toBeVisible();
    await expect(page.locator('[data-system-field="id"]')).toHaveText(systemCase.id);
    await expect(page.locator('[data-system-field="status"]')).toHaveText('Unavailable in this Lab');
    await expect(page.locator('[data-system-field="implementation"]')).toHaveText(systemCase.status);
    await expect(page.locator('[data-system-field="reason"]')).toContainText(systemCase.reason);
    await expect(page.locator('[data-system-field="source"]')).toContainText('#2-the-layer-stack-bottom-up-one-layer-at-a-time');
    await expect(page.locator('[data-panel="system-origin"]')).toContainText('Evidence floor 3 of 3');
    expect(await page.evaluate(() => ({
      candidatePressed: document.querySelector('[data-action="show-candidate"]').getAttribute('aria-pressed'),
      sourcePressed: document.querySelector('[data-source-id="source:toy:l0"]').getAttribute('aria-pressed'),
      sourceDetail: document.querySelector('[data-panel="source-detail"]').textContent,
      relationFilter: document.querySelector('[data-field="relation-filter"]').value,
      relationCount: document.querySelector('#relation-count').textContent
    }))).toEqual(preservedInspection);
    await expectOneAnnouncement(() => page.locator('[data-action="return-to-floor"]').click());
    await expect(control).toBeFocused();
    await expect(control).toHaveAccessibleName(`${systemCase.label}. Unavailable in this Lab. ${systemCase.status}.`);
    await expect(systemRefusal).toBeHidden();
    await expect(room).toBeVisible();
    await expect(closureFloor).toHaveAttribute('aria-pressed', 'true');
    await expect(closureFloor).toHaveAttribute('aria-expanded', 'true');
    await expect(relationFilter).toHaveValue('all');
    expect(await page.evaluate(() => ({
      candidatePressed: document.querySelector('[data-action="show-candidate"]').getAttribute('aria-pressed'),
      sourcePressed: document.querySelector('[data-source-id="source:toy:l0"]').getAttribute('aria-pressed'),
      sourceDetail: document.querySelector('[data-panel="source-detail"]').textContent,
      relationFilter: document.querySelector('[data-field="relation-filter"]').value,
      relationCount: document.querySelector('#relation-count').textContent
    }))).toEqual(preservedInspection);
  }

  const removedTrigger = page.locator('[data-system-level-id="system-l1-substrate"]');
  await expectOneAnnouncement(() => removedTrigger.click());
  await removedTrigger.evaluate((node) => {
    window.__removedSystemTrigger = { node, parent: node.parentElement, next: node.nextSibling };
    node.remove();
  });
  await expectOneAnnouncement(() => page.locator('[data-action="return-to-floor"]').click());
  await expect(closureFloor).toBeFocused();
  await expect(page.locator('#selection-status')).toContainText('Original System trigger unavailable; focus returned to the active evidence floor.');
  await expect(room).toBeVisible();
  expect(await page.evaluate(() => ({
    candidatePressed: document.querySelector('[data-action="show-candidate"]').getAttribute('aria-pressed'),
    sourcePressed: document.querySelector('[data-source-id="source:toy:l0"]').getAttribute('aria-pressed'),
    sourceDetail: document.querySelector('[data-panel="source-detail"]').textContent,
    relationFilter: document.querySelector('[data-field="relation-filter"]').value,
    relationCount: document.querySelector('#relation-count').textContent
  }))).toEqual(preservedInspection);
  await page.evaluate(() => {
    const removed = window.__removedSystemTrigger;
    removed.parent.insertBefore(removed.node, removed.next);
    delete window.__removedSystemTrigger;
  });
  await expect(systems).toHaveCount(5);

  await expectOneAnnouncement(() => page.locator('[data-action="reset-orientation"]').click());
  await expect(firstFloor).toBeFocused();
  await expect(firstFloor).toHaveAttribute('aria-pressed', 'true');
  await expect(firstFloor).toHaveAttribute('aria-expanded', 'false');
  await expect(room).toBeHidden();
  await expect(systemRefusal).toBeHidden();
  await expect(toggle).toBeEnabled();
  await expect(page.locator('[data-action="show-candidate"]')).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-field="relation-filter"]')).toHaveValue('all');

  const roomNodeIdentity = await room.evaluate((node) => {
    window.__cutawayRoom = node;
    return node.id;
  });
  await expectOneAnnouncement(() => firstFloor.click());
  await page.evaluate(() => { window.__selectionMutations = 0; });
  await firstFloor.click();
  await page.waitForTimeout(20);
  expect(await page.evaluate(() => window.__selectionMutations)).toBe(0);
  expect(roomNodeIdentity).toBe('floor-room');
  expect(await room.evaluate((node) => node === window.__cutawayRoom)).toBe(true);
  await expect(room).toBeVisible();
  await expect(page.locator('#selection-status')).toContainText('Room open');

  await expect(page.locator('[data-media="room-still"]')).toBeVisible();
  await expect(page.locator('[data-media="room-still"]')).toHaveAttribute('src', '/assets/research-tower-concepts/robot-paper-library.png');
  await expect(page.locator('[data-media="ambient-tableau"]')).toBeVisible();
  await expect(page.locator('[data-panel="room-scene"]')).toHaveAttribute('data-motion', 'running');
  await expect(page.locator('[data-verification-field="selected-floor"]')).toHaveText('evidence-l0-corpus');
  await expect(page.locator('[data-list="known-evidence"]')).toContainText('Locked synthetic source anchors expose locators');
  await expect(page.locator('[data-list="unbound-evidence"]')).toContainText('representative real source');
  await expect(page.locator('[data-verification-field="executable"]')).toHaveText('false');
  await expect(page.locator('img[aria-hidden="true"]')).toHaveCount(1);
  await expect(page.locator('canvas, [data-robot-role], [data-action*="verification"], form')).toHaveCount(0);
  const sceneBounds = await page.locator('[data-panel="room-scene"], [data-media="room-still"], [data-media="ambient-tableau"]').evaluateAll(
    (items) => items.map((item) => item.getBoundingClientRect().toJSON())
  );
  expect(sceneBounds[1].x).toBeGreaterThanOrEqual(sceneBounds[0].x);
  expect(sceneBounds[1].right).toBeLessThanOrEqual(sceneBounds[0].right + 1);
  expect(sceneBounds[2].bottom).toBeLessThanOrEqual(sceneBounds[0].bottom + 1);
  await firstFloor.focus();
  const controlHeights = await page.locator('.tower-floor, [data-action="toggle-floor-room"], .system-control, .source-control, [data-action="show-candidate"], [data-action="reset-orientation"]').evaluateAll(
    (items) => items.map((item) => item.getBoundingClientRect().height)
  );
  expect(controlHeights.every((height) => height >= 44)).toBe(true);
  await firstFloor.focus();
  await page.keyboard.press('Tab');
  const focusGeometry = await page.locator(':focus').evaluate((item) => ({ outlineStyle: getComputedStyle(item).outlineStyle, outlineWidth: parseFloat(getComputedStyle(item).outlineWidth) }));
  expect(focusGeometry.outlineStyle).not.toBe('none');
  expect(focusGeometry.outlineWidth).toBeGreaterThanOrEqual(3);
  const positions = await page.locator('[data-object="research-tower"], [data-panel="floor-room"], [data-region="system-reference"]').evaluateAll(
    (items) => items.map((item) => getComputedStyle(item).position)
  );
  expect(positions.every((position) => position !== 'fixed')).toBe(true);
  if (testInfo.project.name === 'desktop') {
    const wideGeometry = await page.evaluate(() => {
      const tower = document.querySelector('[data-object="research-tower"]').getBoundingClientRect();
      const elevation = document.querySelector('[data-panel="tower-elevation"]').getBoundingClientRect();
      const room = document.querySelector('[data-panel="floor-room"]').getBoundingClientRect();
      return {
        sideBySide: elevation.right <= room.left,
        contained: elevation.left >= tower.left && room.right <= tower.right && elevation.top >= tower.top && room.bottom <= tower.bottom,
        unobscured: elevation.width > 0 && elevation.height > 0 && room.width > 0 && room.height > 0
      };
    });
    expect(wideGeometry).toEqual({ sideBySide: true, contained: true, unobscured: true });
    await page.screenshot({ path: testInfo.outputPath('cutaway-open-desktop.png'), fullPage: true });
  }
  expect(pageErrors).toEqual([]);
  expect(consoleErrors).toEqual([]);
  expect(failedRequests).toEqual([]);
  expect(mutationRequests).toEqual([]);
  expect(externalRequests).toEqual([]);
});

test('cutaway tower remains animation-free under reduced motion', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/demo/research-tower');
  const firstFloor = page.getByRole('button', { name: /Evidence floor 1 of 3/ });
  await firstFloor.click();
  await expect(page.locator('#floor-room')).toBeVisible();
  await expect(page.locator('[data-panel="room-scene"]')).toHaveAttribute('data-motion', 'stopped');
  await expect(page.locator('[data-media="ambient-tableau"]')).toBeVisible();
  const firstFrame = await page.locator('[data-media="ambient-tableau"]').evaluate((node) => getComputedStyle(node).backgroundPosition);
  await page.waitForTimeout(100);
  expect(await page.locator('[data-media="ambient-tableau"]').evaluate((node) => getComputedStyle(node).backgroundPosition)).toBe(firstFrame);
  const motion = await page.locator('[data-object="research-tower"] *').evaluateAll((items) => items.map((item) => {
    const style = getComputedStyle(item);
    return { animationName: style.animationName, transitionDuration: style.transitionDuration };
  }));
  expect(motion.every((item) => item.animationName === 'none' && item.transitionDuration === '0s')).toBe(true);
  expect(errors).toEqual([]);
});

test('ambient tableau runs only for a visible open L0 room', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.goto('/demo/research-tower');
  const scene = page.locator('[data-panel="room-scene"]');
  const tableau = page.locator('[data-media="ambient-tableau"]');
  const firstFloor = page.getByRole('button', { name: /Evidence floor 1 of 3/ });
  await firstFloor.click();
  await expect(scene).toHaveAttribute('data-motion', 'running');
  const activeMotion = await tableau.evaluate((node) => {
    const style = getComputedStyle(node);
    return { name: style.animationName, duration: style.animationDuration, iterations: style.animationIterationCount };
  });
  expect(activeMotion).toEqual({ name: 'ambient-lab-loop', duration: '10s', iterations: 'infinite' });
  const status = await page.locator('#selection-status').textContent();
  await page.waitForTimeout(150);
  await expect(page.locator('#selection-status')).toHaveText(status);

  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, value: 'hidden' });
    document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect(scene).toHaveAttribute('data-motion', 'stopped');
  await expect(tableau).toHaveCSS('animation-name', 'none');
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, value: 'visible' });
    document.dispatchEvent(new Event('visibilitychange'));
  });
  await expect(scene).toHaveAttribute('data-motion', 'running');

  const toggle = page.locator('[data-action="toggle-floor-room"]');
  await toggle.click();
  await expect(page.locator('#floor-room')).toBeHidden();
  await expect(scene).toHaveAttribute('data-motion', 'stopped');
  await expect(tableau).toBeHidden();
  await toggle.click();
  await expect(page.locator('#floor-room')).toBeVisible();
  await expect(scene).toHaveAttribute('data-motion', 'running');

  await page.getByRole('button', { name: /Evidence floor 2 of 3/ }).click();
  await expect(scene).toHaveAttribute('data-motion', 'stopped');
  await expect(tableau).toBeHidden();
  await firstFloor.click();
  await page.locator('[data-system-level-id="system-l1-substrate"]').click();
  await expect(scene).toHaveAttribute('data-motion', 'stopped');
  await expect(tableau).toBeHidden();
  expect(errors).toEqual([]);
});

test('post-construction failure rolls back to the same disabled surface', async ({ page }) => {
  const errors = [];
  const consoleErrors = [];
  const mutationRequests = [];
  page.on('pageerror', (error) => errors.push(error.message));
  page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  page.on('request', (request) => { if (request.method() !== 'GET') mutationRequests.push(`${request.method()} ${request.url()}`); });
  await page.goto('/demo/research-tower?inject_render_failure=after-build');
  await expect(page.locator('#connection-status')).toHaveText('Witness unavailable');
  await expect(page.locator('#selection-status')).toContainText('Injected render failure after staging');
  await expect(page.locator('[data-panel="witness-binding"]')).toContainText('No validation record is bound');
  await expect(page.locator('[data-panel="active-floor-summary"]')).toHaveText('No evidence floor is selected while the witness is unavailable.');
  await expect(page.locator('[data-list="levels"] .tower-floor')).toHaveCount(0);
  await expect(page.locator('[data-list="system-levels"] [data-system-level-id]')).toHaveCount(0);
  await expect(page.locator('[data-list="sources"] [data-source-id]')).toHaveCount(0);
  await expect(page.locator('[data-action="reset-orientation"]')).toBeDisabled();
  await expect(page.locator('[data-action="toggle-floor-room"]')).toBeDisabled();
  await expect(page.locator('[data-action="show-candidate"]')).toBeDisabled();
  await expect(page.locator('[data-field="relation-filter"]')).toBeDisabled();
  await expect(page.locator('[data-action="return-to-floor"]')).toBeDisabled();
  await expect(page.locator('[data-media="room-still"]')).not.toHaveAttribute('src');
  await expect(page.locator('[data-panel="room-scene"]')).toHaveAttribute('data-motion', 'stopped');
  await page.evaluate(() => {
    document.querySelector('[data-action="reset-orientation"]').click();
    document.querySelector('[data-action="toggle-floor-room"]').click();
    document.querySelector('[data-action="show-candidate"]').click();
    document.querySelector('[data-field="relation-filter"]').dispatchEvent(new Event('change'));
    document.querySelector('[data-action="return-to-floor"]').click();
  });
  await page.waitForTimeout(50);
  expect(errors).toEqual([]);
  expect(consoleErrors).toEqual([]);
  expect(mutationRequests).toEqual([]);
});

test('unknown room media is omitted without suppressing textual evidence', async ({ page }) => {
  const errors = [];
  const failedRequests = [];
  page.on('pageerror', (error) => errors.push(error.message));
  page.on('requestfailed', (request) => failedRequests.push(request.url()));
  await page.goto('/demo/research-tower?inject_media_url=unknown');
  await page.getByRole('button', { name: /Evidence floor 1 of 3/ }).click();
  await expect(page.locator('[data-media="room-still"]')).toBeHidden();
  await expect(page.locator('[data-media="room-still"]')).not.toHaveAttribute('src');
  await expect(page.locator('[data-media="ambient-tableau"]')).toBeHidden();
  await expect(page.locator('[data-panel="room-scene"]')).toHaveAttribute('data-motion', 'stopped');
  await expect(page.locator('[data-panel="scene-caveat"]')).toContainText('evidence text remains available');
  await expect(page.locator('[data-panel="scene-content"]')).toContainText('Locked synthetic source anchors, locators, digests, and byte sizes.');
  await expect(page.locator('[data-verification-field="selected-floor"]')).toHaveText('evidence-l0-corpus');
  expect(errors).toEqual([]);
  expect(failedRequests).toEqual([]);
});

test('unknown evidence scene is rejected by the closed L0 contract before presentation', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.route('**/api/research-tower/l0', async (route) => {
    const response = await route.fetch();
    const payload = await response.json();
    payload.scene_manifest.towers[0].scenes[0].level_id = 'evidence-unknown';
    await route.fulfill({ response, json: payload });
  });
  await page.goto('/demo/research-tower');
  await expect(page.locator('#connection-status')).toHaveText('Witness unavailable');
  await expect(page.locator('#selection-status')).toContainText('Scene and verification floor identities do not match');
  await expect(page.locator('[data-list="levels"] .tower-floor')).toHaveCount(0);
  await expect(page.locator('[data-media="room-still"]')).not.toHaveAttribute('src');
  await expect(page.locator('[data-media="ambient-tableau"]')).toBeHidden();
  await expect(page.locator('[data-panel="room-scene"]')).toHaveAttribute('data-motion', 'stopped');
  expect(errors).toEqual([]);
});

test('missing decorative media preserves the evidence and textual fallback', async ({ page }) => {
  const errors = [];
  const consoleErrors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  await page.route('**/robot-paper-library.png', (route) => route.abort('failed'));
  await page.goto('/demo/research-tower');
  await page.getByRole('button', { name: /Evidence floor 1 of 3/ }).click();
  await expect(page.locator('[data-media="room-still"]')).toBeHidden();
  await expect(page.locator('[data-panel="room-scene"]')).toHaveAttribute('data-motion', 'stopped');
  await expect(page.locator('[data-panel="scene-caveat"]')).toContainText('evidence text remains available');
  await expect(page.locator('[data-panel="scene-id"]')).toHaveText('evidence-l0-corpus');
  await expect(page.locator('[data-verification-field="selected-floor"]')).toHaveText('evidence-l0-corpus');
  await expect(page.locator('[data-list="verification-bindings"] li')).toHaveCount(3);
  expect(errors).toEqual([]);
  expect(consoleErrors).toEqual(['Failed to load resource: net::ERR_FAILED']);
});

test('exact source-binding failures stay visible and suppress ordinary floor claims', async ({ page }) => {
  const pageErrors = [];
  const consoleErrors = [];
  const mutationRequests = [];
  let bindingStatus = 'object_unavailable';
  page.on('pageerror', (error) => pageErrors.push(error.message));
  page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  page.on('request', (request) => { if (request.method() !== 'GET') mutationRequests.push(`${request.method()} ${request.url()}`); });
  await page.route('**/api/research-tower/l0', async (route) => {
    const response = await route.fetch();
    const payload = await response.json();
    const source = payload.sources.find((item) => item.id === 'source:toy:readme');
    source.binding_status = bindingStatus;
    source.observed_sha256 = bindingStatus === 'digest_mismatch' ? '0'.repeat(64) : null;
    payload.verification_prompts = buildVerificationPromptProjections(payload, payload.scene_manifest);
    await route.fulfill({ response, json: payload });
  });

  for (const status of ['object_unavailable', 'path_missing', 'digest_mismatch']) {
    bindingStatus = status;
    await page.goto(`/demo/research-tower?binding-failure=${status}`);
    await page.getByRole('button', { name: /Evidence floor 1 of 3/ }).click();
    const failedBinding = page.locator(`[data-list="verification-bindings"] [data-binding-status="${status}"]`);
    await expect(failedBinding).toHaveCount(1);
    await expect(failedBinding).toContainText('repository git:domainspec-core');
    await expect(failedBinding).toContainText('object 1a3b5747554b232020def052a779b1b06713d27a');
    await expect(failedBinding).toContainText('path projects/cyberalchemy-lab/research/tower-evidence-navigator/fixtures/source/toy-tower/README.md');
    await expect(failedBinding).toContainText(`observed SHA-256 ${status === 'digest_mismatch' ? '0'.repeat(64) : 'unavailable'}`);
    await expect(page.locator('[data-panel="scene-content"]')).toContainText(`Ordinary sourced claim unavailable: source:toy:readme is ${status}`);
    await expect(page.locator('[data-panel="scene-content"]')).not.toContainText('Locked synthetic source anchors, locators, digests, and byte sizes.');
    await expect(page.locator('[data-list="known-evidence"]')).toContainText('no combined floor claim is presented');
    await expect(page.locator('[data-list="known-evidence"]')).not.toContainText('Locked synthetic source anchors expose locators');
    await expect(page.locator('[data-list="unbound-evidence"]')).toContainText(status);
    await expect(page.locator('[data-list="unbound-evidence"]')).toContainText('Ordinary sourced claim suppressed');
    const sourceControl = page.locator('[data-source-id="source:toy:readme"]');
    await expect(sourceControl).toContainText(status);
    await sourceControl.click();
    await expect(page.locator('[data-panel="source-detail"]')).toContainText(`Binding: ${status}`);
    await expect(page.locator('[data-panel="source-detail"]')).toContainText('Git object: 1a3b5747554b232020def052a779b1b06713d27a');
  }
  expect(pageErrors).toEqual([]);
  expect(consoleErrors).toEqual([]);
  expect(mutationRequests).toEqual([]);
});

test('tower and open room reflow without horizontal clipping at exact narrow viewports', async ({ page }, testInfo) => {
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.goto('/demo/research-tower');
  for (const viewport of [{ width: 390, height: 844 }, { width: 320, height: 568 }]) {
    await page.setViewportSize(viewport);
    await page.locator('[data-action="reset-orientation"]').click();
    await expect(page.locator('#floor-room')).toBeHidden();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
    const overviewContained = await page.evaluate(() => {
      const viewportWidth = document.documentElement.clientWidth;
      return [...document.querySelectorAll('button:not([disabled]), select:not([disabled]), [data-object="research-tower"], [data-region="system-reference"]')]
        .every((node) => {
          const rect = node.getBoundingClientRect();
          return rect.x >= -1 && rect.right <= viewportWidth + 1;
        });
    });
    expect(overviewContained).toBe(true);
    await page.getByRole('button', { name: /Evidence floor 1 of 3/ }).click();
    await expect(page.locator('#floor-room')).toBeVisible();
    const geometry = await page.evaluate(() => {
      const viewportWidth = document.documentElement.clientWidth;
      const meaningful = [...document.querySelectorAll('button:not([disabled]), select:not([disabled]), [data-panel="floor-room"], [data-panel="room-scene"], [data-region="system-reference"]')];
      const bounds = meaningful.map((node) => {
        const rect = node.getBoundingClientRect();
        return { x: rect.x, right: rect.right };
      });
      const elevation = document.querySelector('[data-panel="tower-elevation"]').getBoundingClientRect();
      const room = document.querySelector('[data-panel="floor-room"]').getBoundingClientRect();
      const system = document.querySelector('[data-region="system-reference"]').getBoundingClientRect();
      return {
        viewportWidth,
        noHorizontalScroll: document.documentElement.scrollWidth <= viewportWidth,
        allContained: bounds.every((rect) => rect.x >= -1 && rect.right <= viewportWidth + 1),
        order: elevation.top < room.top && room.top < system.top,
        bodyOverflowX: getComputedStyle(document.body).overflowX
      };
    });
    expect(geometry.noHorizontalScroll).toBe(true);
    expect(geometry.allContained).toBe(true);
    expect(geometry.order).toBe(true);
    expect(['hidden', 'clip']).not.toContain(geometry.bodyOverflowX);
    if (viewport.width === 320) {
      await page.screenshot({ path: testInfo.outputPath('cutaway-open-320x568.png'), fullPage: true });
    }
  }
  expect(errors).toEqual([]);
});

test('cutaway tower fails closed when the locked witness is unavailable', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.route('**/api/research-tower/l0', (route) => route.fulfill({
    status: 503,
    contentType: 'application/json',
    body: JSON.stringify({ message: 'Locked witness deliberately unavailable' })
  }));
  await page.goto('/demo/research-tower');
  await expect(page.locator('#connection-status')).toHaveText('Witness unavailable');
  await expect(page.locator('#selection-status')).toContainText('Locked witness deliberately unavailable');
  await expect(page.locator('[data-panel="active-floor-summary"]')).toHaveText('No evidence floor is selected while the witness is unavailable.');
  await expect(page.locator('[data-list="levels"] .tower-floor')).toHaveCount(0);
  await expect(page.locator('[data-list="system-levels"] [data-system-level-id]')).toHaveCount(0);
  await expect(page.locator('#floor-room')).toBeHidden();
  await expect(page.locator('[data-panel="system-refusal"]')).toBeHidden();
  await expect(page.locator('[data-action="reset-orientation"]')).toBeDisabled();
  await expect(page.locator('[data-action="toggle-floor-room"]')).toBeDisabled();
  await expect(page.locator('[data-action="show-candidate"]')).toBeDisabled();
  await expect(page.locator('[data-field="relation-filter"]')).toBeDisabled();
  await page.evaluate(() => {
    document.querySelector('[data-action="reset-orientation"]').click();
    document.querySelector('[data-action="toggle-floor-room"]').click();
    document.querySelector('[data-action="show-candidate"]').click();
    document.querySelector('[data-field="relation-filter"]').dispatchEvent(new Event('change'));
  });
  await page.waitForTimeout(50);
  expect(errors).toEqual([]);
});
