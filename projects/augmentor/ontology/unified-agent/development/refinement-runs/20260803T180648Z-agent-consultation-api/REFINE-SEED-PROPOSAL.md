# Refine Seed Proposal: Agent Consultation API

## Operator Intent

Refine an API that agents can consult to obtain data for answering user
questions through an agent.

## Inferred Target

Design a read-only consultation API over the private Augmentor unified-agent
ontology. The API returns bounded, source-linked evidence to an answering agent;
the answering agent remains responsible for composing the user-facing answer.

The target is this design package:

`projects/augmentor/ontology/unified-agent/`

The future consumer remains owned by:

`../workspace-resonant/2.0.0-alpha`

## Desired Outcome

Produce an MVP-ready, non-executed API design and implementation plan that
defines:

- who may call the API and how access is checked;
- the distinction between the consultation API and the answering agent;
- supported lookup, search, traversal, comparison, explanation, and context-pack
  operations;
- request selectors, limits, response records, errors, freshness, and caching;
- source links, candidate status, confidence, owner routes, claim ceilings, and
  unresolved gaps returned with evidence;
- how the answering agent cites, abstains, asks for clarification, and reports
  missing or conflicting information;
- protection against source mutation, trusted-memory writes, ontology promotion,
  execution, and authority decisions;
- a small falsification suite covering ordinary, ambiguous, unsupported,
  conflicting, stale, unauthorized, and oversized questions;
- an implementation sequence with exact future write scopes and validation
  commands.

## Selected Product Boundary

```text
User question
  -> Answering agent
  -> Read-only consultation API
  -> Private source-bound read model
  -> Evidence bundle with limits and provenance
  -> Answering agent response or abstention
  -> User
```

The API is not itself a source of truth, memory owner, reasoning authority,
answer authority, approval service, router, or execution engine.

## Source Context

- `README.md` defines the package as private, source-bound, candidate-local, and
  non-authoritative.
- `profile.json` fixes `authority_effect: none` and
  `release_admission: not-granted`.
- `sources.json` binds the ontology to owner-held sources across DomainSpec,
  CyberAlchemy v2, Arcanum, and ResonantOS.
- The existing ontology separates `SourceRecord`, `ContextSnapshot`, routing,
  memory intake, ontology candidates, authority decisions, reasoning requests,
  and judgment receipts.
- The current password-protected visualization is a presentation surface, not
  an API contract or runtime witness.

## Open Design Questions

1. What is the minimum query language an agent needs without exposing arbitrary
   graph or filesystem access?
2. Which records are safe to return verbatim, summarized, or only by handle?
3. Should the MVP expose HTTP, a native agent tool contract, or both through one
   shared application service?
4. How are question intent, result relevance, source freshness, and confidence
   represented without implying truth or approval?
5. How does the answering agent distinguish no match, insufficient evidence,
   conflicting evidence, access denial, and temporary failure?
6. Which owner may produce a neutral runtime projection from this private
   ontology package?

## Preset And Research Decision

- Preset: `standard`
- Research mode: `research-if-gap-appears`
- Initial research decision: local-first. External research remains blocked
  unless Interrogation or Distill names a concrete protocol, security, or agent
  tool-design gap and the operator confirms one bounded pass.

## Write Scope

Before confirmation, Refine may write only this run folder. After confirmation,
the approved stage owners may write only their declared artifacts under the same
run folder.

No API code, ontology records, visualization files, deployment files,
`workspace-resonant` files, canonical CyberAlchemy v2 sources, Arcanum sources,
Git state, or remote services may be changed by this Refine run.

## Done Criteria

- All ten Refine stages have an owner-native receipt or explicit blocked reason.
- The final design states the API/agent/source/authority boundaries precisely.
- The plan names a smallest testable implementation unit and a larger
  recomposition target.
- The toy scenario produces evidence for pass, abstain, conflict, denial, stale,
  and budget-exceeded outcomes.
- The final synthesis does not claim implementation, integration, release,
  deployment, or production readiness.

## Validation Surface

- Dispatch Spec schema and deterministic validator.
- Target-local manifest and evidence-index completeness.
- Source and ownership reconciliation against the current ontology package.
- Request/response and error-contract review.
- Threat and privacy boundary review.
- Controlled question-to-evidence-to-answer toy scenarios.
- Non-executed implementation-plan review.

## Subagent Strategy

- Preliminary P1 decision: do not create a governed multi-agent dispatch.
- Reason: the fixed Refine loop already owns definition, critique, repair, and
  planning. Turning three context lenses into a research dispatch would require
  the separate explorer-to-auditor research pipeline and duplicate the loop.
- Helper: one read-only `api-boundary-reviewer` governed by `interrogation` at
  stage 7.
- Angle: challenge usefulness, access, privacy, provenance, freshness, query
  budgets, abstention, and the API-to-answering-agent handoff.
- Output: `receipt:api-boundary-review` with status, evidence, blockers,
  residue, and handoff note.
- Join: the parent waits for the helper, verifies its receipt, and closes it
  before Distill Repair.
- Tension gate: not applicable because one helper is not a dispatch fan-out.
- Ledger: no registration before or after the helper; it is recorded in the
  parent run closeout.

## Planned Stage Configuration

1. Context Builder: one parent-owned strict evidence baseline.
2. Invoke Define: define the API, consumer, data, trust, and non-goals.
3. Interrogation `refine-review`: challenge the definition and unresolved owner
   choices.
4. Refine research decision: remain local-first unless a named gap appears.
5. Distill: select the smallest coherent consultation contract.
6. Invoke Design: design operations, records, flow, access, failure, and agent
   consumption.
7. Interrogation `refine-design-review`: pressure-test usefulness and boundaries
   with one independent read-only API-boundary reviewer.
8. Distill Repair: run controlled question scenarios and repair the design.
9. Invoke Plan: produce a non-executed implementation plan.
10. Interrogation `refine-final`, followed by Refine-owned synthesis.
