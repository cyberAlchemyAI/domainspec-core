---
title: GoldenQuill Memory And Knowledge Handling Refine Seed Proposal
date: 2026-05-31
target: goldenquill-memory-knowledge-handling
status: proposed
---

# Refine Seed Proposal

## Seed

The client is right that memory/knowledge is a layer that needs work, but the repository already has several partial layers. The next move should not be "add memory" in the abstract. It should define a Memory/Knowledge Mesh that coordinates existing retrieval, lessons, cards, knowledge packs, vault reads, reflection packets, and substrate mutation gates under Arcanum-compatible ownership rules.

## Refined Problem

GoldenQuill currently has useful memory and knowledge pieces:

- Read-only unified retrieval across multiple registers.
- MEMORY.md consolidation and auto-trigger mechanics.
- Lessons/institutional memory.
- Signed cards as reusable domain knowledge.
- Knowledge packs for Scribe terminology.
- Vault-owned read skills and research DB boundary.
- Prototype memory mutation contracts in `golden_quill_substrate`.
- Reflection Packet specs/gates that point toward cross-cycle learning.

The weakness is not total absence. The weakness is that these surfaces do not yet share a single production mental model: which surface stores what, who may mutate it, how retrieval is ranked, how evidence becomes reusable memory, and when a candidate becomes canonical.

## Refined Target

Design a production-ready Memory/Knowledge Mesh for GoldenQuill that works well with Arcanum:

- Arcanum Inventory handles evidence cards, indexes, retrieval packets, and non-authoritative handoffs.
- Arcanum Ontology handles meaning roles, branch context, and semantic governance.
- GoldenQuill Vault handles authoritative per-org and shared persisted state.
- GoldenQuill Logician handles gates, signatures, org isolation, and promotion checks.
- Invoke authors the design/plan artifacts.
- Task Session implements bounded pieces after approval.

## Done Criteria

- Memory/knowledge surfaces are classified by authority, scope, mutability, and maturity.
- Existing machinery is reused where it already exists.
- New improvements are scoped as a coherent layer, not scattered fixes.
- The design includes six Invoke design views.
- The next route is a plan or task-session candidate, not hidden implementation.
