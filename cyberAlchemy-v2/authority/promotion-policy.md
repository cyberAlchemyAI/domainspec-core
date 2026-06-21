# Promotion Policy

Status: candidate local policy
Owner: CyberAlchemy v2

CyberAlchemy v2 promotes evidence by owner route, not by enthusiasm.

## Promotion Ladder

| State | Meaning | May promote to |
| --- | --- | --- |
| Source evidence | Authored or observed material in its original home. | Inventory candidate |
| Import candidate | Path-level staged authority material with source posture and promotion route. | Inventory candidate, ontology candidate, or local authority proposal |
| Inventory candidate | Source-backed lookup entry, evidence card, or EvidenceSet. | Ontology candidate or context pack |
| Ontology candidate | Branch map or thick entry with meaning, edges, confidence, and promotion path. | Definition, constitution, decision, or spec proposal |
| Local authority | Definition, constitution rule, discipline, decision, or promoted spec. | Implementation or validation work |
| Implemented behavior | Code, package, runtime adapter, or generated projection with tests or reports. | Release candidate |
| Stable repository asset | Maintained authority, implementation, docs, and validation evidence. | Standalone extraction |

## Required Gates

| Gate | Use when | Result |
| --- | --- | --- |
| definitions-governance | A term becomes load-bearing across artifacts. | Update definitions, index, and drift audit. |
| discipline-governance | A recurring practice needs a card, catalog row, and hardening route. | Formalize discipline or route elsewhere. |
| constitution-governance | A structural rule should constrain future artifacts. | Add or compose constitution rules and validation model. |
| authority import | Scattered definitions, constitutions, axioms, or glossaries must be staged before promotion. | Update import ledgers and classify source posture. |
| decision-gate | Public/private, scope, naming, ownership, or promotion is contested. | Human decision record. |
| task-session | A bounded implementation or mutation is ready to execute. | Work-pack execution and validation report. |

## Pass, Flag, Block

- Pass: evidence, owner, boundary, and validation surface are adequate for the
  next route.
- Flag: the next route may proceed with named risk and open questions.
- Block: mutation or promotion must stop until a decision, evidence, or
  validation gap is closed.

## Open Questions

### OQ-1. What evidence threshold is enough for standalone extraction?

Context: this starter package gives structure, not enough runtime evidence.
Recommendation: require at least one promoted architecture map, one validation
report, and a public/private scrub before extraction. Status: OPEN.
