# Stage 2: Define The Agent Consultation API

## Plain Definition

The Agent Consultation API is a read-only service that gives an answering agent
a small, source-linked set of information relevant to a user question. The API
does not write knowledge and does not decide what the final answer should say.

The answering agent must either:

- answer within the returned evidence and its stated limits;
- ask for a narrower question;
- describe a conflict or missing source; or
- abstain when the available information cannot support an answer.

## Purpose

The API exists to make Augmentor knowledge usable by agents without exposing
the private ontology package, treating retrieval as truth, or giving the API
control over memory, routing, execution, approval, or authority.

## Actors And Owners

| Actor or owner | Responsibility | Explicit limit |
| --- | --- | --- |
| User | Asks the question and receives the answer. | A question does not authorize protected work. |
| Answering agent | Forms a consultation request, reads evidence, and composes or withholds an answer. | It cannot raise the evidence claim ceiling. |
| Host agent adapter | Supplies caller identity, request identity, scope, limits, and policy reference. | It cannot bypass the access policy. |
| Consultation service | Selects and packages bounded evidence from an approved projection. | It is read-only and non-authoritative. |
| Access-policy owner | Defines which caller may see which record and field classes. | Unselected for production; missing policy fails closed. |
| Projection owner | Compiles a neutral runtime projection from owner-held sources. | Unselected; compilation is outside the query API. |
| Source providers | Own source bytes, correction, deletion, and trusted-write policy. | A successful read is not a write or admission. |
| Answer owner | Owns the user-facing response behavior in the host product. | The API cannot claim this role. |

## Service Boundary

```text
AnsweringAgent
  -> ConsultationToolAdapter
  -> ConsultationService
     -> AccessPolicyPort
     -> ProjectionReader
     -> EvidenceLimiter
  <- EvidenceResponse
  -> AnswerPolicy
  -> answer | clarification | abstention
```

The service reads a neutral, versioned projection. It never reads arbitrary
filesystem paths supplied by the caller and never exposes private owner
bindings that the projection policy has not admitted.

## Supported Operations

| Operation | Meaning | Required bound |
| --- | --- | --- |
| `lookup` | Return records for exact stable IDs. | ID count and allowed record kinds. |
| `search` | Find records relevant to a question or terms. | result count, text length, time, and projection version. |
| `traverse` | Follow allowed relation kinds from selected records. | depth 1 in MVP, node and edge limits. |
| `compare` | Return named differences and shared evidence for selected records. | small record count; no inferred winner. |
| `explain` | Return stored direct or technical explanations for a record or lane. | approved explanation fields only. |
| `context` | Compose a bounded evidence bundle for one answering-agent turn. | token, item, source, and time limits. |

No operation accepts an arbitrary query language, file path, shell command,
database expression, owner-service command, or executable tool request.

## Request Definition

Every request contains:

- `schema_version`;
- `request_id` and `question_id`;
- `caller` with host-issued agent, tenant/workspace, thread, and policy refs;
- one `operation`;
- a query with stable IDs, terms, allowed record kinds, or relation kinds;
- `scope` with an approved projection ID and version;
- `limits` for items, sources, traversal depth, response bytes, context tokens,
  and elapsed time;
- optional `known_source_digests` for freshness checks.

Unknown fields, missing identity, an unknown operation, negative limits, or a
scope outside the policy are invalid. The service does not guess corrections.

## Evidence Response Definition

Every response contains:

- request and projection identity;
- one outcome status;
- selected and excluded record IDs;
- evidence items with stable record ID, record kind, direct summary, source
  handles, safe selectors, source digest, source posture, source owner, evidence
  confidence, commitment status, freshness, record owner route, authority
  effect, claim ceiling, and forbidden inferences;
- conflicts and missing-evidence statements;
- limits requested and used;
- response-generation time and cache status;
- next allowed action for the answering agent.

Retrieval relevance is recorded separately from evidence confidence. A high
retrieval score means only that the item matched the query well.

## Outcome Status

`ok`, `partial`, `no_match`, `insufficient_evidence`, `conflict`, `stale`,
`denied`, `invalid_request`, `budget_exceeded`, and `temporary_failure` are
distinct. Only `ok` and qualified `partial` may support a direct answer.

## Answering-Agent Contract

The agent must:

1. Use only returned evidence for factual claims attributed to this API.
2. Preserve source posture, freshness, conflicts, and claim ceilings.
3. Never describe a candidate or retrieval score as approved truth.
4. Cite safe source handles or record IDs supplied by the response.
5. Ask for clarification when a narrower query can close the gap.
6. Abstain when access is denied, evidence is insufficient, a material conflict
   is unresolved, or freshness cannot be established.
7. Never convert a response into a memory write, route decision, approval,
   execution request, or authority decision.

## Non-goals

- Generating the final answer inside the consultation service.
- Accepting knowledge writes or corrections.
- Owning source bytes or durable memory.
- Selecting an authority owner or making an authority decision.
- Routing work, launching agents, or executing tools.
- Providing unrestricted graph or filesystem access.
- Proving production readiness, answer quality, or performance.

## Terminology

| Term | Direct meaning |
| --- | --- |
| Source handle | A safe reference to owner-held information. |
| Projection | A neutral, bounded copy of fields approved for runtime reading. |
| Evidence item | One returned record plus its sources and limits. |
| Claim ceiling | The strongest statement the evidence may support. |
| Retrieval score | How closely a record matched the request, not how true it is. |
| Freshness | Whether the returned record still matches its bound source digests. |
| Abstention | A deliberate decision not to make an unsupported answer. |

## Decisions And Open Gaps

- Selected: one application service with a native agent-tool adapter first.
- Deferred: an HTTP JSON adapter over the same application service.
- Rejected: a combined read/write knowledge API.
- Open owner decision: neutral projection compiler and store.
- Open owner decision: caller identity, tenant scope, and field disclosure.
- Open measurement gap: useful default limits and answer-quality thresholds.

These gaps do not prevent contract design. They prevent production
authorization and fixed operational claims.

## Invoke Result

- Mode: `define`.
- Spell: `invoke`.
- Canonical ID: `invoke`.
- Scope: library, authoring this target-local design artifact.
- Phase status: `flag`.
- Mode contract: `.agents/skills/invoke/define.md`.
- Outputs: this combined spec, glossary, and transport artifact.
- Template selection: compact target-local API definition; the full DomainSpec
  family would add unrelated package artifacts during a Refine run.
- Dispatch techniques: sequence, route menu, owner-boundary check, protected
  context, and residue ledger as validated in `REFINE-DISPATCH.json`.
- Distill validation: stage 5 owns the required scope sanity check.
- Decisions: evidence API plus answering-agent adapter; read-only; native tool
  adapter first.
- Unresolved gaps: projection owner, access-policy approval, measured budgets.
- Next route: `interrogation` in `refine-review` mode.
- Observer status: not configured; visible residue only.

