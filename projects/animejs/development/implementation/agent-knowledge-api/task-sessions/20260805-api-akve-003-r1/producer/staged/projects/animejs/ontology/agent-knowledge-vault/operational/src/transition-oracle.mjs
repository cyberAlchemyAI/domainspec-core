const APPEND_AUDIENCE = 'animejs-work-episode-append';

const reject = (status, code) => ({ accepted: false, status, code, event: null });

function activeAttempt(state) {
  return state?.attempts?.find(attempt => !attempt.outcome) ?? null;
}

function attemptAt(state, ordinal) {
  return state?.attempts?.find(attempt => attempt.ordinal === ordinal) ?? null;
}

function authorize(state, bindings) {
  if (!state) return true;
  const owner = state.owner_binding;
  return owner.principal_id === bindings.principal_id
    && owner.tenant_or_workspace_id === bindings.tenant_or_workspace_id
    && owner.vault_scope === bindings.vault_scope
    && (owner.delegation_id === null || owner.delegation_id === (bindings.delegation_id ?? null));
}

function baseEvent(command, state, bindings, eventType, payload) {
  return {
    event_type: eventType,
    episode_id: state?.episode_id ?? bindings.episode_id,
    revision: (state?.revision ?? 0) + 1,
    graph_digest: state?.opening_graph_digest ?? command.expected_graph_digest,
    command_id: command.command_id,
    payload,
  };
}

export function decideTransition({ state = null, command, bindings, resolvedEvidence = null }) {
  if (!command || !bindings) return reject('invalid_request', 'INVALID_REQUEST');
  if (bindings.capability_audience !== APPEND_AUDIENCE) return reject('denied', 'DENIED');
  if (!authorize(state, bindings)) return reject('denied', 'DENIED');

  if (command.operation === 'open_episode') {
    if (state) return reject('invalid_request', 'REOPEN_FORBIDDEN');
    if (command.episode_id !== null || command.expected_revision !== 0) return reject('invalid_request', 'REOPEN_FORBIDDEN');
    if (command.payload.supersedes_episode_id) {
      if (!bindings.superseded_episode?.terminal) return reject('invalid_request', 'SUPERSESSION_TARGET_NOT_TERMINAL');
      if (bindings.supersession_cycle === true || command.payload.supersedes_episode_id === bindings.episode_id) {
        return reject('invalid_request', 'SUPERSESSION_CYCLE');
      }
    }
    if (!bindings.task_snapshot || !bindings.task_digest || !bindings.version_context_snapshot || !bindings.version_context_digest) {
      return reject('invalid_request', 'HOST_BINDING_REQUIRED');
    }
    const event = baseEvent(command, null, bindings, 'EpisodeOpened', {
      goal: command.payload.goal,
      started_at: command.payload.started_at,
      tags: command.payload.tags ?? [],
      task_snapshot: bindings.task_snapshot,
      task_digest: bindings.task_digest,
      version_context_snapshot: bindings.version_context_snapshot,
      version_context_digest: bindings.version_context_digest,
      owner_binding: {
        principal_id: bindings.principal_id,
        tenant_or_workspace_id: bindings.tenant_or_workspace_id,
        vault_scope: bindings.vault_scope,
        capability_audience: APPEND_AUDIENCE,
        delegation_id: bindings.delegation_id ?? null,
      },
      supersedes_episode_id: command.payload.supersedes_episode_id ?? null,
    });
    return { accepted: true, status: 'accepted', code: null, event };
  }

  if (!state) return reject('denied', 'DENIED');
  if (command.expected_graph_digest !== state.opening_graph_digest) return reject('stale_context', 'STALE_GRAPH_DIGEST');
  if (command.expected_revision !== state.revision) return reject('conflict', 'REVISION_CONFLICT');
  if (state.lifecycle_state !== 'open') return reject('invalid_request', 'EPISODE_TERMINAL');

  if (command.operation === 'append_attempt') {
    if (activeAttempt(state)) return reject('invalid_request', 'DANGLING_ATTEMPT');
    if (command.payload.ordinal !== state.attempts.length + 1) return reject('invalid_request', 'ATTEMPT_ORDINAL_INVALID');
    const event = baseEvent(command, state, bindings, 'AttemptAppended', {
      ordinal: command.payload.ordinal,
      action_summary: command.payload.action_summary,
      input_artifact_handles: command.payload.input_artifact_handles ?? [],
    });
    return { accepted: true, status: 'accepted', code: null, event };
  }

  if (command.operation === 'attach_evidence') {
    const attempt = attemptAt(state, command.payload.attempt_ordinal);
    if (!attempt || attempt.outcome) return reject('evidence_rejected', 'EVIDENCE_TARGET_INVALID');
    if (!resolvedEvidence || resolvedEvidence.handle !== command.payload.evidence_handle) return reject('evidence_rejected', 'EVIDENCE_HANDLE_REVOKED');
    if (resolvedEvidence.target_episode_id !== state.episode_id || resolvedEvidence.target_attempt_ordinal !== attempt.ordinal) {
      return reject('evidence_rejected', 'EVIDENCE_TARGET_MISMATCH');
    }
    if (resolvedEvidence.task_digest !== state.task_digest || resolvedEvidence.version_context_digest !== state.version_context_digest) {
      return reject('evidence_rejected', 'EVIDENCE_CONTEXT_MISMATCH');
    }
    if (attempt.evidence.some(item => item.handle === resolvedEvidence.handle)) return reject('evidence_rejected', 'EVIDENCE_DUPLICATE');
    const event = baseEvent(command, state, bindings, 'EvidenceAttached', { ...resolvedEvidence });
    return { accepted: true, status: 'accepted', code: null, event };
  }

  if (command.operation === 'record_outcome') {
    const attempt = attemptAt(state, command.payload.attempt_ordinal);
    if (!attempt) return reject('invalid_request', 'ATTEMPT_NOT_FOUND');
    if (attempt.outcome) return reject('invalid_request', 'DUPLICATE_OUTCOME');
    if (command.payload.classification === 'succeeded') {
      const admissible = attempt.evidence.some(item => item.state === 'admissible' && ['executed', 'test'].includes(item.evidence_class));
      if (!admissible) return reject('evidence_rejected', 'EVIDENCE_REQUIRED');
    }
    const attached = new Set(attempt.evidence.map(item => item.handle));
    if ((command.payload.witness_handles ?? []).some(handle => !attached.has(handle))) {
      return reject('evidence_rejected', 'EVIDENCE_REQUIRED');
    }
    const event = baseEvent(command, state, bindings, 'OutcomeRecorded', {
      attempt_ordinal: attempt.ordinal,
      classification: command.payload.classification,
      observations: command.payload.observations ?? [],
      witness_handles: command.payload.witness_handles ?? [],
    });
    return { accepted: true, status: 'accepted', code: null, event };
  }

  if (command.operation === 'close_episode') {
    if (activeAttempt(state)) return reject('invalid_request', 'DANGLING_ATTEMPT');
    if (command.payload.disposition === 'completed' && !state.attempts.some(attempt => attempt.outcome)) {
      return reject('invalid_request', 'OUTCOME_REQUIRED');
    }
    const event = baseEvent(command, state, bindings, 'EpisodeClosed', { disposition: command.payload.disposition });
    return { accepted: true, status: 'accepted', code: null, event };
  }

  return reject('invalid_request', 'INVALID_REQUEST');
}

export function applyEpisodeEvent(state, event) {
  if (event.event_type === 'EpisodeOpened') {
    return {
      episode_id: event.episode_id,
      revision: event.revision,
      lifecycle_state: 'open',
      opening_graph_digest: event.graph_digest,
      owner_binding: event.payload.owner_binding,
      task_snapshot: event.payload.task_snapshot,
      task_digest: event.payload.task_digest,
      version_context_snapshot: event.payload.version_context_snapshot,
      version_context_digest: event.payload.version_context_digest,
      goal: event.payload.goal,
      tags: event.payload.tags,
      supersedes_episode_id: event.payload.supersedes_episode_id,
      attempts: [],
      closure: null,
    };
  }
  const next = structuredClone(state);
  next.revision = event.revision;
  if (event.event_type === 'AttemptAppended') next.attempts.push({ ...event.payload, evidence: [], outcome: null });
  if (event.event_type === 'EvidenceAttached') attemptAt(next, event.payload.target_attempt_ordinal).evidence.push(event.payload);
  if (event.event_type === 'OutcomeRecorded') attemptAt(next, event.payload.attempt_ordinal).outcome = event.payload;
  if (event.event_type === 'EpisodeClosed') {
    next.lifecycle_state = event.payload.disposition;
    next.closure = event.payload;
  }
  return next;
}
