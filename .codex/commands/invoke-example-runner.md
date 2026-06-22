# Arcanum Sigil: invoke example runner

<!-- arcanum:capability-id invoke-example-runner -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command invoke-example-runner -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-invoke-example-runner-<UTC timestamp>`.
- `capability.id`: `invoke-example-runner`
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

Run the installed Arcanum sigil `invoke-example-runner` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `invoke-example-runner`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/invoke-example-runner/README.md

````markdown
# Invoke Example Runner

Invoke Example Runner is an Arcana sigil for selecting Invoke template validation prompts and running them through the active Codex session.

It turns the template validation task matrix into an executable workflow: pick one low, medium, or complex example, load the generated prompt, run the native `invoke` skill package by default, and save the user-facing output for later validation.

Legacy command files remain compatibility adapters only. The runner may use `.codex/commands/arcanum-spell-invoke.md`, `invoke-example-next`, `invoke-example-run`, or `run-template-example-with-codex.sh` when the task is explicitly validating the legacy command surface.

## Use When

- a maintainer wants to run one invoke template example,
- a maintainer wants the next unrun example from the template matrix,
- an invoke template family needs low, medium, or complex output evidence,
- generated prompt files need to become saved example outputs.

## Do Not Use When

- the user only wants to inspect the template matrix,
- the prompt has already been run and no rerun is requested,
- the task is to validate saved outputs rather than produce them.

## Default Inputs

- task ID, for example `sigil-medium`,
- or template and complexity, for example `sigil medium`,
- or `next` to select the first prompt without a saved output.

## Default Outputs

- selected prompt path,
- selected output capture path,
- `Invoke Result` saved under `arcanum/spells/invoke/development/example-outputs/`,
- execution surface used: native `invoke`, legacy command, or legacy CLI,
- Dispatch Spec technique trace status,
- Distill validation status for `plan`, `full`, and `validate`,
- Task Session handoff readiness when the result routes to bounded execution,
- run summary with pass, flag, or block.

## Validation Expectations

The saved output must be a real user-facing `Invoke Result`, not a placeholder or save-summary response. Every result must preserve the Invoke Dispatch Spec technique trace requirement. `plan`, `full`, and `validate` results must include Distill validation status before any mutation-capable handoff. If the result routes to `task-session`, the runner records handoff readiness but does not mark implementation work complete.

## Why This Is Arcana

The sigil coordinates prompt selection, Codex command routing, output capture, and validation evidence across invoke templates. It is orchestration around another spell, not a deterministic transformation by itself.

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/invoke-example-runner/SKILL.md

````markdown
---
name: invoke-example-runner
description: "Use when selecting and running invoke template validation prompts in Codex, including picking a task by ID, template, complexity, or the next unrun prompt and saving the Invoke Result output."
argument-hint: "<task-id | template complexity | next>"
tier: arcana
domain: invoke-validation
version: 0.1.0
origin: created to make invoke template examples executable from generated prompt files
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Sigil: Invoke Example Runner

<objective>
Select one Invoke template validation prompt, run it through the active native `invoke` skill package or an explicit legacy compatibility adapter, validate the returned `Invoke Result`, and save the user-facing output as validation evidence.
</objective>

<execution-surface>
Default to the active native `invoke` skill package. Use `.codex/commands/arcanum-spell-invoke.md`, `invoke-example-next`, `invoke-example-run`, or `arcanum/spells/invoke/development/run-template-example-with-codex.sh` only when explicit legacy command compatibility is being validated.

The short legacy commands are discovery bridges into this sigil:

- `invoke-example-next` resolves `next`,
- `invoke-example-run <selection>` resolves an exact task ID, template/complexity pair, or `next`.
</execution-surface>

<process>
1. Resolve the requested example:
   - exact task ID such as `sigil-medium`,
   - template plus complexity such as `sigil medium`,
   - or `next` for the first prompt whose output file does not exist.
2. Use `arcanum/spells/invoke/development/select-template-example-prompt.sh` to locate the prompt and capture path.
3. If the selected output already exists and the user did not request a rerun, return `FLAG` with the existing output path instead of overwriting it.
4. Use the active native `invoke` skill package as the default execution surface. Use `arcanum/spells/invoke/development/run-template-example-with-codex.sh` only when the user wants automated legacy CLI execution.
5. Otherwise read the selected prompt and execute its **Codex Prompt** instructions in the current Codex session.
6. Save the resulting user-facing `Invoke Result` to the prompt's `Expected Capture Path`.
7. Validate the saved result:
   - the output must contain a real `Invoke Result`, not a save-summary response or placeholder,
   - the selected mode must route through canonical `invoke` contracts,
   - every mode result must preserve the Dispatch Spec technique trace or report a block/flag,
   - `plan`, `full`, and `validate` results must include Distill validation status before any mutation-capable handoff,
   - a `task-session` next route must remain a handoff, not completed execution,
   - any subagent strategy must include explicit subagent/local fallback boundaries and expected receipt shape.
8. Return selected prompt, output path, execution surface, validation state, Dispatch trace status, Distill validation status, Task Session handoff readiness, and next unrun prompt if any.
</process>

<quality-bar>
A successful run must:

- select exactly one prompt,
- preserve the prompt's task ID, template target, complexity, and user request,
- route through canonical `invoke` contracts and the active native skill surface by default,
- save a user-facing output file,
- verify Dispatch Spec technique trace evidence,
- verify Distill validation evidence for `plan`, `full`, and `validate`,
- preserve `task-session` as the next owner for bounded execution,
- avoid marking deferred modes as implemented,
- report any block or flag result honestly,
- leave canonical invoke contracts unchanged while running examples.
</quality-bar>

<anti-patterns>
Avoid:

- claiming a prompt was run when only selected,
- overwriting an existing output unless the user requested a rerun,
- bypassing the active native `invoke` skill package,
- treating legacy command compatibility as native authoring readiness,
- editing canonical invoke contracts while running examples,
- accepting an output that lacks Dispatch trace or required Distill validation evidence,
- marking task execution complete when Invoke only emitted a Task Session handoff,
- replacing missing outputs with generic placeholder text.
</anti-patterns>

<output-contract>
Return:

```markdown
## Invoke Example Runner Result

- Selection: <task-id>
- Prompt: <path>
- Output: <path>
- Execution surface: native invoke | legacy command | legacy CLI
- Invoke mode: define | design | plan | handoff | refresh | full | validate
- Invoke status: pass | flag | block
- Dispatch trace: pass | flag | block
- Distill validation: pass | flag | block | skipped | not_applicable
- Task-session handoff: ready | blocked | not_applicable
- Saved output: yes | no
- Next unrun: <task-id | none>
- Follow-up: <items | none>
```
</output-contract>

````
