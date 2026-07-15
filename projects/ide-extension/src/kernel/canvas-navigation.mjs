import { createHash, randomUUID } from 'node:crypto';
import { readWorkspaceHtml } from './canvas.mjs';
import { OPERATIONS_V1_EVENT_VERSION } from './operations-contracts.mjs';

export const NAVIGATION_RETENTION_MS = 15 * 60 * 1000;
export const NAVIGATION_MAX_COMMANDS = 128;

function navigationError(code, message, fields = {}) {
  const error = new Error(message);
  error.code = code;
  Object.assign(error, fields);
  return error;
}

export function normalizeNavigationRequest(input) {
  return {
    schema_version: input.schema_version,
    command_id: input.command_id,
    action: input.action,
    ...(input.action === 'redirect'
      ? {
          destination: {
            kind: input.destination.kind,
            surface_kind: input.destination.surface_kind,
            surface_id: input.destination.surface_id,
            revision_id: input.destination.revision_id
          }
        }
      : {})
  };
}

export function navigationRequestDigest(input) {
  return createHash('sha256')
    .update(JSON.stringify(normalizeNavigationRequest(input)))
    .digest('hex');
}

function v0ContentUrl(surfaceId, revisionId) {
  return `/api/canvas/surfaces/${encodeURIComponent(surfaceId)}`
    + `/revisions/${encodeURIComponent(revisionId)}/content`;
}

function operationsContentUrl(surfaceId, revisionId) {
  return `/api/canvas/operation-surfaces/${encodeURIComponent(surfaceId)}`
    + `/revisions/${encodeURIComponent(revisionId)}/content`;
}

export function projectedDisplayTarget(projection) {
  const selected = projection.canvas?.operations_v1?.display_target;
  if (selected) return selected;
  const surfaceId = projection.canvas?.current_surface_id;
  const surface = surfaceId ? projection.canvas.surfaces[surfaceId] : null;
  if (!surface) return null;
  return {
    kind: 'surface_revision',
    surface_kind: 'v0',
    surface_id: surface.surface_id,
    revision_id: surface.current_revision_id
  };
}

export function projectCanvasDisplay(projection, target = projectedDisplayTarget(projection)) {
  if (!target) return { schema_version: '1', display: null };
  if (target.surface_kind === 'v0') {
    const surface = projection.canvas?.surfaces[target.surface_id];
    const revision = projection.canvas?.revisions[target.revision_id];
    if (!surface || !revision || revision.surface_id !== surface.surface_id
      || !surface.revision_ids.includes(revision.revision_id)) {
      throw navigationError('navigation_target_not_found', 'V0 display target was not found', {
        target
      });
    }
    return {
      schema_version: '1',
      display: {
        ...target,
        surface,
        revision,
        content_url: v0ContentUrl(surface.surface_id, revision.revision_id)
      }
    };
  }

  const operations = projection.canvas?.operations_v1;
  const surface = operations?.surfaces[target.surface_id];
  const revision = operations?.revisions[target.revision_id];
  if (!surface || !revision || revision.operations_surface_id !== surface.operations_surface_id
    || !surface.revision_ids.includes(revision.revision_id)) {
    throw navigationError('navigation_target_not_found', 'Operations display target was not found', {
      target
    });
  }
  if (operations.prune_tombstones[target.revision_id]) {
    throw navigationError('navigation_target_pruned', 'Operations display target was pruned', {
      target,
      tombstone: operations.prune_tombstones[target.revision_id]
    });
  }
  return {
    schema_version: '1',
    display: {
      ...target,
      surface,
      revision,
      content_url: operationsContentUrl(surface.operations_surface_id, revision.revision_id)
    }
  };
}

function navigationNotice(type, commandId, target) {
  return {
    schema_version: '1',
    type,
    command_id: commandId,
    target
  };
}

export function createCanvasNavigationService(options) {
  const {
    workspaceRoot,
    blobStore,
    persistence,
    now = Date.now,
    randomId = randomUUID,
    retentionMs = NAVIGATION_RETENTION_MS,
    maxCommands = NAVIGATION_MAX_COMMANDS
  } = options;
  if (typeof workspaceRoot !== 'string' || !workspaceRoot
    || !blobStore || typeof blobStore.read !== 'function'
    || !persistence || typeof persistence.reconcile !== 'function'
    || typeof persistence.commitEvent !== 'function'
    || typeof now !== 'function' || typeof randomId !== 'function'
    || !Number.isSafeInteger(retentionMs) || retentionMs <= 0
    || !Number.isSafeInteger(maxCommands) || maxCommands <= 0) {
    throw navigationError('navigation_service_invalid', 'navigation service options are invalid');
  }

  const transient = new Map();

  function observedNow() {
    const value = now();
    if (!Number.isSafeInteger(value) || value < 0) {
      throw navigationError('navigation_clock_invalid', 'navigation clock must return epoch milliseconds');
    }
    return value;
  }

  function purgeExpired(observed = observedNow()) {
    for (const [commandId, entry] of transient) {
      if (entry.expires_at_ms <= observed) transient.delete(commandId);
    }
  }

  function retain(record, display, observed = observedNow()) {
    purgeExpired(observed);
    if (transient.has(record.command_id)) transient.delete(record.command_id);
    while (transient.size >= maxCommands) {
      transient.delete(transient.keys().next().value);
    }
    const expiresAtMs = observed + retentionMs;
    const entry = {
      record: {
        ...record,
        expires_at: new Date(expiresAtMs).toISOString(),
        acknowledgement: null
      },
      display,
      expires_at_ms: expiresAtMs
    };
    transient.set(record.command_id, entry);
    return entry;
  }

  function commandResponse(entry, idempotent) {
    return {
      schema_version: '1',
      command: entry.record,
      display: entry.display,
      idempotent
    };
  }

  function conflict(input, expectedDigest, actualDigest) {
    throw navigationError(
      'navigation_command_conflict',
      'navigation command id is already bound to different input',
      {
        command_id: input.command_id,
        expected_digest: expectedDigest,
        actual_digest: actualDigest
      }
    );
  }

  async function assertAvailable(display) {
    if (display.surface_kind === 'v0') {
      let file;
      try {
        file = await readWorkspaceHtml(workspaceRoot, display.surface.path);
      } catch (error) {
        throw navigationError(
          'navigation_target_unavailable',
          'V0 display target bytes are unavailable',
          { target: display, reason: 'workspace_unavailable', cause_code: error.code || null }
        );
      }
      if (file.content_sha256 !== display.revision.content_sha256
        || file.byte_length !== display.revision.byte_length) {
        throw navigationError(
          'navigation_target_unavailable',
          'V0 display target bytes changed after publication',
          { target: display, reason: 'workspace_drift' }
        );
      }
      return display;
    }

    try {
      const blob = await blobStore.read(display.revision.content_sha256);
      if (blob.blob_ref !== display.revision.blob_ref
        || blob.byte_length !== display.revision.byte_length) {
        throw navigationError(
          'navigation_target_unavailable',
          'Operations display target blob metadata changed',
          { target: display, reason: 'blob_metadata_mismatch' }
        );
      }
    } catch (error) {
      if (error.code === 'navigation_target_unavailable') throw error;
      throw navigationError(
        'navigation_target_unavailable',
        'Operations display target bytes are unavailable',
        { target: display, reason: 'blob_unavailable', cause_code: error.code || null }
      );
    }
    return display;
  }

  async function getDisplay(reduceOptions = {}) {
    const { projection } = await persistence.reconcile(reduceOptions);
    const projected = projectCanvasDisplay(projection);
    if (projected.display) await assertAvailable(projected.display);
    return projected;
  }

  async function navigate(input, reduceOptions = {}) {
    const normalizedRequestDigest = navigationRequestDigest(input);
    const observed = observedNow();
    purgeExpired(observed);
    const retained = transient.get(input.command_id);
    if (retained) {
      if (retained.record.normalized_request_digest !== normalizedRequestDigest) {
        conflict(input, retained.record.normalized_request_digest, normalizedRequestDigest);
      }
      return { ...commandResponse(retained, true), notification: null };
    }

    const { projection } = await persistence.reconcile(reduceOptions);
    const durable = projection.canvas?.operations_v1?.redirect_commands[input.command_id];
    if (durable) {
      if (durable.normalized_request_digest !== normalizedRequestDigest) {
        conflict(input, durable.normalized_request_digest, normalizedRequestDigest);
      }
      const display = projectCanvasDisplay(projection, durable.target).display;
      const entry = retain({
        command_id: durable.command_id,
        action: durable.action,
        normalized_request_digest: durable.normalized_request_digest,
        target: durable.target,
        status: 'accepted',
        accepted_at: durable.selected_at
      }, display, observed);
      return { ...commandResponse(entry, true), notification: null };
    }

    if (input.action === 'redirect') {
      const projected = projectCanvasDisplay(projection, input.destination);
      await assertAvailable(projected.display);
      const selectedAt = new Date(observed).toISOString();
      const command = {
        command_id: input.command_id,
        action: 'redirect',
        normalized_request_digest: normalizedRequestDigest,
        target: input.destination,
        selected_at: selectedAt
      };
      const event = {
        event_version: OPERATIONS_V1_EVENT_VERSION,
        event_id: `event-${observed}-${randomId()}`,
        event_type: 'canvas.display_target_selected',
        command,
        created_at: selectedAt
      };
      const committed = await persistence.commitEvent(event, reduceOptions);
      const display = projectCanvasDisplay(committed.projection).display;
      const entry = retain({
        command_id: command.command_id,
        action: command.action,
        normalized_request_digest: command.normalized_request_digest,
        target: command.target,
        status: 'accepted',
        accepted_at: command.selected_at
      }, display, observed);
      return {
        ...commandResponse(entry, false),
        notification: navigationNotice('canvas.display.changed', command.command_id, command.target)
      };
    }

    const projected = projectCanvasDisplay(projection);
    if (!projected.display) {
      throw navigationError('display_target_not_found', 'there is no display target to refresh');
    }
    await assertAvailable(projected.display);
    const acceptedAt = new Date(observed).toISOString();
    const entry = retain({
      command_id: input.command_id,
      action: 'refresh',
      normalized_request_digest: normalizedRequestDigest,
      target: {
        kind: projected.display.kind,
        surface_kind: projected.display.surface_kind,
        surface_id: projected.display.surface_id,
        revision_id: projected.display.revision_id
      },
      status: 'accepted',
      accepted_at: acceptedAt
    }, projected.display, observed);
    return {
      ...commandResponse(entry, false),
      notification: navigationNotice(
        'canvas.refresh.requested',
        input.command_id,
        entry.record.target
      )
    };
  }

  function getStatus(commandId) {
    purgeExpired();
    const entry = transient.get(commandId);
    if (!entry) {
      throw navigationError('navigation_command_not_found', 'transient navigation command was not found', {
        command_id: commandId
      });
    }
    return commandResponse(entry, false);
  }

  function acknowledge(commandId, input) {
    const observed = observedNow();
    purgeExpired(observed);
    const entry = transient.get(commandId);
    if (!entry) {
      throw navigationError('navigation_command_not_found', 'transient navigation command was not found', {
        command_id: commandId
      });
    }
    if (entry.record.acknowledgement?.status === input.status) {
      return commandResponse(entry, true);
    }
    entry.record = {
      ...entry.record,
      status: input.status,
      acknowledgement: {
        status: input.status,
        acknowledged_at: new Date(observed).toISOString()
      }
    };
    return commandResponse(entry, false);
  }

  return Object.freeze({
    acknowledge,
    getDisplay,
    getStatus,
    navigate,
    projectDisplay: projectCanvasDisplay,
    get retainedCount() {
      purgeExpired();
      return transient.size;
    }
  });
}
