import {
  closeSync,
  existsSync,
  mkdirSync,
  openSync,
  readFileSync,
  renameSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { dirname } from "node:path";

import type { StagedCandidateRecord, StudioSessionStorePort } from "../application/ports.js";
import type {
  CommentEvent,
  DiffSummaryHonest,
  HandoffBundle,
  MutationBatch,
  MutationTask,
  PrototypeVariant,
  RevisionManifestEntry,
  StudioSession,
} from "../domain/models.js";

interface PersistentStoreDocument {
  counters: {
    session: number;
    comment: number;
    batch: number;
    revision: number;
  };
  sessions: Record<string, StudioSession>;
  variantsBySession: Record<string, PrototypeVariant[]>;
  commentsBySession: Record<string, CommentEvent[]>;
  batchesBySession: Record<string, MutationBatch[]>;
  revisionsBySession: Record<string, RevisionManifestEntry[]>;
  handoffBySession: Record<string, HandoffBundle>;
  stagedBySession: Record<string, StagedCandidateRecord>;
}

interface CreateFileBackedStudioSessionStoreOptions {
  filePath: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.StudioSessionStore
 *     type: Adapter
 */
export function createFileBackedStudioSessionStore(
  options: CreateFileBackedStudioSessionStoreOptions,
): StudioSessionStorePort {
  const filePath = options.filePath;
  // Preserve the constructor's fail-loud corrupt-file check.
  loadDocument(filePath);

  const readFresh = () => loadDocument(filePath);
  const mutate = <T>(
    mutation: (document: PersistentStoreDocument) => T,
  ): T => {
    return withDocumentLock(filePath, () => {
      const document = loadDocument(filePath);
      const result = mutation(document);
      writeDocument(filePath, document);
      return result;
    });
  };

  return {
    allocateSessionId() {
      return mutate((document) => {
        document.counters.session += 1;
        return `ups-session-${String(document.counters.session).padStart(4, "0")}`;
      });
    },
    allocateCommentId() {
      return mutate((document) => {
        document.counters.comment += 1;
        return `ups-comment-${String(document.counters.comment).padStart(5, "0")}`;
      });
    },
    allocateBatchId() {
      return mutate((document) => {
        document.counters.batch += 1;
        return `ups-batch-${String(document.counters.batch).padStart(5, "0")}`;
      });
    },
    allocateRevisionId(_parentRevisionId) {
      return mutate((document) => {
        document.counters.revision += 1;
        return `rev-${String(document.counters.revision).padStart(4, "0")}`;
      });
    },
    saveSession(session) {
      mutate((document) => {
        document.sessions[session.sessionId] = cloneSession(session);
      });
    },
    getSession(sessionId) {
      const session = readFresh().sessions[sessionId];
      return session ? cloneSession(session) : null;
    },
    saveVariants(sessionId, variants) {
      mutate((document) => {
        document.variantsBySession[sessionId] = variants.map((variant) =>
          cloneVariant(variant),
        );
      });
    },
    listVariants(sessionId) {
      const variants = readFresh().variantsBySession[sessionId] ?? [];
      return variants.map((variant) => cloneVariant(variant));
    },
    appendComment(comment) {
      mutate((document) => {
        const comments = document.commentsBySession[comment.sessionId] ?? [];
        comments.push(cloneComment(comment));
        document.commentsBySession[comment.sessionId] = comments;
      });
    },
    listComments(sessionId, revisionId) {
      const comments = readFresh().commentsBySession[sessionId] ?? [];
      return comments
        .filter((comment) => comment.revisionId === revisionId)
        .map((comment) => cloneComment(comment));
    },
    saveBatch(batch) {
      mutate((document) => {
        const batches = document.batchesBySession[batch.sessionId] ?? [];
        const nextBatches = batches.filter(
          (candidate) => candidate.batchId !== batch.batchId,
        );
        nextBatches.push(cloneBatch(batch));
        document.batchesBySession[batch.sessionId] = nextBatches;
      });
    },
    getBatch(sessionId, batchId) {
      const batches = readFresh().batchesBySession[sessionId] ?? [];
      const batch = batches.find((candidate) => candidate.batchId === batchId);
      return batch ? cloneBatch(batch) : null;
    },
    getDraftBatch(sessionId, batchId) {
      const batches = readFresh().batchesBySession[sessionId] ?? [];
      const candidates = batches.filter((batch) => batch.status === "draft");

      if (batchId) {
        const batch = candidates.find(
          (candidate) => candidate.batchId === batchId,
        );
        return batch ? cloneBatch(batch) : null;
      }

      const latest = candidates[candidates.length - 1];
      return latest ? cloneBatch(latest) : null;
    },
    listBatches(sessionId) {
      const batches = readFresh().batchesBySession[sessionId] ?? [];
      return batches.map((batch) => cloneBatch(batch));
    },
    appendRevision(entry) {
      mutate((document) => {
        const revisions = document.revisionsBySession[entry.sessionId] ?? [];
        revisions.push(cloneRevision(entry));
        document.revisionsBySession[entry.sessionId] = revisions;
      });
    },
    listRevisions(sessionId) {
      const revisions = readFresh().revisionsBySession[sessionId] ?? [];
      return revisions.map((entry) => cloneRevision(entry));
    },
    saveHandoffBundle(bundle) {
      mutate((document) => {
        document.handoffBySession[bundle.sessionId] =
          cloneHandoffBundle(bundle);
      });
    },
    getHandoffBundle(sessionId) {
      const bundle = readFresh().handoffBySession[sessionId];
      return bundle ? cloneHandoffBundle(bundle) : null;
    },
    saveStagedCandidate(sessionId, record) {
      mutate((document) => {
        document.stagedBySession[sessionId] = { ...record };
      });
    },
    getStagedCandidate(sessionId) {
      const record = readFresh().stagedBySession[sessionId];
      return record ? { ...record } : null;
    },
    clearStagedCandidate(sessionId) {
      mutate((document) => {
        delete document.stagedBySession[sessionId];
      });
    },
  };
}

function withDocumentLock<T>(filePath: string, operation: () => T): T {
  mkdirSync(dirname(filePath), { recursive: true });
  const lockPath = `${filePath}.lock`;
  let lockDescriptor: number;
  try {
    lockDescriptor = openSync(lockPath, "wx");
  } catch (cause) {
    if ((cause as NodeJS.ErrnoException).code === "EEXIST") {
      throw new Error(
        `Studio data file is locked by another writer: ${filePath}. Refusing to overwrite concurrent state.`,
      );
    }
    throw cause;
  }

  try {
    return operation();
  } finally {
    closeSync(lockDescriptor);
    unlinkSync(lockPath);
  }
}

function loadDocument(filePath: string): PersistentStoreDocument {
  if (!existsSync(filePath)) {
    return createEmptyDocument();
  }

  // N10 (F12): only an ABSENT file means "fresh start". A present-but-unparseable file must NOT be silently
  // reset to empty (that is silent data-loss) — fail loud so the operator can back it up / investigate.
  const raw = readFileSync(filePath, "utf8");
  let parsed: Partial<PersistentStoreDocument>;
  try {
    parsed = JSON.parse(raw) as Partial<PersistentStoreDocument>;
  } catch (cause) {
    throw new Error(
      `Studio data file is present but not valid JSON: ${filePath}. Refusing to silently reset (data-loss guard) — back it up or remove it to start fresh. Cause: ${String(cause)}`,
    );
  }
  return normalizeDocument(parsed);
}

function writeDocument(
  filePath: string,
  documentState: PersistentStoreDocument,
): void {
  mkdirSync(dirname(filePath), { recursive: true });
  const tempPath = `${filePath}.tmp`;
  writeFileSync(tempPath, JSON.stringify(documentState, null, 2), "utf8");
  renameSync(tempPath, filePath);
}

function createEmptyDocument(): PersistentStoreDocument {
  return {
    counters: {
      session: 0,
      comment: 0,
      batch: 0,
      revision: 0,
    },
    sessions: {},
    variantsBySession: {},
    commentsBySession: {},
    batchesBySession: {},
    revisionsBySession: {},
    handoffBySession: {},
    stagedBySession: {},
  };
}

function normalizeDocument(
  parsed: Partial<PersistentStoreDocument>,
): PersistentStoreDocument {
  const fallback = createEmptyDocument();
  return {
    counters: {
      session: asNumber(parsed.counters?.session),
      comment: asNumber(parsed.counters?.comment),
      batch: asNumber(parsed.counters?.batch),
      revision: asNumber(parsed.counters?.revision),
    },
    sessions: asRecord(parsed.sessions, fallback.sessions),
    variantsBySession: asRecord(
      parsed.variantsBySession,
      fallback.variantsBySession,
    ),
    commentsBySession: asRecord(
      parsed.commentsBySession,
      fallback.commentsBySession,
    ),
    batchesBySession: asRecord(
      parsed.batchesBySession,
      fallback.batchesBySession,
    ),
    revisionsBySession: asRecord(
      parsed.revisionsBySession,
      fallback.revisionsBySession,
    ),
    handoffBySession: asRecord(
      parsed.handoffBySession,
      fallback.handoffBySession,
    ),
    stagedBySession: asRecord(
      parsed.stagedBySession,
      fallback.stagedBySession,
    ),
  };
}

function asNumber(value: unknown): number {
  return typeof value === "number" && Number.isInteger(value) && value >= 0
    ? value
    : 0;
}

function asRecord<T>(
  value: unknown,
  fallback: Record<string, T>,
): Record<string, T> {
  if (!value || typeof value !== "object") {
    return fallback;
  }
  return value as Record<string, T>;
}

function cloneSession(session: StudioSession): StudioSession {
  return {
    ...session,
    variantLabels: [...session.variantLabels],
    baseline: session.baseline ? { ...session.baseline } : null,
    integration: {
      ...session.integration,
    },
  };
}

function cloneVariant(variant: PrototypeVariant): PrototypeVariant {
  return {
    ...variant,
    componentsUsed: [...variant.componentsUsed],
  };
}

function cloneComment(comment: CommentEvent): CommentEvent {
  return {
    ...comment,
    target: {
      ...comment.target,
    },
  };
}

function cloneTask(task: MutationTask): MutationTask {
  return {
    ...task,
  };
}

function cloneBatch(batch: MutationBatch): MutationBatch {
  return {
    ...batch,
    generatedFromCommentIds: [...batch.generatedFromCommentIds],
    tasks: batch.tasks.map((task) => cloneTask(task)),
    approval: {
      ...batch.approval,
    },
  };
}

function cloneRevision(entry: RevisionManifestEntry): RevisionManifestEntry {
  return {
    ...entry,
    baseline: {
      ...entry.baseline,
    },
    appliedTaskIds: [...entry.appliedTaskIds],
    unresolvedCommentIds: [...entry.unresolvedCommentIds],
    diffSummary: {
      ...entry.diffSummary,
    },
    diffSummaryHonest: cloneDiffSummaryHonest(entry.diffSummaryHonest),
  };
}

function cloneHandoffBundle(bundle: HandoffBundle): HandoffBundle {
  return {
    ...bundle,
    baseline: {
      ...bundle.baseline,
    },
    storyRefs: [...bundle.storyRefs],
    requirementRefs: [...bundle.requirementRefs],
    acceptanceRefs: [...bundle.acceptanceRefs],
    sourceRefs: bundle.sourceRefs ? [...bundle.sourceRefs] : undefined,
    missingRefs: bundle.missingRefs ? [...bundle.missingRefs] : undefined,
    diffSummaryHonest: cloneDiffSummaryHonest(bundle.diffSummaryHonest),
  };
}

function cloneDiffSummaryHonest(
  diff: DiffSummaryHonest | undefined,
): DiffSummaryHonest | undefined {
  return diff
    ? {
        ...diff,
        fragments: diff.fragments.map((fragment) => ({ ...fragment })),
        style: { ...diff.style },
        unattributed: { ...diff.unattributed },
      }
    : undefined;
}
