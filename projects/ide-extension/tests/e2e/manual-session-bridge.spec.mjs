import { expect, test } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const screenshotDir = path.join(
  projectRoot,
  'development/manual-session-bridge-plan/work-pack/evidence/SWU-MSB-010-assets'
);

async function expectCoherentBridgeLayout(page) {
  const layout = await page.evaluate(() => {
    const actionBar = document.querySelector('.action-bar').getBoundingClientRect();
    const controls = [...document.querySelectorAll('.action-bar input, .action-bar button')]
      .filter((element) => element.offsetParent !== null)
      .map((element) => {
        const rect = element.getBoundingClientRect();
        return {
          left: rect.left,
          right: rect.right,
          top: rect.top,
          bottom: rect.bottom,
          width: rect.width,
          height: rect.height
        };
      });
    return {
      horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      bodyTextLength: document.body.innerText.trim().length,
      actionWidth: actionBar.width,
      invalidControls: controls.filter((rect) => (
        rect.left < actionBar.left - 1
        || rect.right > actionBar.right + 1
        || rect.width < 30
        || rect.height < 24
      ))
    };
  });
  expect(layout.horizontalOverflow).toBe(false);
  expect(layout.bodyTextLength).toBeGreaterThan(200);
  expect(layout.actionWidth).toBeGreaterThan(250);
  expect(layout.invalidControls).toEqual([]);
}

async function postJson(request, route, data = {}) {
  const response = await request.post(route, { data });
  const body = await response.json();
  return { response, body };
}

test('manual bridge survives target conflict, interruption, requeue, and terminal evidence', async ({ page, request }, testInfo) => {
  const consoleErrors = [];
  const pageErrors = [];
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });
  page.on('pageerror', (error) => pageErrors.push(error.message));

  const viewportName = testInfo.project.name;
  const task = `${viewportName} blind bridge ${'ReadableSegment'.repeat(5)}`;
  const conflictTask = `${viewportName} singleton conflict`;
  await page.goto('/demo/l0');
  await expect(page.locator('#server-status')).toHaveText('Connected');

  const taskInput = page.locator('[data-field="task-input"]');
  await page.locator('[data-action="prepare"]').click();
  await expect(taskInput).toBeFocused();
  await expect(page.locator('#task-error')).toBeVisible();

  await taskInput.fill(task);
  await page.locator('[data-field="skill-input"]').fill('decision-gate');
  await page.locator('[data-action="prepare"]').click();
  await expect(page.locator('#detail-heading')).toHaveText(task);
  const envelopeId = await page.locator('#detail-subtitle').textContent();

  page.once('dialog', (dialog) => dialog.accept());
  await page.locator('[data-action="approve"]').click();
  await expect(page.locator('#detail-status')).toHaveText('Approved - select as poll target');
  await expect(page.locator('[data-list="receipts"] .receipt-row')).toHaveCount(1);
  await expect(page.locator('.receipt-kind')).toHaveText('authorization.receipt');
  await expect(page.locator('.receipt-claim')).toContainText('Authorization only');

  await page.locator('[data-action="ready"]').click();
  await expect(page.locator('#detail-status')).toHaveText('Ready for poll');
  await expect(page.locator('#ready-target')).toContainText(envelopeId);
  await expect(page.locator('#announcement')).toHaveText('Request selected as the poll target');

  const ready = await request.get('/api/bridge/requests/ready?agent_ref=codex.current-session');
  const readyText = await ready.text();
  expect(ready.ok()).toBeTruthy();
  expect(readyText).not.toContain('decision-gate');
  expect(readyText).not.toContain(task);

  const conflictPrepared = await postJson(request, '/api/envelopes/prepare', {
    task: conflictTask,
    requested_skill: 'decision-gate',
    requested_grants: ['preview.read', 'skill.invoke']
  });
  await postJson(request, `/api/approvals/${conflictPrepared.body.approval.approval_id}/approve`);
  await page.locator('[data-action="refresh"]').click();
  await page.locator(`[data-proposal-id="${conflictPrepared.body.envelope.envelope_id}"]`).click();
  await page.locator('[data-action="ready"]').click();
  await expect(page.locator('#error-strip')).toBeVisible();
  await expect(page.locator('#error-message')).toHaveText('ready_target_exists');

  const claimed = await postJson(request, `/api/bridge/requests/${envelopeId}/claim`, {
    schema_version: '2',
    envelope_id: envelopeId,
    agent_ref: 'codex.current-session',
    session_ref: `playwright-${viewportName}-first`,
    assurance: 'unattested'
  });
  expect(claimed.response.status()).toBe(201);
  expect(claimed.body.execution.requested_skill).toBe('decision-gate');
  await page.locator('[data-action="refresh"]').click();
  await page.locator(`[data-proposal-id="${envelopeId}"]`).click();
  await expect(page.locator('#detail-status')).toHaveText('Claimed by unattested local session');
  await expect(page.locator('[data-list="bridge-fields"]')).toContainText(`playwright-${viewportName}-first`);
  await expect(page.locator('[data-list="bridge-fields"]')).toContainText('unattested');

  const firstClaim = claimed.body.claim;
  const interrupted = await postJson(request, `/api/bridge/claims/${firstClaim.claim_id}/interrupt`, {
    schema_version: '2',
    claim_id: firstClaim.claim_id,
    envelope_id: envelopeId,
    session_ref: firstClaim.session_ref,
    assurance: 'unattested',
    reason: 'Playwright claimant stopped before returning evidence.'
  });
  expect(interrupted.response.ok()).toBeTruthy();
  await page.locator('[data-action="refresh"]').click();
  await expect(page.locator('#detail-status')).toContainText('Interrupted');
  await expect(page.locator('[data-action="release"]')).toBeEnabled();
  await expect(page.locator('[data-list="bridge-fields"]')).toContainText('Playwright claimant stopped');

  await page.locator('[data-field="reject-reason"]').fill('Operator permits one fresh read-only attempt.');
  page.once('dialog', (dialog) => dialog.accept());
  await page.locator('[data-action="release"]').click();
  await expect(page.locator('#detail-status')).toHaveText('Approved - select as poll target');
  await expect(page.locator('[data-list="bridge-fields"]')).toContainText('Operator permits one fresh read-only attempt.');
  await page.locator('[data-action="ready"]').click();

  const secondClaimed = await postJson(request, `/api/bridge/requests/${envelopeId}/claim`, {
    schema_version: '2',
    envelope_id: envelopeId,
    agent_ref: 'codex.current-session',
    session_ref: `playwright-${viewportName}-second`,
    assurance: 'unattested'
  });
  const claim = secondClaimed.body.claim;
  const completed = await postJson(request, `/api/bridge/claims/${claim.claim_id}/result`, {
    schema_version: '2',
    claim_id: claim.claim_id,
    claim_attempt_id: claim.claim_attempt_id,
    envelope_id: envelopeId,
    run_id: claim.run_id,
    approval_id: claim.approval_id,
    session_ref: claim.session_ref,
    assurance: 'unattested',
    requested_skill: 'decision-gate',
    skill_sha256: 'e'.repeat(64),
    status: 'passed',
    summary: 'Browser bridge completed with bound read-only evidence.',
    validation: ['desktop or mobile state matrix inspected'],
    evidence_refs: ['projects/ide-extension/SPEC.md']
  });
  expect(completed.response.status()).toBe(201);

  await page.locator('[data-action="refresh"]').click();
  await page.locator('[data-view="history"]').click();
  await page.locator(`[data-proposal-id="${envelopeId}"]`).click();
  await expect(page.locator('#detail-status')).toHaveText('Passed');
  await expect(page.locator('[data-list="receipts"] .receipt-row')).toHaveCount(2);
  await expect(page.locator('.receipt-kind')).toHaveText(['authorization.receipt', 'skill.execution']);
  await expect(page.locator('[data-list="bridge-fields"]')).toContainText('Browser bridge completed');
  await expect(page.locator('[data-list="bridge-fields"]')).toContainText('desktop or mobile state matrix inspected');
  await expect(page.locator('[data-list="bridge-fields"]')).toContainText('Playwright claimant stopped before returning evidence.');
  await expect(page.locator('#error-strip')).toBeHidden();
  await page.locator('[data-evidence-kind="result"]').click();
  await expect(page.locator('#evidence-title')).toHaveText('Result evidence');
  await expect(page.locator('[data-list="evidence-fields"]')).toContainText('Browser bridge completed');

  await expectCoherentBridgeLayout(page);
  await mkdir(screenshotDir, { recursive: true });
  const screenshot = await page.screenshot({
    path: path.join(screenshotDir, `${viewportName}-terminal.png`),
    fullPage: true
  });
  expect(screenshot.byteLength).toBeGreaterThan(10_000);
  const unexpectedConsoleErrors = consoleErrors.filter((message) => (
    !message.includes('status of 409 (Conflict)')
  ));
  expect(unexpectedConsoleErrors).toEqual([]);
  expect(pageErrors).toEqual([]);
});
