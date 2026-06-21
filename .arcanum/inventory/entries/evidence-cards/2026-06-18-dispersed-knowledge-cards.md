---
tags: [inventory, dispersed-knowledge, cartography, reuse-map, promotion-guardrail, public-private-boundary, knowledge-system, contradiction]
node_type: evidence-card
is_session: false
layer: architecture
nature: reference
status: candidate
created: 2026-06-18
dispatch_id: 2026-06-18-dispersed-knowledge-cartography
dispatch_type: research
working_folder: .arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/
sources: [.arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/cartographer-receipts.md, arcanum/, implementation/domainspec/, validation/poker-team/, projects/, cyberAlchemy/, .arcanum/]
---

# Evidence Cards - Dispersed Knowledge

Each card is a candidate read model. Promotion requires the named owner or a
downstream governed route.

## `arcanum-registry-catalog`

- ID: `arcanum-registry-catalog`
- Status: candidate
- Claim or candidate: Synthesis from sampled Arcanum sources: `arcanum/registry/`
  is a catalog/index layer, while capability and spell packages carry the
  richer contract material.
- Source refs: `arcanum/registry/README.md`, `arcanum/registry/SIGILS.md`,
  `arcanum/registry/SPELLS.md`, `arcanum/registry/PACKS.md`,
  `arcanum/arcana/task-session/README.md`, `arcanum/spells/README.md`
- Authority level: source-backed synthesis from Arcanum cartographer receipt
- Promotion owner: Arcanum registry/capability owner
- Trace: `cartographer-arcanum-capabilities`
- Residue: Need full canonical-source crosswalk before a generated catalog is
  promoted.

## `arcanum-runtime-projection-surfaces`

- ID: `arcanum-runtime-projection-surfaces`
- Status: candidate
- Claim or candidate: Synthesis from sampled projection surfaces: generated or
  compatibility surfaces should point back to canonical sources and preserve
  mutation policy.
- Source refs: `.agents/skills/arcanum-bootstrap/SKILL.md`,
  `.agents/skills/refine/SKILL.md`, `.claude/skills/arcanum-bootstrap/SKILL.md`,
  `.github/skills/README.md`,
  `.github/skills/arcanum-spell-arcanum-bootstrap/SKILL.md`,
  `.codex/commands/arcanum-bootstrap.md`, `.codex/commands/task-session.md`,
  `arcanum/arcana/sigil-runtime-installer/SKILL.md`,
  `arcanum/tools/bootstrap_arcanum.sh`
- Authority level: source-backed synthesis from Arcanum cartographer receipt
- Promotion owner: Arcanum runtime/projection owner
- Trace: `cartographer-arcanum-capabilities`
- Residue: Generated host surfaces are broad; representative sampling supports
  the rule, not every projection instance.

## `arcanum-task-session-runtime-boundary`

- ID: `arcanum-task-session-runtime-boundary`
- Status: candidate
- Claim or candidate: Task Session owns bounded task coordination, while
  runtime adapters own execution handoff and host-specific bridges.
- Source refs: `arcanum/arcana/task-session/README.md`,
  `arcanum/arcana/task-session/SKILL.md`,
  `arcanum/arcana/task-session/runtime-adapters/README.md`,
  `arcanum/arcana/task-session/runtime-adapters/codex-goal.md`,
  `arcanum/arcana/task-session/runtime-adapters/runtime-handoff.md`,
  `arcanum/framework/runtime/README.md`,
  `arcanum/framework/runtime/adapters/local-skill.md`,
  `arcanum/framework/runtime/adapters/codex-exec.md`
- Authority level: source-backed synthesis from Arcanum cartographer receipt
- Promotion owner: Arcanum task-session/runtime owner
- Trace: `cartographer-arcanum-capabilities`
- Residue: Needs alignment with current generated runtime skill projections.

## `domainspec-private-boundary-submodule-discipline`

- ID: `domainspec-private-boundary-submodule-discipline`
- Status: candidate
- Claim or candidate: The private parent composes public Arcanum, private
  implementation, and validation submodules under submodule-first publish rules.
- Source refs: `AGENTS.md`, `CLAUDE.md`, `SUBMODULE-DISCIPLINE.md`, `.gitmodules`
- Authority level: source-backed policy evidence
- Promotion owner: private DomainSpec repo owner
- Trace: `cartographer-domainspec-private`
- Residue: Public-safe derivative wording must be scrubbed before any public
  artifact uses this card.

## `domainspec-governance-registry-observability-spine`

- ID: `domainspec-governance-registry-observability-spine`
- Status: candidate
- Claim or candidate: Private DomainSpec has a computable spine across axioms,
  constitution, governance-chain validation, registry/code binding, orphan
  detection, and observability signal loops.
- Source refs: `implementation/domainspec/AXIOMS.md`,
  `implementation/domainspec/CONSTITUTION.md`,
  `implementation/domainspec/tools/validate-governance-chain.ts`,
  `implementation/domainspec/tools/generate-registry.ts`,
  `implementation/domainspec/tools/validate-orphans.ts`,
  `implementation/domainspec/OBSERVABILITY.md`
- Authority level: private source-backed synthesis
- Promotion owner: private DomainSpec implementation owner
- Trace: `cartographer-domainspec-private`
- Residue: Keep private implementation evidence out of public Arcanum until a
  separate public-safe pattern extraction route exists.

## `pokerteam-feature-pack-validation-harness`

- ID: `pokerteam-feature-pack-validation-harness`
- Status: candidate
- Claim or candidate: `validation/poker-team` demonstrates a reusable feature
  pack shape: registry, feature map, governance baseline, signals, pipeline
  reports, alignment reports, and feature-specific decisions.
- Source refs: `validation/poker-team/docs/registry.md`,
  `validation/poker-team/docs/index/feature-map.md`,
  `validation/poker-team/docs/shared/governance-baseline.md`,
  `validation/poker-team/docs/signals/META-HEALTH.md`,
  `validation/poker-team/docs/features/auth-access-control/PIPELINE-REPORT.md`,
  `validation/poker-team/docs/features/auth-access-control/LAYERING-ALIGNMENT-REPORT.md`,
  `validation/poker-team/docs/features/player-onboarding/PILOT-DECISIONS.md`,
  `validation/poker-team/docs/features/player-management/PIPELINE-REPORT.md`
- Authority level: private validation source-backed synthesis
- Promotion owner: validation/poker-team owner
- Trace: `cartographer-domainspec-private`
- Residue: Some signal snapshots are dated and need refresh before quantitative
  claims are reused.

## `sessions-decision-archaeology`

- ID: `sessions-decision-archaeology`
- Status: candidate
- Claim or candidate: Selected session files capture durable decision and
  residue history that should be mined as evidence, not treated as canonical docs.
- Source refs: `sessions/2026-06-15-1723-subagents-strategy-arcanum-wiring.md`,
  `sessions/2026-06-16-1440-subagents-skills-consolidation.md`,
  `sessions/2026-06-17-1354-edge-constitution-and-review-dispatches.md`,
  `sessions/2026-06-17-1357-specs-development-review-wiring.md`
- Authority level: session evidence, low-to-medium confidence until promoted
- Promotion owner: decision-gate or definitions/governance owner
- Trace: `cartographer-domainspec-private`
- Residue: Needs a formal archaeology route before being moved into authority.

## `cyberalchemy-inventory-ontology-loop`

- ID: `cyberalchemy-inventory-ontology-loop`
- Status: candidate
- Claim or candidate: CyberAlchemy describes a source -> inventory -> ontology
  -> context -> execution -> telemetry/reflection knowledge loop.
- Source refs: `cyberAlchemy/agentic-system-inventory-ontology-pipeline.md`,
  `cyberAlchemy/README.md`, `cyberAlchemy/agentic-system-first-working-slice.md`
- Authority level: research/program synthesis
- Promotion owner: CyberAlchemy/project research owner
- Trace: `cartographer-project-research`, `cartographer-knowledge-governance`
- Residue: Several CyberAlchemy artifacts are candidate-stage and need owner
  review before becoming canonical method.

## `cyberalchemy-thick-ontology-entry-contract`

- ID: `cyberalchemy-thick-ontology-entry-contract`
- Status: candidate
- Claim or candidate: CyberAlchemy's ontology entry model gives a reusable card
  shape for identity, content, context, agent payload, edges, evidence,
  confidence, promotion, and maintenance.
- Source refs: `cyberAlchemy/agentic-system-ontology-entry-model.md`,
  `cyberAlchemy/ontology/source-ledger.md`
- Authority level: research/program synthesis
- Promotion owner: ontology-vault or CyberAlchemy owner
- Trace: `cartographer-project-research`
- Residue: Should inform inventory schema only after selector-level cards prove
  enough repeated use.

## `framework-unification-two-axis-model`

- ID: `framework-unification-two-axis-model`
- Status: candidate
- Claim or candidate: Framework Unification supplies a two-axis architecture
  pattern: horizontal pipeline plus vertical mechanisms with single-owner
  invariants.
- Source refs: `projects/framework-unification/CONCEPT-MAP.md`,
  `projects/framework-unification/components/ARTIFACTS.md`
- Authority level: research synthesis
- Promotion owner: framework-unification owner
- Trace: `cartographer-project-research`
- Residue: Do not confuse tier labels, mechanisms, and pipeline stages.

## `ontologize-l0-l1-l2-research-product-tower`

- ID: `ontologize-l0-l1-l2-research-product-tower`
- Status: candidate
- Claim or candidate: Ontologize provides a reusable tower progression from L0
  corpus to L1 reusable patterns to L2 product closure, including a public
  offering derivative.
- Source refs: `projects/ontologize/TOWER.md`,
  `projects/ontologize/levels/L0-corpus.md`,
  `projects/ontologize/levels/L1-pattern-map.md`,
  `projects/ontologize/levels/L2-product-closure-plan.md`,
  `projects/ontologize/PUBLIC-OFFERING.md`
- Authority level: research/product synthesis
- Promotion owner: Ontologize project owner
- Trace: `cartographer-project-research`
- Residue: Keep public offering language separate from internal residue.

## `domainspec-v2-research-tower-discipline`

- ID: `domainspec-v2-research-tower-discipline`
- Status: candidate
- Claim or candidate: `projects/domainspec-v2` is research-gated and
  pre-implementation, with tower-local artifacts and two-lane discipline.
- Source refs: `projects/domainspec-v2/README.md`,
  `projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md`,
  `projects/domainspec-v2/research/alloy-tla-modeling/TOWER.md`,
  `projects/domainspec-v2/research/alloy-tla-modeling/BRIDGE-DECISIONS.md`,
  `projects/domainspec-v2/research/dcb-correctness/RESEARCH-STRATEGY.md`,
  `projects/domainspec-v2/research/dcb-saga-correctness/SYNTHESIS.md`,
  `projects/domainspec-v2/research/intent-tags/FINDINGS.md`
- Authority level: project research evidence
- Promotion owner: DomainSpec v2 owner
- Trace: `cartographer-project-research`, `cartographer-knowledge-governance`
- Residue: Still needs owner decisions before becoming a standalone repo
  architecture decision.

## `arcanum-observability-reflection-loop`

- ID: `arcanum-observability-reflection-loop`
- Status: candidate
- Claim or candidate: Synthesis from Arcanum sources: observed invocation,
  workflow reflection, and runtime handoff treat telemetry as maintenance
  evidence.
- Source refs: `arcanum/spells/observed-invocation-loop/README.md`,
  `arcanum/arcana/workflow-reflect/SKILL.md`,
  `arcanum/framework/runtime/README.md`
- Authority level: source-backed synthesis from Arcanum cartographer receipt
- Promotion owner: Arcanum observability/runtime owner
- Trace: `cartographer-arcanum-capabilities`
- Residue: Telemetry can evidence behavior; it does not define semantic
  authority.

## `arcanum-authoring-front-door`

- ID: `arcanum-authoring-front-door`
- Status: candidate
- Claim or candidate: Invoke and Refine are authoring/front-door capabilities
  for define/design/plan/handoff work rather than execution authority.
- Source refs: `arcanum/spells/invoke/README.md`,
  `arcanum/spells/invoke/define.md`, `arcanum/spells/invoke/design.md`,
  `arcanum/spells/invoke/plan.md`, `arcanum/arcana/refine/SKILL.md`
- Authority level: source-backed synthesis from Arcanum cartographer receipt
- Promotion owner: Arcanum authoring capability owner
- Trace: `cartographer-arcanum-capabilities`
- Residue: Must stay distinct from task-session execution.

## `knowledge-governance-inventory-authority-contract`

- ID: `knowledge-governance-inventory-authority-contract`
- Status: candidate
- Claim or candidate: Inventory pages are read models; material claims need
  source refs or explicit inference/synthesis/open-question labels.
- Source refs: `.arcanum/inventory/schema.md`,
  `.arcanum/inventory/index.md`, `.arcanum/inventory/log.md`,
  `.arcanum/inventory/entries/source-systems.md`
- Authority level: local inventory package rule
- Promotion owner: inventory owner
- Trace: `cartographer-knowledge-governance`, `boundary_skeptic`
- Residue: Existing cards still require periodic selector linting as they grow.

## `knowledge-governance-ontology-candidate-boundary`

- ID: `knowledge-governance-ontology-candidate-boundary`
- Status: candidate
- Claim or candidate: Ontology-vault may classify and condense candidate
  meaning, but it does not promote inventory, definitions, glossaries, sigils,
  spells, or runtime contracts.
- Source refs: `.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md`,
  `.agents/skills/ontology-vault/SKILL.md`, `.arcanum/inventory/schema.md`
- Authority level: candidate ontology-vault boundary rule
- Promotion owner: ontology-vault plus downstream governance owner
- Trace: `cartographer-knowledge-governance`, `boundary_skeptic`
- Residue: Claim-level branch mapping is still candidate and needs owner review.

## `knowledge-governance-observability-control-loop`

- ID: `knowledge-governance-observability-control-loop`
- Status: candidate
- Claim or candidate: `.arcanum/observability/` is an operational feedback loop
  with central signals, per-sigil indexes, configuration, and reflection state.
- Source refs: `.arcanum/observability/README.md`,
  `.arcanum/observability/config.json`,
  `.arcanum/observability/reflection-state.json`,
  `.arcanum/observability/signals/sigil-invocations.jsonl`
- Authority level: observability evidence, not meaning authority
- Promotion owner: observability owner
- Trace: `cartographer-knowledge-governance`
- Residue: JSONL signals need separate review before quantitative claims.

## `knowledge-governance-necronomicon-memory-boundary`

- ID: `knowledge-governance-necronomicon-memory-boundary`
- Status: candidate
- Claim or candidate: Necronomicon memory state is a governed knowledge
  substrate with no-promotion guardrails and owner handoff.
- Source refs: `.arcanum/necronomicon/README.md`,
  `.arcanum/necronomicon/capabilities.json`
- Authority level: local knowledge harness evidence
- Promotion owner: Necronomicon/knowledge harness owner
- Trace: `cartographer-knowledge-governance`
- Residue: Memory/session evidence stays evidence until separately promoted.

## `knowledge-governance-operational-branch-reframing`

- ID: `knowledge-governance-operational-branch-reframing`
- Status: candidate
- Claim or candidate: Ontologize operational ontology treats disciplines as
  inputs to an operational constitution/axiom route, not as axiom-level
  authority by themselves.
- Source refs: `projects/ontologize/operational-ontology/README.md`,
  `projects/ontologize/operational-ontology/HYPOTHESIS.md`,
  `projects/ontologize/operational-ontology/TOWER.md`,
  `projects/ontologize/operational-ontology/NEXT.md`,
  `projects/ontologize/operational-ontology/levels/L1-authority-map.md`,
  `projects/ontologize/operational-ontology/decisions/disciplines-as-axiom.md`
- Authority level: project ontology branch evidence
- Promotion owner: Ontologize operational ontology owner
- Trace: `cartographer-knowledge-governance`
- Residue: Branch remains candidate pending ontology-harness review.

## `contradiction-domainspec-architecture-stub-target`

- ID: `contradiction-domainspec-architecture-stub-target`
- Status: contradiction
- Claim or candidate: `implementation/domainspec/ARCHITECTURE.md` is a
  compatibility stub that points at `architecture/ARCHITECTURE.md`, but that
  target was not observed in this checkout by the cartographer.
- Source refs: `implementation/domainspec/ARCHITECTURE.md`,
  `.arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/cartographer-receipts.md`
- Authority level: contradiction/residue
- Promotion owner: private DomainSpec implementation owner
- Trace: `cartographer-domainspec-private`, `boundary_skeptic`
- Residue: Verify whether the target is absent, generated elsewhere, or omitted
  by checkout state before using the stub as architecture evidence.

## `contradiction-dispatch-telemetry-authority-split`

- ID: `contradiction-dispatch-telemetry-authority-split`
- Status: contradiction
- Claim or candidate: Parent `telemetry/agents/subagents-dispatch.yaml` and
  submodule dispatch/agent-pool files are distinct but similarly named
  surfaces; inventory must keep selectors repo-scoped.
- Source refs: `telemetry/agents/subagents-dispatch.yaml`,
  `implementation/domainspec/telemetry/agents/subagents-dispatch.yaml`,
  `implementation/domainspec/telemetry/agents/agent-pool.yaml`,
  `.arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/cartographer-receipts.md`
- Authority level: contradiction/residue
- Promotion owner: parent repo and private DomainSpec implementation owners
- Trace: `cartographer-domainspec-private`, `boundary_skeptic`
- Residue: Add explicit alias/selector conventions before broad dispatch
  telemetry lookup is automated.

## `knowledge-governance-source-inventory-ontology-control-loop`

- ID: `knowledge-governance-source-inventory-ontology-control-loop`
- Status: candidate
- Claim or candidate: Cross-lane synthesis only: the repo repeats a pattern of
  source evidence -> inventory read model -> ontology candidate map -> owner-gated
  promotion -> observability/reflection. The separate boundary cards above own
  the individual authority surfaces.
- Source refs: `.arcanum/inventory/schema.md`,
  `.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md`,
  `.arcanum/observability/README.md`, `.arcanum/necronomicon/README.md`,
  `cyberAlchemy/agentic-system-inventory-ontology-pipeline.md`
- Authority level: cross-lane synthesis
- Promotion owner: inventory plus ontology-vault plus downstream governance owner
- Trace: `cartographer-knowledge-governance`
- Residue: Needs claim-level branch mapping and owner promotion decisions.
