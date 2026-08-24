import {
  DEFAULT_INTERACTIVE_WORLD_MANIFEST,
  admitWorldManifest,
  canonicalWorldState,
  createInitialWorldProjectionState,
  reduceWorldProjection,
} from './world-model.mjs';
import { createWorldRenderer } from './world-renderer.mjs';

const SNAPSHOT_KEYS = [
  'activeFloorId',
  'rememberedFloorId',
  'viewMode',
  'inspectionKind',
  'inspectionId',
  'openedReferenceId',
  'focusReturnTarget',
];

function bridgeError(code, message, cause = null) {
  const error = new Error(message);
  error.name = 'WorldBridgeError';
  error.code = code;
  error.cause = cause;
  return error;
}

function assertNarrowSnapshot(snapshot) {
  if (!snapshot || typeof snapshot !== 'object' || Array.isArray(snapshot)) {
    throw bridgeError('WORLD_SEMANTIC_SNAPSHOT_INVALID', 'Semantic snapshot must be an object');
  }
  const keys = Object.keys(snapshot);
  if (keys.length !== SNAPSHOT_KEYS.length || keys.some((key) => !SNAPSHOT_KEYS.includes(key))) {
    throw bridgeError('WORLD_SEMANTIC_SNAPSHOT_INVALID', 'Semantic snapshot must contain exactly seven admitted fields');
  }
  for (const key of SNAPSHOT_KEYS) {
    if (!(typeof snapshot[key] === 'string' || snapshot[key] === null)) {
      throw bridgeError('WORLD_SEMANTIC_SNAPSHOT_INVALID', `${key} must be string or null`);
    }
  }
  return snapshot;
}

export function canonicalSemanticInspectionState(snapshot) {
  const value = assertNarrowSnapshot(snapshot);
  return JSON.stringify({
    activeFloorId: value.activeFloorId,
    rememberedFloorId: value.rememberedFloorId,
    viewMode: value.viewMode,
    inspectionKind: value.inspectionKind,
    inspectionId: value.inspectionId,
    openedReferenceId: value.openedReferenceId,
    focusReturnTarget: value.focusReturnTarget,
  });
}

export function mountWorldBridge(options) {
  const allowed = new Set([
    'host',
    'manifest',
    'readSemanticInspectionState',
    'requestSemanticTransition',
    'subscribeCommittedState',
    'onWorldStatus',
  ]);
  if (!options || typeof options !== 'object' || Object.keys(options).some((key) => !allowed.has(key))) {
    throw bridgeError('WORLD_BRIDGE_OPTIONS_INVALID', 'Bridge options exceed the narrow adapter');
  }
  const {
    host,
    manifest = DEFAULT_INTERACTIVE_WORLD_MANIFEST,
    readSemanticInspectionState,
    requestSemanticTransition,
    subscribeCommittedState,
    onWorldStatus,
  } = options;
  for (const [name, value] of Object.entries({
    readSemanticInspectionState,
    requestSemanticTransition,
    subscribeCommittedState,
    onWorldStatus,
  })) {
    if (typeof value !== 'function') throw bridgeError('WORLD_BRIDGE_OPTIONS_INVALID', `${name} must be a function`);
  }
  if (!host?.ownerDocument) throw bridgeError('WORLD_BRIDGE_OPTIONS_INVALID', 'A DOM host is required');

  const admitted = admitWorldManifest(manifest);
  for (const binding of admitted.bindings) {
    const control = host.ownerDocument.getElementById(binding.semantic_control_id);
    if (!control) throw bridgeError('WORLD_BINDING_CONTROL_MISSING', `Missing semantic control ${binding.semantic_control_id}`);
  }

  let projectionState = createInitialWorldProjectionState(admitted);
  let semanticBytes = canonicalSemanticInspectionState(readSemanticInspectionState());
  let status = 'ready';
  let destroyed = false;
  let unsubscribe = () => {};
  let renderer;

  function report(nextStatus, detail = null) {
    status = nextStatus;
    host.setAttribute('data-world-state', nextStatus);
    onWorldStatus({ status: nextStatus, detail });
  }

  function fail(error) {
    if (destroyed) return { status: 'failed', error };
    const before = semanticBytes;
    let after;
    try {
      after = canonicalSemanticInspectionState(readSemanticInspectionState());
    } catch (snapshotError) {
      error = bridgeError('WORLD_SEMANTIC_ROLLBACK_UNREADABLE', snapshotError.message, error);
      after = null;
    }
    if (after !== before) error = bridgeError('WORLD_SEMANTIC_ROLLBACK_BREACH', 'Projection failure changed semantic state', error);
    renderer?.destroy();
    report('failed', { code: error?.code ?? 'WORLD_PROJECTION_FAILED', message: error?.message ?? String(error) });
    return { status: 'failed', error };
  }

  async function sendIntent(intent) {
    if (destroyed || status === 'failed') return { status: 'failed', state: projectionState };
    const reduced = reduceWorldProjection(projectionState, intent, admitted);
    if (reduced.status === 'failed') return fail(bridgeError(reduced.diagnostic.code, reduced.diagnostic.message));
    if (reduced.status === 'no_effect') return reduced;

    if (reduced.request) {
      const binding = admitted.bindings.find(({ hotspot_id: id }) => id === reduced.request.hotspot_id);
      if (!binding) return fail(bridgeError('WORLD_BINDING_MISSING', 'Activation binding disappeared'));
      try {
        const response = await requestSemanticTransition(binding.semantic_action_id, intent.input_kind ?? 'unknown');
        if (!response || !['committed', 'rejected', 'no_effect'].includes(response.status)) {
          return fail(bridgeError('WORLD_SEMANTIC_RESPONSE_INVALID', 'Semantic owner returned an invalid status'));
        }
        const observed = canonicalSemanticInspectionState(readSemanticInspectionState());
        if (response.status !== 'committed') {
          if (observed !== semanticBytes) return fail(bridgeError('WORLD_SEMANTIC_REJECT_MUTATED', 'Rejected semantic request changed state'));
          return { status: response.status === 'rejected' ? 'no_effect' : response.status, state: projectionState };
        }
        if (response.snapshot && canonicalSemanticInspectionState(response.snapshot) !== observed) {
          return fail(bridgeError('WORLD_SEMANTIC_COMMIT_MISMATCH', 'Semantic response does not match committed owner state'));
        }
        semanticBytes = observed;
      } catch (error) {
        return fail(error);
      }
    }

    projectionState = reduced.state;
    renderer.applyState(projectionState);
    report('ready', { projection: canonicalWorldState(projectionState) });
    return { ...reduced, state: projectionState };
  }

  renderer = createWorldRenderer({
    host,
    manifest: admitted,
    initialState: projectionState,
    onIntent: sendIntent,
    onFailure: fail,
  });
  unsubscribe = subscribeCommittedState((snapshot) => {
    if (destroyed || status === 'failed') return;
    try {
      semanticBytes = canonicalSemanticInspectionState(snapshot);
      report('ready', { semantic: semanticBytes });
    } catch (error) {
      fail(error);
    }
  });
  if (typeof unsubscribe !== 'function') {
    renderer.destroy();
    throw bridgeError('WORLD_SUBSCRIPTION_INVALID', 'Semantic subscription must return an unsubscribe function');
  }
  report('ready', { projection: canonicalWorldState(projectionState) });

  function destroy() {
    if (destroyed) return;
    destroyed = true;
    unsubscribe();
    renderer.destroy();
    status = 'destroyed';
    host.setAttribute('data-world-state', 'destroyed');
  }

  return Object.freeze({
    sendIntent,
    focus: () => renderer.focus(),
    destroy,
    getState: () => projectionState,
    getStatus: () => status,
    getSemanticSnapshot: () => semanticBytes,
    getOwnedCallbackCount: () => renderer.getOwnedCallbackCount(),
    isDestroyed: () => destroyed,
  });
}
