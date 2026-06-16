# Skill Routing - Ontologize View-Triad Method

Inventory of sibling skills under `implementation/domainspec/.claude/skills/` that can support this method. The recommended set is intentionally smaller than the full folder.

## Primary Method Skills

| Skill | Use Here | Gate |
| --- | --- | --- |
| `system-view` | Author the shape/stakes view and name load-bearing stances without deciding them. | Required for any view-triad run. |
| `engineer-view` | Author the decision inventory, schemas/contracts, and runtime mechanics. | Required after system-view or source stance list exists. |
| `ontology-view` | Author typed nodes, edges, forbidden-edge guards, schema graph, and ontology cross-reference map. | Required after decision inventory exists or explicit provisional handles are accepted. |

## DomainSpec Lifecycle Support

| Skill | Use Here | Notes |
| --- | --- | --- |
| `domainspec-context-builder` | Build source inventory and strict selector context for each SWU. | Use before writing view artifacts. |
| `domainspec-interview-kits` | Resolve one-question-at-a-time method boundary decisions. | Use when source, audience, or output path is unclear. |
| `domainspec-decision-gate` | Resolve blocker decisions such as output path, dispatch mode, or product-doc mutation. | Use only for consequential blockers. |
| `domainspec-task-session` | Execute one SWU from this work-pack. | Next route after this pack. |
| `domainspec-feature-glossary` | Refresh local glossary for target-specific terms. | Use when the target corpus has unstable terms. |
| `domainspec-definitions-governance` | Maintain canonical definitions and drift checks. | Use if local terms are proposed for promotion. |
| `domainspec-sync-registry` | Sync registry/glossary from feature SPEC concept tables. | Use only if a downstream feature SPEC is introduced. |
| `domainspec-audit-alignment` | Audit produced view artifacts against source contracts. | Useful before product-doc integration. |
| `domainspec-readiness-gate` | Decide pilot/release/production readiness. | Use after pilot triad validation. |
| `domainspec-emit-signals` | Emit structured pipeline signals after a DomainSpec session. | Use after actual view authoring, not just planning. |
| `domainspec-signal-observer` | Derive behavior-level governance signals from telemetry. | Use after multiple view-triad runs. |
| `domainspec-reflect` | Generate tuning reports from accumulated signals. | Use after repeated method runs show patterns. |

## Dispatch And Review Support

| Skill | Use Here | Notes |
| --- | --- | --- |
| `domainspec-subagents-strategy` | Compose optional explorer/skeptic/writer/auditor waves. | Opt-in for contested or high-risk view runs. |
| `research` | Investigate new claims or unresolved evidence questions. | Do not use as the generic dispatcher for view skills. |
| `review` | Red-team existing view artifacts for change requests. | Use after drafts exist. |
| `robot-talks` | Identify cross-layer tensions. | Good for method-design disputes before finalizing view laws. |

## DomainSpec Build And Verification Skills

| Skill | Use Here | Notes |
| --- | --- | --- |
| `domainspec-spec-feature` | Convert the method into a feature SPEC if it becomes productized. | Deferred until method stabilizes. |
| `domainspec-generate-tests` | Generate deterministic test specs for validators. | Use if validators are added. |
| `domainspec-verify-feature` | Verify readiness from specs, tests, implementation, and alignment. | Use after implementation changes exist. |
| `domainspec-implementation-axioms` | Read before any code implementation. | Required if validators or tooling are built. |
| `domainspec-implement` | Implement feature code from DomainSpec docs. | Only after a task-session selects a code SWU. |
| `domainspec-tag-code` | Apply DomainSpec source tags to implementation code. | Only if code is added. |
| `domainspec-brownfield-translation` | Translate an already implemented project into DomainSpec artifacts. | Useful for client repos. |
| `domainspec-start` | Initialize DomainSpec inside an existing repo. | Useful for client onboarding. |
| `domainspec-new-repo` | Start a new DomainSpec consumer repo. | Not needed for this pack. |
| `domainspec-orchestrate` | User-facing router for DomainSpec requests. | Useful once method is stable. |
| `domainspec-pipeline` | End-to-end feature pipeline. | Too broad for initial method authoring. |
| `domainspec-pilot-readiness` | Prepare a feature for pilot testing. | Use after Ontologize pilot triad exists. |

## UI, Infra, And OTel Skills

| Skill | Use Here | Notes |
| --- | --- | --- |
| `domainspec-ui-architecture` | Define frontend architecture if the method gets a UI. | Deferred. |
| `domainspec-ui-phase-bridge` | Bridge feature specs to UI phase workflow. | Deferred. |
| `domainspec-ui-implement` | Implement frontend from UI architecture and UI spec. | Deferred. |
| `domainspec-ui-audit-bridge` | Visual review of implemented frontend code. | Deferred. |
| `domainspec-ui-pipeline` | Full UI lifecycle. | Deferred. |
| `domainspec-infra-architecture` | Define infra architecture. | Deferred unless method becomes a hosted tool. |
| `domainspec-infra-deploy` | Generate deployment artifacts. | Deferred. |
| `domainspec-instrument-otel` | Instrument backend code with OTel. | Deferred until runtime exists. |
| `domainspec-otel-verify` | Verify OTel coverage. | Deferred until instrumentation exists. |

## GSD Execution Layer

Use GSD skills only when the work moves into the GSD planning/execution system. For this pack, `domainspec-task-session` is the preferred executor.

| Skill Family | Use Here |
| --- | --- |
| `gsd-discuss-phase`, `gsd-plan-phase`, `gsd-execute-phase`, `gsd-validate-phase` | Alternative phase workflow if the work is imported into GSD. |
| `gsd-add-backlog`, `gsd-add-phase`, `gsd-insert-phase`, `gsd-review-backlog` | Backlog and roadmap maintenance. |
| `gsd-workstreams`, `gsd-new-workspace`, `gsd-list-workspaces`, `gsd-resume-work` | Workspace management for parallel work. |
| `gsd-review`, `gsd-audit-uat`, `gsd-audit-milestone`, `gsd-verify-work` | Review and verification after GSD implementation. |
| `gsd-fast`, `gsd-quick`, `gsd-do`, `gsd-autonomous` | Lightweight or autonomous task execution; use carefully because this method has governance gates. |
| `gsd-ship`, `gsd-pr-branch`, `commit-message`, `test-uncommitted-changes` | Commit/PR/test support after implementation. |

## Utility And Local Skills

| Skill | Use Here |
| --- | --- |
| `scratchpad` | Multi-turn note capture. |
| `close-session` | Session closure and conversation node. |
| `research` | New evidence investigation. |
| `review` | Existing artifact red-team. |
| `implement-filter` | Not relevant; domain-specific remessa filter work. |
| `gitnexus-*` | Use for code graph exploration, impact analysis, debugging, and refactoring if code implementation starts. |

## Recommended Minimal Route

```text
domainspec-context-builder
-> system-view
-> engineer-view
-> ontology-view
-> domainspec-audit-alignment
-> domainspec-task-session synchronization
```

Use `domainspec-subagents-strategy` only when the target has contested stances, uncertain authority, or high stakeholder risk.

