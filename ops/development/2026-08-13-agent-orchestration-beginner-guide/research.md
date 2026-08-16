# Research substrate: agent orchestration

These sections preserve the ten explorer returns verbatim. Parent-authored normalization lives in `receipts/`; this file does not upgrade any claim beyond the return's own sources and ceiling.

## Agent 1 — Abramsky, Samson — Canonical vocabulary

## Bounded research return

### Beginner-safe glossary

- **Helper** — One agent working inside a parent’s already-bounded scope. It is not a governed dispatch unless work fans out to two or more agents or outgrows that scope.  
  Source: `arcanum/arcana/subagent-strategy/SKILL.md:75-84`.

- **Dispatch** — A governed multi-agent lifecycle used when synthesis, context protection, isolation, or parallelism justifies coordination. It includes proposal, tension checking, human confirmation, registration, dependency-aware execution, and closeout.  
  Source: `arcanum/arcana/subagent-strategy/SKILL.md:75-84,111-127`.  
  Status: operationally described, not a standalone `DEF-ARC-*` definition.

- **Role** — The assignment slot connecting responsibility to one governing capability, owned steps, inputs, outputs, and mutation boundaries. A role is not an agent identity or independent authority.  
  Source: `arcanum/formulae/dispatch-spec/SKILL.md:87-101,126-135`.

- **Capability** — Reusable bounded behavior whose contract owns the delegated work. A sigil is one capability; a spell composes several capabilities.  
  Source: `arcanum/README.md:105-146`; execution ownership at `arcanum/runtime/orchestrate/SKILL.md:76-81`.  
  Status: described, not yet formally defined Arcanum-wide.

- **Step** — A node in a dispatch route. It names a capability, pattern, inputs, outputs, and applicable evidence obligations. A validated step is route description, not execution.  
  Source: `arcanum/formulae/dispatch-spec/SKILL.md:65-101`.

- **Wave** — Roles/actions admitted to run together after dependencies pass. The parent joins the wave and evaluates its gate before exposing later actions.  
  Source: `arcanum/formulae/dispatch-spec/SKILL.md:126-146`; `arcanum/runtime/orchestrate/SKILL.md:151-164`.

- **Gate** — An explicit decision controlling whether a transition may proceed. Artifact existence alone is insufficient; the owning contract decides readiness. Human confirmation, receipt admission, and dependent-wave decisions are distinct gates.  
  Source: `arcanum/arcana/subagent-strategy/SKILL.md:111-126,130-142`; `arcanum/runtime/orchestrate/SKILL.md:151-164`.

- **Join** — Bring terminal agent results back, verify their expected action/agent identities and receipt shape, then admit them for reduction. It is more than waiting for text.  
  Source: `arcanum/runtime/orchestrate/SKILL.md:151-164`.

- **Closeout** — Terminal accounting: every spawned agent is joined and closed, partial failures remain visible, and the paired close event is recorded. Closeout does not mean publication or promotion.  
  Source: `arcanum/arcana/subagent-strategy/SKILL.md:123-127`; private binding at `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:143-144`.

- **Receipt** — A bounded structured report identifying the action, agent, status, artifacts, validation result, and blockers. Receipt admission proves expected shape and identity; it does not make every contained claim true.  
  Source: `arcanum/runtime/orchestrate/schemas/receipt.schema.json`; `arcanum/runtime/orchestrate/SKILL.md:151-164`.

- **Evidence** — Inspectable support for a particular claim. Its claim ceiling depends on its kind: schema validation supports shape, while source-time causal events support runtime execution.  
  Source: `arcanum/definitions/DEFINITIONS.md:77-114`; `arcanum/runtime/orchestrate/SKILL.md:124-133,211-223`.

- **Authority** — The bounded right of an owner or source artifact to decide meaning or mutation for its declared scope. Nearby evidence and generated projections do not inherit that authority.  
  Source: `arcanum/definitions/DEFINITIONS.md:18-59,340-380`; runtime split at `arcanum/runtime/orchestrate/SKILL.md:76-81`.

- **Promotion** — The owner-reviewed move from development evidence into canonical source, normally through a promotion patch. Validation, a receipt, a commit, or file presence alone is not promotion.  
  Source: `arcanum/definitions/DEFINITIONS.md:231-266,396-437`.

- **Sigil** — One reusable capability, placed by epistemic nature in Formulae, Transmutations, or Arcana.  
  Source: `arcanum/README.md:121-138`.  
  Status: descriptive only.

- **Spell** — A workflow composition referencing several owning sigils and defining order, shared state, artifacts, gates, and observation.  
  Source: `arcanum/README.md:140-146`.  
  Status: descriptive only.

### Canonical owner and projection map

| Concern | Owner/source | Claim ceiling |
|---|---|---|
| Arcanum-wide defined terms | `arcanum/definitions/DEFINITIONS.md:1-16` | Normative only for terms actually present |
| Human-facing capability model | `arcanum/README.md:96-146` | Descriptive navigation |
| Portable dispatch lifecycle | `arcanum/arcana/subagent-strategy/SKILL.md:62-73,111-127` | Universal lifecycle routing |
| Dispatch graph shape | `arcanum/formulae/dispatch-spec/SKILL.md:14-25,65-101` | Draft route validator; not execution |
| Native runtime | `arcanum/runtime/orchestrate/SKILL.md:70-81,99-164` | Preflight, actions, joins, gates, closeout |
| DomainSpec bindings | `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:12-31` | Private consumer adapter: constitution, form, pool, registrar, ledger, Inventory policy, paths |
| Codex projections | `.agents/skills/{subagent-strategy,dispatch-spec,orchestrate}/SKILL.md:1-7` | Generated discovery/runtime surfaces; regenerate from canonical source |

Current-worktree comparison found all three generated projection bodies identical to their canonical counterparts from the first heading onward. Their hashes differ because their frontmatter declares generated projection metadata. The inspected `.agents/skills/*` targets are directories, not symlinks, despite `arcanum/README.md:138` describing repository skills as symlinked; treat that sentence as stale for these packages.

### Terms still unresolved globally

Only `contract`, `schema`, `goal spell`, `staged delta`, `approval token`, `development artifact`, `canonical artifact`, and `promotion patch` have relevant formal `DEF-ARC-*` entries. Generic `sigil`, `spell`, and `capability` are explicitly recorded as merely described at `AGENTS.md:171-178`.

`helper`, `dispatch`, `role`, `step`, `wave`, `gate`, `join`, `closeout`, `receipt`, `evidence`, `authority`, and bare `promotion` also lack standalone global definition entries. They have usable owner-local meanings in the cited contracts, but a beginner guide should label these as operational explanations rather than pretend they are canonical definitions.

### Public/private constraints

- Public Arcanum prose may explain the portable lifecycle and its claim ceilings.
- DomainSpec and Saturn remain private and must not be described as shipped; boundary: `AGENTS.md:7-12`.
- Do not export the adapter’s constitution, local paths, schema version, pool, registrar, ledger, Inventory bindings, or private research-owner details into public Arcanum prose; source: adapter `:12-31` and public core `:62-73`.
- Inventory is discovery, not proof or dispatch authority: adapter `:73-83`.
- A generated package, validated route, preflight, receipt, or closeout must not be inflated into canonical authority, promotion, publication, deployment, or production status.
- Avoid the DomainSpec wedge beginning at `arcanum/definitions/DEFINITIONS.md:455` when sourcing public orchestration vocabulary unless its publication classification is separately resolved.

### Current-byte evidence identity

- `arcanum/README.md`: `b542af6d744c6c869c279248b3e24412457af47a914c0df7ec9a9bff679eb582`
- `arcanum/definitions/DEFINITIONS.md`: `e6460f08407b1cb695d5d640e32a820524b94d3b61b3bccd3ee94b80e2f72bf7`
- `arcanum/arcana/subagent-strategy/SKILL.md`: `8720806485cfee54781deb50cc501d0552bad18bdcc4f86c954d882952900c62`
- `arcanum/formulae/dispatch-spec/SKILL.md`: `0aaf1750447ba9daf8b06ba5f2635c148e258ec8e983d5e82eb348fb657e8226`
- `arcanum/runtime/orchestrate/SKILL.md`: `de002a45853414b5ebb6d64c1468cf4bc86a92bb79a6a8570ca6bca8cec347cf`
- private adapter: `327187d7cc3556a1c061caff4ca315923d2eec0415f0b3edd8eb9ea5dee06f3a`

No file was written by this read-only action. The declared artifact below is the parent/coordinator persistence destination.

```json
{
  "schema_version": "arcanum.native-dispatch-runner.receipt.v0.1",
  "action_id": "spawn-0001",
  "dispatch_id": "2026-08-13-agent-orchestration-beginner-guide-route",
  "run_id": "agent-orchestration-beginner-guide-20260813-r1",
  "wave_id": "foundation-explorers",
  "step_id": "s1-foundations",
  "role": "explorer-vocabulary",
  "capability_ref": "research",
  "agent_id": "/root/orchestrate_ce9376d6af8cfc53bd31e8c04efd681ecd456b9efbf12abb682c81eb3693fe69_spawn_0001",
  "status": "pass",
  "artifacts": [
    "ops/development/2026-08-13-agent-orchestration-beginner-guide/receipts/explorer-vocabulary.json"
  ],
  "validation": "pass",
  "blockers": [],
  "started_at": "2026-08-13T19:44:13Z",
  "finished_at": "2026-08-13T19:51:30Z"
}
```

## Agent 2 — Simon, Herbert — Lifecycle owner graph

## Explorer receipt

- Action: `spawn-0002`
- Role: `explorer-owner-graph`
- Status: `pass`
- Validation: `pass`
- Mutation policy: `read-only`
- Changed paths: none
- Intended artifact: `ops/development/2026-08-13-agent-orchestration-beginner-guide/receipts/explorer-owner-graph.json`
- Blockers: none

### Owner-by-transition map

| Transition | Owner and input | Gate / stop | Output, receipt, next owner | Explicit proof ceiling |
|---|---|---|---|---|
| Intent → governed artifacts | **Invoke** receives vague development intent and owns definition, design, plan, Work-Pack, and handoff authoring. | Mode-specific global gates; stop on missing mandatory inputs, blockers, or governance violations. | Authored artifacts plus `Invoke Result`; route to Task Session, Spellcraft, Sigil Development, reflection, or deferred work. | Authorship does not establish target lifecycle completion, implementation execution, registry release, runtime readiness, authority, or promotion. `arcanum/spells/invoke/README.md:20-26,60-90,112-121,271-352,393-447` |
| Route proposal → validated route shape | **Dispatch Spec** consumes a dispatch JSON and validates steps, bindings, dependencies, joins, gates, evidence, scopes, and promotion guardrails. | Block malformed/impossible routes, false promotion claims, or incomplete lifecycle closeout. | `Dispatch Spec Result`; an approved capability-bound route can hand off to Orchestrate. | It neither selects the right capabilities nor executes/spawns them. Its current declared status is `draft`. `arcanum/formulae/dispatch-spec/SKILL.md:14-25,47-101,103-150,176-201` |
| Work Pack → bounded execution frontier | **Implementation Readiness** owns frozen Work-Pack identity, execution policy, entry projection, intent binding, frontier, and outer-loop reduction. | Exact digests, one outstanding action, correlated joins, finite budget, and eight hard stop classes. | Readiness report with distinct owner and Task Session receipt chains; routes through Continuation Router and Task Session. | An owner receipt may reclassify an entry but cannot complete a unit. The controller does not perform owner mutation, expand the frontier, promote, publish, deploy, or contact external systems. `arcanum/spells/implementation-readiness/README.md:9-45,47-67,89-105,125-166,172-174` |
| Receipt → one owner hop | **Continuation Router** consumes one terminal receipt or typed prerequisite plus exact authorization or a validated current Work-Pack binding. | Require unambiguous owner, complete inputs, exact scope/effect, unused fingerprint, and the selected owner’s own gates; stop on ambiguity, cycle, mismatch, or unjoined work. | Ranked routes, one selected route, separate owner receipt, and returned next route/control handle. | It does not perform or reinterpret owner semantic work, recursively continue, or rewrite the source result. `arcanum/arcana/continuation-router/SKILL.md:14-15,56-82,99-170,238-268` |
| Ready unit → implemented and validated unit | **Task Session** owns one bounded task or SWU end to end. | Live task/dependency checks, bounded context, blocker decisions, exact mutation admission, done criteria, acceptance-critical validation, subagent closeout, and evidence synchronization. | `Task Session Result`, validation evidence, separate closeout-owner receipt, continuity cursor, and returned next route. | Admission is not lifecycle, promotion, publication, or deployment authority. Task Session does not execute the next unit or directly edit another owner’s closeout targets. `arcanum/arcana/task-session/SKILL.md:14-20,76-114,129-215,239-365,367-430,622-658` |
| Project evidence → durable project state | **Craft** owns `.craft/ledger.yml`; `CRAFT.md` and indexes are derived views. | Resolve the exact workspace, preserve blockers and decisions, require recomposition evidence, validate before closure. | `Craft Result`, residue, and `next_move`; hand off through the named capability owner. | Craft records route memory and local state but does not rewrite native receipts, execute capabilities, or turn route validation into execution evidence. `arcanum/arcana/craft/SKILL.md:14-25,56-71,114-149,252-268,312-341,360-399` |
| Bounded evidence → durable collaboration locator | **Handoff Notice** publishes, resolves, or inspects a repository-local notice. | Repository/private-boundary check, observed-versus-proposed separation, collision and digest verification. | JSON and Markdown notice, `HN-...` locator, receipt, and named next owner. | A notice is communication evidence only: no authority, task cursor, dispatch, external delivery, or execution. `arcanum/transmutations/handoff-notice/SKILL.md:14-44,47-83,85-112,130-152` |
| Sources → reusable discovery model | **Inventory** owns generated entries, evidence cards, indexes, lint findings, and lookup packets over immutable sources. | Projection conformance, freshness, source coverage, link and schema validation; failed checks block lookup readiness. | `Inventory Result` or downstream lookup packet for Context Builder and other consumers. | Inventory does not own governed meaning, canonical definitions, promotion, or source truth. Its packets are non-authority read models. `arcanum/arcana/inventory/SKILL.md:14-35,103-140,310-339,356-406` |
| Invocation evidence → behavior signals | **Signal Observer** consumes a completed invocation envelope. | Required envelope fields, visible evidence, privacy, one valid append, and loop prevention. | One telemetry row, quality/anti-pattern signals, and a reflection recommendation. | Observation is non-blocking by default and must not alter the primary result, application code, user artifact, or observed capability. `arcanum/arcana/signal-observer/SKILL.md:14-19,32-91,99-145` |
| Managed invocation → observed closeout | **Observed Invocation Loop** coordinates wrapper/hook execution, envelope creation, Signal Observer, and optional reflection. | Managed invocation, valid envelope, append/dedupe evidence, threshold evaluation, and hook enforcement. | Primary result plus telemetry status and optional reflection report/route. | It preserves the primary result, does not replace Experiment Harness, and reflection cannot mutate a sigil or spell without a separately approved lifecycle route. `arcanum/spells/observed-invocation-loop/README.md:12-18,43-81,83-111,161-180` |
| Validated, authorized dispatch → native agent run | **Orchestrate** owns preflight, persisted-action scheduling, native spawn/wait, receipt normalization, joins, gates, dependent-wave planning, recovery, and closeout. | Validator `pass`, authorization, active host operations, persisted action identity, causal event ordering, exact receipt admission, and clean terminal validation. | Preflight receipt, per-action receipts, causal events, gate decisions, and next-wave plan or blocked closeout. | Delegated capabilities retain their bounded semantic work; humans and lifecycle owners retain authority and promotion. Offline reduction and residue are not live execution evidence. `arcanum/runtime/orchestrate/SKILL.md:72-81,99-164,211-239` |

### Beginner-safe structural account

```text
intent
  → Invoke authors a Plan / Work Pack
  → Implementation Readiness admits and sequences its bounded frontier
  → Continuation Router admits one exact owner hop
  → Task Session executes and validates one unit
  → owner-backed closeout synchronizes evidence
  → outer loop either advances or stops

complex multi-agent route
  → Dispatch Spec validates the graph
  → explicit authorization
  → Orchestrate schedules, joins, gates, and closes native agents
  → capability receipts return to the parent

cross-cutting owners
  Craft = project-local state
  Inventory = discovery read model
  Handoff Notice = collaboration evidence
  Observed Invocation Loop = behavior telemetry and learning
```

Therefore, orchestration is not:

- **Planning:** Invoke authors plans; Dispatch Spec validates route shape.
- **Implementation execution:** Task Session or another delegated capability performs bounded semantic work; Orchestrate executes host coordination.
- **Project state:** Craft owns the project ledger.
- **Memory or knowledge authority:** Inventory and telemetry are reusable read models, not truth or promotion owners.
- **Semantic authority:** humans and capability owners retain lifecycle and promotion authority.

### Residue and claim ceiling

- The Inventory packet is `ready_with_residue`, with partial coverage, a preexisting modified index, and 153 warnings. It explicitly grants no dispatch, mutation, promotion, publication, release, deployment, or production authority. `strategy-inventory-packet.json:1-18,156-177`
- No single selected artifact currently teaches the entire strategy-to-closeout lifecycle.
- This receipt establishes a current-source owner map only. It does not establish that any particular dispatch ran successfully or that historical run evidence matches current contracts.
- Runtime identity, run ID, wave ID, agent ID, and timestamps remain parent-normalizer fields; they were not fabricated here.

## Agent 3 — Ahrens, Sönke — Human-facing explanations

{
  "action_id": "spawn-0003",
  "dispatch_id": "2026-08-13-agent-orchestration-beginner-guide",
  "target": "dispatch-sheet.json#/groups/0/agents/2",
  "role": "explorer-human-surfaces",
  "status": "pass",
  "mutation_policy": "read-only",
  "changed_paths": [],
  "result": {
    "pedagogical_moves_that_worked": [
      {
        "move": "Begin with a concrete relation before terminology.",
        "evidence": [
          "projects/domainspec-v2/research/evolvable-validation-framework/whisper/plain-language-guide.md:1-5",
          "arcanum/spells/whisper/README.md:170-180"
        ]
      },
      {
        "move": "Use one finite example throughout, showing the input, each transformation, and the resulting evidence.",
        "evidence": [
          "projects/domainspec-v2/research/evolvable-validation-framework/whisper/plain-language-guide.md:29-111",
          "cyberAlchemy-v2/development/agent-reasoning-engine/BEGINNER-GUIDE.md:123-177"
        ]
      },
      {
        "move": "At every transition, state both what changed and what remains unproved.",
        "evidence": [
          "projects/domainspec-v2/research/evolvable-validation-framework/whisper/plain-language-guide.md:43-49",
          "projects/domainspec-v2/research/evolvable-validation-framework/whisper/plain-language-guide.md:61-85",
          "cyberAlchemy-v2/development/agent-reasoning-engine/BEGINNER-GUIDE.md:26-38"
        ]
      },
      {
        "move": "Separate observed reality, missing evidence, and the nearest bounded next step.",
        "evidence": [
          "projects/domainspec-v2/research/evolvable-validation-framework/whisper/plain-language-guide.md:113-152",
          "cyberAlchemy-v2/development/agent-reasoning-engine/BEGINNER-GUIDE.md:89-121",
          "cyberAlchemy-v2/development/agent-reasoning-engine/BEGINNER-GUIDE.md:297-339"
        ]
      },
      {
        "move": "Teach relations between owners and artifacts instead of presenting a catalogue.",
        "evidence": [
          "arcanum/spells/whisper/README.md:177-186",
          "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/STRATEGY.md:13-34"
        ]
      },
      {
        "move": "End with a retell test and a safe action the reader can actually take.",
        "evidence": [
          "arcanum/spells/whisper/README.md:190-212",
          "cyberAlchemy-v2/development/agent-reasoning-engine/BEGINNER-GUIDE.md:341-358"
        ]
      }
    ],
    "misleading_shortcuts": [
      "A validated plan, explicit confirmation, registration, execution, evidence closure, and closeout must not be collapsed into one idea called approval.",
      "A completed research lifecycle does not prove the findings true; a receipt is evidence, not semantic authority.",
      "Inventory is discovery only, never dispatch authority or proof.",
      "Presence, generated bytes, tests, or route validation do not by themselves prove installation, invocation, integration, publication, or production.",
      "Historical, candidate, current, and terminal states must remain visibly separate. The August 12 strategy says registration and execution had not occurred, while its later findings show partial advancement but still no admitted terminal auditor receipt or unique closeout.",
      "The large typed-state vector in the August 12 findings is valuable source material but too dense for the beginner opening. Introduce its key non-implication through one example before showing any state table.",
      "The modified private beginner guide is a pedagogical precedent only. Its private vocabulary, product facts, and prose cannot become public Arcanum authority.",
      "Automated formatting or delivery-flow checks cannot establish that an explanation is intelligible; Whisper reserves that judgment for human editorial review."
    ],
    "novice_prerequisites": [
      "Only ordinary concepts: a task, a source file, a check, evidence, and explicit human approval.",
      "No prior DomainSpec, Saturn, Dispatch Spec, Orchestrate, or receipt-schema vocabulary.",
      "The reader should first understand that one bounded helper differs from a governed multi-agent run and that a plan differs from permission."
    ],
    "need_before_name_terms": [
      {
        "need": "The work needs several independent viewpoints or dependent stages.",
        "name_after_need": "dispatch"
      },
      {
        "need": "Humans need to understand why the work is split and where disagreement should occur.",
        "name_after_need": "strategy"
      },
      {
        "need": "The host needs one exact machine-readable manifest of roles, scopes, dependencies, and stops.",
        "name_after_need": "dispatch sheet"
      },
      {
        "need": "Two independent checks must challenge the exact proposed route before authorization.",
        "name_after_need": "tension passes"
      },
      {
        "need": "Permission must bind one exact proposal without yet proving execution or truth.",
        "name_after_need": "confirmation"
      },
      {
        "need": "The authorized run needs a durable lifecycle entry.",
        "name_after_need": "registration"
      },
      {
        "need": "Some actions can run together while others require earlier results.",
        "name_after_need": "wave, dependency, join, gate"
      },
      {
        "need": "Each bounded action must return an attributable outcome for admission.",
        "name_after_need": "receipt"
      },
      {
        "need": "The run must distinguish recorded outcomes from truth-owning decisions.",
        "name_after_need": "evidence versus authority"
      },
      {
        "need": "The system must record termination without implying publication or production.",
        "name_after_need": "closeout"
      }
    ],
    "candidate_narrative_anchor": {
      "anchor": "One research question moving through a governed relay",
      "example": "How should a beginner understand agent orchestration?",
      "movement": [
        "A user asks one question.",
        "The parent decides whether one helper is enough or a dispatch is warranted.",
        "Inventory supplies leads but no authority.",
        "A strategy explains the lanes; an exact sheet binds scopes and dependencies.",
        "Independent tension passes challenge that exact sheet.",
        "Explicit human confirmation permits registration and execution of that bounded run.",
        "Agents execute in dependency-gated waves and return receipts.",
        "Joins and gates admit evidence before synthesis, review, findings, and audit.",
        "Closeout records what the run actually completed and preserves residue.",
        "Whisper later composes the evidence-closed research into a beginner guide; that composition is a separate lifecycle."
      ],
      "breakpoint": "The relay analogy must not imply that passing a baton proves the content true. Every handoff still has an owner, gate, evidence ceiling, and possible stop."
    },
    "candidate_retell_chain": {
      "input_or_invitation": "A bounded user question that may require independent, coordinated work.",
      "transformation": "Strategy and exact sheet turn the question into scoped roles, actions, dependencies, gates, and forbidden effects.",
      "immediate_consequence": "Human confirmation allows registration and execution of only that exact route.",
      "later_lifecycle": "Receipts are joined into cited synthesis, independently reviewed, written as findings, audited, and closed.",
      "limit": "Closeout proves only the bounded run state; it does not prove semantic truth, authority, publication, deployment, or production."
    }
  },
  "source_status": [
    {
      "path": "projects/domainspec-v2/research/evolvable-validation-framework/whisper/plain-language-guide.md",
      "sha256": "0eaad78311d9ff61216a19304f1d9be19b557e331b60b219cc975fd73d06909a",
      "worktree": "tracked-clean",
      "status_ceiling": "candidate teaching artifact, not authority",
      "selector": "lines 154-156"
    },
    {
      "path": "projects/domainspec-v2/research/evolvable-validation-framework/whisper/text-intent-substrate.yaml",
      "sha256": "451498faaeb54589762fe9f1f2a63e5a918653c02f90c12beefff6326155f421",
      "worktree": "tracked-clean",
      "status_ceiling": "candidate_internal_guide",
      "selector": "/text_intent_substrate/metadata/artifact_status"
    },
    {
      "path": "cyberAlchemy-v2/development/agent-reasoning-engine/BEGINNER-GUIDE.md",
      "sha256": "62c5a7291fe674ea11f377112e8d78abe80b24c052666667635d446ef7df971f",
      "worktree": "tracked-modified-preexisting",
      "status_ceiling": "draft-for-teammate-review; authority_effect none; private pedagogy evidence only",
      "selector": "lines 1-7"
    },
    {
      "path": "arcanum/spells/whisper/README.md",
      "sha256": "b5b25652b0658e21e32bac0fced6826f52abb0d4c94e548351c2369eb9d9527c",
      "repository_head": "33d3ebfbf6c8fc5af0b9f8a481858358f33a0a67",
      "worktree": "tracked-clean",
      "status_ceiling": "canonical public Whisper contract",
      "selector": "lines 160-212"
    },
    {
      "path": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/STRATEGY.md",
      "sha256": "6097d342a2760106c7179d62e696d92e2f7d46ca7f6cc4bd68dfa4fd8cc8ad46",
      "worktree": "untracked-preexisting",
      "status_ceiling": "historical strategy snapshot; lines 51-52 say unregistered and unauthorized"
    },
    {
      "path": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/findings.md",
      "sha256": "ebbde94feb8e7279daa98c8cb4469f5421419bce27f23769b0f822f9ef28815e",
      "worktree": "untracked-preexisting",
      "status_ceiling": "decision-ready research artifact that cannot self-certify its writer action or terminal run",
      "selector": "lines 362-391"
    }
  ],
  "claim_ceiling": "Pedagogical-pattern exploration only. No current dispatch-completion, canonical-definition, authority, publication, deployment, or production claim follows. Private DomainSpec and Saturn material remains private.",
  "residue": [
    "The eventual guide needs one concrete current dispatch witness from causal receipts; these explanation sources alone cannot supply it.",
    "The August 12 strategy and findings preserve different time layers and must not be harmonized into a false terminal-success story.",
    "No filesystem receipt was written because the action's write scope is empty; the parent owns persistence at receipts/explorer-human-surfaces.json."
  ]
}

## Agent 4 — Ashby, W. Ross — Strategy and human gates

{
  "action_id": "spawn-0004",
  "dispatch_id": "2026-08-13-agent-orchestration-beginner-guide",
  "target": "ops/development/2026-08-13-agent-orchestration-beginner-guide/dispatch-sheet.json#governance_explorers-agent-0",
  "role": "explorer-strategy-gates",
  "status": "pass",
  "mode": "explore",
  "mutation_policy": "read-only",
  "changed_paths": [],
  "result": {
    "direct_answer": "A governed dispatch is a control loop with distinct admission, authorization, execution, evidence, approval, and accounting gates. No upstream success implies a downstream one: Inventory discovery is not authority; readiness and tension PASS are not permission; confirmation is not registration or execution; audit is not final approval when the parent owns that decision; and closeout proves only the bounded run state.",
    "lifecycle": [
      {
        "stage": "1-p1-decision",
        "owner": "domainspec-subagents-strategy",
        "gate": "At least one of synthesis, context protection, isolation, or parallelism must justify coordination.",
        "pass_effect": "Classify the dispatch type and begin strategy design.",
        "stop_or_non_effect": "Otherwise work inline. One bounded helper is not a dispatch unless it fans out to two or more agents or outgrows its parent scope.",
        "selectors": [
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:33-44"
        ]
      },
      {
        "stage": "2-inventory-preflight",
        "owner": "domainspec-subagents-strategy with Inventory as a read model",
        "gate": "For research or review, perform a read-only machine-index-first lookup before drafting the sheet; retain exclusions, gaps, residue, and at least one design consequence.",
        "pass_effect": "Supply bounded discovery leads to the appropriate lanes.",
        "stop_or_non_effect": "Inventory neither decides P1 nor authorizes, tensions, confirms, registers, or proves the dispatch. Degraded lookup remains explicit residue.",
        "selectors": [
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:46-83",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:27-47",
          "ops/development/2026-08-13-agent-orchestration-beginner-guide/strategy-inventory-packet.json#/lookup_status",
          "ops/development/2026-08-13-agent-orchestration-beginner-guide/strategy-inventory-packet.json#/non_authority_notice"
        ]
      },
      {
        "stage": "3-persisted-sheet-and-readiness",
        "owner": "register-dispatch form owner",
        "gate": "Persist a schema-0.8.0 row core without evidence_binding, then require SHEET_VALIDATION=pass, the live schema version, exact SHA-256, and LEDGER_MUTATION=none.",
        "pass_effect": "Close deterministic form, live-type, pool membership, identity uniqueness, approver shape, pair coverage, connection, and path obligations.",
        "stop_or_non_effect": "Readiness is non-mutating and is not tension approval, human permission, registration, or execution.",
        "selectors": [
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:85-97",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/SKILL.md:166-194"
        ]
      },
      {
        "stage": "4-independent-tension",
        "owner": "check-tension",
        "gate": "Two independent agents receive only the exact admitted sheet bytes, its digest, and the rubric. Tests cover axis, clone, spread, pair evidence, and global coherence. Only PASS/PASS proceeds.",
        "pass_effect": "Establish that the route is tensioned by design.",
        "stop_or_non_effect": "Either rejection or disagreement returns the sheet to the strategist; the human does not adjudicate this gate. Tension PASS cannot infer schema admission or authorization.",
        "selectors": [
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/check-tension/SKILL.md:15-37",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/check-tension/SKILL.md:39-72",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/check-tension/SKILL.md:74-120"
        ]
      },
      {
        "stage": "5-human-confirmation",
        "owner": "human",
        "gate": "Ask once only after composite readiness and PASS/PASS tension. Require explicit confirmation of the reviewed material strategy.",
        "pass_effect": "Authorize registration and bounded execution of that material strategy.",
        "stop_or_non_effect": "Silence, discussion, a question, or permission to revise is not confirmation. Confirmation does not prove execution, findings, truth, promotion, publication, deployment, or production.",
        "selectors": [
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:99-120",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/SKILL.md:189-203"
        ]
      },
      {
        "stage": "6-registration",
        "owner": "register-dispatch",
        "gate": "Bind the current sheet path and digest to exactly two independent PASS handles and one direct or equivalently carried confirmation handle.",
        "pass_effect": "Append exactly one dispatch row through the deterministic appender.",
        "stop_or_non_effect": "Registration records authorization and planned topology; it does not demonstrate that execution started or completed.",
        "selectors": [
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:122-128",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/SKILL.md:74-111",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/SKILL.md:196-217"
        ]
      },
      {
        "stage": "7-dependency-gated-execution",
        "owner": "Orchestrate for host coordination; delegated capability owners for semantic work",
        "gate": "A group becomes READY only after sequential or zig-zag predecessors supply the required artifacts and the live type-owner handoff returns ready. Feedback edges are repair routes, not initial dependencies.",
        "pass_effect": "Launch READY groups, run agents within each group in parallel, join receipts, and expose only admitted evidence downstream.",
        "stop_or_non_effect": "needs_feedback may traverse only a confirmed edge with remaining capacity; blocked preserves residue. Partial failures remain visible downstream.",
        "selectors": [
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:128-141",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:49-67",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:178-191"
        ]
      },
      {
        "stage": "8-research-evidence-closure",
        "owner": "research type owner, applied by the strategist",
        "gate": "Before the writer, classify every required evidence row under cited-synthesis or exact-binding as bound, deferred, killed, or unresolved; return ready, needs_feedback, or blocked.",
        "pass_effect": "Only ready admits the writer. Explorer-owned gaps route through a declared explorer feedback edge; interpretation gaps through zig-zag; supported wording defects through writer revision.",
        "stop_or_non_effect": "Do not invent evidence, a post-confirmation edge, or findings.md merely to satisfy the normal output shape.",
        "selectors": [
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:69-117",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:198-227"
        ]
      },
      {
        "stage": "9-writing-audit-and-final-approval",
        "owner": "Writer owns findings.md; auditor evaluates findings.md; declared final_approver owns terminal acceptance.",
        "gate": "Writer receives evidence-closed synthesis. Auditor may approve or request bounded revision. resolved requires acceptance by the declared final approver.",
        "pass_effect": "Produce an audited, cited result at its stated evidence ceiling.",
        "stop_or_non_effect": "research.md remains the strategist's verbatim explorer transcript. With final_approver=parent, an auditor PASS is necessary evidence but does not replace parent terminal approval or grant semantic/promotion authority.",
        "selectors": [
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:119-146",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:198-227",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/constitution/subagents-strategy-constitution-proposal.md:506-528"
        ]
      },
      {
        "stage": "10-closeout",
        "owner": "strategist through register-dispatch",
        "gate": "All spawned agents are terminally accounted for and the final result has a typed exit.",
        "pass_effect": "Append exactly one close row containing close_of, exit_reason, agents_spawned, loop count, and any verbatim feedback prompts.",
        "stop_or_non_effect": "The dispatch row is never edited. Closeout is bounded accounting, not publication, deployment, production readiness, or proof beyond its claim ceiling.",
        "selectors": [
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:143-144",
          "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/SKILL.md:351-385"
        ]
      }
    ],
    "confirmation_binding": {
      "material_fields": [
        "goal and evidence boundary",
        "dispatch type",
        "group purposes",
        "agent identities, roles, angles, prompts, and source scopes",
        "outputs",
        "dependency topology and loop ceilings",
        "final approver",
        "working-folder destination",
        "publication and privacy boundary",
        "validation obligations",
        "stop conditions"
      ],
      "mechanical_only_when_equivalence_is_proved": [
        "whitespace",
        "key order",
        "derived counts",
        "schema defaults",
        "evidence digests and handles",
        "canonical materialization of already-presented content"
      ],
      "change_rules": [
        "Every sheet-byte change invalidates readiness and both tension receipts and requires those machine gates to rerun.",
        "A durable deterministic material-equivalence receipt may carry prior confirmation to mechanically changed bytes.",
        "Material change, unknown equivalence, or an unprovable comparison requires renewed human confirmation."
      ],
      "selectors": [
        "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:99-120",
        "implementation/domainspec/internal_tools/subagents-dispatch-hooks/constitution/subagents-strategy-constitution-proposal.md:1017-1042"
      ]
    },
    "successful_ledger_bound_witness": {
      "dispatch": "2026-08-12-arcanum-cav2-wayfinding-refresh-r2",
      "temporal_trace": [
        {
          "state": "confirmation-ready snapshot",
          "evidence": "The exact sheet passed schema 0.8.0 registrar validation and PASS/PASS tension with ledger_mutation=none; authorization remained pending, spawn count was zero, and registration/execution had not occurred.",
          "selectors": [
            "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/confirmation-readiness.json#/status",
            "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/confirmation-readiness.json#/sheet",
            "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/confirmation-readiness.json#/orchestrate",
            "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/check-tension.json"
          ]
        },
        {
          "state": "explicitly confirmed",
          "evidence": "The confirmation bound digest c78b35fd1e29abd683e7dc7ee0974a53f3aad80e7f7630420d37b2f263280029 and authorized only the read-only research lifecycle and its evidence.",
          "selectors": [
            "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/human-confirmation.json"
          ]
        },
        {
          "state": "registered, execution not yet started",
          "evidence": "The registrar recorded one append, nine agents, five groups, and execution_started=false.",
          "selectors": [
            "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/registration.json"
          ]
        },
        {
          "state": "evidence-closed for writing",
          "evidence": "The exact-binding gate returned ready at a decision-ready-only ceiling while retaining bound, deferred, and killed rows rather than claiming a dependency-closed vertical witness.",
          "selectors": [
            "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/evidence-closure.json#/status",
            "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/evidence-closure.json#/claim_rows",
            "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/evidence-closure.json#/claim_ceiling"
          ]
        },
        {
          "state": "audited and terminally closed",
          "evidence": "The auditor receipt passed. Closeout records resolved, nine agents, three loops, 81 valid causal events, final gate g-audit=gate_pass, and no remaining action, while retaining the no-whole-integration ceiling.",
          "selectors": [
            "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/audit.json",
            "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/dispatch-closeout.json"
          ]
        },
        {
          "state": "append-only ledger closure",
          "evidence": "The ledger contains one dispatch row and exactly one matching close row.",
          "selectors": [
            "telemetry/agents/subagents-dispatch.yaml:6063",
            "telemetry/agents/subagents-dispatch.yaml:6077"
          ]
        }
      ],
      "important_time_layer": "STRATEGY.md lines 46-53 truthfully preserve the earlier pre-registration state. Later receipts and ledger rows show subsequent advancement. These records must be presented as different time layers, not harmonized by rewriting the strategy snapshot.",
      "time_layer_selector": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/STRATEGY.md:44-57"
    },
    "beginner_retell": [
      "First decide whether several agents are genuinely needed.",
      "Use Inventory for leads, never permission.",
      "Persist one exact sheet describing lanes, identities, scopes, dependencies, gates, and stops.",
      "Let machines reject malformed or clone-like routes before involving the human.",
      "Ask the human to authorize the reviewed material strategy.",
      "Register that exact authorized route.",
      "Run only dependency-ready waves and admit attributable receipts.",
      "Do not let the writer proceed until evidence closure says what is bound, deferred, killed, or blocked.",
      "Audit the resulting findings, then let the declared final approver decide the typed exit.",
      "Append one close row that records what actually happened without inflating it into truth, publication, or production."
    ],
    "status_residue": [
      "The constitution surface is explicitly status=draft and version=0.8.2-proposal. The live operational contract is the current adapter, research owner, tension owner, and registrar; do not describe the proposal prose as fully promoted constitutional authority.",
      "The current strategy Inventory packet is ready_with_residue, has partial declared coverage, a preexisting modified index, and 153 historical-tag warnings.",
      "The Inventory entry for the August 12 witness retained an older unexecuted state after direct receipts showed closeout. Direct receipts and ledger rows override that stale read model while both time layers remain visible.",
      "A completed lifecycle establishes bounded process evidence, not the semantic truth of findings."
    ],
    "source_bindings": [
      {
        "path": "ops/development/2026-08-13-agent-orchestration-beginner-guide/dispatch-sheet.json",
        "sha256": "b2f2057a2d268dd458a185b2ca3589e70a06f74028a19bd8bfbdc134de2958f4"
      },
      {
        "path": "ops/development/2026-08-13-agent-orchestration-beginner-guide/strategy-inventory-packet.json",
        "sha256": "7b51a5cf5dfa0acdcc567f361edfc77b38107df7947734765463370d0bf874c9"
      },
      {
        "path": "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md",
        "sha256": "327187d7cc3556a1c061caff4ca315923d2eec0415f0b3edd8eb9ea5dee06f3a"
      },
      {
        "path": "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md",
        "sha256": "de349856edfa0d25a150b43f2f4c4c1e3cbcb2b2a622fe918dfbe5ac89813198"
      },
      {
        "path": "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/SKILL.md",
        "sha256": "db30a23d55df8b103a41aaea1a7c7c04c219568ad121f1a2dd8cd531c5ea7593"
      },
      {
        "path": "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/check-tension/SKILL.md",
        "sha256": "4bc9240f3abb2d06d052fda10e443284953df9fd931bbf9c099cb61131f3f51e"
      },
      {
        "path": "implementation/domainspec/internal_tools/subagents-dispatch-hooks/constitution/subagents-strategy-constitution-proposal.md",
        "sha256": "6946057328c8fe5d31e4e87ef4b71ae2774f2bdff196380bdc33b35f3bb22ee8"
      }
    ]
  },
  "validation": "pass",
  "blockers": [],
  "residue": [
    "No filesystem receipt was written because this action's write scope is empty; the parent owns persistence at receipts/explorer-strategy-gates.json.",
    "No readiness validator, tension gate, registration, ledger append, confirmation, or spawn was performed by this explorer."
  ],
  "claim_ceiling": "Current-source strategy and human-gate lifecycle evidence plus one historical ledger-bound witness. This does not establish the current dispatch's readiness or completion and grants no authority, mutation, promotion, publication, release, deployment, or production claim."
}


## Agent 5 — Spivak, David — Dispatch Spec graph

## Bounded explorer receipt

Action `spawn-0005` passed read-only with no changed paths or blockers.

### Beginner-readable graph model

A Dispatch Spec is a typed route description, not proof that the route ran.

| Element | Meaning |
|---|---|
| Step | A graph node naming one capability, mode, pattern, typed inputs, outputs, and stops. |
| Pattern | The node’s coordination shape: sequential, fan-out, dialectic, validation, synthesis, handoff, and related forms. |
| Typed input/output | Named edges such as artifact, receipt, decision, handle, or frame. Later steps must consume an admissible source. |
| Role | A bounded responsibility slot projected onto one or more steps; it is not an agent identity or semantic authority. |
| Capability target/mode | The governing capability plus exact object and operation delegated to that role. |
| Wave | Roles admitted together after earlier dependencies pass. |
| Dependency | A declared ordering relation at step, role, and wave levels, backed by consumption of an upstream receipt. |
| Join | The rule for collecting a wave’s declared returns before evaluating its gate. |
| Gate | An owner-controlled transition predicate, optionally bound to one wave and its exact required receipts. |
| Write scope | The repository-relative mutation ceiling. Read-only roles cannot declare one; concurrent scopes cannot overlap. |
| Boundary evidence | Owner, handoff, receipt, namespace, and promotion-split contracts surrounding the graph. |
| Lifecycle state | Post-attempt accounting for spawn, join, close, residue, and reroute. It is not populated merely because the route validates. |
| Promotion guardrail | An explicit prohibition against treating route or execution evidence as canonical promotion authority. |

Dispatch Spec is currently declared `draft`. It validates whether a proposed route is explicit, gated, observable, and handoff-ready; it neither selects the correct capabilities nor spawns agents. See `arcanum/formulae/dispatch-spec/SKILL.md:14-25,65-101,103-174,197-201` and schema pointers `/properties/steps`, `/properties/subagent_strategy`, `/properties/gates`, `/properties/boundary_evidence`, and `/properties/subagent_lifecycle`.

### Concrete August 12 specimen

`DISPATCH-ROUTE.json` describes:

- 6 steps: explorer fan-out → synthesis → dialectic review → evidence closure → writing → audit.
- 9 delegated roles arranged into 5 execution waves.
- 6 gates, including human confirmation, four wave gates, and a promotion guardrail.
- `binding_mode: capability-bound`, `execution_owner: orchestrate`, and route-level `authorization: approved`.
- Exactly one mutation-capable role: the writer, bounded to `findings.md`.

Important non-bijection: `s4-evidence-closure` is a parent-owned route step, not a delegated role or execution wave. The reviewer gate admits that parent closure before the writer. A step therefore does not necessarily equal one agent or wave.

The same route snapshot has:

- `/subagent_lifecycle/status = "none"`
- `/subagent_lifecycle/agents = []`
- no `native_stage_receipts`

Therefore it describes an authorized executable shape, not execution evidence. The adjacent `orchestration/run-002/validation.json:1-4` records `pass` with no blocks or flags, but contains no route path, digest, validator version, or timestamp. Its standalone claim ceiling is “a pass result exists at this path,” not “these current route bytes were validated” and not “the route executed.”

### Validator checks that catch real hazards

The current validator blocks or flags:

- duplicate, self, forward, or impossible step dependencies;
- parallel steps without joins;
- dialectic/tournament nodes without roles and convergence criteria;
- validation/toy-game nodes without evidence artifacts;
- missing observability events;
- role capability/mode/input/output mismatches;
- unsafe, forbidden, or concurrently overlapping write scopes;
- role dependencies not mirrored in earlier waves or not consumed as receipts;
- non-final waves without a receipt-bound gate;
- lifecycle `pass` with wrong agent counts, incomplete joins/closes, or missing native-stage receipts;
- active reliance on deprecated command interfaces;
- unknown unqualified techniques or capabilities;
- boundary references to unknown steps;
- direct promotion from execution evidence into canonical knowledge.

Direct selectors: `validate-dispatch.py:356-720,743-805,808-959,968-1016,1022-1077`.

Two bounded blind spots remain:

1. Schema pattern value `xray` conflicts with the semantic check for `x_ray` at `validate-dispatch.py:890`; a pattern-only `xray` step may bypass the required handle/artifact-output check.
2. The validator permits parent-owned steps that are absent from capability-bound roles and waves. That can be legitimate, as with August 12 evidence closure, but ownership must be explicit elsewhere because full step-to-role coverage is not enforced.

### Minimal validator-ready skeleton

Derived from the current contract; not executed or revalidated in this lane.

```json
{
  "dispatch_id": "example-two-wave",
  "intent": {
    "raw": "Research one question, then synthesize it.",
    "objective": "Produce one bounded cited synthesis."
  },
  "mode": "sequence",
  "techniques": ["sequence"],
  "subagent_strategy": {
    "status": "required",
    "trigger": "Synthesis must consume an independently attributed explorer receipt.",
    "explanation": "One role explores; a dependent role synthesizes.",
    "binding_mode": "capability-bound",
    "execution_owner": "orchestrate",
    "roles": [
      {
        "role_id": "explorer",
        "purpose": "Collect source evidence.",
        "owns": "Explorer receipt.",
        "capability_ref": "research",
        "capability_target": "dispatch-sheet.json#explorer",
        "capability_mode": "explore",
        "agent_count": 1,
        "mutation_policy": "read-only",
        "depends_on_roles": [],
        "input_refs": ["intent.raw"],
        "output_refs": ["receipts/explorer.json"],
        "applies_to_steps": ["s1"]
      },
      {
        "role_id": "synthesizer",
        "purpose": "Synthesize admitted evidence.",
        "owns": "Synthesis receipt.",
        "capability_ref": "research",
        "capability_target": "dispatch-sheet.json#synthesizer",
        "capability_mode": "synthesize",
        "agent_count": 1,
        "mutation_policy": "read-only",
        "depends_on_roles": ["explorer"],
        "input_refs": ["receipts/explorer.json"],
        "output_refs": ["receipts/synthesis.json"],
        "applies_to_steps": ["s2"]
      }
    ],
    "execution_waves": [
      {
        "wave_id": "explore",
        "role_ids": ["explorer"],
        "parallel": false,
        "join_policy": "all",
        "gate_after": "g-explore",
        "on_incomplete": "block"
      },
      {
        "wave_id": "synthesize",
        "role_ids": ["synthesizer"],
        "parallel": false,
        "join_policy": "all",
        "depends_on_waves": ["explore"],
        "on_incomplete": "block"
      }
    ],
    "parallelism": "mixed",
    "join_policy": "all",
    "authorization": "requires_user_permission",
    "permission_prompt": "Run this exact two-wave route?",
    "receipt_requirements": [
      "agent_id", "role_id", "spawn_status", "join_status", "close_status",
      "dispatch_id", "step_id", "capability_ref", "capability_target",
      "capability_mode", "wave_id", "write_scope", "status", "artifacts",
      "validation", "observer_status", "blockers", "residue", "reroute",
      "handoff_note"
    ]
  },
  "subagent_lifecycle": {"status": "none", "agents": []},
  "steps": [
    {
      "step_id": "s1",
      "name": "Explore",
      "capability_ref": "research",
      "capability_status": "local-extension",
      "mode": "explore",
      "pattern": "sequential",
      "parallel": false,
      "inputs": [{"kind": "intent", "ref": "intent.raw"}],
      "outputs": [{"kind": "receipt", "ref": "receipts/explorer.json"}],
      "stop_conditions": ["Stop if source evidence is unavailable."]
    },
    {
      "step_id": "s2",
      "name": "Synthesize",
      "capability_ref": "research",
      "capability_status": "local-extension",
      "mode": "synthesize",
      "pattern": "synthesis",
      "parallel": false,
      "depends_on_steps": ["s1"],
      "inputs": [{"kind": "receipt", "ref": "receipts/explorer.json"}],
      "outputs": [{"kind": "receipt", "ref": "receipts/synthesis.json"}],
      "stop_conditions": ["Stop unless the explorer receipt passes."]
    }
  ],
  "gates": [
    {
      "gate_id": "g-explore",
      "kind": "validation",
      "owner": "orchestrate",
      "condition": "The explorer is joined and its receipt passes.",
      "applies_after_wave": "explore",
      "requires_role_receipts": ["receipts/explorer.json"],
      "on_fail": "block"
    }
  ],
  "observability": {
    "dispatch_id_required": true,
    "trace_events": ["wave_ready", "agent_joined", "gate_passed"]
  },
  "promotion_guardrails": [
    "Route and execution evidence grant no semantic promotion authority."
  ]
}
```

### Source identity

- `SKILL.md`: `0aaf1750447ba9daf8b06ba5f2635c148e258ec8e983d5e82eb348fb657e8226`
- `dispatch.schema.yml`: `2875e8051838d6b498353129397af612c8f2829be3a71b36c53e465add245f67`
- `validate-dispatch.py`: `67bdb31067dfdad9f2dd065de9af9b632f45c10845e0d78bf60b6cfc57b3893f`
- capability-bound example: `cc963e435c49821967761c51026dc750d4d93591f4eff5dd9de05ab8aa62da8d`
- August 12 route: `3a647bb344a0afca39e16e35f5c4f800c23b55fffa918e16f6a9d380c005d1fb`
- adjacent validation result: `1631c9155e46a88f7e4ffd537c71bd35367a1629239430a6fe25f41e49765081`

```json
{
  "action_id": "spawn-0005",
  "dispatch_id": "2026-08-13-agent-orchestration-beginner-guide",
  "target": "ops/development/2026-08-13-agent-orchestration-beginner-guide/dispatch-sheet.json#governance_explorers-agent-1",
  "role": "explorer-dispatch-graph",
  "status": "pass",
  "mutation_policy": "read-only",
  "changed_paths": [],
  "artifact": "ops/development/2026-08-13-agent-orchestration-beginner-guide/receipts/explorer-dispatch-graph.json",
  "validation": "pass",
  "blockers": [],
  "claim_ceiling": "Route-shape and validator exploration only. No execution, semantic truth, authority, promotion, publication, deployment, or production claim follows.",
  "residue": [
    "Dispatch Spec remains draft.",
    "The inspected pass result lacks an embedded route digest and cannot independently bind current route bytes.",
    "The August 12 route snapshot contains no lifecycle or native-stage execution evidence.",
    "The xray versus x_ray semantic-check mismatch remains unresolved.",
    "No filesystem receipt was written because this action had an empty write scope; the parent owns persistence."
  ]
}
```


## Agent 6 — Polanyi, Michael — Research evidence pipeline

{
  "action_id": "spawn-0006",
  "dispatch_id": "2026-08-13-agent-orchestration-beginner-guide",
  "target": "dispatch-sheet.json#governance_explorers-agent-2",
  "role": "explorer-research-pipeline",
  "status": "pass",
  "mutation_policy": "read-only",
  "changed_paths": [],
  "result": {
    "fixed_pipeline": {
      "spine": "explorers -> synthesizer -> reviewers -> evidence closure -> writer -> auditor",
      "boundary": "Evidence closure is a strategist-owned handoff gate, not another agent role.",
      "selectors": [
        "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:49-73",
        "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:119-146"
      ]
    },
    "artifact_ownership": {
      "research.md": "A mechanically preserved verbatim transcript of explorer returns, appended by the strategist. Synthesizer and reviewer returns are excluded; the writer does not own this file.",
      "findings.md": "Writer-owned cited synthesis produced only after evidence closure returns ready. It must preserve deferred and killed rows and carry the candidate verdict matrix.",
      "selectors": [
        "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:20-25",
        "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:131-134",
        "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:198-227",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/research.md:1-5"
      ]
    },
    "evidence_closure": {
      "contracts": {
        "cited-synthesis": "Each load-bearing row binds a claim ID, immutable source identity, source-local selector, explorer return, evidence scope, and observed/executed/unverified status.",
        "exact-binding": "Adds the exact reproducible selector, anchor, or structured pointer."
      },
      "verdicts": {
        "ready": "Every required positive row is bound, deferred, or killed.",
        "needs_feedback": "A typed defect has an already-confirmed repair edge with remaining capacity.",
        "blocked": "Required evidence remains unresolved and no eligible declared repair route remains."
      },
      "selectors": [
        "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:69-117",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/evidence-closure.json#/status",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/evidence-closure.json#/claim_rows",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/evidence-closure.json#/open_obligations"
      ]
    },
    "reviewer_gates": {
      "precedent": "Find the actual owner. An owner is positive evidence yielding build-from-owned or already-deployed; no owner yields precedent-clean/novel-attempt. Precedent never emits KILL.",
      "non-vacuity": "Demand the smallest concrete witness. No witness produces KILL.",
      "definitional-soundness": "Test whether the candidate merely renames an existing concept. Tautology produces KILL.",
      "selectors": [
        "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:148-162"
      ]
    },
    "repair_routing": [
      {
        "defect": "Unread source or missing provenance, quote, selector, anchor, or pointer",
        "owner": "explorer",
        "route": "Only a predeclared synthesizer-to-explorer feedback edge; otherwise block."
      },
      {
        "defect": "Conflicting interpretation, architecture, or definition",
        "owner": "synthesizer or skeptic",
        "route": "Declared bounded zig-zag."
      },
      {
        "defect": "Citation placement, verdict formatting, structure, or wording where evidence already exists",
        "owner": "writer",
        "route": "Auditor-to-writer revision."
      },
      {
        "defect": "Approval disagreement",
        "owner": "auditor or parent",
        "route": "Never silently reassign."
      }
    ],
    "successful_run_example": {
      "run": "arcanum-cav2-wayfinding-refresh-20260812-r2",
      "trace": [
        "Three explorer returns were mechanically preserved in research.md.",
        "Synthesizer spawn-0004 completed, then three distinct skeptic actions spawn-0005 through spawn-0007 passed.",
        "Two bounded reviewer-to-synthesis repairs were used; both declared that new source research was unnecessary.",
        "Exact-binding evidence closure returned ready with bound, deferred, and killed rows and authorized the writer only at the decision-ready ceiling.",
        "Writer spawn-0008 produced findings.md. Auditor feedback requested an exact-binding provenance repair while forbidding semantic redesign and new source research.",
        "The writer revision changed findings.md from sha256 bb8cfe25... to ebbde94f...; the final auditor receipt passed against that revised digest.",
        "Parent-owned closeout then recorded coordinator complete, 81 valid causal events, final gate g-audit/pass, no next actions, and exit_reason resolved."
      ],
      "selectors": [
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/synthesis.json#/action_id",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/skeptic-precedent.json#/action_id",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/skeptic-non-vacuity.json#/action_id",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/skeptic-definitional.json#/action_id",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/evidence-closure.json:6-18",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/orchestration/run-002/feedback/round-001.json#/source_research_required",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/orchestration/run-002/feedback/auditor-writer-round-001.json#/required_repairs",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/writer-revision-001.json:3-9",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/audit.json#/artifacts",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/dispatch-closeout.json:6-11"
      ]
    },
    "typed_negative_examples": [
      {
        "claim": "EC-JOIN-METAOWNER",
        "gate": "definitional-soundness",
        "typed_negative": "The proposed durable join owner/artifact/module/registry/validator/gate was removed. Research may compute only an ephemeral non-authoritative conjunction.",
        "selector": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/findings.md:49,260-278"
      },
      {
        "claim": "EC-VERTICAL-WITNESS",
        "gate": "non-vacuity",
        "typed_negative": "NV-001 through NV-006 remained open, so the dependency-closed vertical-witness claim was killed without killing the decision-ready atlas.",
        "selector": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/findings.md:50,349-360"
      }
    ],
    "kill_semantics": "A KILL is not discarded prose. It records the candidate's intended contribution and the exact no-witness or tautology fact that zeroed it. If every candidate is killed, the writer records the typed negatives and an auditor-approved confirmed-kill close is still resolved, not an error.",
    "blocked_pre_synthesis_example": {
      "run": "bolina-formal-modeling-20260813-r1",
      "observed_state": "The explorer gate passed with three explorer receipts and a validator-clean 24-event prefix, but the synthesizer was withheld because the runtime could not emit an admissible dependent-wave run plan.",
      "correct_failure_route": "Close blocked at explorer-stage evidence, preserve research.md, closure and residue, route repair to the Orchestrate capability owner, and do not hand-author a plan or manufacture findings.md.",
      "proof_ceiling": "That run established explorer-stage research only. A valid causal prefix did not establish synthesis, review, findings, audit, model checking, or security.",
      "selectors": [
        "research/2026-08-12-bolina-domainspec-formal-modeling/PARENT-CLOSEOUT.json:7-40",
        "research/2026-08-12-bolina-domainspec-formal-modeling/PARENT-CLOSEOUT.json:42-68",
        "research/2026-08-12-bolina-domainspec-formal-modeling/orchestrate-run/final-event-validation.json:1-8",
        "research/2026-08-12-bolina-domainspec-formal-modeling/orchestrate-run/next-wave-plan-sidecar-receipt.md:13-38",
        "research/2026-08-12-bolina-domainspec-formal-modeling/orchestrate-run/next-wave-plan-sidecar-receipt.md:40-55"
      ]
    },
    "audit_vs_final_approval": {
      "audit": "The auditor evaluates findings.md against the goal, verdict matrix, citation discipline, and claim ceiling, and may return it to the writer. Audit pass concerns the research artifact.",
      "final_approval": "The sheet's declared final approver remains the parent. Parent closeout decides the dispatch lifecycle result from joined receipts and terminal evidence. Neither audit nor closeout grants semantic authority, promotion, publication, deployment, or production status.",
      "successful_run_evidence": "The r2 audit receipt binds the revised findings digest, while the separate dispatch-closeout receipt records resolved terminal lifecycle state with authority_effect none.",
      "selectors": [
        "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md:128-146",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/dispatch-sheet.json#/final_approver",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/audit.json#/artifacts",
        "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/dispatch-closeout.json:6-11"
      ]
    },
    "time_layer_warning": "The revised r2 findings still narrate its writer-time state as lacking admitted terminal auditor/closeout evidence at findings.md:362-374. Later audit and dispatch-closeout receipts establish the subsequent terminal layer. Preserve both layers; do not rewrite the earlier prose into a false contemporaneous success claim.",
    "beginner_safe_summary": "Explorers collect independent evidence. A synthesizer makes one candidate account. Three skeptics ask different questions: is it already owned, does a concrete witness exist, and is it genuinely distinct? Evidence closure checks that every retained claim is bound, explicitly deferred, or killed before writing. The writer turns that closed package into cited findings; the auditor checks only those findings. The parent then decides whether the dispatch itself can close. Missing evidence goes back to the stage that owns it, never into smoother prose."
  },
  "source_status": [
    {
      "path": "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/research/SKILL.md",
      "sha256": "de349856edfa0d25a150b43f2f4c4c1e3cbcb2b2a622fe918dfbe5ac89813198",
      "status_ceiling": "live private research-type owner"
    },
    {
      "path": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/research.md",
      "sha256": "258691ecfd4bf8004acddc1559b28b19c643974427ad7644c7538cc604b21e5b",
      "status_ceiling": "strategist-owned explorer transcript"
    },
    {
      "path": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/findings.md",
      "sha256": "ebbde94feb8e7279daa98c8cb4469f5421419bce27f23769b0f822f9ef28815e",
      "status_ceiling": "audited decision-ready findings with preserved writer-time status layer"
    },
    {
      "path": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/dispatch-closeout.json",
      "sha256": "527f5ee82bdca175d85178685633df78cfea4fb618139d222e60d653b707f72c",
      "status_ceiling": "terminal lifecycle evidence for that bounded run"
    },
    {
      "path": "research/2026-08-12-bolina-domainspec-formal-modeling/PARENT-CLOSEOUT.json",
      "sha256": "30007600b4111f9509ced8a588d81f7ee8c4ad497a3c8608ff6d246d6dff30f7",
      "status_ceiling": "historical blocked-run closeout only"
    }
  ],
  "validation": "pass",
  "blockers": [],
  "claim_ceiling": "Bounded research-pipeline exploration only. It establishes contract structure and the cited successful and blocked run states; it grants no authority, implementation selection, promotion, publication, deployment, production, or semantic-truth claim.",
  "residue": [
    "The strategy Inventory packet is discovery-only and ready_with_residue; its stale r2 entry must not override direct receipts.",
    "The r2 findings and later closeout are different time layers and must remain visibly separate.",
    "The Bolina evidence describes the named initial blocked run only; no claim is made here about later retries.",
    "No filesystem receipt was written because this action's write scope is empty; the parent owns persistence at receipts/explorer-research-pipeline.json."
  ]
}

## Agent 7 — Hewitt, Carl — Current Orchestrate runtime

{
  "action_id": "spawn-0007",
  "dispatch_id": "2026-08-13-agent-orchestration-beginner-guide",
  "target": "ops/development/2026-08-13-agent-orchestration-beginner-guide/dispatch-sheet.json#runtime_evidence_explorers-agent-0",
  "role": "explorer-orchestrate-runtime",
  "status": "pass",
  "mode": "explore",
  "mutation_policy": "read-only",
  "changed_paths": [],
  "result": {
    "direct_answer": "Current Orchestrate is a parent-driven, fail-closed handshake around deterministic compilation and host-native collaboration calls. The scripts persist and validate actions, causal prefixes, receipt admission, gates, dependent plans, and partial-spawn cleanup; they never invoke collaboration tools themselves. A contract-complete run therefore requires both the deterministic artifacts and the parent’s actual native host calls.",
    "mechanism": [
      {
        "stage": "preflight",
        "current_behavior": "Require exact execute grammar, canonical Dispatch Spec PASS, authorization approved or not_needed, and all four required operations from the active host catalog. A successful preflight compiles and persists only the first wave’s state, run plan, and action documents; spawn_attempt_count remains zero.",
        "selectors": [
          "arcanum/runtime/orchestrate/SKILL.md:99-122",
          "arcanum/runtime/orchestrate/hosts/codex-native.md:1-20",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py:175-219",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py:249-394",
          "arcanum/runtime/orchestrate/tests/preflight/test_preflight_contract.py:54-129",
          "arcanum/runtime/orchestrate/tests/preflight/test_preflight_contract.py:146-204"
        ]
      },
      {
        "stage": "persisted action and spawn",
        "current_behavior": "Each closed-schema spawn action binds dispatch, run, wave, step, role, ordinal, capability, target, mode, mutation ceiling, scopes, and references. prepare-spawn requires exact equality with one current run-plan action, rejects replay or an invalid dependency gate, durably appends action_attempted, then exclusively exposes one opaque host request. The parent calls collaboration.spawn_agent exactly once and record-spawn appends either host_spawn_returned with the native agent binding or host_spawn_failed.",
        "selectors": [
          "arcanum/runtime/orchestrate/schemas/action.schema.json:6-48",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py:266-315",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py:318-403",
          "arcanum/runtime/orchestrate/tests/native-driver/test_native_dispatch_driver.py:198-241"
        ]
      },
      {
        "stage": "wait, terminal observation, and logical close",
        "current_behavior": "prepare-wait derives successful action-to-agent bindings from the causal stream, registers each once, then appends wait_attempted before exposing a mailbox-wide wait request. The parent reconciles mailbox activity with list_agents. A known completion becomes agent_terminal then agent_closed; an unresolved known agent becomes wait_timed_out then one agent_interrupted and an explicit timed_out receipt.",
        "selectors": [
          "arcanum/runtime/orchestrate/SKILL.md:151-164",
          "arcanum/runtime/orchestrate/hosts/codex-native.md:105-117",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py:563-648",
          "arcanum/runtime/orchestrate/scripts/validate_run_evidence.py:193-323",
          "arcanum/runtime/orchestrate/tests/native-join/test_native_join_contract.py:85-155",
          "arcanum/runtime/orchestrate/tests/native-join/test_native_join_contract.py:176-235"
        ]
      },
      {
        "stage": "receipt admission, join, gate, and reduction",
        "current_behavior": "Normalized receipts use a closed schema. advance-wave requires a directory containing exactly one expected action-named JSON receipt and nothing else, checks shape and action identity, records each file digest in receipt-admission.json, reduces pass or non-pass outcomes, appends receipt_joined and gate_decided, validates the complete causal prefix, and only then persists state and next actions. A structurally valid non-pass receipt is admitted but forces gate_block and emits no dependents.",
        "selectors": [
          "arcanum/runtime/orchestrate/schemas/receipt.schema.json:6-27",
          "arcanum/runtime/orchestrate/schemas/receipt-admission.schema.yml:6-60",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py:1024-1183",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py:707-801",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py:823-917",
          "arcanum/runtime/orchestrate/tests/native-driver/test_native_dispatch_driver.py:652-707",
          "arcanum/runtime/orchestrate/tests/native-driver/test_native_dispatch_driver.py:894-916"
        ]
      },
      {
        "stage": "dependent-wave planning",
        "current_behavior": "A passing gate may expose a deterministic action set, but those actions are not executable until prepare-next-wave-plan validates the exact dispatch, prior plan, gate, next state, complete causal prefix, run-global action allocation, and byte-exact uncontaminated action directory. It creates the next current-wave plan exclusively and without adding a causal event. The later prepare-spawn must bind the matching earlier passed gate.",
        "selectors": [
          "arcanum/runtime/orchestrate/SKILL.md:166-182",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py:517-704",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py:417-560",
          "arcanum/runtime/orchestrate/tests/native-driver/test_native_dispatch_driver.py:709-892",
          "arcanum/runtime/orchestrate/tests/test_reduce_receipts.py:153-294"
        ]
      },
      {
        "stage": "partial-wave spawn recovery",
        "current_behavior": "After host_spawn_failed, no later action in that wave may spawn and no failed-action receipt may be fabricated. The recovery path waits only for successfully spawned siblings, closes completed siblings or interrupts unresolved ones once, requires separate evidence_closure residue for each, then emits terminal run_blocked plus a typed blocked closeout with no joins, gate, dependents, or retry. Earlier completed waves retain their evidence.",
        "selectors": [
          "arcanum/runtime/orchestrate/SKILL.md:184-209",
          "arcanum/runtime/orchestrate/hosts/codex-native.md:119-133",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py:651-1013",
          "arcanum/runtime/orchestrate/scripts/validate_run_evidence.py:325-438",
          "arcanum/runtime/orchestrate/tests/partial-wave/test_partial_wave_recovery.py:57-159"
        ]
      },
      {
        "stage": "causal evidence and residue",
        "current_behavior": "Causal events use one run identity, contiguous sequence numbers, a closed event vocabulary, and enforced ordering. The driver validates the prospective prefix under a file lock and fsyncs it before returning. Feedback, governance notes, commentary, evidence closure, and reduction notes belong to a separate residue stream and cannot satisfy runtime obligations.",
        "selectors": [
          "arcanum/runtime/orchestrate/schemas/run-event.schema.json:6-123",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py:120-263",
          "arcanum/runtime/orchestrate/scripts/validate_run_evidence.py:54-116",
          "arcanum/runtime/orchestrate/scripts/validate_run_evidence.py:119-449",
          "arcanum/runtime/orchestrate/tests/evidence-order/test_evidence_order.py:38-102",
          "arcanum/runtime/orchestrate/tests/native-driver/test_native_dispatch_driver.py:595-650",
          "arcanum/runtime/orchestrate/tests/native-driver/test_native_dispatch_driver.py:918-946"
        ]
      }
    ],
    "identity_and_replay_invariants": [
      "Action IDs are run-global, monotonically allocated spawn-0001 through spawn-9999 rather than restarting per wave.",
      "A persisted action must exactly equal one current run-plan action and be named in action_artifacts.",
      "Dispatch ID and run ID remain constant across the causal stream; action, wave, role, step, capability, and native agent bindings are checked across actions, receipts, and events.",
      "One action_attempted and one host result are allowed per action; one wait registration, terminal branch, logical close or interrupt, receipt join, and gate decision are allowed at their respective identities.",
      "Dependent actions require a previously recorded matching gate_pass; terminal run_blocked forbids continuation.",
      "Receipt-directory and next-action-directory contamination, missing entries, edited bytes, stale frontiers, or an existing exclusive output block before downstream exposure."
    ],
    "host_and_capacity": {
      "required_operations": [
        "collaboration.spawn_agent",
        "collaboration.wait_agent",
        "collaboration.interrupt_agent",
        "collaboration.list_agents"
      ],
      "optional_operation": "collaboration.send_message",
      "availability_authority": "active-host-tool-catalog",
      "current_dispatch_implication": "The active four-slot host leaves three helper slots beyond the parent, so the declared groups of at most three fit one native wave. This capacity is ambient host evidence, not encoded or enforced by the action schema, run-plan schema, host profile, or coordinator; the coordinator will compile the declared agent_count even if it exceeds currently free slots.",
      "selectors": [
        "arcanum/runtime/orchestrate/hosts/codex-native.md:5-20",
        "arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py:279-355",
        "ops/development/2026-08-13-agent-orchestration-beginner-guide/strategy-inventory-packet.json#/unresolved_gaps/4",
        "ops/development/2026-08-13-agent-orchestration-beginner-guide/strategy-inventory-packet.json#/design_consequences/0"
      ]
    },
    "insufficiency_boundaries": [
      {
        "boundary": "The coordinator’s reduce command is an offline deterministic fixture surface. Without driver handshakes, actual native host calls, joined normalized receipts, and a validator-clean causal stream, it is not live execution evidence.",
        "selectors": [
          "arcanum/runtime/orchestrate/SKILL.md:124-133",
          "arcanum/runtime/orchestrate/hosts/codex-native.md:111-117"
        ]
      },
      {
        "boundary": "The Python driver never invokes collaboration.*. A request file or prose statement therefore cannot prove the host call occurred; host_spawn_returned or host_spawn_failed must be appended from the actual result.",
        "selectors": [
          "arcanum/runtime/orchestrate/hosts/codex-native.md:73-86",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py:1-7"
        ]
      },
      {
        "boundary": "Causal events contain ordered sequence evidence but no timestamps. 'Source-time' here means durable before-call or after-call append ordering, not wall-clock provenance.",
        "selectors": [
          "arcanum/runtime/orchestrate/schemas/run-event.schema.json:6-41",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py:120-168"
        ]
      },
      {
        "boundary": "Exact receipt SHA-256 values live in receipt-admission.json; receipt_joined causal events carry only identity and status. The causal stream alone does not bind the exact receipt bytes.",
        "selectors": [
          "arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py:1085-1107",
          "arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py:1130-1162",
          "arcanum/runtime/orchestrate/schemas/run-event.schema.json:106-120"
        ]
      }
    ],
    "current_contract_residue": [
      "The active-host operation comparison is implemented by the focused preflight harness and required by the skill, but native_dispatch_coordinator.py itself has no active-tool-catalog input. The parent host layer must perform that check.",
      "Normal terminal-result normalization is described by the skill and exercised by a focused scripted-host test, but the driver exposes only generic append-event plus later receipt admission; there is no dedicated record-terminal command that atomically binds a child return, receipt creation, agent_terminal, and agent_closed.",
      "The successful last-wave reducer state becomes complete, with the final causal record normally gate_decided. The inspected runtime has no run_resolved event, successful-closeout schema, or successful closeout driver command. Only partial spawn failure has a terminal run_blocked closeout. Consequently, a separate parent-owned closeout artifact is still required before claiming a resolved dispatch lifecycle.",
      "Host profile prose at hosts/codex-native.md:92 says task_name is derived from role and action ID, while the canonical skill and implemented driver derive it from SHA-256(dispatch_id, run_id) plus action ID and deliberately exclude raw role and run prose. The implementation is the current computational behavior.",
      "The generated .agents Orchestrate package and canonical source have different hashes because their projection metadata differs. Runtime-mechanism claims here bind the clean canonical arcanum/runtime/orchestrate source at nested Arcanum commit 33d3ebfbf6c8fc5af0b9f8a481858358f33a0a67.",
      "Focused tests were inspected but not executed because this action explicitly prohibited running the runtime. Their presence establishes regression intent, not a fresh passing test result."
    ],
    "source_bindings": [
      {
        "path": "arcanum/runtime/orchestrate/SKILL.md",
        "sha256": "de002a45853414b5ebb6d64c1468cf4bc86a92bb79a6a8570ca6bca8cec347cf"
      },
      {
        "path": "arcanum/runtime/orchestrate/hosts/codex-native.md",
        "sha256": "853914dd64f8a2d971a13ba0ab64ffe38af7e2eb963d50634a2a19235645dd73"
      },
      {
        "path": "arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py",
        "sha256": "39359a3cf0c6a937d253e29b71867eaa35b168d5d5d10f8e3f38c619ded39a1f"
      },
      {
        "path": "arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py",
        "sha256": "c2c77b16447a456d6e613c61b795c6beb80d188b4d859190fd7f14621beedd7a"
      },
      {
        "path": "arcanum/runtime/orchestrate/scripts/validate_run_evidence.py",
        "sha256": "d8d699c2d31328d51c3f2c845fb955f6cf599d2c4b7f9c799666b7cdc617ef06"
      },
      {
        "path": "arcanum/runtime/orchestrate/schemas/action.schema.json",
        "sha256": "43b52d8c0cec7b9bf10ad4c518801084e8c09e10bc74b1353f1c76f5c1ac4794"
      },
      {
        "path": "arcanum/runtime/orchestrate/schemas/receipt.schema.json",
        "sha256": "8eeb4acb6274a7343aa4ad3d89f1705af660dc8b82883028927eb15198e694e4"
      },
      {
        "path": "arcanum/runtime/orchestrate/schemas/run-event.schema.json",
        "sha256": "866137d3c42cd8f0db762bd7a4fa2064412f50a09ecd29fc83996cc94ce3eaf9"
      },
      {
        "path": "arcanum/runtime/orchestrate/schemas/run-plan.schema.json",
        "sha256": "7b1f09c7035aa3b5a93ac3db35dd2d0223906c6de95a7eb9796f14a4fc920149"
      }
    ],
    "beginner_safe_summary": "Think of Orchestrate as an evidence-locked dispatcher. First it writes a ticket for each allowed job. Before handing a ticket to a worker, it records that the call is about to happen. After the host returns, it binds the real worker ID. It waits for the whole wave, closes or times out every known worker, admits exactly the expected receipts, and only then decides the gate. A passing gate produces the next tickets, but those tickets need a fresh exact wave plan before use. If spawning fails halfway through, it cleans up the workers that did start and closes the run blocked instead of pretending the wave completed."
  },
  "validation": "pass",
  "blockers": [],
  "claim_ceiling": "Current-source computational and contract exploration only. No runtime command or test suite was executed, no current dispatch completion is established, and no authority, semantic truth, promotion, publication, deployment, or production claim follows.",
  "residue": [
    "No filesystem receipt was written because this action had an empty write scope; the parent owns persistence at ops/development/2026-08-13-agent-orchestration-beginner-guide/receipts/explorer-orchestrate-runtime.json.",
    "Successful terminal closeout beyond reducer state complete remains unverified because the inspected current runtime package contains no dedicated successful-closeout operation.",
    "Host-capacity enforcement remains external to the deterministic coordinator."
  ]
}


## Agent 8 — Shannon, Claude — Causal evidence

{
  "action_id": "spawn-0008",
  "dispatch_id": "2026-08-13-agent-orchestration-beginner-guide",
  "target": "ops/development/2026-08-13-agent-orchestration-beginner-guide/dispatch-sheet.json#runtime_evidence_explorers-agent-1",
  "role": "explorer-causal-evidence",
  "status": "pass",
  "mutation_policy": "read-only",
  "changed_paths": [],
  "result": {
    "direct_answer": "Reliable orchestration evidence is a chain, not a single success flag: preflight admits a first wave; source-recorded events correlate host actions; normalized receipts describe bounded results; joins admit those receipts; gates authorize transitions; logical closes account for agents; and terminal closeout binds the final stream, result digests, exit, and claim ceiling. No earlier artifact proves a later stage, and non-causal residue must never be rewritten as missing history.",
    "correlation_identity": {
      "tuple": [
        "dispatch_id",
        "run_id",
        "wave_id",
        "action_id",
        "agent_id"
      ],
      "rule": "The persisted action and normalized receipt must agree on dispatch, run, wave, and action identity; after spawn, one host agent identity must remain stable through wait registration, terminal observation, logical close, and receipt admission.",
      "event_order_note": "The r2 stream uses contiguous sequence numbers but no wall-clock timestamps. It proves recorded causal order, not elapsed time."
    },
    "evidence_model": [
      {
        "artifact": "preflight or root state snapshot",
        "supports": "Authorization, validation, selected first wave, eligible action set, and—where explicitly recorded—zero spawn attempts.",
        "cannot_support": "Any spawn, terminal result, later-wave transition, audit, or closeout.",
        "selectors": [
          "research/2026-08-12-bolina-domainspec-formal-modeling/orchestrate-run/preflight.json#/spawn_attempt_count",
          "research/2026-08-12-bolina-domainspec-formal-modeling/orchestrate-run/state.json#/state",
          "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/orchestration/run-002/state.json#/selected_wave_id"
        ]
      },
      {
        "artifact": "source-recorded event stream",
        "supports": "Ordered attempts, host returns, waits, terminal observations, closes, joins, gates, interrupts, failures, and run blocks when those event types are schema-valid and the exact stream digest is bound.",
        "cannot_support": "Receipt contents, artifact correctness, semantic truth, or authority. The r2 join events carry receipt status but no receipt digest.",
        "selectors": [
          "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/orchestration/run-002/events.jsonl",
          "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/orchestration/run-002/closeout.json#/causal_stream"
        ]
      },
      {
        "artifact": "normalized receipt",
        "supports": "One action's typed identity, status, validation, blockers, and exact artifact bindings.",
        "cannot_support": "That the receipt was joined, that its wave gate passed, or that the dispatch closed.",
        "selectors": [
          "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/audit.json",
          "research/2026-08-09-skillopt-arcanum-presentation/orchestration/run-001/receipts/spawn-0009.json"
        ]
      },
      {
        "artifact": "receipt_joined event",
        "supports": "Admission of an action result into one reduction under the recorded identity and receipt status.",
        "cannot_support": "The exact receipt bytes by itself because the inspected r2 event schema records no receipt digest.",
        "selector": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/orchestration/run-002/events.jsonl#sequences-21-23,34,57-59,70,80"
      },
      {
        "artifact": "gate_decided event",
        "supports": "The required and admitted action sets and the transition decision for one wave.",
        "cannot_support": "Execution of the dependent wave; that requires later action and host events.",
        "selector": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/orchestration/run-002/events.jsonl#sequences-24,35,60,71,81"
      },
      {
        "artifact": "agent_closed event",
        "supports": "Logical lifecycle accounting after terminal observation.",
        "cannot_support": "Receipt admission, wave completion, dispatch closeout, or semantic acceptance.",
        "selector": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/orchestration/run-002/events.jsonl#event-agent_closed"
      },
      {
        "artifact": "terminal closeout",
        "supports": "A typed bounded exit when it binds the exact causal-stream digest/count, final gate, zero next actions, result digests, and authority ceiling.",
        "cannot_support": "Claims above its declared ceiling, including semantic truth, promotion, publication, deployment, or production.",
        "selectors": [
          "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/orchestration/run-002/closeout.json",
          "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/receipts/dispatch-closeout.json"
        ]
      },
      {
        "artifact": "separate residue or writer-time prose",
        "supports": "A blocker, diagnostic, recovery route, or the writer's contemporaneous knowledge state.",
        "cannot_support": "A missing causal event or a later terminal state. It must stay outside the event stream and retain its time layer.",
        "selectors": [
          "research/2026-08-12-bolina-domainspec-formal-modeling/orchestrate-run/residue.jsonl",
          "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/findings.md:362-374"
        ]
      }
    ],
    "run_comparison": {
      "arcanum_cav2_r2_success": {
        "identity": {
          "dispatch_id": "2026-08-12-arcanum-cav2-wayfinding-refresh-r2-route",
          "run_id": "arcanum-cav2-wayfinding-refresh-20260812-r2"
        },
        "root_snapshot": {
          "state": "wave_ready",
          "selected_wave_id": "explorers",
          "sha256": "085387b9d390e91241b4196b0c9e077b6729fe4c01034604df227a7eb1de5e18",
          "interpretation": "Initial-wave snapshot only, not current terminal state."
        },
        "causal_stream": {
          "sha256": "990af1e4b19328c8e85c775a926e9db4802dcb3cbb7afb3a7b51e0a2ec1b5ee2",
          "events": 81,
          "sequence_range": "1..81 contiguous",
          "actions": 9,
          "unique_agent_ids": 9,
          "joins": 9,
          "gates": 5,
          "terminal_gate": "g-audit/gate_pass",
          "observed_counts": {
            "action_attempted": 9,
            "host_spawn_returned": 9,
            "agent_wait_registered": 9,
            "agent_terminal": 9,
            "agent_closed": 9,
            "receipt_joined": 9,
            "gate_decided": 5,
            "wait_attempted": 22
          }
        },
        "artifact_binding": {
          "writer_original_findings_sha256": "bb8cfe250a854f1045c53521623aa6d8c13de5eecdaa4ca4cd38a5e333680db7",
          "writer_revision_receipt_sha256": "6e024edd92eed79062a174b9558ad46b54326866caf6822fbb40cdd6b4a0d44d",
          "final_findings_sha256": "ebbde94feb8e7279daa98c8cb4469f5421419bce27f23769b0f822f9ef28815e",
          "audit_receipt_sha256": "e356f5be842aeb9883f06f3f53c9f15ac5309c3b91f9ddc9c0daf5fffb8822ef",
          "runtime_closeout_sha256": "a85ec784e9ab34e7d2770cb58b3ea9c24b9868a4ced0bfd39f109c5bcdc4eae1",
          "dispatch_closeout_sha256": "527f5ee82bdca175d85178685633df78cfea4fb618139d222e60d653b707f72c"
        },
        "terminal_claim": "The exact nine-agent research run closed resolved with five passed gates and zero next actions. It produced an audited decision-ready atlas and one terminal Orchestrate canary for this dispatch only.",
        "cannot_claim": "No dependency-closed semantic vertical, whole integration, implementation readiness, authority change, publication, deployment, or production acceptance.",
        "validation_residue": "No separately persisted r2 event-validation receipt was found. orchestration/run-002/validation.json is the small route-shape pass artifact, while event validation is asserted inside closeout.json#/causal_stream/validation. The stream digest and counts match the closeout, but this explorer did not rerun the formal validator."
      },
      "bolina_blocked_layers": {
        "identity": {
          "initial_dispatch_id": "2026-08-12-bolina-domainspec-formal-modeling-route",
          "initial_run_id": "bolina-formal-modeling-20260813-r1"
        },
        "preflight": {
          "status": "pass",
          "state": "wave_ready",
          "run_plan_emitted": true,
          "spawn_attempt_count": 0,
          "sha256": "30b0299d5bef3d23230959ad616a0703eac9702ce1305a3f4a201149264195b1"
        },
        "initial_closeout_layer": {
          "terminal_stage": "explorer gate passed; dependent synthesizer action withheld",
          "validated_prefix_events": 24,
          "prefix_sha256": "e5c0c4ba664ab3d861303ca5431e0de202dbda4d5495478c5d2c568c75677f1e",
          "parent_closeout_sha256": "30007600b4111f9509ced8a588d81f7ee8c4ad497a3c8608ff6d246d6dff30f7",
          "claim_ceiling": "Explorer-stage research only."
        },
        "same_run_resume_layer": {
          "current_stream_events": 50,
          "current_stream_sha256": "7eb402c074ec3fafb092d49e2e8e68430b7e119c40066f6dd4df4668856e115a",
          "events_added": "Synthesizer completed and g-synthesis passed; reviewer spawn-0007 then failed at host capacity, siblings spawn-0005 and spawn-0006 were interrupted, and run_blocked closed the wave.",
          "validator_receipt_sha256": "f816b09e96d6010735663982c9edc4e6d344184ace8123c20984b408eb4ddebb",
          "parent_closeout_sha256": "3fd98964fc67f173266fa4cd3d25e0293208d1d6155622559f4b27b47c500f6e",
          "claim_ceiling": "Source-grounded synthesis only; reviewers did not close."
        },
        "time_layer_warning": "The initial PARENT-CLOSEOUT.json still names events.jsonl at the 24-event digest, but that path now contains the appended 50-event stream. The digest and closeout timestamp identify the historical prefix; the current path alone does not. Never describe the original missing-plan defect as the repository's current terminal state.",
        "later_status": "Separate retry r2 closed with an independence error, and retry r3 later closed_resolved as bounded source-bound research. PARENT-CLOSEOUT-RETRY-003.json has sha256 0bcf9ee28f031afe858a59ce050d8412e2694881bb6eef501bd12849908befce. Even that later success proves no model or solver execution, theorem, Zig conformance, security, authority, publication, deployment, or production readiness."
      },
      "skillopt_research_pass_evidence_block": {
        "identity": {
          "dispatch_id": "2026-08-09-skillopt-arcanum-presentation-research-route",
          "run_id": "20260809T232823Z-skillopt-arcanum-presentation-001"
        },
        "root_snapshot": {
          "state": "wave_ready",
          "selected_wave_id": "explorers",
          "sha256": "d601b089c1c342d759b0cebfb28d220f9e9e2ac485d080014759be6193830608"
        },
        "result_evidence": {
          "reduce_auditor_state": "complete",
          "reduce_auditor_state_sha256": "0e6d1190e1493e948a9e9904825897097607a436582b12b218a27d7e5a2e4093",
          "findings_sha256": "2547fa615f31c1f20fa74b6e428ae16bb55d52deed72c187f4c60324d26a8a1a",
          "auditor_receipt_sha256": "98b452eb25aa6d448b14b83861775bb71ac813e4ae0df7624819f55267c7e671",
          "auditor_verdict": "recommend_accept"
        },
        "causal_evidence": {
          "raw_stream_sha256": "9c94545470e77f8b2d3de5af098093844adf91b705297cb5575e5c28d16dfb63",
          "events": 64,
          "sequence_range": "1..64 contiguous",
          "validator_status": "block",
          "validation_receipt_sha256": "316dbbf68d11363c8d1f286f4b52cf126485c9272352bb31af6245dd6b7b73f2",
          "defects": [
            "All 64 events lack schema_version and wave_id.",
            "Some events also lack required action_id or agent_id.",
            "The stream contains no receipt_joined or gate_decided events.",
            "A canonical passing stream cannot be produced from later receipts and reducer artifacts without unsupported historical synthesis."
          ]
        },
        "terminal_disposition": {
          "status": "closed_with_error",
          "research_result": "Preserved as auditor-accepted presentation research substrate.",
          "orchestration_result": "Not validated.",
          "canonical_events_created": false,
          "renewed_acceptance_required": true,
          "evidence_closeout_sha256": "1027e1227399bf078bdb1ba5feb824b5ed92b76c56cd48897dc2f734fd91ce6f",
          "parent_closeout_sha256": "af45d61e74796caf4f9d5c678f554fa7456b211843c76619517d145ff72b83b3"
        },
        "lesson": "A complete reducer state and a valid normalized auditor receipt can support the research artifact while the orchestration-proof claim remains blocked. Result evidence and execution-history evidence are independent dimensions."
      }
    },
    "time_layer_warnings": [
      "R2 findings.md:362-374 truthfully says at writer time that the auditor and terminal closeout were absent and NV-006 remained open. Later audit and closeout receipts close only that later runtime layer; rewriting the findings prose would falsify chronology.",
      "Root state.json files in all three examples are first-wave snapshots. Treating them as mutable current-state ledgers would incorrectly erase later waves or terminal errors.",
      "Bolina's original 24-event closeout and appended 50-event retry share a path and run ID but have different exact digests and terminal meanings.",
      "SkillOpt's accepted findings do not cure its invalid causal stream; conversely, its event-evidence block does not erase the separately bounded research result."
    ],
    "beginner_retell": [
      "A plan says what should happen.",
      "Preflight says the first step is allowed to start.",
      "Events say what the coordinator recorded around host operations.",
      "A receipt says what one agent returned.",
      "A join says that receipt was admitted.",
      "A gate says the next wave may or may not open.",
      "A logical close accounts for one agent; it is not the dispatch ending.",
      "Terminal closeout binds the exact run history and result at a limited claim ceiling.",
      "Residue explains failures without pretending missing events happened.",
      "If two artifacts disagree, first ask whether they describe different times or different proof dimensions."
    ]
  },
  "source_status": [
    {
      "path": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/orchestration/run-002/events.jsonl",
      "sha256": "990af1e4b19328c8e85c775a926e9db4802dcb3cbb7afb3a7b51e0a2ec1b5ee2",
      "status_ceiling": "Exact terminal causal stream for that bounded r2 run"
    },
    {
      "path": "ops/development/2026-08-12-arcanum-cav2-integration-wayfinding-refresh-r2/orchestration/run-002/closeout.json",
      "sha256": "a85ec784e9ab34e7d2770cb58b3ea9c24b9868a4ced0bfd39f109c5bcdc4eae1",
      "status_ceiling": "Terminal runtime closeout receipt"
    },
    {
      "path": "research/2026-08-12-bolina-domainspec-formal-modeling/PARENT-CLOSEOUT.json",
      "sha256": "30007600b4111f9509ced8a588d81f7ee8c4ad497a3c8608ff6d246d6dff30f7",
      "status_ceiling": "Historical initial 24-event blocked layer only"
    },
    {
      "path": "research/2026-08-12-bolina-domainspec-formal-modeling/PARENT-CLOSEOUT-RETRY-001.json",
      "sha256": "3fd98964fc67f173266fa4cd3d25e0293208d1d6155622559f4b27b47c500f6e",
      "status_ceiling": "Historical 50-event partial-wave blocked layer"
    },
    {
      "path": "research/2026-08-09-skillopt-arcanum-presentation/orchestration/run-001/evidence-closeout-decision.json",
      "sha256": "1027e1227399bf078bdb1ba5feb824b5ed92b76c56cd48897dc2f734fd91ce6f",
      "status_ceiling": "Research-result preservation plus orchestration-evidence block"
    },
    {
      "path": "research/2026-08-09-skillopt-arcanum-presentation/PARENT-CLOSEOUT.json",
      "sha256": "af45d61e74796caf4f9d5c678f554fa7456b211843c76619517d145ff72b83b3",
      "status_ceiling": "Closed-with-error parent disposition"
    }
  ],
  "validation": "pass",
  "validation_details": "Read-only JSON parsing, SHA-256 comparison, sequence/count checks, identity correlation, and artifact-pointer inspection passed. No runtime, event-stream reconstruction, formal validator, registration, ledger mutation, or repository write was performed.",
  "blockers": [],
  "claim_ceiling": "Historical causal-evidence exploration only. It supports the cited bounded run states and their temporal separation; it grants no semantic authority, implementation decision, promotion, publication, deployment, production, or current-runtime conformance claim.",
  "residue": [
    "The r2 event stream does not embed normalized-receipt digests, so exact join-to-receipt byte binding requires the separate receipt and closeout artifacts.",
    "The r2 run has no separately persisted event-validation receipt; its terminal closeout carries the validation assertion.",
    "The original Bolina closeout's path now resolves to later appended bytes; use the recorded digest and time layer.",
    "No filesystem receipt was written because this action had an empty write scope; the parent owns persistence at receipts/explorer-causal-evidence.json."
  ]
}

## Agent 9 — Bateson, Gregory — Failure archaeology

{
  "action_id": "spawn-0009",
  "dispatch_id": "2026-08-13-agent-orchestration-beginner-guide",
  "target": "ops/development/2026-08-13-agent-orchestration-beginner-guide/dispatch-sheet.json#learning_explorers-agent-0",
  "role": "explorer-failure-archaeology",
  "status": "pass",
  "mode": "explore",
  "mutation_policy": "read-only",
  "changed_paths": [],
  "result": {
    "direct_answer": "The supplied history shows that orchestration failures are safest to understand as broken evidence or transition invariants, not generic agent failure. Missing dependent plans must stop later waves; schema-incomplete events must block orchestration proof without erasing separately valid research; partial spawn failure must close or interrupt every started sibling without fabricating receipts; stale Inventory state must yield to direct receipts; and historical prose must retain its original time layer. None of the supplied cases is a product or semantic defect.",
    "classification_summary": {
      "governance_or_evidence_mechanics": [
        "FA-01 task-name collision evidence and deterministic naming mitigation",
        "FA-02 missing dependent-wave plan",
        "FA-04 schema-incomplete causal evidence",
        "FA-05 stale Inventory closeout state",
        "FA-07 successful terminal-closeout ownership gap"
      ],
      "operational_runtime": [
        "FA-03 partial-wave host-capacity failure"
      ],
      "not_a_defect_but_a_time_layer_hazard": [
        "FA-06 historical prose and root-snapshot reinterpretation"
      ],
      "product_or_semantic_blockers": []
    },
    "failure_atlas": [
      {
        "id": "FA-01",
        "case": "Pre-r2 task-name collision and current collision-safe naming",
        "symptom": "The requested historical collision artifact was not among the four supplied inputs. The available runtime receipt instead records the current mitigation: implemented task names derive from SHA-256(dispatch_id, run_id) plus action ID and exclude raw role and run prose. The host-profile prose still describes an older role-and-action derivation.",
        "violated_invariant": "One persisted action must map to one stable, run-scoped native task identity without collision or identity drift.",
        "fail_closed_assessment": "The current deterministic namespace is an appropriate prevention mechanism, but the original collision, its exact trigger, and its historical fail-closed behavior cannot be independently reconstructed from the supplied scope.",
        "failure_class": "governance/runtime identity defect, historical classification provisional",
        "recovery_owner": "Orchestrate runtime owner for implemented identity derivation; host-profile owner for prose synchronization.",
        "must_never_be_synthesized_after_the_fact": [
          "A missing historical collision event stream",
          "An exact original task name",
          "A claim that the original failure had one specific cause beyond the supplied evidence"
        ],
        "permanent_regression_lesson": "Derive native task names from immutable dispatch and run identity plus the run-global action ID; validate uniqueness before host exposure; keep host-profile prose aligned with implemented behavior.",
        "current_status": "Current implementation reports collision-resistant naming. Documentation drift remains. Original failure archaeology remains evidence-incomplete.",
        "evidence": [
          "receipts/explorer-orchestrate-runtime.json#/verbatim_return(parsed)/result/current_contract_residue/3",
          "receipts/explorer-orchestrate-runtime.json#/verbatim_return(parsed)/result/identity_and_replay_invariants/0",
          "strategy-inventory-packet.json#/selected_entries/0/summary",
          "receipts/explorer-causal-evidence.json#/verbatim_return(parsed)/result/run_comparison/arcanum_cav2_r2_success"
        ]
      },
      {
        "id": "FA-02",
        "case": "Bolina missing dependent-wave plan",
        "symptom": "Preflight and the explorer wave passed, but the synthesizer action was withheld because no valid dependent-wave plan existed.",
        "violated_invariant": "A passed gate may expose eligible actions, but dependent actions are not executable until an exact current-wave plan binds the dispatch, prior plan, gate, next state, causal prefix, run-global action allocation, and uncontaminated action bytes.",
        "fail_closed_assessment": "Withholding synthesis was correct because a passed gate alone does not authorize a host spawn. The historical contract was incomplete because it could not produce the required next-wave plan.",
        "failure_class": "governance-only orchestration transition defect",
        "recovery_owner": "Parent Orchestrate driver using the deterministic dependent-wave planning boundary.",
        "must_never_be_synthesized_after_the_fact": [
          "A synthesizer spawn",
          "A synthesizer receipt",
          "A later gate",
          "Findings attributed to a wave that never ran"
        ],
        "permanent_regression_lesson": "Make dependent-wave planning an explicit persisted precondition and require later prepare-spawn to bind the matching earlier gate_pass.",
        "current_status": "Historical initial layer blocked after 24 validated events. The current contract includes prepare-next-wave-plan. The same run later advanced to synthesis before a separate host-capacity failure; a later retry r3 closed as bounded research.",
        "evidence": [
          "strategy-inventory-packet.json#/selected_entries/3",
          "receipts/explorer-orchestrate-runtime.json#/verbatim_return(parsed)/result/mechanism/4",
          "receipts/explorer-causal-evidence.json#/verbatim_return(parsed)/result/run_comparison/bolina_blocked_layers/initial_closeout_layer",
          "receipts/explorer-causal-evidence.json#/verbatim_return(parsed)/result/run_comparison/bolina_blocked_layers/later_status"
        ]
      },
      {
        "id": "FA-03",
        "case": "Bolina partial reviewer-wave spawn failure at host capacity",
        "symptom": "After synthesis passed, reviewer spawn-0007 failed at host capacity. Already spawned siblings spawn-0005 and spawn-0006 were interrupted, and run_blocked closed the wave.",
        "violated_invariant": "After host_spawn_failed, no later action in that wave may spawn, no failed-action receipt may be fabricated, and every successfully spawned sibling must reach terminal accounting or one interruption with separate residue.",
        "fail_closed_assessment": "Stopping the wave, accounting for siblings, emitting no joins or gate, and preserving earlier completed waves was correct. Prevention remains incomplete because active free-slot capacity is ambient host evidence and is not enforced by the coordinator.",
        "failure_class": "operational host/runtime blocker, not governance-only and not product-semantic",
        "recovery_owner": "Parent host layer for capacity-aware scheduling; Orchestrate runtime for deterministic partial-wave cleanup.",
        "must_never_be_synthesized_after_the_fact": [
          "A receipt for the action that failed to spawn",
          "Successful reviewer results for interrupted siblings",
          "A reviewer gate",
          "A retry appended as though it belonged to the blocked wave"
        ],
        "permanent_regression_lesson": "Bound wave size to verified active host capacity before exposure, then retain fail-closed partial-wave recovery for capacity changes or host failures after planning.",
        "current_status": "The historical 50-event layer closed blocked. Current Orchestrate specifies partial-wave recovery, but capacity enforcement remains external to the coordinator.",
        "evidence": [
          "strategy-inventory-packet.json#/unresolved_gaps/4",
          "strategy-inventory-packet.json#/design_consequences/0",
          "receipts/explorer-orchestrate-runtime.json#/verbatim_return(parsed)/result/mechanism/5",
          "receipts/explorer-orchestrate-runtime.json#/verbatim_return(parsed)/result/host_and_capacity",
          "receipts/explorer-causal-evidence.json#/verbatim_return(parsed)/result/run_comparison/bolina_blocked_layers/same_run_resume_layer"
        ]
      },
      {
        "id": "FA-04",
        "case": "SkillOpt schema-incomplete event evidence",
        "symptom": "The 64-event stream was contiguous but every event lacked schema_version and wave_id; some lacked action_id or agent_id; and no receipt_joined or gate_decided events existed.",
        "violated_invariant": "Causal evidence must use one run identity, the closed event vocabulary, required correlation fields, contiguous order, and explicit join and gate transitions.",
        "fail_closed_assessment": "Blocking the orchestration-proof claim while preserving the separately auditor-accepted research artifact was correct. The capture workflow was incomplete because later receipts and reducer state could not repair missing source-time history.",
        "failure_class": "governance-only evidence defect",
        "recovery_owner": "Evidence-closure and parent closeout owners; renewed owner acceptance is required for any repaired candidate evidence.",
        "must_never_be_synthesized_after_the_fact": [
          "Canonical replacement events",
          "Missing joins",
          "Missing gate decisions",
          "Action or agent identities not recorded at source time"
        ],
        "permanent_regression_lesson": "Validate closed-schema causal events as they are appended and preserve result correctness and execution-history correctness as independent proof dimensions.",
        "current_status": "Research result preserved; orchestration result closed_with_error; canonical events were not reconstructed; renewed acceptance required.",
        "evidence": [
          "strategy-inventory-packet.json#/selected_entries/4",
          "receipts/explorer-causal-evidence.json#/verbatim_return(parsed)/result/run_comparison/skillopt_research_pass_evidence_block",
          "receipts/explorer-orchestrate-runtime.json#/verbatim_return(parsed)/result/mechanism/6"
        ]
      },
      {
        "id": "FA-05",
        "case": "Inventory closeout state remained stale after direct r2 completion",
        "symptom": "The selected Inventory entry still describes the August 12 r2 route as unexecuted even though direct audit and closeout receipts establish a later completed run.",
        "violated_invariant": "Inventory is a discovery read model, not execution authority; status claims must resolve to direct current evidence and retain temporal provenance.",
        "fail_closed_assessment": "Refusing to treat the stale Inventory state as authoritative is correct. The closeout-to-Inventory refresh workflow remains incomplete.",
        "failure_class": "governance-only read-model defect",
        "recovery_owner": "Inventory refresh owner, without altering the historical direct receipts.",
        "must_never_be_synthesized_after_the_fact": [
          "A claim that Inventory itself proves execution",
          "A rewritten historical receipt",
          "A merged status that erases when each artifact was true"
        ],
        "permanent_regression_lesson": "Make terminal closeout detectable by Inventory refresh or drift checks, and always surface direct receipts as the higher-confidence source.",
        "current_status": "Open residue in the current strategy packet; direct r2 closeout overrides the stale discovery entry.",
        "evidence": [
          "strategy-inventory-packet.json#/selected_entries/0/use_boundary",
          "strategy-inventory-packet.json#/unresolved_gaps/1",
          "strategy-inventory-packet.json#/residue/2",
          "strategy-inventory-packet.json#/non_authority_notice"
        ]
      },
      {
        "id": "FA-06",
        "case": "Historical findings prose and root snapshots appear stale after later execution",
        "symptom": "The r2 writer-time findings correctly said audit and terminal closeout were absent, while later receipts closed those stages. Root state.json files likewise record first-wave snapshots rather than mutable terminal state.",
        "violated_invariant": "Evidence from different times and proof dimensions must not be silently harmonized.",
        "fail_closed_assessment": "Keeping the original prose and snapshots unchanged is correct. Treating them as current terminal truth would be an interpretive failure, not a reason to rewrite history.",
        "failure_class": "time-layer interpretation hazard, not itself a governance or product defect",
        "recovery_owner": "Synthesizer or guide writer must add explicit temporal qualifiers and cite later closeout artifacts separately.",
        "must_never_be_synthesized_after_the_fact": [
          "Later audit knowledge inside earlier writer prose",
          "A mutable terminal meaning for the initial root snapshot",
          "One blended digest for historical prefixes and later appended streams"
        ],
        "permanent_regression_lesson": "Teach readers to ask whether apparently conflicting artifacts describe different times or different proof dimensions; bind every historical layer by exact digest.",
        "current_status": "Resolved by temporal separation in the causal-evidence receipt; the original artifacts should remain unchanged.",
        "evidence": [
          "receipts/explorer-causal-evidence.json#/verbatim_return(parsed)/result/time_layer_warnings",
          "receipts/explorer-causal-evidence.json#/verbatim_return(parsed)/result/run_comparison/arcanum_cav2_r2_success/root_snapshot",
          "receipts/explorer-causal-evidence.json#/verbatim_return(parsed)/result/run_comparison/bolina_blocked_layers/time_layer_warning"
        ]
      },
      {
        "id": "FA-07",
        "case": "Current successful-runtime closeout remains parent-owned",
        "symptom": "The last successful reducer transition becomes state complete, but the inspected runtime has no run_resolved event, successful-closeout schema, or successful-closeout driver command.",
        "violated_invariant": "A final passed gate or complete reducer state does not itself bind the exact causal stream, result digests, terminal disposition, and claim ceiling.",
        "fail_closed_assessment": "Refusing to claim dispatch completion from reducer state alone is correct. The runtime contract remains incomplete at the successful terminal edge and requires a separate parent-owned closeout artifact.",
        "failure_class": "governance/runtime lifecycle residue",
        "recovery_owner": "Parent closeout owner; any future runtime-owned closeout design belongs to Orchestrate authority.",
        "must_never_be_synthesized_after_the_fact": [
          "A run_resolved event that was never recorded",
          "A successful closeout receipt inferred only from gate_pass",
          "Receipt-byte bindings inferred from receipt_joined events, which carry status but not receipt digests"
        ],
        "permanent_regression_lesson": "Keep final gate, complete reduction, and terminal closeout distinct; bind exact stream and artifact digests in a typed closeout before making a resolved-dispatch claim.",
        "current_status": "Open current-contract residue. The August 12 r2 parent-owned closeout is a successful bounded control case, not proof that the runtime now owns this edge.",
        "evidence": [
          "receipts/explorer-orchestrate-runtime.json#/verbatim_return(parsed)/result/current_contract_residue/2",
          "receipts/explorer-orchestrate-runtime.json#/verbatim_return(parsed)/result/insufficiency_boundaries/3",
          "receipts/explorer-causal-evidence.json#/verbatim_return(parsed)/result/run_comparison/arcanum_cav2_r2_success/causal_stream",
          "receipts/explorer-causal-evidence.json#/verbatim_return(parsed)/result/run_comparison/arcanum_cav2_r2_success/artifact_binding"
        ]
      }
    ],
    "successful_control_case": {
      "case": "August 12 Arcanum-CAV2 r2",
      "observed_chain": "81 contiguous events, nine actions, nine unique native agent IDs, nine joins, five gates, terminal g-audit/gate_pass, and parent-owned runtime and dispatch closeouts.",
      "claim": "That exact bounded nine-agent research run closed resolved and produced an audited decision-ready atlas.",
      "claim_ceiling": "It does not establish a semantic vertical, whole integration, implementation readiness, authority change, publication, deployment, or production acceptance.",
      "important_residue": [
        "No separately persisted r2 event-validation receipt was found; validation is asserted inside closeout.json.",
        "The successful control does not fill the missing original task-name-collision artifact.",
        "Writer-time prose must not be rewritten with later audit or closeout knowledge."
      ]
    },
    "beginner_failure_rules": [
      "If the next-wave ticket was never validly written, the next worker must not start.",
      "If a worker never started, never invent its receipt.",
      "If only part of a wave started, account for or interrupt those workers and close blocked.",
      "Good findings do not repair bad execution history, and bad execution history does not automatically erase separately supported findings.",
      "Inventory helps find evidence; it does not outrank direct receipts.",
      "A final gate is not the same thing as terminal closeout.",
      "When artifacts disagree, first separate their time layers and proof dimensions."
    ],
    "regression_evidence_boundary": {
      "direct_regression_receipt_supplied": false,
      "reported_regression_intent": "The runtime explorer cites focused tests for dependent-wave planning, evidence ordering, native joins, and partial-wave recovery, but explicitly did not execute them.",
      "claim_ceiling": "The current contract and test presence support design intent only; they are not fresh regression-test results."
    }
  },
  "source_status": [
    {
      "path": "ops/development/2026-08-13-agent-orchestration-beginner-guide/dispatch-sheet.json",
      "sha256": "b2f2057a2d268dd458a185b2ca3589e70a06f74028a19bd8bfbdc134de2958f4",
      "status_ceiling": "Current action mandate and learning-explorer scope"
    },
    {
      "path": "ops/development/2026-08-13-agent-orchestration-beginner-guide/strategy-inventory-packet.json",
      "sha256": "7b51a5cf5dfa0acdcc567f361edfc77b38107df7947734765463370d0bf874c9",
      "status_ceiling": "Discovery-only failure leads and stale-status residue"
    },
    {
      "path": "ops/development/2026-08-13-agent-orchestration-beginner-guide/receipts/explorer-orchestrate-runtime.json",
      "sha256": "ce2f9646cff4e0a845f6e0ebfcceeb9d03818ef39ca58724ffdddfe07406efe7",
      "status_ceiling": "Prior explorer account of current runtime contracts and open residue; runtime and tests were not executed"
    },
    {
      "path": "ops/development/2026-08-13-agent-orchestration-beginner-guide/receipts/explorer-causal-evidence.json",
      "sha256": "ec5051e6b2599cdaf484112228a905bb029b33b1527489339af99f2e14778d7a",
      "status_ceiling": "Prior explorer account of cited historical causal layers and exact digests"
    }
  ],
  "validation": "pass",
  "validation_details": "Read and parsed only the four declared JSON inputs, including both embedded normalized explorer returns; checked dispatch, target, action, and role consistency; computed SHA-256 for each supplied input. No historical event stream, direct regression receipt, runtime command, test suite, Inventory mutation, or repository write was performed.",
  "blockers": [],
  "claim_ceiling": "Bounded failure-archaeology synthesis from the four supplied inputs only. It supports the classifications, recovery boundaries, and explicit evidence gaps above; it grants no product diagnosis, semantic authority, runtime conformance, implementation decision, repair authorization, promotion, publication, deployment, or production claim.",
  "residue": [
    "The original task-name-collision artifact and exact failing task names were not supplied, so that history remains provisional.",
    "No direct Inventory closeout-bug artifact or regression receipt was supplied beyond the strategy packet's explicit stale-state residue.",
    "Focused runtime tests were reported by the prior explorer but were not rerun.",
    "No filesystem receipt was written because this action had an empty write scope; the parent owns persistence at ops/development/2026-08-13-agent-orchestration-beginner-guide/receipts/explorer-failure-archaeology.json."
  ]
}

## Agent 10

## Bounded research return

### Reader movement

Before reading, a novice may think orchestration means “ask several agents, wait, then combine their answers.” They may treat a plan, approval, receipt, audit, and completion as roughly interchangeable.

After reading, they should be able to:

- Decide whether one bounded helper is enough or a governed dispatch is justified.
- Separate route design, human authorization, registration, execution, evidence admission, semantic judgment, and terminal accounting.
- Trace one action from persisted ticket through spawn, terminal observation, close, receipt, join, and gate.
- Find the last transition directly supported by evidence.
- Preserve partial work and historical time layers when a run stops.
- Explain why closeout proves neither truth, publication, deployment, nor production.

This movement follows Whisper’s need-before-name, earned-progression, transformed-ending, and lifecycle `retell_chain` checks.  
Evidence: `.agents/skills/whisper/SKILL.md:158-223`; `receipts/explorer-human-surfaces.json#/result/pedagogical_moves_that_worked`.

### Need-before-name order

1. One question needs work inside an already-bounded scope. Call the worker a **helper**.
2. The question needs independent viewpoints or dependent stages. Call the governed coordination lifecycle a **dispatch**.
3. People need to see why work is divided and where disagreement belongs. That explanation is the **strategy**.
4. The host needs an exact account of roles, scopes, dependencies, gates, and stops. That artifact is the **dispatch sheet**.
5. The proposed route must be checked for malformed structure and weak differentiation. These are **readiness/route validation** and two independent **tension passes**.
6. A person must authorize the exact reviewed proposal. That is **confirmation**.
7. The authorized proposal needs a durable lifecycle entry. That is **registration**.
8. Each executable job needs an immutable ticket. That is a **persisted action**.
9. Jobs that are simultaneously eligible form a **wave**; earlier results constrain later waves through **dependencies**.
10. Host operations produce a real worker binding, followed by **wait**, **terminal observation**, and logical **close**.
11. An attributable action result is a **receipt**; admitting it into reduction is a **join**.
12. The decision to expose or block the next wave is a **gate**.
13. Claim-by-claim provenance checking before writing is **evidence closure**.
14. Terminal accounting for the whole bounded run is **closeout**.

Evidence: `receipts/explorer-vocabulary.json#/verbatim_return`; `receipts/explorer-strategy-gates.json#/result/lifecycle`; `receipts/explorer-orchestrate-runtime.json#/result/mechanism`; `receipts/explorer-causal-evidence.json#/result/evidence_model`.

### One finite worked example

The user asks: “How should a beginner understand agent orchestration?”

1. The parent asks whether a single helper can answer safely. Because this question needs independent source exploration, synthesis, adversarial review, writing, and audit, it warrants a dispatch. A helper would remain one bounded lane; it would not acquire dispatch authority.  
   Evidence: `explorer-vocabulary.json#/verbatim_return`; `explorer-strategy-gates.json#/result/lifecycle/0`.

2. The strategy assigns distinct lanes for vocabulary, ownership, human gates, route shape, research flow, runtime behavior, causal evidence, failure history, and novice retelling. Inventory may suggest sources, but it neither decides nor authorizes the route.  
   Evidence: `explorer-strategy-gates.json#/result/lifecycle/1`; `explorer-owner-graph.json#/verbatim_return`.

3. One exact sheet binds agent roles, prompts, read/write boundaries, dependencies, feedback edges, loop caps, outputs, and the final approver. Dispatch Spec checks whether the proposed graph is explicit and executable in shape; validation does not spawn anything.  
   Evidence: `explorer-dispatch-graph.json#/verbatim_return`.

4. Machine readiness and two independent tension passes challenge the exact bytes. Only `PASS/PASS` may reach the person; neither pass is permission. Material changes require the checks again and may require renewed confirmation.  
   Evidence: `explorer-strategy-gates.json#/result/lifecycle/2`; `/result/lifecycle/3`; `/result/confirmation_binding`.

5. The human confirms that exact material strategy. Registration then records the authorized topology. Confirmation does not prove registration, and registration does not prove execution.  
   Evidence: `explorer-strategy-gates.json#/result/lifecycle/4`; `/result/lifecycle/5`.

6. Before host work, Orchestrate preflight requires a validated route, authorization, and the needed host operations. It persists only the first eligible wave and leaves spawn attempts at zero. Thus route validation and runtime preflight remain distinct from execution.  
   Evidence: `explorer-orchestrate-runtime.json#/result/mechanism/0`; `explorer-causal-evidence.json#/result/evidence_model/0`.

7. Each job receives an exact persisted action. Before the native spawn, the driver records the attempt; after the actual host call, it records either the real agent binding or a spawn failure. A request file alone is not spawn evidence.  
   Evidence: `explorer-orchestrate-runtime.json#/result/mechanism/1`; `/result/insufficiency_boundaries/1`.

8. Only dependency-ready actions run. Several eligible roles may form one bounded parallel wave, but later waves remain hidden until the earlier receipts are joined and their gate passes.  
   Evidence: `explorer-dispatch-graph.json#/verbatim_return`; `explorer-orchestrate-runtime.json#/result/mechanism/4`.

9. The parent waits, reconciles the actual agent identities, records terminal observation, and logically closes or interrupts each known worker. Waiting is mailbox activity; it is not receipt admission.  
   Evidence: `explorer-orchestrate-runtime.json#/result/mechanism/2`; `explorer-causal-evidence.json#/result/evidence_model/5`.

10. Exactly the expected normalized receipts are checked and joined. The gate evaluates the admitted set. A valid non-pass receipt remains evidence but blocks dependents.  
    Evidence: `explorer-orchestrate-runtime.json#/result/mechanism/3`; `explorer-causal-evidence.json#/result/evidence_model/2-4`.

11. The research spine then proceeds: explorers → synthesizer → differentiated reviewers → parent-owned evidence closure → writer → auditor. Evidence closure must classify required claims as bound, deferred, killed, or unresolved before the writer starts.  
    Evidence: `explorer-research-pipeline.json#/result/fixed_pipeline`; `/result/evidence_closure`.

12. The writer owns `findings.md`; the auditor judges that artifact. The declared final approver still owns the dispatch’s terminal acceptance. A parent closeout binds the final causal stream, artifacts, exit, residue, and claim ceiling.  
    Evidence: `explorer-research-pipeline.json#/result/artifact_ownership`; `/result/audit_vs_final_approval`; `explorer-causal-evidence.json#/result/evidence_model/6`.

13. Only after evidence-closed research exists should Whisper compose the beginner guide. That writing lifecycle is downstream work, not proof that the research ran correctly or that its claims are authoritative.  
    Evidence: `explorer-human-surfaces.json#/result/candidate_narrative_anchor`; `.agents/skills/whisper/SKILL.md:143-146,210-223`; `plain-language-guide.md:154-156`.

### Retell chain

- **Input:** A bounded user question whose answer needs coordinated independent work.
- **Transformation:** Strategy and an exact validated sheet turn the question into scoped roles, actions, dependencies, gates, and forbidden effects.
- **Immediate consequence:** Explicit confirmation permits registration and execution of only that bounded route.
- **Later lifecycle:** Native results become receipts; joins and gates admit them into synthesis, review, evidence closure, findings, audit, and parent closeout.
- **Limit:** Closeout establishes the bounded run state. It does not establish semantic truth, canonical authority, promotion, publication, deployment, or production.

Evidence: `explorer-human-surfaces.json#/result/candidate_retell_chain`; `explorer-causal-evidence.json#/result/beginner_retell`.

### Analogies and break points

- **Controlled relay:** Each runner receives a bounded baton and the next runner starts only after a handoff check.  
  Break point: passing the baton does not prove the message written on it is true; some transitions are parent-owned rather than agent-owned.  
  Evidence: `explorer-human-surfaces.json#/result/candidate_narrative_anchor`.

- **Call sheet and work tickets:** The dispatch sheet is the agreed production plan; persisted actions are the exact tickets exposed to workers.  
  Break point: a call sheet is neither permission nor evidence that anyone arrived or completed work.  
  Evidence: `explorer-dispatch-graph.json#/verbatim_return`; `explorer-orchestrate-runtime.json#/result/mechanism/1`.

- **Railway signals:** Waves are trains admitted onto bounded track segments; gates control whether the next segment opens.  
  Break point: a green signal authorizes movement but does not prove the train reached its destination or that its cargo is correct.  
  Evidence: `explorer-causal-evidence.json#/result/evidence_model/4`.

### Ten beginner misconceptions

| Misconception | Correction |
|---|---|
| Any delegated work is a dispatch. | One bounded worker is a helper; governed fan-out or dependent coordination is a dispatch. |
| Inventory tells the parent what is true or permitted. | Inventory supplies discovery leads and may be stale; direct owner evidence controls claims. |
| A valid sheet proves the route ran. | Validation proves route shape only. |
| Two tension passes authorize execution. | They qualify the proposal for explicit human confirmation. |
| Confirmation means the run is registered and running. | Confirmation, registration, preflight, and execution are separate transitions. |
| A spawned agent counts as completed work. | Completion still needs terminal observation, logical close, receipt admission, join, and gate. |
| Waiting for an agent is joining it. | Wait observes mailbox activity; join admits a checked receipt. |
| A receipt proves every claim inside it. | It proves an attributable bounded return; claim truth depends on appropriate evidence and owners. |
| Auditor approval or a final gate means closeout, publication, or production. | Audit, final gate, parent closeout, publication, deployment, and production remain distinct. |
| A failed wave means either discard everything or pretend missing work happened. | Preserve completed evidence at its exact status, fabricate nothing, close blocked, and recover through a new bounded route. |

Evidence: `explorer-vocabulary.json#/verbatim_return`; `explorer-strategy-gates.json#/result/lifecycle`; `explorer-causal-evidence.json#/result/evidence_model`; `explorer-failure-archaeology.json#/result/beginner_failure_rules`.

### Minimal useful visuals

Use only two visuals in the eventual guide:

```text
request
  → helper-or-dispatch decision
  → strategy + exact sheet
  → validation + tension
  → human confirmation
  → registration
  → persisted actions
  → spawn → wait → terminal → close
  → receipts → joins → gate
  → synthesis/review → evidence closure
  → findings → audit → parent closeout
  → later Whisper composition

At every gate: pass onward OR stop with explicit residue.
```

And one compact distinction table:

| Evidence says | It does not yet say |
|---|---|
| Route validated | Route executed |
| Spawn returned | Agent completed |
| Receipt exists | Receipt joined |
| Gate passed | Dependent wave executed |
| Findings audited | Claims became authority |
| Dispatch closed | Artifact was published or deployed |

Evidence: `explorer-causal-evidence.json#/result/evidence_model`; `plain-language-guide.md:29-111`.

### Run 1 as a genuine fail-closed case

Run 1 did not merely “fail to finish.” It preserved the boundary between what existed and what the lifecycle had admitted:

- Nine explorer returns existed, but the tenth native spawn hit the host thread limit.
- Explorers 1–8 were joined. Explorer 9’s exact return was preserved but remained explicitly `preserved_not_joined_due_partial_wave_spawn_failure`. Explorer 10 had no receipt.
- The run did not manufacture the missing result, upgrade explorer 9 to joined, or expose synthesis.
- Recovery uses a new dispatch, binds all nine preserved receipts by exact SHA-256, and executes only the missing novice explorer before resuming the research spine.
- This read-only action rechecked all nine files; every digest matches the recovery manifest.
- The recovery cannot rewrite run 1 into a successful ten-explorer wave. It creates a later evidence layer with its own lifecycle.

That makes the stop pedagogically useful: earlier valid work survives, missing transitions remain missing, and recovery advances through new explicit evidence. The capacity failure itself was an operational host/runtime blocker, not a product or semantic defect.

Evidence: `recovery-001/dispatch-sheet.json#/context`; `recovery-001/recovery-input-manifest.json#/preserved_explorers`; `/missing_explorer`; `/admission_rule`; `/failure_policy`; `explorer-failure-archaeology.json#/result/failure_atlas/2`.

### Transformed ending

At the beginning, orchestration looks like a pile of agents and answers. At the end, it becomes a question you can inspect:

> What is the last transition for which direct evidence exists, who owns the next decision, and what remains unproved?

The safest first exercise is to trace one action all the way from persisted ticket to host return, terminal observation, close, receipt, join, and gate. Stop wherever the evidence stops. That is the practical difference between “the agents seem finished” and “this bounded run has an honest, reviewable history.”

Whisper materially shaped this return through need-before-name ordering, one finite witness, explicit non-implications, a retell chain, and a transformed ending. No editorial experiment or human comprehension test was run, so this remains novice-retell research substrate rather than a proven final guide.

```json
{
  "schema_version": "domainspec.research-explorer-receipt.v0.1",
  "dispatch_id": "2026-08-13-agent-orchestration-beginner-guide-recovery-001",
  "action_id": "spawn-0001",
  "explorer_ordinal": 10,
  "target": "ops/development/2026-08-13-agent-orchestration-beginner-guide/recovery-001/dispatch-sheet.json#missing_novice_explorer-agent-0",
  "role": "explorer-novice-retell",
  "capability_ref": "research",
  "mode": "explore",
  "status": "pass",
  "mutation_policy": "read-only",
  "changed_paths": [],
  "artifacts": [
    "ops/development/2026-08-13-agent-orchestration-beginner-guide/receipts/explorer-novice-retell.json"
  ],
  "validation": "pass",
  "validation_details": "Read and parsed the exact recovery sheet, recovery manifest, nine preserved explorer receipts, generated Whisper contract, and supplied plain-language guide. Recomputed all nine preserved explorer SHA-256 values and confirmed exact agreement with the recovery manifest. Checked the return for reader before/after movement, need-before-name ordering, complete lifecycle retell chain, one finite worked example, analogy break points, ten misconception corrections, minimal visuals, transformed ending, run-1 temporal separation, source bindings, and claim ceiling. No file, runtime, test, host operation, registration, ledger, Inventory, telemetry, Git, publication, or external state was mutated.",
  "blockers": [],
  "claim_ceiling": "Bounded novice-retell research substrate derived only from the supplied recovery artifacts and pedagogical sources. It does not draft or validate the final guide, join this action, complete the recovery dispatch, prove current runtime conformance, establish semantic truth or authority, or authorize promotion, publication, deployment, or production.",
  "residue": [
    "The parent owns persistence of this return at the declared artifact path and its admission into the recovery run.",
    "Run 1 explorer 9 remains historically preserved-but-not-joined; this recovery return must not relabel that earlier state.",
    "No human comprehension test or Whisper transport experiment was performed.",
    "Runtime-only run, wave, step, and timestamp fields were not present in the bounded action brief and were not fabricated."
  ]
}
```
