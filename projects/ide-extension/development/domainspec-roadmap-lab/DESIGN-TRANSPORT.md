---
id: ide-extension-domainspec-roadmap-lab-design-transport
status: pass
updatedAt: 2026-07-14
invoke_mode: design
---

# Invoke Design Transport

## Selection

- Mode: `design`, followed only after pass by `plan`.
- Profile: DomainSpec-style architecture bundle adapted to a brownfield private
  IDE surface; local design IDs are explicitly non-canonical.
- Context: [DESIGN-CONTEXT.md](DESIGN-CONTEXT.md), Context Builder
  `standard-strict`, 10 selected sources.
- Strategy input:
  [STRATEGY.md](../domainspec-roadmap-lab-strategy/STRATEGY.md).
- Full dispatch:
  [domainspec-roadmap-lab.dispatch.json](domainspec-roadmap-lab.dispatch.json).
- Subagents: none; the operator requested Invoke authoring, not a dispatch run.

## Output Set

| Required design view/companion | Artifact |
| --- | --- |
| Context, capability, concept/type, flow, state, dependency/interface | [ARCHITECTURE-BUNDLE.md](ARCHITECTURE-BUNDLE.md) |
| User-facing flow and interaction states | [UX-PLAN.md](UX-PLAN.md) |
| Consequential decisions and rejected alternatives | [DESIGN-DECISIONS.md](DESIGN-DECISIONS.md) |
| Term consistency and non-promotion note | [GLOSSARY-CONSISTENCY.md](GLOSSARY-CONSISTENCY.md) |
| Value-order seed for planning | [IMPLEMENTATION-LAYERING-SEED.md](IMPLEMENTATION-LAYERING-SEED.md) |
| Design unit check | [DISTILL-DESIGN-VALIDATION.md](DISTILL-DESIGN-VALIDATION.md) |

## Technique Trace

| Technique | Applied design behavior | Evidence |
| --- | --- | --- |
| `sequence` | Context precedes design; Distill design check precedes plan. | Dispatch S1–S4. |
| `scu_swu_reduction` | Design starts with one node, one restatement, one source request, one proposal. | Architecture design acceptance and layering seed L0. |
| `recomposition_proof` | The one-node loop exercises the same build, Canvas, proposal, routing, and review boundaries needed for later nodes. | Distill design validation. |
| `validation_loop` | Schema/build/browser/human evidence is designed before implementation. | Architecture operations/interfaces and UX comprehension gate. |
| `owner_boundary_check` | Browser evidence is separated from DomainSpec/Craft/Whisper/research acceptance. | Context and state views; RDL-D02/D03/D08/D10. |
| `artifact_contract_bridge` | Roadmap inputs become a generated, fingerprinted presentation without transferring authority. | Architecture operations RDL-O01. |
| `state_namespace_boundary` | Roadmap, presentation copy, Canvas events, and review status have distinct owners. | Design context authority table and dispatch boundaries. |
| `residue_ledger` | Source resolver, identity, collaboration, and production authorization remain named deferrals. | Decisions non-decisions and UX deferred section. |

## Design Gate

Status: **pass**.

The six views agree on the same smallest loop, state bindings, owner boundaries,
and deferred scope. Distill found no acceptance-critical gap requiring design
reopening. This pass permits planning; it does not authorize implementation.

