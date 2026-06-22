# Invoke Example Runner: invoke-example-run

<!-- arcanum:capability-id invoke-example-runner -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command invoke-example-run -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-invoke-example-run-<UTC timestamp>`.
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

Select and run a requested Invoke template validation prompt through the Invoke Example Runner compatibility surface.

## Command Shape

```text
/invoke-example-run <selection>
```

## Process

1. Treat `<selection>` as a task ID, template and complexity pair, or `next`.
2. Resolve the requested example with `arcanum/spells/invoke/development/select-template-example-prompt.sh <selection>`.
3. Run `arcanum/spells/invoke/development/run-template-example-with-codex.sh <selection>` only when validating the explicit legacy Codex CLI path.
4. Otherwise, route through `arcanum-sigil-invoke-example-runner <selection>` and preserve the same selected prompt, output path, validation result, Dispatch trace status, Distill validation status, Task Session handoff readiness, and block or flag status.
5. Return selected prompt, output path, command used, validation result, Dispatch trace status, Distill validation status, Task Session handoff readiness, observability result, and next action.

## Guardrails

- Keep this adapter focused on Invoke template example validation.
- Do not treat legacy CLI execution as required for native Invoke authoring readiness.
- Do not mark bounded implementation complete when Invoke only emitted a Task Session handoff.
