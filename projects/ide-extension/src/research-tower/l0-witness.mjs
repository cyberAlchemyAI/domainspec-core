import { createHash } from 'node:crypto';
import { execFile } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { promisify } from 'node:util';

const REQUIRED_LOCKS = ['fixture', 'package_snapshot', 'relation_registry', 'privacy_policy', 'projection_contract'];
const execFileAsync = promisify(execFile);
const SOURCE_OBJECT_CONTRACTS = new Map([
  ['source:toy:readme', { object_id: '1a3b5747554b232020def052a779b1b06713d27a', path: 'projects/cyberalchemy-lab/research/tower-evidence-navigator/fixtures/source/toy-tower/README.md' }],
  ['source:toy:tower', { object_id: '337b892f2e7835ce2622b365e49af3a2484a30a6', path: 'projects/cyberalchemy-lab/research/tower-evidence-navigator/fixtures/source/toy-tower/TOWER.md' }],
  ['source:toy:l0', { object_id: 'f8445df4d35afe5667d68370024aa193a477b2d3', path: 'projects/cyberalchemy-lab/research/tower-evidence-navigator/fixtures/source/toy-tower/levels/L0-corpus.md' }],
  ['source:toy:l1', { object_id: '136aee7deb405fe9998a5e70602bd61690a20fa0', path: 'projects/cyberalchemy-lab/research/tower-evidence-navigator/fixtures/source/toy-tower/levels/L1-residue-map.md' }],
  ['source:toy:l2', { object_id: '7bb3224e3dcde5038de17bbd6fb3cf735cc00635', path: 'projects/cyberalchemy-lab/research/tower-evidence-navigator/fixtures/source/toy-tower/levels/L2-closure-plan.md' }],
  ['source:toy:gates', { object_id: '500118da1d50d13cbbbd356b62f1db495a5f85f9', path: 'projects/cyberalchemy-lab/research/tower-evidence-navigator/fixtures/source/toy-tower/gates/closure-gates.md' }],
  ['source:toy:residue', { object_id: '0e0134ac348e71564a0876289850f995e7eabb0d', path: 'projects/cyberalchemy-lab/research/tower-evidence-navigator/fixtures/source/toy-tower/residue/open-residue.md' }]
]);

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

function selectSource(source, binding) {
  return {
    id: source.id,
    record_snapshot_id: source.record_snapshot_id,
    logical_source_id: source.logical_source_id,
    locator: source.locator,
    content_digest: source.content_digest,
    expected_sha256: source.content_digest,
    repository_ref: binding.repository_ref,
    object_id: binding.object_id,
    path: binding.path,
    observed_sha256: binding.observed_sha256,
    binding_status: binding.status,
    byte_size: source.byte_size,
    media_type: source.media_type,
    status: source.status,
    provenance: source.provenance
  };
}

function containedSourcePath(sourceRoot, locator) {
  if (!nonEmptyString(locator)) {
    fail('research_tower_source_binding_invalid', 'source binding locator is missing');
  }
  const resolved = path.resolve(sourceRoot, locator);
  const relative = path.relative(sourceRoot, resolved);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    fail('research_tower_source_binding_invalid', `source binding escapes its fixture root: ${locator}`);
  }
  return resolved;
}

async function gitBytesOrNull(repositoryRoot, args) {
  try {
    const { stdout } = await execFileAsync('git', ['-C', repositoryRoot, ...args], { encoding: null, maxBuffer: 4 * 1024 * 1024 });
    return stdout;
  } catch {
    return null;
  }
}

export async function resolveFixtureSourceBindings({ repositoryRoot, sourceRoot, sources, readSource = readFile, readGitObject, resolveGitPath } = {}) {
  if (!Array.isArray(sources) || sources.length === 0) {
    fail('research_tower_source_binding_invalid', 'fixture source bindings are unavailable');
  }
  if (!repositoryRoot || !sourceRoot || SOURCE_OBJECT_CONTRACTS.size !== sources.length) {
    fail('research_tower_source_binding_invalid', 'source bindings require the complete exact repository contract');
  }
  const gitRootBytes = await gitBytesOrNull(repositoryRoot, ['rev-parse', '--show-toplevel']);
  const gitRoot = gitRootBytes?.toString('utf8').trim();
  if (!gitRoot || path.resolve(gitRoot) !== path.resolve(repositoryRoot)) {
    fail('research_tower_source_binding_invalid', 'repository identity does not match the declared repository root');
  }
  const repositoryRef = `git:${path.basename(gitRoot)}`;
  const objectReader = readGitObject || (async (objectId) => gitBytesOrNull(repositoryRoot, ['cat-file', 'blob', objectId]));
  const pathResolver = resolveGitPath || (async (repositoryPath) => {
    const result = await gitBytesOrNull(repositoryRoot, ['rev-parse', `HEAD:${repositoryPath}`]);
    return result?.toString('utf8').trim() || null;
  });
  return Promise.all(sources.map(async (source) => {
    const contract = SOURCE_OBJECT_CONTRACTS.get(source.id);
    if (!contract || !/^[a-f0-9]{64}$/u.test(source.content_digest || '') || !Number.isInteger(source.byte_size)) {
      fail('research_tower_source_binding_invalid', `source binding ${source.id || 'unknown'} is malformed`);
    }
    const target = containedSourcePath(sourceRoot, source.locator);
    const repositoryPath = path.relative(repositoryRoot, target).split(path.sep).join('/');
    if (repositoryPath.startsWith('../') || path.isAbsolute(repositoryPath) || repositoryPath !== contract.path) {
      fail('research_tower_source_binding_invalid', `source binding ${source.id} does not match its exact repository path`);
    }
    const base = { repository_ref: repositoryRef, object_id: contract.object_id, path: contract.path };
    const objectBytes = await objectReader(contract.object_id, contract.path);
    if (!objectBytes) {
      return selectSource(source, { ...base, observed_sha256: null, status: 'object_unavailable' });
    }
    const resolvedObjectId = await pathResolver(contract.path);
    if (!resolvedObjectId) {
      return selectSource(source, { ...base, observed_sha256: null, status: 'path_missing' });
    }
    let pathBytes;
    try {
      pathBytes = await readSource(target);
    } catch {
      return selectSource(source, { ...base, observed_sha256: null, status: 'path_missing' });
    }
    if (resolvedObjectId !== contract.object_id) {
      return selectSource(source, { ...base, observed_sha256: sha256(pathBytes), status: 'digest_mismatch' });
    }
    const objectSha256 = sha256(objectBytes);
    const pathSha256 = sha256(pathBytes);
    if (objectSha256 !== source.content_digest || pathSha256 !== source.content_digest
      || pathBytes.length !== source.byte_size || objectBytes.length !== source.byte_size) {
      return selectSource(source, { ...base, observed_sha256: pathSha256, status: 'digest_mismatch' });
    }
    return selectSource(source, { ...base, observed_sha256: pathSha256, status: 'verified' });
  }));
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
const VERIFICATION_PROMPT_CONTRACTS = new Map([
  ['evidence-l0-corpus', {
    known_id: 'known:locked-synthetic-source-bindings',
    known_statement: 'Locked synthetic source anchors expose locators, digests, byte sizes, and media types for this fixture.',
    gap_id: 'gap:representative-source-and-coverage',
    gap_statement: 'A representative real source and a corpus-coverage witness have not been selected or bound.',
    verification_question: 'Which representative real source should be selected and independently bound before any broader corpus claim is reviewed?',
    route_id: 'candidate-route:external-l1-source-selection',
    route_label: 'Candidate owner route: external L1 representative-source selection'
  }],
  ['evidence-l1-residue', {
    known_id: 'known:open-representative-selection-residue',
    known_statement: 'The representative-selection residue is explicitly open and bound to the synthetic L1 and residue snapshots.',
    gap_id: 'gap:representative-source-selection-decision',
    gap_statement: 'No representative real tower source, selection rationale, or owner decision is bound.',
    verification_question: 'Which real tower, if any, should later be selected?',
    route_id: 'candidate-route:human-owner-source-decision',
    route_label: 'Candidate owner route: human representative-source decision'
  }],
  ['evidence-l2-closure', {
    known_id: 'known:closure-blocked-by-open-residue',
    known_statement: 'Closure remains blocked, and the synthetic L2 and gates snapshots bind that refusal.',
    gap_id: 'gap:closure-witness',
    gap_statement: 'No representative source, closure decision, or independent closure witness is bound.',
    verification_question: 'What bound evidence would satisfy the representative-source gate without exceeding the candidate-local claim ceiling?',
    route_id: 'candidate-route:external-l1-closure-review',
    route_label: 'Candidate owner route: external L1 closure review'
  }]
]);
const FORBIDDEN_ROUTE_FIELDS = [
  'endpoint', 'action', 'request_method', 'method', 'dispatch_hook', 'dispatch',
  'command_binding', 'command', 'execution_status', 'effect', 'score', 'verdict',
  'promotion', 'authority'
];
const SOURCE_BINDING_STATUSES = new Set(['verified', 'object_unavailable', 'path_missing', 'digest_mismatch']);

function verifiedBindingEvidence(reference) {
  return {
    evidence_id: `known:verified-binding:${reference.source_snapshot_id}`,
    statement: `Exact source binding ${reference.source_snapshot_id} remains verified; no combined floor claim is presented while another binding is unavailable.`,
    bound_ref_ids: [reference.source_snapshot_id]
  };
}

function bindingFailureGap(reference) {
  return {
    gap_id: `binding-failure:${reference.source_snapshot_id}`,
    statement: `Source binding ${reference.source_snapshot_id} is ${reference.status}: repository ${reference.repository_ref}; object ${reference.object_id}; path ${reference.path}; expected SHA-256 ${reference.expected_sha256}; observed SHA-256 ${reference.observed_sha256 || 'unavailable'}. Ordinary sourced claim suppressed.`
  };
}

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

export function validateVerificationPromptProjections(projectionSet, view, manifest = view?.scene_manifest) {
  if (!projectionSet || projectionSet.schema_version !== 'cal.verification-prompt-set.v1'
    || projectionSet.authority_effect !== 'none' || projectionSet.interaction_contract !== 'display-only'
    || !Array.isArray(projectionSet.prompts) || projectionSet.prompts.length !== EVIDENCE_SCENE_IDS.size
    || !view || view.authority_effect !== 'none' || !Array.isArray(view.sources)
    || !manifest || !Array.isArray(manifest.towers) || manifest.towers.length !== 1) {
    sceneFailure('verification prompt set is not bound to the candidate-local scene view');
  }
  const scenes = new Map(manifest.towers[0].scenes.map((scene) => [scene.level_id, scene]));
  const sources = new Map(view.sources.map((source) => [source.id, source]));
  const seen = new Set();
  projectionSet.prompts.forEach((prompt) => {
    const contract = prompt && VERIFICATION_PROMPT_CONTRACTS.get(prompt.selected_floor_id);
    const scene = prompt && scenes.get(prompt.selected_floor_id);
    if (!contract || !scene || prompt.schema_version !== 'cal.verification-prompt-projection.v1'
      || seen.has(prompt.selected_floor_id)
      || !Array.isArray(prompt.bound_evidence_refs)
      || !Array.isArray(prompt.known_evidence) || prompt.known_evidence.length === 0
      || !Array.isArray(prompt.unbound_evidence) || prompt.unbound_evidence.length === 0
      || prompt.verification_question !== contract.verification_question
      || !prompt.route_suggestion || prompt.route_suggestion.route_id !== contract.route_id
      || prompt.route_suggestion.label !== contract.route_label || prompt.route_suggestion.executable !== false
      || FORBIDDEN_ROUTE_FIELDS.some((field) => Object.hasOwn(prompt.route_suggestion, field))) {
      sceneFailure('verification prompt does not match its closed floor contract');
    }
    const expectedRefs = scene.source_refs;
    const actualRefs = prompt.bound_evidence_refs.map((reference) => reference.source_snapshot_id);
    if (!equalStringArray(actualRefs, expectedRefs)) {
      sceneFailure(`verification prompt ${prompt.selected_floor_id} exchanges its source bindings`);
    }
    prompt.bound_evidence_refs.forEach((reference) => {
      const source = sources.get(reference.source_snapshot_id);
      const statusShapeValid = reference.status === 'verified'
        ? reference.observed_sha256 === reference.expected_sha256
        : ['object_unavailable', 'path_missing'].includes(reference.status)
          ? reference.observed_sha256 === null
          : reference.status === 'digest_mismatch'
            && /^[a-f0-9]{64}$/u.test(reference.observed_sha256 || '')
            && reference.observed_sha256 !== reference.expected_sha256;
      if (!source || reference.repository_ref !== source.repository_ref
        || reference.object_id !== source.object_id || reference.path !== source.path
        || reference.expected_sha256 !== source.expected_sha256
        || reference.observed_sha256 !== source.observed_sha256
        || reference.status !== source.binding_status
        || !nonEmptyString(reference.repository_ref)
        || !/^[a-f0-9]{40,64}$/u.test(reference.object_id || '')
        || !nonEmptyString(reference.path) || path.isAbsolute(reference.path) || reference.path.startsWith('../')
        || !/^[a-f0-9]{64}$/u.test(reference.expected_sha256 || '')
        || !SOURCE_BINDING_STATUSES.has(reference.status) || !statusShapeValid) {
        sceneFailure(`verification prompt ${prompt.selected_floor_id} contains an invalid exact source binding`);
      }
    });
    const failures = prompt.bound_evidence_refs.filter((reference) => reference.status !== 'verified');
    const expectedKnown = failures.length === 0
      ? [{ evidence_id: contract.known_id, statement: contract.known_statement, bound_ref_ids: expectedRefs }]
      : prompt.bound_evidence_refs.filter((reference) => reference.status === 'verified').map(verifiedBindingEvidence);
    const expectedGaps = [
      { gap_id: contract.gap_id, statement: contract.gap_statement },
      ...failures.map(bindingFailureGap)
    ];
    if (expectedKnown.length === 0 || JSON.stringify(prompt.known_evidence) !== JSON.stringify(expectedKnown)
      || JSON.stringify(prompt.unbound_evidence) !== JSON.stringify(expectedGaps)) {
      sceneFailure(`verification prompt ${prompt.selected_floor_id} does not preserve its evidence/gap distinction`);
    }
    seen.add(prompt.selected_floor_id);
  });
  return projectionSet;
}

export function buildVerificationPromptProjections(view, manifest = view?.scene_manifest) {
  if (!view || !manifest || !Array.isArray(view.sources) || !Array.isArray(manifest.towers)) {
    sceneFailure('verification prompts require the verified scene view');
  }
  const sourceById = new Map(view.sources.map((source) => [source.id, source]));
  const prompts = manifest.towers[0].scenes.map((scene) => {
    const contract = VERIFICATION_PROMPT_CONTRACTS.get(scene.level_id);
    if (!contract) sceneFailure(`verification prompt contract is unavailable for ${scene.level_id}`);
    const boundEvidenceRefs = scene.source_refs.map((sourceId) => {
      const source = sourceById.get(sourceId);
      if (!source) sceneFailure(`verification prompt source ${sourceId} is unavailable`);
      return {
        source_snapshot_id: source.id,
        repository_ref: source.repository_ref,
        object_id: source.object_id,
        path: source.path,
        expected_sha256: source.expected_sha256,
        observed_sha256: source.observed_sha256,
        status: source.binding_status
      };
    });
    const failures = boundEvidenceRefs.filter((reference) => reference.status !== 'verified');
    return {
      schema_version: 'cal.verification-prompt-projection.v1',
      selected_floor_id: scene.level_id,
      bound_evidence_refs: boundEvidenceRefs,
      known_evidence: failures.length === 0
        ? [{ evidence_id: contract.known_id, statement: contract.known_statement, bound_ref_ids: [...scene.source_refs] }]
        : boundEvidenceRefs.filter((reference) => reference.status === 'verified').map(verifiedBindingEvidence),
      unbound_evidence: [
        { gap_id: contract.gap_id, statement: contract.gap_statement },
        ...failures.map(bindingFailureGap)
      ],
      verification_question: contract.verification_question,
      route_suggestion: { route_id: contract.route_id, label: contract.route_label, executable: false }
    };
  });
  return validateVerificationPromptProjections({
    schema_version: 'cal.verification-prompt-set.v1',
    authority_effect: 'none',
    interaction_contract: 'display-only',
    prompts
  }, view, manifest);
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
  const fixturePath = lockedPath(repositoryRoot, lock.inputs.fixture);
  const sourceRoot = path.resolve(path.dirname(fixturePath), '..', '..');
  const verifiedSources = await resolveFixtureSourceBindings({ repositoryRoot, sourceRoot, sources: locked.fixture.source_snapshots });

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
    sources: verifiedSources,
    records: projection.records.map(selectRecord),
    relations: projection.relations.map(({ kind, relation_id, from_id, to_id, direction }) => ({ kind, relation_id, from_id, to_id, direction })),
    residues: locked.fixture.residue_items.map(({ id, status, question, scope, blocked_claim_ids, blocked_gate_ids }) => ({ id, status, question, scope, blocked_claim_ids, blocked_gate_ids })),
    candidates: locked.fixture.ontology_candidates.map(({ id, status, proposed_meaning, scope, evidence_ceiling, contradiction_path }) => ({ id, status, proposed_meaning, scope, evidence_ceiling, contradiction_path })),
    locked_inputs: REQUIRED_LOCKS.map((name) => ({ name, path: lock.inputs[name].path, sha256: lock.inputs[name].sha256 }))
  };
  const sceneManifest = buildTowerSceneManifest(view);
  const completeView = { ...view, scene_manifest: sceneManifest };
  return { ...completeView, verification_prompts: buildVerificationPromptProjections(completeView, sceneManifest) };
}
