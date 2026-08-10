import assert from 'node:assert/strict';
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';
import { createServer } from '../src/server.mjs';
import {
  loadResearchTowerL0,
  ResearchTowerWitnessError,
  validateTowerSceneManifest
} from '../src/research-tower/l0-witness.mjs';

const repositoryRoot = path.resolve(fileURLToPath(new URL('../../..', import.meta.url)));
const projectRoot = path.join(repositoryRoot, 'projects/ide-extension');
const witnessDir = path.join(repositoryRoot, 'projects/cyberalchemy-lab/development/witness-runs/l0-synthetic-001');

function listen(server) { return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server.address().port))); }
function close(server) { return new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve())); }

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
    assert.doesNotMatch(html, /robot-paper-library\.png|robot-cowork-rpg-sprite-sheet\.png|autonomous-observatory-lab\.png|night-knowledge-observatory\.png/);
    assert.doesNotMatch(html, /data-robot-role|toggle-lab-motion|focus-tower|lab-frame-loop|Decorative cowork loop/);
    assert.doesNotMatch(html, /innerHTML/);
    assert.equal(api.status, 200);
    const payload = await api.json();
    assert.equal(payload.witness.witness_id, 'l0-synthetic-001');
    assert.equal(payload.scene_manifest.interaction_contract, 'read-only');
    assert.equal(payload.scene_manifest.towers[0].scenes.length, 3);
    assert.equal(payload.scene_manifest.towers[0].scenes[0].source_refs.length > 0, true);
  } finally { await close(server); await rm(stateDir, { recursive: true, force: true }); }
});
