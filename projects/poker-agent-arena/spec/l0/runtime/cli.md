# Local Arena CLI v0 Runtime CLI

Status: frozen for MVP implementation

## Command Namespace

The Local Arena CLI v0 command namespace is `paa`. During local execution the
same commands must be reachable through:

```sh
PYTHONPATH=projects/poker-agent-arena/src python3 -m poker_agent_arena.cli <command>
```

## Commands

### `paa doctor`

Checks that the local package, L0 fixture files, and bundled sample agents are
present. It prints one JSON object with:

- `ok`: boolean,
- `version`: protocol version,
- `checks`: named check results,
- `missing`: missing paths or capabilities.

### `paa run`

Runs one Kuhn hidden-information match between two local agent commands.

Required options:

- `--agent-a <path-or-command>`
- `--agent-b <path-or-command>`
- `--out <directory>`

Optional options:

- `--fixture kuhn_hidden_info` (default)
- `--seed-handle <handle>` (default: first smoke seed)
- `--decision-timeout-ms <int>` (default: `5000`)
- `--process-kill-after-ms <int>` (default: `10000`)

### `paa eval`

Runs a deterministic seat-rotated Kuhn smoke orbit. It writes a private
transcript, diagnostics report, and machine-readable summary under `--out`.

Required options:

- `--agent-a <path-or-command>`
- `--agent-b <path-or-command>`
- `--out <directory>`

Optional options are the same as `paa run`, plus:

- `--fixture kuhn_hidden_info` (default)
- `--max-hands <int>` to cap the smoke orbit for tests.

### `paa replay`

Replays a private transcript and exports redacted public replay material.

Required arguments:

- private transcript JSONL path.

Required options:

- `--out <directory>`

The command writes:

- `replay-report.json`,
- `public-replay.json`,
- `diagnostics-report.json`.

## Exit Codes

- `0`: command completed and required checks passed.
- `1`: command completed but found validation failures.
- `2`: command input or path error.
