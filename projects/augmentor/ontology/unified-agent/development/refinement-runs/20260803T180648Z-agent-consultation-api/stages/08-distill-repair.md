# Stage 8: Distill Repair

## Repair Verdict

- Mode: `validate` with a repair-focused request.
- Input: `stages/06-design.md` plus `stages/07-design-review.md`.
- Findings considered: H1-H10.
- Findings repaired in this handoff: 10 of 10.
- Verdict: `pass` for non-executed planning.
- Claim ceiling: repaired design contract only; no implementation or owner
  approval follows.

The original Design remains an owner-authored stage artifact. This repair does
not silently edit it. Invoke Plan must consume this artifact as a required
amendment.

## Repaired Boundary

```text
model-visible ConsultationQuery
  + host-injected VerifiedPrincipal
  + host-injected PolicySnapshotRef
  -> ConsultationBoundary
  -> status-tagged mechanical evidence result
  -> AnsweringAgentPolicy
  -> answer | qualify | clarify | abstain
```

The API reports what it found, what it could not inspect, what mechanical limits
were hit, and which structured evidence states exist. It does not decide whether
the evidence is sufficient for a user-facing answer.

## H1: Identity Is Out Of Band

The model-visible query no longer contains caller identity, tenant, bearer token,
or policy digest.

```ts
interface ConsultationQuery {
  schemaVersion: "augmentor.consultation.query@0.1.0";
  requestId: string;
  questionId: string;
  operation: "lookup" | "search" | "context";
  query: ClosedQuery;
  scope: RequestedProjectionScope;
  limits: RequestedLimits;
}

interface VerifiedExecutionContext {
  principal: {
    opaquePrincipalRef: string;
    audience: "augmentor-consultation";
    workspaceId: string;
    expiresAt: string;
    issuer: string;
    signatureDigest: string;
  };
  policy: {
    ref: string;
    digest: string;
    accessEquivalenceClass: string;
  };
  deadlineAt: string;
  cancellationRef: string;
}

consult(query: ConsultationQuery, context: VerifiedExecutionContext)
```

Only the host adapter can construct `VerifiedExecutionContext`. The model cannot
see, supply, or replace credentials.

## H2: Status-tagged Response Variants

The response is a closed union. A denial has a fixed minimal shape:

```ts
type ConsultationResult =
  | EvidenceSuccess
  | EvidencePartial
  | NoMatch
  | InsufficientEvidence
  | StructuredConflict
  | StaleEvidence
  | AccessDenied
  | InvalidQuery
  | BudgetExceeded
  | TemporaryFailure;

interface AccessDenied {
  schemaVersion: string;
  requestId: string;
  questionId: string;
  status: "denied";
  reasonCode: "ACCESS_NOT_AVAILABLE";
  retryable: false;
}
```

`AccessDenied` contains no projection, policy, candidate count, record ID,
conflict, gap, source, selector, or protected query echo.

Aggregate status precedence is mechanical and deterministic:

1. `denied` when verified context or policy access is unavailable;
2. `invalid_request` after identity succeeds but the closed query is invalid;
3. `temporary_failure` when a required dependency fails;
4. `stale` when policy-required projection or source freshness fails;
5. `conflict` only for stored conflict relations or deterministic structured
   predicate collisions;
6. `budget_exceeded` when a hard cap prevents a complete result;
7. `insufficient_evidence` when required source bindings are absent;
8. `no_match` when the complete allowed search returns no record;
9. `partial` when the response is mechanically truncated but usable records
   are present;
10. `ok` when the complete bounded query succeeds.

This precedence never decides whether the answering agent should make a claim.

## H3: Atomic Claims And Compiler-bound Freshness

Evidence is returned as atomic statements rather than one summary with a shared
source list:

```ts
interface EvidenceStatement {
  statementId: string;
  subjectId: string;
  predicate: string;
  object: JsonScalar | string[];
  displayText?: string;
  transformation: {
    kind: "copied-field" | "stored-explanation" | "deterministic-comparison";
    version: string;
    inputFieldRefs: string[];
  };
  sourceHandles: EvidenceSourceHandle[];
  freshness: "current" | "stale" | "unknown";
  claimCeiling: string;
  forbiddenInferences: string[];
}
```

Freshness comes from a compiler-produced `ProjectionManifest` with every input
source digest, compiler version, field allowlist digest, and output digest.
Caller-provided digests are hints only and never establish freshness. Authorized
success variants include safe provenance for records used, excluded, or used in
ranking when policy permits disclosure.

## H4: Reproducible Relevance And Confidence

```ts
interface RetrievalMetric {
  algorithmId: string;
  algorithmVersion: string;
  scale: "normalized-0-1";
  value: number;
  normalizedQueryDigest: string;
  projectionDigest: string;
  candidateScopeDigest: string;
}

interface ConfidenceAssessment {
  level: "low" | "medium" | "high";
  ownerRef: string;
  basis: string;
  assessedAt: string;
  sourceHandle: string;
}
```

The service copies a confidence assessment supplied by its named owner. It never
derives confidence from retrieval rank, agreement count, or agent wording.

## H5: Mechanical Evidence State Only

- `partial` means a declared item, byte, token, source, scan, or time cap caused
  deterministic truncation.
- `conflict` means a stored conflict relation exists or two current structured
  statements bind the same subject and predicate to incompatible scalar values
  under the same scope.
- The service does not classify prose disagreement.
- `answerGuidance` is removed from the API response.
- The answering-agent owner maps statuses and evidence fields to answer,
  qualification, clarification, or abstention.

## H6: MVP Operations And Tagged Results

The MVP retains `lookup`, `search`, and `context`:

```ts
type OperationResult =
  | { kind: "records"; records: NeutralRecord[] }
  | { kind: "statements"; statements: EvidenceStatement[] }
  | { kind: "context"; records: NeutralRecord[]; statements: EvidenceStatement[] };
```

`traverse`, `compare`, and `explain` move to L1. They may return only typed
`edges`, `field-deltas`, or `stored-explanations` variants. They cannot be
implemented as free-form generated prose.

## H7: Limits Before Reads

For every dimension:

```text
effective cap = min(service hard cap, policy cap, request cap)
```

Caps are calculated before any projection read. They include candidate scan,
records, relations, sources joined, UTF-8 serialized bytes, token estimate,
elapsed time, and traversal depth. The token result names estimator ID and
version. Deadline and cancellation propagate into every reader call. No result
may be hydrated after a cap or cancellation is reached.

## H8: Cache Authorized Evidence Payloads Only

The cache key binds:

```text
schema version
+ operation
+ complete normalized query/selectors
+ projection digest
+ policy digest
+ effective field-mask digest
+ access-equivalence class
+ effective limits
```

The cache stores only immutable authorized evidence payloads. Every call builds
a fresh envelope with its own request ID, question ID, time, and cache metadata.
Denials and temporary failures are not shared between principals.

## H9: Neutral Projection Contract

The projection is built outside the consultation request by a one-way compiler:

```text
validated private ontology inputs
  -> explicit field allowlist
  -> opaque stable ID mapping
  -> neutral records and atomic statements
  -> per-field provenance
  -> leakage validator
  -> ProjectionManifest and output digest
```

The manifest includes input source digests, compiler version, allowlist digest,
opaque-ID-map version, record counts by safe kind, output digest, and owner
approval reference. The compiler cannot write back to source owners. Leakage
fixtures reject repository paths, private authority terms or bindings, secret
patterns, undeclared fields, and missing provenance.

L0 may use a synthetic or target-local fixture projection to validate the
contract. A consumer projection of private bytes remains blocked until a named
owner approves the field allowlist and compiler output.

## H10: Retrieved Text Is Untrusted Data

- All returned text is encoded as data inside typed fields.
- Retrieved text never enters system, developer, tool, or instruction roles.
- The answering-agent policy states that instructions, links, commands, or tool
  requests inside evidence must not be followed.
- Length, encoding, and control-character rules are validated.
- The agent may quote or summarize allowed content as evidence but cannot treat
  embedded directions as behavior policy.

## Recomposition After Repair

The smallest coherent unit remains `ConsultationBoundary`, now with:

- model-visible query separated from host-verified execution context;
- status-tagged mechanical results;
- atomic statement provenance;
- compiler-bound freshness;
- early effective limits;
- cache isolation; and
- untrusted-evidence handling.

It still recomposes into the user flow without acquiring answer, reasoning,
memory, routing, authority, or execution ownership.

## Remaining Residue

- Production principal, policy, projection, and answer-policy owners are not
  selected.
- The neutral field allowlist is not approved.
- Caps, latency, and answer quality are unmeasured.
- Planned scenarios are not executed tests.
- Native-tool registration and consumer integration are absent.

## Native Stage Receipt

- Stage: `s8`.
- Owning capability: `distill`.
- Capability handle: `.agents/skills/distill/SKILL.md`.
- Mode: `validate` and repair.
- Artifacts: `stages/08-distill-repair.md` and
  `stages/08-question-scenarios.md`.
- Status: `complete`.
- Verdict: `pass` for plan handoff.
- Reviewer findings closed in design handoff: H1-H10.
- Implementation and production readiness: not granted.
- Observer status: not configured.
- Next route: Invoke Plan.

