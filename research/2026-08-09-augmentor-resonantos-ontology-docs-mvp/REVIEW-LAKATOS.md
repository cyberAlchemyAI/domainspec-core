# REVIEW-LAKATOS — Precedent And Ownership Review

## Verdict

**Revise, then retain.** The federated, owner-preserving direction is defensible, but the draft currently turns a presentation proposal into six apparently settled package identities and understates two implemented ResonantOS precedents: the neutral memory-provider API and the completed host-side Living Archive LLM Wiki loop.

No package name, prefix, version, maintainer, migration, or page relocation is owner-approved. No reviewed component is proven deployed. Precedent does not kill the architecture; it constrains the smallest credible repair.

## Classification

| Material | Classification | Claim ceiling |
| --- | --- | --- |
| ResonantOS Alpha runtime and Augmentor UI | **Already-deployed code path, deployment unproven** | Implemented and documented; not proven installed, released, production-ready, or live |
| Replaceable Augmentor Chat slots | **Build-from-owned** | Documented decision with migration work still named |
| Add-on SDK V0 | **Already-deployed code path, deployment unproven** | Implemented internal SDK; not public marketplace SDK |
| `POST /augmentor/consultation`, contract, service, agent-context adapter | **Already-deployed code path, deployment unproven** | Implemented host-owned read-only interface; no SDK exposure or public deployment inferred |
| Installed neutral projection | **Owner-blocked** | Contract and loader exist; current operator installation is unverified |
| Ontology-consultation SDK request declaration | **Net-new** | `SWU-AOSDK-001` is not started and stops before registry, grants, host binding, installation, or consumers |
| Remaining SDK consultation integration | **Owner-blocked** | Grant, projection approval, installation, consumer, UI, and release owners remain gates |
| Existing unified ontology package and HTML page | **Build-from-owned** | Candidate-local private read model and generated standalone page; no authority or release |
| Six named logical packages and prefixes | **Owner-blocked net-new taxonomy** | Useful proposed partitions, but identities, versions, prefixes, maintainers, and legacy-ID migration are unapproved |
| Beginner Overview | **Build-from-owned** | New composition over owned host/API/SDK/archive evidence |
| Explorable Graph | **Build-from-owned** | Extension of the existing candidate graph/anatomy data |
| Augmentor Anatomy | **Build-from-owned** | Existing candidate anatomy has reusable regions, but many nodes explicitly remain owner-selection-required |
| Developer Interfaces | **Build-from-owned** | Documentation can reuse the implemented SDK and host API; the SDK consultation seam remains net-new |
| Evidence And Limitations | **Net-new presentation** | Source-grounded table design, not runtime capability |
| Deep Reference | **Net-new presentation** | Derived reference layer, not a new authority source |
| Living Archive source/version/search/intake/review/promotion in ResonantOS | **Already-deployed code path, deployment unproven** | ADR-027 records an implemented and completed host baseline |
| Standalone `living-archive` project runtime/artifact | **Owner-blocked** | Separate repository remains docs-first with runtime and artifact type undecided |
| Source-Bound Ontology Concept Record | **Net-new** | Candidate integration record; must not become a second source store, wiki, index, or promotion authority |
| `augmentor.experience` presentation ownership | **Owner-blocked** | No current owner source establishes this owner or package |

## Material Challenges And Smallest Repairs

### 1. Six packages are presented too concretely

The split is a sound design hypothesis, but exact IDs such as `resonantos.system@0.1.0`, prefixes, allowed predicates, and the `augmentor.experience` owner are not inherited from current owner sources. The existing candidate explicitly says the Augmentor meaning owner, disposable-index owner, production-route owner, and canonical knowledge writer remain unresolved.

Selectors:

- `projects/augmentor/ontology/unified-agent/README.md:20-33`
- `projects/augmentor/ontology/unified-agent/visualization/anatomy-map.json:29`
- `projects/augmentor/ontology/unified-agent/visualization/anatomy-map.json:47-50`
- `projects/augmentor/ontology/unified-agent/visualization/anatomy-map.json:97-109`
- `projects/augmentor/ontology/unified-agent/visualization/anatomy-map.json:122-135`

Smallest repair: rename the table **“Proposed logical partitions”**; mark every package ID, version, prefix, predicate allowlist, maintainer, and migration rule `candidate / owner-blocked`. Keep only responsibility boundaries sourced from current owners as established.

### 2. The SDK extension risks duplicating the implemented Agent API

The host already owns a closed, versioned consultation contract and authenticated capability-checked route. The work pack correctly describes the SDK work as a request-only declaration plus an adapter to the existing route, but the synthesis occasionally calls it an “extension” broad enough to sound like a sibling API.

Selectors:

- `../workspace-resonant/2.0.0-alpha/browser-first/host/augmentor-consultation-contract.mjs:5-18`
- `../workspace-resonant/2.0.0-alpha/browser-first/host/augmentor-consultation-contract.mjs:146-193`
- `../workspace-resonant/2.0.0-alpha/browser-first/host/augmentor-consultation-host-service.mjs:8-13`
- `../workspace-resonant/2.0.0-alpha/browser-first/host/augmentor-consultation-host-service.mjs:38-55`
- `projects/augmentor/ontology/unified-agent/development/invoke-runs/20260806T183814Z-addon-sdk-ontology-api/WORK-PACK.md:87-103`
- same work pack `:109-126`
- same work pack `:149-152`

Smallest repair: define the SDK seam exclusively as a manifest declaration and stateless adapter to the host-owned consultation contract. Forbid a second query/result schema, route, projection loader, access registry, cache, or answer policy.

### 3. The draft omits the existing neutral memory-provider API precedent

ADR-026 already specifies a replaceable `memory-system` slot, broker operations, and `POST /memory/{operation}`. A direct page-to-Living-Archive integration or a new Living Archive-specific read/intake API would duplicate that seam and weaken replaceability.

Selectors:

- `../workspace-resonant/2.0.0-alpha/docs/architecture/ADR-026-minimal-kernel-replaceable-default-addons.md:47-66`
- same ADR `:68-113`
- same ADR `:172-193`

Smallest repair: route generic source-memory search/read/intake through the memory-provider broker. Keep Living Archive-specific provenance and review semantics behind its adapter. State explicitly whether consultation merely consumes an installed projection or invokes the memory broker; do not imply both without an owner-selected composition.

### 4. “Living Archive docs-first; runtime partly undecided” conflates two scopes

That claim is true for the separate Living Archive repository, but stale if applied to ResonantOS’s host implementation. ADR-027 says the host baseline implements source/version ledgers, search/index, intake, verifier approval, promotion, lint, and the full LLM Wiki control loop.

Selectors:

- `../living-archive/README.md:3-7`
- `../living-archive/README.md:15-25`
- `../workspace-resonant/2.0.0-alpha/docs/architecture/ADR-027-living-archive-llm-wiki-compliance.md:92-130`
- same ADR `:141-146`
- `../workspace-resonant/2.0.0-alpha/docs/architecture/MODULE-OWNERSHIP.md:30-31`
- same ownership map `:48`

Smallest repair: split the row into:

1. **ResonantOS Living Archive host surface** — implemented, deployment unproven.
2. **Standalone Living Archive project** — docs-first, runtime/artifact owner-blocked.
3. **Source-Bound Ontology Concept Record** — net-new candidate contract.

### 5. The Source-Bound Concept Record could become a duplicate memory store

ADR-027 already owns source versions, wiki pages, provenance, review artifacts, indexes, logs, staleness checks, and promotion. Copying source text, review state, or independent freshness truth into ontology records would establish a second memory database and promotion ledger.

Selectors:

- `../workspace-resonant/2.0.0-alpha/docs/architecture/ADR-027-living-archive-llm-wiki-compliance.md:45-68`
- same ADR `:88-126`
- `../workspace-resonant/2.0.0-alpha/docs/architecture/ADR-026-minimal-kernel-replaceable-default-addons.md:109-113`
- `projects/augmentor/ontology/unified-agent/README.md:27-33`

Smallest repair: make the concept record pointer-only: stable external source/version handles, selectors, digests, and review-receipt references. Living Archive remains owner of source bytes, indexes, review state, and promotion. The projection may cache derived display fields only with digest-bound invalidation.

### 6. Public/private boundaries need an explicit compilation rule

The existing ontology package is private and explicitly forbids projecting private CAV2 terms or owner bindings into ResonantOS without a separate decision. The proposed `resonantos.*` and SDK/API packages could look host-owned or public while originating in the private candidate.

Selectors:

- `projects/augmentor/ontology/unified-agent/README.md:11-18`
- same README `:20-33`
- `../workspace-resonant/2.0.0-alpha/docs/architecture/MODULE-OWNERSHIP.md:37-47`
- `../workspace-resonant/2.0.0-alpha/docs/architecture/ADR-018-addon-sdk-v0.md:15-26`

Smallest repair: keep all six partitions candidate-local until each owner accepts its neutral vocabulary. Compile only an allowlisted, source-handle-based neutral projection; exclude private authority terms, private owner bindings, source paths, and internal notes.

### 7. “Already-deployed” must not be inferred from implementation

The repository contains a deployment adapter, but ownership text describes it as an adapter for a deployment whose reverse proxy has already authenticated the caller; this does not prove any deployment exists. The synthesis correctly says deployment is unverified and should apply that wording consistently to every runtime row.

Selector:

- `../workspace-resonant/2.0.0-alpha/docs/architecture/MODULE-OWNERSHIP.md:28-29`

Smallest repair: use **“implemented code path; deployment unverified”** everywhere unless an operator/deployment receipt is supplied.

### 8. Page relocation remains owner-blocked

The established package says `ontology-visualization.html` is the standalone generated view; no cited owner source authorizes moving it to `/visualization/`.

Selectors:

- `projects/augmentor/ontology/unified-agent/README.md:62-71`
- `projects/augmentor/ontology/unified-agent/visualization/anatomy-map.json:200-215`

Smallest repair: build against the current root page or create a non-authoritative redirect candidate only after the owning project selects the URL contract.

## Killed Alternatives

None are killed by precedent.

- **Unified monolith:** recommended against because it collapses current owners and risks duplicate authority, but precedent alone does not make it impossible.
- **View-only composition:** insufficient for the proposed compatibility/invalidation goals, but remains viable for a smaller documentation-only MVP.
- **Six physical packages:** not selected and not authorized.
- **Direct Living Archive-specific API:** should be rejected for generic memory operations because the neutral memory-provider broker is the existing owner precedent.
- **Second consultation protocol:** should be rejected; the SDK should adapt to the existing host API.

## Residue

- Owners must select package identities, prefixes, versions, maintainers, and legacy-ID migration.
- The host owner must decide whether the documentation page calls consultation only or also consumes the memory-provider broker.
- Living Archive ownership must be split between the implemented ResonantOS host surface and the separate docs-first project.
- Current projection installation, protected deployment, and browser behavior remain unverified.
- No review here grants implementation, acceptance, promotion, publication, release, deployment, or production authority.
