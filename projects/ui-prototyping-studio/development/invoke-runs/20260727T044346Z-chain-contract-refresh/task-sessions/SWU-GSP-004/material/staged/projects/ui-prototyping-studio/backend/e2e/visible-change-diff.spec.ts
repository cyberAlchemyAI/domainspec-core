import { expect, test } from "@playwright/test";

import { cli, newDataDir, seedBaseline, startPreview } from "./helpers";

test("CSS-only mutation remains visible through preview, state, revision, and handoff", async ({
  page,
  request,
}) => {
  const dataFile = newDataDir();
  const sid = seedBaseline(dataFile);
  const comment = cli([
    "comment",
    "add",
    sid,
    "--od-id",
    "cta.primary",
    "--selector",
    "[data-od-id=cta.primary]",
    "--label",
    "Primary button",
    "--intent",
    "restyle",
    "--note",
    "make the primary action visually distinct",
  ], dataFile);
  expect(comment.code).toBe(0);
  const synthesis = cli(["synthesize", sid], dataFile);
  expect(synthesis.code).toBe(0);
  const batchId = synthesis.json.batch.batchId as string;
  expect(cli(["batch", "approve", sid, batchId], dataFile).code).toBe(0);
  expect(cli([
    "apply",
    sid,
    batchId,
    "--candidate-from",
    "e2e/fixtures/style-only.html",
  ], dataFile).code).toBe(0);

  const preview = await startPreview(sid, dataFile);
  try {
    await page.goto(preview.url);
    const pending = page.locator(".pending");
    await expect(pending).toContainText(
      "Per-component structural diff: +0 added · ~0 changed · -0 removed",
    );
    await expect(pending).toContainText("Style/global evidence");
    await expect(pending).toContainText("global-unattributed");
    await expect(pending).toContainText("Visible change evidence: 1");

    const state = await (
      await request.get(`http://127.0.0.1:${preview.port}/state`)
    ).json();
    expect(state.projection.structuralDiff.added).toBe(0);
    expect(state.projection.structuralDiff.changed).toBe(0);
    expect(state.projection.structuralDiff.removed).toBe(0);
    expect(state.projection.structuralDiff.style.changed).toBe(true);
    expect(state.projection.structuralDiff.style.attribution).toBe(
      "global-unattributed",
    );
    expect(state.projection.structuralDiff.visibleChangeCount).toBe(1);
  } finally {
    preview.stop();
  }

  expect(cli(["accept", sid], dataFile).code).toBe(0);
  const revisions = cli(["revisions", sid], dataFile);
  expect(revisions.code).toBe(0);
  expect(revisions.json.at(-1).diffSummaryHonest.style.changed).toBe(true);

  const handoff = cli(
    ["handoff", "export", sid, "--confirm"],
    dataFile,
  );
  expect(handoff.code).toBe(0);
  expect(handoff.json.bundle.diffSummaryHonest.style.changed).toBe(true);
  expect(handoff.json.bundle.diffSummaryHonest.visibleChangeCount).toBe(1);
});
