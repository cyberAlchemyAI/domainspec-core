import { canonicalJson, sha256 } from './canonical-json.mjs';

const semanticClosure = Object.freeze({ semantic_effect: 'none', task_state_unchanged: true, truth_status: 'not_assessed' });

function sameScope(left, right) {
  return ['principal_id', 'tenant_or_workspace_id', 'vault_scope', 'capability_audience'].every(key => left[key] === right[key]);
}

export class InMemoryAtomicEpisodeStore {
  #episodes = new Map();
  #locks = new Map();
  recovery = new Map();

  episode(episodeId) {
    if (!this.#episodes.has(episodeId)) this.#episodes.set(episodeId, { events: [], idempotency: new Map() });
    return this.#episodes.get(episodeId);
  }

  events(episodeId) {
    return structuredClone(this.episode(episodeId).events);
  }

  async transact(episodeId, operation) {
    const prior = this.#locks.get(episodeId) ?? Promise.resolve();
    let release;
    const current = new Promise(resolve => { release = resolve; });
    const queued = prior.then(() => current);
    this.#locks.set(episodeId, queued);
    await prior;
    try {
      return await operation(this.episode(episodeId));
    } finally {
      release();
      if (this.#locks.get(episodeId) === queued) this.#locks.delete(episodeId);
    }
  }
}

export function createEpisodeJournal({ store = new InMemoryAtomicEpisodeStore(), clock = () => new Date().toISOString(), idFactory = digest => `event:${digest.slice(0, 32)}` } = {}) {
  function recoveryHandle(scope, idempotencyKey, requestDigest) {
    return `recovery:${sha256({ scope: { principal_id: scope.principal_id, tenant_or_workspace_id: scope.tenant_or_workspace_id, vault_scope: scope.vault_scope, capability_audience: scope.capability_audience }, idempotency_key: idempotencyKey, request_digest: requestDigest }).slice(0, 40)}`;
  }

  async function append({ scope, requestDigest, proposedEvent, expectedRevision, expectedTailDigest = null, idempotencyKey, failurePoint = null }) {
    if (!scope || !requestDigest || !proposedEvent || !idempotencyKey) throw new TypeError('journal append requires complete normalized input');
    const episodeId = proposedEvent.episode_id;
    const scopedKey = sha256({ principal_id: scope.principal_id, tenant_or_workspace_id: scope.tenant_or_workspace_id, vault_scope: scope.vault_scope, capability_audience: scope.capability_audience, operation: scope.operation, idempotency_key: idempotencyKey });
    const handle = recoveryHandle(scope, idempotencyKey, requestDigest);
    return store.transact(episodeId, async episode => {
      const priorIdempotency = episode.idempotency.get(scopedKey);
      if (priorIdempotency) {
        if (priorIdempotency.request_digest !== requestDigest) {
          return { status: 'invalid_request', diagnostic: { code: 'IDEMPOTENCY_MISMATCH' }, receipt: null, recovery_handle: null, ...semanticClosure };
        }
        return { status: 'replayed', receipt: priorIdempotency.receipt, replayed_at: clock(), recovery_handle: null, diagnostic: null, ...semanticClosure };
      }

      const tail = episode.events.at(-1) ?? null;
      const actualRevision = tail?.revision ?? 0;
      const actualTailDigest = tail?.event_digest ?? null;
      if (expectedRevision !== actualRevision || proposedEvent.revision !== actualRevision + 1 || expectedTailDigest !== actualTailDigest) {
        return { status: 'conflict', diagnostic: { code: 'REVISION_CONFLICT', actual_revision: actualRevision, actual_tail_digest: actualTailDigest }, receipt: null, recovery_handle: null, ...semanticClosure };
      }

      if (failurePoint === 'before_commit') {
        store.recovery.set(handle, { scope: structuredClone(scope), receipt: null });
        return { status: 'temporary_failure', append_outcome: 'not_committed', recovery_handle: handle, receipt: null, diagnostic: { code: 'STORE_UNAVAILABLE' }, ...semanticClosure };
      }

      const recordedAt = clock();
      const withoutDigest = {
        contract: 'animejs-work-episode-event/0.1.0',
        event_id: null,
        episode_id: episodeId,
        revision: proposedEvent.revision,
        event_type: proposedEvent.event_type,
        command_id: proposedEvent.command_id,
        request_digest: requestDigest,
        principal_id: scope.principal_id,
        policy_epoch: scope.policy_epoch,
        graph_digest: proposedEvent.graph_digest,
        recorded_at: recordedAt,
        payload: proposedEvent.payload,
        prior_event_digest: actualTailDigest,
      };
      const identityDigest = sha256(withoutDigest);
      const event = { ...withoutDigest, event_id: idFactory(identityDigest) };
      event.event_digest = sha256(event);
      const receipt = {
        event_id: event.event_id,
        episode_id: episodeId,
        prior_revision: actualRevision,
        new_revision: event.revision,
        event_digest: event.event_digest,
        journal_tail_digest: event.event_digest,
        graph_digest: event.graph_digest,
        reducer_status: 'pending',
        ...semanticClosure,
      };

      episode.events.push(event);
      episode.idempotency.set(scopedKey, { request_digest: requestDigest, receipt });
      store.recovery.set(handle, { scope: structuredClone(scope), receipt });

      if (failurePoint === 'after_commit') {
        return { status: 'temporary_failure', append_outcome: 'committed_receipt_unavailable', recovery_handle: handle, receipt: null, diagnostic: { code: 'RECEIPT_UNAVAILABLE' }, ...semanticClosure };
      }
      return { status: 'accepted', receipt, recovery_handle: null, diagnostic: null, ...semanticClosure };
    });
  }

  function recover({ scope, recoveryHandle: handle }) {
    const entry = store.recovery.get(handle);
    if (!entry || !sameScope(entry.scope, scope)) return { status: 'denied', receipt: null, diagnostic: { code: 'DENIED' }, ...semanticClosure };
    if (!entry.receipt) return { status: 'not_committed', receipt: null, diagnostic: null, ...semanticClosure };
    return { status: 'accepted', receipt: structuredClone(entry.receipt), diagnostic: null, ...semanticClosure };
  }

  return { append, recover, events: episodeId => store.events(episodeId), store, canonicalRequestDigest: command => sha256(JSON.parse(canonicalJson(command))) };
}
