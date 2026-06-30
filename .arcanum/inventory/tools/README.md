# inventory tools

## `inventory-update.cjs` — deterministic inventory record appender (SWU-1 + SWU-2)

Appends ONE record to `.arcanum/inventory/index.json` (updating all seven index maps
consistently) and appends the matching row to the human `index.md` catalog — so neither
index is hand-edited, and neither drifts.

```bash
node tools/inventory-update.cjs add <record.json> --timestamp <iso8601> [--index <dir|file>] [--dry-run]
```

- `--timestamp` is **required** — it becomes `generated_at`. There is no wall-clock
  fallback; the tool refuses to run without it. This is what makes runs reproducible.
- `--index` defaults to the inventory root (`tools/..`); may be a dir (reads
  `index.json` inside) or a file path.
- `--dry-run` reports the change without writing.
- Existing id → **no-op** (idempotent; `generated_at` is not bumped, so re-running is
  byte-identical). `--replace` is **not implemented** (deferred — see below).

Programmatic: `require('./inventory-update.cjs')` exports `addRecord`,
`normalizeEntry`, `serialize`, `validate`, `parseControlledTags`. `addRecord` is pure
(returns a new index; never mutates its input).

### Determinism contract (verified)
1. Timestamp is an input, never wall-clock.
2. Append-only, deduped map updates; no key reordering. `by_id[id] = path` (string),
   the other six maps are `key -> [entry-ids]`.
3. Idempotent on existing id (byte-identical no-op).
4. Serialization: `JSON.stringify(out, null, 2) + "\n"`.

### `by_evidence_set` normalization
New records are written in the **normalized** form `set-id -> [entry-id]`, mirroring
`by_evidence_card`. The 13 legacy keys (`entry-id -> "entry-id"` string form) are left
untouched — migrating them is **SWU-3** (touches existing data; run once, deliberately).

### index.md row sync (SWU-2)
The `add` command also appends a row to the matching `index.md` table. Routing is by
**path prefix, not `kind`** — the data proves `kind` is ambiguous (`kind: page` appears
under `wiki/`, `entries/`, and `../`), while every row in a given table shares a path
prefix:

- `entries/` → `## Entries` · `wiki/` → `## Wiki Pages` · `queries/` → `## Query Files`
  · `lint/` → `## Lint Files`
- any other prefix (`../`, `raw/`, `../../…`) was human-placed with no rule → the tool
  **warns and skips** the md row (json still updates); add that row by hand.

Row shape: `| [path](path) | type | \`tag\`, … | summary |`; `|` and newlines in cells are
escaped. Idempotent (an existing `[path](path)` link in the table → no-op), and it will
**repair** a missing md row even when the json entry already exists. The human
`Last updated:` line is left untouched (residue — human owns that annotation).

### Test (toy_game falsification suites)
```bash
node tools/test/test-inventory-update.cjs   # SWU-1: json determinism (6 groups)
node tools/test/test-index-md.cjs           # SWU-2: index.md row sync (7 groups)
```
SWU-1 falsifies determinism: reproducibility (byte-identical across runs), idempotency
(no-op re-apply), known deltas (7 maps + entries + generated_at; legacy key preserved),
validity (JSON round-trip, unique ids), golden snapshot (`expected.index.json` baseline),
timestamp-required. SWU-2: routing, insertion position, table isolation, unknown-path
no-op, idempotency, determinism, cell-pipe escaping. All pass.

### Measured format delta (the deferred operational concern, quantified)
Reserializing the current real `index.json` (Python-written) through this tool with **no
record change** differs by exactly **one byte**: the real file has no trailing newline,
this tool adds one. Nothing else changes (key order, separators, unicode all match
`json.dump(indent=2)`). So the first real run adds a single `\n`; every run after is
byte-stable. The design's "may reformat the whole file" worry was overstated.

### Deferred
- **SWU-3** — one-shot `by_evidence_set` legacy-key migration (the 13 string-form keys)
  to the normalized array form. Touches existing data; run once, deliberately.
- `--replace` — in-place update of an existing id (the MVP only no-ops existing ids).

Built by refine run `20260629T0700Z-inventory-js-updater` → task-session (SWU-1 + SWU-2).
