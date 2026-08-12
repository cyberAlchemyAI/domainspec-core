const SVG_NS = 'http://www.w3.org/2000/svg';

function projectionFailure(code, message, cause = null) {
  const error = new Error(message);
  error.name = 'WorldRendererError';
  error.code = code;
  error.cause = cause;
  return error;
}

function svgElement(document, name, attributes = {}) {
  const element = document.createElementNS(SVG_NS, name);
  for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, String(value));
  return element;
}

function isEditableTarget(target) {
  const tagName = String(target?.tagName ?? '').toLowerCase();
  return target?.isContentEditable === true || ['input', 'textarea', 'select'].includes(tagName);
}

export function clientPointToWorld(svg, clientX, clientY) {
  if (!Number.isFinite(clientX) || !Number.isFinite(clientY)) {
    throw projectionFailure('WORLD_POINTER_INVALID', 'Pointer coordinates must be finite');
  }
  const matrix = svg.getScreenCTM?.();
  if (!matrix || typeof matrix.inverse !== 'function') {
    throw projectionFailure('WORLD_MATRIX_UNAVAILABLE', 'SVG screen transform is unavailable');
  }
  const inverse = matrix.inverse();
  if (typeof svg.createSVGPoint === 'function') {
    const point = svg.createSVGPoint();
    point.x = clientX;
    point.y = clientY;
    const result = point.matrixTransform(inverse);
    return { x: result.x, y: result.y };
  }
  if (typeof DOMPoint === 'function') {
    const result = new DOMPoint(clientX, clientY).matrixTransform(inverse);
    return { x: result.x, y: result.y };
  }
  throw projectionFailure('WORLD_POINT_API_UNAVAILABLE', 'No SVG point transformation API is available');
}

export function createWorldRenderer({ host, manifest, initialState, onIntent, onFailure }) {
  if (!host?.ownerDocument || typeof host.replaceChildren !== 'function') {
    throw projectionFailure('WORLD_HOST_INVALID', 'A DOM host is required');
  }
  if (typeof onIntent !== 'function' || typeof onFailure !== 'function') {
    throw projectionFailure('WORLD_CALLBACK_INVALID', 'Renderer callbacks are required');
  }

  const document = host.ownerDocument;
  let destroyed = false;
  let state = initialState;
  let pendingInputStartedAt = null;
  let inputSequence = 0;
  const listeners = [];
  const clock = host.ownerDocument.defaultView?.performance ?? globalThis.performance;

  const svg = svgElement(document, 'svg', {
    'data-world-surface': '',
    'data-world-id': manifest.world_id,
    viewBox: `${manifest.view_box.x} ${manifest.view_box.y} ${manifest.view_box.width} ${manifest.view_box.height}`,
    tabindex: '0',
    'aria-label': 'Robot lab world. Use Arrow keys or WASD to move and Enter to inspect the research hotspot.',
    preserveAspectRatio: 'xMidYMid meet',
  });
  const clipId = `${manifest.world_id}-avatar-frame`;
  const definitions = svgElement(document, 'defs');
  const avatarClip = svgElement(document, 'clipPath', { id: clipId });
  avatarClip.append(svgElement(document, 'rect', { x: -7, y: -9, width: 14, height: 18, rx: 3 }));
  definitions.append(avatarClip);
  const camera = svgElement(document, 'g', { 'data-world-camera': '', 'aria-hidden': 'true' });
  const room = svgElement(document, 'rect', {
    'data-world-room': '',
    x: manifest.bounds.min_x,
    y: manifest.bounds.min_y,
    width: manifest.bounds.max_x - manifest.bounds.min_x,
    height: manifest.bounds.max_y - manifest.bounds.min_y,
    rx: 8,
  });
  camera.append(room);

  for (const wall of manifest.walls) {
    camera.append(svgElement(document, 'rect', {
      'data-world-wall': wall.id,
      x: wall.x,
      y: wall.y,
      width: wall.width,
      height: wall.height,
    }));
  }
  for (const hotspot of manifest.hotspots) {
    camera.append(svgElement(document, 'rect', {
      'data-world-hotspot': hotspot.id,
      'data-occluded': hotspot.occluded,
      x: hotspot.x,
      y: hotspot.y,
      width: hotspot.width,
      height: hotspot.height,
      rx: 4,
    }));
  }

  const avatar = svgElement(document, 'g', { 'data-world-avatar': '', 'clip-path': `url(#${clipId})` });
  const avatarPlate = svgElement(document, 'rect', {
    'data-world-avatar-plate': '', x: -8, y: -8, width: 16, height: 16, rx: 5,
  });
  const avatarImage = svgElement(document, 'image', {
    'data-world-avatar-sprite': '',
    href: manifest.avatar.sprite.url,
    x: -7,
    y: -9,
    width: 14 * manifest.avatar.sprite.frame_count,
    height: 18,
    preserveAspectRatio: 'none',
    'data-frame-count': manifest.avatar.sprite.frame_count,
    'data-frame-width': manifest.avatar.sprite.frame_width,
    'data-frame-height': manifest.avatar.sprite.frame_height,
    'data-sheet-width': manifest.avatar.sprite.sheet_width,
    'data-sheet-height': manifest.avatar.sprite.sheet_height,
    'data-source-digest': manifest.avatar.sprite.sha256,
  });
  avatar.append(avatarPlate, avatarImage);
  camera.append(avatar);
  svg.append(definitions, camera);
  host.replaceChildren(svg);

  function listen(target, type, handler) {
    target.addEventListener(type, handler);
    listeners.push(() => target.removeEventListener(type, handler));
  }

  function emit(intent) {
    if (destroyed) return;
    try {
      const result = onIntent(intent);
      if (result && typeof result.catch === 'function') result.catch(onFailure);
    } catch (error) {
      onFailure(error);
    }
  }

  listen(svg, 'pointerdown', (event) => {
    try {
      emit({
        type: 'ACTIVATE_HOTSPOT',
        point: clientPointToWorld(svg, event.clientX, event.clientY),
        input_kind: 'pointer',
      });
    } catch (error) {
      onFailure(error);
    }
  });

  listen(svg, 'keydown', (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || isEditableTarget(event.target)) return;
    const steps = {
      ArrowLeft: [-manifest.avatar.step, 0], a: [-manifest.avatar.step, 0], A: [-manifest.avatar.step, 0],
      ArrowRight: [manifest.avatar.step, 0], d: [manifest.avatar.step, 0], D: [manifest.avatar.step, 0],
      ArrowUp: [0, -manifest.avatar.step], w: [0, -manifest.avatar.step], W: [0, -manifest.avatar.step],
      ArrowDown: [0, manifest.avatar.step], s: [0, manifest.avatar.step], S: [0, manifest.avatar.step],
    };
    if (steps[event.key]) {
      event.preventDefault();
      pendingInputStartedAt = clock.now();
      svg.setAttribute('data-last-input-start-ms', pendingInputStartedAt);
      const [dx, dy] = steps[event.key];
      emit({ type: 'MOVE_AVATAR', dx, dy, input_kind: 'keyboard' });
    } else if (event.key === 'Enter') {
      event.preventDefault();
      emit({ type: 'ACTIVATE_HOTSPOT', input_kind: 'keyboard' });
    }
  });

  function applyState(nextState) {
    if (destroyed) return;
    state = nextState;
    avatar.setAttribute('transform', `translate(${state.pose.x} ${state.pose.y})`);
    avatar.setAttribute('data-pose', `${state.pose.x},${state.pose.y}`);
    camera.setAttribute('transform', `translate(${-state.camera.x} ${-state.camera.y})`);
    svg.setAttribute('data-visible', String(state.visible));
    svg.setAttribute('data-reduced-motion', String(state.reduced_motion));
    svg.setAttribute('data-lifecycle', state.lifecycle);
    svg.setAttribute('data-motion', 'settled');
    if (pendingInputStartedAt !== null) {
      inputSequence += 1;
      svg.setAttribute('data-last-input-sequence', inputSequence);
      svg.setAttribute('data-last-input-latency-ms', Math.max(0, clock.now() - pendingInputStartedAt));
      pendingInputStartedAt = null;
    }
  }

  function focus() {
    if (!destroyed) svg.focus();
  }

  function destroy() {
    if (destroyed) return;
    destroyed = true;
    while (listeners.length) listeners.pop()();
    host.replaceChildren();
  }

  applyState(initialState);
  return Object.freeze({
    element: svg,
    applyState,
    focus,
    destroy,
    getState: () => state,
    getOwnedCallbackCount: () => 0,
    isDestroyed: () => destroyed,
  });
}
