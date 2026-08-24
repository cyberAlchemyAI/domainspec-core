# Invoke Result

- Mode: define → design → plan
- Spell: `invoke`
- Canonical ID: `invoke`
- Scope: library
- Phase status: `pass`
- Mode contracts: `spells/invoke/define.md`,
  `spells/invoke/design.md`, and `spells/invoke/plan.md`
- Target: Body War business ontology whole-atlas arrow representation
- Source mutation: none
- Automatic execution: false

## Define

- Outputs: `CONTEXT-PACK.md`, `GLOSSARY.md`, `SPEC.md`,
  `DEFINE-TRANSPORT.md`
- Discovery: existing completed atlas, source-bound receipts, and the user's
  accepted progressive-arrow correction
- Glossary consistency: pass
- Definition Distill: not required; scope was bounded by the current atlas and
  accepted correction
- Result: pass

The specification requires two connected scales: a 13-lane directed overview
for the six lenses and one exact source → predicate → target arrow for each of
231 canonical relations. It preserves 237/231/122/109/44 coverage.

## Design

- Outputs: `ARCHITECTURE.md`, `UX-PLAN.md`,
  `DESIGN-DISTILL-VALIDATION.md`, `DESIGN-TRANSPORT.md`
- Design views: architecture plus authority/trust, data/lifecycle,
  integration/versioning, persistence/concurrency, quality, UX, and validation
  contracts
- Denominator: pass, 23 detected signals
- Selection: `design-validator-pass`
- Fixed point: pass
- Pass 1:
  `421bc2c3b97876280f6978d75fcf5f3a61c27910ea1626aeb3559b52ff0f9216`
- Pass 2:
  `421bc2c3b97876280f6978d75fcf5f3a61c27910ea1626aeb3559b52ff0f9216`
- Design Distill: pass
- Helper: `/root/bw_arrow_atlas_analysis`, read-only, completed and joined
- Result: pass

The design keeps meaning in real HTML and uses SVG only for geometry. Desktop
gets a bounded six-lens map plus semantic lanes; mobile retains the 13 semantic
lanes and stacks exact arrows. A lens-set change fails closed.

## Plan

- Outputs: `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`,
  `EXECUTION-PACK.md`, `DISPATCH-TRACE.md`, `DISTILL-VALIDATION.md`,
  `PLAN-TRANSPORT.md`, `CONTINUATION.json`, four task specs, four waves, and
  shared execution/closeout control
- Implementation layering: L0 projection, L1 exact relation arrows, L2
  overview/recomposition, L3 browser evidence
- Work Pack: split
- Complexity: medium
- Per-layer planning: L0, L1, L2, L3 waves
- Implementation detail: four complete task specs
- Smallest working units: four
- SWU atomicity: pass; task-shaped count 0
- First-unit narrowness: pass
- Task Session closeout sync: pass at Plan contract
- Plan Distill: pass; recomposition pass; gap count 0
- Distill telemetry:
  `distill-body-war-business-ontology-atlas-arrows-20260730T062453Z`,
  recorded
- Invoke telemetry:
  `invoke-body-war-business-ontology-atlas-arrows-20260730T062453Z`,
  recorded
- Result: pass for explicit selection

## Dispatch Techniques

Applied: `sequence`, `scu_swu_reduction`, `recomposition_proof`,
`validation_loop`, `owner_boundary_check`, `handle_handoff`,
`residue_ledger`, `execution_receipt_handoff`,
`artifact_contract_bridge`, and `concrete_path_evidence`.

Full dispatch: not required. The future route has one sequential Task Session
owner and overlapping write scopes; no multi-agent execution or reusable
cross-owner route is designed.

## Template And Validation

- Templates: standalone implementation-layering, split work-pack, and
  DomainSpec execution-pack; eligibility recorded in `PLAN-TRANSPORT.md`
- Validation strategy: pure projection checks, renderer structure/count checks,
  deterministic full regression, then pinned browser/static-mode evidence
- Plan structural checks: 4 unique SWUs, 4 task specs, 4 waves, 4 closeout
  rows, required implementation-detail/handoff sections, valid continuation
  JSON, scoped whitespace pass
- Design reproducibility: deterministic receipt rerun byte-identical
- Inventory index: lookup-ready; 0 failures and 115 historical tag warnings

## Decisions And Gaps

- Decision: aggregate only cross-lens flow at overview scale; retain every
  canonical relation at exact scale.
- Decision: execute sequentially because renderer and generated-evidence write
  scopes overlap.
- Decision: fixed coordinates are valid only for the known six-lens prototype.
- Acceptance-critical Plan gaps: none.
- Conditional runtime blockers: byte drift, missing predecessor receipt, or
  unavailable shared browser runtime.
- Deferred: general graph layout, filtering, ontology editing, human study,
  formal conformance, publication, release, deployment, and production.

## Capability Ceiling And Next Route

- `artifact_authored`: pass
- `plan-evidence`: pending
- `mutation_runtime_ready`: not evaluated
- `authority_effect`: none
- `release_admission`: not granted
- capability-status resolver: not requested
- selected SWU: none
- first selectable SWU: `SWU-BWAA-001`
- next route: explicit selection of `SWU-BWAA-001`, then Context Builder and
  one Task Session preflight

The currently served `BUSINESS-VIEW-ATLAS.html` was not changed by this run and
still lacks the planned graphical arrows.
