# Final Synthesis — Augmentor + ResonantOS Ontology Documentation MVP

## 1. Decision

Build one generated documentation experience over a federated, owner-preserving
knowledge graph.

The experience explains:

- ResonantOS as the host system;
- Augmentor as ResonantOS's agent-facing consultation experience;
- the implemented internal Add-on SDK as ResonantOS capability infrastructure;
- the implemented host-owned Agent API as Augmentor's read-only ontology
  consultation interface;
- the ontology-consultation SDK seam as planned/absent, adapting to the Agent
  API rather than creating a second API;
- the ResonantOS memory-provider broker and Living Archive host loop as existing
  owned precedents;
- the standalone Living Archive project and the new source-bound ontology record
  as separate scopes;
- the robot anatomy as an explanatory metaphor whose cores open source-bound
  technical records.

The graph is logically federated. This does not select six physical directories,
repositories, package IDs, versions, prefixes, maintainers, or migrations. Those
remain candidate proposals until their owners decide.

This research authorizes only a findings document and a later Refine proposal.
It grants no implementation, ontology admission, package migration, capability
grant, installation, publication, deployment, release, or production authority.

## 2. Current Evidence Boundary

| Surface | Evidence-backed state | Claim ceiling |
| --- | --- | --- |
| ResonantOS Alpha host and Augmentor UI | Implemented and documented code paths | Deployment, installation, release, and production use unverified |
| Replaceable `primary-agent`, `chat-interface`, and `memory-system` slots | Documented architecture; migration completeness unverified | No installed replacement inferred |
| Add-on SDK V0 | Implemented internal SDK | Not a public marketplace SDK; validation is not a grant |
| `POST /augmentor/consultation` contract, service, bridge, and agent-context adapter | Implemented host-owned, read-only interface | Does not write memory/ontology, generate final prose, approve work, or prove deployment |
| Focused `1.2.0` consultation contract | Implemented contract and host behavior | Requires a validated installed `1.2.0` bundle; installation is unverified |
| Installed neutral projection | Contract and installer implemented | Current operator installation unverified |
| Ontology-consultation SDK request seam | Planned/absent; first unit selection-ready only | No registry, grant, binding, installation, consumer, or release proof |
| Neutral memory-provider broker and `POST /memory/{operation}` | Documented ResonantOS owner precedent | Do not create a direct Living Archive-only generic memory API |
| ResonantOS Living Archive host loop | Implemented host baseline in ADR-027 | Deployment and a specific operator dataset remain unverified |
| Standalone Living Archive project | Docs-first; final runtime/artifact ownership remains open | Must not be conflated with the ResonantOS host implementation |
| Unified ontology and generated page | Candidate-local private read model and page | Not promoted, published, deployed, or authoritative |
| Robot core popover and API consultation UI | Candidate implementation with local tests | Live protected deployment and real installed-projection behavior unverified |
| Proposed modular ontology | Research candidate | Logical boundaries only; owner acceptance absent |

Use **implemented code path; deployment unverified** rather than “deployed” for
every repository implementation lacking an operator/deployment receipt.

## 3. Non-Collapse Model

| Kind | Identity | Must not become | Update owner |
| --- | --- | --- | --- |
| System | Host/runtime boundary and owned behavior | Agent, page, or graph | ResonantOS host owner |
| Agent | Actor/interface with bounded behavior | System, capability, or page | Augmentor owner |
| Capability | Declared permission/action vocabulary | Agent, grant, or enforcement result | Capability vocabulary owner |
| Capability grant | Principal + scope + expiry policy record | SDK declaration or API success | Host/policy owner |
| Add-on | Installable/registrable extension | SDK, capability, or agent | Add-on owner |
| SDK | Declaration, validation, protocol, and adapter vocabulary | Runtime, grant, API, or successful installation | SDK owner |
| API | Versioned host interface | SDK, agent, or authority decision | Host/API owner |
| Ontology owner package | Versioned semantic ownership boundary | Directory, compiled graph, or view | Package owner |
| Cross-package relation | Directed typed assertion with a declaring owner | Layout edge, ownership transfer, or reverse assertion | Declaring package owner |
| Experience projection | Digest-bound disposable read model | Canonical ontology, source truth, or runtime state | Regenerated from accepted owner records |
| Documentation page | Human-facing renderer and interaction surface | Ontology package, source record, or proof | Page owner |
| Source record | Revision-bound evidence pointer and provenance | Ontology concept, index entry, or authority decision | Source/Living Archive owner |
| Memory index | Rebuildable retrieval aid | Source bytes, semantic truth, or review state | Memory-provider owner |
| Authority decision | Actor-, scope-, digest-, policy-, and receipt-bound decision | Status label, API result, retrieval hit, or page action | Designated policy/verifier owner |

Capability declaration, host grant, and runtime enforcement must remain separately
queryable. API success proves bounded interface behavior only.

Status axes apply only where meaningful:

- semantic: `candidate | reviewed_candidate | promoted | rejected | contested | not_applicable`;
- runtime: `observed | designed | absent | blocked | deferred | unverified | not_applicable`;
- lifecycle: `current | stale | superseded | retracted | not_applicable`.

Every transition names `updated_by`, `update_basis`, and a receipt. A status word
alone is never an authority decision.

## 4. Proposed Logical Partitions

The following are **candidate logical partitions**, not accepted packages:

| Candidate partition | Responsibility | Explicit exclusion |
| --- | --- | --- |
| ResonantOS system | Shell, thread, host modules, runtime boundaries | Augmentor meaning, SDK syntax, source memory, authority |
| Augmentor agent | Agent identity, interface semantics, declared capabilities, bounded context presentation | Thread persistence, grants, source truth, effects |
| ResonantOS Add-on SDK | Manifest, capability/protocol declarations, validation, add-on identity, stateless host adapters | Host grants, credentials, answers, ontology bytes |
| ResonantOS Agent API | Versioned host consultation interface and adapters | SDK installation, answer prose, ontology authority |
| Living Archive knowledge | Source/version records, neutral broker adapter, retrieval index, intake/review state, lineage | Automatic trusted writes, Augmentor reasoning, ontology promotion by retrieval |
| Augmentor experience | View definitions, layout, annotations, and **derived presentation edges** carrying `derived_from` | Canonical nodes, semantic cross-package relations, source bytes, runtime truth, owner decisions |

Candidate identifiers such as `ros.*`, `aug.*`, `sdk.*`, `api.*`, `la.*`, and
`exp.*` are illustrative only. Existing IDs remain unchanged unless the ontology
owner later approves a migration. `alias` is legal only for the same referent,
meaning, and owner; otherwise use `supersedes` or `replaced_by`.

A semantic relation record requires:

`subject, predicate, object, declaring_package, source_handles, semantic_status,
runtime_status, lifecycle_status, direction, cardinality, valid_from,
invalidated_by, optional_inverse`

Reverse traversal is derived unless an inverse is explicitly declared. Drawing
an edge never creates a semantic relation.

## 5. Query And Update Direction

Read/query direction:

```text
page or authorized consumer
→ owner package or digest-bound projection
→ host-owned interface
→ authenticated capability enforcement
→ bounded records and source handles
→ answer policy and limitations
→ consumer composition or abstention
```

Source/update direction:

```text
owner source revision
→ source record version or invalidation
→ dependent candidate semantic records become stale
→ dependent relations become stale
→ compiled projection regenerates with a new digest
→ documentation refreshes
```

Forbidden reverse direction:

```text
page edit / graph drag / API success / retrieval hit / SDK validation
↛ source record mutation
↛ ontology promotion
↛ capability grant
↛ installation
↛ authority decision
```

The page may create a separately governed intake request. It may not directly
write a source record, memory index, ontology record, relation, grant, or
authority decision.

## 6. One Documentation Experience

Use the current owned target for the MVP:

`projects/augmentor/ontology/unified-agent/ontology-visualization.html`

Do not relocate it to `/visualization/` in the MVP. A later redirect or URL
contract requires an owner decision.

Information architecture:

`Orient → Explore system graph → Inspect Augmentor → Build with SDK/API → Trace memory/evidence → Verify limitations → Deep reference`

### Orient

Explain in one screen:

- ResonantOS is the host.
- Augmentor is its agent-facing experience.
- The SDK lets add-ons declare integration.
- The Agent API lets authorized agents consult reviewed ontology evidence.
- Living Archive owns source memory and review/promotion boundaries.
- The graph/page explains; it does not authorize.

### Explore The System Graph

Show owner records and directed relations for ResonantOS, Augmentor, Add-on SDK,
Agent API, memory-provider broker, ResonantOS Living Archive host surface,
standalone Living Archive, candidate ontology, and experience projection.

Every selected record exposes:

`plain meaning, kind, owner, relation owner, three statuses, what it can do,
what it cannot do, source handles/selectors, projection digest, freshness,
limitations`

Provide synchronized textual relations. A visual edge alone is not evidence.

### Inspect Augmentor Through The Robot

The robot is an explanatory metaphor, not a technical containment diagram.
Body shape, proximity, color, or animation must never imply ownership,
execution order, authority, installation, or runtime presence.

Each core keeps its current visible size even if the robot is reduced. Hover or
focus opens a short preview in the robot frame; click/tap pins one card in the
same frame. The old vertical anatomy-card interface is removed from the primary
experience. A synchronized textual list remains available as an accessible
technical equivalent, not as ten competing cards below the robot.

Each core card contains:

1. a plain heading without labels such as “plain language”;
2. one sentence answering “what is this?”;
3. current state in ordinary words;
4. what goes in and what comes out;
5. how it connects to ResonantOS, SDK, API, and Living Archive;
6. what it cannot do;
7. source/evidence links;
8. one **Consult this part** action when the implemented Agent API mapping is available.

Only the technical record, owner source, selector, statuses, and digest support
a technical claim. The robot gives recognition and orientation.

### Build With SDK And Agent API

Present sibling, non-collapsed tracks:

- **Add-on SDK V0 — implemented internal SDK:** manifests, capabilities,
  protocols, validation, registry/surfaces, degraded behavior, and one example.
- **Ontology consultation SDK seam — planned/absent:** a future manifest request
  plus stateless adapter to the existing Agent API. It may not create another
  query/result schema, route, projection loader, access registry, cache, or
  answer policy.
- **Agent API — implemented host interface:** exact query/focus contracts,
  response policy, source handles, limitations, disconnected states, and
  read-only boundary.

### Trace Memory And Evidence

Generic source-memory operations use the ResonantOS memory-provider broker and
`POST /memory/{operation}`. Living Archive-specific provenance/review behavior
stays behind its adapter. The consultation route consumes an installed neutral
projection; it must not silently become a second memory broker.

### Evidence And Deep Reference

For every claim show its source, stable selector, observed time or revision,
proof status, and forbidden inference. Include the graph schema, candidate
partition map, API/SDK contracts, status rules, invalidation rules, textual
relations, and selector ledger.

## 7. Agent API Core Consultation Contract

A core consultation uses the implemented focused contract. Proposed fixed MVP
request for the `work-spine` core:

```json
{
  "schemaVersion": "augmentor.consultation.query@1.2.0",
  "requestId": "docs-mvp-work-spine-1",
  "questionId": "what-does-work-spine-do",
  "operation": "search",
  "query": {"text": "What does the work spine do?"},
  "scope": {"viewIds": ["experience", "runtime"]},
  "explanation": {"profile": "guided"},
  "focus": {"kind": "anatomy-region", "id": "work-spine"},
  "limits": {
    "maxCandidates": 100,
    "maxRecords": 10,
    "maxSources": 20,
    "maxBytes": 32768,
    "maxTokens": 4096,
    "maxMillis": 1000
  }
}
```

The page reads `answerPolicy` first and renders only validated public fields.
It never stores a secret. The local host owns authentication and grants. When
the API or validated `1.2.0` map is unavailable, the static source-bound card
remains usable and the action reports a concise unavailable/abstain state; it
does not fall back to invented evidence or a legacy focus path.

## 8. Living Archive Contract

Keep three scopes separate:

1. **ResonantOS Living Archive host surface:** implemented source/version
   ledgers, queue, review artifacts, verifier approval, promotion, indexes,
   navigation/log refresh, lint, semantic repair queueing, and neutral broker
   adapter; deployment remains unverified.
2. **Standalone Living Archive project:** docs-first project whose final runtime
   and primary artifact remain owner-blocked.
3. **Source-Bound Ontology Concept Record:** net-new candidate pointer record,
   not another store, wiki, index, or promotion ledger.

The concept record stores only stable external source/version handles,
selectors, digests, typed candidate meaning, dependency links, and external
review-receipt references. Living Archive remains owner of source bytes,
indexes, review state, and promotion. Cached display fields are derived and
digest-invalidated.

An authority decision is a separate first-class record with:

`decision_id, actor_role, candidate_digest, scope, decision, policy_basis,
decided_at, expiry_or_withdrawal, receipt_ref`

Retrieval or API success never creates that record.

## 9. Finite MVP Fixture And Acceptance Manifest

The Refine MVP should create exactly three new fixture artifacts, names still
candidate until the later plan is accepted:

- `visualization/fixtures/docs-mvp.bundle.json`
- `visualization/fixtures/docs-mvp.changed.json`
- `visualization/fixtures/docs-mvp.acceptance.json`

The bundle contains the minimum closed graph for the system overview, the
`work-spine` core, Add-on SDK, planned SDK seam, Agent API, memory broker,
ResonantOS Living Archive host, standalone Living Archive boundary, source
pointer, authority-decision kind, and derived experience view.

Literal source variants:

| Variant | Exact UTF-8 bytes | SHA-256 |
| --- | --- | --- |
| V1 | `Augmentor consultation is read-only evidence retrieval.` | `eaf2f59b00bef988d0c8ded919605f6b7455364d69ddd6d290b2fd3c7b062c2b` |
| V2 | `Augmentor consultation is read-only evidence retrieval through a host-owned API.` | `0c16325d45600f9660cfd14225cdd9d1267be8c45e7369e558ddc759f0ae2271` |

Required fixture observations:

1. load the closed candidate graph and verify unique IDs, allowed imports,
   directed relations, declaring owners, and no dangling references;
2. render the ResonantOS overview and Augmentor robot from the same projection;
3. hover/focus `work-spine` to open one in-frame preview;
4. click/tap to pin the same card and return focus predictably on close;
5. label Add-on SDK V0 “implemented internal SDK”;
6. label the consultation SDK seam “planned/absent” and expose no executable
   control for that seam;
7. submit the exact focused Agent API request above through an intercepted local
   contract test or an authorized installed projection;
8. verify a schema-valid result exposes `resolvedFocus`, allowed views, mapping
   version/digest, evidence, source handles, answer policy, and limitations;
9. display the pointer-only candidate concept without duplicating source bytes,
   review state, index truth, or promotion state;
10. replace V1 with V2, regenerate, and assert the source pointer, dependent
    concept, semantic relations, and experience projection become stale or are
    rebuilt under a new digest;
11. assert the authority-decision fixture/count is byte-identical before and
    after hover, pin, query, API success, retrieval, and intake-request UI;
12. remove or deny the API/map and assert the static card remains, the live
    action reports unavailable/abstain, no raw error body appears, and no legacy
    focus fallback occurs;
13. repeat at desktop and mobile viewport, keyboard-only, touch, and reduced
    motion with a synchronized textual graph.

Existing exact validation surfaces:

```bash
node projects/augmentor/ontology/unified-agent/scripts/build-visualization.mjs --check
node projects/augmentor/ontology/unified-agent/scripts/validate.mjs
node --test projects/augmentor/ontology/unified-agent/tests/visualization.test.mjs
node projects/augmentor/ontology/unified-agent/tests/agent-api.browser.mjs "$(npm root -g)/playwright"
node projects/augmentor/ontology/unified-agent/tests/robot-consultation.browser.mjs "$(npm root -g)/playwright"
node projects/augmentor/ontology/unified-agent/tests/visualization.browser.mjs "$(npm root -g)/playwright"
```

The later Refine plan must add a deterministic fixture/graph acceptance test for
items 1, 9, 10, and 11. Its exact path and command are planned work, not an
existing validation claim. All checks must run against staged bytes; loopback
and Chromium capability are environmental prerequisites, not product repairs.

## 10. Reviewer Dispositions

| Review | Material challenge | Disposition |
| --- | --- | --- |
| Lakatos | Six packages looked settled | Repaired: candidate logical partitions; all IDs/versions/prefixes/maintainers/migration owner-blocked |
| Lakatos | SDK seam risked duplicating Agent API | Repaired: manifest request + stateless adapter only; second protocol explicitly forbidden |
| Lakatos | Neutral memory broker omitted | Repaired: generic memory operations route through owned broker |
| Lakatos | Living Archive scopes conflated | Repaired: host implementation, standalone project, and candidate concept split |
| Lakatos | Concept could duplicate source/review store | Repaired: pointer-only record and digest-bound display cache |
| Lakatos | Private candidate could appear host/public-owned | Repaired: neutral allowlisted projection only; partitions remain candidate-local until owner acceptance |
| Gödel | Witness was intentions, not replayable | Repaired at research-plan level with three proposed fixtures, literal bytes/digests, exact API request, observations, and existing commands; implementation remains future Refine work |
| Gödel | Real Living Archive store was unselected | Killed: MVP uses fixture-local pointer record and owned host precedents only |
| Gödel | SDK separation and unavailable state were prose-only | Repaired with exact rendered labels, non-executable planned seam, and deterministic unavailable behavior |
| Gödel | Page target open | Repaired for MVP: keep current root page; relocation excluded |
| Quine | Experience risked owning semantic truth | Repaired: experience owns derived presentation edges only |
| Quine | Capability/grant/enforcement collapsed | Repaired with separate record kinds and query requirements |
| Quine | Relation identity/update direction incomplete | Repaired with required fields and one-way invalidation flow |
| Quine | Source record/index/authority decision collapsed | Repaired with three distinct identities and owners |
| Quine | Robot metaphor could imply proof | Repaired: visual explains; technical graph + source selector + status + digest proves |

## 11. Killed, Deferred, And Required Close

Killed for this MVP:

- Augmentor as ResonantOS itself;
- agent as capability;
- add-on as SDK;
- SDK as API;
- API success as authority;
- direct generic Living Archive API that bypasses the memory-provider broker;
- a second consultation protocol;
- Living Archive as Augmentor's private database;
- source record as ontology concept;
- memory index as source truth;
- view edge as semantic relation;
- documentation page or graph as ontology truth;
- working consultation through the planned SDK seam;
- real standalone Living Archive ontology storage;
- six physical packages inferred from six logical partitions;
- page relocation during the MVP;
- deployment, release, production, or current installed-projection claims.

Deferred to owners:

- accepted package identities, prefixes, versions, maintainers, and predicate
  registries;
- physical placement and legacy-ID migration;
- cross-package cardinalities and declared inverses;
- authority-decision package ownership;
- whether a future product composition invokes both consultation and the memory
  broker;
- standalone Living Archive runtime/artifact choices;
- protected deployment and current projection installation.

Required close:

The sources support one user-ready documentation direction: a current-root
Augmentor page that explains the ResonantOS host, uses the robot cores as
accessible source-bound entry points, exposes the implemented Agent API without
duplicating it in the SDK, distinguishes the implemented SDK from its planned
consultation seam, and traces source memory through owned broker/Living Archive
boundaries. The ontology remains a candidate federated model and the page a
generated read experience. Neither one grants authority or proves deployment.

## 12. Source Selector Ledger

- ResonantOS SDK: `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-018-addon-sdk-v0.md:15-26,100-126,218-250,340-360`
- Consultation API usage/safety: `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/reference/AUGMENTOR_CONSULTATION_API.md#Send-A-Request`, `#Ask-About-One-Robot-Region`, `#Safety-Boundary`
- Consultation versions/closed query: `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/browser-first/host/augmentor-consultation-contract.mjs:1-18,146-193`
- Neutral memory-provider broker: `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-026-minimal-kernel-replaceable-default-addons.md:47-113,172-193`
- ResonantOS Living Archive implementation: `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-027-living-archive-llm-wiki-compliance.md:45-68,88-146`
- Standalone Living Archive boundary: `/home/vrondelli/projects/living-archive/README.md:3-7,15-25`
- Unified ontology owner boundary/page/validation: `projects/augmentor/ontology/unified-agent/README.md:11-33,62-71,136-145`
- Anatomy records: `projects/augmentor/ontology/unified-agent/visualization/anatomy-map.json:2-15,29,47-50,97-109,122-135,200-215`
- Existing robot/API tests: `projects/augmentor/ontology/unified-agent/tests/agent-api.browser.mjs`, `projects/augmentor/ontology/unified-agent/tests/robot-consultation.browser.mjs`, `projects/augmentor/ontology/unified-agent/tests/visualization.test.mjs`, `projects/augmentor/ontology/unified-agent/tests/visualization.browser.mjs`
- SDK consultation plan ceiling: `projects/augmentor/ontology/unified-agent/development/invoke-runs/20260806T183814Z-addon-sdk-ontology-api/WORK-PACK.md:87-126,149-152`
- Research inputs/reviewer challenges: `research/2026-08-09-augmentor-resonantos-ontology-docs-mvp/research.md`, `REVIEW-LAKATOS.md`, `REVIEW-GODEL.md`, `REVIEW-QUINE.md`
