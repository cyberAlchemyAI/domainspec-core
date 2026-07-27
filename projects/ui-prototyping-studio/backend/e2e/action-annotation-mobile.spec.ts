import { expect, test } from "@playwright/test";

import {
  cli,
  newDataDir,
  seedBaseline,
  seedStaged,
  startPreview,
} from "./helpers";

test("Accept and Revert require live actor-neutral acknowledgment context", async ({
  page,
  request,
}) => {
  const dataFile = newDataDir();
  const sid = seedStaged(dataFile);
  const preview = await startPreview(sid, dataFile);
  try {
    await page.goto(preview.url);
    const before = await (
      await request.get(`http://127.0.0.1:${preview.port}/state`)
    ).json();

    const missingAck = await request.post(
      `http://127.0.0.1:${preview.port}/accept`,
      { data: {} },
    );
    expect(missingAck.status()).toBe(428);
    expect((await missingAck.json()).error).toBe(
      "ACTION_ACKNOWLEDGMENT_REQUIRED",
    );
    expect(
      (
        await (
          await request.get(`http://127.0.0.1:${preview.port}/state`)
        ).json()
      ).head,
    ).toBe(before.head);

    const pending = page.locator('.action-context[data-action="accept"]');
    await expect(pending).toContainText("Candidate identity");
    await expect(pending).toContainText(before.stagedHash);
    await expect(pending).toContainText("Target state");
    await expect(pending).toContainText("RevisionRecorded");
    await expect(pending).toContainText("Diff recap");
    await expect(page.locator("#btn-accept")).toBeDisabled();
    await page.locator("#ack-accept").check();
    await expect(page.locator("#btn-accept")).toBeEnabled();
    await page.locator("#btn-accept").click();

    await expect(page.locator(".recorded")).toBeVisible();
    const accepted = await (
      await request.get(`http://127.0.0.1:${preview.port}/state`)
    ).json();
    const stale = await request.post(
      `http://127.0.0.1:${preview.port}/revert`,
      {
        data: {
          action: "revert",
          acknowledged: true,
          expectedIdentity: "rev-stale",
          expectedState: "RevisionRecorded",
        },
      },
    );
    expect(stale.status()).toBe(409);
    expect((await stale.json()).error).toBe("ACTION_CONTEXT_STALE");
    expect(
      (
        await (
          await request.get(`http://127.0.0.1:${preview.port}/state`)
        ).json()
      ).head,
    ).toBe(accepted.head);

    const revert = page.locator('.action-context[data-action="revert"]');
    await expect(revert).toContainText(accepted.head);
    await expect(revert).toContainText("RevisionRecorded");
    await expect(revert).toContainText("Diff recap");
    await expect(page.locator("#btn-revert")).toBeDisabled();
    await page.locator("#ack-revert").check();
    await page.locator("#btn-revert").click();
    await expect.poll(async () =>
      (
        await (
          await request.get(`http://127.0.0.1:${preview.port}/state`)
        ).json()
      ).head
    ).not.toBe(accepted.head);
    await expect(page.getByRole("button", { name: /export/i })).toHaveCount(0);
  } finally {
    preview.stop();
  }
});

test("annotation is unavailable without content and disabled until a real target", async ({
  page,
}) => {
  const emptyData = newDataDir();
  const opened = cli(["session", "open", "--variants", "1"], emptyData);
  const emptyPreview = await startPreview(opened.json.sessionId, emptyData);
  try {
    await page.goto(emptyPreview.url);
    await expect(page.locator(".annotate.unavailable")).toContainText(
      "Annotation unavailable",
    );
    await expect(page.locator("#cf")).toHaveCount(0);
  } finally {
    emptyPreview.stop();
  }

  const dataFile = newDataDir();
  const sid = seedBaseline(dataFile);
  const preview = await startPreview(sid, dataFile);
  try {
    await page.goto(preview.url);
    await expect(page.locator("#captured-count")).toHaveText("0");
    await expect(page.locator("#cf-od")).toHaveText("none selected");
    await expect(page.locator('#cf button[type="submit"]')).toBeDisabled();
    await expect(page.locator('#cf select[name="severity"] option')).toHaveText([
      "low",
      "medium",
      "high",
      "blocker",
    ]);

    await page
      .frameLocator("#annot")
      .locator('[data-od-id="cta.primary"]')
      .click();
    await expect(page.locator("#cf-od")).toHaveText("cta.primary");
    await expect(page.locator('#cf button[type="submit"]')).toBeEnabled();
    await page.locator('#cf input[name="intent"]').fill("reword");
    await page.locator('#cf input[name="note"]').fill("say Continue");
    await page.locator('#cf button[type="submit"]').click();
    await expect(page.locator("#cf-msg")).toContainText("captured");
    await expect(page.locator("#captured-count")).toHaveText("1");
  } finally {
    preview.stop();
  }
});

test("390px comparison stacks without horizontal document overflow", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const dataFile = newDataDir();
  const sid = seedStaged(dataFile);
  const preview = await startPreview(sid, dataFile);
  try {
    await page.goto(preview.url);
    const before = page.locator(".pending .two .card").nth(0);
    const after = page.locator(".pending .two .card").nth(1);
    await expect(before).toBeVisible();
    await expect(after).toBeVisible();
    const beforeBox = await before.boundingBox();
    const afterBox = await after.boundingBox();
    expect(beforeBox).not.toBeNull();
    expect(afterBox).not.toBeNull();
    expect(afterBox!.y).toBeGreaterThan(beforeBox!.y + beforeBox!.height - 1);
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    const actionContext = page.locator(
      '.action-context[data-action="accept"]',
    );
    await actionContext.scrollIntoViewIfNeeded();
    await expect(actionContext).toBeInViewport();
  } finally {
    preview.stop();
  }
});
