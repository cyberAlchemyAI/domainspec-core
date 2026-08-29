# CyberAlchemy Language Project — Craft View

This is the human view of [`.craft/ledger.yml`](.craft/ledger.yml), which is the
machine-readable source of truth. All definitions here are candidate-local.

## Current state

The package now separates one concept into the meanings needed by different
participants:

| Surface | Term | Meaning |
| --- | --- | --- |
| Business | Recommendation | Evidence-backed advice that does not make or authorize a decision. |
| Governance domain | Rule Review Recommendation | Advice about how a reviewed Governance Rule should be treated. |
| Product | Decision Support Output | The review result shown to help an authorized owner decide. |
| System | Open realization | `DS-D1.2 Value Object` and `DS-D1.1 Entity` remain candidates. |

The root gate is `flag`, not `block`: language work can continue, but DomainSpec
modeling, formalization, and implementation binding cannot select a realization
until the Governance owner answers the identity and lifecycle question.

The Governance kernel input slice now uses one preferred expression across
business, domain, and product language:

| Term | Meaning | DomainSpec candidate realization | Authority boundary |
| --- | --- | --- | --- |
| Governance Program | Named, versioned evaluation instructions. | `DS-D1.1 Entity` | Declares required authority; grants none. |
| Governance Request | One exact proposed consequence. | `DS-D1.2 Value Object` | Is not an owner request, permission, or action. |
| Governance Fact | One verifier-admitted scoped proposition. | `DS-D1.2 Value Object` | Is not Evidence, Authority, or universal truth. |
| Governance Fact Set | Bounded Facts for one Program and Request. | `DS-D1.2 Value Object` | Is not repository state or a lifecycle hash. |

This slice is owner-reviewed candidate language. Its context remains `flag`
because the system-runtime ontology, verifier contracts, Rust types, Runtime
Contract acceptance, and effect adapters do not yet exist.

## Contexts

- `CTX-LANGUAGE-MEANING` owns business, domain, and product meanings.
- `CTX-LANGUAGE-EDGES` owns proposed edge verbs and collision records.
- `CTX-LANGUAGE-REALIZATION` owns the open DomainSpec classification.
- `CTX-LANGUAGE-GOVERNANCE-KERNEL` owns Program, Request, Fact, Fact Set, and
  their CyberAlchemy authority bindings.

## Candidate edge vocabulary

- `offers`: Governance Assessment → Rule Review Recommendation.
- `informs`: Rule Review Recommendation → Governance Decision.
- `requires_facts`: Governance Program → Governance Fact Set.
- `is_evaluated_under`: Governance Request → Governance Program.
- `contains_fact`: Governance Fact Set → Governance Fact.

Both are proposed. Each has a business sentence, product consequence, and a
non-collapse witness in [`edge-vocabulary.json`](edge-vocabulary.json).

## Open decisions

### `DEC-LANGUAGE-REALIZATION-001`

Does Rule Review Recommendation require independent identity and lifecycle, or
is immutable field equality sufficient? Until the owner answers, neither
`Value Object` nor `Entity` is selected.

### `DEC-LANGUAGE-PRODUCES-001`

The Governance product ontology uses `produces` for Capability → Output, while
DomainSpec DS-D2 uses it for Operation → Event. The shared spelling is not
shared meaning. A qualified business verb, explicit bridge, scoped homonym, or
deferral needs owner review.

## Next move

Use the Program–Request–Fact language and
[`authority-bindings.json`](authority-bindings.json) as Define input for the
candidate Governance system-runtime ontology and verifier-contract design. The
Recommendation exercise and `produces` collision remain open independently.

## Boundary

Craft tracks work and residue. This package does not promote definitions, admit
a Discipline, accept a Definition Pack, promote a candidate DomainSpec semantic
mapping into DomainSpec authority, accept a Runtime Contract, authorize
implementation, enforce governance, publish, or deploy anything.
