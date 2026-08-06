# Akashic frontend and ontology foundation — findings

## Recommendation and claim ceiling

Build the smallest direction as a **read-only Reviewed Principle Explorer with a bounded Q1–Q6 question panel**. It should make the seven reviewed principles readable first, expose source-bound evidence on demand, and preserve the exact typed query and diagnostic contracts behind a narrow same-machine adapter. Do not begin with a graph canvas.

This is a candidate architecture, not implementation evidence. No browser application, HTTP adapter, browser-security review, user study, usability result, accessibility-conformance result, approved public graph schema, publication, deployment, live transport, or agent-execution capability was found. The reviewed feed, generated Inventory, and query RecordSet are distinct sources and must not be collapsed or called live/fresh without a future freshness contract.

Evidence: Halford explorer, `research.md#agent-1--halford-graeme`, especially `### Smallest primary journey`, `### Progressive disclosure model`, and `### Boundaries and deferred scope`; Shannon explorer, `research.md#agent-2--shannon-claude`, `## Contract-trace conclusion` and `## Executed Akashic contracts`; exact selectors `example-feed.json#/entries`, `example-feed.json#/consumer_contract`, `graph-queries.mjs#SUPPORTED_OPERATIONS|executeGraphQuery`, and `cli.mjs#evaluateGraphQuery`.

## Five-column verdict matrix

| Candidate | Smallest useful witness | Precedent status | Cost and risk | Verdict |
|---|---|---|---|---|
| Reviewed Principle Explorer + bounded question panel | Browse seven entries, open `At`, inspect its two evidence handles, run Q4/Q5, preserve digests and distinct outcomes | `build-from-owned` | Low–medium; narrow adapter and faithful diagnostics are the hard parts | **Recommend first** |
| Static reader + server-rendered query pages | Same seven entries and six closed forms, with static-build identity separate from query-time binding | `build-from-owned` | Lowest client complexity; weaker continuity and more template state | Viable fallback |
| Graph-first canvas + inspector | `At` plus typed projections and Q1–Q6 overlays with a mandatory semantic table equivalent | `searched precedent-clean` (workspace-scoped only) | High; layout, keyboard equivalence, synchronization, and semantic overclaim risk | Viable future visualization; defer |

No candidate is killed by non-vacuity: Russell’s hand witness passes all three (`reviews.md#russell-bertrand--non-vacuity-gate`). Candidate 3 is deferred because no capability or latency witness justifies its complexity and semantic risk, not because precedent kills it. External precedent search was not run, so “searched precedent-clean” is not a novelty claim (`reviews.md#rittel-horst--precedent-gate`).

## Primary journey and screen/component map

1. **Browse reviewed principles:** render exactly `At, Co, Cr, Ft, Gr, Is, Mo`, one-to-one with `example-feed.json#/entries`, with symbol, plain title, group, description, and a compact binding/ceiling strip.
2. **Open principle detail:** for `At`, show `entry:claim:at`, proposition, authored origin, claim ceiling, evidence count, “Show evidence,” and “Ask a question.”
3. **Inspect evidence:** use a drawer on wide screens and a non-modal page on narrow screens. Show supported field/relation, source ID, selector, scope, and digest; never summarize this as “verified.”
4. **Ask one closed question:** expose six named forms, no free-form query language. Isolate Q6 behind explicit base and target snapshot selection.
5. **Read a derived result:** display operation, authored-input digest or snapshot IDs, operation-specific results, result digest, and one distinct success/empty/indeterminate/prerequisite/error state.
6. **Inspect projection details:** show reviewed-feed binding separately from `generated/current.json#/`; never substitute the fixture-shaped generated Inventory for the seven-principle feed.

Components: `BindingCeilingStrip`, `PrincipleList`, `PrincipleDetail`, `EvidenceDisclosure`, `QuestionPanel`, `SnapshotComparisonForm`, `ResultRegion`, `DiagnosticRegion`, and `ProjectionDetails`. Stable Akashic-owned selectors may follow `data-od-id="akashic:<component>:<identity>"`; this adapts UI Prototyping Studio workspace precedent and proves only deterministic correspondence, with its shimmed-e2e caveat—not usability or deployment (Ashby, `research.md#agent-3--ashby-w-ross`, `### Browser-state and test contract`; UI Studio findings `#What Is Working Now|Where the UX/UI Breaks Trust`).

## Exact browser/runtime adapter contract

Use dependency-light semantic HTML/CSS/ES modules and a narrow Node HTTP adapter around existing Akashic modules. The server owns the repository root and approved artifact paths; browser input can never select a filesystem path or CLI action.

Allowed requests only:

- `GET feed`: load and schema-validate the reviewed feed.
- `GET projection-status`: read the generated pointer and manifest as a separate status surface.
- `POST query`: accept exactly one closed `graph_query_request` variant from `query-contracts.schema.json#$defs/graph_query_request`; allowlist only `graph-queries.mjs#SUPPORTED_OPERATIONS`.
- Q1–Q5 require `expected_authored_input_digest`. Q3 requires exactly two distinct closed domain IDs. Q6 requires explicit `base_snapshot_id`, `target_snapshot_id`, impact index, and server-loaded snapshots.

Response union:

```text
{ kind: "feed", feed, adapter_feed_digest? }
{ kind: "projection_status", current, manifest, status }
{ kind: "query_result", result: {
    operation,
    authored_input_digest | (base_snapshot_id, target_snapshot_id),
    results,
    result_digest
  } }
{ kind: "error", status, diagnostics: [{ code, selector, message }] }
```

An adapter-computed feed digest must be labelled adapter-local. Preserve query result fields and structured diagnostics from `graph-queries.mjs#GraphQueryError|assertAuthoredState|executeGraphQuery` and `query-contracts.schema.json#$defs/graph_query_result`. A new failure invalidates or marks stale the prior-success presentation; it is not an appended banner. Distinguish `source_state_mismatch`, `invalid_input`, `unsupported_expression`, empty result, Q5 indeterminate, and missing-Q6 prerequisites.

Forbidden adapter capabilities: CLI passthrough, user-controlled filesystem access, build/generation, Git import, mutation, authoring, candidate acceptance, review persistence, agent dispatch, authority change, promotion, publication, or deployment. Evidence: Shannon, `research.md#agent-2--shannon-claude`, `## Browser adapter contract`; exact selectors `cli.mjs#evaluateCli|evaluateGraphQuery|parseGitImportArguments` and `graph-queries.mjs#executeGraphQuery`.

## Seven-principle and Q1–Q6 witness

| Query | Concrete screen witness | Required binding and semantics |
|---|---|---|
| Q1 `PrinciplesInGroup` | choose a displayed group; return ordered principles | expected authored-input digest |
| Q2 `PapersIllustratingPrinciple` | from `At`, show related reviewed papers | authored typed relations; empty means no reviewed result in this snapshot |
| Q3 `PrinciplesAcrossDomains` | choose exactly two distinct closed domain IDs | authored Paper→Domain traversal |
| Q4 `EvidenceForPrinciple` | “Show evidence” for `At` | field-scoped evidence plus illustration evidence |
| Q5 `PrincipleCoOccurrenceAndTensionStatus` | show shared-paper witnesses | `tensions: []` and `tension_status: indeterminate`; never “no tension” |
| Q6 `CompareImportSnapshots` | separate base/target form | two explicit snapshot IDs, impact index, server-loaded snapshots, result digest |

The exact feed witness is `example-feed.json#/entries`; closed request/result unions are `query-contracts.schema.json#$defs/graph_query_request|graph_query_result`; binding and Q5 semantics are `graph-queries.mjs#assertAuthoredState|principleCoOccurrenceAndTensionStatus|executeGraphQuery`. Reviewer confirmation: `reviews.md#russell-bertrand--non-vacuity-gate`.

## Candidate public-safe Akashic graph profile

These names and constraints are proposed Akashic-owned vocabulary; they are not an approved or executed graph schema.

| Node kind | Candidate identity | Source/ceiling rule |
|---|---|---|
| `Principle` | `authored_record_id`; `entry_id` only as presentation identity | retain authored origin and feed-entry claim ceiling |
| `Group` | `group_id` | reviewed-feed grouping source |
| `Paper` / `Source` | authored source ID | authored source reference |
| `Domain` | closed domain ID | authored classification source |
| `EvidenceHandle` | preferably a nested value; if promoted to a node, candidate composite of evidence digest + source + selector + relation + scope | current fields do **not** execute a graph-node identity schema |
| `ImportSnapshot` | `snapshot_id` | snapshot source and comparison binding |

Default-deny every declarable edge not listed here:

| Source | Edge | Target | Direction/cardinality | Status and evidence rule |
|---|---|---|---|---|
| `Principle` | `grouped_in` | `Group` | directed; exactly one **only in the reviewed-feed projection** | feed-grounded candidate projection |
| `Principle` | `illustrated_by` | `Paper` | directed; 0..N | authored relation only |
| `Paper` | `classified_in_domain` | `Domain` | directed; 0..N | authored relation only |
| `Principle` | `principle_evidenced_by` | `EvidenceHandle` | directed; contract-required cardinality only | field-scoped principle evidence |
| `Paper` / authored illustration record | `relation_evidenced_by` | `EvidenceHandle` | directed; contract-required cardinality only | relation-scoped evidence; separate from principle evidence |

`co_occurs_with` is not declarable or persisted: it is a symmetric derived read view between `Principle` values, witnessed by shared paper IDs. Snapshot comparison is likewise a derived result, not an edge. `tensions_with` is prohibited because current execution only supports an indeterminate tension status. Reverse labels are UI views, not inverse edge declarations.

All current feed relations preserve `authority_effect:none`; this is already deployed in Akashic, not borrowed. Cycles are structurally unavailable under the current proposed authored endpoint-kind partition; that is candidate reasoning, not a validated Akashic cycle contract. Any kind or endpoint expansion reopens review.

## Precedent and ownership decisions

`precedent_status` is independent of the reuse/adapt/reject decision. Private ontology material supplied questions and review pressure only; it is not an Akashic runtime dependency, authority source, or public text source.

| Pattern | Precedent status | Decision | Akashic treatment |
|---|---|---|---|
| Stable node identity | `already-deployed` | adapt | authored/entry/group/domain/source/snapshot IDs; candidate composite or nested evidence handle |
| Source references | `already-deployed` | adapt | authored origins and evidence source/selector/relation/scope |
| Confidence | `searched precedent-clean` | reject | no executed Akashic confidence contract |
| Challenge/residue | `build-from-owned` | adapt | gaps, indeterminate states, and diagnostics; no imported protocol |
| Typed endpoints | `build-from-owned` | adapt | candidate signatures above; schema-owner approval still needed |
| Direction | `already-deployed` authored; `build-from-owned` reverse views | adapt | preserve authored direction; derived symmetry only for co-occurrence |
| Evidence references | `already-deployed` | reuse Akashic contract | current handles/digests/selectors/scopes; private precedent independently asks similar questions |
| `authority_effect:none` | `already-deployed` | reuse Akashic contract | preserve explicit none; never infer promotion |
| Cardinality | `build-from-owned` | adapt | exact-one grouping only in reviewed-feed projection; otherwise contract proof or 0..N |
| Default denial | `build-from-owned` | adapt | new Akashic candidate catalog; do not copy the private catalog |
| Inverses | `build-from-owned` | adapt | read labels only |
| Cycle policy | `build-from-owned` | adapt | candidate endpoint-partition reasoning; expansion blocks pending review |
| Projection separation | `already-deployed` | reuse Akashic contract | authored records, generated Inventory, reviewed feed, and browser view stay distinct |

Exact private precedent citations are retained only in this private findings file: `cyberAlchemy-v2/ontology/README.md#Ontology`; `NODE-MODEL.md#Purpose|Node Concept Contract`; `RELATION-MODEL.md#Relation Contract|Value-Cycle Guard|Endpoint Rule`; `canonical-kinds/ALLOWED-EDGES.yaml#/`. Rittel’s ownership findings and repairs are at `reviews.md#rittel-horst--precedent-gate`. External precedent search was not run.

## Tests and implementation slices

1. **Adapter contract fixture:** schema-validate feed; expose separate projection status; reject unknown operations, paths, and fields; prove exact result/error union and canonical digest preservation.
2. **Seven-entry semantic reader:** render exactly seven unique entries and `At` identity/ceiling; progressive disclosure; narrow-layout evidence page; no query execution yet.
3. **Evidence and Q1–Q5:** render scoped handles; test every closed request, ordered typed result, empty state, mismatch invalidation, unsupported/invalid diagnostics, and exact Q5 indeterminate wording.
4. **Q6 isolation:** require two explicit IDs, impact index, and server-loaded snapshots; test missing prerequisites and snapshot-bound result identity.
5. **Browser correspondence:** Playwright checks stable Akashic-owned selectors, keyboard disclosure/focus return, live result/error announcement, digest wrapping/copying, text-not-color status, narrow viewport, and semantic list/table equivalents. These are deterministic acceptance checks, not human usability or WCAG conformance claims.

Each slice remains read-only and must pass unit tests for request mapping/error normalization, integration tests against the seven-entry feed and Q1–Q6 fixtures, schema validation, scoped whitespace checks, and browser acceptance before the next slice. Security review, user research, accessibility audit, publication, and deployment are separate gates.

## Public-safe statements and explicit deferrals

Safe to restate publicly after a separate Akashic owner route, without private paths, identifiers, predicates, or copied prose:

- The proposed first UI is a read-only reviewed-principle explorer with six closed questions.
- It keeps reviewed content, generated projections, evidence, and derived results visibly distinct.
- It preserves source selectors, digests, explicit claim ceilings, and distinct empty/invalid/stale/indeterminate states.
- Its candidate graph profile uses Akashic-owned node names, typed endpoints, default denial, non-persisted paper-witnessed co-occurrence, and no inferred tension edge.
- The adapter exposes only allowlisted reads; it cannot mutate, approve, publish, grant authority, import Git state, or execute agents.

Deferred: graph canvas; free-form query language; authoring; candidate acceptance; review persistence; Git/live transport; agent execution; authority and promotion; freshness/live-update contract; consumer inventory; approved public graph schema; security, usability, accessibility-conformance, responsive, and human-trust evidence; publication; deployment; production readiness.

Private precedent may guide questions only. No private path, prose, identifier, predicate, schema, authority binding, or runtime dependency may enter a public Akashic artifact without a separate owner and promotion route.
