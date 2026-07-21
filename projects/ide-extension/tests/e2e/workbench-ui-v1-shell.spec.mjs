import { expect, test } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const evidenceDir = path.join(
  projectRoot,
  'development/workbench-ui-v1/task-sessions/20260720T154814Z-swu-wui-002'
);

function layoutSnapshot() {
  const selectors = [
    '[data-region="work"]',
    '[data-region="canvas"]',
    '.inspector-column'
  ];
  const rectangles = selectors.map((selector) => {
    const rect = document.querySelector(selector).getBoundingClientRect();
    return {
      selector,
      left: rect.left,
      right: rect.right,
      top: rect.top,
      bottom: rect.bottom,
      width: rect.width,
      height: rect.height
    };
  });
  const inspector = document.querySelector('.inspector-column').getBoundingClientRect();
  const inspectorControls = [...document.querySelectorAll('.inspector-column .action-bar input, .inspector-column .action-bar button')]
    .filter((element) => {
      const style = window.getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
    })
    .map((element) => {
      const rect = element.getBoundingClientRect();
      return { left: rect.left, right: rect.right, top: rect.top, bottom: rect.bottom };
    });
  const overlaps = [];
  for (let left = 0; left < rectangles.length; left += 1) {
    for (let right = left + 1; right < rectangles.length; right += 1) {
      const a = rectangles[left];
      const b = rectangles[right];
      const width = Math.min(a.right, b.right) - Math.max(a.left, b.left);
      const height = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (width > 2 && height > 2) overlaps.push(`${a.selector}:${b.selector}`);
    }
  }
  return {
    rectangles,
    overlaps,
    clippedInspectorControls: inspectorControls.filter((rect) => (
      rect.left < inspector.left - 1
      || rect.right > inspector.right + 1
      || rect.top < inspector.top - 1
      || rect.bottom > inspector.bottom + 1
    )),
    canvasBackground: window.getComputedStyle(document.querySelector('#canvas-stage')).backgroundColor,
    horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
    bodyTextLength: document.body.innerText.trim().length
  };
}

test('desktop shell keeps Work, Canvas, and Inspector usable in one grid', async ({ page }) => {
  const consoleErrors = [];
  const pageErrors = [];
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });
  page.on('pageerror', (error) => pageErrors.push(error.message));

  await page.goto('/demo/l0');
  await expect(page.getByRole('region', { name: 'Work' })).toBeVisible();
  await expect(page.getByRole('region', { name: 'Canvas' })).toBeVisible();
  await expect(page.locator('.inspector-column')).toBeVisible();
  await expect(page.locator('[data-action="prepare"]')).toBeVisible();
  await expect(page.locator('[data-action="approve"]')).toBeVisible();
  await expect(page.locator('[data-action="canvas-refresh"]')).toBeVisible();

  const layout = await page.evaluate(layoutSnapshot);
  expect(layout.horizontalOverflow).toBe(false);
  expect(layout.overlaps).toEqual([]);
  expect(layout.clippedInspectorControls).toEqual([]);
  expect(layout.canvasBackground).toBe('rgb(255, 255, 255)');
  expect(layout.bodyTextLength).toBeGreaterThan(120);
  expect(layout.rectangles[0].width).toBeGreaterThanOrEqual(260);
  expect(layout.rectangles[1].width).toBeGreaterThan(500);
  expect(layout.rectangles[2].width).toBeGreaterThanOrEqual(300);
  expect(layout.rectangles[0].right).toBeLessThanOrEqual(layout.rectangles[1].left + 1);
  expect(layout.rectangles[1].right).toBeLessThanOrEqual(layout.rectangles[2].left + 1);

  await mkdir(evidenceDir, { recursive: true });
  const screenshot = await page.screenshot({
    path: path.join(evidenceDir, 'desktop-grid.png'),
    fullPage: true
  });
  expect(screenshot.byteLength).toBeGreaterThan(10_000);
  expect(consoleErrors).toEqual([]);
  expect(pageErrors).toEqual([]);
});
