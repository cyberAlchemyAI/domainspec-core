---
tags: [cyber-alchemy-space, capability-taxonomy, findings, knowledge-craft-governance, two-axis, reuse-map, inventory, dispersed-knowledge, v2-repo, promotion-guardrail]
node_type: findings
is_session: false
layer: architecture
nature: reference
status: draft
created: 2026-06-18
dispatch_id: 2026-06-18-dispersed-knowledge-cartography
dispatch_type: research
working_folder: .arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/
sources: [arcanum/, implementation/domainspec/, validation/poker-team/, projects/framework-unification, projects/ontologize, projects/domainspec-v2, cyberAlchemy/, .arcanum/, .agents/skills/, .claude/skills/]
---

# Findings - Dispersed Knowledge Cartography

## One-Line Answer

DomainSpec v2 should be structured around evidence authority layers, not around
the current folder history: source evidence, research towers, canonical
capability/spec contracts, validation harnesses, inventory cards, ontology
candidate maps, and observability must remain separate but linked.

## What The Cartographers Found

| Lane | Core Finding | Consequence |
| --- | --- | --- |
| Arcanum capability/runtime | Public Arcanum has a clean distinction between registries, canonical packages, spells, runtime adapters, and generated host projections. | v2 should keep catalog, contract, runtime, and generated surfaces separate. |
| Private DomainSpec | The private implementation already has computable governance, registry/code binding, observability, and a validation submodule with feature-pack reports. | v2 should promote these as structural patterns only through explicit private-boundary cards. |
| Project/research | CyberAlchemy, Framework Unification, Ontologize, and DomainSpec v2 research all converge on source -> pattern -> closure/promotion flow. | v2 should stay research-first until a decision gate promotes a tower output. |
| Knowledge governance | Inventory, ontology-vault, Necronomicon, Craft, dispatch, and observability form a feedback stack, but only inventory has the evidence-substrate role. | v2 should expose the knowledge stack directly and prevent ontology from promoting itself. |

## Candidate V2 Repository Structure Hypothesis

This tree is a candidate hypothesis for a later refine or decision-gate route.
It is not promoted architecture. Each top-level area below is supported by an
EvidenceSet or evidence-card family, but final naming and placement still need
owner review.

```text
domainspec-v2/
  README.md
  AGENTS.md
  authority/
    boundaries.md
    promotion-policy.md
    definitions/
    decisions/
  research/
    source-ledger.md
    towers/
      dcb-correctness/
      formal-modeling/
      intent-tags/
      spec-ontology-unification/
      target-state/
    synthesis/
  architecture/
    catalog/
    layers/
    runtime/
    decisions/
  capabilities/
    registry/
    packages/
    generated-surfaces/
  specs/
    domains/
    templates/
    validation-contracts/
  implementation/
    src/
    adapters/
    registry-binding/
  validation/
    feature-packs/
    harnesses/
    reports/
  inventory/
    manifests/
    evidence-cards/
    evidence-sets/
    context-packs/
  ontology/
    candidate-maps/
    branch-maps/
    promotion-requests/
  observability/
    signals/
    reflection/
    dispatch/
  ops/
    release/
    submodule-discipline.md
```

## Candidate Structure Rules

- `authority/` would own definitions, promotion policy, boundary rules, and decisions.
- `research/` would own source-ledgered towers and candidate synthesis; it does not
  mutate templates, validators, or runtime contracts directly.
- `architecture/` would own layer maps, runtime boundaries, and catalog-level views.
- `capabilities/` would own promoted capability contracts and generated projections,
  with projection metadata that points back to canonical sources.
- `specs/` would own domain/spec contracts and validator-grounded templates.
- `implementation/` would own code and registry binding, not research meaning.
- `validation/` would own feature-pack harnesses and evidence snapshots.
- `inventory/` would own source-backed cards and EvidenceSets.
- `ontology/` would own candidate condensation and branch maps until an explicit
  promotion request is approved.
- `observability/` would own feedback signals and dispatch traces as evidence, not as
  semantic authority.

## Reuse Map

| Existing Source | Reusable V2 Pattern | Evidence Card |
| --- | --- | --- |
| `arcanum/registry/`, `arcanum/arcana/`, `arcanum/spells/` | Catalog vs canonical contract vs composition split. | `arcanum-registry-catalog`, `arcanum-task-session-runtime-boundary` |
| `.agents/skills/`, `.claude/skills/`, `.github/skills/`, `.codex/commands/` | Generated runtime projection metadata. | `arcanum-runtime-projection-surfaces` |
| `implementation/domainspec/AXIOMS.md`, `CONSTITUTION.md`, validation scripts | Computable governance and registry/code binding. | `domainspec-governance-registry-observability-spine` |
| `validation/poker-team/docs/` | Feature-pack validation and report shape. | `pokerteam-feature-pack-validation-harness` |
| `cyberAlchemy/agentic-system-inventory-ontology-pipeline.md` | Source -> inventory -> ontology -> context -> execution -> telemetry loop. | `cyberalchemy-inventory-ontology-loop` |
| `projects/framework-unification/CONCEPT-MAP.md` | Two-axis pipeline/mechanism separation. | `framework-unification-two-axis-model` |
| `projects/ontologize/levels/` | L0 corpus -> L1 patterns -> L2 closure plan. | `ontologize-l0-l1-l2-research-product-tower` |
| `projects/domainspec-v2/research/` | Research-gated tower discipline and bounded correctness tracks. | `domainspec-v2-research-tower-discipline` |

## Promotion Guardrails

- Do not promote generated skill mirrors or command projections as canonical
  capability definitions.
- Do not move private implementation evidence into public Arcanum.
- Do not collapse research towers into specs before a decision gate.
- Do not treat observability, sessions, or dispatch ledgers as meaning authority.
- Do not let ontology-vault promote inventory, definitions, glossaries, sigils,
  spells, or runtime contracts by itself.

## Open Questions

- Should v2 keep `inventory/` and `ontology/` as visible top-level folders, or
  should they be mounted under `.arcanum/` while publishing generated read
  models into docs?
- Which DomainSpec private governance surfaces are safe to generalize into
  public Arcanum patterns, and which must remain private?
- Should session archaeology become a formal `authority/decisions/` input stream
  or stay under observability/residue until promoted?
- What exact owner reviews are required before turning the DCB and formal
  modeling towers into validator or implementation work?

## Status

This is a draft inventory finding. It is suitable as a v2 structure proposal and
context-building input, but not as a promoted architecture decision.
