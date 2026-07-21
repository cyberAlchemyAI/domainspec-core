import { expect, test } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const screenshotDir = path.join(
  projectRoot,
  'development/workbench-ui-v1/task-sessions/20260720T170841Z-swu-wui-009'
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
    const controls = [...document.querySelectorAll('button, input, textarea')].filter(visible);
    return {
      horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      overflow: controls.map((element) => {
        const rect = element.getBoundingClientRect();
        return {
          label: element.textContent?.trim() || element.getAttribute('aria-label') || element.id,
          right: rect.right,
          left: rect.left,
          contentOverflow: element.scrollWidth > element.clientWidth + 1
        };
      }).filter((item) => item.left < -1 || item.right > window.innerWidth + 1 || item.contentOverflow)
    };
  });
  expect(layout.horizontalOverflow).toBe(false);
  expect(layout.overflow).toEqual([]);
}

test('Craft selection seeds Task and Context without writing Craft', async ({ page, request }, testInfo) => {
  await page.goto('/demo/l0');
  await expect(page.locator('#server-status')).toHaveText('Connected');

  const beforeFrontier = await (await request.get('/api/craft/frontier')).json();
  const beforeState = await (await request.get('/api/state')).json();
  const source = beforeFrontier.pending[0];
  expect(source).toBeTruthy();

  const sourceButton = page.locator('[data-craft-id]').first();
  await expect(sourceButton).toBeVisible();
  await expect(sourceButton).toHaveAttribute('data-craft-id', source.id);
  await sourceButton.click();

  await expect(page.locator('[data-field="task-input"]')).toHaveValue(source.summary);
  await expect(page.locator('[data-field="context-input"]')).toHaveValue(source.id);
  await expect(sourceButton).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('#announcement')).toHaveText(`Craft source selected: ${source.id}`);
  await expect(page.locator('[data-request-mode="agent-task"]')).toHaveAttribute('aria-checked', 'true');
  await expect(page.locator('[data-field="skill-input"]')).toBeVisible();

  if (testInfo.project.name === 'mobile') {
    await expectMobileFit(page);
  } else {
    const layout = await page.evaluate(() => {
      const work = document.querySelector('[data-region="work"]').getBoundingClientRect();
      const body = document.querySelector('#craft-body').getBoundingClientRect();
      const next = document.querySelector('.craft-next').getBoundingClientRect();
      const list = document.querySelector('#craft-list').getBoundingClientRect();
      const task = document.querySelector('[data-field="task-input"]').getBoundingClientRect();
      const context = document.querySelector('[data-field="context-input"]').getBoundingClientRect();
      const craft = document.querySelector('[data-panel="craft"]').getBoundingClientRect();
      return {
        workLeft: work.left,
        craftLeft: craft.left,
        bodyLeft: body.left,
        bodyRight: body.right,
        nextLeft: next.left,
        nextRight: next.right,
        listRight: list.right,
        craftWidth: craft.width,
        taskWidth: task.width,
        contextWidth: context.width,
        horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
      };
    });
    expect(layout.craftLeft).toBeGreaterThanOrEqual(layout.workLeft - 1);
    expect(layout.bodyLeft).toBeGreaterThanOrEqual(layout.workLeft - 1);
    expect(layout.bodyRight).toBeLessThanOrEqual(layout.workLeft + layout.craftWidth + 1);
    expect(layout.nextLeft).toBeGreaterThanOrEqual(layout.workLeft - 1);
    expect(layout.listRight).toBeLessThanOrEqual(layout.workLeft + layout.craftWidth + 1);
    expect(layout.nextRight - layout.nextLeft).toBeGreaterThan(240);
    expect(layout.craftWidth).toBeGreaterThan(250);
    expect(layout.taskWidth).toBeGreaterThan(150);
    expect(layout.contextWidth).toBeGreaterThan(150);
    expect(layout.horizontalOverflow).toBe(false);
  }

  const afterFrontier = await (await request.get('/api/craft/frontier')).json();
  const afterState = await (await request.get('/api/state')).json();
  expect(afterFrontier.source.sha256).toBe(beforeFrontier.source.sha256);
  expect(afterFrontier.pending).toEqual(beforeFrontier.pending);
  expect(afterState.event_count).toBe(beforeState.event_count);
  expect(afterState.approval_queue).toEqual(beforeState.approval_queue);

  await mkdir(screenshotDir, { recursive: true });
  const screenshot = await page.screenshot({
    path: path.join(screenshotDir, `${testInfo.project.name}-craft-seed.png`),
    fullPage: true
  });
  expect(screenshot.byteLength).toBeGreaterThan(10_000);
});
