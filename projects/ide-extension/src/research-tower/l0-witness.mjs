import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';

const REQUIRED_LOCKS = ['fixture', 'package_snapshot', 'relation_registry', 'privacy_policy', 'projection_contract'];

export class ResearchTowerWitnessError extends Error {
  constructor(code, message) {
    super(message);
    this.name = 'ResearchTowerWitnessError';
    this.code = code;
  }
}

export const sha256 = (value) => createHash('sha256').update(value).digest('hex');

function fail(code, message) {
  throw new ResearchTowerWitnessError(code, message);
}

function lockedPath(repositoryRoot, reference) {
  if (!reference || typeof reference.path !== 'string' || !/^[a-f0-9]{64}$/u.test(reference.sha256 || '')) {
    fail('research_tower_lock_invalid', 'input lock contains an invalid path or digest');
  }
  const resolved = path.resolve(repositoryRoot, reference.path);
  const relative = path.relative(repositoryRoot, resolved);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    fail('research_tower_lock_invalid', `input path escapes the repository: ${reference.path}`);
  }
  return resolved;
}

async function readLockedInput(repositoryRoot, name, reference) {
  const target = lockedPath(repositoryRoot, reference);
  const bytes = await readFile(target);
  if (sha256(bytes) !== reference.sha256) {
    fail('research_tower_witness_stale', `${name} does not match its locked digest`);
  }
  try {
    return JSON.parse(bytes.toString('utf8'));
  } catch {
    fail('research_tower_witness_invalid', `${name} is not valid JSON`);
  }
}

function selectSource(source) {
  return {
    id: source.id,
    logical_source_id: source.logical_source_id,
    locator: source.locator,
    content_digest: source.content_digest,
    byte_size: source.byte_size,
    media_type: source.media_type,
    status: source.status
  };
}

function selectRecord(record) {
  const keys = ['kind', 'id', 'status', 'privacy_class', 'fixture_class', 'proposition', 'scope', 'claim_ceiling', 'review_state', 'gate_result', 'role', 'logical_source_id', 'byte_size', 'media_type', 'evidence_ceiling'];
  return Object.fromEntries(keys.filter((key) => Object.hasOwn(record, key)).map((key) => [key, record[key]]));
}

const EVIDENCE_SCENE_IDS = new Set([
  'evidence-l0-corpus',
  'evidence-l1-residue',
  'evidence-l2-closure'
]);
const EVIDENCE_SCENE_CONTRACTS = new Map([
  ['evidence-l0-corpus', { evidence_state: 'locked-synthetic', implementation_status: 'candidate-local', source_refs: ['source:toy:readme', 'source:toy:tower', 'source:toy:l0'], unavailable_reason: null }],
  ['evidence-l1-residue', { evidence_state: 'open', implementation_status: 'candidate-local', source_refs: ['source:toy:l1', 'source:toy:residue'], unavailable_reason: null }],
  ['evidence-l2-closure', { evidence_state: 'blocked', implementation_status: 'candidate-local', source_refs: ['source:toy:l2', 'source:toy:gates'], unavailable_reason: 'No representative source is selected; this view cannot select one or run a workflow.' }]
]);
const SYSTEM_LAYER_IDS = new Set([
  'system-l1-substrate',
  'system-l2-construction',
  'system-l3-application',
  'system-lphi-policy',
  'system-l4-adjudication'
]);
const SEMANTIC_AXES = ['evidence_progression', 'tower_system_architecture'];
const SYSTEM_VIEW_ANCHOR = 'research/tower-system-taxonomy/SYSTEM-VIEW.md#2-the-layer-stack-bottom-up-one-layer-at-a-time';
const SYSTEM_LAYER_CONTRACTS = new Map([
  ['system-l1-substrate', { label: 'System L1 · Substrate', implementation_status: 'unproven-in-lab', source_refs: [SYSTEM_VIEW_ANCHOR], unavailable_reason: 'A runtime-queryable graph and persona artifacts are not available in this Lab witness.' }],
  ['system-l2-construction', { label: 'System L2 · Construction', implementation_status: 'prior-work-not-live-here', source_refs: [SYSTEM_VIEW_ANCHOR], unavailable_reason: 'Construction methods are not active builders in this canvas.' }],
  ['system-l3-application', { label: 'System L3 · Application', implementation_status: 'unavailable-in-lab', source_refs: [SYSTEM_VIEW_ANCHOR], unavailable_reason: 'No debate, dispatch, or persona operation runs in this canvas.' }],
  ['system-lphi-policy', { label: 'System Lφ · Decision policy', implementation_status: 'design-stage-unproven', source_refs: [SYSTEM_VIEW_ANCHOR], unavailable_reason: 'MOGT has no live Lab run and cannot make choices here.' }],
  ['system-l4-adjudication', { label: 'System L4 · Adjudication', implementation_status: 'governance-only', source_refs: [SYSTEM_VIEW_ANCHOR], unavailable_reason: 'This canvas cannot score, select a winner, or emit a verdict.' }]
]);

function sceneFailure(message) {
  fail('research_tower_scene_manifest_invalid', message);
}

function nonEmptyString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

function equalStringArray(actual, expected) {
  return Array.isArray(actual)
    && actual.length === expected.length
    && expected.every((value, index) => actual[index] === value);
}

function assertSceneDescriptor(scene, sourceIds, claimCeiling) {
  const contract = scene && EVIDENCE_SCENE_CONTRACTS.get(scene.level_id);
  if (!scene || scene.semantic_axis !== 'evidence_progression'
    || !EVIDENCE_SCENE_IDS.has(scene.level_id)
    || !nonEmptyString(scene.scene_kind) || !nonEmptyString(scene.evidence_state)
    || !nonEmptyString(scene.implementation_status)
    || scene.claim_ceiling !== claimCeiling
    || !Array.isArray(scene.source_refs) || scene.source_refs.length === 0
    || !Object.hasOwn(scene, 'unavailable_reason')) {
    sceneFailure('evidence scene is missing a required bound field');
  }
  if (!contract || scene.evidence_state !== contract.evidence_state
    || scene.implementation_status !== contract.implementation_status
    || !equalStringArray(scene.source_refs, contract.source_refs)
    || scene.unavailable_reason !== contract.unavailable_reason) {
    sceneFailure(`evidence scene ${scene.level_id} does not match its closed binding`);
  }
  if (scene.source_refs.some((sourceId) => !sourceIds.has(sourceId))) {
    sceneFailure(`evidence scene ${scene.level_id} references an unbound source`);
  }
  if (scene.level_id === 'L1' || /^L\d+$/u.test(scene.level_id)) {
    sceneFailure('bare numeric level identifiers are forbidden');
  }
  if (['blocked', 'unavailable'].includes(scene.evidence_state)
    && !nonEmptyString(scene.unavailable_reason)) {
    sceneFailure(`evidence scene ${scene.level_id} requires a blocker reason`);
  }
}

function assertSystemDescriptor(layer) {
  const contract = layer && SYSTEM_LAYER_CONTRACTS.get(layer.level_id);
  if (!layer || layer.semantic_axis !== 'tower_system_architecture'
    || !SYSTEM_LAYER_IDS.has(layer.level_id)
    || !nonEmptyString(layer.label) || !nonEmptyString(layer.implementation_status)
    || !nonEmptyString(layer.unavailable_reason)
    || !Array.isArray(layer.source_refs) || layer.source_refs.length === 0) {
    sceneFailure('Tower System descriptor is missing a required boundary field');
  }
  if (!contract || layer.label !== contract.label
    || layer.implementation_status !== contract.implementation_status
    || layer.unavailable_reason !== contract.unavailable_reason
    || !equalStringArray(layer.source_refs, contract.source_refs)) {
    sceneFailure(`Tower System descriptor ${layer.level_id} does not match its closed binding`);
  }
  if (layer.level_id === 'L1' || /^L\d+$/u.test(layer.level_id)) {
    sceneFailure('bare numeric system layer identifiers are forbidden');
  }
}

export function validateTowerSceneManifest(manifest, view) {
  if (!view || view.authority_effect !== 'none' || view.status !== 'candidate-local'
    || !Array.isArray(view.sources) || !Array.isArray(view.residues)
    || !nonEmptyString(view.claim_ceiling)
    || !manifest || manifest.schema_version !== 'cal.tower-scene-manifest.v1'
    || manifest.interaction_contract !== 'read-only'
    || !Array.isArray(manifest.semantic_axes)
    || manifest.semantic_axes.length !== SEMANTIC_AXES.length
    || !SEMANTIC_AXES.every((axis, index) => manifest.semantic_axes[index] === axis)
    || !Array.isArray(manifest.towers) || manifest.towers.length !== 1
    || !Array.isArray(manifest.system_layers)) {
    sceneFailure('only the verified candidate-local L0 read model can build scenes');
  }
  const sourceIds = new Set(view.sources.map((source) => source.id));
  const residue = view.residues.find((item) => item.id === 'residue:representative-selection');
  if (!residue) sceneFailure('the synthetic selection residue is required');
  const tower = manifest.towers[0];
  if (tower.tower_id !== 'tower:toy' || tower.availability !== 'available'
    || tower.claim_ceiling !== view.claim_ceiling || !Array.isArray(tower.scenes)
    || tower.scenes.length !== EVIDENCE_SCENE_IDS.size) {
    sceneFailure('the manifest must contain exactly one available synthetic tower');
  }
  const seenSceneIds = new Set();
  tower.scenes.forEach((scene) => {
    assertSceneDescriptor(scene, sourceIds, tower.claim_ceiling);
    if (seenSceneIds.has(scene.level_id)) sceneFailure('evidence scene identifiers must be unique');
    seenSceneIds.add(scene.level_id);
  });
  if (seenSceneIds.size !== EVIDENCE_SCENE_IDS.size) {
    sceneFailure('the manifest must include the complete evidence-scene set');
  }
  const seenSystemIds = new Set();
  manifest.system_layers.forEach((layer) => {
    assertSystemDescriptor(layer);
    if (seenSystemIds.has(layer.level_id)) sceneFailure('Tower System identifiers must be unique');
    seenSystemIds.add(layer.level_id);
  });
  if (seenSystemIds.size !== SYSTEM_LAYER_IDS.size) {
    sceneFailure('the manifest must include the complete Tower System map');
  }
  return manifest;
}

export function buildTowerSceneManifest(view) {
  if (!view || view.authority_effect !== 'none' || view.status !== 'candidate-local'
    || !Array.isArray(view.sources) || !Array.isArray(view.residues)) {
    sceneFailure('only the verified candidate-local L0 read model can build scenes');
  }
  const residue = view.residues.find((item) => item.id === 'residue:representative-selection');
  if (!residue) sceneFailure('the synthetic selection residue is required');

  const scenes = [
    {
      tower_id: 'tower:toy',
      level_id: 'evidence-l0-corpus',
      semantic_axis: 'evidence_progression',
      scene_kind: 'corpus-observatory',
      evidence_state: 'locked-synthetic',
      implementation_status: 'candidate-local',
      source_refs: ['source:toy:readme', 'source:toy:tower', 'source:toy:l0'],
      claim_ceiling: view.claim_ceiling,
      content: 'Locked synthetic source anchors, locators, digests, and byte sizes.',
      unavailable_reason: null
    },
    {
      tower_id: 'tower:toy',
      level_id: 'evidence-l1-residue',
      semantic_axis: 'evidence_progression',
      scene_kind: 'residue-conservatory',
      evidence_state: residue.status,
      implementation_status: 'candidate-local',
      source_refs: ['source:toy:l1', 'source:toy:residue'],
      claim_ceiling: view.claim_ceiling,
      content: residue.question,
      unavailable_reason: null
    },
    {
      tower_id: 'tower:toy',
      level_id: 'evidence-l2-closure',
      semantic_axis: 'evidence_progression',
      scene_kind: 'closure-workshop',
      evidence_state: 'blocked',
      implementation_status: 'candidate-local',
      source_refs: ['source:toy:l2', 'source:toy:gates'],
      claim_ceiling: view.claim_ceiling,
      content: 'A future external L1 owner may consider real-source selection; this view cannot select a source or run a workflow.',
      unavailable_reason: 'No representative source is selected; this view cannot select one or run a workflow.'
    }
  ];
  const system_layers = [
    { level_id: 'system-l1-substrate', label: 'System L1 · Substrate', implementation_status: 'unproven-in-lab', source_refs: [SYSTEM_VIEW_ANCHOR], unavailable_reason: 'A runtime-queryable graph and persona artifacts are not available in this Lab witness.' },
    { level_id: 'system-l2-construction', label: 'System L2 · Construction', implementation_status: 'prior-work-not-live-here', source_refs: [SYSTEM_VIEW_ANCHOR], unavailable_reason: 'Construction methods are not active builders in this canvas.' },
    { level_id: 'system-l3-application', label: 'System L3 · Application', implementation_status: 'unavailable-in-lab', source_refs: [SYSTEM_VIEW_ANCHOR], unavailable_reason: 'No debate, dispatch, or persona operation runs in this canvas.' },
    { level_id: 'system-lphi-policy', label: 'System Lφ · Decision policy', implementation_status: 'design-stage-unproven', source_refs: [SYSTEM_VIEW_ANCHOR], unavailable_reason: 'MOGT has no live Lab run and cannot make choices here.' },
    { level_id: 'system-l4-adjudication', label: 'System L4 · Adjudication', implementation_status: 'governance-only', source_refs: [SYSTEM_VIEW_ANCHOR], unavailable_reason: 'This canvas cannot score, select a winner, or emit a verdict.' }
  ].map((layer) => ({ ...layer, semantic_axis: 'tower_system_architecture' }));
  return validateTowerSceneManifest({
    schema_version: 'cal.tower-scene-manifest.v1',
    interaction_contract: 'read-only',
    semantic_axes: SEMANTIC_AXES,
    towers: [{
      tower_id: 'tower:toy',
      title: 'Synthetic Research Tower',
      availability: 'available',
      claim_ceiling: view.claim_ceiling,
      scenes
    }],
    system_layers
  }, view);
}

export async function loadResearchTowerL0(options = {}) {
  const repositoryRoot = options.repositoryRoot;
  const witnessDir = options.witnessDir;
  const inputLockPath = options.inputLockPath || path.join(witnessDir, 'INPUT-LOCK.json');
  if (!repositoryRoot || !witnessDir) throw new TypeError('repositoryRoot and witnessDir are required');

  let lock;
  try {
    lock = JSON.parse(await readFile(inputLockPath, 'utf8'));
  } catch {
    fail('research_tower_witness_invalid', 'INPUT-LOCK.json is unavailable or invalid');
  }
  if (lock.authority_effect !== 'none' || lock.fixture_class !== 'synthetic-contract-fixture' || !lock.inputs) {
    fail('research_tower_witness_invalid', 'only the synthetic, non-authorizing L0 witness is accepted');
  }
  if (!REQUIRED_LOCKS.every((name) => Object.hasOwn(lock.inputs, name))) {
    fail('research_tower_lock_invalid', 'INPUT-LOCK.json does not bind the complete L0 input set');
  }

  const locked = Object.fromEntries(await Promise.all(REQUIRED_LOCKS.map(async (name) => [name, await readLockedInput(repositoryRoot, name, lock.inputs[name])] )));
  const [projectionBytes, validationBytes] = await Promise.all([
    readFile(path.join(witnessDir, 'projection.json')),
    readFile(path.join(witnessDir, 'validation-records.json'))
  ]);
  let projection;
  let validation;
  try {
    projection = JSON.parse(projectionBytes.toString('utf8'));
    validation = JSON.parse(validationBytes.toString('utf8'));
  } catch {
    fail('research_tower_witness_invalid', 'witness projection or validation records are invalid JSON');
  }
  const validationRecord = validation.records?.find((record) => record.status === 'pass' && record.result === 'pass');
  if (!validationRecord || validationRecord.validator_id === projection.generator_contract_id) {
    fail('research_tower_witness_invalid', 'witness requires an independent passing validation record');
  }
  if (validationRecord.exact_inputs?.projection_sha256 !== sha256(projectionBytes)
    || validationRecord.exact_inputs?.input_lock_sha256 !== sha256(await readFile(inputLockPath))) {
    fail('research_tower_witness_stale', 'validation record does not bind the current witness bytes');
  }
  if (projection.authority_effect !== 'none' || projection.invalid || projection.stale) {
    fail('research_tower_witness_invalid', 'projection must remain static, valid, fresh, and non-authorizing');
  }
  if (locked.fixture.fixture_class !== 'synthetic-contract-fixture' || locked.fixture.authority_effect !== 'none') {
    fail('research_tower_witness_invalid', 'fixture does not preserve the L0 candidate ceiling');
  }

  const view = {
    schema_version: '1.0.0',
    explorer_id: 'cal-l1-research-tower-explorer',
    authority_effect: 'none',
    status: 'candidate-local',
    claim_ceiling: lock.claim_ceiling,
    witness: {
      witness_id: lock.witness_id,
      fixture_class: lock.fixture_class,
      projection_sha256: sha256(projectionBytes),
      validation_record_id: validationRecord.id,
      validator_id: validationRecord.validator_id
    },
    projection: {
      projection_revision: projection.projection_revision,
      tower_snapshot_id: projection.tower_snapshot_id,
      record_count: projection.records.length,
      relation_count: projection.relations.length,
      privacy_policy_id: projection.privacy?.policy_id
    },
    sources: locked.fixture.source_snapshots.map(selectSource),
    records: projection.records.map(selectRecord),
    relations: projection.relations.map(({ kind, relation_id, from_id, to_id, direction }) => ({ kind, relation_id, from_id, to_id, direction })),
    residues: locked.fixture.residue_items.map(({ id, status, question, scope, blocked_claim_ids, blocked_gate_ids }) => ({ id, status, question, scope, blocked_claim_ids, blocked_gate_ids })),
    candidates: locked.fixture.ontology_candidates.map(({ id, status, proposed_meaning, scope, evidence_ceiling, contradiction_path }) => ({ id, status, proposed_meaning, scope, evidence_ceiling, contradiction_path })),
    locked_inputs: REQUIRED_LOCKS.map((name) => ({ name, path: lock.inputs[name].path, sha256: lock.inputs[name].sha256 }))
  };
  return { ...view, scene_manifest: buildTowerSceneManifest(view) };
}
