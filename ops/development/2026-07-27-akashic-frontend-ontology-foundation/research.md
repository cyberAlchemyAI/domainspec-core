# Akashic frontend and ontology foundation — explorer returns

The sections below preserve the three explorer returns verbatim. They are research evidence, not authority or implementation approval.

## Agent 1 — Halford, Graeme

## Halford, Graeme — task-journey explorer result

### Evidence status

Observations are from current Akashic runtime/feed artifacts. Older research and Phase-0 Design are contextual only: the Phase-0 Architecture explicitly says its runtime evidence is none and is unimplemented, so it cannot override the present feed, CLI, or query implementation.

### Smallest primary journey

A non-programmer who can work with agents should be able to answer:

> “What does this reviewed principle say, what supports it, and what other bounded questions can I ask of the same reviewed snapshot?”

1. **Browse the reviewed principles** in a simple list/cards view: symbol, plain-language title, group, one-sentence description.
2. **Open one principle** to see its exact reviewed wording, authored-origin digest/path, evidence handles, and a persistent “what this does not prove” ceiling.
3. **Ask a bounded question** from a small action menu:
   - principles in a group;
   - evidence for a principle;
   - papers illustrating a principle;
   - principles across selected domains;
   - co-occurrences and the explicitly indeterminate tension status;
   - snapshot comparison, only after the user supplies/selects two compatible snapshots.
4. **Read the result as a derived view**, with input/output/projection digests and a clear distinction between “no result,” “unknown/indeterminate,” and “cannot run because the supplied state is stale or invalid.”

This is a read-only **reviewed-content explorer plus evidence drawer and Q1–Q6 results panel**. It should not start as a graph canvas: current operations are direct scans over validated records, and prior research rejects persisted graph indexes without a latency/capability witness.

### Information architecture and screen sequence

| Screen/state | User-visible content | Why it is smallest |
|---|---|---|
| Home / browse | “Reviewed principles” list; group filter; current feed/profile identifiers; seven entries | The feed itself is a fixed seven-principle read-only witness. |
| Principle detail | Title/symbol, group, description, proposition, evidence count, “Show evidence,” “Ask a question” | Keeps plain reading primary; provenance is available but not forced into every card. |
| Evidence drawer | Each evidence handle: what field it supports, source ID, exact selector, digest, relation | Preserves source-bound evidence rather than a vague “verified” badge. |
| Question panel | Six named, constrained actions with short plain-language prompts; no free-form query language | Matches `SUPPORTED_OPERATIONS`; avoids implying semantic inference or arbitrary graph traversal. |
| Result panel | Ordered results, query name, digest binding, and status explanation | Makes a derived result inspectable without raw JSON as the default. |
| Snapshot comparison step | Explicitly separate Q6 flow requiring base/target snapshot inputs | Q6 has different required inputs and should not masquerade as a normal principle lookup. |

Recommended labels:

- “Reviewed principles,” not “truths,” “knowledge,” or “approved facts.”
- “Source evidence” and “Evidence location,” not “proof.”
- “Related through reviewed records,” not generic “connected.”
- “No accepted tension assertion,” with the exact current status “Tension status: indeterminate”; never “no tension.”
- “Current generated snapshot,” not merely “current” or “live.”
- “This view is read-only,” plus “It cannot add, approve, publish, or change content.”

### Progressive disclosure model

Level 1 is readable content: title, short description, group.  
Level 2 is trust context: reviewed-entry ceiling, authored origin, source/evidence counts.  
Level 3 is exact provenance: selectors, evidence digests, generated-from digests and manifest IDs.  
Level 4 is technical result detail: operation name, expected-authored-input digest, diagnostics, canonical output details.

That order lets an agent-capable but non-programming user begin with content while still reaching the exact evidence required to challenge or cite it. Do not hide the claim ceiling behind a generic info icon; keep a short ceiling visible in detail and result views.

### Empty, mismatch, and failure states

- **No matching principle/paper/domain result:** “No reviewed result in this snapshot.” Do not suggest absence from the world or corpus.
- **No evidence for an expected field:** Show the missing field/group explicitly; do not substitute a generic “verified” status.
- **`source_state_mismatch`:** “This question is tied to a different reviewed input snapshot. Refresh or select the matching snapshot.” Preserve the expected/supplied digest in technical details.
- **`unsupported_expression`:** “This question is not available in this explorer.” Do not offer an unrestricted query box.
- **Invalid input/invalid record set:** “The reviewed data could not be used for this question.” Show one stable diagnostic selector in details, without treating the UI as a repair or admission surface.
- **Q6 inputs missing:** “Comparison needs both a base and target snapshot.” This is a distinct prerequisite, not an empty result.
- **Projection freshness ambiguity:** The present `generated/current.json` identifies a generation and digests, but no live update/HTTP behavior was inspected or proved. Show “snapshot identifier and digest” rather than “up to date” unless a future adapter has a separate freshness contract.

### Responsive and accessibility risks

- Seven items fit a one-column narrow layout; preserve group/filter controls and question actions as stacked controls rather than shrinking a graph or table.
- Evidence selectors and SHA-256 strings can overflow: use wrapping, copy controls, and an accessible full-value disclosure.
- Do not rely on color for group, status, or error state; pair icons/colors with text.
- Evidence drawers/dialogs need focus trap, labelled close action, logical return focus, keyboard navigation, and a non-modal alternative on small screens.
- Give every result region an accessible name and announce completed/error query states with an appropriate live region.
- Empty and indeterminate states need text distinctions; an empty list alone would collapse “no results,” “not computed,” and “no accepted tension.”
- These are design risks, not usability or accessibility evidence: no user study, responsive test, or browser interaction result was inspected.

For implementation validation, borrow only the public-safe testing question of stable `data-od-id` hooks and deterministic Playwright assertions. The UI Studio finding supports these as testability practices, not as proof that this explorer is usable or production-ready.

### Boundaries and deferred scope

The current CLI is a local command surface for validation, read operations, projection operations, graph query, and Git import; it is not browser-safe by itself. A frontend therefore needs a future bounded, read-only adapter that permits only feed retrieval and the six explicit query request shapes. It must not expose build, publication, Git import, content mutation, review, authority, agent dispatch, or any generic filesystem/CLI access.

The feed itself forbids `accept_candidate`, `dispatch_agent`, `grant_authority`, `mutate_content`, `promote_relation`, `publish_projection`, and `self_review`; the user interface should expose no affordance that implies otherwise.

Unverified user assumptions: that intended users are non-programmers who work with agents; that a browser frontend is the desired delivery surface; that current data needs live freshness; and that the browser will be backed by an HTTP adapter. None is proved by the consulted artifacts.

### Exact evidence selectors consulted

- `ops/development/2026-07-27-akashic-frontend-ontology-foundation/dispatch-sheet.json` → `groups[group_id=explorers].agents[agent_name="Halford, Graeme"]`
- `ops/development/2026-07-27-akashic-frontend-ontology-foundation/strategy-inventory-packet.json` → `direct_source_fallbacks`, `unresolved_gaps`, `design_consequences`, `excluded_matches`
- `projects/akashic-records/agent-pool/reviewed-content/example-feed.json` → `/`, `consumer_contract`, `generated_from`, `entries[*].evidence_handles`, `entries[*].claim_ceiling`
- `projects/akashic-records/agent-pool/reviewed-content/feed-manifest.schema.json` → root required properties; `$defs.consumer_contract`; `$defs.feed_entry`
- `projects/akashic-records/src/graph-queries.mjs` → `SUPPORTED_OPERATIONS`; `executeGraphQuery`; `principleCoOccurrenceAndTensionStatus`
- `projects/akashic-records/src/cli.mjs` → `evaluateCli`; `evaluateGraphQuery`
- `projects/akashic-records/generated/current.json` → `/`
- `projects/akashic-records/research/2026-07-27-periodic-table-graph-schema/findings.md` → `## Current L0 boundary`; `## Public content and relation contract`; `## Six-query contract and worked fixture`; `## Generated projections, direct queries, and migration`; `## Public evidence boundary`; `## Five-column verdict matrix`
- `ops/development/2026-07-26-akashic-contract-architecture/findings.md` → `## Direct answer`; `## Current contract inventory`; `## Agent contribution contracts`; `## Authority non-collapse`; `## Proposed public-safe Design delta`; `## Unresolved owners and dissent`
- `projects/akashic-records/development/phase-0-content-contract/design/ARCHITECTURE.md` → lines 3–18, 48–63, 111–150, 175–199, 222–229, 285–332
- `projects/akashic-records/development/phase-0-content-contract/design/VALIDATION-CONTRACTS.md` → `VC-PROJECTION-*`, `VC-VERSION-*`, `VC-PHASE0-NO-*`, deferred graph/Olog clause
- `projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/findings.md` → stable `data-od-id`, deterministic browser evidence, mobile and error-state recommendations

### Compact receipt claim

```json
{
  "action_id": "spawn-0001",
  "status": "pass",
  "validation": "Read-only exploration completed; no external browsing, no writes, and claims separated into observation, inference, and unverified assumptions.",
  "artifacts_consulted": [
    "dispatch-sheet.json",
    "strategy-inventory-packet.json",
    "current Akashic feed/schema/runtime/query/current-generation sources",
    "explicitly routed Akashic research/design sources",
    "explicitly routed UI Studio testing precedent"
  ],
  "blockers": [
    "No browser application, HTTP API, or browser-safe adapter exists.",
    "No validated user-task, usability, accessibility, responsive, or browser-interaction evidence exists.",
    "Freshness/live-update behavior is not proved.",
    "The Phase-0 Design is an authored-complete candidate with runtime evidence none and cannot establish current runtime behavior."
  ],
  "exact_selectors": [
    "dispatch-sheet.json#groups[group_id=explorers].agents[agent_name=Halford, Graeme]",
    "strategy-inventory-packet.json#direct_source_fallbacks",
    "example-feed.json#/consumer_contract",
    "graph-queries.mjs#SUPPORTED_OPERATIONS",
    "graph-queries.mjs#executeGraphQuery",
    "cli.mjs#evaluateGraphQuery",
    "periodic-table-graph-schema/findings.md#Six-query contract and worked fixture",
    "phase-0-content-contract/design/ARCHITECTURE.md:3-18"
  ]
}
```

## Agent 2 — Shannon, Claude

Shannon explorer result (action spawn-0002; exact prompt executed; target ~2200 tokens)

## Contract-trace conclusion

The smallest browser-safe adapter is a read-only, same-machine application boundary that (1) loads and schema-validates the reviewed seven-principle feed, (2) reads the digest-bound generated pointer/manifest as a separate freshness surface, and (3) invokes a narrow server-side wrapper around the existing six `executeGraphQuery` request variants. It must never expose filesystem paths as user-controlled runtime arguments, call `runCli` in a browser, mutate authored records, rebuild/publish projections, import Git, dispatch agents, or infer authority. Browser responses should preserve the runtime result/error envelopes verbatim enough to retain selectors and digests, then add only presentation labels.

## Executed Akashic contracts (current source evidence)

- Reviewed feed: `agent-pool/reviewed-content/example-feed.json#/` has exactly seven Principle entries (At, Co, Cr, Ft, Gr, Is, Mo), stable `entry_id` plus `authored_record_id`, authored origin path/digest, two scoped evidence handles per entry, feed and entry claim ceilings, four generation digests, `authority_effect: none`, zero candidates/review artifacts, and a read-only consumer contract with explicit forbidden actions. Its closed schema is `feed-manifest.schema.json#properties` and `#$defs/feed_entry|evidence_handle|consumer_contract` (lines 1-103, 160-270, 308-342).
- Generated projection is distinct and currently fixture-shaped, not the seven-principle witness: `generated/current.json#/` binds generation path, output digest, projection-manifest digest, and schema version. The selected generation’s `projection-manifest.json#/` binds input/output/validation digests, exact file hashes/sizes, and five authored origins; `inventory.json#/entries` contains three synthetic claims and two synthetic sources. UI must label this as “current generated inventory,” not silently substitute it for the reviewed feed.
- Q1-Q6 executable operation set is `src/graph-queries.mjs#SUPPORTED_OPERATIONS` (53-60): PrinciplesInGroup, PapersIllustratingPrinciple, PrinciplesAcrossDomains, EvidenceForPrinciple, PrincipleCoOccurrenceAndTensionStatus, CompareImportSnapshots. Requests/results are closed one-of contracts in `schema/query-contracts.schema.json#$defs/graph_query_request` (1096-1322) and `#$defs/graph_query_result` (1695-1899).
- All non-snapshot queries require exact `expected_authored_input_digest`, then validate the RecordSet before evaluation (`graph-queries.mjs#assertAuthoredState`, 112-125; `#executeGraphQuery`, 356-434). Results are canonical-JSON SHA-256-bound (`#executeGraphQuery`, 435-458; `src/canonical-json.mjs#canonicalJsonBuffer|sha256Digest`, 5-29). Q6 instead exact-binds base/target snapshot IDs and the CLI requires both snapshot inputs (`src/cli.mjs#evaluateGraphQuery`, 660-779).
- Errors are structured, not exceptional UI prose: graph contract failures carry one `{code, selector, message}` in `GraphQueryError` (`graph-queries.mjs#GraphQueryError`, 62-84); CLI usage is exit 2, graph/runtime failure exit 1 with `akashic-graph-query-error/v1`, success exit 0. Record validation sorts typed diagnostics by phase/path/selector/code (`src/diagnostics.mjs#DIAGNOSTIC_CODES|sortDiagnostics`, 1-89); validation covers shape, time/rights, identity, relation tuples/endpoints, references, and relation evidence scopes (`src/validate-records.mjs#validateRecordSet`, 679-711).
- Q semantics: group and paper/domain traversal use authored typed records/relations; evidence returns field-scoped evidence plus illustration evidence; co-occurrence is derived from shared papers, while `tensions` is currently always empty and `tension_status` is `indeterminate` (`graph-queries.mjs#principleCoOccurrenceAndTensionStatus`, 262-354). A frontend must not draw inferred tension edges.

## Browser adapter contract

Server-owned inputs: fixed repository root, approved feed/current-pointer locations, an allowlist mapping six UI actions to closed request shapes, and server-loaded snapshots for Q6. Response union: `{kind:'feed', feed, feed_digest?}`, `{kind:'projection_status', current, manifest, status}`, `{kind:'query_result', result}`, or `{kind:'error', status, diagnostics}`. Do not invent a feed digest unless computed and named as adapter-local; the feed already exposes its four upstream digests. At every result show authored input/result digest (or snapshot IDs/result digest), evidence selectors, and claim ceiling. “Stale/mismatch,” “invalid input,” “no results,” and “indeterminate tension” are distinct states.

## Public-safe Akashic graph profile (candidate architectural inference, not executed schema)

Node candidates: `Principle` (key `authored_record_id`; presentation key `entry_id`), `Group` (`group_id`), `Paper`/`Source` (authored source ID), `Domain` (closed domain ID), `EvidenceHandle` (content-addressed by `evidence_digest` plus source/selector/scope), and `ImportSnapshot` (`snapshot_id`). Every node carries `source_refs` in Akashic terms; feed-derived nodes carry `claim_ceiling`; no node gains authority or truth status.

Allowed candidate edges, all `authority_effect:none` and default-denied otherwise:
- `Principle -> Group : grouped_in`, directed, exactly 1 for a feed Principle.
- `Principle -> Paper : illustrated_by`, directed, 0..N, authored relation only.
- `Paper -> Domain : classified_in_domain`, directed, 0..N, authored relation only.
- `Principle|illustrated_by -> EvidenceHandle : evidenced_by`, directed, 1..N where the underlying Akashic contract requires evidence; preserve relation and scope.
- `Principle <-> Principle : co_occurs_with`, symmetric derived view only, witnessed by paper IDs; not declarable.
- Snapshot comparison is a derived view between two identified snapshots, not a persisted edge.
No `tensions_with` edge is allowed: current execution returns indeterminate/no tension evidence. No inverse is declarable; reverse labels are read views. Cycles are impossible for the four authored directed edge families under these endpoint kinds; derived symmetric co-occurrence is explicitly cycle-permitted but value-free and non-authoritative. Revisit cycle policy if kinds/endpoints expand.

## Private-precedent reuse/adapt/reject

Private sources remain candidate precedent only: `cyberAlchemy-v2/ontology/README.md#Ontology` (1-18) says ontology may model/project but cannot promote or redefine owner contracts; Node and Relation models are candidate/non-schema (`NODE-MODEL.md#Purpose|Node Concept Contract`, 6-59; `RELATION-MODEL.md#Purpose|Relation Contract`, 6-26).

| Pattern | Verdict | Akashic-safe treatment |
|---|---|---|
| stable node identity | adapt | use existing authored IDs, entry IDs, group/domain IDs, evidence digest, snapshot ID; no private IDs |
| source references | adapt | Akashic authored origins and evidence source/selector/scope |
| confidence | reject for v1 | no executed Akashic confidence contract; do not turn evidence or review into a score |
| challenge/residue | adapt | visible gap/indeterminate/error states only; no imported challenge protocol |
| typed endpoints | adapt | candidate allowed-edge signatures above, grounded in query behavior |
| direction | adapt | preserve authored direction; symmetric only for derived co-occurrence |
| evidence refs | reuse structurally | use executed evidence handles unchanged, including digest/scope/relation |
| authority_effect | reuse structurally | explicit `none`, already present in feed; never infer promotion |
| cardinality | adapt | derive only constraints proven by feed/schema/query shapes; otherwise 0..N |
| default denial | adapt | only listed public-safe edges; precedent file says unlisted forbidden but is scoped to four private Evidence kinds (`ALLOWED-EDGES.yaml` 1-14), so its catalog cannot be copied |
| inverses | adapt | read labels only, never separately declared edges (`ALLOWED-EDGES.yaml` 11-12) |
| cycle policy | adapt | explicit per-family policy above; unknown expansion blocks selection |
| projection separation | reuse structurally | authored records, generated inventory, reviewed feed, and browser view remain non-collapsing layers |

Private relation `authority_effect`, endpoint completeness, and cycle review are useful questions (`RELATION-MODEL.md#Relation Contract|Value-Cycle Guard|Endpoint Rule`, 13-43, 73-77), but its predicates and CAV2 identifiers are rejected. Private node confidence/challenge fields are rejected from v1 because Akashic has no executed counterparts. No CyberAlchemy file, identifier, schema, predicate, or runtime becomes a dependency.

## Claim ceiling / residue

This maps current source contracts and proposes an adapter/profile. It does not prove an HTTP implementation, browser security, usability, accessibility, deployment, live Git transport, agent execution, schema acceptance, publication, or ontology promotion. The stale Akashic README was not used. Inventory entries were treated only as routing leads.

Compact receipt: `action_id=spawn-0002`; `status=complete`; validation=`read-only selector verification against sheet, packet, direct Akashic contracts, exact runtime dependencies, and four permitted private precedent files; no external browse; no writes`; artifacts consulted=`dispatch-sheet.json; strategy-inventory-packet.json; example-feed.json; feed-manifest.schema.json; graph-queries.mjs; cli.mjs; query-contracts.schema.json; validate-records.mjs; diagnostics.mjs; canonical-json.mjs; generated/current.json; selected generation projection-manifest.json and inventory.json; ontology README.md, NODE-MODEL.md, RELATION-MODEL.md, canonical-kinds/ALLOWED-EDGES.yaml`; blockers=`none for research return; implementation/schema/publication remain unapproved`; exact selectors=`sheet groups.explorers.agents[agent_name=Shannon, Claude]; packet direct_source_fallbacks; feed #/ and schema properties/$defs; graph-queries SUPPORTED_OPERATIONS/assertAuthoredState/executeGraphQuery/query helpers; cli evaluateGraphQuery; query schema graph_query_request/result; validateRecordSet; diagnostics DIAGNOSTIC_CODES/sortDiagnostics; canonicalJsonBuffer/sha256Digest; current #/; generation manifests #/; private headings Ontology, Node Concept Contract, Relation Contract, Value-Cycle Guard, Endpoint Rule, ALLOWED-EDGES lines 1-14`.

## Agent 3 — Ashby, W. Ross

## Ashby explorer return — frontend state and evidence-feedback model

### Observations

1. The smallest concrete UI input is the seven-entry reviewed feed, not the generated `current.json` pointer. It contains `At`, `Co`, `Cr`, `Ft`, `Gr`, `Is`, and `Mo`, each with an authored origin, two evidence handles, and an entry-level claim ceiling. The feed itself is explicitly read-only, excludes candidates and review artifacts, has `authority_effect: "none"`, and forbids acceptance, mutation, promotion, publishing, authority grants, agent dispatch, and self-review.  
Selectors: `projects/akashic-records/agent-pool/reviewed-content/example-feed.json#/entries`, `#/consumer_contract`, `#/candidates_included`, `#/review_artifacts_included`, `#/authority_effect`, `#/claim_ceiling`; schema: `feed-manifest.schema.json#/properties/{entries,consumer_contract,candidates_included,review_artifacts_included,authority_effect,claim_ceiling}`.

2. The feed’s provenance is displayable without presenting it as truth: `generated_from` binds input, output, manifest, and request digests; each entry binds `authored_origin.path`, `authored_origin.digest`, and evidence handles (`source_id`, selector, relation, scope, evidence digest).  
Selectors: `example-feed.json#/generated_from`; `#/entries/0..6/{authored_origin,evidence_handles,claim_ceiling}`; `feed-manifest.schema.json#/$defs/{feed_entry,evidence_handle}`.

3. A current generated pointer exists but is only a pointer to one generation plus output and manifest digests. It does not itself establish freshness, parity, review, publication, or authority.  
Selector: `projects/akashic-records/generated/current.json#/`.

4. The existing query layer has six useful, bounded operations: `CompareImportSnapshots`, `EvidenceForPrinciple`, `PapersIllustratingPrinciple`, `PrincipleCoOccurrenceAndTensionStatus`, `PrinciplesAcrossDomains`, and `PrinciplesInGroup`. Non-Q6 queries require the request’s expected authored-input digest to equal the supplied RecordSet digest; invalid requests, unsupported expressions, source-state mismatch, and invalid input become structured diagnostics.  
Selectors: `projects/akashic-records/src/graph-queries.mjs#SUPPORTED_OPERATIONS`, `#assertRequest`, `#assertAuthoredState`, `#executeGraphQuery`; `projects/akashic-records/src/cli.mjs#evaluateGraphQuery`.

5. The current callable surface is a local Node CLI, not an HTTP/browser adapter. Any frontend must receive a bounded read projection or a new read-only adapter; it should not invoke filesystem or Git-import CLI behavior from the browser.  
Selectors: `projects/akashic-records/src/cli.mjs#evaluateCli`, `#evaluateGraphQuery`, `#parseGitImportArguments`.

6. The selected UI Studio research is useful testing precedent, not usability proof. It identifies stable `data-od-id` targets, DOM/screenshot Playwright checks, explicit current-head projection, visible-change integrity, and state coherence after external writes. It also records a caveat: reported Playwright success was shimmed and checked-in fresh e2e was not established in that research run.  
Selectors: `projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/findings.md#What Is Working Now` (stable targets), `#Where the UX/UI Breaks Trust`, `#Rank` rows 1–7, `#Next Implementation Order`.

### Recommended state model

Adopt a compact, always-visible “projection status strip” above the content explorer:

- `Projection`: current pointer’s generation path, output digest (shortened visually but copyable), manifest digest, and a neutral “loaded projection” state.
- `Bound input`: feed `generated_from.input_digest`, schema/profile IDs, and the exact content count “7 reviewed entries”.
- `Ceiling`: “Read-only reviewed content — no admission, review, authority, publishing, or deployment.” Link this to a details drawer that exposes the feed’s explicit forbidden actions.
- `Evidence`: per selected entry, show authored origin plus its evidence handles and selectors in a readable list, not raw JSON.
- `Gaps`: show only concrete absences that the selected dataset can support, e.g. “No candidates included” and “No review artifacts included,” plus query empty results. Never infer missing subject-matter coverage from absence in this feed.
- `Failure`: a dedicated diagnostic panel for `invalid_input`, `unsupported_expression`, and `source_state_mismatch`, containing the code, selector, plain-language meaning, and safe recovery. Do not leave the prior result visually active after a failed query.

This makes provenance and boundaries observable without implying that a digest proves truth, freshness in the wall-clock sense, review, or authority.

### Smallest screen-level flow

1. **Explore reviewed principles** — seven cards/table rows with symbol, title, group, short description, and “Evidence” action. Default state is the reviewed feed only.
2. **Inspect a principle** — open a detail drawer: proposition, authored origin, claim ceiling, evidence handles, and bounded actions:
   - “Show evidence” → `EvidenceForPrinciple`
   - “Related papers” → `PapersIllustratingPrinciple`
   - “Group members” → `PrinciplesInGroup`
3. **Read result or failure** — result view carries the bound input digest and query operation; empty result means “no matching result in this bound RecordSet,” not a negative universal claim. Failure replaces result state with the precise diagnostic.
4. **Projection details** — status strip expands to expose current pointer fields and distinguishes feed-bound provenance from `current.json` pointer provenance.

Q6 snapshot comparison should be deferred from the first screen unless an adapter can supply both explicit snapshot inputs; its input shape is distinct from the feed-backed queries.

### Browser-state and test contract

Use stable, domain-owned selectors such as:

- `data-od-id="projection-status"`
- `data-od-id="projection-digest"`
- `data-od-id="claim-ceiling"`
- `data-od-id="principle-entry-<symbol>"`
- `data-od-id="evidence-handle-<entry>-<n>"`
- `data-od-id="query-result"`
- `data-od-id="query-empty"`
- `data-od-id="query-diagnostic"`
- `data-od-id="gap-candidates-excluded"`
- `data-od-id="gap-review-artifacts-excluded"`

Initial acceptance checks should prove UI/state correspondence, not usability or trust:

- The rendered count is seven and each rendered card maps to exactly one feed entry.
- Selecting `At` exposes `entry:claim:at`, its authored origin, two evidence selectors, and its claim ceiling.
- A result visibly names its operation and expected/bound input digest.
- An injected `source_state_mismatch` renders the diagnostic panel and removes or marks stale the prior result.
- The status strip shows the exact `current.json` generation/output/manifest fields without saying “approved,” “published,” or “fresh.”
- Viewport checks can establish non-overlap, keyboard reachability, and readable status/error content; they do not establish accessibility conformance or user comprehension.

### Boundaries and unresolved matters

- The Phase-0 design documents remain planned/unexecuted candidate design evidence, while the feed and runtime files above provide the current bounded frontend inputs. Do not merge their claim levels.  
  Selectors: `projects/akashic-records/development/phase-0-content-contract/design/ARCHITECTURE.md#Status`, `#Contract State`, `#Authority Non-Collapse`; `VALIDATION-CONTRACTS.md#Contract State Legend`, `#VC-SELECTOR`, `#VC-PROJECTION`.

- Browser evidence can show that a projected status, evidence handle, or failure state is rendered and selectable. It cannot prove user trust, comprehension, accessibility conformance, freshness beyond the displayed bindings, review, authority, publication, or deployment.

- No existing browser app, frontend toolchain, HTTP API, live transport, write workflow, or agent-execution surface was found in the allowed sources. The frontend direction therefore remains an architectural inference: consume a precomputed feed/current-pointer pair and an explicitly read-only query adapter, rather than exposing the CLI directly.

### Compact receipt claim

```yaml
action_id: spawn-0003
status: pass
validation:
  - read-only scope maintained; no files written
  - no external browsing
  - source claims grounded in selected packet-routed files
artifacts_consulted:
  - ops/development/2026-07-27-akashic-frontend-ontology-foundation/dispatch-sheet.json
  - ops/development/2026-07-27-akashic-frontend-ontology-foundation/strategy-inventory-packet.json
  - projects/akashic-records/agent-pool/reviewed-content/example-feed.json
  - projects/akashic-records/agent-pool/reviewed-content/feed-manifest.schema.json
  - projects/akashic-records/generated/current.json
  - projects/akashic-records/src/graph-queries.mjs
  - projects/akashic-records/src/cli.mjs
  - projects/akashic-records/development/phase-0-content-contract/design/ARCHITECTURE.md
  - projects/akashic-records/development/phase-0-content-contract/design/VALIDATION-CONTRACTS.md
  - ops/development/2026-07-26-akashic-contract-architecture/findings.md
  - projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/findings.md
blockers:
  - no browser runtime, HTTP API, or read-only browser adapter exists
  - no user/usability/accessibility evidence exists
  - current pointer does not establish parity, review, authority, or wall-clock freshness
  - UI Studio browser precedent includes shimmed-e2e caveat
exact_selectors:
  - example-feed.json#/consumer_contract
  - example-feed.json#/generated_from
  - example-feed.json#/entries/0..6/{entry_id,authored_origin,evidence_handles,claim_ceiling}
  - feed-manifest.schema.json#/$defs/{feed_entry,evidence_handle}
  - current.json#/
  - graph-queries.mjs#SUPPORTED_OPERATIONS
  - graph-queries.mjs#{assertRequest,assertAuthoredState,executeGraphQuery}
  - cli.mjs#{evaluateCli,evaluateGraphQuery}
  - ARCHITECTURE.md#{Status,Authority Non-Collapse}
  - VALIDATION-CONTRACTS.md#{Contract State Legend,VC-SELECTOR,VC-PROJECTION}
  - ui-prototyping findings.md#{What Is Working Now,Where the UX/UI Breaks Trust,Rank,Next Implementation Order}
```
