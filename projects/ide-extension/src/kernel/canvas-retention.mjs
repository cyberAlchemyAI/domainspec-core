import { createHash, randomUUID } from 'node:crypto';
import {
  OPERATIONS_V1_EVENT_VERSION,
  OPERATIONS_V1_LIMITS
} from './operations-contracts.mjs';

export const RETENTION_COMMAND_LIMIT = 128;

export const DEFAULT_RETENTION_POLICY = Object.freeze({
  soft_bytes: OPERATIONS_V1_LIMITS.retention_soft_bytes,
  hard_bytes: OPERATIONS_V1_LIMITS.retention_hard_bytes,
  grace_ms: OPERATIONS_V1_LIMITS.retention_grace_ms,
  reclaim_below_bytes: OPERATIONS_V1_LIMITS.retention_reclaim_below_bytes
});

function retentionError(code, message, fields = {}) {
  const error = new Error(message);
  error.code = code;
  Object.assign(error, fields);
  return error;
}

function assertPositiveSafeInteger(value, name) {
  if (!Number.isSafeInteger(value) || value <= 0) {
    throw retentionError('retention_policy_invalid', `${name} must be a positive safe integer`, {
      field: name
    });
  }
  return value;
}

export function createRetentionPolicy(overrides = {}) {
  const policy = {
    soft_bytes: overrides.soft_bytes ?? DEFAULT_RETENTION_POLICY.soft_bytes,
    hard_bytes: overrides.hard_bytes ?? DEFAULT_RETENTION_POLICY.hard_bytes,
    grace_ms: overrides.grace_ms ?? DEFAULT_RETENTION_POLICY.grace_ms,
    reclaim_below_bytes: overrides.reclaim_below_bytes
      ?? DEFAULT_RETENTION_POLICY.reclaim_below_bytes
  };
  assertPositiveSafeInteger(policy.soft_bytes, 'soft_bytes');
  assertPositiveSafeInteger(policy.hard_bytes, 'hard_bytes');
  assertPositiveSafeInteger(policy.grace_ms, 'grace_ms');
  assertPositiveSafeInteger(policy.reclaim_below_bytes, 'reclaim_below_bytes');
  if (policy.hard_bytes <= policy.soft_bytes) {
    throw retentionError('retention_policy_invalid', 'hard_bytes must be greater than soft_bytes', {
      field: 'hard_bytes'
    });
  }
  if (policy.reclaim_below_bytes > policy.soft_bytes) {
    throw retentionError(
      'retention_policy_invalid',
      'reclaim_below_bytes must not exceed soft_bytes',
      { field: 'reclaim_below_bytes' }
    );
  }
  return Object.freeze(policy);
}

function operationsState(projection) {
  return projection.canvas?.operations_v1 || null;
}

function unprunedRevisions(operations) {
  if (!operations) return [];
  return Object.values(operations.revisions)
    .filter((revision) => !operations.prune_tombstones[revision.revision_id]);
}

function protectedRevisionIds(operations) {
  const protectedIds = new Set(
    Object.values(operations?.surfaces || {}).map((surface) => surface.current_revision_id)
  );
  if (operations?.display_target?.surface_kind === 'operations_v1') {
    protectedIds.add(operations.display_target.revision_id);
  }
  return protectedIds;
}

function compareRevisions(left, right) {
  const timestampOrder = left.committed_at.localeCompare(right.committed_at);
  return timestampOrder || left.revision_id.localeCompare(right.revision_id);
}

function blobMaps(diagnostics) {
  const blobs = diagnostics?.blobs || [];
  return {
    sizes: new Map(blobs.map((blob) => [blob.sha256, blob.byte_length])),
    referenced: blobs.filter((blob) => blob.referenced),
    orphaned: blobs.filter((blob) => !blob.referenced)
  };
}

function temporaryBytes(diagnostics) {
  if (Number.isSafeInteger(diagnostics?.temporary_bytes)) {
    return diagnostics.temporary_bytes;
  }
  return (diagnostics?.temporary_files || []).reduce(
    (total, entry) => total + (Number.isSafeInteger(entry.byte_length) ? entry.byte_length : 0),
    0
  );
}

function physicalTotalBytes(diagnostics) {
  if (Number.isSafeInteger(diagnostics?.physical_total_bytes)) {
    return diagnostics.physical_total_bytes;
  }
  return (diagnostics?.total_bytes || 0) + temporaryBytes(diagnostics);
}

function candidateDigest(eventCursor, policy, activeRequest, revisionIds) {
  return createHash('sha256').update(JSON.stringify({
    schema_version: '1',
    event_cursor: eventCursor,
    policy,
    pruning_request_id: activeRequest?.pruning_request_id || null,
    revision_ids: revisionIds
  })).digest('hex');
}

export function buildRetentionCandidate(reconciliation, policyInput = DEFAULT_RETENTION_POLICY) {
  const policy = createRetentionPolicy(policyInput);
  const operations = operationsState(reconciliation.projection);
  const diagnostics = reconciliation.canvas_blobs || {
    total_bytes: 0,
    largest_blob: null,
    blobs: [],
    temporary_files: [],
    unexpected_entries: []
  };
  const { sizes, referenced, orphaned } = blobMaps(diagnostics);
  const revisions = unprunedRevisions(operations);
  const protectedIds = protectedRevisionIds(operations);
  const eligible = revisions
    .filter((revision) => !protectedIds.has(revision.revision_id))
    .sort(compareRevisions);
  const referenceCounts = new Map();
  for (const revision of revisions) {
    referenceCounts.set(
      revision.content_sha256,
      (referenceCounts.get(revision.content_sha256) || 0) + 1
    );
  }
  const referencedBytes = referenced.reduce((total, blob) => total + blob.byte_length, 0);
  const orphanBytes = orphaned.reduce((total, blob) => total + blob.byte_length, 0);
  const temporaryFileBytes = temporaryBytes(diagnostics);
  const physicalBytes = physicalTotalBytes(diagnostics);
  let projectedReferencedBytes = referencedBytes;
  const selected = [];
  for (const revision of eligible) {
    if (projectedReferencedBytes < policy.reclaim_below_bytes) break;
    selected.push(revision);
    const remaining = (referenceCounts.get(revision.content_sha256) || 0) - 1;
    referenceCounts.set(revision.content_sha256, remaining);
    if (remaining === 0) {
      projectedReferencedBytes -= sizes.get(revision.content_sha256) || revision.byte_length;
    }
  }
  const reclaimableBytes = referencedBytes - projectedReferencedBytes;
  const projectedTotalBytes = diagnostics.total_bytes - reclaimableBytes;
  const projectedPhysicalTotalBytes = physicalBytes - reclaimableBytes;
  let blockedReason = null;
  if (physicalBytes >= policy.soft_bytes) {
    if (eligible.length === 0) blockedReason = 'no_eligible_revisions';
    else if (projectedPhysicalTotalBytes >= policy.reclaim_below_bytes) {
      blockedReason = orphanBytes > 0 || temporaryFileBytes > 0
        ? 'orphan_or_protected_bytes_above_target'
        : 'protected_bytes_above_target';
    }
  }
  const selectedIds = selected.map((revision) => revision.revision_id);
  const activeRequest = operations?.pruning.active_request || null;
  return Object.freeze({
    schema_version: '1',
    event_cursor: reconciliation.event_count,
    pruning_request_id: activeRequest?.pruning_request_id || null,
    candidate_digest: candidateDigest(
      reconciliation.event_count,
      policy,
      activeRequest,
      selectedIds
    ),
    selected_revisions: Object.freeze(selected.map((revision) => Object.freeze({
      revision_id: revision.revision_id,
      operations_surface_id: revision.operations_surface_id,
      content_sha256: revision.content_sha256,
      blob_ref: revision.blob_ref,
      byte_length: revision.byte_length,
      committed_at: revision.committed_at
    }))),
    selected_revision_ids: Object.freeze(selectedIds),
    eligible_revision_count: eligible.length,
    protected_revision_count: protectedIds.size,
    referenced_bytes: referencedBytes,
    orphan_bytes: orphanBytes,
    temporary_bytes: temporaryFileBytes,
    physical_total_bytes: physicalBytes,
    reclaimable_bytes: reclaimableBytes,
    projected_referenced_bytes: projectedReferencedBytes,
    projected_total_bytes: projectedTotalBytes,
    projected_physical_total_bytes: projectedPhysicalTotalBytes,
    blocked_reason: blockedReason
  });
}

export function buildStorageDiagnostics(reconciliation, policyInput = DEFAULT_RETENTION_POLICY) {
  const policy = createRetentionPolicy(policyInput);
  const operations = operationsState(reconciliation.projection);
  const blobs = reconciliation.canvas_blobs || {
    blob_count: 0,
    total_bytes: 0,
    largest_blob: null,
    blobs: [],
    temporary_files: [],
    unreferenced_blobs: [],
    unexpected_entries: []
  };
  const candidate = buildRetentionCandidate(reconciliation, policy);
  return Object.freeze({
    schema_version: '1',
    policy,
    state: operations?.pruning.state || 'normal',
    active_request: operations?.pruning.active_request || null,
    total_bytes: blobs.total_bytes,
    temporary_bytes: temporaryBytes(blobs),
    physical_total_bytes: physicalTotalBytes(blobs),
    referenced_bytes: candidate.referenced_bytes,
    orphan_bytes: candidate.orphan_bytes,
    blob_count: blobs.blob_count,
    referenced_blob_count: (blobs.blobs || []).filter((blob) => blob.referenced).length,
    orphan_blob_count: (blobs.blobs || []).filter((blob) => !blob.referenced).length,
    largest_blob: blobs.largest_blob,
    temporary_file_count: (blobs.temporary_files || []).length,
    unexpected_entry_count: (blobs.unexpected_entries || []).length,
    eligible_revision_count: candidate.eligible_revision_count,
    candidate_revision_count: candidate.selected_revisions.length,
    blocked_reason: candidate.blocked_reason,
    event_cursor: reconciliation.event_count
  });
}

function commandDigest(value) {
  return createHash('sha256').update(JSON.stringify(value)).digest('hex');
}

function retainCommand(map, commandId, digest, result) {
  map.set(commandId, Object.freeze({ digest, result }));
  while (map.size > RETENTION_COMMAND_LIMIT) map.delete(map.keys().next().value);
}

function commandRetry(map, commandId, digest) {
  const existing = map.get(commandId);
  if (!existing) return null;
  if (existing.digest !== digest) {
    throw retentionError('pruning_command_conflict', 'pruning command id is bound to different input', {
      command_id: commandId
    });
  }
  return existing.result;
}

function hasUnprunedDigest(projection, digest) {
  const operations = operationsState(projection);
  return unprunedRevisions(operations).some((revision) => revision.content_sha256 === digest);
}

export function createCanvasRetentionService(options) {
  const {
    blobStore,
    persistence,
    policy: policyOverrides = {},
    now = () => new Date().toISOString(),
    randomId = randomUUID,
    setTimer = globalThis.setTimeout,
    clearTimer = globalThis.clearTimeout,
    runSerialized = (operation) => operation(),
    onAutomaticResult = () => undefined
  } = options;
  if (!blobStore
    || typeof blobStore.delete !== 'function'
    || typeof blobStore.deleteTemporary !== 'function') {
    throw retentionError(
      'retention_blob_store_invalid',
      'retention blob store must expose delete and deleteTemporary'
    );
  }
  if (!persistence || typeof persistence.reconcile !== 'function'
    || typeof persistence.commitEvent !== 'function') {
    throw retentionError('retention_persistence_invalid', 'retention persistence is invalid');
  }
  if (typeof now !== 'function' || typeof randomId !== 'function'
    || typeof setTimer !== 'function' || typeof clearTimer !== 'function'
    || typeof runSerialized !== 'function' || typeof onAutomaticResult !== 'function') {
    throw retentionError('retention_runtime_invalid', 'retention runtime dependencies are invalid');
  }
  const policy = createRetentionPolicy(policyOverrides);
  const previewCommands = new Map();
  const commitCommands = new Map();
  let deadlineTimer = null;
  let deadlineAt = null;
  let closed = false;
  let lastAutomaticResult = null;

  function clearDeadline() {
    if (deadlineTimer !== null) clearTimer(deadlineTimer);
    deadlineTimer = null;
    deadlineAt = null;
  }

  function timerState() {
    return Object.freeze({
      scheduled: deadlineTimer !== null,
      deadline_at: deadlineAt,
      closed
    });
  }

  function automaticErrorResult(error, source, trigger, reconciliation, reclaimed, pruned) {
    return {
      schema_version: '1',
      status: 'failed',
      source,
      trigger,
      cleanup_blocked: true,
      blocked_reason: 'automatic_cleanup_failed',
      error: {
        code: error.code || 'automatic_cleanup_failed',
        message: error.message,
        cause_code: error.cause_code || null,
        event_id: error.event_id || null,
        tombstone_committed: error.tombstone_committed || false
      },
      reclaimed,
      pruned_revisions: pruned,
      storage: reconciliation ? buildStorageDiagnostics(reconciliation, policy) : null,
      notification: {
        schema_version: '1',
        type: 'canvas.storage.changed',
        reason: 'automatic_prune_failed',
        error_code: error.code || 'automatic_cleanup_failed'
      }
    };
  }

  function finishAutomatic(result, reconciliation, scheduleDeadline = null) {
    let nextEvaluationAt = null;
    if (!closed && scheduleDeadline) {
      nextEvaluationAt = armDeadline(scheduleDeadline, result.reduce_options || {});
    } else {
      clearDeadline();
    }
    const { reduce_options: ignored, ...publicResult } = result;
    lastAutomaticResult = Object.freeze({
      ...publicResult,
      next_evaluation_at: nextEvaluationAt
    });
    return lastAutomaticResult;
  }

  function armDeadline(deadline, reduceOptions) {
    if (closed) return null;
    if (deadlineTimer !== null && deadlineAt === deadline) return deadlineAt;
    clearDeadline();
    const parsedDeadline = Date.parse(deadline);
    const parsedNow = Date.parse(now());
    const delay = Math.max(0, Math.min(2_147_483_647, parsedDeadline - parsedNow));
    deadlineAt = deadline;
    deadlineTimer = setTimer(() => {
      deadlineTimer = null;
      deadlineAt = null;
      if (closed) return;
      Promise.resolve(runSerialized(() => evaluateAutomatic(reduceOptions, { source: 'timer' })))
        .then((result) => onAutomaticResult(result))
        .catch((error) => onAutomaticResult(automaticErrorResult(
          error,
          'timer',
          null,
          null,
          { orphan_bytes: 0, temporary_bytes: 0 },
          []
        )));
    }, delay);
    deadlineTimer?.unref?.();
    return deadlineAt;
  }

  function scheduleActiveRequest(reconciliation, reduceOptions) {
    const activeRequest = operationsState(reconciliation.projection)?.pruning.active_request;
    if (!activeRequest) {
      clearDeadline();
      return null;
    }
    return armDeadline(activeRequest.grace_deadline, reduceOptions);
  }

  async function inspect(reduceOptions = {}, options = {}) {
    let reconciliation = await persistence.reconcile(reduceOptions);
    let notification = null;
    const operations = operationsState(reconciliation.projection);
    if (options.openGrace !== false
      && operations
      && physicalTotalBytes(reconciliation.canvas_blobs) >= policy.soft_bytes
      && operations.pruning.active_request === null) {
      const requestedAt = now();
      const pruningRequest = {
        pruning_request_id: `pruning-request-${randomId()}`,
        observed_bytes: physicalTotalBytes(reconciliation.canvas_blobs),
        soft_limit_bytes: policy.soft_bytes,
        hard_limit_bytes: policy.hard_bytes,
        grace_deadline: new Date(Date.parse(requestedAt) + policy.grace_ms).toISOString(),
        requested_at: requestedAt
      };
      reconciliation = await persistence.commitEvent({
        event_version: OPERATIONS_V1_EVENT_VERSION,
        event_id: `event-${Date.now()}-${randomId()}`,
        event_type: 'canvas.pruning_requested',
        pruning_request: pruningRequest,
        created_at: requestedAt
      }, reduceOptions);
      notification = {
        schema_version: '1',
        type: 'canvas.storage.changed',
        reason: 'grace_opened',
        pruning_request_id: pruningRequest.pruning_request_id
      };
    }
    if (options.schedule !== false) scheduleActiveRequest(reconciliation, reduceOptions);
    return {
      storage: buildStorageDiagnostics(reconciliation, policy),
      notification,
      next_evaluation_at: deadlineAt
    };
  }

  async function preview(input, reduceOptions = {}) {
    const digest = commandDigest(input);
    const retried = commandRetry(previewCommands, input.command_id, digest);
    if (retried) return { ...retried, idempotent: true };
    const reconciliation = await persistence.reconcile(reduceOptions);
    const activeRequest = operationsState(reconciliation.projection)?.pruning.active_request;
    if (!activeRequest) {
      throw retentionError('pruning_request_not_active', 'no pruning grace request is active');
    }
    const candidate = buildRetentionCandidate(reconciliation, policy);
    const result = Object.freeze({
      schema_version: '1',
      command_id: input.command_id,
      idempotent: false,
      candidate,
      storage: buildStorageDiagnostics(reconciliation, policy)
    });
    retainCommand(previewCommands, input.command_id, digest, result);
    return result;
  }

  async function commit(input, reduceOptions = {}) {
    const digest = commandDigest(input);
    const retried = commandRetry(commitCommands, input.command_id, digest);
    if (retried) return { ...retried, idempotent: true };
    let reconciliation = await persistence.reconcile(reduceOptions);
    const activeRequest = operationsState(reconciliation.projection)?.pruning.active_request;
    if (!activeRequest) {
      throw retentionError('pruning_request_not_active', 'no pruning grace request is active');
    }
    const candidate = buildRetentionCandidate(reconciliation, policy);
    if (candidate.candidate_digest !== input.expected_candidate_digest) {
      throw retentionError('pruning_candidate_changed', 'pruning candidate digest is stale', {
        expected_candidate_digest: input.expected_candidate_digest,
        actual_candidate_digest: candidate.candidate_digest
      });
    }
    if (candidate.selected_revisions.length === 0) {
      throw retentionError('pruning_no_candidates', 'no historical revisions are eligible for pruning', {
        blocked_reason: candidate.blocked_reason
      });
    }

    const finalState = candidate.projected_total_bytes < policy.reclaim_below_bytes
      ? 'normal'
      : 'reclaiming';
    const results = [];
    for (const [index, revision] of candidate.selected_revisions.entries()) {
      const prunedAt = now();
      const last = index === candidate.selected_revisions.length - 1;
      const event = {
        event_version: OPERATIONS_V1_EVENT_VERSION,
        event_id: `event-${Date.now()}-${randomId()}`,
        event_type: 'canvas.revision_pruned',
        tombstone: {
          pruning_request_id: activeRequest.pruning_request_id,
          revision_id: revision.revision_id,
          operations_surface_id: revision.operations_surface_id,
          content_sha256: revision.content_sha256,
          blob_ref: revision.blob_ref,
          reason: 'manual',
          retention_state_after: last ? finalState : 'reclaiming',
          pruned_at: prunedAt
        },
        created_at: prunedAt
      };
      try {
        reconciliation = await persistence.commitEvent(event, reduceOptions);
      } catch (error) {
        error.pruned_revisions = results.map((result) => result.revision_id);
        throw error;
      }
      let bodyDeleted = false;
      if (!hasUnprunedDigest(reconciliation.projection, revision.content_sha256)) {
        try {
          const deletion = await blobStore.delete(revision.content_sha256);
          bodyDeleted = deletion.deleted;
        } catch (error) {
          throw retentionError(
            'retention_blob_delete_failed',
            `prune tombstone committed but blob deletion failed: ${error.message}`,
            {
              cause_code: error.code || null,
              revision_id: revision.revision_id,
              content_sha256: revision.content_sha256,
              tombstone_committed: true,
              pruned_revisions: [...results.map((result) => result.revision_id), revision.revision_id]
            }
          );
        }
      }
      results.push(Object.freeze({
        revision_id: revision.revision_id,
        content_sha256: revision.content_sha256,
        body_deleted: bodyDeleted
      }));
    }

    reconciliation = await persistence.reconcile(reduceOptions);
    const result = Object.freeze({
      schema_version: '1',
      command_id: input.command_id,
      idempotent: false,
      candidate_digest: candidate.candidate_digest,
      pruned_revisions: Object.freeze(results),
      storage: buildStorageDiagnostics(reconciliation, policy),
      notification: Object.freeze({
        schema_version: '1',
        type: 'canvas.storage.changed',
        reason: 'manual_prune',
        pruning_request_id: activeRequest.pruning_request_id
      })
    });
    retainCommand(commitCommands, input.command_id, digest, result);
    scheduleActiveRequest(reconciliation, reduceOptions);
    return result;
  }

  async function completeAutomatic(
    reconciliation,
    activeRequest,
    trigger,
    reclaimed,
    reduceOptions
  ) {
    const finalTotalBytes = physicalTotalBytes(reconciliation.canvas_blobs);
    if (finalTotalBytes >= policy.reclaim_below_bytes) return null;
    const completedAt = now();
    return persistence.commitEvent({
      event_version: OPERATIONS_V1_EVENT_VERSION,
      event_id: `event-${Date.now()}-${randomId()}`,
      event_type: 'canvas.pruning_completed',
      completion: {
        pruning_request_id: activeRequest.pruning_request_id,
        trigger,
        reclaimed_orphan_bytes: reclaimed.orphan_bytes,
        reclaimed_temporary_bytes: reclaimed.temporary_bytes,
        final_total_bytes: finalTotalBytes,
        completed_at: completedAt
      },
      created_at: completedAt
    }, reduceOptions);
  }

  async function removeAutomaticResidue(reconciliation) {
    const reclaimed = { orphan_bytes: 0, temporary_bytes: 0 };
    for (const temporary of reconciliation.canvas_blobs.temporary_files || []) {
      const deletion = await blobStore.deleteTemporary(temporary.name);
      if (deletion.deleted) reclaimed.temporary_bytes += deletion.byte_length;
    }
    for (const digest of reconciliation.canvas_blobs.unreferenced_blobs || []) {
      const deletion = await blobStore.delete(digest);
      if (deletion.deleted) reclaimed.orphan_bytes += deletion.byte_length;
    }
    return reclaimed;
  }

  async function pruneAutomatically(reconciliation, activeRequest, reduceOptions) {
    const candidate = buildRetentionCandidate(reconciliation, policy);
    const pruned = [];
    for (const revision of candidate.selected_revisions) {
      const prunedAt = now();
      try {
        reconciliation = await persistence.commitEvent({
          event_version: OPERATIONS_V1_EVENT_VERSION,
          event_id: `event-${Date.now()}-${randomId()}`,
          event_type: 'canvas.revision_pruned',
          tombstone: {
            pruning_request_id: activeRequest.pruning_request_id,
            revision_id: revision.revision_id,
            operations_surface_id: revision.operations_surface_id,
            content_sha256: revision.content_sha256,
            blob_ref: revision.blob_ref,
            reason: 'automatic',
            retention_state_after: 'reclaiming',
            pruned_at: prunedAt
          },
          created_at: prunedAt
        }, reduceOptions);
      } catch (error) {
        error.pruned_revisions = pruned.map((item) => item.revision_id);
        throw error;
      }
      let bodyDeleted = false;
      if (!hasUnprunedDigest(reconciliation.projection, revision.content_sha256)) {
        try {
          const deletion = await blobStore.delete(revision.content_sha256);
          bodyDeleted = deletion.deleted;
        } catch (error) {
          throw retentionError(
            'retention_blob_delete_failed',
            `automatic tombstone committed but blob deletion failed: ${error.message}`,
            {
              cause_code: error.code || null,
              revision_id: revision.revision_id,
              content_sha256: revision.content_sha256,
              tombstone_committed: true,
              pruned_revisions: [...pruned.map((item) => item.revision_id), revision.revision_id]
            }
          );
        }
      }
      pruned.push(Object.freeze({
        revision_id: revision.revision_id,
        content_sha256: revision.content_sha256,
        body_deleted: bodyDeleted
      }));
    }
    return { reconciliation, candidate, pruned };
  }

  async function evaluateAutomatic(reduceOptions = {}, options = {}) {
    const source = options.source || 'evaluation';
    let reconciliation = null;
    let trigger = null;
    let reclaimed = { orphan_bytes: 0, temporary_bytes: 0 };
    let pruned = [];
    let graceNotification = null;
    try {
      reconciliation = await persistence.reconcile(reduceOptions);
      let operations = operationsState(reconciliation.projection);
      if (!operations) {
        return finishAutomatic({
          schema_version: '1', status: 'idle', source, trigger: null,
          cleanup_blocked: false, blocked_reason: null, reclaimed,
          pruned_revisions: pruned, storage: buildStorageDiagnostics(reconciliation, policy),
          notification: null
        }, reconciliation);
      }

      if (operations.pruning.active_request === null
        && physicalTotalBytes(reconciliation.canvas_blobs) >= policy.soft_bytes) {
        const opened = await inspect(reduceOptions, { schedule: false });
        graceNotification = opened.notification;
        reconciliation = await persistence.reconcile(reduceOptions);
        operations = operationsState(reconciliation.projection);
      }

      const activeRequest = operations.pruning.active_request;
      if (!activeRequest) {
        return finishAutomatic({
          schema_version: '1', status: 'idle', source, trigger: null,
          cleanup_blocked: false, blocked_reason: null, reclaimed,
          pruned_revisions: pruned, storage: buildStorageDiagnostics(reconciliation, policy),
          notification: graceNotification
        }, reconciliation);
      }

      const physicalBytes = physicalTotalBytes(reconciliation.canvas_blobs);
      const evaluatedAt = Date.parse(now());
      if (physicalBytes >= policy.hard_bytes) trigger = 'hard_threshold';
      else if (operations.pruning.state === 'reclaiming' || physicalBytes < policy.soft_bytes) {
        trigger = 'recovery';
      } else if (evaluatedAt >= Date.parse(activeRequest.grace_deadline)) {
        trigger = 'grace_expired';
      }

      if (!trigger) {
        return finishAutomatic({
          schema_version: '1', status: 'scheduled', source, trigger: null,
          cleanup_blocked: false, blocked_reason: null, reclaimed,
          pruned_revisions: pruned, storage: buildStorageDiagnostics(reconciliation, policy),
          notification: graceNotification, reduce_options: reduceOptions
        }, reconciliation, activeRequest.grace_deadline);
      }

      reconciliation = await persistence.reconcile(reduceOptions);
      reclaimed = await removeAutomaticResidue(reconciliation);
      reconciliation = await persistence.reconcile(reduceOptions);

      let completion = await completeAutomatic(
        reconciliation,
        activeRequest,
        trigger,
        reclaimed,
        reduceOptions
      );
      if (completion) {
        reconciliation = completion;
        return finishAutomatic({
          schema_version: '1', status: 'completed', source, trigger,
          cleanup_blocked: false, blocked_reason: null, reclaimed,
          pruned_revisions: pruned, storage: buildStorageDiagnostics(reconciliation, policy),
          notification: {
            schema_version: '1', type: 'canvas.storage.changed',
            reason: 'automatic_prune', pruning_request_id: activeRequest.pruning_request_id
          }
        }, reconciliation);
      }

      const automaticPrune = await pruneAutomatically(
        reconciliation,
        activeRequest,
        reduceOptions
      );
      reconciliation = automaticPrune.reconciliation;
      pruned = automaticPrune.pruned;
      reconciliation = await persistence.reconcile(reduceOptions);
      completion = await completeAutomatic(
        reconciliation,
        activeRequest,
        trigger,
        reclaimed,
        reduceOptions
      );
      if (completion) {
        reconciliation = completion;
        return finishAutomatic({
          schema_version: '1', status: 'completed', source, trigger,
          cleanup_blocked: false, blocked_reason: null, reclaimed,
          pruned_revisions: pruned, storage: buildStorageDiagnostics(reconciliation, policy),
          notification: {
            schema_version: '1', type: 'canvas.storage.changed',
            reason: 'automatic_prune', pruning_request_id: activeRequest.pruning_request_id
          }
        }, reconciliation);
      }

      const remaining = buildRetentionCandidate(reconciliation, policy);
      return finishAutomatic({
        schema_version: '1', status: 'blocked', source, trigger,
        cleanup_blocked: true,
        blocked_reason: remaining.blocked_reason || 'target_not_reached',
        reclaimed, pruned_revisions: pruned,
        storage: buildStorageDiagnostics(reconciliation, policy),
        notification: {
          schema_version: '1', type: 'canvas.storage.changed',
          reason: 'automatic_prune_blocked',
          pruning_request_id: activeRequest.pruning_request_id
        }
      }, reconciliation);
    } catch (error) {
      try {
        reconciliation = await persistence.reconcile(reduceOptions);
      } catch {
        // Preserve the first failure and do not attempt cleanup without valid replay.
      }
      return finishAutomatic(
        automaticErrorResult(error, source, trigger, reconciliation, reclaimed, pruned),
        reconciliation
      );
    }
  }

  function close() {
    closed = true;
    clearDeadline();
  }

  return Object.freeze({
    inspect,
    preview,
    commit,
    evaluateAutomatic,
    timerState,
    get lastAutomaticResult() {
      return lastAutomaticResult;
    },
    close,
    policy
  });
}
