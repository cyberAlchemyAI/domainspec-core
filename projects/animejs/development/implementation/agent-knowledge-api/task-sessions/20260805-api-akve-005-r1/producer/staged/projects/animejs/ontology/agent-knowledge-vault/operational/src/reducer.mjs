import { canonicalBytes, sha256 } from './canonical-json.mjs';
import { applyEpisodeEvent } from './transition-oracle.mjs';

const requiredEventFields = ['contract', 'event_id', 'episode_id', 'revision', 'event_type', 'command_id', 'request_digest', 'principal_id', 'policy_epoch', 'graph_digest', 'recorded_at', 'payload', 'prior_event_digest', 'event_digest'];
const eventTypes = new Set(['EpisodeOpened', 'AttemptAppended', 'EvidenceAttached', 'OutcomeRecorded', 'EpisodeClosed']);

function quarantine(code, detail = null) {
  return { status: 'quarantined', snapshot: null, snapshot_bytes: null, snapshot_digest: null, snapshot_key: null, migration_receipt: null, diagnostic: { code, detail } };
}

function sequenceDiagnostic(events) {
  const revisions = events.map(event => event.revision);
  if (new Set(revisions).size !== revisions.length) return 'JOURNAL_FORK';
  const sorted = [...revisions].sort((left, right) => left - right);
  const contiguous = sorted.every((revision, index) => revision === index + 1);
  if (!contiguous) return 'JOURNAL_GAP';
  if (revisions.some((revision, index) => revision !== index + 1)) return 'JOURNAL_ORDER_INVALID';
  return null;
}

function validShape(event) {
  return event && typeof event === 'object'
    && Object.keys(event).length === requiredEventFields.length
    && requiredEventFields.every(key => key in event)
    && event.contract === 'animejs-work-episode-event/0.1.0'
    && eventTypes.has(event.event_type)
    && Number.isInteger(event.revision) && event.revision > 0;
}

function validSemanticStep(state, event) {
  if (event.event_type === 'EpisodeOpened') return state === null && event.revision === 1;
  if (!state || state.lifecycle_state !== 'open') return false;
  if (event.event_type === 'AttemptAppended') return event.payload.ordinal === state.attempts.length + 1 && !state.attempts.some(attempt => !attempt.outcome);
  if (event.event_type === 'EvidenceAttached') {
    const attempt = state.attempts.find(item => item.ordinal === event.payload.target_attempt_ordinal);
    return Boolean(attempt && !attempt.outcome && !attempt.evidence.some(item => item.handle === event.payload.handle));
  }
  if (event.event_type === 'OutcomeRecorded') {
    const attempt = state.attempts.find(item => item.ordinal === event.payload.attempt_ordinal);
    return Boolean(attempt && !attempt.outcome);
  }
  if (event.event_type === 'EpisodeClosed') return !state.attempts.some(attempt => !attempt.outcome);
  return false;
}

export function reduceEpisode({ events, reducerVersion = '1.0.0', previousSnapshots = [] }) {
  if (!Array.isArray(events) || !reducerVersion) return quarantine('INVALID_REDUCER_INPUT');
  if (events.length === 0) return { status: 'empty', snapshot: null, snapshot_bytes: null, snapshot_digest: null, snapshot_key: null, migration_receipt: null, diagnostic: null };
  const sequenceCode = sequenceDiagnostic(events);
  if (sequenceCode) return quarantine(sequenceCode);

  const episodeId = events[0].episode_id;
  const graphDigest = events[0].graph_digest;
  let priorDigest = null;
  let state = null;
  for (const event of events) {
    if (!validShape(event)) return quarantine('EVENT_SCHEMA_INVALID', { revision: event?.revision ?? null });
    if (event.episode_id !== episodeId) return quarantine('JOURNAL_FORK', { revision: event.revision });
    if (event.graph_digest !== graphDigest) return quarantine('GRAPH_DIGEST_MISMATCH', { revision: event.revision });
    if (event.prior_event_digest !== priorDigest) return quarantine('JOURNAL_FORK', { revision: event.revision });
    const { event_digest: declaredDigest, ...withoutDigest } = event;
    if (sha256(withoutDigest) !== declaredDigest) return quarantine('EVENT_DIGEST_MISMATCH', { revision: event.revision });
    if (!validSemanticStep(state, event)) return quarantine('IMPOSSIBLE_TRANSITION', { revision: event.revision, event_type: event.event_type });
    state = applyEpisodeEvent(state, event);
    priorDigest = declaredDigest;
  }

  const snapshot = {
    contract: 'animejs-work-episode-snapshot/0.1.0',
    reducer_version: reducerVersion,
    episode_id: episodeId,
    revision: state.revision,
    last_event_digest: priorDigest,
    opening_graph_digest: graphDigest,
    state,
    semantic_effect: 'none',
    task_state_unchanged: true,
    truth_status: 'not_assessed',
  };
  const snapshotBytes = canonicalBytes(snapshot);
  const snapshotDigest = sha256(snapshotBytes);
  const olderVersion = previousSnapshots.find(item => item.last_event_digest === priorDigest && item.reducer_version !== reducerVersion);
  const migrationReceipt = olderVersion ? {
    contract: 'animejs-work-episode-migration/0.1.0',
    episode_id: episodeId,
    from_reducer_version: olderVersion.reducer_version,
    to_reducer_version: reducerVersion,
    last_event_digest: priorDigest,
    prior_snapshot_digest: olderVersion.snapshot_digest,
    new_snapshot_digest: snapshotDigest,
    prior_snapshot_retained: true,
    authority_effect: 'none',
  } : null;
  return {
    status: 'current', snapshot, snapshot_bytes: snapshotBytes,
    snapshot_digest: snapshotDigest,
    snapshot_key: `${reducerVersion}:${priorDigest}`,
    migration_receipt: migrationReceipt,
    diagnostic: null,
  };
}
