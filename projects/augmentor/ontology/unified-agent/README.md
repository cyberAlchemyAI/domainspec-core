# Augmentor Unified-Agent Ontology

Status: `candidate-local`

Authority effect: `none`

Release admission: `not-granted`

## Purpose

This package is a private, source-bound ontology of the Augmentor agent
experience. It maps the meaning, runtime, knowledge, and authority-bridge
planes needed for one conversational interface across routing, sessions,
subagents, memory, and bounded reasoning.

The package follows the CyberAlchemy v2 candidate node, relation, branch-view,
and package contracts. It does not make Augmentor an authority owner and it
does not change ResonantOS runtime behavior.

## Ownership Boundary

- `domainspec-core` owns this private candidate read model.
- `../workspace-resonant/2.0.0-alpha` retains product and runtime ownership.
- CyberAlchemy v2 owns the ontology contract and private authority vocabulary.
- Dispatch Spec and Orchestrate retain route-validation and execution lifecycle
  ownership.
- Source and memory providers retain their own bytes and trusted-write policy.
- The Augmentor meaning owner, disposable-index owner, production route owner,
  and canonical knowledge writer remain unresolved.

No private CAV2 term or owner binding is projected into ResonantOS by this
package. A neutral generated projection would require a separate owner
decision.

## Package Contents

- `profile.json` fixes the package boundary and blocked outputs.
- `sources.json` binds every load-bearing source to its SHA-256 digest.
- `nodes/nodes.json` contains candidate concepts with confidence and challenge
  contracts.
- `relations/relations.json` contains directed, owner-routed candidate
  relations.
- `views/experience.json` maps the user-facing conversational path.
- `views/runtime.json` maps proposals, approval, Dispatch, Runs, joins, and
  result consumption.
- `views/knowledge.json` maps provider-owned sources, derived retrieval,
  intake, and ontology handoff.
- `views/authority-bridge.json` maps the non-authorizing reasoning and
  authority boundaries.
- `views/README.md` gives a compact human-readable cross-view map.
- `NODE-INDEX.md` provides the review index for all candidate concepts.
- `residue.json` preserves missing owners, adapters, and witnesses.
- `scripts/validate.mjs` validates hashes, contracts, endpoints, views, and
  forbidden authority movement.

## Core Sequences

Ordinary conversation:

```text
ConversationThread
→ Interaction
→ SourceRecord references
→ ContextSnapshot
→ RouteDecision
→ grounded presentation
```

Consequential work:

```text
StrategyProposal
→ ApprovalRecord
→ Dispatch
→ Run
→ LifecycleJoin
→ ResultConsumption
```

Knowledge evolution:

```text
MemoryIntakeRequest
→ provider disposition
→ Inventory-validated candidate evidence
→ OntologyCandidate
→ named-owner AuthorityDecision
```

Reasoning remains separately bounded:

```text
ContextSnapshot
→ ReasoningRequest
→ JudgmentReceipt
→ independent exact-effect gate
```

A `JudgmentReceipt` is never approval, an effect gate, an effect owner, or an
effect runtime.

## Validation

Run:

```bash
node projects/augmentor/ontology/unified-agent/scripts/validate.mjs
node projects/augmentor/ontology/unified-agent/tests/unified-agent-ontology.test.mjs
```

Passing validation proves package shape, source-digest integrity, endpoint
resolution, view resolution, and the declared non-authority boundaries. It does
not prove routing, durable memory, reasoning, promotion, release, or production
readiness.
