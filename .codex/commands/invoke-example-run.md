# invoke-example-run

Run one invoke template validation example by task ID or by template plus complexity.

## Usage

```text
invoke-example-run sigil-medium
invoke-example-run sigil medium
invoke-example-run architecture complex
```

## Process

1. Convert the user's arguments into either `<task-id>` or `<template> <complexity>`.
2. Run:

```bash
arcanum/spells/invoke/development/run-template-example-with-codex.sh <selection>
```

3. Return the selected task ID, output path, log path, and pass/fail status.
4. If the runner fails, show the log path and the first actionable error.

## Notes

- Existing outputs are skipped.
- Use `RERUN=1` with the script for intentional overwrites.
