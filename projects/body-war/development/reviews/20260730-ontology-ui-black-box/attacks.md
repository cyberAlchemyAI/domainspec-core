# Body War ontology UI black-box attacks

This file preserves the joined review returns. Runtime credentials are redacted. These are structural browser pretest observations, not human-comprehension evidence and not implementation authority.

## Cold-reader attacker — verbatim review return

> ## Attack A result
>
> Target: `http://127.0.0.1:37037/?token=<redacted-token>`
>
> The page identifies itself as “Body War Business Ontology,” presenting a 17-layer business knowledge graph. A visible freshness warning says the referenced commit is unavailable and cautions against relying on impact or onboarding answers.
>
> First meaningful task action: use the visible search field for `SuggestedTrack`.
>
> Successful black-box path:
>
> 1. Search returned 22 fuzzy results.
> 2. The top result, “claim SuggestedTrack 100%,” opened a detail panel headed `SuggestedTrack`.
> 3. The panel described it as “A runner-visible proposed route awaiting evidence and separate source-backed promotion.”
> 4. Visible tags included `authority:none` and `candidate-status:reviewed-candidate`.
> 5. A relation row exposed `→ builds on TerritoryUnit`.
> 6. Activating it changed the heading to `TerritoryUnit` and retained a `SuggestedTrack › TerritoryUnit` breadcrumb.
>
> Plain-language boundary: SuggestedTrack is a reviewed proposal, not authoritative merely because it is displayed or selected. It still awaits evidence and a separate source-backed promotion.
>
> ## Findings
>
> ### A1 — Search vocabulary contradicts selected-node vocabulary
>
> - Severity: Medium
> - Verdict: `FIX`
> - Surface/evidence: Searching exact text produced 22 results; the exact match was labeled “claim SuggestedTrack 100%,” while its opened detail used `business-kind:entity`.
> - Harm: The mismatch weakens vocabulary and distinguish tasks and creates a credible wrong turn for a cold reader deciding whether the result is a claim or entity.
> - One-line repair: Label results with the rendered ontology kind and lifecycle posture, for example `Entity · SuggestedTrack · reviewed candidate`.
> - Deterministic assertion: Exact-name search ranks one exact node first and its result kind equals the detail panel’s visible `business-kind`.
> - Accessibility/reduced motion: The complete kind and status must be present in the result’s accessible name; no motion is required.
> - Ceiling: This tests consistent rendered vocabulary, not semantic correctness or comprehension.
>
> ### A2 — Keyboard traversal enters 231 graph edges before local semantic navigation
>
> - Severity: High
> - Verdict: `FIX`
> - Surface/evidence: Initial focus order reached Search as stop 10 and the freshness notice as stop 13, then entered individual edge groups. The initial ARIA artifact contains 231 edge groups before the complementary detail surface.
> - Harm: Locate and trace become traversal-scale visual/keyboard search rather than bounded semantic navigation.
> - One-line repair: Add a skip-to-selected-detail/focus-scene route and remove non-local graph edges from ordinary sequential tab order.
> - Deterministic assertion: After selecting an exact search result, keyboard focus reaches its heading, authority cues, and first relation within five Tab presses, without traversing unrelated edges.
> - Accessibility/reduced motion: Focus-scene entry must announce the selected node and preserve labeled directed relations; reduced-motion mode must pivot immediately.
> - Ceiling: This proves focus ordering and reachability only, not human workload.
>
> ### A3 — Tour provides orientation but replaces the local trace task
>
> - Severity: Medium
> - Verdict: `FIX`
> - Surface/evidence: Starting the tour replaced the selected-node panel with `Tour 1 / 5`; step 5 showed “Keep the authority ceiling visible” and four referenced components, but did not retain the active `SuggestedTrack → builds on → TerritoryUnit` relation.
> - Harm: The tour helps high-level boundary vocabulary but interrupts locate/trace/retell continuity.
> - One-line repair: Preserve the active breadcrumb, selected relation label/direction, and candidate-local ceiling beside every tour step.
> - Deterministic assertion: Starting and exiting the tour retains the selected node, breadcrumb, relation direction/label, and authority tags.
> - Accessibility/reduced motion: Step controls and state were accessible; with `prefers-reduced-motion: reduce`, step 4→5 produced zero active animations.
> - Ceiling: The tour’s structure cannot prove that a human understands the authority boundary.
>
> ## Kept evidence
>
> - `KEEP`: The detail panel visibly combines description, file reference, authority/status tags, backlinks, labeled directions, and breadcrumb history.
> - `KEEP`: `→ builds on TerritoryUnit` was actionable and led deterministically to the destination.
> - `KEEP`: Console inspection reported 0 messages, errors, or warnings.
> - `KEEP`: Sanitized network evidence recorded one navigation and 20 resources, including the graph/config fetches.
> - Residue: Human comprehension, trust, retelling accuracy, semantic correctness, promotion, release, deployment, and production readiness remain unproved.
> - Zero-finding defense: Not applicable; three skeptical findings were retained.

## Color and accessibility attacker — verbatim review return

> ## Attack B result
>
> Target: `http://127.0.0.1:37037/?token=<redacted-token>` in fresh isolated headless Chromium, 1440×1000. Console reported 0 errors and 0 warnings; six observed dynamic JSON requests returned 200. Token-bearing traces were deleted after capture; retained evidence contains no token.
>
> Recoverability without color:
>
> - Node kind: not visually recoverable at the fit-view overview under forced colors; cards collapse to uniform white rectangles without persistent textual kind labels or distinct shapes.
> - Current selection: not recoverable for the tested relation.
> - Relation direction: recoverable in the accessibility name (“Edge from … to …”), but not persistently in the visible UI.
> - Candidate status: partially recoverable from textual node names/descriptions such as “Needs Evidence,” “Preview-Accepted,” and “Source-Backed.”
> - Authority meaning: partially represented in text and the tour step “Keep the authority ceiling visible,” but no persistent authority surface appeared when the tested relation was activated. Human understanding remains unproven.
>
> ### B-01 — Invisible keyboard focus inside the graph
>
> - Severity: high; deterministic accessibility failure.
> - Observation: after 13 reachable controls, Tab entered SVG relation groups. Fifteen consecutive tested relation groups had `tabindex="0"` but computed `outline: rgb(245, 240, 235) none 3px`; no focus indicator was visible. The accessibility tree orders the large relation sequence before node content.
> - Harm: keyboard users cannot locate current focus or efficiently trace/distinguish relations.
> - Repair: use roving tabindex or graph-level navigation and add a forced-colors-safe focus ring to every active graph item.
> - Deterministic assertion: each Tab-reachable graph item must expose a visible focus indicator with nonzero outline/border geometry, and node access must not require traversing every relation.
> - Accessibility/reduced-motion assertion: focus must remain visible in default, grayscale, forced colors, and reduced-motion modes without animation being the sole cue.
> - Authority ceiling: proves keyboard presentation failure only, not ontology correctness or human comprehension.
> - Verdict: **FIX**.
> - Evidence: `/tmp/bw-ui-color/keyboard-edge-focus-no-outline.png`, `/tmp/bw-ui-color/page-2026-07-30T04-10-48-052Z.yml`.
>
> ### B-02 — Active relation and direction lack visible redundant state
>
> - Severity: high; deterministic interaction/presentation failure.
> - Observation: activating the exact relation from `attach-activity-evidence-candidate` to `suggested-track` left the graph and right panel visually unchanged. The panel continued showing only Project Tour content. The relation group retained transparent background and `outline-style: none`; direction existed only in its accessibility name.
> - Harm: users cannot locate the active relation, visually trace its direction, or distinguish it from surrounding edges.
> - Repair: persist a selected-relation panel containing source, relation label, arrow/direction, destination, and a non-color-only selected treatment.
> - Deterministic assertion: click or Enter on a relation must expose persistent source/relation/destination text, programmatic selected state, and a visible border/shape cue under grayscale and forced colors.
> - Accessibility/reduced-motion assertion: announce selection and direction; update immediately under reduced motion.
> - Authority ceiling: relation labels may report admitted structure but must not invent causal, temporal, promotion, or execution meaning.
> - Verdict: **FIX**.
> - Evidence: `/tmp/bw-ui-color/active-relation-default.png`, `/tmp/bw-ui-color/active-relation-grayscale.png`, `/tmp/bw-ui-color/active-relation-forced-colors.png`.
>
> ### B-03 — Forced colors removes categorical node-kind differentiation
>
> - Severity: medium; deterministic presentation failure with UX impact.
> - Observation: forced-colors emulation was active. Body presentation computed to black on white, while graph nodes rendered as uniform white cards on a black canvas. No persistent shape/icon/text treatment distinguished the 17 node kinds at overview scale; the top legend was spatially compressed.
> - Harm: kind and boundary distinctions become color-dependent, weakening distinguish and vocabulary tasks.
> - Repair: print the node kind on every card and pair it with a stable icon or shape and forced-colors-safe border pattern.
> - Deterministic assertion: for every visible node, kind must be available in visible text and accessible name and remain distinguishable with all authored colors suppressed.
> - Accessibility/reduced-motion assertion: redundant kind/status cues must survive grayscale, forced colors, keyboard focus, and reduced motion.
> - Authority ceiling: kind rendering is a presentation claim; semantic correctness remains bounded by the admitted source.
> - Verdict: **FIX**.
> - Evidence: `/tmp/bw-ui-color/active-relation-forced-colors.png`.
>
> ### Preserved cue
>
> Candidate-status wording is not solely color-based: the accessibility tree includes explicit phrases such as “Needs Evidence,” “Source-Backed,” “Preview-Accepted,” and explanatory sentences. **KEEP**, while adding the missing selected-state and authority-boundary surface.
>
> ### Reduced-motion zero-finding defense
>
> `prefers-reduced-motion: reduce` matched and `document.getAnimations()` returned no active animations during the tested static relation interaction. No deterministic reduced-motion failure was observed in that bounded interaction. This does not validate tour or future focus-scene transitions; those require an explicit branch-pivot scenario.
>
> ### Residue
>
> Browser evidence cannot establish novice comprehension, successful retelling, trust, confidence, correct semantic interpretation, ontology promotion, release, deployment, or production readiness. A selected-node state was not independently frozen; node-selection semantics remain review residue rather than a passing claim.

## Branch-pivot attacker — verbatim review return

> ## Attack C result
>
> Target: `http://127.0.0.1:37037/?token=<redacted-token>`.
>
> The current interface supports mouse-driven node-to-node inspector traversal, including a breadcrumb, Back button, visible relation wording/direction, and `authority:none`. It does not implement the proposed focus-scene/branch-pivot contract.
>
> Exact observations:
>
> - Default state contained 237 node elements and 231 edge elements.
> - Tour step 1 named four referenced components but retained all 237 nodes and 231 edges; the screenshot remained a whole-graph overview.
> - Tour step 1 exposed zero persistent edge-label elements, so the 11 known cross-tour relations were not distinguishable as labeled portals.
> - Clicking `Identity and Consent`, then its `→ related to Authentication and Consent` row, opened the destination inspector with a source/destination breadcrumb and Back button. The graph still contained 237 nodes and 231 edges; five incident labels became visible.
> - Advancing to tour step 2 changed the four referenced components but retained the prior `Authentication and Consent` inspector, producing mixed step/selection context.
> - The relation row was a `DIV` with no role or `tabindex`; it was absent from the complementary panel’s 19-element focus order.
> - Under `prefers-reduced-motion: reduce`, the same mouse traversal worked with zero active animations, but still retained all 237 nodes and 231 edges.
> - Activating `Focus` on the non-tour destination changed neither count: 237 nodes and 231 edges before and after. No deterministic one-hop fallback was observed.
> - Both sessions reported zero console errors or warnings; six dynamic graph/config requests returned 200.
> - Both named browser sessions were closed, and the retained `/tmp` evidence passed the credential audit.
>
> ### C-01 — Four-node tour steps are not focus scenes
>
> - Severity: High.
> - Black-box task/evidence: Start tour step 1, which lists four components; observe 237 nodes and 231 edges before and after, with the whole graph still visible.
> - Surface: Learn-mode graph and Tour panel.
> - Harm: Locate, trace, and retell remain whole-graph tasks; the four-node recipe does not bound local meaning.
> - One-line repair: Replace the graph projection atomically with the active tour step’s four nodes plus explicitly labeled outbound portals.
> - Deterministic assertion: Every tour step renders exactly its four `nodeIds`, their admitted internal relations, and every crossing relation as a labeled portal; unrelated nodes are absent from the scene.
> - Accessibility/reduced-motion assertion: Announce the scene heading and node/portal counts; reduced motion performs the same replacement immediately.
> - Authority/human ceiling: This proves rendered projection structure only, not that four nodes are sufficient for comprehension or semantically authoritative.
> - Verdict: `FIX`.
>
> ### C-02 — Outbound traversal is mouse-only and not exposed as a portal
>
> - Severity: High.
> - Black-box task/evidence: Mouse activation of `→ related to Authentication and Consent` succeeds, but the clickable row and its ancestors are generic `DIV`s without role or `tabindex`; the row is absent from focus order. Tour step 1 has zero persistent edge labels.
> - Surface: Selected-node Connections list and graph relations.
> - Harm: Keyboard users cannot perform the same trace, and readers cannot distinguish the known cross-tour relations from the remaining 231 edges.
> - One-line repair: Render every outbound portal as a focusable button/link with source, relation label, direction, destination, and portal status in its accessible name.
> - Deterministic assertion: Tab reaches every visible portal, and Enter/Space yields the same destination, breadcrumb, selected relation, scene, and authority state as mouse activation.
> - Accessibility/reduced-motion assertion: Focus remains visible and direction is announced; reduced motion changes scene without rotation.
> - Authority/human ceiling: A portal may expose admitted relation structure but must not imply cause, time, execution, promotion, or authority.
> - Verdict: `FIX`.
>
> ### C-03 — Inspector traversal preserves useful context but does not pivot the graph
>
> - Severity: Medium.
> - Black-box task/evidence: Mouse traversal produced `Identity and Consent › Authentication and Consent`, Back, reverse relation wording, and `authority:none`; nevertheless all 237 nodes and 231 edges remained.
> - Surface: Destination inspector, breadcrumb, and graph canvas.
> - Harm: The interface conflates opening a node detail with replacing/reorienting a coherent subgraph, weakening distinguish and boundary tasks.
> - One-line repair: Preserve the existing breadcrumb and authority tags while replacing the canvas with the destination scene centered on the selected labeled relation.
> - Deterministic assertion: After portal activation, the breadcrumb grows by one entry, the selected source–label–direction–destination tuple remains visible, and the destination scene replaces the source scene.
> - Accessibility/reduced-motion assertion: Announce destination and stack depth; keyboard and reduced-motion routes must produce identical semantic state.
> - Authority/human ceiling: Breadcrumb continuity is presentation evidence, not proof of semantic correctness or reader understanding.
> - Verdict: `FIX`, while `KEEP`ing the existing breadcrumb, Back control, direction wording, and authority tag.
>
> ### C-04 — Tour advancement retains stale cross-step selection
>
> - Severity: Medium.
> - Black-box task/evidence: After traversing from step-1 component `Identity and Consent` to `Authentication and Consent`, activating Next changed the tour to step 2 and its four new components while retaining the prior destination inspector.
> - Surface: Tour step transition and inspector.
> - Harm: The reader sees two competing contexts, undermining trace, retell, and scene-boundary clarity.
> - One-line repair: Make step changes atomic: reset to the step scene or explicitly preserve prior state as a labeled breadcrumb/portal trail outside the active scene.
> - Deterministic assertion: After changing steps, no selected node outside the active scene remains unless it is explicitly represented as history or an outbound portal.
> - Accessibility/reduced-motion assertion: Announce the new step and context reset; perform it immediately under reduced motion.
> - Authority/human ceiling: Consistent state does not prove that the tour order conveys correct causality or workflow.
> - Verdict: `FIX`.
>
> ### C-05 — No one-hop fallback for non-tour nodes
>
> - Severity: Medium.
> - Black-box task/evidence: At non-tour destination `Authentication and Consent`, activating Focus left 237 nodes and 231 edges before and after.
> - Surface: Node inspector Focus action and graph canvas.
> - Harm: Nodes outside tour scenes cannot be bounded into a deterministic local trace, leaving locate and retell at whole-graph scale.
> - One-line repair: Define Focus for non-tour nodes as selected node plus deterministic one-hop neighbors, with all remaining relations represented as labeled outbound portals.
> - Deterministic assertion: Repeated Focus on the same non-tour node yields the same sorted node/edge/portal set and excludes every unrelated node.
> - Accessibility/reduced-motion assertion: Expose counts and portal names programmatically; reduced motion applies the same set without animated reorientation.
> - Authority/human ceiling: One-hop determinism is a presentation invariant, not a claim that the neighborhood is sufficient or promoted.
> - Verdict: `FIX`.
>
> ## Smallest acceptance contract
>
> 1. Tour start replaces the whole graph with exactly the active four-node scene.
> 2. Every cross-scene relation appears as a labeled, directed, keyboard-operable portal.
> 3. Portal activation atomically replaces the scene while preserving breadcrumb, Back, source/relation/destination, source references, and authority ceiling.
> 4. Tour-step changes cannot retain an unlabeled out-of-scene selection.
> 5. Non-tour Focus deterministically renders one-hop neighbors and outbound portals.
> 6. Mouse, keyboard, and reduced-motion paths produce the same semantic state; reduced motion performs no rotation.
> 7. Spatial position or rotation never encodes causal, temporal, execution, promotion, or authority meaning.
>
> ## Residue and zero-finding defense
>
> No rotation-semantics failure was observed because scene replacement/reorientation is not implemented; therefore the future rotation contract remains untested rather than passed. The reduced-motion check found zero active animations and equivalent present-day mouse inspector traversal, but cannot validate an absent branch-pivot transition.
>
> Human comprehension, four-node sufficiency, retelling accuracy, semantic correctness beyond admitted source, ontology promotion, release, deployment, and production readiness remain unproved.

## Verifier returns

### Proxy-validity verifier — verbatim return

> Verdict: the five change requests are evidence-backed, but none has a sufficiently discriminating acceptance assertion yet. `FIX` all five; `DROP` none.
>
> Evidence keys:
>
> - `E1`: `browser-evidence/attackers/branch-pivot/measurements.json`
> - `E2`: `browser-evidence/attackers/cold-reader/focus-order.json`
> - `E3`: `attacks.md`, Color attacker B-01–B-03
> - `E4`: `browser-evidence/attackers/cold-reader/{search-suggested-track-aria.md,after-search-result-aria.md,after-relation-aria.md}`
> - `E5`: `browser-evidence/{README.md,residue-ledger.yml}`
>
> #### CR-1 — FIX
>
> The failure is literal: tour step 1 names four components but retains 237 nodes/231 edges/zero persistent labels; non-tour `Focus` also remains 237/231 (`E1`). Keep the bounded-hybrid hypothesis, but do not call tour membership a semantic branch or sufficient meaning unit (`E5`).
>
> Required assertion repair: pin test-owned, source-derived sorted arrays for one named tour fixture and one named non-tour fixture—node IDs, internal relation tuples, directed portal tuples—and compare rendered state exactly. Include a fixed unrelated node ID that must be absent. First assert the frozen whole-graph build fails with 237/231. Expected arrays must not be generated by the projection implementation under test.
>
> #### CR-2 — FIX
>
> Search is stop 10; after the freshness notice, ordinary traversal enters graph edges (`E2`). Fifteen sampled edges had `outline-style:none`, while connection rows were non-focusable generic `DIV`s (`E1`, `E3`).
>
> Rewrite “heading, authority cues, and first relation are reachable within five Tabs”: headings/tags need not themselves be focus targets. Assert that an exact-result selection or explicit skip control moves focus to a named detail landmark; its accessible text contains the exact heading and authority tag; the first relation control is reached within a fixed Tab count. Assert computed nonzero outline/border geometry in each mode, without claiming contrast compliance until contrast is measured.
>
> #### CR-3 — FIX
>
> The selected graph relation left the graph and tour panel unchanged (`E3`), while inspector traversal did preserve visible direction wording, breadcrumb, Back, and `authority:none` (`E1`).
>
> Use the literal fixture `Identity and Consent —related to→ Authentication and Consent`. Assert exact tuple text, selected-state attribute, breadcrumb array, stack depth, destination heading, authority/source surfaces, and scene replacement. Pointer, Enter, and Space must yield byte-equivalent serialized semantic state. This proves stable UI state only.
>
> #### CR-4 — FIX
>
> Step 1→2 retained the prior `Authentication and Consent` detail (`E1`); starting the tour displaced the active SuggestedTrack trace (`attacks.md`, A3).
>
> Choose one behavior instead of allowing “reset or preserve.” Pin pre-tour, entered-tour, changed-step, exited-tour state objects and compare exact selected node, breadcrumb, portal/history, and authority fields. Include the observed stale `Authentication and Consent` state as the negative fixture that must fail after step 2.
>
> #### CR-5 — FIX
>
> Exact search already ranks `claim SuggestedTrack 100%` first, but detail reports `business-kind:entity`; forced colors removes persistent kind differentiation (`E3`, `E4`). Thus first-place ranking alone is not discriminating.
>
> Assert the exact result’s visible/accessibility kind equals `entity`, lifecycle posture equals `reviewed-candidate`, and detail exposes the same values plus `authority:none`. Add a non-candidate fixture so absent lifecycle posture is not fabricated. Suppress authored colors and verify text/name plus non-color cue presence; specify semantic roles only, with no palette or contrast claim.
>
> All checks remain structural agent pretests. Search, headings, labels, breadcrumbs, and scripted steps demonstrate reachability and deterministic rendering—not comprehension, retelling accuracy, semantic correctness, promotion, release, deployment, or production readiness (`E5`).

### Semantic-authority verifier — verbatim return

> ## Semantic and authority verification
>
> Overall: verification completed, but no CR is acceptable verbatim. All five repair directions are evidence-supported; each needs a bounded correction before final acceptance. No CR should be dropped.
>
> ### CR-1 — FIX
>
> The failure is verified by `branch-pivot/measurements.json`: tour step 1 retained 237 nodes/231 edges, and non-tour Focus retained the same counts. The frozen graph confirms five disjoint four-node tour sets, 20 total tour nodes, and exactly 11 relations between different tour sets.
>
> Correction required: define admission directly from frozen `tour[].nodeIds` and `edges`, including exact source, target, `direction`, generic `type`, relation-local `description`, and endpoint `filePath` provenance. Every rendered node must retain `authority:none`, `candidate-status:*`, and `branch:business`. Scene membership, portal classification, position, and rotation remain removable projection state and must encode no causal, temporal, execution, promotion, release, or authority meaning.
>
> ### CR-2 — FIX
>
> The keyboard defect is verified: Search is tab stop 10; the freshness warning is stop 13; graph relations follow. Fifteen sampled relation groups had no visible outline, and connection rows were non-focusable generic `DIV`s.
>
> Correction required: parity must cover every pivot-capable node, relation, and portal—not only portals. Enter/Space and pointer activation must produce identical admitted scene membership, relation tuple, breadcrumb depth, provenance, candidate-local authority surface, and immediate reduced-motion result. Visible focus must survive forced colors without color or animation as the sole cue.
>
> ### CR-3 — FIX
>
> The observed inspector path supports breadcrumb, Back, direction wording, and `authority:none`; graph-edge activation did not expose persistent visible selected-relation state.
>
> Correction required: “exact relation wording” is underspecified. The graph distinguishes generic `type` from relation-local `description`; for example, `SuggestedTrack → TerritoryUnit` has `type: builds_on` and `description: supports`. The selected tuple must preserve both fields or explicitly identify which is the displayed predicate, plus source/target direction, endpoint source paths, candidate status, and `authority:none`. A UI paraphrase must not invent causal, temporal, execution, promotion, release, or authority semantics.
>
> ### CR-4 — FIX
>
> The stale-context observation is verified: advancing to tour step 2 retained the prior `Authentication and Consent` inspector.
>
> Correction required: distinguish stored restoration state from active scene state. Tour entry may suspend an existing trace and tour exit may restore it, but step changes cannot visibly mix an out-of-scene selection unless it is explicitly labeled as history or a portal. Pointer, keyboard, and reduced-motion paths must yield the same state. Tour order remains presentation order only—not workflow, causality, lifecycle, execution, or promotion.
>
> ### CR-5 — FIX
>
> The vocabulary mismatch is verified: exact search ranked `claim SuggestedTrack 100%`, while the admitted node carries `business-kind:entity`. Forced colors removed overview-scale kind differentiation.
>
> Correction required: the exact-first ranking already passed, so it is not itself a defect. Acceptance must instead compare search, card, detail, accessible name, and every pivot destination against the same admitted `business-kind:*`, `candidate-status:*`, `authority:none`, and `filePath`. Semantic color roles may supplement these literals but cannot replace them. This establishes source-consistent presentation only—not semantic correctness, promotion, release, deployment, or production readiness.
>
> Authority receipt: the adapter reports `authority_effect: none`, read-only projection, byte-identical builds, and an explicit ceiling excluding implementation, ontology promotion, release, and production claims. The graph hash matches the frozen rubric value `e8f754e6aed7b05759439df82db421eb51fa050c78b86b37d5d689e89a751433`.
