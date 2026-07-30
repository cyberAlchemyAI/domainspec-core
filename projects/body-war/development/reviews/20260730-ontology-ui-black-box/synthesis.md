# Body War ontology UI black-box synthesis

## Decision and boundary

Use a **bounded hybrid UI projection**:

- Nodes in a tour use the source-derived four-node tour scene.
- Nodes outside tours use a deterministic one-hop neighborhood.
- Boundary-crossing relations become labeled, directed portals.
- Type layers remain filters, not focus units or reader journeys.

Tour membership, neighborhoods, portals, position, and motion are removable UI state—not ontology branches or semantic authority. The review remains read-only and establishes structural browser behavior only.

## Preserved tensions

- Search and inspector traversal provide a successful route to `SuggestedTrack`, breadcrumb, relation wording, and `authority:none`; they do not make the 237-node graph comprehensible.
- Existing candidate-status text is useful, but selection, relation direction, and overview node kind are not consistently recoverable without color.
- Existing static reduced-motion interactions showed zero active animations; the proposed pivot remains untested.
- Four-node tours are the smallest explicit source groups, but their sufficiency for human understanding is unproved.

## CR-1 — Exact bounded-hybrid projection

- **Severity/loci:** High; locate, trace, retell, distinguish.
- **Evidence:** Tour step 1 retained 237 nodes, 231 edges, and zero persistent labels; non-tour `Focus` also remained 237/231.
- **Repair:** Replace the whole graph atomically with the admitted tour scene or deterministic non-tour one-hop fixture plus directed portals.
- **Deterministic assertion:** First assert that the frozen whole-graph behavior fails at 237/231. Maintain test-owned, source-derived fixtures independent of the projection implementation for:
  - named tour fixture `Business capability map`;
  - named non-tour fixture `Authentication and Consent`;
  - exact sorted node-ID arrays;
  - exact internal-edge and portal arrays;
  - one fixed, source-verified unrelated node ID that must be absent.

  Every relation tuple pins source, target, direction, generic `type`, relation-local `description`, and both endpoints’ `filePath` provenance. Rendered nodes retain admitted `branch:business`, `candidate-status:*`, and `authority:none`.
- **Accessibility/motion:** Announce the scene name, node count, and portal count; reduced motion performs the identical replacement immediately.
- **Semantic/authority constraint:** Fixture generation reads frozen source bytes; scene membership and portal classification add no ontology, causal, temporal, execution, promotion, release, or authority meaning.
- **Human ceiling:** Exact arrays prove deterministic projection only, not that either focus rule supports human comprehension.

## CR-2 — Named focus destination and complete activation parity

- **Severity/loci:** High; locate, trace, distinguish.
- **Evidence:** Search was tab stop 10; traversal entered graph edges after stop 13. Fifteen sampled relations had no visible outline, and connection rows were non-focusable `DIV`s.
- **Repair:** Provide an explicit skip/selection route to a named detail landmark, roving or graph-level navigation, and visible non-color focus geometry.
- **Deterministic assertion:** Exact-result selection or the skip control moves focus to the named detail landmark; its accessible text contains the exact node heading and admitted authority tag. The first relation control is reached within a pinned Tab count. Every pivot-capable node, relation, and portal must support pointer, Enter, and Space with byte-equivalent serialized scene membership, relation tuple, breadcrumb depth, provenance, status, authority, and reduced-motion result.
- **Accessibility/motion:** Each active control has nonzero computed outline or border geometry in default, grayscale, forced-colors, and reduced-motion modes. No contrast-compliance claim is made without measurement.
- **Semantic/authority constraint:** Navigation exposes admitted state only and cannot manufacture missing relation or lifecycle meaning.
- **Human ceiling:** Establishes focus movement, operability, and parity—not workload or understanding.

## CR-3 — Literal, provenance-bearing selected relation

- **Severity/loci:** High; trace, retell, boundary.
- **Evidence:** Graph-edge activation left the graph and Tour panel visually unchanged, while inspector traversal preserved breadcrumb, Back, visible direction wording, and `authority:none`.
- **Repair:** Persist a selected-relation surface and use the literal fixture `Identity and Consent —related to→ Authentication and Consent`.
- **Deterministic assertion:** The fixture pins the frozen edge’s exact source ID, target ID, direction, generic `type`, relation-local `description`, source and target `filePath`, statuses, and authority tags. Activation must produce exact tuple text, a programmatic selected-state attribute, breadcrumb array, stack depth, destination heading, source surfaces, authority surfaces, and destination-scene replacement. Pointer, Enter, and Space yield byte-equivalent serialized semantic state.
- **Accessibility/motion:** Announce both endpoints, displayed predicate, direction, and stack depth; selected state has a non-color cue; reduced motion updates immediately.
- **Semantic/authority constraint:** The UI must distinguish generic type from relation-local description and identify which supplies the displayed predicate. It may not paraphrase either into cause, time, execution, promotion, release, or authority.
- **Human ceiling:** Proves stable source-consistent UI state only.

## CR-4 — Atomic active tour state with separate restoration state

- **Severity/loci:** Medium; trace, retell, boundary.
- **Evidence:** Step 1→2 retained stale `Authentication and Consent`; tour entry displaced the active `SuggestedTrack → builds on → TerritoryUnit` trace.
- **Repair:** On tour entry, suspend the pre-tour trace in a separate restoration object and replace active state with the tour scene. Every step change atomically resets active selection to the new scene. Tour exit restores the suspended trace.
- **Deterministic assertion:** Pin and compare exact `preTour`, `enteredTour`, `changedStep`, and `exitedTour` state objects, including active node, selected relation, breadcrumb, portal/history, source, status, and authority fields. After step 2, stale active `Authentication and Consent` is the required negative fixture; it may exist only in separately labeled history/restoration state.
- **Accessibility/motion:** Announce tour entry, step replacement, and restoration; pointer, keyboard, and reduced-motion paths yield identical active and stored state.
- **Semantic/authority constraint:** Tour order is presentation order only—not workflow, causality, lifecycle, execution, or promotion.
- **Human ceiling:** Atomic state does not validate the tour narrative.

## CR-5 — Source-literal vocabulary across every surface

- **Severity/loci:** Medium; distinguish, vocabulary, boundary.
- **Evidence:** Exact search already ranked `claim SuggestedTrack 100%` first, but the detail reported `business-kind:entity`; forced colors removed overview-scale kind differentiation. Ranking is therefore not the defect.
- **Repair:** Render the same admitted literals across search result, card, detail, accessible name, and every pivot destination, supplemented by non-color cues.
- **Deterministic assertion:** For `SuggestedTrack`, every surface matches admitted `business-kind:entity`, `candidate-status:reviewed-candidate`, `authority:none`, and `filePath`. Add a source-derived non-candidate fixture and assert that no lifecycle posture is fabricated when `candidate-status:*` is absent. With authored colors suppressed, kind/status remain present in visible text and accessible names with an icon, shape, or border cue.
- **Accessibility/motion:** Redundant literals and cues survive forced colors, grayscale, keyboard focus, and reduced motion.
- **Semantic/authority constraint:** Semantic color roles may supplement source literals but never replace them. No palette-token or contrast-compliance claim is made.
- **Human ceiling:** Proves source-consistent rendering only—not semantic correctness, comprehension, promotion, release, deployment, or production readiness.

## Repair disposition

- Proxy-validity verifier: `FIX` CR-1 through CR-5; `DROP` none — all requested corrections applied.
- Semantic-authority verifier: `FIX` CR-1 through CR-5; `DROP` none — all requested corrections applied.
- Current disposition: repaired for final writer and parent approval; this is not a claim of implementation or browser acceptance.
