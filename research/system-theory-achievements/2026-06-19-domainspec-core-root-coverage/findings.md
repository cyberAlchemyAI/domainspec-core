# DomainSpec Core: Shareable Root-Level Achievements Toward System Theory

Dispatch: `2026-06-19-domainspec-core-root-coverage`

## One-Line Verdict

DomainSpec Core is not a completed self-regulating platform. The inspected root
surfaces contain concrete governance mechanisms such as the dispatch appender
(`internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs`),
append-only enforcement (`internal_tools/subagents-dispatch-hooks/hooks/enforce-append-only-dispatch.cjs`),
the dispatch ledger (`telemetry/agents/subagents-dispatch.yaml`), submodule gates
(`Makefile`, `SUBMODULE-DISCIPLINE.md`), runtime adapter config (`.arcanum/runtime/config.json`),
and telemetry docs (`docs/signals/TERMINAL-GUARD.md`, `.arcanum/observability/README.md`).
Those mechanisms support a narrower claim: this is an owned repository architecture with
authority boundaries, generated runtime projections, selected enforcement gates,
feedback-bearing records, owner-scoped handoffs, and a formal research track around residue
and translation. [R1][R2][R4][R5]

## Terms Used Carefully

- **Governed-system substrate:** artifacts and enforcement paths that constrain mutation,
  preserve state, and route observed signals into later refusal, refresh, rerouting, or
  closure.
- **Boundary:** an authority, publication, ownership, or runtime separation that changes
  allowed mutation, visibility, or source authority.
- **Interface:** a stable contract through which one subsystem can invoke, validate, or
  project another.
- **Feedback:** a return path from observation to changed future behavior. Ledgers and
  telemetry are observations until a later artifact uses them to refuse, refresh, reroute,
  or close work.
- **Closure:** explicit completion or refusal semantics. Human-reviewed handoffs are
  feedback-bearing handoff loops, not automatically closed loops.
- **Variety control:** hooks, appender rules, submodule gates, and policies that narrow
  allowed action variety.
- **Signal preservation:** ledgers and receipts keeping local outcomes available for later
  inspection and reuse.
- **Recursive governance:** the same governance pattern appearing across parent,
  submodule, runtime, and handoff levels while preserving local authority.
- **Residue:** in the formal track, residue is the internal DomainSpec vocabulary for what
  remains across translation, entropy, emergence, and observer/system relations. In the
  operational track, use the plainer phrase "unresolved state and decision leftovers" for
  blocked work, skipped changes, demoted claims, and next-route obligations.

## Precedent Labels

Many achievements below are not novelty claims. Public/private separation, generated
runtime mirrors, append-only ledgers, schema validation, telemetry, CI publishing,
scorecards, and owner handoffs are known engineering and governance patterns.
DomainSpec's achievement is the owned integration and evidence discipline across these
surfaces, plus its internal residue vocabulary and partial formalization track.

## What Is Strongest

### 1. Owned Public Capability Framework With Generated Runtime Projections

The public `arcanum/` surface presents a shareable capability framework through
`arcanum/README.md`, `arcanum/arcana/README.md`, and `arcanum/transmutations/README.md`.
The parent root projects those capabilities into generated or compatibility surfaces:
`.agents/skills/invoke/SKILL.md`, `.claude/skills/invoke/SKILL.md`,
`.codex/commands/invoke.md`, `.codex/commands/dispatch-spec.md`, and
`.arcanum/runtime/config.json`. These witness DomainSpec/Arcanum's owned packaging and
projection pattern, not a new category of runtime architecture. [R1]

This supports a boundary/interface reading because canonical source authority, generated
runtime projections, and local evidence state have different mutation and publication
rules. `arcanum/README.md` also demotes `.codex/commands/` to compatibility adapter status,
while the generated skill headers identify regeneration policy rather than direct mutation
as the update path. [R1]

### 2. Repo-Local Governance/Control Plane With Enforced Ledgers, Hooks, And Guards

The root has already-deployed local mechanisms: `append-dispatch.cjs`, the append-only
hook, `docs/LEDGER-MODEL.md`, `internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs`,
`tools/terminal_guard.sh`, `docs/signals/terminal-guard.jsonl`, `Makefile`, and
`SUBMODULE-DISCIPLINE.md`. Together they witness append-only writes, close rows,
`exit_reason`, `agents_spawned`, command telemetry, and submodule push checks. [R2]

This is an application of known control and governance patterns. The stronger system
claim is limited to mechanisms with enforcement or refusal semantics: appender rules,
hook enforcement, submodule gates, terminal guard behavior, and runtime adapter contracts.
Research-structure checks and observability scaffolding are useful, but they carry less
cybernetic weight unless they change later behavior. [R2]

### 3. Bounded-Artifact And Decision-Scope Discipline

The sampled product artifacts reduce broad claims into reviewable units. Examples include
Ontologize dogfood artifacts
(`projects/ontologize/dogfood/cyberalchemy-lead-evidence-pilot/DOGFOOD-PILOT.md`,
`SCORECARD-SPEC.md`, `RESULTS.md`, `CHANNEL-BRIEFS.md`, `OFFER-MAP.md`), public and
deliverable packaging (`projects/ontologize/PUBLIC-OFFERING.md`,
`projects/ontologize/deliverable/README.md`), CyberAlchemy first-loop design
(`cyberAlchemy/agentic-system-first-working-slice.md`), the UI Prototyping Studio workflow
(`projects/ui-prototyping-studio/README.md`, `SPEC.md`), and Poker Team validation
(`validation/poker-team/README.md`, `recruitment_game/**`,
`backend/src/domain/player/*.ts`, `backend/src/domain/player/*.test.ts`). [R3]

This is best read as bounded-artifact discipline. It supports bounded-rationality language
only where the artifact fixes an evidence threshold, decision owner, metric, scorecard,
or stopping rule. It should not be inflated into product-market validation. [R3]

### 4. Recursive Governance Through Handoffs, Signals, And Receipts

The operations layer records decisions, owner boundaries, refresh reports, delegation
signals, terminal telemetry, architecture-first route manifests, runtime handoffs, and
generated research packages. Witnesses include `docs/decisions/install-profile-contract.md`,
`ops/SURFACE-OWNER-BOUNDARIES.md`, `ops/development/DOMAINSPEC-OWNER-HANDOFF.md`,
`ops/development/LEAN-FORMALIZATION-OWNER-HANDOFF.md`,
`ops/ARCANUM-RUNTIME-SURFACE-REFRESH-REPORT.md`, `docs/signals/DELEGATION-TUNING.md`,
`docs/signals/delegation-tuning.jsonl`, and generated closeout/index artifacts under
`output/research-package-20260616/tests/triton-top2-backward-kernel/`. [R4]

This is recursive governance in the ordinary structural sense: parent-level policies
coordinate submodules and generated surfaces while preserving owner-scoped mutation
boundaries. A stronger viable-system claim would need a mapped VSM analysis, which this
dispatch did not perform. [R4]

### 5. Active Formal/Research Track With Partial Lean-Backed Evidence

The formal/research lane contains concrete theorem-adjacent artifacts and explicit open
status labels: `domainspec-formalization/docs/domainspec-two-layer-framework.md`,
`domainspec-formalization/lean-formalization/DomainSpec.lean`,
`domainspec-formalization/docs/paper.md`, `domainspec-lean-formalization/LEAN-ARCHITECTURE.md`,
`domainspec-lean-formalization/lean-formalization/SchemaInstance.lean`,
`DomainSpec.lean`, `DomainSpecSystem.lean`, `SecondLawDiscrete.lean`,
`domainspec-lean-formalization/THERMODYNAMICS.md`,
`domainspec-lean-formalization/docs/emergence-as-asymmetric-dependence.md`, and
`domainspec-lean-formalization/research-emergence/README.md`. [R5]

Within DomainSpec, residue is the most developed connective vocabulary in the inspected
formal/research surfaces. It links translation, entropy, emergence, and observer/system
relations, but these are adjacent tracks rather than one integrated model. The safest
claim is partial formalization plus disciplined bridge research, not a finished theory.
[R5]

## Public-Safe Achievement Claims

- DomainSpec has a public/private composition model: public Arcanum capabilities,
  generated runtime projections, and private local evidence/telemetry are separated by
  different source-authority, mutation, and publication rules. Witnesses include
  `arcanum/README.md`, `.agents/skills/invoke/SKILL.md`, `.claude/skills/invoke/SKILL.md`,
  `.codex/commands/invoke.md`, and `.arcanum/runtime/config.json`. [R1]
- DomainSpec has a repo-local governance substrate: append-only writes, hook enforcement,
  close rows, command telemetry, submodule gates, and owner handoffs are witnessed by
  `append-dispatch.cjs`, `enforce-append-only-dispatch.cjs`, `docs/LEDGER-MODEL.md`,
  `tools/terminal_guard.sh`, `Makefile`, `SUBMODULE-DISCIPLINE.md`, and
  `ops/SURFACE-OWNER-BOUNDARIES.md`. [R2][R4]
- Sampled product and dogfood artifacts show bounded-artifact practice: Ontologize
  dogfood scorecards, CyberAlchemy first-loop scoping, UI Prototyping Studio workflow, and
  Poker Team validation turn broad intent into reviewable units. [R3]
- Operations artifacts preserve unresolved state and decision leftovers rather than
  erasing them: refresh reports, route manifests, task-session results, closeouts, and
  generated research indexes keep blockers and next routes visible. [R4]
- DomainSpec has an active formal/research track around residue, categorical translation,
  Lean-backed counterexamples, finite/discrete thermodynamics, and emergence framing, with
  explicit anti-claims and open status labels. [R5]

## Claims To Avoid Or Soften

- Do not claim DomainSpec Core is a completed self-regulating platform. The evidence shows
  selected gates, records, and handoffs, while several loops still depend on human
  confirmation, optional observer availability, external runners, or owner-scoped
  downstream work. [R2][R4]
- Do not claim the whole private umbrella is public-ready. Live telemetry, local runtime
  profiles, private validation domains, machine-global settings, and owner-specific traces
  must remain private or be regenerated/scrubbed. [R1][R2][R3][R4]
- Do not claim all generated runtime surfaces are canonical. `.agents/`, `.claude/`,
  `.codex/`, and `.arcanum/` include generated mirrors, compatibility adapters, and local
  state. [R1]
- Do not claim CyberAlchemy, Ontologize, AutoAds, or Body War are market-proven products.
  The stronger evidence is candidate architecture, dogfood planning, bounded offering
  packages, and discovery baselines. [R3]
- Do not claim classic Forrester-style system dynamics. The root contains cybernetic,
  categorical, finite-discrete, and governance-control evidence, but not stock-and-flow
  system-dynamics formalism. [R5]
- Do not claim a settled physics or emergence contribution. The formal track is
  disciplined and partially formalized, but many bridge claims remain conjectural,
  analogy-bounded, or explicitly open. [R5]
- Do not claim a novel control-system paradigm. Many ingredients are known engineering,
  governance, and cybernetic patterns; the current achievement is disciplined integration
  and evidence handling across the inspected surfaces. [R1][R2][R4]

## Relation To System Theory

The root evidence supports a careful system-theory reading only where the term points to an
enforced constraint, state transition, or formal model:

- **Boundary:** public Arcanum, generated mirrors, private telemetry, product artifacts,
  validation domains, and formal research are separated into source-authority and
  publication layers. [R1][R3][R4]
- **Interface:** runtime adapters, generated skill packages, command adapters, dispatch
  forms, and deliverable templates make interaction points inspectable. [R1][R2][R3]
- **Feedback-bearing records:** dispatch close rows, terminal telemetry, delegation
  signals, refresh reports, owner handoffs, and generated closeouts preserve signals; they
  become feedback where later artifacts use them to refuse, refresh, reroute, or close
  work. [R2][R4]
- **Variety control and signal preservation:** hooks, appender rules, submodule gates, and
  cleanup policies narrow permitted actions; ledgers and receipts preserve local outcomes
  for later inspection. [R2][R4]
- **Recursive governance:** parent root governance coordinates submodules and generated
  surfaces while preserving owner-scoped authority. [R4]
- **Residue vocabulary:** the formal/research track gives DomainSpec an internal language
  for what remains across translation, entropy, emergence, and observer/system relations.
  [R5]

The best compact claim is:

> The inspected evidence supports DomainSpec Core as an owned, evidence-backed
> software-development governance corpus using residue vocabulary across formal and
> operational artifacts. Its current achievements are strongest as disciplined integration
> of known boundary, control, telemetry, handoff, bounded-artifact, and formal-research
> patterns. It should not yet be described as a completed autonomous system, a finished
> general theory, or a novel control-system paradigm.

## Evidence Index

- [R1] Public export and runtime projection lane in `research.md`: public Arcanum,
  generated runtime mirrors, compatibility adapters, observability and inventory state,
  and public/private boundary risks. Direct witnesses include `arcanum/README.md`,
  `arcanum/arcana/README.md`, `arcanum/transmutations/README.md`,
  `.agents/skills/invoke/SKILL.md`, `.claude/skills/invoke/SKILL.md`,
  `.codex/commands/invoke.md`, `.codex/commands/dispatch-spec.md`, and
  `.arcanum/runtime/config.json`.
- [R2] Governance and control lane in `research.md`: append-only dispatch governance,
  ledger/appender/tests, terminal guard, Arcanum observability, submodule discipline, and
  formal-tooling receipts. Direct witnesses include
  `internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs`,
  `internal_tools/subagents-dispatch-hooks/hooks/enforce-append-only-dispatch.cjs`,
  `docs/LEDGER-MODEL.md`,
  `internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs`,
  `tools/terminal_guard.sh`, `docs/signals/terminal-guard.jsonl`, `Makefile`, and
  `SUBMODULE-DISCIPLINE.md`.
- [R3] Product, dogfood, and validation lane in `research.md`: Ontologize, CyberAlchemy,
  CyberAlchemy v2, UI Prototyping Studio, Poker Team validation, Whisky Doses, and Body
  War. Direct witnesses include
  `projects/ontologize/dogfood/cyberalchemy-lead-evidence-pilot/DOGFOOD-PILOT.md`,
  `projects/ontologize/dogfood/cyberalchemy-lead-evidence-pilot/SCORECARD-SPEC.md`,
  `cyberAlchemy/agentic-system-first-working-slice.md`,
  `projects/ui-prototyping-studio/README.md`, and `validation/poker-team/README.md`.
- [R4] Operations, handoffs, and recursive governance lane in `research.md`: decisions,
  owner boundaries, refresh reports, delegation/terminal signals, architecture-first
  manifests, and generated research package residue. Direct witnesses include
  `docs/decisions/install-profile-contract.md`, `ops/SURFACE-OWNER-BOUNDARIES.md`,
  `ops/development/DOMAINSPEC-OWNER-HANDOFF.md`,
  `ops/development/LEAN-FORMALIZATION-OWNER-HANDOFF.md`,
  `ops/ARCANUM-RUNTIME-SURFACE-REFRESH-REPORT.md`,
  `docs/signals/DELEGATION-TUNING.md`, and generated closeout/index artifacts under
  `output/research-package-20260616/tests/triton-top2-backward-kernel/`.
- [R5] Formalization and research lane in `research.md`: DomainSpec formalization, Lean
  architecture, residue, finite discrete thermodynamics, emergence framing, and demotion
  of overclaims. Direct witnesses include
  `domainspec-formalization/docs/domainspec-two-layer-framework.md`,
  `domainspec-formalization/lean-formalization/DomainSpec.lean`,
  `domainspec-formalization/docs/paper.md`,
  `domainspec-lean-formalization/LEAN-ARCHITECTURE.md`,
  `domainspec-lean-formalization/lean-formalization/SecondLawDiscrete.lean`,
  `domainspec-lean-formalization/THERMODYNAMICS.md`, and
  `domainspec-lean-formalization/docs/emergence-as-asymmetric-dependence.md`.

## Reviewer Corrections Applied

- Precedent: public copy now labels known engineering/governance patterns as owned
  integration, not novelty.
- Non-vacuity: broad lane citations now carry direct witness paths for major claims.
- Definitional soundness: system-theory terms are defined and tied to enforcement,
  state transition, or formal-model evidence.
