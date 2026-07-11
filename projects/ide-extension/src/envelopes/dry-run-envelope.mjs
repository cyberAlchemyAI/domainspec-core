import { defaultGrants } from '../kernel/grants.mjs';

function stamp(prefix) {
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`;
}

export function prepareDryRunEnvelope(input = {}) {
  const now = new Date().toISOString();
  const requestedGrants = Array.isArray(input.requested_grants) && input.requested_grants.length
    ? input.requested_grants
    : defaultGrants();

  return {
    envelope_id: stamp('env'),
    run_id: stamp('run'),
    agent_ref: input.agent_ref || 'local.noop-agent',
    task: input.task || 'Prepare L0 dry-run receipt',
    context_refs: input.context_refs || ['projects/ide-extension/SPEC.md'],
    requested_grants: requestedGrants,
    approval: {
      required: true,
      approval_id: stamp('approval'),
      approved_by: null,
      approved_at: null
    },
    state: 'awaiting_approval',
    receipts: [],
    created_at: now
  };
}

export function approveDryRunEnvelope(envelope, options = {}) {
  const now = new Date().toISOString();
  const approvedBy = options.approved_by || 'human';
  const approvalId = envelope.approval.approval_id;
  const receipt = {
    receipt_id: stamp('receipt'),
    run_id: envelope.run_id,
    stage: 'l0-dry-run',
    status: 'passed',
    before_ref: options.before_ref || 'state:workbench-before-approval',
    after_ref: options.after_ref || 'state:workbench-after-approval',
    approval_id: approvalId,
    evidence_refs: options.evidence_refs || ['projects/ide-extension/development/founding-research/findings.md'],
    created_at: now
  };

  return {
    envelope: {
      ...envelope,
      approval: {
        ...envelope.approval,
        approved_by: approvedBy,
        approved_at: now
      },
      state: 'passed',
      receipts: [...envelope.receipts, receipt.receipt_id]
    },
    receipt
  };
}

