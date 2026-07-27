---
module: body-war-suggested-track-ontology-domainspec-integration
version: current
status: candidate-local
updatedAt: 2026-07-27
docType: glossary
---

# Glossary

| Term | Meaning in this track | Authority |
| --- | --- | --- |
| Canonical DomainSpec node | The consumer-owned minted node whose `body.logic` is the executable source for CT-2. | Body War source owner |
| Ontology entry | A governed statement of concept meaning, relations, evidence, confidence, promotion state, next gate, and contradiction path. | Body War local ontology owner |
| Ontology fixture | The bounded local entry set used by T-ONTOLOGY-001. Passing it does not promote the entries. | Test evidence only |
| `needs_evidence` | A SuggestedTrack state meaning the suggestion exists without accepted source-backed evidence. | Body War domain sources |
| Bridge manifest | A sidecar that binds exact ontology entry digests to exact DomainSpec node, module, and clause digests. | Body War integration contract |
| Standalone witness | A test whose inputs and verdict do not depend on either of the other standalone lanes. | Work-pack test contract |
| Integration witness | A test that composes already-valid ontology and DomainSpec outputs and proves binding enforcement. | Work-pack test contract |
| Promotion state | The ontology lifecycle state such as `candidate` or `promoted`; it is not set by a test. | Ontology lifecycle owner |
| Development profile | The current DomainSpec profile that admits selected kinds, edges, and node logic without granting release. | DomainSpec v2 profile owner |
| Proof receipt | A deterministic record of sources, digests, cases, observations, and verdict. | Test runner |
| Claim ceiling | The strongest statement supported by the evidence. Here it is experimental CT-2 integration only. | Lifecycle owner |

## Consistency Rules

- “Canonical” refers to the DomainSpec executable rule source, not ontology
  promotion.
- “Pass” refers to the named test boundary only.
- “Integrated” does not mean released, production-ready, or ontology-promoted.
- Ontology and DomainSpec align through IDs and digests; neither silently
  overwrites the other.

