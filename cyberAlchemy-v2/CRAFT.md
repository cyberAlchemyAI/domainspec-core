# CyberAlchemy v2 Craft Ledger

Human-readable view of [.craft/ledger.yml](.craft/ledger.yml). The ledger is
the source of truth; this page is a linked status and navigation surface.

## Quick Links

- Root context: [CTX-CAV2-ROOT](#context-ctx-cav2-root)
- Definition tower work: [CTX-CAV2-DEF-TOWERS](#context-ctx-cav2-def-towers)
- Authority imports: [CTX-CAV2-AUTHORITY-IMPORTS](#context-ctx-cav2-authority-imports)
- Constitution towers: [CTX-CAV2-CONSTITUTION-TOWERS](#context-ctx-cav2-constitution-towers)
- Craft execution surface: [CTX-CAV2-CRAFT-SURFACE](#context-ctx-cav2-craft-surface)
- Boundary review: [CTX-CAV2-BOUNDARY](#context-ctx-cav2-boundary)
- Mint feature (new 2026-06-29): `CTX-CAV2-MINT` + 6 sub-contexts in [.craft/ledger.yml](.craft/ledger.yml) · resolved design + plan: [refine RESULT](development/refinement-runs/20260629T0000Z-cav2-mint-feature/RESULT.md) _(full human-view section regenerable from ledger)_
- DomainSpec v2 (new 2026-06-29): [CTX-CAV2-DOMAINSPEC-V2](#context-ctx-cav2-domainspec-v2) — v2 rework of the DomainSpec pillar · v1→v2 import triage done ([findings](../projects/domainspec-v2/research/2026-06-29-v1-import-triage/findings.md))
- Blocking decisions: [DEC-CAV2-VISIBLE-SPACES-001](#decision-dec-cav2-visible-spaces-001), [DEC-CAV2-PUBLIC-PRIVATE-001](#decision-dec-cav2-public-private-001)
- Active blockers: [BLK-CAV2-SOURCE-TRUTH-001](#blocker-blk-cav2-source-truth-001), [BLK-CAV2-PUBLIC-PRIVATE-001](#blocker-blk-cav2-public-private-001), [BLK-CAV2-VISIBLE-SPACES-001](#blocker-blk-cav2-visible-spaces-001)
- Definition towers artifact: [authority/definitions/DEFINITION-TOWERS.md](authority/definitions/DEFINITION-TOWERS.md)
- Definition localization route: [authority/definitions/DEFINITION-LOCALIZATION-ROUTE.md](authority/definitions/DEFINITION-LOCALIZATION-ROUTE.md)
- Primordial definition cluster: [authority/definitions/source-clusters/primordial.md](authority/definitions/source-clusters/primordial.md)
- Arcanum definition cluster: [authority/definitions/source-clusters/arcanum.md](authority/definitions/source-clusters/arcanum.md)
- Invoke report: [development/invoke/definition-towers/INVOKE-RESULT.md](development/invoke/definition-towers/INVOKE-RESULT.md)

## Contexts

### <a id="context-ctx-cav2-root"></a>CTX-CAV2-ROOT - CyberAlchemy v2 Stable Repository Consolidation

- Stage: `define`
- Gate: `flag`
- Purpose: keep the next stable repository work source-ledgered, authority-bounded, and executable from Craft.
- Current next move: cluster, deduplicate, and localize the 149 staged definition candidates after promoting D29-D39 from the primordial basis.

### <a id="context-ctx-cav2-spaces"></a>CTX-CAV2-SPACES - Project, Source, And Execution Spaces

- Stage: `define`
- Gate: `flag`
- Purpose: map every relevant project area, source corpus, and Craft execution node before deeper promotion work.
- Current next move: review the project/source/Craft space map and close or defer [DEC-CAV2-VISIBLE-SPACES-001](#decision-dec-cav2-visible-spaces-001).
- Evidence: [authority/definitions/DEFINITION-TOWERS.md](authority/definitions/DEFINITION-TOWERS.md), [SOURCE-MAP.md](SOURCE-MAP.md), [.arcanum inventory index](../.arcanum/inventory/index.md), [.arcanum ontology map](../.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md)

### <a id="context-ctx-cav2-def-towers"></a>CTX-CAV2-DEF-TOWERS - Definition Towers And Promotion Queue

- Stage: `define`
- Gate: `flag`
- Purpose: organize high-to-low definition towers for CyberAlchemy, Arcanum, DomainSpec, Craft, knowledge governance, research/product, and validation/ops terms.
- Current next move: classify `artifact` as the last explicit T-1 candidate, then cluster remaining definition candidates by tower, source family, authority posture, and promotion action.
- Evidence: [authority/definitions/DEFINITION-TOWERS.md](authority/definitions/DEFINITION-TOWERS.md), [authority/definitions/DEFINITION-LOCALIZATION-ROUTE.md](authority/definitions/DEFINITION-LOCALIZATION-ROUTE.md), [authority/definitions/source-clusters/primordial.md](authority/definitions/source-clusters/primordial.md), [authority/definitions/source-clusters/arcanum.md](authority/definitions/source-clusters/arcanum.md), [authority/definitions/DEFINITIONS.md](authority/definitions/DEFINITIONS.md), [authority/imports/definitions/MANIFEST.md](authority/imports/definitions/MANIFEST.md)

### <a id="context-ctx-cav2-authority-imports"></a>CTX-CAV2-AUTHORITY-IMPORTS - Authority Imports And Candidate Clustering

- Stage: `define`
- Gate: `flag`
- Purpose: classify staged definitions, constitutions, axioms, and rule candidates before local promotion.
- Current next move: convert the 149 definition candidates into v2-local representation clusters by tower, source family, authority posture, and promotion action.
- Evidence: [authority/imports/definitions/MANIFEST.md](authority/imports/definitions/MANIFEST.md), [authority/imports/constitutions/MANIFEST.md](authority/imports/constitutions/MANIFEST.md)

### <a id="context-ctx-cav2-constitution-towers"></a>CTX-CAV2-CONSTITUTION-TOWERS - Constitution, Axiom, And Rule Towers

- Stage: `define`
- Gate: `flag`
- Purpose: group constitution and rule sources into towers before composing any CyberAlchemy v2 constitution pack.
- Current next move: cluster 106 constitution and axiom candidates into rule towers before composing a v2 constitution pack.
- Evidence: [authority/imports/constitutions/MANIFEST.md](authority/imports/constitutions/MANIFEST.md), [authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md](authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md)

### <a id="context-ctx-cav2-craft-surface"></a>CTX-CAV2-CRAFT-SURFACE - Craft Execution Surface

- Stage: `execute`
- Gate: `flag`
- Purpose: make Craft the local executable ledger for definition towers, blockers, decisions, gaps, next moves, and later recomposition.
- Current next move: keep [.craft/ledger.yml](.craft/ledger.yml) as source of truth and update this view after each meaningful route.
- Evidence: [.craft/ledger.yml](.craft/ledger.yml), [.craft/index.json](.craft/index.json)

### <a id="context-ctx-cav2-boundary"></a>CTX-CAV2-BOUNDARY - Public/Private And Visibility Boundary

- Stage: `validate`
- Gate: `flag`
- Purpose: prevent private implementation evidence, validation evidence, and read-model surfaces from becoming public or canonical by proximity.
- Current next move: resolve public/private and visible-space decisions before standalone extraction.
- Evidence: [SOURCE-MAP.md](SOURCE-MAP.md), [authority/promotion-policy.md](authority/promotion-policy.md)

### <a id="context-ctx-cav2-execution"></a>CTX-CAV2-EXECUTION - Work-Pack And Task-Session Execution Path

- Stage: `plan`
- Gate: `flag`
- Purpose: convert classified tower work into bounded implementation or governance tasks only after promotion and boundary gates are clear enough.
- Current next move: after import clustering, create a bounded work-pack or task-session slice from this ledger.
- Evidence: [development/invoke/definition-towers/INVOKE-RESULT.md](development/invoke/definition-towers/INVOKE-RESULT.md)

### <a id="context-ctx-cav2-domainspec-v2"></a>CTX-CAV2-DOMAINSPEC-V2 - DomainSpec v2 — Pillar Rework

- Stage: `define`
- Gate: `flag`
- Parent: [CTX-CAV2-ROOT](#context-ctx-cav2-root) (recomposes into root) · sibling of the Mint feature (`CTX-CAV2-MINT`)
- Purpose: a fresh v2 design effort for the DomainSpec pillar (the *what* — typed intent → engine / Lean kernel), reworked as a peer cav2 workstream. Opened 2026-06-29 on user request; not yet scoped into blockers, decisions, gaps, or owned artifacts.
- Current next move: **PIVOT (2026-06-29)** — v2 is now the *implementation home*; v1 to be frozen. SWU-A1 hook already shipped in v1. **Batch 1 migration done**: forked the engine (incl. private `src/rules` moat) + 6 Ontology-A docs into [`impl/`](../projects/domainspec-v2/impl/) + seeded [IMPORT-MANIFEST](../projects/domainspec-v2/IMPORT-MANIFEST.md). Batch 2 (validators + code-tag tooling) imported. **impl/ FULLY GREEN 2026-06-30** via npm (pnpm was the blocker, not network): `engine:test` 97/97 · `tags:test` 8/8 · `validate` RC 0 · `typecheck` RC 0 — the validation-governance gate (C9/C10/C11) runs. Next = reformulate the imported docs + Batch 3, freeze v1, wire G4 gate-in-CI.

## Decisions

### <a id="decision-dec-cav2-tower-altitude-001"></a>DEC-CAV2-TOWER-ALTITUDE-001 - Tower Altitude

- Question: Should CyberAlchemy v2 be the umbrella, Arcanum and DomainSpec be pillars, and Craft be an Arcanum-owned execution sub-tower with local priority?
- Status: `active`, non-blocking
- Current selection: `umbrella-pillars-craft-subtower`
- Default direction: `umbrella-pillars-craft-subtower`
- Impact: lets mapping continue while definitions-governance remains responsible for term promotion.
- Evidence: [authority/definitions/DEFINITION-TOWERS.md](authority/definitions/DEFINITION-TOWERS.md)

### <a id="decision-dec-cav2-visible-spaces-001"></a>DEC-CAV2-VISIBLE-SPACES-001 - Visible Inventory/Ontology Spaces

- Question: Should CyberAlchemy v2 keep visible `inventory/` and `ontology/` spaces, or hide them under `.arcanum` with exported docs before standalone extraction?
- Status: `active`, `blocking`
- Current selection: pending
- Default direction: `keep-visible-project-spaces`
- Impact: blocks standalone extraction and final architecture authority, but not local tower mapping.
- Evidence: [SOURCE-MAP.md](SOURCE-MAP.md)

### <a id="decision-dec-cav2-public-private-001"></a>DEC-CAV2-PUBLIC-PRIVATE-001 - Public/Private Evidence Boundary

- Question: Which private implementation and validation evidence may influence public or standalone CyberAlchemy v2 artifacts?
- Status: `active`, `blocking`
- Current selection: pending
- Default direction: `public-safe-pattern-cards-after-scrub`
- Impact: blocks public-facing reuse and extraction, but not private local classification.
- Evidence: [SOURCE-MAP.md](SOURCE-MAP.md)

### <a id="decision-dec-cav2-definition-localization-001"></a>DEC-CAV2-DEFINITION-LOCALIZATION-001 - Definition Localization Route

- Question: Should imported definitions remain external references, or should CyberAlchemy v2 hold project-local representations for all definition material?
- Status: `closed`, non-blocking
- Current selection: `v2-local-definition-space`
- Default direction: `v2-local-definition-space`
- Impact: changes the next definition step from reference-only linking to v2-local source-cluster representation with provenance and authority posture.
- Evidence: [authority/definitions/DEFINITION-LOCALIZATION-ROUTE.md](authority/definitions/DEFINITION-LOCALIZATION-ROUTE.md)

## Blockers

### <a id="blocker-blk-cav2-source-truth-001"></a>BLK-CAV2-SOURCE-TRUTH-001

- Lane: `governance`
- Status: `active`, `refined`
- Role: `definitions_governance`
- Human required: `true`
- Closure: definition candidates have v2-local representation records with provenance, authority posture, and promotion route before promotion.
- Linked decision: [DEC-CAV2-TOWER-ALTITUDE-001](#decision-dec-cav2-tower-altitude-001)
- Evidence: [authority/imports/definitions/MANIFEST.md](authority/imports/definitions/MANIFEST.md)

### <a id="blocker-blk-cav2-public-private-001"></a>BLK-CAV2-PUBLIC-PRIVATE-001

- Lane: `governance`
- Status: `active`, `refined`
- Role: `decision_gate`
- Human required: `true`
- Closure: [DEC-CAV2-PUBLIC-PRIVATE-001](#decision-dec-cav2-public-private-001) closes with public/private derivative rules and evidence links.
- Evidence: [SOURCE-MAP.md](SOURCE-MAP.md)

### <a id="blocker-blk-cav2-visible-spaces-001"></a>BLK-CAV2-VISIBLE-SPACES-001

- Lane: `architecture`
- Status: `active`, `typed`
- Role: `decision_gate`
- Human required: `true`
- Closure: [DEC-CAV2-VISIBLE-SPACES-001](#decision-dec-cav2-visible-spaces-001) closes or defers with explicit extraction-stage rationale.
- Evidence: [SOURCE-MAP.md](SOURCE-MAP.md)

## Gaps

### <a id="gap-gap-cav2-term-clustering-001"></a>GAP-CAV2-TERM-CLUSTERING-001

- Severity: `flag`
- Treatment: `plan`
- Owner route: `definitions-governance`
- Summary: the 149 definition candidates are staged but not clustered by tower, source family, term type, or authority posture.

### <a id="gap-gap-cav2-duplicate-detection-001"></a>GAP-CAV2-DUPLICATE-DETECTION-001

- Severity: `flag`
- Treatment: `plan`
- Owner route: `definitions-governance`
- Summary: duplicate and conflicting terms across Arcanum, DomainSpec, CyberAlchemy, MARS, Ontologize, project glossaries, and research towers have not been detected.

### <a id="gap-gap-cav2-constitution-clustering-001"></a>GAP-CAV2-CONSTITUTION-CLUSTERING-001

- Severity: `flag`
- Treatment: `plan`
- Owner route: `constitution-governance`
- Summary: constitution, axiom, quality-bar, and anti-pattern sources are staged but not clustered into rule towers or composition packs.

### <a id="gap-gap-cav2-workpack-001"></a>GAP-CAV2-WORKPACK-001

- Severity: `deferred`
- Treatment: `split`
- Owner route: `invoke plan then task-session`
- Summary: no bounded work-pack or task-session slice exists yet for executing definition clustering from the Craft surface.

### <a id="gap-gap-cav2-local-representation-001"></a>GAP-CAV2-LOCAL-REPRESENTATION-001

- Severity: `flag`
- Treatment: `plan`
- Owner route: `Craft + definitions-governance`
- Summary: the Arcanum and primordial source clusters are represented; remaining source definition candidates need project-local representation records before promotion or non-promotion decisions can be compared.

## Promoted Definitions

- **CyberAlchemy v2** - [CAV2-D9](authority/definitions/DEFINITIONS.md#cav2-d9-cyberalchemy-v2)
- **definition tower** - [CAV2-D10](authority/definitions/DEFINITIONS.md#cav2-d10-definition-tower)
- **tower space** - [CAV2-D11](authority/definitions/DEFINITIONS.md#cav2-d11-tower-space)
- **Craft execution surface** - [CAV2-D12](authority/definitions/DEFINITIONS.md#cav2-d12-craft-execution-surface)
- **authority promotion queue** - [CAV2-D13](authority/definitions/DEFINITIONS.md#cav2-d13-authority-promotion-queue)
- **source space** - [CAV2-D14](authority/definitions/DEFINITIONS.md#cav2-d14-source-space)
- **project space** - [CAV2-D15](authority/definitions/DEFINITIONS.md#cav2-d15-project-space)
- **typed coupling invariant** - [CAV2-D16](authority/definitions/DEFINITIONS.md#cav2-d16-typed-coupling-invariant)
- **reflection tower method** - [CAV2-D17](authority/definitions/DEFINITIONS.md#cav2-d17-reflection-tower-method)
- **residue** - [CAV2-D18](authority/definitions/DEFINITIONS.md#cav2-d18-residue)
- **ontology** - [CAV2-D19](authority/definitions/DEFINITIONS.md#cav2-d19-ontology)
- **Craft method** - [CAV2-D20](authority/definitions/DEFINITIONS.md#cav2-d20-craft-method)
- **four-facet action method** - [CAV2-D21](authority/definitions/DEFINITIONS.md#cav2-d21-four-facet-action-method)
- **orthogonal classification** - [CAV2-D22](authority/definitions/DEFINITIONS.md#cav2-d22-orthogonal-classification)
- **authority lifecycle axis** - [CAV2-D23](authority/definitions/DEFINITIONS.md#cav2-d23-authority-lifecycle-axis)
- **provenance-first navigation** - [CAV2-D24](authority/definitions/DEFINITIONS.md#cav2-d24-provenance-first-navigation)
- **schema amendment witness** - [CAV2-D25](authority/definitions/DEFINITIONS.md#cav2-d25-schema-amendment-witness)
- **append-only event ledger** - [CAV2-D26](authority/definitions/DEFINITIONS.md#cav2-d26-append-only-event-ledger)
- **residue entropy** - [CAV2-D27](authority/definitions/DEFINITIONS.md#cav2-d27-residue-entropy)
- **value-cycle edge guard** - [CAV2-D28](authority/definitions/DEFINITIONS.md#cav2-d28-value-cycle-edge-guard)
- **axis orthogonality invariant** - [CAV2-D29](authority/definitions/DEFINITIONS.md#cav2-d29-axis-orthogonality-invariant)
- **bounded recursive self-application** - [CAV2-D30](authority/definitions/DEFINITIONS.md#cav2-d30-bounded-recursive-self-application)
- **primitive type** - [CAV2-D31](authority/definitions/DEFINITIONS.md#cav2-d31-primitive-type)
- **method** - [CAV2-D32](authority/definitions/DEFINITIONS.md#cav2-d32-method)
- **definition** - [CAV2-D33](authority/definitions/DEFINITIONS.md#cav2-d33-definition)
- **authority** - [CAV2-D34](authority/definitions/DEFINITIONS.md#cav2-d34-authority)
- **provenance** - [CAV2-D35](authority/definitions/DEFINITIONS.md#cav2-d35-provenance)
- **traceability** - [CAV2-D36](authority/definitions/DEFINITIONS.md#cav2-d36-traceability)
- **gate** - [CAV2-D37](authority/definitions/DEFINITIONS.md#cav2-d37-gate)
- **claim <= proof** - [CAV2-D38](authority/definitions/DEFINITIONS.md#cav2-d38-claim-proof-bound)
- **intent** - [CAV2-D39](authority/definitions/DEFINITIONS.md#cav2-d39-intent)

## Pending By Node

| Node | Pending |
| --- | --- |
| CTX-CAV2-ROOT | Cluster, deduplicate, and localize the 149 staged definition candidates now that Operational Ontology and the D29-D39 primordial-basis terms are resolved. |
| CTX-CAV2-SPACES | DEC-CAV2-VISIBLE-SPACES-001 remains blocking for extraction readiness. |
| CTX-CAV2-DEF-TOWERS | Classify `artifact` as the last explicit T-1 candidate, then cluster remaining definition candidates by tower, source family, authority posture, and promotion action; BLK-CAV2-SOURCE-TRUTH-001, GAP-CAV2-DUPLICATE-DETECTION-001, and GAP-CAV2-LOCAL-REPRESENTATION-001 remain active. |
| CTX-CAV2-AUTHORITY-IMPORTS | GAP-CAV2-TERM-CLUSTERING-001; convert candidates into v2-local representation clusters. |
| CTX-CAV2-CONSTITUTION-TOWERS | GAP-CAV2-CONSTITUTION-CLUSTERING-001. |
| CTX-CAV2-CRAFT-SURFACE | Update the human view after each meaningful ledger mutation. |
| CTX-CAV2-BOUNDARY | DEC-CAV2-PUBLIC-PRIVATE-001 and DEC-CAV2-VISIBLE-SPACES-001. |
| CTX-CAV2-EXECUTION | GAP-CAV2-WORKPACK-001; create a work-pack after import clustering. |
| CTX-CAV2-DOMAINSPEC-V2 | PIVOT: v2 = implementation home, v1 to be frozen. Batch 1+2 forked engine+docs+validators → impl/ + IMPORT-MANIFEST. **impl/ FULLY GREEN 2026-06-30** (npm; engine:test 97/97 · tags:test 8/8 · validate RC 0 · typecheck RC 0). Pending: Batch 3 (audit/layering reformulate); reformulate 6 imported-verbatim docs; v1-freeze; G4 gate-in-CI. Residue: C10/lint vacuous until a real feature lands; attestation fire-point + provability-as-moat bet (commercialization decision-gate); the Lean-positioning question still open. |

## Artifacts

- [.craft/ledger.yml](.craft/ledger.yml) - machine source of truth.
- [.craft/index.json](.craft/index.json) - derived lookup index.
- [CRAFT.md](CRAFT.md) - this human view.
- [authority/definitions/DEFINITION-TOWERS.md](authority/definitions/DEFINITION-TOWERS.md) - candidate tower map.
- [authority/definitions/DEFINITION-LOCALIZATION-ROUTE.md](authority/definitions/DEFINITION-LOCALIZATION-ROUTE.md) - route for localizing imported definitions inside v2.
- [authority/definitions/source-clusters/primordial.md](authority/definitions/source-clusters/primordial.md) - primordial source cluster; D29-D39 are promoted from this cluster and `artifact` remains the next T-1 review candidate.
- [authority/definitions/source-clusters/arcanum.md](authority/definitions/source-clusters/arcanum.md) - v2-local representation rows for Arcanum-wide definitions.
- [development/invoke/definition-towers/INVOKE-RESULT.md](development/invoke/definition-towers/INVOKE-RESULT.md) - Invoke define report.
- [authority/imports/definitions/MANIFEST.md](authority/imports/definitions/MANIFEST.md) - definition import ledger.
- [authority/imports/constitutions/MANIFEST.md](authority/imports/constitutions/MANIFEST.md) - constitution import ledger.

## Boundary Check

No Arcanum canonical surfaces, generated runtime skills, private DomainSpec
implementation files, or validation submodule files were mutated by this Craft
start. This surface records local CyberAlchemy v2 state only.
