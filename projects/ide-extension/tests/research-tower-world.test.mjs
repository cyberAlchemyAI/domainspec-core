import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

import {
  DEFAULT_INTERACTIVE_WORLD_MANIFEST,
  FULL_WALL_COLLISION_FIXTURE,
  WORLD_MANIFEST_VERSION,
  WorldProjectionError,
  admitWorldManifest,
  canonicalWorldState,
  createInitialWorldProjectionState,
  hitTestHotspot,
  reduceWorldProjection,
} from '../src/research-tower/world-model.mjs';
import { createWorldRenderer } from '../src/research-tower/world-renderer.mjs';
import { canonicalSemanticInspectionState, mountWorldBridge } from '../src/research-tower/world-bridge.mjs';
import { createServer } from '../src/server.mjs';

const copy = (value) => structuredClone(value);
const repositoryRoot = path.resolve(fileURLToPath(new URL('../../..', import.meta.url)));
const projectRoot = path.join(repositoryRoot, 'projects/ide-extension');

class FakeElement {
  constructor(ownerDocument, tagName) {
    this.ownerDocument = ownerDocument;
    this.tagName = tagName;
    this.attributes = new Map();
    this.children = [];
    this.listeners = new Map();
    this.parentNode = null;
    this.isContentEditable = false;
  }

  setAttribute(name, value) {
    this.attributes.set(name, String(value));
    if (name === 'id') this.ownerDocument.ids.set(String(value), this);
  }

  getAttribute(name) { return this.attributes.get(name) ?? null; }

  append(...children) {
    for (const child of children) {
      child.parentNode = this;
      this.children.push(child);
    }
  }

  replaceChildren(...children) {
    this.children = [];
    this.append(...children);
  }

  addEventListener(type, listener) {
    if (!this.listeners.has(type)) this.listeners.set(type, new Set());
    this.listeners.get(type).add(listener);
  }

  removeEventListener(type, listener) { this.listeners.get(type)?.delete(listener); }

  dispatch(type, init = {}) {
    const event = { target: this, preventDefault() { this.defaultPrevented = true; }, ...init };
    for (const listener of this.listeners.get(type) ?? []) listener(event);
    return event;
  }

  focus() { this.ownerDocument.activeElement = this; }

  getScreenCTM() {
    return { inverse: () => ({ transformPoint: ({ x, y }) => ({ x: x - 10, y: y - 20 }) }) };
  }

  createSVGPoint() {
    return {
      x: 0,
      y: 0,
      matrixTransform(matrix) {
        return matrix.transformPoint({ x: this.x, y: this.y });
      },
    };
  }

  findByAttribute(name, value = null) {
    if (this.attributes.has(name) && (value === null || this.attributes.get(name) === value)) return this;
    for (const child of this.children) {
      const found = child.findByAttribute(name, value);
      if (found) return found;
    }
    return null;
  }
}

class FakeDocument {
  constructor() {
    this.ids = new Map();
    this.activeElement = null;
  }

  createElementNS(_namespace, name) { return new FakeElement(this, name); }
  createElement(name) { return new FakeElement(this, name); }
  getElementById(id) { return this.ids.get(id) ?? null; }
}

function listen(server) {
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server.address().port)));
}

function close(server) {
  return new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}

function move(state, manifest, dx, dy, inputKind = 'keyboard') {
  return reduceWorldProjection(state, {
    type: 'MOVE_AVATAR', dx, dy, input_kind: inputKind,
  }, manifest);
}

test('world manifest admission accepts the two fixtures and rejects malformed authority or geometry', () => {
  assert.equal(DEFAULT_INTERACTIVE_WORLD_MANIFEST.schema_version, WORLD_MANIFEST_VERSION);
  assert.equal(DEFAULT_INTERACTIVE_WORLD_MANIFEST.avatar.sprite.frame_count, 4);
  assert.equal(DEFAULT_INTERACTIVE_WORLD_MANIFEST.avatar.sprite.frame_width, 543);
  assert.ok(Object.isFrozen(DEFAULT_INTERACTIVE_WORLD_MANIFEST));
  assert.ok(Object.isFrozen(FULL_WALL_COLLISION_FIXTURE));

  const initial = createInitialWorldProjectionState(DEFAULT_INTERACTIVE_WORLD_MANIFEST);
  assert.deepEqual(initial, {
    world_id: 'research-tower-world',
    scene_id: 'L0',
    pose: { x: 48, y: 64 },
    camera: { x: 0, y: 0 },
    visible: true,
    reduced_motion: false,
    lifecycle: 'ready',
    step_index: 0,
    active_hotspot_id: null,
    last_input_kind: null,
  });
  assert.ok(Object.isFrozen(initial));
  assert.throws(
    () => createInitialWorldProjectionState(Object.freeze(copy(DEFAULT_INTERACTIVE_WORLD_MANIFEST))),
    (error) => error instanceof WorldProjectionError && error.code === 'WORLD_MANIFEST_NOT_ADMITTED'
  );

  const cases = [
    ['version', (value) => { value.schema_version = 'v2'; }],
    ['extra top-level key', (value) => { value.evidence = {}; }],
    ['authority', (value) => { value.authority_effect = 'write'; }],
    ['duplicate wall', (value) => { value.walls.push(copy(value.walls[0])); }],
    ['outside geometry', (value) => { value.hotspots[0].x = 200; }],
    ['bad asset', (value) => { value.avatar.sprite.sha256 = '0'.repeat(64); }],
    ['missing binding', (value) => { value.bindings = []; }],
    ['duplicate semantic control', (value) => {
      value.hotspots.push({ id: 'other-hotspot', x: 40, y: 112, width: 16, height: 16, occluded: false });
      value.bindings.push({ hotspot_id: 'other-hotspot', semantic_control_id: 'ontology-candidate-control', semantic_action_id: 'show-other' });
    }],
  ];
  for (const [label, mutate] of cases) {
    const candidate = copy(DEFAULT_INTERACTIVE_WORLD_MANIFEST);
    mutate(candidate);
    assert.throws(() => admitWorldManifest(candidate), WorldProjectionError, label);
  }
});

test('world movement collision and replay is deterministic and non-vacuous', () => {
  const manifest = DEFAULT_INTERACTIVE_WORLD_MANIFEST;
  const trace = [
    [0, 8], [0, 8], [0, 8],
    [8, 0], [8, 0], [8, 0], [8, 0],
  ];
  const run = () => {
    let state = createInitialWorldProjectionState(manifest);
    for (const [dx, dy] of trace) {
      const result = move(state, manifest, dx, dy);
      assert.equal(result.status, 'committed');
      state = result.state;
    }
    return state;
  };
  const first = run();
  const second = run();
  assert.deepEqual(first.pose, { x: 80, y: 88 });
  assert.equal(canonicalWorldState(first), canonicalWorldState(second));

  let clamped = first;
  for (let index = 0; index < 100; index += 1) clamped = move(clamped, manifest, -8, 0).state;
  assert.deepEqual(clamped.pose, { x: 32, y: 88 });

  const wallState = createInitialWorldProjectionState(FULL_WALL_COLLISION_FIXTURE, { pose: { x: 88, y: 88 } });
  const blockedOnce = move(wallState, FULL_WALL_COLLISION_FIXTURE, 8, 0);
  const blockedTwice = move(blockedOnce.state, FULL_WALL_COLLISION_FIXTURE, 8, 0);
  assert.equal(blockedOnce.status, 'no_effect');
  assert.equal(blockedTwice.status, 'no_effect');
  assert.strictEqual(blockedOnce.state, wallState);
  assert.deepEqual(blockedTwice.state.pose, { x: 88, y: 88 });

  for (const intent of [
    { type: 'MOVE_AVATAR', dx: 8, dy: 8, input_kind: 'keyboard' },
    { type: 'MOVE_AVATAR', dx: 7, dy: 0, input_kind: 'keyboard' },
    { type: 'MOVE_AVATAR', dx: Number.NaN, dy: 0, input_kind: 'keyboard' },
  ]) {
    const result = reduceWorldProjection(first, intent, manifest);
    assert.equal(result.status, 'failed');
    assert.strictEqual(result.state, first);
  }
});

test('world hotspot geometry and camera no-effect is a closed decision table', () => {
  const manifest = DEFAULT_INTERACTIVE_WORLD_MANIFEST;
  const initial = createInitialWorldProjectionState(manifest);
  assert.equal(hitTestHotspot(manifest, { x: 136, y: 88 }), 'l0-primary-hotspot');
  assert.equal(hitTestHotspot(manifest, { x: 119, y: 88 }), null);

  const pointer = reduceWorldProjection(initial, {
    type: 'ACTIVATE_HOTSPOT', point: { x: 136, y: 88 }, input_kind: 'pointer',
  }, manifest);
  const overlapState = createInitialWorldProjectionState(manifest, { pose: { x: 136, y: 88 } });
  const keyboard = reduceWorldProjection(overlapState, {
    type: 'ACTIVATE_HOTSPOT', input_kind: 'keyboard',
  }, manifest);
  assert.equal(pointer.status, 'committed');
  assert.equal(keyboard.status, 'committed');
  assert.deepEqual(pointer.request, keyboard.request);
  assert.deepEqual(pointer.request, {
    hotspot_id: 'l0-primary-hotspot',
    semantic_control_id: 'ontology-candidate-control',
    semantic_action_id: 'show-ontology-candidate',
  });

  const outside = reduceWorldProjection(initial, {
    type: 'ACTIVATE_HOTSPOT', point: { x: 119, y: 88 }, input_kind: 'pointer',
  }, manifest);
  assert.equal(outside.status, 'no_effect');
  assert.strictEqual(outside.state, initial);

  const occludedCandidate = copy(manifest);
  occludedCandidate.world_id = 'occluded-control';
  occludedCandidate.hotspots[0].occluded = true;
  const occludedManifest = admitWorldManifest(occludedCandidate);
  const occludedState = createInitialWorldProjectionState(occludedManifest);
  assert.equal(hitTestHotspot(occludedManifest, { x: 136, y: 88 }), null);
  assert.equal(reduceWorldProjection(occludedState, {
    type: 'ACTIVATE_HOTSPOT', point: { x: 136, y: 88 }, input_kind: 'pointer',
  }, occludedManifest).status, 'no_effect');

  const unknown = reduceWorldProjection(initial, {
    type: 'ACTIVATE_HOTSPOT', hotspot_id: 'unknown-hotspot', point: { x: 136, y: 88 }, input_kind: 'pointer',
  }, manifest);
  assert.equal(unknown.status, 'failed');
  assert.equal(unknown.diagnostic.code, 'WORLD_HOTSPOT_UNKNOWN');
  assert.strictEqual(unknown.state, initial);

  const semanticSnapshot = JSON.stringify({ inspectionKind: 'source', inspectionId: 'source:toy:l0' });
  const camera = reduceWorldProjection(initial, { type: 'SET_CAMERA', x: 99, y: -99 }, manifest);
  assert.equal(camera.status, 'committed');
  assert.deepEqual(camera.state.camera, { x: 16, y: -16 });
  assert.equal(semanticSnapshot, JSON.stringify({ inspectionKind: 'source', inspectionId: 'source:toy:l0' }));
});

test('world renderer lifecycle owns SVG input and tears down with zero callbacks', async () => {
  const document = new FakeDocument();
  const host = document.createElement('section');
  const intents = [];
  const failures = [];
  const initial = createInitialWorldProjectionState(DEFAULT_INTERACTIVE_WORLD_MANIFEST);
  const renderer = createWorldRenderer({
    host,
    manifest: DEFAULT_INTERACTIVE_WORLD_MANIFEST,
    initialState: initial,
    onIntent: (intent) => intents.push(intent),
    onFailure: (error) => failures.push(error),
  });
  const surface = host.findByAttribute('data-world-surface');
  const avatar = host.findByAttribute('data-world-avatar');
  assert.ok(surface);
  assert.equal(surface.getAttribute('viewBox'), '0 0 192 192');
  assert.equal(avatar.getAttribute('data-pose'), '48,64');
  assert.equal(host.findByAttribute('data-world-wall', 'north-lab-wall')?.tagName, 'rect');
  assert.equal(host.findByAttribute('data-world-hotspot', 'l0-primary-hotspot')?.tagName, 'rect');
  assert.equal(host.findByAttribute('data-world-avatar-sprite')?.getAttribute('href'), DEFAULT_INTERACTIVE_WORLD_MANIFEST.avatar.sprite.url);
  assert.equal(host.findByAttribute('data-world-avatar-sprite')?.getAttribute('width'), '56');
  assert.equal(host.findByAttribute('data-world-avatar-sprite')?.getAttribute('data-frame-count'), '4');
  assert.equal(host.findByAttribute('data-world-avatar')?.getAttribute('clip-path'), 'url(#research-tower-world-avatar-frame)');

  surface.dispatch('pointerdown', { clientX: 146, clientY: 108 });
  assert.deepEqual(intents.shift(), {
    type: 'ACTIVATE_HOTSPOT', point: { x: 136, y: 88 }, input_kind: 'pointer',
  });
  const keyEvent = surface.dispatch('keydown', { key: 'ArrowRight', altKey: false, ctrlKey: false, metaKey: false, shiftKey: false });
  assert.equal(keyEvent.defaultPrevented, true);
  assert.deepEqual(intents.shift(), { type: 'MOVE_AVATAR', dx: 8, dy: 0, input_kind: 'keyboard' });

  const moved = move(initial, DEFAULT_INTERACTIVE_WORLD_MANIFEST, 0, 8).state;
  renderer.applyState(moved);
  assert.equal(avatar.getAttribute('data-pose'), '48,72');
  renderer.focus();
  assert.strictEqual(document.activeElement, surface);
  assert.equal(renderer.getOwnedCallbackCount(), 0);
  renderer.destroy();
  renderer.destroy();
  assert.equal(host.children.length, 0);
  assert.equal(renderer.isDestroyed(), true);
  surface.dispatch('keydown', { key: 'ArrowLeft' });
  assert.equal(intents.length, 0);
  assert.deepEqual(failures, []);
});

test('world bridge snapshot and request ownership preserves semantic rollback', async () => {
  const document = new FakeDocument();
  const root = document.createElement('main');
  const control = document.createElement('button');
  control.setAttribute('id', 'ontology-candidate-control');
  root.append(control);
  const host = document.createElement('section');
  root.append(host);
  let snapshot = {
    activeFloorId: 'evidence-l0-corpus',
    rememberedFloorId: 'evidence-l0-corpus',
    viewMode: 'room',
    inspectionKind: 'source',
    inspectionId: 'source:toy:l0',
    openedReferenceId: null,
    focusReturnTarget: 'floor-evidence-l0-corpus',
  };
  let subscriber = null;
  let unsubscribeCount = 0;
  const requests = [];
  const statuses = [];
  const bridge = mountWorldBridge({
    host,
    manifest: DEFAULT_INTERACTIVE_WORLD_MANIFEST,
    readSemanticInspectionState: () => ({ ...snapshot }),
    requestSemanticTransition: async (actionId, inputKind) => {
      requests.push({ actionId, inputKind });
      snapshot = { ...snapshot, inspectionKind: 'candidate', inspectionId: 'ontology:candidate:l0' };
      return { status: 'committed', snapshot: { ...snapshot } };
    },
    subscribeCommittedState: (listener) => {
      subscriber = listener;
      return () => { unsubscribeCount += 1; };
    },
    onWorldStatus: (entry) => statuses.push(entry.status),
  });
  assert.match(bridge.getSemanticSnapshot(), /^\{"activeFloorId"/);
  await bridge.sendIntent({ type: 'ACTIVATE_HOTSPOT', point: { x: 136, y: 88 }, input_kind: 'pointer' });
  assert.deepEqual(requests, [{ actionId: 'show-ontology-candidate', inputKind: 'pointer' }]);
  assert.match(bridge.getSemanticSnapshot(), /"inspectionKind":"candidate"/);
  assert.equal(bridge.getOwnedCallbackCount(), 0);
  subscriber({ ...snapshot });
  assert.equal(statuses.at(-1), 'ready');
  bridge.destroy();
  bridge.destroy();
  assert.equal(unsubscribeCount, 1);

  const failureHost = document.createElement('section');
  snapshot = {
    activeFloorId: 'evidence-l0-corpus',
    rememberedFloorId: 'evidence-l0-corpus',
    viewMode: 'room',
    inspectionKind: 'source',
    inspectionId: 'source:toy:l0',
    openedReferenceId: null,
    focusReturnTarget: 'floor-evidence-l0-corpus',
  };
  const before = canonicalSemanticInspectionState(snapshot);
  const failing = mountWorldBridge({
    host: failureHost,
    manifest: DEFAULT_INTERACTIVE_WORLD_MANIFEST,
    readSemanticInspectionState: () => ({ ...snapshot }),
    requestSemanticTransition: async () => { throw new Error('injected bridge failure'); },
    subscribeCommittedState: () => () => {},
    onWorldStatus: () => {},
  });
  const result = await failing.sendIntent({ type: 'ACTIVATE_HOTSPOT', point: { x: 136, y: 88 }, input_kind: 'pointer' });
  assert.equal(result.status, 'failed');
  assert.equal(failing.getStatus(), 'failed');
  assert.equal(canonicalSemanticInspectionState(snapshot), before);
  assert.equal(failureHost.children.length, 0);
});

test('server exposes only exact world modules', async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), 'cal-world-routes-'));
  const server = createServer({ rootDir: projectRoot, stateDir, evidenceRoot: repositoryRoot });
  const port = await listen(server);
  try {
    for (const name of ['world-model.mjs', 'world-renderer.mjs', 'world-bridge.mjs']) {
      const response = await fetch(`http://127.0.0.1:${port}/research-tower/${name}`);
      assert.equal(response.status, 200, name);
      assert.match(response.headers.get('content-type'), /^text\/javascript/);
      assert.equal(await response.text(), await readFile(path.join(projectRoot, 'src/research-tower', name), 'utf8'));
    }
    for (const [method, pathname] of [
      ['GET', '/research-tower/unknown.mjs'],
      ['GET', '/research-tower/world-model.mjs.extra'],
      ['GET', '/research-tower/%2e%2e/server.mjs'],
      ['POST', '/research-tower/world-model.mjs'],
    ]) {
      const response = await fetch(`http://127.0.0.1:${port}${pathname}`, { method });
      assert.ok(response.status >= 400, `${method} ${pathname}`);
      assert.doesNotMatch(await response.text(), /createServer|WORLD_MANIFEST_VERSION/);
    }
  } finally {
    await close(server);
    await rm(stateDir, { recursive: true, force: true });
  }
});
