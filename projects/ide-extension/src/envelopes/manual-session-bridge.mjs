import { createHash, randomUUID } from 'node:crypto';
import {
  bridgeGrants,
  L0_BRIDGE_GRANT_POLICY_VERSION,
  normalizeL0Grants
} from '../kernel/grants.mjs';
import { localOperatorAction } from './dry-run-envelope.mjs';

function id(prefix) {
  return `${prefix}-${randomUUID()}`;
}

function sha256(value) {
  return createHash('sha256').update(JSON.stringify(value)).digest('hex');
}

export function isBridgeGrantProfile(grants) {
  return Array.isArray(grants)
    && JSON.stringify([...grants].sort()) === JSON.stringify(bridgeGrants());
}

export function prepareBridgeEnvelope(input, options = {}) {
  const requestedGrants = normalizeL0Grants(input.requested_grants);
  if (!isBridgeGrantProfile(requestedGrants)) {
    const error = new Error('manual session bridge requires the exact bridge grant profile');
    error.code = 'invalid_bridge_grants';
    throw error;
  }

  const createdAt = options.created_at || new Date().toISOString();
  const envelopeId = options.envelope_id || id('env');
  const runId = options.run_id || id('run');
  const approvalId = options.approval_id || id('approval');
  const approval = {
    required: true,
    approval_id: approvalId,
    actor: null,
    approved_at: null,
    consumed_at: null,
    revoked_at: null,
    rejected_at: null,
    rejection_reason: null
  };
  const envelope = {
    schema_version: '2',
    envelope_id: envelopeId,
    run_id: runId,
    agent_ref: 'codex.current-session',
    task: input.task,
    context_refs: input.context_refs || ['projects/ide-extension/SPEC.md'],
    requested_grants: requestedGrants,
    requested_skill: input.requested_skill,
    approval,
    state: 'awaiting_approval',
    authorization_receipt_id: null,
    claim_id: null,
    result_id: null,
    receipts: [],
    created_at: createdAt
  };
  const approvalRecord = {
    schema_version: '2',
    approval_id: approvalId,
    envelope_id: envelopeId,
    run_id: runId,
    state: 'pending',
    actor: null,
    title: input.task,
    required_for: requestedGrants,
    created_at: createdAt,
    authorized_at: null,
    consumed_at: null,
    revoked_at: null,
    rejected_at: null,
    rejection_reason: null,
    authorization_receipt_id: null
  };

  return { envelope, approval: approvalRecord };
}

export function authorizeBridgeEnvelope(envelope, approval, options = {}) {
  if (envelope?.schema_version !== '2'
    || envelope.state !== 'awaiting_approval'
    || approval?.state !== 'pending') {
    const error = new Error('bridge authorization is already resolved');
    error.code = 'already_resolved';
    throw error;
  }

  const authorizedAt = options.authorized_at || new Date().toISOString();
  const receiptId = options.receipt_id || id('receipt');
  const actor = localOperatorAction();
  const authorizedEnvelope = {
    ...envelope,
    approval: {
      ...envelope.approval,
      actor,
      approved_at: authorizedAt
    },
    state: 'approved',
    authorization_receipt_id: receiptId,
    receipts: [...envelope.receipts, receiptId]
  };
  const authorizedApproval = {
    ...approval,
    state: 'authorized',
    actor,
    authorized_at: authorizedAt,
    authorization_receipt_id: receiptId
  };
  const receipt = {
    schema_version: '2',
    receipt_kind: 'authorization.receipt',
    receipt_id: receiptId,
    run_id: envelope.run_id,
    envelope_id: envelope.envelope_id,
    approval_id: approval.approval_id,
    task: envelope.task,
    task_sha256: sha256(envelope.task),
    requested_skill: envelope.requested_skill,
    requested_skill_sha256: sha256(envelope.requested_skill),
    requested_grants: envelope.requested_grants,
    grant_profile_sha256: sha256(envelope.requested_grants),
    policy_version: L0_BRIDGE_GRANT_POLICY_VERSION,
    actor,
    authorization_status: 'granted',
    authorized_at: authorizedAt,
    created_at: authorizedAt
  };

  return {
    envelope: authorizedEnvelope,
    approval: authorizedApproval,
    receipt,
    created_at: authorizedAt
  };
}

export function selectBridgeTarget(envelope) {
  if (envelope?.schema_version !== '2' || envelope.state !== 'approved') {
    const error = new Error('bridge request is not approved');
    error.code = 'not_approved';
    throw error;
  }
  return { ...envelope, state: 'ready_for_poll' };
}

export function clearBridgeTarget(envelope) {
  if (envelope?.schema_version !== '2' || envelope.state !== 'ready_for_poll') {
    const error = new Error('bridge request is not ready');
    error.code = 'not_ready';
    throw error;
  }
  return { ...envelope, state: 'approved' };
}

export function revokeBridgeAuthorization(envelope, approval, reason, options = {}) {
  if (envelope?.schema_version !== '2'
    || !['approved', 'ready_for_poll'].includes(envelope.state)
    || approval?.state !== 'authorized') {
    const error = new Error('bridge authorization cannot be revoked');
    error.code = 'not_revocable';
    throw error;
  }

  const revokedAt = options.revoked_at || new Date().toISOString();
  const actor = localOperatorAction();
  return {
    envelope: {
      ...envelope,
      approval: {
        ...envelope.approval,
        actor,
        revoked_at: revokedAt,
        rejection_reason: reason
      },
      state: 'blocked'
    },
    approval: {
      ...approval,
      state: 'revoked',
      actor,
      revoked_at: revokedAt,
      rejection_reason: reason
    },
    actor,
    reason,
    created_at: revokedAt
  };
}

export function claimBridgeEnvelope(envelope, approval, request, options = {}) {
  if (envelope?.schema_version !== '2'
    || envelope.state !== 'ready_for_poll'
    || approval?.state !== 'authorized') {
    const error = new Error('bridge request is not claimable');
    error.code = 'not_claimable';
    throw error;
  }
  const claimedAt = options.claimed_at || new Date().toISOString();
  const claimId = options.claim_id || id('claim');
  const claimAttemptId = options.claim_attempt_id || id('attempt');
  const claim = {
    schema_version: '2',
    claim_id: claimId,
    claim_attempt_id: claimAttemptId,
    envelope_id: envelope.envelope_id,
    run_id: envelope.run_id,
    approval_id: approval.approval_id,
    agent_ref: request.agent_ref,
    session_ref: request.session_ref,
    assurance: request.assurance,
    state: 'claimed',
    claimed_at: claimedAt,
    interrupted_at: null,
    interruption_reason: null,
    released_at: null,
    release_reason: null,
    result_id: null
  };
  return {
    envelope: { ...envelope, state: 'claimed', claim_id: claimId },
    claim,
    created_at: claimedAt
  };
}

export function interruptBridgeClaim(envelope, claim, reason, options = {}) {
  if (envelope?.state !== 'claimed' || claim?.state !== 'claimed') {
    const error = new Error('bridge claim is not active');
    error.code = 'claim_not_active';
    throw error;
  }
  const interruptedAt = options.interrupted_at || new Date().toISOString();
  return {
    envelope: { ...envelope, state: 'interrupted' },
    claim: {
      ...claim,
      state: 'interrupted',
      interrupted_at: interruptedAt,
      interruption_reason: reason
    },
    reason,
    created_at: interruptedAt
  };
}

export function releaseBridgeClaim(envelope, claim, reason, options = {}) {
  if (envelope?.state !== 'interrupted' || claim?.state !== 'interrupted') {
    const error = new Error('bridge claim is not interrupted');
    error.code = 'claim_not_interrupted';
    throw error;
  }
  const releasedAt = options.released_at || new Date().toISOString();
  const actor = localOperatorAction();
  return {
    envelope: { ...envelope, state: 'approved', claim_id: null },
    claim: {
      ...claim,
      state: 'released',
      released_at: releasedAt,
      release_reason: reason
    },
    actor,
    reason,
    created_at: releasedAt
  };
}

export function recordBridgeResult(envelope, approval, claim, input, refs, options = {}) {
  if (envelope?.state !== 'claimed'
    || approval?.state !== 'authorized'
    || claim?.state !== 'claimed') {
    const error = new Error('bridge claim is not active for result admission');
    error.code = 'claim_not_active';
    throw error;
  }
  if (!['passed', 'flagged', 'blocked'].includes(input.status)) {
    const error = new Error('unsupported L0 terminal status');
    error.code = 'unsupported_result_status';
    throw error;
  }

  const resultAt = options.result_at || new Date().toISOString();
  const resultId = options.result_id || id('result');
  const receiptId = options.receipt_id || id('receipt');
  const result = {
    ...input,
    result_id: resultId,
    result_at: resultAt
  };
  const terminalEnvelope = {
    ...envelope,
    approval: { ...envelope.approval, consumed_at: resultAt },
    state: input.status,
    result_id: resultId,
    receipts: [...envelope.receipts, receiptId]
  };
  const consumedApproval = {
    ...approval,
    state: 'consumed',
    consumed_at: resultAt
  };
  const completedClaim = {
    ...claim,
    state: 'completed',
    result_id: resultId
  };
  const receipt = {
    schema_version: '2',
    receipt_kind: 'skill.execution',
    receipt_id: receiptId,
    run_id: envelope.run_id,
    envelope_id: envelope.envelope_id,
    approval_id: approval.approval_id,
    authorization_receipt_id: envelope.authorization_receipt_id,
    claim_id: claim.claim_id,
    claim_attempt_id: claim.claim_attempt_id,
    agent_ref: claim.agent_ref,
    session_ref: claim.session_ref,
    assurance: claim.assurance,
    requested_skill: envelope.requested_skill,
    skill_sha256: input.skill_sha256,
    requested_grants: envelope.requested_grants,
    effect_profile: 'preview.read',
    status: input.status,
    summary: input.summary,
    validation: input.validation,
    evidence_refs: input.evidence_refs,
    before_ref: refs.before_ref,
    after_ref: refs.after_ref,
    result_ref: refs.result_ref,
    claimed_at: claim.claimed_at,
    result_at: resultAt,
    created_at: resultAt
  };

  return {
    envelope: terminalEnvelope,
    approval: consumedApproval,
    claim: completedClaim,
    result,
    receipt,
    created_at: resultAt
  };
}
