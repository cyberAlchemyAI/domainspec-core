import { expect, test } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const screenshotDir = path.join(
  projectRoot,
  'development/l0-human-approval-desk-plan/work-pack/evidence/SWU-IDEAD-009-assets'
);

async function stateFrom(request) {
  const response = await request.get('/api/state');
  expect(response.ok()).toBeTruthy();
  return response.json();
}

async function proposalByTitle(request, title) {
  const state = await stateFrom(request);
  const approval = state.approval_queue.find((candidate) => candidate.title === title);
  expect(approval).toBeTruthy();
  return approval;
}

async function expectCoherentLayout(page) {
  const layout = await page.evaluate(() => {
    const selectors = ['.app-header', '.queue-panel', '.detail-panel', '.evidence-panel'];
    const rectangles = selectors.map((selector) => {
      const rect = document.querySelector(selector).getBoundingClientRect();
      return { selector, left: rect.left, right: rect.right, top: rect.top, bottom: rect.bottom };
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
      horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      overlaps,
      bodyTextLength: document.body.innerText.trim().length
    };
  });

  expect(layout.horizontalOverflow).toBe(false);
  expect(layout.overlaps).toEqual([]);
  expect(layout.bodyTextLength).toBeGreaterThan(120);
}

test('human approval workflow survives disposition, reload, and evidence review', async ({ page, request }, testInfo) => {
  const consoleErrors = [];
  const pageErrors = [];
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });
  page.on('pageerror', (error) => pageErrors.push(error.message));

  const viewportName = testInfo.project.name;
  const taskA = `${viewportName} A ${'LongContractSegment'.repeat(7)}`;
  const taskB = `${viewportName} B reject proposal`;

  await page.goto('/demo/l0');
  await expect(page.getByRole('heading', { name: 'Cyber Alchemy' })).toBeVisible();
  await expect(page.getByText('Approval Desk · local workbench', { exact: true })).toBeVisible();
  await expect(page.locator('#server-status')).toHaveText('Connected');
  await expectCoherentLayout(page);

  const taskInput = page.locator('[data-field="task-input"]');
  await taskInput.fill(taskA);
  await page.locator('[data-action="prepare"]').click();
  await expect(page.locator('[data-proposal-id]').filter({ hasText: taskA })).toBeVisible();

  await taskInput.fill(taskB);
  await page.locator('[data-action="prepare"]').click();
  await expect(page.locator('[data-proposal-id]').filter({ hasText: taskB })).toBeVisible();

  const approvalA = await proposalByTitle(request, taskA);
  const approvalB = await proposalByTitle(request, taskB);
  const proposalA = page.locator(`[data-proposal-id="${approvalA.envelope_id}"]`);
  const proposalB = page.locator(`[data-proposal-id="${approvalB.envelope_id}"]`);
  await proposalA.click();
  await expect(page.locator('#detail-heading')).toHaveText(taskA);
  await expect(page.locator('[data-action="approve"]')).toBeEnabled();

  let reachedQueue = false;
  let reachedApprove = false;
  let visibleFocus = false;
  await page.locator('body').click({ position: { x: 1, y: 1 } });
  for (let step = 0; step < 18; step += 1) {
    await page.keyboard.press('Tab');
    const focus = await page.evaluate(() => {
      const active = document.activeElement;
      const style = window.getComputedStyle(active);
      return {
        proposal: Boolean(active?.dataset?.proposalId),
        action: active?.dataset?.action || null,
        outline: style.outlineStyle !== 'none' && style.outlineWidth !== '0px'
      };
    });
    reachedQueue ||= focus.proposal;
    if (focus.action === 'approve') {
      reachedApprove = true;
      visibleFocus = focus.outline;
      break;
    }
  }
  expect(reachedQueue).toBe(true);
  expect(reachedApprove).toBe(true);
  expect(visibleFocus).toBe(true);

  page.once('dialog', (dialog) => dialog.accept());
  await page.locator('[data-action="approve"]').click();
  await expect(page.locator('#detail-status')).toHaveText('passed');
  await expect(page.locator('[data-action="approve"]')).toBeDisabled();

  const replay = await request.post(`/api/approvals/${approvalA.approval_id}/approve`, { data: {} });
  expect(replay.status()).toBe(409);
  expect((await replay.json()).error).toBe('already_resolved');

  await proposalB.click();
  await page.locator('[data-field="reject-reason"]').fill('browser proof rejection');
  page.once('dialog', (dialog) => dialog.accept());
  await page.locator('[data-action="reject"]').click();
  await expect(page.locator('#detail-status')).toHaveText('blocked');
  await expect(page.locator('[data-action="reject"]')).toBeDisabled();

  const rejectedDetailResponse = await request.get(`/api/proposals/${approvalB.envelope_id}`);
  const rejectedDetail = await rejectedDetailResponse.json();
  expect(rejectedDetail.receipts).toEqual([]);
  expect(rejectedDetail.approval.rejection_reason).toBe('browser proof rejection');

  await page.locator('[data-view="history"]').click();
  await expect(page.locator(`[data-proposal-id="${approvalA.envelope_id}"]`)).toBeVisible();
  await expect(page.locator(`[data-proposal-id="${approvalB.envelope_id}"]`)).toBeVisible();

  await page.reload();
  await expect(page.locator('#server-status')).toHaveText('Connected');
  await page.locator('[data-view="history"]').click();
  await page.locator(`[data-proposal-id="${approvalA.envelope_id}"]`).click();
  await expect(page.locator('#detail-status')).toHaveText('passed');
  await expect(page.locator('[data-list="receipts"] .receipt-row')).toHaveCount(1);

  const approvedDetailResponse = await request.get(`/api/proposals/${approvalA.envelope_id}`);
  const approvedDetail = await approvedDetailResponse.json();
  const receipt = approvedDetail.receipts[0];
  for (const kind of ['before', 'after', 'receipt']) {
    await page.locator(`[data-evidence-kind="${kind}"]`).click();
    await expect(page.locator('#evidence-title')).toHaveText(`${kind[0].toUpperCase() + kind.slice(1)} evidence`);
    await expect(page.locator('[data-list="evidence-fields"]')).toContainText(approvalA.envelope_id);

    const evidenceResponse = await request.get(receipt.evidence[kind]);
    expect(evidenceResponse.ok()).toBeTruthy();
    const evidence = await evidenceResponse.json();
    expect(evidence.run_id).toBe(approvalA.run_id);
    expect(evidence.envelope_id).toBe(approvalA.envelope_id);
    expect(evidence.approval_id).toBe(approvalA.approval_id);
  }

  await expectCoherentLayout(page);
  await mkdir(screenshotDir, { recursive: true });
  const screenshot = await page.screenshot({
    path: path.join(screenshotDir, `${viewportName}.png`),
    fullPage: true
  });
  expect(screenshot.byteLength).toBeGreaterThan(10_000);
  expect(consoleErrors).toEqual([]);
  expect(pageErrors).toEqual([]);
});
