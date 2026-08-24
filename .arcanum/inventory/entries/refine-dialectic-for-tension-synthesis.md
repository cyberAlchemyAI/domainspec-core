---
tags:
  - inventory
  - synthesis
  - arcanum
  - dispatch-spec
  - subagents
  - residue
node_type: synthesis
is_session: false
layer: workflow
nature: reference
status: candidate
confidence: medium
created: 2026-07-30
sources:
  - arcanum/arcana/refine/SKILL.md#technique-overlay-policy
  - arcanum/arcana/refine/SKILL.md#strategy-preview-and-permission
  - arcanum/arcana/refine/REFINEMENT-LOOP.md#dispatch-technique-overlays
  - arcanum/arcana/refine/scripts/generate-refine-dispatch.py
---

# Refine `dialectic_for_tension`

This is a non-authority Inventory synthesis explaining one optional Refine
technique overlay. It does not redefine Refine, establish a canonical
definition of dialectics, authorize delegated execution, or promote a design
decision.

## Direct Definition

`dialectic_for_tension` is selected when a refinement target contains competing
principles, explore-versus-exploit pressure, or likely disagreement that should
not be collapsed into a premature answer.

The overlay adds three techniques while preserving the canonical ten-stage
Refine loop:

- `dialectic` preserves and tests competing positions;
- `zig_zag` moves evidence and objections between those positions so each can
  be revised;
- `residue_ledger` records disagreements or tradeoffs that remain unresolved.

The overlay changes critique, repair, synthesis, gate, or evidence expectations.
It is invalid as a decorative label that has no observable consequence in the
dispatch route.

## Explanatory Sequence

The following is an explanatory synthesis of the source contract:

1. Name the tension and the concern protected by each position.
2. Represent both positions strongly enough to survive serious criticism.
3. Test them against local evidence, constraints, failure cases, and each
   other.
4. Zig-zag the resulting objections back into revised positions.
5. Distill a synthesis, conditional decision, selected tradeoff, or owner-routed
   open decision.
6. Preserve anything not honestly resolved in the residue ledger.

The aim is not debate for its own sake or forced consensus. The aim is to
prevent a design from hiding a load-bearing contradiction.

## Refine Stage Effects

The current Refine dispatch generator recommends a `dialectic-critic` role when
this overlay is selected. That role owns stable disagreements,
counterarguments, and unresolved residue across:

- initial definition interrogation;
- design interrogation;
- final synthesis.

Recommended or required subagent execution remains permission-gated. Refine
must show the strategy, role ownership, join policy, and receipt requirements
before any delegated or runtime-backed stage executes.

## Illustrative Example

This example is explanatory synthesis, not a canonical Refine claim:

```text
Position A: automatically promote useful observations so the system learns
quickly.

Position B: require human approval so uncertain observations do not become
authority.
```

A possible synthesis is to automate collection, comparison, and ranking while
keeping canonical promotion with a named human or governed owner. If available
evidence cannot establish that boundary, the result remains an open decision
rather than a fabricated resolution.

## Use And Avoid

Use the overlay when:

- two or more legitimate principles pull the design in different directions;
- selecting one alternative too early would erase important constraints;
- disagreement is likely to affect the definition, design, or plan;
- unresolved tradeoffs need durable residue and an owner route.

Avoid it when:

- the target is straightforward and the baseline Refine sequence is sufficient;
- there is no evidence of a real tension;
- the work is an already-approved execution task rather than refinement;
- “dialectic” would merely rename ordinary review.

## Retrieval Boundary

This entry is a candidate Inventory read model. Exact convergence criteria,
participant roles, and acceptable residue remain dispatch-specific. Use the
canonical Refine skill and validated `REFINE-DISPATCH.json` as the operational
contract.
