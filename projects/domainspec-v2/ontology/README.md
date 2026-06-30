# DomainSpec v2 Ontology Instantiation

Status: candidate local instantiation surface
Owner: DomainSpec v2 owner
Authority effect: none by itself

## Role

This folder is the local place where DomainSpec v2 can sketch ontology entries
that instantiate the CyberAlchemy v2 ontology package shape without becoming a
second base ontology package.

Entries here are candidate/local until a DomainSpec v2 owner route promotes
them. They may cite CyberAlchemy v2 as harvested precedent and modeling shape,
but they do not make CyberAlchemy v2 the decision owner for DomainSpec v2.

## Source Boundaries

| Source | Allowed Reading | Forbidden Reading |
| --- | --- | --- |
| `authority/AUTHORITY-MODEL.md` | Local authority kinds, owner routes, non-collapse rules, and local governance decisions. | A CAV2 authority-kind amendment or public CAV2 schema change. |
| `authority/source-spine.md` | Source posture: CAV2 and v1 are harvested precedent and supporting source only. | A resolution path through CAV2 or v1. |
| `impl/spec/` | DomainSpec language primary source: taxonomy, relationships, axioms, test pipeline, and constitution. | A promoted implementation contract or runtime-conformance verdict. |
| `cyberAlchemy-v2/ontology/` | Candidate node/package shape to instantiate locally. | Base authority over DomainSpec v2 decisions. |
| `cyberAlchemy-v2/specs/` | Promoted contract target after gates. | Raw source for local ontology candidates or a place to write from this folder directly. |

## Local Entry Rules

Every local ontology entry should declare:

- `node_id`: a local stable identifier.
- `instantiates`: a CAV2 package concept such as `concept.authority_envelope`,
  `concept.spec`, `concept.decision`, or `concept.residue`.
- `candidate_status`: `candidate`, `reviewed-candidate`, `deferred`,
  `blocked`, or `projected`.
- `owner_route`: the DomainSpec v2 owner route that can review, promote, block,
  or retire the entry.
- `source_refs`: concrete local source paths.
- `confidence`: top-level `evidence_confidence` and
  `commitment_confidence`.
- `challenge_contract`: protocol-only challenge details; not node confidence,
  not node residue, not a verdict, and not promotion.
- `forbidden_collapse`: what this candidate must not be mistaken for.

## Candidate Example

The example below is not promoted. It demonstrates how a local DomainSpec v2
governance concept can instantiate the CAV2 node shape while keeping the local
owner route in charge.

```yaml
node_id: dsv2.ontology.validation-governance
instantiates: concept.authority_envelope
label: Validation Governance
local_authority_kind: validation-governance
candidate_status: candidate
owner_route: projects/domainspec-v2/authority/AUTHORITY-MODEL.md#authority-kinds
source_refs:
  - projects/domainspec-v2/authority/AUTHORITY-MODEL.md#authority-kinds
  - projects/domainspec-v2/authority/source-spine.md#source-families
  - projects/domainspec-v2/impl/spec/TEST-PIPELINE.md
  - projects/domainspec-v2/impl/spec/TAXONOMY.md
confidence:
  evidence_confidence: medium
  commitment_confidence: medium
challenge_contract:
  challenge_response: owner_review
  valid_challenge_modes:
    - evidence
    - contradiction
    - owner_review
    - validation
  contradiction_edges:
    - dsv2.ontology.entry-that-treats-derived-test-as-runtime-correctness
  validation_edges:
    - projects/domainspec-v2/impl/tools/validate-doc-links.ts
    - projects/domainspec-v2/impl/tools/validate-relationships.ts
  owner_route: validation-governance
  resolution_gate: projects/domainspec-v2/authority/decisions/
  blocking_questions:
    - Does the entry conflate build-time fidelity with runtime conformance?
    - Does the entry route authority through CAV2 or v1 instead of DomainSpec v2?
  challenge_residue_route: projects/domainspec-v2/research/
residue:
  - L2 attestation seal pending for the ratified governance kind.
forbidden_collapse:
  - Not a CAV2 closed authority-kind enumeration change.
  - Not a CyberAlchemy v2 spec promotion.
  - Not runtime correctness or implementation conformance.
  - Not authority over DomainSpec v2 without the local owner route.
```

## Spec Boundary

DomainSpec v2 may use local ontology candidates to organize what a feature,
governance object, or spec concept appears to mean. That does not write a spec
and does not promote a contract.

Promoted contracts live behind gates. For CyberAlchemy v2, `cyberAlchemy-v2/specs/`
is a promoted contract target after research and architecture gates. For
DomainSpec v2, `impl/spec/` is local primary source material and imported
implementation-home evidence, not proof that an ontology candidate has been
promoted.

## Promotion Path

```text
local source refs
  -> candidate ontology entry
  -> DomainSpec v2 owner review
  -> decision, promotion, block, or defer record
  -> optional generated/read-model projection
```

No arrow is automatic. A candidate can be useful for navigation while still
having no authority effect.
