import { diffByOdId } from "./admission.js";
import type { ArtifactContentPort } from "./artifact-content-port.js";
import { resolveCurrentHtml } from "./current-html.js";
import type {
  StagedCandidateRecord,
  StudioSessionStorePort,
} from "./ports.js";
import type {
  DiffSummaryHonest,
  PrototypeVariantStatus,
  StudioSession,
  VariantLabel,
} from "../domain/models.js";

export interface GovernedCurrentHeadProjection {
  available: boolean;
  source: "revision" | "baseline" | "unavailable";
  sourceRef: string | null;
  html: string | null;
  route: "/raw/current";
  revisionId: string;
  label: string;
}

export interface GovernedAnnotationProjection {
  available: boolean;
  route: "/annotate/current" | null;
  revisionId: string;
  capturedCommentCount: number;
}

export interface GovernedHistoricalVariantProjection {
  variantLabel: VariantLabel;
  status: PrototypeVariantStatus;
  relationship: "baseline-lineage" | "historical-variant";
  route: string;
}

export interface GovernedStagedProjection {
  available: boolean;
  route: "/raw/staged" | null;
  candidateHtmlHash: string | null;
  batchId: string | null;
  contentResolved: boolean;
}

export interface GovernedStateProjection {
  sessionId: string;
  state: StudioSession["state"];
  revisionHeadId: string;
  currentHead: GovernedCurrentHeadProjection;
  annotation: GovernedAnnotationProjection;
  historicalVariants: GovernedHistoricalVariantProjection[];
  staged: GovernedStagedProjection;
  structuralDiff: DiffSummaryHonest | null;
  actions: {
    acceptAvailable: boolean;
    discardAvailable: boolean;
    revertAvailable: boolean;
    commentAvailable: boolean;
  };
  evidence: {
    currentHeadResolved: boolean;
    annotationBoundToCurrentHead: boolean;
    stagedContentResolved: boolean;
    revisionCount: number;
    handoffBundlePresent: boolean;
  };
}

interface BuildGovernedStateProjectionInput {
  session: StudioSession;
  store: StudioSessionStorePort;
  artifact: ArtifactContentPort;
}

export function buildGovernedStateProjection(
  input: BuildGovernedStateProjectionInput,
): GovernedStateProjection {
  const { session, store, artifact } = input;
  const revisionId = session.revisionHeadId ?? "rev-0000";
  const revisions = store.listRevisions(session.sessionId);
  const headRevision = revisions.find(
    (entry) => entry.revisionId === session.revisionHeadId,
  );
  const variants = store.listVariants(session.sessionId);
  const baselineVariant = session.baseline
    ? variants.find(
        (variant) => variant.variantLabel === session.baseline!.label,
      )
    : undefined;
  const currentHtml = resolveCurrentHtml(session, store, artifact);
  const sourceRef = headRevision?.candidateHtmlHash
    ? `artifact:${headRevision.candidateHtmlHash}`
    : baselineVariant?.htmlArtifactRef ?? null;
  const source = headRevision?.candidateHtmlHash
    ? "revision"
    : baselineVariant
      ? "baseline"
      : "unavailable";
  const stagedRecord = store.getStagedCandidate(session.sessionId);
  const stagedHtml = readStagedHtml(stagedRecord, artifact);
  const capturedCommentCount = store.listComments(
    session.sessionId,
    revisionId,
  ).length;

  return {
    sessionId: session.sessionId,
    state: session.state,
    revisionHeadId: revisionId,
    currentHead: {
      available: currentHtml !== null,
      source,
      sourceRef,
      html: currentHtml,
      route: "/raw/current",
      revisionId,
      label: currentHeadLabel(session, source, revisionId),
    },
    annotation: {
      available: currentHtml !== null,
      route: currentHtml === null ? null : "/annotate/current",
      revisionId,
      capturedCommentCount,
    },
    historicalVariants: variants.map((variant) => ({
      variantLabel: variant.variantLabel,
      status: variant.status,
      relationship: session.baseline?.label === variant.variantLabel
        ? "baseline-lineage"
        : "historical-variant",
      route: `/raw/variant/${variant.variantLabel}`,
    })),
    staged: {
      available: stagedRecord !== null,
      route: stagedRecord === null ? null : "/raw/staged",
      candidateHtmlHash: stagedRecord?.candidateHtmlHash ?? null,
      batchId: stagedRecord?.batchId ?? null,
      contentResolved: stagedHtml !== null,
    },
    structuralDiff: currentHtml !== null && stagedHtml !== null
      ? diffByOdId(currentHtml, stagedHtml)
      : null,
    actions: {
      acceptAvailable: stagedRecord !== null,
      discardAvailable: stagedRecord !== null,
      revertAvailable: stagedRecord === null && revisions.length > 0,
      commentAvailable: currentHtml !== null,
    },
    evidence: {
      currentHeadResolved: currentHtml !== null,
      annotationBoundToCurrentHead: currentHtml !== null,
      stagedContentResolved: stagedRecord === null || stagedHtml !== null,
      revisionCount: revisions.length,
      handoffBundlePresent:
        store.getHandoffBundle(session.sessionId) !== null,
    },
  };
}

function readStagedHtml(
  record: StagedCandidateRecord | null,
  artifact: ArtifactContentPort,
): string | null {
  return record ? artifact.readHtml(record.stagedRef) : null;
}

function currentHeadLabel(
  session: StudioSession,
  source: GovernedCurrentHeadProjection["source"],
  revisionId: string,
): string {
  if (source === "revision") {
    return `current head · ${revisionId}`;
  }
  if (source === "baseline" && session.baseline) {
    return `current head · ${revisionId} · baseline ${session.baseline.label}`;
  }
  return `current head unavailable · ${revisionId}`;
}
