---
id: digest.arcanum_ontology_vault_harness
sourceArea: arcanum
sourcePaths:
  - arcanum/arcana/ontology-vault/README.md
  - arcanum/spells/ontology-harness/README.md
status: candidate-digest
updatedAt: 2026-05-19
branches:
  - knowledge-governance
  - bridge
---

# Source Digest: Arcanum Ontology Vault And Harness

Sources:

- [Ontology Vault](../../../arcanum/arcana/ontology-vault/README.md)
- [Ontology Harness](../../../arcanum/spells/ontology-harness/README.md)

Ledger: [../source-ledger.md](../source-ledger.md)

## Why This Source Matters

Ontology Vault and Ontology Harness provide the governance machinery for turning scattered repository knowledge into explicit ontology.

They already define the core pattern CyberAlchemy needs:

```text
inventory
  -> ontology-vault
  -> context-builder
  -> branch maps, confidence reviews, bridge validation, and context proof
```

## Compiled Concepts

### Ontology Vault

Ontology Vault helps a repository move from scattered notes, sessions, discoveries, premises, and conventions into a traceable ontology.

It makes explicit:

- knowledge roles;
- maturity states;
- confidence;
- edge rules;
- promotion decisions;
- premise reviews;
- convention changes;
- delegated evidence;
- synthesis findings.

### Ontology Harness

Ontology Harness composes:

- `inventory`;
- `ontology-vault`;
- `context-builder`.

It is used when source knowledge needs mapping, distillation, promotion gates, and proof that future tasks can retrieve ontology evidence compactly.

### Branch-Aware Path

When business intent and system evidence both exist, Ontology Harness can run a branch-aware path:

```text
map business ontology
  -> map system ontology
  -> validate bridge
  -> find drift and traceability gaps
```

### Output Artifacts

The vault and harness can produce:

- ontology map;
- business ontology map;
- system ontology map;
- bridge map;
- traceability matrix;
- drift report;
- session distillation report;
- premise review;
- confidence promotion or demotion report;
- convention change plan;
- validation report;
- context-builder proof.

## CyberAlchemy Adaptation

CyberAlchemy should use Ontology Harness to validate the new agentic ontology pack:

```text
cyberAlchemy/ontology/source-digests/
  -> source-ledger
  -> thick ontology entries
  -> promotion records
  -> context-builder proof
```

Operational Ontology should be treated as a branch-aware extension, not as loose notes.

## Candidate Ontology Claims

| Claim                                                                       | Branch               | Candidate Entry                            |
| --------------------------------------------------------------------------- | -------------------- | ------------------------------------------ |
| Ontology promotion should route through ontology-vault or ontology-harness. | knowledge-governance | `route-policy-ontology-promotion`          |
| Context proof is required before ontology is considered agent-usable.       | knowledge-governance | `gate-context-builder-proof`               |
| Bridge claims must cite both intent and realization evidence.               | bridge               | `gate-bridge-validation`                   |
| Session distillation creates candidates, not final authority.               | knowledge-governance | `rule-session-distillation-candidate-only` |

## Tensions And Promotion Gaps

- The local ontology pack now has source digests, but they are candidates until inventory and ontology-harness validate them.
- Context Builder proof should become a real gate for the first working loop.
- Promotion records still need a concrete directory and examples.

## Agent Payload

Use this digest when deciding which capability owns ontology work:

```text
Need source summaries? inventory
Need ontology roles, confidence, premise review, or promotion? ontology-vault
Need combined inventory + ontology + context proof? ontology-harness
Need task-sized retrieval? context-builder
Need consequential decision? decision-gate
```
