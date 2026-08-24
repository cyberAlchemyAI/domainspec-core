import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const AUDIENCE = 'animejs-knowledge-consult-read';
const VERSION_CONTEXT_ID = 'animejs@4.5.0';
const LOOKUP_NODE_IDS = Object.freeze([
  'recipe:consult:timeline',
  'recipe:consult:svg',
  'topic:documentation:svg/createdrawable',
]);
const ZERO_DIGEST = '0'.repeat(64);

function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value !== null && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

function digest(value) {
  return createHash('sha256').update(canonical(value)).digest('hex');
}

async function loadJson(filePath) {
  return JSON.parse(await readFile(filePath, 'utf8'));
}

function recipeRecord(recipe) {
  return {
    record_id: recipe.id,
    label: recipe.id.replace('recipe:consult:', 'Anime.js '),
    summary: [...recipe.ordered_steps, recipe.validation_requirement].join(' '),
    record_kind: 'recipe',
    source_handle: recipe.evidence_record_ids[0],
    evidence_state: 'admissible',
    version_bounds: { exact: '4.5.0' },
    truth_status: 'not_assessed',
    clearing_criteria: [recipe.validation_requirement],
  };
}

function documentationRecord(route) {
  return {
    record_id: route.id,
    label: route.title,
    summary: `${route.canonical_path} is present in the validated local Anime.js documentation projection.`,
    record_kind: 'documentation',
    source_handle: route.evidence_record_ids[0],
    evidence_state: 'admissible',
    version_bounds: { exact: '4.5.0' },
    truth_status: 'not_assessed',
    clearing_criteria: ['Project-specific execution evidence is required before claiming runtime behavior.'],
  };
}

function failureResult(hostContext, status, code) {
  return {
    contract: 'animejs-knowledge-consult-result/0.1.0',
    request_id: hostContext.request_id,
    graph_digest: ZERO_DIGEST,
    projection_digest: ZERO_DIGEST,
    policy_epoch: hostContext.policy_epoch,
    generated_at: hostContext.received_at,
    status,
    semantic_effect: 'none',
    task_state_unchanged: true,
    truth_status: 'not_assessed',
    records: [],
    edges: [],
    explanation_path: [],
    diagnostic: { code },
  };
}

function evidenceBindings(result) {
  if (result.status !== 'ok') return [];
  return [...new Set(result.records.map((record) => record.source_handle).filter(Boolean))]
    .sort((left, right) => left.localeCompare(right));
}

export async function consultCandidate(candidate, host) {
  if (!candidate || typeof candidate !== 'object') throw new TypeError('candidate is required');
  if (!host || typeof host !== 'object') throw new TypeError('host context is required');
  if (candidate.consultation?.request_id !== host.host_context?.request_id) {
    const result = failureResult(host.host_context, 'invalid_request', 'REQUEST_ID_MISMATCH');
    return {
      contract: 'oava-animejs-consultation-receipt/0.1.0',
      host_request_id: host.host_context.request_id,
      request: null,
      request_digest: null,
      version_context: structuredClone(candidate.consultation?.version_context ?? {}),
      current_projection: { graph_digest: ZERO_DIGEST, projection_digest: ZERO_DIGEST, version_context_id: VERSION_CONTEXT_ID },
      result,
      evidence_bindings: [],
      semantic_effect: 'none',
      claim_limit: 'Consultation failed before evidence lookup; no runtime proof.',
    };
  }

  const vaultRoot = path.resolve(host.vault_root);
  const modulePath = (relative) => pathToFileURL(path.join(vaultRoot, relative)).href;
  const [{ createCapabilityAdapters }, { createConsultationService }, { compileNeutralProjection }] = await Promise.all([
    import(modulePath('operational/src/capability-adapters.mjs')),
    import(modulePath('operational/src/consultation-service.mjs')),
    import(modulePath('operational/src/projection.mjs')),
  ]);

  let currentProjection = null;
  const projectionReader = {
    read: async () => {
      const [allowlist, recipesView, documentationView] = await Promise.all([
        loadJson(path.join(vaultRoot, 'operational/contracts/projection-allowlist.json')),
        loadJson(path.join(vaultRoot, 'views/task-recipes.json')),
        loadJson(path.join(vaultRoot, 'views/documentation-coverage.json')),
      ]);
      if (recipesView.graph_digest !== documentationView.graph_digest) {
        return { status: 'rejected', records: [] };
      }
      const recipes = recipesView.recipes
        .filter((recipe) => LOOKUP_NODE_IDS.includes(recipe.id))
        .map(recipeRecord);
      const documentation = documentationView.routes
        .filter((route) => LOOKUP_NODE_IDS.includes(route.id))
        .map(documentationRecord);
      const records = [...recipes, ...documentation];
      if (records.length !== LOOKUP_NODE_IDS.length) return { status: 'rejected', records: [] };
      currentProjection = compileNeutralProjection({
        baseRecords: records,
        overlay: { status: 'current', records: [], canonical_graph_digest: recipesView.graph_digest, quarantined: [] },
        allowlist,
        requestedViews: ['documentation', 'recipe'],
        grantedViews: ['documentation', 'recipe'],
        ownerReviewRef: 'oava002:consumer-projection',
      });
      return currentProjection;
    },
  };

  const service = createConsultationService({
    projectionReader,
    clock: () => host.host_context.received_at,
  });
  const adapters = createCapabilityAdapters({
    authorize: host.authorize,
    consultationService: service,
    episodeService: null,
    projectReader: null,
    audit: host.audit ?? (async () => {}),
  });
  const request = {
    contract: 'animejs-knowledge-consult-request/0.1.0',
    operation: 'lookup',
    query: {
      text: '',
      node_ids: [...LOOKUP_NODE_IDS],
      task_id: 'TASK-OAVA-CONSULTATION',
      episode_id: null,
      version_context_id: VERSION_CONTEXT_ID,
      relation_types: [],
      evidence_states: ['admissible'],
    },
    limits: structuredClone(host.limits),
    expected: structuredClone(host.expected),
  };

  let result;
  try {
    result = await adapters.invoke({
      descriptor: { capability: AUDIENCE },
      credential: host.credential,
      hostContext: host.host_context,
      body: request,
    });
  } catch {
    result = failureResult(host.host_context, 'temporary_failure', 'PROJECTION_LOAD_FAILED');
  }
  const graphDigest = currentProjection?.manifest?.source_graph_digest ?? result.graph_digest;
  const projectionDigest = currentProjection?.manifest?.projection_digest ?? result.projection_digest;
  return {
    contract: 'oava-animejs-consultation-receipt/0.1.0',
    host_request_id: host.host_context.request_id,
    request,
    request_digest: digest(request),
    version_context: structuredClone(candidate.consultation.version_context),
    current_projection: { graph_digest: graphDigest, projection_digest: projectionDigest, version_context_id: VERSION_CONTEXT_ID },
    result,
    evidence_bindings: evidenceBindings(result),
    semantic_effect: 'none',
    claim_limit: 'Local documentation consultation only; no Anime.js runtime, browser, or visual-quality proof.',
  };
}

export const consultationContract = Object.freeze({
  audience: AUDIENCE,
  version_context_id: VERSION_CONTEXT_ID,
  node_ids: [...LOOKUP_NODE_IDS],
});
