# DomainSpec Core Root Coverage Research

Dispatch: `2026-06-19-domainspec-core-root-coverage`

Purpose: inspect root-level DomainSpec Core surfaces outside the previously reviewed
`implementation/domainspec/` subtree and identify evidence-backed achievements that can
support a shareable system-theory account without overclaiming implementation closure.

## Public Export And Runtime Projection Lane

Inspected surfaces: `.gitmodules`; `arcanum/README.md`; `arcanum/CLAUDE.md`;
`arcanum/arcana/README.md`; `arcanum/transmutations/README.md`;
`arcanum/.agents/README.md`; `arcanum/.github/workflows/claude-skills.yml`;
`arcanum/.github/workflows/pages.yml`; `arcanum/.arcanum/runtime/config.json`;
`arcanum/.arcanum/observability/README.md`; `arcanum/.arcanum/necronomicon/README.md`;
sampled root generated runtime packages under `.agents/skills/`, `.claude/skills/`,
root `.codex/commands/invoke.md`, `.codex/commands/dispatch-spec.md`,
`.codex/hooks.json`, `.arcanum/runtime/`, `.arcanum/observability/`,
`.arcanum/inventory/`, `.arcanum/necronomicon/`, `.arcanum/profiles/`, and
`.claude/worktrees/codex+infra-spec/README.md`.

Evidence-backed achievements:

- Arcanum is already presented as a public-shareable capability framework with
  canonical tiers, lifecycle, registry, observability, and installation story through
  `arcanum/README.md`, `arcanum/arcana/README.md`, and
  `arcanum/transmutations/README.md`. This is actual public packaging plus working
  framework structure.
- The export model is a multi-runtime projection system rather than one prompt surface.
  Root `.arcanum/runtime/config.json` enables adapters such as `native-skill`,
  `codex-skill`, `claude-skill`, `copilot-instructions`, `local-skill`, `codex-exec`,
  `codex-bypass`, and `dry-run`; adapter profiles define handoff and receipt semantics.
- Generated runtime mirrors exist for Codex and Claude. Sampled `.agents/skills/*` and
  `.claude/skills/*` headers identify the surfaces as generated native runtime packages,
  name their generator profile, and define regeneration rather than direct mutation as
  the policy.
- `.codex/commands/invoke.md` and `.codex/commands/dispatch-spec.md` provide legacy
  compatibility command adapters while `arcanum/README.md` demotes `.codex/commands/`
  from canonical status.
- Public packaging has automation support: `arcanum/.github/workflows/claude-skills.yml`
  regenerates a throwaway Claude skill surface and validates it, while
  `arcanum/.github/workflows/pages.yml` deploys public docs.
- Local evidence packages are separated from canonical capability definitions:
  `.arcanum/observability/README.md` treats runs and reflections as telemetry,
  `.arcanum/inventory/README.md` says inventory does not replace canonical sources, and
  `.arcanum/necronomicon/README.md` says harness state is not a copied definition store.
- `.arcanum/observability/runs/craft-feature-readiness-indexes-20260614T201013Z.json`
  records a real run with outputs, validations, flags, and observer recommendations.
- `.arcanum/profiles/decision-profile.yml` explicitly keeps filled decision profiles
  private in `.arcanum/` while public `arcanum` carries only schema/default material.
- `.arcanum/inventory/entries/source-systems.md`,
  `.arcanum/inventory/wiki/repository-map.md`, and
  `.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md` describe the umbrella
  as composed surfaces, but they are candidate read models rather than canonical authority.

System-theory relevance:

- Boundary discipline is strong: canonical capability source (`arcanum/arcana`,
  `transmutations`, `formulae`, `spells`) is separated from generated runtime projection
  (`.agents/skills`, `.claude/skills`, `.codex/commands`) and local evidence state
  (`.arcanum/observability`, `.arcanum/necronomicon`, `.arcanum/inventory`).
- Interface discipline is explicit: `.arcanum/runtime/adapters/*.json` define execution
  interfaces, isolation model, limitations, and validation surface.
- Feedback is present through invocation ledgers and reflection paths in Arcanum
  observability, hooks, and local `.arcanum` state.
- Governance is distributed through capabilities such as `invoke`, `dispatch-spec`, and
  `task-session`, plus stage-worker instructions, instead of being collapsed into one
  actor.
- Open-system composition is visible in `.gitmodules` and the inventory/ontology read
  models: public Arcanum, private implementation, validation harnesses, and local runtime
  overlays compose in the private umbrella.

Boundary risks and demotions:

- `.arcanum/profiles/decision-profile.yml`, `.claude/settings.json`,
  `.claude/worktrees/codex+infra-spec/README.md`, root `.arcanum/inventory/**`,
  `.arcanum/ontology-vault/**`, and `.arcanum/observability/runs/**` are not safe for
  wholesale publication.
- `arcanum/.arcanum/*` and root `.arcanum/*` are local runtime state packages; they should
  be regenerated in target repositories rather than copied blindly.
- `arcanum/README.md` describes `.agents/skills/` as symlinked, but this checkout has
  materialized directories. Treat that as documented model, not current local fact.
- The inspected evidence supports "implemented public framework plus generated runtime
  projections plus local evidence packages"; it does not support saying the whole umbrella
  is already a cleanly publishable product.

## Governance And Control Lane

Inspected surfaces: `AGENTS.md`, `CLAUDE.md`, `SUBMODULE-DISCIPLINE.md`, `Makefile`,
`.gitmodules`, `telemetry/agents/subagents-dispatch.yaml`,
`internal_tools/subagents-dispatch-hooks/**`, `.arcanum/observability/README.md`,
`.arcanum/observability/config.json`, `.arcanum/runtime/config.json`,
`.arcanum/runtime/adapters/**`, `tools/arcanum`, `tools/guard`, `tools/guard-shell`,
`tools/terminal_guard.sh`, `tools/check_research_structure.sh`,
`tools/check_skill_agent_surface_drift.py`, `.formal-tools/**`, and related project-local
toolchain receipts under
`projects/domainspec-v2/research/alloy-tla-modeling/invoke-plan/run-results/toolchain/**`.

Evidence-backed achievements:

- A real append-only dispatch governance mechanism exists through
  `internal_tools/subagents-dispatch-hooks/hooks/enforce-append-only-dispatch.cjs`,
  `internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs`,
  and `telemetry/agents/subagents-dispatch.yaml`.
- The dispatch ledger is typed and lifecycle-aware. `register-dispatch/SKILL.md`,
  `docs/LEDGER-MODEL.md`, and the ledger distinguish dispatch rows from close rows and
  preserve outcome metadata such as `exit_reason`, `agents_spawned`, and
  `feedback_prompts`.
- `internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs` and the
  appender implement strict incoming schema validation, grandfathering for historical
  rows, idempotency, and corruption checks.
- `internal_tools/subagents-dispatch-hooks/README.md`,
  `constitution/subagents-strategy-constitution-proposal.md`, and the router/type/form
  skill split separate strategic routing, type judgment, and form validation.
- `hooks/block-workflow.cjs` and `hooks/enforce-append-only-dispatch.cjs` attenuate
  uncontrolled workflow variety by blocking one orchestration channel and narrowing
  ledger writes to the appender.
- `tools/guard`, `tools/guard-shell`, and `tools/terminal_guard.sh` provide bounded shell
  execution with timeout, retry, risk nudges, and JSONL telemetry to
  `docs/signals/terminal-guard.jsonl`.
- `tools/arcanum`, `.arcanum/observability/config.json`, `.arcanum/runtime/config.json`,
  and `.arcanum/runtime/adapters/**` provide invocation envelopes and optional reflection
  paths.
- `SUBMODULE-DISCIPLINE.md`, `Makefile`, `.gitmodules`, and `CLAUDE.md` make submodule
  governance concrete. `make bump-check` delegates to `git push --recurse-submodules=check
  --dry-run`; `make doctor` checks detached heads, dirty submodules, and orphaned gitlinks.
- `tools/check_research_structure.sh` checks required research file sets, manifest
  references, required README sections, dependency manifest keys, and compatibility alias
  drift.
- `.formal-tools/` contains provisioned formal tools, with stronger evidence of use in
  project-local receipts such as
  `projects/domainspec-v2/research/alloy-tla-modeling/invoke-plan/run-results/toolchain/toolchain-receipt.md`.

System-theory relevance:

- The root uses multiple controllers for distinct disturbances: git/submodule gates,
  dispatch registration, append-only enforcement, terminal guard, research-structure
  validation, and runtime adapter selection.
- Attenuation is strongest where the system forbids or narrows action spaces:
  `block-workflow.cjs`, append-only ledger hooks, and submodule push discipline.
- Dispatch metadata amplifies otherwise ephemeral reasoning by preserving goals, context,
  tension axes, agent angles, and closeout reasons.
- Observability is split by plane: command/runtime observability, dispatch/governance
  observability, and shell behavior telemetry.
- Some loops are genuinely closed: submodule bump checks, close-row ledger completion, and
  ledger corruption surfacing on next write. Others are only partially closed and depend on
  human confirmation, reminder hooks, or optional observer availability.

Boundary risks and demotions:

- `telemetry/agents/subagents-dispatch.yaml` is private governance trace, not a public-safe
  artifact. It can contain identifying fields, prompt bodies, and non-public path context.
- `internal_tools/subagents-dispatch-hooks/README.md` warns that copied skills carry
  repo-relative references and need rebasing.
- `.formal-tools/` is best described as a provisioned local tool cache with project-local
  receipts of use, not a root-level integrated formal-methods subsystem.
- Do not claim a completed self-regulating control system or unified compulsory
  observability plane. The root shows strong prerequisites and selected closed loops.

## Product, Dogfood, And Validation Lane

Inspected surfaces: `projects/ontologize/**`, `projects/autoads/**`,
`projects/ui-prototyping-studio/**`, `projects/whisky-doses/**`, `projects/body-war/**`,
`cyberAlchemy/**`, `cyberAlchemy-v2/**`, and `validation/poker-team/**`. No
`dogfood/application/**` files were found in this checkout.

Evidence-backed achievements:

- `projects/ontologize/dogfood/cyberalchemy-lead-evidence-pilot/DOGFOOD-PILOT.md`,
  `SCORECARD-SPEC.md`, `RESULTS.md`, `CHANNEL-BRIEFS.md`, and `OFFER-MAP.md` define an
  internal dogfood lane that narrows the work to one offer, one conversion event, one
  channel path, one scorecard, and one owner decision. This is a dogfood plan and evidence
  object, not proof of market validation.
- `projects/ontologize/PRODUCT.md`, `PUBLIC-OFFERING.md`, `deliverable/README.md`,
  `deliverable/*`, and `decisions/pilot-and-positioning.md` separate internal doctrine,
  public-safe offer copy, client-sendable package template, and decisions. `PRODUCT.md`
  tags claims as proven or hypothesis, and the deliverable package includes gap sections.
- `projects/ontologize/research/2026-06-18-cyberalchemy-integration-first-sale/findings.md`
  demotes "first product" rhetoric into a narrower Metric Trust Sprint readiness test.
- `cyberAlchemy/README.md`, `cyberAlchemy/agentic-system/README.md`, and
  `cyberAlchemy/agentic-system-first-working-slice.md` decompose a large method into
  inventory, ontology entry contract, promotion governance, operational ontology,
  memory/context, execution feedback, and a first working loop from source to telemetry.
- `cyberAlchemy/research/2026-06-18-product-architecture-wedge-moat/findings.md` treats
  CyberAlchemy as a candidate planning corpus, not a market-proven product or accepted moat,
  and names a required first proof slice.
- `cyberAlchemy-v2/README.md`, `SOURCE-MAP.md`, `authority/boundaries.md`, and
  `authority/**` stage a consolidation surface that separates source evidence, imports,
  local authority, specs, implementation, validation, observability, and ops before any
  extraction into a stable repo.
- `validation/poker-team/README.md`, `onboarding.html`, `recruitment_game/**`,
  `backend/src/domain/player/*.ts`, `backend/src/domain/player/*.test.ts`, and `infra/**`
  show the most concrete operational validation surface in this lane: recruiting flow,
  domain logic, tests, and infrastructure scaffolding.
- `projects/ui-prototyping-studio/README.md` and `SPEC.md` describe a governed UI
  exploration workflow with generated variants, baseline selection, annotation,
  synthesis, approval, application, acceptance, reversion, handoff export, and tests.
- `projects/whisky-doses/domainspec/**` and `projects/whisky-doses/docs/PLAN.md` show a
  reusable DomainSpec runtime/reference bundle and an ordered plan that turns feature
  packages into stories and UI contracts.
- `projects/body-war/README.md` provides a discovery baseline for a game idea, with
  definitions, decisions, hypotheses, experiment candidates, and a first feature slice.

System-theory relevance:

- Bounded rationality appears as repeated narrowing into one inspectable loop: one metric,
  one workflow, one scorecard, one owner decision, one proof slice.
- Decomposition is visible in CyberAlchemy, CyberAlchemy v2, and Whisky Doses surfaces,
  which split sprawling ideas into planes, slices, and ordered artifacts.
- Pilot/product feedback is explicitly demoted into reviewable candidates and scorecards
  rather than treated as silent truth.
- Usable control surfaces are strongest in `projects/ui-prototyping-studio` and
  `validation/poker-team`.

Boundary risks and demotions:

- `cyberAlchemy-v2/authority/boundaries.md` correctly warns that private implementation,
  validation, telemetry, sessions, and parent-local research must not leak into public
  derivatives.
- `validation/poker-team/**` is concrete but private-domain validation material, not public
  proof of a method.
- CyberAlchemy should be described as a candidate planning corpus or first-loop substrate
  hypothesis, not a runtime, market-proven product, or accepted moat.
- Ontologize is a candidate first sale/product test, not yet a demonstrated easy-to-sell
  offer.
- `cyberAlchemy-v2` is a staging repository surface, not an extracted stable repo.
- `projects/body-war` is a discovery baseline, not an application prototype.

## Operations, Handoffs, And Recursive Governance Lane

Inspected surfaces: `docs/decisions/*.md`,
`docs/signals/DELEGATION-TUNING.md`, `docs/signals/TERMINAL-GUARD.md`,
`docs/signals/delegation-tuning.jsonl`, `docs/signals/terminal-guard.jsonl`,
`docs/shared/governance-baseline.md`, `ops/*.md`, `ops/development/*.md`,
`ops/development/refinement-runs/20260615T132005Z-goal-spec-architecture-first/RUN-MANIFEST.md`,
`RUNTIME-HANDOFF.md`, `evidence-index.json`,
`ops/development/domainspec-lean-formalization-glossary-refresh/REFRESH-REPORT.md`,
`VALIDATION.md`, `refresh-report.json`, generated output under
`output/research-package-20260616/tests/triton-top2-backward-kernel/**`, and file
inventory under `sessions/`.

Evidence-backed achievements:

- `docs/decisions/native-runtime-skill-surface.md` and
  `docs/decisions/install-profile-contract.md` separate canonical source, native runtime
  packages, deterministic support utilities, and machine-global mutation.
- `docs/decisions/surface-cleanup-blocker-decisions.md` routes cleanup decisions through
  named options, selected policies, assumptions, blockers, and next-route handoff instead
  of ad hoc sweeping.
- `ops/SURFACE-OWNER-BOUNDARIES.md`, `ops/development/DOMAINSPEC-OWNER-HANDOFF.md`, and
  `ops/development/LEAN-FORMALIZATION-OWNER-HANDOFF.md` prevent parent cleanup from
  mutating child-owned runtime surfaces and convert cross-boundary work into owner-scoped
  handoffs.
- `ops/SKILLS-FIRST-RUNTIME-POLICY.md` demotes command wrappers, classifies generated
  state, and defines validation conditions for cleanup.
- `ops/ARCANUM-RUNTIME-SURFACE-REFRESH-REPORT.md` and
  `ops/development/domainspec-lean-formalization-glossary-refresh/refresh-report.json`
  map source signals such as blocker resolution, artifact drift, route change, and evidence
  additions to target artifacts, skipped changes, and next routes.
- `docs/signals/DELEGATION-TUNING.md`, `docs/signals/delegation-tuning.jsonl`,
  `docs/signals/TERMINAL-GUARD.md`, and `docs/signals/terminal-guard.jsonl` provide
  append-only telemetry for delegation and terminal behavior, including started/terminal
  rows, watchdog budgets, reconciliation, stuck detection, and command guarding.
- `ops/development/refinement-runs/20260615T132005Z-goal-spec-architecture-first/` validates
  an architecture-first route, recommends subagents, specifies receipt requirements, and
  leaves stages `not_run` pending operator confirmation.
- `output/research-package-20260616/tests/triton-top2-backward-kernel/TOWER.md` indexes
  corpus, claims, derivation, dispatch, invoke runs, task sessions, blockers, decision
  ledgers, runner plans, and benchmark artifacts.
- `output/.../dispatch-runs/20260612T121416Z-top2-backward-research/CLOSEOUT.md` and
  `execution-index.json` close a dispatch with route execution receipts while keeping
  implementation gated by unresolved semantic choices.
- Task-session artifacts such as
  `output/.../task-sessions/20260612T135008Z-w0-007-cuda-runner-selection/DECISION-GATE.md`,
  `output/.../task-sessions/20260615T043200Z-sys-001-cap2-allocation/RESULT.md`, and
  `output/.../artifacts/BENCHMARK.md` record blocked execution, local validation success,
  remote-runner failure, bundles produced, and bounded benchmark evidence without inflating
  those into production claims.

System-theory relevance:

- The root shows recursive control layers: root policy governs subrepos and runtime
  surfaces while owner-boundary documents preserve subsystem autonomy.
- Governance loops are explicit where signal becomes refresh report, scoped mutation or
  no-op, validation, and next route.
- Identity and policy boundaries are encoded in install profiles, owner maps, mutation
  policies, and explicit exclusions for machine-global state or submodule-owned state.
- Feedback appears in observability ledgers and decision/validation receipts.
- Operational closure is partial. The system can close many documentary and governance
  loops internally, but execution still depends on operator confirmation, external hosts,
  build repair, and owner-scoped downstream cleanup.

Boundary risks and demotions:

- `ops/development/domainspec-arcanum-build-decisions.md` shows the need for sanitization
  audits, private-term stripping, and conservative defaults for ambiguous capability
  families.
- `docs/decisions/personal-codex-skill-refresh.md` confirms some flows mutate
  machine-global runtime state; do not describe every flow as repo-local.
- `output/research-package-20260616.tar.gz` and generated `output/` trees need careful
  classification before public use.
- Architecture-first route validation is a prepared control loop, not an executed one.
- Triton output shows disciplined progress but keeps CUDA execution, semantic choices, and
  remote-runner continuity unresolved.
- The strongest evidence is governed recursion: stop, hand off, demote claims, preserve
  residue, and re-enter with receipts.

## Formalization And Research Lane

Inspected surfaces: `domainspec-formalization/README.md`,
`domainspec-formalization/docs/**`, `domainspec-formalization/lean-formalization/**`,
`domainspec-lean-formalization/README.md`, `LEAN-ARCHITECTURE.md`, `THERMODYNAMICS.md`,
`docs/**`, `essays/**`, `experiments/**`, `lean-formalization/**`, `research/**`,
`research-bridges/**`, `research-emergence/**`, `research-physics/**`,
`research/tower-system-taxonomy/research.md`, `refs/meta-camadas.md`, and relevant
`docs/features/**` term scans.

Evidence-backed achievements:

- `domainspec-formalization/docs/domainspec-two-layer-framework.md` and
  `domainspec-formalization/lean-formalization/DomainSpec.lean` define a two-layer residue
  split between schema-level and instance-level leakage, with free instance-level Kan
  machinery and conditional schema-level adjunction.
- `domainspec-formalization/README.md` and `domainspec-formalization/docs/paper.md` mark
  the theorem project as conjectural while still claiming Lean-backed refutations and
  counterexamples such as `M2Counter.lean`, `M6Counter.lean`, `S2VsS3Counter.lean`, and
  `CounitCounter.lean`.
- `domainspec-lean-formalization/LEAN-ARCHITECTURE.md` maps what is closed versus
  aspirational, including finite/discrete thermodynamic witnesses, counterexample
  discipline, statement-only adjunctions, and naming ambiguity around residue.
- `domainspec-lean-formalization/lean-formalization/SchemaInstance.lean`,
  `DomainSpec.lean`, and `DomainSpecSystem.lean` connect schema/instance typing, the
  spec-to-system layer, and first-class system packaging.
- `domainspec-lean-formalization/lean-formalization/SecondLawDiscrete.lean`,
  `THERMODYNAMICS.md`, and
  `research-physics/strategy/discrete-tier1-attack.md` contain finite/discrete
  thermodynamics work: monotonicity of `log |noise|`, plateau results, residue/entropy
  profiles, and explicit refusal to overclaim continuous renormalization-group or full
  physical second-law closure.
- `domainspec-lean-formalization/docs/emergence-as-asymmetric-dependence.md`,
  `docs/regimes-of-residue.md`, and `research-emergence/README.md` treat emergence as
  asymmetric dependence and multi-level stratification, mostly as a structured research
  program rather than a closed theorem surface.
- `domainspec-lean-formalization/experiments/pockets-as-noether/synthesis.md`,
  `docs/essays/domainspec-thermodynamics.md`, and `research-physics/README.md` bridge
  residue, entropy, Noether-like readings, and physical interpretation while preserving
  anti-claims.
- `domainspec-formalization/docs/domainspec-paper.md` and `refs/meta-camadas.md` frame
  DomainSpec as a layered self-regulating system with feedback arrows, governance
  attenuation, observer/executor separation, bounded strange loops, Shannon/Ashby
  references, and deterministic derivation claims.

System-theory relevance:

- Dynamics are present mostly through discrete/categorical formalization and finite
  thermodynamics, not classic Forrester stock-and-flow modeling.
- Formalization is high relative to the rest of the corpus: adjunctions, counterexamples,
  residue structures, schema/instance typing, and finite second-law-like results.
- Feedback is conceptually present in `refs/meta-camadas.md` and the paper surfaces, but
  reads more like architectural cybernetics/control vocabulary than explicit
  system-dynamics lineage.
- Emergence is active but not closed. The corpus distinguishes multi-level description from
  full Lean encodability.
- Residue is the most mature connective concept across translation, entropy, emergence,
  and observer/system relations.
- Constraint discipline is strong: counterexamples, status labels, anti-claims, and closure
  vocabularies are explicit.

Boundary risks and demotions:

- `domainspec-formalization/docs/domainspec-paper.md` makes strong production-validation
  claims around a production system, test obligations, observability metrics, domain
  concepts, and replication package. Treat those as paper-surface claims unless separately
  verified.
- Research-physics and research-emergence surfaces are safest when described as bridge
  programs or disciplined tracks, not settled contributions to physics or emergence theory.
- Soften any claim that DomainSpec is already a Forrester-style system-dynamics
  contribution.
- Soften "formal model of governance attenuation" to "architectural or analytical theory
  with partial evidence."
- Soften "validated on a production system" to "presented with case-study and replication
  claims in the paper surface."
- Soften "Noether/thermodynamics/physics bridge" to finite/discrete categorical
  thermodynamics plus active bridge program.
- Soften "emergence is formalized" to emergence has a structured research corpus and some
  theorem-adjacent framing, but not a closed formal theory.
- The strongest root-level thesis is disciplined convergence across categorical translation
  theory, residue accounting, finite discrete thermodynamics, and layered governance/control
  motifs, not a finished unified system theory.
