# Findings — Augmentor + ResonantOS Ontology Documentation MVP

## Practical product thesis

Build one generated documentation experience over a federated, owner-preserving
knowledge graph. Keep the current root page as the MVP target, let the Augmentor
robot provide the recognizable entry point, and make every technical claim resolve
to a typed record, its owner, status, digest, source handle, and stable selector.
The page should explain the system without becoming the system's ontology,
authority surface, memory store, or runtime proof. This direction is supported by
the candidate page and owner boundary already present locally
(`projects/augmentor/ontology/unified-agent/README.md:11-33,62-71,136-145`) and by
the implemented host contracts described below.

The key product choice is federation without collapse: ResonantOS remains the host;
Augmentor remains an agent-facing consultation experience; the Add-on SDK declares
integration; the Agent API performs authorized read-only consultation; the neutral
memory broker owns generic memory operations; Living Archive owns source/version,
index, review, and promotion behavior; and the documentation projection remains a
disposable read model. The reviewed research correction explicitly forbids treating
six useful logical partitions as six accepted physical packages
(`EVIDENCE-CLOSURE.json:resolution_rows[AOD-001]`).

## Verdict matrix

| Question | Verdict | Evidence boundary |
| --- | --- | --- |
| Is one integrated documentation experience warranted? | **Yes, as the selected product direction.** | Current candidate page and validation surface: `projects/augmentor/ontology/unified-agent/README.md:62-71,136-145`; source-bound owner boundary: `README.md:11-33`. |
| Is ResonantOS the same thing as Augmentor? | **No.** ResonantOS is the host; Augmentor is a bounded agent/interface. | Reviewed non-collapse correction: `SYNTHESIS-FINAL.md#Non-Collapse-Model`; `EVIDENCE-CLOSURE.json:resolution_rows[AOD-008]`. |
| Is the Add-on SDK implemented? | **Yes, as an internal SDK code path; deployment/public-marketplace use is not proven.** | `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-018-addon-sdk-v0.md:15-26,100-126,218-250,340-360`. |
| Is the Agent API implemented? | **Yes, as a host-owned read-only interface; installation and deployment remain unverified.** | `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/browser-first/host/augmentor-consultation-contract.mjs:1-18,146-193`; `AUGMENTOR_CONSULTATION_API.md#Send-A-Request,#Ask-About-One-Robot-Region,#Safety-Boundary`. |
| Does the SDK currently provide ontology consultation? | **No. Planned/absent.** Only its first request unit is selection-ready. | `projects/augmentor/ontology/unified-agent/development/invoke-runs/20260806T183814Z-addon-sdk-ontology-api/WORK-PACK.md:87-126,149-152`. |
| Should that SDK seam define a second protocol? | **No; killed.** It may declare a request and use a stateless adapter to the Agent API only. | `EVIDENCE-CLOSURE.json:resolution_rows[AOD-002]`. |
| Should generic memory calls go directly to Living Archive? | **No.** Use the neutral `POST /memory/{operation}` broker; keep Living Archive-specific behavior behind its adapter. | `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-026-minimal-kernel-replaceable-default-addons.md:47-113,172-193`. |
| Is the ResonantOS Living Archive surface implemented? | **Implemented host baseline; deployment and operator data unverified.** | `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-027-living-archive-llm-wiki-compliance.md:45-68,88-146`. |
| Is standalone Living Archive an implemented ontology store? | **No.** It is a separate docs-first project with runtime/artifact ownership still open. | `/home/vrondelli/projects/living-archive/README.md:3-7,15-25`. |
| Are the proposed ontology partitions accepted packages? | **No.** They are reviewed logical boundaries only. | `EVIDENCE-CLOSURE.json:resolution_rows[AOD-001]`. |
| Is the finite MVP implemented and passing? | **No.** Its fixture and acceptance contract are specified for later Refine work. | `SYNTHESIS-FINAL.md#Finite-MVP-Fixture-And-Acceptance-Manifest`; `EVIDENCE-CLOSURE.json:resolution_rows[AOD-006]`. |

## As-built versus planned

| Surface | As-built evidence | Planned or unresolved residue |
| --- | --- | --- |
| ResonantOS host and Augmentor UI | Implemented/documented code paths (`/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/MODULE_MAP.md:7-32,63-76`; `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/MODULE-OWNERSHIP.md:20-21,28-29,39-46`). | Operator installation, deployment, release, and production use are unverified. |
| Replaceable host slots | `primary-agent`, `chat-interface`, and `memory-system` are documented architectural slots (`/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-026-minimal-kernel-replaceable-default-addons.md:47-113`). | Migration completeness and installed replacements are unverified. |
| Add-on SDK V0 | Internal manifest, capability/protocol, validation, registry/surface, and degraded-behavior infrastructure (`/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-018-addon-sdk-v0.md:15-26,100-126,218-250,340-360`). | It is not thereby public, installed, granted, or an answer engine. |
| Agent API | Host-owned query/focus contract, service/bridge behavior, and read-only safety boundary (`/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/browser-first/host/augmentor-consultation-contract.mjs:1-18,146-193`; `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/reference/AUGMENTOR_CONSULTATION_API.md#Safety-Boundary`). | A protected live deployment and currently installed validated `1.2.0` projection are unverified. |
| SDK consultation seam | No implemented seam. | First unit is selection-ready; later work may add a request declaration and stateless adapter only (`projects/augmentor/ontology/unified-agent/development/invoke-runs/20260806T183814Z-addon-sdk-ontology-api/WORK-PACK.md:87-126,149-152`). |
| Memory broker | Neutral provider routing and `POST /memory/{operation}` are documented owner precedent (`/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-026-minimal-kernel-replaceable-default-addons.md:47-113,172-193`). | Consultation-plus-memory composition is an owner decision. |
| Living Archive | ResonantOS host loop has implemented baseline behavior (`/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-027-living-archive-llm-wiki-compliance.md:45-68,88-146`). | Standalone Living Archive runtime and primary artifact remain open (`/home/vrondelli/projects/living-archive/README.md:3-7,15-25`). |
| Unified ontology/page/robot | Candidate-local read model, current root generated page, anatomy records, and local test surfaces exist (`README.md:11-33,62-71,136-145`; `anatomy-map.json:2-15,29,47-50,97-109,122-135,200-215`; named robot/API/browser tests in the selector ledger). | Promotion, publication, deployment, owner acceptance, and the broader user-ready composition are unproven. |

## Selected ontology partition shape

The recommended ontology shape has six **logical** partitions:

| Candidate partition | Owns | Must not own |
| --- | --- | --- |
| ResonantOS system | Shell, thread, host modules, runtime boundaries | Augmentor meaning, SDK syntax, source memory, authority |
| Augmentor agent | Agent identity, interface semantics, declared capabilities, bounded context presentation | Thread persistence, grants, source truth, effects |
| ResonantOS Add-on SDK | Manifest, protocol/capability declarations, validation, add-on identity, stateless host adapters | Grants, credentials, answers, ontology bytes |
| ResonantOS Agent API | Versioned host consultation interface and adapters | SDK installation, answer prose, ontology authority |
| Living Archive knowledge | Source/version records, broker adapter, retrieval index, intake/review state, lineage | Augmentor reasoning, automatic trusted writes, ontology promotion by retrieval |
| Augmentor experience | Views, layout, annotations, derived presentation edges with `derived_from` | Canonical nodes, semantic relations, source bytes, runtime truth, owner decisions |

This split is grounded in the candidate owner boundary and anatomy records
(`README.md:11-33`; `anatomy-map.json:29,47-50,97-109,122-135`) and in the
reviewed ownership repair (`EVIDENCE-CLOSURE.json:resolution_rows[AOD-001,AOD-007]`).
Identifiers such as `ros.*`, `aug.*`, `sdk.*`, `api.*`, `la.*`, and `exp.*` are
illustrative. Package IDs, prefixes, versions, maintainers, physical placement,
predicate registries, cardinalities, inverses, and legacy-ID migration remain owner
decisions.

Every semantic cross-package relation should carry `subject`, `predicate`, `object`,
`declaring_package`, `source_handles`, semantic/runtime/lifecycle statuses,
`direction`, `cardinality`, `valid_from`, `invalidated_by`, and optional inverse.
Reverse traversal is derived unless explicitly declared. Experience geometry and
view edges are presentation records, not semantic assertions
(`SYNTHESIS-FINAL.md#Non-Collapse-Model`; `EVIDENCE-CLOSURE.json:resolution_rows[AOD-007,AOD-008]`).

## Cross-package graph

```text
ResonantOS host
├─ hosts → Augmentor agent experience
├─ owns → Add-on SDK V0
├─ owns → Agent API (/augmentor/consultation)
└─ routes generic memory → memory-provider broker
                              └─ adapts → ResonantOS Living Archive host surface

Augmentor agent
├─ consults through → Agent API
├─ may later request through → SDK declaration + stateless adapter
└─ is explained by → Augmentor experience projection

Living Archive knowledge
├─ owns → source bytes, versions, indexes, review state, promotion
└─ exposes handles to → pointer-only source-bound concept record
                         └─ supports candidate semantic records
                              └─ compiles into digest-bound experience projection

Standalone Living Archive ── separate scope; no runtime equivalence inferred
Authority decision ── separate record; never produced by API/retrieval/page action
```

The query direction is consumer/page → owner record or digest-bound projection →
host interface → authenticated capability enforcement → bounded records/source
handles → answer policy and limitations → composition or abstention. The update
direction is source revision → source-record version/invalidation → stale dependent
concepts and relations → regenerated projection digest → refreshed documentation.
Page edits, graph drags, retrieval hits, API success, and SDK validation do not flow
backward into source mutation, ontology promotion, grants, installation, or authority
(`SYNTHESIS-FINAL.md#Query-And-Update-Direction`).

## One-page documentation information architecture

Use the existing root target
`projects/augmentor/ontology/unified-agent/ontology-visualization.html`; relocation
has no owner evidence and is excluded from this MVP (`README.md:62-71`;
`EVIDENCE-CLOSURE.json:resolution_rows[AOD-010]`). The page sequence is:

1. **Orient.** State the host/agent/SDK/API/Living Archive distinctions and the
   page's non-authoritative boundary.
2. **Explore system graph.** Show typed owner records and directed, owner-declared
   relations. A synchronized text graph is required because visual edges alone are
   not evidence.
3. **Inspect Augmentor.** Use the robot cores to open source-bound technical cards.
4. **Build with SDK/API.** Put the implemented internal SDK, planned/absent SDK
   consultation seam, and implemented Agent API in sibling tracks.
5. **Trace memory/evidence.** Route generic operations through the broker and show
   Living Archive provenance/review ownership.
6. **Verify limitations.** Expose statuses, digest/freshness, answer policy,
   unavailable behavior, and forbidden inference.
7. **Deep reference.** Include schema, partition map, API/SDK contracts, status and
   invalidation rules, textual relations, and selector ledger.

Every selected record exposes plain meaning, kind, owner, relation owner, applicable
semantic/runtime/lifecycle statuses, permitted and prohibited behavior, source
handles/selectors, projection digest, freshness, and limitations
(`SYNTHESIS-FINAL.md#One-Documentation-Experience`).

## Robot core and popover experience

The robot is recognition and navigation, never technical proof. Keep each core's
visible size when the robot is reduced. Hover or keyboard focus opens a short preview
inside the robot frame; click or tap pins exactly one card there; closing returns
focus predictably. Replace the old primary stack of anatomy cards with this single
in-frame card, while retaining a synchronized accessible text list. Existing
candidate interaction is evidenced by
`projects/augmentor/ontology/unified-agent/tests/robot-consultation.browser.mjs:190-240,255-326`;
the broader composition remains planned (`EVIDENCE-CLOSURE.json:resolution_rows[AOD-009]`).

Each core card needs a plain heading, a one-sentence identity, ordinary-language
current state, inputs/outputs, connections to ResonantOS/SDK/API/Living Archive,
explicit limitations, source/evidence links, and one **Consult this part** action
only where an implemented Agent API mapping exists. Shape, proximity, color, and
animation must not imply ownership, runtime presence, execution order, installation,
or authority. Only the typed technical record, owner source, selector, statuses,
and digest support the claim (`SYNTHESIS-FINAL.md#Inspect-Augmentor-Through-The-Robot`).

## Agent API versus SDK behavior

The Agent API is the implemented host-owned interface. For the MVP's `work-spine`
core, the proposed focused request is:

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
  "limits": {"maxCandidates": 100, "maxRecords": 10, "maxSources": 20,
    "maxBytes": 32768, "maxTokens": 4096, "maxMillis": 1000}
}
```

This request is fixed by `SYNTHESIS-FINAL.md#Agent-API-Core-Consultation-Contract`
against the implemented focused contract
(`augmentor-consultation-contract.mjs:1-18,146-193`). The page reads
`answerPolicy` first and renders validated public fields only. It stores no secret;
the local host owns authentication and grants. If the API or validated `1.2.0` map
is unavailable, the static source-bound card remains usable and the action reports
unavailable/abstain without raw errors, invented evidence, or legacy focus fallback
(`AUGMENTOR_CONSULTATION_API.md#Safety-Boundary`).

The SDK is a different owner surface. Add-on SDK V0 is implemented internal
infrastructure, but its ontology-consultation seam is planned/absent. Later work may
add only a manifest request and stateless adapter to the Agent API. It must not add a
second query/result schema, route, loader, access registry, cache, or answer policy
(`WORK-PACK.md:87-126,149-152`; `EVIDENCE-CLOSURE.json:resolution_rows[AOD-002]`).
SDK declaration is not a grant, API success is not authority, and runtime enforcement
must remain separately queryable.

## Living Archive, broker, and source-bound ontology contract

Keep three records distinct:

1. The ResonantOS Living Archive host surface owns its implemented source/version
   ledgers, queue, review artifacts, verifier approval, promotion, indexes,
   navigation/log refresh, lint, repair queueing, and broker adapter
   (`ADR-027:45-68,88-146`). Deployment is unverified.
2. The standalone Living Archive project is docs-first and separately owned; its
   final runtime and primary artifact are unresolved
   (`living-archive/README.md:3-7,15-25`).
3. The proposed Source-Bound Ontology Concept Record is pointer-only: stable external
   source/version handles, selectors, digests, typed candidate meaning, dependency
   links, and external review-receipt references. It is not a store, wiki, index, or
   promotion ledger (`EVIDENCE-CLOSURE.json:resolution_rows[AOD-004,AOD-005]`).

Generic `search/read/intake/review` operations use `POST /memory/{operation}` through
the ResonantOS broker (`ADR-026:47-113,172-193`). Living Archive-specific provenance
and review stay behind its adapter. Cached display fields are derived and invalidated
by digest changes. A distinct authority-decision record carries `decision_id`,
`actor_role`, `candidate_digest`, `scope`, `decision`, `policy_basis`, `decided_at`,
`expiry_or_withdrawal`, and `receipt_ref`; retrieval or API success never creates it
(`SYNTHESIS-FINAL.md#Living-Archive-Contract`).

## Exact finite MVP witness — proposed, not implemented

Later Refine work should create exactly these three candidate fixture artifacts:

- `visualization/fixtures/docs-mvp.bundle.json`
- `visualization/fixtures/docs-mvp.changed.json`
- `visualization/fixtures/docs-mvp.acceptance.json`

The closed bundle covers the ResonantOS overview, `work-spine`, Add-on SDK, planned
SDK seam, Agent API, memory broker, ResonantOS Living Archive host, standalone Living
Archive boundary, source pointer, authority-decision kind, and derived experience
view (`SYNTHESIS-FINAL.md#Finite-MVP-Fixture-And-Acceptance-Manifest`).

The exact source revisions are:

| Variant | Literal UTF-8 bytes | SHA-256 |
| --- | --- | --- |
| V1 | `Augmentor consultation is read-only evidence retrieval.` | `eaf2f59b00bef988d0c8ded919605f6b7455364d69ddd6d290b2fd3c7b062c2b` |
| V2 | `Augmentor consultation is read-only evidence retrieval through a host-owned API.` | `0c16325d45600f9660cfd14225cdd9d1267be8c45e7369e558ddc759f0ae2271` |

### Acceptance criteria

The later implementation must demonstrate all thirteen observations specified in
`SYNTHESIS-FINAL.md#Finite-MVP-Fixture-And-Acceptance-Manifest`:

1. The closed graph has unique IDs, allowed imports, directed relations, declaring
   owners, and no dangling references.
2. The ResonantOS overview and Augmentor robot render from the same projection.
3. Hover/focus on `work-spine` opens one in-frame preview.
4. Click/tap pins that card and close restores focus predictably.
5. Add-on SDK V0 is labeled **implemented internal SDK**.
6. The consultation SDK seam is labeled **planned/absent** and has no executable
   control.
7. The exact focused request above runs through an intercepted local contract test
   or an authorized installed projection.
8. A schema-valid result exposes `resolvedFocus`, allowed views, mapping version and
   digest, evidence, source handles, answer policy, and limitations.
9. The pointer-only concept duplicates no source bytes, review state, index truth,
   or promotion state.
10. Replacing V1 with V2 makes the pointer, dependent concept, semantic relations,
    and projection stale or rebuilds them under a new digest.
11. Authority-decision fixture/count bytes remain identical across hover, pin,
    query, API success, retrieval, and intake-request UI actions.
12. Removing/denying the API or map preserves the static card, reports
    unavailable/abstain, exposes no raw error, and performs no legacy fallback.
13. The experience passes desktop/mobile, keyboard-only, touch, reduced-motion, and
    synchronized-text-graph checks.

Existing validation commands are only existing surfaces, not proof of the proposed
fixture:

```bash
node projects/augmentor/ontology/unified-agent/scripts/build-visualization.mjs --check
node projects/augmentor/ontology/unified-agent/scripts/validate.mjs
node --test projects/augmentor/ontology/unified-agent/tests/visualization.test.mjs
node projects/augmentor/ontology/unified-agent/tests/agent-api.browser.mjs "$(npm root -g)/playwright"
node projects/augmentor/ontology/unified-agent/tests/robot-consultation.browser.mjs "$(npm root -g)/playwright"
node projects/augmentor/ontology/unified-agent/tests/visualization.browser.mjs "$(npm root -g)/playwright"
```

Refine must add a deterministic fixture/graph acceptance test for criteria 1, 9, 10,
and 11, and all acceptance-critical checks must exercise staged bytes. The new test
path and command do not yet exist. Therefore **`implementation_ready=false`** and no
fixture pass, user-ready composition, or SDK consultation behavior is claimed
(`EVIDENCE-CLOSURE.json:resolution_rows[AOD-006],writer_admission`).

## Staged next-owner plan

1. **Ontology owners:** decide whether to accept the six logical partitions and
   select IDs, prefixes, versions, maintainers, predicate registry, relation
   cardinalities/inverses, authority-decision ownership, placement, and migration.
2. **Refine owner:** turn the exact three-artifact witness and thirteen criteria into
   a bounded Work Pack, including the missing graph acceptance test. This findings
   artifact is input, not execution confirmation.
3. **ResonantOS API/SDK owners:** preserve the host Agent API as the single
   consultation protocol; specify only a declaration plus stateless SDK adapter and
   retain separate declaration/grant/enforcement records.
4. **Memory/Living Archive owners:** retain broker routing and choose any future
   consultation-plus-memory composition; independently resolve standalone Living
   Archive runtime/artifact ownership.
5. **Experience/page owner:** keep the current root page for the MVP, implement the
   accessible robot/card and synchronized graph only after an accepted plan, and
   validate staged bytes against the finite witness.
6. **Operator/release owners:** separately establish projection installation,
   protected deployment, publication, release, and production evidence. None is
   inherited from research or local tests.

## Killed alternatives

The evidence closure kills: Augmentor-as-ResonantOS; agent-as-capability;
add-on-as-SDK; SDK-as-API; API/retrieval/validation/page action as authority; a direct
generic Living Archive API bypassing the broker; a second consultation protocol;
Living Archive as Augmentor's internal database; source record as ontology concept;
memory index as source truth; view edge as semantic relation; page/graph as ontology
truth; working consultation through the planned SDK seam; implemented standalone
Living Archive ontology storage; six physical packages inferred from logical
partitions; MVP relocation; an already implemented fixture or graph validator; and
claims of current installation, protected deployment, publication, release, or
production readiness (`EVIDENCE-CLOSURE.json:killed_claims`).

## Authority and implementation residue

These findings select a product direction and preserve a reviewed design correction;
they do not accept an ontology, modify product code, install a capability, grant a
principal, validate a runtime deployment, or authorize Refine execution. The
candidate ontology and generated page remain private candidate-local read surfaces.
The following remain explicitly unresolved: package identities and ownership,
physical placement and migration, relation cardinalities/inverses,
authority-decision package ownership, consultation-plus-memory composition,
standalone Living Archive runtime/artifact, installed projection state, protected
deployment, and implementation/execution of the finite fixture
(`EVIDENCE-CLOSURE.json:deferred_and_excluded,writer_admission`).

The warranted close is narrow: the sources support a current-root documentation
direction that explains the ResonantOS host through accessible Augmentor robot cores,
uses source-bound technical cards, presents the implemented Agent API without
duplicating it in the SDK, separates the internal SDK from its planned consultation
seam, and traces memory through the owned broker/Living Archive boundary. They do not
prove implementation readiness, ontology admission, publication, deployment,
release, or production authority.

## Source selector ledger

- ResonantOS runtime and ownership:
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/MODULE_MAP.md:7-32,63-76`;
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/MODULE-OWNERSHIP.md:20-21,28-29,39-46`.
- Add-on SDK:
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-018-addon-sdk-v0.md:15-26,100-126,218-250,340-360`.
- Agent API contract and documentation:
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/browser-first/host/augmentor-consultation-contract.mjs:1-18,146-193`;
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/reference/AUGMENTOR_CONSULTATION_API.md#Send-A-Request`;
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/reference/AUGMENTOR_CONSULTATION_API.md#Ask-About-One-Robot-Region`;
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/reference/AUGMENTOR_CONSULTATION_API.md#Safety-Boundary`.
- Neutral memory-provider broker:
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-026-minimal-kernel-replaceable-default-addons.md:47-113,172-193`.
- ResonantOS Living Archive host loop:
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-027-living-archive-llm-wiki-compliance.md:45-68,88-146`.
- Standalone Living Archive:
  `/home/vrondelli/projects/living-archive/README.md:3-7,15-25`.
- Unified ontology owner boundary, page, validation, and anatomy:
  `projects/augmentor/ontology/unified-agent/README.md:11-33,62-71,136-145`;
  `projects/augmentor/ontology/unified-agent/visualization/anatomy-map.json:2-15,29,47-50,97-109,122-135,200-215`.
- Robot, Agent API, and visualization test surfaces:
  `projects/augmentor/ontology/unified-agent/tests/robot-consultation.browser.mjs:190-240,255-326`;
  `projects/augmentor/ontology/unified-agent/tests/agent-api.browser.mjs`;
  `projects/augmentor/ontology/unified-agent/tests/visualization.test.mjs`;
  `projects/augmentor/ontology/unified-agent/tests/visualization.browser.mjs`.
- SDK consultation plan ceiling:
  `projects/augmentor/ontology/unified-agent/development/invoke-runs/20260806T183814Z-addon-sdk-ontology-api/WORK-PACK.md:87-126,149-152`.
- Evidence closure and authoritative synthesis:
  `research/2026-08-09-augmentor-resonantos-ontology-docs-mvp/EVIDENCE-CLOSURE.json:resolution_rows[AOD-001..AOD-010],writer_admission,killed_claims,deferred_and_excluded`;
  `research/2026-08-09-augmentor-resonantos-ontology-docs-mvp/SYNTHESIS-FINAL.md#Non-Collapse-Model`;
  `research/2026-08-09-augmentor-resonantos-ontology-docs-mvp/SYNTHESIS-FINAL.md#Query-And-Update-Direction`;
  `research/2026-08-09-augmentor-resonantos-ontology-docs-mvp/SYNTHESIS-FINAL.md#One-Documentation-Experience`;
  `research/2026-08-09-augmentor-resonantos-ontology-docs-mvp/SYNTHESIS-FINAL.md#Agent-API-Core-Consultation-Contract`;
  `research/2026-08-09-augmentor-resonantos-ontology-docs-mvp/SYNTHESIS-FINAL.md#Living-Archive-Contract`;
  `research/2026-08-09-augmentor-resonantos-ontology-docs-mvp/SYNTHESIS-FINAL.md#Finite-MVP-Fixture-And-Acceptance-Manifest`.
