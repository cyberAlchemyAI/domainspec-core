function copy(value) {
  return structuredClone(value);
}

function requireObject(value, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new TypeError(`${label} must be an object`);
  }
}

function sortedUnique(values) {
  return [...new Set(values)].sort((left, right) => left.localeCompare(right));
}

export function buildCandidate(sceneBeat, residue) {
  requireObject(sceneBeat, 'sceneBeat');
  requireObject(residue, 'residue');
  const required = [
    'candidate_id', 'hypothesis', 'semantic_contract', 'proof_ledger',
    'contradiction', 'prototype_scope', 'witness_spec', 'tournament_binding',
    'owner_review', 'consultation_request_id', 'version_context',
    'preconsultation_evidence_bindings',
  ];
  for (const field of required) {
    if (!Object.hasOwn(residue, field)) throw new TypeError(`residue.${field} is required`);
  }
  if (!Array.isArray(residue.preconsultation_evidence_bindings)
      || residue.preconsultation_evidence_bindings.length === 0) {
    throw new TypeError('residue.preconsultation_evidence_bindings must be non-empty');
  }

  return {
    schema_version: 'animation-hypothesis-candidate.v0.1',
    candidate_id: residue.candidate_id,
    scene_beat_ref: copy(sceneBeat),
    hypothesis: copy(residue.hypothesis),
    semantic_contract: copy(residue.semantic_contract),
    consultation: {
      request_id: residue.consultation_request_id,
      audience: 'animejs-knowledge-consult-read',
      query_scope: 'Timeline, SVG, and createDrawable documentation evidence for the S6 typed-relation edge draw.',
      version_context: copy(residue.version_context),
      evidence_bindings: sortedUnique(residue.preconsultation_evidence_bindings),
      status: 'abstain',
      claim_limit: 'Pre-consultation OAVA-001 source binding only; no current Anime.js evidence or runtime claim.',
    },
    proof_ledger: copy(residue.proof_ledger),
    contradiction: copy(residue.contradiction),
    prototype_scope: copy(residue.prototype_scope),
    witness_spec: copy(residue.witness_spec),
    tournament_binding: copy(residue.tournament_binding),
    owner_review: copy(residue.owner_review),
    lineage: {
      work_pack_id: 'WP-OAVA-S6-002',
      swu_id: 'SWU-OAVA-002',
      parent_candidate_id: residue.candidate_id,
      parent_swu_id: 'SWU-OAVA-001',
    },
  };
}

export function bindConsultation(candidate, consultationReceipt) {
  requireObject(candidate, 'candidate');
  requireObject(consultationReceipt, 'consultationReceipt');
  const result = consultationReceipt.result;
  if (!result || result.status !== 'ok') {
    throw new TypeError('only an ok consultation receipt can bind a candidate');
  }
  const evidenceBindings = sortedUnique(consultationReceipt.evidence_bindings ?? []);
  if (evidenceBindings.length === 0) {
    throw new TypeError('an ok consultation receipt requires evidence bindings');
  }
  const priorProof = candidate.proof_ledger.filter(
    (entry) => entry.owner !== 'animejs-knowledge-consultation',
  );
  const documentedCapability = {
    claim: 'The local Anime.js vault documents timeline, SVG, and createDrawable capabilities relevant to the proposed edge draw.',
    proof_state: 'documented_capability',
    evidence_refs: evidenceBindings,
    limitations: [
      'Documentation evidence does not prove runtime behavior or visual quality.',
      'The planned motion still requires a later local Anime.js browser witness.',
    ],
    owner: 'animejs-knowledge-consultation',
  };

  return {
    ...copy(candidate),
    candidate_id: `${candidate.candidate_id}-consult-${result.projection_digest.slice(0, 12)}`,
    consultation: {
      request_id: result.request_id,
      audience: 'animejs-knowledge-consult-read',
      query_scope: consultationReceipt.request.query.node_ids.join(','),
      version_context: copy(consultationReceipt.version_context),
      evidence_bindings: evidenceBindings,
      status: 'ok',
      claim_limit: 'Current local documentation evidence only; no Anime.js runtime, browser, or visual-quality proof.',
    },
    proof_ledger: [...priorProof, documentedCapability],
    lineage: {
      ...copy(candidate.lineage),
      parent_candidate_id: candidate.candidate_id,
      consultation_request_digest: consultationReceipt.request_digest,
      graph_digest: result.graph_digest,
      projection_digest: result.projection_digest,
    },
  };
}

export const internals = { sortedUnique };
