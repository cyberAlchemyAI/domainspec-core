# Body War ontology UI black-box findings

These are structural browser-pretest findings from a read-only projection. They are not evidence of human comprehension, semantic correctness, ontology promotion, release, deployment, or production readiness.

## Three black-box lenses

1. **Cold reader:** Exact search and inspector traversal are possible, but vocabulary differs between search and detail, keyboard access enters a 231-edge sequence, and the tour displaces the active trace.
2. **Color and accessibility:** Keyboard focus is invisible on sampled graph edges; selected relation and direction lack persistent redundant presentation; node kinds collapse under forced colors.
3. **Branch pivot:** Tour steps and Focus do not bound the graph, connection rows are mouse-only, pivoting changes the inspector but not the scene, and tour advancement retains stale selection.

## Severity-ordered change requests

| CR | Severity | Exact failing baseline | Decision |
|---|---|---|---|
| CR-1 | High | Tour step 1 names four nodes but retains 237 nodes, 231 edges, and zero persistent labels; non-tour Focus also remains 237/231. | FIX |
| CR-2 | High | Search is tab stop 10; traversal then enters graph relations, 15 sampled edges have no visible outline, and connection rows are non-focusable `DIV`s. | FIX |
| CR-3 | High | Activating a graph relation leaves graph/tour presentation unchanged and exposes no persistent selected-relation state. | FIX |
| CR-4 | Medium | Step 1→2 retains the out-of-scene `Authentication and Consent` inspector; tour entry displaces the active SuggestedTrack trace. | FIX |
| CR-5 | Medium | Exact search says `claim SuggestedTrack 100%`, while detail says `business-kind:entity`; forced colors removes persistent kind differentiation. | FIX |

### CR-1 — Deterministic focus scenes

- **Focus-scene/color-role contract:** Tour scenes contain exactly frozen `tour[].nodeIds`, admitted internal relations, and every crossing relation as a labeled portal. Non-tour Focus contains the selected node plus a deterministically sorted one-hop neighborhood. Color may supplement, never define, membership or kind.
- **Portal/pivot:** Portal activation atomically replaces the source scene with the destination scene.
- **Breadcrumb/keyboard:** Every portal is a focusable control; scene heading and node/portal counts are announced and breadcrumb history is preserved.
- **Reduced motion:** Perform identical replacement immediately, without rotation.
- **Assertion:** Compare rendered node IDs, internal tuples, and directed portal tuples with test-owned source-derived arrays for one named tour and non-tour fixture; assert a fixed unrelated node is absent and the frozen 237/231 baseline fails.
- **Source/authority:** Preserve source, target, direction, generic `type`, relation-local `description`, endpoint `filePath`, `branch:business`, candidate status, and `authority:none`. Projection geometry conveys no causal, temporal, execution, promotion, release, or authority meaning.
- **Human ceiling:** Exact projection does not prove scene sufficiency or comprehension.

### CR-2 — Keyboard-reachable semantic navigation

- **Focus-scene/color-role contract:** Provide an explicit skip/focus-scene route to a named detail landmark and graph-level or roving navigation. Visible focus must survive forced colors without color as its sole cue.
- **Portal/pivot:** Pointer, Enter, and Space parity covers every pivot-capable node, relation, and portal.
- **Breadcrumb/keyboard:** After exact selection or skip, focus lands on the landmark; its accessible text contains the exact heading and authority tag, and the first relation control is reachable within a fixed Tab count.
- **Reduced motion:** Keyboard activation produces the same immediate semantic state without animated orientation.
- **Assertion:** Verify fixed focus order and nonzero outline/border geometry in default, grayscale, forced-colors, and reduced-motion modes.
- **Source/authority:** Parity includes scene membership, relation tuple, breadcrumb depth, provenance, candidate status, and `authority:none`.
- **Human ceiling:** This proves reachability and visible focus, not workload, comprehension, or contrast compliance.

### CR-3 — Persistent selected relation and atomic pivot

- **Focus-scene/color-role contract:** Expose persistent source, displayed predicate, generic `type`, relation-local `description`, direction, and destination with programmatic selected state plus a non-color-only border/shape cue.
- **Portal/pivot:** Use the literal fixture `Identity and Consent —related to→ Authentication and Consent`; activation replaces the scene and opens the destination.
- **Breadcrumb/keyboard:** Preserve Back, exact breadcrumb array, stack depth, destination heading, and identical pointer/Enter/Space behavior.
- **Reduced motion:** Pivot immediately with the same serialized semantic state.
- **Assertion:** Compare byte-equivalent state containing the tuple, selected attribute, breadcrumb, destination, authority, provenance, and scene membership.
- **Source/authority:** Preserve both `type` and `description`, endpoint paths, statuses, and `authority:none`; paraphrases must not invent stronger meaning.
- **Human ceiling:** Stable selected state does not prove correct interpretation.

### CR-4 — Atomic tour state

- **Focus-scene/color-role contract:** Tour entry suspends the pre-tour trace; each step exclusively owns its active scene. Out-of-scene state appears only as explicitly labeled history or a portal.
- **Portal/pivot:** Step change resets to the new step scene; tour exit restores the suspended trace.
- **Breadcrumb/keyboard:** Pointer and keyboard paths preserve the same explicit history and restoration behavior.
- **Reduced motion:** Entry, step change, and exit update immediately.
- **Assertion:** Pin pre-tour, entered-tour, step-2, and exited-tour state objects; the observed stale `Authentication and Consent` step-2 state must fail.
- **Source/authority:** Authority/provenance fields survive suspension and restoration; tour order is presentation order only.
- **Human ceiling:** Consistent state does not prove workflow, causality, or learning efficacy.

### CR-5 — Source-consistent vocabulary without color dependence

- **Focus-scene/color-role contract:** Search, card, detail, accessible name, and pivot destination expose the same `business-kind`, candidate status, `authority:none`, and `filePath`. Stable text/icon/shape/border cues survive authored-color suppression.
- **Portal/pivot:** Destination vocabulary remains identical before and after every pivot.
- **Breadcrumb/keyboard:** Result and relation accessible names carry the same literals; breadcrumb navigation must not relabel them.
- **Reduced motion:** Vocabulary and redundant cues remain unchanged.
- **Assertion:** `SuggestedTrack` renders `entity`, `reviewed-candidate`, and `authority:none` everywhere; a non-candidate fixture proves lifecycle posture is not fabricated.
- **Source/authority:** All literals come from the admitted source; semantic color roles are supplemental.
- **Human ceiling:** Consistency does not establish semantic correctness or comprehension.

## Disagreements and dropped findings

Both verifiers retain all five CRs; **no CR is dropped**. The following narrower claims are dropped or corrected:

- Exact-first search ranking already passes and is not itself a defect.
- Headings and tags need not be Tab targets; focus should land on a landmark whose accessible text contains them.
- No contrast-compliance claim survives without contrast measurement.
- Zero active animations in current interactions does not validate the absent branch-pivot transition.
- Tour membership is not a semantic branch or proven sufficient meaning unit.
- Rotation semantics remain untested because scene reorientation is not implemented.

## Smallest coherent implementation slice

Implement one frozen four-node tour scene and the literal `Identity and Consent —related to→ Authentication and Consent` portal, including source-derived projection, keyboard/pointer parity, visible forced-colors-safe focus, persistent tuple/provenance/authority state, breadcrumb/Back behavior, atomic scene replacement, and immediate reduced-motion behavior.

The exact next acceptance target is a deterministic black-box test that first reproduces the 237-node/231-edge failing baseline, then matches test-owned node/internal-edge/portal arrays, rejects one fixed unrelated node, and proves byte-equivalent pointer, Enter, Space, and reduced-motion semantic state.

This review neither implements nor authorizes that slice.
