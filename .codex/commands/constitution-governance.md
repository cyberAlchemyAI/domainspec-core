# Arcanum Sigil: constitution governance

<!-- arcanum:capability-id constitution-governance -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command constitution-governance -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-constitution-governance-<UTC timestamp>`.
- `capability.id`: `constitution-governance`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `constitution-governance` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `constitution-governance`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/constitution-governance/README.md

````markdown
# Constitution Governance

Constitution Governance is an Arcana sigil for creating, selecting, composing, and validating modular constitutions.

It exists because constitutions are pattern enforcers for structure and form. They lose force when every rule is poured into one large file and loaded wholesale into every task. A constitution should be small enough to apply pressure, explicit enough to validate, and composable enough to travel with the work that needs it.

## Problem It Solves

A repository can accumulate many governance rules:

- artifact rules,
- chart rendering rules,
- validation rules,
- ontology branch rules,
- implementation planning rules,
- runtime evidence rules,
- presentation or document form rules.

If those rules live in one large constitution, agents either load too much context or ignore the parts that matter. If rules live only in memory, they do not reliably affect artifacts. Constitution Governance keeps constitutions modular, selects the relevant ones for a task, composes them into a small enforcement pack, and routes enforceable rules into validators or review checks.

## Core Stance

Context Builder is necessary but not sufficient.

Context Builder should select the constitutions relevant to a task. Constitution Governance should decide how selected constitutions compose, which rules are enforceable, which validators must run, and which conflicts require a decision gate.

```text
task intent
  -> select relevant constitutions
  -> compose minimal constitution pack
  -> identify enforceable rules
  -> update or require validation adapters
  -> execute task with focused governance context
  -> report pass, flag, block, or proposed constitution change
```

## Use When

- a new constitution or governance rule is needed,
- an existing constitution is growing too large,
- a task needs only selected constitution rules in context,
- multiple constitutions may conflict or overlap,
- a constitution rule should be enforced by a validator,
- a validation script should be updated after a constitution change,
- a governance rule should become canonical inside Arcanum.

## Do Not Use When

- a one-line local note is enough,
- the rule has no expected reuse or enforcement path,
- the task only needs ordinary Context Builder evidence selection,
- a validator change is purely mechanical and the constitution already exists,
- a decision gate is required and no acceptable default exists.

## Core Concepts

- Constitution: a durable governance artifact that enforces structure, form, or artifact behavior.
- Rule: one enforceable or reviewable requirement inside a constitution.
- Selector: a task-to-constitution matching condition.
- Composition pack: the minimal selected set of constitutions and rules for a task.
- Validation adapter: a script, lint rule, review checklist, or test that enforces one or more rules.
- Authority boundary: the owner, scope, and promotion state that say where the rule applies.
- Context load budget: the maximum governance context that should be loaded before rule force decays.

## Outputs

The sigil can produce:

- constitution proposal,
- constitution split plan,
- constitution composition pack,
- constitution selection map,
- validation adapter plan,
- validator update checklist,
- conflict report,
- decision gate packet,
- promotion readiness report.

## Integration

Use [context-builder](../../transmutations/context-builder/) to select task-relevant constitution excerpts and evidence.

Use [decision-gate](../decision-gate/) when constitution scope, precedence, conflict resolution, or canonical promotion needs human choice.

Use [inventory](../inventory/) to store source-backed constitution candidates or reusable evidence about recurring rule failures.

Use [sigil-development](../sigil-development/) when Constitution Governance itself is revised or promoted.

Use validators under [tools/](../../tools/) to enforce rules that can be checked deterministically.

## Why This Is Arcana

Constitution Governance coordinates long-lived rule authority across context selection, artifact form, validation, conflict handling, and promotion. It is not just a formatter or linter; it governs how rules are created, selected, composed, enforced, and retired.

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/constitution-governance/SKILL.md

````markdown
---
name: constitution-governance
description: "Use when: creating, splitting, selecting, composing, validating, or promoting modular constitutions that enforce artifact structure/form without overloading task context."
argument-hint: "<create|add-rule|select|compose|validate|split|promote> <target-or-task> [--constitution <path>] [--output <path>] [--dry-run]"
tier: arcana
domain: constitution-governance
version: 0.1.0
origin: created from the artifact constitution/context-load concern and generalized into an Arcanum canonical sigil
allowed-tools: Read, Write, Glob, Grep, Bash, AskQuestions, Task
---

# Sigil: Constitution Governance

<objective>
Create, maintain, select, compose, and validate modular constitutions so structure/form rules remain enforceable without bloating task context.
</objective>

<logic-type>
Arcana: long-lived governance of modular rule artifacts, context selection, composition precedence, validator integration, and promotion decisions.
</logic-type>

<modes>
- `create`: draft a new constitution with scope, authority, selectors, rules, validation surface, and promotion boundary.
- `add-rule`: add or propose a new rule to an existing constitution, including validator impact.
- `select`: choose constitution excerpts relevant to a task or artifact before execution.
- `compose`: produce a minimal constitution pack from selected constitutions, resolving precedence and conflicts.
- `validate`: check whether an artifact, task, or validator satisfies selected constitution rules.
- `split`: propose a decomposition when one constitution has become too broad or low-effect.
- `promote`: prepare a constitution or rule for canonical adoption after evidence and validation pass.
</modes>

<applicability>
Use this sigil when:

- a governance rule should apply across future artifacts,
- a constitution is becoming a catch-all file,
- a task needs only the constitutions that match its artifact type or structure,
- selected constitutions need composition before a task runs,
- a new constitution rule requires a validation adapter,
- a validator should be updated in response to a constitution rule,
- constitution context load is weakening rule effect.
</applicability>

<non-applicability>
Do not use this sigil when:

- a local task note is enough,
- there is no reuse or validation expectation,
- a deterministic validator already covers the rule and no governance decision remains,
- Context Builder selection alone is enough and no composition, conflict, or validator impact exists.
</non-applicability>

<inputs>
Expected inputs, if available:

- target task, artifact type, constitution path, or rule proposal,
- existing constitution files,
- validator scripts or checks,
- known artifact failures,
- desired canonicality level,
- context budget or task scope,
- evidence from prior runs or reviews.
</inputs>

<default-output>
Prefer target-local outputs:

1. `arcana/constitution-governance/development/` for sigil development artifacts,
2. `<target>/development/constitution-pack.md` for task-specific composition packs,
3. `framework/<NAME>-CONSTITUTION.md` for framework-level constitutions,
4. `tools/` updates only when the user approves or the rule is already accepted.
</default-output>

<process>
1. Resolve the target rule, constitution, task, or artifact type.
2. Classify the request:
   - new constitution,
   - rule addition,
   - selection before execution,
   - composition pack,
   - validation adapter,
   - split/debloat,
   - promotion.
3. Gather only relevant constitution sources and validation surfaces.
4. Decide whether Context Builder selection is enough:
   - enough when the task only needs focused context,
   - not enough when selected rules interact, conflict, need precedence, or require validators.
5. For constitution creation or rule addition, define:
   - scope,
   - owner,
   - authority level,
   - selection predicates,
   - rules,
   - examples and non-examples,
   - validation adapters,
   - promotion boundary,
   - retirement or split triggers.
6. For selection, return only matching constitution rules with source paths, rationale, and excluded rules.
7. For composition, produce a compact constitution pack with:
   - selected rules,
   - precedence,
   - conflicts,
   - validators to run,
   - context budget,
   - pass/flag/block semantics.
8. For validator integration, map each rule to:
   - deterministic check,
   - review-only check,
   - future check,
   - blocked check.
9. Route unresolved precedence, canonicality, or mutation scope decisions through Decision Gate.
10. Validate the result against the target artifact or constitution package.
11. Return paths changed, rules selected, validators required, blockers, and next route.
</process>

<composition-rules>
Constitutions should compose by narrowest applicable scope first:

1. task-specific constitution pack,
2. artifact-type constitution,
3. domain or capability constitution,
4. framework constitution,
5. repository-wide default.

When two rules conflict:

- preserve both rules,
- classify the conflict as blocker, deferrable, or local override,
- use Decision Gate for blocker conflicts,
- do not silently let the larger constitution override the narrower one.

Context packs should include only the rules needed for the task, plus enough source links to audit them.
</composition-rules>

<validation-model>
Each rule must declare one validation mode:

- `deterministic`: script, lint, test, schema, or static check can enforce it,
- `review`: human or model review required,
- `hybrid`: deterministic precheck plus review,
- `none-yet`: constitution records intent, but promotion is blocked until a validation route exists.

Validator changes must cite the constitution rule they enforce.
</validation-model>

<quality-bar>
A successful execution must:

- keep constitutions modular and scoped,
- avoid loading a large constitution when selected rules suffice,
- separate Context Builder selection from constitution composition,
- define rule authority, selectors, examples, and validation mode,
- identify validator updates needed by new rules,
- preserve conflicts instead of smoothing them over,
- route blocker precedence or canonicality decisions through Decision Gate,
- keep generated task packs separate from canonical constitutions,
- return a pass, flag, or block result with paths and validators.
</quality-bar>

<anti-patterns>
Avoid:

- adding every new rule to one giant constitution,
- treating context selection as enforcement,
- treating validators as authority without a constitution rule,
- promoting rules without examples and non-examples,
- loading all constitutions into every task,
- hiding conflicts by choosing the newest rule,
- adding a validator check that is broader than its constitution scope,
- making a constitution canonical because it is convenient rather than evidenced.
</anti-patterns>

<observability>
For meaningful executions, emit or prepare telemetry with:

- mode,
- constitutions inspected,
- rules selected,
- rules added,
- composition pack path,
- validator changes proposed or applied,
- conflicts found,
- decision gates required,
- pass/flag/block result,
- context budget status.
</observability>

<output-contract>
Return:

```markdown
## Constitution Governance Result

- Mode: <create | add-rule | select | compose | validate | split | promote>
- Target: <target>
- Status: pass | flag | block
- Constitutions inspected: <paths>
- Rules selected or changed: <summary>
- Composition pack: <path or none>
- Validator impact: <required | applied | none | blocked>
- Conflicts: <none or list>
- Decisions needed: <none or list>
- Validation: <checks and result>
- Next route: context-builder | decision-gate | task-session | sigil-development | deferred
```
</output-contract>

````
