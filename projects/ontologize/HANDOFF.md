# HANDOFF — ontologize ↔ Arcanum ontology work (for Victor)

- Mode: invoke `handoff` · Date: 2026-06-08 · Author session: ontologize design refinement
- Source session reference: project `projects/ontologize` (research → product → DAG/metrics → delivery
  lanes → Lane B design → ontology branches), all dispatch/refine runs validated `pass`.
- Split reason: **execution continuation** — hand the ontologize design baseline to Victor and connect
  it to the dispersed ontology work already in `domainspec-core` so it isn't rebuilt from scratch.
- Context selection method: context-builder-style obligation-linked sweep of the whole repo (below).

## New-session prompt (paste to start)

> Continue the CyberAlchemy ontology+DAG consulting product (`projects/ontologize`). The design is
> complete and validated: product, DAG/metrics, two delivery lanes, Lane B build design, and the
> 4-branch ontology model. Reconcile it with the existing Arcanum/CyberAlchemy ontology work indexed
> in this handoff, then proceed to WORK-PACK T1 (assessment instrument) for the cap-factory and
> logistics pilots. Read `projects/ontologize/README.md` first.

## What ontologize produced (this work)

- [README](README.md) · [SPEC](SPEC.md) · [DESIGN](DESIGN.md) · [PRODUCT](PRODUCT.md)
- [DAG-AND-METRICS](DAG-AND-METRICS.md) · [DELIVERY-LANES](DELIVERY-LANES.md) ·
  [LANE-B-DESIGN](LANE-B-DESIGN.md) · [ONTOLOGY-BRANCHES](ONTOLOGY-BRANCHES.md)
- [PLAN](PLAN.md) · [IMPLEMENTATION-LAYERING](IMPLEMENTATION-LAYERING.md) · [WORK-PACK](WORK-PACK.md)
- Decisions: [pilot-and-positioning](decisions/pilot-and-positioning.md) · Levels: [L0](levels/L0-corpus.md)/[L1](levels/L1-pattern-map.md)/[L2](levels/L2-product-closure-plan.md)
- Dispatch + refine evidence: [ontologize-research.dispatch.json](ontologize-research.dispatch.json) and
  `development/refinement-runs/{dag-metrics,delivery-lanes,lane-b-design,ontology-branches}`.

## Dispersed ontology work in domainspec-core (context-builder index)

Obligation: _reuse, don't rebuild._ Each entry notes how it relates to ontologize.

### Canonical Arcanum ontology capability (the substrate Lane B builds on)

- `arcanum/arcana/ontology-vault/` — the ontology-vault sigil (branch-aware business↔system, bridge
  edges, confidence, premises). **Relates to:** ONTOLOGY-BRANCHES (B1/B2/B4) + LANE-B-DESIGN.
  Dev lifecycles: `arcanum/arcana/ontology-vault/development/{general-ontology-lifecycle,cyberalchemy-ontology-lifecycle}`.
- `arcanum/spells/ontology-harness/` — composes inventory + ontology-vault + context-builder.
  **Relates to:** the whole Lane B substrate.
- `arcanum/research/proofs/ontology-vault-branching/` — `proof-report.md` + source-vault.
  **Relates to:** ONTOLOGY-BRANCHES — this is prior proof of the branch model; reconcile our 4 branches with it.
- `arcanum/BUSINESS-ONTOLOGY.md` — defines the business/meaning branch vs implementation.
  **Relates to:** ONTOLOGY-BRANCHES B1 (meaning).
- `arcanum/development/cyberalchemy-ontology-lifecycle/` — `ONTOLOGY-ARCHITECTURE.md`, `CONTEXT-HANDOFF.md`,
  `DEFINITIONS-GLOSSARY.md`, `CONCEPT-TOURNAMENT.md`. **Relates to:** PRODUCT + GLOSSARY; likely the
  closest prior "CyberAlchemy ontology" thinking — read before extending.

### Live CyberAlchemy ontology (already-built entries)

- `cyberAlchemy/ontology/` — `entries/`, `source-digests/`, `source-ledger.md`. **Relates to:** an
  existing populated ontology; check whether ontologize should consume/extend it rather than start fresh.
- `cyberAlchemy/agentic-system/slices/02-ontology-entry-contract/` — entry contract.
  **Relates to:** L-dag node schema + Lane B `promotion-record` entry type.
- `cyberAlchemy/agentic-system/slices/04-operational-ontology/` — **operational** ontology slice.
  **Relates to:** ONTOLOGY-BRANCHES B3 (operational, first-class) — directly reconcile.

### GoldenQuill source precedent (read-only, on `master`)

- `projects/goldenquill/pipeline/grant_dag/validate.py` + `tests/grant_dag/` (master) — the 5 node
  types + 11 rules DAG-AND-METRICS was lifted from. **NOTE:** lives on `master`, not on the current
  `codex/goldenquill-client-package` branch.
- `projects/goldenquill/docs/strategy/goldenquill_ontology_dag_grant_research_synthesis_2026-06-01.md`
  (master) — meaning/system/operational/bridge branches; source for ONTOLOGY-BRANCHES.
- `projects/goldenquill/docs/client-packages/...client_sendable_2026-06-01/` — client-package precedent
  for the deliverable template.

### Native skill mirrors (installed)

- `.claude/skills/{ontology-vault,ontology-harness,inventory,context-builder}/SKILL.md` — the runtime
  capabilities Lane B reuses/extends (see LANE-B-DESIGN bridge verdicts).

## Open reconciliation items for Victor

1. **Branch model** — reconcile ONTOLOGY-BRANCHES (4 branches) with `arcanum/research/proofs/ontology-vault-branching`
   and `cyberAlchemy/.../04-operational-ontology`; confirm naming (meaning vs business).
2. **Existing entries** — decide whether `cyberAlchemy/ontology/entries` feed the pilots or are separate.
3. **Lane B bridges** — 3 EXTEND / 2 NET-NEW (see LANE-B-DESIGN); build via `sigil-development` when a pilot is greenlit.
4. **Validation gap** — nothing is client-validated yet; WORK-PACK T1 (assessment) is the entry point.

## Recommended next route

`task-session` → WORK-PACK **T1** (assessment instrument), populating the 4 branches per client; or
`sigil-development` → Lane B Bridge 2 (dispatch) if a Lane-B/Hybrid pilot is greenlit.

## Guardrails

All ontologize outputs are candidates — no canonical Arcanum promotion, no pricing/contracts/named
clients without owner review. GoldenQuill + Arcanum skill defs are read-only source evidence.
