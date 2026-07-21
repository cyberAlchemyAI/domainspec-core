import { expect, test } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const evidenceDir = path.join(
  projectRoot,
  'development/workbench-ui-v1/task-sessions/20260720T162753Z-swu-wui-006'
);

const TIMELINE_STAGES = ['prepared', 'approved', 'available', 'running', 'result', 'receipt'];
const RUN_STATES = [
  'awaiting_approval',
  'approved',
  'ready_for_poll',
  'claimed',
  'interrupted',
  'passed',
  'flagged',
  'blocked',
  'failed',
  'completed'
];

function expectedCurrentStage(state) {
  return {
    awaiting_approval: 'prepared',
    approved: 'approved',
    ready_for_poll: 'available',
    claimed: 'running',
    interrupted: 'running',
    passed: 'receipt',
    flagged: 'result',
    blocked: 'result',
    failed: 'result',
    completed: 'result'
  }[state];
}

async function expectTimelineState(page, stage, state) {
  await expect.poll(async () => (
    page.locator('#bridge-flow [data-status="active"]').first().getAttribute('data-stage')
  )).toBe(stage);
  const statuses = await page.locator('#bridge-flow [data-stage]').evaluateAll((items) => (
    items.map((item) => ({
      stage: item.dataset.stage,
      status: item.dataset.status,
      text: item.textContent.trim()
    }))
  ));
  expect(statuses.map((item) => item.stage)).toEqual(TIMELINE_STAGES);
  expect(statuses.filter((item) => item.status === 'active')).toHaveLength(1);
  expect(statuses.find((item) => item.status === 'active').stage).toBe(stage);
  expect(statuses.slice(0, TIMELINE_STAGES.indexOf(stage)).every((item) => item.status === 'done')).toBe(true);
  expect(statuses.slice(TIMELINE_STAGES.indexOf(stage) + 1).every((item) => item.status === 'pending')).toBe(true);
  if (state === 'interrupted') {
    expect(statuses.find((item) => item.stage === 'running').text).toContain('Interrupted');
  }
  if (['flagged', 'blocked', 'failed'].includes(state)) {
    expect(statuses.find((item) => item.stage === 'result').text).toContain(
      state === 'flagged' ? 'Completed with residue' : state[0].toUpperCase() + state.slice(1)
    );
  }
  await expect(page.locator('#bridge-flow button')).toHaveCount(0);
}

test('RunView timeline renders every typestate in order without action controls', async ({ page }, testInfo) => {
  await page.goto('/demo/l0');
  await expect(page.locator('#server-status')).toHaveText('Connected');

  const fixtures = await page.evaluate(async (states) => {
    const { projectRunView } = await import('/ui/run-view.mjs');
    const { renderRunTimeline } = await import('/ui/run-timeline.mjs');
    const container = document.querySelector('#bridge-flow');

    return states.map((state) => {
      const view = projectRunView({
        envelope: {
          schema_version: '2',
          envelope_id: `env-${state}`,
          run_id: `run-${state}`,
          state
        },
        approval: {
          approval_id: `approval-${state}`,
          state: state === 'awaiting_approval' ? 'pending' : 'authorized'
        },
        activeClaim: ['claimed', 'interrupted'].includes(state)
          ? { claim_id: `claim-${state}`, state }
          : null,
        result: state === 'flagged'
          ? { result_id: 'result-flagged', status: 'flagged', summary: 'Named residue remains.' }
          : null,
        receipts: state === 'passed'
          ? [{ receipt_id: 'receipt-passed', receipt_kind: 'skill.execution' }]
          : []
      });
      renderRunTimeline(container, view);
      return {
        state,
        stage: view.stage,
        current: container.querySelector('[data-status="active"]')?.dataset.stage || null,
        order: [...container.querySelectorAll('[data-stage]')].map((item) => item.dataset.stage),
        statuses: [...container.querySelectorAll('[data-stage]')].map((item) => item.dataset.status),
        text: container.textContent,
        controls: container.querySelectorAll('button').length
      };
    });
  }, RUN_STATES);

  expect(fixtures).toHaveLength(RUN_STATES.length);
  for (const fixture of fixtures) {
    expect(fixture.order).toEqual(TIMELINE_STAGES);
    expect(fixture.current).toBe(expectedCurrentStage(fixture.state));
    expect(fixture.controls).toBe(0);
  }
  expect(fixtures.find((fixture) => fixture.state === 'claimed').text).toContain('Running');
  expect(fixtures.find((fixture) => fixture.state === 'claimed').statuses[3]).toBe('active');
  expect(fixtures.find((fixture) => fixture.state === 'interrupted').text).toContain('Interrupted');
  expect(fixtures.find((fixture) => fixture.state === 'passed').current).toBe('receipt');
  expect(fixtures.find((fixture) => fixture.state === 'flagged').text).toContain('Completed with residue');

  const layout = await page.evaluate(() => ({
    horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
    timelineWidth: document.querySelector('#bridge-flow').getBoundingClientRect().width
  }));
  expect(layout.horizontalOverflow).toBe(false);
  expect(layout.timelineWidth).toBeGreaterThan(0);

  await mkdir(evidenceDir, { recursive: true });
  const screenshot = await page.screenshot({
    path: path.join(evidenceDir, `${testInfo.project.name}-timeline.png`),
    fullPage: true
  });
  expect(screenshot.byteLength).toBeGreaterThan(10_000);
});

test('real bridge request advances the visible timeline through Running', async ({ page, request }, testInfo) => {
  const task = `WUI-006 ${testInfo.project.name} ${Date.now()}`;
  await page.goto('/demo/l0');
  await expect(page.locator('#server-status')).toHaveText('Connected');
  await page.locator('[data-field="task-input"]').fill(task);
  await page.locator('[data-field="skill-input"]').fill('decision-gate');
  await page.locator('[data-action="prepare"]').click();

  const stateResponse = await request.get('/api/state');
  expect(stateResponse.ok()).toBeTruthy();
  const state = await stateResponse.json();
  const approval = state.approval_queue.find((candidate) => candidate.title === task);
  expect(approval).toBeTruthy();
  await page.locator(`[data-proposal-id="${approval.envelope_id}"]`).click();
  await expectTimelineState(page, 'prepared', 'awaiting_approval');

  const showEvidence = async () => {
    if (testInfo.project.name === 'mobile') {
      await page.locator('.mobile-view-nav [data-mobile-view="evidence"]').click();
    }
  };
  await showEvidence();

  page.once('dialog', (dialog) => dialog.accept());
  await page.locator('[data-action="approve"]').click();
  await expectTimelineState(page, 'approved', 'approved');

  await page.locator('[data-action="ready"]').click();
  await expectTimelineState(page, 'available', 'ready_for_poll');

  const claimResponse = await request.post(
    `/api/bridge/requests/${approval.envelope_id}/claim`,
    {
      data: {
        schema_version: '2',
        envelope_id: approval.envelope_id,
        agent_ref: 'openrouter.local-session',
        session_ref: `wui-006-${testInfo.project.name}`,
        assurance: 'unattested'
      }
    }
  );
  expect(claimResponse.status()).toBe(201);

  await page.reload();
  await expect(page.locator('#server-status')).toHaveText('Connected');
  await page.locator(`[data-proposal-id="${approval.envelope_id}"]`).click();
  await showEvidence();
  await expectTimelineState(page, 'running', 'claimed');
});
