---
module: cyberalchemy-agentic-system
slice: 03-promotion-governance
status: candidate
updatedAt: 2026-05-19
docType: slice-work
---

# Slice 03: Promotion Governance

Work layer: [CyberAlchemy Agentic System](../../README.md)
Concepts: [concepts.md](concepts.md)
Navigation: [agentic-system-navigation.md](../../../agentic-system-navigation.md)
Deep dive: [agentic-system-deep-dive.md](../../../agentic-system-deep-dive.md)

## Purpose

Define the promotion system that decides how raw observations, memory, inventory entries, operational lessons, and ontology candidates become more authoritative.

This is the slice that protects the system from accidental canon.

## Already Done

- The deep dive defines the authority ladder, promotion states, gates, confidence split, decision matrix, non-promotion rules, and promotion record shape.
- Necronomicon's knowledge substrate flow already defines the authority ladder from raw interaction to bridge-validated operating context.
- Ontology Vault already owns premise review, confidence promotion, convention updates, and validation.
- The ontology entry model includes a promotion section for every entry.

## Needs To Be Done

- Create `cyberAlchemy/ontology/promotion-rules.md`.
- Create `cyberAlchemy/ontology/promotion-records/`.
- Maintain [knowledge-governance-authority-ladder.md](../../../ontology/entries/knowledge-governance-authority-ladder.md) as the ontology-owned ladder rule.
- Define promotion record filenames and required frontmatter.
- Decide which promotions require `decision-gate`.
- Create first promotion records for the initial ontology entries.
- Add review triggers for demotion, contradiction, and retirement.

## Implementation Slice

1. Create promotion rules from the deep dive:
   - authority ladder,
   - states,
   - gates,
   - confidence matrix,
   - non-promotion rules,
   - record template.
2. Treat [knowledge-governance-authority-ladder.md](../../../ontology/entries/knowledge-governance-authority-ladder.md) as the candidate ontology entry for the ladder.
3. Create first promotion records:
   - `promotion.operational-ontology-candidate`
   - `promotion.memory-treated-as-authority-failure-mode`
   - `promotion.saturn-convergence-loop-candidate`
4. Route privacy-sensitive rules through `decision-gate`.
5. Add promotion state to every first ontology entry.
6. Run context-builder proof for one promoted or reviewed candidate.

## Acceptance Checks

- No memory observation can become ontology authority without passing through inventory or explicit review.
- Every promotion decision records evidence confidence and commitment confidence.
- Every promoted entry has a rollback, retirement, or contradiction path.
- Decision-gate is required when promotion changes privacy, behavior, policy, architecture, or capability contracts.
- The system can reject or demote a claim, not only promote it.

## Links

| Role                       | Link                                                                                                           |
| -------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Promotion section          | [agentic-system-deep-dive.md](../../../agentic-system-deep-dive.md)                                            |
| Entry model promotion rule | [agentic-system-ontology-entry-model.md](../../../agentic-system-ontology-entry-model.md)                      |
| Knowledge substrate flow   | [KNOWLEDGE-SUBSTRATE-FLOW.md](../../../../arcanum/spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md) |
| Ontology Vault             | [Ontology Vault](../../../../arcanum/arcana/ontology-vault/README.md)                                          |
| Ontology Harness           | [Ontology Harness](../../../../arcanum/spells/ontology-harness/README.md)                                      |
| Decision Gate registry     | [Sigil Registry](../../../../arcanum/registry/SIGILS.md)                                                       |
