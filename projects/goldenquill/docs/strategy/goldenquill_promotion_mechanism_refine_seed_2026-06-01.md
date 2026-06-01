---
title: GoldenQuill Promotion Mechanism Refine Seed
date: 2026-06-01
status: strategy-proposal
dispatch: docs/strategy/goldenquill_promotion_mechanism_route_2026-06-01.dispatch.json
seed_for: refine
---

# GoldenQuill Promotion Mechanism Refine Seed

## Target

GoldenQuill promotion mechanism for ontology DAG, grant-run evidence, reusable
lessons, card deltas, org memory, and governed ontology relations.

## Desired Outcome

A refined, non-executed design and implementation plan for the promotion
mechanism, including:

- the smallest coherent promotion unit;
- owner boundary rules;
- state machine;
- validation fixtures;
- real-world outcome evidence and KPI tracking;
- first implementation slice;
- handoff route to Task Session or Ontology Vault decision-gate.

## Preset

`standard`

## Research Mode

`bounded-research`

The local bounded research baseline already exists in:

- `docs/strategy/goldenquill_promotion_mechanism_research_2026-06-01.md`
- `docs/strategy/goldenquill_promotion_mechanism_invoke_design_2026-06-01.md`
- `docs/strategy/goldenquill_promotion_mechanism_refresh_report_2026-06-01.md`

External KPI research has been added through the invoke refresh report. No
additional external research is needed before the first refine proposal unless
the refine review names a funder-family-specific KPI gap.

## Selected Technique Overlays

| Overlay | Why It Applies |
| --- | --- |
| baseline sequence | The route must preserve context, define/design, critique, distill, plan, and final synthesis. |
| x-ray for hidden structure | Promotion crosses evidence, ontology, inventory, card, org-vault, and Logician boundaries. |
| toy-game for low-cost falsification | The design needs positive and negative fixtures before production mutation. |
| memory-residue for context recovery | Prior DAG research and memory architecture findings are material. |
| protected-context for authority boundaries | Org scope and source authority are core safety constraints. |
| lifecycle-depth metrics | Wins, rejections, submissions, review movement, and post-award reporting must be tracked without turning dashboard observations into promotion authority. |

## Proposed Subagent Strategy

Status: `recommended`, not required.

Roles:

| Role | Ownership |
| --- | --- |
| promotion-governance-reader | Inspect Ontology Vault PromotionRecord and Inventory promotion-owner constraints. |
| goldenquill-memory-reader | Inspect MemoryEvidencePacket, memory mesh tasks, and card authority boundaries. |
| validator-designer | Design toy positive and negative fixtures. |
| refinement-critic | Challenge whether PromotionCandidate is the right smallest unit. |
| grants-kpi-researcher | Challenge KPI definitions, denominators, and lifecycle-stage depth scoring. |

Join policy: parent synthesis.

Receipt requirements:

- source paths;
- candidate constraints;
- risks;
- recommended state or schema repairs;
- KPI denominator definitions;
- real-world evidence risks;
- blocked promotion questions.

Authorization: requires user permission before subagents or runtime-backed refine
stages run.

## Runtime Plan After Confirmation

1. Context Builder evidence baseline.
2. Invoke Define from the research/design packet.
3. Interrogation using `refine-review`.
4. Research decision: bounded research already satisfied unless a named gap
   appears.
5. Distill smallest coherent promotion unit.
6. Invoke Design revision.
7. Interrogation using `refine-design-review`.
8. Distill repair.
9. Invoke Plan for non-executed implementation plan.
10. Final Interrogation and Refine synthesis.

## Deferred Work

- Production schema mutation.
- GoldenQuill runtime implementation.
- Ontology Vault template promotion.
- Inventory schema changes.
- Signed-card governance changes.
- Org-vault memory mutation.
- Dashboard implementation.
- Real-world outcome importers.
- KPI-based promotion without owner approval.

## Added Refine Questions From Invoke Refresh

1. Are `GrantOutcomeEvent`, `ApplicationLifecycleState`, and
   `GrantKpiObservation` separate objects, or projections over existing DAG
   nodes?
2. What is the smallest useful stage-depth enum that does not overfit federal
   grants?
3. Which KPIs are dashboard-only, and which may create promotion candidates?
4. How should GoldenQuill generalize lessons from rejections without leaking
   private org or funder feedback?
5. Should wins and rejections both create Reflection Packet candidates by
   default?
6. Which metric denominators must be stored to prevent misleading comparisons?
7. Can GoldenQuill's stage/outcome/validation split become a validator rule for
   grant lifecycle and outcome evidence?

## Confirmation Prompt

Confirm to run the validated refine strategy for the GoldenQuill promotion
mechanism, including the recommended subagent fanout?
