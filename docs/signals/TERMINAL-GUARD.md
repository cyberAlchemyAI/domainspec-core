# Terminal Guard

`tools/terminal_guard.sh` helps prevent terminal-driven agent stalls by:

- nudging risky command shapes before execution,
- wrapping command execution with timeout + output monitoring,
- auto-retrying failures with safer recovery settings,
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

### 3) Auto guarded execution (nudge + run + recovery)

```bash
./tools/terminal_guard.sh auto --timeout 30 --retry-timeout 15 -- rg -n "stageRunId" docs/signals/delegation-tuning.jsonl
```

- Runs preflight nudges automatically.
- Executes under guard with timeout/output monitoring.
- Retries once by default (`--max-retries` is configurable).

### 4) Guarded shell (all commands in-session go through guard)

```bash
./tools/terminal_guard.sh shell --timeout 120 --retry-timeout 45
```

- Use this when you want every command in that terminal session to be guarded.
- Supports `cd` as a built-in and routes all other commands through auto mode.

### 5) Convenience wrappers (recommended default)

```bash
./tools/guard <command> [args...]
./tools/guard
./tools/guard-shell
```

- `./tools/guard <command>` runs `terminal_guard auto`.
- `./tools/guard` starts guarded shell mode.
- `./tools/guard-shell` starts guarded shell mode explicitly.

### 6) Command profile

```bash
./tools/terminal_guard.sh profile --top 20
```

With transcript enrichment:

```bash
./tools/terminal_guard.sh profile --top 20 --transcript /path/to/session.jsonl
```

## Nudge examples

- `search-without-timeout`: add timeout and explicit path scope.
- `backtick-substitution-risk`: backticks can trigger shell command substitution; use single quotes or escape backticks.
- `watch-command`: run async/background for long-lived dev/watch commands.
- `high-output-lines` or `high-output-bytes`: cap output with `head`/`tail`/`-m` or redirect to file.
- `interactive-git-command`: avoid interactive flags in automation paths.
