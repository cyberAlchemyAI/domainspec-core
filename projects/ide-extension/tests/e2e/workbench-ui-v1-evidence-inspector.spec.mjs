import { expect, test } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const screenshotDir = path.join(
  projectRoot,
  'development/workbench-ui-v1/task-sessions/20260720T172635Z-swu-wui-010'
);

async function postJson(request, route, data = {}) {
  const response = await request.post(route, { data });
  const body = await response.json();
  return { response, body };
}

async function showView(page, projectName, view) {
  if (projectName === 'mobile') {
    await page.locator(`.mobile-view-nav [data-mobile-view="${view}"]`).click();
  }
}

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
          left: rect.left,
          right: rect.right,
          contentOverflow: element.scrollWidth > element.clientWidth + 1
        };
      }).filter((item) => item.left < -1 || item.right > window.innerWidth + 1 || item.contentOverflow)
    };
  });
  expect(layout.horizontalOverflow).toBe(false);
  expect(layout.overflow).toEqual([]);
}

test('Inspector keeps terminal receipt evidence attributable to one admitted run', async ({ page, request }, testInfo) => {
  const projectName = testInfo.project.name;
  const task = `WUI-010 retained receipt ${projectName}`;
  const contextRef = 'projects/ide-extension/SPEC.md';

  await page.goto('/demo/l0');
  await expect(page.locator('#server-status')).toHaveText('Connected');
  await page.locator('[data-field="task-input"]').fill(task);
  await page.locator('[data-field="skill-input"]').fill('decision-gate');
  await page.locator('[data-field="context-input"]').fill(contextRef);
  await page.locator('[data-action="prepare"]').click();

  const state = await (await request.get('/api/state')).json();
  const approval = state.approval_queue.find((candidate) => candidate.title === task);
  expect(approval).toBeTruthy();
  const envelopeId = approval.envelope_id;
  await page.locator(`[data-proposal-id="${envelopeId}"]`).click();
  await showView(page, projectName, 'evidence');
  await expect(page.locator('#detail-heading')).toHaveText(task);
  await expect(page.locator('[data-list="contract-fields"]')).toContainText(envelopeId);
  await expect(page.locator('[data-list="grants"]')).toContainText('preview.read');
  await expect(page.locator('[data-list="grants"]')).toContainText('skill.invoke');
  await expect(page.locator('[data-list="context-refs"]')).toContainText(contextRef);

  page.once('dialog', (dialog) => dialog.accept());
  await page.locator('[data-action="approve"]').click();
  await expect(page.locator('[data-list="receipts"] .receipt-row')).toHaveCount(1);
  const authorizationReceiptId = await page.locator('[data-list="receipts"] .receipt-row').first().locator('[data-evidence-kind]').first().getAttribute('data-receipt-id');
  expect(authorizationReceiptId).toBeTruthy();
  await page.locator('[data-action="ready"]').click();

  const ready = await request.get('/api/bridge/requests/ready');
  expect(ready.ok()).toBeTruthy();
  const readyBody = await ready.json();
  expect(JSON.stringify(readyBody)).not.toContain(task);
  expect(JSON.stringify(readyBody)).not.toContain('decision-gate');
  expect(JSON.stringify(readyBody)).not.toContain(contextRef);

  const claimed = await postJson(request, `/api/bridge/requests/${envelopeId}/claim`, {
    schema_version: '2',
    envelope_id: envelopeId,
    agent_ref: `wui-010-${projectName}`,
    session_ref: `wui-010-session-${projectName}`,
    assurance: 'unattested'
  });
  expect(claimed.response.status()).toBe(201);
  const claim = claimed.body.claim;
  expect(claimed.body.execution.requested_skill).toBe('decision-gate');
  expect(claimed.body.execution.requested_grants).toEqual(['preview.read', 'skill.invoke']);
  expect(claimed.body.execution.context_refs).toEqual([contextRef]);

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
    summary: `WUI-010 admitted result for ${projectName}.`,
    validation: ['Inspector attribution checked', 'Evidence groups resolved'],
    evidence_refs: [contextRef]
  });
  expect(completed.response.status()).toBe(201);
  expect(completed.body.receipt.receipt_kind).toBe('skill.execution');

  await showView(page, projectName, 'work');
  await page.locator('[data-action="refresh"]').click();
  await page.locator('[data-view="history"]').click();
  await page.locator(`[data-proposal-id="${envelopeId}"]`).click();
  await showView(page, projectName, 'evidence');
  await expect(page.locator('#detail-status')).toHaveText('Passed');
  await expect(page.locator('[data-action="inspect"]')).toBeVisible();
  await expect(page.locator('[data-action="inspect"]')).toBeEnabled();
  await page.locator('[data-action="inspect"]').click();
  await expect(page.locator('#announcement')).toHaveText('Evidence view opened');

  await expect(page.locator('[data-list="receipts"] .receipt-row')).toHaveCount(2);
  await expect(page.locator('.receipt-kind')).toHaveText(['authorization.receipt', 'skill.execution']);
  await expect(page.locator('.receipt-claim').nth(0)).toContainText('Authorization only');
  await expect(page.locator('.receipt-claim').nth(1)).toContainText('WUI-010 admitted result');
  const executionReceiptId = completed.body.receipt.receipt_id;
  expect(await page.locator(`[data-receipt-id="${executionReceiptId}"]`).count()).toBe(4);

  const identityText = [envelopeId, claim.run_id, claim.approval_id];
  await expect(page.locator('[data-list="contract-fields"]')).toContainText(envelopeId);
  await expect(page.locator('[data-list="contract-fields"]')).toContainText(claim.run_id);
  await expect(page.locator('[data-list="contract-fields"]')).toContainText(claim.approval_id);
  await expect(page.locator('[data-list="bridge-fields"]')).toContainText('Inspector attribution checked');
  await expect(page.locator('[data-list="bridge-fields"]')).toContainText('Evidence groups resolved');
  await expect(page.locator('[data-list="bridge-fields"]')).toContainText(contextRef);

  const evidenceKinds = [
    [authorizationReceiptId, 'before'],
    [authorizationReceiptId, 'after'],
    [authorizationReceiptId, 'receipt'],
    [executionReceiptId, 'before'],
    [executionReceiptId, 'after'],
    [executionReceiptId, 'receipt'],
    [executionReceiptId, 'result']
  ];
  for (const [receiptId, kind] of evidenceKinds) {
    const button = page.locator(`[data-receipt-id="${receiptId}"][data-evidence-kind="${kind}"]`);
    await expect(button).toBeVisible();
    await button.click();
    await expect(page.locator('#evidence-title')).toHaveText(`${kind[0].toUpperCase()}${kind.slice(1)} evidence`);
    const evidenceText = await page.locator('[data-list="evidence-fields"]').innerText();
    for (const identity of identityText) expect(evidenceText).toContain(identity);
  }

  const afterEvidenceState = await (await request.get('/api/state')).json();
  expect(afterEvidenceState.event_count).toBe(state.event_count + 4);
  if (projectName === 'mobile') await expectMobileFit(page);

  await mkdir(screenshotDir, { recursive: true });
  const screenshot = await page.screenshot({
    path: path.join(screenshotDir, `${projectName}-evidence-inspector.png`),
    fullPage: true
  });
  expect(screenshot.byteLength).toBeGreaterThan(10_000);
});
