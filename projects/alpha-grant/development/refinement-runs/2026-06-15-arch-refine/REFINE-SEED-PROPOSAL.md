# Refine Seed Proposal — Decentralized Living Library Architecture

- Run id: `2026-06-15-arch-refine`
- Dispatch id: `refine-2026-06-15-arch-refine`
- Owner: `refine`
- Date: 2026-06-15
- Preset: `standard`
- Research mode: `research-if-gap-appears`

## Target

`projects/alpha-grant/decentralized-living-library-summary.md` — the **initial
architecture** of a multi-node, public-benefit fungal biodiversity and applied
mycology grant network.

The architecture under refinement is, in effect, a graph that is currently
described only in prose:

- **Nodes / capacities** — PA culture (Padilla-Brown / MycoSymbiotics /
  MycoFest), field-methods & soil microbiome (Epp Schmidt), Houston Research
  Node (Balan / University of Houston), funding & operating-system layer
  (Inklovich / FIT Farms / Golden Quill / Tilth).
- **Project lanes** — seven fundable lanes (living library, AMF/INVAM-adjacent,
  soil/agroforestry field network, mushroom co-op, Houston Research Node,
  MycoFest public science, endowment/donor circle).
- **Grant-facing asks** — five fundable asks with amounts, routes, and
  deliverables.
- **Entity / partner routing** — public vs. private vs. co-op vs. university vs.
  fiscal-sponsor lanes that must stay un-commingled.
- **Non-negotiable boundaries** — KU/INVAM authorization limits, unverified
  partner claims, public/private asset separation, Houston-as-research-node
  framing, claims-review limits.

## Refinement objective

Turn the initial prose architecture into a **refined architecture design plus a
non-executed plan** that:

1. Surfaces the node / lane / ask / entity graph explicitly, with ownership and
   authority boundaries made legible (hidden-structure → x-ray).
2. Resolves — or explicitly ledgers — the recurring structural tension between
   **public-benefit infrastructure** and **private/commercial integration**
   (MycoSymbiotics IP, FIT Farms revenue, co-op assets).
3. Names the single highest-leverage architectural fork (the entity-home route)
   as a bounded, approvable decision rather than an open question.
4. Preserves every non-negotiable boundary as a hard gate, especially the
   sensitive external/partner context (KU/INVAM, unverified partners).
5. Selects the smallest coherent architecture unit that still recomposes into
   the full network, then produces a non-executed plan aligned with the
   document's "Recommended Immediate Move" internal decision package.

## Source context

- Primary source: the target summary doc (authoritative; read-only).
- The doc already encodes risks/controls, a 90-day path, and a recommended
  internal decision package — these are evidence inputs, not refine outputs.
- No prior refinement runs exist for this target (no memory-recovery needed).

## Write scope

- Refine writes **only** under
  `projects/alpha-grant/development/refinement-runs/2026-06-15-arch-refine/`.
- The source summary doc is **not** mutated. The refined design is a candidate
  architecture, not a replacement of the source.

## Done criteria

- A validated `REFINE-DISPATCH.json` exists before any stage runs.
- The canonical ten-stage loop is represented in the manifest/index with a
  native receipt or an explicit blocked reason per executed stage.
- A refined architecture design artifact expresses the node/lane/ask/entity
  graph with ownership/authority boundaries.
- The public/private tension is resolved or recorded in a residue ledger.
- A non-executed plan artifact exists.
- Every non-negotiable boundary survives the boundary-preservation gate.
- `RESULT.md` synthesis is built from stage artifacts, not from the route
  proposal.

## Validation surface

- `dispatch-spec` schema conformance for the route shape.
- `interrogation` pass/flag/block at refine-review, refine-design-review, and
  refine-final.
- `distill` coherent-unit selection with a recomposition target, plus a repair
  pass before planning.
- Boundary-preservation and entity-route-approval gates.

## Planned stage configuration

| # | Stage | Capability | Mode |
|---|-------|-----------|------|
| 1 | Context baseline | `context-builder` | `standard` (`--strict --emit both --handoff runtime --persist`) |
| 2 | Invoke Define | `invoke` | `define` |
| 3 | Interrogation | `interrogation` | `refine-review` |
| 4 | Research decision | `refine` | `research-if-gap-appears` |
| 5 | Distill | `distill` | `standard` |
| 6 | Invoke Redefine / Design | `invoke` | `design` (x-ray + dialectic + entity-route menu) |
| 7 | Interrogation | `interrogation` | `refine-design-review` |
| 8 | Distill Repair | `distill` | `validate` |
| 9 | Invoke Plan | `invoke` | `plan` (non-executed) |
| 10 | Final Interrogation + Synthesis | `interrogation` → `refine` | `refine-final` |

## Selected technique overlays

- `baseline_sequence` (default) — sequence, frame/handle handoff, validation
  loop, owner-boundary, observability grouping, minimum-component/data-quality.
- `xray_for_hidden_structure` — the request is literally "refine the initial
  **architecture**"; the architecture is a node/asset/ownership/routing graph
  buried in prose. Applies to the Design stage; outputs a structural artifact.
- `dialectic_for_tension` — public-benefit vs. private/commercial integration is
  a genuine competing-principle tension repeated across the doc. Requires
  opposing roles + convergence criteria + residue ledger at the Design stage.
- `route_menu_for_ambiguity` — the entity-home choice (fiscal sponsor / new
  nonprofit / co-op program / FIT Farms service lane) is a bounded option set
  and the single highest-leverage architectural fork. Adds a route menu output
  and an approval checkpoint gate.
- `protected_context_for_external_or_sensitive_evidence` — KU/INVAM
  authorization, MTA/strain access, and unverified partner claims are sensitive
  external context. Flags protected inputs and enforces a hard boundary gate.

### Overlays considered and not selected

- `tournament_for_alternatives` — dialectic + route menu already cover the
  comparative work; a full elimination tournament is heavier than a
  summary-doc architecture refine needs. Deferred.
- `toy_game_for_low_cost_falsification` — no selected abstraction yet needs a
  controlled failure test; revisit at planning if one appears.
- `memory_residue_for_context_recovery` — no prior runs/rejected candidates to
  recover; `residue_ledger` is still used inside the dialectic overlay.

## Research decision (recorded)

`research-if-gap-appears`. Local-first. The doc references external funders
(NSF, SARE, NRCS, FFAR, USDA NIFA) and external orgs; external research will be
proposed for confirmation **only** if Interrogation or Distill names a specific
external-context gap. External research cannot override the source doc.
