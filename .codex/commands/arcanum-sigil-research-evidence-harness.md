# Arcanum Sigil: research evidence harness

<!-- arcanum:capability-id research-evidence-harness -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command arcanum-sigil-research-evidence-harness -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-sigil-research-evidence-harness-<UTC timestamp>`.
- `capability.id`: `research-evidence-harness`
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

Run the installed Arcanum sigil `research-evidence-harness` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `research-evidence-harness`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/research-evidence-harness/README.md

````markdown
# Research Evidence Harness

Research Evidence Harness is a draft Arcana sigil for turning a planned research
experiment into validated, append-only evidence artifacts. It is the proposed
owner for MARS-derived experiment mechanics that do not belong inside
`research-tower`: run schemas, fixture validation, objective/metric checks,
result summaries, and claim-adjudication readiness.

Status: draft candidate, not promoted.

## Problem Solved

Research Tower makes source understanding durable. It does not execute or
validate empirical research evidence.

MOGT needs a reusable evidence harness because its publication path requires:

- experiment bundle discipline;
- append-only JSONL run data;
- schema validation;
- objective-vector and policy-regime checks;
- Pareto/frontier and overhead metric support;
- reviewer-rubric ingestion;
- result summaries that do not overclaim evidence status;
- dry-run fixture proof before live experiment execution.

## When To Use

Use this sigil when:

- a research project already has claims, protocols, and experiment bundles;
- the next blocker is data shape, fixture validation, scoring, or result
  summarization;
- dry-run evidence must be separated from live evidence;
- a paper, research graph, or claim ledger depends on measured outputs;
- MARS-style research gates need to become project-local executable checks.

## When Not To Use

Do not use this sigil for:

- learning or summarizing a paper;
- broad source discovery or related-work mapping;
- canonical term promotion;
- narrative paper rewriting;
- live experiment execution before dry-run schema and fixture validation pass;
- replacing `experiment-harness` for spell/sigil lifecycle experiments.

## Standard Artifact Set

A standard research evidence harness may produce or update:

- `experiments/schema/*.schema.json`;
- `tools/validate-*-run-jsonl.*`;
- `tools/*metric*.*`;
- `development/fixtures/*.jsonl`;
- `development/fixture-validation-report.md`;
- `experiments/*/data/*.jsonl`;
- `experiments/*/results/*.md`;
- `results/*-EVIDENCE-STATUS.md` readiness notes;
- telemetry or observability signal references.

## Relationship To Existing Capabilities

- `research-tower` owns source-backed learning towers and promotion guardrails.
- `context-builder` owns compact source/evidence packs.
- `inventory` owns source library and provenance coverage.
- `experiment-harness` owns reusable spell/sigil validation mechanics.
- `research-evidence-harness` owns project research data mechanics.
- `task-session` owns bounded execution of approved SWUs.

## Lifecycle

This draft candidate is seeded from MOGT and MARS evidence:

- MOGT harness feasibility blocked on missing research-project mechanics.
- MARS provides reusable bundle, pipeline, context, schema, and telemetry
  patterns.
- MOGT should prove the pattern locally before Arcanum absorbs it as canonical.

## Promotion Rule

This sigil may create validation and result artifacts. It must not mark claims
supported, partially supported, contradicted, or paper-ready unless the relevant
project-specific evidence gate allows that update.

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/research-evidence-harness/SKILL.md

````markdown
---
name: research-evidence-harness
description: "Use when: converting research protocols into validated run schemas, JSONL fixture checks, objective/metric calculations, result summaries, and claim-adjudication readiness without running or overclaiming live experiments."
argument-hint: "<research-project> [--swu <id>] [--dry-run] [--validate] [--summarize]"
tier: arcana
domain: research-governance
version: 0.1.0
origin: proposed from MOGT harness feasibility and MARS import/absorption refinement
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Sigil: Research Evidence Harness

<objective>
Turn planned research experiments into validated evidence-capture artifacts:
schemas, append-only JSONL checks, dry-run fixtures, metric calculations,
result summaries, and claim-adjudication readiness.
</objective>

<logic-type>
Arcana: empirical research evidence governance with schema discipline, dry-run
proof, metric validation, and publication-safe claim boundaries.
</logic-type>

<applicability>
Use this sigil when:

- a research project has claims, protocols, experiment bundles, or a paper
  contract, but lacks executable evidence mechanics;
- dry-run fixtures must prove data shape before live runs;
- JSONL run data needs schema and metadata validation;
- objective vectors, scoring policies, reviewer rubrics, or analysis summaries
  must be checked before evidence status changes;
- MARS-style research pipeline assets are being adapted locally.
</applicability>

<non-applicability>
Do not use this sigil when:

- the task is source understanding, notation translation, local glossary, or
  bridge decisions; use `research-tower`;
- the task is generic spell/sigil prompt validation; use `experiment-harness`;
- the task is broad planning with no approved work unit; use `refine` and
  `invoke`;
- the user wants live experiment execution before dry-run validation has passed.
</non-applicability>

<inputs>
Expected inputs:

- research project root;
- selected experiment or SWU;
- protocols and methodology profiles;
- required common run fields;
- metric and success-criteria definitions;
- source/context requirements;
- write scope;
- validation command or review surface;
- evidence-status guardrails.
</inputs>

<process>
1. Verify the project already has a bounded research objective, claims, and
   experiment bundle roots.
2. Read the selected task or SWU and its write scope.
3. Identify required run fields from the protocol, feasibility report, or
   work-pack.
4. Create or update a project-local run schema.
5. Create or update a validator for append-only JSONL rows.
6. Add synthetic passing and failing fixtures before any live run.
7. Validate fixtures and record command output.
8. Add objective-vector, policy-regime, reviewer-rubric, or metric calculators
   only when the selected SWU owns them.
9. Generate result summaries only from validated fixture or run data.
10. Preserve dry-run/live evidence separation.
11. Block evidence-status upgrades unless live experiment analysis supports the
    claim update and the project gate allows it.
12. Return the validation result, files produced, remaining blockers, and next
    governed route.
</process>

<quality-bar>
A successful execution must:

- preserve the selected write scope;
- create project-local evidence mechanics rather than mutating canonical
  Arcanum contracts;
- validate at least one passing and one failing fixture for schema work;
- reject missing run metadata, objective vectors, policy regimes, and malformed
  metric fields when applicable;
- distinguish dry-run fixture evidence from live experiment evidence;
- keep claim/evidence status unchanged unless a later approved analysis task
  supports an update;
- record validation commands or reviewable evidence;
- leave the next SWU or blocker explicit.
</quality-bar>

<anti-patterns>
Avoid:

- treating a planned protocol as empirical support;
- upgrading paper claims from synthetic fixture data;
- copying MARS project-specific fields into unrelated projects unchanged;
- hiding protocol deviations;
- mixing source discovery, learning tower, and run-data validation in one
  artifact;
- mutating `experiment-harness`, `research-tower`, or paper contracts without a
  separate governed route.
</anti-patterns>

<output-contract>
Return:

```markdown
## Research Evidence Harness Result

- Target: <research project>
- Selected unit: <experiment | task | SWU>
- Mode: dry-run | validate | summarize | mixed
- Status: pass | flag | block
- Schema: <path or none>
- Validator: <path or none>
- Fixtures: <paths or none>
- Metrics: <paths or none>
- Result summary: <path or none>
- Evidence-status boundary: preserved | updated-by-approved-live-analysis | block
- Validation: <commands or review evidence>
- Remaining blockers: <items or none>
- Next route: task-session | codex-goal-profile | publication-research-pipeline | deferred
```
</output-contract>

````
