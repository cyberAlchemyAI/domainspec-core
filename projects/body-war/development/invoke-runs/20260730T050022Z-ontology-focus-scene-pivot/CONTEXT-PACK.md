---
module: body-war-ontology-focus-scene-pivot
version: current
status: define-input
updatedAt: 2026-07-30
docType: invoke-context-pack
---

# Context Pack

## Objective

Turn the accepted Body War ontology UI black-box findings into an
implementation-ready Define, Design, and Plan package for a bounded focus-scene
and portal-pivot interaction in the Ontology Evidence Workbench (OEW).

## Discovery Inputs

| Input | Role | Evidence ceiling |
| --- | --- | --- |
| `projects/body-war/development/reviews/20260730-ontology-ui-black-box/findings.md` | Five accepted change requests and smallest coherent slice | Structural browser findings; not implementation or human comprehension |
| `projects/body-war/development/reviews/20260730-ontology-ui-black-box/synthesis.md` | Bounded-hybrid projection decision and corrected acceptance language | Design direction; not code or acceptance evidence |
| `projects/body-war/development/reviews/20260730-ontology-ui-black-box/PARENT-APPROVAL.json` | Parent acceptance of the repaired review output | Review closure only |
| `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/overlay-manifest.json` | Source ownership map for the OEW overlay | Overlay ownership; generated builds are not source |
| `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/UPSTREAM.lock.json` | Frozen Understand Anything commit and package-manager boundary | Upstream identity only |
| `cyberAlchemy-v2/implementation/ontology-evidence-workbench/generated/runs/BODY-WAR-ONTOLOGY-001/presentation-graph.json` | Frozen Body War presentation input | Candidate-local read projection |

## Verified Baseline

- Frozen presentation graph SHA-256:
  `e8f754e6aed7b05759439df82db421eb51fa050c78b86b37d5d689e89a751433`.
- Current browser scene renders all `237` nodes and `231` edges during tour
  and non-tour focus actions.
- Tour step one names four source members but does not bound the rendered graph.
- Connection rows are not keyboard controls and sampled graph-edge focus has no
  visible outline.
- Graph relation activation changes inspector context without atomically
  replacing the graph scene or exposing a persistent selected relation.
- Tour step changes can retain an out-of-scene inspector selection.
- Source literals are inconsistent across search and detail, and node-kind
  differentiation collapses when authored colors are suppressed.

## Selected Direction

Use a bounded hybrid UI projection:

1. a node in a source tour resolves to exactly that tour's source-declared
   members;
2. a node outside all tours resolves to itself plus a deterministically sorted
   one-hop neighborhood;
3. an edge with exactly one endpoint in the scene resolves to a labeled,
   directed portal;
4. portal activation atomically replaces the current scene with the destination
   scene;
5. type layers remain filters, never semantic branches or focus units.

## Authority And Claim Ceiling

- The Body War ontology remains candidate-local.
- `authority_effect` remains `none`.
- `release_admission` remains `not-granted`.
- Scene membership, layout, position, portal classification, breadcrumb, and
  motion are removable presentation state.
- This package does not authorize viewer implementation, ontology mutation,
  upstream publication, release, deployment, production use, or a claim of
  human comprehension.

## Runtime And Ownership Boundary

- Use the existing OEW package root; do not add another `package.json`.
- Browser acceptance uses the user-global Playwright and installed Chromium
  described by the repository `AGENTS.md`.
- The reviewed Body War route is the native dashboard, not the separate
  `?oew=1` workspace implemented under the current `oew/**` overlay.
- Native dashboard sources are presently available only inside the pinned
  upstream source archive. Implementation must first admit exact native source
  counterparts through a successor overlay/build-lock contract under
  `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/`; it
  must not edit the archive.
- Generated dashboards and generated run outputs are evidence products, never
  direct source-edit targets.
- The existing `package.json` names L1 build scripts that are absent in this
  checkout. The successor build route must repair or replace that explicit
  contract before claiming a rebuilt viewer.
