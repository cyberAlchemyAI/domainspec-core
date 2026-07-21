import { expect, test } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const screenshotDir = path.join(
  projectRoot,
  'development/workbench-ui-v1/task-sessions/20260720T155936Z-swu-wui-003'
);

async function expectMobileFit(page) {
  const layout = await page.evaluate(() => {
    const visible = (element) => {
      const style = window.getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== 'none'
        && style.visibility !== 'hidden'
        && rect.width > 0
        && rect.height > 0;
    };
    const controls = [...document.querySelectorAll('button, input, a')].filter(visible);
    const overflow = controls.map((element) => {
      const rect = element.getBoundingClientRect();
      return {
        label: element.textContent?.trim() || element.getAttribute('aria-label') || element.id,
        right: rect.right,
        left: rect.left,
        contentOverflow: element.scrollWidth > element.clientWidth + 1
      };
    }).filter((item) => item.left < -1 || item.right > window.innerWidth + 1 || item.contentOverflow);
    return {
      horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      overflow
    };
  });

  expect(layout.horizontalOverflow).toBe(false);
  expect(layout.overflow).toEqual([]);
}

test('mobile workbench reaches Work, Canvas, and Evidence without losing state', async ({ page }) => {
  await page.goto('/demo/l0');
  await expect(page.locator('#server-status')).toHaveText('Connected');

  const tablist = page.getByRole('tablist', { name: 'Mobile workbench views' });
  const workTab = page.getByRole('tab', { name: 'Work', exact: true });
  const canvasTab = page.getByRole('tab', { name: 'Canvas', exact: true });
  const evidenceTab = page.getByRole('tab', { name: 'Evidence', exact: true });
  await expect(tablist).toBeVisible();
  await expect(workTab).toHaveAttribute('aria-selected', 'true');
  await expect(page.locator('#work-region')).toBeVisible();
  await expect(page.locator('#canvas-region')).toBeHidden();
  await expect(page.locator('#evidence-region')).toBeHidden();

  await page.locator('[data-request-mode="dry-run"]').click();
  const task = 'Mobile navigation preserves the prepared proposal';
  await page.locator('[data-field="task-input"]').fill(task);
  await page.locator('[data-action="prepare"]').click();
  await expect(page.locator('[data-proposal-id]').filter({ hasText: task })).toBeVisible();

  await canvasTab.click();
  await expect(canvasTab).toHaveAttribute('aria-selected', 'true');
  await expect(page.locator('#canvas-region')).toBeVisible();
  await expect(page.locator('#work-region')).toBeHidden();
  await expect(page.locator('#evidence-region')).toBeHidden();
  await expect(page.locator('#canvas-title')).toBeVisible();
  await expectMobileFit(page);

  await canvasTab.press('ArrowRight');
  await expect(evidenceTab).toHaveAttribute('aria-selected', 'true');
  await expect(page.locator('#evidence-region')).toBeVisible();
  await expect(page.locator('#canvas-region')).toBeHidden();
  await expect(page.locator('#evidence-heading')).toBeVisible();
  await expectMobileFit(page);

  await workTab.click();
  await expect(workTab).toHaveAttribute('aria-selected', 'true');
  await expect(page.locator('[data-proposal-id]').filter({ hasText: task })).toBeVisible();
  await expect(page.locator('#canvas-meta')).toHaveText('No surface published');
  await expectMobileFit(page);

  await evidenceTab.click();
  await mkdir(screenshotDir, { recursive: true });
  const screenshot = await page.screenshot({
    path: path.join(screenshotDir, 'mobile-evidence.png'),
    fullPage: true
  });
  expect(screenshot.byteLength).toBeGreaterThan(10_000);
});
