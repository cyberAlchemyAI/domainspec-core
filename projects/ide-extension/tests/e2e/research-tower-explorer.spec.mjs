import { expect, test } from '@playwright/test';

test('cutaway tower opens one stable room and keeps floor, System, and inspector state separate', async ({ page }) => {
  const pageErrors = [];
  const consoleErrors = [];
  const failedRequests = [];
  const mutationRequests = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));
  page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  page.on('requestfailed', (request) => failedRequests.push(request.url()));
  page.on('request', (request) => { if (request.method() !== 'GET') mutationRequests.push(`${request.method()} ${request.url()}`); });

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

  await residueFloor.focus();
  await page.keyboard.press('Space');
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
  await expect(toggle).toHaveText('Return to tower overview');
  await expect(toggle).toHaveAttribute('aria-expanded', 'true');

  const source = page.locator('[data-source-id="source:toy:l0"]');
  await source.click();
  await expect(source).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-panel="source-detail"]')).toContainText('fixtures/source/toy-tower/levels/L0-corpus.md');

  await closureFloor.focus();
  await page.keyboard.press('Enter');
  await expect(closureFloor).toBeFocused();
  await expect(room).toHaveAttribute('data-origin-floor', 'evidence-l2-closure');
  await expect(page.locator('[data-panel="scene-status"]')).toHaveText('blocked');
  await expect(page.locator('[data-panel="scene-unavailable"]')).toContainText('No representative source is selected');
  await expect(source).toHaveAttribute('aria-pressed', 'true');

  await toggle.click();
  await expect(toggle).toBeFocused();
  await expect(room).toBeHidden();
  await expect(closureFloor).toHaveAttribute('aria-pressed', 'true');
  await expect(closureFloor).toHaveAttribute('aria-expanded', 'false');
  await expect(toggle).toHaveText('Open selected floor room');
  await toggle.click();
  await expect(room).toBeVisible();
  await expect(room).toHaveAttribute('data-origin-floor', 'evidence-l2-closure');
  await expect(source).toHaveAttribute('aria-pressed', 'true');

  const systemCases = [
    { id: 'system-l1-substrate', status: 'unproven-in-lab', reason: 'runtime-queryable graph and persona artifacts' },
    { id: 'system-l2-construction', status: 'prior-work-not-live-here', reason: 'Construction methods are not active builders' },
    { id: 'system-l3-application', status: 'unavailable-in-lab', reason: 'No debate, dispatch, or persona operation' },
    { id: 'system-lphi-policy', status: 'design-stage-unproven', reason: 'MOGT has no live Lab run' },
    { id: 'system-l4-adjudication', status: 'governance-only', reason: 'cannot score, select a winner, or emit a verdict' }
  ];
  for (const systemCase of systemCases) {
    const control = page.locator(`[data-system-level-id="${systemCase.id}"]`);
    await control.click();
    await expect(control).toBeFocused();
    await expect(control).toHaveAttribute('aria-pressed', 'true');
    expect(await systems.evaluateAll((items) => items.filter((item) => item.getAttribute('aria-pressed') === 'true').length)).toBe(1);
    expect(await floors.evaluateAll((items) => items.every((item) => item.getAttribute('aria-pressed') === 'false' && item.getAttribute('aria-expanded') === 'false'))).toBe(true);
    await expect(room).toBeHidden();
    await expect(toggle).toBeDisabled();
    await expect(systemRefusal).toBeVisible();
    await expect(page.locator('[data-system-field="id"]')).toHaveText(systemCase.id);
    await expect(page.locator('[data-system-field="status"]')).toHaveText('Unavailable in this Lab');
    await expect(page.locator('[data-system-field="implementation"]')).toHaveText(systemCase.status);
    await expect(page.locator('[data-system-field="reason"]')).toContainText(systemCase.reason);
    await expect(page.locator('[data-system-field="source"]')).toContainText('#2-the-layer-stack-bottom-up-one-layer-at-a-time');
  }

  await page.locator('[data-action="reset-orientation"]').click();
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
  await firstFloor.click();
  await firstFloor.click();
  expect(roomNodeIdentity).toBe('floor-room');
  expect(await room.evaluate((node) => node === window.__cutawayRoom)).toBe(true);
  await expect(room).toBeVisible();
  await expect(page.locator('#selection-status')).toContainText('Room open');

  await expect(page.locator('img, canvas, [data-robot-role]')).toHaveCount(0);
  const positions = await page.locator('[data-object="research-tower"], [data-panel="floor-room"], [data-region="system-reference"]').evaluateAll(
    (items) => items.map((item) => getComputedStyle(item).position)
  );
  expect(positions.every((position) => position !== 'fixed')).toBe(true);
  expect(pageErrors).toEqual([]);
  expect(consoleErrors).toEqual([]);
  expect(failedRequests).toEqual([]);
  expect(mutationRequests).toEqual([]);
});

test('cutaway tower remains animation-free under reduced motion', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/demo/research-tower');
  const firstFloor = page.getByRole('button', { name: /Evidence floor 1 of 3/ });
  await firstFloor.click();
  await expect(page.locator('#floor-room')).toBeVisible();
  const motion = await page.locator('[data-object="research-tower"] *').evaluateAll((items) => items.map((item) => {
    const style = getComputedStyle(item);
    return { animationName: style.animationName, transitionDuration: style.transitionDuration };
  }));
  expect(motion.every((item) => item.animationName === 'none' && item.transitionDuration === '0s')).toBe(true);
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
