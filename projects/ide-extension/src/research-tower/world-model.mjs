export const WORLD_MANIFEST_VERSION = 'cal.world-manifest.v1';

const SPRITE = Object.freeze({
  url: '/assets/research-tower-concepts/robot-cowork-rpg-sprite-sheet.png',
  sha256: '04fa18bb405b59380b4be2b5a88bebd88632837e1fd21467e626832f43e37afa',
  sheet_width: 2172,
  sheet_height: 724,
  frame_width: 543,
  frame_height: 724,
  frame_count: 4,
});

const IDENTIFIER = /^[A-Za-z0-9][A-Za-z0-9:._-]*$/;
const OWN = (value, key) => Object.prototype.hasOwnProperty.call(value, key);
const ADMITTED_MANIFESTS = new WeakSet();

export class WorldProjectionError extends Error {
  constructor(code, message, details = null) {
    super(message);
    this.name = 'WorldProjectionError';
    this.code = code;
    this.details = details;
  }
}

function fail(code, message, details = null) {
  throw new WorldProjectionError(code, message, details);
}

function assertRecord(value, code, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    fail(code, `${label} must be an object`);
  }
}

function assertClosedKeys(value, required, code, label) {
  assertRecord(value, code, label);
  const expected = new Set(required);
  const keys = Object.keys(value);
  for (const key of required) {
    if (!OWN(value, key)) fail(code, `${label}.${key} is required`);
  }
  for (const key of keys) {
    if (!expected.has(key)) fail(code, `${label}.${key} is not allowed`);
  }
}

function assertIdentifier(value, code, label) {
  if (typeof value !== 'string' || !IDENTIFIER.test(value)) {
    fail(code, `${label} must be a stable identifier`);
  }
}

function assertFiniteInteger(value, code, label, { minimum = -Infinity, maximum = Infinity } = {}) {
  if (!Number.isInteger(value) || value < minimum || value > maximum) {
    fail(code, `${label} must be an integer in ${minimum}..${maximum}`);
  }
}

function assertBoolean(value, code, label) {
  if (typeof value !== 'boolean') fail(code, `${label} must be boolean`);
}

function deepFreeze(value) {
  if (!value || typeof value !== 'object' || Object.isFrozen(value)) return value;
  for (const child of Object.values(value)) deepFreeze(child);
  return Object.freeze(value);
}

function clonePoint(point) {
  return { x: point.x, y: point.y };
}

function cloneRect(rect) {
  return { id: rect.id, x: rect.x, y: rect.y, width: rect.width, height: rect.height };
}

function rectanglesOverlap(left, right) {
  return left.x < right.x + right.width
    && left.x + left.width > right.x
    && left.y < right.y + right.height
    && left.y + left.height > right.y;
}

function pointInsideRect(point, rect) {
  return point.x >= rect.x
    && point.x <= rect.x + rect.width
    && point.y >= rect.y
    && point.y <= rect.y + rect.height;
}

function assertRect(rect, code, label, bounds) {
  assertClosedKeys(rect, ['id', 'x', 'y', 'width', 'height'], code, label);
  assertIdentifier(rect.id, code, `${label}.id`);
  for (const key of ['x', 'y']) assertFiniteInteger(rect[key], code, `${label}.${key}`);
  for (const key of ['width', 'height']) {
    assertFiniteInteger(rect[key], code, `${label}.${key}`, { minimum: 1 });
  }
  if (rect.x < bounds.min_x || rect.y < bounds.min_y
      || rect.x + rect.width > bounds.max_x || rect.y + rect.height > bounds.max_y) {
    fail(code, `${label} must stay inside world bounds`);
  }
}

function assertUniqueIds(items, code, label) {
  const ids = new Set();
  for (const item of items) {
    if (ids.has(item.id)) fail(code, `${label} contains duplicate id ${item.id}`);
    ids.add(item.id);
  }
}

function normalizeManifest(candidate) {
  assertClosedKeys(candidate, [
    'schema_version',
    'world_id',
    'scene_id',
    'view_box',
    'bounds',
    'camera_bounds',
    'avatar',
    'walls',
    'hotspots',
    'bindings',
    'authority_effect',
  ], 'WORLD_MANIFEST_SHAPE_INVALID', 'manifest');

  if (candidate.schema_version !== WORLD_MANIFEST_VERSION) {
    fail('WORLD_MANIFEST_VERSION_UNSUPPORTED', `Expected ${WORLD_MANIFEST_VERSION}`);
  }
  assertIdentifier(candidate.world_id, 'WORLD_MANIFEST_ID_INVALID', 'manifest.world_id');
  assertIdentifier(candidate.scene_id, 'WORLD_MANIFEST_ID_INVALID', 'manifest.scene_id');
  if (candidate.authority_effect !== 'none') {
    fail('WORLD_MANIFEST_AUTHORITY_FORBIDDEN', 'World manifests must have authority_effect:none');
  }

  assertClosedKeys(candidate.view_box, ['x', 'y', 'width', 'height'], 'WORLD_VIEWBOX_INVALID', 'manifest.view_box');
  assertFiniteInteger(candidate.view_box.x, 'WORLD_VIEWBOX_INVALID', 'manifest.view_box.x');
  assertFiniteInteger(candidate.view_box.y, 'WORLD_VIEWBOX_INVALID', 'manifest.view_box.y');
  assertFiniteInteger(candidate.view_box.width, 'WORLD_VIEWBOX_INVALID', 'manifest.view_box.width', { minimum: 1 });
  assertFiniteInteger(candidate.view_box.height, 'WORLD_VIEWBOX_INVALID', 'manifest.view_box.height', { minimum: 1 });

  assertClosedKeys(candidate.bounds, ['min_x', 'max_x', 'min_y', 'max_y'], 'WORLD_BOUNDS_INVALID', 'manifest.bounds');
  for (const key of ['min_x', 'max_x', 'min_y', 'max_y']) {
    assertFiniteInteger(candidate.bounds[key], 'WORLD_BOUNDS_INVALID', `manifest.bounds.${key}`);
  }
  if (candidate.bounds.min_x >= candidate.bounds.max_x || candidate.bounds.min_y >= candidate.bounds.max_y) {
    fail('WORLD_BOUNDS_INVALID', 'World bounds must have positive area');
  }

  assertClosedKeys(candidate.camera_bounds, ['min_x', 'max_x', 'min_y', 'max_y'], 'WORLD_CAMERA_BOUNDS_INVALID', 'manifest.camera_bounds');
  for (const key of ['min_x', 'max_x', 'min_y', 'max_y']) {
    assertFiniteInteger(candidate.camera_bounds[key], 'WORLD_CAMERA_BOUNDS_INVALID', `manifest.camera_bounds.${key}`);
  }
  if (candidate.camera_bounds.min_x > candidate.camera_bounds.max_x
      || candidate.camera_bounds.min_y > candidate.camera_bounds.max_y) {
    fail('WORLD_CAMERA_BOUNDS_INVALID', 'Camera bounds are inverted');
  }

  assertClosedKeys(candidate.avatar, ['spawn', 'step', 'radius', 'sprite'], 'WORLD_AVATAR_INVALID', 'manifest.avatar');
  assertClosedKeys(candidate.avatar.spawn, ['x', 'y'], 'WORLD_AVATAR_INVALID', 'manifest.avatar.spawn');
  assertFiniteInteger(candidate.avatar.spawn.x, 'WORLD_AVATAR_INVALID', 'manifest.avatar.spawn.x');
  assertFiniteInteger(candidate.avatar.spawn.y, 'WORLD_AVATAR_INVALID', 'manifest.avatar.spawn.y');
  assertFiniteInteger(candidate.avatar.step, 'WORLD_AVATAR_INVALID', 'manifest.avatar.step', { minimum: 1 });
  assertFiniteInteger(candidate.avatar.radius, 'WORLD_AVATAR_INVALID', 'manifest.avatar.radius', { minimum: 1 });
  if (candidate.avatar.spawn.x < candidate.bounds.min_x || candidate.avatar.spawn.x > candidate.bounds.max_x
      || candidate.avatar.spawn.y < candidate.bounds.min_y || candidate.avatar.spawn.y > candidate.bounds.max_y) {
    fail('WORLD_AVATAR_INVALID', 'Avatar spawn is outside world bounds');
  }

  assertClosedKeys(candidate.avatar.sprite, [
    'url', 'sha256', 'sheet_width', 'sheet_height', 'frame_width', 'frame_height', 'frame_count',
  ], 'WORLD_SPRITE_INVALID', 'manifest.avatar.sprite');
  for (const [key, value] of Object.entries(SPRITE)) {
    if (candidate.avatar.sprite[key] !== value) {
      fail('WORLD_SPRITE_INVALID', `manifest.avatar.sprite.${key} does not match the admitted local asset`);
    }
  }

  if (!Array.isArray(candidate.walls) || !Array.isArray(candidate.hotspots) || !Array.isArray(candidate.bindings)) {
    fail('WORLD_COLLECTION_INVALID', 'walls, hotspots, and bindings must be arrays');
  }
  if (candidate.walls.length === 0 || candidate.hotspots.length === 0) {
    fail('WORLD_COLLECTION_INVALID', 'At least one wall and hotspot are required');
  }

  candidate.walls.forEach((wall, index) => assertRect(wall, 'WORLD_WALL_INVALID', `manifest.walls[${index}]`, candidate.bounds));
  assertUniqueIds(candidate.walls, 'WORLD_WALL_INVALID', 'manifest.walls');

  candidate.hotspots.forEach((hotspot, index) => {
    assertClosedKeys(hotspot, ['id', 'x', 'y', 'width', 'height', 'occluded'], 'WORLD_HOTSPOT_INVALID', `manifest.hotspots[${index}]`);
    assertRect({ id: hotspot.id, x: hotspot.x, y: hotspot.y, width: hotspot.width, height: hotspot.height }, 'WORLD_HOTSPOT_INVALID', `manifest.hotspots[${index}]`, candidate.bounds);
    assertBoolean(hotspot.occluded, 'WORLD_HOTSPOT_INVALID', `manifest.hotspots[${index}].occluded`);
  });
  assertUniqueIds(candidate.hotspots, 'WORLD_HOTSPOT_INVALID', 'manifest.hotspots');
  for (let left = 0; left < candidate.hotspots.length; left += 1) {
    for (let right = left + 1; right < candidate.hotspots.length; right += 1) {
      if (rectanglesOverlap(candidate.hotspots[left], candidate.hotspots[right])) {
        fail('WORLD_HOTSPOT_AMBIGUOUS', 'Hotspot geometry must not overlap');
      }
    }
  }

  const hotspotIds = new Set(candidate.hotspots.map(({ id }) => id));
  const bindingHotspots = new Set();
  const semanticControls = new Set();
  for (let index = 0; index < candidate.bindings.length; index += 1) {
    const binding = candidate.bindings[index];
    assertClosedKeys(binding, ['hotspot_id', 'semantic_control_id', 'semantic_action_id'], 'WORLD_BINDING_INVALID', `manifest.bindings[${index}]`);
    for (const key of ['hotspot_id', 'semantic_control_id', 'semantic_action_id']) {
      assertIdentifier(binding[key], 'WORLD_BINDING_INVALID', `manifest.bindings[${index}].${key}`);
    }
    if (!hotspotIds.has(binding.hotspot_id) || bindingHotspots.has(binding.hotspot_id)
        || semanticControls.has(binding.semantic_control_id)) {
      fail('WORLD_BINDING_INVALID', 'Bindings must be total and one-to-one');
    }
    bindingHotspots.add(binding.hotspot_id);
    semanticControls.add(binding.semantic_control_id);
  }
  if (bindingHotspots.size !== hotspotIds.size) {
    fail('WORLD_BINDING_INVALID', 'Every hotspot needs exactly one semantic binding');
  }

  return {
    schema_version: candidate.schema_version,
    world_id: candidate.world_id,
    scene_id: candidate.scene_id,
    view_box: { ...candidate.view_box },
    bounds: { ...candidate.bounds },
    camera_bounds: { ...candidate.camera_bounds },
    avatar: {
      spawn: clonePoint(candidate.avatar.spawn),
      step: candidate.avatar.step,
      radius: candidate.avatar.radius,
      sprite: { ...candidate.avatar.sprite },
    },
    walls: candidate.walls.map(cloneRect),
    hotspots: candidate.hotspots.map((hotspot) => ({ ...hotspot })),
    bindings: candidate.bindings.map((binding) => ({ ...binding })),
    authority_effect: 'none',
  };
}

export function admitWorldManifest(candidate) {
  const admitted = deepFreeze(normalizeManifest(candidate));
  ADMITTED_MANIFESTS.add(admitted);
  return admitted;
}

const INTERACTIVE_CANDIDATE = {
  schema_version: WORLD_MANIFEST_VERSION,
  world_id: 'research-tower-world',
  scene_id: 'L0',
  view_box: { x: 0, y: 0, width: 192, height: 192 },
  bounds: { min_x: 32, max_x: 160, min_y: 48, max_y: 144 },
  camera_bounds: { min_x: -16, max_x: 16, min_y: -16, max_y: 16 },
  avatar: { spawn: { x: 48, y: 64 }, step: 8, radius: 8, sprite: { ...SPRITE } },
  walls: [{ id: 'north-lab-wall', x: 96, y: 48, width: 8, height: 24 }],
  hotspots: [{ id: 'l0-primary-hotspot', x: 120, y: 72, width: 32, height: 32, occluded: false }],
  bindings: [{
    hotspot_id: 'l0-primary-hotspot',
    semantic_control_id: 'ontology-candidate-control',
    semantic_action_id: 'show-ontology-candidate',
  }],
  authority_effect: 'none',
};

export const DEFAULT_INTERACTIVE_WORLD_MANIFEST = admitWorldManifest(INTERACTIVE_CANDIDATE);

export const FULL_WALL_COLLISION_FIXTURE = admitWorldManifest({
  ...INTERACTIVE_CANDIDATE,
  world_id: 'research-tower-full-wall-control',
  walls: [{ id: 'full-lab-wall', x: 96, y: 48, width: 8, height: 96 }],
});

function assertManifest(manifest) {
  if (!manifest || !ADMITTED_MANIFESTS.has(manifest)) {
    fail('WORLD_MANIFEST_NOT_ADMITTED', 'An admitted frozen WorldManifest is required');
  }
}

function makeState(manifest, pose) {
  return deepFreeze({
    world_id: manifest.world_id,
    scene_id: manifest.scene_id,
    pose: clonePoint(pose),
    camera: { x: 0, y: 0 },
    visible: true,
    reduced_motion: false,
    lifecycle: 'ready',
    step_index: 0,
    active_hotspot_id: null,
    last_input_kind: null,
  });
}

export function createInitialWorldProjectionState(manifest, options = {}) {
  assertManifest(manifest);
  assertRecord(options, 'WORLD_INITIAL_STATE_INVALID', 'options');
  for (const key of Object.keys(options)) {
    if (key !== 'pose') fail('WORLD_INITIAL_STATE_INVALID', `options.${key} is not allowed`);
  }
  const pose = options.pose ?? manifest.avatar.spawn;
  assertClosedKeys(pose, ['x', 'y'], 'WORLD_INITIAL_STATE_INVALID', 'options.pose');
  assertFiniteInteger(pose.x, 'WORLD_INITIAL_STATE_INVALID', 'options.pose.x');
  assertFiniteInteger(pose.y, 'WORLD_INITIAL_STATE_INVALID', 'options.pose.y');
  if (pose.x < manifest.bounds.min_x || pose.x > manifest.bounds.max_x
      || pose.y < manifest.bounds.min_y || pose.y > manifest.bounds.max_y) {
    fail('WORLD_INITIAL_STATE_INVALID', 'Initial pose is outside world bounds');
  }
  return makeState(manifest, pose);
}

export function canonicalWorldState(state) {
  assertRecord(state, 'WORLD_STATE_INVALID', 'state');
  return JSON.stringify({
    world_id: state.world_id,
    scene_id: state.scene_id,
    pose: { x: state.pose.x, y: state.pose.y },
    camera: { x: state.camera.x, y: state.camera.y },
    visible: state.visible,
    reduced_motion: state.reduced_motion,
    lifecycle: state.lifecycle,
    step_index: state.step_index,
    active_hotspot_id: state.active_hotspot_id,
    last_input_kind: state.last_input_kind,
  });
}

function withState(state, patch) {
  return deepFreeze({
    world_id: state.world_id,
    scene_id: state.scene_id,
    pose: patch.pose ? clonePoint(patch.pose) : clonePoint(state.pose),
    camera: patch.camera ? clonePoint(patch.camera) : clonePoint(state.camera),
    visible: patch.visible ?? state.visible,
    reduced_motion: patch.reduced_motion ?? state.reduced_motion,
    lifecycle: patch.lifecycle ?? state.lifecycle,
    step_index: patch.step_index ?? state.step_index,
    active_hotspot_id: OWN(patch, 'active_hotspot_id') ? patch.active_hotspot_id : state.active_hotspot_id,
    last_input_kind: OWN(patch, 'last_input_kind') ? patch.last_input_kind : state.last_input_kind,
  });
}

function noEffect(state, diagnostic = null) {
  return { status: 'no_effect', state, diagnostic };
}

function failed(state, code, message) {
  return { status: 'failed', state, diagnostic: { code, message } };
}

function avatarRect(point, radius) {
  return { x: point.x - radius, y: point.y - radius, width: radius * 2, height: radius * 2 };
}

function collidesWithWall(manifest, point) {
  const avatar = avatarRect(point, manifest.avatar.radius);
  return manifest.walls.some((wall) => rectanglesOverlap(avatar, wall));
}

export function hitTestHotspot(manifest, point) {
  assertManifest(manifest);
  if (!point || !Number.isFinite(point.x) || !Number.isFinite(point.y)) {
    fail('WORLD_POINT_INVALID', 'A finite world point is required');
  }
  const hit = manifest.hotspots.find((hotspot) => !hotspot.occluded && pointInsideRect(point, hotspot));
  return hit?.id ?? null;
}

function bindingFor(manifest, hotspotId) {
  return manifest.bindings.find((binding) => binding.hotspot_id === hotspotId) ?? null;
}

function clamp(value, minimum, maximum) {
  return Math.min(maximum, Math.max(minimum, value));
}

export function reduceWorldProjection(state, intent, manifest) {
  assertManifest(manifest);
  if (!state || state.world_id !== manifest.world_id || state.scene_id !== manifest.scene_id) {
    return failed(state, 'WORLD_STATE_INVALID', 'State does not belong to the admitted manifest');
  }
  if (!intent || typeof intent !== 'object' || Array.isArray(intent) || typeof intent.type !== 'string') {
    return failed(state, 'WORLD_INTENT_INVALID', 'Intent must be a typed object');
  }

  if (intent.type === 'MOVE_AVATAR') {
    const { dx, dy, input_kind: inputKind } = intent;
    if (!Number.isFinite(dx) || !Number.isFinite(dy)
        || Math.abs(dx) + Math.abs(dy) !== manifest.avatar.step
        || (dx !== 0 && dy !== 0)) {
      return failed(state, 'WORLD_MOVE_INVALID', 'Movement must be one finite cardinal step');
    }
    const candidate = {
      x: clamp(state.pose.x + dx, manifest.bounds.min_x, manifest.bounds.max_x),
      y: clamp(state.pose.y + dy, manifest.bounds.min_y, manifest.bounds.max_y),
    };
    if ((candidate.x === state.pose.x && candidate.y === state.pose.y) || collidesWithWall(manifest, candidate)) {
      return noEffect(state, { code: 'WORLD_MOVE_BLOCKED' });
    }
    return {
      status: 'committed',
      state: withState(state, {
        pose: candidate,
        step_index: state.step_index + 1,
        last_input_kind: typeof inputKind === 'string' ? inputKind : null,
      }),
    };
  }

  if (intent.type === 'ACTIVATE_HOTSPOT') {
    let hotspotId;
    if (OWN(intent, 'hotspot_id')) {
      if (!manifest.hotspots.some(({ id }) => id === intent.hotspot_id)) {
        return failed(state, 'WORLD_HOTSPOT_UNKNOWN', `Unknown hotspot ${intent.hotspot_id}`);
      }
      hotspotId = intent.hotspot_id;
      const hotspot = manifest.hotspots.find(({ id }) => id === hotspotId);
      const point = intent.point ?? state.pose;
      if (hotspot.occluded || !pointInsideRect(point, hotspot)) return noEffect(state);
    } else {
      try {
        hotspotId = hitTestHotspot(manifest, intent.point ?? state.pose);
      } catch (error) {
        return failed(state, error.code ?? 'WORLD_POINT_INVALID', error.message);
      }
    }
    if (!hotspotId) return noEffect(state);
    const binding = bindingFor(manifest, hotspotId);
    if (!binding) return failed(state, 'WORLD_BINDING_MISSING', `Missing binding for ${hotspotId}`);
    return {
      status: 'committed',
      state: withState(state, {
        active_hotspot_id: hotspotId,
        last_input_kind: typeof intent.input_kind === 'string' ? intent.input_kind : null,
      }),
      request: { ...binding },
    };
  }

  if (intent.type === 'SET_CAMERA') {
    if (!Number.isFinite(intent.x) || !Number.isFinite(intent.y)) {
      return failed(state, 'WORLD_CAMERA_INVALID', 'Camera coordinates must be finite');
    }
    const camera = {
      x: clamp(Math.round(intent.x), manifest.camera_bounds.min_x, manifest.camera_bounds.max_x),
      y: clamp(Math.round(intent.y), manifest.camera_bounds.min_y, manifest.camera_bounds.max_y),
    };
    if (camera.x === state.camera.x && camera.y === state.camera.y) return noEffect(state);
    return { status: 'committed', state: withState(state, { camera }) };
  }

  if (intent.type === 'SET_VISIBILITY') {
    if (typeof intent.visible !== 'boolean') return failed(state, 'WORLD_VISIBILITY_INVALID', 'visible must be boolean');
    if (intent.visible === state.visible) return noEffect(state);
    return { status: 'committed', state: withState(state, { visible: intent.visible }) };
  }

  if (intent.type === 'SET_REDUCED_MOTION') {
    if (typeof intent.enabled !== 'boolean') return failed(state, 'WORLD_MOTION_INVALID', 'enabled must be boolean');
    if (intent.enabled === state.reduced_motion) return noEffect(state);
    return { status: 'committed', state: withState(state, { reduced_motion: intent.enabled }) };
  }

  if (intent.type === 'SET_LIFECYCLE') {
    if (!['ready', 'paused', 'destroyed', 'failed'].includes(intent.lifecycle)) {
      return failed(state, 'WORLD_LIFECYCLE_INVALID', 'Unknown lifecycle value');
    }
    if (intent.lifecycle === state.lifecycle) return noEffect(state);
    return { status: 'committed', state: withState(state, { lifecycle: intent.lifecycle }) };
  }

  return failed(state, 'WORLD_INTENT_UNKNOWN', `Unknown intent ${intent.type}`);
}
