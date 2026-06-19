import { existsSync } from "node:fs";
import { join } from "node:path";

import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import type { HandoffBundle, StudioSession } from "../domain/models.js";

const STORY_REF = "docs/features/ui-prototyping-studio/STORIES.md";
const SPEC_REQUIREMENT_REF =
  "docs/features/ui-prototyping-studio/SPEC.md#functional-requirements-mvp";
const SPEC_ACCEPTANCE_REF =
  "docs/features/ui-prototyping-studio/SPEC.md#acceptance-criteria-mvp";
const UI_SPEC_REF = "docs/features/ui-prototyping-studio/UI-SPEC.md";
const TEST_SPEC_REF = "docs/features/ui-prototyping-studio/TEST-SPEC.md";

export interface ExportDesignHandoffInput {
  sessionId: string;
  exportProfile?: string;
  requestedBy: string;
  /**
   * N1 — export is the one IRREVERSIBLE edge (downstream consumption). The human confirmation lives HERE,
   * in the core use-case, so EVERY adapter (CLI, HTTP) inherits it — not only the CLI (closes F1, restores
   * ARCHITECTURE §4 "gates live in the core, never in the adapter"). Must be a non-empty confirming actor.
   */
  confirmedBy?: string;
}

export interface ExportDesignHandoffResult {
  session: StudioSession;
  bundle: HandoffBundle;
}

interface ExportDesignHandoffOptions {
  featureDocsRootDir: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.ExportDesignHandoff
 *     type: Operation
 */
export function makeExportDesignHandoffUseCase(
  store: StudioSessionStorePort,
  options: ExportDesignHandoffOptions,
) {
  return function exportDesignHandoff(
    input: ExportDesignHandoffInput,
  ): ExportDesignHandoffResult {
    // N1 (gate-in-core): the irreversible edge requires an explicit human confirmation. Enforced here so no
    // adapter can reach export unconfirmed (the HTTP route previously bypassed the CLI-only `--confirm`).
    if (!input.confirmedBy || input.confirmedBy.trim().length === 0) {
      throw createUiPrototypingStudioError(
        "HANDOFF_CONFIRMATION_REQUIRED",
        "Export is the one irreversible edge — an explicit human confirmation is required",
        { sessionId: input.sessionId },
      );
    }
    const session = store.getSession(input.sessionId);
    if (!session) {
      throw createUiPrototypingStudioError(
        "SESSION_NOT_FOUND",
        "Session not found",
        {
          sessionId: input.sessionId,
        },
      );
    }

    const revisions = store.listRevisions(session.sessionId);
    if (revisions.length === 0 || !session.revisionHeadId) {
      throw createUiPrototypingStudioError(
        "HANDOFF_REVISION_REQUIRED",
        "Handoff export requires at least one revision manifest entry",
        {
          sessionId: session.sessionId,
          revisionCount: revisions.length,
          revisionHeadId: session.revisionHeadId,
        },
      );
    }

    if (!session.baseline) {
      throw createUiPrototypingStudioError(
        "HANDOFF_REFERENCE_INCOMPLETE",
        "Handoff export requires baseline provenance",
        {
          sessionId: session.sessionId,
        },
      );
    }

    // GAP-009 (G2): feature-doc refs are ADVISORY, not gating. The lean standalone project
    // consolidated STORIES/UI-SPEC/TEST-SPEC into SPEC.md + aspect docs, so a hard existsSync
    // gate blocked handoff in the lean setup. The real anchors (a recorded revision + baseline
    // provenance, checked above) gate the export; the doc refs are pointers a consumer resolves.
    // `missingRefs` is recorded on the bundle for honesty.
    const advisoryFiles = ["SPEC.md", "STORIES.md", "UI-SPEC.md", "TEST-SPEC.md"];
    const missingRefs = advisoryFiles.filter(
      (fileName) => !existsSync(join(options.featureDocsRootDir, fileName)),
    );

    const bundle: HandoffBundle = {
      sessionId: session.sessionId,
      revisionHeadId: session.revisionHeadId,
      baseline: session.baseline,
      variantCount: session.variantCount,
      storyRefs: [STORY_REF],
      requirementRefs: [SPEC_REQUIREMENT_REF],
      acceptanceRefs: [SPEC_ACCEPTANCE_REF],
      uiSpecRef: UI_SPEC_REF,
      testSpecRef: TEST_SPEC_REF,
      missingRefs,
    };

    const nextSession: StudioSession = {
      ...session,
      integration: {
        uiPhaseBridgeReady: true,
        generateTestsUiReady: true,
        uiImplementReady: true,
      },
      state: "RevisionRecorded",
    };

    store.saveSession(nextSession);
    store.saveHandoffBundle(bundle);

    return {
      session: nextSession,
      bundle,
    };
  };
}
