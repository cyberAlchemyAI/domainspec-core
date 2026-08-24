import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';

const root = new URL('../', import.meta.url);
const load = async path => JSON.parse(await readFile(new URL(path, root), 'utf8'));
const digest = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');

function closed(value, schema) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;
  if (schema.required?.some(key => !(key in value))) return false;
  return schema.additionalProperties !== false || Object.keys(value).every(key => key in (schema.properties ?? {}));
}

function validateCommand(command, schema) {
  if (!closed(command, schema)) return false;
  if (!schema.properties.operation.enum.includes(command.operation)) return false;
  if (command.operation === 'open_episode' && (command.episode_id !== null || command.expected_revision !== 0)) return false;
  if (command.operation !== 'open_episode' && typeof command.episode_id !== 'string') return false;
  const branch = schema.allOf.find(item => item.if.properties.operation.const === command.operation)?.then.properties.payload;
  return Boolean(branch && closed(command.payload, branch));
}

test('neutral projection accepts safe records and rejects leakage without digest', async () => {
  const [schema, allowlist, cases] = await Promise.all([load('contracts/neutral-projection-record.schema.json'), load('contracts/projection-allowlist.json'), load('fixtures/projection-contract-cases.json')]);
  assert.equal(closed(cases.accepted_records[0], schema), true);
  assert.match(digest(cases.accepted_records), /^[a-f0-9]{64}$/);
  for (const mutant of cases.rejected_mutants) {
    const candidate = { ...cases.accepted_records[0], [mutant.field]: mutant.value };
    const findings = Object.keys(candidate).filter(key => !allowlist.record_fields.includes(key) || allowlist.forbidden_fields.includes(key));
    const result = findings.length ? { status: 'rejected', findings } : { status: 'accepted', projection_digest: digest(candidate) };
    assert.equal(result.status, 'rejected', mutant.name);
    assert.equal('projection_digest' in result, false, mutant.name);
  }
});

test('neutral projection manifest excludes unknown views and fields', async () => {
  const schema = await load('contracts/neutral-projection-manifest.schema.json');
  assert.equal(schema.additionalProperties, false);
  assert.deepEqual(schema.properties.views.items.enum, ['documentation', 'recipe', 'operational_episode']);
});

test('episode contract admits five closed operations', async () => {
  const [schema, cases] = await Promise.all([load('contracts/episode-command.schema.json'), load('fixtures/episode-contract-cases.json')]);
  assert.deepEqual(schema.properties.operation.enum, ['open_episode', 'append_attempt', 'attach_evidence', 'record_outcome', 'close_episode']);
  assert.equal(schema.properties.operation.enum.includes('supersede_episode'), false);
  for (const command of cases.valid_commands) assert.equal(validateCommand(command, schema), true, command.operation);
});

test('episode contract rejects host fields, caller open ID, and generic operation', async () => {
  const [schema, cases] = await Promise.all([load('contracts/episode-command.schema.json'), load('fixtures/episode-contract-cases.json')]);
  const open = cases.valid_commands[0];
  for (const invalid of cases.invalid_cases) {
    const command = { ...open, [invalid.field]: invalid.value };
    assert.equal(validateCommand(command, schema), false, invalid.name);
  }
});

test('episode contract closes statuses and semantic effect', async () => {
  const [result, codes, event] = await Promise.all([load('contracts/episode-result.schema.json'), load('contracts/status-codes.json'), load('contracts/episode-event.schema.json')]);
  assert.deepEqual(result.properties.status.enum, codes.append_statuses);
  assert.equal(result.properties.semantic_effect.const, 'none');
  assert.equal(result.properties.task_state_unchanged.const, true);
  assert.equal(result.properties.truth_status.const, 'not_assessed');
  assert.deepEqual(event.properties.event_type.enum, ['EpisodeOpened', 'AttemptAppended', 'EvidenceAttached', 'OutcomeRecorded', 'EpisodeClosed']);
  assert.ok(codes.diagnostic_codes.includes('IDEMPOTENCY_MISMATCH'));
  assert.ok(codes.diagnostic_codes.includes('EPISODE_QUARANTINED'));
});

export { closed, validateCommand };
