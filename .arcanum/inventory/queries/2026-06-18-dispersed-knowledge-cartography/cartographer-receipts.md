---
tags: [inventory, raw-returns, cartography, dispatch, dispersed-knowledge, promotion-guardrail]
node_type: research
is_session: false
layer: architecture
nature: evidence
status: candidate
created: 2026-06-18
dispatch_id: 2026-06-18-dispersed-knowledge-cartography
dispatch_type: research
working_folder: .arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/
sources: [arcanum/, implementation/domainspec/, validation/poker-team/, projects/, research/, cyberAlchemy/, .arcanum/, .agents/skills/, .claude/skills/, .github/skills/, .codex/commands/]
---

# Cartographer Receipts

Dispatch: `2026-06-18-dispersed-knowledge-cartography`

These receipts are compact parent-ingested read models from the four read-only
cartographers. Raw repository files remain the authority; these returns are
evidence records for inventory synthesis.

## Lifecycle Receipt

| Role | Runtime agent | Nickname | Join | Close | Status |
| --- | --- | --- | --- | --- | --- |
| `cartographer-arcanum-capabilities` | `019eda19-2d62-7c23-8968-17126f6744f4` | Hooke | joined | closed | complete |
| `cartographer-domainspec-private` | `019eda19-2e2c-7cc0-b2c3-83ef014dec00` | Sagan | joined | closed | complete |
| `cartographer-project-research` | `019eda19-305b-7a92-957d-08771bbf894f` | Laplace | joined | closed | complete |
| `cartographer-knowledge-governance` | `019eda19-34da-7873-b207-56bbd52feadf` | Aristotle | joined | closed | complete |

## Arcanum Capability Lane

Corpus covered:

- `arcanum/registry/{README.md,SIGILS.md,SPELLS.md,PACKS.md}`
- `arcanum/spells/{README.md,invoke/README.md,observed-invocation-loop/README.md,arcanum-bootstrap/README.md,discovery-to-inventory/README.md}`
- `arcanum/arcana/task-session/`, `sigil-runtime-installer/`,
  `sigil-development/`, `spellcraft/`, `skill-decomposer/`,
  `structured-interview-kits/`, `refine/`, `inventory/`,
  `workflow-reflect/`, `x-ray/`, `observability-derivation/`
- `arcanum/framework/runtime/`, `arcanum/tools/`
- Generated/projection surfaces: `.agents/skills/`, `.claude/skills/`,
  `.github/skills/`, `.codex/commands/`

Source-backed findings:

- `arcanum/registry/*` is a catalog/index surface, while package files under
  `arcanum/arcana/*` and `arcanum/spells/*` carry capability contracts.
- `arcanum/spells/README.md` and per-spell READMEs treat spells as composed
  workflows over sigils, keeping orchestration distinct from individual
  capability internals.
- `arcanum/arcana/task-session/` splits bounded task coordination from runtime
  adapters, which gives v2 a clean coordinator/runtime boundary.
- `arcanum/arcana/sigil-runtime-installer/` frames native runtime skills as the
  default and `.codex/commands/` as legacy compatibility.
- Generated host surfaces expose projection metadata such as `canonical_source`
  and `mutation_policy`; they should not become alternate sources of truth.
- Observed Invocation Loop and Workflow Reflect make telemetry and reflection a
  maintenance loop, not an afterthought.

Candidate cards:

- `arcanum-registry-catalog`
- `arcanum-canonical-capability-packages`
- `arcanum-spell-composition`
- `arcanum-task-session-runtime-boundary`
- `arcanum-runtime-projection-surfaces`
- `arcanum-observability-reflection-loop`
- `arcanum-authoring-front-door`

Residue:

- Generated host surfaces are broad; the cartographer sampled representative
  files and treated the canonical projection policy as the durable finding.
- Some public Arcanum packages are draft/seed state and must retain maturity
  labels in any v2 projection.

## Private DomainSpec Lane

Corpus covered:

- `AGENTS.md`, `CLAUDE.md`, `SUBMODULE-DISCIPLINE.md`
- `implementation/domainspec/{ARCHITECTURE.md,AUTHORITY-MAP.md,AXIOMS.md,CONSTITUTION.md,ADLC-ALIGNMENT.md,OBSERVABILITY.md,INFRA-SETUP.md,PHASED-PLAN.md,docs/PROJECT-DECISIONS.md,plan/COMPLETENESS-DASHBOARD.md}`
- `implementation/domainspec/tools/{generate-registry.ts,validate-orphans.ts,validate-governance-chain.ts,validate-relationships.ts,validate-signals.ts,analyze-signals.ts}`
- `implementation/domainspec/backend/src/modules/knowledge-graph/domain/models.ts`
- `implementation/domainspec/telemetry/agents/{subagents-dispatch.yaml,agent-pool.yaml}`
- `validation/poker-team/docs/**` feature maps, registry, signals, feature
  reports, and governance baselines
- Parent `telemetry/agents/subagents-dispatch.yaml` and selected `sessions/*.md`

Source-backed findings:

- `AGENTS.md`, `CLAUDE.md`, and `SUBMODULE-DISCIPLINE.md` define the first
  boundary: public Arcanum, private implementation, validation submodule, and
  submodule-first publish order.
- `implementation/domainspec/AXIOMS.md`, `CONSTITUTION.md`, and
  `tools/validate-governance-chain.ts` form a computable governance chain.
- `generate-registry.ts`, `validate-orphans.ts`, and knowledge-graph domain
  models show a code-to-doc binding model with orphan detection and registry
  generation.
- `OBSERVABILITY.md`, signal validation/analyze scripts, and validation signals
  docs define an outer-loop signal system with meta-health.
- Plan-first execution, project decisions, and completeness dashboards preserve
  complexity gates, W0 baseline work, readiness, and decision locks.
- `validation/poker-team` demonstrates a feature-pack validation harness with
  registry, feature map, governance baseline, signals, and pipeline reports.
- Session files hold decision archaeology and should be mined deliberately, not
  silently flattened into canonical docs.

Candidate cards:

- `domainspec-private-boundary-submodule-discipline`
- `domainspec-governance-registry-observability-spine`
- `pokerteam-feature-pack-validation-harness`
- `domainspec-plan-first-execution-contract`
- `sessions-decision-archaeology`

Contradictions and residue:

- `implementation/domainspec/ARCHITECTURE.md` appears to be a compatibility stub
  that points at an absent `architecture/ARCHITECTURE.md` target in this checkout.
- Parent `telemetry/agents/subagents-dispatch.yaml` and submodule
  `implementation/domainspec/telemetry/agents/*` are similarly named but distinct
  authority surfaces.
- Some validation snapshots are dated and should be refreshed before promotion.

## Project And Research Lane

Corpus covered:

- `cyberAlchemy/` agentic-system, ontology, navigation, source-ledger, and
  inventory/ontology pipeline documents
- `research/cyber-alchemy-space/` and `research/intent-annotation-tags/`
- `projects/framework-unification/`
- `projects/ontologize/`
- `projects/domainspec-v2/` research towers for Alloy/TLA modeling, DCB
  correctness, saga correctness, spec ontology, target state, and intent tags

Source-backed findings:

- CyberAlchemy already describes a source -> inventory -> ontology -> context ->
  execution -> telemetry/reflection knowledge loop, plus candidate operational
  ontology branches.
- The CyberAlchemy ontology entry model provides a rich card shape: identity,
  content, context, agent payload, edges, evidence, confidence, promotion, and
  maintenance.
- Framework Unification gives a reusable two-axis model: one horizontal pipeline
  plus vertical mechanisms, with single-owner invariants.
- Ontologize is the clearest L0 corpus -> L1 pattern map -> L2 closure plan
  tower, including a public-facing derivative.
- `projects/domainspec-v2` is research-gated and pre-implementation. Its
  two-lane discipline and tower-local artifacts are v2 structure precedents.
- DCB correctness is narrower than general proof: it centers freshness and
  concurrency at accepted-evidence boundaries, with bounded witnesses first.
- Alloy/TLA research keeps structural and temporal formalisms separate.
- Intent-tags research warns that syntax alone is weak unless grounded in a
  validator contract.

Candidate cards:

- `cyberalchemy-inventory-ontology-loop`
- `cyberalchemy-thick-ontology-entry-contract`
- `framework-unification-two-axis-model`
- `ontologize-l0-l1-l2-research-product-tower`
- `domainspec-v2-research-tower-discipline`
- `domainspec-v2-bounded-witness-freshness`
- `domainspec-v2-intent-tags-validator-grounding`

Contradictions and residue:

- CyberAlchemy architecture documents include candidate/pre-baseline material;
  current vocabulary authority must be checked per document.
- Product-facing Ontologize artifacts and internal research artifacts overlap;
  inventory should keep their public/private and derivative status visible.
- DCB research should not be rephrased as a broad proof-engine commitment.

## Knowledge Governance Lane

Corpus covered:

- `.arcanum/necronomicon/`
- `.arcanum/observability/`
- `.arcanum/inventory/`
- `.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md`
- `arcanum/.craft/`
- CyberAlchemy inventory/ontology pipeline and source ledger
- Ontologize definitions and operational ontology branch
- `projects/domainspec-v2/README.md`

Source-backed findings:

- `.arcanum/inventory/schema.md` states the authority rule: raw files are source
  evidence; inventory pages are read models; material claims need source refs or
  explicit inference/synthesis/open-question labels.
- `.arcanum/inventory/index.md` and `log.md` showed the missing layer before
  this run: no cartographer receipts, no selector-level evidence cards, and no
  EvidenceSets.
- `.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md` is path-level,
  candidate-only, and explicitly not a promotion authority.
- `.arcanum/observability/` defines an operational feedback/control loop:
  central ledger, per-sigil indexes, thresholds, and reflection state.
- `.arcanum/necronomicon/` preserves the no-promotion guardrail around memory,
  sessions, inventory, and owner handoff.
- Ontologize definitions and operational ontology branches prove the repo
  already separates definitions authority from operational ontology candidates.

Candidate cards:

- `knowledge-governance-source-inventory-ontology-control-loop`
- `knowledge-governance-inventory-authority-contract`
- `knowledge-governance-observability-control-loop`
- `knowledge-governance-necronomicon-memory-boundary`
- `knowledge-governance-operational-branch-reframing`

Contradictions and residue:

- `arcanum/.craft/ledger.yml` references at least one dispatch artifact path
  not observed by the cartographer in the current listing.
- `.arcanum/observability` and `arcanum/.craft` are both trace/control surfaces,
  but they are not the same control plane.
- Ontology condensation was ahead of evidence-card granularity; this artifact
  begins to close that gap without promoting the map.
