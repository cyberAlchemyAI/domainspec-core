# Invoke Example Runner: invoke-example-next

<!-- arcanum:capability-id invoke-example-runner -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command invoke-example-next -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-invoke-example-next-<UTC timestamp>`.
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

Select and run the next unrun Invoke template validation prompt through the Invoke Example Runner compatibility surface.

## Command Shape

```text
/invoke-example-next
```

## Process

1. Resolve the next example with `arcanum/spells/invoke/development/select-template-example-prompt.sh next`.
2. Run `arcanum/spells/invoke/development/run-template-example-with-codex.sh next` only when validating the explicit legacy Codex CLI path.
3. Otherwise, route through `arcanum-sigil-invoke-example-runner next` and preserve the same selected prompt, output path, validation result, Dispatch trace status, Distill validation status, Task Session handoff readiness, and block or flag status.
4. Return selected prompt, output path, command used, validation result, Dispatch trace status, Distill validation status, Task Session handoff readiness, observability result, and next action.

## Guardrails

- Keep this adapter focused on Invoke template example validation.
- Do not treat legacy CLI execution as required for native Invoke authoring readiness.
- Do not mark bounded implementation complete when Invoke only emitted a Task Session handoff.
