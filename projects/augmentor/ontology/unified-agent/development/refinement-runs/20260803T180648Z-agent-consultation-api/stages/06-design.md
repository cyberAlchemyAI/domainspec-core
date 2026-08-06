# Stage 6: Agent Consultation API Design

## Selected API Shape

Build one read-only application service named `ConsultationBoundary` and expose
it first as one native agent tool:

```text
consult_augmentor_knowledge(request) -> response
```

An optional HTTP JSON adapter may be added later. Both adapters must call the
same application service and use the same schemas. The service returns evidence
for an answering agent; it never generates the final answer.

This is a design artifact. No service, adapter, projection, or host integration
has been implemented by this run.

## Design Scope

Included:

- caller and access-policy input;
- logical query operations;
- neutral projection reader;
- source-linked evidence records;
- freshness, conflict, limit, and error behavior;
- answering-agent consumption rules;
- fixture-based acceptance contracts;
- native-tool-first adapter boundary.

Excluded:

- ontology or memory writes;
- authority, approval, routing, execution, and reasoning-engine calls;
- arbitrary filesystem or graph access;
- production authentication mechanism selection;
- deployment, release, and performance claims;
- user-interface changes;
- detailed audit storage.

## 1. Context View

```text
User
  -> host-owned Answering Agent
     -> host-owned Consultation Tool Adapter
        -> ConsultationBoundary
           -> AccessPolicyPort
           -> ProjectionReader
           -> EvidenceResolver
           -> ResponseLimiter
        <- ConsultationResponse
     -> AnswerPolicy
  <- answer | clarification | abstention
```

The runtime projection contains only neutral fields admitted for this consumer.
Private CyberAlchemy vocabulary and direct repository paths remain outside the
API response.

## 2. High-level Structure View

| Component | Responsibility | Owner boundary |
| --- | --- | --- |
| `ConsultationToolAdapter` | Convert the host tool call into a typed request and return the response. | Future ResonantOS/Augmentor host owner. |
| `ConsultationBoundary` | Coordinate one read-only consultation. | Future consultation-service owner. |
| `CallerVerifier` | Accept only host-issued caller context. | Host identity owner; mechanism unselected. |
| `AccessPolicyPort` | Return allowed scope, fields, record kinds, relation kinds, and limits. | Future access-policy owner. |
| `ProjectionReader` | Read one pinned neutral projection by logical IDs and bounded search. | Future projection owner. |
| `EvidenceResolver` | Join records to safe source handles and calculate freshness/conflict state. | Consultation-service owner using provider metadata. |
| `ResponseLimiter` | Enforce count, traversal, byte, token, and time limits. | Consultation-service owner. |
| `AnswerPolicy` | Tell the answering agent when to answer, qualify, clarify, or abstain. | Answering-agent owner. |
| `ProjectionCompiler` | Produce a neutral projection from admitted owner-held inputs. | Separate future owner; never called by the consultation request. |

## 3. Low-level Component View

### Request and response contract

```ts
type QueryKind =
  | "lookup"
  | "search"
  | "traverse"
  | "compare"
  | "explain"
  | "context";

type ConsultationStatus =
  | "ok"
  | "partial"
  | "no_match"
  | "insufficient_evidence"
  | "conflict"
  | "stale"
  | "denied"
  | "invalid_request"
  | "budget_exceeded"
  | "temporary_failure";

interface CallerContext {
  agentId: string;
  workspaceId: string;
  threadId: string;
  policyRef: string;
  policyDigest: string;
  issuedBy: string;
}

interface ConsultationLimits {
  maxItems: number;
  maxSources: number;
  maxTraversalDepth: 0 | 1;
  maxResponseBytes: number;
  maxContextTokens: number;
  maxElapsedMs: number;
}

interface ConsultationRequest {
  schemaVersion: "augmentor.consultation.request@0.1.0";
  requestId: string;
  questionId: string;
  caller: CallerContext;
  operation: QueryKind;
  query: {
    text?: string;
    recordIds?: string[];
    recordKinds?: string[];
    relationKinds?: string[];
  };
  scope: {
    projectionId: string;
    projectionVersion: string;
    requiredSourceDigests?: Record<string, string>;
  };
  limits: ConsultationLimits;
}

interface EvidenceSourceHandle {
  sourceId: string;
  ownerRef: string;
  selector?: string;
  digest: string;
  posture: string;
  freshness: "current" | "stale" | "unknown";
}

interface EvidenceItem {
  recordId: string;
  recordKind: string;
  title: string;
  directSummary: string;
  technicalDefinition?: string;
  retrievalRelevance?: number;
  evidenceConfidence: "low" | "medium" | "high";
  commitmentStatus: string;
  ownerRoute: string;
  authorityEffect: "none";
  claimCeiling: string;
  forbiddenInferences: string[];
  sourceHandles: EvidenceSourceHandle[];
}

interface ConsultationResponse {
  schemaVersion: "augmentor.consultation.response@0.1.0";
  requestId: string;
  questionId: string;
  status: ConsultationStatus;
  projection: {
    id: string;
    version: string;
    digest: string;
  };
  policy: { ref: string; digest: string };
  items: EvidenceItem[];
  selectedIds: string[];
  excluded: Array<{ reason: string; safeCount?: number }>;
  conflicts: Array<{ subjectId: string; sourceHandles: string[]; summary: string }>;
  gaps: string[];
  budget: { requested: ConsultationLimits; used: Record<string, number>; hit: string[] };
  answerGuidance: "answer" | "qualify" | "clarify" | "abstain";
  generatedAt: string;
  cache: "miss" | "safe-hit" | "not-cacheable";
}
```

The response schema intentionally has no `truth`, `approved`, `decision`,
`execute`, `write`, or `recommendedAction` field.

### Operation contracts

| Operation | Resolver behavior | Not allowed |
| --- | --- | --- |
| `lookup` | Resolve exact logical IDs after policy filtering. | Paths, globbing, or guessed IDs. |
| `search` | Normalize bounded text, retrieve candidates, rank, and apply stable ID tie-breaking. | Treating rank as evidence confidence. |
| `traverse` | Follow an allowlisted relation kind for zero or one hop. | Recursive or caller-defined graph code. |
| `compare` | Return deterministic shared/different stored fields and their sources. | Declaring a winner or preferred decision. |
| `explain` | Return stored direct or technical explanation fields. | Generating a new conclusion inside the service. |
| `context` | Run bounded search/lookup/traversal and return one compact evidence set. | Generating the user answer. |

## 4. Workflow Process View

The service processes a request in this order:

1. Validate the closed request schema and hard maximums.
2. Verify the host-issued caller context.
3. Load the exact access-policy snapshot and verify its digest.
4. Resolve the named projection and verify its version and digest.
5. Normalize the query without accepting paths or executable expressions.
6. Retrieve candidates using logical IDs, bounded text search, or allowlisted
   one-hop relations.
7. Apply record and field policy before loading protected text.
8. Rank allowed candidates with a stable ID tie-breaker.
9. Join safe source handles and compare current source digests.
10. Detect conflicts between returned owner-held claims without resolving them.
11. Apply item, source, byte, token, and elapsed-time limits.
12. Select one response status and answer guidance using the decision table.
13. Return the response. Do not perform any write or downstream action.

### Retrieval order

```text
exact ID match
  -> allowed record-kind match
  -> normalized term match
  -> stored relevance score when present
  -> stable record ID tie-break
```

The MVP does not need a graph database or model-generated query planner. A
deterministic fixture projection can implement this order first. A later index
may supply candidates if it preserves the same result fields and limits.

## 5. Decision Flow View

| Condition | Status | Agent guidance |
| --- | --- | --- |
| Caller or policy cannot be verified. | `denied` | Abstain; do not reveal protected IDs or counts. |
| Schema, operation, scope, or limits are invalid. | `invalid_request` | Correct the request; make no factual claim. |
| No allowed record matches. | `no_match` | Clarify or say no matching source was found in this scope. |
| Records match but required source support is missing. | `insufficient_evidence` | Abstain or ask for a better source. |
| Owner-held records materially disagree. | `conflict` | Present the conflict with safe source handles; do not choose a winner. |
| A required digest drifted or freshness is unknown where current evidence is required. | `stale` | Abstain or explicitly qualify as stale if policy allows. |
| A limit stopped completion but the returned subset can support a bounded answer. | `partial` | Qualify and state exactly what was excluded or limited. |
| A limit stopped completion and the subset cannot support an answer. | `budget_exceeded` | Narrow the query or increase an owner-approved limit. |
| A dependency failed temporarily. | `temporary_failure` | Retry according to host policy; do not claim absence. |
| All required evidence is current and within scope. | `ok` | Answer within the claim ceiling and cite returned handles. |

The service computes this result. It does not decide the wording of the final
answer.

## 6. Dependency Interface View

| Dependency | Input | Output | Failure boundary |
| --- | --- | --- | --- |
| Caller verifier | host-issued caller context | verified identity or denial | denial reveals no protected record details |
| Access policy | verified identity, operation, projection metadata | field and record mask plus limits | missing or stale policy denies |
| Projection reader | pinned projection ID/version/digest, normalized query | neutral records and safe source bindings | unknown or drifted projection fails closed |
| Source metadata | safe source handle and expected digest | freshness state | timeout is `temporary_failure` or `stale`, never `no_match` |
| Context budget | response fields and host budget | used counts and cut points | limits produce `partial` or `budget_exceeded` |
| Native tool adapter | closed JSON request/response | host tool result | adapter cannot broaden policy or schema |

## Access And Privacy Contract

- The host supplies caller identity; the request body cannot self-assert access.
- Policy evaluation occurs before protected payload hydration.
- The policy result carries its own digest and is bound into the response.
- Field masks apply independently to summaries, technical definitions, source
  selectors, owner routes, and explanation text.
- A denial does not echo protected query terms, record IDs, result counts, or
  source metadata.
- Tenant or workspace scope is mandatory even for local use.
- The native adapter must not accept raw bearer tokens from the model. The host
  resolves credentials outside the model-visible request.
- Detailed request/response persistence is not part of the MVP. Correlation may
  record request ID, outcome, projection digest, and timing without record text.

## Freshness And Cache Contract

A response is fresh only relative to:

- projection ID, version, and digest;
- access-policy ref and digest;
- every returned required source digest; and
- the response time.

Safe cache key:

```text
hash(caller-scope + policy-digest + projection-digest + normalized-query + limits)
```

Rules:

- never share a cache entry across caller scopes or policy digests;
- do not cache denied responses across identities;
- invalidate on projection or required source digest change;
- preserve the original freshness and source fields on a safe hit;
- use no cache when the policy cannot prove safe reuse;
- do not claim a validated TTL until measurements and owners exist.

## Answering-Agent Policy

The agent receives the response as bounded context, not as hidden system truth.
It must:

1. Check `status` and `answerGuidance` before reading item text.
2. Cite source handles or record IDs for material claims.
3. Say when the evidence is candidate, partial, stale, or disputed.
4. Keep retrieval relevance separate from evidence confidence.
5. Avoid a direct factual answer for `denied`, `invalid_request`,
   `insufficient_evidence`, `conflict`, `stale`, `budget_exceeded`, or
   `temporary_failure`, unless the response explicitly allows a qualified
   partial answer.
6. Never infer that absent access means absent data.
7. Never call a write, route, execution, approval, authority, or reasoning tool
   as a side effect of consultation.

## Security And Failure Review

| Risk | Control |
| --- | --- |
| Prompt asks for a private path. | Closed schema plus logical-ID-only resolver. |
| Caller forges tenant or policy. | Host-issued caller context verified before query handling. |
| Denial reveals protected existence. | Policy-safe denial without identifiers, snippets, or counts. |
| Cache crosses scopes. | Policy and caller-scope binding in cache key. |
| Search score appears authoritative. | Separate `retrievalRelevance` and `evidenceConfidence`. |
| Stale projection supports an answer. | Projection and source digest checks; explicit `stale` result. |
| Conflict is silently resolved. | Return conflict records and force qualify or abstain. |
| Tool call triggers a write. | No writer port, command field, arbitrary URL, or effect field in the application service. |
| Private vocabulary leaks. | Neutral projection and field masks; no direct ontology-file access. |
| Oversized request exhausts context. | Validate hard maximums and return `budget_exceeded` or a qualified `partial`. |

## Versioning And Compatibility

- Request and response schema versions are explicit.
- A new optional field requires a minor version and closed consumer tolerance.
- A changed meaning, status, required field, or policy rule requires a new major
  contract version.
- The native tool name may remain stable only while its schema version routing
  is explicit.
- An HTTP adapter may be introduced only as a transport wrapper; it cannot
  change statuses, policy, limits, or evidence semantics.

## Planned Validation Contracts

The first deterministic fixture suite must cover:

- supported current evidence;
- partial results with exact limit reasons;
- no match;
- insufficient source support;
- conflicting owner-held records;
- stale source digest;
- unauthorized caller without information leakage;
- invalid path-like selector;
- budget exhaustion;
- temporary provider failure;
- relevance score distinct from evidence confidence; and
- answering-agent abstention or qualification for every non-direct-answer state.

These are planned witnesses. They are not executed evidence.

## Design Decisions

| Decision | Selected | Deferred or rejected |
| --- | --- | --- |
| Primary interface | Native agent tool over one application service. | HTTP adapter deferred. |
| Data access | Neutral versioned projection. | Direct private-file access rejected. |
| Query language | Closed query kinds and logical selectors. | GraphQL, arbitrary graph, and filesystem query rejected for MVP. |
| Answer production | Separate answering-agent policy. | Answer generation inside the service rejected. |
| Writes | None. | Memory, ontology, correction, feedback, routing, and execution writes rejected. |
| Search | Deterministic bounded search first. | Vector or graph database deferred until measured need. |
| Cache | Optional safe cache behind exact policy and projection bindings. | Fixed TTL and distributed cache deferred. |

## Open Residue

- The production projection owner is unselected.
- The production access-policy and caller-identity owners are unselected.
- The neutral projection field list needs owner approval before implementation.
- Default latency, token, byte, and result budgets need fixture measurements.
- The concrete native tool registration point in ResonantOS is not selected.
- No current end-to-end request-to-answer witness exists.

None of these gaps changes the read-only contract. All block production or
integration claims until resolved.

## Invoke Result

- Mode: `design`.
- Spell: `invoke`.
- Canonical ID: `invoke`.
- Scope: library, authoring a target-local architecture bundle.
- Phase status: `pass` for the design artifact; production readiness remains
  outside the evidence ceiling.
- Mode contract: `.agents/skills/invoke/design.md`.
- Outputs: `stages/06-design.md`, `design-selection/scope-manifest.json`,
  `design-selection/denominator-receipt.json`, and
  `design-selection/selection-result.json`.
- Design views: all six present.
- Design evidence state: `design-validator-pass` after deterministic selection
  validation.
- Evidence ceiling: design selection and contract completeness only; planned
  fixtures are not Plan evidence.
- Plan evidence: `plan-evidence-pending`.
- Template/profile selection: compact DomainSpec six-view architecture profile;
  no UX companion because the API does not change a rendered semantic surface.
- Dispatch techniques: x-ray, owner-boundary check, protected context,
  state-namespace boundary, and memory-promotion split.
- Distill validation: stage 5 pass for coherent unit; stage 8 owns repaired
  scenario validation.
- Implementation layering: deferred to Invoke Plan.
- Work-pack: not created by Design.
- Next route: independent `refine-design-review`.
- Observer status: not configured.

