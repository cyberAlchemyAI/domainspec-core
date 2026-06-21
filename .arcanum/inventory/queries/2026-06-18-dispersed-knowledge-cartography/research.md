---
tags: [inventory, dispersed-knowledge, raw-returns, cartography, research-program, knowledge-system, promotion-guardrail]
node_type: research
is_session: false
layer: architecture
nature: synthesis
status: candidate
created: 2026-06-18
dispatch_id: 2026-06-18-dispersed-knowledge-cartography
dispatch_type: research
working_folder: .arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/
sources: [.arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/cartographer-receipts.md, arcanum/, implementation/domainspec/, validation/poker-team/, projects/, cyberAlchemy/, .arcanum/]
---

# Research - Dispersed Knowledge Cartography

## Method

The confirmed dispatch split repository cartography into four read-only source
families:

- Arcanum capability/runtime lane
- Private DomainSpec implementation and validation lane
- Project and research tower lane
- Knowledge governance and feedback/control lane

Each lane returned concrete paths, candidate cards, authority conflicts, residue,
and v2 structure implications. This research file folds the receipts into a
source-family map that the findings and evidence cards can reuse.

## Cross-Lane Pattern

The repo has a recurring source-to-promotion chain:

1. Raw source evidence and source ledgers.
2. Inventory cards and EvidenceSets.
3. Ontology-vault candidate condensation.
4. Definitions, constitutions, decisions, or owner-gated promotion.
5. Observability and session residue as feedback evidence.

This pattern appears independently in `.arcanum/inventory/schema.md`,
CyberAlchemy's inventory/ontology pipeline, Ontologize's L0/L1/L2 tower, and the
private DomainSpec governance/registry/observability chain. That convergence is
the strongest architectural signal for v2.

## Authority Families

| Family | Primary Evidence | Authority Posture | Inventory Use |
| --- | --- | --- | --- |
| Public Arcanum | `arcanum/arcana/`, `arcanum/spells/`, `arcanum/registry/`, generated host surfaces | Canonical packages and registries are public authority; host surfaces are generated projections. | Capability catalog, runtime projection map, lifecycle rules. |
| Private DomainSpec | `implementation/domainspec/`, `validation/poker-team/`, parent governance docs | Private implementation and validation authority under submodule discipline. | Governance spine, registry/code binding, validation harness, publish boundary. |
| Research Programs | `projects/domainspec-v2/`, `cyberAlchemy/`, `projects/framework-unification/`, `projects/ontologize/` | Candidate research and reusable patterns; not canonical until promoted. | V2 structure precedents, tower method, two-axis taxonomy, product/public derivative boundaries. |
| Knowledge Governance | `.arcanum/inventory/`, `.arcanum/ontology-vault/`, `.arcanum/observability/`, `.arcanum/necronomicon/`, Craft | Read models and control loops; no direct promotion authority. | Evidence cards, EvidenceSets, branch maps, feedback signals, residue capture. |

## Reusable Design Moves

- Keep catalogs separate from contracts: registry indexes should point to
  canonical package contracts instead of duplicating them.
- Keep generated surfaces visibly derivative with `canonical_source` and
  mutation policy.
- Use feature-pack validation as a reusable v2 shape: spec, aspects, test spec,
  pipeline report, alignment reports, observability report, registry, and index.
- Preserve research towers as non-canonical until a decision-gate or owner
  promotion route moves them.
- Treat sessions, telemetry, and dispatch ledgers as evidence and residue, not
  meaning authority.
- Use thick ontology entry shape only after selector-level evidence exists.

## Main Contradictions And Drift Signals

- `implementation/domainspec/ARCHITECTURE.md` appears to point at an absent
  `architecture/ARCHITECTURE.md` target in this checkout.
- Parent and submodule dispatch telemetry surfaces have similar names but
  different authority. Inventory consumers need explicit selectors.
- Ontologize public offering and internal research overlap but have different
  publication boundaries.
- CyberAlchemy includes candidate/pre-baseline documents; vocabulary authority
  must be checked before promotion.
- The current ontology map had candidate condensation before evidence cards.
  This run supplies the first selector-level cards but does not promote them.

## Candidate V2 Repository Structure Hypothesis

The following tree is a hypothesis for architecture discussion, not a default
repo design or promoted decision. The evidence supports the separation of
authority surfaces; it does not yet choose final folder names, top-level
visibility, or publication boundaries.

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

The important proposal is not the exact folder spelling. The structural
hypothesis is that authority, research, capability contracts, generated
surfaces, validation, inventory, ontology, and observability should stay
physically and semantically distinct unless an owner decision deliberately
combines them.

## Handoff

Use `findings.md` for the human-facing synthesis, `entries/evidence-cards/` for
selector-level reuse, `entries/evidence-sets/` for context-builder and future
v2 structure handoffs, and the ontology map for candidate branch condensation.
