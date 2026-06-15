# Arcanum Sigil: definitions governance

<!-- arcanum:capability-id definitions-governance -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command arcanum-sigil-definitions-governance -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-sigil-definitions-governance-<UTC timestamp>`.
- `capability.id`: `definitions-governance`
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

Run the installed Arcanum sigil `definitions-governance` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `definitions-governance`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/definitions-governance/README.md

````markdown
# Definitions Governance

Definitions Governance is an Arcana sigil for keeping critical terminology authoritative, interpretable, indexed, and traceable across a repository.

It maintains one canonical definition source, keeps lookup artifacts synchronized, separates normative wording from explanatory intuition, and audits downstream drift where terms are reused.

Definitions Governance is the maintainer process, not the place where a
project's definitions live. When the sigil is installed or copied into another
repository, it must resolve that repository's project-level definition authority
before reading or writing terms.

## Problem It Solves

Projects drift when critical terms are redefined in papers, plans, specs, implementation notes, or presentations. A term may look familiar while its meaning silently changes across artifacts.

Definitions Governance prevents that by treating definitions as a governed authority layer with traceable downstream consumers.

## Use When

- a gate-critical or high-impact term is added or revised,
- formulas, notation, or formal constructs need stable interpretation,
- downstream documents reference canonical terms,
- narrative summaries risk redefining normative semantics,
- definition drift needs to be audited.

## Do Not Use When

- the term is local to one feature glossary,
- the wording is informal and non-critical,
- the task is only to rename a label,
- the repository is not ready to own definition governance.

If there is no canonical definitions source but the repository is ready to own
one, use this sigil to initialize a project-level source instead of writing into
the sigil folder.

## Authority Model

The consuming repository should identify:

- canonical definitions source,
- lookup or index layer,
- narrative consumers,
- protocol or process consumers,
- validation checks,
- drift remediation targets.

Default project-level convention when the repository has no existing authority
source:

```text
definitions/
  DEFINITIONS.md
  DEFINITIONS-INDEX.md
  DEFINITION-DRIFT-AUDIT.md
```

Do not store project definitions in:

- the installed sigil package,
- a copied `.codex/skills` package,
- a `.agents/skills` discovery link,
- `arcana/definitions-governance/`,
- any runtime or generated install surface.

Those locations may contain the Definitions Governance process. They are not the
consuming project's terminology authority unless the repository explicitly says
so.

In this Arcanum repository, the project-level authority source is
[definitions/DEFINITIONS.md](../../definitions/DEFINITIONS.md), with lookup in
[definitions/DEFINITIONS-INDEX.md](../../definitions/DEFINITIONS-INDEX.md).

## Why This Is Arcana

Definitions Governance coordinates authority, interpretation, indexing, drift detection, and remediation routing across many artifacts. It governs semantic consistency over time.

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/definitions-governance/SKILL.md

````markdown
---
name: definitions-governance
description: "Use when: maintaining canonical definitions, synchronized indexes, explanatory intuition, and downstream drift checks for critical terms."
argument-hint: "[--add <id>] [--update <id>] [--sync] [--audit] [--config <path>]"
tier: arcana
domain: semantic-governance
version: 0.1.0
origin: generalized from recurring canonical definitions maintenance practice
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Sigil: Definitions Governance

<objective>
Keep critical definitions authoritative, interpretable, discoverable, and traceable across downstream artifacts.
</objective>

<logic-type>
Arcana: semantic authority governance with drift detection and remediation routing.
</logic-type>

<project-authority-boundary>
Definitions Governance is the maintainer process, not the canonical definition
store.

When used in any repository, resolve the consuming project's root and write to
that project's configured definitions surface. Do not place project definitions
inside the installed sigil package, copied skill directory, `.codex/skills`
snapshot, `.agents/skills` symlink target, or `arcana/definitions-governance/`
unless the repository has explicitly configured that path as its project-level
definition authority.

Default project-level convention when no authority source exists:

```text
definitions/
  DEFINITIONS.md
  DEFINITIONS-INDEX.md
  DEFINITION-DRIFT-AUDIT.md
```

For this Arcanum repository, the canonical project-level source is
`definitions/DEFINITIONS.md` and the lookup layer is
`definitions/DEFINITIONS-INDEX.md`.
</project-authority-boundary>

<process>
1. Resolve the consuming project's authority model from the project root, not
   from the installed sigil package:
   - canonical definitions source,
   - lookup or index layer,
   - narrative consumers,
   - operational consumers,
   - validation checks.
2. If no canonical definitions source exists, initialize the default
   project-level `definitions/` surface unless the user or repository metadata
   names a different location.
3. Read the canonical definitions source and index before making changes.
4. Add or update critical terms with stable IDs when the repository uses IDs.
5. For formal or mathematical constructs, keep the minimum interpretation package together:
   - formal expression,
   - variable or notation meaning,
   - operational interpretation,
   - plain-language intuition.
6. Keep explanatory intuition colocated with the definition and clearly non-normative.
7. Sync lookup or index artifacts so definitions are discoverable.
8. Audit downstream drift:
   - conflicting wording,
   - stale anchors,
   - undefined critical terms,
   - narrative text that redefines authority,
   - missing references.
9. Emit remediation items with target files and recommended action.
10. Run available structure, link, or schema validation checks.
</process>

<authority-rule>
Only the consuming project's configured canonical definitions source may define
normative semantics. Narrative, summary, protocol, planning, presentation,
runtime, install-surface, or copied skill artifacts may explain or reference
definitions, but should not redefine them.
</authority-rule>

<quality-bar>
A successful execution must:

- resolve and report the consuming project's canonical definitions path,
- avoid writing project definitions into the sigil package or installed skill copy,
- keep critical terms in the canonical source,
- preserve stable IDs when used,
- colocate plain-language intuition with formal definitions,
- prevent intuition from contradicting normative wording,
- keep indexes synchronized,
- identify downstream drift with exact remediation targets,
- validate structure where checks exist.
</quality-bar>

<anti-patterns>
Avoid:

- using the sigil's own folder as the default project definition authority,
- treating copied skill packages as canonical definition stores,
- letting narrative artifacts become hidden definition authorities,
- adding formulas without symbol meaning and plain-language intent,
- creating detached intuition that can drift away from the definition,
- changing stable IDs casually,
- syncing indexes without auditing downstream consumers,
- treating local glossary terms as global canonical definitions without review.
</anti-patterns>

<output-contract>
Return:

```markdown
## Definitions Governance Summary

- Definitions updated: <ids or none>
- Index synced: yes | no | not applicable
- Drift found: yes | no
- Undefined critical terms: <count>
- Conflicting consumers: <count>
- Validation: pass | fail | not run
- Canonical source: <project-relative path>
- Follow-ups: <ordered remediation list>
```
</output-contract>

````
