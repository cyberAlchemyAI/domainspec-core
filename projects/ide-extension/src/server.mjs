import http from 'node:http';
import { createHash, randomUUID } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  artifactRefFor,
  claimArtifactIds,
  evidenceArtifactIds,
  executionArtifactIds,
  validateArtifactRef,
  validateEvidenceRefs,
  writeArtifactRef
} from './kernel/artifacts.mjs';
import { blockedBeforeApproval, L0_GRANT_POLICY_VERSION } from './kernel/grants.mjs';
import {
  readWorkspaceHtml,
  prepareCanvasPublication,
  projectCurrentCanvas
} from './kernel/canvas.mjs';
import { createCanvasBlobStore } from './kernel/canvas-blobs.mjs';
import { createCanvasNavigationService } from './kernel/canvas-navigation.mjs';
import { createCanvasNotificationHub } from './kernel/canvas-notifications.mjs';
import { createCanvasRetentionService } from './kernel/canvas-retention.mjs';
import {
  BRIDGE_EVENT_VERSION,
  CANVAS_EVENT_VERSION,
  EVENT_VERSION
} from './kernel/projector.mjs';
import {
  OPERATIONS_V1_EVENT_VERSION,
  OPERATIONS_V1_LIMITS
} from './kernel/operations-contracts.mjs';
import { createOperationsService } from './kernel/operations.mjs';
import { loadModuleManifests } from './kernel/registry.mjs';
import { getSchemaValidators } from './kernel/schema-validation.mjs';
import { createProjectionStore } from './kernel/storage.mjs';
import { describeOpenRouterAdapter } from './adapters/openrouter.mjs';
import {
  createDryRunReceipt,
  localOperatorAction,
  normalizeRejectionReason,
  prepareDryRunEnvelope,
  proposeDryRunApproval,
  rejectDryRunEnvelope
} from './envelopes/dry-run-envelope.mjs';
import {
  authorizeBridgeEnvelope,
  claimBridgeEnvelope,
  clearBridgeTarget,
  interruptBridgeClaim,
  isBridgeGrantProfile,
  prepareBridgeEnvelope,
  recordBridgeResult,
  revokeBridgeAuthorization,
  releaseBridgeClaim,
  selectBridgeTarget
} from './envelopes/manual-session-bridge.mjs';

const PROJECT_ROOT = path.resolve(fileURLToPath(new URL('..', import.meta.url)));

function invalidCraftIndex(message) {
  const error = new Error(message);
  error.code = 'craft_index_invalid';
  return error;
}

function validateCraftIndex(index) {
  if (!index || index.schema_version !== '1'
    || index.source?.ledger_path !== '.craft/ledger.yml'
    || !/^[a-f0-9]{64}$/.test(index.source?.sha256 || '')
    || !index.scope?.context_id
    || !index.counts
    || !Array.isArray(index.next_moves)
    || !Array.isArray(index.pending)) {
    throw invalidCraftIndex('Craft index does not match the frontier contract');
  }
  return index;
}

async function readCraftFrontier(craftDir) {
  let ledger;
  let indexSource;
  try {
    [ledger, indexSource] = await Promise.all([
      readFile(path.join(craftDir, 'ledger.yml')),
      readFile(path.join(craftDir, 'index.json'), 'utf8')
    ]);
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
    const unavailable = new Error('Craft ledger or machine index is unavailable');
    unavailable.code = 'craft_frontier_unavailable';
    throw unavailable;
  }

  let index;
  try {
    index = validateCraftIndex(JSON.parse(indexSource));
  } catch (error) {
    if (error.code === 'craft_index_invalid') throw error;
    throw invalidCraftIndex('Craft index must be valid JSON');
  }

  const ledgerSha256 = createHash('sha256').update(ledger).digest('hex');
  if (ledgerSha256 !== index.source.sha256) {
    const stale = new Error('Craft index is stale; regenerate it from .craft/ledger.yml');
    stale.code = 'craft_index_stale';
    throw stale;
  }

  return {
    ...index,
    source: { ...index.source, verified: true }
  };
}

function createMutationQueue() {
  let tail = Promise.resolve();

  return (operation) => {
    const result = tail.then(operation, operation);
    tail = result.then(() => undefined, () => undefined);
    return result;
  };
}

async function readBody(request, maxBytes = Number.POSITIVE_INFINITY) {
  const chunks = [];
  let byteLength = 0;
  for await (const chunk of request) {
    byteLength += chunk.byteLength;
    if (byteLength > maxBytes) {
      const error = new Error(`request body exceeds ${maxBytes} bytes`);
      error.code = 'request_too_large';
      throw error;
    }
    chunks.push(chunk);
  }
  const raw = Buffer.concat(chunks).toString('utf8');
  if (!raw.trim()) return {};

  try {
    return JSON.parse(raw);
  } catch {
    const error = new Error('request body must be valid JSON');
    error.code = 'invalid_json';
    throw error;
  }
}

function invalidRequest(error) {
  return {
    error: 'invalid_request',
    schema_name: error.schema_name,
    validation_errors: error.validation_errors
  };
}

function createEvent(eventType, createdAt, records, eventVersion = EVENT_VERSION) {
  return {
    event_version: eventVersion,
    event_id: `event-${Date.now()}-${randomUUID()}`,
    event_type: eventType,
    ...records,
    created_at: createdAt
  };
}

function eventValidationOptions(schemas) {
  return {
    validateEvent(event, index) {
      try {
        if (event.event_type === 'envelope.prepared') {
          schemas.assert('agent-envelope', event.envelope, `event ${index + 1} envelope`);
          schemas.assert('approval-record', event.approval, `event ${index + 1} approval`);
        } else if (event.event_type === 'receipt.appended' || event.event_type === 'approval.granted') {
          schemas.assert('agent-envelope', event.envelope, `event ${index + 1} envelope`);
          schemas.assert('approval-record', event.approval, `event ${index + 1} approval`);
          schemas.assert('receipt', event.receipt, `event ${index + 1} receipt`);
        } else if (event.event_type === 'approval.rejected' || event.event_type === 'approval.revoked') {
          schemas.assert('agent-envelope', event.envelope, `event ${index + 1} envelope`);
          schemas.assert('approval-record', event.approval, `event ${index + 1} approval`);
        } else if (['bridge.target_selected', 'bridge.target_cleared'].includes(event.event_type)) {
          schemas.assert('agent-envelope', event.envelope, `event ${index + 1} envelope`);
          schemas.assert('bridge-target-request', {
            schema_version: '2',
            action: event.event_type === 'bridge.target_selected' ? 'ready' : 'unready',
            envelope_id: event.envelope.envelope_id,
            approval_id: event.approval_id,
            actor: event.actor
          }, `event ${index + 1} target`);
        } else if (event.event_type === 'bridge.claimed') {
          schemas.assert('agent-envelope', event.envelope, `event ${index + 1} envelope`);
          schemas.assert('bridge-claim-request', {
            schema_version: '2',
            envelope_id: event.claim.envelope_id,
            agent_ref: event.claim.agent_ref,
            session_ref: event.claim.session_ref,
            assurance: event.claim.assurance
          }, `event ${index + 1} claim`);
        } else if (event.event_type === 'bridge.interrupted') {
          schemas.assert('agent-envelope', event.envelope, `event ${index + 1} envelope`);
          schemas.assert('bridge-interrupt-request', {
            schema_version: '2',
            claim_id: event.claim.claim_id,
            envelope_id: event.claim.envelope_id,
            session_ref: event.claim.session_ref,
            assurance: event.claim.assurance,
            reason: event.reason
          }, `event ${index + 1} interrupt`);
        } else if (event.event_type === 'bridge.claim_released') {
          schemas.assert('agent-envelope', event.envelope, `event ${index + 1} envelope`);
          schemas.assert('bridge-release-request', {
            schema_version: '2',
            action: 'release_and_requeue',
            claim_id: event.claim.claim_id,
            envelope_id: event.claim.envelope_id,
            approval_id: event.claim.approval_id,
            actor: event.actor,
            reason: event.reason
          }, `event ${index + 1} release`);
        } else if (event.event_type === 'bridge.result_recorded') {
          schemas.assert('agent-envelope', event.envelope, `event ${index + 1} envelope`);
          schemas.assert('approval-record', event.approval, `event ${index + 1} approval`);
          schemas.assert('receipt', event.receipt, `event ${index + 1} receipt`);
          const { result_id: ignoredResultId, result_at: ignoredResultAt, ...requestResult } = event.result;
          void ignoredResultId;
          void ignoredResultAt;
          schemas.assert('bridge-result-request', requestResult, `event ${index + 1} result`);
        } else if (event.event_type === 'canvas.surface_published') {
          schemas.assert('canvas-publish-request', {
            schema_version: '1',
            path: event.surface.path,
            title: event.surface.title,
            kind: event.surface.kind
          }, `event ${index + 1} canvas publish`);
        } else if (event.event_version === CANVAS_EVENT_VERSION
          && event.event_type === 'canvas.interaction_recorded') {
          schemas.assert('canvas-interaction-request', {
            schema_version: '1',
            surface_id: event.interaction.surface_id,
            revision_id: event.interaction.revision_id,
            event_name: event.interaction.event_name,
            payload: event.interaction.payload
          }, `event ${index + 1} canvas interaction`);
        } else if (event.event_version === OPERATIONS_V1_EVENT_VERSION
          && event.event_type === 'canvas.interaction_recorded') {
          schemas.assert('operations-interaction-request', {
            schema_version: '1',
            operations_surface_id: event.interaction.operations_surface_id,
            revision_id: event.interaction.revision_id,
            event_name: event.interaction.event_name,
            payload: event.interaction.payload
          }, `event ${index + 1} Operations interaction`);
        }
      } catch (error) {
        if (error.code !== 'schema_validation_failed') throw error;
        const historyError = new Error(`event ${index + 1}: ${error.message}`);
        historyError.code = 'invalid_event_history';
        historyError.event_index = index;
        historyError.schema_name = error.schema_name;
        historyError.validation_errors = error.validation_errors;
        throw historyError;
      }
    }
  };
}

function reconciliationRequired(error) {
  return {
    status: 503,
    body: {
      error: 'reconciliation_required',
      event_id: error.event_id,
      recoverable: true
    }
  };
}

function evidenceLinks(receipt) {
  const base = `/api/receipts/${encodeURIComponent(receipt.receipt_id)}/evidence`;
  const links = {
    before: `${base}/before`,
    after: `${base}/after`,
    receipt: `${base}/receipt`
  };
  if (receipt.receipt_kind === 'skill.execution') links.result = `${base}/result`;
  return links;
}

function projectReceiptForUi(receipt) {
  const { before_ref: ignoredBeforeRef, after_ref: ignoredAfterRef, ...safeReceipt } = receipt;
  void ignoredBeforeRef;
  void ignoredAfterRef;
  return {
    ...safeReceipt,
    evidence: evidenceLinks(receipt)
  };
}

function proposalDetail(projection, envelopeId) {
  const envelope = projection.envelopes[envelopeId];
  if (!envelope) return null;
  const approval = projection.approvals[envelope.approval.approval_id] || null;
  const receiptIds = new Set(envelope.receipts);
  const receipts = projection.receipts
    .filter((receipt) => receiptIds.has(receipt.receipt_id))
    .map(projectReceiptForUi);
  const claims = (projection.bridge?.claim_order || [])
    .map((claimId) => projection.bridge.claims[claimId])
    .filter((claim) => claim?.envelope_id === envelopeId);
  const activeClaim = envelope.claim_id
    ? projection.bridge?.claims[envelope.claim_id] || null
    : claims.at(-1) || null;
  const result = envelope.result_id
    ? projection.bridge?.results[envelope.result_id] || null
    : activeClaim?.result_id
      ? projection.bridge?.results[activeClaim.result_id] || null
      : null;
  return { envelope, approval, receipts, claims, active_claim: activeClaim, result };
}

function projectArtifactForUi(artifact) {
  const projection = {
    artifact_version: artifact.artifact_version,
    kind: artifact.kind,
    run_id: artifact.run_id,
    envelope_id: artifact.envelope_id,
    approval_id: artifact.approval_id,
    requested_grants: artifact.requested_grants,
    requested_skill: artifact.requested_skill,
    disposition: artifact.disposition || null,
    state: artifact.state || null,
    created_at: artifact.created_at
  };
  if (artifact.envelope) projection.envelope = artifact.envelope;
  if (artifact.approval) projection.approval = artifact.approval;
  if (artifact.receipt) projection.receipt = projectReceiptForUi(artifact.receipt);
  if (artifact.claim) projection.claim = artifact.claim;
  if (artifact.result) projection.result = artifact.result;
  if (artifact.evidence_refs) projection.evidence_refs = artifact.evidence_refs;
  return projection;
}

function projectReadyRequest(envelope, selectedAt = null) {
  return {
    schema_version: '2',
    request_handle: envelope.envelope_id,
    agent_ref: envelope.agent_ref,
    state: envelope.state,
    effect_profile: 'preview.read',
    assurance: 'unattested',
    created_at: envelope.created_at,
    authorized_at: envelope.approval.approved_at,
    selected_at: selectedAt
  };
}

async function commitBridgeAuthorization(options) {
  const {
    state,
    envelope,
    approval,
    runtime,
    persistence,
    artifactDir,
    evidenceRoot
  } = options;
  const artifactIds = evidenceArtifactIds({
    run_id: envelope.run_id,
    approval_id: approval.approval_id
  });
  const beforeRef = artifactRefFor(artifactDir, artifactIds.before);
  const afterRef = artifactRefFor(artifactDir, artifactIds.after);
  const receiptRef = artifactRefFor(artifactDir, artifactIds.receipt);
  const authorized = authorizeBridgeEnvelope(envelope, approval);
  runtime.schemas.assert('agent-envelope', authorized.envelope, 'authorized bridge envelope');
  runtime.schemas.assert('approval-record', authorized.approval, 'authorized bridge approval');
  runtime.schemas.assert('receipt', authorized.receipt, 'authorization receipt');
  await validateEvidenceRefs(evidenceRoot, state.evidence_refs);

  const artifactBindings = {
    run_id: envelope.run_id,
    envelope_id: envelope.envelope_id,
    approval_id: approval.approval_id,
    requested_grants: envelope.requested_grants,
    requested_skill: envelope.requested_skill
  };
  const beforeArtifact = {
    artifact_version: 2,
    kind: 'approval.before',
    ...artifactBindings,
    state: envelope.state,
    envelope,
    approval,
    created_at: authorized.created_at
  };
  const afterArtifact = {
    artifact_version: 2,
    kind: 'approval.after',
    ...artifactBindings,
    disposition: 'authorized',
    state: authorized.envelope.state,
    envelope: authorized.envelope,
    approval: authorized.approval,
    created_at: authorized.created_at
  };
  const receiptArtifact = {
    artifact_version: 2,
    kind: 'approval.receipt',
    ...artifactBindings,
    disposition: 'authorized',
    evidence_refs: state.evidence_refs,
    receipt: authorized.receipt,
    created_at: authorized.created_at
  };

  await writeArtifactRef(artifactDir, artifactIds.before, beforeArtifact);
  await validateArtifactRef(artifactDir, beforeRef, {
    kind: 'approval.before',
    ...artifactBindings,
    envelope,
    approval
  });
  await writeArtifactRef(artifactDir, artifactIds.after, afterArtifact);
  await validateArtifactRef(artifactDir, afterRef, {
    kind: 'approval.after',
    ...artifactBindings,
    disposition: 'authorized',
    envelope: authorized.envelope,
    approval: authorized.approval
  });
  await writeArtifactRef(artifactDir, artifactIds.receipt, receiptArtifact);
  await validateArtifactRef(artifactDir, receiptRef, {
    kind: 'approval.receipt',
    ...artifactBindings,
    disposition: 'authorized',
    receipt: authorized.receipt
  });

  const event = createEvent('approval.granted', authorized.created_at, {
    envelope: authorized.envelope,
    approval: authorized.approval,
    receipt: authorized.receipt,
    artifact_refs: [beforeRef, afterRef, receiptRef]
  }, BRIDGE_EVENT_VERSION);

  try {
    await persistence.commitEvent(event, runtime.reduceOptions);
  } catch (error) {
    if (error.code === 'reconciliation_required') return reconciliationRequired(error);
    throw error;
  }

  return {
    status: 201,
    body: {
      envelope: authorized.envelope,
      approval: authorized.approval,
      receipt: authorized.receipt,
      artifact_ref: receiptRef,
      artifact_refs: {
        before: beforeRef,
        after: afterRef,
        receipt: receiptRef
      }
    }
  };
}

function sendJson(response, status, value) {
  response.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'cache-control': 'no-store'
  });
  response.end(`${JSON.stringify(value, null, 2)}\n`);
}

function sendText(response, status, value, contentType = 'text/plain; charset=utf-8') {
  response.writeHead(status, {
    'content-type': contentType,
    'cache-control': 'no-store'
  });
  response.end(value);
}

async function serveFile(response, file, contentType) {
  try {
    sendText(response, 200, await readFile(file, 'utf8'), contentType);
  } catch (error) {
    if (error.code === 'ENOENT') {
      sendText(response, 404, 'not found');
      return;
    }
    throw error;
  }
}

export function createServer(options = {}) {
  const rootDir = options.rootDir || PROJECT_ROOT;
  const stateDir = options.stateDir || path.join(rootDir, '.ide-extension/state');
  const modulesDir = options.modulesDir || path.join(rootDir, 'src/modules');
  const publicDir = options.publicDir || path.join(rootDir, 'public');
  const craftDir = options.craftDir || path.join(rootDir, '.craft');
  const evidenceRoot = options.evidenceRoot || path.resolve(rootDir, '../..');
  const workspaceRoot = options.workspaceRoot || evidenceRoot;
  const workbenchFile = path.join(stateDir, 'workbench.json');
  const eventsFile = path.join(stateDir, 'events.jsonl');
  const artifactDir = path.join(stateDir, 'artifacts');
  const mutate = createMutationQueue();
  const canvasNotifications = createCanvasNotificationHub();
  const canvasBlobStore = options.canvasBlobStore || createCanvasBlobStore({ stateDir });
  const persistence = createProjectionStore({
    workbenchFile,
    eventsFile,
    artifactDir,
    canvasBlobStore,
    append: options.appendEvent,
    writeProjection: options.writeProjection
  });
  const operations = createOperationsService({
    workspaceRoot,
    blobStore: canvasBlobStore,
    persistence,
    now: options.operationsNow,
    randomId: options.operationsRandomId
  });
  const canvasNavigation = createCanvasNavigationService({
    workspaceRoot,
    blobStore: canvasBlobStore,
    persistence,
    now: options.navigationNow,
    randomId: options.navigationRandomId,
    retentionMs: options.navigationRetentionMs,
    maxCommands: options.navigationMaxCommands
  });
  const canvasRetention = createCanvasRetentionService({
    blobStore: canvasBlobStore,
    persistence,
    policy: options.retentionPolicy,
    now: options.retentionNow,
    randomId: options.retentionRandomId,
    setTimer: options.retentionSetTimeout,
    clearTimer: options.retentionClearTimeout,
    runSerialized: mutate,
    onAutomaticResult: publishAutomaticRetention
  });
  function publishAutomaticRetention(result) {
    if (result?.notification) canvasNotifications.broadcast(result.notification);
  }
  async function evaluateAutomaticRetention(reduceOptions, source) {
    const result = await canvasRetention.evaluateAutomatic(reduceOptions, { source });
    publishAutomaticRetention(result);
    return result;
  }
  const ready = Promise.all([
    getSchemaValidators(),
    loadModuleManifests(modulesDir)
  ]).then(async ([schemas, modules]) => {
    const reduceOptions = eventValidationOptions(schemas);
    const reconciliation = await persistence.reconcile(reduceOptions);
    const automaticRetention = await mutate(
      () => evaluateAutomaticRetention(reduceOptions, 'startup')
    );
    return { schemas, modules, reduceOptions, reconciliation, automaticRetention };
  });

  const server = http.createServer(async (request, response) => {
    try {
      const url = new URL(request.url, 'http://127.0.0.1');
      const runtime = await ready;

      if (request.method === 'GET' && url.pathname === '/') {
        response.writeHead(302, { location: '/demo/l0' });
        response.end();
        return;
      }

      if (request.method === 'GET' && url.pathname === '/demo/l0') {
        await serveFile(response, path.join(publicDir, 'demo/l0.html'), 'text/html; charset=utf-8');
        return;
      }

      if (request.method === 'GET' && url.pathname === '/assets/cyber-alchemy-logo.svg') {
        await serveFile(
          response,
          path.join(publicDir, 'assets/cyber-alchemy-logo.svg'),
          'image/svg+xml; charset=utf-8'
        );
        return;
      }

      if (request.method === 'GET' && url.pathname === '/api/state') {
        const snapshot = await persistence.reconcile(runtime.reduceOptions);
        sendJson(response, 200, {
          ...snapshot.projection,
          modules: runtime.modules,
          provider_adapters: [describeOpenRouterAdapter()],
          event_count: snapshot.event_count,
          projection_checksum: snapshot.projection_checksum,
          reconciliation: {
            repaired: snapshot.repaired,
            orphan_artifacts: snapshot.orphan_artifacts,
            canvas_blobs: snapshot.canvas_blobs
          }
        });
        return;
      }

      if (request.method === 'GET' && url.pathname === '/api/craft/frontier') {
        try {
          sendJson(response, 200, await readCraftFrontier(craftDir));
        } catch (error) {
          const statuses = {
            craft_frontier_unavailable: 404,
            craft_index_stale: 409,
            craft_index_invalid: 500
          };
          if (!statuses[error.code]) throw error;
          sendJson(response, statuses[error.code], {
            error: error.code,
            message: error.message
          });
        }
        return;
      }

      if (request.method === 'GET' && url.pathname === '/api/canvas/current') {
        const { projection } = await persistence.reconcile(runtime.reduceOptions);
        sendJson(response, 200, projectCurrentCanvas(projection));
        return;
      }

      if (request.method === 'GET' && url.pathname === '/api/canvas/display') {
        try {
          sendJson(response, 200, await canvasNavigation.getDisplay(runtime.reduceOptions));
        } catch (error) {
          const statuses = {
            navigation_target_not_found: 404,
            navigation_target_pruned: 410,
            navigation_target_unavailable: 409
          };
          if (!statuses[error.code]) throw error;
          sendJson(response, statuses[error.code], {
            error: error.code,
            message: error.message,
            reason: error.reason || null,
            tombstone: error.tombstone || null
          });
        }
        return;
      }

      if (request.method === 'GET' && url.pathname === '/api/canvas/storage') {
        const result = await mutate(async () => {
          try {
            return await canvasRetention.inspect(runtime.reduceOptions);
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            throw error;
          }
        });
        if (result.notification) canvasNotifications.broadcast(result.notification);
        if (result.status) sendJson(response, result.status, result.body);
        else sendJson(response, 200, { storage: result.storage });
        return;
      }

      if (request.method === 'POST' && url.pathname === '/api/canvas/pruning/preview') {
        const body = await readBody(request, OPERATIONS_V1_LIMITS.http_request_bytes);
        try {
          runtime.schemas.assert(
            'canvas-pruning-preview-request',
            body,
            'POST canvas pruning preview'
          );
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }
        const result = await mutate(async () => {
          try {
            return { status: 200, body: await canvasRetention.preview(body, runtime.reduceOptions) };
          } catch (error) {
            const statuses = {
              pruning_command_conflict: 409,
              pruning_request_not_active: 409
            };
            if (!statuses[error.code]) throw error;
            return {
              status: statuses[error.code],
              body: { error: error.code, message: error.message, command_id: body.command_id }
            };
          }
        });
        sendJson(response, result.status, result.body);
        return;
      }

      if (request.method === 'POST' && url.pathname === '/api/canvas/pruning/commit') {
        const body = await readBody(request, OPERATIONS_V1_LIMITS.http_request_bytes);
        try {
          runtime.schemas.assert(
            'canvas-pruning-commit-request',
            body,
            'POST canvas pruning commit'
          );
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }
        const result = await mutate(async () => {
          try {
            const committed = await canvasRetention.commit(body, runtime.reduceOptions);
            if (!committed.idempotent) {
              await evaluateAutomaticRetention(runtime.reduceOptions, 'post_prune_commit');
            }
            const { notification, ...responseBody } = committed;
            return {
              status: committed.idempotent ? 200 : 201,
              body: responseBody,
              notification
            };
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            const statuses = {
              pruning_command_conflict: 409,
              pruning_request_not_active: 409,
              pruning_candidate_changed: 409,
              pruning_no_candidates: 409,
              retention_blob_delete_failed: 503
            };
            if (!statuses[error.code]) throw error;
            return {
              status: statuses[error.code],
              body: {
                error: error.code,
                message: error.message,
                command_id: body.command_id,
                expected_candidate_digest: error.expected_candidate_digest || null,
                actual_candidate_digest: error.actual_candidate_digest || null,
                blocked_reason: error.blocked_reason || null,
                cause_code: error.cause_code || null,
                tombstone_committed: error.tombstone_committed || false,
                pruned_revisions: error.pruned_revisions || []
              }
            };
          }
        });
        if (result.notification) canvasNotifications.broadcast(result.notification);
        sendJson(response, result.status, result.body);
        return;
      }

      if (request.method === 'POST' && url.pathname === '/api/canvas/navigation') {
        const body = await readBody(request, OPERATIONS_V1_LIMITS.http_request_bytes);
        try {
          runtime.schemas.assert('canvas-navigation-request', body, 'POST canvas navigation');
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }
        const result = await mutate(async () => {
          try {
            const navigated = await canvasNavigation.navigate(body, runtime.reduceOptions);
            const { notification, ...responseBody } = navigated;
            return {
              status: navigated.idempotent ? 200 : 201,
              body: responseBody,
              notification
            };
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            const statuses = {
              navigation_command_conflict: 409,
              navigation_target_not_found: 404,
              navigation_target_pruned: 410,
              navigation_target_unavailable: 409,
              display_target_not_found: 409
            };
            if (!statuses[error.code]) throw error;
            return {
              status: statuses[error.code],
              body: {
                error: error.code,
                message: error.message,
                command_id: error.command_id || null,
                reason: error.reason || null,
                tombstone: error.tombstone || null
              }
            };
          }
        });
        if (result.notification) canvasNotifications.broadcast(result.notification);
        sendJson(response, result.status, result.body);
        return;
      }

      const navigationStatusMatch = url.pathname.match(/^\/api\/canvas\/navigation\/([^/]+)$/);
      if (request.method === 'GET' && navigationStatusMatch) {
        try {
          sendJson(response, 200, canvasNavigation.getStatus(
            decodeURIComponent(navigationStatusMatch[1])
          ));
        } catch (error) {
          if (error.code !== 'navigation_command_not_found') throw error;
          sendJson(response, 404, { error: error.code, command_id: error.command_id });
        }
        return;
      }

      const navigationAckMatch = url.pathname.match(
        /^\/api\/canvas\/navigation\/([^/]+)\/ack$/
      );
      if (request.method === 'POST' && navigationAckMatch) {
        const body = await readBody(request, OPERATIONS_V1_LIMITS.http_request_bytes);
        try {
          runtime.schemas.assert(
            'canvas-navigation-ack-request',
            body,
            'POST canvas navigation acknowledgement'
          );
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }
        try {
          sendJson(response, 200, canvasNavigation.acknowledge(
            decodeURIComponent(navigationAckMatch[1]),
            body
          ));
        } catch (error) {
          if (error.code !== 'navigation_command_not_found') throw error;
          sendJson(response, 404, { error: error.code, command_id: error.command_id });
        }
        return;
      }

      if (request.method === 'POST' && url.pathname === '/api/canvas/operation-surfaces') {
        const body = await readBody(request, OPERATIONS_V1_LIMITS.http_request_bytes);
        try {
          runtime.schemas.assert(
            'operations-surface-derive-request',
            body,
            'POST Operations surface derivation'
          );
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }

        const result = await mutate(async () => {
          try {
            const derived = await operations.derive(body, runtime.reduceOptions);
            if (!derived.idempotent) {
              await evaluateAutomaticRetention(runtime.reduceOptions, 'post_blob_commit');
            }
            return { status: derived.idempotent ? 200 : 201, body: derived };
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            if (['source_revision_unavailable', 'derivation_key_conflict'].includes(error.code)) {
              return {
                status: 409,
                body: {
                  error: error.code,
                  message: error.message,
                  reason: error.reason || null,
                  source_v0_surface_id: error.source_v0_surface_id || null,
                  source_revision_id: error.source_revision_id || null
                }
              };
            }
            throw error;
          }
        });
        sendJson(response, result.status, result.body);
        return;
      }

      const operationsSurfaceMatch = url.pathname.match(
        /^\/api\/canvas\/operation-surfaces\/([^/]+)$/
      );
      if (request.method === 'GET' && operationsSurfaceMatch) {
        const surfaceId = decodeURIComponent(operationsSurfaceMatch[1]);
        try {
          sendJson(response, 200, await operations.getSurface(surfaceId, runtime.reduceOptions));
        } catch (error) {
          if (error.code === 'operations_surface_not_found') {
            sendJson(response, 404, { error: error.code });
            return;
          }
          throw error;
        }
        return;
      }

      const operationsMutationMatch = url.pathname.match(
        /^\/api\/canvas\/operation-surfaces\/([^/]+)\/operations$/
      );
      if (request.method === 'POST' && operationsMutationMatch) {
        const surfaceId = decodeURIComponent(operationsMutationMatch[1]);
        const body = await readBody(request, OPERATIONS_V1_LIMITS.http_request_bytes);
        try {
          runtime.schemas.assert(
            'content-operation-request',
            body,
            'POST Operations content operation'
          );
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }
        if (body.operations_surface_id !== surfaceId) {
          sendJson(response, 409, { error: 'operations_surface_binding_mismatch' });
          return;
        }

        const result = await mutate(async () => {
          try {
            const operated = await operations.operate(body, runtime.reduceOptions);
            if (!operated.idempotent) {
              await evaluateAutomaticRetention(runtime.reduceOptions, 'post_blob_commit');
            }
            const { notification, ...responseBody } = operated;
            return {
              status: operated.idempotent ? 200 : 201,
              body: responseBody,
              notification
            };
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            const statuses = {
              operations_surface_not_found: 404,
              operation_id_conflict: 409,
              revision_changed: 409,
              operation_mode_unavailable: 409,
              rebuild_source_unavailable: 409,
              rebuild_source_changed: 409,
              operations_byte_limit_exceeded: 413,
              operations_transform_invalid_input: 400,
              operations_transform_invalid_document: 422,
              operations_source_invalid_utf8: 422
            };
            if (!statuses[error.code]) throw error;
            return {
              status: statuses[error.code],
              body: {
                error: error.code,
                message: error.message,
                operation_id: error.operation_id || null,
                mode: error.mode || null,
                expected_revision_id: error.expected_revision_id || null,
                current_revision_id: error.current_revision_id || null,
                limit_name: error.limit_name || null,
                max_bytes: error.max_bytes || null,
                actual_bytes: error.actual_bytes || null,
                reason: error.reason || null,
                expected_sha256: error.expected_sha256 || null,
                actual_sha256: error.actual_sha256 || null
              }
            };
          }
        });
        if (result.notification) canvasNotifications.broadcast(result.notification);
        sendJson(response, result.status, result.body);
        return;
      }

      const operationsContentMatch = url.pathname.match(
        /^\/api\/canvas\/operation-surfaces\/([^/]+)\/revisions\/([^/]+)\/content$/
      );
      if (request.method === 'GET' && operationsContentMatch) {
        const surfaceId = decodeURIComponent(operationsContentMatch[1]);
        const revisionId = decodeURIComponent(operationsContentMatch[2]);
        try {
          const content = await operations.getContent(
            surfaceId,
            revisionId,
            runtime.reduceOptions
          );
          sendText(response, 200, content.bytes, 'text/html; charset=utf-8');
        } catch (error) {
          if (error.code === 'operations_revision_not_found') {
            sendJson(response, 404, { error: error.code });
            return;
          }
          if (error.code === 'revision_pruned') {
            sendJson(response, 410, { error: error.code, tombstone: error.tombstone });
            return;
          }
          throw error;
        }
        return;
      }

      const operationsInteractionMatch = url.pathname.match(
        /^\/api\/canvas\/operation-surfaces\/([^/]+)\/events$/
      );
      if (request.method === 'POST' && operationsInteractionMatch) {
        const surfaceId = decodeURIComponent(operationsInteractionMatch[1]);
        const body = await readBody(request, 16 * 1024);
        try {
          runtime.schemas.assert(
            'operations-interaction-request',
            body,
            'POST Operations canvas interaction'
          );
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }
        if (body.operations_surface_id !== surfaceId) {
          sendJson(response, 409, { error: 'operations_surface_binding_mismatch' });
          return;
        }

        const result = await mutate(async () => {
          const { projection } = await persistence.reconcile(runtime.reduceOptions);
          const operationsState = projection.canvas?.operations_v1;
          const display = operationsState?.display_target;
          if (display?.surface_kind !== 'operations_v1'
            || display.surface_id !== body.operations_surface_id
            || display.revision_id !== body.revision_id) {
            return { status: 409, body: { error: 'stale_canvas_revision' } };
          }
          const receivedAt = new Date().toISOString();
          const event = createEvent('canvas.interaction_recorded', receivedAt, {
            interaction: null
          }, OPERATIONS_V1_EVENT_VERSION);
          event.interaction = {
            event_id: event.event_id,
            cursor: operationsState.interaction_cursor + 1,
            operations_surface_id: body.operations_surface_id,
            revision_id: body.revision_id,
            event_name: body.event_name,
            payload: body.payload,
            received_at: receivedAt
          };
          try {
            await persistence.commitEvent(event, runtime.reduceOptions);
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            throw error;
          }
          return { status: 201, body: { interaction: event.interaction } };
        });
        sendJson(response, result.status, result.body);
        return;
      }

      if (request.method === 'GET' && url.pathname === '/api/canvas/notifications') {
        const { projection } = await persistence.reconcile(runtime.reduceOptions);
        const display = canvasNavigation.projectDisplay(projection).display;
        canvasNotifications.register(response, display);
        return;
      }

      if (request.method === 'GET' && url.pathname === '/api/canvas/events') {
        const afterValues = url.searchParams.getAll('after');
        const rawAfter = afterValues.length === 0 ? '0' : afterValues[0];
        if (afterValues.length > 1 || !/^(0|[1-9][0-9]*)$/.test(rawAfter)
          || !Number.isSafeInteger(Number(rawAfter))) {
          sendJson(response, 400, { error: 'invalid_cursor' });
          return;
        }
        const after = Number(rawAfter);
        const { projection } = await persistence.reconcile(runtime.reduceOptions);
        const interactions = projection.canvas?.interactions || [];
        const interactionCursor = projection.canvas?.interaction_cursor || 0;
        sendJson(response, 200, {
          schema_version: '1',
          events: interactions.filter((interaction) => interaction.cursor > after),
          next_cursor: Math.max(after, interactionCursor)
        });
        return;
      }

      if (request.method === 'POST' && url.pathname === '/api/canvas/events') {
        const body = await readBody(request, 16 * 1024);
        try {
          runtime.schemas.assert('canvas-interaction-request', body, 'POST canvas interaction');
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }

        const result = await mutate(async () => {
          const { projection } = await persistence.reconcile(runtime.reduceOptions);
          const current = projectCurrentCanvas(projection).current;
          if (!current || current.surface_id !== body.surface_id
            || current.revision.revision_id !== body.revision_id) {
            return { status: 409, body: { error: 'stale_canvas_revision' } };
          }
          const receivedAt = new Date().toISOString();
          const event = createEvent('canvas.interaction_recorded', receivedAt, {
            interaction: null
          }, CANVAS_EVENT_VERSION);
          event.interaction = {
            event_id: event.event_id,
            cursor: projection.canvas.interaction_cursor + 1,
            surface_id: body.surface_id,
            revision_id: body.revision_id,
            event_name: body.event_name,
            payload: body.payload,
            received_at: receivedAt
          };
          try {
            await persistence.commitEvent(event, runtime.reduceOptions);
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            throw error;
          }
          return { status: 201, body: { interaction: event.interaction } };
        });
        sendJson(response, result.status, result.body);
        return;
      }

      if (request.method === 'POST' && url.pathname === '/api/canvas/publish') {
        const body = await readBody(request);
        try {
          runtime.schemas.assert('canvas-publish-request', body, 'POST canvas publish');
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }

        let file;
        try {
          file = await readWorkspaceHtml(workspaceRoot, body.path);
        } catch (error) {
          const statuses = {
            invalid_canvas_path: 400,
            canvas_path_escape: 400,
            canvas_file_not_found: 404,
            canvas_not_file: 400
          };
          if (statuses[error.code]) {
            sendJson(response, statuses[error.code], { error: error.code, message: error.message });
            return;
          }
          throw error;
        }

        const result = await mutate(async () => {
          const { projection } = await persistence.reconcile(runtime.reduceOptions);
          const publication = prepareCanvasPublication(projection, body, file);
          if (publication.idempotent) {
            return {
              status: 200,
              body: { ...projectCurrentCanvas(projection), idempotent: true }
            };
          }
          const event = createEvent('canvas.surface_published', publication.published_at, {
            surface: publication.surface,
            revision: publication.revision
          }, CANVAS_EVENT_VERSION);
          try {
            const committed = await persistence.commitEvent(event, runtime.reduceOptions);
            const current = projectCurrentCanvas(committed.projection).current;
            return {
              status: 201,
              body: { current, idempotent: false },
              notification: current
            };
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            throw error;
          }
        });
        if (result.notification) canvasNotifications.broadcast(result.notification);
        sendJson(response, result.status, result.body);
        return;
      }

      const canvasContentMatch = url.pathname.match(
        /^\/api\/canvas\/surfaces\/([^/]+)\/revisions\/([^/]+)\/content$/
      );
      if (request.method === 'GET' && canvasContentMatch) {
        const surfaceId = decodeURIComponent(canvasContentMatch[1]);
        const revisionId = decodeURIComponent(canvasContentMatch[2]);
        const { projection } = await persistence.reconcile(runtime.reduceOptions);
        const surface = projection.canvas?.surfaces[surfaceId];
        const revision = projection.canvas?.revisions[revisionId];
        if (!surface || !revision || revision.surface_id !== surfaceId
          || !surface.revision_ids.includes(revisionId)) {
          sendJson(response, 404, { error: 'canvas_revision_not_found' });
          return;
        }
        let file;
        try {
          file = await readWorkspaceHtml(workspaceRoot, surface.path);
        } catch (error) {
          if (['canvas_file_not_found', 'canvas_not_file', 'canvas_path_escape'].includes(error.code)) {
            sendJson(response, 404, { error: 'canvas_file_unavailable' });
            return;
          }
          throw error;
        }
        if (file.content_sha256 !== revision.content_sha256) {
          sendJson(response, 409, {
            error: 'revision_changed',
            surface_id: surfaceId,
            revision_id: revisionId
          });
          return;
        }
        sendText(response, 200, file.bytes, 'text/html; charset=utf-8');
        return;
      }

      const proposalMatch = url.pathname.match(/^\/api\/proposals\/([^/]+)$/);
      if (request.method === 'GET' && proposalMatch) {
        const { projection } = await persistence.reconcile(runtime.reduceOptions);
        const detail = proposalDetail(projection, decodeURIComponent(proposalMatch[1]));
        if (!detail) {
          sendJson(response, 404, { error: 'proposal_not_found' });
          return;
        }
        sendJson(response, 200, detail);
        return;
      }

      if (request.method === 'GET' && url.pathname === '/api/bridge/requests/ready') {
        const { projection } = await persistence.reconcile(runtime.reduceOptions);
        const readyId = projection.bridge?.ready_target_envelope_id || null;
        if (!readyId) {
          sendJson(response, 200, { request: null });
          return;
        }
        const envelope = projection.envelopes[readyId];
        if (!envelope || envelope.state !== 'ready_for_poll') {
          sendJson(response, 409, { error: 'ready_target_inconsistent' });
          return;
        }
        sendJson(response, 200, {
          request: projectReadyRequest(
            envelope,
            projection.bridge.ready_target_selected_at
          )
        });
        return;
      }

      const targetMatch = url.pathname.match(
        /^\/api\/bridge\/requests\/([^/]+)\/(ready|unready)$/
      );
      if (request.method === 'POST' && targetMatch) {
        const envelopeId = decodeURIComponent(targetMatch[1]);
        const action = targetMatch[2];
        const body = await readBody(request);
        try {
          runtime.schemas.assert('approve-request', body, `POST bridge ${action}`);
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }

        const result = await mutate(async () => {
          const { projection: state } = await persistence.reconcile(runtime.reduceOptions);
          const envelope = state.envelopes[envelopeId];
          if (!envelope) return { status: 404, body: { error: 'envelope_not_found' } };
          if (envelope.schema_version !== '2') {
            return { status: 409, body: { error: 'not_bridge_request' } };
          }
          const approval = state.approvals[envelope.approval.approval_id];
          if (!approval || approval.state !== 'authorized') {
            return { status: 409, body: { error: 'authorization_not_active' } };
          }

          if (action === 'ready' && state.bridge?.ready_target_envelope_id) {
            return {
              status: 409,
              body: {
                error: 'ready_target_exists',
                request_handle: state.bridge.ready_target_envelope_id
              }
            };
          }
          if (action === 'unready'
            && state.bridge?.ready_target_envelope_id !== envelope.envelope_id) {
            return { status: 409, body: { error: 'not_ready_target' } };
          }

          let nextEnvelope;
          try {
            nextEnvelope = action === 'ready'
              ? selectBridgeTarget(envelope)
              : clearBridgeTarget(envelope);
          } catch (error) {
            if (['not_approved', 'not_ready'].includes(error.code)) {
              return { status: 409, body: { error: error.code } };
            }
            throw error;
          }
          const actor = localOperatorAction();
          runtime.schemas.assert('bridge-target-request', {
            schema_version: '2',
            action,
            envelope_id: envelope.envelope_id,
            approval_id: approval.approval_id,
            actor
          }, `bridge ${action} request`);
          runtime.schemas.assert('agent-envelope', nextEnvelope, `bridge ${action} envelope`);
          const createdAt = new Date().toISOString();
          const event = createEvent(
            action === 'ready' ? 'bridge.target_selected' : 'bridge.target_cleared',
            createdAt,
            {
              envelope: nextEnvelope,
              approval_id: approval.approval_id,
              actor
            },
            BRIDGE_EVENT_VERSION
          );

          try {
            await persistence.commitEvent(event, runtime.reduceOptions);
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            throw error;
          }

          return {
            status: action === 'ready' ? 201 : 200,
            body: {
              request: projectReadyRequest(
                nextEnvelope,
                action === 'ready' ? createdAt : null
              ),
              envelope: nextEnvelope
            }
          };
        });
        sendJson(response, result.status, result.body);
        return;
      }

      const claimMatch = url.pathname.match(/^\/api\/bridge\/requests\/([^/]+)\/claim$/);
      if (request.method === 'POST' && claimMatch) {
        const envelopeId = decodeURIComponent(claimMatch[1]);
        const body = await readBody(request);
        try {
          runtime.schemas.assert('bridge-claim-request', body, 'POST bridge claim');
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }
        if (body.envelope_id !== envelopeId) {
          sendJson(response, 409, { error: 'claim_binding_mismatch' });
          return;
        }

        const result = await mutate(async () => {
          const { projection: state } = await persistence.reconcile(runtime.reduceOptions);
          const envelope = state.envelopes[envelopeId];
          if (!envelope) return { status: 404, body: { error: 'envelope_not_found' } };
          if (envelope.state === 'claimed' || envelope.state === 'interrupted') {
            return { status: 409, body: { error: 'already_claimed' } };
          }
          if (state.bridge?.ready_target_envelope_id !== envelopeId) {
            return { status: 409, body: { error: 'not_ready_target' } };
          }
          const approval = state.approvals[envelope.approval.approval_id];
          if (!approval || approval.state !== 'authorized') {
            return { status: 409, body: { error: 'authorization_not_active' } };
          }

          const claimed = claimBridgeEnvelope(envelope, approval, body);
          runtime.schemas.assert('agent-envelope', claimed.envelope, 'claimed bridge envelope');
          const artifactIds = claimArtifactIds({
            run_id: envelope.run_id,
            claim_id: claimed.claim.claim_id
          });
          const claimRef = await writeArtifactRef(artifactDir, artifactIds.claim, {
            artifact_version: 2,
            kind: 'bridge.claim',
            run_id: envelope.run_id,
            envelope_id: envelope.envelope_id,
            approval_id: approval.approval_id,
            claim_id: claimed.claim.claim_id,
            claim_attempt_id: claimed.claim.claim_attempt_id,
            session_ref: claimed.claim.session_ref,
            assurance: claimed.claim.assurance,
            claim: claimed.claim,
            execution: {
              task: envelope.task,
              requested_skill: envelope.requested_skill,
              requested_grants: envelope.requested_grants,
              context_refs: envelope.context_refs
            },
            created_at: claimed.created_at
          });
          await validateArtifactRef(artifactDir, claimRef, {
            kind: 'bridge.claim',
            run_id: envelope.run_id,
            envelope_id: envelope.envelope_id,
            approval_id: approval.approval_id,
            claim_id: claimed.claim.claim_id,
            session_ref: claimed.claim.session_ref,
            assurance: 'unattested'
          });
          const event = createEvent('bridge.claimed', claimed.created_at, {
            envelope: claimed.envelope,
            claim: claimed.claim,
            artifact_refs: [claimRef]
          }, BRIDGE_EVENT_VERSION);
          try {
            await persistence.commitEvent(event, runtime.reduceOptions);
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            throw error;
          }
          return {
            status: 201,
            body: {
              claim: claimed.claim,
              execution: {
                task: envelope.task,
                requested_skill: envelope.requested_skill,
                requested_grants: envelope.requested_grants,
                context_refs: envelope.context_refs
              },
              artifact_ref: claimRef
            }
          };
        });
        sendJson(response, result.status, result.body);
        return;
      }

      const resultMatch = url.pathname.match(/^\/api\/bridge\/claims\/([^/]+)\/result$/);
      if (request.method === 'POST' && resultMatch) {
        const claimId = decodeURIComponent(resultMatch[1]);
        const body = await readBody(request);
        try {
          runtime.schemas.assert('bridge-result-request', body, 'POST bridge result');
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }
        if (body.claim_id !== claimId) {
          sendJson(response, 409, { error: 'result_binding_mismatch' });
          return;
        }

        const result = await mutate(async () => {
          const { projection: state } = await persistence.reconcile(runtime.reduceOptions);
          const claim = state.bridge?.claims[claimId];
          if (!claim) return { status: 404, body: { error: 'claim_not_found' } };
          if (claim.state !== 'claimed') {
            return { status: 409, body: { error: 'claim_not_active' } };
          }
          const envelope = state.envelopes[claim.envelope_id];
          const approval = state.approvals[claim.approval_id];
          const bindings = {
            claim_attempt_id: claim.claim_attempt_id,
            envelope_id: claim.envelope_id,
            run_id: claim.run_id,
            approval_id: claim.approval_id,
            session_ref: claim.session_ref,
            assurance: claim.assurance,
            requested_skill: envelope?.requested_skill
          };
          for (const [field, expected] of Object.entries(bindings)) {
            if (body[field] !== expected) {
              return { status: 409, body: { error: 'result_binding_mismatch', field } };
            }
          }
          if (!['passed', 'flagged', 'blocked'].includes(body.status)) {
            return { status: 409, body: { error: 'unsupported_result_status' } };
          }
          if (!envelope || envelope.state !== 'claimed'
            || !approval || approval.state !== 'authorized') {
            return { status: 409, body: { error: 'claim_not_active' } };
          }

          try {
            await validateEvidenceRefs(evidenceRoot, body.evidence_refs);
          } catch (error) {
            if (['invalid_evidence_refs', 'invalid_evidence_ref', 'evidence_path_escape',
              'evidence_not_found', 'evidence_root_not_found'].includes(error.code)) {
              return { status: 400, body: { error: error.code } };
            }
            throw error;
          }

          const claimIds = claimArtifactIds({ run_id: claim.run_id, claim_id: claim.claim_id });
          const beforeRef = artifactRefFor(artifactDir, claimIds.claim);
          try {
            await validateArtifactRef(artifactDir, beforeRef, {
              kind: 'bridge.claim',
              run_id: claim.run_id,
              envelope_id: claim.envelope_id,
              approval_id: claim.approval_id,
              claim_id: claim.claim_id,
              session_ref: claim.session_ref
            });
          } catch (error) {
            if (error.code?.startsWith('artifact_') || error.code === 'malformed_artifact') {
              return { status: 409, body: { error: 'claim_evidence_unavailable' } };
            }
            throw error;
          }

          const receiptId = `receipt-${randomUUID()}`;
          const resultId = `result-${randomUUID()}`;
          const resultAt = new Date().toISOString();
          const artifactIds = executionArtifactIds({
            run_id: claim.run_id,
            receipt_id: receiptId
          });
          const afterRef = artifactRefFor(artifactDir, artifactIds.after);
          const resultRef = artifactRefFor(artifactDir, artifactIds.result);
          const receiptRef = artifactRefFor(artifactDir, artifactIds.receipt);
          const admitted = recordBridgeResult(
            envelope,
            approval,
            claim,
            body,
            { before_ref: beforeRef, after_ref: afterRef, result_ref: resultRef },
            { receipt_id: receiptId, result_id: resultId, result_at: resultAt }
          );
          runtime.schemas.assert('agent-envelope', admitted.envelope, 'terminal bridge envelope');
          runtime.schemas.assert('approval-record', admitted.approval, 'consumed bridge approval');
          runtime.schemas.assert('receipt', admitted.receipt, 'execution receipt');

          const commonBindings = {
            run_id: claim.run_id,
            envelope_id: claim.envelope_id,
            approval_id: claim.approval_id,
            claim_id: claim.claim_id
          };
          await writeArtifactRef(artifactDir, artifactIds.result, {
            artifact_version: 2,
            kind: 'bridge.result',
            ...commonBindings,
            result: admitted.result,
            created_at: admitted.created_at
          });
          await validateArtifactRef(artifactDir, resultRef, {
            kind: 'bridge.result',
            ...commonBindings,
            result: admitted.result
          });
          await writeArtifactRef(artifactDir, artifactIds.after, {
            artifact_version: 2,
            kind: 'bridge.result.after',
            ...commonBindings,
            state: admitted.envelope.state,
            envelope: admitted.envelope,
            approval: admitted.approval,
            claim: admitted.claim,
            created_at: admitted.created_at
          });
          await validateArtifactRef(artifactDir, afterRef, {
            kind: 'bridge.result.after',
            ...commonBindings,
            envelope: admitted.envelope,
            approval: admitted.approval,
            claim: admitted.claim
          });
          await writeArtifactRef(artifactDir, artifactIds.receipt, {
            artifact_version: 2,
            kind: 'bridge.execution.receipt',
            ...commonBindings,
            receipt: admitted.receipt,
            created_at: admitted.created_at
          });
          await validateArtifactRef(artifactDir, receiptRef, {
            kind: 'bridge.execution.receipt',
            ...commonBindings,
            receipt: admitted.receipt
          });

          const event = createEvent('bridge.result_recorded', admitted.created_at, {
            envelope: admitted.envelope,
            approval: admitted.approval,
            claim: admitted.claim,
            result: admitted.result,
            receipt: admitted.receipt,
            artifact_refs: [beforeRef, afterRef, resultRef, receiptRef]
          }, BRIDGE_EVENT_VERSION);
          try {
            await persistence.commitEvent(event, runtime.reduceOptions);
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            throw error;
          }

          return {
            status: 201,
            body: {
              envelope: admitted.envelope,
              result: admitted.result,
              receipt: admitted.receipt,
              artifact_ref: receiptRef,
              artifact_refs: {
                before: beforeRef,
                after: afterRef,
                result: resultRef,
                receipt: receiptRef
              }
            }
          };
        });
        sendJson(response, result.status, result.body);
        return;
      }

      const claimStatusMatch = url.pathname.match(/^\/api\/bridge\/claims\/([^/]+)$/);
      if (request.method === 'GET' && claimStatusMatch) {
        const claimId = decodeURIComponent(claimStatusMatch[1]);
        const { projection } = await persistence.reconcile(runtime.reduceOptions);
        const claim = projection.bridge?.claims[claimId];
        if (!claim) {
          sendJson(response, 404, { error: 'claim_not_found' });
          return;
        }
        sendJson(response, 200, {
          claim,
          result: claim.result_id ? projection.bridge.results[claim.result_id] || null : null
        });
        return;
      }

      const interruptMatch = url.pathname.match(/^\/api\/bridge\/claims\/([^/]+)\/interrupt$/);
      if (request.method === 'POST' && interruptMatch) {
        const claimId = decodeURIComponent(interruptMatch[1]);
        const body = await readBody(request);
        try {
          runtime.schemas.assert('bridge-interrupt-request', body, 'POST bridge interrupt');
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }
        if (body.claim_id !== claimId) {
          sendJson(response, 409, { error: 'claim_binding_mismatch' });
          return;
        }

        const result = await mutate(async () => {
          const { projection: state } = await persistence.reconcile(runtime.reduceOptions);
          const claim = state.bridge?.claims[claimId];
          if (!claim) return { status: 404, body: { error: 'claim_not_found' } };
          if (claim.session_ref !== body.session_ref
            || claim.envelope_id !== body.envelope_id
            || claim.assurance !== body.assurance) {
            return { status: 409, body: { error: 'claim_binding_mismatch' } };
          }
          const envelope = state.envelopes[claim.envelope_id];
          let interrupted;
          try {
            interrupted = interruptBridgeClaim(envelope, claim, body.reason);
          } catch (error) {
            if (error.code === 'claim_not_active') {
              return { status: 409, body: { error: error.code } };
            }
            throw error;
          }
          runtime.schemas.assert('agent-envelope', interrupted.envelope, 'interrupted bridge envelope');
          const artifactIds = claimArtifactIds({ run_id: claim.run_id, claim_id: claim.claim_id });
          const interruptRef = await writeArtifactRef(artifactDir, artifactIds.interrupt, {
            artifact_version: 2,
            kind: 'bridge.interrupt',
            run_id: claim.run_id,
            envelope_id: claim.envelope_id,
            approval_id: claim.approval_id,
            claim_id: claim.claim_id,
            session_ref: claim.session_ref,
            assurance: claim.assurance,
            reason: interrupted.reason,
            created_at: interrupted.created_at
          });
          const event = createEvent('bridge.interrupted', interrupted.created_at, {
            envelope: interrupted.envelope,
            claim: interrupted.claim,
            reason: interrupted.reason,
            artifact_refs: [interruptRef]
          }, BRIDGE_EVENT_VERSION);
          try {
            await persistence.commitEvent(event, runtime.reduceOptions);
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            throw error;
          }
          return {
            status: 200,
            body: { envelope: interrupted.envelope, claim: interrupted.claim, artifact_ref: interruptRef }
          };
        });
        sendJson(response, result.status, result.body);
        return;
      }

      const releaseMatch = url.pathname.match(/^\/api\/bridge\/claims\/([^/]+)\/release$/);
      if (request.method === 'POST' && releaseMatch) {
        const claimId = decodeURIComponent(releaseMatch[1]);
        const body = await readBody(request);
        try {
          runtime.schemas.assert('reject-request', body, 'POST bridge release');
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }
        const reason = normalizeRejectionReason(body.reason);
        if (!reason) {
          sendJson(response, 400, { error: 'release_reason_required' });
          return;
        }

        const result = await mutate(async () => {
          const { projection: state } = await persistence.reconcile(runtime.reduceOptions);
          const claim = state.bridge?.claims[claimId];
          if (!claim) return { status: 404, body: { error: 'claim_not_found' } };
          const envelope = state.envelopes[claim.envelope_id];
          let released;
          try {
            released = releaseBridgeClaim(envelope, claim, reason);
          } catch (error) {
            if (error.code === 'claim_not_interrupted') {
              return { status: 409, body: { error: error.code } };
            }
            throw error;
          }
          runtime.schemas.assert('bridge-release-request', {
            schema_version: '2',
            action: 'release_and_requeue',
            claim_id: claim.claim_id,
            envelope_id: claim.envelope_id,
            approval_id: claim.approval_id,
            actor: released.actor,
            reason: released.reason
          }, 'bridge release request');
          runtime.schemas.assert('agent-envelope', released.envelope, 'released bridge envelope');
          const artifactIds = claimArtifactIds({ run_id: claim.run_id, claim_id: claim.claim_id });
          const releaseRef = await writeArtifactRef(artifactDir, artifactIds.release, {
            artifact_version: 2,
            kind: 'bridge.release',
            run_id: claim.run_id,
            envelope_id: claim.envelope_id,
            approval_id: claim.approval_id,
            claim_id: claim.claim_id,
            actor: released.actor,
            reason: released.reason,
            created_at: released.created_at
          });
          const event = createEvent('bridge.claim_released', released.created_at, {
            envelope: released.envelope,
            claim: released.claim,
            actor: released.actor,
            reason: released.reason,
            artifact_refs: [releaseRef]
          }, BRIDGE_EVENT_VERSION);
          try {
            await persistence.commitEvent(event, runtime.reduceOptions);
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            throw error;
          }
          return {
            status: 200,
            body: { envelope: released.envelope, claim: released.claim, artifact_ref: releaseRef }
          };
        });
        sendJson(response, result.status, result.body);
        return;
      }

      const evidenceMatch = url.pathname.match(
        /^\/api\/receipts\/([^/]+)\/evidence\/(before|after|receipt|result)$/
      );
      if (request.method === 'GET' && evidenceMatch) {
        const receiptId = decodeURIComponent(evidenceMatch[1]);
        const evidenceKind = evidenceMatch[2];
        const { projection } = await persistence.reconcile(runtime.reduceOptions);
        const receipt = projection.receipts.find((candidate) => candidate.receipt_id === receiptId);
        if (!receipt) {
          sendJson(response, 404, { error: 'receipt_not_found' });
          return;
        }

        let artifactRef;
        let expectedKind;
        if (receipt.receipt_kind === 'skill.execution') {
          const claimIds = claimArtifactIds({
            run_id: receipt.run_id,
            claim_id: receipt.claim_id
          });
          const executionIds = executionArtifactIds({
            run_id: receipt.run_id,
            receipt_id: receipt.receipt_id
          });
          const artifactId = evidenceKind === 'before'
            ? claimIds.claim
            : executionIds[evidenceKind];
          if (!artifactId) {
            sendJson(response, 404, { error: 'evidence_unavailable' });
            return;
          }
          artifactRef = artifactRefFor(artifactDir, artifactId);
          expectedKind = {
            before: 'bridge.claim',
            after: 'bridge.result.after',
            result: 'bridge.result',
            receipt: 'bridge.execution.receipt'
          }[evidenceKind];
        } else {
          const artifactIds = evidenceArtifactIds({
            run_id: receipt.run_id,
            approval_id: receipt.approval_id
          });
          if (!artifactIds[evidenceKind]) {
            sendJson(response, 404, { error: 'evidence_unavailable' });
            return;
          }
          artifactRef = artifactRefFor(artifactDir, artifactIds[evidenceKind]);
          expectedKind = `approval.${evidenceKind}`;
        }
        let artifact;
        try {
          artifact = await validateArtifactRef(artifactDir, artifactRef, {
            kind: expectedKind,
            run_id: receipt.run_id,
            envelope_id: receipt.envelope_id,
            approval_id: receipt.approval_id,
            ...(receipt.receipt_kind === 'skill.execution'
              ? { claim_id: receipt.claim_id }
              : {
                  requested_grants: receipt.requested_grants,
                  requested_skill: receipt.requested_skill
                })
          });
        } catch (error) {
          if (error.code?.startsWith('artifact_') || error.code === 'malformed_artifact') {
            sendJson(response, 404, { error: 'evidence_unavailable' });
            return;
          }
          throw error;
        }
        sendJson(response, 200, projectArtifactForUi(artifact));
        return;
      }

      if (request.method === 'POST' && url.pathname === '/api/envelopes/prepare') {
        const input = await readBody(request);
        try {
          runtime.schemas.assert('prepare-request', input, 'POST /api/envelopes/prepare');
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }

        const result = await mutate(async () => {
          await persistence.reconcile(runtime.reduceOptions);
          let envelope;
          let approvalItem;
          let eventVersion = EVENT_VERSION;

          try {
            if (isBridgeGrantProfile(input.requested_grants)) {
              const prepared = prepareBridgeEnvelope(input);
              envelope = prepared.envelope;
              approvalItem = prepared.approval;
              eventVersion = BRIDGE_EVENT_VERSION;
            } else {
              envelope = prepareDryRunEnvelope(input);
            }
          } catch (error) {
            if (error.code === 'invalid_grants' || error.code === 'invalid_bridge_grants') {
              return {
                status: 400,
                body: {
                  error: error.code,
                  message: error.message,
                  policy_version: error.policy_version || L0_GRANT_POLICY_VERSION
                }
              };
            }
            throw error;
          }

          approvalItem ||= {
            approval_id: envelope.approval.approval_id,
            envelope_id: envelope.envelope_id,
            run_id: envelope.run_id,
            state: 'pending',
            actor: null,
            title: envelope.task,
            required_for: envelope.requested_grants,
            created_at: envelope.created_at,
            approved_at: null,
            consumed_at: null,
            rejected_at: null,
            rejection_reason: null
          };

          runtime.schemas.assert('agent-envelope', envelope, 'prepared envelope');
          runtime.schemas.assert('approval-record', approvalItem, 'pending approval');
          const event = createEvent('envelope.prepared', envelope.created_at, {
            envelope,
            approval: approvalItem
          }, eventVersion);

          try {
            await persistence.commitEvent(event, runtime.reduceOptions);
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            throw error;
          }

          return { status: 201, body: { envelope, approval: approvalItem } };
        });
        sendJson(response, result.status, result.body);
        return;
      }

      const runMatch = url.pathname.match(/^\/api\/envelopes\/([^/]+)\/run$/);
      if (request.method === 'POST' && runMatch) {
        const { projection: state } = await persistence.reconcile(runtime.reduceOptions);
        const envelope = state.envelopes[runMatch[1]];

        if (!envelope) {
          sendJson(response, 404, { error: 'envelope_not_found' });
          return;
        }

        if (blockedBeforeApproval(envelope)) {
          sendJson(response, 409, {
            error: 'approval_required',
            approval_id: envelope.approval.approval_id
          });
          return;
        }
        sendJson(response, 200, { envelope_id: envelope.envelope_id, state: envelope.state });
        return;
      }

      const approvalMatch = url.pathname.match(/^\/api\/approvals\/([^/]+)\/approve$/);
      if (request.method === 'POST' && approvalMatch) {
        const approvalId = approvalMatch[1];
        const body = await readBody(request);
        try {
          runtime.schemas.assert('approve-request', body, 'POST approval approve');
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }

        const result = await mutate(async () => {
          const { projection: state } = await persistence.reconcile(runtime.reduceOptions);
          const approval = state.approvals[approvalId];

          if (!approval) {
            return { status: 404, body: { error: 'approval_not_found' } };
          }

          const envelope = state.envelopes[approval.envelope_id];
          if (
            !envelope
            || envelope.run_id !== approval.run_id
            || envelope.approval.approval_id !== approvalId
          ) {
            return { status: 409, body: { error: 'approval_binding_mismatch' } };
          }

          if (approval.state !== 'pending' || envelope.state !== 'awaiting_approval') {
            return { status: 409, body: { error: 'already_resolved' } };
          }

          if (envelope.schema_version === '2') {
            return commitBridgeAuthorization({
              state,
              envelope,
              approval,
              runtime,
              persistence,
              artifactDir,
              evidenceRoot
            });
          }

          const artifactIds = evidenceArtifactIds({
            run_id: envelope.run_id,
            approval_id: approvalId
          });
          const beforeRef = artifactRefFor(artifactDir, artifactIds.before);
          const afterRef = artifactRefFor(artifactDir, artifactIds.after);
          const receiptRef = artifactRefFor(artifactDir, artifactIds.receipt);
          const proposal = proposeDryRunApproval(envelope);
          const approvedEnvelope = proposal.envelope;
          const consumedApproval = {
            ...approval,
            state: 'consumed',
            actor: localOperatorAction(),
            approved_at: proposal.created_at,
            consumed_at: proposal.created_at
          };
          runtime.schemas.assert('agent-envelope', approvedEnvelope, 'approved envelope');
          runtime.schemas.assert('approval-record', consumedApproval, 'consumed approval');

          const artifactBindings = {
            run_id: envelope.run_id,
            envelope_id: envelope.envelope_id,
            approval_id: approvalId,
            requested_grants: envelope.requested_grants,
            requested_skill: envelope.requested_skill
          };
          const beforeArtifact = {
            artifact_version: 1,
            kind: 'approval.before',
            ...artifactBindings,
            state: envelope.state,
            envelope,
            approval,
            created_at: proposal.created_at
          };
          const afterArtifact = {
            artifact_version: 1,
            kind: 'approval.after',
            ...artifactBindings,
            disposition: 'approved',
            state: approvedEnvelope.state,
            envelope: approvedEnvelope,
            approval: consumedApproval,
            created_at: proposal.created_at
          };

          await writeArtifactRef(artifactDir, artifactIds.before, beforeArtifact);
          await validateArtifactRef(artifactDir, beforeRef, {
            kind: 'approval.before',
            ...artifactBindings,
            envelope,
            approval
          });
          await writeArtifactRef(artifactDir, artifactIds.after, afterArtifact);
          await validateArtifactRef(artifactDir, afterRef, {
            kind: 'approval.after',
            ...artifactBindings,
            disposition: 'approved',
            envelope: approvedEnvelope,
            approval: consumedApproval
          });

          const evidenceRefs = state.evidence_refs;
          await validateEvidenceRefs(evidenceRoot, evidenceRefs);
          const receipt = createDryRunReceipt(approvedEnvelope, {
            receipt_id: proposal.receipt_id,
            created_at: proposal.created_at,
            before_ref: beforeRef,
            after_ref: afterRef,
            evidence_refs: evidenceRefs
          });
          runtime.schemas.assert('receipt', receipt, 'approval receipt');

          const receiptArtifact = {
            artifact_version: 1,
            kind: 'approval.receipt',
            ...artifactBindings,
            disposition: 'approved',
            receipt,
            created_at: proposal.created_at
          };
          await writeArtifactRef(artifactDir, artifactIds.receipt, receiptArtifact);
          await validateArtifactRef(artifactDir, receiptRef, {
            kind: 'approval.receipt',
            ...artifactBindings,
            disposition: 'approved',
            receipt
          });

          const event = createEvent('receipt.appended', receipt.created_at, {
            envelope: approvedEnvelope,
            approval: consumedApproval,
            receipt,
            artifact_refs: [beforeRef, afterRef, receiptRef]
          });

          try {
            await persistence.commitEvent(event, runtime.reduceOptions);
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            throw error;
          }

          return {
            status: 201,
            body: {
              receipt,
              artifact_ref: receiptRef,
              artifact_refs: {
                before: beforeRef,
                after: afterRef,
                receipt: receiptRef
              }
            }
          };
        });
        sendJson(response, result.status, result.body);
        return;
      }

      const rejectionMatch = url.pathname.match(/^\/api\/approvals\/([^/]+)\/reject$/);
      if (request.method === 'POST' && rejectionMatch) {
        const approvalId = rejectionMatch[1];
        const body = await readBody(request);
        try {
          runtime.schemas.assert('reject-request', body, 'POST approval reject');
        } catch (error) {
          if (error.code === 'schema_validation_failed') {
            sendJson(response, 400, invalidRequest(error));
            return;
          }
          throw error;
        }

        let rejectionReason;

        try {
          rejectionReason = normalizeRejectionReason(body.reason);
        } catch (error) {
          if (error.code === 'invalid_rejection_reason') {
            sendJson(response, 400, { error: error.code, message: error.message });
            return;
          }
          throw error;
        }

        const result = await mutate(async () => {
          const { projection: state } = await persistence.reconcile(runtime.reduceOptions);
          const approval = state.approvals[approvalId];

          if (!approval) {
            return { status: 404, body: { error: 'approval_not_found' } };
          }

          const envelope = state.envelopes[approval.envelope_id];
          if (
            !envelope
            || envelope.run_id !== approval.run_id
            || envelope.approval.approval_id !== approvalId
          ) {
            return { status: 409, body: { error: 'approval_binding_mismatch' } };
          }

          if (envelope.schema_version === '2' && approval.state === 'authorized') {
            if (!['approved', 'ready_for_poll'].includes(envelope.state)) {
              return { status: 409, body: { error: 'already_claimed_or_resolved' } };
            }
            const revoked = revokeBridgeAuthorization(
              envelope,
              approval,
              rejectionReason || 'Revoked by local operator.'
            );
            runtime.schemas.assert('agent-envelope', revoked.envelope, 'revoked bridge envelope');
            runtime.schemas.assert('approval-record', revoked.approval, 'revoked bridge approval');
            const event = createEvent('approval.revoked', revoked.created_at, {
              envelope: revoked.envelope,
              approval: revoked.approval,
              actor: revoked.actor,
              reason: revoked.reason
            }, BRIDGE_EVENT_VERSION);

            try {
              await persistence.commitEvent(event, runtime.reduceOptions);
            } catch (error) {
              if (error.code === 'reconciliation_required') return reconciliationRequired(error);
              throw error;
            }
            return {
              status: 200,
              body: { approval: revoked.approval, envelope: revoked.envelope }
            };
          }

          if (approval.state !== 'pending' || envelope.state !== 'awaiting_approval') {
            return { status: 409, body: { error: 'already_resolved' } };
          }

          const rejected = rejectDryRunEnvelope(envelope, { reason: rejectionReason });
          const rejectedApproval = {
            ...approval,
            state: 'rejected',
            actor: localOperatorAction(),
            rejected_at: rejected.rejected_at,
            rejection_reason: rejected.rejection_reason
          };
          runtime.schemas.assert('agent-envelope', rejected.envelope, 'rejected envelope');
          runtime.schemas.assert('approval-record', rejectedApproval, 'rejected approval');
          const event = createEvent('approval.rejected', rejected.rejected_at, {
            envelope: rejected.envelope,
            approval: rejectedApproval
          }, envelope.schema_version === '2' ? BRIDGE_EVENT_VERSION : EVENT_VERSION);

          try {
            await persistence.commitEvent(event, runtime.reduceOptions);
          } catch (error) {
            if (error.code === 'reconciliation_required') return reconciliationRequired(error);
            throw error;
          }

          return {
            status: 200,
            body: {
              approval: rejectedApproval,
              envelope: rejected.envelope
            }
          };
        });
        sendJson(response, result.status, result.body);
        return;
      }

      sendText(response, 404, 'not found');
    } catch (error) {
      if (error.code === 'request_too_large') {
        sendJson(response, 413, { error: error.code, message: error.message });
        return;
      }
      if (error.code === 'invalid_json') {
        sendJson(response, 400, { error: error.code, message: error.message });
        return;
      }
      sendJson(response, 500, { error: error.message });
    }
  });

  const closeServer = server.close.bind(server);
  server.close = (callback) => {
    canvasRetention.close();
    canvasNotifications.close();
    return closeServer(callback);
  };
  server.ready = ready;
  server.canvasNotifications = canvasNotifications;
  server.canvasNavigation = canvasNavigation;
  server.canvasRetention = canvasRetention;
  return server;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const port = Number(process.env.PORT || 8765);
  const server = createServer({
    stateDir: process.env.IDE_EXTENSION_STATE_DIR || undefined,
    workspaceRoot: process.env.IDE_EXTENSION_WORKSPACE_ROOT || undefined
  });
  await server.ready;
  server.listen(port, '127.0.0.1', () => {
    const address = server.address();
    console.log(`ide-extension local workbench: http://127.0.0.1:${address.port}/demo/l0`);
  });
}
