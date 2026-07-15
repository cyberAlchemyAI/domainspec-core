import { createHash, randomUUID } from 'node:crypto';
import { readWorkspaceHtml } from './canvas.mjs';
import { htmlTransformEngine } from './html-transform.mjs';
import {
  assertUtf8ByteLimit,
  OPERATIONS_V1_EVENT_VERSION,
  OPERATIONS_V1_LIMITS
} from './operations-contracts.mjs';

const OPERATIONS_SURFACE_ID_PATTERN = /^operations-surface-[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/;
const REVISION_ID_PATTERN = /^revision-[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/;

function operationsError(code, message, fields = {}) {
  const error = new Error(message);
  error.code = code;
  Object.assign(error, fields);
  return error;
}

function decodeOperationsHtml(bytes) {
  const html = bytes.toString('utf8');
  if (!Buffer.from(html, 'utf8').equals(bytes)) {
    throw operationsError(
      'operations_source_invalid_utf8',
      'Operations source is not valid UTF-8 HTML'
    );
  }
  return html;
}

export function normalizeOperationsDerivationInput(input) {
  return {
    schema_version: input.schema_version,
    source_v0_surface_id: input.source_v0_surface_id,
    source_revision_id: input.source_revision_id,
    operation_surface_idempotency_key: input.operation_surface_idempotency_key
  };
}

export function operationsDerivationDigest(input) {
  return createHash('sha256')
    .update(JSON.stringify(normalizeOperationsDerivationInput(input)))
    .digest('hex');
}

export function normalizeContentOperationInput(input) {
  const inline = input.input.kind === 'inline_html';
  const inputDigest = inline
    ? createHash('sha256').update(Buffer.from(input.input.html, 'utf8')).digest('hex')
    : input.input.expected_sha256;
  return {
    normalized: {
      schema_version: input.schema_version,
      operation_id: input.operation_id,
      operations_surface_id: input.operations_surface_id,
      expected_revision_id: input.expected_revision_id,
      mode: input.mode,
      target: { kind: input.target.kind },
      input: inline
        ? { kind: input.input.kind, content_sha256: inputDigest }
        : {
            kind: input.input.kind,
            path: input.input.path,
            expected_sha256: input.input.expected_sha256
          }
    },
    input_digest: inputDigest
  };
}

export function contentOperationDigest(input) {
  const normalized = normalizeContentOperationInput(input);
  return {
    ...normalized,
    normalized_request_digest: createHash('sha256')
      .update(JSON.stringify(normalized.normalized))
      .digest('hex')
  };
}

function operationsContentUrl(surfaceId, revisionId) {
  return `/api/canvas/operation-surfaces/${encodeURIComponent(surfaceId)}`
    + `/revisions/${encodeURIComponent(revisionId)}/content`;
}

function projectedDerivation(projection, derivation, idempotent) {
  const operations = projection.canvas?.operations_v1;
  const surface = operations?.surfaces[derivation.result_operations_surface_id];
  const revision = operations?.revisions[derivation.result_revision_id];
  if (!surface || !revision) {
    throw operationsError(
      'operations_projection_invalid',
      'derivation outcome is missing from the Operations projection'
    );
  }
  return {
    schema_version: '1',
    surface,
    revision,
    content_url: operationsContentUrl(surface.operations_surface_id, revision.revision_id),
    idempotent
  };
}

function projectedOperation(projection, operation, idempotent) {
  const operations = projection.canvas?.operations_v1;
  const surface = operations?.surfaces[operation.operations_surface_id];
  const revision = operations?.revisions[operation.result_revision_id];
  const resultIndex = surface?.revision_ids.indexOf(operation.result_revision_id) ?? -1;
  if (!surface || !revision || resultIndex < 0) {
    throw operationsError(
      'operations_projection_invalid',
      'operation outcome is missing from the Operations projection'
    );
  }
  const resultSurface = {
    ...surface,
    current_revision_id: operation.result_revision_id,
    revision_ids: surface.revision_ids.slice(0, resultIndex + 1),
    updated_at: operation.committed_at
  };
  const tombstone = operations.prune_tombstones[revision.revision_id] || null;
  return {
    schema_version: '1',
    operation,
    surface: resultSurface,
    revision,
    content_url: operationsContentUrl(resultSurface.operations_surface_id, revision.revision_id),
    idempotent,
    ...(tombstone
      ? {
          result_body_status: 'operation_result_pruned',
          result_body_available: false,
          tombstone
        }
      : {})
  };
}

function sourceUnavailable(input, reason, causeCode = null) {
  return operationsError(
    'source_revision_unavailable',
    'the selected V0 revision is not available as exact workspace bytes',
    {
      source_v0_surface_id: input.source_v0_surface_id,
      source_revision_id: input.source_revision_id,
      reason,
      cause_code: causeCode
    }
  );
}

export function createOperationsService(options) {
  const {
    workspaceRoot,
    blobStore,
    persistence,
    now = () => new Date().toISOString(),
    randomId = randomUUID
  } = options;
  if (typeof workspaceRoot !== 'string' || !workspaceRoot) {
    throw operationsError('operations_service_invalid', 'workspaceRoot is required');
  }
  if (!blobStore || typeof blobStore.put !== 'function') {
    throw operationsError('operations_service_invalid', 'blobStore is required');
  }
  if (!persistence || typeof persistence.reconcile !== 'function'
    || typeof persistence.commitEvent !== 'function') {
    throw operationsError('operations_service_invalid', 'persistence is required');
  }

  async function derive(input, reduceOptions = {}) {
    const normalizedInputDigest = operationsDerivationDigest(input);
    const { projection } = await persistence.reconcile(reduceOptions);
    const operations = projection.canvas?.operations_v1;
    const existing = operations?.derivation_keys[input.operation_surface_idempotency_key];

    if (existing) {
      if (existing.normalized_input_digest !== normalizedInputDigest) {
        throw operationsError(
          'derivation_key_conflict',
          'derivation idempotency key is already bound to different input',
          {
            operation_surface_idempotency_key: input.operation_surface_idempotency_key,
            expected_digest: existing.normalized_input_digest,
            actual_digest: normalizedInputDigest
          }
        );
      }
      return projectedDerivation(projection, existing, true);
    }

    const sourceSurface = projection.canvas?.surfaces[input.source_v0_surface_id];
    const sourceRevision = projection.canvas?.revisions[input.source_revision_id];
    if (!sourceSurface || !sourceRevision
      || sourceRevision.surface_id !== sourceSurface.surface_id
      || !sourceSurface.revision_ids.includes(sourceRevision.revision_id)) {
      throw sourceUnavailable(input, 'projection_missing');
    }

    let file;
    try {
      file = await readWorkspaceHtml(workspaceRoot, sourceSurface.path);
    } catch (error) {
      throw sourceUnavailable(input, 'workspace_unavailable', error.code || null);
    }
    if (file.byte_length > OPERATIONS_V1_LIMITS.source_html_bytes) {
      throw sourceUnavailable(input, 'source_limit_exceeded');
    }
    if (file.content_sha256 !== sourceRevision.content_sha256
      || file.byte_length !== sourceRevision.byte_length) {
      throw sourceUnavailable(input, 'workspace_drift');
    }

    const blob = await blobStore.put(file.bytes);
    const committedAt = now();
    const operationsSurfaceId = `operations-surface-${randomId()}`;
    const revisionId = `revision-${randomId()}`;
    const derivation = {
      operation_surface_idempotency_key: input.operation_surface_idempotency_key,
      normalized_input_digest: normalizedInputDigest,
      source_v0_surface_id: sourceSurface.surface_id,
      source_v0_revision_id: sourceRevision.revision_id,
      result_operations_surface_id: operationsSurfaceId,
      result_revision_id: revisionId
    };
    const surface = {
      operations_surface_id: operationsSurfaceId,
      source_v0_surface_id: sourceSurface.surface_id,
      source_v0_revision_id: sourceRevision.revision_id,
      current_revision_id: revisionId,
      revision_ids: [revisionId],
      created_at: committedAt,
      updated_at: committedAt
    };
    const revision = {
      revision_id: revisionId,
      operations_surface_id: operationsSurfaceId,
      content_sha256: blob.sha256,
      blob_ref: blob.blob_ref,
      byte_length: blob.byte_length,
      committed_at: committedAt
    };
    const event = {
      event_version: OPERATIONS_V1_EVENT_VERSION,
      event_id: `event-${Date.now()}-${randomId()}`,
      event_type: 'canvas.operations_surface_derived',
      derivation,
      surface,
      revision,
      created_at: committedAt
    };
    const committed = await persistence.commitEvent(event, reduceOptions);
    return projectedDerivation(committed.projection, derivation, false);
  }

  async function getSurface(surfaceId, reduceOptions = {}) {
    if (typeof surfaceId !== 'string' || !OPERATIONS_SURFACE_ID_PATTERN.test(surfaceId)) {
      throw operationsError('operations_surface_not_found', 'Operations surface not found');
    }
    const { projection } = await persistence.reconcile(reduceOptions);
    const surface = projection.canvas?.operations_v1?.surfaces[surfaceId];
    const revision = surface
      ? projection.canvas.operations_v1.revisions[surface.current_revision_id]
      : null;
    if (!surface || !revision) {
      throw operationsError('operations_surface_not_found', 'Operations surface not found');
    }
    return {
      schema_version: '1',
      surface,
      revision,
      content_url: operationsContentUrl(surface.operations_surface_id, revision.revision_id)
    };
  }

  async function operate(input, reduceOptions = {}) {
    const digests = contentOperationDigest(input);
    const { projection } = await persistence.reconcile(reduceOptions);
    const operations = projection.canvas?.operations_v1;
    const existingOperation = operations?.operations[input.operation_id];

    if (existingOperation) {
      if (existingOperation.normalized_request_digest !== digests.normalized_request_digest) {
        throw operationsError(
          'operation_id_conflict',
          'operation id is already bound to different input',
          {
            operation_id: input.operation_id,
            expected_digest: existingOperation.normalized_request_digest,
            actual_digest: digests.normalized_request_digest
          }
        );
      }
      return { ...projectedOperation(projection, existingOperation, true), notification: null };
    }
    if (!['replace', 'append', 'rebuild'].includes(input.mode)) {
      throw operationsError(
        'operation_mode_unavailable',
        `operation mode ${input.mode} is not available yet`,
        { mode: input.mode }
      );
    }

    const surface = operations?.surfaces[input.operations_surface_id];
    if (!surface) {
      throw operationsError('operations_surface_not_found', 'Operations surface not found');
    }
    if (surface.current_revision_id !== input.expected_revision_id) {
      throw operationsError(
        'revision_changed',
        'expected Operations revision is no longer current',
        {
          expected_revision_id: input.expected_revision_id,
          current_revision_id: surface.current_revision_id
        }
      );
    }

    let transformed;
    if (input.mode === 'replace') {
      assertUtf8ByteLimit(
        input.input.html,
        OPERATIONS_V1_LIMITS.source_html_bytes,
        'source_html'
      );
      transformed = htmlTransformEngine.replace(input.input.html);
    } else if (input.mode === 'append') {
      assertUtf8ByteLimit(
        input.input.html,
        OPERATIONS_V1_LIMITS.fragment_html_bytes,
        'fragment_html'
      );
      const currentRevision = operations.revisions[surface.current_revision_id];
      if (!currentRevision) {
        throw operationsError(
          'operations_projection_invalid',
          'current Operations revision is missing from the projection'
        );
      }
      const currentBlob = await blobStore.read(currentRevision.content_sha256);
      const currentHtml = decodeOperationsHtml(currentBlob.bytes);
      transformed = htmlTransformEngine.append(currentHtml, input.input.html);
    } else {
      let file;
      try {
        file = await readWorkspaceHtml(workspaceRoot, input.input.path);
      } catch (error) {
        throw operationsError(
          'rebuild_source_unavailable',
          'rebuild workspace source is unavailable',
          { reason: 'workspace_unavailable', cause_code: error.code || null }
        );
      }
      if (file.content_sha256 !== input.input.expected_sha256) {
        throw operationsError(
          'rebuild_source_changed',
          'rebuild workspace source does not match expected digest',
          {
            expected_sha256: input.input.expected_sha256,
            actual_sha256: file.content_sha256
          }
        );
      }
      const sourceHtml = decodeOperationsHtml(file.bytes);
      assertUtf8ByteLimit(
        sourceHtml,
        OPERATIONS_V1_LIMITS.source_html_bytes,
        'source_html'
      );
      transformed = htmlTransformEngine.replace(sourceHtml);
    }
    assertUtf8ByteLimit(
      transformed.html,
      OPERATIONS_V1_LIMITS.result_html_bytes,
      'result_html'
    );
    const blob = await blobStore.put(transformed.bytes);
    const committedAt = now();
    const revisionId = `revision-${randomId()}`;
    const revision = {
      revision_id: revisionId,
      operations_surface_id: surface.operations_surface_id,
      content_sha256: blob.sha256,
      blob_ref: blob.blob_ref,
      byte_length: blob.byte_length,
      committed_at: committedAt
    };
    const nextSurface = {
      ...surface,
      current_revision_id: revisionId,
      revision_ids: [...surface.revision_ids, revisionId],
      updated_at: committedAt
    };
    const operation = {
      operation_id: input.operation_id,
      operations_surface_id: surface.operations_surface_id,
      normalized_request_digest: digests.normalized_request_digest,
      source_revision_id: surface.current_revision_id,
      mode: input.mode,
      target: { kind: input.target.kind },
      input_digest: digests.input_digest,
      source_lineage: input.mode === 'rebuild'
        ? {
            kind: 'workspace_html',
            path: input.input.path,
            expected_sha256: input.input.expected_sha256
          }
        : null,
      status: 'committed',
      result_revision_id: revisionId,
      result_digest: blob.sha256,
      result_blob_ref: blob.blob_ref,
      committed_at: committedAt
    };
    const event = {
      event_version: OPERATIONS_V1_EVENT_VERSION,
      event_id: `event-${Date.now()}-${randomId()}`,
      event_type: 'canvas.content_operation_committed',
      operation,
      surface: nextSurface,
      revision,
      created_at: committedAt
    };
    const committed = await persistence.commitEvent(event, reduceOptions);
    const result = projectedOperation(committed.projection, operation, false);
    const displayTarget = committed.projection.canvas.operations_v1.display_target;
    const notification = displayTarget?.surface_kind === 'operations_v1'
      && displayTarget.surface_id === surface.operations_surface_id
      ? { surface_id: surface.operations_surface_id, revision }
      : null;
    return { ...result, notification };
  }

  async function getContent(surfaceId, revisionId, reduceOptions = {}) {
    if (typeof surfaceId !== 'string' || !OPERATIONS_SURFACE_ID_PATTERN.test(surfaceId)
      || typeof revisionId !== 'string' || !REVISION_ID_PATTERN.test(revisionId)) {
      throw operationsError('operations_revision_not_found', 'Operations revision not found');
    }
    const { projection } = await persistence.reconcile(reduceOptions);
    const operations = projection.canvas?.operations_v1;
    const surface = operations?.surfaces[surfaceId];
    const revision = operations?.revisions[revisionId];
    if (!surface || !revision
      || revision.operations_surface_id !== surface.operations_surface_id
      || !surface.revision_ids.includes(revision.revision_id)) {
      throw operationsError('operations_revision_not_found', 'Operations revision not found');
    }
    const tombstone = operations.prune_tombstones[revisionId];
    if (tombstone) {
      throw operationsError(
        'revision_pruned',
        'Operations revision body was intentionally pruned',
        { tombstone }
      );
    }
    const blob = await blobStore.read(revision.content_sha256);
    return { revision, bytes: blob.bytes };
  }

  return Object.freeze({ derive, getSurface, operate, getContent });
}
