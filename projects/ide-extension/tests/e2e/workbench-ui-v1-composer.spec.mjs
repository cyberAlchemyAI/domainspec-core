import { expect, test } from '@playwright/test';

async function stateFrom(request) {
  const response = await request.get('/api/state');
  expect(response.ok()).toBeTruthy();
  return response.json();
}

async function envelopeForTask(request, task) {
  const state = await stateFrom(request);
  const approval = state.approval_queue.find((candidate) => candidate.title === task);
  expect(approval).toBeTruthy();
  return state.envelopes[approval.envelope_id];
}

test('explicit composer modes preserve input and emit distinct payloads', async ({ page, request }, testInfo) => {
  await page.goto('/demo/l0');
  await expect(page.locator('#server-status')).toHaveText('Connected');

  const agentMode = page.locator('[data-request-mode="agent-task"]');
  const dryRunMode = page.locator('[data-request-mode="dry-run"]');
  const taskInput = page.locator('[data-field="task-input"]');
  const skillInput = page.locator('[data-field="skill-input"]');

  await expect(agentMode).toHaveAttribute('aria-checked', 'true');
  await expect(dryRunMode).toHaveAttribute('aria-checked', 'false');
  await expect(skillInput).toBeVisible();
  expect(await skillInput.getAttribute('required')).not.toBeNull();

  const preservedTask = `Agent task keeps its Task when Skill is missing (${testInfo.project.name})`;
  await taskInput.fill(preservedTask);
  await page.locator('[data-action="prepare"]').click();
  await expect(page.locator('#skill-error')).toBeVisible();
  await expect(taskInput).toHaveValue(preservedTask);
  await expect(page.locator('[data-proposal-id]').filter({ hasText: preservedTask })).toHaveCount(0);

  await skillInput.fill('decision-gate');
  await page.locator('[data-action="prepare"]').click();
  await expect(page.locator('[data-proposal-id]').filter({ hasText: preservedTask })).toBeVisible();
  const agentEnvelope = await envelopeForTask(request, preservedTask);
  expect(agentEnvelope.agent_ref).toBe('codex.current-session');
  expect(agentEnvelope.requested_skill).toBe('decision-gate');
  expect(agentEnvelope.requested_grants).toContain('skill.invoke');

  await agentMode.click();
  await skillInput.fill('decision-gate');
  await dryRunMode.click();
  await expect(dryRunMode).toHaveAttribute('aria-checked', 'true');
  await expect(agentMode).toHaveAttribute('aria-checked', 'false');
  await expect(skillInput).toBeHidden();
  expect(await skillInput.getAttribute('required')).toBeNull();

  const dryRunTask = `Dry run stays explicit even when Skill had a value (${testInfo.project.name})`;
  await taskInput.fill(dryRunTask);
  await page.locator('[data-action="prepare"]').click();
  await expect(page.locator('[data-proposal-id]').filter({ hasText: dryRunTask })).toBeVisible();
  const dryRunEnvelope = await envelopeForTask(request, dryRunTask);
  expect(dryRunEnvelope.agent_ref).toBe('local.noop-agent');
  expect(dryRunEnvelope.requested_skill).toBeNull();
  expect(dryRunEnvelope.requested_grants).not.toContain('skill.invoke');
});
