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
  const missingSource = structuredClone(manifest);
  missingSource.towers[0].scenes[0].source_refs = [];
  assert.throws(() => validateTowerSceneManifest(missingSource, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
  const duplicateLevel = structuredClone(manifest);
  duplicateLevel.towers[0].scenes[1].level_id = 'evidence-l0-corpus';
  assert.throws(() => validateTowerSceneManifest(duplicateLevel, view), (error) => error instanceof ResearchTowerWitnessError && error.code === 'research_tower_scene_manifest_invalid');
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
    assert.match(html, /data-layout="spatial-canvas"/);
    assert.match(html, /data-list="sources"/);
    assert.match(html, /data-field="relation-filter"/);
    assert.match(html, /prefers-reduced-motion/);
    assert.match(html, /robot-paper-library\.png/);
    assert.match(html, /robot-cowork-rpg-sprite-sheet\.png/);
    assert.match(html, /cyberalchemy-mark\.svg/);
    assert.match(html, /data-robot-role="source-scout"/);
    assert.match(html, /data-action="toggle-lab-motion"/);
    assert.match(html, /data-action="focus-tower"/);
    assert.match(html, /data-action="reset-orientation"/);
    assert.match(html, /data-list="towers"/);
    assert.match(html, /data-list="levels"/);
    assert.match(html, /data-panel="scene-status"/);
    assert.match(html, /data-panel="scene-unavailable"/);
    assert.match(html, /lab-frame-loop/);
    assert.doesNotMatch(html, /innerHTML/);
    const asset = await fetch(`http://127.0.0.1:${port}/assets/research-tower-concepts/robot-paper-library.png`);
    assert.equal(asset.status, 200);
    assert.match(asset.headers.get('content-type'), /^image\/png/);
    const [sprite, mark] = await Promise.all([
      fetch(`http://127.0.0.1:${port}/assets/research-tower-concepts/robot-cowork-rpg-sprite-sheet.png`),
      fetch(`http://127.0.0.1:${port}/assets/research-tower-concepts/cyberalchemy-mark.svg`)
    ]);
    assert.equal(sprite.status, 200);
    assert.match(sprite.headers.get('content-type'), /^image\/png/);
    assert.equal(mark.status, 200);
    assert.match(mark.headers.get('content-type'), /^image\/svg\+xml/);
    assert.equal(api.status, 200);
    const payload = await api.json();
    assert.equal(payload.witness.witness_id, 'l0-synthetic-001');
    assert.equal(payload.scene_manifest.interaction_contract, 'read-only');
    assert.equal(payload.scene_manifest.towers[0].scenes.length, 3);
    assert.equal(payload.scene_manifest.towers[0].scenes[0].source_refs.length > 0, true);
  } finally { await close(server); await rm(stateDir, { recursive: true, force: true }); }
});
