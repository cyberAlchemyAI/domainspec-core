import { expect, test } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const evidenceDir = path.join(
  projectRoot,
  'development/workbench-ui-v1/task-sessions/20260720T164437Z-swu-wui-007'
);

async function stateFrom(request) {
  const response = await request.get('/api/state');
  expect(response.ok()).toBeTruthy();
  return response.json();
}

test('legal primary action follows RunView through approval, availability, running, and inspection', async ({ page, request }, testInfo) => {
  const task = `WUI-007 ${testInfo.project.name} ${Date.now()}`;
  const showView = async (view) => {
    if (testInfo.project.name === 'mobile') {
      await page.locator(`.mobile-view-nav [data-mobile-view="${view}"]`).click();
    }
  };

  await page.goto('/demo/l0');
  await expect(page.locator('#server-status')).toHaveText('Connected');
  await page.locator('[data-field="task-input"]').fill(task);
  await page.locator('[data-field="skill-input"]').fill('decision-gate');
  await page.locator('[data-action="prepare"]').click();

  const state = await stateFrom(request);
  const approval = state.approval_queue.find((candidate) => candidate.title === task);
  expect(approval).toBeTruthy();
  await page.locator(`[data-proposal-id="${approval.envelope_id}"]`).click();
  await showView('evidence');

  await expect(page.locator('#action-note')).toHaveAttribute('data-primary-action', 'approve');
  await expect(page.locator('[data-action="approve"]')).toBeEnabled();
  await expect(page.locator('[data-action="ready"]')).toBeDisabled();
  await expect(page.locator('[data-action="inspect"]')).toBeHidden();

  page.once('dialog', (dialog) => dialog.accept());
  await page.locator('[data-action="approve"]').click();
  await expect(page.locator('#action-note')).toHaveAttribute('data-primary-action', 'ready');
  await expect(page.locator('[data-action="approve"]')).toBeDisabled();
  await expect(page.locator('[data-action="ready"]')).toBeEnabled();
  await expect(page.locator('[data-action="reject"]')).toBeEnabled();
  await expect(page.locator('[data-action="inspect"]')).toBeHidden();

  await page.locator('[data-action="ready"]').click();
  await expect(page.locator('#action-note')).toHaveAttribute('data-primary-action', 'available');
  await expect(page.locator('[data-action="ready"]')).toBeDisabled();
  await expect(page.locator('[data-action="unready"]')).toBeEnabled();
  await expect(page.locator('[data-action="reject"]')).toBeEnabled();
  await expect(page.locator('[data-action="inspect"]')).toBeHidden();

  const claimResponse = await request.post(
    `/api/bridge/requests/${approval.envelope_id}/claim`,
    {
      data: {
        schema_version: '2',
        envelope_id: approval.envelope_id,
        agent_ref: 'openrouter.local-session',
        session_ref: `wui-007-${testInfo.project.name}`,
        assurance: 'unattested'
      }
    }
  );
  expect(claimResponse.status()).toBe(201);
  await showView('work');
  await page.locator('[data-action="refresh"]').click();
  await page.locator(`[data-proposal-id="${approval.envelope_id}"]`).click();
  await showView('evidence');
  await expect(page.locator('#action-note')).toHaveAttribute('data-primary-action', 'running');
  await expect(page.locator('#action-note')).toContainText('session owns claim');
  await expect(page.locator('[data-action="approve"]')).toBeDisabled();
  await expect(page.locator('[data-action="ready"]')).toBeDisabled();
  await expect(page.locator('[data-action="unready"]')).toBeDisabled();
  await expect(page.locator('[data-action="release"]')).toBeDisabled();
  await expect(page.locator('[data-action="inspect"]')).toBeHidden();

  const dryRun = await request.post('/api/envelopes/prepare', {
    data: { task: `WUI-007 terminal ${testInfo.project.name}` }
  });
  expect(dryRun.status()).toBe(201);
  const dryRunPacket = await dryRun.json();
  const approved = await request.post(`/api/approvals/${dryRunPacket.approval.approval_id}/approve`, { data: {} });
  expect(approved.status()).toBe(201);
  await showView('work');
  await page.locator('[data-action="refresh"]').click();
  await page.locator('[data-view="history"]').click();
  await page.locator(`[data-proposal-id="${dryRunPacket.envelope.envelope_id}"]`).click();
  await showView('evidence');
  await expect(page.locator('#action-note')).toHaveAttribute('data-primary-action', 'inspect');
  await expect(page.locator('[data-action="inspect"]')).toBeVisible();
  await expect(page.locator('[data-action="inspect"]')).toBeEnabled();
  await page.locator('[data-action="inspect"]').click();
  await expect(page.locator('#announcement')).toHaveText('Evidence view opened');
  await mkdir(evidenceDir, { recursive: true });
  const screenshot = await page.screenshot({
    path: path.join(evidenceDir, `${testInfo.project.name}-actions.png`),
    fullPage: true
  });
  expect(screenshot.byteLength).toBeGreaterThan(10_000);
});
