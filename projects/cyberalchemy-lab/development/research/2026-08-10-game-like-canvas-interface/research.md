# Game-like Canvas Interface — Verbatim Explorer Returns

Dispatch: `2026-08-10-cyberalchemy-game-canvas-interface`
Sheet SHA-256: `25928ddf447105cbd2ba307c6295f89c57bdb7b33a2b8b8b15fa0e4efe91f296`
Retrieval date: `2026-08-10`

The parent assembled the following returns verbatim. This file is research evidence, not product, authority, implementation, or release proof.

## Explorer runtime — spawn-0001

```text
Bounded receipt — action spawn-0001 / explorer-runtime / research-explore / read-only

status: completed
mutation: none (no output file written; parent owns persistence to receipts/explorer-runtime.json)
inputs_read: projects/cyberalchemy-lab/development/research/2026-08-10-game-like-canvas-interface/{dispatch-sheet.json,strategy-inventory-packet.json,CONFIRMATION.md}
confirmation_binding: user-confirmation-25928ddf4471; sheet sha256 25928ddf447105cbd2ba307c6295f89c57bdb7b33a2b8b8b15fa0e4efe91f296
claim_ceiling: primary-source architecture comparison only; no package install, product validation, accessibility proof, or production recommendation.

VERDICT MATRIX
- Native DOM + SVG/Canvas: KEEP FOR SPIKE. Zero new runtime dependency; browser supplies rAF, transforms, pointer/keyboard DOM events, SVG semantics, and Canvas. It does not supply camera, scene graph, tilemap, collision, pathfinding, or deterministic simulation; those must remain a tiny typed local world-state/renderer adapter. Best match for one room/floor, one actor, one hotspot while retaining semantic DOM as control/evidence plane.
- Phaser: FALLBACK (strongest full-engine candidate if spike proves need). Official docs describe scenes, a built-in scroll/zoom/bounded Camera, unified mouse/touch plus keyboard/gamepad input, and Tilemap support for orthogonal/isometric/hex/staggered. NPM/bundle delivery is first-class. MIT. Version caveat: official versioned v3 docs expose 3.90.0, while current official repo package manifest reports 4.2.1; do not pin until the exact npm artifact/tag and v4 API compatibility are independently bound. Phaser is a game framework, so it brings the broadest owned world model but also the largest semantic/control-plane integration surface.
- PixiJS: DEFER. Official docs call it primarily a rendering library. It provides a display tree, federated pointer/touch events and hit testing, ticker/rAF render loop, WebGL/WebGPU rendering, modular extensions, and an optional accessibility extension. MIT; official repo currently identifies v8.18.1 latest (Apr 14 2026), releases show installable v8 artifacts. It does not natively own tilemap/isometric, navigation/pathfinding, physics, or a complete game-state architecture. A camera is normally a root-container transform. Better than raw Canvas when render scale/performance is demonstrated as the bottleneck, but premature for one-room proof.
- Excalibur: DEFER (isometric specialist fallback). Official repo identifies latest v0.32.0 (Dec 23 2025), BSD-2-Clause. It owns TypeScript 2D engine concepts, camera/input/actors, flat TileMap, native IsometricMap with worldToTile/tileToWorld, depth/elevation sorting, and collision; official Tiled plugin supports orthogonal/isometric and camera containment. Strongest direct fit for an isometric actor proof, but smaller ecosystem/maturity surface than Phaser and introduces engine + optional plugin before need is established. Asset loader requires HTTP/XHR, which is compatible with the existing local server but not file://.
- Three.js: KILL for this slice. No evidenced 3D requirement; it widens rendering, asset, camera, and accessibility risk without satisfying a current obligation.

SMALLEST INTEGRATION SPIKE
Use native SVG (preferred for inspectable room/hotspot geometry) or a single Canvas strictly as a disposable visual projection next to—not instead of—the existing semantic DOM. Add no dependency. Implement one local `WorldProjection` adapter with immutable input `{sceneId, roomBounds, actorPose, hotspotIds, camera}`; fixed-step deterministic arrow/WASD actor movement inside one L0 room; a bounded pan transform (no free zoom initially); one hit-tested hotspot that emits a typed navigation intent to the existing DOM evidence selector; DOM focus and evidence selection remain authoritative; reduced-motion disables interpolation; unknown scene/hotspot or renderer init failure hides the projection and leaves textual UI intact. Demonstrate: same input sequence => same actor pose; pointer and keyboard select same hotspot; no external/non-GET requests; teardown restores prior DOM focus/selection; source/evidence bytes never enter renderer state; decorative RobotAvatar is not WorkerExecution. Engine-adoption trigger: only reconsider Phaser if the spike requires 2+ scenes plus camera/tilemap/collision orchestration that materially exceeds this adapter; reconsider Pixi only after measured renderer pressure; reconsider Excalibur if isometric depth/collision becomes the core requirement.

PRIMARY SOURCE LEDGER
Phaser docs overview/install/camera/input/tilemap: https://docs.phaser.io/ ; https://docs.phaser.io/phaser/getting-started/installation ; https://docs.phaser.io/phaser/concepts/cameras ; https://docs.phaser.io/phaser/concepts/input ; https://docs.phaser.io/api-documentation/3.90.0/namespace/tilemaps
Phaser manifest/version/license: https://github.com/phaserjs/phaser/blob/master/package.json ; releases: https://github.com/phaserjs/phaser/releases
Pixi architecture/events/ticker/render loop: https://pixijs.com/8.x/guides/concepts/architecture ; https://pixijs.com/8.x/guides/components/events ; https://pixijs.com/8.x/guides/components/ticker ; https://pixijs.com/8.x/guides/concepts/render-loop
Pixi repo/version/license: https://github.com/pixijs/pixijs ; https://github.com/pixijs/pixijs/blob/dev/LICENSE ; https://github.com/pixijs/pixijs/releases
Excalibur repo/version/license: https://github.com/excaliburjs/excalibur ; isometric: https://excaliburjs.com/docs/isometric/ ; Tiled: https://excaliburjs.com/docs/tiled-plugin/ ; loader: https://excaliburjs.com/docs/loader/
Browser baseline animation: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Basic_animations ; rAF: https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame

residue: Exact package tarball hashes/bundle sizes were not established; no live local bundle/CSP test was authorized; renderer and accessibility claims remain documentation-level until a local spike and human/AT evaluation.
```

## Explorer human interface — spawn-0002

```json
{
  "action_id": "spawn-0002",
  "role": "explorer-human-interface",
  "status": "completed",
  "mutation": "none",
  "evidence_boundary": "Primary web standards, first-party browser guidance, and the supplied Inventory packet only. No human study or assistive-technology session was conducted.",
  "source_ledger": [
    {
      "source": "WHATWG HTML Standard: Canvas",
      "url": "https://html.spec.whatwg.org/multipage/canvas.html",
      "load_bearing_rule": "Interactive canvas regions should map one-to-one to focusable fallback-content controls."
    },
    {
      "source": "WCAG 2.2",
      "url": "https://www.w3.org/TR/WCAG22/",
      "load_bearing_rules": [
        "2.1.1 Keyboard",
        "2.1.2 No Keyboard Trap",
        "2.2.2 Pause, Stop, Hide",
        "2.4.3 Focus Order",
        "2.4.7 Focus Visible",
        "2.4.11 Focus Not Obscured",
        "2.5.7 Dragging Movements",
        "2.5.8 Target Size (Minimum)"
      ]
    },
    {
      "source": "WAI: Animation from Interactions",
      "url": "https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions",
      "load_bearing_rule": "Non-essential interaction-triggered motion must be disableable; reduced-motion preferences are an accepted mechanism."
    },
    {
      "source": "MDN: prefers-reduced-motion",
      "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-motion",
      "load_bearing_rule": "The reduce preference calls for removing, reducing, or replacing non-essential motion; large-scale panning and scaling can be motion triggers."
    }
  ],
  "interaction_findings": [
    {
      "interaction": "pan/zoom",
      "user_job": "Inspect spatially separated rooms without losing current location.",
      "evidence_class": "operability and state-continuity hypothesis",
      "standards": ["WCAG 2.1.1", "WCAG 2.5.7", "WCAG 2.3.3"],
      "browser_witness": "Keyboard and click/tap controls produce the same bounded camera transform as dragging or wheel input; reset restores the canonical view; reduced-motion mode makes transform changes immediate or substantially reduced; focus remains visible and outside the canvas trap.",
      "human_or_at_witness": "Keyboard-only, switch/speech-input, magnification, and vestibular-comfort sessions; comprehension or place-memory benefit requires a comparative human study.",
      "failure_mode": "Drag/wheel-only navigation, focus loss, unbounded zoom, parallax or animated camera movement under reduced motion, or camera state hiding the semantic evidence surface.",
      "disposition": "EXPERIMENT"
    },
    {
      "interaction": "floor focus",
      "user_job": "Choose a floor and understand which floor is active.",
      "evidence_class": "navigation parity",
      "standards": ["WCAG 2.1.1", "WCAG 2.4.3", "WCAG 3.2.1"],
      "browser_witness": "A named DOM control activates each floor; active state is programmatically exposed; activation, not mere focus, changes the view; returning preserves a coherent focus target.",
      "human_or_at_witness": "Screen-reader announcement and zoom/reflow review; any claim that spatial floors improve recall requires human comparison.",
      "failure_mode": "Canvas color or coordinates are the only active-state cue, focus alone changes context, or floor selection diverges from the semantic DOM state.",
      "disposition": "KEEP"
    },
    {
      "interaction": "room entry",
      "user_job": "Open one room’s evidence and return without losing context.",
      "evidence_class": "focus and continuity contract",
      "standards": ["WCAG 2.1.1", "WCAG 2.4.3", "WCAG 2.4.11", "WCAG 3.2.1"],
      "browser_witness": "Every hit-tested room has a one-to-one DOM control; explicit activation opens it; focus moves predictably to the room heading or dialog and returns to the invoker; unknown room IDs fail closed.",
      "human_or_at_witness": "Screen-reader, keyboard-only, magnifier, and cognitive walkthrough of enter/return orientation.",
      "failure_mode": "Pointer-only hit region, invisible focus, unexpected context change on focus, stale room/evidence mismatch, or lost return position.",
      "disposition": "KEEP"
    },
    {
      "interaction": "robot movement",
      "user_job": "Perceive decorative world activity or actor state without confusing it with evidence or worker execution.",
      "evidence_class": "presentation experiment only",
      "standards": ["WCAG 2.2.2", "WCAG 2.3.3"],
      "browser_witness": "Motion can be paused/stopped; reduced-motion mode freezes or replaces locomotion; robot state is labelled decorative and never changes evidence, authority, or worker-execution state.",
      "human_or_at_witness": "Vestibular-comfort and distraction testing. Claims about comprehension, trust, motivation, productivity, learning, or research quality require direct human evidence.",
      "failure_mode": "Continuous unpausable movement, motion under reduce preference, status conveyed only through animation, or decorative avatars described as autonomous agents.",
      "disposition": "EXPERIMENT"
    },
    {
      "interaction": "evidence hotspots",
      "user_job": "Locate and open evidence-bearing objects.",
      "evidence_class": "core evidence-navigation parity",
      "standards": ["WHATWG canvas fallback mapping", "WCAG 2.1.1", "WCAG 2.4.7", "WCAG 2.5.8"],
      "browser_witness": "Each hotspot maps one-to-one to a named focusable DOM control, supports keyboard activation, has visible focus, provides at least a 24-by-24 CSS-pixel target or qualifying spacing/equivalent control, and resolves the same exact evidence identifier.",
      "human_or_at_witness": "Screen-reader naming/order, touch target usability, magnification, and keyboard traversal.",
      "failure_mode": "Canvas-only coordinates, small crowded targets, hover-only disclosure, source-ID divergence, or a hotspot implying evidence/authority merely through presentation.",
      "disposition": "KEEP"
    },
    {
      "interaction": "minimap",
      "user_job": "Understand current viewport location and jump to known places.",
      "evidence_class": "orientation hypothesis",
      "standards": ["WCAG 1.1.1", "WCAG 2.1.1", "WCAG 2.5.8"],
      "browser_witness": "Minimap location has a textual equivalent; jump targets are named and keyboard-operable; target activation synchronizes camera and DOM state; hiding the minimap removes no unique function.",
      "human_or_at_witness": "Low-vision, screen-reader, and cognitive wayfinding study; claimed place-memory improvement needs comparative human evidence.",
      "failure_mode": "Color/position-only orientation, tiny targets, pointer-only jumps, or minimap becoming the sole route to content.",
      "disposition": "EXPERIMENT"
    },
    {
      "interaction": "DOM inspector overlay",
      "user_job": "Read exact evidence and operate controls independently of the world renderer.",
      "evidence_class": "mandatory semantic fallback and source-of-truth boundary",
      "standards": ["WHATWG canvas fallback mapping", "WCAG 2.1.1", "WCAG 2.4.3", "WCAG 2.4.11"],
      "browser_witness": "Overlay remains usable when canvas initialization fails or is disabled; canvas and DOM selections share one typed intent/state bridge; all evidence text, source binding, refusals, and controls remain in semantic DOM; focus is preserved when toggling.",
      "human_or_at_witness": "Screen-reader, keyboard-only, zoom/reflow, high-contrast, and reading-order review.",
      "failure_mode": "Overlay duplicates or drifts from evidence state, becomes inaccessible behind canvas layers, loses focus, or is treated as optional decoration.",
      "disposition": "KEEP"
    }
  ],
  "architecture_constraints": [
    "Keep the semantic DOM as the evidence and control plane; canvas is a disposable spatial projection.",
    "Provide one-to-one DOM controls for interactive canvas regions and synchronize both surfaces through typed navigation intent.",
    "Provide keyboard and single-pointer alternatives to drag-based camera behavior.",
    "Honor prefers-reduced-motion and add a persistent pause/stop mechanism for continuing robot motion.",
    "Retain the existing textual interface as the initialization-failure and no-canvas fallback.",
    "Do not infer WCAG conformance from automated tests."
  ],
  "claim_ceiling": "The evidence supports finite browser-observable operability requirements and a testable experiment design. It does not prove accessibility conformance, usability, spatial cognition, place-memory improvement, comprehension, learning, trust, motivation, productivity, or research quality.",
  "recommended_first_slice": "KEEP room entry, floor focus, evidence hotspots, and the DOM inspector overlay. EXPERIMENT with bounded pan/zoom and one decorative robot only under keyboard, single-pointer, pause, reduced-motion, failure-fallback, and exact state-parity controls. Defer the minimap until human wayfinding need is demonstrated.",
  "receipt_output": "Return supplied to parent for persistence at receipts/explorer-human-interface.json."
}
```

## Explorer integration — spawn-0003

```json
{
  "receipt_version": "host-native-action.v1",
  "action_id": "spawn-0003",
  "role": "explorer-integration",
  "capability": "domainspec-subagents-strategy",
  "target": "dispatch-sheet.json#groups/explorers/agents/2",
  "mode": "research-explore",
  "status": "completed",
  "mutation_policy": "read-only",
  "mutations": [],
  "output_ref": "receipts/explorer-integration.json",
  "output_persistence": "returned-to-parent; not written because write scope is empty",
  "input_binding": {
    "dispatch_id": "2026-08-10-cyberalchemy-game-canvas-interface",
    "confirmation_handle": "user-confirmation-25928ddf4471",
    "dispatch_sheet_sha256": "25928ddf447105cbd2ba307c6295f89c57bdb7b33a2b8b8b15fa0e4efe91f296"
  },
  "verified_byte_bindings": {
    "projects/ide-extension/public/demo/research-tower.html": "255f0e351b836bb13523ad2e71ff4ca39fa2ffdb421139e9e718d69b94885e23",
    "projects/ide-extension/src/research-tower/l0-witness.mjs": "48d0124ef75b81f72be6efcddfe470da3cfdfd10a30228f7c361ec54783ce3ee",
    "projects/ide-extension/tests/research-tower-explorer.test.mjs": "deb805149f862eed79b7f8dd74817866ed55dde1dd502d045f07d876994a7561",
    "projects/ide-extension/tests/e2e/research-tower-explorer.spec.mjs": "5b1c2ad24040615051b783f20d775cc753e765efb7eac05413753ba5b6fb89e9",
    "projects/ide-extension/public/assets/research-tower-concepts/robot-cowork-rpg-sprite-sheet.png": "04fa18bb405b59380b4be2b5a88bebd88632837e1fd21467e626832f43e37afa"
  },
  "findings": {
    "compatibility_verdict": "KEEP a hybrid world-view spike only if the existing semantic DOM remains the evidence and control plane. The canvas must be a disposable navigation projection, never the witness, evidence, worker, or authority source.",
    "current_runtime": {
      "delivery": "Private ESM Node application. The page is served at GET /demo/research-tower; its sole data dependency is GET /api/research-tower/l0.",
      "dependencies": "package.json contains ajv and parse5, with Playwright as development tooling. No Phaser, PixiJS, Excalibur, or Anime.js runtime is installed.",
      "assets": "Concept assets are served through an explicit RESEARCH_TOWER_ASSETS allowlist under /assets/research-tower-concepts/. Unknown asset names return 404.",
      "csp_boundary": "The current page uses a large inline type=module script. No research-tower-specific CSP contract was found in the inspected route. A later strict script-src policy would require extracting the module or binding an exact nonce/hash; an engine must not require CDN or dynamic remote loading."
    },
    "preserved_invariants": [
      "scene_manifest and VerificationPromptProjection remain derived from the locked witness and retain exact floor identity.",
      "VerificationPromptProjection remains display-only with executable:false.",
      "SourceBindingRef failure states remain visible; ordinary combined claims stay suppressed on object_unavailable, path_missing, or digest_mismatch.",
      "System interactions remain refusal-only and create no endpoint, non-GET request, workflow, score, verdict, promotion, or authority effect.",
      "Floor, room, inspection, relation-filter, source/candidate, and focus continuity survive System entry and return.",
      "Unknown scene identities fail closed before presentation.",
      "Unknown or failed decorative media produces no substituted request and leaves textual evidence usable.",
      "API or post-construction render failure rolls back to the same disabled, media-free, non-animated surface.",
      "Reduced motion preserves content and state while stopping animation.",
      "The textual surface remains independently operable by native buttons, select controls, focus management, polite status announcements, and narrow-layout reflow."
    ],
    "proposed_module_boundaries": [
      {
        "module": "src/research-tower/world-contracts.mjs",
        "owns": "Pure validation and types for LabWorldManifest, LabWorldState, WorldIntent, CameraState, RobotAvatar, HotspotRef, and failure codes.",
        "must_not_own": "Witness loading, evidence truth, worker execution, or authority effects."
      },
      {
        "module": "src/research-tower/world-projection.mjs",
        "owns": "Pure mapping from validated scene_manifest plus current semantic selection into disposable render entities and hotspots.",
        "must_not_own": "Independent evidence records or duplicate VerificationPromptProjection generation."
      },
      {
        "module": "public/demo/research-tower-world.mjs",
        "owns": "Renderer lifecycle, camera transform, deterministic avatar stepping, hit testing, resize, visibility, and reduced-motion response.",
        "must_not_own": "Fetches other than the existing admitted witness path, source resolution, or DOM evidence rendering."
      },
      {
        "module": "public/demo/research-tower-bridge.mjs",
        "owns": "Typed translation between WorldIntent and existing semantic controls; DOM state is reflected back into LabWorldState after the existing transition succeeds.",
        "must_not_own": "Direct evidence mutation or synthetic click behavior that bypasses control laws."
      },
      {
        "module": "tests/research-tower-world.test.mjs",
        "owns": "Pure projection, reducer, bounds, unknown-ID, and rollback tests."
      },
      {
        "module": "tests/e2e/research-tower-world.spec.mjs",
        "owns": "Canvas/DOM synchronization, keyboard parity, reduced motion, failure fallback, request ceiling, focus continuity, narrow layout, and frame/input witnesses."
      }
    ],
    "typed_state_contract": {
      "LabWorldManifest": "Versioned projection containing only known floor scene IDs, bounded world coordinates, local admitted asset IDs, hotspot-to-floor mappings, deterministic avatar spawn/path data, and no evidence payload.",
      "LabWorldState": "renderer_status, active_floor_id, room_open, camera{x,y,zoom}, avatar{id,position,facing,presentation_state}, hovered_hotspot_id, reduced_motion, document_visibility, last_committed_semantic_state, failure.",
      "WorldIntent": "PanCamera | ZoomCamera | SelectHotspot(floor_id) | MoveAvatar(target) | ResetView. Intents request navigation only.",
      "RobotAvatar": "Decorative deterministic presentation entity. It has no prompt, task, transport, tool, receipt, worker identity, or authority field.",
      "HotspotRef": "Known manifest ID plus floor_id/control_ref. It contains no evidence claim.",
      "authority_effect": "Always none at the world layer."
    },
    "event_flow": [
      "Pointer, keyboard, or controller input produces a validated WorldIntent.",
      "The world reducer rejects unknown IDs and clamps camera/avatar bounds without touching evidence state.",
      "SelectHotspot resolves to a known existing semantic floor control.",
      "The bridge requests the same existing floor/room transition used by native DOM controls.",
      "Only after that transition commits does the renderer mirror active_floor_id and room_open.",
      "Existing DOM code renders scene_manifest, source bindings, verification projection, residue, and System refusals.",
      "Failure at any renderer or bridge stage stops the world, preserves or restores last_committed_semantic_state, announces the fallback, and leaves the textual controls usable."
    ],
    "finite_first_playable_slice": {
      "scope": "One L0 room only, one bounded world transform, one deterministic decorative robot, and one evidence hotspot mapped to the existing L0 floor control.",
      "required_witnesses": [
        "Camera pan/zoom changes only world transform and does not alter evidence selection.",
        "Robot moves deterministically within declared bounds; it never crosses an inaccessible wall or implies execution.",
        "Hotspot activation selects L0 through the semantic bridge and produces the same VerificationPromptProjection as the native floor button.",
        "Native DOM activation updates the world hotspot and camera focus without a second source of truth.",
        "Unknown hotspot or manifest scene fails closed with zero selection change.",
        "Renderer initialization failure removes or disables only the world layer and preserves the current textual tower.",
        "Reduced motion disables continuous/decorative movement while retaining direct hotspot navigation.",
        "No external request and no non-GET request occurs.",
        "Keyboard users can reach the equivalent native DOM controls without entering the canvas.",
        "System refusal/return preserves both semantic continuity and disposable camera/avatar presentation state where safe."
      ],
      "asset_boundary": "The existing 2172x724 four-tableau image is not a walking sprite. The slice must use a separately admitted local sprite contract or a simple geometric/avatar placeholder; it must not relabel the current tableau as gait animation."
    },
    "performance_budget_proposal": {
      "bundle": "Keep the spike as one locally served, pinned module chunk; record compressed and uncompressed size before accepting an engine dependency.",
      "frame": "Target p95 frame duration <=16.7ms during active input on the declared reference Chromium, with <=33.3ms as a fail threshold for the tiny L0 slice.",
      "input": "Target p95 input-to-visible-world response <=100ms.",
      "idle": "Stop requestAnimationFrame when hidden, world-disabled, System view is active, or no animation/update is needed.",
      "entities": "Bound the first slice to one avatar, one room, and a small fixed hotspot set; no physics or pathfinding library.",
      "layout": "Canvas backing resolution follows device pixel ratio under an explicit cap; CSS sizing must preserve the existing 390x844 and 320x568 no-horizontal-overflow contract."
    },
    "test_extension": [
      "Retain all existing Node and 20-case desktop/mobile E2E coverage unchanged.",
      "Add pure reducer tests for deterministic replay, clamping, unknown IDs, reduced motion, and rollback.",
      "Assert canvas actions and native DOM actions converge on identical active floor, room, verification, focus, and announcement state.",
      "Assert exact zero external and non-GET requests on success and all negative controls.",
      "Inject engine initialization, asset, context-loss, stale-manifest, and bridge failures.",
      "Measure frame duration, input latency, long tasks, canvas backing size, and idle RAF cessation.",
      "Repeat exact 390x844 and 320x568 containment checks with the world enabled and disabled.",
      "Preserve manual residue for screen readers, zoom, motion comfort, comprehension, and accessibility conformance."
    ],
    "killed_or_deferred": [
      "KILL canvas as evidence source or replacement for semantic DOM.",
      "KILL autonomous-agent terminology for RobotAvatar.",
      "KILL external CDN loading and runtime-generated remote assets.",
      "KILL physics/pathfinding in the first slice.",
      "DEFER multi-room tilemaps, autonomous workers, worker visualization, minimap, persistence, and authoritative world state.",
      "DEFER dependency installation until the external runtime comparison binds exact version, license, bundle, module, and offline evidence."
    ]
  },
  "claim_ceiling": "This receipt establishes a read-only compatibility map and finite prototype contract against exact candidate-local bytes. It does not select an engine, authorize implementation or dependency installation, establish accessibility or human benefit, reconcile lifecycle state, or prove release, deployment, or production readiness."
}
```
