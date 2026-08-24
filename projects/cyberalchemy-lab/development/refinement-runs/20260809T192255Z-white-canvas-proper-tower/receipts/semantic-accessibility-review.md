# Semantic and accessibility review receipt

## Identity

- Action: `spawn-0002`.
- Dispatch: `20260809T192255Z-white-canvas-proper-tower`.
- Run / wave / step: `review-run-001` / `white-canvas-review` / `s03-review`.
- Role / capability / mode: `semantic-accessibility-reviewer` / `interrogation` / `refine-review`.
- Mutation and authority effect: none.
- Receipt completeness: pass.
- Target-design verdict: `block` until P0 wording, binding, refusal, and validator requests are incorporated.

## Wording repairs

- Keep “proper tower” internal. User-facing identity: **Synthetic evidence tower — contract fixture, not representative**.
- Replace “one selected tower” with **one preloaded synthetic fixture**.
- Prefix every visible level name with **Evidence floor** and show its `evidence-*` ID as secondary text.
- Replace “L0 corpus” with **Evidence floor 1 of 3 — Synthetic corpus anchors**.
- Replace “L2 closure” with **Evidence floor 3 of 3 — Closure plan, blocked**.
- Replace “Witness verified” with **Locked synthetic witness loaded** and name the validation scope separately.
- Limit “available” to **available for read-only navigation**.
- Label the separate region **Tower System reference — capabilities unavailable in this Lab**.
- Remove the class-only “Focus tower” control or make it actually move keyboard focus with accurate wording.
- Replace subjective/usability claims with observable exposure and viewport criteria; comprehension remains future human-study evidence.

## Required floor bindings

Each control and associated detail exposes exact ID, human label, evidence state, implementation status, sources, claim ceiling, and blocker/refusal where required.

1. `evidence-l0-corpus`: “Evidence floor 1 of 3 — Synthetic corpus anchors”; `locked-synthetic`; `candidate-local`; sources `source:toy:readme`, `source:toy:tower`, `source:toy:l0`; exact view ceiling; explain that locks verify fixture bytes, not corpus coverage or representativeness.
2. `evidence-l1-residue`: “Evidence floor 2 of 3 — Open representative-selection residue”; `open`; `candidate-local`; sources `source:toy:l1`, `source:toy:residue`; residue question and blocked claims/gates; exact ceiling; never appear complete.
3. `evidence-l2-closure`: “Evidence floor 3 of 3 — Closure plan, blocked”; `blocked`; `candidate-local`; sources `source:toy:l2`, `source:toy:gates`; exact ceiling; explicit reason that no representative source is selected and this view cannot select one or run a workflow.

The current manifest validator must be hardened in the future implementation because it does not require each scene's `implementation_status`, does not enforce scene/tower/view ceiling equality, and permits a blocked scene with `unavailable_reason: null`.

## System refusal contract

System descriptors remain outside the evidence-floor group in a separately labelled landmark. Controls stay enabled so their explanations are reachable. Activation:

- retains focus on the System button;
- clears every evidence-floor `aria-pressed` state;
- selects only the matching System explanation;
- announces `Unavailable in this Lab`, exact implementation status, refusal reason, evidence locator, and claim ceiling;
- causes no POST, persistence, execution, scoring, verdict, promotion, or authority effect.

The five source states remain precise: L1 graph/personas unwitnessed; L2 precedent exists but no live builder; L3 precedent exists elsewhere but no live Tower operation; Lphi is design-stage/unproven with zero live MOGT runs; L4 has partial governance precedent but no Lab ELO/oracle runtime or verdict emission. Replace pseudo-selectors such as `SYSTEM-VIEW.md#L1` with stable source selectors or exact digest/line evidence before presenting them as inspectable links.

## Accessibility acceptance criteria

### Keyboard and focus

- Native buttons in DOM order; Enter/Space activation; activation retains focus.
- Text plus `aria-pressed`, never color alone.
- Every selector has `aria-controls` to the shared detail region.
- Reset activates and focuses `evidence-l0-corpus`.
- Focus indicators meet 3:1 adjacent-color contrast and are not clipped.
- Source/candidate/relation interactions work repeatedly; remove `{ once:true }` from repeatable listeners.

### Screen reader

- Named tower region with heading and ordered three-item floor structure.
- Accessible names include floor number, subject, and state.
- One `role="status" aria-live="polite" aria-atomic="true"` announces selection/state/status/refusal.
- Shared detail uses the active control for `aria-labelledby`.
- Spine/guides are `aria-hidden="true"` and carry no exclusive information.
- Loading, locked-synthetic readiness, and unavailable/error remain distinct.
- Manual screen-reader/browser matrix remains required; automation alone is not proof.

### Mobile/reflow

- At 320×568 and 390×844: tower identity, floors, detail, System reference, source/relation/residue inspection.
- Normal scrolling, no absolute/fixed dock overlap, >=44×44px controls, no horizontal overflow.
- At 200%/400% zoom, labels, state, refusal, and focus remain visible without two-dimensional scroll.

### Reduced motion and visual contrast

- Under reduced motion, animations use `animation-name: none` and transitions are removed; do not retain the `.01ms` workaround.
- Selection/content/focus/refusal behavior remains identical.
- Prefer no continuous motion.
- Normal text >=4.5:1; large text, meaningful borders, focus, and state marks >=3:1 where applicable.
- Open, blocked, unavailable, selected, and candidate-local are explicit text states.

## Negative controls

- Reject System IDs inside the floor list and evidence IDs inside the System list.
- Reject bare L0/L1/L2 or “closure” as complete accessible names.
- Reject missing implementation status, sources, exact ceiling, or required blocker reason.
- Reject scene ceiling mismatch and unresolved System evidence selectors.
- System activation leaves zero floors pressed and makes no non-GET request.
- Open/blocked floors never say verified, complete, or capability available.
- Assert the absence of scenic/veil/lab/robot/rotating-image elements and “Decorative cowork loop.”
- Exercise repeated relation and candidate/source interactions.
- Cover initial, floor, System refusal, loading-error, mobile, and reduced-motion states.
- Human comprehension remains unverified without a separate study.

## Severity and reroute

- P0: repair wording; bind every floor; make refusal separate/focus-stable/announced/evidence-bound; harden manifest invariants; remove class-only focus; explicitly remove old animated composition and its tests.
- P1: verify palette contrast; define semantic relationships/live region; normal-flow reflow/zoom; true reduced motion; repeatable listeners; manual screen-reader/browser matrix.
- P2: floor N-of-3 secondary text, hidden CSS spine, no automatic motion by default, restrained validated accents.

Sources: current Define, Inventory packet, manifest, page, Node/E2E tests, prior Refine result, Tower System view, and foundation findings. No runtime/browser validation occurred. Real tower selection, human comprehension, accessibility conformance, responsive behavior, and Tower System runtime capabilities remain open or unproven. Return to parent Refine for definition/design repair; do not route to implementation or lifecycle effects.
