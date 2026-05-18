# invoke-example-next

Run the next unrun invoke template validation example.

## Process

1. Run:

```bash
arcanum/spells/invoke/development/run-template-example-with-codex.sh next
```

2. Return the selected task ID, output path, log path, and pass/fail status.
3. If the runner fails, show the log path and the first actionable error.

## Notes

- Existing outputs are skipped.
- Use `RERUN=1 arcanum/spells/invoke/development/run-template-example-with-codex.sh <task-id>` to overwrite a specific output.
- Use `arcanum/spells/invoke/development/run-template-example-with-codex.sh --all` only for explicit batch runs.
