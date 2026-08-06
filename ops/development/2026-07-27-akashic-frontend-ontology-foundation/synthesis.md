# Frontend and graph candidate synthesis

Action `spawn-0004` — frontend graph synthesis

Status: `pass`  
Validation: Read-only synthesis completed from the target dispatch sheet, all three named receipts, and all three verbatim explorer returns. No external browsing or writes.

## Preserved disagreements

- Halford says the first product should be a readable reviewed-content explorer, not a graph canvas; Shannon agrees on bounded queries but requires an explicit typed graph profile and exact digest/error preservation.
- Ashby would defer Q6 from the first screen unless two snapshots are available; Halford includes it as an explicitly separate comparison step; Shannon requires Q6 remain in the adapter contract because it is one of the six executed operations.
- Ashby recommends an always-visible projection strip; Halford’s progressive disclosure keeps exact provenance below readable content. The synthesis retains a compact always-visible ceiling/binding summary, with full digests and selectors disclosed on demand.
- `generated/current.json` is not the seven-principle source. The reviewed feed and generated Inventory are separate projections and must never be visually collapsed.

## Candidate 1 — Reviewed Principle Explorer with bounded question panel

Recommended smallest direction.

**Primary journey:** Browse seven reviewed principles → open one principle → inspect its source evidence → run one of six named questions → receive an ordered result, empty state, indeterminate state, or structured diagnostic.

**Screens/components**

1. Browse: cards/list, group filter, compact binding/ceiling strip.
2. Principle detail: proposition, group, authored origin, claim ceiling.
3. Evidence drawer/small-screen page: source ID, selector, relation, scope, digest.
4. Question panel: six closed actions, with Q6 in a separate snapshot-comparison section.
5. Result/diagnostic region: operation, bound digest or snapshot IDs, result digest, result/empty/indeterminate/error state.
6. Projection details: reviewed-feed bindings separate from generated Inventory pointer.

**Data flow and adapter:** Browser calls a same-machine, read-only Node adapter. Server owns repository paths, validates the reviewed feed, reads the generated pointer separately, allowlists six closed request variants, invokes `executeGraphQuery`, and returns feed/projection/query/error unions. It never exposes the CLI, filesystem paths, Git import, mutation, review, publication, authority, or agent actions.

**Technology:** dependency-light semantic HTML/CSS/ES modules plus a narrow Node HTTP adapter around existing modules. This minimizes new infrastructure while preserving runtime contracts. Technology choice remains architectural inference because no frontend toolchain or HTTP implementation exists.

**Accessibility/testing:** semantic headings, labelled regions, keyboard-operable disclosure, focus return, non-modal mobile evidence view, wrapped/copyable digests, text-plus-color statuses, and live announcement for completed/error queries. Stable domain-owned `data-od-id` hooks support deterministic Playwright assertions. These checks prove correspondence and keyboard/viewport behavior, not usability, trust, or accessibility conformance.

**Cost/complexity:** low-to-medium. Main complexity is secure adapter allowlisting, digest preservation, Q6 snapshot loading, and faithful diagnostics.

**Deferrals:** free-form queries, graph canvas, authoring, candidate acceptance, review persistence, Git transport, live refresh, agent execution, authority, publication, deployment.

**Evidence ceiling:** candidate architecture only; no HTTP, security, browser, user, accessibility, deployment, or publication evidence.

Citations: Halford return, `### Smallest primary journey`, `### Information architecture and screen sequence`, `### Progressive disclosure model`, `### Boundaries and deferred scope`; exact selectors `example-feed.json#/consumer_contract`, `graph-queries.mjs#SUPPORTED_OPERATIONS`, `cli.mjs#evaluateGraphQuery`. Shannon return, `## Browser adapter contract`, exact selectors `graph-queries.mjs#executeGraphQuery`, `query-contracts.schema.json#$defs/graph_query_request`, `#$defs/graph_query_result`. Ashby return, `### Recommended state model`, `### Browser-state and test contract`, exact selectors `current.json#/`, UI Studio findings `#What Is Working Now`.

## Candidate 2 — Static reviewed-feed reader plus server-rendered query pages

**Primary journey:** Browse/read the seven-principle feed from a generated static page; follow evidence disclosures; submit named query forms to server-rendered result pages.

**Component map:** static principle index/detail sections, evidence disclosures, six HTML forms, projection provenance page, server-rendered result/error templates.

**Data flow/runtime:** build or serve the reviewed feed into HTML; form posts reach the same allowlisted read-only Node boundary. No client application state.

**Technology:** semantic server-rendered HTML with minimal CSS/JavaScript and Node request handlers.

**Exact witness:** It can render all seven principles and all Q1–Q6 operations, including Q6’s two snapshot selectors, but comparison/result transitions are less fluid and prior-result invalidation is naturally page-based.

**Accessibility/testing:** strongest native HTML baseline; stable hooks and Playwright can verify seven rows, At evidence, all form shapes, digest bindings, diagnostics, and narrow viewport layout.

**Cost/complexity:** lowest client complexity; medium server/template complexity. Progressive disclosure and evidence comparison are less convenient.

**Risks:** users may lose context between principle and results; server-rendered diagnostics can become technical; static feed build timing could be mistaken for freshness unless prominently labelled.

**Deferrals/ceiling:** same as Candidate 1. No claim of live freshness or usability.

Citations: Halford, `### Information architecture and screen sequence` and responsive risks; Ashby, `### Smallest screen-level flow`; Shannon, `## Contract-trace conclusion` and `## Executed Akashic contracts`.

## Candidate 3 — Graph-first canvas with inspector

Not recommended for v1.

**Primary journey:** Select a principle node, traverse typed edges, open evidence/result inspector, switch among Q1–Q6 overlays.

**Technology:** client graph-rendering library plus Node adapter.

**Cost/complexity:** high: layout, keyboard navigation, responsive behavior, semantic equivalents, graph/result synchronization, and a new dependency surface.

**Risks:** graph appearance may imply arbitrary traversal, persisted relations, inferred tension, completeness, or authority. It makes progressive disclosure and screen-reader equivalence harder. No latency/capability witness justifies a persisted graph index or graph canvas.

**Deferrals:** entire candidate until a validated user/capability need exists.

**Verdict:** reject for the first frontend, retain only as a future visualization over the same read-only typed result profile.

Citations: Halford, `### Smallest primary journey` (“should not start as a graph canvas”); Shannon, Q semantics under `graph-queries.mjs#principleCoOccurrenceAndTensionStatus`; Ashby, `### Boundaries and unresolved matters`.

## Exact seven-principle and Q1–Q6 witness

The browse view must show exactly `At, Co, Cr, Ft, Gr, Is, Mo` from `example-feed.json#/entries`, each mapping one-to-one to an entry. Selecting `At` must expose `entry:claim:at`, its authored origin, two evidence handles/selectors, and its claim ceiling.

| Query | Screen witness | Required binding/state |
|---|---|---|
| Q1 `PrinciplesInGroup` | choose a displayed group; return ordered matching principles | expected authored-input digest |
| Q2 `PapersIllustratingPrinciple` | from At, request related papers | authored typed relations; empty means no reviewed result |
| Q3 `PrinciplesAcrossDomains` | choose closed domain IDs; return principles | authored Paper→Domain traversal |
| Q4 `EvidenceForPrinciple` | “Show evidence” for At | field-scoped evidence plus illustration evidence |
| Q5 `PrincipleCoOccurrenceAndTensionStatus` | show shared-paper witnesses | `tensions: []`, visibly `tension_status: indeterminate`; never infer “no tension” |
| Q6 `CompareImportSnapshots` | separate base/target snapshot form | both snapshot IDs/inputs and result digest; missing inputs are prerequisite failure |

A supplied digest mismatch must replace or mark stale the prior result and show `source_state_mismatch`, selector, safe recovery, expected digest, and supplied digest. Unsupported, invalid, empty, and indeterminate states remain distinct.

Citations: Shannon, `## Executed Akashic contracts`, selectors `graph-queries.mjs#SUPPORTED_OPERATIONS`, `#assertAuthoredState`, `#executeGraphQuery`, `#principleCoOccurrenceAndTensionStatus`, `cli.mjs#evaluateGraphQuery`; Ashby, `### Browser-state and test contract`; Halford, `### Empty, mismatch, and failure states`.

## Public-safe Akashic graph profile

Candidate nodes:

- `Principle`: authored record ID; presentation entry ID.
- `Group`: group ID.
- `Paper`/`Source`: authored source ID.
- `Domain`: closed domain ID.
- `EvidenceHandle`: evidence digest plus source, selector, relation, scope.
- `ImportSnapshot`: snapshot ID.

All carry Akashic source references where applicable; feed-derived nodes retain claim ceilings. No node implies truth, approval, or authority.

Allowed edges, default-denied otherwise:

| Edge | Direction/cardinality | Status |
|---|---|---|
| Principle `grouped_in` Group | directed; exactly 1 for feed principle | authored/feed-grounded |
| Principle `illustrated_by` Paper | directed; 0..N | authored only |
| Paper `classified_in_domain` Domain | directed; 0..N | authored only |
| Principle or illustration relation `evidenced_by` EvidenceHandle | directed; required only where Akashic contract requires | preserve scope/relation |
| Principle `co_occurs_with` Principle | symmetric; 0..N | derived read view, witnessed by paper IDs |
| Snapshot comparison | none persisted | derived result between two IDs |

Every edge has `authority_effect:none`. No `tensions_with` edge is allowed. Reverse labels are views, not declared inverse edges. Authored edge families are acyclic under these endpoint kinds; symmetric co-occurrence permits cycles as a value-free derived view. Kind expansion reopens cycle review.

## CyberAlchemy precedent decisions

| Structural pattern | Decision | Akashic treatment |
|---|---|---|
| Stable node identity | adapt | existing Akashic authored/entry/group/domain/evidence/snapshot IDs |
| Source references | adapt | authored origins and evidence source/selector/scope |
| Confidence | reject | no executed Akashic confidence contract |
| Challenge/residue | adapt | visible gap, indeterminate, and diagnostic states only |
| Typed endpoints | adapt | exact candidate signatures above |
| Direction | adapt | authored direction; symmetry only for derived co-occurrence |
| Evidence refs | reuse structurally | executed evidence handles without private vocabulary |
| `authority_effect` | reuse structurally | explicit `none`, already present publicly |
| Cardinality | adapt | only constraints proved by current contracts; otherwise 0..N |
| Default denial | adapt | only listed Akashic edges; do not copy private catalog |
| Inverses | adapt | read labels only |
| Cycle policy | adapt | per-family policy above; expansion blocks until reviewed |
| Projection separation | reuse structurally | authored records, generated Inventory, reviewed feed, browser view remain distinct |

No CyberAlchemy identifier, predicate, prose, schema, file, or runtime dependency is imported. Private precedent remains candidate context, never authority or promotion-by-proximity.

Artifacts: dispatch sheet; three explorer receipts; `research.md#agent-1--halford-graeme`; `#agent-2--shannon-claude`; `#agent-3--ashby-w-ross`.  
Blockers: no browser app, HTTP adapter, validated user study, accessibility/usability evidence, freshness contract, deployment evidence, or approved public graph schema exists.
