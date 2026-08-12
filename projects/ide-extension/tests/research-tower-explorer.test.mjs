import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';
import { createServer } from '../src/server.mjs';
import {
  loadResearchTowerL0,
  ResearchTowerWitnessError,
  buildVerificationPromptProjections,
  resolveFixtureSourceBindings,
  sha256,
  validateTowerSceneManifest,
  validateVerificationPromptProjections
} from '../src/research-tower/l0-witness.mjs';

const repositoryRoot = path.resolve(fileURLToPath(new URL('../../..', import.meta.url)));
const projectRoot = path.join(repositoryRoot, 'projects/ide-extension');
const witnessDir = path.join(repositoryRoot, 'projects/cyberalchemy-lab/development/witness-runs/l0-synthetic-001');
const visualAssetDir = path.join(projectRoot, 'public/assets/research-tower-concepts');
const sourceRoot = path.join(repositoryRoot, 'projects/cyberalchemy-lab/research/tower-evidence-navigator');

function listen(server) { return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server.address().port))); }
function close(server) { return new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve())); }

test('approved room assets retain their exact PNG bytes and dimensions', async () => {
  const contracts = [
    ['robot-paper-library.png', '1a224bba26856807db877c7af73bba9f3f7eca076561d3befe67f593259d8536', 1672, 941],
    ['autonomous-observatory-lab.png', '467d5977e960dd4417fbee3d004638f40b0f34a5a9ee0218e02a68c86f063019', 1672, 941],
    ['night-knowledge-observatory.png', '28b2b703228ac0ab33fa4b44d74ce9e09b304d822fb85a789bf9483ae923bc5f', 1672, 941],
    ['robot-cowork-rpg-sprite-sheet.png', '04fa18bb405b59380b4be2b5a88bebd88632837e1fd21467e626832f43e37afa', 2172, 724]
  ];
  for (const [name, digest, width, height] of contracts) {
    const bytes = await readFile(path.join(visualAssetDir, name));
    assert.equal(bytes.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
    assert.equal(bytes.subarray(12, 16).toString('ascii'), 'IHDR');
    assert.equal(bytes.readUInt32BE(16), width);
    assert.equal(bytes.readUInt32BE(20), height);
    assert.equal(sha256(bytes), digest);
  }
});

test('L1 explorer exposes only a verified synthetic L0 read model', async () => {
  const view = await loadResearchTowerL0({ repositoryRoot, witnessDir });
  assert.equal(view.status, 'candidate-local');
  assert.equal(view.authority_effect, 'none');
  assert.equal(view.sources.length, 7);
  assert.equal(view.residues[0].status, 'open');
  assert.equal(view.witness.validator_id, 'cal-l0-independent-validator-v1');
  assert.equal(view.relations.some((relation) => relation.kind === 'derived_from'), true);
  assert.match(view.claim_ceiling, /no representative, IDE, authority/i);
});

test('scene manifest preserves the synthetic evidence boundary and fails closed', async () => {
  const view = await loadResearchTowerL0({ repositoryRoot, witnessDir });
  const manifest = view.scene_manifest;
  assert.equal(manifest.interaction_contract, 'read-only');
  assert.deepEqual(manifest.towers[0].scenes.map((scene) => scene.level_id), [
    'evidence-l0-corpus',
    'evidence-l1-residue',
    'evidence-l2-closure'
  ]);
  assert.equal(manifest.system_layers.every((layer) => layer.semantic_axis === 'tower_system_architecture'), true);
  assert.equal(manifest.system_layers.every((layer) => layer.unavailable_reason), true);
  assert.equal(manifest.towers[0].scenes.every((scene) => scene.implementation_status === 'candidate-local'), true);
  assert.equal(manifest.towers[0].scenes.every((scene) => scene.claim_ceiling === view.claim_ceiling), true);
  assert.match(manifest.towers[0].scenes[2].unavailable_reason, /No representative source is selected/);
  assert.equal(manifest.system_layers.every((layer) => layer.source_refs[0].includes('#2-the-layer-stack-bottom-up-one-layer-at-a-time')), true);
  const missingSource = structuredClone(manifest);
  missingSource.towers[0].scenes[0].source_refs = [];
  assert.throws(() => validateTowerSceneManifest(missingSource, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const duplicateLevel = structuredClone(manifest);
  duplicateLevel.towers[0].scenes[1].level_id = 'evidence-l0-corpus';
  assert.throws(() => validateTowerSceneManifest(duplicateLevel, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const missingStatus = structuredClone(manifest);
  missingStatus.towers[0].scenes[0].implementation_status = '   ';
  assert.throws(() => validateTowerSceneManifest(missingStatus, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const mismatchedCeiling = structuredClone(manifest);
  mismatchedCeiling.towers[0].scenes[1].claim_ceiling = 'broader-than-view';
  assert.throws(() => validateTowerSceneManifest(mismatchedCeiling, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const missingBlocker = structuredClone(manifest);
  missingBlocker.towers[0].scenes[2].unavailable_reason = ' ';
  assert.throws(() => validateTowerSceneManifest(missingBlocker, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const malformedLocator = structuredClone(manifest);
  malformedLocator.system_layers[0].source_refs = ['research/tower-system-taxonomy/SYSTEM-VIEW.md#L1'];
  assert.throws(() => validateTowerSceneManifest(malformedLocator, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const exchangedSources = structuredClone(manifest);
  exchangedSources.towers[0].scenes[0].source_refs = [...manifest.towers[0].scenes[1].source_refs];
  assert.throws(() => validateTowerSceneManifest(exchangedSources, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const exchangedState = structuredClone(manifest);
  exchangedState.towers[0].scenes[0].evidence_state = 'open';
  assert.throws(() => validateTowerSceneManifest(exchangedState, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const blankGlobalCeiling = structuredClone(view);
  blankGlobalCeiling.claim_ceiling = '   ';
  assert.throws(() => validateTowerSceneManifest(manifest, blankGlobalCeiling), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const modifiedEvidenceReason = structuredClone(manifest);
  modifiedEvidenceReason.towers[0].scenes[2].unavailable_reason = 'A different but plausible blocker.';
  assert.throws(() => validateTowerSceneManifest(modifiedEvidenceReason, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const exchangedEvidenceReason = structuredClone(manifest);
  exchangedEvidenceReason.towers[0].scenes[0].unavailable_reason = manifest.towers[0].scenes[2].unavailable_reason;
  assert.throws(() => validateTowerSceneManifest(exchangedEvidenceReason, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const modifiedSystemLabel = structuredClone(manifest);
  modifiedSystemLabel.system_layers[0].label = 'System L1 · Something else';
  assert.throws(() => validateTowerSceneManifest(modifiedSystemLabel, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const exchangedSystemStatus = structuredClone(manifest);
  exchangedSystemStatus.system_layers[0].implementation_status = manifest.system_layers[1].implementation_status;
  assert.throws(() => validateTowerSceneManifest(exchangedSystemStatus, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const exchangedSystemReason = structuredClone(manifest);
  exchangedSystemReason.system_layers[0].unavailable_reason = manifest.system_layers[1].unavailable_reason;
  assert.throws(() => validateTowerSceneManifest(exchangedSystemReason, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const exchangedSystemSource = structuredClone(manifest);
  exchangedSystemSource.system_layers[0].source_refs = [manifest.towers[0].scenes[0].source_refs[0]];
  assert.throws(() => validateTowerSceneManifest(exchangedSystemSource, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const crossedAxis = structuredClone(manifest);
  crossedAxis.towers[0].scenes[0].level_id = 'system-l1-substrate';
  assert.throws(() => validateTowerSceneManifest(crossedAxis, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const reorderedAxes = structuredClone(manifest);
  reorderedAxes.semantic_axes.reverse();
  assert.throws(() => validateTowerSceneManifest(reorderedAxes, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  assert.throws(() => validateTowerSceneManifest(manifest, { ...view, authority_effect: 'execute' }), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
});

test('verification prompts preserve exact floor evidence, gaps, and a non-executable route', async () => {
  const view = await loadResearchTowerL0({ repositoryRoot, witnessDir });
  const projectionSet = view.verification_prompts;
  assert.equal(projectionSet.interaction_contract, 'display-only');
  assert.equal(projectionSet.authority_effect, 'none');
  assert.deepEqual(projectionSet.prompts.map((prompt) => prompt.selected_floor_id), [
    'evidence-l0-corpus',
    'evidence-l1-residue',
    'evidence-l2-closure'
  ]);
  assert.equal(new Set(projectionSet.prompts.map((prompt) => prompt.verification_question)).size, 3);
  assert.equal(projectionSet.prompts.every((prompt) => prompt.route_suggestion.executable === false), true);
  assert.equal(projectionSet.prompts.every((prompt) => prompt.bound_evidence_refs.every((reference) =>
    reference.status === 'verified' && reference.expected_sha256 === reference.observed_sha256)), true);
  assert.equal(projectionSet.prompts.every((prompt) => prompt.bound_evidence_refs.every((reference) =>
    reference.repository_ref === 'git:domainspec-core'
      && /^[a-f0-9]{40,64}$/u.test(reference.object_id)
      && reference.path.startsWith('projects/cyberalchemy-lab/research/tower-evidence-navigator/fixtures/source/'))), true);
  assert.equal(projectionSet.prompts.every((prompt) => prompt.known_evidence.length === 1 && prompt.unbound_evidence.length === 1), true);

  const executableRoute = structuredClone(projectionSet);
  executableRoute.prompts[0].route_suggestion.executable = true;
  assert.throws(() => validateVerificationPromptProjections(executableRoute, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const commandRoute = structuredClone(projectionSet);
  commandRoute.prompts[0].route_suggestion.command = 'run';
  assert.throws(() => validateVerificationPromptProjections(commandRoute, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const exchangedBinding = structuredClone(projectionSet);
  exchangedBinding.prompts[0].bound_evidence_refs[0] = structuredClone(projectionSet.prompts[1].bound_evidence_refs[0]);
  assert.throws(() => validateVerificationPromptProjections(exchangedBinding, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const digestMismatch = structuredClone(projectionSet);
  digestMismatch.prompts[0].bound_evidence_refs[0].observed_sha256 = '0'.repeat(64);
  assert.throws(() => validateVerificationPromptProjections(digestMismatch, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const exchangedQuestion = structuredClone(projectionSet);
  exchangedQuestion.prompts[0].verification_question = projectionSet.prompts[1].verification_question;
  assert.throws(() => validateVerificationPromptProjections(exchangedQuestion, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');

  for (const status of ['object_unavailable', 'path_missing', 'digest_mismatch']) {
    const failedView = structuredClone(view);
    const failedSource = failedView.sources.find((source) => source.id === 'source:toy:readme');
    failedSource.binding_status = status;
    failedSource.observed_sha256 = status === 'digest_mismatch' ? '0'.repeat(64) : null;
    failedView.verification_prompts = buildVerificationPromptProjections(failedView, failedView.scene_manifest);
    const failedPrompt = failedView.verification_prompts.prompts[0];
    assert.equal(failedPrompt.bound_evidence_refs[0].status, status);
    assert.equal(failedPrompt.known_evidence.every((evidence) => !evidence.bound_ref_ids.includes(failedSource.id)), true);
    assert.equal(failedPrompt.known_evidence.every((evidence) => evidence.statement.includes('no combined floor claim is presented')), true);
    assert.equal(failedPrompt.unbound_evidence.some((gap) => gap.statement.includes(status)
      && gap.statement.includes(failedSource.repository_ref)
      && gap.statement.includes(failedSource.object_id)
      && gap.statement.includes(failedSource.path)
      && gap.statement.includes('Ordinary sourced claim suppressed')), true);
    assert.doesNotThrow(() => validateVerificationPromptProjections(failedView.verification_prompts, failedView));
    const leakedClaim = structuredClone(failedView.verification_prompts);
    leakedClaim.prompts[0].known_evidence = structuredClone(projectionSet.prompts[0].known_evidence);
    assert.throws(() => validateVerificationPromptProjections(leakedClaim, failedView), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  }
});

test('exact Git source resolver emits each fail-closed binding state without repairing bytes', async () => {
  const view = await loadResearchTowerL0({ repositoryRoot, witnessDir });
  const sourceInputs = view.sources.map((source) => ({
    id: source.id,
    record_snapshot_id: source.record_snapshot_id,
    logical_source_id: source.logical_source_id,
    locator: source.locator,
    content_digest: source.content_digest,
    byte_size: source.byte_size,
    media_type: source.media_type,
    status: source.status,
    provenance: source.provenance
  }));
  const objectUnavailable = await resolveFixtureSourceBindings({
    repositoryRoot, sourceRoot, sources: sourceInputs, readGitObject: async () => null
  });
  assert.equal(objectUnavailable.every((source) => source.binding_status === 'object_unavailable' && source.observed_sha256 === null), true);
  const pathMissing = await resolveFixtureSourceBindings({
    repositoryRoot, sourceRoot, sources: sourceInputs, readSource: async () => { throw new Error('missing'); }
  });
  assert.equal(pathMissing.every((source) => source.binding_status === 'path_missing' && source.observed_sha256 === null), true);
  const gitPathMissing = await resolveFixtureSourceBindings({
    repositoryRoot, sourceRoot, sources: sourceInputs, resolveGitPath: async () => null
  });
  assert.equal(gitPathMissing.every((source) => source.binding_status === 'path_missing' && source.observed_sha256 === null), true);
  const digestMismatch = await resolveFixtureSourceBindings({
    repositoryRoot,
    sourceRoot,
    sources: sourceInputs,
    readSource: async (target) => Buffer.concat([await readFile(target), Buffer.from('changed')])
  });
  assert.equal(digestMismatch.every((source) => source.binding_status === 'digest_mismatch'
    && /^[a-f0-9]{64}$/u.test(source.observed_sha256)
    && source.observed_sha256 !== source.expected_sha256), true);
  for (const source of [...objectUnavailable, ...pathMissing, ...gitPathMissing, ...digestMismatch]) {
    assert.equal(source.repository_ref, 'git:domainspec-core');
    assert.match(source.object_id, /^[a-f0-9]{40,64}$/u);
    assert.equal(source.path.startsWith('projects/cyberalchemy-lab/research/tower-evidence-navigator/fixtures/source/'), true);
  }
});

test('L1 explorer fails closed when its lock is tampered', async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), 'research-tower-lock-'));
  try {
    const invalidLock = path.join(directory, 'INPUT-LOCK.json');
    await writeFile(invalidLock, JSON.stringify({ authority_effect: 'none', fixture_class: 'synthetic-contract-fixture', inputs: {} }));
    await assert.rejects(() => loadResearchTowerL0({ repositoryRoot, witnessDir, inputLockPath: invalidLock }), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_lock_invalid');
  } finally { await rm(directory, { recursive: true, force: true }); }
});

test('local server serves the explorer and its read-only API', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'research-tower-server-'));
  const server = createServer({ rootDir: projectRoot, stateDir });
  await server.ready;
  const port = await listen(server);
  try {
    const [page, api] = await Promise.all([fetch(`http://127.0.0.1:${port}/demo/research-tower`), fetch(`http://127.0.0.1:${port}/api/research-tower/l0`)]);
    assert.equal(page.status, 200);
    const html = await page.text();
    assert.match(html, /data-workbench="tower-scene-canvas"/);
    assert.match(html, /data-legacy-workbench="research-tower-explorer"/);
    assert.match(html, /data-layout="cutaway-tower"/);
    assert.match(html, /data-stage="tower-world"/);
    assert.match(html, /data-object="research-tower"/);
    assert.match(html, /data-panel="tower-elevation"/);
    assert.match(html, /data-panel="tower-spine"/);
    assert.match(html, /data-action="toggle-floor-room"/);
    assert.match(html, /id="floor-room" class="floor-room" data-panel="floor-room"/);
    assert.match(html, /aria-controls="floor-room"/);
    assert.match(html, /data-panel="system-atlas"/);
    assert.match(html, /data-panel="system-refusal"/);
    assert.match(html, /Synthetic evidence tower/);
    assert.match(html, /Preloaded contract fixture · not representative · read-only navigation/);
    assert.match(html, /Tower System reference — capabilities unavailable in this Lab/);
    assert.match(html, /data-list="sources"/);
    assert.match(html, /data-field="relation-filter"/);
    assert.match(html, /prefers-reduced-motion/);
    assert.match(html, /animation: none !important/);
    assert.match(html, /data-action="reset-orientation"/);
    assert.match(html, /data-list="levels"/);
    assert.match(html, /data-panel="scene-status"/);
    assert.match(html, /data-panel="scene-unavailable"/);
    assert.match(html, /aria-live="polite" aria-atomic="true"/);
    assert.equal((html.match(/aria-live=/g) || []).length, 1);
    assert.equal((html.match(/data-object="research-tower"/g) || []).length, 1);
    assert.equal((html.match(/data-panel="floor-room"/g) || []).length, 1);
    assert.doesNotMatch(html, /overflow-x:\s*clip/);
    assert.doesNotMatch(html, /data-panel="evidence-detail"/);
    assert.doesNotMatch(html, /data-layout="spatial-canvas"/);
    assert.doesNotMatch(html, /\.scene-stack|\.source-orbit|\.cowork-robots|\.live-lab|#constellation-core/);
    assert.match(html, /data-panel="room-scene"/);
    assert.match(html, /data-media="room-still"/);
    assert.match(html, /data-media="ambient-tableau"/);
    assert.match(html, /robot-paper-library\.png/);
    assert.match(html, /robot-cowork-rpg-sprite-sheet\.png/);
    assert.match(html, /autonomous-observatory-lab\.png/);
    assert.match(html, /night-knowledge-observatory\.png/);
    assert.match(html, /Illustrative room scene · no live workers or workflow/);
    assert.match(html, /data-panel="verification-prompt"/);
    assert.match(html, /data-verification-field="executable">false/);
    assert.match(html, /data-action="return-to-floor"/);
    assert.match(html, /Injected render failure after staging/);
    assert.match(html, /data-frame-count="4" data-frame-width="543" data-frame-height="724" data-source-width="2172"/);
    assert.match(html, /04fa18bb405b59380b4be2b5a88bebd88632837e1fd21467e626832f43e37afa/);
    assert.match(html, /animation: ambient-lab-loop 10s steps\(1, end\) infinite/);
    assert.doesNotMatch(html, /data-robot-role|toggle-lab-motion|focus-tower|lab-frame-loop/);
    assert.doesNotMatch(html, /https?:\/\/[^'"\s]+\.(?:png|gif|webp)|anime(?:\.min)?\.js|requestAnimationFrame/);
    assert.doesNotMatch(html, /tabindex=["'][1-9]|aria-modal=|role=["']dialog/);
    assert.doesNotMatch(html, /innerHTML/);
    assert.equal(api.status, 200);
    const payload = await api.json();
    assert.equal(payload.witness.witness_id, 'l0-synthetic-001');
    assert.equal(payload.scene_manifest.interaction_contract, 'read-only');
    assert.equal(payload.scene_manifest.towers[0].scenes.length, 3);
    assert.equal(payload.scene_manifest.towers[0].scenes[0].source_refs.length > 0, true);
    assert.equal(payload.verification_prompts.interaction_contract, 'display-only');
    assert.equal(payload.verification_prompts.prompts.length, 3);
    assert.equal(payload.verification_prompts.prompts.every((prompt) => prompt.route_suggestion.executable === false), true);
  } finally { await close(server); await rm(stateDir, { recursive: true, force: true }); }
});
