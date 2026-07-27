import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { createFileArtifactContentStore } from "../infrastructure/file-artifact-content-store.js";
import { createFileBackedStudioSessionStore } from "../infrastructure/file-studio-session-store.js";
import { buildGovernedStateProjection } from "./governed-state-projection.js";
import { createStudioOrchestrationModule } from "./studio-orchestration-module.js";

const BASE = `<div data-od-id="card.root"><button data-od-id="cta.primary">Go</button><h2 data-od-id="card.title">T</h2></div>`;
const CANDIDATE = BASE.replace(">Go<", ">Continue<");

function withStudio(
  run: (
    studio: ReturnType<typeof createStudioOrchestrationModule>,
    store: ReturnType<typeof createFileBackedStudioSessionStore>,
    artifact: ReturnType<typeof createFileArtifactContentStore>,
  ) => void,
): void {
  const root = mkdtempSync(join(tmpdir(), "ups-projection-"));
  try {
    const store = createFileBackedStudioSessionStore({
      filePath: join(root, "studio.json"),
    });
    const artifact = createFileArtifactContentStore({
      rootDir: join(root, "artifacts"),
    });
    const studio = createStudioOrchestrationModule(store, {
      featureDocsRootDir: root,
      artifactContentStore: artifact,
    });
    run(studio, store, artifact);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

function prepareStaged(
  studio: ReturnType<typeof createStudioOrchestrationModule>,
): string {
  const session = studio.initializeSession({
    requestedVariantCount: 1,
    requestedBy: "test",
  });
  studio.submitPrompt({
    sessionId: session.sessionId,
    prompt: "reword cta",
    submittedBy: "test",
  });
  studio.registerVariants({
    sessionId: session.sessionId,
    variants: [{ label: "A", html: BASE }],
    requestedBy: "test",
  });
  studio.captureCommentEvent({
    sessionId: session.sessionId,
    revisionId: "rev-0000",
    target: {
      selector: "[data-od-id=cta.primary]",
      elementLabel: "Primary button",
      odId: "cta.primary",
    },
    severity: "medium",
    intent: "reword",
    note: "say Continue",
    createdBy: "test",
  });
  const synthesis = studio.synthesizeMutationBatch({
    sessionId: session.sessionId,
    sourceRevisionId: "rev-0000",
    requestedBy: "test",
  });
  studio.approveMutationBatch({
    sessionId: session.sessionId,
    batchId: synthesis.batch.batchId,
    approvedBy: "test",
    approvedAt: "2026-07-27T00:00:00Z",
  });
  studio.applyAndStage({
    sessionId: session.sessionId,
    batchId: synthesis.batch.batchId,
    candidateHtml: CANDIDATE,
    requestedBy: "human:test",
  });
  return session.sessionId;
}

test("projection distinguishes current head from historical variants", () => {
  withStudio((studio, store, artifact) => {
    const sid = prepareStaged(studio);
    const projection = buildGovernedStateProjection({
      session: studio.getSessionSnapshot({ sessionId: sid }),
      store,
      artifact,
    });

    assert.equal(projection.currentHead.source, "baseline");
    assert.match(projection.currentHead.html!, />Go</);
    assert.equal(projection.currentHead.route, "/raw/current");
    assert.equal(projection.annotation.revisionId, "rev-0000");
    assert.equal(projection.annotation.route, "/annotate/current");
    assert.equal(
      projection.historicalVariants[0]?.relationship,
      "baseline-lineage",
    );
    assert.equal(projection.staged.available, true);
    assert.ok(projection.structuralDiff?.changed);
    assert.equal(projection.actions.acceptAvailable, true);
  });
});

test("Accept and Revert move preview and annotation through one revision identity", () => {
  withStudio((studio, store, artifact) => {
    const sid = prepareStaged(studio);
    const accepted = studio.acceptStagedRevision({
      sessionId: sid,
      acceptedAt: "2026-07-27T00:01:00Z",
      requestedBy: "human:test",
    });
    const acceptedProjection = buildGovernedStateProjection({
      session: accepted.session,
      store,
      artifact,
    });
    assert.equal(acceptedProjection.currentHead.source, "revision");
    assert.match(acceptedProjection.currentHead.html!, />Continue</);
    assert.equal(
      acceptedProjection.annotation.revisionId,
      acceptedProjection.currentHead.revisionId,
    );

    const reverted = studio.revertRevision({
      sessionId: sid,
      requestedBy: "human:test",
      revertedAt: "2026-07-27T00:02:00Z",
    });
    const revertedProjection = buildGovernedStateProjection({
      session: reverted.session,
      store,
      artifact,
    });
    assert.match(revertedProjection.currentHead.html!, />Go</);
    assert.doesNotMatch(revertedProjection.currentHead.html!, />Continue</);
    assert.notEqual(
      revertedProjection.currentHead.revisionId,
      acceptedProjection.currentHead.revisionId,
    );
    assert.equal(
      revertedProjection.annotation.revisionId,
      revertedProjection.currentHead.revisionId,
    );
  });
});

test("unresolvable content is explicit and disables annotation", () => {
  withStudio((studio, store, artifact) => {
    const session = studio.initializeSession({
      requestedVariantCount: 1,
      requestedBy: "test",
    });
    const projection = buildGovernedStateProjection({
      session,
      store,
      artifact,
    });
    assert.equal(projection.currentHead.available, false);
    assert.equal(projection.currentHead.source, "unavailable");
    assert.equal(projection.currentHead.html, null);
    assert.equal(projection.annotation.available, false);
    assert.equal(projection.annotation.route, null);
  });
});
