import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawn } from 'node:child_process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_FOUNDATION_ROOT = path.resolve(HERE, '../../../../cyberalchemy-foundation');
const SOURCE_CONTRACTS = Object.freeze({
  'schemas/agent-envelope.schema.json': '20dc7f52742effd8ceed47dce7aaa8d999f5ded39c1166feb75bc3b5f90b1a4e',
  'schemas/approval-record.schema.json': 'cd9d7aa0f7b0a661b949d4de0227a6f3aee123b772aaa73b4255e42ac1a4de68',
  'schemas/bridge-claim-request.schema.json': '43fe74967dcf7b490630b6f78e4f4330885c16177a908c15efdf98b5b4d3179f',
  'schemas/bridge-result-request.schema.json': '06ed6707c7d1f7c9b8747eaa0c0c96f48fbb1b956ae8a7d8949142ba7d120c36',
  'schemas/bridge-interrupt-request.schema.json': '123269241f5c38a92a22199a77cfd8c0988dcf030ce281a3fe2b52d0b5dd65b0',
  'schemas/receipt.schema.json': '2afbb8d4ef10d4e9af537e954f605418cf31500ef6a5aab2ceecdcf51398d9db'
});

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

function digestRecord(record) {
  return sha256(JSON.stringify(record));
}

async function fetchJson(fetchImpl, url, options) {
  const response = await fetchImpl(url, options);
  const body = JSON.parse(await response.text());
  if (!response.ok) {
    const error = new Error(body.message || body.error || `HTTP ${response.status}`);
    error.code = body.error || 'workbench_request_failed';
    error.status = response.status;
    throw error;
  }
  return body;
}

function runProcess(executable, args, input) {
  return new Promise((resolve, reject) => {
    const child = spawn(executable, args, { stdio: ['pipe', 'pipe', 'pipe'] });
    const stdout = [];
    const stderr = [];
    child.stdout.on('data', (chunk) => stdout.push(chunk));
    child.stderr.on('data', (chunk) => stderr.push(chunk));
    child.on('error', reject);
    child.on('close', (code) => {
      if (code !== 0) {
        const error = new Error(Buffer.concat(stderr).toString('utf8').trim() || `runtime exited ${code}`);
        error.code = 'foundation_runtime_failed';
        reject(error);
        return;
      }
      try {
        resolve(JSON.parse(Buffer.concat(stdout).toString('utf8')));
      } catch (error) {
        error.code = 'foundation_runtime_invalid_output';
        reject(error);
      }
    });
    child.stdin.end(JSON.stringify(input));
  });
}

async function distributionDigest(foundationRoot) {
  const refs = ['Cargo.lock', 'runtime/Cargo.toml', 'runtime/src/lib.rs',
    'runtime/src/bin/caf-runtime.rs', 'runtime/src/bin/caf-definition-projection-guest.rs'];
  const records = [];
  for (const ref of refs) records.push({ ref, sha256: sha256(await readFile(path.join(foundationRoot, ref))) });
  return digestRecord({ domain: 'caf.distribution-manifest/v1', records });
}

export async function executeFoundationClaim(options) {
  const {
    baseUrl,
    claimId,
    fetchImpl = fetch,
    foundationRoot = DEFAULT_FOUNDATION_ROOT,
    workbenchRoot = path.resolve(HERE, '../..'),
    runtimeBin = path.join(foundationRoot, 'target/debug/caf-runtime'),
    guestBin = path.join(foundationRoot, 'target/debug/caf-definition-projection-guest'),
    processRunner = runProcess
  } = options;
  const state = await fetchJson(fetchImpl, `${baseUrl}/api/state`);
  const claim = state.bridge?.claims?.[claimId];
  if (!claim || claim.state !== 'claimed') {
    const error = new Error('Foundation requires an active Workbench claim');
    error.code = 'foundation_claim_not_active';
    throw error;
  }
  const envelope = state.envelopes?.[claim.envelope_id];
  const approval = state.approvals?.[claim.approval_id];
  if (!envelope || envelope.state !== 'claimed' || approval?.state !== 'authorized') {
    const error = new Error('Workbench authorization is not active');
    error.code = 'foundation_authorization_not_active';
    throw error;
  }
  if (envelope.requested_skill !== 'foundation-definition-projector') {
    const error = new Error('This adapter only executes the Foundation definition projector');
    error.code = 'foundation_skill_unsupported';
    throw error;
  }

  const compilerUrl = pathToFileURL(path.join(foundationRoot, 'src/workbench-foundation-adapter.mjs'));
  const compiler = await import(compilerUrl.href);
  const definitionBytes = await readFile(path.join(foundationRoot, 'definitions/DEFINITIONS.md'));
  const adapterBytes = await readFile(fileURLToPath(import.meta.url));
  const distribution = await distributionDigest(foundationRoot);
  const hostContract = { id: 'caf.host-contract.ide-workbench/v1', ports: ['preview.read', 'skill.invoke'] };
  const capabilityProfile = { id: 'caf.profile.definition-projector/v1', effect_class: 'effect-free', declared_ports: ['preview.read', 'skill.invoke'] };
  const effectEnvelope = { id: 'caf.effect-envelope.none/v1', external_effects: [], credential_refs: [], network: 'denied', filesystem: 'brokered-read-only' };
  const binding = {
    schema_version: compiler.SCHEMA_VERSION,
    binding_id: `binding-${claim.claim_attempt_id}`,
    candidate_status: 'prototype-candidate',
    authority_effect: 'none',
    host: {
      host_id: 'ide-workbench.local',
      control_plane: 'ide-extension.manual-session-bridge/v2',
      adapter_id: 'caf.workbench-adapter/v1',
      adapter_sha256: sha256(adapterBytes),
      source_contracts: Object.entries(SOURCE_CONTRACTS).map(([ref, digest]) => ({ ref, sha256: digest }))
    },
    workbench: {
      state: claim.state,
      run_id: claim.run_id,
      envelope_id: claim.envelope_id,
      approval_id: claim.approval_id,
      authorization_receipt_id: envelope.authorization_receipt_id,
      claim_id: claim.claim_id,
      claim_attempt_id: claim.claim_attempt_id,
      agent_ref: claim.agent_ref,
      session_ref: claim.session_ref,
      assurance: claim.assurance,
      requested_skill: envelope.requested_skill,
      requested_grants: envelope.requested_grants,
      task_sha256: sha256(JSON.stringify(envelope.task)),
      effect_profile: 'preview.read'
    },
    foundation: {
      distribution: { algorithm: 'sha256', manifest_sha256: distribution },
      installed_guest: { host_id: 'ide-workbench.local', installation_id: 'caf-definition-projector.local-v1', distribution_manifest_sha256: distribution },
      host_contract: { id: hostContract.id, sha256: digestRecord(hostContract) },
      capability_profile: { ...capabilityProfile, sha256: digestRecord(capabilityProfile) },
      effect_envelope: { ...effectEnvelope, sha256: digestRecord(effectEnvelope) },
      input_artifact: {
        ref: 'definitions/DEFINITIONS.md', sha256: sha256(definitionBytes),
        owner_route: 'foundation-definitions-owner', boundary: 'candidate-definitions-read-only',
        claim_ceiling: 'projection-not-source-truth'
      },
      transition: { transition_id: `transition-${claim.claim_attempt_id}`, kind: 'invoke', from: 'enabled', to: 'invoked', idempotency_key: '' }
    },
    ownership: {
      host_system_of_record: 'ide-extension', foundation_result_disposition: 'candidate-only',
      execution_receipt_minter: 'ide-extension', foundation_may_commit_host_state: false
    }
  };
  binding.foundation.transition.idempotency_key = compiler.invocationIdempotencyKey(binding);
  await compiler.verifyWorkbenchSourceContracts(binding, workbenchRoot);
  const invocation = compiler.compileFoundationInvokeRequest(binding);
  const runtime = await processRunner(runtimeBin, [
    '--guest-bin', guestBin,
    '--definitions', path.join(foundationRoot, 'definitions/DEFINITIONS.md')
  ], invocation);
  const resultBody = {
    schema_version: '2', claim_id: claim.claim_id, claim_attempt_id: claim.claim_attempt_id,
    envelope_id: claim.envelope_id, run_id: claim.run_id, approval_id: claim.approval_id,
    session_ref: claim.session_ref, assurance: claim.assurance,
    requested_skill: envelope.requested_skill,
    skill_sha256: sha256(await readFile(guestBin)), status: 'passed',
    summary: `Projected ${runtime.guest_result.definitions.length} current Foundation definitions from ${runtime.guest_result.source.sha256}.`,
    validation: [
      `binding:${binding.binding_id}`,
      `containment:${runtime.containment.mechanism}`,
      `source-currentness:${runtime.guest_result.source.currentness}`,
      'receipt-custody:ide-extension'
    ],
    evidence_refs: ['projects/ide-extension/src/adapters/foundation.mjs']
  };
  const admitted = await fetchJson(fetchImpl, `${baseUrl}/api/bridge/claims/${claimId}/result`, {
    method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(resultBody)
  });
  return { binding, invocation, runtime, admitted };
}
