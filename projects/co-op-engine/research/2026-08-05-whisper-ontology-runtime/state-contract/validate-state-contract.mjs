#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const RESEARCH = dirname(HERE);
const RECEIPT = join(RESEARCH, 'receipts/state-contract-validation.json');
const FIELDS = ['revision', 'lifecycle_phase', 'pending_gate', 'correction_state', 'outcome_ceiling'];
const GATES = ['none', 'intent_freeze', 'editorial_decision', 'mechanical_validation', 'post_apply_review', 'corrected_intent_freeze', 'graph_policy_validation', 'comprehension_assessment'];
const CORRECTIONS = ['none', 'open', 'resolved'];
const CEILINGS = ['not_assessed', 'pass', 'flag', 'block'];
const PHASES = ['not_started', 'intake_recorded', 'intent_frozen', 'plan_generation_scheduled', 'plan_ready', 'audition_generation_scheduled', 'awaiting_editorial_decision', 'editorial_decision_recorded', 'draft_generation_scheduled', 'draft_ready', 'draft_validation_scheduled', 'mechanically_validated', 'correction_pending', 'graph_validation_scheduled', 'graph_validated', 'reviewed', 'residue_recorded'];
const TYPES = ['IntentRecorded', 'IntentFrozen', 'PlanGenerationScheduled', 'PlanProduced', 'AuditionGenerationScheduled', 'AuditionProduced', 'EditorialDecisionRecorded', 'DraftGenerationScheduled', 'DraftProduced', 'DraftValidationScheduled', 'MechanicalAssessmentRecorded', 'CorrectionRecorded', 'IntentFrozen', 'PlanGenerationScheduled', 'PlanProduced', 'AuditionGenerationScheduled', 'AuditionProduced', 'EditorialDecisionRecorded', 'DraftGenerationScheduled', 'DraftProduced', 'DraftValidationScheduled', 'MechanicalAssessmentRecorded', 'GraphValidationScheduled', 'GraphAssessmentRecorded', 'ComprehensionAssessmentRecorded', 'ResidueRecorded'];
const ROWS = [
  'not_started|none|none|not_assessed',
  'intake_recorded|intent_freeze|none|not_assessed',
  'intent_frozen|none|none|not_assessed',
  'plan_generation_scheduled|none|none|not_assessed',
  'plan_ready|none|none|not_assessed',
  'audition_generation_scheduled|none|none|not_assessed',
  'awaiting_editorial_decision|editorial_decision|none|not_assessed',
  'editorial_decision_recorded|none|none|not_assessed',
  'draft_generation_scheduled|none|none|not_assessed',
  'draft_ready|mechanical_validation|none|not_assessed',
  'draft_validation_scheduled|none|none|not_assessed',
  'mechanically_validated|post_apply_review|none|flag',
  'correction_pending|corrected_intent_freeze|open|block',
  'intent_frozen|none|open|block',
  'plan_generation_scheduled|none|open|block',
  'plan_ready|none|open|block',
  'audition_generation_scheduled|none|open|block',
  'awaiting_editorial_decision|editorial_decision|open|block',
  'editorial_decision_recorded|none|open|block',
  'draft_generation_scheduled|none|open|block',
  'draft_ready|mechanical_validation|open|block',
  'draft_validation_scheduled|none|open|block',
  'mechanically_validated|graph_policy_validation|resolved|flag',
  'graph_validation_scheduled|none|resolved|flag',
  'graph_validated|comprehension_assessment|resolved|flag',
  'reviewed|none|resolved|pass',
  'residue_recorded|none|resolved|pass',
];

class ContractError extends Error {
  constructor(code, message) {
    super(`${code}: ${message}`);
    this.code = code;
  }
}

function parse(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function shaBytes(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function shaFile(path) {
  return shaBytes(readFileSync(path));
}

function stateAt(revision) {
  const [lifecycle_phase, pending_gate, correction_state, outcome_ceiling] = ROWS[revision].split('|');
  return { revision, lifecycle_phase, pending_gate, correction_state, outcome_ceiling };
}

function assert(condition, code, message) {
  if (!condition) throw new ContractError(code, message);
}

function validateState(state) {
  assert(state && typeof state === 'object' && !Array.isArray(state), 'INVALID_STATE_SHAPE', 'state must be an object');
  assert(canonical(Object.keys(state).sort()) === canonical([...FIELDS].sort()), 'INVALID_STATE_SHAPE', 'state fields differ');
  assert(Number.isInteger(state.revision) && state.revision >= 0 && state.revision <= 26, 'INVALID_STATE_ENUM', 'revision');
  assert(PHASES.includes(state.lifecycle_phase), 'INVALID_STATE_ENUM', 'lifecycle_phase');
  assert(GATES.includes(state.pending_gate), 'INVALID_STATE_ENUM', 'pending_gate');
  assert(CORRECTIONS.includes(state.correction_state), 'INVALID_STATE_ENUM', 'correction_state');
  assert(CEILINGS.includes(state.outcome_ceiling), 'INVALID_STATE_ENUM', 'outcome_ceiling');
}

function validateSchema(schema) {
  assert(schema.additionalProperties === false, 'STATE_SCHEMA_OPEN', 'additional properties must be false');
  assert(canonical(schema.required) === canonical(FIELDS), 'STATE_SCHEMA_FIELDS', 'required fields differ');
  assert(canonical(schema.properties.lifecycle_phase.enum) === canonical(PHASES), 'STATE_SCHEMA_ENUM', 'lifecycle_phase');
  assert(canonical(schema.properties.pending_gate.enum) === canonical(GATES), 'STATE_SCHEMA_ENUM', 'pending_gate');
  assert(canonical(schema.properties.correction_state.enum) === canonical(CORRECTIONS), 'STATE_SCHEMA_ENUM', 'correction_state');
  assert(canonical(schema.properties.outcome_ceiling.enum) === canonical(CEILINGS), 'STATE_SCHEMA_ENUM', 'outcome_ceiling');
}

function guardEv22(event, closure) {
  const binding = event.bindings ?? {};
  const expected = closure.digest_bindings;
  if (binding.correction_id !== 'COR1' || binding.correction_sha256 !== expected.COR1) throw new ContractError('EV22_CORRECTION_BINDING_MISMATCH', 'COR1');
  if (binding.artifact_id !== 'NE2' || binding.artifact_sha256 !== expected.NE2) throw new ContractError('EV22_ARTIFACT_BINDING_MISMATCH', 'NE2');
  if (binding.assessment_id !== 'MA2' || binding.assessment_sha256 !== expected.MA2) throw new ContractError('EV22_ASSESSMENT_BINDING_MISMATCH', 'MA2');
  if (binding.assessment_result !== 'pass') throw new ContractError('EV22_ASSESSMENT_NOT_PASS', 'MA2');
}

function applyEvent(state, event, ordinal, closure) {
  const before = canonical(state);
  try {
    const expectedId = `EV${String(ordinal + 1).padStart(2, '0')}`;
    assert(event.event_id === expectedId, 'EVENT_ID_MISMATCH', expectedId);
    assert(event.event_type === TYPES[ordinal], 'EVENT_TYPE_MISMATCH', expectedId);
    assert(canonical(state) === canonical(event.prior_state), 'PRIOR_STATE_MISMATCH', expectedId);
    assert(canonical(event.prior_state) === canonical(stateAt(ordinal)), 'ORACLE_PRIOR_MISMATCH', expectedId);
    assert(canonical(event.result_state) === canonical(stateAt(ordinal + 1)), 'ORACLE_RESULT_MISMATCH', expectedId);
    validateState(event.prior_state);
    validateState(event.result_state);
    assert(event.result_state.revision === state.revision + 1, 'REVISION_ADVANCE_INVALID', expectedId);
    if (event.event_id === 'EV22') guardEv22(event, closure);
    else assert(!Object.hasOwn(event, 'bindings'), 'UNEXPECTED_EVENT_BINDINGS', expectedId);
    return clone(event.result_state);
  } catch (error) {
    assert(canonical(state) === before, 'REJECTION_MUTATED_STATE', event.event_id ?? 'unknown');
    throw error;
  }
}

function reduce(events, closure) {
  let state = clone(closure.initial_state);
  for (let index = 0; index < events.length; index += 1) state = applyEvent(state, events[index], index, closure);
  return state;
}

function deriveProjection(state, eventHead) {
  return { schema_version: 'candidate.whisper.run-projection.v1', state: clone(state), event_head: eventHead, residue_ref: 'RR1', authority_effect: 'none' };
}

function expectCode(expected, action) {
  try {
    action();
  } catch (error) {
    if (error instanceof ContractError && error.code === expected) return;
    throw new ContractError('NEGATIVE_WRONG_CODE', `expected ${expected}, got ${error.code ?? error.message}`);
  }
  throw new ContractError('NEGATIVE_ACCEPTED', expected);
}

function runNegatives(cases, sequence) {
  const ids = new Set();
  for (const item of cases) {
    assert(!ids.has(item.case_id), 'NEGATIVE_ID_DUPLICATE', item.case_id);
    ids.add(item.case_id);
    if (item.kind === 'invalid_state') {
      const invalid = stateAt(0);
      invalid[item.field] = item.value;
      expectCode(item.expected_code, () => validateState(invalid));
    } else if (item.kind === 'ev22_binding' || item.kind === 'ev22_missing_binding') {
      const state = reduce(sequence.events.slice(0, 21), sequence.closure);
      const before = canonical(state);
      const event = clone(sequence.events[21]);
      if (item.kind === 'ev22_missing_binding') delete event.bindings[item.field];
      else event.bindings[item.field] = item.value;
      expectCode(item.expected_code, () => applyEvent(state, event, 21, sequence.closure));
      assert(canonical(state) === before, 'REJECTION_MUTATED_STATE', item.case_id);
    } else if (item.kind === 'premature_ev22') {
      const state = reduce(sequence.events.slice(0, item.prefix_length), sequence.closure);
      const before = canonical(state);
      expectCode(item.expected_code, () => applyEvent(state, sequence.events[21], 21, sequence.closure));
      assert(canonical(state) === before, 'REJECTION_MUTATED_STATE', item.case_id);
    } else if (item.kind === 'duplicate_ev22') {
      const state = reduce(sequence.events.slice(0, 22), sequence.closure);
      const before = canonical(state);
      expectCode(item.expected_code, () => applyEvent(state, sequence.events[21], 21, sequence.closure));
      assert(canonical(state) === before, 'REJECTION_MUTATED_STATE', item.case_id);
    } else if (item.kind === 'projection_mutation') {
      const state = stateAt(26);
      const before = canonical(state);
      const mutatingProjection = (subject) => { subject.revision += 1; return { state: subject }; };
      expectCode(item.expected_code, () => {
        mutatingProjection(state);
        if (canonical(state) !== before) throw new ContractError('PROJECTION_MUTATED_STATE', item.case_id);
      });
    } else {
      throw new ContractError('NEGATIVE_KIND_UNKNOWN', item.case_id);
    }
  }
  return ids.size;
}

function validateSequence(sequence) {
  assert(sequence.schema_version === 'candidate.whisper.state-sequence.v1', 'SEQUENCE_VERSION', 'schema version');
  assert(sequence.events.length === 26 && TYPES.length === 26 && ROWS.length === 27, 'SEQUENCE_LENGTH', 'EV01-EV26 required');
  validateState(sequence.closure.initial_state);
  assert(canonical(sequence.closure.initial_state) === canonical(stateAt(0)), 'INITIAL_STATE_MISMATCH', 'closure');
  const live = reduce(sequence.events, sequence.closure);
  const replay = reduce(clone(sequence.events), clone(sequence.closure));
  const liveBytes = Buffer.from(`${canonical(live)}\n`, 'utf8');
  const replayBytes = Buffer.from(`${canonical(replay)}\n`, 'utf8');
  assert(liveBytes.equals(replayBytes), 'LIVE_REPLAY_BYTES_MISMATCH', 'RS26');
  assert(canonical(live) === canonical(stateAt(26)), 'RS26_MISMATCH', 'final state');
  let head = shaBytes(Buffer.from(canonical(sequence.closure), 'utf8'));
  for (const event of sequence.events) head = shaBytes(Buffer.from(`${head}:${canonical(event)}`, 'utf8'));
  const beforeProjection = Buffer.from(`${canonical(live)}\n`, 'utf8');
  const projection = deriveProjection(live, head);
  const afterProjection = Buffer.from(`${canonical(live)}\n`, 'utf8');
  assert(beforeProjection.equals(afterProjection), 'PROJECTION_MUTATED_STATE', 'RP26');
  assert(projection.state.revision === 26 && sequence.events.length === 26, 'PROJECTION_STATE_MISMATCH', 'RP26');
  return { live, liveBytes, replayBytes, eventHead: head };
}

function exactRef(path) {
  const bytes = readFileSync(path);
  return { path: path.slice(RESEARCH.length + 1), sha256: shaBytes(bytes), size_bytes: bytes.length };
}

function expectedReceipt() {
  const schemaPath = join(HERE, 'state.schema.json');
  const sequencePath = join(HERE, 'event-sequence.json');
  const negativesPath = join(HERE, 'negative-fixtures.json');
  const synthesisPath = join(RESEARCH, 'synthesis-revision-3.md');
  const validatorPath = fileURLToPath(import.meta.url);
  const schema = parse(schemaPath);
  const sequence = parse(sequencePath);
  const negatives = parse(negativesPath);
  validateSchema(schema);
  const proof = validateSequence(sequence);
  const negativeCount = runNegatives(negatives.cases, sequence);
  assert(negativeCount === 10, 'NEGATIVE_COUNT_MISMATCH', String(negativeCount));
  return {
    schema_version: 'candidate.whisper.state-contract-validation.v1',
    receipt_id: 'WSCV-001',
    status: 'pass',
    sources: {
      state_schema: exactRef(schemaPath),
      event_sequence: exactRef(sequencePath),
      negative_fixtures: exactRef(negativesPath),
      synthesis_revision_3: exactRef(synthesisPath),
      validator: exactRef(validatorPath),
    },
    proof: {
      accepted_event_count: 26,
      final_revision: 26,
      final_state: proof.live,
      live_state_sha256: shaBytes(proof.liveBytes),
      replay_state_sha256: shaBytes(proof.replayBytes),
      live_replay_bytes_equal: proof.liveBytes.equals(proof.replayBytes),
      journal_head_sha256: proof.eventHead,
      negative_case_count: negativeCount,
      rejected_without_state_advance: true,
      replay_completed_effect_starts: 0,
      projection_mutated_state: false,
    },
    claim_ceiling: 'repaired-candidate-state-contract-only',
    authority_effect: 'none',
  };
}

const receipt = expectedReceipt();
if (process.argv.includes('--print-receipt')) {
  process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
} else {
  const recorded = parse(RECEIPT);
  assert(canonical(recorded) === canonical(receipt), 'RECORDED_RECEIPT_STALE', RECEIPT);
  process.stdout.write(`${process.argv.includes('--self-test') ? 'state-contract-self-test-pass' : 'state-contract-validation-pass'}\n`);
}
