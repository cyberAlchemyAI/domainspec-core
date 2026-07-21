export const RUN_VIEW_STAGES = Object.freeze([
  'prepared',
  'approved',
  'available',
  'running',
  'interrupted',
  'result',
  'receipt',
  'unknown'
]);

export const SUPPORTED_RUN_STATES = Object.freeze([
  'awaiting_approval',
  'approved',
  'ready_for_poll',
  'claimed',
  'interrupted',
  'passed',
  'flagged',
  'blocked',
  'failed',
  'completed'
]);

const TERMINAL_STATES = new Set(['passed', 'flagged', 'blocked', 'failed', 'completed']);

function strings(values) {
  return Array.isArray(values) ? values.filter((value) => typeof value === 'string') : [];
}

function unique(values) {
  return [...new Set(values)];
}

function labelFor(state) {
  return {
    awaiting_approval: 'Awaiting approval',
    approved: 'Approved - make available to poll',
    ready_for_poll: 'Available to poll',
    claimed: 'Running',
    interrupted: 'Interrupted - operator recovery required',
    passed: 'Completed',
    flagged: 'Completed with residue',
    blocked: 'Blocked',
    failed: 'Failed',
    completed: 'Completed'
  }[state] || 'Unknown request state';
}

function stageFor(state, hasResult, hasReceipt) {
  if (state === 'awaiting_approval') return 'prepared';
  if (state === 'approved') return 'approved';
  if (state === 'ready_for_poll') return 'available';
  if (state === 'claimed') return 'running';
  if (state === 'interrupted') return 'interrupted';
  if (TERMINAL_STATES.has(state)) return hasReceipt ? 'receipt' : hasResult ? 'result' : 'result';
  return 'unknown';
}

function legalActionsFor(state, approvalState) {
  if (state === 'awaiting_approval' && approvalState === 'pending') return ['approve', 'reject'];
  if (state === 'approved') return ['ready', 'reject'];
  if (state === 'ready_for_poll') return ['unready', 'reject'];
  if (state === 'claimed') return ['interrupt'];
  if (state === 'interrupted') return ['release'];
  return [];
}

function evidenceFor(result, receipts) {
  const receiptIds = receipts
    .map((receipt) => receipt?.receipt_id)
    .filter((value) => typeof value === 'string');
  const receiptKinds = unique(receipts
    .map((receipt) => receipt?.receipt_kind)
    .filter((value) => typeof value === 'string'));
  const evidenceRefs = unique([
    ...strings(result?.evidence_refs),
    ...receipts.flatMap((receipt) => strings(receipt?.evidence_refs))
  ]);
  const resultId = typeof result?.result_id === 'string' ? result.result_id : null;

  return {
    available: Boolean(resultId || receiptIds.length || evidenceRefs.length),
    result_id: resultId,
    receipt_ids: receiptIds,
    receipt_kinds: receiptKinds,
    evidence_refs: evidenceRefs
  };
}

export function projectRunView(input = {}) {
  const envelope = input.envelope && typeof input.envelope === 'object' ? input.envelope : null;
  const approval = input.approval && typeof input.approval === 'object' ? input.approval : null;
  const activeClaim = input.activeClaim && typeof input.activeClaim === 'object'
    ? input.activeClaim
    : null;
  const result = input.result && typeof input.result === 'object' ? input.result : null;
  const receipts = Array.isArray(input.receipts) ? input.receipts : [];
  const state = typeof envelope?.state === 'string' ? envelope.state : 'unknown';
  const evidence = evidenceFor(result, receipts);

  return {
    schema_version: '1',
    envelope_id: typeof envelope?.envelope_id === 'string' ? envelope.envelope_id : null,
    run_id: typeof envelope?.run_id === 'string' ? envelope.run_id : null,
    approval_id: typeof approval?.approval_id === 'string'
      ? approval.approval_id
      : typeof envelope?.approval?.approval_id === 'string'
        ? envelope.approval.approval_id
        : null,
    source_schema_version: envelope?.schema_version || null,
    typestate: state,
    label: labelFor(state),
    stage: stageFor(state, Boolean(result), evidence.receipt_ids.length > 0),
    legal_actions: legalActionsFor(state, approval?.state),
    claim: {
      claim_id: typeof activeClaim?.claim_id === 'string'
        ? activeClaim.claim_id
        : typeof envelope?.claim_id === 'string'
          ? envelope.claim_id
          : null,
      state: activeClaim?.state || null,
      session_ref: activeClaim?.session_ref || null,
      assurance: activeClaim?.assurance || null
    },
    result: {
      result_id: evidence.result_id,
      status: result?.status || null,
      summary: result?.summary || null
    },
    evidence
  };
}
