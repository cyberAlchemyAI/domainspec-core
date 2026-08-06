import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

import { buildCandidate } from '../lib/build-candidate.mjs';
import { consultCandidate, consultationContract } from '../lib/consult-animejs.mjs';
import { evaluateEligibility } from '../lib/evaluate-eligibility.mjs';

const testRoot = path.dirname(fileURLToPath(import.meta.url));
const runRoot = path.resolve(testRoot, '../..');
const liveRunRoot = process.cwd();
const repositoryRoot = path.resolve(liveRunRoot, '../../../../..');
const vaultRoot = path.join(repositoryRoot, 'projects/animejs/ontology/agent-knowledge-vault');
const readJson = async (target) => JSON.parse(await readFile(target, 'utf8'));
const { validateCandidate } = await import(pathToFileURL(path.join(liveRunRoot, 'prototype/lib/validate-candidate.mjs')).href);

const seed = await readJson(path.join(liveRunRoot, 'prototype/fixtures/candidate.valid.json'));
const schema = await readJson(path.join(liveRunRoot, 'prototype/contracts/animation-hypothesis-candidate.schema.json'));
const sourceSnapshot = await readJson(path.join(liveRunRoot, 'prototype/fixtures/source-snapshot.json'));
const recipesView = await readJson(path.join(vaultRoot, 'views/task-recipes.json'));
const validationContext = { schema, sourceSnapshot, repositoryRoot, validateCandidate };

function candidateInput(overrides = {}) {
  return {
    candidate_id: seed.candidate_id,
    hypothesis: seed.hypothesis,
    semantic_contract: seed.semantic_contract,
    proof_ledger: seed.proof_ledger,
    contradiction: seed.contradiction,
    prototype_scope: seed.prototype_scope,
    witness_spec: seed.witness_spec,
    tournament_binding: seed.tournament_binding,
    owner_review: seed.owner_review,
    consultation_request_id: 'oava002-consult-s6-v1',
    version_context: { library: 'animejs', version: '4.5.0', runtime_used: false },
    preconsultation_evidence_bindings: ['work-pack/closeouts/SWU-OAVA-001.json'],
    ...overrides,
  };
}

function host(overrides = {}) {
  return {
    vault_root: vaultRoot,
    host_context: {
      principal_id: 'principal:oava002',
      tenant_or_workspace_id: 'workspace:domainspec-core',
      capabilities: ['animejs-knowledge-consult-read'],
      policy_epoch: 'policy:oava002-v1',
      vault_scope: 'animejs-agent-knowledge-vault',
      request_id: 'oava002-consult-s6-v1',
      received_at: '2026-08-06T13:33:00Z',
    },
    credential: { audience: 'animejs-knowledge-consult-read' },
    authorize: async () => ({
      authorized: true,
      views: ['documentation', 'recipe'],
      limits: { max_results: 12, max_hops: 2, max_response_bytes: 65536 },
    }),
    limits: { max_results: 12, max_hops: 2, max_response_bytes: 65536 },
    expected: { graph_digest: recipesView.graph_digest, projection_digest: null },
    ...overrides,
  };
}

async function fileMap(root) {
  const result = {};
  async function walk(current) {
    for (const entry of await readdir(current, { withFileTypes: true })) {
      const absolute = path.join(current, entry.name);
      if (entry.isDirectory()) await walk(absolute);
      if (entry.isFile()) {
        const relative = path.relative(root, absolute).split(path.sep).join('/');
        result[relative] = createHash('sha256').update(await readFile(absolute)).digest('hex');
      }
    }
  }
  await walk(root);
  return result;
}

function typedNegative(receipt, status) {
  const result = {
    ...structuredClone(receipt.result),
    status,
    records: [],
    edges: [],
    explanation_path: [],
    diagnostic: { code: `TEST_${status.toUpperCase()}` },
  };
  return { ...structuredClone(receipt), result, evidence_bindings: [] };
}

test('builder is deterministic, schema-valid, and input-pure', async () => {
  const scene = structuredClone(seed.scene_beat_ref);
  const residue = candidateInput();
  const before = structuredClone({ scene, residue });
  const left = buildCandidate(scene, residue);
  const right = buildCandidate(structuredClone(scene), structuredClone(residue));
  assert.deepEqual(left, right);
  assert.deepEqual({ scene, residue }, before);
  assert.equal(left.consultation.status, 'abstain');
  assert.equal((await validateCandidate({ candidate: left, ...validationContext })).code, 'VALID');
});

test('actual local vault consultation returns exact records and admits only documented capability', async () => {
  const before = await fileMap(vaultRoot);
  const candidate = buildCandidate(seed.scene_beat_ref, candidateInput());
  const receipt = await consultCandidate(candidate, host());
  assert.equal(receipt.result.status, 'ok');
  assert.deepEqual(receipt.result.records.map((record) => record.record_id), [...consultationContract.node_ids].sort());
  const expectedEvidence = [
    'evidence:documentation:3dc740ebfb16cdb8a2336824',
    'evidence:documentation:633e03704b3caee5b819f133',
    'evidence:documentation:e05dc4243933cc3d17a9e583',
  ].sort();
  assert.deepEqual(receipt.evidence_bindings, expectedEvidence);
  const decision = await evaluateEligibility({ candidate, consultationReceipt: receipt, validationContext });
  assert.deepEqual([decision.eligible, decision.code, decision.state], [true, 'TOURNAMENT_ELIGIBLE', 'tournament_eligible']);
  assert.deepEqual(decision.evidence_bindings, expectedEvidence);
  assert.equal(decision.candidate.consultation.status, 'ok');
  assert.equal(decision.candidate.proof_ledger.some((entry) => entry.proof_state === 'executed_witness'), false);
  assert.deepEqual(await fileMap(vaultRoot), before);
});

test('consultation and request identities are deterministic', async () => {
  const candidate = buildCandidate(seed.scene_beat_ref, candidateInput());
  const left = await consultCandidate(candidate, host());
  const right = await consultCandidate(candidate, host());
  assert.deepEqual(left, right);
  assert.equal(left.result.request_id, candidate.consultation.request_id);
});

test('wrong expected graph digest produces stale with no evidence', async () => {
  const candidate = buildCandidate(seed.scene_beat_ref, candidateInput());
  const receipt = await consultCandidate(candidate, host({ expected: { graph_digest: 'f'.repeat(64), projection_digest: null } }));
  assert.deepEqual([receipt.result.status, receipt.result.records.length, receipt.evidence_bindings.length], ['stale', 0, 0]);
  const decision = await evaluateEligibility({ candidate, consultationReceipt: receipt, validationContext });
  assert.deepEqual([decision.eligible, decision.code], [false, 'CONSULTATION_STALE']);
});

test('every typed non-ok result is preserved and blocks without fallback', async () => {
  const candidate = buildCandidate(seed.scene_beat_ref, candidateInput());
  const ok = await consultCandidate(candidate, host());
  for (const status of ['abstain', 'denied', 'invalid_request', 'temporary_failure']) {
    const receipt = typedNegative(ok, status);
    const decision = await evaluateEligibility({ candidate, consultationReceipt: receipt, validationContext });
    assert.deepEqual([decision.eligible, decision.code, decision.consultation_status], [false, 'CONSULTATION_NOT_OK', status]);
    assert.equal(decision.candidate, null);
  }
});

test('empty evidence, request mismatch, binding mismatch, and version mismatch fail causally', async () => {
  const candidate = buildCandidate(seed.scene_beat_ref, candidateInput());
  const ok = await consultCandidate(candidate, host());
  const empty = structuredClone(ok);
  empty.result.records = [];
  empty.result.explanation_path = [];
  empty.evidence_bindings = [];
  assert.equal((await evaluateEligibility({ candidate, consultationReceipt: empty, validationContext })).code, 'CONSULTATION_EVIDENCE_EMPTY');

  const wrongRequest = structuredClone(ok);
  wrongRequest.result.request_id = 'other-request';
  assert.equal((await evaluateEligibility({ candidate, consultationReceipt: wrongRequest, validationContext })).code, 'CONSULTATION_REQUEST_MISMATCH');

  const wrongBinding = structuredClone(ok);
  wrongBinding.evidence_bindings = ['evidence:documentation:not-returned'];
  assert.equal((await evaluateEligibility({ candidate, consultationReceipt: wrongBinding, validationContext })).code, 'CONSULTATION_BINDING_MISMATCH');

  const wrongVersion = buildCandidate(seed.scene_beat_ref, candidateInput({ version_context: { library: 'animejs', version: '4.4.0', runtime_used: false } }));
  assert.equal((await evaluateEligibility({ candidate: wrongVersion, consultationReceipt: ok, validationContext })).code, 'VERSION_CONTEXT_MISMATCH');
});

test('candidate and semantic hard gates remain in force', async () => {
  const candidate = buildCandidate(seed.scene_beat_ref, candidateInput());
  const ok = await consultCandidate(candidate, host());
  const invalid = structuredClone(candidate);
  invalid.scene_beat_ref.source_package_digest = '0'.repeat(64);
  assert.equal((await evaluateEligibility({ candidate: invalid, consultationReceipt: ok, validationContext })).code, 'CANDIDATE_INVALID');

  const contradiction = structuredClone(candidate);
  contradiction.contradiction.resolution_status = 'unresolved';
  assert.equal((await evaluateEligibility({ candidate: contradiction, consultationReceipt: ok, validationContext })).code, 'CONTRADICTION_OPEN');

  const reduced = structuredClone(candidate);
  reduced.semantic_contract.reduced_motion_state_machine[
    reduced.semantic_contract.reduced_motion_state_machine.length - 1
  ] = 'different-terminal';
  assert.equal((await evaluateEligibility({ candidate: reduced, consultationReceipt: ok, validationContext })).code, 'REDUCED_MOTION_MISMATCH');
});

test('consumer source contains no network, process, vault-write, or Anime.js runtime path', async () => {
  const files = ['build-candidate.mjs', 'consult-animejs.mjs', 'evaluate-eligibility.mjs'];
  const source = (await Promise.all(files.map((name) => readFile(path.join(runRoot, 'prototype/lib', name), 'utf8')))).join('\n');
  assert.doesNotMatch(source, /\bfetch\s*\(|node:https|node:http|child_process|writeFile|appendFile|anime\.esm\.js/);
});
