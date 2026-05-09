# Terminal Guard

`tools/terminal_guard.sh` helps prevent terminal-driven agent stalls by:

- nudging risky command shapes before execution,
- wrapping command execution with timeout + output monitoring,
- profiling the most-used command heads in repository scripts and optional session transcripts.

## Commands

### 1) Preflight nudge

```bash
./tools/terminal_guard.sh nudge -- rg -n "stageRunId" docs/signals/delegation-tuning.jsonl
```

### 2) Guarded execution

```bash
./tools/terminal_guard.sh run --timeout 20 -- rg -n "stageRunId" docs/signals/delegation-tuning.jsonl
```

- Appends telemetry rows to `docs/signals/terminal-guard.jsonl` by default.
- Use `--no-log` to suppress telemetry for one-off commands.

### 3) Command profile

```bash
./tools/terminal_guard.sh profile --top 20
```

With transcript enrichment:

```bash
./tools/terminal_guard.sh profile --top 20 --transcript /path/to/session.jsonl
```

## Nudge examples

- `search-without-timeout`: add timeout and explicit path scope.
- `watch-command`: run async/background for long-lived dev/watch commands.
- `high-output-lines` or `high-output-bytes`: cap output with `head`/`tail`/`-m` or redirect to file.
- `interactive-git-command`: avoid interactive flags in automation paths.
