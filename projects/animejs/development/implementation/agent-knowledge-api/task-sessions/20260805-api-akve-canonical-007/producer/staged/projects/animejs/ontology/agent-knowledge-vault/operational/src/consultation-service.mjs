const READ_AUDIENCE = 'animejs-knowledge-consult-read';
const operations = new Set(['lookup', 'search', 'context', 'coverage', 'decision', 'episode']);
const topFields = new Set(['contract', 'operation', 'query', 'limits', 'expected']);
const queryFields = new Set(['text', 'node_ids', 'task_id', 'episode_id', 'version_context_id', 'relation_types', 'evidence_states']);
const limitFields = new Set(['max_results', 'max_hops', 'max_response_bytes']);
const expectedFields = new Set(['graph_digest', 'projection_digest']);
const hostFields = new Set(['principal_id', 'tenant_or_workspace_id', 'capabilities', 'policy_epoch', 'vault_scope', 'request_id', 'received_at']);
const zeroDigest = '0'.repeat(64);

function hasUnknown(value, allowed) {
  return !value || typeof value !== 'object' || Array.isArray(value) || Object.keys(value).some(key => !allowed.has(key));
}

function hasExactFields(value, allowed) {
  return !hasUnknown(value, allowed) && Object.keys(value).length === allowed.size;
}

function validOptionalDigest(value) {
  return value === null || (typeof value === 'string' && /^[a-f0-9]{64}$/.test(value));
}

function uniqueBoundedStrings(value, maximum, length) {
  return Array.isArray(value) && value.length <= maximum && new Set(value).size === value.length && value.every(item => typeof item === 'string' && item.length <= length);
}

function containsHostField(value) {
  if (!value || typeof value !== 'object') return false;
  return Object.entries(value).some(([key, child]) => hostFields.has(key) || containsHostField(child));
}

function validRequest(request) {
  if (!hasExactFields(request, topFields) || containsHostField(request)) return false;
  if (request.contract !== 'animejs-knowledge-consult-request/0.1.0' || !operations.has(request.operation)) return false;
  if (!hasExactFields(request.query, queryFields) || !hasExactFields(request.limits, limitFields) || !hasExactFields(request.expected, expectedFields)) return false;
  const { max_results, max_hops, max_response_bytes } = request.limits;
  return Number.isInteger(max_results) && max_results > 0
    && max_results <= 50
    && Number.isInteger(max_hops) && max_hops >= 0
    && max_hops <= 4
    && Number.isInteger(max_response_bytes) && max_response_bytes >= 512 && max_response_bytes <= 262144
    && typeof request.query.text === 'string' && request.query.text.length <= 4000
    && uniqueBoundedStrings(request.query.node_ids, 50, 160)
    && [request.query.task_id, request.query.episode_id, request.query.version_context_id].every(value => value === null || (typeof value === 'string' && value.length <= 160))
    && uniqueBoundedStrings(request.query.relation_types, 30, 120)
    && uniqueBoundedStrings(request.query.evidence_states, 10, 40)
    && request.query.evidence_states.every(state => ['admissible', 'unconfirmed', 'revoked', 'unavailable', 'not_applicable'].includes(state))
    && validOptionalDigest(request.expected.graph_digest)
    && validOptionalDigest(request.expected.projection_digest);
}

function defaultQuery(projection, request) {
  let records = projection.records ?? [];
  const query = request.query;
  if (request.operation === 'lookup' && query.node_ids.length) records = records.filter(record => query.node_ids.includes(record.record_id));
  if (request.operation === 'episode' && query.episode_id) records = records.filter(record => record.record_id.includes(query.episode_id));
  if (['search', 'context', 'coverage', 'decision'].includes(request.operation) && query.text) {
    const terms = query.text.toLocaleLowerCase().split(/\s+/).filter(Boolean);
    records = records.filter(record => terms.some(term => `${record.label} ${record.summary}`.toLocaleLowerCase().includes(term)));
  }
  if (query.evidence_states.length) records = records.filter(record => query.evidence_states.includes(record.evidence_state));
  const ids = new Set(records.map(record => record.record_id));
  const edges = (projection.edges ?? []).filter(edge => ids.has(edge.from_record_id) && ids.has(edge.to_record_id));
  return { records, edges, explanation_path: records.map(record => record.record_id), ambiguous: false, unsupported_claim: false };
}

export function createConsultationService({ projectionReader, clock = () => new Date().toISOString() }) {
  if (!projectionReader?.read) throw new TypeError('projectionReader.read is required');

  function common(hostContext, status, graphDigest, projectionDigest, records = [], edges = [], explanationPath = [], diagnostic = null) {
    return {
      contract: 'animejs-knowledge-consult-result/0.1.0', request_id: hostContext.request_id,
      graph_digest: graphDigest, projection_digest: projectionDigest, policy_epoch: hostContext.policy_epoch,
      generated_at: clock(), status, semantic_effect: 'none', task_state_unchanged: true, truth_status: 'not_assessed',
      records, edges, explanation_path: explanationPath, diagnostic,
    };
  }

  async function consult({ hostContext, grant, request }) {
    if (!grant?.authorized || grant.capability_audience !== READ_AUDIENCE) {
      return common(hostContext, 'denied', zeroDigest, zeroDigest, [], [], [], { code: 'DENIED' });
    }
    if (!validRequest(request)) return common(hostContext, 'invalid_request', zeroDigest, zeroDigest, [], [], [], { code: 'INVALID_REQUEST' });
    const caps = grant.limits ?? { max_results: 12, max_hops: 2, max_response_bytes: 65536 };
    if (request.limits.max_results > caps.max_results || request.limits.max_hops > caps.max_hops || request.limits.max_response_bytes > caps.max_response_bytes) {
      return common(hostContext, 'invalid_request', zeroDigest, zeroDigest, [], [], [], { code: 'LIMIT_EXCEEDS_GRANT' });
    }

    const projection = await projectionReader.read({ views: grant.views ?? [] });
    const graphDigest = projection.manifest?.source_graph_digest ?? zeroDigest;
    const projectionDigest = projection.manifest?.projection_digest ?? zeroDigest;
    if (['pending', 'failed', 'rejected', 'corrupt'].includes(projection.status)) {
      const code = projection.status === 'pending' ? 'PROJECTION_PENDING' : projection.status === 'failed' ? 'PROJECTION_FAILED' : 'PROJECTION_CORRUPT';
      return common(hostContext, 'temporary_failure', graphDigest, projectionDigest, [], [], [], { code, retryable: projection.status === 'pending' });
    }
    if ((request.expected.graph_digest && request.expected.graph_digest !== graphDigest) || (request.expected.projection_digest && request.expected.projection_digest !== projectionDigest)) {
      return common(hostContext, 'stale', graphDigest, projectionDigest, [], [], [], {
        code: 'STALE_PROJECTION', expected: request.expected, actual: { graph_digest: graphDigest, projection_digest: projectionDigest },
      });
    }
    if (request.operation === 'decision' && !request.query.version_context_id) {
      return common(hostContext, 'abstain', graphDigest, projectionDigest, [], [], [], { code: 'ABSTAIN_VERSION_CONTEXT_REQUIRED' });
    }

    const queried = projectionReader.query ? await projectionReader.query(projection, request) : defaultQuery(projection, request);
    if (queried.ambiguous) return common(hostContext, 'abstain', graphDigest, projectionDigest, [], [], [], { code: 'ABSTAIN_AMBIGUOUS_INTENT', clearing_criteria: queried.clearing_criteria ?? [] });
    if (queried.unsupported_claim) return common(hostContext, 'abstain', graphDigest, projectionDigest, [], [], [], { code: 'ABSTAIN_UNSUPPORTED_CLAIM', clearing_criteria: queried.clearing_criteria ?? [] });

    if ((queried.records ?? []).length > request.limits.max_results || (queried.explanation_path ?? []).length > request.limits.max_results) {
      return common(hostContext, 'invalid_request', graphDigest, projectionDigest, [], [], [], { code: 'RESULT_BUDGET_EXCEEDED' });
    }
    const edgeLimit = request.limits.max_hops === 0 ? 0 : request.limits.max_results * request.limits.max_hops;
    if ((queried.hops ?? 0) > request.limits.max_hops || (queried.edges ?? []).length > edgeLimit) {
      return common(hostContext, 'invalid_request', graphDigest, projectionDigest, [], [], [], { code: 'TRAVERSAL_BUDGET_EXCEEDED' });
    }
    const records = queried.records ?? [];
    if (!records.length) return common(hostContext, 'abstain', graphDigest, projectionDigest, [], [], [], { code: 'ABSTAIN_NO_ADMISSIBLE_EVIDENCE' });
    const recordIds = new Set(records.map(record => record.record_id));
    const edges = (queried.edges ?? []).filter(edge => recordIds.has(edge.from_record_id) && recordIds.has(edge.to_record_id));
    const explanationPath = (queried.explanation_path ?? records.map(record => record.record_id)).filter(id => recordIds.has(id));
    const result = common(hostContext, 'ok', graphDigest, projectionDigest, records, edges, explanationPath, projection.status === 'quarantined' ? { code: 'EPISODE_QUARANTINED', quarantined: projection.quarantined ?? [] } : null);
    if (Buffer.byteLength(JSON.stringify(result)) > request.limits.max_response_bytes) {
      return common(hostContext, 'invalid_request', graphDigest, projectionDigest, [], [], [], { code: 'RESPONSE_BUDGET_EXCEEDED' });
    }
    return result;
  }

  return { consult };
}
