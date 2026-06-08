# REFINE-SEED-PROPOSAL — Lane B detailed design

- Run id: `ontologize-lane-b-design-20260608`
- Target: Lane B of the ontologize delivery method — make it buildable.
- Operator sentence: "lane B".

## Interpretation

Refine Lane B from a sketch ([DELIVERY-LANES.md](../../../DELIVERY-LANES.md) "Lane B") into a buildable
design: confirm the four-layer mapping against real Arcanum sigil capabilities, and design the five
named bridges (signed classification register; runtime event→ontology-card dispatch; the 11-rule lint
schema; proof-harness for metric drift; reflection cadence).

## Source context (local-first)

- ontologize: DELIVERY-LANES.md, DAG-AND-METRICS.md, DESIGN.md, prior lane-designer receipts.
- Arcanum skills (read-only): `.claude/skills/{inventory,ontology-vault,context-builder,necronomicon,
observability-setup,observed-invocation-loop,workflow-reflect,decision-gate,sigil-development}/SKILL.md`.

## Write scope

- New: `projects/ontologize/LANE-B-DESIGN.md`.
- Tighten: DELIVERY-LANES.md (link the detailed design), WORK-PACK.md (a Lane-B-bridges build task).
- Run evidence under this folder. Arcanum skills are read-only.

## Done criteria

1. Four-layer mapping confirmed against actual sigil capabilities (with skill paths).
2. Each of the 5 bridges designed: what it is, reuse-existing-sigil vs net-new build, an MVP, rough cost, owner.
3. A build order (which bridge first; what unblocks the logistics/hybrid pilot).
4. Honest gap statement: what Arcanum gives for free vs what must be built.
5. Candidate-tagged; no canonical promotion; no pricing/clients.

## Validation surface

- Each bridge maps to a cited Arcanum capability (skill path) or is marked net-new with a reason.
- Dispatch route validates against the dispatch-spec validator.
- Final interrogation confirms each bridge has a decidable build/reuse verdict + MVP, not a wish.

## Preset / research / subagents

- Preset: standard. Research: no-research (local). Subagents: recommended, **approved** — 1
  capability-surveyor. Join: parent_synthesis.
