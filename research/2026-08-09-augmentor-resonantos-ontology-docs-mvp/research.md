# Augmentor, ResonantOS, SDK, Agent API, and Living Archive Research Returns

These are the bounded explorer returns from the confirmed research dispatch.
They are preserved as explorer-owned evidence and have not yet been reconciled
by the synthesizer. Normalized action receipts are stored under `receipts/`.

## Explorer Turing — Current-State Lane

### Verdict

ResonantOS already contains two distinct implemented surfaces:

1. an internal Add-on SDK contract/validator; and
2. a host-owned, read-only Augmentor consultation API.

They are not the same interface, and current source does not show the
consultation API exposed through `src/sdk/addons/`. The smallest accurate
correction is therefore:

> Show the existing Add-on SDK as an implemented supporting part of Augmentor's
> ResonantOS capability environment, while labeling an add-on-facing
> ontology-consultation SDK adapter/contract as planned or absent.

The current anatomy page collapses these two facts into “Add-on SDK seam —
planned,” then says “No developer kit is installed.” That is stale as a
statement about the SDK generally, although it remains valid for the specific
consultation-via-SDK extension.

### Exact-Binding Component And Interface Graph

| Node | Classification | Owner/boundary | Exact evidence |
| --- | --- | --- | --- |
| ResonantOS Alpha runtime | implemented + documented | Chrome MV3 extension plus authenticated loopback Node bridge; no additional required process | `AGENTS.md#Alpha Runtime Boundary`; `docs/architecture/README.md:24-36`; `docs/architecture/MODULE_MAP.md:7-32` |
| Augmentor user interface | implemented + documented | Extension side panel owns conversation, command routing, approvals, and presentation | `docs/architecture/MODULE_MAP.md:14-24`, especially `:19`; `docs/architecture/MODULE-OWNERSHIP.md:20-21` |
| Add-on SDK V0 | implemented + documented | Supporting SDK source, not a separate Alpha process and not yet a public marketplace SDK | `docs/architecture/README.md:79,91`; `docs/architecture/MODULE_MAP.md:63-76`, especially `:71`; `docs/architecture/MODULE-OWNERSHIP.md:39-46`; `docs/architecture/ADR-018-addon-sdk-v0.md:15-22` |
| Add-on SDK public code surface | implemented | Exports manifest types, SDK version, capabilities/protocols, registry, surface routing, and validation | `src/sdk/addons/index.ts:3-33`; `src/sdk/addons/contracts.ts:24-45,62-83` |
| Add-on manifest validator | implemented | Validates runtime/category/surface, capability, system-slot, memory, tool, skill, connector, and related constraints | `src/sdk/addons/validation.ts:23-110`; validator implementation thereafter; representative tests `src/sdk/addons/validation.test.ts:270-357,361-435,498-560,684-774` |
| Replaceable Augmentor Chat slot model | documented; implementation degree unverified in this bounded lane | Augmentor Chat is a bundled recommended add-on concept providing `primary-agent` and `chat-interface`; the ADR also records migration work | `docs/architecture/ADR-026-minimal-kernel-replaceable-default-addons.md:17-21,51-66,164-191` |
| Augmentor consultation contract | implemented | Closed query/result versions, projection/glossary/manifest validation, optional anatomy focus | `browser-first/host/augmentor-consultation-contract.mjs`; `docs/reference/AUGMENTOR_CONSULTATION_API.md:3-20,89-131` |
| Augmentor consultation engine | implemented | Read-only search/context over an installed neutral projection; returns evidence under a claim ceiling and forbidden-inference list | `browser-first/host/augmentor-consultation-service.mjs:18-20,55-93,162-216,222-280` |
| Augmentor agent-context adapter | implemented | Organizes retrieved evidence for answer composition; does not generate prose or grant authority | `browser-first/host/augmentor-consultation-agent-context.mjs:3-17,18-43,45-67`; `docs/reference/AUGMENTOR_CONSULTATION_API.md:133-150` |
| Consultation host route | implemented | `POST /augmentor/consultation`, capability `augmentor-consultation-read`; owns auth context and calls service | `browser-first/host/augmentor-consultation-host-service.mjs:8-19,20-58` |
| Consultation route composition into bridge | implemented | Host service is constructed and its routes included in bridge composition | `browser-first/host/run-bridge-minimal.mjs:34,357,365` |
| Bridge enforcement edge | implemented | Transport authenticates, resolves route, checks required capability, strips consultation key before handler | `browser-first/host/bridge-server.mjs:885-892,1066-1098` |
| Installed consumer projection | conditionally present, not repository-bundled runtime truth | Must be owner-approved and installed into external user state; bridge does not read private ontology checkout | `docs/reference/AUGMENTOR_CONSULTATION_API.md:22-40`; `browser-first/host/augmentor-consultation-host-service.mjs:11-19` |
| Candidate ontology anatomy map | implemented as candidate-local presentation data; not authority | Presentation-only orientation over source-bound records | `projects/augmentor/ontology/unified-agent/visualization/anatomy-map.json:2-15,212-217` |
| Candidate generated page | implemented as a static candidate page | Embeds an Agent API page contract, posts same-origin to `/augmentor/consultation`, validates response/redirect/content type, and degrades when disconnected | `projects/augmentor/ontology/unified-agent/ontology-visualization.html:1165-1172,1413-1475,1840-1893,1900-1975` |
| Add-on SDK to general Augmentor environment | documented, with implemented SDK substrate | Add-ons may provide Augmentor skills and tools, but contracts grant no extra authority | `docs/architecture/ADR-018-addon-sdk-v0.md:100-126,218-250,340-360`; `src/sdk/addons/contracts.ts:26-42` |
| Add-on SDK to ontology consultation API | absent/unverified | No export, contract, capability, protocol, or adapter for ontology consultation appears in the inspected SDK files | Negative inspection of `src/sdk/addons/{index,contracts,validation}.ts`; the route instead belongs to `browser-first/host/augmentor-consultation-*.mjs` |
| Page to consultation API | implemented in candidate page code; live deployment unverified | Same-origin `fetch`, no consultation secret in page code, explicit disconnected/error states | `ontology-visualization.html:1165,1855-1893,1942-1964`; operator boundary `docs/reference/AUGMENTOR_CONSULTATION_API.md:152-168` |

### Edge Classification Summary

```text
Person
  -> Augmentor extension UI                         implemented/documented
  -> candidate ontology/Agent API page             candidate implementation

Augmentor extension
  -> authenticated Node bridge                     implemented/documented

Node bridge
  -> POST /augmentor/consultation                  implemented
  -> scoped capability/auth enforcement            implemented
  -> installed neutral projection                  implemented contract;
                                                   installed instance unverified

Consultation service
  -> reviewed evidence + answerPolicy              implemented
  -> agent-context composition helper              implemented
  -> answer generation                             absent by design
  -> ontology edits / memory writes / approval     absent by design

ResonantOS capability environment
  -> Add-on SDK manifest/contracts/validation      implemented/documented
  -> add-on tools and Augmentor skills             implemented contract surface
  -> ontology-consultation SDK adapter             absent/unverified

Candidate page
  -> same-origin consultation route                implemented page binding
  -> protected deployed API                        unverified in this lane
```

### Stale Or Misleading Statements

The load-bearing stale source is `anatomy-map.json:200-209`:

- `Add-on SDK seam — planned` incorrectly makes the entire SDK appear future.
- `External · planned · not installed` is supportable only for the proposed
  ontology-consultation SDK extension, not for the internal SDK substrate.
- `ontology-visualization.html:2071-2075` repeats the collapse with “No
  developer kit is installed.”

The generated page embeds the stale anatomy object, so the stale classification
is visibly propagated into the page. By contrast, its Agent API binding is
current and concrete at `ontology-visualization.html:1165` and `:1942-1954`.

### Smallest Correction

Split the current single `addon-sdk` presentation seam into two displayed facts
without changing runtime semantics:

1. **Add-on SDK — existing internal ResonantOS capability substrate**
   - posture: implemented/documented;
   - connected visually to the ResonantOS environment around Augmentor, not
     portrayed as an Augmentor organ or separate Alpha process;
   - boundary: internal SDK V0, not public marketplace/release proof, and
     manifest contracts do not grant runtime authority.
2. **Ontology consultation through the Add-on SDK — planned/not implemented**
   - posture: planned or absent;
   - may remain disconnected;
   - the implemented consultation route is host-owned and direct, not evidence
     of an SDK extension.

Do not relabel the host consultation API as the Add-on SDK. They have different
owners and enforcement surfaces.

### Runtime And Ownership Boundaries

- The page is a consumer UI. It does not own projection validation, access
  grants, route authorization, source memory, ontology mutation, or answer
  authority.
- `browser-first/host/augmentor-consultation-*.mjs` owns read-only consultation
  and explicitly excludes raw ontology, generated answers, memory writes,
  approval, routing, and authority decisions (`MODULE-OWNERSHIP.md:28`).
- `src/sdk/addons/` owns manifest/capability/protocol/validation contracts, and
  those contracts do not grant runtime capabilities (`MODULE-OWNERSHIP.md:46`).
- Architecture applicability is owned by the architecture index; current
  source ownership by `MODULE-OWNERSHIP.md` (`README.md:112-120`).
- The candidate anatomy/page remains candidate-local with
  `authority_effect: none` and no release admission (`anatomy-map.json:212-217`).
- No deployment, publication, release, production status, or installed
  projection state is established by this inspection.

### MVP Validation Surfaces

- Static/source consistency must distinguish the existing internal SDK from the
  planned consultation extension, preserve `/augmentor/consultation`, and avoid
  claims of public SDK availability or deployment.
- SDK validation should include `src/sdk/addons/validation.test.ts` and
  `src/sdk/addons/public-manifests.test.ts`.
- Consultation validation should include
  `browser-first/test/augmentor-consultation.test.mjs` and the bounded
  deployment-adapter contract without turning it into production proof.
- Documentation checks are `npm run docs:check` and `npm run test:docs`.
- Because page behavior is involved, the owning matrix also points to
  `npm run test:browser-first`.
- Browser acceptance should cover desktop/mobile presentation, keyboard access,
  controlled Agent API success, and explicit disconnected-route degradation.

Residue: no live browser, deployment, or installed-projection state was
verified; replaceable Augmentor Chat completeness remains unverified; no
implementation, promotion, publication, deployment, release, or production
inference is authorized.

## Explorer Ahrens — Documentation And Living Archive Lane

### Verdict

Use one progressively disclosed documentation experience built around a stable
teaching sequence:

`Orient → Explore → Inspect Augmentor → Build with interfaces → Verify evidence → Open deep reference`

The experience should reuse the current Augmentor page's body/technical-map
duality and Agent API console, then add the missing ResonantOS overview,
explicit SDK material, Living Archive concept lifecycle, and a consolidated
evidence/limitations layer. It must remain a projection over separately owned
evidence; it is neither ontology authority nor implementation proof.

Living Archive integration should extend the already planned `Source-Bound
Recall Cycle`, not create another memory platform. The ontology concept is a
source-bound AI Memory record with typed meaning and retrieval metadata. It may
be admitted to trusted wiki memory only through the existing host-mediated
review/verifier boundary. The concept, documentation page, graph projection,
Augmentor, and add-ons must never promote it by themselves.

### Evidence And Claim Boundary

- Living Archive remains docs-first with runtime and primary artifact type
  undecided: `/home/vrondelli/projects/living-archive/README.md#Current State`
  and `#Working Rule`.
- The memory-agent refinement is a passed definition and non-executed plan. Its
  smallest unit is one source-bound item recalled across a thread boundary with
  source, selection reason, current-status check, or abstention:
  `RESULT.md#Smallest Coherent Unit` and `#Refine Result`.
- Implementation remains blocked by unselected stack and SWU:
  `WORK-PACK.md#Control Fields` and `#Blockers And Gaps`.
- Living Archive distinguishes Human Knowledge, External Knowledge, and AI
  Memory; concepts and syntheses belong to AI Memory and retain source-version
  links: `ADR-013-living-archive-memory-domains.md#Memory Domains` and
  `#Managed Structure`.
- ResonantOS System Architecture Memory defines source-hash-based `ready`,
  `stale`, `blocked`, and `missing` states: `ADR-014-system-architecture-memory.md#Rules`
  and `#Interfaces`.
- ADR-027 defines source → ingest review artifact → independent verifier/policy
  decision → eligible promotion, with human review for risky cases:
  `ADR-027-living-archive-llm-wiki-compliance.md#Decision` and
  `#Approval And Automation Rules`.
- Current host surfaces separate reads such as `/memory/search` and wiki-page
  reading from review/promotion routes such as
  `/archive/review/artifact/promote`: `memory-host-service.mjs:createMemoryHostService`.
- Source review computes new/changed/unchanged states from version manifests and
  hashes; review is read-only while intake writes only to `Memory/INTAKE`:
  `memory-source-intake-host-service.mjs:sourceReviewSnapshot`,
  `executeMemorySearch`, and `executeMemoryWikiHealth`.
- The simple ontology presentation teaches a “map of meaning with receipts”
  while separating evidence, meaning, commitment, consequence, and refusal:
  `findings.md#Presentation Thesis`, `#Five-Slide Spine`, and
  `#Forbidden Overclaims`.
- The later presentation result gives `Find candidate evidence. Type meaning.
  Bound context. Gate use.` and says memory, ontology, context, Inventory, and
  authority are not runtime actors: Inventory synthesis `#Room Definition and
  Retell Chain` and `#Agent Context and Authority Boundary`.
- The current page provides accessible navigation, beginner body view,
  technical exact-record view, Agent API console, keyboard graph elements,
  visible status/limitations, and reduced motion. It still collapses the SDK
  consultation seam into wholly planned status: `ontology-visualization.html:861`,
  `:878`, `:884`, `:937`, `:1086`, `:845`, and embedded
  `anatomy.external_seams[id=addon-sdk]`.

The literal requested `research/2026-08-03-ontology-authority-agent-context-presentation/findings.md`
was absent. Its accepted Inventory result was used as the current available
presentation result. The requested page path under `/visualization/` was also
absent; the current page is at the package root.

### Exact-Binding Information Architecture

#### 1. Beginner System Overview — What Am I Looking At?

- ResonantOS is the host system; Augmentor is its agent-facing consultation
  experience.
- Show six identities: ResonantOS, Augmentor, capabilities/add-ons, Add-on SDK,
  Agent API, and Living Archive.
- Display evidence posture: implemented, documented decision, planned, absent,
  or unverified.
- Define ontology as a map of meaning with receipts, not the authority that
  approves meaning.
- Teach one path: `source → Living Archive record → bounded context → Augmentor
  consultation → cited answer or abstention`.
- State that nothing shown authorizes work, promotion, publication, or effects.

#### 2. Explorable System Graph — How Do The Pieces Connect?

- Default to system-level nodes.
- Center Augmentor inside the ResonantOS environment.
- Show the Add-on SDK as existing; show the ontology-consultation SDK extension
  separately as planned unless owner evidence upgrades it.
- Show Living Archive as the source/memory owner, not Augmentor's internal DB.
- Show Agent API as an interface into consultation, not the ontology.
- Selecting a node/relation opens plain meaning, owner, status, can/cannot do,
  source selectors, and freshness/invalidation.
- Provide audience, owner-package, posture, and lifecycle filters.
- Provide paths for asking Augmentor, building an add-on, and tracing a source.
- Mirror every visual edge in a textual relation list.

#### 3. Augmentor Anatomy And Capabilities

Preserve the body metaphor while clarifying ownership:

- interface/conversation;
- source grounding;
- bounded context;
- candidate typed meaning;
- distinct route/work request, decision, dispatch, run, and join;
- evidence return separate from memory intake;
- optional advice-only reasoning;
- external approval/authority gates;
- ResonantOS capabilities and add-ons;
- Living Archive retrieval and separate intake proposal.

Each card follows: `What it is → Current state → Owner → Input/output → Evidence
→ Limitation → Related developer interface`.

#### 4. SDK And Agent API Developer Material

Keep sibling tracks:

- Add-on SDK: existing SDK purpose, runtime position, manifest/capabilities,
  request/response/validation/grants/degraded behavior, one minimal example,
  planned ontology-consultation extension, and effect boundary.
- Agent API: consultation purpose, request/focus, response statuses, source
  handles/limitations, one example, missing-host degradation, read-only limit.

#### 5. Evidence And Limitations

Show a filterable table with `Claim | Status | Owner source | Freshness | What
it proves | What it does not prove`. Required rows include the ResonantOS host,
Augmentor consultation, existing SDK, planned SDK extension, Living Archive
domains, host read/review/promotion routes, candidate page, and blocked
memory-agent implementation plan.

Global limits: documentation is not authority; candidate ontology is not
promoted; API success is not permission; intake is not trusted memory;
promotion does not transfer source ownership; passing local validation is not
release/deployment/production proof; missing current authority requires visible
limitation or abstention.

#### 6. Deep Technical Reference

Expose terminology/non-collapse, node/relation records, owner map,
source/provenance, status/lifecycle state machines, Living Archive concept
contract, Agent API status table, SDK contracts, invalidation, query/authority
direction, machine graph download, and source-selector ledger. Keep it collapsed
by default and link summaries through “View exact contract.”

### Living Archive Ontology Concept Contract

Name it `Source-Bound Ontology Concept Record`; do not create a new memory
system or persona.

It stores stable concept ID/scope, label/aliases, typed synopsis, kind, source
handles and revisions/hashes, provenance review artifact, separate evidence and
commitment confidence, lifecycle status, sensitivity/authority floor, typed
relation handles, contradictions, lifecycle receipt, and last source-resolution
state. It excludes copied claims inside pointer-only anchors, RecallContext as
evidence, hidden reasoning, secrets, every transcript turn, or duplicate truth
outside the LLM Wiki.

Index only concept identity/labels, project/domain, kind, source IDs/revisions,
relation endpoints, status, sensitivity/authority, freshness, reviewed wiki
handle, and synopsis search text. Do not select a production graph/vector/SQL
stack here.

Retrieval declares scope, sensitivity, budget, and authority floor; searches the
existing boundary; resolves current sources; filters unsafe records; preserves
contradictions; returns meaning, source handles, selection reason, status,
limitations, and receipt; and abstains when authority/current sources fail.

Invalidate or supersede on source revision/hash change, source disappearance,
owner/scope change, wiki supersession, unsafe contradiction, withdrawn
acceptance, policy expiry, or unresolved provenance. Changed sources create a
new candidate or stale state rather than silent rewrite.

The record never promotes itself and never treats retrieval, ranking, graph
display, documentation, consultation, intake, or add-on use as promotion. Any
routine promotion described by ADR-027 remains an externally governed verifier
or policy transition, not automatic promotion by the concept.

### Three User Journeys

1. **Newcomer understands the system:** sees the six identities, follows the
   ask-Augmentor path, opens one anatomy card, and can distinguish graph
   explanation from approval.
2. **Developer chooses the correct interface:** selects SDK or Agent API by
   intent, sees contract-level posture, tests/copies one example, and understands
   that the existing SDK does not prove the consultation extension.
3. **Maintainer traces and refreshes a concept:** inspects source revision and
   lifecycle state, observes staleness after a source change, opens the review
   route, and confirms no page/API/graph action promoted it.

### Accessibility And Progressive Disclosure

- Semantic landmarks, ordered headings, labeled navigation, real controls, and
  visible focus.
- Keyboard-reachable graph nodes/edges with identity and state in names.
- Synchronized text/table graph equivalent; no color/position/hover-only facts.
- Explicit status text, touch/focus/click parity, reduced motion, and no causal
  meaning dependent on animation.
- Mobile node/relation list and focused drawer rather than tiny SVG text.
- `aria-live` API state announcements and predictable focus return.
- Visible repository/document and source-selector descriptions.
- Every analogy names where it stops.
- Beginner-first disclosure; owners, schemas, digests, and selectors deeper.
- Planned/missing complexity behind a control while the evidence legend stays
  visible.

### Smallest MVP Content Set

One candidate-local documentation experience containing:

1. beginner overview and six-object identity strip;
2. shared graph dataset rendered as overview, anatomy, and technical list;
3. corrected SDK panel separating existing SDK and planned extension;
4. current Agent API console plus degraded state;
5. one Living Archive concept fixture for source, retrieval, invalidation,
   abstention, and separate promotion;
6. evidence/limitations table with exact selectors and freshness;
7. collapsed deep reference and machine-readable graph;
8. three acceptance walkthroughs;
9. desktop/mobile/keyboard/screen-reader/reduced-motion/missing-API/stale-source/
   consistency checks.

Not required: new memory store, selected runtime, vector or graph database, new
agent persona, automatic admission, live SDK extension, deployment, broad
personal memory, or privacy-policy selection.

Residue: the prior presentation findings path and requested visualization path
were stale; SDK status must be joined with Turing; the Living Archive package
owner remains unselected; the memory-agent plan remains blocked by stack and
SWU selection.

## Explorer Fong — Ontology Federation Lane

### Verdict

Select a federated, owner-preserving graph with one generated experience
projection.

The smallest coherent MVP is six logical source packages, each independently
versioned and digest-bound, plus one disposable cross-package projection. The
packages remain candidate-local; their composition has `authority_effect:
none`. The experience projection may explain/query the graph, but cannot become
source truth, transfer ownership, promote ontology meaning, grant SDK access,
or prove runtime behavior.

This corrects the monolith's weakness: `augmentor-unified-agent` mixes product
identity, host runtime, orchestration, evidence, ontology, and future reasoning
under `aug.*`, despite assigning those records to different owners. Evidence:
`nodes/nodes.json#/nodes`, `relations/relations.json#/relations`, and
`README.md:11-31`.

### Selected Package Split

| Package ID | Prefix | Owns | Does not own |
| --- | --- | --- | --- |
| `resonantos.system@0.1.0` | `ros.*` | shell, thread, host modules, runtime boundaries | Augmentor meaning, SDK syntax, source memory, authority |
| `augmentor.agent@0.1.0` | `aug.*` | interface identity, agent capabilities, context-facing presentation | thread persistence, route/grant decisions, source truth, effects |
| `resonantos.addon-sdk@0.1.0` | `sdk.*` | SDK vocabulary, manifest declaration, validation/review metadata, add-on identities | host grants, credentials, consultation answers, ontology bytes |
| `resonantos.agent-api@0.1.0` | `api.*` | versioned interfaces and host adapters, including consultation | SDK installation, consumer prose, ontology authority |
| `living-archive.knowledge@0.1.0` | `la.*` | provider-owned SourceRecord, recall/index ownership, intake/review state, source lineage | ontology promotion, automatic trusted writes, Augmentor reasoning |
| `augmentor.experience@0.1.0` | `exp.*` | view definitions and cross-package presentation edges only | canonical nodes, source bytes, runtime status, owner decisions |

Preserve current `aug.concept.*` and `aug.relation.*` as legacy aliases until an
explicit migration binds each to one new package ID. Same meaning retains ID;
changed ownership/meaning gets a new ID plus `supersedes`.

Recommended shapes:

- Node: `<package-prefix>.concept.<stable-slug>`
- Interface: `<package-prefix>.interface.<stable-slug>@<major>`
- Relation: `<declaring-package-prefix>.relation.<stable-slug>`
- View: `exp.view.<stable-slug>@<major>`
- Source handle: opaque `src-<12hex>` externally; internal binding includes
  owner, source, revision, and SHA-256
- Projection record: derived `rec-<12hex>`, never canonical identity

### Cross-Package Relation Contract

Admit only:

- `presents`
- `implements_interface`
- `declares_capability`
- `invokes`
- `projects_from`
- `references_source`
- `supports_candidate`
- `requests_review`
- `may_inform`
- negative guards `does_not_authorize`, `does_not_imply`, `does_not_deliver`

Every edge requires source/target package and endpoint IDs/versions, predicate,
owner route, evidence refs, runtime posture, `authorityEffect: none`, cycle
policy, and forbidden inferences. Do not allow cross-package `contains`, `owns`,
`is_a`, or `part_of` in the MVP because they imply ownership by proximity.

### Provenance And Status Model

Canonical nodes and edges carry:

```text
id, packageId, packageVersion, kind, label
ownerRef, ownerRoute
sourceBindings[{sourceHandle, sourceRef, revision, sha256, selector}]
evidenceConfidence, commitmentConfidence
semanticStatus, runtimeStatus, lifecycleStatus
freshness, observedAt, invalidatedAt?
claimCeiling, forbiddenInferences[]
supersedes[], conflictsWith[]
```

Keep independent axes:

- semantic: `candidate | reviewed_candidate | promoted | rejected | contested`
- runtime: `observed | designed | absent | blocked | deferred | unverified`
- lifecycle: `current | stale | superseded | retracted`

Consultation outcomes remain separate request states. Do not compress these into
one badge.

### Views And Query Boundaries

Generate:

1. `exp.view.system-overview@0.1.0`
2. `exp.view.augmentor-anatomy@0.1.0`
3. `exp.view.developer-seams@0.1.0`
4. `exp.view.knowledge-memory@0.1.0`
5. `exp.view.authority-boundary@0.1.0`
6. `exp.view.experience@0.1.0`

A view records its role, exact package/version/digest inputs, node/relation
allowlists, allowed readings, forbidden moves, owner route, and residue. It is
an interpretive view, not a namespace, lifecycle state, promotion route, or
source authority.

Queries may address exact IDs, search within selected views, traverse only
allowlisted predicates at bounded depth, and return source handles, freshness,
confidence, statuses, claim ceilings, and conflicts. They may not expose
private owner bindings, resolve opaque handles to private paths, infer
ownership/permission/promotion/runtime truth, combine incompatible contract
families, write memory/ontology, or convert relevance into a decision.

Contract families are exact-match: fixture `0.1.0`, live candidate `1.0.0`, and
rich candidate `1.1.0` are not implicitly compatible.

### Update And Invalidation Rules

1. Package owner changes canonical records and increments version.
2. Compiler verifies selectors and source hashes.
3. Changed input digest invalidates dependent edges, records, views, and cache.
4. Same ID/digest is idempotent; changed semantics conflict unless superseded.
5. Missing source, selector drift, incompatible major, unknown family, or stale
   projection fails closed.
6. Contradictions coexist as structured conflicts.
7. Projection manifest binds compiler, allowlist, package/source, schema, output
   digests, and generation time.
8. Owner approval and host installation remain downstream receipts.

Living Archive invalidation is source-led. Changed/retracted/unavailable bytes
stale derived indexes and projections. Intake requests review; it never mutates
trusted memory automatically.

### SDK And Agent API Boundary

Represent the existing Add-on SDK as an observed ResonantOS capability
environment and the ontology-consultation extension separately as planned.
Expose the existing read-only consultation owner through a proposed additive
SDK request contract and stateless host adapter. SDK validation is not review;
review is not grant; authentication is not policy; evidence is not answer or
authority.

Only `SWU-AOSDK-001`, the request-only declaration boundary, is selection-ready.
Host binding, projection approval, installation, consumer selection,
integration, and release remain not started or owner-blocked.

### Alternatives

- **Kill monolith:** it makes one namespace appear to own host runtime, memory,
  SDK, API, ontology, and authority.
- **Kill view-only composition:** it cannot provide stable cross-source IDs,
  compatibility, package-local invalidation, or ownership-enforced updates.
- **Select federation plus derived experience view:** minimum durable contract
  for ownership, exact versioning, invalidation, bounded queries, and learnable
  documentation without a second runtime or authority system.

### MVP Witness And Claim Ceiling

One fixture bundle binds exact versions/digests for six packages, renders the
system overview, expands Augmentor anatomy, shows the existing SDK as observed,
labels the consultation extension as planned/selection-ready only, opens one
Agent API explanation, and shows one Living Archive source flowing through
retrieval to bounded context and optional intake review. Changing the source
digest visibly stales knowledge and experience projections.

This is candidate information architecture. It does not implement packages,
migrate identifiers, promote meaning, approve neutral bytes, install an SDK
extension, publish documentation, deploy software, or establish production
readiness.

Residue: new package IDs and legacy-ID migration need ontology-owner review;
physical placement and maintainers remain owner decisions; projection approval
does not prove SDK installation; only `SWU-AOSDK-001` is selection-ready.
