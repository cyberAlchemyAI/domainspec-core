---
id: agentic.knowledge_governance_authority_ladder
type: AuthorityLadder
branch: knowledge-governance
status: candidate
owner: CyberAlchemy AI
updatedAt: 2026-05-19
evidenceConfidence: high
commitmentConfidence: medium
---

# Knowledge Governance Authority Ladder

## Content

Definition:

The Knowledge Governance Authority Ladder defines the allowed progression from raw evidence into reusable inventory, governed ontology, reviewed confidence, and downstream route, capability, specification, or context updates.

Purpose:

Prevent knowledge from either disappearing after a session or becoming authoritative too quickly.

Scope:

- Includes source-backed knowledge, session evidence, memory observations, telemetry, operational lessons, ontology candidates, premise review, confidence review, promoted ontology entries, constitutions, axioms, and bridge-validated operating context.
- Excludes direct promotion from raw memory, unreviewed telemetry, pointer-only ontology entries, and global rules inferred from local observations.

Examples:

- A source document becomes an inventory source summary, then a typed inventory entry, then a thick ontology candidate.
- A repeated route miss becomes session evidence, then an operational lesson candidate, then a reviewed ontology entry if evidence and scope survive promotion gates.
- A privacy-sensitive user workflow pattern remains memory until a decision gate defines whether it can influence ontology-guided behavior.

Non-examples:

- A single conversation preference becoming a permanent route policy.
- A telemetry signal directly mutating a sigil definition.
- A source summary treated as promoted ontology without confidence review.

## Context

Use when:

- deciding whether a claim can guide future agents;
- designing inventory-to-ontology flow;
- evaluating memory or telemetry as evidence;
- reviewing promotion, demotion, contradiction, or retirement;
- preparing context for ontology-harness or Context Builder.

Do not use when:

- the task only needs a temporary answer and no durable knowledge change;
- the claim is clearly local and has no future retrieval value;
- a human decision is required but has not happened.

Applies to:

- inventory entries;
- ontology candidates;
- operational lessons;
- memory patterns;
- context solution cards;
- route policies;
- capability updates;
- bridge claims.

Invalidated when:

- a newer ontology convention replaces the ladder;
- promotion states are renamed or restructured;
- evidence shows the ladder allows unsafe authority jumps;
- decision-gate changes the governance contract.

Operational constraints:

- Memory and telemetry can feed the ladder, but they do not skip it.
- Inventory is reusable evidence, not final ontology authority.
- Ontology candidates can guide agents only when candidate status and confidence are visible.
- Consequential behavior changes require decision or lifecycle owner review.

## Agent Payload

Summary:

Before treating knowledge as reusable authority, identify which ladder state it occupies and which owner can move it forward.

Source-material path:

```text
raw source
  -> inventory source summary
  -> typed inventory entry
  -> thick ontology candidate
  -> premise or confidence review
  -> promoted ontology entry
  -> route, capability, specification, or context update
```

Session-operational path:

```text
raw interaction
  -> session evidence
  -> discovery baseline
  -> inventory knowledge
  -> ontology candidate
  -> reviewed premise
  -> confidence decision
  -> constitution or axiom
  -> bridge-validated operating context
```

Required checks:

- Name the current ladder state.
- Cite source, inventory, memory, telemetry, or decision evidence.
- Check evidence confidence and commitment confidence.
- Check whether the claim affects behavior, privacy, architecture, capability contracts, or route policy.
- Route consequential promotions through ontology-vault, ontology-harness, or decision-gate.

Recommended route:

- Use `inventory` for source summaries and typed evidence entries.
- Use `ontology-harness` and `ontology-vault` for ontology candidates, premise review, confidence review, bridge validation, and convention changes.
- Use `decision-gate` when promotion changes behavior, privacy, policy, architecture, or capability contracts.
- Use Context Builder to prove promoted knowledge can be retrieved in task-sized form.

Pitfalls:

- Treating memory as authority.
- Treating inventory as ontology.
- Promoting pointer-only ontology entries.
- Hiding uncertainty after a route update.
- Mutating capabilities from telemetry without owner review.

## Edges

| Edge       | Target                                                                                                      | Evidence                                          | Notes                                 |
| ---------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------- |
| traced_to  | [agentic-system-ontology-synthesis.md](../../agentic-system-ontology-synthesis.md)                          | Knowledge Ladder section                          | Source-material ladder.               |
| traced_to  | [KNOWLEDGE-SUBSTRATE-FLOW.md](../../../arcanum/spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md) | Authority Ladder section                          | Session-operational ladder.           |
| traced_to  | [Ontology Vault](../../../arcanum/arcana/ontology-vault/README.md)                                          | Core concepts and output contracts                | Promotion and confidence ownership.   |
| traced_to  | [BUSINESS-ONTOLOGY.md](../../../arcanum/BUSINESS-ONTOLOGY.md)                                               | Axioms, constitutions, premises, confidence split | Authority roles.                      |
| traced_to  | [necronomicon-knowledge-substrate.md](../source-digests/necronomicon-knowledge-substrate.md)                | Compiled source digest                            | Authority ladder and memory boundary. |
| traced_to  | [arcanum-business-ontology.md](../source-digests/arcanum-business-ontology.md)                              | Compiled source digest                            | Authority roles and confidence split. |
| traced_to  | [arcanum-ontology-vault-harness.md](../source-digests/arcanum-ontology-vault-harness.md)                    | Compiled source digest                            | Promotion owner and context proof.    |
| applies_to | [Slice 03: Promotion Governance](../../agentic-system/slices/03-promotion-governance/README.md)             | Local slice contract                              | Promotion system implementation.      |
| constrains | [agentic-system-ontology-entry-model.md](../../agentic-system-ontology-entry-model.md)                      | Promotion rule                                    | Entry promotion behavior.             |
| constrains | [agentic-system-inventory-ontology-pipeline.md](../../agentic-system-inventory-ontology-pipeline.md)        | Inventory To Ontology Promotion Rule              | Source-to-ontology flow.              |

## Evidence

Inventory entries:

- Pending: `.arcanum/inventory/entries/cyberalchemy-agentic-system/knowledge-governance-authority-ladder.md`

Source references:

- [agentic-system-ontology-synthesis.md](../../agentic-system-ontology-synthesis.md)
- [agentic-system/slices/03-promotion-governance/concepts.md](../../agentic-system/slices/03-promotion-governance/concepts.md)
- [agentic-system-ontology-entry-model.md](../../agentic-system-ontology-entry-model.md)
- [agentic-system-inventory-ontology-pipeline.md](../../agentic-system-inventory-ontology-pipeline.md)
- [necronomicon-knowledge-substrate.md](../source-digests/necronomicon-knowledge-substrate.md)
- [arcanum-business-ontology.md](../source-digests/arcanum-business-ontology.md)
- [arcanum-ontology-vault-harness.md](../source-digests/arcanum-ontology-vault-harness.md)
- [KNOWLEDGE-SUBSTRATE-FLOW.md](../../../arcanum/spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md)
- [Ontology Vault](../../../arcanum/arcana/ontology-vault/README.md)
- [BUSINESS-ONTOLOGY.md](../../../arcanum/BUSINESS-ONTOLOGY.md)

## Confidence

Evidence confidence:

High. The ladder is supported by the synthesis, Necronomicon knowledge substrate, ontology-vault governance model, business ontology authority roles, and the inventory-to-ontology pipeline.

Commitment confidence:

Medium. The system should rely on the ladder as a candidate governance rule now, but it still needs inventory backfill and ontology-harness validation before promotion.

Scope of validity:

CyberAlchemy agentic-system knowledge governance, especially source ingestion, memory promotion, operational lessons, context solution cards, and capability updates.

Expiry condition:

Expires or requires review when ontology-vault conventions, promotion states, privacy policy, or inventory storage model changes.

## Promotion

Current state:

candidate

Next gate:

Create the matching inventory entry and run ontology-harness review.

Required evidence:

- Inventory source summary for the ladder.
- Typed inventory entry with source refs and contradictions.
- Ontology-harness validation of branch, type, edges, and promotion gates.
- Context Builder proof that a future task can retrieve the ladder without loading the whole corpus.

Contradiction path:

If the ladder allows unsafe authority jumps, creates too much overhead, or conflicts with a later decision-gate policy, mark this entry `contradicted` or `retired` and create a replacement governance entry.

## Maintenance

Review trigger:

- New promotion state added.
- Decision-gate changes privacy or authority behavior.
- Ontology-harness rejects branch or edge shape.
- Repeated agent work skips the ladder despite this entry.
- Context Builder cannot retrieve the ladder compactly for promotion tasks.

Owner route:

`ontology-harness` for validation, `ontology-vault` for promotion and confidence review, `decision-gate` for consequential changes.

Open questions:

- Should this become a constitution after the first working loop succeeds?
- Should source-material path and session-operational path remain one entry or split into two linked entries?
- What exact inventory entry schema should represent authority ladders?
