# Body War Ontology UI Black-Box Rubric

## Purpose

Attack the exact existing Body War ontology viewer as a user-facing interface.
The review must produce verified change requests, not implementation.

The browser attackers begin from the rendered interface in isolated fresh
contexts. They may inspect visible text, the accessibility tree, focus order,
computed presentation, browser console/network behavior, and screenshots. They
must not inspect application source code before submitting their initial
observations.

## Frozen Target

- Presentation graph SHA-256:
  `e8f754e6aed7b05759439df82db421eb51fa050c78b86b37d5d689e89a751433`
- Browser baseline receipt SHA-256:
  `86a4f72e3f694c9dcb37e230462fcbbb6e45c50c64f963037562080848757412`
- Browser baseline screenshot SHA-256:
  `58226107c1f2c5e94c71000183665de942c6ce3efbb2134e34094d780a205de7`
- Expected graph counts: 237 nodes, 231 relations, 17 layers, 5 tour
  scenes.
- Runtime: fresh loopback-only gateway and fresh Chromium contexts from the
  shared global Playwright 1.59.1 runtime. The ephemeral access token must not
  be persisted.

## Attack A — Cold Reader

Starting from the default interface without reading source code:

1. State what the page represents.
2. Find `SuggestedTrack`.
3. Identify one relation entering or leaving it, including direction and
   relation label.
4. Explain in plain language what remains candidate-only or non-promoting.
5. Record the first meaningful action, wrong turns, controls used, focus order,
   and any point where the graph becomes a visual search problem rather than a
   semantic navigation problem.

Evidence may establish only whether the interface exposes a usable information
path to an automated cold reader. It cannot establish human comprehension.

## Attack B — Color And Redundant Meaning

Inspect the default graph, a selected node, an active relation, and the
authority/trust surfaces under:

- default color;
- grayscale;
- increased contrast or forced-colors where supported;
- keyboard-only navigation;
- reduced motion.

For node kind, current selection, relation direction, candidate status, and
authority boundary, report whether meaning remains recoverable without color.
Color-only meaning is a finding even if the palette is visually attractive.

Candidate palette direction:

- stable categorical hues for node kinds;
- one high-contrast accent for the current focus scene;
- muted neutral treatment for context outside the scene;
- distinct warning styling for candidate/non-promoting or blocked boundaries;
- no red/green-only semantic pair.

The review may recommend exact tokens only when contrast is measured. It must
prefer semantic roles over arbitrary color names.

## Attack C — Focus Scene And Branch Pivot

Try to determine whether the current interface can present one coherent
subgraph at a time and pivot across an outbound connection.

The proposed interaction contract to attack is:

1. The default view shows one **focus scene**, not all 237 nodes.
2. A focus scene initially uses one existing tour step's explicit `nodeIds`.
3. Relations whose other endpoint lies outside the current scene remain visible
   as labeled outbound portals.
4. Activating an outbound portal replaces the current scene with the
   destination scene and reorients the graph around the selected relation.
5. The transition preserves a breadcrumb/back stack, selected edge label and
   direction, source path, and authority ceiling.
6. Keyboard activation performs the same pivot.
7. Reduced-motion mode performs the pivot without rotation.
8. Nodes not assigned to a tour scene use a deterministic one-hop focus
   neighborhood until a stronger projection owner is selected.

The reviewer must try to falsify tour steps as the branch recipe. In
particular, check whether the 11 known cross-tour relations form intelligible
portals and whether four-node scenes omit necessary local meaning.

## Required Finding Shape

Every finding must include:

- severity;
- black-box task and exact observable evidence;
- target artifact or UI surface;
- why the behavior harms locate/trace/retell/distinguish/boundary/vocabulary;
- one-line repair;
- deterministic acceptance assertion;
- accessibility and reduced-motion assertion;
- authority and human-evidence ceiling;
- `KEEP`, `FIX`, or `DROP` after skeptical verification.

Zero findings in any attack lane require an explicit defense.

## Claim Ceiling

A passing browser run may prove exact-byte loading, interaction structure,
keyboard reachability, presentation invariants, and absence of browser errors.
It cannot prove human comprehension, semantic correctness beyond the admitted
source, ontology promotion, release, deployment, or production readiness.

