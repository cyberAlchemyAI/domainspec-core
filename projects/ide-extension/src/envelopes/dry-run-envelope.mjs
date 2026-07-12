import { normalizeL0Grants } from '../kernel/grants.mjs';

export const MAX_REJECTION_REASON_LENGTH = 500;

function stamp(prefix) {
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`;
}

export function localOperatorAction() {
  return {
    kind: 'local_operator_action',
    assurance: 'unattested'
  };
}

export function normalizeRejectionReason(reason) {
  if (reason === undefined || reason === null || reason === '') return null;
  if (typeof reason !== 'string') {
    const error = new Error('rejection reason must be a string');
    error.code = 'invalid_rejection_reason';
    throw error;
  }

  const normalized = reason.trim();
  if (normalized.length > MAX_REJECTION_REASON_LENGTH) {
    const error = new Error(`rejection reason must be at most ${MAX_REJECTION_REASON_LENGTH} characters`);
    error.code = 'invalid_rejection_reason';
    throw error;
  }

  return normalized || null;
}

export function normalizeDryRunEnvelope(envelope) {
  if (!envelope) return null;

  const approval = envelope.approval || {};
  const { approved_by: ignoredApprovedBy, ...approvalWithoutClaim } = approval;
  void ignoredApprovedBy;
  const resolved = Boolean(approval.approved_at || approval.rejected_at);

  return {
    ...envelope,
    requested_grants: normalizeL0Grants(envelope.requested_grants),
    requested_skill: envelope.requested_skill || null,
    approval: {
      ...approvalWithoutClaim,
      actor: approval.actor || (resolved ? localOperatorAction() : null),
      approved_at: approval.approved_at || null,
      rejected_at: approval.rejected_at || null,
      rejection_reason: approval.rejection_reason ?? null
    }
  };
}

export function prepareDryRunEnvelope(input = {}) {
  const now = new Date().toISOString();
  const requestedGrants = normalizeL0Grants(input.requested_grants);

  return {
    envelope_id: stamp('env'),
    run_id: stamp('run'),
    agent_ref: input.agent_ref || 'local.noop-agent',
    task: input.task || 'Prepare L0 dry-run receipt',
    context_refs: input.context_refs || ['projects/ide-extension/SPEC.md'],
    requested_grants: requestedGrants,
    requested_skill: input.requested_skill || null,
    approval: {
      required: true,
      approval_id: stamp('approval'),
      actor: null,
      approved_at: null,
      rejected_at: null,
      rejection_reason: null
    },
    state: 'awaiting_approval',
    receipts: [],
    created_at: now
  };
}

export function proposeDryRunApproval(envelope) {
  if (
    !envelope
    || envelope.state !== 'awaiting_approval'
    || envelope.approval?.approved_at
    || envelope.approval?.rejected_at
  ) {
    const error = new Error('approval already resolved');
    error.code = 'already_resolved';
    throw error;
  }

  const now = new Date().toISOString();
  const receiptId = stamp('receipt');

  return {
    envelope: {
      ...envelope,
      approval: {
        ...envelope.approval,
        actor: localOperatorAction(),
        approved_at: now
      },
      state: 'passed',
      receipts: [...envelope.receipts, receiptId]
    },
    receipt_id: receiptId,
    created_at: now
  };
}

export function createDryRunReceipt(envelope, options = {}) {
  return {
    receipt_id: options.receipt_id || stamp('receipt'),
    run_id: envelope.run_id,
    envelope_id: envelope.envelope_id,
    approval_id: envelope.approval.approval_id,
    requested_grants: envelope.requested_grants,
    requested_skill: envelope.requested_skill,
    disposition: 'approved',
    stage: 'l0-dry-run',
    status: 'passed',
    before_ref: options.before_ref || 'state:workbench-before-approval',
    after_ref: options.after_ref || 'state:workbench-after-approval',
    evidence_refs: options.evidence_refs || ['projects/ide-extension/development/founding-research/findings.md'],
    created_at: options.created_at || envelope.approval.approved_at || new Date().toISOString()
  };
}

export function approveDryRunEnvelope(envelope, options = {}) {
  const proposal = proposeDryRunApproval(envelope);
  return {
    envelope: proposal.envelope,
    receipt: createDryRunReceipt(proposal.envelope, {
      ...options,
      receipt_id: proposal.receipt_id,
      created_at: proposal.created_at
    })
  };
}

export function rejectDryRunEnvelope(envelope, options = {}) {
  if (
    !envelope
    || envelope.state !== 'awaiting_approval'
    || envelope.approval?.approved_at
    || envelope.approval?.rejected_at
  ) {
    const error = new Error('approval already resolved');
    error.code = 'already_resolved';
    throw error;
  }

  const rejectedAt = new Date().toISOString();
  const rejectionReason = normalizeRejectionReason(options.reason);

  return {
    envelope: {
      ...envelope,
      approval: {
        ...envelope.approval,
        actor: localOperatorAction(),
        rejected_at: rejectedAt,
        rejection_reason: rejectionReason
      },
      state: 'blocked'
    },
    rejected_at: rejectedAt,
    rejection_reason: rejectionReason
  };
}
