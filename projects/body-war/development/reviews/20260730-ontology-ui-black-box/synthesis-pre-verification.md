# Body War ontology UI black-box synthesis

## Decision

Use a **bounded hybrid** as the first focus rule:

- For a node assigned to a tour step, use that existing four-node tour scene.
- For a node outside every tour step, use a deterministic one-hop neighborhood.
- Represent every relation crossing the current boundary as a labeled, directed portal.

This is the narrowest source-preserving hypothesis. The five tour steps are the only explicit small groups in the frozen presentation graph; their 20 nodes and 11 cross-scene relations make them feasible seeds. They are not proven sufficient for comprehension. One-hop is therefore a fallback, not the universal first unit. A type layer is rejected because the 17 layers classify kinds and may remain large; it is not a reader journey or semantic branch. The hybrid remains removable UI projection data: all 237 nodes carry `branch:business`, so no additional ontology branch may be inferred.

## Preserved disagreements and useful existing behavior

- The cold-reader successfully found `SuggestedTrack`, followed `→ builds on TerritoryUnit`, and recovered `authority:none` through search and the detail panel. This proves a reachable inspector path, not graph comprehension.
- The branch attack found the same inspector pattern useful—breadcrumb, Back, directed relation wording, and authority tag—but showed that it never bounded the 237-node/231-edge canvas.
- Candidate/status wording survives without color in parts of the interface. Selection, active relation, node kind at overview scale, and visible direction do not. Preserve the textual status cue; do not claim the overall encoding is color-independent.
- Current tested interactions had zero active animations under reduced motion. That is a present-state zero finding; the absent focus-scene transition remains untested.
- Four-node tour scenes are the safest explicit grouping available, but no automated evidence shows that four nodes preserve enough meaning for a human.

## Candidate UI change requests

### CR-1 — Atomic focus scene and portal pivot

- **Severity/loci:** High; locate, trace, retell, distinguish.
- **Evidence:** Tour step 1 named four components while DOM counts remained 237 nodes and 231 edges; it exposed zero persistent edge labels. Non-tour `Focus` also left both counts unchanged. See `branch-pivot/measurements.json`.
- **Repair:** Atomically render the bounded-hybrid scene and expose every crossing relation as a labeled directed portal.
- **Browser assertion:** A tour scene contains exactly its four admitted `nodeIds`, admitted internal relations, and all crossing portals; repeated non-tour Focus yields the same sorted one-hop node/edge/portal set and excludes unrelated nodes.
- **Accessibility/motion:** Announce scene heading and node/portal counts; portals are keyboard-operable; reduced motion replaces the scene immediately without rotation.
- **Semantic/authority constraint:** Scene membership, portal status, position, and rotation create no causal, temporal, execution, promotion, or authority meaning.
- **Human ceiling:** Proves deterministic projection structure only, not scene sufficiency or comprehension.

### CR-2 — Keyboard navigation and visible focus

- **Severity/loci:** High; locate, trace, distinguish.
- **Evidence:** Search was tab stop 10, followed by the freshness notice and the 231-edge sequence; fifteen tested edge groups had no visible outline. Connection rows were generic `DIV`s without role or `tabindex`.
- **Repair:** Add skip-to-selected-detail plus graph-level/roving focus, with forced-colors-safe focus treatment.
- **Browser assertion:** After exact-result selection, heading, authority cues, and first relation are reachable within five Tabs; each active graph item has nonzero visible focus geometry; every portal supports Enter/Space equivalently to pointer activation.
- **Accessibility/motion:** Focus and announcements survive default, grayscale, forced colors, and reduced motion without animation as the sole cue.
- **Semantic/authority constraint:** Keyboard affordances expose only admitted nodes and relations.
- **Human ceiling:** Establishes reachability and visible focus, not workload or understanding.

### CR-3 — Persistent selected-relation state

- **Severity/loci:** High; trace, retell, boundary.
- **Evidence:** Activating the tested graph relation left the graph and Project Tour panel visually unchanged; direction existed only in the accessible edge name. Inspector traversal separately showed that visible relation wording, breadcrumb, Back, and `authority:none` can work.
- **Repair:** Preserve a selected source–label–direction–destination panel, breadcrumb/back stack, source reference, and authority cues across every pivot.
- **Browser assertion:** Pointer or keyboard activation sets programmatic selection, displays the exact relation tuple, increments stack depth, and replaces the scene while retaining source and authority surfaces.
- **Accessibility/motion:** Announce tuple, destination, and depth; show a non-color border/shape cue in forced colors; reduced motion updates immediately.
- **Semantic/authority constraint:** Display the admitted relation wording; do not paraphrase it into cause, time, execution, or promotion.
- **Human ceiling:** Proves stable rendered state, not semantic correctness beyond source.

### CR-4 — Atomic tour/context state

- **Severity/loci:** Medium; trace, retell, boundary.
- **Evidence:** Advancing from tour step 1 to step 2 retained the prior `Authentication and Consent` inspector, creating mixed step and selection context. Starting the tour also displaced the active `SuggestedTrack → TerritoryUnit` trace.
- **Repair:** On step change, reset to the new scene or retain prior state only as explicitly labeled history/portal context.
- **Browser assertion:** No out-of-scene selection remains after a step change unless represented in breadcrumb history or as a portal; tour enter/exit preserves the prior trace state.
- **Accessibility/motion:** Announce context reset or preservation; keyboard and reduced-motion paths produce identical state.
- **Semantic/authority constraint:** Tour order must not imply workflow, causality, lifecycle, or promotion.
- **Human ceiling:** State coherence does not prove the tour tells the right story.

### CR-5 — Redundant kind/status vocabulary

- **Severity/loci:** Medium; distinguish, vocabulary, boundary.
- **Evidence:** Exact search ranked `claim SuggestedTrack 100%` while detail showed `business-kind:entity`; forced colors collapsed overview cards to uniform rectangles without persistent kind labels. Existing candidate/status phrases remained textual.
- **Repair:** Use source-derived kind and lifecycle posture consistently in search, cards, detail, and accessible names, paired with non-color icon/shape/border cues.
- **Browser assertion:** Exact-name search ranks one exact node first; result kind equals visible detail kind; every visible node exposes kind in text and accessible name with authored colors suppressed.
- **Accessibility/motion:** Cues survive grayscale, forced colors, keyboard focus, and reduced motion.
- **Semantic/authority constraint:** Preserve admitted tags such as `authority:none` and candidate status; recommend semantic color roles only—no unmeasured palette tokens.
- **Human ceiling:** Proves vocabulary consistency and redundant rendering, not correct interpretation, promotion, release, deployment, or production readiness.
