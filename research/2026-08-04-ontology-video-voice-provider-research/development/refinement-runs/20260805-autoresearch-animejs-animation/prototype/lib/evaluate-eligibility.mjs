import { bindConsultation } from './build-candidate.mjs';

function blocked(code, state, result, diagnostic = null) {
  return {
    eligible: false,
    code,
    state,
    consultation_status: result?.status ?? null,
    diagnostic,
    evidence_bindings: [],
    semantic_effect: 'none',
    claim_limit: 'Blocked consultation evidence; no implementation or runtime authority.',
    candidate: null,
  };
}

function sameValues(left, right) {
  return JSON.stringify([...left].sort()) === JSON.stringify([...right].sort());
}

export async function evaluateEligibility({ candidate, consultationReceipt, validationContext }) {
  if (!consultationReceipt || consultationReceipt.contract !== 'oava-animejs-consultation-receipt/0.1.0') {
    return blocked('CONSULTATION_RECEIPT_INVALID', 'consultation_blocked', null);
  }
  const validateCandidate = validationContext?.validateCandidate;
  if (typeof validateCandidate !== 'function') {
    return blocked('CANDIDATE_VALIDATOR_MISSING', 'consultation_blocked', consultationReceipt.result);
  }
  const seedValidation = await validateCandidate({ candidate, ...validationContext });
  if (!seedValidation.valid || seedValidation.code !== 'VALID') {
    const code = seedValidation.code === 'REDUCED_MOTION_MISMATCH'
      ? 'REDUCED_MOTION_MISMATCH'
      : 'CANDIDATE_INVALID';
    return blocked(code, 'consultation_blocked', consultationReceipt.result, seedValidation);
  }
  const { request, result, current_projection: current } = consultationReceipt;
  if (!request || !result) return blocked('CONSULTATION_RECEIPT_INVALID', 'consultation_blocked', result);
  if (request.contract !== 'animejs-knowledge-consult-request/0.1.0'
      || request.operation !== 'lookup'
      || request.query.version_context_id !== 'animejs@4.5.0'
      || request.query.task_id !== 'TASK-OAVA-CONSULTATION') {
    return blocked('CONSULTATION_REQUEST_MISMATCH', 'consultation_blocked', result);
  }
  if (candidate.consultation.request_id !== consultationReceipt.host_request_id
      || candidate.consultation.request_id !== result.request_id) {
    return blocked('CONSULTATION_REQUEST_MISMATCH', 'consultation_blocked', result);
  }
  if (candidate.consultation.version_context?.version !== '4.5.0'
      || consultationReceipt.version_context?.version !== '4.5.0') {
    return blocked('VERSION_CONTEXT_MISMATCH', 'consultation_blocked', result);
  }
  if (result.status === 'stale') {
    return blocked('CONSULTATION_STALE', 'consultation_blocked', result, result.diagnostic);
  }
  if (result.status !== 'ok') {
    return blocked('CONSULTATION_NOT_OK', 'consultation_blocked', result, result.diagnostic);
  }
  const expected = request.expected;
  const projectionMismatch = result.graph_digest !== current.graph_digest
    || result.projection_digest !== current.projection_digest
    || (expected.graph_digest !== null && expected.graph_digest !== result.graph_digest)
    || (expected.projection_digest !== null && expected.projection_digest !== result.projection_digest);
  if (projectionMismatch) return blocked('CONSULTATION_STALE', 'consultation_blocked', result);
  if (result.records.length === 0
      || result.explanation_path.length === 0
      || consultationReceipt.evidence_bindings.length === 0) {
    return blocked('CONSULTATION_EVIDENCE_EMPTY', 'consultation_blocked', result);
  }

  let derived;
  try {
    derived = bindConsultation(candidate, consultationReceipt);
  } catch (error) {
    return blocked('CONSULTATION_BINDING_MISMATCH', 'consultation_blocked', result, { message: error.message });
  }
  const derivedValidation = await validateCandidate({ candidate: derived, ...validationContext });
  if (!derivedValidation.valid || derivedValidation.code !== 'VALID') {
    const code = derivedValidation.code === 'REDUCED_MOTION_MISMATCH'
      ? 'REDUCED_MOTION_MISMATCH'
      : 'CANDIDATE_INVALID';
    return blocked(code, 'consultation_blocked', result, derivedValidation);
  }
  const returnedBindings = [...new Set(result.records.map((record) => record.source_handle).filter(Boolean))];
  if (derived.consultation.status !== result.status
      || !sameValues(derived.consultation.evidence_bindings, consultationReceipt.evidence_bindings)
      || !sameValues(derived.consultation.evidence_bindings, returnedBindings)) {
    return blocked('CONSULTATION_BINDING_MISMATCH', 'consultation_blocked', result);
  }
  if (derived.contradiction.resolution_status !== 'clear') {
    return blocked('CONTRADICTION_OPEN', 'contradiction_quarantined', result);
  }
  if (derived.semantic_contract.semantic_end_states.at(-1)
      !== derived.semantic_contract.reduced_motion_state_machine.at(-1)) {
    return blocked('REDUCED_MOTION_MISMATCH', 'consultation_blocked', result);
  }
  return {
    eligible: true,
    code: 'TOURNAMENT_ELIGIBLE',
    state: 'tournament_eligible',
    consultation_status: result.status,
    diagnostic: null,
    evidence_bindings: [...derived.consultation.evidence_bindings],
    semantic_effect: 'none',
    claim_limit: 'Consultation evidence only; no runtime proof or implementation authority.',
    candidate: derived,
  };
}
