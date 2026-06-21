---
tags: [ontology-vault, dispersed-knowledge, inventory, branch-map, knowledge-craft-governance, candidate-condensation]
node_type: ontology-map
is_session: false
layer: architecture
nature: reference
status: draft
created: 2026-06-18
dispatch_id: 2026-06-18-dispersed-knowledge-cartography
dispatch_type: research
working_folder: .arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/
sources: [.arcanum/inventory/, .arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/cartographer-receipts.md, .arcanum/inventory/entries/evidence-cards/2026-06-18-dispersed-knowledge-cards.md, .arcanum/inventory/entries/evidence-sets/2026-06-18-dispersed-knowledge-sets.md, arcanum/, implementation/domainspec/, projects/framework-unification, projects/ontologize, cyberAlchemy/, .claude/skills/]
---

# Ontology Map - Dispersed Knowledge Condensation

## Scope

- Repository: current `domainspec-core` checkout
- Source folders: `.arcanum/inventory/`, `arcanum/`,
  `implementation/domainspec/`, `projects/framework-unification`,
  `projects/ontologize`, `cyberAlchemy/`, `.claude/skills/`, `research/`,
  `projects/domainspec-v2/`
- Mapping date: 2026-06-18
- Authority: candidate ontology-vault read model only

## Observed Structures

| Structure | Local Name | Generic Concept | Evidence | Notes |
| --- | --- | --- | --- | --- |
| role | `node_type` | knowledge role | `research/cyber-alchemy-space/capability-taxonomy/findings.md`, `.arcanum/inventory/schema.md` | Synthesis: frontmatter classifies findings, research, source manifests, and candidate maps. |
| axis | `layer` | ontology layer | `research/cyber-alchemy-space/capability-taxonomy/findings.md`, `.arcanum/inventory/tags.md` | Synthesis: local layer vocabulary is useful but not yet a canonical crosswalk. |
| maturity | `status` | maturity status | `.arcanum/inventory/schema.md`, `cyberAlchemy/agentic-system-definition.md`, `projects/domainspec-v2/README.md` | Synthesis: candidate/draft/verified/pass/flag/block appear across surfaces. |
| source authority | `sources` | evidence source set | `research/cyber-alchemy-space/capability-taxonomy/findings.md` | Good pattern for inventory-generated artifacts. |
| promotion split | `Inventory -> Ontology -> Definitions/Governance` | source authority rule | `cyberAlchemy/agentic-system-inventory-ontology-pipeline.md`, `.agents/skills/inventory/SKILL.md`, `.agents/skills/ontology-vault/SKILL.md` | Inventory captures evidence; ontology condenses meaning; definitions/governance own promotion. |

## Branch Classification

| Path | Branch | Owner Claim | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `cyberAlchemy/` | business | Agentic-system meaning, philosophy, product narrative, ontology candidates. | `cyberAlchemy/agentic-system-inventory-ontology-pipeline.md` | Contains candidate human-visible ontology pack ideas. |
| `projects/ontologize/` | business, bridge | Product/method knowledge and delivery ontology. | `projects/ontologize/TOWER.md`, `projects/ontologize/levels/L1-pattern-map.md`, `projects/ontologize/PUBLIC-OFFERING.md` | Needs owner review before confidence promotion. |
| `projects/domainspec-v2/` | business, bridge | v2 research hypotheses, lanes, formal modeling, and candidate design ideas. | `projects/domainspec-v2/README.md` | Research stays non-canonical until governed promotion. |
| `arcanum/` | system, bridge | Public capability framework, sigils, spells, registry, method. | `arcanum/README.md` | Public-safe boundary is mandatory. |
| `implementation/domainspec/` | system, bridge | Private v1 implementation and runtime evidence. | `implementation/domainspec/ARCHITECTURE.md`, `.gitmodules` | Submodule owner boundary applies. |
| `.agents/skills/`, `.claude/skills/` | system | Generated runtime skill surfaces. | `.agents/skills/arcanum-bootstrap/SKILL.md`, `.claude/skills/arcanum-bootstrap/SKILL.md`, `.github/skills/README.md` | Must trace canonical source before authority claims. |
| `.arcanum/observability/` | bridge | Runtime evidence and reflection signals. | `.arcanum/observability/README.md` | Evidence, not semantic authority. |
| `.arcanum/inventory/` | bridge | Compiled knowledge lookup layer. | `.arcanum/inventory/README.md` | Candidate read model; not raw authority. |

## Roles And Axes

| Generic Concept | Local Labels | Purpose | Challenge Response | Gaps |
| --- | --- | --- | --- | --- |
| knowledge role | `node_type`, entry `Type`, evidence-card `card_type` | Classify artifacts and cards for lookup. | Keep frontmatter and inventory entry types aligned. | No controlled crosswalk yet. |
| maturity status | `status`, validation result, promotion status | Separate draft, candidate, verified, pass, flag, block. | Preserve evidence confidence separately from commitment confidence. | Status vocabularies differ by surface. |
| evidence source | `sources`, `source_refs`, `evidence_refs` | Link claims to raw paths and selectors. | Require concrete source refs before synthesis. | Most current inventory entries lack selector-level cards. |
| branch ownership | business, system, bridge, mixed, unknown | Prevent business meaning and system implementation from silently redefining each other. | Bridge claims need evidence on both sides. | Branch classification not yet applied claim-by-claim. |
| promotion owner | inventory, ontology-vault, definitions-governance, decision-gate | Prevent direct promotion from execution evidence. | Use promotion splits and owner gates. | No reviewed promotion decisions for this map. |

## Edge Rules

| Edge Type | Direction | Allowed Sources | Allowed Targets | Validation Rule |
| --- | --- | --- | --- | --- |
| `traced_to` | candidate knowledge -> source | any inventory or ontology candidate | raw source path, selector, receipt | Must cite concrete path or evidence-card ID. |
| `realized_by` | business -> system | business concept, intent, workflow | implementation artifact, runtime adapter, skill | Requires evidence from both branches. |
| `observed_by` | claim -> signal | workflow, capability, route claim | observability signal, run envelope, dispatch ledger | Signal is evidence, not meaning. |
| `tested_by` | claim -> test | spec, capability, workflow | test, fixture, validation report | Test cannot redefine business claim. |
| `drifts_from` | observed behavior -> expectation | runtime observation, failure mode | business intent, spec, decision | Preserve both sides and do not smooth contradiction. |
| `candidate_groups` | evidence set -> task | EvidenceSet | context-builder or downstream sigil handoff | EvidenceSet references cards, not copied claims. |

## Inflection Assessment

- Domain knowledge: medium
- Uncertainty: high
- Investment posture: discovery plus focused experiment
- Rationale: The repo already has rich knowledge-governance surfaces and
  candidate ontology material, but the sources are dispersed, generated mirrors
  complicate authority, and branch ownership is not consistently recorded at
  claim level. Full ontology promotion is premature; an inventory-first pass is
  justified.

## Condensed Candidate Map

| Condensed Node | Branch | Candidate Meaning | Evidence Posture | Next Owner |
| --- | --- | --- | --- | --- |
| Capability Catalog And Runtime Projection | system, bridge | Arcanum registries, canonical packages, spells, runtime adapters, and generated projections are separate capability surfaces. | Candidate from `arcanum-registry-catalog`, `arcanum-task-session-runtime-boundary`, `arcanum-runtime-projection-surfaces`. | inventory, then capability owner review. |
| Inventory Evidence Substrate | bridge | Inventory pages are read models that require source refs or explicit synthesis labels. | Candidate from `knowledge-governance-inventory-authority-contract`. | inventory owner. |
| Ontology Candidate Boundary | bridge | Ontology-vault condenses branch meaning but cannot promote source authority, definitions, glossaries, sigils, spells, or runtime contracts. | Candidate from `knowledge-governance-ontology-candidate-boundary`. | ontology-vault plus governance owner. |
| Feedback And Memory Evidence | bridge | Observability, Necronomicon, sessions, Craft, and dispatch ledgers provide evidence/residue, not semantic authority. | Candidate from `knowledge-governance-observability-control-loop`, `knowledge-governance-necronomicon-memory-boundary`, `sessions-decision-archaeology`. | observability/knowledge-harness owners. |
| DomainSpec v2 Research Program | business, bridge | v2 is research-first and promotion-gated, not an implementation repo yet. | Candidate from `domainspec-v2-research-tower-discipline`. | inventory and decision-gate. |
| Public/Private Boundary | bridge | Public Arcanum and private parent/implementation compose but must not leak private evidence into public artifacts. | Candidate from `domainspec-private-boundary-submodule-discipline`. | inventory plus boundary review. |

## Receipt-Backed Candidate Condensation

| Candidate Node | Branch | Evidence Cards | Meaning Boundary | Promotion Guard |
| --- | --- | --- | --- | --- |
| Arcanum Capability Catalog | system, bridge | `arcanum-registry-catalog`, `arcanum-task-session-runtime-boundary`, `arcanum-runtime-projection-surfaces` | Catalogs, canonical packages, runtime adapters, and projections are separate surfaces. | Generated projections cannot define capability meaning. |
| Private Governance Spine | system, bridge | `domainspec-private-boundary-submodule-discipline`, `domainspec-governance-registry-observability-spine` | Private implementation has computable governance, registry/code binding, and signal loops. | Private evidence needs a public-safe extraction route before public reuse. |
| Validation Feature Pack | system, bridge | `pokerteam-feature-pack-validation-harness` | Feature-pack reports are reusable validation structure evidence. | Dated signal snapshots need refresh before quantitative claims. |
| Research Tower Method | business, bridge | `ontologize-l0-l1-l2-research-product-tower`, `domainspec-v2-research-tower-discipline`, `framework-unification-two-axis-model` | Research moves from corpus to patterns to closure, while two-axis maps prevent lifecycle flattening. | Research towers remain non-canonical until decision-gated. |
| Inventory Evidence Substrate | bridge | `knowledge-governance-inventory-authority-contract`, `cyberalchemy-inventory-ontology-loop` | Source evidence feeds inventory read models with selector-level cards. | Inventory read models require source refs or explicit synthesis labels. |
| Ontology Candidate Condensation | bridge | `knowledge-governance-ontology-candidate-boundary`, `cyberalchemy-thick-ontology-entry-contract` | Ontology-vault may group, classify, and branch-map candidate meaning. | Ontology-vault cannot promote itself or redefine source authority. |
| Feedback And Memory Control | bridge | `knowledge-governance-observability-control-loop`, `knowledge-governance-necronomicon-memory-boundary`, `sessions-decision-archaeology` | Observability and memory surfaces provide feedback evidence and residue. | Signals and sessions are evidence until separately reviewed. |

## V2 Branch Hypothesis

| V2 Area | Branch | EvidenceSet | Candidate Role |
| --- | --- | --- | --- |
| `authority/` | bridge | `evset-public-private-boundary` | Candidate area for definitions, decisions, boundary rules, and promotion policy. |
| `research/` | business, bridge | `evset-v2-repository-structure-hypothesis` | Candidate area for source-ledgered towers and non-canonical synthesis. |
| `capabilities/` | system, bridge | `evset-v2-repository-structure-hypothesis` | Candidate area for catalogs, canonical packages, and generated runtime projections. |
| `validation/` | system, bridge | `evset-v2-repository-structure-hypothesis` | Candidate area for feature-pack harnesses, reports, and evidence snapshots. |
| `inventory/` | bridge | `evset-knowledge-governance-stack` | Selector-level cards and context-ready EvidenceSets. |
| `ontology/` | bridge | `evset-knowledge-governance-stack` | Candidate branch maps and promotion requests only. |
| `observability/` | bridge | `evset-knowledge-governance-stack` | Feedback signals, reflection, dispatch traces, and residue. |

## Boundary-Skeptic Repairs

- Replaced broad selectors with concrete selectors or explicit synthesis labels
  in the card and map layer.
- Reintroduced separate boundary cards for inventory authority,
  ontology-candidate boundary, observability control, Necronomicon memory, and
  operational branch reframing.
- Split the earlier overloaded knowledge-governance node into inventory
  evidence substrate, ontology candidate condensation, and feedback/memory
  control nodes.
- Demoted the v2 tree to a structure hypothesis backed by
  `evset-v2-repository-structure-hypothesis`.
- Preserved missing architecture target and dispatch telemetry authority split
  as contradiction cards.

## Gaps

- Evidence-cards and EvidenceSets are first-pass candidate read models.
- Branch classification is candidate-level; owner review is required before use
  as architecture authority.
- No ontology confidence promotion is recommended from this map.
- Generated skill surfaces need canonical-source tracing before capability
  authority claims.
