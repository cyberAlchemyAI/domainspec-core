import { expect, test } from "@playwright/test";

import { cli, newDataDir, seedStaged, startPreview } from "./helpers";

const CTA = '[data-od-id="cta.primary"]';

test("current preview and annotation share the Accept/Revert head identity", async ({
  page,
  request,
}) => {
  const dataFile = newDataDir();
  const sid = seedStaged(dataFile);
  const preview = await startPreview(sid, dataFile);
  try {
    await page.goto(preview.url);

    await expect(page.locator("#current-head figcaption")).toContainText(
      "current head",
    );
    await expect(
      page.frameLocator("#current-head iframe").locator(CTA),
    ).toHaveText("Go");
    await expect(page.frameLocator("#annot").locator(CTA)).toHaveText("Go");
    const before = await (
      await request.get(`http://127.0.0.1:${preview.port}/state`)
    ).json();
    expect(before.projection.currentHead.revisionId).toBe("rev-0000");
    expect(before.projection.annotation.revisionId).toBe("rev-0000");
    expect(before.projection.historicalVariants[0].relationship).toBe(
      "baseline-lineage",
    );

    await page.getByRole("button", { name: /accept/i }).click();
    await expect(
      page.frameLocator("#current-head iframe").locator(CTA),
    ).toHaveText("Continue");
    await expect(page.frameLocator("#annot").locator(CTA)).toHaveText(
      "Continue",
    );
    const accepted = await (
      await request.get(`http://127.0.0.1:${preview.port}/state`)
    ).json();
    expect(accepted.projection.currentHead.source).toBe("revision");
    expect(accepted.projection.annotation.revisionId).toBe(
      accepted.projection.currentHead.revisionId,
    );

    await page.getByRole("button", { name: /revert/i }).click();
    await expect(
      page.frameLocator("#current-head iframe").locator(CTA),
    ).toHaveText("Go");
    await expect(page.frameLocator("#annot").locator(CTA)).toHaveText("Go");
    const reverted = await (
      await request.get(`http://127.0.0.1:${preview.port}/state`)
    ).json();
    expect(reverted.projection.annotation.revisionId).toBe(
      reverted.projection.currentHead.revisionId,
    );
    expect(reverted.projection.currentHead.revisionId).not.toBe(
      accepted.projection.currentHead.revisionId,
    );
  } finally {
    preview.stop();
  }
});

test("an already-running preview projects an external Accept without restart", async ({
  page,
  request,
}) => {
  const dataFile = newDataDir();
  const sid = seedStaged(dataFile);
  const preview = await startPreview(sid, dataFile);
  try {
    await page.goto(preview.url);
    await expect(
      page.frameLocator("#current-head iframe").locator(CTA),
    ).toHaveText("Go");

    const accepted = cli(["accept", sid], dataFile);
    expect(accepted.code).toBe(0);

    await expect(
      page.frameLocator("#current-head iframe").locator(CTA),
    ).toHaveText("Continue");
    await expect(page.frameLocator("#annot").locator(CTA)).toHaveText(
      "Continue",
    );
    const state = await (
      await request.get(`http://127.0.0.1:${preview.port}/state`)
    ).json();
    expect(state.projection.currentHead.source).toBe("revision");
    expect(state.projection.annotation.revisionId).toBe(
      state.projection.currentHead.revisionId,
    );
  } finally {
    preview.stop();
  }
});
