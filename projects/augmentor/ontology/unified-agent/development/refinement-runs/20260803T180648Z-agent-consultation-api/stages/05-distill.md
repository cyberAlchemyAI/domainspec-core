# Stage 5: Distill The Smallest Coherent API Unit

## Distill Result

- Target context: a private, candidate-local Augmentor ontology that must be
  safely usable by an answering agent.
- Objective and output artifact: select the smallest coherent API design unit;
  produce a boundary suitable for detailed design.
- Mode and budget: Standard, one proposal track, two recursive rounds.
- Proposal tracks: one, with labeled Proposer and Balancer passes in the parent
  runtime.
- Recursive rounds: 2 of 2.
- Verdict: `pass`.

## Broad Concept Layer

The broad layer is “agent knowledge support.” It could contain retrieval,
reasoning, memory, routing, answer generation, feedback, and knowledge writes.
That layer is too broad because these behaviors have different owners and
failure effects.

## Role Conversation Trace

### Round 1

- Proposer claim: build one knowledge API with search, explanation, reasoning,
  answer generation, and feedback.
- Evidence or assumption: one interface would appear simpler to the caller.
- Balancer objection category: ownership collapse and hidden effects.
- Objection: answer generation, reasoning, and feedback writes would make a
  read API own decisions and state it does not own.
- Reconciliation: remove reasoning, answer generation, and all writes. Keep a
  separate answering-agent adapter.

### Round 2

- Proposer claim: expose several endpoints directly over ontology files.
- Evidence or assumption: the current JSON structure already contains nodes,
  relations, views, sources, and explanations.
- Balancer objection category: privacy, coupling, and evolution.
- Objection: direct file access leaks private structure and couples callers to
  a candidate package layout.
- Reconciliation: expose one versioned consultation boundary over a neutral
  projection. Logical operations are request kinds, not separate owner services.

## Current Smallest Coherent Unit

`ConsultationBoundary` is one read-only operation:

```text
consult(request: ConsultationRequest) -> ConsultationResponse
```

The request carries verified caller context, one logical query, a projection
scope, and limits. The response carries one fail-closed status and bounded
evidence items with source, freshness, confidence, ownership, and claim limits.

The unit includes four inseparable contracts:

1. request schema;
2. response and evidence-item schema;
3. status and error algebra;
4. answering-agent consumption rules.

Removing any one makes the remaining API unsafe or unusable. Protocol adapters,
indexes, caches, and product UI can be added around this unit later.

## Optimization Point

This unit is small enough to implement first with a deterministic fixture
projection and large enough to support a full question-to-evidence-to-answer
test. Splitting the answer rules from the response schema would hide the most
important consumer contract. Adding HTTP, a graph database, reasoning, or writes
would exceed the first proof.

## Concept Layer Map

```text
Agent knowledge support
  -> read-only knowledge consultation
     -> ConsultationBoundary
        -> request
        -> evidence response
        -> status algebra
        -> answering-agent rules
```

## Closure And Recomposition Proof

The unit closes because it has named input, output, caller, data source, policy,
limits, and failure behavior. It recomposes upward as:

```text
User question
  -> answering agent
  -> ConsultationBoundary
  -> neutral projection and source handles
  -> ConsultationResponse
  -> answer, clarification, or abstention
```

Future native-tool and HTTP adapters call the same boundary. A future search
index supplies records through `ProjectionReader`; it does not change the
request or response meaning.

## Technique Pack Trace

- Abstraction-level guard: separated knowledge support from one consultation
  service contract.
- Recomposition proof: passed as shown above.
- Evolution profile: multiple adapters, more query kinds, and larger projections
  are expected; preserve ports and versioned schemas only.
- Cognitive-load check: one operation and explicit statuses are simpler for the
  agent than a general graph language.
- Boundary-object check: the response envelope is the shared object between the
  retrieval owner and answering-agent owner.
- Concept-versus-knowledge check: selected unit is a design recommendation, not
  observed implementation.
- Cycle guard: stopped after the second round because further reduction removed
  required answer-safety behavior.
- Tournament: skipped; the route menu already rejected write and combined-answer
  designs on owner-boundary grounds.

## Deferred Complexity

- Graph database or vector database.
- Multi-hop or free-form graph query.
- Answer generation in the service.
- Reasoning-engine invocation.
- Knowledge writes and feedback intake.
- Durable distributed cache and cross-tenant deployment.
- Audit and receipt storage beyond request correlation needed for debugging.

## Tension Ledger

- Resolved: usefulness versus safety through bounded evidence plus explicit
  answer behavior.
- Resolved: one interface versus multiple operations through one `consult`
  boundary with typed query kinds.
- Deferred: projection owner.
- Deferred: access-policy owner and production identity mechanism.
- Deferred: measured limits and quality thresholds.

## Premortem

Likely failure: callers treat a relevant candidate record as trusted truth.
Guardrail: separate retrieval score, evidence confidence, commitment status,
freshness, authority effect, and claim ceiling; test that the agent abstains or
qualifies when any required field prevents a direct answer.

## Frame-expiry Note

Revisit this optimization point if the API must support trusted writes,
protected effects, multiple independently deployed data owners, or a production
external protocol. Those changes add owners and failure domains not present in
the current read-only frame.

## Navigation Guide

Start Design with `ConsultationBoundary`. Preserve the four inseparable
contracts. Treat adapters and storage as replaceable ports. Keep unresolved
owner and measurement decisions in the gap ledger.

## Native Stage Receipt

- Stage: `s5`.
- Owning capability: `distill`.
- Capability handle: `.agents/skills/distill/SKILL.md`.
- Receipt kind: native stage.
- Artifact: `stages/05-distill.md`.
- Status: `complete`.
- Verdict: `pass`.
- Evidence emission: not configured; source and role trace are retained here.
- Telemetry: not configured.
- Next route: `invoke design`.

