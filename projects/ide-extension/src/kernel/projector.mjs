import { createHash } from 'node:crypto';

export const EVENT_VERSION = 1;
export const BRIDGE_EVENT_VERSION = 2;
export const CANVAS_EVENT_VERSION = 3;

export function createInitialWorkbench() {
  return {
    project: 'ide-extension',
    boundary: 'l0-witness',
    selected_work_item: {
      work_item_id: 'work-l0-001',
      title: 'Prove approval-gated dry-run receipt loop',
      owner_route: 'task-session',
      source_ref: 'projects/ide-extension/SPEC.md'
    },
    envelopes: {},
    approvals: {},
    approval_queue: [],
    receipts: [],
    current_envelope_id: null,
    current_envelope: null,
    evidence_refs: ['projects/ide-extension/development/founding-research/findings.md']
  };
}

function invalidHistory(message, index, event) {
  const error = new Error(`event ${index + 1}: ${message}`);
  error.code = 'invalid_event_history';
  error.event_index = index;
  error.event_id = event?.event_id || null;
  return error;
}

function assertExactKeys(value, expected, index, event, label = 'event') {
  const actual = value && typeof value === 'object' && !Array.isArray(value)
    ? Object.keys(value).sort()
    : [];
  const wanted = [...expected].sort();
  if (JSON.stringify(actual) !== JSON.stringify(wanted)) {
    throw invalidHistory(`${label} expected fields ${wanted.join(', ')}`, index, event);
  }
}

function assertHeader(event, index, seenEventIds) {
  if (!event || typeof event !== 'object' || Array.isArray(event)) {
    throw invalidHistory('event must be an object', index, event);
  }
  if (![EVENT_VERSION, BRIDGE_EVENT_VERSION, CANVAS_EVENT_VERSION].includes(event.event_version)) {
    throw invalidHistory(`unsupported event_version ${event.event_version}`, index, event);
  }
  if (typeof event.event_id !== 'string' || event.event_id.length === 0) {
    throw invalidHistory('event_id must be a non-empty string', index, event);
  }
  if (seenEventIds.has(event.event_id)) {
    throw invalidHistory(`duplicate event_id ${event.event_id}`, index, event);
  }
  if (typeof event.created_at !== 'string' || event.created_at.length === 0) {
    throw invalidHistory('created_at must be a non-empty string', index, event);
  }
  seenEventIds.add(event.event_id);
}

function assertBinding(condition, message, index, event) {
  if (!condition) throw invalidHistory(message, index, event);
}

function same(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

function replaceRecords(state, envelope, approval) {
  return {
    ...state,
    envelopes: { ...state.envelopes, [envelope.envelope_id]: envelope },
    approvals: { ...state.approvals, [approval.approval_id]: approval },
    approval_queue: state.approval_queue.map((item) => (
      item.approval_id === approval.approval_id ? approval : item
    )),
    current_envelope: state.current_envelope_id === envelope.envelope_id
      ? envelope
      : state.current_envelope
  };
}

function applyV1Prepared(state, event, index) {
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'envelope', 'approval', 'created_at'],
    index,
    event
  );
  const { envelope, approval } = event;
  assertBinding(envelope.state === 'awaiting_approval', 'prepared envelope must await approval', index, event);
  assertBinding(approval.state === 'pending', 'prepared approval must be pending', index, event);
  assertBinding(approval.envelope_id === envelope.envelope_id, 'approval envelope binding mismatch', index, event);
  assertBinding(approval.run_id === envelope.run_id, 'approval run binding mismatch', index, event);
  assertBinding(
    envelope.approval.approval_id === approval.approval_id,
    'approval id binding mismatch',
    index,
    event
  );
  assertBinding(!state.envelopes[envelope.envelope_id], 'duplicate envelope id', index, event);
  assertBinding(!state.approvals[approval.approval_id], 'duplicate approval id', index, event);

  return {
    ...state,
    envelopes: { ...state.envelopes, [envelope.envelope_id]: envelope },
    approvals: { ...state.approvals, [approval.approval_id]: approval },
    approval_queue: [...state.approval_queue, approval],
    current_envelope_id: envelope.envelope_id,
    current_envelope: envelope
  };
}

function assertV1PendingBinding(state, envelope, approval, index, event) {
  const previousApproval = state.approvals[approval.approval_id];
  const previousEnvelope = state.envelopes[envelope.envelope_id];
  assertBinding(previousApproval?.state === 'pending', 'approval is not pending', index, event);
  assertBinding(
    previousApproval.envelope_id === envelope.envelope_id,
    'approval envelope binding changed',
    index,
    event
  );
  assertBinding(previousApproval.run_id === envelope.run_id, 'approval run binding changed', index, event);
  assertBinding(previousEnvelope?.state === 'awaiting_approval', 'envelope is not awaiting approval', index, event);
  assertBinding(
    previousEnvelope.approval.approval_id === approval.approval_id,
    'envelope approval binding changed',
    index,
    event
  );
}

function applyV1Receipt(state, event, index) {
  assertExactKeys(
    event,
    [
      'event_version',
      'event_id',
      'event_type',
      'envelope',
      'approval',
      'receipt',
      'artifact_refs',
      'created_at'
    ],
    index,
    event
  );
  const { envelope, approval, receipt } = event;
  assertV1PendingBinding(state, envelope, approval, index, event);
  assertBinding(envelope.state === 'passed', 'consumed envelope must be passed', index, event);
  assertBinding(approval.state === 'consumed', 'receipt approval must be consumed', index, event);
  assertBinding(receipt.run_id === envelope.run_id, 'receipt run binding mismatch', index, event);
  assertBinding(receipt.envelope_id === envelope.envelope_id, 'receipt envelope binding mismatch', index, event);
  assertBinding(receipt.approval_id === approval.approval_id, 'receipt approval binding mismatch', index, event);
  assertBinding(receipt.disposition === 'approved', 'receipt disposition mismatch', index, event);
  assertBinding(same(receipt.requested_grants, envelope.requested_grants), 'receipt grant binding mismatch', index, event);
  assertBinding(receipt.requested_skill === envelope.requested_skill, 'receipt skill binding mismatch', index, event);
  assertBinding(
    !state.receipts.some((candidate) => candidate.receipt_id === receipt.receipt_id),
    'duplicate receipt id',
    index,
    event
  );
  assertBinding(
    Array.isArray(event.artifact_refs) && event.artifact_refs.every((ref) => typeof ref === 'string'),
    'artifact_refs must be strings',
    index,
    event
  );
  assertBinding(event.artifact_refs.includes(receipt.before_ref), 'before_ref is not committed', index, event);
  assertBinding(event.artifact_refs.includes(receipt.after_ref), 'after_ref is not committed', index, event);

  return {
    ...replaceRecords(state, envelope, approval),
    receipts: [...state.receipts, receipt]
  };
}

function applyV1Rejected(state, event, index) {
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'envelope', 'approval', 'created_at'],
    index,
    event
  );
  const { envelope, approval } = event;
  assertV1PendingBinding(state, envelope, approval, index, event);
  assertBinding(envelope.state === 'blocked', 'rejected envelope must be blocked', index, event);
  assertBinding(approval.state === 'rejected', 'rejected approval must be rejected', index, event);
  return replaceRecords(state, envelope, approval);
}

function reduceV1Event(state, event, index) {
  if (event.event_type === 'envelope.prepared') return applyV1Prepared(state, event, index);
  if (event.event_type === 'receipt.appended') return applyV1Receipt(state, event, index);
  if (event.event_type === 'approval.rejected') return applyV1Rejected(state, event, index);
  throw invalidHistory(`unknown v1 event_type ${event.event_type}`, index, event);
}

function withBridgeState(state) {
  if (state.bridge) return state;
  return {
    ...state,
    bridge: {
      schema_version: '2',
      ready_target_envelope_id: null,
      ready_target_selected_at: null,
      claims: {},
      claim_order: [],
      results: {}
    }
  };
}

function assertV2Record(record, label, index, event) {
  assertBinding(record?.schema_version === '2', `${label} must use schema_version 2`, index, event);
}

function assertOperator(actor, index, event) {
  assertBinding(
    actor?.kind === 'local_operator_action' && actor.assurance === 'unattested',
    'operator actor binding mismatch',
    index,
    event
  );
}

function assertArtifactRefs(refs, index, event) {
  assertBinding(
    Array.isArray(refs) && refs.every((ref) => typeof ref === 'string' && ref.length > 0),
    'artifact_refs must be non-empty strings',
    index,
    event
  );
}

function assertEnvelopeIdentity(previous, next, index, event) {
  assertBinding(previous?.envelope_id === next.envelope_id, 'envelope id binding changed', index, event);
  assertBinding(previous.run_id === next.run_id, 'envelope run binding changed', index, event);
  assertBinding(previous.agent_ref === next.agent_ref, 'envelope agent binding changed', index, event);
  assertBinding(previous.task === next.task, 'envelope task binding changed', index, event);
  assertBinding(previous.requested_skill === next.requested_skill, 'envelope skill binding changed', index, event);
  assertBinding(same(previous.requested_grants, next.requested_grants), 'envelope grants changed', index, event);
  assertBinding(
    previous.approval.approval_id === next.approval.approval_id,
    'envelope approval binding changed',
    index,
    event
  );
}

function assertApprovalIdentity(previous, next, index, event) {
  assertBinding(previous?.approval_id === next.approval_id, 'approval id binding changed', index, event);
  assertBinding(previous.envelope_id === next.envelope_id, 'approval envelope binding changed', index, event);
  assertBinding(previous.run_id === next.run_id, 'approval run binding changed', index, event);
  assertBinding(same(previous.required_for, next.required_for), 'approval grants changed', index, event);
}

function applyV2Prepared(inputState, event, index) {
  const state = withBridgeState(inputState);
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'envelope', 'approval', 'created_at'],
    index,
    event
  );
  const { envelope, approval } = event;
  assertV2Record(envelope, 'envelope', index, event);
  assertV2Record(approval, 'approval', index, event);
  assertBinding(envelope.state === 'awaiting_approval', 'v2 prepared envelope must await approval', index, event);
  assertBinding(approval.state === 'pending', 'v2 prepared approval must be pending', index, event);
  assertBinding(envelope.approval.approval_id === approval.approval_id, 'approval id mismatch', index, event);
  assertBinding(approval.envelope_id === envelope.envelope_id, 'approval envelope mismatch', index, event);
  assertBinding(approval.run_id === envelope.run_id, 'approval run mismatch', index, event);
  assertBinding(!state.envelopes[envelope.envelope_id], 'duplicate envelope id', index, event);
  assertBinding(!state.approvals[approval.approval_id], 'duplicate approval id', index, event);

  return {
    ...state,
    envelopes: { ...state.envelopes, [envelope.envelope_id]: envelope },
    approvals: { ...state.approvals, [approval.approval_id]: approval },
    approval_queue: [...state.approval_queue, approval],
    current_envelope_id: envelope.envelope_id,
    current_envelope: envelope
  };
}

function assertV2Pending(state, envelope, approval, index, event) {
  const previousEnvelope = state.envelopes[envelope.envelope_id];
  const previousApproval = state.approvals[approval.approval_id];
  assertV2Record(envelope, 'envelope', index, event);
  assertV2Record(approval, 'approval', index, event);
  assertBinding(previousEnvelope?.state === 'awaiting_approval', 'v2 envelope is not awaiting approval', index, event);
  assertBinding(previousApproval?.state === 'pending', 'v2 approval is not pending', index, event);
  assertEnvelopeIdentity(previousEnvelope, envelope, index, event);
  assertApprovalIdentity(previousApproval, approval, index, event);
}

function applyV2Authorization(inputState, event, index) {
  const state = withBridgeState(inputState);
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'envelope', 'approval', 'receipt', 'artifact_refs', 'created_at'],
    index,
    event
  );
  const { envelope, approval, receipt } = event;
  assertV2Pending(state, envelope, approval, index, event);
  assertBinding(envelope.state === 'approved', 'authorized envelope must be approved', index, event);
  assertBinding(approval.state === 'authorized', 'approval must be authorized', index, event);
  assertBinding(receipt?.schema_version === '2', 'authorization receipt must use schema_version 2', index, event);
  assertBinding(receipt.receipt_kind === 'authorization.receipt', 'authorization receipt kind mismatch', index, event);
  assertBinding(receipt.run_id === envelope.run_id, 'authorization receipt run mismatch', index, event);
  assertBinding(receipt.envelope_id === envelope.envelope_id, 'authorization receipt envelope mismatch', index, event);
  assertBinding(receipt.approval_id === approval.approval_id, 'authorization receipt approval mismatch', index, event);
  assertBinding(receipt.task === envelope.task, 'authorization receipt task mismatch', index, event);
  assertBinding(receipt.requested_skill === envelope.requested_skill, 'authorization receipt skill mismatch', index, event);
  assertBinding(same(receipt.requested_grants, envelope.requested_grants), 'authorization receipt grants mismatch', index, event);
  assertBinding(envelope.authorization_receipt_id === receipt.receipt_id, 'envelope authorization receipt mismatch', index, event);
  assertBinding(approval.authorization_receipt_id === receipt.receipt_id, 'approval authorization receipt mismatch', index, event);
  assertBinding(envelope.receipts.includes(receipt.receipt_id), 'envelope omits authorization receipt', index, event);
  assertOperator(receipt.actor, index, event);
  assertArtifactRefs(event.artifact_refs, index, event);
  assertBinding(
    !state.receipts.some((candidate) => candidate.receipt_id === receipt.receipt_id),
    'duplicate receipt id',
    index,
    event
  );

  return {
    ...replaceRecords(state, envelope, approval),
    receipts: [...state.receipts, receipt]
  };
}

function assertAuthorizedEnvelope(state, envelope, index, event, allowedStates) {
  const previous = state.envelopes[envelope.envelope_id];
  assertV2Record(envelope, 'envelope', index, event);
  assertBinding(allowedStates.includes(previous?.state), `envelope must be ${allowedStates.join(' or ')}`, index, event);
  assertEnvelopeIdentity(previous, envelope, index, event);
  const approval = state.approvals[previous.approval.approval_id];
  assertBinding(approval?.state === 'authorized', 'authorization is not active', index, event);
  assertBinding(
    approval.authorization_receipt_id === envelope.authorization_receipt_id,
    'authorization receipt binding changed',
    index,
    event
  );
  return { previous, approval };
}

function replaceEnvelope(state, envelope) {
  return {
    ...state,
    envelopes: { ...state.envelopes, [envelope.envelope_id]: envelope },
    current_envelope: state.current_envelope_id === envelope.envelope_id
      ? envelope
      : state.current_envelope
  };
}

function applyV2TargetSelected(inputState, event, index) {
  const state = withBridgeState(inputState);
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'envelope', 'approval_id', 'actor', 'created_at'],
    index,
    event
  );
  const { envelope } = event;
  const { approval } = assertAuthorizedEnvelope(state, envelope, index, event, ['approved']);
  assertOperator(event.actor, index, event);
  assertBinding(approval.approval_id === event.approval_id, 'target approval mismatch', index, event);
  assertBinding(state.bridge.ready_target_envelope_id === null, 'ready target already exists', index, event);
  assertBinding(envelope.state === 'ready_for_poll', 'selected envelope must be ready_for_poll', index, event);

  return {
    ...replaceEnvelope(state, envelope),
    bridge: {
      ...state.bridge,
      ready_target_envelope_id: envelope.envelope_id,
      ready_target_selected_at: event.created_at
    }
  };
}

function applyV2TargetCleared(inputState, event, index) {
  const state = withBridgeState(inputState);
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'envelope', 'approval_id', 'actor', 'created_at'],
    index,
    event
  );
  const { envelope } = event;
  const { approval } = assertAuthorizedEnvelope(state, envelope, index, event, ['ready_for_poll']);
  assertOperator(event.actor, index, event);
  assertBinding(approval.approval_id === event.approval_id, 'target approval mismatch', index, event);
  assertBinding(state.bridge.ready_target_envelope_id === envelope.envelope_id, 'stale ready target', index, event);
  assertBinding(envelope.state === 'approved', 'cleared envelope must be approved', index, event);

  return {
    ...replaceEnvelope(state, envelope),
    bridge: {
      ...state.bridge,
      ready_target_envelope_id: null,
      ready_target_selected_at: null
    }
  };
}

const CLAIM_KEYS = [
  'schema_version',
  'claim_id',
  'claim_attempt_id',
  'envelope_id',
  'run_id',
  'approval_id',
  'agent_ref',
  'session_ref',
  'assurance',
  'state',
  'claimed_at',
  'interrupted_at',
  'interruption_reason',
  'released_at',
  'release_reason',
  'result_id'
];

function assertClaimRecord(claim, index, event) {
  assertExactKeys(claim, CLAIM_KEYS, index, event, 'claim');
  assertV2Record(claim, 'claim', index, event);
  assertBinding(claim.agent_ref === 'codex.current-session', 'claim agent mismatch', index, event);
  assertBinding(claim.assurance === 'unattested', 'claim assurance mismatch', index, event);
  assertBinding(typeof claim.session_ref === 'string' && claim.session_ref.length > 0, 'claim session_ref missing', index, event);
  assertBinding(
    ['claimed', 'interrupted', 'released', 'completed'].includes(claim.state),
    'claim state is invalid',
    index,
    event
  );
}

function assertClaimIdentity(previous, next, index, event) {
  for (const key of [
    'claim_id', 'claim_attempt_id', 'envelope_id', 'run_id', 'approval_id',
    'agent_ref', 'session_ref', 'assurance', 'claimed_at'
  ]) {
    assertBinding(previous?.[key] === next[key], `claim ${key} binding changed`, index, event);
  }
}

function applyV2Claimed(inputState, event, index) {
  const state = withBridgeState(inputState);
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'envelope', 'claim', 'artifact_refs', 'created_at'],
    index,
    event
  );
  const { envelope, claim } = event;
  const { approval } = assertAuthorizedEnvelope(state, envelope, index, event, ['ready_for_poll']);
  assertClaimRecord(claim, index, event);
  assertBinding(state.bridge.ready_target_envelope_id === envelope.envelope_id, 'claim target is not ready', index, event);
  assertBinding(!state.bridge.claims[claim.claim_id], 'duplicate claim id', index, event);
  assertBinding(claim.state === 'claimed', 'new claim must be claimed', index, event);
  assertBinding(claim.envelope_id === envelope.envelope_id, 'claim envelope mismatch', index, event);
  assertBinding(claim.run_id === envelope.run_id, 'claim run mismatch', index, event);
  assertBinding(claim.approval_id === approval.approval_id, 'claim approval mismatch', index, event);
  assertBinding(envelope.state === 'claimed', 'claimed envelope state mismatch', index, event);
  assertBinding(envelope.claim_id === claim.claim_id, 'envelope claim id mismatch', index, event);
  assertBinding(claim.interrupted_at === null && claim.released_at === null && claim.result_id === null, 'new claim has terminal fields', index, event);
  assertArtifactRefs(event.artifact_refs, index, event);

  return {
    ...replaceEnvelope(state, envelope),
    bridge: {
      ...state.bridge,
      ready_target_envelope_id: null,
      ready_target_selected_at: null,
      claims: { ...state.bridge.claims, [claim.claim_id]: claim },
      claim_order: [...state.bridge.claim_order, claim.claim_id]
    }
  };
}

function applyV2Interrupted(inputState, event, index) {
  const state = withBridgeState(inputState);
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'envelope', 'claim', 'reason', 'artifact_refs', 'created_at'],
    index,
    event
  );
  const { envelope, claim } = event;
  const previousEnvelope = state.envelopes[envelope.envelope_id];
  const previousClaim = state.bridge.claims[claim.claim_id];
  assertV2Record(envelope, 'envelope', index, event);
  assertClaimRecord(claim, index, event);
  assertBinding(previousEnvelope?.state === 'claimed', 'envelope is not claimed', index, event);
  assertBinding(previousClaim?.state === 'claimed', 'claim is not active', index, event);
  assertEnvelopeIdentity(previousEnvelope, envelope, index, event);
  assertClaimIdentity(previousClaim, claim, index, event);
  assertBinding(envelope.state === 'interrupted', 'interrupted envelope state mismatch', index, event);
  assertBinding(envelope.claim_id === claim.claim_id, 'interrupted envelope claim mismatch', index, event);
  assertBinding(claim.state === 'interrupted', 'claim must be interrupted', index, event);
  assertBinding(claim.interrupted_at === event.created_at, 'claim interruption timestamp mismatch', index, event);
  assertBinding(claim.interruption_reason === event.reason, 'claim interruption reason mismatch', index, event);
  assertBinding(claim.released_at === null && claim.result_id === null, 'interrupted claim has later fields', index, event);
  assertArtifactRefs(event.artifact_refs, index, event);

  return {
    ...replaceEnvelope(state, envelope),
    bridge: {
      ...state.bridge,
      claims: { ...state.bridge.claims, [claim.claim_id]: claim }
    }
  };
}

function applyV2Released(inputState, event, index) {
  const state = withBridgeState(inputState);
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'envelope', 'claim', 'actor', 'reason', 'artifact_refs', 'created_at'],
    index,
    event
  );
  const { envelope, claim } = event;
  const previousEnvelope = state.envelopes[envelope.envelope_id];
  const previousClaim = state.bridge.claims[claim.claim_id];
  assertOperator(event.actor, index, event);
  assertV2Record(envelope, 'envelope', index, event);
  assertClaimRecord(claim, index, event);
  assertBinding(previousEnvelope?.state === 'interrupted', 'envelope is not interrupted', index, event);
  assertBinding(previousClaim?.state === 'interrupted', 'claim is not interrupted', index, event);
  assertEnvelopeIdentity(previousEnvelope, envelope, index, event);
  assertClaimIdentity(previousClaim, claim, index, event);
  assertBinding(envelope.state === 'approved', 'released envelope must return to approved', index, event);
  assertBinding(envelope.claim_id === null && envelope.result_id === null, 'released envelope retains claim/result', index, event);
  assertBinding(claim.state === 'released', 'released claim state mismatch', index, event);
  assertBinding(claim.released_at === event.created_at, 'claim release timestamp mismatch', index, event);
  assertBinding(claim.release_reason === event.reason, 'claim release reason mismatch', index, event);
  assertBinding(claim.result_id === null, 'released claim has a result', index, event);
  assertArtifactRefs(event.artifact_refs, index, event);

  return {
    ...replaceEnvelope(state, envelope),
    bridge: {
      ...state.bridge,
      claims: { ...state.bridge.claims, [claim.claim_id]: claim }
    }
  };
}

function assertResultRecord(result, index, event) {
  assertExactKeys(
    result,
    [
      'schema_version', 'result_id', 'claim_id', 'claim_attempt_id', 'envelope_id',
      'run_id', 'approval_id', 'session_ref', 'assurance', 'requested_skill',
      'skill_sha256', 'status', 'summary', 'validation', 'evidence_refs', 'result_at'
    ],
    index,
    event,
    'result'
  );
  assertV2Record(result, 'result', index, event);
  assertBinding(['passed', 'flagged', 'blocked', 'failed'].includes(result.status), 'result status invalid', index, event);
  assertBinding(result.assurance === 'unattested', 'result assurance mismatch', index, event);
  assertBinding(Array.isArray(result.validation), 'result validation must be an array', index, event);
  assertBinding(Array.isArray(result.evidence_refs), 'result evidence_refs must be an array', index, event);
}

function applyV2Result(inputState, event, index) {
  const state = withBridgeState(inputState);
  assertExactKeys(
    event,
    [
      'event_version', 'event_id', 'event_type', 'envelope', 'approval', 'claim',
      'result', 'receipt', 'artifact_refs', 'created_at'
    ],
    index,
    event
  );
  const { envelope, approval, claim, result, receipt } = event;
  const previousEnvelope = state.envelopes[envelope.envelope_id];
  const previousApproval = state.approvals[approval.approval_id];
  const previousClaim = state.bridge.claims[claim.claim_id];
  assertV2Record(envelope, 'envelope', index, event);
  assertV2Record(approval, 'approval', index, event);
  assertClaimRecord(claim, index, event);
  assertResultRecord(result, index, event);
  assertBinding(previousEnvelope?.state === 'claimed', 'result envelope is not claimed', index, event);
  assertBinding(previousApproval?.state === 'authorized', 'result authorization is not active', index, event);
  assertBinding(previousClaim?.state === 'claimed', 'result claim is not active', index, event);
  assertEnvelopeIdentity(previousEnvelope, envelope, index, event);
  assertApprovalIdentity(previousApproval, approval, index, event);
  assertClaimIdentity(previousClaim, claim, index, event);
  assertBinding(envelope.state === result.status, 'envelope/result status mismatch', index, event);
  assertBinding(envelope.result_id === result.result_id, 'envelope result id mismatch', index, event);
  assertBinding(approval.state === 'consumed', 'terminal result must consume authorization', index, event);
  assertBinding(approval.authorization_receipt_id === envelope.authorization_receipt_id, 'consumed authorization receipt mismatch', index, event);
  assertBinding(claim.state === 'completed' && claim.result_id === result.result_id, 'claim result binding mismatch', index, event);
  for (const key of ['claim_id', 'claim_attempt_id', 'envelope_id', 'run_id', 'approval_id', 'session_ref']) {
    assertBinding(result[key] === claim[key], `result ${key} binding mismatch`, index, event);
  }
  assertBinding(result.requested_skill === envelope.requested_skill, 'result skill mismatch', index, event);
  assertBinding(result.result_at === event.created_at, 'result timestamp mismatch', index, event);
  assertBinding(receipt?.schema_version === '2' && receipt.receipt_kind === 'skill.execution', 'execution receipt kind mismatch', index, event);
  for (const key of ['run_id', 'envelope_id', 'approval_id', 'claim_id', 'claim_attempt_id', 'session_ref']) {
    assertBinding(receipt[key] === result[key], `execution receipt ${key} mismatch`, index, event);
  }
  assertBinding(receipt.authorization_receipt_id === envelope.authorization_receipt_id, 'execution authorization receipt mismatch', index, event);
  assertBinding(receipt.requested_skill === result.requested_skill, 'execution receipt skill mismatch', index, event);
  assertBinding(receipt.skill_sha256 === result.skill_sha256, 'execution receipt skill hash mismatch', index, event);
  assertBinding(receipt.status === result.status, 'execution receipt status mismatch', index, event);
  assertBinding(same(receipt.validation, result.validation), 'execution receipt validation mismatch', index, event);
  assertBinding(same(receipt.evidence_refs, result.evidence_refs), 'execution receipt evidence mismatch', index, event);
  assertBinding(envelope.receipts.includes(receipt.receipt_id), 'envelope omits execution receipt', index, event);
  assertBinding(!state.bridge.results[result.result_id], 'duplicate result id', index, event);
  assertBinding(!state.receipts.some((candidate) => candidate.receipt_id === receipt.receipt_id), 'duplicate receipt id', index, event);
  assertArtifactRefs(event.artifact_refs, index, event);
  for (const ref of [receipt.before_ref, receipt.after_ref, receipt.result_ref]) {
    assertBinding(event.artifact_refs.includes(ref), 'execution receipt artifact is not committed', index, event);
  }

  return {
    ...replaceRecords(state, envelope, approval),
    receipts: [...state.receipts, receipt],
    bridge: {
      ...state.bridge,
      claims: { ...state.bridge.claims, [claim.claim_id]: claim },
      results: { ...state.bridge.results, [result.result_id]: result }
    }
  };
}

function applyV2Rejected(inputState, event, index) {
  const state = withBridgeState(inputState);
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'envelope', 'approval', 'created_at'],
    index,
    event
  );
  const { envelope, approval } = event;
  assertV2Pending(state, envelope, approval, index, event);
  assertBinding(envelope.state === 'blocked', 'rejected v2 envelope must be blocked', index, event);
  assertBinding(approval.state === 'rejected', 'v2 approval must be rejected', index, event);
  assertBinding(envelope.approval.rejected_at === event.created_at, 'envelope rejection timestamp mismatch', index, event);
  assertOperator(approval.actor, index, event);
  return replaceRecords(state, envelope, approval);
}

function applyV2Revoked(inputState, event, index) {
  const state = withBridgeState(inputState);
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'envelope', 'approval', 'actor', 'reason', 'created_at'],
    index,
    event
  );
  const { envelope, approval } = event;
  const previousEnvelope = state.envelopes[envelope.envelope_id];
  const previousApproval = state.approvals[approval.approval_id];
  assertOperator(event.actor, index, event);
  assertV2Record(envelope, 'envelope', index, event);
  assertV2Record(approval, 'approval', index, event);
  assertBinding(['approved', 'ready_for_poll'].includes(previousEnvelope?.state), 'envelope cannot be revoked', index, event);
  assertBinding(previousApproval?.state === 'authorized', 'authorization is not active', index, event);
  assertEnvelopeIdentity(previousEnvelope, envelope, index, event);
  assertApprovalIdentity(previousApproval, approval, index, event);
  assertBinding(envelope.state === 'blocked', 'revoked envelope must be blocked', index, event);
  assertBinding(approval.state === 'revoked', 'approval must be revoked', index, event);
  assertBinding(approval.revoked_at === event.created_at, 'revocation timestamp mismatch', index, event);
  assertBinding(envelope.approval.revoked_at === event.created_at, 'envelope revocation timestamp mismatch', index, event);
  assertBinding(approval.rejection_reason === event.reason, 'revocation reason mismatch', index, event);

  const next = replaceRecords(state, envelope, approval);
  return {
    ...next,
    bridge: {
      ...state.bridge,
      ready_target_envelope_id: state.bridge.ready_target_envelope_id === envelope.envelope_id
        ? null
        : state.bridge.ready_target_envelope_id,
      ready_target_selected_at: state.bridge.ready_target_envelope_id === envelope.envelope_id
        ? null
        : state.bridge.ready_target_selected_at
    }
  };
}

function reduceV2Event(state, event, index) {
  if (event.event_type === 'envelope.prepared') return applyV2Prepared(state, event, index);
  if (event.event_type === 'approval.granted') return applyV2Authorization(state, event, index);
  if (event.event_type === 'approval.rejected') return applyV2Rejected(state, event, index);
  if (event.event_type === 'approval.revoked') return applyV2Revoked(state, event, index);
  if (event.event_type === 'bridge.target_selected') return applyV2TargetSelected(state, event, index);
  if (event.event_type === 'bridge.target_cleared') return applyV2TargetCleared(state, event, index);
  if (event.event_type === 'bridge.claimed') return applyV2Claimed(state, event, index);
  if (event.event_type === 'bridge.interrupted') return applyV2Interrupted(state, event, index);
  if (event.event_type === 'bridge.claim_released') return applyV2Released(state, event, index);
  if (event.event_type === 'bridge.result_recorded') return applyV2Result(state, event, index);
  throw invalidHistory(`unknown v2 event_type ${event.event_type}`, index, event);
}

function withCanvasState(state) {
  if (state.canvas) return state;
  return {
    ...state,
    canvas: {
      schema_version: '1',
      current_surface_id: null,
      surfaces: {},
      revisions: {},
      interactions: [],
      interaction_cursor: 0
    }
  };
}

const CANVAS_SURFACE_KEYS = [
  'surface_id',
  'path',
  'title',
  'kind',
  'current_revision_id',
  'revision_ids',
  'created_at',
  'updated_at'
];

const CANVAS_REVISION_KEYS = [
  'revision_id',
  'surface_id',
  'content_sha256',
  'byte_length',
  'published_at'
];

const CANVAS_INTERACTION_KEYS = [
  'event_id',
  'cursor',
  'surface_id',
  'revision_id',
  'event_name',
  'payload',
  'received_at'
];

function assertCanvasSurface(surface, index, event) {
  assertExactKeys(surface, CANVAS_SURFACE_KEYS, index, event, 'surface');
  assertBinding(/^surface-[A-Za-z0-9][A-Za-z0-9._-]*$/.test(surface.surface_id), 'surface id invalid', index, event);
  assertBinding(typeof surface.path === 'string' && surface.path.endsWith('.html'), 'surface path invalid', index, event);
  assertBinding(typeof surface.title === 'string' && /\S/.test(surface.title), 'surface title invalid', index, event);
  assertBinding(['presentation', 'decision', 'craft', 'generic'].includes(surface.kind), 'surface kind invalid', index, event);
  assertBinding(Array.isArray(surface.revision_ids) && surface.revision_ids.length > 0, 'surface revision ids missing', index, event);
  assertBinding(new Set(surface.revision_ids).size === surface.revision_ids.length, 'surface revision ids duplicate', index, event);
  assertBinding(surface.revision_ids.at(-1) === surface.current_revision_id, 'surface current revision mismatch', index, event);
  assertBinding(typeof surface.created_at === 'string' && typeof surface.updated_at === 'string', 'surface timestamps invalid', index, event);
}

function assertCanvasRevision(revision, index, event) {
  assertExactKeys(revision, CANVAS_REVISION_KEYS, index, event, 'revision');
  assertBinding(/^revision-[A-Za-z0-9][A-Za-z0-9._-]*$/.test(revision.revision_id), 'revision id invalid', index, event);
  assertBinding(/^surface-[A-Za-z0-9][A-Za-z0-9._-]*$/.test(revision.surface_id), 'revision surface id invalid', index, event);
  assertBinding(/^[a-f0-9]{64}$/.test(revision.content_sha256), 'revision hash invalid', index, event);
  assertBinding(Number.isInteger(revision.byte_length) && revision.byte_length > 0, 'revision byte length invalid', index, event);
  assertBinding(typeof revision.published_at === 'string', 'revision timestamp invalid', index, event);
}

function applyCanvasPublished(inputState, event, index) {
  const state = withCanvasState(inputState);
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'surface', 'revision', 'created_at'],
    index,
    event
  );
  const { surface, revision } = event;
  assertCanvasSurface(surface, index, event);
  assertCanvasRevision(revision, index, event);
  assertBinding(revision.surface_id === surface.surface_id, 'revision surface binding mismatch', index, event);
  assertBinding(revision.revision_id === surface.current_revision_id, 'revision current binding mismatch', index, event);
  assertBinding(revision.published_at === event.created_at, 'revision publish timestamp mismatch', index, event);
  assertBinding(surface.updated_at === event.created_at, 'surface update timestamp mismatch', index, event);
  assertBinding(!state.canvas.revisions[revision.revision_id], 'duplicate canvas revision id', index, event);

  const existingById = state.canvas.surfaces[surface.surface_id];
  const existingByPath = Object.values(state.canvas.surfaces)
    .find((candidate) => candidate.path === surface.path);
  assertBinding(!existingByPath || existingByPath.surface_id === surface.surface_id, 'surface path identity changed', index, event);
  assertBinding(!existingById || existingById.path === surface.path, 'surface id path changed', index, event);

  if (existingById) {
    assertBinding(surface.created_at === existingById.created_at, 'surface creation timestamp changed', index, event);
    assertBinding(
      same(surface.revision_ids, [...existingById.revision_ids, revision.revision_id]),
      'surface revision order mismatch',
      index,
      event
    );
    const duplicateHash = existingById.revision_ids.some((revisionId) => (
      state.canvas.revisions[revisionId].content_sha256 === revision.content_sha256
    ));
    assertBinding(!duplicateHash, 'duplicate canvas revision hash', index, event);
  } else {
    assertBinding(surface.created_at === event.created_at, 'new surface creation timestamp mismatch', index, event);
    assertBinding(same(surface.revision_ids, [revision.revision_id]), 'new surface must start with one revision', index, event);
  }

  return {
    ...state,
    canvas: {
      ...state.canvas,
      current_surface_id: surface.surface_id,
      surfaces: { ...state.canvas.surfaces, [surface.surface_id]: surface },
      revisions: { ...state.canvas.revisions, [revision.revision_id]: revision }
    }
  };
}

function applyCanvasInteraction(inputState, event, index) {
  const state = withCanvasState(inputState);
  assertExactKeys(
    event,
    ['event_version', 'event_id', 'event_type', 'interaction', 'created_at'],
    index,
    event
  );
  const { interaction } = event;
  assertExactKeys(interaction, CANVAS_INTERACTION_KEYS, index, event, 'interaction');
  assertBinding(interaction.event_id === event.event_id, 'interaction event id mismatch', index, event);
  assertBinding(interaction.received_at === event.created_at, 'interaction timestamp mismatch', index, event);
  assertBinding(interaction.cursor === state.canvas.interaction_cursor + 1, 'interaction cursor is not monotonic', index, event);
  assertBinding(state.canvas.current_surface_id === interaction.surface_id, 'interaction surface is not current', index, event);
  const surface = state.canvas.surfaces[interaction.surface_id];
  assertBinding(surface?.current_revision_id === interaction.revision_id, 'interaction revision is not current', index, event);
  assertBinding(typeof interaction.event_name === 'string' && interaction.event_name.length > 0, 'interaction event name missing', index, event);
  assertBinding(
    interaction.payload && typeof interaction.payload === 'object' && !Array.isArray(interaction.payload),
    'interaction payload must be an object',
    index,
    event
  );

  return {
    ...state,
    canvas: {
      ...state.canvas,
      interactions: [...state.canvas.interactions, interaction],
      interaction_cursor: interaction.cursor
    }
  };
}

function reduceCanvasEvent(state, event, index) {
  if (event.event_type === 'canvas.surface_published') return applyCanvasPublished(state, event, index);
  if (event.event_type === 'canvas.interaction_recorded') return applyCanvasInteraction(state, event, index);
  throw invalidHistory(`unknown canvas event_type ${event.event_type}`, index, event);
}

export function reduceEvents(events, options = {}) {
  let state = createInitialWorkbench();
  const seenEventIds = new Set();

  for (const [index, event] of events.entries()) {
    assertHeader(event, index, seenEventIds);
    options.validateEvent?.(event, index);
    if (event.event_version === EVENT_VERSION) {
      state = reduceV1Event(state, event, index);
    } else if (event.event_version === BRIDGE_EVENT_VERSION) {
      state = reduceV2Event(state, event, index);
    } else {
      state = reduceCanvasEvent(state, event, index);
    }
  }

  return state;
}

export function projectionChecksum(projection) {
  return createHash('sha256').update(JSON.stringify(projection)).digest('hex');
}
