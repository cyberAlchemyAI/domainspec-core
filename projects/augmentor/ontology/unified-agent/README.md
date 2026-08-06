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
- `views/intent-route.json` maps Augmentor intent through the deterministic,
  zero-authority resolver boundary and retained product/runtime owners.
- `views/README.md` gives a compact human-readable cross-view map.
- `NODE-INDEX.md` provides the review index for all candidate concepts.
- `residue.json` preserves missing owners, adapters, and witnesses.
- `explanations/beginner.json` gives every node and lane six progressive
  explanation lenses. The interface presents them as **What it means**,
  **What exists today**, **How it works**, **Show an example**,
  **Compare it to something familiar**, and **What it cannot do** while
  preserving the canonical fields underneath.
  Each node also has a short friendly name. Direct explanations use familiar
  words and leave examples and metaphors to their optional lenses.
- `ontology-visualization.html` is a standalone, source-generated interactive
  view of the complete ontology.
- `visualization/template.html` owns the visualization layout and interaction
  behavior without external assets or network dependencies. Beginner copy is
  shown first; canonical names, formal definitions, IDs, owner routes, and
  source references stay inside collapsed technical details.
- `scripts/build-visualization.mjs` embeds the current ontology sources and
  detects stale generated output.
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

Intent routing expands the classification seam without replacing its owners:

```text
ContextSnapshot → IntentRouteRequest ─┐
                                      ├→ ResolverInvocation
RouteCatalogProjection ───────────────┘          │
                                                 ▼
                                         RouteDisposition
                                                 │ may inform
                                                 ▼
                                          RouteDecision
```

`RouteDisposition` is always zero-authority and remains distinct from
`RouteDecision`, `StrategyProposal`, `ApprovalRecord`, `Dispatch`, `Run`, and
`JudgmentReceipt`.

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
node projects/augmentor/ontology/unified-agent/scripts/build-visualization.mjs --check
node projects/augmentor/ontology/unified-agent/scripts/validate.mjs
node projects/augmentor/ontology/unified-agent/tests/unified-agent-ontology.test.mjs
node --test projects/augmentor/ontology/unified-agent/tests/visualization.test.mjs
node projects/augmentor/ontology/unified-agent/tests/visualization.browser.mjs "$(npm root -g)/playwright"
```

The project-specific UX evidence runner accepts the Playwright module root,
managed preview URL, generated HTML path, and an output directory. It captures
screenshots, an interaction trace, ARIA output, layout measurements, findings,
and explicit human-review residue under `output/playwright/ux-validator/`.

Passing validation proves package shape, source-digest integrity, endpoint
resolution, view resolution, and the declared non-authority boundaries. It does
not prove routing, durable memory, reasoning, promotion, release, or production
readiness.
