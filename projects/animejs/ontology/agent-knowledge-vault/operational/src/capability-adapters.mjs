const CAPABILITIES = Object.freeze({
  'animejs-knowledge-consult-read': { kind: 'consult', contract: 'animejs-knowledge-consult-request/0.1.0' },
  'animejs-work-episode-append': { kind: 'append', contract: 'animejs-work-episode-command/0.1.0' },
  'animejs-work-episode-receipt-read': { kind: 'receipt', contract: 'animejs-work-episode-receipt-request/0.1.0' },
  'animejs-work-episode-project-read': { kind: 'project', contract: 'animejs-work-episode-project-request/0.1.0' },
});
const hostFields = new Set(['principal_id', 'tenant_or_workspace_id', 'capabilities', 'policy_epoch', 'vault_scope', 'request_id', 'received_at', 'capability_audience']);
const zeroDigest = '0'.repeat(64);

function containsHostField(value) {
  if (!value || typeof value !== 'object') return false;
  return Object.entries(value).some(([key, child]) => hostFields.has(key) || containsHostField(child));
}

function denied(kind, hostContext) {
  if (kind === 'consult') return { contract: 'animejs-knowledge-consult-result/0.1.0', request_id: hostContext.request_id, graph_digest: zeroDigest, projection_digest: zeroDigest, policy_epoch: hostContext.policy_epoch, generated_at: hostContext.received_at, status: 'denied', semantic_effect: 'none', task_state_unchanged: true, truth_status: 'not_assessed', records: [], edges: [], explanation_path: [], diagnostic: { code: 'DENIED' } };
  if (kind === 'append' || kind === 'receipt') return { contract: 'animejs-work-episode-result/0.1.0', request_id: hostContext.request_id, status: 'denied', semantic_effect: 'none', task_state_unchanged: true, truth_status: 'not_assessed', receipt: null, diagnostic: { code: 'DENIED' }, recovery_handle: null };
  return { contract: 'animejs-work-episode-project-result/0.1.0', request_id: hostContext.request_id, status: 'denied', semantic_effect: 'none', task_state_unchanged: true, truth_status: 'not_assessed', project: null, diagnostic: { code: 'DENIED' } };
}

function invalid(kind, hostContext) {
  const result = denied(kind, hostContext);
  result.status = 'invalid_request';
  result.diagnostic = { code: 'INVALID_REQUEST' };
  return result;
}

function routeBodyValid(kind, body) {
  if (kind === 'receipt') return Object.keys(body).length === 2 && typeof body.recovery_handle === 'string' && body.recovery_handle.length > 0;
  if (kind === 'project') return Object.keys(body).length === 2 && (body.episode_id === null || (typeof body.episode_id === 'string' && body.episode_id.length > 0));
  return true;
}

export function createCapabilityAdapters({ authorize, consultationService, episodeService, projectReader, audit = async () => {} }) {
  if (typeof authorize !== 'function') throw new TypeError('authorize port is required');

  async function invoke({ descriptor, credential, hostContext, body }) {
    const capability = descriptor?.capability;
    const route = CAPABILITIES[capability];
    if (!route) return denied('project', hostContext);
    const exactAudience = typeof credential?.audience === 'string'
      && credential.audience === capability
      && credential.audience !== '*'
      && !credential.audience.includes(',');
    if (!exactAudience) {
      const result = denied(route.kind, hostContext);
      await audit({ capability, dimension: route.kind, outcome: 'denied', reason: 'audience_mismatch', request_id: hostContext.request_id });
      return result;
    }

    const authorization = await authorize({ capability, credential, hostContext });
    if (!authorization?.authorized) {
      const result = denied(route.kind, hostContext);
      await audit({ capability, dimension: route.kind, outcome: 'denied', reason: 'policy', request_id: hostContext.request_id });
      return result;
    }
    if (!body || body.contract !== route.contract) {
      const result = denied(route.kind, hostContext);
      await audit({ capability, dimension: route.kind, outcome: 'denied', reason: 'body_capability_mismatch', request_id: hostContext.request_id });
      return result;
    }
    if (containsHostField(body)) {
      const result = invalid(route.kind, hostContext);
      await audit({ capability, dimension: route.kind, outcome: 'invalid_request', reason: 'host_field_spoof', request_id: hostContext.request_id });
      return result;
    }
    if (!routeBodyValid(route.kind, body)) {
      const result = invalid(route.kind, hostContext);
      await audit({ capability, dimension: route.kind, outcome: 'invalid_request', reason: 'closed_body_violation', request_id: hostContext.request_id });
      return result;
    }

    const grant = { ...authorization, capability_audience: capability };
    let result;
    if (route.kind === 'consult') result = await consultationService.consult({ hostContext, grant, request: body });
    if (route.kind === 'append') result = await episodeService.appendCommand({ hostContext, grant, command: body });
    if (route.kind === 'receipt') result = await episodeService.recoverReceipt({ hostContext, grant, recoveryHandle: body.recovery_handle });
    if (route.kind === 'project') {
      const project = await projectReader.read({ hostContext, grant, episodeId: body.episode_id ?? null });
      const projectStates = new Set(['current', 'pending', 'failed', 'corrupt', 'quarantined']);
      result = projectStates.has(project.status)
        ? { contract: 'animejs-work-episode-project-result/0.1.0', request_id: hostContext.request_id, status: project.status, semantic_effect: 'none', task_state_unchanged: true, truth_status: 'not_assessed', project: project.project ?? null, diagnostic: project.diagnostic ?? null }
        : { contract: 'animejs-work-episode-project-result/0.1.0', request_id: hostContext.request_id, status: 'temporary_failure', semantic_effect: 'none', task_state_unchanged: true, truth_status: 'not_assessed', project: null, diagnostic: { code: 'PROJECTION_CORRUPT' } };
    }
    await audit({ capability, dimension: route.kind, outcome: result.status, reason: null, request_id: hostContext.request_id });
    return result;
  }

  return { invoke, capabilities: Object.keys(CAPABILITIES) };
}
