import { expect, test } from '@playwright/test';

test('tower scene canvas supports evidence selection, refusal, and source inspection', async ({ page }, testInfo) => {
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.goto('/demo/research-tower');
  await expect(page.locator('[data-workbench="tower-scene-canvas"]')).toBeVisible();
  await expect(page.locator('[data-layout="spatial-canvas"]')).toBeVisible();
  await expect(page.locator('#connection-status')).toHaveText('Witness verified');
  await expect(page.locator('[data-list="towers"] [data-tower-id="tower:toy"]')).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-list="levels"] [data-scene-id]')).toHaveCount(3);
  await expect(page.locator('[data-panel="scene-status"]')).toContainText('locked-synthetic');
  const residueScene = page.locator('[data-scene-id="evidence-l1-residue"]');
  await residueScene.focus();
  await page.keyboard.press('Space');
  await expect(residueScene).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-panel="scene-status"]')).toContainText('open');
  await expect(page.locator('[data-panel="scene-content"]')).toContainText('Which real tower');
  await page.locator('[data-system-level-id="system-lphi-policy"]').click();
  await expect(page.locator('[data-panel="scene-status"]')).toContainText('Unavailable');
  await expect(page.locator('[data-panel="scene-unavailable"]')).toContainText('MOGT has no live Lab run');
  await page.locator('[data-action="focus-tower"]').click();
  await expect(page.locator('#lab-canvas')).toHaveClass(/tower-focused/);
  await page.locator('[data-action="reset-orientation"]').click();
  await expect(page.locator('#lab-canvas')).not.toHaveClass(/tower-focused/);
  await expect(page.locator('[data-scene-id="evidence-l0-corpus"]')).toBeFocused();
  await expect(page.locator('[data-list="sources"] button')).toHaveCount(7);
  await page.locator('[data-source-id="source:toy:l0"]').click();
  await expect(page.locator('[data-panel="source-detail"]')).toContainText('fixtures/source/toy-tower/levels/L0-corpus.md');
  await page.locator('[data-field="relation-filter"]').selectOption('blocked_by');
  await expect(page.locator('[data-list="relations"] .relation')).toHaveCount(2);
  await expect(page.locator('[data-panel="residue-detail"]')).toContainText('open');
  await expect(page.locator('[data-panel="claim-ceiling"]')).toContainText('no representative');
  if (testInfo.project.name === 'mobile') {
    await expect(page.locator('[data-panel="live-lab"]')).toBeHidden();
  } else {
    await expect(page.locator('[data-panel="live-lab"]')).toBeVisible();
  }
  await expect(page.locator('[data-panel="live-lab"]')).toHaveAttribute('aria-hidden', 'true');
  await expect(page.locator('[data-robot-role]')).toHaveCount(3);
  await expect(page.locator('[data-robot-role="source-scout"]')).toHaveCSS('animation-name', /source-scout-route/);
  await expect(page.locator('[data-panel="lab-activity"]')).toContainText('Decorative cowork loop');
  await page.locator('#constellation-core').click();
  await expect(page.locator('#detail-heading')).toHaveText('Candidate meaning');
  await page.getByRole('button', { name: 'Pause lab motion' }).click();
  await expect(page.locator('#lab-canvas')).toHaveClass(/motion-paused/);
  await expect(page.getByRole('button', { name: 'Resume lab motion' })).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-robot-role="source-scout"]')).toHaveCSS('animation-play-state', 'paused');
  await expect(page.locator('.source-orbit')).toHaveCSS('position', 'absolute');
  await expect(page.locator('.guides path').first()).not.toHaveCSS('animation-name', 'none');
  await expect(page.locator('body')).not.toHaveCSS('overflow-x', 'scroll');
  expect(errors).toEqual([]);
});

test('tower scene canvas keeps semantic controls readable with reduced motion', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/demo/research-tower');
  await expect(page.locator('#connection-status')).toHaveText('Witness verified');
  await expect(page.locator('[data-list="levels"] [data-scene-id="evidence-l2-closure"]')).toBeVisible();
  await page.locator('[data-scene-id="evidence-l2-closure"]').click();
  await expect(page.locator('[data-panel="scene-status"]')).toContainText('blocked');
  await expect(page.locator('[data-panel="scene-content"]')).toContainText('cannot select a source');
  await expect(page.locator('.scene.library')).toHaveCSS('animation-duration', '1e-05s');
});
