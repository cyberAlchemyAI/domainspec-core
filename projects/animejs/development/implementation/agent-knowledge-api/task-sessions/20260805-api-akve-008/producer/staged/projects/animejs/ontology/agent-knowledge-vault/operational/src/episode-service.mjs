import { decideTransition } from './transition-oracle.mjs';
import { sha256 } from './canonical-json.mjs';

const APPEND_AUDIENCE = 'animejs-work-episode-append';
const RECEIPT_AUDIENCE = 'animejs-work-episode-receipt-read';
const operations = new Set(['open_episode', 'append_attempt', 'attach_evidence', 'record_outcome', 'close_episode']);
const hostFields = new Set(['principal_id', 'tenant_or_workspace_id', 'capabilities', 'policy_epoch', 'vault_scope', 'request_id', 'received_at', 'capability_audience']);
const topFields = new Set(['contract', 'command_id', 'idempotency_key', 'operation', 'episode_id', 'expected_revision', 'expected_graph_digest', 'payload']);
const payloadContracts = {
  open_episode: { required: ['task_handle', 'version_context_handle', 'goal', 'started_at'], allowed: ['task_handle', 'version_context_handle', 'goal', 'started_at', 'tags', 'supersedes_episode_id'] },
  append_attempt: { required: ['ordinal', 'action_summary', 'input_artifact_handles'], allowed: ['ordinal', 'action_summary', 'input_artifact_handles'] },
  attach_evidence: { required: ['attempt_ordinal', 'evidence_handle'], allowed: ['attempt_ordinal', 'evidence_handle'] },
  record_outcome: { required: ['attempt_ordinal', 'classification', 'observations', 'witness_handles'], allowed: ['attempt_ordinal', 'classification', 'observations', 'witness_handles'] },
  close_episode: { required: ['disposition'], allowed: ['disposition'] },
};
const reservedSnapshotFields = new Set(['owner', 'owner_route', 'approval', 'approvals', 'route', 'routing', 'capabilities', 'policy', 'policy_epoch', 'authority', 'authority_effect', 'release', 'release_state', 'promotion', 'secret', 'credentials']);

function containsHostField(value) {
  if (!value || typeof value !== 'object') return false;
  return Object.entries(value).some(([key, child]) => hostFields.has(key) || containsHostField(child));
}

function validCommand(command) {
  if (!command || typeof command !== 'object' || Array.isArray(command) || Object.keys(command).some(key => !topFields.has(key)) || containsHostField(command)) return false;
  if (command.contract !== 'animejs-work-episode-command/0.1.0' || !operations.has(command.operation)) return false;
  const contract = payloadContracts[command.operation];
  if (!command.payload || typeof command.payload !== 'object' || Array.isArray(command.payload)) return false;
  if (contract.required.some(key => !(key in command.payload)) || Object.keys(command.payload).some(key => !contract.allowed.includes(key))) return false;
  if (command.operation === 'open_episode') return command.episode_id === null && command.expected_revision === 0;
  return typeof command.episode_id === 'string' && command.episode_id.length > 0 && Number.isInteger(command.expected_revision) && command.expected_revision > 0;
}

function sanitizeSnapshot(value) {
  if (Array.isArray(value)) return value.map(sanitizeSnapshot);
  if (!value || typeof value !== 'object') return value;
  return Object.fromEntries(Object.entries(value).filter(([key]) => !reservedSnapshotFields.has(key)).map(([key, child]) => [key, sanitizeSnapshot(child)]));
}

function semanticResult(hostContext, status, receipt = null, diagnostic = null, recoveryHandle = null) {
  return {
    contract: 'animejs-work-episode-result/0.1.0', request_id: hostContext.request_id, status,
    semantic_effect: 'none', task_state_unchanged: true, truth_status: 'not_assessed',
    receipt, diagnostic, recovery_handle: recoveryHandle,
  };
}

function oracleResult(hostContext, decision) {
  return semanticResult(hostContext, decision.status, null, { code: decision.code }, null);
}

export function createEpisodeService({ journal, taskResolver, versionContextResolver, evidenceResolver, episodeReader, reducerScheduler, supersessionChecker = async () => ({ terminal: false, cycle: false }), episodeIdFactory = ({ hostContext, command }) => `episode:${sha256({ principal_id: hostContext.principal_id, tenant_or_workspace_id: hostContext.tenant_or_workspace_id, vault_scope: hostContext.vault_scope, idempotency_key: command.idempotency_key }).slice(0, 32)}` }) {
  for (const [name, port] of Object.entries({ journal, taskResolver, versionContextResolver, evidenceResolver, episodeReader, reducerScheduler })) {
    if (!port) throw new TypeError(`${name} port is required`);
  }

  function journalScope(hostContext, operation) {
    return { principal_id: hostContext.principal_id, tenant_or_workspace_id: hostContext.tenant_or_workspace_id, vault_scope: hostContext.vault_scope, capability_audience: APPEND_AUDIENCE, policy_epoch: hostContext.policy_epoch, operation };
  }

  async function appendCommand({ hostContext, grant, command, failurePoint = null }) {
    if (!grant?.authorized || grant.capability_audience !== APPEND_AUDIENCE) return semanticResult(hostContext, 'denied', null, { code: 'DENIED' });
    if (!validCommand(command)) return semanticResult(hostContext, 'invalid_request', null, { code: 'INVALID_REQUEST' });
    const requestDigest = journal.canonicalRequestDigest(command);
    const episodeId = command.operation === 'open_episode' ? episodeIdFactory({ hostContext, command }) : command.episode_id;
    let state = await episodeReader.readState(episodeId);
    const bindings = {
      episode_id: episodeId, principal_id: hostContext.principal_id, tenant_or_workspace_id: hostContext.tenant_or_workspace_id,
      vault_scope: hostContext.vault_scope, capability_audience: APPEND_AUDIENCE, delegation_id: grant.delegation_id ?? null,
    };

    if (command.operation === 'open_episode' && state) {
      const replay = await journal.append({ scope: journalScope(hostContext, command.operation), requestDigest, proposedEvent: { episode_id: episodeId, revision: 1, event_type: 'EpisodeOpened', command_id: command.command_id, graph_digest: command.expected_graph_digest, payload: {} }, expectedRevision: 0, expectedTailDigest: null, idempotencyKey: command.idempotency_key, failurePoint });
      return semanticResult(hostContext, replay.status, replay.receipt, replay.diagnostic, replay.recovery_handle);
    }

    let resolvedEvidence = null;
    if (command.operation === 'open_episode') {
      const [task, version] = await Promise.all([
        taskResolver.resolve(command.payload.task_handle, hostContext),
        versionContextResolver.resolve(command.payload.version_context_handle, hostContext),
      ]);
      if (!task?.snapshot || !task.digest || !version?.snapshot || !version.digest) return semanticResult(hostContext, 'invalid_request', null, { code: 'HOST_BINDING_REQUIRED' });
      bindings.task_snapshot = sanitizeSnapshot(task.snapshot);
      bindings.task_digest = task.digest;
      bindings.version_context_snapshot = sanitizeSnapshot(version.snapshot);
      bindings.version_context_digest = version.digest;
      if (command.payload.supersedes_episode_id) {
        const supersession = await supersessionChecker(command.payload.supersedes_episode_id, episodeId, hostContext);
        bindings.superseded_episode = { terminal: supersession.terminal === true };
        bindings.supersession_cycle = supersession.cycle === true;
      }
    } else if (command.operation === 'attach_evidence') {
      const evidence = await evidenceResolver.resolve(command.payload.evidence_handle, {
        hostContext, episode_id: state?.episode_id, attempt_ordinal: command.payload.attempt_ordinal,
        task_digest: state?.task_digest, version_context_digest: state?.version_context_digest,
      });
      if (!evidence?.accepted) return semanticResult(hostContext, 'evidence_rejected', null, { code: evidence?.code ?? 'EVIDENCE_HANDLE_REVOKED' });
      resolvedEvidence = sanitizeSnapshot(evidence.binding);
    }

    const decision = decideTransition({ state, command, bindings, resolvedEvidence });
    if (!decision.accepted) return oracleResult(hostContext, decision);
    const appendResult = await journal.append({
      scope: journalScope(hostContext, command.operation), requestDigest,
      proposedEvent: decision.event, expectedRevision: command.expected_revision,
      expectedTailDigest: state?.last_event_digest ?? null, idempotencyKey: command.idempotency_key, failurePoint,
    });
    if (!['accepted', 'replayed'].includes(appendResult.status)) return semanticResult(hostContext, appendResult.status, appendResult.receipt, appendResult.diagnostic, appendResult.recovery_handle);
    let reducerStatus = appendResult.receipt.reducer_status;
    try {
      reducerStatus = await reducerScheduler.schedule(episodeId);
    } catch {
      reducerStatus = 'failed';
    }
    return semanticResult(hostContext, appendResult.status, { ...appendResult.receipt, reducer_status: reducerStatus }, appendResult.diagnostic, appendResult.recovery_handle);
  }

  function recoverReceipt({ hostContext, grant, recoveryHandle }) {
    if (!grant?.authorized || grant.capability_audience !== RECEIPT_AUDIENCE) return semanticResult(hostContext, 'denied', null, { code: 'DENIED' });
    const recovered = journal.recover({ scope: journalScope(hostContext, 'recover_receipt'), recoveryHandle });
    if (recovered.status === 'not_committed') return semanticResult(hostContext, 'temporary_failure', null, { code: 'NOT_COMMITTED' });
    return semanticResult(hostContext, recovered.status, recovered.receipt, recovered.diagnostic);
  }

  return { appendCommand, recoverReceipt };
}
