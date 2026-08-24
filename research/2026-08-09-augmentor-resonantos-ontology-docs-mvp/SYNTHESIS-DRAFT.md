# Synthesis Draft — Augmentor, ResonantOS, Ontology, SDK, Agent API, And Living Archive Documentation MVP

## 1. Synthesis Decision

Select a federated, owner-preserving ontology model presented through one
generated, single-page documentation experience.

The page presents:

- ResonantOS as the host system.
- Augmentor as ResonantOS's agent-facing consultation experience.
- The existing Add-on SDK as part of the ResonantOS capability environment
  around Augmentor.
- The existing host-owned Agent API consultation route as a separate interface.
- A future ontology-consultation Add-on SDK extension as planned/absent, not as
  part of the already implemented SDK.
- Living Archive as the source-memory and review boundary, not as Augmentor's
  internal database.
- The documentation graph as a derived, candidate-local projection with
  `authority_effect: none`.

The selected model is logical federation first. It does not decide that six new
physical directories or repositories must be created. Package identity,
versioning, ownership, and invalidation boundaries are required in the model;
physical placement and maintainers remain owner decisions.

No implementation, package migration, promotion, installation, publication,
deployment, release, or production claim follows from this synthesis.

## 2. Reconciled Status Vocabulary

Every component and relation keeps three independent axes:

- Semantic: `candidate | reviewed_candidate | promoted | rejected | contested`
- Runtime: `observed | designed | absent | blocked | deferred | unverified`
- Lifecycle: `current | stale | superseded | retracted`

Beginner summaries may render these as implemented, documented decision,
planned, absent, or unverified. `Candidate`, `validated`, `installed`,
`promoted`, and `deployed` are never synonyms.

## 3. Component And Owner Graph

| Component | Logical owner | Current classification | Can do | Cannot be inferred |
| --- | --- | --- | --- | --- |
| ResonantOS Alpha runtime | ResonantOS host/runtime owners | Implemented and documented | Host extension UI, authenticated loopback bridge, module composition | Deployment or production readiness |
| Augmentor UI | ResonantOS extension-side Augmentor owner | Implemented and documented | Conversation, command routing, approvals, presentation | Source-memory ownership, ontology authority |
| Replaceable Augmentor Chat slot | ResonantOS add-on architecture owner | Documented decision; completeness unverified | Intended `primary-agent` and `chat-interface` replacement model | Completed migration or installed replacement |
| Add-on SDK V0 | `src/sdk/addons/` owner | Implemented and documented | Manifest contracts, capabilities, protocols, registry, surfaces, validation | Public marketplace availability, host grants, ontology consultation |
| Ontology-consultation SDK extension | Future SDK/host integration owner | Planned/absent; `SWU-AOSDK-001` selection-ready only | Proposed request declaration and adapter seam | Host binding, installation, release, working consultation through SDK |
| Augmentor consultation contract and engine | `browser-first/host/augmentor-consultation-*` owner | Implemented | Validate contracts; read-only search/context over installed neutral projection | Answer generation, ontology edits, memory writes, approval, routing authority |
| `POST /augmentor/consultation` | ResonantOS bridge/host owner | Implemented | Authenticated, capability-checked consultation invocation | Public deployment or SDK exposure |
| Agent-context adapter | Consultation host owner | Implemented | Organize retrieved evidence for answer composition | Generate prose or grant authority |
| Installed neutral projection | External user-state/operator boundary | Contract implemented; installed instance unverified | Supply approved projection data | Repository-bundled truth or current installation |
| Candidate ontology packages | Respective logical package owners | Candidate design | Preserve IDs, provenance, ownership, status, invalidation, bounded relations | Promoted ontology or physical package layout |
| Experience projection/page | `augmentor.experience` presentation owner | Candidate-local implementation/design | Explain/query graph views; call Agent API; show limitations | Canonical truth, runtime ownership, promotion, deployment |
| Living Archive source memory | Living Archive owner | Docs-first; domains/governance documented; runtime partly undecided | Own source records, recall/index, intake/review state, lineage | Automatic trusted writes or implemented ontology store |
| ADR-027 review/promotion boundary | Living Archive host/verifier/policy owners | Documented host baseline | Review intake and govern eligibility | Automatic promotion by Augmentor, page, ontology record, SDK, or retrieval |
| Source-Bound Ontology Concept Record | Living Archive candidate concept model | Planned candidate | Bind typed meaning to source, revision, provenance, freshness, review state | New memory platform, source transfer, self-promotion |

### Principal Edges

```text
Person
  -> Augmentor UI                                      implemented/documented
  -> candidate documentation experience               candidate-local

Augmentor UI
  -> ResonantOS authenticated bridge                   implemented

ResonantOS bridge
  -> POST /augmentor/consultation                      implemented
  -> authentication and capability enforcement        implemented
  -> installed neutral projection                     contract implemented;
                                                       instance unverified

Consultation service
  -> reviewed evidence and answer policy               implemented
  -> agent-context organization                        implemented
  -> generated answer                                  absent by design
  -> ontology/memory mutation or approval              absent by design

ResonantOS capability environment
  -> Add-on SDK V0                                     implemented/documented
  -> add-on tools and Augmentor skills                 implemented contract
  -> ontology-consultation SDK extension               planned/absent

Living Archive
  -> source records and source-led invalidation        documented/planned
  -> read/search surfaces                              current host surface
  -> intake review and governed promotion              ADR-027 host baseline
  -> automatic trusted write                           forbidden

Candidate experience projection
  -> six owner packages                                projects_from
  -> Agent API                                         invokes
  -> owner evidence                                    references_source
  -> promotion, permission, runtime truth              does_not_imply
```

## 4. Selected Modular Ontology Split

Use six logical source packages and one disposable compiled projection:

| Package | Prefix | Owns | Explicit exclusions |
| --- | --- | --- | --- |
| `resonantos.system@0.1.0` | `ros.*` | Shell, thread, host modules, runtime boundaries | Augmentor semantics, SDK syntax, source memory, authority |
| `augmentor.agent@0.1.0` | `aug.*` | Agent identity, interface semantics, capabilities, context-facing presentation | Thread persistence, grants, source truth, effects |
| `resonantos.addon-sdk@0.1.0` | `sdk.*` | Manifest/SDK vocabulary, declaration, validation metadata, add-on identity | Host grants, credentials, answers, ontology bytes |
| `resonantos.agent-api@0.1.0` | `api.*` | Versioned host interfaces and adapters, including consultation | SDK installation, consumer prose, ontology authority |
| `living-archive.knowledge@0.1.0` | `la.*` | Source records, recall/index ownership, intake/review state, source lineage | Ontology promotion, automatic trusted writes, Augmentor reasoning |
| `augmentor.experience@0.1.0` | `exp.*` | View definitions and cross-package presentation relations | Canonical nodes, source bytes, runtime status, owner decisions |

The compiler produces a digest-bound disposable projection. Logical federation
is not a filesystem mandate. The MVP may keep candidate files together if it
preserves package identity/version, record-level owners, source bindings,
digests, local invalidation, import allowlists, and no ownership transfer by
physical proximity.

Recommended IDs:

- Node: `<prefix>.concept.<stable-slug>`
- Interface: `<prefix>.interface.<stable-slug>@<major>`
- Relation: `<declaring-prefix>.relation.<stable-slug>`
- View: `exp.view.<stable-slug>@<major>`
- External source handle: `src-<12hex>`
- Derived projection record: `rec-<12hex>`

Existing `aug.concept.*` and `aug.relation.*` remain legacy aliases pending an
ontology-owner-approved migration. Preserve IDs only when meaning and ownership
remain the same; otherwise create a new ID plus `supersedes`.

Allowed cross-package predicates are `presents`, `implements_interface`,
`declares_capability`, `invokes`, `projects_from`, `references_source`,
`supports_candidate`, `requests_review`, `may_inform`, `does_not_authorize`,
`does_not_imply`, and `does_not_deliver`. Disallow cross-package `contains`,
`owns`, `is_a`, and `part_of` in the MVP.

Reject the unified monolith because it collapses owners. Reject view-only
composition because it lacks stable IDs, compatibility, owner-enforced updates,
and package-local invalidation. Select logical federation plus one generated
experience view.

## 5. Single-Page Documentation Architecture

Use:

`Orient → Explore → Inspect Augmentor → Build with interfaces → Verify evidence → Open deep reference`

### Beginner Overview

Show ResonantOS, Augmentor, capabilities/add-ons, Add-on SDK, Agent API, and
Living Archive. Teach:

`source → Living Archive record → bounded context → Augmentor consultation → cited answer or abstention`

State that ontology is a map of meaning with receipts, not self-approving
authority, and that retrieval/API/SDK/graph display authorizes no effects.

### Explorable Graph

Center Augmentor inside ResonantOS. Place the existing SDK around it as
capability infrastructure, not an organ. Keep the consultation SDK extension a
separate planned seam. Show Living Archive as external source-memory owner and
Agent API as the implemented host interface.

Each selected object shows:

`plain meaning → owner → status axes → can do → cannot do → source selectors → freshness/invalidation`

Provide audience/owner/posture/lifecycle/evidence filters and a synchronized
textual relation list.

### Augmentor Anatomy

Retain body/technical-map duality while separating interface, source grounding,
bounded context, typed meaning, route/work lifecycle, evidence return, memory
intake, advice-only reasoning, external gates, ResonantOS capabilities/add-ons,
and Living Archive retrieval/intake.

Cards follow:

`What it is → Current state → Owner → Input/output → Evidence → Limitation → Related developer interface`

### Developer Interfaces

Present sibling tracks:

- Add-on SDK: existing internal SDK, runtime position, manifests/capabilities/
  protocols/validation/degraded behavior, one example, separate planned
  consultation extension, no capability grant by validation.
- Agent API: implemented consultation, request/focus, response statuses, source
  handles/limitations, one example, disconnected behavior, read-only limit.

### Evidence And Limitations

Use:

`Claim | Semantic status | Runtime status | Lifecycle status | Owner source | Freshness | What it proves | What it does not prove`

Include host, Augmentor, API route/service, existing SDK, planned extension,
Living Archive domains/review routes, candidate page/packages, installed
projection state, and blocked memory-agent plan.

### Deep Reference

Collapse terminology, schemas, package/owner map, provenance, status axes,
Living Archive concept, Agent API status, SDK contracts, invalidation,
query/authority limits, ID migration, machine graph, and selector ledger.

The current HTML page is at
`projects/augmentor/ontology/unified-agent/ontology-visualization.html`; the
requested `/visualization/` page path is stale. Anatomy data remains at
`visualization/anatomy-map.json`. Keeping or relocating the page requires an
owner decision.

## 6. Living Archive Integration Contract

`Source-Bound Ontology Concept Record` extends the Source-Bound Recall Cycle; it
does not create a memory product/store/persona.

Fields include concept ID/scope, label/aliases, synopsis/kind, source handles
with revision/hash/selector, review provenance, separate evidence/commitment
confidence, three status axes, sensitivity/authority floor, typed relations,
conflicts, lifecycle receipt, last resolution, and supersession/retraction.

Retrieval declares scope, sensitivity, budget, and authority floor; resolves
current source identity; filters unsafe records; preserves conflicts; returns
meaning, handles, selection reason, freshness, limits, and receipt; and abstains
when sources or authority checks fail.

ADR-027 is the documented host baseline for ingest review and governed promotion
eligibility. The Source-Bound Recall Cycle is a passed definition/non-executed
plan. Living Archive remains docs-first about final runtime/artifact type. The
concept is a candidate integration contract over that boundary, not proof of an
implemented ontology store or broader memory-agent plan.

Invalidate/supersede when source revision/hash changes, source/selector fails,
owner/scope changes, reviewed content is superseded, a conflict becomes unsafe,
acceptance is withdrawn, policy expires, provenance fails, or contract/package
versions are incompatible. Never silently rewrite meaning. Missing authority
fails closed.

## 7. Agent API And SDK Interaction

```text
Documentation page or authorized consumer
  -> same-origin POST /augmentor/consultation
  -> bridge authentication
  -> augmentor-consultation-read capability
  -> contract validation
  -> installed neutral projection resolution
  -> read-only search/context
  -> evidence + answer policy + limitations
  -> agent-context adapter
  -> consumer composition or abstention
```

The page carries no consultation secret and degrades visibly when unavailable.

The SDK supplies declarations, protocols, manifests, registry/surface routing,
and validation. The consultation SDK extension is a proposed additive request
contract plus stateless adapter; only the request declaration unit is
selection-ready. Host binding, approval, installation, consumer integration,
release, and deployment remain unproven.

SDK validation is not review; review is not grant; authentication is not policy;
evidence is not answer; answer is not authority; API implementation is not SDK
implementation; approval is not installation; API success is not permission.

## 8. Literal MVP Witness

Use one local fixture bundle with exact package versions/digests:

1. load six logical packages;
2. show ResonantOS host and Augmentor agent;
3. expand anatomy;
4. show SDK V0 implemented;
5. show consultation SDK extension planned/absent;
6. submit one controlled read-only Agent API request;
7. resolve one Living Archive source with exact revision/hash/selector;
8. create one candidate Source-Bound Ontology Concept Record;
9. retrieve bounded context with reason, sources, freshness, limitations;
10. return cited result or abstention;
11. offer separate intake review;
12. change fixture source digest;
13. re-resolve;
14. stale dependent concept, relations, and view;
15. disclose staleness or abstain;
16. prove no page/graph/API/SDK/retrieval/intake step promoted the record.

This proves candidate information architecture, source-bound invalidation,
interface coherence, and degraded states only.

## 9. Source-Bound Acceptance Criteria

- Correct host/agent/SDK/API/Living Archive identities and owners.
- Existing SDK and planned consultation extension visibly separate.
- Agent API remains host-owned.
- Logical packages expose exclusions; physical placement remains undecided.
- Legacy IDs remain aliases pending owner migration.
- Every material record has source/selector, owner, freshness, statuses, claim
  ceiling, and forbidden inferences.
- Current root page path or explicit owner-approved relocation.
- Missing historical findings disclosed; Inventory substitute not impersonated.
- Installed projection remains unverified without operator evidence.
- Source change stales dependent records; source failure fails closed; conflicts
  stay visible; retrieval gives reasons/limitations; authority failure abstains.
- Intake and promotion remain separate.
- `/augmentor/consultation` and secret-free client preserved.
- Success, validation failure, disconnected host, redirect, and unexpected
  content states visible.
- API success never rendered as authority or release proof.
- Semantic landmarks, real controls, focus, keyboard graph, text equivalent,
  no color/hover/animation-only facts, touch parity, reduced motion, mobile
  list/drawer, live API announcements, predictable focus return, readable
  selectors/limitations.
- Relevant SDK, consultation, docs, browser-first, and browser walkthrough tests
  run against staged bytes; passing remains candidate-local proof.

## 10. Evidence Matrix

| Source | Selector | Lane | Scope | Proof status |
| --- | --- | --- | --- | --- |
| ResonantOS `AGENTS.md` | `#Alpha Runtime Boundary` | Turing | Alpha runtime | Implemented/documented |
| Architecture README | `:24-36`, `:79`, `:91`, `:112-120` | Turing | Runtime, SDK, architecture applicability | Documented |
| `MODULE_MAP.md` | `:7-32`, `:63-76` | Turing | Module graph, SDK position | Documented |
| `MODULE-OWNERSHIP.md` | `:20-21`, `:28`, `:39-46` | Turing | Augmentor, consultation, SDK ownership | Owner boundary |
| ADR-018 | `:15-22`, `:100-126`, `:218-250`, `:340-360` | Turing | SDK V0 and effects | Documented decision |
| SDK index/contracts/validation | cited lines in explorer return | Turing | Existing SDK exports/contracts/validation | Implemented |
| ADR-026 | `:17-21`, `:51-66`, `:164-191` | Turing | Replaceable Augmentor model | Documented; completeness unverified |
| Consultation contract/service/adapter/host | cited modules and lines | Turing | API and read-only evidence | Implemented |
| Bridge composition/enforcement | cited modules and lines | Turing | Auth and capability | Implemented |
| Anatomy map | `:2-15`, `:200-217` | Turing/Ahrens | Candidate anatomy and stale SDK seam | Candidate/stale |
| Root ontology page | cited lines | Turing/Ahrens | Page, accessibility, API binding, stale SDK prose | Candidate; deployment unverified |
| Living Archive README | `#Current State`, `#Working Rule` | Ahrens | Docs-first status | Current limitation |
| Memory-agent result/work pack | cited selectors | Ahrens | Recall Cycle and implementation blockers | Passed definition; blocked plan |
| ADR-013/014/027 | cited selectors | Ahrens | Domains, staleness, governed promotion | Documented decisions |
| Memory host/intake services | cited functions | Ahrens | Read/review/promotion separation | Implemented host surface |
| Ontology presentation research | cited headings | Ahrens | Teaching and authority separation | Research/Inventory substitute |
| Unified node/relation data and README | cited selectors | Fong | Mixed-owner monolith | Candidate evidence |
| `SWU-AOSDK-001` | request declaration | Fong | Consultation SDK extension | Selection-ready only |

## 11. Residue And Owner Gates

- Physical package placement and maintainers require owner decisions.
- Package IDs and legacy migration require ontology-owner review.
- Page keep-or-relocate remains open.
- Requested prior presentation findings are absent; Inventory is only a bounded
  substitute.
- Living Archive runtime, storage stack, and primary artifact remain undecided.
- Memory-agent implementation remains blocked.
- Replaceable Augmentor Chat completeness remains unverified.
- Installed projection, protected deployment, and live browser behavior remain
  unverified.
- Only `SWU-AOSDK-001` is selection-ready; later integration remains gated.
- Changed acceptance-bound bytes require new inventory, digests, validation,
  review, and owner acceptance.
